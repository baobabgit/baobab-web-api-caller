"""Tests de `SystemTimeProvider`."""

from __future__ import annotations

from unittest.mock import patch

from baobab_web_api_caller.transport.system_time_provider import SystemTimeProvider


class TestSystemTimeProvider:
    """Tests unitaires pour `SystemTimeProvider`."""

    def test_monotonic_delegates_to_time_monotonic(self) -> None:
        """monotonic() doit renvoyer time.monotonic()."""

        provider = SystemTimeProvider()
        with patch(
            "baobab_web_api_caller.transport.system_time_provider.time.monotonic"
        ) as mock_mono:
            mock_mono.return_value = 123.0
            assert provider.monotonic() == 123.0
            mock_mono.assert_called_once()
