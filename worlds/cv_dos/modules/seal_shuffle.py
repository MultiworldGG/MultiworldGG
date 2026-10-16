import struct
from dataclasses import dataclass
seal_list = [
    "Lost Village",
    "Wizardry Lab",
    "Dark Chapel",
    "Dark Chapel Inner",
    "Garden of Madness",
    "Demon Guest House",
    "Condemned Tower",
    "Subterranean Hell",
    "Cursed Clock Tower",
    "Silenced Ruins",
    "The Pinnacle",
    "Demon Guest House Upper",
    "Mine of Judgment",
    "Castle Center",
    "The Abyss"
]

seals = [
    "Magic Seal 1",
    "Magic Seal 2",
    "Magic Seal 3",
    "Magic Seal 4",
    "Magic Seal 5"
]


@dataclass
class SealData:
    nodes: int  # The number of nodes this seal has
    line_count: int  # How many connections this seal has
    address: int  # The address of the seal
    rotation_address: int  # address of the rotation value
    seal_pointer: int  # Address that contains a pointer to the current seal


def set_seals(world):
    # 0222f294 + 4 * index

    world.magic_seal_table = {
        "Lost Village": "Magic Seal 1",
        "Wizardry Lab": "Magic Seal 1",
        "Dark Chapel": "Magic Seal 2",
        "Dark Chapel Inner": "Magic Seal 2",
        "Garden of Madness": "Magic Seal 2",  # Dario
        "Demon Guest House": "Magic Seal 3",
        "Subterranean Hell": "Magic Seal 3",
        "Condemned Tower": "Magic Seal 3",
        "Cursed Clock Tower": "Magic Seal 4",
        "Silenced Ruins": "Magic Seal 4",
        "Demon Guest House Upper": "Magic Seal 4",
        "The Pinnacle": "Magic Seal 4",
        "Mine of Judgment": "Magic Seal 5",
        "Castle Center": "Magic Seal 5",
        "The Abyss": "Magic Seal 5"
    }

    if world.options.seal_shuffle:
        for seal in world.magic_seal_table:
            world.magic_seal_table[seal] = world.random.choice(seals)  # Randomize the list

        if world.options.early_seal_1:
            # We still want to set this early so the player doesn't get stuck
            world.magic_seal_table["Lost Village"] = "Magic Seal 1"


def write_seals(world, rom):
    for index, seal in enumerate(seal_list):
        rom.write_to_file(0x222F294 + (index * 4), "overlay_0", bytearray([seals.index(world.magic_seal_table[seal])]))


max_node_counts = {
    2: 2,
    3: 4,
    4: 6,
    5: 10,
    6: 12,
    7: 14,
    8: 16,
    9: 18,
    10: 20
}

min_node_counts = {
    3: 3,
    4: 3,
    5: 4,
    6: 4,
    7: 5,
    8: 5,
    9: 5,
}


def randomize_seal_patterns(world, rom):
    from ..Options import RandomizeSealDetails
    seal_data = {
        "Magic Seal 1": SealData(3, 3, 0x222f1b0, 0x222f214, 0x0222F21C),
        "Magic Seal 2": SealData(4, 4, 0x222f1b4, 0x222f234, 0x0222F23C),
        "Magic Seal 3": SealData(4, 6, 0x222f1bc, 0x222f1f4, 0x0222F1FC),
        "Magic Seal 4": SealData(6, 8, 0x222f1c4, 0x222f254, 0x0222F25C),
        "Magic Seal 5": SealData(6, 11, 0x222f1d0, 0x222f274, 0x0222F27C),
    }

    for index, seal in enumerate(seals):
        rotation = world.random.randint(0, 0xFFFF)
        data = seal_data[seal]

        if world.options.randomize_seal_details:
            file = "overlay_41"  # We need to repoint the seals to a new file
            data.address = (0x02308DD0 + (0x16 * index))
            if world.options.randomize_seal_details == RandomizeSealDetails.option_simple:
                data.nodes = world.random.randint(max(2, data.nodes - 2), data.nodes + 2)
                new_line_count = world.random.randint(data.line_count - 3, data.line_count + 3)
                new_line_count = max(2, new_line_count)
                new_line_count = min(max_node_counts[data.nodes], new_line_count)
                data.line_count = new_line_count
            elif world.options.randomize_seal_details == RandomizeSealDetails.option_chaos:
                data.nodes = world.random.randint(2, 10)
                data.line_count = world.random.randint(2, max_node_counts[data.nodes])
            elif world.options.randomize_seal_details == RandomizeSealDetails.option_chaos_weighted:
                data.line_count = world.random.randint(2, 20)
                if data.line_count == 2:
                    data.nodes = 2
                elif data.line_count == 20:
                    data.nodes = 10
                else:
                    if data.line_count >= 10:
                        node_target = data.line_count // 2
                    else:
                        node_target = min_node_counts[data.line_count]

                    data.nodes = max(2, min(10, world.random.randint(node_target, node_target + 1)))

        else:
            file = "overlay_0"
        timer = 0xB4 + (15 * (max(0, data.line_count - 11)))
        rom.write_to_file(data.rotation_address + 0x18, "overlay_0", struct.pack("H", timer))
        # rom.write_to_file(data.rotation_address + 0x04, "overlay_0", struct.pack("H", draw_speed))

        built_seal = False
        seal_array = []
        while not built_seal:
            seal_array = []
            valid_edges = {a: [] for a in range(data.nodes)}
            for a, edge_list in valid_edges.items():
                for b in range(data.nodes):
                    if a == b:
                        continue
                    edge_list.append(b)

            cur = world.random.randrange(data.nodes)
            seal_array.append(cur)
            for _ in range(data.line_count - 1):
                if not valid_edges[cur]:
                    built_seal = False
                    break
                next_node = world.random.choice(valid_edges[cur])
                valid_edges[cur].remove(next_node)
                valid_edges[next_node].remove(cur)
                cur = next_node
                seal_array.append(cur)
            else:
                built_seal = True
        seal_array.append(0xFF)  # Add the ending terminator
        rom.write_to_file(data.address, file, bytearray(seal_array))
        rom.write_to_file(data.rotation_address, "overlay_0", struct.pack("H", rotation))
        rom.write_to_file(data.seal_pointer, "overlay_0", struct.pack("I", data.address))
        rom.write_to_file(data.rotation_address - 4, "overlay_0", bytearray([data.nodes]))
