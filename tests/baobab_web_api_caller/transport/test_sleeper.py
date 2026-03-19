"""Tests de `Sleeper`."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from baobab_web_api_caller.transport.sleeper import Sleeper


@dataclass(frozen=True, slots=True)
class FakeSleeper(Sleeper):
    """Implémentation concrète locale pour tester le contrat abstrait."""

    last_seconds: float | None = None

    def sleep(self, seconds: float) -> None:
        """Mémorise la valeur reçue."""

        # Note: dataclass frozen => on utilise object.__setattr__.
        object.__setattr__(self, "last_seconds", float(seconds))


class TestSleeper:
    """Tests unitaires pour `Sleeper`."""

    def test_is_abstract(self) -> None:
        """La classe abstraite ne doit pas être instanciée directement."""

        with pytest.raises(TypeError):
            # pylint: disable=abstract-class-instantiated
            Sleeper()  # type: ignore[abstract]  # pyright: ignore[reportGeneralTypeIssues]

    def test_fake_sleeper_records_seconds(self) -> None:
        """sleep() doit recevoir et stocker la durée demandée."""

        sleeper = FakeSleeper()
        sleeper.sleep(1.25)
        assert sleeper.last_seconds == 1.25
