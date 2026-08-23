from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items

if TYPE_CHECKING:
    from .world import UncannyCatWorld

BASE_ID = 100

# name -> (id, list of gimmick items logically required to reach the check)
LOCATION_DATA: dict[str, tuple[int, list[str]]] = {
    "0-1: Welcome to UNCANNY CAT GOLF! Complete": (BASE_ID + 0, []),
    "0-1: Welcome to UNCANNY CAT GOLF! Peak Rank": (BASE_ID + 1000, []),
    "0-1: Welcome to UNCANNY CAT GOLF! Good Rank": (BASE_ID + 3000, []),
    "0-2: Hello Walls Complete": (BASE_ID + 1, []),
    "0-2: Hello Walls Peak Rank": (BASE_ID + 1001, []),
    "0-2: Hello Walls Good Rank": (BASE_ID + 3001, []),
    "0-3: Meet the Slopes Complete": (BASE_ID + 2, []),
    "0-3: Meet the Slopes Peak Rank": (BASE_ID + 1002, []),
    "0-3: Meet the Slopes Good Rank": (BASE_ID + 3002, []),
    "0-4: Pretty Pennies Complete": (BASE_ID + 3, []),
    "0-4: Pretty Pennies Peak Rank": (BASE_ID + 1003, []),
    "0-4: Pretty Pennies Good Rank": (BASE_ID + 3003, []),
    "0-5: Onward and Golfward! Complete": (BASE_ID + 4, []),
    "0-5: Onward and Golfward! Peak Rank": (BASE_ID + 1004, []),
    "0-5: Onward and Golfward! Good Rank": (BASE_ID + 3004, []),

    "1-1: Welcome to GOLF CENTRAL! Complete": (BASE_ID + 100, []),
    "1-1: Welcome to GOLF CENTRAL! Peak Rank": (BASE_ID + 1100, []),
    "1-1: Welcome to GOLF CENTRAL! Good Rank": (BASE_ID + 3100, []),
    "1-2: Getting Around Complete": (BASE_ID + 101, []),
    "1-2: Getting Around Peak Rank": (BASE_ID + 1101, []),
    "1-2: Getting Around Good Rank": (BASE_ID + 3101, []),
    "1-3: A New Angle Complete": (BASE_ID + 102, []),
    "1-3: A New Angle Peak Rank": (BASE_ID + 1102, []),
    "1-3: A New Angle Good Rank": (BASE_ID + 3102, []),
    "1-4: Breakthrough! Complete": (BASE_ID + 103, ["Breakable Tiles"]),
    "1-4: Breakthrough! Peak Rank": (BASE_ID + 1103, ["Breakable Tiles"]),
    "1-4: Breakthrough! Good Rank": (BASE_ID + 3103, ["Breakable Tiles"]),
    "1-5: Right up my Alley Complete": (BASE_ID + 104, ["Breakable Tiles"]),
    "1-5: Right up my Alley Peak Rank": (BASE_ID + 1104, ["Breakable Tiles"]),
    "1-5: Right up my Alley Good Rank": (BASE_ID + 3104, ["Breakable Tiles"]),
    "1-6: Roundabout Complete": (BASE_ID + 105, ["Breakable Tiles"]),
    "1-6: Roundabout Peak Rank": (BASE_ID + 1105, ["Breakable Tiles"]),
    "1-6: Roundabout Good Rank": (BASE_ID + 3105, ["Breakable Tiles"]),
    "1-7: Bunker Funk Complete": (BASE_ID + 106, ["Breakable Tiles"]),
    "1-7: Bunker Funk Peak Rank": (BASE_ID + 1106, ["Breakable Tiles"]),
    "1-7: Bunker Funk Good Rank": (BASE_ID + 3106, ["Breakable Tiles"]),
    "1-8: Bony Cronies Complete": (BASE_ID + 107, []),
    "1-8: Bony Cronies Peak Rank": (BASE_ID + 1107, []),
    "1-8: Bony Cronies Good Rank": (BASE_ID + 3107, []),
    "1-9: Kitty Litter Complete": (BASE_ID + 108, []),
    "1-9: Kitty Litter Peak Rank": (BASE_ID + 1108, []),
    "1-9: Kitty Litter Good Rank": (BASE_ID + 3108, []),
    "1-10: Double Trouble Complete": (BASE_ID + 109, []),
    "1-10: Double Trouble Peak Rank": (BASE_ID + 1109, []),
    "1-10: Double Trouble Good Rank": (BASE_ID + 3109, []),
    "1-11: Triple Trouble Complete": (BASE_ID + 110, []),
    "1-11: Triple Trouble Peak Rank": (BASE_ID + 1110, []),
    "1-11: Triple Trouble Good Rank": (BASE_ID + 3110, []),
    "1-12: An Absurd Amount of Trouble Complete": (BASE_ID + 111, []),
    "1-12: An Absurd Amount of Trouble Peak Rank": (BASE_ID + 1111, []),
    "1-12: An Absurd Amount of Trouble Good Rank": (BASE_ID + 3111, []),
    "1-13: The Key to Success Complete": (BASE_ID + 112, ["Keys"]),
    "1-13: The Key to Success Peak Rank": (BASE_ID + 1112, ["Keys"]),
    "1-13: The Key to Success Good Rank": (BASE_ID + 3112, ["Keys"]),
    "1-14: Ooooh, Pretty Colors Complete": (BASE_ID + 113, ["Keys"]),
    "1-14: Ooooh, Pretty Colors Peak Rank": (BASE_ID + 1113, ["Keys"]),
    "1-14: Ooooh, Pretty Colors Good Rank": (BASE_ID + 3113, ["Keys"]),
    "1-15: Almost a Cakewalk Complete": (BASE_ID + 114, ["Keys"]),
    "1-15: Almost a Cakewalk Peak Rank": (BASE_ID + 1114, ["Keys"]),
    "1-15: Almost a Cakewalk Good Rank": (BASE_ID + 3114, ["Keys"]),
    "1-16: Silly Yard Complete": (BASE_ID + 115, ["Keys"]),
    "1-16: Silly Yard Peak Rank": (BASE_ID + 1115, ["Keys"]),
    "1-16: Silly Yard Good Rank": (BASE_ID + 3115, ["Keys"]),
    "1-17: Scattered Around Complete": (BASE_ID + 116, ["Keys"]),
    "1-17: Scattered Around Peak Rank": (BASE_ID + 1116, ["Keys"]),
    "1-17: Scattered Around Good Rank": (BASE_ID + 3116, ["Keys"]),
    "1-18: Rest Stop Complete": (BASE_ID + 117, []),
    "1-18: Rest Stop Peak Rank": (BASE_ID + 1117, []),
    "1-18: Rest Stop Good Rank": (BASE_ID + 3117, []),

    "2-1: Welcome to GLOWSTICK CITY! Complete": (BASE_ID + 200, []),
    "2-1: Welcome to GLOWSTICK CITY! Peak Rank": (BASE_ID + 1200, []),
    "2-1: Welcome to GLOWSTICK CITY! Good Rank": (BASE_ID + 3200, []),
    "2-2: Stop Right There! Complete": (BASE_ID + 201, []),
    "2-2: Stop Right There! Peak Rank": (BASE_ID + 1201, []),
    "2-2: Stop Right There! Good Rank": (BASE_ID + 3201, []),
    "2-3: Parking Lot Complete": (BASE_ID + 202, []),
    "2-3: Parking Lot Peak Rank": (BASE_ID + 1202, []),
    "2-3: Parking Lot Good Rank": (BASE_ID + 3202, []),
    "2-4: Just Zoomin' By Complete": (BASE_ID + 203, []),
    "2-4: Just Zoomin' By Peak Rank": (BASE_ID + 1203, ["Go Markers"]),
    "2-4: Just Zoomin' By Good Rank": (BASE_ID + 3203, []),
    "2-5: Stop 'n' Start Complete": (BASE_ID + 204, ["Keys"]),
    "2-5: Stop 'n' Start Peak Rank": (BASE_ID + 1204, ["Keys", "Go Markers", "Stop Markers"]),
    "2-5: Stop 'n' Start Good Rank": (BASE_ID + 3204, ["Keys", "Go Markers", "Stop Markers"]),
    "2-6: Backstreet Skullz Complete": (BASE_ID + 205, ["Breakable Tiles"]),
    "2-6: Backstreet Skullz Peak Rank": (BASE_ID + 1205, ["Breakable Tiles", "Go Markers", "Stop Markers"]),
    "2-6: Backstreet Skullz Good Rank": (BASE_ID + 3205, ["Breakable Tiles", "Go Markers", "Stop Markers"]),
    "2-7: Look Both Ways Complete": (BASE_ID + 206, []),
    "2-7: Look Both Ways Peak Rank": (BASE_ID + 1206, []),
    "2-7: Look Both Ways Good Rank": (BASE_ID + 3206, []),
    "2-8: Dimlit District Complete": (BASE_ID + 207, ["Breakable Tiles"]),
    "2-8: Dimlit District Peak Rank": (BASE_ID + 1207, ["Breakable Tiles", "Stop Markers", "Go Markers"]),
    "2-8: Dimlit District Good Rank": (BASE_ID + 3207, ["Breakable Tiles", "Stop Markers", "Go Markers"]),
    "2-9: This is A Mugging Complete": (BASE_ID + 208, []),
    "2-9: This is A Mugging Peak Rank": (BASE_ID + 1208, ["Stop Markers", "Go Markers"]),
    "2-9: This is A Mugging Good Rank": (BASE_ID + 3208, ["Stop Markers", "Go Markers"]),
    "2-10: jump pad introductary level Complete": (BASE_ID + 209, ["Jump Pads"]),
    "2-10: jump pad introductary level Peak Rank": (BASE_ID + 1209, ["Jump Pads"]),
    "2-10: jump pad introductary level Good Rank": (BASE_ID + 3209, ["Jump Pads"]),
    "2-11: Heist To Meet You Complete": (BASE_ID + 210, ["Keys", "Breakable Tiles", "Jump Pads", "Go Markers"]),
    "2-11: Heist To Meet You Peak Rank": (BASE_ID + 1210, ["Keys", "Breakable Tiles", "Jump Pads", "Go Markers"]),
    "2-11: Heist To Meet You Good Rank": (BASE_ID + 3210, ["Keys", "Breakable Tiles", "Jump Pads", "Go Markers"]),
    "2-12: Highway Getaway! Complete": (BASE_ID + 211, []),
    "2-12: Highway Getaway! Peak Rank": (BASE_ID + 1211, []),
    "2-12: Highway Getaway! Good Rank": (BASE_ID + 3211, []),
    "2-13: Brawl In The Big City Complete": (BASE_ID + 212, ["Keys", "Jump Pads"]),
    "2-13: Brawl In The Big City Peak Rank": (BASE_ID + 1212, ["Keys", "Jump Pads", "Stop Markers"]),
    "2-13: Brawl In The Big City Good Rank": (BASE_ID + 3212, ["Keys", "Jump Pads", "Stop Markers"]),
    "2-14: Waiter! There's Slop In My Soup! Complete": (BASE_ID + 213, ["Keys"]),
    "2-14: Waiter! There's Slop In My Soup! Peak Rank": (
        BASE_ID + 1213,
        ["Keys", "Breakable Tiles", "Jump Pads", "Go Markers", "Stop Markers"],
    ),
    "2-14: Waiter! There's Slop In My Soup! Good Rank": (
        BASE_ID + 3213,
        ["Keys", "Breakable Tiles", "Jump Pads", "Go Markers", "Stop Markers"],
    ),
    "2-15: Back In The Back Alley Complete": (BASE_ID + 214, ["Keys", "Jump Pads"]),
    "2-15: Back In The Back Alley Peak Rank": (BASE_ID + 1214, ["Keys", "Jump Pads", "Stop Markers"]),
    "2-15: Back In The Back Alley Good Rank": (BASE_ID + 3214, ["Keys", "Jump Pads", "Stop Markers"]),
    "2-16: Trickshot! Complete": (BASE_ID + 215, ["Jump Pads"]),
    "2-16: Trickshot! Peak Rank": (BASE_ID + 1215, ["Jump Pads", "Stop Markers", "Go Markers"]),
    "2-16: Trickshot! Good Rank": (BASE_ID + 3215, ["Jump Pads", "Stop Markers", "Go Markers"]),
    "2-17: Baby Vegas Complete": (BASE_ID + 216, ["Keys", "Jump Pads"]),
    "2-17: Baby Vegas Peak Rank": (BASE_ID + 1216, ["Keys", "Jump Pads", "Stop Markers"]),
    "2-17: Baby Vegas Good Rank": (BASE_ID + 3216, ["Keys", "Jump Pads", "Stop Markers"]),
    "2-18: Good Night, Glowstick City Complete": (BASE_ID + 217, ["Jump Pads"]),
    "2-18: Good Night, Glowstick City Peak Rank": (BASE_ID + 1217, ["Jump Pads"]),
    "2-18: Good Night, Glowstick City Good Rank": (BASE_ID + 3217, ["Jump Pads"]),

    "3-1: Welcome to CHUCKLE PARK! Complete": (BASE_ID + 300, []),
    "3-1: Welcome to CHUCKLE PARK! Peak Rank": (BASE_ID + 1300, []),
    "3-1: Welcome to CHUCKLE PARK! Good Rank": (BASE_ID + 3300, []),
    "3-1: Welcome to CHUCKLE PARK! Yellow Smiley": (BASE_ID + 2303, []),
    "3-2: Chuckle-Go-Round Complete": (BASE_ID + 301, ["Breakable Tiles"]),
    "3-2: Chuckle-Go-Round Peak Rank": (BASE_ID + 1301, ["Breakable Tiles", "Stop Markers"]),
    "3-2: Chuckle-Go-Round Good Rank": (BASE_ID + 3301, ["Breakable Tiles", "Stop Markers"]),
    "3-2: Chuckle-Go-Round Yellow Smiley": (BASE_ID + 2308, []),
    "3-3: Switch It Up! Complete": (BASE_ID + 302, ["Switch Tiles"]),
    "3-3: Switch It Up! Peak Rank": (BASE_ID + 1302, ["Switch Tiles"]),
    "3-3: Switch It Up! Good Rank": (BASE_ID + 3302, ["Switch Tiles"]),
    "3-4: JumbleHouse Complete": (BASE_ID + 303, ["Switch Tiles"]),
    "3-4: JumbleHouse Peak Rank": (BASE_ID + 1303, ["Switch Tiles"]),
    "3-4: JumbleHouse Good Rank": (BASE_ID + 3303, ["Switch Tiles"]),
    "3-5: Titular Chuckles Complete": (BASE_ID + 304, ["Keys"]),
    "3-5: Titular Chuckles Peak Rank": (BASE_ID + 1304, ["Keys", "Breakable Tiles"]),
    "3-5: Titular Chuckles Good Rank": (BASE_ID + 3304, ["Keys", "Breakable Tiles"]),
    "3-5: Titular Chuckles Yellow Smiley": (BASE_ID + 2323, []),
    "3-6: Cleanup On Aisle 2! Complete": (BASE_ID + 305, ["Breakable Tiles"]),
    "3-6: Cleanup On Aisle 2! Peak Rank": (BASE_ID + 1305, ["Breakable Tiles"]),
    "3-6: Cleanup On Aisle 2! Good Rank": (BASE_ID + 3305, ["Breakable Tiles"]),
    "3-7: Chuckles Inc. Complete": (BASE_ID + 306, ["Keys"]),
    "3-7: Chuckles Inc. Peak Rank": (BASE_ID + 1306, ["Keys", "Jump Pads", "Stop Markers", "Go Markers"]),
    "3-7: Chuckles Inc. Good Rank": (BASE_ID + 3306, ["Keys", "Jump Pads", "Stop Markers", "Go Markers"]),
    "3-7: Chuckles Inc. Yellow Smiley": (BASE_ID + 2333, ["Keys", "Stop Markers"]),
    "3-8: How Many Licks... Complete": (BASE_ID + 307, ["Breakable Tiles"]),
    "3-8: How Many Licks... Peak Rank": (BASE_ID + 1307, ["Breakable Tiles"]),
    "3-8: How Many Licks... Good Rank": (BASE_ID + 3307, ["Breakable Tiles"]),
    "3-9: House of Mirrors Complete": (BASE_ID + 308, ["Breakable Tiles"]),
    "3-9: House of Mirrors Peak Rank": (BASE_ID + 1308, ["Breakable Tiles"]),
    "3-9: House of Mirrors Good Rank": (BASE_ID + 3308, ["Breakable Tiles"]),
    "3-10: You Bring a Light? Complete": (BASE_ID + 309, []),
    "3-10: You Bring a Light? Peak Rank": (BASE_ID + 1309, []),
    "3-10: You Bring a Light? Good Rank": (BASE_ID + 3309, []),
    "3-11: Four Leaf Marathon Complete": (BASE_ID + 310, ["Keys", "Jump Pads"]),
    "3-11: Four Leaf Marathon Peak Rank": (BASE_ID + 1310, ["Keys", "Jump Pads"]),
    "3-11: Four Leaf Marathon Good Rank": (BASE_ID + 3310, ["Keys", "Jump Pads"]),
    "3-11: Four Leaf Marathon Red Smiley": (BASE_ID + 2350, []),
    "3-11: Four Leaf Marathon Green Smiley": (BASE_ID + 2351, []),
    "3-11: Four Leaf Marathon Blue Smiley": (BASE_ID + 2352, []),
    "3-11: Four Leaf Marathon Yellow Smiley": (BASE_ID + 2353, ["Keys", "Jump Pads"]),
    "3-12: Pursuit of Happiness Complete": (BASE_ID + 311, ["Switch Tiles"]),
    "3-12: Pursuit of Happiness Peak Rank": (BASE_ID + 1311, ["Switch Tiles", "Stop Markers", "Go Markers"]),
    "3-12: Pursuit of Happiness Good Rank": (BASE_ID + 3311, ["Switch Tiles", "Stop Markers", "Go Markers"]),
    "3-12: Pursuit of Happiness Red Smiley": (BASE_ID + 2355, []),
    "3-12: Pursuit of Happiness Green Smiley": (BASE_ID + 2356, ["Switch Tiles"]),
    "3-12: Pursuit of Happiness Blue Smiley": (BASE_ID + 2357, ["Switch Tiles"]),
    "3-12: Pursuit of Happiness Yellow Smiley": (BASE_ID + 2358, ["Switch Tiles"]),
    "3-12: Pursuit of Happiness Orange Smiley": (BASE_ID + 2359, ["Switch Tiles", "Go Markers", "Stop Markers"]),
    "3-13: UNCANNY DOG GOLF Complete": (BASE_ID + 312, ["Dog", "Switch Tiles"]),
    "3-13: UNCANNY DOG GOLF Peak Rank": (BASE_ID + 1312, ["Dog", "Switch Tiles"]),
    "3-13: UNCANNY DOG GOLF Good Rank": (BASE_ID + 3312, ["Dog", "Switch Tiles"]),
    "3-14: Canny's Best Friend Complete": (BASE_ID + 313, ["Dog"]),
    "3-14: Canny's Best Friend Peak Rank": (BASE_ID + 1313, ["Dog", "Switch Tiles"]),
    "3-14: Canny's Best Friend Good Rank": (BASE_ID + 3313, ["Dog", "Switch Tiles"]),
    "3-15: UNCANNY DOG GOLF but with a cat instead of a dog Complete": (BASE_ID + 314, ["Dog", "Switch Tiles"]),
    "3-15: UNCANNY DOG GOLF but with a cat instead of a dog Peak Rank": (BASE_ID + 1314, ["Dog", "Switch Tiles"]),
    "3-15: UNCANNY DOG GOLF but with a cat instead of a dog Good Rank": (BASE_ID + 3314, ["Dog", "Switch Tiles"]),
    "3-16: He Shoots! He scores! Complete": (BASE_ID + 315, ["Dog"]),
    "3-16: He Shoots! He scores! Peak Rank": (BASE_ID + 1315, ["Dog"]),
    "3-16: He Shoots! He scores! Good Rank": (BASE_ID + 3315, ["Dog"]),
    "3-16: He Shoots! He scores! Red Smiley": (BASE_ID + 2375, ["Dog"]),
    "3-17: Racetrack Chasetrack Complete": (BASE_ID + 316, ["Keys", "Dog", "Jump Pads"]),
    "3-17: Racetrack Chasetrack Peak Rank": (BASE_ID + 1316, ["Keys", "Dog", "Jump Pads", "Stop Markers"]),
    "3-17: Racetrack Chasetrack Good Rank": (BASE_ID + 3316, ["Keys", "Dog", "Jump Pads", "Stop Markers"]),
    "3-17: Racetrack Chasetrack Blue Smiley": (BASE_ID + 2382, ["Dog", "Jump Pads"]),
    "3-17: Racetrack Chasetrack Yellow Smiley": (BASE_ID + 2383, ["Dog", "Jump Pads"]),
    "3-18: The Chuckle Coaster Complete": (BASE_ID + 317, ["Jump Pads"]),
    "3-18: The Chuckle Coaster Peak Rank": (BASE_ID + 1317, ["Jump Pads"]),
    "3-18: The Chuckle Coaster Good Rank": (BASE_ID + 3317, ["Jump Pads"]),

    "4-1: Welcome to THE FINAL FRONTIER. Complete": (BASE_ID + 400, []),
    "4-1: Welcome to THE FINAL FRONTIER. Peak Rank": (BASE_ID + 1400, []),
    "4-1: Welcome to THE FINAL FRONTIER. Good Rank": (BASE_ID + 3400, []),
    "4-2: No Time 4 Messing Around Complete": (BASE_ID + 401, ["Switch Tiles"]),
    "4-2: No Time 4 Messing Around Peak Rank": (BASE_ID + 1401, ["Switch Tiles"]),
    "4-2: No Time 4 Messing Around Good Rank": (BASE_ID + 3401, ["Switch Tiles"]),
    "4-3: Now You're Thinking With Portal Complete": (BASE_ID + 402, ["Portals"]),
    "4-3: Now You're Thinking With Portal Peak Rank": (BASE_ID + 1402, ["Portals"]),
    "4-3: Now You're Thinking With Portal Good Rank": (BASE_ID + 3402, ["Portals"]),
    "4-4: Wholesome DIY Complete": (BASE_ID + 403, ["Portals"]),
    "4-4: Wholesome DIY Peak Rank": (BASE_ID + 1403, ["Portals"]),
    "4-4: Wholesome DIY Good Rank": (BASE_ID + 3403, ["Portals"]),
    "4-5: Cube Town Complete": (BASE_ID + 404, ["Switch Tiles"]),
    "4-5: Cube Town Peak Rank": (BASE_ID + 1404, ["Switch Tiles"]),
    "4-5: Cube Town Good Rank": (BASE_ID + 3404, ["Switch Tiles"]),
    "4-6: Jumbling Labrynth Complete": (BASE_ID + 405, ["Portals", "Jump Pads"]),
    "4-6: Jumbling Labrynth Peak Rank": (BASE_ID + 1405, ["Portals", "Jump Pads"]),
    "4-6: Jumbling Labrynth Good Rank": (BASE_ID + 3405, ["Portals", "Jump Pads"]),
    "4-7: Production Room Complete": (BASE_ID + 406, ["Dog"]),
    "4-7: Production Room Peak Rank": (BASE_ID + 1406, ["Dog", "Jump Pads", "Go Markers"]),
    "4-7: Production Room Good Rank": (BASE_ID + 3406, ["Dog", "Jump Pads", "Go Markers"]),
    "4-8: On Heavens No The Chuckles Are Plentiful Complete": (BASE_ID + 407, ["Nuke", "Stop Markers", "Switch Tiles"]),
    "4-8: On Heavens No The Chuckles Are Plentiful Peak Rank": (BASE_ID + 1407, ["Nuke", "Stop Markers", "Switch Tiles"]),
    "4-8: On Heavens No The Chuckles Are Plentiful Good Rank": (BASE_ID + 3407, ["Nuke", "Stop Markers", "Switch Tiles"]),
    "4-9: Uncanny Valley Complete": (BASE_ID + 408, ["Jump Pads", "Stop Markers", "Keys", "Nuke"]),
    "4-9: Uncanny Valley Peak Rank": (BASE_ID + 1408, ["Jump Pads", "Stop Markers"]),
    "4-9: Uncanny Valley Good Rank": (BASE_ID + 3408, ["Jump Pads", "Stop Markers"]),
    "4-10: Dog Patrol Complete": (BASE_ID + 409, ["Dog"]),
    "4-10: Dog Patrol Peak Rank": (BASE_ID + 1409, ["Dog"]),
    "4-10: Dog Patrol Good Rank": (BASE_ID + 3409, ["Dog"]),
    "4-11: The Really Cool Mining Level Complete": (BASE_ID + 410, ["Dog", "Breakable Tiles"]),
    "4-11: The Really Cool Mining Level Peak Rank": (BASE_ID + 1410, ["Dog", "Breakable Tiles"]),
    "4-11: The Really Cool Mining Level Good Rank": (BASE_ID + 3410, ["Dog", "Breakable Tiles"]),
    "4-12: Weather Alert Complete": (BASE_ID + 411, ["Keys", "Jump Pads"]),
    "4-12: Weather Alert Peak Rank": (BASE_ID + 1411, ["Keys", "Jump Pads"]),
    "4-12: Weather Alert Good Rank": (BASE_ID + 3411, ["Keys", "Jump Pads"]),
    "4-13: The Downfall Complete": (BASE_ID + 412, ["Breakable Tiles"]),
    "4-13: The Downfall Peak Rank": (BASE_ID + 1412, ["Breakable Tiles"]),
    "4-13: The Downfall Good Rank": (BASE_ID + 3412, ["Breakable Tiles"]),
    "4-14: I Saw This In A Movie Once Complete": (BASE_ID + 413, ["Keys"]),
    "4-14: I Saw This In A Movie Once Peak Rank": (BASE_ID + 1413, ["Keys"]),
    "4-14: I Saw This In A Movie Once Good Rank": (BASE_ID + 3413, ["Keys"]),
    "4-15: Abandoned Workspace Complete": (BASE_ID + 414, ["Keys"]),
    "4-15: Abandoned Workspace Peak Rank": (BASE_ID + 1414, ["Keys"]),
    "4-15: Abandoned Workspace Good Rank": (BASE_ID + 3414, ["Keys"]),
    "4-16: Crimson Outpost Complete": (BASE_ID + 415, ["Breakable Tiles", "Nuke"]),
    "4-16: Crimson Outpost Peak Rank": (BASE_ID + 1415, ["Breakable Tiles", "Nuke"]),
    "4-16: Crimson Outpost Good Rank": (BASE_ID + 3415, ["Breakable Tiles", "Nuke"]),
    "4-17: CATaclysmic CATastrophe Complete": (BASE_ID + 416, ["Switch Tiles", "Portals"]),
    "4-17: CATaclysmic CATastrophe Peak Rank": (BASE_ID + 1416, ["Switch Tiles", "Portals", "Stop Markers"]),
    "4-17: CATaclysmic CATastrophe Good Rank": (BASE_ID + 3416, ["Switch Tiles", "Portals", "Stop Markers"]),
    "4-18: The Wall Complete": (BASE_ID + 417, []),
    "4-18: The Wall Peak Rank": (BASE_ID + 1417, []),
    "4-18: The Wall Good Rank": (BASE_ID + 3417, []),

    "5-1: Elysian Fields. Complete": (BASE_ID + 500, []),
    "5-1: Elysian Fields. Peak Rank": (BASE_ID + 1500, []),
    "5-1: Elysian Fields. Good Rank": (BASE_ID + 3500, []),
    "5-2: ... Complete": (BASE_ID + 501, []),
    "5-2: ... Peak Rank": (BASE_ID + 1501, []),
    "5-2: ... Good Rank": (BASE_ID + 3501, []),
    "5-3: ..? Complete": (BASE_ID + 502, []),
    "5-3: ..? Peak Rank": (BASE_ID + 1502, []),
    "5-3: ..? Good Rank": (BASE_ID + 3502, []),
    "5-4: The Horse Is Here. Complete": (BASE_ID + 503, ["Golf Balls"]),
    "5-4: The Horse Is Here. Peak Rank": (BASE_ID + 1503, ["Golf Balls"]),
    "5-4: The Horse Is Here. Good Rank": (BASE_ID + 3503, ["Golf Balls"]),
    "5-5: Unstable Complete": (BASE_ID + 504, ["Golf Balls"]),
    "5-5: Unstable Peak Rank": (BASE_ID + 1504, ["Golf Balls"]),
    "5-5: Unstable Good Rank": (BASE_ID + 3504, ["Golf Balls"]),
    "5-6: Close Encounters Of The Equine Kind Complete": (BASE_ID + 505, ["Breakable Tiles", "Golf Balls"]),
    "5-6: Close Encounters Of The Equine Kind Peak Rank": (BASE_ID + 1505, ["Breakable Tiles", "Golf Balls"]),
    "5-6: Close Encounters Of The Equine Kind Good Rank": (BASE_ID + 3505, ["Breakable Tiles", "Golf Balls"]),
    "5-7: Late to the Party Complete": (BASE_ID + 506, ["Golf Balls"]),
    "5-7: Late to the Party Peak Rank": (BASE_ID + 1506, ["Golf Balls"]),
    "5-7: Late to the Party Good Rank": (BASE_ID + 3506, ["Golf Balls"]),
    "5-8: Megaton Of Skeleton Complete": (BASE_ID + 507, ["Golf Balls"]),
    "5-8: Megaton Of Skeleton Peak Rank": (BASE_ID + 1507, ["Golf Balls"]),
    "5-8: Megaton Of Skeleton Good Rank": (BASE_ID + 3507, ["Golf Balls"]),
    "5-9: Neigh Impossible Complete": (BASE_ID + 508, ["Breakable Tiles", "Golf Balls"]),
    "5-9: Neigh Impossible Peak Rank": (BASE_ID + 1508, ["Breakable Tiles", "Golf Balls"]),
    "5-9: Neigh Impossible Good Rank": (BASE_ID + 3508, ["Breakable Tiles", "Golf Balls"]),
    "5-10: Move It Or Lose It Complete": (BASE_ID + 509, ["Breakable Tiles", "Golf Balls"]),
    "5-10: Move It Or Lose It Peak Rank": (BASE_ID + 1509, ["Breakable Tiles", "Golf Balls", "Go Markers", "Stop Markers"]),
    "5-10: Move It Or Lose It Good Rank": (BASE_ID + 3509, ["Breakable Tiles", "Golf Balls", "Go Markers", "Stop Markers"]),
    "5-11: Why Is There A Highway Here?!?! Complete": (BASE_ID + 510, ["Golf Balls", "Jump Pads"]),
    "5-11: Why Is There A Highway Here?!?! Peak Rank": (BASE_ID + 1510, ["Golf Balls", "Jump Pads"]),
    "5-11: Why Is There A Highway Here?!?! Good Rank": (BASE_ID + 3510, ["Golf Balls", "Jump Pads"]),
    "5-12: Two Face Temple Complete": (BASE_ID + 511, ["Golf Balls", "Switch Tiles"]),
    "5-12: Two Face Temple Peak Rank": (BASE_ID + 1511, ["Golf Balls", "Switch Tiles"]),
    "5-12: Two Face Temple Good Rank": (BASE_ID + 3511, ["Golf Balls", "Switch Tiles"]),
    "5-12: Two Face Temple Blue Smiley": (BASE_ID + 2557, []),
    "5-13: What Is This, A Crossover Episode? Complete": (BASE_ID + 512, ["Golf Balls"]),
    "5-13: What Is This, A Crossover Episode? Peak Rank": (BASE_ID + 1512, ["Golf Balls"]),
    "5-13: What Is This, A Crossover Episode? Good Rank": (BASE_ID + 3512, ["Golf Balls"]),
    "5-14: Containment Breach Complete": (BASE_ID + 513, ["Golf Balls", "Switch Tiles", "Nuke"]),
    "5-14: Containment Breach Peak Rank": (BASE_ID + 1513, ["Golf Balls", "Switch Tiles", "Nuke"]),
    "5-14: Containment Breach Good Rank": (BASE_ID + 3513, ["Golf Balls", "Switch Tiles", "Nuke"]),
    "5-15: Hoppin' Mad Complete": (BASE_ID + 514, ["Golf Balls", "Portals|Jump Pads"]),
    "5-15: Hoppin' Mad Peak Rank": (BASE_ID + 1514, ["Golf Balls", "Portals", "Jump Pads"]),
    "5-15: Hoppin' Mad Good Rank": (BASE_ID + 3514, ["Golf Balls", "Portals", "Jump Pads"]),
    "5-16: The Wizard of Gimmica Strikes!! Complete": (BASE_ID + 515, ["Golf Balls"]),
    "5-16: The Wizard of Gimmica Strikes!! Peak Rank": (BASE_ID + 1515, ["Golf Balls"]),
    "5-16: The Wizard of Gimmica Strikes!! Good Rank": (BASE_ID + 3515, ["Golf Balls"]),
    "5-17: Perilous Plinko Complete": (BASE_ID + 516, ["Golf Balls"]),
    "5-17: Perilous Plinko Peak Rank": (BASE_ID + 1516, ["Golf Balls"]),
    "5-17: Perilous Plinko Good Rank": (BASE_ID + 3516, ["Golf Balls"]),
    "5-18: The End Is Neigh. Complete": (BASE_ID + 517, ["Landmines"]),
    "5-18: The End Is Neigh. Peak Rank": (BASE_ID + 1517, ["Landmines"]),
    "5-18: The End Is Neigh. Good Rank": (BASE_ID + 3517, ["Landmines"]),

    "P-1: Welcome to...? Complete": (BASE_ID + 600, []),
    "P-1: Welcome to...? Peak Rank": (BASE_ID + 1600, []),
    "P-1: Welcome to...? Good Rank": (BASE_ID + 3600, []),
    "P-2: Welcome to COSMIC CHAMPIONSHIP!! Complete": (BASE_ID + 601, ["Keys", "Jump Pads"]),
    "P-2: Welcome to COSMIC CHAMPIONSHIP!! Peak Rank": (BASE_ID + 1601, ["Keys", "Jump Pads"]),
    "P-2: Welcome to COSMIC CHAMPIONSHIP!! Good Rank": (BASE_ID + 3601, ["Keys", "Jump Pads"]),
    "P-3: Avoid the Void Complete": (BASE_ID + 602, ["Switch Tiles"]),
    "P-3: Avoid the Void Peak Rank": (BASE_ID + 1602, ["Switch Tiles", "Stop Markers"]),
    "P-3: Avoid the Void Good Rank": (BASE_ID + 3602, ["Switch Tiles", "Stop Markers"]),
    "P-4: I Couldn't Beat This One :( Complete": (BASE_ID + 603, ["Switch Tiles"]),
    "P-4: I Couldn't Beat This One :( Peak Rank": (BASE_ID + 1603, ["Switch Tiles"]),
    "P-4: I Couldn't Beat This One :( Good Rank": (BASE_ID + 3603, ["Switch Tiles"]),
    "P-5: Starstorm! Complete": (BASE_ID + 604, ["Breakable Tiles"]),
    "P-5: Starstorm! Peak Rank": (BASE_ID + 1604, ["Breakable Tiles", "Stop Markers"]),
    "P-5: Starstorm! Good Rank": (BASE_ID + 3604, ["Breakable Tiles", "Stop Markers"]),
    "P-6: Oh My Goodness, This Beat Is So Hard Complete": (BASE_ID + 605, ["Metronome"]),
    "P-6: Oh My Goodness, This Beat Is So Hard Peak Rank": (BASE_ID + 1605, ["Metronome"]),
    "P-6: Oh My Goodness, This Beat Is So Hard Good Rank": (BASE_ID + 3605, ["Metronome"]),
    "P-7: Ourple Complete": (BASE_ID + 606, ["Metronome", "Keys", "Switch Tiles"]),
    "P-7: Ourple Peak Rank": (BASE_ID + 1606, ["Metronome", "Keys", "Switch Tiles"]),
    "P-7: Ourple Good Rank": (BASE_ID + 3606, ["Metronome", "Keys", "Switch Tiles"]),
    "P-8: Get In The Groove! Complete": (BASE_ID + 607, ["Metronome", "Portals"]),
    "P-8: Get In The Groove! Peak Rank": (BASE_ID + 1607, ["Metronome", "Portals"]),
    "P-8: Get In The Groove! Good Rank": (BASE_ID + 3607, ["Metronome", "Portals"]),
    "P-9: Neon Hopscotch Complete": (BASE_ID + 608, ["Metronome"]),
    "P-9: Neon Hopscotch Peak Rank": (BASE_ID + 1608, ["Metronome"]),
    "P-9: Neon Hopscotch Good Rank": (BASE_ID + 3608, ["Metronome"]),
    "P-10: Claustrophobia Complete": (BASE_ID + 609, ["Metronome", "Keys"]),
    "P-10: Claustrophobia Peak Rank": (BASE_ID + 1609, ["Metronome", "Keys"]),
    "P-10: Claustrophobia Good Rank": (BASE_ID + 3609, ["Metronome", "Keys"]),
    "P-11: Beat The Beat The Beat The Beat The Beat Complete": (BASE_ID + 610, ["Metronome", "Portals"]),
    "P-11: Beat The Beat The Beat The Beat The Beat Peak Rank": (BASE_ID + 1610, ["Metronome", "Portals"]),
    "P-11: Beat The Beat The Beat The Beat The Beat Good Rank": (BASE_ID + 3610, ["Metronome", "Portals"]),
    "P-11: Beat The Beat The Beat The Beat The Beat Yellow Smiley": (BASE_ID + 2653, ["Metronome", "Portals"]),
    "P-12: JumbleRAVE!! Complete": (BASE_ID + 611, ["Switch Tiles", "Jump Pads"]),
    "P-12: JumbleRAVE!! Peak Rank": (BASE_ID + 1611, ["Switch Tiles", "Jump Pads"]),
    "P-12: JumbleRAVE!! Good Rank": (BASE_ID + 3611, ["Switch Tiles", "Jump Pads"]),
    "P-13: where are you going come back Complete": (BASE_ID + 612, []),
    "P-13: where are you going come back Peak Rank": (BASE_ID + 1612, []),
    "P-13: where are you going come back Good Rank": (BASE_ID + 3612, []),
    "P-14: Sea of Lies Complete": (BASE_ID + 613, []),
    "P-14: Sea of Lies Peak Rank": (BASE_ID + 1613, []),
    "P-14: Sea of Lies Good Rank": (BASE_ID + 3613, []),
    "P-15: Santa's Revenge (What!!!) Complete": (BASE_ID + 614, ["Portals", "Breakable Tiles", "Keys"]),
    "P-15: Santa's Revenge (What!!!) Peak Rank": (BASE_ID + 1614, ["Portals", "Breakable Tiles", "Keys"]),
    "P-15: Santa's Revenge (What!!!) Good Rank": (BASE_ID + 3614, ["Portals", "Breakable Tiles", "Keys"]),
    "P-15: Santa's Revenge (What!!!) Yellow Smiley": (BASE_ID + 2673, ["Portals", "Breakable Tiles", "Keys"]),
    "P-16: Towards The Singularity Complete": (BASE_ID + 615, ["Keys", "Jump Pads", "Go Markers"]),
    "P-16: Towards The Singularity Peak Rank": (BASE_ID + 1615, ["Keys", "Jump Pads", "Go Markers"]),
    "P-16: Towards The Singularity Good Rank": (BASE_ID + 3615, ["Keys", "Jump Pads", "Go Markers"]),
    "P-17: One Last Huzzah Complete": (
        BASE_ID + 616,
        ["Keys", "Breakable Tiles", "Switch Tiles", "Stop Markers", "Nuke", "Dog", "Metronome"],
    ),
    "P-17: One Last Huzzah Peak Rank": (
        BASE_ID + 1616,
        ["Keys", "Breakable Tiles", "Switch Tiles", "Stop Markers", "Nuke", "Dog", "Metronome", "Go Markers"],
    ),
    "P-17: One Last Huzzah Good Rank": (
        BASE_ID + 3616,
        ["Keys", "Breakable Tiles", "Switch Tiles", "Stop Markers", "Nuke", "Dog", "Metronome", "Go Markers"],
    ),
    "P-17: One Last Huzzah Yellow Smiley": (
        BASE_ID + 2683,
        ["Keys", "Breakable Tiles", "Switch Tiles", "Stop Markers"],
    ),
    "P-18: Farewell, Uncanny Cat Golf Complete": (BASE_ID + 617, []),
    "P-18: Farewell, Uncanny Cat Golf Peak Rank": (BASE_ID + 1617, []),
    "P-18: Farewell, Uncanny Cat Golf Good Rank": (BASE_ID + 3617, []),

    "E-0: Deep Breaths... Complete": (BASE_ID + 700, []),
    "E-0: Deep Breaths... Peak Rank": (BASE_ID + 1700, []),
    "E-0: Deep Breaths... Good Rank": (BASE_ID + 3700, []),
    "E-1: Feline Beeline Complete": (BASE_ID + 701, ["Keys"]),
    "E-1: Feline Beeline Peak Rank": (BASE_ID + 1701, ["Keys"]),
    "E-1: Feline Beeline Good Rank": (BASE_ID + 3701, ["Keys"]),
    "E-2: T-T-Tilted Complete": (BASE_ID + 702, []),
    "E-2: T-T-Tilted Peak Rank": (BASE_ID + 1702, []),
    "E-2: T-T-Tilted Good Rank": (BASE_ID + 3702, []),
    "E-3: Lying Face Complete": (BASE_ID + 703, ["Switch Tiles", "Jump Pads"]),
    "E-3: Lying Face Peak Rank": (BASE_ID + 1703, ["Switch Tiles", "Jump Pads"]),
    "E-3: Lying Face Good Rank": (BASE_ID + 3703, ["Switch Tiles", "Jump Pads"]),
    "E-4: Tricky Thicket Complete": (BASE_ID + 704, ["Portals", "Jump Pads", "Breakable Tiles"]),
    "E-4: Tricky Thicket Peak Rank": (BASE_ID + 1704, ["Portals", "Jump Pads", "Breakable Tiles", "Go Markers"]),
    "E-4: Tricky Thicket Good Rank": (BASE_ID + 3704, ["Portals", "Jump Pads", "Breakable Tiles", "Go Markers"]),
    "E-5: Three Ring Circus Complete": (BASE_ID + 705, []),
    "E-5: Three Ring Circus Peak Rank": (BASE_ID + 1705, []),
    "E-5: Three Ring Circus Good Rank": (BASE_ID + 3705, []),
    "E-6: But Passion Is Mortal... Complete": (BASE_ID + 706, ["Switch Tiles"]),
    "E-6: But Passion Is Mortal... Peak Rank": (BASE_ID + 1706, ["Switch Tiles", "Stop Markers", "Go Markers"]),
    "E-6: But Passion Is Mortal... Good Rank": (BASE_ID + 3706, ["Switch Tiles", "Stop Markers", "Go Markers"]),
    "E-7: The Key to Failure Complete": (BASE_ID + 707, ["Breakable Tiles", "Keys", "Jump Pads"]),
    "E-7: The Key to Failure Peak Rank": (BASE_ID + 1707, ["Breakable Tiles", "Keys", "Jump Pads"]),
    "E-7: The Key to Failure Good Rank": (BASE_ID + 3707, ["Breakable Tiles", "Keys", "Jump Pads"]),
    "E-8: HE'S IN THE WALLS!!! Complete": (BASE_ID + 708, ["Keys", "Jump Pads"]),
    "E-8: HE'S IN THE WALLS!!! Peak Rank": (BASE_ID + 1708, ["Keys", "Jump Pads"]),
    "E-8: HE'S IN THE WALLS!!! Good Rank": (BASE_ID + 3708, ["Keys", "Jump Pads"]),
    "E-9: Infinity Plaza Complete": (BASE_ID + 709, ["Keys", "Breakable Tiles"]),
    "E-9: Infinity Plaza Peak Rank": (BASE_ID + 1709, ["Keys", "Breakable Tiles"]),
    "E-9: Infinity Plaza Good Rank": (BASE_ID + 3709, ["Keys", "Breakable Tiles"]),
    
    # MINIGAME LOCATIONS
    "Bort Bash: Round 1": (BASE_ID + 5000, ["Bort Bash"]),
    "Bort Bash: Round 2": (BASE_ID + 5001, ["Bort Bash"]),
    "Bort Bash: Round 3": (BASE_ID + 5002, ["Bort Bash"]),
    "Bort Bash: Round 4": (BASE_ID + 5003, ["Bort Bash"]),
    "Bort Bash: Round 5": (BASE_ID + 5004, ["Bort Bash"]),
    "Bort Bash: Round 6": (BASE_ID + 5005, ["Bort Bash"]),
    "Bort Bash: Round 7": (BASE_ID + 5006, ["Bort Bash"]),
    "Bort Bash: Round 8": (BASE_ID + 5007, ["Bort Bash"]),
    "Bort Bash: Round 9": (BASE_ID + 5008, ["Bort Bash"]),
    "Bort Bash: Round 10": (BASE_ID + 5009, ["Bort Bash"]),
    "Meowls: 10km": (BASE_ID + 6000, ["Meowls"]),
    "Meowls: 20km": (BASE_ID + 6001, ["Meowls"]),
    "Meowls: 30km": (BASE_ID + 6002, ["Meowls"]),
    "Meowls: 40km": (BASE_ID + 6003, ["Meowls"]),
    "Meowls: 50km": (BASE_ID + 6004, ["Meowls"]),
    "Meowls: 60km": (BASE_ID + 6005, ["Meowls"]),
    "Meowls: 70km": (BASE_ID + 6006, ["Meowls"]),
    "Meowls: 80km": (BASE_ID + 6007, ["Meowls"]),
    "Meowls: 90km": (BASE_ID + 6008, ["Meowls"]),
    "Meowls: 100km": (BASE_ID + 6009, ["Meowls"]),
    "UNCANNY_DASH: 25 Score": (BASE_ID + 7000, ["UNCANNY_DASH"]),
    "UNCANNY_DASH: 50 Score": (BASE_ID + 7001, ["UNCANNY_DASH"]),
    "UNCANNY_DASH: 75 Score": (BASE_ID + 7002, ["UNCANNY_DASH"]),
    "UNCANNY_DASH: 100 Score": (BASE_ID + 7003, ["UNCANNY_DASH"]),
    "UNCANNY_DASH: 125 Score": (BASE_ID + 7004, ["UNCANNY_DASH"]),
    "UNCANNY_DASH: 150 Score": (BASE_ID + 7005, ["UNCANNY_DASH"]),
    "UNCANNY_DASH: 175 Score": (BASE_ID + 7006, ["UNCANNY_DASH"]),
    "UNCANNY_DASH: 200 Score": (BASE_ID + 7007, ["UNCANNY_DASH"]),
    "UNCANNY_DASH: 225 Score": (BASE_ID + 7008, ["UNCANNY_DASH"]),
    "UNCANNY_DASH: 250 Score": (BASE_ID + 7009, ["UNCANNY_DASH"]),
}

# The world class needs a plain name -> id mapping, without the logic requirements attached.
LOCATION_NAME_TO_ID: dict[str, int] = {name: data[0] for name, data in LOCATION_DATA.items()}

LEVEL_LOCATION_SUFFIXES = (
    " Complete", " Peak Rank", " Good Rank",
    " Red Smiley", " Green Smiley", " Blue Smiley", " Yellow Smiley", " Orange Smiley",
)

MINIGAME_LOCATION_PREFIXES = tuple(f"{name}: " for name in sorted(items.MINIGAME_ITEM_NAMES))


class UncannyCatLocation(Location):
    game = "Uncanny Cat Golf"


def is_minigame_location(location_name: str) -> bool:
    """Minigame checks belong to a minigame rather than a level, so level and prism logic should skip them."""
    return location_name.startswith(MINIGAME_LOCATION_PREFIXES)


def level_item_name(location_name: str) -> str:
    """"1-4: Breakthrough! Peak Rank" -> "1-4: Breakthrough!" (the level unlock item)."""
    for suffix in LEVEL_LOCATION_SUFFIXES:
        if location_name.endswith(suffix):
            return location_name[: -len(suffix)]
    return location_name


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def get_excluded_locations(world: UncannyCatWorld) -> set[str]:
    """Locations that don't exist under the player's options, and so get neither a check nor an unlock item."""
    included_worlds = items.get_included_world_prefixes(world)
    # The goal level is not included
    goal_level = items.GOAL_LEVEL[world.options.goal_level.value]

    excluded: set[str] = set()
    for location_name in LOCATION_NAME_TO_ID:
        if is_minigame_location(location_name):
            if not world.options.minigames:
                excluded.add(location_name)
            continue

        level = level_item_name(location_name)
        if items.world_prefix(level) not in included_worlds:
            excluded.add(location_name)
        elif level == goal_level:
            excluded.add(location_name)
        elif not world.options.peak_checks and location_name.endswith(" Peak Rank"):
            excluded.add(location_name)
    return excluded


def create_all_locations(world: UncannyCatWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: UncannyCatWorld) -> None:
    excluded = get_excluded_locations(world)
    for loc_name, loc_id in LOCATION_NAME_TO_ID.items():
        if loc_name in excluded:
            continue
        if loc_name.startswith("0"):
            region_name = "World 0 (Tutorial)"
        elif loc_name.startswith("1"):
            region_name = "World 1 (Golf Central)"
        elif loc_name.startswith("2"):
            region_name = "World 2 (Glowstick City)"
        elif loc_name.startswith("3"):
            region_name = "World 3 (Chuckle Park)"
        elif loc_name.startswith("4"):
            region_name = "World 4 (Final Frontier)"
        elif loc_name.startswith("5"):
            region_name = "World 5 (Elysian Fields)"
        elif loc_name.startswith("P"):
            region_name = "World P (Cosmic Championship)"
        elif loc_name.startswith("E"):
            region_name = "World E (Endless Levels)"
        else:
            region_name = "Summer Villa"
        region = world.get_region(region_name)
        region.add_locations({loc_name: loc_id}, UncannyCatLocation)


def create_events(world: UncannyCatWorld) -> None:
    # Victory lives in Menu because it is always physically reachable; its access rule is what actually gates it.
    menu = world.get_region("Menu")
    menu.add_event(
        "Victory", "Victory", location_type=UncannyCatLocation, item_type=items.UncannyCatItem
    )
