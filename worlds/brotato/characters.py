import random
from collections.abc import Sequence
from typing import NamedTuple

from Options import OptionError

from .constants import (
    ABYSSAL_TERRORS_CHARACTERS,
    ALL_CHARACTERS,
    BASE_GAME_CHARACTERS,
    CHARACTER_GROUPS,
    PRIMAL_DREAD_CHARACTERS,
    CharacterGroup,
)
from .options import StartingCharacters


class CharacterGroupInfo(NamedTuple):
    enabled: bool
    include_characters: set[str]
    group: CharacterGroup


class CharacterInfoOutput(NamedTuple):
    available_characters: list[str]
    starting_characters: list[str]


def get_available_and_starting_characters(
    include_base_game_characters: set[str],
    enable_abyssal_terrors_dlc: bool,
    enable_primal_dread_dlc: bool,
    include_abyssal_terrors_characters: set[str],
    include_primal_dread_characters: set[str],
    starting_character_mode: StartingCharacters,
    num_starting_characters: int,
    num_characters: int,
    random: random.Random,
) -> CharacterInfoOutput:
    character_pack_info: dict[str, CharacterGroupInfo] = {
        BASE_GAME_CHARACTERS.name: CharacterGroupInfo(
            enabled=True,
            include_characters=include_base_game_characters,
            group=BASE_GAME_CHARACTERS,
        ),
        ABYSSAL_TERRORS_CHARACTERS.name: CharacterGroupInfo(
            enabled=enable_abyssal_terrors_dlc,
            include_characters=include_abyssal_terrors_characters,
            group=ABYSSAL_TERRORS_CHARACTERS,
        ),
        PRIMAL_DREAD_CHARACTERS.name: CharacterGroupInfo(
            enabled=enable_primal_dread_dlc,
            include_characters=include_primal_dread_characters,
            group=PRIMAL_DREAD_CHARACTERS,
        ),
    }

    valid_characters: set[str] = set()
    for pack_enabled, include_characters_from_pack, pack_characters in character_pack_info.values():
        if pack_enabled:
            valid_characters |= {c for c in pack_characters.characters if c in include_characters_from_pack}

    # Pick characters from the starting character pool first, then add more others until we have the requested amount.
    all_starting_characters_for_option: list[str] = get_starting_characters_for_option(
        starting_character_mode, enable_abyssal_terrors_dlc, enable_primal_dread_dlc
    )
    valid_starting_characters: list[str] = [
        char for char in all_starting_characters_for_option if char in valid_characters
    ]
    if not valid_starting_characters:
        options_str = ", ".join(
            [
                f"{enable_abyssal_terrors_dlc=}",
                f"{starting_character_mode=}",
                f"{num_starting_characters=}",
                f"{include_base_game_characters=}",
                # Put these two last because they can generate very long entries
                f"{num_characters=}",
                f"{include_abyssal_terrors_characters=}",
            ]
        )
        raise OptionError(f"No valid starting characters for given options: {options_str}")

    num_starting_characters_to_select = min(num_starting_characters, len(valid_starting_characters), num_characters)
    starting_characters: list[str] = random.sample(valid_starting_characters, num_starting_characters_to_select)

    included_characters: list[str] = starting_characters.copy()
    num_characters_to_add = num_characters - len(included_characters)
    if num_characters_to_add > 0:
        valid_characters_to_add = sorted(valid_characters - set(starting_characters))
        num_characters_to_sample = min(num_characters_to_add, len(valid_characters_to_add))
        included_characters += random.sample(valid_characters_to_add, num_characters_to_sample)
    return CharacterInfoOutput(available_characters=included_characters, starting_characters=starting_characters)


def get_starting_characters_for_option(
    starting_character_mode: StartingCharacters,
    enable_abyssal_terrors_dlc: bool,
    enable_primal_dread_dlc: bool,
) -> list[str]:
    """Returns a sorted list of the possible starting characters for the given starting character mode.

    This naively returns ALL characters for the mode, ignoring the include_*_characters options. It's assumed that the
    caller will filter the output list down to what's allowed from the other options.

    Returns a sorted list of the valid starting characters. The output is sorted to guarantee deterministic random
    selection.
    """
    starting_characters: Sequence[str]
    match starting_character_mode.value:
        case StartingCharacters.option_default_all:
            starting_characters = [char for group in CHARACTER_GROUPS.values() for char in group.default_characters]
        case StartingCharacters.option_random_all:
            starting_characters = ALL_CHARACTERS
        case StartingCharacters.option_default_base_game:
            starting_characters = BASE_GAME_CHARACTERS.default_characters
        case StartingCharacters.option_random_base_game:
            starting_characters = BASE_GAME_CHARACTERS.characters
        case StartingCharacters.option_default_abyssal_terrors:
            if not enable_abyssal_terrors_dlc:
                raise OptionError(
                    f"Starting option set to {starting_character_mode}, but Abyssal Terrors DLC is disabled."
                )
            starting_characters = ABYSSAL_TERRORS_CHARACTERS.default_characters
        case StartingCharacters.option_random_abyssal_terrors:
            if not enable_abyssal_terrors_dlc:
                raise OptionError(
                    f"Starting option set to {starting_character_mode}, but Abyssal Terrors DLC is disabled."
                )
            starting_characters = ABYSSAL_TERRORS_CHARACTERS.characters

        case StartingCharacters.option_default_primal_dread:
            if not enable_primal_dread_dlc:
                raise OptionError(
                    f"Starting option set to {starting_character_mode}, but Primal Dread DLC is disabled."
                )
            starting_characters = PRIMAL_DREAD_CHARACTERS.default_characters
        case StartingCharacters.option_random_primal_dread:
            if not enable_primal_dread_dlc:
                raise OptionError(
                    f"Starting option set to {starting_character_mode}, but Primal Dread DLC is disabled."
                )
            starting_characters = PRIMAL_DREAD_CHARACTERS.characters

        case _:
            raise OptionError(f"Unknown value for starting character option: {starting_character_mode}")

    return sorted(starting_characters)
