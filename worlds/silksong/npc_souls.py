from __future__ import annotations

import json
import pkgutil
from dataclasses import replace

from BaseClasses import ItemClassification
from Options import OptionError

CATALOGUE = tuple(json.loads(pkgutil.get_data(__package__, 'npc_souls.json')))
BY_NAME = {row['name']: row for row in CATALOGUE}


def item_name(npc):
    return 'NPC Soul: ' + npc


def soul_requirement(world, npc):
    from .boss_souls import SETH_SOUL, progressive_seth
    return (SETH_SOUL, 2) if npc == "Seth" and progressive_seth(world) else (item_name(npc), 1)


def enabled_npcs(world):
    if not world.options.npc_souls:
        return ()
    passthrough = getattr(world.multiworld, 're_gen_passthrough', {}).get(world.game)
    if passthrough is not None:
        validate_slot_data(passthrough)
        return tuple(passthrough.get('npc_soul_npcs', ()))
    act = int(world.get_content_scope().removeprefix("act_"))
    return tuple(row["name"] for row in CATALOGUE if not row.get("legacy") and row.get("act", 1) <= act)


def validate_slot_data(data):
    names = data.get('npc_soul_npcs', [])
    if (not isinstance(names, list) or any(not isinstance(n, str) for n in names)
            or len(set(names)) != len(names) or any(n not in BY_NAME for n in names)):
        raise ValueError('Unsupported NPC Souls configuration.')
    if names and not data.get('npc_souls', False):
        raise ValueError('NPC Souls setting does not match its enabled NPCs.')
    if data.get('npc_souls', False) and 'npc_soul_npcs' not in data:
        raise ValueError('NPC Souls configuration is missing.')


def location_gate(world, name):
    from rule_builder.rules import CanReachRegion, Has
    from .room_graph_logic import native_region_name
    result = None
    for npc in enabled_npcs(world):
        if name not in BY_NAME[npc]['checks']:
            continue
        soul, count = soul_requirement(world, npc)
        rule = Has(soul, count)
        if name in BY_NAME[npc].get('act_3_fallbacks', ()):
            rule = rule | CanReachRegion(native_region_name('Act: 3'))
        result = rule if result is None else result & rule
    return result


def gate(world, name, rules, field):
    npcs = tuple(npc for npc in enabled_npcs(world) if name in BY_NAME[npc][field])
    if not npcs:
        return rules
    result = []
    for rule in rules:
        from .requirements import item_count
        souls = tuple(soul_requirement(world, npc) for npc in npcs if not (
            'Act: 3' in rule.all_of and name in BY_NAME[npc].get('act_3_fallbacks', ())))
        result.append(replace(rule,
            all_of=tuple(dict.fromkeys((*rule.all_of, *(soul for soul, count in souls if count == 1)))),
            item_counts=tuple(dict.fromkeys((*rule.item_counts,
                *(item_count(count, soul) for soul, count in souls if count > 1))))))
    return tuple(result)


def gate_location(world, name, rules):
    from .requirements import req
    alternatives = tuple(req(event, crest=False) for npc in enabled_npcs(world)
                         for event in BY_NAME[npc].get('alternatives', {}).get(name, ()))
    return alternatives or gate(world, name, rules, 'checks')


def gate_graph(world, graph):
    if not enabled_npcs(world):
        return graph
    missing = {name for npc in enabled_npcs(world) for name in BY_NAME[npc]['events']} - graph.keys()
    if missing:
        raise OptionError('NPC Souls is missing mapped interaction events: ' + ', '.join(sorted(missing)))
    return {name: gate(world, name, rules, 'events') for name, rules in graph.items()}


def add_souls_to_pool(world, entries):
    from .items import ItemPoolEntry, item_data_table
    npcs = enabled_npcs(world)
    if not npcs:
        return
    indices = [i for i, e in enumerate(entries) if e.placement_category is None
               and item_data_table[e.name].classification == ItemClassification.filler
               and e.source_category not in {'Memento', 'MemoryLocket', 'Journal'}]
    if len(indices) < len(npcs):
        raise OptionError(f'NPC Souls needs {len(npcs)} anywhere filler slots; only {len(indices)} remain. '
                          'Enable more anywhere cache or resource checks.')
    for npc, i in zip(npcs, world.random.sample(indices, len(npcs))):
        entries[i] = ItemPoolEntry(soul_requirement(world, npc)[0], 'NpcSoul')


def export_world(world, slot_data):
    npcs = enabled_npcs(world)
    slot_data['npc_souls'] = bool(world.options.npc_souls)
    slot_data['npc_soul_npcs'] = list(npcs)
    if not npcs:
        return
    from .requirements import _export_requirement_group
    affected = {name for npc in npcs for name in (*BY_NAME[npc]['checks'], *BY_NAME[npc].get('alternatives', {}))}
    overrides = location_overrides(world, world._progression_location_rules)
    for name in affected:
        if name in slot_data['requirements']:
            rules = overrides[name]
            group = _export_requirement_group(rules)
            if name in world.get_logic_unknown_locations():
                group['logic_unknown'] = True
            slot_data['requirements'][name] = group
    for npc in npcs:
        for name in BY_NAME[npc]['events']:
            slot_data['abstract_requirements'][name] = _export_requirement_group(
                world._silksong_native_abstract_requirements[name])


def location_overrides(world, rules):
    from .requirements import get_location_requirements, REQUIREMENTS
    result = dict(rules)
    for npc in enabled_npcs(world):
        for name in (*BY_NAME[npc]['checks'], *BY_NAME[npc].get('alternatives', {})):
            original = rules.get(name)
            if original is None:
                original = get_location_requirements(name) if name in REQUIREMENTS else ()
            result[name] = gate_location(world, name, original)
    return result


def gate_wishes(world, wishes):
    result = []
    for wish in wishes:
        task = wish.task
        for location in wish.locations:
            task = gate_location(world, location, task)
        result.append(replace(wish, task=task))
    return tuple(result)
