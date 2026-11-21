import json
from unittest import TestCase
from typing import Callable, Iterable, Any

from rule_builder.rules import Rule, NestedRule, WrapperRule, And
from test.general import setup_multiworld
from worlds import AutoWorldRegister

from ..data.levels import Level
from ..data.logic import EPISODES, CHAPTERS_BY_NUMBERS, CHAPTERS_BY_SHORT_NAME
from ..data.logic.extraction import ExtractionRuleReplacer
from ..data.logic.option_filters import LogicOptions
from ..data.logic.types import Chapter

from ..constants import GAME_NAME
from ..items import CHARACTERS_AND_VEHICLES_BY_NAME
from ..options import LogicDifficulty, get_option_name


_DUMP_EXTRACTION_RULE_TO_FILE = False

if _DUMP_EXTRACTION_RULE_TO_FILE:
    import os
    from Utils import get_file_safe_name
    def json_dump_rule(rule_dict: dict[str, Any], un_nested: bool, owner_name: str, chapter: Chapter):
        un_nested_str = "un_nested" if un_nested else "original"
        file_name = f"{get_file_safe_name(owner_name)}_{un_nested_str}.json"
        # A local git repository, so I can compare changes.
        dir_path = os.path.join("G:\\", "git_Repos_other", "lsw_tcs_logic_dump", "rules_dump",
                                get_file_safe_name(chapter.area.readable_name))
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, file_name), "w", encoding="utf-8") as f:
            json.dump(rule_dict, f, ensure_ascii=False, indent=2)
        print()
else:
    def json_dump_rule(rule_dict: dict[str, Any], un_nested: bool, owner_name: str, chapter: Chapter):
        json.dumps(rule_dict)


def chapters_iter() -> Iterable[Chapter]:
    for episode in EPISODES:
        yield from episode


def chapters_test(test_func: "Callable[[TestEpisodes, Chapter], None]") -> "Callable[[TestEpisodes], None]":
    def test_chapters(self: "TestEpisodes"):
        for chapter in chapters_iter():
            with self.subTest(chapter=(chapter.area.get_long_name()), chapter_name=chapter.name):
                test_func(self, chapter)
    return test_chapters


class TestEpisodes(TestCase):
    def assertCharacterExists(self, character: str):
        self.assertIn(character, CHARACTERS_AND_VEHICLES_BY_NAME, f"Character '{character}' not found.")

    def assertCharacterIsSendable(self, character: str):
        self.assertTrue(CHARACTERS_AND_VEHICLES_BY_NAME[character].is_sendable,
                        f"Character '{character}' is not sendable")

    def assertCharacterUsableInChapterRequirements(self, character):
        self.assertCharacterExists(character)
        self.assertCharacterIsSendable(character)

    @chapters_test
    def test_minikit_count(self, chapter: Chapter):
        """Test that each chapter has exactly 10 minikits defined."""
        self.assertEqual(len(chapter.minikits), 10)

    @chapters_test
    def test_unique_minikit_pickup_names_per_level(self, chapter: Chapter):
        """Test that within each level in a chapter, the minikit pickup names are unique."""
        for level, minikits in chapter.level_minikits.items():
            with self.subTest(level=level):
                found_pickup_names = set()
                for minikit_data in minikits.values():
                    for pickup_name in minikit_data.pickup_names:
                        self.assertNotIn(pickup_name, found_pickup_names)
                        found_pickup_names.add(pickup_name)

    @chapters_test
    def test_location_regions_exist(self, chapter: Chapter):
        for location_data in chapter.all_in_level_location_data:
            self.assertIn(location_data.region, chapter.regions)

    @chapters_test
    def test_chapter_completion_has_unique_status_level(self, chapter: Chapter):
        """Test that the Chapter Completion region is in a level ending with _status, and that no other regions are in
        this level."""
        self.assertIn("Chapter Completion", chapter.region_to_level)
        status_level = chapter.region_to_level["Chapter Completion"]
        self.assertTrue(status_level.name.endswith("_STATUS"))
        for region, level in chapter.region_to_level.items():
            if region != "Chapter Completion":
                self.assertNotEqual(level, status_level)

    def test_levels_unique_per_chapter(self):
        """Test that levels are unique to a single chapter."""
        seen_levels: set[Level] = set()
        for chapter in chapters_iter():
            chapter_levels = set(chapter.region_to_level.values())
            self.assertTrue(seen_levels.isdisjoint(chapter_levels))
            seen_levels.update(chapter_levels)

    @chapters_test
    def test_levels_exist_in_area(self, chapter: Chapter):
        for level in set(chapter.region_to_level.values()):
            self.assertIn(level, chapter.area.levels)

    def test_episode_chapter_numbers(self):
        """Test that chapter episode/chapter numbers are unique and within the expected bounds."""
        seen_by_episode = {episode_number: set() for episode_number in range(1, 7)}
        allowed_chapter_numbers = range(1, 7)
        for chapter in chapters_iter():
            area = chapter.area
            self.assertIn(area.get_chapter_episode(), seen_by_episode)
            self.assertIn(area.get_chapter_number_in_episode(), allowed_chapter_numbers)

            seen_chapters = seen_by_episode[area.get_chapter_episode()]
            self.assertNotIn(area.get_chapter_number_in_episode(), seen_chapters)

            seen_chapters.add(area.get_chapter_number_in_episode())

    @chapters_test
    def test_regions_are_used(self, chapter: Chapter):
        """Test that each region contains at least one exit, or at least one location, or is used in a
        CanReachRegion rule."""
        unused_region_names = {name for name, exits in chapter.regions.items() if not exits}
        unused_region_names.discard("Chapter Completion")
        unused_region_names.difference_update(chapter.regions_in_can_reach)
        if not unused_region_names:
            return
        for location_data in chapter.all_in_level_location_data:
            if location_data.region in unused_region_names:
                unused_region_names.remove(location_data.region)
                if not unused_region_names:
                    return
        self.fail(f"There are unused regions: {sorted(unused_region_names)}")

    @chapters_test
    def test_story_characters(self, chapter: Chapter):
        for character in chapter.area.get_purchase_characters():
            self.assertCharacterUsableInChapterRequirements(character.readable_name)

    @chapters_test
    def test_purchase_characters(self, chapter: Chapter):
        for character in chapter.area.get_purchase_characters():
            self.assertCharacterUsableInChapterRequirements(character.readable_name)
            self.assertGreater(character.purchase_cost, 0)

    def test_purchase_characters_unique_per_chapter(self):
        seen_characters = set()
        for chapter in chapters_iter():
            for character in chapter.area.get_purchase_characters():
                self.assertNotIn(character, seen_characters, f"{character} from {chapter.short_name} already found.")
            seen_characters.update(chapter.area.get_purchase_characters())

    @staticmethod
    def chapter_rule_gen(chapter: Chapter) -> Iterable[tuple[str, Rule]]:
        for region_name, exits in chapter.regions.items():
            for exit_ in exits:
                exit_name = exit_.name
                if not exit_name:
                    exit_name = f"{region_name} -> {exit_.to_region}"
                yield exit_name, exit_.rule
                if exit_.er_rule is not None:
                    yield exit_name + "(ER)", exit_.er_rule

        for minikit_name, minikit_data in chapter.minikits.items():
            yield minikit_name, minikit_data.rule
            if minikit_data.er_rule is not None:
                yield minikit_name + "(ER)", minikit_data.er_rule

        for ridable, ridable_data in chapter.ridables.items():
            if not isinstance(ridable_data, tuple):
                ridable_data_tuple = (ridable_data,)
            else:
                ridable_data_tuple = ridable_data
            for ridable_datum in ridable_data_tuple:
                yield ridable.readable_name, ridable_datum.rule
                if ridable_datum.er_rule is not None:
                    yield ridable.readable_name + "(ER)", ridable_datum.er_rule

        yield "Power Brick", chapter.power_brick.rule
        if chapter.power_brick.er_rule is not None:
            yield "Power Brick (ER)", chapter.power_brick.er_rule

        yield "Extra Chapter Entrance Rules", chapter.extra_entrance_rules

    def _check_top_level_rule(self, rule: Rule, logic_options_allowed: bool = True):
        if isinstance(rule, LogicOptions):
            self.assertTrue(logic_options_allowed,
                            "Found a LogicOptions not nested within another LogicOptions or at the top level")
        if isinstance(rule, WrapperRule):
            self._check_top_level_rule(rule.child, False)
        elif isinstance(rule, NestedRule):
            for child in rule.children:
                self._check_top_level_rule(child, False)

    @chapters_test
    def test_extraction_un_nesting(self, chapter: Chapter):
        replacer = ExtractionRuleReplacer()
        for owner_name, rule in self.chapter_rule_gen(chapter):
            with self.subTest(name=owner_name):
                un_nested = replacer.replace_top_level_rule(rule)
                self._check_top_level_rule(un_nested)

    @chapters_test
    def test_rules_json_serializable(self, chapter: Chapter):
        replacer = ExtractionRuleReplacer()
        for owner_name, rule in self.chapter_rule_gen(chapter):
            with self.subTest(name=owner_name):
                un_nested = replacer.replace_top_level_rule(rule)

                with self.subTest(un_nested=False):
                    json_dump_rule(rule.to_dict(), False, owner_name, chapter)
                if un_nested is not rule:
                    with self.subTest(un_nested=True):
                        json_dump_rule(un_nested.to_dict(), True, owner_name, chapter)

    def test_rules_resolve(self):
        # PyCharm sees that the ClassVar is not assigned, or something, and assumes it is actually an instance
        # attribute, and then complains about access to a generic instance attribute from the class.
        # Technically this is a bug in core AP because TypeVars cannot be used in ClassVars because it makes no sense
        # when each instance of a generic class can have a different generic type.
        # noinspection PyTypeChecker
        logic_difficulties = [
            LogicDifficulty(v) for v in LogicDifficulty.name_lookup.keys()
        ]
        world_types = [AutoWorldRegister.world_types[GAME_NAME]] * len(logic_difficulties)
        options = [
            {
                get_option_name(LogicDifficulty): difficulty.value,
            } for difficulty in logic_difficulties
        ]

        # Only bother with running up to `generate_early` because the rules for each chapter will be grabbed and
        # resolved manually. CanReachRegion rules don't actually need their objects to exist because the resolved rules
        # only store the names. CanReachLocation/CanReachEntrance rules do however, but are currently unused, so test
        # performance can be increased by performing fewer generation steps.
        mw = setup_multiworld(world_types, steps=("generate_early",), seed=None, options=options)
        for world, logic_difficulty in zip(mw.worlds.values(), logic_difficulties):
            def test_function(_self, chapter: Chapter):
                for owner_name, rule in self.chapter_rule_gen(chapter):
                    with self.subTest(rule=owner_name):
                        rule.resolve(world)

            with self.subTest(difficulty=logic_difficulty.current_option_name):
                chapters_test(test_function)(self)

    def test_chapters_by_numbers(self):
        for episode_number, chapters in CHAPTERS_BY_NUMBERS.items():
            for chapter_number, chapter in chapters.items():
                area = chapter.area
                self.assertEqual(episode_number, area.get_chapter_episode())
                self.assertEqual(chapter_number, area.get_chapter_number_in_episode())

    def test_chapters_by_short_name(self):
        for short_name, chapter in CHAPTERS_BY_SHORT_NAME.items():
            self.assertEqual(short_name, chapter.short_name)

    def test_expected_no_minikits_levels(self):
        expected_no_minikits_levels = {
            # The level with the Slave 1 and the Power Brick.
            Level.CLOUDCITYESCAPE_B,
            # The final battle against Zam's Speeder.
            Level.PURSUIT_E,
            # The falling elevator.
            Level.CRUISER_D,
            # The many forcefields corridor before the final fight.
            Level.MAUL_E,
            # The optional elevator room with four hat machines (and a challenge kit).
            Level.DEATHSTARRESCUE_D,
            # The twin turbolaster control room where you shoot TIE Fighters for a lot of studs.
            Level.DEATHSTARRESCUE_E,
            # The waste disposal/crusher room with the Power Brick.
            Level.DEATHSTARESCAPE_D,
        }

        levels_with_minikits = {level for chapter in chapters_iter() for level in chapter.level_minikits.keys()}
        playable_chapter_levels = {level for chapter in chapters_iter() for level in chapter.area.get_playable_levels()}
        playable_chapter_levels_without_minikits = playable_chapter_levels - levels_with_minikits

        self.assertEqual(playable_chapter_levels_without_minikits, expected_no_minikits_levels)
