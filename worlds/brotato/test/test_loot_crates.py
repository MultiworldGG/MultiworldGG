from unittest import TestCase

from ..loot_crates import build_loot_crate_groups
from .data_sets.loot_crates import LOOT_CRATE_GROUP_DATA_SETS


class TestLootCrateGroups(TestCase):
    def test_common_loot_crate_groups_correct(self):
        for test_data in LOOT_CRATE_GROUP_DATA_SETS:
            with self.subTest(msg=test_data.description):
                common_loot_crate_groups = build_loot_crate_groups(
                    test_data.options.num_common_crate_drops,
                    test_data.options.num_common_crate_drop_groups,
                    test_data.options.num_victories,
                )
                self.assertEqual(
                    len(common_loot_crate_groups),
                    len(test_data.expected_common_groups),
                    msg="Incorrect number of common loot crate groups for ",
                )
                for idx, (group, expected_group) in enumerate(
                    zip(common_loot_crate_groups, test_data.expected_common_groups, strict=True)
                ):
                    self.assertEqual(group, expected_group, msg=f"Mismatch for group {idx}.")

    def test_legendary_loot_crate_groups_correct(self):
        for test_data in LOOT_CRATE_GROUP_DATA_SETS:
            with self.subTest(msg=test_data.description, test_data=test_data):
                legendary_loot_crate_groups = build_loot_crate_groups(
                    test_data.options.num_legendary_crate_drops,
                    test_data.options.num_legendary_crate_drop_groups,
                    test_data.options.num_victories,
                )
                self.assertEqual(
                    len(legendary_loot_crate_groups),
                    len(test_data.expected_legendary_groups),
                    msg="Incorrect number of legendary loot crate groups",
                )
                for idx, (group, expected_group) in enumerate(
                    zip(legendary_loot_crate_groups, test_data.expected_legendary_groups, strict=True)
                ):
                    self.assertEqual(group, expected_group, msg=f"Mismatch for group {idx}.")
