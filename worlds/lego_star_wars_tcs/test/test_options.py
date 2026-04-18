from typing import Iterable
from unittest import TestCase

from Options import Option, PerGameCommonOptions, VerifyKeys

from ..items import CHARACTERS_AND_VEHICLES_BY_NAME, EXTRAS_BY_NAME
from ..options import (
    LegoStarWarsTCSOptions,
    ChapterStoryUnlockCharactersNotRequired,
    PreferredCharacters,
    PreferredExtras,
)


BASE_OPTIONS = PerGameCommonOptions.type_hints
TCS_OPTIONS = {k: v for k, v in LegoStarWarsTCSOptions.type_hints.items() if k not in BASE_OPTIONS}


class TestOptions(TestCase):
    def test_options_have_display_name(self) -> None:
        """Test that all options have display_name set. display_name is used by webhost."""
        option_type: type[Option]
        for option_name, option_type in TCS_OPTIONS.items():
            with self.subTest(option_name):
                self.assertTrue(hasattr(option_type, "display_name"))

    def test_options_use_rich_text_doc(self) -> None:
        """Test that all options use rich_text_doc. This displays newlines better and allows for formatting."""
        option_type: type[Option]
        for option_name, option_type in TCS_OPTIONS.items():
            with self.subTest(option_name):
                self.assertTrue(option_type.rich_text_doc)

    def _test_valid_keys(self, all_keys: Iterable[str], *options: type[VerifyKeys]):
        all_keys_set = set(all_keys)
        for option in options:
            with self.subTest(option.__name__):
                self.assertLessEqual(set(option.valid_keys), all_keys_set)

    def test_character_valid_keys(self):
        self._test_valid_keys(
            CHARACTERS_AND_VEHICLES_BY_NAME.keys(),
            ChapterStoryUnlockCharactersNotRequired,
            PreferredCharacters,
        )

    def test_extra_valid_keys(self):
        self._test_valid_keys(EXTRAS_BY_NAME.keys(), PreferredExtras)
