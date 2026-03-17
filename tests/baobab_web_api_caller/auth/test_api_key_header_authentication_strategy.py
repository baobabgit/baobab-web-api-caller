"""Tests de `ApiKeyHeaderAuthenticationStrategy`."""

from __future__ import annotations

import pytest

from baobab_web_api_caller.auth.api_key_header_authentication_strategy import (
    ApiKeyHeaderAuthenticationStrategy,
)
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestApiKeyHeaderAuthenticationStrategy:
    """Tests unitaires pour `ApiKeyHeaderAuthenticationStrategy`."""

    def test_apply_sets_api_key_header(self) -> None:
        """Ajoute le header paramétré."""

        req = BaobabRequest(method=HttpMethod.GET, path="/v1/items", query_params={}, headers={})
        out = ApiKeyHeaderAuthenticationStrategy(header_name="X-Api-Key", api_key="k").apply(req)

        assert dict(out.headers)["X-Api-Key"] == "k"
        assert not dict(req.headers)

    def test_header_name_must_be_non_empty(self) -> None:
        """Valide le nom de header."""

        with pytest.raises(ConfigurationException):
            ApiKeyHeaderAuthenticationStrategy(header_name=" ", api_key="k")

    def test_api_key_must_be_non_empty(self) -> None:
        """Valide la clé."""

        with pytest.raises(ConfigurationException):
            ApiKeyHeaderAuthenticationStrategy(header_name="X", api_key=" ")
