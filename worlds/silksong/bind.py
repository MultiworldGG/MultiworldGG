from dataclasses import replace

from .boss_souls import BY_BOSS
from .locations import canonicalize_location_name
from .requirements import CREST_ITEMS, NON_SHAMAN_CREST_ITEMS, REQUIREMENTS, get_location_requirements, req


CAPABILITY = 'Capability: Bind'
BOSSES = ('Boss: Widow', 'Boss: First Sinner', 'Boss: Grand Mother Silk')
LOCATIONS = frozenset(canonicalize_location_name(name) for name in (
    *BOSSES,
    *(f'Crest Unlock: {crest}' for crest in ('Wanderer', 'Reaper', 'Beast', 'Architect', 'Shaman')),
    *(f'Skill Unlock: {skill}' for skill in ('Dash', 'Wall Jump', 'Harpoon', 'Silk Soar', 'Needolin')),
    *(f'Silk Skill: {skill}' for skill in ('Silkspear', 'Sharpdart', 'Rune Rage', 'Thread Storm', 'Pale Nails')),
))
EVENTS = frozenset((
    'Event: Grand Mother Silk Defeated',
    'Event: Grand Mother Silk Snared',
    *(name for boss in BOSSES for name in (*BY_BOSS[boss]['events'], *BY_BOSS[boss]['combat'])),
))


def enabled(world):
    return bool(world.options.bind_randomization.value)


def pool_items(world):
    if world.options.bind_randomization.current_key == 'per_crest':
        from .items import CREST_BIND_ITEMS
        return CREST_BIND_ITEMS
    return ('Bind',) if enabled(world) else ()


def gate(rules):
    return tuple(replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, CAPABILITY)))) for rule in rules)


def gate_location(world, name, rules):
    if not enabled(world):
        return rules
    rules = stall_rules(world, rules)
    return gate(rules) if name in LOCATIONS else rules


def stall_terms(terms):
    if not any(name.startswith('Technique: Heal Stall ') for name in terms):
        return terms
    crests = CREST_ITEMS.intersection(terms)
    if crests == {'Crest: Shaman'}:
        return None
    return tuple(dict.fromkeys((*terms, *(crest.removeprefix('Crest: ') + ' Bind'
                                         for crest in sorted(crests & NON_SHAMAN_CREST_ITEMS)))))


def stall_rules(world, rules):
    if world.options.bind_randomization.current_key != 'per_crest':
        return rules
    result = []
    for rule in rules:
        terms = stall_terms(rule.all_of)
        if terms is not None:
            result.append(replace(rule, all_of=terms) if terms != rule.all_of else rule)
    return tuple(result)


def gate_graph(world, graph):
    if not enabled(world):
        return graph
    result = {name: gate(stall_rules(world, rules)) if name in EVENTS else stall_rules(world, rules)
              for name, rules in graph.items()}
    per_crest = world.options.bind_randomization.current_key == 'per_crest'
    result[CAPABILITY] = tuple(req(crest, crest.removeprefix('Crest: ') + ' Bind', crest=False)
                               for crest in sorted(CREST_ITEMS)) if per_crest else (
                                   req('Bind', any_of=tuple(sorted(CREST_ITEMS)), crest=False),)
    for name, rules in graph.items():
        if name.startswith('Technique: Heal Stall ') and rules:
            result[name] = tuple(req(crest, crest.removeprefix('Crest: ') + ' Bind', crest=False)
                                 for crest in sorted(NON_SHAMAN_CREST_ITEMS)) if per_crest else gate(rules)
    return result


def location_overrides(world, rules):
    world._bind_native_source_candidates = set()
    if not enabled(world):
        return rules
    result = dict(rules)
    for name in REQUIREMENTS.keys() | rules.keys():
        original = rules[name] if name in rules else get_location_requirements(name)
        updated = gate_location(world, name, original)
        if updated != original:
            result[name] = updated
            if name not in rules:
                world._bind_native_source_candidates.add(name)
    return result


def export_world(world, slot_data):
    slot_data['bind_randomization'] = world.options.bind_randomization.current_key
    if not enabled(world):
        return
    from .requirements import _export_requirement_group
    for name, rules in world._silksong_native_abstract_requirements.items():
        if name == CAPABILITY or name in EVENTS or name.startswith('Technique: Heal Stall '):
            slot_data['abstract_requirements'][name] = _export_requirement_group(rules)
    for name, rules in world._progression_location_rules.items():
        if name in LOCATIONS or (name in REQUIREMENTS and
                stall_rules(world, get_location_requirements(name)) != get_location_requirements(name)):
            slot_data['requirements'][name] = _export_requirement_group(rules)
    if world.options.bind_randomization.current_key == 'per_crest':
        for group in (*slot_data['requirements'].values(), *slot_data['abstract_requirements'].values()):
            alternatives = []
            for rule in group.get('alternatives', ()):
                terms = stall_terms(tuple(rule.get('all_of', ())))
                if terms is not None:
                    alternatives.append({**rule, 'all_of': list(terms)})
            group['alternatives'] = alternatives
