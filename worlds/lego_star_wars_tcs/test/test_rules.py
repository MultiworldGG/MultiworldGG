from unittest import TestCase

from BaseClasses import CollectionState
from rule_builder.rules import Has, Rule, And, Or, HasAny
from test.general import setup_multiworld
from worlds import AutoWorldRegister

from ..character_ability import CharacterAbility
from ..constants import GAME_NAME
from ..data.characters import Character
from ..data.extras import Extra
from ..data.items.character_items import NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA
from ..data.items.vehicle_items import VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA
from ..data.logic.option_filters import logic_options
from ..data.logic.macros import can_jump_distance_rule
from ..data.logic.rules import (
    HasAbility,
    HasAbilityExceptCharacters,
    HasAnyAbilities,
    HasAnyCharacterExcept,
    HasAbilityCombination,
)
from ..options import LogicDifficulty

BASE_ITEM = "BASE_ITEM"
NORMAL_ITEM = "NORMAL_ITEM"
MODERATE_ITEM = "MODERATE_ITEM"
HARD_ITEM = "HARD_ITEM"

BASIC_OPTIONS = logic_options(
    base=Has(BASE_ITEM),
    normal=Has(NORMAL_ITEM),
    moderate=Has(MODERATE_ITEM),
    hard=Has(HARD_ITEM),
)


class TestLogicOptionsRules(TestCase):
    def items_from_simple_rule(self, rule: Rule) -> list[str]:
        items = []
        self.assertIsInstance(rule, (Has, And))
        if isinstance(rule, Has):
            items.append(rule.item_name)
        elif isinstance(rule, And):
            for child_rule in rule.children:
                self.assertIsInstance(child_rule, Has)
                items.append(child_rule.item_name)
        return items

    def test_logic_options_and_full_spread(self):
        options = logic_options(
            base=Has("base item 2"),
            hard=Has("hard item 2"),
        ).and_rule(BASIC_OPTIONS)

        self.assertEqual(self.items_from_simple_rule(options.base), ["base item 2", BASE_ITEM])
        self.assertEqual(self.items_from_simple_rule(options.normal), ["base item 2", NORMAL_ITEM])
        self.assertEqual(self.items_from_simple_rule(options.moderate), ["base item 2", MODERATE_ITEM])
        self.assertEqual(self.items_from_simple_rule(options.hard), ["hard item 2", HARD_ITEM])

    def test_logic_options_and_full_spread_reverse(self):
        options = BASIC_OPTIONS.and_rule(
            logic_options(
                base=Has("base item 2"),
                hard=Has("hard item 2"),
            )
        )

        self.assertEqual(self.items_from_simple_rule(options.base), [BASE_ITEM, "base item 2"])
        self.assertEqual(self.items_from_simple_rule(options.normal), [NORMAL_ITEM, "base item 2"])
        self.assertEqual(self.items_from_simple_rule(options.moderate), [MODERATE_ITEM, "base item 2"])
        self.assertEqual(self.items_from_simple_rule(options.hard), [HARD_ITEM, "hard item 2"])

    def test_logic_option_single_rule_full_spread(self):
        options = BASIC_OPTIONS.and_rule(Has("spread rule"))

        self.assertEqual(self.items_from_simple_rule(options.base), [BASE_ITEM, "spread rule"])
        self.assertEqual(self.items_from_simple_rule(options.normal), [NORMAL_ITEM, "spread rule"])
        self.assertEqual(self.items_from_simple_rule(options.moderate), [MODERATE_ITEM, "spread rule"])
        self.assertEqual(self.items_from_simple_rule(options.hard), [HARD_ITEM, "spread rule"])

    def test_logic_options_partial_spread(self):
        options = logic_options(
            base=Has("base item 2"),
            hard=Has("hard item 2"),
        ).and_rule(BASIC_OPTIONS, apply_to="moderate+")

        self.assertEqual(self.items_from_simple_rule(options.base), ["base item 2"])
        self.assertEqual(self.items_from_simple_rule(options.normal), ["base item 2"])
        self.assertEqual(self.items_from_simple_rule(options.moderate), ["base item 2", MODERATE_ITEM])
        self.assertEqual(self.items_from_simple_rule(options.hard), ["hard item 2", HARD_ITEM])

    def test_logic_options_single_rule_partial_spread(self):
        options = logic_options(
            base=Has("base item 2"),
            hard=Has("hard item 2"),
        ).and_rule(BASIC_OPTIONS.normal, apply_to="moderate+")

        self.assertEqual(self.items_from_simple_rule(options.base), ["base item 2"])
        self.assertEqual(self.items_from_simple_rule(options.normal), ["base item 2"])
        self.assertEqual(self.items_from_simple_rule(options.moderate), ["base item 2", NORMAL_ITEM])
        self.assertEqual(self.items_from_simple_rule(options.hard), ["hard item 2", NORMAL_ITEM])


class TestJumpDistanceMacros(TestCase):
    def _test(self, distance: float, expected_ability: CharacterAbility, *expected_characters: str):
        rule = can_jump_distance_rule(distance).make_simpler_rule()
        if expected_characters:
            self.assertIsInstance(rule, Or)
            for child in rule.children:
                self.assertIsInstance(child, (HasAbility, HasAny))
                if isinstance(child, HasAbility):
                    self.assertIs(child.ability, expected_ability)
                elif isinstance(child, HasAny):
                    self.assertEqual(set(expected_characters), set(child.item_names))
        else:
            self.assertIsInstance(rule, HasAbility)
            self.assertIs(rule.ability, expected_ability)

    def test_0_5(self):
        self._test(0.5, CharacterAbility.CAN_BARELY_JUMP)

    def test_0_56(self):
        self._test(0.56, CharacterAbility.CAN_BARELY_JUMP)

    def test_0_6(self):
        self._test(0.6, CharacterAbility.CAN_JUMP_DISTANCE_0_69,
                   # 0.65
                   "Geonosian",
                   "Watto",
                   )

    def test_0_65(self):
        self._test(0.65, CharacterAbility.CAN_JUMP_DISTANCE_0_69,
                   # 0.65
                   "Geonosian",
                   "Watto",
                   )

    def test_0_7(self):
        self._test(0.7, CharacterAbility.CAN_JUMP_DISTANCE_0_84,
                   # 0.7
                   "Clone",
                   "Clone (Episode III)",
                   "Clone (Episode III, Pilot)",
                   "Commander Cody",
                   "Clone (Episode III, Swamp)",
                   "Clone (Episode III, Walker)",
                   "Disguised Clone",
                   "Boss Nass",
                   # 0.766...
                   "Dexter Jettster",
                   )

    def test_0_8(self):
        self._test(0.8, CharacterAbility.CAN_JUMP_DISTANCE_0_84)

    def test_0_9(self):
        self._test(0.9, CharacterAbility.CAN_JUMP_DISTANCE_0_92, "Lando Calrissian", "Lando (Palace Guard)")

    def test_1_0(self):
        with self.assertRaises(ValueError):
            can_jump_distance_rule(1.0)


class TestAbilityExceptCharacters(TestCase):
    def test_jedi_except_yoda(self):
        """Test a fairly common case of needing any Jedi, except Yoda/Yoda (Ghost)"""
        rule = HasAbilityExceptCharacters(CharacterAbility.JEDI, Character.YODA, Character.YODA_GHOST)
        made = rule.make_simpler_rule()

        self.assertIsInstance(made, Or)
        self.assertEqual(len(made.children), 2)

        child0 = made.children[0]
        self.assertIsInstance(child0, HasAnyAbilities)
        self.assertEqual(child0.abilities, CharacterAbility.SITH | CharacterAbility.CAN_WEAR_HAT_AND_DOUBLE_JUMP)

        child1 = made.children[1]
        self.assertIsInstance(child1, HasAny)
        self.assertEqual(set(child1.item_names), {
            "Aayla Secura",
            "Ki-Adi Mundi",
            "Kit Fisto",
            "Luke Skywalker (Endor)",
            "Luminara",
            "Plo Koon",
            "Shaak Ti",
        })

    def test_double_jump_except_yoda(self):
        """Test a fairly common case of needing any Double Jumper character, except Yoda/Yoda (Ghost)"""
        rule = HasAbilityExceptCharacters(CharacterAbility.CAN_DOUBLE_JUMP, Character.YODA, Character.YODA_GHOST)
        made = rule.make_simpler_rule()

        self.assertIsInstance(made, Or)
        self.assertEqual(len(made.children), 2)
        child1 = made.children[0]
        child2 = made.children[1]

        self.assertIsInstance(child1, HasAnyAbilities)
        self.assertEqual(child1.abilities, CharacterAbility.CAN_TRIPLE_JUMP_GREAT_DISTANCE | CharacterAbility.HIGH_JUMP)

        self.assertIsInstance(child2, Has)
        self.assertEqual(child2.item_name, Character.ADMIRAL_ACKBAR.readable_name)

    def test_has_any_character_except(self):
        """Test HasAnyCharacterExcept with random assortments of characters."""
        world_type = AutoWorldRegister.world_types[GAME_NAME]
        # Extras are not in logic in the lowest logic difficulty.
        options = [{"logic_difficulty": LogicDifficulty.option_normal}]
        mw = setup_multiworld([world_type], steps=(), options=options)
        world = mw.worlds[1]
        test_state = CollectionState(mw)
        vehicle_characters = [d.character for d in VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA.values()]
        normal_characters = [d.character for d in NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA.values()]
        for characters in (vehicle_characters, normal_characters):
            for _ in range(len(characters)):
                # Pick some character to exclude.
                except_characters = set(mw.random.sample(characters, k=mw.random.choice(range(1, 6))))
                with self.subTest(except_characters=except_characters):
                    rule = HasAnyCharacterExcept(*except_characters)
                    collection_rule = rule.resolve(world)
                    for character in characters:
                        expect_true = character not in except_characters
                        if character is Character.EVENT_SUPER_GONK_DROID:
                            # Super Gonk Droid is only available via a collect() override.
                            items = [
                                world.create_item(Character.GONK_DROID.readable_name),
                                world.create_item(Extra.SUPER_GONK.readable_name),
                            ]
                            # The collect override includes "Gonk Droid", so if "Gonk Droid" is not also excluded, the
                            # rule should pass.
                            if Character.GONK_DROID not in except_characters:
                                expect_true = True
                        else:
                            items = [world.create_item(character.readable_name)]
                        for item in items:
                            test_state.collect(item, True)
                        try:
                            if expect_true:
                                self.assertTrue(collection_rule(test_state), f"Failed for {character!r}")
                            else:
                                self.assertFalse(collection_rule(test_state), f"Failed for {character!r}")
                        finally:
                            for item in items:
                                test_state.remove(item)


class TestAbilityCombinations(TestCase):
    def test_ride_vehicles_and_high_jump(self):
        rule = HasAbilityCombination.static_make_simpler_rule(
            CharacterAbility.CAN_RIDE_VEHICLES | CharacterAbility.HIGH_JUMP)
        self.assertIsInstance(rule, HasAny)
        self.assertEqual(set(rule.item_names), {"Jar Jar Binks", "Captain Tarpals"})

    def test_ride_vehicles_and_double_jump(self):
        rule = HasAbilityCombination.static_make_simpler_rule(
            CharacterAbility.CAN_RIDE_VEHICLES | CharacterAbility.CAN_DOUBLE_JUMP)
        self.assertIsInstance(rule, Or)
        self.assertEqual(len(rule.children), 2)

        r1 = rule.children[0]
        self.assertIsInstance(r1, HasAbility)
        self.assertEqual(r1.ability, CharacterAbility.JEDI)

        r2 = rule.children[1]
        self.assertIsInstance(r2, HasAny)
        self.assertEqual(set(r2.item_names), {"Jar Jar Binks", "Captain Tarpals", "Admiral Ackbar"})

    def test_imperial_and_jedi(self):
        rule = HasAbilityCombination.static_make_simpler_rule(
            CharacterAbility.IMPERIAL | CharacterAbility.JEDI)
        self.assertIsInstance(rule, HasAny)
        self.assertEqual(set(rule.item_names), {"Darth Vader", "The Emperor"})

    def test_imperial_and_jedi_or_ride_vehicles_and_high_jump(self):
        rule = HasAbilityCombination.static_make_simpler_rule(
            CharacterAbility.IMPERIAL | CharacterAbility.JEDI,
            CharacterAbility.CAN_RIDE_VEHICLES | CharacterAbility.HIGH_JUMP,
        )
        self.assertIsInstance(rule, Or)
        self.assertEqual(len(rule.children), 2)

        r1 = rule.children[0]
        self.assertIsInstance(r1, HasAny)
        self.assertEqual(set(r1.item_names), {"Darth Vader", "The Emperor"})

        r2 = rule.children[1]
        self.assertIsInstance(r2, HasAny)
        self.assertEqual(set(r2.item_names), {"Jar Jar Binks", "Captain Tarpals"})

    def test_bounty_hunter_and_can_build_bricks(self):
        rule = HasAbilityCombination.static_make_simpler_rule(
            CharacterAbility.BOUNTY_HUNTER | CharacterAbility.CAN_BUILD_BRICKS)
        self.assertIsInstance(rule, Or)
        self.assertEqual(len(rule.children), 2)

        r1 = rule.children[0]
        self.assertIsInstance(r1, HasAbility)
        self.assertEqual(r1.ability, CharacterAbility.JETPACK)

        r2 = rule.children[1]
        self.assertIsInstance(r2, HasAny)
        self.assertEqual(set(r2.item_names), {"Bossk", "Dengar", "Greedo", "Zam Wesell"})

    def test_bounty_hunter_and_astromech_panel(self):
        rule = HasAbilityCombination.static_make_simpler_rule(
            CharacterAbility.BOUNTY_HUNTER | CharacterAbility.ASTROMECH_PANEL)
        self.assertIsInstance(rule, HasAny)
        self.assertEqual(set(rule.item_names), {"4-LOM", "IG-88"})

    def test_bounty_hunter_and_double_jump(self):
        rule = HasAbilityCombination.static_make_simpler_rule(
            CharacterAbility.BOUNTY_HUNTER | CharacterAbility.CAN_DOUBLE_JUMP)
        self.assertIsInstance(rule, HasAny)
        self.assertEqual(set(rule.item_names), set())

    def test_can_wear_hat_and_jedi(self):
        rule = HasAbilityCombination.static_make_simpler_rule(CharacterAbility.CAN_WEAR_HAT | CharacterAbility.JEDI)
        self.assertIsInstance(rule, HasAbility)
        self.assertEqual(rule.ability, CharacterAbility.CAN_WEAR_HAT_AND_DOUBLE_JUMP)
