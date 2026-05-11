### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from random import Random
from typing import TYPE_CHECKING

from ..auxiliary import scrub_list
from ..enums import GameMode
from ..locations.locationbase import LocationData
from ..names import regionnames
from ..options import CupheadOptions
from . import leveldefs as ldef
from . import levelids, levelshuffle
from .levelbase import LevelData

if TYPE_CHECKING:
    from ..settings import CupheadSettings

def _add_level(level_ref: dict[str, LevelData], lname: str, level_def: dict[str, LevelData]):
    if lname in level_ref:
        raise KeyError(f"Level '{lname}' already exists")
    level_ref[lname] = level_def[lname]

def setup_levels(
        settings: "CupheadSettings",
        options: CupheadOptions,
        active_locations: dict[str,LocationData]
    ) -> dict[str,LevelData]:
    use_dlc = options.use_dlc.bvalue
    levels: dict[str, LevelData] = {}

    _debug_scrub = settings.is_debug_bit_on(32)

    _add_level(levels, regionnames.level_tutorial, ldef.level_special)
    for lev, data in {**ldef.level_boss, **ldef.level_boss_final, **ldef.level_rungun}.items():
        if lev in levels:
            raise KeyError(f"Level '{lev}' already exists")
        levels[lev] = LevelData(
            data.world_location,
            scrub_list(data.locations, active_locations.keys(), _debug_scrub),
        )
    levels.update(ldef.level_mausoleum)

    if use_dlc:
        for lev,data in {**ldef.level_dlc_boss, **ldef.level_dlc_boss_final}.items():
            levels[lev] = LevelData(
                data.world_location,
                scrub_list(data.locations, active_locations.keys(), _debug_scrub),
            )
        levels.update(ldef.level_dlc_chesscastle_boss)
        if options.dlc_chalice.value > 0 and (options.mode.evalue & GameMode.DLC_NO_ISLE4) == 0:
            _add_level(levels, regionnames.level_dlc_tutorial, ldef.level_dlc_special)
        #_add_level(levels, regionnames.level_dlc_graveyard, ldef.level_dlc_special)

    return levels

def setup_level_map(options: CupheadOptions) -> dict[int,int]:
    rand = Random(options.level_shuffle_seed.value)
    level_map: dict[int,int] = {}

    level_map.update(
        levelshuffle.get_level_shuffle_map(
            rand,
            options.use_dlc.bvalue,
            options.level_shuffle.evalue,
            options.level_shuffle_kingdice.bvalue
        )
    )

    for k, v in options.level_placements.value.items():
        level_map[levelids.level_to_id[k]] = levelids.level_to_id[v]

    return level_map
