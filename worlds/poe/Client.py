import asyncio
import logging
import os
import traceback
import typing
from random import Random
from typing import TYPE_CHECKING
from dataclasses import dataclass
    

import colorama
import Utils
from CommonClient import ClientCommandProcessor, CommonContext, server_loop, gui_enabled
from pathlib import Path

from worlds.poe import Items

from .poeClient.fileHelper import load_settings, save_settings, find_possible_client_txt_path
from .poeClient import main as poe_main
from .poeClient import gggAPI
from .poeClient import textUpdate
from .poeClient import itemFilter
from . import Options
from .Version import POE_VERSION, BACKWARDS_COMPATIBLE_VERSIONS

class PathOfExileCommandProcessor(ClientCommandProcessor):
    if TYPE_CHECKING:
        ctx: "PathOfExileContext"
    logger = logging.getLogger("poeClient.PathOfExileCommandProcessor")

    def _cmd_loot_filter_sounds(self, sounds: str = "") -> bool:
        """Set the lootfilter drop sound. no_sound = 0; TTS = 1; jingles = 2"""
        int_mapping = {0: "no_sound", 1: "TTS", 2: "jingles"}
        if sounds not in {"0", "1", "2"}:
            self.output(f"To set, please provide a valid sounds configuration (0, 1, 2).\nCurrent setting is: {int_mapping.get(self.ctx.filter_options.loot_filter_sounds, 'unknown')}")
            return False
        self.ctx.filter_options.loot_filter_sounds = int(sounds)
        self.ctx.update_settings()
        sound_string = int_mapping.get(int(sounds), "unknown")
        self.output(f"Loot filter drop sounds set to: {sound_string}")
        return True
    
    def _cmd_loot_filter_display(self, display: str = "") -> bool:
        """Set the lootfilter display mode. show_classification = 0; hide_classification = 1; randomize_lootfilter_style = 2"""
        int_mapping = {0: "show_classification", 1: "hide_classification", 2: "randomize_lootfilter_style"}
        if display not in {"0", "1", "2"}:
            self.output(f"To set, please provide a valid display configuration (0, 1, 2).\nCurrent setting is: {int_mapping.get(self.ctx.filter_options.loot_filter_display, 'unknown')}")
            return False
        self.ctx.filter_options.loot_filter_display = int(display)
        self.ctx.update_settings()
        display_string = int_mapping.get(int(display), "unknown")
        self.output(f"Loot filter display mode set to: {display_string}")
        return True

    def _cmd_enable_tts(self, enable: bool | str | None = None) -> bool:
        """Enable or disable TTS generation."""
        if enable is None:
            tts_enabled_implied = not self.ctx.filter_options.tts_enabled
            self.output(f"Turning TTS {'on' if tts_enabled_implied else 'off'}")
            enable = tts_enabled_implied
        if isinstance(enable, str):
            lowered = enable.lower()
            if lowered in {"true", "1", "yes", "y", "on"}:
                enable_bool = True
            elif lowered in {"false", "0", "no", "n", "off"}:
                enable_bool = False
            else:
                self.output("ERROR: Please provide a valid boolean value for enabling TTS (True/False).")
                return False
        elif isinstance(enable, bool):
            enable_bool = enable
        else:
            self.output("ERROR: Please provide a valid boolean value for enabling TTS (True/False).")
            return False

        self.ctx.filter_options.tts_enabled = enable_bool
        self.ctx.update_settings()
        if enable_bool:
            self.output("TTS generation enabled.")
        else:
            self.output("TTS generation disabled.")
        return True

    def _cmd_tts_speed(self, speed: int) -> bool:  # actually receives a string from the CLI
        """Set the speed of TTS generation."""
        try:
            speed = int(speed)
        except (TypeError, ValueError):
            self.output("ERROR: Please provide a valid positive integer for TTS speed.")
            return False
        if speed <= 0:
            self.output("ERROR: Please provide a valid positive integer for TTS speed.")
            return False
        self.ctx.filter_options.tts_speed = speed
        self.ctx.update_settings()
        self.output(f"TTS speed set to {speed} words per minute.")
        return True

    reset_poe_doc_path = False
    def _cmd_poe_documents_directory(self, path:str|None = None) -> bool:
        r"""Change the default directory for poe item filters, this may be needed if running on linux.
        Path of exile only looks for item filters at C:\Users\<USER>\Documents\My Games\Path of Exile."""
        filter_path = None

        if not path:
            if self.reset_poe_doc_path:
                filter_path = itemFilter.DEFAULT_POE_DOC_PATH
                self.output(f"Setting to default path: {str(filter_path)}")
            else:
                self.output("The current directory for poe item filters is:")
                self.output(f"  {itemFilter.poe_doc_path}")
                self.output("Run this command again to set it to the default directory.")
                self.reset_poe_doc_path = True
            return False
        self.reset_poe_doc_path = False
        filter_path = Path(path)
        if not filter_path.exists():
            self.output(f"ERROR: The provided path does not exist: {path}")
            return False
        if not filter_path.is_dir():
            self.output(f"ERROR: The provided path is not a directory: {path}")
            return False
        itemFilter.set_poe_doc_path(filter_path)
        self.ctx.poe_doc_path = str(filter_path)
        self.ctx.update_settings()
        self.logger.debug(f"[DEBUG] Set poe documents directory to: {filter_path}")
        return True

    def _cmd_generate_tts(self) -> bool:
        """Generate TTS for missing locations. Run this after connecting to the server."""
        from .poeClient import tts

        if not self.ctx.missing_locations:
            self.output("No missing locations to generate TTS for, are you connected to the server?")
            return False
        if not self.ctx.filter_options.tts_enabled:
            self.output("TTS is disabled, please enable it using '/enable_tts' to generate TTS.")
            return False
        tts.generate_tts_tasks_from_missing_locations(self.ctx)
        tts.run_tts_tasks()
        return True

    def _cmd_whisper_updates(self, enable: bool | str | None = None) -> bool:
        """Enable or disable whispering item updates to the in game chat."""
        if enable is None:
            whisper_enabled_implied = not self.ctx.game_options.get("whisper_updates", False)
            self.output(f"Turning whisper updates {'on' if whisper_enabled_implied else 'off'}")
            enable = whisper_enabled_implied
        if isinstance(enable, str):
            lowered = enable.lower()
            if lowered in {"true", "1", "yes", "y", "on"}:
                enable_bool = True
            elif lowered in {"false", "0", "no", "n", "off"}:
                enable_bool = False
            else:
                self.output("ERROR: Please provide a valid boolean value for enabling whisper updates (True/False).")
                return False
        elif isinstance(enable, bool):
            enable_bool = enable
        else:
            self.output("ERROR: Please provide a valid boolean value for enabling whisper updates (True/False).")
            return False

        self.ctx.game_options["whisper_updates"] = enable_bool
        self.ctx.whisper_updates_enabled = enable_bool
        self.ctx.update_settings()

        if enable_bool:
            self.output("Whisper updates enabled.")
        else:
            self.output("Whisper updates disabled.")
        return True


    def _cmd_poe_auth(self) -> bool:
        """Authenticate with Path of Exile's OAuth2 service."""
        from .poeClient import gggOAuth
        from urllib.parse import urlparse

        raw = getattr(self.ctx, "server_address", "") or ""
        try:
            parsed = urlparse(raw if "://" in raw else f"ws://{raw}")
            host = parsed.hostname or ""
            port = parsed.port
            server = f"{host}:{port}" if port else host
        except Exception:
            server = raw

        gggOAuth.slot_info = {
            "server":   server,
            "slot":     getattr(self.ctx, "auth",     "") or "",
            "password": getattr(self.ctx, "password", "") or "",
        }

        def on_complete(task):
            try:
                task.result()  # Will raise if auth failed
                self.output("Authentication successful!")
            except Exception as e:
                self.output(f"Authentication failed: {e}")

        task = asyncio.create_task(gggAPI.request_new_access_token())
        task.add_done_callback(on_complete)
        self.output("Authentication started...")
        return True

    def _cmd_set_client_text_path(self, path: str = "") -> bool:
        """Set the path to the Path of Exile client text file."""
        if not path:
            self.output("ERROR: Please provide a valid path to the client text file.")
            return False
        client_path = Path(path)
        if not client_path.exists():
            self.output(f"ERROR: The provided path does not exist: {path}")
            return False
        if not client_path.is_file():
            if client_path.is_dir():
                self.output(f"The provided path is a dir: {path}, looking for a file with the name 'Client.txt' in the directory.")
                client_path = client_path / "Client.txt"
                if not client_path.exists() or not client_path.is_file():
                    self.output(f"ERROR: The file 'Client.txt' does not exist in the provided directory: {path}")
                    return False
            else:
                self.output(f"ERROR: The provided path is not a file, or a directory but it... exists? no idea what you are doing here: {path}")
                return False


        self.ctx.client_text_path = client_path
        poe_main.path_to_client_txt = self.ctx.client_text_path
        self.ctx.update_settings()
        self.output(f"Client text path set to: {client_path}")
        return True

    def _cmd_char_name(self, character_name: str = "") -> bool:
        """Set the character name for the Path of Exile client."""
        if not character_name:
            self.output("ERROR: Please provide a character name.")
            return False
        self.ctx.character_name = character_name
        self.ctx.update_settings()
        self.output(f"Character name set to: {character_name}")
        return True

    def _cmd_base_item_filter(self, filter_name: str = "") -> bool:
        """Set the base item filter. (this needs to be a local file, and remember to add the .filter extension)"""
        filter_name = Path(filter_name).name
        if not filter_name:
            self.output(f"Please provide a valid item filter name. The current item filter is: {self.ctx.base_item_filter or 'None'}")
            return False
        if not filter_name.endswith(".filter"):
            filter_name += ".filter"
            self.output(f"adding .filter extension to the filter name: {filter_name}")

        if filter_name == f"{itemFilter.AP_FILTER_NAME}.filter" or filter_name == f"{itemFilter.INVALID_FILTER_NAME}.filter":
            self.output(f"ERROR: The filter name '{filter_name}' is reserved, please choose a different name.")
            return False

        self.ctx.base_item_filter = filter_name
        self.ctx.update_settings()  # Save the settings
        self.output(f"Base item filter set to: {filter_name}")
        return True

    def _cmd_start_poe(self) -> bool:
        """Start the Path of Exile client."""
        #required
        self.logger.info(f"Path of Exile apworld version: {POE_VERSION}")
        self.output(f"Path of Exile apworld version: {POE_VERSION}")

        if not self.ctx.slot_data:
            self.output(f"_________________________________________________________________________________\n"
                        f"Connect to a multiworld server before starting the Path of Exile client!\n"
                        f"Use either the GUI or the '/connect' command to connect.\n"
                        f"_________________________________________________________________________________")
            return False

        if not self.ctx.client_text_path:
            possible_path = find_possible_client_txt_path()
            if possible_path:
                self.ctx.client_text_path = possible_path
                self.output(f"_________________________________________________________________________________\n"
                            f"Using a possible client text path located here: {self.ctx.client_text_path},\n "
                            f"THIS MAY NOT BE THE CORRECT PATH, please verify it is correct, and change it if wrong "
                            f"using the 'set_client_text_path <path>' command.\n"
                            f"_________________________________________________________________________________")
            else:
                self.output("Please set the client text path using the 'set_client_text_path <path>' command.")
                return False
        
        #optional to start
        if not self.ctx.character_name:
            self.output("Please set your character name using when in game typing '!ap char', or by using the 'poe_char_name <name> command'.")
        if not self.ctx.base_item_filter:
            self.output("If you would like to use a custom item filter, please set the base item filter using the 'poe_base_item_filter <filter_name>' command.")

        self.output(f"Starting Path of Exile client for character: {self.ctx.character_name}")
        if self.ctx.running_task and not self.ctx.running_task.done():
            self.output("Path of Exile client is already running... Killing it and starting a new one.")
            self.ctx.running_task.cancel()
            return False
        self.ctx.running_task = asyncio.create_task(poe_main.client_start(self.ctx), name="main_async_task")
        self.ctx.running_task.add_done_callback(lambda task: handle_task_errors(task, self.ctx, self))

        return True

    def _cmd_client(self, path: str = "") -> bool:
        """Shortcut for setting the client text path."""
        return self._cmd_set_client_text_path(path)

    def _cmd_char(self, character_name: str = "") -> bool:
        """Shortcut for setting the character name. (can also be done by typing '@<charname> !ap char' into the in game chat)"""
        return self._cmd_char_name(character_name)


    def _cmd_filter(self, filter_name: str = "") -> bool:
        """Shortcut for setting the base item filter."""
        return self._cmd_base_item_filter(filter_name)

    def _cmd_start(self) -> bool:
        """Shortcut for starting the Path of Exile client."""
        return self._cmd_start_poe()

    def _cmd_stop(self) -> bool:
        """Stop the Path of Exile client."""
        if self.ctx.running_task:
            if not self.ctx.running_task.done():
                self.output("Stopping Path of Exile client...")
                self.ctx.running_task.cancel()
                self.output("Path of Exile client stopped.")
                return True
            else:
                self.output("Path of Exile client was already stopped.")
        else:
            self.output("Path of Exile client is not running.")
            return False
    
    def _cmd_deathlink(self):
        """Toggles deathlink"""
        def on_complete(task):
            self.output(f"Death link mode {'enabled' if self.ctx.get_is_death_linked() else 'disabled'}.")
        asyncio.create_task(self.ctx.update_death_link(not self.ctx.get_is_death_linked())).add_done_callback(on_complete)

def handle_task_errors(task: asyncio.Task, ctx: "PathOfExileContext", cmdprocessor: PathOfExileCommandProcessor):
    """Handle errors in the task."""
    try:
         task.result()  # Will raise if the task failed
    except Exception as e:
        cmdprocessor.output(f"ERROR, the client borked: {e}")

        logger = logging.getLogger("poeClient.PathOfExileContext")
        logger.setLevel(logging.DEBUG)
        tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        logger.error(f"Error: {e}\nTraceback:\n{tb_str}")
        logger.error(f"Task failed with error: {e}")

        ctx.running_task = None

        cmdprocessor.output(f"Trying to restart the client...")
        cmdprocessor._cmd_start_poe()

@dataclass
class FilterOptions:
    """Options for Text-to-Speech (TTS) generation."""
    tts_speed: int = 250  # Default TTS speed in words per minute
    tts_enabled: bool = False  # Default TTS enabled state
    loot_filter_display: int = 0  #    option_show_classification = 0    option_hide_classification = 1    option_randomize_lootfilter_style = 2
    loot_filter_sounds: int = 0  #    option_no_sound = 0    option_TTS = 1    option_jingles = 2
    #    sfx_enabled: bool = True  # Whether to play random sound effects for item pickups (trap)
    
class PathOfExileContext(CommonContext):
    # THESE ARE ALL STATIC.
    # but I guess that's ok, because we only have one client per game.

    game = "Path of Exile"
    command_processor = PathOfExileCommandProcessor
    items_handling = 0b111
    
    last_response_from_api = {}
    last_entered_zone = ""
    last_character_level: int = 1

    passives_used: int = 0
    passives_available: int = 0

    previously_received_item_ids: list[int] = []
    character_name: str = ""
    client_text_path: Path = ""
    base_item_filter: str = ""
    poe_doc_path: str = ""
    generated_version: str = ""
    whisper_updates_enabled: bool = True
    loaded_client_settings: bool = False
    text_to_send: list[tuple[str, bool]] = [] # list of (message, prepend_char_name) tuples to send to in-game chat
    slot_data = {}
    game_options = {}
    client_options = {}

    running_task : asyncio.Task | None = None

    filter_options = FilterOptions()

    _debug = True  # Enable debug mode for poe client

    logger = logging.getLogger("poeClient.PathOfExileContext")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_is_death_linked(self) -> bool:
        """Check if the client is in death link mode."""
        return "DeathLink" in self.tags

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game="Path of Exile")

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        self.command_processor.output(self=self, text=f"Death link event received from {data.get('source', 'unknown')}")
        if self.get_is_death_linked():
            asyncio.create_task(textUpdate.receive_deathlink(self)).add_done_callback(lambda task: handle_task_errors(task, self, self.command_processor))

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)

        if cmd == 'Connected':
            self.slot_data = args.get('slot_data', {})
            self.game_options = self.slot_data.get('game_options', {})
            self.client_options = self.slot_data.get('client_options', {})
            self.generated_version = self.slot_data.get('generated_version', 'unknown')

            if self.generated_version != POE_VERSION:
                if self.generated_version in BACKWARDS_COMPATIBLE_VERSIONS:
                    log = (f"Connected to a multiworld generated with a different version: {self.generated_version}, "+
                           f"running version {POE_VERSION}. This is marked as backwards compatible, and should be OK.")
                    self.logger.info(log)
                    self.command_processor.output(self=self.command_processor, text=log)
                else:
                    log = (f"_________________________________________________________________________________\n"+
                           f"Server generated with unsupported version!\n"+
                           f"Server:{self.generated_version}\n"+
                           f"Client:{POE_VERSION}\n"+
                           f"This may cause issues!!!\n"+
                           f"_________________________________________________________________________________")
                    self.logger.warning(log)
                    self.command_processor.output(self=self.command_processor, text=log)

            if self.game_options.get("deathlink", False):
                asyncio.create_task(self.update_death_link(True)).add_done_callback(
                    lambda task: self.command_processor.output(self=self, text=f"Death link mode {'enabled' if self.get_is_death_linked() else 'disabled'}."))

            # Request info for all locations after connecting
            location_ids = list(self.missing_locations)

            asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts", "locations": location_ids}]))

        if cmd == 'RoomInfo':
            def injest_load_client_settings(task):
                logger = logging.getLogger("poeClient.PathOfExileContext.injest_load_client_settings")
                try:
                    settings = task.result()
                    if settings:
                        # if there are local settings, use those first -- otherwise use server settings -- otherwise use defaults.
                        tts_settings = settings.get("tts_enabled") # can be True, False, or None
                        self.filter_options.tts_enabled = tts_settings if isinstance(tts_settings, bool) else bool(self.client_options.get('ttsEnabled', False))
                        self.filter_options.loot_filter_sounds = settings.get("loot_filter_sounds") or int(self.client_options.get('lootFilterSounds')) or Options.LootFilterSounds.default
                        self.filter_options.loot_filter_display = settings.get("loot_filter_display") or int(self.client_options.get('lootFilterDisplay')) or  Options.LootFilterDisplay.default
                        self.filter_options.tts_speed = settings.get("tts_speed", int(self.client_options.get('ttsSpeed', 250)))
                        self.client_text_path = settings.get("client_txt", self.client_text_path)
                        self.character_name = settings.get("last_char", self.character_name)
                        self.base_item_filter = settings.get("base_item_filter", self.base_item_filter)
                        self.poe_doc_path = settings.get("poe_doc_path", self.poe_doc_path)
                        self.whisper_updates_enabled = settings.get("whisper_updates", True)
                        self.previously_received_item_ids = settings.get("already_received_items", [])
                        self.loaded_client_settings = True
                        logger.debug(f"[DEBUG] Loaded settings: {settings}")
                    if self.poe_doc_path:
                        itemFilter.set_poe_doc_path(self.poe_doc_path)
                except Exception as e:
                    logger.info(f"[ERROR] Failed to load settings: {e}")

                msg = f"Starting Character: {self.game_options.get('starting_character', 'no starting character found')}"
                self.command_processor.output(self=self.command_processor, text=msg)
            def load_client_settings(task=None):
                if not self.seed_name:
                    self.logger.info("[DEBUG]: No seed name found in RoomInfo!!!!! STILL IDK WHY.")
                task = asyncio.create_task(load_settings(self))
                task.add_done_callback(injest_load_client_settings)

            if not self.seed_name:

                self.logger.info("[DEBUG]: No seed name found in RoomInfo. IDK WHY.")
                asyncio.create_task(asyncio.sleep(0.2)).add_done_callback(load_client_settings)

            else:
                if self._debug:
                    self.logger.info(f"[DEBUG] RoomInfo received with seed name: {self.seed_name}")
                load_client_settings()


            # self.command_processor.output(self=self, text=f"[color=green]{msg}[/color]") #TODO: color in GUI

        if cmd == 'ReceivedItems':
            self.send_received_item_updates()

    def send_received_item_updates(self):
        if not self.loaded_client_settings:
            return # don't send updates until settings are loaded, because we would be duplicating messages
        received_ids: list[int] = [item.item for item in self.items_received]
        new_items: list[str] = []
        added_ids = set()
        self.logger.info(f"[DEBUG]: Received {len(received_ids)} items")
        for network_item in self.items_received:
            # Newly-obtained items
            is_more_than_one = Items.item_table[network_item.item].get("count", 0)

            if (not network_item.item in self.previously_received_item_ids or is_more_than_one) and network_item.item not in added_ids:
                added_ids.add(network_item.item)

                # handle items with more than 1 count
                if is_more_than_one:
                    count_of_items_already_received = self.previously_received_item_ids.count(network_item.item)
                    count_of_sent_received = [i.item for i in self.items_received].count(network_item.item)
                    count_of_item = count_of_sent_received - count_of_items_already_received
                    if count_of_item <= 0:
                        continue
                    elif count_of_item > 1:
                        new_items.append(f"{count_of_item}x {str(self.item_names.lookup_in_game(network_item.item))}")
                    else:# count_of_item == 1:
                        new_items.append(str(self.item_names.lookup_in_game(network_item.item)))
                    continue

                new_items.append(str(self.item_names.lookup_in_game(network_item.item)))
        if self.whisper_updates_enabled and new_items:
            self.text_to_send.append(("You received new items! : " + ", ".join(new_items), True))
        self.previously_received_item_ids = received_ids
        if self.loaded_client_settings:
            self.update_settings()

    def update_settings(self):
        """Update a setting and save it to the settings file."""
        
        def set_settings(task):
            try:
                task.result()  # Will raise if save failed
                if self._debug:
                    self.logger.info(f"[DEBUG] Settings saved successfully.")
            except Exception as e:
                self.logger.error(f"[ERROR] Failed to save settings: {e}")
        
        task = asyncio.create_task(save_settings(self))
        task.add_done_callback(set_settings)

    def run_gui(self) -> None:
        #from .ClientGui import start_gui # custom UI
        #start_gui(self)

        super().run_gui()

async def main():
    Utils.init_logging("PathOfExileClient", exception_logger="Client")

    ctx = PathOfExileContext(None, None)

    #if gui_enabled:
    if True: # we can disable GUI for testing here
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    # use colorama to display colored text highlighting
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()





























#    def _cmd_test_tts(self) -> bool:
#        from .poeClient import tts
#
#        import worlds.poe.Items as Items
#        # mock a context with missing locations, player names, and item lookup and such
#        class mockCtx:
#            class mock_network_item:
#                def __init__(self, item, player):
#                    self.item = item
#                    self.player = player
#
#            class mock_item_names:
#                def lookup_in_slot(self, item, player):
#                    # Mock item names lookup
#                    return f"ItemName_{str(item)} for Player{player}"
#
#            def __init__(self):
#                self.missing_locations = list(Items.item_table.keys())
#                self.locations_info = {
#                    loc_id: self.mock_network_item(item, player)
#                    for (loc_id, item), player in zip(Items.item_table.items(), range(1, len(Items.item_table) + 1))
#                }
#                self.player_names = {player_id: f"Player{player_id}" for player_id in
#                                     range(1, len(Items.item_table) + 1)}
#                self.item_names = self.mock_item_names()
#
#        mctx = mockCtx()
#        tts.generate_tts_tasks_from_missing_locations(mctx)
#        tts.run_tts_tasks()
