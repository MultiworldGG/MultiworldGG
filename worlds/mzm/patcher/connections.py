from enum import Enum, IntEnum
import struct
from typing import NamedTuple

from .constants import Area
from .local_rom import LocalRom, get_rom_address


class ConnectionType(Enum):
    DOOR = 0
    OPEN = 1
    ELEVATOR = 2


class Direction(IntEnum):
    RIGHT = 1 << 4
    LEFT = 1 << 5
    UP = 1 << 6
    DOWN = 1 << 7

    def inverse(self):
        if self & (self.RIGHT | self.LEFT):
            return type(self)(self ^ (self.RIGHT | self.LEFT))
        else:
            return type(self)(self ^ (self.UP | self.DOWN))


class ConnectionData(NamedTuple):
    door_index: int
    area_connection_index: int
    connection_type: ConnectionType
    direction: Direction


CONNECTION_DATA: dict[str, dict[str, ConnectionData]] = {
    "Brinstar": {
        "Transport to Norfair": ConnectionData(57, 2, ConnectionType.ELEVATOR, Direction.DOWN),
        "Transport to Tourian": ConnectionData(61, 4, ConnectionType.ELEVATOR, Direction.DOWN),
        "Transport to Kraid": ConnectionData(9, 6, ConnectionType.ELEVATOR, Direction.DOWN),
        "Entry Cavern": ConnectionData(0, 8, ConnectionType.OPEN, Direction.UP),
    },
    "Kraid": {
        "Transport to Brinstar": ConnectionData(0, 7, ConnectionType.ELEVATOR, Direction.UP),
        "Save Room Kraid D": ConnectionData(103, 23, ConnectionType.OPEN, Direction.RIGHT),
    },
    "Norfair": {
        "Transport to Ridley": ConnectionData(70, 0, ConnectionType.ELEVATOR, Direction.DOWN),
        "Transport to Brinstar": ConnectionData(0, 3, ConnectionType.ELEVATOR, Direction.UP),
        "Transport to Crateria": ConnectionData(76, 13, ConnectionType.ELEVATOR, Direction.UP),
        "Imago Larva Arena": ConnectionData(108, 17, ConnectionType.OPEN, Direction.DOWN),
        "Accessway": ConnectionData(129, 22, ConnectionType.OPEN, Direction.LEFT),
    },
    "Ridley": {
        "Transport to Norfair": ConnectionData(0, 1, ConnectionType.ELEVATOR, Direction.UP),
        "Insect Tunnel": ConnectionData(60, 18, ConnectionType.OPEN, Direction.UP),
    },
    "Tourian": {
        "Transport to Brinstar": ConnectionData(0, 5, ConnectionType.ELEVATOR, Direction.UP),
        # "Escape Shaft": ConnectionData(11, 11, ConnectionType.ELEVATOR, Direction.UP),  # Escape
        "Escape Shaft": ConnectionData(21, 16, ConnectionType.ELEVATOR, Direction.UP),  # Ruined
    },
    "Crateria": {
        "Transport to Brinstar": ConnectionData(11, 9, ConnectionType.OPEN, Direction.DOWN),
        # "Transport to Tourian": ConnectionData(13, 10, ConnectionType.ELEVATOR, Direction.DOWN),  # Escape
        "Transport to Norfair": ConnectionData(17, 12, ConnectionType.ELEVATOR, Direction.DOWN),
        "Ship Entryway": ConnectionData(33, 14, ConnectionType.OPEN, Direction.RIGHT),
        "Ruins Entryway": ConnectionData(24, 20, ConnectionType.OPEN, Direction.RIGHT),
        # "Ruins Entryway": ConnectionData(49, 21, ConnectionType.OPEN, Direction.RIGHT),  # Duped room, unused?
        "Transport to Tourian": ConnectionData(51, 24, ConnectionType.ELEVATOR, Direction.DOWN),  # Ruined
    },
    "Chozodia": {
        "Escape Tunnel": ConnectionData(150, 15, ConnectionType.OPEN, Direction.LEFT),
        "Crossway": ConnectionData(220, 19, ConnectionType.OPEN, Direction.LEFT),
    },
}


def apply_connections(rom: LocalRom, connections: dict[str, str]):
    for source, destination in connections.items():
        try:
            source_area, source_room = source.split(" - ")
            source_data = CONNECTION_DATA[source_area][source_room]
        except KeyError:
            source_data = None
        try:
            dest_area, dest_room = destination.split(" - ")
            destination_data = CONNECTION_DATA[dest_area][dest_room]
        except (KeyError, ValueError):
            destination_data = None
        _apply_connection(rom, (source, source_data), (destination, destination_data))


def _apply_connection(
    rom: LocalRom,
    source: tuple[str, ConnectionData | None],
    destination: tuple[str, ConnectionData | None],
):
    source_name, source_data = source
    if source_data is None:
        raise KeyError(source_name)
    source_area = source_name.split(" - ")[0]
    destination_name, destination_data = destination
    if destination_data is None:
        raise KeyError(destination_name)
    destination_area = Area[destination_name.split(" - ")[0].upper()]
    error_message = f"Could not connect {source_name} and {destination_name}: "

    if source_data.connection_type != destination_data.connection_type:
        raise ValueError(error_message + "must be connected the same way")
    if (
        source_data.connection_type != ConnectionType.ELEVATOR
        and destination_data.direction != source_data.direction.inverse()
    ):
        raise ValueError(error_message + "connecting non-elevators with the same direction")
    elif destination_data.direction != source_data.direction.inverse():
        raise NotImplementedError(error_message + "connecting elevators with the same direction")

    rom.write(
        get_rom_address(f"s{source_area}Doors", 12 * source_data.door_index + 6),
        struct.pack("<B", destination_data.door_index),
    )
    rom.write(
        get_rom_address("sAreaConnections", 3 * source_data.area_connection_index + 2),
        struct.pack("<B", destination_area),
    )
