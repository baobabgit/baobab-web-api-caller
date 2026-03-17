"""Contrat d'exécution des requêtes HTTP."""

from __future__ import annotations

from abc import ABC, abstractmethod

from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse


class BaobabWebApiCaller(ABC):
    """Contrat bas niveau d'exécution d'une requête HTTP.

    Cette abstraction permet d'isoler l'exécution (transport) des couches supérieures (service,
    mapping d'erreurs, pagination).
    """

    @abstractmethod
    def call(self, request: BaobabRequest) -> BaobabResponse:
        """Exécute une requête et retourne une réponse.

        :param request: Requête à exécuter.
        :type request: BaobabRequest
        :return: Réponse normalisée.
        :rtype: BaobabResponse
        """
