import logging
import pkgutil
import random

import orjson

import Utils
import time

from BaseClasses import ItemClassification
from NetUtils import ClientStatus, NetworkItem

from typing import TYPE_CHECKING, Optional, Dict, Set, ClassVar, Any, Tuple, Union

import worlds._bizhawk as bizhawk

from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor
#else:
    #BizHawkClientContext = object

from .ItemHandlers import ApeEscapeMemoryInput, StunTrapHandler, MonkeyMashHandler, RainbowCookieHandler, \
    CameraRotateHandler
from .Strings import AEItem, AEDoor, AELocation, DS_Options, DS_ButtonAndDoors, Commands_Dict
from .Locations import cointable, hundoMonkeysCount, hundoCoinsCount, doorTransitions
from .Items import gadgetsValues, trap_name_to_value, trap_to_local_traps
from .RAMAddress import RAM
from .Options import GoalOption, RequiredTokensOption, TotalTokensOption, TokenLocationsOption, \
    LogicOption, InfiniteJumpOption, SuperFlyerOption, EntranceOption, KeyOption, ExtraKeysOption, CoinOption, \
    MailboxOption, LampOption, GadgetOption, ShuffleNetOption, ShuffleWaterNetOption, LowOxygenSounds, TrapPercentage, \
    ItemDisplayOption, KickoutPreventionOption, DeathLink, RandomizeStartingRoomOption, TrapLink, FastTokenGoalOption

EXPECTED_ROM_NAME = "ape escape / AP 2"

logger = logging.getLogger("Client")

def cmd_ae_commands(self: "BizHawkClientCommandProcessor") -> None:
    """Show what commands are available for Ape Escape Archipelago"""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Ape Escape":
        logger.warning("This command can only be used when playing Ape Escape.")
        return
    presetColors = list(RAM.colortable.keys())
    logger.info(f"----------------------------------------------\n"
                f"Commands for Ape Escape\n"
                f"----------------------------------------------\n"
                f"  /ae_commands\n"
                f"      Description: Show this list\n"
                f"  /bh_itemdisplay [On/Off]\n"
                f"      Description: Display items directly in the Bizhawk client\n"
                f"      [Optional] Status (On/Off): Toggle or Enable/Disable the option\n"
                f"  /prevent_kickout [On/Off]\n"
                f"      Description: If on, prevents Spike from being ejected \n"
                f"                    after catching all monkeys in a level\n"
                f"      [Optional] Status (On/Off): Toggle or Enable/Disable the option\n"
                f"  /deathlink [On/Off]\n"
                f"      Description: Enable/Disable the deathlink option\n"
                f"      [Optional] Status (On/Off): Toggle or Enable/Disable the option\n"
                f"  /auto_equip [On/Off]\n"
                f"      Description: When on, will equip gadgets if there is a free face button\n"
                f"      [Optional] Status (On/Off): Toggle or Enable/Disable the option\n"
                f"  /syncprogress \n"
                f"      Description: Fetch the server's state of monkeys and sync it into the game\n"
                f"      [Optional] \"cancel\": If prompted, cancel the currently pending sync\n"
                f"  /spikecolor \n"
                f"      Description: Display/Change Spike's color palette according to presets\n"
                f"      or RGB Hex values (\"000000\" to \"FFFFFF\")\n"
                f"      Presets: {presetColors}\n"
                f"  \n")


def cmd_bh_itemdisplay(self: "BizHawkClientCommandProcessor", status = "") -> None:
    """Toggle the item display in Bizhawk"""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Ape Escape":
        logger.warning("This command can only be used when playing Ape Escape.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return

    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, ApeEscapeClient)
    if status == "":
        if client.bhdisplay == 0:
            msg = "ON"
        else:
            msg = "OFF"
        logger.info(f"Bizhawk Item Display: {msg}\n"
                    f"    To change the status, use the command like so: /bh_itemdisplay [on/off]")
        return
    elif status.lower() == "on":
        client.bhdisplay = 1
    else:
        client.bhdisplay = 0
    client.changeBHDisplay = True
    if client.bhdisplay == 1:
        item_display = "ON"
        # client.send_bizhawk_message(ctx, "Bizhawk Item Display Enabled", "Passthrough", "")
    else:
        item_display = "OFF"
        # client.send_bizhawk_message(ctx, "Bizhawk Item Display Disabled", "Passthrough", "")
    client.BHDisplay_DS = client.bhdisplay
    logger.info(f"Bizhawk Item Display is now {item_display}\n")


def cmd_prevent_kickout(self: "BizHawkClientCommandProcessor", status = "") -> None:
    """Toggle Kickout Prevention on and off"""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Ape Escape":
        logger.warning("This command can only be used when playing Ape Escape.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return

    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, ApeEscapeClient)
    if status == "":
        if client.bhdisplay == 0:
            msg = "ON"
        else:
            msg = "OFF"
        logger.info(f"Kickout Prevention: {msg}\n"
                    f"    To change the status, use the command like so: /prevent_kickout [on/off]")
        return
    elif status.lower() == "on":
        client.preventKickOut = 1
    elif status.lower() == "off":
        client.preventKickOut = 0
    else:
        logger.info(f"Invalid argument for function ""prevent_kickout""\n")
        return
    # Replace slot_data
    # client.change_kickout_prevention(ctx)
    client.changeKickout = True
    if client.preventKickOut == 1:
        kickout = "ON"
        # client.send_bizhawk_message(ctx, "Kickout Prevention Enabled", "Custom", "")
    else:
        kickout = "OFF"
        # client.send_bizhawk_message(ctx, "Kickout Prevention Disabled", "Custom", "")
    client.KickoutPrevention_DS = client.preventKickOut
    logger.info(f"Kickout Prevention is now {kickout}\n")


def cmd_deathlink(self: "BizHawkClientCommandProcessor", status = "") -> None:
    """Toggle Deathlink on and off"""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Ape Escape":
        logger.warning("This command can only be used when playing Ape Escape.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return

    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, ApeEscapeClient)
    if status == "":
        if client.deathlink == 0:
            msg = "ON"
        else:
            msg = "OFF"
        logger.info(f"Deathlink: {msg}\n"
                    f"    To change the status, use the command like so: /deathlink [on/off]")
        return
    elif status.lower() == "on":
        client.deathlink = 1
    elif status.lower() == "off":
        client.deathlink = 0
    else:
        logger.info(f"Invalid argument for function ""deathlink""\n")
        return
    # Replace slot_data

    #client.change_kickout_prevention(ctx)
    client.changeDeathlink = True
    if client.deathlink == 1:
        Utils.async_start(ctx.update_death_link(True))
        msg = "ON"
        #client.send_bizhawk_message(ctx, "Deathlink Enabled", "Custom", "")
    else:
        Utils.async_start(ctx.update_death_link(False))
        msg = "OFF"
        #client.send_bizhawk_message(ctx, "Deathlink Disabled", "Custom", "")
    client.DeathLink_DS = client.deathlink

    logger.info(f"Deathlink is now {msg}\n")


def cmd_auto_equip(self: "BizHawkClientCommandProcessor", status = "") -> None:
    """Toggle Auto-Equip on and off"""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Ape Escape":
        logger.warning("This command can only be used when playing Ape Escape.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return

    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, ApeEscapeClient)
    if status == "":
        if client.autoequip == 0:
            msg = "ON"
        else:
            msg = "OFF"
        logger.info(f"Auto-Equip: {msg}\n"
                    f"    To change the status, use the command like so: /autoequip [on/off]")
        return
    elif status.lower() == "on":
        client.autoequip = 1
    elif status.lower() == "off":
        client.autoequip = 0
    else:
        logger.info(f"Invalid argument for function ""autoequip""\n")
        return
    # Replace slot_data

    #client.change_kickout_prevention(ctx)
    client.changeAutoEquip = True
    if client.autoequip == 1:
        msg = "ON"
        #client.send_bizhawk_message(ctx, "Automatic Gadget Equipping Enabled", "Custom", "")
    else:
        msg = "OFF"
        #client.send_bizhawk_message(ctx, "Automatic Gadget Equipping Disabled", "Custom", "")
    client.AutoEquip_DS = client.autoequip
    logger.info(f"Auto Equip is now {msg}\n")


def cmd_spikecolor(self: "BizHawkClientCommandProcessor", color = "") -> None:
    """Check or change Spike's color"""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Ape Escape":
        logger.warning("This command can only be used when playing Ape Escape.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return

    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, ApeEscapeClient)
    presetColors = list(RAM.colortable.keys())
    presetValues = list(RAM.colortable.values())
    if color == "":
        if client.DS_spikecolor == -2 or client.DS_spikecolor is None:
            # No datastorage, use slot_data
            try:
                spikecolor = presetColors[ctx.slot_data["spikecolor"]]
            except:
                # Should not go there, but No slot_data, use vanilla
                spikecolor = presetColors[0]
        else:
            # Custom
            if type(client.DS_spikecolor) is str or type(client.DS_spikecolor) is int:
                error = False
                try:
                    # Preset color name
                    spikecolor = presetColors[presetColors.index(str(client.DS_spikecolor))]
                except:
                    try:
                        # Preset color number
                        spikecolor = presetColors[presetValues.index(int(client.DS_spikecolor, 16))]
                    except:
                        # Preset color value
                        try:
                            print(f"DS_spikecolor_HEX: {int(format(client.DS_spikecolor, 'x'), 16)}")
                            spikecolor = presetColors[presetValues.index(int(format(client.DS_spikecolor, "x"), 16))]
                        except:
                            # Use custom color as given
                            spikecolor = client.DS_spikecolor
            else:
                # Custom but not recognised, setting to vanilla
                spikecolor = 0xFFFFFF
            try:
                spikecolor = format(int(spikecolor, 16), "x").upper()
            except:
                pass
        logger.info(f"Current Spike color: {spikecolor}\n"
                    f"    To change Spike's color, use the following command: /spikecolor [color]\n"
                    f"    Accepts RGB Hex values (\"000000\" to \"FFFFFF\") and preset values\n"
                    f"    Presets: {presetColors}\n")
        return
    elif color.lower() in presetColors:
        client.DS_spikecolor = str(presetColors[presetColors.index(color)])
    elif len(color) == 6:
        try:
            client.DS_spikecolor = format(int(color, 16), "x")
            color = color.upper()
        except:
            logger.info(f"Invalid argument for function ""color""\n")
            return
    else:
        logger.info(f"Invalid argument for function ""color""\n")
        return
    client.changeSkin = True
    logger.info(f"Spike color is now {color}\n")


def cmd_syncprogress(self: "BizHawkClientCommandProcessor", status = "") -> None:
    """Sync the game progress with the server (Monkeys and Coins)"""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Ape Escape":
        logger.warning("This command can only be used when playing Ape Escape.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, ApeEscapeClient)
    if status.lower() == "cancel":
        if client.syncWaitConfirm == True:
            logger.info(f"[---] Progress Sync canceled [---] ")
            client.syncWaitConfirm = False
        else:
            logger.info(f"[---] Use the command \"/syncprogress\" without an argument to start the sync [---] ")
        return
    elif status.lower() != "":
        logger.info(f"Wrong argument provided for command ""syncprogress""")
        return

    if client.syncWaitConfirm == False:
        logger.warning(f"\n[!!!] **WARNING** [!!!]\n"
                       f"    This action will **OVERWRITE YOUR LOCAL PROGRESS** with the server's state.\n"
                       f"    It will update all server-known locations,\n"
                       f"    marking monkeys as \"Caught\" and coins as \"Collected\".\n"
                       "     ***Use \"/syncprogress\" again to confirm, or \"/syncprogress cancel\" to cancel***\n")
        client.syncWaitConfirm = True
    else:
        client.syncWaitConfirm = False
        # Turn on the flag, the client will do the work
        client.boolsyncprogress = True

class ApeEscapeClient(BizHawkClient):
    game = "Ape Escape"
    system = "PSX"
    patch_suffix = ".apae"

    apworld_manifest = orjson.loads(pkgutil.get_data(__name__, "archipelago.json").decode("utf-8"))
    client_version = apworld_manifest["world_version"]
    #client_version = "0.9.1"

    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    local_found_key_items: Dict[str, bool]
    goal_flag: int

    offset = 128000000
    levelglobal = 0
    roomglobal = 0
    worldkeycount = 0
    tokencount = 0
    boss1flag = 0
    boss2flag = 0
    boss3flag = 0
    boss4flag = 0
    lastenteredLevel = 0
    boolsyncprogress = False
    syncWaitConfirm = False
    countMonkeys = False
    changeKickout = False
    changeDeathlink = False
    changeAutoEquip = False
    changeBHDisplay = False
    KickoutPrevention_DS = -1
    DeathLink_DS = -1
    AutoEquip_DS = -1
    BHDisplay_DS = -1
    preventKickOut = -1
    deathlink = -1
    autoequip = -1
    bhdisplay = -1
    replacePunch = True
    currentCoinAddress = RAM.startingCoinAddress
    resetClient = False
    inWater = 0
    waternetState = 0
    watercatchState = 0
    bizhawk_itemdisplay = False
    bizhawk_display_set = False
    MM_Completed = False
    PPM_Completed = False
    gotDatastorage = False
    mailboxTextReplaced = False

    def __init__(self) -> None:
        super().__init__()
        self.ape_handler = MonkeyMashHandler(None)
        self.rainbow_cookie = RainbowCookieHandler(None)
        self.stun_trap = StunTrapHandler(None)
        self.camera_rotate_trap = CameraRotateHandler(None)
        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}

    def initialize_client(self):
        self.messagequeue = []
        self.currentCoinAddress = RAM.startingCoinAddress
        self.countMonkeys = False
        self.DS_spikecolor = -2
        self.changeSkin = False
        self.lastenteredLevel = 0
        self.boolsyncprogress = False
        self.syncWaitConfirm = False
        self.changeKickout = False
        self.changeDeathlink = False
        self.changeAutoEquip = False
        self.changeBHDisplay = False
        self.replacePunch = True
        self.killPlayer = True
        self.inWater = 0
        self.waternetState = 0
        self.watercatchState = 0
        self.death_counter = None
        self.previous_death_link = 0
        self.pending_death_link: bool = False
        self.locations_list = {}
        # default to true, as we don't want to send a deathlink until playing
        self.sending_death_link: bool = True
        self.ignore_next_death_link = False
        self.DIButton = 0
        self.CrCWaterButton = 0
        # self.CrCBasementButton = 0
        self.MM_Painting_Button = 0
        self.MM_MonkeyHead_Button = 0
        self.DR_Block_Pushed = 0
        self.TVT_Lobby_Button = 0
        self.bool_MMDoubleDoor = False
        self.bool_LampGlobal = False
        self.gotBanana = False
        self.lowOxygenCounter = 1
        self.specialitem_queue = []
        self.priority_trap_queue = []
        self.bizhawk_itemdisplay = False
        self.bizhawk_display_set = False
        self.gotDatastorage = False
        self.initDatastorage = False
        self.ForceTransition = False
        self.ChangeRoom = False
        self.ER_phase = 1
        self.allowcollect = 0
        self.forcecollect = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        ape_identifier_ram_address: int = 0xA37F0
        ape_identifier_ram_address_PAL: int = 0xA37F0
        # BASCUS-94423SYS in ASCII = Ape Escape
        bytes_expected: bytes = bytes.fromhex("4241534355532D3934343233535953")
        bytes_expected_PAL:bytes = bytes.fromhex("4245534345532D3031353634535953")
        Commands_List = list(Commands_Dict.keys())
        try:
            bytes_actual: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                ape_identifier_ram_address, len(bytes_expected), "MainRAM"
            )]))[0]
            if bytes_actual != bytes_expected:
                # Remove commands from client from list in Strings.py
                for command in Commands_List:
                    if command in ctx.command_processor.commands:
                        ctx.command_processor.commands.pop(command)
                return False
        except Exception:
            # Remove commands from client from list in Strings.py
            for command in Commands_List:
                if command in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop(command)
            return False

        if not self.game == "Ape Escape":
            # Remove commands from client from list in Strings.py
            for command in Commands_List:
                if command in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop(command)
            return False
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        # Add custom commands to client from list in Strings.py
        for command in Commands_List:
            if command not in ctx.command_processor.commands:
                functionName = Commands_Dict[command]
                linkedfunction = globals()[functionName]
                ctx.command_processor.commands[command] = linkedfunction
        self.initialize_client()

        return True


    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Connected":
            logger.info(f"================================================\n"
                        f"    -- Connected to Bizhawk successfully! --    \n"
                        f"      Archipelago Ape Escape version {self.client_version}      \n"
                        f"================================================\n"
                        f"Custom commands are available for this game.    \n"
                        f"Type /ae_commands for the full list.            \n"
                        f"================================================\n")
            self.initialize_client()
        if cmd == "Bounced":
            if "tags" in args:
                assert ctx.slot is not None
                source_name = args["data"]["source"]
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.on_deathlink(ctx)
                if "TrapLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    trap_name: str = args["data"]["trap_name"]

                    if trap_name not in trap_to_local_traps:
                        # We don't know how to handle this trap, ignore it
                        return

                    local_trap_name: str = trap_to_local_traps.get(trap_name)
                    #print(local_trap_name)
                    trap_value: int = trap_name_to_value.get(local_trap_name)

                    if "trapweights" not in ctx.slot_data:
                        #print("option not in slotdata")
                        return

                    if local_trap_name not in ctx.slot_data["trapweights"]:
                        # This trap is not in the list, ignore it
                        # *Version mismatch or partial YAML*
                        #print("Not in list")
                        return

                    if ctx.slot_data["trapweights"][f"{local_trap_name}"] == 0:
                        # The player disabled this trap type
                        #print("Trap disabled by the player")
                        return

                    message = f"Received linked {trap_name} from {source_name}"
                    logger.info(message)
                    self.priority_trap_queue.insert(0,[trap_value,time.time()])
                    Utils.async_start(self.send_bizhawk_message(ctx,message,"Passthrough", ""))

        if cmd in {"PrintJSON"} and "type" in args:
            # When a message is received
            if args["type"] == "ItemSend":
                item = args["item"]
                networkItem = NetworkItem(*item)
                recieverID = args["receiving"]
                senderID = networkItem.player
                locationID = networkItem.location
                relevant = (recieverID == ctx.slot or senderID == ctx.slot)
                message = ""
                itemName = ctx.item_names.lookup_in_slot(networkItem.item, recieverID)
                itemCategory = networkItem.flags
                if relevant:
                    if itemCategory == ItemClassification.progression + ItemClassification.useful:
                        itemClass = "Prog. Useful"
                    elif itemCategory == ItemClassification.progression + ItemClassification.trap:
                        itemClass = "Prog. Trap"
                    elif itemCategory == ItemClassification.useful + ItemClassification.trap:
                        itemClass = "Useful Trap"
                    elif itemCategory == ItemClassification.progression:
                        itemClass = "Progression"
                    elif itemCategory == ItemClassification.useful:
                        itemClass = "Useful"
                    elif itemCategory == ItemClassification.trap:
                        itemClass = "Trap"
                        if itemName not in ctx.slot_data["trapsonreconnect"] and recieverID == ctx.slot:
                            self.specialitem_queue.append([(networkItem.item - self.offset),0])
                    elif itemCategory == ItemClassification.filler:
                        itemClass = "Filler"
                    else:
                        itemClass = "Other"
                        # Should not happen anymore,except for rare occasions that items get the progressive_skip_balancing tag

                    recieverName = ctx.player_names[recieverID]
                    senderName = ctx.player_names[senderID]

                    if recieverID != ctx.slot and senderID == ctx.slot:
                        message = f"Sent '{itemName}' ({itemClass}) to {recieverName}"
                    elif recieverID == ctx.slot and senderID != ctx.slot:
                        message = f"Received '{itemName}' ({itemClass}) from {senderName}"
                    elif recieverID == ctx.slot and senderID == ctx.slot:
                        message =  f"You found your own '{itemName}' ({itemClass})"

                    self.messagequeue.append(message)
                # If there is a PRINTJSON which is sent by the player
                if "TrapLink" in ctx.tags and recieverID == ctx.slot and itemName in trap_name_to_value:
                    Utils.async_start(self.send_trap_link(ctx, itemName))
        if cmd == "Retrieved":
            if "keys" not in args:
                print(f"invalid Retrieved packet to ApeEscapeClient: {args}")
                return
            keys = dict(args["keys"])
            if f"AE_kickoutprevention_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.KickoutPrevention_DS = keys.get(f"AE_kickoutprevention_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            if f"AE_deathlink_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.DeathLink_DS = keys.get(f"AE_deathlink_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            if f"AE_autoequip_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.AutoEquip_DS = keys.get(f"AE_autoequip_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            if f"AE_bhdisplay_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.BHDisplay_DS = keys.get(f"AE_bhdisplay_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            if f"AE_DIButton_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.DIButton = keys.get(f"AE_DIButton_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            if f"AE_CrCWaterButton_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.CrCWaterButton = keys.get(f"AE_CrCWaterButton_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            # if f"AE_CrCBasementButton_{ctx.team}_{ctx.slot}" in args["keys"]:
            # self.CrCBasementButton = keys.get(f"AE_CrCBasementButton_{ctx.team}_{ctx.slot}", None)
            if f"AE_MM_Painting_Button_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.MM_Painting_Button = keys.get(f"AE_MM_Painting_Button_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            if f"AE_MM_MonkeyHead_Button_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.MM_MonkeyHead_Button = keys.get(f"AE_MM_MonkeyHead_Button_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            if f"AE_TVT_Lobby_Button_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.TVT_Lobby_Button = keys.get(f"AE_TVT_Lobby_Button_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            if f"AE_DR_Block_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.DR_Block_Pushed = keys.get(f"AE_DR_Block_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            if f"AE_spikecolor_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.DS_spikecolor = keys.get(f"AE_spikecolor_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True

    async def check_gadgets(self, ctx: "BizHawkClientContext",gadgetStateFromServer) -> list[str]:
        gadgets = []
        gadgetsDict = {
            1: AEItem.Club.value,
            2: AEItem.Net.value,
            4: AEItem.Radar.value,
            8: AEItem.Sling.value,
            16: AEItem.Hoop.value,
            32: AEItem.Punch.value,
            64: AEItem.Flyer.value,
            128: AEItem.Car.value
        }
        for gadget in gadgetsDict.items():
            if gadgetStateFromServer & gadget[0] != 0:
                gadgets.append(gadget[1])
        return gadgets


    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        x = 3

    async def ds_options_handling(self, ctx: "BizHawkClientContext", context):
        if context == "init":
            if ctx.team is None:
                self.initDatastorage = False
                return
            keys = [f"AE_{Option}_{ctx.team}_{ctx.slot}" for Option in DS_Options]
            await ctx.send_msgs([{"cmd": "Get", "keys": keys}])

            if not self.gotDatastorage:
                return

            self.initDatastorage = True

            # Kickout Prevention
            if self.KickoutPrevention_DS is None:
                # Used slotdata
                self.preventKickOut = int(ctx.slot_data["kickoutprevention"])
            else:
                # Got valid Datastorage, take this instead of slot_data
                self.preventKickOut = self.KickoutPrevention_DS

            # Deathlink
            if self.DeathLink_DS is None:
                # Used slotdata
                self.deathlink = int(ctx.slot_data["death_link"])
            else:
                # Got valid Datastorage, take this instead of slot_data
                self.deathlink = self.DeathLink_DS

            # Auto Equip
            if self.AutoEquip_DS is None:
                # Used slotdata
                self.autoequip = int(ctx.slot_data["autoequip"])
                #self.AutoEquip_DS = self.autoequip
            else:
                # Got valid Datastorage, take this instead of slot_data
                self.autoequip = self.AutoEquip_DS

            # Bizhawk Item Display
            if self.BHDisplay_DS is None:
                # Used slotdata
                self.bhdisplay = int(ctx.slot_data["itemdisplay"])
                #self.BHDisplay_DS = self.bhdisplay
            else:
                # Got valid Datastorage, take this instead of slot_data
                self.bhdisplay = self.BHDisplay_DS

            loggermessage = "\n--Options Status--\n"
            loggermessage += f"Kickout Prevention: {"ON" if self.preventKickOut == 1 else "OFF"}\n"
            loggermessage += f"DeathLink: {"ON" if self.deathlink == 1 else "OFF"}\n"
            loggermessage += f"Auto-Equip: {"ON" if self.autoequip == 1 else "OFF"}\n"
            loggermessage += f"Bizhawk Item Display: {"ON" if self.bhdisplay == 1 else "OFF"}\n"
            logger.info(loggermessage)
        elif context == "change":
            if self.changeKickout:
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": f"AE_kickoutprevention_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": self.preventKickOut}],
                        }
                    ]
                )
                msg = f"Kickout Prevention {"Enabled" if self.preventKickOut == 1 else "Disabled"}"
                await self.send_bizhawk_message(ctx, msg, "Passthrough", "")
                self.changeKickout = False
            if self.changeDeathlink:
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": f"AE_deathlink_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": self.deathlink}],
                        }
                    ]
                )
                msg = f"Deathlink {"Enabled" if self.deathlink == 1 else "Disabled"}"
                await self.send_bizhawk_message(ctx, msg, "Passthrough", "")
                self.changeDeathlink = False
            if self.changeAutoEquip:
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": f"AE_autoequip_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": self.autoequip}],
                        }
                    ]
                )
                msg = f"Auto-Equip {"Enabled" if self.autoequip == 1 else "Disabled"}"
                await self.send_bizhawk_message(ctx, msg, "Passthrough", "")
                self.changeAutoEquip = False
            if self.changeBHDisplay:
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": f"AE_bhdisplay_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": self.bhdisplay}],
                        }
                    ]
                )
                msg = f"Bizhawk Item Display {"Enabled" if self.bhdisplay == 1 else "Disabled"}"
                await self.send_bizhawk_message(ctx, msg, "Passthrough", "")
                self.changeBHDisplay = False

    async def syncprogress(self, ctx: "BizHawkClientContext") -> None:
        if self.boolsyncprogress:
            self.forcecollect = True
            self.boolsyncprogress = False

    async def process_bizhawk_messages(self, ctx: "BizHawkClientContext") -> None:
        if self.bhdisplay == 1:
            for message in self.messagequeue:
                await self.send_bizhawk_message(ctx, message, "Custom", "")
                self.messagequeue.pop(0)
        else:
            self.messagequeue = []
    async def send_bizhawk_message(self, ctx: "BizHawkClientContext", message, msgtype, data) -> None:
        if self.bhdisplay == 1:
            # I'm now using a new message method, passing with ParseJSON instead.
            # It checks all the sender/receiver info and send a "Custom" message through this function

            if msgtype == "Custom":
                strMessage = message
                await bizhawk.display_message(ctx.bizhawk_ctx, strMessage)
            elif msgtype == "Passthrough":
                strMessage = message
                await bizhawk.display_message(ctx.bizhawk_ctx, strMessage)
        elif msgtype == "Passthrough":
            strMessage = message
            await bizhawk.display_message(ctx.bizhawk_ctx, strMessage)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:

        # Detects if the AP connection is made.
        # If not, "return" immediately to not send anything while not connected
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None or ctx.auth is None:
            self.initClient = False
            return
        # Detection for triggering "initialize_client()" when Disconnecting/Reconnecting to AP (only once per connection)
        if self.initClient == False:
            self.initClient = True
            self.initialize_client()
            await self.ds_options_handling(ctx,"init")
            await self.Spike_Color_handling(ctx, "", "init")

            strMessage = "Connected to Bizhawk Client - Ape Escape Archipelago v " + str(self.client_version)
            #logger.info(f"[INFO]{strMessage}")
            await self.send_bizhawk_message(ctx, strMessage, "Passthrough", "")
        try:
            if self.gotDatastorage:
                # Last init to write the status
                if not self.initDatastorage:
                    await self.ds_options_handling(ctx, "init")
                    await self.Spike_Color_handling(ctx, "", "init")

                if  self.changeKickout or self.changeDeathlink or self.changeAutoEquip or self.changeBHDisplay:
                    await self.ds_options_handling(ctx, "change")
                if self.boolsyncprogress:

                    await self.syncprogress(ctx)
            else:
                # Not send anything before having the options set
                await self.ds_options_handling(ctx, "init")
                await self.Spike_Color_handling(ctx, "", "init")

                return

            # Set locations list to use within functions
            self.locations_list = ctx.checked_locations

            if self.ape_handler.bizhawk_context is None:
                self.ape_handler = MonkeyMashHandler(ctx)

            if self.rainbow_cookie.bizhawk_context is None:
                self.rainbow_cookie = RainbowCookieHandler(ctx)

            if self.stun_trap.bizhawk_context is None:
                self.stun_trap = StunTrapHandler(ctx)

            if self.camera_rotate_trap.bizhawk_context is None:
                self.camera_rotate_trap = CameraRotateHandler(ctx)

            self.allowcollect = ctx.slot_data["allowcollect"]

            # Game state, locations and items read
            readsDict = {
                "recv_index": (RAM.lastReceivedArchipelagoID, 4, "MainRAM"),
                "gameState": (RAM.gameStateAddress, 1, "MainRAM"),
                "currentRoom": (RAM.currentRoomIdAddress, 1, "MainRAM"),  # Current Room
                "NearbyRoom": (RAM.Nearby_RoomIDAddress, 1, "MainRAM"),  # Nearby Room
                "currentLevel": (RAM.currentLevelAddress, 1, "MainRAM"),  # Current Level
                "gameRunning": (RAM.gameRunningAddress, 1, "MainRAM"),
                "jakeVictory": (RAM.jakeVictoryAddress, 1, "MainRAM"), # Jake Races Victory state
                "transitionPhase": (RAM.transitionPhaseAddress, 1, "MainRAM"),
                "Transition_Screen_Progress": (RAM.Transition_Screen_Progress, 1, "MainRAM"),
                "LoadingState": (RAM.LoadingState, 1, "MainRAM"),
                "localLevelState": (RAM.localLevelState, 1, "MainRAM"),
                # Locations (Coins, Monkeys, Mailboxes)
                "previousCoinStateRoom": (self.currentCoinAddress - 2, 1, "MainRAM"),  # Previous Coin State Room
                "currentCoinStateRoom": (self.currentCoinAddress, 1, "MainRAM"),  # Current New Coin State Room
                "coinCount": (RAM.totalCoinsAddress, 1, "MainRAM"),  # Coin Count
                "localhundoCount": (RAM.hundoApesAddress, 1, "MainRAM"),  # Hundo monkey count, to write to required count
                "requiredApes": (RAM.requiredApesAddress, 1, "MainRAM"),
                "currentApes": (RAM.currentApesAddress, 1, "MainRAM"),
                "gotMail": (RAM.gotMailAddress, 1, "MainRAM"),
                "mailboxID": (RAM.mailboxIDAddress, 1, "MainRAM"),
                # Items
                "energyChips": (RAM.energyChipsAddress, 1, "MainRAM"),
                "cookies": (RAM.cookieAddress, 1, "MainRAM"),
                "totalLives": (RAM.livesAddress, 1, "MainRAM"),
                "flashAmmo": (RAM.flashAddress, 1, "MainRAM"),
                "rocketAmmo": (RAM.rocketAddress, 1, "MainRAM"),
                "keyCountFromServer": (RAM.keyCountFromServer, 1, "MainRAM"),
                "tokenCountFromServer": (RAM.tokenCountFromServer, 1, "MainRAM"),
                # Misc
                "spikeState": (RAM.spikeStateAddress, 1, "MainRAM"),
                "spikeState2": (RAM.spikeState2Address, 1, "MainRAM"),
                "kickoutofLevel": (RAM.kickoutofLevelAddress, 4, "MainRAM"),
                "kickoutofLevel2": (RAM.kickoutofLevelAddress2, 4, "MainRAM"),
                "CrC_BossPhase": (RAM.CrC_BossPhaseAddress, 1, "MainRAM"),
                "CrC_BossLife": (RAM.CrC_BossLife, 1, "MainRAM"),
                "CrC_kickoutofLevel": (RAM.CrC_kickoutofLevelAddress, 4, "MainRAM"),
                "TVT_kickoutofLevel": (RAM.TVT_kickoutofLevelAddress, 4, "MainRAM"),
                "TVT_BossPhase": (RAM.TVT_BossPhase, 1, "MainRAM"),
                "TVT_BossLife": (RAM.TVT_BossLife, 1, "MainRAM"),
                "S1_P2_State": (RAM.S1_P2_State, 1, "MainRAM"),
                "S1_P2_Life": (RAM.S1_P2_Life, 1, "MainRAM"),
                "S2_isCaptured": (RAM.S2_isCaptured, 1, "MainRAM"),
                "S1_Cutscene_Redirection": (RAM.S1_Cutscene_Redirection, 4, "MainRAM"),
                "S2_Cutscene_Redirection": (RAM.S2_Cutscene_Redirection, 4, "MainRAM"),
                "S1_P1_FightTrigger": (RAM.S1_P1_FightTrigger, 1, "MainRAM"),
                "S2_CutsceneState": (RAM.S2_CutsceneState, 1, "MainRAM"),
                "S2_GlobalCutsceneState": (RAM.S2_GlobalCutsceneState, 1, "MainRAM"),
                "InputListener" : (RAM.InputListener, 1, "MainRAM"),
                "Warp_State" : (RAM.Warp_State, 1, "MainRAM"),
                "spikeColor": (RAM.spikeColor, 3, "MainRAM"),
                "Spike_X_Pos": (RAM.Spike_X_PosAddress, 4, "MainRAM"),
                "Spike_Y_Pos": (RAM.Spike_Y_PosAddress, 4, "MainRAM"),
                "Spike_Z_Pos": (RAM.Spike_Z_PosAddress, 4, "MainRAM"),
                "Spike_CanMove": (RAM.Spike_CanMove, 1, "MainRAM"),
                # Gadgets
                "gadgets": (RAM.unlockedGadgetsAddress, 1, "MainRAM"),  # Gadget unlocked states
                "gadgetStateFromServer": (RAM.gadgetStateFromServer, 2, "MainRAM"),
                "heldGadget": (RAM.heldGadgetAddress, 1, "MainRAM"),  # Currently held gadget
                "triangleGadget": (RAM.triangleGadgetAddress, 1, "MainRAM"),  # Gadget equipped to each face button
                "squareGadget": (RAM.squareGadgetAddress, 1, "MainRAM"),
                "circleGadget": (RAM.circleGadgetAddress, 1, "MainRAM"),
                "crossGadget": (RAM.crossGadgetAddress, 1, "MainRAM"),
                "gadgetUseState": (RAM.gadgetUseStateAddress, 1, "MainRAM"),  # Which gadget is used in what way. **Not used at the moment
                "punchVisualAddress": (RAM.punchVisualAddress, 32, "MainRAM"),
                "CatchingState": (RAM.CatchingState, 1, "MainRAM"),
                # Level Select/Menu data
                "LS_currentWorld": (RAM.selectedWorldAddress, 1, "MainRAM"),  # In level select, the current world
                "LS_currentLevel": (RAM.selectedLevelAddress, 1, "MainRAM"),  # In level select, the current level
                "status_currentWorld": (RAM.enteredWorldAddress, 1, "MainRAM"),  # After selecting a level, the entered world
                "status_currentLevel": (RAM.enteredLevelAddress, 1, "MainRAM"),  # After selecting a level, the entered level
                "menuState": (RAM.menuStateAddress, 1, "MainRAM"),
                "menuState2": (RAM.menuState2Address, 1, "MainRAM"),
                "newGameAddress": (RAM.newGameAddress, 1, "MainRAM"),
                # Level Select Coin hiding
                "CoinTable": (RAM.startingCoinAddress, 100, "MainRAM"),
                "TempCoinTable": (RAM.temp_startingCoinAddress, 100, "MainRAM"),
                "levelselect_coinlock_Address": (RAM.levelselect_coinlock_Address, 1, "MainRAM"),
                "SA_Completed": (RAM.SA_CompletedAddress, 1, "MainRAM"),
                "temp_SA_Completed": (RAM.temp_SA_CompletedAddress, 1, "MainRAM"),
                "GA_Completed": (RAM.GA_CompletedAddress, 1, "MainRAM"),
                "temp_GA_Completed": (RAM.temp_GA_CompletedAddress, 1, "MainRAM"),
                "worldIsScrollingRight": (RAM.worldIsScrollingRight, 2, "MainRAM"),
                "Specter1CompleteAddress": (RAM.Specter1CompleteAddress, 1, "MainRAM"),
                "Specter2CompleteAddress": (RAM.Specter2CompleteAddress, 1, "MainRAM"),
                # Water Net
                "canDive": (RAM.canDiveAddress, 4, "MainRAM"),
                "canWaterCatch": (RAM.canWaterCatchAddress, 1, "MainRAM"),
                "WaterNetStateFromServer": (RAM.tempWaterNetAddress, 1, "MainRAM"),
                "WaterCatchStateFromServer": (RAM.tempWaterCatchAddress, 1, "MainRAM"),
                "isUnderwater": (RAM.isUnderwater, 1, "MainRAM"),  # Underwater variable
                "swim_oxygenLevel": (RAM.swim_oxygenLevelAddress, 2, "MainRAM"),
                # Lamp Reads
                "CBLampStateFromServer": (RAM.tempCB_LampAddress, 1, "MainRAM"),
                "DILampStateFromServer": (RAM.tempDI_LampAddress, 1, "MainRAM"),
                "CrCLampStateFromServer": (RAM.tempCrC_LampAddress, 1, "MainRAM"),
                "CPLampStateFromServer": (RAM.tempCP_LampAddress, 1, "MainRAM"),
                "SFLampStateFromServer": (RAM.tempSF_LampAddress, 1, "MainRAM"),
                "TVTLobbyLampStateFromServer": (RAM.tempTVT_Lobby_LampAddress, 1, "MainRAM"),
                "TVTTankLampStateFromServer": (RAM.tempTVT_Tank_LampAddress, 1, "MainRAM"),
                "MMLampStateFromServer": (RAM.tempMM_LampAddress, 1, "MainRAM"),
                # Doors
                "MM_Lobby_DoubleDoor": (RAM.temp_MMLobbyDoorAddress, 1, "MainRAM"),
                "MM_Lobby_DoubleDoor_Open": (RAM.MM_Lobby_DoubleDoor_OpenAddress, 1, "MainRAM"),
                "MM_Jake_DefeatedAddress": (RAM.MM_Jake_DefeatedAddress, 1, "MainRAM"),
                "MM_Professor_RescuedAddress": (RAM.MM_Professor_RescuedAddress, 1, "MainRAM"),
                "MM_Clown_State": (RAM.MM_Clown_State, 1, "MainRAM"),
                "MM_Natalie_RescuedAddress": (RAM.MM_Natalie_RescuedAddress, 1, "MainRAM"),
                "MM_Jake_Defeated": (RAM.temp_MM_Jake_DefeatedAddress, 1, "MainRAM"),
                "MM_Professor_Rescued": (RAM.temp_MM_Professor_RescuedAddress, 1, "MainRAM"),
                "MM_Natalie_Rescued": (RAM.temp_MM_Natalie_RescuedAddress, 1, "MainRAM"),
                "MM_Natalie_Rescued_Local": (RAM.MM_Natalie_Rescued_Local, 1, "MainRAM"),
                "MM_Lobby_DoorDetection": (RAM.MM_Lobby_DoorDetection, 4, "MainRAM"),
                "WSW_RoomState": (RAM.WSW_RoomState, 1, "MainRAM"),
                "lockCamera": (RAM.lockCamera, 1, "MainRAM"),
                "MM_AlertRoom_ButtonPressed": (RAM.MM_AlertRoom_ButtonPressed, 1, "MainRAM"),
                # Buttons
                "DI_Button_Pressed": (RAM.DI_Button_Pressed, 1, "MainRAM"),
                "CrC_Water_ButtonPressed": (RAM.CrC_Water_ButtonPressed, 1, "MainRAM"),
                "CrC_Basement_ButtonPressed": (RAM.CrC_Basement_ButtonPressed, 1, "MainRAM"),
                "TVT_Lobby_ButtonPressed": (RAM.TVT_Lobby_Button, 1, "MainRAM"),
                "MM_MonkeyHead_ButtonPressed": (RAM.MM_MonkeyHead_Button, 1, "MainRAM"),
                "MM_Painting_ButtonPressed": (RAM.MM_Painting_Button, 1, "MainRAM"),
                "DR_Block_Pushed": (RAM.DR_Block_Pushed, 1, "MainRAM"),
                # MonkeyCounts
                "FF_MonkeyCount": (RAM.levelMonkeyCount[11], 1, "MainRAM"),
                "PO_MonkeyCount": (RAM.levelMonkeyCount[12], 1, "MainRAM"),
                "ML_MonkeyCount": (RAM.levelMonkeyCount[13], 1, "MainRAM"),
                "TJ_MonkeyCount": (RAM.levelMonkeyCount[21], 1, "MainRAM"),
                "DR_MonkeyCount": (RAM.levelMonkeyCount[22], 1, "MainRAM"),
                "CR_MonkeyCount": (RAM.levelMonkeyCount[23], 1, "MainRAM"),
                "SA_MonkeyCount": (RAM.levelMonkeyCount[31], 1, "MainRAM"),
                "CB_MonkeyCount": (RAM.levelMonkeyCount[41], 1, "MainRAM"),
                "CC_MonkeyCount": (RAM.levelMonkeyCount[42], 1, "MainRAM"),
                "DI_MonkeyCount": (RAM.levelMonkeyCount[43], 1, "MainRAM"),
                "SM_MonkeyCount": (RAM.levelMonkeyCount[51], 1, "MainRAM"),
                "FR_MonkeyCount": (RAM.levelMonkeyCount[52], 1, "MainRAM"),
                "HS_MonkeyCount": (RAM.levelMonkeyCount[53], 1, "MainRAM"),
                "GA_MonkeyCount": (RAM.levelMonkeyCount[61], 1, "MainRAM"),
                "ST_MonkeyCount": (RAM.levelMonkeyCount[71], 1, "MainRAM"),
                "WSW_MonkeyCount": (RAM.levelMonkeyCount[72], 1, "MainRAM"),
                "CRC_MonkeyCount": (RAM.levelMonkeyCount[73], 1, "MainRAM"),
                "CP_MonkeyCount": (RAM.levelMonkeyCount[81], 1, "MainRAM"),
                "SF_MonkeyCount": (RAM.levelMonkeyCount[82], 1, "MainRAM"),
                "TVT_MonkeyCount": (RAM.levelMonkeyCount[83], 1, "MainRAM"),
                "MM_MonkeyCount": (RAM.levelMonkeyCount[91], 1, "MainRAM")
            }

            readTuples = [Value for Value in readsDict.values()]

            reads = await bizhawk.read(ctx.bizhawk_ctx, readTuples)
            reads = [int.from_bytes(reads[i], byteorder = "little") for i,x in enumerate(reads)]
            readValues = dict(zip(readsDict.keys(), reads))

            # GameStates
            recv_index = readValues["recv_index"]
            gameState = readValues["gameState"]
            currentRoom = readValues["currentRoom"]
            NearbyRoom = readValues["NearbyRoom"]
            currentLevel = readValues["currentLevel"]
            gameRunning = readValues["gameRunning"]
            jakeVictory = readValues["jakeVictory"]
            transitionPhase = readValues["transitionPhase"]
            Transition_Screen_Progress = readValues["Transition_Screen_Progress"]
            LoadingState = readValues["LoadingState"]
            localLevelState = readValues["localLevelState"]
            # Locations
            previousCoinStateRoom = readValues["previousCoinStateRoom"]
            currentCoinStateRoom = readValues["currentCoinStateRoom"]
            coinCount = readValues["coinCount"]
            localhundoCount = readValues["localhundoCount"]
            requiredApes = readValues["requiredApes"]
            currentApes = readValues["currentApes"]
            gotMail = readValues["gotMail"]
            mailboxID = readValues["mailboxID"]
            # Items
            energyChips = readValues["energyChips"]
            cookies = readValues["cookies"]
            totalLives = readValues["totalLives"]
            flashAmmo = readValues["flashAmmo"]
            rocketAmmo = readValues["rocketAmmo"]
            keyCountFromServer = readValues["keyCountFromServer"]
            tokenCountFromServer = readValues["tokenCountFromServer"]
            # Misc
            spikeState = readValues["spikeState"]
            spikeState2 = readValues["spikeState2"]
            kickoutofLevel = readValues["kickoutofLevel"]
            kickoutofLevel2 = readValues["kickoutofLevel2"]
            CrC_BossPhase = readValues["CrC_BossPhase"]
            CrC_BossLife = readValues["CrC_BossLife"]
            CrC_kickoutofLevel = readValues["CrC_kickoutofLevel"]
            TVT_kickoutofLevel = readValues["TVT_kickoutofLevel"]
            TVT_BossPhase = readValues["TVT_BossPhase"]
            TVT_BossLife = readValues["TVT_BossLife"]
            S1_P2_State = readValues["S1_P2_State"]
            S1_P2_Life = readValues["S1_P2_Life"]
            S2_isCaptured = readValues["S2_isCaptured"]
            S1_Cutscene_Redirection = readValues["S1_Cutscene_Redirection"]
            S2_Cutscene_Redirection = readValues["S2_Cutscene_Redirection"]
            S1_P1_FightTrigger = readValues["S1_P1_FightTrigger"]
            S2_CutsceneState = readValues["S2_CutsceneState"]
            S2_GlobalCutsceneState = readValues["S2_GlobalCutsceneState"]
            InputListener = readValues["InputListener"]
            Warp_State = readValues["Warp_State"]
            spikeColor = readValues["spikeColor"]
            Spike_X_Pos = readValues["Spike_X_Pos"]
            Spike_Y_Pos = readValues["Spike_Y_Pos"]
            Spike_Z_Pos = readValues["Spike_Z_Pos"]
            Spike_CanMove = readValues["Spike_CanMove"]

            # Gadgets
            gadgets = readValues["gadgets"]
            gadgetStateFromServer = readValues["gadgetStateFromServer"]
            heldGadget = readValues["heldGadget"]
            triangleGadget = readValues["triangleGadget"]
            squareGadget = readValues["squareGadget"]
            circleGadget = readValues["circleGadget"]
            crossGadget = readValues["crossGadget"]
            gadgetUseState = readValues["gadgetUseState"]
            punchVisualAddress = readValues["punchVisualAddress"]
            CatchingState = readValues["CatchingState"]

            # Level Select/Menu data
            LS_currentWorld = readValues["LS_currentWorld"]
            LS_currentLevel = readValues["LS_currentLevel"]
            status_currentWorld = readValues["status_currentWorld"]
            status_currentLevel = readValues["status_currentLevel"]
            menuState = readValues["menuState"]
            menuState2 = readValues["menuState2"]
            newGameAddress = readValues["newGameAddress"]
            # Level Select Coin hiding
            CoinTable = readValues["CoinTable"]
            TempCoinTable = readValues["TempCoinTable"]
            levelselect_coinlock_Address = readValues["levelselect_coinlock_Address"]
            SA_Completed = readValues["SA_Completed"]
            temp_SA_Completed = readValues["temp_SA_Completed"]
            GA_Completed = readValues["GA_Completed"]
            temp_GA_Completed = readValues["temp_GA_Completed"]
            worldIsScrollingRight = readValues["worldIsScrollingRight"]
            Specter1CompleteAddress = readValues["Specter1CompleteAddress"]
            Specter2CompleteAddress = readValues["Specter2CompleteAddress"]

            # Water net shuffle
            canDive = readValues["canDive"]
            canWaterCatch = readValues["canWaterCatch"]
            WaterNetStateFromServer = readValues["WaterNetStateFromServer"]
            WaterCatchStateFromServer = readValues["WaterCatchStateFromServer"]
            isUnderwater = readValues["isUnderwater"]
            swim_oxygenLevel = readValues["swim_oxygenLevel"]

            CBLampStateFromServer = readValues["CBLampStateFromServer"]
            DILampStateFromServer = readValues["DILampStateFromServer"]
            CrCLampStateFromServer = readValues["CrCLampStateFromServer"]
            CPLampStateFromServer = readValues["CPLampStateFromServer"]
            SFLampStateFromServer = readValues["SFLampStateFromServer"]
            TVTLobbyLampStateFromServer = readValues["TVTLobbyLampStateFromServer"]
            TVTTankLampStateFromServer = readValues["TVTTankLampStateFromServer"]
            MMLampStateFromServer = readValues["MMLampStateFromServer"]

            # Doors
            MM_Lobby_DoubleDoor = readValues["MM_Lobby_DoubleDoor"]
            MM_Lobby_DoubleDoor_Open = readValues["MM_Lobby_DoubleDoor_Open"]
            MM_Jake_DefeatedAddress = readValues["MM_Jake_DefeatedAddress"]
            MM_Professor_RescuedAddress = readValues["MM_Professor_RescuedAddress"]
            MM_Clown_State = readValues["MM_Clown_State"]
            MM_Natalie_RescuedAddress = readValues["MM_Natalie_RescuedAddress"]
            MM_Jake_Defeated = readValues["MM_Jake_Defeated"]
            MM_Professor_Rescued = readValues["MM_Professor_Rescued"]
            MM_Natalie_Rescued = readValues["MM_Natalie_Rescued"]
            MM_Natalie_Rescued_Local = readValues["MM_Natalie_Rescued_Local"]
            MM_Lobby_DoorDetection = readValues["MM_Lobby_DoorDetection"]
            WSW_RoomState = readValues["WSW_RoomState"]
            lockCamera = readValues["lockCamera"]
            MM_AlertRoom_ButtonPressed = readValues["MM_AlertRoom_ButtonPressed"]

            # Buttons
            DI_Button_Pressed = readValues["DI_Button_Pressed"]
            CrC_Water_ButtonPressed = readValues["CrC_Water_ButtonPressed"]
            CrC_Basement_ButtonPressed = readValues["CrC_Basement_ButtonPressed"]
            TVT_Lobby_ButtonPressed = readValues["TVT_Lobby_ButtonPressed"]
            MM_MonkeyHead_ButtonPressed = readValues["MM_MonkeyHead_ButtonPressed"]
            MM_Painting_ButtonPressed = readValues["MM_Painting_ButtonPressed"]
            DR_Block_Pushed = readValues["DR_Block_Pushed"]

            monkeylevelcounts = [
                readValues["FF_MonkeyCount"],
                readValues["PO_MonkeyCount"],
                readValues["ML_MonkeyCount"],
                readValues["TJ_MonkeyCount"],
                readValues["DR_MonkeyCount"],
                readValues["CR_MonkeyCount"],
                readValues["SA_MonkeyCount"],
                readValues["CB_MonkeyCount"],
                readValues["CC_MonkeyCount"],
                readValues["DI_MonkeyCount"],
                readValues["SM_MonkeyCount"],
                readValues["FR_MonkeyCount"],
                readValues["HS_MonkeyCount"],
                readValues["GA_MonkeyCount"],
                readValues["ST_MonkeyCount"],
                readValues["WSW_MonkeyCount"],
                readValues["CRC_MonkeyCount"],
                readValues["CP_MonkeyCount"],
                readValues["SF_MonkeyCount"],
                readValues["TVT_MonkeyCount"],
                readValues["MM_MonkeyCount"],
            ]

            # Write tables
            itemsWrites = []
            Menuwrites = []
            S2_writes = []
            # When in Menu, change the behavior of "NewGame" to warp you to time station instead
            if gameState == RAM.gameState["Menu"] and newGameAddress == 0xAC:
                Menuwrites += [(RAM.newGameAddress, 0x98.to_bytes(1, "little"), "MainRAM")]
                Menuwrites += [(RAM.cookieAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                await bizhawk.write(ctx.bizhawk_ctx, Menuwrites)

            # Set Initial received_ID when in first level ever OR in first hub ever
            if (recv_index == 0xFFFFFFFF) or (recv_index == 0x00FF00FF):
                recv_index = 0
                # Set gadgetStateFromServer if it is default
                if gadgetStateFromServer == 0xFFFF or gadgetStateFromServer == 0x00FF:
                    gadgetStateFromServer = 0
            if keyCountFromServer == 0xFF:
                # Get items from server
                keyCountFromServer = 0

            if tokenCountFromServer == 0xFF:
                # Get items from server
                tokenCountFromServer = 0

            if MM_Lobby_DoubleDoor == 0xFF:
                MM_Lobby_DoubleDoor = 0

            if MM_Jake_Defeated > 0x01:
                MM_Jake_Defeated = 0

            if MM_Professor_Rescued > 0x01:
                MM_Professor_Rescued = 0

            if MM_Natalie_Rescued > 0x01:
                MM_Natalie_Rescued = 0

            #if Specter1CompleteAddress == 0:
                #Specter1CompleteAddress = 0
                #S1_writes += [(RAM.Specter1CompleteAddress, Specter1CompleteAddress.to_bytes(1, "little"), "MainRAM")]
                #S1_writes += [(RAM.tempSpecter1CompleteAddress, Specter1CompleteAddress.to_bytes(1, "little"), "MainRAM")]
                #await bizhawk.write(ctx.bizhawk_ctx, S1_writes)

            if Specter2CompleteAddress == 255:
                Specter2CompleteAddress = 0
                S2_writes += [(RAM.Specter2CompleteAddress, Specter2CompleteAddress.to_bytes(1, "little"), "MainRAM")]
                S2_writes += [(RAM.tempSpecter2CompleteAddress, Specter2CompleteAddress.to_bytes(1, "little"), "MainRAM")]
                await bizhawk.write(ctx.bizhawk_ctx, S2_writes)

            if Specter1CompleteAddress == 0:
                self.MM_Completed = False
            else:
                self.MM_Completed = True

            if Specter2CompleteAddress == 0:
                self.PPM_Completed = False
            else:
                self.PPM_Completed = True

            # Get WaterNet state from memory
            waternetState = 0
            if WaterNetStateFromServer != 0xFF:
                waternetState = WaterNetStateFromServer

            # Get Dive state from memory
            watercatchState = 0
            if WaterCatchStateFromServer != 0x00:
                watercatchState = WaterCatchStateFromServer

            # Get Lamp states
            CBLampState = 0
            DILampState = 0
            CrCLampState = 0
            CPLampState = 0
            SFLampState = 0
            TVTLobbyLampState = 0
            TVTTankLampState = 0
            MMLampState = 0

            if CBLampStateFromServer != 0x00 and CBLampStateFromServer != 0xFF: CBLampState = CBLampStateFromServer
            if DILampStateFromServer != 0x00 and DILampStateFromServer != 0xFF: DILampState = DILampStateFromServer
            if CrCLampStateFromServer != 0x00 and CrCLampStateFromServer != 0xFF: CrCLampState = CrCLampStateFromServer
            if CPLampStateFromServer != 0x00 and CPLampStateFromServer != 0xFF: CPLampState = CPLampStateFromServer
            if SFLampStateFromServer != 0x00 and SFLampStateFromServer != 0xFF: SFLampState = SFLampStateFromServer
            if TVTLobbyLampStateFromServer != 0x00 and TVTLobbyLampStateFromServer != 0xFF: TVTLobbyLampState = TVTLobbyLampStateFromServer
            if TVTTankLampStateFromServer != 0x00 and TVTTankLampStateFromServer != 0xFF: TVTTankLampState = TVTTankLampStateFromServer
            if MMLampStateFromServer != 0x00 and MMLampStateFromServer != 0xFF: MMLampState = MMLampStateFromServer

            START_recv_index = recv_index
            initialitemValueslist = [
                gadgetStateFromServer,
                keyCountFromServer,
                tokenCountFromServer,
                waternetState,watercatchState,
                MM_Lobby_DoubleDoor,
                CBLampState,DILampState,CrCLampState,CPLampState,SFLampState,TVTLobbyLampState,TVTTankLampState,MMLampState,
                energyChips, cookies, totalLives,flashAmmo, rocketAmmo
            ]
            # Prevent sending items when connecting early (Sony, Menu or Intro Cutscene)
            firstBootStates = {RAM.gameState["Sony"], RAM.gameState["Menu"], RAM.gameState["Cutscene2"], RAM.gameState["Demo"], RAM.gameState["Save/Load"], RAM.gameState["Memory"]}
            boolIsFirstBoot = gameState in firstBootStates
            if recv_index < (len(ctx.items_received)) and not boolIsFirstBoot:
                increment = 0
                for item in ctx.items_received:
                    # Increment to already received address first before sending
                    itemName = ctx.item_names.lookup_in_slot(item.item,ctx.slot)
                    if increment < START_recv_index:
                        increment += 1
                    else:
                        recv_index += 1
                        if RAM.items["Club"] <= (item.item - self.offset) <= RAM.items["Car"]:
                            if gadgetStateFromServer | (item.item - self.offset) != gadgetStateFromServer:
                                gadgetStateFromServer = gadgetStateFromServer | (item.item - self.offset)
                        elif (item.item - self.offset) == RAM.items["Key"]:
                            keyCountFromServer += 1
                        elif (item.item - self.offset) == RAM.items["Token"]:
                            tokenCountFromServer += 1
                            if ctx.slot_data["goal"] == GoalOption.option_tokenhunt and tokenCountFromServer == min(ctx.slot_data["requiredtokens"], ctx.slot_data["totaltokens"]):
                                await ctx.send_msgs([{
                                    "cmd": "StatusUpdate",
                                    "status": ClientStatus.CLIENT_GOAL
                                }])
                                await self.send_bizhawk_message(ctx, "You have completed your goal o[8(|)", "Passthrough", "")
                                ctx.finished_game = True
                        #elif (item.item - self.offset) == ["Victory"]:
                            #pass
                        elif (item.item - self.offset) == RAM.items["WaterNet"]:
                            waternetState = 2
                            watercatchState = 1
                        elif (item.item - self.offset) == RAM.items["ProgWaterNet"]:
                            if waternetState != 2:
                                waternetState += 1
                        elif (item.item - self.offset) == RAM.items["MM_DoubleDoorKey"]:
                            MM_Lobby_DoubleDoor = 1
                        elif (item.item - self.offset) == RAM.items["WaterCatch"]:
                            watercatchState = 1
                        elif (item.item - self.offset) == RAM.items["CB_Lamp"]:
                            CBLampState = 1
                        elif (item.item - self.offset) == RAM.items["DI_Lamp"]:
                            DILampState = 1
                        elif (item.item - self.offset) == RAM.items["CrC_Lamp"]:
                            CrCLampState = 1
                        elif (item.item - self.offset) == RAM.items["CP_Lamp"]:
                            CPLampState = 1
                        elif (item.item - self.offset) == RAM.items["SF_Lamp"]:
                            SFLampState = 1
                        elif (item.item - self.offset) == RAM.items["TVT_Lobby_Lamp"]:
                            TVTLobbyLampState = 1
                        elif (item.item - self.offset) == RAM.items["TVT_Tank_Lamp"]:
                            TVTTankLampState = 1
                        elif (item.item - self.offset) == RAM.items["MM_Lamp"]:
                            MMLampState = 1
                        elif RAM.items["Shirt"] <= (item.item - self.offset) <= RAM.items["ThreeRocket"]:
                            if (item.item - self.offset) == RAM.items["Triangle"] or (item.item - self.offset) == RAM.items["BigTriangle"] or (item.item - self.offset) == RAM.items["BiggerTriangle"]:
                                if (item.item - self.offset) == RAM.items["Triangle"]:
                                    energyChips += 1
                                elif (item.item - self.offset) == RAM.items["BigTriangle"]:
                                    energyChips += 5
                                elif (item.item - self.offset) == RAM.items["BiggerTriangle"]:
                                    energyChips += 25
                                # If total gets greater than 100, subtract 100 and give a life instead
                                if energyChips >= 100:
                                    energyChips = energyChips - 100
                                    # Don't give a life if it would exceed 99 lives
                                    if totalLives < 100:
                                        totalLives += 1
                            elif (item.item - self.offset) == RAM.items["Cookie"]:
                                if cookies < 5:
                                    cookies += 1
                            elif (item.item - self.offset) == RAM.items["FiveCookies"]:
                                cookies = 5
                            elif (item.item - self.offset) == RAM.items["Shirt"]:
                                if totalLives < 100:
                                    totalLives += 1
                            # add special pellets, ensuring they don't go over the current cap
                            elif (item.item - self.offset) == RAM.items["Flash"]:
                                if flashAmmo < 9:
                                    flashAmmo += 1
                            elif (item.item - self.offset) == RAM.items["Rocket"]:
                                if rocketAmmo < 9:
                                    rocketAmmo += 1
                            elif (item.item - self.offset) == RAM.items["ThreeFlash"]:
                                flashAmmo += 3
                                if flashAmmo > 9:
                                    flashAmmo = 9
                            elif (item.item - self.offset) == RAM.items["ThreeRocket"]:
                                rocketAmmo += 3
                                if rocketAmmo > 9:
                                    rocketAmmo = 9
                        elif RAM.items["BananaPeelTrap"] <= (item.item - self.offset) <= RAM.items["CameraRotateTrap"]:
                            if itemName in ctx.slot_data["trapsonreconnect"]:
                                self.specialitem_queue.append([(item.item - self.offset),0])
                        elif (item.item - self.offset) == RAM.items["RainbowCookie"]:
                            self.specialitem_queue.append([(item.item - self.offset),0])

                itemValueslist = [
                    gadgetStateFromServer,
                    keyCountFromServer,
                    tokenCountFromServer,
                    waternetState, watercatchState,
                    MM_Lobby_DoubleDoor,
                    CBLampState, DILampState, CrCLampState, CPLampState, SFLampState, TVTLobbyLampState,
                    TVTTankLampState, MMLampState,
                    energyChips, cookies, totalLives,flashAmmo, rocketAmmo,
                ]
                # Writes to memory if there is a new item, after the loop
                #If the increment is different from recv_index this means we received items
                if increment != recv_index:
                    itemsWrites += [(RAM.lastReceivedArchipelagoID, recv_index.to_bytes(4, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempLastReceivedArchipelagoID, recv_index.to_bytes(4, "little"), "MainRAM")]
                if initialitemValueslist[0] != itemValueslist[0] or increment == 0:
                    itemsWrites += [(RAM.gadgetStateFromServer, gadgetStateFromServer.to_bytes(2, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempGadgetStateFromServer, gadgetStateFromServer.to_bytes(2, "little"), "MainRAM")]
                if initialitemValueslist[1] != itemValueslist[1]:
                    itemsWrites += [(RAM.keyCountFromServer, keyCountFromServer.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempKeyCountFromServer, keyCountFromServer.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[2] != itemValueslist[2]:
                    itemsWrites += [(RAM.tokenCountFromServer, tokenCountFromServer.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempTokenCountFromServer, tokenCountFromServer.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[3] != itemValueslist[3]:
                    itemsWrites += [(RAM.WaterNetAddress, waternetState.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempWaterNetAddress, waternetState.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[4] != itemValueslist[4]:
                    itemsWrites += [(RAM.WaterCatchAddress, watercatchState.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempWaterCatchAddress, watercatchState.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[5] != itemValueslist[5]:
                    itemsWrites += [(RAM.temp_MMLobbyDoorAddress, MM_Lobby_DoubleDoor.to_bytes(1, "little"), "MainRAM")]

                if initialitemValueslist[6] != itemValueslist[6]:
                    itemsWrites += [(RAM.CB_LampAddress, CBLampState.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempCB_LampAddress, CBLampState.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[7] != itemValueslist[7]:
                    itemsWrites += [(RAM.DI_LampAddress, DILampState.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempDI_LampAddress, DILampState.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[8] != itemValueslist[8]:
                    itemsWrites += [(RAM.CrC_LampAddress, CrCLampState.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempCrC_LampAddress, CrCLampState.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[9] != itemValueslist[9]:
                    itemsWrites += [(RAM.CP_LampAddress, CPLampState.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempCP_LampAddress, CPLampState.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[10] != itemValueslist[10]:
                    itemsWrites += [(RAM.SF_LampAddress, SFLampState.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempSF_LampAddress, SFLampState.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[11] != itemValueslist[11]:
                    itemsWrites += [(RAM.TVT_Lobby_LampAddress, TVTLobbyLampState.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempTVT_Lobby_LampAddress, TVTLobbyLampState.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[12] != itemValueslist[12]:
                    itemsWrites += [(RAM.TVT_Tank_LampAddress, TVTTankLampState.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempTVT_Tank_LampAddress, TVTTankLampState.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[13] != itemValueslist[13]:
                    itemsWrites += [(RAM.MM_LampAddress, MMLampState.to_bytes(1, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempMM_LampAddress, MMLampState.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[14] != itemValueslist[14]:
                    itemsWrites += [(RAM.energyChipsAddress, energyChips.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[15] != itemValueslist[15]:
                    itemsWrites += [(RAM.cookieAddress, cookies.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[16] != itemValueslist[16]:
                    itemsWrites += [(RAM.livesAddress, totalLives.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[17] != itemValueslist[17]:
                    itemsWrites += [(RAM.flashAddress, flashAmmo.to_bytes(1, "little"), "MainRAM")]
                if initialitemValueslist[18] != itemValueslist[18]:
                    itemsWrites += [(RAM.rocketAddress, rocketAmmo.to_bytes(1, "little"), "MainRAM")]

            self.worldkeycount = keyCountFromServer
            self.tokencount = tokenCountFromServer

            # ======== Locations handling =========
            Locations_Reads = [currentLevel,gameState,currentRoom,previousCoinStateRoom,currentCoinStateRoom,gameRunning,TVT_BossPhase,gotMail,mailboxID,jakeVictory,S1_P2_State,S1_P2_Life,S2_isCaptured,levelselect_coinlock_Address,CoinTable,TempCoinTable,monkeylevelcounts,currentApes,transitionPhase]
            await self.locations_handling(ctx, Locations_Reads)


            # Write Array
            # Training Room, set to 0xFF to mark as complete

            # Gadgets unlocked
            # Required apes (to match hundo)
            writes = [
                #(RAM.trainingRoomProgressAddress, 0xFF.to_bytes(1, "little"), "MainRAM"),
                (RAM.unlockedGadgetsAddress, gadgetStateFromServer.to_bytes(2, "little"), "MainRAM"),
                (RAM.requiredApesAddress, localhundoCount.to_bytes(1, "little"), "MainRAM"),
            ]
            GadgetTrainingsUnlock = 0x00000000
            trainingRoomProgress = 0xFF
            # Training Room Unlock state checkup: Set to 0x00000000 to prevent all buttons from working
            varGoal = ctx.slot_data["goal"]
            varFastTokenGoal = ctx.slot_data["fasttokengoal"]
            boolActivateFastGoalWarp = (varFastTokenGoal == FastTokenGoalOption.option_on and varGoal in (GoalOption.option_mmtoken,GoalOption.option_ppmtoken) and tokenCountFromServer >= min(ctx.slot_data["requiredtokens"], ctx.slot_data["totaltokens"]))
            # **Going into the room**
            if (transitionPhase == RAM.transitionPhase["InTransition"] and NearbyRoom == 90):
                # If the FastGoal warp needs to be activated,needs to be done in transition
                if boolActivateFastGoalWarp:
                    GadgetTrainingsUnlock = 0x8C63FDCC
                    trainingRoomProgress = 0x01
                else:
                    GadgetTrainingsUnlock = 0x00000000
                    trainingRoomProgress  = 0xFF
            elif currentRoom == 90:
                # **After the transition or while in room**
                # Check for FastTokenGoal + enough tokens
                if boolActivateFastGoalWarp:
                    GadgetTrainingsUnlock = 0x8C63FDCC
                    trainingRoomProgress = 0x01
                    # Check which door needs to be redirected to
                    if varGoal == GoalOption.option_mmtoken:
                        doorTransition = doorTransitions.get(AEDoor.MM_SPECTER1_ROOM.value)
                        targetRoom = doorTransition[0]
                        targetDoor = doorTransition[1]
                    else:
                        doorTransition = doorTransitions.get(AEDoor.PPM_ENTRY.value)
                        targetRoom = doorTransition[0]
                        targetDoor = doorTransition[1]
                    # Change Transition2 to the desired transitions as needed
                    TR2_Adresses = list(RAM.transitionAddresses.get(2))
                    writes += [(TR2_Adresses[0], targetRoom.to_bytes(1, "little"), "MainRAM")]
                    writes += [(TR2_Adresses[1], targetDoor.to_bytes(1, "little"), "MainRAM")]
                else:
                    # You are in the room, but FastToken is not on OR you do not have enough tokens
                    GadgetTrainingsUnlock = 0x00000000
                    trainingRoomProgress = 0xFF
            else:
                # Not going into the Training Room NOR being into it, set these values to normal
                GadgetTrainingsUnlock = 0x8C63FDCC
                trainingRoomProgress = 0xFF

            InFastTokenWarp = RAM.gameState["TimeStation"] == gameState and boolActivateFastGoalWarp and currentRoom in {83,86,87}
            if InFastTokenWarp:
                writes += [(RAM.gameStateAddress, RAM.gameState["InLevel"].to_bytes(1, "little"), "MainRAM")]
            writes += [(RAM.GadgetTrainingsUnlockAddress, GadgetTrainingsUnlock.to_bytes(4, "little"), "MainRAM")]
            writes += [(RAM.trainingRoomProgressAddress, trainingRoomProgress.to_bytes(1, "little"), "MainRAM")]

            # Kickout Prevention (Monkey catch + Boss Kills)
            if self.preventKickOut == 1:
                if gameState in (RAM.gameState["InLevel"], RAM.gameState["InLevelTT"]):
                    if currentRoom == 48:
                        if CrC_BossPhase == 4 and CrC_BossLife == 0x00:
                            writes += [(RAM.CrC_BossPhaseAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                            #writes += [(RAM.CrC_DoorVisual, 0xF8.to_bytes(1, "little"), "MainRAM")]
                            #writes += [(RAM.CrC_DoorHitBox, 0xF8.to_bytes(1, "little"), "MainRAM")]
                    if currentRoom == 68:
                        if TVT_BossPhase == 4 and TVT_BossLife == 0x00:
                            writes += [(RAM.TVT_BossPhase, 0x05.to_bytes(1, "little"), "MainRAM")]

                    # Prevents Kickout if it is not already prevented
                    if kickoutofLevel != 0:
                        writes += [(RAM.kickoutofLevelAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                        writes += [(RAM.kickoutofLevelAddress2, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                    if localLevelState != 0x03:
                        writes += [(RAM.localLevelState, 0x03.to_bytes(1, "little"), "MainRAM")]
                else:
                    # Stops preventing Kickout outside of the Levels, since it could cause crashes
                    if kickoutofLevel == 0:
                        writes += [(RAM.kickoutofLevelAddress, 0x84830188.to_bytes(4, "little"), "MainRAM")]
                        writes += [(RAM.kickoutofLevelAddress2, 0x24020001.to_bytes(4, "little"), "MainRAM")]
            elif self.preventKickOut == 0:
                # Ensure you always get kicked out when catching the last monkey, to be consistent
                if kickoutofLevel == 0:
                    writes += [(RAM.kickoutofLevelAddress, 0x84830188.to_bytes(4, "little"), "MainRAM")]
                    writes += [(RAM.kickoutofLevelAddress2, 0x24020001.to_bytes(4, "little"), "MainRAM")]
                if RAM.gameState["Cleared"] == gameState:
                    if temp_SA_Completed == 0xFF:
                        writes += [(RAM.SA_CompletedAddress, 0x19.to_bytes(1, "little"), "MainRAM")]
                        writes += [(RAM.temp_SA_CompletedAddress, SA_Completed.to_bytes(1, "little"), "MainRAM")]
                        writes += [(RAM.GA_CompletedAddress, 0x19.to_bytes(1, "little"), "MainRAM")]
                        writes += [(RAM.temp_GA_CompletedAddress, GA_Completed.to_bytes(1, "little"), "MainRAM")]
                elif RAM.gameState["LevelSelect"] != gameState:
                    # Should reset the values once "Completed" state is exited
                    # Could maybe check if in Time Hub instead?
                    if temp_SA_Completed != 0xFF:
                        writes += [(RAM.SA_CompletedAddress, temp_SA_Completed.to_bytes(1, "little"), "MainRAM")]
                        writes += [(RAM.temp_SA_CompletedAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                    # Maybe not needed for GA since it will result in 0 but kept just to be safe
                    if temp_SA_Completed != 0xFF:
                        writes += [(RAM.GA_CompletedAddress, temp_GA_Completed.to_bytes(1, "little"), "MainRAM")]
                        writes += [(RAM.temp_GA_CompletedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                if localLevelState != 0x00:
                    writes += [(RAM.localLevelState, 0x00.to_bytes(1, "little"), "MainRAM")]

            # Flag to mark MM as completed for goal check if needed
            if self.MM_Completed == True and Specter1CompleteAddress == 0:
                Specter1CompleteAddress = 1
                #print(f"Wrote value to Specter2CompleteAddress : 1")
                writes += [(RAM.Specter1CompleteAddress, Specter1CompleteAddress.to_bytes(1, "little"), "MainRAM")]
                writes += [(RAM.tempSpecter1CompleteAddress, Specter1CompleteAddress.to_bytes(1, "little"), "MainRAM")]

            # PPM_Completed flag for "100% Complete" label on PPM level
            if self.PPM_Completed == True and Specter2CompleteAddress == 0:
                Specter2CompleteAddress = 1
                #print(f"Wrote value to Specter2CompleteAddress : 1")
                writes += [(RAM.Specter2CompleteAddress, Specter2CompleteAddress.to_bytes(1, "little"), "MainRAM")]
                writes += [(RAM.tempSpecter2CompleteAddress, Specter2CompleteAddress.to_bytes(1, "little"), "MainRAM")]

            # If there is messages waiting in the queue, print them to Bizhawk
            if self.messagequeue is not None and self.messagequeue != []:
                await self.process_bizhawk_messages(ctx)

            # ======== Handle Death Link =========
            DL_Reads = [cookies, gameRunning, gameState, menuState2, spikeState2]
            await self.handle_death_link(ctx, DL_Reads)

            # ======== Update tags (DeathLink and TrapLink) =========
            await self.update_tags(ctx)

            # ======== Handle Trap Link =========
            #await self.handle_trap_link(ctx)

            # ======== Spike Color handling =========
            # For checking if the chosen color currently needs to be applied.
            Color_Reads = [gameState, spikeColor, spikeState2]
            await self.Spike_Color_handling(ctx, Color_Reads, "")
            # ================================

            # ======== Special Items Handling =========
            # For Traps and Special Items.
            currentGadgets = await self.check_gadgets(ctx, gadgetStateFromServer)
            SpecialItems_Reads = [gameState, gotMail, spikeState, spikeState2, menuState, menuState2, currentGadgets, currentRoom, gameRunning, self.DS_spikecolor,heldGadget,CatchingState,cookies]
            await self.specialitems_handling(ctx, SpecialItems_Reads)
            # ================================

            # ======== Monkey Mashing =========
            if self.ape_handler.is_active:
                await self.ape_handler.send_monkey_inputs()
            else:
                if self.ape_handler.sentMessage == False:
                    message = "Monkey Mash Trap finished"
                    await self.send_bizhawk_message(ctx, message, "Passthrough", "")
                    self.ape_handler.sentMessage = True
            # ================================

            # ======== Rainbow Cookie =========
            if self.rainbow_cookie.is_active:
                await self.rainbow_cookie.update_state_and_deactivate()
            else:
                if self.rainbow_cookie.sentMessage == False:
                    message = "Rainbow Cookie finished"
                    await self.send_bizhawk_message(ctx, message, "Passthrough", "")
                    self.rainbow_cookie.sentMessage = True
            # ================================

            # ======== Stun Trap =========
            if self.stun_trap.is_active:
                await self.stun_trap.update_state_and_deactivate(currentRoom)
            else:
                if self.stun_trap.sentMessage == False:
                    message = "Stun Trap finished"
                    await self.send_bizhawk_message(ctx, message, "Passthrough", "")
                    self.stun_trap.sentMessage = True
            # ================================

            # ======== Camera Rotate Trap =========
            if self.camera_rotate_trap.is_active:
                await self.camera_rotate_trap.update_state_and_deactivate(currentRoom)
            else:
                if self.camera_rotate_trap.sentMessage == False:
                    message = "Camera Rotate Trap finished"
                    await self.send_bizhawk_message(ctx, message, "Passthrough", "")
                    self.camera_rotate_trap.sentMessage = True
            # ================================
            # ======= Credits skipping =======
            # Credits skipping function for S1 and S2
            Credits_Reads = [currentRoom, gameState, S1_Cutscene_Redirection, S2_Cutscene_Redirection]
            await self.Credits_handling(ctx, Credits_Reads)
            # ================================

            # ======= PPM Optimizations =======
            # Execute the code segment for PPM fight locking
            PPM_Reads = [currentRoom, currentLevel, gameState,S2_CutsceneState,S2_GlobalCutsceneState]
            await self.PPM_Optimizations(ctx, PPM_Reads)
            # ================================

            # ======= MM Optimizations =======
            # Execute the code segment for MM Double Door and related optimizations
            MM_Reads = [currentRoom, currentLevel, gameState, NearbyRoom, transitionPhase, MM_Jake_Defeated, MM_Lobby_DoubleDoor, MM_Lobby_DoorDetection, MM_Lobby_DoubleDoor_Open, MM_Jake_DefeatedAddress, MM_Natalie_RescuedAddress, MM_Natalie_Rescued, MM_Natalie_Rescued_Local, MM_Professor_Rescued, S1_P1_FightTrigger, MM_Clown_State,MM_AlertRoom_ButtonPressed]
            await self.MM_Optimizations(ctx, MM_Reads)
            # ================================

            # ====== Permanent Buttons =======
            # Execute the Button handling code segment
            Button_Reads = [currentRoom, gameState, DI_Button_Pressed, CrC_Water_ButtonPressed, CrC_Basement_ButtonPressed, TVT_Lobby_ButtonPressed, MM_MonkeyHead_ButtonPressed, MM_Painting_ButtonPressed, DR_Block_Pushed, transitionPhase]
            await self.permanent_buttons_handling(ctx, Button_Reads)
            # ================================

            localLampsUpdate = {20: CBLampState, 53: CPLampState, 79: MMLampState}
            globalLampsUpdate = {26: DILampState, 46: CrCLampState, 57: SFLampState, 65: TVTLobbyLampState, 66: TVTTankLampState}

            # ========= Lamp Unlocks =========
            # Tables for Lamp updates
            # Execute the Lamp unlocking code segment
            Lamps_Reads = [gameState, currentRoom, NearbyRoom, localLampsUpdate, globalLampsUpdate, transitionPhase,WSW_RoomState,lockCamera]
            await self.lamps_unlocks_handling(ctx, Lamps_Reads)
            # ================================

            # ========== Water Net ===========
            # Swim/Dive Prevention code
            WN_Reads = [gameState, waternetState, gameRunning, spikeState2, swim_oxygenLevel, cookies, isUnderwater, watercatchState]
            await self.water_net_handling(ctx, WN_Reads)
            # ================================

            # ====== Monkey count sync ========
            # ** There is a vanilla bug that Monkey count RAM addresses can be wrong sometimes. **
            # For checking if the Monkey count is correct. (Mainly for PPM unlock)
            MonkeyCount_Reads = [currentLevel, gameState, monkeylevelcounts]
            await self.syncMonkeycount(ctx, MonkeyCount_Reads)
            # ================================

            # ====== Gadgets handling ========
            # For checking which gadgets should be equipped
            # Also apply Magic Punch visual correction
            Gadgets_Reads = [currentLevel, currentRoom, heldGadget, gadgetStateFromServer, crossGadget, squareGadget, circleGadget, triangleGadget, menuState, menuState2, punchVisualAddress, gameState, currentGadgets]
            await self.gadgets_handler(ctx, Gadgets_Reads, temp_SA_Completed, temp_GA_Completed)
            # ================================

            # == Level Select Optimization ===
            # Execute the Level Select optimization code segment
            LSO_Reads = [gameState, CoinTable, TempCoinTable, SA_Completed, temp_SA_Completed, GA_Completed, temp_GA_Completed, LS_currentLevel, LS_currentWorld, worldIsScrollingRight,levelselect_coinlock_Address]
            await self.level_select_optimization(ctx, LSO_Reads)
            # ================================

            # == Entrance Randomization Handling ===
            # For all things related to ER and Room Rando
            ER_Reads = [gameState, status_currentWorld, status_currentLevel, currentLevel, transitionPhase, Spike_X_Pos, Spike_Y_Pos, Spike_Z_Pos, spikeState2, currentRoom,gameRunning, InputListener,Warp_State,Transition_Screen_Progress,LoadingState,Spike_CanMove]
            await self.ER_Handling(ctx, ER_Reads)


            # Unlock levels
            writes += self.unlockLevels(ctx, monkeylevelcounts, gameState, hundoMonkeysCount, ctx.slot_data["reqkeys"], ctx.slot_data["newpositions"], temp_SA_Completed, temp_GA_Completed, Specter2CompleteAddress)
            # ===== Text Replacements ======
            # Replace text Time Station mailbox here.
            # ==============================
            if self.mailboxTextReplaced == False:
                if currentRoom == 88 and gotMail == 0x02 and mailboxID == 0x71:
                    self.mailboxTextReplaced = True
                    mailboxtext = ""
                    mailboxbytes = []

                    mailboxbytes += text_to_bytes("World settings")
                    mailboxbytes += [13] # New line

                    # Add goal to mailbox text
                    if ctx.slot_data["goal"] == GoalOption.option_mm or ctx.slot_data["goal"] == GoalOption.option_mmtoken:
                        mailboxtext = "Goal: Specter 1"
                    elif ctx.slot_data["goal"] == GoalOption.option_ppm or ctx.slot_data["goal"] == GoalOption.option_ppmtoken:
                        mailboxtext = "Goal: Specter 2"
                    else:
                        mailboxtext = "Goal: Token Hunt"
                    mailboxbytes += text_to_bytes(mailboxtext)
                    mailboxbytes += [13]

                    # Add token information to mailbox text
                    if ctx.slot_data["goal"] == GoalOption.option_mmtoken or ctx.slot_data["goal"] == GoalOption.option_ppmtoken or ctx.slot_data["goal"] == GoalOption.option_tokenhunt:
                        mailboxbytes += text_to_bytes("You need")
                        mailboxbytes += [13]
                        reqtokens = min(ctx.slot_data["requiredtokens"], ctx.slot_data["totaltokens"])
                        tottokens = max(ctx.slot_data["requiredtokens"], ctx.slot_data["totaltokens"])
                        mailboxbytes += text_to_bytes(str(reqtokens) + "/" + str(tottokens) + " tokens.")
                        mailboxbytes += [13]
                        mailboxbytes += [13]
                        mailboxbytes += text_to_bytes("You now have")
                        mailboxbytes += [13]
                        # Grammar handling
                        if self.tokencount != 1:
                            mailboxbytes += text_to_bytes(str(self.tokencount) + " tokens.")
                        else:
                            mailboxbytes += text_to_bytes(str(self.tokencount) + " token.")
                    else:
                        mailboxbytes += [13]
                        mailboxbytes += text_to_bytes("There are no token")
                        mailboxbytes += [13]
                        mailboxbytes += text_to_bytes("requirements for")
                        mailboxbytes += [13]
                        mailboxbytes += text_to_bytes("this world.")

                    # Pad the text with zeroes to account for the fixed length first page
                    while len(mailboxbytes) < 79:
                        mailboxbytes += [0]

                    # Next page
                    mailboxbytes += [13]
                    mailboxbytes += [13]
                    mailboxbytes += [15]

                    # Add difficulty and trick information to mailbox text
                    if ctx.slot_data["logic"] == LogicOption.option_normal:
                        mailboxtext = "Difficulty: Normal"
                    elif ctx.slot_data["logic"] == LogicOption.option_hard:
                        mailboxtext = "Difficulty: Hard"
                    else:
                        mailboxtext = "Difficulty: Expert"
                    mailboxbytes += text_to_bytes(mailboxtext)
                    mailboxbytes += [13]

                    if ctx.slot_data["infinitejump"] == InfiniteJumpOption.option_false:
                        mailboxtext = "Infinite Jump: Off"
                    else:
                        mailboxtext = "Infinite Jump: On"
                    mailboxbytes += text_to_bytes(mailboxtext)
                    mailboxbytes += [13]

                    if ctx.slot_data["superflyer"] == SuperFlyerOption.option_false:
                        mailboxtext = "Super Flyer: Off"
                    else:
                        mailboxtext = "Super Flyer: On"
                    mailboxbytes += text_to_bytes(mailboxtext)
                    mailboxbytes += [13]

                    # Add lamp shuffle information to mailbox text
                    if ctx.slot_data["lamp"] == LampOption.option_false:
                        mailboxtext = "Lamp Shuffle: Off"
                    else:
                        mailboxtext = "Lamp Shuffle: On"
                    mailboxbytes += text_to_bytes(mailboxtext)
                    mailboxbytes += [13]

                    # Add Water Net information to mailbox text
                    mailboxbytes += text_to_bytes("Water Net Status:")
                    mailboxbytes += [13]
                    mailboxbytes += text_to_bytes("Swim ")
                    if waternetState == 0: # Can't swim
                        mailboxbytes += [10] # X button icon
                        mailboxbytes += [4]
                    else:
                        mailboxbytes += [10] # O button icon
                        mailboxbytes += [1]
                    mailboxbytes += text_to_bytes(" Dive ")
                    if waternetState == 2: # Can dive
                        mailboxbytes += [10]
                        mailboxbytes += [1]
                    else:
                        mailboxbytes += [10]
                        mailboxbytes += [4]
                    mailboxbytes += [13]
                    mailboxbytes += text_to_bytes("Catch ")
                    if watercatchState == 0: # Can't water catch
                        mailboxbytes += [10]
                        mailboxbytes += [4]
                    else:
                        mailboxbytes += [10]
                        mailboxbytes += [1]

                    # Next page
                    mailboxbytes += [13]
                    mailboxbytes += [13]
                    mailboxbytes += [15]

                    # Add coin and mailbox shuffle information to mailbox text
                    if ctx.slot_data["coin"] == CoinOption.option_false:
                        mailboxtext = "Coins: Off"
                    else:
                        mailboxtext = "Coins: On"
                    mailboxbytes += text_to_bytes(mailboxtext)
                    mailboxbytes += [13]

                    if ctx.slot_data["mailbox"] == MailboxOption.option_false:
                        mailboxtext = "Mailboxes: Off"
                    else:
                        mailboxtext = "Mailboxes: On"
                    mailboxbytes += text_to_bytes(mailboxtext)
                    mailboxbytes += [13]

                    # Add world key information to mailbox text
                    if ctx.slot_data["unlocksperkey"] == KeyOption.option_none:
                        mailboxbytes += [13]
                        mailboxbytes += text_to_bytes("There are no")
                        mailboxbytes += [13]
                        mailboxbytes += text_to_bytes("World Keys in")
                        mailboxbytes += [13]
                        mailboxbytes += text_to_bytes("this world.")
                        mailboxbytes += [13]
                    else:
                        mailboxbytes += text_to_bytes("Keys unlock")
                        mailboxbytes += [13]
                        if ctx.slot_data["unlocksperkey"] == KeyOption.option_world:
                            mailboxtext = "one world each."
                        elif ctx.slot_data["unlocksperkey"] == KeyOption.option_level:
                            mailboxtext = "one level each."
                        else:
                            mailboxtext = "two levels each."
                        mailboxbytes += text_to_bytes(mailboxtext)
                        mailboxbytes += [13]
                        # Grammar handling
                        if ctx.slot_data["extrakeys"] != 1:
                            mailboxbytes += text_to_bytes("There are " + str(ctx.slot_data["extrakeys"]))
                            mailboxbytes += [13]
                            mailboxbytes += text_to_bytes("extra World Keys.")
                        else:
                            mailboxbytes += text_to_bytes("There is " + str(ctx.slot_data["extrakeys"]))
                            mailboxbytes += [13]
                            mailboxbytes += text_to_bytes("extra World Key.")
                        mailboxbytes += [13]
                        if self.worldkeycount != 1:
                            mailboxbytes += text_to_bytes("You have " + str(self.worldkeycount) + " keys.")
                        else:
                            mailboxbytes += text_to_bytes("You have " + str(self.worldkeycount) + " key.")

                    # Next page
                    mailboxbytes += [13]
                    mailboxbytes += [13]
                    mailboxbytes += [15]

                    # Add entrance shuffle information to mailbox text
                    if ctx.slot_data["entrance"] == EntranceOption.option_off:
                        mailboxtext = "Entrance: Off"
                    elif ctx.slot_data["entrance"] == EntranceOption.option_on:
                        mailboxtext = "Entrance: On"
                    else:
                        mailboxtext = "Entrance: Lock MM"
                    mailboxbytes += text_to_bytes(mailboxtext)
                    mailboxbytes += [13]
                    # Add random first room information to mailbox text
                    # Not sure how to format it better than this
                    if ctx.slot_data["randomizestartingroom"] == RandomizeStartingRoomOption.option_off:
                        mailboxtext = "RandStartRoom: Off"
                    else:
                        mailboxtext = "RandStartRoom: On"
                    mailboxbytes += text_to_bytes(mailboxtext)
                    mailboxbytes += [13]

                    # Add door and lamp statuses to mailbox text
                    mailboxbytes += text_to_bytes("MM Double Door: ")
                    if MM_Lobby_DoubleDoor == 0: # Don't have item
                        mailboxbytes += [10] # X button icon
                        mailboxbytes += [4]
                    else:
                        mailboxbytes += [10] # O button icon
                        mailboxbytes += [1]
                    mailboxbytes += [13]
                    if ctx.slot_data["lamp"] == LampOption.option_true:
                        mailboxbytes += text_to_bytes("          Lamps")
                        mailboxbytes += [13]
                        mailboxbytes += text_to_bytes("CB: ")
                        if CBLampState == 0: # Don't have item
                            mailboxbytes += [10] # X button icon
                            mailboxbytes += [4]
                        else:
                            mailboxbytes += [10] # O button icon
                            mailboxbytes += [1]
                        mailboxbytes += text_to_bytes(" DI: ")
                        if DILampState == 0: # Don't have item
                            mailboxbytes += [10] # X button icon
                            mailboxbytes += [4]
                        else:
                            mailboxbytes += [10] # O button icon
                            mailboxbytes += [1]
                        mailboxbytes += text_to_bytes(" CC: ")
                        if CrCLampState == 0: # Don't have item
                            mailboxbytes += [10] # X button icon
                            mailboxbytes += [4]
                        else:
                            mailboxbytes += [10] # O button icon
                            mailboxbytes += [1]
                        mailboxbytes += [13]
                        mailboxbytes += text_to_bytes("CP: ")
                        if CPLampState == 0: # Don't have item
                            mailboxbytes += [10] # X button icon
                            mailboxbytes += [4]
                        else:
                            mailboxbytes += [10] # O button icon
                            mailboxbytes += [1]
                        mailboxbytes += text_to_bytes(" SF: ")
                        if SFLampState == 0: # Don't have item
                            mailboxbytes += [10] # X button icon
                            mailboxbytes += [4]
                        else:
                            mailboxbytes += [10] # O button icon
                            mailboxbytes += [1]
                        mailboxbytes += text_to_bytes(" TV: ")
                        if TVTLobbyLampState == 0: # Don't have item
                            mailboxbytes += [10] # X button icon
                            mailboxbytes += [4]
                        else:
                            mailboxbytes += [10] # O button icon
                            mailboxbytes += [1]
                        mailboxbytes += [13]
                        mailboxbytes += text_to_bytes("TV: ")
                        if TVTTankLampState == 0: # Don't have item
                            mailboxbytes += [10] # X button icon
                            mailboxbytes += [4]
                        else:
                            mailboxbytes += [10] # O button icon
                            mailboxbytes += [1]
                        mailboxbytes += text_to_bytes(" MM: ")
                        if MMLampState == 0: # Don't have item
                            mailboxbytes += [10] # X button icon
                            mailboxbytes += [4]
                        else:
                            mailboxbytes += [10] # O button icon
                            mailboxbytes += [1]

                    # End mailbox text
                    mailboxbytes += [13]
                    # Pad the text with zeroes to overwrite all pre-existing text
                    while len(mailboxbytes) < 600:
                        mailboxbytes += [0]

                    for x in range(0, 600):
                        writes += [(RAM.timeStationMailboxStart + x, mailboxbytes[x].to_bytes(1, "little"), "MainRAM")]
            else:
                if not (currentRoom == 88 and gotMail == 0x02 and mailboxID == 0x71):
                    self.mailboxTextReplaced = False

            await bizhawk.write(ctx.bizhawk_ctx, writes)
            #await bizhawk.guarded_write(ctx.bizhawk_ctx, TR_writes, TR_guards)
            await bizhawk.write(ctx.bizhawk_ctx, itemsWrites)

            self.levelglobal = currentLevel
            # For future room Auto-Tab in tracker
            if self.roomglobal != currentRoom:
                self.roomglobal = currentRoom
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": f"AE_room_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": currentRoom}],
                        }
                    ]
                )

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def locations_handling(self, ctx: "BizHawkClientContext", Locations_Reads) -> None:
        currentLevel = Locations_Reads[0]
        gameState = Locations_Reads[1]
        currentRoom = Locations_Reads[2]
        previousCoinStateRoom = Locations_Reads[3]
        currentCoinStateRoom = Locations_Reads[4]
        gameRunning = Locations_Reads[5]
        TVT_BossPhase = Locations_Reads[6]
        gotMail = Locations_Reads[7]
        mailboxID = Locations_Reads[8]
        jakeVictory = Locations_Reads[9]
        S1_P2_State = Locations_Reads[10]
        S1_P2_Life = Locations_Reads[11]
        S2_isCaptured = Locations_Reads[12]
        levelselect_coinlock_Address = Locations_Reads[13]
        CoinTable = Locations_Reads[14]
        TempCoinTable = Locations_Reads[15]
        monkeylevelcounts = Locations_Reads[16]
        currentApes = Locations_Reads[17]
        transitionPhase = Locations_Reads[18]

        locationsToSend = []
        monkeysToSend = set()
        coinsToSend = set()
        mailToSend = set()
        bossesToSend = set()
        racesToSend = set()
        allowcollect = 1 if self.allowcollect == 0x01 or self.forcecollect == True else 0
        SyncCount = 0
        # Replace levelID if in Monkey Madness
        if 0x18 < currentLevel <= 0x1D:
            level = 0x18
        else:
            level = currentLevel

        # Local update conditions
        # Condition to not update on first pass of client (self.roomglobal is 0 on first pass)
        if self.roomglobal == 0:
            localcondition = False
            return
        else:
            localcondition = (currentLevel == self.levelglobal)

        # Stock BossRooms in a variable (For excluding these rooms in local monkeys sending)
        locationWrites = []
        levelsToSync = []
        bossRooms = RAM.bossListLocal.keys()
        mailboxesRooms = RAM.mailboxListLocal.keys()
        redmailboxesRooms = RAM.redMailboxes.keys()
        keyList = list(RAM.monkeyListGlobal.keys())
        valList = list(RAM.monkeyListGlobal.values())

        addresses = []
        for val in valList:
            tuple1 = (val, 1, "MainRAM")
            addresses.append(tuple1)
        globalMonkeys = await bizhawk.read(ctx.bizhawk_ctx, addresses)
        GlobalIDToValueTable  = dict(zip(keyList,globalMonkeys))
        # localmonkeys = await bizhawk.read(ctx.bizhawk_ctx, addresses)
        # Check if in level select or in time hub, then read global monkeys

        temp_counter = currentApes
        if gameState == RAM.gameState["LevelSelect"] or currentLevel == RAM.levels["Time"] or (level == 0x18 and gameState == RAM.gameState["InLevel"]) or self.forcecollect and transitionPhase != 0x06:
            for i in range(len(globalMonkeys)):
                MonkeyID = keyList[i]
                MonkeyAddress = valList[i]
                iscaught = int.from_bytes(GlobalIDToValueTable[MonkeyID], byteorder='little') == RAM.caughtStatus["PrevCaught"]
                if iscaught:
                    if (MonkeyID + self.offset) not in self.locations_list:
                        monkeysToSend.add(MonkeyID + self.offset)
                else:
                    if allowcollect == 0x01:
                        if (MonkeyID + self.offset) in self.locations_list:
                            levels_containing_monkey = [level for level, monkeys in RAM.monkeysperlevel.items() if MonkeyID in monkeys]
                            room_containing_monkey = [room for room, monkeys in RAM.monkeyListTempLocal.items() if MonkeyID in monkeys]
                            if currentLevel in RAM.MM_roomspersublevel.keys():
                                Sub_Levels_Rooms = list(RAM.MM_roomspersublevel[currentLevel])
                            else:
                                Sub_Levels_Rooms = []
                            if levels_containing_monkey[0] == 0x18 and (level == 0x18 and (room_containing_monkey not in Sub_Levels_Rooms)) and currentRoom not in room_containing_monkey:
                                #print(f"+1 for Monkey#{MonkeyID}")
                                temp_counter += 1
                            locationWrites += [(MonkeyAddress,0x02.to_bytes(1, "little"), "MainRAM")]
                            GlobalIDToValueTable[MonkeyID] = 0x02.to_bytes(1, "little")
                            if not set(levels_containing_monkey).issubset(set(levelsToSync)):
                                levelsToSync += levels_containing_monkey
        # if being in a level
        # check if NOT in a boss room since there is no monkeys to send there
        if gameState == RAM.gameState["InLevel"] and (localcondition) and not (currentRoom in bossRooms):
            monkeyaddrs = RAM.monkeyListLocal[currentRoom]
            key_list = list(monkeyaddrs.keys())
            val_list = list(monkeyaddrs.values())

            addresses = []
            for val in val_list:
                tuple1 = (val, 1, "MainRAM")
                addresses.append(tuple1)
            localmonkeys = await bizhawk.read(ctx.bizhawk_ctx, addresses)

            if level == 0x18:
                levelRooms = list(RAM.MM_roomspersublevel[currentLevel])
            else:
                levelRooms = list(RAM.roomsperlevel[currentLevel])

            for i in range(len(levelRooms)):
                roomID = levelRooms[i]
                inRoom = currentRoom == roomID
                MonkeysInRoom_keys = list(RAM.monkeyListLocal.get(roomID).keys())
                MonkeysInRoom_address = list(RAM.monkeyListLocal.get(roomID).values())

                for x in range(len(MonkeysInRoom_keys)):
                    MonkeyID = MonkeysInRoom_keys[x]
                    GlobalMonkeyAddress = RAM.monkeyListGlobal.get(MonkeyID)
                    iscaughtglobal = int.from_bytes(GlobalIDToValueTable[MonkeyID], byteorder='little') in (RAM.caughtStatus["Caught"],RAM.caughtStatus["PrevCaught"])
                    if inRoom:
                        if transitionPhase != 0x06:
                            iscaughtlocal = int.from_bytes(localmonkeys[x], byteorder='little') in (RAM.caughtStatus["Caught"], RAM.caughtStatus["PrevCaught"])
                        else:
                            iscaughtlocal = False
                        if iscaughtlocal:
                            # If the Monkey is not already in the sent locations list, add it to an array to send location
                            if (MonkeyID + self.offset) not in self.locations_list and currentRoom == self.roomglobal:
                                monkeysToSend.add(MonkeyID + self.offset)
                                locationWrites += [(GlobalMonkeyAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                                GlobalIDToValueTable[MonkeyID] = 0x02.to_bytes(1, "little")
                                iscaughtglobal = True
                        else:
                            if allowcollect:
                                # If the location ID is in the list and they are not caught, sync them
                                if (MonkeyID + self.offset) in self.locations_list and transitionPhase != 0x06:
                                    #MonkeyID = key_list[x]
                                    MonkeyAddress = val_list[x]
                                    levels_containing_monkey = [level for level, monkeys in RAM.monkeysperlevel.items() if MonkeyID in monkeys]
                                    MonkeyHitboxUpdateAddress = RAM.localMonkeyHitbox.get(MonkeyAddress)
                                    locationWrites += [(MonkeyHitboxUpdateAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                                    locationWrites += [(MonkeyAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                                    locationWrites += [(GlobalMonkeyAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                                    #print(f"+1 for Monkey#{MonkeyID}")
                                    #print(f"iscaughtglobal:{iscaughtglobal}")
                                    temp_counter += 1
                                    if not set(levels_containing_monkey).issubset(set(levelsToSync)):
                                        levelsToSync += levels_containing_monkey
                                        #print(levelsToSync)
                    else:
                        if allowcollect:
                            # Supposed to only do a local sync of the current MM_Sub-Level
                            if (MonkeyID + self.offset) in self.locations_list and iscaughtglobal == False:
                                #print(f"Synched monkey #{MonkeyID}")
                                levels_containing_monkey = [level for level, monkeys in RAM.monkeysperlevel.items() if MonkeyID in monkeys]
                                room_containing_monkey = [room for room, monkeys in RAM.monkeyListTempLocal.items() if MonkeyID in monkeys]
                                MonkeyAddress = RAM.monkeyListTempLocal.get(room_containing_monkey[0]).get(MonkeyID)
                                locationWrites += [(GlobalMonkeyAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                                locationWrites += [(MonkeyAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                                GlobalIDToValueTable[MonkeyID] = 0x02.to_bytes(1, "little")
                                iscaughtglobal = True
                                print(f"Local +1 for Monkey#{MonkeyID}")
                                temp_counter += 1
                                if not set(levels_containing_monkey).issubset(set(levelsToSync)):
                                    levelsToSync += levels_containing_monkey
                                    #print(levelsToSync)
            if temp_counter > currentApes:
                locationWrites += [(RAM.currentApesAddress, temp_counter.to_bytes(1, "little"), "MainRAM")]

        # Check for Coins

        # New Coins System !
        # Gets the entirety of the game's coin table, then evaluate if the server is missing some of them
        # If a coin is collected and is not in the server it will then send

        # When allowcollect is on, the inverse is also true : Any coin the server have that is not in the game will be put in the game

        targetCoinTable = TempCoinTable if levelselect_coinlock_Address == 0x01 else CoinTable
        targetTableAddress = RAM.temp_startingCoinAddress if levelselect_coinlock_Address == 0x01 else RAM.startingCoinAddress

        # List of coins already in the client
        FormattedCoinTable = self.format_cointable(ctx,targetCoinTable,0,0,"Locations")
        if FormattedCoinTable == "":
            FormattedCoinTable = []
        FormattedCoinTable.sort(reverse=True)

        # List of coins in the client that the server does not have
        ClientCoinTable = [item for item in FormattedCoinTable if (item + self.offset + 300) not in self.locations_list]
        ClientCoinTable.sort(reverse=True)

        # List of coins in the server that the client does not have
        ServerCoinTable = [(item - self.offset - 300) for item in self.locations_list if (300 < (item - self.offset) <= 385) and (item - self.offset - 300) not in FormattedCoinTable]
        ServerCoinTable.sort(reverse=True)

        # Assemble the 2 coin table (Client and MissingFromServer)
        CoinsTableString = "".join([f"01{item:02x}" for item in FormattedCoinTable])
        FinalCoinsTableString = "".join([f"01{item:02x}" for item in ServerCoinTable])
        finalCoinTable = f"{CoinsTableString}{FinalCoinsTableString}"

        # Adjust to the coin table format
        while len(finalCoinTable) < 200:
            finalCoinTable = f"00FF{finalCoinTable}"
        CoinsTableint = int(f"0x{finalCoinTable}", 16)
        if allowcollect == 0x01:
            if ServerCoinTable != set() and ServerCoinTable != []:
                locationWrites += [(targetTableAddress, CoinsTableint.to_bytes(100, "little"), "MainRAM")]
        if ClientCoinTable != set() and ClientCoinTable != []:
            [coinsToSend.add((item + self.offset + 300)) for item in ClientCoinTable]

        if currentRoom in FormattedCoinTable:
            CoinValues = RAM.coinsListLocal.get(currentRoom)
            CoinVisualSprite = CoinValues[0]
            CoinHitBoxPosition = CoinValues[1]
            locationWrites2 = []
            locationGuards2 = []
            locationWrites2 += [(CoinVisualSprite, 0x00.to_bytes(1, "little"), "MainRAM")]
            locationWrites2 += [(CoinHitBoxPosition, RAM.CoinHitBoxPositionOff.to_bytes(2, "little"), "MainRAM")]
            locationGuards2 += [(CoinVisualSprite,0x04.to_bytes(1, "little"), "MainRAM")]
            locationGuards2 += [(RAM.currentRoomIdAddress,currentRoom.to_bytes(1, "little"), "MainRAM")]
            await bizhawk.guarded_write(ctx.bizhawk_ctx, locationWrites2,locationGuards2)

        if locationWrites:
            await bizhawk.write(ctx.bizhawk_ctx, locationWrites)

        if levelsToSync:
            # Sync all needed levels and return the number synched
            SyncCount = await self.syncAllMonkeycount(ctx,levelsToSync)
        # Check for level bosses
        if gameState == RAM.gameState["InLevel"] and (localcondition) and (currentRoom in bossRooms):
            bossaddrs = RAM.bossListLocal[currentRoom]
            key_list = list(bossaddrs.keys())
            val_list = list(bossaddrs.values())
            addresses = []

            for val in val_list:
                tuple1 = (val, 1, "MainRAM")
                addresses.append(tuple1)

            bossesList = await bizhawk.read(ctx.bizhawk_ctx, addresses)
            #bossesToSend = set()

            for i in range(len(bossesList)):
                # For TVT boss, check TVT_BossPhase, if it's 3 the fight is ongoing
                if (currentRoom == 68):
                    if (TVT_BossPhase == 3 and int.from_bytes(bossesList[i], byteorder='little') == 0x00):
                        if (key_list[i] + self.offset) not in self.locations_list:
                            bossesToSend.add(key_list[i] + self.offset)
                elif (currentRoom == 70):
                    if (gameRunning == 1 and int.from_bytes(bossesList[i], byteorder='little') == 0x00):
                        if (key_list[i] + self.offset) not in self.locations_list:
                            bossesToSend.add(key_list[i] + self.offset)
                            self.MM_Jake_Defeated = 1
                elif (currentRoom == 71):
                    if int.from_bytes(bossesList[i], byteorder='little') == 0x00:
                        if (key_list[i] + self.offset) not in self.locations_list:
                            bossesToSend.add(key_list[i] + self.offset)
                            self.MM_Professor_Rescued = 1
                else:
                    if int.from_bytes(bossesList[i], byteorder='little') == 0x00:
                        if (key_list[i] + self.offset) not in self.locations_list:
                            bossesToSend.add(key_list[i] + self.offset)

        # Check for Mailboxes
        if (localcondition) and (currentRoom in mailboxesRooms) and (gameState == RAM.gameState["InLevel"] or gameState == RAM.gameState["TimeStation"]):
            mailboxesaddrs = RAM.mailboxListLocal[currentRoom]

            boolGotMail = (gotMail == 0x02)
            key_list = list(mailboxesaddrs.keys())
            val_list = list(mailboxesaddrs.values())

            #mail_to_send = set()
            # Rearrange the array if there is 2 indexes for the same mailbox
            for i in range(len(val_list)):
                strVal = str(val_list[i])
                if strVal.__contains__("{"):
                    strVal = strVal.replace("{", "").replace("}", "")
                    strVal = strVal.split(",")
                    for j in range(len(strVal)):
                        key_list.append(key_list[i])
                        val_list.append(int(strVal[j]))
                    val_list.pop(i)
                    key_list.pop(i)
            for i in range(len(val_list)):
                if val_list[i] == mailboxID and boolGotMail:
                    if (key_list[i] + self.offset) not in self.locations_list:
                        mailToSend.add(key_list[i] + self.offset)

            # Only triggers if there is a red mailbox in the room and you are NOT viewing mail
            if (currentRoom in redmailboxesRooms) and (gotMail == 0x00):
                redMailboxaddrs = RAM.redMailboxes[currentRoom]

                redkey_list = list(redMailboxaddrs.keys())
                redval_list = list(redMailboxaddrs.values())

                addresses = []

                for val in redval_list:
                    tuple1 = (val, 1, "MainRAM")
                    addresses.append(tuple1)

                redMailboxesList = await bizhawk.read(ctx.bizhawk_ctx, addresses)
                for i in range(len(redkey_list)):
                    if int.from_bytes(redMailboxesList[i], byteorder='little') == 0x01:
                        if (redkey_list[i] + self.offset) not in self.locations_list:
                            mailToSend.add(redkey_list[i] + self.offset)

        # Check for Jake Victory
        if currentRoom == 19 and gameState == RAM.gameState["JakeCleared"] and jakeVictory == 0x2:
            #racesToSend = set()
            racesToSend.add(295 + self.offset)
            racesToSend.add(296 + self.offset)
            racesToSend.add(297 + self.offset)
            racesToSend.add(298 + self.offset)
            racesToSend.add(299 + self.offset)

        elif currentRoom == 36 and gameState == RAM.gameState["JakeCleared"] and jakeVictory == 0x2:
            #coins = set()
            racesToSend.add(290 + self.offset)
            racesToSend.add(291 + self.offset)
            racesToSend.add(292 + self.offset)
            racesToSend.add(293 + self.offset)
            racesToSend.add(294 + self.offset)


        # Check for victory conditions
        specter1Condition = (currentRoom == 86 and S1_P2_State == 1 and S1_P2_Life == 0)
        specter2Condition = (currentRoom == 87 and S2_isCaptured == 1)
        currentgoal = ctx.slot_data["goal"]
        if RAM.gameState["InLevel"] == gameState and specter1Condition:
            bossesToSend.add(self.offset + 205)
            if currentgoal in (GoalOption.option_mm, GoalOption.option_mmtoken) and not ctx.finished_game:
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])
                    await self.send_bizhawk_message(ctx, "You have completed your goal o[8(|)", "Passthrough", "")
            self.MM_Completed = True
            ctx.finished_game = True
        if RAM.gameState["InLevel"] == gameState and specter2Condition:
            bossesToSend.add(self.offset + 206)

            if currentgoal in (GoalOption.option_ppm, GoalOption.option_ppmtoken) and not ctx.finished_game:
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])
                    await self.send_bizhawk_message(ctx, "You have completed your goal o[8(|)", "Passthrough", "")
            self.PPM_Completed = True
            ctx.finished_game = True

        locationsToSend = monkeysToSend | coinsToSend | mailToSend | bossesToSend | racesToSend
        if locationsToSend != "" and locationsToSend != set():
            await ctx.check_locations(locationsToSend)

        if self.forcecollect == True:
            msg = f"=================================\n"
            msg += f"Synced progress into the game:\n"
            if ctx.slot_data["coin"] == 0x01:
                if len(ServerCoinTable) == 0:
                    msg += f"    No Coins updated\n"
                else:
                    msg += f"    {len(ServerCoinTable)} Coins updated\n"
            if SyncCount == 0:
                msg += f"    No Monkeys updated\n"
            else:
                msg += f"    {SyncCount} Monkeys updated\n"
            msg += f"=================================\n"
            logger.info(msg)
            self.forcecollect = False
    async def syncMonkeycount(self, ctx: "BizHawkClientContext", MonkeyCount_Reads) -> None:
        # Recalculate Monkey count on level exit by validating catch status of each monkey within the level
        # After recalculating, compare it to existing value and replace if needed

        currentLevel = MonkeyCount_Reads[0]
        gameState = MonkeyCount_Reads[1]
        monkeylevelCounts = MonkeyCount_Reads[2]

        MonkeyCountWrites = []

        # If in level, store the current level
        # Also triggers a boolean to check the count of monkeys on exit
        if gameState == RAM.gameState['InLevel'] and self.countMonkeys == False:
            self.countMonkeys = True

        if self.countMonkeys == True:
            self.lastenteredLevel = currentLevel
        # When exiting a level,it will recount monkeys and update the counter if needed
        if ((gameState == RAM.gameState["LevelSelect"] or gameState == RAM.gameState["TimeStation"]) and self.countMonkeys == True):

            self.countMonkeys = False
            monkeysperlevel_Keys = RAM.monkeysperlevel.keys()
            if self.lastenteredLevel not in monkeysperlevel_Keys:
                return
            # Get a list of all monkeys present in the lastenteredlevel :
            levelmonkeys = RAM.monkeysperlevel[self.lastenteredLevel]

            addresses = []

            for val in levelmonkeys:
                tuple1 = (RAM.monkeyListGlobal[val], 1, "MainRAM")
                addresses.append(tuple1)
            # Get global caught status of the monkeys
            level_MonkeyStates = await bizhawk.read(ctx.bizhawk_ctx, addresses)

            levelindex  = list(RAM.levels.values())
            monkeycountsAddresses = list(RAM.levelMonkeyCount.values())
            localcount = 0
            RAMMonkeycount = monkeylevelCounts[levelindex.index(self.lastenteredLevel)],

            # Check each values if monkeys are caught and increment a local counter
            for x in range(len(level_MonkeyStates)):
                MonkeyState = int.from_bytes(level_MonkeyStates[x], "little")
                if MonkeyState == 0x02:
                    localcount += 1
            # If there is a missmatch, correct the value in the RAM for the level
            if localcount != RAMMonkeycount:
                MonkeyCountWrites += [(monkeycountsAddresses[levelindex.index(self.lastenteredLevel)], localcount.to_bytes(1, "little"), "MainRAM")]

        await bizhawk.write(ctx.bizhawk_ctx, MonkeyCountWrites)

    async def syncAllMonkeycount(self, ctx: "BizHawkClientContext",levelindexes) -> int:
        # Recalculate ALL Monkey count on level exit by validating catch status of each monkey within the level
        # After recalculating, compare it to existing value and replace if needed

        MonkeyCountWrites = []

        # If in level, store the current level
        # Also triggers a boolean to check the count of monkeys on exit

        # When exiting a level,it will recount monkeys and update the counter if needed
        # Get a list of all monkeys present in the lastenteredlevel :
        GlobalCount = 0
        for x in range(len(levelindexes)):
            levelID = levelindexes[x]
            #print(f"synched level #{levelID}")
            levelmonkeys = RAM.monkeysperlevel.get(levelID)
            addresses = []

            for val in levelmonkeys:
                tuple1 = (RAM.monkeyListGlobal[val], 1, "MainRAM")
                addresses.append(tuple1)
            # Get global caught status of the monkeys
            level_MonkeyStates = await bizhawk.read(ctx.bizhawk_ctx, addresses)

            levelindex  = list(RAM.levels.values())
            monkeycountsAddresses = list(RAM.levelMonkeyCount.values())
            localcount = 0

            # Check each values if monkeys are caught and increment a local counter
            for y in range(len(level_MonkeyStates)):
                MonkeyState = int.from_bytes(level_MonkeyStates[y], "little")
                if MonkeyState == 0x02:
                    localcount += 1
                    GlobalCount += 1
            # Correct the value in the RAM for the level
            MonkeyCountWrites += [(monkeycountsAddresses[levelindex.index(levelID)],localcount.to_bytes(1, "little"), "MainRAM")]

        await bizhawk.write(ctx.bizhawk_ctx, MonkeyCountWrites)
        return GlobalCount

    async def gadgets_handler(self, ctx: "BizHawkClientContext", Gadgets_Reads, SAcomplete, GAcomplete):
        currentLevel = Gadgets_Reads[0]
        currentRoom = Gadgets_Reads[1]
        heldGadget = Gadgets_Reads[2]
        gadgetStateFromServer = Gadgets_Reads[3]
        crossGadget = Gadgets_Reads[4]
        squareGadget = Gadgets_Reads[5]
        circleGadget = Gadgets_Reads[6]
        triangleGadget = Gadgets_Reads[7]
        menuState = Gadgets_Reads[8]
        menuState2 = Gadgets_Reads[9]
        punchVisualAddress = Gadgets_Reads[10]
        gameState = Gadgets_Reads[11]
        currentGadgets = Gadgets_Reads[12]
        # print(currentGadgets)
        gadgets_Writes = []
        punch_Guards = []
        punch_Writes = []

        if gameState == RAM.gameState['InLevel']:

            # Add radar to races if the level has been cleared and the player has radar, to allow radaring Jake
            if (currentLevel == 0x07):
                if (AEItem.Radar.value in currentGadgets) and (SAcomplete == 25):
                    gadgets_Writes += [(RAM.triangleGadgetAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
            elif (currentLevel == 0x0E):
                if (AEItem.Radar.value in currentGadgets) and (GAcomplete == 25):
                    gadgets_Writes += [(RAM.triangleGadgetAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                # If the current level is Gladiator Attack, the Sky Flyer is currently equipped, and the player does not have the Sky Flyer: unequip it
                if (heldGadget == 6) and (gadgetStateFromServer & 64 == 0):
                    gadgets_Writes += [(RAM.crossGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                    gadgets_Writes += [(RAM.heldGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
        # Unequip the Time Net if it was shuffled. Note that just checking the Net option is not sufficient to known if the net was actually shuffled - we need to ensure there are locations in this world that don't require net to be sure.
        if ctx.slot_data["shufflenet"] == ShuffleNetOption.option_true and (
                ctx.slot_data["coin"] == CoinOption.option_true or ctx.slot_data[
            "mailbox"] == MailboxOption.option_true):
            if (crossGadget == 1) and (gadgetStateFromServer & 2 == 0):
                gadgets_Writes += [(RAM.crossGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]

        # Equip the selected starting gadget onto the triangle button. Stun Club is the default and doesn't need changing. Additionally, in the "none" case, switch the selection to the Time Net if it wasn't shuffled.
        if ((heldGadget == 0) and (gadgetStateFromServer % 2 == 0)):
            if ctx.slot_data["gadget"] == GadgetOption.option_radar:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                triangleGadget = 0x02
            elif ctx.slot_data["gadget"] == GadgetOption.option_sling:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x03.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x03.to_bytes(1, "little"), "MainRAM")]
                triangleGadget = 0x03
            elif ctx.slot_data["gadget"] == GadgetOption.option_hoop:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x04.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x04.to_bytes(1, "little"), "MainRAM")]
                triangleGadget = 0x04
            elif ctx.slot_data["gadget"] == GadgetOption.option_flyer:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x06.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x06.to_bytes(1, "little"), "MainRAM")]
                triangleGadget = 0x06
            elif ctx.slot_data["gadget"] == GadgetOption.option_car:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x07.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x07.to_bytes(1, "little"), "MainRAM")]
                triangleGadget = 0x07
            elif ctx.slot_data["gadget"] == GadgetOption.option_punch:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                triangleGadget = 0x05
            elif ctx.slot_data["gadget"] == GadgetOption.option_none or ctx.slot_data["gadget"] == GadgetOption.option_waternet:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                if ctx.slot_data["shufflenet"] == ShuffleNetOption.option_true:
                    gadgets_Writes += [(RAM.heldGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                elif ctx.slot_data["shufflenet"] == ShuffleNetOption.option_false:
                    gadgets_Writes += [(RAM.heldGadgetAddress, 0x01.to_bytes(1, "little"), "MainRAM")]

        # If Auto-Equip is on, still checks to exclude races from it
        if self.autoequip == 1 and (currentRoom != 19 and currentRoom != 36):
            if currentGadgets :
                boolCrossGadget = crossGadget  == 0xFF
                boolSquareGadget = squareGadget == 0xFF
                boolCircleGadget = circleGadget == 0xFF
                boolTriangleGadget = triangleGadget == 0xFF
                boolFreeSpace = boolCrossGadget or boolSquareGadget or boolCircleGadget or boolTriangleGadget
                boolNoGadgets = boolCrossGadget and boolSquareGadget and boolCircleGadget and boolTriangleGadget
                if boolFreeSpace:
                    for x in range(len(currentGadgets)):
                        gadget = gadgetsValues[currentGadgets[x]]
                        boolGadgetOnCross = crossGadget == gadget
                        boolGadgetOnSquare = squareGadget == gadget
                        boolGadgetOnCircle = circleGadget == gadget
                        boolGadgetOnTriangle = triangleGadget == gadget
                        boolGadgetAlreadyOn = boolGadgetOnCross or boolGadgetOnSquare or boolGadgetOnCircle or boolGadgetOnTriangle
                        if not boolGadgetAlreadyOn:
                            if boolCrossGadget:
                                crossGadget = gadget
                                gadgets_Writes += [(RAM.crossGadgetAddress, gadget.to_bytes(1, "little"), "MainRAM")]
                                if boolNoGadgets:
                                    gadgets_Writes += [(RAM.heldGadgetAddress, gadget.to_bytes(1, "little"), "MainRAM")]
                                    boolNoGadgets = False
                            elif boolSquareGadget:
                                squareGadget = gadget
                                gadgets_Writes += [(RAM.squareGadgetAddress, gadget.to_bytes(1, "little"), "MainRAM")]
                            elif boolCircleGadget:
                                circleGadget = gadget
                                gadgets_Writes += [(RAM.circleGadgetAddress, gadget.to_bytes(1, "little"), "MainRAM")]
                            elif boolTriangleGadget:
                                triangleGadget = gadget
                                gadgets_Writes += [(RAM.triangleGadgetAddress, gadget.to_bytes(1, "little"), "MainRAM")]

        # Punch Visual glitch in menu fix
        # Replace all values from 0x0E78C0 to 0x0E78DF to this:
        # 0010000000000000E00B00000000000000100000000000000000000000000000
        bytes_ToWrite: bytes = bytes.fromhex(
            "0010000000000000E00B00000000000000100000000000000000000000000000")

        if menuState == 0x00 and menuState2 == 0x01 and gameState != RAM.gameState['LevelSelect']:
            if (AEItem.Punch.value in currentGadgets) and punchVisualAddress.to_bytes(32, "little") != bytes_ToWrite: # and self.replacePunch == True:
                punch_Writes += [(RAM.punchVisualAddress, bytes_ToWrite, "MainRAM")]
                punch_Guards += [(RAM.menuStateAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                punch_Guards += [(RAM.menuState2Address, 0x01.to_bytes(1, "little"), "MainRAM")]
                await bizhawk.guarded_write(ctx.bizhawk_ctx, punch_Writes, punch_Guards)
        await bizhawk.write(ctx.bizhawk_ctx, gadgets_Writes)

    async def Spike_Color_handling(self, ctx: "BizHawkClientContext", Color_Reads, context) -> None:
        if context == "init":
            #print(f"Datastoredskin: {self.DS_spikecolor}")
            await ctx.send_msgs([{
                "cmd": "Get",
                "keys": [f"AE_spikecolor_{ctx.team}_{ctx.slot}"]
            }])
            return
        # grounded = [0x00, 0x01, 0x02, 0x05, 0x07]
        gameState = Color_Reads[0]
        currentspikecolor = Color_Reads[1]
        spikeState2 = Color_Reads[2]
        #print(currentspikecolor)
        #spike_bytes = spikecolor.to_bytes(2, "little")

        presetskins = list(RAM.colortable.keys())
        presetskinsvalues = list(RAM.colortable.values())

        Color_Writes = []

        validgamestates = (RAM.gameState['InLevel'], RAM.gameState['InLevelTT'],RAM.gameState['TimeStation'])
        # Does not execute the function if you not in a level or TimeStation

        if (gameState not in validgamestates):
            return None

        # Check if you got a skin in Slot_data/Datastorage
        if self.DS_spikecolor != -2 and self.DS_spikecolor is not None:
            # If it is a tuple,convert it back to string
            if type(self.DS_spikecolor) is tuple:
                # Transfer from tuple to other types
                self.DS_spikecolor = self.DS_spikecolor[0]
            if type(self.DS_spikecolor) is str:
                if str(self.DS_spikecolor).lower() in presetskins:
                    spikecolor = presetskins.index(str(self.DS_spikecolor).lower())
                    if self.DS_spikecolor == "vanilla":
                        customspikecolor = "vanilla"
                    else:
                        customspikecolor = presetskinsvalues[presetskins.index(str(self.DS_spikecolor).lower())]
                else:
                    # Not in preset skins, treat as custom
                    spikecolor = -1
                    customspikecolor = int(self.DS_spikecolor,16)
            elif type(self.DS_spikecolor) is int:
                # If the value is of type "int", it is a preset number from Slot_data or Hex RGB value
                if int(self.DS_spikecolor) in presetskinsvalues:
                    colorindex = presetskinsvalues.index(int(self.DS_spikecolor))
                    spikecolor = colorindex
                    customspikecolor = presetskinsvalues[colorindex]
                else:
                    # Not in vanilla skins, treat as custom
                    spikecolor = -1
                    customspikecolor = self.DS_spikecolor
            else:
                #Non-valid type, treat as "Vanilla"
                spikecolor = 0
                customspikecolor = "vanilla"
        else:
            #No Datastorage yet,use slotdata
            spikecolor = ctx.slot_data["spikecolor"]
            customspikecolor = ctx.slot_data["customspikecolor"]

        # Check which skin to choose from the list
        if spikecolor == 0:
            customspikecolor = "vanilla"
            skin_to_bytes = 0xFFFFFF.to_bytes(3, "big")
        elif spikecolor != -1:
            # Preset Skin
            customspikecolor = presetskinsvalues[spikecolor]
            skin_to_bytes = customspikecolor.to_bytes(3, "little")
        else:
            # Check for a Custom Skin
            error = False
            try:
                #Custom Skin validation
                # If it passes this check, it's safe to say it's at least Hexadecimal
                skin_to_bytes = bytes.fromhex(customspikecolor)
                customspikecolor = int.from_bytes(skin_to_bytes, "big")
            except:
                error = True
            if error:
                try:
                    #Custom Skin validation (int)
                    # If it passes this check, it's safe to say it's at least Hexadecimal
                    skin_to_bytes = customspikecolor.to_bytes(3, "big")
                    customspikecolor = format(customspikecolor, 'X')
                except:
                    spikecolor = 0
                    customspikecolor = "vanilla"
                    skin_to_bytes = 0xFFFFFF.to_bytes(3, "big")

        if self.changeSkin == True:
            await ctx.send_msgs([{
                "cmd": "Set",
                # "key": str(ctx.player_names[ctx.slot]) + "_DIButton",
                "key": f"AE_spikecolor_{ctx.team}_{ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "replace", "value": customspikecolor}]
            }])
            self.changeSkin = False

        # Prevent color updates if value is not vanilla
        if customspikecolor != "vanilla":

            Color_Writes += [(RAM.spike_RedColorUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            Color_Writes += [(RAM.spike_GreenColorUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            Color_Writes += [(RAM.spike_BlueColorUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            Color_Writes += [(RAM.spikeSkinPalette, RAM.skinpallettable["white"].to_bytes(3, "little"), "MainRAM")]

        else:
            Color_Writes += [(RAM.spike_RedColorUpdate, 0xA20200F4.to_bytes(4, "little"), "MainRAM")]
            Color_Writes += [(RAM.spike_GreenColorUpdate, 0xA20200F5.to_bytes(4, "little"), "MainRAM")]
            Color_Writes += [(RAM.spike_BlueColorUpdate, 0xA20200F6.to_bytes(4, "little"), "MainRAM")]
            Color_Writes += [(RAM.spikeSkinPalette, RAM.skinpallettable["vanilla"].to_bytes(3, "little"), "MainRAM")]

        if currentspikecolor != customspikecolor and spikeState2 not in [0x2B,0x4D]:
            # Overwrite the skin if it not currently in place
            # *And if spike is not burning in Ice/Lava
            Color_Writes += [(RAM.spikeColor, skin_to_bytes, "MainRAM")]


        if Color_Writes:
            await bizhawk.write(ctx.bizhawk_ctx, Color_Writes)

    async def Credits_handling(self, ctx: "BizHawkClientContext", Credits_Reads) -> None:
        currentRoom = Credits_Reads[0]
        gameState = Credits_Reads[1]
        S1_Cutscene_Redirection = hex(Credits_Reads[2])
        S2_Cutscene_Redirection = hex(Credits_Reads[3])
        Credits_Writes = []

        # Does not execute the function if you not in a level (Or custscene of S1)
        if (gameState not in (RAM.gameState['InLevel'], RAM.gameState['InLevelTT'],RAM.gameState['Cutscene2'])):
            return None

        if gameState == RAM.gameState['Cutscene2']:
            if S1_Cutscene_Redirection != 0x2403000D:
                Credits_Writes += [(RAM.S1_Cutscene_Redirection, 0x2403000D.to_bytes(4, "little"), "MainRAM")]

        if currentRoom == 87:
            if S2_Cutscene_Redirection != 0x2403000D:
                Credits_Writes += [(RAM.S2_Cutscene_Redirection, 0x2403000D.to_bytes(4, "little"), "MainRAM")]
        await bizhawk.write(ctx.bizhawk_ctx, Credits_Writes)


    async def PPM_Optimizations(self, ctx: "BizHawkClientContext", PPM_Reads) -> None:
        currentRoom = PPM_Reads[0]
        currentLevel = PPM_Reads[1]
        gameState = PPM_Reads[2]
        S2_CutsceneState = PPM_Reads[3]
        S2_GlobalCutsceneState = PPM_Reads[4]
        token = self.tokencount


        PPM_Writes = []

        # print("Current/Next Room is Specter 1 room")
        if ctx.slot_data["goal"] == GoalOption.option_ppmtoken and gameState in (RAM.gameState["InLevel"],RAM.gameState["InLevelTT"],RAM.gameState["TimeStation"],RAM.gameState["LevelSelect"]):
            # print("with the correct goal")
            if token < min(ctx.slot_data["requiredtokens"], ctx.slot_data["totaltokens"]):
                #if currentRoom == 87 and gameState == RAM.gameState["InLevel"]:
                # Prevent the fight if not enough tokens
                #if S2_CutsceneState != 0x05:
                #PPM_Writes += [(RAM.S2_CutsceneState, 0x05.to_bytes(1, "little"), "MainRAM")]
                if S2_GlobalCutsceneState != 0x05:
                    PPM_Writes += [(RAM.S2_GlobalCutsceneState, 0x05.to_bytes(1, "little"), "MainRAM")]
            else:
                # Allow the fight if not already completed
                if self.PPM_Completed == False:
                    #if S2_CutsceneState == 0x05:
                    #PPM_Writes += [(RAM.S2_CutsceneState, 0x00.to_bytes(1, "little"), "MainRAM")]
                    if S2_GlobalCutsceneState == 0x05:
                        PPM_Writes += [(RAM.S2_GlobalCutsceneState, 0x00.to_bytes(1, "little"), "MainRAM")]
        await bizhawk.write(ctx.bizhawk_ctx, PPM_Writes)

    async def MM_Optimizations(self, ctx: "BizHawkClientContext", MM_Reads) -> None:
        currentRoom = MM_Reads[0]
        currentLevel = MM_Reads[1]
        gameState = MM_Reads[2]
        NearbyRoom = MM_Reads[3]
        transitionPhase = MM_Reads[4]
        MM_Jake_Defeated = MM_Reads[5]
        MM_Lobby_DoubleDoor = MM_Reads[6]
        MM_Lobby_DoorDetection = MM_Reads[7]
        MM_Lobby_DoubleDoor_Open = MM_Reads[8]
        MM_Jake_DefeatedAddress = MM_Reads[9]
        MM_Natalie_RescuedAddress = MM_Reads[10]
        MM_Natalie_Rescued = MM_Reads[11]
        MM_Natalie_Rescued_Local = MM_Reads[12]
        MM_Professor_Rescued = MM_Reads[13]
        S1_P1_FightTrigger = MM_Reads[14]
        MM_Clown_State = MM_Reads[15]
        MM_AlertRoom_ButtonPressed = MM_Reads[16]

        MM_Writes = []
        SpecterLevels = (RAM.levels['Specter'], RAM.levels['S_Jake'], RAM.levels['S_Circus'], RAM.levels['S_Coaster'], RAM.levels['S_Western Land'], RAM.levels['S_Castle'])
        writes = []
        guards = []

        # Only do the MM_Optimizations IN Monkey Madness, else revert back to default behavior and do nothing else
        if currentLevel not in SpecterLevels or gameState == RAM.gameState['LevelSelect']:
            writes += [(RAM.MM_Lobby_DoorDetection, 0x8C820000.to_bytes(4, "little"), "MainRAM")]
            guards += [(RAM.MM_Lobby_DoorDetection, 0x8C800000.to_bytes(4, "little"), "MainRAM")]
            await bizhawk.guarded_write(ctx.bizhawk_ctx, writes, guards)
            return None
        # print("MM_Optimizations")

        if MM_Jake_Defeated == 1:
            MM_Writes += [(RAM.MM_Jake_DefeatedAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
            MM_Writes += [(RAM.temp_MM_Jake_DefeatedAddress, 0x01.to_bytes(1, "little"), "MainRAM")]
        else:
            MM_Writes += [(RAM.MM_Jake_DefeatedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
            MM_Writes += [(RAM.temp_MM_Jake_DefeatedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]

        if MM_Professor_Rescued == 1:
            MM_Writes += [(RAM.MM_Professor_RescuedAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
            MM_Writes += [(RAM.temp_MM_Professor_RescuedAddress, 0x01.to_bytes(1, "little"), "MainRAM")]
        else:
            MM_Writes += [(RAM.MM_Professor_RescuedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
            MM_Writes += [(RAM.temp_MM_Professor_RescuedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]

        if MM_Natalie_Rescued == 1:
            MM_Writes += [(RAM.MM_Natalie_RescuedAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
            MM_Writes += [(RAM.temp_MM_Natalie_RescuedAddress, 0x01.to_bytes(1, "little"), "MainRAM")]
        else:
            MM_Writes += [(RAM.MM_Natalie_RescuedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
            MM_Writes += [(RAM.temp_MM_Natalie_RescuedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]

        # Natalie's Rescue Coffin room detection (When in the room)
        if currentRoom == 76:
            if MM_Natalie_Rescued_Local == 0x01:
                MM_Writes += [(RAM.temp_MM_Natalie_RescuedAddress, 0x01.to_bytes(1, "little"), "MainRAM")]

        # Natalie's Cutscene reset (When transitioning to Haunted Mansion)
        if NearbyRoom == 75 and MM_Natalie_Rescued != 0x01 and transitionPhase == RAM.transitionPhase["InTransition"]:
            MM_Writes += [(RAM.MM_Natalie_CutsceneState, 0x00.to_bytes(1, "little"), "MainRAM")]

        # Clown cutscene reset
        if NearbyRoom == 71 and MM_Professor_Rescued != 0x01 and transitionPhase == RAM.transitionPhase["InTransition"]:
            if MM_Clown_State == 0x05:
                MM_Writes += [(RAM.MM_Clown_State, 0x00.to_bytes(1, "little"), "MainRAM")]

        # When going into the MM_Lobby, disable the Door Detection
        if (NearbyRoom == 69 and transitionPhase == RAM.transitionPhase["InTransition"]) or (currentRoom == 69 and transitionPhase != RAM.transitionPhase["InTransition"]):
            # print("Next room == Lobby")
            if MM_Lobby_DoorDetection != 0x8C800000:
                MM_Writes += [(RAM.MM_Lobby_DoorDetection, 0x8C800000.to_bytes(4, "little"), "MainRAM")]
        elif (NearbyRoom != 69 and transitionPhase == RAM.transitionPhase["InTransition"]):
            if MM_Lobby_DoorDetection != 0x8C820000:
                MM_Writes += [(RAM.MM_Lobby_DoorDetection, 0x8C820000.to_bytes(4, "little"), "MainRAM")]

        # MM_Lobby door handling
        if currentRoom == 69 and transitionPhase != RAM.transitionPhase["InTransition"]:
            # Open the Electric Door and remove the Hitbox blocking you to go to Go Karz room (Jake fight)
            MM_Writes += [(RAM.MM_Lobby_JakeDoorFenceAddress, 0x01.to_bytes(1, "little"), "MainRAM")]
            MM_Writes += [(RAM.MM_Lobby_JakeDoor_HitboxAddress, 0x80.to_bytes(1, "little"), "MainRAM")]
            MM_Writes += [(RAM.MM_Lobby_DoubleDoor_OpenAddress, 0x05.to_bytes(1, "little"), "MainRAM")]

            door_addresses = RAM.doors_addresses

            if currentRoom in door_addresses.keys():
                doorlist_keys = list(door_addresses[currentRoom].keys())
                doorlist_values = list(door_addresses[currentRoom].values())

                # print(doorlist_values)
                for x in range(len(doorlist_keys)):
                    Door_writes = []
                    Door_guards = [(RAM.currentRoomIdAddress, currentRoom.to_bytes(1, "little"), "MainRAM")]
                    # lamp_values2 = list(lamp_values[x].__str__().replace("[", "").replace("]", "").split(","))
                    door_values = list(doorlist_values[x])
                    # print(doorlist_values[x])
                    door_bytes = door_values[0]
                    door_openvalue = door_values[1].to_bytes(door_bytes, "little")
                    door_closedvalue = door_values[2].to_bytes(door_bytes, "little")
                    door_address = (doorlist_keys[x])
                    # print(door_address)
                    if MM_Lobby_DoubleDoor == 0:
                        # Close the door if opened
                        Door_writes += [(door_address, door_closedvalue, "MainRAM")]
                        Door_guards += [(door_address, door_openvalue, "MainRAM")]
                    else:
                        # Open the door if it's closed
                        Door_writes += [(door_address, door_openvalue, "MainRAM")]
                        Door_guards += [(door_address, door_closedvalue, "MainRAM")]

                    await bizhawk.guarded_write(ctx.bizhawk_ctx, Door_writes, Door_guards)
        # Push the "Alert" button if BG is already caught and the button is not pressed (From /syncprogress or !collect)
        if currentRoom == 85 and MM_AlertRoom_ButtonPressed == 0x00 and transitionPhase != 6:
            BG_address = RAM.monkeyListGlobal.get(204)
            localBG_address = RAM.monkeyListLocal.get(currentRoom).get(204)
            Monkey_Reads = []

            Monkey_Reads += [(BG_address, 1, "MainRAM")]
            Monkey_Reads += [(localBG_address, 1, "MainRAM")]
            Monkey_Values = await bizhawk.read(ctx.bizhawk_ctx, Monkey_Reads)

            BG_caught = int.from_bytes(Monkey_Values[0], "little")
            local_BG_caught = int.from_bytes(Monkey_Values[1], "little")
            # This means BG is set as caught and the button is not pressed
            if BG_caught in (0x02,0x03) or local_BG_caught in (0x02,0x03):
                MM_Writes += [(RAM.MM_AlertRoom_ButtonPressed, 0x01.to_bytes(1, "little"), "MainRAM")]
                MM_Writes += [(RAM.MM_AlertRoom_CutsceneTrigger1, 0x02.to_bytes(1, "little"), "MainRAM")]
                MM_Writes += [(RAM.MM_AlertRoom_BGCanPushButton, 0x00.to_bytes(1, "little"), "MainRAM")]
        # Prevent Specter 1 fight for Specter 1 token goal when not having enough tokens.
        token = self.tokencount
        if (NearbyRoom == 83 and transitionPhase == RAM.transitionPhase["InTransition"]) or (currentRoom == 83 and transitionPhase != RAM.transitionPhase["InTransition"]):
            # print("Current/Next Room is Specter 1 room")
            if ctx.slot_data["goal"] == GoalOption.option_mmtoken:
                # print("with the correct goal")
                if token < min(ctx.slot_data["requiredtokens"], ctx.slot_data["totaltokens"]):
                    # print("and insufficient tokens")
                    # MM_Writes += [(RAM.S1_P1_Life, 0x06.to_bytes(1, "little"), "MainRAM")]
                    # Prevent the fight
                    MM_Writes += [(RAM.S1_P1_FightTrigger, 0x0D.to_bytes(1, "little"), "MainRAM")]
                else:
                    # Allow the fight
                    if S1_P1_FightTrigger == 0x0D:
                        MM_Writes += [(RAM.S1_P1_FightTrigger, 0x00.to_bytes(1, "little"), "MainRAM")]

        await bizhawk.write(ctx.bizhawk_ctx, MM_Writes)


    async def permanent_buttons_handling(self, ctx: "BizHawkClientContext", Button_Reads) -> None:
        currentRoom = Button_Reads[0]
        gameState = Button_Reads[1]
        DI_Button_Pressed = Button_Reads[2]
        CrC_Water_ButtonPressed = Button_Reads[3]
        CrC_Basement_ButtonPressed = Button_Reads[4]
        TVT_Lobby_ButtonPressed = Button_Reads[5]
        MM_MonkeyHead_ButtonPressed = Button_Reads[6]
        MM_Painting_ButtonPressed = Button_Reads[7]
        DR_Block_Pushed = Button_Reads[8]
        transitionPhase = Button_Reads[9]

        Button_Writes = []
        Button_Guards = []
        # Does not execute the function if you not in a level
        if (gameState not in (RAM.gameState['InLevel'],RAM.gameState['InLevelTT'])):
            return None

        # print("permanent_buttons_handling")
        # If CrC_ButtonRoom button is pressed,send the value "{Player}_CrCWaterButton" to the server's Datastorage
        # This behavior unlocks the door permanently after you press the button once.
        if currentRoom == 11 and transitionPhase != RAM.transitionPhase["InTransition"]:
            if DR_Block_Pushed == 0x01:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    # "key": str(ctx.player_names[ctx.slot]) + "_DIButton",
                    "key": f"AE_DR_Block_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "replace", "value": 1}]
                }])

        if currentRoom == 28 and transitionPhase != RAM.transitionPhase["InTransition"]:
            if DI_Button_Pressed == 0x01:
                if self.DIButton != 1:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        # "key": str(ctx.player_names[ctx.slot]) + "_DIButton",
                        "key": f"AE_DIButton_{ctx.team}_{ctx.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": 1}]
                    }])

        if currentRoom == 49 and transitionPhase != RAM.transitionPhase["InTransition"]:
            if CrC_Water_ButtonPressed == 0x01:
                if self.CrCWaterButton != 1:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        # "key": str(ctx.player_names[ctx.slot]) + "_CrCWaterButton",
                        "key": f"AE_CrCWaterButton_{ctx.team}_{ctx.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": 1}]
                    }])

        # if currentRoom == 47:
        #     if CrC_Basement_ButtonPressed == 0x01:
        #         if self.CrCBasementButton != 1:
        #             await ctx.send_msgs([{
        #                 "cmd": "Set",
        #                 "key": str(ctx.player_names[ctx.slot]) + "_CrCBasementButton",
        #                 "default": 0,
        #                 "want_reply": False,
        #                 "operations": [{"operation": "replace", "value": 1}]
        #             }])

        if currentRoom == 65 and transitionPhase != RAM.transitionPhase["InTransition"]:
            if TVT_Lobby_ButtonPressed == 0x01:
                if self.TVT_Lobby_Button != 1:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        # "key": str(ctx.player_names[ctx.slot]) + "_TVT_Lobby_Button",
                        "key": f"AE_TVT_Lobby_Button_{ctx.team}_{ctx.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": 1}]
                    }])

        # Detection of Interior Climb button press (MonkeyHead Room)
        if currentRoom == 84 and transitionPhase != RAM.transitionPhase["InTransition"]:
            if MM_MonkeyHead_ButtonPressed == 0x01:
                if self.MM_MonkeyHead_Button != 1:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"AE_MM_MonkeyHead_Button_{ctx.team}_{ctx.slot}",
                        #"key": str(ctx.player_names[ctx.slot]) + "_MM_MonkeyHead_Button",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": 1}]
                    }])

        # Detection of Painting button press (Outside Climb)
        if currentRoom == 82 and transitionPhase != RAM.transitionPhase["InTransition"]:
            if MM_Painting_ButtonPressed == 0x01:
                if self.MM_Painting_Button != 1:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"AE_MM_Painting_Button_{ctx.team}_{ctx.slot}",
                        #"key": str(ctx.player_names[ctx.slot]) + "_MM_Painting_Button",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": 1}]
                    }])

        # Dexter's Island Slide Room button unlock
        if currentRoom == 28 and transitionPhase != RAM.transitionPhase["InTransition"]:
            if self.DIButton != 1:
                await ctx.send_msgs([{
                    "cmd": "Get",
                    "keys": [f"AE_DIButton_{ctx.team}_{ctx.slot}"]
                }])
            if self.DIButton == 1:
                buttonDoors_toggles = RAM.buttonDoors_toggles.get("DI_Button")
                buttonDoors_keys = list(buttonDoors_toggles.keys())
                buttonDoors_values = list(buttonDoors_toggles.values())

                button_writes2 = []
                button_Guards = [(RAM.currentRoomIdAddress, currentRoom.to_bytes(1, "little"), "MainRAM")]
                for x in range(len(buttonDoors_keys)):
                    button_values = list(buttonDoors_values[x])
                    button_bytes = button_values[0]
                    button_openvalue = button_values[1].to_bytes(button_bytes, "little")
                    button_closedvalue = button_values[2].to_bytes(button_bytes, "little")
                    button_address = (buttonDoors_keys[x])
                    button_writes2 += [(button_address, button_openvalue, "MainRAM")]
                    button_Guards += [(button_address, button_closedvalue, "MainRAM")]
                await bizhawk.guarded_write(ctx.bizhawk_ctx, button_writes2, button_Guards)

        # Crumbling Castle Water Room door unlock check
        if currentRoom == 45 and transitionPhase != RAM.transitionPhase["InTransition"]:
            if self.CrCWaterButton != 1:
                await ctx.send_msgs([{
                    "cmd": "Get",
                    "keys": [f"AE_CrCWaterButton_{ctx.team}_{ctx.slot}"]
                }])
            if self.CrCWaterButton == 1:
                buttonDoors_toggles = RAM.buttonDoors_toggles.get("CrCWaterButton")
                buttonDoors_keys = list(buttonDoors_toggles.keys())
                buttonDoors_values = list(buttonDoors_toggles.values())

                button_writes2 = []
                button_Guards = [(RAM.currentRoomIdAddress, currentRoom.to_bytes(1, "little"), "MainRAM")]
                for x in range(len(buttonDoors_keys)):
                    button_values = list(buttonDoors_values[x])
                    button_bytes = button_values[0]
                    button_openvalue = button_values[1].to_bytes(button_bytes, "little")
                    button_closedvalue = button_values[2].to_bytes(button_bytes, "little")
                    button_address = (buttonDoors_keys[x])
                    button_writes2 += [(button_address, button_openvalue, "MainRAM")]
                    button_Guards += [(button_address, button_closedvalue, "MainRAM")]
                await bizhawk.guarded_write(ctx.bizhawk_ctx, button_writes2, button_Guards)

        # Crumbling Castle Basement Room door unlock check
        # if currentRoom == 47:
        #     if CrC_Basement_DoorVisual1 != 0x00:
        #         if self.CrCBasementButton != 1:
        #             await ctx.send_msgs([{
        #                 "cmd": "Get",
        #                 "keys": [str(ctx.player_names[ctx.slot]) + "_CrCBasementButton"]
        #             }])
        #         if self.CrCBasementButton == 1:
        #             Button_Writes += [(RAM.CrC_Basement_DoorHitBox1, 0xF200F808.to_bytes(4, "little"), "MainRAM")]
        #             Button_Writes += [(RAM.CrC_Basement_DoorHitBox2, 0x0008FB00.to_bytes(4, "little"), "MainRAM")]
        #             Button_Writes += [(RAM.CrC_Basement_DoorHitBox3, 0x01000400.to_bytes(4, "little"), "MainRAM")]
        #             Button_Writes += [(RAM.CrC_Basement_DoorVisual1, 0x00.to_bytes(1, "little"), "MainRAM")]
        #             Button_Writes += [(RAM.CrC_Basement_DoorVisual2, 0xF0.to_bytes(1, "little"), "MainRAM")]
        #             Button_Writes += [(RAM.CrC_Basement_ButtonVisual1, 0x80178ADC.to_bytes(4, "little"), "MainRAM")]
        #             Button_Writes += [(RAM.CrC_Basement_ButtonVisual2, 0x80178AF4.to_bytes(4, "little"), "MainRAM")]
        #             Button_Writes += [(RAM.CrC_Basement_ButtonVisual3, 0x80178C14.to_bytes(4, "little"), "MainRAM")]
        #             Button_Writes += [(RAM.CrC_Basement_ButtonVisual4, 0x80178B0C.to_bytes(4, "little"), "MainRAM")]

        # TV Tower water draining check
        if currentRoom == 65 and transitionPhase != RAM.transitionPhase["InTransition"]:
            if self.TVT_Lobby_Button != 1:
                await ctx.send_msgs([{
                    "cmd": "Get",
                    "keys": [f"AE_TVT_Lobby_Button_{ctx.team}_{ctx.slot}"]
                }])
            if self.TVT_Lobby_Button == 1:
                buttonDoors_toggles = RAM.buttonDoors_toggles.get("TVT_Lobby_Button")
                buttonDoors_keys = list(buttonDoors_toggles.keys())
                buttonDoors_values = list(buttonDoors_toggles.values())

                button_writes2 = []
                button_Guards = [(RAM.currentRoomIdAddress, currentRoom.to_bytes(1, "little"), "MainRAM")]
                for x in range(len(buttonDoors_keys)):
                    button_values = list(buttonDoors_values[x])
                    button_bytes = button_values[0]
                    button_openvalue = button_values[1].to_bytes(button_bytes, "little")
                    button_closedvalue = button_values[2].to_bytes(button_bytes, "little")
                    button_address = (buttonDoors_keys[x])
                    button_writes2 += [(button_address, button_openvalue, "MainRAM")]
                    button_Guards += [(button_address, button_closedvalue, "MainRAM")]
                await bizhawk.guarded_write(ctx.bizhawk_ctx, button_writes2, button_Guards)

        # Monkey Madness Castle Lobby checks
        if currentRoom == 80 and transitionPhase != RAM.transitionPhase["InTransition"]:
            # Monkey Madness Monkey Head door unlock check
            if self.MM_MonkeyHead_Button != 1:
                await ctx.send_msgs([{
                    "cmd": "Get",
                    "keys": [f"AE_MM_MonkeyHead_Button_{ctx.team}_{ctx.slot}"]
                }])
            if self.MM_MonkeyHead_Button == 1:
                buttonDoors_toggles = RAM.buttonDoors_toggles.get("MM_MonkeyHead_Button")
                buttonDoors_keys = list(buttonDoors_toggles.keys())
                buttonDoors_values = list(buttonDoors_toggles.values())

                button_writes2 = []
                button_Guards = [(RAM.currentRoomIdAddress, currentRoom.to_bytes(1, "little"), "MainRAM")]
                for x in range(len(buttonDoors_keys)):
                    button_values = list(buttonDoors_values[x])
                    button_bytes = button_values[0]
                    button_openvalue = button_values[1].to_bytes(button_bytes, "little")
                    button_closedvalue = button_values[2].to_bytes(button_bytes, "little")
                    button_address = (buttonDoors_keys[x])
                    button_writes2 += [(button_address, button_openvalue, "MainRAM")]
                    button_Guards += [(button_address, button_closedvalue, "MainRAM")]
                await bizhawk.guarded_write(ctx.bizhawk_ctx, button_writes2, button_Guards)

            # Monkey Madness Painting door unlock check
            if self.MM_Painting_Button != 1:
                await ctx.send_msgs([{
                    "cmd": "Get",
                    "keys": [f"AE_MM_Painting_Button_{ctx.team}_{ctx.slot}"]
                }])
            if self.MM_Painting_Button == 1:
                buttonDoors_toggles = RAM.buttonDoors_toggles.get("MM_Painting_Button")
                buttonDoors_keys = list(buttonDoors_toggles.keys())
                buttonDoors_values = list(buttonDoors_toggles.values())

                button_writes2 = []
                button_Guards = [(RAM.currentRoomIdAddress, currentRoom.to_bytes(1, "little"), "MainRAM")]
                for x in range(len(buttonDoors_keys)):
                    button_values = list(buttonDoors_values[x])
                    button_bytes = button_values[0]
                    button_openvalue = button_values[1].to_bytes(button_bytes, "little")
                    button_closedvalue = button_values[2].to_bytes(button_bytes, "little")
                    button_address = (buttonDoors_keys[x])
                    button_writes2 += [(button_address, button_openvalue, "MainRAM")]
                    button_Guards += [(button_address, button_closedvalue, "MainRAM")]
                await bizhawk.guarded_write(ctx.bizhawk_ctx, button_writes2, button_Guards)

        #await bizhawk.write(ctx.bizhawk_ctx, Button_Writes)


    async def lamps_unlocks_handling(self, ctx: "BizHawkClientContext", Lamps_Reads) -> None:
        # Variables
        gameState = Lamps_Reads[0]
        currentRoom = Lamps_Reads[1]
        NearbyRoom = Lamps_Reads[2]
        localLampsUpdate = Lamps_Reads[3]
        globalLampsUpdate = Lamps_Reads[4]
        transitionPhase = Lamps_Reads[5]
        WSW_RoomState = Lamps_Reads[6]
        lockCamera = Lamps_Reads[7]

        # Deactivate Monkeys detection for lamps and switch to manual door opening if lamp shuffle is activated
        # Condition for some rooms that require the same addresses to function properly
        specialrooms = [41, 44, 67, 75, 76]

        Lamps_writes = []

        # Does not execute the function if you not in a level
        if (gameState not in (RAM.gameState['InLevel'], RAM.gameState['InLevelTT'])):
            return None

        # print("lamps_unlocks_handling")

        lampDoors_toggles = RAM.lampDoors_toggles
        # Trigger Monkey Lamps depending on Lamp states
        boolOpenDoor = False

        # Update lamp doors depending on value
        # print(lampDoors_toggles.keys())
        GotLamp = False
        RoomHaveLamp = False
        if currentRoom in localLampsUpdate:
            GotLamp = localLampsUpdate[currentRoom] == 0x01
            RoomHaveLamp = True
        elif currentRoom in globalLampsUpdate:
            GotLamp = globalLampsUpdate[currentRoom] == 0x01
            RoomHaveLamp = True

        NearbyRoomHaveLamp = False
        if NearbyRoom in localLampsUpdate:
            NearbyRoomHaveLamp = True
        elif NearbyRoom in globalLampsUpdate:
            NearbyRoomHaveLamp = True

        if ctx.slot_data["lamp"] == 0x00:
            # If the room had a lamp, activate all values while going in the transition
            if (NearbyRoomHaveLamp == True and transitionPhase == RAM.transitionPhase["InTransition"] and (NearbyRoom not in specialrooms)) or (RoomHaveLamp == True and transitionPhase != RAM.transitionPhase["InTransition"]):
                # print("LampRoom")
                Lamps_writes += [(RAM.localLamp_MonkeyDetect, RAM.lampDoors_update['localLamp_MonkeyDetect_ON'].to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_MonkeyDetect1, RAM.lampDoors_update['globalLamp_MonkeyDetect1_ON'].to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_MonkeyDetect2, RAM.lampDoors_update['globalLamp_MonkeyDetect2_ON'].to_bytes(4, "little"), "MainRAM")]
            elif (NearbyRoom in specialrooms and transitionPhase == RAM.transitionPhase["InTransition"]) or (currentRoom in specialrooms):
                #print("SpecialRoom")
                if currentRoom == 41 and WSW_RoomState == 0x00 and lockCamera == 0x80:
                    Lamps_writes += [(RAM.WSW_RoomState, 0x01.to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.localLamp_MonkeyDetect, RAM.lampDoors_update['localLamp_MonkeyDetect_ON'].to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_MonkeyDetect1, RAM.lampDoors_update['globalLamp_MonkeyDetect1_OFF'].to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_MonkeyDetect2, RAM.lampDoors_update['globalLamp_MonkeyDetect2_OFF'].to_bytes(4, "little"), "MainRAM")]
            elif (NearbyRoomHaveLamp == False and transitionPhase == RAM.transitionPhase["InTransition"]) or ((currentRoom not in specialrooms) and (RoomHaveLamp == False)):
                # print("NoLampsRoom")
                Lamps_writes += [(RAM.localLamp_MonkeyDetect, RAM.lampDoors_update['localLamp_MonkeyDetect_OFF'].to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_MonkeyDetect1, RAM.lampDoors_update['globalLamp_MonkeyDetect1_OFF'].to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_MonkeyDetect2, RAM.lampDoors_update['globalLamp_MonkeyDetect2_OFF'].to_bytes(4, "little"), "MainRAM")]
        else:
            if (NearbyRoom in specialrooms and transitionPhase == RAM.transitionPhase["InTransition"]) or currentRoom in specialrooms:
                # print("SpecialRoom")
                if currentRoom == 41 and WSW_RoomState == 0x00 and lockCamera == 0x80:
                    Lamps_writes += [(RAM.WSW_RoomState, 0x01.to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.localLamp_MonkeyDetect, RAM.lampDoors_update['localLamp_MonkeyDetect_ON'].to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_MonkeyDetect1, RAM.lampDoors_update['globalLamp_MonkeyDetect1_OFF'].to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_MonkeyDetect2, RAM.lampDoors_update['globalLamp_MonkeyDetect2_OFF'].to_bytes(4, "little"), "MainRAM")]
            elif (currentRoom not in specialrooms) or transitionPhase == RAM.transitionPhase["InTransition"]:
                # print("NotSpecialRoom")
                Lamps_writes += [(RAM.localLamp_MonkeyDetect, RAM.lampDoors_update['localLamp_MonkeyDetect_OFF'].to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_MonkeyDetect1, RAM.lampDoors_update['globalLamp_MonkeyDetect1_OFF'].to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_MonkeyDetect2, RAM.lampDoors_update['globalLamp_MonkeyDetect2_OFF'].to_bytes(4, "little"), "MainRAM")]

        # You can now have the Lamp Item and bypass the door
        if currentRoom in lampDoors_toggles.keys() and GotLamp:
            lamplist_keys = list(lampDoors_toggles[currentRoom].keys())
            lamplist_values = list(lampDoors_toggles[currentRoom].values())
            Lamps_writes2 = []
            Lamps_Guards = [(RAM.currentRoomIdAddress, currentRoom.to_bytes(1, "little"), "MainRAM")]
            for x in range(len(lamplist_keys)):
                lamp_values = list(lamplist_values[x])
                lamp_bytes = lamp_values[0]
                lamp_openvalue = lamp_values[1].to_bytes(lamp_bytes, "little")
                lamp_closedvalue = lamp_values[2].to_bytes(lamp_bytes, "little")
                lamp_address = (lamplist_keys[x])
                Lamps_writes2 += [(lamp_address, lamp_openvalue, "MainRAM")]
                Lamps_Guards += [(lamp_address, lamp_closedvalue, "MainRAM")]
            await bizhawk.guarded_write(ctx.bizhawk_ctx, Lamps_writes2, Lamps_Guards)
        await bizhawk.write(ctx.bizhawk_ctx, Lamps_writes)


    async def specialitems_handling(self, ctx: "BizHawkClientContext", SpecialItems_Reads) -> None:
        gameState = SpecialItems_Reads[0]
        gotMail = SpecialItems_Reads[1]
        spikeState = SpecialItems_Reads[2]
        spikeState2 = SpecialItems_Reads[3]
        menuState = SpecialItems_Reads[4]
        menuState2 = SpecialItems_Reads[5]
        currentGadgets = SpecialItems_Reads[6]
        currentRoom = SpecialItems_Reads[7]
        gameRunning = SpecialItems_Reads[8]
        DS_spikeColor = SpecialItems_Reads[9]
        heldGadget = SpecialItems_Reads[10]
        CatchingState = SpecialItems_Reads[11]
        cookies = SpecialItems_Reads[12]

        SpecialItems_Writes = []
        SpecialItems_Guards = []

        # Gamestate
        valid_gameStates = (RAM.gameState['InLevel'], RAM.gameState['InLevelTT'], RAM.gameState['TimeStation'], RAM.gameState['Jake'])
        grounded = [0x00, 0x01, 0x02, 0x05, 0x07]
        is_grounded = (spikeState2 in grounded)
        is_catching = (CatchingState == 0x08)
        is_dead = (cookies == 0)
        in_menu = (menuState == 0 and menuState2 == 1)
        reading_mail = (gotMail == 0x01) or (gotMail == 0x02)
        is_sliding = (spikeState2 in (0x2F,0x30))
        is_idle = (spikeState == 0x12) and (spikeState2 in {0x80, 0x81, 0x82, 0x83, 0x84})
        in_race = (currentRoom == 19 or currentRoom == 36)
        cannot_control = (gameRunning == 0)
        stunned = (spikeState2 == 0x58)
        StunTrap_incompatible_list = [RAM.items["IcyHotPantsTrap"],RAM.items["StunTrap"],RAM.items["BananaPeelTrap"],RAM.items["MonkeyMashTrap"]]

        if (gameState not in valid_gameStates or in_menu or reading_mail or is_sliding or is_idle or cannot_control or is_catching):
            self.ape_handler.pause = True
            self.rainbow_cookie.pause = True
            self.camera_rotate_trap.pause = True
        else:
            self.ape_handler.pause = False
            self.rainbow_cookie.pause = False
            self.camera_rotate_trap.pause = False

        if not self.specialitem_queue and not self.priority_trap_queue:
            #Exit if no traps
            return None

        else:
            if self.priority_trap_queue:
                item_id = self.priority_trap_queue[0][0]
                item_info = self.priority_trap_queue[0][1]
                IsPriority = True
            else:
                item_id = self.specialitem_queue[0][0]
                item_info = self.specialitem_queue[0][1]
                IsPriority = False

            StunTrap_incompatible = self.stun_trap.is_active and (item_id in StunTrap_incompatible_list)
            # Does not send the traps in these states
            if gameState not in valid_gameStates or in_menu or reading_mail or is_sliding or in_race or is_idle or cannot_control or stunned or StunTrap_incompatible:
                if is_idle:
                    # Trigger a Wake Up for spike. Banana Peel is deadly while Idle
                    SpecialItems_Writes += [(RAM.spikeIdleTimer, 0x0000.to_bytes(2, "little"), "MainRAM")]
                    await bizhawk.write(ctx.bizhawk_ctx, SpecialItems_Writes)
                if not IsPriority:
                    #Not priority
                    if item_info >= 10:
                        # Trap Removed for incompatibility(10 passes)
                        self.specialitem_queue.pop(0)
                    elif StunTrap_incompatible:
                        # Trap moved to the end
                        self.specialitem_queue.insert(len(self.specialitem_queue)-1,[item_id,item_info +1])
                        self.specialitem_queue.pop(0)
                else:
                    #Is priority
                    #Give the trap 5 seconds to trigger, else discard
                    if (time.time()) >= item_info + 5:
                        self.priority_trap_queue.pop(0)
                return None
                # Exit without sending trap, keeping it active for the next pass
            #print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            #print(item_info)
            #print(IsPriority)
            # Banana Peel Trap handling
            if item_id == RAM.items['BananaPeelTrap']:
                if IsPriority:
                    self.priority_trap_queue.pop(0)
                else:
                    self.specialitem_queue.pop(0)
                SpecialItems_Writes += [(RAM.spikeState2Address, 0x2F.to_bytes(1, "little"), "MainRAM")]

            # Gadget Shuffle Trap handling
            elif item_id == RAM.items['GadgetShuffleTrap']:
                if IsPriority:
                    self.priority_trap_queue.pop(0)
                else:
                    self.specialitem_queue.pop(0)
                # print(self.specialitem_queue)
                chosen_gadgets = []
                chosen_values = [0, 0, 0, 0]
                faces = [0, 1, 2, 3]
                facesNames = ["P1 X","P1 Square","P1 Circle","P1 Triangle"]
                faceValues = [0xBF,0x7F,0xDF,0xEF]
                Trap_writes = []
                Trap_writes2 = []
                Trap_guards = []

                # Exit if no gadgets has been unlocked yet
                if currentGadgets == []:
                    return None

                # 1 pass for each face
                for x in range(4):
                    randomFace = int(round(random.random() * (len(faces) - 1), None))
                    face = faces[randomFace]
                    # If there is no more gadgets, it means we put an "Empty" spot
                    if currentGadgets == []:
                        # print("Face #" + str(randomFace + 1) + ": None | 255")
                        chosen_values[face] = 0xFF
                        faces.pop(randomFace)
                    else:
                        randomGadget = int(round(random.random() * (len(currentGadgets) - 1), None))
                        gadget_value = gadgetsValues[currentGadgets[randomGadget]]
                        chosen_values[face] = gadget_value
                        # print("Face #" + str(faces[randomFace]) + ": " + str(currentGadgets[randomGadget]) + " | " + str(gadgetsValues[currentGadgets[randomGadget]]))
                        chosen_gadgets.append(str(currentGadgets[randomGadget]))
                        currentGadgets.pop(randomGadget)
                        faces.pop(randomFace)
                # print(chosen_gadgets)

                Trap_writes += [(RAM.crossGadgetAddress, chosen_values[0].to_bytes(1, "little"), "MainRAM")]
                Trap_writes += [(RAM.squareGadgetAddress, chosen_values[1].to_bytes(1, "little"), "MainRAM")]
                Trap_writes += [(RAM.circleGadgetAddress, chosen_values[2].to_bytes(1, "little"), "MainRAM")]
                Trap_writes += [(RAM.triangleGadgetAddress, chosen_values[3].to_bytes(1, "little"), "MainRAM")]

                await bizhawk.write(ctx.bizhawk_ctx, Trap_writes)

                # Select a gadget slot
                randomSelect = int(round(random.random() * (len(chosen_values) - 1), None))

                Trap_writes2 += [(RAM.Controls_TriggersShapes, faceValues[randomSelect].to_bytes(1, "little"), "MainRAM")]

                Trap_guards += [(RAM.crossGadgetAddress, chosen_values[0].to_bytes(1, "little"), "MainRAM")]
                Trap_guards += [(RAM.squareGadgetAddress, chosen_values[1].to_bytes(1, "little"), "MainRAM")]
                Trap_guards += [(RAM.circleGadgetAddress, chosen_values[2].to_bytes(1, "little"), "MainRAM")]
                Trap_guards += [(RAM.triangleGadgetAddress, chosen_values[3].to_bytes(1, "little"), "MainRAM")]

                #Analog_values = {}
                #await self.ape_handler.input_controller.set_inputs(Analog_values)

                #if spikeState2 in (128, 129, 131, 132):
                #Trap_writes += [(RAM.spikeState2Address, 0x00.to_bytes(1, "little"), "MainRAM")]
                #Trap_writes += [(RAM.heldGadgetAddress, chosen_values[randomSelect].to_bytes(1, "little"), "MainRAM")]
                #Trap_writes += [(RAM.Controls_TriggersShapes, faceValues[randomSelect].to_bytes(1, "little"), "MainRAM")]
                if heldGadget != chosen_values[randomSelect]:
                    timeout_count = 0
                    while timeout_count < 10:
                        timeout_count += 1
                        #print(timeout_count)
                        await bizhawk.guarded_write(ctx.bizhawk_ctx, Trap_writes2, Trap_guards)

            # Monkey Mash Trap handling
            elif item_id == RAM.items['MonkeyMashTrap']:
                if IsPriority:
                    self.priority_trap_queue.pop(0)
                else:
                    self.specialitem_queue.pop(0)
                mash_duration = 10  # Example: 10 seconds per powerup item
                if self.ape_handler.is_active:
                    message = f"Monkey Mash trap extended by {mash_duration} seconds! (Current: {round(self.ape_handler.duration, 0)} seconds)"
                else:
                    message = f"Monkey Mash trap activated for {mash_duration} seconds!"
                await self.send_bizhawk_message(ctx, message, "Passthrough", "")
                self.ape_handler.activate_monkey(mash_duration)
                #print(message)

            # Icy Hot Trap handling
            elif item_id == RAM.items['IcyHotPantsTrap']:
                # Does not fire the trap if not grounded in some way
                if is_grounded:
                    if IsPriority:
                        self.priority_trap_queue.pop(0)
                    else:
                        self.specialitem_queue.pop(0)
                    SpecialItems_Writes += [(RAM.spikeState2Address, 0x4D.to_bytes(1, "little"), "MainRAM")]
                    SpecialItems_Writes += [(RAM.spike_LavaOrIceTimer, 0x0100.to_bytes(2, "little"), "MainRAM")]
                    # If the chosen spikecolor is "Vanilla", choose an effect at random between Burn/Frost
                    if DS_spikeColor == "vanilla":
                        randomEffect = int(round(random.random() * (2-1), None))
                        if randomEffect == 0:
                            # Burn Effect
                            SpecialItems_Writes += [(RAM.spikeColor, 0x000000.to_bytes(3, "big"), "MainRAM")]
                        else:
                            # Frost Effect:
                            SpecialItems_Writes += [(RAM.spikeColor, 0x0000FF.to_bytes(3, "big"), "MainRAM")]
                else:
                    if IsPriority:
                        if item_info >= (time.time() + 5):
                            #print("TrapLinked Trap expired")
                            self.priority_trap_queue.pop(0)
            # Rainbow Cookie handling
            elif item_id == RAM.items['RainbowCookie']:
                self.specialitem_queue.pop(0)
                item_duration = 20  # Example: 20 seconds per powerup item
                if self.rainbow_cookie.is_active:
                    message = f"Rainbow Cookie extended by {item_duration} seconds! (Current: {round(self.rainbow_cookie.duration, 0)} seconds)"
                else:
                    message = f"Rainbow Cookie activated for {item_duration} seconds!"
                await self.send_bizhawk_message(ctx, message, "Passthrough", "")
                await self.rainbow_cookie.activate_rainbow_cookie(item_duration)

            #Stun Trap handling
            elif item_id == RAM.items['StunTrap']:
                if IsPriority:
                    self.priority_trap_queue.pop(0)
                else:
                    self.specialitem_queue.pop(0)
                item_duration = 2  # Example: 2 seconds per powerup item
                #if self.stun_trap.is_active:
                #    message = f"Stun Trap extended by {item_duration} seconds! (Current: {round(self.stun_trap.duration, 0)} seconds)"
                #else:
                #    message = f"Stun Trap activated for {item_duration} seconds!"
                message = f"Stun Trap activated for {item_duration} seconds!"
                await self.send_bizhawk_message(ctx, message, "Passthrough", "")
                await self.stun_trap.activate_StunTrap(item_duration,spikeState2,currentRoom)
            #Camera Rotate Trap handling
            elif item_id == RAM.items['CameraRotateTrap']:
                if IsPriority:
                    self.priority_trap_queue.pop(0)
                else:
                    self.specialitem_queue.pop(0)
                item_duration = 20  # Example: 2 seconds per powerup item
                #if self.stun_trap.is_active:
                #    message = f"Stun Trap extended by {item_duration} seconds! (Current: {round(self.stun_trap.duration, 0)} seconds)"
                #else:
                #    message = f"Stun Trap activated for {item_duration} seconds!"
                message = f"Camera Rotate Trap activated for {item_duration} seconds!"
                await self.send_bizhawk_message(ctx, message, "Passthrough", "")
                await self.camera_rotate_trap.activate_camera_rotate(item_duration, currentRoom)

            if SpecialItems_Writes:
                await bizhawk.write(ctx.bizhawk_ctx, SpecialItems_Writes)

    async def ER_Handling(self, ctx: "BizHawkClientContext", ER_Reads) -> None:
        gameState = ER_Reads[0]
        status_currentWorld = ER_Reads[1]
        status_currentLevel = ER_Reads[2]
        currentLevel = ER_Reads[3]
        transitionPhase = ER_Reads[4]
        Spike_X_Pos = ER_Reads[5]
        Spike_Y_Pos = ER_Reads[6]
        Spike_Z_Pos = ER_Reads[7]
        spikeState2 = ER_Reads[8]
        currentRoom = ER_Reads[9]
        gameRunning = ER_Reads[10]
        InputListener = ER_Reads[11]
        Warp_State = ER_Reads[12]
        Transition_Screen_Progress = ER_Reads[13]
        LoadingState = ER_Reads[14]
        Spike_CanMove = ER_Reads[15]

        ER_writes = []
        ER_guards = []

        # List of vanilla rooms per level
        baselevelidtofirstroom = dict(zip(RAM.baselevelids, RAM.firstroomids))
        firstroomids = ctx.slot_data["firstrooms"]
        # List of current rooms per level
        firstrooms = firstroomids.copy()
        firstrooms.sort()
        currentlevelidtofirstroom = dict(zip(RAM.baselevelids, firstrooms))

        if gameState == RAM.gameState["LevelSelect"]:
            # writes += [(RAM.preventRoomOverride, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            ER_writes += [(RAM.localApeStartAddress, 0x0.to_bytes(8, "little"), "MainRAM")]
            # Update level (and potentially era) names.
            bytestowrite = ctx.slot_data["levelnames"]
            # This is a bit of a "magic number" right now. Trying to get the length didn't work.
            # Trying to write all the bytes at once also didn't work.
            for x in range(0, 308):
                ER_writes += [(RAM.startOfLevelNames + x, bytestowrite[x].to_bytes(1, "little"), "MainRAM")]
        # Reroute the player to the correct level. Technically only needed for entrance shuffle, vanilla entrances are just a special case of entrance shuffle so this works perfectly fine for that case, too.
        if gameState == RAM.gameState["LevelIntro"] or gameState == RAM.gameState["LevelIntroTT"]:
            # Pull the order of first rooms from slot data. This is a List sorted by the order of entrances in the level select - so the first value is the room being entered from Fossil Field.
            firstroomids = ctx.slot_data["firstrooms"]
            entranceorder = ctx.slot_data["entranceids"]
            # Match these room ids to the internal identifiers - 11, 12, 13, 21, ... 83, 91, 92
            # levelidtofirstroom = dict(zip(RAM.levelAddresses.keys(), RAM.firstroomids))
            levelidtofirstroom = dict(zip(RAM.levelAddresses.keys(), firstroomids))
            selectedWorld = status_currentWorld
            selectedLevel = status_currentLevel
            # Use Selected World (0-9) and Selected Level (0-2) to determine the selected level.
            chosenLevel = 10 * selectedWorld + selectedLevel + 11
            # Peak Point Matrix doesn't follow the pattern, so manually override if it's that.
            # print(chosenLevel)
            if chosenLevel > 100:
                chosenLevel = 92

            targetRoom = levelidtofirstroom.get(chosenLevel)

            targetLevel = entranceorder[firstroomids.index(targetRoom)]
            levelrooms = list(RAM.roomsperlevel[targetLevel])
            levelrooms.sort()

            ER_writes += [(RAM.currentRoomIdAddress, targetRoom.to_bytes(1, "little"), "MainRAM")]
            ER_writes += [(RAM.currentLevelAddress, targetLevel.to_bytes(1, "little"), "MainRAM")]
            if baselevelidtofirstroom.get(targetLevel) == currentlevelidtofirstroom[targetLevel]:
                VanillaRoom = True
            else:
                VanillaRoom = False

            if VanillaRoom == False:
                if InputListener == 0x02 and self.ChangeRoom == False:
                    #print("Disable Event_Load_Block")
                    ER_writes += [(RAM.Event_Load_Block, RAM.Event_Load_Block_Off.to_bytes(4, "little"), "MainRAM")]
                    self.ChangeRoom = True
        # Code to send Spike to the right transition (If needed)
        if gameState in (RAM.gameState["InLevel"], RAM.gameState["InLevelTT"]):

            # For all of the Monkey Madness levels, treat it as Monkey Madness
            if 0x18 < currentLevel < 0x1E:
                level = 0x18
            else:
                level = currentLevel
            # Check if the spawn room for the current level is vanilla

            if baselevelidtofirstroom.get(level) == currentlevelidtofirstroom[level]:
                VanillaRoom = True
            else:
                VanillaRoom = False

            if self.ChangeRoom == True and gameRunning == 0x01:
                #print(InputListener)
                self.ChangeRoom = False
                #print("Replace the Event_Load_Block back to default")
                ER_writes += [(RAM.Event_Load_Block, RAM.Event_Load_Block_On.to_bytes(4, "little"), "MainRAM")]

            LevelStartRoom = currentlevelidtofirstroom[level]

            TR_writes = []
            TR_guards = []
            # If the level's first room is not vanilla,validate some conditions
            if VanillaRoom == False:
                # Special code handling for TVT Water Room Spawn
                if currentLevel == 22 and LevelStartRoom == 64:
                    # Drain the water if you are starting in the TVT - Water Room as part of Randomize First Rooms
                    if self.TVT_Lobby_Button != 1:
                        await ctx.send_msgs([{
                            "cmd": "Get",
                            "keys": [f"AE_TVT_Lobby_Button_{ctx.team}_{ctx.slot}"]
                        }])
                    if self.TVT_Lobby_Button != 1:
                        await ctx.send_msgs([{
                            "cmd": "Set",
                            # "key": str(ctx.player_names[ctx.slot]) + "_TVT_Lobby_Button",
                            "key": f"AE_TVT_Lobby_Button_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": 1}]
                        }])
        await bizhawk.write(ctx.bizhawk_ctx, ER_writes)

    def format_cointable(self,ctx: "BizHawkClientContext",CoinTable,SA_Completed,GA_Completed,usage = ""):
        SA = 0
        GA = 0
        PPM = 0
        #print(format(CoinTable,'X'))
        #print(SA_Completed)
        #print(GA_Completed)
        if (CoinTable == RAM.blank_coinTable or CoinTable == RAM.blank_coinTable2) and (SA_Completed == 0x00) and (GA_Completed == 0x00):
            return ""

        entranceorder = ctx.slot_data["entranceids"]
        baselevelids = RAM.baselevelids
        hex_string = format(CoinTable,'X')
        # Split into byte pairs and reverse the list
        if len(hex_string) % 2 != 0:
            hex_string = f"0{hex_string}"
        byte_pairs = [hex_string[i:i + 2] for i in range(0, len(hex_string), 2)]
        bytes_coins_list = [hex_string[i:i + 2] for i in range(0, len(hex_string), 4)]
        coins_reversed_byte_pairs = bytes_coins_list[::-1]
        reversed_byte_pairs = byte_pairs[::-1]
        coins_reversed_byte_pairs = reversed_byte_pairs[::2]
        value_to_remove = 'FF'
        coins_list = [int(item,16) for item in coins_reversed_byte_pairs if item != value_to_remove]
        if usage == "Locations":
            # Only need to extract coins from this list
            return coins_list

        trueCoinsList = []
        #print(coins_list)
        for i in range(len(entranceorder)):
            entranceID = entranceorder[i]
            #print(entranceorder.index(entranceID))
            baseLevelID = baselevelids[entranceorder.index(entranceID)]
            if SA_Completed == 0x19 and entranceID == 7:
                coins_list += [item for item in RAM.coinsperlevel.get(entranceID)]
            if GA_Completed == 0x19 and entranceID == 14:
                coins_list += [item for item in RAM.coinsperlevel.get(entranceID)]
            #print(f"BaseLevelID:{baseLevelID}")

            if RAM.coinsperlevel.get(entranceID) != {}:
                #print(set(RAM.coinsperlevel.get(entranceID)))
                if set(RAM.coinsperlevel.get(entranceID)).issubset(set(coins_list)):
                    # Add all of "EntranceID" coins to the list
                    if baseLevelID == 7:
                        SA = 1
                    elif baseLevelID == 14:
                        GA = 1
                    elif baseLevelID == 30:
                        PPM = 1
                    else:
                        trueCoinsList += (item for item in RAM.coinsperlevel.get(baseLevelID))
                    #print(f"All coins in level {entranceID} are in the coins list.")
                    #print(trueCoinsList)
                    #print(baseLevelID)
                #else:
                #print(f"Not all elements in level {entranceID} are in the coins list.")
        #print(coins_list)
        # Join the reversed byte pairs back into a string
        #inverted_hex_string = "".join(reversed_byte_pairs)
        inverted_hex_string = "".join([f"01{int(item):02x}" for item in trueCoinsList])

        #print(f"Original: {hex_string}")
        #print(f"Inverted (byte order): {inverted_hex_string}")

        return [inverted_hex_string,SA,GA,PPM]
    async def level_select_optimization(self, ctx: "BizHawkClientContext", LSO_Reads) -> None:
        # For coin display to be ignored while in Level Select
        gameState = LSO_Reads[0]
        CoinTable = LSO_Reads[1]
        TempCoinTable = LSO_Reads[2]
        SA_Completed = LSO_Reads[3]
        Temp_SA_Completed = LSO_Reads[4]
        GA_Completed = LSO_Reads[5]
        Temp_GA_Completed = LSO_Reads[6]
        LS_currentLevel = LSO_Reads[7]
        LS_currentWorld = LSO_Reads[8]
        worldIsScrollingRight = LSO_Reads[9]
        levelselect_coinlock_Address = LSO_Reads[10]

        LS_Writes = []
        if RAM.gameState["LevelSelect"] == gameState:
            if levelselect_coinlock_Address == 0xFF:
                LS_Writes += [(RAM.levelselect_coinlock_Address, 0x01.to_bytes(1, "little"), "MainRAM")]
                currentCoinTable = CoinTable
                current_SA_Completed = SA_Completed
                current_GA_Completed = GA_Completed
            else:
                currentCoinTable = TempCoinTable
                current_SA_Completed = Temp_SA_Completed
                current_GA_Completed = Temp_GA_Completed
            #if CoinTable != RAM.blank_coinTable and ((TempCoinTable == RAM.blank_coinTable)) or ((TempCoinTable == RAM.blank_coinTable2)):
            #if ((TempCoinTable == RAM.blank_coinTable)) or ((TempCoinTable == RAM.blank_coinTable2)):
            #DisplayCoinsTable = int(self.format_cointable(ctx, CoinTable),16)
            Formated_Coins = self.format_cointable(ctx, currentCoinTable,current_SA_Completed,current_GA_Completed)
            if Formated_Coins != "":
                DisplayCoinsTable = Formated_Coins[0]
                SA = Formated_Coins[1]
                GA = Formated_Coins[2]
                PPM = Formated_Coins[3]
            else:
                DisplayCoinsTable = ""
                SA = 0
                GA = 0
                PPM = 0
            #print(f"DisplayCoinsTable:{DisplayCoinsTable}"
            #f"\nSA:{SA}"
            #f"\nGA:{GA}"
            #f"\nPPM:{PPM}")
            if DisplayCoinsTable == {} or DisplayCoinsTable == "":
                DisplayCoinsTable = RAM.blank_coinTable
            else:
                DisplayCoinsTable = int(DisplayCoinsTable,16)
                #print(DisplayCoinsTable)
            #print(DisplayCoinsTable)
            #LS_Writes += [(RAM.startingCoinAddress, RAM.blank_coinTable.to_bytes(100, "little"), "MainRAM")]
            if DisplayCoinsTable != CoinTable:
                #print("Wrote DisplayTable")
                LS_Writes += [(RAM.startingCoinAddress, DisplayCoinsTable.to_bytes(100, "little"), "MainRAM")]
            if currentCoinTable != TempCoinTable:
                #print("Wrote To TempCoinTable")
                LS_Writes += [(RAM.temp_startingCoinAddress, currentCoinTable.to_bytes(100, "little"), "MainRAM")]
            if current_SA_Completed != Temp_SA_Completed:
                #print("Wrote To TempSA")
                LS_Writes += [(RAM.temp_SA_CompletedAddress, current_SA_Completed.to_bytes(1, "little"), "MainRAM")]
            if current_GA_Completed != Temp_GA_Completed:
                #print("Wrote To TempGA")
                LS_Writes += [(RAM.temp_GA_CompletedAddress, current_SA_Completed.to_bytes(1, "little"), "MainRAM")]

            if SA == 1:
                LS_Writes += [(RAM.SA_CompletedAddress, 0x19.to_bytes(1, "little"), "MainRAM")]
            else:
                LS_Writes += [(RAM.SA_CompletedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]

            if GA == 1:
                LS_Writes += [(RAM.GA_CompletedAddress, 0x19.to_bytes(1, "little"), "MainRAM")]
            else:
                LS_Writes += [(RAM.GA_CompletedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]


            if PPM == 1:
                LS_Writes += [(RAM.PPMShowCoins, 0x02.to_bytes(1, "little"), "MainRAM")]
            else:
                LS_Writes += [(RAM.PPMShowCoins, 0x00.to_bytes(1, "little"), "MainRAM")]



        elif RAM.gameState["Cleared"] != gameState:
            if levelselect_coinlock_Address == 0x01:
                LS_Writes += [(RAM.levelselect_coinlock_Address, 0xFF.to_bytes(1, "little"), "MainRAM")]
                LS_Writes += [(RAM.startingCoinAddress, TempCoinTable.to_bytes(100, "little"), "MainRAM")]
                LS_Writes += [(RAM.temp_startingCoinAddress, RAM.blank_coinTable.to_bytes(100, "little"), "MainRAM")]
                if Temp_SA_Completed != 0xFF:
                    LS_Writes += [(RAM.SA_CompletedAddress, Temp_SA_Completed.to_bytes(1, "little"), "MainRAM")]
                    LS_Writes += [(RAM.temp_SA_CompletedAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                if Temp_GA_Completed != 0x00:
                    LS_Writes += [(RAM.GA_CompletedAddress, Temp_GA_Completed.to_bytes(1, "little"), "MainRAM")]
                    LS_Writes += [(RAM.temp_GA_CompletedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]

        # Prevent scrolling past the unlocked ERA/level
        if gameState == RAM.gameState["LevelSelect"]:
            reqkeys = ctx.slot_data["reqkeys"]

            # Get all keys required for the next world, based on first level of ERAS
            WorldUnlocks = [reqkeys[3], reqkeys[6], reqkeys[7], reqkeys[10], reqkeys[13], reqkeys[14], reqkeys[17], reqkeys[20], reqkeys[21]]
            # Format current selected level to compare against reqkeys table
            currentLevel = (3 * LS_currentWorld) + LS_currentLevel
            if LS_currentWorld >= 3:
                currentLevel -= 2
            if LS_currentWorld >= 6:
                currentLevel -= 2

            # Check if the selected world is the last (To stay within bound of the list)
            if 0 <= LS_currentWorld < 9:
                # Modified old fix to detect current level requirement and scroll back to the last unlocked world/level
                if self.worldkeycount < reqkeys[currentLevel]:
                    # Kinda strange condition but just to be sure ;)
                    if LS_currentLevel == 0 and LS_currentWorld != 0:
                        LS_Writes += [(RAM.selectedWorldAddress, (LS_currentWorld - 1).to_bytes(1, "little"), "MainRAM")]
                    else:
                        LS_Writes += [(RAM.selectedLevelAddress, (LS_currentLevel - 1).to_bytes(1, "little"), "MainRAM")]

                # If you have less World Keys that the required keys for the next ERA, disable R1, Right Stick and Right DPAD detection

                if (LS_currentWorld < 8) and (worldIsScrollingRight == 0xFFFF):
                    if (self.worldkeycount < WorldUnlocks[LS_currentWorld + 1]):
                        LS_Writes += [(RAM.worldScrollToRightDPAD, 0x0000.to_bytes(2, "little"), "MainRAM")]
                        LS_Writes += [(RAM.worldScrollToRightR1, 0x0000.to_bytes(2, "little"), "MainRAM")]
                elif (self.worldkeycount < WorldUnlocks[LS_currentWorld]):
                    LS_Writes += [(RAM.worldScrollToRightDPAD, 0x0000.to_bytes(2, "little"), "MainRAM")]
                    LS_Writes += [(RAM.worldScrollToRightR1, 0x0000.to_bytes(2, "little"), "MainRAM")]
                else:
                    LS_Writes += [(RAM.worldScrollToRightDPAD, 0x0009.to_bytes(2, "little"), "MainRAM")]
                    LS_Writes += [(RAM.worldScrollToRightR1, 0x0009.to_bytes(2, "little"), "MainRAM")]

        await bizhawk.write(ctx.bizhawk_ctx, LS_Writes)


    async def water_net_handling(self, ctx: "BizHawkClientContext", WN_Reads) -> None:
        # Water Net client handling
        # If Progressive WaterNet is 0 no Swim and no Dive, if it's 1 No Dive (Swim only)
        # 8-9 Jumping/falling, 35-36 D-Jump, 83-84 Flyer => don't reset the counter

        inAir = [0x08, 0x09, 0x35, 0x36, 0x83, 0x84]
        swimming = [0x46, 0x47]
        grounded = [0x00, 0x01, 0x02, 0x05, 0x07]  # 0x80, 0x81 Removed them since you can fling you net and give you extra air

        limited_OxygenLevel = 0x64

        gameState = WN_Reads[0]
        waternetState = WN_Reads[1]
        gameRunning = WN_Reads[2]
        spikeState2 = WN_Reads[3]
        swim_oxygenLevel = WN_Reads[4]
        cookies = WN_Reads[5]
        isUnderwater = WN_Reads[6]
        watercatchState = WN_Reads[7]

        WN_writes = []

        is_grounded = spikeState2 in grounded
        # Base variables
        if waternetState == 0x00:
            WN_writes += [(RAM.swim_surfaceDetectionAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.canDiveAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_oxygenReplenishSoundAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_ReplenishOxygenUWAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_replenishOxygenOnEntryAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
        elif waternetState == 0x01:
            WN_writes += [(RAM.swim_surfaceDetectionAddress, 0x0801853A.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.canDiveAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_oxygenReplenishSoundAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_ReplenishOxygenUWAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_replenishOxygenOnEntryAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
        else:
            # (waternetstate > 0x01)
            WN_writes += [(RAM.swim_surfaceDetectionAddress, 0x0801853A.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.canDiveAddress, 0x08018664.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_oxygenReplenishSoundAddress, 0x0C021DFE.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_ReplenishOxygenUWAddress, 0xA4500018.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_replenishOxygenOnEntryAddress, 0xA4434DC8.to_bytes(4, "little"), "MainRAM")]

        # Oxygen Handling
        if waternetState == 0x00:
            if gameState == RAM.gameState["InLevel"] or gameState == RAM.gameState["InLevelTT"]:
                if gameRunning == 0x01:
                    # Set the air to the "Limited" value if 2 conditions:
                    # Oxygen is higher that "Limited" value AND spike is Swimming or Grounded
                    if spikeState2 in swimming:
                        if (swim_oxygenLevel > limited_OxygenLevel):
                            WN_writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
                    else:
                        # if self.waterHeight != 0:
                        # self.waterHeight = 0
                        if is_grounded:
                            WN_writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]

                #else:
                # Game Not running
                #if swim_oxygenLevel == 0 and cookies == 0 and gameRunning == 0:
                if swim_oxygenLevel == 0 and cookies == 0:
                    # You died while swimming, reset Oxygen to "Limited" value prevent death loops
                    WN_writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
                    WN_writes += [(RAM.isUnderwater, 0x00.to_bytes(1, "little"), "MainRAM")]

        if waternetState == 0x01:

            if isUnderwater == 0x00 and swim_oxygenLevel != limited_OxygenLevel:
                WN_writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
            if swim_oxygenLevel == 0 and cookies == 0 and gameRunning == 0:
                # You died while swimming, reset Oxygen to "Limited" value prevent death loops
                WN_writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
                WN_writes += [(RAM.isUnderwater, 0x00.to_bytes(1, "little"), "MainRAM")]

        # WaterCatch unlocking stuff bellow
        if watercatchState == 0x00:
            WN_writes += [(RAM.canWaterCatchAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
        else:
            WN_writes += [(RAM.canWaterCatchAddress, 0x04.to_bytes(1, "little"), "MainRAM")]

        # Low Oxygen Sounds
        if spikeState2 in swimming:

            # Off
            if ctx.slot_data["lowoxygensounds"] == 0x00:
                WN_writes += [(RAM.swim_oxygenLowLevelSoundAddress, 0x3C028004.to_bytes(4, "little"), "MainRAM")]
                WN_writes += [(RAM.swim_oxygenMidLevelSoundAddress, 0x3C028004.to_bytes(4, "little"), "MainRAM")]
            # Half Beeps
            elif ctx.slot_data["lowoxygensounds"] == 0x01:

                self.lowOxygenCounter += 1
                # Should start at 1
                # print(self.lowOxygenCounter)
                if self.lowOxygenCounter <= 2:
                    WN_writes += [(RAM.swim_oxygenLowLevelSoundAddress, 0x3C02800F.to_bytes(4, "little"), "MainRAM")]
                    WN_writes += [(RAM.swim_oxygenMidLevelSoundAddress, 0x3C02800F.to_bytes(4, "little"), "MainRAM")]
                elif self.lowOxygenCounter <= 3:
                    WN_writes += [(RAM.swim_oxygenLowLevelSoundAddress, 0x3C028004.to_bytes(4, "little"), "MainRAM")]
                    WN_writes += [(RAM.swim_oxygenMidLevelSoundAddress, 0x3C028004.to_bytes(4, "little"), "MainRAM")]
                elif self.lowOxygenCounter > 3:
                    self.lowOxygenCounter = 0

            # On (Vanilla)
            else:
                # print("Vanilla")
                WN_writes += [(RAM.swim_oxygenLowLevelSoundAddress, 0x3C02800F.to_bytes(4, "little"), "MainRAM")]
                WN_writes += [(RAM.swim_oxygenMidLevelSoundAddress, 0x3C02800F.to_bytes(4, "little"), "MainRAM")]
        else:
            if self.lowOxygenCounter != 1:
                self.lowOxygenCounter = 1

        await bizhawk.write(ctx.bizhawk_ctx,WN_writes)


    async def update_tags (self, ctx: "BizHawkClientContext") -> None:
        updateTags = False
        if ctx.slot_data["death_link"] == DeathLink.option_true or self.deathlink == 1:
            if "DeathLink" not in ctx.tags:
                ctx.tags.add("DeathLink")
                updateTags = True
        else:
            if "DeathLink" in ctx.tags:
                ctx.tags.remove("DeathLink")
                updateTags = True
        if ctx.slot_data["trap_link"] == TrapLink.option_true:
            if "TrapLink" not in ctx.tags:
                ctx.tags.add("TrapLink")
                updateTags = True
        else:
            if "TrapLink" in ctx.tags:
                ctx.tags.remove("TrapLink")
                updateTags = True
        if updateTags:
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

    async def handle_trap_link(self, ctx: "BizHawkClientContext") -> None:
        if ctx.slot_data["trap_link"] == TrapLink.option_true:
            if "TrapLink" not in ctx.tags:
                ctx.tags.add("TrapLink")
                await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])
        else:
            if "TrapLink" in ctx.tags:
                ctx.tags.remove("TrapLink")
                await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

    async def handle_death_link(self, ctx: "BizHawkClientContext", DL_Reads) -> None:
        """
        Checks whether the player has died while connected and sends a death link if so.
        """
        cookies = DL_Reads[0]
        gameRunning = DL_Reads[1]
        gameState = DL_Reads[2]
        menuState2 = DL_Reads[3]
        spikestate2 = DL_Reads[4]

        OnTree = {56, 57, 58, 59, 60}

        DL_writes = []
        DL_writes2 = []
        if self.deathlink == 1:
            if "DeathLink" not in ctx.tags:
                #await ctx.update_death_link(True)
                self.previous_death_link = ctx.last_death_link
            if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
                if cookies == 0x00 and not self.sending_death_link and gameState in (RAM.gameState["InLevel"],RAM.gameState["TimeStation"]):
                    await self.send_deathlink(ctx)
                elif cookies != 0x00:
                    self.sending_death_link = False
            # Wait on exiting menu before sending deathlink
            if self.pending_death_link and menuState2 != 1:
                DL_writes += [(RAM.cookieAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                DL_writes += [(RAM.instakillAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                if spikestate2 in OnTree:
                    DL_writes2 += [(RAM.Controls_TriggersShapes, 0xFD.to_bytes(1, "little"), "MainRAM")]
                self.pending_death_link = False
                self.sending_death_link = True
                await bizhawk.write(ctx.bizhawk_ctx, DL_writes)
                await bizhawk.write(ctx.bizhawk_ctx, DL_writes2)
        elif self.deathlink == 0:
            #await ctx.update_death_link(False)
            self.previous_death_link = ctx.last_death_link

    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        DeathMessageList = ["`Ohhh noooo!`", "`This bites.`"]
        randomNumber = (round(random.random() * (len(DeathMessageList) - 1),None))
        DeathMessage = DeathMessageList[randomNumber]
        DeathText = ctx.player_names[ctx.slot] + " says: " + DeathMessage + " (Died)"
        await ctx.send_death(DeathText)

    async def send_trap_link(self, ctx: "BizHawkClientContext", trap_name: str):

        if "TrapLink" not in ctx.tags or ctx.slot == None:
            return

        await ctx.send_msgs([{
            "cmd": "Bounce", "tags": ["TrapLink"],
            "data": {
                "time": time.time(),
                "source": ctx.player_names[ctx.slot],
                "trap_name": trap_name
            }
        }])
        #logger.info(f"Sent linked {trap_name}")

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True


    def unlockLevels(self, ctx: "BizHawkClientContext", monkeylevelCounts, gameState, hundoMonkeysCount, reqkeys, newpositions, SAcomplete, GAcomplete, PPMcomplete):

        key = self.worldkeycount
        token = self.tokencount
        curApesWrite = ""
        reqApesWrite = ""
        hundoWrite = ""
        levellocked = RAM.levelStatus["Locked"].to_bytes(1, byteorder = "little")
        levelopen = RAM.levelStatus["Open"].to_bytes(1, byteorder = "little")
        levelhundo = RAM.levelStatus["Hundo"].to_bytes(1, byteorder = "little")
        allCompleted = True

        debug = False

        levels_keys = hundoMonkeysCount.keys()
        levels_list = list(levels_keys)
        if gameState == RAM.gameState["LevelSelect"] or debug:
            for x in range(len(levels_list)):
                if monkeylevelCounts[x] < hundoMonkeysCount[levels_list[x]]:
                    # print("Level " + str(x) + " not completed" + str(int.from_bytes(monkeylevelCounts[x])) + "/" + str(hundoMonkeysCount[levels_list[x]]))
                    allCompleted = False
                    break
                    # Does not need to check the rest of the levels, at least 1 is not completed

        if ctx.slot_data["goal"] == GoalOption.option_ppmtoken:
            PPMUnlock = (key >= reqkeys[21] and token >= min(ctx.slot_data["requiredtokens"], ctx.slot_data["totaltokens"]))
        elif ctx.slot_data["goal"] == GoalOption.option_mmtoken or ctx.slot_data["goal"] == GoalOption.option_tokenhunt:
            PPMUnlock = (key >= reqkeys[21])
        else:
            PPMUnlock = (key >= reqkeys[21] and allCompleted)

        # Set unlocked/locked state of levels
        # This does not handle assignment of Specter Coin icons.
        # Most of this handling is about entrance order - the Hundo check would need to be pulled out of the big if chain because it's about level order right now.
        # Make sure that Hundo doesn't get set on a level that needs to be Locked and that Open doesn't get set on a level that needs to be Hundo.
        levelstates = []
        for index in range(0, 22):
            # Do we have enough keys for this level? If no, lock. If yes, continue.
            if key >= reqkeys[index]:
                # Are we checking the final entrance? If yes, open. If no, continue.
                if index != 21:
                    # Do we have enough keys for the next level? If no, lock. If yes, open.
                    if key >= reqkeys[index + 1]:
                        levelstates.append((RAM.levelAddresses[list(RAM.levelAddresses.keys())[index]], levelopen, "MainRAM"))
                    else:
                        levelstates.append((RAM.levelAddresses[list(RAM.levelAddresses.keys())[index]], levellocked, "MainRAM"))
                else:
                    levelstates.append((RAM.levelAddresses[list(RAM.levelAddresses.keys())[index]], levelopen, "MainRAM"))
            else:
                levelstates.append((RAM.levelAddresses[list(RAM.levelAddresses.keys())[index]], levellocked, "MainRAM"))

        # Set hundo status on entrances that are open and have all monkeys in them caught.
        # Starts by checking Fossil Field (the level)
        for index in range(0, 22):
            # Is this level a race level?
            if index == 6:
                # Is Stadium Attack completed?
                if SAcomplete == 25:
                    levelstates[newpositions[index]] = (RAM.levelAddresses[list(RAM.levelAddresses.keys())[newpositions[index]]], levelhundo, "MainRAM")
            elif index == 13:
                # Is Gladiator Attack completed?
                if GAcomplete == 25:
                    levelstates[newpositions[index]] = (RAM.levelAddresses[list(RAM.levelAddresses.keys())[newpositions[index]]], levelhundo, "MainRAM")
            elif index == 21:
                # Is Peak Point Matrix completed?
                if PPMcomplete == 1:
                    levelstates[newpositions[index]] = (RAM.levelAddresses[list(RAM.levelAddresses.keys())[newpositions[index]]], levelhundo, "MainRAM")
            else:
                # Standard level
                # Check if the entrance of the indexed level is open.
                # If yes, continue. If no, do nothing, the state is correct.
                # (Index 0) If Fossil Field is at Dark Ruins, this checks the Dark Ruins entrance (index 4).
                if levelstates[newpositions[index]] == (RAM.levelAddresses[list(RAM.levelAddresses.keys())[newpositions[index]]], levelopen, "MainRAM"):
                    # Check if all monkeys of the indexed level are caught.
                    # If yes, set the state to hundo. If no, do nothing, the state is correct.
                    # (Index 0) If Fossil Field is at Dark Ruins, set the Dark Ruins entrance (index 4) to hundo.
                    if monkeylevelCounts[index] >= hundoMonkeysCount[levels_list[index]]:
                        levelstates[newpositions[index]] = (RAM.levelAddresses[list(RAM.levelAddresses.keys())[newpositions[index]]], levelhundo, "MainRAM")

        # Monkey Madness entrance must be set to locked if Peak Point Matrix should be locked
        if PPMUnlock == False:
            levelstates[20] = ((RAM.levelAddresses[list(RAM.levelAddresses.keys())[20]], levellocked, "MainRAM"))

        # If there is a change in required monkeys count, include it in the writes
        returns = list(levelstates)
        if curApesWrite != "":
            returns.append(curApesWrite)
        if reqApesWrite != "":
            returns.append(reqApesWrite)
        if hundoWrite != "":
            returns.append(hundoWrite)
        return returns


# Mailbox text helper functions
def text_to_bytes(name):
    bytelist = []
    for x in name:
        bytelist.append(character_lookup(x))
    return bytelist


def character_lookup(byte):
    if byte.isspace():  # Space
        return 255
    if byte.isalpha():
        return ord(byte) - 49  # Both uppercase and lowercase letters
    if byte.isdecimal():
        if int(byte) < 6:
            return ord(byte) + 58  # 0-5
        else:
            return ord(byte) + 68  # 6-9
    if ord(byte) == 39:  # Single apostrophe
        return 187
    if ord(byte) == 46:  # Period
        return 172
    if ord(byte) == 47:  # Slash
        return 141
    if ord(byte) == 58:  # Colon
        return 174
