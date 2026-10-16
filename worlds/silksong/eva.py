"""Eva's rewards and native crest unlock thresholds."""

EVA_NODE = 'weavenest-atla/weavenest-atla-eva#eva-pod'
EVOLVED_HUNTER = 'Evolved Hunter Crest'
YELLOW_VESTICREST = 'Yellow Vesticrest'
BLUE_VESTICREST = 'Blue Vesticrest'
SYLPHSONG = 'Sylphsong'
EVA_POINT = 'Eva Crest Point'
EVA_REWARDS = {
    'Hunter Evolution 1': (EVOLVED_HUNTER, 'Eva', 0),
    'Yellow Vesticrest': (YELLOW_VESTICREST, 'Eva', 12),
    'Blue Vesticrest': (BLUE_VESTICREST, 'Eva', 20),
    'Hunter Evolution 2': (EVOLVED_HUNTER, 'Eva', 27),
    'Sylphsong': (SYLPHSONG, 'Eva', 32),
}
EVA_CREST_SLOTS = {
    'Crest: Reaper': (4, ('Red 1', 'Blue 1', 'Yellow 1')),
    'Crest: Wanderer': (4, ('Blue 1', 'Blue 2', 'Yellow 1')),
    'Crest: Beast': (3, ('Yellow 1', 'Yellow 2')),
    'Crest: Witch': (3, ('Red 1', 'Blue 1', 'Blue 2')),
    'Crest: Architect': (3, ('Blue 1', 'Yellow 1', 'Yellow 2', 'Blue 2')),
    'Crest: Shaman': (3, ('Blue 1', 'Blue 2')),
}
EVA_POINT_SOURCES = tuple(
    (f'Event: Eva {crest} {label}', crest, slot)
    for crest, (free, slots) in EVA_CREST_SLOTS.items()
    for label, slot in (
        *((f'base {index + 1}', None) for index in range(free)),
        *((label, f'Crest Slot: {crest.removeprefix("Crest: ")} ({label})') for label in slots),
    )
)
