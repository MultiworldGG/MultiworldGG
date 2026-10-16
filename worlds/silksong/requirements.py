from __future__ import annotations

from .combat import SKILLS_BY_TIER, TOOLS_BY_TIER, build_requirements as build_combat_requirements
from .eva import EVA_NODE, EVA_REWARDS, EVA_POINT, EVA_POINT_SOURCES, EVA_CREST_SLOTS, EVOLVED_HUNTER, YELLOW_VESTICREST, BLUE_VESTICREST

from collections import Counter, OrderedDict, deque
from dataclasses import dataclass, field, replace
from functools import lru_cache
from itertools import combinations, product
from types import MappingProxyType
from typing import Callable, Dict, Iterable, Mapping
from weakref import WeakKeyDictionary

from BaseClasses import CollectionState

from .display_names import (
    FLEA_ITEM_NAMES,
    clean_item_display_name,
)
from .minor_pickups import (
    ACTIVE_MINOR_PICKUP_LOCATION_NAMES,
    MINOR_PICKUP_SOURCE,
)
from .lore_tablets import (
    LORE_TABLET_JUNK_ONLY_LOCATION_NAMES,
    LORE_TABLET_SOURCES,
)
from .minor_caches import (
    ACTIVE_MINOR_CACHE_LOCATION_NAMES,
    MINOR_CACHE_SOURCE,
)
from .locations import (
    COURIER_DELIVERY_WISH_LOCATION_NAMES,
    CARDINIUS_CYLINDER_ITEM_BY_TURN_IN_LOCATION,
    INDIVIDUAL_RELIC_TURN_IN_ITEM_NAMES,
    LOCATION_NAMES_BY_CATEGORY,
    MASK_SHARD_LOCATION_NAMES,
    NEEDLE_UPGRADE_LOCATION_NAMES,
    PINMASTER_OIL_QUEST_LOCATION,
    QUEST_LOCATION_NAMES,
    SCROUNGE_RELIC_ITEM_BY_TURN_IN_LOCATION,
    SCROUNGE_RELIC_ITEM_NAMES,
    SILK_HEART_LOCATION_NAMES,
    SPOOL_FRAGMENT_LOCATION_NAMES,
    canonicalize_location_name,
    location_data_table,
)
from .room_graph import load_room_graph
from .room_graph_logic import (
    CompiledRoomClause,
    CompiledRoomGraph,
    SPOOL_FRAGMENT_COUNT_ITEM,
    compile_room_graph,
    room_event_name,
    room_node_name,
)
from .wish_events import (
    SILK_AND_SOUL_LACE_DEFEATED_ITEM,
    SILK_AND_SOUL_MANDATORY_EVENTS,
    SILK_AND_SOUL_MANDATORY_WISH_ITEM,
    SILK_AND_SOUL_WISH_HALF_POINT_ITEM,
    SILK_AND_SOUL_WISH_POINT_ITEM,
    SONGCLAVE_BOARD_COMPLETION_ITEM,
    WISH_LOGIC_EVENTS,
    WISH_LOGIC_EVENT_ITEM_NAMES,
)

# Requirements are split between shared paths and individual locations.
# Each location records its act, nearest path and additional requirements.

CREST_ITEMS: frozenset[str] = frozenset(
    (
        'Crest: Hunter',
        'Crest: Reaper',
        'Crest: Shaman',
        'Crest: Architect',
        'Crest: Wanderer',
        'Crest: Beast',
        'Crest: Witch',
    )
)
NON_ARCHITECT_CREST_ITEMS: frozenset[str] = frozenset(
    crest for crest in CREST_ITEMS
    if crest != 'Crest: Architect'
)
NON_SHAMAN_CREST_ITEMS: frozenset[str] = frozenset(
    crest for crest in CREST_ITEMS
    if crest != 'Crest: Shaman'
)
USABLE_SHARPDART_REQUIREMENT = 'Usable Sharpdart'
USABLE_RUNE_RAGE_REQUIREMENT = 'Usable Rune Rage'
USABLE_THREAD_STORM_REQUIREMENT = 'Usable Thread Storm'
USABLE_NEEDLE_PHIAL_REQUIREMENT = 'Usable Needle Phial'
USABLE_FLEA_BREW_REQUIREMENT = 'Usable Flea Brew'
USABLE_MAGMA_BELL_REQUIREMENT = 'Usable Magma Bell'
USABLE_SCUTTLEBRACE_REQUIREMENT = 'Usable Scuttlebrace'
USABLE_CINDRIL_LOADOUT_REQUIREMENT = 'Usable Cindril Loadout'
BROODFEAST_SEARED_TOOL_ITEMS: tuple[str, ...] = (
    'Tool: Flintslate',
    'Tool: Pimpillo',
    'Tool: Wispfire Lantern',
    'Tool: Voltvessels',
)
BROODFEAST_SHREDDED_TOOL_ITEMS: tuple[str, ...] = (
    'Tool: Sawtooth Circlet',
    'Tool: Cogwork Wheel',
    "Tool: Delver's Drill",
    'Tool: Conchcutter',
    'Crest: Beast',
    'Crest: Architect',
)
BROODFEAST_SKEWERED_TOOL_ITEMS: tuple[str, ...] = (
    'Tool: Sting Shard',
    'Tool: Longpin',
)
SPOOL_FRAGMENT_ITEM_NAMES = ('Spool Fragment',)
RED_TOOL_SLOT = 'Red'
BLUE_TOOL_SLOT = 'Blue'
YELLOW_TOOL_SLOT = 'Yellow'
TOOL_SLOT_COLORS: frozenset[str] = frozenset((
    RED_TOOL_SLOT,
    BLUE_TOOL_SLOT,
    YELLOW_TOOL_SLOT,
))
NATIVE_TOOL_SLOT_COUNTS_BY_CREST: Mapping[
    str,
    Mapping[str, int],
] = MappingProxyType({
    'Crest: Hunter': MappingProxyType({
        RED_TOOL_SLOT: 1,
        BLUE_TOOL_SLOT: 1,
        YELLOW_TOOL_SLOT: 1,
    }),
    'Crest: Reaper': MappingProxyType({
        RED_TOOL_SLOT: 1,
        BLUE_TOOL_SLOT: 1,
        YELLOW_TOOL_SLOT: 1,
    }),
    'Crest: Shaman': MappingProxyType({}),
    'Crest: Architect': MappingProxyType({
        RED_TOOL_SLOT: 3,
    }),
    'Crest: Wanderer': MappingProxyType({
        RED_TOOL_SLOT: 1,
        YELLOW_TOOL_SLOT: 2,
    }),
    'Crest: Beast': MappingProxyType({
        RED_TOOL_SLOT: 2,
    }),
    'Crest: Witch': MappingProxyType({
        RED_TOOL_SLOT: 1,
        BLUE_TOOL_SLOT: 1,
    }),
})
NATIVE_TOOL_SLOT_COLORS_BY_CREST: Mapping[str, frozenset[str]] = (
    MappingProxyType({
        crest_item: frozenset(slot_counts)
        for crest_item, slot_counts
        in NATIVE_TOOL_SLOT_COUNTS_BY_CREST.items()
    })
)
RANDOMIZED_TOOL_SLOT_ITEMS_BY_COLOR_AND_CREST: Mapping[
    str,
    Mapping[str, tuple[str, ...]],
] = MappingProxyType({
    RED_TOOL_SLOT: MappingProxyType({
        'Crest: Hunter': (
            'Crest Slot: Hunter (Red 1)',
        ),
        'Crest: Reaper': (
            'Crest Slot: Reaper (Red 1)',
        ),
        'Crest: Witch': (
            'Crest Slot: Witch (Red 1)',
        ),
    }),
    BLUE_TOOL_SLOT: MappingProxyType({
        'Crest: Wanderer': (
            'Crest Slot: Wanderer (Blue 1)',
            'Crest Slot: Wanderer (Blue 2)',
        ),
        'Crest: Architect': (
            'Crest Slot: Architect (Blue 1)',
            'Crest Slot: Architect (Blue 2)',
        ),
        'Crest: Shaman': (
            'Crest Slot: Shaman (Blue 1)',
            'Crest Slot: Shaman (Blue 2)',
        ),
        'Crest: Hunter': (
            'Crest Slot: Hunter (Blue 1)',
        ),
        'Crest: Reaper': (
            'Crest Slot: Reaper (Blue 1)',
        ),
        'Crest: Witch': (
            'Crest Slot: Witch (Blue 1)',
            'Crest Slot: Witch (Blue 2)',
        ),
    }),
    YELLOW_TOOL_SLOT: MappingProxyType({
        'Crest: Beast': (
            'Crest Slot: Beast (Yellow 1)',
            'Crest Slot: Beast (Yellow 2)',
        ),
        'Crest: Architect': (
            'Crest Slot: Architect (Yellow 1)',
            'Crest Slot: Architect (Yellow 2)',
        ),
        'Crest: Hunter': (
            'Crest Slot: Hunter (Yellow 1)',
        ),
        'Crest: Reaper': (
            'Crest Slot: Reaper (Yellow 1)',
        ),
        'Crest: Wanderer': (
            'Crest Slot: Wanderer (Yellow 1)',
        ),
    }),
})
NATIVE_BLUE_SLOT_CREST_ITEMS: frozenset[str] = frozenset(
    crest_item
    for crest_item, slot_colors in NATIVE_TOOL_SLOT_COLORS_BY_CREST.items()
    if BLUE_TOOL_SLOT in slot_colors
)
RANDOMIZED_BLUE_SLOT_ITEMS_BY_CREST: Mapping[str, tuple[str, ...]] = (
    MappingProxyType({
        crest_item: slot_items
        for crest_item, slot_items
        in RANDOMIZED_TOOL_SLOT_ITEMS_BY_COLOR_AND_CREST[
            BLUE_TOOL_SLOT
        ].items()
        if not NATIVE_TOOL_SLOT_COUNTS_BY_CREST[crest_item].get(
            BLUE_TOOL_SLOT,
            0,
        )
    })
)
RANDOMIZED_BLUE_SLOT_ITEM_NAMES: frozenset[str] = frozenset(
    slot_item
    for slot_items in RANDOMIZED_BLUE_SLOT_ITEMS_BY_CREST.values()
    for slot_item in slot_items
)
NATIVE_YELLOW_SLOT_CREST_ITEMS: frozenset[str] = frozenset(
    crest_item
    for crest_item, slot_colors in NATIVE_TOOL_SLOT_COLORS_BY_CREST.items()
    if YELLOW_TOOL_SLOT in slot_colors
)
RANDOMIZED_YELLOW_SLOT_ITEMS_BY_CREST: Mapping[
    str,
    tuple[str, ...],
] = MappingProxyType({
    crest_item: slot_items
    for crest_item, slot_items
    in RANDOMIZED_TOOL_SLOT_ITEMS_BY_COLOR_AND_CREST[
        YELLOW_TOOL_SLOT
    ].items()
    if not NATIVE_TOOL_SLOT_COUNTS_BY_CREST[crest_item].get(
        YELLOW_TOOL_SLOT,
        0,
    )
})
ALL_RANDOMIZED_TOOL_SLOT_ITEM_NAMES: frozenset[str] = frozenset(
    slot_item
    for slot_items_by_crest
    in RANDOMIZED_TOOL_SLOT_ITEMS_BY_COLOR_AND_CREST.values()
    for slot_items in slot_items_by_crest.values()
    for slot_item in slot_items
)

SKILL_ITEMS: tuple[str, ...] = tuple(
    clean_item_display_name(name)
    for name in (
        'Ability: Faydown Cloak',
        'Ability: Needle Strike',
        'Ancestral Art: Silk Soar',
        'Ancestral Art: Cling Grip',
        "Ability: Drifter's Cloak",
        'Ancestral Art: Swift Step',
        'Ancestral Art: Clawline',
        'Item: Quill',
        'Ancestral Art: Needolin',
    )
)

CLOAK_REQUIRED_SKILL_ITEMS = frozenset({'Silk Soar', 'Clawline', 'Faydown Cloak', "Drifter's Cloak", 'Needolin', 'Needle Strike'})

SILK_HEART_ITEM = 'Progressive Silkheart'
SWIFT_STEP_ITEM = 'Swift Step'
PROGRESSIVE_SWIFT_STEP_ITEM = 'Progressive Swift Step'
PROGRESSIVE_NEEDLE_UPGRADE_ITEM = 'Progressive Needle Upgrade'
PALE_OIL_ITEM = 'Pale Oil'
RUINED_TOOL_ITEM = 'Ruined Tool'
SIMPLE_KEY_WORMWAYS = 'Simple Key (Wormways)'
SIMPLE_KEY_DEEP_DOCKS = 'Simple Key (Deep Docks)'
SIMPLE_KEY_GREEN_PRINCE = 'Simple Key (Green Prince)'
SIMPLE_KEY_ROSARY_BANK = 'Simple Key (Rosary Bank)'
SIMPLE_KEY_ITEMS: tuple[str, ...] = (
    SIMPLE_KEY_WORMWAYS,
    SIMPLE_KEY_DEEP_DOCKS,
    SIMPLE_KEY_GREEN_PRINCE,
    SIMPLE_KEY_ROSARY_BANK,
)
MEMORY_LOCKET_ITEM = 'Memory Locket'
CREST_SLOT_LOCATION_NAMES: frozenset[str] = frozenset(
    name for name in LOCATION_NAMES_BY_CATEGORY['CrestSlot'] if name not in EVA_REWARDS
)
CRAFTMETAL_ITEM = 'Craftmetal'
MOSSBERRY_ITEM = 'Mossberry'
POLLIP_HEART_ITEM = 'Pollip Heart'
POLLIP_HEART_COUNT = 6
RITE_OF_REBIRTH_EVENT = 'Event: Rite of Rebirth Completed'
POLLIP_HEART_SOURCE_LOCATION_NAMES: tuple[str, ...] = tuple(
    LOCATION_NAMES_BY_CATEGORY['PollipHeart']
)
SILKEATER_ITEM = 'Silkeater'
KEY_OF_APOSTATE_ITEM = 'Key of Apostate'
WHITE_KEY_ITEM = 'White Key'
SURGEONS_KEY_ITEM = "Surgeon's Key"
ARCHITECTS_KEY_ITEM = "Architect's Key"
CRAW_SUMMONS_ITEM = 'Craw Summons'
CRAWFATHER_LOCATION = 'Boss: Crawfather'

# These relics become progression only while their optional individual
# deposit checks are enabled. They remain Useful in ordinary seeds except
# for the Sacred Cylinder, which is independently required for its melody.
OPTION_DEPENDENT_PROGRESSION_ITEM_NAMES: frozenset[str] = frozenset(
    INDIVIDUAL_RELIC_TURN_IN_ITEM_NAMES
)

# The room graph is pure declarative data, so it can be normalized
# before LocationRequirement is defined. Its clauses are converted to live AP
# rules below once the helper dataclasses exist.
def _canonicalize_compiled_checks(
    graph: CompiledRoomGraph,
) -> tuple[
    Mapping[str, tuple[CompiledRoomClause, ...]],
    Mapping[str, tuple[str, ...]],
]:
    requirements: dict[str, tuple[CompiledRoomClause, ...]] = {}
    source_ids: dict[str, list[str]] = {}
    for source_name, clauses in graph.check_requirements.items():
        canonical_name = canonicalize_location_name(source_name)
        if (
            canonical_name in requirements
            and requirements[canonical_name] != clauses
        ):
            raise ValueError(
                f'Conflicting room graph requirements for {canonical_name}'
            )
        requirements[canonical_name] = clauses
        canonical_source_ids = source_ids.setdefault(canonical_name, [])
        for source_id in graph.check_source_ids[source_name]:
            if source_id not in canonical_source_ids:
                canonical_source_ids.append(source_id)
    return (
        MappingProxyType(requirements),
        MappingProxyType({
            name: tuple(ids)
            for name, ids in source_ids.items()
        }),
    )


MAPPER_GRAPH_ENABLED = load_room_graph().assumptions.get("mapper_schema") == 3
_SOURCE_COMPILED_ROOM_GRAPH = compile_room_graph()
(
    _CANONICAL_ROOM_GRAPH_CHECK_REQUIREMENTS,
    _CANONICAL_ROOM_GRAPH_CHECK_SOURCE_IDS,
) = _canonicalize_compiled_checks(_SOURCE_COMPILED_ROOM_GRAPH)
COMPILED_ROOM_GRAPH = replace(
    _SOURCE_COMPILED_ROOM_GRAPH,
    check_requirements=_CANONICAL_ROOM_GRAPH_CHECK_REQUIREMENTS,
    check_source_ids=_CANONICAL_ROOM_GRAPH_CHECK_SOURCE_IDS,
    authoritative_check_names=frozenset(
        canonicalize_location_name(name)
        for name in _SOURCE_COMPILED_ROOM_GRAPH.authoritative_check_names
    ),
    quarantined_check_names=frozenset(
        canonicalize_location_name(name)
        for name in _SOURCE_COMPILED_ROOM_GRAPH.quarantined_check_names
    ),
)

_eva_clauses = {
    name: (CompiledRoomClause(all_of=(room_node_name(EVA_NODE), *(
        (f'Event: Eva {points} Points',) if points else ()
    ))),)
    for name, (_, _, points) in EVA_REWARDS.items()
}
COMPILED_ROOM_GRAPH = replace(
    COMPILED_ROOM_GRAPH,
    check_requirements=MappingProxyType({**COMPILED_ROOM_GRAPH.check_requirements, **_eva_clauses}),
    check_source_ids=MappingProxyType({**COMPILED_ROOM_GRAPH.check_source_ids, **{name: (EVA_NODE,) for name in EVA_REWARDS}}),
    authoritative_check_names=COMPILED_ROOM_GRAPH.authoritative_check_names | EVA_REWARDS.keys(),
    quarantined_check_names=COMPILED_ROOM_GRAPH.quarantined_check_names - EVA_REWARDS.keys(),
)

_quest_item_clauses = {
    'Loddie - Heavy Rosary Necklace': (CompiledRoomClause(all_of=(
        room_node_name('the-marrow/the-marrow-jail#ground-floor'),
        room_event_name('event:mapper/bb722371-5624-4a76-b335-a989e6677a1b'),
        'Event: Widow Defeated',
    )),),
    'Maiden Soul': (CompiledRoomClause(all_of=(
        room_node_name('bone-bottom/bone-bottom-town#ground-level'),
        'Event: Silk and Soul Offered',
    )),),
    'Hermit Soul': (CompiledRoomClause(all_of=(
        room_node_name('bellhart/bellhart-lower#hermit'),
        'Event: Silk and Soul Offered',
    )),),
    'Seeker Soul': (CompiledRoomClause(all_of=(
        room_node_name('bilewater/bilewater-arena-shack#room'),
    )),),
    'Pollen Heart': COMPILED_ROOM_GRAPH.check_requirements['Boss: Nyleth'],
    "Hunter's Heart": COMPILED_ROOM_GRAPH.check_requirements['Boss: Skarrsinger Karmelita'],
    'Encrusted Heart': COMPILED_ROOM_GRAPH.check_requirements['Boss: Crust King Khann'],
}
_quest_item_nodes = {
    'Loddie - Heavy Rosary Necklace': 'the-marrow/the-marrow-jail#ground-floor',
    'Maiden Soul': 'bone-bottom/bone-bottom-town#ground-level',
    'Hermit Soul': 'bellhart/bellhart-lower#hermit',
    'Seeker Soul': 'bilewater/bilewater-arena-shack#room',
    'Pollen Heart': 'grand-gate/nyleth-fight#room',
    "Hunter's Heart": 'far-fields/memory-karmelita#arena',
    'Encrusted Heart': 'sands-of-karak/coral-tower#main',
}
COMPILED_ROOM_GRAPH = replace(
    COMPILED_ROOM_GRAPH,
    check_requirements=MappingProxyType({**COMPILED_ROOM_GRAPH.check_requirements, **_quest_item_clauses}),
    check_source_ids=MappingProxyType({**COMPILED_ROOM_GRAPH.check_source_ids, **{
        name: (node,) for name, node in _quest_item_nodes.items()
    }}),
    authoritative_check_names=COMPILED_ROOM_GRAPH.authoritative_check_names | _quest_item_clauses.keys(),
    quarantined_check_names=COMPILED_ROOM_GRAPH.quarantined_check_names - _quest_item_clauses.keys(),
)

# Compiled room-graph checks use live logic. Checks that cannot be compiled
# are tracked separately below and cannot hold progression.
ROOM_GRAPH_CANONICAL_CHECK_NAMES: frozenset[str] = frozenset(
    canonicalize_location_name(name)
    for name in COMPILED_ROOM_GRAPH.authoritative_check_names
)
ROOM_GRAPH_QUARANTINED_CHECK_NAMES: frozenset[str] = frozenset(
    canonicalize_location_name(name)
    for name in COMPILED_ROOM_GRAPH.quarantined_check_names
)

SINNER_ROAD_EXACT_COMMUNITY_CHECK_NAMES: frozenset[str] = frozenset({
    "Sinner's Road - Rosary Chest",
    "Sinner's Road - Rosary Cache #1",
    "Sinner's Road - Rosary Cache #2",
    "Sinner's Road - Rosary Cache #3",
    "Sinner's Road - Rosary Cache #4",
    "Sinner's Road - Rosary Cache #5",
    "Sinner's Road - Rosary Cache #6",
    "Sinner's Road - Rosary Cache #7",
    "Sinner's Road - Rosary Cache #8",
    "Sinner's Road - Shell Shard Cache #1",
    "Sinner's Road - Shell Shard Cache #2",
    "Sinner's Road - Shell Shard Cache #3",
    "Sinner's Road - Shell Shard Cache #4",
    "Sinner's Road - Shell Shard Cache #5",
    "Sinner's Road - Shell Shard Cache #6",
    "Sinner's Road - Shell Shard Cache #7",
    "Sinner's Road - Frayed Rosary String",
    "Sinner's Road - Shard Bundle",
    "Sinner's Road - Map Purchase",
    "Boss: Disgraced Chef Lugoli",
    "Flea: Sinner's Road",
    "Wish: My Missing Brother",
    "Tacks",
    "Barbed Bracelet",
    "Roachkeeper - Simple Key",
})
SINNER_ROAD_UNRESOLVED_COMMUNITY_CHECK_NAMES: frozenset[str] = frozenset()
SINNER_ROAD_NON_COMMUNITY_FALLBACK_CHECK_NAMES: frozenset[str] = frozenset()
SINNER_MISSING_BROTHER_LOCATION = "Wish: My Missing Brother"
SINNER_MISSING_COURIER_EVENT = "Event: Missing Courier Rescued"
_SINNER_MISSING_BROTHER_COMMUNITY_CLAUSES = (
    COMPILED_ROOM_GRAPH.check_requirements.get(
        SINNER_MISSING_BROTHER_LOCATION,
        (),
    )
)
SINNER_MISSING_BROTHER_COMMUNITY_EVENT_COMPILED = bool(
    _SINNER_MISSING_BROTHER_COMMUNITY_CLAUSES
) and all(
    SINNER_MISSING_COURIER_EVENT in clause.all_of
    for clause in _SINNER_MISSING_BROTHER_COMMUNITY_CLAUSES
)

ROSARY_BANK_GATED_LOCATIONS: frozenset[str] = frozenset(
    canonicalize_location_name(location_name)
    for location_name in {
        'Rosary Cannon',
        'High Halls - Pale Rosary Necklace',
        *(f'High Halls - Rosary Cache #{index}' for index in range(1, 7)),
    }
)
RUINED_TOOL_REPAIR_LOCATIONS: tuple[str, ...] = (
    'Silkshot (Forge Daughter)',
    'Silkshot (Twelfth Architect)',
    'Silkshot (Original)',
)

# Every physical purchase which spends Craftmetal. The three Silkshot sources
# are alternate repairs for one shared vanilla tool. Randomized repair handling
# returns both ingredients while another active repair remains, so the group
# consumes one Craftmetal in total. Every other purchase consumes one. The
# Bone_12 Loddie fallback keeps its free Tool Pouch branch and is not a
# Craftmetal purchase.
CRAFTMETAL_PURCHASE_LOCATIONS: frozenset[str] = frozenset({
    *RUINED_TOOL_REPAIR_LOCATIONS,
    'Pimpillo',
    'Cogwork Wheel',
    'Scuttlebrace',
    'Sawtooth Circlet',
    'Cogfly',
    'Sting Shard',
    'Magma Bell',
})
CRAFTMETAL_MAXIMUM_CONSUMPTION = (
    len(
        CRAFTMETAL_PURCHASE_LOCATIONS
        - frozenset(RUINED_TOOL_REPAIR_LOCATIONS)
    )
    + 1
)
# Routes which need only the run/ground-momentum half of Swift Step accept the
# first progressive copy in split seeds.  Full dash routes continue to use
# SWIFT_STEP_ITEM, which resolves to two progressive copies when split.
SWIFT_STEP_OR_SPRINT_ITEMS: tuple[str, ...] = (
    SWIFT_STEP_ITEM,
    PROGRESSIVE_SWIFT_STEP_ITEM,
)
# The far-right ledge in Shellwood_01 uses the same traversal alternatives as
# the Longpin alcove above Bellhart. One shared movement tuple defines Longpin
# and the three adjacent shard caches.
SHELLWOOD_LONGPIN_MOVEMENT_ITEMS: tuple[str, ...] = (
    'Ancestral Art: Swift Step',
    'Ability: Faydown Cloak',
    'Ancestral Art: Clawline',
)
SILK_HEART_TRAVERSAL_ITEMS: frozenset[str] = frozenset(
    (
        'Clawline',
        'Silk Soar',
        'Needolin',
    )
)
LOGIC_ITEM_DEPENDENCIES: Mapping[str, tuple[str, ...]] = {
    item_name: (SILK_HEART_ITEM,)
    for item_name in SILK_HEART_TRAVERSAL_ITEMS
}


@dataclass(frozen=True)
class _AbstractValuesSnapshot:
    """State-independent portion of one abstract-logic evaluation.

    Access rules are called repeatedly for many locations while Archipelago's
    fill algorithm is testing the same simulated inventory. Only immutable
    results are stored here. The public helper creates the small closures used
    by its callers.
    """

    abstract_values: Mapping[str, bool]
    item_counts: tuple[tuple[str, int], ...]
    has_crest: bool
    has_spear: bool


_ABSTRACT_VALUES_CACHE_LIMIT = 128
_ABSTRACT_VALUES_CACHE: WeakKeyDictionary[object, OrderedDict] = (
    WeakKeyDictionary()
)


def _player_inventory_signature(
    state: CollectionState,
    player: int,
) -> tuple[object, ...] | None:
    """Return a mutation-safe key for a player's simulated inventory.

    States without ``prog_items`` skip caching because their mutation history
    cannot be tracked safely.
    """

    validation_signature = getattr(
        state,
        '_silksong_inventory_signature',
        None,
    )
    if validation_signature is not None:
        return validation_signature

    progression_items = getattr(state, 'prog_items', None)
    if progression_items is None:
        return None
    try:
        player_items = progression_items[player]
    except (KeyError, IndexError, TypeError):
        return None
    items_method = getattr(player_items, 'items', None)
    if not callable(items_method):
        return None
    return tuple(
        (str(name), int(count))
        for name, count in items_method()
        if count
    )


def _get_abstract_values_cache(
    state: CollectionState,
    player: int,
    cache_key: tuple[object, ...],
) -> _AbstractValuesSnapshot | None:
    try:
        state_cache = _ABSTRACT_VALUES_CACHE.get(state)
    except TypeError:
        return None
    if state_cache is None:
        return None
    snapshot = state_cache.get(cache_key)
    if snapshot is not None:
        state_cache.move_to_end(cache_key)
    return snapshot


def _store_abstract_values_cache(
    state: CollectionState,
    cache_key: tuple[object, ...],
    snapshot: _AbstractValuesSnapshot,
) -> None:
    try:
        state_cache = _ABSTRACT_VALUES_CACHE.setdefault(
            state,
            OrderedDict(),
        )
    except TypeError:
        return
    state_cache[cache_key] = snapshot
    state_cache.move_to_end(cache_key)
    while len(state_cache) > _ABSTRACT_VALUES_CACHE_LIMIT:
        state_cache.popitem(last=False)


def get_logic_item_dependencies(
    split_dash_and_sprint: bool = False,
    silk_heart_logic: bool = False,
) -> Mapping[str, tuple[str, ...]]:
    """Return dependencies that apply to the selected movement model."""

    dependencies = dict(LOGIC_ITEM_DEPENDENCIES) if silk_heart_logic else {}
    if split_dash_and_sprint:
        # Duplicate entries encode a two-copy progressive
        # requirement in exported slot data. The AP reachability evaluator
        # enforces the same count directly.
        dependencies[SWIFT_STEP_ITEM] = (
            PROGRESSIVE_SWIFT_STEP_ITEM,
            PROGRESSIVE_SWIFT_STEP_ITEM,
        )
    return dependencies

FLEA_ITEMS: tuple[str, ...] = FLEA_ITEM_NAMES

SHAKRA_MAP_ITEMS: tuple[str, ...] = (
    'Map: Mosslands',
    'Map: The Marrow',
    'Map: Deep Docks',
    'Map: Far Fields',
    'Map: Wormways',
    "Map: Hunter's March",
    'Map: Greymoor',
    'Map: Bellhart',
    'Map: Shellwood',
    'Map: Blasted Steps',
    "Map: Sinner's Road",
    'Map: Mount Fay',
    'Map: Sands of Karak',
    'Map: Bilewater',
)

SHAKRA_MAP_LOCATIONS: tuple[str, ...] = tuple(
    canonicalize_location_name(
        item_name.replace('Map: ', 'Map Purchase: ', 1)
    )
    for item_name in SHAKRA_MAP_ITEMS
)

TRAILS_END_REQUIREMENT_SHAKRA_STOCK = 'shakra_stock'
TRAILS_END_REQUIREMENT_OWNED_MAPS = 'owned_maps'
SUPPORTED_TRAILS_END_REQUIREMENTS = frozenset((
    TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    TRAILS_END_REQUIREMENT_OWNED_MAPS,
))

STATIC_MAP_ITEMS: tuple[str, ...] = (
    'Map: Weavenest Atla',
    'Map: Grand Gate',
    'Map: Underworks',
    'Map: Choral Chambers',
    'Map: Whispering Vaults',
    'Map: Whiteward',
    'Map: Cogwork Core',
    'Map: Memorium',
    'Map: High Halls',
    'Map: The Slab',
    'Map: Putrified Ducts',
    'Map: The Cradle',
    'Map: Verdania',
    'Map: The Abyss',
)

THREEFOLD_MELODY_ITEMS: tuple[str, ...] = (
    "Architect's Melody",
    "Conductor's Melody",
    "Vaultkeeper's Melody",
)

JUDGE_BELL_ITEMS: tuple[str, ...] = (
    'Bell: The Marrow',
    'Bell: Deep Docks',
    'Bell: Greymoor',
    'Bell: Shellwood',
    'Bell: Bellhart',
)

# Checks outside the verified source set keep their bootstrap rule and
# progression restriction until each missing state condition is represented.
_PLAYTEST_LOCATION_SOURCES: tuple[str, ...] = (
    'Pin Purchase: Bench',
    'Pin Purchase: Ventrica',
    'Pin Purchase: Bellway',
    'Pin Purchase: Vendor',
    'Relic Pickup: Weaver Totem Witch',
    'Relic Pickup: Psalm Cylinder Library Roof',
    'Relic Pickup: Bone Record Wisp Top',
    'Relic Pickup: Weaver Totem Bonetown_upper_room',
    'Relic Pickup: Librarian Melody Cylinder',
    'Relic Pickup: Seal Chit City Merchant',
    'Relic Pickup: Psalm Cylinder Ward',
    'Relic Pickup: Weaver Record Conductor',
    'Relic Pickup: Psalm Cylinder Librarian',
    'Relic Pickup: Psalm Cylinder Hang',
    'Relic Pickup: Seal Chit Ward Corpse',
    'Relic Pickup: Weaver Record Sprint_Challenge',
    'Relic Pickup: Psalm Cylinder Grindle',
    'Relic Pickup: Weaver Record Weave_08',
    'Relic Pickup: Bone Record Understore_Map_Room',
    'Relic Pickup: Bone Record Bone_East_14',
    'Relic Pickup: Seal Chit Aspid_01',
    'Relic Pickup: Seal Chit Silk Siphon',
    'Relic Pickup: Bone Record Greymoor_flooded_corridor',
    'Relic Pickup: Weaver Totem Slab_Bottom',
    'Relic Pickup: Ancient Egg Abyss Middle',
    'Bell Shrine Completion: bellShrineBoneForest',
    'Bell Shrine Completion: bellShrineWilds',
    'Bell Shrine Completion: bellShrineGreymoor',
    'Bell Shrine Completion: bellShrineShellwood',
    'Bell Shrine Completion: bellShrineBellhart',
    'Boss Completion: defeatedMossMother',
    'Boss Completion: skullKingKilled',
    'Boss Completion: defeatedBellBeast',
    'Boss Completion: defeatedAntQueen',
    'Boss Completion: defeatedSongGolem',
    'Boss Completion: defeatedDockForemen',
    'Boss Completion: defeatedVampireGnatBoss',
    'Boss Completion: defeatedCrowCourt',
    'Boss Completion: defeatedSplinterQueen',
    'Boss Completion: defeatedSeth',
    'Boss Completion: defeatedFlowerQueen',
    'Boss Completion: defeatedRoachkeeperChef',
    'Boss Completion: defeatedPhantom',
    'Boss Completion: DefeatedSwampShaman',
    'Boss Completion: defeatedCoralKing',
    'Boss Completion: defeatedLastJudge',
    'Boss Completion: defeatedGreyWarrior',
    'Boss Completion: defeatedFirstWeaver',
    'Boss Completion: defeatedBroodMother',
    'Boss Completion: defeatedTrobbio',
    'Boss Completion: defeatedTormentedTrobbio',
    'Boss Completion: defeatedCogworkDancers',
    'Boss Completion: defeatedLaceTower',
    'Boss Completion: defeatedSongChevalierBoss',
    'Boss Completion: defeatedWhiteCloverstag',
    'Boss Completion: defeatedCloverDancers',
    'Boss Completion: defeatedWispPyreEffigy',
    'Boss Completion: defeatedAntTrapper',
    'Boss Completion: defeatedCoralDrillerSolo',
    'Boss Completion: wardBossDefeated',
    'Boss Completion: defeatedZapCoreEnemy',
    'Boss Completion: spinnerDefeated',
    'Boss Completion: skullKingDefeated',
    'Crafting Kit Source: Forge Tool Kit',
    'Crafting Kit Source: Architect Tool Kit',
    'Crafting Kit Source: Grindle Tool Kit',
    'Crafting Kit Source: Crow Feathers',
)
PLAYTEST_LOCATIONS: tuple[str, ...] = tuple(
    canonicalize_location_name(location_name)
    for location_name in _PLAYTEST_LOCATION_SOURCES
)

# These routes use asset identities and published vanilla access information.
# They may hold progression. Checks with extra state requirements remain
# outside this tuple.
_LOGIC_PASS_A_LOCATION_SOURCES: tuple[str, ...] = (
    'Pin Purchase: Bench',
    'Pin Purchase: Ventrica',
    'Pin Purchase: Bellway',
    'Pin Purchase: Vendor',
    'Relic Pickup: Psalm Cylinder Library Roof',
    'Relic Pickup: Bone Record Wisp Top',
    'Relic Pickup: Weaver Totem Bonetown_upper_room',
    'Relic Pickup: Librarian Melody Cylinder',
    'Relic Pickup: Psalm Cylinder Ward',
    'Relic Pickup: Weaver Record Conductor',
    'Relic Pickup: Psalm Cylinder Librarian',
    'Relic Pickup: Psalm Cylinder Hang',
    'Relic Pickup: Weaver Record Sprint_Challenge',
    'Relic Pickup: Psalm Cylinder Grindle',
    'Relic Pickup: Weaver Record Weave_08',
    'Relic Pickup: Bone Record Understore_Map_Room',
    'Relic Pickup: Bone Record Bone_East_14',
    'Relic Pickup: Seal Chit Aspid_01',
    'Relic Pickup: Seal Chit Ward Corpse',
    'Relic Pickup: Seal Chit Silk Siphon',
    'Relic Pickup: Bone Record Greymoor_flooded_corridor',
    'Relic Pickup: Weaver Totem Slab_Bottom',
    'Relic Pickup: Ancient Egg Abyss Middle',
    'Bell Shrine Completion: bellShrineBoneForest',
    'Bell Shrine Completion: bellShrineWilds',
    'Bell Shrine Completion: bellShrineGreymoor',
    'Bell Shrine Completion: bellShrineShellwood',
    'Bell Shrine Completion: bellShrineBellhart',
    'Boss Completion: defeatedMossMother',
    'Boss Completion: defeatedBellBeast',
    'Boss Completion: defeatedSongGolem',
    'Boss Completion: defeatedDockForemen',
    'Boss Completion: defeatedVampireGnatBoss',
    'Boss Completion: defeatedSplinterQueen',
    'Boss Completion: defeatedSeth',
    'Boss Completion: defeatedAntQueen',
    'Boss Completion: defeatedCrowCourt',
    'Boss Completion: defeatedFlowerQueen',
    'Boss Completion: defeatedCoralKing',
    'Boss Completion: defeatedRoachkeeperChef',
    'Boss Completion: defeatedPhantom',
    'Boss Completion: DefeatedSwampShaman',
    'Boss Completion: defeatedLastJudge',
    'Boss Completion: defeatedGreyWarrior',
    'Boss Completion: defeatedFirstWeaver',
    'Boss Completion: defeatedTrobbio',
    'Boss Completion: defeatedTormentedTrobbio',
    'Boss Completion: defeatedCogworkDancers',
    'Boss Completion: defeatedLaceTower',
    'Boss Completion: defeatedWispPyreEffigy',
    'Boss Completion: wardBossDefeated',
    'Boss Completion: defeatedZapCoreEnemy',
    'Boss Completion: spinnerDefeated',
    'Boss Completion: skullKingDefeated',
    'Crafting Kit Source: Forge Tool Kit',
    'Crafting Kit Source: Architect Tool Kit',
    'Crafting Kit Source: Grindle Tool Kit',
)
LOGIC_PASS_A_LOCATIONS: tuple[str, ...] = tuple(
    canonicalize_location_name(location_name)
    for location_name in _LOGIC_PASS_A_LOCATION_SOURCES
)

# These quest checks have access rules. Most remain junk-only until all quest
# states are represented. The locations below may hold progression.
_LOGIC_PASS_A_QUEST_LOCATION_SOURCES: tuple[str, ...] = (
    'Quest Completion: A Pinsmiths Tools',
    'Quest Completion: Belltown House Mid',
    'Quest Completion: Building Materials',
    'Quest Completion: Building Materials (Bridge)',
    'Quest Completion: Building Materials (Statue)',
    'Quest Completion: Courier Delivery Bonebottom',
    'Quest Completion: Courier Delivery Dustpens Slave',
    'Quest Completion: Courier Delivery Fixer',
    'Quest Completion: Courier Delivery Fleatopia',
    'Quest Completion: Courier Delivery Mask Maker',
    'Quest Completion: Courier Delivery Pilgrims Rest',
    'Quest Completion: Courier Delivery Songclave',
    'Quest Completion: Extractor Blue Worms',
    'Quest Completion: Fine Pins',
    'Quest Completion: Garmond Black Threaded',
    'Quest Completion: Great Gourmand',
    'Quest Completion: Journal',
    'Quest Completion: Mr Mushroom',
    'Quest Completion: Pilgrim Rags',
    'Quest Completion: Rock Rollers',
    'Quest Completion: Save City Merchant',
    'Quest Completion: Save City Merchant Bridge',
    'Quest Completion: Save Courier Short',
    'Quest Completion: Save Courier Tall',
    'Quest Completion: Save Sherma',
    'Quest Completion: Shiny Bell Goomba',
    'Quest Completion: Skull King',
    'Quest Completion: Song Pilgrim Cloaks',
    'Quest Completion: Songclave Donation 1',
    'Quest Completion: Songclave Donation 2',
    'Quest Completion: Steel Sentinel Pt2',
)
LOGIC_PASS_A_QUEST_LOCATIONS: tuple[str, ...] = tuple(
    location_name
    for location_name in (
        *(
            canonicalize_location_name(source_name)
            for source_name in _LOGIC_PASS_A_QUEST_LOCATION_SOURCES
        ),
        'Wish: Restoration of Bellhart',
    )
    if location_name in QUEST_LOCATION_NAMES
)

PROGRESSION_SAFE_QUEST_LOCATIONS: frozenset[str] = frozenset(
    (
        'Wish: Final Audience',
        'Wish: Pain, Anguish and Misery',
        'Wish: Fatal Resolve',
        'Wish: Restoration of Bellhart',
        'Wish: Bone Bottom Repairs',
        'Wish: A Lifesaving Bridge',
        'Wish: My Missing Courier',
        'Wish: Volatile Flintbeetles',
        'Wish: Balm for the Wounded',
        # This Wish also needs its quest chain. Unlike the three nearby
        # Act-conversion Wishes, it is not permanently missable.
        'Wish: An Icon of Hope',
        # The capture route reaches the Slab combat Arena.
        'Wish: Passing of the Age',
        "Wish: Queen's Egg",
        *(
            (SINNER_MISSING_BROTHER_LOCATION,)
            if SINNER_MISSING_BROTHER_COMMUNITY_EVENT_COMPILED
            else ()
        ),
    )
)
JUNK_ONLY_QUEST_LOCATIONS: frozenset[str] = (
    frozenset(QUEST_LOCATION_NAMES) - PROGRESSION_SAFE_QUEST_LOCATIONS
)

# Crawbug Clearing has a complete source and prerequisite route.
PROGRESSION_SAFE_CENSUS_LOCATIONS: frozenset[str] = frozenset(
    (
        canonicalize_location_name('Crafting Kit Source: Crow Feathers'),
    )
)

# These rewards can disappear permanently when their optional encounter is
# skipped or its quest state advances. They remain in the seed for completion
# tracking and map visibility while accepting neither useful equipment nor
# required progression.
ALWAYS_JUNK_ONLY_MISSABLE_LOCATIONS: frozenset[str] = frozenset(
    (
        'Boss: Skull Tyrant (Bone Bottom)',
        # These delivery wishes explicitly require the pre-Act-3 world.
        'Wish: Bone Bottom Supplies',
        "Wish: Pilgrim's Rest Supplies",
        # Unfinished collection Wishes are removed by the Act 3 conversion.
        'Wish: Garb of the Pilgrims',
        'Wish: The Terrible Tyrant',
        # Handing in a Pale Oil before accepting this Wish can skip its
        # completion state permanently.
        "Wish: Pinmaster's Oil",
        # Opening the Weaver Gate makes this inscription missable.
        'The Slab - Weaver Gate Inscription',
    )
)

TEMPORARILY_UNVERIFIED_SHARED_CHECK_LOCATIONS: frozenset[str] = frozenset()

# These physical sources are stable, but their mandatory vanilla key or quest
# state is not an AP item or event yet. They remain visible and randomized
# while rejecting required progression behind an unrepresented gate.
TEMPORARILY_UNVERIFIED_KEY_OR_QUEST_LOCATIONS: frozenset[str] = frozenset(
    canonicalize_location_name(location_name)
    for location_name in (
        'Mask Shard: Dark Hearts',
        'Spider Strings',
        'Relic: Choral Commandment (Jubilana)',
        'Spool Fragment: Jubilana (Songclave)',
    )
)

# These direct pickups have source and movement requirements. Their routes do
# not rely on an omitted key, quest counter or negative story state.
HELD_MINOR_PICKUP_LOCATIONS: frozenset[str] = frozenset((
    'Underworks - Pristine Core',
))

VERIFIED_MINOR_PICKUP_LOCATIONS: frozenset[str] = (
    frozenset(
        canonicalize_location_name(location_name)
        for location_name in (
            'Deep Docks - Beast Shard',
            'Wormways - Frayed Rosary String',
            'Shellwood - Shard Bundle',
        )
    )
    | (
        ROOM_GRAPH_CANONICAL_CHECK_NAMES
        & frozenset(
            canonicalize_location_name(name)
            for name in ACTIVE_MINOR_PICKUP_LOCATION_NAMES
        )
    )
) - HELD_MINOR_PICKUP_LOCATIONS

# Each source below has its own encoded requirement and may hold progression.
# Other minor caches remain filler/trap-only until their room movement is
# represented.
MANUALLY_VERIFIED_MINOR_CACHE_LOCATIONS: frozenset[str] = frozenset(
    canonicalize_location_name(location_name)
    for location_name in (
        'Blasted Steps - Rosary Cache',
        'Moss Grotto - Rosary Cache',
        'Moss Grotto - Shell Shard Cache #1',
        'Moss Grotto - Shell Shard Cache #2',
        'Moss Grotto - Shell Shard Cache #5',
        'Moss Grotto - Shell Shard Cache #6',
        'Moss Grotto - Shell Shard Cache #7',
        'Shellwood - Shell Shard Cache #12',
        'Shellwood - Shell Shard Cache #4',
        'Shellwood - Shell Shard Cache #5',
        'Shellwood - Shell Shard Cache #6',
        'The Marrow - Rosary Cache #1',
        'The Marrow - Rosary Cache #2',
        'The Marrow - Rosary Cache #3',
        'The Marrow - Rosary Cache #4',
        'The Marrow - Rosary Cache #5',
        'The Marrow - Rosary Cache #6',
        'The Marrow - Rosary Cache #7',
        'The Marrow - Rosary Cache #11',
        'The Marrow - Rosary Cache #12',
        'The Marrow - Rosary Cache #13',
        'The Marrow - Rosary Cache #14',
        'The Marrow - Rosary Cache #15',
        'The Marrow - Rosary Cache #16',
        'The Marrow - Shell Shard Cache #2',
        'The Marrow - Shell Shard Cache #3',
        'The Marrow - Shell Shard Cache #4',
        'The Marrow - Shell Shard Cache #5',
        'The Marrow - Shell Shard Cache #6',
        'The Marrow (Mosslands Passage) - Rosary Cache #1',
        'The Marrow (Mosslands Passage) - Rosary Cache #2',
        'Bone Bottom - Rosary Cache #4',
        'Bone Bottom - Rosary Cache #5',
        'Bone Bottom - Rosary Cache #8',
        'Bone Bottom - Rosary Cache #9',
        'Bonegrave - Rosary Cache #1',
        'Bonegrave - Rosary Cache #2',
        'Bonegrave - Rosary Cache #3',
        'Bonegrave - Rosary Cache #4',
        'Mosshome - Rosary Cache #1',
        'Mosshome - Rosary Cache #2',
        'Mosshome - Rosary Cache #3',
        'Mosshome - Rosary Cache #4',
        'Greymoor - Rosary Cache #7',
        'Greymoor - Rosary Cache #8',
        'Greymoor - Rosary Cache #10',
        'Greymoor - Rosary Cache #11',
        'Greymoor - Rosary Cache #12',
        'Greymoor - Rosary Cache #13',
        'Greymoor - Rosary Cache #14',
        'Greymoor - Shell Shard Cache #1',
        'Greymoor - Shell Shard Cache #2',
        # Deep Docks #1-3 share Bone_East_13 and require Magma Bell.
        'Deep Docks - Shell Shard Cache #1',
        'Deep Docks - Shell Shard Cache #2',
        'Deep Docks - Shell Shard Cache #3',
    )
) | (
    ROOM_GRAPH_CANONICAL_CHECK_NAMES
    & frozenset(
        canonicalize_location_name(name)
        for name in ACTIVE_MINOR_CACHE_LOCATION_NAMES
    )
)

ROOM_GRAPH_PROMOTED_FALLBACK_LOCATIONS: frozenset[str] = frozenset({
    "Architect's Key",
    'Blasted Steps - Map Purchase',
    'Blasted Steps - Memory Locket',
    'Boss: Voltvyrm',
    'Choral Chambers - Memory Locket',
    'Cogwork Wheel',
    'Crest: Architect',
    'Ecstasy of the End - Pale Oil',
    'Egg of Flealia',
    'Fleatopia - Tool Pouch',
    'Greymoor - Bellshrine',
    'Longclaw',
    'Sawtooth Circlet',
    'Sands of Karak - Map Purchase',
    'Sands of Karak - Memory Locket',
    'Scuttlebrace',
    "Sinner's Road - Map Purchase",
    'Silkshot (Twelfth Architect)',
    'Twelfth Architect - Crafting Kit',
    'Underworks (East) - Spool Fragment',
    'Underworks - Pristine Core',
    'Underworks - Shell Shard Cache #1',
    'Underworks - Shell Shard Cache #2',
    'Underworks - Shell Shard Cache #7',
    'Underworks - Shell Shard Cache #8',
    'Underworks - Shell Shard Cache #9',
    'Underworks - Shell Shard Cache #10',
    'Underworks - Shell Shard Cache #11',
    'Underworks - Shell Shard Cache #16',
    'Volt Filament',
    'Whispering Vaults - Shard Bundle',
    'Wish: Passing of the Age',
})

_LOGIC_PASS_A_PROGRESSION_CANDIDATES: frozenset[str] = frozenset(
    (
        *SHAKRA_MAP_LOCATIONS,
        *LOGIC_PASS_A_LOCATIONS,
        *PROGRESSION_SAFE_CENSUS_LOCATIONS,
        *PROGRESSION_SAFE_QUEST_LOCATIONS,
        *NEEDLE_UPGRADE_LOCATION_NAMES,
        *MASK_SHARD_LOCATION_NAMES,
        *SPOOL_FRAGMENT_LOCATION_NAMES,
        *SILK_HEART_LOCATION_NAMES,
        *CRAFTMETAL_PURCHASE_LOCATIONS,
        *MANUALLY_VERIFIED_MINOR_CACHE_LOCATIONS,
        *ROOM_GRAPH_CANONICAL_CHECK_NAMES,
    )
) - (
    ALWAYS_JUNK_ONLY_MISSABLE_LOCATIONS
    | TEMPORARILY_UNVERIFIED_SHARED_CHECK_LOCATIONS
    | TEMPORARILY_UNVERIFIED_KEY_OR_QUEST_LOCATIONS
    | (
        ROOM_GRAPH_QUARANTINED_CHECK_NAMES
        - ROOM_GRAPH_PROMOTED_FALLBACK_LOCATIONS
    )
    | SINNER_ROAD_UNRESOLVED_COMMUNITY_CHECK_NAMES
)

ACT_ORDER: tuple[str, ...] = ('Act 1', 'Act 2', 'Act 3')

PATH_ORDER: tuple[str, ...] = (
    'Mosslands - Moss Grotto', # Start area
    'Weavenest - Atla',
    'Mosslands - Ruined Chapel',
    'Mosslands - Bone Bottom',
    'Mosslands - Bonegrave',
    'Mosslands - Snail Shamans',
    'The Marrow - Mosshome Gate',
    'Mosslands - Moss Druid',
    'The Marrow - Toll',
    'The Marrow - Bellshrine', # Requires silkspear
    'The Marrow - Shooting Gallery',
    "Hunter's March - Trap",
    'Deep Docks - Toll', # Can't go west (blocked by lever)
    'Deep Docks - Forge',
    'Deep Docks - Lower',
    'Deep Docks - Bellshrine',
    'Deep Docks - Abyss Exit', # Act 3
    'Deep Docks - Sauna',
    'Deep Docks - Diving Bell',
    'Far Fields - Gated Toll', # Discarded, only a checkpoint that leads nowhere unless open
    'Far Fields - Bellway',
    "Far Fields - Pilgrim's Rest", # Inside Far Fields
    'Far Fields - Seamstress', # Air balloon
    'Far Fields - Sprintmaster', # Top east
    'Far Fields - Karmelita',
    'Weavenest - Cindril',
    'Wormways - Entrance',
    'Wormways - Bottom',
    'Wormways Middle',
    'Wormways - Plasmium Lab',
    'Shellwood - Bellshrine',
    'Shellwood - Overgrown West',
    'Shellwood - Chapel Exit',
    'Shellwood - Greyroot',
    'Bellhart - Bellhart',
    'Bellhart - Widow',
    'Greymoor - Halfway House',
    'Greymoor - Bellshrine',
    'Greymoor - Wisp Thicket',
    'Blasted Steps - Toll',
    'Blasted Steps - Pinstress',
    'Blasted Steps - Bellway',
    "Sinner's Road - Broken Toll",
    "Sinner's Road - Styx",
    'Bilewater - Bellway',
    'Bilewater - Bilehaven',
    'Bilewater - Exhaust Organ',
    'Bilewater - Twisted Bud', # Not a bench
    'Grand Gate', # Not a bench, at the elevator before collapse
    'Underworks - Broken Elevator', # Below Grand Gate
    'Underworks - Confession Toll',
    'Underworks - Twelfth Architect',
    "Underworks - Architect's Shop", # Not a bench, just avobe Twelfth Architect
    'Underworks - Whiteward',
    'Choral Chambers - Outside Underworks',
    'Choral Chambers - Below Dining',
    'Choral Chambers - Spa',
    'Choral Chambers - High Halls Entrance',
    'Choral Chambers - First Shrine',
    'Choral Chambers - Songclave',
    'Choral Chambers - Grand Bellway',
    'Outlying Citadel - Lower Cogwork Core',
    'Outlying Citadel - Cogwork Core',
    'Outlying Citadel - High Halls Ventrica',
    'Outlying Citadel - Memorium',
    'Outlying Citadel - Library',
    'Outlying Citadel - Sacred Vault',
    'Putrified Ducts - Bellway',
    'Putrified Ducts - Huntress',
    'Putrified Ducts - Fleatopia',
    'The Slab - Capture Event', # Abstract
    'The Slab - Bellway',
    'The Slab - Window',
    'Mount Fay - Shakra',
    'Mount Fay - Toll',
    'Mount Fay - Final Climb',
    'Mount Fay - Workbench',
    'Sands of Karak - Sands of Karak',
    'Sands of Karak - Coral Tower',
    'The Cradle - Terminus',
    'The Cradle - Surface Ascent',
    'Abyss - Void Tendrils',
    'Abyss - Escape',
    # Bellways
    'Bellways',
    'Bellway - Deep Docks',
    'Bellway - Far Fields',
    'Bellway - Greymoor',
    'Bellway - Bellhart',
    'Bellway - Blasted Steps',
    'Bellway - Grand Bellway',
    'Bellway - The Slab',
    'Bellway - Shellwood',
    'Bellway - Bilewater',
    'Bellway - Putrified Ducts',
    # Ventrica
    'Ventrica',
    'Ventrica - Choral Chambers',
    'Ventrica - Underworks',
    'Ventrica - Grand Bellway',
    'Ventrica - High Halls',
    'Ventrica - Songclave',
    'Ventrica - Memorium',
)


@dataclass(frozen=True)
class ItemCountRequirement:
    """Require a minimum total across one or more interchangeable AP items."""

    item_names: tuple[str, ...]
    minimum: int

    def as_slot_data(self) -> dict[str, object]:
        return {
            "items": [
                clean_item_display_name(item_name)
                for item_name in self.item_names
            ],
            "minimum": self.minimum,
        }


@dataclass(frozen=True)
class LocationRequirement:
    all_of: tuple[str, ...] = field(default_factory=tuple)
    any_of: tuple[str, ...] = field(default_factory=tuple)
    required_locations: tuple[str, ...] = field(default_factory=tuple)
    require_any_crest: bool = True
    require_silk_spear: bool = False
    minimum_skip_tier: int = 0
    act: str = ""
    path_name: str = ""
    item_counts: tuple[ItemCountRequirement, ...] = field(default_factory=tuple)

    def as_slot_data(self) -> dict[str, object]:
        return {
            "all_of": [
                clean_item_display_name(item_name)
                for item_name in self.all_of
            ],
            "any_of": [
                clean_item_display_name(item_name)
                for item_name in self.any_of
            ],
            "required_locations": list(self.required_locations),
            "require_any_crest": self.require_any_crest,
            "require_silk_spear": self.require_silk_spear,
            "minimum_skip_tier": self.minimum_skip_tier,
            "act": self.act,
            "path": self.path_name,
            "item_counts": [
                count_requirement.as_slot_data()
                for count_requirement in self.item_counts
            ],
        }


def item_count(minimum: int, *item_names: str) -> ItemCountRequirement:
    return ItemCountRequirement(tuple(item_names), minimum)


def req(
    *all_of: str,
    any_of: Iterable[str] = (),
    required_locations: Iterable[str] = (),
    crest: bool = True,
    silk_spear: bool = False,
    skip_tier: int = 0,
    act: str = "",
    path_name: str = "",
    item_counts: Iterable[ItemCountRequirement] = (),
) -> LocationRequirement:
    return LocationRequirement(
        all_of=tuple(all_of),
        any_of=tuple(any_of),
        required_locations=tuple(
            canonicalize_location_name(location_name)
            for location_name in required_locations
        ),
        require_any_crest=crest,
        require_silk_spear=silk_spear,
        minimum_skip_tier=skip_tier,
        act=act,
        path_name=path_name,
        item_counts=tuple(item_counts),
    )


def area(
    act_number: int,
    path_name: str,
    *all_of: str,
    any_of: Iterable[str] = (),
    required_locations: Iterable[str] = (),
    crest: bool = True,
    silk_spear: bool = False,
    item_counts: Iterable[ItemCountRequirement] = (),
) -> LocationRequirement:
    act_name = f"Act {act_number}"
    return req(
        f"Act: {act_number}",
        f"Path: {path_name}",
        *all_of,
        any_of=any_of,
        required_locations=required_locations,
        crest=crest,
        silk_spear=silk_spear,
        act=act_name,
        path_name=path_name,
        item_counts=item_counts,
    )


def _volatile_flintbeetle_act_one_requirement(
    *,
    crest: bool,
    path_name: str = '',
) -> LocationRequirement:
    """Reach every quest target before the Act 3 ground fallback."""

    return req(
        'Act: 1',
        room_event_name('event:mapper/559e7c1d-8a73-4246-956c-2b92014d6a6a'),
        crest=crest,
        act='Act 1',
        path_name=path_name,
    )


_BLASTED_STEPS_ACCESS_PATHS: tuple[str, ...] = (
    'Blasted Steps - Toll',
    'Blasted Steps - Pinstress',
    'Blasted Steps - Bellway',
)


def grindle_access(
    act_number: int,
    *additional_requirements: str,
) -> tuple[LocationRequirement, ...]:
    """Reach Grindle with Cling Grip and one of the two verified climbs."""

    return tuple(
        requirement
        for path_name in _BLASTED_STEPS_ACCESS_PATHS
        for requirement in (
            area(
                act_number,
                path_name,
                *additional_requirements,
                'Ancestral Art: Cling Grip',
                'Ancestral Art: Silk Soar',
                crest=False,
            ),
            area(
                act_number,
                path_name,
                *additional_requirements,
                'Ancestral Art: Cling Grip',
                'Ability: Faydown Cloak',
                crest=False,
            ),
        )
    )


def _compiled_room_clause_requirement(
    clause: CompiledRoomClause,
) -> LocationRequirement:
    return req(
        *clause.all_of,
        *((f"Silk Cost: {clause.silk_cost}",) if clause.silk_cost else ()),
        crest=False,
        silk_spear=clause.require_silk_spear,
        skip_tier=clause.minimum_skip_tier,
        item_counts=(
            item_count(
                minimum,
                *(
                    SPOOL_FRAGMENT_ITEM_NAMES
                    if item_name == SPOOL_FRAGMENT_COUNT_ITEM
                    else JUDGE_BELL_ITEMS if item_name == "$bellshrines"
                    else FLEA_ITEMS if item_name == "$fleas"
                    else (item_name,)
                ),
            )
            for item_name, minimum in clause.item_counts
        ),
    )


ROOM_NODE_REQUIREMENTS: Dict[str, tuple[LocationRequirement, ...]] = {
    name: tuple(
        _compiled_room_clause_requirement(clause)
        for clause in clauses
    )
    for name, clauses in COMPILED_ROOM_GRAPH.node_requirements.items()
}
ROOM_NODE_REQUIREMENTS["Room Node: wish-menus/bone-bottom-wish-wall#room"] += (
    req("Room Node: bone-bottom/bone-bottom-town#ground-level",
        "Room Event: event:mapper/visit-shellwood", crest=False),
)
ROOM_EVENT_REQUIREMENTS: Dict[str, tuple[LocationRequirement, ...]] = {
    name: tuple(
        _compiled_room_clause_requirement(clause)
        for clause in clauses
    )
    for name, clauses in COMPILED_ROOM_GRAPH.event_requirements.items()
}
for _event in WISH_LOGIC_EVENTS:
    if not _event.requires_checked_source:
        continue
    for _target in load_room_graph().assumptions.get("event_aliases", {}).get(_event.item_name, ()):
        _name = room_event_name("event:mapper/" + _target)
        ROOM_EVENT_REQUIREMENTS[_name] = tuple(
            replace(clause, item_counts=(*clause.item_counts, item_count(1, _event.item_name)))
            for clause in ROOM_EVENT_REQUIREMENTS[_name]
        )

ROOM_CHECK_REQUIREMENTS: Dict[str, tuple[LocationRequirement, ...]] = {
    canonicalize_location_name(name): tuple(
        _compiled_room_clause_requirement(clause)
        for clause in clauses
    )
    for name, clauses in COMPILED_ROOM_GRAPH.check_requirements.items()
}


ROOM_CHECK_REQUIREMENTS['Volt Filament'] = tuple(
    replace(source, all_of=(*source.all_of,
        room_event_name('event:mapper/c245a3a8-e4da-44e6-96bf-329e94ea8298')))
    for source in ROOM_CHECK_REQUIREMENTS['Volt Filament']
)


ABYSS_ESCAPED_EVENT = 'Event: Abyss Escaped'
if MAPPER_GRAPH_ENABLED:
    _escape_start = room_node_name('the-abyss/abyss-escape#start')
    _escape_end = room_node_name('the-abyss/abyss-escape#end')
    _escape_route = tuple(
        source for source in ROOM_NODE_REQUIREMENTS[_escape_end]
        if _escape_start in source.all_of
    )
    if not _escape_route:
        raise ValueError('The directed Abyss escape route is missing.')
    ROOM_EVENT_REQUIREMENTS[ABYSS_ESCAPED_EVENT] = tuple(
        replace(source, all_of=(*source.all_of,
            'Act: 3',
            room_node_name('the-abyss/weavenest-absolom#the-void'),
            room_node_name('deep-docks/deep-docks-church#top'),
            room_event_name('event:mapper/reviewed:dark-below-accepted')))
        for source in _escape_route
    )
    _ritual = room_event_name('event:mapper/reviewed:everbloom-ritual')
    ROOM_EVENT_REQUIREMENTS[_ritual] = tuple(
        replace(source, all_of=(*source.all_of, ABYSS_ESCAPED_EVENT))
        for source in ROOM_EVENT_REQUIREMENTS[_ritual]
    )
    ROOM_CHECK_REQUIREMENTS['Elegy of the Deep'] = tuple(
        replace(source, all_of=(*source.all_of, ABYSS_ESCAPED_EVENT))
        for source in ROOM_CHECK_REQUIREMENTS['Elegy of the Deep']
    )


BUGS_OF_PHARLOOM_REWARD_LOCATIONS = frozenset((
    canonicalize_location_name('Tool Pouch: Bugs of Pharloom'),
    'Wish: Bugs of Pharloom',
))
for _room in load_room_graph().rooms:
    for _event in _room.events:
        if canonicalize_location_name(_event.label) in BUGS_OF_PHARLOOM_REWARD_LOCATIONS:
            ROOM_EVENT_REQUIREMENTS[room_event_name(_event.id)] = ()
for _journal_reward in BUGS_OF_PHARLOOM_REWARD_LOCATIONS:
    if _journal_reward in ROOM_CHECK_REQUIREMENTS:
        ROOM_CHECK_REQUIREMENTS[_journal_reward] = tuple(
            replace(source, all_of=(*source.all_of, 'Event: Bugs of Pharloom Completed'))
            for source in ROOM_CHECK_REQUIREMENTS[_journal_reward]
        )


POLLIP_RITE_ROOM_NODE = (
    room_event_name("event:mapper/pollip-rite-completed")
    if MAPPER_GRAPH_ENABLED
    else room_node_name("shellwood/shellwood-25b#room")
)
_POLLIP_RITE_BASE_REQUIREMENTS = (
    (req(room_node_name("shellwood/greyroot#room"), crest=False),)
    if MAPPER_GRAPH_ENABLED
    else ROOM_NODE_REQUIREMENTS.get(POLLIP_RITE_ROOM_NODE, ())
)


@lru_cache(maxsize=2)
def _get_pollip_rite_room_requirements(
    pollip_heart_count: int,
) -> tuple[LocationRequirement, ...]:
    if pollip_heart_count not in (0, POLLIP_HEART_COUNT):
        raise ValueError(
            "Pollip Heart count must use the live quest threshold of "
            f"{POLLIP_HEART_COUNT} but received {pollip_heart_count!r}."
        )

    adjusted = []
    for requirement in _POLLIP_RITE_BASE_REQUIREMENTS:
        item_counts = tuple(
            count_requirement
            for count_requirement in requirement.item_counts
            if POLLIP_HEART_ITEM not in count_requirement.item_names
        )
        required_locations = tuple(
            location_name
            for location_name in requirement.required_locations
            if location_name not in POLLIP_HEART_SOURCE_LOCATION_NAMES
        )
        if pollip_heart_count:
            item_counts = (
                *item_counts,
                item_count(pollip_heart_count, POLLIP_HEART_ITEM),
            )
        else:
            required_locations = tuple(dict.fromkeys((
                *required_locations,
                *POLLIP_HEART_SOURCE_LOCATION_NAMES,
            )))
        adjusted.append(replace(
            requirement,
            item_counts=item_counts,
            required_locations=required_locations,
        ))
    return tuple(adjusted)


if _POLLIP_RITE_BASE_REQUIREMENTS:
    ROOM_NODE_REQUIREMENTS[POLLIP_RITE_ROOM_NODE] = (
        _get_pollip_rite_room_requirements(0)
    )


EQUIPPED_SILK_SKILL_REQUIREMENTS: Mapping[
    str,
    tuple[LocationRequirement, ...],
] = {
    # Architect has no Silk Skill slot. Explicit crest alternatives keep this
    # equipped-skill rule data-driven for both AP generation and the client map.
    USABLE_SHARPDART_REQUIREMENT: tuple(
        req('Sharpdart', crest, crest=False)
        for crest in sorted(NON_ARCHITECT_CREST_ITEMS)
    ),
    USABLE_RUNE_RAGE_REQUIREMENT: tuple(
        req('Rune Rage', crest, crest=False)
        for crest in sorted(NON_ARCHITECT_CREST_ITEMS)
    ),
    USABLE_THREAD_STORM_REQUIREMENT: tuple(
        req('Thread Storm', crest, crest=False)
        for crest in sorted(NON_ARCHITECT_CREST_ITEMS)
    ),
}

def _build_equipped_colored_tool_requirements(
    *tool_items_with_colors: tuple[str, str],
    randomized_crest_slots_enabled: bool = True,
    additional_required_items: tuple[str, ...] = (),
) -> tuple[LocationRequirement, ...]:
    """Build tool loadouts that fit every item on one crest."""

    if not tool_items_with_colors:
        raise ValueError("A colored-tool loadout needs at least one tool.")

    tool_item_names = tuple(
        item_name for item_name, _slot_color in tool_items_with_colors
    ) + tuple(additional_required_items)
    required_colors = tuple(
        slot_color for _item_name, slot_color in tool_items_with_colors
    )
    unknown_colors = set(required_colors) - TOOL_SLOT_COLORS
    if unknown_colors:
        raise ValueError(
            f"Unknown tool slot colors: {sorted(unknown_colors)!r}"
        )
    required_slot_counts = Counter(required_colors)

    requirements = []
    extras = ((BLUE_TOOL_SLOT, BLUE_VESTICREST), (YELLOW_TOOL_SLOT, YELLOW_VESTICREST))
    for crest_item in sorted(NATIVE_TOOL_SLOT_COUNTS_BY_CREST):
        for size in range(3):
            for selected_extras in combinations(extras, size):
                extra_colors = {color for color, _ in selected_extras}
                missing = {
                    color: max(0, count - NATIVE_TOOL_SLOT_COUNTS_BY_CREST[crest_item].get(color, 0) - int(color in extra_colors))
                    for color, count in required_slot_counts.items()
                }
                choices = []
                for color, count in missing.items():
                    slots = RANDOMIZED_TOOL_SLOT_ITEMS_BY_COLOR_AND_CREST.get(color, {}).get(crest_item, ()) if randomized_crest_slots_enabled else ()
                    choices.append(tuple(combinations(slots, count)))
                for selected_slots in product(*choices):
                    requirements.append(req(
                        *tool_item_names, crest_item,
                        *(name for _, name in selected_extras),
                        *(slot for group in selected_slots for slot in group),
                        crest=False,
                    ))
    return tuple(requirements)


COLORED_TOOL_LOADOUTS: Mapping[
    str,
    tuple[tuple[str, str], ...],
] = MappingProxyType({
    **{
        f"Usable {name.removeprefix('Tool: ')}": ((name, RED_TOOL_SLOT),)
        for name in (
            *BROODFEAST_SEARED_TOOL_ITEMS,
            *BROODFEAST_SHREDDED_TOOL_ITEMS,
            *BROODFEAST_SKEWERED_TOOL_ITEMS,
            *('Tool: ' + name for tools in TOOLS_BY_TIER.values() for name in tools
              if name not in ('Curveclaw', 'Curvesickle')),
        )
        if name.startswith('Tool: ')
    },
    USABLE_FLEA_BREW_REQUIREMENT: (
        ('Tool: Flea Brew', RED_TOOL_SLOT),
    ),
    USABLE_NEEDLE_PHIAL_REQUIREMENT: (
        ('Tool: Needle Phial', RED_TOOL_SLOT),
    ),
    USABLE_MAGMA_BELL_REQUIREMENT: (
        ('Magma Bell', BLUE_TOOL_SLOT),
    ),
    USABLE_SCUTTLEBRACE_REQUIREMENT: (
        ('Tool: Scuttlebrace', YELLOW_TOOL_SLOT),
    ),
    'Usable Plasmium Phial': (('Tool: Plasmium Phial', RED_TOOL_SLOT),),
    'Usable Silkspeed Anklets': (('Tool: Silkspeed Anklets', YELLOW_TOOL_SLOT),),
    'Usable Drill Crystal Pogo Loadout': (
        ("Tool: Delver's Drill", RED_TOOL_SLOT),
        ('Tool: Memory Crystal', BLUE_TOOL_SLOT),
    ),
    USABLE_CINDRIL_LOADOUT_REQUIREMENT: (
        ('Tool: Flea Brew', RED_TOOL_SLOT),
        ('Tool: Silkspeed Anklets', YELLOW_TOOL_SLOT),
    ),
})

VOLT_SKILL_REQUIREMENTS = {
    'Volt Skill: ' + skill: tuple(
        alternative
        for alternative in _build_equipped_colored_tool_requirements(
            ('Tool: Volt Filament', BLUE_TOOL_SLOT),
            additional_required_items=(skill,),
        )
        if any(crest in alternative.all_of for crest in NON_ARCHITECT_CREST_ITEMS)
    )
    for skills in SKILLS_BY_TIER.values() for skill in skills
}
VANILLA_VOLT_SKILL_REQUIREMENTS = {
    'Volt Skill: ' + skill: tuple(
        alternative
        for alternative in _build_equipped_colored_tool_requirements(
            ('Tool: Volt Filament', BLUE_TOOL_SLOT),
            randomized_crest_slots_enabled=False,
            additional_required_items=(skill,),
        )
        if any(crest in alternative.all_of for crest in NON_ARCHITECT_CREST_ITEMS)
    )
    for skills in SKILLS_BY_TIER.values() for skill in skills
}


COLORED_TOOL_ACTIVATION_ITEMS: Mapping[str, tuple[str, ...]] = (
    MappingProxyType({
        USABLE_SCUTTLEBRACE_REQUIREMENT: (
            'Ancestral Art: Swift Step',
        ),
    })
)

def _build_route_loadout_requirements(randomized_crest_slots_enabled: bool):
    names = {name for table in (COMPILED_ROOM_GRAPH.node_requirements,
                               COMPILED_ROOM_GRAPH.event_requirements,
                               COMPILED_ROOM_GRAPH.check_requirements)
             for clauses in table.values() for clause in clauses for name in clause.all_of
             if name.startswith("Loadout: ")}
    result = {}
    for name in sorted(names):
        parts = name.removeprefix("Loadout: ").split(" + ")
        tools = {}
        allowed_crests = set(CREST_ITEMS)
        extras = set()
        for part in parts:
            if part in CREST_ITEMS:
                allowed_crests.intersection_update((part,))
            elif part in COLORED_TOOL_LOADOUTS:
                tools.update(COLORED_TOOL_LOADOUTS[part])
                extras.update(COLORED_TOOL_ACTIVATION_ITEMS.get(part, ()))
            elif part in EQUIPPED_SILK_SKILL_REQUIREMENTS:
                allowed_crests.intersection_update(NON_ARCHITECT_CREST_ITEMS)
                extras.add(part.removeprefix("Usable "))
            else:
                raise ValueError(f"Unknown route equipment requirement: {part}")
        alternatives = (_build_equipped_colored_tool_requirements(
            *sorted(tools.items()),
            randomized_crest_slots_enabled=randomized_crest_slots_enabled,
            additional_required_items=tuple(sorted(extras)),
        ) if tools else tuple(req(*sorted(extras), crest, crest=False)
                              for crest in sorted(allowed_crests)))
        result[name] = tuple(alternative for alternative in alternatives
                             if set(alternative.all_of) & allowed_crests)
    return result


EQUIPPED_COLORED_TOOL_REQUIREMENTS: Mapping[
    str,
    tuple[LocationRequirement, ...],
] = MappingProxyType({
    **VOLT_SKILL_REQUIREMENTS,
    **_build_route_loadout_requirements(True),
    **{requirement_name: _build_equipped_colored_tool_requirements(
        *loadout,
        additional_required_items=(
            COLORED_TOOL_ACTIVATION_ITEMS.get(requirement_name, ())
        ),
    )
    for requirement_name, loadout in COLORED_TOOL_LOADOUTS.items()}
})

VANILLA_CREST_SLOT_COLORED_TOOL_REQUIREMENTS: Mapping[
    str,
    tuple[LocationRequirement, ...],
] = MappingProxyType({
    **VANILLA_VOLT_SKILL_REQUIREMENTS,
    **_build_route_loadout_requirements(False),
    **{requirement_name: _build_equipped_colored_tool_requirements(
        *loadout,
        randomized_crest_slots_enabled=False,
        additional_required_items=(
            COLORED_TOOL_ACTIVATION_ITEMS.get(requirement_name, ())
        ),
    )
    for requirement_name, loadout in COLORED_TOOL_LOADOUTS.items()}
})

OPTION_DEPENDENT_CREST_SLOT_ITEM_NAMES: frozenset[str] = frozenset(
    item_name
    for alternatives in EQUIPPED_COLORED_TOOL_REQUIREMENTS.values()
    for alternative in alternatives
    for item_name in alternative.all_of
    if item_name in ALL_RANDOMIZED_TOOL_SLOT_ITEM_NAMES
)


ACT_REQUIREMENTS: Dict[str, tuple[LocationRequirement, ...]] = {
    'Act: 1': (
        req(crest=False, silk_spear=False),
    ),
    'Act: 2': (
        req('Event: Act 2 Started', crest=False),
    ),
    'Act: 3': (
        req('Event: Act 3 Started', crest=False),
    ),
}

PATH_REQUIREMENTS: Dict[str, tuple[LocationRequirement, ...]] = {
    'Path: Mosslands - Moss Grotto': (
        req(crest=False),  # Starting area (only one not requiring crest)
        req('Path: Mosslands - Ruined Chapel'), # Route back
        req('Path: Mosslands - Bone Bottom'), # Route back
        req('Path: Weavenest - Atla', 'Ancestral Art: Needolin'), # Route back
    ),
    'Path: Weavenest - Atla': (
        req('Path: Mosslands - Moss Grotto', 'Ancestral Art: Needolin'),
    ),
    'Path: Mosslands - Ruined Chapel': (
        req('Path: Mosslands - Moss Grotto'),
    ),
    'Path: Mosslands - Bone Bottom': (
        req('Path: Mosslands - Moss Grotto'),
        req('Path: The Marrow - Toll'),
        req('Path: The Marrow - Mosshome Gate'),
        req('Path: Wormways - Bottom'),
        req('Path: Wormways - Plasmium Lab'),
        req('Path: Shellwood - Bellshrine'),
        req('Path: Blasted Steps - Toll'),
        req('Path: Blasted Steps - Bellway'),
    ),
    'Path: The Marrow - Mosshome Gate': (
        req('Path: Mosslands - Bone Bottom'),
        req('Path: Mosslands - Moss Druid'),
        req('Path: Wormways - Entrance'),
    ),
    'Path: Mosslands - Moss Druid': ( # Silk spear or run/dash or double jump
        req('Path: The Marrow - Mosshome Gate', silk_spear=True),
        req(
            'Path: The Marrow - Mosshome Gate',
            any_of=(
                *SWIFT_STEP_OR_SPRINT_ITEMS,
                'Ability: Faydown Cloak',
            ),
        ),
    ),
    'Path: Mosslands - Bonegrave': (
        req('Path: Wormways - Bottom'),
        req(
            'Path: Mosslands - Bone Bottom',
            'Ancestral Art: Cling Grip',
        ),
    ),
    'Path: Mosslands - Snail Shamans': ( # Start of Act 3
        req('Path: Mosslands - Ruined Chapel', 'Path: Putrified Ducts - Fleatopia'),
    ),
    'Path: The Marrow - Toll': (
        req('Path: Mosslands - Bone Bottom'),
        req('Path: Deep Docks - Toll'), # One way
        req('Path: Deep Docks - Forge'), # One way
    ),
    'Path: The Marrow - Bellshrine': (
        req('Path: The Marrow - Mosshome Gate', silk_spear=True),
        # Blocked path to the East until Bellbeast has been freed
    ),
    'Path: The Marrow - Shooting Gallery': (
        req(
            'Path: The Marrow - Bellshrine',
            'Event: Bell Beast Defeated',
        ),
        req('Path: Bellhart - Bellhart', 'Ancestral Art: Cling Grip'),
    ),
    "Path: Hunter's March - Trap": (
        req('Path: The Marrow - Shooting Gallery'),
        # Can't be reached from Deep Docks - Toll (blocked by lever)
        # Can't be reached from Far Fields - Gated Toll (blocked by one way lever)
    ),
    'Path: Deep Docks - Toll': (
        req('Path: The Marrow - Shooting Gallery'),
        req("Path: Hunter's March - Trap"), # One way lever
        req('Path: Far Fields - Gated Toll'), # One way lever
        req('Path: Bellway - Deep Docks'), # Bellway
    ),
    'Path: Deep Docks - Forge': (
        req('Path: Deep Docks - Toll'),
        req('Path: Deep Docks - Abyss Exit'),
        # Path from Deep Docks - Bellshrine is blocked (one way lever)
    ),
    'Path: Deep Docks - Lower': (
        # The direct entrance is the Simple Key door immediately south of
        # Forge Daughter. Clawline can instead enter lower Deep Docks from
        # the Far Fields side without opening that door.
        req('Path: Deep Docks - Forge', SIMPLE_KEY_DEEP_DOCKS),
        req('Path: Far Fields - Bellway', 'Ancestral Art: Clawline'),
    ),
    'Path: Deep Docks - Bellshrine': (
        req('Path: Deep Docks - Forge', any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline')),
        # Path from the East is blocked by one way door that unlocks from the West
    ),
    'Path: Deep Docks - Abyss Exit': ( # ACT 3
        req('Path: Abyss - Escape', 'Ancestral Art: Silk Soar'), # Act 3
    ),
    'Path: Deep Docks - Diving Bell': ( # ACT 3
        req('Path: Deep Docks - Sauna', 'Act: 3'),
    ),
    'Path: Deep Docks - Sauna': ( # ACT 3
        req('Path: Mosslands - Snail Shamans'), # Logic requirement
        req('Path: Deep Docks - Diving Bell'),
    ),
    'Path: Far Fields - Gated Toll': (
        req('Path: Deep Docks - Toll'), # One way
        req('Path: Far Fields - Bellway', "Ability: Drifter's Cloak"),
        req('Path: Deep Docks - Bellshrine', 'Ancestral Art: Cling Grip', any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline')),
        # Can't be reached from Far Fields - Pilgrim's Rest (one way lever)
    ),
    'Path: Far Fields - Bellway': (
        req("Path: Far Fields - Pilgrim's Rest"),
        req('Path: Far Fields - Seamstress', "Ability: Drifter's Cloak"),
        req('Path: Bellway - Far Fields'), # Bellway
    ),
    "Path: Far Fields - Pilgrim's Rest": (
        # The ordinary first visit reaches Pilgrim's Rest and then the Bellway
        # before Seamstress awards Drifter's Cloak.
        req(
            'Path: Deep Docks - Bellshrine',
            'Ancestral Art: Swift Step',
        ),
        req('Path: Deep Docks - Bellshrine', 'Ancestral Art: Cling Grip', "Ability: Drifter's Cloak", any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline')),
        req('Path: Far Fields - Seamstress', "Ability: Drifter's Cloak"),
        # Can't reach from Far Fields - Bellway (one way explosive)
        # Route from Greymoor - Bellshrine is blocked (one direction only)
        req('Path: Far Fields - Sprintmaster', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline'),
    ),
    'Path: Far Fields - Sprintmaster': ( # Act 3 frontier
        req('Path: Far Fields - Karmelita'),
    ),
    'Path: Far Fields - Seamstress': (
        req('Path: Deep Docks - Bellshrine', any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline')),
        req('Path: Weavenest - Cindril', 'Ancestral Art: Needolin'),
        req('Path: Far Fields - Bellway', 'Ancestral Art: Swift Step'),
    ),
    'Path: Far Fields - Karmelita': (
        # The hidden route starts at Karmelita's statue in Hunter's March.
        req(
            'Act: 3',
            "Path: Hunter's March - Trap",
            'Ancestral Art: Silk Soar',
        ),
    ),
    'Path: Weavenest - Cindril': ( # Requires Needolin
        req('Path: Far Fields - Seamstress', 'Ancestral Art: Needolin', any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline')),
    ),
    # The southern vestibule is enough to register Shakra's Vendor Pins, but
    # her Wormways Map and the Wormways Flea are beyond Pebb's 500-Rosary
    # Simple Key gate. The currency remains grindable so it is not represented
    # as an AP inventory item.
    'Path: Wormways - Entrance': (
        req(
            'Path: The Marrow - Mosshome Gate',
            any_of=(
                'Crest: Beast',
                *SWIFT_STEP_OR_SPRINT_ITEMS,
                "Ability: Drifter's Cloak",
                'Ability: Faydown Cloak',
            ),
        ),
        req('Path: Wormways - Bottom', SIMPLE_KEY_WORMWAYS),
    ),
    'Path: Wormways - Bottom': (
        req(
            'Path: Wormways - Entrance',
            SIMPLE_KEY_WORMWAYS,
            any_of=SWIFT_STEP_OR_SPRINT_ITEMS,
        ),
        req('Path: Mosslands - Bone Bottom', 'Ancestral Art: Silk Soar'),
        req(
            'Path: Wormways Middle',
            any_of=(
                *SWIFT_STEP_OR_SPRINT_ITEMS,
                'Ability: Faydown Cloak',
                'Ancestral Art: Clawline',
            ),
        ),
    ),
    'Path: Wormways Middle': (
        req(
            'Path: Wormways - Bottom',
            any_of=(
                *SWIFT_STEP_OR_SPRINT_ITEMS,
                'Ability: Faydown Cloak',
                'Ancestral Art: Clawline',
            ),
        ),
    ),
    'Path: Wormways - Plasmium Lab': (
        req('Path: Wormways Middle', 'Ancestral Art: Cling Grip'),
    ),
    'Path: Shellwood - Overgrown West': (
        req('Room Node: shellwood/shellwood-03#top', crest=False),
    ),
    'Path: Shellwood - Bellshrine': (
        req('Room Node: shellwood/bellshrine-03#room', crest=False),
    ),
    'Path: Shellwood - Chapel Exit': (
        req('Room Node: shellwood/shellwood-25#right-corridor', crest=False),
    ),
    'Path: Shellwood - Greyroot': (
        req('Room Node: shellwood/room-witch#room', crest=False),
    ),
    'Path: Bellhart - Bellhart': (
        req('Room Node: bellhart/belltown#ground-level', crest=False),
    ),
    'Path: Bellhart - Widow': (
        req('Room Node: bellhart/belltown-shrine#arena', crest=False),
    ),
    'Path: Greymoor - Halfway House': (
        req('Path: Bellhart - Bellhart'),
        req('Path: Greymoor - Bellshrine', any_of=('Ancestral Art: Cling Grip', 'Ancestral Art: Swift Step', 'Ability: Faydown Cloak')),
        req('Room Node: greymoor/greymoor-03#bottom', crest=False),
        req(
            'Room Node: the-marrow/the-marrow-flea-caravan#main-area',
            crest=False,
            item_counts=(item_count(5, *FLEA_ITEMS),),
        ),
        # Path from Greymoor - Bellshrine blocked (one way door)
    ),
    'Path: Greymoor - Bellshrine': (
        req('Path: Greymoor - Halfway House', any_of=('Ancestral Art: Cling Grip', "Ability: Drifter's Cloak")),
        # The vanilla Far Fields ascent is the Drifter's Cloak wind route.
        # Cling Grip is obtained later in Shellwood and is not part of it.
        req("Path: Far Fields - Pilgrim's Rest", "Ability: Drifter's Cloak"),
        # Path from Sinner's Road - Styx blocked (one way wall)
    ),
    'Path: Greymoor - Wisp Thicket': (
        req('Room Node: wisp-thicket/wisp-thicket-bench#bottom', crest=False),
    ),
    'Path: Blasted Steps - Toll': (
        req('Path: Blasted Steps - Bellway', 'Ancestral Art: Cling Grip', any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline')),
        req(
            'Path: Blasted Steps - Pinstress',
            'Ancestral Art: Cling Grip',
            'Ancestral Art: Swift Step',
            any_of=(
                "Ability: Drifter's Cloak",
                'Ability: Faydown Cloak',
                'Ancestral Art: Clawline',
            ),
        ),
        req('Path: Shellwood - Overgrown West', 'Ancestral Art: Cling Grip'),
    ),
    'Path: Blasted Steps - Pinstress': (
        req('Path: Blasted Steps - Bellway', 'Ancestral Art: Cling Grip', any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline')),
        req('Path: Blasted Steps - Toll', 'Ancestral Art: Cling Grip', any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline')),
    ),
    'Path: Blasted Steps - Bellway': (
        req('Path: Blasted Steps - Toll', 'Ancestral Art: Cling Grip', any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline')),
        req('Path: Blasted Steps - Pinstress', 'Ancestral Art: Cling Grip', any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline')),
        req('Path: Sands of Karak - Sands of Karak', 'Ancestral Art: Clawline'),
        req('Path: Bellway - Blasted Steps'), # Bellway
    ),
    "Path: Sinner's Road - Broken Toll": (
        req(
            room_node_name("sinner-s-road/sinner-s-road-entrance#room"),
            crest=False,
        ),
        req('Path: Bilewater - Exhaust Organ', 'Ancestral Art: Cling Grip', 'Ancestral Art: Swift Step', 'Ancestral Art: Needolin'),
    ),
    "Path: Sinner's Road - Styx": (
        req("Path: Sinner's Road - Broken Toll", 'Ancestral Art: Cling Grip'),
        req('Path: Bilewater - Bellway', 'Ancestral Art: Cling Grip', 'Ancestral Art: Swift Step'),
    ),
    'Path: Bilewater - Bellway': (
        req("Path: Sinner's Road - Styx", 'Ancestral Art: Cling Grip', 'Ancestral Art: Swift Step'),
        req('Path: Bilewater - Bilehaven', 'Ability: Faydown Cloak'),
        # The Whispering Vaults entrance is a one-way drop into the Twisted
        # Bud enclosure. Opening its gate then reaches main Bilewater.
        req('Path: Bilewater - Twisted Bud'),
        req('Path: Bellway - Bilewater'), # Bellway
    ),
    'Path: Bilewater - Bilehaven': (
        req('Path: Bilewater - Bellway', 'Ability: Faydown Cloak', 'Ancestral Art: Cling Grip'),
    ),
    'Path: Bilewater - Exhaust Organ': ( # Require Needolin for Mist
        req("Path: Sinner's Road - Broken Toll", 'Ancestral Art: Cling Grip', 'Ancestral Art: Swift Step', 'Ancestral Art: Needolin'),
        req('Path: Bilewater - Bellway', 'Ancestral Art: Cling Grip', 'Ancestral Art: Swift Step', 'Ancestral Art: Needolin'),
    ),
    'Path: Bilewater - Twisted Bud': (
        req(
            'Path: Outlying Citadel - Library',
            'Ancestral Art: Clawline',
            'Ancestral Art: Swift Step',
            'Ancestral Art: Cling Grip',
        ),
    ),
    'Path: Grand Gate': (
        req('Event: Act 2 Started', 'Event: Last Judge Defeated'),
        req('Path: Choral Chambers - Below Dining'),
        req('Path: Underworks - Broken Elevator', 'Ancestral Art: Silk Soar'),
    ),
    'Path: Underworks - Broken Elevator': (
        req('Path: Grand Gate'),
        req('Event: Act 2 Started', 'Path: Greymoor - Wisp Thicket', 'Ancestral Art: Cling Grip', 'Ancestral Art: Swift Step', 'Ability: Faydown Cloak'),
        req('Path: Underworks - Confession Toll'),
    ),
    'Path: Underworks - Confession Toll': (
        req('Path: Underworks - Broken Elevator', 'Ancestral Art: Cling Grip'),
        # The temporary bridge is opened from the eastern Underworks after
        # arriving through Whiteward or the post-Trobbio Vaults lift.
        req('Path: Underworks - Twelfth Architect', 'Ancestral Art: Cling Grip'),
        req('Path: Choral Chambers - Outside Underworks', 'Ancestral Art: Cling Grip'),
        req('Path: Ventrica', 'Path: Ventrica - Underworks'), # Ventrica
    ),
    'Path: Underworks - Twelfth Architect': (
        req("Path: Underworks - Architect's Shop"),
        # The Cauldron is reached from Whiteward or from the Whispering
        # Vaults lift after Trobbio.  Neither route may require Clawline:
        # Clawline is the reward found in the Cauldron itself.  The hidden
        # Whiteward route still has a vertical climb requiring Cling Grip.
        req('Path: Underworks - Whiteward', 'Ancestral Art: Cling Grip'),
        req('Event: Act 2 Started', 'Event: Trobbio Defeated'),
    ),
    "Path: Underworks - Architect's Shop": (
        req('Path: Underworks - Twelfth Architect', any_of=('Ancestral Art: Clawline', 'Ability: Faydown Cloak')),
    ),
    # Whiteward's lower Choral Chambers lift consumes the named White Key.
    'Path: Underworks - Whiteward': (
        req('Event: Whiteward Elevator Unlocked'),
    ),
    'Path: Choral Chambers - Outside Underworks': (
        req('Path: Underworks - Confession Toll', 'Ancestral Art: Cling Grip'),
        req('Path: Grand Gate', 'Ancestral Art: Cling Grip'),
        req('Path: Choral Chambers - Below Dining'),
    ),
    'Path: Choral Chambers - Below Dining': (
        req('Path: Choral Chambers - Outside Underworks'),
        req('Path: Choral Chambers - Grand Bellway'),
        req('Path: Grand Gate'),
        req('Path: Choral Chambers - First Shrine'),
        req('Path: Choral Chambers - High Halls Entrance', 'Ancestral Art: Clawline'),
    ),
    'Path: Choral Chambers - Spa': (
        req('Path: Choral Chambers - Below Dining'),
        # The Choral-side Slab route begins at the bridge's right node.
        req(room_node_name("the-slab/slab-bridge#right")),
        req('Path: Ventrica', 'Path: Ventrica - Choral Chambers'), # Ventrica
    ),
    'Path: Choral Chambers - High Halls Entrance': (
        req('Path: Choral Chambers - Below Dining', 'Ancestral Art: Clawline'),
        # This is the Choral approach to the Dancers, not High Halls proper.
        # High Halls itself remains Clawline-gated below.
        req('Path: Choral Chambers - First Shrine', 'Ancestral Art: Cling Grip'),
        req('Path: Outlying Citadel - High Halls Ventrica', 'Ancestral Art: Clawline'),
    ),
    'Path: Choral Chambers - First Shrine': (
        req('Path: Choral Chambers - Below Dining'),
        req('Path: Choral Chambers - Grand Bellway'),
        req('Path: Choral Chambers - Songclave'),
        req('Path: Choral Chambers - High Halls Entrance', 'Ancestral Art: Clawline'),
    ),
    'Path: Choral Chambers - Songclave': (
        req('Path: Choral Chambers - First Shrine'),
        # Entering Whispering Vaults from the lower Cogwork Core lets Hornet
        # clear the Vaults arena and open this shortcut from the Vaults side.
        # The edge remains one-way because Songclave cannot use the passage
        # before it has been opened from inside the Vaults.
        req(
            'Path: Outlying Citadel - Library',
            'Ancestral Art: Cling Grip',
        ),
        req('Path: Outlying Citadel - Memorium', 'Ability: Faydown Cloak'),
        req('Path: Outlying Citadel - Sacred Vault', 'Ancestral Art: Cling Grip', 'Ancestral Art: Clawline'),
        req('Path: Ventrica', 'Path: Ventrica - Songclave'), # Ventrica
    ),
    'Path: Choral Chambers - Grand Bellway': (
        req('Event: Act 2 Started'),
        req('Path: Choral Chambers - First Shrine'),
        req('Path: Choral Chambers - Below Dining'),
        req('Path: Bellway - Grand Bellway'), # Bellway
        req('Path: Ventrica', 'Path: Ventrica - Grand Bellway'), # Ventrica
    ),
    'Path: Outlying Citadel - Lower Cogwork Core': (
        req('Event: Cogwork Dancers Defeated'),
    ),
    # The upper Core checks stay gated while the lower Core -> Whispering
    # Vaults -> Trobbio route can lead to Clawline.
    'Path: Outlying Citadel - Cogwork Core': (
        req('Path: Outlying Citadel - Lower Cogwork Core', 'Ancestral Art: Clawline'),
        req('Path: Outlying Citadel - High Halls Ventrica', 'Ancestral Art: Clawline'),
        req('Path: Outlying Citadel - Sacred Vault', 'Ancestral Art: Cling Grip', 'Ancestral Art: Clawline'),
    ),
    'Path: Outlying Citadel - High Halls Ventrica': (
        req('Path: Choral Chambers - High Halls Entrance', 'Ancestral Art: Clawline'),
        req('Path: Outlying Citadel - Cogwork Core', 'Ancestral Art: Clawline'),
        req('Path: Ventrica', 'Path: Ventrica - High Halls'), # Ventrica
    ),
    'Path: Outlying Citadel - Memorium': (
        req('Path: Choral Chambers - Songclave', 'Ability: Faydown Cloak'),
        req(room_node_name("putrified-ducts/putrified-ducts-entrance#entrance")),
        req('Path: Ventrica', 'Path: Ventrica - Memorium'), # Ventrica
    ),
    'Path: Outlying Citadel - Library': (
        req('Path: Outlying Citadel - Lower Cogwork Core', 'Ancestral Art: Cling Grip'),
        req('Path: Outlying Citadel - Sacred Vault', 'Ancestral Art: Cling Grip', 'Ancestral Art: Clawline'),
    ),
    'Path: Outlying Citadel - Sacred Vault': (
        req('Path: Outlying Citadel - Cogwork Core', 'Ancestral Art: Cling Grip', 'Ancestral Art: Clawline'),
        req('Path: Outlying Citadel - Library', 'Ancestral Art: Cling Grip', 'Ancestral Art: Clawline'),
        req('Path: Choral Chambers - Songclave', 'Ancestral Art: Cling Grip', 'Ancestral Art: Clawline'),
    ),
    'Path: Putrified Ducts - Bellway': (
        req(room_node_name("putrified-ducts/putrified-ducts-bellway#bellway")),
    ),
    'Path: Putrified Ducts - Huntress': (
        req(room_node_name("putrified-ducts/huntress#room")),
    ),
    'Path: Putrified Ducts - Fleatopia': (
        req(
            room_node_name("putrified-ducts/fleatopia#fleatopia"),
            'Event: Last Judge Defeated',
            item_counts=(item_count(22, *FLEA_ITEMS),),
        ),
    ),
    'Path: The Slab - Capture Event': (
        # Established path name: reachability of the fixed Key of Apostate pickup
        # is used as the monotonic proxy. Actual capture is not required.
        req('Path: Putrified Ducts - Huntress'),
    ),
    'Path: The Slab - Bellway': (
        req(room_node_name("the-slab/slab-bellway#room")),
    ),
    'Path: The Slab - Window': (
        req(room_node_name("the-slab/slab-window#room")),
    ),
    'Path: Mount Fay - Shakra': (
        # Clawline reaches Mount Fay and Shakra's entrance camp. Drifter's
        # Cloak becomes mandatory for the climb above this landmark.
        req('Path: The Slab - Bellway', 'Ancestral Art: Clawline'),
        req('Path: Mount Fay - Toll', 'Ancestral Art: Clawline', "Ability: Drifter's Cloak"),
        req('Path: Mount Fay - Workbench'),
        req('Path: Mount Fay - Final Climb'),
    ),
    'Path: Mount Fay - Toll': (
        req(
            'Path: Mount Fay - Shakra',
            'Ancestral Art: Clawline',
            "Ability: Drifter's Cloak",
        ),
    ),
    'Path: Mount Fay - Final Climb': (
        req('Path: Mount Fay - Toll', 'Ancestral Art: Clawline', "Ability: Drifter's Cloak"),
        req('Path: Mount Fay - Workbench'),
    ),
    'Path: Mount Fay - Workbench': (
        req('Path: Mount Fay - Final Climb', 'Ancestral Art: Clawline', "Ability: Drifter's Cloak"),
    ),
    'Path: Sands of Karak - Sands of Karak': (
        req('Path: Blasted Steps - Pinstress', 'Ancestral Art: Clawline'),
    ),
    'Path: Sands of Karak - Coral Tower': (
        req('Path: Sands of Karak - Sands of Karak', 'Ancestral Art: Clawline'),
        req('Path: Sands of Karak - Sands of Karak', 'Ancestral Art: Silk Soar', 'Ancestral Art: Needolin'),
    ),
    'Path: The Cradle - Terminus': (
        req('Event: Cradle Opened'),
        req('Path: The Cradle - Surface Ascent', 'Ancestral Art: Silk Soar', 'Ancestral Art: Clawline'),
        req('Path: Ventrica'),
    ),
    'Path: The Cradle - Surface Ascent': (
        req('Path: The Cradle - Terminus', 'Ancestral Art: Silk Soar', 'Ancestral Art: Clawline'),
        req('Path: Outlying Citadel - Cogwork Core', 'Ancestral Art: Silk Soar', 'Ancestral Art: Clawline'),
    ),
    'Path: Abyss - Void Tendrils': (
        req('Path: Deep Docks - Diving Bell'),
    ),
    'Path: Abyss - Escape': (
        # Abyss remains outside the authoritative room graph, but every escape
        # route ends at the same one-way gauntlet. Keep its universal gate here
        # without choosing between the earlier Upper Big Room/Landing branches.
        req(
            "Option: Proficient Movement",
            'Path: Abyss - Void Tendrils',
            'Ancestral Art: Silk Soar',
            "Ability: Drifter's Cloak",
            'Ancestral Art: Cling Grip',
            'Ability: Faydown Cloak',
        ),
        req(
            'Path: Abyss - Void Tendrils',
            'Ancestral Art: Silk Soar',
            "Ability: Drifter's Cloak",
            'Ancestral Art: Cling Grip',
            'Ability: Faydown Cloak',
            'Ancestral Art: Clawline',
        ),
    ),
    # Bellways
    'Path: Bellways': (
        # Booths may be bought before this, but the Bell Beast network cannot
        # actually be used until the beast has been freed.
        req('Event: Bell Beast Defeated', crest=False),
    ),
    'Path: Bellway - Deep Docks': (
        req('Path: Bellways', 'Bellway: Deep Docks'),
    ),
    'Path: Bellway - Far Fields': (
        req('Path: Bellways', 'Bellway: Far Fields'),
    ),
    'Path: Bellway - Greymoor': (
        req('Path: Bellways', 'Bellway: Greymoor'),
    ),
    'Path: Bellway - Bellhart': (
        req('Path: Bellways', 'Bellway: Bellhart'),
    ),
    'Path: Bellway - Blasted Steps': (
        req('Path: Bellways', 'Bellway: Blasted Steps'),
    ),
    'Path: Bellway - Grand Bellway': (
        req('Path: Bellways', 'Bellway: Grand Bellway'),
    ),
    'Path: Bellway - The Slab': (
        req('Path: Bellways', 'Bellway: The Slab'),
    ),
    'Path: Bellway - Shellwood': (
        req('Path: Bellways', 'Bellway: Shellwood'),
    ),
    'Path: Bellway - Bilewater': (
        req('Path: Bellways', 'Bellway: Bilewater'),
    ),
    'Path: Bellway - Putrified Ducts': (
        req('Path: Bellways', 'Bellway: Putrified Ducts'),
    ),
    # Ventrica
    'Path: Ventrica': (
        req('Path: Choral Chambers - Spa'),
        req('Path: Underworks - Confession Toll'),
        req('Path: Choral Chambers - Grand Bellway'),
        req('Path: Outlying Citadel - High Halls Ventrica'),
        # The station is the First Shrine, one floor above Songclave.
        req('Path: Choral Chambers - First Shrine'),
        req('Path: Outlying Citadel - Memorium'),
    ),
    'Path: Ventrica - Choral Chambers': (
        req('Path: Ventrica', 'Ventrica: Choral Chambers'),
    ),
    'Path: Ventrica - Underworks': (
        req('Path: Ventrica', 'Ventrica: Underworks'),
    ),
    'Path: Ventrica - Grand Bellway': (
        req('Path: Ventrica', 'Ventrica: Grand Bellway'),
    ),
    'Path: Ventrica - High Halls': (
        req('Path: Ventrica', 'Ventrica: High Halls'),
    ),
    'Path: Ventrica - Songclave': (
        req('Path: Ventrica', 'Ventrica: Songclave'),
    ),
    'Path: Ventrica - Memorium': (
        req('Path: Ventrica', 'Ventrica: Memorium'),
    ),
}

ACT_ONE_GOAL_EVENT = 'Event: Act 2 Started'
ACT_TWO_GOAL_EVENT = 'Event: Grand Mother Silk Defeated'
CURSED_ENDING_GOAL_EVENT = 'Event: Cursed Ending'
FINAL_GOAL_EVENT = 'Event: Lost Lace Defeated'
FLEA_HUNT_GOAL_KEY = 'flea_hunt'
DEFAULT_FLEA_HUNT_GOAL_COUNT = 30
MIN_FLEA_HUNT_GOAL_COUNT = 1
MAX_FLEA_HUNT_GOAL_COUNT = 30
GOAL_EVENT_BY_KEY: Mapping[str, str] = {
    'act_1': ACT_ONE_GOAL_EVENT,
    'act_2': ACT_TWO_GOAL_EVENT,
    'act_3': FINAL_GOAL_EVENT,
    'cursed_ending': CURSED_ENDING_GOAL_EVENT,
}


def normalize_trails_end_requirement(mode: str) -> str:
    """Check that the chosen Trail's End requirement is supported."""

    normalized = str(mode or '').strip().lower()
    if normalized not in SUPPORTED_TRAILS_END_REQUIREMENTS:
        raise ValueError(
            f"Unknown Trail's End requirement: {mode!r}"
        )
    return normalized


@lru_cache(maxsize=2)
def get_trails_end_map_requirements(mode: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK):
    mode = normalize_trails_end_requirement(mode)
    if mode == TRAILS_END_REQUIREMENT_OWNED_MAPS:
        return (req(*SHAKRA_MAP_ITEMS, crest=False),)
    return (req(crest=False, required_locations=SHAKRA_MAP_LOCATIONS),)


@lru_cache(maxsize=2)
def get_trails_end_requirements(
    mode: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
) -> tuple[LocationRequirement, ...]:
    """Return Trail's End routes for the selected map requirement."""

    mode = normalize_trails_end_requirement(mode)
    common_items = (
        'Event: Act 2 Started',
        'Path: Bilewater - Bilehaven',
        'Path: Mount Fay - Workbench',
        'Ability: Faydown Cloak',
    )
    required_maps = (
        SHAKRA_MAP_ITEMS
        if mode == TRAILS_END_REQUIREMENT_OWNED_MAPS
        else ()
    )
    required_map_locations = (
        ()
        if mode == TRAILS_END_REQUIREMENT_OWNED_MAPS
        else SHAKRA_MAP_LOCATIONS
    )
    return (
        req(
            *common_items,
            *required_maps,
            crest=False,
            required_locations=(
                *required_map_locations,
                'Boss Completion: DefeatedSwampShaman',
            ),
        ),
        req(
            *common_items,
            *required_maps,
            crest=False,
            required_locations=required_map_locations,
            item_counts=(
                item_count(2, *THREEFOLD_MELODY_ITEMS),
            ),
        ),
    )

# These are logical story events rather than shuffled items. Reaching every
# prerequisite means the corresponding vanilla story action can be completed.
# Combat-only gates count as complete once their arena is
# reachable, matching the rest of this no-difficulty-settings logic.
LAST_JUDGE_ROOM_EVENT = room_event_name(
    'event:blasted-steps/last-judge-arena/last-judge-defeated'
)


EVENT_REQUIREMENTS: Dict[str, tuple[LocationRequirement, ...]] = {
    "Event: Ordinary Silk Blockades Cleared": (
        req("Room Event: event:mapper/95f1f75b-e452-4709-9fbc-ad8785ac520a", crest=False),
    ),
    'Event: Bell Beast Defeated': (
        req(
            'Path: The Marrow - Bellshrine',
            crest=False,
        ),
    ),
    'Event: Rite of the Pollip Completed': (
        req(POLLIP_RITE_ROOM_NODE, crest=False),
    ),
    RITE_OF_REBIRTH_EVENT: (
        req(
            POLLIP_RITE_ROOM_NODE,
            'Event: Widow Defeated',
            crest=False,
        ),
    ),
    # The tools and Flea beyond the Craw Lake arena are all downstream of the
    # same combat gauntlet. Combat execution is not a separate difficulty gate,
    # so reaching the arena with the vanilla traversal ability resolves it.
    'Event: Craw Lake Cleared': (
        req(
            'Path: Greymoor - Bellshrine',
            "Ability: Drifter's Cloak",
            crest=False,
        ),
    ),
    'Event: Fourth Chorus Defeated': (
        req(
            'Path: Far Fields - Bellway',
            'Event: Flexile Spines Completed',
            crest=False,
        ),
    ),
    # Flexile Spines (the ``Brolly Get`` quest) asks for 25 Common
    # Spines, which are farmable from Far Fields enemies and are not AP items.
    # Turning it in sets the vanilla hasBrolly flag used by Fourth Chorus's
    # encounter FSM even when the randomized Drifter's Cloak item is elsewhere.
    'Event: Flexile Spines Completed': (
        req(
            'Path: Far Fields - Seamstress',
            crest=False,
        ),
    ),
    # Wish completion events below represent monotonic vanilla quest state.
    # Their counters use farmable vanilla resources, so AP logic needs the
    # giver, objective and prerequisite routes rather than inventory items.
    'Event: Bone Bottom Repairs Completed': (
        req(
            'Path: Mosslands - Bone Bottom',
            'Event: Bell Beast Defeated',
            crest=False,
        ),
    ),
    'Event: Lifesaving Bridge Completed': (
        req(
            'Event: Bone Bottom Repairs Completed',
            'Event: Widow Defeated',
            crest=False,
        ),
        req(
            'Event: Bone Bottom Repairs Completed',
            'Path: Greymoor - Halfway House',
            crest=False,
        ),
    ),
    'Event: Other Courier Delivery Completed': (
        area(
            1,
            'Mosslands - Bone Bottom',
            'Path: Bellhart - Bellhart',
            'Event: Bell Beast Defeated',
            'Event: Missing Brother Rescued',
        ),
        area(
            3,
            'Mosslands - Bone Bottom',
            'Path: Bellhart - Bellhart',
        ),
        area(
            2,
            'Putrified Ducts - Fleatopia',
            'Path: Bellhart - Bellhart',
            'Event: Missing Brother Rescued',
            item_counts=(item_count(22, *FLEA_ITEMS),),
        ),
        area(
            1,
            "Far Fields - Pilgrim's Rest",
            'Path: Bellhart - Bellhart',
            'Event: Missing Brother Rescued',
        ),
        area(
            2,
            'Choral Chambers - Songclave',
            'Path: Bellhart - Bellhart',
            'Event: Missing Brother Rescued',
        ),
        area(
            3,
            'Choral Chambers - Songclave',
            'Path: Bellhart - Bellhart',
        ),
    ),
    'Event: Queen\'s Egg Delivered': (
        req(
            'Path: Bellhart - Bellhart',
            'Event: Missing Brother Rescued',
            'Event: Other Courier Delivery Completed',
            room_node_name(
                'sinner-s-road/sinner-s-road-styx-room#right'
            ),
            crest=False,
        ),
    ),
    'Event: Fine Pins Completed': (
        req(
            'Path: Choral Chambers - First Shrine',
            'Path: Choral Chambers - Songclave',
            crest=False,
        ),
    ),
    'Event: Building Up Songclave Completed': (
        req(
            'Path: Choral Chambers - First Shrine',
            'Path: Choral Chambers - Songclave',
            crest=False,
        ),
    ),
    'Event: Wandering Merchant Rescued': (
        req(
            'Path: Choral Chambers - Below Dining',
            'Path: Choral Chambers - Songclave',
            crest=False,
        ),
    ),
    'Event: Missing Courier Rescued': (
        req(
            # The Bellhart Wishwall starts the search. The actual rescue is
            # Aspid_01 immediately north of Bone Bottom. The Shellwood clue
            # chain is optional and must not gate completion.
            'Event: Widow Defeated',
            'Path: Bellhart - Bellhart',
            'Path: Mosslands - Bone Bottom',
            crest=False,
        ),
    ),
    'Event: Missing Brother Rescued': (
        req(
            'Event: Missing Courier Rescued',
            "Path: Sinner's Road - Broken Toll",
            # One vanilla activation route is an active Songclave.
            'Path: Choral Chambers - Songclave',
            crest=False,
        ),
        req(
            'Event: Missing Courier Rescued',
            "Path: Sinner's Road - Broken Toll",
            # Alternatively, accepting Great Taste from the Gourmand is
            # sufficient. Its giver is adjacent to the First Shrine.
            'Path: Choral Chambers - First Shrine',
            crest=False,
        ),
    ),
    'Event: Balm for the Wounded Completed': (
        req(
            # Meeting Sherma in Songclave and visiting Whiteward activates
            # the rescue scene in Ward_09.
            'Path: Choral Chambers - Songclave',
            'Path: Underworks - Whiteward',
            crest=False,
        ),
    ),
    'Event: Cloaks of the Choir Completed': (
        req(
            'Event: Building Up Songclave Completed',
            'Event: Fine Pins Completed',
            'Path: Choral Chambers - First Shrine',
            'Path: Choral Chambers - Songclave',
            crest=False,
        ),
    ),
    'Event: Strengthening Songclave Completed': (
        req(
            # Donation 2 is Donation 1 plus any three other verified
            # pre-Donation-2 Enclave-board completions.
            'Event: Building Up Songclave Completed',
            'Path: Choral Chambers - Songclave',
            crest=False,
            item_counts=(
                item_count(4, SONGCLAVE_BOARD_COMPLETION_ITEM),
            ),
        ),
    ),
    'Event: Whiteward Elevator Unlocked': (
        req(
            'Path: Choral Chambers - First Shrine',
            WHITE_KEY_ITEM,
            crest=False,
        ),
    ),
    'Event: Elegy of the Deep Learned': (
        req(
            'Elegy of the Deep',
            'Ancestral Art: Needolin',
            crest=False,
        ),
    ),
    'Event: Shrine Guardian Seth Defeated': (
        req(
            'Act: 3',
            'Path: Grand Gate',
            'Ancestral Art: Silk Soar',
            crest=False,
        ),
    ),
    'Event: Craw Summons Obtained': (
        req(
            'Act: 3',
            'Path: Mosslands - Ruined Chapel',
            'Event: Craw Lake Cleared',
            any_of=(
                'Path: Bellhart - Bellhart',
                'Path: Bilewater - Bellway',
                'Path: Far Fields - Bellway',
                'Path: Shellwood - Overgrown West',
                "Path: Sinner's Road - Styx",
                'Path: Greymoor - Wisp Thicket',
            ),
            crest=False,
        ),
    ),
    'Event: Cogwork Dancers Defeated': (
        req(
            'Path: Choral Chambers - High Halls Entrance',
            crest=False,
        ),
    ),
    'Event: Trobbio Defeated': (
        req(
            'Path: Outlying Citadel - Library',
            crest=False,
        ),
    ),
    'Event: Tormented Trobbio Defeated': (
        area(
            3,
            'Outlying Citadel - Library',
            'Progressive Claw Mirror',
            'Ancestral Art: Silk Soar',
        ),
    ),
    'Event: Five Bellshrines Rung': (
        req(
            *JUDGE_BELL_ITEMS,
            crest=False,
        ),
    ),
    'Event: Last Judge Defeated': (
        req(
            LAST_JUDGE_ROOM_EVENT,
            crest=False,
        ),
    ),
    'Event: Phantom Defeated': (
        req(
            'Path: Bilewater - Exhaust Organ',
            'Ancestral Art: Needolin',
            crest=False,
        ),
    ),
    'Event: Act 2 Started': (
        req(
            'Room Node: grand-gate/grand-bridge#room',
            crest=False,
        ),
        req(
            'Room Node: choral-chambers/grand-bellway#base',
            crest=False,
        ),
    ),
    'Event: Threefold Melody Learned': (
        req(
            'Event: Act 2 Started',
            *THREEFOLD_MELODY_ITEMS,
            'Ancestral Art: Clawline',
            'Ancestral Art: Needolin',
            crest=False,
        ),
    ),
    'Event: Cradle Opened': (
        req(
            'Event: Threefold Melody Learned',
            'Path: Outlying Citadel - Cogwork Core',
            'Ancestral Art: Cling Grip',
            'Ancestral Art: Clawline',
            crest=False,
        ),
    ),
    ACT_TWO_GOAL_EVENT: (
        req(
            'Event: Cradle Opened',
            'Path: The Cradle - Terminus',
            crest=False,
        ),
    ),
    CURSED_ENDING_GOAL_EVENT: (
        req(
            ACT_TWO_GOAL_EVENT,
            'Path: Shellwood - Greyroot',
            'Twisted Bud',
            crest=False,
        ),
    ),
    # Trail's End uses Shakra's carried stock by default. owned_maps
    # replaces those purchases with ownership of the same 14 map items.
    "Trail's End Maps": get_trails_end_map_requirements(),
    'Event: Trail\'s End Completed': get_trails_end_requirements(),
    'Event: Bellhart Full House Conversation': (
        req('Path: Bellhart - Bellhart', crest=False),
    ),
    'Event: Silk and Soul Offered': tuple(
        req(
            'Event: Act 2 Started',
            'Path: Putrified Ducts - Fleatopia',
            'Path: Choral Chambers - Songclave',
            'Event: Bellhart Full House Conversation',
            "Event: Trail's End Completed",
            'Ability: Faydown Cloak',
            SILK_AND_SOUL_LACE_DEFEATED_ITEM,
            crest=False,
            item_counts=tuple(
                count_requirement
                for count_requirement in (
                    item_count(
                        len(SILK_AND_SOUL_MANDATORY_EVENTS),
                        SILK_AND_SOUL_MANDATORY_WISH_ITEM,
                    ),
                    item_count(
                        full_point_count,
                        SILK_AND_SOUL_WISH_POINT_ITEM,
                    ),
                    (
                        item_count(
                            half_point_count,
                            SILK_AND_SOUL_WISH_HALF_POINT_ITEM,
                        )
                        if half_point_count
                        else None
                    ),
                )
                if count_requirement is not None
            ),
        )
        # The native target is 17 points. Full Wishes are one point and the
        # six supply/delivery Wishes are half a point, so only even half-point
        # thresholds change the minimum number of full Wishes.
        for full_point_count, half_point_count in (
            (17, 0),
            (16, 2),
            (15, 4),
            (14, 6),
        )
    ),
    'Event: Silk and Soul Completed': (
        req('Event: Silk and Soul Offered', 'Maiden Soul', 'Hermit Soul', 'Seeker Soul', 'Tool: Snare Setter', crest=False),
    ),
    'Event: Grand Mother Silk Snared': (
        req(
            'Event: Silk and Soul Completed',
            room_node_name('the-cradle/act2-gms-arena#arena')
            if MAPPER_GRAPH_ENABLED else 'Path: The Cradle - Terminus',
            'Combat: Grand Mother Silk',
            'Ancestral Art: Needolin',
            crest=False,
        ),
    ),
    'Event: Act 3 Started': (
        req('Event: Grand Mother Silk Snared', crest=False),
    ),
    # Three standard Old Hearts are used instead of the optional Verdania
    # substitute, which is not represented by the current path graph.
    'Event: Three Old Hearts Awakened': (
        req(
            'Act: 3',
            'Path: Abyss - Escape',
            'Pollen Heart',
            "Hunter's Heart",
            'Encrusted Heart',
            'Path: Mosslands - Snail Shamans',
            'Ancestral Art: Needolin',
            'Ancestral Art: Silk Soar',
            crest=False,
        ),
    ),
    'Event: Everbloom Obtained': (
        req(
            'Event: Three Old Hearts Awakened',
            'Path: Mosslands - Snail Shamans',
            crest=False,
        ),
    ),
    FINAL_GOAL_EVENT: (
        req(
            'Event: Everbloom Obtained',
            'Path: Deep Docks - Diving Bell',
            'Path: Abyss - Void Tendrils',
            'Ancestral Art: Silk Soar',
        ),
    ),
}

class _VersionedRequirementMap(
    dict[str, tuple[LocationRequirement, ...]]
):
    """Track graph mutations so cached reachability stays valid."""

    revision: int = 0

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.revision = 0

    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, value)
        self.revision += 1

    def __delitem__(self, key) -> None:
        super().__delitem__(key)
        self.revision += 1

    def clear(self) -> None:
        if self:
            super().clear()
            self.revision += 1

    def pop(self, key, *default):
        contained_key = key in self
        value = super().pop(key, *default)
        if contained_key:
            self.revision += 1
        return value

    def popitem(self):
        value = super().popitem()
        self.revision += 1
        return value

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        value = super().setdefault(key, default)
        self.revision += 1
        return value

    def update(self, *args, **kwargs) -> None:
        if args or kwargs:
            super().update(*args, **kwargs)
            self.revision += 1

    def __ior__(self, other):
        super().__ior__(other)
        self.revision += 1
        return self


LEDGE_GRAB_CAPABILITY_REQUIREMENT = 'Capability: Ledge Grab'
SWIM_CAPABILITY_REQUIREMENT = 'Capability: Swim'
INNATE_CAPABILITY_REQUIREMENTS = {
    LEDGE_GRAB_CAPABILITY_REQUIREMENT: (req(crest=False),),
    SWIM_CAPABILITY_REQUIREMENT: (req(crest=False),),
}
RANDOMIZED_INNATE_CAPABILITY_REQUIREMENTS = {
    LEDGE_GRAB_CAPABILITY_REQUIREMENT: (
        req('Ledge Grab', crest=False),
    ),
    SWIM_CAPABILITY_REQUIREMENT: (
        req('Swim', crest=False),
    ),
}

if MAPPER_GRAPH_ENABLED:
    EVENT_REQUIREMENTS[RITE_OF_REBIRTH_EVENT] = (
        req(POLLIP_RITE_ROOM_NODE, 'Event: Widow Defeated', 'Event: Mapper Rebirth Started', crest=False),
    )
    EVENT_REQUIREMENTS['Event: Everbloom Obtained'] = (
        req(room_event_name('event:mapper/owned/everbloom'), crest=False),
    )

PROFICIENT_COMBAT_REQUIREMENT = "Option: Proficient Combat"
PROFICIENT_COMBAT_REQUIREMENTS = (req(crest=False),)

@lru_cache(maxsize=2)
def eva_point_requirements(randomized_slots: bool):
    result = {
        source: (req(crest, *((slot,) if slot else ()), crest=False),)
        for source, crest, slot in EVA_POINT_SOURCES
    }
    for points in (12, 20, 27, 32):
        name = f'Event: Eva {points} Points'
        if randomized_slots:
            result[name] = (req(crest=False, item_counts=(item_count(points, EVA_POINT),)),)
        else:
            result[name] = tuple(
                req(*crests, crest=False, item_counts=(
                    (item_count(points - free, MEMORY_LOCKET_ITEM),) if points > free else ()
                ))
                for size in range(1, len(EVA_CREST_SLOTS) + 1)
                for crests in combinations(EVA_CREST_SLOTS, size)
                for free, locked in ((
                    sum(EVA_CREST_SLOTS[crest][0] for crest in crests),
                    sum(len(EVA_CREST_SLOTS[crest][1]) for crest in crests),
                ),)
                if free + locked >= points
            )
    return MappingProxyType(result)


EVENT_REQUIREMENTS.update({
    'Event: Hunt Combat Ready': (
        req(PROFICIENT_COMBAT_REQUIREMENT),
        req('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', item_counts=(item_count(3, 'Progressive Needle Upgrade'),)),
    ),
    'Event: Volatile Flintbeetles Completed': (
        _volatile_flintbeetle_act_one_requirement(crest=True),
    ),
    "Event: Pinmaster's Oil Completed": ROOM_CHECK_REQUIREMENTS["Wish: Pinmaster's Oil"],
    "Event: Pinmaster's Oil Point Earned": (
        req("Event: Pinmaster's Oil Completed", crest=False),
        req(item_counts=(item_count(2, PROGRESSIVE_NEEDLE_UPGRADE_ITEM),), crest=False),
    ),
    'Event: Silver Bells Completed': ROOM_CHECK_REQUIREMENTS['Wish: Silver Bells'],
    'Event: The Terrible Tyrant Completed': (
        req(room_node_name('bone-bottom/bone-bottom-town#ground-level'),
            room_node_name('the-marrow/the-marrow-skull-tyrant-arena#room'),
            'Ancestral Art: Cling Grip', 'Combat: Skull Tyrant (Bone Bottom)'),
    ),
    'Event: Wailing Mother Completed': (
        req(room_node_name('the-slab/slab-arena#arena'),
            room_event_name('event:mapper/260cb049-e57d-4d5e-8b29-983c717b1af5'),
            'Event: Strengthening Songclave Completed', 'Path: Choral Chambers - Songclave',
            'Ancestral Art: Cling Grip', 'Ability: Faydown Cloak',
            'Combat: Broodmother', 'Combat: Broodmother Gauntlet'),
    ),
    'Event: Bugs of Pharloom Completed': (),
})


ABSTRACT_REQUIREMENTS = _VersionedRequirementMap(
    {
        PROFICIENT_COMBAT_REQUIREMENT: (),
        "Option: Proficient Movement": (),
        "Option: Flea Brew Jump Logic": (),
        **{f"Technique: {technique} {tier}": ()
           for technique in ("Heal Stall", "Hazard Respawn", "Scuttlebrace", "Crest Pogo", "Needle Strike", "Enemy Pogo", "Drill Crystal Pogo", 'Flea Brew Stall', 'Flintslate Stall', 'Plasmium Phial Stall', 'Voltvessels Stall')
           for tier in (1, 2, 3)},
        "Capability: Has Any Map": tuple(req("Map: " + area, crest=False) for area in (
            "Mosslands", "The Marrow", "Deep Docks", "Far Fields", "Wormways", "Hunter's March",
            "Greymoor", "Bellhart", "Shellwood", "Blasted Steps", "Sinner's Road", "Mount Fay",
            "Sands of Karak", "Bilewater", "Weavenest Atla", "Grand Gate", "Underworks",
            "Choral Chambers", "Whispering Vaults", "Whiteward", "Cogwork Core", "Memorium",
            "High Halls", "The Slab", "Putrified Ducts", "The Cradle", "The Abyss", "Verdania",
        )),
        "Event: Selected Steel Soul Resting Sites Visited": (),
        "Option: Steel Soul On": (),
        "Option: Steel Soul Off": (req(crest=False),),
        "Option: Bellshrinesanity On": (),
        "Option: Bellshrinesanity Off": (req(crest=False),),
        **INNATE_CAPABILITY_REQUIREMENTS,
        **eva_point_requirements(True),
        **ACT_REQUIREMENTS,
        **EVENT_REQUIREMENTS,
        **PATH_REQUIREMENTS,
        **build_combat_requirements(req, item_count, CREST_ITEMS),
        **EQUIPPED_SILK_SKILL_REQUIREMENTS,
        **EQUIPPED_COLORED_TOOL_REQUIREMENTS,
        **{
            f'Damage: {kind}': tuple(
                req(
                    f"Usable {name.removeprefix('Tool: ')}"
                    if name.startswith('Tool: ') else name,
                    crest=False,
                )
                for name in names
            )
            for kind, names in (
                ('Searing', BROODFEAST_SEARED_TOOL_ITEMS),
                ('Shredding', BROODFEAST_SHREDDED_TOOL_ITEMS),
                ('Skewering', BROODFEAST_SKEWERED_TOOL_ITEMS),
            )
        },
        **ROOM_NODE_REQUIREMENTS,
        # The Bell Beast room event replaces the earlier path-derived event
        # of the same name.
        **ROOM_EVENT_REQUIREMENTS,
    }
)

MAPPER_UNRESOLVED_LEGACY_REFERENCES: frozenset[str] = frozenset()
if MAPPER_GRAPH_ENABLED:
    MAPPER_UNRESOLVED_LEGACY_REFERENCES = frozenset(
        name
        for alternatives in ABSTRACT_REQUIREMENTS.values()
        for alternative in alternatives
        for name in (*alternative.all_of, *alternative.any_of)
        if name.startswith(('Room Node: ', 'Room Event: ')) and name not in ABSTRACT_REQUIREMENTS
    )
    ABSTRACT_REQUIREMENTS.update({name: () for name in MAPPER_UNRESOLVED_LEGACY_REFERENCES})

BELLWAY_RANDOMIZED_STATIONS_REQUIREMENTS = (
    req(
        'Room Node: bone-bottom/bone-bottom-bellway#room'
        if MAPPER_GRAPH_ENABLED else 'Path: Mosslands - Bone Bottom',
        crest=False,
    ),
)

STARTING_LOCATION_VANILLA = 'vanilla'
STARTING_LOCATION_BONE_BOTTOM = 'bone_bottom'
SUPPORTED_STARTING_LOCATIONS = frozenset((
    STARTING_LOCATION_VANILLA,
    STARTING_LOCATION_BONE_BOTTOM,
))
MOSS_GROTTO_WITHOUT_START_ROOT_REQUIREMENTS = (
    PATH_REQUIREMENTS['Path: Mosslands - Moss Grotto'][1:]
)
BONE_BOTTOM_START_ROOT_REQUIREMENTS = (
    req(crest=False),
    *PATH_REQUIREMENTS['Path: Mosslands - Bone Bottom'],
)


def normalize_starting_location_key(starting_location: str) -> str:
    """Validate one concrete starting-location option key."""

    normalized = str(starting_location or '').strip().lower()
    if normalized not in SUPPORTED_STARTING_LOCATIONS:
        raise ValueError(
            f"Unknown Silksong starting location: {starting_location!r}"
        )
    return normalized


DONATION_CAPACITY_EVENTS: Mapping[str, str] = {
    'Room Event: event:mapper/reviewed:bone-bottom-repairs-capacity': 'Wish: Bone Bottom Repairs',
    'Room Event: event:mapper/reviewed:bone-bottom-bridge-capacity': 'Wish: A Lifesaving Bridge',
    'Room Event: event:mapper/reviewed:bone-bottom-statue-capacity': 'Wish: An Icon of Hope',
}


@lru_cache(maxsize=25)
def get_silk_and_soul_requirements(points: int = 17):
    points = max(0, min(24, points))
    template = ABSTRACT_REQUIREMENTS['Event: Silk and Soul Offered'][0]
    mandatory = template.item_counts[0]
    return tuple(
        replace(template, item_counts=(mandatory, *(
            (item_count(max(0, points - halves // 2), SILK_AND_SOUL_WISH_POINT_ITEM),)
            if points > halves // 2 else ()
        ), *((item_count(halves, SILK_AND_SOUL_WISH_HALF_POINT_ITEM),) if halves else ())))
        for halves in range(0, min(6, points * 2) + 1, 2)
    )


@lru_cache(maxsize=3)
def combat_requirement_overrides(proficient_combat: int):
    if proficient_combat == 2:
        return {PROFICIENT_COMBAT_REQUIREMENT: PROFICIENT_COMBAT_REQUIREMENTS}
    if proficient_combat == 1:
        overrides = {
            name: alternatives
            for name, alternatives in build_combat_requirements(
                req, item_count, CREST_ITEMS, tier_reduction=1
            ).items()
            if name.endswith(' Damage') or name.startswith('Combat: ')
        }
        overrides['Event: Hunt Combat Ready'] = (
            req(PROFICIENT_COMBAT_REQUIREMENT),
            req('Ancestral Art: Swift Step', 'Ability: Faydown Cloak',
                item_counts=(item_count(2, 'Progressive Needle Upgrade'),)),
        )
        return overrides
    return {}


def technique_requirement_overrides(
    heal_stall_tier: int,
    hazard_respawn_tier: int,
    scuttlebrace_tier: int,
    red_tool_stall_tier: int,
    crest_pogo_tier: int,
    needle_strike_tier: int,
    enemy_pogo_tier: int,
    drill_crystal_pogo_tier: int = 0,
) -> dict[str, tuple[LocationRequirement, ...]]:
    return {
        f"Technique: {name} {tier}": (req(crest=name == "Crest Pogo"),) if selected >= tier else ()
        for name, selected in (
            ("Heal Stall", heal_stall_tier),
            ("Hazard Respawn", hazard_respawn_tier),
            ("Scuttlebrace", scuttlebrace_tier),
            ("Crest Pogo", crest_pogo_tier),
            ("Needle Strike", needle_strike_tier),
            ("Enemy Pogo", enemy_pogo_tier),
            ("Drill Crystal Pogo", drill_crystal_pogo_tier),
            ("Flea Brew Stall", red_tool_stall_tier),
            ("Flintslate Stall", red_tool_stall_tier),
            ("Plasmium Phial Stall", red_tool_stall_tier),
            ("Voltvessels Stall", red_tool_stall_tier),
        )
        for tier in (1, 2, 3)
    }


def get_abstract_requirements(
    allow_bellways_before_bell_beast: bool = False,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    pollip_heart_count: int = 0,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    donation_tool_pouch_requirements: Mapping[str, int] | None = None,
    room_node_overrides: Mapping[str, tuple[LocationRequirement, ...]] | None = None,
) -> Mapping[str, tuple[LocationRequirement, ...]]:
    """Return the abstract graph used by the selected world options."""

    starting_location = normalize_starting_location_key(starting_location)
    trails_end_requirement = normalize_trails_end_requirement(
        trails_end_requirement
    )
    if pollip_heart_count not in (0, POLLIP_HEART_COUNT):
        raise ValueError(
            "Pollip Heart count must use the live quest threshold of "
            f"{POLLIP_HEART_COUNT} but received {pollip_heart_count!r}."
        )

    if (
        not room_node_overrides
        and silk_and_soul_points == 17
        and not allow_bellways_before_bell_beast
        and randomized_crest_slots_enabled
        and starting_location == STARTING_LOCATION_VANILLA
        and trails_end_requirement == TRAILS_END_REQUIREMENT_SHAKRA_STOCK
        and not pollip_heart_count
        and not randomize_ledge_grab
        and not randomize_swim
        and not proficient_combat
        and not proficient_movement
        and not flea_brew_jump_logic
        and sharpdart_logic
        and not heal_stall_tier
        and not hazard_respawn_tier
        and not scuttlebrace_tier
        and not red_tool_stall_tier
        and not crest_pogo_tier
        and not needle_strike_tier
        and not enemy_pogo_tier
        and not drill_crystal_pogo_tier
        and not bell_shrine_sanity
        and not steel_soul
        and not any(name in ABSTRACT_REQUIREMENTS for name in DONATION_CAPACITY_EVENTS)
    ):
        return ABSTRACT_REQUIREMENTS

    adjusted_requirements = dict(ABSTRACT_REQUIREMENTS)
    if steel_soul:
        adjusted_requirements["Option: Steel Soul On"] = (req(crest=False),)
        adjusted_requirements["Option: Steel Soul Off"] = ()
        from .game_modes import RESTING_SITES_VISITED, resting_site_requirements
        adjusted_requirements[RESTING_SITES_VISITED] = resting_site_requirements(steel_soul_sites)
    if room_node_overrides:
        adjusted_requirements.update(room_node_overrides)
    adjusted_requirements['Event: Silk and Soul Offered'] = get_silk_and_soul_requirements(silk_and_soul_points)
    if proficient_movement:
        adjusted_requirements["Option: Proficient Movement"] = PROFICIENT_COMBAT_REQUIREMENTS
    if flea_brew_jump_logic:
        adjusted_requirements["Option: Flea Brew Jump Logic"] = (req(crest=False),)
    if bell_shrine_sanity:
        adjusted_requirements["Option: Bellshrinesanity On"] = (req(crest=False),)
        adjusted_requirements["Option: Bellshrinesanity Off"] = ()
    adjusted_requirements.update(technique_requirement_overrides(
        heal_stall_tier, hazard_respawn_tier, scuttlebrace_tier,
        red_tool_stall_tier, crest_pogo_tier, needle_strike_tier, enemy_pogo_tier, drill_crystal_pogo_tier,
    ))
    adjusted_requirements.update(combat_requirement_overrides(proficient_combat))
    if randomize_ledge_grab:
        adjusted_requirements[LEDGE_GRAB_CAPABILITY_REQUIREMENT] = (
            RANDOMIZED_INNATE_CAPABILITY_REQUIREMENTS[
                LEDGE_GRAB_CAPABILITY_REQUIREMENT
            ]
        )
    if randomize_swim:
        adjusted_requirements[SWIM_CAPABILITY_REQUIREMENT] = (
            RANDOMIZED_INNATE_CAPABILITY_REQUIREMENTS[
                SWIM_CAPABILITY_REQUIREMENT
            ]
        )
    if allow_bellways_before_bell_beast:
        adjusted_requirements['Path: Bellways'] = (
            BELLWAY_RANDOMIZED_STATIONS_REQUIREMENTS
        )
    if not randomized_crest_slots_enabled:
        adjusted_requirements.update(eva_point_requirements(False))
        # Vanilla Crest Slots do not consume received AP slot items and their
        # Memory Locket spending is not represented in AP inventory logic.
        adjusted_requirements.update(
            VANILLA_CREST_SLOT_COLORED_TOOL_REQUIREMENTS
        )
    if starting_location == STARTING_LOCATION_BONE_BOTTOM:
        if MAPPER_GRAPH_ENABLED:
            for node in load_room_graph().assumptions['starting_nodes']:
                name = 'Room Node: ' + node
                adjusted_requirements[name] = tuple(
                    clause for clause in adjusted_requirements[name]
                    if clause != req(crest=False)
                )
            start = 'Room Node: bone-bottom/bone-bottom-town#ground-level'
            if start not in adjusted_requirements:
                raise ValueError('Mapper graph has no Bone Bottom starting node')
            adjusted_requirements[start] = (*adjusted_requirements[start], req(crest=False))
        # Replace the zero-requirement Moss Grotto root with Bone Bottom.
        # Every normal return route remains intact, so the fixed-point graph
        # derives Moss Grotto from its physical route back out of Bone Bottom.
        adjusted_requirements['Path: Mosslands - Moss Grotto'] = (
            MOSS_GROTTO_WITHOUT_START_ROOT_REQUIREMENTS
        )
        adjusted_requirements['Path: Mosslands - Bone Bottom'] = (
            BONE_BOTTOM_START_ROOT_REQUIREMENTS
        )
    if trails_end_requirement == TRAILS_END_REQUIREMENT_OWNED_MAPS:
        adjusted_requirements["Trail's End Maps"] = get_trails_end_map_requirements(trails_end_requirement)
        adjusted_requirements["Event: Trail's End Completed"] = (
            get_trails_end_requirements(trails_end_requirement)
        )
    if pollip_heart_count:
        adjusted_requirements[POLLIP_RITE_ROOM_NODE] = (
            _get_pollip_rite_room_requirements(pollip_heart_count)
        )
    capacity_events = DONATION_CAPACITY_EVENTS.keys() & adjusted_requirements.keys()
    if capacity_events:
        from .prices import get_shell_shard_donation_tool_pouch_requirements
        capacities = get_shell_shard_donation_tool_pouch_requirements({})
        if donation_tool_pouch_requirements is not None:
            capacities.update(donation_tool_pouch_requirements)
        for name in capacity_events:
            count = capacities[DONATION_CAPACITY_EVENTS[name]]
            if type(count) is not int or not 0 <= count <= 4:
                raise ValueError(f'Invalid donation Tool Pouch requirement: {count!r}')
            if count:
                adjusted_requirements[name] = tuple(
                    replace(clause, item_counts=(*clause.item_counts, item_count(count, 'Progressive Tool Pouch')))
                    for clause in adjusted_requirements[name]
                )
    if not sharpdart_logic:
        adjusted_requirements[USABLE_SHARPDART_REQUIREMENT] = ()
    return adjusted_requirements


MINOR_PICKUP_AREA_BY_SCENE: Mapping[str, tuple[int, str]] = {
    'ant_04_left': (1, "Hunter's March - Trap"),
    'aqueduct_01': (2, 'Putrified Ducts - Bellway'),
    'aqueduct_05_festival': (2, 'Putrified Ducts - Fleatopia'),
    'arborium_11': (2, 'Outlying Citadel - Memorium'),
    'bone_10': (1, 'The Marrow - Toll'),
    'bone_east_04b': (1, 'Deep Docks - Toll'),
    'bone_east_14': (1, "Far Fields - Pilgrim's Rest"),
    'bone_east_24': (3, 'Far Fields - Sprintmaster'),
    'cog_07': (3, 'Outlying Citadel - Lower Cogwork Core'),
    'cog_10': (2, 'Outlying Citadel - Cogwork Core'),
    'coral_03': (1, 'Blasted Steps - Toll'),
    'coral_36': (1, 'Blasted Steps - Bellway'),
    'crawl_02': (1, 'Wormways Middle'),
    'dock_02': (1, 'Deep Docks - Toll'),
    'dock_11': (3, 'Deep Docks - Diving Bell'),
    'dust_01': (1, "Sinner's Road - Broken Toll"),
    'dust_06': (1, "Sinner's Road - Styx"),
    'greymoor_05': (1, 'Greymoor - Halfway House'),
    'greymoor_12': (1, 'Greymoor - Wisp Thicket'),
    'greymoor_15': (1, 'Greymoor - Halfway House'),
    'greymoor_15b': (1, 'Greymoor - Halfway House'),
    'hang_06_bank': (2, 'Outlying Citadel - High Halls Ventrica'),
    'hang_16': (2, 'Outlying Citadel - High Halls Ventrica'),
    'library_02': (2, 'Outlying Citadel - Library'),
    'library_09': (2, 'Choral Chambers - Songclave'),
    'library_12': (2, 'Outlying Citadel - Library'),
    'mosstown_02': (1, 'The Marrow - Mosshome Gate'),
    'room_forge': (1, 'Deep Docks - Forge'),
    'shadow_02': (1, 'Bilewater - Bellway'),
    'shellwood_01': (1, 'Shellwood - Overgrown West'),
    'shellwood_01b': (1, 'Shellwood - Overgrown West'),
    'shellwood_13': (1, 'Shellwood - Greyroot'),
    'shellwood_25': (1, 'Shellwood - Central Toll'),
    'slab_02': (2, 'The Slab - Capture Event'),
    'slab_04': (2, 'The Slab - Capture Event'),
    'slab_18': (2, 'The Slab - Bellway'),
    'song_04': (2, 'Choral Chambers - Grand Bellway'),
    'song_07': (2, 'Choral Chambers - Below Dining'),
    'song_09': (2, 'Choral Chambers - First Shrine'),
    'tut_01': (1, 'Mosslands - Moss Grotto'),
    'under_03': (2, 'Underworks - Broken Elevator'),
    'under_07c': (2, 'Underworks - Confession Toll'),
    'under_12': (2, 'Underworks - Twelfth Architect'),
    'under_17': (2, "Underworks - Architect's Shop"),
    'under_18': (2, 'Underworks - Whiteward'),
    'wisp_02': (1, 'Greymoor - Wisp Thicket'),
    'wisp_03': (1, 'Greymoor - Wisp Thicket'),
}


def _minor_pickup_requirement(location_name: str) -> LocationRequirement:
    _source_location_name, scene_name = next(
        (source_name, scene_name)
        for source_name, scene_name, _asset, _x, _y
        in MINOR_PICKUP_SOURCE
        if canonicalize_location_name(source_name) == location_name
    )
    if scene_name == 'tut_01':
        return area(1, 'Mosslands - Moss Grotto', crest=False)
    if scene_name == 'slab_22':
        return req(
            'Act: 2',
            room_node_name("the-slab/slab-chilly-top#room"),
            'Ancestral Art: Cling Grip',
            'Swift Step',
            act='Act 2',
        )
    act_number, path_name = MINOR_PICKUP_AREA_BY_SCENE[scene_name]
    if scene_name == 'dock_11':
        return area(
            act_number,
            path_name,
            'Ancestral Art: Clawline',
        )
    if scene_name == 'cog_07':
        return area(
            act_number,
            path_name,
            'Ancestral Art: Silk Soar',
        )
    if scene_name == 'cog_10':
        return area(
            act_number,
            path_name,
            'Ability: Faydown Cloak',
        )
    if scene_name == 'hang_06_bank':
        return area(
            act_number,
            path_name,
            SIMPLE_KEY_ROSARY_BANK,
        )
    return area(act_number, path_name)


# These are coarse area-entry gates. Every cache has a room and coordinate,
# but its room-to-room movement requirement is not represented. Keeping these
# checks junk-only provides map opacity without allowing an inferred route to
# carry progression.
MINOR_CACHE_AREA_BY_MAP_REGION: Mapping[str, tuple[int, str]] = {
    'Tut': (1, 'Mosslands - Moss Grotto'),
    'Moss_Cave': (1, 'Mosslands - Moss Grotto'),
    'Mosstown': (1, 'The Marrow - Mosshome Gate'),
    'Bonetown': (1, 'Mosslands - Bone Bottom'),
    'Bone': (1, 'The Marrow - Toll'),
    'Ant': (1, "Hunter's March - Trap"),
    'Dock': (1, 'Deep Docks - Toll'),
    'Wilds': (1, 'Far Fields - Bellway'),
    'Greymoor': (1, 'Greymoor - Halfway House'),
    'Shellwood': (1, 'Shellwood - Overgrown West'),
    'Wisp': (1, 'Greymoor - Wisp Thicket'),
    'Dust': (1, "Sinner's Road - Broken Toll"),
    'Blasted_Steps': (1, 'Blasted Steps - Bellway'),
    'Coral_Caves': (1, 'Sands of Karak - Sands of Karak'),
    'Swamp': (1, 'Bilewater - Bellway'),
    'Belltown': (1, 'Bellhart - Bellhart'),
    'Song_Gate': (2, 'Grand Gate'),
    'Under': (2, 'Underworks - Broken Elevator'),
    'Ward': (2, 'Underworks - Whiteward'),
    'Song': (2, 'Choral Chambers - Grand Bellway'),
    'Library': (2, 'Outlying Citadel - Library'),
    'Hang': (2, 'Outlying Citadel - High Halls Ventrica'),
    'Arborium': (2, 'Outlying Citadel - Memorium'),
    'Aqueduct': (2, 'Putrified Ducts - Bellway'),
    'Slab': (2, 'The Slab - Capture Event'),
    'Peak': (2, 'Mount Fay - Shakra'),
    'Cradle': (2, 'The Cradle - Terminus'),
    'Abyss': (3, 'Abyss - Void Tendrils'),
}


def _minor_cache_requirement(location_name: str) -> LocationRequirement:
    source = next(
        source
        for source in MINOR_CACHE_SOURCE
        if canonicalize_location_name(source[0]) == location_name
    )
    source_location_name = source[0]
    map_region = source[9]
    scene_name = source[2].casefold()
    if scene_name == 'bone_east_14':
        return area(1, "Far Fields - Pilgrim's Rest")
    if scene_name == 'bone_east_24':
        return area(3, 'Far Fields - Sprintmaster')
    if source_location_name in {
        'Deep Docks - Shell Shard Cache #1',
        'Deep Docks - Shell Shard Cache #2',
        'Deep Docks - Shell Shard Cache #3',
    }:
        return area(
            1,
            'Deep Docks - Lower',
            USABLE_MAGMA_BELL_REQUIREMENT,
            crest=False,
        )
    if scene_name == 'dock_02b':
        return area(1, 'Deep Docks - Lower')
    act_number, path_name = MINOR_CACHE_AREA_BY_MAP_REGION[map_region]
    if scene_name == 'hang_06_bank':
        return area(
            act_number,
            path_name,
            SIMPLE_KEY_ROSARY_BANK,
        )
    if source_location_name == 'Blasted Steps - Rosary Cache':
        return area(
            act_number,
            path_name,
            SWIFT_STEP_ITEM,
        )
    if source_location_name == 'Moss Grotto - Rosary Cache':
        return area(
            act_number,
            path_name,
            SWIFT_STEP_ITEM,
        )
    if source_location_name in {
        'Shellwood - Shell Shard Cache #4',
        'Shellwood - Shell Shard Cache #5',
        'Shellwood - Shell Shard Cache #6',
    }:
        return area(
            1,
            'Shellwood - Central Toll',
            any_of=SHELLWOOD_LONGPIN_MOVEMENT_ITEMS,
        )
    if source_location_name in {
        'Bone Bottom - Rosary Cache #6',
        'Bone Bottom - Rosary Cache #7',
    }:
        # These Bonegrave caches use Wormways-side access like the nearby
        # sources rather than the room graph's incorrect upper-right-exit
        # geometry.
        return area(1, 'Mosslands - Bonegrave')
    if source_location_name in {
        'Bonegrave - Rosary Cache #1',
        'Bonegrave - Rosary Cache #2',
        'Bonegrave - Rosary Cache #3',
        'Bonegrave - Rosary Cache #4',
    }:
        # These four caches are inside the Wanderer chapel before its combat.
        # The client keeps the chapel door open while any of them is in-seed,
        # so acquiring Wanderer Crest elsewhere cannot invalidate this route.
        return area(1, 'Mosslands - Bonegrave')
    if source_location_name in {
        'The Marrow - Rosary Cache #14',
        'The Marrow - Rosary Cache #15',
        'The Marrow - Rosary Cache #16',
        'The Marrow - Shell Shard Cache #4',
        'The Marrow - Shell Shard Cache #5',
        'The Marrow - Shell Shard Cache #6',
    }:
        # These exact Bone_07/Bone_14/Bone_19 sources are all in the
        # Lower-Pogo, Mr-Burns-house and Upper-Pogo branch beyond the
        # Shooting Gallery rather than in the opening Toll section.
        return area(1, 'The Marrow - Shooting Gallery')
    if source_location_name in {
        'Greymoor - Rosary Cache #7',
        'Greymoor - Rosary Cache #8',
        'Greymoor - Rosary Cache #10',
        'Greymoor - Rosary Cache #11',
        'Greymoor - Rosary Cache #12',
        'Greymoor - Rosary Cache #13',
        'Greymoor - Rosary Cache #14',
        'Greymoor - Shell Shard Cache #1',
        'Greymoor - Shell Shard Cache #2',
    }:
        return area(
            act_number,
            path_name,
            SWIFT_STEP_ITEM,
        )
    return area(
        act_number,
        path_name,
        crest=map_region != 'Tut',
    )

LAST_AUDIENCE_REQUIREMENTS = tuple(
    area(
        2,
        'Outlying Citadel - High Halls Ventrica',
        room_node_name('cogwork-core/cogwork-core-second-sentinel#shard-bundle-check'),
        'Path: Choral Chambers - Songclave',
        *route,
    )
    for route in (
        (
            room_node_name('choral-chambers/memorium-entrance-tunnel#base'),
            room_node_name('choral-chambers/choral-chambers-east-to-west#left-side'),
            room_node_name('choral-chambers/choral-chambers-east-to-west#right-side'),
            "Conductor's Melody",
            'Event: Building Up Songclave Completed',
        ),
        (
            room_node_name('choral-chambers/memorium-entrance-tunnel#base'),
            'Event: Everbloom Obtained',
        ),
    )
)

PINSTRESS_BATTLE_REQUIREMENT = area(
    3,
    'Mount Fay - Workbench',
    'Path: Blasted Steps - Pinstress',
    'Ability: Needle Strike',
    'Ancestral Art: Silk Soar',
    'Ancestral Art: Needolin',
    "Ability: Drifter's Cloak",
)

REQUIREMENT_ROW_SOURCE: tuple[tuple[str, LocationRequirement], ...] = (
    # STARTING LOCATIONS
    ('Crest Unlock: Hunter', req(crest=False)),  # No act/path gate: bootstrap row.

    # SIMPLE KEYS
    # The Bone Bottom stock moves to Grindle if it remains unbought in Act 3.
    # Both vendors therefore report one stable AP source.
    ('Simple Key: Bone Bottom Shop', area(
        1,
        'Mosslands - Bone Bottom',
    )),
    *(
        ('Simple Key: Bone Bottom Shop', requirement)
        for requirement in grindle_access(3)
    ),
    ('Simple Key: Roachkeeper', area(
        1,
        "Sinner's Road - Styx",
        'Ability: Faydown Cloak',
    )),
    ('Simple Key: Songclave Shop', area(
        2,
        'Choral Chambers - Songclave',
        'Event: Wandering Merchant Rescued',
    )),
    ('Simple Key: Sands of Karak East Bench', area(
        1,
        'Sands of Karak - Sands of Karak',
        'Ability: Faydown Cloak',
    )),

    # ACT 1
    # Mosslands
    ('Tool Unlock: Rosary Magnet', area(1, 'Mosslands - Bone Bottom')),
    ('Tool Unlock: Mosscreep Tool 1', area(
        1,
        'Mosslands - Moss Druid',
        silk_spear=True,
        item_counts=(item_count(3, MOSSBERRY_ITEM),),
    )),
    ('Tool Unlock: Mosscreep Tool 1', area(
        1,
        'Mosslands - Moss Druid',
        any_of=(
            *SWIFT_STEP_OR_SPRINT_ITEMS,
            'Ability: Faydown Cloak',
            USABLE_SHARPDART_REQUIREMENT,
        ),
        item_counts=(item_count(3, MOSSBERRY_ITEM),),
    )),
    ('Crest Unlock: Wanderer', area(1, 'Mosslands - Bonegrave')),

    # Weavenest Atla
    ('Tool Unlock: Silk Snare', area(1, 'Weavenest - Atla', 'Ancestral Art: Cling Grip', 'Ability: Faydown Cloak')),
    ('Tool Unlock: White Ring', area(1, 'Weavenest - Atla')),

    # The Marrow
    ('Tool Unlock: Bone Necklace', area(1, 'The Marrow - Toll')),
    ('Tool Unlock: Compass', area(1, 'The Marrow - Toll')),
    ('Skill Unlock: Quill', area(1, 'The Marrow - Toll')),
    ('Spell Unlock: Silk Spear', area(1, 'The Marrow - Mosshome Gate')),
    ('Tool Unlock: Straight Pin', area(1, 'The Marrow - Shooting Gallery')),

    ('Save Flea: The Marrow (Tangle)', area(
        1,
        'The Marrow - Bellshrine',
        'Event: Bell Beast Defeated',
    )),

    # Hunter's March
    ('Tool Unlock: Curve Claws', area(1, "Hunter's March - Trap", any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline'))),
    # Mottled Child's second throwing reward upgrades Curveclaw. Its source
    # and base-tool prerequisite are represented. The final vertical route
    # through Bone_East_22 cannot hold progression until its minimum movement
    # requirement is represented.
    ('Curvesickle', area(
        1,
        'Far Fields - Bellway',
        'Progressive Curveclaw',
    )),
    ('Tool Unlock: Fractured Mask', area(1, "Hunter's March - Trap", any_of=('Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline'))),
    ('Crest Unlock: Beast', area(1, "Hunter's March - Trap", "Ability: Drifter's Cloak")),

    ("Save Flea: Hunter's March (Yapper)", area(1, "Hunter's March - Trap")),

    # Deep Docks
    # Swift Step is obtained in northern Deep Docks before the dash-gated
    # Bellshrine/Lace route.
    ('Skill Unlock: Dash', area(1, 'Deep Docks - Toll')),
    ('Tool Unlock: WebShot Forge', area(
        1,
        'Deep Docks - Forge',
        'Ruined Tool',
        CRAFTMETAL_ITEM,
    )),
    ('Tool Unlock: Sting Shard', area(
        1,
        'Deep Docks - Forge',
        CRAFTMETAL_ITEM,
    )),
    ('Tool Unlock: Lava Charm', area(
        1,
        'Deep Docks - Forge',
        CRAFTMETAL_ITEM,
    )),
    ('Tool Unlock: Flintstone', area(1, 'Deep Docks - Lower', any_of=("Ability: Drifter's Cloak", 'Ancestral Art: Swift Step', 'Ability: Faydown Cloak', 'Ancestral Art: Clawline'))),

    ('Save Flea: Deep Docks Bellway (Eepy)', area(1, 'Deep Docks - Bellshrine')),
    ('Save Flea: Deep Docks Weaver Burial Spire (Squeesh)', area(1, 'Deep Docks - Toll', 'Ancestral Art: Swift Step')),
    ('Save Flea: Deep Docks Mines (Le Bomba)', area(
        1,
        'Deep Docks - Lower',
        'Ancestral Art: Clawline',
        any_of=(
            'Ancestral Art: Cling Grip',
            USABLE_SCUTTLEBRACE_REQUIREMENT,
            'Ancestral Art: Silk Soar',
        ),
    )),

    # Far Fields
    ("Skill Unlock: Drifter's Cloak", area(1, 'Far Fields - Seamstress')),
    ('Tool Unlock: Weighted Anklet', area(1, "Far Fields - Pilgrim's Rest")),
    ('Tool Unlock: Sprintmaster', area(
        1,
        'Weavenest - Cindril',
        any_of=SWIFT_STEP_OR_SPRINT_ITEMS,
    )),
    ('Tool Unlock: Bell Bind', area(1, 'Far Fields - Bellway')),

    ("Save Flea: Pilgrim's Rest (Sleeby)", area(1, "Far Fields - Pilgrim's Rest", "Ability: Drifter's Cloak", 'Ancestral Art: Cling Grip')),
    ('Save Flea: Far Fields Captured (Thoughtless)', area(
        1,
        'Far Fields - Bellway',
    )),

    # Wormways
    ('Spell Unlock: Silk Charge', area(
        1,
        'Wormways - Bottom',
        'Ancestral Art: Needolin',
        'Ancestral Art: Clawline',
    )),
    ('Spell Unlock: Silk Charge', area(
        1,
        'Wormways - Bottom',
        'Ancestral Art: Needolin',
        'Ancestral Art: Swift Step',
        "Ability: Drifter's Cloak",
    )),
    ('Tool Unlock: Dead Mans Purse', area(1, 'Wormways - Bottom')),
    ('Tool Unlock: Extractor', area(1, 'Wormways - Plasmium Lab')),
    ('Tool Unlock: Lifeblood Syringe', area(
        1,
        'Wormways - Plasmium Lab',
        USABLE_NEEDLE_PHIAL_REQUIREMENT,
        crest=False,
    )),

    ('Save Flea: Wormways (Snacc)', area(1, 'Wormways - Bottom')), # Simple spike pogo

    # Shellwood
    ('Skill Unlock: Wall Jump', area(1, 'Shellwood - Central Toll')),
    ('Tool Unlock: Harpoon', area(
        1,
        'Shellwood - Central Toll',
        any_of=SHELLWOOD_LONGPIN_MOVEMENT_ITEMS,
    )),
    ('Tool Unlock: Poison Pouch', area(1, 'Shellwood - Greyroot')),

    ('Save Flea: Shellwood (Shelly)', area(1, 'Shellwood - Overgrown West')),

    # Bellhart
    ('Tool Unlock: Multibind', area(
        1,
        'Bellhart - Bellhart',
        'Event: Missing Courier Rescued',
    )),
    ('Skill Unlock: Needolin', area(1, 'Bellhart - Widow')),

    ('Save Flea: Bellhart (Bellphy)', area(
        1,
        'Shellwood - Central Toll',
        'Ancestral Art: Cling Grip',
    )),

    # Greymoor
    ('Tool Unlock: Flea Brew', area(
        1,
        'Greymoor - Halfway House',
        item_counts=(item_count(5, *FLEA_ITEMS),),
    )),
    ('Crest Unlock: Reaper', area(
        1,
        'Greymoor - Halfway House',
        SWIFT_STEP_ITEM,
    )),
    ('Spell Unlock: Thread Sphere', area(
        1,
        'Greymoor - Bellshrine',
        'Event: Craw Lake Cleared',
    )),
    ('Tool Unlock: Tri Pin', area(
        1,
        'Greymoor - Bellshrine',
        'Event: Craw Lake Cleared',
    )),
    ('Tool Unlock: Pimpilo', area(
        1,
        'Greymoor - Bellshrine',
        CRAFTMETAL_ITEM,
    )),
    ('Crest Unlock: Witch', area(
        2,
        'Greymoor - Halfway House',
        RITE_OF_REBIRTH_EVENT,
    )),
    ('Tool Unlock: Wisp Lantern', area(1, 'Greymoor - Wisp Thicket')),

    # The confirmed upper-tower route needs the complete movement set below.
    # Neither Cling Grip plus full Swift Step nor Faydown plus Cling alone can
    # make the final crossings to Snoozles.
    ('Save Flea: Greymoor Tower (Snoozles)', area(
        1,
        'Greymoor - Halfway House',
        'Ancestral Art: Cling Grip',
        'Ability: Faydown Cloak',
        SWIFT_STEP_ITEM,
        'Ancestral Art: Clawline',
    )),
    ('Save Flea: Greymoor Craw Lake (Gwah)', area(
        1,
        'Greymoor - Bellshrine',
        'Event: Craw Lake Cleared',
    )),
    ('Flea: Greymoor - Kratt', area(
        1,
        'Greymoor - Halfway House',
        'Ancestral Art: Cling Grip',
    )),

    # Blasted Steps
    ('Skill Unlock: Charge Slash', area(1, 'Blasted Steps - Pinstress')),
    ('Tool Unlock: Magnetite Dice', area(1, 'Blasted Steps - Bellway')),  # Magnetite Dice Act 1 source: Lumble the Lucky.
    *(
        ('Tool Unlock: Magnetite Dice', requirement)
        for requirement in grindle_access(3)
    ),
    # Grindle requires Cling Grip after entering Blasted Steps, plus either
    # Silk Soar or Faydown Cloak for the remaining climb.
    *(
        ('Tool Unlock: Thief Charm', requirement)
        for requirement in grindle_access(1)
    ),
    *(
        ('Tool Unlock: Thief Claw', requirement)
        for requirement in grindle_access(
            1,
            'Ancestral Art: Clawline',
        )
    ),

    ('Save Flea: Blasted Steps (Nini)', area(1, 'Blasted Steps - Bellway', 'Ancestral Art: Cling Grip')),

    # Sands of Karak
    ('Tool Unlock: Conch Drill', area(1, 'Sands of Karak - Coral Tower')),
    ('Tool Unlock: Zap Imbuement', area(1, 'Sands of Karak - Sands of Karak')),

    ('Save Flea: Sands of Karak (Crustly)', area(
        1,
        'Sands of Karak - Coral Tower',
    )),

    # Sinner's Road
    # Tacks' ordinary source is the pre-Act-3 Roach Guts Wish from Crull and
    # Benjin. Its free corpse pickup is only the Act 3 fallback. Dust_Shack is
    # entered directly from Dust_04, represented by the Broken Toll node. The
    # ten unrandomized Muckroach drops add no AP inventory requirement.
    ('Tool Unlock: Tack', area(1, "Sinner's Road - Broken Toll")),
    ('Tool Unlock: Barbed Wire', area(1, "Sinner's Road - Broken Toll", "Ability: Drifter's Cloak")),

    ("Save Flea: Sinner's Road (Stelf)", area(1, "Sinner's Road - Styx")),


    #Bilewater
    ('Ruined Tool', area(1, 'Bilewater - Ruined Tool')),
    ('Spell Unlock: Parry', area(1, 'Bilewater - Exhaust Organ')),
    ('Tool Unlock: Quick Sling', area(
        1,
        'Bilewater - Bellway',
        'Ability: Faydown Cloak',
        'Ancestral Art: Cling Grip',
    )),
    # Trail's End is completed before Silk and Soul can begin. Shakra Ring is
    # awarded before Act 3, so it depends on Trail's End rather than later
    # Shakra inventory.
    ('Tool Unlock: Shakra Ring', req("Event: Trail's End Completed")),

    ('Save Flea: Exhaust Organ (Rangle)', area(
        1,
        'Bilewater - Exhaust Organ',
    )),
    ('Save Flea: Bilehaven (Spangle)', area(
        1,
        'Bilewater - Corpse Sack Chamber',
        'Ancestral Art: Cling Grip',
    )),
    ('Save Flea: Bilewater Thieves (Cower)', area(
        1,
        'Bilewater - Twisted Bud',
    )),

    # ACT 2
    # Underworks
    ('Tool Unlock: WebShot Architect', area(
        2,
        "Underworks - Architect's Shop",
        'Ruined Tool',
        CRAFTMETAL_ITEM,
    )),  # Ruined Tool + Twelfth Architect repair.
    ('Tool Unlock: Screw Attack', area(2, 'Underworks - Broken Elevator')),
    ('Skill Unlock: Harpoon', area(
        2,
        'Underworks - Twelfth Architect',
        "Ability: Drifter's Cloak",
        'Ancestral Art: Cling Grip',
        'Ancestral Art: Swift Step',
    )),
    ('Skill Unlock: Harpoon', area(
        2,
        'Underworks - Twelfth Architect',
        "Ability: Drifter's Cloak",
        'Ancestral Art: Cling Grip',
        'Ability: Faydown Cloak',
    )),
    ('Tool Unlock: Quickbind', area(2, 'Underworks - Whiteward')),
    ('Crest Unlock: Architect', area(
        2,
        "Underworks - Architect's Shop",
        ARCHITECTS_KEY_ITEM,
    )),
    ('Tool Unlock: Cogwork Saw', area(
        2,
        "Underworks - Architect's Shop",
        CRAFTMETAL_ITEM,
    )),
    ('Tool Unlock: Scuttlebrace', area(
        2,
        "Underworks - Architect's Shop",
        CRAFTMETAL_ITEM,
    )),
    ('Tool Unlock: Brolly Spike', area(
        2,
        "Underworks - Architect's Shop",
        CRAFTMETAL_ITEM,
    )),

    ('Save Flea: Underworks (Boomy)', area(
        2,
        'Underworks - Twelfth Architect',
    )),
    ('Save Flea: Wisp Thicket (Fidget)', area(
        2,
        'Greymoor - Wisp Thicket',
        'Ancestral Art: Cling Grip',
        'Ability: Faydown Cloak',
    )),

    # Choral Chambers
    # Claw Mirror is Trobbio's direct drop at the Stage. Its explicit boss
    # event also receives any later Trobbio route changes.
    ('Tool Unlock: Dazzle Bind', area(
        2,
        'Outlying Citadel - Library',
        'Event: Trobbio Defeated',
    )),
    # Tormented Trobbio's direct reward is the second Claw Mirror tier. These
    # use the same route requirements as the boss encounter itself.
    ('Dark Mirror', area(
        3,
        'Outlying Citadel - Library',
        'Progressive Claw Mirror',
        'Ancestral Art: Silk Soar',
    )),
    ('Tool Unlock: Musician Charm', area(
        2,
        'Choral Chambers - Songclave',
        'Path: Outlying Citadel - Memorium',
        'Event: Wandering Merchant Rescued',
        'Ability: Faydown Cloak',
    )),
    ('Tool Unlock: Wallcling', area(
        2,
        'Choral Chambers - Songclave',
        'Event: Wandering Merchant Rescued',
    )),
    ('Tool Unlock: Spool Extender', area(
        2,
        'Choral Chambers - Songclave',
        'Event: Wandering Merchant Rescued',
    )),
    ('Tool Unlock: Lightning Rod', area(2, 'Outlying Citadel - Memorium')),

    ('Save Flea: Choral Cambers Spa (Oowa)', area(
        2,
        'Choral Chambers - Spa',
    )),
    ('Save Flea: Choral Cambers Walled (Mimi)', area(
        2,
        'Choral Chambers - Below Dining',
    )),
    ('Save Flea: Songclave (Groggy)', area(
        2,
        'Outlying Citadel - Library',
        'Ancestral Art: Cling Grip',
        'Ancestral Art: Clawline',
    )),
    ('Save Flea: Whispering Vaults (Birdy)', area(
        2,
        'Outlying Citadel - Library',
        'Ancestral Art: Cling Grip',
    )),
    ('Flea: Memorium - Huge Flea', area(
        2,
        'Outlying Citadel - Memorium',
        'Ability: Faydown Cloak',
    )),

    # High Halls
    *(("Tool Unlock: Reserve Bind", rule) for rule in LAST_AUDIENCE_REQUIREMENTS),
    *(
        ('Tool Unlock: Reserve Bind', requirement)
        for requirement in grindle_access(1)
    ),
    ('Tool Unlock: Rosary Cannon', area(
        2,
        'Outlying Citadel - High Halls Ventrica',
        SIMPLE_KEY_ROSARY_BANK,
    )),
    ('Tool Unlock: Cogwork Flier', area(
        2,
        'Outlying Citadel - High Halls Ventrica',
        'Ancestral Art: Clawline',
        CRAFTMETAL_ITEM,
    )),

    # Putrified Ducts
    ('Tool Unlock: Longneedle', area(
        2,
        'Putrified Ducts - Huntress',
        item_counts=(
            item_count(1, *BROODFEAST_SEARED_TOOL_ITEMS),
            item_count(1, *BROODFEAST_SHREDDED_TOOL_ITEMS),
            item_count(1, *BROODFEAST_SKEWERED_TOOL_ITEMS),
        ),
    )),
    ('Tool Unlock: Maggot Charm', area(
        2,
        'Putrified Ducts - Bellway',
    )),
    ('Flea: Putrified Ducts - Vog', area(
        2,
        'Putrified Ducts - Bellway',
        'Ability: Faydown Cloak',
    )),
    ('Tool Unlock: Flea Charm', req(
        'Path: Putrified Ducts - Fleatopia',
        item_counts=(item_count(MAX_FLEA_HUNT_GOAL_COUNT, *FLEA_ITEMS),),
    )),

    # Mount Fay
    ('Tool Unlock: WebShot Weaver', area(
        2,
        'Mount Fay - Workbench',
        'Ruined Tool',
        CRAFTMETAL_ITEM,
    )),  # Needs Ruined Tool, Craftmetal, then Mount Fay repair.
    ('Skill Unlock: Double Jump', area(2, 'Mount Fay - Workbench', 'Ancestral Art: Needolin', "Ability: Drifter's Cloak")),  # Faydown Cloak summit requires Needolin. Harpoon and Drifter's Cloak are in Path: Mount Fay.
    ('Tool Unlock: Pinstress Tool', PINSTRESS_BATTLE_REQUIREMENT),
    ('Tool Unlock: Revenge Crystal', area(2, 'Mount Fay - Toll')),

    ('Save Flea: Mount Fay (Ice Cube)', area(
        2,
        'Mount Fay - Final Climb',
        'Ancestral Art: Cling Grip',
    )),

    # The Slab
    ('Spell Unlock: Silk Bomb', area(
        2,
        'The Slab - Bellway',
        'Path: Putrified Ducts - Huntress',
        'Ability: Faydown Cloak',
    )),

    ('Save Flea: The Slab Cell (Sway)', req(
        'Act: 2',
        room_node_name("the-slab/slab-flea-cell#room"),
        act='Act 2',
    )),
    ('Save Flea: The Slab Bellway (Honk Shoo)', area(
        2,
        'The Slab - Bellway',
        'Ability: Faydown Cloak',
    )),

    # The second Moss Druid reward is claimed from the same physical room as
    # the first. The seven randomized Mossberries are its actual gate. Some of
    # those berries may naturally place it late without inventing an Act 3
    # Abyss source.
    ('Tool Unlock: Mosscreep Tool 2', area(
        1,
        'Mosslands - Moss Druid',
        item_counts=(item_count(7, MOSSBERRY_ITEM),),
    )),

    # ACT 3
    ('Crest Unlock: Shaman', area(3, 'Mosslands - Ruined Chapel')),
    ('Spell Unlock: Silk Boss Needle', area(3, 'Abyss - Void Tendrils')),  # Pale Nails requires Act 3 return using Silk Soar.
    ('Skill Unlock: Silk Soar', area(3, 'Abyss - Void Tendrils', 'Ancestral Art: Needolin')),

    # Rosary prices are grindable and therefore are not AP inventory gates.
    ('Pinmaster Plinney: Sharpened Needle', req(
        'Event: Widow Defeated',
    )),
    ('Pinmaster Plinney: Shining Needle', req(
        'Event: Widow Defeated',
        item_counts=(
            item_count(1, PROGRESSIVE_NEEDLE_UPGRADE_ITEM),
            item_count(1, PALE_OIL_ITEM),
        ),
    )),
    ('Pinmaster Plinney: Hivesteel Needle', req(
        'Event: Widow Defeated',
        item_counts=(
            item_count(2, PROGRESSIVE_NEEDLE_UPGRADE_ITEM),
            item_count(2, PALE_OIL_ITEM),
        ),
    )),
    ('Pinmaster Plinney: Pale Steel Needle', req(
        'Event: Widow Defeated',
        item_counts=(
            item_count(3, PROGRESSIVE_NEEDLE_UPGRADE_ITEM),
            item_count(3, PALE_OIL_ITEM),
        ),
    )),
    ('Pale Oil: Whispering Vaults', area(
        2,
        'Outlying Citadel - Library',
        'Ancestral Art: Cling Grip',
    )),
    ('Pale Oil: Great Taste of Pharloom', area(
        2,
        'Choral Chambers - Below Dining',
        'Event: Last Judge Defeated',
        'Path: Mosslands - Moss Druid',
        'Path: Greymoor - Halfway House',
        "Path: Far Fields - Pilgrim's Rest",
        "Path: Sinner's Road - Styx",
        'Path: Sands of Karak - Sands of Karak',
        SWIFT_STEP_ITEM,
        'Ancestral Art: Cling Grip',
        'Ancestral Art: Clawline',
        'Ability: Faydown Cloak',
    )),
    ('Pale Oil: Ecstasy of the End', area(
        3,
        'Putrified Ducts - Fleatopia',
        'Tool: Egg of Flealia',
        item_counts=(item_count(MAX_FLEA_HUNT_GOAL_COUNT, *FLEA_ITEMS),),
    )),

    # SHAKRA PINS
    # Rosary prices are grindable and therefore are not AP inventory gates.
    ('Pin Purchase: Bench', area(1, 'The Marrow - Toll', crest=False)),
    ('Pin Purchase: Ventrica', area(
        2,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
        any_of=(
            'Ventrica: Choral Chambers',
            'Ventrica: Underworks',
            'Ventrica: Grand Bellway',
            'Ventrica: High Halls',
            'Ventrica: Songclave',
            'Ventrica: Memorium',
        ),
        crest=False,
    )),
    ('Pin Purchase: Bellway', req('Event: Bell Beast Defeated', crest=False)),
    ('Pin Purchase: Vendor', req(
        any_of=(
            'Path: Deep Docks - Toll',
            'Path: Wormways - Entrance',
            'Path: Greymoor - Halfway House',
        ),
        crest=False,
    )),

    # RELICS
    # Asset suffixes identify the source scene. The four relics whose
    # quest/key state is still missing remain in the fallback block below.
    ('Relic Pickup: Psalm Cylinder Library Roof', area(
        2,
        'Outlying Citadel - Library',
        'Ancestral Art: Clawline',
    )),
    ('Relic Pickup: Bone Record Wisp Top', area(
        1,
        'Greymoor - Wisp Thicket',
        'Ancestral Art: Clawline',
    )),
    ('Relic Pickup: Weaver Totem Bonetown_upper_room', area(
        1,
        'Mosslands - Bone Bottom',
        'Ancestral Art: Swift Step',
    )),
    ('Relic Pickup: Librarian Melody Cylinder', area(
        2,
        'Underworks - Twelfth Architect',
        'Event: Trobbio Defeated',
        'Ancestral Art: Clawline',
    )),
    ('Relic Pickup: Psalm Cylinder Ward', area(
        2,
        'Underworks - Whiteward',
        SURGEONS_KEY_ITEM,
    )),
    ('Relic Pickup: Weaver Record Conductor', area(
        3,
        'Outlying Citadel - High Halls Ventrica',
        'Ancestral Art: Clawline',
    )),
    ('Relic Pickup: Psalm Cylinder Librarian', area(2, 'Outlying Citadel - Library')),
    ('Relic Pickup: Psalm Cylinder Hang', area(
        2,
        'Outlying Citadel - High Halls Ventrica',
        'Ancestral Art: Clawline',
    )),
    ('Relic Pickup: Seal Chit Ward Corpse', area(
        2,
        'Underworks - Whiteward',
        'Path: Choral Chambers - Songclave',
    )),
    ('Relic Pickup: Weaver Record Sprint_Challenge', area(
        1,
        'Weavenest - Cindril',
        USABLE_CINDRIL_LOADOUT_REQUIREMENT,
        crest=False,
    )),
    *(
        ('Relic Pickup: Psalm Cylinder Grindle', requirement)
        for requirement in grindle_access(1)
    ),
    ('Relic Pickup: Weaver Record Weave_08', area(
        1,
        'Weavenest - Atla',
        'Ancestral Art: Cling Grip',
    )),
    ('Relic Pickup: Bone Record Understore_Map_Room', area(
        2,
        'Underworks - Broken Elevator',
    )),
    ('Relic Pickup: Bone Record Bone_East_14', area(
        1,
        'Far Fields - Seamstress',
        "Ability: Drifter's Cloak",
    )),
    # The Moss Grotto commandment sits directly on the opening descent through
    # Aspid_01.  It is available from the vanilla Moss Grotto start without a
    # crest or movement item. Bone Bottom is the destination below it, not its
    # access prerequisite.
    ('Relic Pickup: Seal Chit Aspid_01', area(
        1,
        'Mosslands - Moss Grotto',
        crest=False,
    )),
    ('Relic Pickup: Seal Chit Silk Siphon', area(
        2,
        'Underworks - Whiteward',
        'Path: Choral Chambers - Songclave',
        any_of=('Ancestral Art: Silk Soar', 'Ability: Faydown Cloak'),
    )),
    ('Relic Pickup: Seal Chit City Merchant', area(
        2,
        'Choral Chambers - Songclave',
        'Path: Outlying Citadel - Memorium',
        'Event: Wandering Merchant Rescued',
        'Ability: Faydown Cloak',
    )),
    ('Relic Pickup: Bone Record Greymoor_flooded_corridor', area(
        1,
        'Greymoor - Halfway House',
    )),
    ('Relic Pickup: Weaver Totem Slab_Bottom', area(
        2,
        'The Slab - Bellway',
        'Path: The Slab - Capture Event',
        'Ancestral Art: Cling Grip',
    )),
    ('Relic Pickup: Ancient Egg Abyss Middle', area(3, 'Abyss - Void Tendrils')),

    # BELLSHRINES
    ('Bell Shrine Completion: bellShrineBoneForest', area(
        1,
        'The Marrow - Bellshrine',
        silk_spear=True,
    )),
    ('Bell Shrine Completion: bellShrineWilds', area(
        1,
        'Deep Docks - Bellshrine',
        'Ancestral Art: Swift Step',
    )),
    ('Bell Shrine Completion: bellShrineGreymoor', area(
        1,
        'Greymoor - Bellshrine',
        'Event: Craw Lake Cleared',
    )),
    ('Bell Shrine Completion: bellShrineShellwood', area(
        1,
        'Shellwood - Bellshrine',
        'Ancestral Art: Cling Grip',
    )),
    # Native Bellshrine Sequence Bellhart is a post-Widow state transition.
    # Unlike a manual song door, it never checks hasNeedolin/canUseNeedolin.
    ('Bell Shrine Completion: bellShrineBellhart', req(
        'Event: Widow Defeated',
    )),

    # BOSSES
    # Combat execution is not a separate difficulty gate.
    ('Boss Completion: defeatedMossMother', area(1, 'Mosslands - Ruined Chapel')),
    ('Boss Completion: defeatedBellBeast', req('Event: Bell Beast Defeated')),
    ('Boss Completion: defeatedSongGolem', area(
        1,
        'Far Fields - Bellway',
        'Event: Flexile Spines Completed',
    )),
    # StartAct3 force-sets this flag when the optional Act 1 encounter was
    # skipped. Model the vanilla alias explicitly.
    ('Boss Completion: defeatedSongGolem', req(
        'Event: Act 3 Started',
        crest=False,
    )),
    ('Boss Completion: defeatedDockForemen', area(
        1,
        'Deep Docks - Forge',
        'Ancestral Art: Clawline',
    )),
    ('Boss Completion: defeatedVampireGnatBoss', area(
        1,
        'Greymoor - Bellshrine',
    )),
    ('Boss Completion: defeatedAntQueen', area(
        3,
        'Far Fields - Karmelita',
        'Event: Elegy of the Deep Learned',
    )),
    ('Boss Completion: defeatedCrowCourt', req(
        'Path: Greymoor - Halfway House',
        CRAW_SUMMONS_ITEM,
        any_of=(
            "Ability: Drifter's Cloak",
            'Ancestral Art: Silk Soar',
        ),
    )),
    ('Boss Completion: defeatedSplinterQueen', area(
        1,
        'Shellwood - Central Toll',
    )),
    ('Boss Completion: defeatedSeth', area(
        3,
        'Grand Gate',
        'Ancestral Art: Silk Soar',
    )),
    ('Boss Completion: defeatedFlowerQueen', area(
        3,
        'Grand Gate',
        'Event: Shrine Guardian Seth Defeated',
        'Event: Elegy of the Deep Learned',
    )),
    ('Boss Completion: defeatedRoachkeeperChef', area(
        1,
        "Sinner's Road - Styx",
        'Ability: Faydown Cloak',
    )),
    ('Boss Completion: defeatedPhantom', area(
        1,
        'Bilewater - Exhaust Organ',
        'Ancestral Art: Needolin',
    )),
    ('Boss Completion: DefeatedSwampShaman', area(
        1,
        'Bilewater - Bilehaven',
        'Ability: Faydown Cloak',
    )),
    ('Boss Completion: defeatedCoralKing', area(
        3,
        'Sands of Karak - Coral Tower',
        'Event: Elegy of the Deep Learned',
        'Ancestral Art: Silk Soar',
    )),
    ('Boss: Grand Mother Silk', req(ACT_TWO_GOAL_EVENT, act='Act 2')),
    ('Boss: Bell Eater', req(
        'Event: Act 3 Started', 'Event: Bell Beast Defeated', act='Act 3',
    )),
    ('Boss: Plasmified Zango', req(
        'Event: Act 3 Started',
        room_node_name('wormways/wormways-zango-arena#room'),
        act='Act 3',
    )),
    ('Boss: Lost Garmond', area(
        3, 'Blasted Steps - Bellway',
        'Event: Widow Defeated', 'Event: Everbloom Obtained',
    )),
    ('Boss: Pinstress', PINSTRESS_BATTLE_REQUIREMENT),
    ('Wish: Fatal Resolve', PINSTRESS_BATTLE_REQUIREMENT),
    ('Wish: Pain, Anguish and Misery', area(
        3, 'Outlying Citadel - Library',
        'Path: Choral Chambers - Songclave',
        'Progressive Claw Mirror', 'Ancestral Art: Silk Soar',
    )),
    *(("Wish: Final Audience", rule) for rule in LAST_AUDIENCE_REQUIREMENTS),
    ('Boss: Great Conchflies', area(1, 'Blasted Steps - Toll')),
    ('Boss Completion: defeatedLastJudge', req('Event: Last Judge Defeated')),
    ('Boss Completion: defeatedGreyWarrior', area(
        3,
        'Sands of Karak - Sands of Karak',
        'Ancestral Art: Silk Soar',
        'Ancestral Art: Needolin',
    )),
    ('Boss Completion: defeatedFirstWeaver', req(
        'Act: 2',
        room_node_name(
            "the-slab/slab-first-sinner-antechamber#room"
        ),
        'Ability: Faydown Cloak',
        act='Act 2',
    )),
    ('Boss Completion: defeatedTrobbio', area(
        2,
        'Outlying Citadel - Library',
    )),
    # StartAct3 also force-sets defeatedTrobbio. Keeping that vanilla flag as
    # an alternate logical source matches what the client will report.
    ('Boss Completion: defeatedTrobbio', req(
        'Event: Act 3 Started',
        crest=False,
    )),
    ('Boss Completion: defeatedTormentedTrobbio', area(
        3,
        'Outlying Citadel - Library',
        'Progressive Claw Mirror',
        'Ancestral Art: Silk Soar',
    )),
    ('Boss Completion: defeatedCogworkDancers', area(
        2,
        'Choral Chambers - High Halls Entrance',
    )),
    ('Boss Completion: defeatedLaceTower', area(
        2,
        'The Cradle - Terminus',
        'Event: Cradle Opened',
    )),
    # These four encounters share the route of their native reward source.
    # Gurr and Raging Conchfly remain below until their local requirements are
    # represented.
    ('Boss Completion: defeatedWispPyreEffigy', area(
        1,
        'Greymoor - Wisp Thicket',
    )),
    ('Boss Completion: wardBossDefeated', area(
        2,
        'Underworks - Whiteward',
        'Ancestral Art: Clawline',
        SURGEONS_KEY_ITEM,
    )),
    ('Boss Completion: defeatedZapCoreEnemy', area(
        1,
        'Sands of Karak - Sands of Karak',
    )),
    ('Boss Completion: spinnerDefeated', area(
        1,
        'Bellhart - Widow',
    )),

    # CRAFTING KITS
    ('Crafting Kit Source: Forge Tool Kit', area(1, 'Deep Docks - Forge')),
    ('Crafting Kit Source: Architect Tool Kit', area(
        2,
        'Underworks - Twelfth Architect',
        'Ancestral Art: Clawline',
    )),
    *(
        ('Crafting Kit Source: Grindle Tool Kit', requirement)
        for requirement in grindle_access(1)
    ),
    ('Crafting Kit Source: Crow Feathers', area(
        1,
        'Greymoor - Halfway House',
        'Event: Widow Defeated',
    )),

    # WISHES
    # The story needs these even when there's no item to send.
    ('Quest Completion: A Pinsmiths Tools', area(
        2,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
        'Path: Outlying Citadel - Library',
        'Ancestral Art: Cling Grip',
    )),
    ('Quest Completion: A Pinsmiths Tools', area(
        2,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
        'Path: Choral Chambers - First Shrine',
        'Path: Mosslands - Moss Druid',
        'Path: Greymoor - Halfway House',
        'Event: Missing Brother Rescued',
        'Path: Sands of Karak - Sands of Karak',
        "Path: Sinner's Road - Styx",
        'Ability: Faydown Cloak',
    )),
    ('Quest Completion: A Pinsmiths Tools', area(
        3,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
        'Path: Putrified Ducts - Fleatopia',
        'Tool: Egg of Flealia',
        item_counts=(item_count(MAX_FLEA_HUNT_GOAL_COUNT, *FLEA_ITEMS),),
    )),
    # Belltown House Start is Restoration of Bellhart. The
    # greeter's first conversation plus leaving Bellhart are repeatable local
    # actions. Its remaining native gates are modeled conditionally in
    # rules.py when Needle Upgrades or Relics are themselves randomized.
    ('Quest Completion: Belltown House Start', area(
        1,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
    )),
    ('Quest Completion: Belltown House Mid', area(
        2,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
        'Event: Cogwork Dancers Defeated',
        required_locations=('Quest Completion: Belltown House Start',),
    )),
    ('Quest Completion: Belltown House Mid', area(
        2,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
        'Ancestral Art: Clawline',
        required_locations=('Quest Completion: Belltown House Start',),
    )),
    ('Quest Completion: Belltown House Mid', area(
        2,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
        'Path: Choral Chambers - Songclave',
        required_locations=('Quest Completion: Belltown House Start',),
    )),
    ('Quest Completion: Building Materials', req(
        'Event: Bone Bottom Repairs Completed',
    )),
    ('Quest Completion: Building Materials (Bridge)', req(
        'Event: Lifesaving Bridge Completed',
    )),
    ('Quest Completion: Building Materials (Statue)', area(
        2,
        'Mosslands - Bone Bottom',
        'Event: Lifesaving Bridge Completed',
    )),
    ('Quest Completion: Courier Delivery Bonebottom', area(
        1,
        'Mosslands - Bone Bottom',
        'Path: Bellhart - Bellhart',
        'Event: Bell Beast Defeated',
        'Event: Missing Brother Rescued',
    )),
    ('Quest Completion: Courier Delivery Dustpens Slave', req(
        'Event: Queen\'s Egg Delivered',
    )),
    ('Quest Completion: Courier Delivery Fixer', area(
        3,
        'Mosslands - Bone Bottom',
        'Path: Bellhart - Bellhart',
    )),
    ('Quest Completion: Courier Delivery Fleatopia', area(
        2,
        'Putrified Ducts - Fleatopia',
        'Path: Bellhart - Bellhart',
        'Event: Missing Brother Rescued',
        item_counts=(item_count(22, *FLEA_ITEMS),),
    )),
    ('Quest Completion: Courier Delivery Mask Maker', area(
        2,
        'Mount Fay - Workbench',
        'Path: Bellhart - Bellhart',
        'Event: Queen\'s Egg Delivered',
        'Event: Threefold Melody Learned',
        'Ability: Faydown Cloak',
    )),
    ('Quest Completion: Courier Delivery Pilgrims Rest', area(
        1,
        "Far Fields - Pilgrim's Rest",
        'Path: Bellhart - Bellhart',
        'Event: Missing Brother Rescued',
    )),
    ('Quest Completion: Courier Delivery Songclave', area(
        2,
        'Choral Chambers - Songclave',
        'Path: Bellhart - Bellhart',
        'Event: Missing Brother Rescued',
    )),
    # Act 3 exposes the same Songclave delivery independently of its ordinary
    # pre-Soul-Snare availability window.
    ('Quest Completion: Courier Delivery Songclave', area(
        3,
        'Choral Chambers - Songclave',
        'Path: Bellhart - Bellhart',
    )),
    ('Quest Completion: Extractor Blue Worms', area(
        3,
        'Wormways - Plasmium Lab',
        USABLE_NEEDLE_PHIAL_REQUIREMENT,
        crest=False,
    )),
    ('Quest Completion: Fine Pins', req(
        'Event: Fine Pins Completed',
    )),
    ('Quest Completion: Garmond Black Threaded', area(
        3,
        'Blasted Steps - Bellway',
        'Event: Widow Defeated',
        'Event: Everbloom Obtained',
    )),
    ('Quest Completion: Great Gourmand', area(
        2,
        'Choral Chambers - First Shrine',
        'Event: Last Judge Defeated',
        'Path: Mosslands - Moss Druid',
        'Path: Greymoor - Halfway House',
        'Event: Missing Brother Rescued',
        'Path: Sands of Karak - Sands of Karak',
        "Path: Sinner's Road - Styx",
        'Ability: Faydown Cloak',
    )),
    ('Quest Completion: Journal', area(
        1,
        'Greymoor - Halfway House',
    )),
    ('Quest Completion: Mr Mushroom', area(
        3,
        'The Cradle - Surface Ascent',
        'Path: Mosslands - Ruined Chapel',
        'Path: Mosslands - Bone Bottom',
        'Path: Far Fields - Seamstress',
        'Path: Greymoor - Wisp Thicket',
        'Path: Putrified Ducts - Bellway',
        room_node_name("the-slab/slab-arena#arena"),
        'Path: Mount Fay - Workbench',
        'Ancestral Art: Silk Soar',
        'Ancestral Art: Needolin',
    )),
    ('Quest Completion: Pilgrim Rags', area(
        1,
        'Mosslands - Bone Bottom',
        'Path: The Marrow - Mosshome Gate',
        'Event: Bell Beast Defeated',
    )),
    (
        'Quest Completion: Rock Rollers',
        _volatile_flintbeetle_act_one_requirement(
            crest=True,
            path_name='The Marrow - Toll',
        ),
    ),
    # Act 3 removes an unfinished Rock Rollers quest and leaves the same
    # Memory Locket reward as a ground fallback in Bone_10.
    ('Quest Completion: Rock Rollers', area(
        3,
        'Mosslands - Bone Bottom',
    )),
    ('Quest Completion: Save City Merchant', req(
        'Event: Wandering Merchant Rescued',
    )),
    ('Quest Completion: Save City Merchant Bridge', area(
        2,
        'Outlying Citadel - Memorium',
        'Event: Wandering Merchant Rescued',
        'Event: Strengthening Songclave Completed',
        'Ability: Faydown Cloak',
    )),
    ('Quest Completion: Save Courier Short', req(
        'Event: Missing Courier Rescued',
    )),
    ('Quest Completion: Save Courier Tall', req(
        'Event: Missing Brother Rescued',
    )),
    ('Quest Completion: Save Sherma', req(
        'Event: Balm for the Wounded Completed',
    )),
    ('Quest Completion: Shiny Bell Goomba', area(
        1,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
    )),
    ('Quest Completion: Skull King', area(
        1,
        'Mosslands - Bone Bottom',
        'Ancestral Art: Cling Grip',
    )),
    ('Quest Completion: Song Pilgrim Cloaks', req(
        'Event: Cloaks of the Choir Completed',
    )),
    ('Quest Completion: Songclave Donation 1', req(
        'Event: Building Up Songclave Completed',
    )),
    ('Quest Completion: Songclave Donation 2', req(
        'Event: Strengthening Songclave Completed',
    )),
    ('Quest Completion: Steel Sentinel Pt2', req(
        'Room Event: event:mapper/da476bc2-0b8d-4b9c-b040-2e0f75c197b8', crest=False,
    )),

    # Shakra carries missed stock forward. Valid routes prove access to a
    # physical shop or to story events that place her at a persistent camp.
    # Receiving a randomized movement or Silk Skill item is not itself shop
    # access and does not reproduce the vanilla mapper-evaluation sequence.
    ('Map Purchase: Mosslands', area(1, 'The Marrow - Toll')),
    ('Map Purchase: The Marrow', area(1, 'The Marrow - Toll')),
    ('Map Purchase: The Marrow', req('Event: Bell Beast Defeated')),
    ('Map Purchase: Deep Docks', area(1, 'Deep Docks - Toll')),
    ('Map Purchase: Deep Docks', area(1, 'Deep Docks - Bellshrine')),
    ('Map Purchase: Deep Docks', req('Event: Widow Defeated')),
    ('Map Purchase: Far Fields', area(1, 'Far Fields - Bellway')),
    ('Map Purchase: Far Fields', req('Event: Widow Defeated')),
    ('Map Purchase: Far Fields', req('Event: Act 2 Started')),
    ('Map Purchase: Wormways', area(1, 'Wormways - Bottom')),
    ('Map Purchase: Wormways', req('Event: Act 2 Started')),
    ("Map Purchase: Hunter's March", area(1, "Hunter's March - Trap")),
    ("Map Purchase: Hunter's March", req('Event: Act 2 Started')),
    ('Map Purchase: Greymoor', area(1, 'Greymoor - Halfway House')),
    ('Map Purchase: Greymoor', area(
        1,
        'Greymoor - Bellshrine',
        'Event: Craw Lake Cleared',
    )),
    ('Map Purchase: Bellhart', area(
        1,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
    )),
    ('Map Purchase: Shellwood', area(1, 'Shellwood - Overgrown West')),
    ('Map Purchase: Shellwood', req('Event: Widow Defeated')),
    ('Map Purchase: Blasted Steps', area(1, 'Blasted Steps - Bellway')),
    ('Map Purchase: Blasted Steps', req('Event: Last Judge Defeated')),
    ("Map Purchase: Sinner's Road", area(1, "Sinner's Road - Broken Toll")),
    ('Map Purchase: Mount Fay', area(2, 'Mount Fay - Shakra')),
    ('Map Purchase: Sands of Karak', area(1, 'Sands of Karak - Sands of Karak')),
    ('Map Purchase: Bilewater', area(
        1,
        'Bilewater - Bellway',
        'Ability: Faydown Cloak',
    )),
    ('Map Purchase: Bilewater', area(
        1,
        'Bilewater - Bilehaven',
        'Ability: Faydown Cloak',
    )),

    # Static map pickups and machines. Sources with unresolved local movement,
    # alternate-machine or quest-state details cannot hold progression.
    ('Map Pickup: Weavenest Atla', area(1, 'Weavenest - Atla')),
    ('Map Purchase: Grand Gate', area(2, 'Grand Gate')),
    ('Map Pickup: Underworks', area(2, 'Underworks - Broken Elevator')),
    ('Map Purchase: Choral Chambers', area(
        2,
        'Choral Chambers - Grand Bellway',
    )),
    ('Map Purchase: Whispering Vaults', area(
        2,
        'Outlying Citadel - Library',
    )),
    ('Map Purchase: Whiteward', area(2, 'Underworks - Whiteward')),
    ('Map Pickup: Cogwork Core', area(
        2,
        'Outlying Citadel - Cogwork Core',
    )),
    ('Map Purchase: Memorium', area(
        2,
        'Outlying Citadel - Memorium',
    )),
    ('Map Purchase: High Halls', area(
        2,
        'Outlying Citadel - High Halls Ventrica',
    )),
    ('Map Pickup: The Slab', req(
        'Act: 2',
        room_node_name("the-slab/slab-grindle#room"),
        act='Act 2',
    )),
    ('Map Pickup: Putrified Ducts', area(
        2,
        'Putrified Ducts - Bellway',
    )),
    ('Map Purchase: The Cradle', area(2, 'The Cradle - Terminus')),
    ('Map Pickup: Verdania', area(
        3,
        'Greymoor - Bellshrine',
        SIMPLE_KEY_GREEN_PRINCE,
        'Event: Cogwork Dancers Defeated',
        'Event: Craw Lake Cleared',
        'Event: Elegy of the Deep Learned',
        crest=False,
    )),
    ('Map Pickup: The Abyss', area(
        3,
        'Abyss - Void Tendrils',
        'Ancestral Art: Cling Grip',
    )),

    # Learned-song sources.
    ("Architect's Melody", area(
        2,
        'Outlying Citadel - Cogwork Core',
        'Ancestral Art: Clawline',
    )),
    ("Conductor's Melody", area(
        2,
        'Outlying Citadel - High Halls Ventrica',
        'Ancestral Art: Clawline',
    )),
    ("Vaultkeeper's Melody", area(
        2,
        'Outlying Citadel - Library',
        'Relic: Sacred Cylinder',
    )),
    ('Elegy of the Deep', area(
        3,
        'Mosslands - Ruined Chapel',
        'Path: Abyss - Escape',
        'Ancestral Art: Needolin',
        crest=False,
    )),
    ('Beastling Call', req(
        'Event: Act 3 Started',
        'Event: Bell Beast Defeated',
        crest=False,
    )),

    # Bellways
    ('Bellway Unlock: Deep Docks', area(1, 'Deep Docks - Toll')),
    ('Bellway Unlock: Far Fields', area(1, 'Far Fields - Bellway')),
    ('Bellway Unlock: Greymoor', area(1, 'Greymoor - Halfway House')),
    ('Bellway Unlock: Bellhart', area(1, 'Bellhart - Bellhart')),
    ('Bellway Unlock: Blasted Steps', area(1, 'Blasted Steps - Bellway')),
    ('Bellway Unlock: Grand Bellway', area(2, 'Choral Chambers - Grand Bellway')),
    ('Bellway Unlock: The Slab', area(2, 'The Slab - Bellway')),
    ('Bellway Unlock: Shellwood', area(1, 'Shellwood - Bellshrine')),
    ('Bellway Unlock: Bilewater', area(1, 'Bilewater - Bellway')),
    ('Bellway Unlock: Putrified Ducts', area(2, 'Putrified Ducts - Bellway')),

    # Ventrica
    ('Ventrica Unlock: Choral Chambers', area(2, 'Choral Chambers - Spa')),
    ('Ventrica Unlock: Underworks', area(2, 'Underworks - Confession Toll')),
    ('Ventrica Unlock: Grand Bellway', area(2, 'Choral Chambers - Grand Bellway')),
    ('Ventrica Unlock: High Halls', area(2, 'Outlying Citadel - High Halls Ventrica')),
    ('Ventrica Unlock: Songclave', area(2, 'Choral Chambers - First Shrine')),
    ('Ventrica Unlock: Memorium', area(2, 'Outlying Citadel - Memorium')),

    # CREST SLOT UNLOCKS
    # Slot expansion is available from the crest UI once its matching crest
    # is owned. Randomized Lockets add the shared fill-aware count separately.
    ('Hunter Slot Unlock: Red 0 -2', req('Crest: Hunter', crest=False)),
    ('Hunter Slot Unlock: Blue -2 0', req('Crest: Hunter', crest=False)),
    ('Hunter Slot Unlock: Yellow 2 0', req('Crest: Hunter', crest=False)),
    ('Beast Slot Unlock: Yellow -1 0', req('Crest: Beast', crest=False)),
    ('Beast Slot Unlock: Yellow 1 0', req('Crest: Beast', crest=False)),
    ('Witch Slot Unlock: Red 0 -2', req('Crest: Witch', crest=False)),
    ('Witch Slot Unlock: Blue -1 0', req('Crest: Witch', crest=False)),
    ('Witch Slot Unlock: Blue 1 0', req('Crest: Witch', crest=False)),
    ('Reaper Slot Unlock: Red 0 -1', req('Crest: Reaper', crest=False)),
    ('Reaper Slot Unlock: Blue -1 1', req('Crest: Reaper', crest=False)),
    ('Reaper Slot Unlock: Yellow 1 1', req('Crest: Reaper', crest=False)),
    ('Architect Slot Unlock: Blue -1 2', req('Crest: Architect', crest=False)),
    ('Architect Slot Unlock: Yellow 1 2', req('Crest: Architect', crest=False)),
    ('Architect Slot Unlock: Yellow 2 0', req('Crest: Architect', crest=False)),
    ('Architect Slot Unlock: Blue -2 0', req('Crest: Architect', crest=False)),
    ('Shaman Slot Unlock: Blue -1 0', req('Crest: Shaman', crest=False)),
    ('Shaman Slot Unlock: Blue 1 0', req('Crest: Shaman', crest=False)),
    ('Wanderer Slot Unlock: Blue -2 1', req('Crest: Wanderer', crest=False)),
    ('Wanderer Slot Unlock: Blue 2 1', req('Crest: Wanderer', crest=False)),
    ('Wanderer Slot Unlock: Yellow 0 -2', req('Crest: Wanderer', crest=False)),

    # MASK SHARDS
    # Every row below is a stable vanilla source, not the Nth shard collected.
    # Pebb relocates his unbought shard to Grindle in Act 3, so both physical
    # shop routes resolve to the same AP location.
    ('Mask Shard: Pebb (Bone Bottom) / Grindle (Act 3)', area(
        1,
        'Mosslands - Bone Bottom',
    )),
    *(
        (
            'Mask Shard: Pebb (Bone Bottom) / Grindle (Act 3)',
            requirement,
        )
        for requirement in grindle_access(3)
    ),
    ('Mask Shard: Wormways', area(1, 'Wormways - Bottom')),
    ('Mask Shard: Far Fields (Above the Seamstress)', area(
        1,
        'Far Fields - Seamstress',
        "Ability: Drifter's Cloak",
    )),
    ('Mask Shard: Shellwood', area(
        1,
        'Shellwood - Overgrown West',
    )),
    ('Mask Shard: The Marrow - Deep Docks Passage', area(
        1,
        'The Marrow - Shooting Gallery',
        any_of=(
            'Ancestral Art: Cling Grip',
            'Ancestral Art: Swift Step',
        ),
    )),
    ('Mask Shard: Weavenest Atla', area(
        1,
        'Weavenest - Atla',
        'Ancestral Art: Cling Grip',
    )),
    ('Mask Shard: Savage Beastfly', area(
        2,
        'Choral Chambers - Songclave',
        'Path: Far Fields - Bellway',
        "Path: Hunter's March - Trap",
        'Event: Fourth Chorus Defeated',
        "Ability: Drifter's Cloak",
    )),
    ('Mask Shard: Savage Beastfly', area(
        3,
        'Choral Chambers - Songclave',
        'Path: Far Fields - Bellway',
        "Path: Hunter's March - Trap",
        "Ability: Drifter's Cloak",
    )),
    ('Mask Shard: Cogwork Core', area(
        2,
        'Outlying Citadel - Lower Cogwork Core',
        'Event: Cogwork Dancers Defeated',
    )),
    ('Mask Shard: Whispering Vaults', area(
        2,
        'Outlying Citadel - Library',
    )),
    ('Mask Shard: Bilewater', area(
        2,
        'Bilewater - Bilehaven',
        'Ability: Faydown Cloak',
    )),
    ('Mask Shard: Far Fields (Skull Cave)', area(
        2,
        'Far Fields - Bellway',
        'Ancestral Art: Clawline',
        "Ability: Drifter's Cloak",
    )),
    ('Mask Shard: The Slab (Key of the Apostate)', area(
        2,
        'The Slab - Capture Event',
        KEY_OF_APOSTATE_ITEM,
        any_of=('Ability: Faydown Cloak', 'Ancestral Art: Silk Soar'),
    )),
    ('Mask Shard: Mount Fay', area(
        2,
        'Mount Fay - Shakra',
        'Ability: Faydown Cloak',
    )),
    ('Mask Shard: Wisp Thicket', area(
        2,
        'Greymoor - Wisp Thicket',
        'Ability: Faydown Cloak',
    )),
    ('Mask Shard: Jubilana (Songclave)', area(
        2,
        'Choral Chambers - Songclave',
        'Event: Wandering Merchant Rescued',
    )),
    ('Mask Shard: Blasted Steps', area(
        2,
        'Blasted Steps - Bellway',
        'Ancestral Art: Clawline',
        'Ability: Faydown Cloak',
    )),
    ('Mask Shard: Blasted Steps', area(
        3,
        'Blasted Steps - Bellway',
        'Ancestral Art: Silk Soar',
    )),
    ('Mask Shard: Fastest in Pharloom', area(
        3,
        'Far Fields - Sprintmaster',
        "Path: Hunter's March - Trap",
        'Ancestral Art: Silk Soar',
    )),
    ('Mask Shard: The Hidden Hunter', area(
        3,
        'Far Fields - Karmelita',
        'Ancestral Art: Silk Soar',
    )),
    ('Mask Shard: Dark Hearts', area(
        3,
        'Bellhart - Bellhart',
    )),
    ('Mask Shard: Brightvein', area(
        3,
        'Mount Fay - Shakra',
        'Ancestral Art: Silk Soar',
    )),

    # SPOOL FRAGMENTS
    ('Spool Fragment: Bone Bottom', area(
        1,
        'The Marrow - Toll',
    )),
    ('Spool Fragment: Deep Docks (Central)', area(
        1,
        'Deep Docks - Toll',
    )),
    ('Spool Fragment: Greymoor', area(
        1,
        'Greymoor - Halfway House',
        'Event: Craw Lake Cleared',
        'Ancestral Art: Cling Grip',
    )),
    ('Spool Fragment: The Slab', area(
        1,
        'The Slab - Window',
        'Ancestral Art: Cling Grip',
    )),
    ('Spool Fragment: Weavenest Atla', area(
        1,
        'Weavenest - Atla',
        'Ancestral Art: Needolin',
        'Ancestral Art: Cling Grip',
    )),
    ('Spool Fragment: Frey (Bellhart)', area(
        1,
        'Bellhart - Bellhart',
        'Event: Missing Courier Rescued',
    )),
    ('Spool Fragment: Flea Caravan', area(
        2,
        'Blasted Steps - Bellway',
        'Event: Last Judge Defeated',
        item_counts=(item_count(12, *FLEA_ITEMS),),
    )),
    ('Spool Fragment: Cogwork Core', area(
        2,
        'Outlying Citadel - Lower Cogwork Core',
    )),
    ('Spool Fragment: Underworks (East)', area(
        2,
        'Underworks - Whiteward',
    )),
    ('Spool Fragment: Grand Gate', area(
        2,
        'Grand Gate',
    )),
    ('Spool Fragment: Underworks (Gauntlet)', area(
        2,
        'Underworks - Confession Toll',
    )),
    ('Spool Fragment: Whiteward', area(
        2,
        'Underworks - Whiteward',
    )),
    ('Spool Fragment: Balm for the Wounded', area(
        2,
        'Underworks - Whiteward',
        'Path: Choral Chambers - Songclave',
    )),
    ('Spool Fragment: Deep Docks (Southeast)', area(
        2,
        'Deep Docks - Lower',
        'Ancestral Art: Clawline',
        'Ancestral Art: Cling Grip',
    )),
    ('Spool Fragment: High Halls', area(
        2,
        'Outlying Citadel - High Halls Ventrica',
        'Ability: Faydown Cloak',
        'Ancestral Art: Clawline',
    )),
    ('Spool Fragment: High Halls', area(
        3,
        'Outlying Citadel - High Halls Ventrica',
        'Ancestral Art: Silk Soar',
    )),
    ('Spool Fragment: Memorium', area(
        2,
        'Outlying Citadel - Memorium',
        'Ability: Faydown Cloak',
        'Ancestral Art: Clawline',
        any_of=(
            'Ancestral Art: Cling Grip',
            USABLE_SCUTTLEBRACE_REQUIREMENT,
        ),
    )),
    *(
        ('Spool Fragment: Grindle (Blasted Steps)', requirement)
        for requirement in grindle_access(1)
    ),
    ('Spool Fragment: Jubilana (Songclave)', area(
        2,
        'Choral Chambers - Songclave',
        'Path: Outlying Citadel - Memorium',
        'Event: Wandering Merchant Rescued',
        'Ability: Faydown Cloak',
    )),

    (
        'Silk Heart: Bell Beast',
        area(
            1,
            'The Marrow - Mosshome Gate',
            'Event: Bell Beast Defeated',
            silk_spear=True,
        ),
    ),
    (
        'Silk Heart: The Unravelled',
        area(
            2,
            'Underworks - Whiteward',
            'Ancestral Art: Clawline',
            SURGEONS_KEY_ITEM,
        ),
    ),
    (
        'Silk Heart: Lace (Cradle)',
        area(
            2,
            'The Cradle - Terminus',
            'Event: Cradle Opened',
        ),
    ),

    # Repeated collectibles use area access for their one-time physical
    # sources.
    ("Memory Locket: Pilgrim's Rest Shop", area(
        1,
        "Far Fields - Pilgrim's Rest",
    )),
    *(
        ("Memory Locket: Pilgrim's Rest Shop", requirement)
        for requirement in grindle_access(3)
    ),
    # Tool Pouches are four stable physical sources. Pilgrim's Rest moves its
    # unbought stock to Grindle in Act 3, so both shop routes report one check.
    ("Tool Pouch: Pilgrim's Rest", area(
        1,
        "Far Fields - Pilgrim's Rest",
    )),
    *(
        ("Tool Pouch: Pilgrim's Rest", requirement)
        for requirement in grindle_access(3)
    ),
    ('Tool Pouch: Loddie', area(
        1,
        'The Marrow - Shooting Gallery',
    )),
    ('Tool Pouch: Bugs of Pharloom', area(
        1,
        'Greymoor - Halfway House',
    )),
    ('Tool Pouch: Fleatopia', area(
        2,
        'Putrified Ducts - Fleatopia',
    )),
    # Scripted Beast Shards use their native reward actors. Marrowmaw uses the
    # room graph. Other flat fallbacks stay non-progression until their routes
    # are added.
    ('Beast Shard: Marrowmaw', area(
        1,
        'Mosslands - Moss Grotto',
    )),
    ('Beast Shard: Craggler', area(
        1,
        'Wormways - Bottom',
    )),
    ("Beast Shard: Pilgrim's Rest", area(
        1,
        "Far Fields - Pilgrim's Rest",
    )),
    ('Beast Shard: Memorium', area(
        2,
        'Outlying Citadel - Memorium',
    )),
    ('Beast Shard: Sprintmaster', area(
        3,
        'Far Fields - Sprintmaster',
    )),
    ("Memory Locket: Hunter's March", area(
        1,
        "Hunter's March - Trap",
        "Ability: Drifter's Cloak",
    )),
    ('Memory Locket: Greymoor', area(
        1,
        'Greymoor - Halfway House',
    )),
    ('Memory Locket: Halfway Home', area(
        2,
        'Greymoor - Halfway House',
        'Ability: Faydown Cloak',
    )),
    ('Memory Locket: Bellhart Shop', area(
        1,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
    )),
    ('Memory Locket: Bellhart Roof', area(
        1,
        'Bellhart - Bellhart',
        'Ancestral Art: Silk Soar',
    )),
    (
        'Memory Locket: Volatile Flintbeetles',
        _volatile_flintbeetle_act_one_requirement(
            crest=True,
            path_name='The Marrow - Toll',
        ),
    ),
    ('Memory Locket: Volatile Flintbeetles', area(
        3,
        'Mosslands - Bone Bottom',
    )),
    ('Memory Locket: The Marrow', area(
        1,
        'The Marrow - Toll',
        'Ancestral Art: Cling Grip',
    )),
    ('Memory Locket: Choral Chambers', area(
        2,
        'Choral Chambers - Grand Bellway',
    )),
    ('Memory Locket: Wormways', area(1, 'Wormways - Bottom')),
    ('Memory Locket: Blasted Steps', area(
        1,
        'Blasted Steps - Bellway',
        'Ancestral Art: Cling Grip',
    )),
    ('Memory Locket: Underworks', area(
        2,
        'Underworks - Confession Toll',
    )),
    ('Memory Locket: Whispering Vaults', area(
        2,
        'Outlying Citadel - Library',
        'Ancestral Art: Cling Grip',
    )),
    ('Memory Locket: Bilewater West', area(
        1,
        'Bilewater - Bellway',
        'Ancestral Art: Cling Grip',
        'Ancestral Art: Swift Step',
    )),
    ('Memory Locket: Deep Docks', area(
        2,
        'Deep Docks - Lower',
        'Ancestral Art: Cling Grip',
    )),
    ('Memory Locket: Bilewater East', area(
        2,
        'Bilewater - Corpse Sack Chamber',
    )),
    ('Memory Locket: The Slab', area(
        2,
        'The Slab - Bellway',
        'Ancestral Art: Cling Grip',
    )),
    ('Memory Locket: Memorium', area(
        2,
        'Outlying Citadel - Memorium',
        'Ability: Faydown Cloak',
    )),
    ('Memory Locket: Far Fields (Act 3)', area(
        3,
        'Far Fields - Karmelita',
        'Ancestral Art: Silk Soar',
    )),
    ('Memory Locket: Sands of Karak', area(
        2,
        'Sands of Karak - Sands of Karak',
        'Ancestral Art: Clawline',
    )),

    ('Craftmetal: Bone Bottom Shop', area(1, 'Mosslands - Bone Bottom')),
    # The physical Bone_07 source is in Lower Pogo, beyond the Shooting
    # Gallery route rather than in the opening Toll section.
    ('Craftmetal: The Marrow', area(
        1,
        'The Marrow - Shooting Gallery',
    )),
    ('Craftmetal: Deep Docks', area(1, 'Deep Docks - Toll')),
    ('Craftmetal: Blasted Steps', area(
        1,
        'Blasted Steps - Bellway',
        'Ancestral Art: Cling Grip',
    )),
    ('Craftmetal: Underworks', area(2, 'Underworks - Whiteward')),
    ('Craftmetal: Putrified Ducts', area(
        2,
        'Putrified Ducts - Huntress',
        'Ability: Faydown Cloak',
    )),
    ('Craftmetal: Wisp Thicket', area(
        2,
        'Greymoor - Wisp Thicket',
        'Ancestral Art: Cling Grip',
        'Ability: Faydown Cloak',
    )),
    ('Craftmetal: Songclave Shop', area(
        2,
        'Choral Chambers - Songclave',
        'Event: Wandering Merchant Rescued',
    )),

    ('Mossberry: Moss Grotto #1', area(
        1,
        'Mosslands - Moss Grotto',
        crest=False,
    )),
    ('Mossberry: Moss Grotto #2', area(
        1,
        'Mosslands - Moss Grotto',
        crest=False,
    )),
    ('Mossberry: Bone Bottom', area(1, 'Mosslands - Bone Bottom')),
    ('Mossberry: Mosshome', area(1, 'Mosslands - Moss Druid')),
    ('Mossberry: Bonegrave', area(1, 'Mosslands - Bonegrave')),
    ('Mossberry: Weavenest Atla', area(1, 'Weavenest - Atla')),
    ('Mossberry: Memorium', area(
        2,
        'Outlying Citadel - Memorium',
    )),

    # The installed game has six finite Shell Flower sources. Timothy's
    # source graph places the first three after Drifter's Cloak and the last
    # three after Cling Grip. Explicit Swift Step keeps the route conservative
    # when Shellwood itself was entered through a Bellway.
    ('Pollip Heart: Shellwood #1', area(
        1,
        'Shellwood - Overgrown West',
        SWIFT_STEP_ITEM,
        "Ability: Drifter's Cloak",
    )),
    ('Pollip Heart: Shellwood #2', area(
        1,
        'Shellwood - Overgrown West',
        SWIFT_STEP_ITEM,
        "Ability: Drifter's Cloak",
    )),
    ('Pollip Heart: Shellwood #3', area(
        1,
        'Shellwood - Central Toll',
        SWIFT_STEP_ITEM,
        "Ability: Drifter's Cloak",
    )),
    ('Pollip Heart: Shellwood #4', area(
        1,
        'Shellwood - Greyroot',
        SWIFT_STEP_ITEM,
        "Ability: Drifter's Cloak",
        'Ancestral Art: Cling Grip',
    )),
    ('Pollip Heart: Shellwood #5', area(
        1,
        'Shellwood - Greyroot',
        SWIFT_STEP_ITEM,
        "Ability: Drifter's Cloak",
        'Ancestral Art: Cling Grip',
    )),
    ('Pollip Heart: Shellwood #6', area(
        1,
        'Shellwood - Overgrown West',
        SWIFT_STEP_ITEM,
        "Ability: Drifter's Cloak",
        'Ancestral Art: Cling Grip',
    )),

    ('Silkeater: Deep Docks', area(2, 'Deep Docks - Lower')),
    # The Greymoor cocoon hangs at the top of the tower immediately west of
    # Halfway Home.  Its intended Act 1 route is the tower's wall climb, so
    # Cling Grip is required. The later Faydown Cloak cannot substitute for
    # that climb.
    ('Silkeater: Greymoor', area(
        1,
        'Greymoor - Halfway House',
        'Ancestral Art: Cling Grip',
    )),
    ('Silkeater: Blasted Steps', area(
        1,
        'Blasted Steps - Bellway',
    )),
    ('Silkeater: Exhaust Organ', area(1, 'Bilewater - Exhaust Organ')),
    ('Silkeater: Choral Chambers West', area(
        2,
        'Choral Chambers - Grand Bellway',
        'Ancestral Art: Cling Grip',
    )),
    ('Silkeater: Choral Chambers East', area(
        2,
        'Choral Chambers - Below Dining',
        'Ancestral Art: Cling Grip',
    )),
    ('Silkeater: Whispering Vaults', area(
        2,
        'Outlying Citadel - Library',
        'Ancestral Art: Cling Grip',
    )),
    ('Silkeater: Whiteward', area(2, 'Underworks - Whiteward')),
    ('Silkeater: The Cradle', area(2, 'The Cradle - Terminus')),

    # Named, non-fungible keys and Craw Summons.
    ('Key of Apostate', area(2, 'Putrified Ducts - Huntress')),
    ('White Key', area(2, 'Choral Chambers - Songclave')),
    ("Surgeon's Key", area(
        2,
        'Underworks - Whiteward',
        'Ancestral Art: Clawline',
    )),
    ("Architect's Key", area(
        2,
        "Underworks - Architect's Shop",
    )),
    ('Craw Summons', req('Event: Craw Summons Obtained')),

    # Scrounge is available in restored Bellhart after Widow. Although one
    # conversation may deposit several held relics, every relic has its own
    # persistent deposited state and therefore its own AP check.
    *(
        (
            location_name,
            area(
                1,
                'Bellhart - Bellhart',
                'Event: Widow Defeated',
                relic_item_name,
            ),
        )
        for location_name, relic_item_name
        in SCROUNGE_RELIC_ITEM_BY_TURN_IN_LOCATION.items()
    ),

    # Cardinius's RelicBoardOwner persists each cylinder deposit separately.
    # His established Vaultkeeper's Melody source uses this same Library
    # access, so the turn-ins add only possession of the matching cylinder.
    *(
        (
            location_name,
            area(
                2,
                'Outlying Citadel - Library',
                cylinder_item_name,
            ),
        )
        for location_name, cylinder_item_name
        in CARDINIUS_CYLINDER_ITEM_BY_TURN_IN_LOCATION.items()
    ),

    # GOAL
    ('Goal', req(FINAL_GOAL_EVENT)),
    (
        'Deep Docks - Beast Shard',
        area(
            3,
            'Deep Docks - Diving Bell',
            'Ancestral Art: Clawline',
        ),
    ),
    (
        'Shellwood - Shard Bundle',
        area(
            1,
            'Shellwood - Greyroot',
            'Ancestral Art: Cling Grip',
        ),
    ),
    (
        'Wormways - Frayed Rosary String',
        area(
            1,
            'Wormways Middle',
            'Ancestral Art: Cling Grip',
        ),
    ),
    *(
        (location_name, req(crest=False))
        for location_name in PLAYTEST_LOCATIONS
        if (
            location_name not in LOGIC_PASS_A_LOCATIONS
            and canonicalize_location_name(location_name)
            not in PROGRESSION_SAFE_CENSUS_LOCATIONS
            and canonicalize_location_name(location_name)
            not in TEMPORARILY_UNVERIFIED_KEY_OR_QUEST_LOCATIONS
        )
    ),
    *(
        (location_name, _minor_pickup_requirement(location_name))
        for location_name in ACTIVE_MINOR_PICKUP_LOCATION_NAMES
        if canonicalize_location_name(location_name)
        not in VERIFIED_MINOR_PICKUP_LOCATIONS
    ),
    *(
        (location_name, _minor_cache_requirement(location_name))
        for location_name in ACTIVE_MINOR_CACHE_LOCATION_NAMES
    ),
    *(
        (
            source.location_name,
            area(
                source.act_number,
                source.path_name,
                *(
                    ('Ancestral Art: Needolin',)
                    if source.requires_needolin
                    else ()
                ),
                crest=(
                    source.location_name
                    != "Moss Grotto - Shaman Storeroom Record"
                ),
            ),
        )
        for source in LORE_TABLET_SOURCES
        if source.location_name != "Verdania - Lake Plaque"
    ),
    (
        'Moss Grotto - Rosary Cache',
        req(
            'Act: 1',
            'Path: Mosslands - Moss Grotto',
            any_of=SWIFT_STEP_OR_SPRINT_ITEMS,
            skip_tier=1,
            act='Act 1',
            path_name='Mosslands - Moss Grotto',
        ),
    ),
)


def _world_order(requirement: LocationRequirement) -> tuple[int, int]:
    act_index = ACT_ORDER.index(requirement.act) if requirement.act in ACT_ORDER else -1
    path_index = PATH_ORDER.index(requirement.path_name) if requirement.path_name in PATH_ORDER else -1
    return act_index, path_index


# A room-graph source normally replaces its old Act, path and movement row.
# These entries keep their established rules because the graph does not cover
# the reward room or its node does not describe the pickup approach.
_ROOM_GRAPH_ESTABLISHED_ONLY_LOCATIONS: frozenset[str] = frozenset(
    (
        'Crest: Shaman',
        'Elegy of the Deep',
        'Relic: Choral Commandment (Moss Grotto)',
        'Bone Bottom - Rosary Cache #8',
        'Bone Bottom - Rosary Cache #9',
        # Their graph records are not yet connected by a complete route.
        'Deep Docks - Rosary Cache #1',
        'Deep Docks - Rosary Cache #2',
    )
)


_CLAWLINE_GATED_LOCATIONS: frozenset[str] = frozenset(
    (
        'Whispering Vaults - Rosary Cache #5',
        'Whispering Vaults - Shell Shard Cache #1',
        'Songclave - Heavy Rosary Necklace',
        'Relic: Psalm Cylinder (East Whispering Vaults)',
        'Deep Docks - Shard Bundle #1',
        'Deep Docks - Shell Shard Cache #5',
        'Deep Docks - Rosary Cache #1',
        'Deep Docks - Rosary Cache #2',
        'Flintslate',
        'Deep Docks - Shell Shard Cache #6',
        'Deep Docks - Shell Shard Cache #7',
        'Deep Docks - Shell Shard Cache #8',
        'Deep Docks - Shell Shard Cache #9',
        'Cogfly',
        'High Halls - Shell Shard Cache #2',
    )
)


# These local conditions remain attached to every room-graph source clause.
# They supplement source geometry instead of becoming alternate routes.
_ROOM_GRAPH_PRESERVED_LOCAL_GATES: Mapping[
    str, tuple[LocationRequirement, ...]
] = {
    **{
        location_name: (
            req('Ancestral Art: Clawline', crest=False),
        )
        for location_name in _CLAWLINE_GATED_LOCATIONS
    },
    'Throwing Ring': (
        req(
            "Event: Trail's End Completed",
            room_node_name('bellhart/belltown#lower-area'),
            crest=False,
        ),
    ),
    'Needolin': (
        req('Path: Bellhart - Widow', crest=False),
    ),
    'Boss: Widow': (
        req('Path: Bellhart - Widow', crest=False),
    ),
    'Boss: Nyleth': (
        req('Event: Shrine Guardian Seth Defeated', crest=False),
    ),
    'Cogwork Core - Pristine Core': (
        req('Act: 3', crest=False, act='Act 3'),
    ),
    # Forge Daughter consumes one Craftmetal for each of these purchases. The
    # Silkshot graph clause already carries its separate Ruined Tool gate.
    'Greymoor - Bellshrine': (
        req('Event: Craw Lake Cleared', crest=False),
    ),
    'Flea: Greymoor - Craw Lake': (
        req('Event: Craw Lake Cleared', crest=False),
    ),
    'Threefold Pin': (
        req('Event: Craw Lake Cleared', crest=False),
    ),
    'Thread Storm': (
        req('Event: Craw Lake Cleared', crest=False),
    ),
    'Greymoor - Spool Fragment': (
        req('Event: Craw Lake Cleared', crest=False),
    ),
    'Greymoor - Map Purchase': (
        req('Event: Craw Lake Cleared', crest=False),
    ),
    'Silkshot (Forge Daughter)': (
        req(CRAFTMETAL_ITEM, crest=False),
    ),
    'Sting Shard': (
        req(CRAFTMETAL_ITEM, crest=False),
    ),
    'Magma Bell': (
        req(CRAFTMETAL_ITEM, crest=False),
    ),
    # Keelal appears only after Greyroot's Rite of Rebirth. Preserve this
    # local story gate when the room graph replaces the old flat source row.
    'Relic: Weaver Effigy (Keelal, Shellwood)': (
        req(RITE_OF_REBIRTH_EVENT, crest=False),
    ),
    'Pin Purchase: Bellway Pins': (
        req('Event: Bell Beast Defeated', crest=False),
    ),
    'Loddie - Tool Pouch': (
        req('Event: Widow Defeated', crest=False),
    ),
    'Wish: Bone Bottom Repairs': (
        req('Event: Bone Bottom Repairs Completed', crest=False),
    ),
    'Wish: A Lifesaving Bridge': (
        req('Event: Lifesaving Bridge Completed', crest=False),
    ),
    'Wish: An Icon of Hope': (
        req(
            'Act: 2',
            'Event: Lifesaving Bridge Completed',
            crest=False,
            act='Act 2',
        ),
    ),
    # The large fossil is a child of fixer_statue. That parent is activated
    # only after Building Materials (Statue) / An Icon of Hope completes, so
    # merely reaching Bone Bottom cannot make this physical cache available.
    'Bone Bottom - Shell Shard Cache': (
        req(
            'Act: 2',
            'Event: Lifesaving Bridge Completed',
            crest=False,
            act='Act 2',
        ),
    ),
    'Wish: Garb of the Pilgrims': (
        req(
            'Act: 1',
            'Path: The Marrow - Mosshome Gate',
            'Event: Bell Beast Defeated',
            crest=False,
            act='Act 1',
        ),
    ),
    'Wish: Volatile Flintbeetles': (
        _volatile_flintbeetle_act_one_requirement(crest=False),
        # The unfinished Wish becomes a ground reward in Bone_10 in Act 3.
        req('Act: 3', crest=False, act='Act 3'),
    ),
    'Wish: The Terrible Tyrant': (
        req(
            'Act: 1',
            'Ancestral Art: Cling Grip',
            crest=False,
            act='Act 1',
        ),
    ),
    'Wish: My Missing Courier': (
        req('Event: Missing Courier Rescued', crest=False),
    ),
    SINNER_MISSING_BROTHER_LOCATION: (
        req('Event: Missing Brother Rescued', crest=False),
    ),
    'Shellwood - Weaver Harp Inscription': (
        req('Ancestral Art: Needolin', crest=False),
    ),
    'Bellhart Shop - Memory Locket': (
        req('Event: Widow Defeated', crest=False),
    ),
    'Frey (Bellhart) - Spool Fragment': (
        req('Event: Missing Courier Rescued', crest=False),
    ),
    'Multibinder': (
        req('Event: Missing Courier Rescued', crest=False),
    ),
    'Bellhart - Map Purchase': (
        req('Event: Widow Defeated', crest=False),
    ),
    'Pinmaster Plinney: Sharpened Needle': (
        req('Event: Widow Defeated', crest=False),
    ),
    'Pinmaster Plinney: Shining Needle': (
        req(
            'Event: Widow Defeated',
            crest=False,
            item_counts=(
                item_count(1, PROGRESSIVE_NEEDLE_UPGRADE_ITEM),
                item_count(1, PALE_OIL_ITEM),
            ),
        ),
    ),
    'Pinmaster Plinney: Hivesteel Needle': (
        req(
            'Event: Widow Defeated',
            crest=False,
            item_counts=(
                item_count(2, PROGRESSIVE_NEEDLE_UPGRADE_ITEM),
                item_count(2, PALE_OIL_ITEM),
            ),
        ),
    ),
    'Pinmaster Plinney: Pale Steel Needle': (
        req(
            'Event: Widow Defeated',
            crest=False,
            item_counts=(
                item_count(3, PROGRESSIVE_NEEDLE_UPGRADE_ITEM),
                item_count(3, PALE_OIL_ITEM),
            ),
        ),
    ),
    'Bellhart - Bellshrine': (
        req('Event: Widow Defeated', crest=False),
    ),
    'Boss: Skarrsinger Karmelita': (
        req(),
    ),
    'Far Fields (Skull Cave) - Mask Shard': (
        req('Act: 2', crest=False, act='Act 2'),
    ),
    **{
        location_name: (
            req(
                'Event: Widow Defeated',
                relic_item_name,
                crest=False,
            ),
        )
        for location_name, relic_item_name
        in SCROUNGE_RELIC_ITEM_BY_TURN_IN_LOCATION.items()
    },
}


# These are distinct physical sources or later vendor-stock states.  They stay
# OR alternatives to the room-graph source. They are never combined
# with it as though their path were an extra local movement requirement.
_ROOM_GRAPH_EXTERNAL_SOURCE_ALTERNATIVES: Mapping[
    str, tuple[LocationRequirement, ...]
] = {
    'Boss: Fourth Chorus': (
        req('Event: Act 3 Started', crest=False),
    ),
    'Boss: Trobbio': (
        req('Event: Act 3 Started', crest=False),
    ),
    'Greymoor - Map Purchase': (
        req('Path: Greymoor - Halfway House', crest=False),
    ),
    'Bone Bottom Shop - Craftmetal': grindle_access(3),
    'Bone Bottom Shop - Simple Key': grindle_access(3),
    'Pebb (Bone Bottom) / Grindle (Act 3) - Mask Shard': (
        grindle_access(3)
    ),
    'Magnetite Brooch': grindle_access(3),
    'The Marrow - Map Purchase': (
        req('Event: Bell Beast Defeated', crest=False),
    ),
    'Deep Docks - Map Purchase': (
        req('Event: Widow Defeated', crest=False),
    ),
    'Wormways - Map Purchase': (
        req('Event: Act 2 Started', crest=False),
    ),
    'Shellwood - Map Purchase': (
        req('Event: Widow Defeated', crest=False),
    ),
    'Blasted Steps - Map Purchase': (
        req('Event: Last Judge Defeated', crest=False),
    ),
    'Far Fields - Map Purchase': (
        req('Event: Widow Defeated', crest=False),
        req('Event: Act 2 Started', crest=False),
    ),
    "Hunter's March - Map Purchase": (
        req('Event: Act 2 Started', crest=False),
    ),
    "Pilgrim's Rest Shop - Memory Locket": grindle_access(3),
    "Pilgrim's Rest - Tool Pouch": grindle_access(3),
    'Pin Purchase: Vendor Pins': (
        req('Path: Greymoor - Halfway House', crest=False),
    ),
}


def _merge_item_count_requirements(
    *groups: Iterable[ItemCountRequirement],
) -> tuple[ItemCountRequirement, ...]:
    """Combine equal item-count predicates using their stricter minimum."""

    merged: dict[tuple[str, ...], int] = {}
    for group in groups:
        for count_requirement in group:
            item_names = count_requirement.item_names
            merged[item_names] = max(
                merged.get(item_names, 0),
                count_requirement.minimum,
            )
    return tuple(
        item_count(minimum, *item_names)
        for item_names, minimum in merged.items()
    )


def _combine_room_graph_gate(
    graph_source: LocationRequirement,
    gate: LocationRequirement,
) -> LocationRequirement:
    """Attach one non-source gate to one source."""

    return LocationRequirement(
        all_of=tuple(dict.fromkeys((
            *graph_source.all_of,
            *gate.all_of,
        ))),
        any_of=tuple(dict.fromkeys((*graph_source.any_of, *gate.any_of))),
        required_locations=tuple(dict.fromkeys((
            *graph_source.required_locations,
            *gate.required_locations,
        ))),
        require_any_crest=(
            graph_source.require_any_crest or gate.require_any_crest
        ),
        require_silk_spear=(
            graph_source.require_silk_spear or gate.require_silk_spear
        ),
        minimum_skip_tier=max(
            graph_source.minimum_skip_tier,
            gate.minimum_skip_tier,
        ),
        act=gate.act or graph_source.act,
        path_name=gate.path_name or graph_source.path_name,
        item_counts=_merge_item_count_requirements(
            graph_source.item_counts,
            gate.item_counts,
        ),
    )


_CANONICAL_REQUIREMENT_ROW_SOURCE: tuple[
    tuple[str, LocationRequirement], ...
] = tuple(
    (
        canonicalize_location_name(location_name),
        requirement,
    )
    for location_name, requirement in REQUIREMENT_ROW_SOURCE
)


def _compile_requirements(
    rows: Iterable[tuple[str, LocationRequirement]],
) -> Dict[str, tuple[LocationRequirement, ...]]:
    compiled: dict[str, list[LocationRequirement]] = {}
    for location_name, requirement in rows:
        compiled.setdefault(location_name, []).append(requirement)
    return {name: tuple(requirements) for name, requirements in compiled.items()}


def _attach_preserved_local_gates(
    location_name: str,
    sources: Iterable[LocationRequirement],
) -> Iterable[LocationRequirement]:
    gates = _ROOM_GRAPH_PRESERVED_LOCAL_GATES.get(location_name)
    if MAPPER_GRAPH_ENABLED and location_name in {
        'Wish: Volatile Flintbeetles',
        'Volatile Flintbeetles - Memory Locket',
        'Pinmaster Plinney: Sharpened Needle',
        'Pinmaster Plinney: Shining Needle',
        'Pinmaster Plinney: Hivesteel Needle',
        'Pinmaster Plinney: Pale Steel Needle',
    }:
        gates = None
    if not gates:
        yield from sources
        return
    yield from (
        _combine_room_graph_gate(source, gate)
        for source in sources
        for gate in gates
    )


_ESTABLISHED_REQUIREMENTS_BY_LOCATION: dict[
    str, tuple[LocationRequirement, ...]
] = _compile_requirements(_CANONICAL_REQUIREMENT_ROW_SOURCE)


def _authoritative_requirement_rows() -> Iterable[
    tuple[str, LocationRequirement]
]:
    """Resolve established rows against the authoritative room graph."""

    for location_name, established in _ESTABLISHED_REQUIREMENTS_BY_LOCATION.items():
        graph_sources = ROOM_CHECK_REQUIREMENTS.get(location_name)
        if MAPPER_GRAPH_ENABLED and not graph_sources and location_name != 'Goal':
            yield location_name, req(crest=False)
            continue
        if (
            not graph_sources
            or (not MAPPER_GRAPH_ENABLED and location_name in _ROOM_GRAPH_ESTABLISHED_ONLY_LOCATIONS)
        ):
            yield from (
                (location_name, requirement)
                for requirement in _attach_preserved_local_gates(
                    location_name,
                    established,
                )
            )
            continue

        yield from (
            (location_name, requirement)
            for requirement in _attach_preserved_local_gates(
                location_name,
                graph_sources,
            )
        )

        yield from (
            (location_name, alternative)
            for alternative in (() if MAPPER_GRAPH_ENABLED else _ROOM_GRAPH_EXTERNAL_SOURCE_ALTERNATIVES.get(
                location_name,
                (),
            ))
        )

    # A graph source may precede its flat fallback row and takes precedence
    # once all of its requirements compile.
    yield from (
        (location_name, requirement)
        for location_name, requirements in ROOM_CHECK_REQUIREMENTS.items()
        if location_name not in _ESTABLISHED_REQUIREMENTS_BY_LOCATION
        for requirement in _attach_preserved_local_gates(
            location_name,
            requirements,
        )
    )


REQUIREMENT_ROWS: tuple[tuple[str, LocationRequirement], ...] = tuple(
    sorted(
        _authoritative_requirement_rows(),
        key=lambda row: _world_order(row[1]),
    )
)


REQUIREMENTS: Dict[str, tuple[LocationRequirement, ...]] = _compile_requirements(REQUIREMENT_ROWS)
from .boss_journal import base_requirements as journal_requirements
REQUIREMENTS.update(journal_requirements(REQUIREMENTS, req))

# Locations stay in the pool but cannot hold required progression until their
# omitted vanilla key, quest, mode or movement condition is represented.
UNVERIFIED_PROGRESSION_LOCATIONS: frozenset[str] = frozenset(
    canonicalize_location_name(location_name)
    for location_name in (
        # These sources occur in a graph area, but at least one room
        # transition, local condition or identity is unresolved.
        *(
            ROOM_GRAPH_QUARANTINED_CHECK_NAMES
            - ROOM_GRAPH_PROMOTED_FALLBACK_LOCATIONS
        ),
        # Its verified traversal can still self-lock required movement during
        # fill, so keep the check non-progression until placement can model it.
        'Blasted Steps - Mask Shard',
        'Pimpillo',
        'Greymoor - Silkeater',
        'Far Fields - Shell Shard Cache #8',
        'Boss: Skull Tyrant (Bone Bottom)',
        'Tool Unlock: Reserve Bind',
        'Relic: Bone Scroll (Wisp Thicket)',
        'Wisp Thicket - Mask Shard',
        'Map Purchase: The Cradle',
        'Map Pickup: Verdania',
        'Map Pickup: The Abyss',
        'Beastling Call',
        # Curvesickle's source-room movement is incomplete, so it may be useful
        # but not required progression.
        'Curvesickle',
        # Their minimum room traversal requirements are not represented.
        'Tool Pouch: Bugs of Pharloom',
        "Beast Shard: Pilgrim's Rest",
        'Beast Shard: Memorium',
        'Beast Shard: Sprintmaster',
        'Flea: Memorium - Huge Flea',
        *TEMPORARILY_UNVERIFIED_SHARED_CHECK_LOCATIONS,
        *TEMPORARILY_UNVERIFIED_KEY_OR_QUEST_LOCATIONS,
        *(
            location_name
            for location_name in PLAYTEST_LOCATIONS
            if (
                location_name not in LOGIC_PASS_A_LOCATIONS
                and canonicalize_location_name(location_name)
                not in PROGRESSION_SAFE_CENSUS_LOCATIONS
                and canonicalize_location_name(location_name)
                not in ROOM_GRAPH_CANONICAL_CHECK_NAMES
            )
        ),
        *(
            location_name
            for location_name in ACTIVE_MINOR_PICKUP_LOCATION_NAMES
            if location_name not in {
                'Moss Grotto - Frayed Rosary String',
                'The Marrow (Flea Caravan Passage) - Frayed Rosary String',
                *VERIFIED_MINOR_PICKUP_LOCATIONS,
            }
        ),
    )
)

# Most Quest checks enter the pool before all route state is represented.
# They may hold any item that is not required for progression.
JUNK_ONLY_LOCATIONS: frozenset[str] = frozenset(
    canonicalize_location_name(location_name)
    for location_name in (
        *JUNK_ONLY_QUEST_LOCATIONS,
        *SINNER_ROAD_UNRESOLVED_COMMUNITY_CHECK_NAMES,
        *SINNER_ROAD_NON_COMMUNITY_FALLBACK_CHECK_NAMES,
        # These scripted or held sources have incomplete encounter
        # requirements, so they may hold only non-advancement rewards.
        'Fleatopia - Rosary Necklace',
        'Fleatopia - Rosary String',
        *HELD_MINOR_PICKUP_LOCATIONS,
        # These caches remain non-advancement-only until their room movement
        # requirements are represented.
        *(
            location_name
            for location_name in ACTIVE_MINOR_CACHE_LOCATION_NAMES
            if (
                canonicalize_location_name(location_name)
                not in MANUALLY_VERIFIED_MINOR_CACHE_LOCATIONS
            )
        ),
        *LORE_TABLET_JUNK_ONLY_LOCATION_NAMES,
    )
) | ALWAYS_JUNK_ONLY_MISSABLE_LOCATIONS

# These checks have incomplete routes. They unlock after Victory and cannot
# hold advancement items.
LOGIC_UNKNOWN_LOCATIONS: frozenset[str] = (
    UNVERIFIED_PROGRESSION_LOCATIONS | JUNK_ONLY_LOCATIONS
) - frozenset((PINMASTER_OIL_QUEST_LOCATION,))
if MAPPER_GRAPH_ENABLED:
    UNVERIFIED_PROGRESSION_LOCATIONS = ROOM_GRAPH_QUARANTINED_CHECK_NAMES
    JUNK_ONLY_LOCATIONS = frozenset(ALWAYS_JUNK_ONLY_MISSABLE_LOCATIONS & location_data_table.keys())
    LOGIC_UNKNOWN_LOCATIONS = UNVERIFIED_PROGRESSION_LOCATIONS

LOGIC_UNKNOWN_LOCATIONS |= BUGS_OF_PHARLOOM_REWARD_LOCATIONS

LOGIC_PASS_A_PROGRESSION_LOCATIONS: frozenset[str] = (
    _LOGIC_PASS_A_PROGRESSION_CANDIDATES - LOGIC_UNKNOWN_LOCATIONS - JUNK_ONLY_LOCATIONS
)


class _AssumedMapperInventory:
    def __init__(self, unavailable_items):
        self.unavailable_items = unavailable_items
        self.prog_items = {1: Counter({'assumed inventory': 1})}

    def count(self, item, player):
        return 0 if clean_item_display_name(item) in self.unavailable_items else 1_000_000

    def has(self, item, player, count=1):
        return self.count(item, player) >= count


def get_mapper_option_quarantines(unavailable_items=frozenset(), **options) -> frozenset[str]:
    if not MAPPER_GRAPH_ENABLED:
        return frozenset()
    state = _AssumedMapperInventory(unavailable_items)
    return frozenset(
        name for name in ROOM_GRAPH_CANONICAL_CHECK_NAMES
        if not make_requirements_rule(get_location_requirements(name), 1, **options)(state)
    )


def is_logic_unknown_location(location_name: str) -> bool:
    """Return whether a check still has unresolved access logic."""

    return (
        canonicalize_location_name(location_name)
        in LOGIC_UNKNOWN_LOCATIONS
    )

# This path is retained as a map landmark but currently has no location or
# onward route attached to it.
ALLOWED_DEAD_PATHS: frozenset[str] = frozenset(
    ('Path: Shellwood - Chapel Exit',)
)


def has_any_crest(state: CollectionState, player: int) -> bool:
    return any(state.has(crest, player) for crest in CREST_ITEMS)


def has_any_non_architect_crest(state: CollectionState, player: int) -> bool:
    return any(state.has(crest, player) for crest in NON_ARCHITECT_CREST_ITEMS)


def has_silk_spear(state: CollectionState, player: int) -> bool:
    return (
        state.has('Silkspear', player)
        and has_any_non_architect_crest(state, player)
    )


_STATIC_ABSTRACT_REQUIREMENT_ITEMS = tuple(ABSTRACT_REQUIREMENTS.items())
_STATIC_BELLWAY_ABSTRACT_REQUIREMENT_ITEMS = tuple(
    (
        requirement_name,
        BELLWAY_RANDOMIZED_STATIONS_REQUIREMENTS
        if requirement_name == 'Path: Bellways'
        else alternatives,
    )
    for requirement_name, alternatives in _STATIC_ABSTRACT_REQUIREMENT_ITEMS
)
_STATIC_VANILLA_CREST_SLOT_ABSTRACT_REQUIREMENT_ITEMS = tuple(
    (
        requirement_name,
        VANILLA_CREST_SLOT_COLORED_TOOL_REQUIREMENTS.get(
            requirement_name,
            alternatives,
        ),
    )
    for requirement_name, alternatives in _STATIC_ABSTRACT_REQUIREMENT_ITEMS
)
_STATIC_BELLWAY_VANILLA_CREST_SLOT_ABSTRACT_REQUIREMENT_ITEMS = tuple(
    (
        requirement_name,
        BELLWAY_RANDOMIZED_STATIONS_REQUIREMENTS
        if requirement_name == 'Path: Bellways'
        else VANILLA_CREST_SLOT_COLORED_TOOL_REQUIREMENTS.get(
            requirement_name,
            alternatives,
        ),
    )
    for requirement_name, alternatives in _STATIC_ABSTRACT_REQUIREMENT_ITEMS
)


@lru_cache(maxsize=64)
def _get_static_abstract_requirement_items(
    allow_bellways_before_bell_beast: bool,
    randomized_crest_slots_enabled: bool,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    pollip_heart_count: int = 0,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
) -> tuple[tuple[str, tuple[LocationRequirement, ...]], ...]:
    starting_location = normalize_starting_location_key(starting_location)
    trails_end_requirement = normalize_trails_end_requirement(
        trails_end_requirement
    )
    if pollip_heart_count not in (0, POLLIP_HEART_COUNT):
        raise ValueError(
            "Pollip Heart count must use the live quest threshold of "
            f"{POLLIP_HEART_COUNT} but received {pollip_heart_count!r}."
        )
    if randomized_crest_slots_enabled:
        requirement_items = (
            _STATIC_BELLWAY_ABSTRACT_REQUIREMENT_ITEMS
            if allow_bellways_before_bell_beast
            else _STATIC_ABSTRACT_REQUIREMENT_ITEMS
        )
    else:
        requirement_items = (
            _STATIC_BELLWAY_VANILLA_CREST_SLOT_ABSTRACT_REQUIREMENT_ITEMS
            if allow_bellways_before_bell_beast
            else _STATIC_VANILLA_CREST_SLOT_ABSTRACT_REQUIREMENT_ITEMS
        )

    if not randomized_crest_slots_enabled:
        eva_rules = eva_point_requirements(False)
        requirement_items = tuple((name, eva_rules.get(name, alternatives)) for name, alternatives in requirement_items)

    if silk_and_soul_points != 17:
        requirement_items = tuple(
            (name, get_silk_and_soul_requirements(silk_and_soul_points) if name == 'Event: Silk and Soul Offered' else alternatives)
            for name, alternatives in requirement_items
        )

    if steel_soul:
        from .game_modes import RESTING_SITES_VISITED, resting_site_requirements
        requirement_items = tuple((name, resting_site_requirements(steel_soul_sites) if name == RESTING_SITES_VISITED else rules)
                                  for name, rules in requirement_items)
        requirement_items = tuple(
            (name, (req(crest=False),) if name == "Option: Steel Soul On" else () if name == "Option: Steel Soul Off" else alternatives)
            for name, alternatives in requirement_items
        )

    if bell_shrine_sanity:
        requirement_items = tuple(
            (name, (req(crest=False),) if name == "Option: Bellshrinesanity On" else () if name == "Option: Bellshrinesanity Off" else alternatives)
            for name, alternatives in requirement_items
        )

    if proficient_movement:
        requirement_items = tuple(
            (name, PROFICIENT_COMBAT_REQUIREMENTS if name == "Option: Proficient Movement" else alternatives)
            for name, alternatives in requirement_items
        )

    if flea_brew_jump_logic:
        requirement_items = tuple(
            (name, (req(crest=False),) if name == "Option: Flea Brew Jump Logic" else alternatives)
            for name, alternatives in requirement_items
        )

    if not sharpdart_logic:
        requirement_items = tuple(
            (name, () if name == USABLE_SHARPDART_REQUIREMENT else alternatives)
            for name, alternatives in requirement_items
        )

    technique_overrides = technique_requirement_overrides(
        heal_stall_tier, hazard_respawn_tier, scuttlebrace_tier,
        red_tool_stall_tier, crest_pogo_tier, needle_strike_tier, enemy_pogo_tier, drill_crystal_pogo_tier,
    )
    requirement_items = tuple((name, technique_overrides.get(name, alternatives)) for name, alternatives in requirement_items)

    if proficient_combat:
        combat_overrides = combat_requirement_overrides(proficient_combat)
        requirement_items = tuple(
            (name, combat_overrides.get(name, alternatives))
            for name, alternatives in requirement_items
        )

    if randomize_ledge_grab or randomize_swim:
        randomized_capabilities = {
            **(
                {
                    LEDGE_GRAB_CAPABILITY_REQUIREMENT: (
                        RANDOMIZED_INNATE_CAPABILITY_REQUIREMENTS[
                            LEDGE_GRAB_CAPABILITY_REQUIREMENT
                        ]
                    )
                }
                if randomize_ledge_grab
                else {}
            ),
            **(
                {
                    SWIM_CAPABILITY_REQUIREMENT: (
                        RANDOMIZED_INNATE_CAPABILITY_REQUIREMENTS[
                            SWIM_CAPABILITY_REQUIREMENT
                        ]
                    )
                }
                if randomize_swim
                else {}
            ),
        }
        requirement_items = tuple(
            (
                requirement_name,
                randomized_capabilities.get(
                    requirement_name,
                    alternatives,
                ),
            )
            for requirement_name, alternatives in requirement_items
        )

    if (
        starting_location == STARTING_LOCATION_VANILLA
        and trails_end_requirement == TRAILS_END_REQUIREMENT_SHAKRA_STOCK
        and not pollip_heart_count
    ):
        return requirement_items

    return tuple(
        (
            requirement_name,
            MOSS_GROTTO_WITHOUT_START_ROOT_REQUIREMENTS
            if (
                starting_location == STARTING_LOCATION_BONE_BOTTOM
                and requirement_name == 'Path: Mosslands - Moss Grotto'
            )
            else BONE_BOTTOM_START_ROOT_REQUIREMENTS
            if (
                starting_location == STARTING_LOCATION_BONE_BOTTOM
                and requirement_name == 'Path: Mosslands - Bone Bottom'
            )
            else get_trails_end_requirements(trails_end_requirement)
            if (
                requirement_name == "Event: Trail's End Completed"
                and trails_end_requirement
                == TRAILS_END_REQUIREMENT_OWNED_MAPS
            )
            else _get_pollip_rite_room_requirements(pollip_heart_count)
            if (
                requirement_name == POLLIP_RITE_ROOM_NODE
                and pollip_heart_count
            )
            else alternatives,
        )
        for requirement_name, alternatives in requirement_items
    )


@dataclass(frozen=True)
class _AbstractWorklistPlan:
    requirement_names: tuple[str, ...]
    dependents_by_requirement: Mapping[str, tuple[str, ...]]


def _iter_abstract_references_for_worklist(
    requirement: LocationRequirement,
    known_requirements: frozenset[str],
    active_locations: tuple[str, ...] = (),
) -> Iterable[str]:
    yield from (
        reference
        for reference in (*requirement.all_of, *requirement.any_of)
        if reference in known_requirements
    )
    for location_name in requirement.required_locations:
        canonical_name = canonicalize_location_name(location_name)
        if canonical_name in active_locations:
            continue
        next_active_locations = (*active_locations, canonical_name)
        for location_requirement in REQUIREMENTS.get(canonical_name, ()):
            yield from _iter_abstract_references_for_worklist(
                location_requirement,
                known_requirements,
                next_active_locations,
            )


@lru_cache(maxsize=16)
def _compile_abstract_worklist_plan(
    requirements_signature: tuple[
        tuple[str, tuple[LocationRequirement, ...]], ...
    ],
) -> _AbstractWorklistPlan:
    """Index abstract reverse dependencies for one option-adjusted graph.

    The structural signature keeps cached plans valid if the graph changes.
    Normal worlds reuse the compiled plan after the first solve.
    """

    requirement_names = tuple(
        name for name, _alternatives in requirements_signature
    )
    known_requirements = frozenset(requirement_names)
    dependents: dict[str, list[str]] = {
        name: [] for name in requirement_names
    }
    for owner_name, alternatives in requirements_signature:
        dependencies = {
            reference
            for requirement in alternatives
            for reference in _iter_abstract_references_for_worklist(
                requirement,
                known_requirements,
            )
        }
        for dependency_name in dependencies:
            dependents[dependency_name].append(owner_name)

    return _AbstractWorklistPlan(
        requirement_names=requirement_names,
        dependents_by_requirement={
            name: tuple(owners)
            for name, owners in dependents.items()
            if owners
        },
    )


@lru_cache(maxsize=64)
def _compile_static_abstract_worklist_plan(
    allow_bellways_before_bell_beast: bool,
    randomized_crest_slots_enabled: bool,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    pollip_heart_count: int = 0,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
) -> _AbstractWorklistPlan:
    requirements_signature = _get_static_abstract_requirement_items(
        allow_bellways_before_bell_beast,
        randomized_crest_slots_enabled,
        starting_location,
        trails_end_requirement,
        randomize_ledge_grab,
        randomize_swim,
        pollip_heart_count,
        proficient_combat=proficient_combat,
        proficient_movement=proficient_movement,
        flea_brew_jump_logic=flea_brew_jump_logic,
        sharpdart_logic=sharpdart_logic,
        red_tool_stall_tier=red_tool_stall_tier,
        crest_pogo_tier=crest_pogo_tier,
        needle_strike_tier=needle_strike_tier,
        enemy_pogo_tier=enemy_pogo_tier,
        drill_crystal_pogo_tier=drill_crystal_pogo_tier,
        heal_stall_tier=heal_stall_tier,
        hazard_respawn_tier=hazard_respawn_tier,
        scuttlebrace_tier=scuttlebrace_tier,
        bell_shrine_sanity=bell_shrine_sanity,
        steel_soul=steel_soul,
        steel_soul_sites=steel_soul_sites,
        silk_and_soul_points=silk_and_soul_points,
    )
    return _compile_abstract_worklist_plan(requirements_signature)


def _matches_static_abstract_requirements(
    abstract_requirements: Mapping[
        str,
        tuple[LocationRequirement, ...],
    ],
    allow_bellways_before_bell_beast: bool,
    randomized_crest_slots_enabled: bool,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    pollip_heart_count: int = 0,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
) -> bool:
    """Return whether this is the unchanged runtime graph."""

    expected_items = _get_static_abstract_requirement_items(
        allow_bellways_before_bell_beast,
        randomized_crest_slots_enabled,
        starting_location,
        trails_end_requirement,
        randomize_ledge_grab,
        randomize_swim,
        pollip_heart_count,
        proficient_combat=proficient_combat,
        proficient_movement=proficient_movement,
        flea_brew_jump_logic=flea_brew_jump_logic,
        sharpdart_logic=sharpdart_logic,
        red_tool_stall_tier=red_tool_stall_tier,
        crest_pogo_tier=crest_pogo_tier,
        needle_strike_tier=needle_strike_tier,
        enemy_pogo_tier=enemy_pogo_tier,
        drill_crystal_pogo_tier=drill_crystal_pogo_tier,
        heal_stall_tier=heal_stall_tier,
        hazard_respawn_tier=hazard_respawn_tier,
        scuttlebrace_tier=scuttlebrace_tier,
        bell_shrine_sanity=bell_shrine_sanity,
        steel_soul=steel_soul,
        steel_soul_sites=steel_soul_sites,
        silk_and_soul_points=silk_and_soul_points,
    )
    return (
        len(abstract_requirements) == len(expected_items)
        and all(
            abstract_requirements.get(requirement_name) is alternatives
            for requirement_name, alternatives in expected_items
        )
    )


def _compute_abstract_values(
    state: CollectionState,
    player: int,
    split_dash_and_sprint: bool = False,
    allow_bellways_before_bell_beast: bool = False,
    skips_tier: int = 0,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    pollip_heart_count: int = 0,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
) -> tuple[
    dict[str, bool],
    bool,
    bool,
    Callable[[str], bool],
    Callable[[str], int],
]:
    """Resolve abstract Act/Path requirements once for a CollectionState.

    The path graph contains many cycles. Recursively expanding Path requirements
    from every location causes Archipelago's fill algorithm to spend most of its
    time walking the same cyclic graph over and over. This computes the same
    least fixed point with a dependency worklist: evaluate every owner once,
    then revisit only owners which reference a newly reachable abstract value.
    """
    logic_item_dependencies = get_logic_item_dependencies(
        split_dash_and_sprint,
        silk_heart_logic=silk_heart_logic,
    )
    item_counts: dict[str, int] = {}

    inventory_signature = _player_inventory_signature(state, player)
    cache_key: tuple[object, ...] | None = None
    cached_snapshot: _AbstractValuesSnapshot | None = None
    if inventory_signature is not None:
        cache_key = (
            player,
            split_dash_and_sprint,
            silk_heart_logic,
            allow_bellways_before_bell_beast,
            skips_tier,
            randomized_crest_slots_enabled,
            normalize_starting_location_key(starting_location),
            normalize_trails_end_requirement(trails_end_requirement),
            scuttlebrace_logic_enabled,
            randomize_ledge_grab,
            randomize_swim,
            pollip_heart_count,
            proficient_combat,
            proficient_movement,
            flea_brew_jump_logic,
            sharpdart_logic,
            red_tool_stall_tier,
            crest_pogo_tier,
            needle_strike_tier,
            enemy_pogo_tier,
            drill_crystal_pogo_tier,
            heal_stall_tier,
            hazard_respawn_tier,
            scuttlebrace_tier,
            bell_shrine_sanity,
            steel_soul,
            steel_soul_sites,
            silk_and_soul_points,
            inventory_signature,
            ABSTRACT_REQUIREMENTS.revision,
        )

    def count_item(item_name: str) -> int:
        canonical_name = clean_item_display_name(item_name)
        if canonical_name not in item_counts:
            count_method = getattr(state, "count", None)
            if callable(count_method):
                count = count_method(canonical_name, player)
            else:
                count = int(state.has(canonical_name, player))
            item_counts[canonical_name] = count
        return item_counts[canonical_name]

    def has_item(item_name: str) -> bool:
        canonical_name = clean_item_display_name(item_name)
        if (
            split_dash_and_sprint
            and canonical_name == SWIFT_STEP_ITEM
        ):
            return count_item(PROGRESSIVE_SWIFT_STEP_ITEM) >= 2
        return count_item(item_name) > 0

    if cache_key is not None:
        cached_snapshot = _get_abstract_values_cache(
            state,
            player,
            cache_key,
        )
    if cached_snapshot is not None:
        item_counts.update(cached_snapshot.item_counts)
        return (
            cached_snapshot.abstract_values,
            cached_snapshot.has_crest,
            cached_snapshot.has_spear,
            has_item,
            count_item,
        )

    has_crest = any(has_item(crest) for crest in CREST_ITEMS)
    has_spear = (
        has_item('Silkspear')
        and any(has_item(crest) for crest in NON_ARCHITECT_CREST_ITEMS)
    )

    abstract_requirements = get_abstract_requirements(
        allow_bellways_before_bell_beast,
        randomized_crest_slots_enabled,
        starting_location,
        trails_end_requirement,
        pollip_heart_count,
        randomize_ledge_grab=randomize_ledge_grab,
        randomize_swim=randomize_swim,
        proficient_combat=proficient_combat,
        proficient_movement=proficient_movement,
        flea_brew_jump_logic=flea_brew_jump_logic,
        sharpdart_logic=sharpdart_logic,
        red_tool_stall_tier=red_tool_stall_tier,
        crest_pogo_tier=crest_pogo_tier,
        needle_strike_tier=needle_strike_tier,
        enemy_pogo_tier=enemy_pogo_tier,
        drill_crystal_pogo_tier=drill_crystal_pogo_tier,
        heal_stall_tier=heal_stall_tier,
        hazard_respawn_tier=hazard_respawn_tier,
        scuttlebrace_tier=scuttlebrace_tier,
        bell_shrine_sanity=bell_shrine_sanity,
        steel_soul=steel_soul,
        steel_soul_sites=steel_soul_sites,
        silk_and_soul_points=silk_and_soul_points,
    )
    if _matches_static_abstract_requirements(
        abstract_requirements,
        allow_bellways_before_bell_beast,
        randomized_crest_slots_enabled,
        starting_location,
        trails_end_requirement,
        randomize_ledge_grab,
        randomize_swim,
        pollip_heart_count,
        proficient_combat=proficient_combat,
        proficient_movement=proficient_movement,
        flea_brew_jump_logic=flea_brew_jump_logic,
        sharpdart_logic=sharpdart_logic,
        red_tool_stall_tier=red_tool_stall_tier,
        crest_pogo_tier=crest_pogo_tier,
        needle_strike_tier=needle_strike_tier,
        enemy_pogo_tier=enemy_pogo_tier,
        drill_crystal_pogo_tier=drill_crystal_pogo_tier,
        heal_stall_tier=heal_stall_tier,
        hazard_respawn_tier=hazard_respawn_tier,
        scuttlebrace_tier=scuttlebrace_tier,
        bell_shrine_sanity=bell_shrine_sanity,
        steel_soul=steel_soul,
        steel_soul_sites=steel_soul_sites,
        silk_and_soul_points=silk_and_soul_points,
    ):
        worklist_plan = _compile_static_abstract_worklist_plan(
            allow_bellways_before_bell_beast,
            randomized_crest_slots_enabled,
            starting_location,
            trails_end_requirement,
            randomize_ledge_grab,
            randomize_swim,
            pollip_heart_count,
            proficient_combat=proficient_combat,
            proficient_movement=proficient_movement,
            flea_brew_jump_logic=flea_brew_jump_logic,
            sharpdart_logic=sharpdart_logic,
            red_tool_stall_tier=red_tool_stall_tier,
            crest_pogo_tier=crest_pogo_tier,
            needle_strike_tier=needle_strike_tier,
            enemy_pogo_tier=enemy_pogo_tier,
            drill_crystal_pogo_tier=drill_crystal_pogo_tier,
            heal_stall_tier=heal_stall_tier,
            hazard_respawn_tier=hazard_respawn_tier,
            scuttlebrace_tier=scuttlebrace_tier,
            bell_shrine_sanity=bell_shrine_sanity,
            steel_soul=steel_soul,
            steel_soul_sites=steel_soul_sites,
            silk_and_soul_points=silk_and_soul_points,
        )
    else:
        # Validation tools occasionally patch the graph. Compile those
        # structural variants independently.
        worklist_plan = _compile_abstract_worklist_plan(
            tuple(abstract_requirements.items())
        )
    abstract_values = {
        requirement_name: False
        for requirement_name in worklist_plan.requirement_names
    }
    pending: deque[str] = deque(worklist_plan.requirement_names)
    queued = set(worklist_plan.requirement_names)

    def activate_if_satisfied(requirement_name: str) -> None:
        if abstract_values[requirement_name]:
            return
        if any(
            _satisfies_requirement_with_values(
                alternative,
                abstract_values,
                has_item,
                count_item,
                has_crest,
                has_spear,
                logic_item_dependencies,
                skips_tier,
                scuttlebrace_logic_enabled=scuttlebrace_logic_enabled,
            )
            for alternative in abstract_requirements[requirement_name]
        ):
            abstract_values[requirement_name] = True
            for owner_name in worklist_plan.dependents_by_requirement.get(
                requirement_name, (),
            ):
                if not abstract_values[owner_name] and owner_name not in queued:
                    pending.append(owner_name)
                    queued.add(owner_name)

    while pending:
        requirement_name = pending.popleft()
        queued.remove(requirement_name)
        activate_if_satisfied(requirement_name)

    if cache_key is not None:
        _store_abstract_values_cache(
            state,
            cache_key,
            _AbstractValuesSnapshot(
                abstract_values=MappingProxyType(abstract_values.copy()),
                item_counts=tuple(item_counts.items()),
                has_crest=has_crest,
                has_spear=has_spear,
            ),
        )

    return abstract_values, has_crest, has_spear, has_item, count_item


def _has_named_requirement_with_values(
    item_or_requirement_name: str,
    abstract_values: Mapping[str, bool],
    has_item: Callable[[str], bool],
    logic_item_dependencies: Mapping[str, tuple[str, ...]] = (
        LOGIC_ITEM_DEPENDENCIES
    ),
    scuttlebrace_logic_enabled: bool = True,
) -> bool:
    if (
        not scuttlebrace_logic_enabled
        and item_or_requirement_name == USABLE_SCUTTLEBRACE_REQUIREMENT
    ):
        return False
    if item_or_requirement_name in abstract_values:
        return abstract_values[item_or_requirement_name]
    canonical_name = clean_item_display_name(
        item_or_requirement_name
    )
    return (
        has_item(item_or_requirement_name)
        and (canonical_name not in CLOAK_REQUIRED_SKILL_ITEMS or any(has_item(crest) for crest in CREST_ITEMS))
        and all(
            has_item(dependency_name)
            for dependency_name in logic_item_dependencies.get(
                canonical_name,
                (),
            )
        )
    )


def _satisfies_requirement_with_values(
    requirement: LocationRequirement,
    abstract_values: Mapping[str, bool],
    has_item: Callable[[str], bool],
    count_item: Callable[[str], int],
    has_crest: bool,
    has_spear: bool,
    logic_item_dependencies: Mapping[str, tuple[str, ...]] = (
        LOGIC_ITEM_DEPENDENCIES
    ),
    skips_tier: int = 0,
    active_locations: tuple[str, ...] = (),
    scuttlebrace_logic_enabled: bool = True,
) -> bool:
    if requirement.minimum_skip_tier > skips_tier:
        return False
    if requirement.require_any_crest and not has_crest:
        return False
    if requirement.require_silk_spear and not has_spear:
        return False
    if requirement.all_of and not all(
        _has_named_requirement_with_values(
            item_name,
            abstract_values,
            has_item,
            logic_item_dependencies,
            scuttlebrace_logic_enabled,
        )
        for item_name in requirement.all_of
    ):
        return False
    if requirement.any_of and not any(
        _has_named_requirement_with_values(
            item_name,
            abstract_values,
            has_item,
            logic_item_dependencies,
            scuttlebrace_logic_enabled,
        )
        for item_name in requirement.any_of
    ):
        return False
    if any(
        not _can_reach_required_location_with_values(
            location_name,
            abstract_values,
            has_item,
            count_item,
            has_crest,
            has_spear,
            logic_item_dependencies,
            skips_tier,
            active_locations,
            scuttlebrace_logic_enabled,
        )
        for location_name in requirement.required_locations
    ):
        return False
    if any(
        sum(count_item(item_name) for item_name in count_requirement.item_names)
        < count_requirement.minimum
        for count_requirement in requirement.item_counts
    ):
        return False
    return True


def _can_reach_required_location_with_values(
    location_name: str,
    abstract_values: Mapping[str, bool],
    has_item: Callable[[str], bool],
    count_item: Callable[[str], int],
    has_crest: bool,
    has_spear: bool,
    logic_item_dependencies: Mapping[str, tuple[str, ...]],
    skips_tier: int,
    active_locations: tuple[str, ...],
    scuttlebrace_logic_enabled: bool,
) -> bool:
    canonical_name = canonicalize_location_name(location_name)
    if canonical_name in LOGIC_UNKNOWN_LOCATIONS:
        return True
    if canonical_name in active_locations:
        return False
    alternatives = REQUIREMENTS.get(canonical_name)
    if not alternatives:
        return False
    next_active_locations = (*active_locations, canonical_name)
    return any(
        _satisfies_requirement_with_values(
            alternative,
            abstract_values,
            has_item,
            count_item,
            has_crest,
            has_spear,
            logic_item_dependencies,
            skips_tier,
            next_active_locations,
            scuttlebrace_logic_enabled,
        )
        for alternative in alternatives
    )


def _has_named_requirement(
    item_or_requirement_name: str,
    state: CollectionState,
    player: int,
    seen: tuple[str, ...] = (),
    split_dash_and_sprint: bool = False,
    allow_bellways_before_bell_beast: bool = False,
    skips_tier: int = 0,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    pollip_heart_count: int = 0,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
) -> bool:
    # Each item or graph requirement uses the fixed-point values.
    # ``seen`` is unused because cycle handling happens in the graph solver.
    del seen
    logic_item_dependencies = get_logic_item_dependencies(
        split_dash_and_sprint,
        silk_heart_logic=silk_heart_logic,
    )
    abstract_values, _, _, has_item, _ = _compute_abstract_values(
        state,
        player,
        split_dash_and_sprint,
        allow_bellways_before_bell_beast,
        skips_tier,
        randomized_crest_slots_enabled,
        starting_location,
        trails_end_requirement,
        scuttlebrace_logic_enabled,
        randomize_ledge_grab,
        randomize_swim,
        pollip_heart_count,
        proficient_combat=proficient_combat,
        proficient_movement=proficient_movement,
        flea_brew_jump_logic=flea_brew_jump_logic,
        sharpdart_logic=sharpdart_logic,
        red_tool_stall_tier=red_tool_stall_tier,
        crest_pogo_tier=crest_pogo_tier,
        needle_strike_tier=needle_strike_tier,
        enemy_pogo_tier=enemy_pogo_tier,
        drill_crystal_pogo_tier=drill_crystal_pogo_tier,
        heal_stall_tier=heal_stall_tier,
        hazard_respawn_tier=hazard_respawn_tier,
        scuttlebrace_tier=scuttlebrace_tier,
        bell_shrine_sanity=bell_shrine_sanity,
        steel_soul=steel_soul,
        steel_soul_sites=steel_soul_sites,
        silk_and_soul_points=silk_and_soul_points,
        silk_heart_logic=silk_heart_logic,
    )
    return _has_named_requirement_with_values(
        item_or_requirement_name,
        abstract_values,
        has_item,
        logic_item_dependencies,
        scuttlebrace_logic_enabled,
    )


def _satisfies_requirement(
    requirement: LocationRequirement,
    state: CollectionState,
    player: int,
    seen: tuple[str, ...] = (),
    split_dash_and_sprint: bool = False,
    skips_tier: int = 0,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    pollip_heart_count: int = 0,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
) -> bool:
    # Evaluate one location requirement using the fixed-point values.
    # ``seen`` is unused because cycle handling happens in the graph solver.
    del seen
    logic_item_dependencies = get_logic_item_dependencies(
        split_dash_and_sprint,
        silk_heart_logic=silk_heart_logic,
    )
    abstract_values, has_crest, has_spear, has_item, count_item = (
        _compute_abstract_values(
            state,
            player,
            split_dash_and_sprint,
            False,
            skips_tier,
            randomized_crest_slots_enabled,
            starting_location,
            trails_end_requirement,
            scuttlebrace_logic_enabled,
            randomize_ledge_grab,
            randomize_swim,
            pollip_heart_count,
            proficient_combat=proficient_combat,
            proficient_movement=proficient_movement,
            flea_brew_jump_logic=flea_brew_jump_logic,
            sharpdart_logic=sharpdart_logic,
            red_tool_stall_tier=red_tool_stall_tier,
            crest_pogo_tier=crest_pogo_tier,
            needle_strike_tier=needle_strike_tier,
            enemy_pogo_tier=enemy_pogo_tier,
            drill_crystal_pogo_tier=drill_crystal_pogo_tier,
            heal_stall_tier=heal_stall_tier,
            hazard_respawn_tier=hazard_respawn_tier,
            scuttlebrace_tier=scuttlebrace_tier,
            bell_shrine_sanity=bell_shrine_sanity,
            steel_soul=steel_soul,
            steel_soul_sites=steel_soul_sites,
            silk_and_soul_points=silk_and_soul_points,
            silk_heart_logic=silk_heart_logic,
        )
    )
    return _satisfies_requirement_with_values(
        requirement,
        abstract_values,
        has_item,
        count_item,
        has_crest,
        has_spear,
        logic_item_dependencies,
        skips_tier,
        scuttlebrace_logic_enabled=scuttlebrace_logic_enabled,
    )


def make_requirements_rule(
    requirements: tuple[LocationRequirement, ...],
    player: int,
    split_dash_and_sprint: bool = False,
    allow_bellways_before_bell_beast: bool = False,
    skips_tier: int = 0,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    pollip_heart_count: int = 0,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
):
    def access_rule(state: CollectionState) -> bool:
        logic_item_dependencies = get_logic_item_dependencies(
            split_dash_and_sprint,
            silk_heart_logic=silk_heart_logic,
        )
        abstract_values, has_crest, has_spear, has_item, count_item = (
            _compute_abstract_values(
                state,
                player,
                split_dash_and_sprint,
                allow_bellways_before_bell_beast,
                skips_tier,
                randomized_crest_slots_enabled,
                starting_location,
                trails_end_requirement,
                scuttlebrace_logic_enabled,
                randomize_ledge_grab,
                randomize_swim,
                pollip_heart_count,
                proficient_combat=proficient_combat,
                proficient_movement=proficient_movement,
                flea_brew_jump_logic=flea_brew_jump_logic,
                sharpdart_logic=sharpdart_logic,
                red_tool_stall_tier=red_tool_stall_tier,
                crest_pogo_tier=crest_pogo_tier,
                needle_strike_tier=needle_strike_tier,
                enemy_pogo_tier=enemy_pogo_tier,
                drill_crystal_pogo_tier=drill_crystal_pogo_tier,
                heal_stall_tier=heal_stall_tier,
                hazard_respawn_tier=hazard_respawn_tier,
                scuttlebrace_tier=scuttlebrace_tier,
                bell_shrine_sanity=bell_shrine_sanity,
                steel_soul=steel_soul,
                steel_soul_sites=steel_soul_sites,
                silk_and_soul_points=silk_and_soul_points,
                silk_heart_logic=silk_heart_logic,
            )
        )
        return any(
            _satisfies_requirement_with_values(
                requirement,
                abstract_values,
                has_item,
                count_item,
                has_crest,
                has_spear,
                logic_item_dependencies,
                skips_tier,
                scuttlebrace_logic_enabled=scuttlebrace_logic_enabled,
            )
            for requirement in requirements
        )

    return access_rule


def make_rule(
    location_name: str,
    player: int,
    split_dash_and_sprint: bool = False,
    allow_bellways_before_bell_beast: bool = False,
    skips_tier: int = 0,
    crest_slot_memory_locket_count: int = 0,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    pollip_heart_count: int = 0,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
):
    if is_logic_unknown_location(location_name):
        return lambda _state: True
    return make_requirements_rule(
        get_location_requirements(
            location_name,
            crest_slot_memory_locket_count,
            pollip_heart_count,
        ),
        player,
        split_dash_and_sprint,
        allow_bellways_before_bell_beast,
        skips_tier,
        randomized_crest_slots_enabled,
        starting_location,
        trails_end_requirement,
        scuttlebrace_logic_enabled,
        randomize_ledge_grab,
        randomize_swim,
        pollip_heart_count,
        proficient_combat=proficient_combat,
        proficient_movement=proficient_movement,
        flea_brew_jump_logic=flea_brew_jump_logic,
        sharpdart_logic=sharpdart_logic,
        red_tool_stall_tier=red_tool_stall_tier,
        crest_pogo_tier=crest_pogo_tier,
        needle_strike_tier=needle_strike_tier,
        enemy_pogo_tier=enemy_pogo_tier,
        drill_crystal_pogo_tier=drill_crystal_pogo_tier,
        heal_stall_tier=heal_stall_tier,
        hazard_respawn_tier=hazard_respawn_tier,
        scuttlebrace_tier=scuttlebrace_tier,
        bell_shrine_sanity=bell_shrine_sanity,
        steel_soul=steel_soul,
        steel_soul_sites=steel_soul_sites,
        silk_and_soul_points=silk_and_soul_points,
        silk_heart_logic=silk_heart_logic,
    )


def get_location_requirements(
    location_name: str,
    crest_slot_memory_locket_count: int = 0,
    pollip_heart_count: int = 0,
) -> tuple[LocationRequirement, ...]:
    """Return option-adjusted requirements for one physical check."""

    canonical_name = canonicalize_location_name(location_name)
    requirements = REQUIREMENTS[canonical_name]
    if crest_slot_memory_locket_count < 0:
        raise ValueError(
            "Crest Slot Memory Locket count cannot be negative."
        )
    if pollip_heart_count < 0:
        raise ValueError("Pollip Heart count cannot be negative.")
    if pollip_heart_count not in (0, POLLIP_HEART_COUNT):
        raise ValueError(
            "Pollip Heart count must use the live quest threshold of "
            f"{POLLIP_HEART_COUNT} but received {pollip_heart_count!r}."
        )

    count_requirements: list[ItemCountRequirement] = []
    if (
        crest_slot_memory_locket_count
        and canonical_name in CREST_SLOT_LOCATION_NAMES
    ):
        count_requirements.append(
            item_count(
                crest_slot_memory_locket_count,
                MEMORY_LOCKET_ITEM,
            )
        )
    pollip_source_requirements: tuple[str, ...] = ()
    if canonical_name == 'Pollip Pouch':
        if pollip_heart_count:
            count_requirements.append(
                item_count(pollip_heart_count, POLLIP_HEART_ITEM)
            )
        else:
            pollip_source_requirements = (
                POLLIP_HEART_SOURCE_LOCATION_NAMES
            )
    if (
        count_requirements
        or pollip_source_requirements
    ):
        return tuple(
            replace(
                requirement,

                required_locations=tuple(dict.fromkeys((
                    *requirement.required_locations,
                    *pollip_source_requirements,
                ))),
                item_counts=(
                    *requirement.item_counts,
                    *count_requirements,
                ),
            )
            for requirement in requirements
        )
    return requirements


def get_pinmaster_oil_requirements(
    randomize_pale_oils: bool,
) -> tuple[LocationRequirement, ...]:
    requirements = get_location_requirements(PINMASTER_OIL_QUEST_LOCATION)
    if not randomize_pale_oils:
        return requirements
    return (area(
        2,
        'Bellhart - Bellhart',
        'Event: Widow Defeated',
        item_counts=(
            item_count(1, PROGRESSIVE_NEEDLE_UPGRADE_ITEM),
            item_count(1, PALE_OIL_ITEM),
        ),
    ),)


def get_crawfather_requirements(
    randomize_needle_upgrades: bool,
    randomize_pale_oils: bool,
) -> tuple[LocationRequirement, ...]:
    """Return Crawfather's movement and Needle upgrade gates."""

    requirements = get_location_requirements(CRAWFATHER_LOCATION)
    if MAPPER_GRAPH_ENABLED and CRAWFATHER_LOCATION in ROOM_GRAPH_CANONICAL_CHECK_NAMES:
        return requirements
    if randomize_needle_upgrades or randomize_pale_oils:
        return tuple(
            replace(
                requirement,
                item_counts=_merge_item_count_requirements(
                    requirement.item_counts,
                    (
                        item_count(
                            2,
                            PROGRESSIVE_NEEDLE_UPGRADE_ITEM,
                        ),
                    ),
                ),
            )
            for requirement in requirements
        )

    needle_requirements = get_location_requirements(
        PINMASTER_OIL_QUEST_LOCATION
    )
    return tuple(
        _combine_room_graph_gate(requirement, needle_requirement)
        for requirement in requirements
        for needle_requirement in needle_requirements
    )


def get_goal_requirements(
    goal_key: str,
    flea_hunt_count: int = DEFAULT_FLEA_HUNT_GOAL_COUNT,
    pollip_heart_count: int = 0,
    spelling_bee_item_names: tuple[str, ...] | None = None,
) -> tuple[LocationRequirement, ...]:
    if pollip_heart_count < 0:
        raise ValueError("Pollip Heart count cannot be negative.")
    if pollip_heart_count not in (0, POLLIP_HEART_COUNT):
        raise ValueError(
            "Pollip Heart count must use the live quest threshold of "
            f"{POLLIP_HEART_COUNT} but received {pollip_heart_count!r}."
        )

    from .alphabet_mode import (
        ALPHABET_ITEM_NAMES,
        SPELLING_BEE_GOAL_KEY,
    )

    if goal_key == SPELLING_BEE_GOAL_KEY:
        return (
            req(
                *(
                    ALPHABET_ITEM_NAMES
                    if spelling_bee_item_names is None
                    else spelling_bee_item_names
                ),
                crest=False,
            ),
        )

    if goal_key == FLEA_HUNT_GOAL_KEY:
        if not (
            MIN_FLEA_HUNT_GOAL_COUNT
            <= flea_hunt_count
            <= MAX_FLEA_HUNT_GOAL_COUNT
        ):
            raise ValueError(
                "Flea Hunt count must be between "
                f"{MIN_FLEA_HUNT_GOAL_COUNT} and "
                f"{MAX_FLEA_HUNT_GOAL_COUNT} but received "
                f"{flea_hunt_count!r}."
            )
        return (
            req(
                crest=False,
                item_counts=(
                    item_count(flea_hunt_count, *FLEA_ITEMS),
                ),
            ),
        )

    try:
        goal_event = GOAL_EVENT_BY_KEY[goal_key]
    except KeyError as exc:
        raise ValueError(f"Unknown Silksong goal option: {goal_key!r}") from exc

    if goal_key == 'cursed_ending':
        if pollip_heart_count:
            # Received Hearts update the native Shell Flower quest count.
            return (
                req(
                    goal_event,
                    item_counts=(
                        item_count(
                            pollip_heart_count,
                            POLLIP_HEART_ITEM,
                        ),
                    ),
                ),
            )

        # Vanilla Hearts use their six physical source routes. Room-graph
        # checks expose movement choices as DNF, so combine one route from
        # each source instead of flattening those choices into an AND gate.
        combined_routes: tuple[LocationRequirement, ...] = (
            req(goal_event, crest=False),
        )
        for location_name in LOCATION_NAMES_BY_CATEGORY['PollipHeart']:
            source_requirements = get_location_requirements(location_name)
            expanded_sources = tuple(
                replace(
                    source_requirement,
                    all_of=(
                        *source_requirement.all_of,
                        *((any_of_item,) if any_of_item is not None else ()),
                    ),
                    any_of=(),
                )
                for source_requirement in source_requirements
                for any_of_item in (
                    source_requirement.any_of
                    if source_requirement.any_of
                    else (None,)
                )
            )
            combined_routes = tuple(dict.fromkeys(
                _combine_room_graph_gate(combined, source_requirement)
                for combined in combined_routes
                for source_requirement in expanded_sources
            ))
        return combined_routes

    return (req(goal_event),)


def make_goal_rule(
    goal_key: str,
    player: int,
    split_dash_and_sprint: bool = False,
    flea_hunt_count: int = DEFAULT_FLEA_HUNT_GOAL_COUNT,
    allow_bellways_before_bell_beast: bool = False,
    skips_tier: int = 0,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    pollip_heart_count: int = 0,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    spelling_bee_item_names: tuple[str, ...] | None = None,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
):
    return make_requirements_rule(
        get_goal_requirements(
            goal_key,
            flea_hunt_count,
            pollip_heart_count,
            spelling_bee_item_names,
        ),
        player,
        split_dash_and_sprint,
        allow_bellways_before_bell_beast,
        skips_tier,
        randomized_crest_slots_enabled,
        starting_location,
        trails_end_requirement,
        scuttlebrace_logic_enabled,
        randomize_ledge_grab,
        randomize_swim,
        pollip_heart_count,
        proficient_combat=proficient_combat,
        proficient_movement=proficient_movement,
        flea_brew_jump_logic=flea_brew_jump_logic,
        sharpdart_logic=sharpdart_logic,
        red_tool_stall_tier=red_tool_stall_tier,
        crest_pogo_tier=crest_pogo_tier,
        needle_strike_tier=needle_strike_tier,
        enemy_pogo_tier=enemy_pogo_tier,
        drill_crystal_pogo_tier=drill_crystal_pogo_tier,
        heal_stall_tier=heal_stall_tier,
        hazard_respawn_tier=hazard_respawn_tier,
        scuttlebrace_tier=scuttlebrace_tier,
        bell_shrine_sanity=bell_shrine_sanity,
        steel_soul=steel_soul,
        steel_soul_sites=steel_soul_sites,
        silk_and_soul_points=silk_and_soul_points,
        silk_heart_logic=silk_heart_logic,
    )


def _export_requirement_group(requirements: tuple[LocationRequirement, ...]) -> dict[str, object]:
    return {
        'alternatives': [
            requirement.as_slot_data()
            for requirement in requirements
        ],
    }


def _apply_scuttlebrace_logic_option(
    requirements: tuple[LocationRequirement, ...],
    enabled: bool,
) -> tuple[LocationRequirement, ...]:
    """Prune Scuttlebrace-only route alternatives when its logic is off."""

    if enabled:
        return requirements

    adjusted: list[LocationRequirement] = []
    for requirement in requirements:
        if USABLE_SCUTTLEBRACE_REQUIREMENT in requirement.all_of:
            continue
        any_of = tuple(
            name
            for name in requirement.any_of
            if name != USABLE_SCUTTLEBRACE_REQUIREMENT
        )
        if requirement.any_of and not any_of:
            continue
        adjusted.append(replace(requirement, any_of=any_of))
    return tuple(adjusted)


def export_requirements(
    goal_key: str = 'act_3',
    flea_hunt_count: int = DEFAULT_FLEA_HUNT_GOAL_COUNT,
    allow_bellways_before_bell_beast: bool = False,
    crest_slot_memory_locket_count: int = 0,
    pollip_heart_count: int = 0,
    bone_bottom_statue_tool_pouch_count: int = 0,
    randomize_needle_upgrades: bool = False,
    randomize_pale_oils: bool = False,
    scuttlebrace_logic_enabled: bool = True,
    spelling_bee_item_names: tuple[str, ...] | None = None,
    randomized_relics: bool = False,
) -> Mapping[str, dict[str, object]]:
    exported: dict[str, dict[str, object]] = {}
    for name, requirements in REQUIREMENTS.items():
        resolved_requirements = (
            get_goal_requirements(
                goal_key,
                flea_hunt_count,
                pollip_heart_count,
                spelling_bee_item_names,
            )
            if name == 'Goal'
            else get_crawfather_requirements(
                randomize_needle_upgrades,
                randomize_pale_oils,
            )
            if name == CRAWFATHER_LOCATION
            else get_pinmaster_oil_requirements(
                randomize_pale_oils
            )
            if name == PINMASTER_OIL_QUEST_LOCATION
            else get_location_requirements(
                name,
                crest_slot_memory_locket_count,
                pollip_heart_count,
            )
        )
        if (
            bone_bottom_statue_tool_pouch_count > 0
            and name in {
                'Wish: An Icon of Hope',
                'Bone Bottom - Shell Shard Cache',
            }
        ):
            resolved_requirements = tuple(
                replace(
                    requirement,
                    item_counts=_merge_item_count_requirements(
                        requirement.item_counts,
                        (
                            item_count(
                                bone_bottom_statue_tool_pouch_count,
                                'Progressive Tool Pouch',
                            ),
                        ),
                    ),
                )
                for requirement in resolved_requirements
            )
        if name == 'Quest Completion: Belltown House Start':
            if randomize_needle_upgrades:
                resolved_requirements = tuple(
                    replace(
                        requirement,
                        item_counts=_merge_item_count_requirements(
                            requirement.item_counts,
                            (
                                item_count(
                                    1,
                                    PROGRESSIVE_NEEDLE_UPGRADE_ITEM,
                                ),
                            ),
                        ),
                    )
                    for requirement in resolved_requirements
                )
            if randomized_relics:
                resolved_requirements = tuple(
                    replace(
                        requirement,
                        any_of=SCROUNGE_RELIC_ITEM_NAMES,
                    )
                    for requirement in resolved_requirements
                )
        group = _export_requirement_group(
            _apply_scuttlebrace_logic_option(
                resolved_requirements,
                scuttlebrace_logic_enabled,
            )
        )
        if name in LOGIC_UNKNOWN_LOCATIONS:
            group['logic_unknown'] = True
        exported[name] = group
    for name in sorted(LOGIC_UNKNOWN_LOCATIONS - set(exported)):
        group = _export_requirement_group(())
        group['logic_unknown'] = True
        exported[name] = group
    return exported


def export_wish_logic_events(
    exported_requirements: Mapping[str, dict[str, object]],
    active_event_names: Iterable[str] | None = None,
) -> list[dict[str, object]]:
    """Export the same hidden event sources used by the AP region graph."""

    active_names = (
        None
        if active_event_names is None
        else frozenset(active_event_names)
    )
    exported_events: list[dict[str, object]] = []
    for event in WISH_LOGIC_EVENTS:
        if active_names is not None and event.location_name not in active_names:
            continue
        if event.source_location:
            source_name = canonicalize_location_name(
                event.source_location
            )
            source_group = exported_requirements[source_name]
        else:
            source_group = _export_requirement_group((
                req(event.source_region, crest=False),
            ))
        exported_events.append({
            'location': event.location_name,
            'item': event.item_name,
            'checked_source': (
                source_name if event.requires_checked_source else ''
            ),
            'requirement': source_group,
        })
    return exported_events


def export_abstract_requirements(
    allow_bellways_before_bell_beast: bool = False,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    pollip_heart_count: int = 0,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    donation_tool_pouch_requirements: Mapping[str, int] | None = None,
    room_node_overrides: Mapping[str, tuple[LocationRequirement, ...]] | None = None,
) -> Mapping[str, dict[str, object]]:
    """Expose the option-adjusted fixed-point graph to external logic tools."""

    exported = {
        name: _export_requirement_group(
            _apply_scuttlebrace_logic_option(
                requirements,
                scuttlebrace_logic_enabled,
            )
        )
        for name, requirements in get_abstract_requirements(
            allow_bellways_before_bell_beast,
            randomized_crest_slots_enabled,
            starting_location,
            trails_end_requirement,
            pollip_heart_count,
            randomize_ledge_grab=randomize_ledge_grab,
            randomize_swim=randomize_swim,
            proficient_combat=proficient_combat,
            proficient_movement=proficient_movement,
            flea_brew_jump_logic=flea_brew_jump_logic,
            sharpdart_logic=sharpdart_logic,
            red_tool_stall_tier=red_tool_stall_tier,
            crest_pogo_tier=crest_pogo_tier,
            needle_strike_tier=needle_strike_tier,
            enemy_pogo_tier=enemy_pogo_tier,
            drill_crystal_pogo_tier=drill_crystal_pogo_tier,
            heal_stall_tier=heal_stall_tier,
            hazard_respawn_tier=hazard_respawn_tier,
            scuttlebrace_tier=scuttlebrace_tier,
            bell_shrine_sanity=bell_shrine_sanity,
            steel_soul=steel_soul,
            steel_soul_sites=steel_soul_sites,
            silk_and_soul_points=silk_and_soul_points,
            donation_tool_pouch_requirements=donation_tool_pouch_requirements,
            room_node_overrides=room_node_overrides,
        ).items()
        if (
            scuttlebrace_logic_enabled
            or name != USABLE_SCUTTLEBRACE_REQUIREMENT
        )
    }

    for event, source in {
        LAST_JUDGE_ROOM_EVENT: 'Boss: Last Judge',
        'Event: Last Judge Defeated': 'Boss: Last Judge',
        'Event: Widow Defeated': 'Boss: Widow',
        'Room Event: event:mapper/reviewed:phantom-defeated': 'Boss: Phantom',
        'Event: Act 2 Started': 'Act: 2',
    }.items():
        if event in exported:
            exported[event]['checked_source'] = source
        for target in load_room_graph().assumptions.get('event_aliases', {}).get(event, ()):
            target_name = room_event_name('event:mapper/' + target)
            if target_name in exported:
                exported[target_name]['checked_source'] = source
    return exported



def export_logic_item_dependencies(
    split_dash_and_sprint: bool = False,
    silk_heart_logic: bool = False,
) -> Mapping[str, list[str]]:
    """Expose implicit item dependencies to diagnostics and external logic tools."""

    return {
        item_name: list(dependencies)
        for item_name, dependencies in get_logic_item_dependencies(
            split_dash_and_sprint,
            silk_heart_logic=silk_heart_logic,
        ).items()
    }


def _iter_named_references(requirements: Iterable[LocationRequirement]) -> Iterable[str]:
    for requirement in requirements:
        yield from requirement.all_of
        yield from requirement.any_of
        for count_requirement in requirement.item_counts:
            yield from count_requirement.item_names


def _all_requirement_groups() -> tuple[tuple[LocationRequirement, ...], ...]:
    return tuple(REQUIREMENTS.values()) + tuple(ABSTRACT_REQUIREMENTS.values())


def _get_abstract_dependency_closure(
    requirements: Iterable[LocationRequirement],
) -> frozenset[str]:
    abstract_names = frozenset(ABSTRACT_REQUIREMENTS)
    pending = [
        name
        for requirement in requirements
        for name in _iter_abstract_references_for_worklist(
            requirement,
            abstract_names,
        )
    ]
    dependencies: set[str] = set()
    while pending:
        name = pending.pop()
        if name in dependencies:
            continue
        dependencies.add(name)
        pending.extend(
            reference
            for requirement in ABSTRACT_REQUIREMENTS[name]
            for reference in _iter_abstract_references_for_worklist(
                requirement,
                abstract_names,
            )
        )
    return frozenset(dependencies)


def _get_dead_paths() -> frozenset[str]:
    referenced_names = {
        reference
        for requirement_group in _all_requirement_groups()
        for reference in _iter_named_references(requirement_group)
    }
    unused_paths = set(PATH_REQUIREMENTS) - referenced_names

    abstract_values = {name: False for name in ABSTRACT_REQUIREMENTS}
    changed = True
    while changed:
        changed = False
        for name, alternatives in ABSTRACT_REQUIREMENTS.items():
            if abstract_values[name]:
                continue
            if any(
                _satisfies_requirement_with_values(
                    alternative,
                    abstract_values,
                    lambda _name: True,
                    lambda _name: 1_000_000,
                    True,
                    True,
                    skips_tier=3,
                )
                for alternative in alternatives
            ):
                abstract_values[name] = True
                changed = True
    unreachable_paths = {
        name
        for name in PATH_REQUIREMENTS
        if not abstract_values[name]
    }
    return frozenset(unused_paths | unreachable_paths)


def _get_vanilla_reward_name(location_name: str) -> str:
    # Import locally because items.py imports this module to classify its
    # logic references. Validation runs after both modules are initialized.
    from .items import get_vanilla_reward_name
    from .locations import location_data_table

    try:
        category = location_data_table[location_name].category
        return get_vanilla_reward_name(location_name, category)
    except (KeyError, ValueError):
        return ''


def _get_location_self_dependencies(
    location_names: Iterable[str],
    item_names: Iterable[str],
    player: int = 1,
) -> frozenset[str]:
    # Import locally because items.py imports this module while constructing
    # classifications. A location holding one copy of a repeatable item is
    # not self-locked when another copy of that same item can satisfy its
    # requirement. Validation must remove one copy, not the entire identity.
    from .items import ITEM_POOL_COUNTS, REPEATED_CATEGORY_ITEM_COUNTS

    item_name_set = frozenset(item_names)
    maximum_item_counts = dict(ITEM_POOL_COUNTS)
    for category_counts in REPEATED_CATEGORY_ITEM_COUNTS.values():
        for item_name, count in category_counts.items():
            maximum_item_counts[item_name] = max(
                maximum_item_counts.get(item_name, 1),
                count,
            )

    class ValidationState:
        def __init__(self, missing_item: str | None):
            self.missing_item = missing_item
            self.missing_item_count = (
                0
                if missing_item is None
                else max(0, maximum_item_counts.get(missing_item, 1) - 1)
            )
            self._silksong_inventory_signature = (
                'validation',
                item_name_set,
                missing_item,
                self.missing_item_count,
            )

        def has(self, item_name: str, _player: int) -> bool:
            if item_name not in item_name_set:
                return False
            if item_name != self.missing_item:
                return True
            return self.missing_item_count > 0

        def count(self, item_name: str, _player: int) -> int:
            if item_name not in item_name_set:
                return 0
            if item_name != self.missing_item:
                return 1_000_000
            return self.missing_item_count

    full_inventory_state = ValidationState(None)
    missing_item_states: dict[str, ValidationState] = {}

    def missing_item_state(item_name: str) -> ValidationState:
        state = missing_item_states.get(item_name)
        if state is None:
            state = ValidationState(item_name)
            missing_item_states[item_name] = state
        return state

    logic_item_references = get_logic_item_references()
    dependencies = {
        f"{location_name} -> {reward_name}"
        for location_name in location_names
        if (
            location_name in REQUIREMENTS
            and location_name not in LOGIC_UNKNOWN_LOCATIONS
        )
        for reward_name in (_get_vanilla_reward_name(location_name),)
        if reward_name in logic_item_references
        for access_rule in (make_rule(location_name, player, skips_tier=3),)
        if (
            reward_name in item_name_set
            and access_rule(full_inventory_state)
            and not access_rule(missing_item_state(reward_name))
        )
    }
    return frozenset(dependencies)


def get_logic_item_references() -> frozenset[str]:
    """Return every real item that can affect a logic rule.

    Act and Path names live in the same requirement fields as items, so they
    are filtered out here. Crest and Silk Spear requirements are represented
    by flags and must be added explicitly.
    """
    all_requirements = tuple(
        requirement
        for requirement_groups in _all_requirement_groups()
        for requirement in requirement_groups
    ) + tuple(
        requirement
        for requirement_groups
        in RANDOMIZED_INNATE_CAPABILITY_REQUIREMENTS.values()
        for requirement in requirement_groups
    ) + get_trails_end_requirements(
        TRAILS_END_REQUIREMENT_OWNED_MAPS
    )
    references = {
        clean_item_display_name(name)
        for name in _iter_named_references(all_requirements)
        if name not in ABSTRACT_REQUIREMENTS
    }
    all_logic_item_dependencies = get_logic_item_dependencies(True, silk_heart_logic=True)
    references.update(
        dependency_name
        for item_name in tuple(references)
        for dependency_name in all_logic_item_dependencies.get(item_name, ())
    )
    if any(requirement.require_any_crest for requirement in all_requirements):
        references.update(CREST_ITEMS)
    if any(requirement.require_silk_spear for requirement in all_requirements):
        references.add('Silkspear')
    return frozenset(references)


_REQUIREMENTS_VALIDATION_CACHE_LIMIT = 8
_REQUIREMENTS_VALIDATION_CACHE: OrderedDict[tuple[object, ...], None] = (
    OrderedDict()
)


def _requirements_validation_signature(
    location_names: frozenset[str],
    item_names: frozenset[str],
    progression_item_names: frozenset[str] | None,
) -> tuple[object, ...]:
    from .items import ITEM_POOL_COUNTS

    return (
        location_names,
        item_names,
        progression_item_names,
        tuple(REQUIREMENTS.items()),
        tuple(ABSTRACT_REQUIREMENTS.items()),
        tuple(RANDOMIZED_INNATE_CAPABILITY_REQUIREMENTS.items()),
        tuple(PATH_REQUIREMENTS.items()),
        PATH_ORDER,
        LOGIC_UNKNOWN_LOCATIONS,
        ALLOWED_DEAD_PATHS,
        tuple(sorted(ITEM_POOL_COUNTS.items())),
        tuple(sorted(get_logic_item_dependencies(True, silk_heart_logic=True).items())),
        CREST_ITEMS,
        OPTION_DEPENDENT_PROGRESSION_ITEM_NAMES,
        get_trails_end_requirements(TRAILS_END_REQUIREMENT_OWNED_MAPS),
        FINAL_GOAL_EVENT,
        tuple(sorted(
            (location_name, _get_vanilla_reward_name(location_name))
            for location_name in location_names
        )),
    )


def validate_requirements(
    location_names: Iterable[str],
    item_names: Iterable[str],
    progression_item_names: Iterable[str] | None = None,
    *,
    check_vanilla_self_locks: bool = True,
) -> None:
    location_name_set = frozenset(location_names)
    item_name_set = frozenset(item_names) | WISH_LOGIC_EVENT_ITEM_NAMES
    progression_item_name_set = (
        None
        if progression_item_names is None
        else (
            frozenset(progression_item_names)
            | WISH_LOGIC_EVENT_ITEM_NAMES
        )
    )
    validation_signature = _requirements_validation_signature(
        location_name_set,
        item_name_set,
        progression_item_name_set,
    ) + (check_vanilla_self_locks,)
    if validation_signature in _REQUIREMENTS_VALIDATION_CACHE:
        _REQUIREMENTS_VALIDATION_CACHE.move_to_end(validation_signature)
        return

    requirement_location_names = set(REQUIREMENTS)
    logic_item_references = get_logic_item_references()
    path_order_names = tuple(f"Path: {name}" for name in PATH_ORDER)

    missing_locations = (
        location_name_set
        - requirement_location_names
        - LOGIC_UNKNOWN_LOCATIONS
    )
    extra_locations = requirement_location_names - location_name_set
    unknown_items = logic_item_references - item_name_set
    missing_paths_from_order = set(PATH_REQUIREMENTS) - set(path_order_names)
    extra_paths_in_order = set(path_order_names) - set(PATH_REQUIREMENTS)
    duplicate_paths_in_order = {
        name
        for name in path_order_names
        if path_order_names.count(name) > 1
    }
    direct_self_dependencies = {
        requirement_name
        for requirement_name, alternatives in ABSTRACT_REQUIREMENTS.items()
        if any(
            requirement_name in (*alternative.all_of, *alternative.any_of)
            for alternative in alternatives
        )
    }
    location_self_dependencies = (
        _get_location_self_dependencies(location_name_set, item_name_set)
        if check_vanilla_self_locks
        else frozenset()
    )
    dead_paths = frozenset() if MAPPER_GRAPH_ENABLED else _get_dead_paths()
    unexpected_dead_paths = frozenset() if MAPPER_GRAPH_ENABLED else dead_paths - ALLOWED_DEAD_PATHS
    stale_dead_path_allowlist = frozenset() if MAPPER_GRAPH_ENABLED else ALLOWED_DEAD_PATHS - dead_paths
    unknown_quarantined_locations = (
        LOGIC_UNKNOWN_LOCATIONS - location_name_set
    )
    unknown_required_locations = {
        location_name
        for alternatives in (
            *REQUIREMENTS.values(),
            *ABSTRACT_REQUIREMENTS.values(),
        )
        for alternative in alternatives
        for location_name in alternative.required_locations
        if location_name not in requirement_location_names
    }
    invalid_item_counts = {
        f"{owner}:{count_requirement.minimum}:{','.join(count_requirement.item_names)}"
        for owner, alternatives in (
            *REQUIREMENTS.items(),
            *ABSTRACT_REQUIREMENTS.items(),
        )
        for alternative in alternatives
        for count_requirement in alternative.item_counts
        if (
            count_requirement.minimum < 1
            or not count_requirement.item_names
            or len(count_requirement.item_names)
            != len(set(count_requirement.item_names))
        )
    }
    goal_dependencies = (
        _get_abstract_dependency_closure(REQUIREMENTS["Goal"])
        if "Goal" in REQUIREMENTS
        else frozenset()
    )
    missing_goal_dependencies = (
        {'Act: 3', FINAL_GOAL_EVENT} - goal_dependencies
    )
    goal_direct_references = (
        set(_iter_named_references(REQUIREMENTS["Goal"]))
        if "Goal" in REQUIREMENTS
        else set()
    )
    missing_direct_goal_event = (
        set()
        if FINAL_GOAL_EVENT in goal_direct_references
        else {FINAL_GOAL_EVENT}
    )
    non_progression_logic_items: set[str] = set()
    if progression_item_name_set is not None:
        non_progression_logic_items = (
            logic_item_references
            & item_name_set
            - progression_item_name_set
            - OPTION_DEPENDENT_PROGRESSION_ITEM_NAMES
        )

    if (
        missing_locations
        or extra_locations
        or unknown_items
        or non_progression_logic_items
        or missing_paths_from_order
        or extra_paths_in_order
        or duplicate_paths_in_order
        or direct_self_dependencies
        or location_self_dependencies
        or unexpected_dead_paths
        or stale_dead_path_allowlist
        or unknown_quarantined_locations
        or unknown_required_locations
        or invalid_item_counts
        or missing_goal_dependencies
        or missing_direct_goal_event
    ):
        raise ValueError(
            "Invalid Silksong requirement table: "
            f"missing_locations={sorted(missing_locations)}, "
            f"extra_locations={sorted(extra_locations)}, "
            f"unknown_items={sorted(unknown_items)}, "
            f"non_progression_logic_items={sorted(non_progression_logic_items)}, "
            f"missing_paths_from_order={sorted(missing_paths_from_order)}, "
            f"extra_paths_in_order={sorted(extra_paths_in_order)}, "
            f"duplicate_paths_in_order={sorted(duplicate_paths_in_order)}, "
            f"direct_self_dependencies={sorted(direct_self_dependencies)}, "
            f"location_self_dependencies={sorted(location_self_dependencies)}, "
            f"unexpected_dead_paths={sorted(unexpected_dead_paths)}, "
            f"stale_dead_path_allowlist={sorted(stale_dead_path_allowlist)}, "
            f"unknown_quarantined_locations={sorted(unknown_quarantined_locations)}, "
            f"unknown_required_locations={sorted(unknown_required_locations)}, "
            f"invalid_item_counts={sorted(invalid_item_counts)}, "
            f"missing_goal_dependencies={sorted(missing_goal_dependencies)}, "
            f"missing_direct_goal_event={sorted(missing_direct_goal_event)}"
        )

    _REQUIREMENTS_VALIDATION_CACHE[validation_signature] = None
    _REQUIREMENTS_VALIDATION_CACHE.move_to_end(validation_signature)
    while (
        len(_REQUIREMENTS_VALIDATION_CACHE)
        > _REQUIREMENTS_VALIDATION_CACHE_LIMIT
    ):
        _REQUIREMENTS_VALIDATION_CACHE.popitem(last=False)
