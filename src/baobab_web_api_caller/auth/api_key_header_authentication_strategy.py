"""Stratégie API key via en-tête HTTP."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_web_api_caller.auth.authentication_strategy import AuthenticationStrategy
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


@dataclass(frozen=True, slots=True)
class ApiKeyHeaderAuthenticationStrategy(AuthenticationStrategy):
    """Ajoute une API key dans un header.

    :param header_name: Nom du header.
    :type header_name: str
    :param api_key: Valeur de la clé.
    :type api_key: str
    :raises ConfigurationException: Si les paramètres sont invalides.
    """

    header_name: str
    api_key: str

    def __post_init__(self) -> None:
        if not isinstance(self.header_name, str) or self.header_name.strip() == "":
            raise ConfigurationException("header_name must be a non-empty string")
        if not isinstance(self.api_key, str) or self.api_key.strip() == "":
            raise ConfigurationException("api_key must be a non-empty string")
        if ":" in self.header_name or " " in self.header_name:
            raise ConfigurationException("header_name must not contain spaces or ':'")

    def apply(self, request: BaobabRequest) -> BaobabRequest:
        """Ajoute/écrase le header API key."""

        return request.with_header(self.header_name, self.api_key)
