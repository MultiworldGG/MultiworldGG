"""Act 1 goal content exclusions."""

from __future__ import annotations

from typing import Mapping

from .eva import EVA_CREST_SLOTS, EVA_REWARDS
from .locations import HUNTER_CREST_SLOT_LOCATION_NAMES, INDIVIDUAL_RELIC_ITEM_BY_TURN_IN_LOCATION
from .requirements import (
    COMPILED_ROOM_GRAPH,
    _ESTABLISHED_REQUIREMENTS_BY_LOCATION,
)


ACT_ONE_GOAL_KEY = "act_1"
ACT_ONE_TOOL_POUCH_SUPPLY = 3
_BONE_BOTTOM_REPAIRS_LOCATION_NAME = "Wish: Bone Bottom Repairs"
_LIFESAVING_BRIDGE_LOCATION_NAME = "Wish: A Lifesaving Bridge"

_POST_ACT_ONE_SOURCE_ACTS = frozenset(("Act 2", "Act 3"))
_UNTAGGED_POST_ACT_ONE_LOCATION_NAMES = frozenset(
    (
        "Bellhart Roof - Memory Locket",
        "Throwing Ring",
        "Curvesickle",
        "Egg of Flealia",
        "Wish: Fine Pins",
        "Wish: The Wandering Merchant",
        "Wish: My Missing Brother",
        "Wish: Balm for the Wounded",
        "Wish: Cloaks of the Choir",
        "Wish: Building Up Songclave",
        "Wish: Strengthening Songclave",
        "Wish: Songclave Supplies",
        "Wish: Fleatopia Supplies",
        "Wish: Liquid Lacquer",
        "Beastling Call",
        "Craw Summons",
        "Boss: Broodmother",
        "Boss: Second Sentinel",
        "Boss: Trobbio",
        "Boss: Palestag",
        "Boss: Clover Dancers",
        "Boss: Gurr the Outcast",
        "Boss: Raging Conchfly",
    )
)

_POST_ACT_ONE_SOURCE_LOCATION_NAMES = frozenset(
    location_name
    for location_name, requirements in
    _ESTABLISHED_REQUIREMENTS_BY_LOCATION.items()
    if (
        requirements
        and all(
            requirement.act in _POST_ACT_ONE_SOURCE_ACTS
            for requirement in requirements
        )
    )
) | _UNTAGGED_POST_ACT_ONE_LOCATION_NAMES

_POST_ACT_ONE_RELIC_TURN_IN_LOCATION_NAMES = frozenset(
    turn_in_location
    for turn_in_location, relic_item in
    INDIVIDUAL_RELIC_ITEM_BY_TURN_IN_LOCATION.items()
    if relic_item in _POST_ACT_ONE_SOURCE_LOCATION_NAMES
)

_POST_ACT_ONE_ROOM_GRAPH_LOCATION_NAMES = frozenset(
    location_name
    for location_name, source_ids in
    COMPILED_ROOM_GRAPH.check_source_ids.items()
    if any(
        source_id.startswith(
            (
                "choral-chambers/",
                "cogwork-core/",
                "underworks/",
                "grand-gate/",
                "whispering-vaults/",
                "whiteward/",
                "high-halls/",
                "memorium/",
            )
        )
        for source_id in source_ids
    )
)

_ACT_ONE_DEPENDENCY_EXCLUDED_LOCATION_NAMES = frozenset(
    (
        "Pollen Heart",
        "Everbloom",
        "Sprintmaster's Memento",
        "Guardian's Memento",
        "Hero's Memento",
        'Grey Memento',
        'Surface Memento',
        'Craw Memento',
        "Hunter's Heart",
        "Encrusted Heart",
        "Twisted Bud",
        "Maiden Soul",
        "Hermit Soul",
        "Seeker Soul",
        "Bilewater - Map Purchase",
        "Sands of Karak - Map Purchase",
        "Flea: Deep Docks - Mines",
        "Flea: Sands of Karak",
        "Volt Filament",
        "Snare Setter",
        "Thief's Mark",
        "Snitch Pick",
        "Quick Sling",
        "Druid's Eyes",
        "Flintslate",
        "Sharpdart",
        "Boss: Forebrothers Signis & Gron",
        "Boss: Disgraced Chef Lugoli",
        "Boss: Groal the Great",
        "Boss: Voltvyrm",
        "Boss: Crawfather",
        "Greymoor - Rosary Cache #35",
        "Greymoor - Rosary Cache #36",
        "Greymoor - Rosary Cache #37",
        "Boss: Father of the Flame",
        "Wispfire Lantern",
        "Pinmaster Plinney: Shining Needle",
        "Pinmaster Plinney: Hivesteel Needle",
        "Pinmaster Plinney: Pale Steel Needle",
        "Crest Slot: Witch (Red 1)",
        "Crest Slot: Witch (Blue 1)",
        "Crest Slot: Witch (Blue 2)",
        "Crest Slot: Architect (Blue 1)",
        "Crest Slot: Architect (Yellow 1)",
        "Crest Slot: Architect (Yellow 2)",
        "Crest Slot: Architect (Blue 2)",
        "Crest Slot: Shaman (Blue 1)",
        "Crest Slot: Shaman (Blue 2)",
        "Deep Docks - Shard Bundle #1",
        "Shellwood - Shard Bundle",
        "Shellwood - Rosary String #2",
        "Relic: Weaver Effigy (Keelal, Shellwood)",
        "Shellwood - Shell Shard Cache #1",
        "Shellwood - Shell Shard Cache #2",
        "Shellwood - Shell Shard Cache #3",
        "Shellwood - Shell Shard Cache #12",
        "Grindle (Blasted Steps) - Spool Fragment",
        "Relic: Psalm Cylinder (Grindle)",
        "Grindle - Crafting Kit",
        "The Slab - Frayed Rosary String #1",
        "The Slab - Shard Bundle",
        "The Slab - Frayed Rosary String #2",
        "The Slab - Frayed Rosary String #3",
        "Choral Chambers - Heavy Rosary Necklace",
        "Cogwork Core - Shard Bundle",
        "Songclave - Heavy Rosary Necklace",
        "Underworks - Frayed Rosary String #2",
        "Wisp Thicket - Rosary Necklace",
        "Deep Docks - Rosary Cache #1",
        "Deep Docks - Rosary Cache #2",
        "Sinner's Road - Rosary Cache #8",
        "Bone Bottom - Shell Shard Cache",
        "Deep Docks - Shell Shard Cache #5",
        "Deep Docks - Shell Shard Cache #6",
        "Deep Docks - Shell Shard Cache #7",
        "Deep Docks - Shell Shard Cache #8",
        "Deep Docks - Shell Shard Cache #9",
        "Far Fields - Pale Rosary Necklace",
        "Far Fields - Rosary Cache #18",
        "Far Fields - Shell Shard Cache #2",
        "Far Fields - Shell Shard Cache #3",
        "Far Fields - Shell Shard Cache #8",
        "Sands of Karak - Shell Shard Cache #1",
        "Sands of Karak - Shell Shard Cache #2",
        "Sands of Karak - Shell Shard Cache #3",
        "Sands of Karak - Shell Shard Cache #4",
        "Sands of Karak - Shell Shard Cache #11",
        "Sands of Karak - Shell Shard Cache #9",
        "Sands of Karak - Shell Shard Cache #10",
        "Wisp Thicket - Shell Shard Cache #1",
        "Wisp Thicket - Shell Shard Cache #2",
        "Wisp Thicket - Shell Shard Cache #3",
        "Wisp Thicket - Shell Shard Cache #4",
        "Wisp Thicket - Shell Shard Cache #5",
        "Wisp Thicket - Shell Shard Cache #6",
        "Wisp Thicket - Shell Shard Cache #7",
        "Conchcutter",
        "Flea: Bilehaven",
        "Putrified Ducts - Frayed Rosary String",
        "Bilewater - Frayed Rosary String",
        "Bilewater - Rosary Cache #3",
        "Bilewater - Shell Shard Cache #1",
        "Bilewater - Shell Shard Cache #2",
        "Bilewater - Shell Shard Cache #3",
        "Bilewater - Shell Shard Cache #4",
        "Sands of Karak East Bench - Simple Key",
        "Sands of Karak - Upper Coral Tablet",
    )
)

_POST_ACT_ONE_CREST_SLOT_LOCATION_NAMES_BY_CREST = {
    "Crest: Witch": frozenset(
        (
            "Crest Slot: Witch (Red 1)",
            "Crest Slot: Witch (Blue 1)",
            "Crest Slot: Witch (Blue 2)",
        )
    ),
    "Crest: Architect": frozenset(
        (
            "Crest Slot: Architect (Blue 1)",
            "Crest Slot: Architect (Yellow 1)",
            "Crest Slot: Architect (Yellow 2)",
            "Crest Slot: Architect (Blue 2)",
        )
    ),
    "Crest: Shaman": frozenset(
        (
            "Crest Slot: Shaman (Blue 1)",
            "Crest Slot: Shaman (Blue 2)",
        )
    ),
}


ACT_ONE_EXCLUDED_LOCATION_NAMES = (
    _POST_ACT_ONE_SOURCE_LOCATION_NAMES
    | _POST_ACT_ONE_RELIC_TURN_IN_LOCATION_NAMES
    | _POST_ACT_ONE_ROOM_GRAPH_LOCATION_NAMES
    | _ACT_ONE_DEPENDENCY_EXCLUDED_LOCATION_NAMES
)


def get_act_one_excluded_location_names(
    major_key_mode: str = "vanilla",
    boss_mode: str = "anywhere",
    donation_tool_pouch_requirements: Mapping[str, int] | None = None,
    starting_crest_item: str | None = None,
) -> frozenset[str]:
    if major_key_mode not in {"vanilla", "anywhere"}:
        raise ValueError(
            f"Unknown Major Key randomization mode: {major_key_mode!r}"
        )
    if boss_mode not in {"vanilla", "anywhere"}:
        raise ValueError(f"Unknown Boss Sanity mode: {boss_mode!r}")

    requirements = donation_tool_pouch_requirements or {}
    if any(requirement < 0 for requirement in requirements.values()):
        raise ValueError("Tool Pouch requirements cannot be negative")

    excluded = ACT_ONE_EXCLUDED_LOCATION_NAMES - (
        _POST_ACT_ONE_CREST_SLOT_LOCATION_NAMES_BY_CREST.get(
            starting_crest_item,
            frozenset(),
        )
    )
    if starting_crest_item in excluded:
        excluded |= HUNTER_CREST_SLOT_LOCATION_NAMES
    if (
        requirements.get(_BONE_BOTTOM_REPAIRS_LOCATION_NAME, 0)
        > ACT_ONE_TOOL_POUCH_SUPPLY
    ):
        excluded |= frozenset(
            (
                _BONE_BOTTOM_REPAIRS_LOCATION_NAME,
                _LIFESAVING_BRIDGE_LOCATION_NAME,
            )
        )
    elif (
        requirements.get(_LIFESAVING_BRIDGE_LOCATION_NAME, 0)
        > ACT_ONE_TOOL_POUCH_SUPPLY
    ):
        excluded |= frozenset((_LIFESAVING_BRIDGE_LOCATION_NAME,))
    eva_points = sum(
        free + sum(
            f"Crest Slot: {crest.removeprefix('Crest: ')} ({slot})" not in excluded
            for slot in slots
        )
        for crest, (free, slots) in EVA_CREST_SLOTS.items()
        if crest not in excluded or crest == starting_crest_item
    )
    excluded |= frozenset(
        name for name, (_, _, points) in EVA_REWARDS.items()
        if points > eva_points
    )
    return excluded
