from typing import List

from dataclasses import dataclass

from Options import (
    Choice,
    DeathLinkMixin,
    DefaultOnToggle,
    OptionGroup,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
)


class Goal(Choice):
    """
    Determines the victory condition.

    Three Artifacts: Retrieve the Coconut of Quendor, the Cube of Foundation and the Skull of Yoruk
    Artifact of Magic Hunt: Retrieve X artifacts of magic and bring them to the walking castle
    Spell Heist: Acquire all spells and travel to the Port Foozle signpost
    Zork Tour: Visit all 23 landmarks and travel to the Port Foozle signpost
    Grim Journey: Experience all 31 player deaths and go beyond the gates of Hades
    """

    display_name: str = "Goal"

    option_three_artifacts: int = 0
    option_artifact_of_magic_hunt: int = 1
    option_spell_heist: int = 2
    option_zork_tour: int = 3
    option_grim_journey: int = 4

    default = 0


class ArtifactsOfMagicTotal(Range):
    """
    Determines how many Artifacts of Magic are in the item pool.

    Only relevant if the selected goal is Artifact of Magic Hunt.
    """

    display_name = "Artifacts of Magic Total"

    range_start = 5
    range_end = 20

    default = 20


class ArtifactsOfMagicRequired(Range):
    """
    Determines how many Artifacts of Magic are required to win.

    Only relevant if the selected goal is Artifact of Magic Hunt.
    """

    display_name = "Artifacts of Magic Required"

    range_start = 5
    range_end = 20

    default = 15


class LandmarksRequired(Range):
    """
    Determines how many Landmarks are required to win.

    Only relevant if the selected goal is Zork Tour.
    """

    display_name = "Landmarks Required"

    range_start = 10
    range_end = 23

    default = 23


class DeathsRequired(Range):
    """
    Determines how many Deaths are required to win.

    Only relevant if the selected goal is Grim Journey.
    """

    display_name = "Deaths Required"

    range_start = 10
    range_end = 31

    default = 31


class StartingLocation(Choice):
    """
    Determines the in-game location the player will start at.

    The player always starts with VOXAM, which can be used to teleport back to the starting location at any time.
    Depending on the starting location, the player may also be given a starter kit of items to help them get going.

    Note: VOXAM will only work from the spell quickbar. It will have no effect from the spellbook.
    """

    display_name: str = "Starting Location"

    option_port_foozle: int = 0
    option_crossroads: int = 1
    option_dm_lair: int = 2
    option_dm_lair_house: int = 3
    option_gue_tech: int = 4
    option_spell_lab: int = 5
    option_hades_shore: int = 6
    option_flood_control_dam_3: int = 7
    option_monastery_totemizer: int = 8
    option_monastery_exhibit: int = 9

    default = "random"


class Hotspots(Choice):
    """
    Determines the behavior of hotspots (interactable areas of the screen) in the game.

    Enabled: All hotspots will be enabled at the start of the game
    Require Item per Region: An item will enable all hotspots for a given region (e.g. Hotspots: Crossroads)
    Require Item per Hotspot: An item will enable a specific hotspot (e.g. Hotspot: Subway Token Slot)
    """

    display_name: str = "Hotspots"

    option_enabled: int = 0
    option_require_item_per_region: int = 1
    option_require_item_per_hotspot: int = 2

    default = 0


class CraftableSpells(Choice):
    """
    Determines the behavior when craftable spells (BEBURTT, OBIDIL, SNAVIG, YASTARD) are obtained.
    Spells in a starting location's starter kit always have precedence over this option.

    Vanilla: After crafting a spell, the player will be given that exact spell
    Any Spell: After crafting a spell, the player will be given a random spell
    Anything: After crafting a spell, a random item from the multiworld will be unlocked
    """

    display_name: str = "Craftable Spells"

    option_vanilla: int = 0
    option_any_spell: int = 1
    option_anything: int = 2

    default = 2


class WildVoxam(Toggle):
    """
    If true, casting VOXAM will have a small chance to teleport the player to a different location.

    This option can enable small stretches of out-of-logic gameplay in the early game, with strong diminishing returns
    as the game progresses.
    """

    display_name: str = "Wild VOXAM"


class WildVoxamChance(Range):
    """
    Determines the percentage chance that a VOXAM cast will be wild.
    """

    display_name = "Wild VOXAM Chance %"

    range_start = 1
    range_end = 10

    default = 5


class Deathsanity(Toggle):
    """
    If true, adds 31 unique player death locations to the world.

    This option will be forced on if your goal is Grim Journey.
    """

    display_name: str = "Deathsanity"


class Landmarksanity(DefaultOnToggle):
    """
    If true, adds 23 landmark locations to the world.

    This option will be forced on if your goal is Zork Tour.
    """

    display_name: str = "Landmarksanity"


class ShuffleTimeTunnels(Toggle):
    """
    If true, shuffles the destination of the three time tunnels. For example, the time tunnel in the Dungeon Master's
    Lair could lead to the Dragon Archipelago instead of the White House.
    """

    display_name: str = "Shuffle Time Tunnels"


class EntranceRandomizer(Choice):
    """
    Determines the behavior of entrances in the game.

    Disabled: Entrances are not randomized and lead to their vanilla areas
    Coupled: Entrances are randomized. Going back through an entrance will lead back to the previous area
    Uncoupled: Entrances are randomized. Going back through an entrance can lead to a different area
    """

    display_name: str = "Entrance Randomizer"

    option_disabled: int = 0
    option_coupled: int = 1
    option_uncoupled: int = 2

    default = 0


class EntranceRandomizerIncludeSubwayDestinations(Toggle):
    """
    If true, the entrance randomizer will include subway destinations in the randomization pool.

    Only relevant if the entrance randomizer is enabled.
    """

    display_name: str = "Entrance Randomizer - Include Subway Destinations"


class TrapPercentage(Range):
    """
    Determines the percentage chance that a trap will replace a filler item.

    Possible traps are:
    - Infinite Corridor Trap: The player is teleported to a random depth in the Infinite Corridor
    - Reverse Controls Trap: The player's panorama controls are reversed for 30 seconds
    - Teleport Trap: The player is teleported to a random location
    - ZVision Trap: The player's vision is distorted for 30 seconds
    """

    display_name = "Trap Percentage"

    range_start = 0
    range_end = 100

    default = 0


class InfiniteCorridorTrapWeight(Range):
    """
    Determines the weight of the Infinite Corridor Trap.

    The higher the weight, the more likely this trap will be chosen when a trap is rolled.
    """

    display_name = "Infinite Corridor Trap Weight"

    range_start = 0
    range_end = 100

    default = 1


class ReverseControlsTrapWeight(Range):
    """
    Determines the weight of the Reverse Controls Trap.

    The higher the weight, the more likely this trap will be chosen when a trap is rolled.
    """

    display_name = "Reverse Controls Trap Weight"

    range_start = 0
    range_end = 100

    default = 1


class TeleportTrapWeight(Range):
    """
    Determines the weight of the Teleport Trap.

    The higher the weight, the more likely this trap will be chosen when a trap is rolled.
    """

    display_name = "Teleport Trap Weight"

    range_start = 0
    range_end = 100

    default = 1


class ZVisionTrapWeight(Range):
    """
    Determines the weight of the ZVision Trap.

    The higher the weight, the more likely this trap will be chosen when a trap is rolled.
    """

    display_name = "ZVision Trap Weight"

    range_start = 0
    range_end = 100

    default = 1


class GrantMissableLocationChecks(Toggle):
    """
    If true, performing an irreversible action will grant the location checks that would have become unobtainable as a
    result of that action as soon as they are in logic.

    Otherwise, the player is expected to potentially have to use the save system to reach those location checks. If you
    don't like the idea of rarely having to reload an earlier save to get a location check, make sure this option is
    enabled.

    Note: This option requires Universal Tracker to be installed alongside the client. Without it, no location checks
    are granted.
    """

    display_name: str = "Grant Missable Checks"


class ClientSeedInformation(Choice):
    """
    Determines what information about the seed the client will reveal after using the /zork command.

    Reveal Nothing: No information about the seed is displayed
    Reveal Goal: Only the goal of the seed is displayed
    Reveal Goal and Options: Both the goal and the options of the seed are displayed
    """

    display_name: str = "Client Seed Information"

    option_reveal_nothing: int = 0
    option_reveal_goal: int = 1
    option_reveal_goal_and_options: int = 2

    default = 2


class InGameOverlay(Choice):
    """
    Determines what information the client displays on top of the game.

    Disabled: Nothing is displayed
    Enabled: Goal progress, received and sent item notifications, trap countdowns and death link announcements are displayed
    Enabled with Tracker: Same as Enabled, plus a list of the locations currently in logic (requires Universal Tracker)
    """

    display_name: str = "In-Game Overlay"

    option_disabled: int = 0
    option_enabled: int = 1
    option_enabled_with_tracker: int = 2

    default = 1


@dataclass
class ZorkGrandInquisitorOptions(PerGameCommonOptions, DeathLinkMixin):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    artifacts_of_magic_total: ArtifactsOfMagicTotal
    artifacts_of_magic_required: ArtifactsOfMagicRequired
    landmarks_required: LandmarksRequired
    deaths_required: DeathsRequired
    starting_location: StartingLocation
    hotspots: Hotspots
    craftable_spells: CraftableSpells
    wild_voxam: WildVoxam
    wild_voxam_chance: WildVoxamChance
    deathsanity: Deathsanity
    landmarksanity: Landmarksanity
    shuffle_time_tunnels: ShuffleTimeTunnels
    entrance_randomizer: EntranceRandomizer
    entrance_randomizer_include_subway_destinations: EntranceRandomizerIncludeSubwayDestinations
    trap_percentage: TrapPercentage
    infinite_corridor_trap_weight: InfiniteCorridorTrapWeight
    reverse_controls_trap_weight: ReverseControlsTrapWeight
    teleport_trap_weight: TeleportTrapWeight
    zvision_trap_weight: ZVisionTrapWeight
    grant_missable_location_checks: GrantMissableLocationChecks
    client_seed_information: ClientSeedInformation
    in_game_overlay: InGameOverlay


option_groups: List[OptionGroup] = [
    OptionGroup(
        "Goal Options",
        [
            Goal,
            ArtifactsOfMagicTotal,
            ArtifactsOfMagicRequired,
            LandmarksRequired,
            DeathsRequired,
        ],
    ),
    OptionGroup(
        "Gameplay Options",
        [
            StartingLocation,
            Hotspots,
            CraftableSpells,
            WildVoxam,
            WildVoxamChance,
            Deathsanity,
            Landmarksanity,
            ShuffleTimeTunnels,
            EntranceRandomizer,
            EntranceRandomizerIncludeSubwayDestinations,
        ],
    ),
    OptionGroup(
        "Trap Options",
        [
            TrapPercentage,
            InfiniteCorridorTrapWeight,
            ReverseControlsTrapWeight,
            TeleportTrapWeight,
            ZVisionTrapWeight,
        ],
    ),
    OptionGroup(
        "Client Options",
        [
            GrantMissableLocationChecks,
            ClientSeedInformation,
            InGameOverlay,
        ],
    ),
]
