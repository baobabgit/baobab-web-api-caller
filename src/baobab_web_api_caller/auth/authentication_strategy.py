"""Abstraction des stratégies d'authentification."""

from __future__ import annotations

from abc import ABC, abstractmethod

from baobab_web_api_caller.core.baobab_request import BaobabRequest


class AuthenticationStrategy(ABC):
    """Stratégie d'authentification appliquée à une requête.

    La stratégie doit être pure du point de vue du modèle : elle ne doit pas muter l'objet de
    requête mais retourner une nouvelle instance si des modifications sont nécessaires.
    """

    @abstractmethod
    def apply(self, request: BaobabRequest) -> BaobabRequest:
        """Applique l'authentification à une requête.

        :param request: Requête d'entrée.
        :type request: BaobabRequest
        :return: Requête authentifiée (même instance si aucune modification n'est requise).
        :rtype: BaobabRequest
        """
