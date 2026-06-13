import unittest
from unittest.mock import Mock, patch, MagicMock
from BaseClasses import ItemClassification, MultiWorld
import copy

from . import PoeTestBase
from .. import Items, Locations, Options
from ..Options import PathOfExileOptions
from ..Logic import setup_early_items, setup_character_items, get_goal_act, cull_items_to_place, deprioritize_non_logic_gems
from ..data import ItemTable


def _make_options():
    """Return a fully-configured mock PathOfExileOptions."""
    opt = Mock(spec=PathOfExileOptions)

    opt.progressive_gear = Mock()
    opt.progressive_gear.value = 0
    opt.progressive_gear.option_enabled = 0
    opt.progressive_gear.option_disabled = 1
    opt.progressive_gear.option_progressive_except_for_unique = 2

    opt.gucci_hobo_mode = Mock()
    opt.gucci_hobo_mode.value = 0
    opt.gucci_hobo_mode.option_disabled = 0
    opt.gucci_hobo_mode.option_allow_one_slot_of_normal_rarity = 1
    opt.gucci_hobo_mode.option_no_non_unique_items = 2

    opt.add_passive_skill_points_to_item_pool = Mock()
    opt.add_passive_skill_points_to_item_pool.value = True

    opt.gear_upgrades = Mock()
    opt.gear_upgrades.value = 0
    opt.gear_upgrades.option_no_gear_unlocked = 0
    opt.gear_upgrades.option_all_gear_unlocked_at_start = 1
    opt.gear_upgrades.option_all_normal_and_unique_gear_unlocked = 2
    opt.gear_upgrades.option_all_normal_gear_unlocked = 3
    opt.gear_upgrades.option_all_uniques_unlocked = 4

    opt.add_flasks_to_item_pool = Mock()
    opt.add_flasks_to_item_pool.value = True

    opt.add_max_links_to_item_pool = Mock()
    opt.add_max_links_to_item_pool.value = True

    opt.add_skill_gems_to_item_pool = True
    opt.add_support_gems_to_item_pool = True

    opt.starting_character = Mock()
    opt.starting_character.value = 1
    opt.starting_character.option_scion = 1
    opt.starting_character.option_marauder = 2
    opt.starting_character.option_duelist = 3
    opt.starting_character.option_ranger = 4
    opt.starting_character.option_shadow = 5
    opt.starting_character.option_witch = 6
    opt.starting_character.option_templar = 7

    opt.usable_starting_gear = Mock()
    opt.usable_starting_gear.value = 0
    opt.usable_starting_gear.option_starting_weapon_flask_and_gems = 0
    opt.usable_starting_gear.option_starting_weapon_and_gems = 1
    opt.usable_starting_gear.option_starting_weapon = 2
    opt.usable_starting_gear.option_starting_weapon_and_flask_slots = 3

    opt.allow_unlock_of_other_characters = Mock()
    opt.allow_unlock_of_other_characters.value = True

    opt.ascendancies_available_per_class = Mock()
    opt.ascendancies_available_per_class.value = 3

    return opt


def _make_world(goal_act=5):
    """Return a mock world wired up with a default item pool and options."""
    world = Mock()
    world.goal_act = goal_act
    world.player = 1
    world.options = _make_options()
    world.random = Mock()
    world.random.sample = lambda population, k: population[:k]

    world.items_to_place = {
        1:   {"id": 1,   "name": "Random Sword",                    "category": ["Random Gear"]},
        2:   {"id": 2,   "name": "Progressive Sword",               "category": ["Progressive Gear"]},
        3:   {"id": 3,   "name": "Life Flask",                      "category": ["Flask"]},
        100: {"id": 100, "name": "Progressive passive point",       "category": ["Passive"], "count": 10},
        101: {"id": 101, "name": "Low Level Gem",                   "category": ["MainSkillGem"], "reqLevel": 10},
        102: {"id": 102, "name": "High Level Gem",                  "category": ["SupportGem"], "reqLevel": 80},
        200: {"id": 200, "name": "Progressive max links - Weapon",  "category": ["max links"], "count": 1},
        300: {"id": 300, "name": "Juggernaut",                      "category": ["Ascendancy", "Marauder Class"]},
        301: {"id": 301, "name": "Berserker",                       "category": ["Ascendancy", "Marauder Class"]},
        302: {"id": 302, "name": "Chieftain",                       "category": ["Ascendancy", "Marauder Class"]},
        400: {"id": 400, "name": "Ascendant",                       "category": ["Ascendancy", "Scion Class"]},
        500: {"id": 500, "name": "Marauder",                        "category": ["Marauder Class"]},
        501: {"id": 501, "name": "Witch",                           "category": ["Witch Class"]},
        502: {"id": 502, "name": "Ranger",                          "category": ["Ranger Class"]},
        600: {"id": 600, "name": "Progressive Flask Slots",         "category": ["Flask"], "count": 5},
    }
    world.item_name_to_id = {item["name"]: item["id"] for item in world.items_to_place.values()}
    world.items_procollected = {}
    world.remove_and_create_item_by_name = Mock()
    world.remove_and_create_items_by_itemdict = Mock(return_value=[])
    world.precollect = Mock()
    world.create_item = Mock()

    world.multiworld = Mock()
    world.multiworld.state = Mock()
    world.multiworld.state.count = Mock(return_value=0)

    world.MAX_GUCCI_GEAR_UPGRADES = 10
    world.MAX_GEAR_UPGRADES = 10
    world.MAX_FLASK_SLOTS = 10
    world.MAX_LINK_UPGRADES = 10
    world.MAX_SKILL_GEMS = 10

    return world


# ---------------------------------------------------------------------------
# setup_early_items
# ---------------------------------------------------------------------------

class TestSetupEarlyItems(PoeTestBase):

    @patch('worlds.poe.Logic.setup_character_items')
    @patch('worlds.poe.Logic.Items.get_gear_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_flask_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_max_links_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_main_skill_gem_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_support_gem_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_by_name', return_value=None)
    @patch('worlds.poe.Logic.Locations.acts', {5: {"maxMonsterLevel": 50}})
    def test_progressive_gear_enabled_removes_random_gear(self, *_mocks):
        world = _make_world()
        world.items_to_place = {
            1: {"id": 1, "name": "Random Sword",    "category": ["Random Gear"]},
            2: {"id": 2, "name": "Progressive Sword","category": ["Progressive Gear"]},
        }
        world.item_name_to_id = {"Random Sword": 1, "Progressive Sword": 2}
        world.options.progressive_gear.value = world.options.progressive_gear.option_enabled

        with patch('worlds.poe.Logic.Items.get_by_category', return_value=[{"name": "Random Sword", "id": 1}]):
            setup_early_items(world)

        self.assertNotIn(1, world.items_to_place, "Random Gear should be removed when progressive enabled")
        self.assertIn(2, world.items_to_place, "Progressive Gear should stay")

    @patch('worlds.poe.Logic.setup_character_items')
    @patch('worlds.poe.Logic.Items.get_gear_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_flask_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_max_links_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_main_skill_gem_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_support_gem_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_by_name', return_value=None)
    @patch('worlds.poe.Logic.Locations.acts', {5: {"maxMonsterLevel": 50}})
    def test_progressive_gear_disabled_removes_progressive_gear(self, *_mocks):
        world = _make_world()
        world.items_to_place = {
            1: {"id": 1, "name": "Random Sword",    "category": ["Random Gear"]},
            2: {"id": 2, "name": "Progressive Sword","category": ["Progressive Gear"]},
        }
        world.item_name_to_id = {"Random Sword": 1, "Progressive Sword": 2}
        world.options.progressive_gear.value = world.options.progressive_gear.option_disabled

        with patch('worlds.poe.Logic.Items.get_by_category', return_value=[{"name": "Progressive Sword", "id": 2}]):
            setup_early_items(world)

        self.assertNotIn(2, world.items_to_place, "Progressive Gear should be removed when disabled")
        self.assertIn(1, world.items_to_place, "Random Gear should stay")

    @patch('worlds.poe.Logic.setup_character_items')
    @patch('worlds.poe.Logic.Items.get_gear_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_flask_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_max_links_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_main_skill_gem_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_support_gem_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_by_name', return_value=None)
    @patch('worlds.poe.Logic.Items.get_by_category', return_value=[])
    @patch('worlds.poe.Logic.Locations.acts', {5: {"maxMonsterLevel": 50}})
    def test_gem_level_filtering_removes_high_level_gems(self, *_mocks):
        world = _make_world()
        world.items_to_place = {
            1: {"id": 1, "name": "Low Level Gem",  "category": ["MainSkillGem"], "reqLevel": 10},
            2: {"id": 2, "name": "High Level Gem", "category": ["SupportGem"],  "reqLevel": 80},
            3: {"id": 3, "name": "Normal Item",    "category": ["Gear"],        "reqLevel": 10},
        }

        setup_early_items(world)

        self.assertIn(1, world.items_to_place,    "Low-level gem should stay")
        self.assertNotIn(2, world.items_to_place, "High-level gem (reqLevel > maxMonsterLevel) should be removed")
        self.assertIn(3, world.items_to_place,    "Non-gem item should stay")

    @patch('worlds.poe.Logic.setup_character_items')
    @patch('worlds.poe.Logic.Items.get_gear_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_flask_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_max_links_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_main_skill_gem_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_support_gem_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_by_name', return_value=None)
    @patch('worlds.poe.Logic.Items.get_by_category', return_value=[])
    @patch('worlds.poe.Logic.Locations.acts', {5: {"maxMonsterLevel": 50}})
    def test_gucci_hobo_mode_upgrades_uniques_to_progression(self, *_mocks):
        world = _make_world()
        unique_item = {"id": 99, "name": "Bringer of Rain", "category": ["Unique"], "classification": ItemClassification.filler}
        world.items_to_place = {99: unique_item}
        world.item_name_to_id = {"Bringer of Rain": 99}
        world.options.gucci_hobo_mode.value = world.options.gucci_hobo_mode.option_no_non_unique_items

        with patch('worlds.poe.Logic.Items.get_gear_items', return_value=[unique_item]):
            setup_early_items(world)

        self.assertEqual(unique_item["classification"], ItemClassification.progression,
                         "Unique items should become progression in gucci_hobo mode")

    @patch('worlds.poe.Logic.setup_character_items')
    @patch('worlds.poe.Logic.Items.get_gear_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_flask_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_max_links_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_main_skill_gem_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_support_gem_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_by_category', return_value=[])
    @patch('worlds.poe.Logic.Locations.acts', {5: {"maxMonsterLevel": 50}})
    def test_passive_points_removed_when_disabled(self, *_mocks):
        world = _make_world()
        passive = {"id": 100, "name": "Progressive passive point", "category": ["Passive"], "count": 10}
        world.items_to_place = {100: passive}
        world.item_name_to_id = {"Progressive passive point": 100}
        world.options.add_passive_skill_points_to_item_pool.value = False

        with patch('worlds.poe.Logic.Items.get_by_name', return_value=passive):
            setup_early_items(world)

        self.assertNotIn(100, world.items_to_place, "Passive points should be removed when disabled")


# ---------------------------------------------------------------------------
# setup_character_items
# ---------------------------------------------------------------------------

class TestSetupCharacterItems(PoeTestBase):

    def _make_char_world(self):
        world = _make_world()
        world.options.usable_starting_gear.value = world.options.usable_starting_gear.option_starting_weapon_flask_and_gems
        return world

    @patch('worlds.poe.Logic.Items.get_ascendancy_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_ascendancy_class_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_base_class_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_max_links_items', return_value=[])
    @patch('worlds.poe.Logic.ItemTable.starting_items_table', {
        "Marauder": {"weapon": "Rusty Sword", "gem": "Cleave", "support": "Ruthless Support"}
    })
    def test_starting_character_is_precollected(self, *_mocks):
        world = self._make_char_world()
        world.options.starting_character.value = world.options.starting_character.option_marauder
        world.options.usable_starting_gear.value = world.options.usable_starting_gear.option_starting_weapon

        char_item = Mock()
        world.remove_and_create_item_by_name = Mock(return_value=char_item)
        world.items_to_place = {"Progressive Rusty Sword": {"id": 999, "name": "Progressive Rusty Sword", "category": []}}
        world.item_name_to_id = {"Progressive Rusty Sword": 999}
        world.options.progressive_gear.value = world.options.progressive_gear.option_enabled

        setup_character_items(world)

        world.precollect.assert_any_call(char_item)

    def test_other_characters_removed_when_not_allowed(self):
        world = self._make_char_world()
        world.options.starting_character.value = world.options.starting_character.option_witch
        world.options.allow_unlock_of_other_characters.value = False
        world.options.usable_starting_gear.value = world.options.usable_starting_gear.option_starting_weapon
        world.options.progressive_gear.value = world.options.progressive_gear.option_disabled

        world.items_to_place = {
            501: {"id": 501, "name": "Witch",    "category": ["Witch Class"]},
            502: {"id": 502, "name": "Marauder", "category": ["Marauder Class"]},
        }
        world.item_name_to_id = {"Witch": 501, "Marauder": 502}

        base_class_items = [{"id": 501, "name": "Witch"}, {"id": 502, "name": "Marauder"}]
        starting_table = {"Witch": {"weapon": "Driftwood Wand", "gem": "Fireball", "support": "Added Fire Damage Support"}}

        with patch('worlds.poe.Logic.Items.get_base_class_items', return_value=base_class_items), \
             patch('worlds.poe.Logic.Items.get_max_links_items', return_value=[]), \
             patch('worlds.poe.Logic.Items.get_ascendancy_items', return_value=[]), \
             patch('worlds.poe.Logic.Items.get_ascendancy_class_items', return_value=[]), \
             patch('worlds.poe.Logic.ItemTable.starting_items_table', starting_table):
            setup_character_items(world)

        self.assertIn(501, world.items_to_place,    "Starting character should stay in pool")
        self.assertNotIn(502, world.items_to_place, "Other characters should be removed")

    @patch('worlds.poe.Logic.Items.get_ascendancy_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_ascendancy_class_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_base_class_items', return_value=[])
    @patch('worlds.poe.Logic.Items.get_max_links_items', return_value=[])
    @patch('worlds.poe.Logic.ItemTable.starting_items_table', {
        "Ranger": {"weapon": "Crude Bow", "gem": "Burning Arrow", "support": "Pierce Support"}
    })
    def test_ascendancies_not_added_for_act_1_goal(self, *_mocks):
        """Goal act < 3 → no ascendancy items added (Labyrinth not reachable)."""
        world = _make_world(goal_act=1)
        world.options.starting_character.value = world.options.starting_character.option_ranger
        world.options.usable_starting_gear.value = world.options.usable_starting_gear.option_starting_weapon
        world.options.progressive_gear.value = world.options.progressive_gear.option_disabled

        asc_item = {"id": 300, "name": "Deadeye", "category": ["Ascendancy", "Ranger Class"]}
        world.items_to_place = {300: asc_item}
        world.item_name_to_id = {"Deadeye": 300}

        with patch('worlds.poe.Logic.Items.get_ascendancy_items', return_value=[asc_item]):
            setup_character_items(world)

        # ascendancy should be stripped (goal < 3, temp_items_to_place never populated)
        self.assertNotIn(300, world.items_to_place, "Ascendancy items should be removed for act-1 goal")


# ---------------------------------------------------------------------------
# get_goal_act
# ---------------------------------------------------------------------------

class TestGetGoalAct(PoeTestBase):

    def setUp(self):
        super().setUp()
        self.world = Mock()
        self.options = Mock()
        self.options.goal = Mock()
        self.options.goal.option_complete_act_1 = 1
        self.options.goal.option_complete_act_2 = 2
        self.options.goal.option_complete_act_3 = 3
        self.options.goal.option_complete_act_4 = 4
        self.options.goal.option_kauri_fortress_act_6 = 5
        self.options.goal.option_complete_act_6 = 6
        self.options.goal.option_complete_act_7 = 7
        self.options.goal.option_complete_act_8 = 8
        self.options.goal.option_complete_act_9 = 9
        self.options.goal.option_complete_the_campaign = 10

    def test_all_goal_act_mappings(self):
        cases = [
            (self.options.goal.option_complete_act_1, 1),
            (self.options.goal.option_complete_act_2, 2),
            (self.options.goal.option_complete_act_3, 3),
            (self.options.goal.option_complete_act_4, 4),
            (self.options.goal.option_kauri_fortress_act_6, 5),
            (self.options.goal.option_complete_act_6, 6),
            (self.options.goal.option_complete_act_7, 7),
            (self.options.goal.option_complete_act_8, 8),
            (self.options.goal.option_complete_act_9, 9),
            (self.options.goal.option_complete_the_campaign, 10),
        ]
        for goal_value, expected_act in cases:
            with self.subTest(goal=goal_value, expected=expected_act):
                self.options.goal.value = goal_value
                self.assertEqual(get_goal_act(self.world, self.options), expected_act)

    def test_unknown_goal_returns_11(self):
        self.options.goal.value = 999
        self.assertEqual(get_goal_act(self.world, self.options), 11)


# ---------------------------------------------------------------------------
# cull_items_to_place
# ---------------------------------------------------------------------------

class TestCullItemsToPlace(PoeTestBase):

    def _make_cull_world(self):
        world = Mock()
        world.player = 1
        world.player_name = "Tester"
        world.random = Mock()
        world.random.sample = lambda population, k: population[:k]
        world.random.choice = lambda seq: seq[0]
        world.precollect = Mock()
        return world

    def test_no_cull_needed_when_counts_match(self):
        world = self._make_cull_world()
        items = {
            1: {"id": 1, "name": "A", "classification": ItemClassification.filler, "count": 2},
        }
        locations = [None, None]  # len == 2

        result = cull_items_to_place(world, items, locations)
        self.assertEqual(sum(i.get("count", 1) for i in result.values()), 2)

    def test_filler_culled_before_useful(self):
        world = self._make_cull_world()
        items = {
            1: {"id": 1, "name": "Filler", "classification": ItemClassification.filler, "count": 3},
            2: {"id": 2, "name": "Useful", "classification": ItemClassification.useful,  "count": 3},
        }
        locations = [None] * 4  # need to drop 2

        result = cull_items_to_place(world, items, locations)
        total = sum(i.get("count", 1) for i in result.values())
        self.assertEqual(total, 4)
        # filler should be reduced/removed first
        filler_remaining = result.get(1, {}).get("count", 0)
        useful_remaining = result.get(2, {}).get("count", 3)
        self.assertLessEqual(filler_remaining, 1, "Filler should be culled down first")
        self.assertEqual(useful_remaining, 3, "Useful should not be touched while filler remains")

    def test_entire_item_removed_when_count_fits_budget(self):
        world = self._make_cull_world()
        items = {
            1: {"id": 1, "name": "Filler", "classification": ItemClassification.filler, "count": 2},
            2: {"id": 2, "name": "Prog",   "classification": ItemClassification.progression, "count": 3},
        }
        locations = [None] * 3  # need to remove 2 (all of item 1)

        result = cull_items_to_place(world, items, locations)
        self.assertNotIn(1, result, "Filler item with count == cull amount should be fully removed")
        self.assertIn(2, result,    "Progression item should never be culled")

    def test_item_count_reduced_when_partial_cull_needed(self):
        world = self._make_cull_world()
        items = {
            1: {"id": 1, "name": "Filler", "classification": ItemClassification.filler, "count": 5},
        }
        locations = [None] * 3  # need to drop 2

        result = cull_items_to_place(world, items, locations)
        self.assertIn(1, result)
        self.assertEqual(result[1]["count"], 3, "Count should be reduced by the cull amount")

    def test_progression_items_never_culled(self):
        world = self._make_cull_world()
        items = {
            1: {"id": 1, "name": "Prog", "classification": ItemClassification.progression, "count": 5},
        }
        locations = [None] * 2  # need to cull 3, but nothing eligible

        result = cull_items_to_place(world, items, locations)
        # No filler/useful → error logged and loop breaks; items unchanged (or precollect fallback)
        # Either way, progression item must not be removed
        self.assertIn(1, result, "Progression items should never be removed by culling")


# ---------------------------------------------------------------------------
# deprioritize_non_logic_gems
# ---------------------------------------------------------------------------

class TestDeprioritizeNonLogicGems(PoeTestBase):

    def _make_gem_world(self, goal_act=2):
        world = Mock()
        world.goal_act = goal_act
        world.random = Mock()
        world.random.sample = lambda population, k: population[:k]
        opt = Mock()
        opt.skill_gems_per_act = Mock(value=2)
        opt.support_gems_per_act = Mock(value=1)
        world.options = opt
        return world

    def test_empty_gem_table_returns_unchanged(self):
        world = self._make_gem_world()
        table = {1: {"id": 1, "name": "Sword", "category": ["Gear"], "classification": ItemClassification.useful}}
        with patch('worlds.poe.Logic.Items.get_all_gems', return_value=[]):
            result = deprioritize_non_logic_gems(world, table)
        self.assertEqual(result, table)

    def test_selected_gems_become_progression(self):
        world = self._make_gem_world(goal_act=1)
        gem = {"id": 1, "name": "Fireball", "category": ["MainSkillGem"], "reqLevel": 1,
               "classification": ItemClassification.useful}
        table = {1: gem}

        with patch('worlds.poe.Logic.Items.get_all_gems', return_value=[gem]), \
             patch('worlds.poe.Logic.Items.get_main_skill_gem_items', return_value=[gem]), \
             patch('worlds.poe.Logic.Items.get_support_gem_items', return_value=[]), \
             patch('worlds.poe.Logic.Items.get_utility_skill_gem_items', return_value=[]), \
             patch('worlds.poe.Logic.Items.get_by_has_every_category', return_value=[]), \
             patch('worlds.poe.Logic.Locations.acts', {1: {"maxMonsterLevel": 10}}):
            result = deprioritize_non_logic_gems(world, table)

        self.assertEqual(result[1]["classification"], ItemClassification.progression,
                         "Sampled gem should become progression")

    def test_unselected_progression_gems_downgraded_to_useful(self):
        world = self._make_gem_world(goal_act=1)
        # gem_a: reqLevel=1 → selected in act-0 starter sample
        # gem_b: reqLevel=2, maxMonsterLevel=1 → ineligible for act-0 (reqLevel != 1) and
        #        ineligible for act loop (reqLevel > maxMonsterLevel) → never selected → downgraded
        gem_a = {"id": 1, "name": "Fireball",  "category": ["MainSkillGem"], "reqLevel": 1,
                 "classification": ItemClassification.progression}
        gem_b = {"id": 2, "name": "Frostbolt", "category": ["MainSkillGem"], "reqLevel": 2,
                 "classification": ItemClassification.progression}
        table = {1: gem_a, 2: gem_b}

        def main_gems_side_effect(tbl=None):
            return [gem_a, gem_b]

        with patch('worlds.poe.Logic.Items.get_all_gems', return_value=[gem_a, gem_b]), \
             patch('worlds.poe.Logic.Items.get_main_skill_gem_items', side_effect=main_gems_side_effect), \
             patch('worlds.poe.Logic.Items.get_support_gem_items', return_value=[]), \
             patch('worlds.poe.Logic.Items.get_utility_skill_gem_items', return_value=[]), \
             patch('worlds.poe.Logic.Items.get_by_has_every_category', return_value=[]), \
             patch('worlds.poe.Logic.Locations.acts', {1: {"maxMonsterLevel": 1}}):
            result = deprioritize_non_logic_gems(world, table)

        selected = [gid for gid, g in result.items() if g["classification"] == ItemClassification.progression]
        downgraded = [gid for gid, g in result.items() if g["classification"] == ItemClassification.useful]
        self.assertEqual(len(selected), 1,   "Only sampled gem should be progression")
        self.assertEqual(len(downgraded), 1, "Unsampled progression gem should be downgraded to useful")


if __name__ == '__main__':
    unittest.main()
