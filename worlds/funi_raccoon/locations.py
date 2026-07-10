from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items

if TYPE_CHECKING:
    from .world import FuniRaccoonWorld

LOCATION_NAME_TO_ID = {
    "Store Moai": 1001,
    "Store Street Lamp": 1002,
    "Store Dumbbell": 1003,
    "Store Lama/Alpaca Maybe?": 1004,
    "Store Gym": 1005,
    "Store Vending Machine (accepts doubloons)": 1007,
    "Store DOUBLOONS": 1008,
    "Store Radio": 1009,
    "Store unregistered firearm": 1011,
    "Store Under Construction": 1016,
    "Store Chicken": 1017,
    "Store Washing Machine": 1018,
    "Store Michelle Cat": 1019,
    "Store Brob Energy": 1020,
    "Store Buisness Man": 1021,
    "Store Concrete Cat": 1022,
    "Store Gizmo Cat": 1023,
    "Store Keksz Cat": 1024,
    "Store Michi Cat": 1025,
    "Store boingler Cat": 1026,
    "Store Paracetamol 650mg": 1027,
    "Store Heavy Stone Torch": 1028,
    "Store Computer Monitor (60hz)": 1031,
    "Store Sign": 1037,
    "Store Crack Head": 1038,
    "Store Crayon": 1039,
    "Store Cricket Bat": 1040,
    "Store Pirate": 1042,
    "Store Pirate 2": 1043,
    "Store Pirate 3": 1044,
    "Store ROAD NOT DONE": 1045,
    "Store Microwave": 1048,
    "Store Toaster": 1049,
    "Store Logan/Real Knight Left": 1050,
    "Store Logan/Real Knight Right": 1051,
    "Store Evil Fish": 1052,
    "Store Feral Dog": 1053,
    "Store Windmill": 1054,
    "Store Marketable Plushie Box": 1055,
    "Store Goo": 1056,
    "Store Beenie the Birthday Boy": 1057,
    "Store Fan": 1059,
    "Store Letter B": 1061,
    "Store Beenie, Our Savior": 1062,
    "Store Candle": 1063,
    "Store Funi Marketable Plushie": 1064,
    "Store Patrick O'Hara": 1065,
    "Store Toastie": 1066,
    "Store Crisp": 1067,
    "Store Beautiful Flower": 1068,
    "Store Divider": 1069,
    "Store Office Chair": 1070,
    "Store Desk": 1071,
    "Store My Favourite Chair": 1073,
    "Store Cricket": 1074,
    "Store Crisps Undying Love": 1075,
    "Store Blimbo Village Sign": 1076,
    "Store Ougham Stone": 1077,
    'Store "Cow"': 1078,
    "Store Old Ass Rusty Ass Key": 1080,
    "Store Plimbo": 1081,
    "Store Fridge Key": 1082,
    "Store Orphan Tyre": 1084,
    "Store Papa Tyre": 1085,
    "Store Smoker": 1086,
    "Store Broken Truck": 1087,
    "Store CHEESE": 1088,
    "Store Gas Drum": 1089,
    "Store Coffee Shop (closed)": 1090,
    "Store Trolley": 1091,
    "Store Trasco Sign": 1092,
    "Store Folding Chair": 1093,
    "Store Cooling Rod": 1094,
    "Store Warning": 1095,
    "Store Pickaxe": 1096,
    "Store Broken Wall": 1097,
    "Store Fone": 1098,
    "Store Coffee Cup": 1099,
    "Store Kettle": 1100,
    "Store Radiator": 1101,
    "Store Flower Blimbo": 1102,
    "Store Blimbo City Sign": 1103,
    "Store Bench": 1104,
    "Store Evil Raccoon": 1105,
    "Store Naked Fella": 1106,
    "Store Bin": 1107,
    "Store Friend Martin Friendship Statue": 1108,
    "Store Knifedog": 1109,
    "Store Suitcase": 1110,
    "Store Cheeky Pint": 1111,
    "Store Flowian": 1112,
    "Store Bomb": 1113,
    "Store Bell Boy": 1114,
    "Store Demon Core": 1115,
    "Store Apple": 1116,
    "Store Gas Pumpo": 1117,
    "Store CD Player": 1118,
    "Store Radio Blimbo": 1119,
    "Store Binocublo": 1120,
    "Store Police Car": 1121,
    "Store Hazelnut": 1122,
    "Store Anti Sads": 1123,
    'Store "TV Remote"': 1124,
    "Store Synthesizer": 1125,
    "Store Brick": 1126,
    "Store Lloyd": 1127,
    "Store Manhole Cover": 1128,
    "Store Old Sign": 1129,
    "Store Warning Sign": 1130,
    "Store Area Sign": 1131,
    "Store Orb": 1132,
    "Store Ms. Heel": 1134,
    "Store Mr. Heel": 1135,
    "Store Belgium Waffle": 1136,
    "Store GREENISH ABOMINATION": 1137,
    "Store Priestess": 1138,
    "Store Beenie Saves The Orphans": 1140,
    "Store Eel Can": 1141,
    "Store Barrel": 1142,
    "Store BookBlo": 1143,
    "Store Fridge": 1144,
    "Store Fridgling": 1145,
    "Store Snowball": 1146,
    "Store Leeches!": 1147,
    "Store Plimbo's Cooling Rod": 1148,
    "Store Fridge King's Cooling Rod": 1149,
    "Store Beach Ball": 1150,
    "Store Milk Klubnika": 1151,
    "Store Mikk Masive Sign": 1152,
    "Store Chairapist": 1154,
    "Store Digital Polaroid Camera": 1155,
    "Store Yolky": 1156,
    "Store Pawn": 1157,
    "Store Rook": 1158,
    "Store Bishop": 1159,
    "Store Queen": 1160,
    "Store King": 1161,
    "Store Real Gym": 1162,
    "Store Spoonsweet": 1163,
    "Store Wriks Celler": 1164,
    "Store Door": 1165,
    "Store Funi Raccoon Game Deluxe": 1166,
    "Store Patrice": 1167,
    "Store Goo Container": 1168,
    "Store Butterfly": 1169,
    "Store Patrick O Bobble": 1170,
    "Store Dice": 1171,
    "Store Lughling": 1172,
    "Store Book Stack": 1173,
    "Store Average Canadian": 1174,
    "Store Cheese Wife": 1175,
    "Store Brazil Knight": 1176,
    "Store Doggy": 1177,
    "Store Real Football": 1178,
    "Store Hintblo": 1179,
    "Store Funi Raccoon": 1180,
    
    "Get 1000 Score with Kei Truck": 2001,
    "Get 2000 Score with Kei Truck": 2002,
    "Get 3000 Score with Kei Truck": 2003,
    "Get 4000 Score with Kei Truck": 2004,
    "Get 5000 Score with Kei Truck": 2005,
    "Eat Mystical Dumbbell - Act 1": 3001,
    "Eat Mystical Dumbbell - Act 2": 3002,
    "Eat Mystical Dumbbell - Act 3": 3003,
    "Eat Mystical Dumbbell - Act 4": 3004,
    "Purchase Kei Truck Radio":   4001,
    "Purchase Kei Truck Toaster": 4002,
    "Purchase Kei Truck Boost":   4003,
    "Find Michi Cat": 5001,
    "Find Michelle Cat": 5002,
    "Find Concrete Cat": 5003,
    "Find Gizmo Cat": 5004,
    "Find Keksz Cat": 5005,
    "Find boingler Cat": 5006,
    "Find Sun Hat":          6001,
    "Find Sombrero":         6002,
    "Find Top Hat":          6003,
    "Find Jester Hat":       6004,
    "Find Raccoon Hat":      6005,
    "Find Media Player Hat": 6006,
    "Find Fridge Crown":     6007,
    "Find Patty Hat":        6008,
    "Eat Green Mystical Gem":  7001,
    "Eat Blue Mystical Gem":   7002,
    "Eat Purple Mystical Gem": 7003,
    "Eat Red Mystical Gem":    7004,
    
    # --- Euro collectibles ---
    "Norwich: Euro at train station":               8001,
    "Norwich: Euro at chicken farm island":         8002,
    "Chicken Farm: Euro on pillar":                 8003,
    "Gym: Euro on roof with vending machine":       8004,
    "Gym: Euro behind building":                    8005,
    "Gym: Euro at end of train tracks":             8006,
    "Gym: Euro on bee sign under clouds":           8007,
    "Tyre: Euro on roof of entrance":               8008,
    "Water Zone: Euro under stairs underwater":     8009,
    "Beenie Death: Euro behind cross":              8010,
    "Canyon: Euro on edge of canyon":               8011,
    "Trasco: Euro on edge wall 1":                  8012,
    "Trasco: Euro on edge wall 2":                  8013,
    "Trasco: Euro on edge wall 3":                  8014,
    "City: Euro on watertower":                     8015,
    "City: Euro near boat on edge of city":         8016,
    "City: Euro at Robin P. Bobin Store":           8017,
    "City: Euro next to Robin P. Bobin Store":      8018,
    "City: Euro near Guns stands":                  8019,
    "City: Euro under city on girders 1":           8020,
    "City: Euro under city on girders 2":           8021,
    "City: Euro under city on girders 3":           8022,
    "City: Euro under city on girders 4":           8023,
    "City: Euro near cheese wheel":                 8024,
    "Village: Euro on castle":                      8025,
    "Village: Euro near furnace":                   8026,
    "Wastes: Euro on top of breakfast building":    8027,
    "Wastes: Euro on top of chinese building":      8028,
    "Wastes: Euro on lower end of chinese building": 8029,
    "Wastes: Euro on sad therapy sign building":    8030,
    "Wastes: Euro nearby mystical dumbbell in flowers": 8031,
    "Wastes: Euro on road edge":                    8032,
    "Wastes: Euro on dead blimbos building":        8033,
    "Desert: Euro on tilted building":              8034,
    "Desert: Euro in moai head pool 1":             8035,
    "Desert: Euro in moai head pool 2":             8036,
    "Desert: Euro in moai head pool 3":             8037,
    "Desert: Euro in moai head pool 4":             8038,
    "Desert: Euro in moai head pool 5":             8039,
    "Desert: Euro in moai head pool 6":             8040,
    "Desert: Euro on pillar near MFC":              8041,
    "Desert: Euro on yellow house roof in fridge land": 8042,
    "Desert: Euro in New Buisness HQ":              8043,
    "Desert: Euro on top of fridge land skull":     8044,
    "Desert: Euro on blue house roof in fridge land": 8045,
    "Desert: Euro in BLMB nuclear reactor":         8046,
    "Brazil: Euro on middle hill":                  8047,
    "Hat Store: Euro from saving Toastie":          8048,

    # --- Random Extras ---
    "Complete Behrman Speedway in under 1 minute": 9001,
}


class FuniRaccoonLocation(Location):
    game = "Funi Raccoon Game"


# Maps each location to the region it belongs in based on the item's first
# in-game appearance. Items that first appear in Sphere 1 are not listed
# and default to "Overworld".
LOCATION_REGION: dict[str, str] = {
    # --- Act 1 ---
    # Behrman Gymnasium
    "Store Radio":                                "Behrman Gymnasium",
    "Store Concrete Cat":                         "Behrman Gymnasium",
    "Store Paracetamol 650mg":                    "Behrman Gymnasium",
    "Store Digital Polaroid Camera":              "Behrman Gymnasium",
    "Find Concrete Cat":                          "Behrman Gymnasium",
    "Gym: Euro on roof with vending machine":     "Behrman Gymnasium",
    "Gym: Euro behind building":                  "Behrman Gymnasium",
    "Gym: Euro at end of train tracks":           "Behrman Gymnasium",
    "Gym: Euro on bee sign under clouds":         "Behrman Gymnasium",

    # Behrman Speedway
    "Complete Behrman Speedway in under 1 minute":"Behrman Speedway",

    # Tyre World
    "Store Orphan Tyre":                          "Tyre World",
    "Store Papa Tyre":                            "Tyre World",
    "Store Smoker":                               "Tyre World",
    "Store Broken Truck":                         "Tyre World",
    "Tyre: Euro on roof of entrance":             "Tyre World",

    # Chicken Farm
    "Store Chicken":                              "Chicken Farm",
    "Find Sombrero":                              "Chicken Farm",
    "Norwich: Euro at chicken farm island":       "Chicken Farm",
    "Chicken Farm: Euro on pillar":               "Chicken Farm",

    # HAT STORE
    "Store Mr. Heel":                             "HAT STORE",
    "Store Ms. Heel":                             "HAT STORE",
    "Hat Store: Euro from saving Toastie":        "HAT STORE",

    # Cleaners
    "Store Washing Machine":                      "Cleaners",

    # Da Waaaater Zoooone
    "Store Gizmo Cat":                            "Da Waaaater Zoooone",
    "Find Gizmo Cat":                             "Da Waaaater Zoooone",
    "Store Fan":                                  "Da Waaaater Zoooone",
    "Eat Green Mystical Gem":                     "Da Waaaater Zoooone",
    "Water Zone: Euro under stairs underwater":   "Da Waaaater Zoooone",
    
    # Raccoon Central Station
    "Store Manhole Cover":                        "Raccoon Central Station",
    "Store Old Sign":                             "Raccoon Central Station",
    "Store Warning Sign":                         "Raccoon Central Station",
    "Store Area Sign":                            "Raccoon Central Station",
    "Store Funi Raccoon Game Deluxe":             "Raccoon Central Station",
    "Store Bench":                                "Raccoon Central Station",

    # Museum (15 items)
    "Store Logan/Real Knight Left":               "Museum",
    "Store Logan/Real Knight Right":              "Museum",
    "Store Pawn":                                 "Museum",
    "Store Rook":                                 "Museum",
    "Store Bishop":                               "Museum",
    "Store King":                                 "Museum",
    "Store Queen":                                "Museum",
    "Store Spoonsweet":                           "Museum",
    "Store Wriks Celler":                         "Museum",
    "Store Barrel":                               "Museum",
    "Store Friend Martin Friendship Statue":      "Museum",
    "Store Funi Raccoon":                         "Museum",
    "Find Top Hat":                               "Museum",
    
    # Chamber
    "Store Michi Cat":                            "Chamber",
    "Find Michi Cat":                             "Chamber",
    "Eat Mystical Dumbbell - Act 2":              "Chamber",

    # --- Act 2 (25 items) ---
    # Beenie HQ
    "Store Evil Fish":                            "Beenie HQ",
    "Store Beenie the Birthday Boy":              "Beenie HQ",
    "Store Letter B":                             "Beenie HQ",
    "Store Patrick O'Hara":                       "Beenie HQ",
    "Store Beach Ball":                           "Beenie HQ",
    "Store Crayon":                               "Beenie HQ",
    "Store Funi Marketable Plushie":              "Beenie HQ",

    # Beenie Factory
    "Store Marketable Plushie Box":               "Beenie Factory",
    "Store Goo":                                  "Beenie Factory",

    # The Process
    "Store Microwave":                            "The Process",
    "Store Beautiful Flower":                     "The Process",
    "Store Buisness Man":                         "The Process",
    "Store Patrice":                              "The Process",
    "Find Jester Hat":                            "The Process",

    # THE MACHINE
    "Store Beenie, Our Savior":                   "THE MACHINE",
    "Store Candle":                               "THE MACHINE",
    "Store Beenie Saves The Orphans":             "THE MACHINE",

    # Fish Vore
    "Store Pirate":                               "Fish Vore",
    "Store Pirate 2":                             "Fish Vore",
    "Store Pirate 3":                             "Fish Vore",

    # Goo Office
    "Store Divider":                              "Goo Office",
    "Store Office Chair":                         "Goo Office",
    "Store Desk":                                 "Goo Office",
    "Store Goo Container":                        "Goo Office",

    # Underground Metro
    "Store Keksz Cat":                            "Underground Metro",
    "Find Keksz Cat":                             "Underground Metro",

    # Beenies Ascension
    "Store Priestess":                            "Beenies Ascension",
    "Beenie Death: Euro behind cross":            "Beenies Ascension",

    # Fields
    "Store Feral Dog":                            "Fields",
    # Store Windmill is storable from Fields or from Blimbo Village once Act 3 is
    # open, so it's hosted in Beenie HQ (skipping the Goo gate into Fields) with an
    # explicit rule in rules.py.
    "Store Windmill":                             "Beenie HQ",
    "Store Crisp":                                "Fields",
    "Store Crisps Undying Love":                  "Fields",

    # Fellowship of the Church of the Beenie
    "Store Folding Chair":                        "Fellowship",
    "Store GREENISH ABOMINATION":                 "Fellowship",

    # Howth
    "Store Street Lamp":                          "Howth",
    "Store Kettle":                               "Howth",
    "Eat Blue Mystical Gem":                      "Howth",

    # --- Act 3 (35 items) ---
    
    # Blimbo Village
    "Store Blimbo Village Sign":                  "Blimbo Village",
    "Store Gas Drum":                             "Blimbo Village",
    "Store Ougham Stone":                         "Blimbo Village",
    'Store "Cow"':                                "Blimbo Village",
    "Store CHEESE":                               "Blimbo Village",
    "Store Door":                                 "Blimbo Village",
    "Store Under Construction":                   "Blimbo Village",
    "Store ROAD NOT DONE":                        "Blimbo Village",
    "Store Old Ass Rusty Ass Key":                "Blimbo Village",
    "Store Fone":                                 "Blimbo Village",
    "Store Plimbo":                               "Blimbo Village",
    "Find Media Player Hat":                      "Blimbo Village",
    "Village: Euro on castle":                    "Blimbo Village",
    "Village: Euro near furnace":                 "Blimbo Village",
    "Purchase Kei Truck Radio":                   "Blimbo Village",
    "Purchase Kei Truck Toaster":                 "Blimbo Village",
    "Purchase Kei Truck Boost":                   "Blimbo Village",
    "Get 1000 Score with Kei Truck":              "Blimbo Village",
    "Get 2000 Score with Kei Truck":              "Blimbo Village",
    "Get 3000 Score with Kei Truck":              "Blimbo Village",
    "Get 4000 Score with Kei Truck":              "Blimbo Village",
    "Get 5000 Score with Kei Truck":              "Blimbo Village",
    
    # Petrol Station (within the Blimbo Village area)
    "Store Gas Pumpo":                            "Petrol Station",
    "Store Binocublo":                            "Petrol Station",
    "Store Police Car":                           "Petrol Station",
    "Store Knifedog":                             "Petrol Station",
    "Store Bomb":                                 "Petrol Station",

    # Bildal Mines (from Blimbo Village)
    "Store Pickaxe":                              "Bildal Mines",
    "Store boingler Cat":                         "Bildal Mines",
    "Find boingler Cat":                          "Bildal Mines",
    "Store Broken Wall":                          "Bildal Mines",

    # Cricket
    "Store Cricket Bat":                          "Cricket",
    "Store Cricket":                              "Cricket",

    # Garden World
    "Store Flowian":                              "Garden World",
    "Store Radio Blimbo":                         "Garden World",
    
    # Mikk Barge
    "Eat Purple Mystical Gem":                    "Mikk Barge",
    "Store Mikk Masive Sign":                    "Mikk Barge",

    # The Forest
    "Store Eel Can":                              "The Forest",
    "Find Raccoon Hat":                           "The Forest",

    # Trasco Carpark
    "Store Coffee Shop (closed)":                 "Trasco Carpark",
    "Store Trolley":                              "Trasco Carpark",
    "Store Fridge Key":                           "Trasco Carpark",
    # Store Fridge is reachable from Trasco Carpark or by taking the train to Brazil,
    # so it's hosted in the always-open station with an explicit rule in rules.py.
    "Store Fridge":                               "Raccoon Central Station",
    "Store CD Player":                            "Trasco Carpark",
    "Store Trasco Sign":                          "Trasco Carpark",
    "Eat Mystical Dumbbell - Act 3":              "Trasco Carpark",
    "Trasco: Euro on edge wall 1":                "Trasco Carpark",
    "Trasco: Euro on edge wall 2":                "Trasco Carpark",
    "Trasco: Euro on edge wall 3":                "Trasco Carpark",

    # Fridge World
    "Store Milk Klubnika":                        "Fridge World",
    
    # Purgatory
    "Store My Favourite Chair":                   "Purgatory",

    # --- Blimbo City cluster (35 items + Kei Truck) ---
    "Store Coffee Cup":                           "Blimbo City",
    "Store Radiator":                             "Blimbo City",
    "Store Evil Raccoon":                         "Blimbo City",
    "Store Naked Fella":                          "Blimbo City",
    "Store Bin":                                  "Blimbo City",
    "Store Blimbo City Sign":                     "Blimbo City",
    "Store Suitcase":                             "Blimbo City",
    "Store Bell Boy":                             "Blimbo City",
    "Store Yolky":                                "Blimbo City",
    "Store Patrick O Bobble":                     "Blimbo City",
    "Store Dice":                                 "Blimbo City",
    "Store Average Canadian":                     "Blimbo City",
    "Store Apple":                                "Blimbo City",
    "City: Euro on watertower":                   "Blimbo City",
    "City: Euro near boat on edge of city":       "Blimbo City",
    "City: Euro at Robin P. Bobin Store":         "Blimbo City",
    "City: Euro next to Robin P. Bobin Store":    "Blimbo City",
    "City: Euro near Guns stands":                "Blimbo City",
    "City: Euro under city on girders 1":         "Blimbo City",
    "City: Euro under city on girders 2":         "Blimbo City",
    "City: Euro under city on girders 3":         "Blimbo City",
    "City: Euro under city on girders 4":         "Blimbo City",
    "City: Euro near cheese wheel":               "Blimbo City",

    # Pub (from Blimbo City)
    "Store Cheeky Pint":                          "Pub",
    "Find Patty Hat":                             "Pub",

    # BLMB Reactor Core (from Blimbo City + Kei Truck)
    "Store Cooling Rod":                          "BLMB Reactor Core",
    "Store Demon Core":                           "BLMB Reactor Core",
    "Store Warning":                              "BLMB Reactor Core",

    # --- Act 4 (50 items + Kei Truck) ---
    # Messed Up Canyon
    "Store BookBlo":                              "Messed Up Canyon",
    "Store Cheese Wife":                          "Messed Up Canyon",
    "Canyon: Euro on edge of canyon":             "Messed Up Canyon",

    # Pharmacy
    "Store Anti Sads":                            "Pharmacy",
    "Store Leeches!":                             "Pharmacy",

    # The Desert
    "Store Snowball":                             "The Desert",
    "Store Fridgling":                            "The Desert",
    "Store Fridge King's Cooling Rod":            "The Desert",
    "Find Fridge Crown":                          "The Desert",
    "Desert: Euro on tilted building":            "The Desert",
    "Desert: Euro in moai head pool 1":           "The Desert",
    "Desert: Euro in moai head pool 2":           "The Desert",
    "Desert: Euro in moai head pool 3":           "The Desert",
    "Desert: Euro in moai head pool 4":           "The Desert",
    "Desert: Euro in moai head pool 5":           "The Desert",
    "Desert: Euro in moai head pool 6":           "The Desert",
    "Desert: Euro on pillar near MFC":            "The Desert",
    "Desert: Euro on yellow house roof in fridge land": "The Desert",
    "Desert: Euro in New Buisness HQ":            "The Desert",
    "Desert: Euro on top of fridge land skull":   "The Desert",
    "Desert: Euro on blue house roof in fridge land":   "The Desert",
    "Desert: Euro in BLMB nuclear reactor":       "The Desert",

    # The Well of Knowledge
    "Store Hazelnut":                             "The Well of Knowledge",

    # Cliffs of Nowher
    "Store Butterfly":                            "Cliffs of Nowher",
    "Store Lughling":                             "Cliffs of Nowher",

    # Da Dryyyy Zoooone
    "Eat Red Mystical Gem":                       "Da Dryyyy Zoooone",

    # Municipal Wastes
    "Store Chairapist":                           "Municipal Wastes",
    "Store Synthesizer":                          "Municipal Wastes",
    "Store Real Gym":                             "Municipal Wastes",
    "Store Plimbo's Cooling Rod":                 "Municipal Wastes",
    "Store Lloyd":                                "Municipal Wastes",
    "Eat Mystical Dumbbell - Act 4":              "Municipal Wastes",
    "Wastes: Euro on top of breakfast building":  "Municipal Wastes",
    "Wastes: Euro on top of chinese building":    "Municipal Wastes",
    "Wastes: Euro on lower end of chinese building": "Municipal Wastes",
    "Wastes: Euro on sad therapy sign building":  "Municipal Wastes",
    "Wastes: Euro nearby mystical dumbbell in flowers": "Municipal Wastes",
    "Wastes: Euro on road edge":                  "Municipal Wastes",
    "Wastes: Euro on dead blimbos building":      "Municipal Wastes",

    # The Gully
    "Store Belgium Waffle":                       "The Gully",
    "Store Orb":                                  "The Gully",
    
    # Brazil
    "Store Brazil Knight":                        "Brazil",
    "Store Real Football":                        "Brazil",
    "Store Doggy":                                "Brazil",
    "Brazil: Euro on middle hill":                "Brazil",
}


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


_EURO_LOCATIONS  = {n for n, i in LOCATION_NAME_TO_ID.items() if 8001 <= i <= 8999}
_GEM_LOCATIONS   = {n for n, i in LOCATION_NAME_TO_ID.items() if 7001 <= i <= 7999}
_HAT_LOCATIONS   = {n for n, i in LOCATION_NAME_TO_ID.items() if 6001 <= i <= 6999}


def get_excluded_locations(world: FuniRaccoonWorld) -> set[str]:
    excluded: set[str] = set()
    if not world.options.eurosanity:
        excluded |= _EURO_LOCATIONS
    if not world.options.gemsanity:
        excluded |= _GEM_LOCATIONS
    if not world.options.hatsanity:
        excluded |= _HAT_LOCATIONS
    return excluded


def create_all_locations(world: FuniRaccoonWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: FuniRaccoonWorld) -> None:
    excluded = get_excluded_locations(world)
    for loc_name, loc_id in LOCATION_NAME_TO_ID.items():
        if loc_name in excluded:
            continue
        region_name = LOCATION_REGION.get(loc_name, "Overworld")
        region = world.get_region(region_name)
        region.add_locations({loc_name: loc_id}, FuniRaccoonLocation)


def create_events(world: FuniRaccoonWorld) -> None:
    overworld = world.get_region("Overworld")
    overworld.add_event(
        "Victory", "Victory", location_type=FuniRaccoonLocation, item_type=items.FuniRaccoonItem
    )
