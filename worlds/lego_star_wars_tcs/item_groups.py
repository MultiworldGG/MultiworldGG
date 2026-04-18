from typing import Mapping, Sequence

from .constants import CharacterAbility
from .items import (
    CHARACTERS_AND_VEHICLES_BY_NAME,
    GenericCharacterData,
    EXTRAS_BY_NAME,
    MINIKITS_BY_COUNT,
    CHAPTER_UNLOCKS,
)
from .levels import CHAPTER_AREA_STORY_CHARACTERS, CHAPTER_AREAS


def _ability_to_character() -> Mapping[CharacterAbility, Sequence[GenericCharacterData]]:
    ability_to_character: dict[CharacterAbility, list[GenericCharacterData]] = {}
    for char in CHARACTERS_AND_VEHICLES_BY_NAME.values():
        for ability in char.abilities:
            ability_to_character.setdefault(ability, []).append(char)
    return {k: tuple(v) for k, v in ability_to_character.items()}


ABILITY_TO_CHARACTERS: Mapping[CharacterAbility, Sequence[GenericCharacterData]] = _ability_to_character()
# ABILITY_TO_CHARACTER_NAMES: Mapping[CharacterAbility, Sequence[str]] = {
#     ability: tuple(char.name for char in characters) for ability, characters in ABILITY_TO_CHARACTERS.items()
# }


def _ability_to_readable(ability: CharacterAbility) -> str:
    return ability.name.replace("_", " ").title() + " Characters"  # type: ignore # (.name is str | None)


ITEM_GROUPS: dict[str, set[str]] = {
    **{_ability_to_readable(ability): {c.name for c in characters if c.is_sendable}
       for ability, characters in ABILITY_TO_CHARACTERS.items()},
    "No Abilities Characters": {name for name, c in CHARACTERS_AND_VEHICLES_BY_NAME.items()
                                if c.is_sendable and c.abilities is CharacterAbility.NONE},
    "Non-Vehicle Characters": {c.name for c in CHARACTERS_AND_VEHICLES_BY_NAME.values()
                               if c.item_type == "Character" and c.is_sendable},
    "Vehicle Characters": {v.name for v in CHARACTERS_AND_VEHICLES_BY_NAME.values()
                           if v.item_type == "Vehicle" and v.is_sendable},
    **{
        f"{chapter.short_name} Story Unlock Characters": set(chapter.character_requirements)
        for chapter in CHAPTER_AREAS
    },
    **{
        f"{chapter.short_name} Purchase Unlock Characters": set(chapter.alt_character_requirements)
        for chapter in CHAPTER_AREAS if chapter.alt_character_requirements
    },
    "Characters": {c.name for c in CHARACTERS_AND_VEHICLES_BY_NAME.values() if c.is_sendable},
    "Extras": {e.name for e in EXTRAS_BY_NAME.values() if e.is_sendable} | {"Progressive Score Multiplier"},
    "Minikits": {m.name for m in MINIKITS_BY_COUNT.values() if m.is_sendable},
    "Episode Unlocks": {f"Episode {i} Unlock" for i in "123456"},
    "Chapter Unlocks": {data.name for data in CHAPTER_UNLOCKS},
    "Junk": {
        "Silver Stud",
        "Gold Stud",
        "Blue Stud",
        "Purple Stud",
        "Power Up",
    },
}
