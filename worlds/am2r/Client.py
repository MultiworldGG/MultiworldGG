import asyncio
import json
import random
import datetime
import re
from asyncio import StreamReader, StreamWriter
from random import randint

from worlds import terraria
from worlds.am2r.items import item_table
from worlds.am2r.locations import get_location_datas

from Utils import async_start, init_logging, persistent_store, persistent_load
from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger, \
    get_base_parser

if __name__ == "__main__":
    init_logging("AM2RClient", exception_logger="Client")

CONNECTION_TIMING_OUT_STATUS = "Connection timing out"
CONNECTION_REFUSED_STATUS = "Connection Refused"
CONNECTION_RESET_STATUS = "Connection was reset"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"
item_location_scouts = {}
item_id_to_game_id: dict = {item.code: item.game_id for item in item_table.values()}
location_id_to_game_id: dict = {location.code: location.game_id for location in get_location_datas(None, None)}
game_id_to_location_id: dict = {location.game_id: location.code for location in get_location_datas(None, None) if location.code != None}
players = []
custom_messages = []
enable_enemy = True
enable_default = True
enable_ror2 = True
enable_terraria = True
enable_copypastas = True
enable_randplayer = True
enable_custom = True
AprilFoolsSurprise = False


def get_version():
    import os
    import json
    import zipfile
    from pathlib import Path
    from io import TextIOWrapper

    dirpath = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(dirpath, "archipelago.json")
    local_json = {}

    # Try to read the file directly first
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            local_json = json.load(f)
    except Exception:
        # If direct read fails, check if this module is inside a .apworld archive and try to open it as a zip
        try:
            p = Path(dirpath)
            parts = p.parts
            ap_index = next((i for i, part in enumerate(parts) if part.lower().endswith(".apworld")), None)
            if ap_index is not None:
                archive_path = Path(*parts[: ap_index + 1])
                internal_parts = parts[ap_index + 1 :]
                # candidate internal path using forward slashes
                candidate = "/".join((*internal_parts, "archipelago.json")) if internal_parts else "archipelago.json"
                try:
                    with zipfile.ZipFile(str(archive_path), "r") as z:
                        namelist = z.namelist()
                        target = candidate if candidate in namelist else next((n for n in namelist if n.lower().endswith("archipelago.json")), None)
                        if target:
                            with z.open(target) as bf:
                                with TextIOWrapper(bf, encoding="utf-8") as f:
                                    local_json = json.load(f)
                        else:
                            logger.warning(f"No archipelago.json found inside archive {archive_path} (checked {candidate})")
                except Exception as e:
                    logger.warning(f"Failed to read metadata from archive {archive_path}: {e}")
            else:
                logger.warning(f"Failed to read local metadata: file not found at {full_path}")
        except Exception as e:
            logger.warning(f"Failed to locate .apworld archive for local metadata: {e}")

    local_version = local_json.get("world_version") if local_json else None
    return local_version

def save_custom_messages_to_file():
    global custom_messages
    try:
        storage = load_custom_messages_from_file(True)
        if "custom_messages" in storage:
            custom_messages.extend(storage["Custom_Messages"])
            custom_messages = list(set(custom_messages))
    except Exception as e:
        logger.version(f"Error loading custom messages: {e}")
        pass

    persistent_store("Custom_Messages", "AM2R", custom_messages)

def overwrite_custom_messages():
    persistent_store("Custom_Messages", "AM2R", custom_messages)


def load_custom_messages_from_file(return_load: bool):
    global custom_messages
    if return_load:
        return persistent_load().get("Custom_Messages", {}).get("AM2R", {})
    else:
        custom_messages = persistent_load().get("Custom_Messages", {}).get("AM2R", {})


def extract_enemy_name(enemy) -> str:
    known_problems = {
        "TPO2": "TPO-2",
        "TPO": "TPO",
        "PincherFly": "Pincherfly",
        "SpikePlant": "Spike Plants",
        "A3": "Industrial Complex Mechanisms",
        "A2": "Hydro Station Mechanisms",
        "RoboMine": "Robomine",
        "BladeBot": "Bladebot",
        "GlowFly": "Glowfly",
        "TorizoGhost": "Torizo Ghost",
        "BlobThrower": "Blob Thrower",
        "CoreXShell": "Core-X",
        "CoreX": "Core-X",
        "Monster": "Larval Metroid",
        "ChuteLeech": "Chute Leech",
        "MeboidBarrier": "Meboid",
        "Meboid": "Mebit",
        "WConnector": "Chiny Tozo", # Skip to default (the M gets killed)
        "TestKeys": "Chiny Tozo", # Skip to default
    }
    enemy = enemy.replace("o", "", 1)  # Remove leading 'o' if present
    enemy = re.sub(r'^M(?=[A-Z])', '', enemy) # Remove leading 'M' if followed by uppercase letter

    for entry in known_problems: # Check for known problems first
        if enemy.startswith(entry):
            return known_problems[entry]

    match = re.match(r'([A-Z][a-z]+)', enemy) # Match CamelCase pattern
    if match:
        return match.group(1)


    return "Chiny Tozo"  # Default fallback name





class AM2RCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_am2r(self):
        """Check AM2R Connection State"""
        if isinstance(self.ctx, AM2RContext):
            logger.info(f"Connection Status: {self.ctx.am2r_status}")

    def _cmd_septoggs(self):
        """Septogg information"""
        logger.info("Hi, messenger for the co-creator of the Septoggs here. The Septoggs were creatures found in the \
original MII as platforms to help samus with Space Jumping, we wanted to include them along with the Blob Throwers to \
complete the enemy roster from the original game, but had to come up with another purpose for them to work besides \
floating platforms. They do help the player, which is most noticeable in randomizer modes, but they also act as \
environmental story telling, akin to the Zebesian Roaches and Tatori from Super Metroid. This can be seen with the Baby \
Septoggs randomly appearing in certain areas with camouflage of that environment, more and more babies appearing by \
Metroid husks in the breeding grounds after more Metroids are killed in the area (to show how much damage the Metroids \
can cause to the ecosystem and establish that Septoggs are scavengers), and Baby Septoggs staying close to Elder \
Septoggs (as they feel safe next to the durable Elders)")

    def _cmd_credits(self):
        """Huge thanks to all the people listed here"""
        logger.info("AM2R Multiworld Randomizer brought to you by:")
        logger.info("Programmers: Ehseezed and DodoBirb")
        logger.info("Additional help by: Scungip")
        logger.info("Initial Multiworld Mod by: DodoBirb")
        logger.info("Resplashed Mod by: Abyssal Creature, Mystical")
        logger.info("Multisquared Mod by: Steele")
        logger.info("Sprite Artists: Abyssal Creature, Mimolette")
        logger.info("New Trap Sprites by: Mystical")
        logger.info("Special Thanks to all the beta testers and the AM2R Community Updates Team")
        logger.info("And Variable who was conned into becoming a programmer to fix issues he found")


    def _cmd_deathlink(self):
        """Toggles deathlink"""
        if isinstance(self.ctx, AM2RContext):
            self.ctx.set_deathLink = not self.ctx.set_deathLink
            if self.ctx.set_deathLink:
                logger.info(f"Deathlink enabled.")
            else:
                logger.info(f"Deathlink disabled.")

    def _cmd_custom_message(self, *message):
        """Add a custom deathlink message. Use {player} to include your player name,
        {enemy} to include the enemy that killed you (if available),
        and {randplayer} to include a random player.
        Use /custom_message with no arguments to see your current custom messages."""

        global custom_messages
        message = " ".join(message).strip()
        if message == "":
            if len(custom_messages) == 0:
                logger.info("You have no custom deathlink messages.")
            else:
                logger.info("Your custom deathlink messages are:")
                for i, msg in enumerate(custom_messages):
                    logger.info(f"  {i + 1}. {msg}")
                logger.info("Use /custom_message <message> to add a new message.")
                logger.info("Use /remove_custom_message <number> to remove a message.")
        else:
            if message in custom_messages:
                logger.info("This message is already in your custom messages.")
            else:
                custom_messages.append(message)
                logger.info("Custom deathlink message added.")


    def _cmd_toggle_messages(self, type: str = ""):
        """Toggles what deathlink messages you will send if enabled"""
        global enable_default
        global enable_ror2
        global enable_terraria
        global enable_copypastas
        global enable_enemy
        global enable_randplayer
        global enable_custom

        if type == "":
            logger.info("You can toggle the following deathlink message categories:")
            logger.info("default - A standard message pack everyone gets")
            if enable_default:
                logger.info("  (currently enabled)")
            else:
                logger.info("  (currently disabled)")

            logger.info("ror2 - Messages ripped directly from Risk of Rain( Returns/2)")
            if enable_ror2:
                logger.info("  (currently enabled)")
            else:
                logger.info("  (currently disabled)")

            if enable_terraria:
                logger.info("terraria - Messages ripped directly from Terraria")
                if enable_terraria:
                    logger.info("  (currently enabled)")

            logger.info("copypastas - Various copypastas")
            if enable_copypastas:
                logger.info("  (currently enabled)")
            else:
                logger.info("  (currently disabled)")

            logger.info("enemy - Messages that include an enemy")
            if enable_enemy:
                logger.info("  (currently enabled)")
            else:
                logger.info("  (currently disabled)")
            logger.info("randplayer - Messages that include another random player")
            if enable_randplayer:
                logger.info("  (currently enabled)")
            else:
                logger.info("  (currently disabled)")

            logger.info("custom - Custom messages you have added using /custom_message")
            if enable_custom:
                logger.info("  (currently enabled)")
            else:
                logger.info("  (currently disabled)")
            logger.info("Use /toggle_messages <category> to toggle a category")

        elif type == "default":
            enable_default = not enable_default
            if enable_default:
                logger.info("Default deathlink messages enabled.")
            else:
                logger.info("Default deathlink messages disabled.")
        elif type == "ror2":
            enable_ror2 = not enable_ror2
            if enable_ror2:
                logger.info("Risk of Rain 2 deathlink messages enabled.")
            else:
                logger.info("Risk of Rain 2 deathlink messages disabled.")
        elif type == "terraria":
            enable_terraria = not enable_terraria
            if enable_terraria:
                logger.info("Terraria deathlink messages enabled.")
            else:
                logger.info("Terraria deathlink messages disabled.")
        elif type == "copypastas":
            enable_copypastas = not enable_copypastas
            if enable_copypastas:
                logger.info("Copypasta deathlink messages enabled.")
            else:
                logger.info("Copypasta deathlink messages disabled.")
        elif type == "enemy":
            enable_enemy = not enable_enemy
            if enable_enemy:
                logger.info("Enemy deathlink messages enabled.")
            else:
                logger.info("Enemy deathlink messages disabled.")
        elif type == "randplayer":
            enable_randplayer = not enable_randplayer
            if enable_randplayer:
                logger.info("Random player deathlink messages enabled.")
            else:
                logger.info("Random player deathlink messages disabled.")
        elif type == "custom":
            enable_custom = not enable_custom
            if enable_custom:
                logger.info("Custom deathlink messages enabled.")
            else:
                logger.info("Custom deathlink messages disabled.")
        else:
            logger.info(f"Unknown category '{type}'. Use /toggle_messages with no arguments to see a list of categories.")

        if not(enable_default or enable_ror2 or enable_terraria or enable_copypastas or enable_enemy or enable_randplayer):
            logger.info("All deathlink message categories are disabled. You will send a generic message when you die.")


class AM2RContext(CommonContext):
    command_processor = AM2RCommandProcessor
    game = 'AM2R'
    items_handling = 0b111 # full remote
    
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.error_message = []
        self.waiting_for_client = False
        self.am2r_streams: (StreamReader, StreamWriter) = None
        self.am2r_sync_task = None
        self.am2r_status = CONNECTION_INITIAL_STATUS
        self.received_locscouts = False
        self.metroids_required = 41
        self.client_requesting_scouts = False
        self.TrapSprites = 0
        self.Tozos = 0
        self.deathlink_pending = None
        self.set_deathLink = False

    
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            self.waiting_for_client = True
            logger.info('No AM2R details found. Reconnect to MW server after AM2R is connected.')
            return
        
        await self.send_connect()

    def run_gui(self):
        import webbrowser
        from kvui import GameManager
        from kivy.metrics import dp
        from kivymd.uix.menu import MDDropdownMenu
        from kivymd.uix.button import MDButton, MDButtonText



        class AM2RManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "AM2R Multiworld Client"

            def menu_open(self, button):
                import urllib.request, json
                with urllib.request.urlopen("https://raw.githubusercontent.com/Ehseezed/Archipelago-Integration/refs/heads/8th-Aniversary/Gotchas/websites.json") as websites:
                    websites = json.loads(websites.read().decode())
                menu_items = [
                    {"text": "Save Custom Messages", "on_release": lambda: save_custom_messages_to_file()},
                    {"text": "Load Custom Messages", "on_release": lambda: load_custom_messages_from_file(False)},
                    {"text": "Overwrite Custom Messages", "on_release": lambda: overwrite_custom_messages()},
                    {"text": "Help!", "on_release": lambda: webbrowser.open("https://github.com/Ehseezed/Archipelago-Integration/blob/8th-Aniversary/Gotchas%2FGotchas.md")},
                    {"text": "Thursday", "on_release": lambda: webbrowser.open(random.choice(websites))},
                ]
                MDDropdownMenu(caller=button, items=menu_items, width_mult=3).open()


            def build(self):
                b = super().build()

                dropdown_button = MDButton(MDButtonText(text="Menu"), style="filled", size=(dp(100), dp(70)), radius=5,
                                           size_hint_x=None, size_hint_y=None, pos_hint={"center_y": 0.55},
                                           on_release=self.menu_open)
                dropdown_button.height = self.server_connect_bar.height
                self.connect_layout.add_widget(dropdown_button)
                return b

        self.ui = AM2RManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict):
        global players
        global custom_messages
        global enable_enemy
        global enable_default
        global enable_ror2
        global enable_terraria
        global enable_copypastas
        global enable_randplayer
        global enable_custom
        global AprilFoolsSurprise


        if cmd == "Connected":
            players = list(self.player_names.values())
            self.metroids_required = args["slot_data"]["MetroidsRequired"]

            local_version = get_version()

            try:
                rolled_version = args["slot_data"]["Version"]
            except KeyError:
                rolled_version = "0"

            if local_version !=  rolled_version or "unknown" in (local_version, rolled_version):
                if not(rolled_version == "unknown" or local_version is None):
                    self.error_message = ["0"]
                    if local_version < rolled_version:
                        self.error_message.append(f"your seed might have extra features that your current client version does not support please update to at least version {rolled_version} of the world to match what was used to generate the seed")
                    else:
                        if rolled_version == "0":
                            self.error_message[0] = ("Whoever rolled this seed is using a version of the randomizer older than 1.3.2 \n"
                                               "Please be aware that some of the settings you have intended to use may not work as expected\n"
                                               "Actually I'm shocked that this made it past generation so please let me know if you ever manage to see this")
                            self.error_message.append("From updates older than 1.4.0: you will miss out on Wrong Warps, Trap Sprites, Tozo Chance, and Deathlink\n"
                                       "Fortunately Deathlink is handled client side so you should be fine there but if you had custom messages you will need to re-add them")
                        else:
                            self.error_message[0] = f"Whoever rolled this seed is using AM2R Multiworld Randomizer version {rolled_version}\n"

                        if rolled_version < "1.4.0":
                            self.error_message.append("From update 1.4.0: you will miss out on Ice Traps")

                        if rolled_version < "1.4.4":
                            self.error_message.append("From update 1.4.4: you will miss out on seeded wrong warp traps, fixing the \"fake bombs\" issue that nobody noticed, and weighted minor item fill")

                        # if rolled_version < []:
                        #     message = ""
                        #     self.error_message.append(message)

                    if self.error_message[0] == "0":
                        self.error_message.pop(0)
                else:
                    if local_version == "unknown":
                        a = "the client"
                    if rolled_version == "unknown":
                        a = "the server"
                    self.error_message[0] = f"Could not determine version mismatch due to unknown version on {a}."


            try:
                self.trap_list = generate_transitions(args["slot_data"]["TrapSeed"])
            except KeyError:
                self.trap_list = generate_transitions(0)
            try:
                self.Tozos = args["slot_data"]["Tozos"]
                self.TrapSprites = args["slot_data"]["TrapSprites"]
            except KeyError:
                self.Tozos = 0
                self.TrapSprites = 5
            try:
                if args["slot_data"]["DeathLink"]:
                    self.set_deathLink = True
            except KeyError:
                self.set_deathLink = False

            try:
                custom_messages = args["slot_data"]["CustomDeathLinkMessages"]
            except KeyError:
                custom_messages = []

            try:
                message_packs = args["slot_data"]["DeathlinkMessagePacks"]
                enable_enemy = True if "enemy" in message_packs else False
                enable_default = True if "default" in message_packs else False
                enable_ror2 = True if "ror2" in message_packs else False
                enable_terraria = True if "terraria" in message_packs else False
                enable_copypastas = True if "copypastas" in message_packs else False
                enable_randplayer = True if "randplayer" in message_packs else False
                enable_custom = True if "custom" in message_packs else False
            except KeyError:
                enable_enemy = False
                enable_default =False
                enable_ror2 = False
                enable_terraria = False
                enable_copypastas = False
                enable_randplayer = False
                enable_custom = False

            try:
                if args["slot_data"]["AprilFoolsSurprise"]:
                    AprilFoolsSurprise = True
            except:
                AprilFoolsSurprise = False

        elif cmd == "LocationInfo":
            logger.info("Received Location Info")
            if self.error_message is not None:
                self.error_message = list(tuple(self.error_message))
                for message in self.error_message:
                    self.ui.print_json([{"text": message,
                                         "type": "color",
                                         "color": "red"}])
                self.error_message = None


    def on_deathlink(self, data: dict):
        self.deathlink_pending = "whatkillsyou"
        super().on_deathlink(data)

def generate_transitions(trap_seed):
    rooms = []
    print(f'Trap Seed: {trap_seed}')
    evil_rooms = [129, 236, 237, 243, 244, 245, 351, 357, 358, 380, 381, 385, 391, 392]
    random.seed(trap_seed)
    while len(rooms) <= 99:
        room = randint(21, 393)
        while room in evil_rooms:
            print("extremely loud incorrect buzzer")
            room = randint(21, 393)
            room = str(room)

        rooms.append(room)
    print(f'rooms: {rooms}')

    return rooms




def get_payload(ctx: AM2RContext):
    global upper, lower

    items_to_give = [item_id_to_game_id[item.item] for item in ctx.items_received if item.item in item_id_to_game_id]
    if not ctx.locations_info:
        locations = [location.code for location in get_location_datas(None, None) if location.code is not None]
        async_start(ctx.send_msgs([{"cmd": "LocationScouts", "locations": locations, "create_as_hint": 0}]))
        return json.dumps({
            "cmd": "items", "items": items_to_give 
        })

    match ctx.TrapSprites:
        case 0:
            upper = 82
            lower = 20
        case 2:
            upper = 38
            lower = 20
        case 1:
            upper = 47
            lower = 40
        case 3:
            upper = 62
            lower = 50
        case 4:
            upper = 82
            lower = 70
        case 5:
            upper = 15
            lower = 0
        case _:
            upper = 15
            lower = 0

    if AprilFoolsSurprise:
        upper = 82
        lower = 0


    non_ids = [48,49,63,64,65,66,67,68,69]

    # 0b111 = full remote
    # 0b000 = bad
    # 0b001 = progression
    # 0b010 = good
    # 0b100 = trap

    if ctx.deathlink_pending:
        print(f"Deathlink pending: {ctx.deathlink_pending}")


    if ctx.deathlink_pending == "whatkillsyou":
        ctx.deathlink_pending = None
        return json.dumps({
            "cmd": "whatkillsyou",
        })

    if ctx.client_requesting_scouts:
        itemdict = {}
        for locationid, netitem in ctx.locations_info.items():
            itemid = randint(lower, upper)
            while itemid in non_ids:
                print("extremely loud incorrect buzzer")
                itemid = randint(lower, upper)
            gamelocation = location_id_to_game_id[locationid]

            if ctx.Tozos != 0:
                if netitem.item in item_id_to_game_id:
                    if netitem.flags & 0b100 != 0:
                        gameitem = itemid
                    elif ctx.Tozos > randint(0,100):
                        gameitem = item_id_to_game_id[netitem.item] + 20
                    else:
                        gameitem = item_id_to_game_id[netitem.item]
                elif netitem.flags & 0b001 == 1:
                    gameitem = 102 #
                else:
                    gameitem = 103
            else:
                if netitem.item in item_id_to_game_id:
                    if netitem.flags & 0b100 != 0:
                        gameitem = itemid
                    else:
                        gameitem = item_id_to_game_id[netitem.item]
                elif netitem.flags & 0b001 == 1:
                    gameitem = 100
                else:
                    gameitem = 101
            if AprilFoolsSurprise:
                gameitem = itemid
            itemdict[gamelocation] = gameitem
        ret = json.dumps(
            {
                'cmd':"locations",
                'items': itemdict,
                'metroids': ctx.metroids_required,
                'trapseed': ctx.trap_list
            }
        )
        return ret
    ret_payload = json.dumps(
        {
           "cmd": "items",
           "items": items_to_give,
        }
    )
    return ret_payload

async def parse_payload(ctx: AM2RContext, data_decoded):
    item_list = [game_id_to_location_id[int(location)] for location in data_decoded["Items"]]
    game_finished = bool(int(data_decoded["GameCompleted"]))
    item_set = set(item_list)
    ctx.locations_checked = item_list
    new_locations = [location for location in ctx.missing_locations if location in item_set]
    if new_locations:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_locations}])
    if game_finished and not ctx.finished_game:
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": 30}])
        ctx.finished_game = True

async def am2r_sync_task(ctx: AM2RContext):
    global players
    logger.info("Starting AM2R connector, use /am2r for status information.")
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "white"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "black"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "red"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "green"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "yellow"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "blue"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "magenta"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "cyan"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "slateblue"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "plum"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "salmon"}])
    # ctx.ui.print_json([{"text": "This is a color test",
    #                     "type": "color",
    #                     "color": "orange"}])
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.am2r_streams:
            (reader, writer) = ctx.am2r_streams
            msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=5)
                    data_decoded = json.loads(data.decode())
                    ctx.auth = data_decoded["SlotName"]
                    ctx.password = data_decoded["SlotPass"]
                    ctx.client_requesting_scouts = not bool(int(data_decoded["SeedReceived"]))
                    await parse_payload(ctx, data_decoded)
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.am2r_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.am2r_streams = None


                await ctx.update_death_link(ctx.set_deathLink)

                if data_decoded["Deathlinked"] == True and ctx.set_deathLink:
                # if True:
                    consoles = ["Color TV-Game", "NES/Famicom", "Super Famicom/SNES", "Nintendo 64", "GameCube",
                                "Wii", "Wii U", "Nintendo Switch", "Nintendo Switch 2", "Game & Watch", "Game Boy",
                                "Game Boy Advance", "Nintendo DS", "Nintendo 3DS", "Pokemon Mini", "Virtual Boy"]
                    reasons = []
                    if ctx.auth in players:
                        players.remove(ctx.auth)
                    if "Archipelago" in players:
                        players.remove("Archipelago")

                    try:
                        rand_player = random.choice(players)
                    except IndexError:
                        rand_player = "Ehseezed"
                    player = ctx.auth
                    enemy = data_decoded["CauseOfDeath"]
                    enemy = extract_enemy_name(enemy)
                    print(f"Enemy extracted: {enemy}")
                    reason = ""

                    default = [
                        f"{player} was killed",
                        f"{player} forgot their X-Vaccine",
                        f"Omega Metroid landed the 0 to death on {player}",
                        f"{player} ran out of Energy",
                        f"{player}'s controller disconnected",
                        f"{player} bid farewell, cruel world",
                        f"{player} has turned you into a tombstone",
                        f"What?\nKills you",
                        f"{player} is not feeling good...\nThey are feeling evil",
                        f"{player} wants you to know it was a rollback hit",
                        "Thursday",  # Special handling for Thursday
                        f"{player} was slain by a Chiny Tozo",
                        f"Which one of you idiots decided that {player} sends DeathLinks?",
                        f"{player} received a DMCA takedown notice from Nintendo",
                        f"{player} ran out of memory",
                        f"{player}'s level was divisible by 5",
                        f"{player} was brutally murdered by hammers and whatnot",
                        f"{player} is wondering if there is a better way",
                        f"{player} was found by the SA-X",
                        f"{player} just simply wanted to kill you",
                        f"{player}'s power bomb did not scare the metroid",
                        f"{player} was not authorised by Adam",
                        f"{player} calls it \"Wide Beam\" and was promptly killed for it",
                        f"{player} has always been a bit clumsy",
                        f"{player} couldn't escape mines",
                        f"{player} has a modern Android device",
                        f"{player} was silenced for asking for a Mac port",
                        f"{player} is prohibited to speak for the next 12 hours and by law has to stand up for the next 4",
                        f"Fatal Memory Error\nOut of memory!",
                        f"{player} was trying to port AM2R to the {random.choice(consoles)}",
                        f"{player}'s blunder will be added to the skullboard",
                        f"{player} wants you to immagine this (https://www.youtube.com/watch?v=Ad87SqVYizA) any time they die",
                        f"{player} wants you to know that they are not a gamer",
                        f"{player} wants you to know that stick drift is real and its really annoying",
                        f"Your honor {player} is innocent, the real criminal is the one who decided that {player} should send DeathLinks",
                        f"{player} was killed by a horde of angry Archipelago players for sending DeathLinks",
                        f"{player} has been suspended for 50 days.",
                        f"That gameplay was ass: Multiworld Terminated",
                        f"For whom the wombat malls",
                        f"{player} insists its but a scratch",
                        f"{player} experienced the killer rabbit",
                        (f"In front of you are 2 doors. Due to budget cuts only {player} stand in front of "
                         f"them and {player} lies 50% of the time."),
                        f"In front of {player} there are 2 doors. Due to budget cuts, only Ehseezed stands in front of them, and Ehseezed lies 50% of the time.",
                        f"{player} saved the animals",
                        f"{player} touched the sand map",
                        f"Unlike the Gatordile algorithm, {player} does not stay winning",
                        f"{player} could not stop gambling",
                        f"{player} got everyone else killed making them tonight's biggest loser",
                        f"{player} had a bad time",
                        f"{player} fell for it",
                        f"{player} pixel bonked",
                        f"{player} was sent to the crystal",
                        f"{player} pulled a lever, it was the wrong one",
                        f"{player} has released all the remaining hate from their world",
                        f"And Yet.",
                        f"{player} asked for AM2R support on the main server",
                        f"{player} piped an online command into bash",
                        f"{player}@{player}:~$sudo rm -rf / --no-preserve-root",
                    ]
                    includes_random_player = [
                        f"{player} and their friends suffered the consequences of {player}'s actions",
                        f"In front of {player} there are 2 doors. Due to budget cuts, only {rand_player} stands in front of them, and {rand_player} lies 50% of the time.",
                        f"{rand_player} had the controller",
                        f"Mom said it was {rand_player}'s turn on the Game Boy",
                        f"{player} did that to mess with {rand_player}",
                    ]
                    includes_enemy = [
                        f"{player} was killed by {enemy}",
                        f"{enemy} will be celebrated for this one",
                        f"{player}: \"What?\"\n{enemy}: \"Kills you\"",
                        f"{player}: \"What?\"\n{enemy}: \"Kills you\"",
                        f"{enemy} did not like the way {player} looked at them",
                        f"{enemy} was defending their honor",
                        f"{enemy} asked",
                        f"{player}\'s last time fighting {enemy} was in 1.1",
                        f"{player}@{enemy}:~$sudo rm -rf / --no-preserve-root"
                    ]
                    ror2 = [
                        f"{player} dies a slightly embarrassing death",
                        f"{player} votes to lower the difficulty",
                        f"Not a trace of {player} will be found",
                        f"The planet has killed {player}",
                        f"That was absolutely {player}'s fault",
                        f"That was definitely not {player}'s fault",
                        f"Beep.. beep.. beeeeeeeeeeeeeeeee",
                        f"{player} was styled uppon",
                        f"{player} has shattered into innumerable pieces",
                    ]
                    terraria = [
                        f"{player} was slain by {enemy}."
                        f"{player} was eviscerated by {rand_player}'s Speed Booster."
                        f"{player} was murdered by {rand_player}'s Bad Sense of Humor."
                        f"{player}'s face was torn off by {enemy}."
                        f"{player}'s entrails were ripped out by {enemy}."
                        f"{player} was destroyed by {rand_player}'s Greed."
                        f"{player}'s skull was crushed by {rand_player}'s Hammer."
                        f"{player} got massacred by {enemy}."
                        f"{player} got impaled by {rand_player}'s Super Missile."
                        f"{player} was torn in half by {enemy}."
                        f"{player} was decapitaded by {rand_player}'s Gambling Adiction."
                        f"{player} let their arms get torn off by {enemy}."
                        f"{player} watched their innards become outards by {rand_player}'s OOL Checks."
                        f"{player} was brutally dissected by {enemy}."
                        f"{player}'s extremities were detached by {rand_player}'s Ping Reply."
                        f"{player}'s body was mangled by {enemy}."
                        f"{player}'s vital organs were ruptured by {rand_player}'s BK Game."
                        f"{player} was turned into a pile of flesh by {enemy}."
                        f"{player} was removed from the multiworld by {rand_player}'s Bad Memory."
                        f"{player} got snapped in half by {enemy}."
                        f"{player} was cut down the middle by {enemy}."
                        f"{player} was chopped up by {rand_player}'s Gen Alpha Slang."
                        f"{player}'s plea for death was answered by {rand_player}'s Hatred."
                        f"{player}'s meat was ripped off the bone by {enemy}."
                        f"{player}'s flailing about was finally stopped by {rand_player}'s Out of Memory Error."
                        f"{player} had their head removed by {enemy}."
                        f"{player}'s bowels were unplugged by {rand_player}'s Speech Disorder."
                        f"{player}'s journey was ended by {enemy}."
                        f"{player} was sent to Ocram's House by {rand_player}'s Bad Decision Making."
                        f"{player} was macerated by {enemy}."
                        f"{player} was exsanguinated by {rand_player}'s Thirsty Aptitude."
                        f"{player} was sent to the bone zone by {rand_player}'s Guitar Riff."
                        f"{player} was spontaneously lobotomized by {enemy}."
                        f"{player} was pressed into a succulent pulp by {rand_player}'s Lack of Checks."
                        f"{player} was ground into sad meat by {enemy}."
                        f"{player}'s bones were shattered by {rand_player}'s Bomb."
                        f"{player} was turned into monster food by {enemy}."
                        f"{player} had their home remodeled by {rand_player}'s Game Addiction."
                        f"{player} was voluntold to donate blood by {enemy}."
                        f"{player} had their cap peeled back by {rand_player}'s YAML Settings."
                        f"{player}'s top knot was carved off by {enemy}."
                        f"{player}'s parts were misplaced by {rand_player}'s Generation Error."
                        f"{player} was blended into a zesty sauce by {rand_player}'s Psychic Powers."
                        f"{player}'s spine was ripped out by {enemy}."
                        f"{player}'s living streak was ended by {rand_player}'s Game Choices."
                        f"{player} received a forced amputation by {enemy}."
                        f"{player}'s neck was snapped by {rand_player}'s These Hands."
                        f"{player} was shredded to bits by {enemy}."
                        f"{player} succumbed to a fatal injury by {enemy}."
                        f"{player} was informed of their expiration date by {rand_player}'s Credit Card."
                        f"{player}'s incompetence was put on display by {enemy}."
                        f"{player}'s soul was extractinated by {rand_player}'s Thirty Scarabs."
                        f"{player} underwent a merciful euthanasia by {enemy}."
                        f"{player} was eaten from the bottom up by {enemy}."
                        f"{player} was deboned by {rand_player}'s 2/7 Children Kills."
                        f"{player} had both kidneys stolen by {rand_player}'s Lips and Teeth."
                        f"{player}'s depravity was ended by {enemy}."
                        f"{player}'s disc was herniated by {enemy}."
                        f"{player}'s body was donated to science by {rand_player}'s Chiny Tozos."
                        f"{player} had their brain turned to jam by {rand_player}'s Negative Energy."
                        f"{player} was turned into a long pig by {enemy}."
                        f"{player} was sent to the farm by {enemy}."
                        f"{player}'s clogs were popped by {enemy}."
                        f"{player}'s ticker was stopped by {rand_player}'s Time Eaters."
                        f"{player} was whacked in the head by {rand_player}'s Stick."
                        f"{player} got rubbed out by {rand_player}'s I Use Arch btw."
                        f"{player} was degloved by {enemy}."
                        f"{player} was flayed by {enemy}."
                        f"{player} was ganked by {enemy}."
                        f"{player} got spanked by {rand_player}'s Hint Cost."
                        f"{player} got got by {rand_player}'s Horrible Sleep Schedule."
                        f"{player} got murked by {rand_player}'s Smugness."
                        f"{player} was put in a glass coffin by {enemy}."
                        f"{player} was put on the wrong side of the grass by {enemy}."
                        f"{player} will quickly be forgotten by {rand_player}'s Game Coordination."
                        f"{player} was smote by {enemy}."
                        f"{player} fell to their death."
                        f"{player} didn't bounce."
                        f"{player} invented gravity."
                        f"{player} discovered the meaning of defenestration."
                        f"{player} was freeeee, free-fallin'."
                        f"{player} tried to ice skate uphill."
                        f"{player} thought they could fly."
                        f"{player} left a crater."
                        f"{player} forgot their happy thought."
                        f"{player} forgot to breathe."
                        f"{player} is sleeping with the fish."
                        f"{player} drowned."
                        f"{player} is shark food."
                        f"{player} tried to drink a lake."
                        f"{player} discovered Atlantis."
                        f"{player} forgot to bring a towel."
                        f"{player} got melted."
                        f"{player} was incinerated."
                        f"{player} tried to swim in lava."
                        f"{player} likes to play in magma."
                        f"{player} is bad at the Floor Is Lava."
                        f"{player} couldn't put the fire out."
                        f"{player} was reduced to charcoal."
                        f"{player} was burnt to a crisp."
                        f"{player} is a well-done steak."
                        f"{player} was consumed by the inferno."
                        f"{player} couldn't find the antidote."
                        f"{player} couldn't breathe."
                        f"{player} was buried alive."
                        f"{player} couldn't contain the watts."
                        f"{player} was turned into a battery."
                        f"{player}'s positive lifeforce became negative."
                        f"{player} became a lightning rod."
                        f"{player} shattered into pieces."
                        f"{player} can't be put back together again."
                        f"{player} needs to be swept up."
                        f"{player} just became another dirt pile."
                        f"{player}'s legs appeared where their head should be."
                        f"{player} didn't materialize."
                        f"{player} starved to death."
                        f"{player} couldn't find food."
                        f"{player} forgot to eat."
                        f"{player} was licked."
                        f"{player} got to 1st base with the Wall of Flesh!"
                        f"{player} tried to escape."
                        f"{player} died for the team."
                        f"{player} was slain..."
                        f"{player} was stabbed."
                        f"{player} was killed by something in the dark!"
                        f"{player} became an astronaut."
                        f"{player} is now space debris."
                        f"{player} left orbit."
                        f"{player} has ascended."
                        f"{player} departed SR388."
                        f"{player} was never seen again."
                        f"{player} dug too deep."
                        f"{player} never stopped falling."
                        f"{player} entered the abyss."
                        f"{player} reached the core."
                    ]
                    copypastas = [
                        (f"{player}, you little fucker.  You made a shit of piece with your trash Isaac. "
                         f"It's fucking bad, this trash game. I will become back my money. "
                         f"I hope you will in your next time a cow on a trash farm you sucker."),

                        ("The FitnessGram™ Pacer Test is a multistage aerobic capacity test that progressively "
                         "gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. "
                         "Line up at the start. The running speed starts slowly, but gets faster each minute after you "
                         "hear this signal. [beep] A single lap should be completed each time you hear this sound. "
                         "[ding] Remember to run in a straight line, and run as long as possible. The second time you "
                         "fail to complete a lap before the sound, your test is over. The test will begin on the word "
                         "start. On your mark, get ready, start."),
                    ]

                    try:
                        for i in range(len(custom_messages)):
                            custom_messages[i] = custom_messages[i].replace("{player}", player)
                            custom_messages[i] = custom_messages[i].replace("{enemy}", enemy)
                            custom_messages[i] = custom_messages[i].replace("{rand_player}", rand_player)
                    except:
                        pass

                    if enable_default:
                        reasons.extend(default)

                    if enable_ror2:
                        reasons.extend(ror2)

                    if enable_terraria:
                        reasons.extend(terraria)

                    if enable_copypastas:
                        reasons.extend(copypastas)

                    if enemy != "Chiny Tozo" and enable_enemy:
                        reasons.extend(includes_enemy)

                    if rand_player != "" and enable_randplayer:
                        reasons.extend(includes_random_player)

                    if len(custom_messages) > 0 and enable_custom:
                        reasons.extend(custom_messages)

                    reason = random.choice(reasons)

                    if enemy == "Client":
                        reason = f"This one wasnt {player}\'s fault it was whoever turned on Health Sync"

                    if reason == "Thursday":
                        if datetime.datetime.now().weekday() != 3:
                            reason = f"{player} remembered it isn't Thursday yet"
                        else:
                            reason = f"{player} realized \"Thursday\" is not this Thursday"

                    if reason == "":
                        reason = "Ehseezed has made an error in their code and you should probably alert them\nUnless you have no messages enabled in which case its your fault"
                        if not (enable_default or enable_ror2 or enable_terraria or enable_copypastas or enable_enemy or enable_randplayer):
                            logger.info("Hey its me this one is your fault not mine you disabled all the message categories")


                    ctx.ui.print_json([{"text": f"Sent Deathlink Message: \n{reason}",
                                        "type": "color",
                                        "color": "cyan"}])

                    await ctx.send_death(f"{reason}")



            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.am2r_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.am2r_streams = None

            if ctx.am2r_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Slot name: " + ctx.auth)
                    logger.info("Successfully Connected to AM2R")
                    ctx.am2r_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.am2r_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.am2r_status = error_status
                logger.info("Lost connection to AM2R and attempting to reconnect. Use /am2r for status updates")
        else:
            try:
                # logger.debug("Attempting to connect to AM2R")
                ctx.am2r_streams = await asyncio.wait_for(asyncio.open_connection("127.0.0.1", 64197), timeout=10)
                ctx.am2r_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.am2r_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                # logger.debug("Connection Refused, Trying Again")
                ctx.am2r_status = CONNECTION_REFUSED_STATUS
                continue

async def main(args):
    random.seed()
    ctx = AM2RContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    ctx.am2r_sync_task = asyncio.create_task(am2r_sync_task(ctx), name="AM2R Sync")
    await ctx.exit_event.wait()
    ctx.server_address = None

    await ctx.shutdown()


def launch():
    # Text Mode to use !hint and such with games that have no text entry
    import colorama

    parser = get_base_parser(description="AM2R Client for interfacing with AM2RMultiworld/Multisquared mods")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args()

    colorama.init(args)

    asyncio.run(main(args))
    colorama.deinit()

if __name__ == "__main__":
    launch()