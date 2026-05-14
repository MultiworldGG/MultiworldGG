from unittest import TestCase

from ..constants import CharacterAbility
from ..items import ITEM_DATA_BY_NAME, CHARACTERS_AND_VEHICLES_BY_NAME
from ..levels import CHAPTER_AREAS, BONUS_AREAS
from ..locations import LOCATION_NAME_TO_ID


class TestLevels(TestCase):
    def test_area_requirements(self):
        for area in CHAPTER_AREAS:
            for requirement in area.character_requirements:
                self.assertIn(requirement, ITEM_DATA_BY_NAME)

    def test_character_shop_unlocks(self):
        for area in CHAPTER_AREAS:
            for shop_unlock_location, _cost in area.character_shop_unlocks.items():
                self.assertIn(shop_unlock_location, LOCATION_NAME_TO_ID)

    def test_power_bricks(self):
        for area in CHAPTER_AREAS:
            self.assertIn(area.power_brick_location_name, LOCATION_NAME_TO_ID)

    def test_main_ability_requirements_satisfied_by_story_characters(self):
        for area in CHAPTER_AREAS:
            with self.subTest(area.name):
                story_character_abilities = CharacterAbility.NONE
                for character in area.character_requirements:
                    story_character_abilities |= CHARACTERS_AND_VEHICLES_BY_NAME[character].abilities
                self.assertLessEqual(area.completion_main_ability_requirements, story_character_abilities)

    def test_playable_level_ids(self):
        all_ids_so_far = set()
        for areas in [CHAPTER_AREAS, BONUS_AREAS]:
            for area in areas:
                with self.subTest(area.name):
                    level_ids = area.playable_level_ids
                    self.assertEqual(len(level_ids), len(set(level_ids)))
                    self.assertEqual(list(level_ids), sorted(level_ids))
                    if level_ids:
                        previous = level_ids[0]
                        for level_id in level_ids[1:]:
                            self.assertEqual(previous + 1, level_id)
                            previous = level_id
                    self.assertTrue(all_ids_so_far.isdisjoint(level_ids))
                    all_ids_so_far.update(level_ids)
