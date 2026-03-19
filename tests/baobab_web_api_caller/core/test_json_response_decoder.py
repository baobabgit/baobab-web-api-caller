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

    def test_decode_accepts_application_problem_json(self) -> None:
        """Décode aussi les content-types JSON suffixés."""

        resp = BaobabResponse(
            status_code=400,
            headers={"Content-Type": "application/problem+json"},
            text='{"title": "bad request"}',
            content=b'{"title": "bad request"}',
        )

        out = JsonResponseDecoder().decode(resp)
        assert out.json_data == {"title": "bad request"}

    def test_decode_accepts_application_vnd_api_json_with_charset(self) -> None:
        """Décode les variantes JSON avec paramètres."""

        resp = BaobabResponse(
            status_code=200,
            headers={"Content-Type": "application/vnd.api+json; charset=utf-8"},
            text='{"data": []}',
            content=b'{"data": []}',
        )

        out = JsonResponseDecoder().decode(resp)
        assert out.json_data == {"data": []}

    def test_decode_accepts_application_hal_json(self) -> None:
        """Décode une variante JSON de type HAL."""

        resp = BaobabResponse(
            status_code=200,
            headers={"Content-Type": "application/hal+json"},
            text='{"_links": {"self": {"href": "/"}}}',
            content=b'{"_links": {"self": {"href": "/"}}}',
        )

        out = JsonResponseDecoder().decode(resp)
        assert out.json_data == {"_links": {"self": {"href": "/"}}}

    def test_decode_ignores_when_content_type_is_missing(self) -> None:
        """Sans Content-Type, la réponse est laissée intacte."""

        resp = BaobabResponse(status_code=200, headers={}, text='{"ok": true}')
        out = JsonResponseDecoder().decode(resp)
        assert out is resp

    def test_decode_raises_on_empty_json_body(self) -> None:
        """Body vide + type JSON -> exception explicite."""

        resp = BaobabResponse(
            status_code=200,
            headers={"Content-Type": "application/json"},
            text="  ",
            content=b"",
        )

        with pytest.raises(ResponseDecodingException, match="Missing response body"):
            JsonResponseDecoder().decode(resp)

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
