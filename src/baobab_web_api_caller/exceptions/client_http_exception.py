"""Exceptions HTTP côté client."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.http_exception import HttpException


class ClientHttpException(HttpException):
    """Erreur HTTP client (4xx)."""
