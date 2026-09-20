from dataclasses import dataclass, field
from enum import Enum
from itertools import count

from BaseClasses import Item, ItemClassification

from .constants import BASE_ID, PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE

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
    CHARACTER_BEAST_MASTER = "Beast Master"
    CHARACTER_WOUNDED = "Wounded"
    # Abyssal Terrors Characters
    CHARACTER_BABY = "Baby"
    CHARACTER_VAGABOND = "Vagabond"
    CHARACTER_TECHNOMAGE = "Technomage"
    CHARACTER_VAMPIRE = "Vampire"
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
    # Base game characters
    PROGRESSIVE_WAVE_CAP_WELL_ROUNDED = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Well Rounded")
    PROGRESSIVE_WAVE_CAP_BRAWLER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Brawler")
    PROGRESSIVE_WAVE_CAP_CRAZY = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Crazy")
    PROGRESSIVE_WAVE_CAP_RANGER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Ranger")
    PROGRESSIVE_WAVE_CAP_MAGE = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Mage")
    PROGRESSIVE_WAVE_CAP_CHUNKY = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Chunky")
    PROGRESSIVE_WAVE_CAP_OLD = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Old")
    PROGRESSIVE_WAVE_CAP_LUCKY = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Lucky")
    PROGRESSIVE_WAVE_CAP_MUTANT = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Mutant")
    PROGRESSIVE_WAVE_CAP_GENERALIST = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Generalist")
    PROGRESSIVE_WAVE_CAP_LOUD = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Loud")
    PROGRESSIVE_WAVE_CAP_MULTITASKER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Multitasker")
    PROGRESSIVE_WAVE_CAP_WILDLING = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Wildling")
    PROGRESSIVE_WAVE_CAP_PACIFIST = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Pacifist")
    PROGRESSIVE_WAVE_CAP_GLADIATOR = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Gladiator")
    PROGRESSIVE_WAVE_CAP_SAVER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Saver")
    PROGRESSIVE_WAVE_CAP_SICK = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Sick")
    PROGRESSIVE_WAVE_CAP_FARMER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Farmer")
    PROGRESSIVE_WAVE_CAP_GHOST = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Ghost")
    PROGRESSIVE_WAVE_CAP_SPEEDY = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Speedy")
    PROGRESSIVE_WAVE_CAP_ENTREPRENEUR = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Entrepreneur")
    PROGRESSIVE_WAVE_CAP_ENGINEER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Engineer")
    PROGRESSIVE_WAVE_CAP_EXPLORER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Explorer")
    PROGRESSIVE_WAVE_CAP_DOCTOR = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Doctor")
    PROGRESSIVE_WAVE_CAP_HUNTER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Hunter")
    PROGRESSIVE_WAVE_CAP_ARTIFICER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Artificer")
    PROGRESSIVE_WAVE_CAP_ARMS_DEALER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Arms Dealer")
    PROGRESSIVE_WAVE_CAP_STREAMER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Streamer")
    PROGRESSIVE_WAVE_CAP_CYBORG = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Cyborg")
    PROGRESSIVE_WAVE_CAP_GLUTTON = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Glutton")
    PROGRESSIVE_WAVE_CAP_JACK = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Jack")
    PROGRESSIVE_WAVE_CAP_LICH = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Lich")
    PROGRESSIVE_WAVE_CAP_APPRENTICE = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Apprentice")
    PROGRESSIVE_WAVE_CAP_CRYPTID = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Cryptid")
    PROGRESSIVE_WAVE_CAP_FISHERMAN = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Fisherman")
    PROGRESSIVE_WAVE_CAP_GOLEM = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Golem")
    PROGRESSIVE_WAVE_CAP_KING = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="King")
    PROGRESSIVE_WAVE_CAP_RENEGADE = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Renegade")
    PROGRESSIVE_WAVE_CAP_ONE_ARMED = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="One Armed")
    PROGRESSIVE_WAVE_CAP_BULL = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Bull")
    PROGRESSIVE_WAVE_CAP_SOLDIER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Soldier")
    PROGRESSIVE_WAVE_CAP_MASOCHIST = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Masochist")
    PROGRESSIVE_WAVE_CAP_KNIGHT = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Knight")
    PROGRESSIVE_WAVE_CAP_DEMON = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Demon")
    PROGRESSIVE_WAVE_CAP_BEAST_MASTER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Beast Master")
    PROGRESSIVE_WAVE_CAP_WOUNDED = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Wounded")
    # Abyssal Terrors Characters
    PROGRESSIVE_WAVE_CAP_BABY = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Baby")
    PROGRESSIVE_WAVE_CAP_VAGABOND = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Vagabond")
    PROGRESSIVE_WAVE_CAP_TECHNOMAGE = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Technomage")
    PROGRESSIVE_WAVE_CAP_VAMPIRE = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Vampire")
    PROGRESSIVE_WAVE_CAP_SAILOR = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Sailor")
    PROGRESSIVE_WAVE_CAP_CURIOUS = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Curious")
    PROGRESSIVE_WAVE_CAP_BUILDER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Builder")
    PROGRESSIVE_WAVE_CAP_CAPTAIN = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Captain")
    PROGRESSIVE_WAVE_CAP_CREATURE = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Creature")
    PROGRESSIVE_WAVE_CAP_CHEF = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Chef")
    PROGRESSIVE_WAVE_CAP_DRUID = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Druid")
    PROGRESSIVE_WAVE_CAP_DWARF = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Dwarf")
    PROGRESSIVE_WAVE_CAP_GANGSTER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Gangster")
    PROGRESSIVE_WAVE_CAP_DIVER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Diver")
    PROGRESSIVE_WAVE_CAP_HIKER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Hiker")
    PROGRESSIVE_WAVE_CAP_BUCCANEER = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Buccaneer")
    PROGRESSIVE_WAVE_CAP_OGRE = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Ogre")
    PROGRESSIVE_WAVE_CAP_ROMANTIC = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char="Romantic")


_char_items: list[ItemName] = [x for x in ItemName if x.name.startswith("CHARACTER_")]
_wave_cap_items: list[ItemName] = [x for x in ItemName if x.name.startswith("PROGRESSIVE_WAVE_CAP")]

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
    *[BrotatoItemBase(name=c, classification=ItemClassification.progression) for c in _wave_cap_items],
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
