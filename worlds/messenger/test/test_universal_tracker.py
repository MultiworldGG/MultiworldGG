import unittest
from typing import Any, ClassVar, cast

from test.general import setup_multiworld
from test.param import classvar_matrix

from ...AutoWorld import call_all
from .. import MessengerWorld
from ..connections import RANDOMIZED_CONNECTIONS, TRANSITIONS
from ..options import ShufflePortals, ShuffleTransitions
from ..portals import PORTALS
from ..shop import FIGURINES, SHOP_ITEMS
from . import MessengerTestBase

UT_GEN_STEPS = ("generate_early", "create_regions", "create_items", "set_rules", "connect_entrances", "generate_basic")

WORLD_TO_TRACKER_ENTRANCE_MAPPING = {
    "HQ - Artificer's Challenge": "Artificer's Challenge",
    "HQ - Artificer's Portal": "Artificer's Portal",
} | {f"HQ - {portal} Portal": f"ToTHQ {portal} Portal" for portal in PORTALS}

class UniversalTrackerTestBase(MessengerTestBase):
    """
    Will generate a solo seed to build a real slot data. Then, will generate a
    second solo seed using said slot data for the `re_gen_passthrough` used by
    universal tracker.
    """
    run_default_tests = False

    slot_data: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        if cls is UniversalTrackerTestBase:
            raise unittest.SkipTest("No running tests on UniversalTrackerTestBase import.")
        super().setUpClass()

    def setUp(self) -> None:
        super().setUp()
        if not hasattr(self, "world"):
            return

        self.slot_data = self.world.fill_slot_data().copy()

        self.multiworld = setup_multiworld(MessengerWorld, steps=(), options=self.options)
        self.world = cast(MessengerWorld, self.multiworld.worlds[self.player])

        self.multiworld.re_gen_passthrough = {MessengerWorld.game: self.slot_data}
        self.multiworld.enforce_deferred_connections = "default"

        for step in UT_GEN_STEPS:
            call_all(self.multiworld, step)


class DefaultUniversalTrackerTest(UniversalTrackerTestBase):
    def test_starting_portals_are_reapplied(self) -> None:
        self.assertListEqual(self.slot_data["starting_portals"], self.world.starting_portals)

    def test_starting_portals_unlock_events_are_hidden(self) -> None:
        for portal in self.slot_data["starting_portals"]:
            region = portal[:-7]
            self.assertIn(f"{region} - Portal unlock", self.world.ut_map_page_hidden_events[region])

    def test_price_shop_are_reversed(self) -> None:
        self.assertDictEqual(
            self.slot_data["shop"],
            {SHOP_ITEMS[item].internal_name: price for item, price in self.world.shop_prices.items()},
        )
        self.assertDictEqual(
            self.slot_data["figures"],
            {FIGURINES[item].internal_name: price for item, price in self.world.figurine_prices.items()},
        )
        self.assertEqual(self.slot_data["max_price"], self.world.total_shards)

    def test_deferred_level_exists_are_hidden(self) -> None:
        hidden_entrances = {e for entrances in self.world.ut_map_page_hidden_entrances.values() for e in entrances}
        for e in RANDOMIZED_CONNECTIONS.keys():
            self.assertIn(e, hidden_entrances)

    def test_deferred_hq_portals_are_hidden(self) -> None:
        for portal in PORTALS:
            self.assertIn(f"HQ - {portal} Portal", self.world.ut_map_page_hidden_entrances["Overworld"])


@classvar_matrix(shuffle_portals=ShufflePortals.options.keys() - ShufflePortals.aliases.keys())
class ShufflePortalsUniversalTrackerTest(UniversalTrackerTestBase):
    shuffle_portals: ClassVar[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = {
            "shuffle_portals": self.shuffle_portals,
        }

    def test_can_recreate_world(self) -> None:
        self.assertListEqual(self.slot_data["starting_portals"], self.world.starting_portals)
        self.assertListEqual(self.slot_data["portal_exits"], self.world.portal_mapping)


@classvar_matrix(shuffle_transitions=ShuffleTransitions.options.keys() - ShuffleTransitions.aliases.keys())
class ShuffleTransitionsCoupledUniversalTrackerTest(UniversalTrackerTestBase):
    shuffle_transitions: ClassVar[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = {
            "shuffle_transitions": self.shuffle_transitions,
        }

    def test_can_recreate_world(self) -> None:
        re_gen_transitions = [
            [
                TRANSITIONS.index(
                    RANDOMIZED_CONNECTIONS[WORLD_TO_TRACKER_ENTRANCE_MAPPING.get(transition.name, transition.name)]
                ),
                TRANSITIONS.index(
                    transition.connected_region.name
                    if transition.connected_region is not None
                    else self.world.deferred_connections[transition.name]
                ),
            ]
            for transition in self.world.transitions
        ]

        self.assertListEqual(self.slot_data["starting_portals"], self.world.starting_portals)
        self.assertListEqual(self.slot_data["transitions"], re_gen_transitions)
