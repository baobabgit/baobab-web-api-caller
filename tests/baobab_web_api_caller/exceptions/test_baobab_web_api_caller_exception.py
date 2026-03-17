"""Tests de `BaobabWebApiCallerException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)


class TestBaobabWebApiCallerException:
    """Tests unitaires pour `BaobabWebApiCallerException`."""

    def test_is_exception(self) -> None:
        """Vérifie l'héritage depuis `Exception`."""

        assert issubclass(BaobabWebApiCallerException, Exception)

    def test_can_be_instantiated(self) -> None:
        """Vérifie l'instanciation avec message."""

        exc = BaobabWebApiCallerException("boom")
        assert str(exc) == "boom"
