### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Iterable
from enum import IntEnum, IntFlag
from typing import Any, Generic, Self, TypeVar

from typing_extensions import override

from Options import Choice, NumericOption, Option, OptionDict, OptionError, Range, Toggle, Visibility

from . import _levelset

T = TypeVar("T")
TEnum = TypeVar("TEnum", bound=IntEnum)
TFlag = TypeVar("TFlag", bound=IntFlag)

class EnumOption(Generic[TEnum]):
    value: int
    enum_type: type[TEnum]

    @property
    def evalue(self) -> TEnum:
        """enum value"""
        return self.enum_type(self.value)

    @evalue.setter
    def evalue(self, value: TEnum | int):
        self.value = int(value)

class FlagOption(Generic[TFlag]):
    value: int
    flag_type: type[TFlag]

    @property
    def fvalue(self) -> TFlag:
        """flag value"""
        return self.flag_type(self.value)

    @fvalue.setter
    def fvalue(self, value: TFlag | int):
        self.value = int(value)

class BoolOption:
    value: int

    @property
    def bvalue(self) -> bool:
        """bool value"""
        return bool(self.value)

class BToggle(BoolOption, Toggle): ...

class BDefaultOnToggle(BToggle):
    default = 1

class ChoiceEx(Choice):
    random_value: int = -1

    @classmethod
    @override
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "random":
            cls.name_lookup[cls.random_value] = "RandomInt"
            return cls(cls.random_value)
        return super().from_text(text)

class ConstOption(Option[Any], Generic[T]):
    value: T
    default: Any = 0
    visibility = Visibility.none

    def __init__(self):
        self.value = getattr(self.__class__, "value", self.default)
        self.default = self.value

    @classmethod
    @override
    def from_any(cls, data: Any) -> Self:
        res = cls()
        cls.name_lookup[res.value] = str(res.value)
        return res

class ConstNumericOption(NumericOption):
    value: int
    default: int = 0
    visibility = Visibility.none

    def __init__(self):
        self.value = int(getattr(self.__class__, "value", self.default))
        self.default = self.value

    @classmethod
    @override
    def from_any(cls, data: Any) -> Self:
        res = cls()
        cls.name_lookup[res.value] = str(res.value)
        return res

class ConstToggle(ConstNumericOption):
    option_false = 0
    option_true = 1
    default: int = 0

    @classmethod
    @override
    def get_option_name(cls, value: int):
        return "Yes" if value != 0 else "No"

    __hash__ = Option.__hash__  # type: ignore

class LevelDict(OptionDict):
    valid_keys: Iterable[str] = frozenset(_levelset.levels)
    valid_values: Iterable[str] = valid_keys

    def __init__(self, value: dict[str, Any]):
        res: dict[str, str] = {}
        for x, y in value.items():
            if x in self.valid_keys and y in self.valid_values:
                res[x] = y
            else:
                raise OptionError(f"Option {self.__class__.__name__} contains invalid levels. '{x}: {y}' is invalid")
        super().__init__(res)

class LaxRange(Range):
    range_start = 0
    range_end = 10
    hard_min = 0
    hard_max = 100

    def __init__(self, value: int):
        if value < self.hard_min:
            raise OptionError(f"Option {self.__class__.__name__} cannot be less than {self.hard_min}!")
        if value > self.hard_max:
            raise OptionError(f"Option {self.__class__.__name__} cannot be greater than {self.hard_max}!")
        self.value = value
