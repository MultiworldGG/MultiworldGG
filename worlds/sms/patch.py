import random
from importlib.resources import read_binary

from gclib.gcm import GCM
from gclib.dol import DOL, DOLSection

from .Helper_Functions import StringByteFunction as sbf

CUSTOM_CODE_OFFSET_START = 0x3F00A0
SMS_PLAYER_NAME_BYTE_LENGTH = 64

# class SMSTest:

def update_dol_offsets(gcm: GCM, dol: DOL, seed: str, slot_name: str, starting_nozzle: int, level_access: bool,
    coin_shines: bool, blue_rando: int, all_shines_selectable: int) -> (GCM, DOL):

    random.seed(seed)

    dol_data = gcm.read_file_data("sys/main.dol")
    dol.read(dol_data)

    change_nozzle_values = "481ad8a4"
    fmv_values1 = "38600001"
    fmv_values2 = "38600001"
    blue_visual_fix_values = "4e800020"
    skip_blue_save_values = "60000000"
    nozzle_rando_value1 = "481c7ecc"
    nozzle_rando_value2 = "481aeaa4"
    nozzle_rando_value3 = "481aeae0"
    nozzle_rando_value4 = "4814e6cc"
    plaza_darkness1_value = "4800006C"
    plaza_darkness2_value = "4E800020"
    all_episodes_unlocked_value = "38000008"

    # Changing Game ID and Game Name from boot.bin
    bin_data = gcm.read_file_data("sys/boot.bin")
    bin_data.seek(0x04)
    bin_data.write(bytes.fromhex("4150"))
    bin_data.seek(0x34)
    bin_data.write(bytes.fromhex("20417263686970656C61676F"))
    gcm.changed_files["sys/boot.bin"] = bin_data

    # ChangeNozzle offset to check if we own the nozzles
    change_nozzle_offset = dol.convert_address_to_offset(0x8026a164)

    dol.data.seek(change_nozzle_offset)
    dol.data.write(bytes.fromhex(change_nozzle_values))

    # FMV Offset patching to skip cutscenes in game
    fmv_offset1 = dol.convert_address_to_offset(0x802B5EF4)
    fmv_offset2 = dol.convert_address_to_offset(0x802B5E8C)

    dol.data.seek(fmv_offset1)
    dol.data.write(bytes.fromhex(fmv_values1))
    dol.data.seek(fmv_offset2)
    dol.data.write(bytes.fromhex(fmv_values2))

    # Blue Coin Visual Bug Fix (No HUD Glitches upon picking up blue coins)
    blue_visual_fix_offset = dol.convert_address_to_offset(0x8014757c)

    dol.data.seek(blue_visual_fix_offset)
    dol.data.write(bytes.fromhex(blue_visual_fix_values))

    # Skip Blue Coin Save Prompt
    skip_blue_save_offset = dol.convert_address_to_offset(0x8029A73C)

    dol.data.seek(skip_blue_save_offset)
    dol.data.write(bytes.fromhex(skip_blue_save_values))

    # Replace section two with our own custom section, which is about 1000 hex bytes long.
    new_dol_size = 0x2048
    new_dol_sect = DOLSection(CUSTOM_CODE_OFFSET_START, 0x80417800, new_dol_size)
    dol.sections[2] = new_dol_sect

    # Append the extra bytes we expect, to ensure we can write to them in memory.
    dol.data.seek(len(dol.data.getvalue()))
    blank_data = b"\x00" * new_dol_size
    dol.data.write(blank_data)

    custom_dol_code = read_binary(__name__, "SMS_custom_code.smsco")
    # print(f"{custom_dol_code}")

    dol.data.seek(CUSTOM_CODE_OFFSET_START)
    dol.data.write(custom_dol_code)

    # Fludd Nozzle Rando Codes
    fludd1_offset = dol.convert_address_to_offset(0x8024F934)
    fludd2_offset = dol.convert_address_to_offset(0x80268DD4)
    fludd3_offset = dol.convert_address_to_offset(0x80268E18)
    fludd4_offset = dol.convert_address_to_offset(0x802C924C)

    dol.data.seek(fludd1_offset)
    dol.data.write(bytes.fromhex(nozzle_rando_value1))

    dol.data.seek(fludd2_offset)
    dol.data.write(bytes.fromhex(nozzle_rando_value2))

    dol.data.seek(fludd3_offset)
    dol.data.write(bytes.fromhex(nozzle_rando_value3))

    dol.data.seek(fludd4_offset)
    dol.data.write(bytes.fromhex(nozzle_rando_value4))

    # Offset and branch rewrite for Nozzle Enforcement in TWaterGun::init()
    twatergun_init_offset = dol.convert_address_to_offset(0x8026aa44)

    dol.data.seek(twatergun_init_offset)
    dol.data.write(bytes.fromhex("481ad03c"))

    # Offset to change Yoshi Egg Spawn Flag
    delfino_yoshi_egg_offset = dol.convert_address_to_offset(0x801bbf84)
    others_yoshi_egg_offset = dol.convert_address_to_offset(0x801bbfb0)

    dol.data.seek(delfino_yoshi_egg_offset)
    dol.data.write(bytes.fromhex("4825bb65"))
    dol.data.seek(others_yoshi_egg_offset)
    dol.data.write(bytes.fromhex("4825bb39"))

    # Player Slot Name Writing
    slot_name_offset = dol.convert_address_to_offset(0x80418000)

    dol.data.seek(slot_name_offset)
    dol.data.write(sbf.string_to_bytes(slot_name, SMS_PLAYER_NAME_BYTE_LENGTH))

    # Removes plaza darkness so game won't go full dark mode above 120 shines
    plaza_darkness1_offset = dol.convert_address_to_offset(0x8017D1E0)
    plaza_darkness2_offset = dol.convert_address_to_offset(0x8027C67C)

    dol.data.seek(plaza_darkness1_offset)
    dol.data.write(bytes.fromhex(plaza_darkness1_value))
    dol.data.seek(plaza_darkness2_offset)
    dol.data.write(bytes.fromhex(plaza_darkness2_value))

    # Unlocks all episodes in Shine Select screen
    if all_shines_selectable:
        all_episodes_unlocked_offset1 = dol.convert_address_to_offset(0x80174e60)
        all_episodes_unlocked_offset2 = dol.convert_address_to_offset(0x80174e74)

        # Changes branch to jump to 0x80174E74 so all Shines are loaded on Episode Select properly
        dol.data.seek(all_episodes_unlocked_offset1)
        dol.data.write(bytes.fromhex("41820015"))

        dol.data.seek(all_episodes_unlocked_offset2)
        dol.data.write(bytes.fromhex(all_episodes_unlocked_value))

    # If Ticketed mode, set Noki requirement to 0 so it opens whenever ticket is acquired
    if level_access is True:
        noki_entrance_requirement = dol.convert_address_to_offset(0x802b79e3)

        dol.data.seek(noki_entrance_requirement)
        dol.data.write(bytes.fromhex("00"))

    # If starting Fluddless, changes flags to skip Airstrip and start in post-statue plaza
    if starting_nozzle == 2:
        boot_to_plaza_offset = dol.convert_address_to_offset(0x80164E32)
        dol.data.seek(boot_to_plaza_offset)
        # Is there a way to write only a half-word?
        # dol.data.write_u16(bytes.fromhex("0208"))
        dol.data.write(bytes.fromhex("020838A0"))

    # QOL shines no longer boot out of stage


    # for section in dol.sections:
    #     print(f"Section at 0x{section.offset:X} (0x{section.address:X}) size 0x{section.size:X}")

    dol.save_changes()
    gcm.changed_files["sys/main.dol"] = dol.data

    return gcm, dol
