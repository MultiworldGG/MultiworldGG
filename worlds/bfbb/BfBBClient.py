import asyncio
import os.path
import shutil
import subprocess
import sys
import time
import traceback
import zipfile
from enum import Flag
from typing import Callable, Optional, Any, Dict, Tuple

import dolphin_memory_engine

import Utils
import settings

tracker_loaded = False
try:
    if settings.get_settings().get('bfbb_options', {}).get('use_tracker', True):
        from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
        from worlds.tracker.TrackerClient import TrackerCommandProcessor as SuperClientCommandProcessor
        tracker_loaded = True
    else:
        from CommonClient import CommonContext as SuperContext
        from CommonClient import ClientCommandProcessor as SuperClientCommandProcessor
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext
    from CommonClient import ClientCommandProcessor as SuperClientCommandProcessor
from CommonClient import server_loop, gui_enabled, logger, \
    get_base_parser, handle_url_arg
from settings import get_settings
from .Rom import BfBBContainer

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"


class CheckTypes(Flag):
    SPAT = 1
    SOCK = 2
    SKILLS = 4
    GOLDEN_UNDERWEAR = 8
    LEVEL_ITEMS = 16
    PURPLE_SO = 32


CONNECTION_REFUSED_VANILLA_GAME_STATUS = "Vanilla game detected. Please load the patched game."
CONNECTION_REFUSED_GAME_STATUS = "Dolphin Connection refused due to invalid Game. Please load the US Version of BfBB or if you already do, restart dolphin."
CONNECTION_REFUSED_SAVE_STATUS = "Dolphin Connection refused due to invalid Save. " \
                                 "Please make sure you loaded a save file used on this slot and seed."
CONNECTION_LOST_STATUS = "Dolphin Connection was lost. Please restart your emulator and make sure BfBB is running."
CONNECTION_CONNECTED_STATUS = "Dolphin Connected"
CONNECTION_INITIAL_STATUS = "Dolphin Connection has not been initiated"

GAME_ID = b'GQPE78'

SCENE_OBJ_LIST_PTR_ADDR = 0x803cb9ec
SCENE_OBJ_LIST_SIZE_ADDR = 0x803cac08

CUR_SCENE_PTR_ADDR = 0x803c2518

GLOBALS_ADDR = 0x803c0558

HEALTH_ADDR = GLOBALS_ADDR + 0x16B0
MAX_HEALTH_ADDR = GLOBALS_ADDR + 0x1738
SHINY_COUNT_ADDR = GLOBALS_ADDR + 0x1B00
SPAT_COUNT_ADDR = GLOBALS_ADDR + 0x1B04
SOCK_PER_LEVEL_COUNT_ADDR = GLOBALS_ADDR + 0x1B08
# MAX_SOCK_PER_LEVEL_ADDR = GLOBALS_ADDR + 0x1B44
# SOCK_CURRENT_LEVEL_ADDR = GLOBALS_ADDR + 0x1B80
LEVEL_PICKUP_PER_LEVEL_ADDR = GLOBALS_ADDR + 0x1b84
# LEVEL_PICKUP_CURRENT_LEVEL_ADDR = GLOBALS_ADDR + 0x1bc0
SOCK_COUNT_ADDR = GLOBALS_ADDR + 0x1BC4
POWERUPS_ADDR = 0x803c0f15
PLAYER_ADDR = 0x803C0C38
PLAYER_CONTROL_OWNER = 0x803c1ce0
PLAYER_SETTINGS_PRT_ADDR = 0x803c0f1c

# AP free space usage
# notes on free space
# 0x817FFFF6 - 0x817FFFFF
# around 0x8179f890-0x817fcf00 (?)

# @0x817f0080 save game write injection code
# @0x817f0400 save game read injection code


SLOT_NAME_ADDR = 0x8028F2a0
SEED_ADDR = SLOT_NAME_ADDR + 0x40
# we currently write/read 0x20 bytes starting from 0x817f0000 to/from save game
# we could extend up to 0x80 bytes or more if we move AP code from 0x817f0080 to somewhere else
# expected received item index
EXPECTED_INDEX_ADDR = 0x817f0000
# delayed item
BALLOON_KID_COUNT_ADDR = 0x817f0004
SANDMAN_COUNT_ADDR = 0x817f0005
POWER_CRYSTAL_COUNT_ADDR = 0x817f0006
CANNON_BUTTON_COUNT_ADDR = 0x817f0007
SAVED_SLOT_NAME_ADDR = 0x817f0020
SAVED_SEED_ADDR = SAVED_SLOT_NAME_ADDR + 0x40
# some custom code at 0x817f0080


# Changes to HIPs needed
# remove GiveCollectable link from King JF in JF04
# remove Decrement BALLOON_COUNTER and GiveCollectable links from GL01 balloon platforms
# remove Decrement BALLOON_COUNTER from GL01 BALLON_X_COUNT_DISP
# remove GiveCollectable links from bc02/bc03/bc04 sec buttons
# remove Decrement SANDMAN_COUNTER links from sm03 sandmans
# remove GiveCollectable links from kf01/kf02/kf04 lost camper triggers
# remove Increment MATTS_CRYSTAL_COUNTER link from kf04 powercrystals
# remove Decrement BUTTON_COUNTER and GiveCollectable links from gy03 buttons 1-4
# remove Decrement BUTTON_COUNTER from gy03 BUTTON_DISPs
# remove GivePowerUp from b101 DeathCutscene and b201 RoboPatrickNPC

base_id = 1490000

SOCK_PICKUP_IDS = {
    (base_id + 100 + 0): (b'HB01', 0x39fe1ac4),  # behind trash
    (base_id + 100 + 1): (b'HB01', 0x39fe1ac5),  # on fountain
    (base_id + 100 + 2): (b'HB01', 0x39fe1ac7),  # patrick
    # (base_id + 100 + ?): (b'HB01', 0x7fd6ed10), # TEMP SOCK??
    (base_id + 100 + 3): (b'HB02', 0x39fe1ac4),  # lib
    (base_id + 100 + 4): (b'HB03', 0x39fe1ac4),  # squid
    (base_id + 100 + 5): (b'HB04', 0x39fe1ac4),  # pat
    (base_id + 100 + 6): (b'HB06', 0x39fe1ac4),  # shoals
    (base_id + 100 + 7): (b'HB07', 0x8361f615),  # kk
    (base_id + 100 + 8): (b'JF01', 0x39fe1ac4),  # on JF rock
    (base_id + 100 + 9): (b'JF01', 0x39fe1ac5),  # near bungee
    (base_id + 100 + 10): (b'JF01', 0x39fe1ac6),  # on island
    (base_id + 100 + 11): (b'JF01', 0x39fe1ac7),  # on fountain
    (base_id + 100 + 12): (b'JF01', 0x39fe1ac8),  # on water
    (base_id + 100 + 13): (b'JF01', 0x39fe1ac9),  # bowling
    (base_id + 100 + 14): (b'JF02', 0x39fe1ac4),  # on slide 1
    (base_id + 100 + 15): (b'JF02', 0x39fe1ac5),  # on plat after slide 1
    (base_id + 100 + 16): (b'JF02', 0x39fe1ac6),  # on plat in cave before slide 2
    (base_id + 100 + 17): (b'JF02', 0x39fe1ac7),  # on water in cave
    (base_id + 100 + 18): (b'JF03', 0x485e3882),  # on plat near flower/ leaning plat/gate
    (base_id + 100 + 19): (b'JF03', 0x485e3883),  # flying tiki minigame
    (base_id + 100 + 20): (b'JF03', 0x485e3884),  # plat near waterfall
    (base_id + 100 + 21): (b'JF04', 0x8269bea9),  # on slide
    (base_id + 100 + 22): (b'BB01', 0x7319bbfc),  # on broken house
    (base_id + 100 + 23): (b'BB01', 0x7319bbfd),  # in broken house by tartar
    (base_id + 100 + 24): (b'BB01', 0x7319bbfe),  # on floating plat
    (base_id + 100 + 25): (b'BB01', 0x7319bbff),  # on copper house railing
    (base_id + 100 + 26): (b'BB02', 0x08857ce6),  # on windmill
    (base_id + 100 + 27): (b'BB02', 0x08857ce7),  # on orange rooftop/ under slide
    (base_id + 100 + 28): (b'BB02', 0x08857ce8),  # behind lighthouse
    (base_id + 100 + 29): (b'BB03', 0x4d73f257),  # in lighthouse
    (base_id + 100 + 30): (b'BB04', 0x7319bbfc),  # in sea needle
    (base_id + 100 + 31): (b'GL01', 0x70848599),  # on watchtower on island
    (base_id + 100 + 32): (b'GL01', 0x7084859a),  # in sand castle
    (base_id + 100 + 33): (b'GL01', 0x7084859b),  # on juice bar
    (base_id + 100 + 34): (b'GL01', 0x7084859c),  # on top of sand castle
    (base_id + 100 + 35): (b'GL01', 0x7084859d),  # on sand castle entrance gate
    (base_id + 100 + 36): (b'GL02', 0x70848599),  # under ledge in cave
    (base_id + 100 + 37): (b'GL02', 0x7084859a),  # on water in cave
    (base_id + 100 + 38): (b'GL02', 0x7084859b),  # on side ledge in cave
    (base_id + 100 + 39): (b'GL03', 0x93d05cf9),  # tiki minigame
    (base_id + 100 + 40): (b'GL03', 0x93d05cfa),  # ice skating dupli
    (base_id + 100 + 41): (b'GL03', 0x93d05cfb),  # on booth
    (base_id + 100 + 42): (b'RB01', 0xa17bd220),  # on roof near elevator
    (base_id + 100 + 43): (b'RB01', 0xa17bd221),  # on rock
    (base_id + 100 + 44): (b'RB01', 0xa17bd222),  # near slide
    (base_id + 100 + 45): (b'RB02', 0xa122b810),  # near exit ledge
    (base_id + 100 + 46): (b'RB02', 0xa122b811),  # midway right ledge
    (base_id + 100 + 47): (b'RB02', 0xa122b812),  # on entrance
    (base_id + 100 + 48): (b'RB03', 0x7b0c4887),  # bungee
    (base_id + 100 + 49): (b'RB03', 0x7b0c4888),  # near dupli
    (base_id + 100 + 50): (b'RB03', 0x7b0c4889),  # button under laser plat
    (base_id + 100 + 51): (b'BC01', 0x93d05cf9),  # bungee
    (base_id + 100 + 52): (b'BC02', 0x4d73f257),  # top of middle plat
    (base_id + 100 + 53): (b'BC03', 0x93d05cf9),  # clamp
    (base_id + 100 + 54): (b'BC04', 0x93d05cf9),  # behind tilting plat
    (base_id + 100 + 55): (b'SM01', 0x4d73f257),  # below bridge
    (base_id + 100 + 56): (b'SM01', 0x4d73f258, 0xa255034a),  # snowman
    (base_id + 100 + 57): (b'SM02', 0x4d73f257),  # legde near start
    (base_id + 100 + 58): (b'SM02', 0x4d73f258),  # underpass
    (base_id + 100 + 59): (b'SM02', 0x4d73f259),  # plat near end
    (base_id + 100 + 60): (b'SM03', 0x4a531868),  # at end
    (base_id + 100 + 61): (b'SM03', 0x4a531869),  # on last tunnel near end
    (base_id + 100 + 62): (b'SM04', 0x4a531868),  # top ledge near start
    (base_id + 100 + 63): (b'SM04', 0x4a531869),  # in cave
    (base_id + 100 + 64): (b'SM04', 0x4a53186a),  # on ice plat
    (base_id + 100 + 65): (b'KF01', 0x8361f615),  # on high plat near puff
    (base_id + 100 + 66): (b'KF01', 0x8361f616),  # at waterfall near kid
    (base_id + 100 + 67): (b'KF01', 0x8361f617),  # tiki bowling
    (base_id + 100 + 68): (b'KF02', 0x39fe1ac4),  # on ledge with glove
    (base_id + 100 + 69): (b'KF02', 0x39fe1ac5),  # on tiki stack near arf
    (base_id + 100 + 70): (b'KF04', 0xa9fa6889),  # on ledge near ent/box
    (base_id + 100 + 71): (b'KF05', 0x4d9f3243),  # on slide halfway-ish
    (base_id + 100 + 72): (b'GY01', 0x93d05cf9),  # on plat in middle
    (base_id + 100 + 73): (b'GY02', 0x93d05cf9),  # inside ship wreck
    (base_id + 100 + 74): (b'GY03', 0x93d05cf9),  # on rope
    (base_id + 100 + 75): (b'DB02', 0x4a531868),  # on top ledge after swinger before skulls
    (base_id + 100 + 76): (b'DB02', 0x4a531869),  # oil tower bottom
    (base_id + 100 + 77): (b'DB02', 0x4a53186a),  # swingers plat
    (base_id + 100 + 78): (b'DB03', 0x93d05cf9),  # in air at tramp
    (base_id + 100 + 79): (b'DB04', 0x93d05cf9),  # on floating tiki
}
# (spat name, scene id, id)
SPAT_PICKUP_IDS = {
    (base_id + 0): (b'HB01', 0xe0886670),
    (base_id + 1): (b'HB01', 0xe0886671),
    (base_id + 2): (b'HB01', 0xe0886672),
    (base_id + 3): (b'HB02', 0x35e915c0),
    (base_id + 4): (b'HB03', 0x23264b51),
    (base_id + 5): (b'HB05', 0xb7fd0b01),
    (base_id + 6): (b'HB01', 0xe0886675),
    (base_id + 7): (b'HB08', 0xf70f6fe7),
    (base_id + 8): (b'JF01', 0xe5cc6afe),
    (base_id + 9): (b'JF01', 0xe5cc6aff),
    (base_id + 10): (b'JF02', 0xcaaacd23),
    (base_id + 11): (b'JF02', 0xcaaacd22),
    (base_id + 12): (b'JF03', 0x1bd186f6),
    (base_id + 13): (b'JF03', 0x1bd186f5),
    (base_id + 14): (b'JF04', 0x6a90778d),
    (base_id + 15): (b'JF01', 0xe5cc6b00),
    (base_id + 16): (b'BB01', 0xc763bce0),
    (base_id + 17): (b'BB01', 0xc763bce1),
    (base_id + 18): (b'BB01', 0xc763bce2),
    (base_id + 19): (b'BB02', 0xc763bce0),
    (base_id + 20): (b'BB02', 0xc763bce1),
    (base_id + 21): (b'BB03', 0x35e915c0),
    (base_id + 22): (b'BB04', 0x35e915c0),
    (base_id + 23): (b'BB04', 0x35e915c1),
    (base_id + 24): (b'GL01', 0xf70f6fe7),
    (base_id + 25): (b'GL01', 0xf70f6fe8),
    (base_id + 26): (b'GL01', 0xf70f6fe9),
    (base_id + 27): (b'GL01', 0xf70f6fea),
    (base_id + 28): (b'GL02', 0xf70f6feb),
    (base_id + 29): (b'GL03', 0xf70f6fec),
    (base_id + 30): (b'GL03', 0xf70f6fed),
    (base_id + 31): (b'GL03', 0xf70f6fee),
    (base_id + 32): (b'B101', 0xe13ad616),
    (base_id + 33): (b'RB01', 0x0f74bf40),
    (base_id + 34): (b'RB01', 0x0f74bf41),
    (base_id + 35): (b'RB01', 0x0f74bf42),
    (base_id + 36): (b'RB01', 0x0f74bf43),
    (base_id + 37): (b'RB02', 0x0f74bf40),
    (base_id + 38): (b'RB03', 0x35e915c1),
    (base_id + 39): (b'RB03', 0x35e915c0),
    (base_id + 40): (b'RB03', 0x35e915c2),
    (base_id + 41): (b'BC01', 0xf70f6fe7),
    (base_id + 42): (b'BC02', 0xf70f6fe8),
    (base_id + 43): (b'BC02', 0xf70f6fe9),
    (base_id + 44): (b'BC02', 0xf70f6fea),
    (base_id + 45): (b'BC02', 0xf70f6feb),
    (base_id + 46): (b'BC03', 0xf70f6fec),
    (base_id + 47): (b'BC04', 0xf70f6fed),
    (base_id + 48): (b'BC05', 0xf70f6fee),
    (base_id + 49): (b'SM01', 0x35e915c0),
    (base_id + 50): (b'SM01', 0x35e915c1),
    (base_id + 51): (b'SM02', 0xe877614a),
    (base_id + 52): (b'SM02', 0xe877614b),
    (base_id + 53): (b'SM03', 0xf70f6fe7),
    (base_id + 54): (b'SM03', 0xf70f6fe8),
    (base_id + 55): (b'SM04', 0x35e915c0),
    (base_id + 56): (b'SM04', 0x35e915c1),
    (base_id + 57): (b'B201', 0x35e915c0),
    (base_id + 58): (b'KF01', 0x69f03106),
    (base_id + 59): (b'KF01', 0x69f03107),
    (base_id + 60): (b'KF02', 0x2af58ccd),
    (base_id + 61): (b'KF02', 0x2af58cce),
    (base_id + 62): (b'KF04', 0x35e915c4),
    (base_id + 63): (b'KF04', 0x35e915c5),
    (base_id + 64): (b'KF05', 0xf70f6fe7),
    (base_id + 65): (b'KF05', 0xf70f6fe8),
    (base_id + 66): (b'GY01', 0xf70f6fe7),
    (base_id + 67): (b'GY01', 0xf70f6fe8),
    (base_id + 68): (b'GY01', 0xf70f6fe9),
    (base_id + 69): (b'GY02', 0xf70f6fea),
    (base_id + 70): (b'GY02', 0xf70f6feb),
    (base_id + 71): (b'GY03', 0xf70f6fec),
    (base_id + 72): (b'GY03', 0xf70f6fed),
    (base_id + 73): (b'GY04', 0xf70f6fee),
    (base_id + 74): (b'DB01', 0x35e915c0),
    (base_id + 75): (b'DB01', 0x35e915c1),
    (base_id + 76): (b'DB02', 0x0f74bf40),
    (base_id + 77): (b'DB02', 0x0f74bf41),
    (base_id + 78): (b'DB03', 0xf70f6feb),
    (base_id + 79): (b'DB04', 0x35e915c5),
    (base_id + 80): (b'DB01', 0x35e915c6),
    (base_id + 81): (b'DB05', 0x35e915c7),
    (base_id + 82): (b'B302', 0xf70f6fe7),
    (base_id + 83): (b'B302', 0xf70f6fe8),
    (base_id + 84): (b'HB01', 0xc08d3390),
    (base_id + 85): (b'HB01', 0xc08d3391),
    (base_id + 86): (b'HB01', 0xc08d3392),
    (base_id + 87): (b'HB01', 0xc08d3393),
    (base_id + 88): (b'HB01', 0xc08d3394),
    (base_id + 89): (b'HB01', 0xc08d3395),
    (base_id + 90): (b'HB01', 0xc08d3396),
    (base_id + 91): (b'HB01', 0xc08d3397),
    (base_id + 92): (b'HB01', 0xecd3e66c, 0xecd3e6ef, 0xecd32772),
    (base_id + 93): (b'HB01', 0xecd3e66d, 0xecd3e6f0, 0xecd32773),
    (base_id + 94): (b'HB01', 0xecd3e66e, 0xecd3e6f1, 0xecd32774),
    (base_id + 95): (b'HB01', 0xecd3e66f, 0xecd3e6f2, 0xecd32775),
    (base_id + 96): (b'HB01', 0xecd3e670, 0xecd3e6f3, 0xecd32776),
    (base_id + 97): (b'HB01', 0xecd3e671, 0xecd3e6f4, 0xecd32777),
    (base_id + 98): (b'HB01', 0xecd3e672, 0xecd3e6f5, 0xecd32778),
    (base_id + 99): (b'HB01', 0xecd3e673, 0xecd3e6f6, 0xecd32779),
}
SPAT_COUNTER_IDS = {
    (base_id + 0): (None, 0x5f45b825),
    (base_id + 1): (None, 0x5f45b826),
    (base_id + 2): (None, 0x5f45b827),
    (base_id + 3): (None, 0x5f45b828),
    (base_id + 4): (None, 0x5f45b829),
    (base_id + 5): (None, 0x5f45b82a),
    (base_id + 6): (None, 0x5f45b82b),
    (base_id + 7): (None, 0x5f45b82c),
    (base_id + 8): (None, 0x5caad1af),
    (base_id + 9): (None, 0x5caad1b0),
    (base_id + 10): (None, 0x5caad1b1),
    (base_id + 11): (None, 0x5caad1b2),
    (base_id + 12): (None, 0x5caad1b3),
    (base_id + 13): (None, 0x5caad1b4),
    (base_id + 14): (None, 0x5caad1b5),
    (base_id + 15): (None, 0x5caad1b6),
    (base_id + 16): (None, 0x9af0a293),
    (base_id + 17): (None, 0x9af0a294),
    (base_id + 18): (None, 0x9af0a295),
    (base_id + 19): (None, 0x9af0a296),
    (base_id + 20): (None, 0x9af0a297),
    (base_id + 21): (None, 0x9af0a298),
    (base_id + 22): (None, 0x9af0a299),
    (base_id + 23): (None, 0x9af0a29a),
    (base_id + 24): (None, 0x946d626c),
    (base_id + 25): (None, 0x946d626d),
    (base_id + 26): (None, 0x946d626e),
    (base_id + 27): (None, 0x946d626f),
    (base_id + 28): (None, 0x946d6270),
    (base_id + 29): (None, 0x946d6271),
    (base_id + 30): (None, 0x946d6272),
    (base_id + 31): (None, 0x946d6273),
    (base_id + 32): (None, 0x917b7f42),
    (base_id + 33): (None, 0xfbd386c3),
    (base_id + 34): (None, 0xfbd386c4),
    (base_id + 35): (None, 0xfbd386c5),
    (base_id + 36): (None, 0xfbd386c6),
    (base_id + 37): (None, 0xfbd386c7),
    (base_id + 38): (None, 0xfbd386c8),
    (base_id + 39): (None, 0xfbd386c9),
    (base_id + 40): (None, 0xfbd386ca),
    (base_id + 41): (None, 0x5f42d1d4),
    (base_id + 42): (None, 0x5f42d1d5),
    (base_id + 43): (None, 0x5f42d1d6),
    (base_id + 44): (None, 0x5f42d1d7),
    (base_id + 45): (None, 0x5f42d1d8),
    (base_id + 46): (None, 0x5f42d1d9),
    (base_id + 47): (None, 0x5f42d1da),
    (base_id + 48): (None, 0x5f42d1db),
    (base_id + 49): (None, 0xe169bcd1),
    (base_id + 50): (None, 0xe169bcd2),
    (base_id + 51): (None, 0xe169bcd3),
    (base_id + 52): (None, 0xe169bcd4),
    (base_id + 53): (None, 0xe169bcd5),
    (base_id + 54): (None, 0xe169bcd6),
    (base_id + 55): (None, 0xe169bcd7),
    (base_id + 56): (None, 0xe169bcd8),
    (base_id + 57): (None, 0x55cdae83),
    (base_id + 58): (None, 0xd2b8fff2),
    (base_id + 59): (None, 0xd2b8fff3),
    (base_id + 60): (None, 0xd2b8fff4),
    (base_id + 61): (None, 0xd2b8fff5),
    (base_id + 62): (None, 0xd2b8fff6),
    (base_id + 63): (None, 0xd2b8fff7),
    (base_id + 64): (None, 0xd2b8fff8),
    (base_id + 65): (None, 0xd2b8fff9),
    (base_id + 66): (None, 0x8c99c8b9),
    (base_id + 67): (None, 0x8c99c8ba),
    (base_id + 68): (None, 0x8c99c8bb),
    (base_id + 69): (None, 0x8c99c8bc),
    (base_id + 70): (None, 0x8c99c8bd),
    (base_id + 71): (None, 0x8c99c8be),
    (base_id + 72): (None, 0x8c99c8bf),
    (base_id + 73): (None, 0x8c99c8c0),
    (base_id + 74): (None, 0x870cff19),
    (base_id + 75): (None, 0x870cff1a),
    (base_id + 76): (None, 0x870cff1b),
    (base_id + 77): (None, 0x870cff1c),
    (base_id + 78): (None, 0x870cff1d),
    (base_id + 79): (None, 0x870cff1e),
    (base_id + 80): (None, 0x870cff1f),
    (base_id + 81): (None, 0x870cff20),
    (base_id + 82): (None, 0x1a1fddc4),
    (base_id + 83): (None, 0x1a1fddc5),
    (base_id + 84): (None, 0x192c4d8e),
    (base_id + 85): (None, 0x192c4d8f),
    (base_id + 86): (None, 0x192c4d90),
    (base_id + 87): (None, 0x192c4d91),
    (base_id + 88): (None, 0x192c4d92),
    (base_id + 89): (None, 0x192c4d93),
    (base_id + 90): (None, 0x192c4d94),
    (base_id + 91): (None, 0x192c4d95),
    (base_id + 92): (None, 0xcae5663f),
    (base_id + 93): (None, 0xcae56640),
    (base_id + 94): (None, 0xcae56641),
    (base_id + 95): (None, 0xcae56642),
    (base_id + 96): (None, 0xcae56643),
    (base_id + 97): (None, 0xcae56644),
    (base_id + 98): (None, 0xcae56645),
    (base_id + 99): (None, 0xcae56646),
}
# golden underware ids
# 0x3E3DE77 - 79
GOLDEN_UNDERWEAR_IDS = {
    (base_id + 180): (b'HB01', 0x3E3DE77),
    (base_id + 181): (b'HB01', 0x3E3DE78),
    (base_id + 182): (b'HB01', 0x3E3DE79)
}
KING_JF_DISP_ID = {
    (base_id + 183 + 0): (b'JF04', 0xb4e7cb55),
}
STEERING_WHEEL_PICKUP_IDS = {
    (base_id + 183 + 1): (b'BB01', 0x62f79b31),  # on tikis near start
    (base_id + 183 + 2): (b'BB01', 0x62f79b32),  # on canopy near house
    (base_id + 183 + 3): (b'BB01', 0x62f79b33),  # on house with cannon near exit
    (base_id + 183 + 4): (b'BB01', 0x62f79b34),  # on crashed boat near sea needle
    (base_id + 183 + 5): (b'BB01', 0x62f79b35),  # near hole
    (base_id + 183 + 6): (b'BB02', 0xa8d10901),  # on pipe near start
    (base_id + 183 + 7): (b'BB02', 0xa8d10902),  # on orange rooftop under slide
    (base_id + 183 + 8): (b'BB02', 0xa8d10903),  # on floating plats
    (base_id + 183 + 9): (b'BB03', 0x03f22dda),  # bottom light tower
    (base_id + 183 + 10): (b'BB04', 0x62f79b31),  # east door sea needle
    (base_id + 183 + 11): (b'BB04', 0x62f79b32),  # north door sea needle
}
BALLOON_KID_COUNTER_ID = (b'GL01', 0xa6662680)
BALLOON_KID_TASKBOX_ID = (b'GL01', 0xa416ce3b)
BALLOON_KID_SUC_TRIG_ID = (b'GL01', 0xa4883601)
BALLOON_KID_PLAT_IDS = {
    (base_id + 183 + 12): (b'GL01', 0x3db4fe59),  # near puff
    (base_id + 183 + 13): (b'GL01', 0x393949cc),  # near swinging logs
    (base_id + 183 + 14): (b'GL01', 0x34bd953f),  # near sinking logs
    (base_id + 183 + 15): (b'GL01', 0x3041e0b2),  # on water 1
    (base_id + 183 + 16): (b'GL01', 0x2bc62c25),  # on water 2
}
ART_WORK_IDS = {
    (base_id + 183 + 17): (b'RB01', 0xcad32f04),  # near tramp
    (base_id + 183 + 18): (b'RB01', 0xcad32f05),  # near start
    (base_id + 183 + 19): (b'RB02', 0xcad32f06),  # bottom
    (base_id + 183 + 20): (b'RB02', 0xcad32f07),  # near exit
    (base_id + 183 + 21): (b'RB03', 0x40152776),  # behind laser
    (base_id + 183 + 22): (b'RB03', 0x40152777),  # on sleepytime plat
}
OVERRIDE_BUTTON_IDS = {
    (base_id + 183 + 23): (b'BC02', 0x5e64831b),  # at comp
    (base_id + 183 + 24): (b'BC02', 0x5e64831c),  # at lasers
    (base_id + 183 + 25): (b'BC03', 0x91f2a6cf),  # top tunnel
    (base_id + 183 + 26): (b'BC04', 0xc1841225),  # ball
}
SANDMAN_SOCK_ID = SOCK_PICKUP_IDS[(base_id + 100 + 60)]
SANDMAN_CNTR_ID = (b'SM03', 0xc4e703d6)  # starts at 8
SANDMAN_DSTR_IDS = {
    (base_id + 183 + 27): (b'SM03', 0xd4d3bec2),  # at start
    (base_id + 183 + 28): (b'SM03', 0xd4d3bec3),  # lower path after first turn
    (base_id + 183 + 29): (b'SM03', 0xd4d3bec4),  # on shortcut
    (base_id + 183 + 30): (b'SM03', 0xd4d3bec5),  # on right spiral
    (base_id + 183 + 31): (b'SM03', 0xd4d3bec6),  # on left spiral
    (base_id + 183 + 32): (b'SM03', 0xd4d3bec7),  # middle of 1st 3-way split near end
    (base_id + 183 + 33): (b'SM03', 0xd4d3bec8),  # left path of 1st 3-way split near end
    (base_id + 183 + 34): (b'SM03', 0xd4d3bec9),  # on turn after cave
}
LOST_CAMPER_TRIG_IDS = {
    (base_id + 183 + 35): (b'KF01', 0x153CCF73),  # near puff
    (base_id + 183 + 36): (b'KF01', 0x153CCF74),  # near waterfall
    (base_id + 183 + 37): (b'KF01', 0x153CCF75),  # near exit
    (base_id + 183 + 38): (b'KF02', 0x9c2d8bb3),  # not at gate 4Head
    (base_id + 183 + 39): (b'KF02', 0x9c2d8bb4),  # at gate
    (base_id + 183 + 40): (b'KF04', 0x609203fd),  # near end
}
POWERCRYSTAL_TASKBOX_IDS = [
    (b'KF04', 0xed5ab88e),  # bob
    (b'KF04', 0x419f15d3),  # pat
]
POWERCRYSTAL_COUNTER_ID = (b'KF04', 0xed81694f)
POWERCRYSTAL_PICKUP_IDS = {
    (base_id + 183 + 41): (b'KF04', 0x96017696),  # behind 1st gate
    (base_id + 183 + 42): (b'KF04', 0x96017697),  # top water room before 2 gate near button
    (base_id + 183 + 43): (b'KF04', 0x96017698),  # top near 3 gate
    (base_id + 183 + 44): (b'KF04', 0x96017699),  # top big room
    (base_id + 183 + 45): (b'KF04', 0x9601769a),  # top tall vine
    (base_id + 183 + 46): (b'KF04', 0x9601769b),  # top last room
}

# CANNON_BUTTON_COUNTER_ID = 0x9a101de7
CANNON_BUTTON_DISP_IDS = [
    (b'GY03', 0x46d4fa25),
    (b'GY03', 0x46d4fa26),
    (b'GY03', 0x46d4fa27),
    (b'GY03', 0x46d4fa28),
]
CANNON_BUTTON_SPAT_ID = SPAT_PICKUP_IDS[(base_id + 71)]
CANNON_BUTTON_PLAT_IDS = [
    (b'GY03', 0x6d1f11b4),  # spring
    (b'GY03', 0xc60e4bcf),  # chest closed
    (b'GY03', 0x5950cb1d),  # chest open
]
# CANNON_DONE_DISP_ID = (b'GY03', 0x979347fd)
CANNON_BUTTON_IDS = {
    (base_id + 183 + 47): (b'GY03', 0x1344a38c),  # on deck
    (base_id + 183 + 48): (b'GY03', 0x1344a38d),  # on middle mast
    (base_id + 183 + 49): (b'GY03', 0x1344a38e),  # on front mast
    (base_id + 183 + 50): (b'GY03', 0x1344a38f),  # near steering wheel
    # (b'GY03', 0x1344a390), # in chest
}
PURPLE_SO_IDS = {
    (base_id + 236 + 0): (b'HB01', 0x2f49f01c),  # behind CB
    (base_id + 236 + 1): (b'JF01', 0xc94ad407),  # on island
    (base_id + 236 + 2): (b'JF02', 0x2193f576),  # on goo
    (base_id + 236 + 3): (b'JF03', 0xb75df2ce),  # on goo under bridge
    (base_id + 236 + 4): (b'JF04', 0x2193f576),  # on slide
    (base_id + 236 + 5): (b'BB01', 0xffd417af),  # at fenced off glove near lighthouse
    (base_id + 236 + 6): (b'BB01', 0x2193f576),  # on platform near lighthouse
    (base_id + 236 + 7): (b'BB02', 0xf68f73a6),  # on flying platform
    (base_id + 236 + 8): (b'BB02', 0xf68f73a7),  # on top of windmill blades
    (base_id + 236 + 9): (b'BB03', 0xf68f73a6),  # in tiki stack
    (base_id + 236 + 10): (b'BB04', 0x2193f576),  # south door
    (base_id + 236 + 11): (b'GL01', 0x2193f576),  # end of log path near ms puff
    (base_id + 236 + 12): (b'GL02', 0x2193f576),  # on ledge under checkpoint
    (base_id + 236 + 13): (b'GL03', 0x2193f576),  # on tikis after slide
    (base_id + 236 + 14): (b'RB01', 0x752e0aa8),  # under swing along spat
    (base_id + 236 + 15): (b'RB02', 0x6d07a8bc),  # near roof
    (base_id + 236 + 16): (b'RB03', 0x6d07a8bc),  # on tikis near exit
    (base_id + 236 + 17): (b'BC01', 0x2193f576),  # dupli bowling
    (base_id + 236 + 18): (b'BC02', 0x2193f576),  # in hidden cave near entrance
    (base_id + 236 + 19): (b'BC02', 0x2193f577),  # on slide
    (base_id + 236 + 20): (b'BC03', 0x2193f576),  # above disco floor/ about half way
    (base_id + 236 + 21): (b'BC04', 0x2193f576),  # in ball dispenser
    (base_id + 236 + 22): (b'SM01', 0x2193f576),  # on ledge near entrance
    (base_id + 236 + 23): (b'SM02', 0x6b9489ab),  # on slide under tiki
    (base_id + 236 + 24): (b'SM02', 0x6b9489ac),  # on stone arc
    (base_id + 236 + 25): (b'SM04', 0xf68f73a6),  # in cave on drop to exit
    (base_id + 236 + 26): (b'KF01', 0x076e9319),  # near waterfall
    (base_id + 236 + 27): (b'KF02', 0x2193f576),  # bungee near waterfall
    (base_id + 236 + 28): (b'KF04', 0x2193f576),  # top of tall room
    (base_id + 236 + 29): (b'KF05', 0xf68f73a6),  # on slide after leave
    (base_id + 236 + 30): (b'GY01', 0x2193f576),  # on left wall near tubelet
    (base_id + 236 + 31): (b'GY02', 0x2193f576),  # on mast below wall jump section
    (base_id + 236 + 32): (b'GY03', 0x2193f576),  # on top of mast
    (base_id + 236 + 33): (b'DB01', 0x2193f576),  # behind KK
    (base_id + 236 + 34): (b'DB02', 0x76579669),  # on tikis near start
    (base_id + 236 + 35): (b'DB02', 0xf68f73a6),  # on flower
    (base_id + 236 + 36): (b'DB03', 0x2193f576),  # on clarinet
    (base_id + 236 + 37): (b'DB04', 0x2193f576),  # on tiki near ent
}

valid_scenes = [
    b'HB01', b'HB02', b'HB03', b'HB04', b'HB05', b'HB06', b'HB07', b'HB08', b'HB09', b'HB10',
    b'JF01', b'JF02', b'JF03', b'JF04',
    b'BB01', b'BB02', b'BB03', b'BB04',
    b'GL01', b'GL02', b'GL03',
    b'B101',
    b'RB01', b'RB02', b'RB03',
    b'BC01', b'BC02', b'BC03', b'BC04', b'BC05',
    b'SM01', b'SM02', b'SM03', b'SM04',
    b'B201',
    b'KF01', b'KF02', b'KF04', b'KF05',
    b'GY01', b'GY02', b'GY03', b'GY04',
    b'DB01', b'DB02', b'DB03', b'DB04', b'DB05', b'DB06',
    b'B302', b'B303',
]

invalid_scenes = [
    b'HB00',  # intro cutscene
    b'MNU3', b'MNU4', b'MNU5',  # menus
    b'PG12',  # post game arena
    b'SPSA', b'SPSB', b'SPSC',  # idk
]


class BfBBCommandProcessor(SuperClientCommandProcessor):
    def __init__(self, ctx: SuperContext):
        super().__init__(ctx)

    def _cmd_dolphin(self):
        """Check Dolphin Connection State"""
        if isinstance(self.ctx, BfBBContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_deathlink(self):
        """Toggle Death Link override."""
        if self.ctx.server is None or self.ctx.server.socket.closed or self.ctx.auth is None:
            logger.info("Not connected")
            return

        if isinstance(self.ctx, BfBBContext):
            if not self.ctx.death_link:
                logger.info(f"Death Link is not enabled for this Slot")
                return

            self.ctx.disable_death_link = not self.ctx.disable_death_link
            Utils.async_start(self.ctx.update_tags())
            logger.info(f"Toggled Death Link {"off" if self.ctx.disable_death_link else "on"}")

    def _cmd_ringlink(self):
        """Toggle Ring Link override."""
        if self.ctx.server is None or self.ctx.server.socket.closed or self.ctx.auth is None:
            logger.info("Not connected")
            return

        if isinstance(self.ctx, BfBBContext):
            if not self.ctx.ring_link:
                logger.info(f"Ring Link is not enabled for this Slot")
                return

            self.ctx.disable_ring_link = not self.ctx.disable_ring_link
            Utils.async_start(self.ctx.update_tags())
            logger.info(f"Toggled Ring Link {"off" if self.ctx.disable_ring_link else "on"}")

    def _cmd_ringlink_ratio(self, ratio: str = ""):
        """Overwrite or check the Shiny Object to Ring ratio (1-100). Resets after reconnect."""
        if self.ctx.server is None or self.ctx.server.socket.closed or self.ctx.auth is None:
            logger.info("Not connected")
            return
        if isinstance(self.ctx, BfBBContext):
            if not ratio:
                logger.info(f"Current Shiny Object to Ring ratio: {self.ctx.so_to_ring_ratio}")
                return

            try:
                new_ratio = int(ratio)
            except ValueError:
                logger.info("The ratio has to be an integer.")
                return

            if 100 < new_ratio or new_ratio < 1:
                logger.info("The ratio has to be between 1 and 100")
                return

            if not self.ctx.ring_link:
                logger.info(f"Ring Link is not enabled for this Slot")
                return

            self.ctx.so_to_ring_ratio = new_ratio
            logger.info(f"Set Shiny Object to Ring ratio to: {self.ctx.so_to_ring_ratio}")


class BfBBContext(SuperContext):
    command_processor = BfBBCommandProcessor
    game = 'Battle for Bikini Bottom'
    items_handling = 0b111  # full remote
    tags = {"AP"}

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.included_check_types: CheckTypes = CheckTypes.SPAT
        self.items_received_2 = []
        self.dolphin_sync_task = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.password_requested = False
        self.given_socks = 0
        self.spat_count = 0
        self.sock_count = 0
        self.LAST_STATE = [bytes([0, 0]), bytes([0, 0]), bytes([0, 0])]
        self.last_rev_index = -1
        self.has_send_death = False
        self.last_death_link_send = time.time()
        self.current_scene_key = None
        self.death_link = False
        self.disable_death_link = False
        self.ring_link = False
        self.disable_ring_link = False
        self.previous_shiny_objects = None
        self.instance_id = time.time()
        self.so_to_ring_ratio = 10

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        self.password = None
        self.tags = {'AP'}
        await super().disconnect(allow_autoreconnect)

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.disable_death_link = False
            self.disable_ring_link = False
            self.current_scene_key = f"bfbb_current_scene_T{self.team}_P{self.slot}"
            self.set_notify(self.current_scene_key)
            self.last_rev_index = -1
            self.items_received_2 = []
            self.included_check_types = CheckTypes.SPAT
            self.death_link = bool(args['slot_data'].get('death_link', 0))
            self.ring_link = bool(args['slot_data'].get('ring_link', 0))
            self.so_to_ring_ratio = args['slot_data'].get('shiny_object_to_ring_ratio', 10)
            if self.death_link or self.ring_link:
                Utils.async_start(self.update_tags())
            if 'include_socks' in args['slot_data'] and args['slot_data']['include_socks']:
                self.included_check_types |= CheckTypes.SOCK
            if 'include_skills' in args['slot_data'] and args['slot_data']['include_skills']:
                self.included_check_types |= CheckTypes.SKILLS
            if 'include_golden_underwear' in args['slot_data'] and args['slot_data']['include_golden_underwear']:
                self.included_check_types |= CheckTypes.GOLDEN_UNDERWEAR
            if 'include_level_items' in args['slot_data'] and args['slot_data']['include_level_items']:
                self.included_check_types |= CheckTypes.LEVEL_ITEMS
            if 'include_purple_so' in args['slot_data'] and args['slot_data']['include_purple_so']:
                self.included_check_types |= CheckTypes.PURPLE_SO
        if cmd == 'ReceivedItems':
            if args["index"] >= self.last_rev_index:
                self.last_rev_index = args["index"]
                for item in args['items']:
                    self.items_received_2.append((item, self.last_rev_index))
                    self.last_rev_index += 1
            self.items_received_2.sort(key=lambda v: v[1])
            self._update_item_counts(args)
        elif cmd == "Bounced":
            if "tags" in args:
                related_tags = args["tags"]
                if "RingLink" in related_tags:
                    self.on_ringlink(args["data"])
        super().on_package(cmd, args)

    async def update_tags(self):
        old_tags = self.tags.copy()
        if self.death_link and not self.disable_death_link:
            self.tags.add("DeathLink")
        else:
            self.tags -= {"DeathLink"}
        if self.ring_link and not self.disable_ring_link:
            self.tags.add("RingLink")
        else:
            self.tags -= {"RingLink"}
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}])

    def on_ringlink(self, data):
        if not self.ring_link or self.disable_ring_link:
            return
        if not "amount" in data:
            return

        amount = data["amount"] * self.so_to_ring_ratio
        # we can safely handle packets with no source because we know it's not us,
        # and we only use source to skip our own packets
        source = data.get("source", None)

        if source == self.instance_id:
            return

        _give_shiny_objects(self, amount)
        self.previous_shiny_objects = None

    def on_deathlink(self, data: Dict[str, Any]) -> None:
        if not self.death_link or self.disable_death_link:
            return
        super().on_deathlink(data)
        _give_death(self)

    def _update_item_counts(self, args: dict):
        self.spat_count = len([item for item in self.items_received if item.item == base_id + 0])
        self.sock_count = len([item for item in self.items_received if item.item == base_id + 1])

    async def server_auth(self, password_requested: bool = False):
        self.password_requested = password_requested
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info('Awaiting connection to Dolphin and loaded save file to get player information')
            return
        else:
            self.awaiting_rom = False
        if password_requested and not self.password:
            await super(BfBBContext, self).server_auth(password_requested)
        await self.send_connect()

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for The Wind Waker client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = f"{apname} Battle for Bikini Bottom Client"
        return ui


def _is_ptr_valid(ptr):
    return 0x80000000 <= ptr < 0x817fffff


def _find_obj_in_obj_table(id: int, ptr: Optional[int] = None, size: Optional[int] = None):
    if size is None:
        size = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_SIZE_ADDR)
    if ptr is None:
        ptr = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_PTR_ADDR)
        if not _is_ptr_valid(ptr): return None
    try:
        counter_list_entry = 0
        # this is our initial index "guess"
        idx = id & (size - 1)
        skip = False
        for i in range(0, size):
            # addr for entry in the list at idx
            counter_list_entry = ptr + idx * 0x8
            if not _is_ptr_valid(counter_list_entry):
                return None
            # get id from the entry
            obj_id = dolphin_memory_engine.read_word(counter_list_entry)
            # if the id matches, we are at the right entry
            if obj_id == id:
                break
            # the returns NULL if it encounters id 0, so just skip if we do
            if obj_id == 0:
                break
            # we are not at the right entry so look at the next
            idx += 1
            # rollover at end of list
            if idx == size:
                idx = 0
        if skip: return -1
        # read counter pointer from the entry
        obj_ptr = dolphin_memory_engine.read_word(counter_list_entry + 0x4)
        if not _is_ptr_valid(obj_ptr):
            return None
        return obj_ptr
    except:
        return None


def _give_spat(ctx: BfBBContext):
    cur_spat_count = dolphin_memory_engine.read_word(SPAT_COUNT_ADDR)
    dolphin_memory_engine.write_word(SPAT_COUNT_ADDR, cur_spat_count + 1)
    if cur_spat_count > ctx.spat_count:
        logger.info("!Some went wrong with the spat count!")


def _give_sock(ctx: BfBBContext):
    cur_sock_count = dolphin_memory_engine.read_word(SOCK_COUNT_ADDR)
    dolphin_memory_engine.write_word(SOCK_COUNT_ADDR, cur_sock_count + 1)
    if cur_sock_count > ctx.sock_count:
        logger.info("!Some went wrong with the sock count!")


def _give_golden_underwear(ctx: BfBBContext):
    cur_max_health = dolphin_memory_engine.read_word(MAX_HEALTH_ADDR)
    dolphin_memory_engine.write_word(MAX_HEALTH_ADDR, cur_max_health + 1)
    dolphin_memory_engine.write_word(HEALTH_ADDR, cur_max_health + 1)
    if cur_max_health > 6:
        logger.info("!Some went wrong with max health!")


def _give_powerup(ctx: BfBBContext, offset: int):
    dolphin_memory_engine.write_byte(POWERUPS_ADDR + offset, 1)


def _give_death(ctx: BfBBContext):
    if ctx.slot and dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS \
            and check_ingame(ctx) and check_control_owner(ctx, lambda owner: owner == 0):
        dolphin_memory_engine.write_word(HEALTH_ADDR, 0)


def _give_level_pickup(ctx: BfBBContext, lvl_idx: int):
    assert -1 < lvl_idx < 15, "invalid level index in _give_level_pickup"
    addr = LEVEL_PICKUP_PER_LEVEL_ADDR + 0x4 * lvl_idx
    cur_count = dolphin_memory_engine.read_word(addr)
    dolphin_memory_engine.write_word(addr, cur_count + 1)
    # ToDo: check if we need to write to CurrentLevel too


def _give_shiny_objects(ctx: BfBBContext, amount: int) -> object:
    cur_count = dolphin_memory_engine.read_word(SHINY_COUNT_ADDR)
    dolphin_memory_engine.write_word(SHINY_COUNT_ADDR, min(0x01869F, max(cur_count + amount, 0)))


def _inc_delayed_item_count(ctx: BfBBContext, addr: int, val: int = 1):
    cur_count = dolphin_memory_engine.read_byte(addr)
    dolphin_memory_engine.write_byte(addr, cur_count + val)


def _get_ptr_from_info(ctx: BfBBContext, info: Tuple[bytes, int]):
    if not _check_cur_scene(ctx, info[0]):
        return None
    obj_ptr = _find_obj_in_obj_table(info[1])
    if obj_ptr is None or obj_ptr == -1:
        return None
    return obj_ptr


def _set_counter_value(ctx: BfBBContext, cntr_info: Tuple[bytes, int], val: int):
    obj_ptr = _get_ptr_from_info(ctx, cntr_info)
    if obj_ptr is None:
        return
    count_addr = obj_ptr + 0x14
    cur_count = int.from_bytes(dolphin_memory_engine.read_bytes(count_addr, 0x2), "big")
    if cur_count != val:
        dolphin_memory_engine.write_bytes(count_addr, val.to_bytes(0x2, "big"))


def _set_pickup_active(ctx: BfBBContext, pickup_info: Tuple[bytes, int]):
    obj_ptr = _get_ptr_from_info(ctx, pickup_info)
    if obj_ptr is None:
        return
    state = dolphin_memory_engine.read_word(obj_ptr + 0x16c)
    if state & 0x8 == 0:  # not collected yet
        current_pickup_flags = int.from_bytes(dolphin_memory_engine.read_bytes(obj_ptr + 0x264, 0x2), "big")
        current_pickup_flags |= 0x2
        dolphin_memory_engine.write_bytes(obj_ptr + 0x264, current_pickup_flags.to_bytes(0x2, "big"))
        current_ent_flags = dolphin_memory_engine.read_byte(obj_ptr + 0x18)
        current_ent_flags |= 0x1
        dolphin_memory_engine.write_byte(obj_ptr + 0x18, current_ent_flags)


def _set_plat_active(ctx: BfBBContext, plat_info: Tuple[bytes, int]):
    obj_ptr = _get_ptr_from_info(ctx, plat_info)
    if obj_ptr is None:
        return
    state = dolphin_memory_engine.read_byte(obj_ptr + 0x18)
    if state & 0x1 == 0:
        dolphin_memory_engine.write_byte(obj_ptr + 0x18, state | 0x1)  # visible
    coll_mask = dolphin_memory_engine.read_byte(obj_ptr + 0x22)
    if coll_mask != 0x18:
        dolphin_memory_engine.write_byte(obj_ptr + 0x22, 0x18)  # collision on


def _set_plat_inactive(ctx: BfBBContext, plat_info: Tuple[bytes, int]):
    obj_ptr = _get_ptr_from_info(ctx, plat_info)
    if obj_ptr is None:
        return
    state = dolphin_memory_engine.read_byte(obj_ptr + 0x18)
    if state & 0x1 == 0x1:
        dolphin_memory_engine.write_byte(obj_ptr + 0x18, state & ~0x1)  # invisible
    coll_mask = dolphin_memory_engine.read_byte(obj_ptr + 0x22)
    if coll_mask == 0x18:
        dolphin_memory_engine.write_byte(obj_ptr + 0x22, 0)  # collision off


def _set_taskbox_success(ctx: BfBBContext, task_info: Tuple[bytes, int]):
    obj_ptr = _get_ptr_from_info(ctx, task_info)
    if obj_ptr is None:
        return
    state_addr = obj_ptr + 0x18
    state = dolphin_memory_engine.read_word(state_addr)
    enabled_ptr = obj_ptr + 0x10
    enabled = dolphin_memory_engine.read_byte(enabled_ptr)
    if 0 < state < 3 and enabled == 1:
        dolphin_memory_engine.write_word(state_addr, 3)
        # _set_trig_active(ctx, BALLOON_KID_SUC_TRIG_ID)


def _set_trig_active(ctx: BfBBContext, trig_info: Tuple[bytes, int]):
    obj_ptr = _get_ptr_from_info(ctx, trig_info)
    if obj_ptr is None:
        return
    addr = obj_ptr + 0x7
    val = dolphin_memory_engine.read_byte(addr)
    if val & 1 != 1:
        dolphin_memory_engine.write_byte(addr, val & 1)


def _check_cur_scene(ctx: BfBBContext, scene_id: bytes, scene_ptr: Optional[int] = None):
    if scene_ptr is None:
        scene_ptr = dolphin_memory_engine.read_word(CUR_SCENE_PTR_ADDR)
        if not _is_ptr_valid(scene_ptr): return False
    cur_scene = dolphin_memory_engine.read_bytes(scene_ptr, 0x4)
    return cur_scene == scene_id


def _print_player_info(ctx: BfBBContext):
    base_flags = dolphin_memory_engine.read_bytes(PLAYER_ADDR + 6, 0x2)
    if base_flags != ctx.LAST_STATE[0]:
        str_1 = format(int(ctx.LAST_STATE[0].hex(), 16), '#018b')
        str_1 = f"{str_1[2:10]} {str_1[10:]}"
        str_2 = format(int(base_flags.hex(), 16), '#018b')
        str_2 = f"{str_2[2:10]} {str_2[10:]}"
        print(f"player base flags:\t{str_1}-> {str_2}")
        ctx.LAST_STATE[0] = base_flags
    ent_flags = dolphin_memory_engine.read_bytes(PLAYER_ADDR + 0x18, 0x2)
    if ent_flags != ctx.LAST_STATE[1]:
        str_1 = format(int(ctx.LAST_STATE[1].hex(), 16), '#018b')
        str_1 = f"{str_1[2:10]} {str_1[10:]}"
        str_2 = format(int(ent_flags.hex(), 16), '#018b')
        str_2 = f"{str_2[2:10]} {str_2[10:]}"
        print(f"ent_flags:\t\t\t{str_1}-> {str_2}")
        ctx.LAST_STATE[1] = ent_flags
    pflags = dolphin_memory_engine.read_bytes(PLAYER_ADDR + 0x1b, 0x2)
    if pflags != ctx.LAST_STATE[2]:
        str_1 = format(int(ctx.LAST_STATE[2].hex(), 16), '#018b')
        str_1 = f"{str_1[2:10]} {str_1[10:]}"
        str_2 = format(int(pflags.hex(), 16), '#018b')
        str_2 = f"{str_2[2:10]} {str_2[10:]}"
        print(f"pflags:\t\t\t\t{str_1}-> {str_2}")
        ctx.LAST_STATE[2] = pflags


def _give_item(ctx: BfBBContext, item_id: int):
    temp = item_id - base_id
    if temp == 0:
        _give_spat(ctx)
    elif temp == 1:
        _give_sock(ctx)
    elif temp == 2:
        _give_shiny_objects(ctx, 100)
    elif temp == 3:
        _give_shiny_objects(ctx, 250)
    elif temp == 4:
        _give_shiny_objects(ctx, 500)
    elif temp == 5:
        _give_shiny_objects(ctx, 750)
    elif temp == 6:
        _give_shiny_objects(ctx, 1000)
    elif temp == 7:
        _give_powerup(ctx, 0)
    elif temp == 8:
        _give_powerup(ctx, 1)
    elif temp == 9:
        _give_golden_underwear(ctx)
    elif temp == 10:
        _give_level_pickup(ctx, 1)
    elif temp == 11:
        _give_level_pickup(ctx, 2)
    elif temp == 12:
        _give_level_pickup(ctx, 3)
        _inc_delayed_item_count(ctx, BALLOON_KID_COUNT_ADDR)
    elif temp == 13:
        _give_level_pickup(ctx, 5)
    elif temp == 14:
        _give_level_pickup(ctx, 6)
    elif temp == 15:
        _inc_delayed_item_count(ctx, SANDMAN_COUNT_ADDR)
    elif temp == 16:
        _give_level_pickup(ctx, 9)
    elif temp == 17:
        _inc_delayed_item_count(ctx, POWER_CRYSTAL_COUNT_ADDR)
    elif temp == 18:
        _give_level_pickup(ctx, 10)
        _inc_delayed_item_count(ctx, CANNON_BUTTON_COUNT_ADDR)
    else:
        logger.warning(f"Received unknown item with id {item_id}")


async def update_delayed_items(ctx: BfBBContext):
    if not await check_alive(ctx):
        return
    if CheckTypes.LEVEL_ITEMS in ctx.included_check_types:
        balloon_count = dolphin_memory_engine.read_byte(BALLOON_KID_COUNT_ADDR)
        _set_counter_value(ctx, BALLOON_KID_COUNTER_ID, max(5 - balloon_count, 0))
        if balloon_count >= 5:
            _set_taskbox_success(ctx, BALLOON_KID_TASKBOX_ID)
        sandman_count = dolphin_memory_engine.read_byte(SANDMAN_COUNT_ADDR)
        _set_counter_value(ctx, SANDMAN_CNTR_ID, max(8 - sandman_count, 0))
        if sandman_count >= 8:
            _set_pickup_active(ctx, SANDMAN_SOCK_ID)
        power_crystal_count = dolphin_memory_engine.read_byte(POWER_CRYSTAL_COUNT_ADDR)
        _set_counter_value(ctx, POWERCRYSTAL_COUNTER_ID, power_crystal_count)
        if power_crystal_count >= 6:
            for v in POWERCRYSTAL_TASKBOX_IDS:
                _set_taskbox_success(ctx, v)
        cannon_button_count = dolphin_memory_engine.read_byte(CANNON_BUTTON_COUNT_ADDR)
        if cannon_button_count >= 4:
            _set_pickup_active(ctx, CANNON_BUTTON_SPAT_ID)
            _set_plat_active(ctx, CANNON_BUTTON_PLAT_IDS[0])
            _set_plat_inactive(ctx, CANNON_BUTTON_PLAT_IDS[1])
            # _set_plat_inactive(ctx, CANNON_BUTTON_PLAT_IDS[2])


async def give_items(ctx: BfBBContext):
    await update_delayed_items(ctx)
    expected_idx = dolphin_memory_engine.read_word(EXPECTED_INDEX_ADDR)
    # we need to loop some items
    for item, idx in ctx.items_received_2:
        if check_control_owner(ctx, lambda owner: owner & 0x2 or owner & 0x8000 or owner & 0x200 or owner & 0x1):
            return
        if expected_idx <= idx:
            item_id = item.item
            _give_item(ctx, item_id)
            dolphin_memory_engine.write_word(EXPECTED_INDEX_ADDR, idx + 1)
            await asyncio.sleep(.01)  # wait a bit for values to update


# ToDo: do we actually want this?
# ToDo: implement socks/golden underwear/lvl_pickups/skills/ etc..
# async def set_locations(ctx: BfBBContext):
#     scene_ptr = dolphin_memory_engine.read_word(CUR_SCENE_PTR_ADDR)
#     if not _is_ptr_valid(scene_ptr):
#         return
#     scene = dolphin_memory_engine.read_bytes(scene_ptr, 0x4)
#     ptr = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_PTR_ADDR)
#     if not _is_ptr_valid(ptr):
#         return
#     size = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_SIZE_ADDR)
#     for v in ctx.checked_locations:
#         if v not in SPAT_PICKUP_IDS.keys():
#             continue
#         val = SPAT_PICKUP_IDS[v]
#         if val[0] != scene:
#             continue
#         obj_ptr = _find_obj_in_obj_table(val[1], ptr, size)
#         if obj_ptr is None: break
#         if obj_ptr == -1: continue
#         if not _is_ptr_valid(obj_ptr + 0x16C):
#             return
#         obj_state = dolphin_memory_engine.read_word(obj_ptr + 0x16C)
#         print(obj_state)
#         if obj_state is not None and obj_state & 0x4 == 0:
#             dolphin_memory_engine.write_word(obj_ptr + 0x16c, obj_state & ~0x3f | 0x4)


def _check_pickup_state(ctx: BfBBContext, obj_ptr: int):
    if not _is_ptr_valid(obj_ptr + 0x16C):
        return False
    obj_state = dolphin_memory_engine.read_word(obj_ptr + 0x16c)
    return obj_state & 0x08 > 0 and obj_state & 0x37 == 0


def _check_button_state(ctx: BfBBContext, obj_ptr: int):
    if not _is_ptr_valid(obj_ptr + 0x144):
        return False
    btn_state = dolphin_memory_engine.read_word(obj_ptr + 0x144)
    return btn_state & 0x1 == 0x1


def _check_destructible_state(ctx: BfBBContext, obj_ptr: int):
    if not _is_ptr_valid(obj_ptr + 0xdc):
        return False
    health = dolphin_memory_engine.read_word(obj_ptr + 0xdc)
    return health == 0


def format_to_bitmask(val: bytes) -> str:
    result = ''
    for b in val:
        result += format(b, '#010b') + ' '
    return result


def get_player_type(ctx: BfBBContext):
    player_settings_ptr = dolphin_memory_engine.read_word(PLAYER_SETTINGS_PRT_ADDR)
    if not _is_ptr_valid(player_settings_ptr):
        return None
    player_type = dolphin_memory_engine.read_word(player_settings_ptr)
    return player_type

def get_character_name(ctx: BfBBContext):
    player_type = get_player_type(ctx)
    if player_type == 0:
        return "Spongebob"
    elif player_type == 1:
        return "Patrick"
    elif player_type == 2:
        return "Sandy"
    else:
        return None

def _check_platform_state(ctx: BfBBContext, obj_ptr: int):
    if not _is_ptr_valid(obj_ptr + 0x18):
        return False
    state = dolphin_memory_engine.read_byte(obj_ptr + 0x18)
    return state != 1


def _check_counter(ctx: BfBBContext, obj_ptr: int, target_cb: Callable):
    if not _is_ptr_valid(obj_ptr + 0x14):
        return False
    counter = int.from_bytes(dolphin_memory_engine.read_bytes(obj_ptr + 0x14, 0x2), "big")
    return target_cb(counter)


def _check_base_inactive(ctx: BfBBContext, obj_ptr: int):
    if not _is_ptr_valid(obj_ptr + 0x6):
        return False
    state = dolphin_memory_engine.read_bytes(obj_ptr + 0x6, 0x2)
    return state[1] & 0x1 == 0


def _check_base_active(ctx: BfBBContext, obj_ptr: int):
    return not _check_base_inactive(ctx, obj_ptr)


async def _check_objects_by_id(ctx: BfBBContext, locations_checked: set, id_table: dict, check_cb: Callable):
    scene_ptr = dolphin_memory_engine.read_word(CUR_SCENE_PTR_ADDR)
    if not _is_ptr_valid(scene_ptr):
        return
    scene = dolphin_memory_engine.read_bytes(scene_ptr, 0x4)
    ptr = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_PTR_ADDR)
    if not _is_ptr_valid(ptr):
        return
    size = dolphin_memory_engine.read_word(SCENE_OBJ_LIST_SIZE_ADDR)
    for k, v in id_table.items():
        if k in locations_checked and (k != base_id + 83 or ctx.finished_game):  # we need to check base_id + 83 for goal
            continue
        if v[0] is not None and v[0] != scene:
            continue
        for i in range(1, len(v)):
            obj_ptr = _find_obj_in_obj_table(v[i], ptr, size)
            if obj_ptr is None: break
            if obj_ptr == -1: continue
            if check_cb(ctx, obj_ptr):
                locations_checked.add(k)
                if k == base_id + 83 and not ctx.finished_game:
                    print("send done")
                    await ctx.send_msgs([
                        {"cmd": "StatusUpdate",
                         "status": 30}
                    ])
                    ctx.finished_game = True
                break


async def _check_spats(ctx: BfBBContext, locations_checked: set):
    await _check_objects_by_id(ctx, locations_checked, SPAT_COUNTER_IDS,
                               lambda ctx, ptr: _check_counter(ctx, ptr, lambda cnt: cnt == 2))
    await _check_objects_by_id(ctx, locations_checked, SPAT_PICKUP_IDS, _check_pickup_state)


async def _check_socks(ctx: BfBBContext, locations_checked: set):
    await _check_objects_by_id(ctx, locations_checked, SOCK_PICKUP_IDS, _check_pickup_state)


async def _check_golden_underwear(ctx: BfBBContext, locations_checked: set):
    await _check_objects_by_id(ctx, locations_checked, GOLDEN_UNDERWEAR_IDS, _check_pickup_state)


async def _check_level_pickups(ctx: BfBBContext, locations_checked: set):
    await _check_objects_by_id(ctx, locations_checked, KING_JF_DISP_ID, _check_base_active)
    await _check_objects_by_id(ctx, locations_checked, STEERING_WHEEL_PICKUP_IDS, _check_pickup_state)
    await _check_objects_by_id(ctx, locations_checked, BALLOON_KID_PLAT_IDS, _check_platform_state)
    await _check_objects_by_id(ctx, locations_checked, ART_WORK_IDS, _check_pickup_state)
    await _check_objects_by_id(ctx, locations_checked, OVERRIDE_BUTTON_IDS, _check_button_state)
    await _check_objects_by_id(ctx, locations_checked, SANDMAN_DSTR_IDS, _check_destructible_state)
    await _check_objects_by_id(ctx, locations_checked, LOST_CAMPER_TRIG_IDS, _check_base_inactive)
    await _check_objects_by_id(ctx, locations_checked, POWERCRYSTAL_PICKUP_IDS, _check_pickup_state)
    await _check_objects_by_id(ctx, locations_checked, CANNON_BUTTON_IDS, _check_button_state)


async def _check_purple_so(ctx: BfBBContext, locations_checked: set):
    await _check_objects_by_id(ctx, locations_checked, PURPLE_SO_IDS, _check_pickup_state)


def _check_skills(ctx: BfBBContext, locations_checked: set):
    # just check if we checked the boss spats locations
    if (base_id + 32) in locations_checked and (base_id + 234) not in locations_checked:
        locations_checked.add(base_id + 234)
    if (base_id + 57) in locations_checked and (base_id + 235) not in locations_checked:
        locations_checked.add(base_id + 235)


async def check_locations(ctx: BfBBContext):
    await _check_spats(ctx, ctx.locations_checked)
    if CheckTypes.SOCK in ctx.included_check_types:
        await _check_socks(ctx, ctx.locations_checked)
    if CheckTypes.SKILLS in ctx.included_check_types:
        _check_skills(ctx, ctx.locations_checked)
    if CheckTypes.GOLDEN_UNDERWEAR in ctx.included_check_types:
        await _check_golden_underwear(ctx, ctx.locations_checked)
    if CheckTypes.LEVEL_ITEMS in ctx.included_check_types:
        await _check_level_pickups(ctx, ctx.locations_checked)
    if CheckTypes.PURPLE_SO in ctx.included_check_types:
        await _check_purple_so(ctx, ctx.locations_checked)
    # ignore already in server state
    send_locations = await ctx.check_locations(ctx.locations_checked)
    # print([ctx.location_names[location] for location in send_locations])


async def check_alive(ctx: BfBBContext):
    cur_health = dolphin_memory_engine.read_word(HEALTH_ADDR)
    return not (cur_health <= 0 or check_control_owner(ctx, lambda owner: owner & 0x4))

async def check_death(ctx: BfBBContext):
    cur_health = dolphin_memory_engine.read_word(HEALTH_ADDR)
    grabbed_by_hans = check_control_owner(ctx, lambda owner: owner & 0x4)
    if cur_health <= 0 or grabbed_by_hans:
        if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
            ctx.has_send_death = True
            if grabbed_by_hans:
                death_text = f"{ctx.player_names[ctx.slot]} was saved by Hans"
            else:
                death_text = f"{ctx.player_names[ctx.slot]} has died"
                character_name = get_character_name(ctx)
                if character_name:
                    death_text = f"{death_text} as {character_name}"
            await ctx.send_death(death_text)
    else:
        ctx.has_send_death = False


def check_ingame(ctx: BfBBContext, ignore_control_owner: bool = False) -> bool:
    scene_ptr = dolphin_memory_engine.read_word(CUR_SCENE_PTR_ADDR)
    if not _is_ptr_valid(scene_ptr):
        return False
    scene = dolphin_memory_engine.read_bytes(scene_ptr, 0x4)
    if scene not in valid_scenes:
        return False
    update_current_scene(ctx, scene.decode('ascii'))
    return True


def update_current_scene(ctx: BfBBContext, scene: str):
    if not ctx.slot and not ctx.auth:
        return
    if ctx.current_scene_key is None or ctx.current_scene_key not in ctx.stored_data:
        return
    if ctx.stored_data[ctx.current_scene_key] == scene:
        return
    Utils.async_start(ctx.send_msgs([{
        "cmd": "Set",
        "key": ctx.current_scene_key,
        "default": None,
        "want_reply": True,
        "operations": [{
            "operation": "replace",
            "value": scene,
        }],
    }]))


def check_control_owner(ctx: BfBBContext, check_cb: Callable[[int], bool]) -> bool:
    owner = dolphin_memory_engine.read_word(PLAYER_CONTROL_OWNER)
    return check_cb(owner)


def validate_save(ctx: BfBBContext) -> bool:
    saved_slot_bytes = dolphin_memory_engine.read_bytes(SAVED_SLOT_NAME_ADDR, 0x40).strip(b'\0')
    slot_bytes = dolphin_memory_engine.read_bytes(SLOT_NAME_ADDR, 0x40).strip(b'\0')
    saved_seed_bytes = dolphin_memory_engine.read_bytes(SAVED_SEED_ADDR, 0x10).strip(b'\0')
    seed_bytes = dolphin_memory_engine.read_bytes(SEED_ADDR, 0x10).strip(b'\0')
    if len(slot_bytes) > 0 and len(seed_bytes) > 0:
        if len(saved_slot_bytes) == 0 and len(saved_seed_bytes) == 0:
            # write info to save
            dolphin_memory_engine.write_bytes(SAVED_SLOT_NAME_ADDR, slot_bytes)
            dolphin_memory_engine.write_bytes(SAVED_SEED_ADDR, seed_bytes)
            logger.debug("saved slot/seed info")
            return True
        elif slot_bytes == saved_slot_bytes and seed_bytes == saved_seed_bytes:
            return True
        else:
            if slot_bytes != saved_slot_bytes:
                logger.warn(f"Saved slot info do not match: {slot_bytes} != {saved_slot_bytes}")
            if seed_bytes != saved_seed_bytes:
                logger.warn(f"Saved seed info do not match: {seed_bytes} != {saved_seed_bytes}")
            return False
    else:
        logger.warn("ROM doesn't contain any slot/seed info. Please make sure your apworld version match between client and patch file and then re-patch.")
    return False


async def handle_ring_link(ctx: BfBBContext):
    if (not check_ingame(ctx) or
        not check_control_owner(ctx, lambda owner: owner == 0) or
        not await check_alive(ctx)):
        # we are not in a state where we can check SO count and get a reasonable value
        return


    current_shiny_objects = dolphin_memory_engine.read_word(SHINY_COUNT_ADDR)
    previous = ctx.previous_shiny_objects

    if ctx.previous_shiny_objects is None:
        # no previous value, so we can set it to current and get out since the difference will be 0
        ctx.previous_shiny_objects = current_shiny_objects
        return

    # using int cast to always round towards 0
    difference = int((current_shiny_objects - previous)/ctx.so_to_ring_ratio)

    if difference != 0:
        ctx.previous_shiny_objects = current_shiny_objects
        msg = {
            "cmd": "Bounce",
            "slots": [ctx.slot],
            "data": {
                "time": time.time(),
                "source": ctx.instance_id,
                "amount": difference
            },
            "tags": {"RingLink"}
        }
        await ctx.send_msgs([msg])


async def dolphin_sync_task(ctx: BfBBContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information")
    while not ctx.exit_event.is_set():
        try:
            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if not check_ingame(ctx):
                    # reset AP values when on main menu
                    # ToDo: this should be done via patch when other globals are reset
                    if _check_cur_scene(ctx, b'MNU3'):
                        for i in range(0, 0x80, 0x4):
                            cur_val = dolphin_memory_engine.read_word(EXPECTED_INDEX_ADDR + i)
                            if cur_val != 0:
                                dolphin_memory_engine.write_word(EXPECTED_INDEX_ADDR + i, 0)
                    await asyncio.sleep(.1)
                    continue
                # _print_player_info(ctx)
                if ctx.slot:
                    if not validate_save(ctx):
                        logger.info(CONNECTION_REFUSED_SAVE_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_SAVE_STATUS
                        dolphin_memory_engine.un_hook()
                        await ctx.disconnect()
                        await asyncio.sleep(5)
                        continue
                    ctx.current_scene_key = f"bfbb_current_scene_T{ctx.team}_P{ctx.slot}"
                    ctx.set_notify(ctx.current_scene_key)
                    if ctx.death_link and not ctx.disable_death_link:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                    if ctx.ring_link and not ctx.disable_ring_link:
                        await handle_ring_link(ctx)
                    # await set_locations(ctx)
                else:
                    if not ctx.auth:
                        ctx.auth = dolphin_memory_engine.read_bytes(SLOT_NAME_ADDR, 0x40).decode('utf-8').strip(
                            '\0')
                        if ctx.auth == '\x02\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00' \
                                       '\x00\x02\x00\x00\x00\x04\x00\x00\x00\x04':
                            logger.info(CONNECTION_REFUSED_VANILLA_GAME_STATUS)
                            ctx.dolphin_status = CONNECTION_REFUSED_VANILLA_GAME_STATUS
                            ctx.awaiting_rom = False
                            dolphin_memory_engine.un_hook()
                            await ctx.disconnect()
                            await asyncio.sleep(5)
                    if ctx.awaiting_rom:
                        await ctx.server_auth(ctx.password_requested)
                await asyncio.sleep(.5)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    cur_game_id = dolphin_memory_engine.read_bytes(0x80000000, 6)
                    if dolphin_memory_engine.read_bytes(0x80000000, 6) == GAME_ID:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                    else:
                        logger.debug(f"got GAME_ID {cur_game_id} instead of {GAME_ID}")
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin_memory_engine.un_hook()
                        await asyncio.sleep(1)
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


async def patch_and_run_game(ctx: BfBBContext, patch_file):
    try:
        rom_path = BfBBContainer.get_rom_path()
        def _run_full_patch_process() -> str:
            result_path = os.path.splitext(patch_file)[0] + BfBBContainer.result_file_ending
            logger.info("Applying patch file, please wait...")

            with zipfile.ZipFile(patch_file, 'r') as patch_archive:
                if not BfBBContainer.check_version(patch_archive):
                    raise Exception("apbfbb version doesn't match this client. "
                                    "Make sure your generator and client are the same.")

            # BfBBContainer.check_hash()
            shutil.copy(rom_path, result_path)
            BfBBContainer.apply_hiphop_changes(
                zipfile.ZipFile(patch_file, 'r'), rom_path, result_path
            )
            BfBBContainer.apply_binary_changes(
                zipfile.ZipFile(patch_file, 'r'), result_path
            )
            return result_path

        loop = asyncio.get_running_loop()
        final_path = await loop.run_in_executor(None, _run_full_patch_process)

        logger.info(f'Successfully patched the game at {final_path}')
        auto_start = get_settings().bfbb_options.rom_start
        if auto_start:
            run_game(final_path)

    except Exception as msg:
        logger.info(msg, extra={'compact_gui': True})
        logger.debug(traceback.format_exc())
        ctx.gui_error('Error', msg)


def run_game(gcm_file):
    dolphin_path = get_settings().bfbb_options.dolphin_path
    subprocess.Popen(
        [
            dolphin_path,
            gcm_file,
        ],
        cwd=Utils.local_path("."),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

async def main(args):
    ctx = BfBBContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if tracker_loaded:
        ctx.run_generator()
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    ctx.patch_task = None
    if args.patch_file:
        ext = os.path.splitext(args.patch_file)[1]
        if ext == BfBBContainer.patch_file_ending:
            logger.info("apbfbb file supplied, beginning patching process...")
            ctx.patch_task = asyncio.create_task(patch_and_run_game(ctx, args.patch_file), name="PatchGame")
        elif ext == BfBBContainer.result_file_ending:
            run_game(args.patch_file)
        else:
            logger.warning(f"Unknown patch file extension {ext}")

    async def waitForPatchThenStartSync(ctx: BfBBContext):
        try:
            if ctx.patch_task:
                await ctx.patch_task
        except asyncio.CancelledError:
            return

        if not ctx.exit_event.is_set():
            ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")
    asyncio.create_task(waitForPatchThenStartSync(ctx))

    await ctx.exit_event.wait()
    ctx.server_address = None

    tasks_to_await = []
    if ctx.patch_task:
        ctx.patch_task.cancel()
        tasks_to_await.append(ctx.patch_task)
    if ctx.dolphin_sync_task:
        ctx.dolphin_sync_task.cancel()
        tasks_to_await.append(ctx.dolphin_sync_task)

    if tasks_to_await:
        await asyncio.gather(*tasks_to_await, return_exceptions=True)

    await ctx.shutdown()

def launch(*args):
    parser = get_base_parser("BfBB Client")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument('patch_or_url', default=[], nargs="*",
                        help='Path to an .apbfbb patch file and/or url.')
    args = parser.parse_args(args)
    if not hasattr(args, 'url'):
        args.url = None
    if not hasattr(args, 'patch_file'):
        args.patch_file = ""

    for v in args.patch_or_url:
        if (v.startswith("archipelago://") or v.startswith("mwgg://")) and not args.url:
            args.url = v
            args = handle_url_arg(args, parser=parser)
        elif v.endswith(BfBBContainer.patch_file_ending) and not args.patch_file:
            args.patch_file = v

    if not args.patch_file:
        file_types = (('BfBB Patch File', ('.apbfbb',)), ('NGC iso', ('.gcm',)),)
        args.patch_file = Utils.open_filename("Select .apbfbb", file_types) or ""
        if not args.patch_file:
            return

    Utils.init_logging("BfBBClient")

    # logger.warning(f"starting args {args}")

    import colorama

    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == '__main__':
    launch(*sys.argv[1:])
