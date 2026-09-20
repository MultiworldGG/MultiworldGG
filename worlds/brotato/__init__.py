import logging
from dataclasses import asdict
from typing import Any, ClassVar

from BaseClasses import Item, MultiWorld, Region, Tutorial
from Options import OptionGroup
from worlds.AutoWorld import WebWorld, World

from . import options  # So we don't need to import every option class when defining option groups
from .characters import get_available_and_starting_characters
from .constants import (
    MAX_SHOP_SLOTS,
    PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE,
    RUN_COMPLETE_LOCATION_TEMPLATE,
)
from .item_weights import create_items_from_weights
from .items import BrotatoItem, ItemName, filler_items, item_name_groups, item_name_to_id, item_table
from .locations import location_name_groups, location_name_to_id
from .loot_crates import (
    BrotatoLootCrateGroup,
    build_loot_crate_groups,
)
from .options import (
    BrotatoOptions,
)
from .regions import create_regions
from .rules import create_has_run_wins_rule
from .shop_slots import get_num_shop_slot_and_lock_button_items
from .wave_caps import get_wave_cap_info
from .waves import get_wave_for_each_item, get_waves_with_checks

logger = logging.getLogger("Brotato")


class BrotatoWeb(WebWorld):
    # TODO: Add actual tutorial!
    tutorials: list[Tutorial] = [  # noqa: RUF012
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Brotato randomizer connected to a MultiworldGG Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["RampagingHippy"],
        )
    ]
    theme = "dirt"
    rich_text_options_doc = True

    option_groups: ClassVar[list[OptionGroup]] = [
        OptionGroup(
            "Loot Crates",
            [
                options.SpawnNormalLootCrates,
                options.NumberCommonCrateDropLocations,
                options.NumberCommonCrateDropsPerCheck,
                options.NumberCommonCrateDropGroups,
                options.NumberLegendaryCrateDropLocations,
                options.NumberLegendaryCrateDropsPerCheck,
                options.NumberLegendaryCrateDropGroups,
            ],
        ),
        OptionGroup(
            "Shop Slots",
            [options.StartingShopSlots, options.StartingShopLockButtonsMode, options.NumberStartingShopLockButtons],
        ),
        OptionGroup(
            "Item Weights",
            [
                options.CommonItemWeight,
                options.UncommonItemWeight,
                options.RareItemWeight,
                options.LegendaryItemWeight,
                options.CommonUpgradeWeight,
                options.UncommonUpgradeWeight,
                options.RareUpgradeWeight,
                options.LegendaryUpgradeWeight,
                options.GoldWeight,
                options.XpWeight,
            ],
        ),
        OptionGroup(
            "Abyssal Terrors DLC",
            [options.EnableAbyssalTerrorsDLC, options.IncludeAbyssalTerrorsCharacters],
        ),
    ]


class BrotatoWorld(World):
    """
    Brotato is a top-down arena shooter roguelite where you play a potato wielding up to
    6 weapons at a time to fight off hordes of aliens. Choose from a variety of traits
    and items to create unique builds and survive until help arrives.
    """

    options_dataclass = BrotatoOptions
    options: BrotatoOptions
    game: ClassVar[str] = "Brotato"
    web = BrotatoWeb()
    data_version = 0
    required_client_version: tuple[int, int, int] = (0, 5, 0)

    item_name_to_id: ClassVar[dict[str, int]] = item_name_to_id
    item_name_groups: ClassVar[dict[str, set[str]]] = item_name_groups

    _filler_items: list[str] = filler_items
    _starting_characters: list[str]
    _include_characters: list[str]
    """The characters whose locations (wave/run complete) may have progression and useful items.

    This is derived from options.include_characters.

    This is a distinct list from the options value because:

    * We want to sanitize the list to make sure typos or other errors don't cause bugs down the road.
    * We want to keep things in character definition order for readability by using a list instead of a set.
    """

    location_name_to_id: ClassVar[dict[str, int]] = location_name_to_id
    location_name_groups: ClassVar[dict[str, set[str]]] = location_name_groups

    num_wins_needed: int
    """The number of runs won needed to achieve the goal.

    This is the minimum of the num_victories option value and the total number of characters available.
    """

    num_shop_slot_items: int
    num_shop_lock_button_items: int

    waves_with_checks: list[int]
    """Which waves will count as locations.

    Calculated from player options in generate_early.
    """

    num_wave_cap_increases: int
    """The number of Progressive Wave Cap items to create."""

    wave_access: dict[int, int]
    """Lookup of waves to the number of wave cap increases needed to access it.

    For example, wave_access[1] has the number of increases needed for wave 1 to be in
    logic.
    """

    common_loot_crate_groups: list[BrotatoLootCrateGroup]
    """Information about each common loot crate group, i.e. how many crates it has and how many wins it needs.

    Calculated from player options in generate_early().
    """

    legendary_loot_crate_groups: list[BrotatoLootCrateGroup]
    """Information about each legendary loot crate group, i.e. how many crates it has and how many wins it needs.

    Calculated from player options in generate_early().
    """

    nonessential_item_counts: dict[ItemName, int]
    """The names and counts of the items in the pool that aren't characters, shop slots, or shop locks.

    This includes the (Brotato) items, upgrades, gold and XP drops, which are populated from the respective weight
    options to fill all locations not taken by the aforementioned items.

    These are "nonessential" because they aren't strictly necessary for completion, like character items, or incredibly
    useful with a strict cap, like the shop slots and locks. There's probably a better name for this, but I can't think
    of it at the time of writing.

    These are determined in generate_early() instead of create_items() so we can use the amount of them to determine
    combat logic.
    """

    def __init__(self, world: MultiWorld, player: int) -> None:
        super().__init__(world, player)

    def create_item(self, name: str | ItemName) -> BrotatoItem:
        if isinstance(name, ItemName):
            name = name.value
        return item_table[self.item_name_to_id[name]].to_item(self.player)

    def generate_early(self) -> None:
        # Determine needed values from the options
        self.waves_with_checks = get_waves_with_checks(self.options.waves_per_drop)
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough:
            self._starting_characters = re_gen_passthrough[self.game]["starting_characters"]
            self._include_characters = re_gen_passthrough[self.game]["include_characters"]
        else:
            self._include_characters, self._starting_characters = get_available_and_starting_characters(
                self.options.include_base_game_characters.value,
                bool(self.options.enable_abyssal_terrors_dlc.value),
                self.options.include_abyssal_terrors_characters.value,
                self.options.starting_characters,
                self.options.num_starting_characters.value,
                self.options.num_characters.value,
                self.random,
            )

        # Clamp the number of wins needed to goal to the number of included characters, so the game isn't unwinnable.
        self.num_wins_needed = min(self.options.num_victories.value, len(self._include_characters))

        self.num_wave_cap_increases, self.wave_access = get_wave_cap_info(self.options.num_wave_caps)

        # Thought: if num victories is clamped, do some of the groups become unreachable?
        self.common_loot_crate_groups = build_loot_crate_groups(
            self.options.num_common_crate_drops.value,
            self.options.num_common_crate_drop_groups.value,
            self.num_wins_needed,
        )
        self.legendary_loot_crate_groups = build_loot_crate_groups(
            self.options.num_legendary_crate_drops.value,
            self.options.num_legendary_crate_drop_groups.value,
            self.num_wins_needed,
        )

        self.num_shop_slot_items, self.num_shop_lock_button_items = get_num_shop_slot_and_lock_button_items(
            self.options.num_starting_shop_slots,
            self.options.shop_lock_buttons_mode,
            self.options.num_starting_lock_buttons,
        )

        # The number of locations available, not including the "Run Won" locations, which always have "Run Won" items.
        num_locations = sum(
            [
                len(self._include_characters),  # Run Won Locations
                len(self._include_characters) * len(self.waves_with_checks),  # Wave Complete Locations
                self.options.num_common_crate_drops.value,
                self.options.num_legendary_crate_drops.value,
            ]
        )

        num_essential_items = sum(
            [
                len(self._include_characters),  # Run Won Items
                len(self._include_characters) - len(self._starting_characters),  # The character items
                self.num_wave_cap_increases * len(self._include_characters),
                self.num_shop_slot_items,
                self.num_shop_lock_button_items,
            ]
        )

        num_nonessential_items = max(num_locations - num_essential_items, 0)
        self.nonessential_item_counts = create_items_from_weights(
            num_nonessential_items,
            self.random,
            self.options.common_item_weight,
            self.options.uncommon_item_weight,
            self.options.rare_item_weight,
            self.options.legendary_item_weight,
            self.options.common_upgrade_weight,
            self.options.uncommon_upgrade_weight,
            self.options.rare_upgrade_weight,
            self.options.legendary_upgrade_weight,
            self.options.gold_weight,
            self.options.xp_weight,
        )

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = create_has_run_wins_rule(self.player, self.num_wins_needed)

    def create_regions(self) -> None:
        def create_region(region_name: str) -> Region:
            return Region(region_name, self.player, self.multiworld)

        regions: list[Region] = create_regions(
            create_region,
            self._include_characters,
            self.waves_with_checks,
            self.wave_access,
            self.common_loot_crate_groups,
            self.legendary_loot_crate_groups,
        )

        self.multiworld.regions.extend(regions)

    def create_items(self) -> None:
        item_pool: list[BrotatoItem | Item] = []

        for character in self._include_characters:
            character_item: BrotatoItem = self.create_item(character)
            if character in self._starting_characters:
                self.multiworld.push_precollected(character_item)
            else:
                item_pool.append(character_item)

            for _ in range(self.num_wave_cap_increases):
                wave_cap_increase_item = self.create_item(
                    name=PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char=character)
                )
                item_pool.append(wave_cap_increase_item)

        # Create an item for each nonessential item. These are determined in generate_early().
        for item_name, item_count in self.nonessential_item_counts.items():
            item_pool += [self.create_item(item_name) for _ in range(item_count)]

        item_pool += [self.create_item(ItemName.SHOP_SLOT) for _ in range(self.num_shop_slot_items)]
        item_pool += [self.create_item(ItemName.SHOP_LOCK_BUTTON) for _ in range(self.num_shop_lock_button_items)]

        self.multiworld.itempool += item_pool

        # Place "Run Won" items at the Run Won locations. Do this before fill happens so
        # plandos can't place items here.
        for character in self._include_characters:
            item: BrotatoItem = self.create_item(ItemName.RUN_COMPLETE)
            run_won_location = RUN_COMPLETE_LOCATION_TEMPLATE.format(char=character)
            self.multiworld.get_location(run_won_location, self.player).place_locked_item(item)

    def pre_fill(self) -> None:
        pass

    def get_filler_item_name(self) -> str:
        return self.random.choice(self._filler_items)

    def fill_slot_data(self) -> dict[str, Any]:
        # Define outside dict for readability
        spawn_normal_loot_crates: bool = (
            self.options.spawn_normal_loot_crates.value == self.options.spawn_normal_loot_crates.option_true
        )
        wave_per_game_item: dict[int, list[int]] = get_wave_for_each_item(self.nonessential_item_counts)
        return {
            "deathlink": self.options.death_link.value,
            "waves_with_checks": self.waves_with_checks,
            "wave_access": self.wave_access,
            "num_wins_needed": self.num_wins_needed,
            "gold_reward_mode": self.options.gold_reward_mode.value,
            "xp_reward_mode": self.options.xp_reward_mode.value,
            "enable_enemy_xp": self.options.enable_enemy_xp.value == self.options.enable_enemy_xp.option_true,
            "num_starting_shop_slots": self.options.num_starting_shop_slots.value,
            "num_starting_shop_lock_buttons": (MAX_SHOP_SLOTS - self.num_shop_lock_button_items),
            "spawn_normal_loot_crates": spawn_normal_loot_crates,
            "num_common_crate_locations": self.options.num_common_crate_drops.value,
            "num_common_crate_drops_per_check": self.options.num_common_crate_drops_per_check.value,
            "common_crate_drop_groups": [asdict(g) for g in self.common_loot_crate_groups],
            "num_legendary_crate_locations": self.options.num_legendary_crate_drops.value,
            "num_legendary_crate_drops_per_check": self.options.num_legendary_crate_drops_per_check.value,
            "legendary_crate_drop_groups": [asdict(g) for g in self.legendary_loot_crate_groups],
            "wave_per_game_item": wave_per_game_item,
            "enable_abyssal_terrors_dlc": self.options.enable_abyssal_terrors_dlc.value,
            # Info for Universal Tracker, the mod doesn't use these.
            "starting_characters": self._starting_characters,
            "include_characters": self._include_characters,
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any] | None:
        if "starting_characters" in slot_data:
            # If this key is present, all UT-related keys should be present
            return {
                "starting_characters": slot_data["starting_characters"],
                "include_characters": slot_data["include_characters"],
            }
        # Backwards compat with worlds generated before UT support was added
        return None
