from BaseClasses import CollectionState
from .bases import PokemonCrystalTestBase
from ..data import data
from ..fly import get_fly_regions, SILVER_CAVE_FLY_INDEX


class FlyUnlockItemsTest(PokemonCrystalTestBase):
    options = {
        "randomize_fly_unlocks": "off",
        "randomize_fly_destinations": "off",
    }

    def flypoints(self):
        fly_regions = get_fly_regions(self.world)
        if self.world.options.randomize_fly_destinations:
            return [(f"Fly Destination {i}", i, fr) for i, fr in enumerate(fly_regions, start=1)]
        return [(f"REGION_FLY -> {fr.exit_region}", fr.id, fr) for fr in fly_regions]

    def opens(self, entrance_name, item):
        state = CollectionState(self.multiworld)
        state.collect(item, prevent_sweep=True)
        return self.multiworld.get_entrance(entrance_name, self.player).access_rule(state)

    def test_flypoints_opened_by_either_fly_item(self):
        for entrance_name, flypoint, _ in self.flypoints():
            entrance = self.multiworld.get_entrance(entrance_name, self.player)
            self.assertFalse(entrance.access_rule(CollectionState(self.multiworld)), entrance_name)
            for item in (f"Fly {data.fly_regions[flypoint - 1].name}", f"Fly Unlock {flypoint}"):
                self.assertTrue(self.opens(entrance_name, self.world.create_item(item)),
                                f"{entrance_name} not opened by {item}")

    def test_visit(self):
        for entrance_name, _, fly_region in self.flypoints():
            visit = self.world.create_event(f"EVENT_VISITED_{fly_region.base_identifier}")
            self.assertEqual(self.opens(entrance_name, visit), not self.world.options.randomize_fly_unlocks,
                             entrance_name)


class FlyUnlockItemsDestinationsTest(FlyUnlockItemsTest):
    options = {**FlyUnlockItemsTest.options, "randomize_fly_destinations": "on"}


class FlyUnlockItemsJohtoOnlyTest(FlyUnlockItemsTest):
    options = {**FlyUnlockItemsTest.options, "johto_only": "on"}


class FlyUnlockItemsDestinationsJohtoOnlyTest(FlyUnlockItemsTest):
    options = {**FlyUnlockItemsDestinationsTest.options, "johto_only": "on"}


class FlyUnlockItemsRandomizedTest(FlyUnlockItemsTest):
    options = {**FlyUnlockItemsTest.options, "randomize_fly_unlocks": "on"}


class FlyUnlockItemsRandomizedDestinationsTest(FlyUnlockItemsTest):
    options = {**FlyUnlockItemsRandomizedTest.options, "randomize_fly_destinations": "on"}


class FlyUnlockItemsRandomizedDestinationsJohtoOnlyTest(FlyUnlockItemsTest):
    options = {**FlyUnlockItemsRandomizedDestinationsTest.options, "johto_only": "on"}


class FlyUnlockItemsExcludeSilverCaveTest(FlyUnlockItemsTest):
    options = {**FlyUnlockItemsTest.options, "randomize_fly_unlocks": "exclude_silver_cave"}

    def test_locked_silver_cave_item_opens_flypoint(self):
        item = self.multiworld.get_location("Visit Silver Cave", self.player).item
        entrance_name = next(name for name, flypoint, _ in self.flypoints() if flypoint == SILVER_CAVE_FLY_INDEX)
        self.assertTrue(self.opens(entrance_name, item), f"{entrance_name} not opened by {item.name}")


class FlyUnlockItemsExcludeSilverCaveDestinationsTest(FlyUnlockItemsExcludeSilverCaveTest):
    options = {**FlyUnlockItemsExcludeSilverCaveTest.options, "randomize_fly_destinations": "on"}


class FlyUnlockItemsExcludeSilverCaveIncludeSilverCaveTest(FlyUnlockItemsExcludeSilverCaveTest):
    options = {**FlyUnlockItemsExcludeSilverCaveTest.options, "johto_only": "include_silver_cave"}


class FlyUnlockItemsExcludeSilverCaveIncludeSilverCaveDestinationsTest(FlyUnlockItemsExcludeSilverCaveTest):
    options = {**FlyUnlockItemsExcludeSilverCaveDestinationsTest.options, "johto_only": "include_silver_cave"}


class FlyUnlockItemsExcludeSilverCaveJohtoOnlyDestinationsTest(FlyUnlockItemsTest):
    options = {**FlyUnlockItemsExcludeSilverCaveDestinationsTest.options, "johto_only": "on"}
