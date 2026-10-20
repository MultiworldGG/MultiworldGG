"""Act 2 goal content exclusions.

The table maps physical sources unavailable before the Act 2 ending to AP
location names. Shared locations remain when at least one source is available
before that ending.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable, Mapping

from .eva import EVA_CREST_SLOTS, EVA_REWARDS

from .lore_tablets import (
    LORE_TABLET_ACT_THREE_LOCATION_NAMES,
    LORE_TABLET_ITEM_BY_LOCATION,
)


ACT_TWO_GOAL_KEY = "act_2"
CURSED_ENDING_GOAL_KEY = "cursed_ending"

# These sources are reserved for Act 3 content scopes.
ACT_THREE_ONLY_GOAL_LOCATION_NAMES: frozenset[str] = frozenset(
    (
        "Bellhart Roof - Memory Locket",
        "Pollen Heart",
        "Everbloom",
        "Sprintmaster's Memento",
        "Guardian's Memento",
        "Hero's Memento",
        'Surface Memento',
        'Craw Memento',
        "Hunter's Heart",
        "Encrusted Heart",
        "Conjoined Heart",
        "Cogwork Core - Pristine Core",
        "Curvesickle",
        "Wish: Fatal Resolve",
        "Wish: Hero's Call",
        "Wish: Pain, Anguish and Misery",
        "Wish: Survivor's Camp Supplies",
        "Boss: Bell Eater",
        "Beastling Call",
        "Boss: Plasmified Zango",
        "Boss: Lost Garmond",
        "Boss: Pinstress",
        "Boss: Shrine Guardian Seth",
        "Boss: Watcher at the Edge",
    )
)

# Canonical AP locations whose physical sources are unavailable before the
# Act 2 ending. Two source-level exceptions apply:
#
# * Silk Soar's Abyss source leaves, but its item is not listed in the
#   pool-removal table. The pool builder keeps it only in Anywhere when
#   unrestricted filler can make room for it.
# * The Cradle - Map Purchase remains because Cradle_02 is a valid Act 2 source.
#   Tube_Hub is only the same check's post-Act-3 fallback.
#
# Runtfeast has no separate AP Wish location.  It shares the canonical
# Longclaw check with Act 2 Broodfeast, so that shared location remains.
ACT_TWO_HAND_TESTED_UNAVAILABLE_LOCATION_NAMES: frozenset[str] = frozenset(
    (
        "Boss: Grand Mother Silk",
        "Silk Soar",
        "Pale Nails",
        "Pin Badge",
        "Brightvein - Mask Shard",
        "Relic: Rune Harp (High Halls)",
        "Far Fields - Pale Rosary Necklace",
        "Elegy of the Deep",
        "Craw Summons",
        "Boss: Crawfather",
        'Greymoor - craw court rosary vault stash',
        'Greymoor - the other craw court rosary vault stash',
        'Greymoor - the final craw court rosary vault stash',
        "Crest: Shaman",
        "Relic: Arcane Egg",
        "The Abyss - Map Pickup",
        "Verdania - Map Pickup",
        "The Abyss - Shell Shard Cache #1",
        "The Abyss - Shell Shard Cache #2",
        "The Abyss - Shell Shard Cache #3",
        "The Abyss - Shell Shard Cache #4",
        "The Abyss - Shell Shard Cache #5",
        "The Abyss - Shell Shard Cache #6",
        "The Abyss - Shell Shard Cache #7",
        "The Abyss - Shell Shard Cache #8",
        "The Abyss - Shell Shard Cache #9",
        "Far Fields - Rosary Cache #19",
        "Boss: Skarrsinger Karmelita",
        "Boss: Crust King Khann",
        "Boss: Nyleth",
        "Boss: Tormented Trobbio",
        "Boss: Gurr the Outcast",
        "Boss: Clover Dancers",
        "Boss: Palestag",
        "Dark Mirror",
        "The Hidden Hunter - Mask Shard",
        "Dark Hearts - Mask Shard",
        "The Cradle - Silkeater",
        "Wish: Passing of the Age",
        "Wish: Advanced Alchemy",
        "Ecstasy of the End - Pale Oil",
        "Pinmaster Plinney: Pale Steel Needle",
        *LORE_TABLET_ACT_THREE_LOCATION_NAMES,
    )
)

ACT_TWO_REQUIRED_DEPENDENCY_LOCATION_NAMES: frozenset[str] = frozenset(
    (
        "Relic Turn-in: Arcane Egg",
        "Relic Turn-in: Rune Harp (High Halls)",
    )
)

ACT_TWO_EXCLUDED_LOCATION_NAMES: frozenset[str] = (
    ACT_TWO_HAND_TESTED_UNAVAILABLE_LOCATION_NAMES
    | ACT_TWO_REQUIRED_DEPENDENCY_LOCATION_NAMES
    | ACT_THREE_ONLY_GOAL_LOCATION_NAMES
)
ACT_TWO_SHAMAN_SLOT_LOCATION_NAMES: frozenset[str] = frozenset(
    (
        "Crest Slot: Shaman (Blue 1)",
        "Crest Slot: Shaman (Blue 2)",
    )
)



ACT_TWO_SILK_SOAR_LOCATION_NAMES: frozenset[str] = frozenset((
    "Grey Memento",
    "Whispering Vaults - Mask Shard",
    "Whispering Vaults - Shard Bundle",
    *(f"Far Fields - Rosary Cache #{number}" for number in (18, 20, 21)),
    *(f"Far Fields - Shell Shard Cache #{number}" for number in range(2, 8)),
    "Grand Gate - Shell Shard Cache",
    "Mount Fay - Shell Shard Cache #3",
    "Mount Fay - Shell Shard Cache #4",
    "Putrified Ducts - Shell Shard Cache #8",
    *(f"Underworks - Shell Shard Cache #{number}" for number in (7, 8, 11)),
    "Far Fields (Act 3) - Memory Locket",
))


CURSED_ENDING_WITCH_SLOT_LOCATION_NAMES = frozenset((
    "Crest Slot: Witch (Red 1)",
    "Crest Slot: Witch (Blue 1)",
    "Crest Slot: Witch (Blue 2)",
))


def get_act_two_excluded_location_names(
    starting_crest_item: str | None,
    skill_mode: str = "anywhere",
    cursed_ending: bool = False,
    silk_soar_begone: bool = False,
    retained_items: tuple[str, ...] = (),
) -> frozenset[str]:
    """Exclude later-act sources in every Skill randomization mode."""

    excluded = ACT_TWO_EXCLUDED_LOCATION_NAMES
    if starting_crest_item != "Crest: Shaman" and "Crest: Shaman" not in retained_items:
        excluded |= ACT_TWO_SHAMAN_SLOT_LOCATION_NAMES

    if skill_mode not in {"vanilla", "anywhere"}:
        raise ValueError(f"Unknown Skill randomization mode: {skill_mode!r}")
    if skill_mode != "anywhere" or silk_soar_begone:
        excluded |= ACT_TWO_SILK_SOAR_LOCATION_NAMES
    if cursed_ending:
        excluded |= {"Crest: Witch"}
        if starting_crest_item != "Crest: Witch":
            excluded |= CURSED_ENDING_WITCH_SLOT_LOCATION_NAMES
    if cursed_ending:
        points = sum(
            free + sum(f"Crest Slot: {crest.removeprefix('Crest: ')} ({slot})" not in excluded for slot in slots)
            for crest, (free, slots) in EVA_CREST_SLOTS.items()
            if crest not in excluded or crest == starting_crest_item or crest in retained_items
        )
        excluded |= {name for name, (_, _, required) in EVA_REWARDS.items() if required > points}
    return excluded


# Pool entries carry their source lane, so repeated identities can be removed
# without touching identical rewards belonging to a different category.  The
# Boss, Quest and RelicTurnIn checks use generic filler rather than a native
# item identity. Their lane reductions remove the same number of copies.
ACT_TWO_POOL_REMOVALS_BY_SOURCE_CATEGORY: Mapping[
    str,
    Mapping[str, int],
] = {
    "OldHeart": {"Pollen Heart": 1, "Hunter's Heart": 1, "Encrusted Heart": 1, "Conjoined Heart": 1},
    "Everbloom": {"Everbloom": 1},
    "Memento": {"Sprintmaster's Memento": 1, "Guardian's Memento": 1, "Hero's Memento": 1, 'Surface Memento': 1, 'Craw Memento': 1},
    "Map": {
        "Map: The Abyss": 1,
        "Map: Verdania": 1,
    },
    "Relic": {
        "Relic: Arcane Egg": 1,
        "Relic: Rune Harp (High Halls)": 1,
    },
    "Resource:pristine_core": {"Pristine Core": 1},
    "Tool": {"Progressive Claw Mirror": 1, "Progressive Curveclaw": 1, "Pin Badge": 1},
    "Spell": {"Pale Nails": 1},
    "Melody": {"Elegy of the Deep": 1, "Beastling Call": 1},
    "MemoryLocket": {"Memory Locket": 1},
    "MajorKey": {"Craw Summons": 1},
    "Resource:pale_rosary_necklace": {"Pale Rosary Necklace": 1},
    "MaskShard": {"Mask Shard": 3},
    "Silkeater": {"Silkeater": 1},
    "NeedleUpgrade": {"Progressive Needle Upgrade": 1},
    "PaleOil": {"Pale Oil": 1},
    "Resource:rosary_cache": {"Rosaries (10)": 4},
    "Resource:shell_shard_cache": {"Shell Shards (10)": 9},
    "Boss": {
        "Rosaries (60)": 9,
        "Shell Shards (80)": 6,
    },
    "Quest": {
        "Rosaries (60)": 3,
        "Shell Shards (80)": 2,
    },
    "RelicTurnIn": {"Shell Shards (80)": 2},
    "LoreTablet": {
        LORE_TABLET_ITEM_BY_LOCATION[location_name]: 1
        for location_name in LORE_TABLET_ACT_THREE_LOCATION_NAMES
    },
}


def trim_act_two_pool_entries(
    entries: Iterable,
    starting_crest_item: str | None,
    skill_mode: str = "anywhere",
    cursed_ending: bool = False,
    silk_soar_begone: bool = False,
    retained_items: tuple[str, ...] = (),
):
    remaining = list(entries)
    removals = {
        category: Counter(item_counts)
        for category, item_counts in
        ACT_TWO_POOL_REMOVALS_BY_SOURCE_CATEGORY.items()
    }
    if skill_mode != "anywhere" or silk_soar_begone:
        for category, item_counts in {
            "Memento": {"Grey Memento": 1},
            "MaskShard": {"Mask Shard": 1},
            "MemoryLocket": {"Memory Locket": 1},
            "Resource:shard_bundle": {"Shard Bundle": 1},
            "Resource:rosary_cache": {"Rosaries (10)": 3},
            "Resource:shell_shard_cache": {"Shell Shards (10)": 13},
        }.items():
            removals.setdefault(category, Counter()).update(item_counts)
    if starting_crest_item == "Crest: Shaman":
        removals.setdefault("Crest", Counter())["Crest: Hunter"] += 1
    else:
        removals.setdefault("Crest", Counter())["Crest: Shaman"] += 1
        if "Crest: Shaman" not in retained_items:
            removals.setdefault("CrestSlot", Counter()).update(
                {item_name: 1 for item_name in ACT_TWO_SHAMAN_SLOT_LOCATION_NAMES}
            )

    if cursed_ending:
        item = "Crest: Hunter" if starting_crest_item == "Crest: Witch" else "Crest: Witch"
        removals.setdefault("Crest", Counter())[item] += 1
        if starting_crest_item != "Crest: Witch":
            removals.setdefault("CrestSlot", Counter()).update(
                {name: 1 for name in CURSED_ENDING_WITCH_SLOT_LOCATION_NAMES})

    if cursed_ending:
        excluded = get_act_two_excluded_location_names(
            starting_crest_item, skill_mode, cursed_ending, silk_soar_begone, retained_items)
        removals.setdefault("Eva", Counter()).update(
            reward for name, (reward, _, _) in EVA_REWARDS.items() if name in excluded)

    for source_category, item_counts in removals.items():
        if not any(
            entry.source_category == source_category
            for entry in remaining
        ):
            continue
        for item_name, count in item_counts.items():
            for _copy_index in range(count):
                entry_index = next(
                    (
                        index
                        for index, entry in enumerate(remaining)
                        if (
                            entry.source_category == source_category
                            and entry.name == item_name
                        )
                    ),
                    None,
                )
                if entry_index is None:
                    raise ValueError(
                        "Act 2 content trim could not remove "
                        f"{item_name!r} from the active "
                        f"{source_category!r} pool lane."
                    )
                remaining.pop(entry_index)
    return tuple(remaining)
