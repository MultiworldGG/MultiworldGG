from dataclasses import dataclass
from typing import Dict

from Options import PerGameCommonOptions, Range, Toggle


class RandomizerSeed(Range):
    """Seed sent by Archipelago to the in-game randomizer. -1 makes AP generate and send a seed in slot data."""
    display_name = "Randomizer Seed"
    range_start = -1
    range_end = 2147483647
    default = -1

class RandomizeCharacterInitialStats(Toggle):
    """Randomizes initial character stats."""
    display_name = "Randomize Character Initial Stats"
    default = 1

class RandomizeCharacterStatProgression(Toggle):
    """Randomizes character stat progression."""
    display_name = "Randomize Character Stat Progression"
    default = 1

class CharacterSRankStats(Range):
    """Number of S-rank stats assigned during stat progression randomization."""
    display_name = "Character S Rank Stats"
    range_start = 0
    range_end = 8
    default = 0

class CharacterARankStats(Range):
    """Number of A-rank stats assigned during stat progression randomization."""
    display_name = "Character A Rank Stats"
    range_start = 0
    range_end = 8
    default = 3

class CharacterBRankStats(Range):
    """Number of B-rank stats assigned during stat progression randomization."""
    display_name = "Character B Rank Stats"
    range_start = 0
    range_end = 8
    default = 3

class CharacterCRankStats(Range):
    """Number of C-rank stats assigned during stat progression randomization."""
    display_name = "Character C Rank Stats"
    range_start = 0
    range_end = 8
    default = 2

class RandomizeCharacterStatBoosts(Toggle):
    """Randomizes character stat boost nodes."""
    display_name = "Randomize Character Stat Boosts"
    default = 1

class HPStatBoostValueLevel1(Range):
    """HP stat boost value for level 1 nodes."""
    display_name = "HP Stat Boost Value Level 1"
    range_start = 0
    range_end = 999
    default = 10

class HPStatBoostValueLevel2(Range):
    """HP stat boost value for level 2 nodes."""
    display_name = "HP Stat Boost Value Level 2"
    range_start = 0
    range_end = 999
    default = 20

class HPStatBoostValueLevel3(Range):
    """HP stat boost value for level 3 nodes."""
    display_name = "HP Stat Boost Value Level 3"
    range_start = 0
    range_end = 999
    default = 30

class HPStatBoostValueLevel4(Range):
    """HP stat boost value for level 4 nodes."""
    display_name = "HP Stat Boost Value Level 4"
    range_start = 0
    range_end = 999
    default = 40

class TPStatBoostValueLevel1(Range):
    """TP stat boost value for level 1 nodes."""
    display_name = "TP Stat Boost Value Level 1"
    range_start = 0
    range_end = 999
    default = 5

class TPStatBoostValueLevel2(Range):
    """TP stat boost value for level 2 nodes."""
    display_name = "TP Stat Boost Value Level 2"
    range_start = 0
    range_end = 999
    default = 5

class TPStatBoostValueLevel3(Range):
    """TP stat boost value for level 3 nodes."""
    display_name = "TP Stat Boost Value Level 3"
    range_start = 0
    range_end = 999
    default = 5

class TPStatBoostValueLevel4(Range):
    """TP stat boost value for level 4 nodes."""
    display_name = "TP Stat Boost Value Level 4"
    range_start = 0
    range_end = 999
    default = 10

class CoreStatsBoostValueLevel1(Range):
    """Core stat boost value for level 1 nodes."""
    display_name = "Core Stats Boost Value Level 1"
    range_start = 0
    range_end = 999
    default = 2

class CoreStatsBoostValueLevel2(Range):
    """Core stat boost value for level 2 nodes."""
    display_name = "Core Stats Boost Value Level 2"
    range_start = 0
    range_end = 999
    default = 2

class CoreStatsBoostValueLevel3(Range):
    """Core stat boost value for level 3 nodes."""
    display_name = "Core Stats Boost Value Level 3"
    range_start = 0
    range_end = 999
    default = 4

class CoreStatsBoostValueLevel4(Range):
    """Core stat boost value for level 4 nodes."""
    display_name = "Core Stats Boost Value Level 4"
    range_start = 0
    range_end = 999
    default = 6

class AgiStatBoostValueLevel1(Range):
    """Agility stat boost value for level 1 nodes."""
    display_name = "Agi Stat Boost Value Level 1"
    range_start = 0
    range_end = 999
    default = 1

class AgiStatBoostValueLevel2(Range):
    """Agility stat boost value for level 2 nodes."""
    display_name = "Agi Stat Boost Value Level 2"
    range_start = 0
    range_end = 999
    default = 1

class AgiStatBoostValueLevel3(Range):
    """Agility stat boost value for level 3 nodes."""
    display_name = "Agi Stat Boost Value Level 3"
    range_start = 0
    range_end = 999
    default = 1

class AgiStatBoostValueLevel4(Range):
    """Agility stat boost value for level 4 nodes."""
    display_name = "Agi Stat Boost Value Level 4"
    range_start = 0
    range_end = 999
    default = 2

class CritStatBoostValueLevel1(Range):
    """Critical stat boost value for level 1 nodes."""
    display_name = "Crit Stat Boost Value Level 1"
    range_start = 0
    range_end = 999
    default = 4

class CritStatBoostValueLevel2(Range):
    """Critical stat boost value for level 2 nodes."""
    display_name = "Crit Stat Boost Value Level 2"
    range_start = 0
    range_end = 999
    default = 4

class CritStatBoostValueLevel3(Range):
    """Critical stat boost value for level 3 nodes."""
    display_name = "Crit Stat Boost Value Level 3"
    range_start = 0
    range_end = 999
    default = 5

class CritStatBoostValueLevel4(Range):
    """Critical stat boost value for level 4 nodes."""
    display_name = "Crit Stat Boost Value Level 4"
    range_start = 0
    range_end = 999
    default = 6

class RandomizeCharacterEquipment(Toggle):
    """Randomizes character weapon types/equipment setup."""
    display_name = "Randomize Character Equipment"
    default = 1

class RandomizeCharacterPassives(Toggle):
    """Randomizes character passive skills."""
    display_name = "Randomize Character Passives"
    default = 1

class RandomizeCharacterSkills(Toggle):
    """Randomizes character active skills."""
    display_name = "Randomize Character Skills"
    default = 1

class RandomizeMechSkills(Toggle):
    """Randomizes mech skills."""
    display_name = "Randomize Mech Skills"
    default = 1

class RandomizeMechStatBoosts(Toggle):
    """Randomizes mech stat boosts."""
    display_name = "Randomize Mech Stat Boosts"
    default = 1

class RandomizeEmblemStats(Toggle):
    """Randomizes class emblem stats."""
    display_name = "Randomize Emblem Stats"
    default = 1

class RandomizeEmblemSkills(Toggle):
    """Randomizes class emblem skills."""
    display_name = "Randomize Emblem Skills"
    default = 1

class RandomizeEmblemPassives(Toggle):
    """Randomizes class emblem passives."""
    display_name = "Randomize Emblem Passives"
    default = 1

class AddTier1Weapons(Toggle):
    """Adds tier 1 weapons for characters whose weapon type normally starts later."""
    display_name = "Add Tier 1 Weapons"
    default = 1



@dataclass
class ChainedEchoesOptions(PerGameCommonOptions):
    randomizer_seed: RandomizerSeed
    randomize_character_initial_stats: RandomizeCharacterInitialStats
    randomize_character_stat_progression: RandomizeCharacterStatProgression
    character_s_rank_stats: CharacterSRankStats
    character_a_rank_stats: CharacterARankStats
    character_b_rank_stats: CharacterBRankStats
    character_c_rank_stats: CharacterCRankStats
    randomize_character_stat_boosts: RandomizeCharacterStatBoosts
    hp_stat_boost_value_level_1: HPStatBoostValueLevel1
    hp_stat_boost_value_level_2: HPStatBoostValueLevel2
    hp_stat_boost_value_level_3: HPStatBoostValueLevel3
    hp_stat_boost_value_level_4: HPStatBoostValueLevel4
    tp_stat_boost_value_level_1: TPStatBoostValueLevel1
    tp_stat_boost_value_level_2: TPStatBoostValueLevel2
    tp_stat_boost_value_level_3: TPStatBoostValueLevel3
    tp_stat_boost_value_level_4: TPStatBoostValueLevel4
    core_stats_boost_value_level_1: CoreStatsBoostValueLevel1
    core_stats_boost_value_level_2: CoreStatsBoostValueLevel2
    core_stats_boost_value_level_3: CoreStatsBoostValueLevel3
    core_stats_boost_value_level_4: CoreStatsBoostValueLevel4
    agi_stat_boost_value_level_1: AgiStatBoostValueLevel1
    agi_stat_boost_value_level_2: AgiStatBoostValueLevel2
    agi_stat_boost_value_level_3: AgiStatBoostValueLevel3
    agi_stat_boost_value_level_4: AgiStatBoostValueLevel4
    crit_stat_boost_value_level_1: CritStatBoostValueLevel1
    crit_stat_boost_value_level_2: CritStatBoostValueLevel2
    crit_stat_boost_value_level_3: CritStatBoostValueLevel3
    crit_stat_boost_value_level_4: CritStatBoostValueLevel4
    randomize_character_equipment: RandomizeCharacterEquipment
    randomize_character_passives: RandomizeCharacterPassives
    randomize_character_skills: RandomizeCharacterSkills
    randomize_mech_skills: RandomizeMechSkills
    randomize_mech_stat_boosts: RandomizeMechStatBoosts
    randomize_emblem_stats: RandomizeEmblemStats
    randomize_emblem_skills: RandomizeEmblemSkills
    randomize_emblem_passives: RandomizeEmblemPassives
    add_tier_1_weapons: AddTier1Weapons


# Keys expected by the Chained Echoes client when reading AP slot data.
SLOT_DATA_OPTION_NAMES: Dict[str, str] = {
    "RandomizerSeed": "randomizer_seed",
    "RandomizeCharacterInitialStats": "randomize_character_initial_stats",
    "RandomizeCharacterStatProgression": "randomize_character_stat_progression",
    "CharacterSRankStats": "character_s_rank_stats",
    "CharacterARankStats": "character_a_rank_stats",
    "CharacterBRankStats": "character_b_rank_stats",
    "CharacterCRankStats": "character_c_rank_stats",
    "RandomizeCharacterStatBoosts": "randomize_character_stat_boosts",
    "HPStatBoostValueLevel1": "hp_stat_boost_value_level_1",
    "HPStatBoostValueLevel2": "hp_stat_boost_value_level_2",
    "HPStatBoostValueLevel3": "hp_stat_boost_value_level_3",
    "HPStatBoostValueLevel4": "hp_stat_boost_value_level_4",
    "TPStatBoostValueLevel1": "tp_stat_boost_value_level_1",
    "TPStatBoostValueLevel2": "tp_stat_boost_value_level_2",
    "TPStatBoostValueLevel3": "tp_stat_boost_value_level_3",
    "TPStatBoostValueLevel4": "tp_stat_boost_value_level_4",
    "CoreStatsBoostValueLevel1": "core_stats_boost_value_level_1",
    "CoreStatsBoostValueLevel2": "core_stats_boost_value_level_2",
    "CoreStatsBoostValueLevel3": "core_stats_boost_value_level_3",
    "CoreStatsBoostValueLevel4": "core_stats_boost_value_level_4",
    "AgiStatBoostValueLevel1": "agi_stat_boost_value_level_1",
    "AgiStatBoostValueLevel2": "agi_stat_boost_value_level_2",
    "AgiStatBoostValueLevel3": "agi_stat_boost_value_level_3",
    "AgiStatBoostValueLevel4": "agi_stat_boost_value_level_4",
    "CritStatBoostValueLevel1": "crit_stat_boost_value_level_1",
    "CritStatBoostValueLevel2": "crit_stat_boost_value_level_2",
    "CritStatBoostValueLevel3": "crit_stat_boost_value_level_3",
    "CritStatBoostValueLevel4": "crit_stat_boost_value_level_4",
    "RandomizeCharacterEquipment": "randomize_character_equipment",
    "RandomizeCharacterPassives": "randomize_character_passives",
    "RandomizeCharacterSkills": "randomize_character_skills",
    "RandomizeMechSkills": "randomize_mech_skills",
    "RandomizeMechStatBoosts": "randomize_mech_stat_boosts",
    "RandomizeEmblemStats": "randomize_emblem_stats",
    "RandomizeEmblemSkills": "randomize_emblem_skills",
    "RandomizeEmblemPassives": "randomize_emblem_passives",
    "AddTier1Weapons": "add_tier_1_weapons",
}
