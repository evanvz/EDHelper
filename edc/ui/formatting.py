from __future__ import annotations
from typing import Any, Optional

def clean_token(value: Any) -> Any:
    """
    Convert Frontier internal tokens like '$economy_Extraction;' into 'Extraction'.
    If value isn't a token-like string, returns unchanged.
    """
    if not isinstance(value, str):
        return value

    s = value.strip()
    if not s:
        return s

    # Strip the journal token decorations
    if s.startswith("$"):
        s = s[1:]
    if s.endswith(";"):
        s = s[:-1]

    # Remove common prefixes that show up in system meta
    for prefix in ("government_", "economy_", "SYSTEM_SECURITY_", "system_security_"):
        if s.startswith(prefix):
            s = s[len(prefix):]
            break

    s = s.replace("_", " ").strip()
    if s:
        s = s[0].upper() + s[1:]
    return s

def text(value: Any, default: str = "") -> str:
    """
    Safe string conversion for UI display.
    Also cleans token-like strings.
    """
    if value is None:
        return default
    v = clean_token(value)
    if v is None:
        return default
    if isinstance(v, str):
        return v.strip() if v.strip() else default
    return str(v)

def int_commas(value: Any, default: str = "") -> str:
    try:
        if value is None:
            return default
        return f"{int(value):,}"
    except Exception:
        return default

def credits(value: Any, default: str = "") -> str:
    """
    Formats credits as '1,234,567 cr'
    """
    try:
        if value is None:
            return default
        return f"{int(value):,} cr"
    except Exception:
        return default

def pct_1(value: Any, default: str = "") -> str:
    """
    Formats 0..1 floats as '12.3%'. If already 0..100, still works reasonably.
    """
    try:
        if value is None:
            return default
        x = float(value)
        if 0.0 <= x <= 1.0:
            x *= 100.0
        return f"{x:.1f}%"
    except Exception:
        return default

def join_meta(*parts: Optional[str], sep: str = " | ") -> str:
    items = []
    for p in parts:
        if not p:
            continue
        s = str(p).strip()
        if s:
            items.append(s)
    return sep.join(items)