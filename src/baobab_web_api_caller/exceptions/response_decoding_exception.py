"""Exceptions liées au décodage de réponse."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)


class ResponseDecodingException(BaobabWebApiCallerException):
    """Erreur lors du décodage d'une réponse (ex: JSON invalide, encodage inattendu)."""
