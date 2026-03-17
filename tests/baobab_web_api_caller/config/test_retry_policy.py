"""Tests de `RetryPolicy`."""

from __future__ import annotations

import pytest

from baobab_web_api_caller.config.retry_policy import RetryPolicy
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestRetryPolicy:
    """Tests unitaires pour `RetryPolicy`."""

    def test_default_is_valid(self) -> None:
        """Vérifie la configuration par défaut."""

        policy = RetryPolicy()
        assert policy.max_attempts == 1
        assert policy.backoff_seconds == 0.0
        assert policy.backoff_multiplier == 1.0

    def test_invalid_max_attempts(self) -> None:
        """Refuse max_attempts < 1."""

        with pytest.raises(ConfigurationException):
            RetryPolicy(max_attempts=0)

    def test_invalid_backoff_seconds(self) -> None:
        """Refuse backoff négatif."""

        with pytest.raises(ConfigurationException):
            RetryPolicy(backoff_seconds=-1)

    def test_invalid_multiplier(self) -> None:
        """Refuse un multiplicateur < 1."""

        with pytest.raises(ConfigurationException):
            RetryPolicy(backoff_multiplier=0.5)
