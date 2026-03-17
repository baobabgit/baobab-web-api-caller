"""Tests de `RequestUrlBuilder`."""

from __future__ import annotations

import pytest

from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.core.request_url_builder import RequestUrlBuilder
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestRequestUrlBuilder:
    """Tests unitaires pour `RequestUrlBuilder`."""

    def test_build_without_query_params(self) -> None:
        """Construit l'URL sans query params."""

        builder = RequestUrlBuilder(base_url="https://example.com")
        req = BaobabRequest(method=HttpMethod.GET, path="/v1/items", query_params={}, headers={})
        assert builder.build(req) == "https://example.com/v1/items"

    def test_build_with_query_params(self) -> None:
        """Construit l'URL avec query params."""

        builder = RequestUrlBuilder(base_url="https://example.com")
        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={"q": "x y", "page": "1"},
            headers={},
        )
        url = builder.build(req)
        assert url.startswith("https://example.com/v1/items?")
        assert "q=x+y" in url
        assert "page=1" in url

    def test_build_with_repeated_query_params(self) -> None:
        """Supporte les clés répétées via séquences."""

        builder = RequestUrlBuilder(base_url="https://example.com")
        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={"tag": ["a", "b"], "page": "1"},
            headers={},
        )
        url = builder.build(req)
        assert url.startswith("https://example.com/v1/items?")
        assert "tag=a" in url
        assert "tag=b" in url
        assert "page=1" in url

    def test_base_url_must_not_end_with_slash(self) -> None:
        """Refuse une base_url avec slash final."""

        with pytest.raises(ConfigurationException):
            RequestUrlBuilder(base_url="https://example.com/")
