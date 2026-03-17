"""Stratégie API key via query parameters."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_web_api_caller.auth.authentication_strategy import AuthenticationStrategy
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


@dataclass(frozen=True, slots=True)
class ApiKeyQueryAuthenticationStrategy(AuthenticationStrategy):
    """Ajoute une API key dans les query params.

    :param param_name: Nom du paramètre.
    :type param_name: str
    :param api_key: Valeur de la clé.
    :type api_key: str
    :raises ConfigurationException: Si les paramètres sont invalides.
    """

    param_name: str
    api_key: str

    def __post_init__(self) -> None:
        if not isinstance(self.param_name, str) or self.param_name.strip() == "":
            raise ConfigurationException("param_name must be a non-empty string")
        if not isinstance(self.api_key, str) or self.api_key.strip() == "":
            raise ConfigurationException("api_key must be a non-empty string")
        if " " in self.param_name:
            raise ConfigurationException("param_name must not contain spaces")

    def apply(self, request: BaobabRequest) -> BaobabRequest:
        """Ajoute/écrase le paramètre API key."""

        query_params: dict[str, str | list[str]] = {}
        for key, value in request.query_params.items():
            if isinstance(value, str):
                query_params[key] = value
            else:
                query_params[key] = list(value)

        existing = query_params.get(self.param_name)
        if existing is None:
            query_params[self.param_name] = self.api_key
        elif isinstance(existing, str):
            query_params[self.param_name] = [existing, self.api_key]
        else:
            existing.append(self.api_key)

        return BaobabRequest(
            method=request.method,
            path=request.path,
            query_params=query_params,
            headers=request.headers,
            json_body=request.json_body,
            form_body=request.form_body,
            timeout_seconds=request.timeout_seconds,
        )
