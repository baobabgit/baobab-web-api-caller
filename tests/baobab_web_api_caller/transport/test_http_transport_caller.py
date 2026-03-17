"""Tests de `HttpTransportCaller`."""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import Mock

import pytest
import requests

from baobab_web_api_caller.auth.bearer_authentication_strategy import BearerAuthenticationStrategy
from baobab_web_api_caller.config.rate_limit_policy import RateLimitPolicy
from baobab_web_api_caller.config.retry_policy import RetryPolicy
from baobab_web_api_caller.config.default_header_provider import DefaultHeaderProvider
from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.error_response_mapper import ErrorResponseMapper
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.core.request_url_builder import RequestUrlBuilder
from baobab_web_api_caller.core.response_decoder import ResponseDecoder
from baobab_web_api_caller.exceptions.rate_limit_exception import RateLimitException
from baobab_web_api_caller.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from baobab_web_api_caller.exceptions.response_decoding_exception import ResponseDecodingException
from baobab_web_api_caller.exceptions.server_http_exception import ServerHttpException
from baobab_web_api_caller.exceptions.timeout_exception import TimeoutException
from baobab_web_api_caller.exceptions.transport_exception import TransportException
from baobab_web_api_caller.transport.http_transport_caller import HttpTransportCaller
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory
from baobab_web_api_caller.transport.sleeper import Sleeper
from baobab_web_api_caller.transport.throttler import Throttler
from baobab_web_api_caller.transport.time_provider import TimeProvider


@dataclass(frozen=True, slots=True)
class FakeSessionFactory(RequestsSessionFactory):
    """Factory de session injectant un mock."""

    session: requests.Session

    def create(self) -> requests.Session:
        return self.session


@dataclass(slots=True)
class FakeTimeProvider(TimeProvider):
    """Provider de temps contrôlable."""

    now: float = 0.0

    def monotonic(self) -> float:
        return float(self.now)


@dataclass(slots=True)
class FakeSleeper(Sleeper):
    """Sleeper de test (pas d'attente réelle)."""

    time_provider: FakeTimeProvider
    sleeps: list[float]

    def sleep(self, seconds: float) -> None:
        seconds_f = float(seconds)
        self.sleeps.append(seconds_f)
        self.time_provider.now += seconds_f


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
        session.close.assert_called_once()
        response.close.assert_called_once()
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
        session.close.assert_called_once()
        response.close.assert_called_once()
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
        session.close.assert_called_once()

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
        session.close.assert_called_once()

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
        session.close.assert_called_once()
        response.close.assert_called_once()

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
        session.close.assert_called_once()
        response.close.assert_called_once()

    def test_retry_succeeds_after_timeout(self) -> None:
        """Succès après retry sur timeout."""

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        response.content = b'{"ok": true}'
        response.text = '{"ok": true}'
        response.json.return_value = {"ok": True}

        session = Mock(spec=requests.Session)
        session.request.side_effect = [requests.Timeout("boom"), response]

        time_provider = FakeTimeProvider(now=0.0)
        sleeps: list[float] = []
        sleeper = FakeSleeper(time_provider=time_provider, sleeps=sleeps)
        throttler = Throttler(
            rate_limit_policy=RateLimitPolicy(min_interval_seconds=0.0),
            time_provider=time_provider,
            sleeper=sleeper,
        )

        cfg = ServiceConfig(
            base_url="https://example.com",
            retry_policy=RetryPolicy(max_attempts=2, backoff_seconds=0.2, backoff_multiplier=1.0),
        )
        url_builder = Mock(spec=RequestUrlBuilder)
        url_builder.build.return_value = "https://example.com/x"
        default_headers = Mock(spec=DefaultHeaderProvider)
        default_headers.apply.side_effect = lambda r: r
        response_decoder = Mock(spec=ResponseDecoder)
        response_decoder.decode.side_effect = lambda r: r
        error_mapper = Mock(spec=ErrorResponseMapper)
        error_mapper.raise_for_error.side_effect = lambda r: None
        caller = HttpTransportCaller(
            service_config=cfg,
            session_factory=FakeSessionFactory(session=session),
            url_builder=url_builder,
            default_header_provider=default_headers,
            response_decoder=response_decoder,
            error_response_mapper=error_mapper,
            throttler=throttler,
        )

        req = BaobabRequest(method=HttpMethod.GET, path="/x", query_params={}, headers={})
        resp = caller.call(req)
        assert resp.status_code == 200
        assert session.request.call_count == 2
        assert sleeps == [0.2]
        session.close.assert_called_once()
        response.close.assert_called_once()

    def test_retry_succeeds_after_5xx(self) -> None:
        """Succès après retry sur 5xx."""

        response_500 = Mock(spec=requests.Response)
        response_500.status_code = 500
        response_500.headers = {}
        response_500.content = b""
        response_500.text = ""

        response_200 = Mock(spec=requests.Response)
        response_200.status_code = 200
        response_200.headers = {}
        response_200.content = b""
        response_200.text = ""

        session = Mock(spec=requests.Session)
        session.request.side_effect = [response_500, response_200]

        time_provider = FakeTimeProvider(now=0.0)
        sleeps: list[float] = []
        sleeper = FakeSleeper(time_provider=time_provider, sleeps=sleeps)
        throttler = Throttler(
            rate_limit_policy=RateLimitPolicy(min_interval_seconds=0.0),
            time_provider=time_provider,
            sleeper=sleeper,
        )

        cfg = ServiceConfig(
            base_url="https://example.com",
            retry_policy=RetryPolicy(max_attempts=2, backoff_seconds=0.1, backoff_multiplier=1.0),
        )
        url_builder = Mock(spec=RequestUrlBuilder)
        url_builder.build.return_value = "https://example.com/x"
        default_headers = Mock(spec=DefaultHeaderProvider)
        default_headers.apply.side_effect = lambda r: r
        response_decoder = Mock(spec=ResponseDecoder)
        response_decoder.decode.side_effect = lambda r: r
        error_mapper = Mock(spec=ErrorResponseMapper)
        error_mapper.raise_for_error.side_effect = lambda r: None
        caller = HttpTransportCaller(
            service_config=cfg,
            session_factory=FakeSessionFactory(session=session),
            url_builder=url_builder,
            default_header_provider=default_headers,
            response_decoder=response_decoder,
            error_response_mapper=error_mapper,
            throttler=throttler,
        )

        req = BaobabRequest(method=HttpMethod.GET, path="/x", query_params={}, headers={})
        _ = caller.call(req)
        assert session.request.call_count == 2
        assert sleeps == [0.1]
        session.close.assert_called_once()
        response_500.close.assert_called_once()
        response_200.close.assert_called_once()

    def test_retry_fails_after_max_attempts_on_5xx(self) -> None:
        """Échec final après retries sur 5xx."""

        response_503_a = Mock(spec=requests.Response)
        response_503_a.status_code = 503
        response_503_a.headers = {}
        response_503_a.content = b""
        response_503_a.text = ""

        response_503_b = Mock(spec=requests.Response)
        response_503_b.status_code = 503
        response_503_b.headers = {}
        response_503_b.content = b""
        response_503_b.text = ""

        session = Mock(spec=requests.Session)
        session.request.side_effect = [response_503_a, response_503_b]

        time_provider = FakeTimeProvider(now=0.0)
        sleeps: list[float] = []
        sleeper = FakeSleeper(time_provider=time_provider, sleeps=sleeps)
        throttler = Throttler(
            rate_limit_policy=RateLimitPolicy(min_interval_seconds=0.0),
            time_provider=time_provider,
            sleeper=sleeper,
        )

        cfg = ServiceConfig(
            base_url="https://example.com",
            retry_policy=RetryPolicy(max_attempts=2, backoff_seconds=0.1, backoff_multiplier=1.0),
        )
        url_builder = Mock(spec=RequestUrlBuilder)
        url_builder.build.return_value = "https://example.com/x"
        default_headers = Mock(spec=DefaultHeaderProvider)
        default_headers.apply.side_effect = lambda r: r
        response_decoder = Mock(spec=ResponseDecoder)
        response_decoder.decode.side_effect = lambda r: r
        error_mapper = Mock(spec=ErrorResponseMapper)
        error_mapper.raise_for_error.side_effect = ServerHttpException("boom")
        caller = HttpTransportCaller(
            service_config=cfg,
            session_factory=FakeSessionFactory(session=session),
            url_builder=url_builder,
            default_header_provider=default_headers,
            response_decoder=response_decoder,
            error_response_mapper=error_mapper,
            throttler=throttler,
        )

        req = BaobabRequest(method=HttpMethod.GET, path="/x", query_params={}, headers={})
        with pytest.raises(ServerHttpException):
            caller.call(req)
        assert session.request.call_count == 2
        assert sleeps == [0.1]
        session.close.assert_called_once()
        response_503_a.close.assert_called_once()
        response_503_b.close.assert_called_once()

    def test_429_is_retried_and_then_raises(self) -> None:
        """Retry sur 429 puis exception projet RateLimitException."""

        response_429_a = Mock(spec=requests.Response)
        response_429_a.status_code = 429
        response_429_a.headers = {}
        response_429_a.content = b""
        response_429_a.text = ""

        response_429_b = Mock(spec=requests.Response)
        response_429_b.status_code = 429
        response_429_b.headers = {}
        response_429_b.content = b""
        response_429_b.text = ""

        session = Mock(spec=requests.Session)
        session.request.side_effect = [response_429_a, response_429_b]

        time_provider = FakeTimeProvider(now=0.0)
        sleeps: list[float] = []
        sleeper = FakeSleeper(time_provider=time_provider, sleeps=sleeps)
        throttler = Throttler(
            rate_limit_policy=RateLimitPolicy(min_interval_seconds=0.0),
            time_provider=time_provider,
            sleeper=sleeper,
        )

        cfg = ServiceConfig(
            base_url="https://example.com",
            retry_policy=RetryPolicy(max_attempts=2, backoff_seconds=0.1, backoff_multiplier=1.0),
        )
        url_builder = Mock(spec=RequestUrlBuilder)
        url_builder.build.return_value = "https://example.com/x"
        default_headers = Mock(spec=DefaultHeaderProvider)
        default_headers.apply.side_effect = lambda r: r
        response_decoder = Mock(spec=ResponseDecoder)
        response_decoder.decode.side_effect = lambda r: r
        error_mapper = Mock(spec=ErrorResponseMapper)
        error_mapper.raise_for_error.side_effect = RateLimitException("boom")
        caller = HttpTransportCaller(
            service_config=cfg,
            session_factory=FakeSessionFactory(session=session),
            url_builder=url_builder,
            default_header_provider=default_headers,
            response_decoder=response_decoder,
            error_response_mapper=error_mapper,
            throttler=throttler,
        )

        req = BaobabRequest(method=HttpMethod.GET, path="/x", query_params={}, headers={})
        with pytest.raises(RateLimitException):
            caller.call(req)
        assert session.request.call_count == 2
        assert sleeps == [0.1]
        session.close.assert_called_once()
        response_429_a.close.assert_called_once()
        response_429_b.close.assert_called_once()

    def test_throttling_respects_min_interval_without_real_sleep(self) -> None:
        """Respect de l'intervalle minimal entre deux appels."""

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.headers = {}
        response.content = b""
        response.text = ""

        session = Mock(spec=requests.Session)
        session.request.return_value = response

        time_provider = FakeTimeProvider(now=0.0)
        sleeps: list[float] = []
        sleeper = FakeSleeper(time_provider=time_provider, sleeps=sleeps)
        throttler = Throttler(
            rate_limit_policy=RateLimitPolicy(min_interval_seconds=1.0),
            time_provider=time_provider,
            sleeper=sleeper,
        )

        cfg = ServiceConfig(
            base_url="https://example.com", retry_policy=RetryPolicy(max_attempts=1)
        )
        url_builder = Mock(spec=RequestUrlBuilder)
        url_builder.build.return_value = "https://example.com/x"
        default_headers = Mock(spec=DefaultHeaderProvider)
        default_headers.apply.side_effect = lambda r: r
        response_decoder = Mock(spec=ResponseDecoder)
        response_decoder.decode.side_effect = lambda r: r
        error_mapper = Mock(spec=ErrorResponseMapper)
        error_mapper.raise_for_error.side_effect = lambda r: None
        caller = HttpTransportCaller(
            service_config=cfg,
            session_factory=FakeSessionFactory(session=session),
            url_builder=url_builder,
            default_header_provider=default_headers,
            response_decoder=response_decoder,
            error_response_mapper=error_mapper,
            throttler=throttler,
        )

        req = BaobabRequest(method=HttpMethod.GET, path="/x", query_params={}, headers={})
        _ = caller.call(req)
        _ = caller.call(req)

        assert session.request.call_count == 2
        assert sleeps == [1.0]
        assert session.close.call_count == 2
        assert response.close.call_count == 2
