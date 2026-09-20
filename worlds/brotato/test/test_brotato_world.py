from ..loot_crates import BrotatoLootCrateGroup
from . import BrotatoTestBase
from .data_sets.loot_crates import LOOT_CRATE_GROUP_DATA_SETS
from .data_sets.num_characters import NUM_CHARACTERS_DATA_SETS


class TestBrotatoWorld(BrotatoTestBase):
    """Test attributes on the BrotatoWorld instance directly."""

    def test_all_num_character_options_work(self):
        # Which characters we pick to include shouldn't matter, just the amount.
        for test_data in NUM_CHARACTERS_DATA_SETS:
            with self.data_set_subtest(test_data):
                self.assertEqual(len(self.world._include_characters), test_data.num_characters)
                self.assertEqual(self.world.num_wins_needed, test_data.num_characters)
                self.test_fill()
                self.test_empty_state_can_reach_something()
                self.test_all_state_can_reach_everything()

    def test_common_loot_crate_groups_correct(self):
        """Checks that the apworld common loot crate groups are correct.

        This is similar to test_loot_crates.py -> test_common_loot_crate_groups_correct,
        except that this one checks the attributes on the apworld after generating
        instead of calling build_loot_crate_groups directly. This helps check that the
        options of the test data are valid (relevant when changing option maximums), and
        that we actually apply the results of build_loot_crate_groups to the apworld.
        """
        for test_idx, test_data in enumerate(LOOT_CRATE_GROUP_DATA_SETS):
            with self.data_set_subtest(test_data, idx=test_idx):
                groups: list[BrotatoLootCrateGroup] = self.world.common_loot_crate_groups
                expected_groups: list[BrotatoLootCrateGroup] = test_data.expected_common_groups
                self.assertEqual(len(groups), len(expected_groups))
                for group_idx, (group, expected_group) in enumerate(zip(groups, expected_groups, strict=True)):
                    self.assertEqual(group, expected_group, f"Common loot crate group {group_idx} is not correct.")

    def test_legendary_loot_crate_groups_correct(self):
        for test_idx, test_data in enumerate(LOOT_CRATE_GROUP_DATA_SETS):
            with self.data_set_subtest(test_data, idx=test_idx):
                groups: list[BrotatoLootCrateGroup] = self.world.legendary_loot_crate_groups
                expected_groups: list[BrotatoLootCrateGroup] = test_data.expected_legendary_groups
                self.assertEqual(len(groups), len(expected_groups))
                for group_idx, (group, expected_group) in enumerate(zip(groups, expected_groups, strict=True)):
                    self.assertEqual(group, expected_group, f"Legendary loot crate group {group_idx} is not correct.")
