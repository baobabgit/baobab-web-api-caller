"""Tests de `NextPageUrlExtractor`."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.pagination.next_page_url_extractor import (
    NextPageUrlExtractor,
)


@dataclass(frozen=True, slots=True)
class FakeNextPageUrlExtractor(NextPageUrlExtractor):
    """Implémentation concrète locale pour tester le contrat abstrait."""

    next_url: str | None = "/items?page=2"

    def extract_next_page_url(self, response: BaobabResponse) -> str | None:
        """Retourne une valeur configurée."""

        return self.next_url


class TestNextPageUrlExtractor:
    """Tests unitaires pour `NextPageUrlExtractor`."""

    def test_is_abstract(self) -> None:
        """La classe abstraite ne doit pas être instanciée."""

        cls = NextPageUrlExtractor
        with pytest.raises(TypeError):
            # pylint: disable=abstract-class-instantiated
            cls()  # type: ignore[abstract]  # pyright: ignore[reportGeneralTypeIssues]

    def test_extract_contract_returns_str_or_none(self) -> None:
        """Vérifie la valeur de retour d'extract_next_page_url."""

        response = BaobabResponse(status_code=200, headers={}, text="ok", json_data=None)
        extractor = FakeNextPageUrlExtractor(next_url="/items?page=2")
        assert extractor.extract_next_page_url(response) == "/items?page=2"

        extractor_none = FakeNextPageUrlExtractor(next_url=None)
        assert extractor_none.extract_next_page_url(response) is None
