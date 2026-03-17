"""Tests de `RequestsSessionFactory`."""

from __future__ import annotations

import requests

from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory


class TestRequestsSessionFactory:
    """Tests unitaires pour `RequestsSessionFactory`."""

    def test_create_returns_session(self) -> None:
        """Crée une session requests."""

        session = RequestsSessionFactory().create()
        assert isinstance(session, requests.Session)
