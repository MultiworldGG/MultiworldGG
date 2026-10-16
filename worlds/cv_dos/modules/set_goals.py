import struct
from .text_builder import text_encoder


def set_goal_triggers(world, condition, area) -> set:
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
        rom.write_to_file(0x02225BC0 + 0x10 * index, "overlay_0", bytearray([trigger_keys.index(condition)]))  # Write the actual condition key
        required_flags = 0
        if condition in ["bosses"]:  # More will be added to this in the future
            condition_list = goal_rule_order[index]
            for flag in condition_list:
                required_flags |= boss_flags[flag]
        rom.write_to_file(0x02225BC2 + 0x10 * index, "overlay_0", struct.pack("H", required_flags))

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
                    condition_text += f"-{boss_text[flag]}\v"  # line break after doing 3 lines
                else:
                    condition_text += f"-{boss_text[flag]}\n"
        string_array = [0x01, 0x00, 0xE7, 0x04, 0xE3, 0x18]  # Initialize the string + use Hammer's data
        string_array += text_encoder(condition_text)

        if string_array[len(string_array) - 1] != 0xE9:
            string_array.append(0xE5)  # Add a button press to close out the text
        string_array.extend([0xE4, 0xEA])  # Close out the textbox
        rom.write_to_file(0x02229960 + (0x200 * index), "overlay_0", bytearray(string_array))
