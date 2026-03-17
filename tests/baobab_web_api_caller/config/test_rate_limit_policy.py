"""Tests de `RateLimitPolicy`."""

from __future__ import annotations

import pytest

from baobab_web_api_caller.config.rate_limit_policy import RateLimitPolicy
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestRateLimitPolicy:
    """Tests unitaires pour `RateLimitPolicy`."""

    def test_default_is_valid(self) -> None:
        """Vérifie la configuration par défaut."""

        policy = RateLimitPolicy()
        assert policy.min_interval_seconds == 0.0

    def test_negative_interval_is_invalid(self) -> None:
        """Refuse un intervalle négatif."""

        with pytest.raises(ConfigurationException):
            RateLimitPolicy(min_interval_seconds=-0.1)
