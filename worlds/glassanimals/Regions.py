# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.


from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import Has

if TYPE_CHECKING:
    from . import GlassAnimalsWorld


ALBUM_REGIONS: dict[str, str] = {
    "Dreamland":                    "include_dreamland",
    "I Love You So F***ing Much":   "include_ilysfm",
    "How to Be a Human Being":      "include_htbahb",
    "Zaba":                         "include_zaba",
}

# The item needed to enter each album region.
# Most regions share their name with the album item, but Dreamland's item is "Dreamland (Album)".
REGION_REQUIRED_ITEM: dict[str, str] = {
    "Dreamland":                    "Dreamland (Album)",
    "I Love You So F***ing Much":   "I Love You So F***ing Much",
    "How to Be a Human Being":      "How to Be a Human Being",
    "Zaba":                         "Zaba",
}


def create_and_connect_regions(world: GlassAnimalsWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    for region_name, option_name in ALBUM_REGIONS.items():
        if getattr(world.options, option_name).value:
            album_region = Region(region_name, world.player, world.multiworld)
            world.multiworld.regions.append(album_region)
            menu.connect(album_region, rule=Has(REGION_REQUIRED_ITEM[region_name]))