from typing import Any

from ..options import StartingShopLockButtonsMode
from ..waves import get_wave_for_each_item
from . import BrotatoTestBase
from .data_sets.shop_slots import SHOP_SLOT_TEST_DATA_SETS


class TestBrotatoSlotData(BrotatoTestBase):
    run_default_tests = False

    options: dict[str, Any] = {  # noqa: RUF012
        # Only set options that are referenced by slot_data
        "num_victories": 10,
        "starting_characters": 0,
        "waves_per_drop": 2,
        "num_wave_caps": 4,
        "num_common_crate_drops_per_check": 2,
        "num_common_crate_drop_groups": 5,
        "num_legendary_crate_drops_per_check": 1,
        "num_legendary_crate_drop_groups": 2,
        "num_starting_shop_slots": 1,
        "shop_lock_buttons_mode": StartingShopLockButtonsMode.option_custom,
        "num_starting_lock_buttons": 2,
        "num_common_crate_drops": 20,
        "num_legendary_crate_drops": 0,
        # Set the weights so only common items are made, to properly test item wave entry
        "common_item_weight": 1,
        "uncommon_item_weight": 0,
        "rare_item_weight": 0,
        "legendary_item_weight": 0,
        "common_upgrade_weight": 0,
        "uncommon_upgrade_weight": 0,
        "rare_upgrade_weight": 0,
        "legendary_upgrade_weight": 0,
        "gold_weight": 0,
        "xp_weight": 0,
    }

    def test_slot_data_num_wins_needed(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["num_wins_needed"], 10)

    def test_slot_data_num_starting_shop_slots(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["num_starting_shop_slots"], 1)

    def test_slot_data_starting_shop_lock_buttons(self):
        for test_case in SHOP_SLOT_TEST_DATA_SETS:
            with self.data_set_subtest(test_case):
                slot_data = self.world.fill_slot_data()
                self.assertEqual(
                    slot_data["num_starting_shop_lock_buttons"], test_case.expected_num_starting_lock_buttons
                )

    def test_slot_data_num_common_crate_locations(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["num_common_crate_locations"], 20)

    def test_slot_data_num_common_crate_drops_per_check(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["num_common_crate_drops_per_check"], 2)

    def test_slot_data_num_legendary_crate_locations(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["num_legendary_crate_locations"], 0)

    def test_slot_data_num_legendary_crate_drops_per_check(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["num_legendary_crate_drops_per_check"], 1)

    def test_slot_data_wave_per_game_item(self):
        slot_data = self.world.fill_slot_data()
        # Testing get_wave_for_each_item is done elsewhere, we just want to see that the slot data matches.
        expected_wave_per_item = get_wave_for_each_item(self.world.nonessential_item_counts)
        self.assertEqual(slot_data["wave_per_game_item"], expected_wave_per_item)

    def test_slot_data_wave_access(self):
        expected_wave_access = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 1,
            7: 1,
            8: 1,
            9: 1,
            10: 1,
            11: 2,
            12: 2,
            13: 2,
            14: 2,
            15: 2,
            16: 3,
            17: 3,
            18: 3,
            19: 3,
            20: 3,
        }
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["wave_access"], expected_wave_access)
