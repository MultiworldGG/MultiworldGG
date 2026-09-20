from collections.abc import Mapping
from typing import Any

from BaseClasses import ItemClassification
from worlds.AutoWorld import World
from Options import OptionError

from . import items, locations, regions, rules, web_world
from . import options as UncannyCat_options

class UncannyCatWorld(World):
    """
    Uncanny Cat Golf is a game about shooting a cat into various golf holes, with hijinx aplenty
    """
    
    game = "Uncanny Cat Golf"
    web = web_world.UncannyCatWebWorld()

    options_dataclass = UncannyCat_options.UncannyCatOptions
    options: UncannyCat_options.UncannyCatOptions 

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID
    item_name_groups = items.ITEM_GROUPS

    origin_region_name = "Menu"

    ut_can_gen_without_yaml = True
    glitches_item_name: str = "out_of_logic"
        
    def generate_early(self) -> None:
        # A goal level in World 5 or World P forces that world's levels on
        goal = items.GOAL_LEVEL[self.options.goal_level.value]
        goal_world = items.world_prefix(goal)
        if goal_world == "5":
            self.options.world_5_levels.value = 1
        elif goal_world == "P":
            self.options.world_p_levels.value = 1

        if not rules.seed_levels(self):
            raise OptionError(
                f"Uncanny Cat Golf ({self.player_name}) has no levels left to play. "
                f"Leave at least one level out of Excluded Levels, or enable more worlds."
            )

        # Ensure prism count always works.
        self.options.prism_unlock_amount.value = min(
            self.options.prism_unlock_amount.value, rules.max_obtainable_prisms(self)
        )

        # Only as many macguffins as there are open locations for them
        if self.options.macguffin_goal:
            open_locations = items.get_open_location_count(self)
            if open_locations < 1:
                raise OptionError(
                    f"Uncanny Cat Golf ({self.player_name}) has no room for any Cannium Prisms for the macguffin goal. "
                    f"Enable more worlds or checks, or exclude fewer levels."
                )
            self.options.macguffin_amount.value = min(self.options.macguffin_amount.value, open_locations)

        # Chill Mode forces panic mode off
        if self.options.chill_mode:
            self.options.panic_mode.value = 0
            
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            for key, value in slot_data.items():
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

    def create_item(self, name: str) -> items.UncannyCatItem:
        if name == self.glitches_item_name:
            return items.UncannyCatItem(name, ItemClassification.progression, None, self.player)
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "goal_level": self.options.goal_level.value,
            "prism_unlock_amount": self.options.prism_unlock_amount.value,
            "macguffin_goal": self.options.macguffin_goal.value,
            "macguffin_amount": self.options.macguffin_amount.value,
            "macguffin_percent_required": self.options.macguffin_percent_required.value,
            "macguffin_required": items.get_macguffins_required(self),
            "gimmick_lock": self.options.gimmick_lock.value,
            "level_unlock_style": self.options.level_unlock_style.value,
            "minigames": self.options.minigames.value,
            "world_5_levels": self.options.world_5_levels.value,
            "world_p_levels": self.options.world_p_levels.value,
            "world_e_levels": self.options.world_e_levels.value,
            "peak_checks": self.options.peak_checks.value,
            "coinsanity": self.options.coinsanity.value,
            "excluded_levels": sorted(self.options.excluded_levels.value),
            "excluded_minigames": sorted(self.options.excluded_minigames.value),
            "rank_check_difficulty": self.options.rank_check_difficulty.value,
            "temp_modifiers": self.options.temp_modifiers.value,
            "chill_mode": self.options.chill_mode.value,
            "panic_mode": self.options.panic_mode.value,
            "death_link": self.options.death_link.value,
            "death_link_amnesty": self.options.death_link_amnesty.value,
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data