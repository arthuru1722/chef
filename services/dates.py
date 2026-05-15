import re
import unicodedata
from datetime import datetime
from difflib import get_close_matches


MONTHS = {
    "janeiro": 1,
    "fevereiro": 2,
    "marco": 3,
    "março": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
}

MONTH_ALIASES = {
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "sete": 9,
    "setempo": 9,
    "septembro": 9,
    "out": 10,
    "nov": 11,
    "dez": 12,
}


def normalize_text(value):
    value = unicodedata.normalize("NFKD", str(value or "").strip().lower())
    value = value.encode("ASCII", "ignore").decode("ASCII")
    return re.sub(r"[^a-z0-9]", "", value)


def month_number(value):
    normalized = normalize_text(value)
    if not normalized:
        return None
    if normalized.isdigit():
        number = int(normalized)
        return number if 1 <= number <= 12 else None

    month_lookup = {normalize_text(key): number for key, number in MONTHS.items()}
    month_lookup.update({normalize_text(key): number for key, number in MONTH_ALIASES.items()})
    if normalized in month_lookup:
        return month_lookup[normalized]

    match = get_close_matches(normalized, month_lookup.keys(), n=1, cutoff=0.72)
    return month_lookup[match[0]] if match else None


def full_year(value):
    digits = re.sub(r"\D", "", str(value or ""))
    if not digits:
        return None
    if len(digits) == 1:
        return 2020 + int(digits)
    if len(digits) == 2:
        return 2000 + int(digits)
    return int(digits[:4])


def parse_signature_date(values):
    try:
        day = int(str(values.get("dataFinalDia") or "").strip())
        month = month_number(values.get("dataFinalMesExtenso"))
        year = full_year(values.get("dataFinalAnoUltimoDigito"))
        if not month or not year:
            return None
        return datetime(year, month, day)
    except (TypeError, ValueError):
        return None


def signature_label(values):
    date_time = parse_signature_date(values)
    if date_time:
        return date_time.strftime("%d/%m/%Y")
    return ""
