import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


def _split_origins(raw: str) -> list[str]:
    return [o.strip() for o in raw.split(",") if o.strip()]


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://eps_user:eps_pass@localhost:5432/eps_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    ALLOWED_ORIGINS = _split_origins(
        os.environ.get(
            "ALLOWED_ORIGINS",
            "http://localhost:4200,http://127.0.0.1:4200",
        )
    )
