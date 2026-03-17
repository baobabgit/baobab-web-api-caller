"""Tests de `BasicAuthenticationStrategy`."""

from __future__ import annotations

import base64

import pytest

from baobab_web_api_caller.auth.basic_authentication_strategy import BasicAuthenticationStrategy
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestBasicAuthenticationStrategy:
    """Tests unitaires pour `BasicAuthenticationStrategy`."""

    def test_apply_sets_basic_authorization_header(self) -> None:
        """Ajoute le header Authorization (Basic)."""

        req = BaobabRequest(method=HttpMethod.GET, path="/v1/items", query_params={}, headers={})
        out = BasicAuthenticationStrategy(username="u", password="p").apply(req)

        expected = base64.b64encode(b"u:p").decode("ascii")
        assert dict(out.headers)["Authorization"] == f"Basic {expected}"
        assert not dict(req.headers)

    def test_username_must_not_be_empty(self) -> None:
        """Valide le username."""

        with pytest.raises(ConfigurationException):
            BasicAuthenticationStrategy(username=" ", password="p")

    def test_username_must_not_contain_colon(self) -> None:
        """Évite l'ambiguïté user:pass."""

        with pytest.raises(ConfigurationException):
            BasicAuthenticationStrategy(username="u:", password="p")
