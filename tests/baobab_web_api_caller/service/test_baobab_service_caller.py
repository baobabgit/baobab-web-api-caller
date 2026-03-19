"""Tests de `BaobabServiceCaller`."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.baobab_web_api_caller import BaobabWebApiCaller
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.service.baobab_service_caller import BaobabServiceCaller


@dataclass(frozen=True, slots=True)
class RecordingCaller(BaobabWebApiCaller):
    """Double de test qui enregistre la dernière requête."""

    last_request: BaobabRequest | None = None

    def call(self, request: BaobabRequest) -> BaobabResponse:
        object.__setattr__(self, "last_request", request)
        return BaobabResponse(status_code=200, headers={})


class TestBaobabServiceCaller:
    """Tests unitaires pour `BaobabServiceCaller`."""

    def test_call_delegates_request_without_merging_default_headers(self) -> None:
        """Ne fusionne pas les headers par défaut : le transport en est responsable."""

        cfg = ServiceConfig(
            base_url="https://example.com",
            default_headers={"Accept": "application/json", "X": "1"},
        )
        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={"q": "x"},
            headers={"X": "2", "X-Req": "1"},
            timeout_seconds=0.5,
        )
        _ = service.call(req)

        assert caller.last_request is not None
        assert caller.last_request.method is HttpMethod.GET
        assert caller.last_request.path == "/v1/items"
        assert dict(caller.last_request.query_params) == {"q": "x"}
        assert dict(caller.last_request.headers) == {"X": "2", "X-Req": "1"}
        assert caller.last_request.timeout_seconds == 0.5

    def test_convenience_methods_delegate_to_call(self) -> None:
        """Vérifie les helpers HTTP."""

        cfg = ServiceConfig(base_url="https://example.com")

        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.get("/ping")
        assert caller.last_request is not None
        assert caller.last_request.method is HttpMethod.GET

        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.post("/items", json_body={"a": 1})
        assert caller.last_request is not None
        assert caller.last_request.method is HttpMethod.POST
        assert caller.last_request.json_body == {"a": 1}

        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.put("/items/1", form_body={"a": "1"})
        assert caller.last_request is not None
        assert caller.last_request.method is HttpMethod.PUT
        assert caller.last_request.form_body is not None
        assert dict(caller.last_request.form_body) == {"a": "1"}

        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.patch("/items/1", json_body={"b": 2})
        assert caller.last_request is not None
        assert caller.last_request.method is HttpMethod.PATCH

        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.delete("/items/1")
        assert caller.last_request is not None
        assert caller.last_request.method is HttpMethod.DELETE

        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.head("/items/1")
        assert caller.last_request is not None
        assert caller.last_request.method is HttpMethod.HEAD

        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.options("/items")
        assert caller.last_request is not None
        assert caller.last_request.method is HttpMethod.OPTIONS

    def test_get_query_params_simple_string(self) -> None:
        """GET avec une valeur simple par clé."""

        cfg = ServiceConfig(base_url="https://example.com")
        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.get("/search", query_params={"format": "json"})
        assert caller.last_request is not None
        assert dict(caller.last_request.query_params) == {"format": "json"}

    def test_get_query_params_repeated_via_sequence(self) -> None:
        """GET avec clé répétée via Sequence[str]."""

        cfg = ServiceConfig(base_url="https://example.com")
        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.get("/items", query_params={"tag": ["a", "b"]})
        assert caller.last_request is not None
        frozen = caller.last_request.query_params
        assert frozen["tag"] == ("a", "b")

    def test_post_query_params_mixed_simple_and_sequence(self) -> None:
        """POST avec mélange clé simple et séquence."""

        cfg = ServiceConfig(base_url="https://example.com")
        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.post(
            "/items",
            query_params={"q": "x", "tag": ("u", "v")},
            json_body={"name": "n"},
        )
        assert caller.last_request is not None
        qp = caller.last_request.query_params
        assert qp["q"] == "x"
        assert qp["tag"] == ("u", "v")
        assert caller.last_request.json_body == {"name": "n"}

    def test_delete_query_params_sequence(self) -> None:
        """DELETE sans body : query multi-valeurs."""

        cfg = ServiceConfig(base_url="https://example.com")
        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.delete("/items/1", query_params={"reason": ["a", "b"]})
        assert caller.last_request is not None
        assert caller.last_request.method is HttpMethod.DELETE
        assert caller.last_request.query_params["reason"] == ("a", "b")

    def test_head_query_params_simple(self) -> None:
        """HEAD sans body : valeur simple."""

        cfg = ServiceConfig(base_url="https://example.com")
        caller = RecordingCaller()
        service = BaobabServiceCaller(service_config=cfg, web_api_caller=caller)
        _ = service.head("/status", query_params={"verbose": "1"})
        assert caller.last_request is not None
        assert caller.last_request.method is HttpMethod.HEAD
        assert caller.last_request.query_params["verbose"] == "1"
