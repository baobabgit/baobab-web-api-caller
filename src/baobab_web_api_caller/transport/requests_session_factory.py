"""Factory de sessions `requests`."""

from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass(frozen=True, slots=True)
class RequestsSessionFactory:
    """Crée des instances de :class:`requests.Session`.

    Cette abstraction permet d'injecter des doubles de tests (sessions factices) dans le transport.
    """

    def create(self) -> requests.Session:
        """Crée une session requests.

        :return: Session.
        :rtype: requests.Session
        """

        return requests.Session()
