from BaseClasses import Item, Location
from .Locations import grinch_locations_to_id, grinch_locations, GrinchLocation, get_location_names_per_category, GrinchLocationData
from .Items import (grinch_items_to_id, GrinchItem, ALL_ITEMS_TABLE, MISC_ITEMS_TABLE, get_item_names_per_category,
    TRAPS_TABLE, MOVES_TABLE, USEFUL_ITEMS_TABLE)
from .Regions import connect_regions
from .Rules import set_location_rules

from .Client import *
from typing import ClassVar

from worlds.AutoWorld import World
from Options import OptionError

from .GrinchOptions import GrinchOptions
from .Web import GrinchWeb


class GrinchWorld(World):
    """
    The Grinch is a 2000 platform video game loosely based on the film How the Grinch Stole Christmas. As the Grinch, 
    the player can jump, ground pound, and use his smelly breath to guide his way through various obstacles in the game.
    """
    game: ClassVar[str] = "The Grinch"
    options_dataclass = GrinchOptions
    options: GrinchOptions
    topology_present = True # not an open world game, very linear, allows "Paths" in spoiler log
    item_name_to_id: ClassVar[dict[str, int]] = grinch_items_to_id()
    location_name_to_id: ClassVar[dict[str, int]] = grinch_locations_to_id()
    required_client_version = (0, 6, 6) # Unused atm, replaced by ap.json
    item_name_groups = get_item_names_per_category()
    location_name_groups = get_location_names_per_category()
    web = GrinchWeb()

    songs_chosen: dict

    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player YAML

    def __init__(self, *args, **kwargs):  # Pulls __init__ function and takes control from there in BaseClasses.py
        self.origin_region_name: str = "Mount Crumpit"
        super(GrinchWorld, self).__init__(*args, **kwargs)
        self.songs_chosen = {}

    def generate_early(self) -> None:  # Special conditions changed before generation occurs
        from CommonClient import logger
        if self.options.ring_link == 1 and self.options.unlimited_eggs == 1:
            raise OptionError("Cannot enable both unlimited rotten eggs and ring links. You can only enable one of " +
                f"these at a time. The following player's YAML needs to be fixed: {self.player_name}")

        # if self.options.randomize_sleigh_parts and "Submarine World" in self.options.exclude_environments:
        #     self.multiworld.push_precollected(self.create_item("Twin-End Tuba"))
            # raise logger.info("Because Twin-End Tuba is forced into Submarine World, " +
            #                   f"{self.player_name} cannot exclude exclude the Submarine World environment.")

        # Total available weight sum of filler items.
        # If this is 0, it means no filler was provided by the user, which will cause generation errors as there will
        #   be not enough items for all defined locations. Later this can be changed to default item and this get removed.
        total_fillerweights = sum(self.options.filler_weight[filler] for filler in self.options.filler_weight.keys())
        if total_fillerweights <= 0:
            logger.warning(f"Player {self.player_name} has all filler weights set to 0. Using Presents instead for filler.")

        total_trapweights = sum(self.options.trap_weight[trap] for trap in self.options.trap_weight.keys())
        if total_trapweights <= 0 and self.options.trap_percentage >= 1:
            raise OptionError("Cannot begin generation as no trap options are defined. At least one trap item " +
                f"must have a weight of at least 1. The following player's YAML needs to be fixed: {self.player_name}")

        if self.options.music_rando.value == 1:
            for music_enabled_region, region_data in ALL_REGIONS_INFO.items():
                if region_data.allow_music_rando:
                    self.songs_chosen[music_enabled_region] = self.random.randint(2, 22)

        # this handles all related logical UT things
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                slot_data = self.multiworld.re_gen_passthrough[self.game]
                print(slot_data)
                self.options.unlimited_eggs.value = slot_data["unlimited_eggs"]
                self.options.starting_area.value = slot_data["starting_area"]
                self.options.exclude_environments.value = ["exclude_environments"]
                self.options.giftsanity.value = slot_data["giftsanity"]
                self.options.progressive_vacuums = slot_data["progressive_vacuums"]
                self.options.missionsanity = slot_data["missionsanity"]
                self.options.supadow_minigames = slot_data["supadow_minigames"]
                self.options.move_rando = slot_data["move_rando"]
                self.options.moves_to_randomize = slot_data["moves_to_randomize"]
                self.options.gadget_rando = slot_data["gadget_rando"]
                self.options.gadgets_to_randomize = slot_data["gadgets_to_randomize"]
                self.options.exclude_gc = slot_data["exclude_gc"]
                self.options.progressive_gadgets = slot_data["progressive_gadgets"]
                self.options.killsanity = slot_data["killsanity"]
                self.options.misc_checks = slot_data["misc_checks"]
                self.options.randomize_mission_items = slot_data["randomize_mission_items"]
                self.options.randomize_sleigh_parts = slot_data["randomize_sleigh_parts"]

    def create_regions(self):  # Generates all regions for the multiworld
        connect_regions(self, self.multiworld)

        wv_subareas: set[str] = {
            "Post Office",
            "Clock Tower",
            "City Hall",
        }
        wf_subareas: set[str] = {
            "Civic Center",
            "Ski Resort",
        }
        wd_subareas: set[str] = {
            "Minefield",
            "Power Plant",
            "Generator Building",
        }
        wl_subareas: set[str] = {
            "Scout's Hut",
            "North Shore",
            "Mayor's Villa",
            "Submarine World",
        }

        for location, data in grinch_locations.items():
            region = self.get_region(data.region)

            if location == "MC - Sleigh Ride - Save Christmas":
                region.add_event(location, "Goal", None, Location, Item)
                continue

            # No .value after self.options because UT no likey
            if location == "MC - Unlock the Grinch Copter" and self.options.exclude_gc:
                continue

            # No .value after self.options because UT no likey
            if "Giftsanity" in data.location_group and (not self.options.giftsanity or self.options.exclude_gc):
                continue

            # No .value after self.options because UT no likey
            if "Missions" in data.location_group and self.options.missionsanity in [0,2]:
                continue

            # No .value after self.options because UT no likey
            if "Missionsanity" in data.location_group and self.options.missionsanity in [0,1]:
                continue

            if "Miscellaneous" in data.location_group and self.options.misc_checks == False:
                continue

            if location == "WV - Squashing All Gifts":
                exclude_wv_squash: bool = False
                for wv_sub in wv_subareas:
                    if wv_sub in self.options.exclude_environments:
                        exclude_wv_squash = True

                if exclude_wv_squash:
                    continue  # Ignores the creation of WV Squashing all Gifts

            elif location == "WF - Squashing All Gifts":
                exclude_wf_squash: bool = False
                for wf_sub in wf_subareas:
                    if wf_sub in self.options.exclude_environments:
                        exclude_wf_squash = True

                if exclude_wf_squash:
                    continue  # Ignores the creation of WF Squashing all Gifts

            elif location == "WD - Squashing All Gifts":
                exclude_wd_squash: bool = False
                for wd_sub in wd_subareas:
                    if wd_sub in self.options.exclude_environments:
                        exclude_wd_squash = True

                if exclude_wd_squash:
                    continue  # Ignores the creation of WD Squashing all Gifts

            elif location == "WL - Squashing All Gifts":
                exclude_wl_squash: bool = False
                for wl_sub in wl_subareas:
                    if wl_sub in self.options.exclude_environments:
                        exclude_wl_squash = True

                if exclude_wl_squash:
                    continue  # Ignores the creation of WL Squashing all Gifts

            if "Mission Specific Item Locations" in data.location_group and self.options.randomize_mission_items:
                continue

            if ("WL - Mayor's Villa - Hook" in location
                    and not self.options.randomize_mission_items
                    and self.options.exclude_gc
                    and not "Mayor's Villa" in self.options.exclude_environments):
                continue

            if "Sleigh Parts" in data.location_group and self.options.randomize_sleigh_parts:
                continue

            # If the region is in the list to be ignored, DON'T create the location and just continue.
            # Ex if Mount Crumpit is in the exclude env list, no locations should exist in Mount Crumpit.
            if region.name in self.options.exclude_environments:
                if region.name == "Mount Crumpit":
                    logger.warning(f"Player {self.player_name} has excluded Mount Crumpit, which is where a large number of Sphere 1 locations usually exist.")
                continue


            entry = GrinchLocation(self.player, location, region, data)
            region.locations.append(entry)

    def create_item(self, item: str) -> GrinchItem:  # Creates specific items on demand
        if item in ALL_ITEMS_TABLE.keys():
            return GrinchItem(item, self.player, ALL_ITEMS_TABLE[item])

        raise Exception(f"Invalid item name: {item}")

    def create_items(self):  # Generates all items for the multiworld
        self_itempool: list[GrinchItem] = []
        sub_area_items: dict[str, list[str]] = {
            "Who Cloak": ["Post Office"],
            "Scout Clothes": ["Mayor's Villa", "North Shore"],
            "Cable Car Access Card": ["Ski Resort"],
        }
        missionsanity_items: dict[str, list[str]] = {
            "Who Cloak": ["Post Office"],
            "Scout Clothes": ["Mayor's Villa", "North Shore"],
            "Drill": ["North Shore"],
            "Painting Bucket": ["Whoville"],
        }

        # Precollected items is stored per player. First, we must get the current player's starting inventory.
        # From here, we get an AP item list. But, we only care about the name. So we get a list of strings as a result.
        player_start_inv: list[str] = [item.name for item in self.multiworld.precollected_items[self.player]]

        for sleigh_parts in SLEIGH_TABLE:
            if sleigh_parts in player_start_inv:
                continue

            # if "Sleigh Room Key" in sleigh_parts:
            #     self_itempool.append(self.create_item(sleigh_parts))

            if not self.options.randomize_sleigh_parts:
                if "Exhaust Pipes" in sleigh_parts:
                    self.multiworld.get_location("WV - Exhaust Pipes", self.player).place_locked_item(
                        self.create_item("Exhaust Pipes"))
                if "Skis" in sleigh_parts:
                    self.multiworld.get_location("WF - Skis", self.player).place_locked_item(
                        self.create_item("Skis"))
                if "Tires" in sleigh_parts:
                    self.multiworld.get_location("WD - Tires", self.player).place_locked_item(
                        self.create_item("Tires"))
                if not "Submarine World" in self.options.exclude_environments and "Twin-End Tuba" in sleigh_parts:
                    self.multiworld.get_location("WL - Submarine World - Twin-End Tuba", self.player).place_locked_item(
                        self.create_item("Twin-End Tuba"))
                else:
                    self.multiworld.push_precollected(self.create_item("Twin-End Tuba"))
                if "GPS" in sleigh_parts:
                    self.multiworld.get_location("WL - South Shore - GPS", self.player).place_locked_item(
                        self.create_item("GPS"))
            else:
                self_itempool.append(self.create_item(sleigh_parts))

        for hearts_added in USEFUL_ITEMS_TABLE:
            if hearts_added == grinch_items.useful_items.HEART_OF_STONE:
                # Get the count of already created Heart of Stone items, but capped to 4
                heart_stone_count: int = min(player_start_inv.count(grinch_items.useful_items.HEART_OF_STONE), 4)
                for _ in range(4 - heart_stone_count):
                    self_itempool.append(self.create_item(hearts_added))

        for mission_item in MISSION_ITEMS_TABLE:
            # Only create the item if it doesn't already exist in the player's start inventory.
            if mission_item in player_start_inv:
                continue

            # Checks to see if there are any locations in the Sub-area list.
            sub_area_has_no_locations: bool = False

            if mission_item in sub_area_items:
                sub_area_has_no_locations = True
                for grinch_reg in sub_area_items[mission_item]:
                    if len(self.get_region(grinch_reg).get_locations()) > 0:
                        sub_area_has_no_locations = False

            # If the item is a sub_area_item that has 0 locations, add it to start inventory
            if sub_area_has_no_locations:
                self.multiworld.push_precollected(self.create_item(mission_item))
                player_start_inv.append(mission_item)
            # Else if the player disables missionsanity, add the item into start inventory
            # No .value after self.options.missionsanity because UT no likey
            elif self.options.missionsanity == 0:
                self.multiworld.push_precollected(self.create_item(mission_item))
                player_start_inv.append(mission_item)
            elif self.options.missionsanity == 2:
                if mission_item in missionsanity_items:
                    self_itempool.append(self.create_item(mission_item))
                else:
                    self.multiworld.push_precollected(self.create_item(mission_item))
                    player_start_inv.append(mission_item)

            if not self.options.randomize_mission_items:

                if "Painting Bucket" in mission_item:
                    self.multiworld.get_location("WV - Painting Bucket", self.player).place_locked_item(
                        self.create_item("Painting Bucket"))

                if not "Clock Tower" in self.options.exclude_environments:
                    if "Who Cloak" in mission_item:
                        self.multiworld.get_location("WV - Clock Tower - Who Cloak", self.player).place_locked_item(
                            self.create_item("Who Cloak"))
                    else:
                        self.multiworld.push_precollected(self.create_item("Who Cloak"))

                    if "Hammer" in mission_item:
                        self.multiworld.get_location("WV - Clock Tower - Hammer", self.player).place_locked_item(
                            self.create_item("Hammer"))
                    else:
                        self.multiworld.push_precollected(self.create_item("Hammer"))

                if not "City Hall" in self.options.exclude_environments:
                    if "Sculpting Tools" in mission_item:
                        self.multiworld.get_location("WV - City Hall - Sculpting Tools", self.player).place_locked_item(
                            self.create_item("Sculpting Tools"))
                    else:
                        self.multiworld.push_precollected(self.create_item("Sculpting Tools"))

                if "Glue Bucket" in mission_item:
                    self.multiworld.get_location("WF - Glue Bucket", self.player).place_locked_item(
                        self.create_item("Glue Bucket"))

                if "Cable Car Access Card" in mission_item:
                    self.multiworld.get_location("WF - Cable Car Access Card", self.player).place_locked_item(
                        self.create_item("Cable Car Access Card"))

                if not "Minefield" in self.options.exclude_environments:
                    if "Scissors" in mission_item:
                        self.multiworld.get_location("WD - Minefield - Scissors", self.player).place_locked_item(
                            self.create_item("Scissors"))
                    else:
                        self.multiworld.push_precollected(self.create_item("Scissors"))

                if not "Scout's Hut" in self.options.exclude_environments:
                    if "Scout Clothes" in mission_item:
                        self.multiworld.get_location("WL - Scout's Hut - Scout Clothes", self.player).place_locked_item(
                            self.create_item("Scout Clothes"))
                    else:
                        self.multiworld.push_precollected(self.create_item("Scout Clothes"))

                if not "North Shore" in self.options.exclude_environments:
                    if "Drill" in mission_item:
                        self.multiworld.get_location("WL - North Shore - Drill", self.player).place_locked_item(
                            self.create_item("Drill"))
                    else:
                        self.multiworld.push_precollected(self.create_item("Drill"))

                if not "Mayor's Villa" in self.options.exclude_environments:
                    if "Rope" in mission_item:
                        self.multiworld.get_location("WL - Mayor's Villa - Rope", self.player).place_locked_item(
                            self.create_item("Rope"))
                    else:
                        self.multiworld.push_precollected(self.create_item("Rope"))

                    if not self.options.exclude_gc and "Hook" in mission_item:
                        self.multiworld.get_location("WL - Mayor's Villa - Hook", self.player).place_locked_item(
                            self.create_item("Hook"))
                    else:
                        self.multiworld.push_precollected(self.create_item("Hook"))

            # Else, let the multiworld create the item normally.
            else:
                self_itempool.append(self.create_item(mission_item))

        # Add various moves that the user requested.
        for moves_added in MOVES_TABLE:
            # Only create the item if it doesn't already exist in the player's start inventory.
            if moves_added in player_start_inv:
                continue

            if self.options.move_rando and moves_added in self.options.moves_to_randomize:
                self_itempool.append(self.create_item(moves_added))
            else:
                self.multiworld.push_precollected(self.create_item(moves_added))
                player_start_inv.append(moves_added)

        # Adds gadgets
        for gadgets_added in GADGETS_TABLE:
            if gadgets_added == "Grinch Copter" and self.options.exclude_gc:
                continue

            if gadgets_added == "Marine Mobile" and "Submarine World" in self.options.exclude_environments:
                self.multiworld.push_precollected(self.create_item(gadgets_added))
                player_start_inv.append(gadgets_added)
                continue

            # Only create the item if it doesn't already exist in the player's start inventory.
            elif gadgets_added in player_start_inv:
                continue

            if self.options.gadget_rando and gadgets_added in self.options.gadgets_to_randomize:
                self_itempool.append(self.create_item(gadgets_added))
            else:
                self.multiworld.push_precollected(self.create_item(gadgets_added))
                player_start_inv.append(gadgets_added)
                continue

        if not self.options.progressive_vacuums:
        # When the starting area is chosen, add the key to the starting inventory.
            if self.options.starting_area == 0:
                self.multiworld.push_precollected(self.create_item("Whoville Vacuum Tube"))
                player_start_inv.append("Whoville Vacuum Tube")
            elif self.options.starting_area == 1:
                self.multiworld.push_precollected(self.create_item("Who Forest Vacuum Tube"))
                player_start_inv.append("Who Forest Vacuum Tube")
            elif self.options.starting_area == 2:
                self.multiworld.push_precollected(self.create_item("Who Dump Vacuum Tube"))
                player_start_inv.append("Who Dump Vacuum Tube")
            elif self.options.starting_area == 3:
                self.multiworld.push_precollected((self.create_item("Who Lake Vacuum Tube")))
                player_start_inv.append("Who Lake Vacuum Tube")
        else:
            self.multiworld.push_precollected((self.create_item("Progressive Vacuum Tube")))
            player_start_inv.append("Progressive Vacuum Tube")

        if not self.options.progressive_vacuums:
            for vacuums_added in KEYS_TABLE.keys():
                if vacuums_added == "Progressive Vacuum Tube":
                    continue

                if vacuums_added not in player_start_inv:
                    self_itempool.append(self.create_item(vacuums_added))
        else:
            progress_vac_count: int = min(player_start_inv.count("Progressive Vacuum Tube"),4)
            for _ in range(4 - progress_vac_count):
                self_itempool.append(self.create_item("Progressive Vacuum Tube"))

        if not self.options.randomize_sleigh_parts:
            self.multiworld.get_location("WV - Exhaust Pipes", self.player).place_locked_item(
                self.create_item("Exhaust Pipes"))
            self.multiworld.get_location("WF - Skis", self.player).place_locked_item(
                self.create_item("Skis"))
            self.multiworld.get_location("WD - Tires", self.player).place_locked_item(
                self.create_item("Tires"))
            if not "Submarine World" in self.options.exclude_environments:
                self.multiworld.get_location("WL - Submarine World - Twin-End Tuba", self.player).place_locked_item(
                    self.create_item("Twin-End Tuba"))
            else:
                self.multiworld.push_precollected(self.create_item("Twin-End Tuba"))
            self.multiworld.get_location("WL - South Shore - GPS", self.player).place_locked_item(
                self.create_item("GPS"))

        # Get number of current unfilled locations
        unfilled_locations: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(self_itempool)
        trap_locations: int = int(math.floor(unfilled_locations * (self.options.trap_percentage / 100)))
        filler_locations = unfilled_locations - trap_locations

        # If trap_locations is 0, this will automatically get skipped
        for _ in range(trap_locations):
            # Keys are the individual items, values are the weights based on the option being set
            self_itempool.append(self.create_item(self.get_weighted_filler_item
                (list(self.options.trap_weight.keys()), list(self.options.trap_weight.values()))))

        total_fillerweights = sum(self.options.filler_weight[filler] for filler in self.options.filler_weight.keys())
        for _ in range(filler_locations):
            if total_fillerweights > 0:
                # Keys are the individual items, values are the weights based on the option being set
                self_itempool.append(self.create_item(self.get_weighted_filler_item(
                    list(self.options.filler_weight.keys()), list(self.options.filler_weight.values()))))
            else:
                self_itempool.append(self.create_item("Present"))

        self.multiworld.itempool += self_itempool

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Goal", self.player)
        set_location_rules(self)

    def get_weighted_filler_item(self, other_filler: list[str], weights_dict: list[int]) -> str:
        # The below does this for deterministic reasons, otherwise if you rolled the same seed, you would get different outcomes.
            local_dict: dict[str, int] = dict(zip(other_filler, weights_dict))
            # local_dict["Present"] = 1
            return self.random.choices(list(local_dict.keys()), list(local_dict.values()))[0]

    # this handles ingame/client related things
    def fill_slot_data(self):
        return {
            "unlimited_eggs": self.options.unlimited_eggs.value,
            "ring_link": self.options.ring_link.value,
            "starting_area": self.options.starting_area.value,
            "exclude_environments": self.options.exclude_environments.value,
            "giftsanity": self.options.giftsanity.value,
            "progressive_vacuums": self.options.progressive_vacuums.value,
            "missionsanity": self.options.missionsanity.value,
            "supadow_minigames": self.options.supadow_minigames.value,
            "move_rando": self.options.move_rando.value,
            "moves_to_randomize": self.options.moves_to_randomize.value,
            "gadget_rando": self.options.gadget_rando.value,
            "gadgets_to_randomize": self.options.gadgets_to_randomize.value,
            "exclude_gc": self.options.exclude_gc.value,
            "progressive_gadgets": self.options.progressive_gadgets.value,
            "killsanity": self.options.killsanity.value,
            "misc_checks": self.options.misc_checks.value,
            "death_link": self.options.death_link.value,
            "damage_rate": self.options.damage_rate.value,
            "music_rando": self.options.music_rando.value,
            "chosen_music": self.songs_chosen,
            "reduced_cutscenes": self.options.reduced_cutscenes.value,
            "randomize_mission_items": self.options.randomize_mission_items.value,
            "randomize_sleigh_parts": self.options.randomize_sleigh_parts.value,
        }

    def generate_output(self, output_directory: str) -> None:
        # print("")
        pass