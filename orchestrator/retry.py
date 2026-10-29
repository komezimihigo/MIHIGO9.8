from __future__ import annotations

import random
import time
from typing import Optional


def backoff_delay(attempt: int, base: float = 2.0, max_delay: float = 120.0) -> float:
    delay = min(base * (2 ** max(0, attempt - 1)), max_delay)
    return delay + random.uniform(0, 0.5 * delay)


def sleep_with_backoff(attempt: int, base: float = 2.0, max_delay: float = 120.0) -> float:
    delay = backoff_delay(attempt, base=base, max_delay=max_delay)
    time.sleep(delay)
    return delay
