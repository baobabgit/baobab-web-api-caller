"""Tests de `ServiceCallException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)
from baobab_web_api_caller.exceptions.service_call_exception import ServiceCallException


class TestServiceCallException:
    """Tests unitaires pour `ServiceCallException`."""

    def test_inheritance(self) -> None:
        """Vérifie l'héritage."""

        assert issubclass(ServiceCallException, BaobabWebApiCallerException)

    def test_instantiation(self) -> None:
        """Vérifie l'instanciation."""

        exc = ServiceCallException("call")
        assert str(exc) == "call"
