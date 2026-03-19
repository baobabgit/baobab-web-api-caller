"""Tests de `Paginator`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import pytest

from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.baobab_web_api_caller import BaobabWebApiCaller
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.core.request_url_builder import RequestUrlBuilder
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException
from baobab_web_api_caller.pagination.next_page_url_extractor import NextPageUrlExtractor
from baobab_web_api_caller.pagination.page_extractor import PageExtractor
from baobab_web_api_caller.pagination.paginator import Paginator
from baobab_web_api_caller.service.baobab_service_caller import BaobabServiceCaller


@dataclass(frozen=True, slots=True)
class FakePageExtractor(PageExtractor[int]):
    """Extracteur d'items depuis `response.json_data`."""

    def extract_items(self, response: BaobabResponse) -> Sequence[int]:
        assert isinstance(response.json_data, dict)
        items = response.json_data["items"]
        assert isinstance(items, list)
        return [int(x) for x in items]


@dataclass(frozen=True, slots=True)
class FakeNextPageUrlExtractor(NextPageUrlExtractor):
    """Extracteur de next URL depuis `response.json_data`."""

    def extract_next_page_url(self, response: BaobabResponse) -> str | None:
        assert isinstance(response.json_data, dict)
        url = response.json_data.get("next")
        if url is None:
            return None
        assert isinstance(url, str)
        return url


@dataclass(frozen=True, slots=True)
class MapCaller(BaobabWebApiCaller):
    """Caller bas niveau retournant une réponse par URL."""

    responses_by_url: dict[str, BaobabResponse]
    last_urls: list[str]

    def call(self, request: BaobabRequest) -> BaobabResponse:
        url = RequestUrlBuilder(base_url="https://example.com").build(request)
        self.last_urls.append(url)
        return self.responses_by_url[url]


class TestPaginator:
    """Tests unitaires de pagination multi-pages."""

    def test_pages_and_items_iterate_over_multiple_pages_relative_urls(self) -> None:
        """Enchaînement sur pages via URL relative."""

        responses = {
            "https://example.com/items?page=1": BaobabResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                json_data={"items": [1, 2], "next": "/items?page=2"},
            ),
            "https://example.com/items?page=2": BaobabResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                json_data={"items": [3], "next": None},
            ),
        }
        low = MapCaller(responses_by_url=responses, last_urls=[])
        service = BaobabServiceCaller(
            service_config=ServiceConfig(base_url="https://example.com"), web_api_caller=low
        )
        paginator = Paginator(
            service_caller=service,
            page_extractor=FakePageExtractor(),
            next_page_url_extractor=FakeNextPageUrlExtractor(),
        )

        initial = BaobabRequest(
            method=HttpMethod.GET,
            path="/items",
            query_params={"page": "1"},
            headers={},
        )

        items = list(paginator.items(initial))
        assert items == [1, 2, 3]
        assert low.last_urls == [
            "https://example.com/items?page=1",
            "https://example.com/items?page=2",
        ]

    def test_pagination_preserves_repeated_query_params(self) -> None:
        """Les paramètres dupliqués dans next_page_url sont préservés en séquences."""

        responses = {
            "https://example.com/items?page=1&tag=a&tag=b": BaobabResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                json_data={
                    "items": [1],
                    "next": "/items?page=2&tag=a&tag=b",
                },
            ),
            "https://example.com/items?page=2&tag=a&tag=b": BaobabResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                json_data={"items": [2], "next": None},
            ),
        }
        low = MapCaller(responses_by_url=responses, last_urls=[])
        service = BaobabServiceCaller(
            service_config=ServiceConfig(base_url="https://example.com"), web_api_caller=low
        )
        paginator = Paginator(
            service_caller=service,
            page_extractor=FakePageExtractor(),
            next_page_url_extractor=FakeNextPageUrlExtractor(),
        )

        initial = BaobabRequest(
            method=HttpMethod.GET,
            path="/items",
            query_params={"page": "1", "tag": ["a", "b"]},
            headers={},
        )

        items = list(paginator.items(initial))
        assert items == [1, 2]
        assert low.last_urls == [
            "https://example.com/items?page=1&tag=a&tag=b",
            "https://example.com/items?page=2&tag=a&tag=b",
        ]

    def test_pagination_preserves_repeated_query_params_for_multiple_keys(self) -> None:
        """Plusieurs clés dupliquées simultanément sont préservées."""

        responses = {
            "https://example.com/items?page=1&tag=a&tag=b&cat=c&cat=d": BaobabResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                json_data={
                    "items": [1],
                    "next": "/items?page=2&tag=a&tag=b&cat=c&cat=d",
                },
            ),
            "https://example.com/items?page=2&tag=a&tag=b&cat=c&cat=d": BaobabResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                json_data={"items": [2], "next": None},
            ),
        }
        low = MapCaller(responses_by_url=responses, last_urls=[])
        service = BaobabServiceCaller(
            service_config=ServiceConfig(base_url="https://example.com"), web_api_caller=low
        )
        paginator = Paginator(
            service_caller=service,
            page_extractor=FakePageExtractor(),
            next_page_url_extractor=FakeNextPageUrlExtractor(),
        )

        initial = BaobabRequest(
            method=HttpMethod.GET,
            path="/items",
            query_params={"page": "1", "tag": ["a", "b"], "cat": ["c", "d"]},
            headers={},
        )

        items = list(paginator.items(initial))
        assert items == [1, 2]
        assert low.last_urls == [
            "https://example.com/items?page=1&tag=a&tag=b&cat=c&cat=d",
            "https://example.com/items?page=2&tag=a&tag=b&cat=c&cat=d",
        ]

    def test_next_page_absolute_url_must_match_service_host(self) -> None:
        """URL suivante absolue vers un autre host -> ConfigurationException."""

        responses = {
            "https://example.com/items?page=1": BaobabResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                json_data={"items": [1], "next": "https://evil.example/items?page=2"},
            ),
        }
        low = MapCaller(responses_by_url=responses, last_urls=[])
        service = BaobabServiceCaller(
            service_config=ServiceConfig(base_url="https://example.com"), web_api_caller=low
        )
        paginator = Paginator(
            service_caller=service,
            page_extractor=FakePageExtractor(),
            next_page_url_extractor=FakeNextPageUrlExtractor(),
        )
        initial = BaobabRequest(
            method=HttpMethod.GET, path="/items", query_params={"page": "1"}, headers={}
        )

        with pytest.raises(ConfigurationException):
            list(paginator.items(initial))
