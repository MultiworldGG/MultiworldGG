from typing import Callable, Dict, List, NamedTuple, Optional, Set, TYPE_CHECKING

from BaseClasses import Location

from . import Data

if TYPE_CHECKING:
    from . import MMZero3World


class MMZero3Location(Location):
    game = "Mega Man Zero 3"


class MMZero3LocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["MMZero3World"], bool] = lambda world: True
    locked_item: Optional[str] = None


# Stage names as they appear in game order
stage_names = [
    "Derelict Spacecraft", "Aegis Volcano Base", "Oceanic Highway Ruins",
    "Weapons Repair Factory", "Old Residential", "Missile Factory",
    "Twilight Desert", "Forest of Anatre", "Frontline Ice Base",
    "Area X-2", "Energy Facility", "Snowy Plains",
    "Sunken Library", "Giant Elevator", "Sub Arcadia"
]

def extra_life_sanity_on(world: "MMZero3World") -> bool:
    return world.options.extra_life_sanity.value

def itemsanity_on(world: "MMZero3World") -> bool:
    return world.options.itemsanity.value

location_data_table: Dict[str, MMZero3LocationData] = {

    "Resistance Base 023: Room 02D - 1 Story Progress": MMZero3LocationData(region="Resistance Base 2", address=23),
    "Resistance Base 044: Talk to Rocinolle - 2 Story Progress": MMZero3LocationData(region="Resistance Base 3", address=44),
    "Resistance Base 058: Talk to Right Tower Soldier": MMZero3LocationData(region="Resistance Base 1", address=58),
    "Resistance Base 092: Talk to Cerveau": MMZero3LocationData(region="Resistance Base 1", address=92),
    "Resistance Base 099: Room 03D": MMZero3LocationData(region="Resistance Base 1", address=99),
    "Resistance Base 106: Left Corner of Rooftop": MMZero3LocationData(region="Resistance Base 1", address=106),
    "Resistance Base 107: Talk to Andrew - 1 Story Progress": MMZero3LocationData(region="Resistance Base 2", address=107),
    "Resistance Base 116: Talk to Alouette - 1 Story Progress": MMZero3LocationData(region="Resistance Base 2", address=116),
    "Resistance Base 165: Near Alouette": MMZero3LocationData(region="Resistance Base 1", address=165),
    "Resistance Base 166: Near Cerveau": MMZero3LocationData(region="Resistance Base 1", address=166),
    "Resistance Base 167: Talk to Rocinolle": MMZero3LocationData(region="Resistance Base 1", address=167),
    "Resistance Base 168: 2nd Floor Hall": MMZero3LocationData(region="Resistance Base 1", address=168),
    "Resistance Base 169: Talk to Hibou - 1 Story Progress": MMZero3LocationData(region="Resistance Base 2", address=169),
    "Resistance Base 170: Near Rocinolle": MMZero3LocationData(region="Resistance Base 1", address=170),
    "Resistance Base 171: Left Room on 1st Floor": MMZero3LocationData(region="Resistance Base 1", address=171),
    "Resistance Base 172: Right Room on 1st Floor": MMZero3LocationData(region="Resistance Base 1", address=172),
    "Resistance Base 173: Talk to Hirondelle - 1 Story Progress": MMZero3LocationData(region="Resistance Base 2", address=173),
    "Resistance Base 174: Talk to Doigt - 1 Story Progress": MMZero3LocationData(region="Resistance Base 2", address=174),
    "Resistance Base 175: Talk to Menart": MMZero3LocationData(region="Resistance Base 1", address=175),
    "Resistance Base 176: Near Pic": MMZero3LocationData(region="Resistance Base 1", address=176),

    "Derelict Spacecraft 133: 5th Grand Cannon Kill": MMZero3LocationData(region="Derelict Spacecraft", address=133),
    "Derelict Spacecraft 140: 3rd Shrimpolin Kill": MMZero3LocationData(region="Derelict Spacecraft", address=140),
    "Derelict Spacecraft 158: 4th Shotcounter Kill": MMZero3LocationData(region="Derelict Spacecraft", address=158),
    "Derelict Spacecraft 156: 4th Batring Kill": MMZero3LocationData(region="Derelict Spacecraft", address=156),
    "Derelict Spacecraft (1) 024: 1st Pit Secret Wall": MMZero3LocationData(region="Derelict Spacecraft", address=24),
    "Derelict Spacecraft (2) 037: Ledge Past Entrance": MMZero3LocationData(region="Derelict Spacecraft", address=37),
    "Derelict Spacecraft (3) 050: Ice Side Room": MMZero3LocationData(region="Derelict Spacecraft", address=50),
    "Derelict Spacecraft (4) 101: Ledge in Top Right": MMZero3LocationData(region="Derelict Spacecraft", address=101),
    "Derelict Spacecraft (5) 111: Final Ascent Bottom": MMZero3LocationData(region="Derelict Spacecraft", address=111),
    "Derelict Spacecraft (6) 007: Final Ascent Ledge": MMZero3LocationData(region="Derelict Spacecraft", address=7),
    
    "Aegis Volcano Base 141: 3rd Volcaire Kill": MMZero3LocationData(region="Aegis Volcano Base", address=141),
    "Aegis Volcano Base 146: 4th Lamplort Kill": MMZero3LocationData(region="Aegis Volcano Base", address=146),
    "Aegis Volcano Base (1) 047: Ledge Above Lava": MMZero3LocationData(region="Aegis Volcano Base", address=47),
    "Aegis Volcano Base (2) 102: 1st Box Inside": MMZero3LocationData(region="Aegis Volcano Base", address=102),
    "Aegis Volcano Base (3) 026: Platform Above First Room": MMZero3LocationData(region="Aegis Volcano Base", address=26),
    "Aegis Volcano Base (4) 114: Push 1st Container": MMZero3LocationData(region="Aegis Volcano Base", address=114),
    "Aegis Volcano Base (5) 073: Platform After Pushed Container": MMZero3LocationData(region="Aegis Volcano Base", address=73),
    "Aegis Volcano Base (6) 152: 10th Crossbyne Kill (Miniboss)": MMZero3LocationData(region="Aegis Volcano Base", address=152),
    "Aegis Volcano Base (7) 072: Lamplort Box": MMZero3LocationData(region="Aegis Volcano Base", address=72),
    "Aegis Volcano Base (8) 008: Top Gabyoall Box": MMZero3LocationData(region="Aegis Volcano Base", address=8),
    
    "Oceanic Highway Ruins 159: 4th Sharkseal X Kill": MMZero3LocationData(region="Oceanic Highway Ruins", address=159),
    "Oceanic Highway Ruins 161: 3rd Icebon Kill": MMZero3LocationData(region="Oceanic Highway Ruins", address=161),
    "Oceanic Highway Ruins 160: 4th Shelluno Kill": MMZero3LocationData(region="Oceanic Highway Ruins", address=160),
    "Oceanic Highway Ruins (1) 005: 1st Pit Breakable": MMZero3LocationData(region="Oceanic Highway Ruins", address=5),
    "Oceanic Highway Ruins (2) 075: 1st Underwater Pit": MMZero3LocationData(region="Oceanic Highway Ruins", address=75),
    "Oceanic Highway Ruins (3) 009: Above Cyber Door": MMZero3LocationData(region="Oceanic Highway Ruins", address=9),
    "Oceanic Highway Ruins (4) 059: Above 1st Spike Wall": MMZero3LocationData(region="Oceanic Highway Ruins", address=59),
    "Oceanic Highway Ruins (5) 079: Miniboss Kill": MMZero3LocationData(region="Oceanic Highway Ruins", address=79),
    "Oceanic Highway Ruins (6) 049: Spiked Platforms": MMZero3LocationData(region="Oceanic Highway Ruins", address=49),
    "Oceanic Highway Ruins (7) 113: Left of Final Button": MMZero3LocationData(region="Oceanic Highway Ruins", address=113),
    
    "Weapons Repair Factory 147: 5th Lemmingles Kill": MMZero3LocationData(region="Weapons Repair Factory", address=147),
    "Weapons Repair Factory 131: 5th Deathlock Kill": MMZero3LocationData(region="Weapons Repair Factory", address=131),
    "Weapons Repair Factory 052: 3rd Lemmingles Generator Kill": MMZero3LocationData(region="Weapons Repair Factory", address=52),
    "Weapons Repair Factory (1) 012: Below 3rd Hammer": MMZero3LocationData(region="Weapons Repair Factory", address=12),
    "Weapons Repair Factory (2) 115: Hit 3rd Hammer": MMZero3LocationData(region="Weapons Repair Factory", address=115),
    "Weapons Repair Factory (3) 104: Past 4th Hammer": MMZero3LocationData(region="Weapons Repair Factory", address=104),
    "Weapons Repair Factory (4) 093: Miniboss Kill": MMZero3LocationData(region="Weapons Repair Factory", address=93),
    "Weapons Repair Factory (5) 100: Behind Lemmingles Generator": MMZero3LocationData(region="Weapons Repair Factory", address=100),
    "Weapons Repair Factory (6) 084: Conveyor Descent Ledge": MMZero3LocationData(region="Weapons Repair Factory", address=84),
    "Weapons Repair Factory (7) 053: Ladder Into Junk": MMZero3LocationData(region="Weapons Repair Factory", address=53),
    
    "Old Residential 145: 5th Seimeran Kill": MMZero3LocationData(region="Old Residential", address=145),
    "Old Residential 135: 3rd Pillar Cannon Kill": MMZero3LocationData(region="Old Residential", address=135),
    "Old Residential (1) 039: 1st Door": MMZero3LocationData(region="Old Residential", address=39),
    "Old Residential (2) 001: Stump Door": MMZero3LocationData(region="Old Residential", address=1),
    "Old Residential (3) 112: Floor Breakables": MMZero3LocationData(region="Old Residential", address=112),
    "Old Residential (4) 074: Left Fork Door": MMZero3LocationData(region="Old Residential", address=74),
    "Old Residential (5) 067: Miniboss Kill": MMZero3LocationData(region="Old Residential", address=67),
    "Old Residential (6) 028: Box After Bombers": MMZero3LocationData(region="Old Residential", address=28),
    "Old Residential (7) 048: Top Right Secret Door": MMZero3LocationData(region="Old Residential", address=48),
    "Old Residential (8) 013: 2 Pits Left of Secret Door Exit": MMZero3LocationData(region="Old Residential", address=13),

    "Missile Factory 139: 4th Eye Cannon Kill": MMZero3LocationData(region="Missile Factory", address=139),
    "Missile Factory 127: 4th Pantheon Guardian Kill": MMZero3LocationData(region="Missile Factory", address=127),
    "Missile Factory 138: 4th Generator Cannon Kill": MMZero3LocationData(region="Missile Factory", address=138),
    "Missile Factory 098: 6th Generator Cannon Spawn Kill": MMZero3LocationData(region="Missile Factory", address=98),
    "Missile Factory (1) 057: Spiky Side Room": MMZero3LocationData(region="Missile Factory", address=57),
    "Missile Factory (2) 030: By Cyber Door": MMZero3LocationData(region="Missile Factory", address=30),
    "Missile Factory (3) 090: 2nd Conveyor Slopes Ledge": MMZero3LocationData(region="Missile Factory", address=90),
    "Missile Factory (4) 055: Left of 2nd Conveyor Slope": MMZero3LocationData(region="Missile Factory", address=55),
    "Missile Factory (5) 117: Above 2nd Conveyor Slope": MMZero3LocationData(region="Missile Factory", address=117),
    "Missile Factory (6) 021: Top Left Ledge": MMZero3LocationData(region="Missile Factory", address=21),
    
    "Twilight Desert 091: 5th Shrimpolin Kill": MMZero3LocationData(region="Twilight Desert", address=91),
    "Twilight Desert 153: 5th Flopper Kill": MMZero3LocationData(region="Twilight Desert", address=153),
    "Twilight Desert 154: 5th PurpleNerple Kill": MMZero3LocationData(region="Twilight Desert", address=154),
    "Twilight Desert (1) 085: After Long Quicksand": MMZero3LocationData(region="Twilight Desert", address=85),
    "Twilight Desert (2) 089: Miniboss Kill": MMZero3LocationData(region="Twilight Desert", address=89),
    "Twilight Desert (3) 031: Above 1st Pillar Cannon": MMZero3LocationData(region="Twilight Desert", address=31),
    "Twilight Desert (4) 022: Above 2nd Cyber Door": MMZero3LocationData(region="Twilight Desert", address=22),
    "Twilight Desert (5) 105: After 1st Helicopter": MMZero3LocationData(region="Twilight Desert", address=105),
    "Twilight Desert (6) 118: After 1st Helicopter": MMZero3LocationData(region="Twilight Desert", address=118),
    "Twilight Desert (7) 065: 2nd Helicopter Kill": MMZero3LocationData(region="Twilight Desert", address=65),
    
    "Forest of Anatre 157: 5th Mellnet Kill": MMZero3LocationData(region="Forest of Anatre", address=157),
    "Forest of Anatre 134: 7th Tile Cannon Kill": MMZero3LocationData(region="Forest of Anatre", address=134),
    "Forest of Anatre (1) 063: Treetops Above Start": MMZero3LocationData(region="Forest of Anatre", address=63),
    "Forest of Anatre (2) 002: Ledge Above 1st Door": MMZero3LocationData(region="Forest of Anatre", address=2),
    "Forest of Anatre (3) 071: 3rd Button Lower Path": MMZero3LocationData(region="Forest of Anatre", address=71),
    "Forest of Anatre (4) 014: Above 7th Button": MMZero3LocationData(region="Forest of Anatre", address=14),
    "Forest of Anatre (5) 119: 7th Button Lower Path": MMZero3LocationData(region="Forest of Anatre", address=119),
    "Forest of Anatre (6) 108: 8th Button Spike Pit": MMZero3LocationData(region="Forest of Anatre", address=108),
    "Forest of Anatre (7) 076: Above 9th Button": MMZero3LocationData(region="Forest of Anatre", address=76),
    "Forest of Anatre (8) 040: Breakables Below Boss Room": MMZero3LocationData(region="Forest of Anatre", address=40),
    
    "Frontline Ice Base 132: 3rd Gyro Cannon Kill": MMZero3LocationData(region="Frontline Ice Base", address=132),
    "Frontline Ice Base 128: 3rd Pantheon Aqua Kill": MMZero3LocationData(region="Frontline Ice Base", address=128),
    "Frontline Ice Base 136: 3rd Heavy Cannon Kill": MMZero3LocationData(region="Frontline Ice Base", address=136),
    "Frontline Ice Base (1) 066: Top Route Tower": MMZero3LocationData(region="Frontline Ice Base", address=66),
    "Frontline Ice Base (2) 109: Top Route Indoor Ledge": MMZero3LocationData(region="Frontline Ice Base", address=109),
    "Frontline Ice Base (3) 015: Top Route Pipe Passage": MMZero3LocationData(region="Frontline Ice Base", address=15),
    "Frontline Ice Base (4) 032: Ledge Before 2nd Door": MMZero3LocationData(region="Frontline Ice Base", address=32),
    "Frontline Ice Base (5) 035: Ledge After 2nd Door": MMZero3LocationData(region="Frontline Ice Base", address=35),
    "Frontline Ice Base (6) 120: Heavy Cannon Box": MMZero3LocationData(region="Frontline Ice Base", address=120),
    "Frontline Ice Base (7) 068: Final Ascent": MMZero3LocationData(region="Frontline Ice Base", address=68),
    
    "Area X-2 137: 4th Capsule Cannon Kill": MMZero3LocationData(region="Area X-2", address=137),
    "Area X-2 (1) 110: 1st Descent Ledge": MMZero3LocationData(region="Area X-2", address=110),
    "Area X-2 (2) 121: 1st Descent Bottom": MMZero3LocationData(region="Area X-2", address=121),
    "Area X-2 (3) 062: Ledge Above Platforms": MMZero3LocationData(region="Area X-2", address=62),
    "Area X-2 (4) 034: 1st Ascent Top": MMZero3LocationData(region="Area X-2", address=34),
    "Area X-2 (5) 042: Spiky Ascent Bottom": MMZero3LocationData(region="Area X-2", address=42),
    "Area X-2 (6) 070: Spiky Ascent Middle": MMZero3LocationData(region="Area X-2", address=70),
    "Area X-2 (7) 077: Spiky Ascent Top": MMZero3LocationData(region="Area X-2", address=77),
    "Area X-2 (8) 069: Platforms Side Room (Lower)": MMZero3LocationData(region="Area X-2", address=69),
    "Area X-2 (9) 061: Platforms Side Room (Upper)": MMZero3LocationData(region="Area X-2", address=61),
    
    "Energy Facility 155: 9th Mothjiro Kill": MMZero3LocationData(region="Energy Facility", address=155),
    "Energy Facility 150: 4th Snakecord Kill": MMZero3LocationData(region="Energy Facility", address=150),
    "Energy Facility (1) 056: Box Past 1st Cyber Door": MMZero3LocationData(region="Energy Facility", address=56),
    "Energy Facility (2) 124: 1st Ascent Right Path": MMZero3LocationData(region="Energy Facility", address=124),
    "Energy Facility (3) 082: Box After 1st Ascent": MMZero3LocationData(region="Energy Facility", address=82),
    "Energy Facility (4) 149: Miniboss Kill": MMZero3LocationData(region="Energy Facility", address=149),
    "Energy Facility (5) 064: Girder Ride Left": MMZero3LocationData(region="Energy Facility", address=64),
    "Energy Facility (6) 095: Girder Ride Right": MMZero3LocationData(region="Energy Facility", address=95),
    "Energy Facility (7) 078: Snakecord Guarded Secret Wall": MMZero3LocationData(region="Energy Facility", address=78),
    "Energy Facility (8) 004: Girder Maze Top Left": MMZero3LocationData(region="Energy Facility", address=4),
    
    "Snowy Plains 162: 4th Shellcrawler Kill": MMZero3LocationData(region="Snowy Plains", address=162),
    "Snowy Plains 130: 4th Pantheon Base Kill": MMZero3LocationData(region="Snowy Plains", address=130),
    "Snowy Plains (1) 003: 2nd Slope Secret Wall": MMZero3LocationData(region="Snowy Plains", address=3),
    "Snowy Plains (2) 029: 1st Rail Set Start": MMZero3LocationData(region="Snowy Plains", address=29),
    "Snowy Plains (3) 025: 1st Rail Set Middle": MMZero3LocationData(region="Snowy Plains", address=25),
    "Snowy Plains (4) 103: 1st Rail Set 2nd Pit Secret Wall": MMZero3LocationData(region="Snowy Plains", address=103),
    "Snowy Plains (5) 046: 5th Miniboss Snowball Kill": MMZero3LocationData(region="Snowy Plains", address=46),
    "Snowy Plains (6) 060: Miniboss Kill": MMZero3LocationData(region="Snowy Plains", address=60),
    "Snowy Plains (7) 123: 2nd Rail Set Start": MMZero3LocationData(region="Snowy Plains", address=123),
    "Snowy Plains (8) 086: 2nd Rail Set Middle": MMZero3LocationData(region="Snowy Plains", address=86),
    
    "Sunken Library (1) 125: Ledge Above First Pool": MMZero3LocationData(region="Sunken Library", address=125),
    "Sunken Library (2) 051: Under Second Pool": MMZero3LocationData(region="Sunken Library", address=51),
    "Sunken Library (3) 043: Last Exposed Wire": MMZero3LocationData(region="Sunken Library", address=43),
    "Sunken Library (4) 033: Past Exposed Wires": MMZero3LocationData(region="Sunken Library", address=33),
    "Sunken Library (5) 094: End of 1st Passage": MMZero3LocationData(region="Sunken Library", address=94),
    "Sunken Library (6) 096: Above 1st Door": MMZero3LocationData(region="Sunken Library", address=96),
    "Sunken Library 010: Dr. Weil Data": MMZero3LocationData(region="Sunken Library", address=10),
    "Sunken Library 017: Omega Data": MMZero3LocationData(region="Sunken Library", address=17),
    "Sunken Library 016: Dark Elf Data": MMZero3LocationData(region="Sunken Library", address=16),
    "Sunken Library 018: Elf Wars Data": MMZero3LocationData(region="Sunken Library", address=18),
    
    "Giant Elevator 148: 5th Cattatank Kill": MMZero3LocationData(region="Giant Elevator", address=148),
    "Giant Elevator 144: 6th Shotloid Kill": MMZero3LocationData(region="Giant Elevator", address=144),
    "Giant Elevator 129: 4th Pantheon Fist Kill": MMZero3LocationData(region="Giant Elevator", address=129),
    "Giant Elevator (1) 045: 1st Passage High Ledges": MMZero3LocationData(region="Giant Elevator", address=45),
    "Giant Elevator (2) 041: 1st Passage High Ledges": MMZero3LocationData(region="Giant Elevator", address=41),
    "Giant Elevator (3) 080: 1st Passage High Ledges": MMZero3LocationData(region="Giant Elevator", address=80),
    "Giant Elevator (4) 054: 1st Passage High Ledges": MMZero3LocationData(region="Giant Elevator", address=54),
    "Giant Elevator (5) 122: 1st Descent Ledge": MMZero3LocationData(region="Giant Elevator", address=122),
    "Giant Elevator (6) 027: 1st Descent Bottom Left Breakable": MMZero3LocationData(region="Giant Elevator", address=27),
    "Giant Elevator (7) 088: Miniboss Kill": MMZero3LocationData(region="Giant Elevator", address=88),
    
    "Sub Arcadia 163: 5th Cannonhopper Kill": MMZero3LocationData(region="Sub Arcadia", address=163),
    "Sub Arcadia 143: 3rd Petatria Kill": MMZero3LocationData(region="Sub Arcadia", address=143),
    "Sub Arcadia 142: 5th Claveker Kill": MMZero3LocationData(region="Sub Arcadia", address=142),
    "Sub Arcadia (1) 036: 1st Descent Ledge": MMZero3LocationData(region="Sub Arcadia", address=36),
    "Sub Arcadia (2) 081: Platforms Room Under Start": MMZero3LocationData(region="Sub Arcadia", address=81),
    "Sub Arcadia (3) 038: Platforms Room Top Left": MMZero3LocationData(region="Sub Arcadia", address=38),
    "Sub Arcadia (4) 006: Phantom Kill, Cyberspace Top Left": MMZero3LocationData(region="Sub Arcadia", address=6),
    "Sub Arcadia (5) 180: Platforms Room Bottom": MMZero3LocationData(region="Sub Arcadia", address=180),
    "Sub Arcadia (6) 087: Box Past 1st Door": MMZero3LocationData(region="Sub Arcadia", address=87),
    "Sub Arcadia (7) 083: Final Descent Left": MMZero3LocationData(region="Sub Arcadia", address=83),
    
    "Abandoned Research Laboratory 126: 5th Pantheon Hunter Kill": MMZero3LocationData(region="Abandoned Research Laboratory", address=126),
    "Abandoned Research Laboratory (1) 097: 1st Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=97),
    "Abandoned Research Laboratory (2) 177: Ledge Above Spike Zone": MMZero3LocationData(region="Abandoned Research Laboratory", address=177),
    "Abandoned Research Laboratory (3) 151: Ice Zone Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=151),
    "Abandoned Research Laboratory (4) 019: Ice Zone Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=19),
    "Abandoned Research Laboratory (5) 020: Ice Zone Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=20),
    "Abandoned Research Laboratory (6) 178: Ice Zone Alarm Ledge": MMZero3LocationData(region="Abandoned Research Laboratory", address=178),
    "Abandoned Research Laboratory (7) 164: Ice Zone Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=164),
    "Abandoned Research Laboratory (8) 179: Final Section Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=179),
    "Abandoned Research Laboratory (9) 011: Final Section Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=11),

    # Completion conditions. These ones aren't actually related to anything in game,
    # and are just included so that the amount of items and locations stay 1-1
    "Complete Derelict Spacecraft": MMZero3LocationData(region="Derelict Spacecraft", address=181),
    "Complete Aegis Volcano Base": MMZero3LocationData(region="Aegis Volcano Base", address=182),
    "Complete Oceanic Highway Ruins": MMZero3LocationData(region="Oceanic Highway Ruins", address=183),
    "Complete Weapons Repair Factory": MMZero3LocationData(region="Weapons Repair Factory", address=184),
    "Complete Old Residential": MMZero3LocationData(region="Old Residential", address=185),
    "Complete Missile Factory": MMZero3LocationData(region="Missile Factory", address=186),
    "Complete Twilight Desert": MMZero3LocationData(region="Twilight Desert", address=187),
    "Complete Forest of Anatre": MMZero3LocationData(region="Forest of Anatre", address=188),
    "Complete Frontline Ice Base": MMZero3LocationData(region="Frontline Ice Base", address=189),
    "Complete Area X-2": MMZero3LocationData(region="Area X-2", address=190),
    "Complete Energy Facility": MMZero3LocationData(region="Energy Facility", address=191),
    "Complete Snowy Plains": MMZero3LocationData(region="Snowy Plains", address=192),
    "Complete Sunken Library": MMZero3LocationData(region="Sunken Library", address=193),
    "Complete Giant Elevator": MMZero3LocationData(region="Giant Elevator", address=194),
    "Complete Sub Arcadia": MMZero3LocationData(region="Sub Arcadia", address=195),

    "Complete Abandoned Research Laboratory": MMZero3LocationData(
        region="Abandoned Research Laboratory",
        locked_item="Victory",
        address=196,
    ),

    # Chips
    "Collect Ice Body Chip": MMZero3LocationData(region="Oceanic Highway Ruins", address=197),
    "Collect Thunder Body Chip": MMZero3LocationData(region="Weapons Repair Factory", address=198),
    "Collect Flame Body Chip": MMZero3LocationData(region="Aegis Volcano Base", address=199),
    "Collect Light Body Chip": MMZero3LocationData(region="Old Residential", address=200),
    "Collect Absorber Body Chip": MMZero3LocationData(region="Giant Elevator", address=201),
    "Collect Spike Foot Chip": MMZero3LocationData(region="Snowy Plains", address=202),
    "Collect Quick Foot Chip": MMZero3LocationData(region="Area X-2", address=203),
    "Collect Double Jump Foot Chip": MMZero3LocationData(region="Energy Facility", address=204),
    "Collect Shadow Dash Foot Chip": MMZero3LocationData(region="Sunken Library", address=205),

    # EX Skills
    "A+ Rank Clear: Derelict Spacecraft": MMZero3LocationData(region="Derelict Spacecraft", address=206),
    "A+ Rank Clear: Aegis Volcano Base": MMZero3LocationData(region="Aegis Volcano Base", address=207),
    "A+ Rank Clear: Oceanic Highway Ruins": MMZero3LocationData(region="Oceanic Highway Ruins", address=208),
    "A+ Rank Clear: Weapons Repair Factory": MMZero3LocationData(region="Weapons Repair Factory", address=209),
    "A+ Rank Clear: Old Residential": MMZero3LocationData(region="Old Residential", address=210),
    "A+ Rank Clear: Missile Factory": MMZero3LocationData(region="Missile Factory", address=211),
    "A+ Rank Clear: Twilight Desert": MMZero3LocationData(region="Twilight Desert", address=212),
    "A+ Rank Clear: Forest of Anatre": MMZero3LocationData(region="Forest of Anatre", address=213),
    "A+ Rank Clear: Frontline Ice Base": MMZero3LocationData(region="Frontline Ice Base", address=214),
    "A+ Rank Clear: Area X-2": MMZero3LocationData(region="Area X-2", address=215),
    "A+ Rank Clear: Energy Facility": MMZero3LocationData(region="Energy Facility", address=216),
    "A+ Rank Clear: Snowy Plains": MMZero3LocationData(region="Snowy Plains", address=217),
    "A+ Rank Clear: Sunken Library": MMZero3LocationData(region="Sunken Library", address=218),
    "A+ Rank Clear: Giant Elevator": MMZero3LocationData(region="Giant Elevator", address=219),
    "A+ Rank Clear: Sub Arcadia": MMZero3LocationData(region="Sub Arcadia", address=220),

    # Sub Tanks
    "Old Residential Subtank: Top Left Past Bombers": MMZero3LocationData(region="Old Residential", address=221),
    "Forest of Anatre Subtank: Climb Extending Wall": MMZero3LocationData(region="Forest of Anatre", address=222),

    # Weapons
    "Collect Recoil Rod": MMZero3LocationData(region="Resistance Base 1", address=226),
    "Collect Shield Boomerang": MMZero3LocationData(region="Resistance Base 1", address=227),

    # Extra Lives
    "Oceanic Highway Ruins 1-UP: 1st Section Platforms": MMZero3LocationData(region="Oceanic Highway Ruins", address=231, can_create=extra_life_sanity_on),
    "Old Residential 1-UP (1): Right of Fork": MMZero3LocationData(region="Old Residential", address=232, can_create=extra_life_sanity_on),
    "Old Residential 1-UP (2): Left Fork Door": MMZero3LocationData(region="Old Residential", address=233, can_create=extra_life_sanity_on),
    "Missile Factory 1-UP: Towards End Of Missile": MMZero3LocationData(region="Missile Factory", address=234, can_create=extra_life_sanity_on),
    "Forest of Anatre 1-UP: In Tree Near Start": MMZero3LocationData(region="Forest of Anatre", address=235, can_create=extra_life_sanity_on),
    "Energy Facility 1-UP: Girder Maze Top Left": MMZero3LocationData(region="Energy Facility", address=236, can_create=extra_life_sanity_on),
    "Snowy Plains 1-UP: Pit Before 2nd Rail Set": MMZero3LocationData(region="Snowy Plains", address=237, can_create=extra_life_sanity_on), 
    "Giant Elevator 1-UP: 1st Passage High Ledges": MMZero3LocationData(region="Giant Elevator", address=238, can_create=extra_life_sanity_on),
    "Sub Arcadia 1-UP: Above Exit Door in Spike Room": MMZero3LocationData(region="Sub Arcadia", address=239, can_create=extra_life_sanity_on),
    "Resistance Base 1-UP: In Locked Room by Andrew": MMZero3LocationData(region="Resistance Base 1", address=240, can_create=extra_life_sanity_on),

    # Minibosses
    "Weapons Repair Factory Miniboss: Bee Server": MMZero3LocationData(region="Weapons Repair Factory", address=242),
    "Oceanic Highway Ruins Miniboss: Modified Pantheon Aqua": MMZero3LocationData(region="Oceanic Highway Ruins", address=243),
    "Old Residential Miniboss: Megamilpa": MMZero3LocationData(region="Old Residential", address=244),
    "Twilight Desert Miniboss: Or Wormer": MMZero3LocationData(region="Twilight Desert", address=245),
    "Snowy Plains Miniboss: Blanc Wormer": MMZero3LocationData(region="Snowy Plains", address=246),
    "Energy Facility Miniboss: Locomo-If": MMZero3LocationData(region="Energy Facility", address=247),
    "Energy Facility Port Room 1: Reactor Core": MMZero3LocationData(region="Energy Facility", address=248),
    "Energy Facility Port Room 2: Reactor Core": MMZero3LocationData(region="Energy Facility", address=249),
    "Giant Elevator Miniboss: Spearook": MMZero3LocationData(region="Giant Elevator", address=250),
    "Sub Arcadia Miniboss: Phantom": MMZero3LocationData(region="Sub Arcadia", address=251),
    "Aegis Volcano Base Miniboss: Crossbynes": MMZero3LocationData(region="Aegis Volcano Base", address=252),

    # Itemsanity:
    "Derelict Spacecraft E-Crystal: Ice Side Room": MMZero3LocationData(region="Derelict Spacecraft", address=301, can_create=itemsanity_on),
    "Derelict Spacecraft Energy: Ledge After Entrance": MMZero3LocationData(region="Derelict Spacecraft", address=302, can_create=itemsanity_on),

    "Aegis Volcano Base E-Crystal (1): Ledge Above Lava": MMZero3LocationData(region="Aegis Volcano Base", address=303, can_create=itemsanity_on),
    "Aegis Volcano Base Energy: Platform Above First Room": MMZero3LocationData(region="Aegis Volcano Base", address=304, can_create=itemsanity_on), #mobility
    "Aegis Volcano Base E-Crystal (2): Push 1st Container": MMZero3LocationData(region="Aegis Volcano Base", address=305, can_create=itemsanity_on), #recoil
    "Aegis Volcano Base E-Crystal (3): Push 1st Container": MMZero3LocationData(region="Aegis Volcano Base", address=306, can_create=itemsanity_on), #recoil
    "Aegis Volcano Base E-Crystal (4): After Mini Boss": MMZero3LocationData(region="Aegis Volcano Base", address=307, can_create=itemsanity_on),
    "Aegis Volcano Base E-Crystal (5): Ascent After Mini Boss": MMZero3LocationData(region="Aegis Volcano Base", address=308, can_create=itemsanity_on),
    "Aegis Volcano Base E-Crystal (6): After Second Lava Blocks": MMZero3LocationData(region="Aegis Volcano Base", address=309, can_create=itemsanity_on),

    "Oceanic Highway Ruins E-Crystal (1): 1st Pit Breakable": MMZero3LocationData(region="Oceanic Highway Ruins", address=310, can_create=itemsanity_on), #recoil
    "Oceanic Highway Ruins E-Crystal (2): 1st Pit Breakable": MMZero3LocationData(region="Oceanic Highway Ruins", address=311, can_create=itemsanity_on), #recoil
    "Oceanic Highway Ruins E-Crystal (3): 1st Underwater Pit": MMZero3LocationData(region="Oceanic Highway Ruins", address=312, can_create=itemsanity_on),
    "Oceanic Highway Ruins E-Crystal (4): 1st Underwater Pit": MMZero3LocationData(region="Oceanic Highway Ruins", address=313, can_create=itemsanity_on),
    "Oceanic Highway Ruins E-Crystal (5): Above Cyber Door": MMZero3LocationData(region="Oceanic Highway Ruins", address=314, can_create=itemsanity_on),
    "Oceanic Highway Ruins E-Crystal (6): Above Cyber Door": MMZero3LocationData(region="Oceanic Highway Ruins", address=315, can_create=itemsanity_on),
    "Oceanic Highway Ruins Energy (1): 1st Section Platforms": MMZero3LocationData(region="Oceanic Highway Ruins", address=316, can_create=itemsanity_on),
    "Oceanic Highway Ruins Energy (2): Destroy Box Using Boss": MMZero3LocationData(region="Oceanic Highway Ruins", address=317, can_create=itemsanity_on),
    "Oceanic Highway Ruins Energy (3): Platform after 2nd Pressure Pad": MMZero3LocationData(region="Oceanic Highway Ruins", address=318, can_create=itemsanity_on),
    "Oceanic Highway Ruins E-Crystal (7): Spiked Platforms": MMZero3LocationData(region="Oceanic Highway Ruins", address=319, can_create=itemsanity_on),

    "Weapons Repair Factory Energy (1): Before 1st Junk Pit": MMZero3LocationData(region="Weapons Repair Factory", address=320, can_create=itemsanity_on),
    "Weapons Repair Factory E-Crystal (1): Hit 3rd Hammer": MMZero3LocationData(region="Weapons Repair Factory", address=321, can_create=itemsanity_on), #recoil
    "Weapons Repair Factory E-Crystal (2): Hit 3rd Hammer": MMZero3LocationData(region="Weapons Repair Factory", address=322, can_create=itemsanity_on), #recoil
    "Weapons Repair Factory Energy (2): In Junk Pit": MMZero3LocationData(region="Weapons Repair Factory", address=323, can_create=itemsanity_on),
    "Weapons Repair Factory E-Crystal (3): Before Mini Boss Door": MMZero3LocationData(region="Weapons Repair Factory", address=324, can_create=itemsanity_on),
    "Weapons Repair Factory E-Crystal (4): Before Mini Boss Door": MMZero3LocationData(region="Weapons Repair Factory", address=325, can_create=itemsanity_on),
    "Weapons Repair Factory Energy (3): After Mini Boss": MMZero3LocationData(region="Weapons Repair Factory", address=326, can_create=itemsanity_on),
    "Weapons Repair Factory E-Crystal (5): Before Conveyor Descent": MMZero3LocationData(region="Weapons Repair Factory", address=327, can_create=itemsanity_on),
    "Weapons Repair Factory E-Crystal (6): Before Conveyor Descent": MMZero3LocationData(region="Weapons Repair Factory", address=328, can_create=itemsanity_on),
    "Weapons Repair Factory E-Crystal (7): Ladder Into Junk": MMZero3LocationData(region="Weapons Repair Factory", address=329, can_create=itemsanity_on),

    "Old Residential E-Crystal (1): Stump Door": MMZero3LocationData(region="Old Residential", address=330, can_create=itemsanity_on), #fire
    "Old Residential Energy (1): Stump Door": MMZero3LocationData(region="Old Residential", address=331, can_create=itemsanity_on), #fire
    "Old Residential E-Crystal (2): Above 1st Door": MMZero3LocationData(region="Old Residential", address=332, can_create=itemsanity_on),
    "Old Residential E-Crystal (3): Above 1st Door": MMZero3LocationData(region="Old Residential", address=333, can_create=itemsanity_on),
    "Old Residential E-Crystal (4): Door after Cutscene": MMZero3LocationData(region="Old Residential", address=334, can_create=itemsanity_on), #fire
    "Old Residential E-Crystal (5): Door after Cutscene": MMZero3LocationData(region="Old Residential", address=335, can_create=itemsanity_on), #fire
    "Old Residential E-Crystal (6): Door after Cutscene": MMZero3LocationData(region="Old Residential", address=336, can_create=itemsanity_on), #fire
    "Old Residential Energy (2): Top Right Secret Door": MMZero3LocationData(region="Old Residential", address=337, can_create=itemsanity_on),
    "Old Residential E-Crystal (7): Top Right Secret Door": MMZero3LocationData(region="Old Residential", address=338, can_create=itemsanity_on),
    "Old Residential E-Crystal (8): Top Right Secret Door": MMZero3LocationData(region="Old Residential", address=339, can_create=itemsanity_on),
    "Old Residential Energy (3): Falling Platforms": MMZero3LocationData(region="Old Residential", address=340, can_create=itemsanity_on),
    "Old Residential E-Crystal (9): Falling Platforms": MMZero3LocationData(region="Old Residential", address=341, can_create=itemsanity_on),
    "Old Residential E-Crystal (10): Falling Platforms": MMZero3LocationData(region="Old Residential", address=342, can_create=itemsanity_on),
    "Old Residential E-Crystal (11): Falling Platforms": MMZero3LocationData(region="Old Residential", address=343, can_create=itemsanity_on),
    "Old Residential E-Crystal (12): Falling Platforms": MMZero3LocationData(region="Old Residential", address=344, can_create=itemsanity_on),
    "Old Residential E-Crystal (13): Top Left Past Bombers": MMZero3LocationData(region="Old Residential", address=345, can_create=itemsanity_on), #mobility
    "Old Residential Energy (4): Climb after Miniboss": MMZero3LocationData(region="Old Residential", address=346, can_create=itemsanity_on),
    "Old Residential Energy (5): Before Top Right Secret Door": MMZero3LocationData(region="Old Residential", address=347, can_create=itemsanity_on),
    "Old Residential Energy (6): Breakable Blocks by Bombers": MMZero3LocationData(region="Old Residential", address=348, can_create=itemsanity_on), # rod

    "Missile Factory E-Crystal (1): Pit Under Ladder": MMZero3LocationData(region="Missile Factory", address=349, can_create=itemsanity_on),
    "Missile Factory E-Crystal (2): Pit Under Ladder": MMZero3LocationData(region="Missile Factory", address=350, can_create=itemsanity_on),
    "Missile Factory E-Crystal (3): Missile Top Path": MMZero3LocationData(region="Missile Factory", address=351, can_create=itemsanity_on),
    "Missile Factory Energy (1): Missile Bottom Path": MMZero3LocationData(region="Missile Factory", address=352, can_create=itemsanity_on),
    "Missile Factory Energy (2): Missile Top Right": MMZero3LocationData(region="Missile Factory", address=353, can_create=itemsanity_on), #Technically nothing, but double jump anyway

    "Twilight Desert Energy: Above 2nd Pillar Cannon": MMZero3LocationData(region="Twilight Desert", address=354, can_create=itemsanity_on),

    "Forest of Anatre Energy (1): Treetops Above Generator Cannon": MMZero3LocationData(region="Forest of Anatre", address=355, can_create=itemsanity_on), # fire
    "Forest of Anatre Energy (2): 7th Button Upper Path": MMZero3LocationData(region="Forest of Anatre", address=356, can_create=itemsanity_on),
    "Forest of Anatre Energy (3): Breakables Below Boss Room": MMZero3LocationData(region="Forest of Anatre", address=357, can_create=itemsanity_on), # recoil

    "Frontline Ice Base Energy: Top Route Tower": MMZero3LocationData(region="Frontline Ice Base", address=358, can_create=itemsanity_on), # splash
    "Frontline Ice Base E-Crystal (1): Bottom Route Cave": MMZero3LocationData(region="Frontline Ice Base", address=359, can_create=itemsanity_on),
    "Frontline Ice Base E-Crystal (2): Bottom Route Cave": MMZero3LocationData(region="Frontline Ice Base", address=360, can_create=itemsanity_on),
    "Frontline Ice Base E-Crystal (3): Ledge After 2nd Door": MMZero3LocationData(region="Frontline Ice Base", address=361, can_create=itemsanity_on),

    "Area X-2 Energy (1): 1st Descent Ledge": MMZero3LocationData(region="Area X-2", address=362, can_create=itemsanity_on),
    "Area X-2 Energy (2): 1st Ascent Left": MMZero3LocationData(region="Area X-2", address=363, can_create=itemsanity_on),
    "Area X-2 Energy (3): Spiky Ascent Middle": MMZero3LocationData(region="Area X-2", address=364, can_create=itemsanity_on),
    "Area X-2 Energy (4): Spiky Ascent Top": MMZero3LocationData(region="Area X-2", address=365, can_create=itemsanity_on),

    "Energy Facility Energy (1): 1st Ascent Right Path": MMZero3LocationData(region="Energy Facility", address=366, can_create=itemsanity_on),
    "Energy Facility Energy (2): Ladder Descent": MMZero3LocationData(region="Energy Facility", address=367, can_create=itemsanity_on),
    "Energy Facility Energy (3): Ascent After 1st Reactor": MMZero3LocationData(region="Energy Facility", address=368, can_create=itemsanity_on),
    "Energy Facility E-Crystal (1): Ascent After 1st Reactor": MMZero3LocationData(region="Energy Facility", address=369, can_create=itemsanity_on),
    "Energy Facility E-Crystal (2): Ascent After 1st Reactor": MMZero3LocationData(region="Energy Facility", address=370, can_create=itemsanity_on),
    "Energy Facility Energy (4): Before Second Reactor": MMZero3LocationData(region="Energy Facility", address=371, can_create=itemsanity_on),

    "Sunken Library Energy (1): Ledge Above First Pool": MMZero3LocationData(region="Sunken Library", address=372, can_create=itemsanity_on),
    "Sunken Library Energy (2): Incorrect Room": MMZero3LocationData(region="Sunken Library", address=373, can_create=itemsanity_on),
    "Sunken Library E-Crystal (1): Incorrect Room": MMZero3LocationData(region="Sunken Library", address=374, can_create=itemsanity_on),
    "Sunken Library Energy (3): Incorrect Room": MMZero3LocationData(region="Sunken Library", address=375, can_create=itemsanity_on),
    "Sunken Library E-Crystal (2): Incorrect Room": MMZero3LocationData(region="Sunken Library", address=376, can_create=itemsanity_on),
    "Sunken Library E-Crystal (3): Incorrect Room": MMZero3LocationData(region="Sunken Library", address=377, can_create=itemsanity_on),

    "Giant Elevator E-Crystal (1): 1st Passage High Ledges": MMZero3LocationData(region="Giant Elevator", address=378, can_create=itemsanity_on),
    "Giant Elevator E-Crystal (2): 1st Descent Ledge": MMZero3LocationData(region="Giant Elevator", address=379, can_create=itemsanity_on),
    "Giant Elevator Energy: Final Descent Ledge": MMZero3LocationData(region="Giant Elevator", address=380, can_create=itemsanity_on),

    "Sub Arcadia E-Crystal: Pit Near Start": MMZero3LocationData(region="Sub Arcadia", address=381, can_create=itemsanity_on),
    "Sub Arcadia Energy: Final Descent Near Top": MMZero3LocationData(region="Sub Arcadia", address=382, can_create=itemsanity_on),
}

# Cerveau's shop
# Max 48 Slots: locations 253–300
def shop_slot_is_stocked(slot: int) -> Callable[["MMZero3World"], bool]:
    """can_create for one shop slot: the seed stocks the first shop_slots of them."""
    def can_create(world: "MMZero3World") -> bool:
        return slot < world.options.shop_slots.value

    return can_create

shop_location_names: List[str] = []
for slot_number in range(Data.AP_SHOP_SLOTS_MAX):
    shop_name = f"Cerveau's Shop Slot {slot_number + 1}"
    shop_location_names.append(shop_name)
    location_data_table[shop_name] = MMZero3LocationData(
        region="Resistance Base 1",
        address=Data.AP_SHOP_LOCATION_FIRST + slot_number,
        can_create=shop_slot_is_stocked(slot_number),
    )

# Location groups for `!hint` and tracker filtering.
location_categories: Dict[str, range] = {
    "Secret Disks": range(1, 181),
    "Stage Clears": range(181, 197),
    "Chips": range(197, 206),
    "A+ Rank Clears": range(206, 221),
    "Subtanks": range(221, 223),
    "Weapons": range(226, 228),
    "1-UPs": range(Data.AP_LOC_EXLIFE_FIRST, Data.AP_LOC_EXLIFE_FIRST + Data.AP_EXLIFE_COUNT),
    "Minibosses": range(242, 253),
    "Itemsanity": range(Data.AP_LOC_ITEMSANITY_FIRST,
                                          Data.AP_LOC_ITEMSANITY_FIRST
                                          + Data.AP_ITEMSANITY_COUNT),
    "Shop": range(Data.AP_SHOP_LOCATION_FIRST,
                  Data.AP_SHOP_LOCATION_FIRST + Data.AP_SHOP_SLOTS_MAX),
}


def build_location_name_groups() -> Dict[str, Set[str]]:
    """Item Groups. One per stage and one per kind of check."""
    groups: Dict[str, Set[str]] = {}

    for name, data in location_data_table.items():
        # The base is three regions since its checks are gated on Story Progress,
        # but I still feel like a player asking resistance base is asking for all 3 together.
        stage = "Resistance Base" if data.region.startswith("Resistance Base") else data.region
        groups.setdefault(stage, set()).add(name)

        if data.address is None:
            continue
        for group, ids in location_categories.items():
            if data.address in ids:
                groups.setdefault(group, set()).add(name)

    return groups


location_name_groups = build_location_name_groups()

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
