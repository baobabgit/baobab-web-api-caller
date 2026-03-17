"""Abstraction de temps pour tests stables."""

from __future__ import annotations

from abc import ABC, abstractmethod


class TimeProvider(ABC):
    """Fournit un temps monotone pour le throttling/retry.

    L'utilisation d'un temps monotone évite les problèmes liés aux changements d'horloge système.
    """

    @abstractmethod
    def monotonic(self) -> float:
        """Retourne un timestamp monotone (secondes)."""
