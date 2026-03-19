"""Façade de service : construction et exécution de requêtes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.baobab_web_api_caller import BaobabWebApiCaller
from baobab_web_api_caller.core.http_method import HttpMethod


@dataclass(frozen=True, slots=True)
class BaobabServiceCaller:
    """Façade de haut niveau pour appeler un service REST.

    Cette classe construit des :class:`~baobab_web_api_caller.core.baobab_request.BaobabRequest`
    à partir d'une :class:`~baobab_web_api_caller.config.service_config.ServiceConfig` et délègue
    l'exécution à un :class:`~baobab_web_api_caller.core.baobab_web_api_caller.BaobabWebApiCaller`.
    """

    service_config: ServiceConfig
    web_api_caller: BaobabWebApiCaller

    def call(self, request: BaobabRequest) -> BaobabResponse:
        """Exécute une requête, en appliquant la configuration de service.

        Cette méthode délègue l'exécution au caller bas niveau.

        La fusion finale des headers par défaut (issus de `ServiceConfig.default_headers`) avec
        les headers de la requête, ainsi que l'application d'éventuels mécanismes d'authentification,
        sont traitées côté transport (`build_call_context`).

        :param request: Requête à exécuter.
        :type request: BaobabRequest
        :return: Réponse.
        :rtype: BaobabResponse
        """
        return self.web_api_caller.call(request)

    def get(
        self,
        path: str,
        *,
        query_params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout_seconds: float | None = None,
    ) -> BaobabResponse:
        """Raccourci GET."""

        req = BaobabRequest(
            method=HttpMethod.GET,
            path=path,
            query_params={} if query_params is None else dict(query_params),
            headers={} if headers is None else dict(headers),
            timeout_seconds=timeout_seconds,
        )
        return self.call(req)

    def post(
        self,
        path: str,
        *,
        query_params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        json_body: object | None = None,
        form_body: Mapping[str, str] | None = None,
        timeout_seconds: float | None = None,
    ) -> BaobabResponse:
        """Raccourci POST."""

        req = BaobabRequest(
            method=HttpMethod.POST,
            path=path,
            query_params={} if query_params is None else dict(query_params),
            headers={} if headers is None else dict(headers),
            json_body=json_body,
            form_body=form_body,
            timeout_seconds=timeout_seconds,
        )
        return self.call(req)

    def put(
        self,
        path: str,
        *,
        query_params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        json_body: object | None = None,
        form_body: Mapping[str, str] | None = None,
        timeout_seconds: float | None = None,
    ) -> BaobabResponse:
        """Raccourci PUT."""

        req = BaobabRequest(
            method=HttpMethod.PUT,
            path=path,
            query_params={} if query_params is None else dict(query_params),
            headers={} if headers is None else dict(headers),
            json_body=json_body,
            form_body=form_body,
            timeout_seconds=timeout_seconds,
        )
        return self.call(req)

    def patch(
        self,
        path: str,
        *,
        query_params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        json_body: object | None = None,
        form_body: Mapping[str, str] | None = None,
        timeout_seconds: float | None = None,
    ) -> BaobabResponse:
        """Raccourci PATCH."""

        req = BaobabRequest(
            method=HttpMethod.PATCH,
            path=path,
            query_params={} if query_params is None else dict(query_params),
            headers={} if headers is None else dict(headers),
            json_body=json_body,
            form_body=form_body,
            timeout_seconds=timeout_seconds,
        )
        return self.call(req)

    def delete(
        self,
        path: str,
        *,
        query_params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout_seconds: float | None = None,
    ) -> BaobabResponse:
        """Raccourci DELETE."""

        req = BaobabRequest(
            method=HttpMethod.DELETE,
            path=path,
            query_params={} if query_params is None else dict(query_params),
            headers={} if headers is None else dict(headers),
            timeout_seconds=timeout_seconds,
        )
        return self.call(req)

    def head(
        self,
        path: str,
        *,
        query_params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout_seconds: float | None = None,
    ) -> BaobabResponse:
        """Raccourci HEAD."""

        req = BaobabRequest(
            method=HttpMethod.HEAD,
            path=path,
            query_params={} if query_params is None else dict(query_params),
            headers={} if headers is None else dict(headers),
            timeout_seconds=timeout_seconds,
        )
        return self.call(req)

    def options(
        self,
        path: str,
        *,
        query_params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout_seconds: float | None = None,
    ) -> BaobabResponse:
        """Raccourci OPTIONS."""

        req = BaobabRequest(
            method=HttpMethod.OPTIONS,
            path=path,
            query_params={} if query_params is None else dict(query_params),
            headers={} if headers is None else dict(headers),
            timeout_seconds=timeout_seconds,
        )
        return self.call(req)
