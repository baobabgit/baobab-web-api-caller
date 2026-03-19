"""Mapping des erreurs de réponse vers des exceptions projet."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

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

    _STATUS_REASONS: ClassVar[dict[int, str]] = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        429: "Too Many Requests",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
    }

    def raise_for_error(self, response: BaobabResponse) -> None:
        """Lève une exception projet si le status code indique une erreur.

        Le message et les attributs de l'exception exposent un sous-ensemble des informations
        de la réponse (status, extrait de body texte, quelques en-têtes utiles) pour faciliter
        le diagnostic tout en évitant de logguer des payloads trop volumineux.

        Le champ `message` est de la forme `HTTP {status_code} {raison}` lorsqu'une raison
        standard est connue, et sinon `HTTP {status_code} Client Error` / `Server Error`.
        """

        status = response.status_code
        if status < 400:
            return

        body_excerpt = self._extract_body_excerpt(response.text)
        headers_subset = self._extract_diagnostic_headers(response.headers)
        message = self._build_error_message(status)

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

    @classmethod
    def _build_error_message(cls, status_code: int) -> str:
        reason = cls._STATUS_REASONS.get(status_code)
        if reason is not None:
            return f"HTTP {status_code} {reason}"
        if 400 <= status_code <= 499:
            return f"HTTP {status_code} Client Error"
        return f"HTTP {status_code} Server Error"

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
            "www-authenticate",
        }

        subset: dict[str, str] = {}
        for key, value in headers.items():
            lowered = key.lower()
            if lowered in interesting_keys:
                subset[key] = value

        return subset or None
