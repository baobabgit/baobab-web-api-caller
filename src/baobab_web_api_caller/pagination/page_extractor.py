"""Contrat d'extraction d'items depuis une page."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

from baobab_web_api_caller.core.baobab_response import BaobabResponse

TItem = TypeVar("TItem")  # pylint: disable=invalid-name


class PageExtractor(ABC, Generic[TItem]):
    """Extrait les items d'une réponse paginée."""

    @abstractmethod
    def extract_items(self, response: BaobabResponse) -> Sequence[TItem]:
        """Extrait les items d'une page.

        :param response: Réponse décodée.
        :type response: BaobabResponse
        :return: Items.
        :rtype: Sequence[TItem]
        """
