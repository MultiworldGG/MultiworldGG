import itertools
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
    nodes: int # The number of nodes this seal has
    line_count: int # How many connections this seal has
    address: int # The address of the seal
    rotation_address: int  # address of the rotation value

def set_seals(world):
    #0222f294 + 4 * index

    placed_seals = []

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
            world.magic_seal_table[seal] = world.random.choice(seals) # Randomize the list

        if world.options.early_seal_1:
            world.magic_seal_table["Lost Village"] = "Magic Seal 1"  # We still want to set this early so the player doesn't get stuck

    for seal in world.magic_seal_table:
        if seal in ["Mine of Judgment", "The Abyss"] and world.mine_status == "Disabled":
            continue
        else:
            if world.magic_seal_table[seal] not in placed_seals:
                world.multiworld.itempool.append(world.set_classifications(world.magic_seal_table[seal]))  # Create the seal items if necessary
                world.extra_item_count += 1
                placed_seals.append(world.magic_seal_table[seal])

def write_seals(world, rom):
    for index, seal in enumerate(seal_list):
        rom.write_bytes(0x15C0B4 + (index * 4), bytearray([seals.index(world.magic_seal_table[seal])]))


def randomize_seal_patterns(world, rom):
    seal_data = {
        "Magic Seal 1": SealData(3, 3, 0x15BFD0, 0x15C034),
        "Magic Seal 2": SealData(4, 4, 0x15BFD4, 0x15C054),
        "Magic Seal 3": SealData(4, 6, 0x15BFDC, 0x15C014),
        "Magic Seal 4": SealData(6, 8, 0x15BFE4, 0x15C074),
        "Magic Seal 5": SealData(6, 11, 0x15BFF0, 0x15C094),
    }


    for index, seal in enumerate(seals):
        rotation = world.random.randint(0, 0xFFFF)
        valid_lines = {}
        data = seal_data[seal]
        built_seal = False
        while not built_seal:
            seal_array = []
            valid_edges = {a: [] for a in range(data.nodes)}
            for a, edge_list in valid_edges.items():
                for b in range(data.nodes):
                    if a == b: continue
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
        rom.write_bytes(data.address, bytearray(seal_array))
        rom.write_bytes(data.rotation_address, struct.pack("H", rotation))