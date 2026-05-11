### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

# ruff: noqa: RUF012

import unittest
from collections import Counter
from contextlib import redirect_stdout
from dataclasses import fields
from io import StringIO
from typing import Any

from Options import PerGameCommonOptions

from .. import options
from ..world import enums as e
from ..world.options import CupheadOptions, optionbits
from . import CupheadTestBase


class TestOptionNames(unittest.TestCase):
    def test_option_names(self):
        common_fieldnames = set(fields(PerGameCommonOptions))
        option_fields = [f for f in fields(options.CupheadOptions) if f not in common_fieldnames]

        for field in option_fields:
            with self.subTest(field.name):
                assert field.name == field.type.name, f"{field.name} != {field.type.name}" # type: ignore

# Borrowed from Hammerwatch (thx @Parcosmic)
# https://github.com/Parcosmic/Hammerwatch-Archipelago
class TestOptions(CupheadTestBase):
    option_dict: dict[str, dict[str, Any]] = {
        "Freemove": {
            "freemove_isles": True,
        },
        "DLC": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
        },
        "Level Shuffle": {
            "level_shuffle": "enabled"
        },
        "Level Shuffle Plane": {
            "level_shuffle": "plane_separate"
        },
        "Weapon Progressive": {
            "weapon_mode": "progressive",
        },
        "Weapon EX Separate": {
            "weapon_mode": "ex_separate",
        },
        "No Ability Rando": {
            "randomize_abilities": False,
        },
        "Boss Secrets": {
            "boss_secret_checks": True,
        },
        "DLC Freemove": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
            "freemove_isles": True,
        },
        "Collect Contracts": {
            "mode": "collect_contracts",
        },
        "DLC Collect Ingredients Goal": {
            "use_dlc": True,
            "mode": "dlc_collect_ingredients",
        },
        "DLC Collect Both Goal": {
            "use_dlc": True,
            "mode": "dlc_collect_both",
        },
        "DLC Devil Goal": {
            "use_dlc": True,
            "mode": "beat_devil"
        },
        "Buy Out Shop Goal": {
            "use_dlc": False,
            "mode": "buy_out_shop"
        },
        "DLC Buy Out Shop Goal": {
            "use_dlc": True,
            "mode": "buy_out_shop"
        },
        "DLC Devil Goal No Abilities": {
            "use_dlc": True,
            "mode": "beat_devil",
            "randomize_abilities": False,
        },
        "No Grade Checks": {
            "boss_grade_checks": "disabled",
            "rungun_grade_checks": "disabled",
        },
        "No Grade Checks Full Accessibility Silverworth": {
            "accessibility": "full",
            "boss_grade_checks": "disabled",
            "rungun_grade_checks": "disabled",
            "silverworth_quest": True,
        },
        "DLC No Grade Checks": {
            "use_dlc": True,
            "boss_grade_checks": "disabled",
            "rungun_grade_checks": "disabled",
        },
        "DLC No Chalice": {
            "use_dlc": True,
            "dlc_chalice": "disabled"
        },
        "DLC Chalice Vanilla": {
            "use_dlc": True,
            "dlc_chalice": "vanilla"
        },
        "DLC Chalice Start": {
            "use_dlc": True,
            "dlc_chalice": "start"
        },
        "DLC Cactusgirl": {
            "use_dlc": True,
            "dlc_chalice": "randomized",
            "dlc_cactusgirl_quest": True
        },
        "DLC Weapon Ex": {
            "use_dlc": True,
            "weapon_mode": "progressive",
        },
        "DLC Level Shuffle": {
            "use_dlc": True,
            "level_shuffle": "enabled"
        },
        "DLC Level Shuffle Plane": {
            "use_dlc": True,
            "level_shuffle": "plane_separate"
        },
        "Hard Logic": {
            "logic_mode": "hard"
        },
        "Hard Logic Freemove": {
            "logic_mode": "hard",
            "freemove_isles": True
        },
        "DLC Hard Logic": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
            "logic_mode": "hard"
        },
        "DLC Hard Logic Freemove": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
            "logic_mode": "hard",
            "freemove_isles": True
        },
        "No Weapons": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
            "start_weapon": "none",
            "freemove_isles": True
        },
        "No Weapons Hard Logic": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
            "logic_mode": "hard",
            "start_weapon": "none",
            "freemove_isles": True
        },
        #"No Weapons w Whetstone and Parry": {
        #    "use_dlc": True,
        #    "mode": "dlc_beat_both",
        #    "start_weapon": "none",
        #    "start_inventory": {"Whetstone": 1, "Parry": 1},
        #    "freemove_isles": True
        #},
        "No Weapons Progressive": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
            "start_weapon": "none",
            "weapon_mode": "progressive",
            "freemove_isles": True
        },
        "No Weapons Progressive Hard Logic": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
            "logic_mode": "hard",
            "start_weapon": "none",
            "weapon_mode": "progressive",
            "freemove_isles": True
        },
        "No Weapons EX Separate": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
            "start_weapon": "none",
            "weapon_mode": "ex_separate",
            "freemove_isles": True
        },
        "No Weapons EX Separate Hard Logic": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
            "logic_mode": "hard",
            "start_weapon": "none",
            "weapon_mode": "ex_separate",
            "freemove_isles": True
        }
    }

    def _check_all_items_are_active(self, option_set_name: str):
        game_players = set(self.multiworld.get_game_players(self.game))
        player_items = {p: [x.name for x in self.multiworld.get_items() if x.player == p] for p in game_players}
        for items in player_items.values():
            remaining_items = Counter(items)
            for item in items:
                assert remaining_items[item] > 0, \
                    f"{option_set_name}: '{item}' exists even though it isn't an active item."
                remaining_items[item] -= 1
                if remaining_items[item] < 1:
                    del remaining_items[item]
            assert len(remaining_items.keys()) == 0, \
                f"{option_set_name}: The following items are active but have not been created: {remaining_items}"

    def _check_all_locations_are_active(self, option_set_name: str):
        for player in self.multiworld.get_game_players(self.game):
            remaining_locs = set(self.multiworld.worlds[player].active_locations.keys())
            for region in self.multiworld.get_regions(player):
                for loc in region.locations:
                    assert loc.name in remaining_locs, \
                        f"{option_set_name}: '{loc.name}' exists even though it isn't an active location."
                    remaining_locs.remove(loc.name)
            assert len(remaining_locs) == 0, \
                f"{option_set_name}: The following locations are active but have not been created: {remaining_locs}"

    def test_default_options(self):
        option_set_name = "Default Options"
        test_world = TestOptions()
        test_world.world_setup()
        test_world._check_all_items_are_active(option_set_name)
        test_world._check_all_locations_are_active(option_set_name)
        if self.world.settings.is_debug_bit_on(1024): # type: ignore
            print(f"Seed of '{option_set_name}': {test_world.multiworld.seed}")
        test_world.test_fill()

    def test_options(self):
        for option_set, opts in self.option_dict.items():
            with self.subTest(option_set):
                test_world = TestOptions()
                test_world.options = opts
                test_world.world_setup()
                test_world._check_all_items_are_active(option_set)
                test_world._check_all_locations_are_active(option_set)
                if self.world.settings.is_debug_bit_on(1024): # type: ignore
                    print(f"Seed of '{option_set}': {test_world.multiworld.seed}")
                test_world.test_fill()
                test_world.world_setup()
                test_world.test_empty_state_can_reach_something()
                test_world.world_setup()
                test_world.test_all_state_can_reach_everything()

class TestOptionBits(CupheadTestBase):
    def test_option_bits(self):
        test_world = TestOptionBits()
        test_world.options = {
            "boss_secret_checks": True,
        }
        test_world.world_setup()

        bitsa = optionbits.bitify(test_world.world.options)  # type: ignore

        test_worldb = TestOptionBits()
        test_worldb.world_setup()

        optionbits.debitify(test_worldb.world.options, bitsa)  # type: ignore
        test_worldb.assertEqual(bitsa, optionbits.bitify(test_worldb.world.options))  # type: ignore

class TestOptionSanitizer(CupheadTestBase):
    auto_construct = False

    def test_dlc_off_sanitizes_dlc_options(self):
        test_world = TestOptionSanitizer()
        test_world.options = {
            "use_dlc": False,
            "mode": "dlc_collect_both",
            "start_weapon": "dlc_converge",
            "dlc_chalice": "randomized",
            "dlc_curse_mode": "vanilla",
            "dlc_kingsleap": "include_all",
            "dlc_boss_chalice_checks": "separate_grade_required",
            "dlc_rungun_chalice_checks": "separate_grade_required",
            "dlc_kingdice_chalice_checks": "separate",
            "dlc_chess_chalice_checks": "separate",
            "dlc_cactusgirl_quest": True,
        }
        test_world.world_setup()
        world_options = test_world.world.options
        assert isinstance(world_options, CupheadOptions)

        self.assertEqual(world_options.dlc_chalice.value, int(e.ChaliceMode.DISABLED))
        self.assertEqual(world_options.dlc_curse_mode.value, int(e.CurseMode.OFF))
        self.assertEqual(world_options.dlc_kingsleap.value, int(e.ChessCastleMode.EXCLUDE))
        self.assertEqual(world_options.dlc_boss_chalice_checks.value, int(e.ChaliceCheckMode.DISABLED))
        self.assertEqual(world_options.dlc_rungun_chalice_checks.value, int(e.ChaliceCheckMode.DISABLED))
        self.assertEqual(world_options.dlc_kingdice_chalice_checks.value, int(e.ChaliceCheckMode.DISABLED))
        self.assertEqual(world_options.dlc_chess_chalice_checks.value, int(e.ChaliceCheckMode.DISABLED))
        self.assertFalse(world_options.dlc_cactusgirl_quest.value)

    def test_dlc_off_preserves_no_start_weapon(self):
        test_world = TestOptionSanitizer()
        test_world.options = {
            "use_dlc": False,
            "start_weapon": "none",
        }
        test_world.world_setup()
        world_options = test_world.world.options
        assert isinstance(world_options, CupheadOptions)

        self.assertTrue(world_options.start_weapon.is_none())

    def test_single_player_no_start_weapon_warns(self):
        test_world = TestOptionSanitizer()
        test_world.options = {
            "logic_mode": "hard",
            "start_weapon": "none",
            "randomize_abilities": False,
            "test_overrides": {"sani": True},
        }

        out = StringIO()
        with redirect_stdout(out):
            test_world.world_setup()

        output = out.getvalue()
        assert "single-player generation with start_weapon set to 'none' may fail" in output

    def test_minimal_accessibility_warns_on_risky_combo(self):
        test_world = TestOptionSanitizer()
        test_world.options = {
            "accessibility": "minimal",
            "weapon_mode": "progressive",
            "randomize_abilities": True,
            "boss_grade_checks": "a_grade",
            "pacifist_quest": True,
            "silverworth_quest": True,
            "test_overrides": {"sani": True}
        }

        out = StringIO()
        with redirect_stdout(out):
            test_world.world_setup()

        output = out.getvalue()
        assert "Accessibility is set to 'minimal' with high-risk options enabled" in output
