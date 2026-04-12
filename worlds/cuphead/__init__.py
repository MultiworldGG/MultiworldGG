from __future__ import annotations
from typing import TextIO, Any
from typing_extensions import override
from BaseClasses import Item, Tutorial, ItemClassification, CollectionState
from worlds.AutoWorld import World, WebWorld
from .rules import rules
from .names import ItemNames, LocationNames
from .options import CupheadOptions, presets
from .options.optionsanitizer import OptionSanitizer
from .enums import WeaponMode
from .wconf import WorldConfig
from .settings import CupheadSettings
from .items import itemgroups, weapons, itemcreate, itemdefs as idef
from .items.itembase import ItemData
from .locations import locationdefs as ld
from .locations.locationbase import LocationData
from .levels.levelids import level_ids
from .levels.levelbase import LevelData
from .shop import ShopData
from . import options, locations, levels, regions, items, shop, slotdata
from . import debug as dbg

class CupheadWebWorld(WebWorld):
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Cuphead MultiworldGG randomizer on your machine",
        "English",
        "setup_en.md",
        "setup/en",
        ["JKLeckr"]
    )
    tutorials = [setup_en]
    option_groups = options.cuphead_option_groups
    options_presets = presets.option_presets

class CupheadWorld(World):
    """
    A classic run and gun action game heavily focused on boss battles
    """

    GAME_NAME: str = "Cuphead"
    APWORLD_VERSION: str = "alpha02i"

    SLOT_DATA_VERSION: int = 4

    WCONFIG_DEFAULT: WorldConfig = WorldConfig()

    game: str = GAME_NAME # type: ignore
    author: str = "JKL"
    web = CupheadWebWorld()
    options_dataclass = CupheadOptions
    options: CupheadOptions # type: ignore
    version: str = APWORLD_VERSION
    origin_region_name: str = "Start"

    required_client_version: tuple[int, int, int] = (0, 6, 0)
    required_server_version: tuple[int, int, int] = (0, 6, 0)

    item_name_to_id = idef.name_to_id
    location_name_to_id = ld.name_to_id

    item_name_groups = itemgroups.item_groups

    item_names = set(idef.items_all.keys())
    location_names = set(ld.locations_all.keys())

    settings: CupheadSettings # type: ignore

    wconfig: WorldConfig

    active_items: dict[str, ItemData]
    active_locations: dict[str, LocationData]

    level_map: dict[int, int] = {}

    def solo_setup(self) -> None:
        # Put items in early to prevent fill errors. TODO: Make this more elegant.
        if self.wconfig.randomize_abilities:
            self.multiworld.early_items[self.player][ItemNames.item_ability_parry] = 1
            self.multiworld.early_items[self.player][ItemNames.item_ability_dash] = 1
        if (self.wconfig.weapon_mode & WeaponMode.PROGRESSIVE) > 0:
            _start_weapon = weapons.weapon_p_dict[self.start_weapon]
            self.multiworld.early_items[self.player][_start_weapon] = 1
        if (self.wconfig.weapon_mode & WeaponMode.EX_SEPARATE) > 0:
            _weapon = self.random.choice(weapons.weapon_ex_dict)
            self.multiworld.early_items[self.player][_weapon] = 1

    @override
    def generate_early(self) -> None:
        self.options.version.value = self.version

        self.option_sanitizer = OptionSanitizer(self.player, self.options, self.random)

        options.resolve_dependent_options(self.options)
        options.resolve_random_options(self.options, self.random)

        self.option_sanitizer.sanitize_options()

        # World Config (See wconfig.py)
        self.wconfig = WorldConfig(self.options)

        self.topology_present = not self.wconfig.freemove_isles

        self.use_dlc = self.wconfig.use_dlc
        self.start_weapon = self.wconfig.start_weapon
        self.level_shuffle = self.wconfig.level_shuffle

        coin_amounts = self.wconfig.coin_amounts
        self.total_coins = coin_amounts[0] + (coin_amounts[1]*2) + (coin_amounts[2]*3)

        self.active_items: dict[str,ItemData] = items.setup_items(self.wconfig)
        self.active_locations: dict[str,LocationData] = locations.setup_locations(self.wconfig)
        self.active_levels: dict[str,LevelData] = levels.setup_levels(self.wconfig,self.active_locations)

        if len(self.level_map) < 1:
            self.level_map = levels.setup_level_map(self.wconfig)

        self.shop: ShopData = shop.setup_shop_data(self.wconfig)

        self.contract_requirements: tuple[int,int,int] = self.wconfig.contract_requirements
        self.dlc_ingredient_requirements: int = self.wconfig.dlc_ingredient_requirements

        # Solo World Setup (for loners)
        if self.multiworld.players<2:
            self.solo_setup()

    @override
    def fill_slot_data(self) -> dict[str, Any]:
        return slotdata.fill_slot_data(self)

    @override
    def create_regions(self) -> None:
        regions.create_regions(self)
        #print(self.multiworld.get_locations(self.player))
        #print(regions.list_multiworld_regions_names(self.multiworld))
        #print(self.multiworld.get_region(LocationNames.level_mausoleum_ii, self.player).locations)

    @override
    def create_item(self, name: str, force_classification: ItemClassification | None = None) -> Item:
        return items.create_item(name, self.player, force_classification)

    @override
    def create_items(self) -> None:
        items.create_items(self)

    @override
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if len(self.option_sanitizer.option_overrides)>0:
            spoiler_handle.write(f"\n{self.player_name} Option Changes:\n\n")
            spoiler_handle.write('\n'.join([x for x in self.option_sanitizer.option_overrides]) + '\n')
        if len(self.level_map)>0:
            spoiler_handle.write(f"\n{self.player_name} Level Shuffle Map:\n\n")
            spoiler_handle.write(
                '\n'.join([f"{level_ids[x]} -> {level_ids[y]}" for x, y in self.level_map.items()]) + '\n'
            )

        def _gen_shop_list(y: list[str]) -> str:
            return "\n".join([f" {z}" for z in y])

        spoiler_handle.write(f"\n{self.player_name} Shop Items:\n\n")
        spoiler_handle.write("\n".join([
            f"{x}:\n{_gen_shop_list(y)}" for x, y in self.shop.shop_locations.items() \
                if (x != LocationNames.shop_set4 or self.use_dlc)
        ]))

    @override
    def collect(self, state: CollectionState, item: Item) -> bool:
        #print(item.name)
        if item.name in (ItemNames.item_coin2, ItemNames.item_coin3):
            amount = 3 if item.name == ItemNames.item_coin3 else 2
            _name = self.collect_item(
                state,
                itemcreate.create_item(ItemNames.item_coin, self.player)
            )
            if _name:
                state.add_item(_name, self.player, amount)
                return True
            return False
        elif (self.wconfig.weapon_mode & WeaponMode.PROGRESSIVE) > 0 and item.name in weapons.weapon_dict.values():
            _name = self.collect_item(
                state,
                itemcreate.create_active_item(weapons.weapon_p_dict[weapons.weapon_to_index[item.name]], self),
            )
            if _name:
                state.add_item(_name, self.player, 2)
                return True
            return False
        else:
            return super().collect(state, item)

    @override
    def remove(self, state: CollectionState, item: Item) -> bool:
        if item.name in (ItemNames.item_coin2, ItemNames.item_coin3):
            amount = 3 if item.name == ItemNames.item_coin3 else 2
            _name = self.collect_item(
                state,
                itemcreate.create_item(ItemNames.item_coin, self.player),
                True
            )
            if _name:
                state.remove_item(_name, self.player, amount)
                return True
            return False
        elif (self.wconfig.weapon_mode & WeaponMode.PROGRESSIVE) > 0 and item.name in weapons.weapon_dict.values():
            _name = self.collect_item(
                state,
                itemcreate.create_active_item(weapons.weapon_p_dict[weapons.weapon_to_index[item.name]], self),
                True
            )
            if _name:
                state.remove_item(_name, self.player, 2)
                return True
            return False
        else:
            return super().remove(state, item)

    @override
    def get_filler_item_name(self) -> str:
        return items.get_filler_item_name(self)

    @override
    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        hint_dict: dict[int, str] = {}
        if len(self.level_map)>0:
            for level, lmap in self.level_map.items():
                if (
                    level_ids[level] in self.active_levels and
                    level_ids[lmap] in self.active_levels and
                    level != lmap
                ):
                    for loc in self.active_levels[level_ids[lmap]].locations:
                        if loc in self.active_locations and loc in self.location_name_to_id:
                            hint_dict[self.location_name_to_id[loc]] = level_ids[level]
                            if self.settings.is_debug_bit_on(16):
                                print(f"Hint: {loc} -> {level_ids[level]}")
                        #else:
                        #    print(f"{loc} not valid for shuffle hint.")
        for shopl, locs in self.shop.shop_locations.items():
            if shopl != LocationNames.shop_set4 or self.use_dlc:
                for loc in locs:
                    hint_dict[self.location_name_to_id[loc]] = shopl
        hint_data.update({self.player: hint_dict})

    @override
    def set_rules(self) -> None:
        rules.set_rules(self)

    @override
    def post_fill(self) -> None:
        #debug.print_locations(self)
        if self.settings.is_debug_bit_on(4):
            dbg.debug_visualize_regions(self, self.settings.is_debug_bit_on(8))
        return super().post_fill()

    def get_start_locations(self) -> list[str]:
        _region = self.multiworld.get_region("Start", self.player)
        return [s.name for s in _region.locations]

    @override
    def __getattr__(self, item: str) -> Any:
        if item == "wconfig":
            return self.__class__.WCONFIG_DEFAULT
        return super().__getattr__(item)

    # For Universal Tracker
    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        slotdata.interpret_slot_data(self, slot_data)
        #dbg.debug_print_regions(self)
        if self.settings.is_debug_bit_on(256):
            dbg.debug_visualize_regions(self, True, "UT")
