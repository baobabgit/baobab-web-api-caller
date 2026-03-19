"""Tests de la fonction `build_call_context`."""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import Mock

import requests

from baobab_web_api_caller.auth.bearer_authentication_strategy import BearerAuthenticationStrategy
from baobab_web_api_caller.auth.no_authentication_strategy import NoAuthenticationStrategy
from baobab_web_api_caller.config.default_header_provider import DefaultHeaderProvider
from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.transport.call_context_builder import build_call_context
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory
from baobab_web_api_caller.core.request_url_builder import RequestUrlBuilder


@dataclass(frozen=True, slots=True)
class FakeSessionFactory(RequestsSessionFactory):
    """Factory de session injectant un mock."""

    session: requests.Session

    def create(self) -> requests.Session:
        """Retourne la session injectée."""

        return self.session


class TestBuildCallContext:
    """Tests unitaires pour `build_call_context`."""

    def test_build_call_context_merges_headers_and_resolves_timeout(self) -> None:
        """Vérifie la fusion des headers et la résolution du timeout."""

        session = Mock(spec=requests.Session)
        session_factory = FakeSessionFactory(session=session)

        service_config = ServiceConfig(
            base_url="https://example.com",
            default_headers={},
            authentication_strategy=NoAuthenticationStrategy(),
            default_timeout_seconds=1.0,
        )
        default_header_provider = DefaultHeaderProvider(
            default_headers={"Accept": "application/json"}
        )
        url_builder = RequestUrlBuilder(base_url=service_config.base_url)

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={"q": "x"},
            headers={"X-Test": "1"},
            timeout_seconds=0.5,
        )

        ctx = build_call_context(
            request=req,
            service_config=service_config,
            default_header_provider=default_header_provider,
            url_builder=url_builder,
            session_factory=session_factory,
        )

        assert dict(ctx.prepared_request.headers) == {
            "Accept": "application/json",
            "X-Test": "1",
        }
        assert ctx.timeout == 0.5
        assert ctx.url == url_builder.build(ctx.prepared_request)
        assert ctx.session is session

    def test_request_headers_override_default_headers_for_same_key(self) -> None:
        """Les en-têtes de la requête écrasent les valeurs par défaut pour une même clé."""

        session = Mock(spec=requests.Session)
        session_factory = FakeSessionFactory(session=session)

        service_config = ServiceConfig(
            base_url="https://example.com",
            default_headers={},
            authentication_strategy=NoAuthenticationStrategy(),
            default_timeout_seconds=1.0,
        )
        default_header_provider = DefaultHeaderProvider(
            default_headers={"Accept": "text/plain", "X-Shared": "from-default"}
        )
        url_builder = RequestUrlBuilder(base_url=service_config.base_url)

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/r",
            query_params={},
            headers={"Accept": "application/json", "X-Shared": "from-request"},
        )

        ctx = build_call_context(
            request=req,
            service_config=service_config,
            default_header_provider=default_header_provider,
            url_builder=url_builder,
            session_factory=session_factory,
        )

        assert dict(ctx.prepared_request.headers) == {
            "Accept": "application/json",
            "X-Shared": "from-request",
        }

    def test_authentication_strategy_overrides_request_headers_for_same_key(self) -> None:
        """L'authentification est appliquée en dernier et peut écraser la requête."""

        session = Mock(spec=requests.Session)
        session_factory = FakeSessionFactory(session=session)

        service_config = ServiceConfig(
            base_url="https://example.com",
            default_headers={"X-Default": "1"},
            authentication_strategy=BearerAuthenticationStrategy(token="svc-token"),
            default_timeout_seconds=1.0,
        )
        default_header_provider = DefaultHeaderProvider(
            default_headers=service_config.default_headers
        )
        url_builder = RequestUrlBuilder(base_url=service_config.base_url)

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/r",
            query_params={},
            headers={"Authorization": "Bearer user-override", "X-Req": "2"},
        )

        ctx = build_call_context(
            request=req,
            service_config=service_config,
            default_header_provider=default_header_provider,
            url_builder=url_builder,
            session_factory=session_factory,
        )

        assert dict(ctx.prepared_request.headers) == {
            "X-Default": "1",
            "X-Req": "2",
            "Authorization": "Bearer svc-token",
        }
