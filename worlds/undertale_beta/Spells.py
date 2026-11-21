from dataclasses import dataclass
import math
import typing


@dataclass
class _undertale_procedural_spell:
    effect_one: str = "none"
    effect_two: str = "none"
    atk_add: float = 0.0
    atk_sub: float = 0.0
    atk_mult: float = 0.0
    atk_div: float = 1.0
    def_add: float = 0.0
    def_sub: float = 0.0
    def_mult: float = 0.0
    def_div: float = 1.0
    hp_add: float = 0.0
    hp_sub: float = 0.0
    hp_mult: float = 0.0
    hp_div: float = 1.0
    lv_add: float = 0.0
    lv_sub: float = 0.0
    lv_mult: float = 0.0
    lv_div: float = 1.0
    total_add: float = 0.0
    total_sub: float = 0.0
    total_mult: float = 0.0
    total_div: float = 1.0
    soul_mode_length: int = 0
    target_def_add: float = 0.0
    target_def_sub: float = 0.0
    target_def_mult: float = 0.0
    target_def_div: float = 1.0
    tp_cost: float = 0.0

spell_effects = {
    "heal": 5,
    "over_heal": 16,
    "damage_target": 5,
    "damage_all": 10,
    "target_defense_reduction": 6,
    "brave_defense": 20,
    "patient_regen": 25,
    "pacify_target": 45,
    "self_defense_reduction": 10,
}

targeting_spell_effects = [
    "damage_target",
    "damage_all",
]

numerical_spell_effects = [
    "heal",
    "over_heal",
    "damage_target",
    "damage_all",
    "target_defense_reduction",
    "self_defense_reduction",
]

soul_spell_effects = [
    "brave_defense",
    "patient_regen",
]
