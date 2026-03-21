"""Scénarios release gate contre `https://postman-echo.com`."""

from __future__ import annotations

from typing import Mapping

import pytest

from baobab_web_api_caller.exceptions.timeout_exception import TimeoutException
from tests.baobab_web_api_caller.integration_external.helpers import (
    POSTMAN_ECHO_BASE_URL,
    make_release_gate_service_caller,
)


def _header_value_case_insensitive(headers: Mapping[str, str], name: str) -> str | None:
    """Lit un en-tête HTTP en ignorant la casse des noms."""

    lowered = name.lower()
    for key, value in headers.items():
        if key.lower() == lowered:
            return value
    return None


@pytest.mark.integration_external
class TestPostmanEchoReleaseGate:
    """Contrôles complémentaires sur un second fournisseur public."""

    def test_get_query_params_echoed_in_json(self) -> None:
        """Les query params sont présents dans le corps JSON d'écho."""

        service = make_release_gate_service_caller(POSTMAN_ECHO_BASE_URL)
        response = service.get(
            "/get",
            query_params={"baobab": "postman", "layer": "integration"},
        )
        assert response.status_code == 200
        assert response.json_data is not None
        payload = response.json_data
        assert isinstance(payload, dict)
        args = payload.get("args")
        assert isinstance(args, dict)
        assert args.get("baobab") == "postman"
        assert args.get("layer") == "integration"

    def test_post_json_body_echoed(self) -> None:
        """Le JSON POST est rejoué dans la réponse d'écho."""

        service = make_release_gate_service_caller(POSTMAN_ECHO_BASE_URL)
        body = {"check": "post_json", "n": 2}
        response = service.post("/post", json_body=body)
        assert response.status_code == 200
        assert response.json_data is not None
        payload = response.json_data
        assert isinstance(payload, dict)
        assert payload.get("json") == body

    def test_explicit_status_code_from_status_endpoint(self) -> None:
        """L'endpoint `/status/{code}` renvoie le statut demandé (hors 2xx « succès » HTTP)."""

        service = make_release_gate_service_caller(POSTMAN_ECHO_BASE_URL)
        response = service.get("/status/201")
        assert response.status_code == 201

    def test_response_headers_surface_on_baobab_response(self) -> None:
        """Les en-têtes de réponse renvoyés par Postman Echo sont lisibles côté client."""

        service = make_release_gate_service_caller(POSTMAN_ECHO_BASE_URL)
        response = service.get(
            "/response-headers",
            query_params={"X-Baobab-Release-Gate": "observed"},
        )
        assert response.status_code == 200
        value = _header_value_case_insensitive(
            response.headers,
            "X-Baobab-Release-Gate",
        )
        assert value == "observed"

    @pytest.mark.usefixtures("require_delay_timeout_scenario")
    def test_delay_exceeding_timeout_raises_timeout_exception(self) -> None:
        """Délai serveur > timeout client : `TimeoutException` (scénario optionnel)."""

        service = make_release_gate_service_caller(
            POSTMAN_ECHO_BASE_URL,
            default_timeout_seconds=1.0,
        )
        with pytest.raises(TimeoutException):
            service.get("/delay/3", timeout_seconds=1.0)
