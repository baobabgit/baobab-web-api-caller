"""Configuration d'un service distant."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping
from urllib.parse import urlparse

from baobab_web_api_caller.auth.authentication_strategy import AuthenticationStrategy
from baobab_web_api_caller.auth.no_authentication_strategy import NoAuthenticationStrategy
from baobab_web_api_caller.config.rate_limit_policy import RateLimitPolicy
from baobab_web_api_caller.config.retry_policy import RetryPolicy
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException
from baobab_web_api_caller.utils.mapping_utils import freeze_str_mapping


@dataclass(frozen=True, slots=True)
class ServiceConfig:
    """Configuration transverse d'un service distant.

    :param base_url: Base URL du service (ex: ``https://api.example.com``).
    :type base_url: str
    :param default_headers: Headers appliqués par défaut à chaque requête.
    :type default_headers: Mapping[str, str]
    :param authentication_strategy: Stratégie d'authentification à appliquer.
    :type authentication_strategy: AuthenticationStrategy
    :param default_timeout_seconds: Timeout par défaut en secondes.
    :type default_timeout_seconds: float | None
    :param retry_policy: Politique de retry.
    :type retry_policy: RetryPolicy
    :param rate_limit_policy: Politique de throttling.
    :type rate_limit_policy: RateLimitPolicy
    :raises ConfigurationException: Si la configuration est invalide.
    """

    base_url: str
    default_headers: Mapping[str, str] = MappingProxyType({})
    authentication_strategy: AuthenticationStrategy = NoAuthenticationStrategy()
    default_timeout_seconds: float | None = None
    retry_policy: RetryPolicy = RetryPolicy()
    rate_limit_policy: RateLimitPolicy = RateLimitPolicy()

    def __post_init__(self) -> None:
        normalized = self._normalize_and_validate_base_url(self.base_url)
        object.__setattr__(self, "base_url", normalized)
        object.__setattr__(
            self, "default_headers", freeze_str_mapping(self.default_headers, "default_headers")
        )

        if not isinstance(self.authentication_strategy, AuthenticationStrategy):
            raise ConfigurationException(
                "authentication_strategy must be an AuthenticationStrategy"
            )

        if self.default_timeout_seconds is not None and self.default_timeout_seconds <= 0:
            raise ConfigurationException("default_timeout_seconds must be positive when provided")

        if not isinstance(self.retry_policy, RetryPolicy):
            raise ConfigurationException("retry_policy must be a RetryPolicy")
        if not isinstance(self.rate_limit_policy, RateLimitPolicy):
            raise ConfigurationException("rate_limit_policy must be a RateLimitPolicy")

    @staticmethod
    def _normalize_and_validate_base_url(base_url: str) -> str:
        if not isinstance(base_url, str) or base_url.strip() == "":
            raise ConfigurationException("base_url must be a non-empty string")

        trimmed = base_url.strip()
        parsed = urlparse(trimmed)
        if parsed.scheme not in {"http", "https"}:
            raise ConfigurationException("base_url must start with http:// or https://")
        if parsed.netloc == "":
            raise ConfigurationException("base_url must include a host")

        normalized = trimmed.rstrip("/")
        return normalized
