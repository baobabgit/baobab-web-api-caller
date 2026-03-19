"""Tests de `ResourceNotFoundException`."""

from __future__ import annotations

from baobab_web_api_caller.exceptions.client_http_exception import ClientHttpException
from baobab_web_api_caller.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)


class TestResourceNotFoundException:
    """Tests unitaires pour `ResourceNotFoundException`."""

    def test_inheritance(self) -> None:
        """ResourceNotFoundException doit hériter de ClientHttpException."""

        assert issubclass(ResourceNotFoundException, ClientHttpException)

    def test_instantiation_str_and_status_code(self) -> None:
        """status_code et message sont conservés."""

        exc = ResourceNotFoundException(status_code=404, message="404")
        assert str(exc) == "404"
        assert exc.status_code == 404
