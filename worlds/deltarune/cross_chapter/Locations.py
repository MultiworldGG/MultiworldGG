from enum import StrEnum
from typing import TYPE_CHECKING

from worlds.deltarune.Locations import LocationData, LocationGroups, LocationIDs
from worlds.deltarune.Regions import Regions

if TYPE_CHECKING:
    from .. import DeltaruneWorld


cross_chapter_locations: dict = {
    Regions.fusion: [
        LocationData(
            LocationIDs.cc_castle_town_dd_burger_fusion,
            should_be_included=lambda world: world.can_access_fusion(),
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_silver_card_fusion,
            should_be_included=lambda world: world.can_access_fusion(),
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_twin_ribbon_fusion,
            should_be_included=lambda world: world.can_access_fusion()
            and world.has_at_least_one_chapter_included([2, 3])
            and (
                (world.is_starting_equipment_removed() and world.has_at_least_one_chapter_included([1, 3]))
                or (not world.is_starting_equipment_removed() and world.has_at_least_one_chapter_included([1, 2, 3]))
            ),
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_spike_band_fusion,
            should_be_included=lambda world: world.can_access_fusion()
            and world.include_chapter(1)
            and (
                world.include_chapter(2)
                or (
                    not world.is_starting_equipment_removed()
                    and (world.include_chapter(4) or world.have_all_chapters_included([3, 4]))
                )
            ),
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_tensionbow_fusion,
            should_be_included=lambda world: world.can_access_fusion()
            and world.include_chapter(2)
            and (not world.is_weird_route() or world.is_all_routes()),
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_twistedsword_fusion,
            should_be_included=lambda world: world.can_access_fusion()
            and world.include_chapter(2)
            and world.is_unused_items_included()
            and world.is_weird_route(),
            group=LocationGroups.castle_town,
        ),
    ],
    Regions.lost_rabbick: [
        LocationData(
            LocationIDs.cc_lost_rabbick,
            should_be_included=lambda world: (world.include_chapter(3) and world.is_all_routes())
            or (world.include_chapter(1) and world.is_weird_route() and world.is_chapter_1_recruit_system_enabled()),
            group=LocationGroups.cross_chapter,
        ),
    ],
}
