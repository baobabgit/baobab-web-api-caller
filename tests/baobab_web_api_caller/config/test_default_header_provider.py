"""Tests de `DefaultHeaderProvider`."""

from __future__ import annotations

from typing import Mapping, cast

import pytest

from baobab_web_api_caller.config.default_header_provider import DefaultHeaderProvider
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestDefaultHeaderProvider:
    """Tests unitaires pour `DefaultHeaderProvider`."""

    def test_apply_merges_headers_without_overriding_request(self) -> None:
        """Les headers de la requête priment."""

        provider = DefaultHeaderProvider(default_headers={"Accept": "application/json", "X": "1"})
        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={},
            headers={"X": "2"},
        )
        out = provider.apply(req)
        assert out is not req
        assert dict(out.headers) == {"Accept": "application/json", "X": "2"}

    def test_apply_returns_same_request_when_no_default_headers(self) -> None:
        """Évite de recréer si rien à appliquer."""

        provider = DefaultHeaderProvider(default_headers={})
        req = BaobabRequest(method=HttpMethod.GET, path="/v1/items", query_params={}, headers={})
        assert provider.apply(req) is req

    def test_invalid_headers_raise(self) -> None:
        """Valide str->str."""

        with pytest.raises(ConfigurationException):
            DefaultHeaderProvider(default_headers=cast(Mapping[str, str], {"X": 1}))
