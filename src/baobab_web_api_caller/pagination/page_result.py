"""Résultat de page paginée."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

TItem = TypeVar("TItem")  # pylint: disable=invalid-name


@dataclass(frozen=True, slots=True)
class PageResult(Generic[TItem]):
    """Résultat d'une page.

    :param items: Items extraits.
    :type items: Sequence[TItem]
    :param next_page_url: URL de la page suivante, si présente.
    :type next_page_url: str | None
    """

    items: Sequence[TItem]
    next_page_url: str | None
