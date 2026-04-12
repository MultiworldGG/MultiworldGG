import copy, re
from typing import Any, TYPE_CHECKING

from gcbrickwork.JMP import JMPEntry, JMP

from ...Locations import LMLocationData, ALL_LOCATION_TABLE

if TYPE_CHECKING:
    from ..LM_Randomize_ISO import LuigisMansionRandomizer

# Used to update speedy spirit observers that spawn them in and switch them to the blackout only table instead.
SPEEDY_OBSERVER_INDEX: list[int] = [183, 182, 179, 178, 177, 101, 100, 99, 98, 97, 21, 19]
SPEEDY_ENEMY_INDEX: list[int] = [128, 125, 115, 114, 113, 67, 66, 60, 59, 58, 7, 6]

# Used to "fuzzy-match" chest colors for items from other games.
MONEY_ITEM_NAMES: list[str] = ["Bills", "Coin", "Gold Bar", "Rupee", "Leaf", "Green", "Gold", "Jewel"]
EXPLODE_ITEM_NAMES: list[str] = ["Bomb", "Missile", "Glove", "Red", "Tunic", "Cloth", "Armor", "Boot", "Shoe"]
ICY_ITEM_NAMES: list[str] = ["Ice Trap", "White", "Ice Beam", "Icy", "Freeze"]
LIGHT_ITEM_NAMES: list[str] = ["Light", "Big Key", "Yellow", "Banana", "Boss Key", "Sun", "Laser"]
BLUEISH_ITEM_NAMES: list[str] = ["Small Key", "Blue", "Ocean", "Sea", "Magic"]

# This is a list of furniture that is at ceiling height. These need to be adjusted to avoid spawning items out of bounds.
CEILING_FURNITURE_LIST: list[int] = [4, 38, 43, 62, 63, 76, 77, 81, 84, 85, 91, 92, 101, 110, 111, 137, 156, 158, 159,
    163, 173, 174, 189, 190, 195, 199, 200, 228, 240, 266, 310, 342, 352, 354, 355, 356, 357, 358, 359, 373, 374, 378,
    379, 380, 381, 399, 423, 426, 445, 446, 454, 459, 460, 463, 467, 485, 547, 595, 596, 631, 632, 636, 657, 671, 672]

# Similar to Ceiling furniture, except only needs a slight adjustment to prevent items from going out of bounds.
MEDIUM_HEIGHT_FURNITURE_LIST: list[int] = [0, 1, 104, 112, 113, 114, 124, 125, 135, 136, 204, 206, 210, 232, 234, 235,
    264, 265, 270, 315, 343, 344, 345, 346, 347, 353, 361, 362, 363, 368, 369, 370, 376, 388, 397, 398, 411, 418, 431,
    438, 444, 520, 526, 544, 552, 553, 554, 555, 557, 602, 603, 634, 635]

# List of ghosts that can be replaced/changed in game.
GHOST_LIST: list[str] = ["yapoo1", "mapoo1", "mopoo1", "yapoo2", "mapoo2", "mopoo2", "banaoba", "topoo1", "topoo2",
    "topoo3", "topoo4","heypo1", "heypo2", "heypo3", "heypo4", "heypo5", "heypo6", "heypo7", "heypo8", "skul",
    "putcher1", "tenjyo", "tenjyo2"]

# List of ghosts that can be chosen from once a random selection has been made
RANDOM_GHOST_LISTS: list[list[str]] = [["yapoo1"], ["mapoo1"], ["mopoo1"], ["banaoba"], ["putcher1"],
    ["tenjyo", "tenjyo2"], ["heypo1", "heypo2", "heypo3", "heypo4", "heypo5", "heypo6", "heypo7", "heypo8"],
    ["topoo1", "topoo2", "topoo3", "topoo4"]]

# Dictionary of Freestanding Location names and their index in keyinfo.
LOCATION_TO_INDEX: dict[str, int] = {
    "The Well Key": 0,
    "Ghost Foyer Key": 1,
    "1F Bathroom Shelf Key": 3,
    "Fortune Teller Candles": 4,
    "Wardrobe Shelf Key": 5,
}

# List of Trees to update when WDYM is enabled.
WDYM_TREES: list[int] = [184, 185, 138, 139, 140, 141]

# List of Carpets, Roof Hut, and Telephone Room Frame that needs furniture height lifted.
WDYM_RAISE_LIST: list[int] = [628, 629, 683, 698, 716]

# List of other WDYM checks, such as gallery furniture, kitchen 4th wall, and rails/fences.
WDYM_MAKE_MOVE_LIST: list[int] = [9, 61, 69, 118, 303, 321, 322, 323, 23, 314]

CHEST_NAMES: list[str] = ["ytakara1", "rtakara1", "btakara1", "wtakara1", "gtakara1"]

# Converts AP readable name to in-game name
def get_item_name(item_data: dict, slot: int) -> str:
    if int(item_data["player"]) != slot:
        return "nothing"  # TODO return AP item(s) here

    if item_data["door_id"] != 0:
        return "key_" + str(item_data["door_id"])
    elif any(money_name in item_data["name"] for money_name in ["Coins", "Bills", "Gold Bars"]):
        if item_data["type"] in ("Freestanding", "Chest", "BSpeedy", "Mouse"):
            return "nothing" # Do not spawn the money physically let it be handled remotely
        return "money"

    match item_data["name"]:
        case "Fire Element Medal":
            return "elffst"
        case "Water Element Medal":
            return "elwfst"
        case "Ice Element Medal":
            return "elifst"

        case "Mario's Hat":
            return "mcap"
        case "Mario's Letter":
            return "mletter"
        case "Mario's Shoe":
            return "mshoes"
        case "Mario's Glove":
            return "mglove"
        case "Mario's Star":
            return "mstar"

        case "Gold Diamond":
            if item_data["type"] == "Freestanding" or item_data["type"] == "Chest":
                return "nothing"  # Do not spawn the gem physically let it be handled remotely
            return "rdiamond"
        case "Sapphire":
            if item_data["type"] in ("Freestanding", "Chest", "BSpeedy", "Mouse"):
                return "nothing"  # Do not spawn the gem physically let it be handled remotely
            return "sapphire"
        case "Emerald":
            if item_data["type"] in ("Freestanding", "Chest", "BSpeedy", "Mouse"):
                return "nothing"  # Do not spawn the gem physically let it be handled remotely
            return "emerald"
        case "Ruby":
            if item_data["type"] in ("Freestanding", "Chest", "BSpeedy", "Mouse"):
                return "nothing"  # Do not spawn the gem physically let it be handled remotely
            return "ruby"
        case "Diamond":
            if item_data["type"] == "Freestanding" or item_data["type"] == "Chest":
                return "nothing"  # Do not spawn the gem physically let it be handled remotely
            return "diamond"

        case "Poison Mushroom":
            if item_data["type"] == "Freestanding":
                return "nothing"
            return "mkinoko"
        case "Small Heart":
            return "sheart"
        case "Large Heart":
            return "lheart"
        case "Bomb":
            if item_data["type"] == "Freestanding":
                return "nothing"
            return "itembomb"
        case "Ice Trap":
            if item_data["type"] == "Freestanding":
                return "nothing"
            return "ice"
        case "Banana Trap":
            if item_data["type"] == "Freestanding":
                return "nothing"
            return "banana"

        case "Boo Radar":
            return "gameboy"
        case "Vacuum Upgrade" | "Poltergust 3000":
            return "vbody"

    return "nothing"


def get_item_appear_name(item_data: dict, slot: int) -> str:
    if int(item_data["player"]) != slot:
        return "nothing"  # TODO return AP item(s) here

    if item_data["door_id"] != 0:
        return "key_" + str(item_data["door_id"])

    if any(money_name in item_data["name"] for money_name in ["Coins", "Bills", "Gold Bars"]):
        return "money"

    match item_data["name"]:
        case "Fire Element Medal":
            return "elffst"
        case "Water Element Medal":
            return "elwfst"
        case "Ice Element Medal":
            return "elifst"

        case "Mario's Hat":
            return "mcap"
        case "Mario's Letter":
            return "mletter"
        case "Mario's Shoe":
            return "mshoes"
        case "Mario's Glove":
            return "mglove"
        case "Mario's Star":
            return "mstar"

        case "Gold Diamond" | "Sapphire" | "Emerald" | "Ruby" | "Diamond":
            return "money"

        case "Poison Mushroom":
            return "mkinoko"
        case "Small Heart":
            return "sheart"
        case "Large Heart":
            return "lheart"
        case "Bomb":
            return "itembomb"
        case "Ice Trap":
            return "ice"
        case "Banana Trap":
            return "banana"

        case "Boo Radar":
            return "gameboy"
        case "Vacuum Upgrade" | "Poltergust 3000":
            return "vbody"

    return "nothing"

def find_item_appear_index(item_appear_entries: list[JMPEntry], item_name: str) -> int:
    # Within the itemappear table relevant to the map, find the item that matches the same name.
    # Once found, return the first instance of that itemappear's index.
    filtered_item_appear: list[int] = [index for index, item_appear_entry in enumerate(item_appear_entries)
        if str(item_appear_entry["item0"]) == item_name]
    return filtered_item_appear[0]


# Indicates the chest size that will be loaded in game based on item provided. 0 = small, 1 = medium, 2 = large
def get_chest_size_from_item(lm_gen: "LuigisMansionRandomizer", item_data: dict, current_size: int) -> int:
    chest_option: int = int(lm_gen.output_data["Options"]["chest_types"])
    door_id: int = int(item_data["door_id"])

    # Vanilla chest options were chosen
    if chest_option == 0 or item_data["room_no"] == 11:
        return current_size

    # This is a door and should select based on the key size
    elif door_id > 0:
        return _get_chest_size_from_key(door_id)

    item_name: str = str(item_data["name"])
    is_for_slot: bool = lm_gen.slot == int(item_data["player"])
    item_class: str = str(item_data["classification"])

    # Match either what the item represents in vanilla or match against AP item classification
    if chest_option == 1 or chest_option == 3:
        return _chest_size_match_name(item_name, is_for_slot)

    # Both size and color are matched against AP item class
    elif chest_option == 4:
        return _chest_size_item_class(lm_gen, item_class)

    # Uses receiving player's item class to prioritize size
    elif chest_option == 5:
        if not is_for_slot:
            return _chest_size_item_class(lm_gen, item_class)

        return _chest_size_match_name(item_name, is_for_slot)

    # Full random, or something equivalent was chosen (Like Option 2)
    else:
        return lm_gen.random.choice(sorted([0, 1, 2]))

# Indicates the chest size that will be loaded in game based on key type. 0 = small, 1 = medium, 2 = large
def _get_chest_size_from_key(key_id) -> int:
    match key_id:
        case 3 | 42 | 59 | 72:
            return 2
        case _:
            return 0

def _chest_size_item_class(lm_gen: "LuigisMansionRandomizer", item_class: str) -> int:
    trap_option: int = int(lm_gen.output_data["Options"]["trap_chests"])

    if "progression" in item_class:
        return 2
    elif "useful" in item_class:
        return 1
    elif "trap" in item_class:
        if trap_option == 0:
            return 0
        elif trap_option == 1:
            return 2
        else:
            return lm_gen.random.choice(sorted([0, 1, 2]))
    # Filler or something else
    else:
        return 0

def _chest_size_match_name(item_name: str, is_for_slot: bool) -> int:
    # Avoids situations where "Boo" may be in other games
    if "Boo" in item_name and is_for_slot:
        return 0

    # "Money" is easier to handle than all types of money/bundles
    if any(iname in item_name for iname in MONEY_ITEM_NAMES):
        item_name = "Money"
    match item_name:
        case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
            return 0
        case "Small Heart" | "Money":
            return 0
        case "Large Heart":
            return 1
        case "Poison Mushroom" | "Bomb" | "Ice Trap" | "Gold Diamond" | "Banana Trap":
            return 2
        case "Fire Element Medal" | "Water Element Medal" | "Ice Element Medal":
            return 2
        case "Sapphire" | "Emerald" | "Ruby" | "Diamond":
            return 1

    return 0


# Changes the type of chest loaded in game based on the type of item that is hidden inside
def get_item_chest_visual(lm_gen: "LuigisMansionRandomizer", item_data: dict, current_visual: str) -> str:
    chest_option: int = int(lm_gen.output_data["Options"]["chest_types"])

    # Vanilla chest options were chosen
    if chest_option == 0 or item_data["room_no"] == 11:
        return current_visual

    item_name: str = str(item_data["name"])
    is_for_slot: bool = lm_gen.slot == int(item_data["player"])
    item_class: str = str(item_data["classification"])

    # Match the item represents in vanilla
    if chest_option == 1:
        return _chest_visual_match_name(item_name, True, is_for_slot)

    # Chest Visual are determined by AP item classification
    elif chest_option == 3 or chest_option == 4:
        return _chest_visual_item_class(lm_gen, item_class)

    # Uses receiving player's item class to prioritize visual
    elif chest_option == 5:
        if not is_for_slot:
            return _chest_visual_item_class(lm_gen, item_class)
        return _chest_visual_match_name(item_name, False, is_for_slot)

    # Full random, or something equivalent was chosen (Like Option 2)
    else:
        return lm_gen.random.choice(sorted(CHEST_NAMES))

def _chest_visual_item_class(lm_gen: "LuigisMansionRandomizer", item_class: str) -> str:
    trap_option: int = int(lm_gen.output_data["Options"]["trap_chests"])

    if "progression" in item_class:
        return "ytakara1"
    elif "useful" in item_class:
        return "btakara1"
    elif "trap" in item_class:
        if trap_option == 0:
            return "rtakara1"
        elif trap_option == 1:
            return "ytakara1"
        else:
            return lm_gen.random.choice(sorted(CHEST_NAMES))
    # Filler or something else
    else:
        return "gtakara1"

def _chest_visual_match_name(item_name: str, fuzzy_match: bool, is_for_slot: bool) -> str:
    # Avoids situations where "Boo" may be in other games
    if "Boo" in item_name and is_for_slot:
        return "wtakara1"

    if fuzzy_match:
        item_name = _fuzzy_match_item_name(item_name)
    else:
        # "Money" is easier to handle than all types of money/bundles
        if any(money_name for money_name in MONEY_ITEM_NAMES if money_name in item_name):
            item_name = "Money"
    match item_name:
        case "Heart Key" | "Club Key" | "Diamond Key" | "Spade Key":
            return "ytakara1"
        case "Small Heart" | "Large Heart" | "Banana Trap":
            return "ytakara1"
        case "Fire Element Medal" | "Bomb" | "Ruby":
            return "rtakara1"
        case "Water Element Medal" | "Poison Mushroom" | "Sapphire":
            return "btakara1"
        case "Ice Element Medal" | "Ice Trap" | "Diamond":
            return "wtakara1"
        case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
            return "rtakara1"
        case "Gold Diamond" | "Emerald" | "Money":
            return "gtakara1"

    return "btakara1"

def _fuzzy_match_item_name(item_name: str) -> str:
    if any(iname in item_name for iname in MONEY_ITEM_NAMES):
        item_name = "Money"
    elif any(iname in item_name for iname in EXPLODE_ITEM_NAMES):
        item_name = "Bomb"
    elif any(iname in item_name for iname in LIGHT_ITEM_NAMES):
        item_name = "Banana Trap"
    elif any(iname in item_name for iname in BLUEISH_ITEM_NAMES):
        item_name = "Sapphire"
    elif any(iname in item_name for iname in ICY_ITEM_NAMES):
        item_name = "Ice Trap"
    return item_name

# Indicates the key model to use when spawning the item.
def _get_key_name(door_id):
    match door_id:
        case 3:
            return "key02"
        case 42:
            return "key03"
        case 59:
            return "key04"
        case 72:
            return "key05"
        case _:
            return "key01"

def create_iteminfo_entry(item_door_id: int, info_item_name: str, hp_amt: int=0, is_escape: int=0) -> dict:
    """Creates a dictionary for use in the iteminfotable"""
    open_no: int = item_door_id
    if open_no > 0:
        char_name: str = _get_key_name(open_no)
    else:
        char_name = info_item_name

    return {
        "name": info_item_name,
        "character_name": char_name,
        "OpenDoorNo": open_no,
        "HPAmount": hp_amt,
        "IsEscape": is_escape
    }

def create_observer_entry(pos_x: float, pos_y: float, pos_z: float, room_no: int, cond_type: int, do_type: int,
    arg0: int = 0, arg1: int = 0, arg2: int = 0, arg3: int = 0, arg4: int = 0, arg5: int = 0, code_name: str = "(null)",
    string_arg0: str = "(null)", cond_string_arg0: str = "(null)", cond_arg0: int = 0,
    appear_flag: int = 0, disappear_flag: int = 0) -> dict[str, Any]:

    return {
        "name": "observer", # Arbitrary, can be whatever
        "code_name": code_name,
        "string_arg0": string_arg0,
        "cond_string_arg0": cond_string_arg0,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "pos_z": pos_z,
        "dir_x": 0.000000, # Useless, does not function in game
        "dir_y": 0.000000, # Useless, does not function in game
        "dir_z": 0.000000, # Useless, does not function in game
        "scale_x": 1.000000, # Useless, does not function in game
        "scale_y": 1.000000, # Useless, does not function in game
        "scale_z": 1.000000, # Useless, does not function in game
        "room_no": room_no,
        "cond_arg0": cond_arg0,
        "arg0": arg0,
        "arg1": arg1,
        "arg2": arg2,
        "arg3": arg3,
        "arg4": arg4,
        "arg5": arg5,
        "appear_flag": appear_flag,
        "disappear_flag": disappear_flag,
        "cond_type": cond_type,
        "do_type": do_type,
        "invisible": 1, # This makes the observer not visible in game.
        "(Undocumented)": 0 # This currently does not do anything but is recommended to be set to 0
    }

# Creates an entry dict for the itemappeartable
def create_itemappear_entry(item_name: str) -> dict:
    new_item = {}
    for itemid in range(20):
        new_item["item" + str(itemid)] = item_name
    return new_item

def apply_new_ghost(lm_rando: "LuigisMansionRandomizer", enemy_entry: JMPEntry, element: str):
    # TODO add a default heigh for ghosts on each floor to re-adjust things moving up and down.
    # The list of ghosts that can replace the vanilla ones. Only includes the ones without elements.
    # Excludes Skul ghosts as well unless the railinfo jmp table is updated.

    # If the vanilla ghost is a Ceiling Ghost, reduce its spawning Y position so the new ghost spawns on the floor.
    curr_enemy_name: str = str(enemy_entry["name"])
    curr_pos_y: float = float(enemy_entry["pos_y"])
    if "tenjyo" in curr_enemy_name:
        enemy_entry["pos_y"] = curr_pos_y - 200.000000

    # If a room is supposed to have an element, replace all the ghosts in it to be only ghosts with that element.
    # Otherwise, randomize the ghosts between the non-element ones from the list.
    match element:
        case "Ice":
            enemy_entry["name"] = "mapoo2"
        case "Water":
            enemy_entry["name"] = "mopoo2"
        case "Fire":
            enemy_entry["name"] = "yapoo2"
        case "No Element":
            # No Shy Guy ghosts allowed currently, as they need a path defined in a path file to be used correctly.
            no_shy_ghosts: list[list[str]] = copy.deepcopy(RANDOM_GHOST_LISTS)
            no_shy_ghosts = [enemy_list for enemy_list in no_shy_ghosts if not
                any("heypo" in enemy_name for enemy_name in enemy_list)]
            new_enemy = lm_rando.random.choice(sorted(list(lm_rando.random.choice(sorted(no_shy_ghosts)))))
            enemy_entry["name"] = new_enemy

    # If the new ghost is a Ceiling Ghost, increase its spawning Y position so it spawns in the air.
    new_pos_y: float = float(enemy_entry["pos_y"])
    if "tenjyo" in curr_enemy_name:
        enemy_entry["pos_y"] = new_pos_y + 200.000000


def get_output_dict(lm_rando: "LuigisMansionRandomizer") -> dict:
    """Gets the furniture/plant dicts in which we want to get items for/create."""
    output_dict: dict = {**lm_rando.output_data["Locations"]["Furniture"]}
    if "Plant" in lm_rando.output_data["Locations"].keys():
        output_dict: dict = {
            **output_dict,
            **lm_rando.output_data["Locations"]["Plant"]}
    return output_dict

def update_furniture_entries(lm_rando: "LuigisMansionRandomizer", map_id: int, furniture_entries: list[JMPEntry],
    item_appear_entries: list[JMPEntry]):
    """Updates the various furniture that needs to be changed and looks up the related item from the item_appear table
    that will spawn once interacted with."""
    for loc_name, loc_data in get_output_dict(lm_rando).items():
        if not int(loc_data["map_id"]) == map_id:
            continue

        location_data: LMLocationData = ALL_LOCATION_TABLE[loc_name]
        furniture_entry: JMPEntry = furniture_entries[loc_data["loc_enum"]]
        if location_data.remote_only:
            furniture_entry["generate"] = 0
            furniture_entry["generate_num"] = 0
            furniture_entry["item_table"] = 0
            continue

        actor_item_name = get_item_appear_name(loc_data, lm_rando.slot)
        if not actor_item_name == "money":
            furniture_entry["item_table"] = find_item_appear_index(item_appear_entries, actor_item_name) if map_id == 2 else 0 # TODO Remove this once itemappear is fixed.
            furniture_entry["generate"] = 0
            furniture_entry["generate_num"] = 0
            continue

        # Update the Money fields based on the Money provided.
        furniture_entry["item_table"] = 11
        int_money_amt = 1
        if re.search(r"^\d+", loc_data["name"]):
            int_money_amt = int(re.search(r"^\d+", loc_data["name"]).group())
        furniture_entry["generate_num"] = int_money_amt
        if "Coins" in loc_data["name"]:
            if "Bills" in loc_data["name"]:
                furniture_entry["generate"] = 3
            else:
                furniture_entry["generate"] = 1
        elif "Bills" in loc_data["name"]:
            furniture_entry["generate"] = 2
        elif "Sapphire" in loc_data["name"]:
            furniture_entry["generate"] = 4
        elif "Emerald" in loc_data["name"]:
            furniture_entry["generate"] = 6
        elif "Ruby" in loc_data["name"]:
            furniture_entry["generate"] = 5
        elif "Gold Bar" in loc_data["name"]:
            furniture_entry["generate"] = 7
        elif loc_data["name"] == "Diamond":
            furniture_entry["generate"] = 9
        elif loc_data["name"] == "Gold Diamond":
            furniture_entry["generate"] = 10

def update_item_info_entries(lm_rando: "LuigisMansionRandomizer", item_info: JMP):
    """Adds any items that dont already exist in the item_info table."""
    already_exist: list[str] = [str(i_entry["name"]) for i_entry in item_info.data_entries]

    for loc_name, loc_data in get_output_dict(lm_rando).items():
        lm_item_name: str = get_item_name(loc_data, lm_rando.slot)
        if not lm_item_name in already_exist:
            item_info.add_jmp_entry(create_iteminfo_entry(loc_data["door_id"], lm_item_name))
            already_exist.append(lm_item_name)