"""Throttling (intervalle minimal) testable."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_web_api_caller.config.rate_limit_policy import RateLimitPolicy
from baobab_web_api_caller.transport.sleeper import Sleeper
from baobab_web_api_caller.transport.time_provider import TimeProvider


@dataclass(slots=True)
class Throttler:
    """Applique une politique de limitation de débit."""

    rate_limit_policy: RateLimitPolicy
    time_provider: TimeProvider
    sleeper: Sleeper
    _last_call_ts: float | None = None

    def throttle(self) -> None:
        """Attend si nécessaire pour respecter l'intervalle minimal."""

        min_interval = float(self.rate_limit_policy.min_interval_seconds)
        if min_interval <= 0:
            return

        now = float(self.time_provider.monotonic())
        if self._last_call_ts is None:
            self._last_call_ts = now
            return

        elapsed = now - self._last_call_ts
        remaining = min_interval - elapsed
        if remaining > 0:
            self.sleeper.sleep(remaining)
            now = float(self.time_provider.monotonic())

        self._last_call_ts = now
