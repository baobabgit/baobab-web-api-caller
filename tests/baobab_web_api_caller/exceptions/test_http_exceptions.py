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

        assert str(HttpException("http")) == "http"
        assert str(ClientHttpException("client")) == "client"
        assert str(ServerHttpException("server")) == "server"
        assert str(ResourceNotFoundException("404")) == "404"
        assert str(RateLimitException("429")) == "429"
