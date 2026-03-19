"""Tests de `AuthenticationStrategy`."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from baobab_web_api_caller.auth.authentication_strategy import AuthenticationStrategy
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod


@dataclass(frozen=True, slots=True)
class FakeAuthenticationStrategy(AuthenticationStrategy):
    """Implémentation concrète locale pour tester le contrat abstrait."""

    def apply(self, request: BaobabRequest) -> BaobabRequest:
        """Retourne la requête inchangée (aucune mutation)."""

        return request


class TestAuthenticationStrategy:
    """Tests unitaires pour `AuthenticationStrategy`."""

    def test_is_abstract(self) -> None:
        """La classe abstraite ne doit pas être instanciée directement."""

        with pytest.raises(TypeError):
            AuthenticationStrategy()  # pyright: ignore[reportGeneralTypeIssues]

    def test_apply_contract_returns_request(self) -> None:
        """Une stratégie concrète renvoie une requête typée."""

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={},
            headers={},
        )

        out = FakeAuthenticationStrategy().apply(req)
        assert isinstance(out, BaobabRequest)
        assert out == req

