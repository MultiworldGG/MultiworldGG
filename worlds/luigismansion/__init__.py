# Python related Imports
import os, threading
from dataclasses import fields
from typing import ClassVar

# AP Related Imports
import Options
from BaseClasses import ItemClassification, Item
from Utils import visualize_regions, local_path
from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess, icon_paths

# Relative Imports
from .Items import LMItem, LMItemData, ALL_ITEMS_TABLE, BOO_ITEM_TABLE, ITEM_TABLE, get_item_names_per_category
from .LM_Web import LMWeb
from .Locations import *
from .LuigiOptions import *
from .Hints import get_hints_by_option, ALWAYS_HINT, PORTRAIT_HINTS
from .Regions import *
from .Rules import *
from .Rules import set_element_rules
from .iso_helper.LM_Rom import LMPlayerContainer
from .client.luigismansion_settings import LuigisMansionSettings
from .client.constants import CLIENT_VERSION, AP_WORLD_VERSION_NAME, RANDOMIZER_NAME

if TYPE_CHECKING:
    from NetUtils import MultiData

def run_client(*args):
    from .LMClient import main  # lazy import
    launch_subprocess(main, name="LuigiMansionClient", args=args)

# Adds the launcher for our component and our client logo.
components.append(
    Component("Luigi's Mansion Client", func=run_client, component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".aplm"), icon="archiboolego"))
icon_paths["archiboolego"] = f"ap:{__name__}/data/archiboolego.png"

class LMWorld(World):
    """
    Luigi's Mansion is an adventure game starring everyone's favorite plumber brother, Luigi.
    Luigi has won a strange mansion but upon arriving, he discovers it's full of ghosts, with his brother inside!
    Armed with the mysterious Poltergust 3000, Luigi will need to overcome his fears to kick the ghosts out
    before he can move in and save Mario!
    """

    game: ClassVar[str] = RANDOMIZER_NAME
    options_dataclass = LuigiOptions.LMOptions
    options: LuigiOptions.LMOptions

    topology_present = True
    item_name_to_id: ClassVar[dict[str, int]] = {
        name: LMItem.get_apid(data.code) for name, data in ALL_ITEMS_TABLE.items() if data.code is not None
    }
    location_name_to_id: ClassVar[dict[str, int]] = {
        name: LMLocation.get_apid(data.code) for name, data in ALL_LOCATION_TABLE.items() if data.code is not None
    }
    settings: ClassVar[LuigisMansionSettings]
    item_name_groups = get_item_names_per_category()
    required_client_version = (0, 6, 6)
    web = LMWeb()

    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml

    # Adding these to be able to grab from other classes, such as test classes
    ghost_affected_regions: dict[str, str]
    open_doors: dict[int, int]
    hints: dict[str, dict[str, str]]
    boo_spheres: dict[str, int]
    silver_portrait_upgrades: dict[str, int]
    gold_portrait_upgrades: dict[str, int]
    portrait_ghost_health: dict [str, int]

    # Adding all filler dict to be used later on
    all_filler_dict: dict[str, int]
    trap_filler_dict: dict[str, int]
    other_filler_dict: dict[str, int]

    # Additional Upgrade Count Lists used to calculate how many upgrades Gold/Silver needs.
    # Without this, UT will not be able to calculate the required amount of upgrades properly.
    silver_original_counts: list[int]
    gold_original_counts: list[int]

    def __init__(self, *args, **kwargs):
        super(LMWorld, self).__init__(*args, **kwargs)
        self.ghost_affected_regions = copy.deepcopy({key: val.element_type for (key, val) in REGION_LIST.items() if val.element_type})
        self.open_doors: dict[int, int] = copy.deepcopy(vanilla_door_state)
        self.origin_region_name: str = "Foyer"
        # If hints for other peoples worlds are enabled or need to calculate boo health by sphere
        self.finished_post_generation = threading.Event()
        self.boo_spheres = {}
        self.silver_portrait_upgrades = {}
        self.gold_portrait_upgrades = {}
        self.silver_original_counts = []
        self.gold_original_counts = []
        self.portrait_ghost_health = {}
        self.hints = {}
        self.spawn_full_locked: bool = False
        self.local_early_key: str = ""
        self.all_filler_dict = {}
        self.trap_filler_dict = {}
        self.other_filler_dict = {}

    @staticmethod
    def interpret_slot_data(slot_data):
        # There are more clever ways to do this, but all would require much larger changes
        return slot_data  # Tell UT that we have logic to fix

    def _set_optional_locations(self):
        # Set the flags for progression location by checking player's settings
        if self.options.WDYM_checks:
            for location, data in WDYM_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if data.require_poltergust:
                    add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                set_element_rules(self, entry, False)
                region.locations.append(entry)
        if self.options.toadsanity:
            for location, data in TOAD_LOCATION_TABLE.items():
                # If location is starting room toad, assign to starting room. Otherwise proceed as normal
                if location == "Starting Room Toad":
                    region = self.get_region(self.origin_region_name)
                else:
                    region = self.get_region(data.region)
                entry: LMLocation = LMLocation(self.player, location, region, data)
                set_element_rules(self, entry, True)
                region.locations.append(entry)
        if "Full" in self.options.furnisanity.value:
            for location, data in FURNITURE_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if data.require_poltergust:
                    add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                if data.code in (603,604,605,606,607,608,609): #Specifically the Artist's Easels require element rules
                    set_element_rules(self, entry, True)
                else:
                    set_element_rules(self, entry, False)
                region.locations.append(entry)
        else:
            location_dict: dict[str, LMLocationData] = {}
            if self.options.game_mode.value == 1:
                for name, loc_data in FURNITURE_LOCATION_TABLE.items():
                    if not loc_data.require_poltergust:
                        location_dict.update({name: loc_data})

            for group in sorted(self.options.furnisanity.value):
                match group:
                    case "Ceiling":
                        location_dict = {
                            **location_dict,
                            **CEILING_LOCATION_TABLE
                        }
                    case "Decor":
                        location_dict = {
                            **location_dict,
                            **DECOR_LOCATION_TABLE
                        }
                    case "Hangables":
                        location_dict = {
                            **location_dict,
                            **HANGABLES_LOCATION_TABLE
                        }
                    case "Seating":
                        location_dict = {
                            **location_dict,
                            **SEATING_LOCATION_TABLE
                        }
                    case "Candles":
                        location_dict = {
                            **location_dict,
                            **CANDLES_LOCATION_TABLE
                        }
                    case "Surfaces":
                        location_dict = {
                            **location_dict,
                            **SURFACES_LOCATION_TABLE
                        }
                    case "Storage":
                        location_dict = {
                            **location_dict,
                            **STORAGE_LOCATION_TABLE
                        }
                    case "Drawers":
                        location_dict = {
                            **location_dict,
                            **DRAWERS_LOCATION_TABLE
                        }
                    case "Plants":
                        location_dict = {
                            **location_dict,
                            **PLANT_LOCATION_TABLE
                        }
                    case "Treasures":
                        location_dict = {
                            **location_dict,
                            **TREASURES_LOCATION_TABLE
                        }
                    case "Basement":
                        location_dict = {
                            **location_dict,
                            **BASEMENT_LOCS
                        }
                    case "1st Floor":
                        location_dict = {
                            **location_dict,
                            **FIRST_FLOOR_LOCS
                        }
                    case "2nd Floor":
                        location_dict = {
                            **location_dict,
                            **SECOND_FLOOR_LOCS
                        }
                    case "Attic":
                        location_dict = {
                            **location_dict,
                            **ATTIC_LOCS
                        }
                    case "Roof":
                        location_dict = {
                            **location_dict,
                            **ROOF_LOCS
                        }

            for location, data in location_dict.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if data.require_poltergust or region.name == self.origin_region_name:
                    add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                if data.code in (603,604,605,606,607,608,609): #Specifically the Artist's Easels require element rules
                    set_element_rules(self, entry, True)
                else:
                    set_element_rules(self, entry, False)
                region.locations.append(entry)
        if self.options.gold_mice:
            for location, data in GOLD_MICE_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Blackout", self.player), "and")
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                region.locations.append(entry)
        if self.options.speedy_spirits:
            for location, data in SPEEDY_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Blackout", self.player), "and")
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                region.locations.append(entry)
        if self.options.portrification:
            for location, data in PORTRAIT_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                if entry.region == "Twins' Room" and self.open_doors.get(28) == 0:
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                if data.region == "Fortune-Teller's Room": # If it's Clairvoya's room, should match Mario item count
                    add_rule(entry,
                             lambda state: state.has_group_unique("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                set_element_rules(self, entry, True)
                region.locations.append(entry)
        else:
            for location, data in PORTRAIT_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                entry.address = None
                entry.place_locked_item(Item("Portrait _Ghost", ItemClassification.progression, None, self.player))
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                if entry.region == "Twins' Room" and self.open_doors.get(28) == 0:
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                if data.region == "Fortune-Teller's Room": # If it's Clairvoya's room, should match Mario item count
                    add_rule(entry,
                             lambda state: state.has_group_unique("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                set_element_rules(self, entry, True)
                region.locations.append(entry)
        if self.options.silver_ghosts:
            # Set max required upgrades based on chosen max health value
            # @200, 350, 500, 650, 800 +1 upgrade
            # randomly choose a number of upgrades for a given portrait ghost.
            # After spheres, set health values based on sphere + number of upgrades compared to max value
            number_list: list[int] = self.portrait_health_by_sphere() if not self.silver_original_counts else self.silver_original_counts
            self.silver_original_counts = copy.deepcopy(number_list)
            for location, data in SILVER_PORTRAIT_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                if entry.code == 978 and self.open_doors.get(28) == 0:
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                if entry.code == 981:
                    add_rule(entry,
                             lambda state: state.has_group_unique("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                portrait_short_name = location.split("-")[0].split(" ", 1)[1].strip()
                location_name = [name for name in PORTRAIT_LOCATION_TABLE.keys() if portrait_short_name in name]
                if self.options.portrait_health_option.value == 2:
                    if entry.code not in (977, 985, 992):
                        upgrade_count = number_list.pop()
                        if upgrade_count > 0:
                            add_rule(entry, lambda state, up_count=upgrade_count: state.has("Vacuum Upgrade", self.player, up_count))
                        self.silver_portrait_upgrades.update({location_name[0]: upgrade_count})
                elif self.options.portrait_health_option.value < 2:
                    if entry.code not in (977, 985, 992):
                        portrait_short_name = location.split("-")[0].split(" ", 1)[1].strip()
                        location_name = [name for name in PORTRAIT_LOCATION_TABLE.keys() if portrait_short_name in name]
                        health = self.portrait_ghost_health[location_name[0]]
                        upgrade_count = math.floor(health / 200)
                        if upgrade_count > 0:
                            add_rule(entry, lambda state, up_count=upgrade_count: state.has("Vacuum Upgrade", self.player, up_count))
                set_element_rules(self, entry, True)
                region.locations.append(entry)
        if self.options.gold_ghosts:
            # Set max required upgrades based on chosen max health value
            # @130, 260, 390, 520, 650 +1 upgrade - cap max health at 600 if gold portraits are chosen
            # randomly choose a number of upgrades for a given portrait ghost.
            # After spheres, set health values based on sphere + number of upgrades compared to max value
            number_list: list[int] = self.portrait_health_by_sphere() if not self.gold_original_counts else self.gold_original_counts
            self.gold_original_counts = copy.deepcopy(number_list)
            for location, data in GOLD_PORTRAIT_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                if entry.code == 953 and self.open_doors.get(28) == 0: # Special logic for twins
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                if entry.code == 956: # Special logic for Clairvoya
                    add_rule(entry,
                             lambda state: state.has_group_unique("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                # Choose number of upgrades for each portrasit ghost if by sphere is on
                portrait_short_name = location.split("-")[0].split(" ", 1)[1].strip()
                location_name = [name for name in PORTRAIT_LOCATION_TABLE.keys() if portrait_short_name in name]
                if self.options.portrait_health_option.value == 2:
                    if entry.code not in (952, 960, 967):
                        upgrade_count = number_list.pop()
                        if entry.code in (962, 971): # Gold borders requiring Vac Upgrade
                            min_vac_count = min(5, upgrade_count+1, self.options.vacuum_upgrades.value)
                            add_rule(entry, lambda state, up_count=min_vac_count: state.has("Vacuum Upgrade", self.player, up_count))
                            self.gold_portrait_upgrades.update({location_name[0]: min_vac_count})
                        else:
                            if upgrade_count > 0:
                                add_rule(entry, lambda state, up_count=upgrade_count: state.has("Vacuum Upgrade", self.player, up_count))
                            self.gold_portrait_upgrades.update({location_name[0]: upgrade_count})
                elif self.options.portrait_health_option.value < 2:
                    if entry.code not in (952, 960, 967):
                        health = self.portrait_ghost_health[location_name[0]]
                        upgrade_count = math.floor(health/130)
                        if upgrade_count > 0:
                            add_rule(entry, lambda state, up_count=upgrade_count: state.has("Vacuum Upgrade", self.player, up_count))
                set_element_rules(self, entry, True)
                region.locations.append(entry)
        if self.options.lightsanity:
            for location, data in LIGHT_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if data.require_poltergust:
                    add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                if entry.region == "Twins' Room" and self.open_doors.get(28) == 0:
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                if data.region == "Fortune-Teller's Room": # If it's Clairvoya's room, should match Mario item count
                    add_rule(entry,
                             lambda state: state.has_group_unique("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                elif entry.code == 772: # If family hallway light
                    add_rule(entry, lambda state: state.can_reach_location("Nursery Clear Chest", self.player))
                elif entry.code == 773: # If 1F Hallway light
                    add_rule(entry, lambda state: state.can_reach_location("Graveyard Clear Chest", self.player))
                elif entry.code in (778, 782, 784, 789, 790, 851): # If any other hallway light
                    add_rule(entry, lambda state: state.can_reach_location("Balcony Clear Chest", self.player))
                elif entry.code == 757 and self.options.enemizer.value != 2: # If sitting room light
                    add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                set_element_rules(self, entry, True)
                region.locations.append(entry)
        if self.options.walksanity:
            for location, data in WALK_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if data.require_poltergust:
                    add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                set_element_rules(self, entry, False)
                region.locations.append(entry)
        if self.options.grassanity:
            for location, data in MEME_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if data.require_poltergust:
                    add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                set_element_rules(self, entry, False)
                region.locations.append(entry)
        if self.options.boosanity:
            for location, data in ROOM_BOO_LOCATION_TABLE.items():
                region: Region = self.get_region(data.region)
                entry: LMLocation = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Boo Radar", self.player), "and")
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                if entry.region == "Twins' Room" and self.open_doors.get(28) == 0:
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                elif data.region == "Nursery" and self.open_doors.get(27) == 0:
                    add_rule(entry, lambda state: state.has("Nursery Key", self.player), "and")
                elif data.region == "Fortune-Teller's Room": # If it's Clairvoya's room, should match Mario item count
                    add_rule(entry,
                             lambda state: state.has_group_unique("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                if entry.parent_region.name == self.origin_region_name:
                    if self.spawn_full_locked:
                        keys = REGION_LIST[self.origin_region_name].door_keys
                        add_rule(entry, lambda state: state.has_any(keys, self.player), "and")
                set_element_rules(self, entry, True)
                region.locations.append(entry)
            for location, data in BOOLOSSUS_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Ice Element Medal", self.player), "and")
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                region.locations.append(entry)
        else:
            for location, data in ROOM_BOO_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                entry.address = None
                entry.place_locked_item(Item("Boo", ItemClassification.progression, None, self.player))
                if self.options.boo_gates:
                    add_rule(entry, lambda state: state.has("Boo Radar", self.player), "and")
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                if entry.region == "Twins' Room" and self.open_doors.get(28) == 0:
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                elif data.region == "Nursery" and self.open_doors.get(27) == 0:
                    add_rule(entry, lambda state: state.has("Nursery Key", self.player), "and")
                elif data.region == "Fortune-Teller's Room": # If it's Clairvoya's room, should match Mario item count
                    add_rule(entry,
                             lambda state: state.has_group_unique("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                if entry.parent_region.name == self.origin_region_name:
                    if self.spawn_full_locked:
                        keys = REGION_LIST[self.origin_region_name].door_keys
                        add_rule(entry, lambda state: state.has_any(keys, self.player), "and")
                entry.code = None
                set_element_rules(self, entry, True)
                region.locations.append(entry)
            for location, data in BOOLOSSUS_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                entry.address = None
                entry.code = None
                entry.place_locked_item(Item("Boo", ItemClassification.progression, None, self.player))
                add_rule(entry, lambda state: state.has("Ice Element Medal", self.player), "and")
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
                region.locations.append(entry)

        rankcalc = 0
        if self.options.rank_requirement == 0:
            rankcalc = 0
        elif 1 < self.options.rank_requirement < 3:
            rankcalc = 1
        elif self.options.rank_requirement == 3:
            rankcalc = 2
        elif 3 < self.options.rank_requirement < 5:
            rankcalc = 3
        elif self.options.rank_requirement == 6:
            rankcalc = 4
        else:
            rankcalc = 5
        loc = self.get_location("King Boo")
        if rankcalc != 0 :
            add_rule(loc, lambda state: state.has("Gold Diamond", self.player, rankcalc), "and")
        add_rule(loc, lambda state: state.has("Poltergust 3000", self.player), "and")

    def portrait_health_by_sphere(self) -> list[int]:
        amount_per_group = math.floor(19 / (self.options.vacuum_upgrades.value + 1))
        remainder = math.ceil(19 % (self.options.vacuum_upgrades.value + 1))
        number_list: list[int] = []
        for i in range(self.options.vacuum_upgrades.value + 1):
            number_list += list([i for _ in range(amount_per_group)])
        for _ in range(remainder):
            number_list += [0]
        self.random.shuffle(number_list)
        return number_list

    def _set_ut_logic(self):
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if not self.game in self.multiworld.re_gen_passthrough:
                return False

            slot_data: dict = self.multiworld.re_gen_passthrough[self.game]
            self.options.rank_requirement.value = slot_data["rank requirement"]
            self.options.game_mode.value = slot_data["game mode"]
            self.options.vacuum_upgrades.value = slot_data["better vacuum"]
            self.options.vacuum_start.value = slot_data["vacuum start"]
            self.options.boo_radar.value = slot_data["boo radar"]
            self.options.door_rando.value = slot_data["door rando"]
            self.options.toadsanity.value = slot_data["toadsanity"]
            self.options.gold_mice.value = slot_data["gold_mice"]
            self.options.furnisanity.value = slot_data["furnisanity"]
            self.options.boosanity.value = slot_data["boosanity"]
            self.options.portrification.value = slot_data["portrait ghosts"]
            self.options.speedy_spirits.value = slot_data["speedy spirits"]
            self.options.lightsanity.value = slot_data["lightsanity"]
            self.options.walksanity.value = slot_data["walksanity"]
            self.options.mario_items.value = slot_data["clairvoya requirement"]
            self.options.boo_gates.value = slot_data["boo gates"]
            # self.options.washroom_boo_count.value = slot_data["washroom boo count"]
            self.options.balcony_boo_count.value = slot_data["balcony boo count"]
            self.options.final_boo_count.value = slot_data["final boo count"]
            self.options.enemizer.value = slot_data["enemizer"]
            self.options.luigi_max_health.value = slot_data["luigi max health"]
            self.origin_region_name = slot_data["spawn_region"]
            self.ghost_affected_regions = slot_data["ghost elements"]
            self.local_early_key = slot_data["local first key"]
            self.options.silver_ghosts.value = slot_data["silver rank"]
            self.options.gold_ghosts.value = slot_data["gold rank"]
            self.options.WDYM_checks.value = slot_data["WDYM"]
            self.options.grassanity.value = slot_data["grassanity"]

            # Needed to avoid option errors, otherwise they will randomly roll still.
            self.options.trap_link.value = slot_data["trap_link"],
            self.options.energy_link.value = slot_data["energy_link"],
            self.options.ring_link.value = slot_data["ring_link"]

            # Update Door list based on the slot's open/closed doors.
            self.open_doors = slot_data["door rando list"]  # this should be the same list from slot data
            self.open_doors = {int(k): v for k, v in self.open_doors.items()}

            spawn_doors = copy.deepcopy(REGION_LIST[self.origin_region_name].door_ids)
            if spawn_doors:
                for door in REGION_LIST[self.origin_region_name].door_ids:
                    if self.open_doors[door] == 0:
                        spawn_doors.remove(door)
                if not spawn_doors:
                    self.spawn_full_locked: bool = True

            # Various Portrait Ghost health related options.
            self.portrait_ghost_health = slot_data["portrait_health"]
            self.options.portrait_health_option.value = slot_data["portrait_ghost_health_option"]
            self.silver_original_counts = list(slot_data["silver_original_counts"])
            self.gold_original_counts = list(slot_data["gold_original_counts"])
            return True

        return False


    def generate_early(self):
        using_ut = self._set_ut_logic()

        if self.options.energy_link == 1 and self.options.ring_link == 1:
            raise Options.OptionError(f"In {RANDOMIZER_NAME}, both energy_link and ring_link cannot be enabled.\n"
                                      f"This error was found in {self.player_name}'s {RANDOMIZER_NAME} world."
                                      f"Their YAML must be fixed")

        if (self.options.boosanity == 1 or self.options.boo_gates == 1) and self.options.boo_radar == 2:
            raise Options.OptionError(f"When Boo Radar is excluded, neither Boosanity nor Boo Gates can be active.\n"
                                      f"This error was found in {self.player_name}'s {RANDOMIZER_NAME} world."
                                      f"Their YAML must be fixed")

        if self.options.game_mode.value == 1:
            self.options.vacuum_start.value = 0
            self.options.door_rando.value = 3

        if self.options.vacuum_start.value:
            self.multiworld.push_precollected(self.create_item("Poltergust 3000"))

        # If player wants to start with boo radar
        if self.options.boo_radar == 0:
            self.multiworld.push_precollected(self.create_item("Boo Radar"))

        if self.options.gold_ghosts.value == 1 and self.options.vacuum_upgrades.value < 1:
            self.options.vacuum_upgrades.value = 1

        # Anything below this is normal logic, so if using UT, can exit early.
        if using_ut:
            return

        # if hint distribution is vague, disabled, junk, do not send hints.
        if self.options.hint_distribution.value in (1, 4, 5):
            self.options.send_hints.value = 0

        if self.options.boosanity.value == 0 and self.options.balcony_boo_count.value > 31:
            self.options.balcony_boo_count.value = 31

        if self.options.random_spawn.value > 0:
            self.origin_region_name = self.random.choice(sorted([region_name for (region_name, region_data) in
                REGION_LIST.items() if region_data.allow_random_spawn]))

        # If spawn region is past Boolossus, make sure the gate is possible
        if self.origin_region_name in FLIP_BALCONY_BOO_EVENT_LIST:
            if self.options.balcony_boo_count.value > 4 and self.options.boosanity.value == 0:
                self.options.balcony_boo_count.value = 4

        if self.options.boo_gates.value == 0:
            self.options.final_boo_count.value = 0
            self.options.balcony_boo_count.value = 0
            # self.options.washroom_boo_count.value = 0

        if self.options.enemizer == 1:
            set_ghost_type(self, self.ghost_affected_regions)
        elif self.options.enemizer == 2:
            for key in self.ghost_affected_regions.keys():
                self.ghost_affected_regions[key] = "No Element"

        if self.options.door_rando == 1 or self.options.door_rando == 2:
            for key in  self.open_doors.keys():
                # If door is a suite_door, lock it in this option
                if self.options.door_rando.value == 2 and key in [3, 42, 59, 72]:
                    self.open_doors[key] = 0
                    continue
                self.open_doors[key] = self.random.choice(sorted([0,1]))
        elif self.options.door_rando.value == 3:
            for door_id in self.open_doors.keys():
                self.open_doors[door_id] = 1
        elif self.options.door_rando.value == 4:
            for door_id in self.open_doors.keys():
                self.open_doors[door_id] = 0

        spawn_doors = copy.deepcopy(REGION_LIST[self.origin_region_name].door_ids)
        if spawn_doors and self.origin_region_name != "Butler's Room":
            for door in REGION_LIST[self.origin_region_name].door_ids:
                if self.open_doors[door] == 0:
                    spawn_doors.remove(door)
            if not spawn_doors:
                self.spawn_full_locked: bool = True

        if self.options.early_first_key.value == 1:
            early_key = ""
            for key in REGION_LIST[self.origin_region_name].early_keys:
                key_data: LMItemData = ITEM_TABLE[key]
                if self.open_doors[key_data.doorid] == 0:
                    early_key = key
                    break
            if len(early_key) > 0:
                self.local_early_key = early_key
                self.multiworld.local_early_items[self.player].update({early_key: 1})

        if self.options.portrait_health_option.value == 0:
            for ghost, data in PORTRAIT_LOCATION_TABLE.items():
                if data.code == 638:
                    continue
                self.portrait_ghost_health.update({ghost: self.options.portrait_health_value.value})
        elif self.options.portrait_health_option.value == 1:
            for ghost, data in PORTRAIT_LOCATION_TABLE.items():
                if data.code == 638:
                    continue
                health = self.random.randint(1, self.options.portrait_health_value.value)
                self.portrait_ghost_health.update({ghost: health})
        elif self.options.portrait_health_option.value == 3:
            for ghost, data in PORTRAIT_LOCATION_TABLE.items():
                if data.code == 638:
                    continue
                self.portrait_ghost_health.update({ghost: 100})

        if self.options.gold_ghosts.value == 1 and self.options.portrait_health_option.value != 2:
            max_health = max(self.portrait_ghost_health.values())
            upgrade_count = min(5, math.floor(max_health / 130))
            if self.options.vacuum_upgrades.value < upgrade_count:
                self.options.vacuum_upgrades.value = upgrade_count
        elif self.options.silver_ghosts.value == 1 and self.options.portrait_health_option.value != 2:
            max_health = max(self.portrait_ghost_health.values())
            upgrade_count = min(5, math.floor(max_health / 200))
            if self.options.vacuum_upgrades.value < upgrade_count:
                self.options.vacuum_upgrades.value = upgrade_count

        self.trap_filler_dict: dict[str, int] = self.options.trap_weights.value

        self.other_filler_dict: dict[str, int] = {
            "20 Coins & Bills": self.options.filler_weights["Bundles"],
            "Sapphire": self.options.filler_weights["Gems"],
            "Emerald": self.options.filler_weights["Gems"],
            "Ruby": self.options.filler_weights["Gems"],
            "Diamond": math.ceil(self.options.filler_weights["Gems"] * 0.4),
            "Small Heart": self.options.filler_weights["Hearts"],
            "Large Heart":  max(0,self.options.filler_weights["Hearts"] - 5),
            "10 Coins": self.options.filler_weights["Coins"],
            "20 Coins": max(0,self.options.filler_weights["Coins"] - 5),
            "30 Coins": max(0,self.options.filler_weights["Coins"] - 10),
            "15 Bills": self.options.filler_weights["Bills"],
            "25 Bills": max(0,self.options.filler_weights["Bills"] - 5),
            "1 Gold Bar": self.options.filler_weights["Bars"],
            "2 Gold Bars": max(0,self.options.filler_weights["Bars"] - 5),
        }
        if self.options.grassanity.value == 1:
            self.other_filler_dict.update({"Grass": self.options.filler_weights["Dust"],})
        else:
            self.other_filler_dict.update({"Dust": self.options.filler_weights["Dust"],})

        self.all_filler_dict = {**self.trap_filler_dict, **self.other_filler_dict}

    def create_regions(self):
        # Add all randomizable regions
        for region_name in REGION_LIST.keys():
            self.multiworld.regions.append(LMRegion(region_name, REGION_LIST[region_name], self.player, self.multiworld))

        # Assign each location to their region
        for location, data in BASE_LOCATION_TABLE.items():
            # Set our special spawn locations to the spawn regions
            if data.code in (708, 853):
                region = self.get_region(self.origin_region_name)
            else:
                region = self.get_region(data.region)
            entry = LMLocation(self.player, location, region, data)
            if data.require_poltergust:
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
            set_element_rules(self, entry, False)
            if location == "Huge Flower (Boneyard)":
                add_rule(entry, lambda state: state.has("Progressive Flower", self.player, 3))
            if entry.code is None:
                entry.place_locked_item(Item(entry.locked_item, ItemClassification.progression, None, self.player))
            region.locations.append(entry)
        for location, data in ENEMIZER_LOCATION_TABLE.items():
            region = self.get_region(data.region)
            entry = LMLocation(self.player, location, region, data)
            add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
            set_element_rules(self, entry, True)
            region.locations.append(entry)
        for location, data in CLEAR_LOCATION_TABLE.items():
            region = self.get_region(data.region)
            entry = LMLocation(self.player, location, region, data)
            if data.require_poltergust:
                add_rule(entry, lambda state: state.has("Poltergust 3000", self.player), "and")
            # If it's Clairvoya's room chest, should match Mario item count.
            # Do not compare to region to keep rule correct for the Candles Key
            if data.code == 5:
                add_rule(entry,
                         lambda state: state.has_group_unique("Mario Item", self.player, self.options.mario_items.value))
            if entry.region == "Twins' Room" and self.open_doors.get(28) == 0:
                add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
            set_element_rules(self, entry, True)
            region.locations.append(entry)
        self._set_optional_locations()
        connect_regions(self)

    def create_item(self, item: str) -> LMItem:
        if (self.options.gold_ghosts.value == 1 or self.options.silver_ghosts.value == 1) and item == "Vacuum Upgrade":
            set_progress = True
        else:
            set_progress = False

        if item in ALL_ITEMS_TABLE.keys():
            return LMItem(item, self.player, ALL_ITEMS_TABLE[item], set_progress)
        raise Exception(f"Invalid item name: {item}")

    # def post_fill(self):
    #     visualize_regions(self.multiworld.get_region(self.origin_region_name, self.player), "luigiregions.puml", linetype_ortho=False)

    def create_items(self):
        from .Helper_Functions import LMDynamicAddresses
        lm_addresses: LMDynamicAddresses = LMDynamicAddresses()
        lm_addresses.update_item_addresses()

        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]
        if len(self.local_early_key) > 0:
            exclude += self.local_early_key
        loc_itempool: list[LMItem] = []
        if self.options.boosanity:
            for item, data in BOO_ITEM_TABLE.items(): # Always create 1 copy of each boo and not more
                for _ in range(max(0, 1 - exclude.count(item))):
                    loc_itempool.append(self.create_item(item))
        if self.options.boo_radar.value == 2:
            exclude += ["Boo Radar"]
        for item, data in ITEM_TABLE.items():
            copies_to_place = 1
            if data.doorid in self.open_doors.keys() and self.open_doors.get(data.doorid) == 1:
                exclude += [item]
            if item == "Gold Diamond": # Gold Diamonds
                copies_to_place = 5
            elif item == "Progressive Flower": # Progressive Flowers
                copies_to_place = 3
            elif item == "Vacuum Upgrade":
                    copies_to_place = self.options.vacuum_upgrades.value
            copies_to_place = max(0, copies_to_place - exclude.count(item))
            for _ in range(copies_to_place):
                loc_itempool.append(self.create_item(item))

        # Calculate the number of additional filler items to create to fill all locations
        n_locations = len(self.multiworld.get_unfilled_locations(self.player))
        n_items = len(loc_itempool)
        n_filler_items = n_locations - n_items
        n_trap_items = math.ceil(n_filler_items*(self.options.trap_percentage.value/100))
        n_other_filler = n_filler_items - n_trap_items

        if sum(self.trap_filler_dict.values()) > 0:# Add filler items to the item pool. Add traps if they are on.
            for _ in range(n_trap_items):
                loc_itempool.append(self.create_item(self.get_trap_item_name()))

            for _ in range(n_other_filler):
                loc_itempool.append(self.create_item((self.get_other_filler_item())))
        else:
            for _ in range(n_filler_items):
                loc_itempool.append(self.create_item((self.get_other_filler_item())))

        self.multiworld.itempool += loc_itempool

    def get_trap_item_name(self) -> str:
        filler_traps = dict(sorted(self.trap_filler_dict.items()))
        return self.random.choices(list(filler_traps.keys()), weights=list(filler_traps.values()), k=1)[0]


    def get_other_filler_item(self) -> str:
        if sum(self.other_filler_dict.values()) != 0:
            other_filler = dict(sorted(self.other_filler_dict.items()))
            return self.random.choices(list(other_filler.keys()), weights=list(other_filler.values()), k=1)[0]
        else:
            return "Dust" if self.options.grassanity.value == 0 else "Grass"

    # Used for ItemLink and overrides the one used by AP.
    def get_filler_item_name(self) -> str:
        if sum(self.all_filler_dict.values()) != 0:
            filler_dict = dict(sorted(self.all_filler_dict.items()))
            return self.random.choices(list(filler_dict.keys()), weights=list(filler_dict.values()), k=1)[0]
        else:
            return "Dust" if self.options.grassanity.value == 0 else "Grass"

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Mario's Painting", self.player)

    def post_fill(self) -> None:
        if self.options.boosanity:
            # Count number of trap items on these locations. Determine difference between total trap count and 8
            # then repick using other filler listing if difference is positive, equal to difference, and replace those items
            boolossus_locations: list[LMLocation] = []
            for location in BOOLOSSUS_LOCATION_TABLE.keys():
                boolossus_locations += [self.get_location(location)]
            trap_boolossus_list = [lm_loc for lm_loc in boolossus_locations if (lm_loc.item.classification ==
                ItemClassification.trap and lm_loc.item.player == self.player)]
            if len(trap_boolossus_list) > 8:
                trap_count = len(trap_boolossus_list) - 8
                for _ in range(trap_count):
                    loc = self.random.choice(trap_boolossus_list)
                    # Un-place the existing item.
                    loc.item.location = None
                    loc.item = None
                    # Place a new, replacement filler item.
                    self.multiworld.push_item(loc, self.create_item(self.get_other_filler_item()), False)
                    trap_boolossus_list.remove(loc)

    @classmethod # output_directory is required even though we don't use it
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str):
        # Filter for any Luigi's Mansion worlds that need hints or have boo health by sphere turned on
        hint_worlds = {world.player for world in multiworld.get_game_worlds(cls.game)
                       if (world.options.hint_distribution.value != 5 and world.options.hint_distribution.value != 1)}
        boo_worlds = {world.player for world in multiworld.get_game_worlds(cls.game)
                      if world.options.boo_health_option.value == 2}
        portrait_sphere_worlds = {world.player for world in multiworld.get_game_worlds(cls.game)
                      if world.options.portrait_health_option.value == 2}

        # Even if no worlds have any hints/boo worlds, always set the thread anyway as it won't hurt anything.
        try:
            if not boo_worlds and not hint_worlds and not portrait_sphere_worlds:
                return

            if hint_worlds:
                # Produce hints for LM games that need them
                get_hints_by_option(multiworld, hint_worlds)

            if portrait_sphere_worlds:
                portrait_health_sphere_things(multiworld, portrait_sphere_worlds)

            # Produce values for boo health for worlds the need them
            def check_boo_players_done() -> None:
                done_players = set()
                for player in boo_worlds:
                    player_lm_world = multiworld.worlds[player]
                    if len(player_lm_world.boo_spheres.keys()) == len(ROOM_BOO_LOCATION_TABLE.keys()):
                        done_players.add(player)
                boo_worlds.difference_update(done_players)
            if boo_worlds:
                for sphere_num, sphere in enumerate(multiworld.get_spheres(), 1):
                    for loc in sphere:
                        if loc.player in boo_worlds and loc.name in ROOM_BOO_LOCATION_TABLE.keys():
                            player_world = multiworld.worlds[loc.player]
                            player_world.boo_spheres.update({loc.name: sphere_num})
                        check_boo_players_done()

                    if not boo_worlds:
                        return
        except Exception:
            import traceback
            traceback.print_exc()
            raise
        finally:
            _set_gen_thread_finished(multiworld, cls.game)

    # Output options, locations and doors for patcher
    def generate_output(self, output_directory: str):
        if 'W' in self.multiworld.seed_name:
            ap_seed: str = str(self.multiworld.seed_name[1:])
        else:
            ap_seed: str = str(self.multiworld.seed_name)

        # Output seed name and slot number to seed RNG in randomizer client
        output_data: dict = {
            "Seed": ap_seed,
            "Slot": self.player,
            "Name": self.player_name,
            "Options": {},
            "Locations": {},
            "Entrances": self.open_doors,
            "Room Enemies": self.ghost_affected_regions,
            "Hints": {},
            "Portrait Health": {},
            AP_WORLD_VERSION_NAME: CLIENT_VERSION
        }

        # Output relevant options to file
        for field in fields(self.options):
            if field.name == "plando_items":
                continue
            output_data["Options"][field.name] = getattr(self.options, field.name).value

        # Output the spawn region name
        output_data["Options"]["spawn"]: str = self.origin_region_name

        # Wait for output thread to finish first.
        if ((self.options.hint_distribution != 5 and self.options.hint_distribution != 1) or
            self.options.boo_health_option.value == 2 or self.options.portrait_health_option.value == 2):
            self.finished_post_generation.wait()

        # If current world required hint distribution, update the output hint dict
        if self.options.hint_distribution != 5 and self.options.hint_distribution != 1:
            output_data["Hints"] = self.hints

        # We output the portrait health here in case option 2 (health by sphere) is chosen,
        #   which is after the above thread waiting.
        output_data["Portrait Health"] = self.portrait_ghost_health

        # Output which item has been placed at each location
        for location in list(lmloc for lmloc in self.get_locations() if isinstance(lmloc, LMLocation)):
            if location.address is None and not (location.name in ROOM_BOO_LOCATION_TABLE.keys()):
                continue

            if location.item.code is None:
                item_info = {
                    "player": location.item.player,
                    "name": location.item.name,
                    "game": self.game,
                    "classification": location.item.classification,
                    "door_id": 0, # Will always be 0 as an event item
                    "room_no": 0, # Will always be 0 as an event item
                    "map_id": 0, # Will always be 0 as an event item
                    "type": location.type,
                    "loc_enum": location.jmpentry, # Will always be 0 as an event item
                }
            elif location.item:
                loc_region: LMRegionInfo = REGION_LIST[location.parent_region.name]
                item_info = {
                    "player": location.item.player,
                    "name": location.item.name,
                    "game": location.item.game,
                    "classification": location.item.classification.name,
                    "room_no": loc_region.room_id,
                    "map_id": loc_region.map_id,
                    "type": location.type,
                    "loc_enum": location.jmpentry,
                }
                if location.address and location.item.player == self.player:
                    lm_item: "LMItem" = self.create_item(location.item.name)
                    item_info.update({"door_id": lm_item.doorid if lm_item.type == "Door Key" else 0})
                else:
                    item_info.update({"door_id": 0}) # There is no door id for another player's game
            else:
                item_info = {"name": "Nothing", "game": self.game, "classification": "filler"}

            if self.options.boo_health_option.value == 2 and location.name in ROOM_BOO_LOCATION_TABLE.keys():
                item_info.update({"boo_sphere": self.boo_spheres[location.name]})

            if not location.type in output_data["Locations"].keys():
                output_data["Locations"][location.type] = {}
            output_data["Locations"][location.type][location.name] = item_info

        # Outputs the plando details to our expected output file
        # Create the output path based on the current player + expected patch file ending.
        patch_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
            f"{LMPlayerContainer.patch_file_ending}")
        # Create a zip (container) that will contain all the necessary output files for us to use during patching.
        lm_container = LMPlayerContainer(output_data, patch_path, self.multiworld.player_name[self.player], self.player)
        # Write the expected output zip container to the Generated Seed folder.
        lm_container.write()

    # Fill slot data for LM tracker
    def fill_slot_data(self):
        if 'W' in self.multiworld.seed_name:
            ap_seed: str = str(self.multiworld.seed_name[1:])
        else:
            ap_seed: str = str(self.multiworld.seed_name)

        return {
            "rank requirement": self.options.rank_requirement.value,
            "game mode": self.options.game_mode.value,
            "better vacuum": self.options.vacuum_upgrades.value,
            "vacuum start": self.options.vacuum_start.value,
            "boo radar": self.options.boo_radar.value,
            "door rando": self.options.door_rando.value,
            "door rando list": self.open_doors,
            "ghost elements": self.ghost_affected_regions,
            "toadsanity": self.options.toadsanity.value,
            "gold_mice": self.options.gold_mice.value,
            "furnisanity": self.options.furnisanity.value,
            "boosanity": self.options.boosanity.value,
            "portrait ghosts": self.options.portrification.value,
            "speedy spirits": self.options.speedy_spirits.value,
            "lightsanity": self.options.lightsanity.value,
            "walksanity": self.options.walksanity.value,
            "WDYM": self.options.WDYM_checks.value,
            "grassanity": self.options.grassanity.value,
            "silver rank": self.options.silver_ghosts.value,
            "gold rank": self.options.gold_ghosts.value,
            "clairvoya requirement": self.options.mario_items.value,
            "boo gates": self.options.boo_gates.value,
            "boolossus_difficulty": self.options.boolossus_difficulty.value,
            # "washroom boo count": self.options.washroom_boo_count.value,
            "balcony boo count": self.options.balcony_boo_count.value,
            "final boo count": self.options.final_boo_count.value,
            "enemizer": self.options.enemizer.value,
            "spawn_region": self.origin_region_name,
            "death_link": self.options.death_link.value,
            "trap_link": self.options.trap_link.value,
            "energy_link": self.options.energy_link.value,
            "ring_link": self.options.ring_link.value,
            "call_mario": self.options.call_mario.value,
            "luigi max health": self.options.luigi_max_health.value,
            "pickup animation": self.options.enable_pickup_animation.value,
            "send_hints": self.options.send_hints.value,
            "portrait_hints": self.options.portrait_hints.value,
            "hints": self.hints,
            "apworld version": CLIENT_VERSION,
            "seed": ap_seed,
            "disabled_traps": _get_disabled_traps(self.options),
            "self_item_messages": self.options.self_item_messages.value,
            "enable_ring_client_msg": self.options.enable_ring_client_msg.value,
            "enable_trap_client_msg": self.options.enable_trap_client_msg.value,
            "local first key": self.local_early_key,
            "portrait_health": self.portrait_ghost_health,
            "portrait_ghost_health_option": self.options.portrait_health_option.value,
            "silver_original_counts": self.silver_original_counts,
            "gold_original_counts": self.gold_original_counts,
        }

    def modify_multidata(self, multidata: "MultiData") -> None:
        # Wait for output thread to finish first.
        if ((self.options.hint_distribution != 5 and self.options.hint_distribution != 1) or
            self.options.boo_health_option.value == 2 or self.options.portrait_health_option.value == 2):
            self.finished_post_generation.wait()

def _get_disabled_traps(options: LuigiOptions.LMOptions) -> int:
    """
    Gets all traps with a weight of 0 to let trap link know they should be ignored when other players acquire them.
    """
    from .client.links.trap_link import TrapLinkType

    def _is_disabled(weight_percent: int) -> bool:
        return weight_percent == 0

    # We cast the flag values to an int to reduce amount of data being sent to the server.
    trap_flags: int = 0
    if _is_disabled(options.trap_weights["Poison Mushroom"]):
        trap_flags += TrapLinkType.POISON.value
    if _is_disabled(options.trap_weights["Banana Trap"]):
        trap_flags += TrapLinkType.BANANA.value
    if _is_disabled(options.trap_weights["Bomb"]):
        trap_flags += TrapLinkType.BOMB.value
    if _is_disabled(options.trap_weights["Bonk Trap"]):
        trap_flags += TrapLinkType.BONK.value
    if _is_disabled(options.trap_weights["Ice Trap"]):
        trap_flags += TrapLinkType.ICE.value
    if _is_disabled(options.trap_weights["Possession Trap"]):
        trap_flags += TrapLinkType.POSSESSION.value
    if _is_disabled(options.trap_weights["No Vac Trap"]):
        trap_flags += TrapLinkType.NOVAC.value
    if _is_disabled(options.trap_weights["Fear Trap"]):
        trap_flags += TrapLinkType.FEAR.value
    if _is_disabled(options.trap_weights["Squash Trap"]):
        trap_flags += TrapLinkType.SQUASH.value
    if _is_disabled(options.trap_weights["Spooky Time"]):
        trap_flags += TrapLinkType.SPOOKY.value
    if _is_disabled(options.trap_weights["Ghost"]):
        trap_flags += TrapLinkType.GHOST.value

    return trap_flags

def _set_gen_thread_finished(multiworld: MultiWorld, game_name: str):
    for world in multiworld.get_game_worlds(game_name):
        world.finished_post_generation.set()