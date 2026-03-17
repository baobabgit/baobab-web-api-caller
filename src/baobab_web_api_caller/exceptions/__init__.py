"""Exceptions spécifiques au projet.

Toutes les exceptions exposées par la librairie dérivent de :class:`BaobabWebApiCallerException`.
"""

from __future__ import annotations

from baobab_web_api_caller.exceptions.authentication_exception import AuthenticationException
from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)
from baobab_web_api_caller.exceptions.client_http_exception import ClientHttpException
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException
from baobab_web_api_caller.exceptions.http_exception import HttpException
from baobab_web_api_caller.exceptions.rate_limit_exception import RateLimitException
from baobab_web_api_caller.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from baobab_web_api_caller.exceptions.response_decoding_exception import ResponseDecodingException
from baobab_web_api_caller.exceptions.server_http_exception import ServerHttpException
from baobab_web_api_caller.exceptions.service_call_exception import ServiceCallException
from baobab_web_api_caller.exceptions.timeout_exception import TimeoutException
from baobab_web_api_caller.exceptions.transport_exception import TransportException

__all__ = [
    "AuthenticationException",
    "BaobabWebApiCallerException",
    "ClientHttpException",
    "ConfigurationException",
    "HttpException",
    "RateLimitException",
    "ResourceNotFoundException",
    "ResponseDecodingException",
    "ServerHttpException",
    "ServiceCallException",
    "TimeoutException",
    "TransportException",
]
