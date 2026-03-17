"""Tests de `BearerAuthenticationStrategy`."""

from __future__ import annotations

import pytest

from baobab_web_api_caller.auth.bearer_authentication_strategy import BearerAuthenticationStrategy
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestBearerAuthenticationStrategy:
    """Tests unitaires pour `BearerAuthenticationStrategy`."""

    def test_apply_sets_authorization_header(self) -> None:
        """Ajoute le header Authorization."""

        req = BaobabRequest(method=HttpMethod.GET, path="/v1/items", query_params={}, headers={})
        out = BearerAuthenticationStrategy(token="abc").apply(req)
        assert out is not req
        assert not dict(req.headers)
        assert dict(out.headers)["Authorization"] == "Bearer abc"

    def test_token_must_not_be_empty(self) -> None:
        """Valide le token."""

        with pytest.raises(ConfigurationException):
            BearerAuthenticationStrategy(token="  ")
