"""Tests de `BaobabResponse`."""

from __future__ import annotations

from typing import Mapping, cast

import pytest

from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException


class TestBaobabResponse:
    """Tests unitaires pour `BaobabResponse`."""

    def test_minimal_response_is_created(self) -> None:
        """Vérifie la création minimale."""

        resp = BaobabResponse(status_code=200, headers={})
        assert resp.status_code == 200
        assert not dict(resp.headers)
        assert resp.text is None
        assert resp.content is None
        assert resp.json_data is None
        assert resp.is_success is True

    def test_status_code_validation(self) -> None:
        """Vérifie la validation du status code."""

        with pytest.raises(ConfigurationException):
            BaobabResponse(status_code=99, headers={})

        with pytest.raises(ConfigurationException):
            BaobabResponse(status_code=600, headers={})

        with pytest.raises(ConfigurationException):
            BaobabResponse(status_code="200", headers={})  # type: ignore[arg-type]

    def test_headers_validation(self) -> None:
        """Vérifie la validation des headers."""

        with pytest.raises(ConfigurationException):
            BaobabResponse(status_code=200, headers=cast(Mapping[str, str], {"X": 1}))

    def test_content_accepts_bytearray_and_normalizes_to_bytes(self) -> None:
        """Autorise bytearray et normalise en bytes."""

        resp = BaobabResponse(status_code=200, headers={}, content=bytearray(b"abc"))
        assert resp.content == b"abc"

    def test_is_success(self) -> None:
        """Vérifie la propriété is_success."""

        assert BaobabResponse(status_code=204, headers={}).is_success is True
        assert BaobabResponse(status_code=302, headers={}).is_success is False
        assert BaobabResponse(status_code=404, headers={}).is_success is False
