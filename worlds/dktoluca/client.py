import logging
import time
import random

from enum import Enum
from NetUtils import ClientStatus, NetworkItem, color
from worlds.AutoSNIClient import SNIClient, SnesReader, SnesData, Read
from .constants import *
from .locations import sorted_locations_table, banana_birds

logger = logging.getLogger("Client")
snes_logger = logging.getLogger("SNES")

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SNIClient import SNIContext

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
SRAM_START = 0xE00000

DKC3_SRAM = SRAM_START + 0x700
DKC3_SETTINGS = ROM_START + 0x3AFF00

DKC3_ENERGY_PACKET = DKC3_SRAM + 0x2E
DKC3_EXCHANGE_RATE = 200000000
DK_BARREL_BANANA_COST = 20
DK_BARREL_MAX = 3

DKC3_ROMHASH_START = 0xFFC0
ROMHASH_SIZE = 0x15

POINTER_MAIN_MAP = 0xB179
POINTER_IN_LEVEL = 0x8076

class DKC3Memory(Enum):
    settings = Read(DKC3_SETTINGS, 0x40)
    recv_index = Read(DKC3_SRAM + 0x2C, 0x02)
    level_flags = Read(WRAM_START + 0x00632, 0x100)
    collectible_data = Read(WRAM_START + 0x1F800, 0x100)
    unlocks = Read(DKC3_SRAM, 0x28)
    barrel_count = Read(DKC3_SRAM + 0x30, 0x02)
    current_map_level = Read(DKC3_SRAM + 0x3C, 0x02)
    energy_packet = Read(DKC3_SRAM + 0x2E, 0x02)
    gameplay_pointer = Read(WRAM_START + 0x4E, 0x02)
    banana_birds = Read(WRAM_START + 0x642, 0x0E)
    banana_bird_count = Read(WRAM_START + 0x05CD, 0x02)
    bear_coin_count = Read(WRAM_START + 0x05C9, 0x02)
    bonus_coin_count = Read(WRAM_START + 0x05CB, 0x02)
    dk_coin_count = Read(WRAM_START + 0x05CF, 0x02)
    cog_count = Read(WRAM_START + 0x05D1, 0x02)
    vehicles = Read(WRAM_START + 0x0611, 0x02)
    lives = Read(WRAM_START + 0x05D5, 0x02)
    extractinator_upgrades = Read(DKC3_SRAM + 0x32, 0x02)
    started_save = Read(WRAM_START + 0x0C2, 2)

countable_items = {
    0x05CD: DKC3Memory.banana_bird_count,
    0x05D1: DKC3Memory.cog_count,
    0x05CB: DKC3Memory.bonus_coin_count,
    0x0030: DKC3Memory.barrel_count,
    0x05C9: DKC3Memory.bear_coin_count,
    0x05CF: DKC3Memory.dk_coin_count,
    0x05D5: DKC3Memory.lives,
    0x0032: DKC3Memory.extractinator_upgrades,
}

class ConnectMemory(Enum):
    rom_hash = Read(DKC3_ROMHASH_START, ROMHASH_SIZE)
    settings = Read(DKC3_SETTINGS, 0x40)


class DKC3SNIClient(SNIClient):
    game = GAME_NAME
    patch_suffix = ".aptoluca"
    slot_data: dict
    ctx: "SNIContext"
    memory_reader = SnesReader(DKC3Memory)
    connect_reader = SnesReader(ConnectMemory)

    def __init__(self):
        super().__init__()
        self.game_state = False
        self.energy_link_enabled = False
        self.received_trap_link = False
        self.barrel_request = ""
        self.barrel_count = ""
        self.current_map = 0
        self.barrel_label = None


    async def validate_rom(self, ctx: "SNIContext"):
        snes_data = await self.connect_reader.read(ctx)
        if snes_data is None:
            return False

        rom_name = snes_data.get(ConnectMemory.rom_hash)
        settings = snes_data.get(ConnectMemory.settings)

        if rom_name is None or settings is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:4] != b"DKCT":
            if "request" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("request")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True

        update_tags = False

        energy_link = settings[0x19]
        if energy_link and "EnergyLink" not in ctx.tags:
            ctx.tags.add("EnergyLink")
            update_tags = True
            if "request" not in ctx.command_processor.commands:
                ctx.command_processor.commands["request"] = cmd_request

        if update_tags:
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])
        
        ctx.rom = rom_name

        return True


    async def game_watcher(self, ctx: "SNIContext"):
        if ctx.server is None:
            return
        
        from SNIClient import snes_buffered_write, snes_flush_writes

        memory_data = await self.memory_reader.read(ctx)
        if memory_data is None:
            self.game_state = False
            self.current_map = 0
            return
        
        loaded_save = int.from_bytes(memory_data.get(DKC3Memory.started_save), "little")
        if loaded_save == 0:
            self.game_state = False
            self.current_map = 0
            return

        gameplay_pointer = int.from_bytes(memory_data.get(DKC3Memory.gameplay_pointer), "little")
        if gameplay_pointer == POINTER_MAIN_MAP or gameplay_pointer == POINTER_IN_LEVEL:
            self.game_state = True
            
        if not self.game_state:
            return

        if "EnergyLink" in ctx.tags:
            await self.handle_energy_link(ctx, memory_data)

        new_checks = []
        setting_data = list(memory_data.get(DKC3Memory.settings))
        current_map_level = int.from_bytes(memory_data.get(DKC3Memory.current_map_level), "little")
        level_flags = list(memory_data.get(DKC3Memory.level_flags))
        collectible_data = list(memory_data.get(DKC3Memory.collectible_data))
        banana_bird_flags = list(memory_data.get(DKC3Memory.banana_birds))

        enabled_dk_coin = setting_data[0x0E]
        enabled_kong = setting_data[0x0F]
        enabled_balloon = setting_data[0x10]
        enabled_banana = setting_data[0x11]
        enabled_coin = setting_data[0x12]
        enabled_birds = setting_data[0x13]

        if current_map_level >= 0x1D and current_map_level < 0x4D and current_map_level in sorted_locations_table.keys():
            for loc_id in sorted_locations_table[current_map_level]:
                # Early discard already checked locations
                if loc_id in ctx.locations_checked:
                    continue

                # Get info from the location ID
                level_id = loc_id >> 24
                loc_type = (loc_id >> 20) & 0x0F
                loc_data = loc_id & 0x000FFFFF

                if loc_type in [0x00, 0x01, 0x02]:
                    # Clears, Bonuses, DK Coins
                    if level_flags[level_id] & loc_data:
                        new_checks.append(loc_id)
                elif loc_type == 0x03 and enabled_dk_coin:
                    # DK Coins
                    if level_flags[level_id] & loc_data:
                        new_checks.append(loc_id)
                elif loc_type == 0x04 and enabled_kong:
                    # KONG
                    if level_flags[level_id] & loc_data:
                        new_checks.append(loc_id)
                elif loc_type == 0x05 and enabled_balloon:
                    # Balloons
                    if collectible_data[loc_data + 1] & 0x01:
                        new_checks.append(loc_id)
                elif loc_type == 0x06 and enabled_banana:
                    # Bananas
                    if collectible_data[loc_data + 1] & 0x02:
                        new_checks.append(loc_id)
                elif loc_type == 0x07 and enabled_coin:
                    # Coins
                    if collectible_data[loc_data + 1] & 0x04:
                        new_checks.append(loc_id)
    
        if enabled_birds:
            for _, loc_id in banana_birds.items():
                if loc_id in ctx.locations_checked:
                    continue
                loc_data = loc_id & 0x000FFFFF
                if banana_bird_flags[loc_data] & 0x02:
                    new_checks.append(loc_id)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        # Check goals
        goal_check = 0
        selected_goal = setting_data[0x04]

        level_data = level_flags[0x23]
        if level_data & 0x1C:
            goal_check |= 1
        
        level_data = level_flags[0x24]
        if level_data & 0x20:
            goal_check |= 2

        if goal_check & selected_goal == selected_goal:
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
                return
            
        # Add a label that shows how many Barrels are left
        await self.handle_barrel_label(ctx, memory_data)

        # Receive items
        recv_index = int.from_bytes(memory_data.get(DKC3Memory.recv_index), "little")
        if recv_index < len(ctx.items_received):
            item: NetworkItem = ctx.items_received[recv_index]
            recv_index += 1
            sending_game = ctx.slot_info[item.player].game
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))
            
            item_ram = item.item & 0x100000
            item_type = item.item & 0xF0000
            item_data = item.item & 0x0FFFF

            if item_type == FLAG:
                snes_buffered_write(ctx, DKC3_SRAM + item_data, 0x01.to_bytes(1, "little"))

            elif item_type == COUNT:
                count = int.from_bytes(memory_data.get(countable_items[item_data]), "little")
                count = min(99, count+1)
                if item_ram:
                    # WRAM
                    snes_buffered_write(ctx, WRAM_START + item_data, count.to_bytes(2, "little"))
                else:
                    # SRAM 
                    snes_buffered_write(ctx, DKC3_SRAM + item_data, count.to_bytes(2, "little"))

            elif item_type == DIXIE:
                kongs = memory_data.get(DKC3Memory.unlocks)[0]
                kongs |= 0x01
                snes_buffered_write(ctx, DKC3_SRAM, kongs.to_bytes(1, "little"))
                
            elif item_type == KIDDY:
                kongs = memory_data.get(DKC3Memory.unlocks)[0]
                kongs |= 0x02
                snes_buffered_write(ctx, DKC3_SRAM, kongs.to_bytes(1, "little"))

            elif item_type == VEHICLE:
                vehicles = int.from_bytes(memory_data.get(DKC3Memory.vehicles), "little")
                if (vehicles & HOVERCRAFT) == 0:
                    vehicles |= HOVERCRAFT
                elif (vehicles & TURBO_SKI) == 0:
                    vehicles |= TURBO_SKI
                elif (vehicles & GYROCOPTER) == 0:
                    vehicles |= GYROCOPTER
                snes_buffered_write(ctx, WRAM_START + 0x0611, vehicles.to_bytes(2, "little"))
                
            snes_buffered_write(ctx, DKC3_SRAM + 0x2C, recv_index.to_bytes(2, "little"))

        updated_level_flags = False
        updated_banana_birds = False

        for loc_id in ctx.checked_locations:
            if loc_id not in ctx.locations_checked:
                ctx.locations_checked.add(loc_id)

                # Get info from the location ID
                level_id = loc_id >> 24
                loc_type = (loc_id >> 20) & 0x0F
                loc_data = loc_id & 0x000FFFFF

                if loc_type in [0x00, 0x01, 0x02]:
                    # Clears, Bonuses, DK Coins
                    level_flags[level_id] |= loc_data
                    updated_level_flags = True
                elif loc_type == 0x03 and enabled_dk_coin:
                    # DK Coins
                    level_flags[level_id] |= loc_data
                    updated_level_flags = True
                elif loc_type == 0x04 and enabled_kong:
                    # KONG
                    level_flags[level_id] |= loc_data
                    updated_level_flags = True
                elif loc_type == 0x08 and enabled_birds:
                    banana_bird_flags[loc_data] |= 0x02
                    updated_banana_birds = True
        
        if updated_level_flags:
            snes_buffered_write(ctx, WRAM_START + 0x632, bytearray(level_flags))
        if updated_banana_birds:
            snes_buffered_write(ctx, WRAM_START + 0x642, bytearray(banana_bird_flags))

        await snes_flush_writes(ctx)        


    async def handle_energy_link(self, ctx: "SNIContext", memory_data: SnesData[DKC3Memory]):
        from SNIClient import snes_buffered_write, snes_flush_writes

        # Deposits EnergyLink into pool
        energy_packet = int.from_bytes(memory_data.get(DKC3Memory.energy_packet), "little")
        energy_packet = int(energy_packet * DKC3_EXCHANGE_RATE / 10) >> 4
        if energy_packet != 0:
            await ctx.send_msgs([{
                "cmd": "Set", 
                "key": f"EnergyLink{ctx.team}", 
                "slot": ctx.slot,
                "default": 0,
                "operations":
                    [{"operation": "add", "value": energy_packet}],
            }])
            snes_buffered_write(ctx, DKC3_ENERGY_PACKET, bytearray([0x00, 0x00]))

        barrels = int.from_bytes(memory_data.get(DKC3Memory.barrel_count), "little")
        
        if self.barrel_request == "place_request":
            self.barrel_request_tag = f"dkc2-dkbarrel-{ctx.team}-{ctx.slot}-{random.randint(0, 0xFFFFFFFF)}"
            value = DK_BARREL_BANANA_COST * DKC3_EXCHANGE_RATE * self.barrel_count
            await ctx.send_msgs([{ 
                "cmd": "Set", 
                "key": f"EnergyLink{ctx.team}", 
                "slot": ctx.slot,
                "tag": self.barrel_request_tag,
                "default": 0,
                "want_reply": True,
                "operations":
                    [{"operation": "add", "value": -value},
                    {"operation": "max", "value": 0}],
            }])
            self.barrel_request = "pending"

        elif self.barrel_request == "successful":
            barrels += self.barrel_count
            barrels &= 0x0FFF
            snes_buffered_write(ctx, DKC3_SRAM + 0x30, bytes([barrels]))
            self.barrel_request = ""
            self.barrel_count = 0
            logger.info(f"Delivered DK Barrel! You have {barrels} barrels pending to be actually delivered in game.")
        
        elif self.barrel_request == "not_enough_funds":
            await ctx.send_msgs([{
                "cmd": "Set", 
                "key": f"EnergyLink{ctx.team}", 
                "slot": ctx.slot,
                "default": 0,
                "operations":
                    [{"operation": "add", "value": self.barrel_request_refund}],
            }])
            self.barrel_request_refund = 0
            self.barrel_request = ""
            logger.info(f"Not enough bananas to summon a barrel! You need at least {DK_BARREL_BANANA_COST * self.barrel_count} bananas.")
            self.barrel_count = 0

        await snes_flush_writes(ctx)

    async def handle_barrel_label(self, ctx: "SNIContext", memory_data: SnesData[DKC3Memory]):
        try:
            from kvui import MDLabel as Label
        except ImportError:
            from kvui import Label

        if not self.barrel_label:
            self.barrel_label = Label(text=f"", size_hint_x=None, width=120, halign="center")
            ctx.ui.connect_layout.add_widget(self.barrel_label)

        barrels = int.from_bytes(memory_data.get(DKC3Memory.barrel_count), "little")
        self.barrel_label.text = f"Barrels: {barrels}"
        

    def on_package(self, ctx: "SNIContext", cmd: str, args: dict):
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            self.slot_data = args.get("slot_data", None)
            self.barrel_request = ""
            if self.slot_data["energy_link"]:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                if ctx.ui:
                    ctx.ui.enable_energy_link()
                    ctx.ui.energy_link_label.text = "Bananas: Standby"
                    snes_logger.info(f"Initialized EnergyLink{ctx.team}")

        elif cmd == "SetReply" and args["key"].startswith("EnergyLink"):
            if self.barrel_request == "pending" and "tag" in args:
                if args["tag"] == self.barrel_request_tag:
                    self.barrel_request_tag = ""
                    dk_barrel_cost = DKC3_EXCHANGE_RATE * DK_BARREL_BANANA_COST * self.barrel_count
                    if args["original_value"] < dk_barrel_cost:
                        # send back the original value
                        value = args["original_value"]
                        self.barrel_request = "not_enough_funds"
                        self.barrel_request_refund = value
                    else: 
                        value = args["value"]
                        self.barrel_request = "successful"
            else: 
                value = args["value"]
                    
            if ctx.ui:
                pool = (value or 0) /  DKC3_EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Bananas: {float(pool):.2f}"

        elif cmd == "Retrieved":
            if f"EnergyLink{ctx.team}" in args["keys"] and args["keys"][f"EnergyLink{ctx.team}"] and ctx.ui:
                pool = (args["keys"][f"EnergyLink{ctx.team}"] or 0) / DKC3_EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Bananas: {float(pool):.2f}"


def cmd_request(self, amount: str = ""):
    """
    Request a DK Barrel from the banana pool (EnergyLink).
    """
    if self.ctx.game != GAME_NAME:
        logger.warning(f"This command can only be used while playing {GAME_NAME}")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if amount:
            try:
                amount = int(amount)
            except ValueError:
                logger.info(f"Please specify a valid number.")
                return
            if amount <= 0:
                logger.info(f"Please specify a number higher than 0.")
                return
            if self.ctx.client_handler.barrel_request != "":
                logger.info(f"You already have a DK Barrel in queue.")
                return
            else:
                self.ctx.client_handler.barrel_request = "place_request"
                self.ctx.client_handler.barrel_count = amount
                logger.info(f"Placing a DK barrel request...")
        else:
            logger.info(f"You need to specify how many Barrels you will request.")
