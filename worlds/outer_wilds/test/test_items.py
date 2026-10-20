from .bases import OuterWildsTestBase
from ..options import ShuffleEquipment


easy_equipment = {
    "Surface Integrity Scanner",
    "Eject Button",
    "Landing Camera",
}
normal_equipment = {
    "Autopilot",
    "Velocity Matcher",
}
hard_equipment = {
    "Ship Medkit",
    "Ship Jetpack Refueler",
    "Velocity Indicator",
    "Distance Indicator",
    "Ship Lights",
}


class TestShuffleSpacesuitTrue(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": True,
    }

    def test_shuffle_spacesuit_true(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        self.assertSetEqual(precollected_item_names, hard_equipment)
        self.assertIn("Spacesuit", itempool_names)


class TestShuffleSpacesuitFalse(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": False,
    }

    def test_shuffle_spacesuit_false(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        self.assertSetEqual(precollected_item_names, hard_equipment.union({"Spacesuit"}))
        self.assertNotIn("Spacesuit", itempool_names)


class TestShuffleEquipmentEasy(OuterWildsTestBase):
    options = {
        "shuffle_equipment": ShuffleEquipment.option_easy,
    }

    def test_shuffle_equipment(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        for e in easy_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)
        for e in normal_equipment:
            self.assertIn(e, precollected_item_names)
            self.assertNotIn(e, itempool_names)
        for e in hard_equipment:
            self.assertIn(e, precollected_item_names)
            self.assertNotIn(e, itempool_names)


class TestShuffleEquipmentNormal(OuterWildsTestBase):
    options = {
        "shuffle_equipment": ShuffleEquipment.option_normal,
    }

    def test_shuffle_equipment(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        for e in easy_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)
        for e in normal_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)
        for e in hard_equipment:
            self.assertIn(e, precollected_item_names)
            self.assertNotIn(e, itempool_names)


class TestShuffleEquipmentHard(OuterWildsTestBase):
    options = {
        "shuffle_equipment": ShuffleEquipment.option_hard,
    }

    def test_shuffle_equipment(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        for e in easy_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)
        for e in normal_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)
        for e in hard_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)

