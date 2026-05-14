from collections.abc import Collection
from typing import Optional

from .z80asm.Assembler import GameboyAddress
from .z80asm.Util import hex_str


class RomData:
    """
    A class that creates methods that are necessary for ROM Handling.
    """
    buffer: bytearray

    def __init__(self, file: bytes, name: Optional[str] = None) -> None:
        """
        Loads a rom file when the RomData class is called.

        Parameters:
            file (bytes): A buffer from a rom file.
            name (Optional[str]): The name of the provided file.
        """
        self.file = bytearray(file)
        self.name = name

    def read_bit(self, address: int, bit_number: int) -> bool:
        """
        Reads bit infomation from a memory address and it's number.

        Parameters:
            address (int): A memory address to read from.
            bit_number (int): A number used to determine a boolean statement.

        Returns:
            bool: When a bit is 0, then it's false. True otherwise.
        """
        bitflag = (1 << bit_number)
        return (self.buffer[address] & bitflag) != 0

    def read_byte(self, address: int) -> int:
        """
        Reads a byte from a given memory address.

        Parameters:
            address (int): A memory address to read from

        Returns:
            int: A byte that is returned as a result of reading the memory address.
        """
        return self.file[address]

    def read_bytes(self, start_address: int, length: int) -> bytearray:
        """
        Reads a byte from a given memory address.

        Parameters:
            address (int): A memory address to read from

        Returns:
            bytearray: An array of bytes that are returned as a result of reading the memory address.
        """
        return self.file[start_address:start_address + length]

    def read_word(self, address: int):
        """
        Reads a word from a given memory address.

        Parameters:
            address (int): A memory address to read from

        Returns:
            str: A word that is returned as a result of reading the memory address.
        """
        word_bytes = self.read_bytes(address, 2)
        return (word_bytes[1] * 0x100) + word_bytes[0]

    def write_byte(self, address: int, value: int) -> None:
        """
        Writes down a byte to the ROM.

        Parameters:
            address (int): A memory address used for writing.
            value (int): A value that will be written to the provided memory address.
        """
        self.file[address] = value

    def write_bytes(self, start_address: int, values: Collection[int]) -> None:
        """
        Writes down bytes to the ROM.

        Parameters:
            address (int): A memory address used for writing.
            values (Collection[int]): Values that will be written to the provided memory address.
        """
        self.file[start_address:start_address + len(values)] = values

    def write_word(self, address: int, value: int) -> None:
        """
        Writes down a word to the ROM.

        Parameters:
            address (int): A memory address used for writing.
            value (int): A value that will be written to the provided memory address.
        """
        value = value & 0xFFFF
        self.write_bytes(address, [value & 0xFF, (value >> 8) & 0xFF])

    def write_word_be(self, address: int, value: int) -> None:
        """
        Writes down a word to the ROM with a different method.

        Parameters:
            address (int): A memory address used for writing.
            value (int): A value that will be written to the provided memory address.
        """
        value = value & 0xFFFF
        self.write_bytes(address, [(value >> 8) & 0xFF, value & 0xFF])

    def add_bank(self, fill: int) -> None:
        """
        Adds a bank to the ROM

        Parameters:
            fill (int): A bank number that will be written to the ROM
        """
        self.file.extend([fill] * 0x4000)

    def update_header_checksum(self) -> None:
        """
        Updates the 8-bit checksum for ROM data located in the rom header.
        """
        result = -0x19
        for b in self.read_bytes(0x134, 0x19):
            result -= int(b)
        self.write_byte(0x14D, result & 0xFF)

    def update_checksum(self, address: int):
        """
        Updates the 16-bit checksum for ROM data located in the rom header.
        This is calculated by summing the non-global-checksum bytes in the rom.
        This must not be confused with the header checksum, which is the byte before.

        Parameters:
            address (int): The memory address used for updating a game's checksum.
        """
        result = 0
        for b in self.read_bytes(0x0, address):
            result += b
        for b in self.read_bytes(address + 2, 0xffffff):
            result += b
        result &= 0xffff
        self.write_word_be(address, result & 0xffff)

    def update_rom_size(self) -> None:
        """
         Updates the ROM size for ROM data located in the rom header.
        """
        if len(self.file) == 0x100000:
            self.write_byte(0x148, 0x05)
        elif len(self.file) == 0x200000:
            self.write_byte(0x148, 0x06)
        else:
            raise ValueError(f"Invalid ROM size: {hex(len(self.file))}")

    def get_chest_addr(self, group_and_room: int, bank: int, table_addr: int) -> int:
        """
        Return the address where to edit item ID and sub-ID to modify the contents
        of the chest contained in given room of given group

        Parameters:
            bank (int): The memory address of a bank.
            table_addr (int): The memory address from the chestDataGroupTable inside a bank

        Returns:
            int: The address of a treasure chest.

        Raises:
            Exception: Unknown chest in room {GROUP}|{ROOM}
        """
        base_addr = GameboyAddress(bank, table_addr).address_in_rom()
        room = group_and_room & 0xFF
        group = group_and_room >> 8
        current_addr = GameboyAddress(bank, self.read_word(base_addr + (group * 2))).address_in_rom()
        while self.read_byte(current_addr) != 0xff:
            chest_room = self.read_byte(current_addr + 1)
            if chest_room == room:
                return current_addr + 2
            current_addr += 4
        raise Exception(f"Unknown chest in room {group}|{hex_str(room)}")

    def output(self) -> bytes:
        """
        Gives the user an output of the ROM.

        Returns:
            bytes: A buffer of a ROM.
        """
        return bytes(self.file)
