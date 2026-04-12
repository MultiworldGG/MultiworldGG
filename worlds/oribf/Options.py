from dataclasses import dataclass

from Options import Toggle, Choice, Range, OptionSet, PerGameCommonOptions

class Goal(OptionSet):
    """Choose the end goal. You may choose multiple
    AllSkillTrees: Find all 10 skill trees (including Kuro's feather)
    AllMaps: Place all 9 mapstones around the map
    WarmthFragments: Collect the required number of Warmth Fragments
    WorldTour: Collect the required number of Relics. Up to 11 areas (default 8) around Nibel will be chosen to contain a relic in a random location
    """
    display_name = "Goal"
    valid_keys = {
        "AllSkillTrees",
        "AllMaps",
        "WarmthFragments",
        "WorldTour"
    }
    default = {
        "AllSkillTrees"
    }

class RequireFinalEscape(Toggle):
    """Whether or not the final escape in Mount Horu is required to goal
    If true, the final escape will need to be completed. The door to the escape will only open once other all other goals are complete.
    If false, the player only needs to reach the escape door once all other goals are complete"""
    display_name = "Require Final Escape"
    default = 1

class WarmthFragmentsAvailable(Range):
    """The number of Warmth Fragments that exist"""
    display_name = "Warmth Fragments Available"
    range_start = 1
    range_end = 50
    default = 30

class WarmthFragmentsRequired(Range):
    """The number of Warmth Fragments needed for the goal"""
    display_name = "Warmth Fragments Required"
    range_start = 1
    range_end = 50
    default = 20

class RelicCount(Range):
    """The number of areas chosen to contain Relics"""
    display_name = "Relic Count"
    range_start = 1
    range_end = 11
    default = 8

class LogicDifficulty(Choice):
    """Sets the difficulty of the logic"""
    display_name = "Difficulty"
    option_casual = 0
    option_standard = 1
    option_expert = 2
    option_master = 3
    default = 0

class KeystoneLogic(Choice):
    """Choose how keystones can be used.
    Anywhere: All keystones can be used anywhere.
    Area Specific: Keystones are restricted to be used only in their given area."""
    display_name = "Keystone Logic"
    option_anywhere = 0
    option_area_specific = 1
    default = 0

class MapstoneLogic(Choice):
    """Choose how mapstones can be used.
    Anywhere: All mapstones can be used anywhere.
    Area Specific: Mapstones are restricted to be used only in their given area.
    Progressive: Similar to anywhere, but it doesn't matter where the mapstone is used.
        The first mapstone used will always send ProgressiveMapstone1 and the last will send ProgressiveMapstone9"""
    display_name = "Mapstone Logic"
    option_anywhere = 0
    option_area_specific = 1
    option_progressive = 2
    default = 0

class IncludeTeleporters(Toggle):
    """Whether or not teleporters are included in the item pool"""
    display_name = "Include Teleporters"
    default = 1

class ExtraSkills(Toggle):
    """Adds an extra copy of each of the skills. Also adds an extra copy of Clean Water and Wind"""
    display_name = "Extra Skills"
    default = 0

class ExtraKeystones(Range):
    """Adds extra keystones to the pool to make them easier to get. Affects anywhere and area specific logic
    Due to differences between anywhere and area specific counts, this acts as a percentage to add to the base.
    Ex. at 50%, 40 keystones (anywhere logic) becomes 60 keystones 
        and 8 Ginso keystones (area specific logic) becomes 12 Ginso keystones"""
    display_name = "Extra Keystones"
    range_start = 0
    range_end = 100
    default = 0

class ExtraMapstones(Range):
    """Adds extra mapstones to the pool to make it easier to get the 9 required. Affects anywhere and progressive mapstone logic"""
    display_name = "Extra Mapstones"
    range_start = 0
    range_end = 9
    default = 0

class DeathLinkLogic(Choice):
    """Enable Death Link
    Disabled: Death Link is disabled
    Partial: Death Link is enabled, but will not send a death for any instant kill deaths.
    Full: Death Link is enabled, and will send for every death"""
    display_name = "Death Link"
    option_disabled = 0
    option_partial = 1
    option_full = 2
    default = 0

class DeathLinkCount(Range):
    """How many deaths are allowed before sending a death link
    Has no effect if death link is disabled"""
    display_name = "Death Link Count"
    range_start = 1
    range_end = 30
    default = 1

class SeinLogic(Choice):
    """How to place Sein in the multiworld
    Vanilla: Sein is placed at the normal location
    Start: Adds Sein to the starting inventory"""
    display_name = "Sein Logic"
    option_vanilla = 0
    option_start = 1
    default = 0

class LogicModifiers(OptionSet):
    """Additional modifiers to add to the base logic difficulty. Some options only affect higher difficulties.
    The default is all modifiers are enabled except for Glitches.

    - Lure: Allows luring enemies to be considered for logic. 
    Affects standard and above, but higher difficulties may require more difficult lures.
    
    - DamageBoost: Allows taking damage to be considered for logic. 
    Affects all difficulties, but higher difficulties may require more damage. Use of Ultra Defense ability limited to master. 
    At least 12 ability cells will be in logic before needing to use this ability.
    
    - DoubleBash: Allows double bash technique to be considered for logic. Affects expert and above.
    
    - GrenadeJump: Allows grenade jump technique to be considered for logic. Affects master.
    
    - AirDash: Allows air dash ability to be considered for logic. Affects standard and above. 
    At least 3 ability cells will be in logic before needing to use this ability.
    
    - ChargeDash: Allows charge dash ability to be considered for logic. Affects expert and above. 
    At least 6 ability cells will be in logic before needing to use this ability.
    
    - TripleJump: Allows triple jump ability to be considered for logic. Only affects master. 
    At least 12 ability cells will be in logic before needing to use this ability.
    
    - ChargeFlameBurn: Allows charge flame burn ability to be considered for logic. Only affects master. 
    At least 3 ability cells will be in logic before needing to use this ability.
    
    - Rekindle: Allows rekindle ability to be considered for logic. Only affects standard, expert, and master
    for specifically the Ghost Lever trick in Blackroot Burrows
    
    - Glitches: Allows glitches to be considered for logic. Affects all logic difficulties
    """
    display_name = "Logic Modifiers"
    valid_keys = {
        "Lure",
        "DamageBoost",
        "DoubleBash",
        "GrenadeJump",
        "AirDash",
        "ChargeDash",
        "TripleJump",
        "ChargeFlameBurn",
        "Rekindle",
        "Glitches"
    }
    default = {
        "Lure",
        "DamageBoost",
        "DoubleBash",
        "GrenadeJump",
        "AirDash",
        "ChargeDash",
        "TripleJump",
        "ChargeFlameBurn",
        "Rekindle"
    }

class RestrictDungeonKeys(Toggle):
    """Due to teleporters, it is possible for dungeon keys (ex. GinsoKey) to end up placed inside 
    their dungeon. This option prevents those keys from being placed there"""
    display_name = "Restrict Dungeon Keys"
    default = 0

@dataclass
class OriBlindForestOptions(PerGameCommonOptions):
    goal: Goal
    require_final_escape: RequireFinalEscape
    warmth_fragments_available: WarmthFragmentsAvailable
    warmth_fragments_required: WarmthFragmentsRequired
    relic_count: RelicCount
    logic_difficulty: LogicDifficulty
    keystone_logic: KeystoneLogic
    mapstone_logic: MapstoneLogic
    include_teleporters: IncludeTeleporters
    extra_keystones: ExtraKeystones
    extra_mapstones: ExtraMapstones
    extra_skills: ExtraSkills
    deathlink_logic: DeathLinkLogic
    deathlink_count: DeathLinkCount
    sein_logic: SeinLogic
    logic_modifiers: LogicModifiers
    restrict_dungeon_keys: RestrictDungeonKeys

# determines which options are passed through to the slot data
slot_data_options: list[str] = [
    "goal",
    "require_final_escape",
    "warmth_fragments_available",
    "warmth_fragments_required",
    "relic_count",
    "logic_difficulty",
    "keystone_logic",
    "mapstone_logic",
    "deathlink_logic",
    "deathlink_count",
    "logic_modifiers"
]
