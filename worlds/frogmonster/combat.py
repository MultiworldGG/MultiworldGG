from typing import NamedTuple
from enum import Enum
from functools import total_ordering

from .names import item_names as i
from .names import combat_names as c

@total_ordering
class Difficulty(Enum):
    EASY = 0
    NORMAL = 1
    HARD = 2
    VERY_HARD = 3
    HYPOTHETICALLY_POSSIBLE = 4  # Would like to implement this sometime.
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value

class CombatType(NamedTuple): 
    name: str
    score_easy: int
    score_normal: int
    score_hard: int
    score_very_hard: int
    need: list[str] = []
    want: list[str] = []
    tags: list[str] = []

def score_undefined():
    raise NotImplementedError("A combat has not been scored yet.")

X = 0

combat_data = [
    CombatType(name=c.marvin_arena_1,          score_easy=X, score_normal=0, score_hard=-4, score_very_hard=0, tags=["stationary"]),
    CombatType(name=c.outskirts_arena_1,       score_easy=X, score_normal=1, score_hard=-2, score_very_hard=0,),
    CombatType(name=c.very_lost_swamp_general, score_easy=X, score_normal=0, score_hard=-3, score_very_hard=0,),
    CombatType(name=c.very_lost_swamp_arena_1, score_easy=X, score_normal=X, score_hard=-2, score_very_hard=0,),
    CombatType(name=c.yellow_forest_general,   score_easy=X, score_normal=X, score_hard=-1, score_very_hard=0,),
    CombatType(name=c.yellow_forest_arena_1,   score_easy=X, score_normal=X, score_hard=0,  score_very_hard=0,),
    CombatType(name=c.yellow_forest_arena_2,   score_easy=X, score_normal=X, score_hard=2,  score_very_hard=0,),
    CombatType(name=c.green_sea_arena_1,       score_easy=X, score_normal=X, score_hard=-1, score_very_hard=0, tags=["underwater", "swarm"]),
    CombatType(name=c.green_sea_arena_3,       score_easy=X, score_normal=X, score_hard=4,  score_very_hard=X, tags=["underwater", "swarm"]),
    CombatType(name=c.under_city_arena_1,      score_easy=X, score_normal=0, score_hard=-2, score_very_hard=0, tags=["swarm"]),
    CombatType(name=c.forest_floor_general,    score_easy=X, score_normal=0, score_hard=-1, score_very_hard=0,),
    CombatType(name=c.forest_floor_arena_1,    score_easy=X, score_normal=X, score_hard=0,  score_very_hard=0,),
    CombatType(name=c.treetops_general,        score_easy=X, score_normal=0, score_hard=0,  score_very_hard=0,),
    CombatType(name=c.treetops_arena_1,        score_easy=X, score_normal=X, score_hard=0,  score_very_hard=0,),
    CombatType(name=c.treetops_arena_2,        score_easy=X, score_normal=0, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.old_road_general,        score_easy=X, score_normal=X, score_hard=0,  score_very_hard=0,),
    CombatType(name=c.old_road_arena_1,        score_easy=X, score_normal=X, score_hard=2,  score_very_hard=0,),
    CombatType(name=c.old_road_arena_2,        score_easy=X, score_normal=X, score_hard=2,  score_very_hard=0,),
    CombatType(name=c.old_wood_general,        score_easy=X, score_normal=X, score_hard=0,  score_very_hard=0,),
    CombatType(name=c.old_wood_arenas,         score_easy=X, score_normal=X, score_hard=3,  score_very_hard=0,),
    CombatType(name=c.estate_general,          score_easy=X, score_normal=X, score_hard=3,  score_very_hard=0,),
    CombatType(name=c.fog_garden_general,      score_easy=X, score_normal=X, score_hard=2,  score_very_hard=0,),
    CombatType(name=c.fog_garden_arena_1,      score_easy=X, score_normal=X, score_hard=3,  score_very_hard=0,),
    CombatType(name=c.fog_garden_arena_2,      score_easy=X, score_normal=X, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.hive_general,            score_easy=X, score_normal=X, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.well_general_upper,      score_easy=X, score_normal=X, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.well_general_lower,      score_easy=X, score_normal=X, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.thickness_general,       score_easy=X, score_normal=X, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.thickness_arena_1,       score_easy=X, score_normal=X, score_hard=5,  score_very_hard=0,),
    CombatType(name=c.ridge_general,           score_easy=X, score_normal=X, score_hard=2,  score_very_hard=0,),
    CombatType(name=c.moridonos_general,       score_easy=X, score_normal=X, score_hard=2,  score_very_hard=0,),
    CombatType(name=c.moridonos_arena_1,       score_easy=X, score_normal=X, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.moridonos_arena_2,       score_easy=X, score_normal=X, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.moridonos_arena_3,       score_easy=X, score_normal=X, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.moridonos_arena_4,       score_easy=X, score_normal=X, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.under_under_general,     score_easy=X, score_normal=X, score_hard=1,  score_very_hard=0,),
    CombatType(name=c.under_under_arena_1,     score_easy=X, score_normal=X, score_hard=4,  score_very_hard=0,),
    CombatType(name=c.deep_general,            score_easy=X, score_normal=X, score_hard=2,  score_very_hard=0,),
    CombatType(name=c.deep_arena_1,            score_easy=X, score_normal=X, score_hard=5,  score_very_hard=0,),
    CombatType(name=c.reef_arena_1,            score_easy=X, score_normal=X, score_hard=5,  score_very_hard=0,),
    CombatType(name=c.reef_general,            score_easy=X, score_normal=X, score_hard=2,  score_very_hard=0,),
    CombatType(name=c.rootden_general,         score_easy=X, score_normal=X, score_hard=3,  score_very_hard=0, need=[i.tongue_swing]),
    CombatType(name=c.quarry_general,          score_easy=X, score_normal=X, score_hard=2,  score_very_hard=0,),
    CombatType(name=c.quarry_arena_1,          score_easy=X, score_normal=X, score_hard=5,  score_very_hard=0,),
    CombatType(name=c.temple_general,          score_easy=X, score_normal=X, score_hard=3,  score_very_hard=0,),

    CombatType(name=c.groth,                   score_easy=1, score_normal=0, score_hard=-4, score_very_hard=0,),
    CombatType(name=c.marvin,                  score_easy=X, score_normal=0, score_hard=-3, score_very_hard=0, tags=["stationary"]),
    CombatType(name=c.snake,                   score_easy=X, score_normal=1, score_hard=-2, score_very_hard=0,),
    CombatType(name=c.yanoy,                   score_easy=X, score_normal=X, score_hard=-1, score_very_hard=0,),
    CombatType(name=c.placeholder,             score_easy=X, score_normal=X, score_hard=7,  score_very_hard=X, need=[i.dash]),
    CombatType(name=c.limbs,                   score_easy=X, score_normal=X, score_hard=0,  score_very_hard=0,),
    CombatType(name=c.eels,                    score_easy=X, score_normal=X, score_hard=3,  score_very_hard=0, tags=["underwater"]),
    CombatType(name=c.xoto,                    score_easy=X, score_normal=X, score_hard=0,  score_very_hard=0, need=[i.dash, i.sticky_hands]),
    CombatType(name=c.valda,                   score_easy=X, score_normal=X, score_hard=5,  score_very_hard=X, need=[i.dash], tags=["stationary"]),
    CombatType(name=c.djumbo,                  score_easy=X, score_normal=X, score_hard=6,  score_very_hard=X, need=[i.dash]),
    CombatType(name=c.dekula,                  score_easy=X, score_normal=X, score_hard=5,  score_very_hard=X,),
    CombatType(name=c.chroma,                  score_easy=X, score_normal=X, score_hard=0,  score_very_hard=0, need=[i.dash]),
    CombatType(name=c.tymbal,                  score_easy=X, score_normal=X, score_hard=5,  score_very_hard=0, need=[i.dash], want=[i.sticky_hands], tags=["swarm"]),
    CombatType(name=c.foraz,                   score_easy=X, score_normal=X, score_hard=6,  score_very_hard=X, need=[i.dash]),
    CombatType(name=c.hedgeward,               score_easy=X, score_normal=X, score_hard=6,  score_very_hard=X, need=[i.dash]),
    CombatType(name=c.runi,                    score_easy=X, score_normal=X, score_hard=6,  score_very_hard=X, need=[i.dash]),
    CombatType(name=c.barge,                   score_easy=X, score_normal=X, score_hard=0,  score_very_hard=X,),
    CombatType(name=c.door_crab,               score_easy=X, score_normal=X, score_hard=8,  score_very_hard=X, need=[i.dash]),
    CombatType(name=c.lazaro,                  score_easy=X, score_normal=X, score_hard=8,  score_very_hard=X, need=[i.dash]),
    CombatType(name=c.zythida,                 score_easy=X, score_normal=X, score_hard=8,  score_very_hard=X, need=[i.tongue_swing, i.dash],),
    CombatType(name=c.krogar,                  score_easy=X, score_normal=X, score_hard=8,  score_very_hard=X, tags=["underwater"]),
    CombatType(name=c.moridono,                score_easy=X, score_normal=X, score_hard=8,  score_very_hard=X,),
    CombatType(name=c.brothers,                score_easy=X, score_normal=X, score_hard=8,  score_very_hard=X, need=[i.dash]),
    CombatType(name=c.myzand_1,                score_easy=X, score_normal=X, score_hard=10, score_very_hard=X, need=[i.dash, i.tongue_swing, i.sticky_hands]),
    CombatType(name=c.myzand_2,                score_easy=X, score_normal=X, score_hard=10, score_very_hard=X, need=[i.dash]),
    CombatType(name=c.mud,                     score_easy=X, score_normal=X, score_hard=7, score_very_hard=X, need=[i.dash]),
    CombatType(name=c.borp,                    score_easy=X, score_normal=X, score_hard=7, score_very_hard=X, need=[i.dash]),
    CombatType(name=c.balsam,                  score_easy=X, score_normal=X, score_hard=7, score_very_hard=X, need=[i.dash]),
]

secret_synergies = {
    i.fireball: i.cicada,
    i.beans: i.mushfrog,
    i.mushbomb: i.blue_jelly,
    i.hive: i.dragonfly,
    i.puff: i.moth,
    i.sharp_shot: i.axolotyl,
    i.zap: i.eel,
    i.slam: i.turtle
}

tanky_bugs = {
    i.turtle,
    i.blue_snack,
    i.beet,
    i.moth
}

mana_bugs = {
    i.wormy,
    i.blue_jelly,
    i.purple_snack,
    i.roof_snail
}