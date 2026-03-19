"""Tests de `RateLimitException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.client_http_exception import ClientHttpException
from baobab_web_api_caller.exceptions.rate_limit_exception import RateLimitException


class TestRateLimitException:
    """Tests unitaires pour `RateLimitException`."""

    def test_inheritance(self) -> None:
        """RateLimitException doit hériter de ClientHttpException."""

        assert issubclass(RateLimitException, ClientHttpException)

    def test_instantiation_str_and_status_code(self) -> None:
        """status_code et message sont conservés."""

        exc = RateLimitException(status_code=429, message="429")
        assert str(exc) == "429"
        assert exc.status_code == 429
