"""Exception ressource introuvable."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.client_http_exception import ClientHttpException


class ResourceNotFoundException(ClientHttpException):
    """Ressource non trouvée (HTTP 404)."""
