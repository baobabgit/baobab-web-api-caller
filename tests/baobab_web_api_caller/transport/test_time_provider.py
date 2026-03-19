"""Tests de `TimeProvider`."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from baobab_web_api_caller.transport.time_provider import TimeProvider


@dataclass(frozen=True, slots=True)
class FakeTimeProvider(TimeProvider):
    """Implémentation concrète locale pour tester le contrat abstrait."""

    value: float = 0.0

    def monotonic(self) -> float:
        """Retourne la valeur configurée."""

        return float(self.value)


class TestTimeProvider:
    """Tests unitaires pour `TimeProvider`."""

    def test_is_abstract(self) -> None:
        """La classe abstraite ne doit pas être instanciée."""

        with pytest.raises(TypeError):
            TimeProvider()  # pyright: ignore[reportGeneralTypeIssues]

    def test_fake_time_provider_returns_value(self) -> None:
        """monotonic() doit renvoyer la valeur attendue."""

        provider = FakeTimeProvider(value=42.0)
        assert provider.monotonic() == 42.0

