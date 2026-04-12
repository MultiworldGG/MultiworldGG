import struct

dawn_text_map = {" ": 0x00, '"': 0x02, "#": 0x03, "$": 0x04, "%": 0x05,
       "&": 0x06, "'": 0x07, "(": 0x08, ")": 0x09, "*": 0x0A,
       "+": 0x0B, ",": 0x0C, "-": 0x0D, ".": 0x0E, "/": 0x0F,
       "0": 0x10, "1": 0x11, "2": 0x12, "3": 0x13, "4": 0x14,
       "5": 0x15, "6": 0x16, "7": 0x17, "8": 0x18, "9": 0x19,
       ":": 0x1A, ";": 0x1B, "<": 0x1C, "=": 0x1D, ">": 0x1E,
       "?": 0x1F, "@": 0x20, "A": 0x21, "B": 0x22, "C": 0x23,
       "D": 0x24, "E": 0x25, "F": 0x26, "G": 0x27, "H": 0x28,
       "I": 0x29, "J": 0x2A, "K": 0x2B, "L": 0x2C, "M": 0x2D,
       "N": 0x2E, "O": 0x2F, "P": 0x30, "Q": 0x31, "R": 0x32,
       "S": 0x33, "T": 0x34, "U": 0x35, "V": 0x36, "W": 0x37,
       "X": 0x38, "Y": 0x39, "Z": 0x3A, "[": 0x3B, "\\": 0x3C,
       "]": 0x3D, "^": 0x3E, "_": 0x3F, "`": 0x40, "a": 0x41,
       "b": 0x42, "c": 0x43, "d": 0x44, "e": 0x45, "f": 0x46,
       "g": 0x47, "h": 0x48, "i": 0x49, "j": 0x4A, "k": 0x4B,
       "l": 0x4C, "m": 0x4D, "n": 0x4E, "o": 0x4F, "p": 0x50,
       "q": 0x51, "r": 0x52, "s": 0x53, "t": 0x54, "u": 0x55,
       "v": 0x56, "w": 0x57, "x": 0x58, "y": 0x59, "z": 0x5A,
       "{": 0x5B, "|": 0x5C, "}": 0x5D, "~": 0x5E, "■": 0x5F,
       "¢": 0x61, "£": 0x62, "©": 0x64, "®": 0x65, "°": 0x66,
       "±": 0x67, "¿": 0x6A, "Á": 0x6B, "Á": 0x6C, "\n": 0xE6,
       "\v": [0xE5, 0xE9]}

def set_goal_triggers(world, condition, area):
    if condition == "throne_room":
        goal = {"Aguni Defeated"}
    elif condition == "garden":
        goal = {"Power of Darkness"}
    elif condition == "bosses":
        goal = {"Village Boss Clear", "Lab Boss Clear", "Chapel Boss Clear", "Inner Chapel Boss Clear", "Garden Boss Clear", "Guest House Boss Clear",
               "Subterranean Hell Boss Clear", "Tower Boss Clear", "Clock Tower Boss Clear", "Ruins Boss Clear", "Aguni Defeated", "Upper Guest House Boss Clear",
               "Mine Boss Clear", "Abyss Boss Clear"}
        if area == "Mine" or world.mine_status == "Disabled" or (world.mine_status == "Locked" and area == world.mine_requisites):
            goal.remove("Mine Boss Clear")
            goal.remove("Abyss Boss Clear")
        if not world.options.goal:
            goal.remove("Aguni Defeated")
    else:
        goal = None
    
    return goal

def write_goal_triggers(world, rom):
    goal_settings = [
        world.options.garden_condition,
        world.options.mine_condition,
        world.options.menace_condition
    ]

    trigger_keys = [
        "none",
        "throne_room",
        "garden",
        "bosses"
    ]

    goal_rule_order = [
        world.garden_triggers,
        world.mine_triggers,
        world.menace_triggers
    ]

    boss_flags = {
        "Village Boss Clear": 0x02,
        "Lab Boss Clear": 0x04,
        "Chapel Boss Clear": 0x08,
        "Inner Chapel Boss Clear": 0x10,
        "Garden Boss Clear": 0x20,
        "Guest House Boss Clear": 0x40,
        "Tower Boss Clear": 0x80,
        "Subterranean Hell Boss Clear": 0x0100,
        "Clock Tower Boss Clear": 0x0200,
        "Ruins Boss Clear": 0x0400,
        "Aguni Defeated": 0x0800,
        "Upper Guest House Boss Clear": 0x1000,
        "Mine Boss Clear": 0x2000,
        "Abyss Boss Clear": 0x8000  # 4000 is used for the Garden

    }

    boss_text = {
        "Village Boss Clear": "Lost Village",
        "Lab Boss Clear": "Wizardry Lab",
        "Chapel Boss Clear": "Dark Chapel",
        "Inner Chapel Boss Clear": "Inner Dark Chapel",
        "Garden Boss Clear": "Garden of Madness",
        "Guest House Boss Clear": "Demon Guest House",
        "Tower Boss Clear": "Condemned Tower",
        "Subterranean Hell Boss Clear": "Subterranean Hell",
        "Clock Tower Boss Clear": "Cursed Clock Tower",
        "Ruins Boss Clear": "Silenced Ruins",
        "Aguni Defeated": "Pinnacle",
        "Upper Guest House Boss Clear": "Upper Guest House",
        "Mine Boss Clear": "Mine of Judgment",
        "Abyss Boss Clear": "Abyss"
    }

    for index, trigger in enumerate(goal_settings):
        condition = trigger.current_key
        rom.write_bytes(0x153F47 + 0x10 * index, bytearray([trigger_keys.index(condition)]))  # Write the actual condition key
        required_flags = 0
        if condition in ["bosses"]:  # More will be added to this in the future
            condition_list = goal_rule_order[index]
            for flag in condition_list:
                required_flags |= boss_flags[flag]
        rom.write_bytes(0x153F48 + 0x10 * index, struct.pack("H", required_flags))

        condition_text = "Yo, I've got some intel for you.\nTo access this area, you need to\n"

        if condition == "throne_room":
            condition_text += "defeat whatever's in the throne room."
        elif condition == "garden":
            condition_text += "reject the power of darkness."
        elif condition in ["bosses"]:
            condition_text += " defeat the bosses of these areas.\v"
            for con_index, flag in enumerate(condition_list):
                if (con_index + 1) & 1:
                    condition_text += f"-{boss_text[flag]}   "
                elif not (con_index + 1) % 6:
                    condition_text += f"-{boss_text[flag]}\v" # line break after doing 3 lines
                else:
                    condition_text += f"-{boss_text[flag]}\n"
        string_array = [0x01, 0x00, 0xE7, 0x04, 0xE3, 0x18] # Initialize the string + use Hammer's data
        for char in condition_text:
            if isinstance(dawn_text_map[char], list):
                string_array.extend(dawn_text_map[char])
            else:
                string_array.append(dawn_text_map[char])

        if string_array[len(string_array) - 1] != 0xE9:
            string_array.append(0xE5)  # Add a button press to close out the text
        string_array.extend([0xE4, 0xEA])  # Close out the textbox
        rom.write_bytes(0x15096F + (0x200 * index), bytearray(string_array))