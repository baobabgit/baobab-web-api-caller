"""Construction d'URL de requête."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlencode

from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


@dataclass(frozen=True, slots=True)
class RequestUrlBuilder:
    """Construit l'URL finale à partir d'une base URL et d'une requête.

    :param base_url: Base URL normalisée (sans ``/`` final).
    :type base_url: str
    :raises ConfigurationException: Si la base URL est invalide.
    """

    base_url: str

    def __post_init__(self) -> None:
        if not isinstance(self.base_url, str) or self.base_url.strip() == "":
            raise ConfigurationException("base_url must be a non-empty string")
        if self.base_url.endswith("/"):
            raise ConfigurationException("base_url must not end with '/'")

    def build(self, request: BaobabRequest) -> str:
        """Construit l'URL à appeler.

        :param request: Requête.
        :type request: BaobabRequest
        :return: URL finale.
        :rtype: str
        """

        if not request.path.startswith("/"):
            raise ConfigurationException("request.path must start with '/'")

        url = f"{self.base_url}{request.path}"
        if request.query_params:
            items: list[tuple[str, str]] = []
            for key, value in request.query_params.items():
                if isinstance(value, str):
                    items.append((key, value))
                else:
                    for v in value:
                        items.append((key, v))
            query = urlencode(items, doseq=True, safe=":/")
            return f"{url}?{query}"
        return url
