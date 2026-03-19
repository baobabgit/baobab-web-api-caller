"""Tests de `ClientHttpException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.client_http_exception import ClientHttpException
from baobab_web_api_caller.exceptions.http_exception import HttpException


class TestClientHttpException:
    """Tests unitaires pour `ClientHttpException`."""

    def test_inheritance(self) -> None:
        """ClientHttpException doit hériter de HttpException."""

        assert issubclass(ClientHttpException, HttpException)

    def test_instantiation_str_and_status_code(self) -> None:
        """status_code et message sont conservés."""

        exc = ClientHttpException(status_code=418, message="client")
        assert str(exc) == "client"
        assert exc.status_code == 418

