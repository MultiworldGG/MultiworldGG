from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Sims4World

class UTMixin:

    ut_can_gen_without_yaml = True
    passthrough: dict[str, Any]

    # for UT, not called in standard generation
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # returns slot data to be used in UT regen
        return slot_data

    def get_options_from_slot_data(self, world: Sims4World):

        if hasattr(world.multiworld, "re_gen_passthrough"):
            if "The Sims 4" in world.multiworld.re_gen_passthrough:
                self.passthrough = world.multiworld.re_gen_passthrough["The Sims 4"]
                world.options.goal.value = self.passthrough["goal_value"]
                world.options.career.value = self.passthrough["career_value"]
                world.options.expansion_packs.value = self.passthrough["expansion_packs"]
                world.options.game_packs.value = self.passthrough["game_packs"]
                world.options.stuff_packs.value = self.passthrough["stuff_packs"]
                world.options.cas_kits.value = self.passthrough["cas_kits"]
                world.options.build_kits.value = self.passthrough["build_kits"]