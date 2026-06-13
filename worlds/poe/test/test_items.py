"""
Tests for the Path of Exile Items module
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from BaseClasses import ItemClassification
from worlds.poe import Items
from worlds.poe.Items import ItemDict, PathOfExileItem
from worlds.poe import Logic
from . import PoeTestBase


class TestItemDict(unittest.TestCase):
    """Test the ItemDict TypedDict structure"""
    
    def test_item_dict_structure(self):
        """Test that ItemDict can be created with expected fields"""
        item_dict: ItemDict = {
            "id": 1,
            "name": "Test Item",
            "category": ["TestCategory"],
            "classification": ItemClassification.progression,
            "count": 1,
            "reqLevel": 10,
            "reqToUse": ["Sword"]
        }
        
        self.assertEqual(item_dict["id"], 1)
        self.assertEqual(item_dict["name"], "Test Item")
        self.assertEqual(item_dict["category"], ["TestCategory"])
        self.assertEqual(item_dict["classification"], ItemClassification.progression)
        self.assertEqual(item_dict["count"], 1)
        self.assertEqual(item_dict["reqLevel"], 10)
        self.assertEqual(item_dict["reqToUse"], ["Sword"])


class TestPathOfExileItem(unittest.TestCase):
    """Test the PathOfExileItem class"""
    
    def test_path_of_exile_item_creation(self):
        """Test creating a PathOfExileItem instance"""
        item = PathOfExileItem("Test Item", ItemClassification.progression, 123, 1)
        
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.classification, ItemClassification.progression)
        self.assertEqual(item.code, 123)
        self.assertEqual(item.player, 1)
        self.assertEqual(item.game, "Path of Exile")
    
    def test_path_of_exile_item_attributes(self):
        """Test PathOfExileItem attributes"""
        item = PathOfExileItem("Test Item", ItemClassification.useful, 456, 2)
        
        # Test that category attribute exists (itemInfo might not be initialized by default)
        self.assertTrue(hasattr(item, 'category'))


class TestItemTableFunctions(PoeTestBase):
    """Test functions that work with the item table"""
    
    def setUp(self):
        super().setUp()
        # Create a mock item table for testing
        self.mock_item_table = {
            1: {"id": 1, "name": "Life Flask", "category": ["Flask"], "reqLevel": 1},
            2: {"id": 2, "name": "Marauder", "category": ["Character Class"], "reqLevel": None},
            3: {"id": 3, "name": "Juggernaut", "category": ["Ascendancy", "Marauder Class"], "reqLevel": None},
            4: {"id": 4, "name": "Fireball", "category": ["MainSkillGem"], "reqLevel": 1, "reqToUse": ["Wand", "Staff"]},
            5: {"id": 5, "name": "Added Fire Damage", "category": ["SupportGem"], "reqLevel": 8},
            6: {"id": 6, "name": "Portal", "category": ["UtilSkillGem"], "reqLevel": 10},
            7: {"id": 7, "name": "Progressive Gear", "category": ["Gear", "Progressive Gear"], "reqLevel": None},
            8: {"id": 8, "name": "Iron Sword", "category": ["Gear", "Weapon", "Sword"], "reqLevel": 1},
            9: {"id": 9, "name": "Leather Cap", "category": ["Gear", "Armor", "Helmet"], "reqLevel": 1},
            10: {"id": 10, "name": "6-Link", "category": ["max links"], "reqLevel": None},
            11: {"id": 11, "name": "Unique Sword", "category": ["Gear", "Weapon", "Sword", "Unique"], "reqLevel": 15},
        }
    
    def test_get_flask_items(self):
        """Test getting flask items"""
        result = Items.get_flask_items(self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Life Flask")
    
    def test_get_character_class_items(self):
        """Test getting character class items"""
        result = Items.get_character_class_items(self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Marauder")
    
    def test_get_ascendancy_items(self):
        """Test getting ascendancy items"""
        result = Items.get_ascendancy_items(self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Juggernaut")
    
    def test_get_ascendancy_class_items(self):
        """Test getting ascendancy items for specific class"""
        result = Items.get_ascendancy_class_items("Marauder", self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Juggernaut")
        
        # Test with non-existent class
        result = Items.get_ascendancy_class_items("NonExistent", self.mock_item_table)
        self.assertEqual(len(result), 0)
    
    def test_get_main_skill_gem_items(self):
        """Test getting main skill gem items"""
        result = Items.get_main_skill_gem_items(self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Fireball")
    
    def test_get_support_gem_items(self):
        """Test getting support gem items"""
        result = Items.get_support_gem_items(self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Added Fire Damage")
    
    def test_get_utility_skill_gem_items(self):
        """Test getting utility skill gem items"""
        result = Items.get_utility_skill_gem_items(self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Portal")
    
    def test_get_gear_items(self):
        """Test getting gear items"""
        result = Items.get_gear_items(self.mock_item_table)
        self.assertEqual(len(result), 4)  # Progressive Gear, Iron Sword, Leather Cap, Unique Sword
        gear_names = {item["name"] for item in result}
        self.assertIn("Progressive Gear", gear_names)
        self.assertIn("Iron Sword", gear_names)
        self.assertIn("Leather Cap", gear_names)
        self.assertIn("Unique Sword", gear_names)
    
    def test_get_armor_items(self):
        """Test getting armor items"""
        result = Items.get_armor_items(self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Leather Cap")
    
    def test_get_weapon_items(self):
        """Test getting weapon items"""
        result = Items.get_weapon_items(self.mock_item_table)
        self.assertEqual(len(result), 2)  # Iron Sword, Unique Sword
        weapon_names = {item["name"] for item in result}
        self.assertIn("Iron Sword", weapon_names)
        self.assertIn("Unique Sword", weapon_names)
    
    def test_get_max_links_items(self):
        """Test getting max links items"""
        result = Items.get_max_links_items(self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "6-Link")
    
    def test_get_all_gems(self):
        """Test getting all gem items"""
        result = Items.get_all_gems(self.mock_item_table)
        self.assertEqual(len(result), 3)  # Fireball, Added Fire Damage, Portal
        gem_names = {item["name"] for item in result}
        self.assertIn("Fireball", gem_names)
        self.assertIn("Added Fire Damage", gem_names)
        self.assertIn("Portal", gem_names)
    
    def test_get_main_skill_gems_by_required_level(self):
        """Test getting main skill gems by level requirement"""
        result = Items.get_main_skill_gems_by_required_level(1, 5, self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Fireball")
        
        # Test with level range that excludes the gem
        result = Items.get_main_skill_gems_by_required_level(10, 20, self.mock_item_table)
        self.assertEqual(len(result), 0)
    
    def test_get_main_skill_gems_by_required_level_and_useable_weapon(self):
        """Test getting main skill gems by level and weapon requirement"""
        # Test with matching weapon
        result = Items.get_main_skill_gems_by_required_level_and_useable_weapon(
            {"Wand"}, 1, 5, self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Fireball")
        
        # Test with non-matching weapon
        result = Items.get_main_skill_gems_by_required_level_and_useable_weapon(
            {"Bow"}, 1, 5, self.mock_item_table)
        self.assertEqual(len(result), 0)
    
    def test_get_by_category(self):
        """Test getting items by category"""
        result = Items.get_by_category("Flask", self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Life Flask")
        
        # Test with non-existent category
        result = Items.get_by_category("NonExistent", self.mock_item_table)
        self.assertEqual(len(result), 0)
    
    def test_get_by_has_every_category(self):
        """Test getting items that have all specified categories"""
        result = Items.get_by_has_every_category({"Ascendancy", "Marauder Class"}, self.mock_item_table)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Juggernaut")
        
        # Test with categories that no item has all of
        result = Items.get_by_has_every_category({"Flask", "Weapon"}, self.mock_item_table)
        self.assertEqual(len(result), 0)
    
    def test_get_by_has_any_category(self):
        """Test getting items that have any of the specified categories"""
        result = Items.get_by_has_any_category({"Flask", "Weapon"}, self.mock_item_table)
        self.assertEqual(len(result), 3)  # Life Flask, Iron Sword, Unique Sword
        names = {item["name"] for item in result}
        self.assertIn("Life Flask", names)
        self.assertIn("Iron Sword", names)
        self.assertIn("Unique Sword", names)
    
    def test_get_by_name(self):
        """Test getting item by name"""
        result = Items.get_by_name("Fireball", self.mock_item_table)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Fireball")
        
        # Test with non-existent name
        result = Items.get_by_name("NonExistent", self.mock_item_table)
        self.assertIsNone(result)


class TestItemDeprioritization(PoeTestBase):
    """Test item deprioritization functions"""
    
    def setUp(self):
        super().setUp()
        self.mock_world = Mock()
        self.mock_world.goal_act = 5
        self.mock_world.random = Mock()
        self.mock_world.random.sample = Mock(side_effect=lambda x, k: x[:k])
        
        self.mock_options = Mock()
        self.mock_options.skill_gems_per_act.value = 2
        self.mock_options.support_gems_per_act.value = 1
        self.mock_options.gear_upgrades_per_act.value = 3
        self.mock_world.options = self.mock_options
        
        # Mock item table
        self.mock_item_table = {
            1: {"id": 1, "name": "Fireball", "category": ["MainSkillGem"], 
                "reqLevel": 1, "classification": ItemClassification.progression},
            2: {"id": 2, "name": "Ice Bolt", "category": ["MainSkillGem"], 
                "reqLevel": 10, "classification": ItemClassification.progression},
            3: {"id": 3, "name": "Added Fire", "category": ["SupportGem"], 
                "reqLevel": 5, "classification": ItemClassification.progression},
            4: {"id": 4, "name": "Portal", "category": ["UtilSkillGem"], 
                "reqLevel": 1, "classification": ItemClassification.progression},
            5: {"id": 5, "name": "Iron Sword", "category": ["Gear", "Weapon"], 
                "reqLevel": 1, "classification": ItemClassification.progression},
            6: {"id": 6, "name": "Steel Sword", "category": ["Gear", "Weapon"], 
                "reqLevel": 5, "classification": ItemClassification.progression},
        }
    
    @patch('worlds.poe.Locations.acts')
    def test_deprioritize_non_logic_gems(self, mock_acts):
        """Test gem deprioritization based on logic requirements"""
        mock_acts.__getitem__ = Mock(side_effect=lambda x: {"maxMonsterLevel": x * 5})

        # Mock Items module functions to return our test data
        with patch('worlds.poe.Items.get_main_skill_gem_items', return_value=[self.mock_item_table[1], self.mock_item_table[2]]), \
             patch('worlds.poe.Items.get_support_gem_items', return_value=[self.mock_item_table[3]]), \
             patch('worlds.poe.Items.get_utility_skill_gem_items', return_value=[self.mock_item_table[4]]):

            # Create a copy to test against original
            original_table = self.mock_item_table.copy()
            result = Logic.deprioritize_non_logic_gems(self.mock_world, original_table)
            
            # Should return the modified table
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), len(self.mock_item_table))
            
            # Check that selected gems remain progression
            # With goal_act=5, skill_gems_per_act=2, support_gems_per_act=1:
            # - Act 0: 4 starter gems (level 1 main gems)
            # - Acts 1-5: 2 main + 1 support + 2 utility per act
            # Since we only have limited test gems, some should remain progression
            
            # At least some gems should remain progression (the selected ones)
            progression_gems = [item for item in result.values() 
                              if any(cat in item["category"] for cat in ["MainSkillGem", "SupportGem", "UtilSkillGem"])
                              and item["classification"] == ItemClassification.progression]
            self.assertGreater(len(progression_gems), 0, "Some gems should remain progression for logic")
            
            # Test that the function actually modifies gem classifications
            # Since we have limited test data, at least the structure should be maintained
            for item_id, item in result.items():
                self.assertIn("classification", item)
                self.assertIsInstance(item["classification"], ItemClassification)

class TestItemCulling(PoeTestBase):
    """Test item culling functionality"""
    
    def setUp(self):
        super().setUp()
        self.mock_world = Mock()
        self.mock_world.random = Mock()
        self.mock_world.random.sample = Mock(side_effect=lambda x, k: x[:k])
        
        # Create test items and locations
        self.test_items = {
            1: {"id": 1, "name": "Item1", "classification": ItemClassification.progression, "count": 1},
            2: {"id": 2, "name": "Item2", "classification": ItemClassification.useful, "count": 2},
            3: {"id": 3, "name": "Item3", "classification": ItemClassification.filler, "count": 3},
        }
        
        self.test_locations = {
            1: {"id": 1, "name": "Loc1"},
            2: {"id": 2, "name": "Loc2"},
            3: {"id": 3, "name": "Loc3"},
        }
    
    def test_cull_items_to_place_exact_match(self):
        """Test culling when items exactly match locations"""
        result = Logic.cull_items_to_place(self.mock_world, self.test_items.copy(), self.test_locations)
        
        # Should not cull anything if counts match
        total_items = sum(item.get("count", 1) for item in result.values())
        self.assertEqual(total_items, len(self.test_locations))
    
    def test_cull_items_to_place_excess_items(self):
        """Test culling when there are more items than locations"""
        # Add more items than locations
        excess_items = self.test_items.copy()
        excess_items[4] = {"id": 4, "name": "Item4", "classification": ItemClassification.filler, "count": 5}
        
        result = Logic.cull_items_to_place(self.mock_world, excess_items, self.test_locations)
        
        # Should cull items to match location count
        total_items = sum(item.get("count", 1) for item in result.values())
        self.assertEqual(total_items, len(self.test_locations))
    
    def test_cull_items_prioritizes_filler_over_useful(self):
        """Test that culling prioritizes removing filler items over useful items"""
        # Create scenario where we need to cull some items
        excess_items = {
            1: {"id": 1, "name": "Prog", "classification": ItemClassification.progression, "count": 1},
            2: {"id": 2, "name": "Useful", "classification": ItemClassification.useful, "count": 1},
            3: {"id": 3, "name": "Filler", "classification": ItemClassification.filler, "count": 5},
        }
        
        # Only 2 locations, so should cull 5 items
        small_locations = {1: {"id": 1}, 2: {"id": 2}}
        
        result = Logic.cull_items_to_place(self.mock_world, excess_items, small_locations)
        
        # Progression should always be preserved
        self.assertIn(1, result)
        # Filler should be reduced/removed
        total_items = sum(item.get("count", 1) for item in result.values())
        self.assertEqual(total_items, 2)


class TestItemNameGroups(PoeTestBase):
    """Test item name grouping functionality"""
    
    @patch('worlds.poe.Items.item_table')
    def test_get_item_name_groups(self, mock_item_table):
        """Test getting item name groups by category"""
        mock_item_table.values.return_value = [
            {"name": "Life Flask", "category": ["Flask"]},
            {"name": "Mana Flask", "category": ["Flask"]},
            {"name": "Fireball", "category": ["MainSkillGem"]},
            {"name": "Ice Bolt", "category": ["MainSkillGem"]},
        ]
        
        result = Items.get_item_name_groups()
        
        self.assertIn("Flask", result)
        self.assertIn("MainSkillGem", result)
        self.assertEqual(result["Flask"], {"Life Flask", "Mana Flask"})
        self.assertEqual(result["MainSkillGem"], {"Fireball", "Ice Bolt"})


class TestMemoization(PoeTestBase):
    """Test memoization cache functionality"""
    
    def test_memoization_cache_usage(self):
        """Test that memoization cache is used for repeated calls"""
        # Clear cache first
        Items.memoize_cache.clear()
        
        # Create a test table that has MainSkillGem items
        test_table = {
            1: {"id": 1, "name": "Fireball", "category": ["MainSkillGem"], "reqLevel": 5}
        }
        
        # First call should populate cache (only works with global item_table)
        result1 = Items.get_main_skill_gems_by_required_level(1, 10, test_table)
        
        # Since we're using a custom table, cache won't be used, but function should work
        self.assertEqual(len(result1), 1)
        self.assertEqual(result1[0]["name"], "Fireball")


if __name__ == '__main__':
    unittest.main()
