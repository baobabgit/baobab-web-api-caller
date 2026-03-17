"""Tests de `ApiKeyQueryAuthenticationStrategy`."""

from __future__ import annotations

import pytest

from baobab_web_api_caller.auth.api_key_query_authentication_strategy import (
    ApiKeyQueryAuthenticationStrategy,
)
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestApiKeyQueryAuthenticationStrategy:
    """Tests unitaires pour `ApiKeyQueryAuthenticationStrategy`."""

    def test_apply_sets_query_param(self) -> None:
        """Ajoute le query param paramétré."""

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={"q": "x"},
            headers={"X-Test": "1"},
        )
        out = ApiKeyQueryAuthenticationStrategy(param_name="api_key", api_key="k").apply(req)

        assert dict(req.query_params) == {"q": "x"}
        assert dict(out.query_params) == {"q": "x", "api_key": "k"}

    def test_apply_appends_api_key_when_param_already_present(self) -> None:
        """Ajoute l'API key en conservant les valeurs existantes."""

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={"api_key": "existing"},
            headers={},
        )
        out = ApiKeyQueryAuthenticationStrategy(param_name="api_key", api_key="k").apply(req)

        assert dict(req.query_params) == {"api_key": "existing"}
        assert dict(out.query_params) == {"api_key": ("existing", "k")}

    def test_param_name_must_be_non_empty(self) -> None:
        """Valide le nom du paramètre."""

        with pytest.raises(ConfigurationException):
            ApiKeyQueryAuthenticationStrategy(param_name=" ", api_key="k")

    def test_api_key_must_be_non_empty(self) -> None:
        """Valide la clé."""

        with pytest.raises(ConfigurationException):
            ApiKeyQueryAuthenticationStrategy(param_name="k", api_key=" ")
