from typing import List, Set, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location
from worlds.generic.Rules import CollectionRule
from .Logic import stage_clear_round_clears_included, stage_clear_individual_clears_included, \
    round_clear_has_special, stage_clear_has_special, puzzle_individual_clears_included, puzzle_round_clears_included, \
    goal_locations_included, normal_puzzle_set_included, extra_puzzle_set_included, versus_stage_clears_included
from .Options import StarterPack, VersusGoal
from .Rom import SRAM_FACTOR
from .data.Constants import versus_stage_names, versus_free_names, versus_clear_prefixes, SC_CLEARS_START, \
    PZ_CLEARS_START, EXTRA_CLEARS_START, VS_CLEARS_START, CLEARED_SHOCK_PANELS

if TYPE_CHECKING:
    from . import TetrisAttackWorld

SC_GOAL = 1
SC_STAGE_CLEAR = 2
SC_ROUND_CLEAR = 3
SC_SPECIAL = 4
PZ_STAGE_CLEAR = 5
PZ_ROUND_CLEAR = 6
EXTRA_CLEAR = 7
EXTRA_ROUND_CLEAR = 8
VS_CLEAR = 9
VS_FREE = 10
VS_NORMAL = 11
VS_HARD = 12
VS_VHARD = 13
SHOCK_PANEL = 14


class TetrisAttackLocation(Location):
    game = "Tetris Attack"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)


class LocationData(NamedTuple):
    region: str
    location_class: int
    code: Optional[int]
    access_rule: CollectionRule = lambda state: True


location_table: Dict[str, LocationData] = {
    "Stage Clear Last Stage Clear": LocationData("Stage Clear", SC_GOAL, 0x224),
    "All Friends Normal Again": LocationData("Overworld", VS_FREE, 0x235),
}

for n in range(1, 7):
    sc_base_loc = SC_CLEARS_START + (n - 1) * 6
    pz_base_loc = PZ_CLEARS_START + (n - 1) * 11
    extra_base_loc = EXTRA_CLEARS_START + (n - 1) * 11
    location_table[f"Stage Clear Round {n} Clear"] = LocationData(f"SC Round {n}", SC_ROUND_CLEAR, sc_base_loc)
    location_table[f"Stage Clear Round {n} Special"] = LocationData(f"SC Round {n}", SC_SPECIAL,
                                                                    sc_base_loc + (1 << SRAM_FACTOR))
    for s in range(1, 6):
        location_table[f"Stage Clear {n}-{s} Clear"] = LocationData(f"SC Round {n}", SC_STAGE_CLEAR, sc_base_loc + s)
        location_table[f"Stage Clear {n}-{s} Special"] = LocationData(f"SC Round {n}", SC_SPECIAL,
                                                                      sc_base_loc + s + (1 << SRAM_FACTOR))
    location_table[f"Puzzle Round {n} Clear"] = LocationData(f"Puzzle L{n}", PZ_ROUND_CLEAR, pz_base_loc)
    location_table[f"Extra Puzzle Round {n} Clear"] = LocationData(f"Extra L{n}", EXTRA_ROUND_CLEAR, extra_base_loc)
    for s in range(1, 11):
        location_table[f"Puzzle {n}-{str(s).zfill(2)} Clear"] = LocationData(f"Puzzle L{n}", PZ_STAGE_CLEAR,
                                                                             pz_base_loc + s)
        location_table[f"Extra Puzzle {n}-{str(s).zfill(2)} Clear"] = LocationData(f"Extra L{n}", EXTRA_CLEAR,
                                                                                   extra_base_loc + s)
for n in range(0, 12):
    if n < 8:
        region = "Overworld"
        location_table[versus_free_names[n]] = LocationData(region, VS_FREE, VS_CLEARS_START + n + (1 << SRAM_FACTOR))
    else:
        region = "Mt Wickedness"
    location_table[versus_stage_names[n]] = LocationData(region, VS_CLEAR, VS_CLEARS_START + n)
    location_table[f"{versus_clear_prefixes[n]} Normal Clear"] = LocationData(region, VS_NORMAL,
                                                                              VS_CLEARS_START + n + (3 << SRAM_FACTOR))
    location_table[f"{versus_clear_prefixes[n]} Hard Clear"] = LocationData(region, VS_HARD,
                                                                            VS_CLEARS_START + n + (4 << SRAM_FACTOR))
    location_table[f"{versus_clear_prefixes[n]} V.Hard Clear"] = LocationData(region, VS_VHARD,
                                                                              VS_CLEARS_START + n + (5 << SRAM_FACTOR))
for n in range(1, 101):
    loc_id = CLEARED_SHOCK_PANELS + n * (1 << SRAM_FACTOR)
    location_table[f"Stage Clear ! Panels Check #{n}"] = LocationData("Stage Clear", SHOCK_PANEL, loc_id)
for n in range(0, 12):
    # TODO: Simplify the above table to loops
    pass


def get_locations(world: Optional["TetrisAttackWorld"]) -> Dict[str, LocationData]:
    include_stage_clear = True
    include_sc_round_clears = True
    include_sc_individual_clears = True
    exclude_sc_round_6_last_check = True
    include_pz_round_clears = True
    include_pz_individual_clears = True
    include_extra_round_clears = True
    include_extra_individual_clears = True
    include_vs_stage_clears = True
    multiple_goals = True
    special_stage_trap_count = 1
    shock_panel_group_count = 1
    if world:
        include_stage_clear = world.options.stage_clear_goal or world.options.stage_clear_inclusion
        include_sc_round_clears = stage_clear_round_clears_included(world.options)
        include_sc_individual_clears = stage_clear_individual_clears_included(world.options)
        exclude_sc_round_6_last_check = world.options.starter_pack != StarterPack.option_stage_clear_round_6
        include_normal_puzzles = normal_puzzle_set_included(world.options)
        include_extra_puzzles = extra_puzzle_set_included(world.options)
        puzzle_round_clears = puzzle_round_clears_included(world.options)
        puzzle_individual_clears = puzzle_individual_clears_included(world.options)
        include_pz_round_clears = puzzle_round_clears and include_normal_puzzles
        include_pz_individual_clears = puzzle_individual_clears and include_normal_puzzles
        include_extra_round_clears = puzzle_round_clears and include_extra_puzzles
        include_extra_individual_clears = puzzle_individual_clears and include_extra_puzzles
        include_vs_stage_clears = versus_stage_clears_included(world.options)
        special_stage_trap_count = world.options.special_stage_trap_count
        shock_panel_group_count = world.options.shock_panel_checks.value
        if not include_stage_clear:
            special_stage_trap_count = 0
            shock_panel_group_count = 0
        multiple_goals = goal_locations_included(world.options)

    excluded_locations: Set[str] = set()
    if not multiple_goals:
        excluded_locations.add("Stage Clear Last Stage Clear")
        excluded_locations.add("Puzzle Round 6 Clear")

    included_classes: List[int] = []
    if include_stage_clear:
        included_classes.append(SC_GOAL)
        included_classes.append(SC_SPECIAL)
        included_classes.append(SHOCK_PANEL)
    if include_sc_round_clears:
        included_classes.append(SC_ROUND_CLEAR)
    if include_sc_individual_clears:
        included_classes.append(SC_STAGE_CLEAR)
    if include_pz_round_clears:
        included_classes.append(PZ_ROUND_CLEAR)
    if include_pz_individual_clears:
        included_classes.append(PZ_STAGE_CLEAR)
    if include_extra_round_clears:
        included_classes.append(EXTRA_ROUND_CLEAR)
    if include_extra_individual_clears:
        included_classes.append(EXTRA_CLEAR)
    if include_vs_stage_clears:
        included_classes.append(VS_CLEAR)
        included_classes.append(VS_FREE)
    if exclude_sc_round_6_last_check:
        if include_sc_round_clears:
            excluded_locations.add("Stage Clear Round 6 Clear")
        else:
            excluded_locations.add("Stage Clear 6-5 Clear")
    for r in range(1, 7):
        if not round_clear_has_special(r, special_stage_trap_count):
            excluded_locations.add(f"Stage Clear Round {r} Special")
        for s in range(1, 6):
            if not stage_clear_has_special(r, s, special_stage_trap_count):
                excluded_locations.add(f"Stage Clear {r}-{s} Special")
    if ((world.options.versus_goal == VersusGoal.option_easy
         or world.options.versus_goal == VersusGoal.option_no_vs)
            and not world.options.versus_easy_bowser):
        excluded_locations.add(versus_stage_names[10])
        excluded_locations.add(f"{versus_clear_prefixes[10]} Normal Clear")
        excluded_locations.add(f"{versus_clear_prefixes[10]} Hard Clear")
        excluded_locations.add(f"{versus_clear_prefixes[10]} V.Hard Clear")
    if ((world.options.versus_goal == VersusGoal.option_easy
         or world.options.versus_goal == VersusGoal.option_normal
         or world.options.versus_goal == VersusGoal.option_no_vs)
            and not world.options.versus_easy_bowser):
        excluded_locations.add(versus_stage_names[11])
        excluded_locations.add(f"{versus_clear_prefixes[11]} Normal Clear")
        excluded_locations.add(f"{versus_clear_prefixes[11]} Hard Clear")
        excluded_locations.add(f"{versus_clear_prefixes[11]} V.Hard Clear")
    excluded_locations.add(f"{versus_clear_prefixes[11]} Normal Clear")
    for i in range(shock_panel_group_count + 1, 101):
        excluded_locations.add(f"Stage Clear ! Panels Check #{i}")

    new_locations = dict(
        filter(lambda item: item[1].location_class in included_classes and item[0] not in excluded_locations,
               location_table.items()))

    return new_locations
