"""Usines et constantes pour les tests d'intégration externes."""

from __future__ import annotations

from baobab_web_api_caller.auth.authentication_strategy import AuthenticationStrategy
from baobab_web_api_caller.auth.no_authentication_strategy import NoAuthenticationStrategy
from baobab_web_api_caller.config.retry_policy import RetryPolicy
from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.service.baobab_service_caller import BaobabServiceCaller
from baobab_web_api_caller.transport.http_transport_caller import HttpTransportCaller
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory

# URLs publiques documentées (services de test uniquement).
HTTPBIN_BASE_URL: str = "https://httpbin.org"
POSTMAN_ECHO_BASE_URL: str = "https://postman-echo.com"

# Timeouts par défaut : suffisant pour le réseau public, sans rallonger inutilement.
DEFAULT_INTEGRATION_TIMEOUT_SECONDS: float = 25.0


def make_release_gate_service_config(
    base_url: str,
    *,
    authentication_strategy: AuthenticationStrategy | None = None,
    default_timeout_seconds: float | None = DEFAULT_INTEGRATION_TIMEOUT_SECONDS,
) -> ServiceConfig:
    """Configuration minimale pour les appels réseau (un seul essai, pas de backoff)."""

    strategy = authentication_strategy or NoAuthenticationStrategy()
    return ServiceConfig(
        base_url=base_url,
        authentication_strategy=strategy,
        retry_policy=RetryPolicy(max_attempts=1, backoff_seconds=0.0, backoff_multiplier=1.0),
        default_timeout_seconds=default_timeout_seconds,
    )


def make_release_gate_service_caller(
    base_url: str,
    *,
    authentication_strategy: AuthenticationStrategy | None = None,
    default_timeout_seconds: float | None = DEFAULT_INTEGRATION_TIMEOUT_SECONDS,
) -> BaobabServiceCaller:
    """Construit une façade + transport HTTP réel pour les scénarios release gate.

    Une seule tentative HTTP évite les attentes longues en cas d'erreur transitoire.
    """

    cfg = make_release_gate_service_config(
        base_url,
        authentication_strategy=authentication_strategy,
        default_timeout_seconds=default_timeout_seconds,
    )
    transport = HttpTransportCaller.from_service_config(cfg, RequestsSessionFactory())
    return BaobabServiceCaller(service_config=cfg, web_api_caller=transport)
