"""Scénarios release gate contre `https://httpbin.org`."""

from __future__ import annotations

import pytest

from baobab_web_api_caller.auth.basic_authentication_strategy import BasicAuthenticationStrategy
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.resource_not_found_exception import ResourceNotFoundException
from baobab_web_api_caller.transport.http_transport_caller import HttpTransportCaller
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory
from tests.baobab_web_api_caller.integration_external.helpers import (
    HTTPBIN_BASE_URL,
    make_release_gate_service_caller,
    make_release_gate_service_config,
)


@pytest.mark.integration_external
class TestHttpBinReleaseGate:
    """Contrôle minimal de la façade et du transport contre HTTPBin."""

    def test_get_simple_query_params_visible_in_echo(self) -> None:
        """Les query params simples sont encodés et visibles dans le JSON d'inspection."""

        service = make_release_gate_service_caller(HTTPBIN_BASE_URL)
        response = service.get("/get", query_params={"baobab_q": "release", "lang": "fr"})
        assert response.status_code == 200
        assert response.json_data is not None
        payload = response.json_data
        assert isinstance(payload, dict)
        args = payload.get("args")
        assert isinstance(args, dict)
        assert args.get("baobab_q") == "release"
        assert args.get("lang") == "fr"

    def test_get_multi_value_query_params(self) -> None:
        """Les clés répétées sont transmises et visibles côté HTTPBin."""

        service = make_release_gate_service_caller(HTTPBIN_BASE_URL)
        response = service.get(
            "/get",
            query_params={"tag": ["integration", "release"]},
        )
        assert response.status_code == 200
        assert response.json_data is not None
        payload = response.json_data
        assert isinstance(payload, dict)
        args = payload.get("args")
        assert isinstance(args, dict)
        tag = args.get("tag")
        assert tag == ["integration", "release"]

    def test_get_custom_request_headers_forwarded(self) -> None:
        """Les en-têtes de requête arrivent dans l'écho HTTPBin."""

        service = make_release_gate_service_caller(HTTPBIN_BASE_URL)
        response = service.get(
            "/headers",
            headers={"X-Baobab-Integration": "release-gate"},
        )
        assert response.status_code == 200
        assert response.json_data is not None
        payload = response.json_data
        assert isinstance(payload, dict)
        headers = payload.get("headers")
        assert isinstance(headers, dict)
        # HTTPBin normalise souvent en casse mixte ; on vérifie la présence fonctionnelle.
        keys_lower = {str(k).lower() for k in headers}
        assert "x-baobab-integration" in keys_lower

    def test_post_json_body_echoed(self) -> None:
        """Le corps JSON POST est renvoyé dans le champ `json` d'HTTPBin."""

        service = make_release_gate_service_caller(HTTPBIN_BASE_URL)
        body = {"suite": "integration_external", "step": 1}
        response = service.post("/post", json_body=body, headers={"Accept": "application/json"})
        assert response.status_code == 200
        assert response.json_data is not None
        payload = response.json_data
        assert isinstance(payload, dict)
        assert payload.get("json") == body

    def test_basic_auth_succeeds_against_httpbin(self) -> None:
        """Basic Auth réelle : identifiants publics documentés par HTTPBin (pas de secret)."""

        user, password = "baobab_user", "baobab_pass"
        service = make_release_gate_service_caller(
            HTTPBIN_BASE_URL,
            authentication_strategy=BasicAuthenticationStrategy(username=user, password=password),
        )
        response = service.get(f"/basic-auth/{user}/{password}")
        assert response.status_code == 200
        assert response.json_data is not None
        payload = response.json_data
        assert isinstance(payload, dict)
        assert payload.get("authenticated") is True
        assert payload.get("user") == user

    def test_http_error_maps_to_project_exception_with_context(self) -> None:
        """Erreur HTTP volontaire : `ResourceNotFoundException` + message / attributs enrichis."""

        service = make_release_gate_service_caller(HTTPBIN_BASE_URL)
        with pytest.raises(ResourceNotFoundException) as caught:
            service.get("/status/404")
        exc = caught.value
        assert exc.status_code == 404
        assert "HTTP 404" in str(exc)
        assert exc.body_excerpt is None or isinstance(exc.body_excerpt, str)

    def test_http_transport_caller_raw_path_without_facade(self) -> None:
        """Le transport HTTP réel (sans raccourci façade) transmet bien la requête."""

        cfg = make_release_gate_service_config(HTTPBIN_BASE_URL)
        transport = HttpTransportCaller.from_service_config(cfg, RequestsSessionFactory())
        request = BaobabRequest(
            method=HttpMethod.GET,
            path="/get",
            query_params={"transport": "HttpTransportCaller"},
            headers={},
        )
        response = transport.call(request)
        assert response.status_code == 200
        assert response.json_data is not None
        payload = response.json_data
        assert isinstance(payload, dict)
        args = payload.get("args")
        assert isinstance(args, dict)
        assert args.get("transport") == "HttpTransportCaller"
