from BaseClasses import Location
from typing import TYPE_CHECKING

from worlds.deltarune.Locations import LocationData, LocationGroups, LocationIDs
from worlds.deltarune.Regions import Regions

if TYPE_CHECKING:
    from .. import DeltaruneWorld

chapter5_locations = {
    Regions.ch5_mew_mew_shop: [
        LocationData(
            id=LocationIDs.ch5_pinks_shop_1,
            group=LocationGroups.chapter5,
        ),
        LocationData(
            id=LocationIDs.ch5_pinks_shop_2,
            group=LocationGroups.chapter5,
        ),
        LocationData(
            id=LocationIDs.ch5_pinks_shop_3,
            group=LocationGroups.chapter5,
        ),
        LocationData(
            id=LocationIDs.ch5_pinks_shop_4,
            group=LocationGroups.chapter5,
        ),
    ],
    Regions.ch5_flower_rewards: [
        LocationData(
            id=LocationIDs.ch5_castle_top_flower_gift_aqua,
            group=LocationGroups.chapter5,
        ),
        LocationData(
            id=LocationIDs.ch5_castle_top_flower_gift_orange,
            group=LocationGroups.chapter5,
        ),
        LocationData(
            id=LocationIDs.ch5_castle_top_flower_gift_blue,
            group=LocationGroups.chapter5,
        ),
        LocationData(
            id=LocationIDs.ch5_castle_top_flower_gift_seth,
            group=LocationGroups.chapter5,
        ),
        LocationData(
            id=LocationIDs.ch5_castle_top_flower_gift_green,
            group=LocationGroups.chapter5,
        ),
        LocationData(
            id=LocationIDs.ch5_castle_top_flower_gift_yellow,
            group=LocationGroups.chapter5,
        ),
        LocationData(
            id=LocationIDs.ch5_castle_top_flowerys_gift,
            group=LocationGroups.chapter5,
        ),
    ],
}
