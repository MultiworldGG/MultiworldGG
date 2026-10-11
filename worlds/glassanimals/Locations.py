# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.


from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Location

if TYPE_CHECKING:
    from . import GlassAnimalsWorld


class GlassAnimalsLocation(Location):
    game = "Glass Animals Discography"


# Thematic freebie locations, checkable from the start (no items required)
FREEBIE_LOCATIONS = [
    "Welcome to Dreamland",
    "Heat Wave",
    "Gooey (Intro)",
    "Radio Play",
    "First Listen",
    "Encore",
    "A Dreamland Primer",
]

ILYSFM_SONGS = [
    "Show Pony",
    "whatthehellishappening?",
    "Creatures in Heaven",
    "Wonderful Nothing",
    "A Tear in Space (Airlock)",
    "I Can't Make You Fall In Love Again",
    "How I Learned To Love The Bomb",
    "White Roses",
    "On the Run",
    "Lost in the Ocean",
]

DREAMLAND_SONGS = [
    "Dreamland",
    "Tangerine",
    "((Home Movie: 1994))",
    "Hot Sugar",
    "((Home Movie: BTX))",
    "Space Ghost Coast to Coast",
    "Tokyo Drifting",
    "Melon and the Coconut",
    "Your Love (Déjà Vu)",
    "Waterfalls Coming Out Of Your Mouth",
    "It's All So Incredibly Loud",
    "((Home Movie: Rockets))",
    "Domestic Bliss",
    "Heat Waves",
    "((Home Movie: Shoes On))",
    "Helium",
]

HTBAHB_SONGS = [
    "Life Itself",
    "Youth",
    "Season 2 Episode 3",
    "Pork Soda",
    "Mama's Gun",
    "Cane Shuga",
    "[Premade Sandwiches]",
    "The Other Side of Paradise",
    "Take a Slice",
    "Poplar St",
    "Agnes",
]

ZABA_SONGS = [
    "Flip",
    "Black Mambo",
    "Pools",
    "Gooey",
    "Walla Walla",
    "Intruxx",
    "Hazey",
    "Toes",
    "Wyrd",
    "Cocoa Hooves",
    "JDNT",
]

# Short songs are only included when the include_short_songs option is enabled
SHORT_SONGS = {
    "((Home Movie: 1994))",
    "((Home Movie: BTX))",
    "((Home Movie: Rockets))",
    "((Home Movie: Shoes On))",
}

SONG_ORDER = [
    *ILYSFM_SONGS,
    *DREAMLAND_SONGS,
    *HTBAHB_SONGS,
    *ZABA_SONGS,
]

SONG_REGIONS: dict[str, str] = {
    **{song: "I Love You So F***ing Much" for song in ILYSFM_SONGS},
    **{song: "Dreamland" for song in DREAMLAND_SONGS},
    **{song: "How to Be a Human Being" for song in HTBAHB_SONGS},
    **{song: "Zaba" for song in ZABA_SONGS},
}


class LocationData(NamedTuple):
    region: str


LOCATION_TABLE: dict[str, LocationData] = {
    # Freebie locations (accessible from start, no item required)
    **{name: LocationData("Menu") for name in FREEBIE_LOCATIONS},
    # Song locations
    **{name: LocationData(region) for name, region in SONG_REGIONS.items()},
}

LOCATION_NAME_TO_ID = {
    name: 2010 + i for i, name in enumerate(LOCATION_TABLE)
}

REGIONS: dict[str, list[str]] = {}
for name, data in LOCATION_TABLE.items():
    REGIONS.setdefault(data.region, []).append(name)


def create_all_locations(world: GlassAnimalsWorld) -> None:
    include_short_songs = world.options.include_short_songs.value
    for region_name, location_names in REGIONS.items():
        try:
            region = world.get_region(region_name)
        except KeyError:
            continue
        for loc_name in location_names:
            if loc_name in SHORT_SONGS and not include_short_songs:
                continue
            loc = GlassAnimalsLocation(
                world.player,
                loc_name,
                LOCATION_NAME_TO_ID[loc_name],
                region,
            )
            region.locations.append(loc)