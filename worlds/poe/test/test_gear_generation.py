"""
Integration tests for gear generation modes.

Each class runs a full world generation (via WorldTestBase) with a specific
progressive_gear option, then asserts which item types appear in the pool.

progressive_gear modes:
  enabled (1)                    → Progressive gear only; Random Gear removed
  disabled (0)                   → Random Gear only; Progressive Gear removed
  progressive_except_for_unique  → Both Progressive gear AND Unique Random gear;
                                   Normal/Magic/Rare Random Gear removed
"""

from . import PoeTestBase
from .. import Items


def _pool_names(multiworld, player=1):
    """Return a set of item names currently in the multiworld item pool."""
    return {item.name for item in multiworld.itempool if item.player == player}


# Names of items in the "Progressive Gear" category — derived once from the source table.
_PROGRESSIVE_GEAR_NAMES = {
    item["name"] for item in Items.item_table.values()
    if "Progressive Gear" in item.get("category", [])
}

# Names of items in the "Random Gear" category, split by unique vs non-unique.
_RANDOM_GEAR_NAMES = {
    item["name"] for item in Items.item_table.values()
    if "Random Gear" in item.get("category", [])
}
_UNIQUE_RANDOM_GEAR_NAMES = {
    item["name"] for item in Items.item_table.values()
    if "Random Gear" in item.get("category", []) and "Unique" in item.get("category", [])
}
_NON_UNIQUE_RANDOM_GEAR_NAMES = _RANDOM_GEAR_NAMES - _UNIQUE_RANDOM_GEAR_NAMES


def _has_progressive_gear(pool_names):
    return bool(pool_names & _PROGRESSIVE_GEAR_NAMES)


def _has_random_normal_gear(pool_names):
    """Normal/Magic/Rare Random Gear (not unique) still in pool."""
    return bool(pool_names & _NON_UNIQUE_RANDOM_GEAR_NAMES)


def _has_unique_random_gear(pool_names):
    return bool(pool_names & _UNIQUE_RANDOM_GEAR_NAMES)


class TestProgressiveGearEnabled(PoeTestBase):
    """progressive_gear = enabled → only Progressive gear in pool."""
    options = {
        "progressive_gear": "enabled",
        "goal": "complete_act_1",
        "gucci_hobo_mode": "disabled",
    }

    def test_progressive_gear_items_exist(self):
        pool = _pool_names(self.multiworld)
        self.assertTrue(_has_progressive_gear(pool),
                        "Progressive gear items should be in the item pool")

    def test_no_random_normal_gear(self):
        pool = _pool_names(self.multiworld)
        self.assertFalse(_has_random_normal_gear(pool),
                         "Normal/Magic/Rare Random Gear should not be in pool when progressive enabled")

    def test_no_unique_random_gear(self):
        pool = _pool_names(self.multiworld)
        self.assertFalse(_has_unique_random_gear(pool),
                         "Unique Random Gear should not be in pool when progressive enabled (not gucci mode)")


class TestProgressiveGearDisabled(PoeTestBase):
    """progressive_gear = disabled → only Random Gear (all rarities) in pool."""
    options = {
        "progressive_gear": "disabled",
        "goal": "complete_act_1",
        "gucci_hobo_mode": "disabled",
    }

    def test_random_gear_exists(self):
        pool = _pool_names(self.multiworld)
        self.assertTrue(_has_random_normal_gear(pool) or _has_unique_random_gear(pool),
                        "Random Gear (Normal/Unique) should be in pool when progressive disabled")

    def test_no_progressive_gear(self):
        pool = _pool_names(self.multiworld)
        self.assertFalse(_has_progressive_gear(pool),
                         "Progressive Gear should not be in pool when progressive disabled")


class TestProgressiveExceptForUnique(PoeTestBase):
    """progressive_except_for_unique → Progressive gear + Unique Random gear coexist;
    Normal/Magic/Rare Random Gear is removed."""
    options = {
        "progressive_gear": "progressive_except_for_unique",
        "goal": "complete_act_1",
        "gucci_hobo_mode": "disabled",
    }

    def test_progressive_gear_exists(self):
        pool = _pool_names(self.multiworld)
        self.assertTrue(_has_progressive_gear(pool),
                        "Progressive gear items should be in pool in progressive_except_for_unique mode")

    def test_unique_random_gear_exists(self):
        pool = _pool_names(self.multiworld)
        self.assertTrue(_has_unique_random_gear(pool),
                        "Unique Random Gear should remain in pool in progressive_except_for_unique mode")

    def test_no_normal_magic_rare_random_gear(self):
        pool = _pool_names(self.multiworld)
        self.assertFalse(_has_random_normal_gear(pool),
                         "Normal/Magic/Rare Random Gear should be removed in progressive_except_for_unique mode")

    def test_both_gear_types_coexist(self):
        """Core assertion: progressive items AND unique random items are both present."""
        pool = _pool_names(self.multiworld)
        has_prog = _has_progressive_gear(pool)
        has_unique = _has_unique_random_gear(pool)
        self.assertTrue(has_prog and has_unique,
                        f"Expected both Progressive gear and Unique Random gear. "
                        f"progressive={has_prog}, unique_random={has_unique}")

    def test_progressive_gear_counts_reduced(self):
        """Progressive gear counts are reduced by 1 (to leave room for the unique random slot).

        cleanup_gear_based_on_progressive_option decrements count by 1 for non-flask
        Progressive Gear items in this mode, so the pool count for at least one item
        should be less than its full-table count.
        """
        from collections import Counter

        # Full counts from the source item table (before any generation adjustments)
        full_counts = {item["name"]: item.get("count", 1)
                       for item in Items.get_gear_items()
                       if "Progressive Gear" in item["category"] and "Flask" not in item["category"]}

        # Pool counts after generation (each Item object = 1 copy)
        pool_counts = Counter(
            item.name for item in self.multiworld.itempool
            if item.player == 1 and item.name in full_counts
        )

        reduced = [name for name, full in full_counts.items()
                   if name in pool_counts and pool_counts[name] < full]
        self.assertTrue(len(reduced) > 0,
                        f"Expected some Progressive gear items to have reduced counts; "
                        f"full={dict(list(full_counts.items())[:3])}, "
                        f"pool={dict(list(pool_counts.items())[:3])}")
