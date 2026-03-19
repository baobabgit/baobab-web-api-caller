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

        ErrorResponseMapper().raise_for_error(
            BaobabResponse(status_code=200, headers={}, text="ok")
        )

    def test_maps_401_with_context(self) -> None:
        """401 -> AuthenticationException avec contexte enrichi."""

        response = BaobabResponse(
            status_code=401,
            headers={"Content-Type": "text/plain", "X-Request-Id": "abc"},
            text="unauthorized",
        )

        with pytest.raises(AuthenticationException) as exc_info:
            ErrorResponseMapper().raise_for_error(response)

        err = exc_info.value
        assert err.status_code == 401
        assert "HTTP 401 Unauthorized" in str(err)
        assert err.body_excerpt == "unauthorized"
        assert err.headers == {"Content-Type": "text/plain", "X-Request-Id": "abc"}

    def test_maps_401_includes_www_authenticate(self) -> None:
        """401 -> conserve WWW-Authenticate si présent."""

        response = BaobabResponse(
            status_code=401,
            headers={"WWW-Authenticate": "Bearer", "Content-Type": "text/plain"},
            text="unauthorized",
        )

        with pytest.raises(AuthenticationException) as exc_info:
            ErrorResponseMapper().raise_for_error(response)

        err = exc_info.value
        assert err.status_code == 401
        assert "HTTP 401 Unauthorized" in str(err)
        assert err.body_excerpt == "unauthorized"
        assert err.headers == {
            "WWW-Authenticate": "Bearer",
            "Content-Type": "text/plain",
        }

    def test_maps_404_with_context(self) -> None:
        """404 -> ResourceNotFoundException avec contexte enrichi."""

        response = BaobabResponse(
            status_code=404,
            headers={"Content-Type": "application/json"},
            text='{"error": "not found"}',
        )

        with pytest.raises(ResourceNotFoundException) as exc_info:
            ErrorResponseMapper().raise_for_error(response)

        err = exc_info.value
        assert err.status_code == 404
        assert "HTTP 404 Not Found" in str(err)
        assert err.body_excerpt == '{"error": "not found"}'

    def test_maps_429_with_context(self) -> None:
        """429 -> RateLimitException avec contexte enrichi (Retry-After)."""

        response = BaobabResponse(
            status_code=429,
            headers={"Retry-After": "10"},
            text="too many requests",
        )

        with pytest.raises(RateLimitException) as exc_info:
            ErrorResponseMapper().raise_for_error(response)

        err = exc_info.value
        assert err.status_code == 429
        assert "HTTP 429 Too Many Requests" in str(err)
        assert err.body_excerpt == "too many requests"
        assert err.headers == {"Retry-After": "10"}

    def test_maps_other_4xx(self) -> None:
        """Autres 4xx -> ClientHttpException avec body tronqué si nécessaire."""

        long_body = "x" * 300
        response = BaobabResponse(
            status_code=418,
            headers={"Content-Type": "text/plain"},
            text=long_body,
        )

        with pytest.raises(ClientHttpException) as exc_info:
            ErrorResponseMapper().raise_for_error(response)

        err = exc_info.value
        assert err.status_code == 418
        assert "HTTP 418 Client Error" in str(err)
        assert err.body_excerpt is not None
        assert err.body_excerpt.startswith("x" * 256)
        assert err.body_excerpt.endswith("…")

    def test_maps_5xx(self) -> None:
        """5xx -> ServerHttpException."""

        response = BaobabResponse(
            status_code=503,
            headers={"Content-Type": "text/plain"},
            text="service unavailable",
        )

        with pytest.raises(ServerHttpException) as exc_info:
            ErrorResponseMapper().raise_for_error(response)

        err = exc_info.value
        assert err.status_code == 503
        assert "HTTP 503 Service Unavailable" in str(err)
        assert err.body_excerpt == "service unavailable"

    def test_empty_body_produces_no_excerpt(self) -> None:
        """Body vide -> body_excerpt = None."""

        response = BaobabResponse(
            status_code=500,
            headers={"Content-Type": "text/plain"},
            text="   ",
        )

        with pytest.raises(ServerHttpException) as exc_info:
            ErrorResponseMapper().raise_for_error(response)

        assert exc_info.value.body_excerpt is None

    def test_headers_subset_is_limited(self) -> None:
        """Seuls quelques headers sont conservés dans l'exception."""

        response = BaobabResponse(
            status_code=502,
            headers={
                "Content-Type": "text/plain",
                "X-Request-Id": "abc",
                "X-Other": "ignored",
            },
            text="bad gateway",
        )

        with pytest.raises(ServerHttpException) as exc_info:
            ErrorResponseMapper().raise_for_error(response)

        headers = exc_info.value.headers
        assert headers is not None
        assert "Content-Type" in headers
        assert "X-Request-Id" in headers
        assert "X-Other" not in headers
