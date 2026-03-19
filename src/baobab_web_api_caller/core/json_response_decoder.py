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

    Le décodage est tenté uniquement si l'en-tête ``Content-Type`` indique un JSON
    (``application/json`` ou un type ``application/*+json``).
    """

    def decode(self, response: BaobabResponse) -> BaobabResponse:
        content_type = response.headers.get("Content-Type", "")
        if not self._is_json_content_type(content_type):
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
        if raw_text.strip() == "":
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

    @staticmethod
    def _is_json_content_type(content_type: str) -> bool:
        media_type = content_type.split(";", 1)[0].strip().lower()
        if media_type == "application/json":
            return True
        return media_type.startswith("application/") and media_type.endswith("+json")
