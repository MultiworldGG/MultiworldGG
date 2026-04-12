"""Holds additional rules for alternative settings, to be iterated over by the parsing function contained within."""
from typing import Callable, NamedTuple, TYPE_CHECKING
from functools import partial

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule
from .combat import Difficulty
from .rules_helpers import can_fight
from .names import item_names as i
from .names import location_names as l
from .names import region_names as r
from .names import combat_names as c

if TYPE_CHECKING:
    from __init__ import FrogmonsterWorld

class FMAccessData(NamedTuple):
    op: str
    rule: Callable[[int, Difficulty, CollectionState], bool]

def parse_access_rule_group(world: "FrogmonsterWorld", group: dict[str, dict[str, FMAccessData]]) -> None:

    if "locations" in group:
        for location_data in group["locations"].items():
            name = location_data[0]
            access_data = location_data[1]
            location = world.multiworld.get_location(name, world.player)
            if access_data.op == "replace":
                location.access_rule = partial(access_data.rule, world.player, world.difficulty)
            elif access_data.op in ["or", "and"]:
                add_rule(location, partial(access_data.rule, world.player, world.difficulty), combine=access_data.op)
            else:
                raise ValueError(f"Invalid access rule type {access_data.op} for location {name}.")
            
    if "entrances" in group:
        for entrance_data in group["entrances"].items():
            name = entrance_data[0]
            access_data = entrance_data[1]
            entrance = world.multiworld.get_entrance(name, world.player)
            if access_data.op == "replace":
                entrance.access_rule = partial(access_data.rule, world.player, world.difficulty)
            elif access_data.op in ["or", "and"]:
                add_rule(entrance, partial(access_data.rule, world.player, world.difficulty), combine=access_data.op)
            else:
                raise ValueError(f"Invalid access rule type {access_data.op} for entrance {name}.") 

access_rule_groups = {
    "parkour_rules": {
        "locations": {
            l.sparkling_gem_1: FMAccessData(op="replace", rule=lambda player, dif, state: True),  # There's a mushroom in the poison fields you can stand on just off to the side of the chest.
            l.metal_ore_10: FMAccessData(op="or", rule=lambda player, dif, state: state.has_all([i.sticky_hands, i.dash, i.cricket], player)),  # A well-timed wavedash and cricket can bypass the tongue swing.
            l.sparkling_gem_2: FMAccessData(op="replace", rule=lambda player, dif, state: True),  # There's a part of the tree that you can stand on. Jump to it from Trench's house.
        },
        "entrances": {
            f"{r.hive} -> {r.treetops}": FMAccessData(op="or", rule=lambda player, dif, state: can_fight(c.hive_general, player, dif, state) and state.has(i.dash, player)),  # Climb on top of the hive to get height.
            f"{r.hive} -> {r.cicada_cove}": FMAccessData(op="or", rule=lambda player, dif, state: can_fight(c.hive_general, player, dif, state) and state.has(i.dash, player)),  # Climb on top of the hive to get height.
            f"{r.forest_floor} -> {r.treetops}": FMAccessData(op="or", rule=lambda player, dif, state: can_fight(c.forest_floor_general, player, dif, state) and state.has(i.mushbomb, player))  # Rocket jump to the top of the tree.
        }
    },
    "deathlink_rules": {
        "entrances": {
            f"{r.anywhere} -> Soul Frog": FMAccessData(op="replace", rule=lambda player, dif, state: False),
            f"{r.anywhere} -> Soul Fish": FMAccessData(op="replace", rule=lambda player, dif, state: False),
        }
    },
    "goal_eye_chest_rules": {
        "locations": {
            l.goal: FMAccessData(op="replace", rule=lambda player, dif, state: True)
        }
    }
}
