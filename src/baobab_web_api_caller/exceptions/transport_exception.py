"""Exceptions liées au transport HTTP(S)."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)


class TransportException(BaobabWebApiCallerException):
    """Erreur de transport (ex: réseau, TLS, DNS, connexion)."""
