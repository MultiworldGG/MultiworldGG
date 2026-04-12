from collections import defaultdict
from typing import Any, Iterable, List, Mapping

from BaseClasses import (Item, ItemClassification, Location,
                         LocationProgressType, Region, Tutorial)
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule, add_rule, set_rule

from .enums import DLC, APItemType, DS2Version, ItemCategory
from .options import DarkSouls2Options, option_groups
from .locations import LocationData, locations_by_region, regions_by_location, locations_to_keep_unrandomized, location_name_groups
from .items import ItemData, item_dictionary, item_list, item_name_groups
from .regions import region_dictionary, region_list
from .rules import connection_rules, location_rules, combat_logic_easy, combat_logic_medium, combat_logic_hard


class DS2Location(Location):
    game: str = "Dark Souls II"
    data: LocationData

    def __init__(self, player, name, address, parent, data):
        self.data = data
        super(DS2Location, self).__init__(
            player, name, address, parent
        )


class DS2Item(Item):
    game: str = "Dark Souls II"
    data: ItemData

    def __init__(self, name, classification, code, player, data):
        self.data = data
        super(DS2Item, self).__init__(
            name, classification, code, player
        )


class DarkSouls2Web(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the MultiworldGG Dark Souls II randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["WildBunnie"]
    )
    # setup_pt = Tutorial()  # TODO

    options_page = True  # TODO look into this
    game_info_languages = ['en']  # , 'pt']
    tutorials = [setup_en]
    theme = "ice"
    bug_report_page = "https://github.com/WildBunnie/DarkSoulsII-Archipelago/issues"
    options_presets = {}  # TODO
    option_groups = option_groups
    rich_text_options_doc = True
    location_descriptions = {}  # TODO
    item_descriptions = {}  # TODO


class DarkSouls2World(World):
    """
    Dark Souls II is a 2014 action role-playing game and the second installment of the Dark Souls series.
    It is set in the kingdom of Drangleic and follows an undead traveler searching for a cure to their affliction.
    """
    game = "Dark Souls II"

    web = DarkSouls2Web()

    options_dataclass = DarkSouls2Options
    options: DarkSouls2Options

    item_name_to_id = {
        item_data.name: item_data.code
        for item_data in item_list
        if not item_data.exclude
    }

    location_name_to_id = {
        location_data.name: location_data.address
        for locations in locations_by_region.values()
        for location_data in locations
        if location_data.address != None
    }

    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def _is_dlc_enabled(self, dlc: DLC) -> bool:
        if dlc == DLC.SUNKEN_KING and not self.options.sunken_king_dlc:
            return False
        if dlc == DLC.OLD_IRON_KING and not self.options.old_iron_king_dlc:
            return False
        if dlc == DLC.IVORY_KING and not self.options.ivory_king_dlc:
            return False
        return True

    def _is_version_selected(self, version: DS2Version) -> bool:
        if version == DS2Version.SOTFS and self.options.game_version != "sotfs":
            return False
        if version == DS2Version.VANILLA and self.options.game_version != "vanilla":
            return False
        return True

    def generate_early(self) -> None:
        if self.options.early_blacksmith == "early_global":
            self.multiworld.early_items[self.player]["Lenigrast's Key"] = 1
        elif self.options.early_blacksmith == "early_local":
            self.multiworld.local_early_items[self.player]["Lenigrast's Key"] = 1

    def create_regions(self) -> None:
        region_lookup: dict[str, Region] = {}

        # create regions and locations
        for region_data in region_list:
            if not self._is_dlc_enabled(region_data.dlc):
                continue
            region = Region(region_data.name, self.player, self.multiworld)

            for location_data in locations_by_region[region_data.name]:
                if not self._is_version_selected(location_data.version):
                    continue
                # TODO check if user chose to remove this

                if location_data.is_event:
                    region.add_event(location_data.name)
                    continue

                location = DS2Location(
                    self.player,
                    location_data.name,
                    location_data.address,
                    region,
                    location_data,
                )

                if location_data.missable:
                    location.progress_type = LocationProgressType.EXCLUDED
                region.locations.append(location)

            self.multiworld.regions.append(region)
            region_lookup[region_data.name] = region

        # setup connections
        for region_data in region_list:
            if region_data.name not in region_lookup:
                continue
            region = region_lookup[region_data.name]
            for connection in region_data.connections:
                if connection not in region_lookup:
                    continue
                region.connect(region_lookup[connection])

        # TODO more win conditions
        victory_region = region_lookup["Throne of Want"]
        victory_loc = Location(
            self.player, "Defeat Nashandra", None, victory_region)
        victory_region.locations.append(victory_loc)

        victory_loc.place_locked_item(Item("Victory", ItemClassification.progression, None, self.player))
        set_rule(victory_loc, lambda state: state.can_reach_location("ThroneOfWant: Soul of Nashandra", self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    # i don't love how this is done but i cannot come up with something better
    # TODO maybe dont allow dlc items
    def create_items(self) -> None:
        item_pool: List[DS2Item] = []
        items_added: List[str] = []

        locations_to_fill: List[DS2Location] = self.multiworld.get_unfilled_locations(self.player)
        max_pool_size = len(locations_to_fill)

        # Add original items from locations
        for location in locations_to_fill:
            item_data = item_dictionary[location.data.original_item_name]

            if location.data.keep_original_item:
                location.place_locked_item(self.create_item(location.data.original_item_name))
                items_added.append(location.data.original_item_name)
                max_pool_size -= 1
                continue

            if item_data.skip or item_data.exclude:
                continue

            if item_data.category == ItemCategory.UNIQUE and item_data.name in items_added:
                continue

            items_added.append(item_data.name)
            item_pool.append(self.create_item(item_data.name))

        # Add missing progression items

        # We do this now instead of before the previous step because
        # if we did it before we would get two of any progression item
        # that isn't unique, which is not something we really want
        missing_progression_items = [
            item.name for item in item_list
            if item.name not in items_added
            and item.classification == ItemClassification.progression
        ]

        assert len(item_pool) + len(missing_progression_items) <= max_pool_size, "Item pool cannot fit all dark souls 2 progression items"

        for progression_item in missing_progression_items:
            item_pool.append(self.create_item(progression_item))

        # Fill remaining slots with filler items
        for _ in range(max_pool_size - len(item_pool)):
            item_pool.append(self.create_item(self.get_filler_item_name()))

        assert len(item_pool) == max_pool_size

        self.multiworld.itempool.extend(item_pool)

    def set_rules(self) -> None:
        locations: Iterable[DS2Location] = self.multiworld.get_locations(self.player)
        for location in locations:
            if location.address != None and location.data.is_shop:
                add_item_rule(location, lambda item:
                              (item.player != self.player or
                               item.data.bundle == False))

        for connection_rule_data in connection_rules:
            _from, _to = connection_rule_data.spot.split(" -> ")
            from_region = region_dictionary[_from]
            to_region = region_dictionary[_to]

            if not self._is_dlc_enabled(from_region.dlc):
                continue
            if not self._is_dlc_enabled(to_region.dlc):
                continue
            if not self._is_version_selected(connection_rule_data.version):
                continue

            add_rule(
                self.multiworld.get_entrance(connection_rule_data.spot, self.player),
                connection_rule_data.to_collection_rule(self.player)
            )

        for location_rule_data in location_rules:
            region_name = regions_by_location[location_rule_data.spot]
            region_data = region_dictionary[region_name]

            if not self._is_dlc_enabled(region_data.dlc):
                continue
            if not self._is_version_selected(location_rule_data.version):
                continue

            add_rule(
                self.multiworld.get_location(location_rule_data.spot, self.player),
                location_rule_data.to_collection_rule(self.player)
            )

        combat_rules = []
        if self.options.combat_logic == "easy":
            combat_rules = combat_logic_easy
        elif self.options.combat_logic == "medium":
            combat_rules = combat_logic_medium
        elif self.options.combat_logic == "hard":
            combat_rules = combat_logic_hard
        
        # TODO dont duplicate this code
        if combat_rules:
            for combat_rule_data in combat_rules:
                _from, _to = combat_rule_data.spot.split(" -> ")
                from_region = region_dictionary[_from]
                to_region = region_dictionary[_to]

                if not self._is_dlc_enabled(from_region.dlc):
                    continue
                if not self._is_dlc_enabled(to_region.dlc):
                    continue
                if not self._is_version_selected(combat_rule_data.version):
                    continue

                add_rule(
                    self.multiworld.get_entrance(combat_rule_data.spot, self.player),
                    combat_rule_data.to_collection_rule(self.player)
                )


    def create_item(self, name: str) -> DS2Item:
        item_data: ItemData = item_dictionary[name]

        if item_data.max_reinforcement > 0 and self.random.randint(0, 99) < self.options.randomize_equipment_level_percentage:
            if item_data.max_reinforcement == 5:
                min_reinforcement = self.options.min_equipment_reinforcement_in_5
                max_reinforcement = self.options.max_equipment_reinforcement_in_5
                if min_reinforcement > max_reinforcement: min_reinforcement = max_reinforcement
                item_data.reinforcement = self.random.randint(min_reinforcement, max_reinforcement)

            if item_data.max_reinforcement == 10:
                min_reinforcement = self.options.min_equipment_reinforcement_in_10
                max_reinforcement = self.options.max_equipment_reinforcement_in_10
                if min_reinforcement > max_reinforcement: min_reinforcement = max_reinforcement 
                item_data.reinforcement = self.random.randint(min_reinforcement, max_reinforcement)

        return DS2Item(name, item_data.classification, item_data.code, self.player, item_data)

    def get_filler_item_name(self) -> str:
        filler_items = {
            item.name for item in item_list
            if item.category != ItemCategory.UNIQUE
            and not item.skip
            and not item.exclude
            and not item.version == DS2Version.SOTFS
        }
        return self.random.choice(tuple(filler_items))

    # TODO review
    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = self.options.as_dict(
            "game_version",
            "no_weapon_req",
            "no_spell_req",
            "no_armor_req",
            "no_equip_load",
        )

        keep_unrandomized = locations_to_keep_unrandomized
        if self.options.infinite_lifegems:
            keep_unrandomized.add(375400601)

        _location_map = {}
        for locations in locations_by_region.values():
            for location_data in locations:
                if location_data.is_event:
                    continue

                key = location_data.ds2_id + location_data.location_type.value

                if key not in _location_map:
                    _location_map[key] = {
                        "location_key": key,
                        "archipelago_ids": []
                    }

                    if (location_data.shop_price > 0):
                        _location_map[key]["shop_price"] = location_data.shop_price

                _location_map[key]["archipelago_ids"].append(location_data.address)

        for key in keep_unrandomized:
            if key not in _location_map:
                _location_map[key] = {"location_key": key}

            _location_map[key]["keep_unrandomized"] = True

        slot_data["location_data"] = list(_location_map.values())

        slot_data["item_data"] = [
            {
                "item_id": item.code,
                "item_type": item.item_type.value,
                "is_bundle": item.bundle,
                "reinforcement": item.reinforcement
            }
            for item in item_list
        ]

        return slot_data
