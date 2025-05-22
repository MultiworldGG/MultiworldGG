from typing import TypedDict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification

from .Names import SkillNames, JunkNames, UsefulNames

class ItemDict(TypedDict):
    classification: ItemClassification
    count: int
    name: str
    tech_type: str


class ItemData(NamedTuple):
    code: Optional[int]
    progression: bool


class Sims4Item(Item):
    game: str = "The Sims 4"


skills_table: dict[int, ItemDict] = {
    0x73340001: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_comedy,
                 'tech_type': 'Skill'},
    0x73340002: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_guitar,
                 'tech_type': 'Skill'},
    0x73340003: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_logic,
                 'tech_type': 'Skill'},
    0x73340004: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_piano,
                 'tech_type': 'Skill'},
    0x73340005: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_charisma,
                 'tech_type': 'Skill'},
    0x73340006: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_cooking,
                 'tech_type': 'Skill'},
    0x73340007: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_fishing,
                 'tech_type': 'Skill'},
    0x73340008: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_fitness,
                 'tech_type': 'Skill'},
    0x73340009: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_gardening,
                 'tech_type': 'Skill'},
    0x7334000A: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_gourmet,
                 'tech_type': 'Skill'},
    0x7334000B: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_handiness,
                 'tech_type': 'Skill'},
    0x7334000C: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_mischief,
                 'tech_type': 'Skill'},
    0x7334000D: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_mixology,
                 'tech_type': 'Skill'},
    0x7334000E: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_painting,
                 'tech_type': 'Skill'},
    0x7334000F: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_programming,
                 'tech_type': 'Skill'},
    0x73340010: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_rocket_science,
                 'tech_type': 'Skill'},
    0x73340011: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_video_gaming,
                 'tech_type': 'Skill'},
    0x73340012: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_violin,
                 'tech_type': 'Skill'},
    0x73340013: {'classification': ItemClassification.progression,
                 'count': 8,
                 'name': SkillNames.base_skill_writing,
                 'tech_type': 'Skill'},
    0x73340014: {'classification': ItemClassification.progression,
                 'count': 4,
                 'name': SkillNames.base_skill_photography,
                 'tech_type': 'Skill'}
}
useful_table = {
    0x733400FF: {'classification': ItemClassification.useful,
                 'count': 4,
                 'name': UsefulNames.skill_gain_boost,
                 'tech_type': 'Skill Gain Multiplier'}

}

junk_table = {
    0x73340FFF: {'classification': ItemClassification.filler,
                 'count': 0,
                 'name': JunkNames.twothousand_simoleons,
                 'tech_type': 'Simoleons'},
    0x73340FFE: {'classification': ItemClassification.filler,
                 'count': 0,
                 'name': JunkNames.fivethousand_simoleons,
                 'tech_type': 'Simoleons'},
    0x73340FFD: {'classification': ItemClassification.filler,
                 'count': 0,
                 'name': JunkNames.career_performance_boost,
                 'tech_type': 'Career Boost'},
}

item_table = {
    **junk_table,
    **useful_table,
    **skills_table
}

filler_set: set[str] = set()

for item_id, item_data in junk_table.items():
    item_name = item_data["name"]
    filler_set.add(item_name)
