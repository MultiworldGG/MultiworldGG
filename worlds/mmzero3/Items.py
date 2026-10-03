from typing import Callable, Dict, List, NamedTuple, Optional, Set, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import MMZero3World

class MMZero3Item(Item):
    game: str = "Mega Man Zero 3"

class MMZero3ItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[["MMZero3World"], bool] = lambda world: True
    # How many copies of the item go in the pool. For progressive items.
    count: Callable[["MMZero3World"], int] = lambda world: 1


# Stage names as they appear in game order. Final level not included here.
stage_names = [
    "Derelict Spacecraft", "Aegis Volcano Base", "Oceanic Highway Ruins",
    "Weapons Repair Factory", "Old Residential", "Missile Factory",
    "Twilight Desert", "Forest of Anatre", "Frontline Ice Base",
    "Area X-2", "Energy Facility", "Snowy Plains",
    "Sunken Library", "Giant Elevator", "Sub Arcadia"
]

# Weapon as they appear in game order.
weapon_names = ["Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"]

# Progressive upgrades.
weapon_chains: Dict[str, List[str]] = {
    "Buster": ["Owns", "Semi Charge", "Full Charge", "Attack +1", "Attack +2", "Attack +3"],
    "Z-Saber": ["Owns", "2nd Slash", "3rd Slash", "Charged Slash", "Attack +1", "Attack +2", "Attack +3"],
    "Recoil Rod": ["Owns", "Charged Rod", "Attack +1", "Attack +2", "Attack +3"],
    "Shield Boomerang": ["Owns", "Charged Throw", "Attack +1", "Attack +2", "Attack +3"],
}
def weapon_ability_level(weapon: str, ability: str) -> int:
    return weapon_chains[weapon].index(ability) + 1


item_data_table: Dict[str, MMZero3ItemData] = {
    "Disk 001: Auto-Charge Head Chip": MMZero3ItemData(code=1, type=ItemClassification.useful),
    "Disk 002: Auto-Recover Head Chip": MMZero3ItemData(code=2, type=ItemClassification.useful),
    "Disk 003: Quick-Charge Head Chip": MMZero3ItemData(code=3, type=ItemClassification.useful),
    "Disk 004: Frog Foot Chip": MMZero3ItemData(code=4, type=ItemClassification.useful),
    "Disk 005: Splash Jump Foot Chip": MMZero3ItemData(code=5, type=ItemClassification.progression),
    "Disk 006: Ultima Foot Chip": MMZero3ItemData(code=6, type=ItemClassification.progression),
    "Disk 007: File A": MMZero3ItemData(code=7, type=ItemClassification.filler),
    "Disk 008: File B": MMZero3ItemData(code=8, type=ItemClassification.filler),
    "Disk 009: File C": MMZero3ItemData(code=9, type=ItemClassification.filler),
    "Disk 010: File D": MMZero3ItemData(code=10, type=ItemClassification.filler),
    "Disk 011: File E": MMZero3ItemData(code=11, type=ItemClassification.filler),
    "Disk 012: File F": MMZero3ItemData(code=12, type=ItemClassification.filler),
    "Disk 013: File G": MMZero3ItemData(code=13, type=ItemClassification.filler),
    "Disk 014: File H": MMZero3ItemData(code=14, type=ItemClassification.filler),
    "Disk 015: File I": MMZero3ItemData(code=15, type=ItemClassification.filler),
    "Disk 016: File J": MMZero3ItemData(code=16, type=ItemClassification.filler),
    "Disk 017: File K": MMZero3ItemData(code=17, type=ItemClassification.filler),
    "Disk 018: File L": MMZero3ItemData(code=18, type=ItemClassification.filler),
    "Disk 019: File M": MMZero3ItemData(code=19, type=ItemClassification.filler),
    "Disk 020: File N": MMZero3ItemData(code=20, type=ItemClassification.filler),
    "Disk 021: Martina (Double Health)": MMZero3ItemData(code=21, type=ItemClassification.useful),
    "Disk 022: Milvy (+4 Max Health)": MMZero3ItemData(code=22, type=ItemClassification.useful),
    "Disk 023: Elphy (+4 Max Health)": MMZero3ItemData(code=23, type=ItemClassification.useful),
    "Disk 024: Sylphy (+4 Max Health)": MMZero3ItemData(code=24, type=ItemClassification.useful),
    "Disk 025: Rilphy (+4 Max Health)": MMZero3ItemData(code=25, type=ItemClassification.useful),
    "Disk 026: Artan (Sub Tank)": MMZero3ItemData(code=26, type=ItemClassification.useful),
    "Disk 027: Zictan (Sub Tank)": MMZero3ItemData(code=27, type=ItemClassification.useful),
    "Disk 028: Mott (Extra Lives)": MMZero3ItemData(code=28, type=ItemClassification.filler),
    "Disk 029: Dott (Extra Lives)": MMZero3ItemData(code=29, type=ItemClassification.filler),
    "Disk 030: Curiph (Small Heal)": MMZero3ItemData(code=30, type=ItemClassification.filler),
    "Disk 031: Luriph (Small Heal)": MMZero3ItemData(code=31, type=ItemClassification.filler),
    "Disk 032: Suriph (Small Heal)": MMZero3ItemData(code=32, type=ItemClassification.filler),
    "Disk 033: Tiriph (Small Heal)": MMZero3ItemData(code=33, type=ItemClassification.filler),
    "Disk 034: Yuriph (Small Heal)": MMZero3ItemData(code=34, type=ItemClassification.filler),
    "Disk 035: Beriph (Small Heal)": MMZero3ItemData(code=35, type=ItemClassification.filler),
    "Disk 036: Wiliph (Small Heal)": MMZero3ItemData(code=36, type=ItemClassification.filler),
    "Disk 037: Cyliph (Small Heal)": MMZero3ItemData(code=37, type=ItemClassification.filler),
    "Disk 038: Snoq (Large Heal)": MMZero3ItemData(code=38, type=ItemClassification.filler),
    "Disk 039: Mathiq (Large Heal)": MMZero3ItemData(code=39, type=ItemClassification.filler),
    "Disk 040: Mylaq (Large Heal)": MMZero3ItemData(code=40, type=ItemClassification.filler),
    "Disk 041: Ajiq (Large Heal)": MMZero3ItemData(code=41, type=ItemClassification.filler),
    "Disk 042: Dobuq (Large Heal)": MMZero3ItemData(code=42, type=ItemClassification.filler),
    "Disk 043: Mulaq (Large Heal)": MMZero3ItemData(code=43, type=ItemClassification.filler),
    "Disk 044: Mailla (Bullets to Health)": MMZero3ItemData(code=44, type=ItemClassification.useful),
    "Disk 045: Miulla (Bullets to Health)": MMZero3ItemData(code=45, type=ItemClassification.useful),
    "Disk 046: Cloppe (Drops Health)": MMZero3ItemData(code=46, type=ItemClassification.useful),
    "Disk 047: Sloppe (Drops Health)": MMZero3ItemData(code=47, type=ItemClassification.useful),
    "Disk 048: Putite (Non-Lethal Spikes)": MMZero3ItemData(code=48, type=ItemClassification.useful),
    "Disk 049: Balette (Run Faster)": MMZero3ItemData(code=49, type=ItemClassification.useful),
    "Disk 050: Maya (Faster Ladders)": MMZero3ItemData(code=50, type=ItemClassification.useful),
    "Disk 051: Kwappa (Slower Sliding)": MMZero3ItemData(code=51, type=ItemClassification.useful),
    "Disk 052: Gambul (No Recoil)": MMZero3ItemData(code=52, type=ItemClassification.useful),
    "Disk 053: Biraid (Pit Recovery)": MMZero3ItemData(code=53, type=ItemClassification.useful),
    "Disk 054: Birleaf (Pit Recovery)": MMZero3ItemData(code=54, type=ItemClassification.useful),
    "Disk 055: Pitaph (Slows Enemies)": MMZero3ItemData(code=55, type=ItemClassification.useful),
    "Disk 056: Pitapuh (Slows Enemies)": MMZero3ItemData(code=56, type=ItemClassification.useful),
    "Disk 057: Beetack (Direct Bullets)": MMZero3ItemData(code=57, type=ItemClassification.useful),
    "Disk 058: Beenipe (Direct Bullets)": MMZero3ItemData(code=58, type=ItemClassification.useful),
    "Disk 059: Archim (Arcing Bullets)": MMZero3ItemData(code=59, type=ItemClassification.useful),
    "Disk 060: Archil (Arcing Bullets)": MMZero3ItemData(code=60, type=ItemClassification.useful),
    "Disk 061: Byse (Double Drop Value)": MMZero3ItemData(code=61, type=ItemClassification.useful),
    "Disk 062: Dylphina (Drop Rate Up)": MMZero3ItemData(code=62, type=ItemClassification.useful),
    "Disk 063: Lizetus (Up Saber Combo)": MMZero3ItemData(code=63, type=ItemClassification.useful),
    "Disk 064: Cottus (Down Saber Combo)": MMZero3ItemData(code=64, type=ItemClassification.useful),
    "Disk 065: Shuthas (4 Buster Shots)": MMZero3ItemData(code=65, type=ItemClassification.useful),
    "Disk 066: Malthas (Saber Spin)": MMZero3ItemData(code=66, type=ItemClassification.useful),
    "Disk 067: Ilethas (Slash Bullets)": MMZero3ItemData(code=67, type=ItemClassification.useful),
    "Disk 068: Enethas (EC from Block)": MMZero3ItemData(code=68, type=ItemClassification.useful),
    "Disk 069: Busras (Buster +1)": MMZero3ItemData(code=69, type=ItemClassification.useful),
    "Disk 070: Sabras (Saber +1)": MMZero3ItemData(code=70, type=ItemClassification.useful),
    "Disk 071: Roderas (Recoil Rod +1)": MMZero3ItemData(code=71, type=ItemClassification.useful),
    "Disk 072: Boomeras (Shield +1)": MMZero3ItemData(code=72, type=ItemClassification.useful),
    "Disk 073: Clokkle (Faster Charge)": MMZero3ItemData(code=73, type=ItemClassification.useful),
    "Disk 074: Metoras (Enemies to Mets)": MMZero3ItemData(code=74, type=ItemClassification.filler),
    "Disk 075: Metorika (Enemies to Mets)": MMZero3ItemData(code=75, type=ItemClassification.filler),
    "Disk 076: Metorph (Enemies to Mets)": MMZero3ItemData(code=76, type=ItemClassification.filler),
    "Disk 077: Metella (Enemies to Mets)": MMZero3ItemData(code=77, type=ItemClassification.filler),
    "Disk 078: Meterom (Enemies to Mets)": MMZero3ItemData(code=78, type=ItemClassification.filler),
    "Disk 079: Kynite (Kill All Enemies)": MMZero3ItemData(code=79, type=ItemClassification.filler),
    "Disk 080: Surnite (Kill All Enemies)": MMZero3ItemData(code=80, type=ItemClassification.filler),
    "Disk 081: Tenite (Kill All Enemies)": MMZero3ItemData(code=81, type=ItemClassification.filler),
    "Disk 082: Stopalla (Stun Enemies)": MMZero3ItemData(code=82, type=ItemClassification.filler),
    "Disk 083: Stopina (Stun Enemies)": MMZero3ItemData(code=83, type=ItemClassification.filler),
    "Disk 084: Stopule (Stun Enemies)": MMZero3ItemData(code=84, type=ItemClassification.filler),
    "Disk 085: Stopeta (Stun Enemies)": MMZero3ItemData(code=85, type=ItemClassification.filler),
    "Disk 086: Stoposa (Stun Enemies)": MMZero3ItemData(code=86, type=ItemClassification.filler),
    "Disk 087: Hanmarga (Half Boss HP)": MMZero3ItemData(code=87, type=ItemClassification.useful),
    "Disk 088: Hanmarji (Half Boss HP)": MMZero3ItemData(code=88, type=ItemClassification.useful),
    "Disk 089: Hanmarbo (Half Boss HP)": MMZero3ItemData(code=89, type=ItemClassification.useful),
    "Disk 090: Aina (Sets Rank to A)": MMZero3ItemData(code=90, type=ItemClassification.useful),
    "Disk 091: Acooi (Sets Rank to A)": MMZero3ItemData(code=91, type=ItemClassification.useful),
    "Disk 092: Achoon (Sets Rank to A)": MMZero3ItemData(code=92, type=ItemClassification.useful),
    "Disk 093: Anater (Sets Rank to A)": MMZero3ItemData(code=93, type=ItemClassification.useful),
    "Disk 094: Awarne (Sets Rank to A)": MMZero3ItemData(code=94, type=ItemClassification.useful),
    "Disk 095: 80 E-Crystals": MMZero3ItemData(code=95, type=ItemClassification.filler),
    "Disk 096: 100 E-Crystals": MMZero3ItemData(code=96, type=ItemClassification.filler),
    "Disk 097: 200 E-Crystals": MMZero3ItemData(code=97, type=ItemClassification.filler),
    "Disk 098: 150 E-Crystals": MMZero3ItemData(code=98, type=ItemClassification.filler),
    "Disk 099: 40 E-Crystals": MMZero3ItemData(code=99, type=ItemClassification.filler),
    "Disk 100: 100 E-Crystals": MMZero3ItemData(code=100, type=ItemClassification.filler),
    "Disk 101: 100 E-Crystals": MMZero3ItemData(code=101, type=ItemClassification.filler),
    "Disk 102: 50 E-Crystals": MMZero3ItemData(code=102, type=ItemClassification.filler),
    "Disk 103: 80 E-Crystals": MMZero3ItemData(code=103, type=ItemClassification.filler),
    "Disk 104: 100 E-Crystals": MMZero3ItemData(code=104, type=ItemClassification.filler),
    "Disk 105: 100 E-Crystals": MMZero3ItemData(code=105, type=ItemClassification.filler),
    "Disk 106: 40 E-Crystals": MMZero3ItemData(code=106, type=ItemClassification.filler),
    "Disk 107: 500 E-Crystals": MMZero3ItemData(code=107, type=ItemClassification.filler),
    "Disk 108: 100 E-Crystals": MMZero3ItemData(code=108, type=ItemClassification.filler),
    "Disk 109: 100 E-Crystals": MMZero3ItemData(code=109, type=ItemClassification.filler),
    "Disk 110: 100 E-Crystals": MMZero3ItemData(code=110, type=ItemClassification.filler),
    # bitflags
    "Disk 111: Potted Plants to Base": MMZero3ItemData(code=111, type=ItemClassification.filler),
    "Disk 112: New Nurse Elf Design": MMZero3ItemData(code=112, type=ItemClassification.filler),
    "Disk 113: Reploid to Base Hall": MMZero3ItemData(code=113, type=ItemClassification.filler),
    "Disk 114: Alouette Dress Design": MMZero3ItemData(code=114, type=ItemClassification.filler),

    "Disk 115: Reploid to Room 02A": MMZero3ItemData(code=115, type=ItemClassification.filler),
    "Disk 116: Crea (Lore File)": MMZero3ItemData(code=116, type=ItemClassification.filler),
    "Disk 117: Orange Cats to Base": MMZero3ItemData(code=117, type=ItemClassification.filler),
    "Disk 118: Phantom Cyber Elf to Base Roof": MMZero3ItemData(code=118, type=ItemClassification.filler),
    "Disk 119: Posters to Base": MMZero3ItemData(code=119, type=ItemClassification.filler),
    # The Room spawns 1-up which is a check
    "Disk 120: New Room Near Andrew": MMZero3ItemData(code=120, type=ItemClassification.progression), 
    "Disk 121: Reploid to Room 1F-A": MMZero3ItemData(code=121, type=ItemClassification.filler),
    
    "Disk 122: Flowers to Base Roof": MMZero3ItemData(code=122, type=ItemClassification.filler),
    "Disk 123: New Animal Elf Design": MMZero3ItemData(code=123, type=ItemClassification.filler),
    "Disk 124: Young Andrew": MMZero3ItemData(code=124, type=ItemClassification.filler),
    "Disk 125: Seagulls to Base": MMZero3ItemData(code=125, type=ItemClassification.filler),
    "Disk 126: Tabby Cats to Base": MMZero3ItemData(code=126, type=ItemClassification.filler),
    "Disk 127: Grafitti to Base": MMZero3ItemData(code=127, type=ItemClassification.filler),
    "Disk 128: Reploid to Room 02D": MMZero3ItemData(code=128, type=ItemClassification.filler),
    
    "Disk 129: Right Tower Reploid Dialogue": MMZero3ItemData(code=129, type=ItemClassification.filler),
    "Disk 130: Reploid to Room 02B": MMZero3ItemData(code=130, type=ItemClassification.filler),
    "Disk 131: Reploid to Room 02C": MMZero3ItemData(code=131, type=ItemClassification.filler),
    "Disk 132: Reploid to Floor 2": MMZero3ItemData(code=132, type=ItemClassification.filler),
    "Disk 133: Elpizo Cyber Elf by Command Room": MMZero3ItemData(code=133, type=ItemClassification.filler),
    "Disk 134: Left Tower Reploid Dialogue": MMZero3ItemData(code=134, type=ItemClassification.filler),
    
    "Disk 135: New Hacker Elf Design": MMZero3ItemData(code=135, type=ItemClassification.filler),
    "Disk 136: Lilies to Base": MMZero3ItemData(code=136, type=ItemClassification.filler),
    "Disk 137: Flying Fish to the Base Dock": MMZero3ItemData(code=137, type=ItemClassification.filler),
    "Disk 138: Reploid to Room 03C": MMZero3ItemData(code=138, type=ItemClassification.filler),
    "Disk 139: Reploid to Floor 3": MMZero3ItemData(code=139, type=ItemClassification.filler),
    "Disk 140: Reploid to Room 03D": MMZero3ItemData(code=140, type=ItemClassification.filler),
    # non-bitflags
    "Disk 141: Dialogue Box: Silver": MMZero3ItemData(code=141, type=ItemClassification.filler),
    "Disk 142: Dialogue Box: Blue": MMZero3ItemData(code=142, type=ItemClassification.filler),
    "Disk 143: Dialogue Box: Action": MMZero3ItemData(code=143, type=ItemClassification.filler),
    "Disk 144: Dialogue Box: Mechanical": MMZero3ItemData(code=144, type=ItemClassification.filler),
    "Disk 145: Dialogue Box: Rosebush": MMZero3ItemData(code=145, type=ItemClassification.filler),
    "Disk 146: Dialogue Box: Command Line": MMZero3ItemData(code=146, type=ItemClassification.filler),
    "Disk 147: Dialogue Box: Chains": MMZero3ItemData(code=147, type=ItemClassification.filler),
    "Disk 148: Dialogue Box: Explosion": MMZero3ItemData(code=148, type=ItemClassification.filler),
    "Disk 149: Title Screen: Alt 1": MMZero3ItemData(code=149, type=ItemClassification.filler),
    "Disk 150: Title Screen: Alt 2": MMZero3ItemData(code=150, type=ItemClassification.filler),
    "Disk 151: Title Screen: Alt 3": MMZero3ItemData(code=151, type=ItemClassification.filler),
    "Disk 152: Title Screen: Ciel": MMZero3ItemData(code=152, type=ItemClassification.filler),
    "Disk 153: Elevator: Wood": MMZero3ItemData(code=153, type=ItemClassification.filler),
    "Disk 154: Elevator: Capsule": MMZero3ItemData(code=154, type=ItemClassification.filler),
    "Disk 155: Base Environment: Night": MMZero3ItemData(code=155, type=ItemClassification.filler),
    "Disk 156: Base Environment: Snowy": MMZero3ItemData(code=156, type=ItemClassification.filler),
    "Disk 157: Ciel PC: New": MMZero3ItemData(code=157, type=ItemClassification.filler),
    "Disk 158: Ciel PC: Vending Machine": MMZero3ItemData(code=158, type=ItemClassification.filler),
    "Disk 159: Ciel PC: Monument": MMZero3ItemData(code=159, type=ItemClassification.filler),
    "Disk 160: Ciel PC: Supercomputer": MMZero3ItemData(code=160, type=ItemClassification.filler),
    "Disk 161: Life Pickup: Blue Orbs": MMZero3ItemData(code=161, type=ItemClassification.filler),
    "Disk 162: Life Pickup: Flashing Squares": MMZero3ItemData(code=162, type=ItemClassification.filler),
    "Disk 163: E-Crystals: Orbs": MMZero3ItemData(code=163, type=ItemClassification.filler),
    "Disk 164: E-Crystals: Green": MMZero3ItemData(code=164, type=ItemClassification.filler),
    
    # 165 - 176 found through talking to NPCs. They are the only items that do nothing in game.
    # These will later be given functionality through some cool Romhack edits.
    # Zero's basic moves or stage access codes.
    "Disk 165: Ciel (Lore File)": MMZero3ItemData(code=165, type=ItemClassification.filler),
    "Disk 166: Cerveau (Lore File)": MMZero3ItemData(code=166, type=ItemClassification.filler),
    "Disk 167: Andrew (Lore File)": MMZero3ItemData(code=167, type=ItemClassification.filler),
    "Disk 168: Alouette (Lore File)": MMZero3ItemData(code=168, type=ItemClassification.filler),
    "Disk 169: Hibou (Lore File)": MMZero3ItemData(code=169, type=ItemClassification.filler),
    "Disk 170: Rocinolle (Lore File)": MMZero3ItemData(code=170, type=ItemClassification.filler),
    "Disk 171: Perroquiet (Lore File)": MMZero3ItemData(code=171, type=ItemClassification.filler),
    "Disk 172: Autruche (Lore File)": MMZero3ItemData(code=172, type=ItemClassification.filler),
    "Disk 173: Hirondelle (Lore File)": MMZero3ItemData(code=173, type=ItemClassification.filler),
    "Disk 174: Doigt (Lore File)": MMZero3ItemData(code=174, type=ItemClassification.filler),
    "Disk 175: Menart (Lore File)": MMZero3ItemData(code=175, type=ItemClassification.filler),
    "Disk 176: Pic (Lore File)": MMZero3ItemData(code=176, type=ItemClassification.filler),
    
    "Disk 177: Extra Life: Blue Z": MMZero3ItemData(code=177, type=ItemClassification.filler),
    "Disk 178: Extra Life: Green Z": MMZero3ItemData(code=178, type=ItemClassification.filler),
    "Disk 179: Black Buster Shots": MMZero3ItemData(code=179, type=ItemClassification.filler),
    "Disk 180: Nail Buster Shots": MMZero3ItemData(code=180, type=ItemClassification.filler),
    
    "Victory": MMZero3ItemData(code=300,type=ItemClassification.progression),

    # Stage access. Abandoned Research Laboratory not included, since its based on a goal condition.
    **{
        f"{stage} Access": MMZero3ItemData(
            code=180 + idx + 1,
            type=ItemClassification.progression,
        )
        for idx, stage in enumerate(stage_names)
    },
    
    # Chips
    "Ice Body Chip": MMZero3ItemData(code=197, type=ItemClassification.useful),
    "Thunder Body Chip": MMZero3ItemData(code=198, type=ItemClassification.useful),
    "Flame Body Chip": MMZero3ItemData(code=199, type=ItemClassification.progression),
    "Light Body Chip": MMZero3ItemData(code=200, type=ItemClassification.useful),
    "Absorber Body Chip": MMZero3ItemData(code=201, type=ItemClassification.useful),
    "Spike Foot Chip": MMZero3ItemData(code=202, type=ItemClassification.useful),
    "Quick Foot Chip": MMZero3ItemData(code=203, type=ItemClassification.useful),
    "Double Jump Foot Chip": MMZero3ItemData(code=204, type=ItemClassification.progression),
    "Shadow Dash Foot Chip": MMZero3ItemData(code=205, type=ItemClassification.useful),

    # EX Skills
    "EX Skill: Burst Shot": MMZero3ItemData(code=208, type=ItemClassification.useful),
    "EX Skill: Throw Blade": MMZero3ItemData(code=213, type=ItemClassification.useful),
    "EX Skill: Saber Smash": MMZero3ItemData(code=211, type=ItemClassification.useful),
    "EX Skill: 1000 Slash": MMZero3ItemData(code=214, type=ItemClassification.useful),
    "EX Skill: Shield Sweep": MMZero3ItemData(code=216, type=ItemClassification.useful),
    # Progression: It deals fire damage without needing charge attacks.
    "EX Skill: Split Heavens": MMZero3ItemData(code=212, type=ItemClassification.progression),
    "EX Skill: Blizzard Arrow": MMZero3ItemData(code=209, type=ItemClassification.useful),
    "EX Skill: Reflected Laser": MMZero3ItemData(code=206, type=ItemClassification.useful),
    "EX Skill: Soul Launcher": MMZero3ItemData(code=215, type=ItemClassification.useful),
    "EX Skill: Orbit Shield": MMZero3ItemData(code=217, type=ItemClassification.useful),
    "EX Skill: V-Shot": MMZero3ItemData(code=207, type=ItemClassification.useful),
    "EX Skill: Gale Attack": MMZero3ItemData(code=210, type=ItemClassification.useful),

    # skipping 218-220 to stay clear of A+ rank clear location IDs)

    # Other Items
    "Subtank #1": MMZero3ItemData(code=221, type=ItemClassification.progression),
    "Subtank #2": MMZero3ItemData(code=222, type=ItemClassification.progression),

    # skipping 223 because i skipped it by accident and im lazy

    # Weapons
    # A starting weapon is already at step 1, so it has one less copy.
    **{
        f"Progressive {weapon}": MMZero3ItemData(
            code=224 + idx,
            type=ItemClassification.progression,
            count=lambda world, w=weapon: len(weapon_chains[w]) - world.starting_level(w),
        )
        for idx, weapon in enumerate(weapon_names)
    },

    # Advances the Resistance Base's story state. Mostly just unlocks new NPC dialogue
    "Story Progress": MMZero3ItemData(
        code=228,
        type=ItemClassification.progression,
        count=lambda world: 2,
    ),

    # Filler Items
    "100 Energy Crystals": MMZero3ItemData(
        code=301,
        can_create=lambda world: False  # Only created from `get_filler_item_name`.
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
stage_access_names = [f"{stage} Access" for stage in stage_names]
progressive_weapon_names = [f"Progressive {weapon}" for weapon in weapon_names]

# Story Progress
STORY_MID = 1   # Mission Set 2 NPCs dialogue
STORY_LATE = 2  # Mission Set 4 NPCs dialogue

# Item groups for `!hint` and tracker filtering.
item_categories: Dict[str, range] = {
    "Secret Disks": range(1, 181),
    "Head Chips": range(1, 4),
    "Stage Access": range(181, 196),
    "Chips": range(197, 206),
    "Body Chips": range(197, 202),
    "Foot Chips": range(202, 206),
    "EX Skills": range(206, 218),
    "Subtanks": range(221, 223),
    "Weapons": range(224, 228),
}


def build_item_name_groups() -> Dict[str, Set[str]]:
    groups: Dict[str, Set[str]] = {}

    for name, data in item_data_table.items():
        if data.code is None:
            continue
        for group, ids in item_categories.items():
            if data.code in ids:
                groups.setdefault(group, set()).add(name)

    return groups


item_name_groups = build_item_name_groups()

secret_disk_names = [
    name for name, data in item_data_table.items()
    if data.code is not None and 1 <= data.code <= 180
]
