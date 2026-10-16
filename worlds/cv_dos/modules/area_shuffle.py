from enum import IntEnum
from typing import NamedTuple
import struct

from BaseClasses import EntranceType
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances


class DoorTransitionData(NamedTuple):
    # Left-facing doors should use the right exit of the connecting Transition room.
    # Right facing doors should pull the data of the connecting room
    source_pointer: int  # Pointer to this door's data field in arm9.
    room_pointer: int  # Pointer to which room this door belongs to
    x_pos: int  # X-Position of this door
    y_pos: int  # Y-Position of this door
    entrance_name: str
    is_left_facing: bool = False


castle_entrances = [
    "Sec00Rm07",  # Lost Village -> Demon Guest House (Numbers West)
    "Sec00Rm15",  # Lost Village -> Wizardry Lab (Moat door)
    "Sec00Rm16",  # Lost Village -> Dem Guest House (Lower)
    "Sec00Rm0DObj03",  # Lost Village -> Wizardry Lab (West Gate)
    "Sec00Rm0DObj04",  # Lost Village -> Wizardry Lab (Underwater)

    "Sec01Rm04",  # Demon Guest House -> Lost Village (Tall room)
    "Sec01Rm2A",  # Demon Guest House -> Lost Village (Lower entrance)
    "Sec01Rm30",  # Demon Guest House -> Garden of Madness (Central)
    "Sec01Rm3F",  # Demon Guest House -> Garden of Madness (Dario area)
    "Sec01Rm33",  # Demon Guest House -> Pinnacle (West Exit)

    "Sec02Rm07",  # Wizardry Lab -> Lost Village (Moat)
    "Sec02Rm10",  # Wizardry Lab -> Subterranean Hell (East Gate)
    "Sec02Rm15",  # Wizardry Lab -> Garden of Madness (Lower Door)
    "Sec02Rm00",  # Wizardry Lab -> Lost Village (West Gate)
    "Sec02Rm18",  # Wizardry Lab -> Lost Village (Underwater west side)
    "Sec02Rm1E",  # Wizardry Lab -> Subterranean Hell (Underwater east side

    "Sec03Rm00",  # Garden of Madness -> Demon Guest House (Lower, east)
    "Sec03Rm09",  # Garden of Madness -> Wizardry Lab (Balore blocks exit)
    "Sec03Rm13",  # Garden of Madness -> Subterranean Hell (Through water tunnel)
    "Sec03Rm16",  # Garden of Madness -> Dark Chapel (East Exit)
    "Sec03Rm10",  # Garden of Madness -> Cursed Clock Tower (Past upper gate)
    "Sec03Rm05",  # Garden of Madness -> Demon Guest House (Past dario)

    "Sec04Rm03",  # Dark Chapel -> Garden of madness (west exit)
    "Sec04Rm15",  # Dark Chapel -> Condemned Tower (east exit)
    "Sec04Rm08",  # Dark Chapel -> Subterranean Hell (Catacombs exit)

    "Sec05Rm00",  # Condemned Tower -> Cursed Clock Tower (Upper exit)
    "Sec05Rm01",  # Condemned Tower -> Dark Chapel (Lower exit)

    "Sec06Rm00",  # Sub. Hell -> Wizardry Lab (Spike Room)
    "Sec06Rm01",  # Sub. Hell -> Wizardry Lab (Above waterfall)
    "Sec06Rm06",  # Sub. Hell -> Silenced Ruins (Lower Door)
    "Sec06Rm0E",  # Sub. Hell -> Garden of Madness (Central door)
    "Sec06Rm11",  # Sub. Hell -> Silenced Ruins (Gate)
    "Sec06Rm13",  # Sub. Hell -> Dark Chapel (Rahab door)

    "Sec07Rm00",  # Silenced Ruins -> Sub. Hell (Timestop room)
    "Sec07Rm08",  # Silenced Ruins -> Sub. Hell (back)

    "Sec08Rm1E",  # CCT -> Condemned Tower (East Exit)
    "Sec08Rm02",  # CCT -> Garden of madness (West lower)
    "Sec08Rm06",  # CCT -> Pinnacle (Spike hall)

    "Sec09Rm1A",  # Pinnacle -> Cursed Clock Tower (East exit)
    "Sec09Rm07"  # Pinnacle -> Demon Guest House (West exit)
]

door_data = {
    "Sec00Rm07": DoorTransitionData(0x020A5214, 0x020A5224, 0x00, 0x00, "Lost Village: Highest Door", True),
    "Sec01Rm04": DoorTransitionData(0x020A1BEC, 0x020A1C0C, 0x00, 0x00, "Demon Guest House: Number Puzzle West Door"),

    "Sec00Rm15": DoorTransitionData(0x020A8C58, 0x020A8C68, 0x00, 0x00, "Lost Village: Moat Door", True),
    "Sec02Rm07": DoorTransitionData(0x020A6E34, 0x020A6DD0, 0x00, 0x00, "Wizardry Lab: Main Entrance"),

    "Sec00Rm16": DoorTransitionData(0x020A5298, 0x020A52A8, 0x00, 0x00, "Lost Village: Courtyard Door", True),
    "Sec01Rm2A": DoorTransitionData(0x020A431C, 0x020A433C, 0x00, 0x00, "Demon Guest House: Lower Left Door"),

    "Sec00Rm0DObj03": DoorTransitionData(0x020A8B50, 0x020A8B60, 0x00, 0x00, "Lost Village: Underground Tunnel Upper Door", True),
    "Sec02Rm00": DoorTransitionData(0x020A64D4, 0x020A64F4, 0x00, 0x00, "Wizardry Lab: Behind West Gate"),

    "Sec00Rm0DObj04": DoorTransitionData(0x020A8BD4, 0x020A8BE4, 0x00, 0x00, "Lost Village: Underground Tunnel Lower Door", True),
    "Sec02Rm18": DoorTransitionData(0x020A8344, 0x020A8364, 0x00, 0x00, "Wizardry Lab: Iron Golem Hall"),

    "Sec01Rm30": DoorTransitionData(0x020ABA40, 0x020ABA50, 0x00, 0x00, "Demon Guest House: Lower Right Door", True),
    "Sec03Rm00": DoorTransitionData(0x020A9C00, 0x020A9B7C, 0x00, 0xC0, "Garden of Madness: Central West Door"),

    "Sec01Rm3F": DoorTransitionData(0x020ABAC4, 0x020ABAD4, 0x00, 0x00, "Demon Guest House: Central Door", True),
    "Sec03Rm05": DoorTransitionData(0x020AA15C, 0x020AA138, 0x00, 0x00, "Garden of Madness: Post-Boss Area"),

    "Sec01Rm33": DoorTransitionData(0x020BAB14, 0x020BAB24, 0x00, 0x00, "Demon Guest House: Upper Exit", True),
    "Sec09Rm07": DoorTransitionData(0x020B9854, 0x020B9874, 0x00, 0x00, "The Pinnacle: West Exit"),

    "Sec02Rm10": DoorTransitionData(0x020B3F78, 0x020B3F88, 0x00, 0x00, "Wizardry Lab: East Gate", True),
    "Sec06Rm01": DoorTransitionData(0x020B276C, 0x020B278C, 0x00, 0x00, "Subterranean Hell: Above Waterfall"),

    "Sec02Rm15": DoorTransitionData(0x020ABB48, 0x020ABB58, 0x00, 0x00, "Wizardry Lab: East Exit", True),
    "Sec03Rm09": DoorTransitionData(0x020AA5EC, 0x020AA598, 0x00, 0x0240, "Garden of Madness: Lower West Door"),

    "Sec02Rm1E": DoorTransitionData(0x020B3EF4, 0x020B3F04, 0x00, 0x00, "Wizardry Lab: East Underwater Room Door", True),
    "Sec06Rm00": DoorTransitionData(0x020B2670, 0x020B2690, 0x00, 0x00, "Subterranean Hell: Spikes Chamber"),

    "Sec03Rm13": DoorTransitionData(0x020ABC50, 0x020ABC60, 0x00, 0x00, "Garden of Madness: Water-locked Door", True),
    "Sec06Rm0E": DoorTransitionData(0x020B3460, 0x020B3480, 0x00, 0x00, "Subterranean Hell: Central Area Door"),

    "Sec03Rm16": DoorTransitionData(0x020ABCD4, 0x020ABCE4, 0x00, 0x00, "Garden of Madness: East Exit", True),
    "Sec04Rm03": DoorTransitionData(0x020ACFF4, 0x020ACFC0, 0x00, 0xC0, "Dark Chapel: West Door"),

    "Sec03Rm10": DoorTransitionData(0x020ABBCC, 0x020ABBDC, 0x00, 0x00, "Garden of Madness: Gate Door", True),
    "Sec08Rm02": DoorTransitionData(0x020B6710, 0x020B6720, 0x00, 0xC0, "Cursed Clock Tower: Lower Exit"),

    "Sec04Rm15": DoorTransitionData(0x020B0D58, 0x020B0D68, 0x00, 0x00, "Dark Chapel: East Door", True),
    "Sec05Rm01": DoorTransitionData(0x020AF10C, 0x020AF12C, 0x00, 0x00, "Condemned Tower: Lower Door"),

    "Sec04Rm08": DoorTransitionData(0x020B4104, 0x020B4114, 0x00, 0x00, "Dark Chapel: Catacombs Door", True),
    "Sec06Rm13": DoorTransitionData(0x020B3978, 0x020B3954, 0x00, 0x00, "Subterranean Hell: Boss Area"),

    "Sec06Rm06": DoorTransitionData(0x020B3FFC, 0x020B400C, 0x00, 0x00, "Subterranean Hell: Lower Right Exit", True),
    "Sec07Rm00": DoorTransitionData(0x020B4E74, 0x020B4E94, 0x00, 0x00, "Silenced Ruins: Antechamber Door"),

    "Sec07Rm08": DoorTransitionData(0x020B4080, 0x020B4090, 0x00, 0x00, "Silenced Ruins: Back Exit", True),
    "Sec06Rm11": DoorTransitionData(0x020B376C, 0x020B377C, 0x00, 0x00, "Subterranean Hell: Gate Door"),

    "Sec08Rm1E": DoorTransitionData(0x020B0CD4, 0x020B0CE4, 0x00, 0x00, "Cursed Clock Tower: East Exit", True),
    "Sec05Rm00": DoorTransitionData(0x020AF018, 0x020AF038, 0x00, 0x00, "Condemned Tower: Upper Door"),

    "Sec09Rm1A": DoorTransitionData(0x020BAB98, 0x020BABA8, 0x00, 0x00, "The Pinnacle: East Exit", True),
    "Sec08Rm06": DoorTransitionData(0x020B6B18, 0x020B6B38, 0x00, 0x00, "Cursed Clock Tower: Spike Hall Door"),
}


class DoorOrientation(IntEnum):
    # Directions
    Left = 1
    Right = 2


entrance_map: dict[int, list[int]] = {
  DoorOrientation.Left: [DoorOrientation.Right],  # Left-facing Doors
  DoorOrientation.Right: [DoorOrientation.Left]   # Right-facing doors
}


def shuffle_doors(world):
    for connection_room in castle_entrances:
        entrance = world.get_entrance(connection_room)
        entrance.randomization_type = EntranceType.TWO_WAY
        if door_data[connection_room].is_left_facing:
            entrance.randomization_group = DoorOrientation.Left
            disconnect_entrance_for_randomization(entrance, DoorOrientation.Left)
        else:
            entrance.randomization_group = DoorOrientation.Right
            disconnect_entrance_for_randomization(entrance, DoorOrientation.Right)
    world.connected_doors = randomize_entrances(world, True, entrance_map).pairings


def patch_castle_connections(world, rom):
    for door in world.connected_doors:
        source = door[0]
        destination = door[1]
        address = door_data[source].source_pointer
        des_pointer = door_data[destination].room_pointer

        rom.write_to_file(address, "arm9", struct.pack("I", des_pointer))
        rom.write_to_file(address + 0x0A, "arm9", struct.pack("H", door_data[destination].x_pos))
        rom.write_to_file(address + 0x0C, "arm9", struct.pack("H", door_data[destination].y_pos))


exit_regions = {
    "Sec00Rm07": "Lost Village Upper Doorway",
    "Sec00Rm15": "Lost Village Upper",
    "Sec00Rm16": "Lost Village Courtyard",
    "Sec00Rm0DObj03": "Lost Village Underground Middle",
    "Sec00Rm0DObj04": "Lost Village Underground Bottom",

    "Sec01Rm04": "Demon Guest House Number Puzzle West",
    "Sec01Rm2A": "Demon Guest House Lower",
    "Sec01Rm30": "Demon Guest House Lower",
    "Sec01Rm3F": "Demon Guest House Main",
    "Sec01Rm33": "Demon Guest House Upper",

    "Sec02Rm07": "Wizardry Lab Main",
    "Sec02Rm10": "Wizardry Lab East Gate",
    "Sec02Rm15": "Wizardry Lab Main",
    "Sec02Rm00": "Wizardry Lab West Gate",
    "Sec02Rm18": "Wizardry Lab Sunken West Door",
    "Sec02Rm1E": "Wizardry Lab Sunken East Door",

    "Sec03Rm00": "Garden of Madness Lower",
    "Sec03Rm09": "Garden of Madness Lower",
    "Sec03Rm13": "Garden of Madness Water Blocked",
    "Sec03Rm16": "Garden of Madness Lower",
    "Sec03Rm10": "Garden of Madness East Gate",
    "Sec03Rm05": "Garden of Madness Post-Boss",

    "Sec04Rm03": "Dark Chapel",
    "Sec04Rm15": "Dark Chapel Post-Button",
    "Sec04Rm08": "Dark Chapel Catacombs Exit",

    "Sec05Rm00": "Condemned Tower Post Wall",
    "Sec05Rm01": "Condemned Tower Bottom",

    "Sec06Rm00": "Subterranean Hell Spike Room West",
    "Sec06Rm01": "Subterranean Hell Shaft Top",
    "Sec06Rm06": "Subterranean Hell Shaft Bottom",
    "Sec06Rm0E": "Subterranean Hell Central Exit",
    "Sec06Rm11": "Subterranean Hell Button Gate Room",
    "Sec06Rm13": "Subterranean Hell Top Entrance",

    "Sec07Rm00": "Silenced Ruins Antechamber",
    "Sec07Rm08": "Silenced Ruins Back Exit",

    "Sec08Rm1E": "Cursed Clock Tower Entrance",
    "Sec08Rm02": "Cursed Clock Tower Entrance",
    "Sec08Rm06": "Cursed Clock Tower Exit",

    "Sec09Rm1A": "The Pinnacle Lower",
    "Sec09Rm07": "The Pinnacle Left Exit"
}


def set_ut_regions(world):
    for door in world.connected_doors:
        world.get_entrance(door[0]).connected_region = world.get_region(exit_regions[door[1]])
