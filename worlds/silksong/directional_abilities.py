from __future__ import annotations

from dataclasses import replace
from functools import lru_cache
from .display_names import clean_item_display_name


ABILITIES = ('Cling Grip', 'Ledge Grab', 'Clawline', 'Swift Step', 'Dash')
ITEMS = tuple(f'{ability} ({side})' for ability in ABILITIES for side in ('Left', 'Right'))


def progressive_steps(first_right=False):
    sides = ('Right', 'Left') if first_right else ('Left', 'Right')
    return ('Sprint', *(f'Dash ({side})' for side in sides))


@lru_cache(maxsize=4096)
def split_requirement_counts(rules, enabled):
    if not enabled:
        return rules
    result = []
    for rule in rules:
        counts = []
        for count in rule.item_counts:
            name = clean_item_display_name(count.item_names[0]) if len(count.item_names) == 1 else None
            ability = 'Dash' if name == 'Swift Step' and 'Dash' in enabled else name
            if ability in enabled:
                counts.extend(replace(count, item_names=(f'{ability} ({side})',)) for side in ('Left', 'Right'))
            elif name == 'Progressive Swift Step' and 'Dash' in enabled:
                counts.append(replace(count, item_names=('Sprint',), minimum=min(count.minimum, 1)))
                if count.minimum >= 2:
                    counts.extend(replace(count, item_names=(f'Dash ({side})',), minimum=1) for side in ('Left', 'Right'))
            else:
                counts.append(count)
        result.append(replace(rule, item_counts=tuple(counts)) if tuple(counts) != rule.item_counts else rule)
    return tuple(result)


def selected(options, skills_randomized=True):
    enabled = lambda name: bool(getattr(getattr(options, name, None), 'value', False))
    result = []
    if enabled('ledgegrab_ability_rando') and enabled('directional_ledge_grab'):
        result.append('Ledge Grab')
    if skills_randomized:
        for ability, key in (('Cling Grip', 'directional_cling_grip'), ('Clawline', 'directional_clawline')):
            if enabled(key):
                result.append(ability)
        if enabled('directional_swift_step'):
            result.append('Dash' if enabled('split_dash_and_sprint') else 'Swift Step')
    return tuple(result)


def requirements(req, enabled=()):
    result = {}
    for ability in ('Cling Grip', 'Ledge Grab', 'Clawline', 'Dash', 'Sprint'):
        base = {'Ledge Grab': 'Capability: Ledge Grab', 'Dash': 'Swift Step',
                'Sprint': 'Capability: Sprint'}.get(ability, 'Ancestral Art: ' + ability)
        split = ability in enabled or ability in ('Dash', 'Sprint') and 'Swift Step' in enabled
        item = 'Swift Step' if 'Swift Step' in enabled and ability in ('Dash', 'Sprint') else ability
        for side in ('Left', 'Right'):
            result[f'Directional: {ability} {side}'] = (
                req(f'{item} ({side})', crest=ability != 'Ledge Grab') if split
                else req(base, crest=False),
            )
    result['Capability: Sprint'] = (req('Swift Step'), req('Progressive Swift Step'))
    if 'Dash' in enabled:
        result['Capability: Sprint'] = (req('Sprint'),)
        result['Progressive Swift Step'] = (req('Sprint', crest=False),)
    elif 'Swift Step' in enabled:
        result['Capability: Sprint'] = (req('Swift Step (Left)', 'Swift Step (Right)'),)
    for ability in enabled:
        base = 'Swift Step' if ability == 'Dash' else ability
        rule = (req(f'{ability} (Left)', f'{ability} (Right)', crest=ability != 'Ledge Grab'),)
        result[base] = rule
        if ability == 'Ledge Grab':
            result['Capability: Ledge Grab'] = rule
        else:
            result['Ancestral Art: ' + base] = rule
    return result


def split_pool(entries, enabled, entry_type, replace_filler):
    extras = []
    for ability in enabled:
        if ability == 'Dash':
            extras.append('Progressive Swift Step')
            continue
        source = ability
        matches = [i for i, entry in enumerate(entries) if clean_item_display_name(entry.name) == source]
        if not matches:
            continue
        index = matches[-1]
        entry = entries[index]
        entries[index] = entry_type(f'{ability} (Left)', entry.source_category, entry.placement_category)
        extras.append(f'{ability} (Right)')
    replace_filler(entries, tuple(extras), None)
