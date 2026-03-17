"""Exemple minimal d'utilisation du Paginator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.pagination.next_page_url_extractor import NextPageUrlExtractor
from baobab_web_api_caller.pagination.page_extractor import PageExtractor
from baobab_web_api_caller.pagination.paginator import Paginator
from baobab_web_api_caller.service.baobab_service_caller import BaobabServiceCaller
from baobab_web_api_caller.transport.http_transport_caller import HttpTransportCaller
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory


@dataclass(frozen=True, slots=True)
class ItemsExtractor(PageExtractor[object]):
    """Extrait la liste d'items depuis `response.json_data`."""

    def extract_items(self, response: BaobabResponse) -> Sequence[object]:
        assert isinstance(response.json_data, dict)
        items = response.json_data.get("items", [])
        assert isinstance(items, list)
        return items


@dataclass(frozen=True, slots=True)
class NextUrlExtractor(NextPageUrlExtractor):
    """Extrait l'URL de page suivante depuis `response.json_data`."""

    def extract_next_page_url(self, response: BaobabResponse) -> str | None:
        assert isinstance(response.json_data, dict)
        next_url = response.json_data.get("next")
        return None if next_url is None else str(next_url)


def main() -> None:
    cfg = ServiceConfig(base_url="https://example.com")
    transport = HttpTransportCaller.from_service_config(
        service_config=cfg, session_factory=RequestsSessionFactory()
    )
    service = BaobabServiceCaller(service_config=cfg, web_api_caller=transport)

    paginator = Paginator(
        service_caller=service,
        page_extractor=ItemsExtractor(),
        next_page_url_extractor=NextUrlExtractor(),
    )
    initial = BaobabRequest(
        method=HttpMethod.GET, path="/items", query_params={"page": "1"}, headers={}
    )
    _ = list(paginator.items(initial))


if __name__ == "__main__":
    main()
