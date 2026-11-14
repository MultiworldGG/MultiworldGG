from enum import IntEnum
from typing import NamedTuple
from BaseClasses import Item, MultiWorld
import json
import pkgutil


class DigimonWorldItemCategory(IntEnum):
    CONSUMABLE = 0,
    MISC = 1,
    EVENT = 2,
    RECRUIT = 3,
    SKIP = 4,
    DV = 5,
    FLAG = 6,
    SOUL = 7,
    BOOSTER = 8


class DigimonWorldItemData(NamedTuple):
    name: str
    dw_code: int
    category: DigimonWorldItemCategory


class DigimonWorldItem(Item):
    game: str = "Digimon World"

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 690000
        return {item_data.name: base_id + item_data.dw_code for item_data in _all_items}


key_item_names = {
    "Progressive Stat Cap"
}
key_item_categories = {
    DigimonWorldItemCategory.RECRUIT,
    DigimonWorldItemCategory.FLAG,
    DigimonWorldItemCategory.SOUL,
    DigimonWorldItemCategory.BOOSTER,
}

_all_items = [DigimonWorldItemData(row[0], row[1], row[2]) for row in [    
    ("Betamon",            1001, DigimonWorldItemCategory.RECRUIT),  
    ("Greymon",            1002, DigimonWorldItemCategory.RECRUIT),  
    ("Devimon",            1003, DigimonWorldItemCategory.RECRUIT),  
    ("Airdramon",            1004, DigimonWorldItemCategory.RECRUIT),  
    ("Tyrannomon",            1005, DigimonWorldItemCategory.RECRUIT),  
    ("Meramon",            1006, DigimonWorldItemCategory.RECRUIT),  
    ("Seadramon",            1007, DigimonWorldItemCategory.RECRUIT),  
    ("Numemon",            1008, DigimonWorldItemCategory.RECRUIT),  
    ("MetalGreymon",            1009, DigimonWorldItemCategory.RECRUIT),  
    ("Mamemon",            1010, DigimonWorldItemCategory.RECRUIT),  
    ("Monzaemon",            1011, DigimonWorldItemCategory.RECRUIT),  
    ("Gabumon",            1012, DigimonWorldItemCategory.RECRUIT),  
    ("Elecmon",            1013, DigimonWorldItemCategory.RECRUIT),  
    ("Kabuterimon",            1014, DigimonWorldItemCategory.RECRUIT),  
    ("Angemon",            1015, DigimonWorldItemCategory.RECRUIT),  
    ("Birdramon",            1016, DigimonWorldItemCategory.RECRUIT),  
    ("Garurumon",            1017, DigimonWorldItemCategory.RECRUIT),  
    ("Frigimon",            1018, DigimonWorldItemCategory.RECRUIT),  
    ("Whamon",            1019, DigimonWorldItemCategory.RECRUIT),  
    ("Vegiemon",            1020, DigimonWorldItemCategory.RECRUIT),  
    ("SkullGreymon",            1021, DigimonWorldItemCategory.RECRUIT),  
    ("MetalMamemon",            1022, DigimonWorldItemCategory.RECRUIT),  
    ("Vademon",            1023, DigimonWorldItemCategory.RECRUIT),  
    ("Patamon",            1024, DigimonWorldItemCategory.RECRUIT),  
    ("Kunemon",            1025, DigimonWorldItemCategory.RECRUIT),  
    ("Unimon",            1026, DigimonWorldItemCategory.RECRUIT),  
    ("Ogremon",            1027, DigimonWorldItemCategory.RECRUIT),  
    ("Shellmon",            1028, DigimonWorldItemCategory.RECRUIT),  
    ("Centarumon",            1029, DigimonWorldItemCategory.RECRUIT),  
    ("Bakemon",            1030, DigimonWorldItemCategory.RECRUIT),  
    ("Drimogemon",            1031, DigimonWorldItemCategory.RECRUIT),  
    ("Sukamon",            1032, DigimonWorldItemCategory.RECRUIT),  
    ("Andromon",            1033, DigimonWorldItemCategory.RECRUIT),  
    ("Giromon",            1034, DigimonWorldItemCategory.RECRUIT),  
    ("Etemon",            1035, DigimonWorldItemCategory.RECRUIT),  
    ("Biyomon",            1036, DigimonWorldItemCategory.RECRUIT),  
    ("Palmon",            1037, DigimonWorldItemCategory.RECRUIT),  
    ("Monochromon",            1038, DigimonWorldItemCategory.RECRUIT),  
    ("Leomon",            1039, DigimonWorldItemCategory.RECRUIT),  
    ("Coelamon",            1040, DigimonWorldItemCategory.RECRUIT),  
    ("Kokatorimon",            1041, DigimonWorldItemCategory.RECRUIT),  
    ("Kuwagamon",            1042, DigimonWorldItemCategory.RECRUIT),  
    ("Mojyamon",            1043, DigimonWorldItemCategory.RECRUIT),  
    ("Nanimon",            1044, DigimonWorldItemCategory.RECRUIT),  
    ("Megadramon",            1045, DigimonWorldItemCategory.RECRUIT),  
    ("Piximon",            1046, DigimonWorldItemCategory.RECRUIT),  
    ("Digitamamon",            1047, DigimonWorldItemCategory.RECRUIT),  
    ("Penguinmon",            1048, DigimonWorldItemCategory.RECRUIT),  
    ("Ninjamon",            1049, DigimonWorldItemCategory.RECRUIT),  
    # souls: one per recruit
    ("Betamon Soul",             1101, DigimonWorldItemCategory.SOUL),
    ("Greymon Soul",             1102, DigimonWorldItemCategory.SOUL),
    ("Devimon Soul",             1103, DigimonWorldItemCategory.SOUL),
    ("Airdramon Soul",           1104, DigimonWorldItemCategory.SOUL),
    ("Tyrannomon Soul",          1105, DigimonWorldItemCategory.SOUL),
    ("Meramon Soul",             1106, DigimonWorldItemCategory.SOUL),
    ("Seadramon Soul",           1107, DigimonWorldItemCategory.SOUL),
    ("Numemon Soul",             1108, DigimonWorldItemCategory.SOUL),
    ("MetalGreymon Soul",        1109, DigimonWorldItemCategory.SOUL),
    ("Mamemon Soul",             1110, DigimonWorldItemCategory.SOUL),
    ("Monzaemon Soul",           1111, DigimonWorldItemCategory.SOUL),
    ("Gabumon Soul",             1112, DigimonWorldItemCategory.SOUL),
    ("Elecmon Soul",             1113, DigimonWorldItemCategory.SOUL),
    ("Kabuterimon Soul",         1114, DigimonWorldItemCategory.SOUL),
    ("Angemon Soul",             1115, DigimonWorldItemCategory.SOUL),
    ("Birdramon Soul",           1116, DigimonWorldItemCategory.SOUL),
    ("Garurumon Soul",           1117, DigimonWorldItemCategory.SOUL),
    ("Frigimon Soul",            1118, DigimonWorldItemCategory.SOUL),
    ("Whamon Soul",              1119, DigimonWorldItemCategory.SOUL),
    ("Vegiemon Soul",            1120, DigimonWorldItemCategory.SOUL),
    ("SkullGreymon Soul",        1121, DigimonWorldItemCategory.SOUL),
    ("MetalMamemon Soul",        1122, DigimonWorldItemCategory.SOUL),
    ("Vademon Soul",             1123, DigimonWorldItemCategory.SOUL),
    ("Patamon Soul",             1124, DigimonWorldItemCategory.SOUL),
    ("Kunemon Soul",             1125, DigimonWorldItemCategory.SOUL),
    ("Unimon Soul",              1126, DigimonWorldItemCategory.SOUL),
    ("Ogremon Soul",             1127, DigimonWorldItemCategory.SOUL),
    ("Shellmon Soul",            1128, DigimonWorldItemCategory.SOUL),
    ("Centarumon Soul",          1129, DigimonWorldItemCategory.SOUL),
    ("Bakemon Soul",             1130, DigimonWorldItemCategory.SOUL),
    ("Drimogemon Soul",          1131, DigimonWorldItemCategory.SOUL),
    ("Sukamon Soul",             1132, DigimonWorldItemCategory.SOUL),
    ("Andromon Soul",            1133, DigimonWorldItemCategory.SOUL),
    ("Giromon Soul",             1134, DigimonWorldItemCategory.SOUL),
    ("Etemon Soul",              1135, DigimonWorldItemCategory.SOUL),
    ("Biyomon Soul",             1136, DigimonWorldItemCategory.SOUL),
    ("Palmon Soul",              1137, DigimonWorldItemCategory.SOUL),
    ("Monochromon Soul",         1138, DigimonWorldItemCategory.SOUL),
    ("Leomon Soul",              1139, DigimonWorldItemCategory.SOUL),
    ("Coelamon Soul",            1140, DigimonWorldItemCategory.SOUL),
    ("Kokatorimon Soul",         1141, DigimonWorldItemCategory.SOUL),
    ("Kuwagamon Soul",           1142, DigimonWorldItemCategory.SOUL),
    ("Mojyamon Soul",            1143, DigimonWorldItemCategory.SOUL),
    ("Nanimon Soul",             1144, DigimonWorldItemCategory.SOUL),
    ("Megadramon Soul",          1145, DigimonWorldItemCategory.SOUL),
    ("Piximon Soul",             1146, DigimonWorldItemCategory.SOUL),
    ("Digitamamon Soul",         1147, DigimonWorldItemCategory.SOUL),
    ("Penguinmon Soul",          1148, DigimonWorldItemCategory.SOUL),
    ("Ninjamon Soul",            1149, DigimonWorldItemCategory.SOUL),
    
    ("SM Recovery",            2000, DigimonWorldItemCategory.CONSUMABLE),
    ("Med Recovery",           2001, DigimonWorldItemCategory.CONSUMABLE),
    ("Lrg Recovery",           2002, DigimonWorldItemCategory.CONSUMABLE),
    ("Sup Recovery",           2003, DigimonWorldItemCategory.CONSUMABLE),
    ("MP Floppy",              2004, DigimonWorldItemCategory.CONSUMABLE),
    ("Medium MP",              2005, DigimonWorldItemCategory.CONSUMABLE),
    ("Large MP",               2006, DigimonWorldItemCategory.CONSUMABLE),
    ("Double flop",            2007, DigimonWorldItemCategory.CONSUMABLE),
    ("Various",                2008, DigimonWorldItemCategory.CONSUMABLE),
    ("Omnipotent",             2009, DigimonWorldItemCategory.CONSUMABLE),
    ("Protection",             2010, DigimonWorldItemCategory.CONSUMABLE),
    ("Restore",                2011, DigimonWorldItemCategory.CONSUMABLE),
    ("Sup.restore",            2012, DigimonWorldItemCategory.CONSUMABLE),
    ("Bandage",                2013, DigimonWorldItemCategory.CONSUMABLE),
    ("Medicine",               2014, DigimonWorldItemCategory.CONSUMABLE),
    ("Off. Disk",              2015, DigimonWorldItemCategory.CONSUMABLE),
    ("Def. Disk",              2016, DigimonWorldItemCategory.CONSUMABLE),
    ("Hispeed dsk",            2017, DigimonWorldItemCategory.CONSUMABLE),
    ("Omni Disk",              2018, DigimonWorldItemCategory.CONSUMABLE),
    ("S.Off.disk",             2019, DigimonWorldItemCategory.CONSUMABLE),
    ("S.Def.disk",             2020, DigimonWorldItemCategory.CONSUMABLE),
    ("S.speed.disk",           2021, DigimonWorldItemCategory.CONSUMABLE),
    ("Auto Pilot",             2022, DigimonWorldItemCategory.CONSUMABLE),
    ("Off. Chip",              2023, DigimonWorldItemCategory.CONSUMABLE),
    ("Def. Chip",              2024, DigimonWorldItemCategory.CONSUMABLE),
    ("Brain Chip",             2025, DigimonWorldItemCategory.CONSUMABLE),
    ("Quick Chip",             2026, DigimonWorldItemCategory.CONSUMABLE),
    ("HP Chip",                2027, DigimonWorldItemCategory.CONSUMABLE),
    ("MP Chip",                2028, DigimonWorldItemCategory.CONSUMABLE),
    ("DV Chip A",              2029, DigimonWorldItemCategory.CONSUMABLE),
    ("DV Chip D",              2030, DigimonWorldItemCategory.CONSUMABLE),
    ("DV Chip E",              2031, DigimonWorldItemCategory.CONSUMABLE),
    ("Port. potty",            2032, DigimonWorldItemCategory.CONSUMABLE),
    ("Trn. manual",            2033, DigimonWorldItemCategory.MISC),
    ("Rest pillow",            2034, DigimonWorldItemCategory.MISC),
    ("Enemy repel",            2035, DigimonWorldItemCategory.MISC),
    ("Enemy bell",             2036, DigimonWorldItemCategory.MISC),
    ("Health shoe",            2037, DigimonWorldItemCategory.MISC),
    ("Meat",                   2038, DigimonWorldItemCategory.CONSUMABLE),
    ("Giant Meat",             2039, DigimonWorldItemCategory.CONSUMABLE),
    ("Sirloin",                2040, DigimonWorldItemCategory.CONSUMABLE),
    ("Supercarrot",            2041, DigimonWorldItemCategory.CONSUMABLE),
    ("Hawk radish",            2042, DigimonWorldItemCategory.CONSUMABLE),
    ("Spiny green",            2043, DigimonWorldItemCategory.CONSUMABLE),
    ("Digimushrm",             2044, DigimonWorldItemCategory.CONSUMABLE),
    ("Ice mushrm",             2045, DigimonWorldItemCategory.CONSUMABLE),
    ("Deluxmushrm",            2046, DigimonWorldItemCategory.CONSUMABLE),
    ("Digipine",               2047, DigimonWorldItemCategory.CONSUMABLE),
    ("Blue apple",             2048, DigimonWorldItemCategory.CONSUMABLE),
    ("Red Berry",              2049, DigimonWorldItemCategory.CONSUMABLE),
    ("Gold Acorn",             2050, DigimonWorldItemCategory.CONSUMABLE),
    ("Big Berry",              2051, DigimonWorldItemCategory.CONSUMABLE),
    ("Sweet Nut",              2052, DigimonWorldItemCategory.CONSUMABLE),
    ("Super veggy",            2053, DigimonWorldItemCategory.CONSUMABLE),
    ("Pricklypear",            2054, DigimonWorldItemCategory.CONSUMABLE),
    ("Orange bana",            2055, DigimonWorldItemCategory.CONSUMABLE),
    ("Power fruit",            2056, DigimonWorldItemCategory.CONSUMABLE),
    ("Power Ice",              2057, DigimonWorldItemCategory.CONSUMABLE),
    ("Speed Leaf",             2058, DigimonWorldItemCategory.CONSUMABLE),
    ("Sage Fruit",             2059, DigimonWorldItemCategory.CONSUMABLE),
    ("Muscle Yam",             2060, DigimonWorldItemCategory.CONSUMABLE),
    ("Calm berry",             2061, DigimonWorldItemCategory.CONSUMABLE),
    ("Digianchovy",            2062, DigimonWorldItemCategory.CONSUMABLE),
    ("Digisnapper",            2063, DigimonWorldItemCategory.CONSUMABLE),
    ("DigiTrout",              2064, DigimonWorldItemCategory.CONSUMABLE),
    ("Black trout",            2065, DigimonWorldItemCategory.CONSUMABLE),
    ("Digicatfish",            2066, DigimonWorldItemCategory.CONSUMABLE),
    ("Digiseabass",            2067, DigimonWorldItemCategory.CONSUMABLE),
    ("Moldy Meat",             2068, DigimonWorldItemCategory.CONSUMABLE),
    ("Happymushrm",            2069, DigimonWorldItemCategory.CONSUMABLE),
    ("Chain melon",            2070, DigimonWorldItemCategory.CONSUMABLE),
    ("Grey Claws",             2071, DigimonWorldItemCategory.DV),
    ("Fireball",               2072, DigimonWorldItemCategory.DV),
    ("Flamingwing",            2073, DigimonWorldItemCategory.DV),
    ("Iron Hoof",              2074, DigimonWorldItemCategory.DV),
    ("Mono Stone",             2075, DigimonWorldItemCategory.DV),
    ("Steel drill",            2076, DigimonWorldItemCategory.DV),
    ("White Fang",             2077, DigimonWorldItemCategory.DV),
    ("Black Wing",             2078, DigimonWorldItemCategory.DV),
    ("Spike Club",             2079, DigimonWorldItemCategory.DV),
    ("Flamingmane",            2080, DigimonWorldItemCategory.DV),
    ("White Wing",             2081, DigimonWorldItemCategory.DV),
    ("Torn tatter",            2082, DigimonWorldItemCategory.DV),
    ("Electo ring",            2083, DigimonWorldItemCategory.DV),
    ("Rainbowhorn",            2084, DigimonWorldItemCategory.DV),
    ("Rooster",                2085, DigimonWorldItemCategory.DV),
    ("Unihorn",                2086, DigimonWorldItemCategory.DV),
    ("Horn helmet",            2087, DigimonWorldItemCategory.DV),
    ("Scissor jaw",            2088, DigimonWorldItemCategory.DV),
    ("Fertilizer",             2089, DigimonWorldItemCategory.DV),
    ("Koga laws",              2090, DigimonWorldItemCategory.DV),
    ("Waterbottle",            2091, DigimonWorldItemCategory.DV),
    ("North Star",             2092, DigimonWorldItemCategory.DV),
    ("Red Shell",              2093, DigimonWorldItemCategory.DV),
    ("Hard Scale",             2094, DigimonWorldItemCategory.DV),
    ("Bluecrystal",            2095, DigimonWorldItemCategory.DV),
    ("Ice crystal",            2096, DigimonWorldItemCategory.DV),
    ("Hair grower",            2097, DigimonWorldItemCategory.DV),
    ("Sunglasses",             2098, DigimonWorldItemCategory.DV),
    ("Metal part",             2099, DigimonWorldItemCategory.DV),
    ("Fatal Bone",             2100, DigimonWorldItemCategory.DV),
    ("Cyber part",             2101, DigimonWorldItemCategory.DV),
    ("Mega Hand",              2102, DigimonWorldItemCategory.DV),
    ("Silver ball",            2103, DigimonWorldItemCategory.DV),
    ("Metal armor",            2104, DigimonWorldItemCategory.DV),
    ("Chainsaw",               2105, DigimonWorldItemCategory.DV),
    ("Small spear",            2106, DigimonWorldItemCategory.DV),
    ("X Bandage",              2107, DigimonWorldItemCategory.DV),
    ("Ray Gun",                2108, DigimonWorldItemCategory.DV),
    ("Gold banana",            2109, DigimonWorldItemCategory.DV),
    ("Mysty Egg",              2110, DigimonWorldItemCategory.DV),
    ("Red Ruby",               2111, DigimonWorldItemCategory.DV),
    ("Beetlepearl",            2112, DigimonWorldItemCategory.DV),
    ("Coral charm",            2113, DigimonWorldItemCategory.DV),
    ("Moon mirror",            2114, DigimonWorldItemCategory.DV),
    ("Blue Flute",             2115, DigimonWorldItemCategory.MISC),
    ("old fishrod",            2116, DigimonWorldItemCategory.MISC),
    ("Amazing rod",            2117, DigimonWorldItemCategory.MISC),
    ("Leomonstone",            2118, DigimonWorldItemCategory.MISC),
    ("Mansion key",            2119, DigimonWorldItemCategory.MISC),
    ("Gear",                   2120, DigimonWorldItemCategory.MISC),
    ("Rain Plant",             2121, DigimonWorldItemCategory.CONSUMABLE),
    ("Steak",                  2122, DigimonWorldItemCategory.CONSUMABLE),
    ("Frig Key",               2123, DigimonWorldItemCategory.MISC),
    ("AS Decoder",             2124, DigimonWorldItemCategory.MISC),
    ("Giga Hand",              2125, DigimonWorldItemCategory.DV),
    ("Noble Mane",             2126, DigimonWorldItemCategory.DV),
    ("Metalbanana",            2127, DigimonWorldItemCategory.DV),  
    
    ("Progressive Stat Cap",            3000, DigimonWorldItemCategory.MISC),
    ("1000 Bits",            3001, DigimonWorldItemCategory.MISC),
    ("5000 Bits",            3002, DigimonWorldItemCategory.MISC),

    ("1 Prosperity",         4000, DigimonWorldItemCategory.EVENT),
    ("2 Prosperity",         4001, DigimonWorldItemCategory.EVENT),
    ("3 Prosperity",         4002, DigimonWorldItemCategory.EVENT),
    ("4 Prosperity",         4003, DigimonWorldItemCategory.EVENT),
    ("5 Prosperity",         4004, DigimonWorldItemCategory.EVENT),
    ("6 Prosperity",         4005, DigimonWorldItemCategory.EVENT),
    ("7 Prosperity",         4006, DigimonWorldItemCategory.EVENT),
    ("8 Prosperity",         4007, DigimonWorldItemCategory.EVENT),
    ("9 Prosperity",         4008, DigimonWorldItemCategory.EVENT),
    ("10 Prosperity",        4009, DigimonWorldItemCategory.EVENT),
    ("11 Prosperity",        4010, DigimonWorldItemCategory.EVENT),
    ("12 Prosperity",        4011, DigimonWorldItemCategory.EVENT),
    ("13 Prosperity",        4012, DigimonWorldItemCategory.EVENT),
    ("14 Prosperity",        4013, DigimonWorldItemCategory.EVENT),
    ("15 Prosperity",        4014, DigimonWorldItemCategory.EVENT),
    ("16 Prosperity",        4015, DigimonWorldItemCategory.EVENT),
    ("17 Prosperity",        4016, DigimonWorldItemCategory.EVENT),
    ("18 Prosperity",        4017, DigimonWorldItemCategory.EVENT),
    ("19 Prosperity",        4018, DigimonWorldItemCategory.EVENT),
    ("20 Prosperity",        4019, DigimonWorldItemCategory.EVENT),
    ("21 Prosperity",        4020, DigimonWorldItemCategory.EVENT),
    ("22 Prosperity",        4021, DigimonWorldItemCategory.EVENT),
    ("23 Prosperity",        4022, DigimonWorldItemCategory.EVENT),
    ("24 Prosperity",        4023, DigimonWorldItemCategory.EVENT),
    ("25 Prosperity",        4024, DigimonWorldItemCategory.EVENT),
    ("26 Prosperity",        4025, DigimonWorldItemCategory.EVENT),
    ("27 Prosperity",        4026, DigimonWorldItemCategory.EVENT),
    ("28 Prosperity",        4027, DigimonWorldItemCategory.EVENT),
    ("29 Prosperity",        4028, DigimonWorldItemCategory.EVENT),
    ("30 Prosperity",        4029, DigimonWorldItemCategory.EVENT),
    ("31 Prosperity",        4030, DigimonWorldItemCategory.EVENT),
    ("32 Prosperity",        4031, DigimonWorldItemCategory.EVENT),
    ("33 Prosperity",        4032, DigimonWorldItemCategory.EVENT),
    ("34 Prosperity",        4033, DigimonWorldItemCategory.EVENT),
    ("35 Prosperity",        4034, DigimonWorldItemCategory.EVENT),
    ("36 Prosperity",        4035, DigimonWorldItemCategory.EVENT),
    ("37 Prosperity",        4036, DigimonWorldItemCategory.EVENT),
    ("38 Prosperity",        4037, DigimonWorldItemCategory.EVENT),
    ("39 Prosperity",        4038, DigimonWorldItemCategory.EVENT),
    ("40 Prosperity",        4039, DigimonWorldItemCategory.EVENT),
    ("41 Prosperity",        4040, DigimonWorldItemCategory.EVENT),
    ("42 Prosperity",        4041, DigimonWorldItemCategory.EVENT),
    ("43 Prosperity",        4042, DigimonWorldItemCategory.EVENT),
    ("44 Prosperity",        4043, DigimonWorldItemCategory.EVENT),
    ("45 Prosperity",        4044, DigimonWorldItemCategory.EVENT),
    ("46 Prosperity",        4045, DigimonWorldItemCategory.EVENT),
    ("47 Prosperity",        4046, DigimonWorldItemCategory.EVENT),
    ("48 Prosperity",        4047, DigimonWorldItemCategory.EVENT),
    ("49 Prosperity",        4048, DigimonWorldItemCategory.EVENT),
    ("50 Prosperity",        4049, DigimonWorldItemCategory.EVENT),
    ("51 Prosperity",        4050, DigimonWorldItemCategory.EVENT),
    ("52 Prosperity",        4051, DigimonWorldItemCategory.EVENT),
    ("53 Prosperity",        4052, DigimonWorldItemCategory.EVENT),
    ("54 Prosperity",        4053, DigimonWorldItemCategory.EVENT),
    ("55 Prosperity",        4054, DigimonWorldItemCategory.EVENT),
    ("56 Prosperity",        4055, DigimonWorldItemCategory.EVENT),
    ("57 Prosperity",        4056, DigimonWorldItemCategory.EVENT),
    ("58 Prosperity",        4057, DigimonWorldItemCategory.EVENT),
    ("59 Prosperity",        4058, DigimonWorldItemCategory.EVENT),
    ("60 Prosperity",        4059, DigimonWorldItemCategory.EVENT),
    ("61 Prosperity",        4060, DigimonWorldItemCategory.EVENT),
    ("62 Prosperity",        4061, DigimonWorldItemCategory.EVENT),
    ("63 Prosperity",        4062, DigimonWorldItemCategory.EVENT),
    ("64 Prosperity",        4063, DigimonWorldItemCategory.EVENT),
    ("65 Prosperity",        4064, DigimonWorldItemCategory.EVENT),
    ("66 Prosperity",        4065, DigimonWorldItemCategory.EVENT),
    ("67 Prosperity",        4066, DigimonWorldItemCategory.EVENT),
    ("68 Prosperity",        4067, DigimonWorldItemCategory.EVENT),
    ("69 Prosperity",        4068, DigimonWorldItemCategory.EVENT),
    ("70 Prosperity",        4069, DigimonWorldItemCategory.EVENT),
    ("71 Prosperity",        4070, DigimonWorldItemCategory.EVENT),
    ("72 Prosperity",        4071, DigimonWorldItemCategory.EVENT),
    ("73 Prosperity",        4072, DigimonWorldItemCategory.EVENT),
    ("74 Prosperity",        4073, DigimonWorldItemCategory.EVENT),
    ("75 Prosperity",        4074, DigimonWorldItemCategory.EVENT),
    ("76 Prosperity",        4075, DigimonWorldItemCategory.EVENT),
    ("77 Prosperity",        4076, DigimonWorldItemCategory.EVENT),
    ("78 Prosperity",        4077, DigimonWorldItemCategory.EVENT),
    ("79 Prosperity",        4078, DigimonWorldItemCategory.EVENT),
    ("80 Prosperity",        4079, DigimonWorldItemCategory.EVENT),
    ("81 Prosperity",        4080, DigimonWorldItemCategory.EVENT),
    ("82 Prosperity",        4081, DigimonWorldItemCategory.EVENT),
    ("83 Prosperity",        4082, DigimonWorldItemCategory.EVENT),
    ("84 Prosperity",        4083, DigimonWorldItemCategory.EVENT),
    ("85 Prosperity",        4084, DigimonWorldItemCategory.EVENT),
    ("86 Prosperity",        4085, DigimonWorldItemCategory.EVENT),
    ("87 Prosperity",        4086, DigimonWorldItemCategory.EVENT),
    ("88 Prosperity",        4087, DigimonWorldItemCategory.EVENT),
    ("89 Prosperity",        4088, DigimonWorldItemCategory.EVENT),
    ("90 Prosperity",        4089, DigimonWorldItemCategory.EVENT),
    ("91 Prosperity",        4090, DigimonWorldItemCategory.EVENT),
    ("92 Prosperity",        4091, DigimonWorldItemCategory.EVENT),
    ("93 Prosperity",        4092, DigimonWorldItemCategory.EVENT),
    ("94 Prosperity",        4093, DigimonWorldItemCategory.EVENT),
    ("95 Prosperity",        4094, DigimonWorldItemCategory.EVENT),
    ("96 Prosperity",        4095, DigimonWorldItemCategory.EVENT),
    ("97 Prosperity",        4096, DigimonWorldItemCategory.EVENT),
    ("98 Prosperity",        4097, DigimonWorldItemCategory.EVENT),
    ("99 Prosperity",        4098, DigimonWorldItemCategory.EVENT),
    ("100 Prosperity",       4099, DigimonWorldItemCategory.EVENT),


    ("Mojyamon #1, Digimushrm traded",                 5001, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #1, Supercarrot traded",                5002, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #1, Happymushrm traded",                5003, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #2, Giant Meat traded",                 5004, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #2, Black trout traded",                5005, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #2, Hispeed disk traded",               5006, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #3, Omnipotent traded",                 5007, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #3, med.recovery traded",               5008, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #3, Digianchovy traded",                5009, DigimonWorldItemCategory.FLAG),
    ("Unlocked Old Fishrod",                           5010, DigimonWorldItemCategory.FLAG),
    ("Unlocked Amazing Rod",                           5011, DigimonWorldItemCategory.FLAG),
    ("Unlocked Inventory Addon #1",                    5012, DigimonWorldItemCategory.FLAG),
    ("Unlocked Inventory Addon #2",                    5013, DigimonWorldItemCategory.FLAG),
    ("Got starting items from Tokomon",                5015, DigimonWorldItemCategory.FLAG),
    ("Will get ambushed by Greymon in File City",      5016, DigimonWorldItemCategory.FLAG),
    ("Landslide blocking path to Unimon cleared",      5017, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #1 despawned",                          5018, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #2 despawned",                          5019, DigimonWorldItemCategory.FLAG),
    ("Mojyamon #3 despawned",                          5020, DigimonWorldItemCategory.FLAG),
    ("Lava Cave opened",                               5021, DigimonWorldItemCategory.FLAG),
    ("Yuramon told you about the Invisible Bridge",    5022, DigimonWorldItemCategory.FLAG),
    ("Back Exit for Drill Tunnel opened",              5023, DigimonWorldItemCategory.FLAG),
    ("Misty Trees fog removed",                        5024, DigimonWorldItemCategory.FLAG),
    ("Beaten Ogremon #3",                              5025, DigimonWorldItemCategory.FLAG),
    ("Beat Ogremon #2",                                5026, DigimonWorldItemCategory.FLAG),
    ("Shellmon's island is elevated",                  5027, DigimonWorldItemCategory.FLAG),
    ("Shellmon's island is down again",                5028, DigimonWorldItemCategory.FLAG),
    ("Talked with Shellmon about the elevator problem", 5029, DigimonWorldItemCategory.FLAG),
    ("Spotted the repaired bridge",                    5030, DigimonWorldItemCategory.FLAG),
    ("Defeated Ogremon #1",                            5031, DigimonWorldItemCategory.FLAG),
    ("Path to Volume Villa has been opened",           5032, DigimonWorldItemCategory.FLAG),
    ("Factorial Town (Savanna) entrance opened",       5033, DigimonWorldItemCategory.FLAG),
    ("Factorial Town entrance open",                   5034, DigimonWorldItemCategory.FLAG),
    ("Toy Mansion unlocked",                           5035, DigimonWorldItemCategory.FLAG),
]]

# booster packs from data/booster_packs.json; booster_pack_cards maps item name -> card ids
BOOSTER_CODE_BASE = 3003
_booster_cfg = json.loads(pkgutil.get_data(__name__, "data/booster_packs.json").decode("utf-8"))
booster_pack_cards = {}
for _p in _booster_cfg["packs"]:
    if _p.get("random"):
        continue
    _name = f"{_p['name']} Booster Pack"
    _all_items.append(DigimonWorldItemData(_name, BOOSTER_CODE_BASE + int(_p["flag"]), DigimonWorldItemCategory.BOOSTER))
    booster_pack_cards[_name] = {_booster_cfg["card_ids"][c] for t in _p["tiers"] for c in t["cards"]}

item_descriptions = {
}

item_dictionary = {item_data.name: item_data for item_data in _all_items}


def BuildItemPool(world: MultiWorld, count, options):
    item_pool = []
    remaining_count = count
    if(options.progressive_stats.value):
        if(options.early_statcap.value):
            remaining_count = remaining_count - 8
        else:
            remaining_count = remaining_count - 9
    consumable_count = round(remaining_count * 0.6)
    remaining_count = remaining_count - consumable_count
    dv_count = round(remaining_count * 0.8)
    remaining_count = remaining_count - dv_count
    bit_count = remaining_count
    
    if options.guaranteed_items.value:
        for item_name in options.guaranteed_items.value:
            item = item_dictionary[item_name]
            item_pool.append(item)
            bit_count -= 1
    if(options.progressive_stats.value):
        # add 9 stat cap items to the pool
        if(options.early_statcap.value):            
            for i in range(8):
                item_pool.append(item_dictionary["Progressive Stat Cap"])
        else: 
            for i in range(9):
                item_pool.append(item_dictionary["Progressive Stat Cap"])
    for i in range(consumable_count):
        consumables = [item for item in _all_items if item.category == DigimonWorldItemCategory.CONSUMABLE]
        item = world.random.choice(consumables)
        item_pool.append(item)
    for i in range(dv_count):
        dv = [item for item in _all_items if item.category == DigimonWorldItemCategory.DV]
        item = world.random.choice(dv)
        item_pool.append(item)
    for i in range(bit_count):    
        bit = [item for item in _all_items if "Bits" in item.name]
        item = world.random.choice(bit)
        item_pool.append(item)    
    world.random.shuffle(item_pool)
    return item_pool