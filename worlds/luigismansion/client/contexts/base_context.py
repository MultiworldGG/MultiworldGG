""" Base context for Luigi's Mansion's game tab in the client. """

# Python related imports
import asyncio, random, copy

# AP related imports
import Utils

apname = Utils.instance_name if Utils.instance_name else "Archipelago"

# Relative related imports
from .universal_context import UniversalContext, UniversalCommandProcessor, logger
from ..links.network_engine import ArchipelagoNetworkEngine
from ..links.energy_link.energy_link_client import EnergyLinkClient
from ..links.trap_link import TrapLink
from ..links.ring_link import RingLink
from ..links.link_base import LinkBase
from ..wallet import Wallet
from ...client.constants import *
from ...Hints import ALWAYS_HINT, PORTRAIT_HINTS

# 3rd Party related imports
import dolphin_memory_engine as dme


# Handles when Luigi says "Mario" in game.
LUIGI_SHOUT_ADDR = 0x804EB558
LUIGI_SHOUT_DURATION = 3 # Time in seconds of how long the mario shout lasts.
LUIGI_SHOUT_RAMVALUE = 0xBCB84ED4
LUIGI_SHOUT_LIST = ["Mario?", "Marrrio", "MARIO!", "MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARIOOOOOOOOOOOOOOOOOOOO"]

class BaseContext(UniversalContext):

    network_engine: ArchipelagoNetworkEngine
    wallet: Wallet
    energy_link: EnergyLinkClient
    trap_link: TrapLink
    ring_link: RingLink
    call_mario: bool = False
    yelling_in_client: bool = False
    self_item_messages: int = None
    hints = None
    portrait_hints: bool = None
    hint_dict: dict[str, int] = None

    def __init__(self, server_address, password):
        """
        Initialize the Luigi's Mansion Universal Context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        super().__init__(server_address, password)
        self.network_engine = ArchipelagoNetworkEngine(self)
        self.wallet = Wallet()
        self.trap_link = TrapLink(self.network_engine)
        self.ring_link = RingLink(self.network_engine, self.wallet)
        self.energy_link = EnergyLinkClient(self.network_engine, self.wallet)
        self.already_fired_events = False

    async def wait_for_next_loop(self, time_to_wait: float):
        await asyncio.sleep(time_to_wait)
    
    def on_connected(self, args):
        tags: list[str] = []
        if _check_tag(self.trap_link, self.network_engine, args):
            tags.append(self.trap_link.friendly_name)
        if _check_tag(self.ring_link, self.network_engine, args):
            tags.append(self.ring_link.friendly_name)
        if len(tags) > 0:
            Utils.async_start(self.network_engine.update_client_tags_async(tags), name="UpdateClientTags")

        self.trap_link.on_connected(args)
        self.ring_link.on_connected(args)

        # Argument related slot data
        slot_data = args["slot_data"]
        self.call_mario = bool(slot_data["call_mario"])
        self.self_item_messages = int(slot_data["self_item_messages"])
        self.portrait_hints = bool(slot_data["portrait_hints"])
        self.hints = slot_data["hints"]

        self.hint_dict = copy.deepcopy(ALWAYS_HINT)
        # If portrait ghost hints are on, check them too
        if self.portrait_hints:
            self.hint_dict.update(PORTRAIT_HINTS)

    def make_gui(self):
        # Performing local import to prevent additional UIs to appear during the patching process.
        # This appears to be occurring if a spawned process does not have a UI element when importing kvui/kivymd.
        from .lm_tab import build_gui, GameManager, MDLabel, MDLinearProgressIndicator

        ui: type[GameManager] = super().make_gui()
        ui.important_labels = {}
        class LMGuiWrapper(ui):
            wallet_ui: MDLabel
            boo_count: MDLabel
            wallet_progress_bar: MDLinearProgressIndicator
            base_title = f"Luigi's Mansion {CLIENT_VERSION}"

            def build(self):
                container = super().build()

                self.base_title += f" | {apname}"
                build_gui(self)

                return container

            def get_wallet_value(self):
                current_worth = 0
                total_worth = self.ctx.wallet.get_rank_requirement()

                if self.ctx.check_ingame():
                    current_worth = self.ctx.wallet.get_wallet_worth()

                self.wallet_ui.text = f"{format(current_worth, ',d')} / Required Money: {format(total_worth, ',d')}"
                if total_worth != 0:
                    self.wallet_progress_bar.value = current_worth / total_worth
                else:
                    self.wallet_progress_bar.value = 100

            def update_boo_count_label(self, item_count: int):
                boo_total = 50
                self.boo_count.text = f"{item_count} / {boo_total}"
                self.boo_progress_bar.value = item_count / boo_total

            def update_flower_label(self, count: int):
                self.flower_label.text = f"{count}"

            def update_vacuum_label(self, item_count: int):
                self.vacuum_label.text = f"{item_count}"

            def update_king_boo_label(self, count: int):
                self.king_boo_label.text = f"{count}"

            def update_balcony_boo_label(self, count: int):
                self.balcony_boo_label.text = f"{count}"

        return LMGuiWrapper

    async def handle_ringlink_async(self):
        await self.ring_link.handle_ring_link_async()

    async def lm_send_hints(self):
        # If the hint address is empty, no hint has been looked at and we return
        current_hint = int.from_bytes(dme.read_bytes(0x803D33AC, 1))
        if not current_hint > 0:
            return

        # Check for current room so we know which hint(s) we need to look at, since they mostly all use the same flags
        current_room = dme.read_word(dme.follow_pointers(ROOM_ID_ADDR, [ROOM_ID_OFFSET]))
        if current_room == 73:
            return
        player_id = 0
        location_id = 0

        # Go through all the hints to check which hint matches the room we are in
        for hint, hintfo in self.hints.items():
            if current_room != self.hint_dict[hint]:
                continue

            # If we match in room 53 or 59, figure out which flag is on and use the matching hint
            if current_room in (59, 53):
                if current_room == 59:
                    if (current_hint & (1 << 5)) > 0 and hint == "<doll1>":
                        player_id = int(hintfo["Send Player ID"])
                        location_id = int(hintfo["Location ID"])
                    elif (current_hint & (1 << 6)) > 0 and hint == "<doll2>":
                        player_id = int(hintfo["Send Player ID"])
                        location_id = int(hintfo["Location ID"])
                    elif (current_hint & (1 << 7)) > 0 and hint == "<doll3>":
                        player_id = int(hintfo["Send Player ID"])
                        location_id = int(hintfo["Location ID"])
                    else:
                        continue
                else:
                    if (current_hint & (1 << 5)) > 0 and hint == "Left Telephone":
                        player_id = int(hintfo["Send Player ID"])
                        location_id = int(hintfo["Location ID"])
                    elif (current_hint & (1 << 6)) > 0 and hint == "Center Telephone":
                        player_id = int(hintfo["Send Player ID"])
                        location_id = int(hintfo["Location ID"])
                    elif (current_hint & (1 << 7)) > 0 and hint == "Right Telephone":
                        player_id = int(hintfo["Send Player ID"])
                        location_id = int(hintfo["Location ID"])
                    else:
                        continue
            else:
                player_id = int(hintfo["Send Player ID"])
                location_id = int(hintfo["Location ID"])

            # Make sure we didn't somehow try to send a null hint
            if player_id == 0 or location_id == 0:
                logger.error("Hint incorrectly parsed in lm_send_hints while trying to send. " +
                             "Please inform the Luigi's mansion developers")
                Utils.messagebox("Hint Error",
                                 f"Hint incorrectly parsed in lm_send_hints while trying to send. " +
                                 "Please inform the Luigi's mansion developers" +
                                 f"Location_ID:" + str({location_id}) + " player_id:" + str({player_id}))

            # Send correct CreateHints command
            Utils.async_start(self.send_msgs([{
                "cmd": "CreateHints",
                "player": player_id,
                "locations": [location_id],
            }]))

    async def check_mario_yell(self):
        # Prevents the console from receiving the same message over and over.
        if not self.yelling_in_client:
            luigi_shouting = dme.read_word(LUIGI_SHOUT_ADDR)
            if luigi_shouting == LUIGI_SHOUT_RAMVALUE:
                self.yelling_in_client = True
                Utils.async_start(yell_in_client(self), name="Luigi Is Yelling")

def _check_tag(link: LinkBase, network_engine: ArchipelagoNetworkEngine, args) -> bool:
    slot_data = args["slot_data"]
    return link.slot_name in slot_data and slot_data[link.slot_name] == 1 and link.friendly_name not in network_engine.get_tags()

async def yell_in_client(ctx: BaseContext) -> None:
    logger.info(random.choice(LUIGI_SHOUT_LIST))
    await ctx.wait_for_next_loop(LUIGI_SHOUT_DURATION)
    ctx.yelling_in_client = False
    return


class BaseCommandProcessor(UniversalCommandProcessor):
    def __init__(self, ctx: BaseContext, server_address: str = None):
        if server_address:
            ctx.server_address = server_address
        super().__init__(ctx)

    def _cmd_traplink(self):
        """Toggle traplink from client. Overrides default setting."""
        if isinstance(self.ctx, BaseContext):
            Utils.async_start(self.ctx.network_engine.update_tags_async(not self.ctx.trap_link.is_enabled(),
                "TrapLink"), name="Update Traplink")

    def _cmd_ringlink(self):
        """Toggle traplink from client. Overrides default setting."""
        if isinstance(self.ctx, BaseContext):
            Utils.async_start(self.ctx.network_engine.update_tags_async(not self.ctx.ring_link.is_enabled(),
                "RingLink"), name="Update RingLink")

    def _cmd_ringlink_msg(self):
        """ Toggles RingLink messages being displayed in the client."""
        if isinstance(self.ctx, BaseContext):
            self.ctx.ring_link.set_logs(not self.ctx.ring_link.enable_logger)
            _log_msg_status_to_client(self.ctx.ring_link)

    def _cmd_traplink_msg(self):
        """ Toggles TrapLink messages being displayed in the client."""
        if isinstance(self.ctx, BaseContext):
            self.ctx.trap_link.set_logs(not self.ctx.trap_link.enable_logger)
            _log_msg_status_to_client(self.ctx.trap_link)

def _log_msg_status_to_client(link_base: LinkBase):
    is_enabled: str = "disabled"
    if link_base.enable_logger:
        is_enabled = "enabled"
    logger.info("%s client logs are now %s.", link_base.friendly_name,  is_enabled)
