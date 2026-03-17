"""Itération générique sur des pages basées sur une URL suivante."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, TypeVar
from urllib.parse import parse_qsl, urlparse

from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException
from baobab_web_api_caller.pagination.next_page_url_extractor import NextPageUrlExtractor
from baobab_web_api_caller.pagination.page_extractor import PageExtractor
from baobab_web_api_caller.pagination.page_result import PageResult
from baobab_web_api_caller.service.baobab_service_caller import BaobabServiceCaller

TItem = TypeVar("TItem")  # pylint: disable=invalid-name


@dataclass(frozen=True, slots=True)
class Paginator(Generic[TItem]):
    """Paginator générique, basé sur une URL de page suivante.

    Le paginator ne connaît pas le format de la réponse. Il délègue l'extraction des items et de
    l'URL de la page suivante à des extracteurs injectés.
    """

    service_caller: BaobabServiceCaller
    page_extractor: PageExtractor[TItem]
    next_page_url_extractor: NextPageUrlExtractor

    def pages(self, initial_request: BaobabRequest) -> Iterator[PageResult[TItem]]:
        """Itère sur les pages.

        :param initial_request: Requête initiale (souvent GET).
        :type initial_request: BaobabRequest
        :return: Itérateur de pages.
        :rtype: Iterator[PageResult[TItem]]
        """

        request: BaobabRequest | None = initial_request
        while request is not None:
            response = self.service_caller.call(request)
            items = self.page_extractor.extract_items(response)
            next_url = self.next_page_url_extractor.extract_next_page_url(response)
            yield PageResult(items=items, next_page_url=next_url)

            request = (
                None
                if next_url is None
                else self._request_from_next_url(
                    next_url=next_url,
                    base_request=initial_request,
                )
            )

    def items(self, initial_request: BaobabRequest) -> Iterator[TItem]:
        """Itère sur tous les items de toutes les pages."""

        for page in self.pages(initial_request):
            yield from page.items

    def _request_from_next_url(
        self, *, next_url: str, base_request: BaobabRequest
    ) -> BaobabRequest:
        parsed = urlparse(next_url)
        if parsed.scheme in {"http", "https"}:
            base = urlparse(self.service_caller.service_config.base_url)
            if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
                raise ConfigurationException(
                    "next_page_url must target the same host as service_config.base_url"
                )
            path = parsed.path
            query = parsed.query
        else:
            # URL relative (ex: /v1/items?page=2)
            path = parsed.path
            query = parsed.query

        if not path:
            raise ConfigurationException("next_page_url must include a path")
        if not path.startswith("/"):
            path = f"/{path}"

        query_params = self._parse_query_params(query)
        return BaobabRequest(
            method=base_request.method,
            path=path,
            query_params=query_params,
            headers=base_request.headers,
            timeout_seconds=base_request.timeout_seconds,
        )

    @staticmethod
    def _parse_query_params(query: str) -> dict[str, str | list[str]]:
        params: dict[str, str | list[str]] = {}
        for k, v in parse_qsl(query, keep_blank_values=True, strict_parsing=False):
            existing = params.get(k)
            if existing is None:
                params[k] = v
            elif isinstance(existing, list):
                existing.append(v)
            else:
                params[k] = [existing, v]
        return params
