from dataclasses import dataclass
from enum import Enum
from functools import cached_property

BASE_ID = 0x7A70_0000


NUM_WAVES = 20
MAX_DIFFICULTY = 5


class ItemRarity(Enum):
    # These values match the constants in Brotato, which the client mod uses. Change at your own risk.
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    LEGENDARY = 3


@dataclass(frozen=True)
class CharacterGroup:
    name: str
    characters: tuple[str, ...]
    """All characters in the group"""
    default_characters: tuple[str, ...]
    """The characters available from the group in a fresh save of the game."""

    @cached_property
    def unlockable_characters(self) -> tuple[str, ...]:
        """The characters in the group which must be unlocked."""
        return tuple(set(self.characters) - set(self.default_characters))

    @cached_property
    def num_characters(self) -> int:
        return len(self.characters)

    @cached_property
    def num_default_characters(self) -> int:
        return len(self.default_characters)

    @cached_property
    def num_unlockable_characters(self) -> int:
        return len(self.unlockable_characters)


class CharacterGroups(dict[str, CharacterGroup]):
    base: CharacterGroup
    abyssal_terrors: CharacterGroup


BASE_GAME_CHARACTERS = CharacterGroup(
    name="Base Game",
    characters=(
        "Well Rounded",
        "Brawler",
        "Crazy",
        "Ranger",
        "Mage",
        "Chunky",
        "Old",
        "Lucky",
        "Mutant",
        "Generalist",
        "Loud",
        "Multitasker",
        "Wildling",
        "Pacifist",
        "Gladiator",
        "Saver",
        "Sick",
        "Farmer",
        "Ghost",
        "Speedy",
        "Entrepreneur",
        "Engineer",
        "Explorer",
        "Doctor",
        "Hunter",
        "Artificer",
        "Arms Dealer",
        "Streamer",
        "Cyborg",
        "Glutton",
        "Jack",
        "Lich",
        "Apprentice",
        "Cryptid",
        "Fisherman",
        "Golem",
        "King",
        "Renegade",
        "One Armed",
        "Bull",
        "Soldier",
        "Masochist",
        "Knight",
        "Demon",
        "Baby",
        "Vagabond",
        "Technomage",
        "Vampire",
        "Beast Master",
    ),
    default_characters=("Well Rounded", "Brawler", "Crazy", "Ranger", "Mage"),
)

ABYSSAL_TERRORS_CHARACTERS = CharacterGroup(
    name="Abyssal Terrors DLC",
    characters=(
        "Sailor",
        "Curious",
        "Builder",
        "Captain",
        "Creature",
        "Chef",
        "Druid",
        "Dwarf",
        "Gangster",
        "Diver",
        "Hiker",
        "Buccaneer",
        "Ogre",
        "Romantic",
    ),
    default_characters=("Sailor", "Curious", "Builder", "Captain", "Creature"),
)

CHARACTER_GROUPS = CharacterGroups(base=BASE_GAME_CHARACTERS, abyssal_terrors=ABYSSAL_TERRORS_CHARACTERS)
"""Mapping of game pack to its character group.

Used to easily iterate over different groups of characters, so adding characters from future DLCs is simpler.
"""

ALL_CHARACTERS = tuple(c for group in CHARACTER_GROUPS.values() for c in group.characters)
"""Tuple of all characters from the base game and DLC."""
TOTAL_NUM_CHARACTERS = len(ALL_CHARACTERS)
"""The total number of character across the base game and all DLC."""

MAX_REQUIRED_RUN_WINS = TOTAL_NUM_CHARACTERS

MAX_NORMAL_CRATE_DROPS = 50
MAX_LEGENDARY_CRATE_DROPS = 50

# THe maximum number of groups is the maximum number of crates, otherwise we'd have
# groups which could never be filled.
MAX_NORMAL_CRATE_DROP_GROUPS = MAX_NORMAL_CRATE_DROPS
MAX_LEGENDARY_CRATE_DROP_GROUPS = MAX_LEGENDARY_CRATE_DROPS

# Weights to use when generating Brotato items using the "default item weights" option. These weights are intended to
# match the rarity of each tier in the vanilla game. The distribution is not explicitly defined in the game, but we can
# make a reasonable guess by looking at the max chances of getting items of each rarity/tier from the shop or loot
# crates, which are publicly listed here: https://brotato.wiki.spellsandguns.com/Shop#Rarity_of_Shop_Items_and_Luck. We
# use the values from the "Max Chance" column in the table in the linked sections as weights. It's not perfect, but it
# "feels" right and seems close enough.
DEFAULT_ITEM_WEIGHTS: tuple[int, int, int, int] = (100, 60, 25, 8)

MAX_COMMON_UPGRADES = 50
MAX_UNCOMMON_UPGRADES = 50
MAX_RARE_UPGRADES = 50
MAX_LEGENDARY_UPGRADES = 50

MAX_SHOP_SLOTS = 4  # Brotato default, can't easily increase beyond this.

# Location name string templates
CRATE_DROP_LOCATION_TEMPLATE = "Loot Crate {num}"
LEGENDARY_CRATE_DROP_LOCATION_TEMPLATE = "Legendary Loot Crate {num}"
WAVE_COMPLETE_LOCATION_TEMPLATE = "Wave {wave} Completed ({char})"
RUN_COMPLETE_LOCATION_TEMPLATE = "Run Won ({char})"
SHOP_ITEM_LOCATION_TEMPLATE = "{tier} Shop Item {num}"

# Region name string templates
CRATE_DROP_GROUP_REGION_TEMPLATE = "Loot Crate Group {num}"
LEGENDARY_CRATE_DROP_GROUP_REGION_TEMPLATE = "Legendary Loot Crate Group {num}"
CHARACTER_REGION_TEMPLATE = "In-Game ({char})"
