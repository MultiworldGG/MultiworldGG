import collections
import datetime
import functools
import logging
import random
import time

from typing import Dict, List, Optional, Set, Tuple, Union

from .data.entrance_randomizer_data import entrances_to_game_locations_reverse, relevant_game_locations
from .data.item_data import item_data, ZorkGrandInquisitorItemData
from .data.location_data import location_data, ZorkGrandInquisitorLocationData

from .data.mapping_data import (
    death_cause_labels,
    entrance_names,
    game_location_to_region,
    hotspots_for_regional_hotspot,
    labels_for_enum_items,
    voxam_cast_game_locations,
)

from .data.missable_location_data import (
    missable_location_grant_conditions_data,
    ZorkGrandInquisitorMissableLocationGrantConditionsData,
)

from .data_funcs import game_id_to_items, items_with_tag, locations_with_tag

from .enums import (
    ZorkGrandInquisitorClientSeedInformation,
    ZorkGrandInquisitorCraftableSpellBehaviors,
    ZorkGrandInquisitorDeathsanity,
    ZorkGrandInquisitorEntranceRandomizer,
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorHotspots,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLandmarksanity,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorRegions,
    ZorkGrandInquisitorStartingLocations,
    ZorkGrandInquisitorTags,
)

from .game_state_manager import GameStateManager


class GameController:
    logger: Optional[logging.Logger]

    game_state_manager: GameStateManager

    received_items: Set[ZorkGrandInquisitorItems]
    completed_locations: Set[ZorkGrandInquisitorLocations]

    completed_locations_queue: collections.deque
    received_items_queue: collections.deque

    all_spell_items: Set[ZorkGrandInquisitorItems]
    all_hotspot_items: Set[ZorkGrandInquisitorItems]
    all_goal_items: Set[ZorkGrandInquisitorItems]
    all_trap_items: Set[ZorkGrandInquisitorItems]

    game_id_to_items: Dict[int, ZorkGrandInquisitorItems]

    possible_inventory_items: Set[ZorkGrandInquisitorItems]

    available_inventory_slots: Set[int]

    goal_item_count: int
    goal_completed: bool

    game_location: Optional[str]
    game_location_since: int

    option_goal: Optional[ZorkGrandInquisitorGoals]
    option_artifacts_of_magic_required: Optional[int]
    option_artifacts_of_magic_total: Optional[int]
    option_landmarks_required: Optional[int]
    option_deaths_required: Optional[int]
    option_starting_location: Optional[ZorkGrandInquisitorStartingLocations]
    option_hotspots: Optional[ZorkGrandInquisitorHotspots]
    option_craftable_spells: Optional[ZorkGrandInquisitorCraftableSpellBehaviors]
    option_wild_voxam: Optional[bool]
    option_wild_voxam_chance: Optional[int]
    option_deathsanity: Optional[ZorkGrandInquisitorDeathsanity]
    option_landmarksanity: Optional[ZorkGrandInquisitorLandmarksanity]
    option_entrance_randomizer: Optional[ZorkGrandInquisitorEntranceRandomizer]
    option_entrance_randomizer_include_subway_destinations: Optional[bool]
    option_trap_percentage: Optional[int]
    option_grant_missable_location_checks: Optional[bool]
    option_client_seed_information: Optional[ZorkGrandInquisitorClientSeedInformation]
    option_death_link: Optional[bool]

    starter_kit: Optional[List[str]]
    initial_totemizer_destination: Optional[ZorkGrandInquisitorItems]

    entrance_randomizer_data: Dict[Tuple[str, str], Tuple[str, str]]
    entrance_randomizer_last_locations_visited: collections.deque

    discovered_regions: Set[str]
    discovered_entrances: Set[str]

    received_traps: List[ZorkGrandInquisitorItems]

    active_trap: Optional[ZorkGrandInquisitorItems]
    active_trap_until: Optional[datetime.datetime]

    energy_link_queue: collections.deque
    pause_energy_link_monitoring: bool

    pending_death_link: Tuple[bool, Optional[str], Optional[str]]
    outgoing_death_link: Tuple[bool, Optional[str]]
    pause_death_monitoring: bool

    save_ids: Optional[Tuple[int, int, int]]

    valid_save_message_shown: bool
    invalid_save_message_shown: bool

    def __init__(self, logger=None) -> None:
        self.logger = logger

        self.game_state_manager = GameStateManager()

        self.received_items = set()
        self.completed_locations = set()

        self.completed_locations_queue = collections.deque()
        self.received_items_queue = collections.deque()

        self.all_spell_items = items_with_tag(ZorkGrandInquisitorTags.SPELL)

        self.all_hotspot_items = (
            items_with_tag(ZorkGrandInquisitorTags.HOTSPOT)
            | items_with_tag(ZorkGrandInquisitorTags.SUBWAY_DESTINATION)
            | items_with_tag(ZorkGrandInquisitorTags.TOTEMIZER_DESTINATION)
        )

        self.all_goal_items = {
            ZorkGrandInquisitorItems.ARTIFACT_OF_MAGIC,
            ZorkGrandInquisitorItems.LANDMARK,
            ZorkGrandInquisitorItems.DEATH,
        }

        self.all_trap_items = items_with_tag(ZorkGrandInquisitorTags.TRAP)

        self.game_id_to_items = game_id_to_items()

        self.possible_inventory_items = (
            items_with_tag(ZorkGrandInquisitorTags.INVENTORY_ITEM)
            | items_with_tag(ZorkGrandInquisitorTags.SPELL)
            | items_with_tag(ZorkGrandInquisitorTags.TOTEM)
        )

        self.available_inventory_slots = set()

        self.goal_item_count = 0
        self.goal_completed = False

        self.game_location = None
        self.game_location_since = 0

        self.option_goal = None
        self.option_artifacts_of_magic_required = None
        self.option_artifacts_of_magic_total = None
        self.option_landmarks_required = None
        self.option_deaths_required = None
        self.option_starting_location = None
        self.option_hotspots = None
        self.option_craftable_spells = None
        self.option_wild_voxam = None
        self.option_wild_voxam_chance = None
        self.option_deathsanity = None
        self.option_landmarksanity = None
        self.option_entrance_randomizer = None
        self.option_entrance_randomizer_include_subway_destinations = None
        self.option_trap_percentage = None
        self.option_grant_missable_location_checks = None
        self.option_client_seed_information = None
        self.option_death_link = None

        self.starter_kit = None
        self.initial_totemizer_destination = None

        self.entrance_randomizer_data = dict()
        self.entrance_randomizer_last_locations_visited = collections.deque(maxlen=2)

        self.discovered_regions = {ZorkGrandInquisitorRegions.ANYWHERE.value}
        self.discovered_entrances = set()

        self.received_traps = list()

        self.active_trap = None
        self.active_trap_until = None

        self.energy_link_queue = collections.deque()
        self.pause_energy_link_monitoring = False

        self.pending_death_link = (False, None, None)
        self.outgoing_death_link = (False, None)
        self.pause_death_monitoring = False

        self.save_ids = None

        self.valid_save_message_shown = False
        self.invalid_save_message_shown = False

    @functools.cached_property
    def brog_items(self) -> Set[ZorkGrandInquisitorItems]:
        return {
            ZorkGrandInquisitorItems.BROGS_BICKERING_TORCH,
            ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH,
            ZorkGrandInquisitorItems.BROGS_GRUE_EGG,
            ZorkGrandInquisitorItems.BROGS_PLANK,
        }

    @functools.cached_property
    def griff_items(self) -> Set[ZorkGrandInquisitorItems]:
        return {
            ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP,
            ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN,
        }

    @functools.cached_property
    def lucy_items(self) -> Set[ZorkGrandInquisitorItems]:
        return {
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4,
        }

    @property
    def totem_items(self) -> Set[ZorkGrandInquisitorItems]:
        return self.brog_items | self.griff_items | self.lucy_items

    @property
    def game_location_required_duration(self) -> int:
        if self.option_entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
            return 1000

        return 0

    @functools.cached_property
    def missable_locations(self) -> Set[ZorkGrandInquisitorLocations]:
        return locations_with_tag(ZorkGrandInquisitorTags.MISSABLE)

    @property
    def is_deathsanity(self) -> bool:
        return self.option_deathsanity == ZorkGrandInquisitorDeathsanity.ON

    def log(self, message) -> None:
        if self.logger:
            self.logger.info(message)

    def log_debug(self, message) -> None:
        if self.logger:
            self.logger.debug(message)

    def open_process_handle(self) -> bool:
        return self.game_state_manager.open_process_handle()

    def close_process_handle(self) -> bool:
        return self.game_state_manager.close_process_handle()

    def is_process_running(self) -> bool:
        return self.game_state_manager.is_process_running

    def output_seed_information(self) -> None:
        if self.option_goal is not None:
            self.log("Seed Information:")

            if self.option_client_seed_information == ZorkGrandInquisitorClientSeedInformation.REVEAL_NOTHING:
                self.log("    REDACTED by the Inquisition")
                return

            self.log(f"    Goal: {labels_for_enum_items[self.option_goal]}")

            if self.option_client_seed_information == ZorkGrandInquisitorClientSeedInformation.REVEAL_GOAL:
                return

            if self.option_goal == ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT:
                self.log(f"    Artifacts of Magic Required: {self.option_artifacts_of_magic_required}")
                self.log(f"    Artifacts of Magic Total: {self.option_artifacts_of_magic_total}")
            elif self.option_goal == ZorkGrandInquisitorGoals.ZORK_TOUR:
                self.log(f"    Landmarks Required: {self.option_landmarks_required}")
            elif self.option_goal == ZorkGrandInquisitorGoals.GRIM_JOURNEY:
                self.log(f"    Deaths Required: {self.option_deaths_required}")

            self.log(f"    Starting Location: {labels_for_enum_items[self.option_starting_location]}")
            self.log(f"    Hotspots: {labels_for_enum_items[self.option_hotspots]}")
            self.log(f"    Craftable Spells: {labels_for_enum_items[self.option_craftable_spells]}")

            if self.option_wild_voxam:
                self.log(f"    Wild VOXAM: On ({self.option_wild_voxam_chance}% chance)")
            else:
                self.log(f"    Wild VOXAM: Off")

            self.log(f"    Deathsanity: {labels_for_enum_items[self.option_deathsanity]}")
            self.log(f"    Landmarksanity: {labels_for_enum_items[self.option_landmarksanity]}")
            self.log(f"    Entrance Randomizer: {labels_for_enum_items[self.option_entrance_randomizer]}")

            if self.option_entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
                if self.option_entrance_randomizer_include_subway_destinations:
                    self.log("    Entrance Randomizer - Include Subway Destinations: On")
                else:
                    self.log("    Entrance Randomizer - Include Subway Destinations: Off")

            self.log(f"    Trap Percentage: {self.option_trap_percentage}%")

            if self.option_grant_missable_location_checks:
                self.log(f"    Grant Missable Location Checks: On")
            else:
                self.log(f"    Grant Missable Location Checks: Off")

            if self.option_death_link:
                self.log(f"    Death Link: On")
            else:
                self.log(f"    Death Link: Off")

    def output_starter_kit(self) -> None:
        if self.starter_kit is None:
            return

        self.log("Starter Kit:")

        if len(self.starter_kit):
            item: str
            for item in self.starter_kit:
                if self.option_hotspots == ZorkGrandInquisitorHotspots.ENABLED:
                    if item.startswith("Hotspot"):
                        continue
                elif item in (
                    "Hotspot: Dungeon Master's Lair Entrance",
                    "Hotspot: Spell Lab Bridge Exit",
                ):
                    continue

                self.log(f"    {item}")
        else:
            self.log("    Nothing")

    def output_goal_item_update(self) -> None:
        if self.goal_completed:
            return

        if self.option_goal == ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT:
            self.log(
                f"Received {self.goal_item_count} of {self.option_artifacts_of_magic_required} required Artifacts of Magic"
            )

            if self.goal_item_count >= self.option_artifacts_of_magic_required:
                self.log("All needed Artifacts of Magic have been found! Get to the Walking Castle to win")
        elif self.option_goal == ZorkGrandInquisitorGoals.ZORK_TOUR:
            self.log(
                f"Visited {self.goal_item_count} of {self.option_landmarks_required} required Landmarks"
            )

            if self.goal_item_count >= self.option_landmarks_required:
                self.log("All needed Landmarks have been visited! Get to the Port Foozle signpost to win")
        elif self.option_goal == ZorkGrandInquisitorGoals.GRIM_JOURNEY:
            self.log(
                f"Experienced {self.goal_item_count} of {self.option_deaths_required} required Deaths"
            )

            if self.goal_item_count >= self.option_deaths_required:
                self.log("All needed Deaths have been experienced! Go beyond the gates of hell to win")

    def update(self) -> None:
        if self.game_state_manager.is_process_still_running():
            try:
                self.game_state_manager.refresh_game_location()

                if self.game_state_manager.game_location != self.game_location:
                    self.game_location = self.game_state_manager.game_location
                    self.game_location_since = int(time.time() * 1000)

                if not self._check_for_valid_save():
                    return

                self._apply_initial_totemizer_destination()
                self._apply_starting_location()

                self._apply_permanent_game_state()
                self._apply_conditional_game_state()

                self._apply_permanent_game_flags()

                self._manage_game_location()

                if self.option_entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
                    self._manage_entrance_randomizer()

                self._check_for_completed_locations()

                if self.option_grant_missable_location_checks:
                    self._check_for_missable_locations_to_grant()

                self._process_received_items()

                self._manage_hotspots()
                self._manage_items()

                self._apply_conditional_teleports()

                if self.option_trap_percentage:
                    self._manage_traps()

                if self._player_is_at("dg3e"):
                    self._manage_energy_link()

                if self.option_death_link:
                    self._handle_death_link()

                self._check_for_victory()
            except Exception as e:
                self.log_debug(e)

    def reset(self) -> None:
        self.received_items = set()
        self.completed_locations = set()

        self.completed_locations_queue = collections.deque()
        self.received_items_queue = collections.deque()

        self.available_inventory_slots = set()

        self.goal_item_count = 0
        self.goal_completed = False

        self.game_location = None
        self.game_location_since = 0

        self.option_goal = None
        self.option_artifacts_of_magic_required = None
        self.option_artifacts_of_magic_total = None
        self.option_landmarks_required = None
        self.option_deaths_required = None
        self.option_starting_location = None
        self.option_hotspots = None
        self.option_craftable_spells = None
        self.option_wild_voxam = None
        self.option_wild_voxam_chance = None
        self.option_deathsanity = None
        self.option_landmarksanity = None
        self.option_entrance_randomizer = None
        self.option_entrance_randomizer_include_subway_destinations = None
        self.option_trap_percentage = None
        self.option_grant_missable_location_checks = None
        self.option_client_seed_information = None
        self.option_death_link = None

        self.starter_kit = None
        self.initial_totemizer_destination = None

        self.entrance_randomizer_data = dict()
        self.entrance_randomizer_last_locations_visited = collections.deque(maxlen=2)

        self.discovered_regions = {ZorkGrandInquisitorRegions.ANYWHERE.value}
        self.discovered_entrances = set()

        self.received_traps = list()

        self.active_trap = None
        self.active_trap_until = None

        self.energy_link_queue = collections.deque()
        self.pause_energy_link_monitoring = False

        self.pending_death_link = (False, None, None)
        self.outgoing_death_link = (False, None)
        self.pause_death_monitoring = False

        self.save_ids = None

        self.valid_save_message_shown = False
        self.invalid_save_message_shown = False

    def _check_for_valid_save(self) -> bool:
        if self._player_is_at("gary"):
            return False

        save_ids: Tuple[int, int, int] = (
            self._read_game_state_value_for(19997),
            self._read_game_state_value_for(19998),
            self._read_game_state_value_for(19999),
        )

        if save_ids == (0, 0, 0):
            self._write_game_state_value_for(19997, self.save_ids[0])
            self._write_game_state_value_for(19998, self.save_ids[1])
            self._write_game_state_value_for(19999, self.save_ids[2])
        elif save_ids != self.save_ids:
            if not self.invalid_save_message_shown:
                self.log(
                    "Unexpected save file for this seed. Please load a valid save file or start a new game."
                )

                self.invalid_save_message_shown = True
                self.valid_save_message_shown = False

            return False

        if not self.valid_save_message_shown:
            self.log("Valid save file detected. Have fun!")

            self.valid_save_message_shown = True
            self.invalid_save_message_shown = False

        return True

    def _apply_initial_totemizer_destination(self) -> None:
        if self.initial_totemizer_destination is None:
            return None

        if self._read_game_state_value_for(19986) == 0:
            mapping: Dict[ZorkGrandInquisitorItems, int] = {
                ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION: 0,
                ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_SURFACE_OF_MERZ: 1,
                ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_NEWARK_NEW_JERSEY: 2,
                ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_INFINITY: 3,
                ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL: 4,
            }

            self._write_game_state_value_for(9617, mapping[self.initial_totemizer_destination])
            self._write_game_state_value_for(19986, 1)

    def _apply_starting_location(self, force: bool = False) -> None:
        if self.option_starting_location is None:
            return None

        if self._read_game_state_value_for(19985) == 0 or force:
            if self.option_starting_location == ZorkGrandInquisitorStartingLocations.PORT_FOOZLE:
                self.game_state_manager.set_game_location("ps10", 825)
            elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.CROSSROADS:
                self.game_state_manager.set_game_location("uc10", 1200)
            elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.DM_LAIR:
                self.game_state_manager.set_game_location("dg10", 1410)
            elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR:
                self.game_state_manager.set_game_location("dv10", 1673)
            elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.GUE_TECH:
                self.game_state_manager.set_game_location("tr20", 150)
            elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.SPELL_LAB:
                self.game_state_manager.set_game_location("tp20", 1244)
            elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.HADES_SHORE:
                self.game_state_manager.set_game_location("uh10", 950)
            elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.SUBWAY_FLOOD_CONTROL_DAM:
                self.game_state_manager.set_game_location("ue10", 1578)
            elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.MONASTERY:
                self.game_state_manager.set_game_location("mt20", 0)
            elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.MONASTERY_EXHIBIT:
                self.game_state_manager.set_game_location("me10", 1023)

            self._write_game_state_value_for(19985, 1)
            time.sleep(0.1)

            self.game_state_manager.refresh_game_location()

            if self.game_state_manager.game_location != self.game_location:
                self.game_location = self.game_state_manager.game_location
                self.game_location_since = int(time.time() * 1000)

    def _apply_permanent_game_state(self) -> None:
        self._write_game_state_value_for(10934, 1)  # Rope Taken
        self._write_game_state_value_for(10418, 1)  # Mead Light Taken
        self._write_game_state_value_for(10275, 0)  # Lantern in Crate
        self._write_game_state_value_for(10297, 0)  # Lantern on Jack's Table
        self._write_game_state_value_for(5221, 1)  # Player has Lantern
        self._write_game_state_value_for(13929, 1)  # Great Underground Door Open
        self._write_game_state_value_for(13968, 1)  # Subway Token Taken
        self._write_game_state_value_for(12930, 1)  # Hammer Taken
        self._write_game_state_value_for(12935, 1)  # Griff Totem Taken
        self._write_game_state_value_for(12948, 1)  # ZIMDOR Scroll Taken
        self._write_game_state_value_for(4058, 1)  # Shovel Taken
        self._write_game_state_value_for(4059, 1)  # THROCK Scroll Taken
        self._write_game_state_value_for(11758, 1)  # KENDALL Scroll Taken
        self._write_game_state_value_for(16959, 1)  # Old Scratch Card Taken
        self._write_game_state_value_for(12840, 0)  # Zork Rocks in Perma-Suck Machine
        self._write_game_state_value_for(11886, 1)  # Student ID Taken
        self._write_game_state_value_for(16279, 1)  # Prozork Tablet Taken
        self._write_game_state_value_for(13260, 1)  # GOLGATEM Scroll Taken
        self._write_game_state_value_for(4834, 1)  # Flatheadia Fudge Taken
        self._write_game_state_value_for(4746, 1)  # Jar of Hotbugs Taken
        self._write_game_state_value_for(4755, 1)  # Hungus Lard Taken
        self._write_game_state_value_for(4758, 1)  # Mug Taken
        self._write_game_state_value_for(3716, 1)  # NARWILE Scroll Taken
        self._write_game_state_value_for(17147, 1)  # Lucy Totem Taken
        self._write_game_state_value_for(9818, 1)  # Middle Telegraph Hammer Taken
        self._write_game_state_value_for(5032, 0)  # Always Consider SNAVIG to not be Reassembled
        self._write_game_state_value_for(3766, 0)  # ANS Scroll in Window
        self._write_game_state_value_for(4980, 0)  # ANS Scroll in Window
        self._write_game_state_value_for(3768, 0)  # GIV Scroll in Window
        self._write_game_state_value_for(4978, 0)  # GIV Scroll in Window
        self._write_game_state_value_for(3765, 0)  # SNA Scroll in Window
        self._write_game_state_value_for(4979, 0)  # SNA Scroll in Window
        self._write_game_state_value_for(3767, 0)  # VIG Scroll in Window
        self._write_game_state_value_for(4977, 0)  # VIG Scroll in Window
        self._write_game_state_value_for(15065, 1)  # Brog's Bickering Torch Taken
        self._write_game_state_value_for(15088, 1)  # Brog's Flickering Torch Taken
        self._write_game_state_value_for(2628, 4)  # Brog's Grue Eggs Taken
        self._write_game_state_value_for(2971, 1)  # Brog's Plank Taken
        self._write_game_state_value_for(1340, 1)  # Griff's Inflatable Sea Captain Taken
        self._write_game_state_value_for(1341, 1)  # Griff's Inflatable Raft Taken
        self._write_game_state_value_for(1477, 1)  # Griff's Air Pump Taken
        self._write_game_state_value_for(1814, 1)  # Griff's Dragon Tooth Taken
        self._write_game_state_value_for(15424, 1)  # Initial State of Card Game
        self._write_game_state_value_for(15403, 0)  # Lucy's Cards Taken
        self._write_game_state_value_for(15404, 1)  # Lucy's Cards Taken
        self._write_game_state_value_for(15405, 4)  # Lucy's Cards Taken
        self._write_game_state_value_for(5222, 1)  # User Has Spell Book
        self._write_game_state_value_for(13930, 1)  # Skip Well Cutscenes
        self._write_game_state_value_for(19057, 1)  # Skip Well Cutscenes
        self._write_game_state_value_for(13934, 1)  # Skip Well Cutscenes
        self._write_game_state_value_for(13935, 1)  # Skip Well Cutscenes
        self._write_game_state_value_for(13384, 1)  # Skip Meanwhile... Cutscene
        self._write_game_state_value_for(18275, 1)  # Skip Flashback Cutscene
        self._write_game_state_value_for(8620, 1)  # First Coin Paid to Charon
        self._write_game_state_value_for(8731, 1)  # First Coin Paid to Charon
        self._write_game_state_value_for(191, 1)  # VOXAM Learned
        self._write_game_state_value_for(19243, 0)  # Keep VOXAM Miscast Counter at 0
        self._write_game_state_value_for(15384, 0)  # Never Consider All Artifacts to be Placed

    def _apply_conditional_game_state(self):
        # Teleporter Destinations
        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_CROSSROADS):
            self._write_game_state_value_for(12918, 1)
        else:
            self._write_game_state_value_for(12918, 0)

        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR):
            self._write_game_state_value_for(2203, 1)
        else:
            self._write_game_state_value_for(2203, 0)

        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH):
            self._write_game_state_value_for(7132, 1)
        else:
            self._write_game_state_value_for(7132, 0)

        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB):
            self._write_game_state_value_for(16545, 1)
        else:
            self._write_game_state_value_for(16545, 0)

        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES):
            self._write_game_state_value_for(7119, 1)
        else:
            self._write_game_state_value_for(7119, 0)

        if self._player_has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY):
            self._write_game_state_value_for(7148, 1)
        else:
            self._write_game_state_value_for(7148, 0)

        # Monastery Rope
        if self._player_has(ZorkGrandInquisitorItems.MONASTERY_ROPE):
            self._write_game_state_value_for(9637, 1)
        else:
            self._write_game_state_value_for(9637, 0)

        # Well Rope
        if self._player_has(ZorkGrandInquisitorItems.WELL_ROPE):
            self._write_game_state_value_for(10304, 1)
            self._write_game_state_value_for(13938, 0)
        else:
            self._write_game_state_value_for(10304, 0)
            self._write_game_state_value_for(13938, 1)

        # Pouch of Zorkmids
        if self._player_has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS):
            self._write_game_state_value_for(5827, 1)
        else:
            self._write_game_state_value_for(5827, 0)

        # Cocoa Ingredients
        is_cocoa_brewed: bool = ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU in self.completed_locations

        if self._player_has(ZorkGrandInquisitorItems.COCOA_INGREDIENTS) and not is_cocoa_brewed:
            self._write_game_state_value_for(4750, 1)  # Jar of Hotbugs
            self._write_game_state_value_for(4763, 1)  # Moss of Mareilon
            self._write_game_state_value_for(4766, 1)  # Flatheadia Fudge
            self._write_game_state_value_for(4772, 1)  # Mug
            self._write_game_state_value_for(4769, 1)  # Quelbee Honeycomb
        else:
            self._write_game_state_value_for(4750, 0)
            self._write_game_state_value_for(4763, 0)
            self._write_game_state_value_for(4766, 0)
            self._write_game_state_value_for(4772, 0)
            self._write_game_state_value_for(4769, 0)

        # Brog Torches
        if self._player_is_brog() and self._player_has(ZorkGrandInquisitorItems.BROGS_BICKERING_TORCH):
            self._write_game_state_value_for(10999, 1)
        else:
            self._write_game_state_value_for(10999, 0)

        if self._player_is_brog() and self._player_has(ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH):
            self._write_game_state_value_for(10998, 1)
        else:
            self._write_game_state_value_for(10998, 0)

        # Lucy Strip Grue, Fire, Water Losses
        if self._read_game_state_value_for(14568) < 8:
            self._write_game_state_value_for(14568, 8)

    def _apply_permanent_game_flags(self) -> None:
        self._write_game_flags_value_for(13597, 2)  # Monastery Vent
        self._write_game_flags_value_for(9437, 2)  # Monastery Exhibit Door to Outside
        self._write_game_flags_value_for(3074, 2)  # White House Door
        self._write_game_flags_value_for(13005, 2)  # Map
        self._write_game_flags_value_for(13006, 2)  # Sword
        self._write_game_flags_value_for(13007, 2)  # Sword
        self._write_game_flags_value_for(4854, 2)  # Hungus Lard
        self._write_game_flags_value_for(13389, 2)  # Moss of Mareilon
        self._write_game_flags_value_for(4301, 2)  # Quelbee Honeycomb
        self._write_game_flags_value_for(12895, 2)  # Change Machine Money
        self._write_game_flags_value_for(4150, 2)  # Prozorked Snapdragon
        self._write_game_flags_value_for(13413, 2)  # Letter Opener
        self._write_game_flags_value_for(15403, 2)  # Lucy's Cards
        self._write_game_flags_value_for(4876, 2)  # Cocoa Ingredient - Jar of Hotbugs
        self._write_game_flags_value_for(4877, 2)  # Cocoa Ingredient - Moss of Mareilon
        self._write_game_flags_value_for(4874, 2)  # Cocoa Ingredient - Flatheadia Fudge
        self._write_game_flags_value_for(4875, 2)  # Cocoa Ingredient - Mug
        self._write_game_flags_value_for(4873, 2)  # Cocoa Ingredient - Quelbee Honeycomb
        self._write_game_flags_value_for(10809, 2)  # Back of Jack's Shop
        self._write_game_flags_value_for(10314, 2)  # Well Rope
        self._write_game_flags_value_for(10848, 2)  # Keep Spellbar Enabled (ps10)
        self._write_game_flags_value_for(10862, 2)  # Keep Spellbar Enabled (ps1e)
        self._write_game_flags_value_for(10868, 2)  # Keep Spellbar Enabled (ps20)
        self._write_game_flags_value_for(10302, 2)  # Keep Spellbar Enabled (pc10)
        self._write_game_flags_value_for(10311, 2)  # Keep Spellbar Enabled (pc1e)
        self._write_game_flags_value_for(10918, 2)  # Keep Spellbar Enabled (px10)
        self._write_game_flags_value_for(10967, 2)  # Keep Spellbar Enabled (px1h)
        self._write_game_flags_value_for(10984, 2)  # Keep Spellbar Enabled (px1j)
        self._write_game_flags_value_for(10993, 2)  # Keep Spellbar Enabled (px1k)
        self._write_game_flags_value_for(10414, 2)  # Keep Spellbar Enabled (pe10)
        self._write_game_flags_value_for(10492, 2)  # Keep Spellbar Enabled (pe20)
        self._write_game_flags_value_for(10516, 2)  # Keep Spellbar Enabled (pe2e)
        self._write_game_flags_value_for(10575, 2)  # Keep Spellbar Enabled (pe2j)
        self._write_game_flags_value_for(10589, 2)  # Keep Spellbar Enabled (pe30)
        self._write_game_flags_value_for(10639, 2)  # Keep Spellbar Enabled (pe3k)
        self._write_game_flags_value_for(10659, 2)  # Keep Spellbar Enabled (pe40)
        self._write_game_flags_value_for(10677, 2)  # Keep Spellbar Enabled (pe4g)
        self._write_game_flags_value_for(10697, 2)  # Keep Spellbar Enabled (pe50)
        self._write_game_flags_value_for(10773, 2)  # Keep Spellbar Enabled (pe5h)
        self._write_game_flags_value_for(10756, 2)  # Keep Spellbar Enabled (pe5f)
        self._write_game_flags_value_for(10786, 2)  # Keep Spellbar Enabled (pe6e)
        self._write_game_flags_value_for(10722, 2)  # Keep Spellbar Enabled (pe5e)
        self._write_game_flags_value_for(19603, 2)  # Keep Spellbar Enabled (pe5n)
        self._write_game_flags_value_for(10620, 2)  # Keep Spellbar Enabled (pe3j)
        self._write_game_flags_value_for(10439, 2)  # Keep Spellbar Enabled (pe1e)
        self._write_game_flags_value_for(10805, 2)  # Keep Spellbar Enabled (pp10)
        self._write_game_flags_value_for(10805, 2)  # Keep Spellbar Enabled (pp10)
        self._write_game_flags_value_for(10838, 2)  # Keep Spellbar Enabled (pp1j)
        self._write_game_flags_value_for(8435, 0)  # Always Allow Moving to Hades Phone
        self._write_game_flags_value_for(4991, 0)  # Always Allow Moving to DM Lair Mirror

    def _manage_game_location(self) -> None:
        if self._read_game_state_value_for(19985) == 0:
            return

        if self.game_location not in game_location_to_region:
            return

        # Only register White House - Interior if the player is there as Brog
        if self.game_location == "sg10" and not self._player_is_brog():
            return

        if self._player_is_at_for_at_least(self.game_location, 1000):
            self.discovered_regions.add(game_location_to_region[self.game_location].value)

    def _manage_entrance_randomizer(self) -> None:
        if self._read_game_state_value_for(19985) == 0:
            return

        if self.game_location not in relevant_game_locations:
            return

        entrance_randomizer_last_locations_visited_length: int = len(self.entrance_randomizer_last_locations_visited)

        if entrance_randomizer_last_locations_visited_length == 0:
            self.entrance_randomizer_last_locations_visited.append(self.game_location)
        elif entrance_randomizer_last_locations_visited_length == 1:
            if self.entrance_randomizer_last_locations_visited[0] != self.game_location:
                self.entrance_randomizer_last_locations_visited.append(self.game_location)
        elif entrance_randomizer_last_locations_visited_length == 2:
            if self.entrance_randomizer_last_locations_visited[1] != self.game_location:
                self.entrance_randomizer_last_locations_visited.append(self.game_location)

        if len(self.entrance_randomizer_last_locations_visited) == 2:
            location_pairing_key: str = "-".join(self.entrance_randomizer_last_locations_visited)

            if location_pairing_key in self.entrance_randomizer_data:
                next_game_location: str = "".join(self.entrance_randomizer_data[location_pairing_key].split(" ")[:-1])
                offset: int = int(self.entrance_randomizer_data[location_pairing_key].split(" ")[-1])

                self.game_state_manager.set_game_location(next_game_location, offset)

                entrance_pair: Tuple[str, str] = (
                    self.entrance_randomizer_last_locations_visited[0],
                    self.entrance_randomizer_last_locations_visited[1]
                )

                self.discovered_entrances.add(entrance_names[entrances_to_game_locations_reverse[entrance_pair]])

                self.entrance_randomizer_last_locations_visited.clear()

    def _check_for_completed_locations(self) -> None:
        location: ZorkGrandInquisitorLocations
        data: ZorkGrandInquisitorLocationData
        for location, data in location_data.items():
            if location in self.completed_locations or not isinstance(
                location, ZorkGrandInquisitorLocations
            ):
                continue

            is_location_completed: bool = True

            trigger: Union[str, int, Tuple[int, ...]]
            value: Union[str, int, Tuple[int, ...], Tuple[str, ...]]
            for trigger, value in data.game_state_trigger:
                if trigger == "location":
                    if isinstance(value, str):
                        if not self._player_is_at_for_at_least(value, self.game_location_required_duration):
                            is_location_completed = False
                            break
                    elif isinstance(value, tuple):
                        if not any(
                            self._player_is_at_for_at_least(key, self.game_location_required_duration) for key in value
                        ):
                            is_location_completed = False
                            break
                elif isinstance(trigger, int):
                    if isinstance(value, int):
                        if self._read_game_state_value_for(trigger) != value:
                            is_location_completed = False
                            break
                    elif isinstance(value, tuple):
                        if self._read_game_state_value_for(trigger) not in value:
                            is_location_completed = False
                            break
                    else:
                        is_location_completed = False
                        break
                elif isinstance(trigger, tuple):
                    game_state_values: List[int] = [self._read_game_state_value_for(key) for key in trigger]

                    if value not in game_state_values:
                        is_location_completed = False
                        break
                else:
                    is_location_completed = False
                    break

            if is_location_completed:
                self.completed_locations.add(location)
                self.completed_locations_queue.append(location)

                self._after_location_completed(location)

    def _after_location_completed(self, location: ZorkGrandInquisitorLocations) -> None:
        # Write certain events to unused game state that otherwise don't have a permanent way to track
        if location == ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP:
            self._write_game_state_value_for(19951, 1)
        elif location == ZorkGrandInquisitorLocations.REASSEMBLE_SNAVIG:
            self._write_game_state_value_for(19952, 1)

    def _check_for_missable_locations_to_grant(self) -> None:
        missable_location: ZorkGrandInquisitorLocations
        for missable_location in self.missable_locations:
            if missable_location in self.completed_locations:
                continue

            data: ZorkGrandInquisitorLocationData = location_data[missable_location]

            if ZorkGrandInquisitorTags.DEATHSANITY in data.tags and not self.is_deathsanity:
                continue

            condition_data: ZorkGrandInquisitorMissableLocationGrantConditionsData = (
                missable_location_grant_conditions_data.get(missable_location)
            )

            if condition_data is None:
                self.log_debug(f"Missable Location {missable_location.value} has no grant conditions")
                continue

            if condition_data.game_location_condition is not None:
                if not self._player_is_at_for_at_least(
                    condition_data.game_location_condition, self.game_location_required_duration
                ):
                    continue

            location_condition_intersection: Set[ZorkGrandInquisitorLocations] = (
                set(condition_data.location_condition) & self.completed_locations
            )

            if len(location_condition_intersection):
                grant_location: bool = True

                item: ZorkGrandInquisitorItems
                for item in condition_data.item_conditions or tuple():
                    if self._player_doesnt_have(item):
                        grant_location = False
                        break

                if grant_location:
                    self.completed_locations_queue.append(missable_location)

    def _process_received_items(self) -> None:
        while len(self.received_items_queue) > 0:
            item: ZorkGrandInquisitorItems = self.received_items_queue.popleft()
            data: ZorkGrandInquisitorItemData = item_data[item]

            if ZorkGrandInquisitorTags.FILLER in data.tags:
                continue

            self.received_items.add(item)

            if ZorkGrandInquisitorTags.HOTSPOT_REGIONAL in data.tags:
                hotspot_item: ZorkGrandInquisitorItems
                for hotspot_item in hotspots_for_regional_hotspot[item]:
                    self.received_items.add(hotspot_item)

    def _manage_hotspots(self) -> None:
        hotspot_item: ZorkGrandInquisitorItems
        for hotspot_item in self.all_hotspot_items:
            data: ZorkGrandInquisitorItemData = item_data[hotspot_item]

            if hotspot_item not in self.received_items:
                key: int
                for key in data.statemap_keys:
                    self._write_game_flags_value_for(key, 2)
            else:
                if hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_666_MAILBOX:
                    if self.game_location == "hp5g":
                        if self._read_game_state_value_for(9113) == 0:
                            self._write_game_flags_value_for(9116, 0)
                        else:
                            self._write_game_flags_value_for(9116, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS:
                    if self.game_location == "qb2g":
                        if self._read_game_state_value_for(15433) == 0:
                            self._write_game_flags_value_for(15434, 0)
                        else:
                            self._write_game_flags_value_for(15434, 2)

                        if self._read_game_state_value_for(15435) == 0:
                            self._write_game_flags_value_for(15436, 0)
                        else:
                            self._write_game_flags_value_for(15436, 2)

                        if self._read_game_state_value_for(15437) == 0:
                            self._write_game_flags_value_for(15438, 0)
                        else:
                            self._write_game_flags_value_for(15438, 2)

                        if self._read_game_state_value_for(15439) == 0:
                            self._write_game_flags_value_for(15440, 0)
                        else:
                            self._write_game_flags_value_for(15440, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX:
                    if self.game_location == "tp2g":
                        if self._read_game_state_value_for(12095) == 1:
                            self._write_game_flags_value_for(9115, 2)
                        else:
                            self._write_game_flags_value_for(9115, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_BLINDS:
                    if self.game_location == "dv1e":
                        if self._read_game_state_value_for(4743) == 0:
                            self._write_game_flags_value_for(4799, 0)
                        else:
                            self._write_game_flags_value_for(4799, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_BUCKET:
                    has_well_rope: bool = self._player_has(ZorkGrandInquisitorItems.WELL_ROPE)

                    if self.game_location == "uw10" and has_well_rope:
                        self._write_game_flags_value_for(13928, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS:
                    if self.game_location == "tr5g":
                        key: int
                        for key in data.statemap_keys:
                            self._write_game_flags_value_for(key, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT:
                    if self.game_location == "tr5g":
                        self._write_game_flags_value_for(12702, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_VACUUM_SLOT:
                    if self.game_location == "tr5m":
                        self._write_game_flags_value_for(12909, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CHANGE_MACHINE_SLOT:
                    if self.game_location == "tr5j":
                        if self._read_game_state_value_for(12892) == 0:
                            self._write_game_flags_value_for(12900, 0)
                        else:
                            self._write_game_flags_value_for(12900, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR:
                    if self.game_location == "dw1e":
                        if self._read_game_state_value_for(4983) == 0:
                            self._write_game_flags_value_for(5010, 0)
                        else:
                            self._write_game_flags_value_for(5010, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT:
                    if self.game_location == "me2j":
                        if self._read_game_state_value_for(9491) == 2:
                            self._write_game_flags_value_for(9539, 0)
                        else:
                            self._write_game_flags_value_for(9539, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER:
                    if self.game_location == "me2j":
                        if self._read_game_state_value_for(9546) == 2 or self._read_game_state_value_for(9419) == 1:
                            self._write_game_flags_value_for(19712, 2)
                        else:
                            self._write_game_flags_value_for(19712, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT:
                    if self.game_location == "sg1f":
                        self._write_game_flags_value_for(2586, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DENTED_LOCKER:
                    if self.game_location == "th3j":
                        five_is_open: bool = self._read_game_state_value_for(11847) == 1
                        six_is_open: bool = self._read_game_state_value_for(11840) == 1
                        seven_is_open: bool = self._read_game_state_value_for(11841) == 1
                        eight_is_open: bool = self._read_game_state_value_for(11848) == 1

                        rocks_in_six: bool = self._read_game_state_value_for(11769) == 1
                        six_blasted: bool = self._read_game_state_value_for(11770) == 1

                        if five_is_open or six_is_open or seven_is_open or eight_is_open or rocks_in_six or six_blasted:
                            self._write_game_flags_value_for(11878, 2)
                        else:
                            self._write_game_flags_value_for(11878, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DIRT_MOUND:
                    if self.game_location == "te5e":
                        if self._read_game_state_value_for(11747) == 0:
                            self._write_game_flags_value_for(11751, 0)
                        else:
                            self._write_game_flags_value_for(11751, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DOCK_WINCH:
                    if self.game_location == "pe2e":
                        self._write_game_flags_value_for(15147, 0)
                        self._write_game_flags_value_for(15153, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW:
                    if self.game_location == "cd70":
                        self._write_game_flags_value_for(1705, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS:
                    if self.game_location == "cd3h":
                        raft_in_left: bool = self._read_game_state_value_for(1301) == 1
                        raft_in_right: bool = self._read_game_state_value_for(1304) == 1
                        raft_inflated: bool = self._read_game_state_value_for(1379) == 1

                        captain_in_left: bool = self._read_game_state_value_for(1374) == 1
                        captain_in_right: bool = self._read_game_state_value_for(1381) == 1
                        captain_inflated: bool = self._read_game_state_value_for(1378) == 1

                        left_inflated: bool = (raft_in_left and raft_inflated) or (captain_in_left and captain_inflated)

                        right_inflated: bool = (raft_in_right and raft_inflated) or (
                                captain_in_right and captain_inflated
                        )

                        if left_inflated:
                            self._write_game_flags_value_for(1425, 2)
                        else:
                            self._write_game_flags_value_for(1425, 0)

                        if right_inflated:
                            self._write_game_flags_value_for(1426, 2)
                        else:
                            self._write_game_flags_value_for(1426, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_HOUSE_EXIT:
                    if self.game_location == "dv10":
                        self._write_game_flags_value_for(4791, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE:
                    if self.game_location == "uc3e":
                        if self._read_game_state_value_for(13060) == 0:
                            self._write_game_flags_value_for(13106, 0)
                        else:
                            self._write_game_flags_value_for(13106, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS:
                    if self.game_location == "ue1e":
                        if self._read_game_state_value_for(14318) == 0:
                            self._write_game_flags_value_for(13219, 0)
                            self._write_game_flags_value_for(13220, 0)
                            self._write_game_flags_value_for(13221, 0)
                            self._write_game_flags_value_for(13222, 0)
                        else:
                            self._write_game_flags_value_for(13219, 2)
                            self._write_game_flags_value_for(13220, 2)
                            self._write_game_flags_value_for(13221, 2)
                            self._write_game_flags_value_for(13222, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS:
                    if self.game_location == "ue1e":
                        if self._read_game_state_value_for(14318) == 0:
                            self._write_game_flags_value_for(14327, 0)
                            self._write_game_flags_value_for(14332, 0)
                            self._write_game_flags_value_for(14337, 0)
                            self._write_game_flags_value_for(14342, 0)
                        else:
                            self._write_game_flags_value_for(14327, 2)
                            self._write_game_flags_value_for(14332, 2)
                            self._write_game_flags_value_for(14337, 2)
                            self._write_game_flags_value_for(14342, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT:
                    if self.game_location == "tr5e":
                        self._write_game_flags_value_for(12528, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS:
                    if self.game_location == "tr5e":
                        if self._read_game_state_value_for(12220) == 0:
                            self._write_game_flags_value_for(12523, 2)
                            self._write_game_flags_value_for(12524, 2)
                            self._write_game_flags_value_for(12525, 2)
                        else:
                            self._write_game_flags_value_for(12523, 0)
                            self._write_game_flags_value_for(12524, 0)
                            self._write_game_flags_value_for(12525, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE:
                    if self.game_location == "uc1g":
                        if self._read_game_state_value_for(12931) == 1 or self._read_game_state_value_for(12929) == 1:
                            self._write_game_flags_value_for(13002, 2)
                        else:
                            self._write_game_flags_value_for(13002, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL:
                    if self.game_location == "pe5e":
                        if self._read_game_state_value_for(10277) == 0:
                            self._write_game_flags_value_for(10726, 0)
                        else:
                            self._write_game_flags_value_for(10726, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR:
                    if self.game_location == "tr1k":
                        if self._read_game_state_value_for(12212) == 0:
                            self._write_game_flags_value_for(12280, 0)
                        else:
                            self._write_game_flags_value_for(12280, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_GRASS:
                    if self.game_location in ("te10", "te1g", "te20", "te30", "te40"):
                        key: int
                        for key in data.statemap_keys:
                            self._write_game_flags_value_for(key, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_WINDOWS:
                    if self.game_location == "te3e":
                        if self._read_game_state_value_for(11536) == 1:
                            self._write_game_flags_value_for(11543, 0)
                    elif self.game_location == "tr1g":
                        self._write_game_flags_value_for(12256, 0)
                    elif self.game_location == "te40":
                        self._write_game_flags_value_for(11720, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS:
                    if self.game_location == "hp1e":
                        if self._read_game_state_value_for(8431) == 1:
                            key: int
                            for key in data.statemap_keys:
                                self._write_game_flags_value_for(key, 0)
                        else:
                            key: int
                            for key in data.statemap_keys:
                                self._write_game_flags_value_for(key, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER:
                    if self.game_location == "hp1e":
                        if self._read_game_state_value_for(8431) == 1:
                            self._write_game_flags_value_for(8446, 2)
                        else:
                            self._write_game_flags_value_for(8446, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_HARRY:
                    if self.game_location == "dg4e":
                        if self._read_game_state_value_for(4237) == 1 and self._read_game_state_value_for(4034) == 1:
                            self._write_game_flags_value_for(4260, 2)
                        else:
                            self._write_game_flags_value_for(4260, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY:
                    if self.game_location == "dg4h":
                        if self._read_game_state_value_for(4279) == 1:
                            self._write_game_flags_value_for(18026, 2)
                        else:
                            self._write_game_flags_value_for(18026, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH:
                    if self.game_location == "dg4g":
                        if self._read_game_state_value_for(4034) == 1:
                            self._write_game_flags_value_for(17623, 2)
                        else:
                            self._write_game_flags_value_for(17623, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR:
                    if self.game_location == "uc4e":
                        if self._read_game_state_value_for(13062) == 1:
                            self._write_game_flags_value_for(13140, 2)
                        else:
                            self._write_game_flags_value_for(13140, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR:
                    if self.game_location == "pe1e":
                        if self._read_game_state_value_for(10451) == 1:
                            self._write_game_flags_value_for(10441, 2)
                        else:
                            self._write_game_flags_value_for(10441, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_LOUDSPEAKER_VOLUME_BUTTONS:
                    if self.game_location == "pe2j":
                        self._write_game_flags_value_for(19632, 0)
                        self._write_game_flags_value_for(19627, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_DOOR:
                    if self.game_location == "sw4e":
                        if self._read_game_state_value_for(2989) == 1:
                            self._write_game_flags_value_for(3025, 2)
                        else:
                            self._write_game_flags_value_for(3025, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG:
                    if self.game_location == "sw4e":
                        self._write_game_flags_value_for(3036, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_MIRROR:
                    if self.game_location == "dw1f":
                        self._write_game_flags_value_for(5031, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_MOSSY_GRATE:
                    if self.game_location == "ue2g":
                        if self._read_game_state_value_for(13278) == 0:
                            self._write_game_flags_value_for(13390, 0)
                        else:
                            self._write_game_flags_value_for(13390, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR:
                    if self.game_location == "qe1e":
                        if self._player_is_brog():
                            self._write_game_flags_value_for(2447, 0)
                        elif self._player_is_griff():
                            self._write_game_flags_value_for(2455, 0)
                        elif self._player_is_lucy():
                            if self._read_game_state_value_for(2457) == 0:
                                self._write_game_flags_value_for(2455, 0)
                            else:
                                self._write_game_flags_value_for(2455, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS:
                    if self.game_location == "tr3h":
                        if self._read_game_state_value_for(11777) == 1:
                            self._write_game_flags_value_for(12389, 2)
                        else:
                            self._write_game_flags_value_for(12389, 0)

                        self._write_game_state_value_for(12390, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE:
                    if self.game_location == "dg4f":
                        if self._read_game_state_value_for(4241) == 1:
                            self._write_game_flags_value_for(4302, 2)
                        else:
                            self._write_game_flags_value_for(4302, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE:
                    if self.game_location == "tp1e":
                        if self._read_game_state_value_for(16342) == 1:
                            self._write_game_flags_value_for(16383, 2)
                            self._write_game_flags_value_for(16384, 2)
                        else:
                            self._write_game_flags_value_for(16383, 0)
                            self._write_game_flags_value_for(16384, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE:
                    if self.game_location == "sg6e":
                        if self._read_game_state_value_for(15715) == 1:
                            self._write_game_flags_value_for(2769, 2)
                            self._write_game_flags_value_for(2761, 2)
                            self._write_game_flags_value_for(2764, 2)
                            self._write_game_flags_value_for(2767, 2)
                        else:
                            self._write_game_flags_value_for(2769, 0)
                            self._write_game_flags_value_for(2761, 0)
                            self._write_game_flags_value_for(2764, 0)
                            self._write_game_flags_value_for(2767, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON:
                    if self.game_location == "dg2f":
                        if self._read_game_state_value_for(4114) == 1 or self._read_game_state_value_for(4115) == 1:
                            self._write_game_flags_value_for(4149, 2)
                        else:
                            self._write_game_flags_value_for(4149, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_BUTTONS:
                    if self.game_location == "tr5f":
                        self._write_game_flags_value_for(12584, 0)
                        self._write_game_flags_value_for(12585, 0)
                        self._write_game_flags_value_for(12586, 0)
                        self._write_game_flags_value_for(12587, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_COIN_SLOT:
                    if self.game_location == "tr5f":
                        self._write_game_flags_value_for(12574, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT:
                    if self.game_location == "ue2j":
                        if self._read_game_state_value_for(13408) == 1:
                            self._write_game_flags_value_for(13412, 2)
                        else:
                            self._write_game_flags_value_for(13412, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER:
                    if self.game_location == "tp4g":
                        self._write_game_flags_value_for(12170, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_BRIDGE_EXIT:
                    if self.game_location == "tp10":
                        self._write_game_flags_value_for(12045, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM:
                    if self.game_location == "tp1e":
                        if self._read_game_state_value_for(16342) == 1 and self._read_game_state_value_for(16374) == 0:
                            self._write_game_flags_value_for(16382, 0)
                        else:
                            self._write_game_flags_value_for(16382, 2)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM:
                    if self.game_location == "dg3e":
                        self._write_game_flags_value_for(4209, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE:
                    if self.game_location == "th3r":
                        self._write_game_flags_value_for(11973, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT:
                    if self.game_location == "uc6e":
                        self._write_game_flags_value_for(13168, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY:
                    if self.game_location == "qb2e":
                        if self._read_game_state_value_for(15395) == 1:
                            self._write_game_flags_value_for(15396, 2)
                        else:
                            self._write_game_flags_value_for(15396, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH:
                    if self.game_location == "mt2e":
                        self._write_game_flags_value_for(9706, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS:
                    if self.game_location == "mt2g":
                        self._write_game_flags_value_for(9728, 0)
                        self._write_game_flags_value_for(9729, 0)
                        self._write_game_flags_value_for(9730, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.SUBWAY_DESTINATION_CROSSROADS:
                    if self.game_location == "us2e":
                        self._write_game_flags_value_for(13760, 0)
                    elif self.game_location == "ue2e":
                        self._write_game_flags_value_for(13323, 0)
                    elif self.game_location == "uh2e":
                        self._write_game_flags_value_for(13512, 0)
                    elif self.game_location == "um2e":
                        self._write_game_flags_value_for(13651, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM:
                    if self.game_location == "us2e":
                        self._write_game_flags_value_for(13757, 0)
                    elif self.game_location == "ue2e":
                        self._write_game_flags_value_for(13297, 0)
                    elif self.game_location == "uh2e":
                        self._write_game_flags_value_for(13486, 0)
                    elif self.game_location == "um2e":
                        self._write_game_flags_value_for(13625, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES:
                    if self.game_location == "us2e":
                        self._write_game_flags_value_for(13758, 0)
                    elif self.game_location == "ue2e":
                        self._write_game_flags_value_for(13309, 0)
                    elif self.game_location == "uh2e":
                        self._write_game_flags_value_for(13498, 0)
                    elif self.game_location == "um2e":
                        self._write_game_flags_value_for(13637, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY:
                    if self.game_location == "us2e":
                        self._write_game_flags_value_for(13759, 0)
                    elif self.game_location == "ue2e":
                        self._write_game_flags_value_for(13316, 0)
                    elif self.game_location == "uh2e":
                        self._write_game_flags_value_for(13505, 0)
                    elif self.game_location == "um2e":
                        self._write_game_flags_value_for(13644, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION:
                    if self.game_location == "mt1f":
                        self._write_game_flags_value_for(9660, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_SURFACE_OF_MERZ:
                    if self.game_location == "mt1f":
                        self._write_game_flags_value_for(9662, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_NEWARK_NEW_JERSEY:
                    if self.game_location == "mt1f":
                        self._write_game_flags_value_for(9664, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_INFINITY:
                    if self.game_location == "mt1f":
                        self._write_game_flags_value_for(9666, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL:
                    if self.game_location == "mt1f":
                        self._write_game_flags_value_for(9668, 0)

    def _manage_items(self) -> None:
        if self._player_is_afgncaap():
            self.available_inventory_slots = self._determine_available_inventory_slots()

            received_inventory_items: Set[ZorkGrandInquisitorItems]
            received_inventory_items = self.received_items & self.possible_inventory_items

            received_inventory_items = self._filter_received_inventory_items(received_inventory_items)
        elif self._player_is_totem():
            self.available_inventory_slots = self._determine_available_inventory_slots(is_totem=True)

            received_inventory_items: Set[ZorkGrandInquisitorItems]

            if self._player_is_brog():
                received_inventory_items = self.received_items & self.brog_items
                received_inventory_items = self._filter_received_brog_inventory_items(received_inventory_items)
            elif self._player_is_griff():
                received_inventory_items = self.received_items & self.griff_items
                received_inventory_items = self._filter_received_griff_inventory_items(received_inventory_items)
            elif self._player_is_lucy():
                received_inventory_items = self.received_items & self.lucy_items
                received_inventory_items = self._filter_received_lucy_inventory_items(received_inventory_items)
            else:
                return None
        else:
            return None

        game_state_inventory_items: Set[ZorkGrandInquisitorItems] = self._determine_game_state_inventory()

        inventory_items_to_remove: Set[ZorkGrandInquisitorItems]
        inventory_items_to_remove = game_state_inventory_items - received_inventory_items

        inventory_items_to_add: Set[ZorkGrandInquisitorItems]
        inventory_items_to_add = received_inventory_items - game_state_inventory_items

        item: ZorkGrandInquisitorItems
        for item in inventory_items_to_remove:
            self._remove_from_inventory(item)

        item: ZorkGrandInquisitorItems
        for item in inventory_items_to_add:
            self._add_to_inventory(item)

        # Item Deduplication (Just in Case)
        seen_items: Set[int] = set()

        i: int
        for i in range(151, 171):
            item: int = self._read_game_state_value_for(i)

            if item in seen_items:
                self._write_game_state_value_for(i, 0)
            else:
                seen_items.add(item)

    def _apply_conditional_teleports(self) -> None:
        # Skip Well Cutscene
        if self._player_is_at("uw1x"):
            self.game_state_manager.set_game_location("uw10", 0)

        # Skip Y'Gael Cutscene
        if self._player_is_at("ej10"):
            self.game_state_manager.set_game_location("uc10", 1200)

        # Skip Power Outage Cutscene
        if self._player_is_at("ue1q"):
            self.game_state_manager.set_game_location("ue1e", 0)

        # Bucket -> Surface
        if self._player_is_at("uw1k") and self._read_game_state_value_for(13938) == 0:
            self.game_state_manager.set_game_location("pc10", 250)

        # Monastery Subway Station -> Monastery
        if self._player_is_at("um1e") and self._read_game_state_value_for(9637) == 1:
            self.game_state_manager.set_game_location("mt10", 1531)

        # VOXAM Cast
        zork_rocks_inert: bool = self._read_game_state_value_for(11767) == 0

        if self._read_game_state_value_for(9) == 224:
            time.sleep(0.1)
            self._write_game_state_value_for(9, 0)

            if zork_rocks_inert:
                self._cast_voxam()

    def _cast_voxam(self, force_wild: bool = False) -> None:
        if self.option_entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
            self.entrance_randomizer_last_locations_visited.clear()

        if not self.option_wild_voxam and not force_wild:
            self._apply_starting_location(force=True)
            return None

        voxam_roll: int = random.randint(1, 100)

        if (voxam_roll <= self.option_wild_voxam_chance) or force_wild:
            starting_location: ZorkGrandInquisitorStartingLocations = (
                random.choice(tuple(voxam_cast_game_locations.keys()))
            )

            game_location: Tuple[Tuple[str, int], ...] = (
                random.choice(voxam_cast_game_locations[starting_location])
            )

            game_location_offset: int = 0

            if game_location[1] == 1:
                game_location_offset = random.randint(0, 1800)

            self.game_state_manager.set_game_location(
                game_location[0], game_location_offset
            )
        else:
            self._apply_starting_location(force=True)

    def _manage_traps(self) -> None:
        if not self._player_is_afgncaap() or self._read_game_state_value_for(19985) == 0:
            return None

        zork_rocks_inert: bool = self._read_game_state_value_for(11767) == 0

        if not zork_rocks_inert:
            return None

        if self.active_trap_until:
            if datetime.datetime.now() > self.active_trap_until:
                if self.active_trap == ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS:
                    self._deactivate_trap_reverse_controls()
                elif self.active_trap == ZorkGrandInquisitorItems.TRAP_ZVISION:
                    self._deactivate_trap_zvision()

                self.active_trap = None
                self.active_trap_until = None

        if self.active_trap is not None:
            if self.active_trap == ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS:
                self._activate_trap_reverse_controls()
            elif self.active_trap == ZorkGrandInquisitorItems.TRAP_ZVISION:
                self._activate_trap_zvision()

            return None

        processed_trap_counters: Dict[ZorkGrandInquisitorItems, int] = {
            ZorkGrandInquisitorItems.TRAP_INFINITE_CORRIDOR: self._read_game_state_value_for(19990),
            ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS: self._read_game_state_value_for(19991),
            ZorkGrandInquisitorItems.TRAP_TELEPORT: self._read_game_state_value_for(19992),
            ZorkGrandInquisitorItems.TRAP_ZVISION: self._read_game_state_value_for(19993),
        }

        traps_remaining: int = len(self.received_traps) - sum(processed_trap_counters.values()) - 1
        traps_remaining_message: str = f"Traps remaining: {traps_remaining}" if traps_remaining else ""

        trap: ZorkGrandInquisitorItems
        for trap in self.received_traps:
            if processed_trap_counters[trap]:
                processed_trap_counters[trap] -= 1
                continue

            game_state_key: int = -1
            if trap == ZorkGrandInquisitorItems.TRAP_INFINITE_CORRIDOR:
                game_state_key = 19990

                if not self._player_is_at_starting_location():
                    self._activate_trap_infinite_corridor()
                    self.log(f"Infinite Corridor Trap! {traps_remaining_message}")
            elif trap == ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS:
                game_state_key = 19991

                if not self._player_is_at_starting_location():
                    self.active_trap = ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS
                    self.active_trap_until = datetime.datetime.now() + datetime.timedelta(seconds=30)

                    self._activate_trap_reverse_controls()

                    self.log(f"Reverse Controls Trap for 30 seconds! {traps_remaining_message}")
            elif trap == ZorkGrandInquisitorItems.TRAP_TELEPORT:
                game_state_key = 19992

                if not self._player_is_at_starting_location():
                    self._activate_trap_teleport()
                    self.log(f"Teleport Trap! {traps_remaining_message}")
            elif trap == ZorkGrandInquisitorItems.TRAP_ZVISION:
                game_state_key = 19993

                if not self._player_is_at_starting_location():
                    self.active_trap = ZorkGrandInquisitorItems.TRAP_ZVISION
                    self.active_trap_until = datetime.datetime.now() + datetime.timedelta(seconds=30)

                    self._activate_trap_zvision()

                    self.log(f"ZVision Trap for 30 seconds! {traps_remaining_message}")

            current_count: int = self._read_game_state_value_for(game_state_key)
            self._write_game_state_value_for(game_state_key, current_count + 1)

            break

    def _activate_trap_infinite_corridor(self) -> None:
        if self.option_entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
            self.entrance_randomizer_last_locations_visited.clear()

        depth = random.randint(10, 20)

        self._write_game_state_value_for(11005, depth)
        self.game_state_manager.set_game_location("th20", random.randint(0, 1800))

        time.sleep(0.1)

        self._write_game_state_value_for(11005, depth)

    def _activate_trap_reverse_controls(self) -> None:
        self.game_state_manager.set_panorama_reversed(True)

    def _deactivate_trap_reverse_controls(self) -> None:
        self.game_state_manager.set_panorama_reversed(False)

    def _activate_trap_teleport(self) -> None:
        self._cast_voxam(force_wild=True)
        time.sleep(0.1)

    def _activate_trap_zvision(self) -> None:
        self.game_state_manager.set_zvision(True)

    def _deactivate_trap_zvision(self) -> None:
        self.game_state_manager.set_zvision(False)

    def _manage_energy_link(self) -> None:
        mushroom_hammered: bool = self._read_game_state_value_for(4217) == 1
        mushroom_hammered_throck: bool = self._read_game_state_value_for(4219) == 1
        mushroom_hammered_snapdragon: bool = self._read_game_state_value_for(4220) == 1
        mushroom_hammered_snapdragon_throck: bool = self._read_game_state_value_for(4222) == 1

        any_mushroom_hammered: bool = (
            mushroom_hammered
            or mushroom_hammered_throck
            or mushroom_hammered_snapdragon
            or mushroom_hammered_snapdragon_throck
        )

        # Pause Monitoring Flag
        if self.pause_energy_link_monitoring and not any_mushroom_hammered:
            self.pause_energy_link_monitoring = False

        if not self.pause_energy_link_monitoring and any_mushroom_hammered:
            # Contribute Energy
            if mushroom_hammered:
                self.energy_link_queue.append(750)
            elif mushroom_hammered_throck:
                self.energy_link_queue.append(1500)
            elif mushroom_hammered_snapdragon:
                self.energy_link_queue.append(750)
            elif mushroom_hammered_snapdragon_throck:
                self.energy_link_queue.append(1500)

            self.pause_energy_link_monitoring = True

    def _handle_death_link(self) -> None:
        # Pause Monitoring Flag
        if self.pause_death_monitoring and not self._player_is_at("gjde"):
            self.pause_death_monitoring = False

        # Incoming Death Link
        if not self._player_is_at("gjde") and self.pending_death_link[0]:
            self._write_game_state_value_for(2201, 35)
            self.game_state_manager.set_game_location("gjde", 0)

            if self.pending_death_link[2]:
                self.log(f"Death Link: {self.pending_death_link[2]}")
            else:
                self.log(f"Death Link: Triggered by {self.pending_death_link[1]}")

            self.pending_death_link = (False, None, None)

        # Outgoing Death Link
        if not self.pause_death_monitoring:
            death_cause_id: int = self._read_game_state_value_for(2201)

            if self._player_is_at("gjde") and death_cause_id != 35:
                death_cause: str = death_cause_labels.get(
                    death_cause_id,
                    "PLAYER died of unknown causes"
                )

                self.outgoing_death_link = (True, death_cause)
                self.pause_death_monitoring = True

    def _check_for_victory(self) -> None:
        duration: int = self.game_location_required_duration

        if self.option_goal == ZorkGrandInquisitorGoals.THREE_ARTIFACTS:
            coconut_is_placed = self._read_game_state_value_for(2200) == 1
            cube_is_placed = self._read_game_state_value_for(2322) == 1
            skull_is_placed = self._read_game_state_value_for(2321) == 1

            self.goal_completed = coconut_is_placed and cube_is_placed and skull_is_placed
        elif self.option_goal == ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT:
            if self.goal_item_count >= self.option_artifacts_of_magic_required:
                if self._player_is_at_for_at_least("dc10", duration) and self._player_is_afgncaap():
                    self.goal_completed = True
        elif self.option_goal == ZorkGrandInquisitorGoals.SPELL_HEIST:
            if not len(self.all_spell_items - self.received_items):
                if self._player_is_at_for_at_least("ps1e", duration):
                    self.goal_completed = True
        elif self.option_goal == ZorkGrandInquisitorGoals.ZORK_TOUR:
            if self.goal_item_count >= self.option_landmarks_required:
                if self._player_is_at_for_at_least("ps1e", duration):
                    self.goal_completed = True
        elif self.option_goal == ZorkGrandInquisitorGoals.GRIM_JOURNEY:
            if self.goal_item_count >= self.option_deaths_required:
                if self._player_is_at_for_at_least("hp60", duration):
                    self.goal_completed = True

    def _determine_game_state_inventory(self) -> Set[ZorkGrandInquisitorItems]:
        game_state_inventory: Set[ZorkGrandInquisitorItems] = set()

        # Item on Cursor
        item_on_cursor: int = self._read_game_state_value_for(9)

        if item_on_cursor != 0:
            if item_on_cursor in self.game_id_to_items:
                game_state_inventory.add(self.game_id_to_items[item_on_cursor])

        # Item in Inspector
        item_in_inspector: int = 0

        if self._player_is_afgncaap():
            item_in_inspector = self._read_game_state_value_for(4512)
        elif self._player_is_brog():
            item_in_inspector = self._read_game_state_value_for(2194)
        elif self._player_is_griff():
            item_in_inspector = self._read_game_state_value_for(2196)
        elif self._player_is_lucy():
            item_in_inspector = self._read_game_state_value_for(2198)

        if item_in_inspector != 0:
            if item_in_inspector in self.game_id_to_items:
                game_state_inventory.add(self.game_id_to_items[item_in_inspector])

        # Items in Inventory Slots
        i: int
        for i in range(151, 171):
            if self._read_game_state_value_for(i) != 0:
                if self._read_game_state_value_for(i) in self.game_id_to_items:
                    game_state_inventory.add(
                        self.game_id_to_items[self._read_game_state_value_for(i)]
                    )

        # Pouch of Zorkmids
        if self._read_game_state_value_for(5827) == 1:
            game_state_inventory.add(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS)

        # Spells
        i: int
        for i in range(192, 203):
            if self._read_game_state_value_for(i) == 1:
                if i in self.game_id_to_items:
                    game_state_inventory.add(self.game_id_to_items[i])

        # Totems
        if self._read_game_state_value_for(4853) == 1:
            game_state_inventory.add(ZorkGrandInquisitorItems.TOTEM_BROG)

        if self._read_game_state_value_for(4315) == 1:
            game_state_inventory.add(ZorkGrandInquisitorItems.TOTEM_GRIFF)

        if self._read_game_state_value_for(5223) == 1:
            game_state_inventory.add(ZorkGrandInquisitorItems.TOTEM_LUCY)

        return game_state_inventory

    def _add_to_inventory(self, item: ZorkGrandInquisitorItems) -> None:
        data: ZorkGrandInquisitorItemData = item_data[item]

        if data.statemap_keys is None:
            return None

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            if len(self.available_inventory_slots):  # Inventory slot overflow protection
                inventory_slot: int = self.available_inventory_slots.pop()
                self._write_game_state_value_for(inventory_slot, data.statemap_keys[0])
        elif ZorkGrandInquisitorTags.SPELL in data.tags:
            self._write_game_state_value_for(data.statemap_keys[0], 1)
        elif ZorkGrandInquisitorTags.TOTEM in data.tags:
            self._write_game_state_value_for(data.statemap_keys[0], 1)

    def _remove_from_inventory(self, item: ZorkGrandInquisitorItems) -> None:
        data: ZorkGrandInquisitorItemData = item_data[item]

        if data.statemap_keys is None:
            return None

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            inventory_slot: Optional[int] = self._inventory_slot_for(item)

            if inventory_slot is None:
                return None

            self._write_game_state_value_for(inventory_slot, 0)

            if inventory_slot != 9:
                self.available_inventory_slots.add(inventory_slot)
        elif ZorkGrandInquisitorTags.SPELL in data.tags:
            self._write_game_state_value_for(data.statemap_keys[0], 0)
        elif ZorkGrandInquisitorTags.TOTEM in data.tags:
            self._write_game_state_value_for(data.statemap_keys[0], 0)

    def _determine_available_inventory_slots(self, is_totem: bool = False) -> Set[int]:
        available_inventory_slots: Set[int] = set()

        inventory_slot_range_end: int = 171

        if is_totem:
            if self._player_is_brog():
                inventory_slot_range_end = 161
            elif self._player_is_griff():
                inventory_slot_range_end = 160
            elif self._player_is_lucy():
                inventory_slot_range_end = 157

        i: int
        for i in range(151, inventory_slot_range_end):
            if self._read_game_state_value_for(i) == 0:
                available_inventory_slots.add(i)

        return available_inventory_slots

    def _inventory_slot_for(self, item) -> Optional[int]:
        data: ZorkGrandInquisitorItemData = item_data[item]

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            i: int
            for i in range(151, 171):
                if self._read_game_state_value_for(i) == data.statemap_keys[0]:
                    return i

        if self._read_game_state_value_for(9) == data.statemap_keys[0]:
            return 9

        if self._read_game_state_value_for(4512) == data.statemap_keys[0]:
            return 4512

        return None

    def _filter_received_inventory_items(
        self, received_inventory_items: Set[ZorkGrandInquisitorItems]
    ) -> Set[ZorkGrandInquisitorItems]:
        to_filter_inventory_items: Set[ZorkGrandInquisitorItems] = self.totem_items

        inventory_item_values: Set[int] = set()

        i: int
        for i in range(151, 171):
            inventory_item_value: int = self._read_game_state_value_for(i)

            # Always get rid of blue sword. Causes issues with ER
            if inventory_item_value == 100:
                inventory_item_value = 21
                self._write_game_state_value_for(i, inventory_item_value)

            inventory_item_values.add(inventory_item_value)

        cursor_item_value: int = self._read_game_state_value_for(9)
        inspector_item_value: int = self._read_game_state_value_for(4512)

        inventory_item_values.add(cursor_item_value)
        inventory_item_values.add(inspector_item_value)

        item: ZorkGrandInquisitorItems
        for item in received_inventory_items:
            if item == ZorkGrandInquisitorItems.HUNGUS_LARD:
                if self._read_game_state_value_for(4870) == 1:
                    to_filter_inventory_items.add(item)
                elif (
                    self._read_game_state_value_for(4244) == 1
                    and self._read_game_state_value_for(4309) == 0
                ):
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER:
                if self._read_game_state_value_for(9491) == 3:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.MAP:
                if self._read_game_state_value_for(16618) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.MEAD_LIGHT:
                if 105 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(17620) > 0:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(4034) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.OLD_SCRATCH_CARD:
                if 32 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(12892) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.PERMA_SUCK_MACHINE:
                if self._read_game_state_value_for(12218) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.PLASTIC_SIX_PACK_HOLDER:
                if self._read_game_state_value_for(15150) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(10421) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.PROZORK_TABLET:
                if self._read_game_state_value_for(4115) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SANDWITCH_WRAPPER:
                if self._read_game_state_value_for(19951) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS:
                if 41 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(19952) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV:
                if 48 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(19952) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SNAPDRAGON:
                if self._read_game_state_value_for(4199) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.STUDENT_ID:
                if self._read_game_state_value_for(11838) == 1:
                    if self._read_game_state_value_for(9) != 39:
                        to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SUBWAY_TOKEN:
                if self._read_game_state_value_for(13167) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.SWORD:
                if 22 in inventory_item_values:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.ZIMDOR_SCROLL:
                if self._read_game_state_value_for(12167) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.ZORK_ROCKS:
                if self._read_game_state_value_for(12486) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(12487) == 1:
                    to_filter_inventory_items.add(item)
                elif 52 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(11769) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(11840) == 1:
                    to_filter_inventory_items.add(item)

        return received_inventory_items - to_filter_inventory_items

    def _filter_received_brog_inventory_items(
        self, received_inventory_items: Set[ZorkGrandInquisitorItems]
    ) -> Set[ZorkGrandInquisitorItems]:
        to_filter_inventory_items: Set[ZorkGrandInquisitorItems] = set()

        inventory_item_values: Set[int] = set()

        i: int
        for i in range(151, 161):
            inventory_item_values.add(self._read_game_state_value_for(i))

        cursor_item_value: int = self._read_game_state_value_for(9)
        inspector_item_value: int = self._read_game_state_value_for(2194)

        inventory_item_values.add(cursor_item_value)
        inventory_item_values.add(inspector_item_value)

        item: ZorkGrandInquisitorItems
        for item in received_inventory_items:
            if item == ZorkGrandInquisitorItems.BROGS_BICKERING_TORCH:
                if 103 in inventory_item_values:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH:
                if 104 in inventory_item_values:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.BROGS_GRUE_EGG:
                if self._read_game_state_value_for(2577) == 1:
                    to_filter_inventory_items.add(item)
                elif 71 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(2641) == 1:
                    to_filter_inventory_items.add(item)

        return received_inventory_items - to_filter_inventory_items

    def _filter_received_griff_inventory_items(
        self, received_inventory_items: Set[ZorkGrandInquisitorItems]
    ) -> Set[ZorkGrandInquisitorItems]:
        to_filter_inventory_items: Set[ZorkGrandInquisitorItems] = set()

        inventory_item_values: Set[int] = set()

        i: int
        for i in range(151, 160):
            inventory_item_values.add(self._read_game_state_value_for(i))

        cursor_item_value: int = self._read_game_state_value_for(9)
        inspector_item_value: int = self._read_game_state_value_for(4512)

        inventory_item_values.add(cursor_item_value)
        inventory_item_values.add(inspector_item_value)

        item: ZorkGrandInquisitorItems
        for item in received_inventory_items:
            if item == ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT:
                if self._read_game_state_value_for(1301) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(1304) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(16562) == 1:
                    to_filter_inventory_items.add(item)
            if item == ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN:
                if self._read_game_state_value_for(1374) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(1381) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(16562) == 1:
                    to_filter_inventory_items.add(item)

        return received_inventory_items - to_filter_inventory_items

    def _filter_received_lucy_inventory_items(
        self, received_inventory_items: Set[ZorkGrandInquisitorItems]
    ) -> Set[ZorkGrandInquisitorItems]:
        to_filter_inventory_items: Set[ZorkGrandInquisitorItems] = set()

        inventory_item_values: Set[int] = set()

        i: int
        for i in range(151, 157):
            inventory_item_values.add(self._read_game_state_value_for(i))

        cursor_item_value: int = self._read_game_state_value_for(9)
        inspector_item_value: int = self._read_game_state_value_for(2198)

        inventory_item_values.add(cursor_item_value)
        inventory_item_values.add(inspector_item_value)

        item: ZorkGrandInquisitorItems
        for item in received_inventory_items:
            if item == ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1:
                if 120 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15433) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15435) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15437) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15439) == 1:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15472) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2:
                if 121 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15433) == 2:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15435) == 2:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15437) == 2:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15439) == 2:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15472) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3:
                if 122 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15433) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15435) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15437) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15439) == 3:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15472) == 1:
                    to_filter_inventory_items.add(item)
            elif item == ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4:
                if 123 in inventory_item_values:
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15433) in (4, 5):
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15435) in (4, 5):
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15437) in (4, 5):
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15439) in (4, 5):
                    to_filter_inventory_items.add(item)
                elif self._read_game_state_value_for(15472) == 1:
                    to_filter_inventory_items.add(item)

        return received_inventory_items - to_filter_inventory_items

    def _read_game_state_value_for(self, key: int) -> Optional[int]:
        try:
            return self.game_state_manager.read_game_state_value_for(key)
        except Exception as e:
            self.log_debug(f"Exception: {e} while trying to read game state key '{key}'")
            raise e

    def _write_game_state_value_for(self, key: int, value: int) -> Optional[bool]:
        try:
            return self.game_state_manager.write_game_state_value_for(key, value)
        except Exception as e:
            self.log_debug(f"Exception: {e} while trying to write '{key} = {value}' to game state")
            raise e

    def _read_game_flags_value_for(self, key: int) -> Optional[int]:
        try:
            return self.game_state_manager.read_game_flags_value_for(key)
        except Exception as e:
            self.log_debug(f"Exception: {e} while trying to read game flags key '{key}'")
            raise e

    def _write_game_flags_value_for(self, key: int, value: int) -> Optional[bool]:
        try:
            return self.game_state_manager.write_game_flags_value_for(key, value)
        except Exception as e:
            self.log_debug(f"Exception: {e} while trying to write '{key} = {value}' to game flags")
            raise e

    def _player_has(self, item: ZorkGrandInquisitorItems) -> bool:
        return item in self.received_items

    def _player_doesnt_have(self, item: ZorkGrandInquisitorItems) -> bool:
        return item not in self.received_items

    def _player_is_at(self, game_location: str) -> bool:
        return self.game_location == game_location

    def _player_is_at_for_at_least(self, game_location: str, milliseconds: int) -> bool:
        return self.game_location == game_location and (
            int(time.time() * 1000) - self.game_location_since >= milliseconds
        )

    def _player_is_at_starting_location(self) -> bool:
        if self.option_starting_location == ZorkGrandInquisitorStartingLocations.PORT_FOOZLE:
            return self._player_is_at("ps10")
        elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.CROSSROADS:
            return self._player_is_at("uc10")
        elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.DM_LAIR:
            return self._player_is_at("dg10")
        elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR:
            return self._player_is_at("dv10")
        elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.GUE_TECH:
            return self._player_is_at("tr20")
        elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.SPELL_LAB:
            return self._player_is_at("tp20")
        elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.HADES_SHORE:
            return self._player_is_at("uh10")
        elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.SUBWAY_FLOOD_CONTROL_DAM:
            return self._player_is_at("ue10")
        elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.MONASTERY:
            return self._player_is_at("mt20")
        elif self.option_starting_location == ZorkGrandInquisitorStartingLocations.MONASTERY_EXHIBIT:
            return self._player_is_at("me10")

    def _player_is_afgncaap(self) -> bool:
        return self._read_game_state_value_for(1596) == 1

    def _player_is_totem(self) -> bool:
        return self._player_is_brog() or self._player_is_griff() or self._player_is_lucy()

    def _player_is_brog(self) -> bool:
        return self._read_game_state_value_for(1520) == 1

    def _player_is_griff(self) -> bool:
        return self._read_game_state_value_for(1296) == 1

    def _player_is_lucy(self) -> bool:
        return self._read_game_state_value_for(1524) == 1
