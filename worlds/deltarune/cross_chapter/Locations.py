from enum import StrEnum
from typing import TYPE_CHECKING

from worlds.deltarune.Locations import LocationData, LocationGroups, LocationIDs
from worlds.deltarune.LogicHelper import (
    can_access_fusion,
    include_deluxedinner_fusion,
    include_dogwidow_fusion,
    include_lost_rabbick,
    include_monarchrbn_fusion,
    include_punchbowl_fusion,
    include_spike_band_fusion,
    include_tensionbow_fusion,
    include_tensionmax_fusion,
    include_truetie_fusion,
    include_tvdinner_fusion,
    include_twin_ribbon_fusion,
    include_twistedsword_fusion,
)
from worlds.deltarune.Regions import Regions

if TYPE_CHECKING:
    from .. import DeltaruneWorld


cross_chapter_locations: dict = {
    Regions.fusion: [
        LocationData(
            LocationIDs.cc_castle_town_dd_burger_fusion,
            should_be_included=can_access_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_silver_card_fusion,
            should_be_included=can_access_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_twin_ribbon_fusion,
            should_be_included=include_twin_ribbon_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_spike_band_fusion,
            should_be_included=include_spike_band_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_tensionbow_fusion,
            should_be_included=include_tensionbow_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_twistedsword_fusion,
            should_be_included=include_twistedsword_fusion,
            group=LocationGroups.castle_town,
        ),
    ],
    Regions.lost_rabbick: [
        LocationData(
            LocationIDs.cc_lost_rabbick,
            should_be_included=include_lost_rabbick,
            group=LocationGroups.cross_chapter,
        ),
    ],
    Regions.ch5_fusion: [
        LocationData(
            LocationIDs.cc_castle_town_monarchrbn_fusion,
            should_be_included=include_monarchrbn_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_truetie_fusion,
            should_be_included=include_truetie_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_tvdinner_fusion,
            should_be_included=include_tvdinner_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_deluxedinner_fusion,
            should_be_included=include_deluxedinner_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_punchbowl_fusion,
            should_be_included=include_punchbowl_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_tensionmax_fusion,
            should_be_included=include_tensionmax_fusion,
            group=LocationGroups.castle_town,
        ),
        LocationData(
            LocationIDs.cc_castle_town_dogwidow_fusion,
            should_be_included=include_dogwidow_fusion,
            group=LocationGroups.castle_town,
        ),
    ],
}
