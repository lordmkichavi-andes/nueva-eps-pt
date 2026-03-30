"""Ejecutar una vez si la BD se creó sin datos: python seed_medicamentos.py"""
from app import create_app
from app.extensions import db
from app.models import Medicamento

SAMPLE = [
    ("Acetaminofén 500 mg", True),
    ("Ibuprofeno 400 mg", True),
    ("Medicamento especial NO POS A", False),
    ("Medicamento especial NO POS B", False),
]


def run():
    app = create_app()
    with app.app_context():
        if Medicamento.query.first():
            print("Ya existen medicamentos; no se insertó nada.")
            return
        for nombre, es_pos in SAMPLE:
            db.session.add(Medicamento(nombre=nombre, es_pos=es_pos))
        db.session.commit()
        print("Medicamentos de ejemplo insertados.")


if __name__ == "__main__":
    run()
