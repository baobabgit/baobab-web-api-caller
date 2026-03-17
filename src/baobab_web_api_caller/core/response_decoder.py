"""Abstraction du décodage de réponse."""

from __future__ import annotations

from abc import ABC, abstractmethod

from baobab_web_api_caller.core.baobab_response import BaobabResponse


class ResponseDecoder(ABC):
    """Décode une :class:`~baobab_web_api_caller.core.baobab_response.BaobabResponse`.

    Le décodage est séparé du transport afin de rester testable et interchangeable.
    """

    @abstractmethod
    def decode(self, response: BaobabResponse) -> BaobabResponse:
        """Retourne une réponse éventuellement enrichie (ex: json décodé).

        :param response: Réponse brute.
        :type response: BaobabResponse
        :return: Réponse décodée/enrichie.
        :rtype: BaobabResponse
        """
