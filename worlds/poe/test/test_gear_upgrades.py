"""
Tests for interaction between gear_upgrades and progressive_gear options.

Bug: when progressive_gear=enabled, the gear_upgrades pre-collect block
(Logic.py setup_early_items) still pre-collects Normal/Random gear items
instead of Progressive gear items. This leaves both systems active:
Normal gear pre-collected AND Progressive gear items in pool.

Expected: in progressive mode, gear_upgrades should pre-collect Progressive
gear items, not Normal/Random gear items.
"""

from . import PoeTestBase
from .. import Items


def _precollected_names(multiworld, player=1):
    return [item.name for item in multiworld.precollected_items[player]]


def _item_pool_names(multiworld, player=1):
    return [item.name for item in multiworld.itempool if item.player == player]


def _is_normal_gear(name: str) -> bool:
    item = next((i for i in Items.item_table.values() if i["name"] == name), None)
    if not item:
        return False
    return "Normal" in item.get("category", []) and "Gear" in item.get("category", [])


def _is_progressive_gear(name: str) -> bool:
    item = next((i for i in Items.item_table.values() if i["name"] == name), None)
    if not item:
        return False
    return "Progressive Gear" in item.get("category", [])


# ---- Regression: non-progressive mode should still work ----

class TestNormalGearUpgradesWithProgressiveDisabled(PoeTestBase):
    """progressive_gear=disabled + gear_upgrades=all_normal_gear_unlocked
    → Normal gear pre-collected, no Progressive gear pre-collected."""
    options = {
        "progressive_gear": "disabled",
        "gear_upgrades": "all_normal_gear_unlocked",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_normal_gear_precollected(self):
        names = _precollected_names(self.multiworld)
        normal_gear = [n for n in names if _is_normal_gear(n)]
        self.assertTrue(len(normal_gear) > 0,
                        f"Normal gear should be pre-collected when gear_upgrades=all_normal_gear_unlocked; got: {names}")

    def test_no_progressive_gear_precollected(self):
        names = _precollected_names(self.multiworld)
        progressive_gear = [n for n in names if _is_progressive_gear(n)]
        self.assertEqual(progressive_gear, [],
                         f"No Progressive gear should be pre-collected in non-progressive mode; got: {progressive_gear}")


# ---- Failing tests: expose the bug ----

class TestNormalGearUpgradesWithProgressiveEnabled(PoeTestBase):
    """progressive_gear=enabled + gear_upgrades=all_normal_gear_unlocked
    → should pre-collect Progressive gear, NOT Normal/Random gear.

    Currently FAILS: the code pre-collects Normal gear items regardless of
    progressive_gear setting (see Logic.py setup_early_items TODO comment)."""
    options = {
        "progressive_gear": "enabled",
        "gear_upgrades": "all_normal_gear_unlocked",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_no_normal_gear_precollected_in_progressive_mode(self):
        """Normal/Random gear items must NOT be pre-collected when progressive_gear=enabled."""
        names = _precollected_names(self.multiworld)
        normal_gear = [n for n in names if _is_normal_gear(n)]
        self.assertEqual(normal_gear, [],
                         f"Normal gear should NOT be pre-collected when progressive_gear=enabled; got: {normal_gear}")

    def test_progressive_gear_precollected_instead(self):
        """Progressive gear items SHOULD be pre-collected to honour gear_upgrades intent."""
        names = _precollected_names(self.multiworld)
        progressive_gear = [n for n in names if _is_progressive_gear(n)]
        self.assertTrue(len(progressive_gear) > 0,
                        f"Progressive gear should be pre-collected when gear_upgrades + progressive_gear=enabled; got: {names}")

    def test_normal_gear_not_in_item_pool(self):
        """Progressive mode must have removed Normal/Random gear from the pool."""
        pool = _item_pool_names(self.multiworld)
        normal_gear_in_pool = [n for n in pool if _is_normal_gear(n)]
        self.assertEqual(normal_gear_in_pool, [],
                         f"Normal gear should not be in item pool in progressive mode; got: {normal_gear_in_pool[:5]}")


class TestAllGearUnlockedWithProgressiveEnabled(PoeTestBase):
    """progressive_gear=enabled + gear_upgrades=all_gear_unlocked_at_start
    → same bug: Normal/Magic/Rare gear pre-collected instead of Progressive gear."""
    options = {
        "progressive_gear": "enabled",
        "gear_upgrades": "all_gear_unlocked_at_start",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_no_normal_gear_precollected(self):
        names = _precollected_names(self.multiworld)
        normal_gear = [n for n in names if _is_normal_gear(n)]
        self.assertEqual(normal_gear, [],
                         f"Normal gear should NOT be pre-collected when progressive_gear=enabled; got: {normal_gear}")

    def test_progressive_gear_precollected(self):
        names = _precollected_names(self.multiworld)
        progressive_gear = [n for n in names if _is_progressive_gear(n)]
        self.assertTrue(len(progressive_gear) > 0,
                        f"Progressive gear should be pre-collected; got: {names}")


class TestNormalAndUniqueUnlockedWithProgressiveEnabled(PoeTestBase):
    """progressive_gear=enabled + gear_upgrades=all_normal_and_unique_gear_unlocked."""
    options = {
        "progressive_gear": "enabled",
        "gear_upgrades": "all_normal_and_unique_gear_unlocked",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_no_normal_gear_precollected(self):
        names = _precollected_names(self.multiworld)
        normal_gear = [n for n in names if _is_normal_gear(n)]
        self.assertEqual(normal_gear, [],
                         f"Normal gear should NOT be pre-collected when progressive_gear=enabled; got: {normal_gear}")

    def test_progressive_gear_precollected(self):
        names = _precollected_names(self.multiworld)
        progressive_gear = [n for n in names if _is_progressive_gear(n)]
        self.assertTrue(len(progressive_gear) > 0,
                        f"Progressive gear should be pre-collected; got: {names}")
