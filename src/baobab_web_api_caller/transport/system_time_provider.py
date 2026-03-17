"""Implémentation système de `TimeProvider`."""

from __future__ import annotations

import time
from dataclasses import dataclass

from baobab_web_api_caller.transport.time_provider import TimeProvider


@dataclass(frozen=True, slots=True)
class SystemTimeProvider(TimeProvider):
    """Provider basé sur `time.monotonic`."""

    def monotonic(self) -> float:
        """Retourne `time.monotonic()` en secondes."""

        return time.monotonic()
