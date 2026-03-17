"""Tests des exceptions HTTP."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.client_http_exception import ClientHttpException
from baobab_web_api_caller.exceptions.http_exception import HttpException
from baobab_web_api_caller.exceptions.rate_limit_exception import RateLimitException
from baobab_web_api_caller.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from baobab_web_api_caller.exceptions.server_http_exception import ServerHttpException


class TestHttpExceptions:
    """Tests unitaires pour la hiérarchie HTTP."""

    def test_http_exception_inheritance(self) -> None:
        """Vérifie l'héritage de base."""

        assert issubclass(ClientHttpException, HttpException)
        assert issubclass(ServerHttpException, HttpException)
        assert issubclass(ResourceNotFoundException, ClientHttpException)
        assert issubclass(RateLimitException, ClientHttpException)

    def test_http_exceptions_instantiation(self) -> None:
        """Vérifie l'instanciation."""

        base = HttpException(status_code=400, message="http")
        assert str(base) == "http"
        assert base.status_code == 400

        client = ClientHttpException(status_code=418, message="client")
        assert str(client) == "client"
        assert client.status_code == 418

        server = ServerHttpException(status_code=500, message="server")
        assert str(server) == "server"
        assert server.status_code == 500

        not_found = ResourceNotFoundException(status_code=404, message="404")
        assert str(not_found) == "404"
        assert not_found.status_code == 404

        rate_limit = RateLimitException(status_code=429, message="429")
        assert str(rate_limit) == "429"
        assert rate_limit.status_code == 429
