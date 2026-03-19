"""Tests de `ResponseDecoder`."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.response_decoder import ResponseDecoder


@dataclass(frozen=True, slots=True)
class FakeResponseDecoder(ResponseDecoder):
    """Implémentation concrète locale pour tester le contrat abstrait."""

    def decode(self, response: BaobabResponse) -> BaobabResponse:
        """Retourne la réponse inchangée."""

        return response


class TestResponseDecoder:
    """Tests unitaires pour `ResponseDecoder`."""

    def test_is_abstract(self) -> None:
        """La classe abstraite ne doit pas être instanciée."""

        with pytest.raises(TypeError):
            # pylint: disable=abstract-class-instantiated
            ResponseDecoder()  # type: ignore[abstract]  # pyright: ignore[reportGeneralTypeIssues]

    def test_decode_contract_returns_response(self) -> None:
        """Une implémentation concrète renvoie une BaobabResponse."""

        response = BaobabResponse(status_code=200, headers={}, text="ok", json_data=None)
        out = FakeResponseDecoder().decode(response)
        assert out == response
