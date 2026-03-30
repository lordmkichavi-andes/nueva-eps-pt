from flask import Flask
from flask_cors import CORS

from app.auth import auth_bp
from app.error_handlers import register_error_handlers, register_jwt_handlers
from app.extensions import db, jwt
from app.solicitudes import solicitudes_bp


def create_app(config_override=None):
    app = Flask(__name__)
    app.config.from_object("config.Config")
    if config_override:
        app.config.update(config_override)

    CORS(
        app,
        origins=app.config["ALLOWED_ORIGINS"],
        supports_credentials=True,
    )

    db.init_app(app)
    jwt.init_app(app)
    register_jwt_handlers(jwt)
    register_error_handlers(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(solicitudes_bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
