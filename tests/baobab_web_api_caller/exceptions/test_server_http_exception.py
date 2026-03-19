"""Tests de `ServerHttpException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.http_exception import HttpException
from baobab_web_api_caller.exceptions.server_http_exception import ServerHttpException


class TestServerHttpException:
    """Tests unitaires pour `ServerHttpException`."""

    def test_inheritance(self) -> None:
        """ServerHttpException doit hériter de HttpException."""

        assert issubclass(ServerHttpException, HttpException)

    def test_instantiation_str_and_status_code(self) -> None:
        """status_code et message sont conservés."""

        exc = ServerHttpException(status_code=500, message="server")
        assert str(exc) == "server"
        assert exc.status_code == 500
