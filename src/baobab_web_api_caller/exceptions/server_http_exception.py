"""Exceptions HTTP côté serveur."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.http_exception import HttpException


class ServerHttpException(HttpException):
    """Erreur HTTP serveur (5xx)."""
