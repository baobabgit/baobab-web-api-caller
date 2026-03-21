"""Package racine de `baobab-web-api-caller`.

Ce package fournit une librairie orientée objet pour simplifier les appels HTTP(S) vers des
API REST.

**Contrat public stable (Semantic Versioning à partir de la 1.0.0)** : les noms listés dans
:data:`__all__` constituent la surface d’API garantie pour une compatibilité **mineure** (ajouts
rétrocompatibles) dans les versions ``1.x.y``. Toute **rupture** intentionnelle de ces symboles
nécessitera une version **majeure** (``2.0.0``).

Les sous-modules internes (``transport``, ``core``, etc.) restent accessibles pour des usages
avancés, mais seuls les symboles exportés ici sont considérés comme **stables** pour le support
de compatibilité.

Voir aussi : ``docs/public_api_1_0_0.md``.
"""

from __future__ import annotations

from baobab_web_api_caller.auth import (
    ApiKeyHeaderAuthenticationStrategy,
    ApiKeyQueryAuthenticationStrategy,
    AuthenticationStrategy,
    BasicAuthenticationStrategy,
    BearerAuthenticationStrategy,
    NoAuthenticationStrategy,
)
from baobab_web_api_caller.config.rate_limit_policy import RateLimitPolicy
from baobab_web_api_caller.config.retry_policy import RetryPolicy
from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.baobab_web_api_caller import BaobabWebApiCaller
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.download.bulk_file_downloader import BulkFileDownloader
from baobab_web_api_caller.exceptions import (
    AuthenticationException,
    BaobabWebApiCallerException,
    ClientHttpException,
    ConfigurationException,
    HttpException,
    RateLimitException,
    ResourceNotFoundException,
    ResponseDecodingException,
    ServerHttpException,
    ServiceCallException,
    TimeoutException,
    TransportException,
)
from baobab_web_api_caller.pagination.next_page_url_extractor import NextPageUrlExtractor
from baobab_web_api_caller.pagination.page_extractor import PageExtractor
from baobab_web_api_caller.pagination.page_result import PageResult
from baobab_web_api_caller.pagination.paginator import Paginator
from baobab_web_api_caller.service.baobab_service_caller import BaobabServiceCaller
from baobab_web_api_caller.transport.http_transport_caller import HttpTransportCaller
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory

__version__ = "1.0.0"

# Surface publique figée pour la compatibilité semver (1.x) — ordre alphabétique.
__all__ = [
    "ApiKeyHeaderAuthenticationStrategy",
    "ApiKeyQueryAuthenticationStrategy",
    "AuthenticationException",
    "AuthenticationStrategy",
    "BaobabRequest",
    "BaobabResponse",
    "BaobabServiceCaller",
    "BaobabWebApiCaller",
    "BaobabWebApiCallerException",
    "BasicAuthenticationStrategy",
    "BearerAuthenticationStrategy",
    "BulkFileDownloader",
    "ClientHttpException",
    "ConfigurationException",
    "HttpException",
    "HttpMethod",
    "HttpTransportCaller",
    "NextPageUrlExtractor",
    "NoAuthenticationStrategy",
    "PageExtractor",
    "PageResult",
    "Paginator",
    "RateLimitException",
    "RateLimitPolicy",
    "RequestsSessionFactory",
    "ResourceNotFoundException",
    "ResponseDecodingException",
    "RetryPolicy",
    "ServerHttpException",
    "ServiceCallException",
    "ServiceConfig",
    "TimeoutException",
    "TransportException",
    "__version__",
]
