"""Mapping des erreurs de réponse vers des exceptions projet."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.exceptions.authentication_exception import AuthenticationException
from baobab_web_api_caller.exceptions.client_http_exception import ClientHttpException
from baobab_web_api_caller.exceptions.rate_limit_exception import RateLimitException
from baobab_web_api_caller.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from baobab_web_api_caller.exceptions.server_http_exception import ServerHttpException


@dataclass(frozen=True, slots=True)
class ErrorResponseMapper:
    """Transforme une réponse en exception projet lorsque nécessaire."""

    def raise_for_error(self, response: BaobabResponse) -> None:
        """Lève une exception projet si le status code indique une erreur."""

        status = response.status_code
        if status < 400:
            return

        message = f"HTTP {status}"
        if status == 401:
            raise AuthenticationException(message)
        if status == 404:
            raise ResourceNotFoundException(message)
        if status == 429:
            raise RateLimitException(message)
        if 400 <= status <= 499:
            raise ClientHttpException(message)
        raise ServerHttpException(message)
