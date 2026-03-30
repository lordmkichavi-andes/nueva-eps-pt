from flask import Blueprint

solicitudes_bp = Blueprint("solicitudes", __name__, url_prefix="/api")

from app.solicitudes import routes  # noqa: E402, F401
