from dataclasses import dataclass
from typing import List

from .enums import DLC


@dataclass
class RegionData:
    name: str
    """The Archipelago name for this region."""

    connections: List[str]
    """The names of regions that become accessible when entering this region."""

    dlc: DLC = None
    """The DLC this region belongs to."""


region_list: List[RegionData] = [
    RegionData("Menu", ["Things Betwixt"]),

    RegionData("Things Betwixt", ["Majula"]),

    RegionData("Majula", [
        "Forest of Fallen Giants",
        "Heide's Tower of Flame",
        "Huntsman's Copse",
        "The Pit",
        "Shaded Woods"
    ]),

    RegionData("Forest of Fallen Giants", [
        "Forest of Fallen Giants - Salamander Pit",
        "Forest of Fallen Giants - Soldier Key",
        "Memory of Vammar"
    ]),
    RegionData("Forest of Fallen Giants - Salamander Pit", []),
    RegionData("Forest of Fallen Giants - Soldier Key", [
        "The Lost Bastille - FOFG",
        "Memory of Orro",
        "Memory of Jeigh"
    ]),

    RegionData("Heide's Tower of Flame", [
        "Cathedral of Blue",
        "No-man's Wharf"
    ]),

    RegionData("Cathedral of Blue", []),

    RegionData("No-man's Wharf", ["The Lost Bastille - Wharf"]),

    RegionData("The Lost Bastille - Wharf", [
        "The Lost Bastille - Early",
        "The Lost Bastille - After Key"
    ]),
    RegionData("The Lost Bastille - FOFG", ["The Lost Bastille - Early"]),
    RegionData("The Lost Bastille - Early", ["The Lost Bastille - After Statue"]),
    RegionData("The Lost Bastille - After Statue", [
        "Belfry Luna",
        "The Lost Bastille - After Key",
        "The Lost Bastille - Late"
    ]),
    RegionData("The Lost Bastille - After Key", [
        "The Lost Bastille - Late"
    ]),
    RegionData("The Lost Bastille - Late", [
        "Sinners' Rise"
    ]),

    RegionData("Belfry Luna", []),
    RegionData("Sinners' Rise", []),

    RegionData("Huntsman's Copse", [
        "Undead Purgatory",
        "Harvest Valley"
    ]),

    RegionData("Undead Purgatory", []),

    RegionData("Harvest Valley", ["Earthen Peak"]),

    RegionData("Earthen Peak", ["Iron Keep"]),

    RegionData("Iron Keep", [
        "Belfry Sol",
        "Brume Tower"
    ]),

    RegionData("Belfry Sol", []),

    RegionData("The Pit", [
        "Grave of Saints",
        "The Gutter"
    ]),

    RegionData("Grave of Saints", []),

    RegionData("The Gutter", ["Black Gulch"]),

    RegionData("Black Gulch", ["Shulva, Sanctum City"]),

    RegionData("Shaded Woods", [
        "Doors of Pharros",
        "Drangleic Castle",
        "Aldia's Keep"
    ]),

    RegionData("Doors of Pharros", ["Brightstone Cove Tseldora"]),

    RegionData("Brightstone Cove Tseldora", []),

    RegionData("Drangleic Castle", [
        "Shrine of Amana",
        "Throne of Want",
        "Frozen Eleum Loyce"
    ]),

    RegionData("Shrine of Amana", ["Undead Crypt"]),

    RegionData("Undead Crypt", []),

    RegionData("Aldia's Keep", ["Dragon Aerie"]),

    RegionData("Dragon Aerie", ["Dragon Shrine"]),

    RegionData("Dragon Shrine", []),

    RegionData("Memory of Jeigh", []),
    RegionData("Memory of Orro", []),
    RegionData("Memory of Vammar", []),

    RegionData("Throne of Want", []),

    RegionData("Shulva, Sanctum City", [
        "Dragon's Sanctum",
        "Cave of The Dead"
    ], dlc=DLC.SUNKEN_KING),
    RegionData("Dragon's Sanctum", ["Dragon's Sanctum - Dragon Stone"], dlc=DLC.SUNKEN_KING),
    RegionData("Dragon's Sanctum - Dragon Stone", [], dlc=DLC.SUNKEN_KING),
    RegionData("Cave of The Dead", [], dlc=DLC.SUNKEN_KING),

    RegionData("Brume Tower", ["Brume Tower - Scepter",], dlc=DLC.OLD_IRON_KING),
    RegionData("Brume Tower - Scepter", [
        "Iron Passage",
        "Memory of the Old Iron King"
    ], dlc=DLC.OLD_IRON_KING),
    RegionData("Iron Passage", [], dlc=DLC.OLD_IRON_KING),
    RegionData("Memory of the Old Iron King", [], dlc=DLC.OLD_IRON_KING),

    RegionData("Frozen Eleum Loyce", ["Frigid Outskirts"], dlc=DLC.IVORY_KING),
    RegionData("Frigid Outskirts", [], dlc=DLC.IVORY_KING),
]

region_dictionary = {region.name: region for region in region_list}
