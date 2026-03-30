"""Validación de entrada reutilizable (un solo lugar para reglas de negocio simples)."""
from typing import Optional

from email_validator import EmailNotValidError, validate_email


def parse_email(value: object, *, lower: bool = True) -> Optional[str]:
    """
    Devuelve correo normalizado y válido, o None.
    `lower=True` alinea login/registro; para datos de formulario NO POS también aplica.
    """
    if not value or not isinstance(value, str):
        return None
    text = value.strip()
    if lower:
        text = text.lower()
    try:
        validate_email(text, check_deliverability=False)
        return text
    except EmailNotValidError:
        return None
