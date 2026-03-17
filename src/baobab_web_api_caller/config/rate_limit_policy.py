"""Politique de limitation de débit (throttling)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


@dataclass(frozen=True, slots=True)
class RateLimitPolicy:
    """Décrit une politique de limitation de débit.

    Cette classe modélise uniquement des paramètres. Elle n'implémente pas l'attente, qui sera
    prise en charge par la couche transport.

    :param min_interval_seconds: Intervalle minimal entre deux appels (en secondes).
    :type min_interval_seconds: float
    :raises ConfigurationException: Si les paramètres sont invalides.
    """

    min_interval_seconds: float = 0.0

    def __post_init__(self) -> None:
        if not isinstance(self.min_interval_seconds, (int, float)) or self.min_interval_seconds < 0:
            raise ConfigurationException("min_interval_seconds must be a float >= 0")
