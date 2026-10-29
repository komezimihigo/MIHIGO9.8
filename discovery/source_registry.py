from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SourceProvider:
    name: str
    priority: int = 0

    def discover(self, query: str) -> List[Dict[str, Any]]:
        return []


class SourceRegistry:
    def __init__(self) -> None:
        self.providers: List[SourceProvider] = []

    def register(self, provider: SourceProvider) -> None:
        self.providers.append(provider)

    def discover(self, query: str) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for provider in sorted(self.providers, key=lambda p: p.priority, reverse=True):
            results.extend(provider.discover(query))
        return results
