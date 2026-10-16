"""This module provides an interface for connecting to a pcsx2 game"""
from enum import Enum
from struct import unpack, pack
from typing import Any

from CommonClient import logger
from worlds.rac3.constants.other_ratchets import GAME_ID_TO_OTHER_RATCHET
from worlds.rac3.constants.version import RAC3VERSION
from worlds.rac3.pypine import Pine


class GameInterface:
    """Base class for connecting with a pcsx2 game"""

    class DataType(Enum):
        """Enum class for data types"""
        INT8 = 1
        INT16 = 2
        INT32 = 3
        BYTES = 4
        FLOAT = 5
        STRING = 6

    current_game: str = "None"
    game_id_error: str | None = None
    is_connecting: bool = False
    emulator_connected: bool = False
    cycle_reads_count: int = 0
    cycle_writes_count: int = 0
    cycle_batch_reads_count: int = 0
    cycle_batch_writes_count: int = 0
    cycle_times: list[float] = []
    pypine: Pine = Pine()
    write_batcher: dict[tuple[int, DataType], Any] = {}

    def __init__(self) -> None:
        pass

    @staticmethod
    def bits_to_value(bits: set[int]) -> int:
        """Converts a set of bits into its integer value representation

        :param bits: Set object, members of this set indicate which ordered bits are flipped, first bit is order ``0``
        :return: Integer value
        """
        value: int = 0
        for bit in bits:
            if 0 <= bit <= 7:
                value += 1 << bit
            else:
                raise ValueError(f"Invalid bit position {bit}")
        return value

    @staticmethod
    def value_to_bits(value: int) -> set[int]:
        """Decomposes an integer value into its bit representation, returned as a set object.

        :param value: Integer value
        :return: Set object, members of this set indicate which ordered bits are flipped, first bit is order ``0``
        """
        bits: set[int] = set()
        for i in range(8):
            if value & (1 << i):
                bits.add(i)
        return bits

    def _read8(self, address: int) -> int:
        self.cycle_reads_count += 1
        return self.pypine.read_int8(address)

    def _read16(self, address: int) -> int:
        self.cycle_reads_count += 1
        return self.pypine.read_int16(address)

    def _read32(self, address: int) -> int:
        self.cycle_reads_count += 1
        return self.pypine.read_int32(address)

    def _read8_batch(self, addresses: list[int]) -> list[int]:
        self.cycle_batch_reads_count += 1
        return self.pypine.batch_read_int8(addresses)

    def _read16_batch(self, addresses: list[int]) -> list[int]:
        self.cycle_batch_reads_count += 1
        return self.pypine.batch_read_int16(addresses)

    def _read32_batch(self, addresses: list[int]) -> list[int]:
        self.cycle_batch_reads_count += 1
        return self.pypine.batch_read_int32(addresses)

    def _read_bytes(self, address: int, n: int) -> bytes:
        self.cycle_batch_reads_count += 1
        return self.pypine.read_bytes(address, n)

    def _read_float(self, address: int) -> float:
        self.cycle_reads_count += 1
        return unpack("f", self.pypine.read_bytes(address, 4))[0]

    def _read_string(self, address: int, n: int) -> str:
        self.cycle_batch_reads_count += 1
        return self.pypine.read_string(address, n)

    def batch_write(self):
        """Send all the stashed writes to pypine"""
        batch: list[tuple[Pine.DataSize, int, bytes]] = []
        for (address, operation), value in self.write_batcher.items():
            match operation:
                case self.DataType.INT8:
                    batch.append((self.pypine.DataSize.INT8, address, value.to_bytes(1, "little")))
                case self.DataType.INT16:
                    batch.append((self.pypine.DataSize.INT16, address, value.to_bytes(2, "little")))
                case self.DataType.INT32:
                    batch.append((self.pypine.DataSize.INT32, address, value.to_bytes(4, "little")))
                case self.DataType.BYTES:
                    batch.extend([(size, chunk, value[chunk - address:chunk - address + size]) for size, chunk in
                                  self.pypine._chunks(address, len(value))])
                case self.DataType.FLOAT:
                    batch.append((self.pypine.DataSize.INT32, address, pack("<f", value)))
                case self.DataType.STRING:
                    data = value.encode("ascii") + b"\x00"
                    batch.extend([(size, chunk, data[chunk - address:chunk - address + size]) for size, chunk in
                                  self.pypine._chunks(address, len(data))])
                case _:
                    logger.warning(f"Unknown write operation: {self.DataType(operation)}, "
                                   f"with address+value: {address}, {value}")
        self.cycle_batch_writes_count += len(batch)
        self.pypine.batch_write(batch)
        self.write_batcher.clear()

    def connect_to_game(self):
        """Initializes the connection to PCSX2 and verifies it is connected to the right game"""
        self.is_connecting = True
        logger.debug("Begin attempting emulator connection...")
        try:
            self.pypine.connect()
        except self.pypine.ConnectionError:
            self.is_connecting = False
            self.emulator_connected = False
            logger.debug("No Connection to PCSX2 Emulator")
            return
        except self.pypine.DuplicateConnectionError:
            self.is_connecting = False
            self.emulator_connected = False
            logger.warning("Duplicate connection to PCSX2 Emulator detected")
            return
        self.is_connecting = False
        if not self.pypine.is_connected():
            self.emulator_connected = False
            logger.debug("No Connection to PCSX2 Emulator")
            return
        logger.info("Connected to PCSX2 Emulator")
        self.emulator_connected = True
        self.current_game = "None"
        try:
            self.verify_game_version()
        except RuntimeError:
            logger.warning("PCSX2 Emulator is unreachable")
            self.emulator_connected = False
        except ConnectionError as error:
            logger.warning(f"Connection to PCSX2 Emulator lost: {error}")
            self.emulator_connected = False

    def disconnect_from_game(self):
        """Remove connection to PCSX Emulator"""
        self.pypine.disconnect()
        self.current_game = "None"
        logger.info("Disconnected from PCSX2 Emulator")
        self.emulator_connected = False

    def verify_game_version(self) -> bool:
        """Verify that the current game loaded in the PCSX connection has a valid game ID for Ratchet and Clank 3"""
        # logger.debug("Start Game Verification")
        try:
            game_id = self.pypine.get_game_id()
        except ConnectionError as error:
            logger.debug(f"Game Verify Connection Error: {error}")
            return False
        # The first read of the address will be null if the client is faster than the emulator
        if game_id is None:
            logger.info("No Game Loaded")
            return False
        if game_id != self.current_game:
            logger.info("Detecting new game version...")
            match game_id:
                case RAC3VERSION.US_ID:
                    self.current_game = game_id
                    logger.info("Version Detected: US release")
                case RAC3VERSION.US_GH_ID:
                    self.current_game = game_id
                    logger.info("Version Detected: US Greatest Hits release")
                    logger.warning("WARNING: Game version untested, please inform apworld devs of any "
                                   "inconsistencies found")
                case RAC3VERSION.JP_ID:
                    self.current_game = game_id
                    logger.info("Version Detected: Japanese release")
                    logger.warning("WARNING: JP support is currently in beta, but the game is completable, "
                                   "please inform yuxia228 of any Japanese version-specific issues.")
                case RAC3VERSION.JP_TB_ID:
                    self.current_game = game_id
                    logger.info("Version Detected: Japanese The Best release")
                    logger.warning("WARNING: Game version untested, please inform apworld devs of any "
                                   "inconsistencies found")
                case RAC3VERSION.KO_ID:
                    self.current_game = game_id
                    logger.info("Version Detected: Korean release")
                    logger.warning("WARNING: Game version untested, please inform apworld devs of any "
                                   "inconsistencies found")
                case RAC3VERSION.CH_ID:
                    self.current_game = game_id
                    logger.info("Version Detected: Chinese release")
                    logger.warning("WARNING: Game version untested, please inform apworld devs of any "
                                   "inconsistencies found")
                case RAC3VERSION.EU_ID:
                    self.current_game = game_id
                    logger.info("Version Detected: EU release")
                    logger.warning("WARNING: PAL support is currently in beta, but the game is completable, "
                                   "please inform apworld devs of any inconsistencies found")
                case _:
                    self.current_game = "None"
                    other_ratchet_game = GAME_ID_TO_OTHER_RATCHET.get(game_id)
                    if other_ratchet_game is not None:
                        logger.warning(f"Connected to {other_ratchet_game} instead of Ratchet and Clank 3!\n"
                                       "This client is for Ratchet and Clank 3 only, please load the correct Ratchet "
                                       "game to play.")
                    else:
                        logger.info("Unknown game version detected")
        if self.current_game == "None" and self.game_id_error != game_id and game_id != b"\x00\x00\x00\x00\x00\x00":
            logger.warning(f"Connected to the wrong game ({game_id})")
            self.game_id_error = game_id
            return False
        # logger.debug("Valid Game detected")
        return True

    def get_connection_state(self) -> bool:
        """Safe connection test"""
        try:
            if not self.pypine.is_connected():
                return False
            return self.verify_game_version()
        except RuntimeError:
            return False
