"""Hooks et garde-fous pour les tests d'intégration externes."""

from __future__ import annotations

import os

import pytest
import requests

from tests.baobab_web_api_caller.integration_external.helpers import (
    HTTPBIN_BASE_URL,
    POSTMAN_ECHO_BASE_URL,
)

_ENV_ENABLE = "BAOBAB_RUN_EXTERNAL_INTEGRATION"
_PROBE_TIMEOUT_SECONDS = 8


class _ReachabilityCache:
    """Évite les sondes réseau répétées au sein d'une même session pytest."""

    checked: bool = False
    ok: bool = False


def _probe_public_test_services() -> bool:
    """Retourne True si HTTPBin et Postman Echo répondent (GET simple)."""

    endpoints = (
        f"{HTTPBIN_BASE_URL}/get",
        f"{POSTMAN_ECHO_BASE_URL}/get",
    )
    for url in endpoints:
        try:
            response = requests.get(url, timeout=_PROBE_TIMEOUT_SECONDS)
            response.raise_for_status()
        except (OSError, requests.RequestException):
            return False
    return True


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Active les tests uniquement sur opt-in ; saute si les services sont injoignables."""

    if item.get_closest_marker("integration_external") is None:
        return

    if os.environ.get(_ENV_ENABLE, "").strip() != "1":
        pytest.skip(
            f"Tests d'intégration externes désactivés : définir {_ENV_ENABLE}=1 "
            "(voir README / docs/03_release_validation_checklist.md)."
        )

    if not _ReachabilityCache.checked:
        _ReachabilityCache.ok = _probe_public_test_services()
        _ReachabilityCache.checked = True

    if not _ReachabilityCache.ok:
        pytest.skip(
            "Services de test publics injoignables (HTTPBin et/ou Postman Echo) ; "
            "vérifiez le réseau ou réessayez plus tard."
        )


@pytest.fixture
def require_delay_timeout_scenario() -> None:
    """Scénario delay/timeout optionnel (évite la fragilité sur réseaux lents)."""

    if os.environ.get("BAOBAB_EXTERNAL_INTEGRATION_TIMEOUT_TEST", "").strip() != "1":
        pytest.skip(
            "Scénario delay/timeout optionnel : définir "
            "BAOBAB_EXTERNAL_INTEGRATION_TIMEOUT_TEST=1 pour l'exécuter."
        )
