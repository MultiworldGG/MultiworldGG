"""This module provides string constants for Nanotech Level location names.

Nanotech Level locations are checked by reading the player's max health
(PlayerInventory.max_health, a float — see core/player.py and
MAX_HEALTH_ADDR_BY_PLANET_ID in core/address_maps/ps2.py) directly as the
level number itself — e.g. a max_health reading of 6.0 means Nanotech Level
6 — rather than by tracking cumulative health EXP against thresholds.
PLAYER_HEALTH_EXP (core/player_health_exp.py) still exists and is still
boosted by the Nanotech Experience Multiplier option — it's just not what
location detection reads from. See PlayerHealthExpInventory.check_level().

The player starts at Nanotech Level 5 by default, so levels 1-5 are never
locations — only levels 6-75 are.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5NanotechLevels:
    """String constants for each Nanotech Level location name (levels 6-75;
    the player starts at Nanotech Level 5 by default, so levels 1-5 are
    never locations)."""

    LEVEL_6 = "Nanotech Level: 6"
    LEVEL_7 = "Nanotech Level: 7"
    LEVEL_8 = "Nanotech Level: 8"
    LEVEL_9 = "Nanotech Level: 9"
    LEVEL_10 = "Nanotech Level: 10"
    LEVEL_11 = "Nanotech Level: 11"
    LEVEL_12 = "Nanotech Level: 12"
    LEVEL_13 = "Nanotech Level: 13"
    LEVEL_14 = "Nanotech Level: 14"
    LEVEL_15 = "Nanotech Level: 15"
    LEVEL_16 = "Nanotech Level: 16"
    LEVEL_17 = "Nanotech Level: 17"
    LEVEL_18 = "Nanotech Level: 18"
    LEVEL_19 = "Nanotech Level: 19"
    LEVEL_20 = "Nanotech Level: 20"
    LEVEL_21 = "Nanotech Level: 21"
    LEVEL_22 = "Nanotech Level: 22"
    LEVEL_23 = "Nanotech Level: 23"
    LEVEL_24 = "Nanotech Level: 24"
    LEVEL_25 = "Nanotech Level: 25"
    LEVEL_26 = "Nanotech Level: 26"
    LEVEL_27 = "Nanotech Level: 27"
    LEVEL_28 = "Nanotech Level: 28"
    LEVEL_29 = "Nanotech Level: 29"
    LEVEL_30 = "Nanotech Level: 30"
    LEVEL_31 = "Nanotech Level: 31"
    LEVEL_32 = "Nanotech Level: 32"
    LEVEL_33 = "Nanotech Level: 33"
    LEVEL_34 = "Nanotech Level: 34"
    LEVEL_35 = "Nanotech Level: 35"
    LEVEL_36 = "Nanotech Level: 36"
    LEVEL_37 = "Nanotech Level: 37"
    LEVEL_38 = "Nanotech Level: 38"
    LEVEL_39 = "Nanotech Level: 39"
    LEVEL_40 = "Nanotech Level: 40"
    LEVEL_41 = "Nanotech Level: 41"
    LEVEL_42 = "Nanotech Level: 42"
    LEVEL_43 = "Nanotech Level: 43"
    LEVEL_44 = "Nanotech Level: 44"
    LEVEL_45 = "Nanotech Level: 45"
    LEVEL_46 = "Nanotech Level: 46"
    LEVEL_47 = "Nanotech Level: 47"
    LEVEL_48 = "Nanotech Level: 48"
    LEVEL_49 = "Nanotech Level: 49"
    LEVEL_50 = "Nanotech Level: 50"
    LEVEL_51 = "Nanotech Level: 51"
    LEVEL_52 = "Nanotech Level: 52"
    LEVEL_53 = "Nanotech Level: 53"
    LEVEL_54 = "Nanotech Level: 54"
    LEVEL_55 = "Nanotech Level: 55"
    LEVEL_56 = "Nanotech Level: 56"
    LEVEL_57 = "Nanotech Level: 57"
    LEVEL_58 = "Nanotech Level: 58"
    LEVEL_59 = "Nanotech Level: 59"
    LEVEL_60 = "Nanotech Level: 60"
    LEVEL_61 = "Nanotech Level: 61"
    LEVEL_62 = "Nanotech Level: 62"
    LEVEL_63 = "Nanotech Level: 63"
    LEVEL_64 = "Nanotech Level: 64"
    LEVEL_65 = "Nanotech Level: 65"
    LEVEL_66 = "Nanotech Level: 66"
    LEVEL_67 = "Nanotech Level: 67"
    LEVEL_68 = "Nanotech Level: 68"
    LEVEL_69 = "Nanotech Level: 69"
    LEVEL_70 = "Nanotech Level: 70"
    LEVEL_71 = "Nanotech Level: 71"
    LEVEL_72 = "Nanotech Level: 72"
    LEVEL_73 = "Nanotech Level: 73"
    LEVEL_74 = "Nanotech Level: 74"
    LEVEL_75 = "Nanotech Level: 75"
