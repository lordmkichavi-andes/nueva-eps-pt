from datetime import datetime, timezone

from app.extensions import db


def _utc_now():
    return datetime.now(timezone.utc)


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=_utc_now)

    solicitudes = db.relationship("Solicitud", backref="usuario", lazy=True)


class Medicamento(db.Model):
    __tablename__ = "medicamentos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    es_pos = db.Column(db.Boolean, nullable=False, default=True)


class Solicitud(db.Model):
    __tablename__ = "solicitudes"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    medicamento_id = db.Column(db.Integer, db.ForeignKey("medicamentos.id"), nullable=False)
    numero_orden = db.Column(db.String(100), nullable=True)
    direccion = db.Column(db.String(500), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    correo = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=_utc_now)

    medicamento = db.relationship("Medicamento", lazy="joined")
