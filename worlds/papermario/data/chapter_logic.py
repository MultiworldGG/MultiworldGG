from .LocationsList import location_table, location_groups
from ..options import ShuffleLetters, BowserCastleMode

# prefixes should be 3 characters long;
# used to exclude locations belong to given chapter
areas_by_chapter = {
    0: ["GR ", "TT ", "TTT", "SSS", "PCG"],
    1: ["KR ", "KBF"],
    2: ["MR ", "DDD", "DDO", "DDR"],
    3: ["FOR", "BM ", "GG ", "TC "],
    4: ["SGT"],
    5: ["JJ ", "MLL"],
    6: ["FLO"],
    7: ["SR ", "CP "],
    8: ["BC ", "PC "]
}

# chapters mapped to items that grant progression exclusively in those chapters
prog_items_by_chapter = {
    0: [],  # chapter 0 doesn't get excluded
    1: [
        "Koopa Fortress Key",
        "Koopa Fortress Key",
        "Koopa Fortress Key",
        "Koopa Fortress Key",
        "Kooper Shell",
        "Letter to Koover 1",
        "Letter to Koover 2",
        "Letter to Mort T",
        "Letter to Kolorado",
        "Artifact",
    ],
    2: [
        "Pulse Stone",
        "Ruins Key",
        "Ruins Key",
        "Ruins Key",
        "Ruins Key",
        "Pyramid Stone",
        "Lunar Stone",
        "Diamond Stone",
        "Lyrics",
        "Letter to Nomadimouse",
        "Letter to Mr E",
        "Letter to Little Mouser",
    ],
    3: [
        "Forest Pass",
        "Boo Portrait",
        "Boo Weight",
        "Boo Record",
        "Letter to Igor",
        "Letter to Franky",
        "Tubba Castle Key",
        "Tubba Castle Key",
        "Tubba Castle Key",
    ],
    4: [
        "Mystery Note",
        "Toy Train",
    ],
    5: [
        "Jade Raven",
        "Letter to Red Yoshi Kid",
        "Volcano Vase",
    ],
    6: [
        "Crystal Berry",
        "Water Stone",
        "Miracle Water",
        "Magical Bean",
        "Fertile Soil",
    ],
    7: [
        "Red Key",
        "Blue Key",
        "Crystal Palace Key",
        "Star Stone",
        "Letter to Mayor Penguin",
        "Letter to Frost T",
        "Snowman Scarf",
        "Snowman Bucket",
        "Warehouse Key",
    ],
    8: [
        "Bowser Castle Key",
        "Bowser Castle Key",
        "Bowser Castle Key",
        "Bowser Castle Key",
        "Bowser Castle Key",
        "Prison Key",
        "Prison Key",
    ]
}


# chapter excluded locations will be given PM filler items and their key items
# will be left in their vanilla locations
def get_chapter_excluded_location_names(
    excluded_chapters,
    letter_rewards_option,
) -> list:
    # Start with any locations that require more than the set number of spirits
    ch_excluded_locations = []

    # Basically, remove any checks that require several chapter regions
    # Koopa Koot item locations; setting will always be vanilla, so we don't
    # want to use any of his locations
    ch_excluded_locations.extend(location_groups["FavorReward"])
    ch_excluded_locations.extend(location_groups["FavorItem"])

    # Letter chain locations; setting will never have the final chain reward
    # randomized unless on full shuffle
    if letter_rewards_option <= ShuffleLetters.option_Full_Shuffle:
        ch_excluded_locations.extend(location_groups["LetterChain"])
        ch_excluded_locations.append("GR Goomba Village Goompapa Letter Reward 2")

    # Kolorado letter/artifact turn ins logically require chapter 2 access, even
    # though the checks are in Koopa Village
    # Even if chapter 1 is included, remove the checks unless chapter 2 is in
    if 1 not in excluded_chapters and 2 in excluded_chapters:
        ch_excluded_locations.append("KR Koopa Village 2 Kolorado Artifact Reward")
        ch_excluded_locations.append("KR Koopa Village 2 Kolorado Letter Reward")

    # Radio trade events need removed if chapter 1 is removed
    if 1 in excluded_chapters:
        ch_excluded_locations.extend(location_groups["RadioTradeEvent"])

    # if chapter 1 is in, allow the first trade event to stay in even if
    # trades 2 and 3 can't happen
    elif 2 in excluded_chapters:
        ch_excluded_locations.append("DDD N3W1 Ruins Entrance Radio Trade Event 2 Reward")
        ch_excluded_locations.append("TT Port District Radio Trade Event 3 Reward")

    for chapter in excluded_chapters:
        for prefix in areas_by_chapter[chapter]:
            ch_excluded_locations.extend([
                name
                for (name, data) in location_table.items()
                if name.startswith(prefix) and name not in ch_excluded_locations
            ])

    locs_beyond_spirits_requirements = get_locations_beyond_spirit_requirements(
        7 - len(excluded_chapters)
    )
    for loc in locs_beyond_spirits_requirements:
        if loc not in ch_excluded_locations:
            ch_excluded_locations.append(loc)

    return ch_excluded_locations


def get_chapter_excluded_item_names(chapters) -> list:
    ch_excluded_items = []
    for chapter in chapters:
        ch_excluded_items.extend(prog_items_by_chapter[chapter])

    return ch_excluded_items


def get_bowser_castle_removed_locations(bowser_castle_mode) -> list:
    removed_locations = []
    if bowser_castle_mode >= BowserCastleMode.option_Shortened:
        removed_locations.extend([
            "BC Dark Cave 1 Yellow Block",
            "BC Dark Cave 2 Yellow Block",
            "BC Outside Lower Jail Yellow Block",
            "BC Lava Channel 3 On Island 1",
            "BC Lava Channel 3 On Island 2",
            "BC Lava Key Room In Chest",
            "BC Lower Jail In Crate 1",
            "BC Lower Jail In Crate 2",
            "BC Front Door Exterior Red Block",
            "BC Castle Key Room On The Ground",
            "BC Hidden Key Room On The Ground",
            "BC Left Water Puzzle Top Left Ledge",
            "BC Right Water Puzzle Hidden Block",
        ])

    if bowser_castle_mode == BowserCastleMode.option_Boss_Rush:
        removed_locations.extend([
            "BC Outside Lower Jail Defeat Koopatrol Reward",
            "BC Battlement Yellow Block Left",
            "BC Battlement Yellow Block Center",
            "BC Battlement Yellow Block Right",
            "BC Battlement On Ledge",
            "BC East Upper Jail Defeat Koopatrol Reward",
            "BC West Upper Jail Defeat Koopatrol Reward",
            "BC Item Shop Shop Item 1",
            "BC Item Shop Shop Item 2",
            "BC Item Shop Shop Item 3",
            "BC Item Shop Shop Item 4",
            "BC Item Shop Shop Item 5",
            "BC Item Shop Shop Item 6",
            "BC Ultra Shroom Room On The Ground",
            "BC Room with Hidden Door 1 Yellow Block",
            "BC Room with Hidden Door 1 Hidden Block",
        ])

    return removed_locations


def get_locations_beyond_spirit_requirements(spirits: int) -> list:
    location_names = []
    if spirits < 6:
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 20")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 19")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 18")
    if spirits < 5:
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 17")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 16")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 15")
        location_names.append("TT Gate District Dojo: Master 3")
        location_names.append("TT Port District Radio Trade Event 3 Reward")
    if spirits < 4:
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 14")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 13")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 12")
        location_names.append("TT Plaza District Rowf's Shop Set 5 - 3")
        location_names.append("TT Plaza District Rowf's Shop Set 5 - 2")
        location_names.append("TT Plaza District Rowf's Shop Set 5 - 1")
        location_names.append("TT Gate District Dojo: Master 2")
    if spirits < 3:
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 11")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 10")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 9")
        location_names.append("TT Plaza District Rowf's Shop Set 4 - 3")
        location_names.append("TT Plaza District Rowf's Shop Set 4 - 2")
        location_names.append("TT Plaza District Rowf's Shop Set 4 - 1")
        location_names.append("TT Gate District Dojo: Master 1")
        location_names.append("DDD N3W1 Ruins Entrance Radio Trade Event 2 Reward")
    if spirits < 2:
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 8")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 7")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 6")
        location_names.append("TT Plaza District Rowf's Shop Set 3 - 3")
        location_names.append("TT Plaza District Rowf's Shop Set 3 - 2")
        location_names.append("TT Plaza District Rowf's Shop Set 3 - 1")
    if spirits < 1:
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 5")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 4")
        location_names.append("KR Koopa Village 2 Koopa Koot Reward 3")
        location_names.append("TT Plaza District Rowf's Shop Set 2 - 3")
        location_names.append("TT Plaza District Rowf's Shop Set 2 - 2")
        location_names.append("TT Plaza District Rowf's Shop Set 2 - 1")
        location_names.append("TT Gate District Dojo: Lee")
        location_names.append("TT Gate District Radio Trade Event 1 Reward")

    return location_names
