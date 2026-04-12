from __future__ import annotations

import collections
import copy
import logging
import asyncio
import urllib.parse
import colorama
import typing
import time
import functools
import warnings
import sys
import ModuleUpdate
from typing import Optional

ModuleUpdate.update()
from tkinter import filedialog
import websockets
import Utils
import struct
import math
import subprocess

from CommonClient import (
    CommonContext,
    ClientCommandProcessor,
    get_base_parser,
    logger,
    server_loop,
    gui_enabled,
)

if __name__ == "__main__":
    Utils.init_logging("TextClient", exception_logger="Client")

from MultiServer import CommandProcessor
from NetUtils import (Endpoint, decode, NetworkItem, encode, JSONtoTextParser, ClientStatus, Permission, NetworkSlot,
                      RawJSONtoTextParser, add_json_text, add_json_location, add_json_item, JSONTypes,
                      SlotType)  # HintStatus
from Utils import Version, stream_input, async_start, ByValue
from worlds import network_data_package, AutoWorldRegister
import os
import ssl
import enum

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

class HintStatus(ByValue, enum.IntEnum):
    HINT_UNSPECIFIED = 0
    HINT_NO_PRIORITY = 10
    HINT_AVOID = 20
    HINT_PRIORITY = 30
    HINT_FOUND = 40


if typing.TYPE_CHECKING:
    import kvui
    import argparse

logger = logging.getLogger("Client")

# without terminal, we have to use gui mode
gui_enabled = not sys.stdout or "--nogui" not in sys.argv


@Utils.cache_argsless
def get_ssl_context():
    import certifi
    return ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())


class SRB2ClientCommandProcessor(ClientCommandProcessor):
    def _cmd_dummy(self):
        """This is a surprise tool that will help us later"""
        return



class SRB2Context(CommonContext):

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)
        self.slot = 0
        self.game = "Sonic Robo Blast 2"
        self.missing_checks = None
        self.prev_found = None
        self.location_ids = None
        self.seed_name = None
        self.activate_death: bool = False
        self.last_death_link = None
        self.death_link: float = time.time()
        self.death_link_lockout: float = time.time()
        self.ring_link: bool = False
        self.previous_rings = 0
        self.ring_link_rings = 0
        self.goal_type: int = 0
        self.bcz_emblems: int = 0
        self.goal_type = 0
        self.actsanity = False
        self.matchmaps = None
        self.items_handling = 0b001 | 0b010 | 0b100  # Receive items from other worlds, starting inv, and own items
        self.location_name_to_ap_id = None
        self.location_ap_id_to_name = None
        self.item_name_to_ap_id = None
        self.item_ap_id_to_name = None
        self.prev_found = []
        self.texttransfer = []
        self.locations_checked = set()  # local state
        self.locations_scouted = set()
        self.items_received = []
        self.missing_locations = set()  # server state
        self.checked_locations = set()  # server state
        self.server_locations = set()  # all locations the server knows of, missing_location | checked_locations
        self.locations_info = {}


        #default settings to be overwritten in connected


    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):

        if cmd == "Connected":


            self.missing_checks = args["missing_locations"]
            self.prev_found = args["checked_locations"]
            self.location_ids = set(args["missing_locations"] + args["checked_locations"])
            #set up save file checking tasks here
            self.bcz_emblems = args["slot_data"]["BlackCoreEmblems"]
            self.matchmaps = args["slot_data"]["EnableMatchMaps"]
            self.goal_type = args["slot_data"]["CompletionType"]
            self.actsanity = args["slot_data"]["ActSanity"]
            if args["slot_data"]["DeathLink"] != 0:
                self.death_link = True
                self.tags.add("DeathLink")
            else:
                self.death_link = False
            if args["slot_data"]["RingLink"] != 0:
                self.ring_link = args["slot_data"]["RingLink"]
                self.tags.add("RingLink")
            else:
                self.ring_link = False

            # if we don't have the seed name from the RoomInfo packet, wait until we do.
            while not self.seed_name:
                time.sleep(1)


        elif cmd == "RoomInfo":
            self.seed_name = args['seed_name']

        elif cmd == "Bounced":
            tags = args.get("tags", [])
            if "RingLink" in tags:
                handle_received_rings(self, args["data"])

            # If receiving data package, resync previous items
            #asyncio.create_task(self.receive_item())#probably important
    #def on_ringlink(self, rings) -> None:
    #   self.rings = rings



    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        """Gets dispatched when a new DeathLink is triggered by another linked player."""
        self.last_death_link = time.time()#max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        self.activate_death = True
        if text:
            logger.info(f"DeathLink: {text}")
        else:
            logger.info(f"DeathLink: Received from {data['source']}")

    def on_print_json(self, args: dict):
        if self.ui:
            # send copy to UI
            self.ui.print_json(copy.deepcopy(args["data"]))
            self.texttransfer.append(copy.deepcopy(args["data"]))
        logging.getLogger("FileLog").info(self.rawjsontotextparser(copy.deepcopy(args["data"])),
                                          extra={"NoStream": True})
        logging.getLogger("StreamLog").info(self.jsontotextparser(copy.deepcopy(args["data"])),
                                            extra={"NoFile": True})

async def keep_alive(ctx: CommonContext, seconds_between_checks=100):
    """some ISPs/network configurations drop TCP connections if no payload is sent (ignore TCP-keep-alive)
     so we send a payload to prevent drop and if we were dropped anyway this will cause an auto-reconnect."""
    seconds_elapsed = 0
    while not ctx.exit_event.is_set():
        await asyncio.sleep(1)  # short sleep to not block program shutdown
        if ctx.server and ctx.slot:
            seconds_elapsed += 1
            if seconds_elapsed > seconds_between_checks:
                await ctx.send_msgs([{"cmd": "Bounce", "slots": [ctx.slot]}])
                seconds_elapsed = 0



async def server_autoreconnect(ctx: CommonContext):
    await asyncio.sleep(ctx.current_reconnect_delay)
    if ctx.server_address and ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")


async def console_loop(ctx: CommonContext):
    commandprocessor = ctx.command_processor(ctx)
    queue = asyncio.Queue()
    stream_input(sys.stdin, queue)
    while not ctx.exit_event.is_set():
        try:
            input_text = await queue.get()
            queue.task_done()

            if ctx.input_requests > 0:
                ctx.input_requests -= 1
                ctx.input_queue.put_nowait(input_text)
                continue

            if input_text:
                commandprocessor(input_text)
        except Exception as e:
            logger.exception(e)

def handle_received_rings(ctx, data):#shamelessly stolen code from shadow the hedgehog's client
    amount = data["amount"] # yeah his personal client that he made
    source = data["source"] # can you tell im tired trying to write this
    if source == ctx.slot:
        return

    ctx.ring_link_rings += amount




def handle_url_arg(args: "argparse.Namespace",
                   parser: "typing.Optional[argparse.ArgumentParser]" = None) -> "argparse.Namespace":
    """
    Parse the url arg "archipelago://name:pass@host:port" from launcher into correct launch args for CommonClient
    If alternate data is required the urlparse response is saved back to args.url if valid
    """
    if not args.url:
        return args

    url = urllib.parse.urlparse(args.url)
    if url.scheme != "archipelago":
        if not parser:
            parser = get_base_parser()
        parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")
        return args

    args.url = url
    args.connect = url.netloc
    if url.username:
        args.name = urllib.parse.unquote(url.username)
    if url.password:
        args.password = urllib.parse.unquote(url.password)

    return args


def launch(*args):

    async def main(args):
        ctx = SRB2Context(args.connect, args.password)
        ctx.auth = args.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        loop = asyncio.get_running_loop()
        file_path = filedialog.askdirectory(title="Select SRB2 root folder")
        loop.create_task(file_watcher(ctx, file_path), name="save data watcher")
        loop.create_task(item_handler(ctx, file_path), name="incoming item handler")
        # why the fuck does it work now

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description=f"SRB2 {apname} Client")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help=f"{apname} connection url")
    args = parser.parse_args(args)

    args = handle_url_arg(args, parser=parser)

    # use colorama to display colored text highlighting on windows
    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()


async def item_handler(ctx, file_path):
    file_path2 = file_path + "/apgamedat1.ssg"


    try:
        os.mkdir(file_path+"/luafiles/archipelago")
    except FileExistsError:
        print("no need to make a new folder")
    try:
        f = open(file_path + "/luafiles/archipelago/APTranslator.dat", 'r+b')#TODO check for file and get num traps if needed
    except FileNotFoundError:
        f = open(file_path + "/luafiles/archipelago/APTranslator.dat", 'w+b')  # TODO check for file and get num traps if needed
        f.write(0x69.to_bytes(1, byteorder="little"))
        f.seek(0x1B)
        f.write(0x00.to_bytes(3, byteorder="little"))
    f.close()
    # set up new save file here
    # dont need to zero anything out because the first write will overwrite everything wrong

    locs_received = []
    received_bytes = [0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0]

    numreceived = 0
    currenttrap = 0
    while True:
        while ctx.total_locations is not None:


            try:
                f = open(file_path + "/luafiles/archipelago/APTranslator.dat", 'r+b')
            except PermissionError:
                logger.info('Could not open APTranslator.dat. Permission Error')
                await asyncio.sleep(1)
                continue
            f.seek(0x1D)
            f.write(ctx.ring_link.to_bytes(1, byteorder="little"))






            traps = 0
            emeralds = 0
            emblemhints = 0
            emblems = 0
            startrings = 0
            soundtest = 0
            currreceived = 0
            f.seek(0x12)
            num_traps = int.from_bytes(f.read(2), 'little')

            # read characters until null terminator in g
            # compare string/number to token list
            # if found, send respective check
            # repeat until end of file
            # clear file g

            for i in ctx.items_received:
                currreceived +=1
                id = i[0]
                if id == 2:
                    emeralds += 1
                    continue
                if id == 1:
                    emblems += 1
                    continue
                if id == 3:
                    emblemhints += 1
                if id == 80:
                    soundtest = 1
                if id == 74:
                    startrings += 1
                if id == 4 or id == 5 or id == 6 or id == 7 or id == 8 or id == 9 or id == 70 or id == 71 or id == 72 or id == 73 or id == 75 or id == 76 or id == 77 or id == 78 or id == 79 or id==84 or id == 81 or id ==82 or id==83 or id == 86:
                    traps += 1
                    if traps == num_traps + 1:

                        f.seek(0x02)
                        if id == 4:  # 1up
                            f.write(0x01.to_bytes(1, byteorder="little"))
                        if id == 6:  # pity shield
                            f.write(0x02.to_bytes(1, byteorder="little"))
                        if id == 5:  # gravity boots
                            f.write(0x03.to_bytes(1, byteorder="little"))
                        if id == 7:  # replay tutorial
                            f.write(0x04.to_bytes(1, byteorder="little"))
                        if id == 8:  # ring loss
                            f.write(0x05.to_bytes(1, byteorder="little"))
                        if id == 9:  # drop inputs
                            f.write(0x07.to_bytes(1, byteorder="little"))
                        if id == 70:  # & knuckles
                            f.write(0x06.to_bytes(1, byteorder="little"))
                        if id == 71:  # 50 rings
                            f.write(0x08.to_bytes(1, byteorder="little"))
                        if id == 72:  # 20 rings
                            f.write(0x09.to_bytes(1, byteorder="little"))
                        if id == 73:  # 10 rings
                            f.write(0x0A.to_bytes(1, byteorder="little"))
                        if id == 75:  # slippery floors
                            f.write(0x0B.to_bytes(1, byteorder="little"))
                        if id == 76:  # 1000 points
                            f.write(0x0C.to_bytes(1, byteorder="little"))
                        if id == 77:  # sonic forces
                            f.write(0x0D.to_bytes(1, byteorder="little"))
                        if id == 78:  # temp invincibility
                            f.write(0x0E.to_bytes(1, byteorder="little"))
                        if id == 79:  # temp speed shoes
                            f.write(0x0F.to_bytes(1, byteorder="little"))
                        if id == 81:  # spb
                            f.write(0x10.to_bytes(1, byteorder="little"))
                        if id == 82:  # shrink
                            f.write(0x11.to_bytes(1, byteorder="little"))
                        if id == 83:  # grow
                            f.write(0x12.to_bytes(1, byteorder="little"))
                        if id == 84:  # double rings
                            f.write(0x13.to_bytes(1, byteorder="little"))
                        if id == 86:  # jumpscare
                            f.write(0x14.to_bytes(1, byteorder="little"))

                        f.seek(0x12)
                        f.write((num_traps + 1).to_bytes(2, byteorder="little"))
                        f.seek(0x18)

                        f.write(0x01.to_bytes(1,byteorder="little"))  # let srb2 know to read the file
                        continue
                    # in the future it would be efficient to always hold a list of sent items so the file doesnt
                if id in locs_received:  # have to be read every second
                    continue

                if id == 10:  # greenflower
                    received_bytes[0] = received_bytes[0] | 1
                    received_bytes[0] = received_bytes[0] | 2
                    received_bytes[0] = received_bytes[0] | 4
                if id == 105: #gfz1
                    received_bytes[0] = received_bytes[0] | 1
                if id == 106: #gfz2
                    received_bytes[0] = received_bytes[0] | 2
                if id == 107: #gfz3
                    received_bytes[0] = received_bytes[0] | 4

                if id == 11:  # techno hill
                    received_bytes[0] = received_bytes[0] | 8
                    received_bytes[0] = received_bytes[0] | 16
                    received_bytes[0] = received_bytes[0] | 32
                if id == 108: #thz1
                    received_bytes[0] = received_bytes[0] | 8
                if id == 109: #thz2
                    received_bytes[0] = received_bytes[0] | 16
                if id == 110: #thz3
                    received_bytes[0] = received_bytes[0] | 32

                if id == 12:  # deep sea
                    received_bytes[0] = received_bytes[0] | 64
                    received_bytes[0] = received_bytes[0] | 128
                    received_bytes[1] = received_bytes[1] | 1
                if id == 111: #dsz1
                    received_bytes[0] = received_bytes[0] | 64
                if id == 112: #dsz2
                    received_bytes[0] = received_bytes[0] | 128
                if id == 113: #dsz3
                    received_bytes[1] = received_bytes[1] | 1

                if id == 13:  # castle eggman
                    received_bytes[1] = received_bytes[1] | 2
                    received_bytes[1] = received_bytes[1] | 4
                    received_bytes[1] = received_bytes[1] | 8
                if id == 114: #cez1
                    received_bytes[1] = received_bytes[1] | 2
                if id == 115: #cez2
                    received_bytes[1] = received_bytes[1] | 4
                if id == 116: #cez3
                    received_bytes[1] = received_bytes[1] | 8

                if id == 14:  # arid canyon
                    received_bytes[1] = received_bytes[1] | 16
                    received_bytes[1] = received_bytes[1] | 32
                    received_bytes[1] = received_bytes[1] | 64
                if id == 117:  # acz1
                    received_bytes[1] = received_bytes[1] | 16
                if id == 118:  # acz2
                    received_bytes[1] = received_bytes[1] | 32
                if id == 119:  # acz3
                    received_bytes[1] = received_bytes[1] | 64

                if id == 15:  # red volcano
                    received_bytes[1] = received_bytes[1] | 128
                    received_bytes[2] = received_bytes[2] | 1
                    received_bytes[2] = received_bytes[2] | 2
                if id == 120:  # rvz1
                    received_bytes[1] = received_bytes[1] | 128
                if id == 121:  # rvz2
                    received_bytes[2] = received_bytes[2] | 1
                if id == 122:  # rvz3
                    received_bytes[2] = received_bytes[2] | 2

                if id == 16:  # egg rock
                    received_bytes[2] = received_bytes[2] | 4
                    received_bytes[2] = received_bytes[2] | 8
                    received_bytes[2] = received_bytes[2] | 16
                if id == 123:  # erz1
                    received_bytes[2] = received_bytes[2] | 4
                if id == 124:  # erz2
                    received_bytes[2] = received_bytes[2] | 8
                if id == 125:  # erz3
                    received_bytes[2] = received_bytes[2] | 16

                if id == 17:  # black core
                    received_bytes[2] = received_bytes[2] | 32
                    received_bytes[2] = received_bytes[2] | 64
                    received_bytes[2] = received_bytes[2] | 128
                if id == 126:  # bcz1
                    received_bytes[2] = received_bytes[2] | 32
                if id == 127:  # bcz2
                    received_bytes[2] = received_bytes[2] | 64
                if id == 128:  # bcz3
                    received_bytes[2] = received_bytes[2] | 128

                if id == 18:  # frozen hillside
                    received_bytes[3] = received_bytes[3] | 1
                if id == 19:  # pipe towers
                    received_bytes[3] = received_bytes[3] | 2
                if id == 20:  # forest fortress
                    received_bytes[3] = received_bytes[3] | 4
                if id == 21:  # final demo
                    received_bytes[3] = received_bytes[3] | 8
                if id == 22:  # haunted heights
                    received_bytes[3] = received_bytes[3] | 16
                if id == 23:  # aerial garden
                    received_bytes[3] = received_bytes[3] | 32
                if id == 24:  # azure temple
                    received_bytes[3] = received_bytes[3] | 64

                if id == 25:  # floral fields
                    received_bytes[3] = received_bytes[3] | 128
                if id == 26:  # toxic plateau
                    received_bytes[4] = received_bytes[4] | 1
                if id == 27:  # flooded cove
                    received_bytes[4] = received_bytes[4] | 2
                if id == 28:  # cavern fortress
                    received_bytes[4] = received_bytes[4] | 4
                if id == 29:  # dusty wasteland
                    received_bytes[4] = received_bytes[4] | 8
                if id == 30:  # magma caves
                    received_bytes[4] = received_bytes[4] | 16
                if id == 31:  # egg satellite
                    received_bytes[4] = received_bytes[4] | 32
                if id == 32:  # black hole
                    received_bytes[4] = received_bytes[4] | 64
                if id == 33:  # christmas chime
                    received_bytes[4] = received_bytes[4] | 128
                if id == 34:  # dream hill
                    received_bytes[5] = received_bytes[5] | 1
                if id == 35:  # alpine praradise
                    received_bytes[5] = received_bytes[5] | 2
                    received_bytes[5] = received_bytes[5] | 4
                if id == 129: #apz1
                    received_bytes[5] = received_bytes[5] | 2
                if id == 130: #apz2
                    received_bytes[5] = received_bytes[5] | 4

                if id == 55:#sonic
                    received_bytes[5] = received_bytes[5] | 8
                if id == 50:  # tails
                    received_bytes[5] = received_bytes[5] | 16
                if id == 51:  # knuckles
                    received_bytes[5] = received_bytes[5] | 32
                if id == 53:  # fang
                    received_bytes[5] = received_bytes[5] | 64
                if id == 52:  # amy
                    received_bytes[5] = received_bytes[5] | 128
                if id == 54:  # metal sonic
                    received_bytes[6] = received_bytes[6] | 1


                if id == 56:  # whirlwind
                    received_bytes[6] = received_bytes[6] | 2
                if id == 57:  # armageddon
                    received_bytes[6] = received_bytes[6] | 4
                if id == 58:  # elemental
                    received_bytes[6] = received_bytes[6] | 8
                if id == 59:  # attraction
                    received_bytes[6] = received_bytes[6] | 16
                if id == 60:  # force
                    received_bytes[6] = received_bytes[6] | 32
                if id == 61:  # flame
                    received_bytes[6] = received_bytes[6] | 64
                if id == 62:  # bubble
                    received_bytes[6] = received_bytes[6] | 128
                if id == 63:  # lightning
                    received_bytes[7] = received_bytes[7] | 1


                if id == 100: #paraloop
                    received_bytes[7] = received_bytes[7] | 2
                if id == 101: #night helper
                    received_bytes[7] = received_bytes[7] | 4
                if id == 102: #link freeze
                    received_bytes[7] = received_bytes[7] | 8
                if id == 103: #extra time
                    received_bytes[7] = received_bytes[7] | 16
                if id == 104: #drill refill
                    received_bytes[7] = received_bytes[7] | 32

                # #match map flags
                if id == 200:#jade valley
                    received_bytes[7] = received_bytes[7] | 64
                if id == 201:#toxic plateau
                    received_bytes[7] = received_bytes[7] | 128
                if id == 202:#fuckass water map
                    received_bytes[8] = received_bytes[8] | 1
                if id == 203:#thunder citedel
                    received_bytes[8] = received_bytes[8] | 2
                if id == 204:#desolate twilight
                    received_bytes[8] = received_bytes[8] | 4
                if id == 205:#frigid mountain
                    received_bytes[8] = received_bytes[8] | 8
                if id == 206:#orbital hangar
                    received_bytes[8] = received_bytes[8] | 16
                if id == 207:#sapphire falls
                    received_bytes[8] = received_bytes[8] | 32
                if id == 208:#diamond blizzard
                    received_bytes[8] = received_bytes[8] | 64
                if id == 209:#Celestial Sanctuary
                    received_bytes[8] = received_bytes[8] | 128
                if id == 210:#frost columns
                    received_bytes[9] = received_bytes[9] | 1
                if id == 211:#Meadow Match Zone
                    received_bytes[9] = received_bytes[9] | 2
                if id == 212:#granite lake
                    received_bytes[9] = received_bytes[9] | 4
                if id == 213:#summit showdown
                    received_bytes[9] = received_bytes[9] | 8
                if id == 214:#Silver Shiver
                    received_bytes[9] = received_bytes[9] | 16
                if id == 215:#uncharted badlands
                    received_bytes[9] = received_bytes[9] | 32
                if id == 216:#Pristine Shores
                    received_bytes[9] = received_bytes[9] | 64
                if id == 217:#crystalline heights
                    received_bytes[9] = received_bytes[9] | 128
                if id == 218:#starlit warehouse
                    received_bytes[10] = received_bytes[10] | 1
                if id == 219:#fuckass space map
                    received_bytes[10] = received_bytes[10] | 2
                if id == 220:#airborne temple
                    received_bytes[10] = received_bytes[10] | 4
                if id == 150:#zoom tubes
                    received_bytes[10] = received_bytes[10] | 8
                if id == 151:#Rope hangs
                    received_bytes[10] = received_bytes[10] | 16
                if id == 152:#swinging maces
                    received_bytes[10] = received_bytes[10] | 32
                if id == 153:#minecarts
                    received_bytes[10] = received_bytes[10] | 64
                if id == 154:#rollout rocks
                    received_bytes[10] = received_bytes[10] | 128
                if id == 155:#gargoyle statues
                    received_bytes[11] = received_bytes[11] | 1
                if id == 156:#air bubbles
                    received_bytes[11] = received_bytes[11] | 2
                if id == 157:#Buoyant Slime
                    received_bytes[11] = received_bytes[11] | 4
                if id == 158:#dust devils
                    received_bytes[11] = received_bytes[11] | 8
                if id == 159:#yellow springs
                    received_bytes[11] = received_bytes[11] | 16
                if id == 160:#red springs
                    received_bytes[11] = received_bytes[11] | 32
                if id == 161:#blue springs
                    received_bytes[11] = received_bytes[11] | 64

                #received_bytes[11] = received_bytes[11] | 128 #deathlink toggle
                locs_received.append(id)
            if (ctx.bcz_emblems > 0 and emblems >= ctx.bcz_emblems):
                if not ctx.actsanity and 17 not in locs_received:
                    locs_received.append(17)
                    received_bytes[2] = received_bytes[2] | 32
                    received_bytes[2] = received_bytes[2] | 64
                    received_bytes[2] = received_bytes[2] | 128
                if ctx.actsanity and 128 not in locs_received:
                    received_bytes[2] = received_bytes[2] | 128

            # this would be so much better if i made a list of everything and then wrote it to the file all at once
            if ctx.matchmaps:
                received_bytes[11] = received_bytes[11] | 128
            if ctx.death_link:
                received_bytes[2] = received_bytes[2] | 16
            f.seek(0x14)
            if emblemhints >= 2:
                emblemhints = 3 #bits 1 and 2 set
            if soundtest!= 0:
                emblemhints += 4 #sound test bullshit
            f.write(emblemhints.to_bytes(1, byteorder="little"))  # this sucks
            if emeralds > 7:
                emeralds = 7
            f.seek(0x0F)

            if emeralds == 0:
                f.write(0x00.to_bytes(2, byteorder="little"))  # this sucks
            if emeralds == 1:
                f.write(0x01.to_bytes(2, byteorder="little"))  # this sucks
            if emeralds == 2:
                f.write(0x03.to_bytes(2, byteorder="little"))  # this sucks
            if emeralds == 3:
                f.write(0x07.to_bytes(2, byteorder="little"))  # this sucks
            if emeralds == 4:
                f.write(0x0F.to_bytes(2, byteorder="little"))  # this sucks
            if emeralds == 5:
                f.write(0x1F.to_bytes(2, byteorder="little"))  # this sucks
            if emeralds == 6:
                f.write(0x3F.to_bytes(2, byteorder="little"))  # this sucks
            if emeralds >= 7:
                f.write(0x7F.to_bytes(2, byteorder="little"))  # this sucks

            f.seek(0x03)
            f.write(bytes(received_bytes))
            # TODO change to only write on startup, file close, or new item received
            f.seek(0x15)
            f.write(emblems.to_bytes(1, byteorder="little"))
            f.seek(0x16)
            f.write(ctx.bcz_emblems.to_bytes(1, byteorder="little"))
            f.seek(0x17)
            f.write(startrings.to_bytes(1, byteorder="little"))
            if numreceived < currreceived:
                f.seek(0x18)
                f.write(0x01.to_bytes(1, byteorder="little"))  # let srb2 know to read the file for filler
                numreceived = currreceived
            if num_traps > traps:
                if len(ctx.items_received)!=0:#TODO fix this hack
                    f.seek(0x12)
                    f.write(traps.to_bytes(2, byteorder="little"))  # let srb2 know to read the file

            if len(ctx.texttransfer) > 0:
                h = open(file_path + "/luafiles/archipelago/APTextTransfer.txt", 'w+b')#i love character 81 not fucking existing so i cant use the python string stuf :))))))
                for jsons in ctx.texttransfer:
                    for strings in jsons:
                        try:
                            type = strings["type"]
                            if type == "player_id":
                                if int(strings["text"]) == ctx.slot:
                                    h.write(0x81.to_bytes(1, byteorder="little"))
                                else:
                                    h.write(0x82.to_bytes(1, byteorder="little"))
                                h.write(ctx.slot_info[int(strings["text"])].name.encode("ascii"))
                            elif type == "item_id":
                                if int(strings["flags"])==0:#filler
                                    h.write(0x88.to_bytes(1, byteorder="little"))
                                elif int(strings["flags"])==1:#important
                                    h.write(0x89.to_bytes(1, byteorder="little"))
                                elif int(strings["flags"])==2:#useful
                                    h.write(0x84.to_bytes(1, byteorder="little"))
                                elif int(strings["flags"])==3:#useful+important
                                    h.write(0x8F.to_bytes(1, byteorder="little"))
                                elif int(strings["flags"])==4:#trap
                                    h.write(0x87.to_bytes(1, byteorder="little"))
                                else:
                                    h.write(0x85.to_bytes(1, byteorder="little"))
                                h.write((ctx.item_names.lookup_in_game(int(strings["text"]), ctx.slot_info[int(strings["player"])].game)).encode("ascii"))#int(strings["player"])))

                            elif type == "location_id":
                                h.write(0x83.to_bytes(1, byteorder="little"))
                                h.write((ctx.location_names.lookup_in_slot(int(strings["text"]), int(strings["player"]))).encode("ascii"))

                        except KeyError:
                            h.write(0x80.to_bytes(1, byteorder="little"))
                            try:
                                h.write((strings["text"].encode("UTF-8"))) #stupid
                            except UnicodeError:
                                h.write("UTF-8 ENCODING ERROR".encode("UTF-8"))
                        except UnicodeError:
                            h.write("UTF-8 ENCODING ERROR".encode("UTF-8"))

                    h.write(0x0A.to_bytes(1, byteorder="little"))
                ctx.texttransfer = []
                f.seek(0x18)
                f.write(0x03.to_bytes(1, byteorder="little")) #let srb2 know to read the texttransfer file
                h.close()

            try:
                g = open(file_path2, 'r+b')
                g.seek(0x10)  # always select No save to go back to the ap hub
                g.write(0x7D.to_bytes(2, byteorder="little"))  # or find a console command that does that
                g.close()
            except:
                print("save file 1 not found, create it to more easily return to the multiworld hub")

            # todo handle deathlink traps and 1ups

            if ctx.death_link == True:
                f.seek(0x01)
                is_dead = f.read(1)
                if ctx.death_link_lockout + 4 <= time.time():

                    if ctx.activate_death == True:
                        f.seek(0x00)  # received deathlink
                        f.write(0x01.to_bytes(1, byteorder="little"))
                        f.seek(0x18)
                        f.write((int.from_bytes(f.read(1), 'little') | 1).to_bytes(1,byteorder="little"))  # let srb2 know to read the file
                        ctx.death_link_lockout = time.time()
                        print("kill yourself")
                        ctx.activate_death = False

                    elif is_dead != b'\x00':  # outgoing deathlink
                        f.seek(0x01)
                        f.write(0x00.to_bytes(1, byteorder="little"))
                        message = ctx.player_names[ctx.slot] + " wasn't able to retry in time"

                        await ctx.send_death(message)
                        ctx.death_link_lockout = time.time()
                        print("killed myself")

                else:
                    ctx.activate_death = False
                    print("in lockout")
                    # write 0s to both slots if conditions havent been met
                    f.seek(0x00)
                    f.write(0x00.to_bytes(2, byteorder="little"))
            # print("wrote new file data")
            if ctx.ring_link != 0:
            #more stolen code from shadow himself
                f.seek(0x1B)
                current_rings_bytes = f.read(2)
                current_rings = int.from_bytes(current_rings_bytes, byteorder="little")

                difference = current_rings - ctx.previous_rings
                ctx.previous_rings = current_rings + ctx.ring_link_rings


                #TODO special code for when rings goes over 9999


                if difference != 0:
                    #logger.info("got here with a difference of " + str(difference))
                    msg = {
                        "cmd": "Bounce",
                        "slots": [ctx.slot],
                        "data": {
                            "time": time.time(),
                            "source": ctx.slot,
                            "amount": difference
                        },
                        "tags":["RingLink"]
                    }

                    await ctx.send_msgs([msg])

                #here write new ring value back into file
                f.seek(0x1B)
                if current_rings+ctx.ring_link_rings < 0:
                    ctx.ring_link_rings = -current_rings
                if current_rings+ctx.ring_link_rings <= 65535:
                    f.write(int(current_rings+ctx.ring_link_rings).to_bytes(2, byteorder="little"))
                else:
                    f.write(int(65535).to_bytes(2, byteorder="little"))
                ctx.ring_link_rings = 0
                # logger.info("ring link rings is " + str(ctx.ring_link_rings))

            f.close()
            await asyncio.sleep(1)
        await asyncio.sleep(1)

async def file_watcher(ctx, file_path):
    locs_to_send = set()
    num_sent = 0
    locs_sent = set()
    file_path2 = file_path + "/apgamedat.dat"

    while ctx.total_locations is None:
        await asyncio.sleep(1)
        continue

    await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])
    # wait to connect



    try:  # once connected verify apgamedat exists

        if not os.path.isfile(file_path2):
            raise FileNotFoundError  # stupid code
        f = open(file_path2, 'r+b')
        checkma = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0,0,0,0,0,0,0,0,0]
        for i in ctx.checked_locations:
            if i < 260:
                i = i - 1
                r1 = math.floor(i / 8)
                r2 = i % 8

                # divide then floor to get byte number
                # modulo to get byte value to set
                if r2 == 0:
                    checkma[r1] += 1
                if r2 == 1:
                    checkma[r1] += 2
                if r2 == 2:
                    checkma[r1] += 4
                if r2 == 3:
                    checkma[r1] += 8
                if r2 == 4:
                    checkma[r1] += 16
                if r2 == 5:
                    checkma[r1] += 32
                if r2 == 6:
                    checkma[r1] += 64
                if r2 == 7:
                    checkma[r1] += 128
        f.seek(0x0C)##TODO check whats unlocked then reveal zones here
        for i in range(0x50):
            f.write(0x00.to_bytes(1, byteorder="little")) #set level visited flags
        for i in ctx.items_received:
            id = i[0]
            if id == 10:
                f.seek(0x0C)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x0D)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x0E)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 11:#techno hill
                f.seek(0x0F)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x10)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x11)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 12:#deep sea
                f.seek(0x12)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x13)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x14)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 13:  # CASTLE EGGMAN
                f.seek(0x15)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x16)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x17)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 14:  # arid canyon
                f.seek(0x18)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x19)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x1A)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 15:  # RED VOLCANO
                f.seek(0x1B)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x1C)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x1D)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 16:  # egg rock
                f.seek(0x21)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x22)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x23)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 17:#black core
                f.seek(0x24)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x25)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x26)
                f.write(0x01.to_bytes(1, byteorder="little"))

            if id == 18: #fhz
                f.seek(0x29)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 19: #ptz
                f.seek(0x2A)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 20: #ffz
                f.seek(0x2B)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 21: #fdz
                f.seek(0x2C)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 22: #hhz
                f.seek(0x33)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 23: #agz
                f.seek(0x34)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 24: #atz
                f.seek(0x35)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 25: #sp1
                f.seek(0x3D)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 26: #sp2
                f.seek(0x3E)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 27:#sp3
                f.seek(0x3F)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 28:#sp4
                f.seek(0x40)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 29:#sp5
                f.seek(0x41)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 30:#sp6
                f.seek(0x42)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 31:#sp7
                f.seek(0x43)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 32:#sp8
                f.seek(0x44)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 33: #ccz
                f.seek(0x51)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 34: #dhz
                f.seek(0x52)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if id == 35: #apz:
                f.seek(0x53)
                f.write(0x01.to_bytes(1, byteorder="little"))
                f.seek(0x54)
                f.write(0x01.to_bytes(1, byteorder="little"))
            if ctx.matchmaps:
                if id == 200:
                    f.seek(0x21F)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 201:
                    f.seek(0x220)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 202:
                    f.seek(0x221)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 203:
                    f.seek(0x222)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 204:
                    f.seek(0x223)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 205:
                    f.seek(0x224)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 206:
                    f.seek(0x225)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 207:
                    f.seek(0x226)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 208:
                    f.seek(0x227)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 209:
                    f.seek(0x228)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 210:
                    f.seek(0x229)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 211:
                    f.seek(0x22A)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 212:
                    f.seek(0x22B)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 213:
                    f.seek(0x22C)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 214:
                    f.seek(0x22D)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 215:
                    f.seek(0x22E)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 216:
                    f.seek(0x22F)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 217:
                    f.seek(0x230)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 218:
                    f.seek(0x243)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 219:
                    f.seek(0x244)
                    f.write(0x01.to_bytes(1, byteorder="little"))
                if id == 220:
                    f.seek(0x245)
                    f.write(0x01.to_bytes(1, byteorder="little"))
            else:
                f.seek(0x21F)
                for i in range(0x30):
                    f.write(0x00.to_bytes(1, byteorder="little"))  # set level visited flags
        f.seek(0x450)
        f.write(0x00.to_bytes(0x3000, byteorder="little"))
        f.seek(0x417)
        f.write(bytes(checkma))
        f.seek(0x220)


        f.close()
    except FileNotFoundError:

        print("apgamedat.dat does not exist, let SRB2 make a new one...")
    except PermissionError:

        print("could not overwrite old save data (lack of permission). Try closing the file in HXD you dumbass")

##    cfg = open(file_path + "/AUTOEXEC.CFG", "w")
##    cfg.write("addfile addons/SL_ArchipelagoSRB2_v134.pk3")
##    cfg.close()
##    os.chdir(file_path)
    if os.path.exists(file_path+"/addons/SL_ArchipelagoSRB2_v161.pk3"):
        try:
            subprocess.Popen([file_path + "/srb2win.exe", "-file", "/addons/SL_ArchipelagoSRB2_v161.pk3"], cwd=file_path)
        except:
            logger.info('Could not open srb2win.exe. Open the game and load the addon manually')
    else:
        try:
            subprocess.Popen([file_path + "/srb2win.exe"], cwd=file_path)
            logger.info('Could not find SL_ArchipelagoSRB2_v161.pk3 in the addons folder. You must load the addon manually')
        except:
            logger.info('Could not open srb2win.exe. Open the game and load the addon manually')

    # look into subprocess.Popen, if used correctly, i might be able to acess srb2's console output for commands and
    # use COM_BufInsertText(server, "command") to type in console
    # recieved notifications

    #cfg = open(file_path + "/AUTOEXEC.CFG", "w")
    #cfg.write("")
    #cfg.close()
    # if not do nothing (srb2 will create an empty gamedat on launch)
    # if it does, get checked locations from the server, and overwrite corresponding bits in apgamedat

    # create AUTOEXEC.CFG with the text "addfile addons/ArchipelagoSRB2.pk3"
    # launch srb2
    # clear AUTOEXEC.CFG so people dont get confused when they cant uninstall the ap mod
    while not os.path.isfile(file_path2):
        await asyncio.sleep(1)  # wait for srb2 to make new apgamedat if it doesnt exist
    previous = os.stat(file_path2).st_mtime
    token_numbers = ["1111149056392167424", "1205520896132120576",
                     "2429916160140509184",
                     "2-134217728-658505728",
                     "2-360185856-495452160",
                     "4979369984-525336576",
                     "41241513984-335544320",
                     "554525952-457179136",
                     "5-1048576000-398458880",
                     "741313894458720256",
                     "7763363328442499072",
                     "7125829120645922816",
                     "7838860800929038336",
                     "767528294458720256",
                     "81522532352-880803840",
                     "8964689920541065216",
                     "8635437056-434110464",
                     "8579862528461373440",
                     "1016777216-880803840",
                     "10352321536-434110464",
                     "10752877568264241152",
                     "11-587202560-1132462080",
                     "11362807296-650117120",
                     "11-318767104-1040187392",
                     "11-738197504-213909504",
                     "11452984832115343360",
                     "13-263192576-510132224",
                     "13-805306368-415236096",
                     "13184549376-75497472",
                     "148388608-1247805440",
                     "14514850816-429391872",
                     "14589299712-1384120320",
                     "161562378240243269632",
                     "16232783872557842432",
                     "163019898881172307968",
                     "16-158007296-949813248",
                     "22312475648-427819008",
                     "22-878706688-677380096",
                     "2325165824633339904",
                     "23664797184679477248",
                     "23-742391808266338304",
                     "33-1742733312-1530920960",
                     "33-662700032-1296039936",
                     "33-585629696-1988624384",
                     "331482686464-1557135360",
                     "331577058304-1828716544",
                     "331665138688-243269632",
                     "331694498816-494927872",
                     "331811939328754974720",
                     "331728053248436207616",
                     "3316714301441484783616",
                     "411069547520-618659840",
                     "41-576716800-681574400",
                     "41-576716800-694157312",
                     "41-589299712-694157312",
                     "41-589299712-681574400",
                     "411614807041367343104"
                     ]
    oneupids = ["1:L2","1:L8","1:L11","2:L0","2:L10","2:L11","2:L12","2:L17","2:L18","2:L21","2:L23","2:L30","4:L1",
                "4:L11","4:L17","4:L22","4:L26","4:L28","4:L30","4:L33","4:L40","5:L4","5:L7","5:L10","5:L15","5:L19",
                "5:L25","5:L26","5:L30","5:L33","5:L34","5:L46","5:L49","7:L6","7:L7","7:L9","7:L10","7:L11","7:L12",
                "7:L17","7:L22","7:L23","7:L25","7:L26","7:L27","7:L35","7:L36","7:L37","7:L44","7:L47","7:L50","7:L52",
                "8:L1","8:L2","8:L4","8:L6","8:L18","8:L28","8:L30","8:L33","8:L39","8:L40","8:L43","8:L47","8:L49",
                "8:L50","8:L52","10:L1","10:L2","10:L4","10:L6","10:L7","10:L9","10:L25","10:L41","10:L43","10:L44",
                "11:L3","11:L5","11:L9","11:L15","11:L19","11:L20","11:L23","11:L24","11:L25","11:L31","11:L33",
                "11:L36","11:L44","11:L48","13:L2","13:L3","13:L8","13:L11","13:L13","13:L21","13:L30","13:L32","13:L37",
                "13:L38","14:L1","14:L2","14:L4","14:L5","14:L11","14:L12","14:L15","14:L21","14:L30","14:L33",
                "14:L37","14:L42","14:L47","14:L53","14:L54","14:L55","14:L56","14:L57","16:L0","16:L2","16:L4","16:L7",
                "16:L11","16:L13","16:L18","16:L19","16:L21","22:L0","22:L1","22:L2","22:L3","22:L5","22:L8","22:L9",
                "22:L17","23:L0","23:L1","23:L3","23:L5","23:L6","23:L7","23:L14","23:L17","23:L19","23:L21","23:L26",
                "23:L27","23:L29","23:L35","25:L0","25:L1","26:L0","30:L2","30:L12","31:L0","31:L1","31:L2","31:L3","31:L4",
                "31:L5","32:L4","32:L6","32:L13","32:L16","32:L22","33:L0","33:L18","33:L21","33:L22","33:L31","33:L32",
                "33:L37","33:L41","33:L42","33:L45","33:L52","33:L66","33:L69","33:L72","33:L74","40:L2","40:L5",
                "40:L6","40:L7","40:L8","40:L11","40:L15","40:L16","40:L17","40:L19","40:L21","40:L27","40:L32",
                "40:L33","40:L34","40:L36","40:L37","41:L4","41:L5","41:L7","41:L8","41:L10","41:L20","41:L22","41:L23",
                "41:L24","41:L28","41:L36","41:L37","41:L38","41:L39","41:L40","41:L46","41:L50","41:L51","41:L52",
                "41:L54","41:L57","41:L58","41:L59","41:L60","41:L61","41:L62","41:L64","41:L68","41:L76","41:L78",
                "41:L80","41:L81","42:L8","42:L9","42:L16","42:L22","42:L25","42:L27","42:L31","42:L33","42:L36",
                "42:L39","42:L40","42:L41","42:L42","42:L46","42:L52","42:L55","42:L57","42:L60","539:L14"]

    superringids = ["1:R0","1:R1","1:R3","1:R4","1:R5","1:R6","1:R7","1:R9","1:R10","1:R12","1:R13","1:R14","2:R1",
"2:R2","2:R3","2:R4","2:R5","2:R6","2:R7","2:R8","2:R9","2:R13","2:R14","2:R15","2:R16","2:R19","2:R20","2:R22","2:R24",
"2:R25","2:R26","2:R27","2:R28","2:R29","4:R0","4:R2","4:R3","4:R4","4:R5","4:R6","4:R7","4:R8","4:R9","4:R10","4:R12",
"4:R13","4:R14","4:R15","4:R16","4:R18","4:R19","4:R20","4:R21","4:R23","4:R24","4:R25","4:R27","4:R29","4:R31","4:R32",
"4:R34","4:R35","4:R36","4:R37","4:R38","4:R39","4:R41","5:R0","5:R1","5:R2","5:R3","5:R5","5:R6","5:R8","5:R9","5:R11",
"5:R12","5:R13","5:R14","5:R16","5:R17","5:R18","5:R20","5:R21","5:R22","5:R23","5:R24","5:R27","5:R28","5:R29","5:R31",
"5:R32","5:R35","5:R36","5:R37","5:R38","5:R39","5:R40","5:R41","5:R42","5:R43","5:R44","5:R45","5:R47","5:R48","5:R50",
"5:R51","5:R52","7:R0","7:R1","7:R2","7:R3","7:R4","7:R5","7:R8","7:R13","7:R14","7:R15","7:R16","7:R18","7:R19","7:R20",
"7:R21","7:R24","7:R28","7:R29","7:R30","7:R31","7:R32","7:R33","7:R34","7:R38","7:R39","7:R40","7:R41","7:R42","7:R43",
"7:R45","7:R46","7:R48","7:R49","7:R51","8:R0","8:R3","8:R5","8:R7","8:R8","8:R9","8:R10","8:R11","8:R12","8:R13",
"8:R14","8:R15","8:R16","8:R17","8:R19","8:R20","8:R21","8:R22","8:R23","8:R24","8:R25","8:R26","8:R27","8:R29","8:R31",
"8:R32","8:R34","8:R35","8:R36","8:R37","8:R38","8:R41","8:R42","8:R44","8:R45","8:R46","8:R48","8:R51","10:R0","10:R3",
"10:R5","10:R8","10:R10","10:R11","10:R12","10:R13","10:R14","10:R15","10:R16","10:R17","10:R18","10:R19","10:R20",
"10:R21","10:R22","10:R23","10:R24","10:R26","10:R27","10:R28","10:R29","10:R30","10:R31","10:R32","10:R33","10:R34",
"10:R35","10:R36","10:R37","10:R38","10:R39","10:R40","10:R42","11:R0","11:R1","11:R2","11:R4","11:R6","11:R7","11:R8",
"11:R10","11:R11","11:R12","11:R13","11:R14","11:R16","11:R17","11:R18","11:R21","11:R22","11:R26","11:R27","11:R28",
"11:R29","11:R30","11:R32","11:R34","11:R35","11:R37","11:R38","11:R39","11:R40","11:R41","11:R42","11:R43","11:R45",
"11:R46","11:R47","11:R49","11:R50","11:R51","11:R52","11:R53","11:R54","11:R55","11:R56","11:R57","11:R58","11:R59",
"11:R60","11:R61","11:R62","13:R0","13:R1","13:R4","13:R5","13:R6","13:R7","13:R9","13:R10","13:R12","13:R14","13:R15",
"13:R16","13:R17","13:R18","13:R19","13:R20","13:R22","13:R23","13:R24","13:R25","13:R26","13:R27","13:R28","13:R29",
"13:R31","13:R33","13:R34","13:R35","13:R36","14:R0","14:R3","14:R6","14:R7","14:R8","14:R9","14:R10","14:R13","14:R14",
"14:R16","14:R17","14:R18","14:R19","14:R20","14:R22","14:R23","14:R24","14:R25","14:R26","14:R27","14:R28","14:R29",
"14:R31","14:R32","14:R34","14:R35","14:R36","14:R38","14:R39","14:R40","14:R41","14:R43","14:R44","14:R45","14:R46",
"14:R48","14:R49","14:R50","14:R51","14:R52","14:R58","16:R1","16:R3","16:R5","16:R6","16:R8","16:R9","16:R10",
"16:R12","16:R14","16:R15","16:R16","16:R17","16:R20","22:R4","22:R6","22:R7","22:R10","22:R11","22:R12","22:R13",
"22:R14","22:R15","22:R16","22:R18","22:R19","22:R20","22:R21","22:R22","22:R23","22:R24","22:R25","23:R2","23:R4",
"23:R8","23:R9","23:R10","23:R11","23:R12","23:R13","23:R15","23:R16","23:R18","23:R20","23:R22","23:R23","23:R24",
"23:R25","23:R28","23:R30","23:R31","23:R32","23:R33","23:R34","23:R36","30:R0","30:R1","30:R3","30:R4","30:R5","30:R6",
"30:R7","30:R8","30:R9","30:R10","30:R11","30:R13","32:R0","32:R1","32:R2","32:R3","32:R5","32:R7","32:R8","32:R9",
"32:R10","32:R11","32:R12","32:R14","32:R15","32:R17","32:R18","32:R19","32:R20","32:R21","32:R23","32:R24","32:R25",
"33:R1","33:R2","33:R3","33:R4","33:R5","33:R6","33:R7","33:R8","33:R9","33:R10","33:R11","33:R12","33:R13","33:R14",
"33:R15","33:R16","33:R17","33:R19","33:R20","33:R23","33:R24","33:R25","33:R26","33:R27","33:R28","33:R29","33:R30",
"33:R33","33:R34","33:R35","33:R36","33:R38","33:R39","33:R40","33:R43","33:R44","33:R46","33:R47","33:R48","33:R49",
"33:R50","33:R51","33:R53","33:R54","33:R55","33:R56","33:R57","33:R58","33:R59","33:R60","33:R61","33:R62","33:R63",
"33:R64","33:R65","33:R67","33:R68","33:R70","33:R71","33:R73","40:R0","40:R1","40:R3","40:R4","40:R9","40:R10",
"40:R12","40:R13","40:R14","40:R18","40:R20","40:R22","40:R23","40:R24","40:R25","40:R26","40:R28","40:R29","40:R30",
"40:R31","40:R35","40:R38","40:R39","41:R0","41:R1","41:R2","41:R3","41:R6","41:R9","41:R11","41:R12","41:R13","41:R14",
"41:R15","41:R16","41:R17","41:R18","41:R19","41:R21","41:R25","41:R26","41:R27","41:R29","41:R30","41:R31","41:R32",
"41:R33","41:R34","41:R35","41:R41","41:R42","41:R43","41:R44","41:R45","41:R47","41:R48","41:R49","41:R53","41:R55",
"41:R56","41:R63","41:R65","41:R66","41:R67","41:R69","41:R70","41:R71","41:R72","41:R73","41:R74","41:R75","41:R77",
"41:R79","42:R0","42:R1","42:R2","42:R3","42:R4","42:R5","42:R6","42:R7","42:R10","42:R11","42:R12","42:R13","42:R14",
"42:R15","42:R17","42:R18","42:R19","42:R20","42:R21","42:R23","42:R24","42:R26","42:R28","42:R29","42:R30","42:R32",
"42:R34","42:R35","42:R37","42:R38","42:R43","42:R44","42:R45","42:R47","42:R48","42:R49","42:R50","42:R51","42:R53",
"42:R54","42:R56","42:R58","42:R59","42:R61","532:R0","532:R1","532:R2","532:R3","532:R4","532:R5","532:R6","532:R7",
"532:R8","532:R9","532:R10","532:R11","532:R12","532:R13","532:R14","532:R15","532:R16","532:R17","533:R0","533:R1",
"533:R2","533:R3","533:R4","533:R5","533:R6","533:R7","533:R8","533:R9","533:R10","533:R11","533:R12","533:R13",
"533:R14","533:R15","533:R16","533:R17","533:R18","533:R19","533:R20","533:R21","534:R0","534:R1","534:R2","534:R3",
"534:R4","534:R5","534:R6","534:R7","534:R8","534:R9","534:R10","534:R11","534:R12","534:R13","534:R14","534:R15",
"534:R16","534:R17","534:R18","534:R19","534:R20","534:R21","534:R22","534:R23","534:R24","535:R0","535:R1","535:R2",
"535:R3","535:R4","535:R5","535:R6","535:R7","535:R8","535:R9","535:R10","535:R11","535:R12","535:R13","535:R14",
"535:R15","535:R16","536:R0","536:R1","536:R2","536:R3","536:R4","536:R5","536:R6","536:R7","536:R8","536:R9","536:R10",
"536:R11","537:R0","537:R1","537:R2","537:R3","537:R4","537:R5","537:R6","537:R7","537:R8","537:R9","537:R10","537:R11",
"538:R0","538:R1","538:R2","538:R3","538:R4","538:R5","538:R6","538:R7","538:R8","538:R9","538:R10","538:R11","538:R12",
"538:R13","538:R14","538:R15","538:R16","538:R17","538:R18","538:R19","538:R20","538:R21","538:R22","538:R23","538:R24",
"539:R0","539:R1","539:R2","539:R3","539:R4","539:R5","539:R6","539:R7","539:R8","539:R9","539:R10","539:R11","539:R12",
"539:R13","539:R15","539:R16","539:R17","539:R18","540:R0","540:R1","540:R2","540:R3","540:R4","540:R5",
"540:R6","540:R7","540:R8","540:R9","540:R10","540:R11","540:R12","540:R13","540:R14","540:R15","540:R16","540:R17",
"540:R18","540:R19","540:R20","540:R21","540:R22","540:R23","540:R24","540:R25","541:R0","541:R1","541:R2","541:R3",
"541:R4","541:R5","541:R6","541:R7","541:R8","541:R9","541:R10","541:R11","541:R12","541:R13","541:R14","541:R15",
"541:R16","541:R17","541:R18","541:R19","541:R20","541:R21","542:R0","542:R1","542:R2","542:R3","542:R4","542:R5",
"542:R6","542:R7","542:R8","542:R9","542:R10","542:R11","542:R12","542:R13","542:R14","542:R15","542:R16","542:R17",
"542:R18","542:R19","542:R20","542:R21","543:R0","543:R1","543:R2","543:R3","543:R4","543:R5","544:R0","544:R1",
"544:R2","544:R3","544:R4","544:R5","544:R6","544:R7","544:R8","544:R9","544:R10","545:R0","545:R1","545:R2","545:R3",
"545:R4","545:R5","545:R6","545:R7","545:R8","545:R9","545:R10","545:R11","545:R12","545:R13","545:R14","545:R15",
"545:R16","545:R17","545:R18","545:R19","545:R20","545:R21","545:R22","546:R0","546:R1","546:R2","546:R3","546:R4",
"546:R5","546:R6","546:R7","546:R8","546:R9","546:R10","546:R11","546:R12","546:R13","546:R14","546:R15","546:R16",
"546:R17","546:R18","546:R19","546:R20","546:R21","546:R22","546:R23","546:R24","546:R25","546:R26","546:R27","546:R28",
"546:R29","546:R30","546:R31","546:R32","546:R33","546:R34","546:R35","546:R36","546:R37","546:R38","546:R39","546:R40",
"546:R41","546:R42","546:R43","546:R44","547:R0","547:R1","547:R2","547:R3","547:R4","547:R5","547:R6","547:R7",
"547:R8","548:R0","548:R1","548:R2","548:R3","548:R4","548:R5","548:R6","548:R7","548:R8","548:R9","548:R10","548:R11",
"548:R12","548:R13","548:R14","548:R15","548:R16","548:R17","548:R18","548:R19","549:R0","549:R1","549:R2","549:R3",
"549:R4","549:R5","549:R6","549:R7","549:R8","549:R9","549:R10","549:R11","549:R12","549:R13","549:R14","549:R15",
"549:R16","549:R17","549:R18","549:R19","549:R20","549:R21","569:R0","569:R1","569:R2","569:R3","569:R4","569:R5",
"569:R6","569:R7","569:R8","569:R9","569:R10","569:R11","570:R0","570:R1","570:R2","570:R3","570:R4","570:R5",
"570:R6","570:R7","570:R8","570:R9","570:R10","570:R11"]
    # format is [gamemap]:[monitortype][checkid]"







    while True:
        # run the console command to get recieved items
        try:
            g = open(file_path + "/luafiles/archipelago/APTokens.txt", 'r+')
            for lines in g:
                lines = lines.strip()
                if lines is None:
                    break
                for i in token_numbers:
                    if lines == i:
                        locs_to_send.add(token_numbers.index(i) + 260)
                        break
                for i in oneupids:
                    if lines == i:
                        locs_to_send.add(oneupids.index(i) + 320)
                        break
                for i in superringids:
                    if lines == i:
                        locs_to_send.add(superringids.index(i) + 570)
                        break
            g.truncate(0)
            g.close()
        except FileNotFoundError:
            print("APTokens.txt not found, collect an emerald token to create it")

        current = os.stat(file_path2).st_mtime
        if current != previous:

            previous = current
            with open(file_path2, 'rb') as f:
                f.seek(0x417)  # start of the emblem save file
                for i in range(0, 0x21):
                    byte = int.from_bytes(f.read(1), 'little')
                    # convert each check into corresponding location number
                    for j in range(8):
                        bit = (byte >> j) & 1
                        if bit == 1:
                            locs_to_send.add(8 * i + j + 1)
                            if (8 * i + j + 1) == 128 and ctx.goal_type == 0:
                                ctx.finished_game = True
                                await ctx.send_msgs([{
                                    "cmd": "StatusUpdate",
                                    "status": ClientStatus.CLIENT_GOAL
                                }])

                f.seek(0x457)
                byte = int.from_bytes(f.read(1), 'little')
                if byte != 0 and ctx.goal_type == 1:
                    ctx.finished_game = True
                    locs_to_send.add(259)
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])


            f.close()
            # Compare locs_to_send to locations already sent
        if len(locs_to_send) > num_sent:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])
            print("sending new checks")
            num_sent = len(locs_to_send)
        await asyncio.sleep(1)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    launch(*sys.argv[1:])
