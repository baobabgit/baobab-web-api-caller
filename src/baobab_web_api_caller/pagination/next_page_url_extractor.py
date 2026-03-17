"""Contrat d'extraction de l'URL de page suivante."""

from __future__ import annotations

from abc import ABC, abstractmethod

from baobab_web_api_caller.core.baobab_response import BaobabResponse


class NextPageUrlExtractor(ABC):
    """Détermine l'URL de page suivante à partir d'une réponse."""

    @abstractmethod
    def extract_next_page_url(self, response: BaobabResponse) -> str | None:
        """Retourne l'URL de page suivante si présente.

        :param response: Réponse décodée.
        :type response: BaobabResponse
        :return: URL suivante ou None.
        :rtype: str | None
        """
