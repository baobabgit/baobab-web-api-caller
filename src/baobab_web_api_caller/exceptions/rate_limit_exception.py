"""Exception de limitation de débit."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.client_http_exception import ClientHttpException


class RateLimitException(ClientHttpException):
    """Limitation de débit (HTTP 429)."""
