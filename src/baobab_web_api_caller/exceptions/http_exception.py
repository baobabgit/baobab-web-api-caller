"""Exceptions liées aux réponses HTTP en erreur."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)


class HttpException(BaobabWebApiCallerException):
    """Erreur HTTP (4xx/5xx) renvoyée par le serveur distant."""
