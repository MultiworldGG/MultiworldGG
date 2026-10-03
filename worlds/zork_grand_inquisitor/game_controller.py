import collections
import datetime
import functools
import logging
import random
import time

from typing import Dict, List, Optional, Set, Tuple, Union

from .data.entrance_randomizer_data import entrances_to_game_locations_reverse
from .data.item_data import item_data, ZorkGrandInquisitorItemData
from .data.location_data import location_data, ZorkGrandInquisitorLocationData

from .data.mapping_data import (
    death_cause_labels,
    entrance_names,
    held_item_forms,
    hotspots_for_regional_hotspot,
    labels_for_enum_items,
    voxam_cast_game_locations,
)

from .data.missable_location_data import missable_location_grant_conditions_data

from .data_funcs import game_id_to_items, items_with_tag, locations_with_tag

from .enums import (
    ZorkGrandInquisitorClientSeedInformation,
    ZorkGrandInquisitorCraftableSpellBehaviors,
    ZorkGrandInquisitorDeathsanity,
    ZorkGrandInquisitorEntranceRandomizer,
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorHotspots,
    ZorkGrandInquisitorInGameOverlayOptions,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLandmarksanity,
    ZorkGrandInquisitorLocations,
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

    logged_errors: Set[str]

    game_location: Optional[str]

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
    option_shuffle_time_tunnels: Optional[bool]
    option_entrance_randomizer: Optional[ZorkGrandInquisitorEntranceRandomizer]
    option_entrance_randomizer_include_subway_destinations: Optional[bool]
    option_trap_percentage: Optional[int]
    option_grant_missable_location_checks: Optional[bool]
    option_client_seed_information: Optional[ZorkGrandInquisitorClientSeedInformation]
    option_in_game_overlay: Optional[ZorkGrandInquisitorInGameOverlayOptions]
    option_death_link: Optional[bool]

    starter_kit: Optional[List[str]]
    initial_totemizer_destination: Optional[ZorkGrandInquisitorItems]

    time_tunnel_destinations: Dict[str, str]
    entrance_randomizer_data: Dict[str, Tuple[str, int]]
    entrance_randomizer_arrivals: Dict[Tuple[str, str], str]

    discovered_entrances: Set[str]

    received_traps: List[ZorkGrandInquisitorItems]

    should_prepare_processed_trap_counters: bool
    processed_trap_counters: Dict[ZorkGrandInquisitorItems, int]
    active_trap_timestamps: Dict[ZorkGrandInquisitorItems, Optional[int]]
    pending_infinite_corridor_depth: Optional[int]
    pending_walking_castle_return: bool

    energy_link_queue: collections.deque
    pause_energy_link_monitoring: bool

    pending_death_link: Tuple[bool, Optional[str], Optional[str]]
    outgoing_death_link: Tuple[bool, Optional[str]]
    pause_death_monitoring: bool

    death_return_history: collections.deque
    death_return_held_item: int
    death_return_arrived_at: Optional[datetime.datetime]
    death_return_text_done_at: Optional[datetime.datetime]

    save_ids: Optional[Tuple[int, int, int]]

    valid_save_message_shown: bool
    invalid_save_message_shown: bool

    toasts_pending: collections.deque
    toasts_shown: List[Tuple[str, datetime.datetime]]
    status_messages: List[Tuple[str, datetime.datetime]]
    locations_in_logic: List[str]
    announced_missable_locations: Set[ZorkGrandInquisitorLocations]
    is_overlay_enabled: bool
    is_in_logic_overlay_enabled: bool

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
            ZorkGrandInquisitorItems.DEATH,
            ZorkGrandInquisitorItems.LANDMARK,
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

        self.logged_errors = set()

        self.game_location = None

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
        self.option_shuffle_time_tunnels = None
        self.option_entrance_randomizer = None
        self.option_entrance_randomizer_include_subway_destinations = None
        self.option_trap_percentage = None
        self.option_grant_missable_location_checks = None
        self.option_client_seed_information = None
        self.option_in_game_overlay = None
        self.option_death_link = None

        self.starter_kit = None
        self.initial_totemizer_destination = None

        self.time_tunnel_destinations = dict()
        self.entrance_randomizer_data = dict()
        self.entrance_randomizer_arrivals = dict()

        self.discovered_entrances = set()

        self.received_traps = list()

        self.should_prepare_processed_trap_counters = True

        self.processed_trap_counters = {
            ZorkGrandInquisitorItems.TRAP_INFINITE_CORRIDOR: 0,
            ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS: 0,
            ZorkGrandInquisitorItems.TRAP_TELEPORT: 0,
            ZorkGrandInquisitorItems.TRAP_ZVISION: 0,
        }

        self.active_trap_timestamps = {
            ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS: None,
            ZorkGrandInquisitorItems.TRAP_ZVISION: None,
        }

        self.pending_infinite_corridor_depth = None
        self.pending_walking_castle_return = False

        self.energy_link_queue = collections.deque()
        self.pause_energy_link_monitoring = False

        self.pending_death_link = (False, None, None)
        self.outgoing_death_link = (False, None)
        self.pause_death_monitoring = False

        self.death_return_history = collections.deque(maxlen=16)
        self.death_return_held_item = 0
        self.death_return_arrived_at = None
        self.death_return_text_done_at = None

        self.save_ids = None

        self.valid_save_message_shown = False
        self.invalid_save_message_shown = False

        self.toasts_pending = collections.deque(maxlen=20)
        self.toasts_shown = list()
        self.status_messages = list()
        self.locations_in_logic = list()
        self.announced_missable_locations = set()
        self.is_overlay_enabled = False
        self.is_in_logic_overlay_enabled = False

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

    @functools.cached_property
    def missable_locations(self) -> Set[ZorkGrandInquisitorLocations]:
        return locations_with_tag(ZorkGrandInquisitorTags.MISSABLE)

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

    def clear_overlays(self) -> None:
        self.game_state_manager.clear_overlays()

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
                self.log("    Wild VOXAM: Off")

            self.log(f"    Deathsanity: {labels_for_enum_items[self.option_deathsanity]}")
            self.log(f"    Landmarksanity: {labels_for_enum_items[self.option_landmarksanity]}")

            if self.option_shuffle_time_tunnels:
                self.log("    Shuffle Time Tunnels: On")
            else:
                self.log("    Shuffle Time Tunnels: Off")

            self.log(f"    Entrance Randomizer: {labels_for_enum_items[self.option_entrance_randomizer]}")

            if self.option_entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
                if self.option_entrance_randomizer_include_subway_destinations:
                    self.log("    Entrance Randomizer - Include Subway Destinations: On")
                else:
                    self.log("    Entrance Randomizer - Include Subway Destinations: Off")

            self.log(f"    Trap Percentage: {self.option_trap_percentage}%")

            if self.option_grant_missable_location_checks:
                self.log("    Grant Missable Location Checks: On")
            else:
                self.log("    Grant Missable Location Checks: Off")

            self.log(f"    In-Game Overlay: {labels_for_enum_items[self.option_in_game_overlay]}")

            if self.option_death_link:
                self.log("    Death Link: On")
            else:
                self.log("    Death Link: Off")

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
                if not self.game_state_manager.begin_tick():
                    return

                self.game_location = self.game_state_manager.game_location

                if not self._check_for_valid_save():
                    self.game_state_manager.set_game_changes_active(False)
                    self.game_state_manager.end_tick()
                    return

                self.game_state_manager.set_game_changes_active(True)

                self._apply_initial_totemizer_destination()
                self._apply_starting_location()

                self._apply_permanent_game_state()
                self._apply_conditional_game_state()

                self._apply_permanent_game_flags()

                self._manage_game_location()

                self._manage_location_redirects()

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

                self._manage_death_return()

                self._check_for_victory()

                self._manage_overlays()

                self.game_state_manager.end_tick()
            except Exception:
                import traceback

                error: str = traceback.format_exc()

                if error not in self.logged_errors:
                    self.logged_errors.add(error)

                    with open("zork_grand_inquisitor_errors.log", "a") as f:
                        f.write(error + "\n\n")

    def reset(self) -> None:
        self.received_items = set()
        self.completed_locations = set()

        self.completed_locations_queue = collections.deque()
        self.received_items_queue = collections.deque()

        self.available_inventory_slots = set()

        self.goal_item_count = 0
        self.goal_completed = False

        self.game_location = None

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
        self.option_shuffle_time_tunnels = None
        self.option_entrance_randomizer = None
        self.option_entrance_randomizer_include_subway_destinations = None
        self.option_trap_percentage = None
        self.option_grant_missable_location_checks = None
        self.option_client_seed_information = None
        self.option_in_game_overlay = None
        self.option_death_link = None

        self.starter_kit = None
        self.initial_totemizer_destination = None

        self.time_tunnel_destinations = dict()
        self.entrance_randomizer_data = dict()
        self.entrance_randomizer_arrivals = dict()

        self.discovered_entrances = set()

        self.received_traps = list()

        self.should_prepare_processed_trap_counters = True

        self.processed_trap_counters = {
            ZorkGrandInquisitorItems.TRAP_INFINITE_CORRIDOR: 0,
            ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS: 0,
            ZorkGrandInquisitorItems.TRAP_TELEPORT: 0,
            ZorkGrandInquisitorItems.TRAP_ZVISION: 0,
        }

        self.active_trap_timestamps = {
            ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS: None,
            ZorkGrandInquisitorItems.TRAP_ZVISION: None,
        }

        self.pending_infinite_corridor_depth = None
        self.pending_walking_castle_return = False

        self.energy_link_queue = collections.deque()
        self.pause_energy_link_monitoring = False

        self.pending_death_link = (False, None, None)
        self.outgoing_death_link = (False, None)
        self.pause_death_monitoring = False

        self.death_return_history = collections.deque(maxlen=16)
        self.death_return_held_item = 0
        self.death_return_arrived_at = None
        self.death_return_text_done_at = None

        self.save_ids = None

        self.valid_save_message_shown = False
        self.invalid_save_message_shown = False

        self.toasts_pending = collections.deque(maxlen=20)
        self.toasts_shown = list()
        self.status_messages = list()
        self.locations_in_logic = list()
        self.announced_missable_locations = set()
        self.is_overlay_enabled = False
        self.is_in_logic_overlay_enabled = False

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
            return

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
            return

        if self._read_game_state_value_for(19985) == 0 or force:
            starting_locations: Dict[ZorkGrandInquisitorStartingLocations, Tuple[str, int]] = {
                ZorkGrandInquisitorStartingLocations.PORT_FOOZLE: ("ps10", 825),
                ZorkGrandInquisitorStartingLocations.CROSSROADS: ("uc10", 1200),
                ZorkGrandInquisitorStartingLocations.DM_LAIR: ("dg10", 1410),
                ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR: ("dv10", 1673),
                ZorkGrandInquisitorStartingLocations.GUE_TECH: ("tr20", 150),
                ZorkGrandInquisitorStartingLocations.SPELL_LAB: ("tp20", 1244),
                ZorkGrandInquisitorStartingLocations.HADES_SHORE: ("uh10", 950),
                ZorkGrandInquisitorStartingLocations.SUBWAY_FLOOD_CONTROL_DAM: ("ue10", 1578),
                ZorkGrandInquisitorStartingLocations.MONASTERY: ("mt20", 0),
                ZorkGrandInquisitorStartingLocations.MONASTERY_EXHIBIT: ("me10", 1023),
            }

            game_location: str
            offset: int
            game_location, offset = starting_locations[self.option_starting_location]

            if self.option_starting_location != ZorkGrandInquisitorStartingLocations.PORT_FOOZLE:
                self.game_state_manager.kill_side_effect(10262)
                self.game_state_manager.kill_side_effect(1011)

            if self.game_state_manager.set_game_location(game_location, offset):
                self.game_location = game_location
                self._write_game_state_value_for(19985, 1)

    def _apply_permanent_game_state(self) -> None:
        permanent_game_state: Dict[int, int] = {
            10297: 0,  # Lantern on Jack's Table
            5221: 1,  # Player has Lantern
            13929: 1,  # Great Underground Door Open
            5032: 0,  # Always Consider SNAVIG to not be Reassembled
            4980: 0,  # ANS Scroll in Window
            3768: 0,  # GIV Scroll in Window
            3765: 0,  # SNA Scroll in Window
            4979: 0,  # SNA Scroll in Window
            3767: 0,  # VIG Scroll in Window
            4977: 0,  # VIG Scroll in Window
            15424: 1,  # Initial State of Card Game
            5222: 1,  # User Has Spell Book
            13930: 1,  # Skip Well Cutscenes
            19057: 1,  # Skip Well Cutscenes
            13934: 1,  # Skip Well Cutscenes
            13935: 1,  # Skip Well Cutscenes
            13384: 1,  # Skip Meanwhile... Cutscene
            18275: 1,  # Skip Flashback Cutscene
            8620: 1,  # First Coin Paid to Charon
            8731: 1,  # First Coin Paid to Charon
            191: 1,  # VOXAM Learned
            19243: 0,  # Keep VOXAM Miscast Counter at 0
            15384: 0,  # Never Consider All Artifacts to be Placed
        }

        location: ZorkGrandInquisitorLocations
        pickup_game_state: Dict[int, int]
        for location, pickup_game_state in (
            (ZorkGrandInquisitorLocations.SHOVEL, {4058: 1}),
            (ZorkGrandInquisitorLocations.THROCK_SCROLL, {4059: 1}),
            (ZorkGrandInquisitorLocations.HUNGUS_LARD, {4755: 1}),
            (ZorkGrandInquisitorLocations.JAR_OF_HOTBUGS, {4746: 1}),
            (ZorkGrandInquisitorLocations.FLATHEADIA_FUDGE, {4834: 1}),
            (ZorkGrandInquisitorLocations.MUG, {4758: 1}),
            (ZorkGrandInquisitorLocations.QUELBEE_HONEYCOMB, {4321: 1}),
            (ZorkGrandInquisitorLocations.HAMMER, {12930: 1}),
            (ZorkGrandInquisitorLocations.GRIFFS_TOTEM, {12935: 1}),
            (ZorkGrandInquisitorLocations.ZIMDOR_SCROLL, {12948: 1}),
            (ZorkGrandInquisitorLocations.SUBWAY_TOKEN, {13968: 1}),
            (ZorkGrandInquisitorLocations.GOLGATEM_SCROLL, {13260: 1}),
            (ZorkGrandInquisitorLocations.LETTER_OPENER, {13414: 1}),
            (ZorkGrandInquisitorLocations.OLD_SCRATCH_CARD, {16959: 1}),
            (ZorkGrandInquisitorLocations.KENDALL_SCROLL, {11758: 1}),
            (ZorkGrandInquisitorLocations.STUDENT_ID, {11886: 1}),
            (ZorkGrandInquisitorLocations.PROZORK_TABLET, {16279: 1}),
            (ZorkGrandInquisitorLocations.ZORK_ROCKS, {12840: 0}),
            (ZorkGrandInquisitorLocations.LUCYS_TOTEM, {17147: 1}),
            (ZorkGrandInquisitorLocations.MEAD_LIGHT_AND_PLASTIC_SIX_PACK_HOLDER, {10418: 1}),
            (ZorkGrandInquisitorLocations.ROPE, {10934: 1}),
            (ZorkGrandInquisitorLocations.LANTERN, {10275: 0}),
            (ZorkGrandInquisitorLocations.SCROLL_FRAGMENT_ANS, {3766: 0}),
            (ZorkGrandInquisitorLocations.SCROLL_FRAGMENT_GIV, {4978: 0}),
            (ZorkGrandInquisitorLocations.BROGS_BICKERING_TORCH, {15065: 1}),
            (ZorkGrandInquisitorLocations.BROGS_FLICKERING_TORCH, {15088: 1}),
            (ZorkGrandInquisitorLocations.BROGS_GRUE_EGG, {2628: 4}),
            (ZorkGrandInquisitorLocations.GRIFFS_INFLATABLE_SEA_CAPTAIN, {1340: 1}),
            (ZorkGrandInquisitorLocations.GRIFFS_INFLATABLE_RAFT, {1341: 1}),
            (ZorkGrandInquisitorLocations.GRIFFS_AIR_PUMP, {1477: 1}),
            (ZorkGrandInquisitorLocations.GRIFFS_DRAGON_TOOTH, {1814: 1}),
            (ZorkGrandInquisitorLocations.LUCYS_PLAYING_CARDS, {15403: 0, 15404: 1, 15405: 4}),
        ):
            if location in self.completed_locations:
                permanent_game_state.update(pickup_game_state)

        if ZorkGrandInquisitorLocations.BROGS_PLANK in self.completed_locations or not self._player_is_brog():
            permanent_game_state[2971] = 1
        else:
            permanent_game_state[2971] = 0

        if ZorkGrandInquisitorLocations.NARWILE_SCROLL in self.completed_locations or not self._player_is_afgncaap():
            permanent_game_state[3716] = 1
        else:
            permanent_game_state[3716] = 0

            if self._player_is_at("dc1h") and self._read_game_state_value_for(3716) == 1:
                self.game_state_manager.kill_side_effect(3727)

                key: int
                for key in (3715, 3722, 3723):
                    self._write_game_state_value_for(key, 0)

        self.game_state_manager.set_state_value_overrides(permanent_game_state)

        self.game_state_manager.set_state_value_remaps(
            [
                (first_key, last_key, blue_sword, sword)
                for first_key, last_key in ((9, 9), (101, 149), (151, 170), (4512, 4512))
                for blue_sword, sword in ((100, 21), (111, 22))
            ]
        )

        state_value_read_overrides: List[Tuple[int, int, int]] = [
            (19731, 10704, 0),
            (10277, 18177, 0),
            (10277, 18179, 0),
        ]

        if ZorkGrandInquisitorLocations.BROGS_TOTEM in self.completed_locations:
            state_value_read_overrides.extend([(4853, 19077, 1), (4853, 9379, 1)])
        else:
            state_value_read_overrides.extend([(4853, 19077, 0), (4853, 9379, 0)])

        if ZorkGrandInquisitorLocations.MOSS_OF_MAREILON in self.completed_locations:
            state_value_read_overrides.append((13279, 13388, 1))

        if ZorkGrandInquisitorLocations.POUCH_OF_ZORKMIDS in self.completed_locations:
            state_value_read_overrides.append((12896, 12891, 0))

        self.game_state_manager.set_state_value_read_overrides(state_value_read_overrides)

        blocked_actions: List[Tuple[Optional[int], Optional[str]]] = [
            (9844, "inventory"),
            (11975, "inventory"),
            (17497, "dissolve"),
            (17497, "change_location"),
            (10312, "cursor"),
            (10327, "streamvideo"),
        ]

        game_location: str
        puzzle: int
        action: str
        for location, game_location, puzzle, action in (
            (ZorkGrandInquisitorLocations.SHOVEL, "dg1e", 4102, "inventory"),
            (ZorkGrandInquisitorLocations.THROCK_SCROLL, "dg1e", 4103, "dissolve"),
            (ZorkGrandInquisitorLocations.THROCK_SCROLL, "dg1e", 4103, "change_location"),
            (ZorkGrandInquisitorLocations.HUNGUS_LARD, "dv1g", 4856, "inventory"),
            (ZorkGrandInquisitorLocations.JAR_OF_HOTBUGS, "dv1g", 4849, "inventory"),
            (ZorkGrandInquisitorLocations.FLATHEADIA_FUDGE, "dv1f", 4837, "inventory"),
            (ZorkGrandInquisitorLocations.MUG, "dv1k", 4916, "inventory"),
            (ZorkGrandInquisitorLocations.QUELBEE_HONEYCOMB, "dg4f", 4335, "inventory"),
            (ZorkGrandInquisitorLocations.MOSS_OF_MAREILON, "ue2g", 13279, "inventory"),
            (ZorkGrandInquisitorLocations.SNAPDRAGON, "dg2f", 4184, "inventory"),
            (ZorkGrandInquisitorLocations.HAMMER, "uc1g", 12930, "inventory"),
            (ZorkGrandInquisitorLocations.MAP, "uc1g", 12932, "inventory"),
            (ZorkGrandInquisitorLocations.MAP, "uc1g", 13028, "inventory"),
            (ZorkGrandInquisitorLocations.SWORD, "uc1g", 12933, "inventory"),
            (ZorkGrandInquisitorLocations.SWORD, "uc1g", 13031, "inventory"),
            (ZorkGrandInquisitorLocations.GRIFFS_TOTEM, "uc1j", 12935, "change_location"),
            (ZorkGrandInquisitorLocations.ZIMDOR_SCROLL, "uc1m", 13054, "inventory"),
            (ZorkGrandInquisitorLocations.ZIMDOR_SCROLL, "uc1m", 13054, "change_location"),
            (ZorkGrandInquisitorLocations.SUBWAY_TOKEN, "uw1k", 13968, "inventory"),
            (ZorkGrandInquisitorLocations.GOLGATEM_SCROLL, "ue1h", 13260, "dissolve"),
            (ZorkGrandInquisitorLocations.GOLGATEM_SCROLL, "ue1h", 13260, "change_location"),
            (ZorkGrandInquisitorLocations.LETTER_OPENER, "ue2j", 13414, "inventory"),
            (ZorkGrandInquisitorLocations.OLD_SCRATCH_CARD, "uh1g", 16962, "inventory"),
            (ZorkGrandInquisitorLocations.KENDALL_SCROLL, "te5e", 11758, "dissolve"),
            (ZorkGrandInquisitorLocations.KENDALL_SCROLL, "te5e", 11758, "change_location"),
            (ZorkGrandInquisitorLocations.STUDENT_ID, "th3p", 11962, "inventory"),
            (ZorkGrandInquisitorLocations.PROZORK_TABLET, "th3w", 16296, "inventory"),
            (ZorkGrandInquisitorLocations.POUCH_OF_ZORKMIDS, "tr5j", 12905, "dissolve"),
            (ZorkGrandInquisitorLocations.POUCH_OF_ZORKMIDS, "tr5j", 12905, "change_location"),
            (ZorkGrandInquisitorLocations.ZORK_ROCKS, "tr5h", 12879, "inventory"),
            (ZorkGrandInquisitorLocations.NARWILE_SCROLL, "dc1h", 3730, "dissolve"),
            (ZorkGrandInquisitorLocations.NARWILE_SCROLL, "dc1h", 3730, "change_location"),
            (ZorkGrandInquisitorLocations.LUCYS_TOTEM, "me2m", 17150, "dissolve"),
            (ZorkGrandInquisitorLocations.LUCYS_TOTEM, "me2m", 17150, "change_location"),
            (ZorkGrandInquisitorLocations.LUCYS_TOTEM, "me2m", 17150, "cursor"),
            (ZorkGrandInquisitorLocations.BROGS_TOTEM, "hp6g", 9381, "dissolve"),
            (ZorkGrandInquisitorLocations.BROGS_TOTEM, "hp6g", 9381, "change_location"),
            (ZorkGrandInquisitorLocations.MEAD_LIGHT_AND_PLASTIC_SIX_PACK_HOLDER, "pe2h", 16249, "inventory"),
            (ZorkGrandInquisitorLocations.ROPE, "px1h", 10974, "inventory"),
            (ZorkGrandInquisitorLocations.LANTERN, "pe2f", 15186, "inventory"),
            (ZorkGrandInquisitorLocations.SCROLL_FRAGMENT_ANS, "dm1h", 4538, "inventory"),
            (ZorkGrandInquisitorLocations.SCROLL_FRAGMENT_ANS, "de1f", 3782, "inventory"),
            (ZorkGrandInquisitorLocations.SCROLL_FRAGMENT_ANS, "dg3e", 4227, "inventory"),
            (ZorkGrandInquisitorLocations.SCROLL_FRAGMENT_GIV, "dw1h", 5165, "inventory"),
            (ZorkGrandInquisitorLocations.BROGS_BICKERING_TORCH, "sw50", 15071, "inventory"),
            (ZorkGrandInquisitorLocations.BROGS_FLICKERING_TORCH, "sw50", 15072, "inventory"),
            (ZorkGrandInquisitorLocations.BROGS_GRUE_EGG, "sg2e", 2664, "inventory"),
            (ZorkGrandInquisitorLocations.BROGS_PLANK, "sw4f", 3072, "inventory"),
            (ZorkGrandInquisitorLocations.GRIFFS_INFLATABLE_SEA_CAPTAIN, "cd2k", 1345, "inventory"),
            (ZorkGrandInquisitorLocations.GRIFFS_INFLATABLE_SEA_CAPTAIN, "cd2k", 1347, "inventory"),
            (ZorkGrandInquisitorLocations.GRIFFS_INFLATABLE_RAFT, "cd2k", 1348, "inventory"),
            (ZorkGrandInquisitorLocations.GRIFFS_INFLATABLE_RAFT, "cd2k", 1350, "inventory"),
            (ZorkGrandInquisitorLocations.GRIFFS_AIR_PUMP, "cd4h", 1491, "inventory"),
            (ZorkGrandInquisitorLocations.GRIFFS_DRAGON_TOOTH, "cm10", 1806, "inventory"),
            (ZorkGrandInquisitorLocations.LUCYS_PLAYING_CARDS, "qb2g", 17556, "inventory"),
        ):
            if location not in self.completed_locations and game_location[:2] == self.game_location[:2]:
                blocked_actions.append((puzzle, action))

        self.game_state_manager.set_blocked_actions(blocked_actions)

        key: int
        value: int
        for key, value in permanent_game_state.items():
            self._write_game_state_value_for(key, value)

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

        if self._read_game_state_value_for(11767) == 1 and self._read_game_state_value_for(11769) == 0:
            self._write_game_state_value_for(11767, 4)
            self._write_game_state_value_for(11768, 2)

        # Zork Rocks Blast Locker ASAP
        if self._read_game_state_value_for(11767) > 0 and self._read_game_state_value_for(11769) == 1:
            self._write_game_state_value_for(11767, 5)

        if self._read_game_state_value_for(10277) == 0 and self._read_game_state_value_for(17159) == 1:
            self._write_game_state_value_for(17159, 0)

        if (
            self.game_location not in ("qs1x", "qs1e")
            and self._read_game_state_value_for(14570) == 0
            and self._read_game_state_value_for(19883) == 1
        ):
            self._write_game_state_value_for(19883, 0)

        if self.game_location != "mx2e" and not self.game_location.startswith("g"):
            if self._read_game_state_value_for(9818) in (1, 3):
                self.game_state_manager.kill_side_effect(9832)
                self._write_game_state_value_for(9832, 0)
                self._write_game_state_value_for(9834, 0)

            if self._read_game_state_value_for(9825) == 1 and self._read_game_state_value_for(9826) == 0:
                self.game_state_manager.kill_side_effect(9827)
                self._write_game_state_value_for(9827, 0)
                self._write_game_state_value_for(9825, 0)

            self._write_game_state_value_for(9818, 0)
            self._write_game_state_value_for(9844, 0)

        if self.game_location.startswith("em"):
            key: int
            for key in range(192, 203):
                if self._read_game_state_value_for(key) in (1, 2):
                    self._write_game_state_value_for(key, 3)
        elif self._read_game_state_value_for(2343) == 1 and not self.game_location.startswith(("dc", "g")):
            self._clean_up_flathead_mesa()

        if (
            self.game_location == "dg4f"
            and self._read_game_state_value_for(4299) == 0
            and self._read_game_state_value_for(4244) == 1
            and self._read_game_state_value_for(4309) == 1
            and self._read_game_state_value_for(4310) == 0
        ):
            self._write_game_state_value_for(4244, 0)
            self._write_game_state_value_for(4309, 0)

        if not self.game_location.startswith(("hp", "g")):
            if any(self._read_game_state_value_for(key) != 0 for key in (8418, 8419, 8420, 8421, 8424)):
                self.game_state_manager.kill_side_effect(8421)
                self.game_state_manager.kill_side_effect(8422)

                key: int
                for key in (8418, 8419, 8420, 8421, 8424):
                    self._write_game_state_value_for(key, 0)

            if not any(self._read_game_state_value_for(key) == 1 for key in (1596, 1520, 1296, 1524)):
                self._write_game_state_value_for(1596, 1)

    def _apply_permanent_game_flags(self) -> None:
        self._write_game_flags_value_for(13597, 2)  # Monastery Vent
        location: ZorkGrandInquisitorLocations
        keys: Tuple[int, ...]
        for location, keys in (
            (ZorkGrandInquisitorLocations.HUNGUS_LARD, (4854,)),
            (ZorkGrandInquisitorLocations.QUELBEE_HONEYCOMB, (4301,)),
            (ZorkGrandInquisitorLocations.MOSS_OF_MAREILON, (13389,)),
            (ZorkGrandInquisitorLocations.SNAPDRAGON, (4150,)),
            (ZorkGrandInquisitorLocations.MAP, (13005,)),
            (ZorkGrandInquisitorLocations.SWORD, (13006, 13007)),
            (ZorkGrandInquisitorLocations.LETTER_OPENER, (13413,)),
            (ZorkGrandInquisitorLocations.POUCH_OF_ZORKMIDS, (12895,)),
            (ZorkGrandInquisitorLocations.LUCYS_PLAYING_CARDS, (15403,)),
        ):
            if location in self.completed_locations:
                key: int
                for key in keys:
                    self._write_game_flags_value_for(key, 2)

        if ZorkGrandInquisitorLocations.BROGS_PLANK in self.completed_locations or not self._player_is_brog():
            self._write_game_flags_value_for(3074, 2)

        if self._player_is_afgncaap() and self._read_game_state_value_for(2343) == 1:
            key: int
            for key in (2332, 2336, 2338):
                self._write_game_flags_value_for(key, 2)

        if self._read_game_state_value_for(12930) == 0:
            key: int
            for key in (13005, 13006, 13007):
                self._write_game_flags_value_for(key, 2)

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
        self._write_game_flags_value_for(10838, 2)  # Keep Spellbar Enabled (pp1j)
        self._write_game_flags_value_for(8435, 0)  # Always Allow Moving to Hades Phone
        self._write_game_flags_value_for(4991, 0)  # Always Allow Moving to DM Lair Mirror

    def _manage_game_location(self) -> None:
        if self._read_game_state_value_for(19985) == 0:
            return

        if any(
            destination == "uw10" and origin not in ("uw10", "uw1f", "uw1g", "uw1k") and not is_loading
            for origin, destination, _, is_loading in self.game_state_manager.arrivals
        ):
            self.show_toast("Cast VOXAM to reach the surface")

        if self._player_is_afgncaap() and self._read_game_state_value_for(2343) == 0 and any(
            destination == "dc10" and not origin.startswith("dc") and not is_loading
            for origin, destination, _, is_loading in self.game_state_manager.arrivals
        ):
            self.show_toast("Cast VOXAM to visit Flathead Mesa")

        if self._player_is_afgncaap() and any(
            destination == "dc10" and origin.startswith("em") and not is_loading
            for origin, destination, _, is_loading in self.game_state_manager.arrivals
        ):
            self.show_toast("Cast VOXAM to return to the Dungeon Master's House")

    def _manage_location_redirects(self) -> None:
        location_redirects: List[Tuple[str, str, str, int]] = list()

        if len(self.time_tunnel_destinations):
            time_tunnels: Dict[str, Tuple[Tuple[str, int], str, Tuple[str, int], str]] = {
                "dw1j": (("sw40", 1682), "sw2e", ("dw10", 332), "sg6e"),
                "hp6f": (("cd60", 1360), "cd6j", ("hp60", 1494), "cd6k"),
                "me2f": (("qe10", 1238), "qe1f", ("me20", 1362), "qs1e"),
            }

            time_tunnel_names: List[str] = list(time_tunnels)

            origin: str
            destination: str
            is_loading: bool
            for origin, destination, _, is_loading in self.game_state_manager.arrivals:
                if destination == "dc10" and not is_loading:
                    tunnel: str
                    for tunnel in time_tunnel_names:
                        if origin == time_tunnels[tunnel][3]:
                            self._write_game_state_value_for(19987, time_tunnel_names.index(tunnel) + 1)

            completed_world: int = self._read_game_state_value_for(19987)

            if completed_world:
                used_tunnel: str = next(
                    tunnel
                    for tunnel, world in self.time_tunnel_destinations.items()
                    if world == time_tunnel_names[completed_world - 1]
                )

                vanilla_return: str
                for vanilla_return in ("dw10", "hp60", "me20", "gjaq"):
                    location_redirects.append(("dc1m", vanilla_return, *time_tunnels[used_tunnel][2]))

            tunnel: str
            world: str
            for tunnel, world in self.time_tunnel_destinations.items():
                location_redirects.append((tunnel, time_tunnels[tunnel][0][0], *time_tunnels[world][0]))
                location_redirects.append((time_tunnels[world][1], time_tunnels[world][2][0], *time_tunnels[tunnel][2]))

        if self._player_is_brog():
            location_redirects.append(("dc1m", "gjaq", "dw10", 332))
        elif self._player_is_griff():
            location_redirects.append(("dc1m", "gjaq", "hp60", 1494))
        elif self._player_is_lucy():
            location_redirects.append(("dc1m", "gjaq", "me20", 1362))

        if self.option_entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
            location_redirects.extend(self._manage_entrance_randomizer())

        well_bottom: Tuple[str, int] = next(
            (
                (new_destination, new_offset)
                for origin, destination, new_destination, new_offset in location_redirects
                if (origin, destination) == ("pc1e", "uw10")
            ),
            ("uw10", 738),
        )

        location_redirects.append(("pc1e", "uw1x", *well_bottom))

        self.game_state_manager.set_location_redirects(location_redirects)

    def _manage_entrance_randomizer(self) -> List[Tuple[str, str, str, int]]:
        if self._read_game_state_value_for(19985) == 0:
            return list()

        origins_for_game_location_pair: Dict[Tuple[str, str], Tuple[str, ...]] = {
            ("dg40", "dv10"): ("dg40", "dg4e"),
            ("dv10", "dc10"): ("dv1e",),
            ("hp50", "hp60"): ("hp50", "hp5f"),
            ("mt2e", "me20"): ("me5e",),
            ("pc1e", "uw10"): ("pc1e", "uw1x"),
            ("pp10", "pe10"): ("pp10", "pp1f", "pp1h"),
            ("ps10", "px10"): ("ps2e",),
            ("px10", "ps10"): ("px1e",),
            ("th30", "tp10"): ("th30", "th3r"),
            ("tp10", "tp50"): ("tp10", "tp1e"),
            ("uc10", "uw10"): ("uc1h",),
            ("uc30", "dg10"): ("uc30", "uc3e"),
            ("uc40", "te10"): ("uc40", "uc4e"),
            ("uc60", "us10"): ("uc6e",),
            ("um10", "mt10"): ("um1e",),
            ("uw10", "pc10"): ("uw10", "uw1f", "uw1g", "uw1k"),
        }

        location_redirects: List[Tuple[str, str, str, int]] = list()
        self.entrance_randomizer_arrivals = dict()

        location_pairing_key: str
        teleport: Tuple[str, int]
        for location_pairing_key, teleport in sorted(self.entrance_randomizer_data.items()):
            origin, destination = location_pairing_key.split("-")
            next_game_location: str = teleport[0]
            offset: int = teleport[1]
            entrance_name: str = entrance_names[entrances_to_game_locations_reverse[(origin, destination)]]

            redirected_origin: str
            for redirected_origin in origins_for_game_location_pair.get((origin, destination), (origin,)):
                location_redirects.append((redirected_origin, destination, next_game_location, offset))
                self.entrance_randomizer_arrivals[(redirected_origin, next_game_location)] = entrance_name

        origin: str
        destination: str
        is_loading: bool
        for origin, destination, _, is_loading in self.game_state_manager.arrivals:
            if not is_loading and (origin, destination) in self.entrance_randomizer_arrivals:
                self.discovered_entrances.add(self.entrance_randomizer_arrivals[(origin, destination)])

        return location_redirects

    def _check_for_completed_locations(self) -> None:
        seen_state_changes: Set[Tuple[int, int]] = set(self.game_state_manager.previous_state_changes + self.game_state_manager.state_changes)

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
                        if not self._player_is_at(value):
                            is_location_completed = False
                            break
                    elif isinstance(value, tuple):
                        if not any(self._player_is_at(key) for key in value):
                            is_location_completed = False
                            break
                elif trigger == "puzzle":
                    if isinstance(value, int):
                        if (value, 1) not in seen_state_changes:
                            is_location_completed = False
                            break
                    elif isinstance(value, tuple):
                        if not any((key, 1) in seen_state_changes for key in value):
                            is_location_completed = False
                            break
                elif trigger == "set":
                    if value not in seen_state_changes:
                        is_location_completed = False
                        break
                elif isinstance(trigger, int):
                    is_single_trigger: bool = len(data.game_state_trigger) == 1

                    if isinstance(value, int):
                        if self._read_game_state_value_for(trigger) != value:
                            if not is_single_trigger or (trigger, value) not in seen_state_changes:
                                is_location_completed = False
                                break
                    elif isinstance(value, tuple):
                        if self._read_game_state_value_for(trigger) not in value:
                            if not is_single_trigger or not any((trigger, option) in seen_state_changes for option in value):
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

            if missable_location.value not in self.locations_in_logic:
                continue

            location_condition: Tuple[Union[ZorkGrandInquisitorLocations, Tuple[int, int]], ...] = (
                missable_location_grant_conditions_data[missable_location]
            )

            if any(
                condition in self.completed_locations
                if isinstance(condition, ZorkGrandInquisitorLocations)
                else self._read_game_state_value_for(condition[0]) == condition[1]
                for condition in location_condition
            ):
                if missable_location not in self.completed_locations_queue:
                    self.completed_locations_queue.append(missable_location)

                if missable_location not in self.announced_missable_locations:
                    self.announced_missable_locations.add(missable_location)
                    self.show_toast(f"Granting Missable: {missable_location.value}")

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

        if self.should_prepare_processed_trap_counters:
            self.should_prepare_processed_trap_counters = False

            trap: ZorkGrandInquisitorItems
            for trap in self.processed_trap_counters:
                self.processed_trap_counters[trap] = self.received_traps.count(trap)

    def _manage_hotspots(self) -> None:
        hotspot_item: ZorkGrandInquisitorItems
        for hotspot_item in self.all_hotspot_items:
            data: ZorkGrandInquisitorItemData = item_data[hotspot_item]

            if hotspot_item not in self.received_items:
                key: int
                for key in data.game_keys:
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
                    if self.game_location == "uw10":
                        self._write_game_flags_value_for(13928, 0)
                elif hotspot_item == ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS:
                    if self.game_location == "tr5g":
                        key: int
                        for key in data.game_keys:
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
                        for key in data.game_keys:
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
                            for key in data.game_keys:
                                self._write_game_flags_value_for(key, 0)
                        else:
                            key: int
                            for key in data.game_keys:
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
                        if self._read_game_state_value_for(11777) == 1 or self._read_game_state_value_for(12393) == 1:
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
        items_returned_by_puzzle: Dict[int, ZorkGrandInquisitorItems] = {
            1351: ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN,
            1352: ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN,
            1353: ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT,
            1354: ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT,
            2651: ZorkGrandInquisitorItems.BROGS_GRUE_EGG,
            4104: ZorkGrandInquisitorItems.SHOVEL,
            4529: ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV,
            4532: ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV,
            4533: ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS,
            4534: ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS,
            4857: ZorkGrandInquisitorItems.HUNGUS_LARD,
            4869: ZorkGrandInquisitorItems.HUNGUS_LARD,
            5158: ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV,
            5161: ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV,
            5162: ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS,
            5163: ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS,
            6144: ZorkGrandInquisitorItems.ZIMDOR_SCROLL,
            13600: ZorkGrandInquisitorItems.SWORD,
            16964: ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
            17197: ZorkGrandInquisitorItems.STUDENT_ID,
            17624: ZorkGrandInquisitorItems.MEAD_LIGHT,
            17625: ZorkGrandInquisitorItems.ZIMDOR_SCROLL,
            18025: ZorkGrandInquisitorItems.CIGAR,
        }

        fired_puzzle_keys: Set[int] = {key for key, value in self.game_state_manager.state_changes if value == 1}

        puzzle_key: int
        item: ZorkGrandInquisitorItems
        for puzzle_key, item in items_returned_by_puzzle.items():
            if puzzle_key in fired_puzzle_keys:
                self._write_game_state_value_for(item_data[item].granted_key, 0)

        managed_items: Set[ZorkGrandInquisitorItems]

        if self._player_is_afgncaap():
            managed_items = self.possible_inventory_items - self.totem_items
        elif self._player_is_brog():
            managed_items = self.brog_items
        elif self._player_is_griff():
            managed_items = self.griff_items
        elif self._player_is_lucy():
            managed_items = self.lucy_items
        else:
            return

        seen_game_ids: Set[int] = {
            self._read_game_state_value_for(key) for key in range(101, 101 + self._read_game_state_value_for(100))
        }

        for key in range(151, 171):
            game_id: int = self._read_game_state_value_for(key)

            if game_id not in self.game_id_to_items:
                continue

            if game_id in seen_game_ids:
                self._write_game_state_value_for(key, 0)
            else:
                seen_game_ids.add(game_id)

        self.available_inventory_slots = self._determine_available_inventory_slots(is_totem=self._player_is_totem())

        game_state_inventory_items: Set[ZorkGrandInquisitorItems] = self._determine_game_state_inventory()

        is_totem_item_accounted_for: Dict[ZorkGrandInquisitorItems, bool] = dict()

        if self._player_is_totem():
            held_game_ids: Set[int] = {
                self._read_game_state_value_for(key) for key in (9, 2194, 2196, 2198, *range(101, 150), *range(151, 171))
            }

            lucy_card_slots: List[int] = [self._read_game_state_value_for(key) for key in (15433, 15435, 15437, 15439)]
            are_lucy_cards_played: bool = self._read_game_state_value_for(15472) == 1

            is_totem_item_accounted_for = {
                ZorkGrandInquisitorItems.BROGS_BICKERING_TORCH: 103 in held_game_ids,
                ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH: 104 in held_game_ids,
                ZorkGrandInquisitorItems.BROGS_GRUE_EGG: (
                    71 in held_game_ids
                    or self._read_game_state_value_for(2577) == 1
                    or self._read_game_state_value_for(2641) == 1
                ),
                ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT: (
                    self._read_game_state_value_for(1301) == 1
                    or self._read_game_state_value_for(1304) == 1
                    or self._read_game_state_value_for(16562) == 1
                ),
                ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN: (
                    self._read_game_state_value_for(1374) == 1
                    or self._read_game_state_value_for(1381) == 1
                    or self._read_game_state_value_for(16562) == 1
                ),
            }

            lucy_cards_being_inserted: Set[int] = {
                self._read_game_state_value_for(card_key)
                for slot_key, card_key in ((15433, 18846), (15435, 18847), (15437, 18848), (15439, 18849))
                if self._read_game_state_value_for(slot_key) == 0
            }

            card: ZorkGrandInquisitorItems
            card_game_ids: Tuple[int, int]
            slot_values: Tuple[int, ...]
            for card, card_game_ids, slot_values in (
                (ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1, (116, 120), (1,)),
                (ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2, (117, 121), (2,)),
                (ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3, (118, 122), (3,)),
                (ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4, (119, 123), (4, 5)),
            ):
                is_totem_item_accounted_for[card] = (
                    card_game_ids[1] in held_game_ids
                    or any(slot_value in lucy_card_slots for slot_value in slot_values)
                    or are_lucy_cards_played
                    or (
                        not set(card_game_ids) & held_game_ids
                        and bool(set(card_game_ids) & lucy_cards_being_inserted)
                    )
                )

            for item in managed_items - game_state_inventory_items:
                if not is_totem_item_accounted_for.get(item, False):
                    self._write_game_state_value_for(item_data[item].granted_key, 0)

            for item in managed_items & game_state_inventory_items:
                if is_totem_item_accounted_for.get(item, False):
                    self._remove_from_inventory(item)
                    game_state_inventory_items.discard(item)

        for item in managed_items:
            granted_key: Optional[int] = item_data[item].granted_key

            if granted_key is None:
                continue

            if self._read_game_state_value_for(granted_key) == 1:
                continue

            if item in self.received_items:
                if (
                    item in game_state_inventory_items
                    or is_totem_item_accounted_for.get(item, False)
                    or self._add_to_inventory(item)
                ):
                    self._write_game_state_value_for(granted_key, 1)
            elif item in game_state_inventory_items:
                self._remove_from_inventory(item)

        if self._read_game_state_value_for(4402) == 0:
            fragment_values: Dict[int, int] = {key: self._read_game_state_value_for(key) for key in (4512, *range(151, 171))}
            held_fragments: Set[int] = {*fragment_values.values(), self._read_game_state_value_for(9)}

            if {101, 48} <= held_fragments or {41, 102} <= held_fragments:
                fragment: int = 48 if 101 in held_fragments else 102

                if self._read_game_state_value_for(9) == fragment:
                    fragment = 101 if fragment == 48 else 41

                key: int
                value: int
                for key, value in fragment_values.items():
                    if value == fragment:
                        self._write_game_state_value_for(key, {41: 101, 48: 102, 101: 41, 102: 48}[fragment])
                        break

    def _apply_conditional_teleports(self) -> None:
        # Skip Y'Gael Cutscene
        if self._player_is_at("ej10"):
            self.game_state_manager.set_game_location("uc10", 1200, is_redirectable=True)

        if (17497, 1) in self.game_state_manager.state_changes:
            self.game_state_manager.persist_game_flags_value_for(13223, 0)

        if (10327, 1) in self.game_state_manager.state_changes:
            self._write_game_state_value_for(18256, 1)

        pickup_game_location: str
        puzzle: int
        for pickup_game_location, puzzle in (
            ("dg1e", 4103),
            ("uc1j", 12935),
            ("uc1m", 13054),
            ("tr5j", 12905),
            ("me2m", 17150),
            ("hp6g", 9381),
        ):
            if self._player_is_at(pickup_game_location) and (puzzle, 1) in self.game_state_manager.state_changes:
                self._write_game_state_value_for(5824, 0)

                if pickup_game_location == "dg1e":
                    key: int
                    for key in (4087, 4088, 4089, 4090, 4091, 4080):
                        self._write_game_state_value_for(key, 0)
                elif pickup_game_location == "uc1j":
                    self.game_state_manager.persist_game_flags_value_for(13048, 0)
                elif pickup_game_location == "uc1m":
                    self._write_game_state_value_for(13050, 0)
                elif pickup_game_location == "me2m":
                    self.game_state_manager.persist_game_flags_value_for(17145, 0)

        # Monastery Subway Station -> Monastery
        if self._player_is_at("um1e") and self._read_game_state_value_for(9637) == 1:
            self.game_state_manager.set_game_location("mt10", 1531, is_redirectable=True)

        game_location: str
        revealing_puzzle: int
        screenset_puzzles: Tuple[int, ...]
        for game_location, revealing_puzzle, screenset_puzzles in (
            ("tr5j", 12904, (12891,)),
            ("ue2g", 14253, (13388,)),
            ("uc1e", 12980, (12957, 12959)),
            ("uc1e", 12964, (12957, 12959)),
            ("te5e", 11762, (11749,)),
            ("dg4f", 4331, (4304,)),
            ("ue2j", 13417, (13410,)),
            ("dc1h", 3716, (3717, 3726)),
        ):
            if self._player_is_at(game_location) and (revealing_puzzle, 1) in self.game_state_manager.state_changes:
                screenset_puzzle: int
                for screenset_puzzle in screenset_puzzles:
                    self._write_game_state_value_for(screenset_puzzle, 0)

        if self.pending_infinite_corridor_depth is not None and self._player_is_at("th20"):
            self._write_game_state_value_for(11005, self.pending_infinite_corridor_depth)
            self.pending_infinite_corridor_depth = None

        if self.pending_walking_castle_return and self._player_is_at("dc1k"):
            self.pending_walking_castle_return = False
            self._clean_up_flathead_mesa()
            self.game_state_manager.set_game_location("dc10", 1192)

        # VOXAM Cast
        zork_rocks_inert: bool = self._read_game_state_value_for(11767) == 0

        is_voxam_on_cursor: bool = self._read_game_state_value_for(9) == 224

        if 224 in [self._read_game_state_value_for(key) for key in range(101, 150)]:
            self.game_state_manager.drop_inventory_item(224)
        elif is_voxam_on_cursor:
            self._write_game_state_value_for(9, 0)

        if is_voxam_on_cursor and zork_rocks_inert:
            self._cast_voxam()

    def _cast_voxam(self, force_wild: bool = False) -> bool:
        if self.option_wild_voxam or force_wild:
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

                return self.game_state_manager.set_game_location(
                    game_location[0], game_location_offset
                )

        if self.game_location in ("uw10", "uw1f", "uw1g", "uw1k"):
            return self.game_state_manager.set_game_location("pc10", 335, is_redirectable=True)

        if self.game_location.startswith("em") or (
            self.game_location.startswith("dc") and self._read_game_state_value_for(2343) == 1
        ):
            self._clean_up_flathead_mesa()
            self.pending_walking_castle_return = True

            return self.game_state_manager.set_game_location("dc1k", 0)

        if self.game_location.startswith("dc"):
            return self.game_state_manager.set_game_location("em10", 237)

        self._apply_starting_location(force=True)

        return True

    def _clean_up_flathead_mesa(self) -> None:
        self.game_state_manager.kill_side_effect(16184)
        self.game_state_manager.kill_side_effect(16179)

        key: int
        for key in (2343, 5595, 5596, 5764, 5781, 5789, 5799, 18107, 18133):
            self._write_game_state_value_for(key, 0)

        self.game_state_manager.persist_game_flags_value_for(18116, 0)

        for key in range(192, 203):
            if self._read_game_state_value_for(key) == 3:
                self._write_game_state_value_for(key, 1)

    def _manage_traps(self) -> None:
        if not self._player_is_afgncaap() or self._read_game_state_value_for(19985) == 0 or self._player_is_at("gjde"):
            return

        zork_rocks_inert: bool = self._read_game_state_value_for(11767) == 0

        if not zork_rocks_inert:
            return

        now_timestamp: int = int(time.time())

        trap: ZorkGrandInquisitorItems
        expiry_timestamp: Optional[int]
        for trap, expiry_timestamp in self.active_trap_timestamps.items():
            if expiry_timestamp is None:
                continue

            if now_timestamp >= expiry_timestamp:
                if trap == ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS:
                    self._deactivate_trap_reverse_controls()
                elif trap == ZorkGrandInquisitorItems.TRAP_ZVISION:
                    self._deactivate_trap_zvision()

                self.active_trap_timestamps[trap] = None
            elif trap == ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS:
                self._activate_trap_reverse_controls()
            elif trap == ZorkGrandInquisitorItems.TRAP_ZVISION:
                self._activate_trap_zvision()

        trap_count: int
        for trap in self.processed_trap_counters:
            trap_count = self.received_traps.count(trap)

            if trap_count <= self.processed_trap_counters[trap]:
                continue

            if trap == ZorkGrandInquisitorItems.TRAP_INFINITE_CORRIDOR:
                if self._activate_trap_infinite_corridor():
                    self.processed_trap_counters[trap] = trap_count

                    self.log("Infinite Corridor Trap!")
                    self.show_status_message("Infinite Corridor Trap!")

                    return
            elif trap == ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS:
                if self.active_trap_timestamps[trap] is None:
                    self._activate_trap_reverse_controls()

                    self.active_trap_timestamps[trap] = now_timestamp + 30
                    self.processed_trap_counters[trap] += 1

                    self.log("Reverse Controls Trap for 30 seconds!")
            elif trap == ZorkGrandInquisitorItems.TRAP_TELEPORT:
                if self._activate_trap_teleport():
                    self.processed_trap_counters[trap] = trap_count

                    self.log("Teleport Trap!")
                    self.show_status_message("Teleport Trap!")

                    return
            elif trap == ZorkGrandInquisitorItems.TRAP_ZVISION:
                if self.active_trap_timestamps[trap] is None:
                    self._activate_trap_zvision()

                    self.active_trap_timestamps[trap] = now_timestamp + 30
                    self.processed_trap_counters[trap] += 1

                    self.log("ZVision Trap for 30 seconds!")

    def _activate_trap_infinite_corridor(self) -> bool:
        depth = random.randint(10, 20)

        if not self.game_state_manager.set_game_location("th20", random.randint(0, 1800)):
            return False

        self._write_game_state_value_for(11005, depth)
        self.pending_infinite_corridor_depth = depth

        return True

    def _activate_trap_reverse_controls(self) -> None:
        self.game_state_manager.set_panorama_reversed(True)

    def _deactivate_trap_reverse_controls(self) -> None:
        self.game_state_manager.set_panorama_reversed(False)

    def _activate_trap_teleport(self) -> bool:
        return self._cast_voxam(force_wild=True)

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
        held_game_id: int = self._read_game_state_value_for(9)

        is_death_link_deferred: bool = (
            self._player_is_at("gjde")
            or self.game_location in ("qs1e", "qs1x", "pe5x", "pp1h", "qb2x", "em1f", "em3n")
            or any(self._read_game_state_value_for(key) != 0 for key in (4512, 2194, 2196, 2198))
            or (self._player_is_at("mx2e") and self._read_game_state_value_for(9818) != 0)
            or (
                held_game_id != 0
                and held_game_id not in self.game_id_to_items
                and held_game_id not in held_item_forms
            )
        )

        if self.pending_death_link[0] and not is_death_link_deferred:
            self._write_game_state_value_for(2201, 35)

            if self.game_state_manager.set_game_location("gjde", 0):
                if self.pending_death_link[2]:
                    self.log(f"Death Link: {self.pending_death_link[2]}")
                    self.show_status_message(f"Death Link: {self.pending_death_link[2]}")
                else:
                    self.log(f"Death Link: Triggered by {self.pending_death_link[1]}")
                    self.show_status_message(f"Death Link: Triggered by {self.pending_death_link[1]}")

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

    def _manage_death_return(self) -> None:
        places_in_world_g: Tuple[str, ...] = ("gjnj", "gm10", "gm1e")

        origin: str
        destination: str
        offset: int
        is_loading: bool
        for origin, destination, offset, is_loading in self.game_state_manager.arrivals:
            if is_loading:
                self.death_return_history.clear()

            self.death_return_history.append(
                (destination, offset, self.game_state_manager.state_value_journal_position)
            )

        if self.game_location and (not self.game_location.startswith("g") or self.game_location in places_in_world_g):
            if not len(self.death_return_history) or self.death_return_history[-1][0] != self.game_location:
                self.death_return_history.append(
                    (
                        self.game_location,
                        self.game_state_manager.game_location_offset or 0,
                        self.game_state_manager.state_value_journal_position,
                    )
                )

        self.game_state_manager.trim_state_value_journal(
            min(
                [position for _, _, position in self.death_return_history],
                default=self.game_state_manager.state_value_journal_position,
            )
        )

        if not self._player_is_at("gjde"):
            self.death_return_held_item = self._read_game_state_value_for(9)
            self.death_return_arrived_at = None
            self.death_return_text_done_at = None
            return

        now: datetime.datetime = datetime.datetime.now()

        if self.death_return_arrived_at is None:
            self.death_return_arrived_at = now

        if self.death_return_text_done_at is None and self._read_game_state_value_for(16224) == 2:
            self.death_return_text_done_at = now

        is_text_read: bool = self.death_return_text_done_at is not None and now - self.death_return_text_done_at >= datetime.timedelta(seconds=2)
        is_waiting_too_long: bool = now - self.death_return_arrived_at >= datetime.timedelta(seconds=30)

        if not is_text_read and not is_waiting_too_long:
            return

        cause_of_death: int = self._read_game_state_value_for(2201)

        menu_locations: List[str] = list()

        game_location: str
        for game_location, _, _ in reversed(self.death_return_history):
            if not game_location.startswith("g") or game_location in places_in_world_g:
                break

            menu_locations.append(game_location)

        is_death_in_inspector: bool = "gjiv" in menu_locations

        game_locations: List[Tuple[str, int, int]] = list()

        history_entry: Tuple[str, int, int]
        for history_entry in self.death_return_history:
            if history_entry[0].startswith("g") and history_entry[0] not in places_in_world_g:
                continue

            if len(game_locations) and game_locations[-1][0] == history_entry[0]:
                continue

            game_locations.append(history_entry)

        if cause_of_death != 35 and not is_death_in_inspector and len(game_locations) >= 2:
            game_locations.pop()

        while cause_of_death != 35 and len(game_locations) >= 2:
            expired_timer_start: Optional[int] = self.game_state_manager.find_expired_timer_start(
                game_locations[-1][2], {1927}
            )

            if expired_timer_start is None or game_locations[0][2] > expired_timer_start:
                break

            while game_locations[-1][2] > expired_timer_start:
                game_locations.pop()

        if cause_of_death != 35 and len(game_locations):
            inventory_before_rewind: Set[ZorkGrandInquisitorItems] = self._determine_game_state_inventory()

            previous_values: Optional[Dict[int, int]] = self.game_state_manager.rewind_state_value_journal(
                game_locations[-1][2]
            )

            if previous_values:
                rewind_excluded_keys: Set[int] = {
                    data.granted_key for data in item_data.values() if data.granted_key is not None
                } | {2201, 4217, 4219, 4220, 4222, 19985, 19986, 19996, 19997, 19998, 19999}

                rewound_values: Dict[int, int] = {
                    key: value for key, value in previous_values.items() if key not in rewind_excluded_keys
                }

                for key, value in rewound_values.items():
                    self._write_game_state_value_for(key, value)

                self.game_state_manager.suppress_state_changes(rewound_values)

                item: ZorkGrandInquisitorItems
                for item in inventory_before_rewind - self._determine_game_state_inventory():
                    if item_data[item].granted_key is not None:
                        self._write_game_state_value_for(item_data[item].granted_key, 0)

        state_repairs: Dict[int, Dict[int, int]] = {
            1: {
                19734: 0,
                19731: 0,
                10277: 0,
                10333: 0,
                17160: 0,
                17161: 0,
                17163: 0,
                10393: 0,
                10269: 0,
                10378: 0,
                17681: 0,
                10395: 0,
                10398: 0,
                10399: 0,
                10400: 0,
            },
            4: {12459: 0},
            11: {1926: 0, 1927: 0, 2008: 0},
            19: {11767: 0, 11768: 0, 13996: 0, 16263: 0, 16509: 0, 16510: 0},
            22: {10412: 0, 10565: 0},
            23: {
                **{key: 0 for key in range(7702, 7784)},
                7765: 2,
                7865: 63,
                17287: 0,
                17288: 0,
                17453: 0,
                **{key: 0 for key in range(17843, 17928)},
                **{key: 1 for key in range(19098, 19179)},
                4512: 0,
                item_data[ZorkGrandInquisitorItems.OLD_SCRATCH_CARD].granted_key: 0,
                6109: 0,
                6150: 0,
                6389: 0,
                17942: 0,
            },
            37: {
                **{key: 0 for key in range(2489, 2494)},
                **{key: 0 for key in range(14382, 14998) if key != 14570},
                **{key: 0 for key in range(15000, 15037)},
                16262: 0,
                **{key: 0 for key in range(16566, 16570)},
                17102: 0,
                18017: 0,
                **{key: 0 for key in range(18875, 18955)},
                **{key: 0 for key in range(19265, 19274)},
                19883: 0,
            },
        }

        control_repairs: Dict[int, Dict[int, int]] = {
            1: {18181: 0, 10711: 0},
            3: {11271: 0, 11273: 0, 11493: 0, 11495: 0, 11703: 0, 11705: 0, 11728: 0, 11730: 0},
            12: {9830: 0, 9819: 0},
            17: {9830: 0, 9819: 0},
            23: {**{key: 2 for key in range(7784, 7865)}, 7837: 0},
        }

        key: int
        value: int
        for key, value in state_repairs.get(cause_of_death, dict()).items():
            self._write_game_state_value_for(key, value)

        if cause_of_death == 19:
            if self._read_game_state_value_for(12487) == 1:
                self._write_game_state_value_for(12486, 1)
                self._write_game_state_value_for(12487, 0)

            for key in [9, *range(101, 150), *range(151, 171), 4512]:
                if self._read_game_state_value_for(key) == 52:
                    self._write_game_state_value_for(key, 37)

            if self.death_return_held_item == 52:
                self.death_return_held_item = 37

        held_item: Optional[ZorkGrandInquisitorItems] = held_item_forms.get(
            self.death_return_held_item, self.game_id_to_items.get(self.death_return_held_item)
        )

        if held_item is not None and item_data[held_item].granted_key is not None:
            self._write_game_state_value_for(item_data[held_item].granted_key, 0)

        self.death_return_held_item = 0

        for key, value in control_repairs.get(cause_of_death, dict()).items():
            self.game_state_manager.persist_game_flags_value_for(key, value)

        if len(game_locations):
            is_returned: bool = self.game_state_manager.set_game_location(*game_locations[-1][:2])
        else:
            self._apply_starting_location(force=True)
            is_returned = True

        if is_returned:
            self.death_return_arrived_at = None
            self.death_return_text_done_at = None

    def _check_for_victory(self) -> None:
        if self.option_goal == ZorkGrandInquisitorGoals.THREE_ARTIFACTS:
            coconut_is_placed = self._read_game_state_value_for(2200) == 1
            cube_is_placed = self._read_game_state_value_for(2322) == 1
            skull_is_placed = self._read_game_state_value_for(2321) == 1

            self.goal_completed = coconut_is_placed and cube_is_placed and skull_is_placed
        elif self.option_goal == ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT:
            if self.goal_item_count >= self.option_artifacts_of_magic_required:
                if self._player_is_at("dc10") and self._player_is_afgncaap():
                    self.goal_completed = True
        elif self.option_goal == ZorkGrandInquisitorGoals.SPELL_HEIST:
            if not len(self.all_spell_items - self.received_items):
                if self._player_is_at("ps1e"):
                    self.goal_completed = True
        elif self.option_goal == ZorkGrandInquisitorGoals.ZORK_TOUR:
            if self.goal_item_count >= self.option_landmarks_required:
                if self._player_is_at("ps1e"):
                    self.goal_completed = True
        elif self.option_goal == ZorkGrandInquisitorGoals.GRIM_JOURNEY:
            if self.goal_item_count >= self.option_deaths_required:
                if self._player_is_at("hp60"):
                    self.goal_completed = True

    def _manage_overlays(self) -> None:
        if not self.is_overlay_enabled:
            self.game_state_manager.clear_overlays()
            return

        goal_progress: str = ""

        if self.option_goal == ZorkGrandInquisitorGoals.THREE_ARTIFACTS:
            artifacts_placed: int = sum(self._read_game_state_value_for(key) == 1 for key in (2200, 2322, 2321))

            goal_progress = f"Artifacts Placed: {artifacts_placed} / 3"
        elif self.option_goal == ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT:
            goal_progress = f"Artifacts of Magic: {self.goal_item_count} / {self.option_artifacts_of_magic_required}"
        elif self.option_goal == ZorkGrandInquisitorGoals.SPELL_HEIST:
            goal_progress = f"Spells Learnt: {len(self.all_spell_items & self.received_items)} / {len(self.all_spell_items)}"
        elif self.option_goal == ZorkGrandInquisitorGoals.ZORK_TOUR:
            goal_progress = f"Landmarks Visited: {self.goal_item_count} / {self.option_landmarks_required}"
        elif self.option_goal == ZorkGrandInquisitorGoals.GRIM_JOURNEY:
            goal_progress = f"Deaths Experienced: {self.goal_item_count} / {self.option_deaths_required}"

        self.game_state_manager.show_goal_progress(goal_progress)

        now: datetime.datetime = datetime.datetime.now()

        self.toasts_shown = [
            (message, shown_at) for message, shown_at in self.toasts_shown if now - shown_at < datetime.timedelta(seconds=4)
        ]

        while len(self.toasts_pending) and len(self.toasts_shown) < self.game_state_manager.toast_capacity:
            self.toasts_shown.append((self.toasts_pending.popleft(), now))

        self.game_state_manager.show_toasts([message for message, _ in self.toasts_shown])

        self.status_messages = [
            (message, shown_at) for message, shown_at in self.status_messages if now - shown_at < datetime.timedelta(seconds=4)
        ]

        status_lines: List[str] = [message for message, _ in self.status_messages]

        now_timestamp: int = int(time.time())

        trap: ZorkGrandInquisitorItems
        expiry_timestamp: Optional[int]
        for trap, expiry_timestamp in self.active_trap_timestamps.items():
            if expiry_timestamp is not None:
                status_lines.append(f"{trap.value}: {max(expiry_timestamp - now_timestamp, 0)} s")

        self.game_state_manager.show_status(status_lines)

        if self.is_in_logic_overlay_enabled:
            self.game_state_manager.show_in_logic([location.replace("Landmark Visited: ", "Landmark: ", 1) for location in sorted(self.locations_in_logic)], self.game_location in ("gjiv", "gjsr", "qb2g", "tr5g"))
        else:
            self.game_state_manager.show_in_logic(list(), False)

    def show_toast(self, message: str) -> None:
        self.toasts_pending.append(message)

    def show_status_message(self, message: str) -> None:
        self.status_messages.append((message, datetime.datetime.now()))

    def _determine_game_state_inventory(self) -> Set[ZorkGrandInquisitorItems]:
        game_state_inventory: Set[ZorkGrandInquisitorItems] = set()

        # Item on Cursor
        item_on_cursor: int = self._read_game_state_value_for(9)

        if item_on_cursor != 0:
            if item_on_cursor in self.game_id_to_items:
                game_state_inventory.add(self.game_id_to_items[item_on_cursor])

        cursor_item: int
        for cursor_item in [self._read_game_state_value_for(key) for key in range(101, 150)]:
            if cursor_item in self.game_id_to_items:
                game_state_inventory.add(self.game_id_to_items[cursor_item])

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

        held_game_ids: List[int] = [self._read_game_state_value_for(key) for key in (9, 4512, *range(151, 171))]

        if 41 in held_game_ids:
            game_state_inventory.add(ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS)

        if 48 in held_game_ids:
            game_state_inventory.add(ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV)

        # Spells
        i: int
        for i in range(192, 203):
            if self._read_game_state_value_for(i) != 0:
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

    def _add_to_inventory(self, item: ZorkGrandInquisitorItems) -> bool:
        data: ZorkGrandInquisitorItemData = item_data[item]

        if data.game_keys is None:
            return False

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            if not len(self.available_inventory_slots):
                return False

            inventory_slot: int = self.available_inventory_slots.pop()
            self._write_game_state_value_for(inventory_slot, data.game_keys[0])
        elif ZorkGrandInquisitorTags.SPELL in data.tags:
            self._write_game_state_value_for(data.game_keys[0], 1)
        elif ZorkGrandInquisitorTags.TOTEM in data.tags:
            self._write_game_state_value_for(data.game_keys[0], 1)

        return True

    def _remove_from_inventory(self, item: ZorkGrandInquisitorItems) -> None:
        data: ZorkGrandInquisitorItemData = item_data[item]

        if data.game_keys is None:
            return

        if ZorkGrandInquisitorTags.INVENTORY_ITEM in data.tags:
            if data.game_keys[0] in [self._read_game_state_value_for(key) for key in range(101, 150)]:
                self.game_state_manager.drop_inventory_item(data.game_keys[0])
                return

            inventory_slot: Optional[int] = self._inventory_slot_for(item)

            if inventory_slot is None:
                return

            self._write_game_state_value_for(inventory_slot, 0)

            if inventory_slot != 9:
                self.available_inventory_slots.add(inventory_slot)
        elif ZorkGrandInquisitorTags.SPELL in data.tags:
            self._write_game_state_value_for(data.game_keys[0], 0)
        elif ZorkGrandInquisitorTags.TOTEM in data.tags:
            self._write_game_state_value_for(data.game_keys[0], 0)

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
                if self._read_game_state_value_for(i) == data.game_keys[0]:
                    return i

        if self._read_game_state_value_for(9) == data.game_keys[0]:
            return 9

        if self._read_game_state_value_for(4512) == data.game_keys[0]:
            return 4512

        return None

    def _read_game_state_value_for(self, key: int) -> int:
        return self.game_state_manager.read_game_state_value_for(key)

    def _write_game_state_value_for(self, key: int, value: int) -> None:
        self.game_state_manager.write_game_state_value_for(key, value)

    def _write_game_flags_value_for(self, key: int, value: int) -> None:
        self.game_state_manager.write_game_flags_value_for(key, value)

    def _player_has(self, item: ZorkGrandInquisitorItems) -> bool:
        return item in self.received_items

    def _player_is_at(self, game_location: str) -> bool:
        return self.game_location == game_location

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
