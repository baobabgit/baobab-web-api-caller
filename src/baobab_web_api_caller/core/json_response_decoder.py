"""Décodage JSON des réponses."""

from __future__ import annotations

import json
from dataclasses import dataclass

from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.response_decoder import ResponseDecoder
from baobab_web_api_caller.exceptions.response_decoding_exception import ResponseDecodingException


@dataclass(frozen=True, slots=True)
class JsonResponseDecoder(ResponseDecoder):
    """Décode le JSON à partir du corps texte/binaire.

    Le décodage est tenté uniquement si l'en-tête ``Content-Type`` indique un JSON.
    """

    def decode(self, response: BaobabResponse) -> BaobabResponse:
        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type.lower():
            return response

        if response.text is not None:
            raw_text = response.text
        elif response.content is not None:
            try:
                raw_text = response.content.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ResponseDecodingException("Unable to decode JSON body as UTF-8") from exc
        else:
            raise ResponseDecodingException("Missing response body for JSON decoding")

        try:
            json_data: object = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise ResponseDecodingException("Invalid JSON response body") from exc

        return BaobabResponse(
            status_code=response.status_code,
            headers=response.headers,
            text=response.text,
            content=response.content,
            json_data=json_data,
        )
