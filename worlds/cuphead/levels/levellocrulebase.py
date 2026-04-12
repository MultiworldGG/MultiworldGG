from __future__ import annotations
from enum import IntEnum
from typing import NamedTuple
from ..names import LocationNames
from .leveldefs import levels_all
from .levelrules import LevelRule
from . import levelrules as lr

class LevelRuleModes(IntEnum):
    NONE = 0
    INHERIT = 1
    INHERIT_OR = 2

class LRule(NamedTuple):
    rule: LevelRule
    mode: LevelRuleModes | int = LevelRuleModes.NONE

class LevelLocRuleData:
    base_region: str
    base_rule: LevelRule | None
    loc_rules: dict[str, LevelRule]

    def _get_loc_rules(self, loc_rules: dict[str, LRule | None], debug: bool = False) -> dict[str, LevelRule]: # noqa: C901
        _loc_rules = loc_rules.copy()
        _event_locs: set[str] = set()
        nloc_rules: dict[str, LevelRule] = {}
        if levels_all[self.base_region]:
            for _loc in levels_all[self.base_region].locations:
                if _loc not in _loc_rules:
                    if _loc.startswith(LocationNames.loc_event_pfx):
                        _event_locs.add(_loc)
                        #print(f"Adding event location {_loc}...")
                    else:
                        _loc_rules[_loc] = LRule(self.base_rule) if self.base_rule else None
                        #print(f"Adding location rule {_loc}...")
        for _loc, lrule in _loc_rules.items():
            if lrule:
                _nrule = lrule.rule
                if self.base_rule:
                    if lrule.mode == LevelRuleModes.INHERIT:
                        _nrule = lr.lrule_and(_nrule, self.base_rule)
                        #print(f"Inheriting rule for {_loc}...")
                    elif lrule.mode == LevelRuleModes.INHERIT_OR:
                        _nrule = lr.lrule_or(_nrule, self.base_rule)
                        #print(f"Inheriting OR rule for {_loc}...")
                nloc_rules[_loc] = _nrule
            elif debug:
                print(f"No rule for {_loc}. Skipping.")
        for _eloc in _event_locs:
            _loc = _eloc.removeprefix(LocationNames.loc_event_pfx)
            if _loc in nloc_rules:
                nloc_rules[_eloc] = nloc_rules[_loc]
                #print(f"Adding event rule {_eloc}...")
        return nloc_rules

    def __init__(
            self,
            base_region: str,
            base_rule: LevelRule | None,
            loc_rules: dict[str, LRule | None],
            register_loc: bool = True,
            debug: bool = False
        ):
        self.base_region = base_region
        self.base_rule = base_rule
        self.loc_rules = self._get_loc_rules(loc_rules, debug)

        if register_loc:
            register_level_loc_rules(base_region, base_rule, loc_rules)

level_loc_rule_locs: set[str] = set()

def register_level_loc_rules(
        base_region: str,
        base_rule: lr.LevelRule | None,
        loc_rules: dict[str, LRule | None]
    ) -> LevelLocRuleData:
    res = LevelLocRuleData(base_region, base_rule, loc_rules, False)
    for loc in loc_rules.keys():
        level_loc_rule_locs.union(loc)
    return res
