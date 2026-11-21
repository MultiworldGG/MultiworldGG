from ...common import UintField, StaticPointer
from ...common_types import CharacterDataFlag3, CharacterEntryFlag2
from ...type_aliases import TCSContext
from ....items import CHARACTERS_AND_VEHICLES_BY_NAME
from ....constants import CharacterAbility
from ....data.characters import Character


P_C_DATA_LIST = StaticPointer(0x93b294)
UNKNOWN_LOADED_CHARACTER_DATA_SIZE = 0x4c
# UnknownLoadedCharacterData.data_flag3
CHARACTER_DATA_FLAG_3 = UintField(0x4)

P_GC_DATA_LIST = StaticPointer(0x93b2a4)
CHARACTER_ENTRY_SIZE = 0x120
# CharacterEntry.UnknownFlag2
CHARACTER_ENTRY_FLAG_2 = UintField(0x90)


# IMPORTANT: TCS appears to have a limit on the number of unique character animations that can be loaded at any time.
#   Forcing too many characters with unique animations can cause the animations for some characters to not load. This
#   more commonly happens when an Area has many "resident" characters that are always included in the Free Play roster
#   when they are unlocked by the player, in addition to a large number of characters picked due to extra character
#   categories being defined.


async def set_ig88_and_4lom_as_protocol_droids(ctx: TCSContext):
    # Give 4-LOM and IG-88 the Protocol flag so that if the player has no Protocol Droid, but does have 4-LOM or
    # IG-88, the game will pick 4-LOM or IG-88 for the Free Play character selection.
    # While 4-LOM and IG-88 can also use Astromech panels, the Astromech flag (0x40) also tells the game that
    # the characters can hover, and can traverse Dagobah's swamps, which neither 4-LOM nor IG-88 can do, so they
    # should not be given the Astromech flag.
    # Character data is loaded once when the game starts, so the changes made here are permanent until the game
    # is restarted.
    array = P_C_DATA_LIST.to_array(ctx, UNKNOWN_LOADED_CHARACTER_DATA_SIZE)
    for character in (Character.IG_88, Character.FOUR_LOM):
        addr_character_data = array[character]
        character_data_flag_3 = CHARACTER_DATA_FLAG_3.get(ctx, addr_character_data)
        new_flag = character_data_flag_3 | CharacterDataFlag3.PROTOCOL.value
        CHARACTER_DATA_FLAG_3.set(ctx, addr_character_data, new_flag)


async def set_astromech_panel_users_as_tightrope_walk(ctx: TCSContext):
    # Give astromech panel users the TIGHTROPE_WALK flag, which a custom category is added for, so that a character that
    # can use astromech panels is always picked, if one is unlocked.
    array = P_GC_DATA_LIST.to_array(ctx, CHARACTER_ENTRY_SIZE)
    for character_data in CHARACTERS_AND_VEHICLES_BY_NAME.values():
        if CharacterAbility.ASTROMECH_PANEL in character_data.abilities:
            addr_character_entry = array[character_data.character]
            character_entry_flag = CHARACTER_ENTRY_FLAG_2.get(ctx, addr_character_entry)
            new_flag = character_entry_flag | CharacterEntryFlag2.TIGHTROPE_WALK.value
            CHARACTER_ENTRY_FLAG_2.set(ctx, addr_character_entry, new_flag)


async def set_droideka_as_tightrope_tilt(ctx: TCSContext):
    # Give droideka the TIGHTROPE_TILT flag, which a custom category is added for, so that Droideka is always picked if
    # unlocked.
    array = P_GC_DATA_LIST.to_array(ctx, CHARACTER_ENTRY_SIZE)
    addr_character_entry = array[Character.DROIDEKA]
    character_entry_flag = CHARACTER_ENTRY_FLAG_2.get(ctx, addr_character_entry)
    new_flag = character_entry_flag | CharacterEntryFlag2.TIGHTROPE_TILT.value
    CHARACTER_ENTRY_FLAG_2.set(ctx, addr_character_entry, new_flag)


async def set_can_remove_droideka_shields_characters_as_got_batarang(ctx: TCSContext):
    # Give characters that can remove droideka shields the GOT_BATARANG flag, which a custom category is added for,
    # so that a character that can remove droideka shields is always picked, if one is unlocked.
    zap_bounty_or_jedi = CharacterAbility.WEAPON_ZAPPER | CharacterAbility.BOUNTY_HUNTER | CharacterAbility.JEDI
    can_remove_droideka_shields = [
        character_data.character for character_data in CHARACTERS_AND_VEHICLES_BY_NAME.values()
        if character_data.abilities & zap_bounty_or_jedi != 0
    ]
    # Droideka bolts also damage Droideka shields.
    can_remove_droideka_shields.append(Character.DROIDEKA)

    array = P_GC_DATA_LIST.to_array(ctx, CHARACTER_ENTRY_SIZE)
    for character_index in can_remove_droideka_shields:
        addr_character_entry = array[character_index]
        character_entry_flag = CHARACTER_ENTRY_FLAG_2.get(ctx, addr_character_entry)
        new_flag = character_entry_flag | CharacterEntryFlag2.GOT_BATARANG.value
        CHARACTER_ENTRY_FLAG_2.set(ctx, addr_character_entry, new_flag)


async def set_yodas_as_super_strength(ctx: TCSContext):
    # Give Yoda characters the HAS_SUPER_STRENGTH flag, which a custom category is added for,
    # so that a Yoda character is always picked, if one is unlocked.
    array = P_GC_DATA_LIST.to_array(ctx, CHARACTER_ENTRY_SIZE)
    for character in (Character.YODA, Character.YODA_GHOST):
        addr_character_entry = array[character]
        character_entry_flag = CHARACTER_ENTRY_FLAG_2.get(ctx, addr_character_entry)
        new_flag = character_entry_flag | CharacterEntryFlag2.HAS_SUPER_STRENGTH.value
        CHARACTER_ENTRY_FLAG_2.set(ctx, addr_character_entry, new_flag)
