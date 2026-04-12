from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle


class GameVersion(Choice):
    """Set the game version you will be playing on

    - **sotfs:** You will be playing the Scholar of the First Sin version
    - **vanilla:** You will be playing the Vanilla version"""
    display_name = "Game Version"
    option_sotfs = 0
    option_vanilla = 1
    default = 0


class OldIronKingDLC(Toggle):
    """Enable Crown of the Old Iron King DLC."""
    display_name = "Enable Crown of the Old Iron King DLC"


class IvoryKingDLC(Toggle):
    """Enable Crown of the Ivory King DLC."""
    display_name = "Enable Crown of the Ivory King DLC"


class SunkenKingDLC(Toggle):
    """Enable Crown of the Sunken King DLC."""
    display_name = "Enable Crown of the Sunken King DLC"

class CombatLogic(Choice):
    """
    Determines the distribution of Estus Flask Shards and Sublime Bone Dust.
    Easy - Most shards/dust available fairly early on
    Medium - Moderate amount of shards/dust available early in the game
    Hard - There is minimal logical requirement for shards/dust to be available before the end of the game
    Disabled - There is zero requirements for shards/dust anywhere; Lost Bastille is Sphere 1 in Scholar, and Sinners' Rise is Sphere 1 in vanilla.
    """
    display_name = "Combat Logic"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_disabled = 3
    default = option_medium

class KeepInfiniteLifegems(Toggle):
    """Keep Melentia's infinite supply of lifegems unrandomized"""
    display_name = "Keep Infinite Lifegems"


class NoWeaponRequirements(Toggle):
    """Remove the requirements to wield weapons"""
    display_name = "No Weapon Requirements"


class NoSpellRequirements(Toggle):
    """Remove the requirements to cast spells"""
    display_name = "No Spell Requirements"


class NoArmorRequirements(Toggle):
    """Remove the requirements to wear armor"""
    display_name = "No Armor Requirements"


class NoEquipLoad(Toggle):
    """Disable the equip load constraint from the game."""
    display_name = "No Equip Load"


class RandomizeEquipmentLevelPercentageOption(Range):
    """The percentage of weapons and armor in the pool to be reinforced."""
    display_name = "Percentage of Randomized Weapons"
    range_start = 0
    range_end = 100
    default = 33


class MinEquipmentReinforcementIn5Option(Range):
    """The minimum reinforcement level for equipment that can only reach +5."""
    display_name = "Minimum Reinforcement of +5 Equipment"
    range_start = 1
    range_end = 5
    default = 1


class MaxEquipmentReinforcementIn5Option(Range):
    """The maximum reinforcement level for equipment that can only reach +5."""
    display_name = "Maximum Reinforcement of +5 Equipment"
    range_start = 1
    range_end = 5
    default = 5


class MinEquipmentReinforcementIn10Option(Range):
    """The minimum reinforcement level for equipment that can only reach +10."""
    display_name = "Minimum Reinforcement of +10 Equipment"
    range_start = 1
    range_end = 10
    default = 1


class MaxEquipmentReinforcementIn10Option(Range):
    """The maximum reinforcement level for equipment that can only reach +10."""
    display_name = "Maximum Reinforcement of +10 Equipment"
    range_start = 1
    range_end = 10
    default = 10


class EarlyBlacksmith(Choice):
    """Force Lenigrast's key into an early sphere in your world or across all worlds."""
    display_name = "Early Blacksmith"
    option_anywhere = 0
    option_early_global = 1
    option_early_local = 2
    default = option_early_local


option_groups = [
    OptionGroup("Game Options", [
        GameVersion,
        SunkenKingDLC,
        OldIronKingDLC,
        IvoryKingDLC
    ]),

    OptionGroup("Equipment", [
        NoWeaponRequirements,
        NoSpellRequirements,
        NoArmorRequirements,
        NoEquipLoad,

        RandomizeEquipmentLevelPercentageOption,
        MinEquipmentReinforcementIn5Option,
        MaxEquipmentReinforcementIn5Option,
        MinEquipmentReinforcementIn10Option,
        MaxEquipmentReinforcementIn10Option
    ]),


    OptionGroup("Quality of Life", [
        KeepInfiniteLifegems,
        EarlyBlacksmith,
        CombatLogic
    ]),
]


@dataclass
class DarkSouls2Options(PerGameCommonOptions):
    game_version: GameVersion
    sunken_king_dlc: SunkenKingDLC
    old_iron_king_dlc: OldIronKingDLC
    ivory_king_dlc: IvoryKingDLC

    no_weapon_req: NoWeaponRequirements
    no_spell_req: NoSpellRequirements
    no_armor_req: NoArmorRequirements
    no_equip_load: NoEquipLoad

    randomize_equipment_level_percentage: RandomizeEquipmentLevelPercentageOption
    min_equipment_reinforcement_in_5: MinEquipmentReinforcementIn5Option
    max_equipment_reinforcement_in_5: MaxEquipmentReinforcementIn5Option
    min_equipment_reinforcement_in_10: MinEquipmentReinforcementIn10Option
    max_equipment_reinforcement_in_10: MaxEquipmentReinforcementIn10Option

    combat_logic: CombatLogic
    infinite_lifegems: KeepInfiniteLifegems
    early_blacksmith: EarlyBlacksmith
