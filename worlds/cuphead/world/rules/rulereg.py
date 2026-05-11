### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Any, NamedTuple

from typing_extensions import override

from BaseClasses import Entrance, Location
from rule_builder.rules import And, Has, Or, Rule

from . import rulebase as rb
from .rulepresetreg import RulePresetReg

if TYPE_CHECKING:
    from ... import CupheadWorld

class SpotType(IntEnum):
    LOCATION = 0
    ENTRANCE = 1

class Spot(NamedTuple):
    name: str
    type: SpotType

class RuleData(NamedTuple):
    rule: Rule["CupheadWorld"]
    combine_and: bool = True

@dataclass(init=False)
class RuleReg:
    _debug: bool = False
    _reg: dict[Spot, list[RuleData]]
    _preset_reg: RulePresetReg
    _world: "CupheadWorld"

    def __init__(self, world: "CupheadWorld"):
        self._debug = world.settings.is_debug_bit_on(256)
        self._reg = {}
        self._preset_reg = RulePresetReg()
        self._world = world

    @property
    def presets(self) -> RulePresetReg:
        return self._preset_reg

    def clear_all_rules(self):
        self._reg.clear()

    def contains(self, spot: str, spot_type: SpotType) -> bool:
        return Spot(spot, spot_type) in self._reg

    def get_rule(self, spot: str, spot_type: SpotType) -> list[RuleData]:
        return self._reg[Spot(spot, spot_type)]

    def _add_rule(self, spot: Spot, rule: Rule["CupheadWorld"], combine_and: bool, insert: bool = False):
        if spot not in self._reg:
            self._reg[spot] = [RuleData(rule)]
        elif insert:
            self._reg[spot][0] = RuleData(self._reg[spot][0].rule, combine_and)
            self._reg[spot].insert(0, RuleData(rule))
        else:
            self._reg[spot].append(RuleData(rule, combine_and))

    def add_rule(self, spot_name: str, spot_type: SpotType, rule: Rule["CupheadWorld"], combine_and: bool = True):
        spot = Spot(spot_name, spot_type)
        self._add_rule(spot, rule, combine_and)

    def insert_rule(self, spot_name: str, spot_type: SpotType, rule: Rule["CupheadWorld"], combine_and: bool = True):
        spot = Spot(spot_name, spot_type)
        self._add_rule(spot, rule, combine_and, True)

    def _pop_ruledata(self, spot: Spot) -> list[RuleData] | None:
        if spot not in self._reg:
            return None
        return self._reg.pop(spot)

    def pop_ruledata(self, spot_name: str, spot_type: SpotType) -> list[RuleData] | None:
        spot = Spot(spot_name, spot_type)
        return self._pop_ruledata(spot)

    def copy_rule(
        self,
        src_spot_name: str,
        src_spot_type: SpotType,
        dest_spot_name: str,
        dest_spot_type: SpotType,
        combine_and: bool = True
    ):
        sspot = Spot(src_spot_name, src_spot_type)
        if sspot not in self._reg:
            raise KeyError(f"{sspot} is not in the rulereg")
        dspot = Spot(dest_spot_name, dest_spot_type)
        rdefs = self._reg[sspot]
        empty_dest = dspot not in self._reg
        if empty_dest:
            self._reg[dspot] = []
        set_combine = not empty_dest
        for rdef in rdefs:
            self._reg[dspot].append(
                RuleData(rdef.rule, combine_and if set_combine else rdef.combine_and)
            )
            if set_combine:
                set_combine = False

    def add_item_rule(self, loc: str, item: str, count: int = 1, combine_and: bool = True):
        self.add_loc_rule(loc, Has(item, count), combine_and)
    def insert_item_rule(self, loc: str, item: str, count: int = 1, combine_and: bool = True):
        self.insert_loc_rule(loc, Has(item, count), combine_and)
    def add_loc_rule(self, loc: str, rule: Rule["CupheadWorld"], combine_and: bool = True):
        self.add_rule(loc, SpotType.LOCATION, rule, combine_and)
    def insert_loc_rule(self, loc: str, rule: Rule["CupheadWorld"], combine_and: bool = True):
        self.insert_rule(loc, SpotType.LOCATION, rule, combine_and)
    def add_region_rule(self, region_name: str, rule: Rule["CupheadWorld"], combine_and: bool = True):
        region = rb.get_region(self._world, region_name)
        for entrance in region.entrances:
            self.add_rule(entrance.name, SpotType.ENTRANCE, rule, combine_and)
    def insert_region_rule(self, region_name: str, rule: Rule["CupheadWorld"], combine_and: bool = True):
        region = rb.get_region(self._world, region_name)
        for entrance in region.entrances:
            self.insert_rule(entrance.name, SpotType.ENTRANCE, rule, combine_and)
    def add_region_exit_rule(self, region_name: str, rule: Rule["CupheadWorld"], combine_and: bool = True):
        region = rb.get_region(self._world, region_name)
        for entrance in region.exits:
            self.add_rule(entrance.name, SpotType.ENTRANCE, rule, combine_and)
    def insert_region_exit_rule(self, region_name: str, rule: Rule["CupheadWorld"], combine_and: bool = True):
        region = rb.get_region(self._world, region_name)
        for entrance in region.exits:
            self.insert_rule(entrance.name, SpotType.ENTRANCE, rule, combine_and)

    def pop_loc_ruledata(self, loc: str) -> list[RuleData] | None:
        return self.pop_ruledata(loc, SpotType.LOCATION)
    def pop_entrance_ruledata(self, entrance_name: str) -> list[RuleData] | None:
        return self.pop_ruledata(entrance_name, SpotType.ENTRANCE)

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(reg = {self._reg!s}, preset_reg = {self._preset_reg!s})"

    def _compile_rules(  # noqa: C901
        self,
        rule_output: bool = True,
        apply_rules: bool = False
    ) -> dict[Location | Entrance, Rule[Any]] | None:
        # This will iterate through the rules for each type and set the rule for
        # that spot (location or entrance) using self._world.set_rules(). It is done this way
        # because rule_builder Rules cannot be appended to exising world rules.
        # So this will stitch together all the rule_builder rules before setting them.
        if self._debug:
            print(f"rr size: {len(self._reg.keys())}")
        if rule_output:
            res: dict[Location | Entrance, Rule[Any]] | None = {}
        else:
            res = None
        for (spot_name, spot_type), rules in self._reg.items():
            if len(rules) < 1:
                print(f"rr: {spot_name} rules is empty")
                continue

            if spot_type == SpotType.ENTRANCE:
                spot = rb.get_entrance_by_name(self._world, spot_name)
            else:
                spot = rb.get_location(self._world, spot_name)

            if len(rules) == 1:
                if self._debug:
                    print(f"rr: '{spot}': `{rules[0].rule}`")
                self._world.set_rule(spot, rules[0].rule)
                continue

            _col: list[Rule[CupheadWorld]] = []
            _and = True
            for rule in rules:
                if rule.combine_and != _and:
                    _rule = And(*_col) if _and else Or(*_col)
                    _col = [_rule]
                    _and = rule.combine_and
                _col.append(rule.rule)

            _res = And(*_col) if _and else Or(*_col)
            if self._debug:
                print(f"rr: '{spot}': `{_res}`")
            if apply_rules:
                self._world.set_rule(spot, _res)
            if res is not None:
                res[spot] = _res

        return res

    def compile_rules(self) -> dict[Location | Entrance, Rule[Any]]:
        res = self._compile_rules(True, False)
        return res if res is not None else {}

    def apply_rules(self):
        return self._compile_rules(False, True)
