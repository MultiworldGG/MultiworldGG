### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from rule_builder.rules import Rule

if TYPE_CHECKING:
    from .... import CupheadWorld

### Base level rule data classes

class InheritMode(IntEnum):
    NONE = 0
    AND = 1
    OR = 2


@dataclass(frozen=True)
class LocationDef:
    rule: Rule["CupheadWorld"] | None = None
    inherit: InheritMode = InheritMode.AND


@dataclass(frozen=True)
class LevelDef:
    locations: dict[str, LocationDef]
    exit_location: str
    access: Rule["CupheadWorld"] | None = None
    physical_access: Rule["CupheadWorld"] | None = None
    base: Rule["CupheadWorld"] | None = None

    def __init__(
        self,
        locations: dict[str, LocationDef],
        exit_location: str | None = None,
        access: Rule["CupheadWorld"] | None = None,
        physical_access: Rule["CupheadWorld"] | None = None,
        base: Rule["CupheadWorld"] | None = None,
    ):
        object.__setattr__(self, "locations", locations)
        object.__setattr__(self, "exit_location", exit_location if exit_location else "")
        object.__setattr__(self, "access", access)
        object.__setattr__(self, "physical_access", physical_access)
        object.__setattr__(self, "base", base)


@dataclass(frozen=True)
class LevelRules:
    levels: dict[str, LevelDef]
