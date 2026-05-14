from flask import Flask

from config import MAX_UPLOAD_SIZE
from database import init_db
from routes.api import api_bp
from routes.contracts import contracts_bp


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE
    app.register_blueprint(contracts_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        init_db()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
