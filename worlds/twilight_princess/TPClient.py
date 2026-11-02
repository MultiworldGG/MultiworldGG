import asyncio
from collections import deque
from copy import deepcopy
import time
import traceback
import math
from typing import TYPE_CHECKING, Any, Optional

from MultiServer import mark_raw
import dolphin_memory_engine

from .ClientItemChecker import check_dungeon_item_count, check_item_count  # type: ignore

from .ClientUtils import *
from .Items import ITEM_TABLE, LOOKUP_ID_TO_NAME
from .Locations import LOCATION_TABLE, TPLocation, TPLocationType, TPFlag
from .options import IliaQuest
import Utils
from CommonClient import (
    ClientCommandProcessor,
    CommonContext,
    logger,
    server_loop,
    gui_enabled,
    get_base_parser,
)

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

# Source - https://stackoverflow.com/a/14119223
# Posted by tomvodi, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-25, License - CC BY-SA 4.0

import tkinter as tk

root = tk.Tk()
root.withdraw()


from NetUtils import NetworkItem, ClientStatus

from .ClientUtils import ITEM_APID_BASE

if TYPE_CHECKING:
    import kvui

CONNECTION_REFUSED_GAME_STATUS = "Dolphin connected but wrong game found. Please load a ROM for Twilight Princess. Trying again in 5 seconds..."
CONNECTION_REFUSED_SAVE_STATUS = "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
CONNECTION_LOST_STATUS = "Dolphin connection was lost. Please restart your emulator and make sure Twilight Princess is running."
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

RANDO_NOT_LOADED_MSG = "Randomizer is not loaded, Client will not work until fixed"
WRONG_SEED_LOADED_MSG = "Invalid Seed\nEither the wrong seed was loaded, or you are not in game yet\nSeed to use: "
CONNECT_IN_GAME_MSG = (
    "Please load a save file and gain control of link before attempting to connect"
)
ITEM_IMBALANCE_MSG_1 = (
    "The game has recieved more items then the server expects.\nGame recieved "
)
ITEM_IMBALANCE_MSG_2 = " items, but server expected "
ITEM_IMBALANCE_MSG_3 = " items to be recieved.\nWhen the 2 numbers match you will begin recieving items again."

VALIDATION_TIME = 10

# CURR_HEALTH_ADDR = 0x804061C2
# CURR_NODE_ADDR = 0x80406B38
# SLOT_NAME_ADDR = 0x80406374
# ITEM_WRITE_ADDR = 0x80406AB0
# EXPECTED_INDEX_ADDR = 0x80406734
# NODES_START_ADDR = 0x804063B0
# ACTIVE_NODE_ADDR = 0x80406B18
LINK_POINTER_ADDR = 0x8040BF6C
M_EVENT_STATUS_ADDR = 0x8040B16D

DEBUGGING = False


def set_address(
    regionCode=None,
    curr_health_addr=None,
    curr_node_addr=None,
    slot_name_addr=None,
    item_write_addr=None,
    expected_index_addr=None,
    nodes_start_addr=None,
    active_node_addr=None,
    link_pointer_addr=None,
    m_event_status_addr=None,
):
    global STRING_ENCODING
    if regionCode is None:
        regionCode = read_byte(0x80000003)
    saveFileAddr = 0x804061C0  # US by default
    STRING_ENCODING = "latin"
    match (regionCode):
        case 0x50:  # ASCII for 'P', which is EU
            saveFileAddr = 0x80408160
            STRING_ENCODING = "latin"
        case 0x4A:  # ASCII for 'J', which is JP
            saveFileAddr = 0x80400300
            STRING_ENCODING = "shift-jis"

    global CURR_HEALTH_ADDR, CURR_NODE_ADDR, SLOT_NAME_ADDR, ITEM_WRITE_ADDR, EXPECTED_INDEX_ADDR, NODES_START_ADDR, ACTIVE_NODE_ADDR, SAVE_FILE_ADDR, LINK_POINTER_ADDR, M_EVENT_STATUS_ADDR, REGION_CODE, MENU_STATE

    REGION_CODE = regionCode

    CURR_HEALTH_ADDR = (
        curr_health_addr if curr_health_addr is not None else saveFileAddr + 0x2
    )
    CURR_NODE_ADDR = (
        curr_node_addr if curr_node_addr is not None else saveFileAddr + 0x978
    )
    SLOT_NAME_ADDR = (
        slot_name_addr if slot_name_addr is not None else saveFileAddr + 0x1B4
    )
    ITEM_WRITE_ADDR = (
        item_write_addr if item_write_addr is not None else saveFileAddr + 0x8F0
    )
    EXPECTED_INDEX_ADDR = (
        expected_index_addr if expected_index_addr is not None else saveFileAddr + 0x8FC
    )
    NODES_START_ADDR = (
        nodes_start_addr if nodes_start_addr is not None else saveFileAddr + 0x1F0
    )
    ACTIVE_NODE_ADDR = (
        active_node_addr if active_node_addr is not None else saveFileAddr + 0x958
    )
    SAVE_FILE_ADDR = saveFileAddr
    LINK_POINTER_ADDR = (
        link_pointer_addr if link_pointer_addr is not None else saveFileAddr + 0x5DAC
    )
    M_EVENT_STATUS_ADDR = (
        m_event_status_addr
        if m_event_status_addr is not None
        else saveFileAddr + 0x4FAD
    )
    match (regionCode):
        case 0x50:  # ASCII for 'P', which is EU
            MENU_STATE = 0x80432207
        case 0x4A:  # ASCII for 'J', which is JP
            MENU_STATE = 0x8042A387
        case _:
            MENU_STATE = 0x80430247


# ...existing code...


class TPCommandProcessor(ClientCommandProcessor):
    """
    Command processor for the Twilight Princess client.

    This class handles all commands that are specific to the Twilight Princess client.
    """

    def __init__(self, ctx: CommonContext):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        super().__init__(ctx)

    def _cmd_dolphin(self) -> None:
        """Display the current Dolphin emulator connection status."""
        if isinstance(self.ctx, TPContext):
            assert isinstance(self.ctx.dolphin_status, str)

            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_deathlink(self) -> None:
        """Toggles Deathlink on / off"""
        logger.info("Updating Deathlink")
        Utils.async_start(self.ctx.update_death_link(not self.ctx.deathlink_enabled))

    def _cmd_debug(self) -> None:
        """Toggles Debug messages from showing"""
        global DEBUGGING
        DEBUGGING = not DEBUGGING

    def _cmd_debug_name(self) -> None:
        """Debug to get player name"""
        logger.info(self.ctx.auth)
        logger.info(read_string(read_pointer(0x800042BC) + 0xAC, 16))

    def _cmd_debug_seed(self) -> None:
        """Debug to get Seed name"""
        logger.info(self.ctx.SeedID)
        logger.info(read_string(read_pointer(0x800042BC) + 0x9C, 16))

    @mark_raw
    def _cmd_validate(self, item_name: str = "") -> None:
        """Debug command to check how many items there should be vs how many you have in game"""

        if self.ctx.dolphin_status != CONNECTION_CONNECTED_STATUS:
            logger.info("please connect dolphin first")
            return

        if item_name not in ITEM_TABLE:
            logger.info("not a valid item")
            return

        logger.info(
            f"Link has {_validate_item(item_name, self.ctx, True)} x {item_name}"
        )

    @mark_raw
    def _cmd_validation_time(self, time: str = "10") -> None:
        """Change the time between validation of links inventory. Time must be a number (Default is 10s)"""
        try:
            num = int(time)

            if num <= 0:
                logger.info("Please choose a number greater then 0")
                return

            logger.info(f"Setting validation to occur every {num}s")
            global VALIDATION_TIME
            VALIDATION_TIME = num
        except ValueError:
            logger.info("Invalid input: cannot convert to integer")

    @mark_raw
    def _cmd_validation_pause(self) -> None:
        """Toggle Validation on and off"""
        if self.ctx.validation_pause.is_set():
            logger.info("Pausing validation")
            self.ctx.validation_pause.set()
        else:
            logger.info("Resuming Validation")
            self.ctx.validation_pause.clear()


class TPContext(CommonContext):
    """
    The context for Twilight Princess client.

    This class manages all interactions with the Dolphin emulator and the Archipelago server for Twilight Princess.
    """

    command_processor: TPCommandProcessor = TPCommandProcessor
    game: str = "Twilight Princess"
    items_handling: int = 0b011

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        """
        Initialize the context with the provided server address and password.

        :param server_address: The address of the Archipelago server.
        :param password: The password for the server.
        """
        super().__init__(server_address, password)
        self.item_queue: deque[tuple[NetworkItem, int]] = deque()
        self.insurance_queue: deque[tuple[str, int]] = deque()
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.last_received_index = -1
        self.has_send_death = False
        self.waiting_to_kill = False
        self.current_node = 0xFF
        self.server_data_copy: dict[str, str | bool] = {}
        self.server_data = deepcopy(server_data)
        self.server_data_built = False
        self.server_data_sent = False
        self.validation_time_start = time.time()
        self.check_in_game_msg_timer = time.time()
        self.hint_timer = time.time()
        self.SeedID = ""
        self.rando_loaded_message = False
        self.connection_tried = False
        # Event is used for pause as it better represents how I want to think about it
        self.validation_pause = asyncio.Event()
        self.hints_created: dict[str, bool] = {}

    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        """
        Disconnect from the server and stop the Dolphin synchronization task.

        :param allow_autoreconnect: Whether to allow the client to automatically reconnect to the server.
        """
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        assert isinstance(password_requested, bool)

        if not await check_ingame(self):
            raise Exception(CONNECT_IN_GAME_MSG)

        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            pointer = read_pointer(0x800042BC)
            if pointer == 0:
                raise Exception(
                    "Failed to read Seed; Please Make sure dolphin is connected correctly"
                )
            self.auth = read_string(pointer + 0xAC, 16)
        await self.send_connect()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """

        if cmd == "Connected":
            self.items_received = []
            self.item_queue = deque()
            self.insurance_queue = deque()
            self.validation_time_start = time.time()
            self.item_imbalance_msg_timer = time.time()
            self.validation_pause.set()
            self.start_inventory: list = []
            self.locations_checked = set()
            self.last_received_index = read_short(EXPECTED_INDEX_ADDR)
            self.ilia_quest = IliaQuest.from_any(IliaQuest.option_vanilla)
            self.deathlink_enabled = False

            if args["slot_data"] is not None and "SeedID" in args["slot_data"]:
                assert isinstance(
                    args["slot_data"]["SeedID"], str
                ), f"{args["slot_data"]["SeedID"]=}"
                self.SeedID = args["slot_data"]["SeedID"]
                pointer = read_pointer(0x800042BC)
                if pointer == 0:
                    raise Exception(
                        "Failed to read Seed; Please Make sure dolphin is connected correctly"
                    )
                read_seedID = read_string(pointer + 0x9C, 16)
                if DEBUGGING:
                    logger.info(
                        f"Debug: Connected checking seed ids\nServer wants: {self.SeedID}\nClient has:  {read_seedID}"
                    )
                if self.SeedID != read_seedID:

                    Utils.async_start(self.disconnect())
                    raise Exception(WRONG_SEED_LOADED_MSG + self.SeedID)

            if args["slot_data"] is not None and "DeathLink" in args["slot_data"]:
                assert isinstance(
                    args["slot_data"]["DeathLink"], int
                ), f"{args["slot_data"]["DeathLink"]=}"
                self.deathlink_enabled = bool(args["slot_data"]["DeathLink"])
                Utils.async_start(self.update_death_link(self.deathlink_enabled))
                if DEBUGGING:
                    logger.info(f"Debug: Seting deathlink to {self.deathlink_enabled}")
            if args["slot_data"] is not None and "StartInventory" in args["slot_data"]:
                assert isinstance(
                    args["slot_data"]["StartInventory"], list
                ), f"{args["slot_data"]["StartInventory"]=}"

                self.start_inventory: list[int] = args["slot_data"]["StartInventory"]
            if (
                args["slot_data"] is not None
                and "Settings" in args["slot_data"]
                and "Ilia Quest" in args["slot_data"]["Settings"]
            ):
                assert isinstance(
                    args["slot_data"]["Settings"]["Ilia Quest"], str
                ), f"{args["slot_data"]["Settings"]["Ilia Quest"]=}"

                self.ilia_quest = IliaQuest.from_text(
                    args["slot_data"]["Settings"]["Ilia Quest"]
                )

            if args["slot_data"] is not None and (
                not args["slot_data"]["World Version"]
                or args["slot_data"]["World Version"] != VERSION
            ):
                logger.info(
                    f"""Error: Client version does not match version of generated seed. 
                            Things may not work as intended,
                            Seed version:{args["slot_data"]["World Version"]} client version:{VERSION}"""
                )
            else:
                logger.info(f"""Connected Using Seed & client version:{VERSION}""")
            self.server_data_built = False
            self.server_data = deepcopy(server_data)

        elif cmd == "ReceivedItems":
            if DEBUGGING:
                logger.info(
                    f"Debug: Recieved Item {args["index"]=}   {self.last_received_index=}"
                )

            assert isinstance(args["items"], list)

            # Every ValidationTime (10s) try to sync if items bad. Also msg to tell people what is happening
            if len(self.items_received) < self.last_received_index:
                if self.item_imbalance_msg_timer > time.time() + VALIDATION_TIME:
                    logger.info(
                        ITEM_IMBALANCE_MSG_1
                        + self.last_received_index
                        + ITEM_IMBALANCE_MSG_2
                        + len(self.items_received)
                        + ITEM_IMBALANCE_MSG_3
                    )
                    self.item_imbalance_msg_timer = time.time()
                    asyncio.create_task(self.send_msgs([{"cmd": "Sync"}]))

            elif len(self.items_received) > self.last_received_index:

                self.validation_pause.set()
                new_items = self.items_received[self.last_received_index :]
                self.last_received_index = len(self.items_received)
                write_short(EXPECTED_INDEX_ADDR, self.last_received_index)

                for item in new_items:
                    assert isinstance(
                        item, NetworkItem
                    ), f"[Twilight Princess Client] Recived an item the is not a Network Item {item=}"

                    if DEBUGGING:
                        logger.info(f"Debug: Recieved {item=} from server")

                    if (
                        item.player != self.slot or item.location == -1
                    ):  # Don't give own items unless cheated in
                        if DEBUGGING:
                            logger.info(f"Debug: Adding into the queue {item=}")
                        self.item_queue.append((item, self.last_received_index))
                    # Add keys to the validation count
                    if LOOKUP_ID_TO_NAME[item.item] in KEY_TO_OFFSET.keys():
                        key_offset = (
                            SAVE_FILE_ADDR
                            + 0x901
                            + KEY_TO_OFFSET[LOOKUP_ID_TO_NAME[item.item]]
                        )
                        key_count = read_byte(key_offset)
                        write_byte(key_offset, key_count + 1)

    def on_deathlink(self, data: dict[str, Any]) -> None:
        """
        Handle a DeathLink event.

        :param data: The data associated with the DeathLink event.
        """
        if DEBUGGING:
            logger.info("Debug: on deathlink trigger")

        super().on_deathlink(data)
        _give_death(self)

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for Twilight Princess client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = f"{apname} Twilight Princess Client"
        return ui

    def event_invalid_slot(self):
        raise Exception("Invalid Slot; Make sure that the right seed is loaded")


def read_byte(console_address: int) -> int:
    """
    Read a byte from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    assert isinstance(console_address, int)
    result = dolphin_memory_engine.read_byte(console_address)
    assert isinstance(result, int)
    result = result % 256
    return result


def read_short(console_address: int) -> int:
    """
    Read a short from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    assert isinstance(console_address, int)
    read_bytes = dolphin_memory_engine.read_bytes(console_address, 2)
    result = int.from_bytes(read_bytes)
    assert isinstance(result, int)
    return result


def read_pointer(console_address: int) -> int:
    """
    Read a pointer from Dolphin memory.
    *Note only reads the pointer not value at pointer

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    assert isinstance(console_address, int)
    result = int.from_bytes(
        dolphin_memory_engine.read_bytes(console_address, 4), byteorder="big"
    )
    assert isinstance(result, int)
    return result


def read_string(console_address: int, strlen: int) -> str:
    """
    Read a string from Dolphin memory.

    :param console_address: Address to read from.
    :param strlen: Length of the string to read.
    :return: The string read from memory.
    """
    assert isinstance(console_address, int)
    assert isinstance(strlen, int)
    result = (
        dolphin_memory_engine.read_bytes(console_address, strlen)
        .split(b"\0", 1)[0]
        .decode(STRING_ENCODING)
    )
    assert isinstance(result, str)
    return result


def write_byte(console_address: int, value: int) -> None:
    """
    Write a byte to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    assert isinstance(console_address, int)
    assert isinstance(value, int)

    dolphin_memory_engine.write_bytes(
        console_address, value.to_bytes(1, byteorder="big")
    )


def write_short(console_address: int, value: int) -> None:
    """
    Write a short to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    assert isinstance(console_address, int)
    assert isinstance(value, int)

    dolphin_memory_engine.write_bytes(
        console_address, value.to_bytes(2, byteorder="big")
    )


def write_string(console_address: int, string: str) -> None:
    """
    Write a string to Dolphin memory.

    :param console_address: Address to write to.
    :param string: String to write.
    """
    assert isinstance(console_address, int)
    assert isinstance(string, str)

    if len(string) > 16:
        raise ValueError("String length must be 16 characters or less.")

    dolphin_memory_engine.write_bytes(
        console_address, string.encode(STRING_ENCODING) + b"\0"
    )


def write_name(name: str):
    assert isinstance(name, str)

    if len(name) > 16:
        name = name[:16]

    # Pad the name with 0x00 characters to make it 16 characters long
    padded_name = name.ljust(16, "\x00")

    logger.info(f"Writing name {padded_name}")
    write_string(SLOT_NAME_ADDR, padded_name)
    # write_byte(SAVE_FILE_ADDR + 0x900, 0x1)


# def check_key_counts()


def _give_death(ctx: TPContext) -> None:
    """
    Trigger the player's death in-game by setting their current health to zero.

    :param ctx: Twilight Princess client context.
    """
    if DEBUGGING:
        logger.info("Debug: Trying to kill player")

    if (
        ctx.slot is not None
        and dolphin_memory_engine.is_hooked()
        and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
        and _check_status()
    ):
        ctx.has_send_death = True

        if read_byte(MENU_STATE) == 2:
            if DEBUGGING:
                logger.info("Debug: Skipped death waiting for out of menu")
            ctx.waiting_to_kill = True
            return

        write_short(CURR_HEALTH_ADDR, 0)

        if DEBUGGING:
            logger.info("Debug: Health set to 0")


async def _give_items(ctx: TPContext, items: list[str]) -> bool:
    """
    Give a batch of items to the player in-game.
    items must contain at max 8 items as that is the size of the queue

    :param ctx: Twilight Princess client context.
    :param items: Name of the items to give.
    :return: Whether the items were successfully given.
    """

    assert isinstance(items, list), f"{items=}"
    assert len(items) > 0, f"{items=}"
    assert (
        len(items) <= 8
    ), f"{len(items)}"  # Could put to 7 to allow for extra buffer incase

    if not await check_ingame(ctx):
        return False
    if not _check_status():
        return False

    for item_name in items:
        assert item_name in ITEM_TABLE, f"{item_name=} not in item table "
        assert isinstance(
            ITEM_TABLE[item_name].item_id, int
        ), f"{item_name=} has no item_id"

    # Only add items to the queue if it is empty
    for i in range(0, 8):
        item_stack_addr = ITEM_WRITE_ADDR + i
        if read_byte(item_stack_addr) != 0x00:
            return False

    # Now its empty
    # Add items starting at 0x8F0 so that it is given first
    for i in range(0, len(items)):
        item_stack_addr = ITEM_WRITE_ADDR + i
        item = items[i]
        # Just incase something happens
        assert (
            read_byte(item_stack_addr) == 0x00
        ), f"Tried to add to the queue but it was not empty"

        if DEBUGGING:
            logger.info(f"Debug: Giving {item} into queue")

        if item == "Victory":
            if not ctx.finished_game:
                logger.info("Player got victory but the game is not complete in client")
            continue

        write_byte(item_stack_addr, ITEM_TABLE[items[i]].item_id)

    # Now the queue is full and all items are added

    ctx.validation_time_start = time.time()

    return True


async def give_items(ctx: TPContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: Twilight Princess client context.
    """
    if (
        await check_ingame(ctx)
        and dolphin_memory_engine.read_byte(CURR_NODE_ADDR) != 0xFF
    ):
        # Items will be filtered from client item_queue to here
        item_give_queue: list[str] = []

        # Empty the Queue
        while len(ctx.item_queue) > 0:

            item, item_index = ctx.item_queue.pop()

            item_name = LOOKUP_ID_TO_NAME[item.item]
            assert (
                item_name in ITEM_TABLE
            ), f"[Twilight Princess Client] tried to give {item_name=} but it is not in the item table"

            item_data = ITEM_TABLE[item_name]

            if DEBUGGING:
                logger.info(f"Debug: Trying to give {item_name=}")

            # Dont need to be worried about
            item_give_queue.append(item_name)

            # Only try to give a full queue or whatever is there
            if len(item_give_queue) == 8:
                if DEBUGGING:
                    logger.info(f"Debug: Queued Items to give {item_give_queue}")
                while not await _give_items(ctx, item_give_queue):
                    await asyncio.sleep(0.5)
                item_give_queue = []
                ctx.validation_time_start = time.time()

        if len(item_give_queue) > 0:
            assert (
                len(item_give_queue) <= 8
            ), f"[Twilight Princess Client] This is an un expected error please report this"
            if DEBUGGING:
                logger.info(f"Debug: Queued Items to give {item_give_queue}")
            while not await _give_items(ctx, item_give_queue):
                await asyncio.sleep(0.5)
            ctx.validation_time_start = time.time()

        # Now validation should be good to occur
        if ctx.validation_pause.is_set():
            ctx.validation_pause.clear()

        return


def _validate_item(
    item_name: str, ctx: TPContext, descriptive=False
) -> int | tuple[int, int]:
    """
    Returns the difference in item count where Positive amount is a missing amount
    """
    item_data = ITEM_TABLE[item_name]

    if item_data.type in [
        "Rupee",
        "Ammo",
        "Trap",
        "Event",
        "Portal",
    ]:
        # Skip all non insurable items
        return -1

    assert isinstance(item_data.code, int), f"{item_name=} does not have a code"

    item_id = item_data.code + ITEM_APID_BASE

    if item_data.type in [
        "Book",
        "Small key",
        "Big Key",
        "Item",
        "Bottle",
        "Bug",
        "Poe",
        "Quest",
    ]:
        actual_item_count = check_item_count(item_name, SAVE_FILE_ADDR)

        expected_item_count = 0
        for item in ctx.items_received:
            if item.item == item_id:
                expected_item_count += 1

        # If item is in KEY_TO_OFFSET count is handled independent of link, everything else must be accounted for
        if item_name not in KEY_TO_OFFSET.keys():
            expected_item_count += ctx.start_inventory.count(item_id)

        expected_item_count = min(expected_item_count, item_data.quantity)

        if descriptive:
            return expected_item_count, actual_item_count
        else:
            return expected_item_count - actual_item_count

    elif item_data.type in [
        "Compass",
        "Map",
    ]:
        item_count = check_dungeon_item_count(
            item_name, NODES_START_ADDR, ctx.current_node
        )

        expected_item_count = 0
        for item in ctx.items_received:
            if item.item == item_id:
                expected_item_count += 1

        expected_item_count += ctx.start_inventory.count(item_id)

        expected_item_count = min(expected_item_count, item_data.quantity)

        if descriptive:
            return expected_item_count, item_count
        else:
            return expected_item_count - item_count

    elif item_data.type in [
        "Heart",
    ]:
        # Only try to give heart pieces and not containers
        if item_name != "Piece of Heart":
            return -1

        actual_heart_pieace_count = read_short(SAVE_FILE_ADDR)
        heart_piece_count = 0
        heart_container_count = 0
        heart_piece_id = ITEM_TABLE["Piece of Heart"].code + ITEM_APID_BASE
        heart_container_id = ITEM_TABLE["Heart Container"].code + ITEM_APID_BASE

        heart_piece_count = [item.item for item in ctx.items_received].count(
            heart_piece_id
        ) + ctx.start_inventory.count(heart_piece_id)

        heart_container_count = [item.item for item in ctx.items_received].count(
            heart_container_id
        ) + ctx.start_inventory.count(heart_container_id)

        heart_difference = (
            (heart_container_count * 5) + heart_piece_count + 15
        ) - actual_heart_pieace_count

        if heart_difference > 0:
            if descriptive:
                return (
                    (heart_container_count * 5) + heart_piece_count + 15
                ), actual_heart_pieace_count
            else:
                return heart_difference
        else:
            return 0
    else:
        assert (
            False
        ), f"[Twilight Princess Client] {item_name=} has an invalid type {item_data.type}"


async def validate_items(ctx: TPContext) -> None:

    # Wait for timer to expire
    if ctx.validation_time_start + VALIDATION_TIME > time.time():
        return

    if not await check_ingame(ctx):
        ctx.insurance_queue = deque()
        if DEBUGGING:
            logger.info("Debug: Insurance occured during load game ")
        return

    # Restart timer if not in correct state
    if (ctx.validation_pause.is_set()) or (not _check_status()):
        ctx.validation_time_start = time.time()
        return

    if DEBUGGING:
        logger.info("Debug: Validating items")

    # First check if item queue is empty as we don't want to double give
    for i in range(0, 8):
        item_stack_addr = ITEM_WRITE_ADDR + i
        if read_byte(item_stack_addr) != 0x00:
            ctx.validation_time_start = time.time()  # Reset timer to wait for empty
            return

    # Now that validation is starting let's pause incase async stuff
    ctx.validation_pause.set()

    for item_name in ITEM_TABLE:

        item_count = _validate_item(item_name, ctx)

        assert isinstance(
            item_count, int
        ), f"[Twilight Princess Client] {item_count=}, {item_name=}"

        if item_count <= 0:  # -1 items are not insurable
            continue

        if DEBUGGING:
            logger.info(
                f"Debug: validation found you are missing {item_count} x {item_name}"
            )

        # Give Heart containers when possible to help things (Note: Heart Containers are a -1 item)
        if item_name == "Piece of Heart" and item_count >= 5:
            full_hearts = math.floor(item_count / 5)
            remainder = item_count % 5

            assert (
                (full_hearts * 5) + remainder
            ) == item_count, f"The math is bad try again {((full_hearts * 5) + remainder)=} {item_count=}"

            ctx.insurance_queue.append(["Heart Container", full_hearts])
            if remainder > 0:
                ctx.insurance_queue.append(["Piece of Heart", remainder])
        elif item_name in KEY_TO_OFFSET.keys():
            key_offset = SAVE_FILE_ADDR + 0x901 + KEY_TO_OFFSET[item_name]
            key_count = read_byte(key_offset)
            write_byte(key_offset, key_count + item_count)
            ctx.insurance_queue.append([item_name, item_count])
        else:
            ctx.insurance_queue.append([item_name, item_count])

        item_give_list: list[str] = []

        if not await check_ingame(ctx):
            ctx.insurance_queue = deque()
            if DEBUGGING:
                logger.info("Debug: Insurance occured during load game ")
            return

        while len(ctx.insurance_queue) > 0:

            item_name, count = ctx.insurance_queue.pop()
            if DEBUGGING:
                logger.info(f"Debug: Popped {item_name} x {count} from insurance queue")

            assert count > 0
            for _ in range(count):

                item_give_list.append(item_name)
                if DEBUGGING:
                    logger.info(f"Adding {item_name=} into the queue")

                if len(item_give_list) == 8 or len(ctx.insurance_queue) <= 0:
                    while not await _give_items(ctx, item_give_list):
                        await asyncio.sleep(0.5)
                    item_give_list = []

    # Set the timer for validation to start again
    ctx.validation_time_start = time.time()


async def check_locations(ctx: TPContext) -> None:
    """
    Iterate through all locations and check whether the player has checked each location.
    If the location is in the active node check memory rather than save data

    Update the server with all newly checked locations since the last update. If the player has completed the goal,
    notify the server.

    :param ctx: Twilight Princess client context.
    """

    if not await check_ingame(ctx):
        return

    current_node = read_byte(CURR_NODE_ADDR)

    locations_read = set()

    for location, data in LOCATION_TABLE.items():

        # There might be a better way but this works for now
        # Also this data is a flag so node handling is not needed
        if location == "Hyrule Castle Ganondorf":
            addr = SAVE_FILE_ADDR + data.offset
            byte = read_byte(addr)
            checked = (byte & data.bit) != 0
            if checked:
                if not ctx.finished_game:
                    logger.info("Game finishing")
                # It sends multiple times incase the server does not acknoledge.
                # Upon completion check locations will stop running
                await ctx.send_msgs(
                    [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
                )
                ctx.finished_game = True
            continue

        # If there is not a valid apid dont bother checking that location
        # apids not given when logic only location
        if not isinstance(data.code, int):
            continue

        # Debug functionality
        if DEBUGGING and (
            not isinstance(data.bit, int) or not isinstance(data.offset, int)
        ):
            logger.info(f"Debug: location:{location} has weird formating")
            continue

        # Skip quest locations if they are pre-collected inverse of itempool handling
        # # Still checking determistic placements for the messages / UT
        if data.flags & TPFlag.Quest:
            if (
                (
                    location == "Renados Letter"
                    and not ctx.ilia_quest.value == IliaQuest.option_vanilla
                )
                or (
                    location == "Telma Invoice"
                    and not ctx.ilia_quest.value
                    in [
                        IliaQuest.option_vanilla,
                        IliaQuest.option_letter,
                    ]
                )
                or (
                    location == "Wooden Statue"
                    and ctx.ilia_quest.value
                    in [IliaQuest.option_statue, IliaQuest.option_charm]
                )
                or (
                    location == "Ilias Charm"
                    and ctx.ilia_quest.value == IliaQuest.option_charm
                )
            ):
                continue

        # Depening on locatin type find the memory address for the flag
        # Checks the active memory for the current node
        match (data.type):
            case TPLocationType.Region:
                region = data.region.value
                assert (
                    isinstance(region, int) and data.offset < 0x20
                ), f"Location {location=} has bad region {region} {data=}"
                if region == current_node:
                    addr = ACTIVE_NODE_ADDR + data.offset
                else:
                    addr = (region * 32) + NODES_START_ADDR + data.offset
            case TPLocationType.Flag:
                addr = SAVE_FILE_ADDR + data.offset
            case TPLocationType.Event:
                if DEBUGGING:
                    logger.info(f"Debug: {location}, is an event with an apid")
                continue

        byte = read_byte(addr)
        checked = (byte & data.bit) != 0
        if checked:
            locations_read.add(TPLocation.get_apid(data.code))

    # Build the server data to use a player and team keyed value
    if not ctx.server_data_built:
        new_server_data_copy = {}
        for i, data in enumerate(server_data):
            assert "TP_" not in data["key"], f"{data=}"
            new_key = f"TP_{ctx.team}_{ctx.slot}_{data["key"]}"
            ctx.server_data[i]["key"] = new_key
            new_value = data["default"]

            assert new_value is not None, f"{new_key}"

            new_server_data_copy[new_key] = new_value
        ctx.server_data_built = True
        ctx.server_data_copy = new_server_data_copy

    # Build out messages to set data into the server (build before location check for mid check changes)
    messages: list[dict[str, any]] = []
    results: list[dict[str, any]] = []
    assert len(ctx.server_data_copy) > 0, f"{ctx.server_data_copy=}"
    for server_copy_key, server_copy_value in ctx.server_data_copy.items():
        data = [data for data in ctx.server_data if data["key"] == server_copy_key][0]
        assert data, f"{server_copy_key=}"

        if data["Region"] == "Flag":
            assert isinstance(server_copy_value, bool), f"{server_copy_key=}"
            addr = SAVE_FILE_ADDR + data["Offset"]
            byte = read_byte(addr)
            checked = (byte & data["Flag"]) != 0
            if checked != server_copy_value:
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {checked}"
                    )
                # The value has changed so update the sever
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": checked}],
                    }
                )
                results.append({server_copy_key: checked})

        elif data["Region"] == "Region":
            assert isinstance(server_copy_value, bool), f"{server_copy_key=}"
            region = data["Node"]
            assert (
                isinstance(region, int) and data["Offset"] < 0x20
            ), f"Location {location=} has bad region {region} {data=}"
            if region == current_node:
                addr = ACTIVE_NODE_ADDR + data["Offset"]
            else:
                addr = (region * 32) + NODES_START_ADDR + data["Offset"]
            byte = read_byte(addr)
            checked = (byte & data["Flag"]) != 0
            if checked != server_copy_value:
                # The value has changed so update the sever
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {checked}"
                    )
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": checked}],
                    }
                )
                results.append({server_copy_key: checked})
        elif data["Region"] == "Node Number":
            assert isinstance(server_copy_value, str), f"{server_copy_key=}"
            node = NODE_TO_STRING[server_copy_value]
            if node != ctx.current_node:
                new_node_str = [
                    node
                    for node, num in NODE_TO_STRING.items()
                    if num == ctx.current_node
                ][0]
                assert isinstance(new_node_str, str), f"{new_node_str=}"
                assert new_node_str, f"{new_node_str=}"
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {new_node_str}"
                    )
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": new_node_str}],
                    }
                )
                results.append({server_copy_key: new_node_str})
        elif data["Region"] == "Room":
            assert isinstance(
                server_copy_value, int
            ), f"{server_copy_key=}, {server_copy_value=}"

            layer_address = SAVE_FILE_ADDR + 0x27220
            if REGION_CODE == 0x50:
                layer_address += 0x20
            current_room = read_byte(layer_address)

            assert isinstance(current_room, int), f"{current_room=}"

            if current_room != server_copy_value:
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {current_room}"
                    )
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": current_room}],
                    }
                )
                results.append({server_copy_key: current_room})
        elif data["Region"] == "Layer":
            assert isinstance(
                server_copy_value, int
            ), f"{server_copy_key=}, {server_copy_value=}"

            layer_address = SAVE_FILE_ADDR + 0x4E0B
            current_layer = read_byte(layer_address)

            assert isinstance(current_layer, int), f"{current_layer=}"

            if current_layer != server_copy_value:
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {current_layer}"
                    )
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [
                            {"operation": "replace", "value": current_layer}
                        ],
                    }
                )
                results.append({server_copy_key: current_layer})
        elif data["Region"] == "Stage":
            assert isinstance(
                server_copy_value, str
            ), f"{server_copy_key=}, {server_copy_value=}"

            result = read_string(SAVE_FILE_ADDR + 0x4E00, 8)

            # Handle the dungeon boss room stages
            if result.startswith("D_MN") and len(result) > 6:
                result = result[:6]

            assert isinstance(result, str), f"{result=}"
            assert result in STAGE_TO_NAME, f"{result=}"

            current_stage_str = STAGE_TO_NAME[result]
            if current_stage_str != server_copy_value:
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {current_stage_str}"
                    )
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [
                            {"operation": "replace", "value": current_stage_str}
                        ],
                    }
                )
                results.append({server_copy_key: current_stage_str})
        elif data["Region"] == "Floor":
            assert isinstance(
                server_copy_value, int
            ), f"{server_copy_key=}, {server_copy_value=}"

            result = SAVE_FILE_ADDR + 0x4AC98
            if REGION_CODE == 0x50:
                result += 0x20
            current_floor = read_byte(result)

            assert isinstance(current_floor, int), f"{current_floor=}"

            if current_floor != server_copy_value:
                if DEBUGGING:
                    logger.info(
                        f"Debug: {server_copy_key} Ready to be set to {current_floor}"
                    )
                messages.append(
                    {
                        "cmd": "Set",
                        "key": data["key"],
                        "default": data["default"],
                        "want_reply": False,
                        "operations": [
                            {"operation": "replace", "value": current_floor}
                        ],
                    }
                )
                results.append({server_copy_key: current_floor})
        else:
            assert False, f"{data=}"

    await asyncio.sleep(0.1)
    if current_node != read_byte(CURR_NODE_ADDR):
        if DEBUGGING:
            logger.info("Debug: Stage changed during location checks skiping checks")
        return

    if not await check_ingame(ctx):
        if DEBUGGING:
            logger.info(
                "Debug: No longer in game during loation checks skipping checks"
            )
        return

    new_locations_checked = locations_read.difference(ctx.locations_checked)
    if new_locations_checked:
        if DEBUGGING:
            logger.info(f"Debug: Sending location checks: {new_locations_checked}")
        await ctx.send_msgs(
            [{"cmd": "LocationChecks", "locations": new_locations_checked}]
        )
        # This might be needed if the clinet doesn't sync, it might also brick if msg is sent but nothing happens
        ctx.locations_checked.update(new_locations_checked)

    # Send out server data messages
    assert len(messages) == len(results), f"{len(messages)=} {len(results)=}"
    for message, result in zip(messages, results):
        assert (
            message["key"] in result
        ), f"{message["key"]=}, {result=}"  # No longer valid as key is individualized
        if DEBUGGING:
            logger.info(
                f"Debug: Sending message for {message["key"]}: {result[message["key"]]}"
            )
        ctx.server_data_copy[message["key"]] = result[message["key"]]
        await ctx.send_msgs(
            [
                message,
            ]
        )


async def check_hints(ctx: TPContext) -> None:
    """
    Parse through a list of shop checks, if the stage and room lines up, then scout the location
    """
    if not await check_ingame(ctx):
        return

    if ctx.hint_timer > time.time() + (VALIDATION_TIME / 2):
        return

    current_stage = read_string(SAVE_FILE_ADDR + 0x4E00, 8)

    layer_address = SAVE_FILE_ADDR + 0x27220
    if REGION_CODE == 0x50:
        layer_address += 0x20
    current_room = read_byte(layer_address)
    await asyncio.sleep(3)
    if current_room != read_byte(layer_address):
        return

    for location, data in HINT_DATA.items():
        assert location in LOCATION_TABLE.keys(), f"{location}"

        stage = data["stage"]
        room = data["room"]

        if current_stage != stage:
            continue
        if current_room != room:
            continue

        loc_id = LOCATION_TABLE[location].code
        assert isinstance(loc_id, int), f"Error: {location=} has no code"

        loc_id = TPLocation.get_apid(loc_id)

        await ctx.send_msgs(
            [
                {
                    "cmd": "CreateHints",
                    "locations": [loc_id],
                    "player": ctx.slot,
                }
            ]
        )
        ctx.hint_timer = time.time()


async def check_alive() -> bool:
    """
    Check if the player is currently alive in-game.

    :return: `True` if the player is alive, otherwise `False`.
    """
    cur_health = read_short(CURR_HEALTH_ADDR)
    return cur_health > 0


async def check_death(ctx: TPContext) -> None:
    """
    Check if the player is currently dead in-game.
    If DeathLink is on, notify the server of the player's death.

    :return: `True` if the player is dead, otherwise `False`.
    """
    if ctx.waiting_to_kill:
        return
    if ctx.slot is not None and await check_ingame(ctx):
        cur_health = read_short(CURR_HEALTH_ADDR)
        if cur_health == 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 5:
                if DEBUGGING:
                    logger.info(
                        "Debug: Sending Death to other players will not send death until player is alive"
                    )
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
        else:
            if DEBUGGING and ctx.has_send_death:
                logger.info("Debug: Player is now alive")
            ctx.has_send_death = False


async def check_ingame(ctx: TPContext, level: int = 0) -> bool:
    """
    Check if the player is currently in-game.
    If the player switches to hyrule field wait 3s to see if the node updates to the menu
    (This check will occur only once per load to the field)

    :return: `True` if the player is in-game, otherwise `False`.
    """

    if not dolphin_memory_engine.is_hooked():
        return False

    # Use Title Stage as in game check
    if read_string(SAVE_FILE_ADDR + 0x4E00, 8) == "F_SP102":
        if ctx.check_in_game_msg_timer + VALIDATION_TIME <= time.time():
            ctx.check_in_game_msg_timer = time.time()
        return False

    new_node = read_byte(CURR_NODE_ADDR)

    # If switching to hyrule field wait and prove not loading title screen
    if ctx.current_node != new_node:
        if new_node == 0x06:
            ctx.current_node = new_node

            if level > 3:
                return False
            level += 1

            await asyncio.sleep(3)
            if not await check_ingame(ctx, level):
                return False
        else:
            ctx.current_node = new_node

    if read_pointer(0x800042BC) != 0x00:
        if (
            ctx.check_in_game_msg_timer + VALIDATION_TIME <= time.time()
        ) and ctx.connection_tried:
            logger.warning(WRONG_SEED_LOADED_MSG + ctx.SeedID)
            ctx.check_in_game_msg_timer = time.time()
        return True
    return False


def _check_status() -> bool:
    """
    Check if link is in a good state to interact with.

    *Gotten from how lunar chooses when to give player items*
    """
    link_actr = read_pointer(LINK_POINTER_ADDR)

    mEventStatus = read_byte(M_EVENT_STATUS_ADDR)
    mDemoType = read_short(link_actr + 0x604)
    mEventId = read_short(link_actr + 0x7BE)

    result = mEventStatus == 0 and mDemoType == 0 and mEventId == 0

    return result


async def dolphin_sync_task(ctx: TPContext) -> None:
    """
    The task loop for managing the connection to Dolphin.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: Twilight Princess client context.
    """
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if (
                dolphin_memory_engine.is_hooked()
                and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
            ):

                if not await check_ingame(ctx):
                    await asyncio.sleep(0.1)
                    continue
                if not ctx.rando_loaded_message:
                    pointer = read_pointer(0x800042BC)
                    if pointer == 0:
                        raise Exception(
                            "Failed to read Seed; Please Make sure dolphin is connected correctly"
                        )
                    read_seedID = read_string(pointer + 0x9C, 16)
                    logger.info(
                        f"Randomizer loaded, you may now connect. Using seed id {read_seedID}"
                    )
                    ctx.rando_loaded_message = True
                if ctx.slot is not None:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                        if ctx.waiting_to_kill:
                            if read_byte(MENU_STATE) != 2 and _check_status():
                                ctx.waiting_to_kill = False
                                await asyncio.sleep(2)
                                _give_death(ctx)
                    # Build data storage here, as on connect cannot deal with async calls and this is before location checks
                    if not ctx.server_data_sent:
                        await ctx.send_msgs(
                            base_server_data_connection(ctx.team, ctx.slot)
                        )
                        ctx.server_data_sent = True
                    await give_items(ctx)
                    await check_locations(ctx)
                    await check_hints(ctx)
                    await validate_items(ctx)

                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    try:
                        if not (
                            dolphin_memory_engine.read_bytes(0x80000000, 3) == b"GZ2"
                            and dolphin_memory_engine.read_byte(0x80000003)
                            in [
                                ord("E"),
                                ord("P"),
                                ord("J"),
                            ]
                        ):
                            logger.info(CONNECTION_REFUSED_GAME_STATUS)
                            ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                            dolphin_memory_engine.un_hook()
                            await asyncio.sleep(5)
                        else:
                            logger.info(CONNECTION_CONNECTED_STATUS)
                            ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                            ctx.locations_checked = set()
                            set_address()
                    except NameError as e:
                        logger.error(f"Global address not set: {e}")
                        set_address(regionCode=ord("E"))
                    except Exception as e:
                        logger.error(f"Unexpected error: {e}")
                        raise e
                else:
                    logger.info(
                        "Connection to Dolphin failed, attempting again in 5 seconds..."
                    )
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info(
                "Connection to Dolphin failed due to error, attempting again in 5 seconds..."
            )
            logger.error(traceback.format_exc())

            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


def main(connect: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Run the main async loop for the Twilight Princess client.

    :param connect: Address of the Archipelago server.
    :param password: Password for server authentication.
    """
    Utils.init_logging("Twilight Princess Client")

    async def _main(connect: Optional[str], password: Optional[str]) -> None:
        ctx = TPContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(
            dolphin_sync_task(ctx), name="DolphinSync"
        )

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama  # type: ignore

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)
