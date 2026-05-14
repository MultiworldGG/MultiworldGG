from ...data import ITEMS_DATA


def get_item_id_and_subid(item: dict):
    # Remote item, use the generic "Archipelago Item"
    if item["item"] == "Archipelago Item" or ("player" in item and not item["progression"]):
        return 0x41, 0x00
    if item["item"] == "Archipelago Progression Item" or ("player" in item and item["progression"]):
        return 0x41, 0x01

    # Local item, put the real item in there
    item_data = ITEMS_DATA[item["item"]]
    item_id = item_data["id"]
    item_subid = item_data["subid"] if "subid" in item_data else 0x00
    if item_id == 0x30:
        item_subid = item_subid & 0x7F  # TODO : Remove when/if master key becomes available on non-master key worlds
    return item_id, item_subid

def camel_case(text):
    """
    Replaces minuses or understores with spaces and upercases all but the first letter of a word.

    Parameters:
        text (str): The text to work with.

    Returns:
        str: The completed text.
    """
    if len(text) == 0:
        return text
    s = text.replace("-", " ").replace("_", " ").split()
    return s[0] + "".join(i.capitalize() for i in s[1:])


def convert_value_to_digits(value: int) -> list[int]:
    """
    Converts a value into digits.

    Parameters:
        value (int): A value to work with.

    Returns:
        list: digits that were made during the conversion.
    """
    digits = []
    while value > 0:
        digits.append(0x30 + (value % 10))
        value = int(value / 10)
    # If list is empty, it means requirement was <= 0, so just display "0"
    if len(digits) == 0:
        digits = [0x30]
    return list(reversed(digits))


def get_available_random_colors_from_sprite_name(sprite_filename: str) -> list[str]:
    """
    Parses the sprite filename to detect a potential "accepted colors suffix" which uses the following format:
    mysrite_<COLORS>.bin, where COLORS is a set of letters representing which colors can be rolled as random colors
    for that sprite.
    This was built for people who play with both random sprite & random color, but who want a subset of colors for
    each sprite (e.g. if they play a Tokay, they only want it orange or red).
    Parameters:
        sprite_filename (str): The name of the sprite to load.
    
    Returns:
        list: Returns a list of available colors for a user's sprite.
    """
    CHARACTER_COLORS = {
        "r": "red",
        "g": "green",
        "b": "blue",
        "o": "orange",
    }

    filename_parts = sprite_filename.split("_")
    if len(filename_parts) <= 1:
        return list(CHARACTER_COLORS.values())

    # Get the final part of the filename and remove the ".bin" extension
    suffix = filename_parts[-1][0:-4]
    if len(suffix) > len(CHARACTER_COLORS.values()):
        return list(CHARACTER_COLORS.values())  # Too long, not a color suffix

    return [color for letter, color in CHARACTER_COLORS.items() if letter in suffix]


def simple_hex(num: int, size: int = 2) -> str:
    """
    Gets a hex string from a number

    Parameters:
        num (int) A number that will be converted into a hex string.
        size (int) The size of the hex string, in number of characters. Default is 2.

    Returns:
        str: Hex from the given number.
    """
    return hex(num)[2:].rjust(size, "0")


def script_delay(frames: int) -> str:
    """
    Gets a script delay from a number of frames.
    
    Parameters:
        frames (int) A number of frames to convert into a script delay.
    Returns:     
        str: A script delay from the given number of frames.
    """
    known_delays = [1, 4, 8, 10, 15, 20, 30, 40, 60, 90, 120, 180, 240]
    if frames in known_delays:
        delay_index = known_delays.index(frames)
        return f"db $f{simple_hex(delay_index, 1)}\n"
    elif frames > 0xff:
        return script_delay(240) + script_delay(frames - 240)
    else:
        return f"db setcounter1,${simple_hex(frames)}\n"
