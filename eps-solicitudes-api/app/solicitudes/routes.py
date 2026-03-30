from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Medicamento, Solicitud
from app.serialization import iso_datetime
from app.solicitudes import solicitudes_bp
from app.validators import parse_email


@solicitudes_bp.get("/medicamentos")
@jwt_required()
def list_medicamentos():
    items = Medicamento.query.order_by(Medicamento.nombre).all()
    return jsonify(
        [
            {
                "id": m.id,
                "nombre": m.nombre,
                "es_pos": m.es_pos,
            }
            for m in items
        ]
    )


@solicitudes_bp.post("/solicitudes")
@jwt_required()
def crear_solicitud():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    try:
        medicamento_id = int(data.get("medicamento_id"))
    except (TypeError, ValueError):
        return jsonify({"error": "medicamento_id es obligatorio y debe ser numérico"}), 400

    med = db.session.get(Medicamento, medicamento_id)
    if not med:
        return jsonify({"error": "Medicamento no encontrado"}), 404

    extra = {}
    if not med.es_pos:
        numero_orden = (data.get("numero_orden") or "").strip()
        direccion = (data.get("direccion") or "").strip()
        telefono = (data.get("telefono") or "").strip()
        correo = parse_email(data.get("correo"))

        if not numero_orden:
            return jsonify({"error": "Número de orden es obligatorio para medicamentos NO POS"}), 400
        if not direccion:
            return jsonify({"error": "Dirección es obligatoria para medicamentos NO POS"}), 400
        if not telefono:
            return jsonify({"error": "Teléfono es obligatorio para medicamentos NO POS"}), 400
        if not correo:
            return jsonify({"error": "Correo electrónico válido es obligatorio para medicamentos NO POS"}), 400

        extra = {
            "numero_orden": numero_orden,
            "direccion": direccion,
            "telefono": telefono,
            "correo": correo,
        }
    else:
        extra = {
            "numero_orden": None,
            "direccion": None,
            "telefono": None,
            "correo": None,
        }

    sol = Solicitud(usuario_id=user_id, medicamento_id=medicamento_id, **extra)
    db.session.add(sol)
    db.session.commit()

    return (
        jsonify(
            {
                "id": sol.id,
                "medicamento_id": sol.medicamento_id,
                "medicamento_nombre": med.nombre,
                "es_pos": med.es_pos,
                "numero_orden": sol.numero_orden,
                "direccion": sol.direccion,
                "telefono": sol.telefono,
                "correo": sol.correo,
                "created_at": iso_datetime(sol.created_at),
            }
        ),
        201,
    )


@solicitudes_bp.get("/solicitudes")
@jwt_required()
def listar_solicitudes():
    user_id = int(get_jwt_identity())
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    if page < 1:
        page = 1
    per_page = min(max(per_page, 1), 100)

    q = Solicitud.query.filter_by(usuario_id=user_id).order_by(Solicitud.created_at.desc())
    total = q.count()
    items = q.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify(
        {
            "items": [
                {
                    "id": s.id,
                    "medicamento_id": s.medicamento_id,
                    "medicamento_nombre": s.medicamento.nombre,
                    "es_pos": s.medicamento.es_pos,
                    "numero_orden": s.numero_orden,
                    "direccion": s.direccion,
                    "telefono": s.telefono,
                    "correo": s.correo,
                    "created_at": iso_datetime(s.created_at),
                }
                for s in items
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page if total else 0,
        }
    )
