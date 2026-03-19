"""Tests de `PageExtractor`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import pytest

from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.pagination.page_extractor import PageExtractor


@dataclass(frozen=True, slots=True)
class FakePageExtractor(PageExtractor[int]):
    """Implémentation concrète locale pour tester le contrat abstrait."""

    items: Sequence[int] = (1, 2)

    def extract_items(self, response: BaobabResponse) -> Sequence[int]:
        """Retourne les items configurés."""

        return self.items


class TestPageExtractor:
    """Tests unitaires pour `PageExtractor`."""

    def test_is_abstract(self) -> None:
        """La classe abstraite ne doit pas être instanciée."""

        with pytest.raises(TypeError):
            PageExtractor()  # pyright: ignore[reportGeneralTypeIssues]

    def test_extract_contract_returns_items(self) -> None:
        """Vérifie le type et la valeur de retour."""

        response = BaobabResponse(status_code=200, headers={}, text="ok", json_data=None)
        extractor = FakePageExtractor(items=(3, 4))
        assert extractor.extract_items(response) == (3, 4)

