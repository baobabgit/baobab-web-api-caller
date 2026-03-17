"""Tests de `TransportException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)
from baobab_web_api_caller.exceptions.transport_exception import TransportException


class TestTransportException:
    """Tests unitaires pour `TransportException`."""

    def test_inheritance(self) -> None:
        """Vérifie l'héritage."""

        assert issubclass(TransportException, BaobabWebApiCallerException)

    def test_instantiation(self) -> None:
        """Vérifie l'instanciation."""

        exc = TransportException("network")
        assert str(exc) == "network"
