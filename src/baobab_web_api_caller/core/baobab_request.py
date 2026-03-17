"""Modèle de requête HTTP."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping
from urllib.parse import quote

from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


@dataclass(frozen=True, slots=True)
class BaobabRequest:
    """Représentation typée d'une requête HTTP.

    La requête est volontairement indépendante du transport concret (requests, httpx, ...).

    :param method: Méthode HTTP.
    :type method: HttpMethod
    :param path: Chemin relatif (ex: ``/v1/items``).
    :type path: str
    :param query_params: Paramètres de query string.
    :type query_params: Mapping[str, str]
    :param headers: En-têtes HTTP.
    :type headers: Mapping[str, str]
    :param json_body: Corps JSON (déjà sérialisé en types Python).
    :type json_body: object | None
    :param form_body: Corps de formulaire (application/x-www-form-urlencoded).
    :type form_body: Mapping[str, str] | None
    :param timeout_seconds: Timeout en secondes.
    :type timeout_seconds: float | None
    :raises ConfigurationException: Si les paramètres de la requête sont invalides.
    """

    method: HttpMethod
    path: str
    query_params: Mapping[str, str]
    headers: Mapping[str, str]
    json_body: object | None = None
    form_body: Mapping[str, str] | None = None
    timeout_seconds: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.method, HttpMethod):
            raise ConfigurationException("method must be an HttpMethod")

        normalized_path = self._normalize_and_validate_path(self.path)
        object.__setattr__(self, "path", normalized_path)

        if self.timeout_seconds is not None and self.timeout_seconds <= 0:
            raise ConfigurationException("timeout_seconds must be positive when provided")

        if self.json_body is not None and self.form_body is not None:
            raise ConfigurationException("json_body and form_body are mutually exclusive")

        object.__setattr__(
            self, "query_params", self._freeze_str_mapping(self.query_params, "query_params")
        )
        object.__setattr__(self, "headers", self._freeze_str_mapping(self.headers, "headers"))
        if self.form_body is not None:
            object.__setattr__(
                self, "form_body", self._freeze_str_mapping(self.form_body, "form_body")
            )

    @staticmethod
    def _normalize_and_validate_path(path: str) -> str:
        if not isinstance(path, str) or path.strip() == "":
            raise ConfigurationException("path must be a non-empty string")

        stripped = path.strip()
        lowered = stripped.lower()
        if lowered.startswith("http://") or lowered.startswith("https://"):
            raise ConfigurationException("path must be a relative path, not an absolute URL")

        if not stripped.startswith("/"):
            stripped = f"/{stripped}"

        if " " in stripped:
            raise ConfigurationException("path must not contain spaces")

        # Normalisation minimale: encode les caractères non sûrs sans toucher au '/'.
        return quote(stripped, safe="/-._~")

    @staticmethod
    def _freeze_str_mapping(value: Mapping[str, str], field_name: str) -> Mapping[str, str]:
        if not isinstance(value, Mapping):
            raise ConfigurationException(f"{field_name} must be a mapping")

        frozen: dict[str, str] = {}
        for k, v in value.items():
            if not isinstance(k, str) or k.strip() == "":
                raise ConfigurationException(f"{field_name} keys must be non-empty strings")
            if not isinstance(v, str):
                raise ConfigurationException(f"{field_name} values must be strings")
            frozen[k] = v
        return MappingProxyType(frozen)

    def with_header(self, name: str, value: str) -> "BaobabRequest":
        """Retourne une nouvelle requête avec un header ajouté/écrasé.

        :param name: Nom du header.
        :type name: str
        :param value: Valeur du header.
        :type value: str
        :return: Nouvelle instance.
        :rtype: BaobabRequest
        """

        headers = dict(self.headers)
        headers[name] = value
        return BaobabRequest(
            method=self.method,
            path=self.path,
            query_params=self.query_params,
            headers=headers,
            json_body=self.json_body,
            form_body=self.form_body,
            timeout_seconds=self.timeout_seconds,
        )
