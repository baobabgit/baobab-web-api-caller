"""Stratégie Bearer token (Authorization: Bearer <token>)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_web_api_caller.auth.authentication_strategy import AuthenticationStrategy
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


@dataclass(frozen=True, slots=True)
class BearerAuthenticationStrategy(AuthenticationStrategy):
    """Applique un token Bearer dans l'en-tête Authorization.

    :param token: Jeton Bearer (sans le préfixe ``Bearer``).
    :type token: str
    :raises ConfigurationException: Si le token est vide.
    """

    token: str

    def __post_init__(self) -> None:
        if not isinstance(self.token, str) or self.token.strip() == "":
            raise ConfigurationException("token must be a non-empty string")

    def apply(self, request: BaobabRequest) -> BaobabRequest:
        """Ajoute/écrase ``Authorization`` avec ``Bearer <token>``."""

        return request.with_header("Authorization", f"Bearer {self.token}")
