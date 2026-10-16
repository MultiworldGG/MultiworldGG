from __future__ import annotations

from random import Random
from typing import Callable, Mapping, Protocol, TypeVar

from Options import OptionError


SPELLING_BEE_GOAL_KEY = "spelling_bee"
ALPHABET_ITEM_CATEGORY = "Alphabet"
ALPHABET_ITEM_NAMES: tuple[str, ...] = tuple(
    f"Letter: {letter}"
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)
ALPHABET_ITEM_ROWS: tuple[tuple[str, str], ...] = tuple(
    (item_name, ALPHABET_ITEM_CATEGORY)
    for item_name in ALPHABET_ITEM_NAMES
)
ALPHABET_ITEM_COUNT = len(ALPHABET_ITEM_NAMES)


def parse_spelling_bee_phrase(
    value: object,
) -> tuple[str, tuple[str, ...]] | None:
    if not isinstance(value, str):
        return None
    if any(
        character not in " ,.!?"
        and not (
            "A" <= character <= "Z"
            or "a" <= character <= "z"
        )
        for character in value
    ):
        return None

    phrase = " ".join(value.split())
    if not phrase:
        return None

    item_names = []
    seen_letters = set()
    for character in phrase:
        if character in " ,.!?":
            continue
        letter = character.upper()
        if letter in seen_letters:
            continue
        seen_letters.add(letter)
        item_names.append(f"Letter: {letter}")
    return (phrase, tuple(item_names)) if item_names else None


class PoolEntry(Protocol):
    name: str
    source_category: str
    placement_category: str | None


PoolEntryType = TypeVar("PoolEntryType", bound=PoolEntry)


def replace_filler_with_alphabet_items(
    entries: list[PoolEntryType],
    is_filler: Callable[[str], bool],
    randomizer: Random | None = None,
    max_replacements_by_placement_category: (
        Mapping[str | None, int] | None
    ) = None,
    replacement_is_advancement: Callable[[str], bool] | None = None,
) -> None:
    eligible_indices = [
        index
        for index, entry in enumerate(entries)
        if is_filler(entry.name)
    ]
    if len(eligible_indices) < ALPHABET_ITEM_COUNT:
        raise OptionError(
            "alphabet_mode needs 26 filler rewards in the configured "
            f"random pool but only {len(eligible_indices)} are available. "
            "Enable more filler-bearing checks such as Boss Sanity, Wish "
            "Sanity, Lore Tablets, Rosary Caches or Shell Shard Caches."
        )
    unrestricted_indices = [
        index
        for index in eligible_indices
        if entries[index].placement_category is None
    ]
    restricted_indices = [
        index
        for index in eligible_indices
        if entries[index].placement_category is not None
    ]
    if randomizer is not None:
        randomizer.shuffle(unrestricted_indices)
        randomizer.shuffle(restricted_indices)
    eligible_indices = unrestricted_indices + restricted_indices
    replacements = list(zip(eligible_indices, ALPHABET_ITEM_NAMES))
    if max_replacements_by_placement_category is not None:
        if replacement_is_advancement is None:
            raise ValueError(
                "Alphabet placement capacity needs an item "
                "classification callback."
            )
        eligible_count_by_category: dict[str | None, int] = {}
        for index in eligible_indices:
            category = entries[index].placement_category
            eligible_count_by_category[category] = (
                eligible_count_by_category.get(category, 0) + 1
            )
        safe_capacity = sum(
            min(
                eligible_count,
                max(
                    0,
                    max_replacements_by_placement_category.get(
                        category,
                        0,
                    ),
                ),
            )
            for category, eligible_count
            in eligible_count_by_category.items()
        )
        advancement_item_names = [
            item_name
            for item_name in ALPHABET_ITEM_NAMES
            if replacement_is_advancement(item_name)
        ]
        if safe_capacity < len(advancement_item_names):
            raise OptionError(
                "alphabet_mode needs "
                f"{len(advancement_item_names)} progression-safe filler "
                "rewards "
                "after reserving non-progression rewards for restricted "
                f"locations, but only {safe_capacity} are available. "
                "Enable more filler-bearing checks or use fewer restrictive "
                "shuffle settings."
            )

        advancement_indices = []
        selected_count_by_category: dict[str | None, int] = {}
        for index in eligible_indices:
            if len(advancement_indices) >= len(advancement_item_names):
                break
            category = entries[index].placement_category
            selected_count = selected_count_by_category.get(category, 0)
            if selected_count >= max_replacements_by_placement_category.get(
                category,
                0,
            ):
                continue
            advancement_indices.append(index)
            selected_count_by_category[category] = selected_count + 1
            if len(advancement_indices) == len(advancement_item_names):
                break
        advancement_index_set = set(advancement_indices)
        useful_item_names = [
            item_name
            for item_name in ALPHABET_ITEM_NAMES
            if not replacement_is_advancement(item_name)
        ]
        useful_indices = [
            index
            for index in eligible_indices
            if index not in advancement_index_set
        ][:len(useful_item_names)]
        replacements = [
            *zip(advancement_indices, advancement_item_names),
            *zip(useful_indices, useful_item_names),
        ]
    for entry_index, item_name in replacements:
        replaced_entry = entries[entry_index]
        entries[entry_index] = type(replaced_entry)(
            item_name,
            replaced_entry.source_category,
            replaced_entry.placement_category,
        )
