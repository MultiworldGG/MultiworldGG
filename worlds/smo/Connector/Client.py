import asyncio
import functools
import typing
from copy import deepcopy

import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"
from NetUtils import encode, NetworkPlayer, NetworkItem, JSONtoTextParser, JSONMessagePart, ClientStatus
from MultiServer import Endpoint
from CommonClient import get_base_parser, gui_enabled, logger, CommonContext, ClientCommandProcessor
from typing import List, Any
from .Packets import PacketHeader, PacketType, Packet, ItemType

from .Data import inverse_shop_items, shop_items, get_item_type, worlds, world_alias, valid_warps, inverse_worlds, \
    multi_moon_locations, world_prefixes
from .Player import SMOPlayer

import traceback

message_types = [
    "ItemSend",
    "Hint",
    "Join",
    "Part",
    "Chat"
]

class SMOJSONToTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)  # No colors for the in-game text

# Add Debug Commands like send_to and shine, etc
class SMOCommandProcessor(ClientCommandProcessor):
    def _cmd_smo(self):
        """Check SMO Connection State"""
        if isinstance(self.ctx, SMOContext):
            logger.info(f"SMO Status: {self.ctx.get_smo_status()}")

    def _cmd_sync(self):
        """Attempt to resync received items"""
        if isinstance(self.ctx, SMOContext):
            logger.info(f"SMO Status: Syncing")
            self.ctx.player_data.item_index = 0
            self.ctx.server_msgs.append({"cmd" : "Sync"})
            # Add the sending locations part here if necessary.

    def _cmd_warp(self, kingdom : str, scenario : int = -1):
        """Warp Mario to another kingdom.
        Change kingdom scenario only if you know what you're doing as it can break the game."""
        if isinstance(self.ctx, SMOContext):
            while kingdom.lower() in world_alias:
                kingdom = world_alias[kingdom]
            if not kingdom in valid_warps:
                warps : str = ""
                for value in valid_warps.values():
                    warps += value + ", "
                warps = warps.removesuffix(", ")
                logger.info(f"{kingdom} is not a valid warp.\nValid warps: {warps}")
            else:
                logger.info(f"Sending Mario to {valid_warps[kingdom]}")
                self.ctx.player_data.add_message(f"Sending Mario to {valid_warps[kingdom]}")
                self.ctx.proxy_msgs.append(Packet(guid=self.ctx.proxy_guid, packet_type=PacketType.ChangeStage,
                                                 packet_data=[kingdom, scenario]))

    # def _cmd_unlock(self, kingdom : int, scenario : int = -1):
    #     if isinstance(self.ctx, SMOContext):
    #         logger.info(f"Unlocking Kingdom {kingdom}")
    #         self.ctx.player_data.add_message(f"Kingdom Unlocked")
    #         self.ctx.proxy_msgs.append(Packet(guid=self.ctx.proxy_guid, packet_type=PacketType.Progress,
    #                                       packet_data=[kingdom, scenario]))

# Change send message and related calls to send packet and serialize and deserialize using the packet of the respective packet type.
# Make sure to receive packets on the connection to send checks through to the AP Server from this client.

class SMOContext(CommonContext):
    command_processor = SMOCommandProcessor
    game = "Super Mario Odyssey"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.proxy : asyncio.Server
        self.proxy_chat = None
        self.gamejsontotext = SMOJSONToTextParser(self)
        self.autoreconnect_task = None
        self.endpoint = None
        self.items_handling = 0b111
        self.room_info = None
        self.connected_msg = None
        self.game_connected : bool = False
        self.awaiting_info : bool = False
        self.full_inventory: List[Any] = []
        self.server_msgs: List[Any] = []
        self.server_comm_task = None
        self.proxy_msgs : List[Packet] = []
        self.proxy_guid : bytearray = bytearray()
        self.player_data : SMOPlayer = SMOPlayer()
        self.player = None
        self.slot_data : dict = {}
        #self.checked_locations : set
        self.ping_task = None
        self.awaiting_connection : bool = False
        self.disconnect_timer : int = 120
        self.logged_in : bool = False
        self.multi_moon_anim : bool = False
        self.death_link_enabled : bool = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(SMOContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def get_smo_status(self) -> str:
        if not self.game_connected:
            return "Not connected to Super Mario Odyssey"

        return "Connected to Super Mario Odyssey"

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)

    async def disconnect_proxy(self):
        if self.endpoint and not self.endpoint.socket.closed:
            await self.endpoint.socket.close()

    def is_connected(self) -> bool:
        return self.server and self.server.socket.open

    # Handle APChatMessage here
    def on_print_json(self, args: dict):
        text = self.gamejsontotext(deepcopy(args["data"]))
        if "type" in args and args["type"] in message_types:
            self.player_data.add_message(text)

        if self.ui:
            self.ui.print_json(args["data"])
        else:
            text = self.jsontotextparser(args["data"])
            logger.info(text)

    def update_items(self):
        # just to be safe - we might still have an inventory from a different room
        if not self.is_connected():
            return

        self.server_msgs.append({"cmd": "ReceivedItems", "index": 0, "items": self.full_inventory})

    def forward_slot_data(self):
        """
        Forwards Slot Data from Archipelago Lobby connection to SMO
        :return:
        """
        #print(self.slot_data)
        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.SlotData,
              packet_data=[self.slot_data["counts"]["cascade"],
                           self.slot_data["counts"]["sand"],
                           self.slot_data["counts"]["wooded"], self.slot_data["counts"]["lake"],
                           self.slot_data["counts"]["lost"], self.slot_data["counts"]["metro"],
                           self.slot_data["counts"]["seaside"],
                           self.slot_data["counts"]["snow"],
                           self.slot_data["counts"]["luncheon"],
                           self.slot_data["counts"]["ruined"],
                           self.slot_data["counts"]["bowser"], self.slot_data["counts"]["dark"],
                           self.slot_data["counts"]["darker"],
                           self.slot_data["regionals"], self.slot_data["capture_sanity"]]))



        # Games
        for i in range(0, len(self.slot_data["shop_games"]), 3):
            if i + 3 < len(self.slot_data["shop_games"]):
        #        print(self.slot_data["shop_games"][i:i + 3])
                self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
                                              packet_data=[0, i, i+1, i+2, self.slot_data["shop_games"][i:i + 3]]))
            else:
        #        print(self.slot_data["shop_games"][i:i + 3])
                self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
                                              packet_data=[0, i, i+1, i+2, self.slot_data["shop_games"][
                                                              i:len(self.slot_data["shop_games"])]]))
        # Players
        for i in range(0, len(self.slot_data["shop_players"]), 3):
            if i + 3 < len(self.slot_data["shop_players"]):
                #print(self.slot_data["shop_players"][i:i + 3])
                self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
                                              packet_data=[1, i, i+1, i+2, self.slot_data["shop_players"][i:i + 3]]))
            else:
                #print(self.slot_data["shop_players"][i:i + 3])
                self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
                                              packet_data=[1, i, i+1, i+2, self.slot_data["shop_players"][
                                                              i:len(self.slot_data["shop_players"])]]))
        # Items
        for i in range(0, len(self.slot_data["shop_ap_items"]), 3):
            if i + 3 < len(self.slot_data["shop_ap_items"]):
                #print(self.slot_data["shop_ap_items"][i:i + 3])
                self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
                                              packet_data=[2, i, i+1, i+2, self.slot_data["shop_ap_items"][i:i + 3]]))
            else:
                #print(self.slot_data["shop_ap_items"][i:i + 3])
                self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
                                              packet_data=[2, i, i+1, i+2, self.slot_data["shop_ap_items"][
                                                              i:len(self.slot_data["shop_ap_items"])]]))

        items = []
        for i in range(2501, 2539):
            if str(i) in self.slot_data["shop_replace_data"]["caps"]:
                items.append(self.slot_data["shop_replace_data"]["caps"][str(i)])
            else:
                items.append([254,254,254,254])
        for i in range(2577, 2582):
            if str(i) in self.slot_data["shop_replace_data"]["caps"]:
                items.append(self.slot_data["shop_replace_data"]["caps"][str(i)])
            else:
                items.append([254,254,254,254])

        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace, packet_data=[0, items]))
        #print(len(items), items)

        items = []
        for i in range(2539, 2582):
            if str(i) in self.slot_data["shop_replace_data"]["clothes"]:
                items.append(self.slot_data["shop_replace_data"]["clothes"][str(i)])
            else:
                items.append([254,254,254,254])
        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace, packet_data=[1, items]))
        #print(len(items), items)

        items = []
        for i in range(2582, 2599):
            if str(i) in self.slot_data["shop_replace_data"]["stickers"]:
                items.append(self.slot_data["shop_replace_data"]["stickers"][str(i)])
            else:
                items.append([254,254,254,254])
        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace, packet_data=[2, items]))

        items = []
        for i in range(2599, 2625):
            if str(i) in self.slot_data["shop_replace_data"]["souvenirs"]:
                items.append(self.slot_data["shop_replace_data"]["souvenirs"][str(i)])
            else:
                items.append([254,254,254,254])
        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace, packet_data=[3, items]))

        items = []
        for i in range(0, 2499):
            if str(i) in self.slot_data["shop_replace_data"]["moons"]:
                items.append(self.slot_data["shop_replace_data"]["moons"][str(i)])
        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace, packet_data=[4, items]))

        # Colors
        print(self.slot_data["shine_colors"])
        data = [[]]
        for shine_uid in range(0, 1168):
            if len(data[-1]) == 51:
                data.append([])
            if shine_uid > 1167:
                break
            if str(shine_uid) in self.slot_data["shine_colors"]:
                data[-1].append([shine_uid, self.slot_data["shine_colors"][str(shine_uid)]])
        print(data)
        for i in data:
            self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShineColor,
                                          packet_data=[i]))
            #print(self.proxy_msgs[-1].packet.info)

        # Checked locations
        data = [[]]
        for loc in self.checked_locations:
            if len(data[-1]) == 100:
                data.append([])
            if loc < 1167:
                data[-1].append(loc)
        for i in data:
            self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShineChecks,
                                              packet_data=[i]))

    def forward_shine_data(self):
        world_id = world_prefixes.index(self.player_data.current_home_stage)
        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShineReplace,
                                         packet_data=[self.slot_data["shine_replace_data"][str(world_id)]]))
        # Items
        #print(self.slot_data["shine_replace_data"][str(world_id)])
        for i in range(0, len(self.slot_data["shine_items"][str(world_id)]), 3):
            if i + 3 < len(self.slot_data["shine_items"][str(world_id)]):
                #print(self.slot_data["shine_items"][str(world_id)][i:i + 3])
                self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
                                             packet_data=[3, i, i + 1, i + 2,
                                                          self.slot_data["shine_items"][str(world_id)][
                                                          i:i + 3]]))
            else:
                #print(self.slot_data["shine_items"][str(world_id)][i:i + 3])
                self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
                                             packet_data=[3, i, i + 1, i + 2,
                                                          self.slot_data["shine_items"][str(world_id)][
                                                          i:len(
                                                              self.slot_data["shine_items"][str(world_id)])]]))

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        if self.death_link_enabled:
            super().on_deathlink(data)
            death_link_packet : Packet = Packet(guid=self.proxy_guid, packet_type=PacketType.DeathLink)
            self.proxy_msgs.append(death_link_packet)
            self.last_death_link = data["time"]

    # Handle sending packets to SMO here
    def on_package(self, cmd: str, args: dict):
        match cmd:
            case "Connected":
                json = args
                me: NetworkPlayer
                if "slot_info" in json.keys():
                    json["slot_info"] = {}
                if "players" in json.keys():

                    for n in json["players"]:
                        if n.slot == json["slot"] and n.team == json["team"]:
                            me = n
                            break

                    # Only put our player info in there as we actually need it
                    json["players"] = [me]
                    self.slot_data = json["slot_data"]
                    #self.checked_locations = json["checked_locations"]
                self.player = me
                self.player_data.add_message(f"Connected to {apname} as {me.name} playing Super Mario Odyssey")
                # Send slot data to SMO
                self.forward_slot_data()
                self.player_data.goal = self.slot_data["goal"]
                self.death_link_enabled = self.slot_data["death_link"]
                self.logged_in = True

                if self.death_link_enabled:
                    self.server_msgs.append({"cmd" : "ConnectUpdate", "tags" : ["AP", "DeathLink"]})
                self.server_msgs.append({"cmd" : "Get", "keys" : [f"{self.player.name}_scenarios"]})
                # if DEBUG:
                #     print(json)
                self.connected_msg = encode([json])
                if self.awaiting_info:
                    self.server_msgs.append(self.room_info)
                    self.update_items()
                    self.awaiting_info = False

            case "RoomUpdate":
                # Same story as above
                json = args
                if "players" in json.keys():
                    json["players"] = []

                self.server_msgs.append(json)

            case "ReceivedItems":
                # Handle Sending various collect packets to SMO here
                if self.multi_moon_anim:
                    return


                if args["index"] == 0:
                    self.full_inventory.clear()
                    # not sure if this is needed?
                    self.player_data.reset_moons()
                    self.player_data.item_index = 0
                    print("Accept full inventory.")

                if args["index"] != self.player_data.item_index:
                    print("Next index mismatch, syncing.")
                    self.server_msgs.append({"cmd" : "Sync"})
                else:
                    self.player_data.item_index += 1

                for item in args["items"]:
                    net_item = NetworkItem(*item)
                    self.full_inventory.append(net_item)

                    packet = None
                    item_type = get_item_type(net_item.item)
                    index = args["index"]
                    match item_type:
                        # Moons
                        case -1:
                            next_moon : int = self.player_data.get_next_moon(net_item.item)
                            if next_moon > -1:
                                packet = Packet(guid=self.proxy_guid, packet_type=PacketType.Check,
                                    packet_data=[next_moon, ItemType.Moon, index, "", "", 0])
                            else:
                                logger.info(f"Received nonexistent moon. This is either caused by a bug or the use of commands to give"
                                            f" this slot more of a type of moon than can possibly exist.")
                        # Regional Coins
                        case 4:
                            pass
                        # Captures
                        case 5:
                            packet = Packet(guid=self.proxy_guid, packet_type=PacketType.Check,
                                            packet_data=[net_item.item - 3701, ItemType.Capture, index, "", "", 0])
                        # Filler
                        case -2:
                            if str(net_item.location) in self.slot_data["coin_values"][str(net_item.player)]:
                                packet = Packet(guid=self.proxy_guid, packet_type=PacketType.Check,
                                    packet_data=[net_item.item, ItemType.Coins, index, "", "", self.slot_data["coin_values"][str(net_item.player)][str(net_item.location)]])
                            else:
                                print(net_item.player, "location id", print(net_item.location))
                        # Flag items
                        case -4:
                            pass

                        case 0:
                            packet = Packet(guid=self.proxy_guid, packet_type=PacketType.Check,
                                packet_data=[net_item.item - 2538, ItemType.Clothes, index, "", "", 0])

                        case 1:
                            packet = Packet(guid=self.proxy_guid, packet_type=PacketType.Check,
                                packet_data=[(net_item.item - 2500) if net_item.item < 2539 else (net_item.item - 2538), ItemType.Cap, index, "", "", 0])

                        case 2:
                            packet = Packet(guid=self.proxy_guid, packet_type=PacketType.Check,
                                packet_data=[net_item.item - 2599, ItemType.Souvenir, index, "", "", 0])

                        case 3:
                            packet = Packet(guid=self.proxy_guid, packet_type=PacketType.Check,
                                packet_data=[net_item.item - 2582, ItemType.Sticker, index, "", "", 0])

                        # case _:
                        #     internal_name = inverse_shop_items[net_item.item].removesuffix("Cap").removesuffix("Clothes")
                        #     print(inverse_shop_items[net_item.item])
                        #     print(internal_name)
                        #     print(get_item_type(net_item.item))
                        #     packet = Packet(guid=self.proxy_guid, packet_type=PacketType.Item,
                        #                     packet_data=[internal_name, get_item_type(net_item.item)])
                    if packet:
                        if packet.header.packet_type == PacketType.Check:
                            if packet.packet.location_id < 0:
                                logger.info("Invalid Location ID in packet.")
                            else:
                                self.proxy_msgs.append(packet)
                        else:
                            self.proxy_msgs.append(packet)

                self.server_msgs.append(args)

            case "RoomInfo":
                self.seed_name = args["seed_name"]
                self.room_info = args

            case "Retrieved":
                pass
                # if f"{self.player.name}_scenarios" in args["keys"] and args["keys"][f"{self.player.name}_scenarios"] is dict:
                #     for key in self.player_data.world_scenarios.keys():
                #         if self.player_data.world_scenarios[key] <= args["keys"][f"{self.player.name}_scenarios"][key]:
                #             self.player_data.world_scenarios[key] = args["keys"][f"{self.player.name}_scenarios"][key]
                #     #for world in self.player_data.world_scenarios.keys():
                #         #self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.Progress,
                #         #                             packet_data=[inverse_worlds[world], self.player_data.world_scenarios[world]]))
                #         #pass
                #
                #     self.server_msgs.append({"cmd": "Set", "key": f"{self.player.name}_scenarios",
                #                              "operations": [
                #                                  {"operation": "replace", "value": self.player_data.world_scenarios}]})
                # else:
                #     self.server_msgs.append({"cmd" : "Set", "key" : f"{self.player.name}_scenarios",
                #                             "operations" : [{ "operation" : "replace", "value" : self.player_data.world_scenarios}]})

            case _:
                if cmd != "PrintJSON":
                    self.server_msgs.append(args)

    def run_gui(self):
        from kvui import GameManager

        class SMOManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = f"{apname} Super Mario Odyssey Client"

        self.ui = SMOManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

async def ping_loop(ctx : SMOContext):
    while not ctx.exit_event.is_set():
        if ctx.endpoint:
            if ctx.disconnect_timer == 0:
                ctx.game_connected = False
            ctx.disconnect_timer = 1
        await asyncio.sleep(1.0)



async def proxy_chat(ctx : SMOContext):
    try:
        clear_msgs : bool = False
        while not ctx.exit_event.is_set():
            if (len(ctx.player_data.messages) > 0 or clear_msgs) and ctx.game_connected:
                msg_packet : Packet = Packet(guid=ctx.proxy_guid, packet_type=PacketType.ArchipelagoChat,
                                             packet_data=[ctx.player_data.next_messages()])
                ctx.proxy_msgs.append(msg_packet)
                if len(ctx.player_data.messages) == 0 and not clear_msgs:
                    clear_msgs = True
                else:
                    clear_msgs = False
            if ctx.multi_moon_anim:
                await asyncio.sleep(27.0)
                ctx.multi_moon_anim = False
                ctx.server_msgs.append({"cmd": "Sync"})


            else:
                await asyncio.sleep(5.0)
    except Exception as e:
        logger.exception(e)


async def handle_proxy(reader : asyncio.StreamReader, writer : asyncio.StreamWriter, ctx : SMOContext) -> None:
    data : bytearray
    packet : Packet
    ctx.endpoint = Endpoint(writer.transport.get_extra_info("socket"))
    ctx.awaiting_connection = True
    try:
        while True:
            data : bytearray = bytearray(await reader.read(PacketHeader.SIZE))
            packet = Packet(guid=ctx.proxy_guid, header_bytes=data)
            if len(ctx.proxy_guid) == 0:
                if len(packet.header.guid) != 0:
                    ctx.proxy_guid = packet.header.guid
                    if len(ctx.proxy_msgs) > 0:
                        for queued_packet in ctx.proxy_msgs:
                            if queued_packet.header.guid == "None":
                                queued_packet.header.guid = ctx.proxy_guid

            packet_size : int = packet.header.packet_size.value
            data = bytearray(await reader.read(packet_size))
            packet.deserialize(data)

            if packet.header.packet_type != PacketType.Unknown:
                ctx.disconnect_timer = 30
                # Prevent appending server message before connected to server.
            match packet.header.packet_type:
                case PacketType.Connect:
                    if ctx.proxy_guid != packet.header.guid:
                        ctx.proxy_guid = packet.header.guid
                    init_packet = Packet(guid=ctx.proxy_guid, packet_type=PacketType.Init)
                    # Insert init packet at 0 in queue so other packets added before aren't dropped.
                    ctx.proxy_msgs.insert(0, init_packet)
                    # Only log initial connection
                    logger.info("SMO Connected")
                    if ctx.awaiting_connection:
                        ctx.awaiting_connection = False
                        ctx.game_connected = True
                    needs_slot_data : bool = True
                    for queued_packet in ctx.proxy_msgs:
                        if queued_packet.header.packet_type == PacketType.SlotData:
                            needs_slot_data = False
                            break
                    if len(ctx.slot_data) > 0 and needs_slot_data:
                        ctx.forward_slot_data()
                        if ctx.player_data.current_home_stage in world_prefixes:
                            ctx.forward_shine_data()
                    ctx.server_msgs.append({"cmd": "Sync"})

                case PacketType.Disconnect:
                    ctx.game_connected = False
                    break

                case PacketType.ChangeStage:
                    stage : str = packet.packet.stage
                    if stage[0:stage.index("World")] != ctx.player_data.current_home_stage:
                        ctx.player_data.current_home_stage = stage[0:stage.index("World")]
                        print(f"Player Changed Home Stage to {ctx.player_data.current_home_stage}")

                        if ctx.is_connected() and ctx.player_data.current_home_stage in world_prefixes:
                            ctx.forward_shine_data()

                case PacketType.Check:
                    print(packet.packet.location_id, packet.packet.item_type)
                    location_id = packet.packet.location_id
                    item_type : int = packet.packet.item_type.value
                    match item_type:
                        case -1:
                            shine_id: int = packet.packet.location_id
                            print(f"Got {shine_id}")
                            if shine_id in multi_moon_locations:
                                ctx.multi_moon_anim = True
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations" : [shine_id]})
                            if ctx.player_data.check_goal(shine_id):
                                ctx.server_msgs.append({"cmd" : "StatusUpdate", "status" : ClientStatus.CLIENT_GOAL})
                                print("Goal achieved")
                        case 0:
                            print(f"Got Clothes {location_id}")
                            location_id = packet.packet.location_id + 2538
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})
                        case 1:
                            print(f"Got Cap {location_id}")
                            location_id = (packet.packet.location_id + 2500) if packet.packet.location_id < 39 else (2538 + packet.packet.location_id)
                            print(f"Got adjusted Cap {location_id}")
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})
                        case 2:
                            print(f"Got Souvenir {location_id}")
                            location_id = packet.packet.location_id + 2599
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})
                        case 3:
                            print(f"Got Sticker {location_id}")
                            location_id = packet.packet.location_id + 2582
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})
                        case 5:
                            print(f"Got Capture {location_id}")
                            location_id = packet.packet.location_id + 3701
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})
                        # Add Regional Coin

                case PacketType.DeathLink:
                    if ctx.death_link_enabled:
                        await ctx.send_death()

            if len(ctx.proxy_msgs) > 0 and ctx.game_connected:
                # num_bytes = 0
                # packets = 0
                # for i in ctx.proxy_msgs:
                #     num_bytes += 20
                #     num_bytes += i.packet.SIZE
                #     if num_bytes < 4096:
                #         packets += 1


                #print(num_bytes)
                #print(packets)
                packet_send_offset : int = 0
                for i in range(len(ctx.proxy_msgs)):
                    if ctx.proxy_msgs[0].header.packet_type == PacketType.Check and ctx.player_data.current_home_stage == "":
                        packet_send_offset += 1
                        #print("Skipping packet cannot be sent now")
                        continue
                    response : Packet = ctx.proxy_msgs.pop(packet_send_offset)
                    b = response.serialize()
                    # if response.header.packet_type == PacketType.ShineColor:
                    #     print("This one", b[20:])
                    writer.write(b)
                    await writer.drain()
                    if response.header.packet_type == PacketType.Connect:
                        await asyncio.sleep(5.0)


                    # for message in ctx.proxy_msgs:
                    #     print(message.header.packet_type)
                #await asyncio.sleep(0.25)

            if not ctx.game_connected and not ctx.awaiting_connection:
                break
    except Exception as e:
        print("Connection Error ", e)
        traceback.print_exc()
        ctx.player_data.item_index = 0
        ctx.player_data.current_home_stage = ""
        ctx.awaiting_connection = True
        writer.close()


async def comm_loop(ctx : SMOContext):
    while not ctx.exit_event.is_set():
        if not ctx.is_connected():
            ctx.logged_in = False
        if len(ctx.server_msgs) > 0 and ctx.logged_in:
            await ctx.send_msgs(ctx.server_msgs)
            ctx.server_msgs.clear()
        await asyncio.sleep(0.1)


def launch(*launch_args: str):
    async def main():
        parser = get_base_parser()
        args = parser.parse_args(launch_args)

        ctx = SMOContext(args.connect, args.password)
        logger.info("Starting Super Mario Odyssey proxy server")

        ctx.proxy = asyncio.start_server(functools.partial(handle_proxy, ctx=ctx), "0.0.0.0", 1027)
        ctx.proxy_chat = asyncio.create_task(proxy_chat(ctx) , name="ChatLoop")
        ctx.ping_task = asyncio.create_task(ping_loop(ctx), name="PingLoop")
        ctx.server_comm_task = asyncio.create_task(comm_loop(ctx), name="CommLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.proxy
        await ctx.proxy_chat
        await ctx.ping_task
        await ctx.server_comm_task
        # Make ping task wait 1-second intervals
        # Add counter member to ctx
        # if packet of any kind is read from stream,
        # reset counter to 5
        # if counter is 0 when ping task runs,
        # send ping packet to SMO reset counter, set awaiting_ping member of ctx true
        # when ping packet received, set awaiting_ping to false
        # if counter reaches 0 and awaiting_ping is true,
        # set game_connected to false.
        # test without ping packet to see if enough packets
        # saturate the stream to keep connection open with Mario idle
        # if not then implement the above.

        await ctx.exit_event.wait()


    Utils.init_logging("SMOClient")
    # options = Utils.get_options()

    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()