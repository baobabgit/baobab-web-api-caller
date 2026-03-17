"""Politique de retry (nouvelle tentative)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Décrit une politique de nouvelle tentative.

    Cette classe modélise uniquement des paramètres. Elle n'implémente pas l'exécution du retry,
    qui sera prise en charge par la couche transport.

    :param max_attempts: Nombre maximum de tentatives (incluant la première).
    :type max_attempts: int
    :param backoff_seconds: Délai initial entre deux tentatives (en secondes).
    :type backoff_seconds: float
    :param backoff_multiplier: Multiplicateur appliqué au backoff après chaque tentative.
    :type backoff_multiplier: float
    :raises ConfigurationException: Si les paramètres sont invalides.
    """

    max_attempts: int = 1
    backoff_seconds: float = 0.0
    backoff_multiplier: float = 1.0

    def __post_init__(self) -> None:
        if not isinstance(self.max_attempts, int) or self.max_attempts < 1:
            raise ConfigurationException("max_attempts must be an int >= 1")
        if not isinstance(self.backoff_seconds, (int, float)) or self.backoff_seconds < 0:
            raise ConfigurationException("backoff_seconds must be a float >= 0")
        if not isinstance(self.backoff_multiplier, (int, float)) or self.backoff_multiplier < 1:
            raise ConfigurationException("backoff_multiplier must be a float >= 1")
