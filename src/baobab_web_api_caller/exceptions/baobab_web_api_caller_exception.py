"""Exception racine du projet."""

from __future__ import annotations


class BaobabWebApiCallerException(Exception):
    """Exception racine pour toutes les erreurs de la librairie.

    Toutes les exceptions spécifiques au projet doivent dériver de cette classe, directement ou
    indirectement.
    """
