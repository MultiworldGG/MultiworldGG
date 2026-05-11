### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from rule_builder.rules import Rule

if TYPE_CHECKING:
    from .... import CupheadWorld

@dataclass(frozen=True, init=False)
class PresetData:
    rule: Rule["CupheadWorld"]
    name: str

    _used_preset_names: ClassVar[set[str]] = set()

    def __init__(self, rule: Rule["CupheadWorld"], name: str):
        if name in self.__class__._used_preset_names:
            raise ValueError(f"Preset name '{name}' already exists!")
        object.__setattr__(self, "rule", rule)
        object.__setattr__(self, "name", name)
        self.__class__._used_preset_names.add(name)
