# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_enums/enum_options.py

from enum import IntEnum, unique


@unique
class BowserCastleMode(IntEnum):
    VANILLA = 0
    SHORTEN = 1
    BOSSRUSH = 2


@unique
class HiddenBlockMode(IntEnum):
    VANILLA = 0
    WATT_OUT = 1
    WATT_ACQUIRED = 2
    ALWAYS_VISIBLE = 3


@unique
class StartingBoots(IntEnum):
    JUMPLESS = -1
    BOOTS = 0
    SUPERBOOTS = 1
    ULTRABOOTS = 2


@unique
class StartingHammer(IntEnum):
    HAMMERLESS = -1
    HAMMER = 0
    SUPERHAMMER = 1
    ULTRAHAMMER = 2


@unique
class IncludeFavorsMode(IntEnum):
    NOT_RANDOMIZED = 0
    RND_REWARD_VANILLA_KEYITEMS = 1
    FULL_SHUFFLE = 2


@unique
class IncludeLettersMode(IntEnum):
    NOT_RANDOMIZED = 0
    SIMPLE_LETTERS = 1
    RANDOM_CHAIN_REWARD = 2
    FULL_SHUFFLE = 3


@unique
class RandomizeConsumablesMode(IntEnum):
    OFF = 0
    FULL_RANDOM = 1
    BALANCED_RANDOM = 2
    MYSTERY_ONLY = 3


@unique
class ItemTrapMode(IntEnum):
    OFF = 0
    SPARSE = 1
    MODERATE = 2
    PLENTY = 3


@unique
class GearShuffleMode(IntEnum):
    VANILLA = 0
    GEAR_LOCATION_SHUFFLE = 1
    FULL_SHUFFLE = 2


@unique
class RandomMoveCosts(IntEnum):
    VANILLA = 0
    BALANCED_RANDOM = 1
    SHUFFLED = 2
    FULLY_RANDOM = 3


# modified from the original since we can't have both a value and a setting from
# one option
# two options per palette would be rather ugly looking and probably a bit
# confusing
# SETTING is the old value, kept them around in case they were needed
@unique
class RandomPalettes(IntEnum):
    DEFAULT_PALETTE = 0
    SELECT_PALETTE = 1
    RANDOM_PICK = 10
    RANDOM_PICK_NOT_VANILLA = 11
    ALWAYS_RANDOM = 12
    RANDOM_PICK_SETTING = 2
    RANDOM_PICK_NOT_VANILLA_SETTING = 3
    ALWAYS_RANDOM_SETTING = 4

    @classmethod
    def get_setting_value(cls, value):
        if value == cls.ALWAYS_RANDOM:
            return cls.ALWAYS_RANDOM_SETTING
        elif value == cls.RANDOM_PICK_NOT_VANILLA:
            return cls.RANDOM_PICK_NOT_VANILLA_SETTING
        elif value == cls.RANDOM_PICK:
            return cls.RANDOM_PICK_SETTING
        return value


@unique
class MerlowRewardPricing(IntEnum):
    CHEAP = 0
    NORMAL = 1

    @classmethod
    def has_value(cls, value):
        return value in set(item.value for item in cls)


@unique
class PartnerUpgradeShuffle(IntEnum):
    OFF = 0
    SUPERBLOCKLOCATIONS = 1
    FULL = 2
