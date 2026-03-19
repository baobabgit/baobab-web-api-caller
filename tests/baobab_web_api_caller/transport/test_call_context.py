"""Tests de `CallContext`."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest.mock import Mock

import pytest
import requests

from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.transport.call_context_builder import CallContext


class TestCallContext:
    """Tests unitaires pour le dataclass `CallContext`."""

    def test_fields_are_exposed(self) -> None:
        """Expose requête préparée, URL, timeout et session."""

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/p",
            query_params={},
            headers={},
        )
        session = Mock(spec=requests.Session)
        ctx = CallContext(
            prepared_request=req,
            url="https://example.com/p",
            timeout=2.5,
            session=session,
        )
        assert ctx.prepared_request is req
        assert ctx.url == "https://example.com/p"
        assert ctx.timeout == 2.5
        assert ctx.session is session

    def test_instance_is_frozen(self) -> None:
        """Le contexte est immuable (slots + frozen)."""

        req = BaobabRequest(
            method=HttpMethod.GET,
            path="/p",
            query_params={},
            headers={},
        )
        session = Mock(spec=requests.Session)
        ctx = CallContext(
            prepared_request=req,
            url="https://example.com/p",
            timeout=None,
            session=session,
        )
        with pytest.raises(FrozenInstanceError):
            ctx.url = "other"  # type: ignore[misc]
