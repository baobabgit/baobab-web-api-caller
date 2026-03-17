"""Abstraction d'attente pour retry/throttling testables."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Sleeper(ABC):
    """Effectue une attente en secondes."""

    @abstractmethod
    def sleep(self, seconds: float) -> None:
        """Attend `seconds` secondes."""
