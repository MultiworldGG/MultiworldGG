from enum import  IntEnum
from typing import Optional, Dict
import struct
from logging import Logger
import asyncio
import random

from worlds.sly1.Locations import bottle_amounts, minigame_locations
from worlds.sly1.data.Constants import ADDRESSES, LEVELS
from worlds.sly1.pcsx2_interface.pine import Pine

class Sly1Episode(IntEnum):
    Paris = 0
    Tide_of_Terror = 1
    Sunset_Snake_Eyes = 2
    Vicious_Voodoo = 3
    Fire_in_the_Sky = 4
    Cold_Heart_of_Hate = 5

class GameInterface:
    """
    Base class for connecting with a pcsx2 game
    """

    pcsx2_interface: Pine = Pine()
    logger: Logger
    game_id_error: Optional[str] = None
    current_game: Optional[str] = None
    addresses: Dict = {}

    def __init__(self, logger) -> None:
        self.logger = logger

    def _read8(self, address: int):
        return self.pcsx2_interface.read_int8(address)

    def _read16(self, address: int):
        return self.pcsx2_interface.read_int16(address)

    def _read32(self, address: int):
        return self.pcsx2_interface.read_int32(address)

    def _read_bytes(self, address: int, n: int):
        return self.pcsx2_interface.read_bytes(address, n)

    def _read_float(self, address: int):
        return struct.unpack("f",self.pcsx2_interface.read_bytes(address, 4))[0]

    def _write8(self, address: int, value: int):
        self.pcsx2_interface.write_int8(address, value)

    def _write16(self, address: int, value: int):
        self.pcsx2_interface.write_int16(address, value)

    def _write32(self, address: int, value: int):
        self.pcsx2_interface.write_int32(address, value)

    def _write_bytes(self, address: int, value: bytes):
        self.pcsx2_interface.write_bytes(address, value)

    def _write_float(self, address: int, value: float):
        self.pcsx2_interface.write_float(address, value)

    def _write_u32(self, address: int, value: int):
        value = value & 0xFFFFFFFF  # truncate to 32-bit unsigned
        value_bytes = value.to_bytes(4, byteorder='little', signed=False)
        self._write_bytes(address, value_bytes)

    def _write_u64(self, address: int, value: int):
        if value < 0 or value > 0xFFFFFFFFFFFFFFFF:
            raise ValueError(f"Value {value} out of range for unsigned 64-bit write.")
        value_bytes = value.to_bytes(8, byteorder='little', signed=False)
        self._write_bytes(address, value_bytes)

    def connect_to_game(self):
        """
        Initializes the connection to PCSX2 and verifies it is connected to the
        right game
        """
        if not self.pcsx2_interface.is_connected():
            self.pcsx2_interface.connect()
            if not self.pcsx2_interface.is_connected():
                return
            self.logger.info("Connected to PCSX2 Emulator")
        try:
            game_id = self.pcsx2_interface.get_game_id()
            # The first read of the address will be null if the client is faster than the emulator
            self.current_game = None
            if game_id in ADDRESSES.keys():
                self.current_game = game_id
                self.addresses = ADDRESSES[game_id]
            if self.current_game is None and self.game_id_error != game_id and game_id != b'\x00\x00\x00\x00\x00\x00':
                self.logger.warning(
                    f"Connected to the wrong game ({game_id})")
                self.game_id_error = game_id
        except RuntimeError:
            pass
        except ConnectionError:
            pass

    def disconnect_from_game(self):
        self.pcsx2_interface.disconnect()
        self.current_game = None
        self.logger.info("Disconnected from PCSX2 Emulator")

    def get_connection_state(self) -> bool:
        try:
            connected = self.pcsx2_interface.is_connected()
            return connected and self.current_game is not None
        except RuntimeError:
            return False

class Sly1Interface(GameInterface):
    moves_locked = False
    def get_current_episode(self) -> Sly1Episode:
        episode_num = self._read32(self.addresses["world id"])
        return Sly1Episode(episode_num)

    def in_cutscene(self) -> bool:
        cutscene_pointer = self._read32(self.addresses["cutscene pointer"])
        sly_control = self._read32(self.addresses["sly control"])
        return cutscene_pointer > 0 and sly_control != 7

    def in_controllable_cutscene(self):
        cutscene_pointer = self._read32(self.addresses["cutscene pointer"])
        return cutscene_pointer > 0

    def in_call(self) -> bool:
        binocucom = self._read32(self.addresses["binocucom"])
        return binocucom == 2

    def in_fmv(self) -> bool:
        fmv = self._read32(self.addresses["FMV"])
        return fmv > 20

    def get_button_press(self) -> int:
        button = self._read32(self.addresses["button pressed"])
        return button

    def skip_cutscene(self, ctx: 'Sly1Context') -> None:
        if ctx.slot_data is None:
            return

        if self.in_cutscene() and ctx.slot_data.get("CutsceneSkip", 1) == 1:
            cutscene_pointer = self._read32(self.addresses["cutscene pointer"])
            self._write32(cutscene_pointer + 744, 0)
        if self.in_call() and ctx.slot_data.get("CutsceneSkip", 1) == 1:
            self._write32(self.addresses["binocucom"], 0)
        if self.in_fmv() and ctx.slot_data.get("CutsceneSkip", 1) == 1:
            self._write32(self.addresses["FMV skip"], 0)
        if self.in_fmv() and self.get_button_press() == 2:
            self._write32(self.addresses["FMV skip"], 0)
        if self.get_button_press() == 2 and self.in_controllable_cutscene():
            cutscene_pointer = self._read32(self.addresses["cutscene pointer"])
            self._write32(cutscene_pointer + 744, 0)

    def get_current_level_name(self) -> str:
        level_addresses = ADDRESSES["SCUS-97198"]["levels"]
        current_address = self.get_current_address()
        current_episode = self.get_current_episode()

        if current_episode in (Sly1Episode.Paris, Sly1Episode.Cold_Heart_of_Hate) or current_address == 8:
            return "N/A"

        episode_index = current_episode - 1
        episode_levels = level_addresses[episode_index]

        return LEVELS[current_episode.name.replace("_", " ")][current_address]

    def get_current_address(self) -> int:
        current_address = self._read32(self.addresses["level id"])
        return current_address

    def check_paris_files(self) -> bool:
        files = self._read32(0x27C66C)
        return files > 0

    def get_sly_struct(self) -> int:
        sly_struct = self._read32(self.addresses["sly struct pointer"])
        return sly_struct

    def get_sly_action(self) -> int:
        sly_struct = self._read32(self.addresses["sly struct pointer"])
        sly_action = self._read32(sly_struct + self.addresses["sly action offset"])
        return sly_action

    def get_active_move(self) -> int:
        active_move = self._read32(self.addresses["active thief move"])
        return active_move

    def get_paused(self) -> bool:
        paused = self._read32(self.addresses["game paused"])
        return paused == 0

    async def write_name_pointers(self) -> None:
        start_value = 0x25EA00
        increment = 50
        current_value = start_value
        name_pointers = self.addresses["name pointers"]
        hub_name_pointers = self.addresses["hub name pointers"]

        for episode in name_pointers:
            for address in episode:
                if address != 0:
                    self._write32(address, current_value)
                    current_value += increment

        for address in hub_name_pointers:
            if address != 0:
                self._write32(address, current_value)
                current_value += increment

    def write_names(self, ctx: 'Sly1Context') -> None:
        addresses = self.addresses["name pointers"]
        hub_addresses = self.addresses["hub name pointers"]
        clue_bundles = ctx.slot_data.get("ItemCluesanityBundleSize", 0)

        if self.get_current_address() == 4 and self.get_current_episode() == 0 and ctx.first_hideout is False:
            ctx.names_dirty = False
            ctx.first_hideout = True

        if self._read32(0x247B98) != 0x25EA00:
            return
        if not ctx.names_dirty:
            return

        for episode_index, (episode_name, level_list) in enumerate(LEVELS.items()):
            for level_index, level_name in enumerate(level_list):
                if addresses[episode_index][level_index] == 0:
                    continue
                pointer_address = self._read32(addresses[episode_index][level_index])
                bottle_count = ctx.bottles[episode_index][level_index] * clue_bundles
                max_bottles = bottle_amounts[level_name].bottle_amount
                if bottle_count > max_bottles:
                    bottle_count = max_bottles
                if clue_bundles > 0:
                    name = f"{level_name} ({bottle_count}/{max_bottles})"
                else:
                    name = f"{level_name}"
                text = name.encode()+bytes([0])
                self._write_bytes(pointer_address, text)

        for episode_index, episode_name in enumerate(LEVELS.keys()):
            pointer_address = self._read32(hub_addresses[episode_index])
            if ctx.hubs[episode_index] is False:
                name = f"{episode_name} (Locked)"
            else:
                name = f"{episode_name}"
            text = name.encode()+bytes([0])
            self._write_bytes(pointer_address, text)

        ctx.names_dirty = False

    def write_anticheat(self):
        addresses = self.addresses["anticheat"]
        for address in addresses:
            if self._read32(address) != 0:
                self._write32(address, 0)
        if self._read32(0x12B760) != 0x03E00008:
            self._write32(0x12B760, 0x03E00008)
        if self._read32(0x12B764) != 0x00000000:
            self._write32(0x12B764, 0x00000000)

    async def activate_trap(self, item_id: int):
        level_name = self.get_current_level_name()
        trap = item_id - 10020025
        current_episode = self.get_current_episode()
        traps = {
            1: self.slide_trap,
            2: self.time_trap,
            3: self.ball_trap,
            4: self.invisibility_trap,
        }

        trap_act = traps.get(trap)
        if trap_act:
            if current_episode == 0 or (level_name + " Key") in minigame_locations:
                asyncio.create_task(self.delayed_trap(item_id))
            else:
                await trap_act()
        else:
            return

    async def delayed_trap(self, trap: int):
        await asyncio.sleep(5)
        await self.activate_trap(trap)

    async def slide_trap(self):
        asyncio.create_task(self.freeze_address(self.addresses["slope control"], 0.7, 1.0))

    async def time_trap(self):
        number = random.randint(1, 2)
        if number == 1:
            asyncio.create_task(self.freeze_address(self.addresses["time control"], 1.5, 1.0))
        if number == 2:
            asyncio.create_task(self.freeze_address(self.addresses["time control"], 0.5, 1.0))

    async def ball_trap(self):
        active_move = self.get_active_move()
        true_moves = self._read32(self.addresses["thief moves"])
        sly_action = self.get_sly_action()
        if sly_action >= 3:
            await asyncio.sleep(1)
            await self.ball_trap()
        self.moves_locked = True
        asyncio.create_task(self.freeze_multiple_addresses([self.addresses["thief moves"],
                                                            self.addresses["active thief move"],
                                                            self.addresses["button pressed"],
                                                            self.addresses["button held"],
                                                            self.addresses["button pressed"] + 2],
                                                           [4, 1, 16, 255, 16],
                                                           [true_moves, active_move, 0, 0, 0]))

    async def invisibility_trap(self):
        sly_struct = self.get_sly_struct()
        sly_opacity = sly_struct + self.addresses["sly opacity offset"]
        cane_opacity = sly_struct + self.addresses["cane offset"]
        charm_offset = sly_struct + self.addresses["charm offset"]
        glow_offset = self._read32(charm_offset) + self.addresses["glow offset"]
        glow_value = self._read32(glow_offset)
        sly_shadow = self.addresses["sly shadow"]
        shadow_value = self._read32(sly_shadow)

        asyncio.create_task(self.freeze_address(sly_opacity, -1.0, 1))
        asyncio.create_task(self.freeze_address(sly_shadow, 0, 1))
        asyncio.create_task(self.freeze_address(cane_opacity, 0, 1))
        #asyncio.create_task(self.freeze_address(glow_offset, 0, glow_value))

    async def freeze_address(self, address: int, value: float, reset_value: float,
                             duration: float = 10.0, interval: float = 0.01):
        #original_value = self._read_float(address)
        start_time = asyncio.get_event_loop().time()
        end_time = start_time + duration

        while asyncio.get_event_loop().time() < end_time:
            self._write_float(address, value)
            await asyncio.sleep(interval)

        self._write_float(address, reset_value)

    async def freeze_multiple_addresses(self, addresses: list, values: list, reset_values: list,
                                        duration: float = 10.0, interval: float = 0.01):
        if len(addresses) != len(values):
            raise ValueError("The number of addresses must match the number of values.")

        #original_values = [self._read32(address) for address in addresses]

        start_time = asyncio.get_event_loop().time()
        end_time = start_time + duration

        while asyncio.get_event_loop().time() < end_time:
            for i, address in enumerate(addresses):
                self._write32(address, values[i])
            await asyncio.sleep(interval)

        # Restore the original values after the duration
        for i, address in enumerate(addresses):
            self._write32(address, reset_values[i])
        self.moves_locked = False

