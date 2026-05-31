"""Utility helpers for EmuLoader."""


def sanitize_and_trim(input_string: str, max_length: int = 0x1F) -> str:
    """Sanitize and trim a string for safe memory writing."""
    normalized = input_string.replace("'", "").replace("`", "").replace("\u2019", "").strip()
    sanitized = "".join(e for e in normalized if e.isalnum() or e == " ").strip()
    return sanitized.upper()[:max_length]
