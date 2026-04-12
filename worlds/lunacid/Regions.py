from entrance_rando import EntranceType
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Protocol, Iterable

from BaseClasses import MultiWorld, Region, Entrance

from worlds.lunacid.strings.regions_entrances import LunacidRegion, LunacidEntrance, starting_location_to_region


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


@dataclass(frozen=True)
class RegionData:
    name: str
    exits: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class EntranceData:
    entrance_name: str
    region_exit: Optional[str] = None
    randomized: bool = False
    dead_end: bool = False
    type: EntranceType = EntranceType.ONE_WAY


lunacid_regions = [
    RegionData(LunacidRegion.menu, [LunacidEntrance.menu_to_start]),
    RegionData(LunacidRegion.starting_area, [LunacidEntrance.start_lobby_to_rest]),

    RegionData(LunacidRegion.hollow_basin, [LunacidEntrance.basin_to_surface, LunacidEntrance.basin_to_temple_path, LunacidEntrance.basin_to_archives_2f]),
    RegionData(LunacidRegion.temple_path, [LunacidEntrance.temple_path_to_basin, LunacidEntrance.temple_path_to_temple_front]),
    RegionData(LunacidRegion.temple_front,
               [LunacidEntrance.temple_front_to_temple_path, LunacidEntrance.temple_front_to_temple_back, LunacidEntrance.temple_front_to_temple_sewers,
                LunacidEntrance.temple_front_to_temple_front_secret, LunacidEntrance.temple_front_to_locked_spot]),
    RegionData(LunacidRegion.temple_locked),
    RegionData(LunacidRegion.temple_front_secret),
    RegionData(LunacidRegion.temple_sewers, [LunacidEntrance.temple_sewers_to_mire, LunacidEntrance.temple_sewers_to_sewers_secret]),
    RegionData(LunacidRegion.temple_sewers_secret),
    RegionData(LunacidRegion.temple_back, [LunacidEntrance.temple_back_to_temple_lower, LunacidEntrance.temple_back_to_temple_secret]),
    RegionData(LunacidRegion.temple_secret, [LunacidEntrance.temple_secret_to_temple_front]),
    RegionData(LunacidRegion.temple_lower, [LunacidEntrance.temple_lower_to_temple_back, LunacidEntrance.temple_lower_ladder, LunacidEntrance.temple_lower_to_forest]),

    RegionData(LunacidRegion.wings_rest, [LunacidEntrance.rest_to_sheryl, LunacidEntrance.rest_to_surface, LunacidEntrance.rest_to_start]),
    RegionData(LunacidRegion.sheryl),

    RegionData(LunacidRegion.forbidden_archives_2f,
               [LunacidEntrance.archives_2f_to_basin, LunacidEntrance.archives_2f_to_1f_back, LunacidEntrance.archives_2f_to_2f_secret]),
    RegionData(LunacidRegion.forbidden_archives_2f_secret),
    RegionData(LunacidRegion.forbidden_archives_1f_back, [LunacidEntrance.archives_1f_back_to_2f, LunacidEntrance.archives_2f_to_3f]),
    RegionData(LunacidRegion.forbidden_archives_3f, [LunacidEntrance.archives_3f_to_2f, LunacidEntrance.archives_3f_to_vampire, LunacidEntrance.archives_3f_to_1f_front,
                                                     LunacidEntrance.archives_3f_to_secret]),
    RegionData(LunacidRegion.forbidden_archives_1f_front, [LunacidEntrance.archives_1f_front_to_3f, LunacidEntrance.archives_1f_to_1f_secret,
                                                           LunacidEntrance.archives_1f_front_to_daedalus]),
    RegionData(LunacidRegion.forbidden_archives_3f_secret),
    RegionData(LunacidRegion.forbidden_archives_1f_front_secret),
    RegionData(LunacidRegion.daedalus),
    RegionData(LunacidRegion.forbidden_archives_vampire, [LunacidEntrance.archives_vampire_to_3f, LunacidEntrance.archives_vampire_to_chasm]),

    RegionData(LunacidRegion.laetus_chasm, [LunacidEntrance.chasm_to_archives_vampire, LunacidEntrance.chasm_to_chasm_upper]),
    RegionData(LunacidRegion.laetus_chasm_upper, [LunacidEntrance.chasm_upper_to_lower, LunacidEntrance.chasm_upper_to_surface, LunacidEntrance.chasm_upper_to_secret]),
    RegionData(LunacidRegion.laetus_chasm_secret),

    RegionData(LunacidRegion.great_well_surface, [LunacidEntrance.surface_to_chasm_upper, LunacidEntrance.surface_to_basin]),

    RegionData(LunacidRegion.fetid_mire, [LunacidEntrance.mire_to_temple_sewers, LunacidEntrance.mire_to_mire_lower_secrets, LunacidEntrance.mire_to_mire_upper_secret,
                                          LunacidEntrance.mire_to_sea]),
    RegionData(LunacidRegion.fetid_mire_lower_secrets),
    RegionData(LunacidRegion.fetid_mire_high_secrets),

    RegionData(LunacidRegion.yosei_forest, [LunacidEntrance.forest_to_lower_forest, LunacidEntrance.forest_to_temple_lower, LunacidEntrance.forest_to_canopy_path]),
    RegionData(LunacidRegion.yosei_lower, [LunacidEntrance.lower_forest_to_forest, LunacidEntrance.lower_forest_secret, LunacidEntrance.lower_forest_to_tomb,
                                           LunacidEntrance.lower_to_patchouli]),
    RegionData(LunacidRegion.yosei_lower_secret),
    RegionData(LunacidRegion.patchouli),
    RegionData(LunacidRegion.yosei_canopy_path, [LunacidEntrance.canopy_path_to_canopy, LunacidEntrance.canopy_path_to_forest]),
    RegionData(LunacidRegion.yosei_tomb, [LunacidEntrance.tomb_to_lower_forest, LunacidEntrance.forest_tomb_to_accursed_tomb]),

    RegionData(LunacidRegion.forest_canopy, [LunacidEntrance.canopy_to_canopy_path]),

    RegionData(LunacidRegion.sanguine_sea, [LunacidEntrance.sea_to_mire, LunacidEntrance.sea_to_castle_entrance, LunacidEntrance.sea_to_accursed_tomb]),

    RegionData(LunacidRegion.accursed_tomb, [LunacidEntrance.accursed_tomb_to_sea, LunacidEntrance.accursed_to_accursed_well, LunacidEntrance.accursed_to_vampire,
                                             LunacidEntrance.accursed_to_mausoleum, LunacidEntrance.accursed_tomb_to_platform, LunacidEntrance.accursed_tomb_to_secrets]),
    RegionData(LunacidRegion.accursed_tomb_platform),
    RegionData(LunacidRegion.mausoleum, [LunacidEntrance.mausoleum_to_secret]),
    RegionData(LunacidRegion.mausoleum_secret),
    RegionData(LunacidRegion.vampire_tomb, [LunacidEntrance.vampire_tomb_to_secret]),
    RegionData(LunacidRegion.vampire_tomb_tape_room),
    RegionData(LunacidRegion.accursed_tomb_secrets),
    RegionData(LunacidRegion.accursed_well, [LunacidEntrance.accursed_well_to_accursed, LunacidEntrance.accursed_tomb_to_forest_tomb]),

    RegionData(LunacidRegion.castle_le_fanu_entrance, [LunacidEntrance.castle_entrance_to_sea, LunacidEntrance.castle_entrance_to_battlefield,
                                                       LunacidEntrance.castle_entrance_to_main_halls, LunacidEntrance.castle_to_cattle,
                                                       LunacidEntrance.rock_castle_le_fanu_secret_skips, LunacidEntrance.rock_castle_le_fanu_spell_skip,
                                                       LunacidEntrance.rock_castle_le_fanu_past_door, LunacidEntrance.rock_castle_le_fanu_queen_door,
                                                       LunacidEntrance.rock_castle_le_fanu_upper_bridge, LunacidEntrance.rock_castle_le_fanu_cattle_deeper_skip]),
    RegionData(LunacidRegion.castle_le_fanu_cattle_prison, [LunacidEntrance.cattle_to_castle, LunacidEntrance.cattle_to_deeper]),
    RegionData(LunacidRegion.castle_le_fanu_cattle_prison_deep, [LunacidEntrance.cattle_to_secret]),
    RegionData(LunacidRegion.castle_le_fanu_cattle_prison_secret),
    RegionData(LunacidRegion.castle_le_fanu_main_halls, [LunacidEntrance.castle_main_halls_to_entrance, LunacidEntrance.castle_main_halls_to_upstairs,
                                                         LunacidEntrance.castle_main_halls_to_queen_path]),
    RegionData(LunacidRegion.castle_le_fanu_upstairs_area, [LunacidEntrance.castle_upstairs_to_main_halls, LunacidEntrance.castle_upstairs_to_forbidden,
                                                            LunacidEntrance.castle_upstairs_to_cattle_back, LunacidEntrance.castle_upstairs_to_queen_rest,
                                                            LunacidEntrance.castle_upstairs_to_tape_room]),
    RegionData(LunacidRegion.castle_le_fanu_upstairs_tape_room),
    RegionData(LunacidRegion.castle_le_fanu_upstairs_queens_rest),
    RegionData(LunacidRegion.castle_le_fanu_upstairs_forbidden_entry,
               [LunacidEntrance.castle_forbidden_to_upstairs, LunacidEntrance.castle_forbidden_to_sealed_ballroom]),
    RegionData(LunacidRegion.castle_le_fanu_cattle_prison_back, [LunacidEntrance.castle_cattle_back_to_cattle_prison, LunacidEntrance.castle_cattle_back_to_upstairs,
                                                                 LunacidEntrance.castle_cattle_back_to_boiling_grotto, LunacidEntrance.castle_cattle_back_to_main_halls]),
    RegionData(LunacidRegion.castle_le_fanu_throne_path, [LunacidEntrance.castle_queen_path_to_throne_room, LunacidEntrance.castle_queen_path_to_main_halls]),

    RegionData(LunacidRegion.holy_battleground, [LunacidEntrance.holy_battle_to_castle_entrance]),

    RegionData(LunacidRegion.sealed_ballroom, [LunacidEntrance.sealed_ballroom_to_rooms, LunacidEntrance.sealed_ballroom_to_secrets,
                                               LunacidEntrance.sealed_ballroom_to_forbidden_entry]),
    RegionData(LunacidRegion.sealed_ballroom_rooms, [LunacidEntrance.sealed_ballroom_rooms_to_cave]),
    RegionData(LunacidRegion.sealed_ballroom_cave_within_room),
    RegionData(LunacidRegion.sealed_ballroom_secret_walls, [LunacidEntrance.sealed_ballroom_secret_room]),
    RegionData(LunacidRegion.sealed_ballroom_room_within_secret),

    RegionData(LunacidRegion.boiling_grotto, [LunacidEntrance.boiling_grotto_to_castle_cattle_back, LunacidEntrance.boiling_grotto_to_secret,
                                              LunacidEntrance.boiling_grotto_to_coffin_room, LunacidEntrance.boiling_grotto_to_sand_temple]),
    RegionData(LunacidRegion.boiling_grotto_coffin_chamber,
               [LunacidEntrance.boiling_grotto_coffin_room_to_boiling_grotto, LunacidEntrance.boiling_grotto_coffin_room_to_tower]),
    RegionData(LunacidRegion.boiling_grotto_secret),

    RegionData(LunacidRegion.sand_temple, [LunacidEntrance.sand_temple_to_deep_snake_pit, LunacidEntrance.sand_temple_to_secret_snake_pit]),
    RegionData(LunacidRegion.secret_snake_pit, [LunacidEntrance.sand_temple_secret_snake_pit_escape]),
    RegionData(LunacidRegion.deep_snake_pit),

    RegionData(LunacidRegion.tower_of_abyss, [LunacidEntrance.abyss_to_5f]),
    RegionData(LunacidRegion.tower_of_abyss_5f, [LunacidEntrance.abyss_5f_to_10f]),
    RegionData(LunacidRegion.tower_of_abyss_10f, [LunacidEntrance.abyss_10f_to_15f]),
    RegionData(LunacidRegion.tower_of_abyss_15f, [LunacidEntrance.abyss_15f_to_20f]),
    RegionData(LunacidRegion.tower_of_abyss_20f, [LunacidEntrance.abyss_20f_to_25f]),
    RegionData(LunacidRegion.tower_of_abyss_25f, [LunacidEntrance.abyss_25f_to_30f]),
    RegionData(LunacidRegion.tower_of_abyss_30f, [LunacidEntrance.abyss_30f_to_35f]),
    RegionData(LunacidRegion.tower_of_abyss_35f, [LunacidEntrance.abyss_35f_to_40f]),
    RegionData(LunacidRegion.tower_of_abyss_40f, [LunacidEntrance.abyss_40f_to_45f]),
    RegionData(LunacidRegion.tower_of_abyss_45f, [LunacidEntrance.abyss_45f_to_50f]),
    RegionData(LunacidRegion.tower_of_abyss_50f, [LunacidEntrance.abyss_50f_to_final]),
    RegionData(LunacidRegion.tower_of_abyss_finish),

    RegionData(LunacidRegion.throne_chamber_front_path, [LunacidEntrance.throne_room_to_castle_queen_path, LunacidEntrance.throne_from_front_to_main]),
    RegionData(LunacidRegion.throne_chamber, [LunacidEntrance.throne_from_main_to_back, LunacidEntrance.throne_from_main_to_front]),
    RegionData(LunacidRegion.throne_chamber_back_path, [LunacidEntrance.throne_room_to_prison, LunacidEntrance.throne_from_back_to_main]),

    RegionData(LunacidRegion.terminus_prison_1f, [LunacidEntrance.terminus_prison_1f_to_2f, LunacidEntrance.terminus_prison_1f_to_3f,
                                                  LunacidEntrance.terminus_prison_1f_to_basement, LunacidEntrance.terminus_prison_1f_to_arena,
                                                  LunacidEntrance.terminus_prison_1f_to_secrets]),
    RegionData(LunacidRegion.terminus_prison_2f, [LunacidEntrance.terminus_prison_2f_to_1f, LunacidEntrance.terminus_prison_2f_to_3f,
                                                  LunacidEntrance.terminus_prison_2f_doors]),
    RegionData(LunacidRegion.terminus_prison_3f, [LunacidEntrance.terminus_prison_3f_to_2f, LunacidEntrance.terminus_prison_3f_to_4f,
                                                  LunacidEntrance.terminus_prison_3f_doors, LunacidEntrance.terminus_prison_3f_to_throne_room]),
    RegionData(LunacidRegion.terminus_prison_4f, [LunacidEntrance.terminus_prison_4f_secret_walls]),
    RegionData(LunacidRegion.terminus_prison_basement, [LunacidEntrance.terminus_prison_basement_to_ash, LunacidEntrance.terminus_prison_basement_to_1f]),
    RegionData(LunacidRegion.terminus_prison_1f_secrets),
    RegionData(LunacidRegion.terminus_prison_2f_rooms),
    RegionData(LunacidRegion.terminus_prison_3f_rooms),
    RegionData(LunacidRegion.terminus_prison_4f_secrets),

    RegionData(LunacidRegion.labyrinth_of_ash, [LunacidEntrance.labyrinth_of_ash_to_terminus_prison, LunacidEntrance.labyrinth_of_ash_to_interior,
                                                LunacidEntrance.labyrinth_of_ash_to_holy_seat]),
    RegionData(LunacidRegion.labyrinth_interior, [LunacidEntrance.labyrinth_interior_to_secret]),
    RegionData(LunacidRegion.labyrinth_secret),
    RegionData(LunacidRegion.holy_seat_of_gold, [LunacidEntrance.holy_seat_to_secret]),
    RegionData(LunacidRegion.holy_seat_of_secret),

    RegionData(LunacidRegion.forlorn_arena, [LunacidEntrance.forlorn_arena_to_path_to_sucsarius, LunacidEntrance.forlorn_arena_to_temple_of_earth,
                                             LunacidEntrance.forlorn_arena_to_water_temple, LunacidEntrance.forlorn_arena_to_terminus_prison]),
    RegionData(LunacidRegion.temple_of_earth, [LunacidEntrance.temple_of_earth_to_secrets]),
    RegionData(LunacidRegion.temple_of_earth_secret),
    RegionData(LunacidRegion.temple_of_water, [LunacidEntrance.temple_of_water_to_lower]),
    RegionData(LunacidRegion.temple_of_water_lower, [LunacidEntrance.temple_of_water_lower_to_secrets]),
    RegionData(LunacidRegion.temple_of_water_lower_secrets),
    RegionData(LunacidRegion.forlorn_path_to_sucsarius, [LunacidEntrance.forlorn_path_to_chamber]),

    RegionData(LunacidRegion.chamber_of_fate, [LunacidEntrance.chamber_to_forlorn_path, LunacidEntrance.chamber_to_grave]),

    RegionData(LunacidRegion.grave_of_the_sleeper, [LunacidEntrance.grave_to_chamber]),

]

lunacid_entrances = [
    # Menu moving to the main starting spot.  Hollow Basin is not guaranteed.
    EntranceData(LunacidEntrance.menu_to_start, LunacidRegion.starting_area),
    EntranceData(LunacidEntrance.start_lobby_to_rest, LunacidRegion.wings_rest),

    # Main basin area
    EntranceData(LunacidEntrance.basin_to_surface, LunacidRegion.great_well_surface, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.basin_to_temple_path, LunacidRegion.temple_path),
    EntranceData(LunacidEntrance.basin_to_archives_2f, LunacidRegion.forbidden_archives_2f, True, type=EntranceType.TWO_WAY),

    # Path to temple of silence
    EntranceData(LunacidEntrance.temple_path_to_basin, LunacidRegion.hollow_basin),
    EntranceData(LunacidEntrance.temple_path_to_temple_front, LunacidRegion.temple_front),

    # temple entrance
    EntranceData(LunacidEntrance.temple_front_to_temple_path, LunacidRegion.temple_path),
    EntranceData(LunacidEntrance.temple_front_to_temple_back, LunacidRegion.temple_back),
    EntranceData(LunacidEntrance.temple_front_to_temple_sewers, LunacidRegion.temple_sewers),
    EntranceData(LunacidEntrance.temple_front_to_temple_front_secret, LunacidRegion.temple_front_secret),
    EntranceData(LunacidEntrance.temple_front_to_locked_spot, LunacidRegion.temple_locked),

    # temple sewers
    EntranceData(LunacidEntrance.temple_sewers_to_sewers_secret, LunacidRegion.temple_sewers_secret),
    EntranceData(LunacidEntrance.temple_sewers_to_mire, LunacidRegion.fetid_mire, True, type=EntranceType.TWO_WAY),

    # temple backend
    EntranceData(LunacidEntrance.temple_back_to_temple_lower, LunacidRegion.temple_lower),
    EntranceData(LunacidEntrance.temple_back_to_temple_secret, LunacidRegion.temple_secret),

    # temple secret.  This is a one-way since one can theoretically always return to menu, and thus wherever you came from to get to secret.
    EntranceData(LunacidEntrance.temple_secret_to_temple_front, LunacidRegion.temple_front),

    # temple lower.  The ladder is one way since it'd require to reach lower anyway.
    EntranceData(LunacidEntrance.temple_lower_to_temple_back, LunacidRegion.temple_back),
    EntranceData(LunacidEntrance.temple_lower_ladder, LunacidRegion.hollow_basin),
    EntranceData(LunacidEntrance.temple_lower_to_forest, LunacidRegion.yosei_forest, True, type=EntranceType.TWO_WAY),

    # wings rest
    EntranceData(LunacidEntrance.rest_to_sheryl, LunacidRegion.sheryl),
    EntranceData(LunacidEntrance.rest_to_surface, LunacidRegion.great_well_surface),
    EntranceData(LunacidEntrance.rest_to_start),  # The ending region will be picked before entrances are randomized and placed then.

    # Forbidden Archives 2f
    EntranceData(LunacidEntrance.archives_2f_to_basin, LunacidRegion.hollow_basin, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.archives_2f_to_1f_back, LunacidRegion.forbidden_archives_1f_back),
    EntranceData(LunacidEntrance.archives_2f_to_2f_secret, LunacidRegion.forbidden_archives_2f_secret),

    # Forbidden Archives 1f.  Note that the 2f to 3f entrance to save me some general anguish.
    EntranceData(LunacidEntrance.archives_1f_back_to_2f, LunacidRegion.forbidden_archives_2f),
    EntranceData(LunacidEntrance.archives_2f_to_3f, LunacidRegion.forbidden_archives_3f),
    EntranceData(LunacidEntrance.archives_1f_front_to_3f, LunacidRegion.forbidden_archives_3f),
    EntranceData(LunacidEntrance.archives_1f_to_1f_secret, LunacidRegion.forbidden_archives_1f_front_secret),
    EntranceData(LunacidEntrance.archives_1f_front_to_daedalus, LunacidRegion.daedalus),

    # forbidden archives 3f
    EntranceData(LunacidEntrance.archives_3f_to_1f_front, LunacidRegion.forbidden_archives_1f_front),
    EntranceData(LunacidEntrance.archives_3f_to_2f, LunacidRegion.forbidden_archives_1f_back),
    EntranceData(LunacidEntrance.archives_3f_to_secret, LunacidRegion.forbidden_archives_3f_secret),
    EntranceData(LunacidEntrance.archives_3f_to_vampire, LunacidRegion.forbidden_archives_vampire),

    # forbidden archives vampire.  Its just the tiny hallway between the main area and chasm.
    EntranceData(LunacidEntrance.archives_vampire_to_3f, LunacidRegion.forbidden_archives_3f),
    EntranceData(LunacidEntrance.archives_vampire_to_chasm, LunacidRegion.laetus_chasm, True, type=EntranceType.TWO_WAY),

    # laetus chasm.  Split up this region since going backwards requires a nasty jump.
    EntranceData(LunacidEntrance.chasm_to_archives_vampire, LunacidRegion.forbidden_archives_vampire, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.chasm_to_chasm_upper, LunacidRegion.laetus_chasm_upper),
    EntranceData(LunacidEntrance.chasm_upper_to_secret, LunacidRegion.laetus_chasm_secret),
    EntranceData(LunacidEntrance.chasm_upper_to_lower, LunacidRegion.laetus_chasm),
    EntranceData(LunacidEntrance.chasm_upper_to_surface, LunacidRegion.great_well_surface, True, type=EntranceType.TWO_WAY),

    # great well surface
    EntranceData(LunacidEntrance.surface_to_basin, LunacidRegion.hollow_basin, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.surface_to_chasm_upper, LunacidRegion.hollow_basin, True, type=EntranceType.TWO_WAY),

    # the fetid mire
    EntranceData(LunacidEntrance.mire_to_temple_sewers, LunacidRegion.temple_sewers, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.mire_to_mire_upper_secret, LunacidRegion.fetid_mire_high_secrets),
    EntranceData(LunacidEntrance.mire_to_mire_lower_secrets, LunacidRegion.fetid_mire_lower_secrets),
    EntranceData(LunacidEntrance.mire_to_sea, LunacidRegion.sanguine_sea, True, type=EntranceType.TWO_WAY),

    # yosei forest main
    EntranceData(LunacidEntrance.forest_to_temple_lower, LunacidRegion.temple_lower, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.forest_to_canopy_path, LunacidRegion.yosei_canopy_path),
    EntranceData(LunacidEntrance.forest_to_lower_forest, LunacidRegion.yosei_lower),

    # yosei lower
    EntranceData(LunacidEntrance.lower_forest_to_forest, LunacidRegion.yosei_forest),
    EntranceData(LunacidEntrance.lower_forest_secret, LunacidRegion.yosei_lower_secret),
    EntranceData(LunacidEntrance.lower_forest_to_tomb, LunacidRegion.yosei_tomb),
    EntranceData(LunacidEntrance.lower_to_patchouli, LunacidRegion.patchouli),

    # this is just the path between the enchanted door and the actual door
    EntranceData(LunacidEntrance.canopy_path_to_forest, LunacidRegion.yosei_forest),
    EntranceData(LunacidEntrance.canopy_path_to_canopy, LunacidRegion.forest_canopy, True, type=EntranceType.TWO_WAY),

    # the drop down area that gets you into accursed tomb.  We need a rule for jumping out if you walk out this way.
    EntranceData(LunacidEntrance.tomb_to_lower_forest, LunacidRegion.yosei_lower),
    EntranceData(LunacidEntrance.forest_tomb_to_accursed_tomb, LunacidRegion.accursed_tomb, True, type=EntranceType.TWO_WAY),

    # the entirety of forest canopy.  Shrimple.
    EntranceData(LunacidEntrance.canopy_to_canopy_path, LunacidRegion.yosei_canopy_path, True, type=EntranceType.TWO_WAY),

    # sanguine sea
    EntranceData(LunacidEntrance.sea_to_mire, LunacidRegion.fetid_mire, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.sea_to_castle_entrance, LunacidRegion.castle_le_fanu_entrance, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.sea_to_accursed_tomb, LunacidRegion.accursed_tomb, True, type=EntranceType.TWO_WAY),

    # accursed tomb
    EntranceData(LunacidEntrance.accursed_tomb_to_sea, LunacidRegion.sanguine_sea, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.accursed_to_vampire, LunacidRegion.vampire_tomb),
    EntranceData(LunacidEntrance.accursed_to_mausoleum, LunacidRegion.mausoleum),
    EntranceData(LunacidEntrance.accursed_tomb_to_secrets, LunacidRegion.accursed_tomb_secrets),
    EntranceData(LunacidEntrance.vampire_tomb_to_secret, LunacidRegion.vampire_tomb_tape_room),
    EntranceData(LunacidEntrance.accursed_to_accursed_well, LunacidRegion.accursed_well),
    EntranceData(LunacidEntrance.accursed_tomb_to_platform, LunacidRegion.accursed_tomb_platform),
    EntranceData(LunacidEntrance.mausoleum_to_secret, LunacidRegion.mausoleum_secret),

    # accursed well; its the top part of accursed tomb where you drop down a well.
    EntranceData(LunacidEntrance.accursed_well_to_accursed, LunacidRegion.accursed_tomb),
    EntranceData(LunacidEntrance.accursed_tomb_to_forest_tomb, LunacidRegion.yosei_tomb, True, type=EntranceType.TWO_WAY),

    # castle le fanu entrance
    EntranceData(LunacidEntrance.castle_entrance_to_sea, LunacidRegion.sanguine_sea, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.castle_entrance_to_battlefield, LunacidRegion.holy_battleground, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.castle_to_cattle, LunacidRegion.castle_le_fanu_cattle_prison),
    EntranceData(LunacidEntrance.castle_entrance_to_main_halls, LunacidRegion.castle_le_fanu_main_halls),
    EntranceData(LunacidEntrance.rock_castle_le_fanu_secret_skips, LunacidRegion.castle_le_fanu_cattle_prison_secret),
    EntranceData(LunacidEntrance.rock_castle_le_fanu_past_door, LunacidRegion.castle_le_fanu_throne_path),
    EntranceData(LunacidEntrance.rock_castle_le_fanu_spell_skip, LunacidRegion.castle_le_fanu_upstairs_forbidden_entry),
    EntranceData(LunacidEntrance.rock_castle_le_fanu_upper_bridge, LunacidRegion.castle_le_fanu_upstairs_area),
    EntranceData(LunacidEntrance.rock_castle_le_fanu_queen_door, LunacidRegion.castle_le_fanu_upstairs_queens_rest),
    EntranceData(LunacidEntrance.rock_castle_le_fanu_cattle_deeper_skip, LunacidRegion.castle_le_fanu_cattle_prison_back),

    # castle le fanu cattle prison.  We split off the deeper area since it also requires a symbol possibly.
    EntranceData(LunacidEntrance.cattle_to_castle, LunacidRegion.castle_le_fanu_entrance),
    EntranceData(LunacidEntrance.cattle_to_deeper, LunacidRegion.castle_le_fanu_cattle_prison_deep),
    EntranceData(LunacidEntrance.cattle_to_secret, LunacidRegion.castle_le_fanu_cattle_prison_secret),

    # castle le fanu main halls
    EntranceData(LunacidEntrance.castle_main_halls_to_entrance, LunacidRegion.castle_le_fanu_entrance),
    EntranceData(LunacidEntrance.castle_main_halls_to_upstairs, LunacidRegion.castle_le_fanu_upstairs_area),
    EntranceData(LunacidEntrance.castle_main_halls_to_queen_path, LunacidRegion.castle_le_fanu_throne_path),

    # castle le fanu upstairs area
    EntranceData(LunacidEntrance.castle_upstairs_to_main_halls, LunacidRegion.castle_le_fanu_main_halls),
    EntranceData(LunacidEntrance.castle_upstairs_to_forbidden, LunacidRegion.castle_le_fanu_upstairs_forbidden_entry),
    EntranceData(LunacidEntrance.castle_upstairs_to_queen_rest, LunacidRegion.castle_le_fanu_upstairs_queens_rest),
    EntranceData(LunacidEntrance.castle_upstairs_to_cattle_back, LunacidRegion.castle_le_fanu_cattle_prison_back),
    EntranceData(LunacidEntrance.castle_upstairs_to_tape_room, LunacidRegion.castle_le_fanu_upstairs_tape_room),

    # castle le fanu forbidden entry.  This is the very tiny spot between the wall you open with magic hitting the window and ballroom.
    EntranceData(LunacidEntrance.castle_forbidden_to_upstairs, LunacidRegion.castle_le_fanu_upstairs_area),
    EntranceData(LunacidEntrance.castle_forbidden_to_sealed_ballroom, LunacidRegion.sealed_ballroom, True, type=EntranceType.TWO_WAY),

    # castle le fanu cattle back.  The back area where the final symbol is.
    EntranceData(LunacidEntrance.castle_cattle_back_to_main_halls, LunacidRegion.castle_le_fanu_main_halls),
    EntranceData(LunacidEntrance.castle_cattle_back_to_upstairs, LunacidRegion.castle_le_fanu_upstairs_area),
    EntranceData(LunacidEntrance.castle_cattle_back_to_cattle_prison, LunacidRegion.castle_le_fanu_cattle_prison),
    EntranceData(LunacidEntrance.castle_cattle_back_to_boiling_grotto, LunacidRegion.boiling_grotto, True, type=EntranceType.TWO_WAY),

    # castle le fanu throne path.  This is the long hallway between the green door and the door to throne chamber.
    EntranceData(LunacidEntrance.castle_queen_path_to_throne_room, LunacidRegion.throne_chamber_front_path, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.castle_queen_path_to_main_halls, LunacidRegion.castle_le_fanu_main_halls),

    # holy battlefield
    EntranceData(LunacidEntrance.holy_battle_to_castle_entrance, LunacidRegion.castle_le_fanu_entrance, True, type=EntranceType.TWO_WAY),

    # sealed ballroom.  Includes the secrets and rooms together since its small enough.
    EntranceData(LunacidEntrance.sealed_ballroom_to_forbidden_entry, LunacidRegion.castle_le_fanu_upstairs_forbidden_entry, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.sealed_ballroom_to_rooms, LunacidRegion.sealed_ballroom_rooms),
    EntranceData(LunacidEntrance.sealed_ballroom_to_secrets, LunacidRegion.sealed_ballroom_secret_walls),
    EntranceData(LunacidEntrance.sealed_ballroom_secret_room, LunacidRegion.sealed_ballroom_room_within_secret),
    EntranceData(LunacidEntrance.sealed_ballroom_rooms_to_cave, LunacidRegion.sealed_ballroom_cave_within_room),

    # boiling grotto
    EntranceData(LunacidEntrance.boiling_grotto_to_castle_cattle_back, LunacidRegion.castle_le_fanu_cattle_prison_back, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.boiling_grotto_to_secret, LunacidRegion.boiling_grotto_secret),
    EntranceData(LunacidEntrance.boiling_grotto_to_coffin_room, LunacidRegion.boiling_grotto_coffin_chamber),
    EntranceData(LunacidEntrance.boiling_grotto_to_sand_temple, LunacidRegion.sand_temple),

    # boiling grotto coffin chamber.  Its the secret wall room where you get in the coffin.  A one way.
    EntranceData(LunacidEntrance.boiling_grotto_coffin_room_to_tower, LunacidRegion.tower_of_abyss),
    EntranceData(LunacidEntrance.boiling_grotto_coffin_room_to_boiling_grotto, LunacidRegion.boiling_grotto),

    # sand temple
    EntranceData(LunacidEntrance.sand_temple_to_secret_snake_pit, LunacidRegion.secret_snake_pit),
    EntranceData(LunacidEntrance.sand_temple_to_deep_snake_pit, LunacidRegion.deep_snake_pit),
    EntranceData(LunacidEntrance.sand_temple_secret_snake_pit_escape, LunacidRegion.sand_temple),

    # tower of abyss
    EntranceData(LunacidEntrance.abyss_to_5f, LunacidRegion.tower_of_abyss_5f),
    EntranceData(LunacidEntrance.abyss_5f_to_10f, LunacidRegion.tower_of_abyss_10f),
    EntranceData(LunacidEntrance.abyss_10f_to_15f, LunacidRegion.tower_of_abyss_15f),
    EntranceData(LunacidEntrance.abyss_15f_to_20f, LunacidRegion.tower_of_abyss_20f),
    EntranceData(LunacidEntrance.abyss_20f_to_25f, LunacidRegion.tower_of_abyss_25f),
    EntranceData(LunacidEntrance.abyss_25f_to_30f, LunacidRegion.tower_of_abyss_30f),
    EntranceData(LunacidEntrance.abyss_30f_to_35f, LunacidRegion.tower_of_abyss_35f),
    EntranceData(LunacidEntrance.abyss_35f_to_40f, LunacidRegion.tower_of_abyss_40f),
    EntranceData(LunacidEntrance.abyss_40f_to_45f, LunacidRegion.tower_of_abyss_45f),
    EntranceData(LunacidEntrance.abyss_45f_to_50f, LunacidRegion.tower_of_abyss_50f),
    EntranceData(LunacidEntrance.abyss_50f_to_final, LunacidRegion.tower_of_abyss_finish),

    # throne chamber
    EntranceData(LunacidEntrance.throne_room_to_castle_queen_path, LunacidRegion.castle_le_fanu_throne_path, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.throne_room_to_prison, LunacidRegion.terminus_prison_3f, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.throne_from_main_to_front, LunacidRegion.throne_chamber_front_path),
    EntranceData(LunacidEntrance.throne_from_front_to_main, LunacidRegion.throne_chamber),
    EntranceData(LunacidEntrance.throne_from_back_to_main, LunacidRegion.throne_chamber),
    EntranceData(LunacidEntrance.throne_from_main_to_back, LunacidRegion.throne_chamber_back_path),

    # terminus prison 1f
    EntranceData(LunacidEntrance.terminus_prison_1f_to_secrets, LunacidRegion.terminus_prison_1f_secrets),
    EntranceData(LunacidEntrance.terminus_prison_1f_to_arena, LunacidRegion.forlorn_arena, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.terminus_prison_1f_to_basement, LunacidRegion.terminus_prison_basement),
    EntranceData(LunacidEntrance.terminus_prison_1f_to_2f, LunacidRegion.terminus_prison_2f),
    EntranceData(LunacidEntrance.terminus_prison_1f_to_3f, LunacidRegion.terminus_prison_3f),

    # terminus prison 2f
    EntranceData(LunacidEntrance.terminus_prison_2f_doors, LunacidRegion.terminus_prison_2f_rooms),
    EntranceData(LunacidEntrance.terminus_prison_2f_to_1f, LunacidRegion.terminus_prison_1f),
    EntranceData(LunacidEntrance.terminus_prison_2f_to_3f, LunacidRegion.terminus_prison_3f),

    # terminus prison 3f
    EntranceData(LunacidEntrance.terminus_prison_3f_to_throne_room, LunacidRegion.throne_chamber_back_path, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.terminus_prison_3f_to_2f, LunacidRegion.terminus_prison_2f),
    EntranceData(LunacidEntrance.terminus_prison_3f_doors, LunacidRegion.terminus_prison_3f_rooms),
    EntranceData(LunacidEntrance.terminus_prison_3f_to_4f, LunacidRegion.terminus_prison_4f),

    # terminus prison 4f
    EntranceData(LunacidEntrance.terminus_prison_4f_secret_walls, LunacidRegion.terminus_prison_4f_secrets),

    # terminus prison basement
    EntranceData(LunacidEntrance.terminus_prison_basement_to_1f, LunacidRegion.terminus_prison_1f),
    EntranceData(LunacidEntrance.terminus_prison_basement_to_ash, LunacidRegion.labyrinth_of_ash, True, type=EntranceType.TWO_WAY),

    # labyrinth of ash
    EntranceData(LunacidEntrance.labyrinth_of_ash_to_terminus_prison, LunacidRegion.terminus_prison_basement, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.labyrinth_of_ash_to_interior, LunacidRegion.labyrinth_interior),
    EntranceData(LunacidEntrance.labyrinth_of_ash_to_holy_seat, LunacidRegion.holy_seat_of_gold),

    # labyrinth of ash interior
    EntranceData(LunacidEntrance.labyrinth_interior_to_secret, LunacidRegion.labyrinth_secret),

    # holy seat of gold
    EntranceData(LunacidEntrance.holy_seat_to_secret, LunacidRegion.holy_seat_of_secret),

    # forlorn arena
    EntranceData(LunacidEntrance.forlorn_arena_to_terminus_prison, LunacidRegion.terminus_prison_1f, True, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.forlorn_arena_to_temple_of_earth, LunacidRegion.temple_of_earth),
    EntranceData(LunacidEntrance.forlorn_arena_to_water_temple, LunacidRegion.temple_of_water),
    EntranceData(LunacidEntrance.forlorn_arena_to_path_to_sucsarius, LunacidRegion.forlorn_path_to_sucsarius),

    # forlorn temples.  Not much so put them together.
    EntranceData(LunacidEntrance.temple_of_earth_to_secrets, LunacidRegion.temple_of_earth_secret),
    EntranceData(LunacidEntrance.temple_of_water_to_lower, LunacidRegion.temple_of_water_lower),
    EntranceData(LunacidEntrance.temple_of_water_lower_to_secrets, LunacidRegion.temple_of_water_lower_secrets),

    # chamber of fate
    EntranceData(LunacidEntrance.forlorn_path_to_chamber, LunacidRegion.chamber_of_fate, False, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.chamber_to_forlorn_path, LunacidRegion.forlorn_path_to_sucsarius, False, type=EntranceType.TWO_WAY),
    EntranceData(LunacidEntrance.chamber_to_grave, LunacidRegion.grave_of_the_sleeper, False, type=EntranceType.TWO_WAY),

    # grave of the sleeper
    EntranceData(LunacidEntrance.grave_to_chamber, LunacidRegion.chamber_of_fate, False, type=EntranceType.TWO_WAY),
]

randomized_entrance_names = [entrance.entrance_name for entrance in lunacid_entrances if entrance.randomized]


def create_regions(starting_area: str, region_factory: RegionFactory, multiworld: MultiWorld) -> Tuple[Dict[str, Region], Dict[str, Entrance]]:
    final_regions = lunacid_regions.copy()
    regions: Dict[str: Region] = {region.name: region_factory(region.name, region.exits) for region in
                                  final_regions}
    entrances: Dict[str: Entrance] = {}
    for region in regions.values():
        for entrance in region.exits:
            multiworld.register_indirect_condition(region, entrance)
            entrances[entrance.name] = entrance

    for connection in lunacid_entrances:
        if connection.entrance_name in entrances:
            entrances[connection.entrance_name].randomization_type = connection.type
            if connection.entrance_name == LunacidEntrance.rest_to_start:
                start_region = starting_location_to_region[starting_area]
                entrances[connection.entrance_name].connect(regions[start_region])
                continue
            entrances[connection.entrance_name].connect(regions[connection.region_exit])
    return regions, entrances
