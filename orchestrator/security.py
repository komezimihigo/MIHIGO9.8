from __future__ import annotations

from typing import Any, Dict


class SecurityPolicy:
    @staticmethod
    def redacted(value: str) -> str:
        if not value:
            return ""
        if len(value) <= 8:
            return "[REDACTED]"
        return value[:2] + "..." + value[-2:]


def ensure_safe_env() -> Dict[str, str]:
    safe: Dict[str, str] = {}
    for key, value in __import__("os").environ.items():
        if any(token in key.lower() for token in ["secret", "token", "password", "key"]):
            safe[key] = SecurityPolicy.redacted(value)
        else:
            safe[key] = value
    return safe
