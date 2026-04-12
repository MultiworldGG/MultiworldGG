from typing import NamedTuple, Optional
from BaseClasses import Item, ItemClassification


class SongData(NamedTuple):
    """Special data container to contain the metadata of each song to make filtering work."""

    code: Optional[int]
    songID: Optional[int]
    singers: set[str]
    DLC: bool
    modded: bool
    difficulties: list[float]


class MegaMixSongItem(Item):
    game: str = "Hatsune Miku Project Diva Mega Mix+"

    def __init__(self, name: str, player: int, data: SongData) -> None:
        super().__init__(name, ItemClassification.progression, data.code, player)


class MegaMixFixedItem(Item):
    game: str = "Hatsune Miku Project Diva Mega Mix+"

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int) -> None:
        super().__init__(name, classification, code, player)
