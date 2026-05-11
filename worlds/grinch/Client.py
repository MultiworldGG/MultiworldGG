import math
import time
import re
from typing import TYPE_CHECKING, Sequence
import asyncio
import NetUtils
import copy
import uuid
import Utils
from BaseClasses import ItemClassification
from worlds.grinch.RamHandler import UpdateMethod
from . import MOVES_TABLE
from .Locations import grinch_locations, GrinchLocation
from .Items import (
    ALL_ITEMS_TABLE,
    MISSION_ITEMS_TABLE,
    GADGETS_TABLE,
    KEYS_TABLE,
    GrinchItemData,
    SLEIGH_TABLE, grinch_items, GrinchItem,
)
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Regions import ALL_REGIONS_INFO
from .Traps import convert_trap

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from CommonClient import logger


# Stores received index of last item received in PS1 memory card save data
# By storing this index, it will remember the last item received and prevent item duplication loops
RECV_ITEM_ADDR = 0x010068
RECV_ITEM_BITSIZE = 4

# Maximum number of times we check if we are in demo mode or not
MAX_DEMO_MODE_CHECK = 30

# List of Menu Map IDs
MENU_MAP_IDS: list[int] = [0x00, 0x02, 0x35, 0x36, 0x37]

MAX_EGGS: int = 200
EGG_COUNT_ADDR: int = 0x010058
EGG_ADDR_BYTESIZE: int = 2

MAX_NITRO_THISTLE: int = 5
NITRO_THISTLE_COUNT_ADDR: int = 0x095305
NITRO_THISTLE_BYTESIZE: int = 1

# Address and value used in checking to teleport player.
START_BUTTON_ADDR: int = 0x01000B
OTHER_BUTTON_ADDR: int = 0x01000A
BUTTONS_ADDR_SIZE: int = 1

# Address and values to teleport
MAP_REGION_ADDR: int = 0x010000
TRIGGER_PLAYER_TELEPORT: int = 0x08FB94
LOBBY_TRIGGER_ADDR: int = 0x0101FF
TRIGGER_ADDR_SIZE: int = 1
MOUNT_CRUMPIT_MAP_ID: int = 0x05
DISGUISE_OFF_ADDR: int = 0x0100B4

# Address related to the ingame timer
TIMER_ADDR: int = 0x0100B3

# Address related to Mount Crumpit Elevator's position
MC_ELEVATOR_ADDR: int = 0x01010D

# Offsets from region table used to handle deathlink related things
HEALTH_REGION_OFFSET: int = 0x3C
DEATHLINK_REGION_OFFSET: int = 0x27
DEATHLINK_CHECK_OFFSET: int = 0x23
ANIMATION_REGION_OFFSET: int = 0x37
ANIMATION_ADDR_SIZE: int = 2

DAMAGE_RATE_ADDR: int = 0x0e9006

STARTING_SONG_ADDR: int = 0x08F8D0
LOOP_BACK_ADDR: int = 0x08F8D8
SONG_ADDR_SIZE: int = 1

class GrinchClient(BizHawkClient):
    game = "The Grinch"
    system = "PSX"
    patch_suffix = ".apgrinch"
    items_handling = 0b111
    demo_mode_buffer: int = 0
    last_map_location: int = -1
    ingame_log: bool = False
    cutscene_goo_log: bool = False
    menu_log: bool = False
    demo_log: bool = False
    previous_egg_count: int = 0
    send_ring_link: bool = False
    unique_client_id: int = 0
    ring_link_enabled: bool = False
    is_grinch_dead: bool = False
    curr_region: str | None = None
    music_rando: bool = False
    chosen_music: dict = {}
    #yes

    def __init__(self):
        super().__init__()
        self.last_received_index = 0
        self.loading_bios_msg = False
        self.unlimited_eggs = False
        self.damage_rate = 1
        self.unique_client_id = 0
        self.chosen_music = {}
        self.reduced_cutscenes = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        # TODO Check the ROM data to see if it matches against bytes expected
        grinch_identifier_ram_address: int = 0x00928C
        bios_identifier_ram_address: int = 0x097F30

        try:
            bytes_actual: bytes = (
                await bizhawk.read(ctx.bizhawk_ctx, [(grinch_identifier_ram_address, 11, "MainRAM")])
            )[0]

            psx_rom_name = bytes_actual.decode("ascii")
            if psx_rom_name != "SLUS_011.97":
                bios_bytes_check: bytes = (
                    await bizhawk.read(ctx.bizhawk_ctx, [(bios_identifier_ram_address, 24, "MainRAM")])
                )[0]

                if "System ROM Version" in bios_bytes_check.decode("ascii"):
                    if not self.loading_bios_msg:
                        self.loading_bios_msg = True
                        logger.error("BIOS is currently loading. Will wait up to 5 seconds before retrying.")

                    return False

                logger.error("Invalid rom detected. You are not playing Grinch USA Version.")
                raise Exception("Invalid rom detected. You are not playing Grinch USA Version.")

            ctx.command_processor.commands["ringlink"] = _cmd_ringlink
            ctx.command_processor.commands["deathlink"] = _cmd_deathlink

        except Exception:
            return False

        ctx.game = self.game
        ctx.items_handling = self.items_handling
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        self.loading_bios_msg = False

        return True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        from CommonClient import logger

        super().on_package(ctx, cmd, args)

        match cmd:
            case "Connected":  # On Connect
                self.ingame_log = False
                self.cutscene_goo_log = False
                self.menu_log = False
                self.demo_log = False
                self.unlimited_eggs = bool(ctx.slot_data["unlimited_eggs"])
                self.damage_rate = int(ctx.slot_data["damage_rate"])
                self.music_rando = bool(ctx.slot_data["music_rando"])
                self.chosen_music = dict(ctx.slot_data["chosen_music"])
                self.reduced_cutscenes = bool(ctx.slot_data["reduced_cutscenes"])
                self.unique_client_id = self._get_uuid()
                # logger.info(
                #     "You are now connected to the client. "
                #     + "There may be a slight delay to check you are not in demo mode before locations start to send."
                # )

                if self.music_rando:
                    Utils.async_start(self.randomize_music(ctx),name="Grinch - Music Randomizer")

                if not self.unlimited_eggs:

                    self.ring_link_enabled = bool(ctx.slot_data["ring_link"])
                    death_link_enabled = bool(ctx.slot_data["death_link"])

                    tags = copy.deepcopy(ctx.tags)

                    if self.ring_link_enabled:
                        ctx.tags.add("RingLink")

                    else:
                        ctx.tags -= {"RingLink"}

                    if death_link_enabled:
                        ctx.tags.add("DeathLink")

                    else:
                        ctx.tags -= {"DeathLink"}

                    if tags != ctx.tags:
                        Utils.async_start(
                            ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}]),
                            "Grinch - Update Link Tags",
                        )

            case "PrintJSON":
                if args.get("type", "") == "Countdown" and len(list(args.get("data", []))) > 0 and \
                    "starting countdown of " in args["data"][0]["text"].lower():
                    countdown_timer: int = int(re.search(r"\d+", args["data"][0]["text"]).group())
                    Utils.async_start(self.update_countdown(ctx, countdown_timer), name=f"Update Grinch - Countdown")

            case "Bounced":
                if "tags" not in args:
                    return

                tags = args.get("tags", [])
                # we can skip checking "DeathLink" in ctx.tags, as otherwise we wouldn't have been sent this
                if ("DeathLink" in tags and args["data"]["source"] != ctx.player_names[ctx.slot] and
                    not self.is_grinch_dead):
                    Utils.async_start(self.kill_grinch(ctx), "Grinch - Received DeathLink")

                if (
                    "RingLink" in ctx.tags
                    and "RingLink" in args["tags"]
                    and args["data"]["source"] != self.unique_client_id
                ):
                    Utils.async_start(self.ring_link_input(args["data"]["amount"], ctx), "Grinch - SyncEggs")

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        await ctx.get_username()

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger

        # If the player is not connected to an AP Server, or their connection was disconnected.
        if not ctx.slot:
            return

        try:
            if not await self.ingame_checker(ctx):
                return

            if "RingLink" in ctx.tags and not any(
                task.get_name() == "Grinch EggLink" for task in asyncio.all_tasks()):
                self.send_ring_link = True
                Utils.async_start(self.ring_link_output(ctx), name="Grinch EggLink")

            if not any(task.get_name() == "Grinch - PlayerButtonInput" for task in asyncio.all_tasks()):
                Utils.async_start(self.watch_to_teleport_player(ctx), "Grinch - PlayerButtonInput")

            await self.location_checker(ctx)
            await self.receiving_items_handler(ctx)
            await self.goal_checker(ctx)
            await self.option_handler(ctx)
            await self.constant_address_update(ctx)
            # await self.funny_secret_goal(ctx)
            #await self.adjust_damage_rate(ctx)

            if "DeathLink" in ctx.tags:
                await self.check_grinch_alive(ctx)

        except bizhawk.RequestFailedError as ex:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            logger.error("Failure to connect / authenticate the grinch. Error details: " + str(ex))
            pass

        except Exception as genericEx:
            # For all other errors, catch this and let the client gracefully disconnect
            logger.error("Unknown error occurred while playing the grinch. Error details: " + str(genericEx))
            await ctx.disconnect(False)
            pass

    async def location_checker(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger

        # Update the AP Server to know what locations are not checked yet.
        local_locations_checked: list[int] = []
        addr_list_to_read: list[tuple[int, int, str]] = []
        local_ap_locations: set[int] = copy.deepcopy(ctx.missing_locations)

        # Loop through the first time of everything left to create the list of RAM addresses to read / monitor.
        for missing_location in local_ap_locations:
            grinch_loc_name = ctx.location_names.lookup_in_game(missing_location)
            grinch_loc_ram_data = grinch_locations[grinch_loc_name]
            missing_addr_list: list[tuple[int, int, str]] = [
                (read_addr.ram_address, read_addr.byte_size, read_addr.ram_area)
                for read_addr in grinch_loc_ram_data.update_ram_addr
            ]
            addr_list_to_read = [*addr_list_to_read, *missing_addr_list]

        returned_bytes: list[bytes] = await bizhawk.read(ctx.bizhawk_ctx, addr_list_to_read)

        # Now loop through everything again and this time get the byte value from the above read, convert to int,
        # and check to see if that ram address has our expected value.
        for missing_location in local_ap_locations:
            # Missing location is the AP ID & we need to convert it back to a location name within our game.
            # Using the location name, we can then get the Grinch ram data from there.
            grinch_loc_name = ctx.location_names.lookup_in_game(missing_location)
            grinch_loc_ram_data = grinch_locations[grinch_loc_name]

            # Grinch ram data may have more than one address to update, so we are going to loop through all addresses in a location
            # We use a list here to keep track of all our checks. If they are all true, then and only then do we mark that location as checked.
            ram_checked_list: list[bool] = []

            for addr_to_update in grinch_loc_ram_data.update_ram_addr:
                is_binary = True if not addr_to_update.binary_bit_pos is None else False

                orig_index: int = addr_list_to_read.index(
                    (addr_to_update.ram_address, addr_to_update.byte_size, "MainRAM")
                )
                value_read_from_bizhawk: int = int.from_bytes(returned_bytes[orig_index], "little")

                if is_binary:
                    ram_checked_list.append((value_read_from_bizhawk & (1 << addr_to_update.binary_bit_pos)) > 0)

                else:
                    expected_int_value = addr_to_update.value
                    ram_checked_list.append(expected_int_value == value_read_from_bizhawk)

            if all(ram_checked_list):
                local_locations_checked.append(GrinchLocation.get_apid(grinch_loc_ram_data.id))

        # Update the AP server with the locally checked list of locations (In other words, locations I found in Grinch)
        locations_sent_to_ap: set[int] = await ctx.check_locations(local_locations_checked)

        if len(locations_sent_to_ap) > 0:
            await self.constant_address_update(ctx)

        ctx.locations_checked = set(local_locations_checked)

    async def receiving_items_handler(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        # Len will give us the size of the items received list & we will track that against how many items we received already
        # If the list says that we have 3 items that we already received items, we will ignore and continue.
        # Otherwise, we will get the new items and give them to the player.

        self.last_received_index = int.from_bytes(
            (await bizhawk.read(ctx.bizhawk_ctx, [(RECV_ITEM_ADDR, RECV_ITEM_BITSIZE, "MainRAM")]))[0],
            "little",
        )

        if len(ctx.items_received) == self.last_received_index:
            return

        # Ensures we only get the new items that we want to give the player
        new_items_only = ctx.items_received[self.last_received_index :]
        ram_addr_dict: dict[int, list[int]] = {}

        for item_received in new_items_only:
            local_item = ctx.item_names.lookup_in_game(item_received.item)

            if "unknown item" in local_item.lower():
                logger.warning(
                    f"Unknown item triggered in pool. Item: {local_item}\nIf you see this message, please report it in the Grinch thread in the AP Discord."
                )
                continue

            grinch_item_ram_data = ALL_ITEMS_TABLE[local_item]

            for addr_to_update in grinch_item_ram_data.update_ram_addr:
                is_binary = True if not addr_to_update.binary_bit_pos is None else False

                if addr_to_update.ram_address in ram_addr_dict.keys():
                    current_ram_address_value = ram_addr_dict[addr_to_update.ram_address][0]
                else:
                    current_ram_address_value = int.from_bytes(
                        (
                            await bizhawk.read(
                                ctx.bizhawk_ctx,
                                [
                                    (
                                        addr_to_update.ram_address,
                                        addr_to_update.byte_size,
                                        addr_to_update.ram_area,
                                    )
                                ],
                            )
                        )[0],
                        addr_to_update.endian,
                    )

                if is_binary:
                    current_ram_address_value = current_ram_address_value | (1 << addr_to_update.binary_bit_pos)

                elif addr_to_update.update_method == UpdateMethod.SET:
                    # if grinch_item_ram_data.classification == ItemClassification.trap:
                    #     trap_val: int | None = convert_trap(self.last_map_location, local_item)
                    #     if trap_val is None:
                    #         continue
                    #     current_ram_address_value = trap_val
                    #
                    #     curr_region_data = ALL_REGIONS_INFO[await self.get_current_region()]
                    #
                    #     death_init_val: int = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx,
                    #     [(curr_region_data.map_table_addr + DEATHLINK_REGION_OFFSET,
                    #     1, "MainRAM")]))[0], "little")
                    #
                    #     # Need to update the trigger address
                    #     if not local_item in ["Depletion Trap", "Who sent me back?", "Dump it to Crumpit"]:
                    #         ram_addr_dict[ALL_REGIONS_INFO[self.curr_region].map_table_addr+0x27] = [
                    #             death_init_val+0x40,
                    #             1,
                    #         ]
                    # else:
                        current_ram_address_value = addr_to_update.value

                elif addr_to_update.update_method == UpdateMethod.ADD:
                    # min() gets the lowest of a set, so we can't go over the max_count
                    current_ram_address_value += addr_to_update.value
                    current_ram_address_value = min(current_ram_address_value, addr_to_update.max_count)

                elif addr_to_update.update_method == UpdateMethod.SUBTRACT:
                    # max() gets the highest of a set, so we can't go under the min_count
                    current_ram_address_value += addr_to_update.value
                    current_ram_address_value = max(current_ram_address_value, addr_to_update.min_count)

                # Write the updated value back into RAM
                ram_addr_dict[addr_to_update.ram_address] = [
                    current_ram_address_value,
                    addr_to_update.byte_size,
                ]

                if local_item == grinch_items.keys.PROGRESSIVE_VACUUM_TUBE:
                    current_vac_count: int = get_item_count_by_id(ctx, item_received.item)
                    if grinch_item_ram_data.update_ram_addr.index(addr_to_update) +1 >= current_vac_count:
                        break

            self.last_received_index += 1

        # Update the latest received item index to ram as well.
        ram_addr_dict[RECV_ITEM_ADDR] = [self.last_received_index, RECV_ITEM_BITSIZE]

        await bizhawk.write(ctx.bizhawk_ctx, self.convert_dict_to_ram_list(ram_addr_dict))


    async def goal_checker(self, ctx: "BizHawkClientContext"):
        if not ctx.finished_game:
            goal_loc = grinch_locations["MC - Sleigh Ride - Save Christmas"]
            goal_ram_data = goal_loc.update_ram_addr[0]
            current_ram_address_value = int.from_bytes(
                (
                    await bizhawk.read(
                        ctx.bizhawk_ctx,
                        [
                            (
                                goal_ram_data.ram_address,
                                goal_ram_data.byte_size,
                                goal_ram_data.ram_area,
                            )
                        ],
                    )
                )[0],
                goal_ram_data.endian,
            )

            # if (current_ram_address_value & (1 << goal_ram_data.binary_bit_pos)) > 0:
            if current_ram_address_value == goal_ram_data.value:
                ctx.finished_game = True
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "StatusUpdate",
                            "status": NetUtils.ClientStatus.CLIENT_GOAL,
                        }
                    ]
                )

    def convert_dict_to_ram_list(self, addr_dict: dict[int, list[int]]) -> list[tuple[int, Sequence[int], str]]:
        addr_list_to_update: list[tuple[int, Sequence[int], str]] = []

        for key, val in addr_dict.items():
            addr_list_to_update.append((key, val[0].to_bytes(val[1], "little"), "MainRAM"))

        return addr_list_to_update

    # Removes the regional access until you actually received it from AP.
    async def constant_address_update(self, ctx: "BizHawkClientContext"):
        ram_addr_dict: dict[int, list[int]] = {}

        list_recv_itemids: list[int] = [netItem.item for netItem in ctx.items_received]
        items_to_check: dict[str, GrinchItemData] = {
            **KEYS_TABLE,
            **MISSION_ITEMS_TABLE,
            **SLEIGH_TABLE,
            **GADGETS_TABLE,
            **MOVES_TABLE,
        }

        heart_count = len(
            list(
                item_id
                for item_id in list_recv_itemids
                if item_id == 42069 + ALL_ITEMS_TABLE[grinch_items.useful_items.HEART_OF_STONE].id
            )
        )
        has_whoville_vacuum_tube = bool(
            len(
                list(
                    item_id
                    for item_id in list_recv_itemids
                    if item_id == 42069 + ALL_ITEMS_TABLE[grinch_items.keys.WHOVILLE].id
                )
            )
        )
        heart_item_data = ALL_ITEMS_TABLE["Heart of Stone"]
        ram_addr_dict[heart_item_data.update_ram_addr[0].ram_address] = [
            min(heart_count, 4),
            1,
        ]

        # Setting mission count for all addresses back to 0 to prevent warping/unlocking after completing 3 missions
        #
        ram_addr_dict[0x0100F0] = [0, 4]

        for item_name, item_data in items_to_check.items():
            # If item is an event or already been received, ignore.
            if item_data.id is None:  # or GrinchLocation.get_apid(item_data.id) in list_recv_itemids:
                continue

            if item_name == grinch_items.keys.PROGRESSIVE_VACUUM_TUBE and has_whoville_vacuum_tube:
                continue

            # This will either constantly update the item to ensure you still have it or take it away if you don't deserve it
            for addr_to_update in item_data.update_ram_addr:
                is_binary = True if not addr_to_update.binary_bit_pos is None else False

                if is_binary:
                    if addr_to_update.ram_address in ram_addr_dict.keys():
                        current_bin_value = ram_addr_dict[addr_to_update.ram_address][0]

                    else:
                        current_bin_value = int.from_bytes(
                            (
                                await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [
                                        (
                                            addr_to_update.ram_address,
                                            addr_to_update.byte_size,
                                            addr_to_update.ram_area,
                                        )
                                    ],
                                )
                            )[0],
                            addr_to_update.endian,
                        )

                    if GrinchLocation.get_apid(item_data.id) in list_recv_itemids:
                        current_bin_value |= 1 << addr_to_update.binary_bit_pos

                    else:
                        current_bin_value &= ~(1 << addr_to_update.binary_bit_pos)

                    ram_addr_dict[addr_to_update.ram_address] = [current_bin_value, 1]

                else:
                    if GrinchLocation.get_apid(item_data.id) in list_recv_itemids:
                        ram_addr_dict[addr_to_update.ram_address] = [
                            addr_to_update.value,
                            addr_to_update.byte_size,
                        ]

                    else:
                        ram_addr_dict[addr_to_update.ram_address] = [
                            0,
                            addr_to_update.byte_size,
                        ]

                if item_name == grinch_items.keys.PROGRESSIVE_VACUUM_TUBE:
                    current_vac_count: int = get_item_count_by_id(ctx, GrinchItem.get_apid(item_data.id))
                    if item_data.update_ram_addr.index(addr_to_update) + 1 >= current_vac_count:
                        break

        await bizhawk.write(ctx.bizhawk_ctx, self.convert_dict_to_ram_list(ram_addr_dict))

    async def get_current_map_id(self, ctx: "BizHawkClientContext"):
        return int.from_bytes(
            (await bizhawk.read(ctx.bizhawk_ctx, [(0x010000, 1, "MainRAM")]))[0],
            "little",
        )

    async def ingame_checker(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger

        ingame_map_id = await self.get_current_map_id(ctx)

        # If not in game or at a menu, or loading the publisher logos
        # If it is not greater than 0x02 and less than 0x35, you are not in game
        # 0x3E is an exception to allow goaling directly after defeating santa instead of after end credits.
        if ingame_map_id in [0x00, 0x02, 0x35, 0x36, 0x37]:
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(0x08FA20, int(1).to_bytes(1, "little"), "MainRAM")],
            )
            if not self.menu_log:
                print("Currently in menu screen")
                self.menu_log = True
            self.ingame_log = False
            self.cutscene_goo_log = False
            self.demo_log = False
            return False
        else:
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(0x08FA20, int(0).to_bytes(1, "little"), "MainRAM")],
            )

        # If grinch has changed maps
        if not ingame_map_id == self.last_map_location:
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"grinch_region_{ctx.team}_{ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "replace", "value": ingame_map_id}]
            }])
            # If the last "map" we were on was a menu or a publisher logo
            if self.last_map_location in MENU_MAP_IDS:
                # Reset our demo mode checker just in case the game is in demo mode.
                # self.demo_mode_buffer = 0
                print("Changed maps")
                self.ingame_log = False
                self.cutscene_goo_log = False
                self.menu_log = False
                self.demo_log = False
                return False

            # Update the previous map we were on to be the current map.
            self.last_map_location = ingame_map_id

        # Add failsafe for goal region to ensure it is able to trigger goal
        if await self.loading_state(ctx) and not ingame_map_id == 0x3E:
            if not self.cutscene_goo_log:
                print("Currently in cutscene or goo")
                self.cutscene_goo_log = True
            self.ingame_log = False
            self.menu_log = False
            self.demo_log = False
            return False

        # # Use this as a delayed check to make sure we are in game
        # if not self.demo_mode_buffer == MAX_DEMO_MODE_CHECK:
        #     await asyncio.sleep(0.1)
        #     self.demo_mode_buffer += 1
        #     print("Demo mode buffer")
        #     return False

        demo_mode = int.from_bytes(
            (await bizhawk.read(ctx.bizhawk_ctx, [(0x01008A, 1, "MainRAM")]))[0],
            "little",
        )

        if demo_mode == 1:
            if not self.demo_log:
                print("Connected in demo mode, warping back to main menu")
                self.demo_log = True
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(MAP_REGION_ADDR, int(0x00).to_bytes(1, "little"), "MainRAM")],
            )
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(0x08FB94, int(1).to_bytes(1, "little"), "MainRAM")],
            )
            self.ingame_log = False
            self.cutscene_goo_log = False
            self.menu_log = False
            return False

        if not self.ingame_log:
            print("You can now start sending locations from the Grinch!")
            self.ingame_log = True
            self.cutscene_goo_log = False
            self.menu_log = False
            self.demo_log = False

        self.curr_region = await self.get_current_region()
        return True

    async def get_current_region(self) -> str | None:
        for grinch_region, grinch_data in ALL_REGIONS_INFO.items():
            # We only care about a region/map that is the same as the grinch
            if self.last_map_location == grinch_data.map_id:
                return grinch_region
        return None

    async def option_handler(self, ctx: "BizHawkClientContext"):
        ingame_map_id = await self.get_current_map_id(ctx)
        if self.unlimited_eggs:
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(EGG_COUNT_ADDR, MAX_EGGS.to_bytes(EGG_ADDR_BYTESIZE, "little"), "MainRAM")],
            )
            if ingame_map_id in [0x0E, 0x10, 0x0F, 0x12]:
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(NITRO_THISTLE_COUNT_ADDR, int(1).to_bytes(NITRO_THISTLE_BYTESIZE, "little"), "MainRAM")],
                    )
                    await asyncio.sleep(0.5)

        if self.reduced_cutscenes:
            # Disables all Whoville tutorial cutscenes & first visit cutscene
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(0x010212, int(95).to_bytes(1, "little"), "MainRAM")],
            )
            # Disables WF first visit cutscene
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(0x01024A, int(2).to_bytes(1, "little"), "MainRAM")],
            )
            # Disables WD first visit cutscene
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(0x01025C, int(2).to_bytes(1, "little"), "MainRAM")],
            )
            # Disables WL first visit cutscene
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(0x010282, int(16).to_bytes(1, "little"), "MainRAM")],
            )

    async def funny_secret_goal(self, ctx: "BizHawkClientContext"):
        secret_cond = False
        secret_cond_activated = False
        while ctx.slot:
            await asyncio.sleep(0.1)
            if not await self.ingame_checker(ctx):
                continue
            if not secret_cond_activated:
                print("funny goal event activated")
                secret_cond_activated = True
            spin_win_hiscore = int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(0x0100FD, 1, "MainRAM")]))[0],
                    "little",)
            dankamania_hiscore= int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(0x0100FB, 1, "MainRAM")]))[0],
                    "little",)
            gc_race_hiscore = int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(0x0100FC, 1, "MainRAM")]))[0],
                    "little",)
            region = int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(MAP_REGION_ADDR, 1, "MainRAM")]))[0],
                    "little",)

            if 0 < spin_win_hiscore <= 29 and region == 0x1A:
                secret_cond = True
            elif dankamania_hiscore >= 12 and region == 0x1B:
                secret_cond = True
            elif 0 < gc_race_hiscore  <= 29 and region == 0x1C:
                secret_cond = True

            if secret_cond:
                    print("LOL?")
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(MAP_REGION_ADDR, int(0x3E).to_bytes(1, "little"), "MainRAM")],
                    )
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(TRIGGER_PLAYER_TELEPORT, int(1).to_bytes(1, "little"), "MainRAM")],
                    )
                    secret_cond = False

    async def ring_link_output(self, ctx: "BizHawkClientContext"):
        # Sends rings to other worlds
        from CommonClient import logger

        while self.send_ring_link and ctx.slot:
            if not await self.ingame_checker(ctx):
                await asyncio.sleep(0.5)
            try:
                current_egg_count = int.from_bytes(
                    (
                        await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(EGG_COUNT_ADDR, EGG_ADDR_BYTESIZE, "MainRAM")],
                        )
                    )[0],
                    "little",
                )
                # Need asyncio sleep because AP may mandate delayed sends for
                await asyncio.sleep(1)

                if (current_egg_count - self.previous_egg_count) != 0:
                    msg = {
                        "cmd": "Bounce",
                        "data": {
                            "time": time.time(),
                            "source": self.unique_client_id,
                            "amount": current_egg_count - self.previous_egg_count,
                        },
                        "tags": ["RingLink"],
                    }
                    # Need asyncio sleep because AP may mandate delayed sends for
                    await asyncio.sleep(1)

                    await ctx.send_msgs([msg])
                    self.previous_egg_count = current_egg_count
                    # logger.info(f"RingLink: You sent {str(current_egg_count - self.previous_egg_count)} rotten eggs.")

                await asyncio.sleep(0.1)

            except Exception as ex:
                logger.error("While monitoring grinch's egg count ingame, an error occurred. Details:" + str(ex))
                self.send_ring_link = False

        if not ctx.slot:
            logger.info("You must be connected to the multi-world in order for RingLink to work properly.")

    async def ring_link_input(self, egg_amount: int, ctx: "BizHawkClientContext"):
        # Receives rings from other worlds
        from CommonClient import logger
        if not (await self.ingame_checker(ctx) and not self.last_map_location in [0x18, 0x19, 0x1A, 0x1B, 0x1C]):
            return

        game_egg_count = int.from_bytes(
            (await bizhawk.read(ctx.bizhawk_ctx, [(EGG_COUNT_ADDR, EGG_ADDR_BYTESIZE, "MainRAM")]))[0],
            "little",
        )
        non_neg_eggs = game_egg_count + egg_amount if game_egg_count + egg_amount > 0 else 0
        current_egg_count = min(non_neg_eggs, MAX_EGGS)

        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (
                    EGG_COUNT_ADDR,
                    int(current_egg_count).to_bytes(EGG_ADDR_BYTESIZE, "little"),
                    "MainRAM",
                )
            ],
        )

        self.previous_egg_count = current_egg_count
        # logger.info(f"RingLink: You received {str(egg_amount)} rotten eggs.")

    async def update_countdown(self, ctx: "BizHawkClientContext", countdown: int):
        if not await self.ingame_checker(ctx): # If we are not in game, don't try and update the counter in_game.
            return
        elif countdown >= 255 or countdown < 1:
            return
        else:
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(TIMER_ADDR, [countdown], "MainRAM")],
            )

    def _get_uuid(self) -> int:
        string_id = str(uuid.uuid4())
        uid: int = 0
        for char in string_id:
            uid += ord(char)

        return uid

    async def watch_to_teleport_player(self, ctx: "BizHawkClientContext"):
        while ctx.slot:
            if not await self.ingame_checker(ctx):
                await asyncio.sleep(5)
                continue

            # Start button pressed and held is captured at bit 3
            get_start_button_state: int = int.from_bytes(
                (await bizhawk.read(ctx.bizhawk_ctx, [(START_BUTTON_ADDR, BUTTONS_ADDR_SIZE, "MainRAM")]))[0],
                "little",)

            if not (get_start_button_state & (1 << 3)) > 0:
                await asyncio.sleep(1)
                continue

            # Right Bumper pressed and held is captured at bit 3
            # Right Trigger pressed and held is captured at bit 1
            # Left Bumper pressed and held is captured at bit 2
            # Left Trigger pressed and held is captured at bit 0
            get_other_buttons_state: int = int.from_bytes(
                (await bizhawk.read(ctx.bizhawk_ctx, [(OTHER_BUTTON_ADDR, BUTTONS_ADDR_SIZE, "MainRAM")]))[0],
                "little",)

            rb_pressed: bool = (get_other_buttons_state & (1 << 3)) > 0
            rt_pressed: bool = (get_other_buttons_state & (1 << 1)) > 0
            lb_pressed: bool = (get_other_buttons_state & (1 << 2)) > 0
            lt_pressed: bool = (get_other_buttons_state & (1 << 0)) > 0

            # If RT and LT are both held + start, sending player up to the top of MC / Tutorial area.
            if await self.paused_state(ctx):
                if rt_pressed and lt_pressed:
                    lobby_val = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(LOBBY_TRIGGER_ADDR,
                        TRIGGER_ADDR_SIZE, "MainRAM")]))[0],"little")
                    lobby_val = set_binary_position(lobby_val, 0, False)
                    await asyncio.sleep(1)
                    await bizhawk.write(ctx.bizhawk_ctx,
                        [(LOBBY_TRIGGER_ADDR, lobby_val.to_bytes(TRIGGER_ADDR_SIZE, "little"), "MainRAM"),
                                (MC_ELEVATOR_ADDR, int(3).to_bytes(TRIGGER_ADDR_SIZE, "little"), "MainRAM"),])
                    await _teleport_player(ctx, MOUNT_CRUMPIT_MAP_ID)

                # If RB and LB are both held + start, sending player to grinch computer room / lobby.
                if lb_pressed and rb_pressed:
                    lobby_val = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(LOBBY_TRIGGER_ADDR,
                        TRIGGER_ADDR_SIZE, "MainRAM")]))[0], "little")
                    lobby_val = set_binary_position(lobby_val, 0, True)
                    await asyncio.sleep(1)
                    await bizhawk.write(ctx.bizhawk_ctx,
                        [(LOBBY_TRIGGER_ADDR, lobby_val.to_bytes(TRIGGER_ADDR_SIZE, "little"), "MainRAM"),
                                (MC_ELEVATOR_ADDR, int(1).to_bytes(TRIGGER_ADDR_SIZE, "little"), "MainRAM")])
                    await _teleport_player(ctx, MOUNT_CRUMPIT_MAP_ID)

                continue

    async def check_grinch_alive(self, ctx: "BizHawkClientContext"):
        reg_name = await self.get_current_region()
        if not reg_name:
            return
        elif self.is_grinch_dead:
            return

        curr_region_data = ALL_REGIONS_INFO[reg_name]
        if not curr_region_data.allow_deathlink:
            return

        death_cutscene: int = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx,
                                                              [(curr_region_data.map_table_addr + DEATHLINK_CHECK_OFFSET,
                                                                1, "MainRAM")]))[0], "little")

        loading_goo: int = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx,
                                                                 [(0x010094, 1, "MainRAM")]))[0], "little")

        if not await self.paused_state(ctx) and death_cutscene == 2 and not self.is_grinch_dead:
            self.is_grinch_dead = True
            await ctx.send_death(ctx.player_names[ctx.slot] + " could not fight off the Christmas cheer...")
            await self.kill_grinch(ctx)

    async def kill_grinch(self, ctx: "BizHawkClientContext"):
        reg_name = await self.get_current_region()
        if not (await self.ingame_checker(ctx) and reg_name):
            return

        curr_region_data = ALL_REGIONS_INFO[reg_name]
        if not curr_region_data.allow_deathlink:
            return

        if await self.paused_state(ctx): # or await self.loading_state(ctx):
            return

        # Update the Health Address to X amount and DeathLink Trigger to 0
        self.is_grinch_dead = True
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(curr_region_data.map_table_addr + HEALTH_REGION_OFFSET, int(0).to_bytes(1, "little"), "MainRAM"),],
        )
        death_init_val: int = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx,
        [(curr_region_data.map_table_addr + DEATHLINK_REGION_OFFSET, 1, "MainRAM")]))[0], "little")
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(curr_region_data.map_table_addr + DEATHLINK_REGION_OFFSET, int(death_init_val+0x40).to_bytes(1, "little"), "MainRAM"),],
        )

        await self.wait_for_grinch_alive(ctx)

    async def adjust_damage_rate(self, ctx: "BizHawkClientContext"):
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(DAMAGE_RATE_ADDR, self.damage_rate.to_bytes(1, "little"), "MainRAM")]
        )

    async def wait_for_grinch_alive(self, ctx: "BizHawkClientContext"):
        curr_region_data = ALL_REGIONS_INFO[await self.get_current_region()]

        death_cutscene: int = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx,
        [(curr_region_data.map_table_addr + DEATHLINK_CHECK_OFFSET,
                                                                      1, "MainRAM")]))[0], "little")

        while death_cutscene == 2 and not await self.paused_state(ctx):
            await asyncio.sleep(3.0)
            death_cutscene: int = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx,
                                                                     [(
                                                                          curr_region_data.map_table_addr + DEATHLINK_CHECK_OFFSET,
                                                                          1, "MainRAM")]))[0], "little")

        self.is_grinch_dead = False

    async def loading_state(self, ctx: "BizHawkClientContext"):
        loading_goo: int = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx,
                [(0x010094, 1, "MainRAM")]))[0], "little")
        in_cutscene: int = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx,
                [(0x01009E, 1, "MainRAM")]))[0], "little")
        # This function returns true if the player currently has the loading goo or is in a cutscene
        return loading_goo == 0 or in_cutscene > 0


    async def paused_state(self, ctx: "BizHawkClientContext"):
        is_game_paused: int = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx,
                [(0x0952A5, 1, "MainRAM")]))[0], "little")
        # This function returns true if the player is paused
        return is_game_paused > 0

    async def randomize_music(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        # While you are connected to AP and the player is not trying to close the client
        while ctx.slot:
            if not await self.ingame_checker(ctx): #or await self.paused_state(ctx) or await self.loading_state(ctx)):
                # await asyncio.sleep(5)
                continue

            current_region: str = await self.get_current_region()
            if not current_region or not ALL_REGIONS_INFO[current_region].allow_music_rando:

                await asyncio.sleep(10)
                continue
            current_song_id: int = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx,
                                                               [(LOOP_BACK_ADDR, SONG_ADDR_SIZE, "MainRAM")]))[0], "little")

            region_music: int = self.chosen_music[current_region]
            # logger.info(region_music)
            if region_music != current_song_id:
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [(STARTING_SONG_ADDR, region_music.to_bytes(SONG_ADDR_SIZE, "little"), "MainRAM"),],
                )
            else:
                await asyncio.sleep(5)
                continue

def _cmd_ringlink(self):
    """Toggle ringling from client. Overrides default setting."""
    if not self.ctx.slot:
        return

    Utils.async_start(
        _update_ring_link(self.ctx, not "RingLink" in self.ctx.tags),
        name="Update RingLink",
    )

def _cmd_deathlink(self):
    """Toggle deathlink from client. Overrides default setting."""
    from worlds._bizhawk.context import BizHawkClientContext
    if isinstance(self.ctx, BizHawkClientContext):
        Utils.async_start(self.ctx.update_death_link(not "DeathLink" in self.ctx.tags), name="Grinch - Update Deathlink")

async def _update_ring_link(ctx: "BizHawkClientContext", ring_link: bool):
    """Helper function to set Ring Link connection tag on/off and update the connection if already connected."""
    old_tags = copy.deepcopy(ctx.tags)

    if ring_link:
        ctx.tags.add("RingLink")
    else:
        ctx.tags -= {"RingLink"}

    if old_tags != ctx.tags and ctx.server and not ctx.server.socket.closed:
        await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

async def _teleport_player(ctx: "BizHawkClientContext", map_id: int):
    await bizhawk.write(
        ctx.bizhawk_ctx,
        [(MAP_REGION_ADDR, map_id.to_bytes(TRIGGER_ADDR_SIZE, "little"), "MainRAM"),
        (TRIGGER_PLAYER_TELEPORT, int(1).to_bytes(TRIGGER_ADDR_SIZE, "little"), "MainRAM"),
        (DISGUISE_OFF_ADDR, int(0).to_bytes(TRIGGER_ADDR_SIZE, "little"), "MainRAM"),
         (TIMER_ADDR, int(0).to_bytes(TRIGGER_ADDR_SIZE, "little"), "MainRAM"),],
    )

# TODO remove these in favor of Art's refactor. Use GrinchRamData going forward.
def check_binary_position(value_to_check: int, binary_position: int) -> bool:
    return (value_to_check & (1 << binary_position)) > 0

def set_binary_position(value_to_check: int, binary_position: int, turn_on: bool) -> int:
    if turn_on:
        return value_to_check | 1 << binary_position
    else:
        return value_to_check & ~(1 << binary_position)

def get_item_count_by_id(ctx: "BizHawkClientContext", item_id: int) -> int:
    return len([netItem for netItem in ctx.items_received if netItem.item == item_id])