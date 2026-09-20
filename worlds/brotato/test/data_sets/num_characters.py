from dataclasses import dataclass
from typing import Any

from ...constants import ABYSSAL_TERRORS_CHARACTERS, BASE_GAME_CHARACTERS, MAX_REQUIRED_RUN_WINS
from .base import BrotatoTestDataSet


@dataclass(frozen=True)
class NumCharactersTestDataSet(BrotatoTestDataSet):
    num_characters: int

    @property
    def test_name(self) -> str:
        return f"num_characters={self.num_characters}"

    @property
    def options_dict(self) -> dict[str, Any]:
        return {
            "num_characters": self.num_characters,
            "num_victories": min(self.num_characters, MAX_REQUIRED_RUN_WINS),
            # Include all characters for simplicity, the num_characters/num_victories above will ensure only the correct
            # amount is chosen.
            "enable_abyssal_terrors_dlc": True,
            "include_base_game_characters": BASE_GAME_CHARACTERS.characters,
            "include_abyssal_terrors_characters": ABYSSAL_TERRORS_CHARACTERS.characters,
        }


NUM_CHARACTERS_DATA_SETS: list[NumCharactersTestDataSet] = [
    NumCharactersTestDataSet(num_characters=n + 1) for n in range(MAX_REQUIRED_RUN_WINS)
]
