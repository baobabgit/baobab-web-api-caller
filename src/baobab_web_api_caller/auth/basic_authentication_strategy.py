"""Stratégie Basic auth (Authorization: Basic <base64(user:pass)>)."""

from __future__ import annotations

import base64
from dataclasses import dataclass

from baobab_web_api_caller.auth.authentication_strategy import AuthenticationStrategy
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


@dataclass(frozen=True, slots=True)
class BasicAuthenticationStrategy(AuthenticationStrategy):
    """Applique l'authentification HTTP Basic.

    Notes de sécurité:
    - Cette stratégie ne réalise pas de chiffrement. En production, l'usage doit se faire sur TLS.
    - Les identifiants ne doivent pas être loggés.

    :param username: Nom d'utilisateur.
    :type username: str
    :param password: Mot de passe.
    :type password: str
    :raises ConfigurationException: Si les paramètres sont invalides.
    """

    username: str
    password: str

    def __post_init__(self) -> None:
        if not isinstance(self.username, str) or self.username.strip() == "":
            raise ConfigurationException("username must be a non-empty string")
        if not isinstance(self.password, str):
            raise ConfigurationException("password must be a string")
        if ":" in self.username:
            raise ConfigurationException("username must not contain ':'")

    def apply(self, request: BaobabRequest) -> BaobabRequest:
        """Ajoute/écrase ``Authorization`` avec l'en-tête Basic."""

        raw = f"{self.username}:{self.password}".encode("utf-8")
        token = base64.b64encode(raw).decode("ascii")
        return request.with_header("Authorization", f"Basic {token}")
