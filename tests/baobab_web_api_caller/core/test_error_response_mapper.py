"""Tests de `ErrorResponseMapper`."""

from __future__ import annotations

import pytest

from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.error_response_mapper import ErrorResponseMapper
from baobab_web_api_caller.exceptions.authentication_exception import AuthenticationException
from baobab_web_api_caller.exceptions.client_http_exception import ClientHttpException
from baobab_web_api_caller.exceptions.rate_limit_exception import RateLimitException
from baobab_web_api_caller.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from baobab_web_api_caller.exceptions.server_http_exception import ServerHttpException


class TestErrorResponseMapper:
    """Tests unitaires pour `ErrorResponseMapper`."""

    def test_no_error_does_not_raise(self) -> None:
        """< 400 ne doit pas lever."""

        ErrorResponseMapper().raise_for_error(BaobabResponse(status_code=200, headers={}))

    def test_maps_401(self) -> None:
        """401 -> AuthenticationException."""

        with pytest.raises(AuthenticationException):
            ErrorResponseMapper().raise_for_error(BaobabResponse(status_code=401, headers={}))

    def test_maps_404(self) -> None:
        """404 -> ResourceNotFoundException."""

        with pytest.raises(ResourceNotFoundException):
            ErrorResponseMapper().raise_for_error(BaobabResponse(status_code=404, headers={}))

    def test_maps_429(self) -> None:
        """429 -> RateLimitException."""

        with pytest.raises(RateLimitException):
            ErrorResponseMapper().raise_for_error(BaobabResponse(status_code=429, headers={}))

    def test_maps_other_4xx(self) -> None:
        """Autres 4xx -> ClientHttpException."""

        with pytest.raises(ClientHttpException):
            ErrorResponseMapper().raise_for_error(BaobabResponse(status_code=418, headers={}))

    def test_maps_5xx(self) -> None:
        """5xx -> ServerHttpException."""

        with pytest.raises(ServerHttpException):
            ErrorResponseMapper().raise_for_error(BaobabResponse(status_code=503, headers={}))
