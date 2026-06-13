"""
Tests for the Path of Exile Rules module
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from BaseClasses import CollectionState
from worlds.poe import Rules, PathOfExileWorld
from worlds.poe.Rules import (
    get_ascendancy_amount_for_act, get_gear_amount_for_act, get_flask_amount_for_act,
    get_gem_link_amount_for_act, get_skill_gem_amount_for_act, get_support_gem_amount_for_act,
    get_passives_amount_for_act, completion_condition, can_reach, SelectLocationsToAdd
)
from . import PoeTestBase


class TestActRequirementFunctions(unittest.TestCase):
    """Test functions that calculate requirements for each act"""
    
    def setUp(self):
        self.mock_opt = Mock()
        self.mock_opt.ascendancies_available_per_class.value = 3
        self.mock_opt.starting_character.value = 2  # Marauder (Not Scion)
        self.mock_opt.starting_character.option_scion = 1
        self.mock_opt.gear_upgrades_per_act.value = 5
        self.mock_opt.gucci_hobo_mode.value = 0  # disabled
        self.mock_opt.gucci_hobo_mode.option_disabled = 0
        self.mock_opt.add_flasks_to_item_pool = Mock(value=True)
        self.mock_opt.flasks_per_act.value = 2
        self.mock_opt.add_max_links_to_item_pool = Mock(value=True)
        self.mock_opt.max_links_per_act.value = 3
        self.mock_opt.skill_gems_per_act.value = 4
        self.mock_opt.support_gems_per_act.value = 3
        self.mock_opt.add_passive_skill_points_to_item_pool.value = True
        self.mock_opt.add_skill_gems_to_item_pool = Mock(value=True)
        self.mock_opt.add_support_gems_to_item_pool = Mock(value=True)
        self.mock_world = Mock()
        self.mock_world.options = self.mock_opt
        self.mock_world.placed_total_gear_upgrades = PathOfExileWorld.MAX_GEAR_UPGRADES
        self.mock_world.placed_total_flask_slots = PathOfExileWorld.MAX_FLASK_SLOTS
        self.mock_world.placed_total_link_upgrades = PathOfExileWorld.MAX_LINK_UPGRADES
        self.mock_world.placed_total_skill_gems = PathOfExileWorld.MAX_SKILL_GEMS
        self.mock_world.placed_total_support_gems = PathOfExileWorld.MAX_SUPPORT_GEMS
    
    def test_get_ascendancy_amount_for_act(self):
        """Test ascendancy amount calculation"""
        # Act 3 and above should return ascendancy amount
        self.assertEqual(get_ascendancy_amount_for_act(3, self.mock_world), 3)
        self.assertEqual(get_ascendancy_amount_for_act(4, self.mock_world), 3)
        # Other acts should return 0
        self.assertEqual(get_ascendancy_amount_for_act(1, self.mock_world), 0)
        self.assertEqual(get_ascendancy_amount_for_act(2, self.mock_world), 0)

    
    def test_get_ascendancy_amount_for_scion(self):
        """Test ascendancy amount for Scion character"""
        self.mock_opt.starting_character.value = self.mock_opt.starting_character.option_scion

        result = get_ascendancy_amount_for_act(3, self.mock_world)
        self.assertEqual(result, 2)  # Scion capped at min(ascendancies_per_class=3, scion_max=2) = 2
    
    def test_get_gear_amount_for_act(self):
        """Test gear amount calculation"""
        # Act 1 should give 0 gear (act - 1)
        self.assertEqual(get_gear_amount_for_act(1, self.mock_world), 0)

        # Act 3 should give 10 gear (5 * 2)
        self.assertEqual(get_gear_amount_for_act(3, self.mock_world), 10)

        # Test cap: placed_total_gear_upgrades acts as ceiling
        self.mock_world.placed_total_gear_upgrades = PathOfExileWorld.MAX_GUCCI_GEAR_UPGRADES
        result = get_gear_amount_for_act(20, self.mock_world)
        self.assertEqual(result, PathOfExileWorld.MAX_GUCCI_GEAR_UPGRADES)
    
    def test_get_flask_amount_for_act(self):
        """Test flask amount calculation"""
        self.assertEqual(get_flask_amount_for_act(1, self.mock_world), 2)  # 2 * act(1)
        self.assertEqual(get_flask_amount_for_act(3, self.mock_world), 6)  # 2 * act(3)

        # Test with flask slots disabled
        self.mock_opt.add_flasks_to_item_pool = False
        self.assertEqual(get_flask_amount_for_act(3, self.mock_world), 0)
    
    def test_get_gem_amount_for_act(self):
        """Test gem slot amount calculation"""
        self.assertEqual(get_gem_link_amount_for_act(1, self.mock_world), 3)  # 3 * act(1)
        self.assertEqual(get_gem_link_amount_for_act(3, self.mock_world), 9)  # 3 * act(3)

        # Test with max links disabled
        self.mock_opt.add_max_links_to_item_pool = False
        self.assertEqual(get_gem_link_amount_for_act(3, self.mock_world), 0)
    
    def test_get_skill_gem_amount_for_act(self):
        """Test skill gem amount calculation"""
        self.assertEqual(get_skill_gem_amount_for_act(1, self.mock_world), 0)
        self.assertEqual(get_skill_gem_amount_for_act(3, self.mock_world), 8)  # 4 * 2

        # Test max cap
        result = get_skill_gem_amount_for_act(20, self.mock_world)
        self.assertEqual(result, PathOfExileWorld.MAX_SKILL_GEMS)
    
    def test_get_support_gem_amount_for_act(self):
        """Test support gem amount calculation"""
        self.assertEqual(get_support_gem_amount_for_act(1, self.mock_world), 0)
        self.assertEqual(get_support_gem_amount_for_act(3, self.mock_world), 6)  # 3 * 2

        # Test max cap
        result = get_support_gem_amount_for_act(20, self.mock_world)
        self.assertEqual(result, PathOfExileWorld.MAX_SUPPORT_GEMS)
    
    def test_get_passives_amount_for_act(self):
        """Test passive points amount calculation"""
        self.assertEqual(get_passives_amount_for_act(1, self.mock_world), 6)
        self.assertEqual(get_passives_amount_for_act(5, self.mock_world), 56)
        self.assertEqual(get_passives_amount_for_act(12, self.mock_world), 136)

        # Test with passive points disabled
        self.mock_opt.add_passive_skill_points_to_item_pool.value = False
        self.assertEqual(get_passives_amount_for_act(5, self.mock_world), 0)

        # Test with act not in table
        self.mock_opt.add_passive_skill_points_to_item_pool.value = True
        self.assertEqual(get_passives_amount_for_act(99, self.mock_world), 0)


class TestCompletionCondition(PoeTestBase):
    """Test completion condition logic"""
    
    def setUp(self):
        super().setUp()
        self.mock_world = Mock()
        self.mock_state = Mock(spec=CollectionState)
    
    @patch('worlds.poe.Rules.can_reach')
    def test_completion_condition_with_bosses(self, mock_can_reach):
        """Test completion condition when bosses are required"""
        self.mock_world.bosses_for_goal = ["shaper", "elder"]
        self.mock_world.goal_act = 10
        mock_can_reach.return_value = True
        
        result = completion_condition(self.mock_world, self.mock_state)
        
        self.assertTrue(result)
        mock_can_reach.assert_called_once_with(11, self.mock_world, self.mock_state)
    
    @patch('worlds.poe.Rules.can_reach')
    def test_completion_condition_without_bosses(self, mock_can_reach):
        """Test completion condition when only act completion is required"""
        self.mock_world.bosses_for_goal = []
        self.mock_world.goal_act = 8
        mock_can_reach.return_value = True
        
        result = completion_condition(self.mock_world, self.mock_state)
        
        self.assertTrue(result)
        mock_can_reach.assert_called_once_with(8, self.mock_world, self.mock_state)


class TestCanReach(PoeTestBase):
    """Test can_reach logic function"""
    
    def setUp(self):
        super().setUp()
        self.mock_world = Mock()
        self.mock_state = Mock(spec=CollectionState)
        self.mock_options = Mock()
        
        # Setup default options
        self.mock_options.disable_generation_logic.value = False
        self.mock_options.ascendancies_available_per_class.value = 3
        self.mock_options.starting_character.value = 2  # Marauder
        self.mock_options.starting_character.option_scion = 1
        self.mock_options.starting_character.current_option_name = "Marauder"
        self.mock_options.gear_upgrades_per_act.value = 2
        self.mock_options.gucci_hobo_mode.value = 0
        self.mock_options.gucci_hobo_mode.option_disabled = 0
        self.mock_options.add_flasks_to_item_pool = Mock(value=True)
        self.mock_options.flasks_per_act.value = 1
        self.mock_options.add_max_links_to_item_pool = Mock(value=True)
        self.mock_options.max_links_per_act.value = 1
        self.mock_options.skill_gems_per_act.value = 2
        self.mock_options.support_gems_per_act.value = 1
        self.mock_options.add_passive_skill_points_to_item_pool.value = True
        self.mock_options.add_skill_gems_to_item_pool = Mock(value=True)
        self.mock_options.add_support_gems_to_item_pool = Mock(value=True)

        self.mock_world.options = self.mock_options
        self.mock_world.player = 1
        self.mock_world.placed_total_gear_upgrades = PathOfExileWorld.MAX_GEAR_UPGRADES
        self.mock_world.placed_total_flask_slots = PathOfExileWorld.MAX_FLASK_SLOTS
        self.mock_world.placed_total_link_upgrades = PathOfExileWorld.MAX_LINK_UPGRADES
        self.mock_world.placed_total_skill_gems = PathOfExileWorld.MAX_SKILL_GEMS
        self.mock_world.placed_total_support_gems = PathOfExileWorld.MAX_SUPPORT_GEMS
    
    def test_can_reach_early_act(self):
        """Test can_reach for acts before act 1"""
        result = can_reach(0, self.mock_world, self.mock_state)
        self.assertTrue(result)
        
        result = can_reach(-1, self.mock_world, self.mock_state)
        self.assertTrue(result)
    
    def test_can_reach_with_disabled_logic(self):
        """Test can_reach when generation logic is disabled"""
        self.mock_options.disable_generation_logic.value = True
        
        result = can_reach(5, self.mock_world, self.mock_state)
        self.assertTrue(result)
    
    @patch('worlds.poe.Items.get_by_category')
    @patch('worlds.poe.Items.get_ascendancy_class_items')
    @patch('worlds.poe.Items.get_gear_items')
    @patch('worlds.poe.Items.get_flask_items')
    @patch('worlds.poe.Items.get_support_gem_items')
    @patch('worlds.poe.Items.get_max_links_items')
    @patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon')
    @patch('worlds.poe.Rules.acts')
    def test_can_reach_act_1_requirements(self, mock_acts, mock_gems_by_weapon, mock_max_links, 
                                         mock_support_gems, mock_flask_items, 
                                         mock_gear_items, mock_ascendancy_items, 
                                         mock_get_by_category):
        """Test can_reach for act 1 with specific requirements"""
        
        # Mock acts data
        mock_acts.__getitem__.return_value = {"maxMonsterLevel": 10}
        
        # Mock item returns using real item names from Items.json
        mock_weapon_items = [
            {"name": "Progressive Sword"}, 
            {"name": "Progressive Axe"}, 
            {"name": "Progressive Bow"}
        ]
        mock_get_by_category.return_value = mock_weapon_items
        mock_ascendancy_items.return_value = [{"name": "Berserker"}]
        mock_gear_items.return_value = [
            {"name": "Progressive BodyArmour"}, 
            {"name": "Progressive Helmet"}
        ]
        mock_flask_items.return_value = [{"name": "Progressive Flask Unlock"}]
        mock_support_gems.return_value = [{"name": "Chance to Bleed Support"}]
        mock_max_links.return_value = [{"name": "Progressive max links - Weapon"}]
        mock_gems_by_weapon.return_value = [
            {"name": "Fireball"}, {"name": "Freezing Pulse"}, 
            {"name": "Spark"}, {"name": "Lightning Tendrils"},
            {"name": "Crushing Fist"}
        ]
        
        # Mock state counts - sufficient for all requirements
        self.mock_state.has_from_list.return_value = True
        self.mock_state.count_from_list.return_value = 10
        self.mock_state.count.return_value = 50
        
        result = can_reach(1, self.mock_world, self.mock_state)
        self.assertTrue(result)
    
    @patch('worlds.poe.Items.get_by_category')
    @patch('worlds.poe.Items.get_ascendancy_class_items')
    @patch('worlds.poe.Items.get_gear_items')
    @patch('worlds.poe.Items.get_flask_items')
    @patch('worlds.poe.Items.get_support_gem_items')
    @patch('worlds.poe.Items.get_max_links_items')
    @patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon')
    @patch('worlds.poe.Rules.acts')
    def test_can_reach_insufficient_requirements(self, mock_acts, mock_gems_by_weapon, mock_max_links,
                                                mock_support_gems, mock_flask_items,
                                                mock_gear_items, mock_ascendancy_items,
                                                mock_get_by_category):
        """Test can_reach when requirements are not met"""
        
        # Mock acts data
        mock_acts.__getitem__.return_value = {"maxMonsterLevel": 30}
        
        # Mock insufficient items
        mock_get_by_category.return_value = []
        mock_ascendancy_items.return_value = []
        mock_gear_items.return_value = []
        mock_flask_items.return_value = []
        mock_support_gems.return_value = []
        mock_max_links.return_value = []
        mock_gems_by_weapon.return_value = []
        
        # Mock insufficient state counts
        self.mock_state.has_from_list.return_value = False
        self.mock_state.count_from_list.return_value = 0
        self.mock_state.count.return_value = 0
        
        result = can_reach(3, self.mock_world, self.mock_state)
        self.assertFalse(result)
    
    @patch('worlds.poe.Items.get_by_category')
    @patch('worlds.poe.Items.get_ascendancy_class_items')
    @patch('worlds.poe.Items.get_gear_items')
    @patch('worlds.poe.Items.get_flask_items')
    @patch('worlds.poe.Items.get_support_gem_items')
    @patch('worlds.poe.Items.get_max_links_items')
    @patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon')
    @patch('worlds.poe.Rules.acts')
    def test_can_reach_act_1_armor_categories(self, mock_acts, mock_gems, mock_max_links, 
                                             mock_support, mock_flask, mock_gear, 
                                             mock_ascendancy, mock_get_by_category):
        """Test act 1 armor category requirements"""
        
        # Mock acts data
        mock_acts.__getitem__.return_value = {"maxMonsterLevel": 10}
        
        # Setup mocks with real item names
        mock_get_by_category.return_value = [{"name": "Progressive Sword"}]
        mock_ascendancy.return_value = []
        mock_gear.return_value = [{"name": "Progressive BodyArmour"}]
        mock_flask.return_value = [{"name": "Progressive Flask Unlock"}] * 5
        mock_support.return_value = []
        mock_max_links.return_value = []
        mock_gems.return_value = [{"name": "Fireball"}] * 10
        
        # Mock state to have enough items for most requirements but test armor categories
        def mock_has_from_list(items, player, count):
            item_names = [item["name"] if isinstance(item, dict) else str(item) for item in items]
            # Return True for helmet and body armour (2 categories)
            if any("Helmet" in name or "BodyArmour" in name for name in item_names):
                return True
            return len(items) > 0
        
        self.mock_state.has_from_list.side_effect = mock_has_from_list
        self.mock_state.count_from_list.return_value = 10
        self.mock_state.count.return_value = 10
        
        result = can_reach(1, self.mock_world, self.mock_state)
        self.assertTrue(result)


class TestSelectLocationsToAdd(PoeTestBase):
    """Test location selection logic"""
    
    def setUp(self):
        super().setUp()
        self.mock_world = Mock()
        self.mock_world.goal_act = 3
        self.mock_world.random = Mock()
        self.mock_world.random.sample = Mock(side_effect=lambda x, k: x[:k])
        self.mock_world.random.shuffle = Mock()
        
        self.mock_options = Mock()
        self.mock_options.add_leveling_up_to_location_pool = True
        # Add proper numeric values for the Mock objects
        self.mock_options.gear_upgrades_per_act.value = 2
        self.mock_options.ascendancies_available_per_class.value = 3
        self.mock_options.starting_character.value = 2  # Marauder
        self.mock_options.starting_character.option_scion = 1
        self.mock_options.gucci_hobo_mode.value = 0
        self.mock_options.gucci_hobo_mode.option_disabled = 0
        self.mock_options.add_flasks_to_item_pool = Mock(value=True)
        self.mock_options.flasks_per_act.value = 1
        self.mock_options.add_max_links_to_item_pool = Mock(value=True)
        self.mock_options.max_links_per_act.value = 1
        self.mock_options.skill_gems_per_act.value = 2
        self.mock_options.support_gems_per_act.value = 1
        self.mock_options.add_passive_skill_points_to_item_pool.value = True
        self.mock_options.add_skill_gems_to_item_pool = Mock(value=True)
        self.mock_options.add_support_gems_to_item_pool = Mock(value=True)

        self.mock_world.options = self.mock_options
        self.mock_world.placed_total_gear_upgrades = PathOfExileWorld.MAX_GEAR_UPGRADES
        self.mock_world.placed_total_flask_slots = PathOfExileWorld.MAX_FLASK_SLOTS
        self.mock_world.placed_total_link_upgrades = PathOfExileWorld.MAX_LINK_UPGRADES
        self.mock_world.placed_total_skill_gems = PathOfExileWorld.MAX_SKILL_GEMS
        self.mock_world.placed_total_support_gems = PathOfExileWorld.MAX_SUPPORT_GEMS

        # Mock locations data
        self.mock_base_item_locations = {
            "loc1": {"name": "Location 1", "act": 1},
            "loc2": {"name": "Location 2", "act": 2},
            "loc3": {"name": "Location 3", "act": 3},
            "loc4": {"name": "Location 4", "act": 4},  # Should be excluded
        }
        
        self.mock_level_locations = {
            "level1": {"name": "Level 5", "level": 5, "act": 1},
            "level2": {"name": "Level 10", "level": 10, "act": 2},
            "level3": {"name": "Level 100", "level": 100, "act": 11},  # Should be excluded by max level
        }
        
        self.mock_acts = {
            1: {"maxMonsterLevel": 8},
            2: {"maxMonsterLevel": 15},
            3: {"maxMonsterLevel": 25},
        }
    
    @patch('worlds.poe.Rules.base_item_type_locations', new_callable=lambda: {})
    @patch('worlds.poe.Rules.level_locations', new_callable=lambda: {})
    @patch('worlds.poe.Rules.acts', new_callable=lambda: {})
    def test_select_locations_to_add_basic(self, mock_acts, mock_level_locs, mock_base_locs):
        """Test basic location selection"""
        mock_base_locs.update(self.mock_base_item_locations)
        mock_level_locs.update(self.mock_level_locations)
        mock_acts.update(self.mock_acts)
        
        result = SelectLocationsToAdd(self.mock_world, 5)
        
        # Should return list of locations
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 5)
    
    @patch('worlds.poe.Rules.base_item_type_locations', new_callable=lambda: {})
    @patch('worlds.poe.Rules.level_locations', new_callable=lambda: {})
    @patch('worlds.poe.Rules.acts', new_callable=lambda: {})
    def test_select_locations_excludes_high_acts(self, mock_acts, mock_level_locs, mock_base_locs):
        """Test that locations from acts higher than goal_act are excluded"""
        mock_base_locs.update(self.mock_base_item_locations)
        mock_level_locs.update(self.mock_level_locations)
        mock_acts.update(self.mock_acts)
        
        result = SelectLocationsToAdd(self.mock_world, 10)
        
        # Should not include location from act 4
        location_names = [loc["name"] for loc in result]
        self.assertNotIn("Location 4", location_names)
    
    @patch('worlds.poe.Rules.base_item_type_locations', new_callable=lambda: {})
    @patch('worlds.poe.Rules.level_locations', new_callable=lambda: {})
    @patch('worlds.poe.Rules.acts', new_callable=lambda: {})
    def test_select_locations_excludes_high_level(self, mock_acts, mock_level_locs, mock_base_locs):
        """Test that level locations above max monster level are excluded"""
        mock_base_locs.update(self.mock_base_item_locations)
        mock_level_locs.update(self.mock_level_locations)
        mock_acts.update(self.mock_acts)
        
        result = SelectLocationsToAdd(self.mock_world, 10)
        
        # Should not include level 100 location
        location_names = [loc["name"] for loc in result]
        self.assertNotIn("Level 100", location_names)
    
    @patch('worlds.poe.Rules.base_item_type_locations', new_callable=lambda: {})
    @patch('worlds.poe.Rules.level_locations', new_callable=lambda: {})
    @patch('worlds.poe.Rules.acts', new_callable=lambda: {})
    def test_select_locations_without_leveling(self, mock_acts, mock_level_locs, mock_base_locs):
        """Test location selection when leveling locations are disabled"""
        mock_base_locs.update(self.mock_base_item_locations)
        mock_level_locs.update(self.mock_level_locations)
        mock_acts.update(self.mock_acts)
        
        self.mock_options.add_leveling_up_to_location_pool = False
        
        result = SelectLocationsToAdd(self.mock_world, 10)
        
        # Should not include any level locations
        location_names = [loc["name"] for loc in result]
        self.assertNotIn("Level 5", location_names)
        self.assertNotIn("Level 10", location_names)


class TestConstants(unittest.TestCase):
    """Test module constants"""

    
    def test_constants_are_reasonable(self):
        """Test that constants have reasonable values"""
        self.assertGreater(PathOfExileWorld.MAX_GUCCI_GEAR_UPGRADES, 0)
        self.assertGreater(PathOfExileWorld.MAX_GEAR_UPGRADES, PathOfExileWorld.MAX_GUCCI_GEAR_UPGRADES)
        self.assertGreater(PathOfExileWorld.MAX_FLASK_SLOTS, 0)
        self.assertGreater(PathOfExileWorld.MAX_LINK_UPGRADES, 0)
        self.assertGreater(PathOfExileWorld.MAX_SKILL_GEMS, 0)
        self.assertGreater(PathOfExileWorld.MAX_SUPPORT_GEMS, 0)
    
    def test_armor_categories(self):
        """Test armor categories list"""
        expected_categories = ["BodyArmour", "Boots", "Gloves", "Helmet", "Amulet", 
                             "Belt", "Ring (left)", "Ring (right)", "Quiver", "Shield"]
        self.assertEqual(Rules.armor_categories, expected_categories)
    
    def test_weapon_categories(self):
        """Test weapon categories list"""
        expected_weapons = ["Axe", "Bow", "Claw", "Dagger", "Mace", "Sceptre", 
                          "Staff", "Sword", "Wand"]
        self.assertEqual(Rules.weapon_categories, expected_weapons)
    
    def test_passives_required_for_act(self):
        """Test passive points required for each act"""
        self.assertIn(1, Rules.passives_required_for_act)
        self.assertIn(12, Rules.passives_required_for_act)
        self.assertEqual(Rules.passives_required_for_act[1], 6)
        self.assertEqual(Rules.passives_required_for_act[12], 136)


class TestCanReachFunction(PoeTestBase):
    """Comprehensive tests for the can_reach function"""
    
    def setUp(self):
        super().setUp()
        # Clear cache before each test
        # clear_item_cache() # This function does not exist
        
        self.mock_world = Mock()
        self.mock_state = Mock(spec=CollectionState)
        self.mock_options = Mock()
        
        # Setup comprehensive default options
        self.mock_options.disable_generation_logic.value = False
        self.mock_options.ascendancies_available_per_class.value = 3
        self.mock_options.starting_character.value = 2  # Marauder
        self.mock_options.starting_character.option_scion = 1
        self.mock_options.starting_character.current_option_name = "Marauder"
        self.mock_options.gear_upgrades_per_act.value = 2
        self.mock_options.gucci_hobo_mode.value = 0
        self.mock_options.gucci_hobo_mode.option_disabled = 0
        self.mock_options.add_flasks_to_item_pool = Mock(value=True)
        self.mock_options.flasks_per_act.value = 1
        self.mock_options.add_max_links_to_item_pool = Mock(value=True)
        self.mock_options.max_links_per_act.value = 1
        self.mock_options.skill_gems_per_act.value = 2
        self.mock_options.support_gems_per_act.value = 1
        self.mock_options.add_passive_skill_points_to_item_pool.value = True
        self.mock_options.add_skill_gems_to_item_pool = Mock(value=True)
        self.mock_options.add_support_gems_to_item_pool = Mock(value=True)

        self.mock_world.options = self.mock_options
        self.mock_world.player = 1
        self.mock_world.placed_total_gear_upgrades = PathOfExileWorld.MAX_GEAR_UPGRADES
        self.mock_world.placed_total_flask_slots = PathOfExileWorld.MAX_FLASK_SLOTS
        self.mock_world.placed_total_link_upgrades = PathOfExileWorld.MAX_LINK_UPGRADES
        self.mock_world.placed_total_skill_gems = PathOfExileWorld.MAX_SKILL_GEMS
        self.mock_world.placed_total_support_gems = PathOfExileWorld.MAX_SUPPORT_GEMS
        
        # Setup default item mocks using real names from Items.json
        self.setup_default_item_mocks()
        
        # Setup default state mocks
        self.setup_default_state_mocks()
    
    def setup_default_item_mocks(self):
        """Setup default mocks for all item functions using real item names"""
        self.weapon_items = [
            {"name": "Progressive Sword"}, 
            {"name": "Progressive Axe"}, 
            {"name": "Progressive Bow"}
        ]
        self.armor_items = [
            {"name": "Progressive Helmet"}, 
            {"name": "Progressive BodyArmour"}, 
            {"name": "Progressive Boots"}
        ]
        self.ascendancy_items = [
            {"name": "Berserker"}, {"name": "Juggernaut"}, {"name": "Chieftain"}
        ]
        self.gear_items = [
            {"name": "Progressive BodyArmour"}, 
            {"name": "Progressive Helmet"},
            {"name": "Progressive Boots"},
            {"name": "Progressive Gloves"},
            {"name": "Progressive Belt"},
            {"name": "Progressive Ring"},
            {"name": "Progressive Amulet"},
            {"name": "Progressive Shield"}
        ]
        self.flask_items = [
            {"name": "Progressive Flask Unlock", "category": ["Flask"]},
            {"name": "Progressive Flask Unlock 2", "category": ["Flask"]},
            {"name": "Progressive Flask Unlock 3", "category": ["Flask"]},
            {"name": "Progressive Flask Unlock 4", "category": ["Flask"]},
            {"name": "Progressive Flask Unlock 5", "category": ["Flask"]}
        ]
        self.support_gem_items = [
            {"name": "Chance to Bleed Support"}, {"name": "Added Fire Damage Support"},
            {"name": "Melee Physical Damage Support"}, {"name": "Faster Attacks Support"},
            {"name": "Multistrike Support"}
        ]
        self.max_links_items = [
            {"name": "Progressive max links - Weapon"}, {"name": "Progressive max links - Body Armour"},
            {"name": "Progressive max links - Helmet"}, {"name": "Progressive max links - Boots"},
            {"name": "Progressive max links - Gloves"}
        ]
        self.skill_gem_items = [
            {"name": "Fireball"}, {"name": "Freezing Pulse"}, {"name": "Lightning Bolt"},
            {"name": "Ice Crash"}, {"name": "Earthquake"}, {"name": "Split Arrow"},
            {"name": "Explosive Arrow"}, {"name": "Cleave"}, {"name": "Spectral Throw"},
            {"name": "Lightning Strike"}
        ]
    
    def setup_default_state_mocks(self):
        """Setup default state mocks for sufficient resources"""
        def mock_has_from_list(items, player, count):
            # Return True for any non-empty item list
            return len(items) > 0
        
        def mock_count_from_list(items, player):
            # Return a reasonable count for any item list
            return max(len(items), 5)
        
        def mock_count(item_name, player):
            # Return sufficient passive points
            return 50
        
        self.mock_state.has_from_list.side_effect = mock_has_from_list
        self.mock_state.count_from_list.side_effect = mock_count_from_list
        self.mock_state.count.side_effect = mock_count
    
    def test_can_reach_early_acts(self):
        """Test can_reach for acts before act 1"""
        # Test act 0 and negative acts
        self.assertTrue(can_reach(0, self.mock_world, self.mock_state))
        self.assertTrue(can_reach(-1, self.mock_world, self.mock_state))
        self.assertTrue(can_reach(-10, self.mock_world, self.mock_state))
    
    def test_can_reach_disabled_logic(self):
        """Test can_reach when generation logic is disabled"""
        self.mock_options.disable_generation_logic.value = True
        
        # Should return True for any act when logic is disabled
        self.assertTrue(can_reach(1, self.mock_world, self.mock_state))
        self.assertTrue(can_reach(5, self.mock_world, self.mock_state))
        self.assertTrue(can_reach(10, self.mock_world, self.mock_state))
    
    @patch('worlds.poe.Items.get_by_category')
    @patch('worlds.poe.Items.get_ascendancy_class_items') 
    @patch('worlds.poe.Items.get_gear_items')
    @patch('worlds.poe.Items.get_flask_items')
    @patch('worlds.poe.Items.get_support_gem_items')
    @patch('worlds.poe.Items.get_max_links_items')
    @patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon')
    @patch('worlds.poe.Rules.acts')
    def test_can_reach_act_1_sufficient_resources(self, mock_acts, mock_skill_gems, 
                                                 mock_max_links, mock_support_gems, 
                                                 mock_flask_items, mock_gear_items,
                                                 mock_ascendancy_items, mock_get_by_category):
        """Test can_reach for act 1 with sufficient resources"""
        mock_acts.__getitem__.return_value = {"maxMonsterLevel": 10}
        
        # Setup mocks to return our test data
        mock_get_by_category.return_value = self.weapon_items
        mock_ascendancy_items.return_value = self.ascendancy_items
        mock_gear_items.return_value = self.gear_items
        mock_flask_items.return_value = self.flask_items
        mock_support_gems.return_value = self.support_gem_items
        mock_max_links.return_value = self.max_links_items
        mock_skill_gems.return_value = self.skill_gem_items
        
        result = can_reach(1, self.mock_world, self.mock_state)
        self.assertTrue(result)
    
    @patch('worlds.poe.Items.get_by_category')
    @patch('worlds.poe.Items.get_ascendancy_class_items')
    @patch('worlds.poe.Items.get_gear_items')
    @patch('worlds.poe.Items.get_flask_items')
    @patch('worlds.poe.Items.get_support_gem_items')
    @patch('worlds.poe.Items.get_max_links_items')
    @patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon')
    @patch('worlds.poe.Rules.acts')
    def test_can_reach_act_1_insufficient_skill_gems(self, mock_acts, mock_skill_gems,
                                                    mock_max_links, mock_support_gems,
                                                    mock_flask_items, mock_gear_items,
                                                    mock_ascendancy_items, mock_get_by_category):
        """Test can_reach for act 1 with insufficient skill gems"""
        mock_acts.__getitem__.return_value = {"maxMonsterLevel": 10}
        
        # Setup mocks - most items available but no skill gems
        mock_get_by_category.return_value = self.weapon_items
        mock_ascendancy_items.return_value = self.ascendancy_items
        mock_gear_items.return_value = self.gear_items
        mock_flask_items.return_value = self.flask_items
        mock_support_gems.return_value = self.support_gem_items
        mock_max_links.return_value = self.max_links_items
        mock_skill_gems.return_value = []  # No skill gems available
        
        # Mock state to return insufficient skill gems
        def mock_count_insufficient(items, player):
            if len(items) == 0:  # skill gems list is empty
                return 0
            return 5
        
        self.mock_state.count_from_list.side_effect = mock_count_insufficient
        
        result = can_reach(1, self.mock_world, self.mock_state)
        self.assertFalse(result)
    
    @patch('worlds.poe.Items.get_by_category')
    @patch('worlds.poe.Items.get_ascendancy_class_items')
    @patch('worlds.poe.Items.get_gear_items')
    @patch('worlds.poe.Items.get_flask_items')
    @patch('worlds.poe.Items.get_support_gem_items')
    @patch('worlds.poe.Items.get_max_links_items')
    @patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon')
    @patch('worlds.poe.Rules.acts')
    def test_can_reach_act_1_insufficient_weapon_types(self, mock_acts, mock_skill_gems,
                                                      mock_max_links, mock_support_gems,
                                                      mock_flask_items, mock_gear_items,
                                                      mock_ascendancy_items, mock_get_by_category):
        """Test can_reach for act 1 with insufficient weapon types"""
        mock_acts.__getitem__.return_value = {"maxMonsterLevel": 10}
        
        # Setup mocks - different return values per weapon category
        def mock_get_by_category_selective(category):
            if category == "Sword":
                return [{"name": "Progressive Sword"}]
            elif category in Rules.armor_categories:
                return self.armor_items
            else:
                return []  # No items for other weapon categories
        
        mock_get_by_category.side_effect = mock_get_by_category_selective
        mock_ascendancy_items.return_value = self.ascendancy_items
        mock_gear_items.return_value = self.gear_items
        mock_flask_items.return_value = self.flask_items
        mock_support_gems.return_value = self.support_gem_items
        mock_max_links.return_value = self.max_links_items
        mock_skill_gems.return_value = self.skill_gem_items
        
        # Mock state to have items from one weapon category only
        def mock_has_from_list_limited(items, player, count):
            if len(items) == 0:
                return False
            item_names = [item["name"] if isinstance(item, dict) else str(item) for item in items]
            return any("Sword" in name for name in item_names)
        
        self.mock_state.has_from_list.side_effect = mock_has_from_list_limited
        
        result = can_reach(1, self.mock_world, self.mock_state)
        self.assertFalse(result)  # Need at least 2 weapon types
    
    @patch('worlds.poe.Items.get_by_category')
    @patch('worlds.poe.Items.get_ascendancy_class_items')
    @patch('worlds.poe.Items.get_gear_items')
    @patch('worlds.poe.Items.get_flask_items')
    @patch('worlds.poe.Items.get_support_gem_items')
    @patch('worlds.poe.Items.get_max_links_items')
    @patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon')
    @patch('worlds.poe.Rules.acts')
    def test_can_reach_act_1_insufficient_armor_categories(self, mock_acts, mock_skill_gems,
                                                          mock_max_links, mock_support_gems,
                                                          mock_flask_items, mock_gear_items,
                                                          mock_ascendancy_items, mock_get_by_category):
        """Test can_reach for act 1 with insufficient armor categories"""
        mock_acts.__getitem__.return_value = {"maxMonsterLevel": 10}
        
        # Setup mocks - different return values per category
        def mock_get_by_category_selective(category):
            if category in Rules.weapon_categories:
                return self.weapon_items  # Multiple weapon types
            elif category == "Helmet":
                return [{"name": "Progressive Helmet"}]  # Only one armor type
            else:
                return []  # No items for other armor categories
        
        mock_get_by_category.side_effect = mock_get_by_category_selective
        mock_ascendancy_items.return_value = self.ascendancy_items
        mock_gear_items.return_value = self.gear_items
        mock_flask_items.return_value = self.flask_items
        mock_support_gems.return_value = self.support_gem_items
        mock_max_links.return_value = self.max_links_items
        mock_skill_gems.return_value = self.skill_gem_items
        
        # Mock state to only have helmet items (not enough armor categories)
        def mock_has_from_list_armor(items, player, count):
            if len(items) == 0:
                return False
            item_names = [item["name"] if isinstance(item, dict) else str(item) for item in items]
            # Only return True for helmet and weapon items
            return any("Helmet" in name or "Sword" in name or "Axe" in name or "Bow" in name 
                      for name in item_names)
        
        self.mock_state.has_from_list.side_effect = mock_has_from_list_armor
        
        result = can_reach(1, self.mock_world, self.mock_state)
        self.assertFalse(result)  # Need at least 2 armor categories
    
    @patch('worlds.poe.Items.get_by_category')
    @patch('worlds.poe.Items.get_ascendancy_class_items')
    @patch('worlds.poe.Items.get_gear_items')
    @patch('worlds.poe.Items.get_flask_items')
    @patch('worlds.poe.Items.get_support_gem_items')
    @patch('worlds.poe.Items.get_max_links_items')
    @patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon')
    @patch('worlds.poe.Rules.acts')
    def test_can_reach_act_1_insufficient_flasks(self, mock_acts, mock_skill_gems,
                                                mock_max_links, mock_support_gems,
                                                mock_flask_items, mock_gear_items,
                                                mock_ascendancy_items, mock_get_by_category):
        """Test can_reach for act 1 with insufficient flasks"""
        mock_acts.__getitem__.return_value = {"maxMonsterLevel": 10}
        
        # Setup mocks - no flasks available
        mock_get_by_category.return_value = self.weapon_items
        mock_ascendancy_items.return_value = self.ascendancy_items
        mock_gear_items.return_value = self.gear_items
        mock_flask_items.return_value = []  # No flasks available
        mock_support_gems.return_value = self.support_gem_items
        mock_max_links.return_value = self.max_links_items
        mock_skill_gems.return_value = self.skill_gem_items
        
        # Mock state to return insufficient flasks
        def mock_count_no_flasks(items, player):
            if len(items) == 0:  # flask items list is empty
                return 0
            return 5
        
        self.mock_state.count_from_list.side_effect = mock_count_no_flasks
        
        result = can_reach(1, self.mock_world, self.mock_state)
        self.assertFalse(result)  # Need at least 3 flasks for act 1
    
    def test_can_reach_scion_character(self):
        """Test can_reach with Scion character (different ascendancy requirements)"""
        self.mock_options.starting_character.value = self.mock_options.starting_character.option_scion
        self.mock_options.starting_character.current_option_name = "Scion"
        
        with patch('worlds.poe.Items.get_by_category') as mock_get_by_category, \
             patch('worlds.poe.Items.get_ascendancy_class_items') as mock_ascendancy_items, \
             patch('worlds.poe.Items.get_gear_items') as mock_gear_items, \
             patch('worlds.poe.Items.get_flask_items') as mock_flask_items, \
             patch('worlds.poe.Items.get_support_gem_items') as mock_support_gems, \
             patch('worlds.poe.Items.get_max_links_items') as mock_max_links, \
             patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon') as mock_skill_gems, \
             patch('worlds.poe.Rules.acts') as mock_acts:
            
            mock_acts.__getitem__.return_value = {"maxMonsterLevel": 30}
            
            # Setup mocks
            mock_get_by_category.return_value = self.weapon_items
            mock_ascendancy_items.return_value = [{"name": "Ascendant"}]  # Scion ascendancy
            mock_gear_items.return_value = self.gear_items
            mock_flask_items.return_value = self.flask_items
            mock_support_gems.return_value = self.support_gem_items
            mock_max_links.return_value = self.max_links_items
            mock_skill_gems.return_value = self.skill_gem_items
            
            # Mock state to return 1 ascendancy item (sufficient for Scion)
            def mock_count_scion(items, player):
                item_names = [item["name"] if isinstance(item, dict) else str(item) for item in items]
                if any("Ascendant" in name for name in item_names):
                    return 2  # Scion needs min(ascendancies_per_class=3, scion_max=2) = 2
                return 5

            self.mock_state.count_from_list.side_effect = mock_count_scion

            result = can_reach(3, self.mock_world, self.mock_state)
            self.assertTrue(result)  # Scion needs 2 ascendancies (min of 3 available, 2 max for Scion)
    
    def test_can_reach_flask_slots_disabled(self):
        """Test can_reach when flask slots are disabled in options"""
        self.mock_options.add_flasks_to_item_pool = False
        
        with patch('worlds.poe.Items.get_by_category') as mock_get_by_category, \
             patch('worlds.poe.Items.get_ascendancy_class_items') as mock_ascendancy_items, \
             patch('worlds.poe.Items.get_gear_items') as mock_gear_items, \
             patch('worlds.poe.Items.get_flask_items') as mock_flask_items, \
             patch('worlds.poe.Items.get_support_gem_items') as mock_support_gems, \
             patch('worlds.poe.Items.get_max_links_items') as mock_max_links, \
             patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon') as mock_skill_gems, \
             patch('worlds.poe.Rules.acts') as mock_acts:
            
            mock_acts.__getitem__.return_value = {"maxMonsterLevel": 20}
            
            # Setup mocks
            mock_get_by_category.return_value = self.weapon_items
            mock_ascendancy_items.return_value = self.ascendancy_items
            mock_gear_items.return_value = self.gear_items
            mock_flask_items.return_value = []  # No flasks needed
            mock_support_gems.return_value = self.support_gem_items
            mock_max_links.return_value = self.max_links_items
            mock_skill_gems.return_value = self.skill_gem_items
            
            # Mock state to return zero flasks (should be fine when disabled)
            def mock_count_no_flasks(items, player):
                if any("Flask" in str(item) for item in items):
                    return 0
                return 5
            
            self.mock_state.count_from_list.side_effect = mock_count_no_flasks
            
            result = can_reach(2, self.mock_world, self.mock_state)
            self.assertTrue(result)  # Should pass even with no flasks when disabled
    
    def test_can_reach_passive_points_disabled(self):
        """Test can_reach when passive points are disabled in options"""
        self.mock_options.add_passive_skill_points_to_item_pool.value = False
        
        with patch('worlds.poe.Items.get_by_category') as mock_get_by_category, \
             patch('worlds.poe.Items.get_ascendancy_class_items') as mock_ascendancy_items, \
             patch('worlds.poe.Items.get_gear_items') as mock_gear_items, \
             patch('worlds.poe.Items.get_flask_items') as mock_flask_items, \
             patch('worlds.poe.Items.get_support_gem_items') as mock_support_gems, \
             patch('worlds.poe.Items.get_max_links_items') as mock_max_links, \
             patch('worlds.poe.Items.get_main_skill_gems_by_required_level_and_useable_weapon') as mock_skill_gems, \
             patch('worlds.poe.Rules.acts') as mock_acts:
            
            mock_acts.__getitem__.return_value = {"maxMonsterLevel": 50}
            
            # Setup mocks
            mock_get_by_category.return_value = self.weapon_items
            mock_ascendancy_items.return_value = self.ascendancy_items
            mock_gear_items.return_value = self.gear_items
            mock_flask_items.return_value = self.flask_items
            mock_support_gems.return_value = self.support_gem_items
            mock_max_links.return_value = self.max_links_items
            mock_skill_gems.return_value = self.skill_gem_items
            
            # Mock state to have sufficient items but zero passive points
            def mock_count(item, player):
                if item == "Progressive passive point":
                    return 0
                return 10  # Sufficient for other item counts
            
            def mock_count_from_list(items, player):
                # Ensure we have enough gear and skill gems for act 5
                return min(10, len(items))  # Return count based on available items, up to 10
            
            self.mock_state.count_from_list.side_effect = mock_count_from_list
            self.mock_state.count.side_effect = mock_count
            self.mock_state.has_from_list.return_value = True  # Has all required items
            
            result = can_reach(5, self.mock_world, self.mock_state)
            self.assertTrue(result)  # Should pass even with no passives when disabled


if __name__ == '__main__':
    unittest.main()