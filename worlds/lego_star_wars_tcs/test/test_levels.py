from unittest import TestCase

from ..constants import CharacterAbility
from ..items import ITEM_DATA_BY_NAME, CHARACTERS_AND_VEHICLES_BY_NAME
from ..levels import CHAPTER_AREAS
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