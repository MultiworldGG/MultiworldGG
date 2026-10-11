from __future__ import annotations

import typing

from BaseClasses import Item, ItemClassification

base_id = 3_870_000


class OddCoupleItem(Item):
    game: str = "Ratchet & Clank: The Odd Couple"


class ItemData(typing.NamedTuple):
    code: int
    classification: ItemClassification


item_table: typing.Dict[str, ItemData] = {
    "Stereo": ItemData(base_id + 0, ItemClassification.progression),
    "Taxi Driver": ItemData(base_id + 1, ItemClassification.progression),
    "Gimp": ItemData(base_id + 2, ItemClassification.progression),
    "Phonecall": ItemData(base_id + 3, ItemClassification.progression),
    "Scissors": ItemData(base_id + 4, ItemClassification.progression),
    "TV": ItemData(base_id + 5, ItemClassification.progression),
    # Pure junk - it pads the pool out to match the location count (see
    # progression_items below) but isn't required for anything, since every
    # location is gated by holding a named scene item, not by what's placed there.
    "Nothing": ItemData(base_id + 6, ItemClassification.filler),
}

# The scene-unlock items, one copy of each placed in the pool. "Gimp" gates
# all three Gimp locations at once but is held (not consumed), so a single
# copy unlocks all three replays - it doesn't need three copies.
progression_items: typing.List[str] = [name for name in item_table if name != "Nothing"]

lookup_id_to_name: typing.Dict[int, str] = {data.code: name for name, data in item_table.items()}
