"""Tests de `SystemSleeper`."""

from __future__ import annotations

from unittest.mock import patch

from baobab_web_api_caller.transport.system_sleeper import SystemSleeper


class TestSystemSleeper:
    """Tests unitaires pour `SystemSleeper`."""

    def test_sleep_calls_time_sleep(self) -> None:
        """sleep() délègue à time.sleep."""

        sleeper = SystemSleeper()
        with patch("baobab_web_api_caller.transport.system_sleeper.time.sleep") as mock_sleep:
            sleeper.sleep(0.25)
            mock_sleep.assert_called_once_with(0.25)

