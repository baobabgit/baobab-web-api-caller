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
    """Contexte prêt à exécuter une requête via `requests`.

    ``prepared_request`` contient les en-têtes finaux (défauts, requête, authentification), cf.
    :func:`build_call_context`.
    """

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

    Point unique d'assemblage des en-têtes HTTP pour l'exécution : aucune fusion complémentaire
    n'est attendue en amont (par exemple dans
    :class:`~baobab_web_api_caller.service.baobab_service_caller.BaobabServiceCaller`).

    Ordre d'application (du plus faible au plus fort priorité pour une même clé d'en-tête) :

    #. ``default_header_provider`` — en-têtes issus de la configuration de service ;
    #. en-têtes portés par ``request`` — ils écrasent les valeurs par défaut pour une même clé ;
    #. ``service_config.authentication_strategy`` — appliquée en dernier (ex. ``Authorization``,
       clé API) et peut donc remplacer une valeur fournie dans la requête pour cette clé.

    Résout ensuite le timeout effectif et construit l'URL finale.

    :param request: Requête telle que fournie par l'appelant (en-têtes utilisateur non fusionnés
        avec les défauts).
    :type request: BaobabRequest
    :param service_config: Configuration du service distant (auth, timeout par défaut).
    :type service_config: ServiceConfig
    :param default_header_provider: Fournisseur des en-têtes par défaut du service.
    :type default_header_provider: DefaultHeaderProvider
    :param url_builder: Constructeur d'URL absolue.
    :type url_builder: RequestUrlBuilder
    :param session_factory: Factory de :class:`requests.Session`.
    :type session_factory: RequestsSessionFactory
    :return: Contexte prêt pour l'appel HTTP.
    :rtype: CallContext
    """

    prepared = default_header_provider.apply(request)
    prepared = service_config.authentication_strategy.apply(prepared)

    timeout = prepared.timeout_seconds
    if timeout is None:
        timeout = service_config.default_timeout_seconds

    url = url_builder.build(prepared)
    session = session_factory.create()
    return CallContext(prepared_request=prepared, url=url, timeout=timeout, session=session)
