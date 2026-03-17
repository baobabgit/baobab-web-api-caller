"""Pagination générique basée sur une URL de page suivante."""

from __future__ import annotations

from baobab_web_api_caller.pagination.next_page_url_extractor import NextPageUrlExtractor
from baobab_web_api_caller.pagination.page_extractor import PageExtractor
from baobab_web_api_caller.pagination.page_result import PageResult
from baobab_web_api_caller.pagination.paginator import Paginator

__all__ = ["NextPageUrlExtractor", "PageExtractor", "PageResult", "Paginator"]
