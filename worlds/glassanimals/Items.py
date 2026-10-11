# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.


from BaseClasses import Item, ItemClassification

from typing import TypedDict

from .Locations import SHORT_SONGS, SONG_ORDER, SONG_REGIONS
from .Regions import ALBUM_REGIONS

class GlassAnimalsItem(Item):
    game: str = "Glass Animals Discography"

class ItemDict(TypedDict):
    classification: ItemClassification
    name: str

ALBUM_NAMES = [
    "Dreamland (Album)",
    "I Love You So F***ing Much",
    "How to Be a Human Being",
    "Zaba",
]

FILLER_NAMES = [
    "Pineapples",
    "Frequency",
    "Signal",
    "Static",
]

ITEM_NAME_TO_ID = {
    **{name: 2010 + i for i, name in enumerate(ALBUM_NAMES)},
    **{name: 2010 + len(ALBUM_NAMES) + i for i, name in enumerate(SONG_ORDER)},
    **{name: 2010 + len(ALBUM_NAMES) + len(SONG_ORDER) + i for i, name in enumerate(FILLER_NAMES)},
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    **{name: ItemClassification.progression for name in ALBUM_NAMES},
    **{name: ItemClassification.progression for name in SONG_ORDER},
    **{name: ItemClassification.filler for name in FILLER_NAMES},
}

ALBUM_OPTIONS = {
    "Dreamland (Album)":       "include_dreamland",
    "I Love You So F***ing Much": "include_ilysfm",
    "How to Be a Human Being": "include_htbahb",
    "Zaba":                    "include_zaba",
}


def create_item_with_correct_classification(world, name: str) -> GlassAnimalsItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return GlassAnimalsItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def get_random_filler_item_name(world) -> str:
    return world.random.choice(FILLER_NAMES)


def create_all_items(world) -> None:
    itempool: list[Item] = []

    for album_name, option_name in ALBUM_OPTIONS.items():
        if getattr(world.options, option_name).value:
            itempool.append(world.create_item(album_name))

    include_short_songs = world.options.include_short_songs.value
    for song_name, region in SONG_REGIONS.items():
        if region not in ALBUM_REGIONS or not getattr(world.options, ALBUM_REGIONS[region]).value:
            continue
        if song_name in SHORT_SONGS and not include_short_songs:
            continue
        itempool.append(world.create_item(song_name))

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_filler = number_of_unfilled_locations - len(itempool)
    itempool += [world.create_filler() for _ in range(needed_filler)]

    world.multiworld.itempool += itempool