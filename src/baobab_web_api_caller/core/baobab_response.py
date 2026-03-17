"""Modèle de réponse HTTP."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


@dataclass(frozen=True, slots=True)
class BaobabResponse:
    """Représentation typée d'une réponse HTTP.

    :param status_code: Code de statut HTTP.
    :type status_code: int
    :param headers: En-têtes HTTP.
    :type headers: Mapping[str, str]
    :param text: Contenu texte (si disponible).
    :type text: str | None
    :param content: Contenu binaire brut (si disponible).
    :type content: bytes | None
    :param json_data: Contenu JSON déjà décodé (si disponible).
    :type json_data: object | None
    :raises ConfigurationException: Si les paramètres de la réponse sont invalides.
    """

    status_code: int
    headers: Mapping[str, str]
    text: str | None = None
    content: bytes | bytearray | None = None
    json_data: object | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status_code, int):
            raise ConfigurationException("status_code must be an int")
        if self.status_code < 100 or self.status_code > 599:
            raise ConfigurationException("status_code must be between 100 and 599")

        object.__setattr__(self, "headers", self._freeze_headers(self.headers))

        if self.text is not None and not isinstance(self.text, str):
            raise ConfigurationException("text must be a string when provided")
        if isinstance(self.content, bytearray):
            object.__setattr__(self, "content", bytes(self.content))
        if self.content is not None and not isinstance(self.content, bytes):
            raise ConfigurationException("content must be bytes when provided")

    @staticmethod
    def _freeze_headers(headers: Mapping[str, str]) -> Mapping[str, str]:
        if not isinstance(headers, Mapping):
            raise ConfigurationException("headers must be a mapping")

        frozen: dict[str, str] = {}
        for k, v in headers.items():
            if not isinstance(k, str) or k.strip() == "":
                raise ConfigurationException("headers keys must be non-empty strings")
            if not isinstance(v, str):
                raise ConfigurationException("headers values must be strings")
            frozen[k] = v
        return MappingProxyType(frozen)

    @property
    def is_success(self) -> bool:
        """Indique si le status code correspond à une réussite HTTP (2xx)."""

        return 200 <= self.status_code <= 299
