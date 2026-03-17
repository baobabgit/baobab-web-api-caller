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
        """Lève une exception projet si le status code indique une erreur.

        Le message et les attributs de l'exception exposent un sous-ensemble des informations
        de la réponse (status, extrait de body texte, quelques en-têtes utiles) pour faciliter
        le diagnostic tout en évitant de logguer des payloads trop volumineux.
        """

        status = response.status_code
        if status < 400:
            return

        body_excerpt = self._extract_body_excerpt(response.text)
        headers_subset = self._extract_diagnostic_headers(response.headers)
        message = f"HTTP {status}"

        if status == 401:
            raise AuthenticationException(
                status_code=status,
                message=message,
                body_excerpt=body_excerpt,
                headers=headers_subset,
            )
        if status == 404:
            raise ResourceNotFoundException(
                status_code=status,
                message=message,
                body_excerpt=body_excerpt,
                headers=headers_subset,
            )
        if status == 429:
            raise RateLimitException(
                status_code=status,
                message=message,
                body_excerpt=body_excerpt,
                headers=headers_subset,
            )
        if 400 <= status <= 499:
            raise ClientHttpException(
                status_code=status,
                message=message,
                body_excerpt=body_excerpt,
                headers=headers_subset,
            )
        raise ServerHttpException(
            status_code=status,
            message=message,
            body_excerpt=body_excerpt,
            headers=headers_subset,
        )

    @staticmethod
    def _extract_body_excerpt(text: str | None, *, max_length: int = 256) -> str | None:
        if text is None:
            return None

        stripped = text.strip()
        if not stripped:
            return None
        if len(stripped) <= max_length:
            return stripped
        return f"{stripped[:max_length]}…"

    @staticmethod
    def _extract_diagnostic_headers(headers: dict[str, str]) -> dict[str, str] | None:
        interesting_keys = {
            "content-type",
            "x-request-id",
            "x-correlation-id",
            "retry-after",
        }

        subset: dict[str, str] = {}
        for key, value in headers.items():
            lowered = key.lower()
            if lowered in interesting_keys:
                subset[key] = value

        return subset or None
