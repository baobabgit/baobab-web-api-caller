"""Utilitaires de manipulation de mappings typés."""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


def freeze_str_mapping(value: Mapping[str, str], field_name: str) -> Mapping[str, str]:
    """Valide et fige un mapping ``str -> str``.

    :param value: Mapping à valider.
    :type value: Mapping[str, str]
    :param field_name: Nom du champ pour les messages d'erreur.
    :type field_name: str
    :return: Mapping figé.
    :rtype: Mapping[str, str]
    :raises ConfigurationException: Si le mapping contient des clés/valeurs invalides.
    """

    if not isinstance(value, Mapping):
        raise ConfigurationException(f"{field_name} must be a mapping")

    frozen: dict[str, str] = {}
    for k, v in value.items():
        if not isinstance(k, str) or k.strip() == "":
            raise ConfigurationException(f"{field_name} keys must be non-empty strings")
        if not isinstance(v, str):
            raise ConfigurationException(f"{field_name} values must be strings")
        frozen[k] = v
    return MappingProxyType(frozen)
