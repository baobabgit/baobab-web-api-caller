"""Tests de bootstrap (métadonnées du package)."""

from __future__ import annotations

import baobab_web_api_caller


class TestPackageMetadata:
    """Classe de tests pour les métadonnées du package."""

    def test_version_is_defined(self) -> None:
        """Vérifie que le package expose une version non vide."""

        assert isinstance(baobab_web_api_caller.__version__, str)
        assert baobab_web_api_caller.__version__.strip() != ""
