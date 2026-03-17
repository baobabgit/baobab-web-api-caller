"""Configuration et politiques transverses.

Ce package regroupe la configuration commune aux services distants (base URL, headers, stratégie
d'authentification, timeout) et des politiques de résilience (retry, throttling) sans dépendre du
transport HTTP.
"""

from __future__ import annotations

from baobab_web_api_caller.config.default_header_provider import DefaultHeaderProvider
from baobab_web_api_caller.config.rate_limit_policy import RateLimitPolicy
from baobab_web_api_caller.config.retry_policy import RetryPolicy
from baobab_web_api_caller.config.service_config import ServiceConfig

__all__ = [
    "DefaultHeaderProvider",
    "RateLimitPolicy",
    "RetryPolicy",
    "ServiceConfig",
]
