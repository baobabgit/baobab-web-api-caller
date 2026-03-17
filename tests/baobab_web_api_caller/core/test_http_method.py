"""Tests de `HttpMethod`."""

from __future__ import annotations

from baobab_web_api_caller.core.http_method import HttpMethod


class TestHttpMethod:
    """Tests unitaires pour `HttpMethod`."""

    def test_contains_expected_methods(self) -> None:
        """Vérifie la présence des verbes attendus."""

        assert HttpMethod.GET.value == "GET"
        assert HttpMethod.POST.value == "POST"
        assert HttpMethod.PUT.value == "PUT"
        assert HttpMethod.PATCH.value == "PATCH"
        assert HttpMethod.DELETE.value == "DELETE"
        assert HttpMethod.HEAD.value == "HEAD"
        assert HttpMethod.OPTIONS.value == "OPTIONS"
