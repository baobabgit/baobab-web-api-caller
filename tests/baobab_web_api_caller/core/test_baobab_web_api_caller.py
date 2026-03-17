"""Tests de `BaobabWebApiCaller` (abstraction)."""

from __future__ import annotations

import inspect

from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.baobab_web_api_caller import BaobabWebApiCaller
from baobab_web_api_caller.core.http_method import HttpMethod


class ConcreteCaller(BaobabWebApiCaller):
    """Implémentation concrète pour tests."""

    def call(self, request: BaobabRequest) -> BaobabResponse:
        return BaobabResponse(status_code=200, headers={"X": request.path})


class TestBaobabWebApiCaller:
    """Tests unitaires pour `BaobabWebApiCaller`."""

    def test_is_abstract(self) -> None:
        """Vérifie que la classe est abstraite."""

        assert inspect.isabstract(BaobabWebApiCaller)
        assert "call" in getattr(BaobabWebApiCaller, "__abstractmethods__", set())

    def test_concrete_implementation_can_be_used(self) -> None:
        """Teste via une implémentation concrète."""

        caller = ConcreteCaller()
        req = BaobabRequest(method=HttpMethod.GET, path="/ping", query_params={}, headers={})
        resp = caller.call(req)
        assert resp.status_code == 200
        assert dict(resp.headers) == {"X": "/ping"}
