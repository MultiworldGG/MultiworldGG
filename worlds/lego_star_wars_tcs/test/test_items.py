from unittest import TestCase

from BaseClasses import ItemClassification, CollectionState
from . import LegoStarWarsWorldTestBase
from ..data.characters import UnlockMethod, Character
from ..data.extras import Extra
from ..data.items import GenericCharacterData
from ..data.items.all_character_items import CHARACTER_TO_ITEM_DATA
from ..data.items.extra_items import ExtraData
from ..data.shop import CHARACTER_SHOP_SLOTS
from ..items import ITEM_DATA, CHARACTERS_AND_VEHICLES_BY_NAME
from ..options import get_option_name, LogicDifficulty, StartingChapter, EnabledChaptersCount, AllowedChapters


_MIN_ID = 1
_MAX_ID = 2**53 - 1


class TestItems(TestCase):
    def test_item_code_uniqueness(self):
        found_codes = set()
        for item in ITEM_DATA:
            if not item.is_sendable:
                self.assertIsNone(item.code, f"{item} is an event but has a code")
                continue
            self.assertIsNotNone(item.code, f"{item} is not an event, but does not have a code")
            self.assertGreaterEqual(item.code, _MIN_ID, f"Item codes must be greater than or equal to {_MIN_ID},"
                                                        f" but {item}'s code is {item.code}")
            self.assertLessEqual(item.code, _MAX_ID, f"Item codes must be less than or equal to {_MAX_ID},"
                                                     f" but {item}'s code is {item.code}")
            self.assertNotIn(item.code, found_codes)
            found_codes.add(item.code)

    def test_item_name_uniqueness(self):
        found_names = set()
        for item in ITEM_DATA:
            self.assertNotIn(item.name, found_names)
            found_names.add(item.name)

    def test_character_number_uniqueness(self):
        found_characters = set()
        for item in ITEM_DATA:
            if not isinstance(item, GenericCharacterData):
                continue
            self.assertNotIn(item.character, found_characters, f"Duplicate character {item.character} for {item}")
            if item.character.is_event():
                self.assertIsNone(item.code, f"{item} is an event but has a code")
                self.assertFalse(item.is_sendable, f"{item} is an event, but is sendable")
            else:
                self.assertIsNotNone(item.code, f"{item} is not an event, but does not have a code")
                self.assertTrue(item.is_sendable, f"{item} is not an event, but is not sendable")
            found_characters.add(item.character)

    def test_shop_slots_count(self):
        """Test that there are the correct number of Character shop slots."""
        # The slots are from 0 to 88.
        self.assertEqual(len(CHARACTER_SHOP_SLOTS), 89)

    def test_shop_slots_characters(self):
        for character in CHARACTER_SHOP_SLOTS:
            self.assertIn(character.readable_name, CHARACTERS_AND_VEHICLES_BY_NAME)

    def test_shop_slots_unlocks(self):
        possible_unlocks = {
            UnlockMethod.START,
            UnlockMethod.AREA_COMPLETE,
            UnlockMethod.INDY_TRAILER,
            UnlockMethod.ALL_EPISODES_COMPLETE,
        }
        for character in CHARACTER_SHOP_SLOTS:
            self.assertIn(character.unlock_method, possible_unlocks)
            if character.unlock_method is UnlockMethod.AREA_COMPLETE:
                areas = character.areas
                self.assertIsNotNone(areas)
                self.assertTrue(len(areas) == 1)
                self.assertTrue(next(iter(areas)).is_chapter())
                self.assertIsNotNone(character.purchase_cost)
                self.assertGreater(character.purchase_cost, 0)


class TestSuperGonkDroidCollectOverridePositive(LegoStarWarsWorldTestBase):
    """The collect override for Super Gonk Droid uses string literals for performance. This test ensures the collect
    override is working correctly."""
    # At least Normal logic must be used, otherwise Extras are not Progression classification.
    # The starting chapter is changed to 1-4, a vehicle chapter, so that the starting characters for 1-1 do not obsolete
    # Super Gonk Droid's abilities, causing Super Gonk Droid to be logically irrelevant, and causing Gonk Droid to be
    # logically irrelevant.
    # All chapters are enabled to ensure there is at least somewhere where Super Gonk Droid would be logically relevant.
    options = {
        get_option_name(LogicDifficulty): LogicDifficulty.option_normal,
        get_option_name(StartingChapter): "1-4",
        get_option_name(EnabledChaptersCount): EnabledChaptersCount.range_end,
    }

    @property
    def run_default_tests(self) -> bool:
        # There are already tests for each Logic Difficulty, so there is no need to re-run the tests for Normal Logic
        # Difficulty
        return False

    def test_super_gonk_droid_collect_override_items(self):
        world = self.world

        gonk_droid = world.create_item(CHARACTER_TO_ITEM_DATA[Character.GONK_DROID].name)
        self.assertIn(ItemClassification.progression, gonk_droid.classification)

        super_gonk = world.create_item(ExtraData.from_extra(Extra.SUPER_GONK).name)
        self.assertIn(ItemClassification.progression, super_gonk.classification)

        event_super_gonk_data = CHARACTER_TO_ITEM_DATA[Character.EVENT_SUPER_GONK_DROID]

        for item1, item2 in ((gonk_droid, super_gonk), (super_gonk, gonk_droid)):
            state = CollectionState(world.multiworld)
            self.assertFalse(state.has(item1.name, world.player))
            self.assertFalse(state.has(item2.name, world.player))
            self.assertFalse(state.has(event_super_gonk_data.name, world.player))

            state.collect(item1, prevent_sweep=True)
            self.assertFalse(state.has(event_super_gonk_data.name, world.player))
            state.collect(item2, prevent_sweep=True)
            self.assertTrue(state.has(event_super_gonk_data.name, world.player))

class TestSuperGonkDroidCollectOverrideNegative(LegoStarWarsWorldTestBase):
    """When no chapter is enabled that should make Super Gonk Droid logically relevant, then Gonk Droid should also not
    be logically relevant, assuming chapter unlock requirements are not set to Random Characters, and Gonk Droid has
    been picked for this."""
    options = {
        get_option_name(LogicDifficulty): LogicDifficulty.option_normal,
        get_option_name(StartingChapter): "1-4",
        get_option_name(EnabledChaptersCount): EnabledChaptersCount.range_end,
        # Only the vehicle levels.
        get_option_name(AllowedChapters): {
            "1-4",
            "2-1",
            "2-5",
            "3-1",
            "4-6",
            "5-1",
            "5-3",
            "6-6",
        }
    }

    def test_super_gonk_droid_collect_override_items(self):
        world = self.world

        gonk_droid = world.create_item(CHARACTER_TO_ITEM_DATA[Character.GONK_DROID].name)
        self.assertNotIn(ItemClassification.progression, gonk_droid.classification)

        super_gonk = world.create_item(ExtraData.from_extra(Extra.SUPER_GONK).name)
        self.assertNotIn(ItemClassification.progression, super_gonk.classification)
