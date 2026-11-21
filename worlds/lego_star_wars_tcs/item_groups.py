from typing import Mapping, Sequence

from .constants import CharacterAbility
from .data.areas import Area
from .data.items import GenericCharacterData
from .data.items.all_character_items import SENDABLE_CHARACTER_TO_ITEM_DATA
from .data.areas import ALL_CHAPTER_AREAS
from .data.items.extra_items import EXTRA_DATA
from .data.items.generic_items import (
    NonDataItemName,
    EPISODE_UNLOCKS,
    CHAPTER_TO_CHAPTER_UNLOCK_ITEM,
    MINIKITS_BY_BUNDLE_SIZE,
)

_SORTED_CHAPTER_AREAS: list[Area] = sorted(ALL_CHAPTER_AREAS)


def _ability_to_sendable_character() -> Mapping[CharacterAbility, Sequence[GenericCharacterData]]:
    ability_to_character: dict[CharacterAbility, list[GenericCharacterData]] = {}
    for char in SENDABLE_CHARACTER_TO_ITEM_DATA.values():
        for ability in char.abilities:
            ability_to_character.setdefault(ability, []).append(char)
    return {k: tuple(v) for k, v in ability_to_character.items()}


ABILITY_TO_SENDABLE_CHARACTERS: Mapping[CharacterAbility, Sequence[GenericCharacterData]]
ABILITY_TO_SENDABLE_CHARACTERS = _ability_to_sendable_character()
# ABILITY_TO_CHARACTER_NAMES: Mapping[CharacterAbility, Sequence[str]] = {
#     ability: tuple(char.name for char in characters) for ability, characters in ABILITY_TO_CHARACTERS.items()
# }


def ability_to_readable_group(ability: CharacterAbility) -> str:
    return ability.name.replace("_", " ").title() + " Characters"  # type: ignore # (.name is str | None)


REVERSE_READABLE_ABILITY_TO_ABILITY = {ability_to_readable_group(ability): ability for ability in CharacterAbility}


ITEM_GROUPS: dict[str, set[str]] = {
    **{ability_to_readable_group(ability): {c.name for c in characters if c.is_sendable}
       for ability, characters in ABILITY_TO_SENDABLE_CHARACTERS.items()},
    "Non-Vehicle Characters": {c.name for c in SENDABLE_CHARACTER_TO_ITEM_DATA.values()
                               if c.item_type == "Character"},
    "Vehicle Characters": {v.name for v in SENDABLE_CHARACTER_TO_ITEM_DATA.values()
                           if v.item_type == "Vehicle"},
    **{
        f"{chapter.get_short_name()} Story Unlock Characters": {c.readable_name for c in chapter.get_story_characters()}
        for chapter in _SORTED_CHAPTER_AREAS
    },
    **{
        f"{chapter.get_short_name()} Purchase Unlock Characters": {
            c.readable_name for c in chapter.get_purchase_characters()
        } for chapter in _SORTED_CHAPTER_AREAS if chapter.get_purchase_characters()
    },
    "Characters": {c.name for c in SENDABLE_CHARACTER_TO_ITEM_DATA.values()},
    "Extras": {e.name for e in EXTRA_DATA if e.is_sendable} | {NonDataItemName.PROGRESSIVE_SCORE_MULTIPLIER.value},
    "Minikits": {m.name for m in MINIKITS_BY_BUNDLE_SIZE.values()},
    "Episode Unlocks": {name.value for name in EPISODE_UNLOCKS.values()},
    "Chapter Unlocks": set(CHAPTER_TO_CHAPTER_UNLOCK_ITEM.values()),
    "Junk": {
        name.value for name in (
            NonDataItemName.SILVER_STUD,
            NonDataItemName.GOLD_STUD,
            NonDataItemName.BLUE_STUD,
            NonDataItemName.PURPLE_STUD,
            NonDataItemName.POWER_UP,
        )
    }
}
