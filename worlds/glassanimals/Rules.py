# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.


from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll

from .Locations import SHORT_SONGS, SONG_REGIONS
from .Regions import ALBUM_REGIONS, REGION_REQUIRED_ITEM

if TYPE_CHECKING:
    from . import GlassAnimalsWorld


def set_all_rules(world: GlassAnimalsWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_location_rules(world: GlassAnimalsWorld) -> None:
    for loc in world.multiworld.get_locations(world.player):
        if loc.name in SONG_REGIONS:
            world.set_rule(loc, Has(loc.name, 1))


def set_completion_condition(world: GlassAnimalsWorld) -> None:
    required_items = []
    for region_name, option_name in ALBUM_REGIONS.items():
        if getattr(world.options, option_name).value:
            required_items.append(REGION_REQUIRED_ITEM[region_name])

    include_short_songs = world.options.include_short_songs.value
    for song_name, region in SONG_REGIONS.items():
        if region not in ALBUM_REGIONS or not getattr(world.options, ALBUM_REGIONS[region]).value:
            continue
        if song_name in SHORT_SONGS and not include_short_songs:
            continue
        required_items.append(song_name)

    world.set_completion_rule(HasAll(*required_items))