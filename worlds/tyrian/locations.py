# Archipelago MultiWorld integration for Tyrian
#
# This file is copyright (C) Kay "Kaito" Sinclaire,
# and is released under the terms of the zlib license.
# See "LICENSE" for more details.

from typing import TYPE_CHECKING, Any

from BaseClasses import LocationProgressType as LPType

from .items import Episode

if TYPE_CHECKING:
    from . import TyrianLocation, TyrianWorld


class LevelRegion:
    # I don't really like the distribution I was getting from just doing random.triangular, so
    # instead we have multiple different types of random prices that can get generated, and we choose
    # which one we want randomly (based on the level we're generating it for).
    # Appending an "!" makes the shop location prioritized.
    base_shop_setup_list: dict[str, tuple[int, int, int]] = {
        "A": (   50,   501,   1),
        "B": (  100,  1001,   1),
        "C": (  200,  2001,   2),
        "D": (  400,  3001,   2),
        "E": (  750,  3001,   5),
        "F": (  500,  5001,   5),
        "G": ( 1000,  7501,   5),
        "H": ( 2000,  7501,  10),
        "I": ( 3000,  9001,  10),
        "J": ( 2000, 10001,   5),
        "K": ( 3000, 10001,  10),
        "L": ( 5000, 10001,  25),
        "M": ( 3000, 15001,  10),
        "N": ( 5000, 15001,  25),
        "O": ( 7500, 15001,  50),
        "P": ( 4000, 20001,  10),
        "Q": ( 5000, 20001,  25),
        "R": ( 6000, 20001,  50),
        "S": ( 8000, 20001, 100),
        "T": ( 7500, 30001,  25),
        "U": ( 9000, 30001,  50),
        "V": (10000, 30001, 100),
        "W": (12000, 30001, 250),
        "X": (15000, 40001, 100),
        "Y": (15000, 40001, 250),
        "Z": (65535, 65536,   1)  # Always max shop price
    }

    episode: Episode
    locations: dict[str, Any]  # List of strings to location or sub-region names
    flattened_locations: dict[str, int]  # Only location names, ignoring sub-regions
    shop_setups: list[str]  # See base_shop_setups_list above

    def __init__(self, episode: Episode, locations: dict[str, Any], shop_setups: list[str] = ["F", "H", "K", "L"]):
        self.episode = episode
        self.locations = locations
        self.shop_setups = shop_setups

        # Immediately create a flattened location list
        def shop_locations(name: str, all_ids: tuple[int, ...]) -> dict[str, int]:
            # Turns "Shop - LEVELNAME (Episode 1)": (...) into individual location names
            return {f"{name} - Item {(shop_id - all_ids[0]) + 1}": shop_id for shop_id in all_ids}

        def flatten(locations: dict[str, Any]) -> dict[str, int]:
            results: dict[str, int] = {}
            for name, value in locations.items():
                if type(value) is dict:
                    results.update(flatten(value))
                elif type(value) is tuple:
                    results.update(shop_locations(name, value))
                else:
                    results[name] = value
            return results

        self.flattened_locations = flatten(locations)

    # Gets a random price based on this level's shop setups, and assigns it to the locaton.
    # Also changes location progress type automatically based on the setup rolled.
    def set_random_shop_price(self, world: "TyrianWorld", location: "TyrianLocation") -> None:
        setup_choice = world.random.choice(self.shop_setups)
        if len(setup_choice) > 1 and setup_choice[-1] == "!":
            location.progress_type = LPType.PRIORITY
        location.shop_price = min(world.random.randrange(*self.base_shop_setup_list[setup_choice[0]]), 65535)

    # Gets a flattened dict of all locations, id: name
    def get_locations(self, base_id: int = 0) -> dict[str, int]:
        return {name: base_id + location_id for (name, location_id) in self.flattened_locations.items()}

    # Returns just names from the above.
    def get_location_names(self) -> set[str]:
        return {name for name in self.flattened_locations.keys()}


class LevelLocationData:

    level_regions: dict[str, LevelRegion] = {

        # =============================================================================================
        # EPISODE 1 - ESCAPE
        # =============================================================================================

        # The hard variant of Tyrian is similarly designed, just with more enemies, so it shares checks.
        "TYRIAN (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "TYRIAN (Episode 1) - First U-Ship Secret": 0,
            "TYRIAN (Episode 1) - Early Spinner Formation": 1,
            "TYRIAN (Episode 1) - Lander near BUBBLES Warp Rock": 2,
            "TYRIAN (Episode 1) - BUBBLES Warp Rock": 3,
            "TYRIAN (Episode 1) - HOLES Warp Orb": 4,
            "TYRIAN (Episode 1) - Ships Between Platforms": 5,
            "TYRIAN (Episode 1) - First Line of Tanks": 6,
            "TYRIAN (Episode 1) - Tank Turn-and-fire Secret": 7,
            "TYRIAN (Episode 1) - SOH JIN Warp Orb": 8,

            "TYRIAN (Episode 1) @ Pass Boss (can time out)": {
                "TYRIAN (Episode 1) - Boss": 9,
                "Shop - TYRIAN (Episode 1)": (1000, 1001, 1002, 1003, 1004),
            },
        }, shop_setups=["A", "B", "C", "D", "D", "E", "F", "F", "G", "I"]),

        "BUBBLES (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "BUBBLES (Episode 1) @ Pass Bubble Lines": {
                "BUBBLES (Episode 1) - Orbiting Bubbles": 10,
                "BUBBLES (Episode 1) - Shooting Bubbles": 11,
                "BUBBLES (Episode 1) - Final Bubble Line": 15,
                "Shop - BUBBLES (Episode 1)": (1010, 1011, 1012, 1013, 1014),

                "BUBBLES (Episode 1) @ Speed Up Section": {
                    "BUBBLES (Episode 1) - Coin Rain, First Line": 12,
                    "BUBBLES (Episode 1) - Coin Rain, Fourth Line": 13,
                    "BUBBLES (Episode 1) - Coin Rain, Sixth Line": 14,
                },
            },
        }, shop_setups=["C", "D", "E", "G", "I"]),

        "HOLES (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "HOLES (Episode 1) - U-Ship Formation 1": 20,
            "HOLES (Episode 1) - U-Ship Formation 2": 21,

            "HOLES (Episode 1) @ Pass Spinner Gauntlet": {
                "HOLES (Episode 1) - Lander after Spinners": 22,
                "HOLES (Episode 1) - U-Ships after Boss Fly-By": 24,
                "HOLES (Episode 1) - Before Speed Up Section": 26,
                "Shop - HOLES (Episode 1)": (1020, 1021, 1022, 1023, 1024),

                "HOLES (Episode 1) @ Destroy Boss Ships": {
                    "HOLES (Episode 1) - Boss Ship Fly-By 1": 23,
                    "HOLES (Episode 1) - Boss Ship Fly-By 2": 25,
                },
            },
        }, shop_setups=["C", "D", "D", "E", "F", "F", "H"]),

        "SOH JIN (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "SOH JIN (Episode 1) - Starting Alcove": 30,
            "SOH JIN (Episode 1) - Triple Diagonal Launchers": 32,
            "SOH JIN (Episode 1) - Checkerboard Pattern": 33,
            "SOH JIN (Episode 1) - Triple Orb Launchers": 34,
            "SOH JIN (Episode 1) - Double Orb Launcher Line": 35,
            "SOH JIN (Episode 1) - Next to Double Point Items": 36,
            "Shop - SOH JIN (Episode 1)": (1030, 1031, 1032, 1033, 1034),

            "SOH JIN (Episode 1) @ Destroy Walls": {
                "SOH JIN (Episode 1) - Walled-in Orb Launcher": 31,
            },
        }, shop_setups=["F", "H", "H", "J", "J", "T"]),

        "ASTEROID1 (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "ASTEROID1 (Episode 1) - Shield Ship in Asteroid Field": 40,
            "ASTEROID1 (Episode 1) - Railgunner 1": 41,
            "ASTEROID1 (Episode 1) - Railgunner 2": 42,
            "ASTEROID1 (Episode 1) - Railgunner 3": 43,
            "ASTEROID1 (Episode 1) - ASTEROID? Warp Orb": 44,
            "ASTEROID1 (Episode 1) - Maneuvering Missiles": 45,

            "ASTEROID1 (Episode 1) @ Destroy Boss": {
                "ASTEROID1 (Episode 1) - Boss": 46,
                "Shop - ASTEROID1 (Episode 1)": (1040, 1041, 1042, 1043, 1044),
            },
        }, shop_setups=["E", "F", "F", "F", "G"]),

        "ASTEROID2 (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "ASTEROID2 (Episode 1) - Tank Turn-around Secret 1": 50,
            "ASTEROID2 (Episode 1) - First Tank Squadron": 51,
            "ASTEROID2 (Episode 1) - Tank Turn-around Secret 2": 52,
            "ASTEROID2 (Episode 1) - Second Tank Squadron": 53,
            "ASTEROID2 (Episode 1) - Tank Bridge": 54,
            "ASTEROID2 (Episode 1) - Tank Assault, Right Tank Secret": 55,
            "ASTEROID2 (Episode 1) - MINEMAZE Warp Orb": 56,

            "ASTEROID2 (Episode 1) @ Destroy Boss": {
                "ASTEROID2 (Episode 1) - Boss": 57,
                "Shop - ASTEROID2 (Episode 1)": (1050, 1051, 1052, 1053, 1054),
            },
        }, shop_setups=["E", "F", "F", "F", "G"]),

        "ASTEROID? (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "ASTEROID? (Episode 1) @ Initial Welcome": {
                "ASTEROID? (Episode 1) - Welcoming Launchers 1": 60,
                "ASTEROID? (Episode 1) - Welcoming Launchers 2": 61,
                "ASTEROID? (Episode 1) - Mid-Boss Launcher": 62,
                "ASTEROID? (Episode 1) - WINDY Warp Orb": 63,

                "ASTEROID? (Episode 1) @ Quick Shots": {
                    "ASTEROID? (Episode 1) - Quick Shot 1": 64,
                    "ASTEROID? (Episode 1) - Quick Shot 2": 65,
                },
                "ASTEROID? (Episode 1) @ Final Gauntlet": {
                    "Shop - ASTEROID? (Episode 1)": (1060, 1061, 1062, 1063, 1064),
                },
            },
        }, shop_setups=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]),

        "MINEMAZE (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "MINEMAZE (Episode 1) @ Destroy Gates": {
                "MINEMAZE (Episode 1) - Starting Gate": 70,
                "MINEMAZE (Episode 1) - Lone Orb": 71,
                "MINEMAZE (Episode 1) - Right Path Gate": 72,
                "MINEMAZE (Episode 1) - That's not a Strawberry": 73,
                "MINEMAZE (Episode 1) - ASTEROID? Warp Orb": 74,
                "MINEMAZE (Episode 1) - Ships Behind Central Gate": 75,
                "Shop - MINEMAZE (Episode 1)": (1070, 1071, 1072, 1073, 1074),
            },
        }, shop_setups=["E", "F", "F", "F", "G"]),

        "WINDY (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "WINDY (Episode 1) @ Fly Through": {
                "Shop - WINDY (Episode 1)": (1080, 1081, 1082, 1083, 1084),

                "WINDY (Episode 1) @ Phase Through Walls": {
                    "WINDY (Episode 1) - Central Question Mark": 80,
                },
            },
        }, shop_setups=["F", "G", "I"]),

        # This is the variant of Savara on Easy or Medium.
        "SAVARA (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "SAVARA (Episode 1) - White Formation Leader 1": 90,
            "SAVARA (Episode 1) - White Formation Leader 2": 91,
            "SAVARA (Episode 1) - Green Plane Line": 92,
            "SAVARA (Episode 1) - Brown Plane Breaking Formation": 93,
            "SAVARA (Episode 1) - Huge Plane, Speeds By": 94,
            "SAVARA (Episode 1) - Vulcan Plane": 95,

            "SAVARA (Episode 1) @ Pass Boss (can time out)": {
                "SAVARA (Episode 1) - Boss": 96,
                "Shop - SAVARA (Episode 1)": (1090, 1091, 1092, 1093, 1094),
            },
        }, shop_setups=["E", "H", "L", "P"]),

        # This is the variant of Savara on Hard or above.
        "SAVARA II (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "SAVARA II (Episode 1) @ Base Requirements": {
                "SAVARA II (Episode 1) - Launched Planes 1": 100,
                "SAVARA II (Episode 1) - Huge Plane Amidst Turrets": 102,
                "SAVARA II (Episode 1) - Vulcan Planes Near Blimp": 103,
                "SAVARA II (Episode 1) - Launched Planes 2": 105,

                "SAVARA II (Episode 1) @ Destroy Green Planes": {
                    "SAVARA II (Episode 1) - Green Plane Sequence 1": 101,
                    "SAVARA II (Episode 1) - Green Plane Sequence 2": 104,
                },
                "SAVARA II (Episode 1) @ Pass Boss (can time out)": {
                    "SAVARA II (Episode 1) - Boss": 106,
                    "Shop - SAVARA II (Episode 1)": (1100, 1101, 1102, 1103, 1104),
                },
            },
        }, shop_setups=["E", "H", "L", "P"]),

        "BONUS (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "BONUS (Episode 1) @ Destroy Patterns": {
                "Shop - BONUS (Episode 1)": (1110, 1111, 1112, 1113, 1114),
            }
        }, shop_setups=["J", "J", "J", "K", "K", "L"]),

        "MINES (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "MINES (Episode 1) - Blue Mine": 121,
            "MINES (Episode 1) - Absolutely Free": 123,
            "MINES (Episode 1) - But Wait There's More": 124,
            "Shop - MINES (Episode 1)": (1120, 1121, 1122, 1123, 1124),

            "MINES (Episode 1) @ Destroy First Orb": {
                "MINES (Episode 1) - Regular Spinning Orbs": 120,

                "MINES (Episode 1) @ Destroy Second Orb": {
                    "MINES (Episode 1) - Repulsor Spinning Orbs": 122,
                },
            },
        }, shop_setups=["E", "F", "G", "H", "J"]),

        "DELIANI (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "DELIANI (Episode 1) - First Turret Wave 1": 130,
            "DELIANI (Episode 1) - First Turret Wave 2": 131,
            "DELIANI (Episode 1) - Tricky Rail Turret": 132,
            "DELIANI (Episode 1) - Second Turret Wave 1": 133,
            "DELIANI (Episode 1) - Second Turret Wave 2": 134,

            "DELIANI (Episode 1) @ Pass Ambush": {
                "DELIANI (Episode 1) - Ambush": 135,
                "DELIANI (Episode 1) - Last Cross Formation": 136,

                "DELIANI (Episode 1) @ Destroy Boss": {
                    "DELIANI (Episode 1) - Boss": 137,
                    "Shop - DELIANI (Episode 1)": (1130, 1131, 1132, 1133, 1134),
                },
            },
        }, shop_setups=["K", "M", "O", "P", "Q"]),

        "SAVARA V (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "SAVARA V (Episode 1) - Green Plane Sequence": 140,
            "SAVARA V (Episode 1) - Flying Between Blimps": 141,
            "SAVARA V (Episode 1) - Brown Plane Sequence": 142,
            "SAVARA V (Episode 1) - Flying Alongside Green Planes": 143,
            "SAVARA V (Episode 1) - Super Blimp": 144,

            "SAVARA V (Episode 1) @ Destroy Bosses": {
                "SAVARA V (Episode 1) - Mid-Boss": 145,
                "SAVARA V (Episode 1) - Boss": 146,
                "Shop - SAVARA V (Episode 1)": (1140, 1141, 1142, 1143, 1144),
            },
        }, shop_setups=["E", "H", "L", "P"]),

        "ASSASSIN (Episode 1)": LevelRegion(episode=Episode.Escape, locations={
            "ASSASSIN (Episode 1) @ Destroy Boss": {
                "ASSASSIN (Episode 1) - Boss": 150,
                "Shop - ASSASSIN (Episode 1)": (1150, 1151, 1152, 1153, 1154),
                # Event: "Episode 1 (Escape) Complete"
            },
        }, shop_setups=["S"]),

        # =============================================================================================
        # EPISODE 2 - TREACHERY
        # =============================================================================================

        "TORM (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "TORM (Episode 2) - Jungle Ship V Formation 1": 160,
            "TORM (Episode 2) - Ship Fleeing Dragon Secret": 161,
            "TORM (Episode 2) - Excuse Me, You Dropped This": 162,
            "TORM (Episode 2) - Jungle Ship V Formation 2": 163,
            "TORM (Episode 2) - Jungle Ship V Formation 3": 164,
            "TORM (Episode 2) - Undocking Jungle Ship": 165,
            "TORM (Episode 2) - Boss Ship Fly-By": 166,

            "TORM (Episode 2) @ Pass Boss (can time out)": {
                "TORM (Episode 2) - Boss": 167,
                "Shop - TORM (Episode 2)": (1160, 1161, 1162, 1163, 1164),
            },
        }, shop_setups=["A", "B", "C", "D", "D", "E", "F", "F", "G", "I"]),

        "GYGES (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "GYGES (Episode 2) - Circled Shapeshifting Turret 1": 170,
            "GYGES (Episode 2) - Wide Waving Worm": 171,
            "GYGES (Episode 2) - Orbsnake": 172,
            "GYGES (Episode 2) @ After Speed Up Section": {
                "GYGES (Episode 2) - GEM WAR Warp Orb": 173,
                "GYGES (Episode 2) - Circled Shapeshifting Turret 2": 174,
                "GYGES (Episode 2) - Last Set of Worms": 175,

                "GYGES (Episode 2) @ Destroy Boss": {
                    "GYGES (Episode 2) - Boss": 176,
                    "Shop - GYGES (Episode 2)": (1170, 1171, 1172, 1173, 1174),
                },
            },
        }, shop_setups=["F", "F", "H", "H", "M"]),

        "BONUS 1 (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "BONUS 1 (Episode 2) @ Destroy Patterns": {
                "Shop - BONUS 1 (Episode 2)": (1180, 1181, 1182, 1183, 1184),
            },
        }, shop_setups=["J", "J", "J", "K", "K", "L"]),

        "ASTCITY (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "ASTCITY (Episode 2) @ Base Requirements": {
                "ASTCITY (Episode 2) - Shield Ship V Formation 1": 190,
                "ASTCITY (Episode 2) - Shield Ship V Formation 2": 191,
                "ASTCITY (Episode 2) - Plasma Turrets Going Uphill": 192,
                "ASTCITY (Episode 2) - Warehouse 92": 193,
                "ASTCITY (Episode 2) - Shield Ship V Formation 3": 194,
                "ASTCITY (Episode 2) - Shield Ship Canyon 1": 195,
                "ASTCITY (Episode 2) - Shield Ship Canyon 2": 196,
                "ASTCITY (Episode 2) - Shield Ship Canyon 3": 197,
                "ASTCITY (Episode 2) - MISTAKES Warp Orb": 198,
                "ASTCITY (Episode 2) - Ending Turret Group": 199,
                "Shop - ASTCITY (Episode 2)": (1190, 1191, 1192, 1193, 1194),
            },
        }, shop_setups=["I", "M", "P"]),

        "BONUS 2 (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "Shop - BONUS 2 (Episode 2)": (1200, 1201, 1202, 1203, 1204),
        }, shop_setups=["J", "N", "N", "Q"]),

        "GEM WAR (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "GEM WAR (Episode 2) @ Base Requirements": {
                "GEM WAR (Episode 2) @ Red Gem Leaders Easy": {
                    "GEM WAR (Episode 2) - Red Gem Leader 2": 211,
                    "GEM WAR (Episode 2) - Red Gem Leader 3": 212,

                    "GEM WAR (Episode 2) @ Red Gem Leaders Medium": {
                        "GEM WAR (Episode 2) - Red Gem Leader 1": 210,

                        "GEM WAR (Episode 2) @ Red Gem Leaders Hard": {
                            "GEM WAR (Episode 2) - Red Gem Leader 4": 213,
                        },
                    },
                },
                "GEM WAR (Episode 2) @ Blue Gem Bosses": {
                    "GEM WAR (Episode 2) - Blue Gem Boss 1": 214,
                    "GEM WAR (Episode 2) - Blue Gem Boss 2": 215,
                    "Shop - GEM WAR (Episode 2)": (1210, 1211, 1212, 1213, 1214),
                },
            },
        }, shop_setups=["H", "M", "P"]),

        "MARKERS (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "MARKERS (Episode 2) @ Base Requirements": {
                "MARKERS (Episode 2) - Right Path Turret": 220,

                "MARKERS (Episode 2) @ Through Minelayer Blockade": {
                    "MARKERS (Episode 2) - Persistent Minelayer": 221,
                    "MARKERS (Episode 2) - Car Destroyer Secret": 222,
                    "MARKERS (Episode 2) - Left Path Turret": 223,
                    "MARKERS (Episode 2) - End Section Turret": 224,
                    "Shop - MARKERS (Episode 2)": (1220, 1221, 1222, 1223, 1224),
                },
            },
        }, shop_setups=["D", "J", "K", "L", "N", "O"]),

        "MISTAKES (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "MISTAKES (Episode 2) @ Base Requirements": {
                "MISTAKES (Episode 2) - Start, Trigger Enemy 1": 230,
                "MISTAKES (Episode 2) - Start, Trigger Enemy 2": 231,
                "MISTAKES (Episode 2) - Orbsnakes, Trigger Enemy 1": 232,
                "MISTAKES (Episode 2) - Claws, Trigger Enemy 1": 234,
                "MISTAKES (Episode 2) - Drills, Trigger Enemy 1": 236,
                "MISTAKES (Episode 2) - Drills, Trigger Enemy 2": 237,
                "Shop - MISTAKES (Episode 2)": (1230, 1231, 1232, 1233, 1234),

                "MISTAKES (Episode 2) @ Bubble Spawner Path": {
                    "MISTAKES (Episode 2) - Claws, Trigger Enemy 2": 235,
                    "MISTAKES (Episode 2) - Super Bubble Spawner": 238,
                },
                "MISTAKES (Episode 2) @ Softlock Path": {
                    "MISTAKES (Episode 2) - Orbsnakes, Trigger Enemy 2": 233,
                    "MISTAKES (Episode 2) - Anti-Softlock": 239,
                },
            },
        }, shop_setups=["B", "D", "J", "K", "L", "O", "V", "Z!"]),

        "SOH JIN (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "SOH JIN (Episode 2) @ Base Requirements": {
                "SOH JIN (Episode 2) - Sinusoidal Missile Wave": 240,
                "SOH JIN (Episode 2) - Second Missile Ship Set": 241,

                "SOH JIN (Episode 2) @ Destroy Second Wave Paddles": {
                    "SOH JIN (Episode 2) - Paddle Destruction 1": 242,
                    "SOH JIN (Episode 2) - Paddle Destruction 2": 243,
                },
                "SOH JIN (Episode 2) @ Fly Through Third Wave Orbs": {
                    "SOH JIN (Episode 2) - Last Missile Ship Set": 244,
                    "Shop - SOH JIN (Episode 2)": (1240, 1241, 1242, 1243, 1244),

                    "SOH JIN (Episode 2) @ Destroy Third Wave Orbs": {
                        "SOH JIN (Episode 2) - Boss Orbs 1": 245,
                        "SOH JIN (Episode 2) - Boss Orbs 2": 246,
                    },
                },
            },
        }, shop_setups=["G", "I", "L", "O"]),

        "BOTANY A (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "BOTANY A (Episode 2) - Retreating Mobile Turret": 250,

            "BOTANY A (Episode 2) @ Beyond Starting Area": {
                "BOTANY A (Episode 2) - Green Ship Pincer": 254,

                "BOTANY A (Episode 2) @ Can Destroy Turrets": {
                    "BOTANY A (Episode 2) - End of Path Secret 1": 251,
                    "BOTANY A (Episode 2) - Mobile Turret Approaching Head-On": 252,
                    "BOTANY A (Episode 2) - End of Path Secret 2": 253,
                },
                "BOTANY A (Episode 2) @ Pass Boss (can time out)": {
                    "BOTANY A (Episode 2) - Boss": 255,
                    "Shop - BOTANY A (Episode 2)": (1250, 1251, 1252, 1253, 1254),
                },
            },
        }, shop_setups=["J", "N", "R"]),

        "BOTANY B (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "BOTANY B (Episode 2) - Starting Platform Sensor": 260,

            "BOTANY B (Episode 2) @ Beyond Starting Platform": {
                "BOTANY B (Episode 2) - Main Platform Sensor 1": 261,
                "BOTANY B (Episode 2) - Main Platform Sensor 2": 262,
                "BOTANY B (Episode 2) - Main Platform Sensor 3": 263,
                "BOTANY B (Episode 2) - Super-Turret on Bridge": 264,

                "BOTANY B (Episode 2) @ Pass Boss (can time out)": {
                    "BOTANY B (Episode 2) - Boss": 265,
                    "Shop - BOTANY B (Episode 2)": (1260, 1261, 1262, 1263, 1264),
                },
            },
        }, shop_setups=["J", "N", "R"]),

        "GRYPHON (Episode 2)": LevelRegion(episode=Episode.Treachery, locations={
            "GRYPHON (Episode 2) @ Base Requirements": {
                "GRYPHON (Episode 2) - Pulse-Turret Wave Mid-Spikes": 270,
                "GRYPHON (Episode 2) - Swooping Pulse-Turrets": 271,
                "GRYPHON (Episode 2) - Sweeping Pulse-Turrets": 272,
                "GRYPHON (Episode 2) - Spike From Behind": 273,
                "GRYPHON (Episode 2) - Breaking Formation 1": 274,
                "GRYPHON (Episode 2) - Breaking Formation 2": 275,
                "GRYPHON (Episode 2) - Breaking Formation 3": 276,
                "GRYPHON (Episode 2) - Breaking Formation 4": 277,
                "GRYPHON (Episode 2) - Breaking Formation 5": 278,

                "GRYPHON (Episode 2) @ Destroy Boss": {
                    "GRYPHON (Episode 2) - Boss": 279,
                    "Shop - GRYPHON (Episode 2)": (1270, 1271, 1272, 1273, 1274),
                    # Event: "Episode 2 (Treachery) Complete"
                },
            },
        }, shop_setups=["S", "S", "V"]),

        # =============================================================================================
        # EPISODE 3 - MISSION: SUICIDE
        # =============================================================================================

        "GAUNTLET (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "GAUNTLET (Episode 3) - Fork Ships, Right": 280,
            "GAUNTLET (Episode 3) - Fork Ships, Middle": 281,
            "GAUNTLET (Episode 3) - Doubled-up Gates": 282,
            "GAUNTLET (Episode 3) - Capsule Ships Near Mace": 283,
            "GAUNTLET (Episode 3) - Split Gates, Left": 284,

            "GAUNTLET (Episode 3) @ Clear Orb Tree": {
                "GAUNTLET (Episode 3) - Tree of Spinning Orbs": 285,
                "GAUNTLET (Episode 3) - Gate near Freebie Item": 286,
                "GAUNTLET (Episode 3) - Freebie Item": 287,

                "Shop - GAUNTLET (Episode 3)": (1280, 1281, 1282, 1283, 1284),
            }
        }, shop_setups=["A", "B", "C", "D", "D", "E", "F", "F", "G", "I"]),

        "IXMUCANE (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "IXMUCANE (Episode 3) - Pebble Ship, Start": 290,

            "IXMUCANE (Episode 3) @ Pass Minelayers Requirements": {
                "IXMUCANE (Episode 3) - Pebble Ship, Speed Up Section": 291,
                "IXMUCANE (Episode 3) - Enemy From Behind": 292,
                "IXMUCANE (Episode 3) - Sideways Minelayer, Domes": 293,
                "IXMUCANE (Episode 3) - Pebble Ship, Domes": 294,
                "IXMUCANE (Episode 3) - Sideways Minelayer, Before Boss": 295,

                "IXMUCANE (Episode 3) @ Pass Boss (can time out)": {
                    "IXMUCANE (Episode 3) - Boss": 296,
                    "Shop - IXMUCANE (Episode 3)": (1290, 1291, 1292, 1293, 1294),
                },
            }
        }, shop_setups=["F", "H", "N"]),

        "BONUS (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "BONUS (Episode 3) - Lone Turret 1": 300,

            "BONUS (Episode 3) @ Pass Onslaughts": {
                "BONUS (Episode 3) - Lone Turret 2": 303,

                "BONUS (Episode 3) @ Get Items from Onslaughts": {
                    "BONUS (Episode 3) - Behind Onslaught 1": 301,
                    "BONUS (Episode 3) - Behind Onslaught 2": 302,
                },
                "BONUS (Episode 3) @ Sonic Wave Hell": {
                    "BONUS (Episode 3) - Sonic Wave Hell Turret": 304,
                    "Shop - BONUS (Episode 3)": (1300, 1301, 1302, 1303, 1304),
                },
            },
        }, shop_setups=["M", "O", "Q"]),

        "STARGATE (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "STARGATE (Episode 3) - The Bubbleway": 310,
            "STARGATE (Episode 3) - First Bubble Spawner": 311,
            "STARGATE (Episode 3) - AST. CITY Warp Orb 1": 312,
            "STARGATE (Episode 3) - AST. CITY Warp Orb 2": 313,
            "STARGATE (Episode 3) - SAWBLADES Warp Orb 1": 314,
            "STARGATE (Episode 3) - SAWBLADES Warp Orb 2": 315,

            "STARGATE (Episode 3) @ Reach Bubble Spawner": {
                "STARGATE (Episode 3) - Super Bubble Spawner": 316,
                "Shop - STARGATE (Episode 3)": (1310, 1311, 1312, 1313, 1314),
            },
        }, shop_setups=["D", "D", "F", "F", "J"]),

        "AST. CITY (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "AST. CITY (Episode 3) @ Base Requirements": {
                "AST. CITY (Episode 3) - Shield Ship, Start": 320,
                "AST. CITY (Episode 3) - Shield Ship, After Boss Dome 1": 322,
                "AST. CITY (Episode 3) - Shield Ship, Before Boss Dome 2": 323,
                "AST. CITY (Episode 3) - Shield Ship, Near Boss Dome 2": 325,
                "AST. CITY (Episode 3) - Shield Ship, Near Boss Dome 3": 327,
                "Shop - AST. CITY (Episode 3)": (1320, 1321, 1322, 1323, 1324),

                "AST. CITY (Episode 3) @ Destroy Boss Domes": {
                    "AST. CITY (Episode 3) - Boss Dome 1": 321,
                    "AST. CITY (Episode 3) - Boss Dome 2": 324,
                    "AST. CITY (Episode 3) - Boss Dome 3": 326,
                    "AST. CITY (Episode 3) - Boss Dome 4": 328,
                }
            }
        }, shop_setups=["I", "M", "P"]),

        "SAWBLADES (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "SAWBLADES (Episode 3) @ Base Requirements": {
                "SAWBLADES (Episode 3) - Pebble Ship, Start 1": 330,
                "SAWBLADES (Episode 3) - Pebble Ship, Start 2": 331,
                "SAWBLADES (Episode 3) - Light Turret, Gravitium Rocks": 332,
                "SAWBLADES (Episode 3) - Waving Sawblade": 333,
                "SAWBLADES (Episode 3) - Light Turret, After Sawblades": 334,
                "SAWBLADES (Episode 3) - Pebble Ship, After Sawblades": 335,
                "SAWBLADES (Episode 3) - SuperCarrot Secret Drop": 336,
                "Shop - SAWBLADES (Episode 3)": (1330, 1331, 1332, 1333, 1334),
            }
        }, shop_setups=["G", "K", "O"]),

        "CAMANIS (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "CAMANIS (Episode 3) @ Base Requirements": {
                "CAMANIS (Episode 3) - Ice Spitter, Near Plasma Guns": 340,
                "CAMANIS (Episode 3) - Blizzard Ship Assault": 341,
                "CAMANIS (Episode 3) - Ice Spitter, After Blizzard": 342,
                "CAMANIS (Episode 3) - Roaming Snowball": 343,
                "CAMANIS (Episode 3) - Ice Spitter, Ending": 344,

                "CAMANIS (Episode 3) @ Pass Boss (can time out)": {
                    "CAMANIS (Episode 3) - Boss": 345,
                    "Shop - CAMANIS (Episode 3)": (1340, 1341, 1342, 1343, 1344),
                }
            }
        }, shop_setups=["J", "P", "P", "U"]),

        "MACES (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "MACES (Episode 3) - Third Mace's Path": 350,
            "MACES (Episode 3) - Sixth Mace's Path": 351,
            "MACES (Episode 3) - A Brief Reprieve, Left": 352,
            "MACES (Episode 3) - A Brief Reprieve, Center": 353,
            "MACES (Episode 3) - A Brief Reprieve, Right": 354,
            "Shop - MACES (Episode 3)": (1350, 1351, 1352, 1353, 1354),
        }, shop_setups=["A", "I", "I", "L", "L", "L", "N", "N", "N", "N"]),

        "TYRIAN X (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "TYRIAN X (Episode 3) @ Base Requirements": {
                "TYRIAN X (Episode 3) - First U-Ship Secret": 360,
                "TYRIAN X (Episode 3) - Second Secret, Same as the First": 361,
                "TYRIAN X (Episode 3) - Side-flying Ship Near Landers": 362,
                "TYRIAN X (Episode 3) - Platform Spinner Sequence": 363,
                "TYRIAN X (Episode 3) - Ships Between Platforms": 364,

                "TYRIAN X (Episode 3) @ Tanks Behind Structures": {
                    "TYRIAN X (Episode 3) - Tank Near Purple Structure": 365,
                    "TYRIAN X (Episode 3) - Tank Turn-and-fire Secret": 366,
                },
                "TYRIAN X (Episode 3) @ Pass Boss (can time out)": {
                    "TYRIAN X (Episode 3) - Boss": 367,
                    "Shop - TYRIAN X (Episode 3)": (1360, 1361, 1362, 1363, 1364),
                },
            }
        }, shop_setups=["A", "B", "C", "D", "D", "E", "F", "F", "G", "I"]),

        "SAVARA Y (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "SAVARA Y (Episode 3) - White Formation Leader": 370,
            "SAVARA Y (Episode 3) - Flying Between Huge Planes": 371,
            "SAVARA Y (Episode 3) - Vulcan Plane Set": 372,

            "SAVARA Y (Episode 3) @ Through Blimp Blockade": {
                "SAVARA Y (Episode 3) - Boss Ship Fly-By": 373,

                "SAVARA Y (Episode 3) @ Death Plane Set": {
                    "SAVARA Y (Episode 3) - Death Plane Set, Right": 374,
                    "SAVARA Y (Episode 3) - Death Plane Set, Center": 375,
                },
                "SAVARA Y (Episode 3) @ Pass Boss (can time out)": {
                    "SAVARA Y (Episode 3) - Boss": 376,
                    "Shop - SAVARA Y (Episode 3)": (1370, 1371, 1372, 1373, 1374),
                },
            }
        }, shop_setups=["E", "H", "L", "P"]),

        "NEW DELI (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "NEW DELI (Episode 3) @ Base Requirements": {
                "NEW DELI (Episode 3) - First Turret Wave 1": 380,
                "NEW DELI (Episode 3) - First Turret Wave 2": 381,

                "NEW DELI (Episode 3) @ The Gauntlet Begins": {
                    "NEW DELI (Episode 3) - Second Turret Wave 1": 382,
                    "NEW DELI (Episode 3) - Second Turret Wave 2": 383,
                    "NEW DELI (Episode 3) - Second Turret Wave 3": 384,
                    "NEW DELI (Episode 3) - Second Turret Wave 4": 385,

                    "NEW DELI (Episode 3) @ Destroy Boss": {
                        "NEW DELI (Episode 3) - Boss": 386,
                        "Shop - NEW DELI (Episode 3)": (1380, 1381, 1382, 1383, 1384),
                    },
                }
            }
        }, shop_setups=["K", "M", "O", "P", "Q"]),

        "FLEET (Episode 3)": LevelRegion(episode=Episode.MissionSuicide, locations={
            "FLEET (Episode 3) @ Base Requirements": {
                "FLEET (Episode 3) - Attractor Crane, Entrance": 390,
                "FLEET (Episode 3) - Fire Shooter, Between Ships": 391,
                "FLEET (Episode 3) - Fire Shooter, Near Massive Ship": 392,
                "FLEET (Episode 3) - Attractor Crane, Mid-Fleet": 393,

                "FLEET (Episode 3) @ Destroy Boss": {
                    "FLEET (Episode 3) - Boss": 394,
                    "Shop - FLEET (Episode 3)": (1390, 1391, 1392, 1393, 1394),
                    # Event: "Episode 3 (Mission: Suicide) Complete"
                },
            }
        }, shop_setups=["V", "V", "W", "X"]),

        # =============================================================================================
        # EPISODE 4 - AN END TO FATE
        # =============================================================================================

        "SURFACE (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "SURFACE (Episode 4) - Pulse-Turret Tank": 400,
            "SURFACE (Episode 4) - Grey Fork Ships, Start": 401,
            "SURFACE (Episode 4) - WINDY Warp Orb": 402,
            "SURFACE (Episode 4) - Grey Fork Ships, Line of Three": 403,

            "SURFACE (Episode 4) @ Destroy Mid-Boss": {
                "SURFACE (Episode 4) - Mid-Boss": 404,
                "SURFACE (Episode 4) - Secret Orb Wheel": 405,
                "SURFACE (Episode 4) - Grey Fork Ships, Ending": 406,

                "SURFACE (Episode 4) @ Destroy Hands or Boss": {
                    "SURFACE (Episode 4) - Boss": 407,
                    "Shop - SURFACE (Episode 4)": (1400, 1401, 1402, 1403, 1404),
                }
            }
        }, shop_setups=["B", "B", "C", "D", "E", "E", "F", "G", "J", "M"]),

        "WINDY (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "WINDY (Episode 4) @ Fly Through": {
                "Shop - WINDY (Episode 4)": (1410, 1411, 1412, 1413, 1414),

                "WINDY (Episode 4) @ Destroy Blocks": {
                    "WINDY (Episode 4) - Main Section, Start 1": 410,
                    "WINDY (Episode 4) - Main Section, Start 2": 411,
                    "WINDY (Episode 4) - Main Section, End": 412,

                    "WINDY (Episode 4) @ Reach Extra Section": {
                        "WINDY (Episode 4) - Extra Section, Start": 413,
                        "WINDY (Episode 4) - Extra Section, End": 414,
                    },
                },
            },
        }, shop_setups=["G", "L", "R"]),

        "LAVA RUN (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "LAVA RUN (Episode 4) @ Base Requirements": {
                "LAVA RUN (Episode 4) - Laser Turret": 420,
                "LAVA RUN (Episode 4) - Semi-Guided Missile Launcher": 421,
                "LAVA RUN (Episode 4) - Fan Ships Traversing Screen 1": 422,
                "LAVA RUN (Episode 4) - Fan Ships Traversing Screen 2": 423,

                "LAVA RUN (Episode 4) @ Pass Boss (can time out)": {
                    "LAVA RUN (Episode 4) - Boss": 424,
                    "Shop - LAVA RUN (Episode 4)": (1420, 1421, 1422, 1423, 1424),
                },
            }
        }, shop_setups=["C", "F", "I", "L"]),

        "CORE (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "CORE (Episode 4) @ Starting Section": {
                "CORE (Episode 4) - Orbited by Lava Bubbles, Start": 430,
                "CORE (Episode 4) - Zica Shield Ship, Start": 431,

                "CORE (Episode 4) @ Critical Core": {
                    "CORE (Episode 4) - Zica Shield Ship, Critical Core": 432,
                    "CORE (Episode 4) - Orbited by Lava Bubbles, Critical Core": 433,
                    "CORE (Episode 4) - Critical Core Freebie Item, Left": 434,
                    "CORE (Episode 4) - Critical Core Freebie Item, Right": 435,

                    "CORE (Episode 4) @ Destroy Boss": {
                        "CORE (Episode 4) - Boss": 436,
                        "Shop - CORE (Episode 4)": (1430, 1431, 1432, 1433, 1434),
                    },
                }
            }
        }, shop_setups=["C", "F", "I", "L"]),

        "LAVA EXIT (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "LAVA EXIT (Episode 4) @ Base Requirements": {
                "LAVA EXIT (Episode 4) - Central Lightning Turret": 440,

                "LAVA EXIT (Episode 4) @ Items with Fixed Health": {
                    "LAVA EXIT (Episode 4) - DESERTRUN Warp Orb": 441,
                    "LAVA EXIT (Episode 4) - Clockwise Orb Wheel": 442,
                    "LAVA EXIT (Episode 4) - Final Lava Bubble Assault, Right": 443,
                    "LAVA EXIT (Episode 4) - Final Lava Bubble Assault, Left": 444,
                },
                "LAVA EXIT (Episode 4) @ Pass Boss (can time out)": {
                    "LAVA EXIT (Episode 4) - Boss": 445,
                    "Shop - LAVA EXIT (Episode 4)": (1440, 1441, 1442, 1443, 1444),
                }
            }
        }, shop_setups=["A", "B"]),  # If the planet is actively turning into a sun, perhaps money's not a concern

        "DESERTRUN (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "DESERTRUN (Episode 4) @ Base Requirements": {
                "DESERTRUN (Episode 4) - Oasis": 450,
                "DESERTRUN (Episode 4) - Afterburner Slalom 1": 451,
                "DESERTRUN (Episode 4) - Afterburner Slalom 2": 452,
                "DESERTRUN (Episode 4) - Afterburner Slalom 3": 453,
                "DESERTRUN (Episode 4) - Afterburner Slalom 4": 454,
                "DESERTRUN (Episode 4) - Afterburner Slalom 5": 455,
                "Shop - DESERTRUN (Episode 4)": (1450, 1451, 1452, 1453, 1454),
            },
        }, shop_setups=["A", "B"]),  # As above

        "SIDE EXIT (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "SIDE EXIT (Episode 4) @ Base Requirements": {
                "SIDE EXIT (Episode 4) - Laser Turret, Start": 460,
                "SIDE EXIT (Episode 4) - Fan Ship Wave": 461,
                "SIDE EXIT (Episode 4) - Laser Turret, Final Onslaught": 462,
                "Shop - SIDE EXIT (Episode 4)": (1460, 1461, 1462, 1463, 1464),
            }
        }, shop_setups=["C", "F", "I", "L"]),

        "?TUNNEL? (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "?TUNNEL? (Episode 4) @ Destroy Boss": {
                "?TUNNEL? (Episode 4) - Boss": 470,
                "Shop - ?TUNNEL? (Episode 4)": (1470, 1471, 1472, 1473, 1474),
            },
        }, shop_setups=["M", "M", "M", "S", "S", "S", "W", "W", "W", "Z!"]),

        "ICE EXIT (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "ICE EXIT (Episode 4) @ Base Requirements": {
                "ICE EXIT (Episode 4) - Large Ice Block": 480,
                "ICE EXIT (Episode 4) - Small Ice Block Wave": 481,
                "ICE EXIT (Episode 4) - ICESECRET Warp Orb": 482,

                "ICE EXIT (Episode 4) @ Destroy Boss": {
                    "ICE EXIT (Episode 4) - Boss": 483,
                    "Shop - ICE EXIT (Episode 4)": (1480, 1481, 1482, 1483, 1484),
                },
            }
        }, shop_setups=["F", "I", "L", "O"]),

        "ICESECRET (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "ICESECRET (Episode 4) @ Time Gate, To Station Start": {
                "ICESECRET (Episode 4) - Ice Block, Start": 490,
                "ICESECRET (Episode 4) - Large U-Ship Mid-Boss": 491,
                "ICESECRET (Episode 4) - Ice Block, After Mid-Boss": 492,
                "ICESECRET (Episode 4) - MegaLaser Dual Drop": 493,

                "ICESECRET (Episode 4) @ Time Gate, To Midpoint": {
                    "ICESECRET (Episode 4) - Ice Block, In Camanis Station": 494,
                    "ICESECRET (Episode 4) - Large Lightning Ship": 495,
                    "ICESECRET (Episode 4) - Ice Block, End of Station": 496,
                    "ICESECRET (Episode 4) - SDF Main Gun Drop": 497,

                    "ICESECRET (Episode 4) @ Time Gate, To Ending": {
                        "ICESECRET (Episode 4) - Boss": 498,
                        "Shop - ICESECRET (Episode 4)": (1490, 1491, 1492, 1493, 1494),
                    }
                }
            }
        }, shop_setups=["P", "R", "V", "Y"]),

        "HARVEST (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "HARVEST (Episode 4) @ Base Requirements": {
                "HARVEST (Episode 4) - V Formation, Start": 500,
                "HARVEST (Episode 4) - V Formation, High Speed": 501,
                "HARVEST (Episode 4) - V Formation, Ending": 507,

                "HARVEST (Episode 4) @ Destroy Energy Blasters": {
                    "HARVEST (Episode 4) - Energy Blaster, in Ship Pincer": 502,
                    "HARVEST (Episode 4) - Energy Blaster, with Gravity Orbs": 503,
                    "HARVEST (Episode 4) - Energy Blaster, with Boss Fleet": 504,
                    "HARVEST (Episode 4) - Grounded Energy Blaster 1": 505,
                    "HARVEST (Episode 4) - Grounded Energy Blaster 2": 506,
                },
                "HARVEST (Episode 4) @ Destroy Boss": {
                    "HARVEST (Episode 4) - Boss": 508,
                    "HARVEST (Episode 4) - Post-Boss Platforms": 509,
                    "Shop - HARVEST (Episode 4)": (1500, 1501, 1502, 1503, 1504),
                },
            }
        }, shop_setups=["M", "M", "Q", "S"]),

        "UNDERDELI (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "UNDERDELI (Episode 4) @ Base Requirements": {
                "UNDERDELI (Episode 4) - Missile Bay, Start": 510,
                "UNDERDELI (Episode 4) - Platform Free Item, Speed Up": 511,
                "UNDERDELI (Episode 4) - Missile Bay, After Speed Up": 512,
                "UNDERDELI (Episode 4) - Battle Section Free Item, Left": 513,
                "UNDERDELI (Episode 4) - Battle Section Free Item, Right": 514,
                "UNDERDELI (Episode 4) - Platform Free Item, Ending": 515,
                "UNDERDELI (Episode 4) - Boss's Red Cell": 516,

                "UNDERDELI (Episode 4) @ Pass Boss (can time out)": {
                    "UNDERDELI (Episode 4) - Boss": 517,
                    "Shop - UNDERDELI (Episode 4)": (1510, 1511, 1512, 1513, 1514),
                }
            }
        }, shop_setups=["M", "M", "Q", "S"]),

        "APPROACH (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "APPROACH (Episode 4) @ Base Requirements": {
                "APPROACH (Episode 4) - Solo White Plane": 520,
                "APPROACH (Episode 4) - Brown Planes, Single Helix": 521,
                "APPROACH (Episode 4) - Brown Planes, Double Helix 1": 522,
                "APPROACH (Episode 4) - Brown Planes, Double Helix 2": 523,

                "APPROACH (Episode 4) @ Destroy Boss Orb": {
                    "APPROACH (Episode 4) - Boss Orb": 524,
                    "Shop - APPROACH (Episode 4)": (1520, 1521, 1522, 1523, 1524),
                }
            }
        }, shop_setups=["K", "L", "N", "R"]),

        "SAVARA IV (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "SAVARA IV (Episode 4) - White Formation Leader, Start": 530,
            "SAVARA IV (Episode 4) - White Formation Leader, Middle": 532,

            "SAVARA IV (Episode 4) @ Destroy Drunk Planes": {
                "SAVARA IV (Episode 4) - Drunk Plane, Middle": 531,
                "SAVARA IV (Episode 4) - Drunk Plane, Ending": 533,
            },
            "SAVARA IV (Episode 4) @ Pass Boss (can time out)": {
                "SAVARA IV (Episode 4) - Boss": 534,
                "Shop - SAVARA IV (Episode 4)": (1530, 1531, 1532, 1533, 1534),
            }
        }, shop_setups=["K", "L", "N", "R"]),

        "DREAD-NOT (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "DREAD-NOT (Episode 4) @ Destroy Boss": {
                "DREAD-NOT (Episode 4) - Boss": 540,
                "Shop - DREAD-NOT (Episode 4)": (1540, 1541, 1542, 1543, 1544),
            }
        }, shop_setups=["W"]),

        "EYESPY (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "EYESPY (Episode 4) @ Base Requirements": {
                "EYESPY (Episode 4) - Green Exploding Eye": 550,
                "EYESPY (Episode 4) - Blue Splitting Eye, Start": 551,
                "EYESPY (Episode 4) - Blue Splitting Eye, Middle": 552,
                "EYESPY (Episode 4) - Guarded Green Eye, Static": 553,
                "EYESPY (Episode 4) - Guarded Green Eye, Swaying": 554,
                "EYESPY (Episode 4) - Billiard Break Secret": 555,

                "EYESPY (Episode 4) @ Destroy Boss": {
                    "EYESPY (Episode 4) - Boss": 556,
                    "Shop - EYESPY (Episode 4)": (1550, 1551, 1552, 1553, 1554),
                }
            }
        }, shop_setups=["Q", "T", "T", "U", "U", "V"]),

        "BRAINIAC (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "BRAINIAC (Episode 4) @ Base Requirements": {
                "BRAINIAC (Episode 4) - Alcove at Start": 560,
                "BRAINIAC (Episode 4) - Second Alcove": 561,
                "BRAINIAC (Episode 4) - Turret-Guarded Pathway": 562,
                "BRAINIAC (Episode 4) - Protron Spreader": 563,
                "BRAINIAC (Episode 4) - Fire Mid-Boss": 564,
                "BRAINIAC (Episode 4) - Rolling Orb Wheel": 565,
                "BRAINIAC (Episode 4) - Ice Mid-Boss": 566,
                "BRAINIAC (Episode 4) - Turret Before Boss": 567,

                "BRAINIAC (Episode 4) @ Destroy Boss": {
                    "BRAINIAC (Episode 4) - Boss": 568,
                    "Shop - BRAINIAC (Episode 4)": (1560, 1561, 1562, 1563, 1564),
                }
            }
        }, shop_setups=["Q", "T", "T", "U", "U", "V"]),

        "NOSE DRIP (Episode 4)": LevelRegion(episode=Episode.AnEndToFate, locations={
            "NOSE DRIP (Episode 4) @ Destroy Boss": {
                "NOSE DRIP (Episode 4) - Boss": 570,
                "Shop - NOSE DRIP (Episode 4)": (1570, 1571, 1572, 1573, 1574),
                # Event: "Episode 4 (An End To Fate) Complete"
            },
        }, shop_setups=["W", "X", "X", "Y"]),

        # =============================================================================================
        # EPISODE 5 - HAZUDRA FODDER
        # =============================================================================================

        "ASTEROIDS (Episode 5)": LevelRegion(episode=Episode.HazudraFodder, locations={
            "ASTEROIDS (Episode 5) - Claw Ship Wave, Start": 580,
            "ASTEROIDS (Episode 5) - Railgunner, Start": 582,
            "ASTEROIDS (Episode 5) - Railgunner, Before Bubble Section": 584,
            "ASTEROIDS (Episode 5) - Claw Ship Wave, Ending": 586,

            "ASTEROIDS (Episode 5) @ Destroy Spinning Orbs": {
                "ASTEROIDS (Episode 5) - Spinning Orbs, Start": 581,
                "ASTEROIDS (Episode 5) - Spinning Orbs, Before Bubble Section": 583,
                "ASTEROIDS (Episode 5) - Spinning Orbs, Ending": 585,
            },
            "ASTEROIDS (Episode 5) @ Destroy Boss": {
                "ASTEROIDS (Episode 5) - Boss": 587,
                "Shop - ASTEROIDS (Episode 5)": (1580, 1581, 1582, 1583, 1584),
            }
        }, shop_setups=["A", "B", "C", "D", "D", "E", "F", "F", "G", "I"]),

        "AST ROCK (Episode 5)": LevelRegion(episode=Episode.HazudraFodder, locations={
            "AST ROCK (Episode 5) @ Base Requirements": {
                "AST ROCK (Episode 5) - Solitary Plasma Turret": 590,
                "AST ROCK (Episode 5) - Red Shield Ship 1": 591,
                "AST ROCK (Episode 5) - Warehouse Colony, Bottom": 592,
                "AST ROCK (Episode 5) - Warehouse Colony, Top-Left": 593,
                "AST ROCK (Episode 5) - Warehouse Colony, Top-Right": 594,
                "AST ROCK (Episode 5) - Red Shield Ship 2": 595,
                "AST ROCK (Episode 5) - Missile Ship": 596,
                "AST ROCK (Episode 5) - Red Shield Ship 3": 597,

                "AST ROCK (Episode 5) @ Destroy Boss": {
                    "AST ROCK (Episode 5) - Boss": 598,
                    "Shop - AST ROCK (Episode 5)": (1590, 1591, 1592, 1593, 1594),
                }
            }
        }, shop_setups=["D", "E", "G", "K", "L"]),

        "MINERS (Episode 5)": LevelRegion(episode=Episode.HazudraFodder, locations={
            "MINERS (Episode 5) @ Base Requirements": {
                "MINERS (Episode 5) - Rock Hauler": 600,
                "MINERS (Episode 5) - Bat-Ship Guarded By Rocks": 602,
                "MINERS (Episode 5) - Monorail Train": 603,
                "MINERS (Episode 5) - UFO Turret, Ending": 605,

                "MINERS (Episode 5) @ Destroy Missile Launchers": {
                    "MINERS (Episode 5) - Missile Launcher, Start": 601,
                    "MINERS (Episode 5) - Missile Launcher, Dodging Rocks": 604,
                },
                "MINERS (Episode 5) @ Pass Boss (can time out)": {
                    "MINERS (Episode 5) - Boss": 606,
                    "Shop - MINERS (Episode 5)": (1600, 1601, 1602, 1603, 1604),
                }
            }
        }, shop_setups=["D", "E", "G", "K", "L"]),

        "SAVARA (Episode 5)": LevelRegion(episode=Episode.HazudraFodder, locations={
            "SAVARA (Episode 5) @ Destroy Most Planes": {
                "SAVARA (Episode 5) - Vulcan Plane, Start": 610,
                "SAVARA (Episode 5) - Brown Plane Sequence": 612,
                "SAVARA (Episode 5) - Vulcan Plane, Boxed In": 613,
                "SAVARA (Episode 5) - White Formation Leader": 614,
                "SAVARA (Episode 5) - Vulcan Plane, Before Speed Up": 616,
                "SAVARA (Episode 5) - Green Plane, End of Speed Up": 617,
            },
            "SAVARA (Episode 5) @ Destroy Huge Planes": {
                "SAVARA (Episode 5) - Huge Planes, Start": 611,
                "SAVARA (Episode 5) - Huge Planes, Halfway": 615,
            },
            "SAVARA (Episode 5) @ Pass Boss (can time out)": {
                "SAVARA (Episode 5) - Boss": 618,
                "Shop - SAVARA (Episode 5)": (1610, 1611, 1612, 1613, 1614),
            },
        }, shop_setups=["F", "H", "J", "M", "N"]),

        "CORAL (Episode 5)": LevelRegion(episode=Episode.HazudraFodder, locations={
            "CORAL (Episode 5) - Breakaway Dolphin": 620,

            "CORAL (Episode 5) @ After Opening": {
                "CORAL (Episode 5) - Lightning Stingray, Near Seahorses": 621,
                "CORAL (Episode 5) - Protron Eel, Near Seahorses 1": 622,
                "CORAL (Episode 5) - Protron Eel, Near Seahorses 2": 623,

                "CORAL (Episode 5) @ Pass Starfish": {
                    "CORAL (Episode 5) - Protron Eel, Near Starfish": 624,
                    "CORAL (Episode 5) - Lightning Stingray, Near Starfish": 625,
                    "CORAL (Episode 5) - High Speed Submarine": 626,

                    "CORAL (Episode 5) @ Destroy Boss": {
                        "CORAL (Episode 5) - Boss": 627,
                        "Shop - CORAL (Episode 5)": (1620, 1621, 1622, 1623, 1624),
                    },
                }
            }
        }, shop_setups=["F", "H", "J", "M", "N"]),

        # Remains here for possible future use (corresponds to unused level)
#       "CANYONRUN (Episode 5)": LevelRegion(episode=Episode.HazudraFodder, locations={
#           "Shop - CANYONRUN (Episode 5)": (1630, 1631, 1632, 1633, 1634),
#       }, shop_setups=[])

        "STATION (Episode 5)": LevelRegion(episode=Episode.HazudraFodder, locations={
            "STATION (Episode 5) @ Base Requirements": {
                "STATION (Episode 5) - Pulse-Turret, Platform Ship Wave 1": 640,
                "STATION (Episode 5) - Pulse-Turret, Platform Ship Wave 2": 641,
                "STATION (Episode 5) - Pulse-Turret, Long Spike Wave": 642,
                "STATION (Episode 5) - Spike, Bottom-Right Corner": 643,
                "STATION (Episode 5) - Pulse-Turret, Drill Wave": 644,
                "STATION (Episode 5) - Spike, Bottom-Left Corner": 645,

                "STATION (Episode 5) @ Survive Crane": {
                    "STATION (Episode 5) - Attractor Crane": 646,
                    "STATION (Episode 5) - Pulse-Turret, With Crane 1": 647,
                    "STATION (Episode 5) - Pulse-Turret, With Crane 2": 648,

                    "STATION (Episode 5) @ Pass Boss (can time out)": {
                        "STATION (Episode 5) - Boss": 649,
                        "Shop - STATION (Episode 5)": (1640, 1641, 1642, 1643, 1644),
                    },
                }
            }
        }, shop_setups=["J", "P", "Q"]),

        "FRUIT (Episode 5)": LevelRegion(episode=Episode.HazudraFodder, locations={
            "FRUIT (Episode 5) @ Base Requirements": {
                "FRUIT (Episode 5) - Apple UFO Wave, Start": 650,
                "FRUIT (Episode 5) - Cherry Stealth Ship": 651,
                "FRUIT (Episode 5) - Banana Blaster Ship": 652,
                "FRUIT (Episode 5) - Apple UFO Wave, Ending": 653,

                "FRUIT (Episode 5) @ Destroy Boss": {
                    "FRUIT (Episode 5) - Boss": 654,
                    "Shop - FRUIT (Episode 5)": (1650, 1651, 1652, 1653, 1654),
                    # Event: "Episode 5 (Hazudra Fodder) Complete"
                }
            }
        }, shop_setups=["S"]),
    }

    # Events for game completion
    events: dict[str, str] = {
        "Episode 1 (Escape) Complete":           "ASSASSIN (Episode 1)",
        "Episode 2 (Treachery) Complete":        "GRYPHON (Episode 2)",
        "Episode 3 (Mission: Suicide) Complete": "FLEET (Episode 3)",
        "Episode 4 (An End to Fate) Complete":   "NOSE DRIP (Episode 4)",
        "Episode 5 (Hazudra Fodder) Complete":   "FRUIT (Episode 5)",
    }

    @classmethod
    def get_location_name_to_id(cls, base_id: int) -> dict[str, int]:
        all_locs = {}
        for region in cls.level_regions.values():
            all_locs.update(region.get_locations(base_id=base_id))
        return all_locs

    @classmethod
    def get_location_groups(cls) -> dict[str, set[str]]:
        # Bring all locations in a level, shop included, into a region named after the level.
        return {level: region.get_location_names() for (level, region) in cls.level_regions.items()}
