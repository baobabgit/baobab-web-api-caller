"""Exceptions liées aux timeouts."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.transport_exception import TransportException


class TimeoutException(TransportException):
    """Erreur de délai dépassé lors d'un appel réseau."""
