"""Tests de `JsonResponseDecoder`."""

from __future__ import annotations

import pytest

from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.json_response_decoder import JsonResponseDecoder
from baobab_web_api_caller.exceptions.response_decoding_exception import ResponseDecodingException


class TestJsonResponseDecoder:
    """Tests unitaires pour `JsonResponseDecoder`."""

    def test_decode_sets_json_data_when_content_type_is_json(self) -> None:
        """Décodage nominal."""

        resp = BaobabResponse(
            status_code=200,
            headers={"Content-Type": "application/json"},
            text='{"ok": true}',
            content=b'{"ok": true}',
        )
        out = JsonResponseDecoder().decode(resp)
        assert out.json_data == {"ok": True}

    def test_decode_ignores_non_json_content_type(self) -> None:
        """Ne touche pas aux réponses non JSON."""

        resp = BaobabResponse(status_code=200, headers={"Content-Type": "text/plain"}, text="hi")
        out = JsonResponseDecoder().decode(resp)
        assert out is resp

    def test_invalid_json_raises(self) -> None:
        """JSON invalide -> exception projet dédiée."""

        resp = BaobabResponse(
            status_code=200,
            headers={"Content-Type": "application/json"},
            text="{not json",
            content=b"{not json",
        )
        with pytest.raises(ResponseDecodingException):
            JsonResponseDecoder().decode(resp)
