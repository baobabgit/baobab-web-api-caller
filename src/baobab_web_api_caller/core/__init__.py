"""Composants centraux (core) de la librairie.

Cette couche contient les modèles typés de requête/réponse et des abstractions de base, sans
dépendre du transport HTTP réel.
"""

from __future__ import annotations

from baobab_web_api_caller.core.baobab_web_api_caller import BaobabWebApiCaller
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.error_response_mapper import ErrorResponseMapper
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.core.json_response_decoder import JsonResponseDecoder
from baobab_web_api_caller.core.request_url_builder import RequestUrlBuilder
from baobab_web_api_caller.core.response_decoder import ResponseDecoder

__all__ = [
    "BaobabWebApiCaller",
    "BaobabRequest",
    "BaobabResponse",
    "ErrorResponseMapper",
    "HttpMethod",
    "JsonResponseDecoder",
    "RequestUrlBuilder",
    "ResponseDecoder",
]
