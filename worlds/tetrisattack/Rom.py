import pkgutil
import math
from typing import TYPE_CHECKING, Iterable, Sequence
import hashlib
import Utils
import os
from struct import pack

import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .Logic import stage_clear_individual_clears_included, stage_clear_round_clears_included, round_clear_has_special, \
    stage_clear_has_special, puzzle_round_clears_included, puzzle_individual_clears_included, \
    normal_puzzle_set_included, extra_puzzle_set_included, get_starting_sc_round, puzzle_individual_unlocks_included, \
    puzzle_progressive_unlocks_included, puzzle_level_gates_included, get_starting_puzzle_level, \
    stage_clear_individual_unlocks_included, stage_clear_progressive_unlocks_included, stage_clear_round_gates_included, \
    get_starting_vs_flag
from .Options import StarterPack, StageClearMode, PuzzleMode, PuzzleGoal, VersusGoal, VersusMode

if TYPE_CHECKING:
    from . import TetrisAttackWorld

WORLD_VERSION: str = "0.4.3"
MASKED_VERSION: int = 6

USAHASH = "44bb94606356f1c0965e12bbc50866b3"

SRAM_FACTOR = 10  # 2^10 = 1 KB or 0x400
ARCHIPELAGO_DATA = 0x100000
GOALS_POSITION = ARCHIPELAGO_DATA + 0x000
SCMODE = ARCHIPELAGO_DATA + 0x003
PZMODE = ARCHIPELAGO_DATA + 0x004
VSMODE = ARCHIPELAGO_DATA + 0x005
DEATHLINKHINT = ARCHIPELAGO_DATA + 0x006
SCTOTAL_CHECKS = ARCHIPELAGO_DATA + 0x008
PZTOTAL_CHECKS = ARCHIPELAGO_DATA + 0x00A
VSTOTAL_CHECKS = ARCHIPELAGO_DATA + 0x00C
SCSHOCKPANEL_CHECKS = ARCHIPELAGO_DATA + 0x00E
SCSHOCKPANELS_PER_CHECK = ARCHIPELAGO_DATA + 0x010
MUSICFILTER = ARCHIPELAGO_DATA + 0x012
STRING_DATA = ARCHIPELAGO_DATA + 0x340
STRING_DATA_SIZE = 0x18
SCROUND1_CHECKS = ARCHIPELAGO_DATA + 0x020
SCROUND2_CHECKS = ARCHIPELAGO_DATA + 0x026
SCROUND3_CHECKS = ARCHIPELAGO_DATA + 0x02C
SCROUND4_CHECKS = ARCHIPELAGO_DATA + 0x032
SCROUND5_CHECKS = ARCHIPELAGO_DATA + 0x038
SCROUND6_CHECKS = ARCHIPELAGO_DATA + 0x03E
SCLASTSTAGE_CHECKS = ARCHIPELAGO_DATA + 0x044
SCSPECIALSTAGE_COUNT = ARCHIPELAGO_DATA + 0x045
VSSTAGE_CHECKS = ARCHIPELAGO_DATA + 0x046
VSNOCONTINUE_CHECKS = ARCHIPELAGO_DATA + 0x052
VSFRIENDSNORMAL_CHECKS = ARCHIPELAGO_DATA + 0x056
VSCHARACTER_CHECKS = ARCHIPELAGO_DATA + 0x057
PUZZLEL1_CHECKS = ARCHIPELAGO_DATA + 0x060
PUZZLEL2_CHECKS = ARCHIPELAGO_DATA + 0x06B
PUZZLEL3_CHECKS = ARCHIPELAGO_DATA + 0x076
PUZZLEL4_CHECKS = ARCHIPELAGO_DATA + 0x081
PUZZLEL5_CHECKS = ARCHIPELAGO_DATA + 0x08C
PUZZLEL6_CHECKS = ARCHIPELAGO_DATA + 0x097
PUZZLESL1_CHECKS = ARCHIPELAGO_DATA + 0x0A2
PUZZLESL2_CHECKS = ARCHIPELAGO_DATA + 0x0AD
PUZZLESL3_CHECKS = ARCHIPELAGO_DATA + 0x0B8
PUZZLESL4_CHECKS = ARCHIPELAGO_DATA + 0x0C3
PUZZLESL5_CHECKS = ARCHIPELAGO_DATA + 0x0CE
PUZZLESL6_CHECKS = ARCHIPELAGO_DATA + 0x0D9
INITIAL_SC_UNLOCKS = ARCHIPELAGO_DATA + 0x120
INITIAL_VS_UNLOCKS = ARCHIPELAGO_DATA + 0x146
INITIAL_PZ_UNLOCKS = ARCHIPELAGO_DATA + 0x160
SCSBOWSER_HP = ARCHIPELAGO_DATA + 0x300
SCSBOWSER_HPSTAGE1 = ARCHIPELAGO_DATA + 0x302
SCSBOWSER_HPSTAGE2 = ARCHIPELAGO_DATA + 0x304
SCSBOWSER_HPSTAGE3 = ARCHIPELAGO_DATA + 0x306
SCLBOWSER_HP = ARCHIPELAGO_DATA + 0x308
SCLBOWSER_HPSTAGE1 = ARCHIPELAGO_DATA + 0x30A
SCLBOWSER_HPSTAGE2 = ARCHIPELAGO_DATA + 0x30C
SCLBOWSER_HPSTAGE3 = ARCHIPELAGO_DATA + 0x30E
SCSBOWSER_BARS = ARCHIPELAGO_DATA + 0x310
SCSBOWSER_BARAMOUNT = ARCHIPELAGO_DATA + 0x312
SCLBOWSER_BARS = ARCHIPELAGO_DATA + 0x314
SCLBOWSER_BARAMOUNT = ARCHIPELAGO_DATA + 0x316
SCLBOWSER_HEAL = ARCHIPELAGO_DATA + 0x318
SC_HPCOLORS = ARCHIPELAGO_DATA + 0x31A
VS_LAST_STAGES = ARCHIPELAGO_DATA + 0x330
VS_MIN_DIFFICULTIES = ARCHIPELAGO_DATA + 0x334


class RomData:
    def __init__(self, file: bytes, name: str = "") -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytearray:
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int) -> None:
        self.file[offset] = value

    def write_bytes(self, offset: int, values: Sequence[int]) -> None:
        self.file[offset:offset + len(values)] = values

    def write_to_file(self, file: str) -> None:
        with open(file, 'wb') as outfile:
            outfile.write(self.file)


class TATKProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [USAHASH]
    game = "Tetris Attack"
    patch_file_ending = ".aptatk"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["tatk_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int) -> None:
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: "TetrisAttackWorld", patch: TATKProcedurePatch) -> None:
    patch.write_file("tatk_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/tatk_basepatch.bsdiff4"))
    puzzle_goals = int(world.options.puzzle_goal)
    if puzzle_goals == PuzzleGoal.option_puzzle_or_extra_puzzle:
        puzzle_goals = 0b111
    # TODO: Add All Clear option
    vs_goals = 0b00000
    match world.options.versus_goal:
        case VersusGoal.option_easy:
            vs_goals |= 0b01100 if world.options.versus_easy_bowser else 0b00100
        case VersusGoal.option_normal:
            vs_goals |= 0b01101 if world.options.versus_easy_bowser else 0b01001
        case VersusGoal.option_hard:
            vs_goals |= 0b01110
        case VersusGoal.option_very_hard:
            vs_goals |= 0b01111
    patch.write_bytes(GOALS_POSITION, [int(world.options.stage_clear_goal), puzzle_goals, vs_goals])
    patch.write_byte(DEATHLINKHINT, 1 if world.options.death_link else 0)
    patch.write_bytes(STRING_DATA, (WORLD_VERSION + '\0').encode('ascii')[:8])
    patch.write_bytes(STRING_DATA + 0x8, (world.player_name + '\0').encode('ascii')[:16])
    patch.write_byte(MUSICFILTER, world.options.music_filter.value)

    # Stage Clear
    include_stage_clear = world.options.stage_clear_goal or world.options.stage_clear_inclusion
    sc_mode = 0b00000
    match world.options.stage_clear_mode:
        case StageClearMode.option_incremental \
             | StageClearMode.option_incremental_with_round_gate:
            sc_mode = 0b00001
        case StageClearMode.option_skippable \
             | StageClearMode.option_skippable_with_round_gate:
            sc_mode = 0b00011
    if world.options.stage_clear_saves:
        sc_mode |= 0b00100
    if world.options.starter_pack != StarterPack.option_stage_clear_round_6:
        sc_mode |= 0b10000
    patch.write_byte(SCMODE, sc_mode)
    rc_inc = stage_clear_round_clears_included(world.options)
    ic_inc = stage_clear_individual_clears_included(world.options)
    if include_stage_clear:
        total_checks = 1 + world.options.shock_panel_checks
        special_stage_count = world.options.special_stage_trap_count.value
        for x in range(0, 6):
            rchecks = get_checks_for_sc_round_clear(x + 1, rc_inc, special_stage_count)
            if rchecks & 0b10:
                total_checks += 1
            if rc_inc:
                total_checks += 1
            if ic_inc:
                total_checks += 5
            s1 = get_checks_for_stage_clear(x + 1, 1, ic_inc, special_stage_count)
            if s1 & 0b10:
                total_checks += 1
            s2 = get_checks_for_stage_clear(x + 1, 2, ic_inc, special_stage_count)
            if s2 & 0b10:
                total_checks += 1
            s3 = get_checks_for_stage_clear(x + 1, 3, ic_inc, special_stage_count)
            if s3 & 0b10:
                total_checks += 1
            s4 = get_checks_for_stage_clear(x + 1, 4, ic_inc, special_stage_count)
            if s4 & 0b10:
                total_checks += 1
            s5 = get_checks_for_stage_clear(x + 1, 5, ic_inc, special_stage_count)
            if s5 & 0b10:
                total_checks += 1
            patch.write_bytes(SCROUND1_CHECKS + x * 6, [rchecks, s1, s2, s3, s4, s5])
        patch.write_byte(SCLASTSTAGE_CHECKS, 0b01)
        patch.write_byte(SCSPECIALSTAGE_COUNT, special_stage_count)
        patch.write_byte(SCTOTAL_CHECKS, total_checks)
        patch.write_byte(SCSHOCKPANEL_CHECKS, world.options.shock_panel_checks.value)
        patch.write_byte(SCSHOCKPANELS_PER_CHECK, world.options.shock_panels_per_check.value)

    # Puzzle
    include_puzzle = normal_puzzle_set_included(world.options)
    include_extra = extra_puzzle_set_included(world.options)
    pz_mode = 0b00000
    match world.options.puzzle_mode:
        case PuzzleMode.option_incremental \
             | PuzzleMode.option_incremental_with_level_gate:
            pz_mode = 0b00001
        case PuzzleMode.option_skippable \
             | PuzzleMode.option_skippable_with_level_gate:
            pz_mode = 0b00011
    if include_puzzle:
        pz_mode |= 0b00100
    if include_extra:
        pz_mode |= 0b01000
    patch.write_byte(PZMODE, pz_mode)
    rc_inc = puzzle_round_clears_included(world.options)
    ic_inc = puzzle_individual_clears_included(world.options)
    total_checks = 0
    for x in range(0, 6):
        if include_puzzle:
            rchecks = get_checks_for_pz_round_clear(x + 1, rc_inc)
            if rc_inc:
                total_checks += 1
            if ic_inc:
                total_checks += 10
            s01 = get_checks_for_puzzle_clear(x + 1, 1, ic_inc)
            s02 = get_checks_for_puzzle_clear(x + 1, 2, ic_inc)
            s03 = get_checks_for_puzzle_clear(x + 1, 3, ic_inc)
            s04 = get_checks_for_puzzle_clear(x + 1, 4, ic_inc)
            s05 = get_checks_for_puzzle_clear(x + 1, 5, ic_inc)
            s06 = get_checks_for_puzzle_clear(x + 1, 6, ic_inc)
            s07 = get_checks_for_puzzle_clear(x + 1, 7, ic_inc)
            s08 = get_checks_for_puzzle_clear(x + 1, 8, ic_inc)
            s09 = get_checks_for_puzzle_clear(x + 1, 9, ic_inc)
            s10 = get_checks_for_puzzle_clear(x + 1, 10, ic_inc)
            patch.write_bytes(PUZZLEL1_CHECKS + x * 11, [rchecks, s01, s02, s03, s04, s05, s06, s07, s08, s09, s10])
        if include_extra:
            rchecks = get_checks_for_pz_round_clear(x + 7, rc_inc)
            if rc_inc:
                total_checks += 1
            if ic_inc:
                total_checks += 10
            s01 = get_checks_for_puzzle_clear(x + 7, 1, ic_inc)
            s02 = get_checks_for_puzzle_clear(x + 7, 2, ic_inc)
            s03 = get_checks_for_puzzle_clear(x + 7, 3, ic_inc)
            s04 = get_checks_for_puzzle_clear(x + 7, 4, ic_inc)
            s05 = get_checks_for_puzzle_clear(x + 7, 5, ic_inc)
            s06 = get_checks_for_puzzle_clear(x + 7, 6, ic_inc)
            s07 = get_checks_for_puzzle_clear(x + 7, 7, ic_inc)
            s08 = get_checks_for_puzzle_clear(x + 7, 8, ic_inc)
            s09 = get_checks_for_puzzle_clear(x + 7, 9, ic_inc)
            s10 = get_checks_for_puzzle_clear(x + 7, 10, ic_inc)
            patch.write_bytes(PUZZLESL1_CHECKS + x * 11, [rchecks, s01, s02, s03, s04, s05, s06, s07, s08, s09, s10])
    patch.write_byte(PZTOTAL_CHECKS, total_checks)

    # Versus
    include_versus = world.options.versus_goal != VersusGoal.option_no_vs or world.options.versus_inclusion
    vs_mode = 0b000
    match world.options.versus_mode:
        case VersusMode.option_goal_difficulty | VersusMode.option_goal_progressive:
            vs_mode |= 0b001
        # case VersusMode.option_progressive_per_stage:
        #     vs_mode |= 0b010
    patch.write_byte(VSMODE, vs_mode)
    goal_diff = 0
    if include_versus:
        match world.options.versus_goal:
            case VersusGoal.option_normal:
                goal_diff = 1
            case VersusGoal.option_hard:
                goal_diff = 2
            case VersusGoal.option_very_hard:
                goal_diff = 3
        goal_stage = 12
        if world.options.versus_easy_bowser:
            patch.write_bytes(VS_LAST_STAGES, [11, 11, 11, 11])
        else:
            match world.options.versus_goal:
                case VersusGoal.option_no_vs | VersusGoal.option_easy:
                    goal_stage = 10
                    patch.write_bytes(VS_LAST_STAGES, [9, 9, 9, 9])
                case VersusGoal.option_normal:
                    goal_stage = 11
                    patch.write_bytes(VS_LAST_STAGES, [9, 10, 10, 10])
                case _:
                    patch.write_bytes(VS_LAST_STAGES, [9, 10, 11, 11])
        total_checks = 1
        for x in range(0, goal_stage):
            sc_checks = 0b00000001
            total_checks += 1
            if x < 8:
                sc_checks |= 0b00000010
                total_checks += 1
            # TODO: Add more checks with difficulties
            patch.write_byte(VSSTAGE_CHECKS + x, sc_checks)
            diff = 0
            if (x == goal_stage - 1
                    or world.options.versus_mode == VersusMode.option_goal_difficulty
                    or world.options.versus_mode == VersusMode.option_goal_progressive):
                diff = goal_diff
            if not world.options.versus_easy_bowser:
                if x == 10:
                    diff = max(diff, 1)
                if x == 11:
                    diff = max(diff, 2)
            patch.write_byte(VS_MIN_DIFFICULTIES + x, diff)
        patch.write_byte(VSFRIENDSNORMAL_CHECKS, 0b1)
        patch.write_byte(VSTOTAL_CHECKS, total_checks)

    # Initial Unlocks
    starting_sc_round = get_starting_sc_round(world.options)
    starting_puzzle_level = get_starting_puzzle_level(world.options)
    starting_vs_flag = get_starting_vs_flag(world.options)

    other_stages_already_unlocked = not (stage_clear_individual_unlocks_included(world.options)
                                         or stage_clear_progressive_unlocks_included(world.options))
    first_stage_already_unlocked = other_stages_already_unlocked
    gate_already_unlocked = not stage_clear_round_gates_included(world.options)
    for x in range(1, 7):
        is_initial_round = x == starting_sc_round
        s1_unlock = first_stage_already_unlocked or is_initial_round
        sx_unlock = other_stages_already_unlocked or is_initial_round
        gate_unlocked = gate_already_unlocked or is_initial_round
        patch.write_bytes(INITIAL_SC_UNLOCKS + 6 * (x - 1), [
            gate_unlocked, s1_unlock, sx_unlock, sx_unlock, sx_unlock, sx_unlock
        ])

    other_stages_already_unlocked = not (puzzle_individual_unlocks_included(world.options)
                                         or puzzle_progressive_unlocks_included(world.options))
    first_stage_already_unlocked = other_stages_already_unlocked
    gate_already_unlocked = not puzzle_level_gates_included(world.options)
    for x in range(1, 13):
        is_initial_level = x == starting_puzzle_level
        s1_unlock = first_stage_already_unlocked or is_initial_level
        sx_unlock = other_stages_already_unlocked or is_initial_level
        gate_unlocked = gate_already_unlocked or is_initial_level
        # TODO: Remove after finding a better way to enforce logic
        if starting_puzzle_level > 0 and x % 6 == starting_puzzle_level % 6 and (
                world.options.puzzle_mode == PuzzleMode.option_individual_stages
                or world.options.puzzle_mode == PuzzleMode.option_incremental_with_level_gate
                or world.options.puzzle_mode == PuzzleMode.option_skippable_with_level_gate):
            s1_unlock = True
            sx_unlock = True
        patch.write_bytes(INITIAL_PZ_UNLOCKS + 11 * (x - 1), [
            gate_unlocked, s1_unlock, sx_unlock, sx_unlock, sx_unlock, sx_unlock, sx_unlock, sx_unlock, sx_unlock,
            sx_unlock, sx_unlock
        ])
    if starting_vs_flag:
        patch.write_bytes(INITIAL_VS_UNLOCKS, [goal_diff + 1, goal_diff + 1])

    # Special Stage and Last Stage
    patch.write_bytes(SCSBOWSER_HP, pack("H", world.options.special_stage_hp_multiplier.value * 100))
    patch.write_bytes(SCSBOWSER_HPSTAGE1,
                      pack("H", min(max(world.options.special_stage_hp_multiplier.value * 75, 99), 3000)))
    patch.write_bytes(SCSBOWSER_HPSTAGE2,
                      pack("H", min(max(world.options.special_stage_hp_multiplier.value * 50, 66), 2000)))
    patch.write_bytes(SCSBOWSER_HPSTAGE3,
                      pack("H", min(max(world.options.special_stage_hp_multiplier.value * 25, 33), 1000)))
    max_health_bars = 1
    if world.options.special_stage_hp_multiplier.value > 11:
        health_bars = math.ceil(world.options.special_stage_hp_multiplier.value / 10)
        max_health_bars = health_bars
        patch.write_bytes(SCSBOWSER_BARS, pack("H", health_bars - 1))
        patch.write_bytes(SCSBOWSER_BARAMOUNT,
                          pack("H", math.ceil(world.options.special_stage_hp_multiplier.value * 100 / health_bars)))
    else:
        patch.write_bytes(SCSBOWSER_BARAMOUNT,
                          pack("H", world.options.special_stage_hp_multiplier.value * 100))
    patch.write_bytes(SCLBOWSER_HP, pack("H", world.options.last_stage_hp_multiplier.value * 100))
    patch.write_bytes(SCLBOWSER_HPSTAGE1,
                      pack("H", min(max(world.options.last_stage_hp_multiplier.value * 75, 99), 3000)))
    patch.write_bytes(SCLBOWSER_HPSTAGE2,
                      pack("H", min(max(world.options.last_stage_hp_multiplier.value * 50, 66), 2000)))
    patch.write_bytes(SCLBOWSER_HPSTAGE3,
                      pack("H", min(max(world.options.last_stage_hp_multiplier.value * 25, 33), 1000)))
    if world.options.last_stage_hp_multiplier.value > 11:
        health_bars = math.ceil(world.options.last_stage_hp_multiplier.value / 10)
        max_health_bars = max(max_health_bars, health_bars)
        patch.write_bytes(SCLBOWSER_BARS, pack("H", health_bars - 1))
        patch.write_bytes(SCLBOWSER_BARAMOUNT,
                          pack("H", math.ceil(world.options.last_stage_hp_multiplier.value * 100 / health_bars)))
    else:
        patch.write_bytes(SCLBOWSER_BARAMOUNT,
                          pack("H", world.options.last_stage_hp_multiplier.value * 100))
    if max_health_bars <= 2:
        patch.write_bytes(SC_HPCOLORS + 2, pack("H", 0x037B))
        patch.write_bytes(SC_HPCOLORS + 4, pack("H", 0x0380))
    patch.write_bytes(SCLBOWSER_HEAL, pack("H", world.options.last_stage_hp_multiplier.value * 100))

    from Utils import __version__
    rom_prefix = bytearray(f'ATK{__version__.replace(".", "")[0:3]}', 'utf8')
    patch.name = bytearray(
        f'{format(MASKED_VERSION, "X")}|{world.player}{world.multiworld.seed:11}\0',
        'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x007FB0, rom_prefix)
    patch.write_bytes(0x007FC0, patch.name)
    patch.write_byte(0x007FDB, MASKED_VERSION)

    patch.write_file("token_patch.bin", patch.get_token_binary())


def get_checks_for_sc_round_clear(round_index: int, include_round_clear: bool, trap_count: int):
    checks_mask = 0b01 if include_round_clear else 0b00
    if round_clear_has_special(round_index, trap_count):
        checks_mask |= 0b10
    return checks_mask


def get_checks_for_stage_clear(round_index: int, stage_index: int, include_stage_clear: bool, trap_count: int):
    checks_mask = 0b01 if include_stage_clear else 0b00
    if stage_clear_has_special(round_index, stage_index, trap_count):
        checks_mask |= 0b10
    return checks_mask


def get_checks_for_pz_round_clear(level_index: int, include_round_clear: bool):
    checks_mask = 0b01 if include_round_clear else 0b00
    return checks_mask


def get_checks_for_puzzle_clear(level_index: int, stage_index: int, include_stage_clear: bool):
    checks_mask = 0b01 if include_stage_clear else 0b00
    return checks_mask


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USAHASH != basemd5.hexdigest():
            raise Exception("Supplied Base Rom does not match known MD5 for US(1.0) release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["tetrisattack_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
