import unittest
from typing import Any
from collections import Counter
from dataclasses import fields
from Options import PerGameCommonOptions
from .. import options
from . import CupheadTestBase

class TestOptionNames(unittest.TestCase):
    def test_option_names(self):
        common_fieldnames = {f for f in fields(PerGameCommonOptions)}
        option_fields = [f for f in fields(options.CupheadOptions) if f not in common_fieldnames]

        for field in option_fields:
            with self.subTest(field.name):
                assert field.name == field.type.name, f"{field.name} != {field.type.name}" # type: ignore

# Borrowed from Hammerwatch (thx @Parcosmic)
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
        "Weapon Ex": {
            "weapon_mode": "progressive",
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
    }

    def _check_all_items_are_active(self, option_set_name: str):
        game_players = set(self.multiworld.get_game_players(self.game))
        player_items = {p: [x.name for x in self.multiworld.get_items() if x.player == p] for p in game_players}
        for _player, items in player_items.items():
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
            remaining_locs = {x for x in self.multiworld.worlds[player].active_locations.keys()}
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
            print(f"Seed of \"{option_set_name}\": {test_world.multiworld.seed}")
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
                    print(f"Seed of \"{option_set}\": {test_world.multiworld.seed}")
                test_world.test_fill()
                test_world.world_setup()
                test_world.test_empty_state_can_reach_something()
                test_world.world_setup()
                test_world.test_all_state_can_reach_everything()
