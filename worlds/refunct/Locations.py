import typing

from BaseClasses import Location


number_buttons_per_cluster = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 2,
    8: 1,
    9: 1,
    10: 2,
    11: 1,
    12: 1,
    13: 1,
    14: 1,
    15: 1,
    16: 1,
    17: 1,
    18: 2,
    19: 1,
    20: 1,
    21: 1,
    22: 1,
    23: 1,
    24: 1,
    25: 1,
    26: 3,
    27: 1,
    28: 2,
    29: 1,
    30: 1,
    31: 1,        
}

number_platforms_per_cluster = {
    1: 7,
    2: 7,
    3: 9,
    4: 9,
    5: 6,
    6: 5,
    7: 4,
    8: 11,
    9: 10,
    10: 9,
    11: 8,
    12: 5,
    13: 4,
    14: 3,
    15: 4,
    16: 3,
    17: 4,
    18: 11,
    19: 5,
    20: 10,
    21: 15,
    22: 2,
    23: 4,
    24: 9,
    25: 8,
    26: 14,
    27: 8,
    28: 20,
    29: 18,
    30: 14,
    31: 5,
}

platforms_with_button_on_them = {
    (1,1): (1,1),
    (2,3): (2,1),
    (3,2): (3,1),
    (4,4): (4,1),
    (5,1): (5,1),
    (6,1): (6,1),
    (7,1): (7,1),
    (7,2): (7,2),
    (8,11): (8,1),
    (9,6): (9,1),
    (10,1): (10,1),
    (10,3): (10,2),
    (11,8): (11,1),
    (12,1): (12,1),
    (13,1): (13,1),
    (14,3): (14,1),
    (15,2): (15,1),
    (16,1): (16,1),
    (17,2): (17,1),
    (18,2): (18,2),
    (18,1): (18,1),
    (19,5): (19,1),
    (20,7): (20,1),
    (21,8): (21,1),
    (22,2): (22,1),
    (23,3): (23,1),
    (24,1): (24,1),
    (25,5): (25,1),
    (26,12): (26,2),
    (26,7): (26,3),
    (26,9): (26,1),
    (27,8): (27,1),
    (28,18): (28,2),
    (28,8): (28,1),
    (29,4): (29,1),
    (30,12): (30,1),
    (31,2): (31,1),
}

starting_platform = (1,2)

cube_clusters = [           
    (4,1),
    (7,1),
    (8,1),
    (8,2),
    (9,1),
    (10,1),
    (12,1),
    (13,1),
    (14,1),
    (18,1),
    (21,1),
    (21,2),
    (23,1),
    (27,1),
    (28,1),
    (29,1),
    (29,2),
    (30,1),
]

extra_cube_clusters = [
    (5,1),
    (6,2),
    (7,2),
    (8,3),
    (13,2),
    (14,2),
    (14,3),
    (19,1), 
    (25,1),
    (26,1),
]

underwater_cube_clusters = [
    (55,1), 
    (55,2),
    (55,3),
    (55,4),
    (55,5),
    (55,6),
    (55,7),
    (55,8),
    (55,9),
    (55,10),
    (55,11), 
    (55,12),
    (55,13),
    (55,14),
    (55,15),
    (55,16),
    (55,17),
    (55,18),
]
   
    
    
    
class LocData(typing.NamedTuple):
    id: int
    main_nr: int
    sub_nr: int
    type_of_check: str = "Platform"
    minigame: str = ""
    
class RefunctLocation(Location):
    game: str = "Refunct"
    
block_brawl_scores = [1,3,6,10,15,18,21,24,27,30,36,42,48,54,60,72,84,96,108,120]
block_blub_scores = [3,15,21,30,42,60,84,120]

location_table = {
    **{f"Button {i}-{j}": LocData(10000000 + i * 100 + j, i, j, "Button", None)
       for i in range(1, 32) for j in range(1, number_buttons_per_cluster[i] + 1)},
    **{f"Platform {i}-{j}": LocData(10010000 + i * 100 + j, i, j, "Platform", None)
       for i in range(1, 32) for j in range(1, number_platforms_per_cluster[i] + 1)},
    **{f"Vanilla Minigame: Button {i}-{j}": LocData(10020000 + i * 100 + j, i, j, "Minigame", "Vanilla")
       for i in range(1, 32) for j in range(1, number_buttons_per_cluster[i] + 1)},
    **{f"Seeker Minigame: Platform {i}-{j}": LocData(10030000 + i * 100 + j, i, j, "Minigame", "Seeker")
       for i in range(1, 32) for j in range(1, number_platforms_per_cluster[i] + 1)},
    **{f"Button Galore Minigame: Button {i}-{j}": LocData(10040000 + i * 100 + j, i, j, "Minigame", "Button Galore")
       for i in range(1, 32) for j in range(1, number_buttons_per_cluster[i] + 1)},
    **{f"OG Randomizer Minigame: Button {i}-{j}": LocData(10050000 + i * 100 + j, i, j, "Minigame", "OG Randomizer")
       for i in range(1, 32) for j in range(1, number_buttons_per_cluster[i] + 1)},
    **{f"Cube {i}-{j}": LocData(10060000 + i * 100 + j, i, j, "Cube", None)
       for (i, j) in cube_clusters},
    **{f"Extra Cube {i}-{j}": LocData(10080000 + i * 100 + j, i, j, "Extra Cube", None)
       for (i, j) in extra_cube_clusters},
    **{f"Underwater Cube {i}-{j}": LocData(10080000 + i * 100 + j, i, j, "Underwater Cube", None)
       for (i, j) in underwater_cube_clusters},
    **{f"Block Brawl Minigame: Reds Score {j}": LocData(10070000 + 1 * 1000 + j, 1, j, "Minigame", "Block Brawl")
       for j in block_brawl_scores},
    **{f"Block Brawl Minigame: Blues Score {j}": LocData(10070000 + 2 * 1000 + j, 2, j, "Minigame", "Block Brawl")
       for j in block_brawl_scores},
    **{f"Block Brawl Minigame: Greens Score {j}": LocData(10070000 + 3 * 1000 + j, 3, j, "Minigame", "Block Brawl")
       for j in block_brawl_scores},
    **{f"Block Brawl Minigame: Yellows Score {j}": LocData(10070000 + 4 * 1000 + j, 4, j, "Minigame", "Block Brawl")
       for j in block_brawl_scores},
    
    **{f"Climb Line Minigame: {i}0m": LocData(10091000 + i, i, None, "Minigame", "Climb Line")
       for i in range(1, 11)},
    **{f"Climb Spiral Minigame: {i}0m": LocData(10092000 + i, i, None, "Minigame", "Climb Spiral")
       for i in range(1, 11)},
    **{f"Climb Chaos Minigame: {i}0m": LocData(10093000 + i, i, None, "Minigame", "Climb Chaos")
       for i in range(1, 11)},
    
    **{f"Block Blub Minigame: Reds Score {j}": LocData(10100000 + 1 * 1000 + j, 1, j, "Minigame", "Block Blub")
       for j in block_blub_scores},
    **{f"Block Blub Minigame: Blues Score {j}": LocData(10100000 + 2 * 1000 + j, 2, j, "Minigame", "Block Blub")
       for j in block_blub_scores},
    **{f"Block Blub Minigame: Greens Score {j}": LocData(10100000 + 3 * 1000 + j, 3, j, "Minigame", "Block Blub")
       for j in block_blub_scores},
    **{f"Block Blub Minigame: Yellows Score {j}": LocData(10100000 + 4 * 1000 + j, 4, j, "Minigame", "Block Blub")
       for j in block_blub_scores},
    
    **{f"Refunct Mountain Minigame: Button {i}-{j}": LocData(10110000 + i * 100 + j, i, j, "Minigame", "Refunct Mountain")
       for i in range(1, 32) for j in range(1, number_buttons_per_cluster[i] + 1)},
    
}
    
platforms_with_button_ids = []
platforms_without_button_ids = []
for cluster, num_platforms in number_platforms_per_cluster.items():
    for platform in range(1, num_platforms + 1):
        if (cluster, platform) not in platforms_with_button_on_them.keys():
            platforms_without_button_ids.append(10010000 + cluster * 100 + platform)
        else:
            platforms_with_button_ids.append(10010000 + cluster * 100 + platform)