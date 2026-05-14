from io import BytesIO

from flask import Blueprint, abort, redirect, render_template, request, send_file, send_from_directory, url_for

from config import IMAGE_DIR
from data.fields import FIELD_GROUPS
from database import delete_contract, get_contract, list_contracts, save_contract
from pdf.generator import build_contract_pdf, contract_download_name
from services.auth import login_required, validate_csrf
from services.contracts import values_from_row
from services.forms import empty_values, values_from_form
from services.images import (
    list_image_options,
    normalize_image_ref,
    resolve_image_source,
    selected_image_ref,
    send_uploaded_image,
)

contracts_bp = Blueprint("contracts", __name__)


def _contract_or_404(contract_id):
    row = get_contract(contract_id)
    if row is None:
        abort(404)
    return row


def _contract_values(row):
    return values_from_row(row)


def _render_form(values, selected_image="", contract_id=""):
    return render_template(
        "index.html",
        field_groups=FIELD_GROUPS,
        values=values,
        contracts=list_contracts(),
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
