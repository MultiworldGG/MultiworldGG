from BaseClasses import ItemClassification
from test.bases import WorldTestBase

from .. import TboiWorld


class TboiTestBase(WorldTestBase):
    game = "The Binding of Isaac Repentance"
    world: TboiWorld

    def item_names(self) -> set[str]:
        return {
            item.name 
            for item in self.multiworld.itempool
        }

    def location_names(self) -> set[str]:
        return {
            location.name
            for location in self.multiworld.get_locations(self.player)
        }

    def region_names(self) -> set[str]:
        return {
            region.name
            for region in self.multiworld.get_regions(self.player)
        }

    def assert_location_accepts_progression(
        self,
        location_name: str,
        expected: bool,
    ) -> None:
        location = self.multiworld.get_location(location_name, self.player)
        progression_item = self.world.create_item("Womb Unlock")
        self.assertEqual(location.item_rule(progression_item), expected)

    def assert_location_accepts_filler(
        self,
        location_name: str,
        expected: bool = True,
    ) -> None:
        location = self.multiworld.get_location(location_name, self.player)
        filler_item = self.world.create_item("Random Coin")
        self.assertEqual(
            filler_item.classification,
            ItemClassification.filler,
        )
        self.assertEqual(location.item_rule(filler_item), expected)
