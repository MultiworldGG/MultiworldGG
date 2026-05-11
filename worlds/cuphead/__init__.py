### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Collection
from typing import Any, ClassVar, TextIO

from typing_extensions import override

from BaseClasses import CollectionState, Item, ItemClassification, MultiWorld, Tutorial
from Options import Option, PerGameCommonOptions
from rule_builder.cached_world import CachedRuleBuilderWorld
from worlds.AutoWorld import WebWorld

from . import debug as dbg
from . import varis
from .fver import FVersion
from .world import items, levels, locations, options, regions, slotdata
from .world.enums import WeaponMode
from .world.items import itemdefs as idef
from .world.items import itemgroups, weapons
from .world.items.itembase import ItemData
from .world.levels.levelbase import LevelData
from .world.levels.levelids import level_ids
from .world.locations import locationdefs as ld
from .world.locations.locationbase import LocationData
from .world.names import itemnames, regionnames
from .world.options import CupheadOptions, presets
from .world.options import optionbits as obits
from .world.options import optionresolver as oresolver
from .world.options.optionsanitizer import OptionSanitizer
from .world.rules import rules
from .world.rules.rulereg import RuleReg
from .world.settings import CupheadSettings
from .world.shop import ShopData


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
    tutorials = [setup_en]  # noqa: RUF012
    option_groups = options.cuphead_option_groups
    options_presets = presets.option_presets

class CupheadWorld(CachedRuleBuilderWorld):
    """
    A classic run and gun action game heavily focused on boss battles
    """

    GAME_NAME: ClassVar[str] = "Cuphead"

    APWORLD_SEM_VERSION: ClassVar[tuple[int, int, int, int]] = (0, 2, 2, 1)
    APWORLD_VERSION_POSTFIX: str = ""
    APWORLD_VERSION_POSTFIX_NO: int = 0
    APWORLD_VERSION: ClassVar[str] = str(FVersion.from_int_tuple(APWORLD_SEM_VERSION, APWORLD_VERSION_POSTFIX))

    AUTHORS: ClassVar[list[str]] = ["JKLeckr"]

    SLOT_DATA_VERSION: ClassVar[int] = 6

    game: ClassVar[str] = GAME_NAME # type: ignore
    web: ClassVar[WebWorld] = CupheadWebWorld()
    options_dataclass: ClassVar[type[PerGameCommonOptions]] = CupheadOptions
    options: CupheadOptions # type: ignore
    origin_region_name: str = "Start"

    required_client_version: tuple[int, int, int] = (0, 6, 7)
    required_server_version: tuple[int, int, int] = (0, 6, 7)

    item_name_to_id: ClassVar[dict[str, int]] = idef.name_to_id
    location_name_to_id: ClassVar[dict[str, int]] = ld.name_to_id

    item_name_groups: ClassVar[dict[str, set[str]]] = itemgroups.item_groups

    item_names: ClassVar[set[str]] = set(idef.items_all.keys())
    location_names: ClassVar[set[str]] = set(ld.locations_all.keys())

    settings: CupheadSettings # type: ignore

    item_mapping: ClassVar[dict[str, str]] = {
        itemnames.item_coin2: itemnames.item_coin,
        itemnames.item_coin3: itemnames.item_coin,
    }

    precollected_counts: dict[str, int]

    active_items: dict[str, ItemData]
    active_locations: dict[str, LocationData]
    active_levels: dict[str, LevelData]

    resolved_start_weapon_index: int

    weapon_dict: dict[int, str]
    weapon_ex_dict: dict[int, str]

    level_map: dict[int, int]
    rlevel_map: dict[int, int]

    rulereg: RuleReg

    fake_gen: bool = False
    ut_can_gen_without_yaml: ClassVar[bool] = True

    def __init__(self, multiworld: MultiWorld, player: int):
        varis.game_name = self.__class__.GAME_NAME
        super().__init__(multiworld, player)

    def _resolve_test_overrides(self):
        if self.options.test_overrides.value.get("sani"):
            self._osani_ovrr = True
        if _ut := self.options.test_overrides.value.get("ut"):
            if (
                isinstance(_ut, dict) and
                self.GAME_NAME in _ut and
                isinstance(_ut[self.GAME_NAME], dict)
            ):
                self.multiworld.re_gen_passthrough = _ut  # pyright: ignore[reportAttributeAccessIssue]
                self.multiworld.generation_is_fake = True  # pyright: ignore[reportAttributeAccessIssue]

    def set_early_items(self):
        if self.options.early_parry.bvalue:
            self.multiworld.early_items[self.player][itemnames.item_ability_parry] = 1

    def count_precollected(self):
        self.precollected_counts = {}

        for item in self.multiworld.precollected_items[self.player]:
            if item.name not in self.precollected_counts:
                self.precollected_counts[item.name] = 1
                continue
            self.precollected_counts[item.name] += 1

    def resolve_start_weapon(self):
        if not self.options.start_weapon.is_none():
            self.resolved_start_weapon_index = self.options.start_weapon.value
            return

        _start_weapon: int | None = None
        _weapons = set(self.weapon_dict.values())
        for pitem in self.precollected_counts:
            if pitem in _weapons:
                _start_weapon = weapons.all_weapon_to_index[pitem]
                break
        if _start_weapon is None:
            _start_weapon = self.random.choice(tuple(self.weapon_dict.keys()))

        self.resolved_start_weapon_index = _start_weapon

    def solo_setup(self):
        # Put items in early to prevent fill errors. TODO: Make this more elegant.
        no_weapons = self.options.start_weapon.is_none()
        if self.options.randomize_abilities.value:
            self.multiworld.early_items[self.player][itemnames.item_ability_parry] = 1
            self.multiworld.early_items[self.player][itemnames.item_ability_dash] = 1
        if (self.options.weapon_mode.value & WeaponMode.PROGRESSIVE) > 0:
            _start_weapon = weapons.weapon_p_dict[self.resolved_start_weapon_index]
            self.multiworld.early_items[self.player][_start_weapon] = 2 if no_weapons else 1
        elif no_weapons:
            _start_weapon = weapons.weapon_dict[self.resolved_start_weapon_index]
            self.multiworld.early_items[self.player][_start_weapon] = 1
        if (
            (self.options.weapon_mode.value & WeaponMode.EX_SEPARATE) > 0 and
            not self.options.randomize_abilities.bvalue
        ):
            _weapon = self.random.choice(weapons.weapon_ex_dict)
            self.multiworld.early_items[self.player][_weapon] = 1

    def re_gen_setup(self):
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            _slot_data_options = slotdata.get_slot_data_options()
            for okey in _slot_data_options:
                opt: Option[Any] | None = getattr(self.options, okey, None)
                if opt is not None:
                    opt.value = opt.from_any(slot_data[okey]).value
                else:
                    print(f"re_gen_setup: WARNING: {okey} is not registered!")

            bits: int = slot_data["gen_bits"]

            self.options.shop_mode.value = slot_data["shop_mode"]
            _contract_reqs = slot_data["contract_requirements"]
            if not isinstance(_contract_reqs, Collection) or len(_contract_reqs) != 3:  # type: ignore
                raise ValueError(f"re_gen: contract_requirements are malformed. v: {_contract_reqs}")
            (self.options.contract_requirements.value,
                self.options.contract_requirements_isle2.value,
                self.options.contract_requirements_isle3.value) = _contract_reqs
            self.options.dlc_ingredient_requirements.value = slot_data["dlc_ingredient_requirements"]

            obits.debitify(self.options, bits)

            # Keys for level_map in slot data are strings, so convert them to ints
            self.level_map = {int(k): v for k, v in slot_data["level_map"].items()}
            self.shop = ShopData(slot_data["shop_map"])
            self.resolved_start_weapon_index = slot_data["resolved_start_weapon"]

    @override
    def generate_early(self):
        if varis.testing:
            self._resolve_test_overrides()

        self.fake_gen = getattr(self.multiworld, "generation_is_fake", False)

        self.options.version.value = self.APWORLD_VERSION

        if self.fake_gen:
            self.re_gen_setup()

        oresolver.resolve_random_options(self.options, self.random)
        oresolver.resolve_dependent_options(self)

        self.option_sanitizer = OptionSanitizer(
            self.player,
            self.player_name,
            self.options,
            self.random,
            self.multiworld.players < 2,
            not varis.testing or hasattr(self, "_osani_ovrr")
        )

        self.option_sanitizer.sanitize_options()

        self.gen_bits = obits.bitify(self.options)

        self.topology_present = not self.options.freemove_isles.bvalue

        self.count_precollected()

        self.use_dlc = self.options.use_dlc.bvalue
        self.start_weapon = self.options.start_weapon.value

        self.weapon_dict = weapons.get_weapon_dict(self.options)
        self.weapon_ex_dict = weapons.get_weapon_ex_dict(self.options)

        if not self.fake_gen:
            #print(self.level_map)
            self.level_map = levels.setup_level_map(self.options)
            self.shop = ShopData.create_from_options(self.options)
            self.resolve_start_weapon()

        self.rlevel_map = {v: k for k, v in self.level_map.items()}

        coin_amounts = self.options.coin_amounts.value
        self.total_coins = coin_amounts[0] + (coin_amounts[1]*2) + (coin_amounts[2]*3)

        self.active_items = items.setup_items(self)
        self.active_locations = locations.setup_locations(self.options)
        self.active_levels = levels.setup_levels(self.settings, self.options, self.active_locations)

        self.rulereg = RuleReg(self)

        self.set_early_items()

        # Solo World Setup (for loners)
        if self.multiworld.players<2:
            self.solo_setup()

        if self.settings.is_debug_bit_on(64):
            print(f"options: {self.options.dump()}")

    @override
    def fill_slot_data(self) -> dict[str, Any]:
        return slotdata.fill_slot_data(self)

    @override
    def create_regions(self):
        regions.create_regions(self)
        #print(self.multiworld.get_locations(self.player))
        #print(regions.list_multiworld_regions_names(self.multiworld))
        #print(self.multiworld.get_region(regionnames.level_mausoleum_ii, self.player).locations)
        #dbg.debug_visualize_regions(self, True)

    @override
    def create_item(self, name: str, force_classification: ItemClassification | None = None) -> Item:
        return items.create_item(name, self.player, force_classification)

    @override
    def create_items(self):
        items.create_items(self)

    @override
    def write_spoiler(self, spoiler_handle: TextIO):
        if len(self.option_sanitizer.option_overrides)>0:
            spoiler_handle.write(f"\n{self.player_name} Option Changes:\n\n")
            spoiler_handle.write("\n".join(list(self.option_sanitizer.option_overrides)) + "\n")
        if len(self.level_map)>0:
            spoiler_handle.write(f"\n{self.player_name} Level Shuffle Map:\n\n")
            spoiler_handle.write(
                "\n".join([f"{level_ids[x]} -> {level_ids[y]}" for x, y in self.level_map.items()]) + "\n"
            )

        def _gen_shop_list(y: list[str]) -> str:
            return "\n".join([f" {z}" for z in y])

        spoiler_handle.write(f"\n{self.player_name} Shop Items:\n\n")
        spoiler_handle.write("\n".join([
            f"{x}:\n{_gen_shop_list(y)}" for x, y in self.shop.shop_locations.items() \
                if (x != regionnames.shop_set4 or self.use_dlc)
        ]))

    @override
    def collect(self, state: CollectionState, item: Item) -> bool:
        #print(item.name)
        changed = super().collect(state, item)
        if changed and item.name.endswith(" Coins", 1):
            amount = int(item.name[0])
            if amount == 2 or amount == 3:
                state.add_item(itemnames.item_coin, self.player, amount)
        return changed

    @override
    def remove(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if changed and item.name.endswith(" Coins", 1):
            amount = int(item.name[0])
            if amount == 2 or amount == 3:
                state.remove_item(itemnames.item_coin, self.player, amount)
        return changed

    @override
    def get_filler_item_name(self) -> str:
        return items.get_filler_item_name(self)

    @override
    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        hint_dict: dict[int, str] = {}
        if self.level_map:
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
            if shopl != regionnames.shop_set4 or self.use_dlc:
                for loc in locs:
                    hint_dict[self.location_name_to_id[loc]] = shopl
        hint_data.update({self.player: hint_dict})

    @override
    def set_rules(self):
        rules.set_rules(self)

    @override
    def post_fill(self):
        #debug.print_locations(self)
        if self.settings.is_debug_bit_on(4):
            dbg.debug_visualize_regions(self, self.settings.is_debug_bit_on(8))
        if self.fake_gen and self.settings.is_debug_bit_on(512):
            #dbg.debug_print_regions(self)
            dbg.debug_visualize_regions(self, True, "UT")

        return super().post_fill()

    def get_start_locations(self) -> list[str]:
        _region = self.multiworld.get_region("Start", self.player)
        return [s.name for s in _region.locations]

    # For Universal Tracker
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        if "version" not in slot_data:
            raise KeyError("'version' is missing from slot data!")
        if "world_version" not in slot_data:
            raise KeyError("'world_version' is missing from slot data!\nIncompatible APWorld!")
        _version = slot_data["version"]
        if _version != CupheadWorld.SLOT_DATA_VERSION:
            raise ValueError(f"Slot data version mismatch. {_version}!={CupheadWorld.SLOT_DATA_VERSION}")

        _world_version = slot_data["world_version"]

        print(f"SlotData version: {_version}")
        print(f"Server APWorld Version: {_world_version}")
        print(f"This APWorld Version: {CupheadWorld.APWORLD_VERSION}")

        if _world_version != CupheadWorld.APWORLD_VERSION:
            print(
                "WARNING: Server version is different than client version. "
                "Logic may be different in tracker compared to actual logic in server."
            )

        return slot_data
