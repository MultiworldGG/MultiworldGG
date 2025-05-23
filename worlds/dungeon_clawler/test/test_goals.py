from . import DungeonClawlerTestBase
from .. import options

#
# class TestCreatureFeatureGoal(DungeonClawlerTestBase):
#     options = {options.Goal.internal_name: options.Goal.option_creature_feature,
#                options.ShuffleMonstermon.internal_name: options.ShuffleMonstermon.option_true,
#                options.ShuffleMoney.internal_name: 1}
#
#     def test_items_needed(self):
#         self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         relevant_item_names = [InventoryItem.laser_bomb, InventoryItem.monstermon_plushie, InventoryItem.faculty_remote]
#         relevant_items = [self.get_item_by_name(item_name) for item_name in relevant_item_names]
#
#         self.collect_all_but(relevant_item_names)
#         self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         for item in relevant_items:
#             self.collect(item)
#         self.assertTrue(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         for item in relevant_items:
#             self.remove(item)
#             self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#             self.collect(item)
#
#
# class TestAllMissionsGoal(DungeonClawlerTestBase):
#     options = {options.Goal.internal_name: options.Goal.option_all_missions,
#                options.ShuffleMonstermon.internal_name: options.ShuffleMonstermon.option_true,
#                options.ShuffleMoney.internal_name: 1}
#
#     def test_items_needed(self):
#         self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         relevant_item_names = [InventoryItem.bob_toolbelt, InventoryItem.an_a_plus, InventoryItem.prestigious_pin,
#                                InventoryItem.laser_beam, InventoryItem.monstermon_plushie, InventoryItem.strange_chemical,
#                                InventoryItem.laser_bomb, InventoryItem.faculty_remote]
#         relevant_items = [self.get_item_by_name(item_name) for item_name in relevant_item_names]
#
#         self.collect_all_but(relevant_item_names)
#         with self.subTest(f"Cannot win with no inventory items"):
#             self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         for item in relevant_items:
#             self.collect(item)
#         with self.subTest(f"Can win with all inventory items"):
#             self.assertTrue(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         for item in relevant_items:
#             with self.subTest(f"{item.name} is necessary to victory"):
#                 self.remove(item)
#                 self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#                 self.collect(item)
#
#
# class TestSecretEndingGoalWithMonstermon(DungeonClawlerTestBase):
#     options = {options.Goal.internal_name: options.Goal.option_secret_ending,
#                options.ShuffleMonstermon.internal_name: options.ShuffleMonstermon.option_true,
#                options.ShuffleMoney.internal_name: 1}
#
#     def test_items_needed(self):
#         self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         relevant_item_names = all_cards
#         relevant_items = [self.get_item_by_name(item_name) for item_name in relevant_item_names]
#
#         self.collect_all_but(relevant_item_names)
#         with self.subTest(f"Cannot win with no monstermon cards"):
#             self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         for item in relevant_items:
#             self.collect(item)
#         with self.subTest(f"Can win with all monstermon cards"):
#             self.assertTrue(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         for item in relevant_items:
#             with self.subTest(f"{item.name} is necessary to victory"):
#                 self.remove(item)
#                 self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#                 self.collect(item)


# class TestAllMissionsAndSecretEndingGoal(DungeonClawlerTestBase):
#     options = {Options.Goal.internal_name: Options.Goal.option_all_missions_and_secret_ending,
#                Options.ShuffleMonstermon.internal_name: Options.ShuffleMonstermon.option_true,
#                Options.ShuffleMoney.internal_name: 1}
#
#     def test_items_needed(self):
#         self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         relevant_item_names = [InventoryItem.bob_toolbelt, InventoryItem.an_a_plus, InventoryItem.prestigious_pin,
#                                InventoryItem.laser_beam, InventoryItem.monstermon_plushie, InventoryItem.strange_chemical,
#                                InventoryItem.laser_bomb, InventoryItem.faculty_remote, *all_cards]
#         relevant_items = [self.get_item_by_name(item_name) for item_name in relevant_item_names]
#
#         self.collect_all_but(relevant_item_names)
#         with self.subTest(f"Cannot win with no inventory items and monstermon cards"):
#             self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         for item in relevant_items:
#             self.collect(item)
#         with self.subTest(f"Can win with all inventory items and monstermon cards"):
#             self.assertTrue(self.multiworld.state.can_reach_location("Victory", self.player))
#
#         for item in relevant_items:
#             with self.subTest(f"{item.name} is necessary to victory"):
#                 self.remove(item)
#                 self.assertFalse(self.multiworld.state.can_reach_location("Victory", self.player))
#                 self.collect(item)
