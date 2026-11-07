from dataclasses import dataclass, field
from typing import Any

from Options import OptionError

from ...constants import (
    ABYSSAL_TERRORS_CHARACTERS,
    ALL_CHARACTERS,
    BASE_GAME_CHARACTERS,
    PRIMAL_DREAD_CHARACTERS,
    TOTAL_NUM_CHARACTERS,
)
from ...options import StartingCharacters
from .base import BrotatoTestDataSet

BASE_GAME_CHARACTERS_SET = set(BASE_GAME_CHARACTERS.characters)
BASE_GAME_DEFAULT_CHARACTERS_SET = set(BASE_GAME_CHARACTERS.default_characters)
ABYSSAL_TERRORS_CHARACTERS_SET = set(ABYSSAL_TERRORS_CHARACTERS.characters)
ABYSSAL_TERRORS_DEFAULT_CHARACTERS_SET = set(ABYSSAL_TERRORS_CHARACTERS.default_characters)
PRIMAL_DREAD_CHARACTERS_SET = set(PRIMAL_DREAD_CHARACTERS.characters)
PRIMAL_DREAD_DEFAULT_CHARACTERS_SET = set(PRIMAL_DREAD_CHARACTERS.default_characters)


@dataclass(frozen=True)
class BrotatoCharacterOptionDataSet(BrotatoTestDataSet):
    # World option equivalents
    include_base_game_characters: set[str]
    enable_abyssal_terrors_dlc: bool
    include_abyssal_terrors_characters: set[str]
    starting_characters_mode: StartingCharacters
    num_starting_characters: int
    num_include_characters: int
    # Expected values
    valid_starting_characters: set[str]
    valid_available_characters: set[str]
    expected_exception: type[Exception] | None = None
    # Metadata
    description: str = ""

    # Primal Dread DLC Character options, appearing later because datasets require it.+
    enable_primal_dread_dlc: bool = False
    include_primal_dread_characters: set[str] = field(default_factory=PRIMAL_DREAD_CHARACTERS_SET.copy)

    @property
    def test_name(self) -> str:
        if self.description:
            return self.description
        return str(self)

    @property
    def options_dict(self) -> dict[str, Any]:
        return {
            "include_base_game_characters": self.include_base_game_characters,
            "enable_abyssal_terrors_dlc": self.enable_abyssal_terrors_dlc,
            "include_abyssal_terrors_characters": self.include_abyssal_terrors_characters,
            "starting_characters_mode": self.starting_characters_mode,
            "num_starting_characters": self.num_starting_characters,
            "num_include_characters": self.num_include_characters,
        }


CHARACTER_TEST_DATA_SETS = [
    BrotatoCharacterOptionDataSet(
        description="Check that starting characters are selected properly from default characters",
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=False,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_default_base_game),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        num_include_characters=20,
        valid_starting_characters=BASE_GAME_DEFAULT_CHARACTERS_SET,
        valid_available_characters=BASE_GAME_CHARACTERS_SET,
    ),
    BrotatoCharacterOptionDataSet(
        description="Check that starting characters are selected from base game characters",
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=False,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_default_base_game),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        num_include_characters=20,
        valid_starting_characters=BASE_GAME_CHARACTERS_SET,
        valid_available_characters=BASE_GAME_CHARACTERS_SET,
    ),
    BrotatoCharacterOptionDataSet(
        description="Check that starting characters are selected from all characters (with only base game enabled)",
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=False,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_default_base_game),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        num_include_characters=20,
        valid_starting_characters=BASE_GAME_CHARACTERS_SET,
        valid_available_characters=BASE_GAME_CHARACTERS_SET,
    ),
    BrotatoCharacterOptionDataSet(
        description="Check that more requested characters than included characters is handled correctly.",
        include_base_game_characters=set(BASE_GAME_CHARACTERS.characters[:10]),
        enable_abyssal_terrors_dlc=False,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_default_base_game),
        num_starting_characters=3,
        num_include_characters=TOTAL_NUM_CHARACTERS,  # If we did something wrong, this should ensure the test fails
        valid_starting_characters=set(BASE_GAME_CHARACTERS.characters[:10]),
        valid_available_characters=set(BASE_GAME_CHARACTERS.characters[:10]),
    ),
    BrotatoCharacterOptionDataSet(
        description="Check that setting starting characters to AT default characters with DLC disabled raises error.",
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=False,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_default_abyssal_terrors),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        num_include_characters=20,
        valid_starting_characters=set(),
        valid_available_characters=set(),
        expected_exception=OptionError,
    ),
    BrotatoCharacterOptionDataSet(
        description="Check that setting starting characters to AT characters with DLC disabled raises error.",
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=False,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_random_abyssal_terrors),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        num_include_characters=20,
        valid_starting_characters=set(),
        valid_available_characters=set(),
        expected_exception=OptionError,
    ),
    BrotatoCharacterOptionDataSet(
        description="Check that setting starting characters to AT characters with no AT characters included raises error.",  # noqa
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=True,
        include_abyssal_terrors_characters=set(),
        starting_characters_mode=StartingCharacters(StartingCharacters.option_random_abyssal_terrors),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        num_include_characters=20,
        valid_starting_characters=set(),
        valid_available_characters=set(),
        expected_exception=OptionError,
    ),
    BrotatoCharacterOptionDataSet(
        description="Check that even with DLC enabled, no AT characters are added if none are included.",
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=True,
        include_abyssal_terrors_characters=set(),
        starting_characters_mode=StartingCharacters(StartingCharacters.option_random_all),
        num_starting_characters=10,
        num_include_characters=20,
        valid_starting_characters=BASE_GAME_CHARACTERS_SET,
        valid_available_characters=BASE_GAME_CHARACTERS_SET,
    ),
    BrotatoCharacterOptionDataSet(
        description="Abyssal Terrors DLC enabled, starting characters are AT default characters",
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=True,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_default_abyssal_terrors),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        num_include_characters=20,
        valid_starting_characters=ABYSSAL_TERRORS_DEFAULT_CHARACTERS_SET,
        valid_available_characters=set(ALL_CHARACTERS),
    ),
    BrotatoCharacterOptionDataSet(
        description="Abyssal Terrors DLC enabled, starting characters are any AT characters",
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=True,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_random_abyssal_terrors),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        num_include_characters=20,
        valid_starting_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        valid_available_characters=set(ALL_CHARACTERS),
    ),
    BrotatoCharacterOptionDataSet(
        description="Abyssal Terrors DLC enabled, starting characters are any characters",
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=True,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_random_all),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        num_include_characters=20,
        valid_starting_characters=set(ALL_CHARACTERS),
        valid_available_characters=set(ALL_CHARACTERS),
    ),
    BrotatoCharacterOptionDataSet(
        description="Abyssal Terrors DLC enabled, starting characters are any default characters, include all chars",
        include_base_game_characters=BASE_GAME_CHARACTERS_SET,
        enable_abyssal_terrors_dlc=True,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_default_all),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        # Assures all default characters are selected to prevent false positives
        num_include_characters=TOTAL_NUM_CHARACTERS,
        valid_starting_characters=BASE_GAME_DEFAULT_CHARACTERS_SET | ABYSSAL_TERRORS_DEFAULT_CHARACTERS_SET,
        valid_available_characters=set(ALL_CHARACTERS),
    ),
    BrotatoCharacterOptionDataSet(
        description="Abyssal Terrors DLC enabled, no base game characters",
        include_base_game_characters=set(),
        enable_abyssal_terrors_dlc=True,
        include_abyssal_terrors_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        starting_characters_mode=StartingCharacters(StartingCharacters.option_default_all),
        num_starting_characters=BASE_GAME_CHARACTERS.num_default_characters,
        # Assures all default characters are selected to prevent false positives
        num_include_characters=20,
        valid_starting_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
        valid_available_characters=ABYSSAL_TERRORS_CHARACTERS_SET,
    ),
]

NON_ERROR_CHARACTER_TEST_DATA_SETS = [ds for ds in CHARACTER_TEST_DATA_SETS if ds.expected_exception is None]
ERROR_CHARACTER_TEST_DATA_SETS = [ds for ds in CHARACTER_TEST_DATA_SETS if ds.expected_exception is not None]
