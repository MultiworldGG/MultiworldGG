from BaseClasses import ItemClassification

from .bases import DredgeTestBase
from ..items import item_table
from ..locations import location_table


def pool_item_names(test: DredgeTestBase) -> list[str]:
    return [item.name for item in test.multiworld.itempool if item.player == test.player]


class TestDefaultOptions(DredgeTestBase):
    options = {}

    def test_three_progressive_hulls(self) -> None:
        self.assertEqual(pool_item_names(self).count("Progressive Hull"), 3)

    def test_no_dlc_items(self) -> None:
        dlc_items = [name for name in pool_item_names(self)
                     if item_table[name].expansion in ("PaleReach", "IronRig")]
        self.assertEqual(dlc_items, [])

    def test_no_licenses_or_passages(self) -> None:
        groups = {item_table[name].item_group for name in pool_item_names(self)}
        self.assertNotIn("Virtual License", groups)
        self.assertNotIn("Virtual Passage Item", groups)

    def test_no_aberration_chance_items(self) -> None:
        groups = {item_table[name].item_group for name in pool_item_names(self)}
        self.assertNotIn("Aberration Chance", groups)


def message_location_names(test: DredgeTestBase) -> list[str]:
    return [location.name for location in test.multiworld.get_locations(test.player)
            if location.name in location_table and location_table[location.name].location_group == "Message"]


class TestMessageBottles(DredgeTestBase):
    options = {}

    def test_ten_bottles_by_default(self) -> None:
        self.assertEqual(len(message_location_names(self)), 10)


class TestNoMessageBottles(DredgeTestBase):
    options = {
        "include_message_bottles": False,
    }

    def test_no_bottles(self) -> None:
        self.assertEqual(message_location_names(self), [])


class TestPaleReach(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
    }

    def test_pale_reach_useful_items_included(self) -> None:
        useful_pale_reach = {name for name, data in item_table.items()
                             if data.classification == ItemClassification.useful and data.expansion == "PaleReach"}
        self.assertTrue(useful_pale_reach.issubset(set(pool_item_names(self))))


class TestIronRig(DredgeTestBase):
    options = {
        "include_iron_rig_dlc": True,
    }

    def test_four_progressive_hulls(self) -> None:
        self.assertEqual(pool_item_names(self).count("Progressive Hull"), 4)


class TestAllOptions(DredgeTestBase):
    options = {
        "include_iron_rig_dlc": True,
        "include_pale_reach_dlc": True,
        "require_boat_performance": True,
        "logical_nets": True,
        "include_aberrations": True,
        "add_fishing_licenses": True,
        "add_passage_items": True,
        "death_link": True,
    }

    def test_licenses_and_passages_included(self) -> None:
        groups = {item_table[name].item_group for name in pool_item_names(self)}
        self.assertIn("Virtual License", groups)
        self.assertIn("Virtual Passage Item", groups)


class TestLicensesAndPassagesWithoutDlc(DredgeTestBase):
    options = {
        "add_fishing_licenses": True,
        "add_passage_items": True,
        "require_boat_performance": True,
    }


class TestStartingHullsCappedWithoutIronRig(DredgeTestBase):
    options = {
        "start_inventory_from_pool": {"Progressive Hull": 4},
    }

    def test_capped_at_pool_hulls(self) -> None:
        self.assertEqual(self.world.options.start_inventory_from_pool.value["Progressive Hull"], 3)


class TestStartingHullsCappedWithIronRig(DredgeTestBase):
    options = {
        "include_iron_rig_dlc": True,
        "start_inventory_from_pool": {"Progressive Hull": 5},
    }

    def test_capped_at_pool_hulls(self) -> None:
        self.assertEqual(self.world.options.start_inventory_from_pool.value["Progressive Hull"], 4)


class TestStartingHullsWithinPool(DredgeTestBase):
    options = {
        "start_inventory_from_pool": {"Progressive Hull": 2},
    }

    def test_request_kept(self) -> None:
        self.assertEqual(self.world.options.start_inventory_from_pool.value["Progressive Hull"], 2)


class TestAberrationChanceItems(DredgeTestBase):
    options = {
        "progressive_aberration_chance_items": 20,
        "guaranteed_aberrations_item": True,
    }

    def test_items_in_pool(self) -> None:
        names = pool_item_names(self)
        self.assertEqual(names.count("Progressive Aberration Chance"), 20)
        self.assertEqual(names.count("Guaranteed Aberrations"), 1)

    def test_slot_data(self) -> None:
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["progressive_aberration_chance_items"], 20)
        self.assertEqual(slot_data["guaranteed_aberrations_item"], 1)


class TestAberrationsWithoutChanceItemsWarns(DredgeTestBase):
    options = {
        "include_aberrations": True,
    }
    run_default_tests = False

    def test_warns(self) -> None:
        with self.assertLogs(level="WARNING") as logs:
            self.world.generate_early()
        self.assertTrue(any("aberration" in line for line in logs.output))


class TestAberrationsWithChanceItemsDoesNotWarn(DredgeTestBase):
    options = {
        "include_aberrations": True,
        "guaranteed_aberrations_item": True,
    }
    run_default_tests = False

    def test_no_warning(self) -> None:
        with self.assertNoLogs(level="WARNING"):
            self.world.generate_early()


class TestNoTrapsByDefault(DredgeTestBase):
    run_default_tests = False

    def test_no_traps(self) -> None:
        groups = {item_table[name].item_group for name in pool_item_names(self)}
        self.assertNotIn("Trap", groups)


class TestAllFillerTraps(DredgeTestBase):
    options = {
        "trap_percentage": 100,
        "enabled_traps": ["Rot Trap", "Slow Trap"],
    }

    def test_filler_is_only_enabled_traps(self) -> None:
        names = pool_item_names(self)
        traps = {name for name in names if item_table[name].item_group == "Trap"}
        self.assertEqual(traps, {"Rot Trap", "Slow Trap"})
        self.assertFalse(any(item_table[name].classification == ItemClassification.filler for name in names))
