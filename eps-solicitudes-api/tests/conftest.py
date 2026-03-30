import pytest

from app import create_app
from app.extensions import db
from app.models import Medicamento


@pytest.fixture
def app():
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "JWT_SECRET_KEY": "test-jwt-secret-key",
            "SECRET_KEY": "test-secret-key",
            "ALLOWED_ORIGINS": ["http://localhost:4200"],
        }
    )
    with application.app_context():
        db.create_all()
        db.session.add_all(
            [
                Medicamento(nombre="Acetaminofén", es_pos=True),
                Medicamento(nombre="NO POS demo", es_pos=False),
            ]
        )
        db.session.commit()
    yield application
    with application.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    r = client.post(
        "/auth/register",
        json={"email": "tester@example.com", "password": "password12"},
    )
    assert r.status_code == 201
    token = r.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
