from enum import StrEnum
from logging import Logger, getLogger
from typing import TYPE_CHECKING

import dolphin_memory_engine as dme

import NetUtils
from BaseClasses import ItemClassification
from NetUtils import JSONtoTextParser
from .constants import CLIENT_NAME, WAIT_TIMER_LONG_TIMEOUT, WAIT_TIMER_SHORT_TIMEOUT, WAIT_TIMER_MEDIUM_TIMEOUT
from ..Helper_Functions import string_to_bytes

if TYPE_CHECKING:
    from ..LMClient import LMContext

# Maximum number of bytes that
MAX_DISPLAYED_CHARS: int = 286
MAX_LOCATION_CHARS: int = 32

class DisplayColors(StrEnum):
    BLACK = fr"\eGC[{JSONtoTextParser.color_codes["black"]}FF]\eCC[{JSONtoTextParser.color_codes["black"]}FF]"
    RED = fr"\eGC[{JSONtoTextParser.color_codes["red"]}FF]\eCC[{JSONtoTextParser.color_codes["red"]}FF]"
    GREEN = fr"\eGC[{JSONtoTextParser.color_codes["green"]}FF]\eCC[{JSONtoTextParser.color_codes["green"]}FF]"
    YELLOW = fr"\eGC[{JSONtoTextParser.color_codes["yellow"]}FF]\eCC[{JSONtoTextParser.color_codes["yellow"]}FF]"
    BLUE = fr"\eGC[{JSONtoTextParser.color_codes["blue"]}FF]\eCC[{JSONtoTextParser.color_codes["blue"]}FF]"
    MAGENTA = fr"\eGC[{JSONtoTextParser.color_codes["magenta"]}FF]\eCC[{JSONtoTextParser.color_codes["magenta"]}FF]"
    CYAN = fr"\eGC[{JSONtoTextParser.color_codes["cyan"]}FF]\eCC[{JSONtoTextParser.color_codes["cyan"]}FF]"
    SLATEBLUE = fr"\eGC[{JSONtoTextParser.color_codes["slateblue"]}FF]\eCC[{JSONtoTextParser.color_codes["slateblue"]}FF]"
    PLUM = fr"\eGC[{JSONtoTextParser.color_codes["plum"]}FF]\eCC[{JSONtoTextParser.color_codes["plum"]}FF]"
    SALMON = fr"\eGC[{JSONtoTextParser.color_codes["salmon"]}FF]\eCC[{JSONtoTextParser.color_codes["salmon"]}FF]"
    WHITE = fr"\eGC[{JSONtoTextParser.color_codes["white"]}FF]\eCC[{JSONtoTextParser.color_codes["white"]}FF]"
    ORANGE = fr"\eGC[{JSONtoTextParser.color_codes["orange"]}FF]\eCC[{JSONtoTextParser.color_codes["orange"]}FF]"


class LMDisplayQueue:

    trap_link_msgs: list[str]
    ring_link_msgs: list[str]
    items_received: list[NetUtils.NetworkItem]
    lm_ctx: "LMContext"
    logger: Logger


    def __init__(self, ctx: "LMContext"):
        r"""There is some custom code injected into LM that allows us to display any text we want in game.
        There is a note that there is at max 286 bytes per line, 10 lines total (can be any amount)
        Lines are indicated by line breaks (\n) and can be anywhere, regardless of character count.
        To change colors, you will need to use the tags '\eGC[RRGGBBAA]\eCC[RRGGBBAA]', where its RGB + Alpha
        Alpha is unused in these lines, so we can set it to whatever static value we want, does not matter.
        \eGC[RRGGBBAA]\eCC[RRGGBBAA] takes up 26 characters on its own.
        Example line: \eGC[FF0000FF]\eCC[FF0000FF]Sample Red Tex here\n"""
        self.ring_link_msgs = []
        self.ring_link_msgs = []
        self.items_received = []
        self.lm_ctx = ctx
        self.logger = getLogger(CLIENT_NAME)


    async def display_in_game(self):
        try:
            while self.lm_ctx.slot:
                if not (self.lm_ctx.check_ingame() and self.lm_ctx.check_alive()):
                    await self.lm_ctx.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                    continue

                await self._check_items_display_queue()
                await self.lm_ctx.wait_for_next_loop(WAIT_TIMER_MEDIUM_TIMEOUT)
        except Exception as genericEx:
            self.logger.error("While trying to display text in game, an unknown issue occurred. Details: " + str(genericEx))

    async def _check_items_display_queue(self):
        """Displays the Received item details in game."""
        while self.items_received:
            display_item = self.items_received.pop(0)
            text_to_display: list[bytes] = []

            # Get the Received Item Name to Display
            lm_item_name = self.lm_ctx.item_names.lookup_in_game(display_item.item).replace("&", "")
            lm_item_class = ItemClassification(display_item.flags).name
            if not lm_item_class is None:
                lm_item_class = lm_item_class.lower()

            # Display the item name based on the associated Item Classification.
            lm_item_str: str = ""
            match lm_item_class:
                case "progression":
                    lm_item_str = DisplayColors.PLUM + lm_item_name
                case "useful":
                    lm_item_str = DisplayColors.BLUE + lm_item_name
                case "trap":
                    lm_item_str = DisplayColors.SALMON + lm_item_name
                case "filler":
                    lm_item_str = DisplayColors.CYAN + lm_item_name
                case _:
                    lm_item_str = DisplayColors.WHITE + lm_item_name
            text_to_display.append(string_to_bytes(lm_item_str, None))

            # Get Received Player's name
            if display_item.player == self.lm_ctx.slot:
                received_line: str = DisplayColors.WHITE + "Found by " + DisplayColors.MAGENTA + "You"
            else:
                sent_player: str = self.lm_ctx.player_names[display_item.player]
                received_line: str = DisplayColors.WHITE + "Found by " + DisplayColors.MAGENTA + sent_player
            text_to_display.append(string_to_bytes(received_line, None))

            # Look up the location name based on the item's player attached.
            if display_item.player == self.lm_ctx.slot:
                loc_name_retr = self.lm_ctx.location_names.lookup_in_game(display_item.location)
            else:
                loc_name_retr = self.lm_ctx.location_names.lookup_in_slot(display_item.location, display_item.player)

            # Get the Received Player's Location Name who found the name
            loc_name_disp = (
                        DisplayColors.GREEN + f"from Location: ({loc_name_retr[:MAX_LOCATION_CHARS].replace("&", "")})")
            text_to_display.append(string_to_bytes(loc_name_disp, None))

            # Get the proper AP Game Name
            if display_item.player == 0:
                recv_text: str = DisplayColors.SALMON + "From the AP Server"
                text_to_display.append(string_to_bytes(recv_text, None))
            elif display_item.player != self.lm_ctx.slot:
                recv_text: str = DisplayColors.SALMON + "in "
                recv_text += self.lm_ctx.slot_info[display_item.player].game.replace("&", "")
                text_to_display.append(string_to_bytes(recv_text, None))

            screen_text: bytes = await _build_msg(text_to_display)
            await self._write_to_screen(screen_text)


    async def _write_to_screen(self, msg_to_write: bytes):
        """Writes the provided message on screen with the associated folors"""
        recv_timer_on_screen: int = 105 # 3.5 Seconds
        item_display_addr: int = 0x80338FC4
        item_timer_addr: int = int(self.lm_ctx.lm_dynamic_addr.dynamic_addresses["Client"]["gItem_Information_Timer"], 16)
        frame_avg_count: int = 30

        dme.write_bytes(item_display_addr, msg_to_write)
        dme.write_word(item_timer_addr, recv_timer_on_screen)
        await self.lm_ctx.wait_for_next_loop(recv_timer_on_screen / frame_avg_count)
        while dme.read_byte(item_timer_addr) > 0:
            await self.lm_ctx.wait_for_next_loop(WAIT_TIMER_SHORT_TIMEOUT)

        # Reset the screen size to avoid old text from being written
        dme.write_bytes(item_display_addr, b"\00" * len(msg_to_write))
        await self.lm_ctx.wait_for_next_loop(WAIT_TIMER_SHORT_TIMEOUT)


async def _build_msg(msg_parts: list[bytes]) -> bytes:
    """Builds a pre-formatted list that will be displayed on the screen.
    Automatically cuts off after the byte limit is reached."""
    if msg_parts is None or len(msg_parts) == 0:
        return b'\00'

    built_msg: bytes = "\n".encode("utf-8").join(msg_parts)[:MAX_DISPLAYED_CHARS]
    return built_msg.replace(b"\\eCC", b"\x1BCC").replace(b"\\eGC", b"\x1BGC") + b"\00"