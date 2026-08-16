from typing import List, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import ItemClassification
from .Logic import stage_clear_progressive_unlocks_included, stage_clear_individual_unlocks_included, \
    stage_clear_round_gates_included, puzzle_progressive_unlocks_included, puzzle_individual_unlocks_included, \
    puzzle_level_gates_included, get_starting_sc_round, get_starting_puzzle_level, normal_puzzle_set_included, \
    extra_puzzle_set_included, versus_progressive_unlocks_included, versus_individual_unlocks_included, \
    get_starting_vs_flag, shock_panels_lead_to_traps
from .Options import StarterPack, VersusGoal, PuzzleMode
from .data.Constants import versus_unlock_names, versus_characters, SC_UNLOCKS_START, PZ_UNLOCKS_START, \
    EXTRA_UNLOCKS_START, VS_CHARACTERS_START, VS_UNLOCKS_START

if TYPE_CHECKING:
    from . import TetrisAttackWorld

FILLER = 0
SC_GOAL = 1
SC_PROGRESSIVE_UNLOCK = 2
SC_INDIVIDUAL_UNLOCK = 3
SC_ROUND_GATE = 4
SC_TRAP = 5
PZ_GOAL = 6
PZ_PROGRESSIVE_UNLOCK = 7
PZ_INDIVIDUAL_UNLOCK = 8
PZ_LEVEL_GATE = 9
EXTRA_PROGRESSIVE_UNLOCK = 10
EXTRA_INDIVIDUAL_UNLOCK = 11
EXTRA_LEVEL_GATE = 12
VS_PROGRESSIVE_UNLOCK = 13
VS_STAGE_UNLOCK = 14
VS_CHARACTER = 15
VS_GATE = 16
VS_GOAL = 17
SHOCK_PANEL = 18


class ItemData(NamedTuple):
    category: str
    code: Optional[int]
    item_class: int
    classification: ItemClassification
    amount: Optional[int] = 1
    starting_id: Optional[int] = None
    amount2: Optional[int] = None
    starting_id2: Optional[int] = None


item_table: Dict[str, ItemData] = {
    "Vs. Progressive Stage Unlock": ItemData("Versus", 19, VS_PROGRESSIVE_UNLOCK,
                                             ItemClassification.progression, 12, 0x046),
    # Items with IDs of at least 0x020 correspond to SRAM locations
    "Stage Clear Last Stage": ItemData("Stage Clear", 0x044, SC_GOAL, ItemClassification.progression),
    "Stage Clear Special Stage Trap": ItemData("Stage Clear", 0x045, SC_TRAP, ItemClassification.trap),
    "Stage Clear Completion": ItemData("Stage Clear", None, SC_GOAL, ItemClassification.progression),
    "Puzzle Completion": ItemData("Puzzle", None, PZ_GOAL, ItemClassification.progression),
    "Versus Completion": ItemData("Versus", None, VS_GOAL, ItemClassification.progression),
    "Mt. Wickedness Gate": ItemData("Overworld", 0x05A, VS_GATE, ItemClassification.progression),

    "Stage Clear ! Panel Bundle": ItemData("Stage Clear", 0x0EA, SHOCK_PANEL,
                                     ItemClassification.progression_deprioritized_skip_balancing),

    # "50 Points": ItemData("Stage Clear", 0x100, FILLER, ItemClassification.filler),
    "80 Points": ItemData("Stage Clear", 0x101, FILLER, ItemClassification.filler),
    "150 Points": ItemData("Stage Clear", 0x102, FILLER, ItemClassification.filler),
    "300 Points": ItemData("Stage Clear", 0x103, FILLER, ItemClassification.filler),
    "400 Points": ItemData("Stage Clear", 0x104, FILLER, ItemClassification.filler),
    "500 Points": ItemData("Stage Clear", 0x105, FILLER, ItemClassification.filler),
    "700 Points": ItemData("Stage Clear", 0x106, FILLER, ItemClassification.filler),
    "900 Points": ItemData("Stage Clear", 0x107, FILLER, ItemClassification.filler),
    "1100 Points": ItemData("Stage Clear", 0x108, FILLER, ItemClassification.filler),
    "1300 Points": ItemData("Stage Clear", 0x109, FILLER, ItemClassification.filler),
    "1500 Points": ItemData("Stage Clear", 0x10A, FILLER, ItemClassification.filler),
    "1800 Points": ItemData("Stage Clear", 0x10B, FILLER, ItemClassification.filler),
    "20 Points": ItemData("Stage Clear", 0x10C, FILLER, ItemClassification.filler),
    "30 Points": ItemData("Stage Clear", 0x10D, FILLER, ItemClassification.filler),
    "50 Points": ItemData("Stage Clear", 0x10E, FILLER, ItemClassification.filler),
    "60 Points": ItemData("Stage Clear", 0x10F, FILLER, ItemClassification.filler),
    "70 Points": ItemData("Stage Clear", 0x110, FILLER, ItemClassification.filler),
    # "80 Points": ItemData("Stage Clear", 0x111, FILLER, ItemClassification.filler),
    "100 Points": ItemData("Stage Clear", 0x112, FILLER, ItemClassification.filler),
    "140 Points": ItemData("Stage Clear", 0x113, FILLER, ItemClassification.filler),
    "170 Points": ItemData("Stage Clear", 0x114, FILLER, ItemClassification.filler),
    "210 Points": ItemData("Stage Clear", 0x115, FILLER, ItemClassification.filler),
    "250 Points": ItemData("Stage Clear", 0x116, FILLER, ItemClassification.filler),
    "290 Points": ItemData("Stage Clear", 0x117, FILLER, ItemClassification.filler),
    "340 Points": ItemData("Stage Clear", 0x118, FILLER, ItemClassification.filler),
    "390 Points": ItemData("Stage Clear", 0x119, FILLER, ItemClassification.filler),
    "440 Points": ItemData("Stage Clear", 0x11A, FILLER, ItemClassification.filler),
    "490 Points": ItemData("Stage Clear", 0x11B, FILLER, ItemClassification.filler),
    "550 Points": ItemData("Stage Clear", 0x11C, FILLER, ItemClassification.filler),
    "610 Points": ItemData("Stage Clear", 0x11D, FILLER, ItemClassification.filler),
    "680 Points": ItemData("Stage Clear", 0x11E, FILLER, ItemClassification.filler),
    "750 Points": ItemData("Stage Clear", 0x11F, FILLER, ItemClassification.filler),
    "820 Points": ItemData("Stage Clear", 0x120, FILLER, ItemClassification.filler),
    "980 Points": ItemData("Stage Clear", 0x121, FILLER, ItemClassification.filler),
    "1060 Points": ItemData("Stage Clear", 0x122, FILLER, ItemClassification.filler),
    "1150 Points": ItemData("Stage Clear", 0x123, FILLER, ItemClassification.filler),
    "1240 Points": ItemData("Stage Clear", 0x124, FILLER, ItemClassification.filler),
    "1330 Points": ItemData("Stage Clear", 0x125, FILLER, ItemClassification.filler),
}

for n in range(1, 7):
    sc_base_loc = SC_UNLOCKS_START + (n - 1) * 6
    pz_base_loc = PZ_UNLOCKS_START + (n - 1) * 11
    extra_base_loc = EXTRA_UNLOCKS_START + (n - 1) * 11

    item_table[f"Stage Clear Progressive Round {n} Unlock"] = ItemData(f"SC Round {n}", n, SC_PROGRESSIVE_UNLOCK,
                                                                       ItemClassification.progression,
                                                                       5, sc_base_loc + 1)
    item_table[f"Puzzle Progressive Level {n} Unlock"] = ItemData(f"Puzzle L{n}", 6 + n, PZ_PROGRESSIVE_UNLOCK,
                                                                  ItemClassification.progression,
                                                                  10, pz_base_loc + 1,
                                                                  0, extra_base_loc + 1)
    item_table[f"Extra Puzzle Progressive Level {n} Unlock"] = ItemData(f"Extra L{n}", 12 + n, EXTRA_PROGRESSIVE_UNLOCK,
                                                                        ItemClassification.progression,
                                                                        10, extra_base_loc + 1)

    item_table[f"Stage Clear Round {n} Gate"] = ItemData("Stage Clear", sc_base_loc, SC_ROUND_GATE,
                                                         ItemClassification.progression)
    for s in range(1, 6):
        item_table[f"Stage Clear {n}-{s} Unlock"] = ItemData(f"SC Round {n}", sc_base_loc + s, SC_INDIVIDUAL_UNLOCK,
                                                             ItemClassification.progression)

    item_table[f"Puzzle Level {n} Gate"] = ItemData("Puzzle", pz_base_loc, PZ_LEVEL_GATE,
                                                    ItemClassification.progression)
    item_table[f"Extra Puzzle Level {n} Gate"] = ItemData("Puzzle", extra_base_loc, EXTRA_LEVEL_GATE,
                                                          ItemClassification.progression)
    for s in range(1, 11):
        item_table[f"Puzzle {n}-{str(s).zfill(2)} Unlock"] = ItemData(f"Puzzle L{n}", pz_base_loc + s,
                                                                      PZ_INDIVIDUAL_UNLOCK,
                                                                      ItemClassification.progression)
        item_table[f"Extra Puzzle {n}-{str(s).zfill(2)} Unlock"] = ItemData(f"Extra L{n}", extra_base_loc + s,
                                                                            EXTRA_INDIVIDUAL_UNLOCK,
                                                                            ItemClassification.progression)
for n in range(0, 12):
    if n < 8:
        region = "Overworld"
        item_table[versus_characters[n]] = ItemData("Overworld", VS_CHARACTERS_START + n, VS_CHARACTER,
                                                    ItemClassification.filler)
    else:
        region = "Mt Wickedness"
    item_table[versus_unlock_names[n]] = ItemData(region, VS_UNLOCKS_START + n, VS_STAGE_UNLOCK,
                                                  ItemClassification.progression)

filler_items = filter((lambda item_tuple: item_tuple[1].item_class == FILLER), item_table.items())
filler_item_names = list(map(lambda item_tuple: item_tuple[0], filler_items))
progressive_items = dict()
for name, row in item_table.items():
    if row.code is not None and row.code < 0x020:
        progressive_items[row.code] = row


def modify_item_amount(old_item: ItemData, new_amount: int):
    return ItemData(old_item.category, old_item.code, old_item.item_class, old_item.classification, new_amount,
                    old_item.starting_id)


def get_items(world: Optional["TetrisAttackWorld"]) -> Dict[str, ItemData]:
    include_sc_progressive_unlocks = True
    include_sc_individual_unlocks = True
    include_sc_round_gates = True
    include_pz_progressive_unlocks = True
    include_pz_individual_unlocks = True
    include_pz_level_gates = True
    include_extra_progressive_unlocks = True
    include_extra_individual_unlocks = True
    include_extra_level_gates = True
    include_vs_progressive_unlocks = True
    include_vs_individual_unlocks = True
    special_stage_trap_count = 1
    shock_panel_group_count = 1
    excluded_items: List[str] = []
    if world:
        include_stage_clear = world.options.stage_clear_goal or world.options.stage_clear_inclusion
        include_sc_progressive_unlocks = stage_clear_progressive_unlocks_included(world.options)
        include_sc_individual_unlocks = stage_clear_individual_unlocks_included(world.options)
        include_sc_round_gates = stage_clear_round_gates_included(world.options)
        include_normal_puzzles = normal_puzzle_set_included(world.options)
        include_extra_puzzles = extra_puzzle_set_included(world.options)
        puzzle_progressive_unlocks = puzzle_progressive_unlocks_included(world.options)
        puzzle_individual_unlocks = puzzle_individual_unlocks_included(world.options)
        puzzle_level_gates = puzzle_level_gates_included(world.options)
        include_pz_progressive_unlocks = puzzle_progressive_unlocks and include_normal_puzzles
        include_pz_individual_unlocks = puzzle_individual_unlocks and include_normal_puzzles
        include_pz_level_gates = puzzle_level_gates and include_normal_puzzles
        include_extra_progressive_unlocks = puzzle_progressive_unlocks and include_extra_puzzles
        include_extra_individual_unlocks = puzzle_individual_unlocks and include_extra_puzzles
        include_extra_level_gates = puzzle_level_gates and include_extra_puzzles
        include_vs_progressive_unlocks = versus_progressive_unlocks_included(world.options)
        include_vs_individual_unlocks = versus_individual_unlocks_included(world.options)
        special_stage_trap_count = world.options.special_stage_trap_count.value
        shock_panel_group_count = world.options.shock_panel_checks.value
        if not include_stage_clear:
            special_stage_trap_count = 0
            shock_panel_group_count = 0
        starter_item_names = get_starter_item_names(world)
        for ex in starter_item_names:
            excluded_items.append(ex)
        if world.options.starter_pack != StarterPack.option_stage_clear_round_6:
            excluded_items.append("Stage Clear Last Stage")

    included_classes: List[int] = []
    if include_sc_progressive_unlocks:
        included_classes.append(SC_PROGRESSIVE_UNLOCK)
    if include_sc_individual_unlocks:
        included_classes.append(SC_INDIVIDUAL_UNLOCK)
    if include_sc_round_gates:
        included_classes.append(SC_ROUND_GATE)
    if shock_panel_group_count > 0:
        included_classes.append(SHOCK_PANEL)
    if special_stage_trap_count > 0:
        included_classes.append(SC_TRAP)
    if include_pz_progressive_unlocks:
        included_classes.append(PZ_PROGRESSIVE_UNLOCK)
    if include_pz_individual_unlocks:
        included_classes.append(PZ_INDIVIDUAL_UNLOCK)
    if include_pz_level_gates:
        included_classes.append(PZ_LEVEL_GATE)
    if include_extra_progressive_unlocks:
        included_classes.append(EXTRA_PROGRESSIVE_UNLOCK)
    if include_extra_individual_unlocks:
        included_classes.append(EXTRA_INDIVIDUAL_UNLOCK)
    if include_extra_level_gates:
        included_classes.append(EXTRA_LEVEL_GATE)
    if include_vs_progressive_unlocks:
        included_classes.append(VS_PROGRESSIVE_UNLOCK)
        included_classes.append(VS_CHARACTER)
        included_classes.append(VS_GATE)
    if include_vs_individual_unlocks:
        included_classes.append(VS_STAGE_UNLOCK)
        included_classes.append(VS_CHARACTER)
        included_classes.append(VS_GATE)

    new_items = dict(filter(lambda item: item[1].item_class in included_classes, item_table.items()))
    for ex in excluded_items:
        data = new_items.get(ex)
        if data:
            if data.amount == 1:
                del new_items[ex]
            else:
                new_items[ex] = modify_item_amount(data, data.amount - 1)
    if "Stage Clear Special Stage Trap" in new_items:
        if special_stage_trap_count > 0:
            new_items["Stage Clear Special Stage Trap"] = modify_item_amount(
                new_items["Stage Clear Special Stage Trap"],
                special_stage_trap_count)
        else:
            del new_items["Stage Clear Special Stage Trap"]
    if "Vs. Progressive Stage Unlock" in new_items and not world.options.versus_easy_bowser:
        old_item = new_items["Vs. Progressive Stage Unlock"]
        unlock_count = old_item.amount
        if world.options.versus_goal == VersusGoal.option_easy or world.options.versus_goal == VersusGoal.option_no_vs:
            unlock_count -= 2
        elif world.options.versus_goal == VersusGoal.option_normal:
            unlock_count -= 1
        new_items["Vs. Progressive Stage Unlock"] = modify_item_amount(old_item, unlock_count)
    if "Stage Clear ! Panel Bundle" in new_items:
        old_item = new_items["Stage Clear ! Panel Bundle"]
        new_classification = old_item.classification
        if shock_panels_lead_to_traps(world.options):
            new_classification |= ItemClassification.trap
        else:
            new_classification |= ItemClassification.useful
        new_items["Stage Clear ! Panel Bundle"] = ItemData(old_item.category, old_item.code, old_item.item_class,
                                                     new_classification, shock_panel_group_count, old_item.starting_id)
    return new_items


def get_starter_item_names(world: "TetrisAttackWorld") -> List[str]:
    starting_sc_round = get_starting_sc_round(world.options)
    starting_puzzle_level = get_starting_puzzle_level(world.options)
    extra_puzzles_included = extra_puzzle_set_included(world.options)
    starting_in_vs = get_starting_vs_flag(world.options)

    starter_items: List[str] = []
    if stage_clear_round_gates_included(world.options):
        if starting_sc_round <= 6:
            starter_items.append(f"Stage Clear Round {starting_sc_round} Gate")
    if stage_clear_progressive_unlocks_included(world.options):
        if starting_sc_round <= 6:
            for _ in range(5):
                starter_items.append(f"Stage Clear Progressive Round {starting_sc_round} Unlock")
    elif stage_clear_individual_unlocks_included(world.options):
        if starting_sc_round <= 6:
            starter_items.append(f"Stage Clear {starting_sc_round}-1 Unlock")
            starter_items.append(f"Stage Clear {starting_sc_round}-2 Unlock")
            starter_items.append(f"Stage Clear {starting_sc_round}-3 Unlock")
            starter_items.append(f"Stage Clear {starting_sc_round}-4 Unlock")
            starter_items.append(f"Stage Clear {starting_sc_round}-5 Unlock")
    if puzzle_level_gates_included(world.options):
        if starting_puzzle_level > 6:
            starter_items.append(f"Extra Puzzle Level {starting_puzzle_level - 6} Gate")
        elif starting_puzzle_level > 0:
            starter_items.append(f"Puzzle Level {starting_puzzle_level} Gate")
    if puzzle_progressive_unlocks_included(world.options):
        if starting_puzzle_level > 6:
            for _ in range(10):
                starter_items.append(f"Extra Puzzle Progressive Level {starting_puzzle_level - 6} Unlock")
        elif starting_puzzle_level > 0:
            for _ in range(10):
                starter_items.append(f"Puzzle Progressive Level {starting_puzzle_level} Unlock")
                # TODO: Remove after finding a better way to enforce logic
                if extra_puzzles_included and (
                        world.options.puzzle_mode == PuzzleMode.option_individual_stages
                        or world.options.puzzle_mode == PuzzleMode.option_incremental_with_level_gate):
                    starter_items.append(f"Extra Puzzle Progressive Level {starting_puzzle_level} Unlock")
    elif puzzle_individual_unlocks_included(world.options):
        if starting_puzzle_level > 6:
            starter_items.append(f"Extra Puzzle {starting_puzzle_level - 6}-01 Unlock")
            starter_items.append(f"Extra Puzzle {starting_puzzle_level - 6}-02 Unlock")
            starter_items.append(f"Extra Puzzle {starting_puzzle_level - 6}-03 Unlock")
            starter_items.append(f"Extra Puzzle {starting_puzzle_level - 6}-04 Unlock")
            starter_items.append(f"Extra Puzzle {starting_puzzle_level - 6}-05 Unlock")
            starter_items.append(f"Extra Puzzle {starting_puzzle_level - 6}-06 Unlock")
            starter_items.append(f"Extra Puzzle {starting_puzzle_level - 6}-07 Unlock")
            starter_items.append(f"Extra Puzzle {starting_puzzle_level - 6}-08 Unlock")
            starter_items.append(f"Extra Puzzle {starting_puzzle_level - 6}-09 Unlock")
            starter_items.append(f"Extra Puzzle {starting_puzzle_level - 6}-10 Unlock")
        elif starting_puzzle_level > 0:
            starter_items.append(f"Puzzle {starting_puzzle_level}-01 Unlock")
            starter_items.append(f"Puzzle {starting_puzzle_level}-02 Unlock")
            starter_items.append(f"Puzzle {starting_puzzle_level}-03 Unlock")
            starter_items.append(f"Puzzle {starting_puzzle_level}-04 Unlock")
            starter_items.append(f"Puzzle {starting_puzzle_level}-05 Unlock")
            starter_items.append(f"Puzzle {starting_puzzle_level}-06 Unlock")
            starter_items.append(f"Puzzle {starting_puzzle_level}-07 Unlock")
            starter_items.append(f"Puzzle {starting_puzzle_level}-08 Unlock")
            starter_items.append(f"Puzzle {starting_puzzle_level}-09 Unlock")
            starter_items.append(f"Puzzle {starting_puzzle_level}-10 Unlock")
            if extra_puzzles_included:  # TODO: Remove after finding a better way to enforce logic
                starter_items.append(f"Extra Puzzle {starting_puzzle_level}-01 Unlock")
                starter_items.append(f"Extra Puzzle {starting_puzzle_level}-02 Unlock")
                starter_items.append(f"Extra Puzzle {starting_puzzle_level}-03 Unlock")
                starter_items.append(f"Extra Puzzle {starting_puzzle_level}-04 Unlock")
                starter_items.append(f"Extra Puzzle {starting_puzzle_level}-05 Unlock")
                starter_items.append(f"Extra Puzzle {starting_puzzle_level}-06 Unlock")
                starter_items.append(f"Extra Puzzle {starting_puzzle_level}-07 Unlock")
                starter_items.append(f"Extra Puzzle {starting_puzzle_level}-08 Unlock")
                starter_items.append(f"Extra Puzzle {starting_puzzle_level}-09 Unlock")
                starter_items.append(f"Extra Puzzle {starting_puzzle_level}-10 Unlock")
    if versus_progressive_unlocks_included(world.options):
        if starting_in_vs:
            starter_items.append("Vs. Progressive Stage Unlock")
            starter_items.append("Vs. Progressive Stage Unlock")
    if versus_individual_unlocks_included(world.options):
        if starting_in_vs:
            starter_items.append(versus_unlock_names[0])
            starter_items.append(versus_unlock_names[1])
    return starter_items
