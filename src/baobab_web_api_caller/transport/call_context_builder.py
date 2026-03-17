"""Construction d'un contexte d'appel HTTP (réutilisable, testable)."""

from __future__ import annotations

from dataclasses import dataclass

import requests

from baobab_web_api_caller.config.default_header_provider import DefaultHeaderProvider
from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.request_url_builder import RequestUrlBuilder
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory


@dataclass(frozen=True, slots=True)
class CallContext:
    """Contexte prêt à exécuter une requête via `requests`."""

    prepared_request: BaobabRequest
    url: str
    timeout: float | None
    session: requests.Session


def build_call_context(
    *,
    request: BaobabRequest,
    service_config: ServiceConfig,
    default_header_provider: DefaultHeaderProvider,
    url_builder: RequestUrlBuilder,
    session_factory: RequestsSessionFactory,
) -> CallContext:
    """Prépare une requête et instancie une session.

    Applique headers par défaut + stratégie d'authentification, résout le timeout effectif,
    puis construit l'URL finale.
    """

    prepared = default_header_provider.apply(request)
    prepared = service_config.authentication_strategy.apply(prepared)

    timeout = prepared.timeout_seconds
    if timeout is None:
        timeout = service_config.default_timeout_seconds

    url = url_builder.build(prepared)
    session = session_factory.create()
    return CallContext(prepared_request=prepared, url=url, timeout=timeout, session=session)
