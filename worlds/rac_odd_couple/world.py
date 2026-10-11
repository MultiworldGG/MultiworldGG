from __future__ import annotations

import os
from typing import ClassVar, Union

import settings
from BaseClasses import Region, Tutorial
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import set_rule

from .items import OddCoupleItem, item_table, progression_items
from .locations import OddCoupleLocation, location_table


class OddCoupleSettings(settings.Group):
    class SwfFile(settings.UserFilePath):
        """Path to your own copy of the vanilla odd_couple.swf. If this file can't
        be found, you'll be prompted to browse for it (and the choice is remembered)."""
        description = "Odd Couple vanilla swf"

    swf_file: Union[SwfFile, str] = SwfFile("odd_couple.swf")


class OddCoupleWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Ratchet & Clank: The Odd Couple for MultiworldGG.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AP Community"],
    )]


class OddCoupleWorld(World):
    """
    The Odd Couple is the Flash minigame tucked away in the Ratchet & Clank series,
    in which Ratchet whiles away an evening alone in his apartment: answering the
    phone, dodging the taxi driver, putting up with the gimp, and surviving the night.
    """

    game = "Ratchet & Clank: The Odd Couple"
    web = OddCoupleWeb()
    options_dataclass = PerGameCommonOptions

    # World lives in world.py rather than __init__.py, so the default
    # settings_key (derived from the module path) would be wrong - pin it.
    settings_key = "rac_odd_couple_options"
    settings: ClassVar[OddCoupleSettings]

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    def create_item(self, name: str) -> OddCoupleItem:
        data = item_table[name]
        return OddCoupleItem(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:
        return "Nothing"

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        menu.locations += [
            OddCoupleLocation(self.player, name, data.code, menu)
            for name, data in location_table.items()
        ]
        self.multiworld.regions.append(menu)

    def create_items(self) -> None:
        self.multiworld.itempool += [self.create_item(name) for name in progression_items]

        # One copy of each progression item isn't guaranteed to fill every
        # location (e.g. "Gimp" gates 3 locations with a single held copy) -
        # pad out the remainder with filler so every location still gets an item.
        # Stashed for set_rules, since the goal is collecting every one of them.
        self.filler_count = len(location_table) - len(progression_items)
        if self.filler_count > 0:
            self.multiworld.itempool += [self.create_item("Nothing") for _ in range(self.filler_count)]

    def set_rules(self) -> None:
        # Every location is inaccessible until its matching item is received,
        # except "The Odd Couple Intro" (item is None), which has no
        # requirement - it's the always-reachable bootstrap location that
        # seeds the very first item, auto-checked by the client on connect.
        for name, data in location_table.items():
            if data.item is None:
                continue
            location = self.multiworld.get_location(name, self.player)
            set_rule(location, lambda state, item=data.item: state.has(item, self.player))

        # Goal: every scene unlocked, i.e. all 6 named items received. Holding
        # them unlocks every location (Gimp's 3 replays included), regardless
        # of what's actually placed at each one - "Nothing" filler isn't part
        # of this check.
        full_clear = {name: 1 for name in progression_items}
        self.multiworld.completion_condition[self.player] = lambda state: state.has_all_counts(
            full_clear, self.player)

    def generate_output(self, output_directory: str) -> None:
        # The patch is a procedure (see patch.py), not a binary diff, so
        # generation doesn't need a copy of the vanilla swf at all - only the
        # player applying the .apoddcouple file does, on their own machine.
        from .patch import OddCouplePatch

        out_base = self.multiworld.get_out_file_name_base(self.player)
        patch = OddCouplePatch(os.path.join(output_directory, f"{out_base}{OddCouplePatch.patch_file_ending}"),
                               player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write()
