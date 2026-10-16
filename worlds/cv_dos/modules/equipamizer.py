from dataclasses import dataclass
from ..Options import RandomWeaponAttributes, RandomWeaponStats
import struct
from .text_builder import text_encoder, calculate_text_width


@dataclass
class DoSWeapon:
    atk: int  # The weapon's attack value
    element: str  # Base element
    frames: int  # How many enemy I-frames this weapon has
    type: str  # Weapon class
    sub_element: str = "None"  # Secondary element, if any
    modifier: str = "None"  # Modifier, if any


modifier_list = [
    "None",
    "Heavy",  # Animation persists after landing
    "Light",  # Animation does not persist after landing
    "Thorned",  # I-frame value is halved
    "Spectral"  # Can walk while moving, Attack is halved
]

sub_elements = ["Fire", "Ice", "Lightning", "Dark", "Holy", "Poison", "Curse", "Petrify"]

element_flags = {
    "None": 0x00,
    "Strike": 0x01,
    "Stab": 0x02,
    "Slash": 0x04,
    "Fire": 0x08,
    "Ice": 0x10,
    "Lightning": 0x20,
    "Dark": 0x40,
    "Holy": 0x80,
    "Poison": 0x0100,
    "Curse": 0x0200,
    "Petrify": 0x0400,
    "Fist": 0x80000000
}

base_address = 0x0209C34C

mod_abbreviations = {
    "Heavy": "Hv",
    "Light": "Lt",
    "Spectral": "Sp",
    "Thorned": "Th"
}

element_abbreviations = {
    "Strike": "Stk",
    "Stab": "Stb",
    "Slash": "Sls",
    "Fire": "Fir",
    "Ice": "Ice",
    "Lightning": "Lit",
    "Dark": "Drk",
    "Holy": "Hly",
    "Poison": "Psn",
    "Curse": "Crs",
    "Petrify": "Stn"
}


def apply_weapon_randomization(world, rom):
    weapons_list = {
        "Bare knuckles": DoSWeapon(0x00, "Strike", 0x08, "None"),
        "Knife": DoSWeapon(0x07, "Stab", 0x0F, "Knife"),
        "Baselard": DoSWeapon(0x0F, "Stab", 0x0F, "Knife"),
        "Combat Knife": DoSWeapon(0x0B, "Stab", 0x0F, "Knife"),
        "Cutall": DoSWeapon(0x13, "Stab", 0x0F, "Knife"),
        "Cinquedia": DoSWeapon(0x19, "Stab", 0x0F, "Knife"),

        "Rapier": DoSWeapon(0x10, "Stab", 0x1E, "Rapier"),
        "Fleuret": DoSWeapon(0x14, "Stab", 0x1E, "Rapier"),
        "Main Gauche": DoSWeapon(0x18, "Stab", 0x1E, "Rapier"),
        "Small Sword": DoSWeapon(0x1C, "Stab", 0x1E, "Rapier"),
        "Estoc": DoSWeapon(0x20, "Stab", 0x1E, "Rapier"),
        "Whip Sword": DoSWeapon(0x24, "Stab", 0x1E, "Rapier"),
        "Garian Sword": DoSWeapon(0x28, "Stab", 0x1E, "Rapier"),
        "Kris Naga": DoSWeapon(0x2D, "Stab", 0x1E, "Rapier"),
        "Nebula": DoSWeapon(0x34, "Stab", 0x1E, "Rapier"),

        "Short Sword": DoSWeapon(0x0F, "Slash", 0x0F, "Sword"),
        "Cutlass": DoSWeapon(0x14, "Slash", 0x0F, "Sword"),
        "Long Sword": DoSWeapon(0x1A, "Slash", 0x0F, "Sword"),
        "Fragarach": DoSWeapon(0x20, "Slash", 0x0F, "Sword"),
        "Hrunting": DoSWeapon(0x26, "Slash", 0x0F, "Sword", "Poison"),
        "Mystletain": DoSWeapon(0x1C, "Slash", 0x0F, "Sword", "Holy"),
        "Joyeuse": DoSWeapon(0x2B, "Slash", 0x0F, "Sword"),
        "Milican's Sword": DoSWeapon(0x01, "Slash", 0x0F, "Sword", "Petrify"),
        "Ice Brand": DoSWeapon(0x30, "Slash", 0x12, "Sword", "Ice"),
        "Laevatain": DoSWeapon(0x19, "Slash", 0x0C, "Sword", "Fire"),
        "Burtgang": DoSWeapon(0x3A, "Slash", 0x0F, "Sword"),
        "Kaladbolg": DoSWeapon(0x41, "Slash", 0x0F, "Sword"),
        "Valmanway": DoSWeapon(0x24, "Stab", 0x0C, "Sword"),
        "Alucard Sword": DoSWeapon(0x37, "Slash", 0x0C, "Sword"),

        "Claymore": DoSWeapon(0x1C, "Slash", 0x23, "Greatsword"),
        "Falchion": DoSWeapon(0x27, "Slash", 0x23, "Greatsword"),
        "Great Sword": DoSWeapon(0x32, "Slash", 0x23, "Greatsword"),
        "Durandal": DoSWeapon(0x3D, "Slash", 0x23, "Greatsword"),
        "Dainslef": DoSWeapon(0x48, "Slash", 0x23, "Greatsword", "Curse"),
        "Ascalon": DoSWeapon(0x53, "Slash", 0x23, "Greatsword"),
        "Balmung": DoSWeapon(0x5E, "Slash", 0x23, "Greatsword"),
        "Final Sword": DoSWeapon(0x6E, "Slash", 0x23, "Greatsword"),
        "Claimh Solais": DoSWeapon(0x78, "Slash", 0x1E, "Greatsword", "Holy"),

        "Spear": DoSWeapon(0x18, "Stab", 0x1E, "Spear"),
        "Partizan": DoSWeapon(0x20, "Stab", 0x1E, "Spear"),
        "Halberd": DoSWeapon(0x28, "Stab", 0x1E, "Spear"),
        "Lance": DoSWeapon(0x31, "Stab", 0x1E, "Spear"),
        "Trident": DoSWeapon(0x3A, "Stab", 0x1E, "Spear"),
        "Brionac": DoSWeapon(0x44, "Stab", 0x1E, "Spear"),
        "Geiborg": DoSWeapon(0x50, "Stab", 0x1E, "Spear"),
        "Longinus": DoSWeapon(0x5C, "Stab", 0x1E, "Spear"),
        "Gungner": DoSWeapon(0x38, "Stab", 0x0C, "Spear", "Lightning"),

        "Mace": DoSWeapon(0x20, "Strike", 0x28, "Hammer"),
        "Morgenstern": DoSWeapon(0x32, "Strike", 0x28, "Hammer", "Stab"),
        "Mjollnjr": DoSWeapon(0x1C, "Strike", 0x0C, "Hammer", "Lightning"),

        "Axe": DoSWeapon(0x2D, "Slash", 0x28, "Axe"),
        "Battle Axe": DoSWeapon(0x41, "Slash", 0x28, "Axe"),
        "Bhuj": DoSWeapon(0x5A, "Slash", 0x28, "Axe"),
        "Great Axe": DoSWeapon(0x73, "Slash", 0x28, "Axe"),
        "Golden Axe": DoSWeapon(0x8C, "Slash", 0x28, "Axe"),
        "Death Scythe": DoSWeapon(0xA6, "Slash", 0x28, "Axe", "Dark"),

        "Blunt Sword": DoSWeapon(0x12, "Slash", 0x08, "Katana"),
        "Katana": DoSWeapon(0x18, "Slash", 0x08, "Katana"),
        "Kotetsu": DoSWeapon(0x1F, "Slash", 0x08, "Katana"),
        "Masamune": DoSWeapon(0x27, "Slash", 0x08, "Katana"),
        "Osafune": DoSWeapon(0x30, "Slash", 0x08, "Katana"),
        "Kunitsuna": DoSWeapon(0x3A, "Slash", 0x08, "Katana"),
        "Yasutsuna": DoSWeapon(0x45, "Slash", 0x08, "Katana"),
        "Muramasa": DoSWeapon(0x54, "Slash", 0x08, "Katana", "Curse"),

        "Brass Knuckles": DoSWeapon(0x05, "Strike", 0x08, "Fist", "Fist"),
        "Cestus": DoSWeapon(0x0C, "Strike", 0x08, "Fist", "Fist"),
        "Whip Knuckle": DoSWeapon(0x14, "Strike", 0x08, "Fist", "Fist"),
        "Mach Punch": DoSWeapon(0x1E, "Strike", 0x0A, "Fist", "Fist"),
        "Kaiser Knuckle": DoSWeapon(0x0F, "Strike", 0x08, "Fist", "Fist"),

        "Handgun": DoSWeapon(0x0F, "Stab", 0x03, "Gun"),
        "Silver Gun": DoSWeapon(0x1E, "Stab", 0x03, "Gun"),

        "Boomerang": DoSWeapon(0x06, "Slash", 0x14, "Throwing"),
        "Chakram": DoSWeapon(0x0C, "Slash", 0x14, "Throwing"),
        "Tomahawk": DoSWeapon(0x14, "Slash", 0x14, "Throwing"),
        "Throwing Sickle": DoSWeapon(0x1E, "Slash", 0x14, "Throwing"),

        "RPG": DoSWeapon(0x64, "Slash", 0x1E, "Gun"),

        "Terror Bear": DoSWeapon(0x01, "Strike", 0x04, "Bear", "Curse"),
        "Nunchakus": DoSWeapon(0x1E, "Strike", 0x0C, "Nunchuks"),
        "Whip": DoSWeapon(0x3C, "Strike", 0x1E, "Whip")
    }

    saved_elements = {}
    saved_percents = {}
    text_address = 0x02228DD0

    for weapon in weapons_list:
        data = weapons_list[weapon]
        id_num = list(weapons_list).index(weapon)
        rolled_subel = False
        rolled_element = False
        rolled_mod = False
        name_mod = ""

        if not id_num:
            continue  # Don't randomize the Fists
        name = weapon

        if world.options.randomize_weapon_stats != RandomWeaponStats.option_normal:
            if world.options.randomize_weapon_stats == RandomWeaponStats.option_consistent:
                if data.type not in saved_percents:
                    stat_percent = int(world.random.triangular(-50, 50))
                    saved_percents[data.type] = stat_percent
                else:
                    stat_percent = saved_percents[data.type] + world.random.randint(-5, 5)  # Add 5% + or - variance
            else:
                stat_percent = int(world.random.triangular(-50, 50))

            if stat_percent in range(-50, -35):
                name_mod = "--"
            elif stat_percent in range(-35, -20):
                name_mod = "-"
            elif stat_percent in range(19, 36):
                name_mod = "+"
            elif stat_percent in range(35, 51):
                name_mod = "++"

            data.atk = apply_num_as_percent(data.atk, stat_percent)

        if world.options.randomize_weapon_attribute != RandomWeaponAttributes.option_normal:
            if world.options.randomize_weapon_attribute == RandomWeaponAttributes.option_consistent:
                if data.type not in saved_elements:
                    chosen_element = world.random.choice(["Strike", "Stab", "Slash"])
                    saved_elements[data.type] = chosen_element
                    data.element = chosen_element
                else:
                    data.element = saved_elements[data.type]  # If the type was logged, use it
            else:
                data.element = world.random.choice(["Strike", "Stab", "Slash"])
            rolled_element = True

        if world.options.randomize_weapon_properties:
            chance = world.random.randint(0, 100)
            if chance < 15:  # 15% chance for a secondary element
                element = world.random.choice(sub_elements)
                rolled_subel = True
            else:
                element = "None"
            data.sub_element = element

            chance = world.random.randint(0, 100)
            if chance < 10:  # 10% chance for a mod
                possible_mods = modifier_list.copy()
                possible_mods.remove("None")
                if data.type in ["Greatsword", "Spear", "Hammer", "Axe", "Bear"] or weapon in [
                                 "RPG", "Nunchakus", "Valmanway", "Whip"]:
                    possible_mods.remove("Heavy")  # These weapons start heavy, so they can only roll light
                elif data.type == "Throwing":
                    possible_mods.remove("Heavy")  # Throwing weapons can't have either of these
                    possible_mods.remove("Light")
                else:
                    possible_mods.remove("Light")

                if weapon in ["Valmanway", "Nunchakus"] or data.type == "Throwing":
                    possible_mods.remove("Spectral")  # These weapons always have this property
                data.modifier = world.random.choice(possible_mods)
                rolled_mod = True
        if data.modifier == "Thorned":
            data.frames = data.frames // 2
        elif data.modifier == "Spectral":
            data.atk = data.atk // 2

        element_data = 0
        element_data |= element_flags[data.element]
        element_data |= element_flags[data.sub_element]
        address = base_address + (0x1C * id_num)
        rom.write_to_file(address + 0x0A, "arm9", bytearray([data.atk]))
        rom.write_to_file(address + 0x17, "arm9", bytearray([data.frames]))
        rom.write_to_file(address + 0x10, "arm9", struct.pack("I", element_data))
        rom.write_to_file(address + 0x09, "arm9", bytearray([modifier_list.index(data.modifier)]))
        if rolled_element:
            name = f"{element_abbreviations[data.element]}" + name
        if rolled_subel:
            name = f"{element_abbreviations[data.sub_element]}" + name

        if rolled_mod:
            name = name + mod_abbreviations[data.modifier]

        name = name + name_mod
        has_removed_space = False
        while calculate_text_width(name) > 98:
            if " " in name:
                name = name.replace(" ", "")
            elif " " in weapon and not has_removed_space:
                name = name.replace(weapon.split(" ")[1], "")
                has_removed_space = True
            elif "a" in name:
                name = name.replace("a", "")
            elif "e" in name:
                name = name.replace("e", "")
            elif "i" in name:
                name = name.replace("i", "")
            elif "o" in name:
                name = name.replace("o", "")
            elif "u" in name:
                name = name.replace("u", "")
            else:
                name = name.replace(name[len(name) // 2], "")  # Chop off a letter in the middle
                print(name)

        encoded_name = [0x01, 0x00]
        encoded_name += text_encoder(name)
        encoded_name += [0xEA, 0x01]
        rom.write_to_file(text_address, "overlay_0", bytearray(encoded_name))
        rom.write_to_file(0x0222F438 + (4 * id_num), "overlay_0", struct.pack("I", text_address))
        text_address += len(encoded_name)  # Update the address for the next iteration


def apply_weapon_properties(rom):
    for i in range(0x4F):
        address = base_address + (0x1C * i)
        mod = rom.read_from_file(address + 0x09, "arm9", 1)[0]
        properties = struct.unpack("H", rom.read_from_file(address + 0x18, "arm9", 2))[0]
        if mod == 1:  # Heavy
            properties |= 0x01
        elif mod == 2:  # Light
            properties &= 0xFE
        elif mod == 4:  # Spectral
            properties |= 0x0248
        rom.write_to_file(address + 0x18, "arm9", struct.pack("H", properties))
        rom.write_to_file(address + 0x09, "arm9", bytearray([0x00]))  # Zero out the property byte


def apply_num_as_percent(base, factor):
    percent = 100 + factor
    value = int((percent / 100) * base)
    return value
