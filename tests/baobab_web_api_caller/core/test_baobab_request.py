"""Tests de `BaobabRequest`."""

from __future__ import annotations

from typing import Mapping, cast

import pytest

from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestBaobabRequest:
    """Tests unitaires pour `BaobabRequest`."""

    def test_minimal_request_is_created_and_normalizes_path(self) -> None:
        """Vérifie la création minimale et la normalisation du path."""

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="v1/items",
            query_params={},
            headers={},
        )
        assert req.path == "/v1/items"
        assert req.method is HttpMethod.GET
        assert not dict(req.query_params)
        assert not dict(req.headers)

    def test_path_cannot_be_absolute_url(self) -> None:
        """Interdit un path de type URL absolue."""

        with pytest.raises(ConfigurationException):
            BaobabRequest(
                method=HttpMethod.GET,
                path="https://example.com/v1/items",
                query_params={},
                headers={},
            )

    def test_path_cannot_contain_spaces(self) -> None:
        """Interdit les espaces dans le path."""

        with pytest.raises(ConfigurationException):
            BaobabRequest(
                method=HttpMethod.GET,
                path="/v1/it ems",
                query_params={},
                headers={},
            )

    def test_timeout_must_be_positive_when_provided(self) -> None:
        """Vérifie la validation du timeout."""

        with pytest.raises(ConfigurationException):
            BaobabRequest(
                method=HttpMethod.GET,
                path="/v1/items",
                query_params={},
                headers={},
                timeout_seconds=0,
            )

    def test_json_and_form_bodies_are_mutually_exclusive(self) -> None:
        """Interdit de fournir json_body et form_body simultanément."""

        with pytest.raises(ConfigurationException):
            BaobabRequest(
                method=HttpMethod.POST,
                path="/v1/items",
                query_params={},
                headers={},
                json_body={"a": 1},
                form_body={"a": "1"},
            )

    def test_headers_must_be_string_mapping(self) -> None:
        """Vérifie la validation des headers (str->str)."""

        with pytest.raises(ConfigurationException):
            BaobabRequest(
                method=HttpMethod.GET,
                path="/v1/items",
                query_params={},
                headers=cast(Mapping[str, str], {"X": 1}),
            )

    def test_with_header_returns_new_request(self) -> None:
        """Vérifie l'API immuable `with_header`."""

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/v1/items",
            query_params={"q": "x"},
            headers={},
        )
        req2 = req.with_header("X-Test", "1")
        assert req2 is not req
        assert not dict(req.headers)
        assert dict(req2.headers) == {"X-Test": "1"}
