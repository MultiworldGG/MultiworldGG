"""This module provides an RAC3 interface to control the game"""
import time
from collections.abc import Iterable
from dataclasses import dataclass
from math import isclose
from random import choice, randint
from typing import Any

from typing_extensions import deprecated

from BaseClasses import ItemClassification
from CommonClient import logger
from Utils import __version__
from worlds.rac3.client.general_interface import GameInterface
from worlds.rac3.client.notification import RAC3NOTIFICATION
from worlds.rac3.client.string_table import StringTable
from worlds.rac3.client.string_table_entry import StringTableEntry
from worlds.rac3.client.texthelper import (TEXT_BYTE_TO_EXPECTED_WIDTH, VENDOR_ITEM_NAME_TEXT_IDS,
                                           format_planet_location_counts, remove_accents)
from worlds.rac3.client.vendor_name_patch import VendorNamePatch
from worlds.rac3.constants.action_type import ACTION_TYPE_NAMES, RAC3ACTIONTYPE
from worlds.rac3.constants.check_type import CHECKTYPE
from worlds.rac3.constants.cutscene_flag import RAC3CUTSCENEFLAG
from worlds.rac3.constants.data.address import SAVE_DATA
from worlds.rac3.constants.data.item import (armor_data, cheat_data, equipable_data, filler_magnitude_data, gadget_data,
                                             infobot_data, ITEM_FROM_AP_CODE, ITEM_NAME_FROM_ID, item_to_status,
                                             non_prog_weapon_data, PROG_TO_NAME_DICT, quick_selectable_data,
                                             RAC3_ITEM_DATA_TABLE, trap_magnitude_data, vidcomic_data)
from worlds.rac3.constants.data.location import (LOCATION_FROM_AP_CODE, LOCATION_TO_INFOBOT_FLAG,
                                                 RAC3_LOCATION_DATA_TABLE, RAC3LOCATIONDATA, REGION_TO_INFOBOT_LOCATION)
from worlds.rac3.constants.data.position import RAC3POSITIONDATA
from worlds.rac3.constants.data.region import INFOBOT_FROM_PLANET, PLANET_FROM_INFOBOT, RAC3_REGION_DATA_TABLE
from worlds.rac3.constants.data.ship_slot import RAC3_SHIP_DATA_TABLE
from worlds.rac3.constants.data.shortcut import RAC3_SHORTCUT_DATA_TABLE
from worlds.rac3.constants.data.status import RAC3_STATUS_DATA_TABLE
from worlds.rac3.constants.data.vendorslot import (ARMOR_VENDOR_INVENTORY, ARMOR_VENDOR_LOCATION_TO_ITEM,
                                                   ARMOR_VENDOR_LOCATION_TO_UNLOCK_REGION,
                                                   ITEM_TO_ARMOR_VENDOR_LOCATION, ITEM_TO_WEAPON_VENDOR_LOCATION,
                                                   MEGACORP_WEAPONS, RAC3ARMORVENDORSLOTDATA, RAC3SHIPVENDORSLOTDATA,
                                                   RAC3SKINVENDORSLOTDATA, RAC3VENDORSLOTDATA, RAC3WEAPONVENDORSLOTDATA,
                                                   SHIP_VENDOR_INVENTORY, WEAPON_VENDOR_LOCATION_TO_ITEM,
                                                   WEAPON_VENDOR_LOCATION_TO_UNLOCK_REGION)
from worlds.rac3.constants.deaths import CLANK_DEATH_FROM_ACTION, DEATH_FROM_ACTION
from worlds.rac3.constants.galactic_map import (COMMON_GROUPS, DEFAULT_GROUPS, GADGET_PICKUP_LOCATIONS,
                                                GAUNTLET_LOCATIONS, GROUP_TAGS, MAP_LOCATION_REGION_OVERRIDES,
                                                RAC3GALACTICMAP, SEPARATE_GROUPS, STORY_LOCATIONS, VENDOR_LOCATIONS)
from worlds.rac3.constants.game_state import RAC3GAMESTATE
from worlds.rac3.constants.input import RAC3INPUT
from worlds.rac3.constants.instruction import (ORIGINAL_INSTRUCTIONS, PATCH_INSTRUCTION_TO_GAME_IDS,
                                               PATCH_INSTRUCTION_TO_NAME, PATCH_INSTRUCTION_TO_PLANET,
                                               PATCHED_INSTRUCTIONS, RAC3INSTRUCTION)
from worlds.rac3.constants.item_tags import RAC3ITEMTAG
from worlds.rac3.constants.items import QUICK_SELECT_LIST, RAC3ITEM, UPGRADE_DICT
from worlds.rac3.constants.locations.challenge_description import (
    GAUNTLET_DESCRIPTION, GAUNTLET_DESCRIPTORS, NATION_CHALLENGE_SIZE,
    NATION_CHALLENGE_TABLE, VR_TRAINING_DESCRIPTION, VR_TRAINING_NAME, VR_TRAINING_NAME_ADDRESS,
)
from worlds.rac3.constants.locations.general import MISSION_COUNTS, RAC3LOCATION, RANGER_MISSION_CHAINS
from worlds.rac3.constants.locations.groups import RAC3LOCATIONGROUP
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.locations.trophies import RAC3TROPHY
from worlds.rac3.constants.messages.box_format import THEME_ID_TO_THEME_COLORS
from worlds.rac3.constants.messages.box_theme import RAC3BOXTHEME
from worlds.rac3.constants.messages.messagebox import RAC3MESSAGEBOX
from worlds.rac3.constants.messages.text_format import CLASSIFICATION_TO_COLOR, FORMAT_NAME_TO_BYTE
from worlds.rac3.constants.messages.text_strings import RAC3TEXTFORMATSTRING
from worlds.rac3.constants.moby_flag import (BOLT_CRANK_TO_REGION, HACKER_PUZZLE_TO_DOOR_IDS, HACKER_PUZZLE_TO_REGION,
                                             REFRACTOR_PUZZLE_TO_REGION, TYHRRANOID_PUZZLE_TO_REGION)
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.player_action import PLAYER_ACTION_NAMES, RAC3PLAYERACTION
from worlds.rac3.constants.player_type import ONE_HP_CHALLENGE_CHARACTERS, PLAYER_TYPE_TO_NAME, RAC3PLAYERTYPE
from worlds.rac3.constants.progress_flag import HALO_JUMP_TO_REGION, RAC3PROGRESSFLAG
from worlds.rac3.constants.region import (INVALID_PLANETS, PLANET_LOAD_OFFSET, PLANET_NAME_FROM_ID,
                                          PLANET_VENDOR_OFFSET, PLANETS_WITH_BOLT_CRANK_PUZZLES,
                                          PLANETS_WITH_HACKER_PUZZLES,
                                          PLANETS_WITH_REFRACTOR_PUZZLES, PLANETS_WITH_TYHRRANOID_PUZZLES, RAC3REGION,
                                          REGION_TO_HACKER_DOOR_COUNT)
from worlds.rac3.constants.ship_slot import RAC3SHIPSLOT, SHIP_SLOTS
from worlds.rac3.constants.shortcuts import RAC3SHORTCUTS, SHORTCUTS
from worlds.rac3.constants.speedups import RAC3SPEEDUPS, SPEEDUPS
from worlds.rac3.constants.status import RAC3STATUS, status_on_off
from worlds.rac3.constants.vendors.name import RAC3VENDORNAME, VENDOR_TYPES
from worlds.rac3.constants.vendors.type import RAC3VENDORTYPE
from worlds.rac3.constants.vendors.vendor import RAC3SHIPVENDOR, RAC3VENDOR, RAC3WEAPONVENDOR, VENDORTYPE_TO_SLOT_SIZE
from worlds.rac3.constants.version import (GAME_ID_TO_OFFSET, GAME_ID_TO_VERSION, jp_convert_address,
                                           PAL_SHIFTED_PLANETS, RAC3VERSION)
from worlds.rac3.constants.weapon_mod import WEAPON_MOD_TO_WEAPON, WEAPON_TO_WEAPON_MODPACK, WEAPONMOD
from worlds.rac3.constants.wrench import RAC3WRENCH
from worlds.rac3.locations import get_challenge_locations, get_completion_location_names


class Rac3Interface(GameInterface):
    """Handles reading and modifying the game memory"""

    @dataclass
    class Options:
        """Data structure for storing options"""
        start_inventory_from_pool: dict[str, int]
        starting_weapons: dict[str, int]
        bolt_and_xp_multiplier: int
        progressive_weapons: int
        weapon_mods: int
        progressive_wrench: int
        armor_upgrade: int
        skill_points: int
        trophies: int
        titanium_bolts: int
        nanotech_milestones: int
        exclude_locations: set[str]
        generation_behavior: int
        deathlink: int
        ship_nose: int
        ship_wings: int
        ship_skin: int
        player_skin: int
        traps_enabled: int
        trap_weight: dict[str, int]
        trap_magnitude: dict[str, int]
        filler_magnitude: dict[str, int]
        rangers: int
        arena: int
        vidcomics: int
        vr_challenges: int
        sewer_crystals: int
        sewer_limitation: int
        nanotech_limitation: int
        weapon_vendors: int
        filler_weight: dict[str, int]
        one_hp_challenge: dict[str, int]
        clank_options: int
        ship_vendor: int
        armor_vendor: int
        scout_vendors: dict[str, int]
        shortcuts: dict[str, int]
        speedups: dict[str, int]
        ngplus_items: int
        ngplus_vendors: int
        ngplus_start: int
        helpdesk: int
        weapon_level_locations: int
        vendor_access: int
        bonus_vidcomic_health: int
        vidcomic_health_upgrade_locations: int
        deathlink_behavior: int
        lock_cc: int
        goal_bio: int
        goal_nef: int
        goal_nano: int
        goal_crystal: int
        goal_tbolts: int
        goal_skillpoints: int
        goal_qwark: int
        goal_museum: int
        goal_planets: int
        goal_completion: int
        goal_boss_qwark: int
        goal_boss_two: int
        goal_boss_noid: int
        goal_boss_warship: int
        goal_boss_scorpio: int
        goal_boss_talos: int
        goal_boss_gears: int
        goal_boss_klunk: int

    UnlockItem: dict[str, int] = {}
    options = Options
    bolt_and_xp_multiplier_value: int = 0
    self_respawning: bool = False
    reloading_handled: bool = False
    is_reloading: int = 0
    timers: dict[str, float] = {}
    planet: str = RAC3REGION.GALAXY
    new_planet: bool = True
    transporter_fixed: bool = False
    player_type: str = RAC3PLAYERTYPE.RATCHET
    player_pos: RAC3POSITIONDATA
    vehicle: int = 0
    action: int = RAC3PLAYERACTION.IDLE
    action_type: int = RAC3ACTIONTYPE.STATIONARY
    prev_action: int = RAC3PLAYERACTION.IDLE
    pause_menu: bool = False
    pausing_game_state: bool = False
    game_state_value: RAC3GAMESTATE = RAC3GAMESTATE.INVALID
    inputs: int = RAC3INPUT.NOTHING
    health: int = 100
    max_health: int = 10
    end_game: bool = False
    crystals_current: int = 0
    crystals_traded: int = 0
    skillpoints: int = 0
    qwarktastic: int = 0
    museum_unlocked: bool = False
    museum_visited: bool = False
    boss_qwark: int = 0
    boss_two: int = 0
    boss_noid: int = 0
    boss_warship: int = 0
    boss_scorpio: int = 0
    boss_talos: int = 0
    boss_gears: int = 0
    boss_klunk: int = 0
    boss_nef: int = 0
    boss_bio: int = 0
    total_locations: int = 0
    pre_end: int = 0
    main_menu: bool = False
    ratchet_moby: int = 0
    between_planets: bool = False
    short_pause: bool = False
    long_pause: bool = False
    ryno: int = 5
    death_count: int = 0
    last_death_count: int = 0
    last_death_state: int = 0
    has_died: bool = False
    died_in_vehicle: bool = False
    died_from_softlock: bool = False
    inside_hacker_puzzle: bool = False
    notification_queue: list[RAC3NOTIFICATION] = []
    notification_time: float = 0
    notification_paused_remaining: float = 0
    notification_merge_count: int = 1
    message_display: bool = False
    ship_slot_limit: int = 0
    pda_vendor: int = 0
    last_in_vehicle_time: float = 0.0
    last_in_vendor_time: float = 0.0
    deathlink_grace_period: float = 0.0
    gadget_grace_period: float = 0.0
    nanotech_exp: int = 0
    homewarping: bool = False
    checked_locations: set[str] = set()
    collected_tbolt_locations: set[str] = set()
    clank_disabled: bool = False
    clank_disabled_trap: bool = False
    visited_planets: set[str] = set()
    weapon_vendor_items: list[str] = []
    armor_vendor_items: list[str] = []
    omega_weapon_vendors_items: list[str] = []
    vendor_type: RAC3VENDORTYPE | None = None
    vendor_string_pointers: dict[str, int] = {}
    challenge_string_pointers: dict[str, int] = {}
    galactic_map_text_pointer_list: int = 0
    vendor_cursor_pos: int = 0
    string_table: StringTable | None = None
    string_entries: dict[int, int] = {}
    vendor_name_table: StringTable | None = None
    vendor_name_patches: dict[int, VendorNamePatch] = {}
    vendor_name_restore_pending: bool = False
    tyhrra_dropship: bool = False
    tyhrra_intro: int = 0
    metro_dropship: int = 0  # 0 is ready, 1 owns the temporary bit, 2 is done for this pause.
    holo_teleport: int = 0
    holo_final_door: int = 0
    holo_door: int = 0
    hacker_door_addresses: dict[int, int] = {}
    opened_the_hacker_doors: bool = False
    opened_the_tyhrranoid_doors: bool = False
    opened_the_refractor_doors: bool = False
    turned_the_bolt_cranks: bool = False
    weapon_levels: dict[str, int] = {}
    delayed_weapon_levelups: list[str] = []
    delayed_debt_trap_count: int = 0
    stored_fillers: dict[str, int] = {}
    initial_fillers: dict[str, int] = {}
    last_hovered_weapon: str = ""
    track_deaths: bool = False
    equipped_item: int = 0
    held_item: int = 0
    last_used_0: int = 0
    last_used_1: int = 0
    last_used_2: int = 0
    last_used_3: int = 0
    last_used_4: int = 0
    last_used_5: int = 0
    weapon_demo: int = 0

    def __init__(self):
        super().__init__()  # GameInterfaceの初期化

    #####################
    # Inherit functions #
    #####################

    def _read8(self, address: int, *, should_convert: bool = True) -> int:
        _address = self.address_convert(address) if should_convert else address
        pending: int | None = self.write_batcher.get((_address, self.DataType.INT8))
        if pending is not None:
            return pending
        return super()._read8(_address)

    def _read16(self, address: int, *, should_convert: bool = True) -> int:
        _address = self.address_convert(address) if should_convert else address
        pending: int | None = self.write_batcher.get((_address, self.DataType.INT16))
        if pending is not None:
            return pending
        return super()._read16(_address)

    def _read32(self, address: int, *, should_convert: bool = True) -> int:
        _address = self.address_convert(address) if should_convert else address
        pending: int | None = self.write_batcher.get((_address, self.DataType.INT32))
        if pending is not None:
            return pending
        return super()._read32(_address)

    def _read8_batch(self, addresses: list[int], *, should_convert: bool = True) -> list[int]:
        if should_convert:
            addresses = [self.address_convert(address) for address in addresses]
        return super()._read8_batch(addresses)

    def _read16_batch(self, addresses: list[int], *, should_convert: bool = True) -> list[int]:
        if should_convert:
            addresses = [self.address_convert(address) for address in addresses]
        return super()._read16_batch(addresses)

    def _read32_batch(self, addresses: list[int], *, should_convert: bool = True) -> list[int]:
        if should_convert:
            addresses = [self.address_convert(address) for address in addresses]
        return super()._read32_batch(addresses)

    def _read_bytes(self, address: int, n: int, *, should_convert: bool = True) -> bytes:
        if should_convert:
            address = self.address_convert(address)
        return super()._read_bytes(address, n)

    def _read_float(self, address: int, *, should_convert: bool = True) -> float:
        if should_convert:
            address = self.address_convert(address)
        return super()._read_float(address)

    def _read_string(self, address: int, n: int, *, should_convert: bool = True) -> str:
        if should_convert:
            address = self.address_convert(address)
        return super()._read_string(address, n)

    def _write8(self, address: int, value: int, *, should_convert: bool = True):
        if should_convert:
            address = self.address_convert(address)
        self.write_batcher[(address, self.DataType.INT8)] = value

    def _write8_skip_cache(self, address: int, value: int, *, should_convert: bool = True):
        if should_convert:
            address = self.address_convert(address)
        return super()._write8(address, value)

    def _write16_skip_cache(self, address: int, value: int, *, should_convert: bool = True):
        if should_convert:
            address = self.address_convert(address)
        return super()._write16(address, value)

    def _write32_skip_cache(self, address: int, value: int, *, should_convert: bool = True):
        if should_convert:
            address = self.address_convert(address)
        return super()._write32(address, value)

    def _write16(self, address: int, value: int, *, should_convert: bool = True):
        if should_convert:
            address = self.address_convert(address)
        self.write_batcher[(address, self.DataType.INT16)] = value

    def _write32(self, address: int, value: int, *, should_convert: bool = True):
        if should_convert:
            address = self.address_convert(address)
        self.write_batcher[(address, self.DataType.INT32)] = value

    def _write_bytes(self, address: int, value: bytes, *, should_convert: bool = True):
        if should_convert:
            address = self.address_convert(address)
        self.write_batcher[(address, self.DataType.BYTES)] = value

    def _write_float(self, address: int, value: float, *, should_convert: bool = True):
        if should_convert:
            address = self.address_convert(address)
        self.write_batcher[(address, self.DataType.FLOAT)] = value

    def _write_string(self, address: int, value: str, *, should_convert: bool = True):
        if should_convert:
            address = self.address_convert(address)
        self.write_batcher[(address, self.DataType.STRING)] = value

    def _read_bits(self, address: int, *, should_convert: bool = True) -> set[int]:
        value = self._read8(address, should_convert=should_convert)
        bits = self.value_to_bits(value)
        return bits

    def _read_flag(self, check: tuple[int, int], *, should_convert: bool = True) -> bool:
        return check[1] in self._read_bits(check[0], should_convert=should_convert)

    def _write_bits(self, data: tuple[int, set[int] | int], *, should_convert: bool = True):
        address, value = data
        _value: set[int] = {value} if isinstance(value, int) else value
        bits: set[int] = self._read_bits(address, should_convert=should_convert)
        if _value.issubset(bits):
            return
        bits |= _value
        write = self.bits_to_value(bits)
        self._write8(address, write, should_convert=should_convert)
        return

    def _unwrite_bits(self, data: tuple[int, set[int] | int], *, should_convert: bool = True):
        address, value = data
        _value: set[int] = {value} if isinstance(value, int) else value
        bits: set[int] = self._read_bits(address, should_convert=should_convert)
        if _value.isdisjoint(bits):
            return
        bits -= _value
        write = self.bits_to_value(bits)
        self._write8(address, write, should_convert=should_convert)
        return

    def address_convert(self, address: int | str) -> int:
        """Convert a US address for the current planet to the active game version."""
        _addr = int(address, 0) if isinstance(address, str) else address
        if (0x001DC7C0 <= _addr <= 0x00300000
            and self.planet in PAL_SHIFTED_PLANETS
            and self.current_game == RAC3VERSION.EU_ID):
            _addr += GAME_ID_TO_OFFSET[RAC3VERSION.EU_ID]
        if self.current_game == RAC3VERSION.JP_ID:
            _addr = jp_convert_address(_addr, self.planet)

        return _addr

    ###############################
    # Called on Server Connection #
    ###############################

    def proc_option(self, slot_data: dict[str, Any]):
        """Process slot option data received when connecting to the server"""
        logger.debug(f"Processing options: {slot_data}")
        self.options.start_inventory_from_pool = slot_data[RAC3OPTION.START_INVENTORY_FROM_POOL]
        self.options.starting_weapons = slot_data[RAC3OPTION.STARTING_WEAPONS]
        self.options.bolt_and_xp_multiplier = slot_data[RAC3OPTION.BOLT_AND_XP_MULTIPLIER]
        self.options.progressive_weapons = slot_data[RAC3OPTION.PROGRESSIVE_WEAPONS]
        self.options.weapon_mods = slot_data[RAC3OPTION.WEAPON_MODS]
        self.options.progressive_wrench = slot_data[RAC3OPTION.PROGRESSIVE_WRENCH]
        self.options.armor_upgrade = slot_data[RAC3OPTION.ARMOR_UPGRADE]
        self.options.skill_points = slot_data[RAC3OPTION.SKILL_POINTS]
        self.options.trophies = slot_data[RAC3OPTION.TROPHIES]
        self.options.titanium_bolts = slot_data[RAC3OPTION.TITANIUM_BOLTS]
        self.options.nanotech_milestones = slot_data[RAC3OPTION.NANOTECH_MILESTONES]
        self.options.exclude_locations = slot_data[RAC3OPTION.EXCLUDE]
        self.options.deathlink = slot_data[RAC3OPTION.DEATHLINK]
        self.options.generation_behavior = slot_data[RAC3OPTION.GENERATION_BEHAVIOR]
        self.options.ship_nose = slot_data[RAC3OPTION.SHIP_NOSE]
        self.options.ship_wings = slot_data[RAC3OPTION.SHIP_WINGS]
        self.options.ship_skin = slot_data[RAC3OPTION.SHIP_SKIN]
        self.options.player_skin = slot_data[RAC3OPTION.PLAYER_SKIN]
        self.options.traps_enabled = slot_data[RAC3OPTION.ENABLE_TRAPS]
        self.options.trap_weight = slot_data[RAC3OPTION.TRAP_WEIGHT]
        self.options.trap_magnitude = slot_data[RAC3OPTION.TRAP_MAGNITUDE]
        self.options.filler_magnitude = slot_data[RAC3OPTION.FILLER_MAGNITUDE]
        self.options.rangers = slot_data[RAC3OPTION.RANGERS]
        self.options.arena = slot_data[RAC3OPTION.ARENA]
        self.options.vidcomics = slot_data[RAC3OPTION.VIDCOMICS]
        self.options.vr_challenges = slot_data[RAC3OPTION.VR_CHALLENGES]
        self.options.sewer_crystals = slot_data[RAC3OPTION.SEWER_CRYSTALS]
        self.options.sewer_limitation = slot_data[RAC3OPTION.SEWER_LIMITATION]
        self.options.nanotech_limitation = slot_data[RAC3OPTION.NANOTECH_LIMITATION]
        self.options.weapon_vendors = slot_data[RAC3OPTION.WEAPON_VENDORS]
        self.options.filler_weight = slot_data[RAC3OPTION.FILLER_WEIGHT]
        self.options.one_hp_challenge = slot_data[RAC3OPTION.ONE_HP_CHALLENGE]
        self.options.clank_options = slot_data[RAC3OPTION.CLANK_OPTIONS]
        self.options.ship_vendor = slot_data[RAC3OPTION.SHIP_VENDOR]
        self.options.armor_vendor = slot_data[RAC3OPTION.ARMOR_VENDOR]
        self.options.scout_vendors = slot_data[RAC3OPTION.SCOUT_VENDORS]
        self.options.shortcuts = slot_data[RAC3OPTION.SHORTCUTS]
        self.options.speedups = slot_data[RAC3OPTION.SPEEDUPS]
        self.options.ngplus_items = slot_data[RAC3OPTION.NGPLUS_ITEMS]
        self.options.ngplus_vendors = slot_data[RAC3OPTION.NGPLUS_VENDOR]
        self.options.ngplus_start = slot_data[RAC3OPTION.NGPLUS_START]
        self.options.helpdesk = slot_data[RAC3OPTION.HELP_DESK]
        self.options.weapon_level_locations = slot_data[RAC3OPTION.WEAPON_LEVEL_LOCATIONS]
        self.options.vendor_access = slot_data[RAC3OPTION.VENDOR_ACCESS]
        self.options.bonus_vidcomic_health = slot_data[RAC3OPTION.BONUS_VIDCOMIC_HEALTH]
        self.options.vidcomic_health_upgrade_locations = slot_data[RAC3OPTION.VIDCOMIC_HEALTH_UPGRADES]
        self.options.deathlink_behavior = slot_data[RAC3OPTION.DEATHLINK_BEHAVIOR]
        self.options.lock_cc = slot_data[RAC3OPTION.LOCK_CC]
        self.options.goal_bio = slot_data[RAC3OPTION.GOAL_BIO]
        self.options.goal_nef = slot_data[RAC3OPTION.GOAL_NEF]
        self.options.goal_nano = slot_data[RAC3OPTION.GOAL_NANO]
        self.options.goal_crystal = slot_data[RAC3OPTION.GOAL_CRYSTAL]
        self.options.goal_tbolts = slot_data[RAC3OPTION.GOAL_TBOLTS]
        self.options.goal_skillpoints = slot_data[RAC3OPTION.GOAL_SKILLPOINTS]
        self.options.goal_qwark = slot_data[RAC3OPTION.GOAL_QWARK]
        self.options.goal_museum = slot_data[RAC3OPTION.GOAL_MUSEUM]
        self.options.goal_planets = slot_data[RAC3OPTION.GOAL_PLANETS]
        self.options.goal_completion = slot_data[RAC3OPTION.GOAL_COMPLETION]
        self.options.goal_boss_qwark = slot_data[RAC3OPTION.GOAL_BOSS_QWARK]
        self.options.goal_boss_two = slot_data[RAC3OPTION.GOAL_BOSS_TWO]
        self.options.goal_boss_noid = slot_data[RAC3OPTION.GOAL_BOSS_NOID]
        self.options.goal_boss_warship = slot_data[RAC3OPTION.GOAL_BOSS_WARSHIP]
        self.options.goal_boss_scorpio = slot_data[RAC3OPTION.GOAL_BOSS_SCORPIO]
        self.options.goal_boss_talos = slot_data[RAC3OPTION.GOAL_BOSS_TALOS]
        self.options.goal_boss_gears = slot_data[RAC3OPTION.GOAL_BOSS_GEARS]
        self.options.goal_boss_klunk = slot_data[RAC3OPTION.GOAL_BOSS_KLUNK]
        self.total_locations = slot_data[RAC3OPTION.TOTAL_LOCATIONS]
        self.pre_end = slot_data[RAC3OPTION.PRE_END]
        for option, value in trap_magnitude_data.items():
            if option not in self.options.trap_magnitude.keys():
                self.options.trap_magnitude.update({option: value})
        for option, value in filler_magnitude_data.items():
            if option not in self.options.filler_magnitude.keys():
                self.options.filler_magnitude.update({option: value})
        for option in ONE_HP_CHALLENGE_CHARACTERS:
            if option not in self.options.one_hp_challenge.keys():
                self.options.one_hp_challenge.update({option: False})
        for option in VENDOR_TYPES:
            if option not in self.options.scout_vendors.keys():
                self.options.scout_vendors.update({option: False})
        for option in SHORTCUTS:
            if option not in self.options.shortcuts.keys():
                self.options.shortcuts.update({option: False})
        for option in SPEEDUPS:
            if option not in self.options.speedups.keys():
                self.options.speedups.update({option: False})

    ########################################
    # Called on Game and Server Connection #
    ########################################

    def init(self):
        """Initialise values once the game and server are both connected"""
        # Unlock state variables/ArmorUpgrade variable
        self.UnlockItem = dict.fromkeys(ITEM_FROM_AP_CODE.values(), 0)
        if self.UnlockItem is not None:
            self.UnlockItem.update({RAC3SHIPSLOT.SLOT_0: 0})
            logger.debug(f"UnlockItem dict:{self.UnlockItem.keys()}")

        # Proc options
        # Bolt and XPMultiplier
        self.bolt_and_xp_multiplier_value = int(self.options.bolt_and_xp_multiplier)
        # EnableWeaponLevelAsItem: if enabled, EXP disabler is running.

        self.weapon_levels = dict.fromkeys(non_prog_weapon_data.keys(), 1)

    def check_main_menu(self):
        """Check if the player is on the main menu, before starting the game"""
        if (self._read32(RAC3STATUS.MAIN_MENU) == 0xFFFFFFFF
            or (self._read32(RAC3STATUS.GAME_LAUNCHED) == 0 and self.current_game == RAC3VERSION.US_ID)):
            return True
        return False

    ##########################
    # Called on Loading File #
    ##########################

    def reset_tracked_progress(self) -> None:
        """Clear the cached goal and location progress for the active file."""
        self.end_game = False
        self.checked_locations.clear()
        self.collected_tbolt_locations.clear()
        self.visited_planets.clear()

    def reset_file(self):
        """Remove all items and progress on the current file, ready to be set based on current slot progress"""
        self.reset_tracked_progress()
        self.remove_all_items()
        self.undo_collections()

    def remove_all_items(self):
        """Remove all items from the player's inventory"""
        for item in self.UnlockItem.keys():
            self.UnlockItem[item] = 0
        for slot in SHIP_SLOTS:
            self._write8(RAC3_SHIP_DATA_TABLE[slot].SLOT_ADDRESS, 0)
        self.UnlockItem[RAC3ITEM.VELDIN] = 1
        # self.UnlockItem[RAC3ITEM.FLORANA] = 1
        # self.UnlockItem[RAC3ITEM.STARSHIP_PHOENIX] = 1
        # self.UnlockItem[RAC3ITEM.MUSEUM] = 1
        self.transporter_fixed = False
        self.timers.clear()
        self.gadget_cycler()
        self.planet_cycler()
        self.weapon_cycler()
        self.weapon_mod_cycler()
        self.vidcomic_cycler()
        self.armor_cycler()
        self.timer_cycler()
        self.weapon_exp_cycler()
        self.verify_quick_select_and_last_used()
        self.clank_cycler()
        self.cheat_cycler()
        self.notification_cycler()
        self.invalidate_string_table_cache()

    def undo_collections(self):
        """Unset flags in the game associated to randomizer locations"""
        checks: dict[int, set[int]] = {}
        for location in RAC3_LOCATION_DATA_TABLE.values():
            if RAC3TAG.SEWER in location.TAGS or RAC3TAG.NANOTECH in location.TAGS:
                continue
            # Unrandomized T-bolt pickups are kept in the save so they can count towards the goal.
            if RAC3TAG.T_BOLT in location.TAGS and not self.options.titanium_bolts:
                continue
            for check in location.CHECK_ADDRESS:
                if check.TYPE & CHECKTYPE.SIZE == CHECKTYPE.BIT:
                    checks.setdefault(check.ADDRESS, set()).add(check.VALUE)
        for bits in checks.items():
            self._unwrite_bits(bits)

    def important_items(self, item: int, us: str, location: int):
        """Runs when loading into game from the main menu to update the player with important items from the server,
        skips filler and trap items to not flood the player with bolts/xp"""
        if (RAC3ITEMTAG.FILLER in RAC3_ITEM_DATA_TABLE[ITEM_FROM_AP_CODE[item]].TAGS or RAC3ITEMTAG.TRAP in
            RAC3_ITEM_DATA_TABLE[ITEM_FROM_AP_CODE[item]].TAGS):
            return
        self.item_received(item, us, None, location)

    def filler_items(self, item: int):
        """Runs when loading into game from the main menu to update the player with filler items from the server"""
        if RAC3ITEMTAG.FILLER in RAC3_ITEM_DATA_TABLE[ITEM_FROM_AP_CODE[item]].TAGS:
            self.initial_fillers[ITEM_FROM_AP_CODE[item]] = self.initial_fillers.get(ITEM_FROM_AP_CODE[item], 0) + 1

    def process_offline_fillers(self, data_received: bool):
        """Process any filler items received while offline"""
        logger.debug(f"Initial filler items: {self.initial_fillers} and data received: {data_received}")
        if not data_received:
            return
        notification_message = ""
        for item, count in self.initial_fillers.items():
            stored_count = self.stored_fillers.get(item, 0)
            if count > stored_count:
                diff = count - stored_count
                logger.debug(f"Processing {diff} offline filler items for {item}")
                for _ in range(diff):
                    self.item_received(RAC3_ITEM_DATA_TABLE[item].AP_CODE, None, None, 0)
                notification_message += (f"Received {RAC3TEXTFORMATSTRING.GREEN}{diff}x {RAC3TEXTFORMATSTRING.WHITE}"
                                         f"{item} {RAC3TEXTFORMATSTRING.NORMAL}while offline\n")
            else:
                logger.debug(f"No new offline filler items for {item} (stored: {stored_count}, current: {count})")
        self.stored_fillers = self.initial_fillers.copy()
        if notification_message:
            self.enqueue_notification(notification_message.removesuffix("\n"), duration=5.0)

    def collect_locations(self, locations: set[str]) -> set[str]:
        """Record collected locations and restore the flags that can safely be set in game."""
        checks: dict[int, set[int]] = {}

        # Prevent softlocks by only collecting ranger mission flags in order
        # Stop at the first gap
        ranger_flags: set[tuple[int, int]] = set()
        for missions in RANGER_MISSION_CHAINS:
            restore_mission = True
            for mission in missions:
                restore_mission = restore_mission and mission in locations
                for check in RAC3_LOCATION_DATA_TABLE[mission].CHECK_ADDRESS:
                    if check.TYPE & CHECKTYPE.SIZE == CHECKTYPE.BIT:
                        ranger_flags.add((check.ADDRESS, check.VALUE))
                        if restore_mission:
                            checks.setdefault(check.ADDRESS, set()).add(check.VALUE)

        output: set[str] = set()
        for location in locations:
            self.checked_locations.add(location)
            output.add(location)
            loc_data: RAC3LOCATIONDATA = RAC3_LOCATION_DATA_TABLE[location]
            if RAC3TAG.NANOTECH in loc_data.TAGS or RAC3TAG.SEWER in loc_data.TAGS:
                continue
            for check in loc_data.CHECK_ADDRESS:
                if (check.TYPE & CHECKTYPE.SIZE == CHECKTYPE.BIT
                        and (check.ADDRESS, check.VALUE) not in ranger_flags):
                    checks.setdefault(check.ADDRESS, set()).add(check.VALUE)
        for bits in checks.items():
            self._write_bits(bits)
        return output

    def load_save(self, save: dict[int, tuple[int, int]]):
        """Set the player's current values based on the server's save-data"""
        if self.check_main_menu():
            return
        logger.debug(f"Save data: {save}")
        defaults: dict[int, tuple[int, int]] = {data.ADDRESS: (data.TYPE, data.VALUE) for data in SAVE_DATA}
        logger.debug(f"Default values: {defaults}")
        for address, data in save.items():
            # Skip writing default values or lingering dev testing values saved on the server
            default = defaults.get(address)
            if default is None or data == default:
                continue

            size, value = data
            match size:
                case CHECKTYPE.BYTE:
                    self._write8(address, value)
                case CHECKTYPE.SHORT:
                    self._write16(address, value)
                case CHECKTYPE.INT:
                    self._write32(address, value)

    def reset_death_count(self):
        """Update the tracked death count to the value in game"""
        self.death_count = self._read32(RAC3STATUS.DEATH_COUNT)
        self.last_death_count = self.death_count

    def add_cosmetics(self):
        """Apply the generated cosmetics to the current game"""
        self._write8(RAC3STATUS.SHIP_CONFIG, self.options.ship_nose + self.options.ship_wings)
        self._write8(RAC3STATUS.SHIP_SKIN, self.options.ship_skin)
        self._write8(RAC3STATUS.PLAYER_SKIN, self.options.player_skin)
        self._write8(RAC3STATUS.PLAYER_SKIN_2, self.options.player_skin)
        self._write32(RAC3STATUS.LOADED_SKIN, 0xFFFFFFFF)  # Invalidate cached skin

    def setup_challenge_mode(self):
        """Make the challenge mode popup not appear if starting in challenge mode"""
        if self.options.ngplus_start:
            self._write8(RAC3STATUS.SEEN_NGPLUS_POPUP, 1)

    def setup_code_cave(self, vendor_strings: dict[str, str], challenge_strings: dict[str, str]):
        """Pack vendor and challenge strings, then reserve the map's text buffers."""
        self.vendor_string_pointers = {}
        self.challenge_string_pointers = {}
        self.galactic_map_text_pointer_list = 0
        start = RAC3INSTRUCTION.CODECAVE_START + 0x10  # The first bytes hold armor purchase flags.
        data = bytearray()
        strings = {
            RAC3VENDOR.NO_ITEMS_AVAILABLE_LOC_KEY: RAC3VENDOR.NO_ITEMS_AVAILABLE_MSG,
            RAC3VENDOR.ALL_ITEMS_SOLD_OUT_LOC_KEY: RAC3VENDOR.ALL_ITEMS_SOLD_OUT_MSG,
            **vendor_strings,
            **challenge_strings,
        }
        packed_challenges: dict[bytes, int] = {}
        for key, string in strings.items():
            is_challenge = key in challenge_strings
            encoded, _ = self.format_color_string(string)
            encoded = encoded.rstrip(b"\x00") + b"\x00"
            if is_challenge and encoded in packed_challenges:
                self.challenge_string_pointers[key] = packed_challenges[encoded]
                continue
            address = start + len(data)
            data.extend(encoded)
            if is_challenge:
                pointer = self.address_convert(address)
                self.challenge_string_pointers[key] = pointer
                packed_challenges[encoded] = pointer
            else:
                self.vendor_string_pointers[key] = address
        pointer_list = (start + len(data) + 7) & ~7
        end = pointer_list + RAC3GALACTICMAP.TEXT_BUFFER_OFFSET + 2 * RAC3GALACTICMAP.TEXT_BUFFER_SIZE
        if end > RAC3INSTRUCTION.CODECAVE_END:
            logger.error("Vendor, challenge, and Galactic Map text exceeds the reserved code cave space.")
            self.vendor_string_pointers = {}
            self.challenge_string_pointers = {}
            return
        data.extend(bytes(end - start - len(data)))
        self._write_bytes(start, bytes(data))
        self.galactic_map_text_pointer_list = self.address_convert(pointer_list)

    def speedup_setup(self):
        """One time setup of speedup options when starting a new session"""
        if self.options.shortcuts.get(RAC3SHORTCUTS.HOLOSTAR_CLANK, False):
            self._write8(RAC3_REGION_DATA_TABLE[RAC3REGION.HOLOSTAR_STUDIOS_CLANK].VISIT_ADDRESS, 1)
        if self.options.speedups.get(RAC3SPEEDUPS.MISSIONS, False):
            self._write_bits(RAC3PROGRESSFLAG.ARIDIA_5TH_MISSION_COMPLETE)  # Aridia final mission access
            for loc, addr in MISSION_COUNTS.items():
                if RAC3_LOCATION_DATA_TABLE[loc].REGION not in [RAC3REGION.STARSHIP_PHOENIX,
                                                                RAC3REGION.ANNIHILATION_NATION]:
                    self._write8(addr, 1)

    def setup_settings(self):
        """Update in game settings based on the slot options"""
        self._write8(RAC3STATUS.HELP_DESK_VOICE, self.options.helpdesk)
        self._write8(RAC3STATUS.HELP_DESK_TEXT, self.options.helpdesk)
        # TODO: Add stuff like camera speed, normal/inverted controls, subtitles, etc.

    def init_stored_fillers(self):
        """Read the stored filler items from memory and fill the stored_fillers dictionary"""
        self.stored_fillers[RAC3ITEM.BOLTS] = self._read32(RAC3STATUS.BOLT_PACKS)
        self.stored_fillers[RAC3ITEM.JACKPOT] = self._read32(RAC3STATUS.JACKPOT_PACKS)
        self.stored_fillers[RAC3ITEM.NANOTECH_XP] = self._read32(RAC3STATUS.NANOTECH_EXP_PACKS)
        self.stored_fillers[RAC3ITEM.WEAPON_XP] = self._read32(RAC3STATUS.WEAPON_LEVEL_PACKS)
        logger.debug(f"Stored filler items: {self.stored_fillers}")

    #############################
    # Start of Main Update Loop #
    #############################

    def early_update(self):
        """Ran early in the update cycle, memory reads should happen here before any evaluations begin"""
        new_planet = PLANET_NAME_FROM_ID[self._read8(RAC3STATUS.PLANET)]
        if self.planet != new_planet:
            self.planet = new_planet
            self.new_planet = True
        else:
            self.new_planet = False
        self.player_type = PLAYER_TYPE_TO_NAME[self._read8(RAC3STATUS.PLAYER_TYPE)]
        self.player_pos = RAC3POSITIONDATA(
            self._read_float(RAC3STATUS.POS_X),
            self._read_float(RAC3STATUS.POS_Y),
            self._read_float(RAC3STATUS.POS_Z))
        self.vehicle = self._read32(RAC3STATUS.VEHICLE_POINTER)
        self.action = self._read8(RAC3STATUS.ACTION)
        self.action_type = self._read8(RAC3STATUS.ACTION_TYPE)
        self.ratchet_moby = self._read32(RAC3STATUS.RATCHET_MOBY_POINTER)
        if not self.between_planets:
            self.between_planets = not bool(self.ratchet_moby)
        elif self.ratchet_moby:
            self.between_planets = False if self.action else True
        self.short_pause = bool(self._read8(RAC3STATUS.SHORT_PAUSE))
        self.long_pause = bool(self._read8(RAC3STATUS.LONG_PAUSE))
        self.prev_action = self._read8(RAC3STATUS.PREV_ACTION)
        self.inputs = RAC3INPUT(self._read16(RAC3STATUS.READ_INPUT))
        self.health = self._read8(RAC3STATUS.HEALTH)
        self.max_health = self._read8(RAC3STATUS.MAX_HEALTH)
        self.crystals_current = self._read8(RAC3STATUS.CRYSTALS_CURRENT)
        self.crystals_traded = self._read8(RAC3STATUS.CRYSTALS_TRADED)
        self.skillpoints = len([byte for byte in self._read_bytes(RAC3STATUS.SKILLPOINTS, 30) if byte])
        self.qwarktastic = self._read8(RAC3STATUS.QWARKTASTIC)
        if self.options.goal_museum:
            self.museum_unlocked = all(self._read_bytes(RAC3STATUS.TROPHY_FLAGS, 15))
            self.museum_visited = bool(self._read8(RAC3_REGION_DATA_TABLE[RAC3REGION.MUSEUM].VISIT_ADDRESS))
        self.boss_qwark = self._read_flag(RAC3PROGRESSFLAG.FLORANA_DEFEAT_QWARK)
        self.boss_two = self._read8(RAC3_LOCATION_DATA_TABLE[
                                        RAC3LOCATION.NATION_THE_TERRIBLE_TWO].CHECK_ADDRESS[0].ADDRESS)
        self.boss_noid = self._read_flag(RAC3PROGRESSFLAG.TYHRRANOSIS_DEFEAT_MOMMA_TYHRRANOID)
        self.boss_warship = self._read_flag(RAC3PROGRESSFLAG.DAXX_DEFEAT_WARSHIP)
        self.boss_scorpio = self._read8(RAC3_LOCATION_DATA_TABLE[
                                            RAC3LOCATION.NATION_MEET_COURTNEY].CHECK_ADDRESS[0].ADDRESS)
        self.boss_talos = (self.options.shortcuts.get(RAC3SHORTCUTS.HOLOSTAR_CLANK, False)
                           or self._read_flag(RAC3PROGRESSFLAG.HOLOSTAR_STUDIOS_CLANK_FINISH_CLANK_SECTION))
        self.boss_gears = self._read_flag(RAC3PROGRESSFLAG.OBANI_DRACO_DEFEAT_COURTNEY)
        self.boss_klunk = self._read_flag(RAC3PROGRESSFLAG.METROPOLIS_DEFEATED_KLUNK)
        self.boss_nef = self._read8(RAC3STATUS.NEFARIOUS)
        self.boss_bio = self._read8(RAC3STATUS.BIOBLITERATOR) & (1 << 6)
        self.is_reloading = self._read8(RAC3STATUS.FORCE_RELOAD)
        self.inside_hacker_puzzle = self._read8(RAC3STATUS.HELD_ITEM) == RAC3_ITEM_DATA_TABLE[RAC3ITEM.HACKER].ID
        self.equipped_item = self._read8(RAC3STATUS.EQUIPPED)
        self.held_item = self._read8(RAC3STATUS.HELD_ITEM)
        self.last_used_0 = self._read8(RAC3STATUS.LAST_USED_0)
        self.last_used_1 = self._read8(RAC3STATUS.LAST_USED_1)
        self.last_used_2 = self._read8(RAC3STATUS.LAST_USED_2)
        self.last_used_3 = self._read8(RAC3STATUS.LAST_USED_3)
        self.last_used_4 = self._read8(RAC3STATUS.LAST_USED_4)
        self.last_used_5 = self._read8(RAC3STATUS.LAST_USED_5)
        self.weapon_demo = self._read8(RAC3STATUS.WEAPON_DEMO)
        self.message_display = bool(self._read_float(self._read32(RAC3MESSAGEBOX.VISIBLE_POINTER)))
        self.nanotech_exp = self._read32(RAC3STATUS.NANOTECH_EXP)
        self.clank_disabled = bool(self._read8(RAC3STATUS.NO_CLANK))
        self.pda_vendor = self.find_pda_vendor()
        self.holo_final_door = self.find_holostar_door()
        if self.holo_final_door:
            pos = (self._read_float(self.holo_final_door + 0x10), self._read_float(self.holo_final_door + 0x14))
            if abs(pos[0] - self.player_pos.X) < 10 and abs(pos[1] - self.player_pos.Y) < 10:
                self.holo_door = self._read16(self.holo_final_door + 0xBE)
        else:
            self.holo_door = 0
        self.pause_check()
        if (self.new_planet or self.between_planets or self.is_reloading
            or self.game_state_value == RAC3GAMESTATE.PLANET_CHANGE):
            self.invalidate_string_table_cache()
        self.vendor_type = self.vendor_check()
        self.get_visited_planets()
        self.determine_weapon_vendor_items()
        self.determine_armor_vendor_items()
        self.vehicle_check()
        self.check_latches()

    def find_pda_vendor(self) -> int:
        """Traverse the moby linked list on Qwarks Hideout to find the PDA vendor moby and return its address"""
        if self.planet != RAC3REGION.QWARKS_HIDEOUT or RAC3LOCATION.HIDEOUT_PDA in self.checked_locations:
            # reset PDA vendor when leaving Qwarks Hideout
            return 0
        target_moby_id = RAC3STATUS.PDA_VENDOR_MOBY_ID
        if self.pda_vendor and self._read16(self.pda_vendor + 0xB2) == target_moby_id:
            return self.pda_vendor
        return self.find_moby_by_id_iteration(target_moby_id)

    def find_holostar_door(self) -> int:
        """Traverse the moby linked list on Holostar to find the final door moby and return its address"""
        if self.planet != RAC3REGION.HOLOSTAR_STUDIOS or RAC3LOCATION.HOLOSTAR_RETURN_TO_SHIP in self.checked_locations:
            # reset moby ID when leaving planet
            return 0
        if self.holo_final_door and self._read16(self.holo_final_door + 0xB2) == 0xC2:
            return self.holo_final_door
        return self.find_moby_by_id_iteration(0xC2)

    def vendor_check(self) -> RAC3VENDORTYPE | None:
        """Returns the current vendor type if the vendor is open, else None"""
        vendor_open = self.game_state_value == RAC3GAMESTATE.VENDOR
        self.update_vendor_name_restores(vendor_open)
        if vendor_open and self.planet in PLANET_VENDOR_OFFSET:
            self.last_in_vendor_time = time.time()
            self.vendor_cursor_pos = self._read32(
                RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.CURSOR_OFFSET, self.current_game))
            try:
                return RAC3VENDORTYPE(self._read8(RAC3VENDOR.get_vendor_property_address(
                    self.planet, RAC3VENDOR.VENDOR_TYPE_OFFSET, self.current_game)))
            except ValueError:
                return None
        return None

    def update_vendor_name_restores(self, vendor_open: bool):
        """Recheck pending name restores and queue any still needed while the vendor is closed."""
        if not self.vendor_name_patches or (vendor_open and not self.vendor_name_restore_pending):
            return
        self.vendor_name_restore_pending = True
        for patch in self.vendor_name_patches.values():
            self.write_batcher.pop((patch.address, self.DataType.INT32), None)
        if self.get_string_table() != self.vendor_name_table:
            return

        remaining = {}
        addresses = [patch.address for patch in self.vendor_name_patches.values()]
        for (text_id, patch), entry in zip(self.vendor_name_patches.items(), self.read_string_entries(addresses)):
            if entry.text_id == text_id and entry.text_pointer == patch.replacement:
                remaining[text_id] = patch
        if self.get_string_table() != self.vendor_name_table:
            return

        self.vendor_name_patches = remaining
        self.vendor_name_restore_pending = bool(remaining) and not vendor_open
        if not remaining:
            self.vendor_name_table = None
        if self.vendor_name_restore_pending:
            for patch in remaining.values():
                self._write32(patch.address, patch.original, should_convert=False)

    def get_visited_planets(self):
        """Returns a set of all planets the player has visited"""
        for region, region_data in RAC3_REGION_DATA_TABLE.items():
            if region in self.visited_planets:
                continue
            unlock_item = INFOBOT_FROM_PLANET.get(region, None)
            if unlock_item is not None:
                unlock_data = self.UnlockItem.get(unlock_item, None)
                # skip planets that are not unlocked yet
                if not unlock_data:
                    continue
            # only read visited flag for newly-unlocked, unvisited planets
            if self._read8(region_data.VISIT_ADDRESS):
                self.visited_planets.add(region)

    def determine_weapon_vendor_items(self):
        """Determine which items should be sold by the weapon vendor on the current planet."""
        if self.options.weapon_vendors:
            items_to_sell: list[str] = []
            already_sold = set()
            for loc, item in WEAPON_VENDOR_LOCATION_TO_ITEM.items():
                if item == RAC3ITEM.RY3N0 and not self.options.ngplus_vendors:
                    continue
                planet = WEAPON_VENDOR_LOCATION_TO_UNLOCK_REGION[loc]
                if self.options.vendor_access:
                    if item not in already_sold and self.UnlockItem[INFOBOT_FROM_PLANET[planet]]:
                        if loc in self.checked_locations:
                            already_sold.add(item)
                        else:
                            items_to_sell.append(item)
                else:
                    if item == RAC3ITEM.HOLO_SHIELD and RAC3LOCATION.TYHRRANOSIS_BOSS not in self.checked_locations:
                        continue
                    if item not in already_sold and planet in self.visited_planets:
                        if loc in self.checked_locations:
                            already_sold.add(item)
                        else:
                            items_to_sell.append(item)
            self.weapon_vendor_items = items_to_sell

        if self.options.ngplus_items:
            omega_items_to_sell: list[str] = []
            v5_weapons = {weapon_name for weapon_name in self.weapon_levels if self.weapon_levels[weapon_name] == 5}
            already_omega = {weapon_name for weapon_name in self.weapon_levels if self.weapon_levels[weapon_name] > 5}
            progressive_weapons_mode = self.options.progressive_weapons
            if self.options.weapon_level_locations and progressive_weapons_mode == 2:
                progressive_weapons_mode = 1  # Force manual levelling if weapon level locations are enabled
            for weapon in v5_weapons:
                if weapon == RAC3ITEM.RY3N0:
                    continue
                if weapon not in already_omega and weapon not in omega_items_to_sell:
                    if progressive_weapons_mode == 1:
                        if self.UnlockItem[weapon] > 5:
                            omega_items_to_sell.append(weapon)
                    else:
                        omega_items_to_sell.append(weapon)
            self.omega_weapon_vendors_items = omega_items_to_sell

    def determine_armor_vendor_items(self):
        """Determine which items should be sold by the armor vendor on the Starship Phoenix."""
        if not self.options.armor_vendor or self.planet != RAC3REGION.STARSHIP_PHOENIX:
            return
        items_to_sell: list[str] = []
        already_sold = set()
        for location, item in ARMOR_VENDOR_LOCATION_TO_ITEM.items():
            planet = ARMOR_VENDOR_LOCATION_TO_UNLOCK_REGION[location]
            if self.options.vendor_access:
                if item not in already_sold and self.UnlockItem[INFOBOT_FROM_PLANET[planet]]:
                    if location in self.checked_locations:
                        already_sold.add(item)
                    else:
                        items_to_sell.append(item)
            else:
                if item not in already_sold and planet in self.visited_planets:
                    if location in self.checked_locations:
                        already_sold.add(item)
                    else:
                        items_to_sell.append(item)
        self.armor_vendor_items = items_to_sell

    def vehicle_check(self):
        """
        Updates the last_in_vehicle_time when the player is in a vehicle.
        Used to detect if the player died while in a vehicle for deathlink.
        """
        current_time = time.time()
        if self.vehicle or (current_time - self.last_in_vehicle_time < 1 and self.action == RAC3PLAYERACTION.DEATH):
            self.last_in_vehicle_time = current_time

    def pause_check(self):
        """Update the current pause data, depending on the current planet"""
        planet_data = RAC3_REGION_DATA_TABLE.get(self.planet)
        if planet_data:
            pause_addr = planet_data.PAUSE_ADDRESS
            game_state = self._read8(RAC3STATUS.GAME_STATE + planet_data.PLANET_SPECIAL_OFFSET)
            self.game_state_value = RAC3GAMESTATE(
                game_state) if game_state <= 9 and game_state != 1 else RAC3GAMESTATE.INVALID
            self.pausing_game_state = True if self.game_state_value > RAC3GAMESTATE.UNPAUSED else False
            self.pause_menu = bool(pause_addr and self.game_state_value == RAC3GAMESTATE.PAUSED
                                   and self._read8(pause_addr))
        else:
            # Unknown planet, assume paused to be safe
            self.pause_menu = True
            self.game_state_value = RAC3GAMESTATE.PAUSED
            self.pausing_game_state = True

    def check_latches(self):
        """Check specific latched states need to be reset"""
        if self.homewarping:
            if self.game_state_value != RAC3GAMESTATE.PLANET_CHANGE:
                self.homewarping = False
        if self.self_respawning:
            if not self.is_reloading:
                self.self_respawning = False

    ##############
    # Intro Skip #
    ##############

    def homewarp(self, planet_id=3):
        """Triggers a planet load to the input planet id, defaulting to the Starship Phoenix"""
        if self.planet not in RAC3_REGION_DATA_TABLE.keys():
            # Unknown planet, abort homewarp
            logger.error(f"Aborting homewarp, Unknown Planet: {self.planet}")
            return
        destination = PLANET_NAME_FROM_ID.get(planet_id)
        if (destination is None or destination in INVALID_PLANETS
            or destination in [RAC3REGION.GALAXY, RAC3REGION.MENU]):
            logger.error(f"Aborting homewarp, invalid destination planet ID: {planet_id}")
            return
        planet_data = RAC3_REGION_DATA_TABLE[self.planet]
        if planet_data.PLANET_TO_LOAD:
            self.homewarping = True
            # Ensure the player is not softlocked from entering the sewers
            if self.planet == RAC3REGION.AQUATOS_BASE:
                self._write8(RAC3STATUS.SEWERS_VISITED, 1)
            self._write8(planet_data.PLANET_TO_LOAD, planet_id)
            self._write8(planet_data.PLANET_SPECIAL_OFFSET + RAC3STATUS.PLANET_LOAD, 1)
            self._write8(planet_data.PLANET_SPECIAL_OFFSET + RAC3STATUS.GAME_STATE, RAC3GAMESTATE.PLANET_CHANGE)
            logger.debug(f"Player home-warped from {self.planet}")
        else:
            logger.warning(f"Couldn't find warp data to leave planet: {self.planet}")

    #################
    # Receive Items #
    #################

    def item_received(self,
                      item_code: int,
                      our_name: str | None,
                      other_player: str | None,
                      location: int):
        """Handle receiving items from the multiworld"""
        name = PROG_TO_NAME_DICT.get(ITEM_FROM_AP_CODE[item_code], ITEM_FROM_AP_CODE[item_code])
        if other_player is not None:
            classification = RAC3_ITEM_DATA_TABLE[name].AP_CLASSIFICATION
            if other_player == our_name:
                if location == 0:
                    pass
                elif location > 0:
                    if classification == ItemClassification.trap:
                        self.enqueue_notification(
                            f"{RAC3TEXTFORMATSTRING.WHITE}Activated "
                            f"{RAC3TEXTFORMATSTRING.NORMAL}{ITEM_FROM_AP_CODE[item_code]} "
                            f"{RAC3TEXTFORMATSTRING.WHITE}at\n"
                            f"{RAC3TEXTFORMATSTRING.WHITE}{LOCATION_FROM_AP_CODE[location]}",
                            RAC3BOXTHEME.WARNING)
                    else:
                        self.enqueue_notification(
                            f"Found "
                            f"{CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]} "
                            f"{RAC3TEXTFORMATSTRING.NORMAL}at\n{LOCATION_FROM_AP_CODE[location]}")
                else:
                    if classification == ItemClassification.trap:
                        self.enqueue_notification(
                            f"{RAC3TEXTFORMATSTRING.WHITE}Activated "
                            f"{RAC3TEXTFORMATSTRING.NORMAL}{ITEM_FROM_AP_CODE[item_code]}",
                            RAC3BOXTHEME.WARNING)
                    else:
                        self.enqueue_notification(
                            f"Collected {CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]}")
            else:
                if classification == ItemClassification.trap:
                    self.enqueue_notification(
                        f"{RAC3TEXTFORMATSTRING.GREEN}{other_player}"
                        f"{RAC3TEXTFORMATSTRING.WHITE} activated your "
                        f"{RAC3TEXTFORMATSTRING.NORMAL}{ITEM_FROM_AP_CODE[item_code]}",
                        RAC3BOXTHEME.WARNING)
                else:
                    self.enqueue_notification(
                        f"Received {CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]} "
                        f"{RAC3TEXTFORMATSTRING.NORMAL}from "
                        f"{RAC3TEXTFORMATSTRING.GREEN}{other_player}")
        logger.debug(f"Item received: {ITEM_FROM_AP_CODE[item_code]}, AP code: {item_code}")
        if name in infobot_data.keys():
            if self.UnlockItem[name]:
                return
            self.UnlockItem[RAC3SHIPSLOT.SLOT_0] += 1
            self.UnlockItem[name] = self.UnlockItem[RAC3SHIPSLOT.SLOT_0]
        else:
            self.UnlockItem[name] += 1
        if name in WEAPON_TO_WEAPON_MODPACK.values():
            self.UnlockItem[name] = WEAPONMOD.ALL
        if name in WEAPON_MOD_TO_WEAPON:
            self.UnlockItem[WEAPON_TO_WEAPON_MODPACK[WEAPON_MOD_TO_WEAPON[name][0]]] |= WEAPON_MOD_TO_WEAPON[name][1]
        match name:
            case RAC3ITEM.HACKER:
                self.puzzle_cycler(name, RAC3SPEEDUPS.HACKER, "opened_the_hacker_doors",
                                   PLANETS_WITH_HACKER_PUZZLES, HACKER_PUZZLE_TO_REGION, True)
            case RAC3ITEM.TYHRRA_GUISE:
                self.puzzle_cycler(name, RAC3SPEEDUPS.TYHRRAGUISE, "opened_the_tyhrranoid_doors",
                                   PLANETS_WITH_TYHRRANOID_PUZZLES, TYHRRANOID_PUZZLE_TO_REGION, True)
            case RAC3ITEM.REFRACTOR:
                self.puzzle_cycler(name, RAC3SPEEDUPS.REFRACTOR, "opened_the_refractor_doors",
                                   PLANETS_WITH_REFRACTOR_PUZZLES, REFRACTOR_PUZZLE_TO_REGION, True)
            case RAC3ITEM.PROGRESSIVE_VIDCOMIC:
                if self.UnlockItem[name] > 5:
                    self.UnlockItem[name] = 5
            case RAC3ITEM.PROGRESSIVE_ARMOR:
                if self.UnlockItem[name] > 4:
                    self.UnlockItem[name] = 4
            case RAC3ITEM.PROGRESSIVE_PACK:
                self.UnlockItem[RAC3ITEM.CLANK] = 1
                self.UnlockItem[RAC3ITEM.HELI_PACK] = 1
                if self.UnlockItem[name] > 1:
                    self.UnlockItem[RAC3ITEM.THRUSTER_PACK] = 1
                    self.UnlockItem[name] = 2
                    self._write32(RAC3STATUS.PENDING_PACK, gadget_data[RAC3ITEM.THRUSTER_PACK].ID)
                else:
                    self._write32(RAC3STATUS.PENDING_PACK, gadget_data[RAC3ITEM.HELI_PACK].ID)
            case RAC3ITEM.HELI_PACK:
                self.UnlockItem[RAC3ITEM.CLANK] = 1
                if self.options.clank_options > 0:
                    self._write32(RAC3STATUS.PENDING_PACK, gadget_data[name].ID)
            case RAC3ITEM.THRUSTER_PACK:
                self.UnlockItem[RAC3ITEM.CLANK] = 1
                if self.options.clank_options > 0:
                    self._write32(RAC3STATUS.PENDING_PACK, gadget_data[name].ID)
            case RAC3ITEM.CLANK:
                self.UnlockItem[RAC3ITEM.HELI_PACK] = 1
                self.UnlockItem[RAC3ITEM.THRUSTER_PACK] = 1
            case RAC3ITEM.CHARGE_BOOTS:
                self._write8(RAC3STATUS.EQUIP_BOOTS, 0x1D)
            case RAC3ITEM.PROGRESSIVE_WRENCH:
                if self.UnlockItem[name] > 8:
                    self.UnlockItem[name] = 8
                self.puzzle_cycler(name, RAC3SPEEDUPS.BOLT_CRANK, "turned_the_bolt_cranks",
                                   PLANETS_WITH_BOLT_CRANK_PUZZLES, BOLT_CRANK_TO_REGION, True)
            case RAC3ITEM.TITANIUM_BOLT:
                if self.UnlockItem[name] > 40:
                    self.UnlockItem[name] = 40
            case RAC3ITEM.BOLTS:
                bolt = self._read32(RAC3STATUS.BOLTS)
                bolt_percentage = self.options.filler_magnitude.get(name, filler_magnitude_data[name])
                bolt_pack = min(200000, max(30000, int(bolt * bolt_percentage / 100)))
                new_bolts = bolt + bolt_pack
                if new_bolts > 0x7FFFFFFF:
                    new_bolts = 0x7FFFFFFF
                self._write32(RAC3STATUS.BOLTS, new_bolts)
                bolt_packs = self._read32(RAC3STATUS.BOLT_PACKS)
                if bolt_packs < 0x7FFFFFFF:
                    bolt_packs += 1
                self._write32(RAC3STATUS.BOLT_PACKS, bolt_packs)
            case RAC3ITEM.INFERNO_MODE:
                timer = self._read32(RAC3STATUS.INFERNO_TIMER)
                new_timer = timer + 1000 + randint(1, 100)
                if new_timer > 0x7FFFFFFF:
                    new_timer = 0x7FFFFFFF
                self._write32(RAC3STATUS.INFERNO_TIMER, new_timer)
            case RAC3ITEM.JACKPOT:
                # Limit multiplier to 128x
                if self.bolt_and_xp_multiplier_value <= 6:
                    jackpot_duration = self.options.filler_magnitude.get(name, filler_magnitude_data[name])
                    _time = time.time() + jackpot_duration
                    key = name + str(_time)
                    # if key already exists, add 1 millisecond to prevent overlap
                    if key in self.timers:
                        _time += 0.001
                        key = name + str(_time)
                    self.timers[key] = _time
                    self.bolt_and_xp_multiplier_value += 1
                jackpot_packs = self._read32(RAC3STATUS.JACKPOT_PACKS)
                if jackpot_packs < 0x7FFFFFFF:
                    jackpot_packs += 1
                self._write32(RAC3STATUS.JACKPOT_PACKS, jackpot_packs)
            case RAC3ITEM.NANOTECH_XP:
                if not self.nanotech_exp:
                    self.nanotech_exp = self._read32(RAC3STATUS.NANOTECH_EXP)
                nanotech_percentage = self.options.filler_magnitude.get(name, filler_magnitude_data[name])
                nanotech_gain = min(300000, max(20000, int(self.nanotech_exp * nanotech_percentage / 100)))
                self.nanotech_exp += nanotech_gain
                if self.nanotech_exp > 0x7FFFFFFF:
                    self.nanotech_exp = 0x7FFFFFFF
                self._write32(RAC3STATUS.NANOTECH_EXP, self.nanotech_exp)
                nanotech_exp_packs = self._read32(RAC3STATUS.NANOTECH_EXP_PACKS)
                if nanotech_exp_packs < 0x7FFFFFFF:
                    nanotech_exp_packs += 1
                self._write32(RAC3STATUS.NANOTECH_EXP_PACKS, nanotech_exp_packs)
            case RAC3ITEM.WEAPON_XP:
                valid_weapons = self.get_valid_weapon_level_ups()
                if valid_weapons:
                    selected_weapon = choice(valid_weapons)
                    if self.game_state_value == RAC3GAMESTATE.WEAPON_UPGRADE:
                        self.delayed_weapon_levelups.append(selected_weapon)
                    else:
                        self.weapon_level_up(selected_weapon)
                weapon_level_packs = self._read32(RAC3STATUS.WEAPON_LEVEL_PACKS)
                if weapon_level_packs < 0x7FFFFFFF:
                    weapon_level_packs += 1
                self._write32(RAC3STATUS.WEAPON_LEVEL_PACKS, weapon_level_packs)
            case RAC3ITEM.OHKO_TRAP:
                self._write8(RAC3STATUS.NANOPAK_HEALTH, 0)
                self._write8(RAC3STATUS.HEALTH, 1)
                if self.player_type == RAC3PLAYERTYPE.GIANT:
                    self._write32(RAC3STATUS.GIANT_CLANK_HEALTH, 1)
                if self.vehicle:
                    health_addr = self._read32(self._read32(self.vehicle + 0x68))
                    self._write_float(health_addr, 1)
            case RAC3ITEM.NO_AMMO_TRAP:
                for weapon_name in non_prog_weapon_data.keys():
                    if self.UnlockItem[weapon_name]:
                        self._write32(non_prog_weapon_data[weapon_name].AMMO_ADDRESS, 0)
                self._write8(RAC3STATUS.QWARK_AMMO, 0)
            case (RAC3ITEM.LOCK_TRAP | RAC3ITEM.MIRROR_TRAP | RAC3ITEM.BLACK_SCREEN_TRAP |
                  RAC3ITEM.INVISIBLE_TRAP | RAC3ITEM.DISARM_TRAP | RAC3ITEM.WRENCH_ONLY_TRAP):
                if self.timers.get(name, False):
                    self.timers[name] += self.options.trap_magnitude.get(name, trap_magnitude_data[name])
                else:
                    self.timers[name] = int(
                        time.time() + self.options.trap_magnitude.get(name, trap_magnitude_data[name]))
            case RAC3ITEM.NO_CLANK_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += self.options.trap_magnitude.get(name, trap_magnitude_data[name])
                else:
                    # Special case for holostar, nefarious base and klunk fight
                    if not self.clank_disabled:
                        self.timers[name] = int(
                            time.time() + self.options.trap_magnitude.get(name, trap_magnitude_data[name]))
            case RAC3ITEM.GADGETRON_DEBT_TRAP:
                # Losing bolts near pda vendor triggers failsafe for the pda vendor location,
                # so we need to delay the debt trap until the player is away from the pda vendor
                if not self.near_pda_vendor():
                    bolts = self._read32(RAC3STATUS.BOLTS)
                    impact = self.options.trap_magnitude.get(name, trap_magnitude_data[name])
                    if impact > 100:
                        impact = 100
                    new_bolts = bolts * (100 - impact) / 100
                    self._write32(RAC3STATUS.BOLTS, int(new_bolts))
                else:
                    self.delayed_debt_trap_count += 1
            case RAC3ITEM.LIGHTSABER_WRENCH:
                self._write8(RAC3STATUS.WRENCH_REPLACEMENT_CHEAT, 1)
        if name in non_prog_weapon_data.keys():
            if non_prog_weapon_data[name].AMMO:
                self._write32(non_prog_weapon_data[name].AMMO_ADDRESS, non_prog_weapon_data[name].AMMO)
        if name in quick_selectable_data.keys() and self.UnlockItem[name] == 1:
            self.update_equip(name)

    def get_valid_weapon_level_ups(self) -> list[str]:
        """Returns a list of valid weapons that can be leveled up from an xp reward, used for notifications"""
        valid_weapons = []
        for weapon_name, weapon_data in non_prog_weapon_data.items():
            if self.UnlockItem[weapon_name]:
                level = max(
                    RAC3_ITEM_DATA_TABLE[ITEM_NAME_FROM_ID[self._read8(weapon_data.LEVEL_ADDRESS)]].LEVEL,
                    self.weapon_levels.get(weapon_name, 1))
                if level == 5:
                    continue  # people should buy NG+ mega variant instead of getting them for free
                if self.options.ngplus_items:
                    max_level = 8
                else:
                    max_level = 5
                if ((weapon_name != RAC3ITEM.RY3N0 and level < max_level) or
                    (weapon_name == RAC3ITEM.RY3N0 and level < self.ryno)):
                    valid_weapons.append(weapon_name)
        return valid_weapons

    def weapon_level_up(self, weapon_name: str):
        """Level up a weapon from xp reward"""
        weapon_data = non_prog_weapon_data[weapon_name]
        current_id = self._read8(weapon_data.LEVEL_ADDRESS)
        current_name = ITEM_NAME_FROM_ID[current_id]
        current_level = max(RAC3_ITEM_DATA_TABLE[current_name].LEVEL, self.weapon_levels.get(weapon_name, 1))
        max_level = 8 if self.options.ngplus_items and weapon_name != RAC3ITEM.RY3N0 else 5
        if current_level < max_level:
            target_level = current_level + 1
            target_id = UPGRADE_DICT[weapon_name][target_level - 1]
            target_name = ITEM_NAME_FROM_ID[target_id]
            target_xp = RAC3_ITEM_DATA_TABLE[target_name].XP_THRESHOLD
            target_ammo = RAC3_ITEM_DATA_TABLE[target_name].AMMO
            self._write32(weapon_data.XP_ADDRESS, target_xp)
            self._write8(weapon_data.LEVEL_ADDRESS, target_id)
            if target_ammo:
                self._write32(weapon_data.AMMO_ADDRESS, target_ammo)

    @deprecated("Unused")
    def weapon_level_from_xp(self, weapon_name: str) -> int:
        """Returns the weapon level based on the current xp"""
        current_xp = self._read32(non_prog_weapon_data[weapon_name].XP_ADDRESS)
        level_from_xp = 1
        max_level = 5  # 8 if self.options.ngplus_items and weapon_name != RAC3ITEM.RY3N0 else 5
        for lvl in range(max_level):
            target_id = UPGRADE_DICT[weapon_name][lvl]
            target_name = ITEM_NAME_FROM_ID[target_id]
            xp_threshold = RAC3_ITEM_DATA_TABLE[target_name].XP_THRESHOLD
            if current_xp >= xp_threshold:
                level_from_xp = lvl + 1
        return level_from_xp

    @deprecated("Unused")
    def has_all_weapons(self) -> bool:
        """Returns whether the player has collected all weapons, used for endgame checks"""
        for weapon_name in non_prog_weapon_data.keys():
            if not self.UnlockItem[weapon_name]:
                return False
        return True

    # TODO: Make this more elegant in terms of how it checks for the next available quick select slot
    def update_equip(self, name: str):
        """Equip the most recently collected weapon/gadget, update recent uses"""
        if quick_selectable_data[name].ID:
            if name in equipable_data.keys():
                last_used_0 = self._read8(RAC3STATUS.LAST_USED_0)
                last_used_1 = self._read8(RAC3STATUS.LAST_USED_1)
                self._write8(RAC3STATUS.LAST_USED_2, last_used_1)
                self._write8(RAC3STATUS.LAST_USED_1, last_used_0)
                self._write8(RAC3STATUS.LAST_USED_0, equipable_data[name].ID)
                self._write8(RAC3STATUS.EQUIPPED, equipable_data[name].ID)
                if not self._read8(RAC3STATUS.WEAPON_LOCK):
                    self._write8(RAC3STATUS.PENDING_ITEM, equipable_data[name].ID)
            for slot in QUICK_SELECT_LIST:
                slot_address = RAC3_STATUS_DATA_TABLE[slot].SLOT_ADDRESS
                if not self._read8(slot_address):
                    self._write8(slot_address, quick_selectable_data[name].ID)
                    break

    ###################
    # Check Locations #
    ###################

    def is_location_checked(self, ap_code: int) -> bool:
        """Reads location data to find what memory check should be done, returns the collection state of the location"""
        location = LOCATION_FROM_AP_CODE[ap_code]
        if location in self.checked_locations:
            return True
        loc_data: RAC3LOCATIONDATA = RAC3_LOCATION_DATA_TABLE[location]
        if (not loc_data  # Ignore locations we don't have data for
            or location == RAC3LOCATION.COMMAND_CENTER_INFOBOT  # Handle CC unlock elsewhere
            or self.weapon_demo and RAC3_ITEM_DATA_TABLE[  # Prevent sending weapon purchases by testing a weapon in VR
                ITEM_NAME_FROM_ID[self.weapon_demo]].UNLOCK_ADDRESS_2 == loc_data.CHECK_ADDRESS):
            return False
        if (self.options.weapon_level_locations and
            self.options.progressive_weapons and
            RAC3TAG.WEAPON_LEVEL in loc_data.TAGS):
            weapon_id = loc_data.CHECK_ADDRESS[0].VALUE
            weapon_level = RAC3_ITEM_DATA_TABLE[ITEM_NAME_FROM_ID.get(weapon_id, RAC3ITEM.SHOCK_CANNON_V8)].LEVEL
            weapon_name = next(name for name, ids in UPGRADE_DICT.items() if weapon_id in ids)
            if weapon_level > self.weapon_levels[weapon_name]:
                return False  # Prevent weapon over-levelling from sending
        # TODO: Implement a distance based checktype
        current_pos = self.player_pos
        pos_loc: bool = False
        pos_check: bool = False
        if location == RAC3LOCATION.OBANI_GEMINI_SKIDD and self.planet == RAC3REGION.OBANI_GEMINI:
            pos_loc = True
            skidd_pos = RAC3POSITIONDATA(201.2, 364.0, 296.8)
            pos_check = (
                abs(current_pos.X - skidd_pos.X) < 8.0
                and abs(current_pos.Y - skidd_pos.Y) < 8.0
                and abs(current_pos.Z - skidd_pos.Z) < 5.0
            )
        if location == RAC3LOCATION.PHOENIX_MEET_SASHA and self.planet == RAC3REGION.STARSHIP_PHOENIX:
            pos_loc = True
            sasha_pos = RAC3POSITIONDATA(157.0, 362.0, 118.0)
            pos_check = (
                abs(current_pos.X - sasha_pos.X) < 8.0
                and abs(current_pos.Y - sasha_pos.Y) < 8.0
                and abs(current_pos.Z - sasha_pos.Z) < 5.0
            )
        if pos_loc:
            if pos_check:
                logger.debug(f"{location} checked, {len(self.checked_locations) / self.pre_end}% completion")
                self.checked_locations.add(location)
                return True
            return False
        if location == RAC3LOCATION.ARIDIA_RANGERS_5 and self.options.speedups.get(RAC3SPEEDUPS.MISSIONS, False):
            if self._read8(MISSION_COUNTS[location]) > 1:  # Aridia final mission needs special checks
                logger.debug(f"{location} checked, {len(self.checked_locations) / self.pre_end}% completion")
                self.checked_locations.add(location)
                return True
            return False
        check_all = self.location_flags_set(loc_data)
        if check_all:
            logger.debug(f"{location} checked, {len(self.checked_locations) / self.pre_end}% completion")
            self.checked_locations.add(location)
        return check_all

    def location_flags_set(self, loc_data: RAC3LOCATIONDATA) -> bool:
        """Returns whether the game memory shows this location as collected"""
        check_all: bool = True
        for check in loc_data.CHECK_ADDRESS:
            value_to_check = 0
            match check.TYPE & CHECKTYPE.SIZE:
                case CHECKTYPE.SKIP:
                    continue
                case CHECKTYPE.BIT:
                    check_all &= check.VALUE in self._read_bits(check.ADDRESS)
                    continue
                case CHECKTYPE.BYTE:
                    value_to_check = self._read8(check.ADDRESS)
                case CHECKTYPE.SHORT:
                    value_to_check = self._read16(check.ADDRESS)
                case CHECKTYPE.INT:
                    value_to_check = self._read32(check.ADDRESS)
            check_all &= check.check_condition(value_to_check)
        return check_all

    def titanium_bolt_count(self) -> int:
        """Titanium Bolts towards the goal: received items, or collected pickups if they aren't randomized"""
        if self.options.titanium_bolts:
            return self.UnlockItem[RAC3ITEM.TITANIUM_BOLT]
        for name, loc_data in RAC3_LOCATION_DATA_TABLE.items():
            if (RAC3TAG.T_BOLT in loc_data.TAGS and name != RAC3TROPHY.PHOENIX_TITANIUM_COLLECTOR
                and name not in self.collected_tbolt_locations and self.location_flags_set(loc_data)):
                self.collected_tbolt_locations.add(name)
        return len(self.collected_tbolt_locations)

    #############
    # Deathlink #
    #############

    def reload_check(self):
        """Detects if the game is being reloaded, and updates death data"""
        if self.is_reloading and not self.reloading_handled and not self.self_respawning:
            self.last_death_state = self.action
            self.died_in_vehicle = time.time() - self.last_in_vehicle_time < 1.5
            self.died_from_softlock = self._read16(RAC3STATUS.SOFTLOCK_TIMER) >= 0xE0
            self.reloading_handled = True
            logger.debug(f"{self.player_type} is Respawning, death state: {self.last_death_state},"
                         f" death count: {self.last_death_count}, in vehicle? {self.died_in_vehicle}")
        if not self.is_reloading and self.reloading_handled:
            self.death_count = self._read32(RAC3STATUS.DEATH_COUNT)
            self.has_died = self.death_count > self.last_death_count
            self.last_death_count = self.death_count
            self.reloading_handled = False
            if self.has_died:
                if self.track_deaths:
                    self.enqueue_notification(
                        f"{RAC3TEXTFORMATSTRING.NORMAL}Death Count: {RAC3TEXTFORMATSTRING.WHITE}{self.death_count}",
                        RAC3BOXTHEME.DEATHLINK)
            logger.debug(f"{self.player_type} has Respawned, death count: {self.death_count}, has died?"
                         f" {self.has_died}")
        else:
            self.has_died = False

    def alive(self) -> tuple[bool, str]:
        """Checks the current game state to determine if the player is still alive, and if not then how they died"""
        if self.has_died:
            self.last_death_count = self.death_count
            logger.debug("Death Detected! (death count increased)")
            match self.player_type:
                case RAC3PLAYERTYPE.CLANK:
                    death = CLANK_DEATH_FROM_ACTION.get(self.last_death_state, "ran out of nanotech.")
                case RAC3PLAYERTYPE.GIANT:
                    death = "didn't stick to the script."
                case _:
                    death = DEATH_FROM_ACTION.get(self.last_death_state, "ran out of nanotech.")

            # Vehicle pointer becomes 0 during reload, but the address next to it gets a value during reload after
            # vehicle death
            if self.died_in_vehicle:
                # Vehicle death uses state 34 which is the same as getting eaten by a shark
                death = "didn't leave the vehicle in time."
            elif self.died_from_softlock:
                death = "softlocked."
            return False, f"{self.player_type} {death}"

        # logger.debug(f"{self.player_type} is Alive")
        return True, f"{self.player_type} is Alive"

    def can_be_killed(self) -> bool:
        """Checks if the player can be killed based on the current game state."""
        current_time = time.time()
        if (self.pausing_game_state
            or self.inside_hacker_puzzle
            or (self.action_type == RAC3ACTIONTYPE.PLAYER_MOVEMENT_LOCKED and not self.vehicle)
            or self.action_type == RAC3ACTIONTYPE.IN_CUTSCENE):
            self.deathlink_grace_period = current_time
        if current_time - self.deathlink_grace_period < 1:
            return False
        return True

    def kill_player(self) -> bool:
        """Checks the current game state to determine if and how to kill the player, returns success/failure"""
        if not self.can_be_killed():
            logger.debug("player unable to be killed")
            return False
        new_health = (self._read8(RAC3STATUS.NANOPAK_HEALTH)
                      if self.options.deathlink_behavior == 1 and self.player_type == RAC3PLAYERTYPE.RATCHET
                      else 0)
        self._write8(RAC3STATUS.HEALTH, new_health)
        self._write8(RAC3STATUS.NANOPAK_HEALTH, 0)
        # death = choice(list(DEATH_FROM_ACTION.keys()))
        if self.vehicle:
            health_addr = self._read32(self._read32(self.vehicle + 0x68))
            self._write32(health_addr, 0)  # health is a float, but we can write 0 as int32
            if self.planet == RAC3REGION.MARCADIA:
                # special case for the marcadia turret mission that cant blow up
                # this will force mission failure and increase death count by 1
                vehicle_reload_addr = self.vehicle + 0xCB
                self._write8(vehicle_reload_addr, 0xD0)  # 0xD0: force reload from vehicle death
            else:
                vehicle_blow_up_addr = self.vehicle + 0xBC
                self._write8(vehicle_blow_up_addr, 0x9)  # 0x9: blow up vehicle immediately 0xA: force respawn
            # self._write8(RAC3STATUS.ACTION, death)
            logger.debug("player in vehicle, killing vehicle too")
            # logger.debug(f'player died of {DEATH_FROM_ACTION[death]}')
        else:
            match self.player_type:
                case RAC3PLAYERTYPE.RATCHET:
                    if self.action not in DEATH_FROM_ACTION.keys() and self.vehicle == 0:
                        self._write8(RAC3STATUS.ACTION, RAC3PLAYERACTION.HURT)
                        # update ratchet state to cancel free fall and other problematic states

                    # self._write8(RAC3STATUS.ACTION, death)
                    # logger.debug(f'player died of {DEATH_FROM_ACTION[death]}')
                case RAC3PLAYERTYPE.CLANK:
                    # Clank taking damage state (updates state to trigger death animation once at 0 health)
                    self._write8(RAC3STATUS.ACTION, RAC3PLAYERACTION.CLANK_HURT)
                    self._write8(RAC3STATUS.PREV_ACTION, RAC3PLAYERACTION.CLANK_HURT)  # Past state
                    self._write8(RAC3STATUS.SECOND_PREV_ACTION,
                                 RAC3PLAYERACTION.CLANK_HURT)  # This helps the death animation trigger
                    logger.debug("player is clank, clank must die dramatically")
                case RAC3PLAYERTYPE.GIANT:
                    # Giant Clank punched state (updates state to trigger death animation once at 0 health)
                    self._write32(RAC3STATUS.GIANT_CLANK_HEALTH, 0)
                    self._write8(RAC3STATUS.ACTION, RAC3PLAYERACTION.GIANT_CLANK_HURT)
                    self._write8(RAC3STATUS.PREV_ACTION, RAC3PLAYERACTION.GIANT_CLANK_HURT)  # Past state
                    self._write8(RAC3STATUS.SECOND_PREV_ACTION,
                                 RAC3PLAYERACTION.GIANT_CLANK_HURT)  # This helps the death animation trigger
                    logger.debug("player is giant clank, giant clank must die dramatically")
                case RAC3PLAYERTYPE.TYHRRANOID:
                    # Tyhrranoid taking damage state (updates state to trigger death animation once at 0 health)
                    self._write8(RAC3STATUS.ACTION, RAC3PLAYERACTION.TYHRRANOID_HURT)
                    self._write8(RAC3STATUS.PREV_ACTION, RAC3PLAYERACTION.TYHRRANOID_HURT)  # Past state
                    self._write8(RAC3STATUS.SECOND_PREV_ACTION,
                                 RAC3PLAYERACTION.TYHRRANOID_HURT)  # This helps the death animation trigger
                    logger.debug("player is tyhrranoid, tyhrranoid must be squished")
                case RAC3PLAYERTYPE.QWARK:
                    # Qwark taking damage state (updates state to trigger death animation once at 0 health)
                    self._write8(RAC3STATUS.ACTION, RAC3PLAYERACTION.QWARK_HURT)
                    self._write8(RAC3STATUS.PREV_ACTION, RAC3PLAYERACTION.QWARK_HURT)  # Past state
                    self._write8(RAC3STATUS.SECOND_PREV_ACTION,
                                 RAC3PLAYERACTION.QWARK_HURT)  # This helps the death animation trigger
                    logger.debug("player is qwark, qwark must die dramatically")
        logger.debug("player successfully killed")
        return True

    ##############
    # Check Goal #
    ##############

    def check_victory(self, server_locations) -> bool:
        """Returns a bool for if the current game state is 'completed' or not"""
        if not self.end_game:
            if self.options.goal_nano > self.max_health:
                return False
            if self.options.goal_crystal > (self.crystals_current + self.crystals_traded):
                return False
            if self.options.goal_tbolts > self.titanium_bolt_count():
                return False
            if self.options.goal_skillpoints > self.skillpoints:
                return False
            if self.options.goal_planets > len(self.visited_planets):
                return False
            if self.options.goal_completion:
                completion_locations = get_completion_location_names(
                    (LOCATION_FROM_AP_CODE[code] for code in server_locations), bool(self.options.lock_cc)
                )
                if self.options.goal_completion * len(completion_locations) > 100 * len(
                    self.checked_locations & completion_locations
                ):
                    return False
            if self.options.goal_qwark and not self.qwarktastic:
                return False
            if self.options.goal_museum and not (self.museum_unlocked and self.museum_visited):
                return False
            if self.options.goal_boss_qwark and not self.boss_qwark:
                return False
            if self.options.goal_boss_two and not self.boss_two:
                return False
            if self.options.goal_boss_noid and not self.boss_noid:
                return False
            if self.options.goal_boss_warship and not self.boss_warship:
                return False
            if self.options.goal_boss_scorpio and not self.boss_scorpio:
                return False
            if self.options.goal_boss_talos and not self.boss_talos:
                return False
            if self.options.goal_boss_gears and not self.boss_gears:
                return False
            if self.options.goal_boss_klunk and not self.boss_klunk:
                return False
            self.end_game = True
            ap_code = RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.COMMAND_CENTER_INFOBOT].AP_CODE
            if ap_code in server_locations and RAC3LOCATION.COMMAND_CENTER_INFOBOT not in self.checked_locations:
                self.collect_locations({RAC3LOCATION.COMMAND_CENTER_INFOBOT})
        if self.end_game:
            if self.options.goal_nef and not self.boss_nef:
                return False
            if self.options.goal_bio and not self.boss_bio:
                return False
        return True

    ###################
    # Changing Planet #
    ###################

    def map_switch(self) -> tuple[str, str]:
        """Update and validate the current planet for the UT map"""
        _raw_planet = RAC3_REGION_DATA_TABLE[self.planet].ID
        _safe_planet = _raw_planet
        if _raw_planet > 55 or self._read8(RAC3STATUS.MAP_CHECK) == 0:
            _safe_planet = 0
        elif _raw_planet > 29:
            _safe_planet = 3
        return PLANET_NAME_FROM_ID[_raw_planet], PLANET_NAME_FROM_ID[_safe_planet]

    def tyhrranosis_fix(self):
        """Prevent a Crash on Tyhrranosis by disabling the robot tyhrranoids"""
        if self.planet == RAC3REGION.TYHRRANOSIS:
            self._write8(RAC3STATUS.ROBONOIDS, 0)
            if self.options.shortcuts.get(RAC3SHORTCUTS.TYHRRANOSIS_DROPSHIP, False):
                self.tyhrra_dropship = bool(self._read8(RAC3CUTSCENEFLAG.TYHRRANOSIS_FINISH_PROLOGUE[0]) & (
                    1 << RAC3CUTSCENEFLAG.TYHRRANOSIS_FINISH_PROLOGUE[1]))

    def softlock_warning(self):
        """Checks if the player is on a planet with a potential softlock and informs them on how to escape"""
        match self.planet:
            case RAC3REGION.HOLOSTAR_STUDIOS | RAC3REGION.HOLOSTAR_STUDIOS_CLANK:
                if not (self.UnlockItem[RAC3ITEM.HACKER] and self.UnlockItem[RAC3ITEM.HYPERSHOT]):
                    logger.info("You do not have the items required to leave this planet through your ship. If you are"
                                " stuck, hold L2 + R2 + L1 + R1 + SELECT to warp back to the phoenix")
                    self.enqueue_notification(
                        f"You do not have the items required\nto leave this planet through your ship.\n\nHold:"
                        f"{RAC3TEXTFORMATSTRING.WHITE}{RAC3TEXTFORMATSTRING.L2}+{RAC3TEXTFORMATSTRING.R2}+"
                        f"{RAC3TEXTFORMATSTRING.L1}+{RAC3TEXTFORMATSTRING.R1}+ SELECT"
                        f"{RAC3TEXTFORMATSTRING.NORMAL}\nto warp back to the {RAC3TEXTFORMATSTRING.GREEN}Starship "
                        f"Phoenix{RAC3TEXTFORMATSTRING.NORMAL}.",
                        RAC3BOXTHEME.WARNING,
                        8.0)
            case RAC3REGION.PHOENIX_ASSAULT:
                logger.info("If you want to travel to the regular phoenix, hold L2 + R2 + L1 + R1 + SELECT")
                self.enqueue_notification(
                    f"If you want to travel to the regular phoenix\nHold:{RAC3TEXTFORMATSTRING.WHITE}"
                    f"{RAC3TEXTFORMATSTRING.L2}+{RAC3TEXTFORMATSTRING.R2}+{RAC3TEXTFORMATSTRING.L1}+"
                    f"{RAC3TEXTFORMATSTRING.R1}+ SELECT",
                    RAC3BOXTHEME.WARNING,
                    5.0)

    def region_disabled_warning(self):
        """Checks if the player went to a planet/region and informs them if they have disabled the content in their
        YAML"""
        match self.planet:
            case RAC3REGION.ANNIHILATION_NATION:
                if not self.options.arena:
                    log_message = "You have disabled Annihilation Nation in your YAML. "
                    notification_message = (f"You have disabled {RAC3TEXTFORMATSTRING.WHITE}Annihilation Nation"
                                            f"{RAC3TEXTFORMATSTRING.NORMAL} in your YAML.\n")
                    if self.options.weapon_vendors:
                        log_message += "You can still buy the Agents of Doom vendor check from the weapon vendor."
                        notification_message += (f"You can still buy the {RAC3TEXTFORMATSTRING.WHITE}Agents of Doom"
                                                 f"{RAC3TEXTFORMATSTRING.NORMAL} vendor check\nfrom the weapon vendor.")
                    else:
                        log_message += "There are no locations on this planet."
                        notification_message += "There are no locations on this planet."
                    logger.info(log_message)
                    self.enqueue_notification(notification_message, RAC3BOXTHEME.WARNING, 5.0)
            case RAC3REGION.METROPOLIS_RANGERS | RAC3REGION.TYHRRANOSIS_RANGERS:
                if self.options.rangers < 2:
                    log_message = (f"You have disabled {RAC3TEXTFORMATSTRING.WHITE}Optional Ranger Missions"
                                   f"{RAC3TEXTFORMATSTRING.NORMAL} in your YAML. There are no locations in this "
                                   f"region.")
                    notification_message = (f"You have disabled {RAC3TEXTFORMATSTRING.WHITE}Optional Ranger Missions"
                                            f"{RAC3TEXTFORMATSTRING.NORMAL} in your YAML.\nThere are no locations in "
                                            f"this region.")
                    logger.info(log_message)
                    self.enqueue_notification(notification_message, RAC3BOXTHEME.WARNING, 5.0)
            case RAC3REGION.ARIDIA:
                if self.options.rangers == 0 or self.options.rangers == 2:
                    log_message = "You have disabled Story Ranger Missions in your YAML. "
                    notification_message = (f"You have disabled {RAC3TEXTFORMATSTRING.WHITE}Story Ranger Missions"
                                            f"{RAC3TEXTFORMATSTRING.NORMAL} in your YAML.\n")
                    if self.options.weapon_vendors:
                        log_message += "You can still buy the Qwack-O-Ray vendor check from the weapon vendor."
                        notification_message += (f"You can still buy the {RAC3TEXTFORMATSTRING.WHITE}Qwack-O-Ray"
                                                 f"{RAC3TEXTFORMATSTRING.NORMAL} vendor check\nfrom the weapon vendor.")
                    else:
                        log_message += "There are no locations on this planet."
                        notification_message += "There are no locations on this planet."
                    logger.info(log_message)
                    self.enqueue_notification(notification_message, RAC3BOXTHEME.WARNING, 5.0)
            case RAC3REGION.BLACKWATER_CITY:
                if self.options.rangers == 0 or self.options.rangers == 2:
                    log_message = ("You have disabled Story Ranger Missions in your YAML. There are no locations on "
                                   "this planet.")
                    notification_message = (f"You have disabled {RAC3TEXTFORMATSTRING.WHITE}Story "
                                            f"Ranger Missions{RAC3TEXTFORMATSTRING.NORMAL} in your YAML.\nThere are "
                                            f"no locations on this planet.")
                    logger.info(log_message)
                    self.enqueue_notification(notification_message, RAC3BOXTHEME.WARNING, 5.0)

    def speedup_unavailable_warning(self):
        """Checks if the player went to a planet/region where an enabled speedup can't apply yet and informs them"""
        match self.planet:
            case RAC3REGION.AQUATOS_BASE:
                if (self.options.speedups.get(RAC3SPEEDUPS.TYHRRAGUISE, False)
                    and not self.UnlockItem[RAC3ITEM.TYHRRA_GUISE]):
                    logger.info("The Tyhrra-Guise puzzles are not skipped automatically because you do not have the "
                                "Tyhrra-Guise yet.")
                    self.enqueue_notification(
                        f"The {RAC3TEXTFORMATSTRING.WHITE}Tyhrra-Guise{RAC3TEXTFORMATSTRING.NORMAL} puzzles are not "
                        f"skipped\nautomatically because you do not have\nthe "
                        f"{RAC3TEXTFORMATSTRING.WHITE}Tyhrra-Guise{RAC3TEXTFORMATSTRING.NORMAL} yet.",
                        RAC3BOXTHEME.WARNING,
                        5.0)

    ##################
    # Player Respawn #
    ##################

    def check_inputs(self, check: RAC3INPUT, pause_required: bool = False) -> bool:
        """Checks if the game is receiving a button combination, with optional pause check"""
        pause_check = self.pause_menu and not self.inputs & RAC3INPUT.START
        return (pause_check or not pause_required) and (self.inputs & check) == check

    def unpause_game(self):
        """Unpause the game if it is on the pause menu"""
        if self.pause_menu:
            self.write_input(RAC3INPUT.START)

    def write_input(self, button: RAC3INPUT):
        """Send the game button inputs"""
        left_shifted = (button & 0x00FF) << 8
        right_shifted = button >> 8
        bitmasked = RAC3INPUT.MASK ^ (left_shifted | right_shifted)
        self._write16(RAC3STATUS.WRITE_INPUT_1, bitmasked)
        self._write16(RAC3STATUS.WRITE_INPUT_2, bitmasked)

    def teleport_to_ship(self):
        """Handle respawning the player, to their ship if available, otherwise to the most recent checkpoint"""
        if self.should_overwrite_respawn():
            logger.debug(f"Player respawned on: {self.planet}")
            self.force_respawn(True)
        else:
            logger.debug(f"Player respawned at last checkpoint on: {self.planet}")
            self.force_respawn()

    def should_overwrite_respawn(self) -> bool:
        """Determine if the current respawn coordinates should be overwritten to the ship coordinates"""
        if self.player_type in {RAC3PLAYERTYPE.CLANK, RAC3PLAYERTYPE.GIANT, RAC3PLAYERTYPE.QWARK}:
            return False
        if self.current_game == RAC3VERSION.JP_ID and self.planet == RAC3REGION.HOLOSTAR_STUDIOS:
            # Entrance coordinates on JP are at the ship instead of clank's trailer
            return RAC3LOCATION.HOLOSTAR_RETURN_TO_SHIP in self.checked_locations
        match self.planet:
            case RAC3REGION.ZELDRIN_STARPORT:
                # Zeldrin: only one respawn point, that is right next to the ship, and we don't want anything to happen
                #          while aboard the leviathan
                return False
            case RAC3REGION.MARCADIA:
                return self._read32(RAC3STATUS.MARCADIA_SECTION) < 2  # 1: Main, 2: Rangers, 3: LDF
            case _:
                return True

    def force_respawn(self, ship: bool | None = None):
        """Force the game to reload the current planet, respawning the player"""
        self.self_respawning = True
        if ship:
            self._write8(RAC3STATUS.FORCE_RELOAD, 2)
        else:
            self._write8(RAC3STATUS.FORCE_RELOAD, 1)

    def check_intro(self) -> bool:
        """Checks if the player has reached the end of the intro by collecting the phoenix coordinates"""
        if not self._read8(RAC3_REGION_DATA_TABLE[RAC3REGION.STARSHIP_PHOENIX].VISIT_ADDRESS):
            return True
        return False

    ###################
    # Vendor Handling #
    ###################

    def vendor_update(self):
        """Read current vendor inventory and replace all items after the all ammo item with all items in the game"""
        # Only update vendor if on a known planet with a vendor
        if self.planet not in PLANET_VENDOR_OFFSET.keys() or self.vendor_type is None:
            return

        if self.options.armor_vendor and self.planet in (RAC3REGION.STARSHIP_PHOENIX, RAC3REGION.PHOENIX_ASSAULT):
            new_armor = self._read32(
                RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.NEW_ARMOR_OFFSET, self.current_game))
            if 0 < new_armor < 5:
                self._write8(RAC3INSTRUCTION.CODECAVE_START + new_armor, 1)
                if new_armor == 4:
                    self._write8(0x001D54B4, 1)  # Infernox skill point

        is_pda_vendor = self._read8(
            RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.IS_PDA_OFFSET, self.current_game))
        if is_pda_vendor:
            return

        new_inventory = []
        match self.vendor_type:
            case RAC3VENDORTYPE.WEAPON:
                # Clear pending item if it is a locked weapon, so they don't equip it
                pending_item = self._read8(RAC3STATUS.PENDING_ITEM)
                if (pending_item and
                    pending_item in ITEM_NAME_FROM_ID and
                    ITEM_NAME_FROM_ID[pending_item] in non_prog_weapon_data and
                    self.UnlockItem[ITEM_NAME_FROM_ID[pending_item]] == 0):
                    self._write8(RAC3STATUS.PENDING_ITEM, 0)

                progressive_weapons_mode = self.options.progressive_weapons
                if self.options.weapon_level_locations and progressive_weapons_mode == 2:
                    progressive_weapons_mode = 1  # Force manual leveling if weapon level locations are enabled
                should_add_ngplus_items = (self.options.ngplus_items and progressive_weapons_mode < 2)
                if not self.options.weapon_vendors and not should_add_ngplus_items:
                    return
                is_slimcognito = (self.planet == RAC3REGION.AQUATOS
                                  and bool(self._read8(RAC3WEAPONVENDOR.get_vendor_property_address(
                        self.planet, RAC3WEAPONVENDOR.VENDOR_WEAPON_TYPE_OFFSET))))
                randomized_items = [item for item in self.weapon_vendor_items
                                    if (item in MEGACORP_WEAPONS) == is_slimcognito]

                # Slim Cognito does not have a max ammo item, so we just replace the entire inventory
                if is_slimcognito:
                    new_inventory.extend(
                        RAC3WEAPONVENDORSLOTDATA(RAC3_ITEM_DATA_TABLE[item].ID) for item in randomized_items)
                else:
                    # Only show gadgetron weapons, keep current inventory up to all_ammo
                    vendor_size = self._read32(RAC3VENDOR.get_vendor_property_address(
                        self.planet, RAC3VENDOR.SLOT_COUNT_OFFSET, self.current_game))
                    found_all_ammo = False
                    for slot_data in [self.read_weapon_vendor_slot_data(slot) for slot in range(vendor_size)]:
                        # Remove ammo for weapons we don't have unlocked yet
                        weapon = ITEM_NAME_FROM_ID.get(slot_data.item_id.value, None)
                        if weapon is not None and weapon in non_prog_weapon_data:
                            if self.UnlockItem[weapon] == 0:
                                continue

                        new_inventory.append(slot_data)
                        if slot_data.all_ammo.value:
                            found_all_ammo = True
                            break
                    # Fallback in case the all ammo is missing
                    if not found_all_ammo:
                        new_inventory = [RAC3WEAPONVENDORSLOTDATA(all_ammo=1)]
                    if self.options.weapon_vendors:
                        new_inventory.extend(RAC3WEAPONVENDORSLOTDATA(RAC3_ITEM_DATA_TABLE[item].ID)
                                             for item in randomized_items)
                    if should_add_ngplus_items:
                        new_inventory.extend([RAC3WEAPONVENDORSLOTDATA(RAC3_ITEM_DATA_TABLE[item].ID, mega=1)
                                              for item in self.omega_weapon_vendors_items])
                if self.planet == RAC3REGION.STARSHIP_PHOENIX or is_slimcognito:
                    # add memory card item
                    new_inventory.append(RAC3WEAPONVENDORSLOTDATA(memcard=1))
                if self.options.weapon_vendors:
                    self.overwrite_vendor_item_names(randomized_items, ITEM_TO_WEAPON_VENDOR_LOCATION)
            case RAC3VENDORTYPE.ARMOR:
                if not self.options.armor_vendor:
                    return
                new_inventory = [ARMOR_VENDOR_INVENTORY[ITEM_TO_ARMOR_VENDOR_LOCATION[item]] for item in
                                 self.armor_vendor_items]
                self.overwrite_vendor_item_names(self.armor_vendor_items, ITEM_TO_ARMOR_VENDOR_LOCATION)
            case RAC3VENDORTYPE.SHIP:
                if not self.options.ship_vendor:
                    return
                ship_keys = list(SHIP_VENDOR_INVENTORY.keys())[:(self.UnlockItem[RAC3SHIPSLOT.SLOT_0] + 1) * 2]
                # Set item_name_ptr for each ship item using the string pointer
                for key in ship_keys:
                    addr = self.vendor_string_pointers.get(key, 0)
                    SHIP_VENDOR_INVENTORY[key].item_name_ptr.value = addr
                filtered_ship_items = [SHIP_VENDOR_INVENTORY[key] for key in ship_keys if
                                       key not in self.checked_locations]
                new_inventory = filtered_ship_items
                # Undo the cosmetic overwrite from buying ship vendor items
                self.add_cosmetics()
            case _:
                logger.debug(f"Vendor cycler does not support vendor type {self.vendor_type} yet")
                return
        self.write_vendor_inventory(new_inventory, self.vendor_type)
        if len(new_inventory) == 0:
            self._write32(
                RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.CURSOR_OFFSET, self.current_game), 0)
        elif self.vendor_cursor_pos >= len(new_inventory):
            self._write32(RAC3VENDOR.get_vendor_property_address(
                self.planet, RAC3VENDOR.CURSOR_OFFSET, self.current_game), len(new_inventory) - 1)

    def read_weapon_vendor_slot_data(self, slot: int) -> RAC3WEAPONVENDORSLOTDATA:
        """Returns the data for a given slot in the vendor inventory"""
        self._read32(
            RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.VENDOR_TYPE_OFFSET, self.current_game))
        return RAC3WEAPONVENDORSLOTDATA(*[self.read_vendor_prop(prop, slot, RAC3VENDORTYPE.WEAPON) for prop in
                                          RAC3WEAPONVENDORSLOTDATA().get_data()])

    def read_armor_vendor_slot_data(self, slot: int) -> RAC3ARMORVENDORSLOTDATA:
        """Returns the data for a given slot in the vendor inventory"""
        self._read32(
            RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.VENDOR_TYPE_OFFSET, self.current_game))
        return RAC3ARMORVENDORSLOTDATA(
            *[self.read_vendor_prop(prop, slot, RAC3VENDORTYPE.ARMOR) for prop in RAC3ARMORVENDORSLOTDATA().get_data()])

    def read_ship_vendor_slot_data(self, slot: int) -> RAC3SHIPVENDORSLOTDATA:
        """Returns the data for a given slot in the vendor inventory"""
        self._read32(
            RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.VENDOR_TYPE_OFFSET, self.current_game))
        return RAC3SHIPVENDORSLOTDATA(
            *[self.read_vendor_prop(prop, slot, RAC3VENDORTYPE.SHIP) for prop in RAC3SHIPVENDORSLOTDATA().get_data()])

    def read_skin_vendor_slot_data(self, slot: int) -> RAC3SKINVENDORSLOTDATA:
        """Returns the data for a given slot in the vendor inventory"""
        self._read32(
            RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.VENDOR_TYPE_OFFSET, self.current_game))
        return RAC3SKINVENDORSLOTDATA(
            *[self.read_vendor_prop(prop, slot, RAC3VENDORTYPE.SKIN) for prop in RAC3SKINVENDORSLOTDATA().get_data()])

    def read_vendor_prop(self, prop: RAC3VENDORSLOTDATA.Property, slot: int, vendor_type: RAC3VENDORTYPE) -> int:
        """Reads the value of a vendor slot property"""
        match prop.size:
            case 1:
                return self._read8(RAC3VENDOR.get_vendor_item_property_address(
                    self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type], self.current_game))
            case 2:
                return self._read16(RAC3VENDOR.get_vendor_item_property_address(
                    self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type], self.current_game))
            case 4:
                return self._read32(RAC3VENDOR.get_vendor_item_property_address(
                    self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type], self.current_game))
            case _:
                raise ValueError(f"Invalid property size: {prop.size} Bytes")

    def write_vendor_inventory(self, inventory: list[RAC3VENDORSLOTDATA], vendor_type: RAC3VENDORTYPE):
        """Write a list of vendor slot data objects to the current planet's vendor inventory"""
        self._write32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.SLOT_COUNT_OFFSET,
                                                             self.current_game), len(inventory))
        if len(inventory) == 0:
            start_address = RAC3VENDOR.get_vendor_property_address(self.planet, 0, self.current_game)
            match vendor_type:
                case RAC3VENDORTYPE.SHIP:
                    # change the string pointer to no items available message in code cave
                    item_name_addr = start_address + RAC3SHIPVENDOR.ITEM_NAME_PTR_OFFSET
                    already_equipped_addr = start_address + RAC3SHIPVENDOR.ITEM_IS_EQUIPPED_OFFSET
                    string_key = (RAC3VENDOR.ALL_ITEMS_SOLD_OUT_LOC_KEY
                                  if self.has_checked_all_locations_with_tag(RAC3TAG.SHIP)
                                  else RAC3VENDOR.NO_ITEMS_AVAILABLE_LOC_KEY)
                    # self._write32(item_name_addr, self.vendor_string_pointers[string_key])
                    # self._write32(already_equipped_addr, 1)
                    self._write32(item_name_addr, self.vendor_string_pointers[string_key])
                    self._write32(already_equipped_addr, 1)
                case _:
                    # clear out vendor slot memory
                    slot_size = VENDORTYPE_TO_SLOT_SIZE[vendor_type]
                    self._write_bytes(start_address, bytes(slot_size * 5))

        for slot, slot_data in enumerate(inventory):
            for prop in slot_data.get_data():
                match prop.size:
                    case 1:
                        self._write8(RAC3VENDOR.get_vendor_item_property_address(
                            self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type], self.current_game),
                            prop.value)
                    case 2:
                        self._write16(RAC3VENDOR.get_vendor_item_property_address(
                            self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type], self.current_game),
                            prop.value)
                    case 4:
                        self._write32(RAC3VENDOR.get_vendor_item_property_address(
                            self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type], self.current_game),
                            prop.value)
        logger.debug(f"Wrote {len(inventory)} items to {vendor_type.name} vendor on planet {self.planet}")

    def hovering_over_ammo(self) -> bool:
        """Check if the player is hovering over the max ammo item in a weapon vendor"""
        if self.vendor_type != RAC3VENDORTYPE.WEAPON:
            return False
        if self.read_weapon_vendor_slot_data(self.vendor_cursor_pos).ammo_text.value:
            return True
        return False

    def hovering_over_mega(self) -> bool:
        """Check if the player is hovering over the mega item in a weapon vendor"""
        if self.vendor_type != RAC3VENDORTYPE.WEAPON:
            return False
        if self.read_weapon_vendor_slot_data(self.vendor_cursor_pos).mega.value:
            return True
        return False

    def invalidate_string_table_cache(self):
        """Discard string table state and queued writes."""
        for patch in self.vendor_name_patches.values():
            self.write_batcher.pop((patch.address, self.DataType.INT32), None)
        self.vendor_name_patches = {}
        self.vendor_name_table = None
        self.vendor_name_restore_pending = False
        self.string_entries = {}
        self.string_table = None

    def get_string_table(self) -> StringTable | None:
        if (self.planet not in PLANET_LOAD_OFFSET or self.between_planets or self.is_reloading
            or self.game_state_value == RAC3GAMESTATE.PLANET_CHANGE):
            return None
        base = self._read32(PLANET_LOAD_OFFSET[self.planet] + RAC3STATUS.PLANET_STRING_TABLE_BASE)
        if not 0 < base <= 0x02000000 - StringTableEntry.SIZE or base % StringTableEntry.SIZE:
            return None
        first = self.read_string_entries([base])[0]
        # In a loaded level text asset, the ID 0 string starts just after the last entry.
        first_text = first.text_pointer
        count, remainder = divmod(first_text - base, StringTableEntry.SIZE)
        if first.text_id != 0 or remainder or not 0 < count <= StringTable.MAX_ENTRIES or first_text >= 0x02000000:
            return None
        return StringTable(
            game_id=self.current_game,
            planet=self.planet,
            base_address=base,
            first_text_address=first_text,
        )

    def read_string_entries(self, addresses: list[int]) -> list[StringTableEntry]:
        """Read the requested rows from the string table."""
        if not addresses:
            return []
        start = min(addresses)
        end = max(addresses) + StringTableEntry.SIZE
        data = self._read_bytes(start, end - start, should_convert=False)
        return [StringTableEntry.from_bytes(data, address - start) for address in addresses]

    def find_string_by_id(self, text_id: int) -> int | None:
        """Return the string pointer for the given string ID."""
        return self.find_strings_by_id((text_id,)).get(text_id)

    def find_strings_by_id(self, text_ids: Iterable[int]) -> dict[int, int]:
        """Find text entries with one table scan per loaded table. Returns a dict of string id to string pointer."""
        table = self.get_string_table()
        if table is None:
            return {}
        if table != self.string_table:
            addresses = list(range(table.base_address, table.first_text_address, StringTableEntry.SIZE))
            entries = {}
            for address, entry in zip(addresses, self.read_string_entries(addresses)):
                # The game's lookup uses the first entry when an ID occurs twice.
                entries.setdefault(entry.text_id, address)
            self.string_entries = entries
            self.string_table = table
        return {text_id: self.string_entries[text_id] for text_id in text_ids if text_id in self.string_entries}

    def get_galactic_map_objective(self, rows_base: int) -> tuple[int, int] | None:
        """Return the live text box state and the row it currently displays."""

        def valid_pointer(address: int, size: int) -> bool:
            return 0 < address <= 0x02000000 - size and address % 4 == 0

        manager = self._read32(RAC3GALACTICMAP.get_ui_manager_state_address(self.planet))
        if not valid_pointer(manager, RAC3GALACTICMAP.ACTIVE_CONTEXT_INDEX_OFFSET + 4):
            return None
        context_index = self._read32(manager + RAC3GALACTICMAP.ACTIVE_CONTEXT_INDEX_OFFSET, should_convert=False)
        if context_index >= RAC3GALACTICMAP.CONTEXT_COUNT:
            return None
        context = self._read32(manager + context_index * 4, should_convert=False)
        if not valid_pointer(context, 4):
            return None
        context_data = self._read32(context, should_convert=False)
        capacity = RAC3GALACTICMAP.WIDGET_REGISTRY_CAPACITY
        if not valid_pointer(context_data, RAC3GALACTICMAP.WIDGET_REGISTRY_SLOTS_OFFSET + capacity * 8):
            return None
        slots = context_data + RAC3GALACTICMAP.WIDGET_REGISTRY_SLOTS_OFFSET
        widget_id = RAC3GALACTICMAP.OBJECTIVE_WIDGET_ID
        step = widget_id % (capacity - 1) + 1
        for probe in range(capacity):
            slot = slots + ((widget_id + probe * step) % capacity) * 8
            key, widget = self._read32_batch([slot, slot + 4], should_convert=False)
            if not widget:
                break
            if key != widget_id or not valid_pointer(widget, RAC3GALACTICMAP.TEXT_BOX_STATE_OFFSET + 4):
                continue
            state = self._read32(widget + RAC3GALACTICMAP.TEXT_BOX_STATE_OFFSET, should_convert=False)
            if not valid_pointer(state, RAC3GALACTICMAP.TEXT_SCALE_OFFSET + 4):
                continue
            primary = self._read32(state + RAC3GALACTICMAP.PRIMARY_TEXT_OFFSET, should_convert=False)
            # Also rejects removed registry entries and the initial scratch text before the map binds a row.
            row_offset = primary - RAC3GALACTICMAP.OBJECTIVE_OFFSET - rows_base
            if 0 <= row_offset < RAC3GALACTICMAP.MAX_ROWS * RAC3GALACTICMAP.ROW_SIZE and row_offset % RAC3GALACTICMAP.ROW_SIZE == 0:
                return state, rows_base + row_offset
        return None

    def galactic_map_uses_code_cave(self) -> bool:
        """Check whether repacking would invalidate the map's live text pointer list."""
        if self.game_state_value != RAC3GAMESTATE.PAUSED:
            return False
        base = RAC3GALACTICMAP.get_rows_address(self.planet)
        if base is None:
            return False
        objective = self.get_galactic_map_objective(self.address_convert(base))
        if objective is None:
            return False
        state, _ = objective
        alternate, count_and_highlight = self._read32_batch(
            [state + RAC3GALACTICMAP.ALTERNATE_TEXT_OFFSET, state + RAC3GALACTICMAP.ALTERNATE_COUNT_OFFSET],
            should_convert=False)
        return (bool(count_and_highlight & 0xFFFF)
                and RAC3INSTRUCTION.CODECAVE_START <= alternate < RAC3INSTRUCTION.CODECAVE_END)

    def overwrite_planet_location_counts(self, server_locations: set[int], checked_locations: set[int]):
        """Show enabled location progress in the Galactic Map's alternate text source."""
        if self.between_planets or self.is_reloading or self.game_state_value != RAC3GAMESTATE.PAUSED:
            return
        pointer_list = self.galactic_map_text_pointer_list
        if not pointer_list:
            return
        base = RAC3GALACTICMAP.get_rows_address(self.planet)
        if base is None:
            return
        objective = self.get_galactic_map_objective(self.address_convert(base))
        if objective is None:
            return
        state, row_address = objective
        scale_address = state + RAC3GALACTICMAP.TEXT_SCALE_OFFSET
        alternate, count_and_highlight = self._read32_batch(
            [state + RAC3GALACTICMAP.ALTERNATE_TEXT_OFFSET, state + RAC3GALACTICMAP.ALTERNATE_COUNT_OFFSET],
            should_convert=False)
        count = count_and_highlight & 0xFFFF
        if count and (alternate != pointer_list or count != 1):
            return

        row = self._read_bytes(row_address, 5, should_convert=False)
        region = PLANET_NAME_FROM_ID.get(int.from_bytes(row[:4], "little"))
        text = b"\x00"
        text_scale = RAC3GALACTICMAP.DEFAULT_TEXT_SCALE
        if region in INFOBOT_FROM_PLANET and row[4] == 1:
            display, scale = self.format_galactic_map_counts(region, server_locations, checked_locations)
            encoded = display.encode("ascii") + b"\x00"
            if len(encoded) <= RAC3GALACTICMAP.TEXT_BUFFER_SIZE:
                text = encoded
                text_scale = scale

        if self._read32(state + RAC3GALACTICMAP.PRIMARY_TEXT_OFFSET, should_convert=False) != row_address + RAC3GALACTICMAP.OBJECTIVE_OFFSET:
            return
        current_scale = self._read_float(scale_address, should_convert=False)
        # Allow for the rounding of a 32-bit float in EE memory.
        if not isclose(current_scale, text_scale, rel_tol=1e-7):
            self._write_float(scale_address, text_scale, should_convert=False)
        first = pointer_list + RAC3GALACTICMAP.TEXT_BUFFER_OFFSET
        second = first + RAC3GALACTICMAP.TEXT_BUFFER_SIZE
        active_buffer = self._read32(pointer_list, should_convert=False) if count else 0
        if (active_buffer not in (first, second)
            or self._read_bytes(active_buffer, len(text), should_convert=False) != text):
            target = second if active_buffer == first else first
            # Publish the pointer only once the buffer is ready, in the existing ordered write batch.
            self._write_bytes(target, text, should_convert=False)
            self._write32(pointer_list, target, should_convert=False)
        if not count:
            self._write32(state + RAC3GALACTICMAP.ALTERNATE_TEXT_OFFSET, pointer_list, should_convert=False)
            self._write16(state + RAC3GALACTICMAP.ALTERNATE_HIGHLIGHT_OFFSET, 0xFFFF, should_convert=False)
            self._write16(state + RAC3GALACTICMAP.ALTERNATE_COUNT_OFFSET, 1, should_convert=False)

    def format_galactic_map_counts(self, region: str, server_locations: set[int],
                                   checked_locations: set[int]) -> tuple[str, float]:
        """Build the destination's progress text and its font scale."""
        counts: dict[str, tuple[int, int]] = {}
        for ap_code in server_locations:
            name = LOCATION_FROM_AP_CODE.get(ap_code)
            if name is None:
                continue
            location = RAC3_LOCATION_DATA_TABLE[name]
            if RAC3TAG.GOAL in location.TAGS:
                continue
            if MAP_LOCATION_REGION_OVERRIDES.get(name, location.REGION) != region:
                continue
            if name in VENDOR_LOCATIONS:
                group = RAC3LOCATIONGROUP.VENDOR
            elif RAC3TAG.SKILLPOINT in location.TAGS:
                group = RAC3LOCATIONGROUP.SKILL_POINTS
            elif name in STORY_LOCATIONS or RAC3TAG.INFOBOT in location.TAGS:
                group = RAC3LOCATIONGROUP.STORY
            elif name in GAUNTLET_LOCATIONS:
                group = RAC3LOCATIONGROUP.GAUNTLET
            else:
                group = RAC3LOCATIONGROUP.OTHER
                for label in SEPARATE_GROUPS.get(region, DEFAULT_GROUPS):
                    if GROUP_TAGS.get(label) in location.TAGS:
                        group = label
                        break
                if (group not in (RAC3LOCATIONGROUP.VR, RAC3LOCATIONGROUP.VID_COMICS, RAC3LOCATIONGROUP.ARENA)
                    and (name in GADGET_PICKUP_LOCATIONS or RAC3TAG.T_BOLT in location.TAGS
                         or RAC3TAG.TROPHY in location.TAGS)):
                    group = RAC3LOCATIONGROUP.COLLECTIBLES
            checked, total = counts.get(group, (0, 0))
            collected = ap_code in checked_locations or name in self.checked_locations
            counts[group] = (checked + int(collected), total + 1)

        checked, total = 0, 0
        secondary_counts = []
        for group in (RAC3LOCATIONGROUP.STORY, *SEPARATE_GROUPS.get(region, DEFAULT_GROUPS), *COMMON_GROUPS,
                      RAC3LOCATIONGROUP.OTHER):
            group_checked, group_total = counts.get(group, (0, 0))
            checked += group_checked
            total += group_total
            if group_total:
                secondary_counts.append((group, group_checked, group_total))
        return format_planet_location_counts(checked, total, secondary_counts)

    def overwrite_challenge_descriptions(self):
        """Overwrite challenge description strings with the archipelago item names."""
        if self.between_planets:
            return

        replacements = {
            text_id: self.challenge_string_pointers[location.NAME]
            for location in get_challenge_locations(self.planet)
            if location.NAME in self.challenge_string_pointers
            for text_id in location.DESCRIPTION_TEXT_IDS
        }
        if not replacements:
            return

        rows = self.find_strings_by_id(replacements)
        table = self.string_table
        if not rows or table is None:
            return

        descriptors = {text_id: self.challenge_description_descriptor(text_id) for text_id in rows}
        addresses = list(rows.values())
        for descriptor in descriptors.values():
            if descriptor is not None:
                name_address, _, _ = descriptor
                addresses.extend((name_address, name_address + 4))
        # The game can restore the original pointers at the same string table address.
        live = dict(zip(addresses, self._read32_batch(addresses, should_convert=False)))
        writes = {}
        for text_id, row in rows.items():
            descriptor = descriptors[text_id]
            if descriptor is not None:
                name_address, title_id, original_id = descriptor
                description_address = name_address + 4
                if live[name_address] != title_id or live[description_address] not in (original_id, text_id):
                    continue
            if live[row] != replacements[text_id]:
                writes[row] = replacements[text_id]
            if descriptor is not None and live[description_address] != text_id:
                writes[description_address] = text_id

        if writes and self.get_string_table() == table:
            for address, value in writes.items():
                self._write32(address, value, should_convert=False)

    def challenge_description_descriptor(self, text_id: int) -> tuple[int, int, int] | None:
        """Return the name field and the expected title and description IDs."""
        if self.planet == RAC3REGION.STARSHIP_PHOENIX and text_id == VR_TRAINING_DESCRIPTION:
            return VR_TRAINING_NAME_ADDRESS[self.current_game], VR_TRAINING_NAME, VR_TRAINING_NAME
        if self.planet == RAC3REGION.ANNIHILATION_NATION and text_id in GAUNTLET_DESCRIPTORS:
            index, title = GAUNTLET_DESCRIPTORS[text_id]
            address = NATION_CHALLENGE_TABLE[self.current_game] + index * NATION_CHALLENGE_SIZE
            return address, title, GAUNTLET_DESCRIPTION
        return None

    def overwrite_pda_vendor_prompts(self):
        """Show the randomized reward in both PDA vendor prompts on Qwark's Hideout."""
        if self.planet != RAC3REGION.QWARKS_HIDEOUT:
            return

        replacements = {
            text_id: self.address_convert(self.vendor_string_pointers[key])
            for text_id, key in (
                (RAC3VENDOR.PDA_PURCHASE_PROMPT_TEXT_ID, RAC3LOCATION.HIDEOUT_PDA),
                (RAC3VENDOR.PDA_INSUFFICIENT_BOLTS_TEXT_ID, RAC3VENDOR.PDA_INSUFFICIENT_BOLTS_KEY),
            )
            if key in self.vendor_string_pointers
        }
        if not replacements:
            return

        for text_id, row in self.find_strings_by_id(replacements).items():
            pointer = replacements[text_id]
            if self._read32(row, should_convert=False) != pointer:
                self._write32(row, pointer, should_convert=False)

    def overwrite_vendor_item_names(self, items: list[str], locations: dict[str, str]):
        """Overwrite string pointers of item names to the code cave strings."""
        replacements = {}
        for item in items:
            text_id = VENDOR_ITEM_NAME_TEXT_IDS.get(item)
            replacement = self.vendor_string_pointers.get(locations.get(item, ""), 0)
            if text_id is not None and text_id not in self.vendor_name_patches and replacement:
                replacements[text_id] = self.address_convert(replacement)
        if not replacements:
            return

        entries = self.find_strings_by_id(replacements)
        table = self.string_table
        if not entries or table is None or (self.vendor_name_patches and table != self.vendor_name_table):
            return
        self.vendor_name_patches = self.vendor_name_patches.copy()
        for (text_id, address), entry in zip(entries.items(), self.read_string_entries(list(entries.values()))):
            pointer = entry.text_pointer
            # The original string is in the text asset. A code cave string pointer isn't a backup.
            if entry.text_id != text_id or not table.first_text_address <= pointer < 0x02000000:
                continue
            replacement = replacements[text_id]
            self.vendor_name_table = table
            self.vendor_name_patches[text_id] = VendorNamePatch(address, pointer, replacement)
            self._write32(address, replacement, should_convert=False)

    def get_vendor_apcodes(self) -> list | None:
        """Returns a list of apcodes for the open vendor. Returns None if no vendor is open"""

        if self.game_state_value != RAC3GAMESTATE.VENDOR or not self.options.scout_vendors:
            return None

        vendor_type = self.vendor_type
        vendor_location_apcodes = []
        match vendor_type:
            case RAC3VENDORTYPE.WEAPON:
                if not self.options.weapon_vendors or not self.options.scout_vendors.get(RAC3VENDORNAME.WEAPON, False):
                    return None
                vendor_items = self.weapon_vendor_items
                is_slimcognito = (self.planet == RAC3REGION.AQUATOS and bool(self._read8(
                    RAC3VENDOR.get_vendor_property_address(self.planet, RAC3WEAPONVENDOR.VENDOR_WEAPON_TYPE_OFFSET))))
                if is_slimcognito:  # Only hint Megacorp weapons
                    filtered_items = [item for item in vendor_items if item in MEGACORP_WEAPONS]
                else:  # Only hint Gadgetron weapons
                    filtered_items = [item for item in vendor_items if item not in MEGACORP_WEAPONS]

                vendor_locations = [ITEM_TO_WEAPON_VENDOR_LOCATION[item] for item in filtered_items if
                                    item in ITEM_TO_WEAPON_VENDOR_LOCATION]
                vendor_location_apcodes = [RAC3_LOCATION_DATA_TABLE[loc].AP_CODE for loc in vendor_locations]
            case RAC3VENDORTYPE.ARMOR:
                if not self.options.armor_vendor or not self.options.scout_vendors.get(RAC3VENDORNAME.ARMOR, False):
                    return None

                armor_items = self.armor_vendor_items
                vendor_locations = [ITEM_TO_ARMOR_VENDOR_LOCATION[item] for item in armor_items if
                                    item in ITEM_TO_ARMOR_VENDOR_LOCATION]
                vendor_location_apcodes = [RAC3_LOCATION_DATA_TABLE[loc].AP_CODE for loc in vendor_locations]
            case RAC3VENDORTYPE.SHIP:
                if not self.options.ship_vendor or not self.options.scout_vendors.get(RAC3VENDORNAME.SHIP, False):
                    return None
                ship_keys = list(SHIP_VENDOR_INVENTORY.keys())[:(self.UnlockItem[RAC3SHIPSLOT.SLOT_0] + 1) * 2]
                filtered_ship_keys = [key for key in ship_keys if key not in self.checked_locations]
                vendor_location_apcodes = [RAC3_LOCATION_DATA_TABLE[key].AP_CODE for key in filtered_ship_keys]

        return vendor_location_apcodes

    ##################
    # Sequence Break #
    ##################

    def sequence_break(self) -> None:
        """Checks the current planet and unsets any planet access flags that would interfere with location collecting"""
        infobot_location = REGION_TO_INFOBOT_LOCATION.get(self.planet, None)
        if infobot_location is not None and infobot_location in LOCATION_TO_INFOBOT_FLAG:
            infobot_flag = LOCATION_TO_INFOBOT_FLAG[infobot_location]
            if (infobot_flag is not None
                and infobot_location not in self.checked_locations
                and infobot_flag != RAC3STATUS.ALLOW_SHIP):
                self._write8(infobot_flag, 0)
        if self.new_planet:
            if self.planet == RAC3REGION.STARSHIP_PHOENIX:
                # Fix can't play Qwark VidComics in some case which first event is skipped
                self._write8(0x001426E8, 1)  # Todo: Take Qwark to Cage Mission

                # Failsafe for return to phoenix after grand prize bout
                if RAC3LOCATION.NATION_GRAND_PRIZE_BOUT in self.checked_locations:
                    self._write8(0x0014276F, 1)

            if self.planet != RAC3REGION.ZELDRIN_STARPORT and not self._read8(RAC3STATUS.ZELDRIN_END_LEVIATHAN):
                self._write8(RAC3STATUS.ZELDRIN_START_LEVIATHAN, 0)

    ##################
    # End of Main Loop #
    ##################

    def late_update(self):
        """Ran at the end of the main loop to update any memory values based on collection state"""
        self.gadget_cycler()
        self.planet_cycler()
        self.phoenix_transporter_cycler()
        self.weapon_cycler()
        self.weapon_mod_cycler()
        self.wrench_cycler()
        self.vidcomic_cycler()
        self.vidcomic_health_cycler()
        self.armor_cycler()
        self.timer_cycler()
        self.cheat_cycler()
        self.weapon_exp_cycler()
        self.verify_quick_select_and_last_used()
        self.clank_cycler()
        self.multiplier_cycler()
        self.challenge_mode_cycler()
        self.patch_cycler()
        self.overflow_fix()
        self.process_delayed_things_cycler()
        self.health_cycler()
        self.shortcut_cycler()
        self.speedup_cycler()
        self.pda_vendor_cycler()
        self.notification_cycler()

    def gadget_cycler(self):
        """Cycles through each gadget and updates their state"""
        if not self.should_cycle_gadgets() or self.near_pda_vendor():
            self.respawn_gadgets()
            return

        for name in gadget_data.keys():
            addr = gadget_data[name].UNLOCK_ADDRESS
            self._write8(addr, 1 if self.UnlockItem[name] else 0)

    def should_cycle_gadgets(self) -> bool:
        """Check if it's safe to cycle gadgets used to ensure gadgets can respawn without the cycler interfering"""
        if self.between_planets:
            return False
        current_time = time.time()
        if self.is_reloading or self.self_respawning or self.action_type == RAC3ACTIONTYPE.PLAYER_MOVEMENT_LOCKED:
            self.gadget_grace_period = current_time
        if current_time - self.gadget_grace_period < 0.75:
            return False
        return True

    def near_pda_vendor(self) -> bool:
        """Check if we are near the PDA Vendor"""
        if self.planet == RAC3REGION.QWARKS_HIDEOUT and self.distance_to_moby_squared(self.pda_vendor) < 225.0:  # 15^2
            # In case the PDA vendor bugs out and doesn't play the cutscene
            if (self._read32(PLANET_LOAD_OFFSET[
                                 self.planet] + RAC3STATUS.PLANET_BOLT_DIFFERENCE_BASE) & 0x80000000  # ie is negative
                and self.action_type != RAC3ACTIONTYPE.PLAYER_MOVEMENT_LOCKED):
                self._write8(gadget_data[RAC3ITEM.PDA].UNLOCK_ADDRESS_2, 1)
            return True
        return False

    def distance_to_moby(self, moby: int) -> float:
        """Calculate the distance from the player to the moby"""
        if self.between_planets or not moby:
            return float("inf")
        player_pos = self.player_pos
        moby_pos = RAC3POSITIONDATA(
            self._read_float(moby + 0x10),
            self._read_float(moby + 0x14),
            self._read_float(moby + 0x18))
        distance = ((player_pos.X - moby_pos.X) ** 2 +
                    (player_pos.Y - moby_pos.Y) ** 2 +
                    (player_pos.Z - moby_pos.Z) ** 2) ** 0.5
        return distance

    def distance_to_moby_squared(self, moby: int) -> float:
        """Calculate the squared distance from the player to the moby"""
        if self.between_planets or not moby:
            return float("inf")
        player_pos = self.player_pos
        moby_pos = RAC3POSITIONDATA(
            self._read_float(moby + 0x10),
            self._read_float(moby + 0x14),
            self._read_float(moby + 0x18))
        distance_squared = ((player_pos.X - moby_pos.X) ** 2 +
                            (player_pos.Y - moby_pos.Y) ** 2 +
                            (player_pos.Z - moby_pos.Z) ** 2)
        return distance_squared

    @deprecated("Unused")
    def get_checked_locations_by_tag(self, tag: str) -> list[str]:
        """Get a list of checked locations that match the given tag"""
        return [loc for loc in self.checked_locations if tag in RAC3_LOCATION_DATA_TABLE[loc].TAGS]

    def has_checked_all_locations_with_tag(self, tag: str) -> bool:
        """Check if all locations with the given tag have been checked"""
        for loc in RAC3_LOCATION_DATA_TABLE.keys():
            if tag in RAC3_LOCATION_DATA_TABLE[loc].TAGS and loc not in self.checked_locations:
                return False
        return True

    def respawn_gadgets(self):
        """Respawn gadget if the associated location isn't checked but the gadget is unlocked through AP"""
        if (self.UnlockItem[RAC3ITEM.REFRACTOR]
            and RAC3LOCATION.MARCADIA_REFRACTOR not in self.checked_locations
            and self.planet == RAC3REGION.MARCADIA):
            self._write8(gadget_data[RAC3ITEM.REFRACTOR].UNLOCK_ADDRESS, 0)

        if (self.UnlockItem[RAC3ITEM.CHARGE_BOOTS]
            and RAC3LOCATION.DAXX_CHARGE_BOOTS not in self.checked_locations
            and self.planet == RAC3REGION.DAXX):
            self._write8(gadget_data[RAC3ITEM.CHARGE_BOOTS].UNLOCK_ADDRESS, 0)

        if (self.UnlockItem[RAC3ITEM.NANO_PAK]
            and RAC3LOCATION.CRASH_SITE_NANO_PAK not in self.checked_locations
            and self.planet == RAC3REGION.CRASH_SITE):
            self._write8(gadget_data[RAC3ITEM.NANO_PAK].UNLOCK_ADDRESS, 0)

        if ((self.UnlockItem[RAC3ITEM.BOLT_GRABBER] or self.UnlockItem[RAC3ITEM.BOX_BREAKER])
            and RAC3LOCATION.ZELDRIN_STARPORT_BOLT_GRABBER not in self.checked_locations
            and self.planet == RAC3REGION.ZELDRIN_STARPORT):
            self._write8(gadget_data[RAC3ITEM.BOLT_GRABBER].UNLOCK_ADDRESS, 0)
            self._write8(gadget_data[RAC3ITEM.BOX_BREAKER].UNLOCK_ADDRESS, 0)
        if (self.UnlockItem[RAC3ITEM.PDA]
            and RAC3LOCATION.HIDEOUT_PDA not in self.checked_locations
            and self.planet == RAC3REGION.QWARKS_HIDEOUT):
            self._write8(gadget_data[RAC3ITEM.PDA].UNLOCK_ADDRESS, 0)

    def planet_cycler(self):
        """Handles unlocking planets if their "infobot" has been collected"""
        for name in infobot_data.keys():
            planet = RAC3_REGION_DATA_TABLE[PLANET_FROM_INFOBOT[name]]
            if self.UnlockItem[name]:
                addr = RAC3_SHIP_DATA_TABLE[SHIP_SLOTS[self.UnlockItem[name] - 1]].SLOT_ADDRESS
                self._write8(addr, planet.ID)
        for number, slot in enumerate(SHIP_SLOTS):
            self.ship_slot_limit = self.UnlockItem[RAC3SHIPSLOT.SLOT_0]
            if number >= self.ship_slot_limit:
                self._write8(RAC3_SHIP_DATA_TABLE[slot].SLOT_ADDRESS, 0)

    def phoenix_transporter_cycler(self):
        """Prevent blocked briefing cutscenes from spawning the transporter at the bridge."""
        if self.transporter_fixed:
            return

        # Mark transporter as fixed early if these flags are set
        if (self._read_flag(RAC3CUTSCENEFLAG.PHOENIX_AQUATOS_MISSION_BRIEFING_CUTSCENE)
            and self._read_flag(RAC3CUTSCENEFLAG.PHOENIX_TYHRRANOSIS_MISSION_BRIEFING_CUTSCENE)):
            self.transporter_fixed = True
            return

        # Start checking if a later story flag has been set
        # Later story flags block the earlier cutscenes
        later_story = bool(self.UnlockItem[RAC3ITEM.MASTER_PLAN])
        if not later_story:
            later_story_addresses = [
                RAC3STATUS.METROPOLIS_KLUNK_COMPLETE,
                RAC3STATUS.ESCAPED_LEVIATHAN,
                RAC3STATUS.TYHRRANOSIS_MOMMA_TYHRRANOID_COMPLETE,
            ]
            for address in later_story_addresses:
                if self._read8(address):
                    later_story = True
                    break

        # Mark these events as completed since the game won't do it
        if later_story or self._read8(RAC3STATUS.AQUATOS_LANDED):
            self._write_bits(RAC3CUTSCENEFLAG.PHOENIX_AQUATOS_MISSION_BRIEFING_CUTSCENE)

        if later_story:
            self._write_bits(RAC3CUTSCENEFLAG.PHOENIX_TYHRRANOSIS_MISSION_BRIEFING_CUTSCENE)

    def weapon_cycler(self):
        """Interval update function: Check unlock/lock status of weapons"""
        # Todo: Overhaul item unlocking using RAC3STATUS.PENDING_ITEM address
        # If in vendor, lock all non-progressive weapons to allow second unlock address to work properly
        if (self.vendor_type == RAC3VENDORTYPE.WEAPON and not self.hovering_over_ammo()
            and not self.hovering_over_mega()):
            weapons_to_remove = self.weapon_vendor_items
            for name in non_prog_weapon_data.keys():
                if name in weapons_to_remove:
                    unlock_addr = non_prog_weapon_data[name].UNLOCK_ADDRESS
                    self._write8(unlock_addr, 0)
            return

        for name in non_prog_weapon_data.keys():
            unlock_addr = non_prog_weapon_data[name].UNLOCK_ADDRESS
            ammo_addr = non_prog_weapon_data[name].AMMO_ADDRESS
            if self.UnlockItem[name]:
                self._write8(unlock_addr, 1)
                if name == RAC3ITEM.RY3N0:
                    _xp = self._read32(RAC3_ITEM_DATA_TABLE[name].XP_ADDRESS)
                    threshold_id = UPGRADE_DICT[name][self.ryno - 1]
                    threshold_xp = RAC3_ITEM_DATA_TABLE[ITEM_NAME_FROM_ID[threshold_id]].XP_THRESHOLD
                    if _xp > threshold_xp:
                        self._write32(RAC3_ITEM_DATA_TABLE[name].XP_ADDRESS, threshold_xp)
                        self._write8(RAC3_ITEM_DATA_TABLE[name].LEVEL_ADDRESS, threshold_id)
            else:
                # Prevent the player from using locked weapons and levelling them to accidentally break vendors
                self._write8(unlock_addr, 0)
                self._write32(ammo_addr, 0)

        if self.equipped_item > 1 and self.UnlockItem[ITEM_NAME_FROM_ID[self.equipped_item]] == 0:
            if self.last_used_1 == 0:
                self.update_weapon_equip(equipable_data[RAC3ITEM.WRENCH].ID, 0, None, None)
                return
            if self.UnlockItem[ITEM_NAME_FROM_ID[self.last_used_1]]:
                self.update_weapon_equip(self.last_used_1, self.last_used_1, self.last_used_2, self.last_used_3)
                return
            if self.last_used_2 == 0:
                self.update_weapon_equip(equipable_data[RAC3ITEM.WRENCH].ID, 0, 0, None)
                return
            if self.UnlockItem[ITEM_NAME_FROM_ID[self.last_used_2]]:
                self.update_weapon_equip(self.last_used_2, self.last_used_2, self.last_used_3, self.last_used_4)
                return
            if self.last_used_3 == 0 or self.UnlockItem[ITEM_NAME_FROM_ID[self.last_used_3]]:
                self.update_weapon_equip(equipable_data[RAC3ITEM.WRENCH].ID, self.last_used_3, self.last_used_4,
                                         self.last_used_5)
            else:
                self.update_weapon_equip(self.last_used_3, self.last_used_3, self.last_used_4, self.last_used_5)

    def weapon_mod_cycler(self):
        """Cycle through all weapon mods and update their state"""
        if self.options.weapon_mods >= 1:
            for weapon_name, data in non_prog_weapon_data.items():
                modpack = WEAPON_TO_WEAPON_MODPACK.get(weapon_name, "")
                if self.UnlockItem[weapon_name]:
                    self._write8(data.MOD_ADDRESS, self.UnlockItem.get(modpack, 0))

    def wrench_cycler(self):
        """Control the wrench variant through data after disabling its automatic Nanotech store."""
        if not self.options.progressive_wrench:
            return
        if self.planet == RAC3REGION.MENU or self.between_planets:
            return

        wrench_addresses = RAC3WRENCH.get_wrench_addresses(self.planet, self.current_game)
        if wrench_addresses is None:
            return
        wrench_instruction = wrench_addresses[0] + RAC3WRENCH.BASE_ITEM_ID_OFFSET
        write_wrench_lvl_instruction = self._read32(wrench_instruction)
        if write_wrench_lvl_instruction not in (RAC3WRENCH.ORIGINAL_INSTRUCTION_VALUE,
                                                RAC3WRENCH.PATCHED_INSTRUCTION_VALUE):
            return

        wrench_levels = UPGRADE_DICT[RAC3ITEM.WRENCH]
        prog_wrench = self.UnlockItem[RAC3ITEM.PROGRESSIVE_WRENCH]
        if prog_wrench > 8:
            prog_wrench = 8

        target_level = wrench_levels[max(1, prog_wrench) - 1]
        self._write8(RAC3STATUS.WRENCH_LEVEL, target_level)

        wrench_equip = wrench_addresses[1] + RAC3WRENCH.EQUIP_WRENCH_ADDRESS_OFFSET
        wrench_swing = wrench_addresses[2] + RAC3WRENCH.SWING_WRENCH_ADDRESS_OFFSET
        equip_instruction = self._read32(wrench_equip)
        swing_instruction = self._read32(wrench_swing)
        should_restore_wrench = (prog_wrench > 0 and
                                 (equip_instruction == RAC3WRENCH.PATCHED_EQUIP_VALUE or
                                  swing_instruction == RAC3WRENCH.PATCHED_SWING_VALUE))

        if write_wrench_lvl_instruction == RAC3WRENCH.ORIGINAL_INSTRUCTION_VALUE or should_restore_wrench:
            self._write8(RAC3STATUS.WRENCH_LEVEL, target_level)

        if write_wrench_lvl_instruction == RAC3WRENCH.ORIGINAL_INSTRUCTION_VALUE:
            self._write32(wrench_instruction, RAC3WRENCH.PATCHED_INSTRUCTION_VALUE)

        if prog_wrench == 0:
            if equip_instruction == RAC3WRENCH.ORIGINAL_EQUIP_VALUE:
                self._write32(wrench_equip, RAC3WRENCH.PATCHED_EQUIP_VALUE)
            if swing_instruction == RAC3WRENCH.ORIGINAL_SWING_VALUE:
                self._write32(wrench_swing, RAC3WRENCH.PATCHED_SWING_VALUE)
            if self._read8(RAC3STATUS.HELD_ITEM) == RAC3_ITEM_DATA_TABLE[RAC3ITEM.WRENCH].ID:
                self._write8(RAC3STATUS.PENDING_ITEM, 1)
        else:
            if equip_instruction == RAC3WRENCH.PATCHED_EQUIP_VALUE:
                self._write32(wrench_equip, RAC3WRENCH.ORIGINAL_EQUIP_VALUE)
            if swing_instruction == RAC3WRENCH.PATCHED_SWING_VALUE:
                self._write32(wrench_swing, RAC3WRENCH.ORIGINAL_SWING_VALUE)

    def update_weapon_equip(self, equip: int | None, last_0: int | None,
                            last_1: int | None, last_2: int | None):
        """Writes new values to the player's last used item history"""

        if equip is not None:
            self._write8(RAC3STATUS.EQUIPPED, equip)
        if last_0 is not None:
            self._write8(RAC3STATUS.LAST_USED_0, last_0)
        if last_1 is not None:
            self._write8(RAC3STATUS.LAST_USED_1, last_1)
        if last_2 is not None:
            self._write8(RAC3STATUS.LAST_USED_2, last_2)

    def vidcomic_cycler(self):
        """Cycle through all vidcomics and update their state"""
        prog_comic = self.UnlockItem[RAC3ITEM.PROGRESSIVE_VIDCOMIC]
        for index, name in enumerate(vidcomic_data.keys()):
            comic = self.UnlockItem[name]
            addr = vidcomic_data[name].UNLOCK_ADDRESS
            if index == 0:
                continue

            # Prevent Vidcomic 2 from reappearing after being collected the first time on Heat Street
            if (index == 2
                and self.planet == RAC3REGION.ANNIHILATION_NATION
                and self.is_location_checked(RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.NATION_HEAT_STREET].AP_CODE)
                and self.game_state_value != RAC3GAMESTATE.PAUSED
                and comic == 0):
                self._write8(addr, 1)
                continue

            value = 0 if index > prog_comic else 1
            self._write8(addr, value)

    def vidcomic_health_cycler(self):
        """Cycle through all vidcomic health upgrades and update their state"""
        bonus_health_upgrades = self.UnlockItem[RAC3ITEM.BONUS_VIDCOMIC_HEALTH_UPGRADE]
        if not bonus_health_upgrades:
            return

        bits = set()
        if bonus_health_upgrades >= 1:
            bits.add(0x0)
        if bonus_health_upgrades >= 2:
            bits.add(0x6)
        if bonus_health_upgrades >= 3:
            bits.add(0x7)
        self._write_bits((RAC3STATUS.VIDCOMIC_HEALTH_UPGRADES, bits))

    def armor_cycler(self):
        """Cycle through all armors and update their state"""
        addr = armor_data[RAC3ITEM.PROGRESSIVE_ARMOR]
        armor = self.UnlockItem[RAC3ITEM.PROGRESSIVE_ARMOR]
        current_armor_value = self._read8(addr.UNLOCK_ADDRESS)

        if current_armor_value != armor:
            self._write8(addr.UNLOCK_ADDRESS, armor)
            self._write8(RAC3STATUS.HELMET, armor)

    def timer_cycler(self):
        """Cycle through the timer dictionary, check their duration, and handle their effects"""
        timers = list(self.timers.items())
        for name, _time in timers:
            is_jackpot = name.startswith(RAC3ITEM.JACKPOT)
            _name = RAC3ITEM.JACKPOT if is_jackpot else name
            if time.time() < _time:
                if not is_jackpot:
                    status = item_to_status[name]
                    if status == RAC3STATUS.BLACK_SCREEN and self._read8(RAC3STATUS.PROGRESSIVE_SCAN):
                        status = RAC3STATUS.BLACK_SCREEN_PROG_SCAN
                    match status:
                        case RAC3STATUS.NO_CLANK:
                            self.clank_disabled_trap = True
                            continue
                        case RAC3STATUS.DISARM:
                            if self.vehicle != 0:
                                continue
                        case _:
                            pass
                    self._write8(status, status_on_off.get(status, [1])[0])

                    # Make vehicles invisible as well
                    if self.vehicle and status == RAC3STATUS.INVISIBLE:
                        flags = self._read32(self.vehicle + 0x34)
                        self._write32(self.vehicle + 0x34, flags | 0x01)
            else:
                self.timers.pop(name)
                if is_jackpot:
                    self.enqueue_notification(
                        f"{RAC3TEXTFORMATSTRING.WHITE}Jackpot x{2 ** self.bolt_and_xp_multiplier_value} "
                        f"{RAC3TEXTFORMATSTRING.NORMAL}effect has worn off.")
                else:
                    self.enqueue_notification(
                        f"{name}{RAC3TEXTFORMATSTRING.WHITE} effect has worn off.",
                        RAC3BOXTHEME.WARNING)
                match _name:
                    # Todo: Check for arena mission on LOCK_TRAP
                    case RAC3ITEM.NO_CLANK_TRAP:
                        self.clank_disabled_trap = False
                        continue
                    case RAC3ITEM.JACKPOT:
                        self.bolt_and_xp_multiplier_value -= 1
                        # Clean up the jackpot status if the multiplier is now 0
                        # Allows x1 mult YAML option to also have jackpot working
                        if self.bolt_and_xp_multiplier_value == 0:
                            self._write8(RAC3STATUS.JACKPOT, 0)
                        continue
                    case _:
                        pass
                status = item_to_status[name]
                if status == RAC3STATUS.BLACK_SCREEN and self._read8(RAC3STATUS.PROGRESSIVE_SCAN):
                    status = RAC3STATUS.BLACK_SCREEN_PROG_SCAN
                self._write8(status, status_on_off.get(status, [0])[1])

                # Make vehicles visible again
                if self.vehicle and status == RAC3STATUS.INVISIBLE:
                    flags = self._read32(self.vehicle + 0x34)
                    self._write32(self.vehicle + 0x34, flags & ~0x01)

        # Remove trap effects for traps not in the timer dictionary to prevent any stuck effects
        # Prevent not having lock trap from unlocking weapon during arena weapon specific challenges every cycle
        # for trap_name, status_address in trap_to_status.items():
        #     if trap_name not in self.trap_timers and trap_name != RAC3ITEM.LOCK_TRAP:
        #         self._write8(status_address, 0)

    def weapon_exp_cycler(self):
        """
        Synchronize weapon experience and level with the player's item collection and vendor state.

        - If progressive weapons are enabled, set each weapon's level and XP threshold based on the number of
        collected upgrades.
        - If the player is in a weapon vendor and not hovering over ammo, force the vendor slot weapon to level 1.
        - For the RY3N0 weapon, cap the level at 4 if the ryno flag is set.
        - If progressive weapons are not enabled, restore weapon level based on XP, unless in a vendor and not
        hovering over ammo, in which case set to base level.
        - Handles both progressive and non-progressive weapon logic, including syncing XP and level addresses in memory.
        """
        progressive_weapon_mode = self.options.progressive_weapons
        if self.options.weapon_level_locations and progressive_weapon_mode == 2:
            progressive_weapon_mode = 1  # Force manual levelling if weapon level locations are enabled

        # Manual weapon levelling for progressive weapons
        if progressive_weapon_mode == 1:
            for weapon_name, weapon_data in non_prog_weapon_data.items():
                target_level = self.UnlockItem[weapon_name]
                if not target_level:
                    continue
                if target_level > 5 and (not self.options.ngplus_items or weapon_name == RAC3ITEM.RY3N0):
                    target_level = 5
                if target_level > 8 and self.options.ngplus_items and weapon_name != RAC3ITEM.RY3N0:
                    target_level = 8
                # Todo: update the ryno special cases to handle any weapon
                if weapon_name == RAC3ITEM.RY3N0 and target_level > self.ryno:
                    target_level = self.ryno
                prev_saved = min(self.weapon_levels.get(weapon_name, 1), target_level)
                current_id = self._read8(weapon_data.LEVEL_ADDRESS)
                if current_id not in ITEM_NAME_FROM_ID:
                    # Recover the last tracked level without granting unearned upgrades.
                    current_id = UPGRADE_DICT[weapon_name][prev_saved - 1]
                    self._write8(weapon_data.LEVEL_ADDRESS, current_id)
                    logger.warning(f"Invalid weapon level ID {hex(current_id)} detected for {weapon_name}. "
                                   f"Restoring to last tracked level {prev_saved}.")
                current_level = RAC3_ITEM_DATA_TABLE[ITEM_NAME_FROM_ID[current_id]].LEVEL
                self.weapon_levels[weapon_name] = prev_saved
                if prev_saved < current_level <= target_level:
                    self.weapon_levels[weapon_name] = current_level
                if self.vendor_type == RAC3VENDORTYPE.WEAPON:
                    if self.read_weapon_vendor_slot_data(self.vendor_cursor_pos).item_id.value == RAC3_ITEM_DATA_TABLE[
                        weapon_name].ID and not self.hovering_over_ammo() and not self.hovering_over_mega():
                        self._write8(weapon_data.LEVEL_ADDRESS, RAC3_ITEM_DATA_TABLE[weapon_name].ID)
                        self.last_hovered_weapon = weapon_name
                    else:
                        restore_level = self.weapon_levels.get(weapon_name, 1)
                        self._write8(weapon_data.LEVEL_ADDRESS, UPGRADE_DICT[weapon_name][restore_level - 1])
                else:
                    target_id = UPGRADE_DICT[weapon_name][target_level - 1]
                    target_xp = RAC3_ITEM_DATA_TABLE[ITEM_NAME_FROM_ID[target_id]].XP_THRESHOLD
                    if current_level >= target_level:
                        self._write32(weapon_data.XP_ADDRESS, target_xp)
                        self._write8(weapon_data.LEVEL_ADDRESS, target_id)
            # restore last hovered weapon if we closed the vendor while it was hovering over it
            if (self.last_hovered_weapon != "" and self.vendor_type != RAC3VENDORTYPE.WEAPON
                and self.game_state_value != RAC3GAMESTATE.WEAPON_UPGRADE):
                restore_level = self.weapon_levels.get(self.last_hovered_weapon, 1)
                self._write8(non_prog_weapon_data[self.last_hovered_weapon].LEVEL_ADDRESS,
                             UPGRADE_DICT[self.last_hovered_weapon][restore_level - 1])
                self.last_hovered_weapon = ""

        # Automatic weapon levelling for progressive weapons
        elif progressive_weapon_mode == 2:
            for weapon_name in non_prog_weapon_data.keys():
                target_level = self.UnlockItem[weapon_name]
                if not target_level:
                    continue
                if target_level > 5 and (not self.options.ngplus_items or weapon_name == RAC3ITEM.RY3N0):
                    target_level = 5
                if target_level > 8 and self.options.ngplus_items and weapon_name != RAC3ITEM.RY3N0:
                    target_level = 8
                if self.vendor_type == RAC3VENDORTYPE.WEAPON:
                    if self.read_weapon_vendor_slot_data(self.vendor_cursor_pos).item_id.value == RAC3_ITEM_DATA_TABLE[
                        weapon_name].ID and not self.hovering_over_ammo():
                        target_level = 1
                if weapon_name == RAC3ITEM.RY3N0 and target_level > self.ryno:
                    target_level = self.ryno
                if weapon_name == RAC3ITEM.RY3N0 and self.weapon_levels.get(weapon_name, 1) > self.ryno:
                    self.weapon_levels[weapon_name] = self.ryno
                # logger.debug(f"weapon: {weapon_name}, target: {target_level}")
                target_id = UPGRADE_DICT[weapon_name][target_level - 1]
                target_name = ITEM_NAME_FROM_ID[target_id]
                target_xp = RAC3_ITEM_DATA_TABLE[target_name].XP_THRESHOLD
                # logger.debug(f"{target_name}, id: {target_id}, xp:{target_xp}")
                self._write32(non_prog_weapon_data[weapon_name].XP_ADDRESS, target_xp)
                self._write8(non_prog_weapon_data[weapon_name].LEVEL_ADDRESS, target_id)
                self.weapon_levels[weapon_name] = target_level
        else:
            if self.delayed_weapon_levelups and self.game_state_value != RAC3GAMESTATE.WEAPON_UPGRADE:
                for weapon_name in self.delayed_weapon_levelups:
                    valid_weapons = self.get_valid_weapon_level_ups()
                    if weapon_name in valid_weapons:
                        logger.debug(f"Applying delayed level up for {weapon_name}")
                        self.weapon_level_up(weapon_name)
                self.delayed_weapon_levelups = []
            for weapon_name, weapon_data in non_prog_weapon_data.items():
                if not self.UnlockItem[weapon_name]:
                    continue
                current_id = self._read8(weapon_data.LEVEL_ADDRESS)
                current_level = RAC3_ITEM_DATA_TABLE[ITEM_NAME_FROM_ID[current_id]].LEVEL
                prev_saved = self.weapon_levels.get(weapon_name, 1)
                if current_level > prev_saved:
                    self.weapon_levels[weapon_name] = current_level
                if self.vendor_type == RAC3VENDORTYPE.WEAPON:
                    if self.read_weapon_vendor_slot_data(self.vendor_cursor_pos).item_id.value == RAC3_ITEM_DATA_TABLE[
                        weapon_name].ID and not self.hovering_over_ammo() and not self.hovering_over_mega():

                        # Temporarily set the vendor-focused weapon to its base/display id
                        self._write8(non_prog_weapon_data[weapon_name].LEVEL_ADDRESS,
                                     RAC3_ITEM_DATA_TABLE[weapon_name].ID)
                        self.last_hovered_weapon = weapon_name
                    else:
                        restore_level = self.weapon_levels.get(weapon_name, 1)
                        if weapon_name == RAC3ITEM.RY3N0 and restore_level > self.ryno:
                            self.weapon_levels[weapon_name] = self.ryno
                            restore_level = self.ryno
                        self._write8(non_prog_weapon_data[weapon_name].LEVEL_ADDRESS,
                                     UPGRADE_DICT[weapon_name][restore_level - 1])
            # restore last hovered weapon if we closed the vendor while it was hovering over it
            if (self.last_hovered_weapon != "" and self.vendor_type != RAC3VENDORTYPE.WEAPON
                and self.game_state_value != RAC3GAMESTATE.WEAPON_UPGRADE):
                restore_level = self.weapon_levels.get(self.last_hovered_weapon, 1)
                if self.last_hovered_weapon == RAC3ITEM.RY3N0 and restore_level > self.ryno:
                    restore_level = self.ryno
                self._write8(non_prog_weapon_data[self.last_hovered_weapon].LEVEL_ADDRESS,
                             UPGRADE_DICT[self.last_hovered_weapon][restore_level - 1])
                self.last_hovered_weapon = ""

    def verify_quick_select_and_last_used(self):
        """Check each slot in quick select and held item history, reset if that item has not been collected yet."""
        _slots = [RAC3STATUS.LAST_USED_0, RAC3STATUS.LAST_USED_1, RAC3STATUS.LAST_USED_2, RAC3STATUS.EQUIPPED]
        for slot in QUICK_SELECT_LIST:
            _slots.append(RAC3_STATUS_DATA_TABLE[slot].SLOT_ADDRESS)
        for addr in _slots:
            idx = self._read8(addr)
            if idx > 1:
                name = ITEM_NAME_FROM_ID[idx]
                if not self.UnlockItem[name]:
                    # Not unlocked, but set
                    self._write8(addr, 0)

    def clank_cycler(self):
        """Handle Clank removal and replace a locked Thruster-Pack with Heli-Pack"""
        # Special cases where Clank is already removed
        if ((self.planet == RAC3REGION.HOLOSTAR_STUDIOS and not self._read8(RAC3STATUS.HOLOSTAR_CLANK_FIX))
            or self.planet == RAC3REGION.AQUATOS_BASE
            or not self.UnlockItem[RAC3ITEM.CLANK]
            or self.clank_disabled_trap):
            self._write8(RAC3STATUS.NO_CLANK, 1)
        # No special case:
        else:
            self._write8(RAC3STATUS.NO_CLANK, 0)
        if self.UnlockItem[RAC3ITEM.THRUSTER_PACK]:
            return

        heli_pack_id = gadget_data[RAC3ITEM.HELI_PACK].ID
        thruster_pack_id = gadget_data[RAC3ITEM.THRUSTER_PACK].ID
        self._write8(RAC3STATUS.PREFER_THRUSTER_PACK, 0)  # Prevents accidentally spawning with the Thruster-Pack
        for address in [RAC3STATUS.SELECTED_PACK, RAC3STATUS.STORED_PACK]:
            if self._read32(address) == thruster_pack_id:
                self._write32(address, heli_pack_id)

        pending_pack_id = self._read32(RAC3STATUS.PENDING_PACK)
        if pending_pack_id == thruster_pack_id:
            self._write32(RAC3STATUS.PENDING_PACK, heli_pack_id)
            pending_pack_id = heli_pack_id

        # Do not do anything if it is the hydro-pack
        if pending_pack_id > heli_pack_id:
            return

        if (self._read32(RAC3STATUS.ACTIVE_PACK) != thruster_pack_id
            or self._read32(RAC3STATUS.PACK_STATE) != 2):  # Not ready for new pack
            return

        # Restore compares against the active pack, even if PACK_EQUIP is already Heli-Pack.
        self._write32(RAC3STATUS.STORED_PACK, heli_pack_id)
        self._write32(RAC3STATUS.RESTORE_PACK, 1)

    def multiplier_cycler(self):
        """Update the Bolt+EXP multiplier based on settings"""
        if self.bolt_and_xp_multiplier_value:
            self._write32(RAC3STATUS.JACKPOT_TIMER, 0x7FFFFFFF)
            self._write8(RAC3STATUS.JACKPOT, self.bolt_and_xp_multiplier_value)

            # Fix latching jackpot fillers from receiving a ton at once
            if (not any("Jackpot" in key for key in self.timers.keys())
                and self.bolt_and_xp_multiplier_value != self.options.bolt_and_xp_multiplier):
                self.bolt_and_xp_multiplier_value = self.options.bolt_and_xp_multiplier

    def challenge_mode_cycler(self):
        """Update challenge mode related values based on settings"""
        if self.options.ngplus_start:
            self._write8(RAC3STATUS.CHALLENGE_MODE, 1)
            if self.options.ngplus_start < 2:
                self._write8(RAC3STATUS.MULTIPLIER, 0)

        # award omega arsenal trophy if all 8 weapon levels are unlocked with ng+ items on and level 5 for ry3no
        if self.options.ngplus_items and self.weapon_levels:
            for weapon_name, level in self.weapon_levels.items():
                if weapon_name == RAC3ITEM.RY3N0:
                    if level < self.ryno or (self.options.progressive_weapons
                                             and self.UnlockItem[weapon_name] < 5):
                        return
                elif level < 8:
                    return
            self._write8(RAC3STATUS.OMEGA_ARSENAL_TROPHY, 1)

    def cheat_cycler(self):
        """Handles unlocking cheats such as the lightsaber wrench cheat"""
        for name in cheat_data.keys():
            addr = cheat_data[name].UNLOCK_ADDRESS
            self._write8(addr, 1 if self.UnlockItem[name] else 0)
            if not self.UnlockItem[name] and name in item_to_status:
                self._write8(item_to_status[name], 0)

    def patch_cycler(self):
        """Apply runtime instruction patches based on current planet."""
        planet_patches = self.get_planet_patch_instructions()
        if not planet_patches:
            return

        if self.planet == RAC3REGION.ANNIHILATION_NATION:
            # One HP challenge patches for Ratchet to prevent automatically losing One Hit Wonder type challenges.
            # Sadly doesn't fix Flee Flawlessly skill point.
            character = self.player_type
            if character == RAC3PLAYERTYPE.TYHRRANOID:
                character = RAC3PLAYERTYPE.RATCHET

            # Apply patches if one HP challenge is enabled for Ratchet.
            if self.options.one_hp_challenge.get(character, False) and character == RAC3PLAYERTYPE.RATCHET:
                for instruction in planet_patches:
                    self.safe_patch_instruction(instruction)
            # Restore original instructions if one HP challenge is not enabled for Ratchet.
            elif not self.options.one_hp_challenge.get(character, False):
                for instruction in planet_patches:
                    self.safe_patch_instruction(instruction, restore=True)
            return

        # Apply all non-conditional patches for the current planet.
        for instruction in planet_patches:
            self.safe_patch_instruction(instruction)

    def get_planet_patch_instructions(self) -> list[int]:
        """Return all patch instructions associated with the current planet and game version."""
        return [instruction for instruction, planet in PATCH_INSTRUCTION_TO_PLANET.items() if
                planet == self.planet and self.current_game in PATCH_INSTRUCTION_TO_GAME_IDS[instruction]]

    def safe_patch_instruction(self, instruction_address: int, restore: bool = False):
        """Safely apply or restore an instruction patch if current opcode matches the expected source opcode."""
        original = ORIGINAL_INSTRUCTIONS.get(instruction_address)
        patched = PATCHED_INSTRUCTIONS.get(instruction_address)
        if original is None or patched is None:
            return

        # Determine source and target opcodes based on whether we are restoring or patching
        source = patched if restore else original
        target = original if restore else patched
        current = self._read32(instruction_address)
        if current == source:
            logger.debug(f"Wrote new patch to {PATCH_INSTRUCTION_TO_NAME[instruction_address]}")
            self._write32(instruction_address, target)

    def overflow_fix(self):
        """Detect any integer overflows and reset the value"""
        if self.nanotech_exp > 0x7FFFFFFF:
            self._write32(RAC3STATUS.NANOTECH_EXP, 0)
            self.enqueue_notification("Negative Nanotech EXP detected! Resetting EXP to 0", RAC3BOXTHEME.WARNING)
        # If other stuff needs overflow fixing, add here

    def process_delayed_things_cycler(self):
        """Process delayed things such as debt traps"""
        if not self.near_pda_vendor():
            for _ in range(self.delayed_debt_trap_count):
                bolts = self._read32(RAC3STATUS.BOLTS)
                impact = self.options.trap_magnitude.get(
                    RAC3ITEM.GADGETRON_DEBT_TRAP, trap_magnitude_data[RAC3ITEM.GADGETRON_DEBT_TRAP])
                if impact > 100:
                    impact = 100
                new_bolts = bolts * (100 - impact) / 100
                self._write32(RAC3STATUS.BOLTS, int(new_bolts))
            self.delayed_debt_trap_count = 0
        # Add any other things we need to delay and process here

    def health_cycler(self):
        """
        Enforces one HP challenge for player and vehicle if enabled in settings
        Sets health to 1 if above 1 for the current character
        """
        character = self.player_type
        if character == RAC3PLAYERTYPE.TYHRRANOID:
            character = RAC3PLAYERTYPE.RATCHET  # Treat Tyhrranoid as Ratchet for one HP challenge
        # Check for one HP challenge for current character
        if self.options.one_hp_challenge.get(character, False):
            if character == RAC3PLAYERTYPE.GIANT:
                if self._read32(RAC3STATUS.GIANT_CLANK_HEALTH) > 1:
                    self._write32(RAC3STATUS.GIANT_CLANK_HEALTH, 1)
            else:
                # Applies to Ratchet, Clank, Qwark
                # Ban shield charger usage if one HP challenge is active for Ratchet
                if character == RAC3PLAYERTYPE.RATCHET:
                    self._write8(non_prog_weapon_data[RAC3ITEM.SHIELD_CHARGER].AMMO_ADDRESS, 0)
                if self.health > 1:
                    self._write8(RAC3STATUS.HEALTH, 1)
                    self._write8(RAC3STATUS.NANOPAK_HEALTH, 0)

        # Vehicle one HP challenge is independent of player_type
        if self.vehicle and self.options.one_hp_challenge.get(RAC3PLAYERTYPE.VEHICLE, False):
            health_addr = self._read32(self._read32(self.vehicle + 0x68))
            max_health = self._read32(self._read32(self.vehicle + 0x68) + 0x34)
            target_health = max_health * 0.01
            if self._read_float(health_addr) > target_health:
                self._write_float(health_addr, target_health)

        # If loading from the main menu we delay fixing the current health until the load is complete
        if self.main_menu:
            if self.max_health > 10:
                self._write8(RAC3STATUS.HEALTH, self.max_health)
                self.main_menu = False

    def shortcut_cycler(self):
        """Activates Taxis/Dropships/Teleporter shortcuts"""
        # if ((self.planet != RAC3REGION.TYHRRANOSIS or self.short_pause)
        #     and RAC3LOCATION.TYHRRANOSIS_BOSS not in self.checked_locations):
        #     self.tyhrra_dropship = 0
        # Release the shortcut's temporary bit even if the pause ended between updates.
        if self.metro_dropship == 1:
            if not (self._read8(RAC3STATUS.METROPOLIS_KLUNK_COMPLETE) & 1):
                self._unwrite_bits(RAC3PROGRESSFLAG.METROPOLIS_DEFEATED_KLUNK)
            self.metro_dropship = 2
        if ((self.planet != RAC3REGION.METROPOLIS or not self.short_pause)
            and RAC3LOCATION.METROPOLIS_DEFEAT_KLUNK not in self.checked_locations):
            self.metro_dropship = 0
        if ((self.planet != RAC3REGION.HOLOSTAR_STUDIOS or not self.short_pause)
            and RAC3LOCATION.HOLOSTAR_RETURN_TO_SHIP not in self.checked_locations):
            self.holo_teleport = 0
        for name, data in RAC3_SHORTCUT_DATA_TABLE.items():
            if self.planet == data.PLANET and self.options.shortcuts.get(name, False):
                if data.ITEMS is None or any(
                    all(self.UnlockItem[item] for item in items) for items in data.ITEMS):
                    # special cases
                    if name == RAC3SHORTCUTS.TYHRRANOSIS_DROPSHIP and data.FLAG_ADDRESSES is not None:
                        if not self.tyhrra_dropship:
                            has_seen_cutscene = bool(self._read8(RAC3CUTSCENEFLAG.TYHRRANOSIS_FINISH_PROLOGUE[0]) & (
                                1 << RAC3CUTSCENEFLAG.TYHRRANOSIS_FINISH_PROLOGUE[1]))
                            if has_seen_cutscene:
                                self.tyhrra_dropship = True
                                self.force_respawn()

                        # logger.debug(f"Pause state: {self.pause_state_value}, latch state: {self.tyhrra_dropship}")
                        # if self.tyhrra_dropship < 1 and self.short_pause:
                        #     self.tyhrra_dropship += 1
                        #     # logger.debug("Set Tyhrranosis Dropship")
                        #     self._write_bits(data.FLAG_ADDRESSES[0])
                        # elif self.tyhrra_dropship == 1 and self.short_pause:
                        #     self.tyhrra_dropship += 1
                        #     # logger.debug("UnSet Tyhrranosis Dropship")
                        #     self._unwrite_bits(data.FLAG_ADDRESSES[0])
                        # continue
                    if name == RAC3SHORTCUTS.METROPOLIS_DROPSHIP and data.FLAG_ADDRESSES is not None:
                        if self.metro_dropship == 0 and self.short_pause:
                            flag = data.FLAG_ADDRESSES[0]
                            if self._read8(RAC3STATUS.METROPOLIS_KLUNK_COMPLETE) & 1 or self._read_flag(flag):
                                self.metro_dropship = 2
                            else:
                                self._write_bits(flag)
                                self.metro_dropship = 1
                        continue
                    if name == RAC3SHORTCUTS.HOLOSTAR_TELEPORTER and data.FLAG_ADDRESSES is not None:
                        if self.holo_teleport == 0 and self.short_pause:
                            self.holo_teleport += 1
                            self._write_bits(data.FLAG_ADDRESSES[0])
                            logger.debug("Set Holostar Teleporter")
                        elif self.holo_teleport == 1 and self.holo_door > 1:
                            logger.debug("Trigger Holostar Cutscene")
                            self.holo_teleport += 1
                            self._unwrite_bits(data.FLAG_ADDRESSES[0])
                            self.force_respawn()
                        continue
                    # all other shortcuts
                    # logger.debug(f"Process: {name}")
                    if data.FLAG_ADDRESSES is not None:
                        _write: dict[int, set[int]] = {}
                        for check in data.FLAG_ADDRESSES:
                            _write.setdefault(check[0], set()).add(check[1])
                        for bits in _write.items():
                            self._write_bits(bits)
                    if data.VISIT_ADDRESSES is not None and not self.visited_planets.issuperset(data.VISIT_ADDRESSES):
                        for address in data.VISIT_ADDRESSES:
                            self._write8(RAC3_REGION_DATA_TABLE[address].VISIT_ADDRESS, 1)

    def speedup_cycler(self):
        """Completes puzzles and speeds up other gameplay"""
        self.hacker_cycler()
        self.puzzle_cycler(RAC3ITEM.TYHRRA_GUISE, RAC3SPEEDUPS.TYHRRAGUISE, "opened_the_tyhrranoid_doors",
                           PLANETS_WITH_TYHRRANOID_PUZZLES, TYHRRANOID_PUZZLE_TO_REGION)
        self.puzzle_cycler(RAC3ITEM.REFRACTOR, RAC3SPEEDUPS.REFRACTOR, "opened_the_refractor_doors",
                           PLANETS_WITH_REFRACTOR_PUZZLES, REFRACTOR_PUZZLE_TO_REGION)
        wrench = RAC3ITEM.PROGRESSIVE_WRENCH if self.options.progressive_wrench else None
        self.puzzle_cycler(wrench, RAC3SPEEDUPS.BOLT_CRANK, "turned_the_bolt_cranks",
                           PLANETS_WITH_BOLT_CRANK_PUZZLES, BOLT_CRANK_TO_REGION)

        if self.new_planet and self.planet != RAC3REGION.TYHRRANOSIS and self.tyhrra_intro > 0:
            if RAC3PROGRESSFLAG.TYHRRANOSIS_COMPLETE_PROLOGUE[1] not in self._read_bits(
                RAC3PROGRESSFLAG.TYHRRANOSIS_COMPLETE_PROLOGUE[0]):
                self.tyhrra_intro = 0
        if self.options.speedups.get(RAC3SPEEDUPS.HALO_JUMPS, False):
            for check, region in HALO_JUMP_TO_REGION.items():
                if self.planet in region:
                    if (region == RAC3REGION.TYHRRANOSIS and self.tyhrra_intro == 0
                        and not self.between_planets):
                        self.tyhrra_intro = 1
                        self.force_respawn()

                    self._write_bits(check)
        # if self.options.speedups.get(RAC3SPEEDUPS.MISSIONS, False):
        #     for check, region in RANGER_TO_REGION.items():
        #         if self.planet in region:
        #             if region == RAC3REGION.ARIDIA:
        #                 pass

    def hacker_cycler(self):
        """Finds hacker puzzle doors on current planet and marks all hacker puzzles complete if hacker is unlocked."""
        if not self.UnlockItem[RAC3ITEM.HACKER] or not self.options.speedups.get(RAC3SPEEDUPS.HACKER, False):
            return

        # Handle door finding for the current planet
        if not self.opened_the_hacker_doors and self.planet in PLANETS_WITH_HACKER_PUZZLES:
            puzzles = [puzzle for puzzle, region in HACKER_PUZZLE_TO_REGION.items() if region == self.planet]
            doors = [door_id for puzzle in puzzles if puzzle in HACKER_PUZZLE_TO_DOOR_IDS for door_id in
                     HACKER_PUZZLE_TO_DOOR_IDS[puzzle]]

            # Try to resolve each door id to a moby address; save successful lookups only
            for door_id in doors:
                if door_id in self.hacker_door_addresses:
                    # already resolved
                    continue
                addr = self.find_moby_by_id_iteration(door_id)
                if addr:
                    self.hacker_door_addresses[door_id] = addr

        # Mark all hacker puzzles as complete
        if self.is_reloading and not self.opened_the_hacker_doors:
            self.opened_the_hacker_doors = True
        checks: dict[int, set[int]] = {}
        for address, bit in [puzzle for puzzle, region in HACKER_PUZZLE_TO_REGION.items() if
                             region in PLANETS_WITH_HACKER_PUZZLES]:
            if bit in checks.get(address, []):
                continue
            checks.setdefault(address, set()).add(bit)
        for bits in checks.items():
            self._write_bits(bits)

        # Open doors if all are resolved
        if (self.planet in PLANETS_WITH_HACKER_PUZZLES
            and len(self.hacker_door_addresses) == REGION_TO_HACKER_DOOR_COUNT.get(self.planet, 0)
            and not self.opened_the_hacker_doors):
            for door_id in self.hacker_door_addresses.keys():
                door_addr = self.hacker_door_addresses[door_id]
                self._write16(door_addr + 0xBE, 5)
            self.opened_the_hacker_doors = True

    # TODO: Add moby scanning for Phoenix Rescue and Command Center Refractor doors since they dont have a progress flag
    def puzzle_cycler(self, item: str | None, option: str, check: str, planets: list[str], table: dict[tuple[int, int],
    str], already: bool | None = False):
        """
        General function for handling updating any puzzle type during the cycler iterations.
        If we pass in an item, we will check if the item is unlocked and if the option is enabled before processing.
        """
        if ((item is not None and not self.UnlockItem[item] and not already)
            or not self.options.speedups.get(option, False)):
            return
        if not already and self.is_reloading and not self.__getattribute__(check):
            self.__setattr__(check, True)
        checks: dict[int, set[int]] = {}
        for address, bit in [puzzle for puzzle, region in table.items() if region in planets]:
            if already:
                if bit not in self._read_bits(address):
                    self.__setattr__(check, False)
                    return
            else:
                if bit in checks.get(address, []):
                    continue
                checks.setdefault(address, set()).add(bit)
        if already:
            self.__setattr__(check, True)
        else:
            for bits in checks.items():
                self._write_bits(bits)

    def find_moby_by_id_traversal(self, target_id: int) -> int:
        """Traverse the moby linked list on the current planet to find a moby with the given ID and return its
        address"""
        if not self.ratchet_moby:
            logger.debug("Ratchet pointer is null")
            return 0
        moby_offset = 0
        current_id = 0
        for traversal_count in range(1, 10001):
            if current_id == target_id:
                moby_addr = self.ratchet_moby + moby_offset
                logger.debug(
                    f"Moby with ID {target_id} found at address: {hex(moby_addr)} after {traversal_count} traversals")
                return moby_addr
            next_ptr_addr = self.ratchet_moby + 0x28 + moby_offset
            if next_ptr_addr < 0 or next_ptr_addr > 0xFFFFFFFF:
                logger.debug(
                    f"Moby with ID {target_id} not found, next pointer address out of range "
                    f"after {traversal_count} traversals")
                return 0
            next_ptr = self._read32(next_ptr_addr)
            if next_ptr == 0:  # Null pointer found
                logger.debug(
                    f"Moby with ID {target_id} not found, reached null pointer after {traversal_count} traversals")
                return 0
            moby_offset = next_ptr - self.ratchet_moby
            if moby_offset < 0:
                logger.debug(
                    f"Moby with ID {target_id} not found, invalid offset detected after {traversal_count} traversals")
                return 0
            current_id_addr = self.ratchet_moby + 0xB2 + moby_offset
            if current_id_addr < 0 or current_id_addr > 0xFFFFFFFF:
                logger.debug(
                    f"Moby with ID {target_id} not found, current id address out of range "
                    f"after {traversal_count} traversals")
                return 0
            current_id = self._read16(current_id_addr)
        logger.debug(f"Moby with ID {target_id} not found after maximum traversals")
        return 0

    def find_moby_by_id_iteration(self, target_id: int) -> int:
        """Find a Moby by UID, stopping at the empty moby with a 0xFF state value at the end of the active moby list."""
        addr = self.ratchet_moby
        ram_end = 0x02000000

        if not 0 < addr < ram_end:
            return 0

        while addr + 0x100 <= ram_end:
            # Read a batch of up to 128 moby addresses at once
            count = min(128, (ram_end - addr) // 0x100)
            moby_addresses = [addr + i * 0x100 for i in range(count)]

            # Read state and UID together using batching
            read_addresses = [moby_addr + offset for moby_addr in moby_addresses for offset in [0x20, 0xB2]]

            # Odd indices are the state, even indices are the UID
            moby_state_uid_pairs = self._read16_batch(read_addresses)

            for i, moby_addr in enumerate(moby_addresses):
                # Since we cant use read8 and read16 together in a batch,
                # so we have to extract the state from the halfword at +0x20.
                state = moby_state_uid_pairs[i * 2] & 0xFF
                # If the state is 0xFF, we've reached the end of the active moby list.
                if state == 0xFF:
                    return 0

                if moby_state_uid_pairs[i * 2 + 1] == target_id:
                    return moby_addr

            addr += count * 0x100

        return 0

    def pda_vendor_cycler(self):
        """Handles PDA vendor logic: finding, resetting, and repurchasing on Qwark's Hideout."""

        # If PDA vendor not found, don't continue
        if self.pda_vendor == 0:
            return

        # Wait until Qwarks Hideout is fully loaded and PDA is unlocked
        if not self.should_cycle_gadgets() or self.UnlockItem[RAC3ITEM.PDA] == 0:
            return

        # If Ratchet has the PDA but has not checked the PDA location, reset the vendor if close
        if (self.UnlockItem[RAC3ITEM.PDA] == 1 and
            not self.is_location_checked(RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.HIDEOUT_PDA].AP_CODE)):
            distance_squared = self.distance_to_moby_squared(self.pda_vendor)
            if distance_squared < 144.0:  # 12^2
                self.reset_pda_vendor()

    def reset_pda_vendor(self):
        """Reset PDA Vendor to initial state to allow repurchasing the PDA"""
        if self.pda_vendor == 0:
            logger.error("PDA Vendor not found, cannot reset")
            return
        self._write8(self.pda_vendor + 0x7C, 1)  # Put PDA back in vendor
        self._write8(self.pda_vendor + 0x94, 0)  # Set bought flag to 0
        self._write8(self.pda_vendor + 0x20, 1)  # Reset interaction state

    def enqueue_notification(self,
                             message_or_notification: str | RAC3NOTIFICATION,
                             theme: int = RAC3BOXTHEME.DEFAULT,
                             duration: float = 3.0) -> None:
        """Append a notification to the queue from a message or pre-built RAC3NOTIFICATION."""
        if isinstance(message_or_notification, RAC3NOTIFICATION):
            notification = message_or_notification
            message = notification.message
        else:
            message = message_or_notification
            notification = RAC3NOTIFICATION(message, theme, duration)

        # Warn and truncate if message exceeds 250 characters
        if len(message) > 250:
            logger.warning(f"Notification message exceeds 250 chars ({len(message)}), truncating: {message[:50]}...")
            notification.message = message[:250]
        self.notification_queue.append(notification)

    def dequeue_notifications(self, count: int = 1) -> None:
        """Pop up to `count` notifications from the front of the queue."""
        for _ in range(max(0, count)):
            if not self.notification_queue:
                break
            self.notification_queue.pop(0)

    def notification_cycler(self):
        """Handle the current displayed pop-up message notification, and message queue"""
        current_time = time.time()
        tyhrranoid_game = (self.player_type == RAC3PLAYERTYPE.TYHRRANOID and self.action ==
                           RAC3PLAYERACTION.TYHRRANOID_MINIGAME)
        paused = ((self.pausing_game_state and self.game_state_value != RAC3GAMESTATE.QUICK_SELECT)
                  or self.between_planets
                  or (current_time - self.last_in_vendor_time) < 0.25)
        self._write32(RAC3MESSAGEBOX.HIDDEN_AND_PAUSED,
                      int(self.inside_hacker_puzzle or paused))
        if self.notification_queue:
            if self.notification_time == 0:
                self.notification_time = current_time + self.notification_queue[0].duration
            if tyhrranoid_game or paused:
                if self.notification_paused_remaining:
                    # Pause the notification timer
                    self.notification_time = current_time + self.notification_paused_remaining
                else:
                    self.notification_time = current_time + self.notification_queue[0].duration
                return
            if self.notification_time < current_time and not self.message_display:
                # Pop the number of messages that were displayed last cycle
                next_duration = self.notification_queue[0].duration
                self.dequeue_notifications(self.notification_merge_count)
                self.write_messagebox_theme()
                logger.debug(f"notification queue: {len(self.notification_queue)}")
                if self.notification_queue:
                    next_duration = self.notification_queue[0].duration
                self.notification_time = current_time + next_duration
            if self.notification_queue:
                # Merge up to 3 notifications of the same theme, but do not exceed 250 chars
                merged_notification = self.notification_queue[0]
                merged_message = merged_notification.message
                theme = merged_notification.theme
                merge_count = 1
                total_length = len(merged_message)
                for i in range(1, min(3, len(self.notification_queue))):
                    next_notification = self.notification_queue[i]
                    next_message = next_notification.message
                    next_theme = next_notification.theme
                    # +1 for the '\n' separator
                    add_length = 1 + len(next_message)
                    if next_theme == theme and (total_length + add_length) <= 250:
                        merged_message += "\n" + next_message
                        total_length += add_length
                        merge_count += 1
                    else:
                        break
                self.notification_merge_count = merge_count
                msg_list, longest_line_length = self.format_textbox_string(merged_message)
                if not self.message_display:
                    if self.notification_time < current_time:
                        self.notification_time = current_time + merged_notification.duration
                    display_time = int((self.notification_time - current_time) * 120)
                    self.messagebox(msg_list, longest_line_length, theme, display_time)
                else:
                    write_message = b""
                    for line in msg_list:
                        write_message += line
                    read_message = self._read_bytes(RAC3MESSAGEBOX.MESSAGE, len(write_message))
                    if read_message != write_message:
                        # Give the player a bit more time to read the new appended line in case it was about to
                        # expire
                        if self.notification_time - current_time < 1.5:
                            self.notification_time = current_time + 1.5
                        display_time = int((self.notification_time - current_time) * 120)
                        # A lot of messages can cause this value to go negative and if so, set a minimum display
                        # time
                        if display_time < 0:
                            self.notification_time = current_time + 1
                            display_time = int((self.notification_time - current_time) * 120)
                        self.messagebox(msg_list, longest_line_length, theme, display_time)
                        # logger.debug("Warning: Incorrect Display message detected")
                        # logger.debug(f"Message: {merged_message}")
                        # logger.debug(f"{read_message}")
                        # logger.debug(f"{write_message}")
                    self.notification_paused_remaining = max(0.0, self.notification_time - current_time)
        else:
            self.notification_time = 0
            self.notification_merge_count = 1

    def write_messagebox_theme(self, theme_name: int = RAC3BOXTHEME.DEFAULT) -> None:
        """Update the current messagebox theme, either to the default or a specific theme"""
        theme = THEME_ID_TO_THEME_COLORS[theme_name]
        self._write32(self._read32(RAC3MESSAGEBOX.BACKGROUND_COLOR_POINTER), theme.BACKGROUND)
        self._write32(self._read32(RAC3MESSAGEBOX.EDGE_COLOR_POINTER), theme.BOX)
        self._write32(self._read32(RAC3MESSAGEBOX.CENTER_COLOR_POINTER), theme.BOX)
        self._write32(self._read32(RAC3MESSAGEBOX.TEXT_COLOR_POINTER), theme.TEXT)

    def format_textbox_string(self, msg: str) -> tuple[list[bytes], int]:
        """Process a full message into game insertable bytes, for use with in game pop-ups"""
        # Split message on \n to handle newlines
        lines = msg.split("\n")
        # Write each line to memory, update string pointers
        longest_line_length = 0
        message_list: list[bytes] = []
        for _idx, line in enumerate(lines):
            # Convert to bytes, add null terminator
            line_bytes, line_expected_length = self.format_color_string(line)
            line_bytes += b"\x00"
            message_list.append(line_bytes)
            if line_expected_length > longest_line_length:
                longest_line_length = line_expected_length
        return message_list, longest_line_length

    @staticmethod
    def format_color_string(msg: str) -> tuple[bytes, int]:
        """Converts a message string with color formatting to game insertable bytes with color formatting"""
        # Normalize and strip accents so characters are ASCII-safe for the game
        # noinspection PyBroadException
        try:
            msg = remove_accents(msg)
        except Exception:
            # Fallback: if remove_accents fails, continue with original msg
            pass
        result = bytearray()
        i = 0
        expected_length = 0
        while i < len(msg):
            matched = False
            for code, byte in FORMAT_NAME_TO_BYTE.items():
                if msg.startswith(code, i):
                    # Insert the color code byte (as a single byte)
                    if isinstance(byte, str):
                        byte = ord(byte)
                    expected_length += TEXT_BYTE_TO_EXPECTED_WIDTH.get(byte, 7)
                    result.append(byte)
                    i += len(code)
                    matched = True
                    break
            if not matched:
                # Insert the ASCII value of the character
                msg_ordinal = ord(msg[i])
                if msg_ordinal < 0 or msg_ordinal > 0x7F:
                    # Replace unsupported characters with a question mark
                    msg_ordinal = ord("?")
                result.append(msg_ordinal)
                expected_length += TEXT_BYTE_TO_EXPECTED_WIDTH.get(msg_ordinal, 7)
                i += 1
        return bytes(result), expected_length

    def messagebox(self,
                   msg_list: list[bytes],
                   longest_line_length: int,
                   box_theme: int = RAC3BOXTHEME.DEFAULT,
                   _time: int = 0x168) -> None:
        """Update the contents of the current pop-up message"""
        if _time < 0:
            _time = 0
        curr_addr = RAC3MESSAGEBOX.MESSAGE
        msg_bytes = b""
        for idx, line in enumerate(msg_list):
            msg_bytes += line
            # self._write_bytes(curr_addr, line)
            # Write pointer to this line at pointer_addr + 4*idx
            self._write32(RAC3MESSAGEBOX.TEXT_POINTER + 4 * idx, curr_addr)
            # Move to next address after this string
            curr_addr += len(line)
        self._write32(RAC3MESSAGEBOX.NUM_LINES, len(msg_list))
        width = longest_line_length
        self.write_messagebox_theme(box_theme)

        self._write32(RAC3MESSAGEBOX.TIMER, _time)
        self._write32(RAC3MESSAGEBOX.TEXT_POINTER, RAC3MESSAGEBOX.MESSAGE)
        self._write32(RAC3MESSAGEBOX.BOX_WIDTH, width)
        self._write_bytes(RAC3MESSAGEBOX.MESSAGE, msg_bytes)
        self._write_float(self._read32(RAC3MESSAGEBOX.VISIBLE_POINTER), 1.0)

    def update_save(self) -> dict[int, tuple[int, int]]:
        """Check if the game save is different to the server"""
        save: dict[int, tuple[int, int]] = {}
        for data in SAVE_DATA:
            match data.TYPE:
                case CHECKTYPE.BYTE:
                    save[data.ADDRESS] = (data.TYPE, self._read8(data.ADDRESS))
                case CHECKTYPE.SHORT:
                    save[data.ADDRESS] = (data.TYPE, self._read16(data.ADDRESS))
                case CHECKTYPE.INT:
                    save[data.ADDRESS] = (data.TYPE, self._read32(data.ADDRESS))

        return save

    #######################
    # Command Only        #
    #######################

    def print_all_vendor_items(self):
        """Print all items sold by the current planet's vendor to the log, including all relevant properties"""
        if self.vendor_type is None:
            logger.error("Vendor type is None, cannot print vendor items. This command should only be used when in a "
                         "vendor menu.")
            return
        num_slots = self._read32(RAC3VENDOR.get_vendor_property_address(
            self.planet, RAC3VENDOR.SLOT_COUNT_OFFSET, self.current_game))
        logger.info(f"{self.vendor_type} has {num_slots} slots")
        match self.vendor_type:
            case RAC3VENDORTYPE.WEAPON:
                for slot, slot_data in enumerate(
                    [self.read_weapon_vendor_slot_data(slot) for slot in range(num_slots)]):
                    item_name = ITEM_NAME_FROM_ID.get(slot_data.item_id.value,
                                                      f"Unknown Item ID {slot_data.item_id.value}")
                    logger.info(
                        f"Vendor Slot {slot}: "
                        f"Item Name: {item_name}, "
                        "\n" + "\n".join(f"{prop.name}: {prop.read_property()}" for prop in slot_data.get_data()) + "\n"
                    )
            case RAC3VENDORTYPE.ARMOR:
                for slot, slot_data in enumerate([self.read_armor_vendor_slot_data(slot) for slot in range(num_slots)]):
                    item_name = ITEM_NAME_FROM_ID.get(slot_data.armor_level.value + 0xF5,
                                                      f"Unknown Armor Level {slot_data.armor_level.value}")
                    logger.info(
                        f"Vendor Slot {slot}: "
                        f"Item Name: {item_name}, "
                        "\n" + "\n".join(f"{prop.name}: {prop.read_property()}" for prop in slot_data.get_data()) + "\n"
                    )
            case RAC3VENDORTYPE.SHIP:
                for slot, slot_data in enumerate([self.read_ship_vendor_slot_data(slot) for slot in range(num_slots)]):
                    item_name = self._read_string(slot_data.item_name_ptr.value, 64)
                    logger.info(
                        f"Vendor Slot {slot}: "
                        f"Item Name: {item_name}, "
                        "\n" + "\n".join(f"{prop.name}: {prop.read_property()}" for prop in slot_data.get_data()) + "\n"
                    )
            case RAC3VENDORTYPE.SKIN:
                for slot, slot_data in enumerate([self.read_skin_vendor_slot_data(slot) for slot in range(num_slots)]):
                    logger.info(
                        f"Vendor Slot {slot}: "
                        f"Item Name: ???, "
                        "\n" + "\n".join(f"{prop.name}: {prop.read_property()}" for prop in slot_data.get_data()) + "\n"
                    )

    def dump_info(self, slot_data: dict[str, Any]):
        """Dumps info about the current state of the client"""
        logger.info(f"Collected Items: {self.UnlockItem}")
        count = 0
        for name in SHIP_SLOTS:
            logger.info(f"Planet{count}: {PLANET_NAME_FROM_ID[self._read8(RAC3_SHIP_DATA_TABLE[name].SLOT_ADDRESS)]}")
            count += 1
        logger.info(f"Slot Data: {slot_data}")
        logger.info(f"Archipelago Version: {__version__}")
        logger.info(f"AP World Version: {RAC3OPTION.VERSION_NUMBER}")
        logger.info(f'Game Version: {GAME_ID_TO_VERSION.get(self.current_game, "Unknown")} ({self.current_game})')
        logger.info(f"Current Planet Tracked: {self.planet}")
        logger.info(f"Current Player Type: {self.player_type}")
        logger.info(
            f"Current Player Action: {PLAYER_ACTION_NAMES.get(self.action, 'Unknown')} ({hex(self.action).upper()})")
        logger.info(
            f"Current Action Type: {ACTION_TYPE_NAMES.get(self.action_type, 'Unknown')} ("
            f"{hex(self.action_type).upper()})")
        logger.info(f"Current Available Weapon Vendor Items: {self.weapon_vendor_items}")
        logger.info(f"Current Available Omega Weapon Items: {self.omega_weapon_vendors_items}")
        logger.info(f"Current Available Armor Vendor Items: {self.armor_vendor_items}")
        if self.cycle_times:
            cycle_min = min(self.cycle_times)
            cycle_avg = sum(self.cycle_times) / len(self.cycle_times)
            cycle_max = max(self.cycle_times)
            logger.info(
                f"Update cycle execution time last {len(self.cycle_times)} cycles: "
                f"min {cycle_min:.4f}s / avg {cycle_avg:.4f}s / max {cycle_max:.4f}s"
            )
        else:
            logger.info("Update cycle execution time: no samples collected yet")
        logger.info(f"Sewer Crystals Inventory: {self._read8(RAC3STATUS.CRYSTALS_CURRENT)}")
        logger.info(f"Sewer Crystals Traded: {self._read8(RAC3STATUS.CRYSTALS_TRADED)}")
        logger.info(f"Ship Slot Limit: {self.ship_slot_limit}")
        if self.planet != RAC3REGION.QWARKS_HIDEOUT:
            pda_vendor_str = "N/A"
        else:
            pda_vendor_str = hex(self.pda_vendor) if self.pda_vendor else "Not Found"
        logger.info(f"PDA Vendor Address: {pda_vendor_str}")
        if self.planet in PLANETS_WITH_HACKER_PUZZLES:
            hacker_door_addr = {door_id: (hex(addr) if addr else "Not Found")
                                for door_id, addr in self.hacker_door_addresses.items()}
        else:
            hacker_door_addr = "N/A"
        logger.info(f"Hacker Door Addresses: {hacker_door_addr}")
        logger.info(f"Opened Hacker Doors: {self.opened_the_hacker_doors}")
        logger.info(f"Opened Tyhrranoid Doors: {self.opened_the_tyhrranoid_doors}")
        logger.info(f"Opened Refractor Doors: {self.opened_the_refractor_doors}")
        logger.info(f"Turned Bolt Cranks: {self.turned_the_bolt_cranks}")
        visited_planets = [planet for planet in self.visited_planets if not (
            planet == RAC3REGION.HOLOSTAR_STUDIOS_CLANK and self.options.shortcuts.get(RAC3SHORTCUTS.HOLOSTAR_CLANK,
                                                                                       False))]
        logger.info(f"Visited Planets: {visited_planets}")
        logger.info(f"Active Patches: {[PATCH_INSTRUCTION_TO_NAME[patch] for patch in self.get_active_patches()]}")
        failed_patches = self.get_failed_patches()
        logger.info(f"Failed Patches: {[PATCH_INSTRUCTION_TO_NAME[patch] for patch in failed_patches]}")
        if len(failed_patches) > 0:
            logger.warning("Failed patches detected: instruction opcodes were neither source nor patched values. "
                           "This may indicate a corrupted ISO or an unsupported game version. "
                           "Please report this to the developers with the above information.")

    def get_active_patches(self) -> list[int]:
        """Return a list of active patch addresses based on the current planet."""
        return [
            instruction for instruction in self.get_planet_patch_instructions()
            if self._read32(instruction) == PATCHED_INSTRUCTIONS[instruction]]

    def get_failed_patches(self) -> list[int]:
        """Return patch addresses whose opcode is neither the original nor patched value."""
        return [
            instruction for instruction in self.get_planet_patch_instructions()
            if self._read32(instruction) not in {
                ORIGINAL_INSTRUCTIONS[instruction],
                PATCHED_INSTRUCTIONS[instruction],
            }]

    def get_goal_status(self, server_locations):
        """Collect the current status of the goal conditions"""
        goal_conditions = "The current status of the unfinished goal requirements:"
        completed_requirements = "\n\nThe following requirements are already completed:"
        collected_sewer = self.crystals_current + self.crystals_traded
        collected_tbolts = self.titanium_bolt_count()
        completed_planets = len(self.visited_planets)
        completion_locations = get_completion_location_names(
            (LOCATION_FROM_AP_CODE[code] for code in server_locations), bool(self.options.lock_cc)
        )
        required_locations = (self.options.goal_completion * len(completion_locations) + 99) // 100
        checked_locations = len(self.checked_locations & completion_locations)
        if self.options.goal_nano > 10:
            if self.options.goal_nano > self.max_health:
                goal_conditions += f"\n- Nanotech level requirement ({self.max_health}/{self.options.goal_nano})"
            else:
                completed_requirements += "\n- Nanotech requirement completed!"
        if self.options.goal_crystal > 0:
            if self.options.goal_crystal > collected_sewer:
                goal_conditions += f"\n- Collect Sewer Crystals ({collected_sewer}/{self.options.goal_crystal})"
            else:
                completed_requirements += "\n- Sewer Crystal requirement completed!"
        if self.options.goal_tbolts > 0:
            if self.options.goal_tbolts > collected_tbolts:
                goal_conditions += f"\n- Collect Titanium Bolts ({collected_tbolts}/{self.options.goal_tbolts})"
            else:
                completed_requirements += "\n- Titanium Bolts (AP item) requirement completed!"
        if self.options.goal_skillpoints > 0:
            if self.options.goal_skillpoints > self.skillpoints:
                goal_conditions += f"\n- Skillpoints completed ({self.skillpoints}/{self.options.goal_skillpoints})"
            else:
                completed_requirements += "\n- Skillpoints requirement completed!"
        if self.options.goal_planets:
            if self.options.goal_planets > completed_planets:
                goal_conditions += f"\n- Planets completed ({completed_planets}/{self.options.goal_planets})"
            else:
                completed_requirements += "\n- Planet completion requirement completed!"
        if self.options.goal_completion > 0:
            if checked_locations < required_locations:
                goal_conditions += (f"\n- Locations collected ({checked_locations}/{required_locations}) "
                                    f"for {self.options.goal_completion}% requirement")
            else:
                completed_requirements += f"\n- Location collection percentage requirement completed!"
        if self.options.goal_qwark:
            if not self.qwarktastic:
                goal_conditions += f"\n- Complete the Qwarktastic Battle on Annihilation Nation!"
            else:
                completed_requirements += f"\n- Qwarktastic battle completed!"
        if self.options.goal_museum:
            if not self.museum_unlocked:
                goal_conditions += "\n- Unlock the Insomniac Museum teleporter in the Phoenix Trophy Room!"
            else:
                completed_requirements += "\n- Insomniac Museum teleporter unlocked!"
            if not self.museum_visited:
                goal_conditions += "\n- Visit the Insomniac Museum!"
            else:
                completed_requirements += "\n- Insomniac Museum visited!"
        if self.options.goal_boss_qwark:
            if not self.boss_qwark:
                goal_conditions += f"\n- Defeat Captain Qwark on Florana!"
            else:
                completed_requirements += f"\n- Captain Qwark defeated!"
        if self.options.goal_boss_two:
            if not self.boss_two:
                goal_conditions += f"\n- Defeat the Terrible Two on Annihilation Nation!"
            else:
                completed_requirements += f"\n- Terrible Two defeated!"
        if self.options.goal_boss_noid:
            if not self.boss_noid:
                goal_conditions += f"\n- Defeat Momma Tyhrranoid on Tyhrranosis!"
            else:
                completed_requirements += f"\n- Momma Tyhrranoid defeated!"
        if self.options.goal_boss_warship:
            if not self.boss_warship:
                goal_conditions += f"\n- Defeat the Warship on Daxx!"
            else:
                completed_requirements += f"\n- Daxx Warship defeated!"
        if self.options.goal_boss_scorpio:
            if not self.boss_scorpio:
                goal_conditions += f"\n- Defeat Scorpio on Annihilation Nation!"
            else:
                completed_requirements += f"\n- Scorpio defeated!"
        if self.options.goal_boss_talos:
            if self.options.shortcuts.get(RAC3SHORTCUTS.HOLOSTAR_CLANK, False):
                completed_requirements += "\n- Terror of Talos skipped via Holostar Skip Clank!"
            elif self.boss_talos:
                completed_requirements += "\n- Terror of Talos defeated!"
            else:
                goal_conditions += "\n- Defeat the Terror of Talos as Giant Clank on Holostar Studios!"
        if self.options.goal_boss_gears:
            if not self.boss_gears:
                goal_conditions += f"\n- Defeat Courtney Gears on Obani Draco!"
            else:
                completed_requirements += f"\n- Courtney Gears defeated!"
        if self.options.goal_boss_klunk:
            if not self.boss_klunk:
                goal_conditions += f"\n- Defeat Klunk on Metropolis!"
            else:
                completed_requirements += f"\n- Klunk defeated!"
        if self.options.goal_nef:
            if not self.boss_nef:
                goal_conditions += f"\n- Defeat Dr. Nefarious on Command Center!"
            else:
                completed_requirements += f"\n- Dr. Nefarious defeated!"
        if self.options.goal_bio:
            if not self.boss_bio:
                goal_conditions += f"\n- Defeat the Biobliterator on Command Center!"
            else:
                completed_requirements += f"\n- Biobliterator defeated!"
        logger.info(goal_conditions + completed_requirements)
