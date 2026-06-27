from typing import TypedDict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification

from .Names import SkillNames, JunkNames, UsefulNames
from .Names.DLC import ExpansionNames, GamePackNames, StuffNames


class ItemDict(TypedDict):
    classification: ItemClassification
    count: int
    name: str
    tech_type: str
    expansion: str


class ItemData(NamedTuple):
    code: Optional[int]
    progression: bool


class Sims4Item(Item):
    game: str = "The Sims 4"


skills_table: dict[int, ItemDict] = {}


class SkillConfigError(ValueError):
    """Raised when skill configuration is invalid."""


def add_skill(skill_name: str, expansion: str, max_level: int) -> int:
    if max_level < 2:
        raise SkillConfigError(f"max_level must be at least 2, got {max_level}")
    if skills_table:
        skill_id = max(skills_table.keys()) + 1
    else:
        skill_id = 0x7334001

    skills_table[skill_id] = {
        "name": skill_name,
        "classification": ItemClassification.progression,
        "count": max_level - 2,
        "tech_type": "Skill",
        "expansion": expansion
        }
    return skill_id


add_skill(SkillNames.base_skill_comedy, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_guitar, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_logic, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_piano, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_violin, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_charisma, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_cooking, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_fishing, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_fitness, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_gardening, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_gourmet, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_handiness, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_mischief, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_mixology, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_painting, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_programming, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_rocket_science, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_video_gaming, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_writing, ExpansionNames.base, 10)
add_skill(SkillNames.base_skill_photography, ExpansionNames.base, 5)
add_skill(SkillNames.or_herbalism_skill, GamePackNames.outdoor_retreat, 10)
add_skill(SkillNames.gtw_baking_skill, ExpansionNames.get_to_work, 10)
add_skill(SkillNames.sd_wellness_skill, GamePackNames.spa_day, 10)
add_skill(SkillNames.gt_dancing_skill, ExpansionNames.get_together, 5)
add_skill(SkillNames.gt_djmixing_skill, ExpansionNames.get_together, 10)
add_skill(SkillNames.cl_singing_skill, ExpansionNames.city_living, 10)
add_skill(SkillNames.vamp_pipeorgan_skill, GamePackNames.vampires, 10)
add_skill(SkillNames.vamp_vampirelore_skill, GamePackNames.vampires, 15)
add_skill(SkillNames.bns_bowling_skill, StuffNames.bowling_night, 5)
add_skill(SkillNames.ph_parenting_skill, GamePackNames.parenthood, 10)
add_skill(SkillNames.cnd_pettraining_skill, ExpansionNames.cats_and_dogs, 5)
add_skill(SkillNames.cnd_veterinarian_skill, ExpansionNames.cats_and_dogs, 10)
add_skill(SkillNames.ja_archaeology_skill, GamePackNames.jungle_adventure, 10)
add_skill(SkillNames.ja_sevadoradianculture_skill, GamePackNames.jungle_adventure, 5)
add_skill(SkillNames.se_flowerarranging_skill, ExpansionNames.seasons, 10)
add_skill(SkillNames.gf_acting_skill, ExpansionNames.get_famous, 10)
add_skill(SkillNames.gf_mediaproduction_skill, ExpansionNames.get_famous, 5)
add_skill(SkillNames.du_researchanddebate_skill, ExpansionNames.discover_university, 10)
add_skill(SkillNames.du_robotics_skill, ExpansionNames.discover_university, 10)
add_skill(SkillNames.el_fabrication_skill, ExpansionNames.eco_lifestyle, 10)
add_skill(SkillNames.el_juicefizzing_skill, ExpansionNames.eco_lifestyle, 5)
add_skill(SkillNames.nk_knitting_skill, StuffNames.nifty_knitting, 10)
add_skill(SkillNames.sy_rock_climbing_skill, ExpansionNames.snowy_escape, 10)
add_skill(SkillNames.sy_skiing_skill, ExpansionNames.snowy_escape, 10)
add_skill(SkillNames.sy_snowboarding_skill, ExpansionNames.snowy_escape, 10)
add_skill(SkillNames.pa_medium_skill, StuffNames.paranormal, 5)
add_skill(SkillNames.cgl_cross_stitch_skill, ExpansionNames.cottage_living, 5)
add_skill(SkillNames.hsy_entrepreneur_skill, ExpansionNames.high_school_years, 5)
add_skill(SkillNames.hr_horse_riding_skill, ExpansionNames.horse_ranch, 10)
add_skill(SkillNames.hr_nectar_making_skill, ExpansionNames.horse_ranch, 5)
add_skill(SkillNames.cc_gemology_skill, StuffNames.crystal_creations, 10)
add_skill(SkillNames.lv_romance_skill, ExpansionNames.lovestruck, 10)
add_skill(SkillNames.lnd_thanatology_skill, ExpansionNames.life_and_death, 5)
add_skill(SkillNames.bnh_pottery_skill, ExpansionNames.business_and_hobbies, 10)
add_skill(SkillNames.bnh_tattooing_skill, ExpansionNames.business_and_hobbies, 10)
add_skill(SkillNames.ebn_apothecary_skill, ExpansionNames.enchanted_by_nature, 10)
add_skill(SkillNames.ebn_natural_living_skill, ExpansionNames.enchanted_by_nature, 10)

useful_table: dict[int, ItemDict] = {
    0x733400FF: {'classification': ItemClassification.useful,
                 'count': 4,
                 'name': UsefulNames.skill_gain_boost,
                 'tech_type': 'Skill Gain Multiplier',
                 'expansion': 'base'},

}

junk_table: dict[int, ItemDict] = {
    0x73340FFF: {'classification': ItemClassification.filler,
                 'count': 0,
                 'name': JunkNames.twothousand_simoleons,
                 'tech_type': 'Simoleons',
                 'expansion': 'base'},
    0x73340FFE: {'classification': ItemClassification.filler,
                 'count': 0,
                 'name': JunkNames.fivethousand_simoleons,
                 'tech_type': 'Simoleons',
                 'expansion': 'base'},
    0x73340FFD: {'classification': ItemClassification.filler,
                 'count': 0,
                 'name': JunkNames.career_performance_boost,
                 'tech_type': 'Career Boost',
                 'expansion': 'base'},
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
