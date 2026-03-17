"""Stratégie d'authentification neutre."""

from __future__ import annotations

from baobab_web_api_caller.auth.authentication_strategy import AuthenticationStrategy
from baobab_web_api_caller.core.baobab_request import BaobabRequest


class NoAuthenticationStrategy(AuthenticationStrategy):
    """Ne modifie pas la requête (aucune authentification)."""

    def apply(self, request: BaobabRequest) -> BaobabRequest:
        """Retourne la requête inchangée."""

        return request
