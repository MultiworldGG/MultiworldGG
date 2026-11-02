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

    def item_id(self):
        return (self.passage << 2) | self.box

    def flag(self):
        return 1 << self.box

    @property
    def classification(self):
        return IC.progression_skip_balancing


class CdItemData(NamedTuple):
    passage: Passage
    level: int

    def item_id(self):
        return (1 << 5) | (self.passage << 2) | self.level

    @property
    def classification(self):
        return IC.filler


class KeyzerItemData(NamedTuple):
    passage: Passage
    level: int

    def item_id(self):
        return (6 << 5) | (self.passage << 2) | self.level

    @property
    def classification(self):
        return IC.progression


class AbilityItemData(NamedTuple):
    ability: int

    def item_id(self):
        return (1 << 6) | self.ability

    @property
    def classification(self):
        return IC.progression


class GoldenTreasureItemData(NamedTuple):
    treasure: int

    def item_id(self):
        return 0x70 | self.treasure

    def passage(self):
        return Passage(self.treasure // 3 + Passage.EMERALD)

    @property
    def classification(self):
        return IC.progression_skip_balancing


class OtherItemData(NamedTuple):
    item: int
    classification: IC

    def item_id(self):
        return (1 << 7) | self.item


ItemData = JewelPieceItemData | CdItemData | KeyzerItemData | AbilityItemData | GoldenTreasureItemData | OtherItemData


jewel_piece_table = {
    "Top Right Entry Jewel Piece":      JewelPieceItemData(Passage.ENTRY,    Box.JEWEL_NE),
    "Top Right Emerald Piece":          JewelPieceItemData(Passage.EMERALD,  Box.JEWEL_NE),
    "Top Right Ruby Piece":             JewelPieceItemData(Passage.RUBY,     Box.JEWEL_NE),
    "Top Right Topaz Piece":            JewelPieceItemData(Passage.TOPAZ,    Box.JEWEL_NE),
    "Top Right Sapphire Piece":         JewelPieceItemData(Passage.SAPPHIRE, Box.JEWEL_NE),
    "Top Right Golden Jewel Piece":     JewelPieceItemData(Passage.GOLDEN,   Box.JEWEL_NE),
    "Bottom Right Entry Jewel Piece":   JewelPieceItemData(Passage.ENTRY,    Box.JEWEL_SE),
    "Bottom Right Emerald Piece":       JewelPieceItemData(Passage.EMERALD,  Box.JEWEL_SE),
    "Bottom Right Ruby Piece":          JewelPieceItemData(Passage.RUBY,     Box.JEWEL_SE),
    "Bottom Right Topaz Piece":         JewelPieceItemData(Passage.TOPAZ,    Box.JEWEL_SE),
    "Bottom Right Sapphire Piece":      JewelPieceItemData(Passage.SAPPHIRE, Box.JEWEL_SE),
    "Bottom Right Golden Jewel Piece":  JewelPieceItemData(Passage.GOLDEN,   Box.JEWEL_SE),
    "Bottom Left Entry Jewel Piece":    JewelPieceItemData(Passage.ENTRY,    Box.JEWEL_SW),
    "Bottom Left Emerald Piece":        JewelPieceItemData(Passage.EMERALD,  Box.JEWEL_SW),
    "Bottom Left Ruby Piece":           JewelPieceItemData(Passage.RUBY,     Box.JEWEL_SW),
    "Bottom Left Topaz Piece":          JewelPieceItemData(Passage.TOPAZ,    Box.JEWEL_SW),
    "Bottom Left Sapphire Piece":       JewelPieceItemData(Passage.SAPPHIRE, Box.JEWEL_SW),
    "Bottom Left Golden Jewel Piece":   JewelPieceItemData(Passage.GOLDEN,   Box.JEWEL_SW),
    "Top Left Entry Jewel Piece":       JewelPieceItemData(Passage.ENTRY,    Box.JEWEL_NW),
    "Top Left Emerald Piece":           JewelPieceItemData(Passage.EMERALD,  Box.JEWEL_NW),
    "Top Left Ruby Piece":              JewelPieceItemData(Passage.RUBY,     Box.JEWEL_NW),
    "Top Left Topaz Piece":             JewelPieceItemData(Passage.TOPAZ,    Box.JEWEL_NW),
    "Top Left Sapphire Piece":          JewelPieceItemData(Passage.SAPPHIRE, Box.JEWEL_NW),
    "Top Left Golden Jewel Piece":      JewelPieceItemData(Passage.GOLDEN,   Box.JEWEL_NW),
}

cd_table = {
    "About that Shepherd CD":           CdItemData(Passage.EMERALD,  0),
    "Things that Never Change CD":      CdItemData(Passage.EMERALD,  1),
    "Tomorrow's Blood Pressure CD":     CdItemData(Passage.EMERALD,  2),
    "Beyond the Headrush CD":           CdItemData(Passage.EMERALD,  3),
    "Driftwood & the Island Dog CD":    CdItemData(Passage.RUBY,     0),
    "The Judge's Feet CD":              CdItemData(Passage.RUBY,     1),
    "The Moon's Lamppost CD":           CdItemData(Passage.RUBY,     2),
    "Soft Shell CD":                    CdItemData(Passage.RUBY,     3),
    "So Sleepy CD":                     CdItemData(Passage.TOPAZ,    0),
    "The Short Futon CD":               CdItemData(Passage.TOPAZ,    1),
    "Avocado Song CD":                  CdItemData(Passage.TOPAZ,    2),
    "Mr. Fly CD":                       CdItemData(Passage.TOPAZ,    3),
    "Yesterday's Words CD":             CdItemData(Passage.SAPPHIRE, 0),
    "The Errand CD":                    CdItemData(Passage.SAPPHIRE, 1),
    "You and Your Shoes CD":            CdItemData(Passage.SAPPHIRE, 2),
    "Mr. Ether & Planaria CD":          CdItemData(Passage.SAPPHIRE, 3),
}

keyzer_table = {
    "Keyzer (Entry Passage Boss)":      KeyzerItemData(Passage.ENTRY,    0),
    "Keyzer (Emerald Passage 1)":       KeyzerItemData(Passage.EMERALD,  0),
    "Keyzer (Emerald Passage 2)":       KeyzerItemData(Passage.EMERALD,  1),
    "Keyzer (Emerald Passage 3)":       KeyzerItemData(Passage.EMERALD,  2),
    "Keyzer (Emerald Passage Boss)":    KeyzerItemData(Passage.EMERALD,  3),
    "Keyzer (Ruby Passage 1)":          KeyzerItemData(Passage.RUBY,     0),
    "Keyzer (Ruby Passage 2)":          KeyzerItemData(Passage.RUBY,     1),
    "Keyzer (Ruby Passage 3)":          KeyzerItemData(Passage.RUBY,     2),
    "Keyzer (Ruby Passage Boss)":       KeyzerItemData(Passage.RUBY,     3),
    "Keyzer (Topaz Passage 1)":         KeyzerItemData(Passage.TOPAZ,    0),
    "Keyzer (Topaz Passage 2)":         KeyzerItemData(Passage.TOPAZ,    1),
    "Keyzer (Topaz Passage 3)":         KeyzerItemData(Passage.TOPAZ,    2),
    "Keyzer (Topaz Passage Boss)":      KeyzerItemData(Passage.TOPAZ,    3),
    "Keyzer (Sapphire Passage 1)":      KeyzerItemData(Passage.SAPPHIRE, 0),
    "Keyzer (Sapphire Passage 2)":      KeyzerItemData(Passage.SAPPHIRE, 1),
    "Keyzer (Sapphire Passage 3)":      KeyzerItemData(Passage.SAPPHIRE, 2),
    "Keyzer (Sapphire Passage Boss)":   KeyzerItemData(Passage.SAPPHIRE, 3),
    "Keyzer (Golden Pyramid Boss)":     KeyzerItemData(Passage.GOLDEN,   0),
}

ability_table = {
    "Progressive Ground Pound":         AbilityItemData(0),
    "Swim":                             AbilityItemData(1),
    "Head Smash":                       AbilityItemData(2),
    "Progressive Grab":                 AbilityItemData(3),
    "Dash Attack":                      AbilityItemData(4),
    "Stomp Jump":                       AbilityItemData(5),
}

golden_treasure_table = {
    "Golden Tree Pot":                  GoldenTreasureItemData( 0),
    "Golden Apple":                     GoldenTreasureItemData( 1),
    "Golden Fish":                      GoldenTreasureItemData( 2),
    "Golden Candle Holder":             GoldenTreasureItemData( 3),
    "Golden Lamp":                      GoldenTreasureItemData( 4),
    "Golden Crescent Moon Bed":         GoldenTreasureItemData( 5),
    "Golden Teddy Bear":                GoldenTreasureItemData( 6),
    "Golden Lollipop":                  GoldenTreasureItemData( 7),
    "Golden Game Boy Advance":          GoldenTreasureItemData( 8),
    "Golden Robot":                     GoldenTreasureItemData( 9),
    "Golden Rocket":                    GoldenTreasureItemData(10),
    "Golden Rocking Horse":             GoldenTreasureItemData(11),
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
