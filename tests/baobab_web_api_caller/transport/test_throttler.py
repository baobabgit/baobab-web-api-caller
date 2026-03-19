"""Tests de `Throttler`."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_web_api_caller.config.rate_limit_policy import RateLimitPolicy
from baobab_web_api_caller.transport.sleeper import Sleeper
from baobab_web_api_caller.transport.time_provider import TimeProvider
from baobab_web_api_caller.transport.throttler import Throttler


@dataclass(slots=True)
class FakeTimeProvider(TimeProvider):
    """TimeProvider contrôlable pour les tests."""

    now: float = 0.0

    def monotonic(self) -> float:
        """Retourne le temps contrôlé."""

        return float(self.now)


@dataclass(slots=True)
class FakeSleeper(Sleeper):
    """Sleeper qui avance le temps pendant les tests."""

    time_provider: FakeTimeProvider
    sleeps: list[float]

    def sleep(self, seconds: float) -> None:
        """Mémorise seconds et avance l'horloge de test."""

        seconds_f = float(seconds)
        self.sleeps.append(seconds_f)
        self.time_provider.now += seconds_f


class TestThrottler:
    """Tests unitaires pour `Throttler`."""

    def test_throttle_sleeps_when_min_interval_not_reached(self) -> None:
        """Si elapsed < min_interval, on attend le reste."""

        time_provider = FakeTimeProvider(now=0.0)
        sleeps: list[float] = []
        sleeper = FakeSleeper(time_provider=time_provider, sleeps=sleeps)
        throttler = Throttler(
            rate_limit_policy=RateLimitPolicy(min_interval_seconds=1.0),
            time_provider=time_provider,
            sleeper=sleeper,
        )

        # 1er appel: initialise _last_call_ts, pas de sleep
        throttler.throttle()
        assert not sleeps
        assert throttler._last_call_ts == 0.0  # pylint: disable=protected-access

        # 2e appel: elapsed=0.2 -> remaining=0.8
        time_provider.now = 0.2
        throttler.throttle()

        assert sleeps == [0.8]
        assert throttler._last_call_ts == 1.0  # pylint: disable=protected-access
