### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import TYPE_CHECKING

from rule_builder.rules import Rule, True_

from ...levels import levelids
from . import levelrulebase as lrb
from .levelruledefs import levelrules

if TYPE_CHECKING:
    from .... import CupheadWorld
    from ...options import CupheadOptions


class LevelRuleComp:
    _world: "CupheadWorld"
    _options: "CupheadOptions"

    def _debug_on(self) -> bool:
        return self._world.settings.is_debug_bit_on(128)

    def _compile_location_rule(
        self,
        level: lrb.LevelDef,
        loc: lrb.LocationDef,
    ) -> Rule["CupheadWorld"] | None:
        match loc.inherit:
            case lrb.InheritMode.NONE:
                return loc.rule
            case lrb.InheritMode.AND:
                if level.base is None:
                    return loc.rule
                if loc.rule is None:
                    return level.base
                return level.base & loc.rule
            case lrb.InheritMode.OR:
                if level.base is None or loc.rule is None:
                    return None
                return level.base | loc.rule

    def _compile_level_loc(
        self,
        rlname: str,
        mrlname: str,
        ldef: lrb.LevelDef,
        locname: str,
        loc: lrb.LocationDef,
    ):
        if locname in self._world.active_locations:
            _rule = self._compile_location_rule(ldef, loc)
            if _rule is None:
                _rule = True_()
            self._world.rulereg.add_loc_rule(locname, _rule)
            if locname == ldef.exit_location:
                self._world.rulereg.add_region_exit_rule(mrlname, _rule)
        else:
            if self._debug_on():
                print(f"Skipping rules for location '{locname}'")
            if locname == ldef.exit_location:
                raise ValueError(
                    f"level '{rlname}' exit_location '{ldef.exit_location}' is an inactive location."
                )

    def _get_rmapped_level_name(self, lname: str) -> str:
        if lname not in levelids.level_to_id:
            #print(f"WARNING: levelrulecomp: {lname} does not have an id. Not mapping.")
            return lname
        _rlevel_map = self._world.rlevel_map
        level_id = levelids.level_to_id[lname]
        if level_id not in _rlevel_map:
            #print(f"WARNING: levelrulecomp: {lname} is not mapped. Not mapping.")
            return lname
        return levelids.level_ids[_rlevel_map[level_id]]

    def compile_levelrules(self):
        active_levels = self._world.active_levels

        for lname, ldef in levelrules.levels.items():
            if self._debug_on():
                print(lname)

            if lname in active_levels:
                if ldef.exit_location and ldef.exit_location not in ldef.locations:
                    raise ValueError(f"'{lname}'.exit_location: '{ldef.exit_location}' is unknown.")

                _prule = ldef.physical_access
                if _prule is not None:
                    self._world.rulereg.insert_region_rule(lname, _prule)

                _rule = ldef.access
                rmlname = self._get_rmapped_level_name(lname)
                self._world.rulereg.add_region_rule(rmlname, _rule if _rule is not None else True_())

                for locname, loc in ldef.locations.items():
                    self._compile_level_loc(lname, rmlname, ldef, locname, loc)
            elif self._debug_on():
                print(f"Skipping rules for level '{lname}'")

    def __init__(self, world: "CupheadWorld"):
        self._world = world
        self._options = world.options
