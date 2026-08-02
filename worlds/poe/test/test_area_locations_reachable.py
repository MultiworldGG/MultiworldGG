"""
Reproduction/regression check for a P2 item in plan-2.2.0.md:

Reporter: Aisu.the.Shadow (6/18/2026) reported "Reach Ancient Pyramid",
"Reach Vaal Ruins" (and "Reach Vaal Ruins" duplicate/typo in original report)
never sent their location check under 2.0.0. Status under 2.1.0 was
unconfirmed in the discord log.

This test verifies, under current code, with add_area_locations_to_location_pool
enabled:
  1. "Reach Ancient Pyramid" and "Reach Vaal Ruins" locations actually exist
     in the generated multiworld (i.e. they weren't silently dropped from the
     area location table).
  2. Both are reachable with full state (test_all_state_can_reach_everything,
     inherited from WorldTestBase, runs automatically for this options combo).
  3. Both become reachable specifically once Act 2 is reached (not stuck
     behind some later act), matching their act=2 entry in AreaLocations.json.

If part 3 fails while part 2 passes, that would point at a location being
mis-bucketed into a later/unreachable-in-practice act by
Regions.create_and_populate_regions's level-based bucketing
(Regions.py:53-56) rather than a hard-unreachable bug.
"""

from . import PoeTestBase
from .. import Locations
from ..Rules import can_reach


AREA_LOCATION_NAMES = ["Reach The Ancient Pyramid", "Reach The Vaal Ruins"]


class TestAncientPyramidAndVaalRuinsReachable(PoeTestBase):
    options = {
        "goal": "complete_act_4",
        "add_area_locations_to_location_pool": True,
        "starting_character": "marauder",
    }

    def test_locations_exist(self):
        names = {loc.name for loc in self.multiworld.get_locations()}
        for name in AREA_LOCATION_NAMES:
            self.assertIn(name, names,
                          f"{name} should be a generated location when add_area_locations_to_location_pool=True")

    def test_locations_are_act_2(self):
        """Sanity check against AreaLocations.json: both should be tagged act 2."""
        for entry in Locations.area_locations.values():
            if entry["name"] in AREA_LOCATION_NAMES:
                self.assertEqual(entry["act"], 2, f"{entry['name']} expected act=2, got {entry['act']}")

    def test_reachable_once_act_2_entered(self):
        """Both locations should become reachable specifically at the point Act 2
        is reached, not require anything beyond it."""
        world = self.multiworld.worlds[1]
        state = self.multiworld.get_all_state(False)
        by_name = {loc.name: loc for loc in self.multiworld.get_locations()}
        for name in AREA_LOCATION_NAMES:
            self.assertIn(name, by_name, f"{name} missing from generated locations")
            loc = by_name[name]
            self.assertTrue(loc.can_reach(state),
                            f"{name} should be reachable with full state (act 2 requirement met)")
