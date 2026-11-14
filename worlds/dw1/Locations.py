from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import DigimonWorldItem

class DigimonWorldLocationCategory(IntEnum):
    RECRUIT = 0
    MISC = 1
    EVENT = 2
    SKIP = 3,
    PROSPERITY = 4,
    CARD = 5,
    CHEST = 6,
    FLAG = 7,
    FIGHT = 8,
    SHOP = 9,


class DigimonWorldLocationData(NamedTuple):
    id: int
    name: str
    default_item: str
    category: DigimonWorldLocationCategory


class DigimonWorldLocation(Location):
    game: str = "Digimon World"
    category: DigimonWorldLocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: DigimonWorldLocationCategory,
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category
        self.id = id

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 69000000
        table_offset = 1000

        table_order = [
            "Misc", "Cards", "Start Game", "Prosperity",
            "File City", "Native Forest", "Drill Tunnel", "Lava Cave - Hot", "Lava Cave - Cooled",
            "Gear Savanna", "Tropical Jungle", "Ancient Dino Region",
            "Freezeland", "Great Canyon", "Ogre Fortress", "Grey Lords Mansion",
            "Underground Lab", "Factorial Town", "Misty Trees", "Toy Town",
            "Ice Sanctuary", "Mt Infinity", "Back Dimension", "Mt Panorama",
            "Secret Beach Cave", "Leomon Cave", "Beetle Land", "Nanimon",
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))
            output.update({location_data.name: location_data.id for location_data in location_tables[region_name]})
        return output

    def place_locked_item(self, item: DigimonWorldItem):
        self.item = item
        self.locked = True
        item.location = self

location_tables = {
    "Start Game": [
        DigimonWorldLocationData(69003000, "Start Game", "1000 Bits", DigimonWorldLocationCategory.RECRUIT),
    ],
    "Cards":[
        DigimonWorldLocationData(69002000, "Player Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002001, "Phoenixmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002002, "H-Kabuterimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002003, "MegaSeadramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002004, "ShogunGekomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002005, "Myotismon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002006, "MetalGreymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002007, "Mamemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002008, "Monzaemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002009, "SkullGreymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002010, "MetalMamemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002011, "Vademon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002012, "Andromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002013, "Giromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002014, "Etemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002015, "Megadramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002016, "Piximon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002017, "Digitamamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002018, "Gekomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002019, "WaruMonzaemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002020, "Jijimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002021, "King of Sukamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002022, "Cherrymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002023, "Guardromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002024, "Hagurumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002025, "Brachiomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002026, "Greymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002027, "Devimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002028, "Airdramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002029, "Tyrannomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002030, "Meramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002031, "Seadramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002032, "Kabuterimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002033, "Angemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002034, "Birdramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002035, "Garurumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002036, "Frigimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002037, "Whamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002038, "Unimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002039, "Ogremon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002040, "Shellmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002041, "Centarumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002042, "Bakemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002043, "Drimogemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002044, "Monochromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002045, "Leomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002046, "Coelamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002047, "Kokatorimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002048, "Kuwagamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002049, "Mojyamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002050, "Ninjamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002051, "Penguinmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002052, "Otamamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002053, "Tentomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002054, "Yanmamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002055, "Gotsumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002056, "Darkrizamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002057, "ToyAgumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002058, "DemiMeramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002059, "Tankmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002060, "Goburimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002061, "Numemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002062, "Vegiemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002063, "Sukamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002064, "Nanimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData(69002065, "Machinedramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
    ],
    "Prosperity":
    [
        DigimonWorldLocationData(69004000, "1 Prosperity", "1 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004001, "2 Prosperity", "2 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004002, "3 Prosperity", "3 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004003, "4 Prosperity", "4 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004004, "5 Prosperity", "5 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004005, "6 Prosperity", "6 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004006, "7 Prosperity", "7 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004007, "8 Prosperity", "8 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004008, "9 Prosperity", "9 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004009, "10 Prosperity", "10 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004010, "11 Prosperity", "11 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004011, "12 Prosperity", "12 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004012, "13 Prosperity", "13 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004013, "14 Prosperity", "14 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004014, "15 Prosperity", "15 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004015, "16 Prosperity", "16 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004016, "17 Prosperity", "17 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004017, "18 Prosperity", "18 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004018, "19 Prosperity", "19 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004019, "20 Prosperity", "20 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004020, "21 Prosperity", "21 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004021, "22 Prosperity", "22 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004022, "23 Prosperity", "23 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004023, "24 Prosperity", "24 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004024, "25 Prosperity", "25 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004025, "26 Prosperity", "26 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004026, "27 Prosperity", "27 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004027, "28 Prosperity", "28 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004028, "29 Prosperity", "29 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004029, "30 Prosperity", "30 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004030, "31 Prosperity", "31 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004031, "32 Prosperity", "32 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004032, "33 Prosperity", "33 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004033, "34 Prosperity", "34 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004034, "35 Prosperity", "35 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004035, "36 Prosperity", "36 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004036, "37 Prosperity", "37 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004037, "38 Prosperity", "38 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004038, "39 Prosperity", "39 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004039, "40 Prosperity", "40 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004040, "41 Prosperity", "41 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004041, "42 Prosperity", "42 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004042, "43 Prosperity", "43 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004043, "44 Prosperity", "44 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004044, "45 Prosperity", "45 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004045, "46 Prosperity", "46 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004046, "47 Prosperity", "47 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004047, "48 Prosperity", "48 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004048, "49 Prosperity", "49 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004049, "50 Prosperity", "50 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004050, "51 Prosperity", "51 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004051, "52 Prosperity", "52 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004052, "53 Prosperity", "53 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004053, "54 Prosperity", "54 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004054, "55 Prosperity", "55 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004055, "56 Prosperity", "56 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004056, "57 Prosperity", "57 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004057, "58 Prosperity", "58 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004058, "59 Prosperity", "59 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004059, "60 Prosperity", "60 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004060, "61 Prosperity", "61 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004061, "62 Prosperity", "62 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004062, "63 Prosperity", "63 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004063, "64 Prosperity", "64 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004064, "65 Prosperity", "65 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004065, "66 Prosperity", "66 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004066, "67 Prosperity", "67 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004067, "68 Prosperity", "68 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004068, "69 Prosperity", "69 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004069, "70 Prosperity", "70 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004070, "71 Prosperity", "71 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004071, "72 Prosperity", "72 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004072, "73 Prosperity", "73 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004073, "74 Prosperity", "74 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004074, "75 Prosperity", "75 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004075, "76 Prosperity", "76 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004076, "77 Prosperity", "77 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004077, "78 Prosperity", "78 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004078, "79 Prosperity", "79 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004079, "80 Prosperity", "80 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004080, "81 Prosperity", "81 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004081, "82 Prosperity", "82 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004082, "83 Prosperity", "83 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004083, "84 Prosperity", "84 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004084, "85 Prosperity", "85 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004085, "86 Prosperity", "86 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004086, "87 Prosperity", "87 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004087, "88 Prosperity", "88 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004088, "89 Prosperity", "89 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004089, "90 Prosperity", "90 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004090, "91 Prosperity", "91 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004091, "92 Prosperity", "92 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004092, "93 Prosperity", "93 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004093, "94 Prosperity", "94 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004094, "95 Prosperity", "95 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004095, "96 Prosperity", "96 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004096, "97 Prosperity", "97 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004097, "98 Prosperity", "98 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004098, "99 Prosperity", "99 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
        DigimonWorldLocationData(69004099, "100 Prosperity", "100 Prosperity", DigimonWorldLocationCategory.PROSPERITY),
    ],
    "Misc": [
    ],
    "File City":
    [
        DigimonWorldLocationData(69007000, "Item Shop: Monochromon 1000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007001, "Item Shop: Monochromon 2000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007002, "Item Shop: Patamon 1000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007003, "Item Shop: Patamon 2000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007004, "Item Shop: Biyomon 1000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007005, "Item Shop: Biyomon 2000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007006, "Item Shop: Unimon 1000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007007, "Item Shop: Unimon 2000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007008, "Secret Item Shop: Numemon 1500 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007009, "Secret Item Shop: Numemon 3000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007010, "Secret Item Shop: Mojyamon 1500 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007011, "Secret Item Shop: Mojyamon 3000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007012, "Secret Item Shop: Mamemon 1500 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007013, "Secret Item Shop: Mamemon 3000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007014, "Secret Item Shop: Devimon 1500 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007015, "Secret Item Shop: Devimon 3000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007016, "Market: Betamon 500 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007017, "Market: Betamon 1000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007018, "Market: Coelamon 500 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007019, "Market: Coelamon 1000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69001002, "Greymon", "Greymon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69099015, "Got starting items from Tokomon", "Got starting items from Tokomon", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099016, "Will get ambushed by Greymon in File City", "Will get ambushed by Greymon in File City", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099017, "Landslide blocking path to Unimon cleared", "Landslide blocking path to Unimon cleared", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099022, "Yuramon told you about the Invisible Bridge", "Yuramon told you about the Invisible Bridge", DigimonWorldLocationCategory.FLAG),
    ],
    "Native Forest":
    [
        DigimonWorldLocationData(69006086, "Defeated Aruraumon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006074, "Defeated Dokunemon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006080, "Defeated Goburimon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006083, "Defeated ModokiBetamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006077, "Defeated RedVegiemon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006096, "Defeated Tsukaimon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001007, "Seadramon", "Seadramon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001025, "Kunemon", "Kunemon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001049, "Ninjamon", "Ninjamon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001040, "Coelamon", "Coelamon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001037, "Palmon", "Palmon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001035, "Etemon", "Etemon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69005054, "Chest: Dragon Eye Lake", "1000 Bits", DigimonWorldLocationCategory.CHEST),
    ],
    "Drill Tunnel":
    [
        DigimonWorldLocationData(69001027, "Ogremon", "Ogremon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69099021, "Lava Cave opened", "Lava Cave opened", DigimonWorldLocationCategory.FLAG),
    ],
    "Lava Cave - Hot":
    [
        DigimonWorldLocationData(69001006, "Meramon", "Meramon", DigimonWorldLocationCategory.RECRUIT),
    ],
    "Lava Cave - Cooled":
    [
        DigimonWorldLocationData(69001031, "Drimogemon", "Drimogemon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69005026, "Chest: Lava Cave Lower", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005008, "Chest: Lava Cave Hidden 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005009, "Chest: Lava Cave Hidden 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005043, "Chest: Post-Meramon South", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005044, "Chest: Post-Meramon North", "1000 Bits", DigimonWorldLocationCategory.CHEST),

        DigimonWorldLocationData(69005029, "Chest: Lava Cave Meramon", "1000 Bits", DigimonWorldLocationCategory.CHEST),

        DigimonWorldLocationData(69099023, "Back Exit for Drill Tunnel opened", "Back Exit for Drill Tunnel opened", DigimonWorldLocationCategory.FLAG),
     ],
    "Gear Savanna":
    [
        DigimonWorldLocationData(69007020, "Recycled Goods Shop: 2000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007021, "Recycled Goods Shop: 4000 Bits", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69006095, "Defeated Akatorimon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006113, "Defeated Meteormon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006079, "Defeated NiseDrimogemon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006082, "Defeated Psychemon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006106, "Defeated Saberdramon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006097, "Defeated Sharmamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006075, "Defeated ShimaUnimon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001010, "Mamemon", "Mamemon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001039, "Leomon", "Leomon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001036, "Biyomon", "Biyomon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001024, "Patamon", "Patamon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001013, "Elecmon", "Elecmon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001032, "Sukamon", "Sukamon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69099010, "Unlocked Old Fishrod", "Unlocked Old Fishrod", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099032, "Path to Volume Villa has been opened", "Path to Volume Villa has been opened", DigimonWorldLocationCategory.FLAG),
    ],
    "Tropical Jungle":
    [
        DigimonWorldLocationData(69007022, "Merit Shop: 15 Merit", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007023, "Merit Shop: 40 Merit", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007024, "Merit Shop: 100 Merit", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007025, "Merit Shop: 250 Merit", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69007026, "Merit Shop: 500 Merit", "1000 Bits", DigimonWorldLocationCategory.SHOP),
        DigimonWorldLocationData(69006110, "Defeated Gekomon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006078, "Defeated J-Mojyamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006093, "Defeated Muchomon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006109, "Defeated Otamamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006067, "Defeated Yanmamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001001, "Betamon", "Betamon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001046, "Piximon", "Piximon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001029, "Centarumon", "Centarumon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001020, "Vegiemon", "Vegiemon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69001030, "Bakemon", "Bakemon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69005042, "Chest: Tropical Jungle Beach", "1000 Bits", DigimonWorldLocationCategory.CHEST),

        DigimonWorldLocationData(69099030, "Spotted the repaired bridge", "Spotted the repaired bridge", DigimonWorldLocationCategory.FLAG),
    ],
    "Ancient Dino Region":
    [
        DigimonWorldLocationData(69001005, "Tyrannomon", "Tyrannomon", DigimonWorldLocationCategory.RECRUIT),
    ],
    "Freezeland":
    [
        DigimonWorldLocationData(69006072, "Defeated Hyogamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006100, "Defeated IceDevimon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006071, "Defeated SnowAgumon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006103, "Defeated SnowGoburimon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006088, "Defeated Vermilimon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001048, "Penguinmon", "Penguinmon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001043, "Mojyamon", "Mojyamon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001017, "Garurumon", "Garurumon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001018, "Frigimon", "Frigimon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001019, "Whamon", "Whamon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69099001, "Mojyamon #1, Digimushrm traded", "Mojyamon #1, Digimushrm traded", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099002, "Mojyamon #1, Supercarrot traded", "Mojyamon #1, Supercarrot traded", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099003, "Mojyamon #1, Happymushrm traded", "Mojyamon #1, Happymushrm traded", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099004, "Mojyamon #2, Giant Meat traded", "Mojyamon #2, Giant Meat traded", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099005, "Mojyamon #2, Black trout traded", "Mojyamon #2, Black trout traded", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099006, "Mojyamon #2, Hispeed disk traded", "Mojyamon #2, Hispeed disk traded", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099007, "Mojyamon #3, Omnipotent traded", "Mojyamon #3, Omnipotent traded", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099008, "Mojyamon #3, med.recovery traded", "Mojyamon #3, med.recovery traded", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099009, "Mojyamon #3, Digianchovy traded", "Mojyamon #3, Digianchovy traded", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099018, "Mojyamon #1 despawned", "Mojyamon #1 despawned", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099019, "Mojyamon #2 despawned", "Mojyamon #2 despawned", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099020, "Mojyamon #3 despawned", "Mojyamon #3 despawned", DigimonWorldLocationCategory.FLAG),
    ],
    "Great Canyon":
    [
        DigimonWorldLocationData(69006101, "Defeated Darkrizamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006105, "Defeated Gururumon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006102, "Defeated SandYanmamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006107, "Defeated Soulmon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006099, "Defeated Weedmon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001038, "Monochromon", "Monochromon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001016, "Birdramon", "Birdramon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69005016, "Chest: Great Canyon Bridge", "1000 Bits", DigimonWorldLocationCategory.CHEST),

        DigimonWorldLocationData(69099031, "Defeated Ogremon #1", "Defeated Ogremon #1", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099027, "Shellmon's island is elevated", "Shellmon's island is elevated", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099028, "Shellmon's island is down again", "Shellmon's island is down again", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099029, "Talked with Shellmon about the elevator problem", "Talked with Shellmon about the elevator problem", DigimonWorldLocationCategory.FLAG),
    ],
    "Ogre Fortress":
    [
        DigimonWorldLocationData(69001028, "Shellmon", "Shellmon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69005019, "Chest: Ogre Fortress Entrance", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005020, "Chest: Ogre Fortress Hall", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005021, "Chest: Ogre Fortress Living Room", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005023, "Chest: Ogre Fortress Storage 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005024, "Chest: Ogre Fortress Storage 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005025, "Chest: Ogre Fortress Storage 3", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005033, "Chest: Ogre Fortress Storage 4", "1000 Bits", DigimonWorldLocationCategory.CHEST),

        DigimonWorldLocationData(69099026, "Beat Ogremon #2", "Beat Ogremon #2", DigimonWorldLocationCategory.FLAG),
    ],
    "Grey Lords Mansion":
    [
        DigimonWorldLocationData(69006108, "Defeated Rockmon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69005000, "Chest: Mansion Attic 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005001, "Chest: Mansion Attic 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005002, "Chest: Mansion Attic 3", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005003, "Chest: Mansion Kitchen", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005004, "Chest: Mansion Brain Room 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005005, "Chest: Mansion Brain Room 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005006, "Chest: Mansion Office", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005048, "Chest: Mansion East Wing 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005049, "Chest: Mansion East Wing 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005050, "Chest: Mansion East Wing 3", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005051, "Chest: Mansion East Wing 4", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005052, "Chest: Mansion Hallway 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005053, "Chest: Mansion Hallway 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
    ],
    "Underground Lab":
    [
        DigimonWorldLocationData(69001021, "SkullGreymon", "SkullGreymon", DigimonWorldLocationCategory.RECRUIT),
    ],
    "Factorial Town":
    [
        DigimonWorldLocationData(69006087, "Defeated Geremon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006092, "Defeated Guardromon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006073, "Defeated PlatinumSukamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001008, "Numemon", "Numemon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001022, "MetalMamemon", "MetalMamemon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001033, "Andromon", "Andromon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001034, "Giromon", "Giromon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69005062, "Chest: Factorial Town Guardromon 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005063, "Chest: Factorial Town Guardromon 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005064, "Chest: Factorial Town Guardromon 3", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005027, "Chest: Factorial Town 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005028, "Chest: Factorial Town 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),

        DigimonWorldLocationData(69099033, "Factorial Town (Savanna) entrance opened", "Factorial Town (Savanna) entrance opened", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099034, "Factorial Town entrance open", "Factorial Town entrance open", DigimonWorldLocationCategory.FLAG),
    ],
    "Misty Trees":
    [
        DigimonWorldLocationData(69006089, "Defeated Fugamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006091, "Defeated MoriShellmon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001012, "Gabumon", "Gabumon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001041, "Kokatorimon", "Kokatorimon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69099011, "Unlocked Amazing Rod", "Unlocked Amazing Rod", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099024, "Misty Trees fog removed", "Misty Trees fog removed", DigimonWorldLocationCategory.FLAG),
    ],
    "Toy Town":
    [
        DigimonWorldLocationData(69006098, "Defeated ClearAgumon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006076, "Defeated Tankmon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006084, "Defeated ToyAgumon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001011, "Monzaemon", "Monzaemon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69005018, "Chest: Toy Mansion 4F", "1000 Bits", DigimonWorldLocationCategory.CHEST),

        DigimonWorldLocationData(69099035, "Toy Mansion unlocked", "Toy Mansion unlocked", DigimonWorldLocationCategory.FLAG),
    ],
    "Ice Sanctuary":
    [
        DigimonWorldLocationData(69006104, "Defeated BlueMeramon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006094, "Defeated Icemon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001015, "Angemon", "Angemon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69005007, "Chest: Ice Sanctuary B1 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005010, "Chest: Ice Sanctuary Blue Room 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005011, "Chest: Ice Sanctuary Blue Room 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005012, "Chest: Ice Sanctuary Teleporter 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005013, "Chest: Ice Sanctuary Teleporter 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005014, "Chest: Ice Sanctuary B1 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005015, "Chest: Ice Sanctuary 4-Way", "1000 Bits", DigimonWorldLocationCategory.CHEST),
    ],
    "Mt Infinity":
    [
        DigimonWorldLocationData(69006085, "Defeated Piddomon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001045, "Megadramon", "Megadramon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001047, "Digitamamon", "Digitamamon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001003, "Devimon", "Devimon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001004, "Airdramon", "Airdramon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001009, "MetalGreymon", "MetalGreymon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69005030, "Chest: Mt. Infinity 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005031, "Chest: Mt. Infinity 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005032, "Chest: Mt. Infinity 3", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005034, "Chest: Mt. Infinity 4", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005035, "Chest: Mt. Infinity 5", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005036, "Chest: Mt. Infinity 6", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005037, "Chest: Mt. Infinity 7", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005038, "Chest: Mt. Infinity 8", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005039, "Chest: Mt. Infinity 9", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005040, "Chest: Mt. Infinity 10a", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005041, "Chest: Mt. Infinity 10b", "1000 Bits", DigimonWorldLocationCategory.CHEST),
    ],
    "Back Dimension":
    [
        DigimonWorldLocationData(69005055, "Chest: Back Dimension 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005056, "Chest: Back Dimension 2a", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005057, "Chest: Back Dimension 2b", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005058, "Chest: Back Dimension 2c", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005059, "Chest: Back Dimension 2d", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005060, "Chest: Back Dimension 3a", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005061, "Chest: Back Dimension 3b", "1000 Bits", DigimonWorldLocationCategory.CHEST),
    ],
    "Mt Panorama":
    [
        DigimonWorldLocationData(69006069, "Defeated Flarerizamon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006068, "Defeated Gotsumon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69006081, "Defeated MudFrigimon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001023, "Vademon", "Vademon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001026, "Unimon", "Unimon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69005045, "Chest: Mt. Panorama 1", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005046, "Chest: Mt. Panorama 2", "1000 Bits", DigimonWorldLocationCategory.CHEST),
        DigimonWorldLocationData(69005047, "Chest: Mt. Panorama 3", "1000 Bits", DigimonWorldLocationCategory.CHEST),
    ],
    "Secret Beach Cave":
    [
        DigimonWorldLocationData(69005022, "Chest: Secret Beach Cave", "1000 Bits", DigimonWorldLocationCategory.CHEST),

        DigimonWorldLocationData(69099025, "Beaten Ogremon #3", "Beaten Ogremon #3", DigimonWorldLocationCategory.FLAG),
    ],
    "Leomon Cave":
    [
        DigimonWorldLocationData(69005017, "Chest: Leomon's Cave", "1000 Bits", DigimonWorldLocationCategory.CHEST),
    ],
    "Beetle Land":
    [
        DigimonWorldLocationData(69006111, "Defeated Tentomon", "1000 Bits", DigimonWorldLocationCategory.FIGHT),
        DigimonWorldLocationData(69001014, "Kabuterimon", "Kabuterimon", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData(69001042, "Kuwagamon", "Kuwagamon", DigimonWorldLocationCategory.RECRUIT),
    ],
    "Nanimon":
    [
        DigimonWorldLocationData(69001044, "Nanimon", "Nanimon", DigimonWorldLocationCategory.RECRUIT),

        DigimonWorldLocationData(69099012, "Unlocked Inventory Addon #1", "Unlocked Inventory Addon #1", DigimonWorldLocationCategory.FLAG),
        DigimonWorldLocationData(69099013, "Unlocked Inventory Addon #2", "Unlocked Inventory Addon #2", DigimonWorldLocationCategory.FLAG),
    ],
}
location_dictionary: Dict[str, DigimonWorldLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
