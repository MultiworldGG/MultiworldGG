import asyncio
import traceback
import colorama

import ModuleUpdate
import Utils
from BaseClasses import ItemClassification
from MultiServer import mark_raw
from NetUtils import ClientStatus
from settings import get_settings
from worlds._bizhawk.context import AuthStatus

ModuleUpdate.update()

apname = Utils.instance_name if Utils.instance_name else "Archipelago"
import logging
import typing
from pymem import pymem
from pymem.exception import ProcessNotFound, ProcessError, PymemError, WinAPIError

from CommonClient import server_loop, gui_enabled, get_base_parser

from .. import options, TCSUniversalTrackerAPWorldVersionMismatchError
from ..constants import GAME_NAME, AP_WORLD_VERSION, SETTINGS_KEY
from ..host_yaml_settings import LegoStarWarsTCSSettings
from ..slot_data import TCSSlotDataOptions, ApWorldVersion, get_slot_data_name
from .client_text import ClientText, clean_string
from .common_addresses import (
    ShopType,
    CantinaRoom,
    GameState1,
    OPENED_MENU_DEPTH_ADDRESS,
    CURRENT_P_AREA_DATA_ADDRESS,
    CHARACTER_CHARACTER_DATA_POINTER,
    CHARACTER_DATA_ID,
)
from .custom_save_data import CustomSaveDataSections, CUSTOM_SAVE_DATA_SECTION_SIZE, CustomSaveFlags2
from .location_checkers.free_play_completion import FreePlayAreaCompletionChecker
from .location_checkers.bonus_level_completion import BonusAreaCompletionChecker
from .location_checkers.minikits import MinikitChecker
from .location_checkers.ridesanity import RidesanityChecker
from .location_checkers.true_jedi_and_minikits_gold_brick import TrueJediAndPowerBrickAndMinikitBrickChecker
from .location_checkers.shop_purchases import PurchasedExtrasChecker, PurchasedCharactersChecker
from .events import (
    EventManager,
    OnLevelChangeEvent,
    OnAreaChangeEvent,
    OnUnhookFromGameEvent,
    OnReceiveSlotDataEvent,
    OnGameWatcherTickEvent,
    OnPlayerCharacterIdChangeEvent,
    OnGameWatcherDisconnectedTickEvent,
)
from .game_state_modifiers import ClientComponent
from .game_state_modifiers.extras import AcquiredExtras
from .game_state_modifiers.characters import AcquiredCharacters
from .game_state_modifiers.cantina_reloader import CantinaReloader
from .game_state_modifiers.death_link_manager import DeathLinkManager
from .game_state_modifiers.generic import AcquiredGeneric
from .game_state_modifiers.goal_manager import GoalManager
from .game_state_modifiers.levels import UnlockedChapterManager
from .game_state_modifiers.locked_cantina_door_display import LockedCantinaDoorDisplay
from .game_state_modifiers.minikits import AcquiredMinikits
from .game_state_modifiers.power_ups import PowerUpReceiver
from .game_state_modifiers.shop_names_replacer import ShopNamesReplacer
from .game_state_modifiers.studs import STUDS_AP_ID_TO_VALUE, give_studs_item
from .game_state_modifiers.text_display import InGameTextDisplay
from .game_state_modifiers.text_replacer import TextReplacer
from .game_state_modifiers.uncap_high_jump import UncapHighJump
from .game_state_modifiers.level_specific_fixes import LevelSpecificFixes
from .game_state_modifiers.patches import apply_game_patches
from .game_state_modifiers.auto_collect_pickups import AutoCollectPickups
from .game_state_modifiers.run_in_a_window import RunInAWindow
from .game_version_check import get_game_version, GameVersion, gog_to_steam

from ..data.levels import Level
from ..data.locations import LOCATION_NAME_TO_ID
from ..data_storage import (
    DATA_STORAGE_KEY_SUFFIX,
    COMPLETED_FREE_PLAY_KEY_PREFIX,
    COMPLETED_TRUE_JEDI_KEY_PREFIX,
    COMPLETED_10_MINIKITS_KEY_PREFIX,
    COMPLETED_BONUSES_KEY_PREFIX,
    COLLECTED_POWER_BRICKS_KEY_PREFIX,
    MINIKIT_GOAL_SUBMITTED_PREFIX,
)


# Universal Tracker client integration.
try:
    from worlds.tracker.TrackerClient import (
        TrackerGameContext as CommonContext,
        TrackerCommandProcessor as ClientCommandProcessor,
    )
except ImportError:
    from CommonClient import CommonContext, ClientCommandProcessor
    UNIVERSAL_TRACKER_LOADED = False
else:
    UNIVERSAL_TRACKER_LOADED = True


logger = logging.getLogger("Client")
debug_logger = logging.getLogger("TCS Debug")

# Aliases for clarity in typing.
MemoryAddress = int
MemoryOffset = int
BitMask = int
LocationId = int


PROCESS_NAME = "LEGOStarWarsSaga"


CURRENT_LEVEL_ID = 0x951bc0  # 2 bytes (or more)
# While in the Cantina and in the shop room, all extras that have been received, but not purchased, must be locked,
# otherwise those extras cannot be bought from the shop.
# When entering the Cantina, all purchased extras that have not been received will need to be locked because entering
# the cantina will unlock all extras that have been purchased.
LEVEL_ID_CANTINA = 325

CURRENT_SAVE_SLOT = 0x802014  # byte, 255/-1 for no save file loaded. [0-5] for save file [1-6]

# Unsure what this is, but it changes when moving between rooms in the cantina and appears to persist while in a level,
# so this can be used to both see what room the player is in when they are in the cantina, and to see what Episode they
# are in at a glance (the current Episode can be determined exactly from the current level ID if this turns out to be
# unreliable for checking the current episode)
# 0: Main room with the shop (what we care about)
# 1: Episode 1 room
# 2: Episode 2 room
# 3: Episode 3 room
# 4: Episode 4 room
# 5: Episode 5 room
# 6: Episode 6 room
# 7: Outside junkyard
# 8: Bonuses room
# 9: Bounty Hunter missions room
CANTINA_ROOM_ID = 0x87b480
CANTINA_ROOM_WITH_SHOP = 0

# Appears to be 1 while in the shop, and 0 otherwise. But becomes 0 when playing a cutscene from within the shop.
# SHOP_CHECK2 = 0x880494  # byte
ACTIVE_SHOP_TYPE_ADDRESS = 0x8801cc


# CUSTOM_CHARACTER_1_NAME = 0x86e520  # char[16], null-terminated, so 15 usable characters
# CUSTOM_CHARACTER_2_NAME = 0x86e558  # char[16], null-terminated, so 15 usable characters

# Byte
# 0 = Blue Lightsaber (requires any Jedi unlocked)
# 1 = Green Lightsaber (default) (requires any Jedi unlocked)
# 2 = Red Lightsaber (requires any Sith unlocked)
# 3 = Purple Lighsaber (requires any Jedi unlocked)
# 4 = Red Blaster (always available)
# 5 = Blue Blaster (always available)
# 6 = Pistol (always available)
# 7 = Shiny Pistol (always available)
# 8 = Crossbow (bowcaster) (requires *unknown* unlocked (probably Chewbacca or Wookie))
# 9 = There is no 9
CUSTOM_CHARACTER_1_WEAPON = 0x86e510

# todo: Add optional gold brick and hint purchase checks (they should go in a different module)
# class PurchasedGoldBricks:
#     pass
# class PurchasedHints:
#     pass

class NoProcessError(RuntimeError):
    pass


LEVEL_ID_KEY_PREFIX = "tcs_current_level_id_"
CANTINA_ROOM_KEY_PREFIX = "tcs_cantina_room_"


class LegoStarWarsTheCompleteSagaCommandProcessor(ClientCommandProcessor):
    AUTO_COLLECT_PICKUPS_ENABLED = ("enabled", "on", "yes")
    AUTO_COLLECT_PICKUPS_DISABLED = ("disabled", "off", "no")
    AUTO_COLLECT_PICKUPS_VEHICLES_ONLY = ("vehicles", "vehicles_only", "vehicles only",
                                          "vehicle", "vehicle_only", "vehicle only",
                                          "vehicle_levels_only", "vehicle levels only",
                                          "vehicle_levels", "vehicle levels")
    AUTO_COLLECT_PICKUPS_ALL = (AUTO_COLLECT_PICKUPS_ENABLED
                                + AUTO_COLLECT_PICKUPS_DISABLED
                                + AUTO_COLLECT_PICKUPS_VEHICLES_ONLY)

    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_color_test(self):
        """
        Test text color choices. You need to be connected to a server to use this command.

        A number of these colors are probably reading parts of the game's memory that are not supposed to be colors. If
        some of these colors display the wrong color while playing, please report that as an issue in the discord thread
        for Lego Star Wars: The Complete Saga.
        """
        ctx = self.ctx
        if isinstance(ctx, LegoStarWarsTheCompleteSagaContext):
            if ctx.last_connected_slot is None or not ctx.is_in_game():
                logger.info("Load into the game and connect to a server first.")
                return
            from ..options import TextColorChoice
            for value, name in TextColorChoice.name_lookup.items():
                msg = ctx.client_text.from_text_color_choice(TextColorChoice(value), name)
                ctx.text_display.queue_message(msg)
            logger.info("Demonstrating text color choices.")

    @mark_raw
    def _cmd_auto_collect_pickups(self, mode: str = ""):
        """
        Toggle automatic collection of spawned pickups. Either on, off, or on for vehicle levels only.

        :param mode: on/off/vehicles, or leave blank to toggle between on/off while maintaining whether only vehicle
        levels are affected.
        """
        ctx = self.ctx
        if isinstance(ctx, LegoStarWarsTheCompleteSagaContext):
            if ctx.last_connected_slot is None or not ctx.is_in_game():
                logger.info("Load into the game and connect to a server first.")
                return
            component = ctx.auto_collect_pickups
            if mode == "":
                # Act like a toggle, while maintaining vehicles_only status.
                component.update(ctx, not component.enabled, component.vehicles_only)
            else:
                best_pick, ok, message = Utils.get_intended_text(mode, self.AUTO_COLLECT_PICKUPS_ALL)
                if not ok:
                    logger.info(message)
                    return
                if ok:
                    if best_pick in self.AUTO_COLLECT_PICKUPS_ENABLED:
                        component.update(ctx, True, False)
                    elif best_pick in self.AUTO_COLLECT_PICKUPS_DISABLED:
                        component.update(ctx, False, False)
                    elif best_pick in self.AUTO_COLLECT_PICKUPS_VEHICLES_ONLY:
                        component.update(ctx, True, True)
                    else:
                        logger.error("Unrecognised value '%s' from fuzzy matching", best_pick)
            if component.enabled:
                if component.vehicles_only:
                    logger.info("Enabled automatic pickup collection (vehicle levels only)")
                else:
                    logger.info("Enabled automatic pickup collection")
            else:
                logger.info("Disabled automatic pickup collection")

    def _cmd_toggle_death_link(self):
        """Toggle Death Link on/off. Whether Death Link is enabled is stored in your save data, so the client will
        remember if Death Link was toggled the next time you connect."""
        ctx = self.ctx
        if isinstance(ctx, LegoStarWarsTheCompleteSagaContext):
            if ctx.last_connected_slot is None or not ctx.is_in_game():
                logger.info("Load into the game and connect to a server first.")
                return
            ctx.death_link_manager.toggle_death_link(ctx)
            if ctx.death_link_manager.death_link_enabled:
                logger.info("Death Link enabled.")
            else:
                logger.info("Death Link disabled.")

    def _impl_cmd_debug_memory_peek(self, num_bytes_to_read: str, *addresses: str, delay: int = 0):
        ctx = self.ctx
        if not isinstance(ctx, LegoStarWarsTheCompleteSagaContext):
            return
        if not addresses:
            logger.info("At least one address is required")
            return
        process = ctx.game_process
        if process is None:
            logger.info("The client is not connected to the game. The command cannot run.")
            return
        try:
            bytes_to_read = int(num_bytes_to_read)
            if bytes_to_read > 256:
                logger.info("Too many bytes to read, maximum is 256, but got %i", bytes_to_read)
                return
            if bytes_to_read < 1:
                logger.info("Too few bytes to read, minimum is 1, but got %i", bytes_to_read)
                return
            address_ints: list[int] = [int(addr, base=16) for addr in addresses]
        except ValueError as ex:
            logger.info("Could not parse command arguments: %s", ex)
        else:
            if delay > 0:
                import time
                # The client freezes for the duration, so there is no point logging and then sleeping 1s at a time in a
                # loop.
                time.sleep(delay)
            path = []
            # The first address is absolute, and is assumed to be intended for the GOG version of the game, so must be
            # adjusted if the player is playing the STEAM version of the game.
            last_address = ctx.adjust_gog_address(address_ints[0])
            for offset_address in address_ints[1:]:
                last_address_points_to = process.read_uint(last_address)
                path.append(last_address)
                if last_address_points_to == 0:
                    logger.info("%#x is a null pointer; stopping here.", last_address)
                    return
                else:
                    next_address = last_address_points_to + offset_address
                    logger.info("%#x points to %#x. Adding offset of %#x gives %#x.",
                                last_address, last_address_points_to, offset_address, next_address)
                    last_address = next_address
            value = process.read_bytes(last_address, bytes_to_read)
            logger.info("At %#x, read %i bytes to get: %s", last_address, bytes_to_read, value.hex())

    def _cmd_debug_memory_peek(self, num_bytes_to_read: str, *addresses: str):
        """Debug command to peek at the game's memory, given the number of bytes to read, and a series of offset
        addresses in hexadecimal. The APWorld developer may provide you a command to run to help identify issues you are
        having."""
        self._impl_cmd_debug_memory_peek(num_bytes_to_read, *addresses, delay=0)

    def _cmd_debug_delayed_memory_peek(self, seconds_delay: str, num_bytes_to_read: str, *addresses: str):
        """Debug command to peek at the game's memory after a delay, given the number of bytes to read, and a series of
        offset addresses in hexadecimal. The APWorld developer may provide you a command to run to help identify issues
        you are having. The client will freeze for the duration of the delay."""
        try:
            seconds_delay = int(seconds_delay)
            if seconds_delay < 0:
                raise ValueError("Minimum delay is 0 seconds")
            if seconds_delay > 10:
                raise ValueError("Maximum delay is 10 seconds")
        except ValueError as ex:
            logger.info("Could not parse seconds_delay as an integer: %s", ex)
        else:
            self._impl_cmd_debug_memory_peek(num_bytes_to_read, *addresses, delay=seconds_delay)

    def _cmd_toggle_windowed(self):
        """Toggle whether the game should run in a window. You will need to enter the Video Settings menu and Confirm
        for the game to update, or alt+tab out and back in. This toggle value is stored in your host.yaml and will be
        applied by the client when connecting to the game (you will still need to enter the Video Settings menu or
        alt-tab if the windowed toggle is enabled)."""
        ctx = self.ctx
        assert isinstance(ctx, LegoStarWarsTheCompleteSagaContext)
        settings: LegoStarWarsTCSSettings = get_settings()[SETTINGS_KEY]
        inverted = not settings.run_in_a_window
        ctx.run_in_a_window.set_windowed(ctx, inverted)
        settings.run_in_a_window = inverted
        settings._changed = True

    if UNIVERSAL_TRACKER_LOADED:
        # noinspection PyUnresolvedReferences
        def _cmd_ut_toggle_all_glitches(self):
            """Toggle showing glitched logic for the highest logic difficulty instead of just the next logic difficulty
            above the logic difficulty you chose in your YAML options (default)."""
            item_name = "UT_GLITCHED_ALL"
            if item_name not in self.ctx.tracker_core.manual_items:
                self._cmd_manually_collect(item_name)
                logger.info("Glitched logic from the highest logic difficulty will now be shown.")
            else:
                # Same as UT's _cmd_reset_manually_collect, but only removing the item that says all glitches should be
                # used in glitched logic.
                manual_items = self.ctx.tracker_core.manual_items.copy()
                manual_items.remove(item_name)
                self.ctx.tracker_core.manual_items = manual_items
                self.ctx.persist_seed_data()
                self.ctx.updateTracker()
                logger.info("Glitched logic from only the next logic difficulty will now be shown.")


class LegoStarWarsTheCompleteSagaContext(CommonContext):
    command_processor = LegoStarWarsTheCompleteSagaCommandProcessor
    game = GAME_NAME
    items_handling = 0b111  # Fully remote

    # Need to override Universal Tracker's "Tracker" tag, otherwise it sets self.game = "" when disconnecting.
    tags = set()

    # Copied from BizHawkClientContext
    server_seed_name: str | None = None
    auth_status: AuthStatus
    password_requested: bool

    disabled_locations: set[int]  # Server state.

    game_process: pymem.Pymem | None = None
    #previous_level_id: int = -1
    current_level_id: int = 0  # Title screen
    current_p_area_data: int = 0  # NULL
    current_cantina_room: CantinaRoom = CantinaRoom.UNKNOWN
    current_p1_character_id: int | None = None
    current_p2_character_id: int | None = None

    game_version: GameVersion = GameVersion.GOG
    # In the case of an unrecognised version, an overall memory offset may be set.
    overall_memory_offset: int = 0
    event_manager: EventManager

    # Client state.
    acquired_characters: AcquiredCharacters
    acquired_extras: AcquiredExtras
    acquired_generic: AcquiredGeneric
    acquired_minikits: AcquiredMinikits
    unlocked_chapter_manager: UnlockedChapterManager
    text_display: InGameTextDisplay
    locked_cantina_door_info: LockedCantinaDoorDisplay
    goal_manager: GoalManager
    power_up_receiver: PowerUpReceiver
    client_expected_idx: int

    # Location checkers.
    free_play_completion_checker: FreePlayAreaCompletionChecker
    true_jedi_and_power_brick_and_minikit_brick_checker: TrueJediAndPowerBrickAndMinikitBrickChecker
    minikit_checker: MinikitChecker
    purchased_extras_checker: PurchasedExtrasChecker
    purchased_characters_checker: PurchasedCharactersChecker
    bonus_area_completion_checker: BonusAreaCompletionChecker
    ridesanity_checker: RidesanityChecker

    # Game-state only.
    text_replacer: TextReplacer
    death_link_manager: DeathLinkManager
    uncap_high_jump: UncapHighJump
    cantina_reloader: CantinaReloader
    shop_names_replacer: ShopNamesReplacer

    # Customizable client behaviour
    received_item_messages: options.ReceivedItemMessages = options.ReceivedItemMessages(
        options.ReceivedItemMessages.option_all)
    checked_location_messages: bool = True
    client_text: ClientText
    auto_collect_pickups: AutoCollectPickups
    run_in_a_window: RunInAWindow

    # A few components are permanent and will need to be manually re-subscribed to receive events because the components
    # won't be re-created.
    permanent_components: tuple[ClientComponent, ...]

    fully_connected: bool
    last_connected_slot: str | None = None
    last_connected_seed_name: str | None = None
    last_loaded_save_file: int | None = None

    def __init__(self, server_address: typing.Optional[str] = None, password: typing.Optional[str] = None) -> None:
        super().__init__(server_address, password)

        # Copied from BizHawkClientContext
        self.auth_status = AuthStatus.NOT_AUTHENTICATED
        self.password_requested = False

        self.disabled_locations = set()

        # Event manager must be set before other attributes, so that the event manager can look for methods that are
        # subscribing to events on the other attributes.
        self.event_manager = EventManager()

        self.client_text = ClientText()
        self.locked_cantina_door_info = LockedCantinaDoorDisplay()
        self.uncap_high_jump = UncapHighJump()
        self.cantina_reloader = CantinaReloader()
        self.level_specific_fixes = LevelSpecificFixes()
        self.text_display = InGameTextDisplay()
        self.run_in_a_window = RunInAWindow()
        # It is not ideal to leak `self` in __init__. The TextReplacer methods could be updated to include a TCSContext
        # parameter if needed, instead of leaking `self`. Alternatively, the TextReplacer could be created only when
        # successfully connecting to the game.
        self.text_replacer = TextReplacer(self)
        self.permanent_components = (
            self.uncap_high_jump,
            self.cantina_reloader,
            self.locked_cantina_door_info,
            self.level_specific_fixes,
            self.text_replacer,
            self.text_display,
            self.run_in_a_window,
        )

        self._reset_non_permanent_components()

        self.client_expected_idx = 0

        self.fully_connected = False

    def __setattr__(self, key, value) -> None:
        super().__setattr__(key, value)
        if isinstance(value, ClientComponent):
            # Subscribe methods that want to receive events.
            self.event_manager.subscribe_events(value)

    def _get_datastorage_key(self, key_prefix: str):
        return key_prefix + DATA_STORAGE_KEY_SUFFIX.format(team=self.team, player=self.slot)

    def _is_datastorage_key(self, to_check: str, prefix: str):
        return to_check.startswith(prefix) and to_check == self._get_datastorage_key(prefix)

    async def check_locations(self, locations: typing.Collection[int]) -> set[int]:
        # Filter out locations the client thinks it has already checked and sent to the server.
        # The base check_locations implementation only filters out locations the server says are checked.
        # If some locations are sent, but the connection is lost, CommonClient sends the contents of
        # self.locations_checked to the server when reconnecting. self.locations_checked is not cleared out when an
        # unintended disconnect (allow_autoreconnect=True) occurs, allowing for any missed location checks to be
        # re-sent.
        locations = set(locations).difference(self.locations_checked)
        return await super().check_locations(locations)

    def on_print_json(self, args: dict) -> None:
        super().on_print_json(args)

        if not self.checked_location_messages and not self.received_item_messages:
            return

        if "type" in args and args["type"] == "ItemSend":
            item = args["item"]
            recipient = args["receiving"]

            classification = ItemClassification(item.flags)
            is_progression = ItemClassification.progression in classification

            # Receiving an item from the server
            if self.slot_concerns_self(recipient):
                item_name = self.item_names.lookup_in_game(item.item)
                item_str = self.client_text.from_classification(classification, clean_string(item_name))
                if self.slot_concerns_self(item.player):
                    # This counts as both a checked location and a received item.
                    if (
                            self.checked_location_messages
                            or (self.received_item_messages and
                                (is_progression or self.received_item_messages == "all"))
                    ):
                        location_name = self.location_names.lookup_in_game(item.location)
                        location_str = self.client_text.location_name(clean_string(location_name))
                        message = f"Found {item_str} ({location_str})"
                        self.text_display.queue_message(message)
                else:
                    if self.received_item_messages and (is_progression or self.received_item_messages == "all"):
                        finder = self.player_names[item.player]
                        finder_str = self.client_text.player_name(clean_string(finder))
                        location_name = self.location_names.lookup_in_slot(item.location, item.player)
                        location_str = self.client_text.location_name(clean_string(location_name))
                        message = f"Received {item_str} from {finder_str} ({location_str})"
                        self.text_display.queue_message(message)
            # Sending an item to the server.
            elif self.slot_concerns_self(item.player):
                item_name = self.item_names.lookup_in_slot(item.item, recipient)
                item_str = self.client_text.from_classification(classification, clean_string(item_name))

                if self.slot_concerns_self(recipient):
                    # Should not happen?
                    location_name = self.location_names.lookup_in_game(item.location)
                    location_str = self.client_text.location_name(clean_string(location_name))
                    message = f"Sent {item_str}...to myself? ({location_str}) Please report this."
                    self.text_display.queue_message(message)
                else:
                    if self.checked_location_messages:
                        owner = self.player_names[recipient]
                        owner_str = self.client_text.player_name(clean_string(owner))
                        location_name = self.location_names.lookup_in_game(item.location)
                        location_str = self.client_text.location_name(clean_string(location_name))
                        message = f"Sent {item_str} to {owner_str} ({location_str})"
                        self.text_display.queue_message(message)

    @staticmethod
    def _validate_version(slot_data: typing.Mapping[str, typing.Any]) -> bool:
        # All versions of the TCS apworld should have written "apworld_version" into slot data, if it is absent then
        # there is an error.
        # This accesses the slot data as its raw value because very old versions of the apworld will not have slot data
        # that is parsable as TCSSlotDataoptions.
        # Ensure the read data from slot_data is a tuple rather than a list so that the comparisons with
        # AP_WORLD_VERSION work as expected.
        server_apworld_version = tuple(slot_data[get_slot_data_name(ApWorldVersion)])
        if AP_WORLD_VERSION != server_apworld_version:
            # If the major version does not match, the versions are incompatible.
            # If the minor version of the client is less than the server, then the versions are incompatible.
            if AP_WORLD_VERSION[0] != server_apworld_version[0] or AP_WORLD_VERSION[1] < server_apworld_version[1]:
                logger.error("Error: The multiworld was generated with apworld version %s, which is not compatible with"
                             " the client's apworld version %s. Disconnecting.",
                             server_apworld_version, AP_WORLD_VERSION)
                return False
            else:
                # If the minor version of the client is equal, then the patch version needs to be compared.
                if AP_WORLD_VERSION[1] == server_apworld_version[1] and AP_WORLD_VERSION[2] < server_apworld_version[2]:
                    # The client has an older patch version than the server, this should just mean the client is
                    # potentially missing some backwards compatible bug fixes, but the bug fixes are likely forwards
                    # compatible, so the connection will be allowed, but with a warning message.
                    logger.warning("Warning: Connected to a multiworld generated with a different, but probably"
                                   " compatible, apworld version %s. The client apworld version is %s. Updating the"
                                   " client version is recommended to avoid issues. Please update your apworld version"
                                   " before reporting any issues.",
                                   server_apworld_version, AP_WORLD_VERSION)
                else:
                    # The client has matching major version and newer minor+patch version, everything *should* be OK
                    # because the client has only additional backwards compatible features and bug fixes.
                    logger.info("Info: Connected to a multiworld generated with a different, but compatible, apworld"
                                " version %s. The client apworld version is %s.",
                                server_apworld_version, AP_WORLD_VERSION)
        else:
            logger.info("Info: Connected to multiworld generated on the same version as the client")

        return True

    def _validate_seed_name_against_save_data(self, new_seed_name: str) -> tuple[bool, str | None]:
        save_data_seed_name = self.read_seed_name_from_save_data()
        debug_logger.info("Seed name from save file is %s", save_data_seed_name)
        debug_logger.info("Seed name from server is %s", new_seed_name)
        if save_data_seed_name is not None:
            if new_seed_name != save_data_seed_name:
                Utils.async_start(self.disconnect())
                logger.info("Connection aborted: The server's seed does not match the save file's seed.")
                self.last_connected_seed_name = None
                self.last_connected_slot = None
                return False, None
            else:
                return True, None
        return True, new_seed_name

    def _read_slot_data(self, slot_data: TCSSlotDataOptions, first_time_setup: bool):
        # The connection to the server is assumed to be OK by this point, so slot_data can now be used to adjust client
        # behaviour.

        on_receive_slot_data_event = OnReceiveSlotDataEvent(self, slot_data, first_time_setup)

        self.client_text = ClientText.from_slot_data(on_receive_slot_data_event.slot_data)

        self.received_item_messages = on_receive_slot_data_event.slot_data.received_item_messages

        self.checked_location_messages = bool(on_receive_slot_data_event.slot_data.checked_location_messages)

        # Fire the event so that the various client components initialize themselves from the slot_data.
        self.event_manager.fire_event(on_receive_slot_data_event)

        self.client_expected_idx = 0

    def on_package(self, cmd: str, args: dict):
        warn_universal_tracker_is_disabled = False
        if UNIVERSAL_TRACKER_LOADED and cmd == "Connected":
            try:
                super().on_package(cmd, args)
            except TCSUniversalTrackerAPWorldVersionMismatchError:
                # If the multiworld apworld version does not match the client apworld version, TCS's Universal Tracker
                # support raises this exception to reject Universal Tracker usage when the apworld versions do not match
                # because there could be logic differences between apworld versions.
                # The client, however, is allowed to connect to older versions that it has backwards compatibility for,
                # so if the player has Universal Tracker installed, connecting should be allowed to continue, even if
                # Universal Tracker will not be usable.
                warn_universal_tracker_is_disabled = True
        else:
            super().on_package(cmd, args)

        if cmd == "RoomInfo":
            new_seed_name = args["seed_name"]

            if self.is_in_game():
                ok, _server_seed_name = self._validate_seed_name_against_save_data(new_seed_name)
                if not ok:
                    return

            if self.last_connected_seed_name is not None and self.last_connected_seed_name != new_seed_name:
                self.on_multiworld_or_slot_changed()
                # The last connected slot is irrelevant if the multiworld itself has changed.
                self.last_connected_slot = None
            self.last_connected_seed_name = new_seed_name
            self.seed_name = new_seed_name
            if self.server_version < (0, 6, 2):
                logger.warning("Lego Star Wars: The Complete Saga works best with servers running AP version 0.6.2 or"
                               " newer. The connected server is running version %s, so some same-slot co-op and tracker"
                               " features will not be available.", self.server_version.as_simple_string())
        elif cmd == "Connected":
            if self.last_connected_seed_name is None:
                # The client should be just about to disconnect from failing to match the server's seed.
                # Disconnect again just in-case.
                Utils.async_start(self.disconnect())
                return

            slot_data = args.get("slot_data")
            if isinstance(slot_data, typing.Mapping):
                if not self._validate_version(slot_data):
                    # _validate_version should have logged the appropriate message to the user.
                    self.last_connected_seed_name = None
                    Utils.async_start(self.disconnect())
                    return
                if warn_universal_tracker_is_disabled:
                    logger.info("Universal Tracker features are disabled due to the client APWorld version not matching"
                                " the APWorld version that generated the multiworld.")
            else:
                logger.error("Error: slot_data missing from Connected message, something is probably broken.")
                Utils.async_start(self.disconnect())
                return

            # It is assumed that the player must be loaded into a save file or a new game at this point.
            ok, server_seed_name_to_write = self._validate_seed_name_against_save_data(self.last_connected_seed_name)
            if not ok:
                self.seed_name = None
                self.last_connected_seed_name = None
                return

            if server_seed_name_to_write is not None:
                self.write_seed_name(server_seed_name_to_write)

            new_slot = self.auth

            if self.last_connected_slot is not None and self.last_connected_slot != new_slot:
                self.on_multiworld_or_slot_changed()
            if self.read_slot_name() is None:
                self.write_slot_name(new_slot)
                self.ap_first_time_setup()
                first_time_setup = True
            else:
                first_time_setup = False
            self.disabled_locations = set(LOCATION_NAME_TO_ID.values()) - self.server_locations

            slot_data_options = TCSSlotDataOptions.from_slot_data(slot_data)
            self._read_slot_data(slot_data_options, first_time_setup)

            # Setting this to non-None indicates to the game watcher loop to start fully running.
            self.last_connected_slot = self.auth
            self.auth_status = AuthStatus.AUTHENTICATED
            # Get, and subscribe to, updates to Free Play completions
            listen_keys = list(
                map(
                    self._get_datastorage_key,
                    (
                        COMPLETED_FREE_PLAY_KEY_PREFIX,
                        COMPLETED_TRUE_JEDI_KEY_PREFIX,
                        COMPLETED_10_MINIKITS_KEY_PREFIX,
                        COMPLETED_BONUSES_KEY_PREFIX,
                        COLLECTED_POWER_BRICKS_KEY_PREFIX,
                        MINIKIT_GOAL_SUBMITTED_PREFIX,
                    )
                )
            )
            Utils.async_start(self.send_msgs(
                [
                    {
                        "cmd": "Get",
                        "keys": listen_keys
                    },
                    {
                        "cmd": "SetNotify",
                        "keys": listen_keys
                    }
                ]
            ))
        elif cmd == "SetReply":
            # todo: After receiving Gold Bricks to write into save data, mark some part of ctx as dirty and get the
            #  client to forcefully autosave the game (Set 0x921e0c/0x921e08 to 1 if the save timers
            #  (0x00921E10/0x00921E14) are not > 0.0, todo: Check if these addresses were GOG or Steam).
            key: str = args["key"]
            if self._is_datastorage_key(key, COMPLETED_FREE_PLAY_KEY_PREFIX):
                value = args["value"]
                if value is not None:
                    self.free_play_completion_checker.update_from_datastorage(self, value)
            elif self._is_datastorage_key(key, COMPLETED_TRUE_JEDI_KEY_PREFIX):
                value = args["value"] or ()
                previous_value = args["original_value"] or ()
                new_values = set(value)
                new_values.difference_update(previous_value)
                if new_values:
                    self.true_jedi_and_power_brick_and_minikit_brick_checker.update_from_datastorage(
                        self, new_true_jedi_area_ids=new_values)
            elif self._is_datastorage_key(key, COMPLETED_10_MINIKITS_KEY_PREFIX):
                value = args["value"] or ()
                previous_value = args["original_value"] or ()
                new_values = set(value)
                new_values.difference_update(previous_value)
                if new_values:
                    self.true_jedi_and_power_brick_and_minikit_brick_checker.update_from_datastorage(
                        self, new_minikits_gold_brick_area_ids=new_values)
            elif self._is_datastorage_key(key, COMPLETED_BONUSES_KEY_PREFIX):
                value = args["value"] or ()
                previous_value = args["original_value"] or ()
                new_values = set(value)
                new_values.difference_update(previous_value)
                if new_values:
                    self.bonus_area_completion_checker.update_from_datastorage(self, new_values)
            elif self._is_datastorage_key(key, COLLECTED_POWER_BRICKS_KEY_PREFIX):
                value = args["value"] or ()
                previous_value = args["original_value"] or ()
                new_values = set(value)
                new_values.difference_update(previous_value)
                if new_values:
                    self.true_jedi_and_power_brick_and_minikit_brick_checker.update_from_datastorage(
                        self, new_power_brick_area_ids=new_values)
            elif self._is_datastorage_key(key, MINIKIT_GOAL_SUBMITTED_PREFIX):
                value = args["value"]
                if value:
                    self.goal_manager.complete_minikit_goal_from_datastorage(self)

        elif cmd == "Retrieved":
            keys: dict[str, typing.Any] = args["keys"]
            completed_free_play = keys.get(self._get_datastorage_key(COMPLETED_FREE_PLAY_KEY_PREFIX))
            if completed_free_play:
                self.free_play_completion_checker.update_from_datastorage(self, completed_free_play)
            completed_true_jedi = keys.get(self._get_datastorage_key(COMPLETED_TRUE_JEDI_KEY_PREFIX))
            if completed_true_jedi:
                self.true_jedi_and_power_brick_and_minikit_brick_checker.update_from_datastorage(
                    self, new_true_jedi_area_ids=completed_true_jedi)
            completed_10_minikits = keys.get(self._get_datastorage_key(COMPLETED_10_MINIKITS_KEY_PREFIX))
            if completed_10_minikits:
                self.true_jedi_and_power_brick_and_minikit_brick_checker.update_from_datastorage(
                    self, new_minikits_gold_brick_area_ids=completed_10_minikits)
            completed_bonuses = keys.get(self._get_datastorage_key(COMPLETED_BONUSES_KEY_PREFIX))
            if completed_bonuses:
                self.bonus_area_completion_checker.update_from_datastorage(self, completed_bonuses)
            collected_power_bricks = keys.get(self._get_datastorage_key(COLLECTED_POWER_BRICKS_KEY_PREFIX))
            if collected_power_bricks:
                self.true_jedi_and_power_brick_and_minikit_brick_checker.update_from_datastorage(
                    self, new_power_brick_area_ids=collected_power_bricks)
            completed_minikit_goal = keys.get(self._get_datastorage_key(MINIKIT_GOAL_SUBMITTED_PREFIX))
            if completed_minikit_goal:
                self.goal_manager.complete_minikit_goal_from_datastorage(self)
        elif cmd == "RoomUpdate":
            self.shop_names_replacer.update_player_names(self)

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        text = data.get("cause", "")
        if text:
            text = f"DeathLink: {text}"
        else:
            text = f"DeathLink: Received from {data['source']}"
        previous_death = self.last_death_link
        super().on_deathlink(data)
        self.death_link_manager.on_deathlink(previous_death, self.last_death_link, text)

    def _update_datastorage_area_ids(self, key_prefix: str, area_ids: list[int], log_name: str):
        if self.server_version < (0, 6, 2):
            # Using the "update" operation on list values was only added in AP 0.6.2, so an older server version will
            # disconnect the client.
            return
        if not area_ids:
            return
        debug_logger.info("Sending %s area_ids to datastorage: %s", log_name, area_ids)
        Utils.async_start(self.send_msgs([{
            "cmd": "Set",
            "key": self._get_datastorage_key(key_prefix),
            "default": [],
            "want_reply": False,
            "operations": [{"operation": "update", "value": area_ids}]
        }]))

    def update_datastorage_free_play_completion(self, area_ids: list[int]):
        self._update_datastorage_area_ids(COMPLETED_FREE_PLAY_KEY_PREFIX, area_ids, "Free Play Completion")

    def update_datastorage_true_jedi_completion(self, area_ids: list[int]):
        self._update_datastorage_area_ids(COMPLETED_TRUE_JEDI_KEY_PREFIX, area_ids, "True Jedi Completion")

    def update_datastorage_10_minikits_completion(self, area_ids: list[int]):
        self._update_datastorage_area_ids(COMPLETED_10_MINIKITS_KEY_PREFIX, area_ids, "10/10 Minikits Completion")

    def update_datastorage_bonuses_completion(self, area_ids: list[int]):
        self._update_datastorage_area_ids(COMPLETED_BONUSES_KEY_PREFIX, area_ids, "Bonuses Completion")

    def update_datastorage_power_bricks_collected(self, area_ids: list[int]):
        self._update_datastorage_area_ids(COLLECTED_POWER_BRICKS_KEY_PREFIX, area_ids, "Power Bricks Collected")

    def update_datastorage_minikits_goal_submitted(self):
        debug_logger.info("Sending minikit-goal-submitted to datastorage")
        Utils.async_start(self.send_msgs([{
            "cmd": "Set",
            "key": self._get_datastorage_key(MINIKIT_GOAL_SUBMITTED_PREFIX),
            "default": False,
            "want_reply": False,
            "operations": [{"operation": "replace", "value": True}]
        }]))

    def on_multiworld_or_slot_changed(self):
        # The client is connecting to a different multiworld or slot to before, so reset all persisted client data.
        self.reset_persisted_client_data()

    def is_location_unchecked(self, location_id: int) -> bool:
        """Return whether a location id exists, but has not been checked according to server state and client state."""
        return ((location_id not in self.locations_checked
                 and location_id not in self.checked_locations)
                and self.is_location_sendable(location_id))

    def is_location_checked(self, location_id: int) -> bool:
        """Return whether a location id is checked according to server state or client state."""
        return location_id in self.locations_checked or location_id in self.checked_locations

    def is_location_sendable(self, location_id: int) -> bool:
        """Return whether a location exists according to server state."""
        return location_id not in self.disabled_locations

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = f"{apname} {self.game} Client (APWorld v{'.'.join(map(str, AP_WORLD_VERSION))})"
        if __debug__ and not Utils.is_frozen():
            ui.logging_pairs.append(("TCS Debug", "Debug"))
        return ui

    async def server_auth(self, password_requested: bool = False):
        self.password_requested = password_requested

        if self.game_process is None:
            logger.info("Awaiting connection to game process before authenticating")
            return

        if not self.is_in_game():
            logger.info("Awaiting a save file to be loaded, or a new game to be started, before authenticating")
            return

        if self.auth is None:
            # todo: Rework client data clearing to run here for slot name changes within the same multiworld.
            self.auth_status = AuthStatus.NEED_INFO
            await self.set_auth()

            if self.auth is None:
                # If a new game was started, there will be no username stored in the save file, so the user will need to
                # provide it.
                await self.get_username()

        if password_requested and not self.password:
            self.auth_status = AuthStatus.NEED_INFO
            await super().server_auth(password_requested)

        self.tags = set()
        await self.send_connect()
        self.auth_status = AuthStatus.PENDING

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth_status = AuthStatus.NOT_AUTHENTICATED
        self.server_seed_name = None
        if not allow_autoreconnect:
            # fixme: CommonClient's connect() calls disconnect(), meaning that the initial client components get
            #  replaced. This is not really a problem, just unnecessary (and doubles up some of the logging).
            self.reset_persisted_client_data()
            self.last_connected_slot = None
            self.last_connected_seed_name = None
        await super().disconnect(allow_autoreconnect)

    async def set_auth(self) -> None:
        slot_name = self.read_slot_name()
        if slot_name is not None:
            self.auth = slot_name
        else:
            # No slot name has been written to the save file yet, so the player will need to provide it.
            pass

    async def shutdown(self):
        logger.info("Shutting down client")
        await self.unhook_game_process()
        return await super().shutdown()

    async def open_game_process(self):
        try:
            process = pymem.Pymem(PROCESS_NAME)
            game_version, memory_offset = get_game_version(process)
            if game_version is None:
                logger.info(f"Connected to process but could not determine memory offsets. Supported game versions are"
                            f" Steam and GOG, make sure your LegoStarWarsSaga.exe has not been modified.")
                return False
            self.game_version = game_version
            self.overall_memory_offset = memory_offset

            self.game_process = process
            # Try for 5 seconds to patch the game before giving up.
            if not await apply_game_patches(self):
                for _ in range(5):
                    await asyncio.sleep(1.0)
                    if not await apply_game_patches(self):
                        logger.info("Waiting for the game to load more before patching...")
                    else:
                        break
                else:
                    logger.info("A connection to the game was made, but the game has not loaded enough to apply"
                                " patches, so the connection has been aborted.")
                    self.game_process = None
                    return False
            # Put the game into a window if the host.yaml settings request doing so. The vanilla game is always
            # fullscreen, so there is nothing to do if host.yaml says to play in fullscreen.
            settings: LegoStarWarsTCSSettings = get_settings()[SETTINGS_KEY]
            if settings.run_in_a_window:
                self.run_in_a_window.set_windowed(self, True)
            self.text_replacer = TextReplacer(self)

            if memory_offset != 0:
                logger.warning(
                    f"Connected to an unrecognised game version with memory offset {memory_offset:X}. Assuming the game"
                    f" version is a modified {game_version.name} version. Things could be very broken. Please report"
                    f" this in the Lego Star Wars: The Complete Saga thread in the Archipelago discord server.")
            else:
                logger.info(
                    "Connected to %s version successfully", game_version.name
                )
            return True
        except ProcessNotFound:
            logger.info(f"{PROCESS_NAME} process not found. Make sure it is running.")
            return False
        except ProcessError as err:
            logger.info(f"Unexpected error connecting to game process: {err}.")
            return False

    async def unhook_game_process(self):
        try:
            await self.event_manager.fire_event_async(OnUnhookFromGameEvent(self))
        finally:
            if self.game_process is not None:
                self.game_process.close_process()
                self.game_process = None
            logger.info("Unhooked game process")

    @property
    def _game_process(self) -> pymem.Pymem:
        process = self.game_process
        if process is None:
            raise NoProcessError("No process to read from")
        else:
            return process

    def adjust_gog_address(self, address: int) -> int:
        if self.game_version is GameVersion.STEAM:
            # Hardcoded, static memory addresses to read from/write to are for the GOG version, so need to be adjusted
            # when playing the Steam version.
            return gog_to_steam(address) + self.overall_memory_offset
        else:
            return address + self.overall_memory_offset

    def read_int(self, address: int, raw=False) -> int:
        return self._game_process.read_int(address if raw else self.adjust_gog_address(address))

    def read_uint(self, address: int, raw=False) -> int:
        return self._game_process.read_uint(address if raw else self.adjust_gog_address(address))

    def read_ushort(self, address: int, raw=False) -> int:
        return self._game_process.read_short(address if raw else self.adjust_gog_address(address))

    def read_bytes(self, address: int, length: int, raw=False) -> bytes:
        return self._game_process.read_bytes(address if raw else self.adjust_gog_address(address), length)

    def read_byte(self, address: int, raw=False) -> bytes:
        return self._game_process.read_bytes(address if raw else self.adjust_gog_address(address), 1)

    def read_float(self, address: int, raw=False) -> float:
        return self._game_process.read_float(address if raw else self.adjust_gog_address(address))

    def read_uchar(self, address: int, raw=False) -> int:
        return self._game_process.read_uchar(address if raw else self.adjust_gog_address(address))
        #return self._game_process.read_bytes(address if raw else self.adjust_gog_address(address), 1)[0]

    def write_int(self, address: int, value: int, raw=False) -> None:
        self._game_process.write_int(address if raw else self.adjust_gog_address(address), value)

    def write_uint(self, address: int, value: int, raw=False) -> None:
        self._game_process.write_uint(address if raw else self.adjust_gog_address(address), value)

    def write_ushort(self, address: int, value: int, raw=False) -> None:
        self._game_process.write_ushort(address if raw else self.adjust_gog_address(address), value)

    def write_byte(self, address: int, value: int, raw=False) -> None:
        self._game_process.write_uchar(address if raw else self.adjust_gog_address(address), value)

    def write_bytes(self, address: int, value: bytes, length: int, raw=False) -> None:
        self._game_process.write_bytes(address if raw else self.adjust_gog_address(address), value, length)

    def write_float(self, address: int, value: float, raw=False) -> None:
        self._game_process.write_float(address if raw else self.adjust_gog_address(address), value)

    def allocate(self, num_bytes: int) -> MemoryAddress:
        return self._game_process.allocate(num_bytes)

    def free(self, address: MemoryAddress) -> None:
        self._game_process.free(address)

    def write_seed_name(self, seed_name: str):
        assert not self.is_seed_name_set(), "Error: The multiworld seed name is already set into the save-data."
        CustomSaveDataSections.MULTIWORLD_SEED_NAME.write_utf8_string(self, seed_name)

    def read_seed_name_from_save_data(self) -> str | None:
        seed_name = CustomSaveDataSections.MULTIWORLD_SEED_NAME.read_utf8_string(self)
        return seed_name if seed_name else None

    def is_seed_name_set(self) -> bool:
        return not CustomSaveDataSections.MULTIWORLD_SEED_NAME.is_utf8_string_empty(self)

    def write_slot_name(self, name: str) -> None:
        # Ensure the bytes have not already been written to.
        assert not self.is_slot_name_set(), "Error: The slot name is already set into the save-data."
        CustomSaveDataSections.SLOT_NAME.write_utf8_string(self, name)

    def read_slot_name(self) -> str | None:
        """
        Read the slot name from the current save file.

        self.is_in_game() should be checked to have returned True before calling this function.

        :return: The slot name in the current save file, or None if no slot name has been written to the current save
        file.
        """
        slot_name = CustomSaveDataSections.SLOT_NAME.read_utf8_string(self)
        return slot_name if slot_name else None

    def is_slot_name_set(self) -> bool:
        """
        Return whether the current save data has a slot name set.
        """
        return not CustomSaveDataSections.SLOT_NAME.is_utf8_string_empty(self)

    def is_connected_to_server(self):
        return self.server is not None and not self.server.socket.closed

    async def update_current_p_area_data(self):
        current_p_area_data = self.current_p_area_data
        new_p_area_data = CURRENT_P_AREA_DATA_ADDRESS.get(self)
        if new_p_area_data != current_p_area_data:
            self.current_p_area_data = new_p_area_data
            await self.event_manager.fire_event_async(OnAreaChangeEvent(self, current_p_area_data, new_p_area_data))

    def update_current_level_id(self, new_level_id: int | None = None):
        if new_level_id is None:
            new_level_id = self.read_ushort(CURRENT_LEVEL_ID)

        current_level_id = self.current_level_id
        if new_level_id != current_level_id:
            # Update client state.
            self.current_level_id = new_level_id
            # Update the datastorage value in the background.
            Utils.async_start(self.send_msgs([{
                "cmd": "Set",
                "key": self._get_datastorage_key(LEVEL_ID_KEY_PREFIX),
                "want_reply": False,
                "operations": [{"operation": "replace", "value": new_level_id}]
            }]))
            self.event_manager.fire_event(OnLevelChangeEvent(self, current_level_id, new_level_id))

    # todo: A number of uses of this method should just check self.current_level_id instead, or listen to the
    #  OnLevelChangeEvent.
    def read_current_level_id(self) -> int:
        """
        Read the current level ID from memory.

        The ID of each level is determined incrementally, by the order of the levels in LEVELS/LEVELS.TXT, where the
        first level (the title screen) has ID 0 and the next level has ID 1 etc.

        :return: The current level ID.
        """
        level_id = self.read_ushort(CURRENT_LEVEL_ID)
        self.update_current_level_id(level_id)
        return level_id

    def update_current_cantina_room(self, new_cantina_room: CantinaRoom) -> None:
        current_cantina_room = self.current_cantina_room
        if new_cantina_room != current_cantina_room:
            # Update client state.
            self.current_cantina_room = new_cantina_room
            # Update the datastorage value in the background.
            Utils.async_start(self.send_msgs([{
                "cmd": "Set",
                "key": self._get_datastorage_key(CANTINA_ROOM_KEY_PREFIX),
                "want_reply": False,
                "operations": [{"operation": "replace", "value": new_cantina_room.value}]
            }]))

    def read_current_cantina_room(self) -> CantinaRoom:
        if not self.read_current_level_id() == LEVEL_ID_CANTINA:
            room = CantinaRoom.NOT_IN_CANTINA
        else:
            current_room_id = self.read_uchar(CANTINA_ROOM_ID)
            if 0 <= current_room_id <= 8:
                room = CantinaRoom(current_room_id)
            else:
                room = CantinaRoom.UNKNOWN
        self.update_current_cantina_room(room)
        return room

    def is_in_game(self) -> bool:
        # There are more than 255 levels, but far fewer than 65536, so assume 2 bytes.
        return ((process := self.game_process) is not None
                and process.read_ushort(self.adjust_gog_address(CURRENT_LEVEL_ID)) != 0)

    def get_current_save_file(self) -> int | None:
        file_number = self.read_uchar(CURRENT_SAVE_SLOT)
        if file_number == 255:
            return None
        else:
            return file_number

    def is_in_shop(self, shop_type: ShopType | None = None) -> bool:
        """Check whether the player is currently in a shop. Does not check for being in-game."""
        return (GameState1.IN_CANTINA_SHOP.is_set(self)
                and self.read_current_level_id() == LEVEL_ID_CANTINA  # Additionally check the player is in the Cantina,
                and self.read_uchar(CANTINA_ROOM_ID) == CantinaRoom.SHOP_ROOM.value  # and in the room with the shops.
                and (shop_type is None or self.read_uchar(ACTIVE_SHOP_TYPE_ADDRESS) == shop_type.value))

    def load_level(self, level: Level, reset_door: bool = False, hard_reset: bool = False):
        """

        :param level: The level to load
        :param reset_door: Reset the saved door. The saved door controls where the player spawns
        :param hard_reset: Fully reload the level, even when the player is in the level already
        :return:
        """
        if self.is_in_game():
            # Based on BrickBench, with addresses converted to Steam addresses.
            if reset_door:
                self.write_byte(0x9513d8, 0)
            if hard_reset:
                self.write_uint(0x803784, 0xFFFFFFFF)
                self.write_uint(0x93b2cc, 0x20)
            level_data_start_addr = self.read_uint(0x951b98)
            # Each level struct is 0x130 bytes. Level IDs are consecutive according to the order they are defined in
            # LEVELS.TXT.
            target_level_data_addr = level_data_start_addr + 0x130 * level.value
            self.write_uint(0x951ba0, target_level_data_addr)
            # Some sort of flag that BrickBench sets. I don't know what this does.
            self.write_uint(0x93d870, 1)

    def reload_cantina(self, hard: bool = False) -> bool:
        """
        Schedule a reload of the Cantina.

        Returns whether the reload could be scheduled.
        """
        if self.is_in_game() and self.read_current_cantina_room() == CantinaRoom.SHOP_ROOM:
            if self.is_in_shop():
                # Reloading the cantina while the shop is open gets the camera stuck in the shop, with seemingly no way
                # to fix.
                return False
            else:
                self.load_level(Level.MAP, hard_reset=hard)
                return True
        return False

    def ap_first_time_setup(self):
        # Custom Character 1 starts with a lightsaber, but the player might not have Jedi unlocked, meaning that Custom
        # Character 1 should not be allowed to use a lightsaber.
        # Custom Characters always have access to blasters, so give Custom Character 1 a Red Blaster.
        self.write_byte(CUSTOM_CHARACTER_1_WEAPON, 4)

    def _get_player_character_addr(self, player: int) -> int:
        # Note: The returned address from this function is not static for the current game instance. Whenever P1 swaps
        #  character with P2 (or P3/P4/etc. for Story mode), the value of this pointer changes to point to the other
        #  character.
        # The data at a character address includes things like the character's position vector and rotation.
        if player == 1:
            # There seems to be the same pointer value at +0x20, but Brick Bench uses 0x93d810 (GOG), so lets use that
            # one.
            # Maybe 0x93d830 can be different in some cases?
            ptr_addr = 0x93d810
        elif player == 2:
            ptr_addr = 0x93d814
        else:
            raise ValueError(f"Invalid player {player}")
        character_address = self.read_uint(ptr_addr)
        return character_address

    def _get_character_data_address(self, character_address: int) -> int:
        # Each character has a pointer to its character data, which controls how the character looks, what animations it
        # plays, and probably what abilities the character has and other static data that can be referenced by multiple
        # characters with the same character data, e.g. all the regular Battle Droids in 1-1 are separate character
        # instances, but each reference the same Battle Droid character data.
        if character_address == 0:
            # NULL pointer
            return 0
        character_data_address = CHARACTER_CHARACTER_DATA_POINTER.get(self, character_address)
        return character_data_address

    def _get_character_id(self, character_data_address) -> int | None:
        if character_data_address == 0:
            return None
        # Character ID is the first 2 bytes
        character_id = CHARACTER_DATA_ID.get(self, character_data_address)
        return character_id

    def _get_player_character_id(self, player: int) -> int | None:
        return self._get_character_id(self._get_character_data_address(self._get_player_character_addr(player)))

    async def update_player_characters(self):
        p1_character_id = self._get_player_character_id(1)
        p2_character_id = self._get_player_character_id(2)
        if p1_character_id != self.current_p1_character_id or p2_character_id != self.current_p2_character_id:
            await self.event_manager.fire_event_async(OnPlayerCharacterIdChangeEvent(
                self,
                self.current_p1_character_id,
                self.current_p2_character_id,
                p1_character_id,
                p2_character_id,
            ))
            self.current_p1_character_id = p1_character_id
            self.current_p2_character_id = p2_character_id

    def set_game_expected_idx(self, idx: int) -> None:
        """Set the expected idx into the custom save flags."""
        addr = CustomSaveFlags2.get_addr(CustomSaveFlags2.ap_last_received_index)
        assert CustomSaveFlags2.ap_last_received_index.size == 4
        self.write_uint(addr, idx)

    def get_game_expected_idx(self) -> int:
        """Retrieve the expected idx from the custom save flags."""
        addr = CustomSaveFlags2.get_addr(CustomSaveFlags2.ap_last_received_index)
        assert CustomSaveFlags2.ap_last_received_index.size == 4
        return self.read_uint(addr)

    def give_item(self, code: int) -> bool:
        if code in STUDS_AP_ID_TO_VALUE:
            # Studs are directly given to the player as they are received, so it is necessary to check that the player
            # is currently in-game.
            if not self.is_in_game():
                return False
            give_studs_item(self, code)
        elif code in self.power_up_receiver.receivable_ap_ids:
            # Power Ups are directly given to the player as they are received, with a buffer of extra Power Ups kept
            # only in the current client session.
            if not self.is_in_game():
                return False
            self.power_up_receiver.give_power_up()
        else:
            self.receive_item(code)
        return True

    def receive_item(self, code: int):
        from .. import LegoStarWarsTCSWorld
        item_name = LegoStarWarsTCSWorld.item_id_to_name.get(code, f"Unknown {code}")
        debug_logger.info(f"Receiving item {item_name} from AP")
        if code in self.acquired_generic.receivable_ap_ids:
            self.acquired_generic.receive_generic(self, code)
        elif code in self.acquired_minikits.receivable_ap_ids:
            self.acquired_minikits.receive_minikit(self, code)
        elif code in self.acquired_characters.receivable_ap_ids:
            self.acquired_characters.receive_character(code)
            self.unlocked_chapter_manager.on_character_or_chapter_or_episode_unlocked(self, code)
        elif code in self.acquired_extras.receivable_ap_ids:
            self.acquired_extras.receive_extra(code)
        elif code in STUDS_AP_ID_TO_VALUE or code in self.power_up_receiver.receivable_ap_ids:
            # The client may be resetting its state after a save data rollback or after connecting to an existing seed.
            pass
        else:
            logger.warning(f"Received unknown item with AP ID {code}")

    def _reset_non_permanent_components(self):
        self.acquired_extras = AcquiredExtras()
        self.acquired_characters = AcquiredCharacters()
        self.acquired_generic = AcquiredGeneric()
        self.acquired_minikits = AcquiredMinikits()

        self.unlocked_chapter_manager = UnlockedChapterManager()
        self.client_expected_idx = 0
        self.current_level_id = 0
        self.current_p_area_data = 0
        self.current_cantina_room = CantinaRoom.UNKNOWN

        self.free_play_completion_checker = FreePlayAreaCompletionChecker()
        self.true_jedi_and_power_brick_and_minikit_brick_checker = TrueJediAndPowerBrickAndMinikitBrickChecker()
        self.minikit_checker = MinikitChecker()
        self.purchased_extras_checker = PurchasedExtrasChecker()
        self.purchased_characters_checker = PurchasedCharactersChecker()
        self.bonus_area_completion_checker = BonusAreaCompletionChecker()
        self.ridesanity_checker = RidesanityChecker()

        self.goal_manager = GoalManager()
        self.power_up_receiver = PowerUpReceiver()

        self.shop_names_replacer = ShopNamesReplacer()
        self.auto_collect_pickups = AutoCollectPickups()

        self.death_link_manager = DeathLinkManager()

    def reset_persisted_client_data(self):
        """
        Reset all client state.

        Used when deliberately disconnecting from a server.
        """
        self.finished_game = False
        self.locations_checked.clear()
        # Event manager must be set before other attributes, so that the event manager can look for methods that are
        # subscribing to events on the other attributes.
        self.event_manager = EventManager()
        # Some of the components are permanent, so need to be manually subscribed to the new EventManager.
        for client_component in self.permanent_components:
            self.event_manager.subscribe_events(client_component)

        self.shop_names_replacer.reset_persisted_client_data(self)
        self._reset_non_permanent_components()


    def reset_client_received_items(self):
        """
        Reset the items that the client thinks it has received.

        Use in cases where the client save data has rolled back.
        """
        self.acquired_extras.clear_received_items()
        self.acquired_characters.clear_received_items()
        self.acquired_generic.clear_received_items()
        self.acquired_minikits.clear_received_items()
        self.power_up_receiver.clear_received_items()

        self.client_expected_idx = 0


async def give_items(ctx: LegoStarWarsTheCompleteSagaContext):
    if ctx.is_in_game():
        # The player can enter a save file, receive items, and then exit back to the main menu without saving,
        # and then load their save file again, reverting their expected_idx to an older value and undoing any studs that
        # were given.
        # To ensure that given studs take into account the player's score multiplier at the time the studs were given,
        # it is necessary to reset all received items on the client side in this case.
        expected_idx_game = ctx.get_game_expected_idx()
        expected_idx_client = ctx.client_expected_idx

        received_items = ctx.items_received

        # Check if the game rolled back its save data, the client needs to reset its items and catch back up to the
        # game.
        if expected_idx_game < ctx.client_expected_idx:
            debug_logger.info("Resetting client received items due to game save data rollback")
            ctx.reset_client_received_items()
            for idx, item in enumerate(received_items[:expected_idx_game]):
                ctx.receive_item(item.item)
                ctx.client_expected_idx = idx + 1
            assert ctx.client_expected_idx == min(expected_idx_game, len(received_items))
        # Check if the player is resuming a seed where the client is fresh and needs to be caught up to the game.
        elif expected_idx_client < expected_idx_game:
            # The client may not have yet connected to the server and received the items to be able to catch up yet, so
            # don't spam the debug log.
            if len(received_items) > expected_idx_client:
                debug_logger.info("Catching up client to game state. Client expected: %i. Game expected: %i.",
                                  ctx.client_expected_idx, expected_idx_game)
                for idx, item in enumerate(received_items[expected_idx_client:expected_idx_game],
                                           start=expected_idx_client):
                    ctx.receive_item(item.item)
                    ctx.client_expected_idx = idx + 1
                # If `expected_idx_client` is to be used beyond this point, it needs to be updated.
                # expected_idx_client = ctx.client_expected_idx
                assert ctx.client_expected_idx == min(expected_idx_game, len(received_items))

        # Check if there are new items.
        if len(received_items) <= expected_idx_game:
            # There are no new items.
            return

        # Loop through items to give.
        # Give the player all items at an index greater than or equal to the expected index.
        for idx, item in enumerate(received_items[expected_idx_game:], start=expected_idx_game):
            while not ctx.give_item(item.item):
                await asyncio.sleep(0.01)

            # Increment the expected index.
            ctx.set_game_expected_idx(idx + 1)
            ctx.client_expected_idx = idx + 1


async def game_watcher_check_save_file(ctx: LegoStarWarsTheCompleteSagaContext,
                                       only_just_loaded_into_game: bool) -> bool:
    """
    Check for changes to the current save file.

    If the player loads a different save file, the client data needs to be reset and reloaded onto the new save file.

    Except, this is not necessary if the player has gone from no save file (starting a new game), to creating a save
    file.

    If the player loads a save file for a different multiworld or slot, they need to be disconnected from the current
    multiworld.

    No save file -> save file:    OK
    Save file -> no save file:    Reset client state and reload onto the new game that has yet to save
    Save file -> other save file: Reset client state and disconnect if the other save is for a different
                                  multiworld/slot.
    :param ctx:
    :param only_just_loaded_into_game: Indicates whether the game was previously in the main menu or not connected, but
    has just loaded into a save file or new game.
    :return:
    """
    current_save_file = ctx.get_current_save_file()

    if ctx.last_connected_slot is None and ctx.last_connected_seed_name is None:
        # The player has made no connection to a server, so there is nothing to check against.
        # The player could have started a new game or loaded an existing save file.
        pass
    else:
        # If the player loads a different save file, re-check the multiworld seed and slot name and reset
        # persistent client data if either the seed or slot name differ.
        last_save_file = ctx.last_loaded_save_file
        if (current_save_file != last_save_file
                or (only_just_loaded_into_game and current_save_file is None and last_save_file is None)):
            last_slot_name = ctx.last_connected_slot
            last_seed_name = ctx.last_connected_seed_name

            # The player is allowed to exit to the main menu and start a new game.
            if current_save_file is None:
                if last_slot_name is not None and ctx.read_slot_name() is None:
                    logger.info("Copied the last connected slot name to the new save file.")
                    ctx.write_slot_name(last_slot_name)
                if last_seed_name is not None and ctx.read_seed_name_from_save_data() is None:
                    logger.info("Copied the last connected multiworld seed name to the new save file.")
                    ctx.write_seed_name(last_seed_name)
                # The save file is new, so run first-time setup.
                ctx.ap_first_time_setup()
            else:
                # The player *could* have another save file with the same seed and slot, which would be
                # unusual, but acceptable.
                # But if the player tries to load into a save file for a different seed/slot, then they need
                # to be disconnected.
                if (last_seed_name is not None
                        and last_seed_name != ctx.read_seed_name_from_save_data()):
                    if ctx.slot:
                        logger.info("Disconnecting from the server because the newly loaded save file's"
                                    " seed does not match the connected multiworld's seed.")
                    await ctx.disconnect()
                    return False
                elif last_slot_name is not None and last_slot_name != ctx.read_slot_name():
                    if ctx.slot:
                        logger.info("Disconnecting from the server because the newly loaded save file's"
                                    " slot name does not match the connected slot.")
                    await ctx.disconnect()
                    return False
        elif current_save_file is not None and only_just_loaded_into_game:
            # The player can start a new game, progress it before connecting to the server (they shouldn't do this
            # because the client won't be running fully at that point), causing it to save to a save slot. Then the
            # player could connect to the server (writing the seed hash and slot name into the save data), but then
            # return to the main menu, reverting the save data to before the seed hash and slot name were written. If
            # the player then loads the save file again, they can end up connected to the server while not having the
            # slot name and seed name hash written into their save file.
            slot_name = ctx.last_connected_slot
            seed_name = ctx.last_connected_seed_name
            if slot_name is not None and seed_name is not None:
                if not ctx.is_slot_name_set():
                    ctx.write_slot_name(slot_name)
                    logger.info("Restored slot name in save data after save data was rolled back to before it was set")
                if not ctx.is_seed_name_set():
                    ctx.write_seed_name(seed_name)
                    logger.info("Restored seed name hash in save data after save data was rolled back to before it was"
                                " set")
    ctx.last_loaded_save_file = current_save_file
    return True


async def game_watcher(ctx: LegoStarWarsTheCompleteSagaContext):
    logger.info("Starting connection to game.")
    last_message = ""
    # Used to track if the player was loaded into a save/new game in the previous loop.
    previously_not_in_game = True

    def log_message(msg: str, always_log=False):
        nonlocal last_message
        if always_log or msg != last_message:
            logger.info(msg)
            last_message = msg

    sleep_time = 0.0
    in_game_watcher_tick_count = 0
    while not ctx.exit_event.is_set():
        if sleep_time > 0.0:
            try:
                await asyncio.wait_for(ctx.watcher_event.wait(), sleep_time)
            except asyncio.TimeoutError:
                pass
            sleep_time = 0.0
        ctx.watcher_event.clear()

        try:
            game_process = ctx.game_process
            if game_process is None:
                previously_not_in_game = True
                if not await ctx.open_game_process():
                    log_message("Connection to game failed, attempting again in 5 seconds...", True)
                    sleep_time = 5
                else:
                    # No wait, start processing items/locations/etc. immediately if the client is connected to the
                    # server.
                    pass
            else:
                if not ctx.is_in_game():
                    in_game_watcher_tick_count = 0
                    previously_not_in_game = True
                    # Need to wait for the player to load into a save file.
                    if (ctx.last_loaded_save_file is not None
                            or ctx.last_connected_seed_name is not None
                            or ctx.last_connected_slot is not None):
                        # There is a previously loaded save file or connected seed/slot, so the player has exited to the
                        # main menu.
                        last_connected_slot_name = ctx.last_connected_slot
                        if last_connected_slot_name is not None:
                            log_message(f"Load back into the save file, or a new game, to continue as"
                                        f" {last_connected_slot_name}.")
                        else:
                            log_message("Load back into a save file or a new game to continue.")
                    else:
                        # There is no previously loaded save file or seed/slot, so the player has just started the game.
                        log_message("Load into a save file or start a new game to continue.")
                    sleep_time = 1.0
                    await ctx.event_manager.fire_event_async(OnGameWatcherDisconnectedTickEvent(ctx))
                    continue

                # The save file check does some extra checks if the player was previously not loaded into a save
                # file/new game, but now is.
                only_just_loaded_into_game = previously_not_in_game
                previously_not_in_game = False

                if not await game_watcher_check_save_file(ctx, only_just_loaded_into_game):
                    # The player changed save file to a save file for a different multiworld or slot.
                    # A message will already have been logged.
                    sleep_time = 1.0
                    continue

                if ctx.last_connected_slot is None or ctx.last_connected_seed_name is None:
                    sleep_time = 1.0
                    if ctx.server is not None and not ctx.server.socket.closed:
                        if ctx.auth_status == AuthStatus.NOT_AUTHENTICATED:
                            await ctx.server_auth(ctx.password_requested)
                        else:
                            # Most likely waiting for the player to enter their slot name.
                            pass
                    else:
                        ctx.auth_status = AuthStatus.NOT_AUTHENTICATED
                        log_message("Connect to a server to continue")
                    await ctx.event_manager.fire_event_async(OnGameWatcherDisconnectedTickEvent(ctx))
                    continue

                # Even if the client has disconnected from the server, it is still important to run a number of
                # coroutines to allow the player to play while disconnected.
                # todo: Is the `is_in_game()` check here still necessary now that there is an earlier check?
                if ctx.is_in_game():
                    # Ensure that the OnLevelChangeEvent gets fired consistently, by updating the current level ID on
                    # each game watcher tick.
                    ctx.update_current_level_id()

                    await give_items(ctx)

                    # Check for changes to the current AreaData pointer, firing an event if it changes.
                    await ctx.update_current_p_area_data()

                    # todo: Firing this event should just be fired by something (ctx?) listening to the Tick event.
                    # Fire OnPlayerCharacterIdChangeEvent if player characters have changed.
                    await ctx.update_player_characters()
                    # Fire Tick event for all ClientComponents subscribed to the event.
                    await ctx.event_manager.fire_event_async(OnGameWatcherTickEvent(ctx, in_game_watcher_tick_count))

                    # Only queue the message if everything else worked so far.
                    msg = "The client is now fully connected to the game, receiving items and checking locations."
                    if last_message != msg:
                        log_message(msg)
                        slot_name = ctx.read_slot_name()
                        if not ctx.is_connected_to_server():
                            # A previous connection must have been made, but the server connection has been lost
                            # unintentionally (it will attempt to auto-reconnect).
                            # todo: Make these messages display for longer somehow (extra argument to queue_message?).
                            ctx.text_display.queue_message(f"Client running in disconnected mode as {slot_name}")
                            ctx.text_display.queue_message(f"Items and checks will be synced once the server connection"
                                                           f" is reestablished")
                        else:
                            ctx.text_display.queue_message(f"Client running and connected as {slot_name}")

                    # Check for newly cleared locations while connected to a slot on a server.
                    # todo: Some of these don't need to be checked very often because they are persisted in the save
                    #  file.
                    if ctx.slot:
                        new_location_checks: list[int] = []
                        # Free play completion needs to be checked often (need to ensure that players cannot click
                        # through the status screen faster than we're polling the game to check for free play!)
                        await ctx.free_play_completion_checker.check_completion(ctx, new_location_checks)

                        # True Jedi and Minikit gold brick in the save data do not need to be checked often.
                        if in_game_watcher_tick_count % 20 == 0:
                            await ctx.true_jedi_and_power_brick_and_minikit_brick_checker.check_save_data(
                                ctx, new_location_checks)
                        if in_game_watcher_tick_count % 10 == 1:
                            await ctx.true_jedi_and_power_brick_and_minikit_brick_checker.check_current_area(
                                ctx, new_location_checks)

                        # The Minikit checker needs to check frequently for in-area minikits, but handles this itself.
                        # The checked minikits are stored, so the minikit checker does not need to be as frequently
                        # polled for locations to send, but still wants to be fairly responsive.
                        if in_game_watcher_tick_count % 5 == 2:
                            await ctx.minikit_checker.check_minikits(ctx, new_location_checks)

                        # Purchases do not need to be checked often.
                        if in_game_watcher_tick_count % 10 == 3:
                            await ctx.purchased_extras_checker.check_extra_purchases(ctx, new_location_checks)
                            await ctx.purchased_characters_checker.check_extra_purchases(ctx, new_location_checks)

                        # Bonus level completion is read from the save data, so does not need to be checked often.
                        if in_game_watcher_tick_count % 20 == 4:
                            await ctx.bonus_area_completion_checker.check_completion(ctx, new_location_checks)

                        # New Ridesanity checks are prepared to be sent by other event callbacks, so Ridesanity is cheap
                        # to check for new locations.
                        if in_game_watcher_tick_count % 10 == 5:
                            await ctx.ridesanity_checker.check_ridesanity(ctx, new_location_checks)

                        # Send newly cleared locations to the server, if there are any.
                        actually_new_location_checks = await ctx.check_locations(new_location_checks)
                        ctx.locations_checked.update(actually_new_location_checks)

                        # Check for goal completion.
                        if not ctx.finished_game:
                            if ctx.goal_manager.is_goal_complete(ctx):
                                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                                ctx.finished_game = True

                    in_game_watcher_tick_count += 1
                sleep_time = 0.1
        except Exception as e:
            await ctx.unhook_game_process()
            ctx.reset_persisted_client_data()
            if isinstance(e, (PymemError, WinAPIError)):
                msg = f"Lost connection to game, attempting re-connection in 5 seconds..."
                logger.error(traceback.format_exc())
            else:
                msg = "Unexpected error occurred, attempting re-connection to game in 5 seconds..."
                logger.error(traceback.format_exc())
            logger.info(msg)
            last_message = msg
            await ctx.disconnect()
            sleep_time = 5
            continue

        # This is reached when there is no game process to connect to, allowing a server connection to be made, without
        # actually connecting to a slot.
        if ctx.server is not None and not ctx.server.socket.closed:
            if ctx.auth_status == AuthStatus.NOT_AUTHENTICATED:
                Utils.async_start(ctx.server_auth(ctx.password_requested))
        else:
            ctx.auth_status = AuthStatus.NOT_AUTHENTICATED


async def main(*launch_args: str):
    Utils.init_logging("LegoStarWarsTheCompleteSagaClient", exception_logger="ClientException")

    parser = get_base_parser()
    args = parser.parse_args(launch_args)

    ctx = LegoStarWarsTheCompleteSagaContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if UNIVERSAL_TRACKER_LOADED:
        # noinspection PyUnresolvedReferences
        ctx.run_generator()

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    game_watcher_task = asyncio.create_task(game_watcher(ctx), name="LegoStarWarsTheCompleteSagaGameWatcher")

    await ctx.exit_event.wait()
    # Wake the game watcher task, if it is currently sleeping, so it can start shutting down when it sees that the
    # exit_event is set.
    ctx.watcher_event.set()
    ctx.server_address = None

    try:
        await game_watcher_task
    except Exception as e:
        logger.exception(e)
    await ctx.shutdown()


def launch(*launch_args: str):
    colorama.just_fix_windows_console()
    asyncio.run(main(*launch_args))
    colorama.deinit()
