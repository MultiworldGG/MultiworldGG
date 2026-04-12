from enum import Enum


class DS2Version(Enum):
    SOTFS = "sotfs"
    VANILLA = "vanilla"


class APLocationType(Enum):
    ItemLotParam2_Chr = 100_000_000
    ItemLotParam2_Other = 200_000_000
    ShopLineupParam = 300_000_000


class APItemType(Enum):
    ITEM = 1
    EVENT = 2


class ItemCategory(Enum):
    MELEE_WEAPON = "Melee Weapons"
    RANGED_WEAPON = "Ranged Weapons"
    MISC_WEAPON = "Misc Weapons"
    STAFF = "Staves"
    CHIME = "Chimes"
    SHIELD = "Shields"
    HEAD_ARMOR = "Head Armor"
    CHEST_ARMOR = "Chest Armor"
    HANDS_ARMOR = "Hands Armor"
    LEGS_ARMOR = "Legs Armor"
    RING = "Rings"
    ARROW = "Arrows"
    GREAT_ARROW = "Great Arrows"
    BOLT = "Bolts"
    SPELL = "Spells"
    UNIQUE = "Unique Items"
    GOOD = "Goods"
    FLASK_UPGRADE = "Flask Upgrades"
    BOSS_SOUL = "Boss Souls"
    SOUL = "Souls"
    GESTURE = "Gestures"
    STATUE = "Statues"
    UPGRADE_MATERIAL = "Upgrade Materials"


class DLC(Enum):
    SUNKEN_KING = 1
    OLD_IRON_KING = 2
    IVORY_KING = 3
    ALL = 4
