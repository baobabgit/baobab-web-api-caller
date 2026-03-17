"""Composants centraux (core) de la librairie.

Cette couche contient les modèles typés de requête/réponse et des abstractions de base, sans
dépendre du transport HTTP réel.
"""

from __future__ import annotations

from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.http_method import HttpMethod

__all__ = [
    "BaobabRequest",
    "BaobabResponse",
    "HttpMethod",
]
