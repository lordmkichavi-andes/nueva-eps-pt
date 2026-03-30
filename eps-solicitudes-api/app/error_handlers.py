"""Handlers globales: respuestas JSON coherentes y mensajes claros para JWT."""
import logging

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith(("/api/", "/auth/")):
            return jsonify({"error": "Recurso no encontrado"}), 404
        return e.get_response() if hasattr(e, "get_response") else (e, 404)

    @app.errorhandler(500)
    def internal_error(e):
        logger.exception("Error interno: %s", e)
        return jsonify({"error": "Error interno del servidor"}), 500


def register_jwt_handlers(jwt: JWTManager) -> None:
    @jwt.unauthorized_loader
    def missing_token(_err):
        return jsonify({"error": "Autenticación requerida"}), 401

    @jwt.invalid_token_loader
    def invalid_token(_err):
        return jsonify({"error": "Token inválido o mal formado"}), 401

    @jwt.expired_token_loader
    def expired_token(_jwt_header, _jwt_payload):
        return jsonify({"error": "Sesión expirada; vuelva a iniciar sesión"}), 401
