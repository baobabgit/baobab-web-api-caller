"""Tests de `ServiceConfig`."""

from __future__ import annotations

from typing import Mapping, cast

import pytest

from baobab_web_api_caller.auth.bearer_authentication_strategy import BearerAuthenticationStrategy
from baobab_web_api_caller.config.rate_limit_policy import RateLimitPolicy
from baobab_web_api_caller.config.retry_policy import RetryPolicy
from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestServiceConfig:
    """Tests unitaires pour `ServiceConfig`."""

    def test_minimal_config_is_valid_and_normalizes_base_url(self) -> None:
        """Valide la config minimale et normalise le base_url."""

        cfg = ServiceConfig(base_url="https://example.com/")
        assert cfg.base_url == "https://example.com"
        assert not dict(cfg.default_headers)

    def test_base_url_must_be_http_or_https(self) -> None:
        """Refuse d'autres schémas."""

        with pytest.raises(ConfigurationException):
            ServiceConfig(base_url="ftp://example.com")

    def test_base_url_must_have_host(self) -> None:
        """Refuse les URLs sans hôte."""

        with pytest.raises(ConfigurationException):
            ServiceConfig(base_url="https://")

    def test_default_headers_validation(self) -> None:
        """Valide str->str."""

        with pytest.raises(ConfigurationException):
            ServiceConfig(
                base_url="https://example.com", default_headers=cast(Mapping[str, str], {"X": 1})
            )

    def test_timeout_must_be_positive_when_provided(self) -> None:
        """Valide le timeout."""

        with pytest.raises(ConfigurationException):
            ServiceConfig(base_url="https://example.com", default_timeout_seconds=0)

    def test_all_components_can_be_injected(self) -> None:
        """Accepte l'injection d'une stratégie et de politiques."""

        cfg = ServiceConfig(
            base_url="https://example.com",
            default_headers={"Accept": "application/json"},
            authentication_strategy=BearerAuthenticationStrategy(token="t"),
            default_timeout_seconds=1.5,
            retry_policy=RetryPolicy(max_attempts=3, backoff_seconds=0.1, backoff_multiplier=2.0),
            rate_limit_policy=RateLimitPolicy(min_interval_seconds=0.5),
        )
        assert cfg.base_url == "https://example.com"
        assert dict(cfg.default_headers) == {"Accept": "application/json"}
        assert cfg.default_timeout_seconds == 1.5
