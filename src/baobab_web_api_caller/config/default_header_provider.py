"""Fournisseur d'en-têtes HTTP par défaut."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.utils.mapping_utils import freeze_str_mapping


@dataclass(frozen=True, slots=True)
class DefaultHeaderProvider:
    """Fournit des en-têtes HTTP à appliquer à une requête.

    Les headers de la requête priment sur les headers par défaut (pas d'écrasement involontaire).

    :param default_headers: Headers par défaut (str->str).
    :type default_headers: Mapping[str, str]
    :raises ConfigurationException: Si les headers sont invalides.
    """

    default_headers: Mapping[str, str]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "default_headers", freeze_str_mapping(self.default_headers, "default_headers")
        )

    def apply(self, request: BaobabRequest) -> BaobabRequest:
        """Retourne une nouvelle requête avec les headers par défaut fusionnés.

        :param request: Requête d'entrée.
        :type request: BaobabRequest
        :return: Requête enrichie.
        :rtype: BaobabRequest
        """

        merged = dict(self.default_headers)
        merged.update(dict(request.headers))
        if merged == dict(request.headers):
            return request
        return BaobabRequest(
            method=request.method,
            path=request.path,
            query_params=request.query_params,
            headers=merged,
            json_body=request.json_body,
            form_body=request.form_body,
            timeout_seconds=request.timeout_seconds,
        )
