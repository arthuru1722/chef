from functools import wraps

from flask import Blueprint, abort, jsonify, request

from config import API_TOKEN
from database import get_contract, list_contract_rows, update_contract_values
from services.auth import is_logged_in
from services.contracts import (
    contract_summary,
    event_time_payload,
    notification_payload,
    payment_payload,
    values_from_row,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def require_api_token(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if is_logged_in():
            return view(*args, **kwargs)
        if not API_TOKEN:
            return jsonify({"error": "api_token_not_configured"}), 401
        if API_TOKEN:
            auth = request.headers.get("Authorization", "")
            token = auth.removeprefix("Bearer ").strip()
            if token != API_TOKEN:
                return jsonify({"error": "unauthorized"}), 401
        return view(*args, **kwargs)

    return wrapper


def contract_or_404(contract_id):
    row = get_contract(contract_id)
    if row is None:
        abort(404)
    return row


def bool_from_payload(payload, key):
    if key not in payload:
        return None
    return bool(payload.get(key))


@api_bp.route("/contracts")
@require_api_token
def contracts():
    include_done = request.args.get("include_done", "1") not in {"0", "false", "False"}
    rows = list_contract_rows()
    summaries = [contract_summary(row) for row in rows]
    if not include_done:
        summaries = [item for item in summaries if not item["evento"]["realizada"]]
    return jsonify({"contracts": summaries})


@api_bp.route("/contracts/<int:contract_id>")
@require_api_token
def contract_detail(contract_id):
    row = contract_or_404(contract_id)
    return jsonify({
        "contract": contract_summary(row),
        "dados": values_from_row(row),
    })


@api_bp.route("/contracts/<int:contract_id>/event-time")
@require_api_token
def contract_event_time(contract_id):
    return jsonify(event_time_payload(contract_or_404(contract_id)))


@api_bp.route("/contracts/<int:contract_id>/payments/1")
@require_api_token
def contract_payment_1(contract_id):
    return jsonify(payment_payload(contract_or_404(contract_id), 1))


@api_bp.route("/contracts/<int:contract_id>/payments/2")
@require_api_token
def contract_payment_2(contract_id):
    return jsonify(payment_payload(contract_or_404(contract_id), 2))


@api_bp.route("/contracts/<int:contract_id>/status", methods=["PATCH", "POST"])
@require_api_token
def update_contract_status(contract_id):
    row = contract_or_404(contract_id)
    values = values_from_row(row)
    payload = request.get_json(silent=True) or {}

    allowed_keys = ("festaRealizada", "parcela1Paga", "parcela2Paga")
    for key in allowed_keys:
        value = bool_from_payload(payload, key)
        if value is not None:
            values[key] = value

    update_contract_values(contract_id, values)
    updated_row = contract_or_404(contract_id)
    return jsonify({"contract": contract_summary(updated_row)})


@api_bp.route("/contracts/<int:contract_id>/event/done", methods=["PATCH", "POST"])
@require_api_token
def update_event_done(contract_id):
    row = contract_or_404(contract_id)
    values = values_from_row(row)
    payload = request.get_json(silent=True) or {}
    values["festaRealizada"] = bool(payload.get("realizada", True))
    update_contract_values(contract_id, values)
    return jsonify(event_time_payload(contract_or_404(contract_id)))


@api_bp.route("/contracts/<int:contract_id>/payments/<int:installment>/paid", methods=["PATCH", "POST"])
@require_api_token
def update_payment_paid(contract_id, installment):
    if installment not in {1, 2}:
        abort(404)
    row = contract_or_404(contract_id)
    values = values_from_row(row)
    payload = request.get_json(silent=True) or {}
    values[f"parcela{installment}Paga"] = bool(payload.get("paga", True))
    update_contract_values(contract_id, values)
    return jsonify(payment_payload(contract_or_404(contract_id), installment))


@api_bp.route("/notifications")
@require_api_token
def notifications():
    try:
        days = int(request.args.get("days", "7"))
    except ValueError:
        days = 7
    days = max(1, min(days, 90))
    return jsonify(notification_payload(list_contract_rows(), days=days))
