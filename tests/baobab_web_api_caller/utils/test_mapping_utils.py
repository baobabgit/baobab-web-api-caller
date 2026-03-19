"""Tests de `mapping_utils`."""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping, cast

import pytest

from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException
from baobab_web_api_caller.utils.mapping_utils import freeze_str_mapping


class TestFreezeStrMapping:
    """Tests unitaires pour la fonction `freeze_str_mapping`."""

    def test_freeze_str_mapping_returns_mapping_proxy(self) -> None:
        """Valide et fige un mapping str->str."""

        frozen = freeze_str_mapping({"a": "1", "b": "2"}, "test_map")
        assert isinstance(frozen, MappingProxyType)
        assert dict(frozen) == {"a": "1", "b": "2"}

    def test_freeze_str_mapping_rejects_non_mapping(self) -> None:
        """Un objet non-mapping est refusé."""

        with pytest.raises(ConfigurationException, match="must be a mapping"):
            freeze_str_mapping(cast(Mapping[str, str], "nope"), "fld")

    def test_freeze_str_mapping_rejects_invalid_keys(self) -> None:
        """Clés vides ou non-str refusées."""

        with pytest.raises(ConfigurationException, match="keys must be non-empty"):
            freeze_str_mapping({"": "x"}, "fld")
        with pytest.raises(ConfigurationException, match="keys must be non-empty"):
            freeze_str_mapping(cast(Mapping[str, str], {1: "x"}), "fld")

    def test_freeze_str_mapping_rejects_non_string_values(self) -> None:
        """Valeurs non-str refusées."""

        with pytest.raises(ConfigurationException, match="values must be strings"):
            freeze_str_mapping(cast(Mapping[str, str], {"a": 1}), "fld")
