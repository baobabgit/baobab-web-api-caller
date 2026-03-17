"""Tests de `AuthenticationException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.authentication_exception import AuthenticationException
from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)


class TestAuthenticationException:
    """Tests unitaires pour `AuthenticationException`."""

    def test_inheritance(self) -> None:
        """Vérifie l'héritage."""

        assert issubclass(AuthenticationException, BaobabWebApiCallerException)

    def test_instantiation(self) -> None:
        """Vérifie l'instanciation."""

        exc = AuthenticationException(status_code=401, message="unauthorized")
        assert str(exc) == "unauthorized"
        assert exc.status_code == 401
