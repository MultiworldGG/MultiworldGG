# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/random_puzzles_minigames.py
"""
This module is used for modifying the puzzles and minigames in various areas of
the game.
"""
from ..data.puzzle_data import puzzle_data
from ..data.ItemList import item_table
from ..options import SpiritRequirements


# TODO set up fill to handle DRO Shop puzzles
def get_puzzles_minigames(random_puzzles: bool, world) -> (list, list):
    """
    Returns a list of randomly rolled data (solutions, initial setups and
    iterations) for puzzles and minigames.
    """
    puzzle_minigame_list = []

    deepjungle_blocked_positions = []
    shopcode_redjar = {}

    spoilerlog_additions = {}

    random = world.random

    for name, data in puzzle_data.items():
        # Fuzzy Tree Minigame Round 1 hops
        if name == "FuzzyTreesRound1":
            num_hops = world.random.randint(10, 13)
            puzzle_minigame_list.append((get_puzzle_key(data[0]), num_hops))

        # Fuzzy Tree Minigame Round 2 hops
        elif name == "FuzzyTreesRound2":
            num_hops = world.random.randint(9, 12)
            puzzle_minigame_list.append((get_puzzle_key(data[0]), num_hops))

        # Fuzzy Tree Minigame Round 3 hops
        elif name == "FuzzyTreesRound3":
            num_hops = world.random.randint(8, 11)
            puzzle_minigame_list.append((get_puzzle_key(data[0]), num_hops))

        # Super Boots Chest Boo Ring
        elif name == "BooRingOBK04":
            num_throws = world.random.randint(6, 10)
            puzzle_minigame_list.append((get_puzzle_key(data[0]), num_throws))

        # Record Boo Ring: Degrees of rotation until item drop
        elif name == "BooRingOBK08Degrees":
            degrees = world.random.randint(180, 540)
            puzzle_minigame_list.append((get_puzzle_key(data[0]), degrees))

        # Record Boo Ring: Delay until main Boo stops
        elif name == "BooRingOBK08Delay":
            delay = world.random.randint(360, 380)
            puzzle_minigame_list.append((get_puzzle_key(data[0]), delay))

        # Toad Town Tunnels Push Block: Initial position
        elif name == "TunnelsPushBlock":
            if not random_puzzles:
                position_encoded = data[1]
            else:
                position_encoded = _random_pushblock_positions(
                    num_blocks=1,
                    min_x=0,
                    max_x=6,
                    min_z=0,
                    max_z=5,
                    disallowed_positions=[],
                    random=random
                )
            puzzle_minigame_list.append((get_puzzle_key(data[0]), position_encoded))

        # Pleasant Path: Attack FX B block code
        elif name == "AttackFXBBlocks":
            if not random_puzzles:
                block_order = data[1]
                spoilerlog_additions["AttackFXBBlocks"] = "Left, Right, Middle"
            else:
                def _map_blocks(block_id: int) -> str:
                    if block_id == 1:
                        return "Left"
                    elif block_id == 2:
                        return "Right"
                    else:
                        return "Middle"
                blocks = [1, 2, 3]
                world.random.shuffle(blocks)
                block_order = (
                    (blocks[0] << 8) +
                    (blocks[1] << 4) +
                    blocks[2]
                )
                spoilerlog_additions["AttackFXBBlocks"] = (
                    f"{_map_blocks(blocks[0])}, {_map_blocks(blocks[1])}, {_map_blocks(blocks[2])}"
                )
            puzzle_minigame_list.append((get_puzzle_key(data[0]), block_order))

        # Koopa Village Push Block: Initial position
        elif name == "KoopaVillagePushBlocks":
            if not random_puzzles:
                positions_encoded = data[1]
            else:
                positions_encoded = _random_pushblock_positions(
                    num_blocks=1,
                    min_x=0,
                    max_x=4,
                    min_z=0,
                    max_z=4,
                    disallowed_positions=[],
                    random=random
                )
            puzzle_minigame_list.append((get_puzzle_key(data[0]), positions_encoded))

        # Dry Dry Outpost: Shop code for Pulse Stone
        elif name == "ShopCodePulseStone":
            if not random_puzzles:
                pulsestone_buy_order = data[1]
                spoilerlog_additions["ShopCodePulseStone"] = (
                    "Dried Shroom, Dusty Hammer"
                )
            else:
                dro_shop_nonuniques = set([
                    item for item in get_dro_shop_items(world)
                    if ((item_table[item][0] == "ITEM"
                        and item_table[item][3] <= 10 and item_table[item][2] <= 0xFF)
                            or item_table[item][0] == "COIN")
                ])
                dro_shop_nonuniques = sorted(list(dict.fromkeys(dro_shop_nonuniques)))
                world.random.shuffle(dro_shop_nonuniques)
                code_item_1 = dro_shop_nonuniques.pop()
                code_item_2 = dro_shop_nonuniques.pop()
                pulsestone_item_order_str = f"{code_item_1}{code_item_2}"
                pulsestone_buy_order = (
                    (item_table[code_item_1][2] << 16)
                    + item_table[code_item_2][2]
                )
                spoilerlog_additions["ShopCodePulseStone"] = (
                    f"{code_item_1}, {code_item_2}"
                )
            puzzle_minigame_list.append((
                get_puzzle_key(data[0]),
                pulsestone_buy_order
            ))

        # Dry Dry Outpost: Shop code for Red Jar
        elif name in ["ShopCodeRedJar1", "ShopCodeRedJar2"]:
            if not random_puzzles:
                buy_order = data[1]
                spoilerlog_additions["ShopCodeRedJar"] = (
                    "Dusty Hammer, Dried Pasta, Dusty Hammer, Dried Shroom"
                )
            else:
                if not shopcode_redjar:
                    # Setup the Red Jar item code before assigning to the
                    # two puzzle dbkeys
                    shopcode_redjar = {1: "", 2: "", 3: "", 4: ""}
                    dro_shop_nonuniques = set([
                        item for item in get_dro_shop_items(world)
                        if ((item_table[item][0] == "ITEM"
                             and item_table[item][3] <= 10 and item_table[item][2] <= 0xFF)
                            or item_table[item][0] == "COIN")
                    ])
                    dro_shop_nonuniques = sorted(list(dict.fromkeys(dro_shop_nonuniques)))
                    if len(dro_shop_nonuniques) < 4:
                        dro_shop_nonuniques.append(world.random.choice(dro_shop_nonuniques))
                    while True:
                        world.random.shuffle(dro_shop_nonuniques)
                        code_item_1 = dro_shop_nonuniques.pop()
                        code_item_2 = dro_shop_nonuniques.pop()
                        code_item_3 = dro_shop_nonuniques.pop()
                        code_item_4 = dro_shop_nonuniques.pop()

                        item_order_str = f"{code_item_1}{code_item_2}{code_item_3}{code_item_4}"

                        # repeat generating a red jar code until the pulse stone
                        # code is no longer found inside of the red jar code
                        if pulsestone_item_order_str not in item_order_str:
                            shopcode_redjar[1] = code_item_1
                            shopcode_redjar[2] = code_item_2
                            shopcode_redjar[3] = code_item_3
                            shopcode_redjar[4] = code_item_4
                            break
                        else:
                            dro_shop_nonuniques.append(code_item_1)
                            dro_shop_nonuniques.append(code_item_2)
                            dro_shop_nonuniques.append(code_item_3)
                            dro_shop_nonuniques.append(code_item_4)
                if name == "ShopCodeRedJar1":
                    buy_order = (
                        (item_table[shopcode_redjar[1]][2] << 16)
                        + item_table[shopcode_redjar[2]][2]
                    )
                else:
                    buy_order = (
                        (item_table[shopcode_redjar[3]][2] << 16)
                        + item_table[shopcode_redjar[4]][2]
                    )
                spoilerlog_additions["ShopCodeRedJar"] = (
                    f"{shopcode_redjar[1]}, {shopcode_redjar[2]}, "
                    f"{shopcode_redjar[3]}, {shopcode_redjar[4]}"
                )
            puzzle_minigame_list.append((
                get_puzzle_key(data[0]),
                buy_order
            ))

        # Dry Dry Ruins: Ruins stones positions
        elif name == "RuinsStones":
            if not random_puzzles:
                slot_order = data[1]
                spoilerlog_additions["RuinsStones"] = (
                    "Pyramid Stone, Empty, Diamond Stone, Empty, Lunar Stone"
                )
            else:
                def _map_stones(stone_id: int) -> str:
                    if stone_id == 1:
                        return "Pyramid Stone"
                    elif stone_id == 2:
                        return "Diamond Stone"
                    elif stone_id == 3:
                        return "Lunar Stone"
                    else:
                        return "Empty"
                slots = [0,0,1, 2, 3]
                random.shuffle(slots)
                slot_order = (
                    (slots[0] << 16)
                  + (slots[1] << 12)
                  + (slots[2] << 8)
                  + (slots[3] << 4)
                  + slots[4]
                )
                spoilerlog_additions["RuinsStones"] = (
                    f"{_map_stones(slots[0])}, {_map_stones(slots[1])}, "
                    f"{_map_stones(slots[2])}, {_map_stones(slots[3])}, "
                    f"{_map_stones(slots[4])}"
                )
            puzzle_minigame_list.append((
                get_puzzle_key(data[0]),
                slot_order
            ))

        # Shy Guy's Toybox: Green Station boxes order
        elif name == "GreenStationBoxes":
            if not random_puzzles:
                boxes_order = data[1]
                spoilerlog_additions["GreenStationBoxes"] = (
                    "Yellow (2), Green (1), Red (3), Blue (4)"
                )
            else:
                # if puzzles random: mod breaks if not exactly 6 values
                def _map_boxes(box_id: int) -> str:
                    if box_id == 1:
                        return "Green (1)"
                    elif box_id == 2:
                        return "Yellow (2)"
                    elif box_id == 3:
                        return "Red (3)"
                    else:
                        return "Blue (4)"
                box_1 = random.randint(1, 4)
                box_2 = random.randint(1, 4)
                box_3 = random.randint(1, 4)
                box_4 = random.randint(1, 4)
                box_5 = random.randint(1, 4)
                box_6 = random.randint(1, 4)
                boxes_order = (
                    (box_1 << 20)
                  + (box_2 << 16)
                  + (box_3 << 12)
                  + (box_4 << 8)
                  + (box_5 << 4)
                  + box_6
                )
                spoilerlog_additions["GreenStationBoxes"] = (
                    f"{_map_boxes(box_1)}, {_map_boxes(box_2)}, {_map_boxes(box_3)}, "
                    f"{_map_boxes(box_4)}, {_map_boxes(box_5)}, {_map_boxes(box_6)}"
                )
            puzzle_minigame_list.append((get_puzzle_key(data[0]), boxes_order))

        # Deep Jungle Push Blocks: Initial positions
        elif name in [
            "DeepJunglePushBlocks1","DeepJunglePushBlocks2",
            "DeepJunglePushBlocks3","DeepJunglePushBlocks4"
        ]:
            if not random_puzzles:
                positions_encoded = data[1]
            else:
                positions_encoded, deepjungle_blocked_positions = _deepjungle_pushblock_positions(
                    name,
                    deepjungle_blocked_positions,
                    random
                )
            puzzle_minigame_list.append((get_puzzle_key(data[0]), positions_encoded))

        # Ultra Hammer room Push Blocks: Initial positions
        elif name == "UltraHammerPushBlocks":
            if not random_puzzles:
                positions_encoded = data[1]
            else:
                positions_encoded = _random_pushblock_positions(
                    num_blocks=2,
                    min_x=5,
                    max_x=14,
                    min_z=0,
                    max_z=4,
                    disallowed_positions=[(14, 1)],
                    random=random
                )
            puzzle_minigame_list.append((get_puzzle_key(data[0]), positions_encoded))

        # Lava Dam Push Blocks: Initial positions
        elif name == "LavaDamPushBlocks":
            if not random_puzzles:
                positions_encoded = data[1]
            else:
                positions_encoded = _lavadam_pushblock_positions(random)
            puzzle_minigame_list.append((get_puzzle_key(data[0]), positions_encoded))

        # Flower Fields Three Tree: Correct hit sequence
        elif name == "FlowerFieldsThreeTrees":
            if not random_puzzles:
                sequence_encoded = data[1]
                spoilerlog_additions["FlowerFieldsThreeTrees"] = "Middle, Right, Left"
            else:
                def _map_tree(tree_id: int) -> str:
                    if tree_id == 1:
                        return "Left"
                    elif tree_id == 2:
                        return "Middle"
                    else:
                        return "Right"
                trees = [1, 2, 3]
                random.shuffle(trees)
                sequence_encoded = (
                    (trees[0] << 8)
                  + (trees[1] << 4)
                  + trees[2]
                )
                spoilerlog_additions["FlowerFieldsThreeTrees"] = (
                    f"{_map_tree(trees[0])}, {_map_tree(trees[1])}, {_map_tree(trees[2])}"
                )
            puzzle_minigame_list.append((get_puzzle_key(data[0]), sequence_encoded))

        # Flower Fields elevators: Initial positions
        elif name == "FlowerFieldsElevators":
            if not random_puzzles:
                positions_encoded = data[1]
            else:
                positions_encoded = (
                    (random.randint(0, 1) << 8)
                  + (random.randint(0, 1) << 4)
                  + random.randint(0, 1)
                )
            puzzle_minigame_list.append((get_puzzle_key(data[0]), positions_encoded))

        # Kooper Duplighost (Shiver Mountain): Actor positions
        elif name == "SAMKooperDuplighost":
            if not random_puzzles:
                actors_swapped = data[1]
            else:
                actors_swapped = random.randint(0, 1)
            puzzle_minigame_list.append((get_puzzle_key(data[0]), actors_swapped))

        # Kooper Duplighosts (Crystal Palace): Actor positions
        elif name == "PRAKooperDuplighosts":
            if not random_puzzles:
                positions_encoded = data[1]
            else:
                npc_ids = [0, 1, 2, 3, 4]
                random.shuffle(npc_ids)
                positions_encoded = (
                    (npc_ids[0] << 16)
                  + (npc_ids[1] << 12)
                  + (npc_ids[2] << 8)
                  + (npc_ids[3] << 4)
                  + npc_ids[4]
                )
            puzzle_minigame_list.append((get_puzzle_key(data[0]), positions_encoded))

        # Bombette Duplighosts: Actor positions
        elif name == "BombetteDuplighosts":
            if not random_puzzles:
                positions_encoded = data[1]
            else:
                npc_ids = [0, 1, 2, 3, 4]
                random.shuffle(npc_ids)
                positions_encoded = (
                    (npc_ids[0] << 16)
                  + (npc_ids[1] << 12)
                  + (npc_ids[2] << 8)
                  + (npc_ids[3] << 4)
                  + npc_ids[4]
                )
            puzzle_minigame_list.append((get_puzzle_key(data[0]), positions_encoded))

        # Albino Dino Statues: Initial positions
        elif name == "AlbinoDinoPositions":
            if not random_puzzles:
                positions_encoded = data[1]
            else:
                positions_encoded = _albino_dino_puzzle(random)
            puzzle_minigame_list.append((get_puzzle_key(data[0]), positions_encoded))

        # Bowser's Castle Up/Down Maze room: Solution
        elif name == "BowsersCastleMaze":
            #if not random_puzzles:
            #    solution_encoded = data[1]
            #else:
            #    solution_encoded = (
            #      + (random.randint(0,1) << 5)
            #      + (random.randint(0,1) << 4)
            #      + (random.randint(0,1) << 3)
            #      + (random.randint(0,1) << 2)
            #      + (random.randint(0,1) << 1)
            #      + 1 # static "up" as last step
            #    )
            # NOTE: randomizing this puzzle is turned off for now, as the map-
            # edit isn't done yet
            solution_encoded = data[1]
            puzzle_minigame_list.append((get_puzzle_key(data[0]), solution_encoded))


    return puzzle_minigame_list, spoilerlog_additions


def _albino_dino_puzzle(random) -> int:
    max_x_coord = 8
    max_z_coord = 2

    dino_1 = (random.randint(0, max_x_coord), random.randint(0, max_z_coord))

    # make sure the dinos don't share a space
    while True:
        dino_2 = (random.randint(0, max_x_coord), random.randint(0, max_z_coord))
        if dino_2[0] == dino_1[0] and dino_2[1] == dino_1[1]:
            continue
        else:
            break
    while True:
        dino_3 = (random.randint(0, max_x_coord), random.randint(0, max_z_coord))
        if dino_3[0] == dino_1[0] and dino_3[1] == dino_1[1]:
            continue
        elif dino_3[0] == dino_2[0] and dino_3[1] == dino_2[1]:
            continue
        else:
            break

    # Hex-Encoding: 0x00xzxzxz
    return (
        (dino_1[0] << 20)
      + (dino_1[1] << 16)
      + (dino_2[0] << 12)
      + (dino_2[1] << 8)
      + (dino_3[0] << 4)
      + dino_3[1]
    )


def _random_pushblock_positions(
    num_blocks: int,
    min_x: int,
    max_x: int,
    min_z: int,
    max_z: int,
    disallowed_positions: list,
    random
) -> int:
    if (
        not 1 <= num_blocks <= 4
     or min_x >= max_x
     or min_z >= max_z
     or min_x < 0
     or max_x > 15
     or min_z < 0
     or max_z > 15
    ):
        raise ValueError

    block_positions = []

    while len(block_positions) < num_blocks:
        new_block_pos = (random.randint(min_x, max_x), random.randint(min_z, max_z))

        if new_block_pos in disallowed_positions:
            continue
        if new_block_pos in block_positions:
            # don't place two at the same coordinates
            continue

        block_positions.append(new_block_pos)

    positions_encoded = 0

    for block in block_positions:
        positions_encoded = positions_encoded << 4
        positions_encoded += block[0]
        positions_encoded = positions_encoded << 4
        positions_encoded += block[1]

    return positions_encoded


def _deepjungle_pushblock_positions(
    puzzle_name: str,
    already_placed: list,
    random
) -> (int, int):

    # Pushblockgrid (x: obstructed, B: boulder, P: push block, %: geyser hole, o: unused hole )
    #              1111111111222222222233
    #    01234567890123456789012345678901
    #   +--------------------------------
    #  0|xxxxxxxxxxxxxxxBBBBBxxxxxxxxxxxx
    #  1|xxxxxxxxxxxxxxxBBBBBxxxxxxxxxxxx
    #  2|xxx       xxxx BBBBB P    xxxxxx
    #  3|xx        xxxx      o
    #  4|    %     o           P  %
    #  5|       P        P
    #  6|              %           P %
    #  7|                           P
    #  8|                     %
    #  9|         o   P
    # 10|
    # 11|
    # Default block default positions: 7/5, 13/9, 16/5, 21/2, 22/4, 26/6, 27/7
    all_block_positions = already_placed.copy()
    new_block_positions = []
    disallowed_positions = [
        # obstructed positions
        (0,2), (0,3), (1,2), (1,3), (2,2),
        (10,2), (10,3), (11,2), (11,3), (12,2), (12,3), (13,2), (13,3),
        (15,2), (16,2), (17,2), (18,2), (19,2),
        (26,2), (27,2), (28,2), (29,2), (30,2), (31,2),
        # geyser holes
        (4,4), (14,6), (21,8), (25,4), (28,6),
        # edge/corner locations where blocks cannot be moved out of
        (2,3), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2), (9,2)
    ]

    if puzzle_name == "DeepJunglePushBlocks4":
        blocks_per_puzzle_name = 1
    else:
        blocks_per_puzzle_name = 2

    while len(new_block_positions) < blocks_per_puzzle_name:
        # Do not place blocks on rows 0, 1, 11, or column 0, 31
        # because the first rows are obstructed, and the outer ring positions
        # don't allow moving the block back into the center
        new_block_pos = (random.randint(1, 30), random.randint(2, 10))

        if new_block_pos in disallowed_positions:
            continue
        if new_block_pos in all_block_positions:
            # don't place two at the same coordinates
            continue
        if (   (    (new_block_pos[0] + 1, new_block_pos[1]) in all_block_positions
                and (   (    (new_block_pos[0],     new_block_pos[1] + 1) in all_block_positions
                         and (new_block_pos[0] + 1, new_block_pos[1] + 1) in all_block_positions)
                     or (    (new_block_pos[0],     new_block_pos[1] - 1) in all_block_positions
                         and (new_block_pos[0] + 1, new_block_pos[1] - 1) in all_block_positions)
                    )
               )
            or (    (new_block_pos[0] - 1, new_block_pos[1]) in all_block_positions
                and (   (    (new_block_pos[0],     new_block_pos[1] + 1) in all_block_positions
                         and (new_block_pos[0] - 1, new_block_pos[1] + 1) in all_block_positions)
                     or (    (new_block_pos[0],     new_block_pos[1] - 1) in all_block_positions
                         and (new_block_pos[0] - 1, new_block_pos[1] - 1) in all_block_positions)
                    )
               )
        ):
            # don't allow four blocks in a square pattern, as then they
            # cannot be pushed
            continue

        new_block_positions.append(new_block_pos)
        all_block_positions.append(new_block_pos)

    positions_encoded = 0

    for block in new_block_positions:
        positions_encoded = positions_encoded << 8
        positions_encoded += block[0]
        positions_encoded = positions_encoded << 8
        positions_encoded += block[1]

    return positions_encoded, all_block_positions


def _lavadam_pushblock_positions(random) -> int:
    block_positions = []
    disallowed_positions = [(9, 0), (10, 0), (11, 0)]

    while len(block_positions) < 3:
        new_block_pos = (random.randint(0, 12), 0)

        if new_block_pos in disallowed_positions:
            continue
        if new_block_pos in block_positions:
            # don't place two at the same coordinates
            continue
        if (
            new_block_pos[0] + 1 in [x for (x, _) in block_positions]
         or new_block_pos[0] - 1 in [x for (x, _) in block_positions]
        ):
            # don't allow two blocks right next to each other, otherwise they
            # cannot be pushed
            continue

        block_positions.append(new_block_pos)

    positions_encoded = 0

    for block in block_positions:
        positions_encoded = positions_encoded << 4
        positions_encoded += block[0]
        positions_encoded = positions_encoded << 4
        positions_encoded += block[1]

    return positions_encoded


def get_dro_shop_items(world) -> list:
    if (    2 in world.excluded_spirits
        and world.options.spirit_requirements.value == SpiritRequirements.option_Specific_And_Limit_Chapter_Logic
    ):
        dro_shop_items = ["Dried Shroom", "Dusty Hammer", "Dried Pasta"]
    else:
        dro_shop_items = []
        for n in range(1, 7):
            shop_loc = world.multiworld.get_location(f"DDO Outpost 1 Shop Item {n}", world.player)
            if shop_loc.item.player == world.player:
                dro_shop_items.append(shop_loc.item.name)
            else:
                dro_shop_items.append("MultiWorldGeneric")

    return dro_shop_items


def get_puzzle_key(puzzle_index):
    return (0xA8 << 24) | puzzle_index
