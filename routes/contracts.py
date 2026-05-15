from io import BytesIO

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, send_file, send_from_directory, url_for

from config import IMAGE_DIR
from data.fields import FIELD_GROUPS
from database import delete_contract, get_contract, list_contract_rows, save_contract, update_contract_values
from pdf.generator import build_contract_pdf, contract_download_name
from services.auth import login_required, validate_csrf
from services.contracts import sorted_contract_rows, values_from_row
from services.forms import empty_values, values_from_form
from services.images import (
    list_image_options,
    normalize_image_ref,
    resolve_image_source,
    selected_image_ref,
    send_uploaded_image,
)
from services.importer import (
    allowed_spreadsheet,
    build_contracts_csv,
    build_template_csv,
    build_template_workbook,
    parse_spreadsheet,
)

contracts_bp = Blueprint("contracts", __name__)


def _contract_or_404(contract_id):
    row = get_contract(contract_id)
    if row is None:
        abort(404)
    return row


def _contract_values(row):
    return values_from_row(row)


def _safe_next(default_endpoint="contracts.index"):
    next_url = request.form.get("next") or request.args.get("next") or url_for(default_endpoint)
    return next_url if next_url.startswith("/") else url_for(default_endpoint)


def _render_form(values, selected_image="", contract_id=""):
    contracts = sorted_contract_rows(list_contract_rows())
    list_filter = request.args.get("filter", "")
    if list_filter == "open":
        contracts = [contract for contract in contracts if not contract["event_done"]]

    return render_template(
        "index.html",
        field_groups=FIELD_GROUPS,
        values=values,
        contracts=contracts,
        list_filter=list_filter,
        images=list_image_options(),
        selected_image=normalize_image_ref(selected_image),
        contract_id=contract_id,
    )


@contracts_bp.route("/")
@login_required
def index():
    return _render_form(empty_values())


@contracts_bp.route("/contrato/<int:contract_id>")
@login_required
def edit_contract(contract_id):
    row = _contract_or_404(contract_id)
    return _render_form(
        _contract_values(row),
        selected_image=row["imagem"] or "",
        contract_id=contract_id,
    )


@contracts_bp.route("/salvar", methods=["POST"])
@login_required
def save_contract_route():
    validate_csrf()
    values = values_from_form(request.form)
    contract_id = request.form.get("contract_id") or None
    current_image = ""

    if contract_id:
        current_row = _contract_or_404(contract_id)
        current_image = current_row["imagem"] or ""
        current_values = _contract_values(current_row)
        for key in ("festaRealizada", "parcela1Paga", "parcela2Paga"):
            values[key] = bool(current_values.get(key))

    image_ref = selected_image_ref(request.form, request.files, current_ref=current_image)
    saved_id = save_contract(values, image_ref, contract_id=contract_id)
    return redirect(url_for("contracts.edit_contract", contract_id=saved_id))


@contracts_bp.route("/contrato/<int:contract_id>/status", methods=["POST"])
@login_required
def update_contract_status_route(contract_id):
    validate_csrf()
    row = _contract_or_404(contract_id)
    values = _contract_values(row)
    for key in ("festaRealizada", "parcela1Paga", "parcela2Paga"):
        if key in request.form:
            values[key] = request.form.get(key) == "1"
    update_contract_values(contract_id, values)
    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify({
            "ok": True,
            "status": {
                "festaRealizada": bool(values.get("festaRealizada")),
                "parcela1Paga": bool(values.get("parcela1Paga")),
                "parcela2Paga": bool(values.get("parcela2Paga")),
            },
        })
    return redirect(_safe_next())


@contracts_bp.route("/importar", methods=["POST"])
@login_required
def import_contracts_route():
    validate_csrf()
    spreadsheet = request.files.get("spreadsheet")
    if not spreadsheet or not spreadsheet.filename:
        flash("Escolha um arquivo .xlsx ou .csv para importar.")
        return redirect(url_for("contracts.index"))
    if not allowed_spreadsheet(spreadsheet.filename):
        flash("Formato invalido. Use .xlsx ou .csv.")
        return redirect(url_for("contracts.index"))

    try:
        contracts = parse_spreadsheet(spreadsheet)
    except Exception:
        flash("Nao consegui ler a planilha. Confira se a primeira linha tem os nomes das colunas.")
        return redirect(url_for("contracts.index"))

    for values in contracts:
        save_contract(values, image_ref="")

    flash(f"{len(contracts)} contrato(s) importado(s).")
    return redirect(url_for("contracts.index"))


@contracts_bp.route("/importar/modelo")
@login_required
def import_template():
    try:
        workbook = build_template_workbook()
        output = BytesIO()
        workbook.save(output)
        output.seek(0)
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="modelo-importacao-contratos.xlsx",
        )
    except ModuleNotFoundError:
        output = BytesIO(build_template_csv())
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="modelo-importacao-contratos.csv",
    )


@contracts_bp.route("/exportar.csv")
@login_required
def export_contracts_csv():
    output = BytesIO(build_contracts_csv(list_contract_rows()))
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="contratos-cheffy.csv",
    )


@contracts_bp.route("/contrato/<int:contract_id>/excluir", methods=["POST"])
@login_required
def delete_contract_route(contract_id):
    validate_csrf()
    _contract_or_404(contract_id)
    delete_contract(contract_id)
    return redirect(url_for("contracts.index"))


@contracts_bp.route("/pdf/<int:contract_id>")
@login_required
def pdf_contract(contract_id):
    row = _contract_or_404(contract_id)
    values = _contract_values(row)
    image_source = resolve_image_source(row["imagem"] or "")
    pdf = build_contract_pdf(values, image_source=image_source)
    return send_file(
        pdf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=contract_download_name(values),
    )


@contracts_bp.route("/uploaded-images/<int:image_id>")
@login_required
def uploaded_image(image_id):
    image = send_uploaded_image(image_id)
    return send_file(
        BytesIO(image["conteudo"]),
        mimetype=image["content_type"],
        download_name=image["nome"],
    )


@contracts_bp.route("/images/<path:filename>")
@login_required
def image_file(filename):
    return send_from_directory(IMAGE_DIR, filename)
