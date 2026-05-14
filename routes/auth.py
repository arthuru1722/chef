from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from database import create_user, get_user_by_username, has_users, mark_user_login
from services.auth import validate_csrf

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/setup", methods=["GET", "POST"])
def setup():
    if has_users():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        validate_csrf()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if len(username) < 3:
            flash("Use um usuario com pelo menos 3 caracteres.")
        elif len(password) < 10:
            flash("Use uma senha com pelo menos 10 caracteres.")
        elif password != confirm:
            flash("As senhas nao conferem.")
        else:
            user_id = create_user(username, password)
            session.clear()
            session["user_id"] = user_id
            session["username"] = username
            return redirect(url_for("contracts.index"))

    return render_template("setup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if not has_users():
        return redirect(url_for("auth.setup"))

    if request.method == "POST":
        validate_csrf()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_user_by_username(username)

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            mark_user_login(user["id"])
            next_url = request.args.get("next") or url_for("contracts.index")
            if not next_url.startswith("/"):
                next_url = url_for("contracts.index")
            return redirect(next_url)

        flash("Usuario ou senha invalidos.")

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    validate_csrf()
    session.clear()
    return redirect(url_for("auth.login"))
