"""This module contains the World class for Ratchet and Clank 3"""
from collections import Counter
from logging import DEBUG, getLogger
from typing import Any, ClassVar, TextIO, TYPE_CHECKING

from BaseClasses import Item, Location, MultiWorld
from NetUtils import MultiData
from Options import OptionError
from worlds.AutoWorld import World
from worlds.rac3.constants.data.item import item_groups, RAC3_ITEM_DATA_TABLE
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.shortcuts import RAC3SHORTCUTS
from worlds.rac3.items import (create_item, create_itempool, get_filler_selection, process_start_inventory,
                               starting_planets, starting_weapons)
from worlds.rac3.locations import get_location_names, get_region_locations, get_total_locations, location_groups
from worlds.rac3.rac3options import RaC3Options
from worlds.rac3.regions import create_regions, get_nanotech_locations, get_regions
from worlds.rac3.rules import set_rules
from worlds.rac3.universal_tracker import setup_options_from_slot_data, tracker_world
from worlds.rac3.web_world import RaC3Web

rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)


class RaC3World(World):
    """
    Ratchet and Clank 3 is a third person action shooter.
    Blast your enemies with over the top weaponry and save the galaxy from total disaster.
    """

    game = RAC3OPTION.GAME_TITLE_FULL
    item_name_to_id = {name: data.AP_CODE for name, data in RAC3_ITEM_DATA_TABLE.items()}
    location_name_to_id = get_location_names()
    location_name_groups = location_groups
    item_name_groups = item_groups
    preplaced_items: list[str] = []
    starting_weapon_list: list[str] = []
    starting_planet_list: list[str] = []
    filler_items: list[str] = []
    # Config for Universal Tracker

    using_ut: bool  # so we can check if we're using UT only once
    passthrough: dict[str, Any]
    ut_can_gen_without_yaml: bool = True
    disable_ut: bool = False
    tracker_world: ClassVar = tracker_world

    for region in get_regions():
        location_name_groups[region] = get_region_locations(region)

    options_dataclass = RaC3Options
    web = RaC3Web()
    if TYPE_CHECKING:
        options = RaC3Options

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    # Generation Begins

    def generate_early(self):
        # count number of . in the version number to determine if dev build
        version_dots = RAC3OPTION.VERSION_NUMBER.count(".")
        if version_dots >= 3 or "dev" in RAC3OPTION.VERSION_NUMBER:
            rac3_logger.warning("\nYou are using a development build of the RaC3 Archipelago Randomizer!\n"
                                "There may be bugs present and features that have not been tested fully.\n"
                                "These builds are meant for testing and bug reporting purposes "
                                "and should not be used for normal play!\n")
        # implement .yaml-less Universal Tracker support
        setup_options_from_slot_data(self)
        self.preplaced_items = [RAC3ITEM.VELDIN, RAC3ITEM.THIRD_PERSON, RAC3ITEM.FIRST_PERSON, RAC3ITEM.LOCK_STRAFE]
        if self.options.clank_options.value == self.options.clank_options.option_start_with:
            self.preplaced_items += [RAC3ITEM.CLANK, RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK]
        for item in self.preplaced_items:
            self.push_precollected(self.create_item(item))
        process_start_inventory(self)
        starting_weapons(self)
        starting_planets(self)
        self.handle_option_errors()
        self.dead_seed_check()

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def handle_option_errors(self) -> None:
        """Check for option combinations that will never result in successful seed generation and warn the player"""
        if (not self.options.shortcuts.value.get(RAC3SHORTCUTS.VELDIN_SKIP, False)
            and self.options.clank_options.value
            and not self.options.titanium_bolts.value
            and not self.options.weapon_vendors.value
            and len(self.starting_weapon_list) > 1
            and self.starting_planet_list
            and (self.multiworld.players == 1 and not self.using_ut)):
            item = ""
            match self.options.clank_options.value:
                case self.options.clank_options.option_shuffled_as_one:
                    item = RAC3ITEM.CLANK
                case self.options.clank_options.option_shuffled_independently:
                    item = RAC3ITEM.HELI_PACK
                case self.options.clank_options.option_shuffled_progressive:
                    item = RAC3ITEM.PROGRESSIVE_PACK
                case _:
                    raise OptionError(
                        "A clank option was added that does not have option error handling, Please warn the developer.")
            self.options.start_inventory_from_pool.value[item] += 1

    def dead_seed_check(self) -> None:
        """Check for option combinations that will result in a dead seed and raise an OptionError to warn the player"""
        nanotech_locations = get_nanotech_locations(self.options)
        no_nanotech_locations = not nanotech_locations

        if (not self.options.shortcuts.value.get(RAC3SHORTCUTS.VELDIN_SKIP, False)
            and not self.options.titanium_bolts.value
            and not self.options.trophies.value
            and not self.options.weapon_vendors.value
            and not self.options.ship_vendor.value
            and not self.options.armor_vendor.value
            and not self.options.vr_challenges.value
            and self.options.skill_points.value < 2
            and no_nanotech_locations
            and len(self.starting_weapon_list) > 1
            and self.starting_planet_list
            and (self.multiworld.players == 1 and not self.using_ut)):
            raise OptionError("Options selected do not allow Ratchet to advance past Starship Phoenix")

    # Start inventory, local, non-local, and early items are finalised

    def create_regions(self) -> None:
        """Create the regions used in the world"""
        create_regions(self)
        self.place_starting_items()

    def place_starting_items(self) -> None:
        """Take the list of starting planets and starting weapons and place them on locations or as precollected"""
        if len(self.starting_weapon_list) > 0:
            self.get_location(RAC3LOCATION.VELDIN_FIRST_RANGER).place_locked_item(
                self.create_item(self.starting_weapon_list[0]))
            if len(self.starting_weapon_list) > 1:
                self.get_location(RAC3LOCATION.VELDIN_SECOND_RANGER).place_locked_item(
                    self.create_item(self.starting_weapon_list[1]))
        if self.options.shortcuts.value.get(RAC3SHORTCUTS.VELDIN_SKIP, False):
            if len(self.starting_planet_list) == 1:  # either [Phoenix] or [Other]
                if self.starting_planet_list[0] == RAC3ITEM.STARSHIP_PHOENIX:
                    self.preplaced_items.append(self.starting_planet_list[0])
                    self.push_precollected(self.create_item(self.starting_planet_list[0]))
                else:
                    self.get_location(RAC3LOCATION.VELDIN_SAVE_VELDIN).place_locked_item(
                        self.create_item(self.starting_planet_list[0]))
            elif len(self.starting_planet_list) > 1:  # always [Phoenix, Other]
                self.preplaced_items.append(self.starting_planet_list[0])
                self.push_precollected(self.create_item(self.starting_planet_list[0]))
                self.get_location(RAC3LOCATION.VELDIN_SAVE_VELDIN).place_locked_item(
                    self.create_item(self.starting_planet_list[1]))
        else:
            if len(self.starting_planet_list) == 1 and self.starting_planet_list[
                0] == RAC3ITEM.STARSHIP_PHOENIX:  # [Phoenix]
                self.get_location(RAC3LOCATION.FLORANA_DEFEAT_QWARK).place_locked_item(
                    self.create_item(self.starting_planet_list[0]))
            elif len(self.starting_planet_list) > 0:  # First entry not Phoenix
                self.get_location(RAC3LOCATION.VELDIN_SAVE_VELDIN).place_locked_item(
                    self.create_item(self.starting_planet_list[0]))
                if len(self.starting_planet_list) > 1:  # size == 2
                    self.get_location(RAC3LOCATION.FLORANA_DEFEAT_QWARK).place_locked_item(
                        self.create_item(self.starting_planet_list[1]))
        self.preplaced_items.extend(self.starting_weapon_list)
        self.preplaced_items.extend(self.starting_planet_list)
        self.get_location(RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR).place_locked_item(
            self.create_item(RAC3ITEM.VICTORY))
        self.preplaced_items.append(RAC3ITEM.VICTORY)

    def create_items(self):
        """Create the items used in the world"""
        exclusion_filler = [self.create_filler() for _ in range(self.get_excluded_count())]
        self.multiworld.itempool.extend(exclusion_filler)

        own_location_count = len(self.multiworld.get_unfilled_locations(self.player))
        itempool = create_itempool(self)
        item_count = len(itempool + exclusion_filler)
        filler_count = own_location_count - item_count
        # rac3_logger.info(f"\nPlayer: {self.player_name}\n"
        #                  f"Own location count: {own_location_count}\n"
        #                  f"Item count: {item_count}\n")

        if filler_count < 0:
            self.handle_not_enough_locations(-filler_count)
            self.random.shuffle(itempool)
            # rac3_logger.info(f"Placing {-filler_count} starting items")
            for item in range(-filler_count):
                # rac3_logger.info(f"Starting with: {itempool[0].name}")
                self.push_precollected(itempool.pop(0))
        else:
            filler = [self.create_filler() for _ in range(filler_count)]
            self.multiworld.itempool.extend(filler)

        self.multiworld.itempool.extend(itempool)
        player_items = Counter(item.player for item in self.multiworld.itempool)
        player_locs = Counter(loc.player for loc in self.multiworld.get_locations() if not loc.item)
        assert player_items[self.player] == player_locs[self.player], (f"Player item count {player_items[self.player]} "
                                                                       f"and location count {player_locs[self.player]} "
                                                                       f"do not match")

    def get_filler_item_name(self) -> str:
        if not len(self.filler_items):
            self.filler_items = get_filler_selection(self)
        return self.random.choice(self.filler_items)

    def get_excluded_count(self) -> int:
        """Get the number of unique excluded locations for this player"""
        excluded_options = self.options.exclude_locations.value
        excluded_locations = set()
        for option in excluded_options:
            if option in location_groups:
                excluded_locations.update(location_groups[option])
            else:
                excluded_locations.add(option)
        return len(excluded_locations)

    def handle_not_enough_locations(self, count: int):
        """Check the available location and items counts, raise OptionErrors to warn the player of too few locations"""
        if self.options.generation_behavior.value:
            return
        excluded_count = self.get_excluded_count()
        option_list: list[str] = []
        if self.options.skill_points.value == 0:
            option_list.append(RAC3OPTION.SKILL_POINTS)
        if self.options.trophies.value == 0:
            option_list.append(RAC3OPTION.TROPHIES)
        if self.options.titanium_bolts.value == 0:
            option_list.append(RAC3OPTION.TITANIUM_BOLTS)
        if self.options.nanotech_milestones.value < 3:
            option_list.append(RAC3OPTION.NANOTECH_MILESTONES)
        if self.options.rangers.value == 0:
            option_list.append(RAC3OPTION.RANGERS)
        if self.options.arena.value == 0:
            option_list.append(RAC3OPTION.ARENA)
        if self.options.vidcomics.value == 0:
            option_list.append(RAC3OPTION.VIDCOMICS)
        if self.options.vidcomic_health_upgrades.value == 0:
            option_list.append(RAC3OPTION.VIDCOMIC_HEALTH_UPGRADES)
        if self.options.vr_challenges.value == 0:
            option_list.append(RAC3OPTION.VR_CHALLENGES)
        if self.options.weapon_vendors.value == 0:
            option_list.append(RAC3OPTION.WEAPON_VENDORS)
        if self.options.armor_vendor.value == 0:
            option_list.append(RAC3OPTION.ARMOR_VENDOR)
        if self.options.ship_vendor.value == 0:
            option_list.append(RAC3OPTION.SHIP_VENDOR)
        if not self.options.weapon_level_locations.value:
            option_list.append(RAC3OPTION.WEAPON_LEVEL_LOCATIONS)
        if self.options.sewer_crystals.value < 3:
            option_list.append(RAC3OPTION.SEWER_CRYSTALS)
        if self.options.sewer_limitation.value < 20:
            option_list.append(RAC3OPTION.SEWER_LIMITATION)
        if self.options.nanotech_limitation.value < 60:
            option_list.append(RAC3OPTION.NANOTECH_LIMITATION)
        if excluded_count > 30:
            option_list.append(RAC3OPTION.EXCLUDE)
        if not option_list:
            option_list: str = "dunno"  # ¯\_(''/)_/¯
        message = (f"Not enough location options enabled by Player: by Player: {self.player_name}! {count} items have "
                   f"nowhere to be placed.")
        if count >= 50:
            message += ("\nThis large of a difference requires Progressive Weapons and or Weapon Mods to be disabled, "
                        "Additional Sewer, Crystal Trade locations, Additional Nanotech level locations or Additional "
                        "Weapon Level locations.")
        if count <= 10 and sum(self.options.start_inventory_from_pool.value.values()) <= 10:
            message += "\nConsider adding some items to your starting_items_from_pool or "
        else:
            message += "\nConsider "
        message += f"adjusting some of the following options: {option_list}"
        raise OptionError(message)

    def set_rules(self):
        set_rules(self)

    # Priority and Excluded locations finalised
    # Local and non-local location rules finalised
    # Read Plando options

    def connect_entrances(self) -> None:
        pass

    def generate_basic(self) -> None:
        pass

    # Remove starting inventory from pool and replace with filler
    # Item Links finalised
    # Resolve Item Plando

    def pre_fill(self) -> None:
        pass

    # Begin Fill stage
    # Distribute early items

    def fill_hook(self,
                  progitempool: list["Item"],
                  usefulitempool: list["Item"],
                  filleritempool: list["Item"],
                  fill_locations: list["Location"]) -> None:
        pass

    # Remainder of Fill happens, error if any unplaced items or unfilled locations remain

    def post_fill(self) -> None:
        pass

    # Progression Balancing

    def finalize_multiworld(self) -> None:
        pass

    def pre_output(self) -> None:
        pass

    # Begin Multithreading
    # Create spoiler

    def generate_output(self, output_directory: str) -> None:
        pass

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        pass

    def fill_slot_data(self) -> dict[str, Any]:
        slot_data: dict[str, Any] = {
            RAC3OPTION.VERSION: RAC3OPTION.VERSION_NUMBER,
            RAC3OPTION.START_INVENTORY_FROM_POOL: self.options.start_inventory_from_pool.value,
            RAC3OPTION.STARTING_WEAPONS: self.options.starting_weapons.value,
            RAC3OPTION.BOLT_AND_XP_MULTIPLIER: self.options.bolt_and_xp_multiplier.value,
            RAC3OPTION.PROGRESSIVE_WEAPONS: self.options.progressive_weapons.value,
            RAC3OPTION.WEAPON_MODS: self.options.weapon_mods.value,
            RAC3OPTION.ARMOR_UPGRADE: self.options.armor_upgrade.value,
            RAC3OPTION.SKILL_POINTS: self.options.skill_points.value,
            RAC3OPTION.TROPHIES: self.options.trophies.value,
            RAC3OPTION.TITANIUM_BOLTS: self.options.titanium_bolts.value,
            RAC3OPTION.NANOTECH_MILESTONES: self.options.nanotech_milestones.value,
            RAC3OPTION.EXCLUDE: self.options.exclude_locations.value,
            RAC3OPTION.DEATHLINK: self.options.deathlink.value,
            RAC3OPTION.GENERATION_BEHAVIOR: self.options.generation_behavior.value,
            RAC3OPTION.SHIP_NOSE: self.options.ship_nose.value,
            RAC3OPTION.SHIP_WINGS: self.options.ship_wings.value,
            RAC3OPTION.SHIP_SKIN: self.options.ship_skin.value,
            RAC3OPTION.PLAYER_SKIN: self.options.player_skin.value,
            RAC3OPTION.ENABLE_TRAPS: self.options.traps_enabled.value,
            RAC3OPTION.TRAP_WEIGHT: self.options.trap_weight.value,
            RAC3OPTION.TRAP_MAGNITUDE: self.options.trap_magnitude.value,
            RAC3OPTION.FILLER_MAGNITUDE: self.options.filler_magnitude.value,
            RAC3OPTION.RANGERS: self.options.rangers.value,
            RAC3OPTION.ARENA: self.options.arena.value,
            RAC3OPTION.VIDCOMICS: self.options.vidcomics.value,
            RAC3OPTION.VR_CHALLENGES: self.options.vr_challenges.value,
            RAC3OPTION.SEWER_CRYSTALS: self.options.sewer_crystals.value,
            RAC3OPTION.SEWER_LIMITATION: self.options.sewer_limitation.value,
            RAC3OPTION.NANOTECH_LIMITATION: self.options.nanotech_limitation.value,
            RAC3OPTION.WEAPON_VENDORS: self.options.weapon_vendors.value,
            RAC3OPTION.FILLER_WEIGHT: self.options.filler_weight.value,
            RAC3OPTION.ONE_HP_CHALLENGE: self.options.one_hp_challenge.value,
            RAC3OPTION.CLANK_OPTIONS: self.options.clank_options.value,
            RAC3OPTION.SHIP_VENDOR: self.options.ship_vendor.value,
            RAC3OPTION.ARMOR_VENDOR: self.options.armor_vendor.value,
            RAC3OPTION.SCOUT_VENDORS: self.options.scout_vendors.value,
            RAC3OPTION.SHORTCUTS: self.options.shortcuts.value,
            RAC3OPTION.SPEEDUPS: self.options.speedups.value,
            RAC3OPTION.NGPLUS_ITEMS: self.options.ngplus_items.value,
            RAC3OPTION.NGPLUS_VENDOR: self.options.ngplus_vendors.value,
            RAC3OPTION.NGPLUS_START: self.options.ngplus_start.value,
            RAC3OPTION.HELP_DESK: self.options.helpdesk.value,
            RAC3OPTION.WEAPON_LEVEL_LOCATIONS: self.options.weapon_level_locations.value,
            RAC3OPTION.VENDOR_ACCESS: self.options.vendor_access.value,
            RAC3OPTION.BONUS_VIDCOMIC_HEALTH: self.options.bonus_vidcomic_health.value,
            RAC3OPTION.VIDCOMIC_HEALTH_UPGRADES: self.options.vidcomic_health_upgrades.value,
            RAC3OPTION.DEATHLINK_BEHAVIOR: self.options.deathlink_behavior.value,
            RAC3OPTION.TOTAL_LOCATIONS: get_total_locations(self),
        }

        return slot_data

    def modify_multidata(self, multidata: "MultiData") -> None:
        pass

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        pass

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        pass

    def write_spoiler_end(self, spoiler_handle: TextIO) -> None:
        pass

    # For Universal Tracker integration
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        """Trigger a regen in UT"""
        return slot_data

    # def post_fill(self) -> None:
    #    from Utils import visualize_regions
    #    visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_world.puml",
    #                      regions_to_highlight=self.multiworld.get_all_state(False).reachable_regions[
    #                          self.player])
