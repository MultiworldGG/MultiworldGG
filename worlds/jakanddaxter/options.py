from dataclasses import dataclass
from functools import cached_property
from typing import Any

from Options import PerGameCommonOptions, StartInventoryPool, Toggle, Choice, Range, DefaultOnToggle, OptionCounter, \
    AssembleOptions
from .items import trap_item_table


class readonly_classproperty:
    """This decorator is used for getting friendly or unfriendly range_end values for options like FireCanyonCellCount
    and CitizenOrbTradeAmount. We only need to provide a getter as we will only be setting a single int to one of two
    values."""
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


@readonly_classproperty
def determine_range_end(cls) -> int:
    from . import JakAndDaxterWorld  # Avoid circular imports.
    friendly = JakAndDaxterWorld.settings.enforce_friendly_options
    return cls.friendly_maximum if friendly else cls.absolute_maximum


class classproperty:
    """This decorator (?) is used for getting and setting friendly or unfriendly option values for the Orbsanity
    options."""
    def __init__(self, getter, setter):
        self.getter = getter
        self.setter = setter

    def __get__(self, obj, value):
        return self.getter(obj)

    def __set__(self, obj, value):
        self.setter(obj, value)


class AllowedChoiceMeta(AssembleOptions):
    """This metaclass overrides AssembleOptions and provides inheriting classes a way to filter out "disallowed" values
    by way of implementing get_disallowed_options. This function is used by Jak and Daxter to check host.yaml settings
    without circular imports or breaking the settings API."""
    _name_lookup: dict[int, str]
    _options: dict[str, int]

    def __new__(mcs, name, bases, attrs):
        ret = super().__new__(mcs, name, bases, attrs)
        ret._name_lookup = attrs["name_lookup"]
        ret._options = attrs["options"]
        return ret

    def set_name_lookup(cls, value : dict[int, str]):
        cls._name_lookup = value

    def get_name_lookup(cls) -> dict[int, str]:
        cls._name_lookup = {k: v for k, v in cls._name_lookup.items() if k not in cls.get_disallowed_options()}
        return cls._name_lookup

    def set_options(cls, value: dict[str, int]):
        cls._options = value

    def get_options(cls) -> dict[str, int]:
        cls._options = {k: v for k, v in cls._options.items() if v not in cls.get_disallowed_options()}
        return cls._options

    def get_disallowed_options(cls):
        return {}

    name_lookup = classproperty(get_name_lookup, set_name_lookup)
    options = classproperty(get_options, set_options)


class AllowedChoice(Choice, metaclass=AllowedChoiceMeta):
    pass


class EnableMoveRandomizer(Toggle):
    """Include movement options as items in the randomizer. Until you find his other moves, Jak is limited to
    running, swimming, single-jumping, and shooting yellow eco through his goggles.

    This adds 11 items to the pool."""
    display_name = "Enable Move Randomizer"


class EnableOrbsanity(Choice):
    """Include bundles of Precursor Orbs as checks. Every time you collect the chosen number of orbs, you will trigger
    another check.

    **Per Level:** bundles are for each level in the game.

    **Global:** bundles carry over level to level.

    This adds a number of Items and Locations to the pool inversely proportional to the size of the bundle.
    For example, if your bundle size is 20 orbs, you will add 100 items to the pool. If your bundle size is 250 orbs,
    you will add 8 items to the pool."""
    display_name = "Enable Orbsanity"
    option_off = 0
    option_per_level = 1
    option_global = 2
    default = 0


class GlobalOrbsanityBundleSize(AllowedChoice):
    """The orb bundle size for Global Orbsanity. This only applies if "Enable Orbsanity" is set to "Global."
    There are 2000 orbs in the game, so your bundle size must be a factor of 2000.

    This value is restricted to safe minimum and maximum values to ensure valid singleplayer games and
    non-disruptive multiplayer games, but the host can remove this restriction by turning off enforce_friendly_options
    in host.yaml."""
    display_name = "Global Orbsanity Bundle Size"
    option_1_orb = 1
    option_2_orbs = 2
    option_4_orbs = 4
    option_5_orbs = 5
    option_8_orbs = 8
    option_10_orbs = 10
    option_16_orbs = 16
    option_20_orbs = 20
    option_25_orbs = 25
    option_40_orbs = 40
    option_50_orbs = 50
    option_80_orbs = 80
    option_100_orbs = 100
    option_125_orbs = 125
    option_200_orbs = 200
    option_250_orbs = 250
    option_400_orbs = 400
    option_500_orbs = 500
    option_1000_orbs = 1000
    option_2000_orbs = 2000
    friendly_minimum = 10
    friendly_maximum = 200
    default = 20

    @classmethod
    def get_disallowed_options(cls) -> set[int]:
        try:
            from . import JakAndDaxterWorld
            if JakAndDaxterWorld.settings.enforce_friendly_options:
                return {cls.option_1_orb,
                        cls.option_2_orbs,
                        cls.option_4_orbs,
                        cls.option_5_orbs,
                        cls.option_8_orbs,
                        cls.option_250_orbs,
                        cls.option_400_orbs,
                        cls.option_500_orbs,
                        cls.option_1000_orbs,
                        cls.option_2000_orbs}
        except ImportError:
            pass
        return set()


class PerLevelOrbsanityBundleSize(AllowedChoice):
    """The orb bundle size for Per Level Orbsanity. This only applies if "Enable Orbsanity" is set to "Per Level."
    There are 50, 150, or 200 orbs per level, so your bundle size must be a factor of 50.

    This value is restricted to safe minimum and maximum values to ensure valid singleplayer games and
    non-disruptive multiplayer games, but the host can remove this restriction by turning off enforce_friendly_options
    in host.yaml."""
    display_name = "Per Level Orbsanity Bundle Size"
    option_1_orb = 1
    option_2_orbs = 2
    option_5_orbs = 5
    option_10_orbs = 10
    option_25_orbs = 25
    option_50_orbs = 50
    friendly_minimum = 10
    default = 25

    @classmethod
    def get_disallowed_options(cls) -> set[int]:
        try:
            from . import JakAndDaxterWorld
            if JakAndDaxterWorld.settings.enforce_friendly_options:
                return {cls.option_1_orb,
                        cls.option_2_orbs,
                        cls.option_5_orbs}
        except ImportError:
            pass
        return set()


class FireCanyonCellCount(Range):
    """The number of power cells you need to cross Fire Canyon.

    This value is restricted to a safe maximum value to ensure valid singleplayer games and non-disruptive multiplayer
    games, but the host can remove this restriction by turning off enforce_friendly_options in host.yaml."""
    display_name = "Fire Canyon Cell Count"
    friendly_maximum = 30
    absolute_maximum = 100
    range_start = 0
    range_end = determine_range_end
    default = 20


class MountainPassCellCount(Range):
    """The number of power cells you need to reach Klaww and cross Mountain Pass.

    This value is restricted to a safe maximum value to ensure valid singleplayer games and non-disruptive multiplayer
    games, but the host can remove this restriction by turning off enforce_friendly_options in host.yaml."""
    display_name = "Mountain Pass Cell Count"
    friendly_maximum = 60
    absolute_maximum = 100
    range_start = 0
    range_end = determine_range_end
    default = 45


class LavaTubeCellCount(Range):
    """The number of power cells you need to cross Lava Tube.

    This value is restricted to a safe maximum value to ensure valid singleplayer games and non-disruptive multiplayer
    games, but the host can remove this restriction by turning off enforce_friendly_options in host.yaml."""
    display_name = "Lava Tube Cell Count"
    friendly_maximum = 90
    absolute_maximum = 100
    range_start = 0
    range_end = determine_range_end
    default = 72


class EnableOrderedCellCounts(DefaultOnToggle):
    """Reorder the Cell Count requirements for vehicle sections to be in ascending order.

    For example, if Fire Canyon Cell Count, Mountain Pass Cell Count, and Lava Tube Cell Count are 60, 30, and 40
    respectively, they will be reordered to 30, 40, and 60."""
    display_name = "Enable Ordered Cell Counts"


class RequirePunchForKlaww(DefaultOnToggle):
    """Force the Punch move to come before Klaww.

    Disabling this setting may require Jak to fight Klaww and Gol and Maia by shooting yellow eco through his goggles.

    This only applies if "Enable Move Randomizer" is ON."""
    display_name = "Require Punch For Klaww"


# 222 is the absolute maximum because there are 9 citizen trades and 2000 orbs to trade (2000/9 = 222).
class CitizenOrbTradeAmount(Range):
    """The number of orbs you need to trade to citizens for a power cell (Mayor, Uncle, etc.).

    Along with Oracle Orb Trade Amount, this setting cannot exceed the total number of orbs in the game (2000).
    The equation to determine the total number of trade orbs is (9 * Citizen Trades) + (6 * Oracle Trades).

    This value is restricted to a safe maximum value to ensure valid singleplayer games and non-disruptive
    multiplayer games, but the host can remove this restriction by turning off enforce_friendly_options in host.yaml."""
    display_name = "Citizen Orb Trade Amount"
    friendly_maximum = 120
    absolute_maximum = 222
    range_start = 0
    range_end = determine_range_end
    default = 90


# 333 is the absolute maximum because there are 6 oracle trades and 2000 orbs to trade (2000/6 = 333).
class OracleOrbTradeAmount(Range):
    """The number of orbs you need to trade to the Oracles for a power cell.

    Along with Citizen Orb Trade Amount, this setting cannot exceed the total number of orbs in the game (2000).
    The equation to determine the total number of trade orbs is (9 * Citizen Trades) + (6 * Oracle Trades).

    This value is restricted to a safe maximum value to ensure valid singleplayer games and non-disruptive
    multiplayer games, but the host can remove this restriction by turning off enforce_friendly_options in host.yaml."""
    display_name = "Oracle Orb Trade Amount"
    friendly_maximum = 150
    absolute_maximum = 333
    range_start = 0
    range_end = determine_range_end
    default = 120


class FillerPowerCellsReplacedWithTraps(Range):
    """
    The number of filler power cells that will be replaced with traps. This does not affect the number of progression
    power cells.

    If this value is greater than the number of filler power cells, then they will all be replaced with traps.
    """
    display_name = "Filler Power Cells Replaced With Traps"
    range_start = 0
    range_end = 100
    default = 0


class FillerOrbBundlesReplacedWithTraps(Range):
    """
    The number of filler orb bundles that will be replaced with traps. This does not affect the number of progression
    orb bundles. This only applies if "Enable Orbsanity" is set to "Per Level" or "Global."

    If this value is greater than the number of filler orb bundles, then they will all be replaced with traps.
    """
    display_name = "Filler Orb Bundles Replaced With Traps"
    range_start = 0
    range_end = 2000
    default = 0


class TrapEffectDuration(Range):
    """
    The length of time, in seconds, that a trap effect lasts. If set to 0, trap items will still be created to replace
    filler items, but they will have no effect ingame.
    """
    display_name = "Trap Effect Duration"
    range_start = 0
    range_end = 60
    default = 30


class TrapWeights(OptionCounter):
    """
    The list of traps and corresponding weights that will be randomly added to the item pool. A trap with weight 10 is
    twice as likely to appear as a trap with weight 5. Set a weight to 0 to prevent that trap from appearing altogether.
    If all weights are 0, no traps are created, overriding the values of "Filler * Replaced With Traps."
    """
    display_name = "Trap Weights"
    min = 0
    default = {trap: 1 for trap in trap_item_table.values()}
    valid_keys = sorted({trap for trap in trap_item_table.values()})

    @cached_property
    def weights_pair(self) -> tuple[list[str], list[int]]:
        return list(self.value.keys()), list(self.value.values())


class BoostedAndExtendedUppercuts(Toggle):
    """
    Create alternate paths to some areas with advanced movement.

    Enabling this setting may require Jak to use boosted and extended uppercuts as opposed to regular movement options.

    It may also require Jak to use uneven geometry, or missing collision boxes to reach unintended locations.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Boosted and Extended Uppercuts"


class PunchUppercutScoutFlies(Toggle):
    """
    Treat *Punch Uppercut* as a valid move to break scout fly boxes.

    Enabling this setting may require Jak to break scout fly boxes using only *Punch Uppercut*, even in confined spaces.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Punch Uppercut Scout Flies"


class GeyserRockCliffClimb(Toggle):
    """
    Remove the movement requirement for the Geyser Rock Cliff.

    Enabling this setting may require Jak to use uneven terrain to reach the cliff with only *Single Jump*.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Geyser Rock Cliff Climb"


class SentinelBeachCannonTowerClimb(Choice):
    """
    Create an alternate path to the Sentinel Beach Cannon Tower.

    Enabling this setting may require Jak to use uneven geometry to reach the cannon tower without having the
    *Blue Eco Switch* unlocked.

    **Medium:** Tower is climbable with only *Double Jump*.

    **Hard:** Tower is climbable with only *Jump Kick* or only *Double Jump*.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Sentinel Beach Cannon Tower Climb"
    option_no = 0
    option_medium = 1
    option_hard = 2


class SnowyMountainEntranceClimb(Choice):
    """
    Create an alternate path into Snowy Mountain.

    Enabling this setting may require Jak to use uneven geometry to reach Snowy Mountain's main area with fewer move
    options.

    **Medium:** only *Double Jump* or *Crouch Jump*

    **Hard:** only *Single Jump*

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Snowy Mountain Entrance Climb"
    option_no = 0
    option_medium = 1
    option_hard = 2


class BoggySwampFlutFlutEscape(Toggle):
    """
    Create an alternate path into the Boggy Swamp Ambush.

    Enabling this setting may require Jak to get Flut Flut into the ambush arena instead of using attacking moves.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Boggy Swamp Flut Flut Escape"


class SnowyMountainFlutFlutEscape(Toggle):
    """
    Changes Snowy Mountain to rely on Flut Flut for movement.

    Enabling this setting may require Jak to get Flut Flut over an invisible barrier to access all of Snowy Mountain.
    """
    display_name = "Snowy Mountain Flut Flut Escape"


class SnowyMountainFlutFlutSkip(Toggle):
    """
    Create an alternative path to the end of the Flut Flut course in Snowy Mountain.

    Enabling this setting may require Jak to use advanced movement tricks to reach the Fort Gate Button with only
    *Single Jump* and no *Flut Flut*.
    """
    display_name = "Snowy Mountain Flut Flut Skip"


class SandoverVillageCliffOrbCacheClimb(Toggle):
    """
    Create an alternative path to the Sandover Village orb cache on the cliff.

    Enabling this setting may require Jak to use precise jumps to reach the orb cache (and the blue eco next to it) with
    only *Single Jump*.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Sandover Village Orb Cache Climb"


class AttacklessLurkerCannons(Toggle):
    """
    Remove the attack requirement for lurker cannon power cells in Sentinel Beach and Misty Island.

    Enabling this setting may require Jak to defeat the lurkers next to the cannon without any attacking moves.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Attackless Lurker Cannons"


class SentinelBeachAttacklessPelican(Toggle):
    """
    Create an alternative path to the Pelican power cell in Sentinel Beach.

    Enabling this setting may require Jak to  use other unlocks to acquire the power cell without any attacking moves.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Sentinel Beach Attackless Pelican"


class AttackWithRollJump(Toggle):
    """
    Treat *Roll Jump* as a valid attack move for some power cells.

    Enabling this setting may require Jak to use *Roll Jump* to destroy objects and acquire these power cells.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Attack with Roll Jump"


class ForbiddenJungleAttacklessSpiralStumpsScoutFly(Toggle):
    """
    Create an alternative path to the Scout Fly "On Spiral Of Stumps" in Forbidden Jungle.

    Enabling this setting may require Jak to use precise movement to collect this scout fly without attack moves.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Forbidden Jungle Attackless Spiral Stumps Scout Fly"


class ForbiddenJungleElevatorSkip(Toggle):
    """
    Create an alternative path to the temple interior in Forbidden Jungle without having *Jungle Elevator* unlocked.

    Enabling this setting may require Jak to get inside the temple with only *Jump Kick*.
    """
    display_name = "Forbidden Jungle Elevator Skip"


class MistyIslandSingleJumpFarSideOrbCache(Toggle):
    """
    Create an alternative path to the Far Side Orb Cache in Misty Island.

    Enabling this setting may require Jak to reach the orb cache with blue eco with only *Single Jump*.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Misty Island Single Jump Far Side Orb Cache"


class MistyIslandAttacklessScoutFlies(Toggle):
    """
    Remove attack requirements to the scout flies "Barrel Ramps", "Ledge Near Arena Entrance", "Near Arena Door",
    "Overlooking Entrance" in Misty Island.

    Enabling this setting may require Jak to break these scout fly boxes with precise blue eco movement or clever use
    of game mechanics.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Misty Island Attackless Scout Flies"


class MistyIslandArenaFightSkip(Toggle):
    """
    Create an alternative path to the power cell "Return To The Dark Eco Pool" in Misty Island.

    Enabling this setting may require Jak to reach this power cell with only *Single Jump*.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Misty Island Arena Fight Skip"


class MistyIslandFarSideCliffSeesawSkip(Toggle):
    """
    Create an alternative path to the far side cliff (with scout fly "Scout Fly On Ledge Near Arena Exit") in Misty
    Island.

    Enabling this setting may require Jak to use uneven terrain to find an alternative way to the cliff, using
    only *Single Jump*.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Misty Island Far Side Cliff Seesaw Skip"


class RockVillageSingleJumpOrbCache(Toggle):
    """
    Remove requirements from the orb cache in Rock Village.

    Enabling this setting may require Jak to use precise movement to reach the orb cache with only *Single Jump*.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Rock Village Single Jump Orb Cache"


class RockVillagePontoonSkip(Toggle):
    """
    Create alternative paths to Boggy Swamp and Klaww Cliff in Rock Village.

    Enabling this setting may require Jak to use precise movement to reach these locations without having the
    *Warrior's Pontoons* unlocked.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Rock Village Pontoon Skip"


class KlawwCliffClimb(Toggle):
    """
    Create an alternative path to get up to Klaww from Rock Village.

    Enabling this setting may require Jak to use glitches and uneven terrain to reach Klaww with only *Single Jump*.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Klaww Cliff Climb"


class KlawwBoulderSkip(Toggle):
    """
    Create an alternative path to Klaww without having enough power cells.

    Enabling this setting may require Jak to use glitches to reach Klaww even if the boulder is not lifted.

    This may drastically increase the amount of reachable locations when Rock Village is reachable.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Klaww Boulder Skip"


class BoggySwampPreciseMovement(Toggle):
    """
    Create an alternative path through Boggy Swamp.

    Enabling this setting may require Jak to traverse through the whole Boggy Swamp with only *Single Jump* using
    precise movement, invincibility after taking damage, and respawns.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Boggy Swamp Precise Movement"


class BoggySwampAttacklessAmbush(Toggle):
    """
    Remove the attack requirement from the Boggy Swamp ambush.

    Enabling this setting may require Jak to defeat the lurkers by only shooting yellow Eco through his goggles.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Boggy Swamp Attackless Ambush"


class BoggySwampFlutFlutSkip(Toggle):
    """
    Create an alternative path through the Flut Flut course in Boggy Swamp without having *Flut Flut* unlocked.

    Enabling this setting may require Jak to complete the whole course with only *Roll Jump*, and reach the scout fly
    "Overlooking Flut Flut" with only *Double Jump* or *Jump Kick*.
    """
    display_name = "Boggy Swamp Flut Flut Skip"


class LostPrecursorCitySingleJumpSlideTubeClimb(Toggle):
    """
    Create an alternative path through the helix with the rising dark eco in Lost Precursor City.

    Enabling this setting may require Jak to use precise movement to reach the power cell at the bottom of Lost
    Precursor City and escape the rising dark eco with only *Single Jump*.

    This only applies if "Enable Move Randomizer" is ON.
    """
    display_name = "Lost Precursor City Single Jump Slide Tube Climb"


class SnowyMountainFortGateSkip(Choice):
    """
    Create an alternative path into the Snowy Mountain Fort Gate without having *Snowy Fort Gate* unlocked.

    Enabling this setting may require Jak to use uneven geometry and precise movement, or *Flut Flut* to enter the Fort
    in Snowy Mountain.

    **On Foot**: Fort is reachable after many movement options are unlocked.

    **Flut Flut**: Fort is reachable after *Flut Flut* is unlocked.
    """
    display_name = "Snowy Mountain Fort Gate Skip"

    option_no = 0
    option_on_foot = 1
    option_flut_flut = 2
    option_both = 3

class SentinelBeachBlueEcoSwitchSkip(Toggle):
    """
    Create an alternative path to the blue eco jump pad in Sentinel Beach without having *Blue Eco Switch* unlocked.

    Enabling this setting may require Jak to use precise movement to reach the jump pad with enough blue eco, using
    only *Punch* or only *Roll Jump*.
    """
    display_name = "Sentinel Beach Blue Eco Switch Skip"

class CompletionCondition(Choice):
    """Set the goal for completing the game."""
    display_name = "Completion Condition"
    option_cross_fire_canyon = 69
    option_cross_mountain_pass = 87
    option_cross_lava_tube = 89
    # option_defeat_dark_eco_plant = 6
    option_defeat_klaww = 86
    option_defeat_gol_and_maia = 112
    option_open_100_cell_door = 116
    default = 112


@dataclass
class JakAndDaxterOptions(PerGameCommonOptions):
    enable_move_randomizer: EnableMoveRandomizer
    enable_orbsanity: EnableOrbsanity
    global_orbsanity_bundle_size: GlobalOrbsanityBundleSize
    level_orbsanity_bundle_size: PerLevelOrbsanityBundleSize
    fire_canyon_cell_count: FireCanyonCellCount
    mountain_pass_cell_count: MountainPassCellCount
    lava_tube_cell_count: LavaTubeCellCount
    enable_ordered_cell_counts: EnableOrderedCellCounts
    require_punch_for_klaww: RequirePunchForKlaww
    citizen_orb_trade_amount: CitizenOrbTradeAmount
    oracle_orb_trade_amount: OracleOrbTradeAmount
    filler_power_cells_replaced_with_traps: FillerPowerCellsReplacedWithTraps
    filler_orb_bundles_replaced_with_traps: FillerOrbBundlesReplacedWithTraps
    trap_effect_duration: TrapEffectDuration
    trap_weights: TrapWeights
    boosted_and_extended_uppercuts: BoostedAndExtendedUppercuts
    punch_uppercut_scout_flies: PunchUppercutScoutFlies
    geyser_rock_cliff_climb: GeyserRockCliffClimb
    sentinel_beach_cannon_tower_climb: SentinelBeachCannonTowerClimb
    snowy_mountain_entrance_climb: SnowyMountainEntranceClimb
    boggy_swamp_flut_flut_escape: BoggySwampFlutFlutEscape
    snowy_mountain_flut_flut_escape: SnowyMountainFlutFlutEscape
    snowy_mountain_flut_flut_skip: SnowyMountainFlutFlutSkip
    sandover_village_cliff_orb_cache_climb: SandoverVillageCliffOrbCacheClimb
    attackless_lurker_cannons: AttacklessLurkerCannons
    sentinel_beach_attackless_pelican: SentinelBeachAttacklessPelican
    attack_with_roll_jump: AttackWithRollJump
    forbidden_jungle_attackless_spiral_stumps_scout_fly: ForbiddenJungleAttacklessSpiralStumpsScoutFly
    forbidden_jungle_elevator_skip: ForbiddenJungleElevatorSkip
    misty_island_single_jump_far_side_orb_cache: MistyIslandSingleJumpFarSideOrbCache
    misty_island_attackless_scout_flies: MistyIslandAttacklessScoutFlies
    misty_island_arena_fight_skip: MistyIslandArenaFightSkip
    misty_island_far_side_cliff_seesaw_skip: MistyIslandFarSideCliffSeesawSkip
    rock_village_single_jump_orb_cache: RockVillageSingleJumpOrbCache
    rock_village_pontoon_skip: RockVillagePontoonSkip
    klaww_cliff_climb: KlawwCliffClimb
    klaww_boulder_skip: KlawwBoulderSkip
    boggy_swamp_precise_movement: BoggySwampPreciseMovement
    boggy_swamp_attackless_ambush: BoggySwampAttacklessAmbush
    boggy_swamp_flut_flut_skip: BoggySwampFlutFlutSkip
    lost_precursor_city_single_jump_slide_tube_climb: LostPrecursorCitySingleJumpSlideTubeClimb
    snowy_mountain_fort_gate_skip: SnowyMountainFortGateSkip
    sentinel_beach_blue_eco_switch_skip: SentinelBeachBlueEcoSwitchSkip
    jak_completion_condition: CompletionCondition
    start_inventory_from_pool: StartInventoryPool

jakanddaxter_option_presets: dict[str, dict[str, Any]] = {
    "Move Randomizer + Easy Tricks & Glitches": {
        "enable_move_randomizer": True,
        "attack_with_roll_jump": True,
        "attackless_lurker_cannons": True,
        "sentinel_beach_attackless_pelican": True,
    },
    "Move Randomizer + Medium Tricks & Glitches": {
        "enable_move_randomizer": True,
        "attack_with_roll_jump": True,
        "attackless_lurker_cannons": True,
        "sentinel_beach_attackless_pelican": True,

        "punch_uppercut_scout_flies": True,
        "geyser_rock_cliff_climb": True,
        "sandover_village_cliff_orb_cache_climb": True,
        "sentinel_beach_cannon_tower_climb": SentinelBeachCannonTowerClimb.option_medium,
        "forbidden_jungle_elevator_skip": True,
        "misty_island_single_jump_far_side_orb_cache": True,
        "misty_island_arena_fight_skip": True,
        "misty_island_far_side_cliff_seesaw_skip": True,
        "rock_village_single_jump_orb_cache": True,
        "rock_village_pontoon_skip": True,
        "klaww_cliff_climb": True,
        "klaww_boulder_skip": True,
        "boggy_swamp_precise_movement": True,
        "snowy_mountain_entrance_climb": SnowyMountainEntranceClimb.option_medium,
        "snowy_mountain_flut_flut_skip": True,
    },
    "Move Randomizer + Hard Tricks & Glitches": {
        "enable_move_randomizer": True,
        "attack_with_roll_jump": True,
        "attackless_lurker_cannons": True,
        "sentinel_beach_attackless_pelican": True,

        "punch_uppercut_scout_flies": True,
        "geyser_rock_cliff_climb": True,
        "sandover_village_cliff_orb_cache_climb": True,
        "sentinel_beach_cannon_tower_climb": SentinelBeachCannonTowerClimb.option_hard,
        "forbidden_jungle_elevator_skip": True,
        "misty_island_single_jump_far_side_orb_cache": True,
        "misty_island_arena_fight_skip": True,
        "misty_island_far_side_cliff_seesaw_skip": True,
        "rock_village_single_jump_orb_cache": True,
        "rock_village_pontoon_skip": True,
        "klaww_cliff_climb": True,
        "klaww_boulder_skip": True,
        "boggy_swamp_precise_movement": True,
        "snowy_mountain_entrance_climb": SnowyMountainEntranceClimb.option_hard,
        "snowy_mountain_flut_flut_skip": True,

        "boosted_and_extended_uppercuts": True,
        "sentinel_beach_blue_eco_switch_skip": True,
        "forbidden_jungle_attackless_spiral_stumps_scout_fly": True,
        "misty_island_attackless_scout_flies": True,
        "boggy_swamp_flut_flut_escape": True,
        "boggy_swamp_flut_flut_skip": True,
        "snowy_mountain_flut_flut_escape": True,
    },
    "Move Randomizer + All Tricks & Glitches": {
        "enable_move_randomizer": True,
        "attack_with_roll_jump": True,
        "attackless_lurker_cannons": True,
        "sentinel_beach_attackless_pelican": True,

        "punch_uppercut_scout_flies": True,
        "geyser_rock_cliff_climb": True,
        "sandover_village_cliff_orb_cache_climb": True,
        "sentinel_beach_cannon_tower_climb": SentinelBeachCannonTowerClimb.option_hard,
        "forbidden_jungle_elevator_skip": True,
        "misty_island_single_jump_far_side_orb_cache": True,
        "misty_island_arena_fight_skip": True,
        "misty_island_far_side_cliff_seesaw_skip": True,
        "rock_village_single_jump_orb_cache": True,
        "rock_village_pontoon_skip": True,
        "klaww_cliff_climb": True,
        "klaww_boulder_skip": True,
        "boggy_swamp_precise_movement": True,
        "snowy_mountain_entrance_climb": SnowyMountainEntranceClimb.option_hard,
        "snowy_mountain_flut_flut_skip": True,

        "boosted_and_extended_uppercuts": True,
        "sentinel_beach_blue_eco_switch_skip": True,
        "forbidden_jungle_attackless_spiral_stumps_scout_fly": True,
        "misty_island_attackless_scout_flies": True,
        "boggy_swamp_flut_flut_escape": True,
        "boggy_swamp_flut_flut_skip": True,
        "snowy_mountain_flut_flut_escape": True,

        "boggy_swamp_attackless_ambush": True,
        "lost_precursor_city_single_jump_slide_tube_climb": True,
        "snowy_mountain_fort_gate_skip": SnowyMountainFortGateSkip.option_both,
    }
}
