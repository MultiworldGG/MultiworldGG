from __future__ import annotations

from enum import IntEnum
from typing import Iterable, NamedTuple

from BaseClasses import Item, ItemClassification as IC

from .data import ap_id_offset, Passage


# Items are encoded as 8-bit numbers as follows:
#                   | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
# Jewel pieces:     | 0   0   0 |  passage  | qdrnt |
# CD:               | 0   0   1 |  passage  | level |
# Keyzer:           | 1   1   0 |  passage  | level |
# Wario abilities:  | 0   1   0   0   0 |  ability  |
# Golden treasures: | 0   1   1   1 |   treasure    |
#
# Junk items:       | 1   0   0   0 |     type      |
# AP item:          | 1   1   1   1   0 |   class   |
#
# For jewel pieces:
#  - passage = 0-5 for entry/emerald/ruby/topaz/sapphire/golden
#  - qdrnt = quadrant, increasing counterclockwise from top left
#
# For CDs:
#  - passage = 0-5 same as jewel pieces, but only 1-4 has a CD
#  - level = increasing as the level goes deeper
#
# For Wario abilities:
#  - 0 = Progressive Ground Pound
#  - 1 = Swimming
#  - 2 = Head Smash
#  - 3 = Progressive Grab
#  - 4 = Dash Attack
#  - 5 = Stomp Jump
#
# Type for junk items:
#  - 0 = Full health item
#  - 1 = Wario form trap
#  - 2 = Single heart recovery
#  - 3 = Single heart damage
#  - 4 = Minigame Medal
#
# Classification for AP items:
#  - 0 = Filler
#  - 1 = Progression
#  - 2 = Useful
#  - 3 = Trap


class Box(IntEnum):
    JEWEL_NE = 0
    JEWEL_SE = 1
    JEWEL_SW = 2
    JEWEL_NW = 3


class JewelPieceItemData(NamedTuple):
    passage: Passage
    box: Box
    classification: IC

    def item_id(self):
        return (self.passage << 2) | self.box

    def flag(self):
        return 1 << self.box


class CdItemData(NamedTuple):
    passage: Passage
    level: int
    classification: IC

    def item_id(self):
        return (1 << 5) | (self.passage << 2) | self.level


class KeyzerItemData(NamedTuple):
    passage: Passage
    level: int
    classification: IC

    def item_id(self):
        return (6 << 5) | (self.passage << 2) | self.level


class AbilityItemData(NamedTuple):
    ability: int
    classification: IC

    def item_id(self):
        return (1 << 6) | self.ability


class GoldenTreasureItemData(NamedTuple):
    treasure: int
    classification: IC

    def item_id(self):
        return 0x70 | self.treasure

    def passage(self):
        return Passage(self.treasure // 3 + Passage.EMERALD)


class OtherItemData(NamedTuple):
    item: int
    classification: IC

    def item_id(self):
        return (1 << 7) | self.item


ItemData = JewelPieceItemData | CdItemData | KeyzerItemData | AbilityItemData | GoldenTreasureItemData | OtherItemData


jewel_piece_table = {
    "Top Right Entry Jewel Piece":      JewelPieceItemData(Passage.ENTRY,    Box.JEWEL_NE, IC.filler),
    "Top Right Emerald Piece":          JewelPieceItemData(Passage.EMERALD,  Box.JEWEL_NE, IC.progression_skip_balancing),
    "Top Right Ruby Piece":             JewelPieceItemData(Passage.RUBY,     Box.JEWEL_NE, IC.progression_skip_balancing),
    "Top Right Topaz Piece":            JewelPieceItemData(Passage.TOPAZ,    Box.JEWEL_NE, IC.progression_skip_balancing),
    "Top Right Sapphire Piece":         JewelPieceItemData(Passage.SAPPHIRE, Box.JEWEL_NE, IC.progression_skip_balancing),
    "Top Right Golden Jewel Piece":     JewelPieceItemData(Passage.GOLDEN,   Box.JEWEL_NE, IC.progression_skip_balancing),
    "Bottom Right Entry Jewel Piece":   JewelPieceItemData(Passage.ENTRY,    Box.JEWEL_SE, IC.filler),
    "Bottom Right Emerald Piece":       JewelPieceItemData(Passage.EMERALD,  Box.JEWEL_SE, IC.progression_skip_balancing),
    "Bottom Right Ruby Piece":          JewelPieceItemData(Passage.RUBY,     Box.JEWEL_SE, IC.progression_skip_balancing),
    "Bottom Right Topaz Piece":         JewelPieceItemData(Passage.TOPAZ,    Box.JEWEL_SE, IC.progression_skip_balancing),
    "Bottom Right Sapphire Piece":      JewelPieceItemData(Passage.SAPPHIRE, Box.JEWEL_SE, IC.progression_skip_balancing),
    "Bottom Right Golden Jewel Piece":  JewelPieceItemData(Passage.GOLDEN,   Box.JEWEL_SE, IC.progression_skip_balancing),
    "Bottom Left Entry Jewel Piece":    JewelPieceItemData(Passage.ENTRY,    Box.JEWEL_SW, IC.filler),
    "Bottom Left Emerald Piece":        JewelPieceItemData(Passage.EMERALD,  Box.JEWEL_SW, IC.progression_skip_balancing),
    "Bottom Left Ruby Piece":           JewelPieceItemData(Passage.RUBY,     Box.JEWEL_SW, IC.progression_skip_balancing),
    "Bottom Left Topaz Piece":          JewelPieceItemData(Passage.TOPAZ,    Box.JEWEL_SW, IC.progression_skip_balancing),
    "Bottom Left Sapphire Piece":       JewelPieceItemData(Passage.SAPPHIRE, Box.JEWEL_SW, IC.progression_skip_balancing),
    "Bottom Left Golden Jewel Piece":   JewelPieceItemData(Passage.GOLDEN,   Box.JEWEL_SW, IC.progression_skip_balancing),
    "Top Left Entry Jewel Piece":       JewelPieceItemData(Passage.ENTRY,    Box.JEWEL_NW, IC.filler),
    "Top Left Emerald Piece":           JewelPieceItemData(Passage.EMERALD,  Box.JEWEL_NW, IC.progression_skip_balancing),
    "Top Left Ruby Piece":              JewelPieceItemData(Passage.RUBY,     Box.JEWEL_NW, IC.progression_skip_balancing),
    "Top Left Topaz Piece":             JewelPieceItemData(Passage.TOPAZ,    Box.JEWEL_NW, IC.progression_skip_balancing),
    "Top Left Sapphire Piece":          JewelPieceItemData(Passage.SAPPHIRE, Box.JEWEL_NW, IC.progression_skip_balancing),
    "Top Left Golden Jewel Piece":      JewelPieceItemData(Passage.GOLDEN,   Box.JEWEL_NW, IC.progression_skip_balancing),
}

cd_table = {
    "About that Shepherd CD":           CdItemData(Passage.EMERALD,  0, IC.filler),
    "Things that Never Change CD":      CdItemData(Passage.EMERALD,  1, IC.filler),
    "Tomorrow's Blood Pressure CD":     CdItemData(Passage.EMERALD,  2, IC.filler),
    "Beyond the Headrush CD":           CdItemData(Passage.EMERALD,  3, IC.filler),
    "Driftwood & the Island Dog CD":    CdItemData(Passage.RUBY,     0, IC.filler),
    "The Judge's Feet CD":              CdItemData(Passage.RUBY,     1, IC.filler),
    "The Moon's Lamppost CD":           CdItemData(Passage.RUBY,     2, IC.filler),
    "Soft Shell CD":                    CdItemData(Passage.RUBY,     3, IC.filler),
    "So Sleepy CD":                     CdItemData(Passage.TOPAZ,    0, IC.filler),
    "The Short Futon CD":               CdItemData(Passage.TOPAZ,    1, IC.filler),
    "Avocado Song CD":                  CdItemData(Passage.TOPAZ,    2, IC.filler),
    "Mr. Fly CD":                       CdItemData(Passage.TOPAZ,    3, IC.filler),
    "Yesterday's Words CD":             CdItemData(Passage.SAPPHIRE, 0, IC.filler),
    "The Errand CD":                    CdItemData(Passage.SAPPHIRE, 1, IC.filler),
    "You and Your Shoes CD":            CdItemData(Passage.SAPPHIRE, 2, IC.filler),
    "Mr. Ether & Planaria CD":          CdItemData(Passage.SAPPHIRE, 3, IC.filler),
}

keyzer_table = {
    "Keyzer (Entry Passage Boss)":      KeyzerItemData(Passage.ENTRY,    0, IC.filler),
    "Keyzer (Emerald Passage 1)":       KeyzerItemData(Passage.EMERALD,  0, IC.progression),
    "Keyzer (Emerald Passage 2)":       KeyzerItemData(Passage.EMERALD,  1, IC.progression),
    "Keyzer (Emerald Passage 3)":       KeyzerItemData(Passage.EMERALD,  2, IC.progression),
    "Keyzer (Emerald Passage Boss)":    KeyzerItemData(Passage.EMERALD,  3, IC.progression),
    "Keyzer (Ruby Passage 1)":          KeyzerItemData(Passage.RUBY,     0, IC.progression),
    "Keyzer (Ruby Passage 2)":          KeyzerItemData(Passage.RUBY,     1, IC.progression),
    "Keyzer (Ruby Passage 3)":          KeyzerItemData(Passage.RUBY,     2, IC.progression),
    "Keyzer (Ruby Passage Boss)":       KeyzerItemData(Passage.RUBY,     3, IC.progression),
    "Keyzer (Topaz Passage 1)":         KeyzerItemData(Passage.TOPAZ,    0, IC.progression),
    "Keyzer (Topaz Passage 2)":         KeyzerItemData(Passage.TOPAZ,    1, IC.progression),
    "Keyzer (Topaz Passage 3)":         KeyzerItemData(Passage.TOPAZ,    2, IC.progression),
    "Keyzer (Topaz Passage Boss)":      KeyzerItemData(Passage.TOPAZ,    3, IC.progression),
    "Keyzer (Sapphire Passage 1)":      KeyzerItemData(Passage.SAPPHIRE, 0, IC.progression),
    "Keyzer (Sapphire Passage 2)":      KeyzerItemData(Passage.SAPPHIRE, 1, IC.progression),
    "Keyzer (Sapphire Passage 3)":      KeyzerItemData(Passage.SAPPHIRE, 2, IC.progression),
    "Keyzer (Sapphire Passage Boss)":   KeyzerItemData(Passage.SAPPHIRE, 3, IC.progression),
    "Keyzer (Golden Pyramid Boss)":     KeyzerItemData(Passage.GOLDEN,   0, IC.progression),
}

ability_table = {
    "Progressive Ground Pound":         AbilityItemData(0, IC.progression),
    "Swim":                             AbilityItemData(1, IC.progression),
    "Head Smash":                       AbilityItemData(2, IC.progression),
    "Progressive Grab":                 AbilityItemData(3, IC.progression),
    "Dash Attack":                      AbilityItemData(4, IC.progression),
    "Stomp Jump":                       AbilityItemData(5, IC.progression),
}

golden_treasure_table = {
    "Golden Tree Pot":                  GoldenTreasureItemData( 0, IC.progression_skip_balancing),
    "Golden Apple":                     GoldenTreasureItemData( 1, IC.progression_skip_balancing),
    "Golden Fish":                      GoldenTreasureItemData( 2, IC.progression_skip_balancing),
    "Golden Candle Holder":             GoldenTreasureItemData( 3, IC.progression_skip_balancing),
    "Golden Lamp":                      GoldenTreasureItemData( 4, IC.progression_skip_balancing),
    "Golden Crescent Moon Bed":         GoldenTreasureItemData( 5, IC.progression_skip_balancing),
    "Golden Teddy Bear":                GoldenTreasureItemData( 6, IC.progression_skip_balancing),
    "Golden Lollipop":                  GoldenTreasureItemData( 7, IC.progression_skip_balancing),
    "Golden Game Boy Advance":          GoldenTreasureItemData( 8, IC.progression_skip_balancing),
    "Golden Robot":                     GoldenTreasureItemData( 9, IC.progression_skip_balancing),
    "Golden Rocket":                    GoldenTreasureItemData(10, IC.progression_skip_balancing),
    "Golden Rocking Horse":             GoldenTreasureItemData(11, IC.progression_skip_balancing),
}

other_item_table = {
    "Full Health Item":                 OtherItemData(0, IC.useful),
    "Wario Form Trap":                  OtherItemData(1, IC.trap),
    "Heart":                            OtherItemData(2, IC.filler),
    "Lightning Trap":                   OtherItemData(3, IC.trap),
    "Minigame Medal":                   OtherItemData(4, IC.filler),
    "Diamond":                          OtherItemData(5, IC.filler),
}

item_table: dict[str, ItemData] = {
    **jewel_piece_table,
    **cd_table,
    **keyzer_table,
    **ability_table,
    **golden_treasure_table,
    **other_item_table,
}


item_name_to_id = {item_name: ap_id_offset + data.item_id() for item_name, data in item_table.items()}


def get_jewel_pieces_by_passage(passage: Passage) -> Iterable[str]:
    return (name for name, data in jewel_piece_table.items() if data.passage == passage)


class WL4ItemBase(Item):
    game: str = "Wario Land 4"
    data: ItemData | None


class WL4Item(WL4ItemBase):
    data: ItemData  # Promise this field is always filled

    def __init__(self, name: str, player: int, force_non_progression: bool = False, force_event: bool = False):
        self.data = item_table[name]
        super(WL4Item, self).__init__(
            name,
            IC.filler if force_non_progression else self.data.classification,
            None if force_event else item_name_to_id[name],
            player,
        )


class WL4EventItem(WL4ItemBase):
    def __init__(self, name: str, player: int):
        self.data = item_table.get(name)
        super(WL4EventItem, self).__init__(name, IC.progression, None, player)
