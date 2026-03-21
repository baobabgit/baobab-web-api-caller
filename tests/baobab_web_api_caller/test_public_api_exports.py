"""Tests du contrat public exporté par le package racine (1.0.0+)."""

from __future__ import annotations

import baobab_web_api_caller


class TestPublicApiExports:
    """Vérifie la surface stable ``__all__``."""

    def test_all_names_are_importable_and_unique(self) -> None:
        """Chaque nom de ``__all__`` doit référencer un objet importable."""

        seen: set[str] = set()
        for name in baobab_web_api_caller.__all__:
            assert name not in seen, f"duplicate export: {name}"
            seen.add(name)
            assert hasattr(baobab_web_api_caller, name), f"missing export: {name}"
            assert getattr(baobab_web_api_caller, name) is not None

    def test_all_sorted_alphabetically_for_maintainability(self) -> None:
        """Facilite les revues et la détection de doublons."""

        assert baobab_web_api_caller.__all__ == sorted(baobab_web_api_caller.__all__)

    def test_version_in_all(self) -> None:
        """La version fait partie du contrat documenté."""

        assert "__version__" in baobab_web_api_caller.__all__
