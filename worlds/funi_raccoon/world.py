from collections.abc import Mapping
from typing import Any

from BaseClasses import ItemClassification
from worlds.AutoWorld import World
from Options import OptionError

from . import items, locations, regions, rules, web_world
from . import options as FuniRaccoon_options

class FuniRaccoonWorld(World):
    """
    Funi Raccoon Game is a game about a Funi Raccoon who steals things.
    """
    
    game = "Funi Raccoon Game"
    web = web_world.FuniRaccoonWebWorld()

    options_dataclass = FuniRaccoon_options.FuniRaccoonOptions
    options: FuniRaccoon_options.FuniRaccoonOptions 

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID
    item_name_groups = {**items.ITEM_GROUPS, "Dumpster Items": set(rules.DUMPSTER_ITEMS)}

    origin_region_name = "Overworld"

    ut_can_gen_without_yaml = True
    glitches_item_name: str = "out_of_logic"
        
    def generate_early(self) -> None:
        if "lugh" in self.options.goal.value:
            self.options.gemsanity.value = True
            
        museum = self.options.museum_threshold.value
        act2 = self.options.act2_threshold.value
        act3 = self.options.act3_threshold.value
        act4 = self.options.act4_threshold.value

        if act2 <= museum:
            raise OptionError(
                f"Act 2 Threshold ({act2}) must be strictly greater than Museum Threshold ({museum})."
            )
        if act3 <= act2:
            raise OptionError(
                f"Act 3 Threshold ({act3}) must be strictly greater than Act 2 Threshold ({act2})."
            )
        if act4 <= act3:
            raise OptionError(
                f"Act 4 Threshold ({act4}) must be strictly greater than Act 3 Threshold ({act3})."
            )

        max_dumpster_items = len(self.item_name_groups["Dumpster Items"])
        if act4 > max_dumpster_items:
            raise OptionError(
                f"Act 4 Threshold ({act4}) cannot be greater than the total pool of "
                f"Dumpster Items ({max_dumpster_items})."
            )

        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            slot_options: dict[str, Any] = slot_data.get("options", {})
            for key, value in slot_options.items():
                opt = getattr(self.options, key, None)
                if opt is not None:
                    setattr(self.options, key, opt.from_any(value))

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.FuniRaccoonItem:
        if name == self.glitches_item_name:
            return items.FuniRaccoonItem(name, ItemClassification.progression, None, self.player)
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "eurosanity":  self.options.eurosanity.value,
            "gemsanity":   self.options.gemsanity.value,
            "hatsanity":   self.options.hatsanity.value,
            "goal":        sorted(self.options.goal.value),
            "current_map": self.origin_region_name,
            "options": {
                **self.options.as_dict("eurosanity", "gemsanity", "hatsanity", "dumpster_weight_blocking", "lugh_quest_locking", "trap_toggle", "museum_threshold", "act2_threshold", "act3_threshold", "act4_threshold", "color_rando"),
                "goal": sorted(self.options.goal.value),
            },
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data