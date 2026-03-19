"""Tests de `HttpException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.http_exception import HttpException


class TestHttpException:
    """Tests unitaires pour `HttpException`."""

    def test_instantiation_with_message_only(self) -> None:
        """message seul -> str(exception) == message."""

        exc = HttpException(status_code=400, message="http")
        assert str(exc) == "http"
        assert exc.status_code == 400
        assert exc.body_excerpt is None
        assert exc.headers is None

    def test_instantiation_includes_body_excerpt_and_headers(self) -> None:
        """Ajoute body_excerpt et headers dans la représentation."""

        exc = HttpException(
            status_code=400,
            message="http",
            body_excerpt="bad body",
            headers={"X-Request-Id": "abc"},
        )

        assert exc.status_code == 400
        assert exc.body_excerpt == "bad body"
        assert exc.headers == {"X-Request-Id": "abc"}

        rendered = str(exc)
        assert "http" in rendered
        assert "body=bad body" in rendered
        assert "headers=X-Request-Id=abc" in rendered
