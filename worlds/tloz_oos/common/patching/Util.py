def camel_case(text: str) -> str:
    if len(text) == 0:
        return text
    s = text.replace("-", " ").replace("_", " ").split()
    return s[0] + "".join(i.capitalize() for i in s[1:])


def convert_value_to_digits(value: int) -> list[int]:
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
    Parse the sprite filename to detect a potential "accepted colors suffix" which uses the following format:
    mysrite_<COLORS>.bin, where COLORS is a set of letters representing which colors can be rolled as random colors
    for that sprite.
    This was built for people who play with both random sprite & random color, but who want a subset of colors for
    each sprite (e.g. if they play a Tokay, they only want it orange or red).
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
    return hex(num)[2:].rjust(size, "0")


def script_delay(frames: int) -> str:
    known_delays = [1, 4, 8, 10, 15, 20, 30, 40, 60, 90, 120, 180, 240]
    if frames in known_delays:
        delay_index = known_delays.index(frames)
        return f"db $f{simple_hex(delay_index, 1)}\n"
    elif frames > 0xff:
        return script_delay(240) + script_delay(frames - 240)
    else:
        return f"db setcounter1,${simple_hex(frames)}\n"
