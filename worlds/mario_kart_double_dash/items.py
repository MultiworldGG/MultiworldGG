from typing import Any, NamedTuple, TYPE_CHECKING
from enum import Enum

from BaseClasses import Item, ItemClassification
from . import game_data, version

if TYPE_CHECKING:
    from . import MkddWorld

PROG = ItemClassification.progression
FILL = ItemClassification.filler
USEF = ItemClassification.useful
SKIP = ItemClassification.progression_skip_balancing
TRAP = ItemClassification.trap

TAG_CUPS = "Cups"
TAG_TT_COURSES = "TT Courses"
TAG_CHARACTERS = "Characters"
TAG_KARTS = "Karts"
TAG_ITEMS = "Items"
TAG_KART_UPGRADES = "Kart Upgrades"
TAG_TRAPS = "Trap"
TAG_SYNC_ONLY = "*Sync/Online Only"

class ItemType(Enum):
    OTHER = 0
    CHARACTER = 1
    KART = 2
    CUP = 3
    TT_COURSE = 4
    ITEM_UNLOCK = 5
    KART_UPGRADE = 6
    RAIN_TRAP = 7

class MkddItem(Item):
    game = version.get_game_name()


class MkddItemData(NamedTuple):
    name: str
    classification: int
    item_type: ItemType = ItemType.OTHER
    address: int = 0
    count: int = 1
    meta: Any = None
    tags: set[str] = set()


PROGRESSIVE_CLASS = "Progressive CC"
PROGRESSIVE_CUP_SKIP = "Progressive GP Race Skip"
PROGRESSIVE_TIME_TRIAL_ITEM = "Progressive Time Trial Item"
PROGRESSIVE_ENGINE = "Progressive Speed Upgrade"
PROGRESSIVE_STARTING_POSITION = "Progressive Starting Position"
RANDOM_ITEM = "Random Item"
TROPHY = "Trophy"
VICTORY = "Victory"
SKIP_DIFFICULTY = "Skip Difficulty Calculation"

OVERLAPPING_START_TRAP = "Overlapping Start Trap"
BANANA_RAIN_TRAP = "Banana Rain Trap"
SHELL_RAIN_TRAP = "Shell Rain Trap"
BOMB_RAIN_TRAP = "Bomb Rain Trap"

def get_item_name_tt_course(course: str) -> str:
    return f"{course} Time Trial"

def get_item_name_character_item(character: str|None, item: str) -> str:
    if character != None:
        return f"{item} for {character}"
    else:
        return f"{item} for Everybody"

def get_item_name_kart_upgrade(upgrade: str, kart: str) -> str:
    return f"{upgrade} for {kart}"


data_table: list[MkddItemData] = [
    MkddItemData("", 0, count = 0), # Id 0 is reserved
    MkddItemData(PROGRESSIVE_CLASS, PROG, count = 3),
    MkddItemData(PROGRESSIVE_CUP_SKIP, USEF, count = 2),
    MkddItemData(PROGRESSIVE_TIME_TRIAL_ITEM, PROG, count = 3),
    MkddItemData(PROGRESSIVE_ENGINE, PROG, count = 0), # Count depends on options.
    MkddItemData(RANDOM_ITEM, FILL, tags={TAG_SYNC_ONLY}),
    MkddItemData(TROPHY, PROG, count = 0),
    MkddItemData(VICTORY, PROG, count = 0),
]
data_table.extend([MkddItemData(char.name, PROG, ItemType.CHARACTER, id, tags = {TAG_CHARACTERS}) for id, char in enumerate(game_data.CHARACTERS)])
data_table.extend([MkddItemData(name, PROG, ItemType.CUP, id, 1 if id != game_data.CUP_ALL_CUP_TOUR else 0, tags = {TAG_CUPS}) for id, name in enumerate(game_data.CUPS)])
data_table.extend([MkddItemData(get_item_name_tt_course(course.name), PROG, ItemType.TT_COURSE, id, tags = {TAG_TT_COURSES}) for id, course in enumerate(game_data.RACE_COURSES)])

for id, kart in enumerate(game_data.KARTS):
    data_table.append(MkddItemData(kart.name, PROG, ItemType.KART, id, tags = {TAG_KARTS}))
    for upgrade in game_data.KART_UPGRADES:
        name = get_item_name_kart_upgrade(upgrade.name, kart.name)
        TAG_KART_UPGRADES_FOR_X = {TAG_KART_UPGRADES, f"Kart upgrades for {kart.name}"}
        data_table.append(MkddItemData(name, PROG, ItemType.KART_UPGRADE, id, 0, upgrade, tags = TAG_KART_UPGRADES_FOR_X))

for item in game_data.ITEMS:
    classification = PROG if item.usefulness > 0 else FILL
    if item != game_data.ITEM_NONE:
        data_table.append(MkddItemData(
            get_item_name_character_item(None, item.name), classification,
            ItemType.ITEM_UNLOCK, count = 0, meta = {"character":None, "item":item},
            tags = {TAG_ITEMS}
            ))
        for character in game_data.CHARACTERS:
            name = get_item_name_character_item(character.name, item.name)
            TAG_ITEMS_FOR_X = {TAG_ITEMS, f"Items for {character.name}"}
            data_table.append(MkddItemData(
                name, classification, ItemType.ITEM_UNLOCK, count = 0,
                meta = {"character": character, "item": item}, tags = TAG_ITEMS_FOR_X
            ))

data_table.append(MkddItemData(PROGRESSIVE_STARTING_POSITION, USEF, count=7))
data_table.append(MkddItemData(OVERLAPPING_START_TRAP, TRAP, count=0, tags={TAG_TRAPS, TAG_SYNC_ONLY}))
data_table.append(MkddItemData(BANANA_RAIN_TRAP, TRAP, ItemType.RAIN_TRAP, count=0, tags={TAG_TRAPS, TAG_SYNC_ONLY}))
data_table.append(MkddItemData(SHELL_RAIN_TRAP, TRAP, ItemType.RAIN_TRAP, count=0, tags={TAG_TRAPS, TAG_SYNC_ONLY}))
data_table.append(MkddItemData(BOMB_RAIN_TRAP, TRAP, ItemType.RAIN_TRAP, count=0, tags={TAG_TRAPS, TAG_SYNC_ONLY}))

# Used by Universal Tracker glitched logic.
data_table.append(MkddItemData(SKIP_DIFFICULTY, PROG, count = 0))

name_to_id: dict[str, int] = {item.name:id for (id, item) in enumerate(data_table) if id > 0}

group_names: set[str] = set()
for data in data_table:
    group_names.update({tag for tag in data.tags if not tag.startswith("*")})
groups: dict[str: set[str]] = {
    group:{data.name for data in data_table if group in data.tags}
    for group in group_names
}
