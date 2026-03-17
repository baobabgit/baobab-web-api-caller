"""Transport HTTP synchrone basé sur `requests`."""

from __future__ import annotations

from dataclasses import dataclass

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
from baobab_web_api_caller.exceptions.timeout_exception import TimeoutException
from baobab_web_api_caller.exceptions.transport_exception import TransportException
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory


@dataclass(frozen=True, slots=True)
class HttpTransportCaller(BaobabWebApiCaller):
    """Implémentation concrète du transport HTTP synchrone.

    L'authentification est appliquée via la stratégie configurée, par composition.
    Cette classe n'implémente pas le mapping d'erreurs avancé (HTTP métier), uniquement une
    normalisation de la réponse et l'encapsulation des erreurs réseau en exceptions du projet.
    """

    service_config: ServiceConfig
    session_factory: RequestsSessionFactory
    url_builder: RequestUrlBuilder
    default_header_provider: DefaultHeaderProvider
    response_decoder: ResponseDecoder
    error_response_mapper: ErrorResponseMapper

    @classmethod
    def from_service_config(
        cls, service_config: ServiceConfig, session_factory: RequestsSessionFactory
    ) -> "HttpTransportCaller":
        """Construit un transport à partir d'une configuration de service."""

        return cls(
            service_config=service_config,
            session_factory=session_factory,
            url_builder=RequestUrlBuilder(base_url=service_config.base_url),
            default_header_provider=DefaultHeaderProvider(
                default_headers=service_config.default_headers
            ),
            response_decoder=JsonResponseDecoder(),
            error_response_mapper=ErrorResponseMapper(),
        )

    def call(self, request: BaobabRequest) -> BaobabResponse:
        """Exécute une requête via `requests`."""

        prepared = self.default_header_provider.apply(request)
        prepared = self.service_config.authentication_strategy.apply(prepared)

        timeout = prepared.timeout_seconds
        if timeout is None:
            timeout = self.service_config.default_timeout_seconds

        url = self.url_builder.build(prepared)
        session = self.session_factory.create()

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
        except requests.Timeout as exc:  # pragma: no cover
            raise TimeoutException(str(exc)) from exc
        except requests.RequestException as exc:  # pragma: no cover
            raise TransportException(str(exc)) from exc

        raw = self._to_baobab_response(response)
        decoded = self.response_decoder.decode(raw)
        self.error_response_mapper.raise_for_error(decoded)
        return decoded

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
