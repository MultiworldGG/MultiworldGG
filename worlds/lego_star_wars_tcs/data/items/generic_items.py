from enum import StrEnum

from . import GenericItemData, GENERIC_ITEMS_BASE, MinikitItemData
from ..areas import Area, EPISODE_AREA_LOOKUP

class NonDataItemName(StrEnum):
    """
    Names of items that are not determined by explicitly defined data.
    """


    # AP Items.
    PROGRESSIVE_SCORE_MULTIPLIER = "Progressive Score Multiplier"

    EPISODE_COMPLETION_TOKEN = "Episode Completion Token"

    EPISODE_1_UNLOCK = "Episode 1 Unlock"
    EPISODE_2_UNLOCK = "Episode 2 Unlock"
    EPISODE_3_UNLOCK = "Episode 3 Unlock"
    EPISODE_4_UNLOCK = "Episode 4 Unlock"
    EPISODE_5_UNLOCK = "Episode 5 Unlock"
    EPISODE_6_UNLOCK = "Episode 6 Unlock"

    MINIKIT = "Minikit"
    TWO_MINIKITS = "2 Minikits"
    FIVE_MINIKITS = "5 Minikits"
    TEN_MINIKITS = "10 Minikits"

    KYBER_BRICK = "Kyber Brick"

    POWER_UP = "Power Up"

    SILVER_STUD = "Silver Stud"
    GOLD_STUD = "Gold Stud"
    BLUE_STUD = "Blue Stud"
    PURPLE_STUD = "Purple Stud"


# todo: Rename this to be in the format like "Negotiations (1-1) Unlock"
CHAPTER_TO_CHAPTER_UNLOCK_ITEM = {
    EPISODE_AREA_LOOKUP[episode][chapter]: f"{episode}-{chapter} Unlock"
    for chapter in range(1, 7)
    for episode in range(1, 7)
}
CHAPTER_UNLOCK_ITEM_TO_CHAPTER: dict[str, Area] = {v: k for k, v in CHAPTER_TO_CHAPTER_UNLOCK_ITEM.items()}
assert len(CHAPTER_UNLOCK_ITEM_TO_CHAPTER) == len(CHAPTER_TO_CHAPTER_UNLOCK_ITEM)

EPISODE_UNLOCKS: dict[int, NonDataItemName] = {
    1: NonDataItemName.EPISODE_1_UNLOCK,
    2: NonDataItemName.EPISODE_2_UNLOCK,
    3: NonDataItemName.EPISODE_3_UNLOCK,
    4: NonDataItemName.EPISODE_4_UNLOCK,
    5: NonDataItemName.EPISODE_5_UNLOCK,
    6: NonDataItemName.EPISODE_6_UNLOCK,
}
EPISODE_UNLOCK_TO_EPISODE: dict[str, int] = {v: k for k, v in EPISODE_UNLOCKS.items()}
assert len(EPISODE_UNLOCK_TO_EPISODE) == len(EPISODE_UNLOCKS)

def _generic(code: int | None, name: str) -> GenericItemData:
    # Ensure any StrEnum is replaced with str.
    return GenericItemData(code + GENERIC_ITEMS_BASE if code is not None else None, str(name))

def _minikit(code: int | None, name: str, size: int) -> MinikitItemData:
    # Ensure any StrEnum is replaced with str.
    return MinikitItemData(code + GENERIC_ITEMS_BASE if code is not None else None, str(name), size)

GENERIC_DATA: list[GenericItemData] = [
    *[_generic(area, name) for area, name in CHAPTER_TO_CHAPTER_UNLOCK_ITEM.items()],
    _generic(500, NonDataItemName.PROGRESSIVE_SCORE_MULTIPLIER),

    _generic(510, NonDataItemName.EPISODE_COMPLETION_TOKEN),

    _generic(520, NonDataItemName.EPISODE_1_UNLOCK),
    _generic(521, NonDataItemName.EPISODE_2_UNLOCK),
    _generic(522, NonDataItemName.EPISODE_3_UNLOCK),
    _generic(523, NonDataItemName.EPISODE_4_UNLOCK),
    _generic(524, NonDataItemName.EPISODE_5_UNLOCK),
    _generic(525, NonDataItemName.EPISODE_6_UNLOCK),

    _minikit(530, NonDataItemName.MINIKIT, 1),
    _minikit(531, NonDataItemName.TWO_MINIKITS, 2),
    _minikit(534, NonDataItemName.FIVE_MINIKITS, 5),
    _minikit(539, NonDataItemName.TEN_MINIKITS, 10),

    _generic(540, NonDataItemName.KYBER_BRICK),

    _generic(550, NonDataItemName.POWER_UP),

    _generic(560, NonDataItemName.SILVER_STUD),
    _generic(561, NonDataItemName.GOLD_STUD),
    _generic(562, NonDataItemName.BLUE_STUD),
    _generic(563, NonDataItemName.PURPLE_STUD),
]
GENERIC_DATA_BY_NAME: dict[str, GenericItemData] = {
    data.name: data for data in GENERIC_DATA
}

MINIKITS_BY_BUNDLE_SIZE: dict[int, MinikitItemData] = {
    data.bundle_size: data for data in GENERIC_DATA if isinstance(data, MinikitItemData)
}

MINIKITS_BY_NAME: dict[str, MinikitItemData] = {
    data.name: data for data in MINIKITS_BY_BUNDLE_SIZE.values()
}
