"""Exceptions liées aux réponses HTTP en erreur."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)


class HttpException(BaobabWebApiCallerException):
    """Erreur HTTP (4xx/5xx) renvoyée par le serveur distant.

    Les exceptions HTTP portent un sous-ensemble des informations de réponse brutes afin
    d'améliorer le diagnostic en environnement de production.

    :param status_code: Code de statut HTTP.
    :type status_code: int
    :param message: Message lisible décrivant l'erreur.
    :type message: str
    :param body_excerpt: Extrait du corps texte de la réponse (optionnel).
    :type body_excerpt: str | None
    :param headers: Sous-ensemble d'en-têtes jugés utiles pour le diagnostic (optionnel).
    :type headers: dict[str, str] | None
    """

    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        body_excerpt: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        details_parts: list[str] = [message]
        if body_excerpt:
            details_parts.append(f"body={body_excerpt}")
        if headers:
            headers_str = ", ".join(f"{k}={v}" for k, v in headers.items())
            details_parts.append(f"headers={headers_str}")

        super().__init__("; ".join(details_parts))

        self.status_code: int = int(status_code)
        self.body_excerpt: str | None = body_excerpt
        self.headers: dict[str, str] | None = dict(headers) if headers is not None else None
