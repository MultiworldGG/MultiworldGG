""" Manages TrapLink interactions between Luigi's Mansion Client and the Archipelago Server. """

import logging
import dolphin_memory_engine as dme

from ..constants import AP_LOGGER_NAME
from .network_engine import ArchipelagoNetworkEngine, TrapNetworkRequest
from .link_base import LinkBase
from ...Items import *
from enum import Flag

logger = logging.getLogger(AP_LOGGER_NAME)

class TrapLinkConstants:
    """
    Constants for internal and public facing energy link names.
    """
    FRIENDLY_NAME = "TrapLink"
    SLOT_NAME = "trap_link"

class SlotDataConstants:
    DISABLED_TRAPS = "disabled_traps"
    ENABLE_LOGGER = "enable_trap_client_msg"
    SLOT_DATA = "slot_data"

class TrapLinkType(Flag):
    """ A flag collection of Trap types supported in Luigi's Mansion. """
    NONE = 0
    POISON = 1
    ICE = 2
    BANANA = 4
    POSSESSION = 8
    BONK = 16
    GHOST = 32
    FEAR = 64
    BOMB = 128
    SPOOKY = 256
    SQUASH = 512
    NOVAC = 1024

class TrapLink(LinkBase):
    """ Manages interactions between Luigi's Mansion Client, emulator, and Archipelago server. """
    received_trap: str = ""
    # We want to ignore traps if the player set the trap weight to 0.
    disabled_trap_flags: TrapLinkType = TrapLinkType.NONE

    def __init__(self, network_engine: ArchipelagoNetworkEngine):
        super().__init__(friendly_name=TrapLinkConstants.FRIENDLY_NAME, slot_name=TrapLinkConstants.SLOT_NAME,
            network_engine=network_engine)

    async def handle_traplink_async(self):
        """ Manages remote Traps being sent to Luigi's Mansion. """
        if self.received_trap:
            lm_item = ALL_ITEMS_TABLE[self.received_trap]
            for addr_to_update in lm_item.update_ram_addr:
                byte_size = 1 if addr_to_update.ram_byte_size is None else addr_to_update.ram_byte_size
                curr_val = addr_to_update.item_count
                if addr_to_update.pointer_offset is not None:
                    dme.write_bytes(dme.follow_pointers(addr_to_update.ram_addr,
                        [addr_to_update.pointer_offset]), curr_val.to_bytes(byte_size, 'big'))
                else:
                    dme.write_bytes(addr_to_update.ram_addr, curr_val.to_bytes(byte_size, 'big'))
            self.received_trap = ""

    async def send_trap_link_async(self, trap_name: str):
        """
        Sends a Trap to the Archipelago server.

        :param trap_name: Friendly name of the trap being set.
        """
        if not self.is_enabled() or self.network_engine.get_slot() is None:
            return

        await self.network_engine.send_trap_link_request_async(
            TrapNetworkRequest(tags=[ TrapLinkConstants.FRIENDLY_NAME ],
            trap_name=trap_name))

    def check_vac_trap_active(self, vac_trap_address: int) -> bool:
        is_trap_active: int = int.from_bytes(dme.read_bytes(vac_trap_address, 4), signed=True)
        return is_trap_active != -1

    def on_bounced(self, args, vac_count: int):
        """
        Performs traplink operations during the 'Bounced' command in `on_package`.
        
        :param args: The arguments to be passed into the 'Bounced' command.
        :param vac_count: Amount of vacuums the player currently has, which indicates if the player needs
        """
        if not self.is_enabled():
            return

        data = args["data"]
        source_name = data["source"]
        # if the traplink tag is not present in the client's available tags, and if traplink isn't available in the args tags,
            # and lastly if the source of the trap was local (slot name matches current client's slot name) we don't want to send a trap
        if TrapLinkConstants.FRIENDLY_NAME in args["tags"] and source_name != self.network_engine.get_player_name(self.network_engine.get_slot()):
            trap_name: str = data["trap_name"]
            if trap_name not in ACCEPTED_TRAPS:
                return

            if trap_name in ICE_TRAP_EQUIV:
                _receive_weighted_trap(self, "Ice Trap", TrapLinkType.ICE)
            elif trap_name in BOMB_EQUIV:
                _receive_weighted_trap(self, "Bomb", TrapLinkType.BOMB)
            elif trap_name in BANANA_TRAP_EQUIV:
                _receive_weighted_trap(self, "Banana Trap", TrapLinkType.BANANA)
            elif trap_name in GHOST_EQUIV:
                _receive_weighted_trap(self, "Ghost", TrapLinkType.GHOST)
            elif trap_name in POISON_MUSH_EQUIV:
                _receive_weighted_trap(self, "Poison Mushroom", TrapLinkType.POISON)
            elif trap_name in BONK_EQUIV:
                _receive_weighted_trap(self, "Bonk Trap", TrapLinkType.BONK)
            elif trap_name in POSSESION_EQUIV:
                _receive_weighted_trap(self, "Possession Trap", TrapLinkType.POSSESSION)
            elif trap_name in FEAR_EQUIV:
                _receive_weighted_trap(self, "Fear Trap", TrapLinkType.FEAR)
            elif trap_name in SPOOKY_EQUIV:
                _receive_weighted_trap(self, "Spooky Time", TrapLinkType.SPOOKY)
            elif trap_name in SQUASH_EQUIV:
                _receive_weighted_trap(self, "Squash Trap", TrapLinkType.SQUASH)
            elif trap_name in NOVAC_EQUIV:
                if vac_count > 0:
                    _receive_weighted_trap(self, "No Vac Trap", TrapLinkType.NOVAC)

    def on_connected(self, args):
        """
        Performs traplink operations during the 'Connected' command in `on_package`.
        
        :param args: The arguments to be passed into the 'Connected' command.
        """
        slot_data = args[SlotDataConstants.SLOT_DATA]
        # The flags are cast to an int when sent to the server, so they need to be cast back to the enum.
        if SlotDataConstants.DISABLED_TRAPS not in slot_data:
            logger.debug("Internal setting 'disabled_traps' not found, zero weighted traps will still be sent to the client.")
        else:
            self.disabled_trap_flags = TrapLinkType(slot_data[SlotDataConstants.DISABLED_TRAPS])
            logger.debug("The following traps will not trigger when Trap Link is enabled: %s.", self.disabled_trap_flags)
        self.enable_logger = bool(slot_data[SlotDataConstants.ENABLE_LOGGER])

def _receive_weighted_trap(trap_link: TrapLink, trap_name: str, trap_type: TrapLinkType):
    if trap_type not in trap_link.disabled_trap_flags:
        trap_link.received_trap = trap_name
        if trap_link.enable_logger:
            logger.info("%s: Receiving trap %s.", TrapLinkConstants.FRIENDLY_NAME, trap_name)
    else:
        if trap_link.enable_logger:
            logger.info("%s: Ignoring trap %s because weight is zero.", TrapLinkConstants.FRIENDLY_NAME, trap_name)
