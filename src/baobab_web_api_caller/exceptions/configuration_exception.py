"""Exceptions liées à la configuration."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)


class ConfigurationException(BaobabWebApiCallerException):
    """Erreur de configuration (ex: base URL invalide, paramètres incohérents)."""
