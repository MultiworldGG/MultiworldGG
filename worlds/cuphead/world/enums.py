### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from enum import IntEnum, IntFlag


class GameMode(IntEnum):
    BEAT_DEVIL = 1
    COLLECT_CONTRACTS = 2
    BUY_OUT_SHOP = 4
    DLC_BEAT_SALTBAKER = 8
    DLC_BEAT_BOTH = 9
    DLC_COLLECT_INGREDIENTS = 16
    DLC_COLLECT_BOTH = 18
    DLC_NO_ISLE4 = 32
    DLC_ISLE4_ONLY = 64
    DLC_BEAT_DEVIL_NO_ISLE4 = 33
    DLC_COLLECT_CONTRACTS_NO_ISLE4 = 34
    DLC_BUY_OUT_SHOP_NO_ISLE4 = 36
    DLC_COLLECT_INGREDIENTS_NO_ISLE4 = 48
    DLC_BEAT_SALTBAKER_ISLE4_ONLY = 72
    DLC_COLLECT_INGREDIENTS_ISLE4_ONLY = 80

class LogicMode(IntEnum):
    NORMAL = 0
    HARD = 1

class WeaponMode(IntEnum):
    NORMAL = 0
    EXCEPT_START = 4 # Not functional on its own.
    PROGRESSIVE = 1
    PROGRESSIVE_EXCEPT_START = 5
    EX_SEPARATE = 2
    EX_SEPARATE_EXCEPT_START = 6

class BossPhaseCheckMode(IntEnum):
    DISABLED = 0
    ENABLED = 1
    SECRET_SEPERATE = 2

class ShopMode(IntEnum):
    TIERS = 0
    STRICT_TIERS = 1
    INDEPENDENT = 2

class LevelShuffleMode(IntEnum):
    DISABLED = 0
    ENABLED = 1
    PLANE_SEPARATE = 2

class GradeCheckMode(IntEnum):
    DISABLED = 0
    A_MINUS_GRADE = 1
    A_GRADE = 2
    A_PLUS_GRADE = 3
    S_GRADE = 4
    PACIFIST = 5

class ChaliceMode(IntEnum):
    DISABLED = 0
    START = 1
    VANILLA = 2
    RANDOMIZED = 3
    CHALICE_ONLY = 4

class ChaliceCheckMode(IntEnum):
    DISABLED = 0
    ENABLED = 1
    SEPARATE = 2
    GRADE_REQUIRED = 4
    SEPARATE_GRADE_REQUIRED = 6

# TODO: Switch to Flag format
class ChessCastleMode(IntEnum):
    EXCLUDE = 0
    EXCLUDE_GAUNTLET = 1
    GAUNTLET_ONLY = 2
    INCLUDE_ALL = 3

class CurseMode(IntEnum):
    OFF = 0
    VANILLA = 1
    REVERSE = 2
    ALWAYS_ON = 3
    ALWAYS_ON_R = 4
    ALWAYS_ON_1 = 5
    ALWAYS_ON_2 = 6
    ALWAYS_ON_3 = 7
    ALWAYS_ON_4 = 8

class ItemGroups(IntFlag):
    NONE = 0
    ESSENTIAL = 1
    SUPER = 2
    CORE_ITEMS = 3
    WEAPON_BASIC = 4
    WEAPON_EX = 8
    WEAPONS = 12
    ABILITIES = 32
    AIM_ABILITIES = 64
    ALL = 255
