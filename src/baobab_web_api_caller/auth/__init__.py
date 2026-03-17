"""Stratégies d'authentification composables.

Cette couche applique des informations d'authentification à une
:class:`~baobab_web_api_caller.core.baobab_request.BaobabRequest` sans dépendre d'un transport
HTTP concret.
"""

from __future__ import annotations

from baobab_web_api_caller.auth.api_key_header_authentication_strategy import (
    ApiKeyHeaderAuthenticationStrategy,
)
from baobab_web_api_caller.auth.api_key_query_authentication_strategy import (
    ApiKeyQueryAuthenticationStrategy,
)
from baobab_web_api_caller.auth.authentication_strategy import AuthenticationStrategy
from baobab_web_api_caller.auth.basic_authentication_strategy import BasicAuthenticationStrategy
from baobab_web_api_caller.auth.bearer_authentication_strategy import BearerAuthenticationStrategy
from baobab_web_api_caller.auth.no_authentication_strategy import NoAuthenticationStrategy

__all__ = [
    "ApiKeyHeaderAuthenticationStrategy",
    "ApiKeyQueryAuthenticationStrategy",
    "AuthenticationStrategy",
    "BasicAuthenticationStrategy",
    "BearerAuthenticationStrategy",
    "NoAuthenticationStrategy",
]
