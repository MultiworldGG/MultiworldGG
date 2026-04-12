from dataclasses import dataclass, field
from enum import Enum
from itertools import count

from BaseClasses import Item, ItemClassification

from .constants import BASE_ID

_id_generator = count(BASE_ID, step=1)


class BrotatoItem(Item):
    game: str = "Brotato"


@dataclass(frozen=True)
class BrotatoItemBase:
    """Hold item data before we assign to a player."""

    name: "ItemName"
    classification: ItemClassification
    # Auto-increments ID without us having to manually set it, so item definition order matters.
    code: int = field(default_factory=_id_generator.__next__)

    def to_item(self, player: int) -> BrotatoItem:
        return BrotatoItem(self.name.value, self.classification, self.code, player)


class ItemName(Enum):
    COMMON_ITEM = "Common Item"
    UNCOMMON_ITEM = "Uncommon Item"
    RARE_ITEM = "Rare Item"
    LEGENDARY_ITEM = "Legendary Item"
    COMMON_UPGRADE = "Common Upgrade"
    UNCOMMON_UPGRADE = "Uncommon Upgrade"
    RARE_UPGRADE = "Rare Upgrade"
    LEGENDARY_UPGRADE = "Legendary Upgrade"
    SHOP_SLOT = "Progressive Shop Slot"
    SHOP_LOCK_BUTTON = "Progressive Shop Lock Button"
    XP_5 = "XP (5)"
    XP_10 = "XP (10)"
    XP_25 = "XP (25)"
    XP_50 = "XP (50)"
    XP_100 = "XP (100)"
    XP_150 = "XP (150)"
    GOLD_10 = "Gold (10)"
    GOLD_25 = "Gold (25)"
    GOLD_50 = "Gold (50)"
    GOLD_100 = "Gold (100)"
    GOLD_200 = "Gold (200)"
    RUN_COMPLETE = "Run Won"
    # Base game characters
    CHARACTER_WELL_ROUNDED = "Well Rounded"
    CHARACTER_BRAWLER = "Brawler"
    CHARACTER_CRAZY = "Crazy"
    CHARACTER_RANGER = "Ranger"
    CHARACTER_MAGE = "Mage"
    CHARACTER_CHUNKY = "Chunky"
    CHARACTER_OLD = "Old"
    CHARACTER_LUCKY = "Lucky"
    CHARACTER_MUTANT = "Mutant"
    CHARACTER_GENERALIST = "Generalist"
    CHARACTER_LOUD = "Loud"
    CHARACTER_MULTITASKER = "Multitasker"
    CHARACTER_WILDLING = "Wildling"
    CHARACTER_PACIFIST = "Pacifist"
    CHARACTER_GLADIATOR = "Gladiator"
    CHARACTER_SAVER = "Saver"
    CHARACTER_SICK = "Sick"
    CHARACTER_FARMER = "Farmer"
    CHARACTER_GHOST = "Ghost"
    CHARACTER_SPEEDY = "Speedy"
    CHARACTER_ENTREPRENEUR = "Entrepreneur"
    CHARACTER_ENGINEER = "Engineer"
    CHARACTER_EXPLORER = "Explorer"
    CHARACTER_DOCTOR = "Doctor"
    CHARACTER_HUNTER = "Hunter"
    CHARACTER_ARTIFICER = "Artificer"
    CHARACTER_ARMS_DEALER = "Arms Dealer"
    CHARACTER_STREAMER = "Streamer"
    CHARACTER_CYBORG = "Cyborg"
    CHARACTER_GLUTTON = "Glutton"
    CHARACTER_JACK = "Jack"
    CHARACTER_LICH = "Lich"
    CHARACTER_APPRENTICE = "Apprentice"
    CHARACTER_CRYPTID = "Cryptid"
    CHARACTER_FISHERMAN = "Fisherman"
    CHARACTER_GOLEM = "Golem"
    CHARACTER_KING = "King"
    CHARACTER_RENEGADE = "Renegade"
    CHARACTER_ONE_ARMED = "One Armed"
    CHARACTER_BULL = "Bull"
    CHARACTER_SOLDIER = "Soldier"
    CHARACTER_MASOCHIST = "Masochist"
    CHARACTER_KNIGHT = "Knight"
    CHARACTER_DEMON = "Demon"
    # Abyssal Terrors Characters
    CHARACTER_BABY = "Baby"
    CHARACTER_VAGABOND = "Vagabond"
    CHARACTER_TECHNOMAGE = "Technomage"
    CHARACTER_VAMPIRE = "Vampire"
    CHARACTER_BEAST_MASTER = "Beast Master"
    CHARACTER_SAILOR = "Sailor"
    CHARACTER_CURIOUS = "Curious"
    CHARACTER_BUILDER = "Builder"
    CHARACTER_CAPTAIN = "Captain"
    CHARACTER_CREATURE = "Creature"
    CHARACTER_CHEF = "Chef"
    CHARACTER_DRUID = "Druid"
    CHARACTER_DWARF = "Dwarf"
    CHARACTER_GANGSTER = "Gangster"
    CHARACTER_DIVER = "Diver"
    CHARACTER_HIKER = "Hiker"
    CHARACTER_BUCCANEER = "Buccaneer"
    CHARACTER_OGRE = "Ogre"
    CHARACTER_ROMANTIC = "Romantic"


_char_items: list[ItemName] = [x for x in ItemName if x.name.startswith("CHARACTER_")]

_items: list[BrotatoItemBase] = [
    BrotatoItemBase(name=ItemName.COMMON_ITEM, classification=ItemClassification.useful),
    BrotatoItemBase(name=ItemName.UNCOMMON_ITEM, classification=ItemClassification.useful),
    BrotatoItemBase(name=ItemName.RARE_ITEM, classification=ItemClassification.useful),
    BrotatoItemBase(name=ItemName.LEGENDARY_ITEM, classification=ItemClassification.useful),
    BrotatoItemBase(name=ItemName.COMMON_UPGRADE, classification=ItemClassification.useful),
    BrotatoItemBase(name=ItemName.UNCOMMON_UPGRADE, classification=ItemClassification.useful),
    BrotatoItemBase(name=ItemName.RARE_UPGRADE, classification=ItemClassification.useful),
    BrotatoItemBase(name=ItemName.LEGENDARY_UPGRADE, classification=ItemClassification.useful),
    BrotatoItemBase(name=ItemName.SHOP_SLOT, classification=ItemClassification.useful),
    BrotatoItemBase(name=ItemName.SHOP_LOCK_BUTTON, classification=ItemClassification.useful),
    BrotatoItemBase(name=ItemName.XP_5, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_10, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_25, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_50, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_100, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.XP_150, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.GOLD_10, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.GOLD_25, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.GOLD_50, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.GOLD_100, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.GOLD_200, classification=ItemClassification.filler),
    BrotatoItemBase(name=ItemName.RUN_COMPLETE, classification=ItemClassification.progression),
    # Individual items for each character
    *[BrotatoItemBase(name=c, classification=ItemClassification.progression) for c in _char_items],
]

item_table: dict[int, BrotatoItemBase] = {item.code: item for item in _items}
item_name_to_id: dict[str, int] = {item.name.value: item.code for item in _items}

filler_items: list[str] = [
    item.name.value for item in item_table.values() if item.classification == ItemClassification.filler
]

item_name_groups: dict[str, set[str]] = {
    "Item Drops": {
        ItemName.COMMON_ITEM.value,
        ItemName.UNCOMMON_ITEM.value,
        ItemName.RARE_ITEM.value,
        ItemName.LEGENDARY_ITEM.value,
    },
    "Upgrades": {
        ItemName.COMMON_UPGRADE.value,
        ItemName.UNCOMMON_UPGRADE.value,
        ItemName.RARE_UPGRADE.value,
        ItemName.LEGENDARY_UPGRADE.value,
    },
    "Shop": {ItemName.SHOP_SLOT.value, ItemName.SHOP_LOCK_BUTTON.value},
    "Gold": {
        ItemName.GOLD_10.value,
        ItemName.GOLD_25.value,
        ItemName.GOLD_50.value,
        ItemName.GOLD_100.value,
        ItemName.GOLD_200.value,
    },
    "XP": {
        ItemName.XP_5.value,
        ItemName.XP_10.value,
        ItemName.XP_25.value,
        ItemName.XP_50.value,
        ItemName.XP_100.value,
        ItemName.XP_150.value,
    },
    "Characters": {c.value for c in _char_items},
}
