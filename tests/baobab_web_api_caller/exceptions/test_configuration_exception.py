"""Tests de `ConfigurationException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestConfigurationException:
    """Tests unitaires pour `ConfigurationException`."""

    def test_inheritance(self) -> None:
        """Vérifie l'héritage."""

        assert issubclass(ConfigurationException, BaobabWebApiCallerException)

    def test_instantiation(self) -> None:
        """Vérifie l'instanciation."""

        exc = ConfigurationException("invalid")
        assert str(exc) == "invalid"
