"""Tests de `HttpTransportCaller`."""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import Mock

import pytest
import requests

from baobab_web_api_caller.auth.bearer_authentication_strategy import BearerAuthenticationStrategy
from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from baobab_web_api_caller.exceptions.response_decoding_exception import ResponseDecodingException
from baobab_web_api_caller.exceptions.timeout_exception import TimeoutException
from baobab_web_api_caller.exceptions.transport_exception import TransportException
from baobab_web_api_caller.transport.http_transport_caller import HttpTransportCaller
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory


@dataclass(frozen=True, slots=True)
class FakeSessionFactory(RequestsSessionFactory):
    """Factory de session injectant un mock."""

    session: requests.Session

    def create(self) -> requests.Session:
        return self.session


class TestHttpTransportCaller:
    """Tests unitaires pour `HttpTransportCaller`."""

    def test_call_builds_url_and_applies_default_headers_and_auth(self) -> None:
        """Vérifie l'assemblage de la requête exécutable."""

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        response.content = b'{"ok": true}'
        response.text = '{"ok": true}'
        response.json.return_value = {"ok": True}

        session = Mock(spec=requests.Session)
        session.request.return_value = response

        cfg = ServiceConfig(
            base_url="https://example.com",
            default_headers={"Accept": "application/json"},
            authentication_strategy=BearerAuthenticationStrategy(token="t"),
            default_timeout_seconds=1.0,
        )
        caller = HttpTransportCaller.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={"q": "x"},
            headers={"X-Req": "1"},
        )
        resp = caller.call(req)

        session.request.assert_called_once()
        kwargs = session.request.call_args.kwargs
        assert kwargs["method"] == "GET"
        assert kwargs["url"].startswith("https://example.com/v1/items?")
        assert "q=x" in kwargs["url"]
        assert kwargs["timeout"] == 1.0
        assert kwargs["headers"]["Accept"] == "application/json"
        assert kwargs["headers"]["X-Req"] == "1"
        assert kwargs["headers"]["Authorization"] == "Bearer t"
        assert resp.status_code == 200
        assert resp.json_data == {"ok": True}

    def test_request_timeout_overrides_default_timeout(self) -> None:
        """Le timeout de la requête doit primer."""

        response = Mock(spec=requests.Response)
        response.status_code = 204
        response.headers = {}
        response.content = b""
        response.text = ""
        response.json.side_effect = ValueError("no json")

        session = Mock(spec=requests.Session)
        session.request.return_value = response

        cfg = ServiceConfig(base_url="https://example.com", default_timeout_seconds=10.0)
        caller = HttpTransportCaller.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={},
            headers={},
            timeout_seconds=0.5,
        )
        _ = caller.call(req)
        assert session.request.call_args.kwargs["timeout"] == 0.5

    def test_timeout_exception_is_wrapped(self) -> None:
        """Wrappe requests.Timeout en TimeoutException."""

        session = Mock(spec=requests.Session)
        session.request.side_effect = requests.Timeout("boom")

        cfg = ServiceConfig(base_url="https://example.com")
        caller = HttpTransportCaller.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )
        req = BaobabRequest(method=HttpMethod.GET, path="/x", query_params={}, headers={})

        with pytest.raises(TimeoutException):
            caller.call(req)

    def test_request_exception_is_wrapped(self) -> None:
        """Wrappe requests.RequestException en TransportException."""

        session = Mock(spec=requests.Session)
        session.request.side_effect = requests.RequestException("boom")

        cfg = ServiceConfig(base_url="https://example.com")
        caller = HttpTransportCaller.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )
        req = BaobabRequest(method=HttpMethod.GET, path="/x", query_params={}, headers={})

        with pytest.raises(TransportException):
            caller.call(req)

    def test_http_404_is_mapped(self) -> None:
        """404 -> ResourceNotFoundException."""

        response = Mock(spec=requests.Response)
        response.status_code = 404
        response.headers = {"Content-Type": "application/json"}
        response.content = b'{"error": "not found"}'
        response.text = '{"error": "not found"}'

        session = Mock(spec=requests.Session)
        session.request.return_value = response

        cfg = ServiceConfig(base_url="https://example.com")
        caller = HttpTransportCaller.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )
        req = BaobabRequest(method=HttpMethod.GET, path="/x", query_params={}, headers={})

        with pytest.raises(ResourceNotFoundException):
            caller.call(req)

    def test_invalid_json_is_mapped_to_decoding_exception(self) -> None:
        """JSON invalide -> ResponseDecodingException."""

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        response.content = b"{not json"
        response.text = "{not json"

        session = Mock(spec=requests.Session)
        session.request.return_value = response

        cfg = ServiceConfig(base_url="https://example.com")
        caller = HttpTransportCaller.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )
        req = BaobabRequest(method=HttpMethod.GET, path="/x", query_params={}, headers={})

        with pytest.raises(ResponseDecodingException):
            caller.call(req)
