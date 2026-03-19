"""Transport HTTP synchrone basé sur `requests`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

import requests

from baobab_web_api_caller.config.default_header_provider import DefaultHeaderProvider
from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.baobab_web_api_caller import BaobabWebApiCaller
from baobab_web_api_caller.core.error_response_mapper import ErrorResponseMapper
from baobab_web_api_caller.core.json_response_decoder import JsonResponseDecoder
from baobab_web_api_caller.core.request_url_builder import RequestUrlBuilder
from baobab_web_api_caller.core.response_decoder import ResponseDecoder
from baobab_web_api_caller.exceptions.rate_limit_exception import RateLimitException
from baobab_web_api_caller.exceptions.server_http_exception import ServerHttpException
from baobab_web_api_caller.exceptions.timeout_exception import TimeoutException
from baobab_web_api_caller.exceptions.transport_exception import TransportException
from baobab_web_api_caller.transport.call_context_builder import build_call_context
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory
from baobab_web_api_caller.transport.system_sleeper import SystemSleeper
from baobab_web_api_caller.transport.system_time_provider import SystemTimeProvider
from baobab_web_api_caller.transport.throttler import Throttler


@dataclass(frozen=True, slots=True)
class HttpTransportCaller(BaobabWebApiCaller):
    """Implémentation concrète du transport HTTP synchrone.

    L'authentification est appliquée via la stratégie configurée, par composition.
    Le mapping des erreurs HTTP (4xx/5xx) est délégué à `ErrorResponseMapper`, afin d'exposer un
    contexte utile (code, extrait de body et certains headers) via la hiérarchie d'exceptions
    du projet.
    Cette classe se concentre ensuite sur la normalisation de la réponse (`BaobabResponse`) et
    l'encapsulation des erreurs réseau (timeouts / erreurs requests) via exceptions du projet.
    """

    service_config: ServiceConfig
    session_factory: RequestsSessionFactory
    url_builder: RequestUrlBuilder
    default_header_provider: DefaultHeaderProvider
    response_decoder: ResponseDecoder
    error_response_mapper: ErrorResponseMapper
    throttler: Throttler

    @classmethod
    def from_service_config(
        cls, service_config: ServiceConfig, session_factory: RequestsSessionFactory
    ) -> "HttpTransportCaller":
        """Construit un transport à partir d'une configuration de service."""

        throttler: Final[Throttler] = Throttler(
            rate_limit_policy=service_config.rate_limit_policy,
            time_provider=SystemTimeProvider(),
            sleeper=SystemSleeper(),
        )
        return cls(
            service_config=service_config,
            session_factory=session_factory,
            url_builder=RequestUrlBuilder(base_url=service_config.base_url),
            default_header_provider=DefaultHeaderProvider(
                default_headers=service_config.default_headers
            ),
            response_decoder=JsonResponseDecoder(),
            error_response_mapper=ErrorResponseMapper(),
            throttler=throttler,
        )

    def call(self, request: BaobabRequest) -> BaobabResponse:
        """Exécute une requête HTTP synchrone via `requests`.

        Comportement principal :
        - applique le throttling avant chaque tentative ;
        - applique la politique de retry sur erreurs réseau (`requests`) et statuts retryables
          (`429`, `5xx`) ;
        - mappe les erreurs HTTP finales via `ErrorResponseMapper` ;
        - ferme systématiquement la `requests.Session` en fin d'appel ;
        - ferme chaque `requests.Response` après normalisation/décodage.
        """

        ctx = build_call_context(
            request=request,
            service_config=self.service_config,
            default_header_provider=self.default_header_provider,
            url_builder=self.url_builder,
            session_factory=self.session_factory,
        )

        try:
            retry_policy = self.service_config.retry_policy
            last_error: Exception | None = None
            for attempt in range(1, retry_policy.max_attempts + 1):
                self.throttler.throttle()
                result = self._try_call_once(ctx.session, ctx.prepared_request, ctx.url, ctx.timeout)

                if isinstance(result, BaobabResponse):
                    if self._is_retryable_status_code(result.status_code):
                        last_error = self._exception_for_retryable_status(result.status_code)
                        if attempt >= retry_policy.max_attempts:
                            self.error_response_mapper.raise_for_error(result)
                    else:
                        self.error_response_mapper.raise_for_error(result)
                        return result
                else:
                    last_error = result
                    if attempt >= retry_policy.max_attempts:
                        raise result

                delay = self._compute_backoff_seconds(
                    attempt, retry_policy.backoff_seconds, retry_policy.backoff_multiplier
                )
                if delay > 0:
                    self.throttler.sleeper.sleep(delay)

            if last_error is None:
                raise TransportException("retry exhausted without error")
            raise last_error
        finally:
            ctx.session.close()

    @staticmethod
    def _compute_backoff_seconds(attempt: int, base: float, multiplier: float) -> float:
        if attempt <= 0:
            return 0.0
        return float(base) * pow(float(multiplier), attempt - 1)

    @staticmethod
    def _is_retryable_status_code(status_code: int) -> bool:
        return status_code == 429 or 500 <= status_code <= 599

    @staticmethod
    def _exception_for_retryable_status(status_code: int) -> Exception:
        if status_code == 429:
            return RateLimitException(
                status_code=status_code,
                message="HTTP 429 Too Many Requests",
            )
        return ServerHttpException(
            status_code=status_code,
            message=f"HTTP {status_code} Server Error",
        )

    def _try_call_once(
        self,
        session: requests.Session,
        prepared: BaobabRequest,
        url: str,
        timeout: float | None,
    ) -> BaobabResponse | Exception:
        response: requests.Response | None = None
        try:
            response = session.request(
                method=prepared.method.value,
                url=url,
                params=None,
                headers=dict(prepared.headers),
                json=prepared.json_body,
                data=dict(prepared.form_body) if prepared.form_body is not None else None,
                timeout=timeout,
            )
        except requests.Timeout as exc:
            return TimeoutException(str(exc))
        except requests.RequestException as exc:
            return TransportException(str(exc))

        try:
            raw = self._to_baobab_response(response)
            return self.response_decoder.decode(raw)
        finally:
            if response is not None:
                response.close()

    @staticmethod
    def _to_baobab_response(response: requests.Response) -> BaobabResponse:
        headers: dict[str, str] = {str(k): str(v) for k, v in response.headers.items()}

        return BaobabResponse(
            status_code=response.status_code,
            headers=headers,
            text=response.text,
            content=response.content,
            json_data=None,
        )
