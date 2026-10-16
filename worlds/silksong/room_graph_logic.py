from __future__ import annotations

import json
import pkgutil

from dataclasses import dataclass, replace
from functools import lru_cache
from itertools import product
from types import MappingProxyType
from typing import Iterable, Mapping

from .combat import requirement_name as combat_requirement_name

from .room_graph import (
    LogicStatus,
    RequirementMode,
    RequirementSpec,
    load_room_graph,
)


ROOM_NODE_PREFIX = "Room Node: "
ROOM_EVENT_PREFIX = "Room Event: "
SPOOL_FRAGMENT_COUNT_ITEM = "__room_graph_spool_fragments__"


@dataclass(frozen=True)
class CompiledRoomClause:
    """One monotonic Archipelago requirement alternative."""

    all_of: tuple[str, ...] = ()
    item_counts: tuple[tuple[str, int], ...] = ()
    require_silk_spear: bool = False
    minimum_skip_tier: int = 0
    silk_cost: int = 0


@dataclass(frozen=True)
class CompiledRoomGraph:
    node_requirements: Mapping[str, tuple[CompiledRoomClause, ...]]
    event_requirements: Mapping[str, tuple[CompiledRoomClause, ...]]
    check_requirements: Mapping[str, tuple[CompiledRoomClause, ...]]
    check_source_ids: Mapping[str, tuple[str, ...]]
    authoritative_check_names: frozenset[str]
    quarantined_check_names: frozenset[str]
    structurally_reachable_nodes: frozenset[str]
    semantically_reachable_nodes: frozenset[str]
    skipped_check_ids: tuple[str, ...]


def room_node_name(node_id: str) -> str:
    return ROOM_NODE_PREFIX + node_id


def room_event_name(event_id: str) -> str:
    return ROOM_EVENT_PREFIX + event_id


@dataclass(frozen=True)
class RoomEventIdentity:
    name: str
    kind: str
    locations: tuple[str, ...]


@lru_cache(maxsize=1)
def room_event_catalog() -> Mapping[str, RoomEventIdentity]:
    rows = json.loads(pkgutil.get_data(__package__, "room_event_names.json"))
    if not isinstance(rows, dict):
        raise ValueError("Room event catalog must map event IDs to identities.")
    entries = {}
    for event_id, row in rows.items():
        if (not isinstance(event_id, str) or not isinstance(row, dict)
                or not isinstance(row.get("name"), str)
                or not row["name"].strip() or row["name"] != row["name"].strip()
                or not isinstance(row.get("kind"), str)
                or not isinstance(row.get("locations"), list)
                or any(not isinstance(name, str) or not name.strip()
                       for name in row["locations"])):
            raise ValueError(f"Invalid room event identity: {event_id}")
        entries[event_id] = RoomEventIdentity(row["name"], row["kind"], tuple(row["locations"]))
    if len({entry.name.casefold() for entry in entries.values()}) != len(entries):
        raise ValueError("Room event display names must be unique.")
    for room in load_room_graph().rooms:
        for event in room.events:
            if event.id not in entries:
                raise ValueError(f"Room event needs an identity: {event.id}")
            identity = entries[event.id]
            mapper_id = event.raw_cells.get("mapper_id")
            locations = tuple(sorted({
                check.canonical_location for check in room.checks
                if mapper_id and check.raw_cells.get("mapper_id") == mapper_id
                and check.canonical_location
            }))
            mapper_kind = rows[event.id].get("mapper_kind", identity.kind)
            if (mapper_kind != event.kind or identity.locations != locations
                    or (identity.kind != mapper_kind and mapper_kind != "unknown")):
                raise ValueError(f"Room event identity is out of date: {event.id}")
            if len(locations) == 1 and identity.name != locations[0]:
                raise ValueError(f"Room event must use its existing location name: {event.id}")
    return MappingProxyType(entries)


@lru_cache(maxsize=1)
def room_event_action_names() -> Mapping[str, str]:
    return MappingProxyType({
        event_id: identity.name for event_id, identity in room_event_catalog().items()
        if identity.kind in {"switch", "blockade"} and not identity.locations
    })


def room_event_action_name(event_id: str) -> str:
    return room_event_action_names()[event_id]


@lru_cache(maxsize=1)
def room_event_display_names() -> Mapping[str, str]:
    return MappingProxyType({
        room_event_name(event_id): ROOM_EVENT_PREFIX + identity.name
        for event_id, identity in room_event_catalog().items()
    })


def native_region_name(requirement_name: str) -> str:
    if not requirement_name.startswith(ROOM_EVENT_PREFIX):
        return requirement_name
    return room_event_display_names().get(requirement_name, requirement_name)


def _part(
    *all_of: str,
    item_counts: Iterable[tuple[str, int]] = (),
    silk_spear: bool = False,
    skip_tier: int = 0,
) -> CompiledRoomClause:
    return CompiledRoomClause(
        all_of=tuple(all_of),
        item_counts=tuple(item_counts),
        require_silk_spear=silk_spear,
        minimum_skip_tier=skip_tier,
    )


_ATOM_ALTERNATIVES: Mapping[str, tuple[CompiledRoomClause, ...]] = {
    "item:architect-crest": (_part("Crest: Architect"),),
    "item:architects-key": (_part("Architect's Key"),),
    "item:beast-crest": (_part("Crest: Beast"),),
    "item:bell-shellwood": (_part("Bell: Shellwood"),),
    "item:bellway-blasted-steps": (_part("Bellway: Blasted Steps"),),
    "item:bellway-bilewater": (_part("Bellway: Bilewater"),),
    "item:bellway-bellhart": (_part("Bellway: Bellhart"),),
    "item:bellway-far-fields": (_part("Bellway: Far Fields"),),
    "item:bellway-putrified-ducts": (_part("Bellway: Putrified Ducts"),),
    "item:bellway-shellwood": (_part("Bellway: Shellwood"),),
    "item:bellway-the-slab": (_part("Bellway: The Slab"),),
    "item:clawline": (_part("Ancestral Art: Clawline"),),
    "item:cling-grip": (_part("Ancestral Art: Cling Grip"),),
    "item:craftmetal": (_part("Craftmetal"),),
    "item:drifters-cloak": (_part("Ability: Drifter's Cloak"),),
    "item:faydown-cloak": (_part("Ability: Faydown Cloak"),),
    "item:flea-brew": (_part("Usable Flea Brew"),),
    # "Filled needle phial" is the state of the original Needle Phial used
    # to finish the Plasmium quest.  Plasmium Phial is the reward, so mapping
    # this atom to it would put that reward behind itself.
    "item:filled-needle-phial": (_part("Usable Needle Phial"),),
    "item:hunter-crest": (_part("Crest: Hunter"),),
    "item:needle-phial": (_part("Usable Needle Phial"),),
    "item:needle-strike": (_part("Ability: Needle Strike"),),
    "item:needolin": (_part("Ancestral Art: Needolin"),),
    "item:key-of-apostate": (_part("Key of Apostate"),),
    "item:ruined-tool": (_part("Ruined Tool"),),
    "item:reaper-crest": (_part("Crest: Reaper"),),
    "item:rune-rage": (_part("Usable Rune Rage"),),
    "item:shaman-crest": (_part("Crest: Shaman"),),
    # Sharpdart must be usable, not merely received. The existing abstract
    # requirement excludes Architect and accepts every crest with a Silk Skill
    # slot.
    "item:sharpdart": (_part("Usable Sharpdart"),),
    "item:silk-soar": (_part("Ancestral Art: Silk Soar"),),
    "item:silk-spear": (_part(silk_spear=True),),
    "item:simple-key": (_part("Simple Key (Wormways)"),),
    "item:deep-docks-key": (_part("Simple Key (Deep Docks)"),),
    "item:thread-storm": (_part("Usable Thread Storm"),),
    "item:wanderer-crest": (_part("Crest: Wanderer"),),
    "item:witch-crest": (_part("Crest: Witch"),),
    "item:white-key": (_part("White Key"),),
    "path:bellways": (_part("Path: Bellways"),),
    "path:bilewater-twisted-bud": (
        _part("Twisted Bud"),
    ),
    "macro:progressive-swift-step-first": (
        _part("Swift Step"),
        _part("Progressive Swift Step"),
    ),
    "macro:progressive-swift-step-full": (_part("Swift Step"),),
    # Confirmed graph vocabulary: any one of Sharpdart, full Dash or
    # Clawline is horizontal movement tech. Sprint alone is not.
    "macro:horizontal-movement-tech": (
        _part("Usable Sharpdart"),
        _part("Swift Step"),
        _part("Ancestral Art: Clawline"),
    ),
    "macro:any-crest": (
        _part("Crest: Hunter"),
        _part("Crest: Reaper"),
        _part("Crest: Shaman"),
        _part("Crest: Architect"),
        _part("Crest: Wanderer"),
        _part("Crest: Beast"),
        _part("Crest: Witch"),
    ),
    # Spike Pogo needs an owned Crest; skip difficulty is checked separately.
    "macro:spike-pogo": (
        _part("Crest: Hunter"),
        _part("Crest: Reaper"),
        _part("Crest: Shaman"),
        _part("Crest: Architect"),
        _part("Crest: Wanderer"),
        _part("Crest: Beast"),
        _part("Crest: Witch"),
    ),
    "macro:crest-pogo": (
        _part("Crest: Hunter", "Technique: Crest Pogo 1"),
        _part("Crest: Reaper", "Technique: Crest Pogo 1"),
        _part("Crest: Shaman", "Technique: Crest Pogo 1"),
        _part("Crest: Architect", "Technique: Crest Pogo 1"),
        _part("Crest: Wanderer", "Technique: Crest Pogo 1"),
        _part("Crest: Beast", "Technique: Crest Pogo 1"),
        _part("Crest: Witch", "Technique: Crest Pogo 1"),
    ),
    "macro:architect-charge": (
        _part("Ability: Needle Strike", "Crest: Architect"),
    ),
    "macro:beast-charge": (
        _part("Ability: Needle Strike", "Crest: Beast"),
    ),
    "macro:hunter-charge": (
        _part("Ability: Needle Strike", "Crest: Hunter"),
    ),
    "macro:reaper-charge": (
        _part("Ability: Needle Strike", "Crest: Reaper"),
    ),
    "macro:shaman-charge": (
        _part("Ability: Needle Strike", "Crest: Shaman"),
    ),
    "macro:wanderer-charge": (
        _part("Ability: Needle Strike", "Crest: Wanderer"),
    ),
    "macro:witch-charge": (
        _part("Ability: Needle Strike", "Crest: Witch"),
    ),
    "macro:blasted-crest-pogo": (
        _part("Crest: Hunter", "Technique: Crest Pogo 1"),
        _part("Crest: Reaper", "Technique: Crest Pogo 1"),
        _part("Crest: Shaman", "Technique: Crest Pogo 1"),
        _part("Crest: Architect", "Technique: Crest Pogo 1"),
        _part("Crest: Beast", "Technique: Crest Pogo 1"),
    ),
    "macro:blasted-proficient-beast": (
        _part("Crest: Beast", skip_tier=1),
    ),
    "macro:blasted-easy-flea-brew-stall": (
        _part("Usable Flea Brew", "Technique: Flea Brew Stall 1"),
    ),
    "macro:blasted-flea-brew-stall": (
        _part("Usable Flea Brew", "Technique: Flea Brew Stall 3"),
    ),
    "macro:blasted-easy-heal-stall": (_part("Technique: Heal Stall 1"),),
    "macro:blasted-heal-stall": (_part("Technique: Heal Stall 3"),),
    "macro:any-non-hunter-crest": (
        _part("Crest: Reaper", "Technique: Crest Pogo 1"),
        _part("Crest: Shaman", "Technique: Crest Pogo 1"),
        _part("Crest: Architect", "Technique: Crest Pogo 1"),
        _part("Crest: Wanderer", "Technique: Crest Pogo 1"),
        _part("Crest: Beast", "Technique: Crest Pogo 1"),
        _part("Crest: Witch", "Technique: Crest Pogo 1"),
    ),
    "macro:any-non-witch-crest": (
        _part("Crest: Hunter"),
        _part("Crest: Reaper"),
        _part("Crest: Shaman"),
        _part("Crest: Architect"),
        _part("Crest: Wanderer"),
        _part("Crest: Beast"),
    ),
    # The Magma Bell must be equippable on an owned crest.  This abstract
    # requirement accounts for native Blue slots and randomized slot upgrades.
    "macro:usable-magma-bell": (_part("Usable Magma Bell"),),
    # Every mapped Scuttlebrace route is the full-speed crawl technique, so
    # merely owning/equipping the tool is insufficient. It also needs the full
    # Swift Step upgrade, never only the first progressive stage.
    "macro:usable-scuttlebrace": (
        _part("Usable Scuttlebrace", "Swift Step", "Technique: Scuttlebrace 1"),
    ),
    "macro:usable-curveclaw": tuple(
        _part("Progressive Curveclaw", crest)
        for crest in (
            "Crest: Hunter",
            "Crest: Reaper",
            "Crest: Architect",
            "Crest: Wanderer",
            "Crest: Beast",
            "Crest: Witch",
        )
    ),
    "macro:damage-searing": (_part("Damage: Searing"),),
    "macro:damage-shredding": (_part("Damage: Shredding"),),
    "macro:damage-skewering": (_part("Damage: Skewering"),),
    "macro:steel-soul-resting-sites": (_part("Event: Selected Steel Soul Resting Sites Visited"),),
    "macro:any-map": (_part("Capability: Has Any Map"),),
    "state:steel-soul-on": (_part("Option: Steel Soul On"),),
    "state:steel-soul-off": (_part("Option: Steel Soul Off"),),
    "state:bellshrinesanity-on": (_part("Option: Bellshrinesanity On"),),
    "state:bellshrinesanity-off": (_part("Option: Bellshrinesanity Off"),),
    "option:proficient-combat": (_part("Option: Proficient Combat"),),
    "option:skips-easy": (_part(skip_tier=1),),
    "option:skips-moderate": (_part(skip_tier=2),),
    "option:skips-difficult": (_part(skip_tier=3),),
    # Bell Beast's silk remains an explicit Silkspear-only gate.
    "capability:break-silk-blockade": (
        _part("Event: Ordinary Silk Blockades Cleared"),
        _part(silk_spear=True),
        _part("Usable Rune Rage"),
        _part("Usable Sharpdart"),
    ),
    # These describe ordinary environmental interactions, not inventory.
    "capability:break-vines": (_part(),),
    "capability:break-walls": (_part(),),
    "capability:free": (_part(),),
    "capability:ledge-grab": (_part("Capability: Ledge Grab"),),
    "capability:swim": (_part("Capability: Swim"),),
    # The client keeps the randomized Wanderer chapel door open, making its
    # monotonic override a free capability in AP logic.
    "capability:wanderer-door-override": (_part(),),
    "state:act-1": (_part("Act: 1"),),
    "state:act-3": (_part("Act: 3"),),
}


# Requirement phrases that refer to action rows. The action itself is reached
# through its node. It is not an AP check.
_ACTION_EVENT_ID_BY_ATOM: Mapping[str, str] = {
    "event:bone-bottom/mosshome-lower/middle-floor-switch-opened":
        "event:bone-bottom/mosshome-middle/flip-switch-to-open-floor-exit",
    "event:bone-bottom/mosshome-lower/spool-ceiling-switch-opened":
        "event:bone-bottom/mosshome-spool/floor-switch-to-open-ceiling-exit",
    "event:bone-bottom/bone-bottom-town/elevator-switch-flipped":
        "event:bone-bottom/bone-bottom-town/elevator-switch",
    "event:bone-bottom/mosshome-middle/flip-the-switch-in-this-area":
        "event:bone-bottom/mosshome-middle/flip-switch-to-open-floor-exit",
    "event:bone-bottom/mosshome-spool/switch-in-room-activated":
        "event:bone-bottom/mosshome-spool/floor-switch-to-open-ceiling-exit",
    "event:the-marrow/the-marrow-entrance/platform-lowered":
        "event:the-marrow/the-marrow-shakra-intro/lower-platform-switch-into-floor",
    "event:the-marrow/the-marrow-bellshrine/bell-must-be-rung":
        "event:the-marrow/the-marrow-bellshrine/ring-bell-switch",
    "event:the-marrow/the-marrow-jail-pathway/platform-switch-activated":
        "event:the-marrow/the-marrow-jail-pathway/platform-switch",
    "event:the-marrow/the-marrow-shaft/bell-must-be-rung":
        "event:the-marrow/the-marrow-bellshrine/ring-bell-switch",
    "event:the-marrow/the-marrow-shakra-intro/lowers-platform-into-the-marrow-entrance":
        "event:the-marrow/the-marrow-shakra-intro/lower-platform-switch-into-floor",
    "event:the-marrow/the-marrow-lava-track/activate-track":
        "event:the-marrow/the-marrow-lava-track/activate-track",
    "event:weavenest-atla/weavenest-atla-teleporter/weavenest-atla-power-activation":
        "event:weavenest-atla/weavenest-atla-power/weavenest-atla-power-activation",
    "event:weavenest-atla/weavenest-atla-grotto/defeat-double-moss-mother":
        "event:weavenest-atla/weavenest-atla-grotto/double-moss-mother-boss-fight",
    "event:wormways/wormways-middle/door-must-be-unlocked-from-the-other-side":
        "event:wormways/wormways-shaft/use-simple-key-on-lock",
    "event:wormways/wormways-shaft/door-unlocked":
        "event:wormways/wormways-shaft/use-simple-key-on-lock",
    "event:wormways/wormways-shaft/door-switch-needs-to-be-flipped":
        "event:wormways/wormways-shaft/flip-door-switch",
    "event:deep-docks/deep-docks-bellshrine/deep-docks-bellshrine-activated":
        "event:deep-docks/deep-docks-bellshrine/activate-deep-docks-bellshrine-switch",
    "event:deep-docks/deep-docks-bench-shaft/gate-unlocked-from-other-side":
        "event:deep-docks/deep-docks-upper-spire/door-switch",
    "event:deep-docks/deep-docks-chains-center/ceiling-switch-activated":
        "event:deep-docks/deep-docks-chains-center/ceiling-switch",
    "event:deep-docks/deep-docks-chains-center/door-switch-flipped":
        "event:deep-docks/deep-docks-chains-center/door-switch",
    "event:deep-docks/deep-docks-entrance/switch-flipped":
        "event:deep-docks/deep-docks-entrance/door-switch",
    "event:deep-docks/deep-docks-lace-intro/gate-switch-flipped":
        "event:deep-docks/deep-docks-lace-intro/gate-switch",
    "event:deep-docks/deep-docks-spool-east/platforms-lowered":
        "event:deep-docks/deep-docks-spool-east/platform-lever",
    "event:deep-docks/deep-docks-magma-slug-tunnels/left-door-switch-flipped":
        "event:deep-docks/deep-docks-magma-slug-tunnels/left-door-switch",
    (
        "event:whispering-vaults/grand-bellway-library/"
        "flick-the-first-lever"
    ): (
        "event:whispering-vaults/grand-bellway-library/"
        "whispering-vaults-flip-switch-6-left"
    ),
    (
        "event:whispering-vaults/vaultkeeper-cauldron-entrance/"
        "open-door-from-right-side-switch-1"
    ): (
        "event:whispering-vaults/vaultkeeper-cauldron-entrance/"
        "whispering-vaults-flip-switch-1-down"
    ),
    (
        "event:deep-docks/deep-docks-magma-slug-tunnels/"
        "right-door-switch-must-be-flipped"
    ):
        "event:deep-docks/deep-docks-magma-slug-tunnels/right-door-switch",
    "event:far-fields/far-fields-deep-docks-loopback/gate-switch-flipped":
        "event:far-fields/far-fields-deep-docks-loopback/gate-switch",
    "event:far-fields/far-fields-deep-lower-west/door-switch-activated":
        "event:far-fields/far-fields-deep-lower-west/door-switch",
    "event:far-fields/far-fields-entrance-east/deep-docks-bellshrine-activated":
        "event:deep-docks/deep-docks-bellshrine/activate-deep-docks-bellshrine-switch",
    "event:hunter-s-march/chapel-of-the-beast/door-switch-flipped":
        "event:hunter-s-march/chapel-of-the-beast/door-switch",
    "event:hunter-s-march/hunter-s-march-deep-docks-passage/defeat-gauntlet":
        "event:hunter-s-march/hunter-s-march-deep-docks-passage/gauntlet-fight",
    "event:hunter-s-march/hunter-s-march-map-shop/defeat-gauntlet":
        "event:hunter-s-march/hunter-s-march-map-shop/gauntlet-fight",
}


# Persistent actions inferred from the controlling side.
# Every entry is monotonic: once that node is reachable, the player can perform
# the action and retain the shortcut/state for the rest of the logic search.
_IMPLICIT_EVENT_SOURCE: Mapping[str, tuple[CompiledRoomClause, ...]] = {
    "event:grand-gate/entrance-to-nyleth/vines-in-door-broken": (
        _part(room_node_name("grand-gate/entrance-to-nyleth#entrance")),
    ),
    (
        "event:putrified-ducts/putrified-ducts-bellway/"
        "breakable-floor-broken-from-vog-camp"
    ): (
        _part(
            room_node_name(
                "putrified-ducts/putrified-ducts-bellway#vog-camp"
            )
        ),
    ),
    "event:sinner-s-road/sinner-s-road-styx-room/left-right-wall-broken": (
        _part(room_node_name("sinner-s-road/sinner-s-road-styx-room#left")),
    ),
    "event:sinner-s-road/sinner-s-road-styx-room/cage-right-wall-broken": (
        _part(room_node_name("sinner-s-road/sinner-s-road-styx-room#cage")),
    ),
    "event:bone-bottom/bone-bottom-town/door-opened-from-other-side": (
        _part(room_node_name("bone-bottom/bonegrave#graveyard")),
    ),
    "event:bone-bottom/bonegrave/wall-broken-from-other-side": (
        _part(room_node_name("bone-bottom/bonegrave#upper-left-exit")),
    ),
    # The Mosshome Upper row identifies the side from which this one-way wall
    # is broken. Once its main area is reachable, the Big Fall
    # middle-right entrance remains open permanently.
    (
        "event:bone-bottom/the-big-fall/"
        "breakable-wall-must-be-opened-from-the-other-side"
    ): (
        _part(room_node_name("bone-bottom/mosshome-upper#main-area")),
    ),
    "event:moss-grotto/ruined-chapel/moss-mother-defeated": (
        _part(room_node_name("moss-grotto/ruined-chapel#boss-room")),
    ),
    # This blocker disappears after leaving Moss Grotto. Reaching Bone Bottom
    # ground level confirms the departure without making the ceiling exit a
    # start route.
    (
        "event:moss-grotto/moss-grotto-center/"
        "has-loading-zone-blocker-until-you-first-leave-moss-grotto"
    ): (
        _part(room_node_name("bone-bottom/bone-bottom-town#ground-level")),
    ),
    "event:the-marrow/the-marrow-bellway/bell-beast-defeated": (
        _part(
            room_node_name("the-marrow/the-marrow-bellway#boss-room"),
            silk_spear=True,
        ),
    ),
    "event:the-marrow/the-marrow-entrance/defeat-gauntlet": (
        _part(room_node_name("the-marrow/the-marrow-entrance#gauntlet-room")),
    ),
    "event:the-marrow/the-marrow-entrance/flipped-door-switch": (
        _part(room_node_name("the-marrow/the-marrow-entrance#after-gauntlet")),
    ),
    "event:the-marrow/the-marrow-flea-caravan/door-switch-activated": (
        _part(room_node_name("the-marrow/the-marrow-flea-caravan#behind-metal-gate")),
    ),
    "event:the-marrow/the-marrow-shaft/door-switch-flipped": (
        _part(room_node_name("the-marrow/the-marrow-shaft#upper-shaft")),
    ),
    "event:the-marrow/the-marrow-shakra-intro/door-switch-flipped": (
        _part(room_node_name("the-marrow/the-marrow-shakra-intro#behind-gate")),
    ),
    "event:the-marrow/the-marrow-skull-tyrant-arena/defeat-skull-tyrant": (
        _part(room_node_name("the-marrow/the-marrow-skull-tyrant-arena#room")),
    ),
    "event:wormways/wormways-craggler-hallway/defeat-craggler": (
        _part(room_node_name("wormways/wormways-craggler-hallway#room")),
    ),
    "event:wormways/wormways-shaft/breakable-wall-must-be-opened-from-the-other-side": (
        _part(room_node_name("wormways/wormways-upper-west#main-area")),
    ),
    "event:deep-docks/deep-docks-chains-center/wall-opened-from-lower-east": (
        _part(room_node_name("deep-docks/deep-docks-chains-lower-east#lower-lava-platform")),
    ),
    "event:deep-docks/deep-docks-chains-upper-east/door-opened-from-the-other-side": (
        _part(room_node_name("deep-docks/deep-docks-chains-upper-east#upper-left-hallway")),
    ),
    "event:deep-docks/deep-docks-chains-upper-east/wall-broken": (
        _part(room_node_name("deep-docks/deep-docks-chains-upper-east#chain-platforms")),
    ),
    "event:deep-docks/deep-docks-chains-upper-east/gate-opened-from-the-other-side": (
        _part(
            room_node_name("deep-docks/deep-docks-chains-upper-east#chain-platforms"),
            "Ancestral Art: Clawline",
        ),
    ),
    "event:deep-docks/deep-docks-entrance/defeat-gauntlet": (
        _part(room_node_name("deep-docks/deep-docks-entrance#gauntlet")),
    ),
    "event:deep-docks/deep-docks-forebrothers/defeat-forebrothers": (
        _part(room_node_name("deep-docks/deep-docks-forebrothers#boss-area")),
    ),
    "event:deep-docks/deep-docks-forge/gauntlet-defeated": (
        _part(room_node_name("deep-docks/deep-docks-forge#gauntlet")),
    ),
    "event:deep-docks/deep-docks-forge/open-airlock-up": (
        _part(room_node_name("deep-docks/deep-docks-forge#gauntlet")),
    ),
    "event:deep-docks/deep-docks-forge/open-airlock-down": (
        _part(room_node_name("deep-docks/deep-docks-forge#forge-daughter")),
    ),
    # The reverse route says the Forge-side crossing is free
    # and activates the airlock.  This is the same state Lace requires from
    # the opposite direction and is unrelated to the spool-room airlock.
    "event:deep-docks/deep-docks-lace-intro/airlock-lever": (
        _part(room_node_name("deep-docks/deep-docks-forge#left-area")),
    ),
    "event:deep-docks/deep-docks-forge/activate-airlock": (
        _part(room_node_name("deep-docks/deep-docks-forge#left-area")),
    ),
    "event:deep-docks/deep-docks-forge/gate-switch-activated": (
        _part(room_node_name("deep-docks/deep-docks-forge#right-area")),
    ),
    "event:deep-docks/deep-docks-lace-intro/defeat-lace": (
        _part(room_node_name("deep-docks/deep-docks-lace-intro#boss-arena")),
    ),
    (
        "event:deep-docks/deep-docks-lower-west-shaft/"
        "must-be-opened-from-the-other-side-for-the-first-time"
    ): (
        _part(room_node_name("deep-docks/deep-docks-sauna#room")),
    ),
    "event:deep-docks/is-this-still-deep-docks-east/wall-must-be-destroyed-from-the-other-side": (
        _part(room_node_name("deep-docks/is-this-still-deep-docks-west#ground")),
    ),
    "event:deep-docks/is-this-still-deep-docks-east/floor-must-be-destroyed-from-the-other-side": (
        _part(room_node_name("deep-docks/deep-docks-spire-lower#room")),
    ),
    "event:deep-docks/deep-docks-map-shop/flip-switch-to-lower-platform": (
        _part(room_node_name("deep-docks/deep-docks-map-shop#lower-area")),
    ),
    "event:deep-docks/deep-docks-chains-lower-east/open-airlock-door": (
        _part(
            room_node_name(
                "deep-docks/deep-docks-chains-lower-east#spool-fragment-area"
            )
        ),
    ),
    # The Underworks lift door is opened from the Broken Elevator side.
    "event:underworks/underworks-shaft/must-be-opened-from-the-other-side": (
        _part(room_node_name("underworks/broken-elevator#room")),
    ),
    # Entering the west arena clears its gauntlet state and reopens the return
    # route.
    "event:underworks/underworks-western-gauntlet/gauntlet": (
        _part(room_node_name("underworks/underworks-western-gauntlet#room")),
    ),
    "event:underworks/underworks-east-shaft/switch-3-flipped": (
        _part(
            room_node_name(
                "underworks/underworks-east-shaft#mid-right-entrance"
            )
        ),
    ),
    "event:underworks/underworks-eastern-gauntlet/lever-1-flipped": (
        _part(
            room_node_name(
                "underworks/underworks-eastern-gauntlet#arena"
            )
        ),
    ),
    # Clearing the Arena makes the fixed Heretic Key available.
    "event:the-slab/slab-arena/gauntlet": (
        _part(room_node_name("the-slab/slab-arena#arena")),
    ),
    # Each shortcut keeps its own one-way unlock.
    "event:the-slab/slab-cell/entrance-door-opened": (
        _part(room_node_name("the-slab/slab-entrance#room")),
    ),
    "event:the-slab/slab-cell/poodle-wall-opened": (
        _part(room_node_name("the-slab/slab-poodle#room")),
    ),
    "event:the-slab/slab-cell/secret-side-wall-opened": (
        _part(room_node_name("the-slab/slab-secret-side-room#bottom")),
    ),
    # The east-to-west room is the controlling side of this one-way door.
    (
        "event:choral-chambers/choral-chambers-eastern-shaft/"
        "door-should-be-opened-from-the-other-side"
    ): (
        _part(
            room_node_name(
                "choral-chambers/choral-chambers-east-to-west#left-side"
            )
        ),
    ),
    # The Spa side breaks the wall into the lower Flea Shaft.
    (
        "event:choral-chambers/choral-chambers-flea-shaft/"
        "breakable-wall-must-be-opened-from-the-other-side"
    ): (
        _part(
            room_node_name("choral-chambers/choral-chambers-spa#spa"),
            "Ancestral Art: Cling Grip",
        ),
        _part(
            room_node_name("choral-chambers/choral-chambers-spa#spa"),
            "Ancestral Art: Silk Soar",
        ),
        _part(
            room_node_name("choral-chambers/choral-chambers-spa#spa"),
            "Ability: Faydown Cloak",
        ),
    ),
    # This shortcut is opened while approaching from Underworks.
    (
        "event:choral-chambers/choral-chambers-outisde-underworks/"
        "only-opened-from-the-other-side"
    ): (
        _part(
            room_node_name(
                "underworks/underworks-outside-choral-chambers#room"
            ),
            "Ancestral Art: Cling Grip",
        ),
        _part(
            room_node_name(
                "underworks/underworks-outside-choral-chambers#room"
            ),
            "Ancestral Art: Silk Soar",
        ),
    ),
    "event:choral-chambers/choral-chambers-outside-spa/gauntlet": (
        _part(
            room_node_name(
                "choral-chambers/choral-chambers-outside-spa#gauntlet"
            )
        ),
    ),
    "event:high-halls/high-halls-arena/gauntlet": (
        _part(room_node_name("high-halls/high-halls-arena#gauntlet-arena")),
    ),
    (
        "event:choral-chambers/high-halls-corridor/"
        "left-door-opened-from-flea-shaft"
    ): (
        _part(
            room_node_name(
                "choral-chambers/choral-chambers-flea-shaft#top-section-3-right"
            )
        ),
    ),
    (
        "event:choral-chambers/high-halls-corridor/"
        "top-door-opened-from-high-halls-vault"
    ): (
        _part(room_node_name("high-halls/high-halls-vault#room")),
    ),
    "event:blasted-steps/great-conchflies/beat-great-conchflies": (
        _part(room_node_name("blasted-steps/great-conchflies#great-conchflies")),
    ),
    "event:blasted-steps/blasted-steps-toll-bench-bottom/lever-broken-from-coral-02": (
        _part(
            room_node_name(
                "blasted-steps/blasted-steps-toll-bench-bottom#top-right-pit-left"
            )
        ),
    ),
    "event:blasted-steps/blasted-steps-wide-long-vertical/lever-broken-from-coral-03": (
        _part(
            room_node_name(
                "blasted-steps/blasted-steps-wide-long-vertical#top-third"
            )
        ),
    ),
    "event:whiteward/whiteward-entrance/set-elevator-to-top": (
        _part(
            room_node_name("whiteward/whiteward-entrance#elevator-shaft"),
            "White Key",
        ),
    ),
    "event:whiteward/whiteward-sherma-gauntlet/balm-for-the-wounded-started": (
        _part("Path: Choral Chambers - Songclave"),
    ),
    "event:whiteward/whiteward-sherma-gauntlet/beat-sherma-gauntlet": (
        _part(room_node_name("whiteward/whiteward-sherma-gauntlet#room")),
    ),
    "event:whiteward/whiteward-unravelled-arena-room/surgeons-key-used": (
        _part(
            room_node_name(
                "whiteward/whiteward-unravelled-arena-room#surgery-tables-left"
            ),
            "Surgeon's Key",
        ),
    ),
    "event:whiteward/whiteward-unravelled-arena-room/beat-unravelled-arena": (
        _part(
            room_node_name(
                "whiteward/whiteward-unravelled-arena-room#key-shaft"
            ),
            "Surgeon's Key",
        ),
    ),
    # The Dancers event comes from their arena and requires an owned crest. The
    # old Choral path was too broad for this event.
    "event:global/cogwork-dancers-defeated": tuple(
        _part(
            room_node_name("cogwork-core/cog-dancers#bossarena"),
            crest,
        )
        for crest in (
            "Crest: Hunter",
            "Crest: Reaper",
            "Crest: Shaman",
            "Crest: Architect",
            "Crest: Wanderer",
            "Crest: Beast",
            "Crest: Witch",
        )
    ),
    "event:the-marrow/the-marrow-skull-wall/opened-from-shellwood": (
        _part(room_node_name("shellwood/mosstown-03#bottom-half")),
    ),
    "event:shellwood/bellshrine-03/activated": (
        _part(room_node_name("shellwood/bellshrine-03#room")),
    ),
    "event:shellwood/mosstown-03/top-exit-opened": (
        _part(room_node_name("shellwood/mosstown-03#top-half")),
    ),
    "event:shellwood/shellwood-02/elevator-activated": (
        _part(room_node_name("shellwood/shellwood-02#ceiling-area")),
    ),
    "event:shellwood/shellwood-02/lower-door-opened": (
        _part(room_node_name("shellwood/shellwood-02#ground-right")),
    ),
    "event:shellwood/shellwood-01/nest-broken": (
        _part(room_node_name("shellwood/shellwood-01#right-platforms")),
    ),
    "event:shellwood/shellwood-01b/elevator-activated": (
        _part(room_node_name("shellwood/shellwood-01b#elevator-platform")),
    ),
    "event:shellwood/shellwood-15/door-opened": (
        _part(
            room_node_name("shellwood/shellwood-15#room"),
            "Ability: Faydown Cloak",
        ),
        _part(
            room_node_name("shellwood/shellwood-15#room"),
            "Ability: Drifter's Cloak",
        ),
        _part(
            room_node_name("shellwood/shellwood-15#room"),
            "Swift Step",
        ),
        _part(
            room_node_name("shellwood/shellwood-15#room"),
            "Ancestral Art: Clawline",
        ),
        _part(
            room_node_name("shellwood/shellwood-15#room"),
            "Usable Sharpdart",
        ),
        _part(
            room_node_name("shellwood/shellwood-15#room"),
            "Crest: Beast",
        ),
    ),
    "event:shellwood/shellwood-26/upper-wall-broken": (
        _part(room_node_name("shellwood/shellwood-26#upper-area")),
    ),
    "event:far-fields/far-fields-deep-docks-backdoor/door-opened": (
        _part(
            room_node_name(
                "deep-docks/deep-docks-chains-upper-east#chain-platforms"
            )
        ),
    ),
    "event:far-fields/far-fields-deep-entrance/right-exit-door-switch-activated": (
        _part(
            room_node_name(
                "far-fields/far-fields-deep-entrance#right-exit-area"
            )
        ),
    ),
    "event:far-fields/far-fields-deep-fort/grunt-defeated": (
        _part(room_node_name("far-fields/far-fields-deep-fort#main-area")),
    ),
    "event:far-fields/far-fields-fort-upper-passage/platform-lowered": (
        _part(
            room_node_name(
                "far-fields/far-fields-fort-upper-passage#left-exit-area"
            )
        ),
    ),
    "event:far-fields/far-fields-pilgrim-s-rest/deep-passage-opened": (
        _part(
            room_node_name(
                "far-fields/far-fields-pilgrim-s-rest-deep-passage#room"
            )
        ),
    ),
    "event:far-fields/far-fields-pinstress-room/attic-blast-opened": (
        _part(
            room_node_name(
                "far-fields/far-fields-pinstress-attic#bottom-left-area"
            )
        ),
    ),
    "event:far-fields/far-fields-skull-room-west/bone-bridge-wall-broken": (
        _part(
            room_node_name(
                "far-fields/far-fields-skull-room-west#bone-bridge"
            )
        ),
    ),
    "event:far-fields/far-fields-skull-room-west/lower-left-wall-broken": (
        _part(
            room_node_name(
                "far-fields/far-fields-skull-room-west#lower-left-exit-area"
            )
        ),
    ),
    "event:far-fields/far-fields-upper-shaft/bridge-lever-activated": (
        _part(
            room_node_name(
                "far-fields/far-fields-upper-shaft#left-march-bridge-room"
            )
        ),
    ),
    "event:far-fields/far-fields-upper-shaft/lower-gate-opened": (
        _part(
            room_node_name("far-fields/far-fields-upper-shaft#the-bottom")
        ),
    ),
    "event:far-fields/far-fields-upper-shaft/shaft-opened": (
        _part(
            room_node_name(
                "far-fields/far-fields-upper-shaft#top-wind-tunnel"
            ),
            "Ability: Drifter's Cloak",
        ),
    ),
    "event:greymoor/greymoor-bellshrine/activated": (
        _part(
            room_node_name("greymoor/greymoor-bellshrine#room"),
            "Event: Craw Lake Cleared",
        ),
    ),
    "event:greymoor/greymoor-craw-lake/lever-broken-from-greymoor-crow-nest": (
        _part(
            room_node_name("greymoor/greymoor-crow-nest#crow-arena")
        ),
    ),
    "event:greymoor/greymoor-west-bellshrine-room/lever-switch": (
        _part(
            room_node_name(
                "greymoor/greymoor-west-bellshrine-room#middle-section-right"
            )
        ),
    ),
    "event:hunter-s-march/chapel-of-the-beast/boss-defeated": tuple(
        _part(
            room_node_name("hunter-s-march/chapel-of-the-beast#boss-arena"),
            crest,
        )
        for crest in (
            "Crest: Hunter",
            "Crest: Reaper",
            "Crest: Shaman",
            "Crest: Architect",
            "Crest: Wanderer",
            "Crest: Beast",
            "Crest: Witch",
        )
    ),
    "event:hunter-s-march/hunter-s-march-deep-docks-passage/gate-switch-flipped": (
        _part(
            room_node_name(
                "hunter-s-march/hunter-s-march-deep-docks-passage#before-gate"
            )
        ),
    ),
    "event:hunter-s-march/hunter-s-march-entrance/grunt-defeated": (
        _part(
            room_node_name(
                "hunter-s-march/hunter-s-march-entrance#before-door"
            )
        ),
    ),
    "event:hunter-s-march/hunter-s-march-treasure-vault/grunts-defeated": (
        _part(
            room_node_name(
                "hunter-s-march/hunter-s-march-treasure-vault#right-of-door"
            )
        ),
    ),
}


_GLOBAL_EVENT_NAME_BY_ATOM: Mapping[str, str] = {
    "event:global/eva-12-points": "Event: Eva 12 Points",
    "event:global/eva-20-points": "Event: Eva 20 Points",
    "event:global/eva-27-points": "Event: Eva 27 Points",
    "event:global/eva-32-points": "Event: Eva 32 Points",
    "event:global/silk-and-soul-offered": "Event: Silk and Soul Offered",
    "event:global/bell-beast-defeated":
        "Event: Bell Beast Defeated",
    "event:global/cogwork-dancers-defeated":
        "Event: Cogwork Dancers Defeated",
    "event:global/elegy-of-the-deep-learned":
        "Event: Elegy of the Deep Learned",
    "event:global/flexile-spines-completed":
        "Event: Flexile Spines Completed",
    "event:global/five-bellshrines-rung":
        "Event: Five Bellshrines Rung",
    "event:global/last-judge-defeated": "Event: Last Judge Defeated",
    "event:grand-gate/grand-bridge/last-judge-defeated":
        "Event: Last Judge Defeated",
    "event:global/missing-courier-rescued":
        "Event: Missing Courier Rescued",
    "event:global/tormented-trobbio-defeated":
        "Event: Tormented Trobbio Defeated",
    "event:global/trobbio-defeated": "Event: Trobbio Defeated",
    "event:the-marrow/the-marrow-bellway/bell-beast-defeated":
        "Event: Bell Beast Defeated",
}


# The room graph starts at Hornet's opening room. Internal coarse-path seeds
# are excluded because they let flat fallback rules bypass doors, switches
# and room connections.
_NODE_SEEDS: Mapping[str, tuple[CompiledRoomClause, ...]] = {
    "moss-grotto/moss-grotto-center#rock-bottom": (_part(),),
}


_EXTERNAL_BOUNDARY_SEEDS: Mapping[str, tuple[CompiledRoomClause, ...]] = {
    "putrified-ducts/putrified-ducts-bellway#bellway": (
        _part("Path: Bellway - Putrified Ducts"),
    ),
    "putrified-ducts/putrified-ducts-entrance#entrance": (
        _part("Path: Outlying Citadel - Memorium"),
    ),
    # The mapped Bellway room starts at the existing Blasted Steps endpoint.
    "blasted-steps/blasted-steps-bellway#room": (
        _part("Path: Blasted Steps - Bellway"),
    ),
    # The mapper's unresolved left transition is the missing handoff from
    # Halfway House. Preserve every compilable alternative. Innate Swim keeps
    # the normal graph unchanged; Swim randomization activates the other gates.
    "greymoor/greymoor-lower-halfway-home-path#room": (
        _part("Path: Greymoor - Halfway House", "Swift Step"),
        _part("Path: Greymoor - Halfway House", "Progressive Swift Step"),
        _part("Path: Greymoor - Halfway House", "Ancestral Art: Clawline"),
        _part("Path: Greymoor - Halfway House", "Ability: Faydown Cloak"),
        _part("Path: Greymoor - Halfway House", "Ability: Drifter's Cloak"),
        _part("Path: Greymoor - Halfway House", "Usable Sharpdart"),
        _part(
            "Path: Greymoor - Halfway House",
            "Crest: Beast",
            skip_tier=1,
        ),
        _part(
            "Path: Greymoor - Halfway House",
            "Usable Flea Brew",
            skip_tier=1,
        ),
        _part("Path: Greymoor - Halfway House", "Capability: Swim"),
    ),
    "greymoor/greymoor-east-bellshrine-room#upper-crow-nest": (
        _part(
            "Path: Greymoor - Halfway House",
            "Ancestral Art: Cling Grip",
        ),
    ),
    "greymoor/greymoor-craw-lake#upper-craw-nest": (
        _part(
            "Path: Greymoor - Halfway House",
            "Ancestral Art: Cling Grip",
        ),
    ),
    # The Bone Scroll side room is entered from the lower Halfway House route
    # by swimming or by combining Clawline with the ordinary ledge grab.
    "greymoor/greymoor-bone-scroll-room#room": (
        _part("Path: Greymoor - Halfway House", "Capability: Swim"),
        _part(
            "Path: Greymoor - Halfway House",
            "Ancestral Art: Clawline",
            "Capability: Ledge Grab",
        ),
    ),
    # Last Judge's arena is outside this room set. Defeating it puts Hornet at
    # the top of the Grand Elevator before the collapse.
    "grand-gate/grand-elevator#top": (
        _part("Event: Act 2 Started", "Event: Last Judge Defeated"),
    ),
    "greymoor/greymoor-bellway#bellway": (
        _part("Path: Bellway - Greymoor"),
    ),
    "greymoor/greymoor-03#bottom": (
        _part("Path: Greymoor - Halfway House"),
    ),
    "bilewater/exhaust-organ-external#left-platform": (
        _part("Path: Bilewater - Exhaust Organ"),
    ),
    # These station connections sit outside the imported rooms. Each route
    # stops at its station.
    "choral-chambers/choral-chambers-ventrica-room#ventrica": (
        _part("Path: Ventrica - Choral Chambers"),
    ),
    "choral-chambers/grand-bellway#base": (
        _part("Path: Bellway - Grand Bellway"),
        _part("Path: Ventrica - Grand Bellway"),
    ),
    "choral-chambers/songclave-tube#room": (
        _part("Path: Ventrica - Songclave"),
    ),

    "deep-docks/deep-docks-forge#left-area": (
        _part("Path: Deep Docks - Forge"),
    ),
    "deep-docks/deep-docks-chains-upper-east#chain-platforms": (
        _part("Path: Deep Docks - Forge", "Simple Key (Deep Docks)"),
    ),
    "deep-docks/deep-docks-bellway#room": (
        _part("Path: Bellway - Deep Docks"),
    ),
    "far-fields/far-fields-bellway#bellway": (
        _part("Path: Bellway - Far Fields"),
    ),
    "shellwood/shellwood-19#right-puddle": (
        _part("Path: Bellway - Shellwood"),
    ),
    "bellhart/belltown-06#lower-level": (
        _part("Path: Greymoor - Halfway House"),
    ),
    "bellhart/belltown-basement#room": (
        _part("Path: Bellway - Bellhart"),
    ),
    "bellhart/belltown#ground-level": (
        _part("Event: Widow Defeated"),
    ),
    "shellwood/shellwood-01b#bench-toll": (
        _part("Event: Widow Defeated"),
    ),
    # Bellway travel reaches this room but does not skip the Slab route.
    "the-slab/slab-bellway#room": (
        _part("Path: Bellway - The Slab"),
    ),
    # The capture sequence ends at Slab_Cell L1.
    "the-slab/slab-cell#l1": (
        _part("Path: The Slab - Capture Event"),
    ),
}


_ALL_NODE_SEEDS: Mapping[str, tuple[CompiledRoomClause, ...]] = {
    **_NODE_SEEDS,
    **_EXTERNAL_BOUNDARY_SEEDS,
}


_TRANSITION_EXTRA_REQUIREMENTS: Mapping[
    str, tuple[CompiledRoomClause, ...]
] = {
    "wisp-thicket/wisp-thicket-cave@t": (
        _part("Event: Act 2 Started"),
    ),
    "bilewater/exhaust-organ-interior@ue": (
        _part("Event: Act 2 Started"),
    ),
    "grand-gate/grand-bridge@r": (
        _part("Event: Act 2 Started"),
    ),
    # Library_07's top exit opens from its Clawline ring. Library_09's
    # west shortcut opens from inside Library_09; the reverse exits are free.
    "whispering-vaults/whispering-vaults-totally-not-white-palace@t": (
        _part(
            room_event_name(
                "event:whispering-vaults/"
                "whispering-vaults-totally-not-white-palace/"
                "whispering-vaults-clawline-ring"
            )
        ),
    ),
    "whispering-vaults/whispering-vaults-hell@tr": (
        _part(
            room_event_name(
                "event:whispering-vaults/whispering-vaults-jumps/"
                "whispering-vaults-flip-switch-6-up"
            )
        ),
    ),
}

_CONNECTION_REQUIREMENT_OVERRIDES: Mapping[
    str, tuple[CompiledRoomClause, ...]
] = {
    (
        "far-fields/far-fields-pinstress-attic"
        "#bottom-left-area>upper-right-area@d1"
    ): (
        _part(
            "Ability: Drifter's Cloak",
            "Ancestral Art: Cling Grip",
        ),
        _part(
            "Ability: Drifter's Cloak",
            "Usable Scuttlebrace",
            "Swift Step",
        ),
        _part("Ancestral Art: Silk Soar"),
    ),
}



# Dust_02 is missing its free downward route from the top opening. The y=93
# lever blocks the room edge, not this descent. Keep the movement-gated climb
# in the other direction.
_CURATED_EDGES: tuple[
    tuple[str, str, tuple[CompiledRoomClause, ...]], ...
] = (
    (
        "shellwood/shellwood-10#ground-level",
        "shellwood/shellwood-10#central-level",
        (_part(skip_tier=1),),
    ),
    (
        "bilewater/bilewater-sinner-s-entrance#left-quarter",
        "bilewater/bilewater-sinner-s-entrance#middle-quarter",
        (
            _part("Ancestral Art: Cling Grip", "Ability: Drifter's Cloak"),
            _part("Ancestral Art: Cling Grip", "Ancestral Art: Clawline"),
            _part("Ancestral Art: Cling Grip", "Usable Sharpdart"),
            _part("Ancestral Art: Cling Grip", "Ability: Faydown Cloak", "Capability: Swim"),
            _part("Ability: Faydown Cloak", "Usable Scuttlebrace", "Capability: Swim"),
            _part("Ancestral Art: Clawline", "Usable Scuttlebrace"),
            _part("Usable Sharpdart", "Usable Scuttlebrace"),
            _part("Swift Step", "Usable Scuttlebrace"),
        ),
    ),
    (
        "greymoor/greymoor-east-bellshrine-room#upper-crow-nest",
        "greymoor/greymoor-silver-shells-room#main-path",
        (
            _part("Ancestral Art: Silk Soar"),
            _part("Ability: Faydown Cloak"),
            _part("Ancestral Art: Cling Grip", skip_tier=1),
            _part("Ancestral Art: Cling Grip", "Swift Step"),
            _part("Ancestral Art: Cling Grip", "Ancestral Art: Clawline"),
            _part("Ancestral Art: Cling Grip", "Usable Sharpdart"),
            _part("Ancestral Art: Cling Grip", "Ability: Drifter's Cloak"),
            _part(skip_tier=3),
            _part("Capability: Ledge Grab", "Swift Step", skip_tier=2),
            _part("Capability: Ledge Grab", "Ancestral Art: Clawline", skip_tier=2),
        ),
    ),
    (
        "sinner-s-road/sinner-s-road-vertical-hall-west#top",
        "sinner-s-road/sinner-s-road-vertical-hall-west#upper-right",
        (_part(),),
    ),
    (
        "sinner-s-road/sinner-s-road-styx-room#right",
        "sinner-s-road/sinner-s-road-styx-room#left",
        (
            _part(
                room_event_name(
                    "event:sinner-s-road/sinner-s-road-styx-room/left-right-wall-broken"
                ),
                skip_tier=1,
            ),
            _part(
                room_event_name(
                    "event:sinner-s-road/sinner-s-road-styx-room/left-right-wall-broken"
                ),
                "Ability: Faydown Cloak",
            ),
            _part(
                room_event_name(
                    "event:sinner-s-road/sinner-s-road-styx-room/left-right-wall-broken"
                ),
                "Ancestral Art: Silk Soar",
                "Ability: Drifter's Cloak",
            ),
            _part(
                room_event_name(
                    "event:sinner-s-road/sinner-s-road-styx-room/left-right-wall-broken"
                ),
                "Ancestral Art: Cling Grip",
                "Usable Sharpdart",
            ),
            _part(
                room_event_name(
                    "event:sinner-s-road/sinner-s-road-styx-room/left-right-wall-broken"
                ),
                "Ancestral Art: Cling Grip",
                "Ancestral Art: Clawline",
            ),
            _part(
                room_event_name(
                    "event:sinner-s-road/sinner-s-road-styx-room/left-right-wall-broken"
                ),
                "Ancestral Art: Cling Grip",
                "Swift Step",
            ),
        ),
    ),
    (
        "sinner-s-road/sinner-s-road-styx-room#right",
        "sinner-s-road/sinner-s-road-styx-room#cage",
        (
            _part(
                room_event_name(
                    "event:sinner-s-road/sinner-s-road-styx-room/cage-right-wall-broken"
                )
            ),
        ),
    ),
    (
        "greymoor/greymoor-craw-lake#craw-building",
        "greymoor/greymoor-craw-lake#middle-craw-nest",
        tuple(
            _part(
                room_event_name(
                    "event:greymoor/greymoor-craw-lake/lever-broken-from-greymoor-crow-nest"
                ),
                crest,
                skip_tier=1,
            )
            for crest in (
                "Crest: Hunter",
                "Crest: Reaper",
                "Crest: Wanderer",
                "Crest: Beast",
                "Crest: Witch",
                "Crest: Architect",
                "Crest: Shaman",
            )
        ),
    ),
    (
        "sands-of-karak/sands-of-karak-lower-right-long-room#left-exit",
        "sands-of-karak/sands-of-karak-lower-right-long-room#lower-centre-platform",
        (
            _part("Ancestral Art: Clawline"),
        ),
    ),
)


# Existing AP locations whose room records represent the
# physical action/room but do not spell the current AP check name as an
# Included check row.  These are identity bindings only. Access still comes
# entirely from the room graph.
_EXISTING_LOCATION_NODE_BINDINGS: Mapping[str, str] = {
    "Beast Shard: Marrowmaw": "moss-grotto/moss-grotto-center#rock-bottom",
    "Bellhart - Outer Sign": "bellhart/belltown-07#room",
    "Mosshome - Moss Plaque": "bone-bottom/mosshome-upper#main-area",
    "The Marrow - Entrance Inscription": (
        "the-marrow/the-marrow-bell-bench#bell-bench"
    ),
    "The Marrow (Flea Caravan) - Rosary Dish": (
        "the-marrow/the-marrow-flea-caravan#main-area"
    ),
    "Bellshrine: The Marrow": "the-marrow/the-marrow-bellshrine#room",
    "Tool Pouch: Loddie": "the-marrow/the-marrow-jail#room",
    "The Marrow - Rosary Cache #11": (
        "the-marrow/the-marrow-lava-track#left-alcove"
    ),
    "The Marrow - Rosary Cache #12": (
        "the-marrow/the-marrow-lava-track#left-alcove"
    ),
    "The Marrow - Rosary Cache #13": (
        "the-marrow/the-marrow-lava-track#right-alcove"
    ),
    "Map Purchase: Wormways": "wormways/wormways-upper-east#upper-area",
    "Pin Purchase: Vendor Pins": "wormways/wormways-upper-east#upper-area",
    "Bellway: Deep Docks": "deep-docks/deep-docks-bellway#room",
    "Bellshrine: Deep Docks": "deep-docks/deep-docks-bellshrine#room",
    "Shellwood - Shellgrave Inscription": "shellwood/shellgrave#room",
    "Shellwood - Weaver Harp Inscription": (
        "shellwood/shellwood-10#ground-level"
    ),
    "Bellshrine: Bellhart": "bellhart/belltown-shrine#arena",
    "Curveclaw": "hunter-s-march/hunter-s-march-skarr-shop#skarr-shop",
    "Far Fields - Rosary Chest #1": (
        "far-fields/far-fields-fort-upper-passage#left-exit-area"
    ),
    "Relic Turn-in: Weaver Effigy (Keelal, Shellwood)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Bone Scroll (Wisp Thicket)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Weaver Effigy (Camora, Moss Grotto)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Choral Commandment (Jubilana)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Rune Harp (High Halls)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Choral Commandment (Western Whiteward)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Rune Harp (Weavenest Cindril)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Rune Harp (Weavenest Atla)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Bone Scroll (Underworks)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Bone Scroll (Far Fields)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Choral Commandment (Moss Grotto)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Choral Commandment (Eastern Whiteward)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Bone Scroll (Greymoor)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Weaver Effigy (Atla, The Slab)": (
        "bellhart/belltown-room-relic#room"
    ),
    "Relic Turn-in: Arcane Egg": "bellhart/belltown-room-relic#room",
}


_GREYMOOR_EAST_CACHE_POGO_REQUIREMENTS = tuple(
    _part(
        room_node_name(
            "greymoor/greymoor-east-bellshrine-room#upper-crow-nest"
        ),
        crest,
        movement,
        "Technique: Crest Pogo 1",
    )
    for crest in (
        "Crest: Hunter",
        "Crest: Reaper",
        "Crest: Wanderer",
        "Crest: Beast",
        "Crest: Witch",
        "Crest: Architect",
        "Crest: Shaman",
    )
    for movement in (
        "Ancestral Art: Clawline",
        "Usable Sharpdart",
        "Swift Step",
        "Ability: Drifter's Cloak",
    )
)


# Existing AP locations whose source is expressed by a persistent graph
# event rather than by a dedicated Included check row.
_EXISTING_LOCATION_CLAUSE_BINDINGS: Mapping[
    str, tuple[CompiledRoomClause, ...]
] = {
    "Greymoor - Rosary Cache #2": _GREYMOOR_EAST_CACHE_POGO_REQUIREMENTS,
    "Greymoor - Rosary Cache #3": _GREYMOOR_EAST_CACHE_POGO_REQUIREMENTS,
    "Beast Shard: Craggler": (
        _part(
            room_event_name(
                "event:wormways/wormways-craggler-hallway/defeat-craggler"
            )
        ),
    ),
    "Drifter's Cloak": (
        _part(
            room_node_name("far-fields/far-fields-pinstress-hut-interior#room"),
            "Event: Flexile Spines Completed",
        ),
    ),
}


def _merge(left: CompiledRoomClause, right: CompiledRoomClause) -> CompiledRoomClause:
    merged_counts: dict[str, int] = dict(left.item_counts)
    for item_name, minimum in right.item_counts:
        merged_counts[item_name] = max(merged_counts.get(item_name, 0), minimum)
    return CompiledRoomClause(
        all_of=tuple(dict.fromkeys((*left.all_of, *right.all_of))),
        silk_cost=left.silk_cost + right.silk_cost,
        item_counts=tuple(merged_counts.items()),
        require_silk_spear=left.require_silk_spear or right.require_silk_spear,
        minimum_skip_tier=max(
            left.minimum_skip_tier,
            right.minimum_skip_tier,
        ),
    )


def _event_requirement_name(atom: str) -> str:
    global_name = _GLOBAL_EVENT_NAME_BY_ATOM.get(atom)
    if global_name is not None:
        return global_name
    action_event_id = _ACTION_EVENT_ID_BY_ATOM.get(atom)
    return room_event_name(action_event_id or atom)


def _atom_alternatives(atom: str) -> tuple[CompiledRoomClause, ...]:
    if atom.startswith("combat:"):
        return (_part(combat_requirement_name(atom.removeprefix("combat:"))),)
    if atom == "mapper:act-2":
        return (_part("Act: 2"),)
    if atom.startswith("mapper:enemy-type-pogo:"):
        _, _, enemy, difficulty = atom.split(":")
        if not enemy or difficulty not in {"none", "easy", "medium", "hard"}:
            raise ValueError(f"unsupported enemy pogo: {atom}")
        tier = {"none": 0, "easy": 1, "medium": 2, "hard": 3}[difficulty]
        return (_part(f"Technique: Enemy Pogo {tier}"),) if tier else (_part(),)
    if atom.startswith("mapper:clawline:") and len(atom.split(":")) == 4:
        _, _, direction, casts = atom.split(":")
        if direction not in {"up", "down", "left", "right"}:
            raise ValueError(f"unsupported Clawline direction: {direction}")
        return _atom_alternatives("mapper:clawline:" + casts)
    if atom.startswith("mapper:"):
        _, kind, difficulty = atom.split(":")
        if kind.endswith("-direction") and difficulty in {"up", "down", "left", "right"}:
            capability = kind.removesuffix("-direction")
            base = {"ledge-grab": "capability:ledge-grab", "cling-grip": "item:cling-grip",
                    "sprint": "macro:progressive-swift-step-first", "dash": "macro:progressive-swift-step-full",
                    "look": "capability:free", "move": "capability:free"}.get(capability)
            if base is None:
                raise ValueError(f"unsupported directional capability: {atom}")
            return _atom_alternatives(base)
        if kind == "attack" and difficulty in {"up", "down", "left", "right"}:
            return (_part(),)
        if kind.endswith("-crest-attack") and difficulty in {"up", "down", "left", "right"}:
            return (_part("Crest: " + kind.removesuffix("-crest-attack").title()),)
        if kind == "clawline":
            casts = int(difficulty)
            if not 1 <= casts <= 8:
                raise ValueError(f"unsupported Clawline quantity: {casts}")
            return (_part("Ancestral Art: Clawline"),)
        if kind == "sharpdart":
            casts = int(difficulty)
            if not 1 <= casts <= 4:
                raise ValueError(f"unsupported Sharpdart quantity: {casts}")
            fragments = max(0, (casts * 4 - 9) * 2)
            return (_part("Usable Sharpdart", item_counts=((SPOOL_FRAGMENT_COUNT_ITEM, fragments),) if fragments else ()),)
        tier = {"none": 0, "easy": 1, "medium": 2, "hard": 3}[difficulty]
        if kind == "trails-end-maps":
            return (_part("Trail's End Maps"),)
        if kind == "bellway-network":
            return (_part("Path: Bellways"),)
        if kind == "marrow-bellway":
            return (_part("Event: Bell Beast Defeated"),)
        if kind == "silkspeed-anklets":
            return (_part("Usable Silkspeed Anklets"),)
        if kind == "elegy-of-the-deep":
            return (_part("Elegy of the Deep", "Ancestral Art: Needolin"),)
        if kind == "wind-skip":
            return (_part("Option: Proficient Movement"),)
        if kind == "needle-strike-stall":
            return tuple(_part("Ability: Needle Strike", crest.all_of[0], f"Technique: Needle Strike {max(1, tier)}") for crest in _ATOM_ALTERNATIVES["macro:any-crest"])
        if kind in {"flintslate-stall", "plasmium-phial-stall", "voltvessels-stall"}:
            tool = {"flintslate-stall": "Flintslate", "plasmium-phial-stall": "Plasmium Phial", "voltvessels-stall": "Voltvessels"}[kind]
            return (_part("Usable " + tool, f"Technique: {tool} Stall {max(1, tier)}"),)
        if kind == "drill-crystal-pogo":
            return (_part("Usable Drill Crystal Pogo Loadout", f"Technique: Drill Crystal Pogo {max(1, tier)}"),)
        if kind == "flea-brew-jump":
            return (_part("Usable Flea Brew", "Option: Flea Brew Jump Logic"),)
        if kind == "flea-brew-stall":
            return (_part("Usable Flea Brew", f"Technique: Flea Brew Stall {max(1, tier)}"),)
        if kind == "proficient-movement":
            return (_part("Option: Proficient Movement"),)
        if kind in {"heal-stall", "hazard-respawn"}:
            name = {"heal-stall": "Heal Stall", "hazard-respawn": "Hazard Respawn"}[kind]
            return (_part(f"Technique: {name} {max(1, tier)}"),)
        if kind == "scuttlebrace":
            return (_part("Usable Scuttlebrace", "Swift Step", f"Technique: Scuttlebrace {max(1, tier)}"),)
        if kind == "spike-pogo-skip":
            return tuple(_merge(crest, _part(f"Technique: Crest Pogo {max(1, tier)}"))
                         for crest in _ATOM_ALTERNATIVES["macro:spike-pogo"])
        if kind == "enemy-pogo":
            return (_part(f"Technique: Enemy Pogo {tier}"),) if tier else (_part(),)
        if kind.endswith("-crest-pogo"):
            return (_part("Crest: " + kind.removesuffix("-crest-pogo").title(), f"Technique: Crest Pogo {max(1, tier)}"),)
        if kind.endswith("-crest-needle-strike"):
            return (_part("Crest: " + kind.removesuffix("-crest-needle-strike").title(), "Ability: Needle Strike", f"Technique: Needle Strike {max(1, tier)}"),)
        raise ValueError(f"unsupported mapper atom: {atom}")
    if atom.startswith("received:"):
        name = atom[len("received:"):]
        if not name:
            raise ValueError("received item name cannot be empty")
        if name == "Swift Step":
            return (_part(name),)
        return (_part(item_counts=((name, 1),)),)
    alternatives = _ATOM_ALTERNATIVES.get(atom)
    if alternatives is not None:
        return alternatives
    if atom.startswith(("count:fleas:", "count:pale-oil:", "count:bellshrines-activated:", "count:craftmetal:")):
        _, kind, quantity = atom.split(":")
        minimum = int(quantity)
        if minimum < 1:
            raise ValueError(f"invalid count: {atom}")
        return (_part(item_counts=(({"fleas":"$fleas", "pale-oil":"Pale Oil", "bellshrines-activated":"$bellshrines", "craftmetal":"Craftmetal"}[kind], minimum),)),)
    if atom == "count:threefold-melody-parts:2":
        return tuple(_part(*pair) for pair in (
            ("Conductor's Melody", "Architect's Melody"),
            ("Conductor's Melody", "Vaultkeeper's Melody"),
            ("Architect's Melody", "Vaultkeeper's Melody"),
        ))
    if atom.startswith("count:mossberry:"):
        try:
            minimum = int(atom.rsplit(":", 1)[1])
        except ValueError as exc:
            raise ValueError(
                f"invalid room-graph mossberry count atom: {atom!r}"
            ) from exc
        if minimum < 1:
            raise ValueError(
                f"invalid room-graph mossberry count atom: {atom!r}"
            )
        return (_part(item_counts=(("Mossberry", minimum),)),)
    if atom.startswith("count:pollip-heart:"):
        try:
            minimum = int(atom.rsplit(":", 1)[1])
        except ValueError as exc:
            raise ValueError(
                f"invalid room-graph pollip-heart count atom: {atom!r}"
            ) from exc
        if minimum < 1:
            raise ValueError(
                f"invalid room-graph pollip-heart count atom: {atom!r}"
            )
        return (_part(item_counts=(("Pollip Heart", minimum),)),)
    if atom.startswith("count:spool-fragment:"):
        try:
            minimum = int(atom.rsplit(":", 1)[1])
        except ValueError as exc:
            raise ValueError(
                f"invalid room-graph Spool Fragment count atom: {atom!r}"
            ) from exc
        if minimum < 1 or minimum > 18:
            raise ValueError(
                f"invalid room-graph Spool Fragment count atom: {atom!r}"
            )
        return (_part(item_counts=((SPOOL_FRAGMENT_COUNT_ITEM, minimum),)),)
    if atom.startswith("count:progressive-silkheart:"):
        try:
            minimum = int(atom.rsplit(":", 1)[1])
        except ValueError as exc:
            raise ValueError(
                f"invalid room-graph Progressive Silkheart count atom: {atom!r}"
            ) from exc
        if minimum < 1:
            raise ValueError(
                f"invalid room-graph Progressive Silkheart count atom: {atom!r}"
            )
        return (_part(item_counts=(("Progressive Silkheart", minimum),)),)
    if atom.startswith("count:progressive-needle-upgrade:"):
        try:
            minimum = int(atom.rsplit(":", 1)[1])
        except ValueError as exc:
            raise ValueError(
                "invalid room-graph Progressive Needle Upgrade count atom: "
                f"{atom!r}"
            ) from exc
        if minimum < 1:
            raise ValueError(
                "invalid room-graph Progressive Needle Upgrade count atom: "
                f"{atom!r}"
            )
        return (_part(item_counts=(("Progressive Needle Upgrade", minimum),)),)
    if atom.startswith("node:"):
        return (_part(room_node_name(atom.removeprefix("node:"))),)
    if atom.startswith("event:"):
        return (_part(_event_requirement_name(atom)),)
    raise ValueError(f"unsupported room-graph atom: {atom!r}")


def _compile_spec(
    requirement: RequirementSpec,
    *prefix: str,
    silk_costs: bool = False,
) -> tuple[CompiledRoomClause, ...]:
    if requirement.mode is RequirementMode.UNRESOLVED:
        return ()
    if requirement.mode is RequirementMode.INHERIT:
        return (_part(*prefix),)

    compiled: list[CompiledRoomClause] = []
    for source_clause in requirement.dnf:
        products: Iterable[tuple[CompiledRoomClause, ...]] = product(
            *(_atom_alternatives(atom) for atom in source_clause)
        ) if source_clause else ((),)
        for product_parts in products:
            clause = _part(*prefix)
            for part in product_parts:
                clause = _merge(clause, part)
            if {"Usable Flea Brew", "Usable Silkspeed Anklets"}.issubset(clause.all_of):
                clause = _merge(clause, _part("Usable Cindril Loadout"))
            equipment = tuple(sorted(name for name in clause.all_of
                                     if name.startswith(("Usable ", "Crest: "))))
            if any(name.startswith("Usable ") for name in equipment) and len(equipment) > 1:
                clause = _merge(clause, _part("Loadout: " + " + ".join(equipment)))
            if silk_costs:
                from .silk_economy import atom_cost
                clause = replace(clause, silk_cost=atom_cost(source_clause, clause))
            compiled.append(clause)
    return tuple(dict.fromkeys(compiled))


def _append_requirements(
    target: dict[str, list[CompiledRoomClause]],
    name: str,
    requirements: Iterable[CompiledRoomClause],
) -> None:
    bucket = target.setdefault(name, [])
    for requirement in requirements:
        # DNF alternatives are monotonic. If an existing clause requires a
        # subset of the new clause's nodes/items/options, the new clause can
        # never unlock anything and is redundant. Conversely, a newly added
        # weaker clause replaces every stronger alternative it subsumes.
        if any(_clause_subsumes(existing, requirement) for existing in bucket):
            continue
        bucket[:] = [
            existing
            for existing in bucket
            if not _clause_subsumes(requirement, existing)
        ]
        bucket.append(requirement)


def _clause_subsumes(
    weaker: CompiledRoomClause,
    stronger: CompiledRoomClause,
) -> bool:
    """Return whether satisfying ``stronger`` always satisfies ``weaker``."""

    if not set(weaker.all_of).issubset(stronger.all_of):
        return False
    if weaker.require_silk_spear and not stronger.require_silk_spear:
        return False
    if weaker.silk_cost > stronger.silk_cost:
        return False
    if weaker.minimum_skip_tier > stronger.minimum_skip_tier:
        return False

    weaker_counts = dict(weaker.item_counts)
    stronger_counts = dict(stronger.item_counts)
    return all(
        minimum <= stronger_counts.get(item_name, 0)
        for item_name, minimum in weaker_counts.items()
    )


def _has_only_declared_room_references(
    clause: CompiledRoomClause,
    declared_owners: Mapping[str, object],
) -> bool:
    return all(
        not reference.startswith((ROOM_NODE_PREFIX, ROOM_EVENT_PREFIX))
        or reference in declared_owners
        for reference in clause.all_of
    )


def _structural_reachability(
    graph,
    authoritative_node_ids: frozenset[str],
    extra_edges: Iterable[tuple[str, str]],
    seed_ids: Iterable[str] | None = None,
) -> frozenset[str]:
    outgoing: dict[str, set[str]] = {}
    transition_by_id = graph.transition_by_id
    for room in graph.authoritative_rooms:
        for transition in room.transitions:
            if not transition.is_compilable:
                continue
            target_port = transition_by_id[transition.target.port_id]
            if target_port.source_node_id not in authoritative_node_ids:
                continue
            outgoing.setdefault(transition.source_node_id, set()).add(
                target_port.source_node_id
            )
        for connection in room.connections:
            if not connection.is_compilable:
                continue
            outgoing.setdefault(connection.source_node_id, set()).add(
                connection.target_node_id
            )
    for source, target in extra_edges:
        outgoing.setdefault(source, set()).add(target)

    reachable = set(_ALL_NODE_SEEDS if seed_ids is None else seed_ids)
    pending = list(reachable)
    while pending:
        source = pending.pop()
        for target in outgoing.get(source, ()):
            if target in reachable:
                continue
            reachable.add(target)
            pending.append(target)
    return frozenset(reachable)


def _semantic_reachable_owners(
    node_requirements: Mapping[str, Iterable[CompiledRoomClause]],
    event_requirements: Mapping[str, Iterable[CompiledRoomClause]],
    strict_owners: bool = False,
) -> frozenset[str]:
    """Resolve nodes which have a satisfiable monotonic route with all items.

    Structural connectivity alone admits closed cycles such as a room whose
    only entrance needs a switch located inside that same room.  For this
    compiler check, normal items and coarse paths are available.
    room nodes and room events still have to derive from a real seed.
    """

    owners = {
        **node_requirements,
        **event_requirements,
    }
    reachable: set[str] = set()
    changed = True
    while changed:
        changed = False
        for owner, alternatives in owners.items():
            if owner in reachable:
                continue
            if any(
                alternative.minimum_skip_tier == 0
                and all(
                    (
                        reference in reachable
                        if (strict_owners and reference in owners) or reference.startswith(
                            (ROOM_NODE_PREFIX, ROOM_EVENT_PREFIX)
                        )
                        else True
                    )
                    for reference in alternative.all_of
                )
                for alternative in alternatives
            ):
                reachable.add(owner)
                changed = True

    return frozenset(reachable)


def _semantic_reachability(node_requirements, event_requirements) -> frozenset[str]:
    return frozenset(
        name[len(ROOM_NODE_PREFIX):]
        for name in _semantic_reachable_owners(node_requirements, event_requirements)
        if name.startswith(ROOM_NODE_PREFIX)
    )


@dataclass(frozen=True)
class CompiledTransition:
    id: str
    source: str
    requirements: tuple[CompiledRoomClause, ...]
    exit_requirements: tuple[CompiledRoomClause, ...]


@lru_cache(maxsize=8192)
def _compile_transition(transition_id, source_node_id, requirement, silk_costs):
    source = room_node_name(source_node_id)
    prefix = ((room_event_name("event:mapper/reviewed:bellhart-full-house-conversation"),)
              if transition_id == "bellhart/belltown@hd" else ())
    rules = _compile_spec(requirement, *prefix, silk_costs=silk_costs)
    return CompiledTransition(transition_id, source,
                              tuple(dict.fromkeys(_merge(_part(source), rule) for rule in rules)), rules)


def compile_transition(transition, *, silk_costs=False):
    return _compile_transition(transition.id, transition.source_node_id,
                               transition.requirement, silk_costs)


def compile_transition_requirements(transition, *, include_source=True, silk_costs=False):
    compiled = compile_transition(transition, silk_costs=silk_costs)
    return compiled.requirements if include_source else compiled.exit_requirements


def compile_room_graph(graph=None, *, node_seeds=None, legacy_rules=None, transition_targets=None, silk_costs=False) -> CompiledRoomGraph:
    graph = load_room_graph() if graph is None else graph
    mapper = graph.assumptions.get("mapper_schema") == 3
    if legacy_rules is None:
        legacy_rules = not mapper
    if mapper and legacy_rules:
        raise ValueError("mapper graphs cannot use legacy traversal rules")
    if mapper and node_seeds is None and graph.assumptions.get("starting_nodes"):
        node_seeds = {node: (_part(),) for node in graph.assumptions["starting_nodes"]}
    if not legacy_rules and node_seeds is None:
        raise ValueError("mapper graphs require explicit starting nodes")
    seeds = _ALL_NODE_SEEDS if node_seeds is None else node_seeds
    curated_edges = _CURATED_EDGES if legacy_rules else ()
    transition_extras = _TRANSITION_EXTRA_REQUIREMENTS if legacy_rules else {}
    connection_overrides = _CONNECTION_REQUIREMENT_OVERRIDES if legacy_rules else {}
    implicit_events = _IMPLICIT_EVENT_SOURCE if legacy_rules else {}
    location_nodes = _EXISTING_LOCATION_NODE_BINDINGS if legacy_rules else {}
    location_clauses = _EXISTING_LOCATION_CLAUSE_BINDINGS if legacy_rules else {}
    authoritative_rooms = graph.authoritative_rooms
    authoritative_node_ids = frozenset(
        node.id for room in authoritative_rooms for node in room.nodes
    )
    if mapper:
        seeds = dict(seeds)
        for arrival in graph.assumptions.get('story_arrivals', ()):
            if arrival.get('act') in {'Act: 2', 'Act: 3'} and not arrival.get('event'):
                requirement = arrival['act']
            elif not arrival.get('act') and arrival.get('event') in graph.event_by_id:
                requirement = room_event_name(arrival['event'])
            else:
                raise ValueError('invalid mapper story arrival')
            node_id = arrival['node_id']
            seeds[node_id] = (*seeds.get(node_id, ()), _part(requirement))
    unknown_seed_ids = tuple(sorted(set(seeds) - authoritative_node_ids))
    if unknown_seed_ids:
        raise ValueError(
            "room graph compiler has undeclared node seeds: "
            + ", ".join(unknown_seed_ids)
        )
    node_requirements: dict[str, list[CompiledRoomClause]] = {
        room_node_name(node_id): [] for node_id in authoritative_node_ids
    }
    for node_id, requirements in seeds.items():
        _append_requirements(
            node_requirements,
            room_node_name(node_id),
            requirements,
        )

    transition_by_id = graph.transition_by_id
    structural_edges: list[tuple[str, str]] = []
    for room in authoritative_rooms:
        for transition in room.transitions:
            if not transition.is_compilable:
                continue
            target_id = transition.target.port_id if transition_targets is None else transition_targets.get(transition.id, transition.target.port_id)
            if target_id is None:
                continue
            target_port = transition_by_id[target_id]
            target_node_id = target_port.source_node_id
            if target_node_id not in authoritative_node_ids:
                continue
            structural_edges.append((transition.source_node_id, target_node_id))
            requirements = compile_transition_requirements(transition, silk_costs=silk_costs)
            extra_requirements = transition_extras.get(
                transition.id,
                (_part(),),
            )
            _append_requirements(
                node_requirements,
                room_node_name(target_node_id),
                (
                    _merge(requirement, extra_requirement)
                    for requirement, extra_requirement in product(
                        requirements,
                        extra_requirements,
                    )
                ),
            )
        for connection in room.connections:
            if not connection.is_compilable:
                continue
            structural_edges.append(
                (connection.source_node_id, connection.target_node_id)
            )
            connection_requirements = (
                connection_overrides.get(connection.id)
            )
            if connection_requirements is None:
                connection_requirements = _compile_spec(
                    connection.requirement,
                    room_node_name(connection.source_node_id),
                    silk_costs=silk_costs,
                )
            else:
                connection_requirements = tuple(
                    _merge(
                        _part(room_node_name(connection.source_node_id)),
                        requirement,
                    )
                    for requirement in connection_requirements
                )
            _append_requirements(
                node_requirements,
                room_node_name(connection.target_node_id),
                connection_requirements,
            )

    for source, target, requirements in curated_edges:
        structural_edges.append((source, target))
        _append_requirements(
            node_requirements,
            room_node_name(target),
            (
                _merge(_part(room_node_name(source)), requirement)
                for requirement in requirements
            ),
        )

    event_requirements: dict[str, list[CompiledRoomClause]] = {}
    for room in authoritative_rooms:
        for event in room.events:
            if not event.is_compilable:
                if mapper:
                    event_requirements.setdefault(room_event_name(event.id), [])
                continue
            # The Shakra switch row puts its effect in the requirement column.
            # Reaching the switch is sufficient to lower the platform.
            if legacy_rules and event.id.endswith("/lower-platform-switch-into-floor"):
                requirements = (_part(room_node_name(event.node_id)),)
            else:
                requirements = _compile_spec(
                    event.requirement,
                    room_node_name(event.node_id),
                    silk_costs=silk_costs,
                )
            _append_requirements(
                event_requirements,
                room_event_name(event.id),
                requirements,
            )

    for atom, requirements in implicit_events.items():
        _append_requirements(
            event_requirements,
            _event_requirement_name(atom),
            requirements,
        )

    if mapper:
        for name, targets in graph.assumptions.get("node_aliases", {}).items():
            _append_requirements(node_requirements, name, (_part(room_node_name(target)) for target in targets))
        for name, targets in graph.assumptions.get("event_aliases", {}).items():
            event_requirements.setdefault(name, [])
            guards = graph.assumptions.get("event_alias_requirements", {}).get(name, ())
            _append_requirements(event_requirements, name, (_part(room_event_name("event:mapper/" + target), *guards) for target in targets))
        for slug, binding in graph.assumptions.get('inventory_bindings', {}).items():
            owner = room_event_name('event:mapper/owned/' + slug)
            if binding['mode'] == 'received':
                clauses = _atom_alternatives('received:' + binding['item_name'])
            elif binding['mode'] == 'vanilla':
                clauses = tuple(_part(room_event_name('event:mapper/' + source)) for source in binding['source_events'])
            else:
                raise ValueError('invalid mapper inventory mode')
            event_requirements.setdefault(owner, [])
            _append_requirements(event_requirements, owner, clauses)
        for owner, clauses in node_requirements.items():
            clauses[:] = [clause for clause in clauses if owner not in clause.all_of]

    semantically_reachable_owners = _semantic_reachable_owners(
        node_requirements, event_requirements, strict_owners=mapper,
    )
    semantically_reachable_nodes = frozenset(
        name[len(ROOM_NODE_PREFIX):] for name in semantically_reachable_owners
        if name.startswith(ROOM_NODE_PREFIX)
    )
    reachable_nodes = _structural_reachability(
        graph,
        authoritative_node_ids,
        ((source, target) for source, target, _requirements in curated_edges),
        seeds,
    )
    check_requirements: dict[str, list[CompiledRoomClause]] = {}
    check_source_ids: dict[str, list[str]] = {}
    skipped_checks: list[str] = []
    declared_owners = {
        **node_requirements,
        **event_requirements,
    }
    present_authoritative_checks = frozenset(
        check.canonical_location
        for room in authoritative_rooms
        for check in room.checks
        if check.currently_randomized and check.canonical_location is not None
    )
    for room in authoritative_rooms:
        for check in room.checks:
            independent_source = mapper and (
                (check.raw_cells.get('inventory_service') == 'crest-slot'
                 and (check.canonical_location or '').startswith('Crest Slot: '))
                or (check.raw_cells.get('automatic_check') == 'hunter-crest'
                    and check.canonical_location == 'Crest: Hunter')
            )
            if (
                not check.currently_randomized
                or (mapper and check.canonical_location in graph.assumptions.get('quarantined_checks', {}))
                or
                not check.is_compilable
                or (not independent_source and check.node_id not in semantically_reachable_nodes)
            ):
                skipped_checks.append(check.id)
                continue
            requirements = tuple(
                requirement
                for requirement in _compile_spec(
                    check.requirement,
                    *(() if independent_source else (room_node_name(check.node_id),)),
                    silk_costs=silk_costs,
                )
                if _has_only_declared_room_references(
                    requirement,
                    declared_owners,
                )
                and (not mapper or all(
                    reference not in declared_owners or reference in semantically_reachable_owners
                    for reference in requirement.all_of
                ))
            )
            if (
                not requirements
                or all(
                    requirement.minimum_skip_tier > 0
                    for requirement in requirements
                )
            ):
                skipped_checks.append(check.id)
                continue
            _append_requirements(
                check_requirements,
                check.canonical_location,
                requirements,
            )
            check_source_ids.setdefault(check.canonical_location, []).append(
                check.id
            )

    if "Boss: Moorwing" in check_requirements:
        reward_name = "Moorwing - Beast Shard"
        _append_requirements(check_requirements, reward_name, check_requirements["Boss: Moorwing"])
        check_source_ids[reward_name] = [
            "native-reward:" + source_id
            for source_id in check_source_ids["Boss: Moorwing"]
        ]

    for location_name, node_id in location_nodes.items():
        if node_id not in semantically_reachable_nodes:
            continue
        _append_requirements(
            check_requirements,
            location_name,
            (_part(room_node_name(node_id)),),
        )
        check_source_ids.setdefault(location_name, []).append(
            f"derived-node:{node_id}"
        )

    for location_name, requirements in location_clauses.items():
        valid_requirements = tuple(
            requirement
            for requirement in requirements
            if _has_only_declared_room_references(requirement, declared_owners)
        )
        if not valid_requirements:
            continue
        _append_requirements(
            check_requirements,
            location_name,
            valid_requirements,
        )
        check_source_ids.setdefault(location_name, []).append(
            "derived-clause:" + location_name
        )

    present_authoritative_checks = frozenset(
        (
            *present_authoritative_checks,
            *location_nodes,
            *location_clauses,
        )
    )

    return CompiledRoomGraph(
        node_requirements=MappingProxyType(
            {name: tuple(rows) for name, rows in node_requirements.items()}
        ),
        event_requirements=MappingProxyType(
            {name: tuple(rows) for name, rows in event_requirements.items()}
        ),
        check_requirements=MappingProxyType(
            {name: tuple(rows) for name, rows in check_requirements.items()}
        ),
        check_source_ids=MappingProxyType(
            {name: tuple(ids) for name, ids in check_source_ids.items()}
        ),
        authoritative_check_names=frozenset(check_requirements),
        quarantined_check_names=frozenset(
            (present_authoritative_checks | frozenset(graph.assumptions.get("expected_checks", ()))) - set(check_requirements)
        ),
        structurally_reachable_nodes=reachable_nodes,
        semantically_reachable_nodes=semantically_reachable_nodes,
        skipped_check_ids=tuple(sorted(skipped_checks)),
    )
