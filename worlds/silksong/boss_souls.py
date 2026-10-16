from __future__ import annotations

import json
import pkgutil
from dataclasses import replace

from BaseClasses import ItemClassification
from Options import OptionError

BOSS = "Boss: Groal the Great"
SOUL = "Soul of Groal the Great"
SETH_SOUL = "Progressive Seth Soul"
SETH_BOSS = "Boss: Shrine Guardian Seth"
EVENT = "Room Event: event:mapper/c072b5f9-82a5-469b-8bf6-b91bb53e5180"

CATALOGUE = tuple(json.loads(pkgutil.get_data(__package__, "boss_souls.json")))
BY_BOSS = {row["boss"]: row for row in CATALOGUE}
BOSS_EVENTS = {row["boss"]: row["events"][0] if row["events"] else None for row in CATALOGUE}


def item_name(boss):
    name = "Skull Tyrant" if boss.startswith("Boss: Skull Tyrant (") else boss.removeprefix("Boss: ")
    return "Soul of " + name


def progressive_seth(world):
    from .npc_souls import enabled_npcs
    return SETH_BOSS in enabled_bosses(world) and "Seth" in enabled_npcs(world)


def pool_item_name(world, boss):
    return SETH_SOUL if boss == SETH_BOSS and progressive_seth(world) else item_name(boss)


def enabled_bosses(world):
    if not bool(getattr(getattr(world.options, "boss_souls", None), "value", 0)):
        return ()
    passthrough = getattr(world.multiworld, "re_gen_passthrough", {}).get(world.game)
    if passthrough is not None:
        validate_slot_data(passthrough)
        return tuple(passthrough.get("boss_soul_bosses", ()))
    excluded = world.get_goal_excluded_location_names()
    act = int(world.get_content_scope().removeprefix("act_"))
    return tuple(row["boss"] for row in CATALOGUE if row["boss"] not in excluded and row.get("act", 1) <= act)


def gate(world, rules, boss=BOSS):
    if boss not in enabled_bosses(world):
        return rules
    soul = pool_item_name(world, boss)
    return tuple(replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, soul)))) for rule in rules)


def gate_location(world, name, rules):
    return gate(world, rules, name) if name in BOSS_EVENTS else rules


def requires_bell_beast_for_travel(world):
    return (world.get_bellway_access_key() == "bell_beast_required"
            and "Boss: Bell Beast" in enabled_bosses(world))


def gate_graph(world, graph):
    bosses = enabled_bosses(world)
    if not bosses:
        return graph
    result = dict(graph)
    for boss in bosses:
        row = BY_BOSS[boss]
        for name in (*row["events"], *row["combat"]):
            if name not in result:
                raise OptionError(f"Boss Souls needs {name} in the room graph.")
            result[name] = gate(world, result[name], boss)
    if requires_bell_beast_for_travel(world):
        result["Path: Bellways"] = gate(world, result["Path: Bellways"], "Boss: Bell Beast")
    return result


def add_souls_to_pool(world, entries):
    bosses = enabled_bosses(world)
    if not bosses:
        return
    from .items import ItemPoolEntry, item_data_table
    indices = [index for index, entry in enumerate(entries)
               if entry.placement_category is None
               and item_data_table[entry.name].classification == ItemClassification.filler
               and entry.source_category not in {"Memento", "MemoryLocket", "Journal"}]
    souls = tuple(dict.fromkeys(pool_item_name(world, boss) for boss in bosses))
    if len(indices) < len(souls):
        raise OptionError(f"Boss Souls needs {len(souls)} anywhere filler slots; only {len(indices)} are available. "
                          "Enable another anywhere category.")
    for soul, index in zip(souls, world.random.sample(indices, len(souls))):
        entries[index] = ItemPoolEntry(soul, "BossSoul")


def prepare_start(world):
    from BaseClasses import CollectionState

    if (world.get_starting_location_key() != "vanilla" or world.options.entrance_randomization
            or getattr(world.multiworld, "re_gen_passthrough", {}).get(world.game) is not None):
        return
    early = world.multiworld.local_early_items[world.player]
    dash_name = "Progressive Swift Step" if world.is_split_dash_and_sprint() else "Swift Step"
    if not early.get(dash_name):
        return
    required = []
    if 'Boss: Moss Mother' in enabled_bosses(world):
        required.append(item_name('Boss: Moss Mother'))
    if not required:
        return
    state = CollectionState(world.multiworld)
    state.sweep_for_advancements(world.get_locations())
    locations = [location for location in world.get_locations()
                 if location.item is None and location.can_reach(state)]
    required = [name for name in required if not state.has(name, world.player)]
    early_count = sum(early.values()) + sum(world.multiworld.early_items[world.player].values())
    if not required or len(locations) > early_count + len(required):
        return
    pool = world.multiworld.itempool
    planned = []
    for name in (*required, dash_name):
        item = next((item for item in pool if item.player == world.player and item.name == name), None)
        candidates = [location for location in world.get_locations()
                      if location.item is None and location not in [loc for loc, _ in planned]
                      and item is not None and location.can_fill(state, item)]
        if not candidates:
            raise OptionError("Souls cannot place the opening encounter souls followed by Early Dash with these settings.")
        planned.append((world.random.choice(candidates), item))
        state.collect(item, True)
        state.sweep_for_advancements(world.get_locations())
    for location, item in planned:
        location.place_locked_item(item)
        pool.remove(item)
    early[dash_name] -= 1
    if not early[dash_name]:
        del early[dash_name]
    world._soul_opening_locations = tuple(location for location, _ in planned)


def export_world(world, slot_data):
    from .requirements import _export_requirement_group
    bosses = enabled_bosses(world)
    slot_data["boss_soul_bosses"] = list(bosses)
    slot_data["boss_souls"] = bool(world.options.boss_souls.value)
    if requires_bell_beast_for_travel(world):
        slot_data["abstract_requirements"]["Path: Bellways"] = _export_requirement_group(
            world._silksong_native_abstract_requirements["Path: Bellways"])
    for boss in bosses:
        for rule in slot_data["requirements"].get(boss, {}).get("alternatives", ()):
            if pool_item_name(world, boss) not in rule["all_of"]:
                rule["all_of"].append(pool_item_name(world, boss))
        row = BY_BOSS[boss]
        for name in (*row["events"], *row["combat"]):
            slot_data["abstract_requirements"][name] = _export_requirement_group(
                world._silksong_native_abstract_requirements[name])


def location_overrides(world, rules):
    from .requirements import get_location_requirements, REQUIREMENTS
    result = dict(rules)
    for boss in enabled_bosses(world):
        if boss not in REQUIREMENTS:
            continue
        result[boss] = gate(world, rules.get(boss, get_location_requirements(boss)), boss)
    return result


def validate_slot_data(slot_data):
    bosses = slot_data.get("boss_soul_bosses", [])
    if (not isinstance(bosses, list) or any(not isinstance(name, str) for name in bosses)
            or len(set(bosses)) != len(bosses) or any(name not in BOSS_EVENTS for name in bosses)):
        raise ValueError("Unsupported Boss Souls configuration.")
    if bosses and not slot_data.get("boss_souls", False):
        raise ValueError("Boss Souls setting does not match its enabled bosses.")
    if slot_data.get("boss_souls", False) and "boss_soul_bosses" not in slot_data:
        raise ValueError("Boss Souls configuration is missing.")
