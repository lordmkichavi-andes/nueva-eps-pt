import bcrypt
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from app.auth import auth_bp
from app.extensions import db
from app.models import Usuario
from app.validators import parse_email

_MIN_PASSWORD_LEN = 8


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = parse_email(data.get("email"))
    password = data.get("password")

    if not email:
        return jsonify({"error": "Correo electrónico inválido"}), 400
    if not password or not isinstance(password, str) or len(password) < _MIN_PASSWORD_LEN:
        return jsonify({"error": "La contraseña debe tener al menos 8 caracteres"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "El correo ya está registrado"}), 409

    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = Usuario(email=email, password_hash=pw_hash)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El correo ya está registrado"}), 409

    token = create_access_token(identity=str(user.id))
    return jsonify({"message": "Usuario registrado", "access_token": token, "user": {"id": user.id, "email": user.email}}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = parse_email(data.get("email"))
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Credenciales inválidas"}), 401

    user = Usuario.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token, "user": {"id": user.id, "email": user.email}})
