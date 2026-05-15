import json
from datetime import datetime, timedelta

from data.defaults import normalize_old_keys
from services.dates import parse_signature_date, signature_label


def values_from_row(row):
    return normalize_old_keys(json.loads(row["dados"]))


def parse_datetime(day, month, year, hour="0", minute="0"):
    try:
        year = str(year or "").strip()
        if len(year) == 2:
            year = f"20{year}"
        return datetime(
            int(year),
            int(month),
            int(day),
            int(hour or 0),
            int(minute or 0),
        )
    except (TypeError, ValueError):
        return None


def event_datetime(values):
    return parse_datetime(
        values.get("diaEvento"),
        values.get("mesEvento"),
        values.get("anoEvento"),
        values.get("horaEvento"),
        values.get("minutoEvento"),
    )


def payment_date(values, installment):
    prefix = f"parcela{installment}"
    return parse_datetime(
        values.get(f"{prefix}Dia"),
        values.get(f"{prefix}Mes"),
        values.get(f"{prefix}Ano"),
    )


def address(values):
    parts = [
        values.get("ruaEvento"),
        values.get("numeroEvento"),
        values.get("bairroEvento"),
        values.get("cidadeEvento"),
        values.get("estadoEvento"),
    ]
    return ", ".join(part for part in parts if part)


def seconds_until(date_time, now=None):
    if date_time is None:
        return None
    now = now or datetime.now()
    return int((date_time - now).total_seconds())


def iso_or_none(date_time):
    return date_time.isoformat(timespec="minutes") if date_time else None


def contract_summary(row, now=None):
    values = values_from_row(row)
    event_at = event_datetime(values)
    payment1 = payment_date(values, 1)
    payment2 = payment_date(values, 2)
    signed_at = parse_signature_date(values)
    return {
        "id": row["id"],
        "titulo": row["titulo"],
        "nomeContratante": values.get("nomeContratante", ""),
        "tipoEvento": values.get("tipoEvento", ""),
        "evento": {
            "dataHora": iso_or_none(event_at),
            "data": event_at.date().isoformat() if event_at else None,
            "hora": event_at.strftime("%H:%M") if event_at else None,
            "segundosAteEvento": seconds_until(event_at, now=now),
            "endereco": address(values),
            "realizada": bool(values.get("festaRealizada")),
        },
        "pagamentos": {
            "parcela1": {
                "data": payment1.date().isoformat() if payment1 else None,
                "valor": values.get("parcela1Numero", ""),
                "paga": bool(values.get("parcela1Paga")),
            },
            "parcela2": {
                "data": payment2.date().isoformat() if payment2 else None,
                "valor": values.get("parcela2Numero", ""),
                "paga": bool(values.get("parcela2Paga")),
            },
        },
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
        "assinatura": {
            "data": signed_at.date().isoformat() if signed_at else None,
            "label": signature_label(values),
        },
    }


def row_for_contract_list(row):
    values = values_from_row(row)
    signed_at = parse_signature_date(values)
    event_at = event_datetime(values)
    return {
        "id": row["id"],
        "titulo": row["titulo"],
        "imagem": row["imagem"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "signature_date": signed_at,
        "signature_label": signature_label(values),
        "event_date": event_at,
        "event_label": event_at.strftime("%d/%m/%Y %H:%M") if event_at else "",
        "event_done": bool(values.get("festaRealizada")),
        "payment1_paid": bool(values.get("parcela1Paga")),
        "payment2_paid": bool(values.get("parcela2Paga")),
    }


def sorted_contract_rows(rows):
    contracts = [row_for_contract_list(row) for row in rows]
    return sorted(
        contracts,
        key=lambda item: (
            item["signature_date"] is not None,
            item["signature_date"] or datetime.min,
            item["updated_at"],
        ),
        reverse=True,
    )


def event_time_payload(row):
    values = values_from_row(row)
    event_at = event_datetime(values)
    return {
        "contractId": row["id"],
        "dataHora": iso_or_none(event_at),
        "segundosAteEvento": seconds_until(event_at),
        "realizada": bool(values.get("festaRealizada")),
    }


def payment_payload(row, installment):
    values = values_from_row(row)
    paid_key = f"parcela{installment}Paga"
    date_time = payment_date(values, installment)
    return {
        "contractId": row["id"],
        "parcela": installment,
        "data": date_time.date().isoformat() if date_time else None,
        "valor": values.get(f"parcela{installment}Numero", ""),
        "paga": bool(values.get(paid_key)),
    }


def notification_payload(rows, days=7):
    now = datetime.now()
    end = now + timedelta(days=days)
    notifications = []

    for row in rows:
        summary = contract_summary(row, now=now)
        event_at = event_datetime(values_from_row(row))
        if event_at and now <= event_at <= end and not summary["evento"]["realizada"]:
            notifications.append({
                "tipo": "evento_proximo",
                "contractId": row["id"],
                "titulo": row["titulo"],
                "dataHora": iso_or_none(event_at),
                "segundosAteEvento": seconds_until(event_at, now=now),
            })

        for installment in (1, 2):
            payment = payment_payload(row, installment)
            payment_at = payment_date(values_from_row(row), installment)
            if payment_at and payment_at <= end and not payment["paga"]:
                notifications.append({
                    "tipo": "pagamento_pendente",
                    "contractId": row["id"],
                    "titulo": row["titulo"],
                    "parcela": installment,
                    "data": payment["data"],
                    "atrasado": payment_at < now,
                })

    return {"days": days, "notifications": notifications}
