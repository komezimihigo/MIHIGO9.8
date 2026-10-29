from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class HealthStatus:
    ok: bool = True
    checks: Dict[str, bool] = field(default_factory=dict)
    details: Dict[str, str] = field(default_factory=dict)


class HealthCheck:
    def __init__(self) -> None:
        self.status = HealthStatus()

    def register(self, name: str, valid: bool, detail: str = "") -> None:
        self.status.checks[name] = valid
        if detail:
            self.status.details[name] = detail
        self.status.ok = all(self.status.checks.values())

    def snapshot(self) -> Dict[str, Any]:
        return {
            "ok": self.status.ok,
            "checks": self.status.checks,
            "details": self.status.details,
        }
