"""Tests de `ResponseDecodingException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.baobab_web_api_caller_exception import (
    BaobabWebApiCallerException,
)
from baobab_web_api_caller.exceptions.response_decoding_exception import ResponseDecodingException


class TestResponseDecodingException:
    """Tests unitaires pour `ResponseDecodingException`."""

    def test_inheritance(self) -> None:
        """Vérifie l'héritage."""

        assert issubclass(ResponseDecodingException, BaobabWebApiCallerException)

    def test_instantiation(self) -> None:
        """Vérifie l'instanciation."""

        exc = ResponseDecodingException("decode")
        assert str(exc) == "decode"
