"""
This module defines a class RabiRibiMemoryIO, which attaches
itself to an open Rabi Ribi process and reads/writes memory
in realtime. This is used to:
 - Recognize when a player gets an item
 - Write items to the player's inventory
 - Handle in game flags when a player recieves an AP item.
 - Modify map data loaded into memory.
 - etc... 
"""
import asyncio
import struct
from typing import List, Tuple

from pymem import pymem

from CommonClient import logger

OFFSET_AREA_ID = int(0x00DDBFA0)
OFFSET_PLAYER_X = int(0x010736C8)
OFFSET_PLAYER_Y = int(0x013EEF00)
OFFSET_GIVE_ITEM_FUNC = int(0x00016FA0)
OFFSET_PLAYER_FROZEN = int(0x01083190)
OFFSET_EVENT_MAP = int(0x00E0D200)
OFFSET_ITEM_MAP = int(0x00E3EB5C)
OFFSET_INVENTORY_START = int(0x016B200C)
OFFSET_EVENT_START = int(0x016B281C)
OFFSET_EGG_START = int(0x016BBDC0)
# This is not max health, player state + 4F0 is
# Used to know if we're on the main menu atm though, so not touching
OFFSET_MAX_HEALTH = int(0x1725DD4) 
OFFSET_PLAYER_PAUSED = int(0x01070E04)
OFFSET_SCENERIO_INDICATOR = int(0x00E6F8A0)
OFFSET_IN_ITEM_GET_ANIMATION = int(0x01724A94)
OFFSET_IN_WARP_MENU = int(0x01724C68)
OFFSET_IN_COSTUME_MENU = int(0x01725BD0)
OFFSET_IN_SAVE_MENU = int(0x01768F88)
OFFSET_CURRENT_WARP_ID = int(0x01725DB8)
 # returns a memory address where various state is stored
OFFSET_PLAYER_STATE = int(0x016C13D8)
# offset from the address from OFFSET_PLAYER_STATE
OFFSET_PLAYER_STATE_HEALTH = int(0x4E0)
EXCLAMATION_POINT_ITEM_ID = 43
UNUSED_ITEM_ID_48 = 48
EVENT_FLAG_ID_START = 255
TILE_LENGTH = 64
EGG_ARRAY_LENGTH = 80 * 3 * 2 # 80 eggs stored as 3 shorts

class RabiRibiMemoryIO():
    """
    RabiRibiMemoryIO serves as an interface for reading/writing memory to and from
    a rabi-ribi game instance.
    """

    def __init__(self):
        self.rr_mem = None
        self.rr_process_id = None
        self.addr_injected_give_item_entrypoint = None

    def is_connected(self):
        if self.rr_mem is None:
            return False
        # confirm the process is still running
        try:
            self._read_int(OFFSET_AREA_ID)
        except pymem.exception.ProcessError:
            logger.info("Lost connection with rabi ribi game.")
            self.rr_process_id = None
            self.rr_mem = None
            return False
        return True

    async def connect(self, exit_event: asyncio.Event):
        logger.info("Waiting for connection to Rabi Ribi game instance...")
        while not exit_event.is_set():
            try:
                self.rr_mem = pymem.Pymem("rabiribi.exe")
                self.rr_process_id = self.rr_mem.process_id
                self.allocate()
                logger.info("Successfully connected to Rabi Ribi Game.")
                return
            except pymem.exception.ProcessNotFound:
                await asyncio.sleep(3)

    def allocate(self):
        self.addr_injected_give_item_entrypoint = self.rr_mem.allocate(12)

    def _read_word(self, offset):
        """
        Read 4 bytes of data at <base_process_address> + offset and return it.

        :int offset: the offset to read data from.
        :returns: The data represented as a byte string
        """
        
        data = self.rr_mem.read_bytes(self.rr_mem.base_address + offset, 4)
        return data
    
    def _read_short(self, offset):
        """
        Read 2 bytes of data at <base_process_address> + offset and return it.

        :int offset: the offset to read data from.
        :returns: The data represented as a byte string
        """

        data = self.rr_mem.read_bytes(self.rr_mem.base_address + offset, 2)
        return data
    
    def _read_byte(self, offset):
        """
        Read 1 byte of data at <base_process_address> + offset and return it.

        :int offset: the offset to read data from.
        """
        data = self.rr_mem.read_bytes(self.rr_mem.base_address + offset, 1)
        return data
    
    def _read_string(self, offset, length):
        data = self.rr_mem.read_bytes(self.rr_mem.base_address + offset, length)
        return data.decode("utf-8")

    def _read_float(self, offset):
        """
        Read a word at the specified offset, and interpret it as a float.

        :int offset: the offset to read data from.
        :returns: The data represented as a float.
        """
        data = self._read_word(offset)
        return struct.unpack("f", data)[0]

    def _read_int(self, offset):
        """
        Read a word at the specified offset, and interpret it as an int.

        :int offset: the offset to read data from.
        :returns: The data represented as a float.
        """
        data = self._read_word(offset)
        return struct.unpack("i", data)[0]

    def _read_4_byte_bool(self, offset):
        """
        Read a word at the specified offset, and interpret it as a bool

        :int offset: the offset to read data from.
        :returns: The data represented as a float.
        """
        data = self._read_word(offset)
        if (struct.unpack("i", data)[0] == 0):
            return False
        return True

    def _read_1_byte_bool(self, offset):
        data = self._read_byte(offset)
        if (struct.unpack("?", data)[0] == 0):
            return False
        return True

    def _read_4_byte_bool_raw(self, address):
        """
        Read a word at the specified address, and interpret it as a bool

        :int address: the address to read data from.
        :returns: The data represented as a float.
        """
        data = self.rr_mem.read_bytes(address, 4)
        if (struct.unpack("i", data)[0] == 0):
            return False
        return True
        

    def read_player_tile_position(self):
        """
        Read the player (area_id,x,y) and convert it to tile (area_id,x,y).

        :returns: The tile position represented as an integer 2-tuple
        """
        area_id = self._read_int(OFFSET_AREA_ID)
        player_x = self._read_float(OFFSET_PLAYER_X)
        player_y = self._read_float(OFFSET_PLAYER_Y)

        # Round to nearest tile
        if (player_x % TILE_LENGTH >= (TILE_LENGTH / 2)):
            player_x += (TILE_LENGTH / 2)
        if (player_y % TILE_LENGTH >= (TILE_LENGTH / 2)):
            player_y += (TILE_LENGTH / 2)

        return (int(area_id), int(player_x // TILE_LENGTH), int(player_y // TILE_LENGTH))
    
    def read_tile_event_id(self, x:int, y:int):
        """
        Read the event ID associated with a specific tile

        :x: x position of the tile
        :y: y position of the tile
        :returns: event id of the tile
        """

        event_tile_offset = (
            OFFSET_EVENT_MAP +
            (((x * 200) + y) * 2)
        )

        data = self._read_short(event_tile_offset)
        return struct.unpack("h", data)[0]

    def is_player_frozen(self):
        """
        Returns True if the player is frozen.
        Frozen counts as losing control of a player (e.g. "you just got item! animation")
        or being in a menu.

        This is used to know when we are safe to do certain actions, like give items to the player.
        """
        return self._read_4_byte_bool(OFFSET_PLAYER_FROZEN) or not self._read_4_byte_bool(OFFSET_MAX_HEALTH) or self.is_player_paused()
    
    def is_player_paused(self):
        """
        Returns true if the player is currently in a menu
        """
        return self._read_4_byte_bool(OFFSET_PLAYER_PAUSED)

    def is_in_item_receive_animation(self):
        return self._read_1_byte_bool(OFFSET_IN_ITEM_GET_ANIMATION)
    
    def is_near_crosswarp(self):
        """
        Returns true if the player is currently within 1 tile of a crosswarp tile
        """
        player_pos = self.read_player_tile_position()
        
        for x in range(-1,2):
            for y in range(-1, 2):
                event_id = self.read_tile_event_id(player_pos[1] + x, player_pos[2] + y)
                if 241 <= event_id <= 251:
                    return True
                
        return False

    def give_item(self, item_id):
        """
        Run the in-game give-item function. We do this by injecting our own code
        which calls the func (setting the correct parameters in the registers),
        and then running a thread at the startpoint of our injected code.

        :int item_id: the rabi-ribi id of the item to give to the player
        :returns: None
        """
        addr_give_item_func = self.rr_mem.base_address + OFFSET_GIVE_ITEM_FUNC
        # We need the relative address for the x86 call instruction.
        # subtract 10 because our injected code traverses 10 bytes before we
        # desired address
        addr_give_item_func = addr_give_item_func - self.addr_injected_give_item_entrypoint - 10

        """
        The below code uses keystone to compile our desired assembly code. But since
        .apworlds dont support external depedencies at the moment, we'll write the bytes
        manually.
        """
        # convert our assembly code to bytes
        # architecture = keystone.KS_ARCH_X86
        # mode = keystone.KS_MODE_32
        # endianess = keystone.KS_MODE_LITTLE_ENDIAN
        # ks = keystone.Ks(architecture, mode | endianess)
        # injected_call_func_code = f"mov ecx,{item_id}; call {addr_give_item_func}; ret".encode()
        # injected_call_func_code, _ = ks.asm(injected_call_func_code)
        # injected_call_func_code = bytes(injected_call_func_code)

        """
        Notation:
            185: mov instruction
            next 4 bytes: the little endian integer value of the item_id
            232: call instruction
            next 4 bytes: the relative address we want to call
            195: ret instruction
        """
        addr_give_item_func =  int(addr_give_item_func).to_bytes(4, byteorder='little', signed=True)
        injected_call_func_code = [185] + list(struct.pack('<i', item_id)) + [232] + list(addr_give_item_func) + [195]
        injected_call_func_code = bytes(injected_call_func_code)

        # write our code to memory
        self.rr_mem.write_bytes(
            self.addr_injected_give_item_entrypoint, 
            injected_call_func_code,
            len(injected_call_func_code)
        )

        # start a thread at the entrypoint of our injected code
        self.rr_mem.start_thread(self.addr_injected_give_item_entrypoint)

    def remove_exclamation_point_from_in_memory_map(self, area_id: int, x: int, y: int):
        """
        This method sets a specific tile on the map loaded into memory to having no item
        on it. This is used to delete items from the map when the player collects an item
        for another world.

        :int area_id: the area id of the location
        :int x: the x coordinate of the item
        :int y: the y coordinate of the item
        """
        map_tile_item_info_offset = (
            self.rr_mem.base_address +
            OFFSET_ITEM_MAP +
            (((x * 200) + y) * 2)
        )
        current_item = self.rr_mem.read_short(map_tile_item_info_offset)
        if current_item == EXCLAMATION_POINT_ITEM_ID:
            self.rr_mem.write_short(map_tile_item_info_offset, 0)

    def remove_exclamation_point_from_inventory(self):
        """
        Removes the exclamation point item (used to represent items from other worlds)
        from the player's inventory.
        """
        self.set_item_state(EXCLAMATION_POINT_ITEM_ID, 0)

    def does_player_have_item_id(self, item_id) -> bool:
        """
        Returns true if player currently has item_id in their inventory.
        """
        return self._read_4_byte_bool(OFFSET_INVENTORY_START + (4 * int(item_id)))

    def get_item_state(self, item_id) -> int:
        """
        Returns the state of an item in the player's inventory.

        If 0, the player does not have the item.
        If 1, the player does have the item.
        If 2 or 3, the player has the item, along with an upgrade.
        If -1, -2, or -3, the player has the item, but has disabled it.
        """
        return self._read_int(OFFSET_INVENTORY_START + (4 * int(item_id)))

    def set_item_state(self, item_id, state):
        """
        Returns the state of an item in the player's inventory.

        If 0, the player does not have the item.
        If 1, the player does have the item.
        If 2 or 3, the player has the item, along with an upgrade.
        If -1, -2, or -3, the player has the item, but has disabled it.
        """
        self.rr_mem.write_int(self.rr_mem.base_address + OFFSET_INVENTORY_START + (4 * int(item_id)), state)

    def get_last_received_item_index(self):
        """
        Gets the index of the last item received from the recieved items list.
        """
        return self.get_item_state(UNUSED_ITEM_ID_48)

    def set_last_received_item_index(self, index):
        """
        Sets the index of the last item received from the recieved items list.
        """
        self.set_item_state(UNUSED_ITEM_ID_48, index)

    def set_event_state(self, event_id: int, state: bool):
        """
        Sets the state of the given event flag ID.
        """
        address = self.rr_mem.base_address + OFFSET_EVENT_START + (4 * (event_id - EVENT_FLAG_ID_START))
        value = 1 if state else 0
        self.rr_mem.write_int(address, value)

    def open_warp_menu(self):
        """
        Opens the warp menu.
        """
        self.rr_mem.write_int(self.rr_mem.base_address + OFFSET_IN_WARP_MENU, 1)

        # When using the warp menu, the player cannot select to warp to their current location.
        # Since we're opening the menu in a random location, we need to set the current location to not be 0
        # to allow warping to Starting Forest. Using -1 allows all warps to be selected.
        self.rr_mem.write_int(self.rr_mem.base_address + OFFSET_CURRENT_WARP_ID, -1)

    def get_collected_eggs(self) -> List[Tuple[int, int, int]]:
        """
        Returns the locations of all eggs collected by the player.
        """
        data = self.rr_mem.read_bytes(self.rr_mem.base_address + OFFSET_EGG_START, EGG_ARRAY_LENGTH)
        eggs: List[Tuple[int, int, int]] = list(struct.iter_unpack('3h', data))

        # Check if the player has 80 eggs
        if (0,0,0) not in eggs:
            return eggs

        egg_count = eggs.index((0,0,0))

        if egg_count >= 0:
            eggs = eggs[:egg_count]

        return eggs

    def get_number_of_eggs_collected(self) -> int:
        """
        Returns the number of eggs the player currently has.
        """
        return len(self.get_collected_eggs())

    def is_on_correct_scenerio(self, scenerio_id: str) -> bool:
        """
        Used for sanity checking that we're on the correct file.
        """
        return self._read_string(OFFSET_SCENERIO_INDICATOR, len(scenerio_id)) == scenerio_id
    
    def is_on_main_menu(self) -> bool:
        """
        True if the player isnt loaded into a game.
        """
        return not self._read_4_byte_bool(OFFSET_MAX_HEALTH) and not self.is_player_paused()

    def is_in_save_menu(self) -> bool:
        """
        True if the player is in the save game menu.
        """
        return self._read_1_byte_bool(OFFSET_IN_SAVE_MENU)

    def is_in_warp_menu(self) -> bool:
        """
        True if the player is currently selecting a warp
        """
        return self._read_4_byte_bool(OFFSET_IN_WARP_MENU)

    def is_in_costume_menu(self) -> bool:
        """
        True if the player is currently selecting a costume
        """
        return self._read_4_byte_bool(OFFSET_IN_COSTUME_MENU)

    def has_zero_health(self) -> bool:
        """
        True if the player's health is at 0
        """
        player_state_health_address = self._read_int(OFFSET_PLAYER_STATE) + OFFSET_PLAYER_STATE_HEALTH 
        return not self._read_4_byte_bool_raw(player_state_health_address)

    def set_player_health_to_zero(self):
        """
        Sets the player health to 0
        """
        player_state_health_address = self._read_int(OFFSET_PLAYER_STATE) + OFFSET_PLAYER_STATE_HEALTH
        self.rr_mem.write_int(player_state_health_address, 0)
