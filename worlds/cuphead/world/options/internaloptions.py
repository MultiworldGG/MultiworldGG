### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import Any, ClassVar, Self

from typing_extensions import override

from Options import FreeText, Option, Range, Visibility

from .protocols import NamedOption

## Internally set Option classes. These options are set internally by the APWorld
## and can never be set by the user. If set by the user, it will be overwritten
## internally.

class Version(FreeText, NamedOption):
    """
    Internal. Set during generation.
    The version of the APWorld
    """
    name = "version"
    display_name = "APWorld Version"
    visibility = Visibility.spoiler
    default = "MISSINGVER"


class CoinAmounts(Option[tuple[int, int, int]], NamedOption):
    """
    Internal. Set during generation.
    Amount of each type of coin
    """
    name = "coin_amounts"
    visibility = Visibility.none
    default = (0, 0, 0)

    def __init__(self, value: tuple[int, int, int]):
        self.value = value

    @classmethod
    @override
    def from_any(cls, data: Any) -> Self:
        values = tuple(int(x) for x in data)
        if len(values) != 3:
            raise ValueError(f"Option {cls.__name__} expects 3 values, got {len(values)}")
        return cls((values[0], values[1], values[2]))

    @classmethod
    @override
    def get_option_name(cls, value: tuple[int, int, int]):
        return f"({value[0]}, {value[1]}, {value[2]})"


class ContractRequirementsIsle2(Range, NamedOption):
    """
    Internal. Set during generation.
    Amount of contracts needed to access Inkwell Isle II
    """
    name = "contract_requirements_isle2"
    visibility = Visibility.none
    range_start = 0
    range_end = 5


class ContractRequirementsIsle3(Range, NamedOption):
    """
    Internal. Set during generation.
    Amount of contracts needed to access Inkwell Isle III
    """
    name = "contract_requirements_isle3"
    visibility = Visibility.none
    range_start = 0
    range_end = 10


class FillerItemWeights(Option[dict[str, int]], NamedOption):
    """
    Internal. Set during generation.
    The formatted result of all the item weights set in options
    """
    name = "filler_item_weights"
    visibility = Visibility.none
    default: ClassVar[dict[str, int]] = {}

    def __init__(self, value: dict[str, int]):
        self.value = value

    @classmethod
    @override
    def from_any(cls, data: Any) -> Self:
        return cls({str(k): int(v) for k, v in dict(data).items()})

    @classmethod
    @override
    def get_option_name(cls, value: dict[str, int]):
        return ", ".join(f"{key}: {v}" for key, v in value.items())


class ShopMap(Option[list[tuple[int, int]]], NamedOption):
    """
    Internal. Set during generation.
    The mapping of the item distribution in the shop
    """
    name = "shop_map"
    visibility = Visibility.none
    default: ClassVar[list[tuple[int, int]]] = []

    def __init__(self, value: list[tuple[int, int]]):
        self.value = value

    @classmethod
    @override
    def from_any(cls, data: Any) -> Self:
        value = [(int(x), int(y)) for x, y in data]
        return cls(value)

    @classmethod
    @override
    def get_option_name(cls, value: list[tuple[int, int]]):
        return ", ".join(f"({v1}, {v2})" for v1, v2 in value)

class TestOverrides(Option[dict[str, Any]], NamedOption):
    """
    Internal. Only used for unittests
    """
    name = "test_overrides"
    visibility = Visibility.none
    default: ClassVar[dict[str, Any]] = {}

    def __init__(self, value: dict[str, Any]):
        self.value = value

    @classmethod
    @override
    def from_any(cls, data: Any) -> Self:
        return cls({str(k): v for k, v in dict(data).items()})

    @classmethod
    @override
    def get_option_name(cls, value: dict[str, int]):
        return ", ".join(f"{key}: {v}" for key, v in value.items())

class TrapItemWeights(Option[dict[str, int]], NamedOption):
    """
    Internal. Set during generation.
    The formatted result of all the trap weights set in options
    """
    name = "trap_item_weights"
    visibility = Visibility.none
    default: ClassVar[dict[str, int]] = {}

    def __init__(self, value: dict[str, int]):
        self.value = value

    @classmethod
    @override
    def from_any(cls, data: Any) -> Self:
        return cls({str(k): int(v) for k, v in dict(data).items()})

    @classmethod
    @override
    def get_option_name(cls, value: dict[str, int]):
        return ", ".join(f"{key}: {v}" for key, v in value.items())
