from typing import Optional

from email_validator import EmailNotValidError, validate_email


def parse_email(value: object, *, lower: bool = True) -> Optional[str]:
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
