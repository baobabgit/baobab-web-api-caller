"""Exceptions liées à l'authentification."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.http_exception import HttpException


class AuthenticationException(HttpException):
    """Erreur d'authentification (ex: credentials invalides, token expiré).

    Hérite de :class:`HttpException` afin d'exposer le contexte de réponse HTTP comme les autres
    erreurs HTTP du projet.
    """
