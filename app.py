from flask import Flask

from config import COOKIE_SECURE, MAX_UPLOAD_SIZE, SECRET_KEY
from database import init_db
from routes.api import api_bp
from routes.auth import auth_bp
from routes.contracts import contracts_bp
from services.auth import csrf_token


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = COOKIE_SECURE
    app.register_blueprint(auth_bp)
    app.register_blueprint(contracts_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        init_db()

    app.jinja_env.globals["csrf_token"] = csrf_token

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
