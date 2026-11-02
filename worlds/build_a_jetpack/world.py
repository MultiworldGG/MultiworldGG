import logging
from collections.abc import Mapping
from typing import Dict, Optional, Any

from worlds.AutoWorld import World
from Options import Option

from . import items, locations, regions, rules, web_world
from . import options as buildjetpack_options

logger = logging.getLogger("Build a Jetpack")

class BuildJetpackWorld(World):
    """
    Build a Jetpack is a PICO-8 game where you dive into the ocean to gather fish and materials.
    The goal of the game is to build a powerful jetpack to fly into the skies.
    """

    game = "Build a Jetpack"
    web = web_world.BuildJetpackWebWorld()
    options_dataclass = buildjetpack_options.BuildJetpackOptions
    options: buildjetpack_options.BuildJetpackOptions
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID
    origin_region_name = "Raft"
    ut_can_gen_without_yaml = True

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.BuildJetpackItem:
        return items.create_item_with_correct_classification(self, name)
    
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "options": self.options.as_dict("death_link", "fishsanity", "harsh_pressure", "extra_upgrades", "trap_chance"),
        }
    
    def generate_early(self) -> None:
        # don't allow settings combinations that will do horrible things to generation
        if self.options.extra_upgrades and not self.options.fishsanity:
            logger.warning(f"Build a Jetpack ({self.player_name}): Extra Upgrades were enabled, but the item pool does not have the space to fit them. Extra Upgrades will be forced off.")
            self.options.extra_upgrades.value = False

        # universal tracker
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            slot_options: dict[str, Any] = slot_data.get("options", {})
            for key, value in slot_options.items():
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    setattr(self.options, key, opt.from_any(value))
    
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data