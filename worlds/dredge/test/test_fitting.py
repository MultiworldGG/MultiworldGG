from unittest import TestCase

from BaseClasses import CollectionState
from .bases import DredgeTestBase
from ..fitting import best_total, hulls_needed
from ..items import item_table
from ..rules import can_equip


class TestHullsNeeded(TestCase):
    def test_every_rod_net_engine_and_light_fits_some_hull(self) -> None:
        for name, item in item_table.items():
            if item.item_group not in ("Rod", "Net", "Engine", "Light"):
                continue
            for include_iron_rig in (False, True):
                with self.subTest(item=name, include_iron_rig=include_iron_rig):
                    self.assertTrue(item.shape, f"{name} has no shape")
                    hulls_needed(name, include_iron_rig)

    def test_known_fits(self) -> None:
        expected = {
            "Starting Gear - Basic Fishing Pole": 0,
            "Flexible Fishing Pole": 0,
            "Hydraulic Rod": 0,
            "Bottomless Lines": 1,
            "Viscera Crane": 1,
            "Versatile Rod": 2,
            "Tendon Rod": 2,
            "Harvesting Platform": 2,
            "Basic Trawl Net": 1,
            "Siphon Trawler": 1,
            "Large Trawl Net": 3,
            "Heavy-Duty Trawl Net": 3,
        }
        for name, hulls in expected.items():
            for include_iron_rig in (False, True):
                with self.subTest(item=name, include_iron_rig=include_iron_rig):
                    self.assertEqual(hulls_needed(name, include_iron_rig), hulls)

    def test_items_without_a_shape_need_no_hull(self) -> None:
        self.assertEqual(hulls_needed("Dredge Crane", False), 0)
        self.assertEqual(hulls_needed("Not An Item", False), 0)


class TestBestTotal(TestCase):
    def test_starting_hull_fits_only_one_of_two_engines(self) -> None:
        engines = ["Starting Gear - Peculiar Engine", "Twin Prop Engine"]
        self.assertEqual(best_total(engines, "speed", 0, False), 35)
        self.assertEqual(best_total(engines, "speed", 1, False), 49)

    def test_two_cell_light_needs_a_hull(self) -> None:
        self.assertEqual(best_total(["Halogen Spotlight"], "lumens", 0, False), 0)
        self.assertEqual(best_total(["Halogen Spotlight"], "lumens", 1, False), 1800)

    def test_picks_the_best_light_that_fits(self) -> None:
        lights = ["Cracked Bulb", "Halogen Spotlight", "Flame of the Sky"]
        self.assertEqual(best_total(lights, "lumens", 1, False), 3500)
        self.assertEqual(best_total(lights, "lumens", 4, True), 5300)

    def test_rebuyable_items_count_more_than_once(self) -> None:
        self.assertEqual(best_total(["Jet Drive Engine"], "speed", 1, False), 54)
        self.assertEqual(best_total(["Cloudy Lens"], "lumens", 1, False), 1500)

    def test_other_items_count_once(self) -> None:
        self.assertEqual(best_total(["Starting Gear - Peculiar Engine"], "speed", 1, False), 14)
        self.assertEqual(best_total(["Flame of the Sky"], "lumens", 4, True), 3500)

    def test_nothing_owned(self) -> None:
        self.assertEqual(best_total([], "speed", 4, True), 0)


class TestCanEquip(DredgeTestBase):
    run_default_tests = False

    def test_versatile_rod_needs_two_hulls(self) -> None:
        world = self.multiworld.worlds[self.player]
        state = CollectionState(self.multiworld)
        state.collect(world.create_item("Versatile Rod"), True)
        state.collect(world.create_item("Progressive Hull"), True)
        self.assertFalse(can_equip("Versatile Rod", state, self.player, False))
        state.collect(world.create_item("Progressive Hull"), True)
        self.assertTrue(can_equip("Versatile Rod", state, self.player, False))
