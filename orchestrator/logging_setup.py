from __future__ import annotations

import logging
from typing import Optional


def configure_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("mihigo")
    logger.setLevel(level.upper())
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)
    return logger
