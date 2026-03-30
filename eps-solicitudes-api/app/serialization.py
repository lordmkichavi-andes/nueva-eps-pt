from typing import Optional


def iso_datetime(dt) -> Optional[str]:
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.isoformat()
    return dt.isoformat() + "Z"
