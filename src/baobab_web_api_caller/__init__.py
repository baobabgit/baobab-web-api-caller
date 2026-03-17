"""Package racine de `baobab-web-api-caller`.

Ce package fournit une librairie orientée objet pour simplifier les appels HTTP(S) vers des
API REST.
"""

from __future__ import annotations

from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.download.bulk_file_downloader import BulkFileDownloader
from baobab_web_api_caller.pagination.paginator import Paginator
from baobab_web_api_caller.service.baobab_service_caller import BaobabServiceCaller
from baobab_web_api_caller.transport.http_transport_caller import HttpTransportCaller
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory

__all__ = [
    "__version__",
    "BaobabRequest",
    "BaobabResponse",
    "BaobabServiceCaller",
    "BulkFileDownloader",
    "HttpMethod",
    "HttpTransportCaller",
    "Paginator",
    "RequestsSessionFactory",
    "ServiceConfig",
]

__version__ = "0.1.0"
