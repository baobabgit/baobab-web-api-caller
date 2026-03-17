"""Tests de `NoAuthenticationStrategy`."""

from __future__ import annotations

from baobab_web_api_caller.auth.no_authentication_strategy import NoAuthenticationStrategy
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod


class TestNoAuthenticationStrategy:
    """Tests unitaires pour `NoAuthenticationStrategy`."""

    def test_apply_returns_same_request_instance(self) -> None:
        """Vérifie qu'aucune mutation n'est nécessaire."""

        req = BaobabRequest(method=HttpMethod.GET, path="/v1/items", query_params={}, headers={})
        strategy = NoAuthenticationStrategy()
        out = strategy.apply(req)
        assert out is req
