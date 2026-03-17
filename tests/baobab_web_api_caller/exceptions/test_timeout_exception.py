"""Tests de `TimeoutException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.timeout_exception import TimeoutException
from baobab_web_api_caller.exceptions.transport_exception import TransportException


class TestTimeoutException:
    """Tests unitaires pour `TimeoutException`."""

    def test_inheritance(self) -> None:
        """Vérifie l'héritage."""

        assert issubclass(TimeoutException, TransportException)

    def test_instantiation(self) -> None:
        """Vérifie l'instanciation."""

        exc = TimeoutException("timeout")
        assert str(exc) == "timeout"
