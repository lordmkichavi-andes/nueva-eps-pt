"""Formato de salida hacia el cliente (API JSON)."""
from typing import Optional


def iso_datetime(dt) -> Optional[str]:
    """ISO 8601 parseable por el front (no concatenar 'Z' si ya hay offset)."""
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.isoformat()
    return dt.isoformat() + "Z"
