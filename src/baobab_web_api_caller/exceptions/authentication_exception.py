"""Exceptions liées à l'authentification."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)


class AuthenticationException(BaobabWebApiCallerException):
    """Erreur d'authentification (ex: credentials invalides, token expiré)."""
