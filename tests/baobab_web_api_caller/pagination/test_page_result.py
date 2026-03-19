"""Tests de `PageResult`."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Sequence

import pytest

from baobab_web_api_caller.pagination.page_result import PageResult


class TestPageResult:
    """Tests unitaires pour `PageResult`."""

    def test_stores_items_and_next_page_url(self) -> None:
        """Vérifie la conservation des champs."""

        items: Sequence[int] = (1, 2)
        page = PageResult(items=items, next_page_url="/items?page=2")
        assert page.items == items
        assert page.next_page_url == "/items?page=2"

    def test_is_frozen(self) -> None:
        """PageResult est immuable (dataclass frozen)."""

        page = PageResult(items=(1,), next_page_url=None)
        with pytest.raises(FrozenInstanceError):
            page.next_page_url = "/other"  # type: ignore[misc]
