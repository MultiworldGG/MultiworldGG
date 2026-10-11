import logging
import math
import pkgutil

import orjson

import Utils
import time

from BaseClasses import ItemClassification
from NetUtils import ClientStatus, NetworkItem

from typing import TYPE_CHECKING, Dict, Any

import worlds._bizhawk as bizhawk

from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

from .Addresses import RAM, NTSCU10RAM, NTSCU11RAM
# from .Enums import GameStatus, LevelInGameIDs, SpyroColor, SpyroStates
from .LevelData import GetLevelData

# from .Options import GoalOptions, TrickDifficultyOptions, MoneybagsOptions, GemsanityOptions, LevelLockOptions, AbilityOptions, BomboOptions, PortalTextColorOptions, WTWarpOptions, SparxUpgradeOptions

logger = logging.getLogger("Client")

Commands_Dict = {
    "s3_help" : "cmd_s3_help",
    "goal" : "cmd_goal",
    "options": "cmd_options",
    "unlockedlevels": "cmd_unlockedlevels",
    "debuginfo" : "cmd_debugInfo",
}

def cmd_s3_help(self: "BizHawkClientCommandProcessor") -> None:
    """Show what commands are available for Spyro 2 Archipelago"""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Spyro 3":
        logger.warning("This command can only be used when playing Spyro: Year of the Dragon.")
        return
    logger.info(f"----------------------------------------------\n"
                f"Commands for Spyro 3\n"
                f"----------------------------------------------\n"
                f"  /s3_help\n"
                f"      Description: Show this list\n"
                f"  /goal\n"
                f"      Description: Shows your current goal and progress towards it.\n"
                f"  /options\n"
                f"      Description: Shows important options for your slot.\n"
                f"  /unlockedLevels\n"
                f"      Description: When level locks are keys, shows the levels you have unlocked.\n"
                f"  /debugInfo\n"
                f"      Description: Prints information about your game to the screen.\n"
                f"      You may be asked to screenshot this if there is an error.\n"
                f"  \n")

def cmd_goal(self: "BizHawkClientCommandProcessor") -> None:
    """Prints information about your game to the screen."""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Spyro 3":
        logger.warning("This command can only be used when playing Spyro: Year of the Dragon.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, Spyro2Client)

    goalText = ""
    progressText = ""
    requiredOrbs = ctx.slot_data["options"]["ripto_door_orbs"]
    orbsNeededText = f"{requiredOrbs} orb" if requiredOrbs == 1 else f"{requiredOrbs} orbs"
    orbsText = f"{client.currentOrbs} orb" if client.currentOrbs == 1 else f"{client.currentOrbs} orbs"
    gemsText = f"{client.currentGems} gem" if client.currentGems == 1 else f"{client.currentGems} gems"
    talismansText = f"{client.currentTalismans} talisman" if client.currentTalismans == 1 else f"{client.currentTalismans} talismans"
    tokensText = f"{client.currentTokens} token" if client.currentTokens == 1 else f"{client.currentTokens} tokens"
    skillPointsText = f"{client.currentSkillPoints} Skill Point" if client.currentSkillPoints == 1 else f"{client.currentSkillPoints} Skill Points"
    defeatedRiptoText = "have defeated Ripto" if client.riptoDefeated else "have not defeated Ripto"
    goal = ctx.slot_data["options"]["goal"]
    openWorldOption = ctx.slot_data["options"]["enable_open_world"]
    if goal == GoalOptions.RIPTO:
        goalText = f"Defeat Ripto and collect {orbsNeededText}, the requirement to open his arena"
        progressText = f"You have {orbsText} and {defeatedRiptoText}."
    elif goal == GoalOptions.SIXTY_FOUR_ORB:
        goalText = "Defeat Ripto and collect all 64 orbs"
        progressText = f"You have {orbsText} and {defeatedRiptoText}."
    elif goal == GoalOptions.HUNDRED_PERCENT:
        if openWorldOption == 0:
            goalText = "Defeat Ripto and collect all 14 talismans, 64 orbs, and 10000 gems"
            progressText = f"You have {talismansText}, {orbsText}, {gemsText},\nand {defeatedRiptoText}"
        else:
            goalText = "Defeat Ripto and collect all 64 orbs and 10000 gems"
            progressText = f"You have {orbsText}, {gemsText}, and {defeatedRiptoText}"
    elif goal == GoalOptions.TEN_TOKENS:
        goalText = "Collect 55 orbs and 8000 gems to unlock the theme park\nand collect all 10 tokens in Dragon Shores"
        progressText = f"You have {orbsText}, {gemsText}, and {tokensText}"
    elif goal == GoalOptions.ALL_SKILLPOINTS:
        goalText = "Collect all 16 skill points"
        progressText = f"You have {skillPointsText}"
    elif goal == GoalOptions.EPILOGUE:
        goalText = "Defeat Ripto and collect all 16 skill points"
        progressText = f"You have {skillPointsText} and {defeatedRiptoText}"
    else:
        logger.error("Error finding your goal")
        return
    logger.info(f"Your goal is: {goalText}\n{progressText}")

def cmd_options(self: "BizHawkClientCommandProcessor"):
    """Shows important options for your slot."""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Spyro 2":
        logger.warning("This command can only be used when playing Spyro 2: Ripto's Rage.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, Spyro2Client)

    gemsanityOption = ctx.slot_data["options"]["enable_gemsanity"]
    if gemsanityOption == GemsanityOptions.OFF:
        gemsanityOption = "Off"
    elif gemsanityOption == GemsanityOptions.PARTIAL:
        gemsanityOption = "Partial"
    else:
        gemsanityOption = "Full"
    levelLockOption = ctx.slot_data["options"]["level_lock_options"]
    moneybagssanity = "Moneybagssanity" if ctx.slot_data["options"]["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY else "Vanilla"
    if levelLockOption == LevelLockOptions.VANILLA:
        levelLockOption = "Vanilla"
    elif levelLockOption == LevelLockOptions.KEYS:
        levelLockOption = "Keys"
    trickDifficultyOption = ctx.slot_data["options"]["trick_difficulty"]
    trickDifficultyString = ""
    if trickDifficultyOption == TrickDifficultyOptions.OFF:
        trickDifficultyString = "Tricks Off"
    elif trickDifficultyOption == TrickDifficultyOptions.EASY:
        trickDifficultyString = "Easy Tricks"
    elif trickDifficultyOption == TrickDifficultyOptions.MEDIUM:
        trickDifficultyString = "Medium Tricks"
    elif trickDifficultyOption == TrickDifficultyOptions.HARD:
        trickDifficultyString = "Hard Tricks"
    else:
        trickDifficultyString = "Custom"
    worldSettings = "Open World" if ctx.slot_data["options"]["enable_open_world"] else "Vanilla Progression"
    goalEnum = ctx.slot_data["options"]["goal"]
    goalString = ""
    if goalEnum == GoalOptions.RIPTO:
        requiredOrbs = ctx.slot_data["options"]["ripto_door_orbs"]
        goalString = f"Ripto ({requiredOrbs} orbs)"
    elif goalEnum == GoalOptions.SIXTY_FOUR_ORB:
        goalString = "Sixty Four Orb"
    elif goalEnum == GoalOptions.HUNDRED_PERCENT:
        goalString = "Hundred Percent"
    elif goalEnum == GoalOptions.TEN_TOKENS:
        goalString = "Ten Tokens"
    elif goalEnum == GoalOptions.ALL_SKILLPOINTS:
        goalString = "All Skill Points"
    elif goalEnum == GoalOptions.EPILOGUE:
        goalString = "Epilogue"
    else:
        goalString = "Unknown"
    optionsString = (f"Goal: {goalString} - Use /goal for more info\n"
                    f"World Settings: {worldSettings}\n"
                    f"Level Locks: {levelLockOption}\n"
                    f"Moneybagssanity: {moneybagssanity}\n"
                    f"Gemsanity: {gemsanityOption}\n"
                    # TODO: Uncomment and support.
                    # f"Powerup Locks: {_powerupLockOption}\n"
                    f"Trick Difficulty: {trickDifficultyString}\n"
                    f"Ripto's Arena Requirement: {ctx.slot_data["options"]["ripto_door_orbs"]} orb(s)")
    logger.info(optionsString)

def cmd_unlockedlevels(self: "BizHawkClientCommandProcessor"):
    """When level locks are keys, shows the levels you have unlocked"""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Spyro 2":
        logger.warning("This command can only be used when playing Spyro 2: Ripto's Rage.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, Spyro2Client)
    client.showUnlockedLevels(ctx, True)

def cmd_debugInfo(self: "BizHawkClientCommandProcessor") -> None:
    """Prints information about your game to the screen."""
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Spyro 2":
        logger.warning("This command can only be used when playing Spyro 2: Ripto's Rage.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return
    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, Spyro2Client)

    host_version = "Unknown"
    if "apworldVersion" in ctx.slot_data:
        host_version = ctx.slot_data["apworldVersion"]
    # TODO: Add more information.
    logger.info(f"Host APWorld Version: {host_version}\n"
                f"Client Version: {client.client_version}\n"
                f"Current Level: {client.currentLevel}\n"
                "Screenshot this if requested to help debug issues.")

class Spyro3Client(BizHawkClient):
    game = "Spyro 3"
    system = "PSX"
    patch_suffix = ".apspyro3"

    apworld_manifest = orjson.loads(pkgutil.get_data(__name__, "archipelago.json").decode("utf-8"))
    client_version = apworld_manifest["world_version"]
    supported_versions = ["2.0.0"]

    boolsyncprogress = False
    syncWaitConfirm = False
    changeDeathlink = False
    DeathLink_DS = -1
    deathlink = -1
    changeItemIndex = False
    item_index_DS = 0
    resetClient = False
    gotDatastorage = False
    initDatastorage = False

    def __init__(self) -> None:
        super().__init__()
        self.messagequeue = []
        self.initClient = False
        self.riptoDefeated = False
        self.hasDoubleJumpItem = False
        self.hasFireballItem = False
        self.previous_death_link = 0
        self.pending_death_link: bool = False
        self.locations_list = {}
        # default to true, as we don't want to send a deathlink until playing
        self.sending_death_link: bool = True
        self.cosmeticQueue = []
        self.lastCosmeticUpdate = 0
        self.healthItemQueue = []
        self.moneybagsUnlocks = set()
        self.unlockedLevels = set()
        self.isInvisible = False
        self.invisibilityEnd = 0
        self.isDestructive = False
        self.destructiveEnd = 0
        self.maxHealth = 3
        self.currentLevel = None
        self.currentOrbs = 0
        self.currentGems = 0
        self.currentTalismans = 0
        self.currentSFTalismans = 0
        self.currentAPTalismans = 0
        self.currentTokens = 0
        self.currentSkillPoints = 0

    def initialize_client(self):
        self.messagequeue = []
        self.boolsyncprogress = False
        self.syncWaitConfirm = False
        self.changeDeathlink = False
        self.previous_death_link = 0
        self.pending_death_link: bool = False
        self.locations_list = {}
        # default to true, as we don't want to send a deathlink until playing
        self.sending_death_link: bool = True
        self.gotDatastorage = False
        self.initDatastorage = False
        self.cosmeticQueue = []
        self.lastCosmeticUpdate = 0
        self.healthItemQueue = []
        self.moneybagsUnlocks = set()
        self.unlockedLevels = set()
        self.riptoDefeated = False
        self.hasDoubleJumpItem = False
        self.hasFireballItem = False
        self.isInvisible = False
        self.invisibilityEnd = 0
        self.isDestructive = False
        self.destructiveEnd = 0
        self.maxHealth = 3
        self.currentLevel = None
        self.currentOrbs = 0
        self.currentGems = 0
        self.currentTalismans = 0
        self.currentSFTalismans = 0
        self.currentAPTalismans = 0
        self.currentTokens = 0
        self.currentSkillPoints = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        s2_identifier_ram_address: int = 0x9244
        # SCUS_944.25 in ASCII = Spyro 2
        bytes_expected: bytes = bytes.fromhex("534355535F3934342E3235")
        Commands_List = list(Commands_Dict.keys())
        try:
            bytes_actual: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                s2_identifier_ram_address, len(bytes_expected), "MainRAM"
            )]))[0]
            if bytes_actual != bytes_expected:
                # Remove commands from client
                for command in Commands_List:
                    if command in ctx.command_processor.commands:
                        ctx.command_processor.commands.pop(command)
                return False
        except Exception:
            # Remove commands from client
            for command in Commands_List:
                if command in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop(command)
            return False

        if not self.game == "Spyro 2":
            # Remove commands from client
            for command in Commands_List:
                if command in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop(command)
            return False
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        # Add custom commands to client
        for command in Commands_List:
            if command not in ctx.command_processor.commands:
                functionName = Commands_Dict[command]
                linkedfunction = globals()[functionName]
                ctx.command_processor.commands[command] = linkedfunction
        self.initialize_client()
        return True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Connected":
            host_version = "Unknown"
            if "apworldVersion" in ctx.slot_data:
                host_version = ctx.slot_data["apworldVersion"]
            if host_version in self.supported_versions:
                compatibility = "These versions are compatible"
            else:
                compatibility = "These versions may not be compatible"

            logger.info(f"================================================\n"
                        f"    -- Connected to Bizhawk successfully! --    \n"
                        f"      Archipelago Spyro 2 version {self.client_version}      \n"
                        f"      Host Spyro 2 version {host_version}                    \n"
                        f"      {compatibility}      \n"
                        #f"================================================\n"
                        #f"Custom commands are available for this game.    \n"
                        #f"Type /ae_commands for the full list.            \n"
                        f"================================================\n")
            self.initialize_client()
        if cmd == "Bounced":
            if "tags" in args:
                assert ctx.slot is not None
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.on_deathlink(ctx)

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
                    elif itemCategory == ItemClassification.filler:
                        itemClass = "Filler"
                    else:
                        itemClass = "Other"

                    recieverName = ctx.player_names[recieverID]
                    senderName = ctx.player_names[senderID]

                    if recieverID != ctx.slot and senderID == ctx.slot:
                        message = f"Sent '{itemName}' ({itemClass}) to {recieverName}"
                    elif recieverID == ctx.slot and senderID != ctx.slot:
                        message = f"Received '{itemName}' ({itemClass}) from {senderName}"
                    elif recieverID == ctx.slot and senderID == ctx.slot:
                        message =  f"You found your own '{itemName}' ({itemClass})"

                    self.messagequeue.append(message)
        if cmd == "Retrieved":
            if "keys" not in args:
                print(f"invalid Retrieved packet to Spyro2Client: {args}")
                return
            keys = dict(args["keys"])
            if f"S2_deathlink_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.DeathLink_DS = keys.get(f"S2_deathlink_{ctx.team}_{ctx.slot}", None)
                self.gotDatastorage = True
            if f"S2_item_index_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.item_index_DS = keys.get(f"S2_item_index_{ctx.team}_{ctx.slot}", 0)
                self.gotDatastorage = True
            else:
                self.item_index_DS = 0

    #async def set_auth(self, ctx: "BizHawkClientContext") -> None:
    #    pass

    async def ds_options_handling(self, ctx: "BizHawkClientContext", context):
        if context == "init":
            if ctx.team is None:
                self.initDatastorage = False
                return
            keys = [f"S2_{Option}_{ctx.team}_{ctx.slot}" for Option in ["deathlink"]]
            keys += [f"S2_item_index_{ctx.team}_{ctx.slot}"]
            await ctx.send_msgs([{"cmd": "Get", "keys": keys}])

            if not self.gotDatastorage:
                return

            self.initDatastorage = True

            # Deathlink
            if self.DeathLink_DS is None:
                # Used slotdata
                self.deathlink = int(ctx.slot_data["options"]["death_link"])
            else:
                # Got valid Datastorage, take this instead of slot_data
                self.deathlink = self.DeathLink_DS

            loggermessage = "\n--Options Status--\n"
            loggermessage += f"DeathLink: {"ON" if self.deathlink == 1 else "OFF"}\n"
            logger.info(loggermessage)
        elif context == "change":
            if self.changeDeathlink:
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": f"S2_deathlink_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": self.deathlink}],
                        }
                    ]
                )
                msg = f"Deathlink {"Enabled" if self.deathlink == 1 else "Disabled"}"
                await self.send_bizhawk_message(ctx, msg, "Passthrough", "")
                self.changeDeathlink = False
            if self.changeItemIndex:
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": f"S2_item_index_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": 0 if self.item_index_DS is None else self.item_index_DS}],
                        }
                    ]
                )
                self.changeItemIndex = False

    async def syncprogress(self, ctx: "BizHawkClientContext") -> None:
        if self.boolsyncprogress:
            self.boolsyncprogress = False

    async def process_bizhawk_messages(self, ctx: "BizHawkClientContext") -> None:
        for message in self.messagequeue:
            await self.send_bizhawk_message(ctx, message, "Custom", "")
            self.messagequeue.pop(0)

    async def send_bizhawk_message(self, ctx: "BizHawkClientContext", message, msgtype, data) -> None:
        if msgtype == "Custom":
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
        if self.initClient is False:
            self.initClient = True
            self.initialize_client()
            await self.ds_options_handling(ctx,"init")

            strMessage = "Connected to Bizhawk Client - Spyro 2 Archipelago v" + str(self.client_version)
            await self.send_bizhawk_message(ctx, strMessage, "Passthrough", "")

            startingHealth = 3
            sparxOption = ctx.slot_data["options"]["enable_progressive_sparx_health"]
            if sparxOption == SparxUpgradeOptions.BLUE:
                startingHealth = 2
            elif sparxOption == SparxUpgradeOptions.GREEN:
                startingHealth = 1
            elif sparxOption != SparxUpgradeOptions.OFF:
                startingHealth = 0
            self.maxHealth = startingHealth
        try:
            if self.gotDatastorage:
                # Last init to write the status
                if not self.initDatastorage:
                    await self.ds_options_handling(ctx, "init")

                if self.changeDeathlink or self.changeItemIndex:
                    await self.ds_options_handling(ctx, "change")
                if self.boolsyncprogress:
                    await self.syncprogress(ctx)
            else:
                # Not send anything before having the options set
                await self.ds_options_handling(ctx, "init")
                return

            # Set locations list to use within functions
            self.locations_list = ctx.checked_locations

            # Game state, locations and items read
            readsDict = {
                "recv_index": (RAM.lastReceivedArchipelagoID, 4, "MainRAM"),
                "gameStatus": (RAM.GameStatus, 1, "MainRAM"),
                "talismanCount": (RAM.TotalTalismanAddress, 1, "MainRAM"),
                "orbCount": (RAM.TotalOrbAddress, 1, "MainRAM"),
                "talismanBitArray": (RAM.TalismanStartAddress, 29, "MainRAM"),
                "orbBitArray": (RAM.OrbStartAddress, 29, "MainRAM"),
                "currentLevel": (RAM.CurrentLevelAddress, 1, "MainRAM"),
                "demoMode": (RAM.IsInDemoMode, 1, "MainRAM"),
                "guidebookText": (RAM.GuidebookText, 9, "MainRAM"),
                "resetCheck": (RAM.ResetCheckAddress, 4, "MainRAM"),
                "moneybagsFlags": (RAM.MoneybagsUnlocks, 0x4c, "MainRAM"),
                "skillPointFlags": (RAM.SkillPointAddresses, 0x11, "MainRAM"),
                "spiritParticles": (RAM.SpiritParticlesAddress, 1, "MainRAM"),
                "shoresTokens": (RAM.TokenAddress, 40, "MainRAM"),
                "totalGems": (RAM.TotalGemAddress, 4, "MainRAM"),
                "currentGems": (RAM.LevelGemsAddress, 29 * 4, "MainRAM"),
                "collectiblesMask": (RAM.GemMaskAddress, 0x0006b000 - 0x0006ac84, "MainRAM"),
                "lifeCount": (RAM.PlayerLives, 2, "MainRAM"),
                "sparxHealth": (RAM.PlayerHealth, 1, "MainRAM"),
                "localGemIncrement": (RAM.localGemIncrementAddress, 4, "MainRAM"),
                "globalGemIncrement": (RAM.globalGemIncrementAddress, 4, "MainRAM"),
                "globalGemRespawnFix": (RAM.globalGemRespawnFixAddress, 4, "MainRAM"),
                "localGemRespawnFix": (RAM.localGemRespawnFixAddress, 4, "MainRAM"),
                "playBeep": (RAM.playBeepAddress, 4, "MainRAM"),
                "doubleJumpLine1": (RAM.DoubleJumpAddress1, 4, "MainRAM"),
                "doubleJumpLine2": (RAM.DoubleJumpAddress2, 4, "MainRAM"),
                "permanentFireball": (RAM.PermanentFireballAddress, 1, "MainRAM"),
                "colossusHockeyScore": (RAM.ColossusSpyroHockeyScore, 1, "MainRAM"),
                "idolFishThrowUp": (RAM.IdolFishThrowUp, 4, "MainRAM"),
                "idolFishIncludeReds": (RAM.IdolFishIncludeReds, 4, "MainRAM"),
                "idolFishIncludeRedsHUD": (RAM.IdolFishIncludeRedsHUD, 4, "MainRAM"),
                "hurricosLightningThiefAddresses": (RAM.HurricosLightningThiefAddresses, 0x18CFC0 - 0x18C8A8, "MainRAM"),
                "spyroHUDScore": (RAM.spyroHUDScore, 1, "MainRAM"),
                "secondBomboStatus": (RAM.secondBomboStatus, 1, "MainRAM"),
                "secondBomboZPos": (RAM.secondBomboStatus - 0x35, 4, "MainRAM"),
                "thirdBomboStatus": (RAM.thirdBomboStatus, 1, "MainRAM"),
                "thirdBomboZPos": (RAM.secondBomboStatus - 0x35, 4, "MainRAM"),
                "bomboAttackAddress": (RAM.bomboAttackAddress, 4, "MainRAM"),
                "fractureHeadbashCheck": (RAM.fractureHeadbashCheck, 4, "MainRAM"),
                "fractureEarthshaperAddresses": (RAM.FractureEarthshaperAddresses, 0x189000 - 0x188DB8, "MainRAM"),
                "maxFractureSpiritParticles": (RAM.maxFractureSpiritParticles, 1, "MainRAM"),
                "opponentHUDScore": (RAM.opponentHUDScore, 1, "MainRAM"),
                "shadyHeadbashCheck": (RAM.ShadyHeadbashCheck, 4, "MainRAM"),
                "gulpDoubleDamage": (RAM.GulpDoubleDamage, 1, "MainRAM"),
                "redGemShadow": (RAM.RedGemShadow, 4, "MainRAM"),
                "redGemColor": (RAM.RedGemColor, 4, "MainRAM"),
                "greenGemShadow": (RAM.GreenGemShadow, 4, "MainRAM"),
                "greenGemColor": (RAM.GreenGemColor, 4, "MainRAM"),
                "blueGemShadow": (RAM.BlueGemShadow, 4, "MainRAM"),
                "blueGemColor": (RAM.BlueGemColor, 4, "MainRAM"),
                "goldGemShadow": (RAM.GoldGemShadow, 4, "MainRAM"),
                "goldGemColor": (RAM.GoldGemColor, 4, "MainRAM"),
                "pinkGemShadow": (RAM.PinkGemShadow, 4, "MainRAM"),
                "pinkGemColor": (RAM.PinkGemColor, 4, "MainRAM"),
                "portalTextRed": (RAM.PortalTextRed, 1, "MainRAM"),
                "portalTextGreen": (RAM.PortalTextGreen, 1, "MainRAM"),
                "portalTextBlue": (RAM.PortalTextBlue, 1, "MainRAM"),
                "riptoDoorOrbRequirement": (RAM.RiptoDoorOrbRequirementAddress, 1, "MainRAM"),
                "riptoDoorOrbDisplay": (RAM.RiptoDoorOrbDisplayAddress, 1, "MainRAM"),
                "crushGuidebookUnlock": (RAM.CrushGuidebookUnlock, 1, "MainRAM"),
                "gulpGuidebookUnlock": (RAM.GulpGuidebookUnlock, 1, "MainRAM"),
                "autumnGuidebookUnlock": (RAM.AutumnGuidebookUnlock, 1, "MainRAM"),
                "winterGuidebookUnlock": (RAM.WinterGuidebookUnlock, 1, "MainRAM"),
                "wtWarpReroute": (RAM.WTWarpAddress, 2, "MainRAM"),
                "wtDoorGem": (RAM.WTDoorGemAddress, 1, "MainRAM"),
                "wtWallOrb": (RAM.WTWallOrbAddress, 1, "MainRAM"),
                "invisibleAddress1": (RAM.InvisibleAddress1, 2, "MainRAM"),
                "invisibleAddress2": (RAM.InvisibleAddress2, 2, "MainRAM"),
                "destructiveAddress": (RAM.DestructiveSpyroAddress, 2, "MainRAM"),
                "zPos": (RAM.PlayerZPos, 4, "MainRAM"),
                "animationLength": (RAM.PlayerAnimationLength, 4, "MainRAM"),
                "spyroState": (RAM.SpyroStateAddress, 1, "MainRAM"),
                "spyroVelocityFlag": (RAM.PlayerVelocityStatus, 1, "MainRAM"),
            }

            readTuples = [Value for Value in readsDict.values()]

            reads = await bizhawk.read(ctx.bizhawk_ctx, readTuples)
            reads = [int.from_bytes(reads[i], byteorder = "little") for i,x in enumerate(reads)]
            readValues = dict(zip(readsDict.keys(), reads))

            recv_index = readValues["recv_index"]
            gameStatus = readValues["gameStatus"]
            talismanCount = readValues["talismanCount"]
            orbCount = readValues["orbCount"]
            talismanBitArray = readValues["talismanBitArray"]
            orbBitArray = readValues["orbBitArray"]
            currentLevel = readValues["currentLevel"]
            self.currentLevel = currentLevel
            demoMode = readValues["demoMode"]
            try:
                guidebookText = readValues["guidebookText"].to_bytes(9, byteorder = "little").decode("ascii")
            except Exception:
                guidebookText = ""
            resetCheck = readValues["resetCheck"]
            moneybagsFlags = readValues["moneybagsFlags"]
            skillPointFlags = readValues["skillPointFlags"]
            spiritParticles = readValues["spiritParticles"]
            shoresTokens = readValues["shoresTokens"]
            totalGems = readValues["totalGems"]
            currentGems = readValues["currentGems"]
            collectiblesMask = readValues["collectiblesMask"]
            lifeCount = readValues["lifeCount"]
            sparxHealth = readValues["sparxHealth"]
            localGemIncrement = readValues["localGemIncrement"]
            globalGemIncrement = readValues["globalGemIncrement"]
            globalGemRespawnFix = readValues["globalGemRespawnFix"]
            localGemRespawnFix = readValues["localGemRespawnFix"]
            playBeep = readValues["playBeep"]
            doubleJumpLine1 = readValues["doubleJumpLine1"]
            doubleJumpLine2 = readValues["doubleJumpLine2"]
            permanentFireball = readValues["permanentFireball"]
            colossusHockeyScore = readValues["colossusHockeyScore"]
            idolFishThrowUp = readValues["idolFishThrowUp"]
            idolFishIncludeReds = readValues["idolFishIncludeReds"]
            idolFishIncludeRedsHUD = readValues["idolFishIncludeRedsHUD"]
            hurricosLightningThiefAddresses = readValues["hurricosLightningThiefAddresses"]
            spyroHUDScore = readValues["spyroHUDScore"]
            secondBomboStatus = readValues["secondBomboStatus"]
            secondBomboZPos = readValues["secondBomboZPos"]
            thirdBomboStatus = readValues["thirdBomboStatus"]
            thirdBomboZPos = readValues["thirdBomboZPos"]
            bomboAttackAddress = readValues["bomboAttackAddress"]
            fractureHeadbashCheck = readValues["fractureHeadbashCheck"]
            fractureEarthshaperAddresses = readValues["fractureEarthshaperAddresses"]
            maxFractureSpiritParticles = readValues["maxFractureSpiritParticles"]
            opponentHUDScore = readValues["opponentHUDScore"]
            shadyHeadbashCheck = readValues["shadyHeadbashCheck"]
            gulpDoubleDamage = readValues["gulpDoubleDamage"]
            redGemShadow = readValues["redGemShadow"]
            redGemColor = readValues["redGemColor"]
            greenGemShadow = readValues["greenGemShadow"]
            greenGemColor = readValues["greenGemColor"]
            blueGemShadow = readValues["blueGemShadow"]
            blueGemColor = readValues["blueGemColor"]
            goldGemShadow = readValues["goldGemShadow"]
            goldGemColor = readValues["goldGemColor"]
            pinkGemShadow = readValues["pinkGemShadow"]
            pinkGemColor = readValues["pinkGemColor"]
            portalTextRed = readValues["portalTextRed"]
            portalTextGreen = readValues["portalTextGreen"]
            portalTextBlue = readValues["portalTextBlue"]
            riptoDoorOrbRequirement = readValues["riptoDoorOrbRequirement"]
            riptoDoorOrbDisplay = readValues["riptoDoorOrbDisplay"]
            crushGuidebookUnlock = readValues["crushGuidebookUnlock"]
            gulpGuidebookUnlock = readValues["gulpGuidebookUnlock"]
            autumnGuidebookUnlock = readValues["autumnGuidebookUnlock"]
            winterGuidebookUnlock = readValues["winterGuidebookUnlock"]
            wtWarpReroute = readValues["wtWarpReroute"]
            wtDoorGem = readValues["wtDoorGem"]
            wtWallOrb = readValues["wtWallOrb"]
            invisibleAddress1 = readValues["invisibleAddress1"]
            invisibleAddress2 = readValues["invisibleAddress2"]
            destructiveAddress = readValues["destructiveAddress"]
            zPos = readValues["zPos"]
            animationLength = readValues["animationLength"]
            spyroState = readValues["spyroState"]
            spyroVelocityFlag = readValues["spyroVelocityFlag"]

            # Write tables
            itemsWrites = []

            # Handle reconnecting and loading into saves without resetting.
            if recv_index != self.item_index_DS and self.item_index_DS is not None:
                recv_index = self.item_index_DS
            elif recv_index != self.item_index_DS and self.item_index_DS is None:
                recv_index = 0

            START_recv_index = recv_index

            # Prevent sending items when connecting early (Sony, Menu or Intro Cutscene)
            firstBootStates = {GameStatus.TitleScreen, GameStatus.Loading}
            boolIsFirstBoot = guidebookText != "Guidebook" or demoMode == 1 or gameStatus in firstBootStates or resetCheck == 0
            if recv_index <= (len(ctx.items_received)) and not boolIsFirstBoot:
                increment = 0
                orbCountFromServer = 0
                sfTalismansFromServer = 0
                apTalismansFromServer = 0
                skillPointsFromServer = 0
                shoresTokensFromServer = 0
                newLives = 0
                healthItemTimestamp = time.time()
                newHealthItems = []
                gemsanityItems = {}
                sparxUpgrades = 0
                oldUnlockedLevels = len(self.unlockedLevels)

                for item in ctx.items_received:
                    # Increment to already received address first before sending
                    itemName = ctx.item_names.lookup_in_slot(item.item, ctx.slot)
                    if itemName == "Orb":
                        orbCountFromServer += 1
                    elif itemName == "Summer Forest Talisman":
                        sfTalismansFromServer += 1
                    elif itemName == "Autumn Plains Talisman":
                        apTalismansFromServer += 1
                    elif itemName == "Ripto Defeated":
                        self.riptoDefeated = True
                    elif itemName == "Skill Point":
                        skillPointsFromServer += 1
                    elif itemName == "Dragon Shores Token":
                        shoresTokensFromServer += 1
                    elif itemName.endswith("Gem") or itemName.endswith("Gems") or itemName.endswith("Gem Bundle"):
                        if itemName in gemsanityItems:
                            gemsanityItems[itemName] += 1
                        else:
                            gemsanityItems[itemName] = 1
                    elif itemName.startswith("Moneybags Unlock"):
                        if ctx.slot_data["options"]["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY or \
                            ctx.slot_data["options"]["start_with_abilities"] and \
                            (
                                itemName.endswith("Swim") or itemName.endswith("Climb") or itemName.endswith("Headbash")
                            ):
                            #if itemName not in self.moneybagsUnlocks:
                            #    logger.info("If you are in the same zone as Moneybags, you can talk to him to complete the unlock for free.")
                            self.moneybagsUnlocks.add(itemName)
                    elif itemName == "Double Jump Ability":
                        self.hasDoubleJumpItem = True
                    elif itemName == "Permanent Fireball Ability":
                        self.hasFireballItem = True
                    elif itemName.endswith("Unlock"):
                        self.unlockedLevels.add(itemName)
                    elif itemName == "Progressive Sparx Health Upgrade":
                        sparxUpgrades += 1
                    if increment < START_recv_index:
                        increment += 1
                    else:
                        if itemName == "Extra Life":
                            newLives += 1
                        elif itemName == "Damage Sparx Trap":
                            newHealthItems.append(itemName)
                        elif itemName == "Sparxless Trap":
                            newHealthItems.append(itemName)
                        elif itemName == "Heal Sparx":
                            newHealthItems.append(itemName)
                        elif itemName in ["Big Head Mode", "Flat Spyro Mode", "Turn Spyro Red", "Turn Spyro Blue", "Turn Spyro Pink", "Turn Spyro Yellow", "Turn Spyro Green", "Turn Spyro Black", "Normal Spyro"]:
                            self.cosmeticQueue.append(itemName)
                        elif itemName == "Invisibility Trap":
                            if self.isInvisible:
                                self.invisibilityEnd += 15
                            else:
                                self.invisibilityEnd = time.time() + 15
                                self.isInvisible = True
                        elif itemName == "Destructive Spyro":
                            if self.isDestructive:
                                self.destructiveEnd += 15
                            else:
                                self.destructiveEnd = time.time() + 15
                                self.isDestructive = True
                        recv_index += 1

                # Writes to memory if there is a new item, after the loop
                # If the increment is different from recv_index this means we received items
                if increment != recv_index:
                    itemsWrites += [(RAM.lastReceivedArchipelagoID, recv_index.to_bytes(4, "little"), "MainRAM")]
                    itemsWrites += [(RAM.tempLastReceivedArchipelagoID, recv_index.to_bytes(4, "little"), "MainRAM")]
                    self.changeItemIndex = True
                    self.item_index_DS = recv_index
                if orbCountFromServer != orbCount:
                    itemsWrites += [(RAM.TotalOrbAddress, orbCountFromServer.to_bytes(1, "little"), "MainRAM")]
                self.currentOrbs = orbCountFromServer
                if currentLevel != LevelInGameIDs.SummerForest and talismanCount != sfTalismansFromServer + apTalismansFromServer:
                    itemsWrites += [(RAM.TotalTalismanAddress, (sfTalismansFromServer + apTalismansFromServer).to_bytes(1, "little"), "MainRAM")]
                elif currentLevel == LevelInGameIDs.SummerForest and talismanCount != sfTalismansFromServer:
                    itemsWrites += [(RAM.TotalTalismanAddress, sfTalismansFromServer.to_bytes(1, "little"), "MainRAM")]
                self.currentTalismans = sfTalismansFromServer + apTalismansFromServer
                if self.currentAPTalismans != apTalismansFromServer or self.currentSFTalismans != sfTalismansFromServer:
                    logger.info(f"Current Talisman count - Summer Forest: {sfTalismansFromServer}; Autumn Plains: {apTalismansFromServer}")
                self.currentSFTalismans = sfTalismansFromServer
                self.currentAPTalismans = apTalismansFromServer
                if newLives != 0:
                    itemsWrites += [(RAM.PlayerLives, min(99, lifeCount + newLives).to_bytes(2, "little"), "MainRAM")]
                if len(newHealthItems) > 0:
                    self.healthItemQueue += [(healthItemTimestamp, newHealthItems)]
                self.currentTokens = shoresTokensFromServer
                self.currentSkillPoints = skillPointsFromServer

                if oldUnlockedLevels < len(self.unlockedLevels):
                    self.showUnlockedLevels(ctx)

                startingHealth = 3
                sparxOption = ctx.slot_data["options"]["enable_progressive_sparx_health"]
                if sparxOption == SparxUpgradeOptions.BLUE:
                    startingHealth = 2
                elif sparxOption == SparxUpgradeOptions.GREEN:
                    startingHealth = 1
                elif sparxOption != SparxUpgradeOptions.OFF:
                    startingHealth = 0
                self.maxHealth = startingHealth + sparxUpgrades

                if ctx.slot_data["options"]["enable_gemsanity"]:
                    itemsWrites += self.calculateCurrentGems(ctx, gemsanityItems, currentGems, totalGems)
                else:
                    self.currentGems = totalGems

                cosmeticTimestamp = time.time()
                if len(self.cosmeticQueue) > 0 and cosmeticTimestamp > self.lastCosmeticUpdate + 5:
                    self.lastCosmeticUpdate = cosmeticTimestamp
                    cosmeticChange = self.cosmeticQueue.pop(0)
                    cosmeticWrites = self.processCosmeticChange(cosmeticChange)
                    if len(cosmeticWrites) > 0:
                        itemsWrites += cosmeticWrites

                # Check for victory conditions
                currentgoal = ctx.slot_data["options"]["goal"]
                if not ctx.finished_game:
                    has_goaled = False
                    if currentgoal == GoalOptions.RIPTO and orbCountFromServer >= ctx.slot_data["options"]["ripto_door_orbs"] and self.riptoDefeated:
                        has_goaled = True
                    elif currentgoal == GoalOptions.SIXTY_FOUR_ORB and orbCountFromServer >= 64 and self.riptoDefeated:
                        has_goaled = True
                    elif currentgoal == GoalOptions.HUNDRED_PERCENT and orbCountFromServer >= 64 and \
                            (ctx.slot_data["options"]["enable_open_world"] or sfTalismansFromServer + apTalismansFromServer >= 14) and \
                            totalGems >= 10000 and self.riptoDefeated:
                        has_goaled = True
                    elif currentgoal == GoalOptions.ALL_SKILLPOINTS and skillPointsFromServer >= 16:
                        has_goaled = True
                    elif currentgoal == GoalOptions.EPILOGUE and skillPointsFromServer >= 16 and self.riptoDefeated:
                        has_goaled = True
                    elif currentgoal == GoalOptions.TEN_TOKENS and shoresTokensFromServer >= 10 and orbCountFromServer >= 55 and totalGems >= 8000:
                        has_goaled = True
                    if has_goaled:
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                        await self.send_bizhawk_message(ctx, "You have completed your goal", "Passthrough", "")
                        ctx.finished_game = True

            if len(itemsWrites) > 0:
                await bizhawk.write(ctx.bizhawk_ctx, itemsWrites)

            # ======== Locations handling =========
            if not boolIsFirstBoot:
                Locations_Reads = [
                    currentLevel,
                    talismanBitArray,
                    orbBitArray,
                    moneybagsFlags,
                    skillPointFlags,
                    spiritParticles,
                    shoresTokens,
                    totalGems,
                    currentGems,
                    collectiblesMask
                ]
                await self.locations_handling(ctx, Locations_Reads)

            if not boolIsFirstBoot and gameStatus not in [GameStatus.Paused, GameStatus.LoadingWorld]:
                # ======== Gemsanity Code Handling ========
                if ctx.slot_data["options"]["enable_gemsanity"]:
                    gemsanity_reads = [localGemIncrement, globalGemIncrement, globalGemRespawnFix, localGemRespawnFix, playBeep]
                    gemsanityWrites = self.handleGemsanity(gemsanity_reads)
                    if len(gemsanityWrites) > 0:
                        await bizhawk.write(ctx.bizhawk_ctx, gemsanityWrites)

                # ======== Moneybags Unlock Handling ========
                moneybagsWrites = self.handleMoneybags(ctx, self.moneybagsUnlocks, moneybagsFlags)
                if len(moneybagsWrites) > 0:
                    await bizhawk.write(ctx.bizhawk_ctx, moneybagsWrites)

                # ======== Ability Handling ========
                abilityReads = [doubleJumpLine1, doubleJumpLine2, permanentFireball]
                abilityWrites = self.handleAbilities(ctx, abilityReads)
                if len(abilityWrites) > 0:
                    await bizhawk.write(ctx.bizhawk_ctx, abilityWrites)

                # ======== Easy Challenge Handling ========
                easyChallengeReads = [
                    currentLevel,
                    colossusHockeyScore,
                    idolFishThrowUp,
                    idolFishIncludeReds,
                    idolFishIncludeRedsHUD,
                    hurricosLightningThiefAddresses,
                    spyroHUDScore,
                    secondBomboStatus,
                    secondBomboZPos,
                    thirdBomboStatus,
                    thirdBomboZPos,
                    bomboAttackAddress,
                    fractureHeadbashCheck,
                    fractureEarthshaperAddresses,
                    maxFractureSpiritParticles,
                    opponentHUDScore,
                    shadyHeadbashCheck,
                    gulpDoubleDamage
                ]
                easyChallengeWrites = self.handleEasyChallenge(ctx, easyChallengeReads)
                if len(easyChallengeWrites) > 0:
                    await bizhawk.write(ctx.bizhawk_ctx, easyChallengeWrites)

                # ======== Color Change Handling ========
                colorChangeReads = [
                    redGemShadow,
                    redGemColor,
                    greenGemShadow,
                    greenGemColor,
                    blueGemShadow,
                    blueGemColor,
                    goldGemShadow,
                    goldGemColor,
                    pinkGemShadow,
                    pinkGemColor,
                    portalTextRed,
                    portalTextGreen,
                    portalTextBlue
                ]
                colorChangeWrites = self.handleColorChanges(ctx, colorChangeReads)
                if len(colorChangeWrites) > 0:
                    await bizhawk.write(ctx.bizhawk_ctx, colorChangeWrites)

                # ======== Elora Text and Door Requirements ========
                # Menuing out of Winter Tundra crashes the game on save file load,
                # since the level ID doesn't change.
                if gameStatus != GameStatus.GameLoadMaybe:
                    eloraDoorReads = [currentLevel, riptoDoorOrbRequirement, riptoDoorOrbDisplay]
                    eloraDoorWrites = self.handleEloraDoorChanges(ctx, eloraDoorReads)
                    if len(eloraDoorWrites) > 0:
                        await bizhawk.write(ctx.bizhawk_ctx, eloraDoorWrites)

                # ======== Open World Handling ========
                openWorldReads = [crushGuidebookUnlock, gulpGuidebookUnlock, autumnGuidebookUnlock, winterGuidebookUnlock]
                openWorldWrites = self.handleOpenWorldChanges(ctx, openWorldReads)
                if len(openWorldWrites) > 0:
                    await bizhawk.write(ctx.bizhawk_ctx, openWorldWrites)

                # ======== Level Lock Handling ========
                levelLockReads = [currentLevel]
                levelLockWrites = self.handleLevelLockChanges(ctx, levelLockReads)
                if len(levelLockWrites) > 0:
                    await bizhawk.write(ctx.bizhawk_ctx, levelLockWrites)

                # ======== Winter Tundra Warp Handling ========
                wtWarpReads = [wtWarpReroute, wtDoorGem, wtWallOrb]
                wtWarpWrites = self.handleWinterWarpChanges(ctx, wtWarpReads)
                if len(wtWarpWrites) > 0:
                    await bizhawk.write(ctx.bizhawk_ctx, wtWarpWrites)

                # ======== Invisibility Handling ========
                invisibilityReads = [invisibleAddress1, invisibleAddress2]
                invisibilityWrites = self.handleInvisibilityChanges(invisibilityReads)
                if len(invisibilityWrites) > 0:
                    await bizhawk.write(ctx.bizhawk_ctx, invisibilityWrites)

                # ======== Destructive Spyro Handling ========
                destructiveReads = [destructiveAddress]
                destructiveWrites = self.handleDestructiveChanges(destructiveReads)
                if len(destructiveWrites) > 0:
                    await bizhawk.write(ctx.bizhawk_ctx, destructiveWrites)

                # ======== Sparx Health Handling ========
                sparxReads = [sparxHealth]
                sparxWrites = self.handleSparxChanges(sparxReads)
                if len(sparxWrites) > 0:
                    await bizhawk.write(ctx.bizhawk_ctx, sparxWrites)

                # ======== Handle Death Link =========
                DL_Reads = [
                    currentLevel,
                    sparxHealth,
                    gameStatus,
                    zPos,
                    animationLength,
                    spyroVelocityFlag,
                    spyroState
                ]
                await self.handle_death_link(ctx, DL_Reads)

            # ======== Update tags (DeathLink) =========
            await self.update_tags(ctx)

            # If there is messages waiting in the queue, print them to Bizhawk
            if self.messagequeue is not None and self.messagequeue != []:
                await self.process_bizhawk_messages(ctx)
            return

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def locations_handling(self, ctx: "BizHawkClientContext", Locations_Reads) -> None:
        current_level = Locations_Reads[0]
        talisman_bit_array = Locations_Reads[1].to_bytes(29, "little")
        orb_bit_array = Locations_Reads[2].to_bytes(29, "little")
        moneybags_flags = Locations_Reads[3].to_bytes(0x4c, "little")
        skill_point_flags = Locations_Reads[4].to_bytes(0x11, "little")
        spirit_particles = Locations_Reads[5]
        shores_tokens = Locations_Reads[6].to_bytes(40, "little")
        total_gems = Locations_Reads[7]
        current_gems = Locations_Reads[8].to_bytes(29 * 4, "little")
        collectibles_mask = Locations_Reads[9].to_bytes(0x0006b000 - 0x0006ac84, "little")

        gemsanity_ids = ctx.slot_data["gemsanity_ids"]

        talismansToSend = set()
        orbsToSend = set()
        bossesToSend = set()
        moneybagsUnlocksToSend = set()
        skillPointUnlocksToSend = set()
        spiritParticlesToSend = set()
        tokensToSend = set()
        totalGemsToSend = set()
        levelGemsToSend = set()
        bottlesToSend = set()
        gemsToSend = set()

        base_id = 1230000
        level_offset = 1000
        level_index = 0
        levels = GetLevelData()
        for level in levels:
            location_offset = 0
            if level.HasTalisman:
                id = base_id + level_offset * level.LevelId + location_offset
                if talisman_bit_array[level_index] != 0 and id not in self.locations_list:
                    talismansToSend.add(id)
                location_offset += 1
            for i in range(level.OrbCount):
                id = base_id + level_offset * level.LevelId + location_offset
                orb_bit = pow(2, i)
                if orb_bit_array[level_index] & orb_bit != 0 and id not in self.locations_list:
                    orbsToSend.add(id)
                location_offset += 1
            if level.IsBoss:
                id = base_id + level_offset * level.LevelId + location_offset
                if talisman_bit_array[level_index] != 0 and id not in self.locations_list:
                    bossesToSend.add(id)
                location_offset += 1
            for i in range(len(level.MoneybagsAddresses)):
                id = base_id + level_offset * level.LevelId + location_offset
                if ctx.slot_data["options"]["moneybags_settings"] != MoneybagsOptions.MONEYBAGSSANITY:
                    # First 2 bytes are price.
                    if moneybags_flags[level.MoneybagsAddresses[i] + 2] != 0 and id not in self.locations_list:
                        moneybagsUnlocksToSend.add(id)
                location_offset += 1
            for i in range(len(level.SkillPointAddresses)):
                id = base_id + level_offset * level.LevelId + location_offset
                if ctx.slot_data["options"]["enable_skillpoint_checks"]:
                    if skill_point_flags[level.SkillPointAddresses[i]] != 0 and id not in self.locations_list:
                        skillPointUnlocksToSend.add(id)
                location_offset += 1
                id = base_id + level_offset * level.LevelId + location_offset
                if ctx.slot_data["options"]["goal"] in [GoalOptions.ALL_SKILLPOINTS, GoalOptions.EPILOGUE]:
                    if skill_point_flags[level.SkillPointAddresses[i]] != 0 and id not in self.locations_list:
                        skillPointUnlocksToSend.add(id)
                location_offset += 1
            for i in range(len(level.LifeBottleAddresses)):
                id = base_id + level_offset * level.LevelId + location_offset
                if ctx.slot_data["options"]["enable_life_bottle_checks"]:
                    bottle_bit = pow(2, level.LifeBottleAddresses[i][1])
                    if collectibles_mask[level.LifeBottleAddresses[i][0]] & bottle_bit != 0 and id not in self.locations_list:
                        bottlesToSend.add(id)
                location_offset += 1
            gem_index = 1
            for i in range(level.TotalGemCount + len(level.GemSkipIndices)):
                if i + 1 not in level.GemSkipIndices:
                    location_id = base_id + level_offset * level.LevelId + location_offset
                    if current_level == level.LevelId:
                        if ctx.slot_data["options"]["enable_gemsanity"] and (len(gemsanity_ids) == 0 or location_id in gemsanity_ids):
                            gem_bit = pow(2, i % 8)
                            if collectibles_mask[level.GemMaskAddress + math.floor(i / 8)] & gem_bit != 0 and location_id not in self.locations_list:
                                gemsToSend.add(location_id)
                    location_offset += 1
                    gem_index += 1
            if level.SpiritParticles > 0:
                id = base_id + level_offset * level.LevelId + location_offset
                if current_level == level.LevelId and ctx.slot_data["options"]["enable_spirit_particle_checks"]:
                    send_check = False
                    if ctx.slot_data["options"]["fracture_easy_earthshapers"] and level.Name == "Fracture Hills":
                        if spirit_particles >= level.SpiritParticles - 7:
                            send_check = True
                    else:
                        if spirit_particles >= level.SpiritParticles:
                            send_check = True
                    if send_check and id not in self.locations_list:
                        spiritParticlesToSend.add(id)
                location_offset += 1
            if level.Name == "Dragon Shores":
                for i in range(10):
                    id = base_id + level_offset * level.LevelId + i
                    if ctx.slot_data["options"]["goal"] == GoalOptions.TEN_TOKENS:
                        if shores_tokens[4 * i] != 0 and id not in self.locations_list:
                            tokensToSend.add(id)
                    location_offset += 1
            level_index += 1

        base_id = 1259000
        for i in range(20):
            id = base_id + i
            if ctx.slot_data["options"]["enable_total_gem_checks"] and \
                    int(ctx.slot_data["options"]["max_total_gem_checks"]) >= 500 * (i + 1):
                if total_gems >= 500 * (i + 1) and id not in self.locations_list:
                    totalGemsToSend.add(id)
        current_gem_address = 0
        offset = 20
        for level in levels:
            if not level.IsBoss:
                if ctx.slot_data["options"]["enable_25_pct_gem_checks"]:
                    id = base_id + offset
                    if int.from_bytes(current_gems[current_gem_address:current_gem_address+4], "little") >= 100 and id not in self.locations_list:
                        levelGemsToSend.add(id)
                offset += 1
                if ctx.slot_data["options"]["enable_50_pct_gem_checks"]:
                    id = base_id + offset
                    if int.from_bytes(current_gems[current_gem_address:current_gem_address+4], "little") >= 200 and id not in self.locations_list:
                        levelGemsToSend.add(id)
                offset += 1
                if ctx.slot_data["options"]["enable_75_pct_gem_checks"]:
                    id = base_id + offset
                    if int.from_bytes(current_gems[current_gem_address:current_gem_address+4], "little") >= 300 and id not in self.locations_list:
                        levelGemsToSend.add(id)
                offset += 1
                if ctx.slot_data["options"]["enable_gem_checks"]:
                    id = base_id + offset
                    if int.from_bytes(current_gems[current_gem_address:current_gem_address+4], "little") >= 400 and id not in self.locations_list:
                        levelGemsToSend.add(id)
                offset += 1
            current_gem_address += 4

        locationsToSend = (talismansToSend | orbsToSend | bossesToSend | moneybagsUnlocksToSend |
                           skillPointUnlocksToSend | spiritParticlesToSend | tokensToSend | totalGemsToSend |
                           levelGemsToSend | bottlesToSend | gemsToSend)
        if locationsToSend != "" and locationsToSend != set():
             await ctx.check_locations(locationsToSend)

    def processCosmeticChange(self, cosmeticChange):
        cosmeticWrites = []
        if cosmeticChange == "Normal Spyro":
            cosmeticWrites += [
                (RAM.SpyroColorAddress, (SpyroColor.SpyroColorDefault).to_bytes(4, "little"), "MainRAM"),
                (RAM.BigHeadMode, (0).to_bytes(2, "little"), "MainRAM")
            ]
        elif cosmeticChange == "Turn Spyro Red":
            cosmeticWrites += [
                (RAM.SpyroColorAddress, (SpyroColor.SpyroColorRed).to_bytes(4, "little"), "MainRAM")
            ]
        elif cosmeticChange == "Turn Spyro Blue":
            cosmeticWrites += [
                (RAM.SpyroColorAddress, (SpyroColor.SpyroColorBlue).to_bytes(4, "little"), "MainRAM")
            ]
        elif cosmeticChange == "Turn Spyro Yellow":
            cosmeticWrites += [
                (RAM.SpyroColorAddress, (SpyroColor.SpyroColorYellow).to_bytes(4, "little"), "MainRAM")
            ]
        elif cosmeticChange == "Turn Spyro Pink":
            cosmeticWrites += [
                (RAM.SpyroColorAddress, (SpyroColor.SpyroColorPink).to_bytes(4, "little"), "MainRAM")
            ]
        elif cosmeticChange == "Turn Spyro Green":
            cosmeticWrites += [
                (RAM.SpyroColorAddress, (SpyroColor.SpyroColorGreen).to_bytes(4, "little"), "MainRAM")
            ]
        elif cosmeticChange == "Turn Spyro Black":
            cosmeticWrites += [
                (RAM.SpyroColorAddress, (SpyroColor.SpyroColorBlack).to_bytes(4, "little"), "MainRAM")
            ]
        elif cosmeticChange == "Big Head Mode":
            cosmeticWrites += [
                (RAM.SpyroHeight, (32).to_bytes(1, "little"), "MainRAM"),
                (RAM.SpyroLength, (32).to_bytes(1, "little"), "MainRAM"),
                (RAM.SpyroWidth, (32).to_bytes(1, "little"), "MainRAM"),
                (RAM.BigHeadMode, (1).to_bytes(2, "little"), "MainRAM")
            ]
        elif cosmeticChange == "Flat Spyro Mode":
            cosmeticWrites += [
                (RAM.SpyroHeight, (16).to_bytes(1, "little"), "MainRAM"),
                (RAM.SpyroLength, (16).to_bytes(1, "little"), "MainRAM"),
                (RAM.SpyroWidth, (2).to_bytes(1, "little"), "MainRAM"),
                (RAM.BigHeadMode, (0x100).to_bytes(2, "little"), "MainRAM")
            ]
        return cosmeticWrites

    def calculateCurrentGems(self, ctx, gemsanityItems, currentGems, totalGems):
        gemItems = []
        currentGemsArr = currentGems.to_bytes(29 * 4, "little")
        newTotalGems = 0
        levels = GetLevelData()
        level_index = 0
        if "gemsanity_gem_bundle_size" in ctx.slot_data["options"]:
            gem_bundle_size = ctx.slot_data["options"]["gemsanity_gem_bundle_size"]
        else:
            gem_bundle_size = 0  # This case shouldn't happen but to be safe.

        for level in levels:
            current_gems = int.from_bytes(currentGemsArr[level_index * 4 : level_index * 4 + 4], "little")
            newCurrentGems = 0
            if "Speedway" in level.Name:
                newTotalGems += current_gems
            else:
                if f"{level.Name} Red Gem" in gemsanityItems.keys():
                    newCurrentGems += 1 * gemsanityItems[f"{level.Name} Red Gem"]
                if f"{level.Name} Green Gem" in gemsanityItems.keys():
                    newCurrentGems += 2 * gemsanityItems[f"{level.Name} Green Gem"]
                if f"{level.Name} Blue Gem" in gemsanityItems.keys():
                    newCurrentGems += 5 * gemsanityItems[f"{level.Name} Blue Gem"]
                if f"{level.Name} Gold Gem" in gemsanityItems.keys():
                    newCurrentGems += 10 * gemsanityItems[f"{level.Name} Gold Gem"]
                if f"{level.Name} Pink Gem" in gemsanityItems.keys():
                    newCurrentGems += 25 * gemsanityItems[f"{level.Name} Pink Gem"]
                if f"{level.Name} 50 Gems" in gemsanityItems.keys():
                    newCurrentGems += 50 * gemsanityItems[f"{level.Name} 50 Gems"]
                if f"{level.Name} Gem Bundle" in gemsanityItems.keys():
                    newCurrentGems += gem_bundle_size * gemsanityItems[f"{level.Name} Gem Bundle"]
                if newCurrentGems != current_gems:
                    gemItems += [(RAM.LevelGemsAddress + 4 * level_index, newCurrentGems.to_bytes(4, "little"), "MainRAM")]
                newTotalGems += newCurrentGems
            level_index += 1
        self.currentGems = newTotalGems
        if newTotalGems != totalGems:
            gemItems += [(RAM.TotalGemAddress, newTotalGems.to_bytes(4, "little"), "MainRAM")]
        return gemItems

    def handleGemsanity(self, gemsanity_reads):
        localGemIncrement = gemsanity_reads[0]
        globalGemIncrement = gemsanity_reads[1]
        globalGemRespawnFix = gemsanity_reads[2]
        localGemRespawnFix = gemsanity_reads[3]
        playBeep = gemsanity_reads[4]
        gemsanity_writes = []

        # Disable updating local and global gem counts on collecting a gem, loading into a level, and respawning.
        if localGemIncrement != 0:
            gemsanity_writes += [(RAM.localGemIncrementAddress, (0).to_bytes(4, "little"), "MainRAM")]
        if globalGemIncrement != 0:
            gemsanity_writes += [(RAM.globalGemIncrementAddress, (0).to_bytes(4, "little"), "MainRAM")]
        if globalGemRespawnFix != 0:
            gemsanity_writes += [(RAM.globalGemRespawnFixAddress, (0).to_bytes(4, "little"), "MainRAM")]
        if localGemRespawnFix != 0:
            gemsanity_writes += [(RAM.localGemRespawnFixAddress, (0).to_bytes(4, "little"), "MainRAM")]
        if playBeep != 0:
            gemsanity_writes += [(RAM.playBeepAddress, (0).to_bytes(4, "little"), "MainRAM")]

        return gemsanity_writes

    def handleMoneybags(self, ctx, moneybagsUnlocks, moneybagsFlags):
        moneybags_writes = []
        moneybagsFlagArr = moneybagsFlags.to_bytes(0x4c, "little")
        # Glimmer bridge is always free.
        if int.from_bytes(moneybagsFlagArr[RAM.GlimmerBridgeUnlock : RAM.GlimmerBridgeUnlock + 2], "little") != 0:
            moneybags_writes += [(RAM.MoneybagsUnlocks + RAM.GlimmerBridgeUnlock, (0).to_bytes(2, "little"), "MainRAM")]

        moneybags_dict = {
            "Moneybags Unlock - Crystal Glacier Bridge": RAM.CrystalBridgeUnlock,
            "Moneybags Unlock - Aquaria Towers Submarine": RAM.AquariaSubUnlock,
            "Moneybags Unlock - Magma Cone Elevator": RAM.MagmaElevatorUnlock,
            "Moneybags Unlock - Swim": RAM.SwimUnlock,
            "Moneybags Unlock - Climb": RAM.ClimbUnlock,
            "Moneybags Unlock - Headbash": RAM.HeadbashUnlock,
            "Moneybags Unlock - Wall by Aquaria Towers": RAM.WallToAquariaUnlock, # Name changed in 2.0.0.
            "Moneybags Unlock - Zephyr Portal": RAM.ZephyrPortalUnlock,
            "Moneybags Unlock - Shady Oasis Portal": RAM.ShadyPortalUnlock,
            "Moneybags Unlock - Icy Speedway Portal": RAM.IcyPortalUnlock,
            "Moneybags Unlock - Canyon Speedway Portal": RAM.CanyonPortalUnlock,
        }
        if ctx.slot_data["options"]["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY:
            for unlock in moneybags_dict.keys():
                unlock_address = moneybags_dict[unlock]
                if self.riptoDefeated or unlock in moneybagsUnlocks:
                    if int.from_bytes(moneybagsFlagArr[unlock_address : unlock_address + 4], "little") != 65536:
                        moneybags_writes += [(RAM.MoneybagsUnlocks + unlock_address, (65536).to_bytes(4, "little"), "MainRAM")]
                else:
                    if int.from_bytes(moneybagsFlagArr[unlock_address : unlock_address + 4], "little") != 20001:
                        moneybags_writes += [(RAM.MoneybagsUnlocks + unlock_address, (20001).to_bytes(4, "little"), "MainRAM")]
        elif ctx.slot_data["options"]["moneybags_settings"] == MoneybagsOptions.VANILLA and \
            (
                ctx.slot_data["options"]["enable_gemsanity"] != GemsanityOptions.OFF or
                ctx.slot_data["options"]["level_lock_options"] != LevelLockOptions.VANILLA
            ):
            for unlock in moneybags_dict.keys():
                unlock_address = moneybags_dict[unlock]
                if int.from_bytes(moneybagsFlagArr[unlock_address: unlock_address + 2], "little") != 0:
                    moneybags_writes += [(RAM.MoneybagsUnlocks + unlock_address, (0).to_bytes(2, "little"), "MainRAM")]
        elif ctx.slot_data["options"]["moneybags_settings"] == MoneybagsOptions.VANILLA and \
            ctx.slot_data["options"]["start_with_abilities"]:
            for unlock in moneybags_dict.keys():
                if not (unlock.endswith("Swim") or unlock.endswith("Climb") or unlock.endswith("Headbash")):
                    continue
                unlock_address = moneybags_dict[unlock]
                if int.from_bytes(moneybagsFlagArr[unlock_address: unlock_address + 4], "little") != 65536:
                    moneybags_writes += [(RAM.MoneybagsUnlocks + unlock_address, (65536).to_bytes(4, "little"), "MainRAM")]
        return moneybags_writes

    def handleAbilities(self, ctx, abilityReads):
        doubleJumpLine1 = abilityReads[0]
        doubleJumpLine2 = abilityReads[1]
        permanentFireball = abilityReads[2]
        ability_writes = []
        doubleJumpOption = ctx.slot_data["options"]["double_jump_ability"]
        fireballOption = ctx.slot_data["options"]["permanent_fireball_ability"]

        if doubleJumpOption == AbilityOptions.OFF or doubleJumpOption == AbilityOptions.IN_POOL and not self.hasDoubleJumpItem:
            if doubleJumpLine1 != 0x2402FE00:
                ability_writes += [(RAM.DoubleJumpAddress1, (0x2402FE00).to_bytes(4, "little"), "MainRAM")]
            if doubleJumpLine2 != 0xAC22A08C:
                ability_writes += [(RAM.DoubleJumpAddress2, (0xAC22A08C).to_bytes(4, "little"), "MainRAM")]
        else:
            if doubleJumpLine1 != 0x24020800:
                ability_writes += [(RAM.DoubleJumpAddress1, (0x24020800).to_bytes(4, "little"), "MainRAM")]
            if doubleJumpLine2 != 0xAC22A0A8:
                ability_writes += [(RAM.DoubleJumpAddress2, (0xAC22A0A8).to_bytes(4, "little"), "MainRAM")]

        if fireballOption == AbilityOptions.OFF or fireballOption == AbilityOptions.IN_POOL and not self.hasFireballItem:
            if permanentFireball != 0:
                ability_writes += [(RAM.PermanentFireballAddress, (0).to_bytes(1, "little"), "MainRAM")]
        elif fireballOption == AbilityOptions.START_WITH or fireballOption == AbilityOptions.IN_POOL and self.hasFireballItem:
            if permanentFireball != 1:
                ability_writes += [(RAM.PermanentFireballAddress, (1).to_bytes(1, "little"), "MainRAM")]
        # Else case is vanilla behavior, controlled by the game
        return ability_writes

    def handleEasyChallenge(self, ctx, easyChallengeReads):
        currentLevel = easyChallengeReads[0]
        colossusHockeyScore = easyChallengeReads[1]
        idolFishThrowUp = easyChallengeReads[2]
        idolFishIncludeReds = easyChallengeReads[3]
        idolFishIncludeRedsHUD = easyChallengeReads[4]
        hurricosLightningThiefAddresses = easyChallengeReads[5].to_bytes(0x18CFC0 - 0x18C8A8, "little")
        spyroHUDScore = easyChallengeReads[6]
        secondBomboStatus = easyChallengeReads[7]
        secondBomboZPos = easyChallengeReads[8]
        thirdBomboStatus = easyChallengeReads[9]
        thirdBomboZPos = easyChallengeReads[10]
        bomboAttackAddress = easyChallengeReads[11]
        fractureHeadbashCheck = easyChallengeReads[12]
        fractureEarthshaperAddresses = easyChallengeReads[13].to_bytes(0x189000 - 0x188DB8, "little")
        maxFractureSpiritParticles = easyChallengeReads[14]
        opponentHUDScore = easyChallengeReads[15]
        shadyHeadbashCheck = easyChallengeReads[16]
        gulpDoubleDamage = easyChallengeReads[17]

        easyChallengeWrites = []

        if currentLevel == LevelInGameIDs.Colossus:
            starting_goals = ctx.slot_data["options"]["colossus_starting_goals"]
            if colossusHockeyScore < starting_goals:
                easyChallengeWrites += [
                    (RAM.ColossusSpyroHockeyScore, starting_goals.to_bytes(1, "little"), "MainRAM"),
                    (RAM.spyroHUDScore, starting_goals.to_bytes(1, "little"), "MainRAM")
                ]
        elif currentLevel == LevelInGameIDs.IdolSprings:
            easy_fish = ctx.slot_data["options"]["idol_easy_fish"]
            if easy_fish:
                if idolFishThrowUp != 0x0802080c:
                    easyChallengeWrites += [(RAM.IdolFishThrowUp, (0x0802080c).to_bytes(4, "little"), "MainRAM")]
                if idolFishIncludeReds != 0x28820006:
                    easyChallengeWrites += [(RAM.IdolFishIncludeReds, (0x28820006).to_bytes(4, "little"), "MainRAM")]
                if idolFishIncludeRedsHUD != 0x28a20006:
                    easyChallengeWrites += [(RAM.IdolFishIncludeRedsHUD, (0x28a20006).to_bytes(4, "little"), "MainRAM")]
        elif currentLevel == LevelInGameIDs.Hurricos:
            easyLightningOrbs = ctx.slot_data["options"]["hurricos_easy_lightning_orbs"]
            if easyLightningOrbs:
                for thiefStatus in RAM.HurricosLightningThiefStatuses:
                    if hurricosLightningThiefAddresses[thiefStatus] != 253:
                        easyChallengeWrites += [(RAM.HurricosLightningThiefAddresses + thiefStatus, (253).to_bytes(1, "little"), "MainRAM")]
                for thiefZCoordinate in RAM.HurricosLightningThiefZCoordinates:
                    if int.from_bytes(hurricosLightningThiefAddresses[thiefZCoordinate:thiefZCoordinate+4]) != 0:
                        easyChallengeWrites += [(RAM.HurricosLightningThiefAddresses + thiefZCoordinate, (0).to_bytes(4, "little"), "MainRAM")]
        elif currentLevel == LevelInGameIDs.BreezeHarbor:
            requiredGears = ctx.slot_data["options"]["breeze_required_gears"]
            if spyroHUDScore > 50:
                easyChallengeWrites += [(RAM.spyroHUDScore, (50).to_bytes(1, "little"), "MainRAM")]
            elif spyroHUDScore < 50 - requiredGears:
                easyChallengeWrites += [(RAM.spyroHUDScore, (50 - requiredGears).to_bytes(1, "little"), "MainRAM")]
        elif currentLevel == LevelInGameIDs.Scorch:
            # Nothing ever goes wrong in Scorch : )
            bomboSettings = ctx.slot_data["options"]["scorch_bombo_settings"]
            if bomboSettings == BomboOptions.FIRST_ONLY:
                # Mark the other two Bombos as complete, and move their models out of rendering range.
                # Otherwise, their models appear on the flagpoles.
                # -0x35 is the offset from status to z coordinate
                if secondBomboStatus != 11:
                    easyChallengeWrites += [(RAM.secondBomboStatus, (11).to_bytes(1, "little"), "MainRAM")]
                if secondBomboZPos != 100000:
                    easyChallengeWrites += [(RAM.secondBomboStatus - 0x35, (100000).to_bytes(4, "little"), "MainRAM")]
                if thirdBomboStatus != 11:
                    easyChallengeWrites += [(RAM.thirdBomboStatus, (11).to_bytes(1, "little"), "MainRAM")]
                if thirdBomboZPos != 100000:
                    easyChallengeWrites += [(RAM.thirdBomboStatus - 0x35, (100000).to_bytes(4, "little"), "MainRAM")]
            elif bomboSettings == BomboOptions.FIRST_ONLY_NO_ATTACK:
                if secondBomboStatus != 11:
                    easyChallengeWrites += [(RAM.secondBomboStatus, (11).to_bytes(1, "little"), "MainRAM")]
                if secondBomboZPos != 100000:
                    easyChallengeWrites += [(RAM.secondBomboStatus - 0x35, (100000).to_bytes(4, "little"), "MainRAM")]
                if thirdBomboStatus != 11:
                    easyChallengeWrites += [(RAM.thirdBomboStatus, (11).to_bytes(1, "little"), "MainRAM")]
                if thirdBomboZPos != 100000:
                    easyChallengeWrites += [(RAM.thirdBomboStatus - 0x35, (100000).to_bytes(4, "little"), "MainRAM")]
                if bomboAttackAddress != 0x0801E71E:
                    easyChallengeWrites += [(RAM.bomboAttackAddress, (0x0801E71E).to_bytes(4, "little"), "MainRAM")]
        elif currentLevel == LevelInGameIDs.FractureHills:
            requireHeadbash = ctx.slot_data["options"]["fracture_require_headbash"]
            easyEarthshapers = ctx.slot_data["options"]["fracture_easy_earthshapers"]
            if not requireHeadbash and fractureHeadbashCheck != 0x0801E2A5:
                easyChallengeWrites += [(RAM.fractureHeadbashCheck, (0x0801E2A5).to_bytes(4, "little"), "MainRAM")]
            if easyEarthshapers:
                for earthshaperStatus in RAM.FractureEarthshaperStatuses:
                    if fractureEarthshaperAddresses[earthshaperStatus] != 253:
                        easyChallengeWrites += [(RAM.FractureEarthshaperAddresses + earthshaperStatus, (253).to_bytes(1, "little"), "MainRAM")]
                for earthshaperZCoordinate in RAM.FractureEarthshaperZCoordinates:
                        if int.from_bytes(fractureEarthshaperAddresses[earthshaperZCoordinate:earthshaperZCoordinate + 4]) != 0:
                            easyChallengeWrites += [(RAM.FractureEarthshaperAddresses + earthshaperZCoordinate, (0).to_bytes(4, "little"), "MainRAM")]
                if maxFractureSpiritParticles != 22:
                    easyChallengeWrites += [(RAM.maxFractureSpiritParticles, (22).to_bytes(1, "little"), "MainRAM")]
        elif currentLevel == LevelInGameIDs.MagmaCone:
            spyroStartingScore = ctx.slot_data["options"]["magma_spyro_starting_popcorn"]
            hunterStartingScore = ctx.slot_data["options"]["magma_hunter_starting_popcorn"]
            if spyroHUDScore < spyroStartingScore:
                easyChallengeWrites += [(RAM.spyroHUDScore, spyroStartingScore.to_bytes(1, "little"), "MainRAM")]
            if opponentHUDScore < hunterStartingScore:
                easyChallengeWrites += [(RAM.opponentHUDScore, hunterStartingScore.to_bytes(1, "little"), "MainRAM")]
        elif currentLevel == LevelInGameIDs.ShadyOasis:
            requireHeadbash = ctx.slot_data["options"]["shady_require_headbash"]
            if not requireHeadbash and shadyHeadbashCheck != 0x00000000:
                easyChallengeWrites += [(RAM.ShadyHeadbashCheck, (0).to_bytes(4, "little"), "MainRAM")]
        elif currentLevel == LevelInGameIDs.GulpsOverlook:
            easyGulp = ctx.slot_data["options"]["easy_gulp"]
            if easyGulp and gulpDoubleDamage != 1:
                easyChallengeWrites += [(RAM.GulpDoubleDamage, (1).to_bytes(1, "little"), "MainRAM")]
        return easyChallengeWrites

    def handleColorChanges(self, ctx, colorChangeReads):
        redGemShadow = colorChangeReads[0]
        redGemColor = colorChangeReads[1]
        greenGemShadow = colorChangeReads[2]
        greenGemColor = colorChangeReads[3]
        blueGemShadow = colorChangeReads[4]
        blueGemColor = colorChangeReads[5]
        goldGemShadow = colorChangeReads[6]
        goldGemColor = colorChangeReads[7]
        pinkGemShadow = colorChangeReads[8]
        pinkGemColor = colorChangeReads[9]
        portalTextRed = colorChangeReads[10]
        portalTextGreen = colorChangeReads[11]
        portalTextBlue = colorChangeReads[12]

        colorChangeWrites = []

        red_gem_shadow_color = ctx.slot_data["options"]["red_gem_shadow_color"]
        red_gem_color = ctx.slot_data["options"]["red_gem_color"]
        green_gem_shadow_color = ctx.slot_data["options"]["green_gem_shadow_color"]
        green_gem_color = ctx.slot_data["options"]["green_gem_color"]
        blue_gem_shadow_color = ctx.slot_data["options"]["blue_gem_shadow_color"]
        blue_gem_color = ctx.slot_data["options"]["blue_gem_color"]
        gold_gem_shadow_color = ctx.slot_data["options"]["gold_gem_shadow_color"]
        gold_gem_color = ctx.slot_data["options"]["gold_gem_color"]
        pink_gem_shadow_color = ctx.slot_data["options"]["pink_gem_shadow_color"]
        pink_gem_color = ctx.slot_data["options"]["pink_gem_color"]
        portal_gem_collection_color = ctx.slot_data["options"]["portal_gem_collection_color"]

        if redGemShadow != red_gem_shadow_color:
            colorChangeWrites += [(RAM.RedGemShadow, red_gem_shadow_color.to_bytes(4, "little"), "MainRAM")]
        if redGemColor != red_gem_color:
            colorChangeWrites += [(RAM.RedGemColor, red_gem_color.to_bytes(4, "little"), "MainRAM")]
        if greenGemShadow != green_gem_shadow_color:
            colorChangeWrites += [(RAM.GreenGemShadow, green_gem_shadow_color.to_bytes(4, "little"), "MainRAM")]
        if greenGemColor != green_gem_color:
            colorChangeWrites += [(RAM.GreenGemColor, green_gem_color.to_bytes(4, "little"), "MainRAM")]
        if blueGemShadow != blue_gem_shadow_color:
            colorChangeWrites += [(RAM.BlueGemShadow, blue_gem_shadow_color.to_bytes(4, "little"), "MainRAM")]
        if blueGemColor != blue_gem_color:
            colorChangeWrites += [(RAM.BlueGemColor, blue_gem_color.to_bytes(4, "little"), "MainRAM")]
        if goldGemShadow != gold_gem_shadow_color:
            colorChangeWrites += [(RAM.GoldGemShadow, gold_gem_shadow_color.to_bytes(4, "little"), "MainRAM")]
        if goldGemColor != gold_gem_color:
            colorChangeWrites += [(RAM.GoldGemColor, gold_gem_color.to_bytes(4, "little"), "MainRAM")]
        if pinkGemShadow != pink_gem_shadow_color:
            colorChangeWrites += [(RAM.PinkGemShadow, pink_gem_shadow_color.to_bytes(4, "little"), "MainRAM")]
        if pinkGemColor != pink_gem_color:
            colorChangeWrites += [(RAM.PinkGemColor, pink_gem_color.to_bytes(4, "little"), "MainRAM")]

        if portal_gem_collection_color == PortalTextColorOptions.RED:
            if portalTextRed != 128:
                colorChangeWrites += [(RAM.PortalTextRed, (128).to_bytes(1, "little"), "MainRAM")]
            if portalTextGreen != 0:
                colorChangeWrites += [(RAM.PortalTextGreen, (0).to_bytes(1, "little"), "MainRAM")]
            if portalTextBlue != 0:
                colorChangeWrites += [(RAM.PortalTextBlue, (0).to_bytes(1, "little"), "MainRAM")]
        elif portal_gem_collection_color == PortalTextColorOptions.GREEN:
            if portalTextRed != 0:
                colorChangeWrites += [(RAM.PortalTextRed, (0).to_bytes(1, "little"), "MainRAM")]
            if portalTextGreen != 128:
                colorChangeWrites += [(RAM.PortalTextGreen, (128).to_bytes(1, "little"), "MainRAM")]
            if portalTextBlue != 0:
                colorChangeWrites += [(RAM.PortalTextBlue, (0).to_bytes(1, "little"), "MainRAM")]
        elif portal_gem_collection_color == PortalTextColorOptions.BLUE:
            if portalTextRed != 0:
                colorChangeWrites += [(RAM.PortalTextRed, (0).to_bytes(1, "little"), "MainRAM")]
            if portalTextGreen != 0:
                colorChangeWrites += [(RAM.PortalTextGreen, (0).to_bytes(1, "little"), "MainRAM")]
            if portalTextBlue != 128:
                colorChangeWrites += [(RAM.PortalTextBlue, (128).to_bytes(1, "little"), "MainRAM")]
        elif portal_gem_collection_color == PortalTextColorOptions.PINK:
            if portalTextRed != 64:
                colorChangeWrites += [(RAM.PortalTextRed, (64).to_bytes(1, "little"), "MainRAM")]
            if portalTextGreen != 0:
                colorChangeWrites += [(RAM.PortalTextGreen, (0).to_bytes(1, "little"), "MainRAM")]
            if portalTextBlue != 64:
                colorChangeWrites += [(RAM.PortalTextBlue, (64).to_bytes(1, "little"), "MainRAM")]
        elif portal_gem_collection_color == PortalTextColorOptions.WHITE:
            if portalTextRed != 128:
                colorChangeWrites += [(RAM.PortalTextRed, (128).to_bytes(1, "little"), "MainRAM")]
            if portalTextGreen != 128:
                colorChangeWrites += [(RAM.PortalTextGreen, (128).to_bytes(1, "little"), "MainRAM")]
            if portalTextBlue != 128:
                colorChangeWrites += [(RAM.PortalTextBlue, (128).to_bytes(1, "little"), "MainRAM")]
        else:
            if portalTextRed != 64:
                colorChangeWrites += [(RAM.PortalTextRed, (64).to_bytes(1, "little"), "MainRAM")]
            if portalTextGreen != 64:
                colorChangeWrites += [(RAM.PortalTextGreen, (64).to_bytes(1, "little"), "MainRAM")]
            if portalTextBlue != 0:
                colorChangeWrites += [(RAM.PortalTextBlue, (0).to_bytes(1, "little"), "MainRAM")]
        return colorChangeWrites

    def handleEloraDoorChanges(self, ctx, eloraDoorReads):
        currentLevel = eloraDoorReads[0]
        riptoDoorOrbRequirement = eloraDoorReads[1]
        riptoDoorOrbDisplay = eloraDoorReads[2]

        eloraDoorWrites = []

        if currentLevel == LevelInGameIDs.WinterTundra:
            requiredOrbs = ctx.slot_data["options"]["ripto_door_orbs"]
            if riptoDoorOrbRequirement != requiredOrbs:
                eloraDoorWrites += [(RAM.RiptoDoorOrbRequirementAddress, requiredOrbs.to_bytes(1, "little"), "MainRAM")]
            if riptoDoorOrbDisplay != requiredOrbs:
                eloraDoorWrites += [(RAM.RiptoDoorOrbDisplayAddress, requiredOrbs.to_bytes(1, "little"), "MainRAM")]
        # TODO: Handle text in Summer Forest and Autumn Plains
        # // Handle Elora in Summer Forest and the door to Crush by special casing talisman count in this level only.
        # // Note that Elora won't open the door if your count is more than 6.
        # if (currentLevel == (byte)LevelInGameIDs.SummerForest)
        # {
        #     Memory.WriteByte(Addresses.TotalTalismanAddress, (byte)summerCount);
        #     WriteStringToMemory(Addresses.SummerEloraStartText, Addresses.SummerEloraEndText, $"Hi, Spyro! You have @4{summerCount}@0 Summer Forest Talismans.");
        #     WriteStringToMemory(Addresses.SummerEloraWarpStartText, Addresses.SummerEloraWarpEndText, $"Hi, Spyro! You have @4{summerCount}@0 Summer Forest Talismans.");
        # }
        # else if (currentLevel == (byte)LevelInGameIDs.AutumnPlains)
        # {
        #     Memory.WriteByte(Addresses.TotalTalismanAddress, (byte)(summerCount + autumnCount));
        #     WriteStringToMemory(Addresses.AutumnEloraStartText, Addresses.AutumnEloraEndText, $"Hi, Spyro! You have @4{summerCount + autumnCount }@0 Talismans.");
        #     WriteStringToMemory(Addresses.AutumnEloraWarpStartText, Addresses.AutumnEloraWarpEndText, $"Hi, Spyro! You have @4{summerCount + autumnCount}@0 Talismans.");
        # }
        return eloraDoorWrites

    def handleOpenWorldChanges(self, ctx, openWorldReads):
        crushGuidebookUnlock = openWorldReads[0]
        gulpGuidebookUnlock = openWorldReads[1]
        autumnGuidebookUnlock = openWorldReads[2]
        winterGuidebookUnlock = openWorldReads[3]

        openWorldOption = ctx.slot_data["options"]["enable_open_world"]
        openWorldWarpUnlocks = ctx.slot_data["options"]["open_world_warp_unlocks"]

        openWorldWrites = []

        if openWorldOption:
            if crushGuidebookUnlock != 1:
                openWorldWrites += [(RAM.CrushGuidebookUnlock, (1).to_bytes(1, "little"), "MainRAM")]
            if gulpGuidebookUnlock != 1:
                openWorldWrites += [(RAM.GulpGuidebookUnlock, (1).to_bytes(1, "little"), "MainRAM")]
            if openWorldWarpUnlocks:
                if autumnGuidebookUnlock != 1:
                    openWorldWrites += [(RAM.AutumnGuidebookUnlock, (1).to_bytes(1, "little"), "MainRAM")]
                if winterGuidebookUnlock != 1:
                    openWorldWrites += [(RAM.WinterGuidebookUnlock, (1).to_bytes(1, "little"), "MainRAM")]
        return openWorldWrites

    def handleLevelLockChanges(self, ctx, levelLockReads):
        currentLevel = levelLockReads[0]
        levelLockOptions = ctx.slot_data["options"]["level_lock_options"]
        levelLockWrites = []
        if levelLockOptions == LevelLockOptions.KEYS:
            levelNames = {
                ("Idol Springs", RAM.IdolNameAddress, 16),
                ("Colossus", RAM.ColossusNameAddress, 12),
                ("Hurricos", RAM.HurricosNameAddress, 12),
                ("Aquaria Towers", RAM.AquariaNameAddress, 16),
                ("Sunny Beach", RAM.SunnyNameAddress, 12),
                ("Ocean Speedway", RAM.OceanNameAddress, 16),
                ("Skelos Badlands", RAM.SkelosNameAddress, 16),
                ("Crystal Glacier", RAM.CrystalNameAddress, 16),
                ("Breeze Harbor", RAM.BreezeNameAddress, 16),
                ("Zephyr", RAM.ZephyrNameAddress, 8),
                ("Metro Speedway", RAM.MetroNameAddress, 16),
                ("Scorch", RAM.ScorchNameAddress, 8),
                ("Shady Oasis", RAM.ShadyNameAddress, 12),
                ("Magma Cone", RAM.MagmaNameAddress, 12),
                ("Fracture Hills", RAM.FractureNameAddress, 16),
                ("Icy Speedway", RAM.IcyNameAddress, 16),
                ("Mystic Marsh", RAM.MysticNameAddress, 16),
                ("Cloud Temples", RAM.CloudNameAddress, 16),
                ("Canyon Speedway", RAM.CanyonNameAddress, 16),
                ("Robotica Farms", RAM.RoboticaNameAddress, 16),
                ("Metropolis", RAM.MetropolisNameAddress, 12),
                ("Dragon Shores", RAM.ShoresNameAddress, 16),
           }
            for level in levelNames:
                levelName = level[0]
                levelNameAddress = level[1]
                levelNameLength = level[2]
                if f"{levelName} Unlock" in self.unlockedLevels:
                    writtenName = text_to_bytes(levelName, levelNameLength)
                else:
                    writtenName = text_to_bytes("LOCKED", levelNameLength)
                # TODO: Write only when value doesn't match
                for x in range(levelNameLength):
                    levelLockWrites += [(levelNameAddress + x, writtenName[x].to_bytes(1, "little"), "MainRAM")]

            if currentLevel == LevelInGameIDs.SummerForest:
                summerUnlocks = [
                    "Idol Springs Unlock" in self.unlockedLevels,
                    "Colossus Unlock" in self.unlockedLevels,
                    "Hurricos Unlock" in self.unlockedLevels,
                    "Aquaria Towers Unlock" in self.unlockedLevels,
                    "Sunny Beach Unlock" in self.unlockedLevels,
                    "Ocean Speedway Unlock" in self.unlockedLevels,
                ]
                # Glimmer is always unlocked.
                # TODO: Write only when value doesn't match
                portalAddress = RAM.SummerPortalBlock + 8
                for isLevelUnlocked in summerUnlocks:
                    if isLevelUnlocked:
                        levelLockWrites += [(portalAddress, (6).to_bytes(4, "little"), "MainRAM")]
                    else:
                        levelLockWrites += [(portalAddress, (0).to_bytes(4, "little"), "MainRAM")]
                    portalAddress += 8
            elif currentLevel == LevelInGameIDs.AutumnPlains:
                autumnUnlocks = [
                    "Skelos Badlands Unlock" in self.unlockedLevels,
                    "Crystal Glacier Unlock" in self.unlockedLevels,
                    "Breeze Harbor Unlock" in self.unlockedLevels,
                    "Zephyr Unlock" in self.unlockedLevels,
                    "Metro Speedway Unlock" in self.unlockedLevels,
                    "Scorch Unlock" in self.unlockedLevels,
                    "Shady Oasis Unlock" in self.unlockedLevels,
                    "Magma Cone Unlock" in self.unlockedLevels,
                    "Fracture Hills Unlock" in self.unlockedLevels,
                    "Icy Speedway Unlock" in self.unlockedLevels,
                ]
                # TODO: Write only when value doesn't match
                portalAddress = RAM.AutumnPortalBlock
                for isLevelUnlocked in autumnUnlocks:
                    if isLevelUnlocked:
                        levelLockWrites += [(portalAddress, (6).to_bytes(4, "little"), "MainRAM")]
                    else:
                        levelLockWrites += [(portalAddress, (0).to_bytes(4, "little"), "MainRAM")]
                    portalAddress += 8
            elif currentLevel == LevelInGameIDs.WinterTundra:
                winterUnlocks = [
                    "Mystic Marsh Unlock" in self.unlockedLevels,
                    "Cloud Temples Unlock" in self.unlockedLevels,
                    "Robotica Farms Unlock" in self.unlockedLevels,
                    "Metropolis Unlock" in self.unlockedLevels,
                    "Canyon Speedway Unlock" in self.unlockedLevels,
                    "Dragon Shores Unlock" in self.unlockedLevels,
                ]
                # TODO: Write only when value doesn't match
                portalAddress = RAM.WinterPortalBlock
                for isLevelUnlocked in winterUnlocks:
                    if isLevelUnlocked:
                        levelLockWrites += [(portalAddress, (6).to_bytes(4, "little"), "MainRAM")]
                    else:
                        levelLockWrites += [(portalAddress, (0).to_bytes(4, "little"), "MainRAM")]
                    portalAddress += 8
        return levelLockWrites

    def handleWinterWarpChanges(self, ctx, wtWarpReads):
        wtWarpReroute = wtWarpReads[0]
        wtDoorGem = wtWarpReads[1]
        wtWallOrb = wtWarpReads[2]
        warpOption = ctx.slot_data["options"]["wt_warp_options"]

        wtWarpWrites = []

        rerouteWarp = 0
        if warpOption == WTWarpOptions.DOOR:
            gemBit = pow(2, RAM.WTDoorGemBit)
            if wtDoorGem & gemBit != 0:
                rerouteWarp = 1
        if warpOption == WTWarpOptions.WALL_ORB:
            orbBit = pow(2, RAM.WTWallOrbBit)
            if wtWallOrb & orbBit != 0:
                rerouteWarp = 1
        if wtWarpReroute != rerouteWarp:
            wtWarpWrites += [(RAM.WTWarpAddress, (rerouteWarp).to_bytes(2, "little"), "MainRAM")]

        return wtWarpWrites

    def handleInvisibilityChanges(self, invisibilityReads):
        invisibleAddress1 = invisibilityReads[0]
        invisibleAddress2 = invisibilityReads[1]

        invisibilityWrites = []

        if not self.isInvisible:
            if invisibleAddress1 != 0:
                invisibilityWrites += [(RAM.InvisibleAddress1, (0).to_bytes(2, "little"), "MainRAM")]
            if invisibleAddress2 != 0:
                invisibilityWrites += [(RAM.InvisibleAddress2, (0).to_bytes(2, "little"), "MainRAM")]
        elif self.invisibilityEnd < time.time():
            self.isInvisible = False
            if invisibleAddress1 != 0:
                invisibilityWrites += [(RAM.InvisibleAddress1, (0).to_bytes(2, "little"), "MainRAM")]
            if invisibleAddress2 != 0:
                invisibilityWrites += [(RAM.InvisibleAddress2, (0).to_bytes(2, "little"), "MainRAM")]
        else:
            if invisibleAddress1 != 1:
                invisibilityWrites += [(RAM.InvisibleAddress1, (1).to_bytes(2, "little"), "MainRAM")]
            if invisibleAddress2 != 0x3402:
                invisibilityWrites += [(RAM.InvisibleAddress2, (0x3402).to_bytes(2, "little"), "MainRAM")]

        return invisibilityWrites

    def handleDestructiveChanges(self, destructiveReads):
        destructiveAddress = destructiveReads[0]

        destructiveWrites = []

        if self.isDestructive and self.destructiveEnd < time.time():
            self.isDestructive = False
            logger.info("Destructive mode has ended.")
            # Turns off on its own.
        elif self.isDestructive:
            if destructiveAddress != 0xFF:
                # TODO: This is buggy.
                # Probably need to temporarily overwrite changes to this halfword elsewhere too.
                destructiveWrites += [(RAM.DestructiveSpyroAddress, (0xFF).to_bytes(2, "little"), "MainRAM")]

        return destructiveWrites

    def handleSparxChanges(self, sparxReads):
        sparxHealth = sparxReads[0]
        currentTimestamp = time.time()

        sparxWrites = []
        i = 0
        while i < len(self.healthItemQueue):
            sparxHealthItems = self.healthItemQueue[i]
            if sparxHealthItems[0] + 3 <= currentTimestamp:
                for item in sparxHealthItems[1]:
                    if item == "Damage Sparx Trap":
                        if 0 < sparxHealth < 128:
                            sparxHealth -= 1
                    elif item == "Sparxless Trap":
                        if 0 < sparxHealth < 128:
                            sparxHealth = 0
                    elif item == "Heal Sparx":
                        if 0 <= sparxHealth < self.maxHealth:
                            sparxHealth += 1
                self.healthItemQueue.pop(i)
            else:
                i = i + 1
        if 128 > sparxHealth > self.maxHealth:
            sparxHealth = self.maxHealth

        if sparxHealth != sparxReads[0]:
            sparxWrites += [(RAM.PlayerHealth, sparxHealth.to_bytes(1, "little"), "MainRAM")]

        return sparxWrites

    async def update_tags(self, ctx: "BizHawkClientContext") -> None:
        updateTags = False
        if ctx.slot_data["options"]["death_link"] or self.deathlink == 1:
            if "DeathLink" not in ctx.tags:
                ctx.tags.add("DeathLink")
                updateTags = True
        else:
            if "DeathLink" in ctx.tags:
                ctx.tags.remove("DeathLink")
                updateTags = True
        if updateTags:
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

    async def handle_death_link(self, ctx: "BizHawkClientContext", DL_Reads) -> None:
        """
        Checks whether the player has died while connected and sends a death link if so.
        """
        deathLinkLevels = [
            LevelInGameIDs.SummerForest,
            LevelInGameIDs.Glimmer,
            LevelInGameIDs.Colossus,
            LevelInGameIDs.IdolSprings,
            LevelInGameIDs.Hurricos,
            LevelInGameIDs.SunnyBeach,
            LevelInGameIDs.AquariaTowers,
            LevelInGameIDs.CrushsDungeon,
            LevelInGameIDs.AutumnPlains,
            LevelInGameIDs.BreezeHarbor,
            LevelInGameIDs.SkelosBadlands,
            LevelInGameIDs.CrystalGlacier,
            LevelInGameIDs.Zephyr,
            LevelInGameIDs.Scorch,
            LevelInGameIDs.FractureHills,
            LevelInGameIDs.MagmaCone,
            LevelInGameIDs.ShadyOasis,
            LevelInGameIDs.GulpsOverlook,
            LevelInGameIDs.WinterTundra,
            LevelInGameIDs.MysticMarsh,
            LevelInGameIDs.CloudTemples,
            LevelInGameIDs.RoboticaFarms,
            LevelInGameIDs.Metropolis,
            LevelInGameIDs.RiptosArena
        ]

        currentLevel = DL_Reads[0]
        health = DL_Reads[1]
        gameState = DL_Reads[2]
        zPos = DL_Reads[3]
        animationLength = DL_Reads[4]
        velocityFlag = DL_Reads[5]
        spyroState = DL_Reads[6]

        DL_writes = []
        if self.deathlink == 1:
            if "DeathLink" not in ctx.tags:
                self.previous_death_link = ctx.last_death_link
            if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
                if not self.sending_death_link and \
                        currentLevel in deathLinkLevels and \
                        gameState not in [GameStatus.Cutscene, GameStatus.Loading, GameStatus.TitleScreen]:
                    cause = None
                    if health > 128:
                        cause = "Damage"
                    elif 0 < zPos < 0x400: # zPos is 0 on initial load into a save.
                        cause = "Fell below death plane"
                    elif spyroState == SpyroStates.Flop and velocityFlag == 1 and 0x3b < animationLength:
                        cause = "Fell to death"
                    elif spyroState == SpyroStates.DeathBurn:
                        cause = "Burned"
                    elif spyroState == SpyroStates.DeathDrowning and animationLength >= 116:
                        cause = "Drowned"
                    elif spyroState == SpyroStates.DeathSquash:
                        cause = "Squashed"
                    if cause is not None:
                        await self.send_deathlink(ctx, cause)
                # Player has respawned.
                elif self.sending_death_link:
                    if health < 128 and zPos >= 0x400 and \
                            not (spyroState == SpyroStates.Flop and velocityFlag == 1 and 0x3b < animationLength) and \
                            spyroState != SpyroStates.DeathBurn and \
                            not (spyroState == SpyroStates.DeathDrowning and animationLength >= 116) and \
                            spyroState != SpyroStates.DeathSquash:
                        self.sending_death_link = False
            if self.pending_death_link:
                if currentLevel not in deathLinkLevels:
                    logger.info("Ignored the DeathLink to avoid softlock in current level.")
                    self.pending_death_link = False
                else:
                    DL_writes += [(RAM.SpyroStateAddress, SpyroStates.DeathPirouette.to_bytes(1, "little"), "MainRAM")]
                self.pending_death_link = False
                self.sending_death_link = True
                await bizhawk.write(ctx.bizhawk_ctx, DL_writes)
        elif self.deathlink == 0:
            self.previous_death_link = ctx.last_death_link

    async def send_deathlink(self, ctx: "BizHawkClientContext", cause) -> None:
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        if cause == "Unknown":
            DeathText = ctx.player_names[ctx.slot] + " died in Spyro 2."
        else:
            DeathText = ctx.player_names[ctx.slot] + f" died in Spyro 2: {cause}"
        await ctx.send_death(DeathText)

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    def showUnlockedLevels(self, ctx, showAll = False):
        levelLockOption = ctx.slot_data["options"]["level_lock_options"]
        if levelLockOption == LevelLockOptions.VANILLA:
            logger.info("Levels have their vanilla unlock requirements.")
        elif levelLockOption != LevelLockOptions.KEYS:
            # TODO: Revisit this message when orb locks are added.
            logger.info("Levels are not locked by keys.")
        else:
            if showAll or len(self.unlockedLevels) >= ctx.slot_data["options"]["level_unlocks"]:
                unlockedLevelsString = "You have unlocked:\n"
                for unlockedLevel in self.unlockedLevels:
                    newLevel = ""
                    if unlockedLevel == "Dragon Shores Unlock":
                        newLevel = "Shores"
                    else:
                        newLevel = unlockedLevel.split(" Unlock")[0].split(" ")[0]
                    if unlockedLevelsString == "You have unlocked:\n":
                        unlockedLevelsString = f"{unlockedLevelsString}{newLevel}"
                    else:
                        unlockedLevelsString = f"{unlockedLevelsString}; {newLevel}"
                if unlockedLevelsString == "You have unlocked:\n":
                    unlockedLevelsString = f"{unlockedLevelsString}No levels yet"
                logger.info(unlockedLevelsString)
#     }
# }

# Text helper functions
def text_to_bytes(name, string_len):
    bytelist = []
    for x in name:
        bytelist.append(ord(x))
    remaining_len = string_len - len(bytelist)
    for i in range(remaining_len):
        bytelist.append(0)
    return bytelist
