# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.


from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World
from . import Items as glass_animals_items
from . import Locations as glass_animals_locations
from . import Regions as glass_animals_regions
from . import Rules as glass_animals_rules
from .Options import GlassAnimalsOptions
from .Web import GlassAnimalsWeb
from .UT import UTMixin

class GlassAnimalsWorld(World, UTMixin):
    """Glass Animals' discography as an AP/MWGG integration where you get checks by listening to music"""

    game = "Glass Animals Discography"
    web = GlassAnimalsWeb()

    base_id = 2010

    options_dataclass = GlassAnimalsOptions
    options: GlassAnimalsOptions

    item_name_to_id = glass_animals_items.ITEM_NAME_TO_ID
    location_name_to_id = glass_animals_locations.LOCATION_NAME_TO_ID

    def generate_early(self) -> None:
        # this is specific to UT, doesn't apply in normal generation
        self.get_options_from_slot_data(self)

    def create_regions(self) -> None:
        glass_animals_regions.create_and_connect_regions(self)
        glass_animals_locations.create_all_locations(self)

    def set_rules(self) -> None:
        glass_animals_rules.set_all_rules(self)
        glass_animals_rules.set_completion_condition(self)

    def create_item(self, name: str) -> glass_animals_items.GlassAnimalsItem:
        return glass_animals_items.create_item_with_correct_classification(self, name)

    def create_items(self) -> None:
        glass_animals_items.create_all_items(self)

    def get_filler_item_name(self) -> str:
        return glass_animals_items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "include_dreamland": self.options.include_dreamland.value,
            "include_ilysfm": self.options.include_ilysfm.value,
            "include_htbahb": self.options.include_htbahb.value,
            "include_zaba": self.options.include_zaba.value,
            "include_short_songs": self.options.include_short_songs.value,
        }