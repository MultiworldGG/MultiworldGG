from __future__ import annotations
from typing import TYPE_CHECKING
import json
from importlib import resources
from BaseClasses import ItemClassification, Location
import re
from pathlib import Path
from dataclasses import dataclass

if TYPE_CHECKING:
    from .world import SimpsonsHitNRunWorld

with resources.files(__package__).joinpath("Data/cards.json").open("r", encoding="utf-8") as f:
    card_info = json.load(f)

@dataclass
class Card:
    id: int
    name: str
    gameid: int
    x: float
    y: float
    z: float

cards_by_name = { card["Desc"]: card for level_cards in card_info.values() for card in level_cards }


LOCATION_NAME_TO_ID = {
    # Level 1 Missions
    "(L1M1) SMRT": 122289,
    "(L1M2) Petty Theft Homer": 122290,
    "(L1M3) Office Spaced": 122291,
    "(L1M4) Blind Big Brother": 122292,
    "(L1M5) Flowers By Irene": 122293,
    "(L1M6) BoneStorm Storm": 122294,
    "(L1M7) The Fat and the Furious": 122295,
    "(L1BM) This Old Shanty": 122296,
    "(LVL 1) Talk to Barney": 122679,

    # Level 1 Races
    "(LVL 1) Time Trial Race": 122297,
    "(LVL 1) Circuit Race": 122298,
    "(LVL 1) Checkpoint Race": 122299,

    # Level 1 Cards
    "(LVL 1) CARD - Simpsons' Backyard": 122692,
    "(LVL 1) CARD - Kwik-E-Mart Roof": 122693,
    "(LVL 1) CARD - Wiggum's Backyard": 122694,
    "(LVL 1) CARD - Corner Outside Near StoneCutter Entrance": 122695,
    "(LVL 1) CARD - Above StoneCutters Table": 122696,
    "(LVL 1) CARD - Highest Platform in Power Plant": 122697,
    "(LVL 1) CARD - Trailer Park": 122698,
    "(LVL 1) CARD - Neighbor's Carport": 122699,
    "(LVL 1) CARD - Behind Flanders' Tree": 122700,
    "(LVL 1) CARD - Jump Past Neighbor's Playground": 122701,
    "(LVL 1) CARD - Above Kwik-E-Mart": 122702,
    "(LVL 1) CARD - Kwik-E-Mart's Dumpster": 122703,
    "(LVL 1) CARD - Krusty Burger's Dumpster": 122704,
    "(LVL 1) CARD - Gas Station Roof": 122705,
    "(LVL 1) CARD - Above Street Between Simpsons' House and Kwik-E-Mart": 122706,
    "(LVL 1) CARD - Evergreen Terrace Horseshoe Road": 122707,
    "(LVL 1) CARD - Top of Krusty Burger Near Kwik-E-Mart": 122708,
    "(LVL 1) CARD - Retirement Castle": 122709,
    "(LVL 1) CARD - Casa Nova": 122710,
    "(LVL 1) CARD - Shortcut Between Church and Lard Lad": 122711,
    "(LVL 1) CARD - Church Sign": 122712,
    "(LVL 1) CARD - Church Dumpster": 122713,
    "(LVL 1) CARD - Dumpster Behind Krusty Burger Near School": 122714,
    "(LVL 1) CARD - Deli Near School": 122715,
    "(LVL 1) CARD - Back of School Roof": 122716,
    "(LVL 1) CARD - Willie's Shack": 122717,
    "(LVL 1) CARD - Grocery Store's Dumpster": 122718,
    "(LVL 1) CARD - Lard Lad Doorbell": 122719,
    "(LVL 1) CARD - House Across From Simpsons' House 1": 122720,
    "(LVL 1) CARD - House Across From Simpsons' House 2": 122721,
    "(LVL 1) CARD - Above Wiggum's": 122722,
    "(LVL 1) CARD - House on Corner Near Graveyard": 122723,
    "(LVL 1) CARD - House Next to Krusty Burger Near Graveyard": 122724,
    "(LVL 1) CARD - Cletus' House": 122725,
    "(LVL 1) CARD - Big Bridge": 122726,
    "(LVL 1) CARD - Flanders' House": 122727,
    "(LVL 1) CARD - Moe's House": 122728,
    "(LVL 1) CARD - Nelson's House": 122729,
    "(LVL 1) CARD - Tire Fire": 122730,
    "(LVL 1) CARD - Power Plant": 122731,
    "(LVL 1) CARD - Across From Gil": 122732,
    "(LVL 1) CARD - Back of Cletus' Shack": 122733,
    "(LVL 1) CARD - Tree on Corner Near Graveyard": 122734,
    "(LVL 1) CARD - Above Trailer Park": 122735,
    "(LVL 1) CARD - Above Street Near Barn": 122736,
    "(LVL 1) CARD - Corner of Tomacco Field": 122737,
    "(LVL 1) CARD - Beside School": 122738,
    "(LVL 1) CARD - Power Plant Parking Lot 1": 122739,
    "(LVL 1) CARD - Power Plant Parking Lot 2": 122740,
    "(LVL 1) CARD - Above Street Near Simpsons' House": 122741,
    "(LVL 1) CARD - Power Plant Platforming 1": 122742,
    "(LVL 1) CARD - Power Plant Platforming 2": 122743,
    "(LVL 1) CARD - Homer's Workstation": 122744,
    "(LVL 1) CARD - Above Nuclear Waste Bridge": 122745,
    "(LVL 1) CARD - Outside Stonecutter Tunnel": 122746,
    "(LVL 1) CARD - Rich Side Gas Station's Dumpster": 122747,
    "(LVL 1) CARD - Roof Across of House Across From Gold Mansion": 122748,
    "(LVL 1) CARD - Outside Burns Mansion Gate": 122749,
    "(LVL 1) CARD - Broken Bridge": 122750,
    "(LVL 1) CARD - Rocket Car": 122751,

    # Level 1 Wasps
    "(LVL 1) WASP - Small Park Next to Simpsons House": 122366,
    "(LVL 1) WASP - Next to the Blue House Besides Simpsons House": 122367,
    "(LVL 1) WASP - Flanders Backyard": 122368,
    "(LVL 1) WASP - Wiggum's Backyard": 122369,
    "(LVL 1) WASP - Kwik-E-Mart Roof": 122370,
    "(LVL 1) WASP - Gas Pump Roof": 122371,
    "(LVL 1) WASP - Lard Lads Roof": 122372,
    "(LVL 1) WASP - School Yard Bus": 122373,
    "(LVL 1) WASP - Back Door of School": 122374,
    "(LVL 1) WASP - School Roof 1": 122375,
    "(LVL 1) WASP - School Roof 2": 122376,
    "(LVL 1) WASP - Top of Tower Before Broken Bridge": 122377,
    "(LVL 1) WASP - Rocket Car": 122378,
    "(LVL 1) WASP - StoneCutters Table 1": 122379,
    "(LVL 1) WASP - StoneCutters Table 2": 122380,
    "(LVL 1) WASP - Barn Haystack": 122381,
    "(LVL 1) WASP - Trailer Park 1": 122382,
    "(LVL 1) WASP - Trailer Park 2": 122383,
    "(LVL 1) WASP - Atop of Bridge Framework 1": 122384,
    "(LVL 1) WASP - Atop of Bridge Framework 2": 122385,

    # Level 1 Gags
    "(LVL 1) GAG - Simpsons TV": 122393,
    "(LVL 1) GAG - Swings Besides Blue House": 122394,
    "(LVL 1) GAG - Simpsons Grill": 122395,
    "(LVL 1) GAG - Simpsons Swing": 122396,
    "(LVL 1) GAG - Simpsons FireBreathing Tiki": 122397,
    "(LVL 1) GAG - Flanders Bomb Shelter": 122398,
    "(LVL 1) GAG - Tank in Front of Power Plant": 122399,
    "(LVL 1) GAG - Homer's Workstation Meltdown": 122400,
    "(LVL 1) GAG - School Fire Extinguisher": 122401,
    "(LVL 1) GAG - School Fire Alarm": 122402,
    "(LVL 1) GAG - Man in Freezer at Kwik-E-Mart": 122403,
    "(LVL 1) GAG - Silent Alarm in Kwik-E-Mart": 122404,
    "(LVL 1) GAG - Arcade Cabinet in Kwik-E-Mart": 122405,
    "(LVL 1) GAG - Squishee Machine in Kwik-E-Mart": 122406,
    "(LVL 1) GAG - ATM in Kwik-E-Mart": 122691,

    # Level 1 Shops
    "(LVL 1) Shop Check 1": 122407,
    "(LVL 1) Shop Check 2": 122408,
    "(LVL 1) Shop Check 3": 122409,
    "(LVL 1) Shop Check 4": 122410,
    "(LVL 1) Shop Check 5": 122411,
    "(LVL 1) Shop Check 6": 122412,

    # Level 2 Missions
    "(L2M1) Detention Deficit Disorder": 122300,
    "(L2M2) Weapons of Mass Delinquency": 122301,
    "(L2M3) Vox Nerduli": 122302,
    "(L2M4) Bart 'n' Frink": 122303,
    "(L2M5) Better Than Beef": 122304,
    "(L2M6) Monkey See Monkey D'oh": 122305,
    "(L2M7) Cell-Outs": 122306,
    "(L2BM) Dial B for Blood": 122307,
    "(LVL 2) Talk to Homer": 122680,

    # Level 2 Races
    "(LVL 2) Time Trial Race": 122308,
    "(LVL 2) Circuit Race": 122309,
    "(LVL 2) Checkpoint Race": 122310,

    # Level 2 Cards
    "(LVL 2) CARD - Statue": 122752,
    "(LVL 2) CARD - Roof Across Monkey Building": 122753,
    "(LVL 2) CARD - Legitimate Businessman's Roof": 122754,
    "(LVL 2) CARD - Car Wash": 122755,
    "(LVL 2) CARD - Train Wagon": 122756,
    "(LVL 2) CARD - Alleyway Behind Krusty Burger": 122757,
    "(LVL 2) CARD - Fountain At Stadium": 122758,
    "(LVL 2) CARD - Light Pole by Court House": 122759,
    "(LVL 2) CARD - Behind Museum Sign": 122760,
    "(LVL 2) CARD - Lion Statue": 122761,
    "(LVL 2) CARD - Park Fountain near Hospital": 122762,
    "(LVL 2) CARD - Hospital Doors": 122763,
    "(LVL 2) CARD - Above Street Near Hospital Parking Lot": 122764,
    "(LVL 2) CARD - Town Hall (Stadium Side)": 122765,
    "(LVL 2) CARD - Stadium Behind Duff Mascot": 122766,
    "(LVL 2) CARD - Stadium Ledge Bench": 122767,
    "(LVL 2) CARD - Tunnel Pillar Near Stadium": 122768,
    "(LVL 2) CARD - Tunnel Pillar Near Downtown": 122769,
    "(LVL 2) CARD - Stadium Billboard": 122770,
    "(LVL 2) CARD - Fire Truck Jump": 122771,
    "(LVL 2) CARD - Tree By Krusty Burger Downtown": 122772,
    "(LVL 2) CARD - Sit N Rotate": 122773,
    "(LVL 2) CARD - Downtown Bank": 122774,
    "(LVL 2) CARD - Monorail": 122775,
    "(LVL 2) CARD - Corner of Monorail Station": 122776,
    "(LVL 2) CARD - Above Street Near Downtown Krusty Float": 122777,
    "(LVL 2) CARD - Ramp Behind Downtown Krusty Burger": 122778,
    "(LVL 2) CARD - Deli Near Monorail": 122779,
    "(LVL 2) CARD - Above Downtown Highway Exit": 122780,
    "(LVL 2) CARD - Closed Highway": 122781,
    "(LVL 2) CARD - Main Highway": 122782,
    "(LVL 2) CARD - East Side Highway Exit": 122783,
    "(LVL 2) CARD - Try N Save Parking Lot": 122784,
    "(LVL 2) CARD - Behind Herman's Military Antiques": 122785,
    "(LVL 2) CARD - Above Street Near Helter Shelter": 122786,
    "(LVL 2) CARD - DMV Sign": 122787,
    "(LVL 2) CARD - DMV Light Pole": 122788,
    "(LVL 2) CARD - Above Street Between DMV and Trainyard": 122789,
    "(LVL 2) CARD - Between Trains": 122790,
    "(LVL 2) CARD - Above Train Crossing": 122791,
    "(LVL 2) CARD - Behind Moving Train": 122792,
    "(LVL 2) CARD - Train Stairs": 122793,
    "(LVL 2) CARD - Near Grease Recycling Plant": 122794,
    "(LVL 2) CARD - Outside Trainyard Parking Spot": 122795,
    "(LVL 2) CARD - Above Street Near Car Wash": 122796,
    "(LVL 2) CARD - On Top of Gas Station at Car Wash": 122797,
    "(LVL 2) CARD - Inside Trainyard Parking Spot": 122798,
    "(LVL 2) CARD - Lexicon Bookstore Roof": 122799,
    "(LVL 2) CARD - King Toot's Music Store Roof": 122800,
    "(LVL 2) CARD - Alley Behind King Toot's Music Store": 122801,
    "(LVL 2) CARD - Legitimate Businessman's Roof 2": 122802,
    "(LVL 2) CARD - Glen's Grocery Roof": 122803,
    "(LVL 2) CARD - Stop Sign Across From Moe's": 122804,
    "(LVL 2) CARD - Platform behind Lard Lad's": 122805,
    "(LVL 2) CARD - Street Near Construction": 122806,
    "(LVL 2) CARD - Under Construction Building Between Krusty Burger and Lard Lad's": 122807,
    "(LVL 2) CARD - Krusty Burger Sign": 122808,
    "(LVL 2) CARD - Near Concrete Mixer": 122809,
    "(LVL 2) CARD - Gazebo Between Museum & Court House": 122810,
    "(LVL 2) CARD - Monkey Box": 122811,
    "(LVL 2) CARD - Hospital Sign": 122812,
    "(LVL 2) CARD - Magnifying Glass Parking Lot": 122813,
    "(LVL 2) CARD - Police Station": 122814,
    "(LVL 2) CARD - Tree Outside Police Station": 122815,
    "(LVL 2) CARD - 50% Off Sign Near Monorail": 122816,
    "(LVL 2) CARD - Wooden Tower": 122817,
    "(LVL 2) CARD - Town Hall Front": 122818,
    "(LVL 2) CARD - Coming Soon Construction Sign": 122819,
    "(LVL 2) CARD - Inside Moe's": 122820,

    # Level 2 Wasps
    "(LVL 2) WASP - CourtHouse Steps": 122413,
    "(LVL 2) WASP - Gazebo Between Museum and Courthouse": 122414,
    "(LVL 2) WASP - Museum Steps": 122415,
    "(LVL 2) WASP - Hospital Front Yard": 122416,
    "(LVL 2) WASP - Roof Across Monkey Building": 122417,
    "(LVL 2) WASP - Town Hall (Front)": 122418,
    "(LVL 2) WASP - Town Hall (Back)": 122419,
    "(LVL 2) WASP - Behind Downtown Krusty Burger": 122420,
    "(LVL 2) WASP - Monorail Stairs": 122421,
    "(LVL 2) WASP - Upstair Beside Monorail": 122422,
    "(LVL 2) WASP - Roof Across Monorail": 122423,
    "(LVL 2) WASP - Stairs Leading atop Trains": 122424,
    "(LVL 2) WASP - Across Moving Train": 122425,
    "(LVL 2) WASP - On Train Past Water Tank": 122426,
    "(LVL 2) WASP - Inside Trainyard Parking Spot": 122427,
    "(LVL 2) WASP - Car Wash": 122428,
    "(LVL 2) WASP - Legitimate Businessman's Rooftop 1": 122429,
    "(LVL 2) WASP - Legitimate Businessman's Rooftop 2": 122430,
    "(LVL 2) WASP - Roof Next to Moe's": 122431,
    "(LVL 2) WASP - Lard Lads Roof": 122432,

    # Level 2 Gags
    "(LVL 2) GAG - CATapult": 122440,
    "(LVL 2) GAG - Cement Truck": 122441,
    "(LVL 2) GAG - Pickled Egg Jar at Moes": 122442,
    "(LVL 2) GAG - Slot Machine at Moes": 122443,
    "(LVL 2) GAG - Love Tester as Moes": 122444,
    "(LVL 2) GAG - Light up Drinks at Moes": 122445,
    "(LVL 2) GAG - Rat's Milk Machine atop Legitimate Businessman's Roof": 122446,
    "(LVL 2) GAG - Blinding Hans Moleman at the DMV": 122447,
    "(LVL 2) GAG - Car Ride at Try-N-Save": 122448,
    "(LVL 2) GAG - Missile Behind Military Antiques": 122449,
    "(LVL 2) GAG - Dumpster Behind Krusty Burger (Near Police Station)": 122450,

    # Level 2 Shops
    "(LVL 2) Shop Check 1": 122451,
    "(LVL 2) Shop Check 2": 122452,
    "(LVL 2) Shop Check 3": 122453,
    "(LVL 2) Shop Check 4": 122454,
    "(LVL 2) Shop Check 5": 122455,
    "(LVL 2) Shop Check 6": 122456,

    # Level 3 Missions
    "(L3M1) Nerd Race Queen": 122311,
    "(L3M2) Clueless": 122312,
    "(L3M3) Bonfire of the Manatees": 122313,
    "(L3M4) Operation Hellfish": 122314,
    "(L3M5) Slithery Sleuthing": 122315,
    "(L3M6) Fishy Deals": 122316,
    "(L3M7) The Old Pirate and the Sea": 122317,
    "(L3BM) Princi-Pal": 122318,
    "(LVL 3) Talk to Otto": 122681,

    # Level 3 Races
    "(LVL 3) Time Trial Race": 122319,
    "(LVL 3) Circuit Race": 122320,
    "(LVL 3) Checkpoint Race": 122321,

    # Level 3 Cards
    "(LVL 3) CARD - Comic Book Guy's Rooftop": 122821,
    "(LVL 3) CARD - Above Bowling": 122822,
    "(LVL 3) CARD - Atop Lighthouse": 122823,
    "(LVL 3) CARD - Edge of Globex Ship": 122824,
    "(LVL 3) CARD - Krusty Studio Balcony": 122825,
    "(LVL 3) CARD - Platforming Below Dam Railing": 122826,
    "(LVL 3) CARD - Beside Broken Bridge": 122827,
    "(LVL 3) CARD - Behind Lighthouse": 122828,
    "(LVL 3) CARD - Pelican Behind Planet Hype 1": 122829,
    "(LVL 3) CARD - Pelican Behind Planet Hype 2": 122830,
    "(LVL 3) CARD - Planet Hype Outdoor Seating": 122831,
    "(LVL 3) CARD - Pelican in Front of Planet Hype 1": 122832,
    "(LVL 3) CARD - Pelican in Front of Planet Hype 2": 122833,
    "(LVL 3) CARD - Pelican Near Squidport Arch": 122834,
    "(LVL 3) CARD - Little Boats on Beach": 122835,
    "(LVL 3) CARD - Big Boat on Beach": 122836,
    "(LVL 3) CARD - Deck by Squidport Pedestrian Entrance 1": 122837,
    "(LVL 3) CARD - Deck by Squidport Pedestrian Entrance 2": 122838,
    "(LVL 3) CARD - Casino Bushes Near Squidport": 122839,
    "(LVL 3) CARD - Lower Casino Entrance": 122840,
    "(LVL 3) CARD - Sidewalk Near Casino Ramp 1": 122841,
    "(LVL 3) CARD - Behind Casino Ramp": 122842,
    "(LVL 3) CARD - Sidewalk Near Casino Ramp 2": 122843,
    "(LVL 3) CARD - Houses Near Bowl-a-Rama": 122844,
    "(LVL 3) CARD - Jazz Hole": 122845,
    "(LVL 3) CARD - Krusty Burger Parking Lot": 122846,
    "(LVL 3) CARD - Gated Houses Near Aztec Theater": 122847,
    "(LVL 3) CARD - Boulevard Near Krusty and Friends Billboard": 122848,
    "(LVL 3) CARD - Stairs Near Krusty and Friends Billboard": 122849,
    "(LVL 3) CARD - Short Wall Down the Street from Gas Station": 122850,
    "(LVL 3) CARD - Concrete Mixer at Gas Station": 122851,
    "(LVL 3) CARD - Green Building Across From Principal Skinner": 122852,
    "(LVL 3) CARD - Lumber King Billboard": 122853,
    "(LVL 3) CARD - Park Across From Android's Dungeon": 122854,
    "(LVL 3) CARD - Behind Krusty Burger Across From Android's Dungeon": 122855,
    "(LVL 3) CARD - Wall E Weasel's Roof": 122856,
    "(LVL 3) CARD - Spaghetti Laboratory": 122857,
    "(LVL 3) CARD - Malaria Zone": 122858,
    "(LVL 3) CARD - Barrels Near Gil": 122859,
    "(LVL 3) CARD - Box Near Gil": 122860,
    "(LVL 3) CARD - Squidport Undercover Police Dumpster": 122861,
    "(LVL 3) CARD - Davey Jones Hamper": 122862,
    "(LVL 3) CARD - Rail Near Globex Ship": 122863,
    "(LVL 3) CARD - Hidden Behind Globex Ship Cargo Containers 1": 122864,
    "(LVL 3) CARD - Globex Ship Crane": 122865,
    "(LVL 3) CARD - Hidden Behind Globex Ship Cargo Containers 2": 122866,
    "(LVL 3) CARD - Globex Ship Inside Cargo Container": 122867,
    "(LVL 3) CARD - Globex Ship Upstairs Rail": 122868,
    "(LVL 3) CARD - Taffy Shop": 122869,
    "(LVL 3) CARD - Across From Taffy Shop": 122870,
    "(LVL 3) CARD - KrustyLu Studios Sign": 122871,
    "(LVL 3) CARD - Behind KrustyLu Studios Sign": 122872,
    "(LVL 3) CARD - News Studio": 122873,
    "(LVL 3) CARD - Bridge Near Giant SPRINGFIELD Sign": 122874,
    "(LVL 3) CARD - Motel Balcony": 122875,
    "(LVL 3) CARD - Motel Awning": 122876,
    "(LVL 3) CARD - Observatory 1": 122877,
    "(LVL 3) CARD - Observatory 2": 122878,
    "(LVL 3) CARD - Kamp Krusty Weight Loss Center": 122879,
    "(LVL 3) CARD - Boar's Head at Kamp Krusty": 122880,
    "(LVL 3) CARD - Dam": 122881,
    "(LVL 3) CARD - Parking Spot Across From Android's Dungeon": 122882,
    "(LVL 3) CARD - Above Road Near Drain Pipe": 122883,
    "(LVL 3) CARD - Behind Duff Brewery Truck": 122884,
    "(LVL 3) CARD - Duff Brewery Landing Pad": 122885,

    # Level 3 Wasps
    "(LVL 3) WASP - Observatory": 122463,
    "(LVL 3) WASP - Broken Railing Below Dam": 122464,
    "(LVL 3) WASP - Broken Railing Above Dam (Exit)": 122465,
    "(LVL 3) WASP - Kamp Krusty Near Stage": 122466,
    "(LVL 3) WASP - Kamp Krusty Well": 122467,
    "(LVL 3) WASP - Exit of Kamp Krusty's Well": 122468,
    "(LVL 3) WASP - Motel Complex": 122469,
    "(LVL 3) WASP - Duff Brewery Behind Krusty Glass": 122470,
    "(LVL 3) WASP - Duff Blimp 1": 122471,
    "(LVL 3) WASP - Duff Blimp 2": 122472,
    "(LVL 3) WASP - Krusty Studio Left": 122473,
    "(LVL 3) WASP - Krusty Studio Right": 122474,
    "(LVL 3) WASP - Globex Ship Front End": 122475,
    "(LVL 3) WASP - Globex Ship Next to the Crane": 122476,
    "(LVL 3) WASP - Globex Ship Stairs": 122477,
    "(LVL 3) WASP - LightHouse": 122478,
    "(LVL 3) WASP - Planet Hype": 122479,
    "(LVL 3) WASP - Beach": 122480,
    "(LVL 3) WASP - Bowling Rooftop": 122481,
    "(LVL 3) WASP - Comic Book Guy Rooftop": 122482,

    # Level 3 Gags
    "(LVL 3) GAG - Comic Book Guy Robot": 122490,
    "(LVL 3) GAG - Comic Book Guy Radioactive Man": 122491,
    "(LVL 3) GAG - Yellow Dumpster Across Krusty Burger": 122492,
    "(LVL 3) GAG - Kid Drowning in Ball Pit": 122493,
    "(LVL 3) GAG - Crane on Ship": 122494,
    "(LVL 3) GAG - Observatory Alarm": 122495,
    "(LVL 3) GAG - Perpetual Motion Machine at Observatory": 122496,
    "(LVL 3) GAG - Telescope at Observatory": 122497,
    "(LVL 3) GAG - (Observatory) Monkey": 122498,
    "(LVL 3) GAG - Kamp Krusty Flag": 122499,
    "(LVL 3) GAG - Boar's Head at Kamp Krusty": 122500,

    # Level 3 Shops
    "(LVL 3) Shop Check 1": 122457,
    "(LVL 3) Shop Check 2": 122458,
    "(LVL 3) Shop Check 3": 122459,
    "(LVL 3) Shop Check 4": 122460,
    "(LVL 3) Shop Check 5": 122461,
    "(LVL 3) Shop Check 6": 122462,

    # Level 4 Missions
    "(L4M1) For a Few Donuts More": 122322,
    "(L4M2) Redneck Roundup": 122323,
    "(L4M3) Ketchup Logic": 122324,
    "(L4M4) Return of the Nearly-Dead": 122325,
    "(L4M5) Wolves Stole My Pills": 122326,
    "(L4M6) The Cola Wars": 122327,
    "(L4M7) From Outer Space": 122328,
    "(L4BM) Beached Love": 122329,
    "(LVL 4) Talk to Willie": 122682,

    # Level 4 Races
    "(LVL 4) Checkpoint Race": 122330,
    "(LVL 4) Circuit Race": 122331,
    "(LVL 4) Time Trial Race": 122332,

    # Level 4 Cards
    "(LVL 4) CARD - Gas Station Roof 1": 122888,
    "(LVL 4) CARD - Burns Mansion Secret": 122889,
    "(LVL 4) CARD - Big Bridge": 122890,
    "(LVL 4) CARD - Atop Tower Before Broken Bridge": 122891,
    "(LVL 4) CARD - Roof of House Across From Gold Mansion": 122892,
    "(LVL 4) CARD - Simpsons' Tree House": 122893,
    "(LVL 4) CARD - End of Trailer Park": 122894,
    "(LVL 4) CARD - Neighbor's Carport": 122895,
    "(LVL 4) CARD - Behind Flanders' Tree": 122896,
    "(LVL 4) CARD - Jump Past Neighbor's Playground": 122897,
    "(LVL 4) CARD - Above Kwik-E-Mart": 122898,
    "(LVL 4) CARD - Kwik-E-Mart's Dumpster": 122899,
    "(LVL 4) CARD - Krusty Burger Dumpster": 122900,
    "(LVL 4) CARD - Gas Station Roof 2": 122901,
    "(LVL 4) CARD - Above Street Between Simpson's House and Kwik-E-Mart": 122902,
    "(LVL 4) CARD - Evergreen Terrace Horseshoe Road": 122903,
    "(LVL 4) CARD - Top of Krusty Burger Near Kwik-E-Mart": 122904,
    "(LVL 4) CARD - Retirement Castle": 122905,
    "(LVL 4) CARD - Casa Nova": 122906,
    "(LVL 4) CARD - Shortcut Between Church and Lard Lad": 122907,
    "(LVL 4) CARD - Church Sign": 122908,
    "(LVL 4) CARD - Church Dumpster": 122909,
    "(LVL 4) CARD - Dumpster Behind Krusty Burger Near School": 122910,
    "(LVL 4) CARD - Deli Near School": 122911,
    "(LVL 4) CARD - Back of School Roof": 122912,
    "(LVL 4) CARD - Willie's Shack": 122913,
    "(LVL 4) CARD - Grocery Store Dumpster": 122914,
    "(LVL 4) CARD - Lard Lad Doorbell": 122915,
    "(LVL 4) CARD - House Across From Simpsons' House 1": 122916,
    "(LVL 4) CARD - House Across From Simpsons' House 2": 122917,
    "(LVL 4) CARD - Above Wiggum's": 122918,
    "(LVL 4) CARD - House on Corner Near Graveyard": 122919,
    "(LVL 4) CARD - House Next to Krusty Burger Near Graveyard": 122920,
    "(LVL 4) CARD - Cletus' House": 122921,
    "(LVL 4) CARD - Big Bridge 2": 122922,
    "(LVL 4) CARD - Flanders' House": 122923,
    "(LVL 4) CARD - Moe's House": 122924,
    "(LVL 4) CARD - Nelson's House": 122925,
    "(LVL 4) CARD - Tire Fire": 122926,
    "(LVL 4) CARD - Power Plant": 122927,
    "(LVL 4) CARD - Across From Gil": 122928,
    "(LVL 4) CARD - Back of Cletus' Shack": 122929,
    "(LVL 4) CARD - Tree on Corner Near Graveyard": 122930,
    "(LVL 4) CARD - Above Trailer Park": 122931,
    "(LVL 4) CARD - Above Street Near Barn": 122932,
    "(LVL 4) CARD - Corner of Tomacco Field": 122933,
    "(LVL 4) CARD - Beside School": 122934,
    "(LVL 4) CARD - Power Plant Parking Lot 1": 122935,
    "(LVL 4) CARD - Power Plant Parking Lot 2": 122936,
    "(LVL 4) CARD - Above Street Near Simpsons' House": 122937,
    "(LVL 4) CARD - Power Plant Platforming 1": 122938,
    "(LVL 4) CARD - Power Plant Platforming 2": 122939,
    "(LVL 4) CARD - Homer's Workstation": 122940,
    "(LVL 4) CARD - Above Nuclear Waste Bridge": 122941,
    "(LVL 4) CARD - Outside Stonecutter Tunnel": 122942,
    "(LVL 4) CARD - Rich Side Gas Station's Dumpster": 122943,
    "(LVL 4) CARD - Roof Across of House Across From Gold Mansion": 122944,
    "(LVL 4) CARD - Outside Burns Mansion Gate": 122945,
    "(LVL 4) CARD - Broken Bridge": 122946,
    "(LVL 4) CARD - Rocket Car": 122947,
    "(LVL 4) CARD - Burns Mansion Backyard": 122948,
    "(LVL 4) CARD - Burns Mansion": 122949,
    "(LVL 4) CARD - Chessboard": 122950,

    # Level 4 Wasps
    "(LVL 4) WASP - Blue House Before Krusty Glass 1": 122501,
    "(LVL 4) WASP - Blue House Before Krusty Glass 2": 122502,
    "(LVL 4) WASP - Flander's Backyard": 122503,
    "(LVL 4) WASP - Wiggum's Backyard 1": 122504,
    "(LVL 4) WASP - Wiggum's Backyard 2": 122505,
    "(LVL 4) WASP - Kwik-E-Mart Rooftop": 122506,
    "(LVL 4) WASP - Gas Station Rooftop": 122507,
    "(LVL 4) WASP - Atop Gasoline Pump": 122508,
    "(LVL 4) WASP - Mr. Burns Giant ChessBoard 1": 122509,
    "(LVL 4) WASP - Mr. Burns Giant ChessBoard 2": 122510,
    "(LVL 4) WASP - Mr. Burns StairCase": 122511,
    "(LVL 4) WASP - Mr. Burns Library": 122512,
    "(LVL 4) WASP - Outside of Homer's Workstation": 122513,
    "(LVL 4) WASP - Atop Trailer Park": 122514,
    "(LVL 4) WASP - In Trailer Park": 122515,
    "(LVL 4) WASP - Barn": 122516,
    "(LVL 4) WASP - Behind School Steps": 122517,
    "(LVL 4) WASP - School Rooftop 1": 122518,
    "(LVL 4) WASP - School Rooftop 2": 122519,
    "(LVL 4) WASP - Atop Tower Before Broken Bridge": 122520,

    # Level 4 Gags
    "(LVL 4) GAG - Simpson TV": 122528,
    "(LVL 4) GAG - Simpsons Swings": 122529,
    "(LVL 4) GAG - Simpsons Grill": 122530,
    "(LVL 4) GAG - Simpsons Fire Breathing Tiki": 122531,
    "(LVL 4) GAG - Krusty Lamp (Bart's Room)": 122532,
    "(LVL 4) GAG - Flanders Bomb Shelter": 122533,
    "(LVL 4) GAG - Tank in Front of Power Plant": 122534,
    "(LVL 4) GAG - Homer's Workstation Meltdown": 122535,
    "(LVL 4) GAG - School Fire Extinguisher ": 122536,
    "(LVL 4) GAG - School Fire Alarm": 122537,
    "(LVL 4) GAG - Frozen man in Kwik-E-Mart": 122538,
    "(LVL 4) GAG - Silent Alarm in Kwik-E-Mart": 122539,
    "(LVL 4) GAG - ATM in Kwik-E-Mart": 122540,
    "(LVL 4) GAG - Arcade Cabinet in Kwik-E-Mart": 122541,
    "(LVL 4) GAG - Squishee Machine in Kwik-E-Mart": 122542,

    # Level 4 Shops
    "(LVL 4) Shop Check 1": 122543,
    "(LVL 4) Shop Check 2": 122544,
    "(LVL 4) Shop Check 3": 122545,
    "(LVL 4) Shop Check 4": 122546,
    "(LVL 4) Shop Check 5": 122547,
    "(LVL 4) Shop Check 6": 122548,

    # Level 5 Missions
    "(L5M1) Incriminating Caffeine": 122333,
    "(L5M2) ...and Baby Makes 8": 122334,
    "(L5M3) Eight is Too Much": 122335,
    "(L5M4) This Little Piggy": 122336,
    "(L5M5) Never Trust a Snake": 122337,
    "(L5M6) Kwik Cash": 122338,
    "(L5M7) Curious Curator": 122339,
    "(L5BM) Kinky Frinky": 122340,
    "(LVL 5) Talk to Homer": 122683,

    # Level 5 Races
    "(LVL 5) Checkpoint Race": 122343,
    "(LVL 5) Circuit Race": 122342,
    "(LVL 5) Time Trial Race": 122341,

    # Level 5 Cards
    "(LVL 5) CARD - Construction Crane Platforming": 122951,
    "(LVL 5) CARD - The Legitimate Businessman's Social Club": 122952,
    "(LVL 5) CARD - Moe's Roof": 122953,
    "(LVL 5) CARD - On Top of Train Across Water Tower": 122954,
    "(LVL 5) CARD - Closed Highway Jump": 122955,
    "(LVL 5) CARD - Downtown Billboard Platforming": 122956,
    "(LVL 5) CARD - Monorail Track": 122957,
    "(LVL 5) CARD - Courthouse Light Pole": 122958,
    "(LVL 5) CARD - Behind Museum Sign": 122959,
    "(LVL 5) CARD - Lion Statue": 122960,
    "(LVL 5) CARD - Park Fountain near Hospital": 122961,
    "(LVL 5) CARD - Hospital Doors": 122962,
    "(LVL 5) CARD - Above Street Near Hospital Parking Lot": 122963,
    "(LVL 5) CARD - Town Hall (Stadium Side)": 122964,
    "(LVL 5) CARD - Stadium Behind Duff Mascot": 122965,
    "(LVL 5) CARD - Stadium Ledge Bench": 122966,
    "(LVL 5) CARD - Tunnel Pillar Near Stadium": 122967,
    "(LVL 5) CARD - Tunnel Pillar Near Downtown": 122968,
    "(LVL 5) CARD - Stadium Billboard": 122969,
    "(LVL 5) CARD - Fire Truck Jump": 122970,
    "(LVL 5) CARD - Tree By Krusty Burger Downtown": 122971,
    "(LVL 5) CARD - Sit N Rotate": 122972,
    "(LVL 5) CARD - Downtown Bank": 122973,
    "(LVL 5) CARD - Monorail": 122974,
    "(LVL 5) CARD - Corner of Monorail Station": 122975,
    "(LVL 5) CARD - Above Street Near Downtown Krusty Float": 122976,
    "(LVL 5) CARD - Ramp Behind Downtown Krusty Burger": 122977,
    "(LVL 5) CARD - Deli Near Monorail": 122978,
    "(LVL 5) CARD - Above Downtown Highway Exit": 122979,
    "(LVL 5) CARD - Closed Highway": 122980,
    "(LVL 5) CARD - Main Highway": 122981,
    "(LVL 5) CARD - East Side Highway Exit": 122982,
    "(LVL 5) CARD - Try N Save Parking Lot": 122983,
    "(LVL 5) CARD - Behind Herman's Military Antiques": 122984,
    "(LVL 5) CARD - Above Street Near Helter Shelter": 122985,
    "(LVL 5) CARD - DMV Sign": 122986,
    "(LVL 5) CARD - DMV Light Pole": 122987,
    "(LVL 5) CARD - Above Street Between DMV and Trainyard": 122988,
    "(LVL 5) CARD - Between Trains": 122989,
    "(LVL 5) CARD - Above Train Crossing": 122990,
    "(LVL 5) CARD - Behind Moving Train": 122991,
    "(LVL 5) CARD - Train Stairs": 122992,
    "(LVL 5) CARD - Near Grease Recycling Plant": 122993,
    "(LVL 5) CARD - Outside Trainyard Parking Spot": 122994,
    "(LVL 5) CARD - Above Street Near Car Wash": 122995,
    "(LVL 5) CARD - On Top of Gas Station at Car Wash": 122996,
    "(LVL 5) CARD - Inside Trainyard Parking Spot": 122997,
    "(LVL 5) CARD - Lexicon Bookstore Roof": 122998,
    "(LVL 5) CARD - King Toot's Music Store Roof": 122999,
    "(LVL 5) CARD - Alley Behind King Toot's Music Store": 123000,
    "(LVL 5) CARD - Legitimate Businessman's Roof 2": 123001,
    "(LVL 5) CARD - Glen's Grocery Roof": 123002,
    "(LVL 5) CARD - Stop Sign Across From Moe's": 123003,
    "(LVL 5) CARD - Platform Behind Lard Lad's": 123005,
    "(LVL 5) CARD - Street Near Construction": 123006,
    "(LVL 5) CARD - Under Construction Building Between Krusty Burger and Lard Lad's": 123007,
    "(LVL 5) CARD - Krusty Burger Sign": 123008,
    "(LVL 5) CARD - Near Concrete Mixer": 123009,
    "(LVL 5) CARD - Gazebo Between Museum & Court House": 123010,
    "(LVL 5) CARD - Monkey Box": 123011,
    "(LVL 5) CARD - Hospital Sign": 123012,
    "(LVL 5) CARD - Magnifying Glass Parking Lot": 123013,
    "(LVL 5) CARD - Police Station": 123014,
    "(LVL 5) CARD - Tree Outside Police Station": 123015,
    "(LVL 5) CARD - 50% Off Sign Near Monorail": 123016,
    "(LVL 5) CARD - Wooden Tower": 123017,
    "(LVL 5) CARD - Town Hall Front": 123018,
    "(LVL 5) CARD - Coming Soon Construction": 123019,

    # Level 5 Wasps
    "(LVL 5) WASP - Front of Hospital": 122549,
    "(LVL 5) WASP - Gazebo Between Museum & Court House": 122550,
    "(LVL 5) WASP - Steps of Town Hall": 122551,
    "(LVL 5) WASP - Museum Steps": 122552,
    "(LVL 5) WASP - Rooftop Next to Moes": 122553,
    "(LVL 5) WASP - Legitimate Businessman's Rooftop 1": 122554,
    "(LVL 5) WASP - Legitimate Businessman's Rooftop 2": 122555,
    "(LVL 5) WASP - Trainyard Stairs": 122556,
    "(LVL 5) WASP - Other Side of Moving Train": 122557,
    "(LVL 5) WASP - Watertower 1": 122558,
    "(LVL 5) WASP - Watertower 2": 122559,
    "(LVL 5) WASP - Police Station Steps": 122560,
    "(LVL 5) WASP - Monorail Stairs": 122561,
    "(LVL 5) WASP - Monorail": 122562,
    "(LVL 5) WASP - Otherside of Monorail 1": 122563,
    "(LVL 5) WASP - Otherside of Monorail 2": 122564,
    "(LVL 5) WASP - Under Giant Purple Beams 1": 122565,
    "(LVL 5) WASP - Under Giant Purple Beams 2": 122566,
    "(LVL 5) WASP - Alleyway Rooftop": 122567,
    "(LVL 5) WASP - Fountain Near Stadium": 122568,

    # Level 5 Gags
    "(LVL 5) GAG - Pickled Egg in Moe's": 122576,
    "(LVL 5) GAG - Slot Machine in Moe's": 122577,
    "(LVL 5) GAG - Love Tester in Moe's": 122578,
    "(LVL 5) GAG - Blind Hans Moleman at the DMV": 122579,
    "(LVL 5) GAG - Dumpster Behind Behind Krusty Burger (Near Police Station)": 122580,
    "(LVL 5) GAG - Light Up Drinks in Moe's": 122690,

    # Level 5 Shops
    "(LVL 5) Shop Check 1": 122581,
    "(LVL 5) Shop Check 2": 122582,
    "(LVL 5) Shop Check 3": 122583,
    "(LVL 5) Shop Check 4": 122584,
    "(LVL 5) Shop Check 5": 122585,
    "(LVL 5) Shop Check 6": 122586,

    # Level 6 Missions
    "(L6M1) Going to the Lu'": 122344,
    "(L6M2) Getting Down with the Clown": 122345,
    "(L6M3) Lab Coat Caper": 122346,
    "(L6M4) Duff for Me, Duff for You": 122347,
    "(L6M5) Full Metal Jackass": 122348,
    "(L6M6) Set to Kill": 122349,
    "(L6M7) Kang and Kodos Strike Back": 122350,
    "(L6BM) Milking The Pigs": 122351,
    "(LVL 6) Talk to Kearney": 122684,

    # Level 6 Races
    "(LVL 6) Checkpoint Race": 122352,
    "(LVL 6) Time Trial Race": 122353,
    "(LVL 6) Circuit Race": 122354,

    # Level 6 Cards
    "(LVL 6) CARD - Above Street BallPit House": 123020,
    "(LVL 6) CARD - Casino Ramp": 123021,
    "(LVL 6) CARD - Planet Hype Sign": 123022,
    "(LVL 6) CARD - Atop Front of Boat": 123023,
    "(LVL 6) CARD - Duff Blimp": 123024,
    "(LVL 6) CARD - Hidden in Bush Next to Kamp Krusty Well Exit": 123025,
    "(LVL 6) CARD - Broken Bridge": 123026,
    "(LVL 6) CARD - Behind Lighthouse": 123027,
    "(LVL 6) CARD - Pelican Behind Planet Hype 1": 123028,
    "(LVL 6) CARD - Pelican Behind Planet Hype 2": 123029,
    "(LVL 6) CARD - Planet Hype Outdoor Seating": 123030,
    "(LVL 6) CARD - Pelican in Front of Planet Hype 1": 123031,
    "(LVL 6) CARD - Pelican in Front of Planet Hype 2": 123032,
    "(LVL 6) CARD - Pelican Near Squidport Arch": 123033,
    "(LVL 6) CARD - Little Boats on Beach": 123034,
    "(LVL 6) CARD - Big Boat on Beach": 123035,
    "(LVL 6) CARD - Deck by Squidport Pedestrian Entrance 1": 123036,
    "(LVL 6) CARD - Deck by Squidport Pedestrian Entrance 2": 123037,
    "(LVL 6) CARD - Casino Bushes Near Squidport": 123038,
    "(LVL 6) CARD - Lower Casino Entrance": 123039,
    "(LVL 6) CARD - Sidewalk Near Casino Ramp 1": 123040,
    "(LVL 6) CARD - Behind Casino Ramp": 123041,
    "(LVL 6) CARD - Sidewalk Near Casino Ramp 2": 123042,
    "(LVL 6) CARD - Houses Near Bowl-a-Rama": 123043,
    "(LVL 6) CARD - Jazz Hole": 123044,
    "(LVL 6) CARD - Krusty Burger Parking Lot": 123045,
    "(LVL 6) CARD - Gated Houses Near Aztec Theater": 123046,
    "(LVL 6) CARD - Boulevard Near Krusty and Friends Billboard": 123047,
    "(LVL 6) CARD - Stairs Near Krusty and Friends Billboard": 123048,
    "(LVL 6) CARD - Short Wall Down the Street from Gas Station": 123049,
    "(LVL 6) CARD - Concrete Mixer at Gas Station": 123050,
    "(LVL 6) CARD - Green Building Across From Principal Skinner": 123051,
    "(LVL 6) CARD - Lumber King Billboard": 123052,
    "(LVL 6) CARD - Park Across From Android's Dungeon": 123053,
    "(LVL 6) CARD - Behind Krusty Burger Across From Android's Dungeon": 123054,
    "(LVL 6) CARD - Wall E Weasel's Roof": 123055,
    "(LVL 6) CARD - Spaghetti Laboratory": 123056,
    "(LVL 6) CARD - Malaria Zone": 123057,
    "(LVL 6) CARD - Barrels Near Gil": 123058,
    "(LVL 6) CARD - Box Near Gil": 123059,
    "(LVL 6) CARD - Squidport Undercover Police Dumpster": 123060,
    "(LVL 6) CARD - Davey Jones Hamper": 123061,
    "(LVL 6) CARD - Rail Near Globex Ship": 123062,
    "(LVL 6) CARD - Hidden Behind Globex Ship Cargo Containers 1": 123063,
    "(LVL 6) CARD - Globex Ship Crane": 123064,
    "(LVL 6) CARD - Hidden Behind Globex Ship Cargo Containers 2": 123065,
    "(LVL 6) CARD - Globex Ship Inside Cargo Container": 123066,
    "(LVL 6) CARD - Globex Ship Upstairs Rail": 123067,
    "(LVL 6) CARD - Taffy Shop": 123068,
    "(LVL 6) CARD - Across From Taffy Shop": 123069,
    "(LVL 6) CARD - KrustyLu Studios Sign": 123070,
    "(LVL 6) CARD - Behind KrustyLu Studios Sign": 123071,
    "(LVL 6) CARD - News Studio": 123072,
    "(LVL 6) CARD - Bridge Near Giant SPRINGFIELD Sign": 123073,
    "(LVL 6) CARD - Motel Balcony": 123074,
    "(LVL 6) CARD - Motel Awning": 123075,
    "(LVL 6) CARD - Observatory 1": 123076,
    "(LVL 6) CARD - Observatory 2": 123077,
    "(LVL 6) CARD - Kamp Krusty Weight Loss Center": 123078,
    "(LVL 6) CARD - Boar's Head at Kamp Krusty": 123079,
    "(LVL 6) CARD - Dam": 123080,
    "(LVL 6) CARD - Parking Spot Across From Android's Dungeon": 123081,
    "(LVL 6) CARD - Above Road Near Drain Pipe": 123082,
    "(LVL 6) CARD - Behind Duff Brewery Truck": 123083,
    "(LVL 6) CARD - Duff Brewery Landing Pad": 123084,
    "(LVL 6) CARD - Captain Chum 'N' Stuff": 123085,
    "(LVL 6) CARD - Upper Casino Entrance": 123086,

    # Level 6 Wasps
    "(LVL 6) WASP - Observatory 1": 122590,
    "(LVL 6) WASP - Observatory 2": 122591,
    "(LVL 6) WASP - Kamp Krusty 1": 122592,
    "(LVL 6) WASP - Kamp Krusty 2": 122593,
    "(LVL 6) WASP - Broken Railing Below Dam": 122594,
    "(LVL 6) WASP - Broken Railing Exit": 122595,
    "(LVL 6) WASP - Motel": 122596,
    "(LVL 6) WASP - Duff Brewery Krusty Glass": 122597,
    "(LVL 6) WASP - Under Duff Blimp": 122598,
    "(LVL 6) WASP - Krusty Studio Left": 122599,
    "(LVL 6) WASP - Krusty Studio Right": 122600,
    "(LVL 6) WASP - Krusty Studio Balcony": 122601,
    "(LVL 6) WASP - Globex Ship Crane": 122602,
    "(LVL 6) WASP - Globex Ship Staircase 1": 122603,
    "(LVL 6) WASP - Globex Ship Staircase 2": 122604,
    "(LVL 6) WASP - Lighthouse": 122605,
    "(LVL 6) WASP - Planet Hype Rooftop": 122606,
    "(LVL 6) WASP - Bowling Rooftop": 122607,
    "(LVL 6) WASP - Comic Book Guy Rooftop 1": 122608,
    "(LVL 6) WASP - Comic Book Guy Rooftop 2": 122609,

    # Level 6 Gags
    "(LVL 6) GAG - Comic Book Guy Robot": 122617,
    "(LVL 6) GAG - Comic Book Guy Radioactive Man": 122618,
    "(LVL 6) GAG - Yellow Dumpster Across Krusty Burger": 122619,
    "(LVL 6) GAG - Kid Drowning in Ball Pit": 122620,
    "(LVL 6) GAG - Crane on Ship": 122621,
    "(LVL 6) GAG - Observatory Alarm": 122622,
    "(LVL 6) GAG - Perpetual Motion Machine at Observatory": 122623,
    "(LVL 6) GAG - Telescope at Observatory": 122624,
    "(LVL 6) GAG - (Observatory) Monkey": 122625,
    "(LVL 6) GAG - Kamp Krusty Flag": 122626,
    "(LVL 6) GAG - Boar's Head at Kamp Krusty": 122627,

    # Level 6 Shops
    "(LVL 6) Shop Check 1": 122587,
    "(LVL 6) Shop Check 2": 122588,
    "(LVL 6) Shop Check 3": 122589,
    "(LVL 6) Shop Check 4": 122628,
    "(LVL 6) Shop Check 5": 122629,
    "(LVL 6) Shop Check 6": 122630,

    # Level 7 Missions
    "(L7M1) Rigor Motors": 122355,
    "(L7M2) Long Black Probes": 122356,
    "(L7M3) Pocket Protector": 122357,
    "(L7M4) There's Something About Monty": 122358,
    "(L7M5) Alien \"Auto\"topsy Part 1": 122359,
    "(L7M6) Alien \"Auto\"topsy Part 2": 122360,
    "(L7M7) Alien \"Auto\"topsy Part 3": 122361,
    "(L7BM) Flaming Tires": 122362,
    "(LVL 7) Talk to Graveyard Zombie": 122685,

    # Level 7 Races
    "(LVL 7) Time Trial Race": 122363,
    "(LVL 7) Circuit Race": 122364,
    "(LVL 7) Checkpoint Race": 122365,

    # Level 7 Cards
    "(LVL 7) CARD - Flanders Bomb Shelter": 123087,
    "(LVL 7) CARD - Blue House Haunted Playground": 123088,
    "(LVL 7) CARD - School Playground": 123089,
    "(LVL 7) CARD - Atop of Lard Lad": 123090,
    "(LVL 7) CARD - Cemetery Moat": 123091,
    "(LVL 7) CARD - Barn Silo": 123092,
    "(LVL 7) CARD - Mr. Burns Office": 123093,
    "(LVL 7) CARD - Neighbor's Carport": 123094,
    "(LVL 7) CARD - Behind Flanders' Tree": 123095,
    "(LVL 7) CARD - Jump Past Neighbor's Playground": 123096,
    "(LVL 7) CARD - Above Kwik-E-Mart": 123097,
    "(LVL 7) CARD - Kwik-E-Mart's Dumpster": 123098,
    "(LVL 7) CARD - Krusty Burger's Dumpster": 123099,
    "(LVL 7) CARD - Gas Station Roof": 123100,
    "(LVL 7) CARD - Above Street Between Simpsons' House and Kwik-E-Mart": 123101,
    "(LVL 7) CARD - Evergreen Terrace Horseshoe Road": 123102,
    "(LVL 7) CARD - Retirement Castle": 123103,
    "(LVL 7) CARD - Casa Nova": 123104,
    "(LVL 7) CARD - Shortcut Between Church and Lard Lad": 123105,
    "(LVL 7) CARD - Church Sign": 123106,
    "(LVL 7) CARD - Church Dumpster": 123107,
    "(LVL 7) CARD - Dumpster Behind Krusty Burger Near School": 123108,
    "(LVL 7) CARD - Deli Near School": 123109,
    "(LVL 7) CARD - Back of School Roof": 123110,
    "(LVL 7) CARD - Willie's Shack": 123111,
    "(LVL 7) CARD - Grocery Store's Dumpster": 123112,
    "(LVL 7) CARD - Lard Lad Doorbell": 123113,
    "(LVL 7) CARD - House Across From Simpsons' House 1": 123114,
    "(LVL 7) CARD - House Across From Simpsons' House 2": 123115,
    "(LVL 7) CARD - Above Wiggum's": 123116,
    "(LVL 7) CARD - House on Corner Near Graveyard": 123117,
    "(LVL 7) CARD - House Next to Krusty Burger Near Graveyard": 123118,
    "(LVL 7) CARD - Cletus' House": 123119,
    "(LVL 7) CARD - Big Bridge": 123120,
    "(LVL 7) CARD - Flanders' House": 123121,
    "(LVL 7) CARD - Moe's House": 123122,
    "(LVL 7) CARD - Nelson's House": 123123,
    "(LVL 7) CARD - Tire Fire": 123124,
    "(LVL 7) CARD - Power Plant": 123125,
    "(LVL 7) CARD - Across From Gil": 123126,
    "(LVL 7) CARD - Back of Cletus' Shack": 123127,
    "(LVL 7) CARD - Tree on Corner Near Graveyard": 123128,
    "(LVL 7) CARD - Above Trailer Park": 123130,
    "(LVL 7) CARD - Above Street Near Barn": 123131,
    "(LVL 7) CARD - Corner of Tomacco Field": 123132,
    "(LVL 7) CARD - Beside School": 123133,
    "(LVL 7) CARD - Power Plant Parking Lot 1": 123134,
    "(LVL 7) CARD - Power Plant Parking Lot 2": 123135,
    "(LVL 7) CARD - Power Plant Wreckage 1": 123136,
    "(LVL 7) CARD - Power Plant Wreckage 2": 123137,
    "(LVL 7) CARD - Power Plant Wreckage 3": 123138,
    "(LVL 7) CARD - Burns' Office Chair": 123139,
    "(LVL 7) CARD - Cemetery Skeleton": 123140,
    "(LVL 7) CARD - Cemetery Crypt": 123141,
    "(LVL 7) CARD - Cemetery Tree": 123142,
    "(LVL 7) CARD - Cemetery": 123143,
    "(LVL 7) CARD - Ghost": 123144,

    # Level 7 Wasps
    "(LVL 7) WASP - Blue House Haunted Playground": 122634,
    "(LVL 7) WASP - Blue House Backyard": 122635,
    "(LVL 7) WASP - Simpsons' Backyard": 122636,
    "(LVL 7) WASP - Flanders' Backyard": 122637,
    "(LVL 7) WASP - Wiggum's Backyard": 122638,
    "(LVL 7) WASP - Atop of Kwik-E-Mart": 122639,
    "(LVL 7) WASP - Atop of Gasoline": 122640,
    "(LVL 7) WASP - Lard Lad Rooftop": 122641,
    "(LVL 7) WASP - Krusty Burger Rooftop": 122642,
    "(LVL 7) WASP - School Playground": 122643,
    "(LVL 7) WASP - The One Being Abducted": 122644,
    "(LVL 7) WASP - School Roof 1": 122645,
    "(LVL 7) WASP - School Roof 2": 122646,
    "(LVL 7) WASP - Bridge Barricade": 122647,
    "(LVL 7) WASP - Bridge Frame by Cletus": 122648,
    "(LVL 7) WASP - TrailerPark 1": 122649,
    "(LVL 7) WASP - TrailerPark 2": 122650,
    "(LVL 7) WASP - Barn Silo": 122651,
    "(LVL 7) WASP - Power Plant Parking lot": 122652,
    "(LVL 7) WASP - Mr. Burns Office": 122653,

    # Level 7 Gags
    "(LVL 7) GAG - Simpsons TV": 122661,
    "(LVL 7) GAG - Simpsons Swing": 122662,
    "(LVL 7) GAG - Simpsons Fire Breathing Tiki": 122663,
    "(LVL 7) GAG - Krusty Lamp (Bart's Room)": 122664,
    "(LVL 7) GAG - Clown Bed (Bart's Room)": 122665,
    "(LVL 7) GAG - Flanders Bomb Shelter": 122666,
    "(LVL 7) GAG - Blue House Haunted Swing": 122667,
    "(LVL 7) GAG - Tank in Front of Power Plant": 122668,
    "(LVL 7) GAG - Frozen Man in Kwik-E-Mart": 122669,
    "(LVL 7) GAG - Silent Alarm in Kwik-E-Mart": 122670,
    "(LVL 7) GAG - Squishee Machine in Kwik-E-Mart": 122671,
    "(LVL 7) GAG - ATM in Kwik-E-Mart": 122672,
    "(LVL 7) GAG - Arcade Cabinet in Kwik-E-Mart": 122673,
    "(LVL 7) GAG - School Fire Alarm": 122674,
    "(LVL 7) GAG - School Fire Extinguisher": 122675,

    # Level 7 Shops
    "(LVL 7) Shop Check 1": 122631,
    "(LVL 7) Shop Check 2": 122632,
    "(LVL 7) Shop Check 3": 122633,
    "(LVL 7) Shop Check 4": 122676,
    "(LVL 7) Shop Check 5": 122677,
    "(LVL 7) Shop Check 6": 122678,
}
LOCATION_ID_TO_NAME = {v: k for k, v in LOCATION_NAME_TO_ID.items()}

location_name_groups = {
    group_name: group_set
    for level in range(1, 8)
    for group_name, group_set in {
        f"Level {level} Missions": {
            name for name in LOCATION_NAME_TO_ID
            if name.startswith(f"(L{level}M") or name.startswith(f"(L{level}BM)")
        },
        f"Level {level} Races": {
            name for name in LOCATION_NAME_TO_ID
            if name.startswith(f"(LVL {level})") and "Race" in name
        },
        f"Level {level} Cards": {
            name for name in LOCATION_NAME_TO_ID
            if name.startswith(f"(LVL {level}) CARD")
        },
        f"Level {level} Wasps": {
            name for name in LOCATION_NAME_TO_ID
            if name.startswith(f"(LVL {level}) WASP")
        },
        f"Level {level} Gags": {
            name for name in LOCATION_NAME_TO_ID
            if name.startswith(f"(LVL {level}) GAG")
        },
        f"Level {level} Shops": {
            name for name in LOCATION_NAME_TO_ID
            if name.startswith(f"(LVL {level}) Shop")
        },
    }.items()
}

class SimpsonsHitNRunLocation(Location):
    game = "Simpsons Hit and Run"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: SimpsonsHitNRunWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: SimpsonsHitNRunWorld):
    hub = world.get_region("Hub")

    level_regions = [world.get_region("Level 1"), world.get_region("Level 2"), world.get_region("Level 3"),
                     world.get_region("Level 4"), world.get_region("Level 5"), world.get_region("Level 6"), world.get_region("Level 7")]

    level_mission_regions = [world.get_region("Level 1 Missions"), world.get_region("Level 2 Missions"), world.get_region("Level 3 Missions"),
                             world.get_region("Level 4 Missions"), world.get_region("Level 5 Missions"), world.get_region("Level 6 Missions"), world.get_region("Level 7 Missions")]

    level_race_regions = [world.get_region("Level 1 Races"), world.get_region("Level 2 Races"), world.get_region("Level 3 Races"),
                          world.get_region("Level 4 Races"), world.get_region("Level 5 Races"), world.get_region("Level 6 Races"), world.get_region("Level 7 Races")]

    level_wasp_regions = [world.get_region("Level 1 Wasps"), world.get_region("Level 2 Wasps"), world.get_region("Level 3 Wasps"),
                          world.get_region("Level 4 Wasps"), world.get_region("Level 5 Wasps"), world.get_region("Level 6 Wasps"), world.get_region("Level 7 Wasps")]

    level_card_regions = [world.get_region("Level 1 Cards"), world.get_region("Level 2 Cards"), world.get_region("Level 3 Cards"),
                          world.get_region("Level 4 Cards"), world.get_region("Level 5 Cards"), world.get_region("Level 6 Cards"), world.get_region("Level 7 Cards")]

    level_gag_regions = [world.get_region("Level 1 Gags"), world.get_region("Level 2 Gags"), world.get_region("Level 3 Gags"),
                         world.get_region("Level 4 Gags"), world.get_region("Level 5 Gags"), world.get_region("Level 6 Gags"), world.get_region("Level 7 Gags")]

    level_shop_regions = [world.get_region("Level 1 Shops"), world.get_region("Level 2 Shops"), world.get_region("Level 3 Shops"),
                          world.get_region("Level 4 Shops"), world.get_region("Level 5 Shops"), world.get_region("Level 6 Shops"), world.get_region("Level 7 Shops")]

    for i in range(7):
        level_num = i + 1

        lvl_mission_locs = [
            name for name in LOCATION_NAME_TO_ID
            if re.match(rf"^\(L{level_num}(M\d+|BM)\)", name)
        ]

        lvl_mission_locs.append(next(
            name for name in LOCATION_NAME_TO_ID
            if name.startswith(f"(LVL {level_num}) Talk to")
        ))

        level_mission_regions[i].add_locations(get_location_names_with_ids(lvl_mission_locs), SimpsonsHitNRunLocation)

        lvl_race_locs = [
            name for name in LOCATION_NAME_TO_ID
            if re.match(rf"^\(LVL {level_num}\).*Race$", name)
        ]

        level_race_regions[i].add_locations(get_location_names_with_ids(lvl_race_locs), SimpsonsHitNRunLocation)

        lvl_card_locs = [
            name for name in LOCATION_NAME_TO_ID
            if re.match(rf"^\(LVL {level_num}\) CARD - .+", name)
        ]
        if world.options.Shuffle_Cards:
            if not hasattr(world.multiworld, "generation_is_fake"):
                lvl_card_locs = world.random.sample(lvl_card_locs, 7)
            else:
                lvl_card_locs = [card.name for card in world.card_table[i * 7:(i + 1) * 7]]
        else:
            lvl_card_locs = lvl_card_locs[:7]

        fill_card_table(world, i, lvl_card_locs)
        level_card_regions[i].add_locations(get_location_names_with_ids(lvl_card_locs), SimpsonsHitNRunLocation)

        lvl_wasp_locs = [
            name for name in LOCATION_NAME_TO_ID
            if re.match(rf"^\(LVL {level_num}\) WASP - .+", name)
        ]

        level_wasp_regions[i].add_locations(get_location_names_with_ids(lvl_wasp_locs), SimpsonsHitNRunLocation)

        lvl_gag_locs = [
            name for name in LOCATION_NAME_TO_ID
            if re.match(rf"^\(LVL {level_num}\) GAG - .+", name)
        ]

        level_gag_regions[i].add_locations(get_location_names_with_ids(lvl_gag_locs), SimpsonsHitNRunLocation)

        lvl_shop_locs = [
            name for name in LOCATION_NAME_TO_ID
            if re.match(rf"^\(LVL {level_num}\) Shop Check.+", name)
        ]

        level_shop_regions[i].add_locations(get_location_names_with_ids(lvl_shop_locs), SimpsonsHitNRunLocation)


def create_events(world: SimpsonsHitNRunWorld) -> None:
    # Don't need this for now.
    pass

def fill_card_table(world: SimpsonsHitNRunWorld, level: int, chosen_cards: list[str]):
    for i, name in enumerate(chosen_cards):
        data = cards_by_name[name]
        gameid = (level + 1) * 10 + (i + 1)

        world.card_table.append(
            Card(
                id = LOCATION_NAME_TO_ID[name],
                name = name,
                gameid = gameid,
                x = data["X"],
                y = data["Y"],
                z = data["Z"]
            )
        )

#For use by UT
def fill_card_table_by_id(world: SimpsonsHitNRunWorld, card_locations: list[int]):
    for i, card_id in enumerate(card_locations):
        data = cards_by_name[LOCATION_ID_TO_NAME[card_id]]

        world.card_table.append(
            Card(
                id=card_id,
                name=data["Desc"],
                gameid=i + 1, #this doesn't really matter for UT
                x=data["X"],
                y=data["Y"],
                z=data["Z"],
            )
        )
