"""Implémentation système de `Sleeper`."""

from __future__ import annotations

import time
from dataclasses import dataclass

from baobab_web_api_caller.transport.sleeper import Sleeper


@dataclass(frozen=True, slots=True)
class SystemSleeper(Sleeper):
    """Sleeper basé sur `time.sleep`."""

    def sleep(self, seconds: float) -> None:
        """Attend via `time.sleep`."""

        time.sleep(seconds)
