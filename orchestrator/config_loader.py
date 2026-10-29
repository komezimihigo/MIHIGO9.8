from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigLoader:
    def __init__(self, path: str = "config/settings.yaml") -> None:
        self.path = Path(path)
        self.data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("PyYAML is required to load configuration.") from exc
        if not self.path.exists():
            raise FileNotFoundError(f"Configuration file missing: {self.path}")
        with self.path.open("r", encoding="utf-8") as fh:
            self.data = yaml.safe_load(fh) or {}

    def get(self, key: str, default: Any = None) -> Any:
        value = self.data
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def require(self, key: str) -> Any:
        value = self.get(key)
        if value in (None, ""):
            raise ValueError(f"Missing required config value: {key}")
        return value
