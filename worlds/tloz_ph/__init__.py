
import logging
from math import ceil
from typing import List, Union, ClassVar, Any, Optional, Tuple, TYPE_CHECKING, Iterable

import settings
from BaseClasses import Tutorial, Region, Location, LocationProgressType, Item, ItemClassification, Entrance, \
    CollectionState
from Fill import fill_restrictive, FillError
from Options import PlandoConnection
from entrance_rando import randomize_entrances, bake_target_group_lookup, EntranceRandomizationError, disconnect_entrance_for_randomization
from worlds.AutoWorld import WebWorld, World

from .Util import *
from .Options import *

from .data import LOCATIONS_DATA
from .data.Constants import *
from .data.Items import ITEMS, ITEM_GROUPS
from .data.Regions import REGIONS
from .data.Entrances import ENTRANCES, entrance_id_to_region, EVENTS, entrance_id_to_entrance
from .Subclasses import PHRegion, decode_entrance_groups, update_switch_logic, EntranceGroups, OPPOSITE_ENTRANCE_GROUPS
from .Client import PhantomHourglassClient  # Unused, but required to register with BizHawkClient
from .tracker.TrackerUtil import TRACKER_WORLD
from rule_builder.cached_world import CachedRuleBuilderWorld

logger = logging.getLogger("Client")
dev_prints = False

if TYPE_CHECKING:
    from .Subclasses import ERPlacementState, PHEntrance, PHRegion, PHTransition

class PhantomHourglassItem(Item):
    game = "Phantom Hourglass"

class PhantomHourglassWeb(WebWorld):
    display_name = "The Legend of Zelda: Phantom Hourglass"
    setup_en = Tutorial(
        "Phantom Hourglass Setup Guide",
        "A guide to setting up Phantom Hourglass MultiworldGG Randomizer on your computer.",
        "English",
        "setup.md",
        "setup/en",
        ["Carrotinator"]
    )
    faq = Tutorial(
        "Phantom Hourglass FAQ",
        "Questions you might have about the implementation, and credits",
        "English",
        "faq_and_credits.md",
        "faq/en",
        ["Carrotinator"]
    )
    tricks = Tutorial(
        "Phantom Hourglass Tricks and Skips",
        "Tricks and skips that might be required in harder logic settings, with videos when available",
        "English",
        "tricks_and_skips.md",
        "tricks_and_skips/en",
        ["Carrotinator"]
    )

    tutorials = [setup_en, faq, tricks]
    game = "The Legend of Zelda - Phantom Hourglass"
    theme = "ocean"
    option_groups = ph_option_groups

class PhantomHourglassSettings(settings.Group):
    class PHGetLogicalPathShortcuts(str):
        """
        For use with universal tracker.
        Toggles if universal tracker can use unlocked shortcuts and map warps to find shorter paths for /get_logical_path.
        """
    class BoatSpeed(int):
        """Your boat's max speed. Default is 266."""

    class BoatFastAccel(str):
        """Makes your boat accelerate instantly after charting a route or changing gear."""

    ut_get_logical_path_shortcuts: Union[PHGetLogicalPathShortcuts, bool] = True
    boat_speed: BoatSpeed = 0x10A
    boat_snap_speed: Union[BoatFastAccel, bool] = True


# Adds a consistent count of items to pool, independent of how many are from locations
def add_items_from_filler(item_pool_dict: dict, filler_item_count: int, item: str, count: int):
    if filler_item_count >= count:
        filler_item_count -= count
        item_pool_dict[item] = item_pool_dict.get(item, 0) + count
    else:
        item_pool_dict[item] = filler_item_count
        filler_item_count = 0
        print(f"Ran out of filler items! on item {item}")
    # print(f"Add item: {item}: {item_pool_dict[item]} | {filler_item_count}")
    return [item_pool_dict, filler_item_count]


def add_spirit_gems(pack_option, add_option):
    if pack_option == 1:
        return {"Power Gem": 20, "Wisdom Gem": 20, "Courage Gem": 20}
    else:
        count = ceil(20 / pack_option.value) + add_option
        return {"Power Gem Pack": count, "Wisdom Gem Pack": count, "Courage Gem Pack": count}


def add_sand(starting_time, time_incr, time_logic):
    max_sand_count = ceil((5999 - starting_time) / time_incr)
    max_time = 1
    if time_logic <= 2:
        max_time = 310 // [1, 2, 4, 0.5][time_logic]
    min_sand_count = ceil(max(max_time - starting_time, 1) / time_incr)
    if min_sand_count > 20:
        print(f"Too many sand items? Adding {min_sand_count} Sands or Hours to pool")

    # Balance to limits
    sand_count = min_sand_count + 2
    if sand_count < 5:
        sand_count = 5
    if sand_count > max_sand_count:
        sand_count = max_sand_count
    # print(f"Sand count: {sand_count} total {starting_time.value + min_sand_count * time_incr.value}")
    return {"Sand of Hours": sand_count}


def add_beedle_point_items():
    return {"Beedle Points (50)": 2, "Beedle Points (20)": 3, "Beedle Points (10)": 4}

def add_pedestal_items(place, option, excluded_dungeons, exclude_option):
    res: dict[str, int] = dict()
    def add_from_group(g, count=1):
        return {n: count for n in ITEM_GROUPS[g]}

    if place == "vanilla":
        return res

    # Create items
    if option == "open_globally":
        res |= add_from_group("Global Pedestal Items")
    elif option == "open_per_dungeon":
        res |= add_from_group("Regular Crystal Items")
        res |= add_from_group("Unique Force Gems", 3)
    elif option == "unique_pedestals":
        res |= add_from_group("Unique Crystal Items")
        res |= add_from_group("Unique Force Gems", 3)

    if exclude_option == 2 and not option == "open_globally":
        for item, count in res.copy().items():
            # print(f"dungeon: {item.split('(')[1][:-1]} from {item}")
            if item.split("(")[1][:-1] in excluded_dungeons:
                res.pop(item)

    return res

class PhantomHourglassWorld(CachedRuleBuilderWorld):
    """
    The Legend of Zelda: Phantom Hourglass is the sea bound handheld sequel to the Wind Waker.
    """
    game = "The Legend of Zelda - Phantom Hourglass"
    options_dataclass = PhantomHourglassOptions
    options: PhantomHourglassOptions
    required_client_version = (0, 6, 0)
    web = PhantomHourglassWeb()
    topology_present = True

    settings: ClassVar[PhantomHourglassSettings]
    settings_key = "tloz_ph_options"

    location_name_to_id = build_location_name_to_id_dict()
    item_name_to_id = build_item_name_to_id_dict()
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS
    origin_region_name = "Menu"

    glitches_item_name = "_UT_Glitched_Logic"
    ut_can_gen_without_yaml = True
    location_id_to_alias: Dict[int, str]
    tracker_world = TRACKER_WORLD
    found_entrances_datastorage_key = ["ph_checked_entrances_{player}_{team}",
                                       "ph_keylocking_{player}_{team}",
                                       "ph_ut_events_{player}_{team}",
                                       "ph_disconnect_entrances_{player}_{team}",
                                       "ph_traversed_entrances_{player}_{team}"]
    item_mapping: dict = {
        i: "Rupees" for i in ITEM_GROUPS["Rupee Items"] } | {
        i: "Treasure" for i in ITEM_GROUPS["Treasure Items"] } | {
        i: "Beedle Points" for i in ITEM_GROUPS["Beedle Point Items"] } | {
        "Power Gem Pack": "Power Gem",
        "Wisdom Gem Pack": "Wisdom Gem",
        "Courage Gem Pack": "Courage Gem"} | {
        i: "Sand" for i in ITEM_GROUPS["Sand Items"] }

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

        self.pre_fill_items: List[PhantomHourglassItem] = []
        self.required_dungeons = []
        self.boss_reward_items_pool: list[str] = []
        self.boss_reward_location_names = []

        self.dungeon_name_groups = {}
        self.post_dungeon_name_groups = {}
        self.boss_room_name_groups = {}

        self.locations_to_exclude: set[str] = set()
        self.locations_to_remove: set[str] = set()
        self.extra_filler_items = []
        self.excluded_dungeons = []
        self.ut_pairings = {}
        self.manual_er_pairings = []
        self.plando_er_pairings = []
        self.required_bosses = []
        self.item_mapping_collect: dict[str, tuple[str, int]] = {}

        self.entrances: dict[str, "Entrance"] = {}
        self.er_placement_state = None
        self.ut_connected_entrances = set()
        self.ut_redisconnected_entrances = set()
        self.ut_traversed_entrances = set()
        self.ut_reconnected_entrances = set()
        self.disconnected_exits_map = {}
        self.ut_excluded = []
        self.ut_created_events = []
        self.treasure_price_index = 0

        self.ut_map_page_hidden_locations = {}
        self.ut_map_page_hidden_entrances = {}
        self.ut_map_page_hidden_events = {}
        self.required_metals = 0
        self.required_rupees: int = 0

        self.dungeon_boss_pairs: dict[str, str] = {}
        self.extra_entrance_plando: list[PlandoConnection] = []

        self.salvage_locations: list[str] = []
        self.ship_part_order: list[list[int]] = []

        self.is_ut = getattr(self.multiworld, "generation_is_fake", False)

    def generate_early(self):
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            # slot_options: dict[str, Any] = slot_data.get("options", {})
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_data.items():
                opt = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))

            # Set randomized data that effects exclusions etc
            self.required_dungeons = list(slot_data["required_dungeons"])
            self.boss_reward_items_pool = slot_data["boss_reward_items_pool"]
            self.ut_pairings = slot_data.get("er_pairings", {})
            self.treasure_price_index = slot_data.get("treasure_price_index", 0)
            required_dungeon_locations = slot_data.get("required_dungeon_locations", [])
            self.locations_to_remove = {self.location_id_to_name[i] for i in slot_data.get("removed_locations", [])}

            # Figure out what events are active, and add to ut_pairings
            print(F"Generating early")
            print(f"UT Pairings: {self.ut_pairings}")
            if self.options.ut_events and getattr(self.multiworld, "enforce_deferred_connections", "default") != "off":
                for event in EVENTS.values():
                    if self.options.ut_events == "unique_events" and event.extra_data.get("shared_event", False):
                        continue
                    if "GOAL" in event.name:
                        if self.options.goal_requirements != "triforce_door" and event.name in ["GOAL: Triforce Door"]:
                            continue
                        if self.options.bellum_access != "zauz" and event.name in ["GOAL: Zauz"]:
                            continue
                        if ((self.options.goal_requirements == "triforce_door" or self.options.bellum_access == "zauz")
                              and event.name in ["GOAL: Bellumbeck"]):
                            continue
                    if not self.options.shuffle_houses and event.name == "EVENT: Open Eddo's Door":
                        continue
                    if not self.options.shuffle_overworld_transitions and event.name == "EVENT: Gust Windmills":
                        continue
                    if "Unnamed Entrance" in event.name:
                        continue
                    if (self.options.dungeon_hint_type.value == 2 and event.name in BOSS_EVENT_TO_LOCATION
                            and BOSS_EVENT_TO_LOCATION[event.name] not in required_dungeon_locations):
                        continue
                    if "silent_event" in event.extra_data:
                        continue

                    print(f"Adding Event: {event.name} {event.id} => {event.vanilla_reciprocal.id}")
                    self.ut_pairings[str(event.id)] = event.vanilla_reciprocal.id

            # Hide stuff in UT map page based on what entrances are randomized
            if not self.ut_map_page_hidden_locations or not self.ut_map_page_hidden_entrances:
                from .tracker.TrackerUtil import get_hidden_entrances
                self.ut_map_page_hidden_locations, self.ut_map_page_hidden_entrances = get_hidden_entrances(self)
        else:
            self.options.shopsanity.value = {s.lower() for s in self.options.shopsanity.value}
            # print(f"Shopsanity {self.options.shopsanity.value}, {self.options.shopsanity.valid_keys_casefold}")
            if 'all' in self.options.shopsanity.value:
                self.options.shopsanity.value = self.options.shopsanity.valid_keys_casefold

            self.pick_required_dungeons()
            if self.options.shuffle_dungeon_entrances:
                self.options.dungeon_shortcuts.value = 0
            # Dungeon hint restrictions
            if self.options.shuffle_bosses.value == 2 and self.options.dungeon_hint_type == "hint_dungeon":
                self.options.dungeon_hint_type.value = 1
            if not self.options.exclude_non_required_dungeons.value:
                self.options.excluded_dungeon_hints.value = 0

            # Keyring restrictions
            if not self.options.keysanity.value:
                self.options.keyrings.value = 0
            if (self.options.randomize_boss_keys.value in [0, 3]
                    or not self.options.keyrings.value):
                self.options.boss_keyrings.value = 0

            if self.options.spirit_type.value == 0 and self.options.global_spirit_upgrades.value:
                self.options.spirit_type.value = 1

            # Treasure Prices
            self.treasure_price_index = self.random.randint(0, 9)

            # Choose salvage locations
            if self.options.randomize_salvage.value:
                salvage_locs = LOCATION_GROUPS["Salvage Locations"].copy()
                self.random.shuffle(salvage_locs)
                self.salvage_locations = salvage_locs[:self.options.salvage_count.value-1]
                # print(len(self.salvage_locations), self.options.salvage_count.value)
                self.locations_to_remove.update(salvage_locs[self.options.salvage_count.value-1:])

            # print(f"remove_locations: {self.options.remove_locations.value}")
            for loc in self.options.remove_locations.value:
                self.locations_to_remove |= set(LOCATION_GROUPS.get(loc, {loc}))

        self.restrict_non_local_items()
        self.create_item_mappings()
        self.count_required_rupees()
        if self.options.goal_requirements == "metal_hunt":
            self.required_metals = self.options.metal_hunt_required.value
        elif self.options.goal_requirements == "defeat_bosses":
            if self.options.boss_reward_pool.value == 1:
                if self.options.dungeons_required.value <= 3:
                    self.required_metals = 0
                else:
                    self.required_metals = self.options.dungeons_required.value - 3
            else:
                self.required_metals = self.options.dungeons_required.value

        if self.options.bellum_access.value == 4:
            self.options.zauz_required_metals.value = self.required_metals
            self.locations_to_exclude.add("Zauz's House Phantom Blade")

    def create_item_mappings(self):
        self.item_mapping_collect |= {
            i: ("Rupees", ITEMS[i].value) for i in ITEM_GROUPS["Rupee Items"] } | {
            i: ("Treasure", prices[self.treasure_price_index]) for i, prices in TREASURE_PRICES.items() } | {
            i: ("Beedle Points", ITEMS[i].value) for i in ITEM_GROUPS["Beedle Point Items"] } | {
            f"{spirit} Gem Pack": (f"{spirit} Gem", self.options.spirit_gem_packs.value) for spirit in SPIRITS } | {
            "Phantom Hourglass": ("Sand", self.options.ph_starting_time.value),
            "Sand of Hours": ("Sand", self.options.ph_time_increment.value),
            "Sand of Hours (Boss)": ("Sand", 120),
            "Sand of Hours (Small)": ("Sand", 60),
            "Heart Container": ("Sand", self.options.ph_heart_time.value)
        }
        # print(f"Mappings: {self.item_mapping_collect}")

    def restrict_non_local_items(self):
        # Restrict non_local_items option in cases where it's incompatible with other options that enforce items
        # to be placed locally (e.g. dungeon items with keysanity off)
        if not self.options.keysanity == "anywhere":
            self.options.non_local_items.value -= set(ITEM_GROUPS["Small Keys"])
        self.options.non_local_items.value -= set(ITEM_GROUPS["Throwable Keys"])
        self.options.non_local_items.value -= set(self.boss_reward_items_pool)

    def create_location(self, region_name: str, location_name: str, local: bool):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, location_name, self.location_name_to_id[location_name], region)
        region.locations.append(location)

        if local:
            location.item_rule = lambda item: item.player == self.player

    def create_regions(self):
        # Add region aliases if UT
        all_regions = set(REGIONS)
        if self.is_ut:
            all_regions.update(set(ENTRANCES.keys()))
            for aliases in region_aliases.values():
                all_regions.update(aliases)
        # Create regions
        for region_name in all_regions:
            region = PHRegion(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Filter dungeon locations
        def add_to_name_group(group_name, group_var):
            if group_name in LOCATIONS_DATA[location_name]:
                group_var.setdefault(LOCATIONS_DATA[location_name][group_name], set())
                group_var[LOCATIONS_DATA[location_name][group_name]].add(location_name)

        for location_name in LOCATIONS_DATA:
            # Used for excluding room sets
            add_to_name_group("dungeon", self.dungeon_name_groups)
            if not self.options.open_post_dungeons.value:
                add_to_name_group("post_dungeon", self.post_dungeon_name_groups)
            add_to_name_group("boss_room", self.boss_room_name_groups)

        # Need to figure out removed locations as to not create them
        self.exclude_locations_automatically()

        # Create locations
        for location_name, location_data in LOCATIONS_DATA.items():
            if not self.location_is_active(location_name, location_data):
                continue
            is_local = "local" in location_data and location_data["local"] is True
            if location_data.region:
                self.create_location(location_data.region, location_name, is_local)

        # Need to create locations before they can be excluded
        for name in self.locations_to_exclude:
            try:
                self.multiworld.get_location(name, self.player).progress_type = LocationProgressType.EXCLUDED
            except KeyError:
                pass  # Archery minigame 2000 is dependent on logic difficulty

        # print(f"bosses: {self.required_bosses} dungeons: {self.required_dungeons} excluded: {self.excluded_dungeons}")
        self.create_events()


    def create_event(self, region_name, event_item_name):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, region_name + ".event", None, region)
        region.locations.append(location)
        location.place_locked_item(PhantomHourglassItem(event_item_name, ItemClassification.progression, None, self.player))

    def location_is_active(self, location_name, location_data):
        if location_name in self.locations_to_remove:
            return False
        if not location_data.conditional and not location_data.has_slot_data:
            return True

        if location_data.has_slot_data:
            for slot, _value, *args in location_data.has_slot_data:
                slot = getattr(self.options, slot, None).value
                if isinstance(slot, set):
                    if _value not in slot:
                        return False
                else:
                    _value = _value if isinstance(_value, list) else [_value]
                    if slot not in _value:
                        return False

            if location_data.restock:
                if 'restocks' not in self.options.shopsanity.value and (
                        location_data.restock in self.options.shopsanity.value or location_data.restock == "always"):
                    # print(f"Restock blocked: {location_name}")
                    return False
            return True

        if location_name in LOCATION_GROUPS["Golden Frogs"]:
            return self.options.randomize_frogs != PhantomHourglassFrogRandomization.option_start_with
        if location_name in LOCATION_GROUPS["Rupee Dig Spots"]:
            return self.options.randomize_digs
        if "Archery Minigame 2000" == location_name:
            return self.options.logic in ["hard", "glitched"] and self.options.randomize_minigames
        if location_name in LOCATION_GROUPS["Minigames"]:
            return self.options.randomize_minigames
        if location_name in LOCATION_GROUPS["Fishing Locations"]:
            return self.options.randomize_fishing
        if location_name in LOCATION_GROUPS["Salvage Locations"]:
            return self.options.randomize_salvage
        if location_name in LOCATION_GROUPS["Free Standing Locations"]:
            return self.options.randomize_pedestal_items.value
        if "Beedle Membership" in location_name:
            return self.options.randomize_beedle_membership.value > 1
        if "Harrow Island" in location_name:
            return self.options.randomize_harrow
        if "Zauz's House Triforce Crest" == location_name:
            return self.options.randomize_triforce_crest
        if location_name == "Man of Smiles' Prize Postcard":  # This it pretty random but whatever...
            return self.options.randomize_beedle_membership.value > 0
        return False

    def pick_required_dungeons(self):
        implemented_dungeons = DUNGEON_NAMES[1:]
        # Plando dungeon pool
        if self.options.plando_dungeon_pool.value:
            plandoed_dungeons = {DUNGEON_ABBREVIATIONS_LOWER.get(d.lower(), title2(d)) for d in self.options.plando_dungeon_pool.value}
            if "Temple of the Ocean King" in plandoed_dungeons:
                self.options.totok_in_dungeon_pool.value = 1
            implemented_dungeons = list(plandoed_dungeons)

        # Remove optional dungeons from pool
        if self.options.ghost_ship_in_dungeon_pool.value == 2 and "Ghost Ship" in implemented_dungeons:
            implemented_dungeons.remove("Ghost Ship")
        if not self.options.totok_in_dungeon_pool.value and "Temple of the Ocean King" in implemented_dungeons:
            implemented_dungeons.remove("Temple of the Ocean King")

        dungeons_required = len(implemented_dungeons) if self.options.dungeons_required > len(implemented_dungeons) \
            else self.options.dungeons_required.value
        if (self.options.totok_in_dungeon_pool.value
            and dungeons_required <= 3
            and self.options.boss_reward_pool.value == 1
            and self.options.spirit_type.value in [1, 2]
            and "Temple of the Ocean King" in implemented_dungeons):
            print(f"Boss rewards incompatible with TotOK for ({self.player_name}), removing TotOK from dungeon pool")
            implemented_dungeons.remove("Temple of the Ocean King")

        # Cap dungeons required if over the number of eligible dungeons
        dungeons_required = len(implemented_dungeons) if self.options.dungeons_required > len(implemented_dungeons) \
            else self.options.dungeons_required.value
        self.options.dungeons_required.value = dungeons_required
        self.random.shuffle(implemented_dungeons)
        self.required_dungeons = implemented_dungeons[:dungeons_required]

        # Cap zauz metals at number of metals
        if self.options.goal_requirements == "defeat_bosses":
            if self.options.zauz_required_metals > dungeons_required:
                self.options.zauz_required_metals.value = dungeons_required
            if self.options.boss_reward_pool.value == 1:
                if dungeons_required <= 3:
                    self.options.zauz_required_metals.value = 0
                else:
                    self.options.zauz_required_metals.value = min(self.options.zauz_required_metals.value, dungeons_required-3)
        elif self.options.goal_requirements == "metal_hunt":
            if self.options.zauz_required_metals > self.options.metal_hunt_total:
                self.options.zauz_required_metals.value = self.options.metal_hunt_total.value
        else:
            self.options.zauz_required_metals.value = 0

        # Cap metal hunt items
        if self.options.metal_hunt_total < self.options.metal_hunt_required:
            self.options.metal_hunt_total.value = self.options.metal_hunt_required.value

        # Choose excluded dungeons
        if self.options.exclude_non_required_dungeons.value:
            always_include = ["Temple of the Ocean King", "Mountain Passage"]
            excluded_dungeons = [d for d in DUNGEON_NAMES
                                 if d not in self.required_dungeons + always_include]
            self.excluded_dungeons = excluded_dungeons

        # Plando boss shuffle
        if self.options.shuffle_bosses.value == 1 and not self.options.decouple_entrances:
            to_shuffle = DUNGEON_TO_BOSS_ITEM_LOCATION_GS.copy()
            to_shuffle.pop("Temple of the Ocean King")
            dungeons = list(to_shuffle.keys())
            bosses = list(to_shuffle.values())
            self.random.shuffle(bosses)
            self.dungeon_boss_pairs = {d: b for d, b in zip(dungeons, bosses)}
            self.extra_entrance_plando += [PlandoConnection(DUNGEON_TO_BOSS_ENTRANCE[d], BOSS_LOC_TO_EXIT[b], "both") for d, b in self.dungeon_boss_pairs.items()]

        # Choose boss reward locations
        if not self.options.require_specific_bosses.value:
            self.required_bosses = list(DUNGEON_TO_BOSS_ITEM_LOCATION.values())
            if self.options.ghost_ship_in_dungeon_pool.value == 2:
                self.required_bosses.remove("_gs")
            if not self.options.totok_in_dungeon_pool:
                self.required_bosses.remove("TotOK B13 Sea Chart Chest")

            # Figure out shuffled boss chain
            if self.options.exclude_non_required_dungeons.value == 2:
                if "_gs" in self.required_bosses:
                    self.required_bosses.remove("_gs")
                    self.required_bosses += ["Ghost Ship Rescue Tetra", "Cubus Sisters Ghost Key"]
                if self.options.ghost_ship_in_dungeon_pool != "rescue_tetra" and "Ghost Ship Rescue Tetra" in self.required_bosses:
                    self.required_bosses.remove("Ghost Ship Rescue Tetra")
                for dungeon in self.excluded_dungeons:
                    if dungeon == "Ghost Ship" and "Ghost Ship Rescue Tetra" in self.required_bosses:
                        self.required_bosses.remove("Ghost Ship Rescue Tetra")
                    boss = self.dungeon_boss_pairs.get(dungeon, DUNGEON_TO_BOSS_ITEM_LOCATION_GS[dungeon])
                    # print(f"\tChecking boss: {dungeon}, {boss}")
                    if boss in self.required_bosses:
                        self.required_bosses.remove(boss)
                # print(f"Remaining bosses: {self.required_bosses}")

        elif self.options.shuffle_bosses.value == 1 and not self.options.decouple_entrances:
            self.required_bosses = []
            for dungeon, boss in self.dungeon_boss_pairs.items():
                if dungeon not in self.required_dungeons:
                    continue
                if dungeon == "Ghost Ship" and self.options.ghost_ship_in_dungeon_pool == "rescue_tetra":
                    self.required_bosses.append("Ghost Ship Rescue Tetra")
                else:
                    self.required_bosses.append(boss)
            if "Temple of the Ocean King" in self.required_dungeons:
                self.required_bosses.append("TotOK B13 Sea Chart Chest")
        else:
            self.required_bosses = [DUNGEON_TO_BOSS_ITEM_LOCATION[dung] for dung in
                                    self.required_dungeons]

        if "_gs" in self.required_bosses:
            self.required_bosses.remove("_gs")
            self.required_bosses.append(
                GHOST_SHIP_BOSS_ITEM_LOCATION[self.options.ghost_ship_in_dungeon_pool.value])

        # Extend mcguffin list
        if self.options.goal_requirements == "defeat_bosses":
            reward_count = self.options.dungeons_required
            if self.options.boss_reward_pool.value == 1:
                spirit_rewards = []
                if self.options.spirit_type.value == 0:
                    spirit_rewards = [f"Spirit of {s} (Progressive)" for s in SPIRITS]
                elif self.options.spirit_type.value == 1:
                    spirit_rewards = [f"Spirit of {s}" for s in SPIRITS]
                elif self.options.spirit_type.value == 2:
                    spirit_rewards = [f"Spirit (Progressive)" for _ in range(3)]
                if reward_count <=3:
                    self.random.shuffle(spirit_rewards)
                    self.boss_reward_items_pool = spirit_rewards[:reward_count]
                    reward_count = 0
                else:
                    self.boss_reward_items_pool = spirit_rewards[:reward_count]
                    reward_count -= 3
            if reward_count:
                self.boss_reward_items_pool += self.pick_metals(reward_count)

        # Add dungeon hints to start
        if self.options.dungeon_hint_location.value == 0 and self.options.dungeon_hint_type == "hint_boss":
            self.options.start_location_hints.value.update(self.required_bosses)

        # print(f"Picked Required Dungeons: {self.required_dungeons} bosses {self.required_bosses} \npairs {self.dungeon_boss_pairs}")


    def pick_metals(self, count):
        metal_items: list = list(ITEM_GROUPS["Vanilla Metals"])
        extended_pool: list = []
        if self.options.additional_metal_names == "vanilla_only":
            extended_pool = list(ITEM_GROUPS["Vanilla Metals"])
        elif self.options.additional_metal_names == "additional_rare_metal":
            extended_pool = ["Additional Rare Metal"]
        elif self.options.additional_metal_names == "custom":
            metal_items += ITEM_GROUPS["Custom Metals"]
            extended_pool = list(ITEM_GROUPS["Metals"])
        elif self.options.additional_metal_names == "custom_prefer_vanilla":
            metal_items = list(ITEM_GROUPS["Custom Metals"])
            extended_pool = list(ITEM_GROUPS["Metals"])

        while len(metal_items) < count:
            metal_items += self.random.choice([extended_pool])

        self.random.shuffle(metal_items)

        if self.options.additional_metal_names == "custom_prefer_vanilla":
            vanillas = list(ITEM_GROUPS["Vanilla Metals"])
            self.random.shuffle(vanillas)
            metal_items = vanillas + metal_items

        return metal_items[:count]

    def count_required_rupees(self):
        multiplier = 0.7 if self.options.shop_hints.value else 1
        rupees = 0

        rupee_totals = {
            "uniques": (2000, 4000, 1500, 0),
            "shields": (240, 0, 0, 0),
            "ammo": (250, 0, 0, 0),
            "treasure": (1800, 800, 2000, 1500),  # masked ship parts 1500, normals 800, treasure 500
            "potions": (330, 250, 80, 200)
        }

        for k, r in rupee_totals.items():
            if k in self.options.shopsanity.value:
                rupees += r[0]
                if self.options.randomize_masked_beedle.value:
                    rupees += r[2]
                    if "restocks" in self.options.shopsanity.value:
                        rupees += r[3]
                if "restocks" in self.options.shopsanity.value:
                    rupees += r[1]

        self.required_rupees = int(rupees*multiplier)
        # print(f"Required Rupees: {rupees} => {self.required_rupees}")

    def create_events(self):
        if self.is_ut:
            self.create_event("Menu", "_is_ut")
        else:
            self.create_event("Menu", "_is_not_ut")

        # Create events for required dungeons
        # print(f"Event bosses: {self.required_bosses} {self.required_dungeons}")
        if self.options.goal_requirements == "defeat_bosses":
            if "Blaaz Boss Reward" in self.required_bosses:
                self.create_event("Post Blaaz", "_required_dungeon")
            if "Cyclok Boss Reward" in self.required_bosses:
                self.create_event("Post Cyclok", "_required_dungeon")
            if "Crayk Boss Reward" in self.required_bosses:
                self.create_event("Post Crayk", "_required_dungeon")
            if "Ghost Ship Rescue Tetra" in self.required_bosses:
                self.create_event("Ghost Ship Tetra", "_required_dungeon")
            if "Cubus Sisters Ghost Key" in self.required_bosses:
                self.create_event("Post Cubus Sisters", "_required_dungeon")
            if "Dongorongo Boss Reward" in self.required_bosses:
                self.create_event("Post Dongorongo", "_required_dungeon")
            if "Gleeok Boss Reward" in self.required_bosses:
                self.create_event("Post Gleeok", "_required_dungeon")
            if "Eox Boss Reward" in self.required_bosses:
                self.create_event("Post Eox", "_required_dungeon")
            if "TotOK B13 Sea Chart Chest" in self.required_bosses:
                self.create_event("TotOK B13 Chest", "_required_dungeon")

        reverse_boss_pairs = {BOSS_LOCATION_TO_DUNGEON[b]: d for d, b in self.dungeon_boss_pairs.items()}

        def dungeon_event(dungeon, region_name, event_item_name):
            if self.options.exclude_non_required_dungeons.value == 2 and dungeon in self.excluded_dungeons:
                return
            self.create_event(region_name, event_item_name)

        def boss_event(dungeon, region_name, event_item_name):
            matching_dungeon = reverse_boss_pairs.get(dungeon, dungeon)
            if self.options.exclude_non_required_dungeons.value == 2 and matching_dungeon in self.excluded_dungeons:
                return
            self.create_event(region_name, event_item_name)

        def post_boss_event(dungeon, region_name, event_item_name):
            if self.options.open_post_dungeons.value:
                self.create_event(region_name, event_item_name)
                return
            boss_event(dungeon, region_name, event_item_name)

        # Post Dungeon Events
        boss_event("Temple of Fire","Post ToF", "_beat_tof")
        boss_event("Temple of Courage", "Post ToC", "_beat_toc")
        boss_event("Temple of Wind", "Post ToW", "_beat_tow")
        boss_event("Goron Temple","Post GT", "_beat_gt")
        boss_event("Temple of Ice", "Post ToI", "_beat_toi")
        boss_event("Mutoh's Temple","Post MT", "_beat_mt")
        dungeon_event("Ghost Ship", "Spawn Pirate Ambush", "_beat_ghost_ship")
        boss_event("Ghost Ship", "Post Cubus Sisters Event", "_beat_cubus_sisters")
        # Farmable minigame events
        self.create_event("Bannan Cannon Game", "_can_play_cannon_game")
        post_boss_event("Temple of Courage","Archery Game", "_can_play_archery")
        self.create_event("Harrow Minigame", "_can_play_harrow")
        post_boss_event("Goron Temple","Dee Ess Goron Race", "_can_play_goron_race")
        self.create_event("TotOK B1 Phantom", "_can_farm_totok")
        # Wayfarer Trade Quest
        self.create_event("Wayfarer Event", "_wayfarer_gift")
        self.create_event("SS Wayfarer Event", "_wayfarer_trade")
        # Shop stuff
        self.create_event("Treasure Teller", "_has_treasure_teller")
        # Switch states etc
        dungeon_event("Temple of Courage", "ToC B1 Invisible Maze", "_toc_b1_maze")
        self.create_event("Bremeur's Temple Event", "_ruins_lower_water")
        self.create_event("Gust North Event", "_windmills")
        self.create_event("Goron Chus Event", "_goron_chus")
        self.create_event("Goron SE Bridge Event", "_goron_bridge")
        self.create_event("Goron NE Event", "_goron_maze_switch")
        self.create_event("Eddo Event", "_eddo_door")
        dungeon_event("Temple of Ice", "ToI B1 Switch", "_toi_b1_switch")
        dungeon_event("Ghost Ship", "Ghost Ship B3", "_rescue_4th_sister")
        # Blue warps
        dungeon_event("Temple of Ice", "ToI Blue Warp", "_toi_blue_warp")
        # Mountain passage
        self.create_event("Mountain Passage 1", "_mp1")
        self.create_event("Mountain Passage Rat", "_mp3")
        # Goal
        self.create_event("Goal", "_beaten_game")

    def exclude_locations_automatically(self):
        locations_to_exclude = set()

        # Filter out boss/post dungeon locations for exclusion/removal
        if self.options.exclude_non_required_dungeons.value:
            # print(f"Excluded dungeons")
            for dungeon in self.excluded_dungeons:
                locations_to_exclude.update(self.dungeon_name_groups[dungeon])
                if self.options.shuffle_bosses != 1 or self.options.decouple_entrances:
                    post_dungeon = dungeon
                else:  # shuffled bosses
                    post_dungeon = BOSS_LOCATION_TO_DUNGEON[self.dungeon_boss_pairs[dungeon]]
                # print(f"\tPost dungeon: {dungeon} -> {post_dungeon}")
                locations_to_exclude.update(self.boss_room_name_groups.get(post_dungeon, []))
                locations_to_exclude.update(self.post_dungeon_name_groups.get(post_dungeon, []))
                if not self.options.shuffle_houses and not self.options.open_post_dungeons.value and post_dungeon == "Temple of Fire":
                    locations_to_exclude.add("Shipyard Chest")
                if dungeon == "Ghost Ship" and not self.options.open_post_dungeons.value:
                    if self.options.randomize_triforce_crest.value:
                        locations_to_exclude.add("Zauz's House Triforce Crest")
                    locations_to_exclude.add("Ocean Miniblin Pirate Ambush Item")


        if self.options.exclude_non_required_dungeons.value == 1:
            self.locations_to_exclude.update(locations_to_exclude)
        elif self.options.exclude_non_required_dungeons.value == 2:
            # print(f"Locations to remove: {locations_to_exclude}")
            self.locations_to_remove.update(locations_to_exclude)

    def create_er_target_groups(self, type_option_lookup):

        simple_mixed_pool = []
        for a, option in type_option_lookup.items():
            if option == "simple_mixed_pool":
                simple_mixed_pool.append(a)

        unique_groups = {entrance.randomization_group for entrance in self.multiworld.get_entrances(self.player)
                         if entrance.parent_region and not entrance.connected_region}


        def get_target_groups(g: int) -> list[int]:
            direction = g & EntranceGroups.DIRECTION_MASK
            area = (g & EntranceGroups.AREA_MASK) >> 3
            island = (g & EntranceGroups.ISLAND_MASK) >> 7
            target_directions, target_areas, target_islands = [], [], set()
            in_simple_mixed_pool = area in simple_mixed_pool
            # print(f"{decode_entrance_groups(g)} in simple pool? {in_simple_mixed_pool}")

            # Create target direction list
            if ((in_simple_mixed_pool and self.options.entrance_directionality.value in [1, 2]) or
                    (not in_simple_mixed_pool and self.options.entrance_directionality.value in [1, 3])):
                #if area == 1 and (not in_simple_mixed_pool or len(simple_mixed_pool) == 1):
                    # 90% if houses are dead ends, and GER can't handle that with disregarded directionality
                    # target_directions = [OPPOSITE_ENTRANCE_GROUPS[direction]]
                # else:
                target_directions = range(7)
            else:
                target_directions = [OPPOSITE_ENTRANCE_GROUPS[direction]]

            # Create target type list
            if in_simple_mixed_pool:
                target_areas += simple_mixed_pool
            else:
                target_areas.append(area)

            # Create target island list
            if ((in_simple_mixed_pool and self.options.shuffle_between_islands.value in [0, 3])
                    or (not in_simple_mixed_pool
                     and self.options.shuffle_between_islands.value in [0, 2]
                     and type_option_lookup[area].value != 3)):
                target_islands.update(range(15))
            else:
                target_islands.add(island)
                # ports still need to be able to connect to the sea
                if area == 3:
                     target_islands.update(range(15))
                if in_simple_mixed_pool and 3 in simple_mixed_pool:
                    target_islands.add(0)
                if island == 0:
                    target_islands.update(range(15))

            def island_iter(loop, t):
                ret = []
                for i in loop:
                    new_group = d | (t << 3) | (i << 7)
                    if new_group in unique_groups:
                        ret.append(new_group)
                return ret

            def area_iter(loop):
                ret = []
                for t in loop:
                    if in_simple_mixed_pool and 3 in simple_mixed_pool and t == 3:
                        ret += island_iter(range(15), t)
                    else:
                        ret += island_iter(target_islands, t)
                return ret

            # Put it all together
            res = []
            for d in target_directions:
                if in_simple_mixed_pool and 3 in simple_mixed_pool and area == 3:
                    res += area_iter(simple_mixed_pool)
                else:
                    res += area_iter(target_areas)


            if dev_prints and False:
                print(f"res: {decode_entrance_groups(g)}")
                print(f"\t{sorted([decode_entrance_groups(i) for i in res])}")
            return res

        return bake_target_group_lookup(self, get_target_groups)

    def connect_entrances(self) -> None:
        # UT only needs to disconnect entrances, use slot data pairings to figure out which
        if self.is_ut:
            disconnect_ids = {int(i) for i in self.ut_pairings.keys()}
            for e in self.entrances.values():
                if ENTRANCES[e.name].id in disconnect_ids:
                    target_name = ENTRANCES[e.name].vanilla_reciprocal.name
                    disconnect_entrance_for_randomization(e, one_way_target_name=target_name)
            if getattr(self.multiworld, "enforce_deferred_connections", "default") == "off":
                for i, pairing in self.ut_pairings.items():
                    _exit: "Entrance" = self.get_entrance(entrance_id_to_entrance[int(i)].name)
                    entrance_region: "Region" = self.get_region(entrance_id_to_region[pairing])
                    _exit.connect(entrance_region)
        else:
            # What option corresponds with what type
            type_option_lookup = {
                1: self.options.shuffle_houses,
                2: self.options.shuffle_caves,
                3: self.options.shuffle_ports,
                4: self.options.shuffle_overworld_transitions,
                5: self.options.shuffle_dungeon_entrances,
                6: self.options.shuffle_bosses,
                7: self.options.shuffle_dungeons_internally,
                8: self.options.shuffle_dungeons_internally,
                9: self.options.shuffle_caves,
                10: self.options.shuffle_caves,
                11: False  # Events, UT only
                }

            # Filter entrances to disconnect by yaml settings
            randomized_entrances: list["Entrance"] = []
            plando_disconnects = set()
            for i in self.options.plando_transitions.value:
                plando_disconnects.add(i.entrance)
                plando_disconnects.add(ENTRANCES[i.entrance].vanilla_reciprocal.name)
                plando_disconnects.add(i.exit)
                plando_disconnects.add(ENTRANCES[i.exit].vanilla_reciprocal.name)
            if dev_prints:
                print(f"Plando disconnects {plando_disconnects}")
            for e in self.entrances.values():
                # print(f"ER: {e.name} {bin(e.randomization_group)} {bin(EntranceGroups.AREA_MASK)} {(e.randomization_group & EntranceGroups.AREA_MASK) >> 3}")
                if type_option_lookup[(e.randomization_group & EntranceGroups.AREA_MASK) >> 3]:
                    if not (ENTRANCES[e.name].extra_data.get("glitched", False) and self.options.logic != "glitched"):
                        randomized_entrances.append(e)
                elif e.name in plando_disconnects:
                    randomized_entrances.append(e)

            # if self.options.shuffle_bosses and self.options.ghost_ship_in_dungeon_pool.value == 2 and self.options.exclude_non_required_dungeons:
            #     randomized_entrances.remove(self.entrances["Ghost Ship Cubus Sisters Reunion"])
            #     randomized_entrances.remove(self.entrances["Cubus Sisters Blue Warp"])

            # Disconnect entrances to shuffle
            for entrance in randomized_entrances:
                target_name = ENTRANCES[entrance.name].vanilla_reciprocal.name
                disconnect_entrance_for_randomization(entrance, one_way_target_name=target_name)
                if dev_prints:
                    print(f"disconnected {entrance.name}, parent {entrance.parent_region}, child {entrance.connected_region}, group {entrance.randomization_group}")


            # Get valid connection groups
            groups = self.create_er_target_groups(type_option_lookup)

            if dev_prints:
                print(f"groups:")
                for a, g in sorted(groups.items()):
                    print(f"\t{a}\t{decode_entrance_groups(a)}: {sorted([decode_entrance_groups(i) for i in g])}")

            # Decide if coupled
            coupled = not self.options.decouple_entrances

            def on_connect(er_state: "ERPlacementState", placed_exits: list["PHEntrance"],
                           paired_entrances: list["PHEntrance"]):

                # Super cursed way of passing switch state options
                # if not hasattr(er_state, "switch_state_option"):
                #     er_state.switch_state_option = self.options.color_switch_behaviour

                # Figure out what exits are new and need to inherit switch state stuff

                new_exits = set()
                if hasattr(er_state, "old_available_exits"):
                    new_exits = set(er_state.find_placeable_exits(True, er_state.entrance_lookup._usable_exits)) - er_state.old_available_exits
                    if dev_prints:
                        # print(f"\ton connecting {placed_exits}, revealed new exits {new_exits}")
                        pass
                else:
                    er_state.old_available_exits = set()

                # Pass on valid switch states to new available exits. Switch logic is backlogged for now
                # for ex, entr in zip(placed_exits, paired_entrances):
                #     update_switch_logic(ex, entr, er_state, self.options.logic.value, self.options.color_switch_behaviour.value, new_exits)

                # Update old exits now that you've used new exits
                er_state.old_available_exits.update(new_exits)

                # Super cursed way of passing in target group lookup to er_state
                if not hasattr(er_state, "target_group_lookup"):
                    er_state.target_group_lookup = groups
                    return False

                # Remove dead ends
                for entr in placed_exits:
                    # print(f"\tConnected {entr.name} group {decode_entrance_groups(entr.randomization_group)}")
                    for i in er_state.dead_end_counter.values():
                        if entr.name in i.dead_ends:
                            i.dead_ends.remove(entr.name)
                            # print(f"\t\tremoved from {decode_entrance_groups(i.group)} dead ends")
                        if entr.name in i.others:
                            i.others.remove(entr.name)
                            # print(f"\t\tremoved from {decode_entrance_groups(i.group)} dead ends")

                return False

            # Connect plando first, cause they will not be redone if failed
            self.connect_plando(self.options.plando_transitions)
            self.connect_plando(self.extra_entrance_plando)
            # Do ER
            ph_max_er_attempts = 10
            for i in range(ph_max_er_attempts):
                # Workaround cause ER likes to link dead ends to each other when ignoring directions.
                # Concept borrowed from CodeGorilla's Crystalis implementation
                try:
                    if not self.options.decouple_entrances: self.manual_er()
                    self.er_placement_state = randomize_entrances(self, coupled, groups, on_connect=on_connect)
                    if dev_prints:
                        print(self.er_placement_state.pairings)
                    break

                except EntranceRandomizationError as error:
                    print(f"Phantom Hourglass ER failed {i+1} time(s), retrying")
                    if i >= ph_max_er_attempts-1:
                        raise EntranceRandomizationError(
                            f"Phantom Hourglass: failed GER after {ph_max_er_attempts} attempts.")
                    # disconnect entrances again, but only if they got connected before
                    for region in self.get_regions():
                        # print(f"\tRegion: {region} | exits {[e for e in region.get_exits()]}")
                        for _exit in region.get_exits():
                            if (_exit.parent_region
                                and _exit.connected_region
                                and _exit in randomized_entrances):
                                # print(f"Disconnecting entrance {_exit} {_exit.randomization_group}")
                                target_name = ENTRANCES[_exit.name].vanilla_reciprocal.name
                                disconnect_entrance_for_randomization(_exit, one_way_target_name=target_name)

    # Based on the messenger's plando connection by Aaron Wagner
    def connect_plando(self, plando_connections: Iterable["PlandoConnection"]) -> None:
        def remove_dangling_exit(region: Region, name) -> None:
            # find the disconnected exit and remove references to it
            for _exit in region.exits:
                if not _exit.connected_region and _exit.name == name:
                    break
            else:
                raise ValueError(f"Unable to find randomized transition for {plando_connection}")

            region.exits.remove(_exit)

        def remove_dangling_entrance(region: Region, name) -> None:
            # find the disconnected entrance and remove references to it
            for _entrance in region.entrances:
                if not _entrance.parent_region and _entrance.name == name:
                    break
            else:
                raise ValueError(f"Invalid target region for {plando_connection}")
            region.entrances.remove(_entrance)

        for plando_connection in plando_connections:
            # get the connecting regions
            r1 = ENTRANCES[plando_connection.entrance]
            reg1 = self.get_region(r1.entrance_region)
            remove_dangling_exit(reg1, plando_connection.entrance)

            r2 = ENTRANCES[plando_connection.exit]
            reg2 = self.get_region(r2.entrance_region)
            remove_dangling_entrance(reg2, plando_connection.exit)
            # connect the regions
            reg1.connect(reg2)
            self.plando_er_pairings.append((r1.name, r2.name))
            if dev_prints:
                print(f"Plando Connecting {r1} => {r2} with regions {reg1} => {reg2}")
                print(f"ER pairings: {self.plando_er_pairings}")

            # pretend the user set the plando direction as "both" regardless of what they actually put on coupled
            if (self.options.decouple_entrances == "couple_all"
                 or plando_connection.direction == "both"):
                remove_dangling_exit(reg2, plando_connection.exit)
                remove_dangling_entrance(reg1, plando_connection.entrance)
                reg2.connect(reg1)
                self.plando_er_pairings.append((r2.name, r1.name))
                if dev_prints:
                    print(f"Connecting backwards {r2} => {r1}")

    def manual_er(self):
        def get_disconnected_entrances():
            return {entrance.name: entrance for region in self.multiworld.get_regions(self.player)
                             for entrance in region.entrances if not entrance.parent_region}
        def get_disconnected_exits():
            return {ex.name: ex for region in self.multiworld.get_regions(self.player)
                             for ex in region.exits if not ex.connected_region}

        def manual_connect(ex, entr):
            # Connect!
            if dev_prints:
                print(f"Connecting {ex} => {entr}")
            target_region = entr.connected_region
            target_region.entrances.remove(entr)
            ex.connect(target_region)
            self.manual_er_pairings.append((ex.name, entr.name))

            # If coupled do reverse entrance
            if not self.options.decouple_entrances:
                ex2 = exit_map[entr.name]
                entr2 = entrance_map[ex.name]
                if dev_prints:
                    print(f"Connecting {ex2} => {entr2}")
                entr2.connected_region.entrances.remove(entr2)
                ex2.connect(entr2.connected_region)
                self.manual_er_pairings.append((ex2.name, entr2.name))

        def get_random_entrance(entr):
            entr_list = [entrance_map[i] for i in entr]
            self.random.shuffle(entr_list)
            return entr_list[0]

        def get_random_exit(ex):
            ex_list = [exit_map[i] for i in ex]
            self.random.shuffle(ex_list)
            return ex_list[0]

        self.manual_er_pairings = []
        bremeur_location = "Ruins NW Pyramid"

        # Connect ruins stuff early given certain risky conditions, because GER can't handle the water level
        if (self.options.shuffle_houses == "shuffle"
                and self.options.shuffle_between_islands.value in [1, 3]):
            # Find entrance objects
            entrance_map = get_disconnected_entrances()
            exit_map = get_disconnected_exits()
            bremeur_entrance = entrance_map["Bremeur's Exit"]
            house_exit = get_random_exit(["Ruins NW Pyramid", "Ruins NE Small Pyramid"])
            bremeur_location = house_exit.name

            # Connect!
            manual_connect(house_exit, bremeur_entrance)

        if (self.options.shuffle_overworld_transitions == "shuffle"
                and self.options.shuffle_between_islands.value in [1, 3]
                and self.options.shuffle_houses.value in [0, 1]):
            entrance_map = get_disconnected_entrances()
            exit_map = get_disconnected_exits()

            # Create entrance pool
            entrance_list = ["Ruins NW One-Way Ledge South",
                             "Ruins NW One-Way Ledge SW",]
            if self.options.entrance_directionality.value in [1, 3]:
                entrance_list += ["Ruins NW Across Bridge East",
                                  "Ruins NW Upper One-Way East",
                                  "Ruins SW Port Cliff North",
                                  "Ruins SW East",
                                  "Ruins NE Doylan Bridge One-Way West"]
                if bremeur_location == "Ruins NE Small Pyramid":
                    entrance_list += ["Ruins NE Doylan's Bridge NW"]

            # Find entrance objects
            maze_exit = exit_map["Ruins SW Upper Maze North"]
            new_entrance = get_random_entrance(entrance_list)

            # Connect!
            manual_connect(maze_exit, new_entrance)

            # If house ends up in the wrong screen, do another manual placement
            old_entrance = new_entrance.name
            if "Ruins NW" in old_entrance:
                if bremeur_location != "Ruins NW Pyramid":
                    new_entrance = get_random_entrance(["Ruins NE Doylan's Bridge NW",
                                                        "Ruins NE Doylan Bridge One-Way West"])
                    if old_entrance != "Ruins NW Across Bridge East":
                        new_exit = exit_map["Ruins NW Across Bridge East"]
                    else:
                        new_exit = get_random_exit(["Ruins NW One-Way Ledge South", "Ruins NW One-Way Ledge SW"])
                    manual_connect(new_exit, new_entrance)

            elif "Ruins NE" in old_entrance:
                if bremeur_location != "Ruins NE Small Pyramid":
                    new_exit = exit_map["Ruins NE Doylan's Bridge NW"]
                    new_entrance = get_random_entrance(["Ruins NW One-Way Ledge South",
                                                        "Ruins NW One-Way Ledge SW",
                                                        "Ruins NW Across Bridge East",
                                                        "Ruins NW Upper One-Way East"])
                    manual_connect(new_exit, new_entrance)

            elif "Ruins SW" in old_entrance:
                new_exit_name = ["Ruins SW Port Cliff North", "Ruins SW East"]
                new_exit_name.remove(old_entrance)
                new_exit = exit_map[new_exit_name[0]]
                if bremeur_location == "Ruins NE Small Pyramid":
                    new_entrance = get_random_entrance(["Ruins NE Doylan's Bridge NW",
                                                        "Ruins NE Doylan Bridge One-Way West"])
                else:
                    new_entrance = get_random_entrance(["Ruins NW One-Way Ledge South",
                                                        "Ruins NW One-Way Ledge SW",
                                                        "Ruins NW Across Bridge East",
                                                        "Ruins NW Upper One-Way East"])
                manual_connect(new_exit, new_entrance)

    def set_rules(self):
        try:
            from .LogicRB import create_connections
            # raise ModuleNotFoundError
        except ModuleNotFoundError:
            from .Logic import create_connections

        create_connections(self, self.player, self.origin_region_name, self.options)
        # self.multiworld.completion_condition[self.player] = lambda state: state.has("_beaten_game", self.player)

    def create_item(self, name: str) -> PhantomHourglassItem:
        classification = ITEMS[name].classification
        if name == "Swordsman's Scroll" and self.options.logic == "glitched":
            classification = ItemClassification.progression
        if self.options.ph_time_logic.value > 2:
            if name in ["Sand of Hours", "Heart Container"]:
                classification = ItemClassification.useful
        if name == "Heart Container" and self.options.ph_heart_time == 0:
            classification = ItemClassification.useful
        if name in self.extra_filler_items:
            self.extra_filler_items.remove(name)
            classification = ItemClassification.filler

        ap_code = self.item_name_to_id[name]
        return PhantomHourglassItem(name, classification, ap_code, self.player)

    def build_item_pool_dict(self):
        def force_vanilla():
            # print(f"\tForcing vanilla {item_name}")
            item_obj = self.create_item(item_name)
            loc_obj = self.multiworld.get_location(loc_name, self.player)
            loc_obj.place_locked_item(item_obj)
            loc_obj.progress_type = LocationProgressType.DEFAULT

        removed_item_quantities = self.options.remove_items_from_pool.value.copy()
        item_pool_dict = {}
        filler_item_count = 0
        for loc_name, loc_data in LOCATIONS_DATA.items():
            if not self.location_is_active(loc_name, loc_data):
                # print(f"{loc_name} is not active")
                continue
            # If no defined vanilla item, fill with filler
            if not loc_data.vanilla_item:
                # print(f"{loc_name} has no defined vanilla item")
                filler_item_count += 1
                continue

            item_name = loc_data.get("item_override", loc_data["vanilla_item"])
            # print(f"item: {item_name} from {loc_name}")
            if item_name == "Filler Item":
                filler_item_count += 1
                continue
            if item_name in removed_item_quantities and removed_item_quantities[item_name] > 0:
                removed_item_quantities[item_name] -= 1
                filler_item_count += 1
                continue
            if self.options.keysanity == "vanilla":
                # Place small key in vanilla location
                if "Small Key" in item_name:
                    force_vanilla()
                    continue
            if self.options.randomize_boss_keys.value in [0, 3] and "Boss Key" in item_name:
                force_vanilla()
                continue
            if loc_data.force_vanilla:
                force_vanilla()
                continue
            if hasattr(ITEMS[item_name], 'dungeon'):
                # dung = item_name.rsplit('(', 1)[1][:-1]
                # If pedestal item location is vanilla, lock them there
                if (self.options.randomize_pedestal_items.value in [0, 1]
                        and item_name in ITEM_GROUPS["Regular Pedestal Items"]):
                    force_vanilla()
                    continue
            if item_name in ITEM_GROUPS["Golden Frog Glyphs"]:
                if self.options.randomize_frogs == "vanilla":
                    forced_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                    continue
            # Goal locations are for UT, and should not have actual items
            if "GOAL" in item_name:
                forced_item = self.create_item(item_name)
                self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                continue
            # if "Treasure Map" in item_name:
            #     filler_item_count += 1
            #     continue
            if (item_name in ITEM_GROUPS["Equipment"] |
                    ITEM_GROUPS["Technical Items"] |
                    ITEM_GROUPS["Spirits"] |
                    ITEM_GROUPS["Small Keys"] | ITEM_GROUPS["Boss Keys"] |
                    ITEM_GROUPS["Potions"] |
                    ITEM_GROUPS["Single Spirit Gems"] |
                    ITEM_GROUPS["Regular Pedestal Items"] |  # These get locked in the dungeon category if vanilla
                    {"Heart Container", "Triforce Crest", "Rare Metal", "Shield"}):
                filler_item_count += 1
                continue

            item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

        # Fill filler count with consistent amounts of items, when filler count is empty it won't add any more items
        # so add progression items first
        add_items = {"Phantom Hourglass": 1, "Boomerang": 1, "Hammer": 1, "Grappling Hook": 1, "Shovel": 1}
        add_items |= self.choose_progressive_items()
        # print(f"pre-keys: {item_pool_dict}")
        key_items, filler_change = self.choose_key_items()
        add_items |= key_items
        filler_item_count += filler_change
        # If metal hunt create and add metals
        if self.options.goal_requirements == "metal_hunt":
            metal_pool = {}
            for i in self.pick_metals(self.options.metal_hunt_total):
                metal_pool.setdefault(i, 0)
                metal_pool[i] += 1
            add_items |= metal_pool.items()
        elif self.options.goal_requirements == "defeat_bosses":
            for i in self.boss_reward_items_pool:
                if i in ITEM_GROUPS["Metals"]:
                    add_items.setdefault(i, 0)
                    add_items[i] += 1
        add_items |= add_spirit_gems(self.options.spirit_gem_packs, self.options.additional_spirit_gems)
        add_items |= {"Triforce Crest": 1} if self.options.randomize_triforce_crest.value else {}
        # Add pedestal items
        if self.options.randomize_pedestal_items.value > 1:
            add_items |= add_pedestal_items(self.options.randomize_pedestal_items, self.options.pedestal_item_options, self.excluded_dungeons, self.options.exclude_non_required_dungeons.value)
        if self.options.map_warp_options.value in [1]:
            add_items |= {i: 1 for i in ITEM_GROUPS["Map Warp Unlocks"]}
        # Add beedle point items
        if self.options.randomize_beedle_membership.value > 0:
            if self.options.randomize_beedle_membership.value > 1:
                add_items |= add_beedle_point_items()
            add_items |= {"Freebie Card": 1, "Complimentary Card": 1}
        # Add items from options
        for item, count in self.options.add_items_to_pool.items():
            add_items.setdefault(item, 0)
            add_items[item] += count
        # Add sand items to pool
        add_items |= add_sand(self.options.ph_starting_time, self.options.ph_time_increment,
                              self.options.ph_time_logic)
        # Add useful items last cause they can risk being overwritten
        if self.options.shield_in_pool.value:
            add_items |= {"Shield": 3}
        add_items |= {"Heart Container": 13}
        add_items |= self.choose_ship_items()
        # add items to item pool
        # print(f"Add items: {add_items}")
        for i, count in add_items.items():
            item_pool_dict, filler_item_count = add_items_from_filler(item_pool_dict, filler_item_count, i, count)
            if filler_item_count <= 0:
                break
        # Add as many filler items as required
        for _ in range(filler_item_count):
            random_filler_item = self.get_filler_item_name()
            item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1
        # Remove items from options, replace with filler
        for item, count in self.options.remove_items_from_pool.items():
            if item in item_pool_dict:
                new_count = item_pool_dict[item] - count
                if new_count < 0:
                    count = count + new_count
                item_pool_dict[item] -= count
                for i in range(count):
                    random_filler_item = self.get_filler_item_name()
                    item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1
        # r = 0
        # for i, c in item_pool_dict.items():
        #     if i in self.item_mapping_collect:
        #         g, t = self.item_mapping_collect[i]
        #         if g in ["Rupees", "Treasure"]:
        #             r += c*t
        # print(f"Total rupees in pool: {r}")
        return item_pool_dict

    def choose_progressive_items(self) -> dict[str, int]:
        res: dict[str, int] = {}

        # Inventory Items
        if self.options.progressive_items.value:
            res |= {"Sword (Progressive)": 2,
                    "Bombs (Progressive)": 3,
                    "Bow (Progressive)": 3,
                    "Bombchus (Progressive)": 3}
            if self.options.randomize_fishing.value:
                res |= {"Fishing Rod (Progressive)": 3}
        else:
            res |= {
                "Oshus' Sword": 1, "Phantom Sword": 1,
                "Bomb Bag": 1, "Bomb Bag Upgrade": 2,
                "Bow": 1, "Quiver Upgrade": 1,
                "Bombchu Bag": 1, "Bombchu Bag Upgrade": 2}
            if self.options.randomize_fishing.value:
                res |= {"Fishing Rod": 1, "Big Catch Lure": 1, "Swordfish Shadows": 1}

        # Spirits
        def add_upgrades():
            if self.options.global_spirit_upgrades.value:
                return {f"Spirit Upgrade": 2}
            else:
                return {f"{s} Upgrade": 2 for s in SPIRITS}

        if self.options.spirit_type == 0:
            res |= {f"Spirit of {s} (Progressive)": 3 for s in SPIRITS}
        elif self.options.spirit_type == 1:
            res |= {f"Spirit of {s}": 1 for s in SPIRITS}
            res |= add_upgrades()
        elif self.options.spirit_type == 2:
            res |= {"Spirit (Progressive)": 3}
            res |= add_upgrades()
        return res

    def choose_key_items(self) -> tuple[dict[str, int], int]:
        res: dict[str, int] = {}

        # Small keys
        keyring_dungeons = []
        if not self.options.keysanity.value:
            pass
        elif self.options.keyrings.value == 2:
            keyring_dungeons = self.random.choices(list(KEY_COUNTS.keys()), k=self.random.randint(0, len(KEY_COUNTS)))
            # print(f"Choice: {keyring_dungeons}")
            res |= {f"Keyring ({dung})": 1 for dung in keyring_dungeons}
            res |= {f"Small Key ({dung})": count for dung, count in KEY_COUNTS.items() if dung not in keyring_dungeons}
        elif self.options.keyrings.value == 1:
            res |= {f"Keyring ({dung})": 1 for dung in KEY_COUNTS.keys()}
            keyring_dungeons = list(KEY_COUNTS.keys())
        else:
            res |= {f"Small Key ({dung})": count for dung, count in KEY_COUNTS.items()}

        # Boss Keys
        if self.options.randomize_boss_keys.value not in [0, 3]:
            if self.options.boss_keyrings.value:
                res |= {f"Boss Key ({dung})": 1 for dung in BOSS_KEY_DUNGEONS if dung not in keyring_dungeons}
            else:
                res |= {f"Boss Key ({dung})": 1 for dung in BOSS_KEY_DUNGEONS}

        # Exceptions
        if not self.options.boss_keyrings and "Temple of Wind" in keyring_dungeons:
            res["Keyring (Temple of Wind)"] = 0
            res["Small Key (Temple of Wind)"] = 1

        filler_change = 0
        if (self.options.accessibility.value in [0, 1]  # full accessibility
                and self.options.keysanity == "in_own_dungeon"
                and "Mountain Passage" not in keyring_dungeons):
            res["Small Key (Mountain Passage)"] = 1
            filler_change = -2
            for loc_name in ["Mountain Passage 1F Entrance Chest", "Mountain Passage 2F Rat Key"]:
                forced_item = self.create_item("Small Key (Mountain Passage)")
                self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)

        # Filter out removed dungeon items
        if self.options.exclude_non_required_dungeons.value == 2:
            for item, count in res.copy().items():
                # print(f"dungeon: {item.split('(')[1][:-1]} from {item}")
                if item.split("(")[1][:-1] in self.excluded_dungeons:
                    res.pop(item)

        # print(f"Key Items: {res}")
        return res, filler_change

    def choose_ship_items(self) -> dict[str, int]:
        res: dict[str, int] = {}
        if self.options.starting_ship.value == -1:
            self.options.starting_ship.value = self.random.randint(0, 8)
        starting_ship = self.options.starting_ship.value

        if self.options.ship_items.value == 1:
            whole_ship_pool = list(ITEM_GROUPS["Whole Ships"].copy())
            whole_ship_pool.sort(key=lambda s: ITEMS[s].ship)
            if starting_ship >= 0:
                whole_ship_pool.pop(self.options.starting_ship.value)
            res = {i: 1 for i in whole_ship_pool}

        if self.options.ship_items.value == 3:  # Progressive ship
            if starting_ship == -2:
                self.options.starting_ship.value = starting_ship = 0
            included_ships = range(starting_ship+1, 9)
            self.ship_part_order: list[list[int]] = [[i]*8 for i in included_ships]
            res = {"Ship (Progressive)": len(included_ships)}

        elif self.options.ship_items.value == 2 or self.options.starting_ship.value == -2:
            included_ships = list(range(9))
            if starting_ship >= 0:
                included_ships.remove(starting_ship)
            part_positions: list[list[int]] = [included_ships.copy() for _ in range(8)]
            [self.random.shuffle(i) for i in part_positions]
            # print(f"ship part positions: {part_positions}")
            ship_part_order: list[list[int]] = [[] for _ in included_ships]
            # print(f"pre order {ship_part_order}")
            for part in part_positions:
                for i, ship_model in enumerate(part):
                    ship_part_order[i].append(ship_model)
            # print(f"ship part order: {ship_part_order}")
            self.ship_part_order = ship_part_order
            if self.options.ship_items.value == 2:
                res = {"Ship: Mismatched": 8}

        return res

    def create_items(self):
        item_pool_dict = self.build_item_pool_dict()
        self.get_extra_filler_items(item_pool_dict)
        # print(f"Extra Filler Items {self.extra_filler_items}")
        items = []
        for item_name, quantity in item_pool_dict.items():
            for _ in range(quantity):
                items.append(self.create_item(item_name))
        self.filter_confined_dungeon_items_from_pool(items)
        self.multiworld.itempool.extend(items)

    def get_extra_filler_items(self, item_pool_dict):
        # Create a random list of useful or currency items to turn into filler to satisfy all removed locations
        filler_count = 0
        extra_items_list = []
        for item, count in item_pool_dict.items():
            if 'backup_filler' in ITEMS[item].tags:
                extra_items_list.extend([item] * count)
            if ITEMS[item].classification in [ItemClassification.filler, ItemClassification.trap]:
                filler_count += count
            # Add sand of hours to extra filler list only if not progression
            if self.options.ph_time_logic > 2:
                if item in ["Sand of Hours", "Heart Container"]:
                    extra_items_list.extend([item] * count)
            # Add hearts if their time is zero
            if item == "Heart Container" and self.options.ph_heart_time == 0:
                extra_items_list.extend([item] * count)

        excluded_locations = self.locations_to_exclude | self.options.exclude_locations.value
        extra_item_count = len(excluded_locations) - filler_count + 25
        # print(f"Excluded locs: {excluded_locations}")
        # print(f"Filler items basic: {len(excluded_locations)} | have: {filler_count} | "
        #       f"available: {len(extra_items_list)} | creating: {extra_item_count}")

        # since item pool is created before items are filtered to dungeon pool,
        # remove the worst case scenario for excluded key items to lighten the pool
        ed = len(self.excluded_dungeons)
        # extra_item_count -= ([0] + list(range(8)))[ed] if self.options.randomize_boss_keys.value != 2 else 0  # boss keys iod
        # extra_item_count -= [0, 0, 0, 1, 3, 6, 9, 12][ed] if self.options.keysanity.value in [0, 1] else 0  # keys iod
        # extra_item_count -= [0, 0, 0, 0, 0, 0, 1, 3][ed] if (self.options.randomize_pedestal_items.value in [0, 1, 2]
        #                                                      and self.options.pedestal_item_options in [0, 1]) else 0
        # extra_item_count -= ed if not self.options.require_specific_bosses else 0  # boss rewards on rsb
        if self.options.shuffle_bosses == 1 and not self.options.decouple_entrances:  # boss exclusion happens later
            extra_item_count += [0, 5, 10, 14, 18, 21, 24, 27][ed]  # worst case boss room + post dungeon locs

        # print(f"Filler items advanced: {extra_item_count}")
        if extra_item_count > 0:
            self.random.shuffle(extra_items_list)
            self.extra_filler_items = extra_items_list[:extra_item_count]

    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        self.pre_fill_boss_rewards()
        self.pre_fill_dungeon_items()

    def filter_confined_dungeon_items_from_pool(self, items: List[PhantomHourglassItem]):
        confined_dungeon_items = []

        # Confine small keys to own dungeon if option is enabled
        if self.options.keysanity == "in_own_dungeon":
            confined_dungeon_items.extend([item for item in items if item.name.startswith("Small Key") or item.name.startswith("Keyring")])
        # Confine small keys to own dungeon if option is enabled
        if self.options.randomize_boss_keys == "in_own_dungeon":
            confined_dungeon_items.extend([item for item in items if item.name.startswith("Boss Key")])
        if self.options.randomize_pedestal_items == "in_own_dungeon":
            confined_dungeon_items.extend([item for item in items if item.name in ITEM_GROUPS["Pedestal Items"]])
        # Remove boss reward items from pool for pre filling
        boss_items = self.boss_reward_items_pool.copy()
        for item in items:
            if item.name in boss_items:
                confined_dungeon_items.append(item)
                boss_items.remove(item.name)

        for item in confined_dungeon_items:
            items.remove(item)
        self.pre_fill_items.extend(confined_dungeon_items)

    def pre_fill_boss_rewards(self):
        if self.is_ut:
            print(f"UT is creating boss rewards! stop it!")
        # Pre-fill dungeon rewards
        if self.options.goal_requirements == "defeat_bosses":
            boss_reward_locations = [loc for loc in self.multiworld.get_locations(self.player)
                                     if loc.name in self.required_bosses]
            boss_reward_items = [self.create_item(item) for item in self.boss_reward_items_pool]

            # Remove from the all_state the items we're about to place
            for item in boss_reward_items:
                self.pre_fill_items.remove(item)

            collection_state = self.multiworld.get_all_state()
            # Perform a prefill to place confined items inside locations of this dungeon
            self.random.shuffle(boss_reward_locations)
            # print(f"Pre-Filling boss rewards: {boss_reward_locations} \n {boss_reward_items}")
            fill_restrictive(self.multiworld, collection_state, boss_reward_locations, boss_reward_items,
                             single_player_placement=True, lock=True, allow_excluded=True)

    def pre_fill_dungeon_items(self):
        if self.is_ut:
            print(f"UT is creating dungeon items! stop it!")

        global_crystal_dungeons = {}
        def global_pedestal_helper(crystal, dungeon):
            global_crystal_dungeons.setdefault(dungeon, [])
            item = crystal + " Crystals"
            if dungeon in self.excluded_dungeons:
                global_crystal_dungeons["Temple of the Ocean King"].append(item)
            else:
                global_crystal_dungeons[self.random.choice(["Temple of the Ocean King", dungeon])].append(item)

        # Since crystals can be in multiple dungeons with global crystals,
        # and them ending up in excluded dungeons causes errors,
        # pre-choose what dungeon they belong to
        if (self.options.randomize_pedestal_items == "in_own_dungeon"
                and self.options.pedestal_item_options == "open_globally"):
            global_crystal_dungeons.setdefault("Temple of the Ocean King", [])
            global_pedestal_helper("Square", "Temple of Courage")
            global_pedestal_helper("Round", "Ghost Ship")
            global_pedestal_helper("Triangle", "Ghost Ship")
        # print(f"global crystal dungeons: {global_crystal_dungeons}")

        # If keysanity is off, dungeon items can only be put inside local dungeon locations, and there are not so many
        # of those which makes them pretty crowded.
        # This usually ends up with generator not having anywhere to place a few small keys, making the seed unbeatable.
        # To circumvent this, we perform a restricted pre-fill here, placing only those dungeon items
        # before anything else.
        for dung_name in DUNGEON_NAMES:
            # print(f"pre-filling {dung_name}")
            # Build a list of locations in this dungeon
            dungeon_location_names = [name for name, loc in LOCATIONS_DATA.items()
                                      if "dungeon" in loc and loc["dungeon"] == dung_name
                                      and name not in self.required_bosses]
            if self.options.shuffle_bosses:  # Exclude boss room if boss shuffling
                dungeon_location_names = [i for i in dungeon_location_names if i not in LOCATION_GROUPS.get(BOSS_LOOKUP.get(dung_name, None), [])]
            dungeon_locations = [loc for loc in self.multiworld.get_locations(self.player)
                                 if loc.name in dungeon_location_names and not loc.locked]

            # From the list of all dungeon items that needs to be placed restrictively, only filter the ones for the
            # dungeon we are currently processing.
            confined_dungeon_items = [item for item in self.pre_fill_items
                                      if item.name.endswith(f"({dung_name})")]

            # Add global crystals/force gems
            if dung_name in global_crystal_dungeons:
                confined_dungeon_items.extend([item for item in self.pre_fill_items if item.name in global_crystal_dungeons[dung_name]])

            # Add force gems
            if self.options.randomize_pedestal_items == "in_own_dungeon" and dung_name == "Temple of the Ocean King":
                confined_dungeon_items.extend([item for item in self.pre_fill_items
                                          if "Force Gem" in item.name])

            if len(confined_dungeon_items) == 0:
                continue  # This list might be empty with some keysanity options

            # Remove from the all_state the items we're about to place
            for item in confined_dungeon_items:
                self.pre_fill_items.remove(item)
            collection_state = self.multiworld.get_all_state()
            # Perform a prefill to place confined items inside locations of this dungeon
            # print(f"Pre fill locs: {dungeon_locations}")
            self.random.shuffle(dungeon_locations)

            # print(f"items {confined_dungeon_items}")
            fill_restrictive(self.multiworld, collection_state, dungeon_locations, confined_dungeon_items,
                             single_player_placement=True, lock=True, allow_excluded=True)

    def get_filler_item_name(self) -> str:
        filler_item_names = [
            "Blue Rupee (5)",
            "Red Rupee (20)",
            "Rupoor (-10)"
        ]
        filler_item_names += ITEM_GROUPS["Treasure Items"]
        filler_item_names += ITEM_GROUPS["Ammo Refills"]
        filler_item_names += ITEM_GROUPS["Potions"]
        if self.options.randomize_fishing:  # If fishing is enable add useless fish to filler pool cause funny :3
            filler_item_names += ["Fish: Skippyjack", "Fish: Toona"]
        if self.options.randomize_salvage:
            filler_item_names += ["Salvage Repair Kit"]
        if self.options.randomize_beedle_membership:
            filler_item_names += ["Compliment Card"]

        item_name = self.random.choice(filler_item_names)
        return item_name

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        player_hint_data = dict()

        pairings = dict()
        if self.er_placement_state:
            for e1, e2 in self.er_placement_state.pairings + self.manual_er_pairings + self.plando_er_pairings:
                pairings[ENTRANCES[e1].id] = ENTRANCES[e2].id
        if not pairings:  # If not er, don't bother trying anything else
            return

        def create_hint_entrances(key):
            hint_entrances = loc_data[key]
            hint_entrances = [hint_entrances] if isinstance(hint_entrances, str) else hint_entrances
            hint_entrances_ids = [e.id for name, e in ENTRANCES.items() if name in hint_entrances]

            for entrance_id in hint_entrances_ids:
                reverse_id = reverse_pairings.get(entrance_id, None)
                if reverse_id is not None and (reverse_id not in dead_end_ids or self.options.decouple_entrances):
                    entrance_list.add(entrance_id_to_entrance[reverse_id].name)

        reverse_pairings = {e2: int(e1) for e1, e2 in pairings.items()}
        dead_end_ids = [e.id for name, e in ENTRANCES.items() if name in DEAD_END_ENTRANCES]

        for loc, loc_data in LOCATIONS_DATA.items():
            if loc_data.hint_entrance:
                entrance_list = set()
                create_hint_entrances("hint_entrance")
                if not entrance_list and loc_data.hint_entrance_secondary:
                    create_hint_entrances("hint_entrance_secondary")

                if entrance_list:
                    player_hint_data[loc_data.id] = ", ".join(entrance_list)

        hint_data[self.player] = player_hint_data

    def collect(self, state: CollectionState, item: Item) -> bool:
        # Code borrowed from Ishigh's early Rule Builder implementation
        change = super().collect(state, item)
        if not change:
            return False

        mapping = self.item_mapping_collect.get(item.name, None)
        if mapping is not None and (item.classification & ItemClassification.progression):
            # if item.name.endswith("Pack"):
            #     print(f"Mapping {mapping} {state.prog_items[self.player][mapping[0]]+5} for item {item.name}")
            state.prog_items[self.player][mapping[0]] += mapping[1]

        return True

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if not change:
            return False

        mapping = self.item_mapping_collect.get(item.name, None)
        if mapping is not None:
            state.prog_items[self.player][mapping[0]] -= mapping[1]

        return True

    def get_location_models(self):
        # get item placement models to send to client
        location_models = {}
        for loc in self.get_locations():
            item = loc.item
            if item is None: continue
            loc_data = LOCATIONS_DATA.get(loc.name, None)
            if not loc_data or not (loc_data.chest_offset is not None or loc_data.gift_addr or loc_data.shop_model):
                # print(f"Failed: {loc} {item} | {loc_data.shop_model} {loc_data.gift_addr} {loc_data.chest_offset}")
                continue  # add dig_spot to this check to enable dig model swaps when ready

            if item.game in ["Phantom Hourglass"]:
                if ITEMS[item.name].model is not None and not (item.name.startswith("Treasure Map") and loc_data.shop_model):
                    location_models[loc_data.id] = ITEMS[item.name].model
                    continue
                elif loc_data.dig_spot:
                    if ITEMS[item.name].model in DIG_MODELS:
                        location_models[loc_data.id] = ITEMS[item.name].model
                        continue

            if loc_data.dig_spot: # default for digs is 0x9, so don't set force gems
                continue
            if item.classification & ItemClassification.progression or item.classification & ItemClassification.useful:
                location_models[loc_data.id] = 0x1E  # blue force gem
            else:
                location_models[loc_data.id] = 0x1D  # red force gem

        # print(f"Location Models: {location_models}")
        return location_models

    # def post_fill(self) -> None:
    #     self.get_location_models()

    def fill_slot_data(self) -> dict:
        options = [
            # Goal
            "goal_requirements", "bellum_access", "boss_reward_pool",
            # Dungeons
            "dungeons_required", "require_specific_bosses", "exclude_non_required_dungeons",
            "ghost_ship_in_dungeon_pool", "totok_in_dungeon_pool",
            # Metal Hunt
            "metal_hunt_total", "metal_hunt_required", "zauz_required_metals",
            # Logic
            "logic", "phantom_combat_difficulty", "boat_requires_sea_chart",
            # Item Randomization
            "boss_keyrings",
            "shopsanity", "shield_in_pool",
            "randomize_minigames", "randomize_digs", "randomize_fishing",
            "keysanity", "randomize_boss_keys", "randomize_pedestal_items",
            "randomize_frogs", "randomize_salvage",
            "randomize_triforce_crest", "randomize_harrow",
            # Beedle randomization
            "randomize_masked_beedle", "randomize_beedle_membership",
            # World Settings
            "map_warp_options", "open_post_dungeons",
            "fog_settings", "skip_ocean_fights",
            "dungeon_shortcuts", "totok_checkpoints",
            "color_switch_behaviour", "pedestal_item_options",
            # Spirit Packs
            "spirit_gem_packs", "additional_spirit_gems",
            # Hint settings
            "dungeon_hint_type", "dungeon_hint_location", "excluded_dungeon_hints",
            "shop_hints", "spirit_island_hints",
            # PH settings
            "ph_time_logic", "ph_starting_time", "ph_time_increment", "ph_heart_time", "ph_required",
            # ships
            "starting_ship", "ship_items", "equip_ship",
            # Cosmetic
            "additional_metal_names", "chest_cutscene_skips",
            # ER
            "shuffle_dungeon_entrances", "shuffle_ports", "shuffle_caves", "shuffle_houses",
            "shuffle_overworld_transitions", "shuffle_bosses",
            "entrance_directionality", "decouple_entrances",
            # UT
            "ut_events", "ut_blocked_entrances_behaviour", "ut_smart_keys",
            # Deathlink
            "death_link"
        ]
        slot_data = self.options.as_dict(*options)
        slot_data["player_id"] = self.player

        # Used to make excluded dungeons consistent for UT
        slot_data["required_dungeons"] = self.required_dungeons
        # Used to determine if reached goal in client
        slot_data["required_metals"] = self.required_metals
        slot_data["removed_dungeons"] = self.excluded_dungeons if self.options.exclude_non_required_dungeons.value == 2 else []
        # Used for dungeon hints in client
        slot_data["required_dungeon_locations"] = self.required_bosses  # for dungeon hints
        slot_data["boss_reward_items_pool"] = self.boss_reward_items_pool
        slot_data["treasure_price_index"] = self.treasure_price_index
        slot_data["location_models"] = self.get_location_models()
        slot_data["removed_locations"] = [self.location_name_to_id[i] for i in self.locations_to_remove]
        slot_data["ship_part_order"] = self.ship_part_order

        # Create ER Pairings, as ids to save space
        pairings = {}
        if self.er_placement_state:
            for e1, e2 in self.er_placement_state.pairings + self.manual_er_pairings + self.plando_er_pairings:
                pairings[ENTRANCES[e1].id] = ENTRANCES[e2].id
        slot_data["er_pairings"] = pairings
        return slot_data

    def write_spoiler(self, spoiler_handle):
        spoiler_handle.write(f"\n")
        if self.options.goal_requirements == "defeat_bosses":
            spoiler_handle.write(f"\nRequired Dungeons ({self.multiworld.player_name[self.player]}):\n")
            for dung in self.required_dungeons:
                spoiler_handle.write(f"\t- {dung}\n")

        if self.excluded_dungeons:
            spoiler_handle.write(f"\nExcluded Dungeons ({self.multiworld.player_name[self.player]}):\n")
            for dung in self.excluded_dungeons:
                spoiler_handle.write(f"\t- {dung}\n")

        if self.options.goal_requirements == "defeat_bosses" and self.options.shuffle_bosses:
            spoiler_handle.write(f"\nRequired Bosses ({self.multiworld.player_name[self.player]}):\n")
            for boss in self.required_bosses:
                spoiler_handle.write(f"\t- {boss}\n")

        if self.er_placement_state.pairings:
            spoiler_handle.write(f"\n\nEntrance Rando ({self.multiworld.player_name[self.player]}):\n")
            prev = None
            arrow = "=>" if self.options.decouple_entrances else "<=>"
            for i in self.er_placement_state.pairings + self.manual_er_pairings + self.plando_er_pairings:
                if (i[1], i[0]) != prev or self.options.decouple_entrances:
                    text = i[0] + f" {arrow} " + i[1]
                    spoiler_handle.write(f"\t{text}\n")
                prev = i


    # UT stuff
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]):
        return slot_data

    # UT reconnect entrances
    def reconnect_found_entrances(self, key, stored_data):
        print(f"UT Tried to defer entrances! key {key}"
              f" {stored_data}"
              )

        if getattr(self.multiworld, "enforce_deferred_connections", "default") == "off":
            print(f"Don't defer entrances when off")

        elif "ph_checked_entrances" in key or "ph_traversed_entrances" in key:
            if stored_data:
                if "ph_traversed_entrances" in key:
                    self.ut_traversed_entrances.update(stored_data)
                # always_connect_checked = set(stored_data) if "ph_checked_entrances" in key else set()

                disconnects = self.ut_redisconnected_entrances - self.ut_traversed_entrances
                reconnects = {i for i in self.ut_redisconnected_entrances & self.ut_traversed_entrances if i not in self.ut_reconnected_entrances}
                new_entrances = (set(stored_data) - self.ut_connected_entrances - disconnects) | reconnects
                if reconnects:
                    self.ut_reconnected_entrances.update(reconnects)

                print(f"new checked entrances: {new_entrances}")

                for i in new_entrances:
                    pairing = self.ut_pairings.get(str(i), None)
                    entr = entrance_id_to_entrance[i]
                    # print(f"Pairing {pairing} {entrance_id_to_entrance[i].name}")
                    # print(f"UT pairings {self.ut_pairings}")

                    if "silent_event" in entr.extra_data:
                        print(f"Connecting silent entrance: {entr.entrance_region} -> {entr.exit_region}")
                        self.get_region(entr.entrance_region).connect(self.get_region(entr.exit_region))
                    elif pairing is not None:
                        exit_name = entrance_id_to_entrance[i].name
                        _exit: "Entrance" = self.get_entrance(entrance_id_to_entrance[i].name)
                        entrance_region: "Region" = self.get_region(entrance_id_to_region[pairing])
                        print(f"Connecting: {_exit} => {entrance_region} | {i}: {pairing}")
                        _exit.connect(entrance_region)

                        if exit_name in BOSS_EVENT_TO_LOCATION:
                            print(f"Globally connecting menu => {_exit.parent_region}")
                            self.get_region("Menu").connect(_exit.parent_region)

                        if "silent_event" in ENTRANCES[exit_name].extra_data:
                            from rule_builder.rules import True_
                            print(f"Setting blank rule for silent entrance {_exit} -> {entrance_region}")
                            self.set_rule(_exit, True_())

                self.ut_connected_entrances |= new_entrances

        elif "ph_disconnect_entrances" in key and stored_data:
            self.ut_redisconnected_entrances.update(stored_data)
            for e in self.entrances.values():
                entr_id = ENTRANCES[e.name].id
                if (entr_id in stored_data and e.parent_region and e.connected_region
                        and entr_id in self.ut_connected_entrances
                        and entr_id not in self.ut_traversed_entrances):
                    print(f"Disconnecting {e.name}")
                    child_region = e.connected_region
                    parent_region = e.parent_region

                    # disconnect the edge
                    child_region.entrances.remove(e)
                    e.connected_region = None
                    # Create target
                    parent_region.create_er_target(e.name)


        if "ph_keylocking" in key and stored_data:
            print(f"Attempting to keylock stuff!")
            for i in stored_data:
                print(f"Excluding {self.location_id_to_name[i]}")
                self.multiworld.get_location(self.location_id_to_name[i], self.player).progress_type = LocationProgressType.EXCLUDED

        if "ph_ut_events" in key and stored_data and self.settings['ut_get_logical_path_shortcuts']:
            # Used to create an event item for specific tracker logic
            def manage_ut_event(stored_name, region_name, event_item_name):
                if stored_name in stored_data and not stored_name in self.ut_created_events:
                    print(f"UT is Creating {event_item_name} event")
                    self.create_event(region_name, event_item_name)
                    self.ut_created_events.append(stored_name)

            # Used when event is only used for get_logical_path. inspired by codegorilla's crystalis implementation
            def connect_existing_regions(stored_name, reg1, reg2, name=None):
                if stored_name in stored_data and not stored_name in self.ut_created_events:
                    try:
                        entr = self.get_entrance(f"{reg1} -> {reg2}")
                        print(f"Entrance exists, removing rule")
                        entr.access_rule = lambda state: True
                    except KeyError:
                        print(f"Entrance does not exist, creating it anew")
                        self.get_region(reg1).connect(self.get_region(reg2), name)
                    self.ut_created_events.append(stored_name)

            manage_ut_event("1f", "TotOK 1F Chart", "_UT_got_chart")
            for event_tag in stored_data:
                if event_tag in hidden_event_connect:
                    connect_existing_regions(event_tag, *hidden_event_connect[event_tag])