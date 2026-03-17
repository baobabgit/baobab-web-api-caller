"""Exceptions de haut niveau liées à l'appel de service."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)


class ServiceCallException(BaobabWebApiCallerException):
    """Erreur lors d'un appel à un service distant (façade)."""
