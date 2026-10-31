from __future__ import annotations

from .eva import EVA_NODE, EVA_REWARDS, EVA_POINT, EVA_POINT_SOURCES, EVA_CREST_SLOTS, EVOLVED_HUNTER, YELLOW_VESTICREST, BLUE_VESTICREST

from dataclasses import dataclass
from typing import Dict, Mapping

from BaseClasses import Location

from .display_names import (
    FLEA_DISPLAY_NAMES,
    ORDINARY_FLEA_DISPLAY_NAMES,
    clean_location_display_name,
)
from .location_display_names import (
    location_first_name, MAPPER_LOCATION_NAMES,
)
from .minor_pickups import MINOR_PICKUP_LOCATION_NAMES, WISH_CURRENCY_REWARDS
from .lore_tablets import (
    ADDITIONAL_LORE_TABLET_SOURCES,
    LORE_TABLET_CATEGORY,
    LORE_TABLET_LOCATION_NAMES,
)
from .minor_caches import (
    MINOR_CACHE_LOCATION_NAMES,
    RETIRED_MINOR_CACHE_LOCATION_NAMES,
)

LOCATION_BASE_ID = 835500


_LOCATION_FIRST_ITEM_LABELS: tuple[str, ...] = (
    'Mask Shard',
    'Spool Fragment',
    'Silk Heart',
    'Bellway',
    'Ventrica',
    'Map Purchase',
    'Map Pickup',
    'Bellshrine',
    'Crafting Kit',
    'Simple Key',
    'Memory Locket',
    'Craftmetal',
    'Mossberry',
    'Pollip Heart',
    'Silkeater',
    'Tool Pouch',
    'Beast Shard',
    'Rosary Necklace',
    'Heavy Rosary Necklace',
    'Frayed Rosary String',
    'Rosary String',
    'Pale Rosary Necklace',
    'Rosary Cache',
    'Shell Shard Cache',
    'Pristine Core',
    'Shard Bundle',
    'Shell Shard Bundle',
    'Pale Oil',
)


def _location_first_display_name(location_name: str) -> str:
    for item_label in _LOCATION_FIRST_ITEM_LABELS:
        prefix = f'{item_label}: '
        if location_name.startswith(prefix):
            return location_first_name(location_name)
    return location_name


def get_item_first_location_name(location_name: str) -> str:
    """Return the source-style name used by paired native rewards."""
    for native_name, mapped_name in MAPPER_LOCATION_NAMES.items():
        if location_name == mapped_name:
            return native_name
    if location_name == 'Relic: Bone Scroll (Greymoor) at bugs lonely resting place':
        return 'Relic: Bone Scroll (Greymoor)'
    if location_name.startswith('Flea: '):
        return location_name
    for item_label in _LOCATION_FIRST_ITEM_LABELS:
        numbered_separator = f' - {item_label} #'
        area_name, separator, number = location_name.rpartition(
            numbered_separator
        )
        if separator and number.isdigit():
            return f'{item_label}: {area_name} #{number}'
        suffix = f' - {item_label}'
        if location_name.endswith(suffix):
            return f'{item_label}: {location_name[:-len(suffix)]}'
    return location_name


@dataclass(frozen=True)
class SilksongLocationData:
    code: int | None
    category: str


CURRENT_LOCATION_SOURCE_ROWS: tuple[tuple[str, str], ...] = (
    ('Skill Unlock: Double Jump', 'Skill'),
    ('Skill Unlock: Charge Slash', 'Skill'),
    ('Skill Unlock: Silk Soar', 'Skill'),
    ('Skill Unlock: Wall Jump', 'Skill'),
    ("Skill Unlock: Drifter's Cloak", 'Skill'),
    ('Skill Unlock: Dash', 'Skill'),
    ('Skill Unlock: Harpoon', 'Skill'),
    ('Skill Unlock: Quill', 'Quill'),
    ('Skill Unlock: Needolin', 'Skill'),
    ('Tool Unlock: WebShot Forge', 'Tool'),
    ('Tool Unlock: WebShot Architect', 'Tool'),
    ('Tool Unlock: WebShot Weaver', 'Tool'),
    ('Tool Unlock: Zap Imbuement', 'Tool'),
    ('Tool Unlock: Tack', 'Tool'),
    ('Tool Unlock: Poison Pouch', 'Tool'),
    ('Tool Unlock: Silk Snare', 'Tool'),
    ('Tool Unlock: Wisp Lantern', 'Tool'),
    ('Tool Unlock: Revenge Crystal', 'Tool'),
    ('Tool Unlock: Lightning Rod', 'Tool'),
    ('Tool Unlock: Tri Pin', 'Tool'),
    ('Tool Unlock: Bell Bind', 'Tool'),
    ('Tool Unlock: Rosary Cannon', 'Tool'),
    ('Tool Unlock: Harpoon', 'Tool'),
    ('Tool Unlock: Brolly Spike', 'Tool'),
    ('Tool Unlock: Dazzle Bind', 'Tool'),
    ('Tool Unlock: Shakra Ring', 'Tool'),
    ('Tool Unlock: Screw Attack', 'Tool'),
    ('Tool Unlock: Quick Sling', 'Tool'),
    ('Tool Unlock: Musician Charm', 'Tool'),
    ('Tool Unlock: Fractured Mask', 'Tool'),
    ('Tool Unlock: Sprintmaster', 'Tool'),
    ('Tool Unlock: Weighted Anklet', 'Tool'),
    ('Tool Unlock: Multibind', 'Tool'),
    ('Tool Unlock: Reserve Bind', 'Tool'),
    ('Tool Unlock: Quickbind', 'Tool'),
    ('Tool Unlock: Barbed Wire', 'Tool'),
    ('Tool Unlock: Sting Shard', 'Tool'),
    ('Tool Unlock: Conch Drill', 'Tool'),
    ('Tool Unlock: Pimpilo', 'Tool'),
    ('Tool Unlock: Straight Pin', 'Tool'),
    ('Tool Unlock: Cogwork Flier', 'Tool'),
    ('Tool Unlock: Curve Claws', 'Tool'),
    ('Tool Unlock: Cogwork Saw', 'Tool'),
    ('Tool Unlock: Flea Brew', 'Tool'),
    ('Tool Unlock: Magnetite Dice', 'Tool'),
    ('Tool Unlock: Rosary Magnet', 'Tool'),
    ('Tool Unlock: White Ring', 'Tool'),
    ('Tool Unlock: Pinstress Tool', 'Tool'),
    ('Tool Unlock: Extractor', 'Tool'),
    ('Tool Unlock: Lifeblood Syringe', 'Tool'),
    ('Tool Unlock: Dead Mans Purse', 'Tool'),
    ('Tool Unlock: Scuttlebrace', 'Tool'),
    ('Tool Unlock: Thief Charm', 'Tool'),
    ('Tool Unlock: Compass', 'Compass'),
    ('Tool Unlock: Thief Claw', 'Tool'),
    ('Tool Unlock: Mosscreep Tool 1', 'Tool'),
    ('Tool Unlock: Mosscreep Tool 2', 'Tool'),
    ('Tool Unlock: Flintstone', 'Tool'),
    ('Tool Unlock: Maggot Charm', 'Tool'),
    ('Tool Unlock: Lava Charm', 'Tool'),
    ('Tool Unlock: Wallcling', 'Tool'),
    ('Tool Unlock: Longneedle', 'Tool'),
    ('Tool Unlock: Bone Necklace', 'Tool'),
    ('Tool Unlock: Spool Extender', 'Tool'),
    ('Tool Unlock: Flea Charm', 'Tool'),
    ('Spell Unlock: Silk Spear', 'Spell'),
    ('Spell Unlock: Parry', 'Spell'),
    ('Spell Unlock: Silk Boss Needle', 'Spell'),
    ('Spell Unlock: Silk Charge', 'Spell'),
    ('Spell Unlock: Silk Bomb', 'Spell'),
    ('Spell Unlock: Thread Sphere', 'Spell'),
    ('Crest Unlock: Witch', 'Crest'),
    ('Crest Unlock: Beast', 'Crest'),
    ('Crest Unlock: Architect', 'Crest'),
    ('Crest Unlock: Shaman', 'Crest'),
    ('Crest Unlock: Reaper', 'Crest'),
    ('Crest Unlock: Wanderer', 'Crest'),
    ('Crest Unlock: Hunter', 'Crest'),
    ('Save Flea: The Marrow (Tangle)', 'Flea'),
    ('Save Flea: Deep Docks Bellway (Eepy)', 'Flea'),
    ('Save Flea: Deep Docks Weaver Burial Spire (Squeesh)', 'Flea'),
    ('Save Flea: Far Fields Captured (Thoughtless)', 'Flea'),
    ("Save Flea: Hunter's March (Yapper)", 'Flea'),
    ('Save Flea: Greymoor Craw Lake (Gwah)', 'Flea'),
    ('Save Flea: Greymoor Tower (Snoozles)', 'Flea'),
    ('Save Flea: Shellwood (Shelly)', 'Flea'),
    ("Save Flea: Pilgrim's Rest (Sleeby)", 'Flea'),
    ('Save Flea: Blasted Steps (Nini)', 'Flea'),
    ("Save Flea: Sinner's Road (Stelf)", 'Flea'),
    ('Save Flea: Exhaust Organ (Rangle)', 'Flea'),
    ('Save Flea: Bellhart (Bellphy)', 'Flea'),
    ('Save Flea: Wormways (Snacc)', 'Flea'),
    ('Save Flea: The Slab Cell (Sway)', 'Flea'),
    ('Save Flea: Bilewater Thieves (Cower)', 'Flea'),
    ('Save Flea: Deep Docks Mines (Le Bomba)', 'Flea'),
    ('Save Flea: Wisp Thicket (Fidget)', 'Flea'),
    ('Save Flea: Bilehaven (Spangle)', 'Flea'),
    ('Save Flea: Choral Cambers Spa (Oowa)', 'Flea'),
    ('Save Flea: Sands of Karak (Crustly)', 'Flea'),
    ('Save Flea: Mount Fay (Ice Cube)', 'Flea'),
    ('Save Flea: Songclave (Groggy)', 'Flea'),
    ('Save Flea: Choral Cambers Walled (Mimi)', 'Flea'),
    ('Save Flea: Whispering Vaults (Birdy)', 'Flea'),
    ('Save Flea: Underworks (Boomy)', 'Flea'),
    ('Save Flea: The Slab Bellway (Honk Shoo)', 'Flea'),
    ('Hunter Slot Unlock: Red 0 -2', 'CrestSlot'),
    ('Hunter Slot Unlock: Blue -2 0', 'CrestSlot'),
    ('Hunter Slot Unlock: Yellow 2 0', 'CrestSlot'),
    ('Reaper Slot Unlock: Red 0 -1', 'CrestSlot'),
    ('Reaper Slot Unlock: Blue -1 1', 'CrestSlot'),
    ('Reaper Slot Unlock: Yellow 1 1', 'CrestSlot'),
    ('Wanderer Slot Unlock: Blue -2 1', 'CrestSlot'),
    ('Wanderer Slot Unlock: Blue 2 1', 'CrestSlot'),
    ('Wanderer Slot Unlock: Yellow 0 -2', 'CrestSlot'),
    ('Beast Slot Unlock: Yellow -1 0', 'CrestSlot'),
    ('Beast Slot Unlock: Yellow 1 0', 'CrestSlot'),
    ('Witch Slot Unlock: Red 0 -2', 'CrestSlot'),
    ('Witch Slot Unlock: Blue -1 0', 'CrestSlot'),
    ('Witch Slot Unlock: Blue 1 0', 'CrestSlot'),
    ('Architect Slot Unlock: Blue -1 2', 'CrestSlot'),
    ('Architect Slot Unlock: Yellow 1 2', 'CrestSlot'),
    ('Architect Slot Unlock: Yellow 2 0', 'CrestSlot'),
    ('Architect Slot Unlock: Blue -2 0', 'CrestSlot'),
    ('Shaman Slot Unlock: Blue -1 0', 'CrestSlot'),
    ('Shaman Slot Unlock: Blue 1 0', 'CrestSlot'),
    ('Mask Shard Unlock #1', 'MaskShard'),
    ('Mask Shard Unlock #2', 'MaskShard'),
    ('Mask Shard Unlock #3', 'MaskShard'),
    ('Mask Shard Unlock #4', 'MaskShard'),
    ('Mask Shard Unlock #5', 'MaskShard'),
    ('Mask Shard Unlock #6', 'MaskShard'),
    ('Mask Shard Unlock #7', 'MaskShard'),
    ('Mask Shard Unlock #8', 'MaskShard'),
    ('Mask Shard Unlock #9', 'MaskShard'),
    ('Mask Shard Unlock #10', 'MaskShard'),
    ('Mask Shard Unlock #11', 'MaskShard'),
    ('Mask Shard Unlock #12', 'MaskShard'),
    ('Mask Shard Unlock #13', 'MaskShard'),
    ('Mask Shard Unlock #14', 'MaskShard'),
    ('Mask Shard Unlock #15', 'MaskShard'),
    ('Mask Shard Unlock #16', 'MaskShard'),
    ('Mask Shard Unlock #17', 'MaskShard'),
    ('Mask Shard Unlock #18', 'MaskShard'),
    ('Mask Shard Unlock #19', 'MaskShard'),
    ('Mask Shard Unlock #20', 'MaskShard'),
    ('Spool Fragment Unlock #1', 'SpoolFragment'),
    ('Spool Fragment Unlock #2', 'SpoolFragment'),
    ('Spool Fragment Unlock #3', 'SpoolFragment'),
    ('Spool Fragment Unlock #4', 'SpoolFragment'),
    ('Spool Fragment Unlock #5', 'SpoolFragment'),
    ('Spool Fragment Unlock #6', 'SpoolFragment'),
    ('Spool Fragment Unlock #7', 'SpoolFragment'),
    ('Spool Fragment Unlock #8', 'SpoolFragment'),
    ('Spool Fragment Unlock #9', 'SpoolFragment'),
    ('Spool Fragment Unlock #10', 'SpoolFragment'),
    ('Spool Fragment Unlock #11', 'SpoolFragment'),
    ('Spool Fragment Unlock #12', 'SpoolFragment'),
    ('Spool Fragment Unlock #13', 'SpoolFragment'),
    ('Spool Fragment Unlock #14', 'SpoolFragment'),
    ('Spool Fragment Unlock #15', 'SpoolFragment'),
    ('Spool Fragment Unlock #16', 'SpoolFragment'),
    ('Spool Fragment Unlock #17', 'SpoolFragment'),
    ('Spool Fragment Unlock #18', 'SpoolFragment'),
    ('Silk Heart Unlock #1', 'SilkHeart'),
    ('Silk Heart Unlock #2', 'SilkHeart'),
    ('Silk Heart Unlock #3', 'SilkHeart'),
    ('Bellway Unlock: Deep Docks', 'Bellway'),
    ('Bellway Unlock: Far Fields', 'Bellway'),
    ('Bellway Unlock: Greymoor', 'Bellway'),
    ('Bellway Unlock: Bellhart', 'Bellway'),
    ('Bellway Unlock: Blasted Steps', 'Bellway'),
    ('Bellway Unlock: Grand Bellway', 'Bellway'),
    ('Bellway Unlock: The Slab', 'Bellway'),
    ('Bellway Unlock: Shellwood', 'Bellway'),
    ('Bellway Unlock: Bilewater', 'Bellway'),
    ('Bellway Unlock: Putrified Ducts', 'Bellway'),
    ('Ventrica Unlock: Choral Chambers', 'Ventrica'),
    ('Ventrica Unlock: Underworks', 'Ventrica'),
    ('Ventrica Unlock: Grand Bellway', 'Ventrica'),
    ('Ventrica Unlock: High Halls', 'Ventrica'),
    ('Ventrica Unlock: Songclave', 'Ventrica'),
    ('Ventrica Unlock: Memorium', 'Ventrica'),
    ('Goal', 'Event'),
    # Shakra shop purchases cannot hold progression until their route
    # requirements are represented.
    ('Map Purchase: Mosslands', 'Map'),
    ('Map Purchase: The Marrow', 'Map'),
    ('Map Purchase: Deep Docks', 'Map'),
    ('Map Purchase: Far Fields', 'Map'),
    ('Map Purchase: Wormways', 'Map'),
    ("Map Purchase: Hunter's March", 'Map'),
    ('Map Purchase: Greymoor', 'Map'),
    ('Map Purchase: Bellhart', 'Map'),
    ('Map Purchase: Shellwood', 'Map'),
    ('Map Purchase: Blasted Steps', 'Map'),
    ("Map Purchase: Sinner's Road", 'Map'),
    ('Map Purchase: Mount Fay', 'Map'),
    ('Map Purchase: Sands of Karak', 'Map'),
    ('Map Purchase: Bilewater', 'Map'),
    ('Pin Purchase: Bench', 'Pin'),
    ('Pin Purchase: Ventrica', 'Pin'),
    ('Pin Purchase: Bellway', 'Pin'),
    ('Pin Purchase: Vendor', 'Pin'),
    # SavedItem identities are kept distinct from the matching `Relic:`
    # item names so logs clearly distinguish checks from received rewards.
    ('Relic Pickup: Weaver Totem Witch', 'Relic'),
    ('Relic Pickup: Psalm Cylinder Library Roof', 'Relic'),
    ('Relic Pickup: Bone Record Wisp Top', 'Relic'),
    ('Relic Pickup: Weaver Totem Bonetown_upper_room', 'Relic'),
    ('Relic Pickup: Librarian Melody Cylinder', 'Relic'),
    ('Relic Pickup: Seal Chit City Merchant', 'Relic'),
    ('Relic Pickup: Psalm Cylinder Ward', 'Relic'),
    ('Relic Pickup: Weaver Record Conductor', 'Relic'),
    ('Relic Pickup: Psalm Cylinder Librarian', 'Relic'),
    ('Relic Pickup: Psalm Cylinder Hang', 'Relic'),
    ('Relic Pickup: Seal Chit Ward Corpse', 'Relic'),
    ('Relic Pickup: Weaver Record Sprint_Challenge', 'Relic'),
    ('Relic Pickup: Psalm Cylinder Grindle', 'Relic'),
    ('Relic Pickup: Weaver Record Weave_08', 'Relic'),
    ('Relic Pickup: Bone Record Understore_Map_Room', 'Relic'),
    ('Relic Pickup: Bone Record Bone_East_14', 'Relic'),
    ('Relic Pickup: Seal Chit Aspid_01', 'Relic'),
    ('Relic Pickup: Seal Chit Silk Siphon', 'Relic'),
    ('Relic Pickup: Bone Record Greymoor_flooded_corridor', 'Relic'),
    ('Relic Pickup: Weaver Totem Slab_Bottom', 'Relic'),
    ('Relic Pickup: Ancient Egg Abyss Middle', 'Relic'),
    # Public PlayerData completion flags. These checks observe completed
    # vanilla actions and never change combat or story state.
    ('Bell Shrine Completion: bellShrineBoneForest', 'BellShrine'),
    ('Bell Shrine Completion: bellShrineWilds', 'BellShrine'),
    ('Bell Shrine Completion: bellShrineGreymoor', 'BellShrine'),
    ('Bell Shrine Completion: bellShrineShellwood', 'BellShrine'),
    ('Bell Shrine Completion: bellShrineBellhart', 'BellShrine'),
    ('Boss Completion: defeatedMossMother', 'Boss'),
    ('Boss Completion: DefeatedBonetownBoss', 'Boss'),
    ('Boss Completion: defeatedBellBeast', 'Boss'),
    ('Boss Completion: defeatedAntQueen', 'Boss'),
    ('Boss Completion: defeatedSongGolem', 'Boss'),
    ('Boss Completion: defeatedDockForemen', 'Boss'),
    ('Boss Completion: defeatedVampireGnatBoss', 'Boss'),
    ('Boss Completion: defeatedCrowCourt', 'Boss'),
    ('Boss Completion: defeatedSplinterQueen', 'Boss'),
    ('Boss Completion: defeatedSeth', 'Boss'),
    ('Boss Completion: defeatedFlowerQueen', 'Boss'),
    ('Boss Completion: defeatedRoachkeeperChef', 'Boss'),
    ('Boss Completion: defeatedPhantom', 'Boss'),
    ('Boss Completion: DefeatedSwampShaman', 'Boss'),
    ('Boss Completion: defeatedCoralKing', 'Boss'),
    ('Boss Completion: defeatedLastJudge', 'Boss'),
    ('Boss Completion: defeatedGreyWarrior', 'Boss'),
    ('Boss Completion: defeatedFirstWeaver', 'Boss'),
    ('Boss Completion: defeatedBroodMother', 'Boss'),
    ('Boss Completion: defeatedTrobbio', 'Boss'),
    ('Boss Completion: defeatedTormentedTrobbio', 'Boss'),
    ('Boss Completion: defeatedCogworkDancers', 'Boss'),
    ('Boss Completion: defeatedLaceTower', 'Boss'),
    ('Boss Completion: defeatedSongChevalierBoss', 'Boss'),
    ('Boss Completion: defeatedWhiteCloverstag', 'Boss'),
    ('Boss Completion: defeatedCloverDancers', 'Boss'),
    ('Crafting Kit Source: Forge Tool Kit', 'Upgrade'),
    ('Crafting Kit Source: Architect Tool Kit', 'Upgrade'),
    ('Crafting Kit Source: Grindle Tool Kit', 'Upgrade'),
    ('Crafting Kit Source: Crow Feathers', 'Upgrade'),
)

# FullQuestBase asset names from quests.bundle. Setup and rumour
# assets, intermediate stages and completions already represented by an
# existing item, fragment or boss check are omitted so a single
# vanilla action does not send two locations.
QUEST_LOCATION_ASSETS: tuple[str, ...] = (
    'A Pinsmiths Tools',
    'Belltown House Mid',
    'Building Materials',
    'Building Materials (Bridge)',
    'Building Materials (Statue)',
    'Courier Delivery Bonebottom',
    'Courier Delivery Dustpens Slave',
    'Courier Delivery Fixer',
    'Courier Delivery Fleatopia',
    'Courier Delivery Mask Maker',
    'Courier Delivery Pilgrims Rest',
    'Courier Delivery Songclave',
    'Extractor Blue Worms',
    'Fine Pins',
    'Garmond Black Threaded',
    'Great Gourmand',
    'Journal',
    'Mr Mushroom',
    'Pilgrim Rags',
    'Rock Rollers',
    'Save City Merchant',
    'Save City Merchant Bridge',
    'Save Courier Short',
    'Save Courier Tall',
    'Save Sherma',
    'Shiny Bell Goomba',
    'Skull King',
    'Song Pilgrim Cloaks',
    'Songclave Donation 1',
    'Songclave Donation 2',
    'Steel Sentinel Pt2',
)

COURIER_DELIVERY_QUEST_ASSETS: frozenset[str] = frozenset((
    'Courier Delivery Bonebottom',
    'Courier Delivery Dustpens Slave',
    'Courier Delivery Fixer',
    'Courier Delivery Fleatopia',
    'Courier Delivery Mask Maker',
    'Courier Delivery Pilgrims Rest',
    'Courier Delivery Songclave',
))

BELLHOME_QUEST_LOCATION_ASSETS: tuple[str, ...] = (
    'Belltown House Start',
)

CURRENT_CORE_SOURCE_NAMES: tuple[str, ...] = (
    'Ability: Faydown Cloak',
    'Ability: Needle Strike',
    'Ancestral Art: Silk Soar',
    'Ancestral Art: Cling Grip',
    "Ability: Drifter's Cloak",
    'Ancestral Art: Swift Step',
    'Ancestral Art: Clawline',
    'Item: Quill',
    'Ancestral Art: Needolin',
    'Tool: Silkshot (Forge Daughter)',
    'Tool: Silkshot (Twelfth Architect)',
    'Tool: Silkshot (Original)',
    'Tool: Volt Filament',
    'Tool: Tacks',
    'Tool: Pollip Pouch',
    'Tool: Snare Setter',
    'Tool: Wispfire Lantern',
    'Tool: Memory Crystal',
    'Tool: Voltvessels',
    'Tool: Threefold Pin',
    'Tool: Warding Bell',
    'Tool: Rosary Cannon',
    'Tool: Longpin',
    'Tool: Sawtooth Circlet',
    'Tool: Claw Mirror',
    'Tool: Throwing Ring',
    "Tool: Delver's Drill",
    'Tool: Quick Sling',
    'Songclave Shop - Spider Strings',
    'Tool: Fractured Mask',
    'Tool: Silkspeed Anklets',
    'Tool: Weighted Belt',
    'Tool: Multibinder',
    'Tool: Reserve Bind',
    'Tool: Injector Band',
    'Tool: Barbed Bracelet',
    'Tool: Sting Shard',
    'Tool: Conchcutter',
    'Tool: Pimpillo',
    'Tool: Straight Pin',
    'Tool: Cogfly',
    'Tool: Curveclaw',
    'Tool: Cogwork Wheel',
    'Tool: Flea Brew',
    'Tool: Magnetite Dice',
    'Bone Bottom Shop - Magnetite Brooch (Grindle in Act 3)',
    'Tool: Weavelight',
    'Tool: Pin Badge',
    'Tool: Needle Phial',
    'Tool: Plasmium Phial',
    "Tool: Dead Bug's Purse",
    'Tool: Scuttlebrace',
    "Tool: Thief's Mark",
    'Tool: Compass',
    'Tool: Snitch Pick',
    "Tool: Druid's Eye",
    "Tool: Druid's Eyes",
    'Tool: Flintslate',
    'Tool: Wreath of Purity',
    'Tool: Magma Bell',
    "Songclave Shop - Ascendant's Grip",
    'Tool: Longclaw',
    'Tool: Shard Pendant',
    'Songclave Shop - Spool Extender',
    'Tool: Egg of Flealia',
    'Silk Skill: Silkspear',
    'Silk Skill: Cross Stitch',
    'Silk Skill: Pale Nails',
    'Silk Skill: Sharpdart',
    'Silk Skill: Rune Rage',
    'Silk Skill: Thread Storm',
    'Crest: Witch',
    'Crest: Beast',
    'Crest: Architect',
    'Crest: Shaman',
    'Crest: Reaper',
    'Crest: Wanderer',
    'Crest: Hunter',
)

_CORE_CANONICAL_LOCATION_NAMES: tuple[str, ...] = tuple(
    clean_location_display_name(name)
    for name in CURRENT_CORE_SOURCE_NAMES
)

_FLEA_CANONICAL_LOCATION_NAMES: tuple[str, ...] = (
    tuple(
        _location_first_display_name(name)
        for name in ORDINARY_FLEA_DISPLAY_NAMES
    )
)

_CREST_SLOT_CANONICAL_LOCATION_NAMES: tuple[str, ...] = (
    'Crest Slot: Hunter (Red 1)',
    'Crest Slot: Hunter (Blue 1)',
    'Crest Slot: Hunter (Yellow 1)',
    'Crest Slot: Reaper (Red 1)',
    'Crest Slot: Reaper (Blue 1)',
    'Crest Slot: Reaper (Yellow 1)',
    'Crest Slot: Wanderer (Blue 1)',
    'Crest Slot: Wanderer (Blue 2)',
    'Crest Slot: Wanderer (Yellow 1)',
    'Crest Slot: Beast (Yellow 1)',
    'Crest Slot: Beast (Yellow 2)',
    'Crest Slot: Witch (Red 1)',
    'Crest Slot: Witch (Blue 1)',
    'Crest Slot: Witch (Blue 2)',
    'Crest Slot: Architect (Blue 1)',
    'Crest Slot: Architect (Yellow 1)',
    'Crest Slot: Architect (Yellow 2)',
    'Crest Slot: Architect (Blue 2)',
    'Crest Slot: Shaman (Blue 1)',
    'Crest Slot: Shaman (Blue 2)',
)

_RELIC_CANONICAL_LOCATION_NAMES: tuple[str, ...] = (
    'Relic: Weaver Effigy (Keelal, Shellwood)',
    'Relic: Psalm Cylinder (East Whispering Vaults)',
    'Relic: Bone Scroll (Wisp Thicket)',
    'Relic: Weaver Effigy (Camora, Moss Grotto)',
    'Relic: Sacred Cylinder',
    'Songclave Shop - Choral Commandment',
    'Relic: Psalm Cylinder (Underworks)',
    'Relic: Rune Harp (High Halls)',
    'Relic: Psalm Cylinder (Vaultkeeper Cardinius)',
    'Relic: Psalm Cylinder (High Halls)',
    'Relic: Choral Commandment (Western Whiteward)',
    'Relic: Rune Harp (Weavenest Cindril)',
    'Relic: Psalm Cylinder (Grindle)',
    'Relic: Rune Harp (Weavenest Atla)',
    'Relic: Bone Scroll (Underworks)',
    'Relic: Bone Scroll (Far Fields)',
    'Relic: Choral Commandment (Moss Grotto)',
    'Relic: Choral Commandment (Eastern Whiteward)',
    'Relic: Bone Scroll (Greymoor) at bugs lonely resting place',
    'Relic: Weaver Effigy (Atla, The Slab)',
    'Relic: Arcane Egg',
)

# Scrounge accepts these fifteen individually persisted relic assets.
SCROUNGE_RELIC_ITEM_NAMES: tuple[str, ...] = (
    'Relic: Weaver Effigy (Keelal, Shellwood)',
    'Relic: Bone Scroll (Wisp Thicket)',
    'Relic: Weaver Effigy (Camora, Moss Grotto)',
    'Relic: Choral Commandment (Jubilana)',
    'Relic: Rune Harp (High Halls)',
    'Relic: Choral Commandment (Western Whiteward)',
    'Relic: Rune Harp (Weavenest Cindril)',
    'Relic: Rune Harp (Weavenest Atla)',
    'Relic: Bone Scroll (Underworks)',
    'Relic: Bone Scroll (Far Fields)',
    'Relic: Choral Commandment (Moss Grotto)',
    'Relic: Choral Commandment (Eastern Whiteward)',
    'Relic: Bone Scroll (Greymoor)',
    'Relic: Weaver Effigy (Atla, The Slab)',
    'Relic: Arcane Egg',
)
SCROUNGE_RELIC_ITEM_BY_TURN_IN_LOCATION: Dict[str, str] = {
    f"Relic Turn-in: {item_name.removeprefix('Relic: ')}": item_name
    for item_name in SCROUNGE_RELIC_ITEM_NAMES
}
SCROUNGE_RELIC_TURN_IN_LOCATION_NAMES: tuple[str, ...] = tuple(
    SCROUNGE_RELIC_ITEM_BY_TURN_IN_LOCATION
)

# Cardinius uses the same per-relic deposited state for the five Psalm
# Cylinders and the Sacred Cylinder. They share the individual turn-in option
# but retain their physical-source names so each deposit is unambiguous.
CARDINIUS_CYLINDER_ITEM_NAMES: tuple[str, ...] = (
    'Relic: Psalm Cylinder (East Whispering Vaults)',
    'Relic: Sacred Cylinder',
    'Relic: Psalm Cylinder (Underworks)',
    'Relic: Psalm Cylinder (Vaultkeeper Cardinius)',
    'Relic: Psalm Cylinder (High Halls)',
    'Relic: Psalm Cylinder (Grindle)',
)
CARDINIUS_CYLINDER_ITEM_BY_TURN_IN_LOCATION: Dict[str, str] = {
    f"Relic Turn-in: {item_name.removeprefix('Relic: ')}": item_name
    for item_name in CARDINIUS_CYLINDER_ITEM_NAMES
}
CARDINIUS_CYLINDER_TURN_IN_LOCATION_NAMES: tuple[str, ...] = tuple(
    CARDINIUS_CYLINDER_ITEM_BY_TURN_IN_LOCATION
)
INDIVIDUAL_RELIC_TURN_IN_ITEM_NAMES: tuple[str, ...] = (
    SCROUNGE_RELIC_ITEM_NAMES + CARDINIUS_CYLINDER_ITEM_NAMES
)
INDIVIDUAL_RELIC_ITEM_BY_TURN_IN_LOCATION: Dict[str, str] = {
    **SCROUNGE_RELIC_ITEM_BY_TURN_IN_LOCATION,
    **CARDINIUS_CYLINDER_ITEM_BY_TURN_IN_LOCATION,
}
INDIVIDUAL_RELIC_TURN_IN_LOCATION_NAMES: tuple[str, ...] = tuple(
    INDIVIDUAL_RELIC_ITEM_BY_TURN_IN_LOCATION
)
RELIC_TURN_IN_LOCATION_CATEGORY = 'RelicTurnIn'

# These names describe the persistent physical source that was collected.
_MASK_SHARD_ITEM_FIRST_LOCATION_NAMES: tuple[str, ...] = (
    'Bone Bottom Shop - Mask Shard (Grindle in Act 3)',
    'Mask Shard: Wormways',
    'Mask Shard: Far Fields (Above the Seamstress)',
    'Mask Shard: Shellwood',
    'Mask Shard: The Marrow - Deep Docks Passage',
    'Mask Shard: Weavenest Atla',
    'Mask Shard: Savage Beastfly',
    'Mask Shard: Cogwork Core',
    'Mask Shard: Whispering Vaults',
    'Mask Shard: Bilewater',
    'Mask Shard: Far Fields (Skull Cave)',
    'Mask Shard: The Slab (Key of the Apostate)',
    'Mask Shard: Mount Fay',
    'Mask Shard: Wisp Thicket',
    'Songclave Shop - Mask Shard',
    'Mask Shard: Blasted Steps',
    'Mask Shard: Fastest in Pharloom',
    'Mask Shard: The Hidden Hunter',
    'Mask Shard: Dark Hearts',
    'Mask Shard: Brightvein',
)
MASK_SHARD_LOCATION_NAMES: tuple[str, ...] = tuple(
    _location_first_display_name(name)
    for name in _MASK_SHARD_ITEM_FIRST_LOCATION_NAMES
)

_SPOOL_FRAGMENT_ITEM_FIRST_LOCATION_NAMES: tuple[str, ...] = (
    'Spool Fragment: Bone Bottom',
    'Spool Fragment: Deep Docks (Central)',
    'Spool Fragment: Greymoor',
    'Spool Fragment: The Slab',
    'Spool Fragment: Weavenest Atla',
    'Spool Fragment: Frey (Bellhart)',
    'Spool Fragment: Flea Caravan',
    'Spool Fragment: Cogwork Core',
    'Spool Fragment: Underworks (East)',
    'Spool Fragment: Grand Gate',
    'Spool Fragment: Underworks (Gauntlet)',
    'Spool Fragment: Whiteward',
    'Spool Fragment: Balm for the Wounded',
    'Spool Fragment: Deep Docks (Southeast)',
    'Spool Fragment: High Halls',
    'Spool Fragment: Memorium',
    'Spool Fragment: Grindle (Blasted Steps)',
    'Songclave Shop - Spool Fragment',
)
SPOOL_FRAGMENT_LOCATION_NAMES: tuple[str, ...] = tuple(
    _location_first_display_name(name)
    for name in _SPOOL_FRAGMENT_ITEM_FIRST_LOCATION_NAMES
)

_SILK_HEART_ITEM_FIRST_LOCATION_NAMES: tuple[str, ...] = (
    'Silk Heart: Bell Beast',
    'Silk Heart: The Unravelled',
    'Silk Heart: Lace (Cradle)',
)
SILK_HEART_LOCATION_NAMES: tuple[str, ...] = tuple(
    _location_first_display_name(name)
    for name in _SILK_HEART_ITEM_FIRST_LOCATION_NAMES
)


def _category_rename_map(
    category: str,
    canonical_names: tuple[str, ...],
) -> dict[str, str]:
    source_names = tuple(
        name
        for name, source_category in CURRENT_LOCATION_SOURCE_ROWS
        if source_category == category
    )
    if len(source_names) != len(canonical_names):
        raise ValueError(
            f'{category} rename count mismatch: '
            f'{len(source_names)} source, {len(canonical_names)} current'
        )
    return dict(zip(source_names, canonical_names))


_DIRECT_LOCATION_RENAMES: dict[str, str] = {
    **dict(zip(
        (
            name
            for name, category in CURRENT_LOCATION_SOURCE_ROWS
            if category in ('Skill', 'Quill', 'Tool', 'Compass', 'Spell', 'Crest')
        ),
        _CORE_CANONICAL_LOCATION_NAMES,
    )),
    **_category_rename_map('Flea', _FLEA_CANONICAL_LOCATION_NAMES),
    **_category_rename_map(
        'CrestSlot',
        _CREST_SLOT_CANONICAL_LOCATION_NAMES,
    ),
    **_category_rename_map('MaskShard', MASK_SHARD_LOCATION_NAMES),
    **_category_rename_map(
        'SpoolFragment',
        SPOOL_FRAGMENT_LOCATION_NAMES,
    ),
    **_category_rename_map('SilkHeart', SILK_HEART_LOCATION_NAMES),
    **_category_rename_map('Relic', _RELIC_CANONICAL_LOCATION_NAMES),
}

_DIRECT_LOCATION_RENAMES.update({
    'Simple Key: Bone Bottom Shop': 'Bone Bottom Shop - Simple Key (Grindle in Act 3)',
    'Craftmetal: Bone Bottom Shop': 'Bone Bottom Shop - Craftmetal (Grindle in Act 3)',
    'White Key': 'Songclave Shop - White Key',
    'Pin Purchase: Bench': 'Pin Purchase: Bench Pins',
    'Pin Purchase: Ventrica': 'Pin Purchase: Ventrica Pins',
    'Pin Purchase: Bellway': 'Pin Purchase: Bellway Pins',
    'Pin Purchase: Vendor': 'Pin Purchase: Vendor Pins',
    'Bell Shrine Completion: bellShrineBoneForest': 'Bellshrine: The Marrow',
    'Bell Shrine Completion: bellShrineWilds': 'Bellshrine: Deep Docks',
    'Bell Shrine Completion: bellShrineGreymoor': 'Bellshrine: Greymoor',
    'Bell Shrine Completion: bellShrineShellwood': 'Bellshrine: Shellwood',
    'Bell Shrine Completion: bellShrineBellhart': 'Bellshrine: Bellhart',
    'Boss Completion: defeatedMossMother': 'Boss: Moss Mother',
    'Boss Completion: DefeatedBonetownBoss': 'Boss: Skull Tyrant (Bone Bottom)',
    'Boss Completion: skullKingKilled': 'Boss: Skull Tyrant (Bone Bottom)',
    'Boss Completion: defeatedBellBeast': 'Boss: Bell Beast',
    'Boss Completion: defeatedAntQueen': 'Boss: Skarrsinger Karmelita',
    'Boss Completion: defeatedSongGolem': 'Boss: Fourth Chorus',
    'Boss Completion: defeatedDockForemen': 'Boss: Forebrothers Signis & Gron',
    'Boss Completion: defeatedVampireGnatBoss': 'Boss: Moorwing',
    'Boss Completion: defeatedCrowCourt': 'Boss: Crawfather',
    'Boss Completion: defeatedSplinterQueen': 'Boss: Sister Splinter',
    'Boss Completion: defeatedSeth': 'Boss: Shrine Guardian Seth',
    'Boss Completion: defeatedFlowerQueen': 'Boss: Nyleth',
    'Boss Completion: defeatedRoachkeeperChef': 'Boss: Disgraced Chef Lugoli',
    'Boss Completion: defeatedPhantom': 'Boss: Phantom',
    'Boss Completion: DefeatedSwampShaman': 'Boss: Groal the Great',
    'Boss Completion: defeatedCoralKing': 'Boss: Crust King Khann',
    'Boss Completion: defeatedCoralDrillers': 'Boss: Great Conchflies',
    'Boss Completion: defeatedLastJudge': 'Boss: Last Judge',
    'Boss Completion: defeatedGreyWarrior': 'Boss: Watcher at the Edge',
    'Boss Completion: defeatedFirstWeaver': 'Boss: First Sinner',
    'Boss Completion: defeatedBroodMother': 'Boss: Broodmother',
    'Boss Completion: defeatedTrobbio': 'Boss: Trobbio',
    'Boss Completion: defeatedTormentedTrobbio': 'Boss: Tormented Trobbio',
    'Boss Completion: defeatedCogworkDancers': 'Boss: Cogwork Dancers',
    'Boss Completion: defeatedLaceTower': 'Boss: Lace (Cradle)',
    'Boss Completion: defeatedSongChevalierBoss': 'Boss: Second Sentinel',
    'Boss Completion: defeatedWhiteCloverstag': 'Boss: Palestag',
    'Boss Completion: defeatedCloverDancers': 'Boss: Clover Dancers',
    'Boss Completion: defeatedWispPyreEffigy':
        'Boss: Father of the Flame',
    'Boss Completion: defeatedAntTrapper': 'Boss: Gurr the Outcast',
    'Boss Completion: defeatedCoralDrillerSolo':
        'Boss: Raging Conchfly',
    'Boss Completion: wardBossDefeated': 'Boss: The Unravelled',
    'Boss Completion: defeatedZapCoreEnemy': 'Boss: Voltvyrm',
    'Boss Completion: spinnerDefeated': 'Boss: Widow',
    'Boss Completion: skullKingDefeated':
        'Boss: Skull Tyrant (The Marrow)',
    'Crafting Kit Source: Forge Tool Kit': 'Crafting Kit: Forge Daughter',
    'Crafting Kit Source: Architect Tool Kit':
        'Crafting Kit: Twelfth Architect',
    'Crafting Kit Source: Grindle Tool Kit': 'Crafting Kit: Grindle',
    'Crafting Kit Source: Crow Feathers':
        'Crafting Kit: Crawbug Clearing (Creige)',
    'Tool Unlock: Dazzle Bind Upgraded': 'Dark Mirror',
    'Tool Unlock: Curve Claws Upgraded': 'Curvesickle',
})

_QUEST_DISPLAY_NAME_BY_ASSET: Mapping[str, str] = {
    'A Pinsmiths Tools': "Wish: Pinmaster's Oil",
    'Belltown House Start': 'Wish: Restoration of Bellhart',
    'Belltown House Mid': "Wish: Bellhart's Glory",
    'Building Materials': 'Wish: Bone Bottom Repairs',
    'Building Materials (Bridge)': 'Wish: A Lifesaving Bridge',
    'Building Materials (Statue)': 'Wish: An Icon of Hope',
    'Courier Delivery Bonebottom': 'Wish: Bone Bottom Supplies',
    'Courier Delivery Dustpens Slave': "Wish: Queen's Egg",
    'Courier Delivery Fixer': "Wish: Survivor's Camp Supplies",
    'Courier Delivery Fleatopia': 'Wish: Fleatopia Supplies',
    'Courier Delivery Mask Maker': 'Wish: Liquid Lacquer',
    'Courier Delivery Pilgrims Rest': "Wish: Pilgrim's Rest Supplies",
    'Courier Delivery Songclave': 'Wish: Songclave Supplies',
    'Extractor Blue Worms': 'Wish: Advanced Alchemy',
    'Fine Pins': 'Wish: Fine Pins',
    'Broodmother Hunt': 'Wish: The Wailing Mother',
    'Garmond Black Threaded': "Wish: Hero's Call",
    'Song Knight': 'Wish: Final Audience',
    'Tormented Trobbio': 'Wish: Pain, Anguish and Misery',
    'Pinstress Battle': 'Wish: Fatal Resolve',
    'Great Gourmand': 'Wish: Great Taste of Pharloom',
    'Journal': 'Wish: Bugs of Pharloom',
    'Mr Mushroom': 'Wish: Passing of the Age',
    'Pilgrim Rags': 'Wish: Garb of the Pilgrims',
    'Rock Rollers': 'Wish: Volatile Flintbeetles',
    'Save City Merchant': 'Wish: The Wandering Merchant',
    'Save City Merchant Bridge': 'Wish: The Lost Merchant',
    'Save Courier Short': 'Wish: My Missing Courier',
    'Save Courier Tall': 'Wish: My Missing Brother',
    'Save Sherma': 'Wish: Balm for the Wounded',
    'Shiny Bell Goomba': 'Wish: Silver Bells',
    'Skull King': 'Wish: The Terrible Tyrant',
    'Song Pilgrim Cloaks': 'Wish: Cloaks of the Choir',
    'Songclave Donation 1': 'Wish: Building Up Songclave',
    'Songclave Donation 2': 'Wish: Strengthening Songclave',
    'Steel Sentinel Pt2': 'Wish: A Vassal Lost',
}


_WISH_OFFER_DISPLAY_NAME_BY_ASSET: Mapping[str, str] = {
    **_QUEST_DISPLAY_NAME_BY_ASSET,
    'Ant Trapper': 'Wish: The Hidden Hunter',
    'Beastfly Hunt': 'Wish: Savage Beastfly',
    'Brolly Get': 'Wish: Flexile Spines',
    'Broodmother Hunt': 'Wish: The Wailing Mother',
    'Crow Feathers Pre': 'Wish: Crawbug Clearing',
    'Doctor Curse Cure': 'Wish: Infestation Operation',
    'Extractor Blue': "Wish: Alchemist's Assistant",
    'Flea Games Pre': 'Wish: Ecstasy of the End',
    'Huntress Quest': 'Wish: Broodfeast',
    'Mossberry Collection Pre': 'Wish: Berry Picking',
    'Pinstress Battle Pre': 'Wish: Fatal Resolve',
    'Save the Fleas Pre': 'Wish: The Lost Fleas',
    'Shakra Final Quest': "Wish: Trail's End",
    'Steel Sentinel': 'Wish: A Vassal Lost',
    'Shell Flowers': 'Wish: Rite of the Pollip',
    'Wood Witch Curse': 'Wish: Rite of Rebirth',
}


def wish_offer_display_name(asset_name: str) -> str:
    return _WISH_OFFER_DISPLAY_NAME_BY_ASSET[asset_name]


def canonicalize_location_name(location_name: str) -> str:
    """Translate a native source name to its player-facing name."""
    if location_name in _DIRECT_LOCATION_RENAMES:
        return _location_first_display_name(
            _DIRECT_LOCATION_RENAMES[location_name]
        )
    current_item_name = clean_location_display_name(location_name)
    if current_item_name != location_name:
        return _location_first_display_name(current_item_name)
    for old_prefix, current_prefix in (
        ('Mask Shard Unlock #', 'Mask Shard #'),
        ('Spool Fragment Unlock #', 'Spool Fragment #'),
        ('Silk Heart Unlock #', 'Silk Heart #'),
        ('Bellway Unlock: ', 'Bellway: '),
        ('Ventrica Unlock: ', 'Ventrica: '),
    ):
        if location_name.startswith(old_prefix):
            return _location_first_display_name(
                current_prefix + location_name[len(old_prefix):]
            )
    quest_prefix = 'Quest Completion: '
    if location_name.startswith(quest_prefix):
        asset_name = location_name[len(quest_prefix):]
        return _location_first_display_name(
            _QUEST_DISPLAY_NAME_BY_ASSET.get(asset_name, location_name)
        )
    return _location_first_display_name(location_name)


CURRENT_QUEST_LOCATION_SOURCES: tuple[str, ...] = tuple(
    f'Quest Completion: {asset_name}'
    for asset_name in QUEST_LOCATION_ASSETS
)
COURIER_DELIVERY_WISH_LOCATION_NAMES: frozenset[str] = frozenset(
    canonicalize_location_name(f'Quest Completion: {asset_name}')
    for asset_name in COURIER_DELIVERY_QUEST_ASSETS
)
CURRENT_LOCATION_SOURCE_ROWS_WITH_QUESTS = (
    *CURRENT_LOCATION_SOURCE_ROWS,
    *(
        (location_name, 'Quest')
        for location_name in CURRENT_QUEST_LOCATION_SOURCES
    ),
)

NEEDLE_UPGRADE_LOCATION_CATEGORY = 'NeedleUpgrade'
PALE_OIL_LOCATION_CATEGORY = 'PaleOil'
_NEEDLE_UPGRADE_ITEM_FIRST_LOCATION_NAMES: tuple[str, ...] = (
    'Pinmaster Plinney: Sharpened Needle',
    'Pinmaster Plinney: Shining Needle',
    'Pinmaster Plinney: Hivesteel Needle',
    'Pinmaster Plinney: Pale Steel Needle',
)
_PALE_OIL_ITEM_FIRST_LOCATION_NAMES: tuple[str, ...] = (
    'Pale Oil: Whispering Vaults',
    'Pale Oil: Great Taste of Pharloom',
    'Pale Oil: Ecstasy of the End',
)
NEEDLE_UPGRADE_LOCATION_NAMES: tuple[str, ...] = tuple(
    _location_first_display_name(name)
    for name in _NEEDLE_UPGRADE_ITEM_FIRST_LOCATION_NAMES
)
PALE_OIL_LOCATION_NAMES: tuple[str, ...] = tuple(
    _location_first_display_name(name)
    for name in _PALE_OIL_ITEM_FIRST_LOCATION_NAMES
)
PINMASTER_OIL_QUEST_LOCATION = "Wish: Pinmaster's Oil"
VOLATILE_FLINTBEETLES_QUEST_LOCATION = 'Wish: Volatile Flintbeetles'

_LOCATION_TABLE_SOURCE_UNNORMALIZED: tuple[tuple[str, str], ...] = tuple(
    (canonicalize_location_name(source_name), category)
    for source_name, category in CURRENT_LOCATION_SOURCE_ROWS_WITH_QUESTS
) + tuple(
    (location_name, NEEDLE_UPGRADE_LOCATION_CATEGORY)
    for location_name in NEEDLE_UPGRADE_LOCATION_NAMES
) + tuple(
    (location_name, PALE_OIL_LOCATION_CATEGORY)
    for location_name in PALE_OIL_LOCATION_NAMES
) + tuple(
    (location_name, 'Resource')
    for location_name in MINOR_PICKUP_LOCATION_NAMES
) + tuple(
    (location_name, 'Resource')
    for location_name in MINOR_CACHE_LOCATION_NAMES
) + (
    # This is the physical Broken SilkShot pickup in Weavenest Murglin.
    ('Ruined Tool', 'Tool'),
    (
        canonicalize_location_name(
            'Boss Completion: defeatedCoralDrillers'
        ),
        'Boss',
    ),
    # Pebb and Grindle are one fallback-aware physical source.
    ('Simple Key: Bone Bottom Shop', 'Key'),
    ('Simple Key: Roachkeeper', 'Key'),
    ('Simple Key: Songclave Shop', 'Key'),
    ('Simple Key: Sands of Karak East Bench', 'Key'),
    # Static maps use their own pickups or map machines.
    ('Map Pickup: Weavenest Atla', 'Map'),
    ('Map Purchase: Grand Gate', 'Map'),
    ('Map Pickup: Underworks', 'Map'),
    ('Map Purchase: Choral Chambers', 'Map'),
    ('Map Purchase: Whispering Vaults', 'Map'),
    ('Map Purchase: Whiteward', 'Map'),
    ('Map Pickup: Cogwork Core', 'Map'),
    ('Map Purchase: Memorium', 'Map'),
    ('Map Purchase: High Halls', 'Map'),
    ('Map Pickup: The Slab', 'Map'),
    ('Map Pickup: Putrified Ducts', 'Map'),
    ('Map Purchase: The Cradle', 'Map'),
    ('Map Pickup: Verdania', 'Map'),
    ('Map Pickup: The Abyss', 'Map'),
    # Learned songs are paired sources with dedicated randomization control.
    ("Architect's Melody", 'Melody'),
    ("Conductor's Melody", 'Melody'),
    ("Vaultkeeper's Melody", 'Melody'),
    ('Elegy of the Deep', 'Melody'),
    ('Beastling Call', 'Melody'),
    ("Memory Locket: Pilgrim's Rest Shop", 'MemoryLocket'),
    ("Memory Locket: Hunter's March", 'MemoryLocket'),
    ('Memory Locket: Greymoor', 'MemoryLocket'),
    ('Memory Locket: Halfway Home', 'MemoryLocket'),
    ('Memory Locket: Bellhart Shop', 'MemoryLocket'),
    ('Memory Locket: Bellhart Roof', 'MemoryLocket'),
    ('Memory Locket: Volatile Flintbeetles', 'MemoryLocket'),
    ('Memory Locket: The Marrow', 'MemoryLocket'),
    ('Memory Locket: Choral Chambers', 'MemoryLocket'),
    ('Memory Locket: Wormways', 'MemoryLocket'),
    ('Memory Locket: Blasted Steps', 'MemoryLocket'),
    ('Memory Locket: Underworks', 'MemoryLocket'),
    ('Memory Locket: Whispering Vaults', 'MemoryLocket'),
    ('Memory Locket: Bilewater West', 'MemoryLocket'),
    ('Memory Locket: Deep Docks', 'MemoryLocket'),
    ('Memory Locket: Bilewater East', 'MemoryLocket'),
    ('Memory Locket: The Slab', 'MemoryLocket'),
    ('Memory Locket: Memorium', 'MemoryLocket'),
    ('Memory Locket: Far Fields (Act 3)', 'MemoryLocket'),
    ('Memory Locket: Sands of Karak', 'MemoryLocket'),
    ('Craftmetal: Bone Bottom Shop', 'Craftmetal'),
    ('Craftmetal: The Marrow', 'Craftmetal'),
    ('Craftmetal: Deep Docks', 'Craftmetal'),
    ('Craftmetal: Blasted Steps', 'Craftmetal'),
    ('Craftmetal: Underworks', 'Craftmetal'),
    ('Craftmetal: Putrified Ducts', 'Craftmetal'),
    ('Craftmetal: Wisp Thicket', 'Craftmetal'),
    ('Craftmetal: Songclave Shop', 'Craftmetal'),
    ('Mossberry: Moss Grotto #1', 'Mossberry'),
    ('Mossberry: Moss Grotto #2', 'Mossberry'),
    ('Mossberry: Bone Bottom', 'Mossberry'),
    ('Mossberry: Mosshome', 'Mossberry'),
    ('Mossberry: Bonegrave', 'Mossberry'),
    ('Mossberry: Weavenest Atla', 'Mossberry'),
    ('Mossberry: Memorium', 'Mossberry'),
    ('Silkeater: Deep Docks', 'Silkeater'),
    ('Silkeater: Greymoor', 'Silkeater'),
    ('Silkeater: Blasted Steps', 'Silkeater'),
    ('Silkeater: Exhaust Organ', 'Silkeater'),
    ('Silkeater: Choral Chambers West', 'Silkeater'),
    ('Silkeater: Choral Chambers East', 'Silkeater'),
    ('Silkeater: Whispering Vaults', 'Silkeater'),
    ('Silkeater: Whiteward', 'Silkeater'),
    ('Silkeater: The Cradle', 'Silkeater'),
    ('Key of Apostate', 'MajorKey'),
    ('White Key', 'MajorKey'),
    ("Surgeon's Key", 'MajorKey'),
    ("Architect's Key", 'MajorKey'),
    ('Craw Summons', 'MajorKey'),
) + (
    # Named NPC Fleas use their own persistent world-state flags.
    ('Flea: Greymoor - Kratt', 'Flea'),
    ('Flea: Putrified Ducts - Vog', 'Flea'),
    ('Flea: Memorium - Huge Flea', 'Flea'),
) + tuple(
    # Individual turn-ins are optional observation checks. Scrounge's first
    # fifteen remain in their released order. Cardinius's six are appended.
    (location_name, RELIC_TURN_IN_LOCATION_CATEGORY)
    for location_name in INDIVIDUAL_RELIC_TURN_IN_LOCATION_NAMES
) + (
    # Native upgrade sources retain the Claw Mirror and Curveclaw names.
    ('Dark Mirror', 'Tool'),
    ('Curvesickle', 'Tool'),
    # Four stable Tool Pouch sources. Mort and Grindle are one shared
    # fallback-aware shop location. Loddie's normal and Act 3 rewards likewise
    # report one location.
    ("Tool Pouch: Pilgrim's Rest", 'ToolPouch'),
    ('Tool Pouch: Loddie', 'ToolPouch'),
    ('Tool Pouch: Bugs of Pharloom', 'ToolPouch'),
    ('Tool Pouch: Fleatopia', 'ToolPouch'),
    # Scripted Beast Shard rewards use boss and race reward hooks rather than
    # the generic pickup path. Only supported native sources are registered
    # here. Skull Tyrant remains excluded.
    ('Beast Shard: Marrowmaw', 'Resource'),
    ('Beast Shard: Craggler', 'Resource'),
    ("Beast Shard: Pilgrim's Rest", 'Resource'),
    ('Beast Shard: Memorium', 'Resource'),
    ('Beast Shard: Sprintmaster', 'Resource'),
) + tuple(
    (canonicalize_location_name(f'Quest Completion: {asset_name}'), 'Quest')
    for asset_name in BELLHOME_QUEST_LOCATION_ASSETS
) + (
    ('Boss: Father of the Flame', 'Boss'),
    ('Boss: Gurr the Outcast', 'Boss'),
    ('Boss: Raging Conchfly', 'Boss'),
    ('Boss: The Unravelled', 'Boss'),
    ('Boss: Voltvyrm', 'Boss'),
    ('Boss: Widow', 'Boss'),
    ('Boss: Skull Tyrant (The Marrow)', 'Boss'),
    ('Pollip Heart: Shellwood #1', 'PollipHeart'),
    ('Pollip Heart: Shellwood #2', 'PollipHeart'),
    ('Pollip Heart: Shellwood #3', 'PollipHeart'),
    ('Pollip Heart: Shellwood #4', 'PollipHeart'),
    ('Pollip Heart: Shellwood #5', 'PollipHeart'),
    ('Pollip Heart: Shellwood #6', 'PollipHeart'),
) + tuple(
    (location_name, LORE_TABLET_CATEGORY)
    for location_name in LORE_TABLET_LOCATION_NAMES
    if location_name not in {source.location_name for source in ADDITIONAL_LORE_TABLET_SOURCES}
) + (
    ('Boss: Grand Mother Silk', 'Boss'),
    ('Boss: Bell Eater', 'Boss'),
    ('Boss: Plasmified Zango', 'Boss'),
    ('Boss: Lost Garmond', 'Boss'),
    ('Boss: Pinstress', 'Boss'),
    ('Wish: Final Audience', 'Quest'),
    ('Wish: Pain, Anguish and Misery', 'Quest'),
    ('Wish: Fatal Resolve', 'Quest'),
) + tuple((name, category) for name, (_, category, _) in EVA_REWARDS.items()) + (
    ('Maiden Soul', 'Soul'),
    ('Hermit Soul', 'Soul'),
    ('Seeker Soul', 'Soul'),
    ('Pollen Heart', 'OldHeart'),
    ("Hunter's Heart", 'OldHeart'),
    ('Encrusted Heart', 'OldHeart'),
    ('Twisted Bud', 'TwistedBud'),
    ('Everbloom', 'Everbloom'),
    ("Sprintmaster's Memento", 'Memento'),
    ("Guardian's Memento", 'Memento'),
    ("Hero's Memento", 'Memento'),
    ('Grey Memento', 'Memento'),
    ('Surface Memento', 'Memento'),
    ('Craw Memento', 'Memento'),
    ('Shell Satchel', 'Tool'),
    ('Boss: Summoned Saviour', 'Boss'),
    ('Beast Shard: Moorwing', 'Resource'),
)

from .boss_journal import ITEM_BY_LOCATION as JOURNAL_ITEMS
_LOCATION_TABLE_SOURCE_UNNORMALIZED += tuple((name, "Journal") for name in JOURNAL_ITEMS)
_LOCATION_TABLE_SOURCE_UNNORMALIZED += tuple((source.location_name, LORE_TABLET_CATEGORY) for source in ADDITIONAL_LORE_TABLET_SOURCES[:1])
_LOCATION_TABLE_SOURCE_UNNORMALIZED += (("Boss: Lace (Deep Docks)", "Boss"),)
_LOCATION_TABLE_SOURCE_UNNORMALIZED += tuple((source.location_name, LORE_TABLET_CATEGORY) for source in ADDITIONAL_LORE_TABLET_SOURCES[1:])

_LOCATION_TABLE_SOURCE_UNNORMALIZED += (('Loddie - Heavy Rosary Necklace', 'Resource'),)
_LOCATION_TABLE_SOURCE_UNNORMALIZED += (('Key of Indolent', 'MajorKey'), ('Key of Heretic', 'MajorKey'))
_LOCATION_TABLE_SOURCE_UNNORMALIZED += (('Conjoined Heart', 'OldHeart'),)
_LOCATION_TABLE_SOURCE_UNNORMALIZED += (('Quest Completion: Broodmother Hunt', 'Resource'),)

WISH_REWARD_LOCATION_BY_COMPLETION: Mapping[str, str] = {
    "Wish: Pinmaster's Oil": canonicalize_location_name('Pinmaster Plinney: Shining Needle'),
    'Wish: Volatile Flintbeetles': 'Volatile Flintbeetles - Memory Locket',
    'Wish: Bugs of Pharloom': 'Bugs of Pharloom - Tool Pouch',
    'Wish: Great Taste of Pharloom': 'Great Taste of Pharloom - Pale Oil',
    'Wish: Balm for the Wounded': canonicalize_location_name('Spool Fragment Unlock #13'),
    'Wish: Fatal Resolve': canonicalize_location_name('Tool Unlock: Pinstress Tool'),
}


LOCATION_TABLE_SOURCE: tuple[tuple[str, str], ...] = tuple(
    (canonicalize_location_name(location_name),
     'Resource' if canonicalize_location_name(location_name) in WISH_CURRENCY_REWARDS else category)
    for location_name, category in _LOCATION_TABLE_SOURCE_UNNORMALIZED
)

QUEST_LOCATION_NAMES: tuple[str, ...] = tuple(
    canonicalize_location_name(location_name)
    for location_name in CURRENT_QUEST_LOCATION_SOURCES
) + tuple(
    canonicalize_location_name(f'Quest Completion: {asset_name}')
    for asset_name in BELLHOME_QUEST_LOCATION_ASSETS
) + (
    'Wish: Final Audience',
    'Wish: Pain, Anguish and Misery',
    'Wish: Fatal Resolve',
    'Wish: The Wailing Mother',
)

location_table: Dict[str, int] = {
    name: LOCATION_BASE_ID + index
    for index, (name, _category) in enumerate(
        entry
        for entry in LOCATION_TABLE_SOURCE
        if entry[1] != 'Event'
    )
}

RETIRED_LOCATION_NAMES = RETIRED_MINOR_CACHE_LOCATION_NAMES | {
    "Whispering Vaults - Heavy Rosary Necklace",
    "The Slab - Weaver Gate Inscription",
}

location_data_table: Dict[str, SilksongLocationData] = {
    name: SilksongLocationData(location_table.get(name), category)
    for name, category in LOCATION_TABLE_SOURCE
    if name not in RETIRED_LOCATION_NAMES
}

PAIRED_LOCATION_CATEGORIES: tuple[str, ...] = (
    'Soul',
    'OldHeart',
    'Everbloom',
    'Memento',
    'TwistedBud',
    'Eva',
    'Skill',
    'Quill',
    'Compass',
    'Tool',
    'Spell',
    'Crest',
    'Flea',
    'CrestSlot',
    'MaskShard',
    'SpoolFragment',
    'SilkHeart',
    'Bellway',
    'Ventrica',
    'Map',
    NEEDLE_UPGRADE_LOCATION_CATEGORY,
    PALE_OIL_LOCATION_CATEGORY,
    'Melody',
    'Pin',
    'Relic',
    'Upgrade',
    'Key',
    'MemoryLocket',
    'Craftmetal',
    'Mossberry',
    'PollipHeart',
    'Silkeater',
    'MajorKey',
    'Resource',
    'ToolPouch',
    'BellShrine',
    LORE_TABLET_CATEGORY,
)

OBSERVATION_LOCATION_CATEGORIES: tuple[str, ...] = (
    'Journal',
    'Boss',
    'Quest',
)

RANDOMIZATION_LOCATION_CATEGORIES: tuple[str, ...] = (
    *PAIRED_LOCATION_CATEGORIES,
    *OBSERVATION_LOCATION_CATEGORIES,
    RELIC_TURN_IN_LOCATION_CATEGORY,
)

LOCATION_NAMES_BY_CATEGORY: Dict[str, tuple[str, ...]] = {
    category: tuple(
        name
        for name, data in location_data_table.items()
        if data.category == category
    )
    for category in RANDOMIZATION_LOCATION_CATEGORIES
}

location_name_groups: Dict[str, set[str]] = {
    category: set(names)
    for category, names in LOCATION_NAMES_BY_CATEGORY.items()
    if category not in location_data_table and category != "Quest"
}
# The data package exposes this friendlier plural group label.
location_name_groups['Wishes'] = (
    set(QUEST_LOCATION_NAMES) - WISH_REWARD_LOCATION_BY_COMPLETION.keys()
) | set(WISH_REWARD_LOCATION_BY_COMPLETION.values()) | {
    canonicalize_location_name(name) for name in (
        'Mask Shard Unlock #7', 'Mask Shard Unlock #17', 'Mask Shard Unlock #18',
        'Mask Shard Unlock #19', 'Drifter\'s Cloak', 'Flea Brew', "Druid's Eye",
        "Druid's Eyes", 'Plasmium Phial', 'Pollip Pouch', 'Longclaw', 'Tacks',
        'Throwing Ring', 'Crawbug Clearing (Creige) - Crafting Kit',
        'Ecstasy of the End - Pale Oil', 'Everbloom',
    )
} & location_data_table.keys()
location_name_groups['Needle Upgrades'] = set(
    NEEDLE_UPGRADE_LOCATION_NAMES
)
location_name_groups['Pale Oils'] = set(
    PALE_OIL_LOCATION_NAMES
)
location_name_groups['Relic Turn-ins'] = set(
    INDIVIDUAL_RELIC_TURN_IN_LOCATION_NAMES
)


class SilksongLocation(Location):
    game = "Hollow Knight: Silksong"


from .progression_catalogue import BOSS_IDS as BOSS_CREDIT_LOCATIONS

BOSS_CREDIT_BY_LOCATION = {
    name: "Boss Credit: " + name.removeprefix("Boss: ")
    for name in (*sorted(BOSS_CREDIT_LOCATIONS - {"Boss: Summoned Saviour", "Boss: Lace (Deep Docks)"}),
                 "Boss: Summoned Saviour", "Boss: Lace (Deep Docks)")
}
