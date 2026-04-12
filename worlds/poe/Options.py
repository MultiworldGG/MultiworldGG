from dataclasses import dataclass, fields, Field
from typing import FrozenSet, Union, Set

from Options import Choice, Toggle, DefaultOnToggle, ItemSet, OptionSet, Range, PerGameCommonOptions, DeathLinkMixin, \
    OptionGroup
from worlds.AutoWorld import World
from worlds.poe import Locations

#--- Goal Options ---

class Goal(Choice):
    """
    Specifies the goal of the world.
    if your goal is act 5, you need to get to the 3rd area in act 6, kauri fortress, because of zone names.
    """
    display_name = "Goal"
    option_complete_the_campaign = 0
    option_complete_act_1 = 1
    option_complete_act_2 = 2
    option_complete_act_3 = 3
    option_complete_act_4 = 4
    option_kauri_fortress_act_6 = 5
    option_complete_act_6 = 6
    option_complete_act_7 = 7
    option_complete_act_8 = 8
    option_complete_act_9 = 9
    alias_complete_act_10 = 0
    option_defeat_bosses = 10
    default = 0

class NumberOfBosses(Range):
    """
    This is ignored if Goal isn't set to defeat_bosses. This specifies the number of bosses that need to be defeated
    (and for you to pick up their drops) in order for you to goal. This will max out at the number of bosses available in the world.
    """
    display_name = "Bosses to kill (if Goal is set Defeat Bosses)"
    range_start = 1
    range_end = len(Locations.bosses.values())
    default = 1

class BossesAvailable(OptionSet):
    """
    This is also ignored if Goal isn't set to defeat_bosses. Specifies the availability of the bosses in the world.
    This will NOT determine how many bosses are available in the world, but rather which bosses can be randomized.
    This will choose any (including _very_ difficult bosses if none are selected.)

    valid choices: [ "hydra", "phoenix", "chimera", "minotaur", "shaper", "uber_shaper", "elder", "uber_elder",
     "uber_uber_elder", "atziri", "al-hezmin", "baran", "drox", "veritania", "sirus", "uber_sirus", "maven",
     "uber_maven", "exarch", "uber_exarch", "eater", "uber_eater", "incarnation_of_neglect", "incarnation_of_fear",
     "incarnation_of_dread", "cortex", "uber_cortex"]
    """
    display_name = "Bosses Available"
    valid_keys = Locations.bosses.keys()
    default = [
        key for key in valid_keys
        if Locations.bosses[key].get('difficulty', 'Guardian') not in {'Uber', 'Pinnacle'}
    ]

#--- Character Options ---

class StartingCharacter(Choice):
    """
    The starting character for the world. This will determine the class available at the start.
    """
    display_name = "Starting Character"
    option_scion       = 1
    option_marauder    = 2
    option_ranger      = 3
    option_witch       = 4
    option_duelist     = 5
    option_templar     = 6
    option_shadow      = 7
    default = "random"

class AscendanciesAvailablePerClass(Range):
    """
    Specifies the maximum number of available ascendancies per class.
    """
    display_name = "Ascendancies Available Per Class"
    range_start = 0
    range_end = 3
    default = 1

class AllowUnlockOfOtherCharacters(Toggle):
    """
    Allows unlocking of other characters.
    """
    display_name = "Allow Unlock of Other Characters"
    default = True

class UsableStartingGear(Choice):
    """
    Specifies if you should start with the gear that you find in the tutorial, for your starting character.
    use this option if you don't want to punch hillock to death.
    """
    display_name = "Usable Starting Gear"
    option_no_starting_gear = 0
    option_starting_weapon = 1
    option_starting_weapon_and_flask_slots = 2
    option_starting_weapon_and_gems = 3
    option_starting_weapon_flask_and_gems = 4
    default = 4

class GucciHoboMode(Choice):
    """
    Specifies if the world should be in Gucci Hobo Mode, this restricts use of any non-unique equipment to only 1 slot.
    This is an extremely difficult challenge intended for experienced players, and will greatly increase the length of your run.
    Expect a very slow start, involving farming early act 1 zones.
    """
    display_name = "Gucci Hobo Mode"
    option_disabled = 0
    option_allow_one_slot_of_any_rarity = 1
    option_allow_one_slot_of_normal_rarity = 2
    option_no_non_unique_items = 3
    default = 0

#--- Generation Options ---

class DisableGenerationLogic(Toggle):
    """
    Disables all generation logic, ignoring any placement rules, and placing items completely randomly. This ignores all other "Minimum Available" Options.
    This will likely make your run very difficult, and is not recommended.
    """
    display_name = "Disable Generation Logic"
    default = False

class ProgressiveGear(Choice):
    """
    Controls whether gear rarity follows a progressive unlock system. Progressive gear is recommended for better game balance and pacing.
    When enabled, you'll receive gear upgrades that will increase in rarity.
    When disabled, you can receive gear of any rarity (you might find rare items before normal ones).
    """
    display_name = "Progressive Gear"
    option_enabled = 1
    option_disabled = 0
    option_progressive_except_for_unique = 2
    default = 1

class GearUpgrades(Choice):
    """
    Specifies if gear rarity should be restricted to a certain rarity, unlockable through items found in the multiworld.
    """
    display_name = "Gear Unlocks"
    option_all_gear_unlocked_at_start = 0
    option_all_normal_and_unique_gear_unlocked = 1
    option_all_normal_gear_unlocked = 2
    option_all_uniques_unlocked = 3
    option_no_gear_unlocked = 4
    default = 4

class GearUpgradesPerAct(Range):
    """
    Specifies a minimum number of rarity of gear upgrades available per act. (there are 38 total)
    This will be ignored if the "Gear Upgrades" option is turned off.
    """
    display_name = "Minimum Available Gear Upgrades Per Act"
    range_start = 0
    range_end = 38
    default = 5

class AddFlasksToItemPool(Toggle):
    """
    Specifies if flasks should be restricted, unlockable through items found in the multiworld.
    You may equip up to 5 flasks of a given rarity, and can unlock more flasks of a rarity through items.
    """
    display_name = "Restricted Flasks"
    default = True

class FlasksPerAct(Range):
    """
    Specifies a minimum number of available flask slots per act. (there are 5 total)
    This will be ignored if the "Flask Slots" option is turned off.
    """
    display_name = "Minimum Available Flask Slots Per Act"
    range_start = 0
    range_end = 5
    default = 3

class AddMaxLinksToItemPool(Toggle):
    """
    Specifies if the number of linked support gem slots you can use in gear should be restricted, unlockable through items found in the multiworld.
    """
    display_name = "Restricted Linked Support Gem"
    default = True

class MaxLinksPerAct(Range):
    """
    Specifies a minimum number of available linked support gem slots per act. (there are 22 total)
    This will be ignored if the "Support Gem Slot Upgrades" option is turned off.
    """
    display_name = "Minimum Available Support Gem Slots Per Act"
    range_start = 0
    range_end = 22
    default = 3

class AddPassiveSkillPointsToItemPool(Toggle):
    """
    Specifies if passive skill points should be restricted, unlockable through items found in the multiworld.
    """
    display_name = "Restricted Passive Skill Points"
    default = True

class AddLevelingUpToLocationPool(Toggle):
    """
    Specifies if leveling up be considered "locations".
    """
    display_name = "Leveling Up as location checks"
    default = True

class AddSkillGemsToItemPool(Toggle):
    """
    Specifies if skill gems should be restricted, unlockable through items found in the multiworld.
    """
    display_name = "Restricted Skill Gems"
    default = True

class SkillGemsPerAct(Range):
    """
    Specifies the minimum number of usable skill gems placed by the generator per act.
    Higher values will place more relevant skill gems early on
    """
    display_name = "Minimum Available Skill Gem Slots Per Act"
    range_start = 0
    range_end = 15
    default = 2

class AddSupportGemsToItemPool(Toggle):
    """
    Specifies if skill gems should be restricted, unlockable through items found in the multiworld.
    """
    display_name = "Restricted Support Gems"
    default = True

class SupportGemsPerAct(Range):
    """
    Specifies the minimum number of usable support gems (by character level) placed by the generator per act.
    """
    display_name = "Minimum Usable Support Gems Per Act"
    range_start = 0
    range_end = 10
    default = 2


#--- Client Options ---

class LootFilterSounds(Choice):
    """
    sounds for the Archipelago items drop.
    """
    display_name = "Loot filter drop sounds."
    option_no_sound = 0
    option_TTS = 1
    option_jingles = 2
    default = 2

class LootFilterDisplay(Choice):
    """
    Loot filter display style.
    """
    display_name = "Loot filter display style."
    option_show_classification = 0
    option_hide_classification = 1
    option_randomize_lootfilter_style = 2
    default = 0

class EnableTTS(DefaultOnToggle):
    """
    Enable Text-to-Speech (TTS). If using other loot filter sounds, this option will still generate TTS audio files for invalid state warnings.
    If this is disabled, this will ignore Loot Filter Sounds if set to TTS.
    If TTS is enabled, the client will generate audio files for item drops that are not already present,
    This may take some time initially, but will speed as audio files are generated and saved.
    """
    display_name = "Enable TTS"
    default = True

class TTSSpeed(Range):
    """
    Speed of the Text-to-Speech (TTS) feature, if enabled.
    """
    display_name = "TTS Speed"
    range_start = 50
    range_end = 500
    default = 250

poe_options_groups = [
    OptionGroup("Goal Options", [
        Goal,
        NumberOfBosses,
        BossesAvailable,
    ]),
    OptionGroup("Character Options", [
        StartingCharacter,
        AscendanciesAvailablePerClass,
        AllowUnlockOfOtherCharacters,

        UsableStartingGear,
        GucciHoboMode,
    ]),
    OptionGroup("Generation Options", [
        ProgressiveGear,
        DisableGenerationLogic,
        
        GearUpgrades,
        GearUpgradesPerAct,

        AddFlasksToItemPool,
        FlasksPerAct,

        AddMaxLinksToItemPool,
        MaxLinksPerAct,

        AddPassiveSkillPointsToItemPool,
        AddLevelingUpToLocationPool,

        AddSkillGemsToItemPool,
        SkillGemsPerAct,

        AddSupportGemsToItemPool,
        SupportGemsPerAct,
    ]),
    OptionGroup("Client Options", [
        LootFilterSounds,
        LootFilterDisplay,
        EnableTTS,
        TTSSpeed,
    ]),
]

all_characters = {
    "Ascendant" : 1,
    "Reliquarian": 1,
    "Berserker" : 1,
    "Chieftain" : 1,
    "Juggernaut" : 1,
    "Champion" : 1,
    "Gladiator" : 1,
    "Slayer" : 1,
    "Deadeye" : 1,
    "Pathfinder" : 1,
    "Warden" : 1,
    "Assassin" : 1,
    "Saboteur" : 1,
    "Trickster" : 1,
    "Elementalist" : 1,
    "Necromancer" : 1,
    "Occultist" : 1,
    "Guardian" : 1,
    "Hierophant" : 1,
    "Inquisitor" : 1,
    "Scion": 1,
    "Marauder": 1,
    "Duelist": 1,
    "Ranger": 1,
    "Shadow": 1,
    "Witch": 1,
    "Templar": 1,
}

guardian_bosses = [
            key for key in Locations.bosses.keys()
            if Locations.bosses[key].get('difficulty', 'Guardian') not in {'Uber', 'Pinnacle'}
]
pinnacle_bosses = [
            key for key in Locations.bosses.keys()
            if Locations.bosses[key].get('difficulty', 'Pinnacle') not in {'Uber', 'Guardian'}
]
uber_bosses = [
            key for key in Locations.bosses.keys()
            if Locations.bosses[key].get('difficulty', 'Uber') not in {'Pinnacle', 'Guardian'}
]

existing_char_preset_option = {
    "add_passive_skill_points_to_item_pool": True,
    "add_leveling_up_to_location_pool": False,
    "start_inventory": all_characters,
    "gear_upgrades": GearUpgrades.option_no_gear_unlocked,
}

poe_presets = {
    "Existing Character - Guardian Boss Rush": {
        "goal": Goal.option_defeat_bosses,
        "number_of_bosses": 3,
        "bosses_available": guardian_bosses,
    } | existing_char_preset_option,
    "Existing Character - Pinnacle Boss Rush": {
        "goal": Goal.option_defeat_bosses,
        "number_of_bosses": 3,
        "bosses_available": pinnacle_bosses,
    } | existing_char_preset_option,
    "Existing Character - Uber Boss Rush": {
        "goal": Goal.option_defeat_bosses,
        "number_of_bosses": 3,
        "bosses_available": uber_bosses,
    } | existing_char_preset_option,
    "Guardian Boss Rush": {
        "goal": Goal.option_defeat_bosses,
        "number_of_bosses": 3,
        "bosses_available": guardian_bosses
    },
    "Pinnacle Boss Rush": {
        "goal": Goal.option_defeat_bosses,
        "number_of_bosses": 3,
        "bosses_available": pinnacle_bosses
    },
    "Uber Boss Rush": {
        "goal": Goal.option_defeat_bosses,
        "number_of_bosses": 3,
        "bosses_available": uber_bosses
    },

    "Quick Sync": {
        "goal": Goal.option_complete_act_1,
    },
    "Impossible": {
        "number_of_bosses": 6,
        "bosses_available": ["uber_uber_elder", "uber_sirus", "uber_maven", "uber_exarch", "uber_eater", "uber_cortex"],
        "gear_upgrades": GearUpgrades.option_no_gear_unlocked,
        "usable_starting_gear":UsableStartingGear.option_no_starting_gear,
        "add_passive_skill_points_to_item_pool": True,
        "add_leveling_up_to_location_pool": True,
        "add_flasks_to_item_pool": True,
        "add_max_links_to_item_pool": True,
        "ascendancies_available_per_class": 0,
        "allow_unlock_of_other_characters": False,
        "gucci_hobo_mode": GucciHoboMode.option_no_non_unique_items,
        "death_link": True,
    }
}

@dataclass
class PathOfExileOptions(DeathLinkMixin, PerGameCommonOptions):
    """
    Common options for Path of Exile.
    """
    goal: Goal
    number_of_bosses: NumberOfBosses
    bosses_available: BossesAvailable

    starting_character: StartingCharacter
    ascendancies_available_per_class: AscendanciesAvailablePerClass
    allow_unlock_of_other_characters: AllowUnlockOfOtherCharacters
    usable_starting_gear: UsableStartingGear
    gucci_hobo_mode: GucciHoboMode

    progressive_gear: ProgressiveGear
    disable_generation_logic: DisableGenerationLogic
    
    gear_upgrades: GearUpgrades
    gear_upgrades_per_act: GearUpgradesPerAct

    add_flasks_to_item_pool: AddFlasksToItemPool
    flasks_per_act: FlasksPerAct

    add_max_links_to_item_pool: AddMaxLinksToItemPool
    max_links_per_act: MaxLinksPerAct

    add_passive_skill_points_to_item_pool: AddPassiveSkillPointsToItemPool
    add_leveling_up_to_location_pool: AddLevelingUpToLocationPool

    add_skill_gems_to_item_pool: AddSkillGemsToItemPool
    skill_gems_per_act: SkillGemsPerAct

    add_support_gems_to_item_pool: AddSupportGemsToItemPool
    support_gems_per_act: SupportGemsPerAct

    loot_filter_sounds: LootFilterSounds
    loot_filter_display: LootFilterDisplay
    enable_tts: EnableTTS
    tts_speed: TTSSpeed



def option_starting_character_to_class_name(option_id: int) -> str:
    mapping = {
        1: "Scion",
        2: "Marauder", 
        3: "Ranger",
        4: "Witch",
        5: "Duelist",
        6: "Templar",
        7: "Shadow",
    }
    return mapping.get(option_id, "Unknown")
