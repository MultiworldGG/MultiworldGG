from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet, Range, Toggle, PerGameCommonOptions, StartInventoryPool


# class Goal(Choice):
#     """
#     Set what base game conditions need to be met to complete the game
#
#     Standard Ending: Return artifacts to collector and trigger the ending
#     All Pursuits: Complete all pursuits
#     All Fish Found: Fill out all applicable encyclopedia entries (Including DLCs will add those fish to this goal)
#     """
#     internal_name = "goal"
#     display_name = "Goal"
#     option_standard_ending = 0
#     option_all_pursuits = 1
#     option_all_fish_found = 2
#     default = 0

class IncludeIronRigDLC(Toggle):
    """
    Include the Iron Rig DLC (Iron Rig DLC required for this)
    """
    display_name = "Include Iron Rig DLC"

# class RequireIronRigEnding(Toggle):
#     """
#     Require Iron Rig ending to have been achieved before game can be completed
#     """
#     internal_name = "require_iron_rig_ending"
#     display_name = "Require Iron Rig Ending"

class IncludePaleReachDLC(Toggle):
    """
    Include the Pale Reach DLC (Pale Reach DLC required for this)
    """
    display_name = "Include Pale Reach DLC"

# class RequirePaleReachEnding(Toggle):
#     """
#     Require Pale Reach ending to have been achieved before game can be completed
#     """
#     internal_name = "require_pale_reach_ending"
#     display_name = "Require Pale Reach Ending"

class RequireBoatPerformance(Toggle):
    """
    Set logic to require a fast enough, well lit boat to reach further areas, counting only engines and lights that
    fit in the hull together.

    Gale Cliffs, Stellar Basin, Twisted Strand and Devil's Spine: 50 knots and 1800 lumens
    Open Ocean dredging, fishing and pickups, and the Iron Rig: 50 knots and 2100 lumens
    The Pale Reach: 60 knots and 2100 lumens
    """
    display_name = "Require Boat Performance"

class LogicalNets(Toggle):
    """
    If enabled, logic may expect players to use nets as the only method of catching fish that are also catchable with a
    rod. This includes passive net catches in specific regions.

    If disabled, logic will only consider rod-based access for such fish, ensuring checks are reachable through active
    fishing.

    Recommended: disabled for players who prefer reliable, targeted fishing.
    """
    display_name = "Logical Nets"

class IncludeAberrations(Toggle):
    """
    If enabled, checks for fish aberrations may contain progression items.
    """
    display_name = "Include Aberrations"

class AddFishingLicenses(Toggle):
    """
    If enabled, adds a required item to be able to catch each region's fish.
    """
    display_name = "Add Fishing Licenses"

class AddPassageItems(Toggle):
    """
    If enabled, adds required items to be able to traverse each zone.
    The Windward Litany = Gale Cliffs
    The Astral Testament = Stellar Basin
    The Mangrove Canticle = Twisted Strand
    The Cinder Gospel = Devil's Spine
    The Pelagic Psalm = Open Ocean
    The Rimebound Chronicle = Pale Reach
    """
    display_name = "Add Passage Items"

class IncludeMessageBottles(DefaultOnToggle):
    """
    If enabled, picking up each of the 10 messages in a bottle is a check.
    """
    display_name = "Include Messages in Bottles"

class IncludeResearchChecks(DefaultOnToggle):
    """
    If enabled, researching each piece of equipment at the research station is a check. Research costs nothing in an
    AP save, so these are free checks once the research tree lets you reach them. Research Parts are never in the pool.
    """
    display_name = "Include Research Checks"

class ProgressiveAberrationChanceItems(Range):
    """
    How many Progressive Aberration Chance items to add. Each raises the minimum chance of catching an aberration by
    an equal share, so having all of them makes every catch an aberration. 0 adds none.

    Logic expects at least half of them (or the Guaranteed Aberrations item) before any aberration, or anything that
    needs one, is in logic. With neither item in the pool, aberrations are left to the normal chance.

    The boost can be switched off in game with "ap aberrations off" or in the mod settings.
    """
    display_name = "Progressive Aberration Chance Items"
    range_start = 0
    range_end = 20
    default = 0

class GuaranteedAberrationsItem(Toggle):
    """
    Adds a Guaranteed Aberrations item that makes every catch an aberration as soon as it's received.
    Once received, every aberration is in logic.

    The boost can be switched off in game with "ap aberrations off" or in the mod settings.
    """
    display_name = "Guaranteed Aberrations Item"

TRAP_NAMES = [
    "Damaging Event Trap", "Scary Event Trap", "Money Loss Trap", "Teleport Trap", "Panic Trap", "Hull Damage Trap",
    "Engine Damage Trap", "Nightfall Trap", "Rot Trap", "Slow Trap", "Lights Out Trap", "Cargo Scramble Trap",
    "Reverse Controls Trap",
]

class TrapPercentage(Range):
    """
    The percentage of filler items replaced with traps. 0 adds no traps.
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0

class EnabledTraps(OptionSet):
    """
    Which traps can replace filler.

    Damaging Event Trap: a monster that can damage your boat appears
    Scary Event Trap: something unsettling but harmless happens
    Money Loss Trap: lose 10% of your money
    Teleport Trap: get pulled back to where the Manifest ability takes you
    Panic Trap: your panic rises sharply
    Hull Damage Trap: your boat takes a hit
    Engine Damage Trap: an engine takes damage
    Nightfall Trap: time skips ahead to nightfall
    Rot Trap: a fish in your cargo rots
    Slow Trap: your boat slows down for a short while
    Lights Out Trap: your lights go out for a short while
    Cargo Scramble Trap: your cargo gets rearranged
    Reverse Controls Trap: your steering and throttle are reversed for a short while
    """
    display_name = "Enabled Traps"
    valid_keys = TRAP_NAMES
    default = frozenset(TRAP_NAMES)

class DeathLink(Toggle):
    """
    Enables deathlink
    """
    display_name = "Death Link"

# class EnableTraps(Toggle):
#     """
#     Allow traps to be added to the pool to replace filler items
#     """
#     internal_name = "enable_traps"
#     display_name = "Enable Traps"


@dataclass
class DREDGEOptions(PerGameCommonOptions):
    # goal: Goal
    include_iron_rig_dlc: IncludeIronRigDLC
    # require_iron_rig_ending: RequireIronRigEnding
    include_pale_reach_dlc: IncludePaleReachDLC
    # require_pale_reach_ending: RequirePaleReachEnding
    require_boat_performance: RequireBoatPerformance
    logical_nets: LogicalNets
    include_aberrations: IncludeAberrations
    add_fishing_licenses: AddFishingLicenses
    add_passage_items: AddPassageItems
    include_message_bottles: IncludeMessageBottles
    include_research_checks: IncludeResearchChecks
    progressive_aberration_chance_items: ProgressiveAberrationChanceItems
    guaranteed_aberrations_item: GuaranteedAberrationsItem
    trap_percentage: TrapPercentage
    enabled_traps: EnabledTraps
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
    # enable_traps: EnableTraps
