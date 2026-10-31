from __future__ import annotations

from .npc_souls import CATALOGUE as NPC_SOUL_CATALOGUE, item_name as npc_soul_name
from .directional_abilities import ITEMS as DIRECTIONAL_ITEMS, split_pool

from .eva import EVA_NODE, EVA_REWARDS, EVA_POINT, EVA_POINT_SOURCES, EVA_CREST_SLOTS, EVOLVED_HUNTER, YELLOW_VESTICREST, BLUE_VESTICREST, SYLPHSONG

from dataclasses import dataclass
from random import Random
from typing import Callable, Dict, FrozenSet, Mapping

from BaseClasses import Item, ItemClassification
from Options import OptionError

from .act2_scope import (
    trim_act_two_pool_entries,
    get_act_two_excluded_location_names,
)
from .display_names import clean_item_display_name
from .minor_families import (
    MINOR_FAMILY_REWARD_COUNTS,
    MINOR_FAMILY_CATEGORIES,
    MINOR_REWARD_BY_LOCATION,
    MINOR_REWARD_COUNTS,
    get_base_randomization_category,
    get_minor_family_category_for_location,
)
from .locations import (
    BOSS_CREDIT_BY_LOCATION,
    INDIVIDUAL_RELIC_TURN_IN_ITEM_NAMES,
    LOCATION_NAMES_BY_CATEGORY,
    WISH_REWARD_LOCATION_BY_COMPLETION,
    MASK_SHARD_LOCATION_NAMES,
    NEEDLE_UPGRADE_LOCATION_CATEGORY,
    PALE_OIL_LOCATION_CATEGORY,
    OBSERVATION_LOCATION_CATEGORIES,
    RELIC_TURN_IN_LOCATION_CATEGORY,
    SPOOL_FRAGMENT_LOCATION_NAMES,
    canonicalize_location_name,
    get_item_first_location_name,
    location_data_table,
)
from .lore_tablets import (
    ADDITIONAL_LORE_TABLET_SOURCES,
    LORE_TABLET_CATEGORY,
    LORE_TABLET_ITEM_BY_LOCATION,
    LORE_TABLET_ITEM_NAMES,
)
from .alphabet_mode import (
    ALPHABET_ITEM_CATEGORY,
    ALPHABET_ITEM_NAMES,
    ALPHABET_ITEM_ROWS,
    replace_filler_with_alphabet_items,
)
from .requirements import (
    SIMPLE_KEY_GREEN_PRINCE,
    get_logic_item_references,
)

ITEM_BASE_ID = 835000


@dataclass(frozen=True)
class SilksongItemData:
    code: int
    category: str
    classification: ItemClassification


CURRENT_ITEM_SOURCE_ROWS: tuple[tuple[str, str], ...] = (
    ('Ability: Faydown Cloak', 'Skill'),
    ('Ability: Needle Strike', 'Skill'),
    ('Ancestral Art: Silk Soar', 'Skill'),
    ('Ancestral Art: Cling Grip', 'Skill'),
    ("Ability: Drifter's Cloak", 'Skill'),
    ('Ancestral Art: Swift Step', 'Skill'),
    ('Ancestral Art: Clawline', 'Skill'),
    ('Item: Quill', 'Quill'),
    ('Ancestral Art: Needolin', 'Skill'),
    ('Tool: Silkshot (Forge Daughter)', 'Tool'),
    ('Tool: Silkshot (Twelfth Architect)', 'Tool'),
    ('Tool: Silkshot (Original)', 'Tool'),
    ('Tool: Volt Filament', 'Tool'),
    ('Tool: Tacks', 'Tool'),
    ('Tool: Pollip Pouch', 'Tool'),
    ('Tool: Snare Setter', 'Tool'),
    ('Tool: Wispfire Lantern', 'Tool'),
    ('Tool: Memory Crystal', 'Tool'),
    ('Tool: Voltvessels', 'Tool'),
    ('Tool: Threefold Pin', 'Tool'),
    ('Tool: Warding Bell', 'Tool'),
    ('Tool: Rosary Cannon', 'Tool'),
    ('Tool: Longpin', 'Tool'),
    ('Tool: Sawtooth Circlet', 'Tool'),
    ('Progressive Claw Mirror', 'Tool'),
    ('Tool: Throwing Ring', 'Tool'),
    ("Tool: Delver's Drill", 'Tool'),
    ('Tool: Quick Sling', 'Tool'),
    ('Tool: Spider Strings', 'Tool'),
    ('Tool: Fractured Mask', 'Tool'),
    ('Tool: Silkspeed Anklets', 'Tool'),
    ('Tool: Weighted Belt', 'Tool'),
    ('Tool: Multibinder', 'Tool'),
    ('Tool: Reserve Bind', 'Tool'),
    ('Tool: Injector Band', 'Tool'),
    ('Tool: Barbed Bracelet', 'Tool'),
    ('Tool: Sting Shard', 'Tool'),
    ('Tool: Conchcutter', 'Tool'),
    ('Tool: Pimpillo', 'Tool'),
    ('Tool: Straight Pin', 'Tool'),
    ('Tool: Cogfly', 'Tool'),
    ('Progressive Curveclaw', 'Tool'),
    ('Tool: Cogwork Wheel', 'Tool'),
    ('Tool: Flea Brew', 'Tool'),
    ('Tool: Magnetite Dice', 'Tool'),
    ('Tool: Magnetite Brooch', 'Tool'),
    ('Tool: Weavelight', 'Tool'),
    ('Tool: Pin Badge', 'Tool'),
    ('Tool: Needle Phial', 'Tool'),
    ('Tool: Plasmium Phial', 'Tool'),
    ('Tool: Shell Satchel', 'Tool'),
    ("Tool: Dead Bug's Purse", 'Tool'),
    ('Tool: Scuttlebrace', 'Tool'),
    ("Tool: Thief's Mark", 'Tool'),
    ('Tool: Compass', 'Compass'),
    ('Tool: Snitch Pick', 'Tool'),
    ('Tool: Flintslate', 'Tool'),
    ('Tool: Wreath of Purity', 'Tool'),
    ('Tool: Magma Bell', 'Tool'),
    ("Tool: Ascendant's Grip", 'Tool'),
    ('Tool: Longclaw', 'Tool'),
    ('Tool: Shard Pendant', 'Tool'),
    ('Tool: Spool Extender', 'Tool'),
    ('Tool: Egg of Flealia', 'Tool'),
    ('Silk Skill: Silkspear', 'Spell'),
    ('Silk Skill: Cross Stitch', 'Spell'),
    ('Silk Skill: Pale Nails', 'Spell'),
    ('Silk Skill: Sharpdart', 'Spell'),
    ('Silk Skill: Rune Rage', 'Spell'),
    ('Silk Skill: Thread Storm', 'Spell'),
    ('Crest: Witch', 'Crest'),
    ('Crest: Beast', 'Crest'),
    ('Crest: Architect', 'Crest'),
    ('Crest: Shaman', 'Crest'),
    ('Crest: Reaper', 'Crest'),
    ('Crest: Wanderer', 'Crest'),
    ('Crest: Hunter', 'Crest'),
    ('Flea: The Marrow', 'Flea'),
    ('Flea: Deep Docks (Bellway)', 'Flea'),
    ('Flea: Deep Docks (Weaver Burial Spire)', 'Flea'),
    ('Flea: Far Fields (Captured)', 'Flea'),
    ("Flea: Hunter's March", 'Flea'),
    ('Flea: Greymoor (Craw Lake)', 'Flea'),
    ('Flea: Greymoor (Tower)', 'Flea'),
    ('Flea: Shellwood', 'Flea'),
    ("Flea: Pilgrim's Rest", 'Flea'),
    ('Flea: Blasted Steps', 'Flea'),
    ("Flea: Sinner's Road", 'Flea'),
    ('Flea: Exhaust Organ', 'Flea'),
    ('Flea: Bellhart', 'Flea'),
    ('Flea: Wormways', 'Flea'),
    ('Flea: The Slab (Cell)', 'Flea'),
    ('Flea: Bilewater (Thieves)', 'Flea'),
    ('Flea: Deep Docks (Mines)', 'Flea'),
    ('Flea: Wisp Thicket', 'Flea'),
    ('Flea: Bilehaven', 'Flea'),
    ('Flea: Choral Chambers (Spa)', 'Flea'),
    ('Flea: Sands of Karak', 'Flea'),
    ('Flea: Mount Fay', 'Flea'),
    ('Flea: Songclave', 'Flea'),
    ('Flea: Choral Chambers (Walled Room)', 'Flea'),
    ('Flea: Whispering Vaults', 'Flea'),
    ('Flea: Underworks', 'Flea'),
    ('Flea: The Slab (Bellway)', 'Flea'),
    ('Crest Slot: Hunter (Red 1)', 'CrestSlot'),
    ('Crest Slot: Hunter (Blue 1)', 'CrestSlot'),
    ('Crest Slot: Hunter (Yellow 1)', 'CrestSlot'),
    ('Crest Slot: Reaper (Red 1)', 'CrestSlot'),
    ('Crest Slot: Reaper (Blue 1)', 'CrestSlot'),
    ('Crest Slot: Reaper (Yellow 1)', 'CrestSlot'),
    ('Crest Slot: Wanderer (Blue 1)', 'CrestSlot'),
    ('Crest Slot: Wanderer (Blue 2)', 'CrestSlot'),
    ('Crest Slot: Wanderer (Yellow 1)', 'CrestSlot'),
    ('Crest Slot: Beast (Yellow 1)', 'CrestSlot'),
    ('Crest Slot: Beast (Yellow 2)', 'CrestSlot'),
    ('Crest Slot: Witch (Red 1)', 'CrestSlot'),
    ('Crest Slot: Witch (Blue 1)', 'CrestSlot'),
    ('Crest Slot: Witch (Blue 2)', 'CrestSlot'),
    ('Crest Slot: Architect (Blue 1)', 'CrestSlot'),
    ('Crest Slot: Architect (Yellow 1)', 'CrestSlot'),
    ('Crest Slot: Architect (Yellow 2)', 'CrestSlot'),
    ('Crest Slot: Architect (Blue 2)', 'CrestSlot'),
    ('Crest Slot: Shaman (Blue 1)', 'CrestSlot'),
    ('Crest Slot: Shaman (Blue 2)', 'CrestSlot'),
    ('Mask Shard #1', 'MaskShard'),
    ('Mask Shard #2', 'MaskShard'),
    ('Mask Shard #3', 'MaskShard'),
    ('Mask Shard #4', 'MaskShard'),
    ('Mask Shard #5', 'MaskShard'),
    ('Mask Shard #6', 'MaskShard'),
    ('Mask Shard #7', 'MaskShard'),
    ('Mask Shard #8', 'MaskShard'),
    ('Mask Shard #9', 'MaskShard'),
    ('Mask Shard #10', 'MaskShard'),
    ('Mask Shard #11', 'MaskShard'),
    ('Mask Shard #12', 'MaskShard'),
    ('Mask Shard #13', 'MaskShard'),
    ('Mask Shard #14', 'MaskShard'),
    ('Mask Shard #15', 'MaskShard'),
    ('Mask Shard #16', 'MaskShard'),
    ('Mask Shard #17', 'MaskShard'),
    ('Mask Shard #18', 'MaskShard'),
    ('Mask Shard #19', 'MaskShard'),
    ('Mask Shard #20', 'MaskShard'),
    ('Spool Fragment #1', 'SpoolFragment'),
    ('Spool Fragment #2', 'SpoolFragment'),
    ('Spool Fragment #3', 'SpoolFragment'),
    ('Spool Fragment #4', 'SpoolFragment'),
    ('Spool Fragment #5', 'SpoolFragment'),
    ('Spool Fragment #6', 'SpoolFragment'),
    ('Spool Fragment #7', 'SpoolFragment'),
    ('Spool Fragment #8', 'SpoolFragment'),
    ('Spool Fragment #9', 'SpoolFragment'),
    ('Spool Fragment #10', 'SpoolFragment'),
    ('Spool Fragment #11', 'SpoolFragment'),
    ('Spool Fragment #12', 'SpoolFragment'),
    ('Spool Fragment #13', 'SpoolFragment'),
    ('Spool Fragment #14', 'SpoolFragment'),
    ('Spool Fragment #15', 'SpoolFragment'),
    ('Spool Fragment #16', 'SpoolFragment'),
    ('Spool Fragment #17', 'SpoolFragment'),
    ('Spool Fragment #18', 'SpoolFragment'),
    ('Bellway: Deep Docks', 'Bellway'),
    ('Bellway: Far Fields', 'Bellway'),
    ('Bellway: Greymoor', 'Bellway'),
    ('Bellway: Bellhart', 'Bellway'),
    ('Bellway: Blasted Steps', 'Bellway'),
    ('Bellway: Grand Bellway', 'Bellway'),
    ('Bellway: The Slab', 'Bellway'),
    ('Bellway: Shellwood', 'Bellway'),
    ('Bellway: Bilewater', 'Bellway'),
    ('Bellway: Putrified Ducts', 'Bellway'),
    ('Ventrica: Choral Chambers', 'Ventrica'),
    ('Ventrica: Underworks', 'Ventrica'),
    ('Ventrica: Grand Bellway', 'Ventrica'),
    ('Ventrica: High Halls', 'Ventrica'),
    ('Ventrica: Songclave', 'Ventrica'),
    ('Ventrica: Memorium', 'Ventrica'),
    # Maps sold by Shakra. These entries are her carried stock.
    ('Map: Mosslands', 'Map'),
    ('Map: The Marrow', 'Map'),
    ('Map: Deep Docks', 'Map'),
    ('Map: Far Fields', 'Map'),
    ('Map: Wormways', 'Map'),
    ("Map: Hunter's March", 'Map'),
    ('Map: Greymoor', 'Map'),
    ('Map: Bellhart', 'Map'),
    ('Map: Shellwood', 'Map'),
    ('Map: Blasted Steps', 'Map'),
    ("Map: Sinner's Road", 'Map'),
    ('Map: Mount Fay', 'Map'),
    ('Map: Sands of Karak', 'Map'),
    ('Map: Bilewater', 'Map'),
    # All four native Crafting Kit sources can be suppressed and award this
    # ordered progressive upgrade.
    ('Progressive Crafting Kit', 'Upgrade'),
    # Named mapping pins only. The generic A-E player markers stay vanilla.
    ('Bench Pins', 'Pin'),
    ('Ventrica Pins', 'Pin'),
    ('Bellway Pins', 'Pin'),
    ('Vendor Pins', 'Pin'),
    # Relic identities come from the native SavedItem assets.
    ('Relic: Weaver Effigy (Keelal, Shellwood)', 'Relic'),
    ('Relic: Psalm Cylinder (East Whispering Vaults)', 'Relic'),
    ('Relic: Bone Scroll (Wisp Thicket)', 'Relic'),
    ('Relic: Weaver Effigy (Camora, Moss Grotto)', 'Relic'),
    ('Relic: Sacred Cylinder', 'Relic'),
    ('Relic: Choral Commandment (Jubilana)', 'Relic'),
    ('Relic: Psalm Cylinder (Underworks)', 'Relic'),
    ('Relic: Rune Harp (High Halls)', 'Relic'),
    ('Relic: Psalm Cylinder (Vaultkeeper Cardinius)', 'Relic'),
    ('Relic: Psalm Cylinder (High Halls)', 'Relic'),
    ('Relic: Choral Commandment (Western Whiteward)', 'Relic'),
    ('Relic: Rune Harp (Weavenest Cindril)', 'Relic'),
    ('Relic: Psalm Cylinder (Grindle)', 'Relic'),
    ('Relic: Rune Harp (Weavenest Atla)', 'Relic'),
    ('Relic: Bone Scroll (Underworks)', 'Relic'),
    ('Relic: Bone Scroll (Far Fields)', 'Relic'),
    ('Relic: Choral Commandment (Moss Grotto)', 'Relic'),
    ('Relic: Choral Commandment (Eastern Whiteward)', 'Relic'),
    ('Relic: Bone Scroll (Greymoor)', 'Relic'),
    ('Relic: Weaver Effigy (Atla, The Slab)', 'Relic'),
    ('Relic: Arcane Egg', 'Relic'),
    ('Rosaries (60)', 'Currency'),
    ('Shell Shards (80)', 'Currency'),
    ('Stagger Trap', 'Trap'),
    ('Rosary Spill Trap', 'Trap'),
    ('Darkness Trap', 'Trap'),
    ('Cursed Crest Trap', 'Trap'),
    ('Muckmaggot Status Trap', 'Trap'),
    ('Progressive Swift Step', 'Skill'),
    ('Progressive Needle Upgrade', 'NeedleUpgrade'),
    ('Pale Oil', 'PaleOil'),
    ("Progressive Druid's Eyes", 'Upgrade'),
    # Appended one-time consumables. Duplicate physical sources share these
    # repeatable AP identities.
    ('Frayed Rosary String', 'Resource'),
    ('Rosary String', 'Resource'),
    ('Rosary Necklace', 'Resource'),
    ('Heavy Rosary Necklace', 'Resource'),
    ('Pale Rosary Necklace', 'Resource'),
    ('Shard Bundle', 'Resource'),
    ('Beast Shard', 'Resource'),
    ('Pristine Core', 'Resource'),
    # Breakable rosary and shell caches use compact repeatable filler.
    ('Rosaries (10)', 'Resource'),
    ('Shell Shards (10)', 'Resource'),
    # Shared prerequisite for the three mutually exclusive vanilla Silkshot
    # repairs.  Randomized seeds return it after the first two active repairs,
    # allowing every AP repair check to remain physically completable.
    ('Ruined Tool', 'Tool'),
    # Each AP item opens exactly one vanilla Simple Key door. Keys are never
    # represented as a fungible, consumable counter.
    ('Simple Key (Wormways)', 'Key'),
    ('Simple Key (Deep Docks)', 'Key'),
    ('Simple Key (Green Prince)', 'Key'),
    ('Simple Key (Rosary Bank)', 'Key'),
    # Static maps use their own physical pickups or map machines.
    ('Map: Weavenest Atla', 'Map'),
    ('Map: Grand Gate', 'Map'),
    ('Map: Underworks', 'Map'),
    ('Map: Choral Chambers', 'Map'),
    ('Map: Whispering Vaults', 'Map'),
    ('Map: Whiteward', 'Map'),
    ('Map: Cogwork Core', 'Map'),
    ('Map: Memorium', 'Map'),
    ('Map: High Halls', 'Map'),
    ('Map: The Slab', 'Map'),
    ('Map: Putrified Ducts', 'Map'),
    ('Map: The Cradle', 'Map'),
    ('Map: Verdania', 'Map'),
    ('Map: The Abyss', 'Map'),
    # Learned songs have distinct gameplay effects and their own source
    # category, separate from movement abilities and Silk Skills.
    ("Architect's Melody", 'Melody'),
    ("Conductor's Melody", 'Melody'),
    ("Vaultkeeper's Melody", 'Melody'),
    ('Elegy of the Deep', 'Melody'),
    ('Beastling Call', 'Melody'),
    ('Memory Locket', 'MemoryLocket'),
    ('Craftmetal', 'Craftmetal'),
    ('Mossberry', 'Mossberry'),
    ('Silkeater', 'Silkeater'),
    ('Key of Indolent', 'MajorKey'),
    ('Key of Heretic', 'MajorKey'),
    ('Key of Apostate', 'MajorKey'),
    ('White Key', 'MajorKey'),
    ("Surgeon's Key", 'MajorKey'),
    ("Architect's Key", 'MajorKey'),
    ('Craw Summons', 'MajorKey'),
    # The three named caravan recruits use their own persistent world-state
    # flags, but are Flea items for pool, milestone and Flea Hunt purposes.
    ('Flea: Greymoor (Kratt)', 'Flea'),
    ('Flea: Putrified Ducts (Vog)', 'Flea'),
    ('Flea: Memorium (Huge Flea)', 'Flea'),
    ('Naked Trap', 'Trap'),
    # Three copies of this ordered reward match the three Silk Heart sources.
    ('Progressive Silkheart', 'SilkHeart'),
    ('Progressive Tool Pouch', 'ToolPouch'),
    # Six copies share one item ID. Receipt order is preserved by
    # the AP item index and the client grants one native Shell Flower each.
    ('Pollip Heart', 'PollipHeart'),
    ('Growstone', 'Resource'),
    ('Rosaries (8)', 'Resource'),
    ('Rosaries (30)', 'Resource'),
    ('Rosaries (70)', 'Resource'),
    ('Rosaries (75)', 'Resource'),
    ('Rosaries (84)', 'Resource'),
    ('Rosaries (90)', 'Resource'),
    ('Rosaries (105)', 'Resource'),
    ('Rosaries (112)', 'Resource'),
    ('Rosaries (115)', 'Resource'),
    ('Rosaries (130)', 'Resource'),
    ('Rosaries (155)', 'Resource'),
    ('Shell Shards (35)', 'Resource'),
    ('Bell: The Marrow', 'BellShrine'),
    ('Bell: Deep Docks', 'BellShrine'),
    ('Bell: Greymoor', 'BellShrine'),
    ('Bell: Shellwood', 'BellShrine'),
    ('Bell: Bellhart', 'BellShrine'),
    ('Shader Trap', 'Trap'),
)

ITEM_TABLE_SOURCE: tuple[tuple[str, str], ...] = tuple(
    (clean_item_display_name(name), category)
    for name, category in CURRENT_ITEM_SOURCE_ROWS
) + tuple(
    (item_name, LORE_TABLET_CATEGORY)
    for item_name in LORE_TABLET_ITEM_NAMES
    if item_name not in {source.item_name for source in ADDITIONAL_LORE_TABLET_SOURCES}
) + ALPHABET_ITEM_ROWS + (
    ('Ledge Grab', 'InnateAbility'),
    ('Swim', 'InnateAbility'),
    (EVOLVED_HUNTER, 'Eva'),
    (YELLOW_VESTICREST, 'Eva'),
    (BLUE_VESTICREST, 'Eva'),
    (SYLPHSONG, 'Eva'),
) + (
    ('Maiden Soul', 'Soul'),
    ('Hermit Soul', 'Soul'),
    ('Seeker Soul', 'Soul'),
    ('Pollen Heart', 'OldHeart'),
    ("Hunter's Heart", 'OldHeart'),
    ('Encrusted Heart', 'OldHeart'),
    ('Twisted Bud', 'TwistedBud'),
    ('Diving Bell Key', 'MajorKey'),
    ('Everbloom', 'Everbloom'),
    ("Sprintmaster's Memento", 'Memento'),
    ("Guardian's Memento", 'Memento'),
    ("Hero's Memento", 'Memento'),
    ('Grey Memento', 'Memento'),
    ('Surface Memento', 'Memento'),
    ('Craw Memento', 'Memento'),
    ('Literacy Trap', 'Trap'),
) + tuple((name, 'Boss') for location, name in BOSS_CREDIT_BY_LOCATION.items()
          if location not in {'Boss: Lace (Deep Docks)', 'Boss: Palestag'}) + (
    ('Soul of Groal the Great', 'BossSoul'),
    ('Soul of Moss Mother', 'BossSoul'),
    ('Soul of Broodmother', 'BossSoul'),
    ('Soul of Crawfather', 'BossSoul'),
    ('Soul of Disgraced Chef Lugoli', 'BossSoul'),
    ('Soul of Raging Conchfly', 'BossSoul'),
    ('Soul of Skull Tyrant', 'BossSoul'),
    *((npc_soul_name(row['name']), 'NpcSoul') for row in NPC_SOUL_CATALOGUE),
)

from .boss_journal import ITEM_BY_LOCATION as JOURNAL_ITEMS, JOURNAL
ITEM_TABLE_SOURCE += tuple((name, "Journal") for name in JOURNAL_ITEMS.values())
ITEM_TABLE_SOURCE += tuple((source.item_name, LORE_TABLET_CATEGORY) for source in ADDITIONAL_LORE_TABLET_SOURCES[:1])
ITEM_TABLE_SOURCE += (("Boss Credit: Lace (Deep Docks)", "Boss"),)
ITEM_TABLE_SOURCE += tuple((source.item_name, LORE_TABLET_CATEGORY) for source in ADDITIONAL_LORE_TABLET_SOURCES[1:])
ITEM_TABLE_SOURCE += (("Boss Credit: Palestag", "Boss"),)
ITEM_TABLE_SOURCE += tuple((name, "InnateAbility" if name.startswith("Ledge Grab") else "Skill") for name in DIRECTIONAL_ITEMS)
ITEM_TABLE_SOURCE += (("Sprint", "Skill"), ("Conjoined Heart", "OldHeart"))

# Rename in place so every established numeric item ID remains unchanged.
NATIVE_ITEM_NAME_TO_TABLE_NAME: Mapping[str, str] = {
    'Skill: Double Jump': 'Ability: Faydown Cloak',
    'Skill: Charge Slash': 'Ability: Needle Strike',
    'Skill: Silk Soar': 'Ancestral Art: Silk Soar',
    'Skill: Wall Jump': 'Ancestral Art: Cling Grip',
    'Skill: Dash': 'Ancestral Art: Swift Step',
    'Skill: Harpoon': 'Ancestral Art: Clawline',
    'Skill: Quill': 'Item: Quill',
    'Skill: Needolin': 'Ancestral Art: Needolin',
    'Tool: WebShot Forge': 'Tool: Silkshot (Forge Daughter)',
    'Tool: WebShot Architect': 'Tool: Silkshot (Twelfth Architect)',
    'Tool: WebShot Weaver': 'Tool: Silkshot (Original)',
    'Tool: Zap Imbuement': 'Tool: Volt Filament',
    'Tool: Tack': 'Tool: Tacks',
    'Tool: Poison Pouch': 'Tool: Pollip Pouch',
    'Tool: Silk Snare': 'Tool: Snare Setter',
    'Tool: Wisp Lantern': 'Tool: Wispfire Lantern',
    'Tool: Revenge Crystal': 'Tool: Memory Crystal',
    'Tool: Lightning Rod': 'Tool: Voltvessels',
    'Tool: Tri Pin': 'Tool: Threefold Pin',
    'Tool: Bell Bind': 'Tool: Warding Bell',
    'Tool: Harpoon': 'Tool: Longpin',
    'Tool: Brolly Spike': 'Tool: Sawtooth Circlet',
    'Tool: Dazzle Bind': 'Progressive Claw Mirror',
    'Tool: Dazzle Bind Upgraded': 'Progressive Claw Mirror',
    'Tool: Shakra Ring': 'Tool: Throwing Ring',
    'Tool: Screw Attack': "Tool: Delver's Drill",
    'Tool: Musician Charm': 'Tool: Spider Strings',
    'Tool: Sprintmaster': 'Tool: Silkspeed Anklets',
    'Tool: Weighted Anklet': 'Tool: Weighted Belt',
    'Tool: Multibind': 'Tool: Multibinder',
    'Tool: Quickbind': 'Tool: Injector Band',
    'Tool: Barbed Wire': 'Tool: Barbed Bracelet',
    'Tool: Conch Drill': 'Tool: Conchcutter',
    'Tool: Pimpilo': 'Tool: Pimpillo',
    'Tool: Cogwork Flier': 'Tool: Cogfly',
    'Tool: Curve Claws': 'Progressive Curveclaw',
    'Tool: Curve Claws Upgraded': 'Progressive Curveclaw',
    'Tool: Cogwork Saw': 'Tool: Cogwork Wheel',
    'Tool: Rosary Magnet': 'Tool: Magnetite Brooch',
    'Tool: White Ring': 'Tool: Weavelight',
    'Tool: Pinstress Tool': 'Tool: Pin Badge',
    'Tool: Extractor': 'Tool: Needle Phial',
    'Tool: Lifeblood Syringe': 'Tool: Plasmium Phial',
    'Tool: Dead Mans Purse': "Tool: Dead Bug's Purse",
    'Tool: Thief Charm': "Tool: Thief's Mark",
    'Tool: Thief Claw': 'Tool: Snitch Pick',
    'Tool: Mosscreep Tool 1': "Progressive Druid's Eyes",
    'Tool: Mosscreep Tool 2': "Progressive Druid's Eyes",
    'Tool: Flintstone': 'Tool: Flintslate',
    'Tool: Maggot Charm': 'Tool: Wreath of Purity',
    'Tool: Lava Charm': 'Tool: Magma Bell',
    'Tool: Wallcling': "Tool: Ascendant's Grip",
    'Tool: Longneedle': 'Tool: Longclaw',
    'Tool: Bone Necklace': 'Tool: Shard Pendant',
    'Tool: Flea Charm': 'Tool: Egg of Flealia',
    'Spell: Silk Spear': 'Silk Skill: Silkspear',
    'Spell: Parry': 'Silk Skill: Cross Stitch',
    'Spell: Silk Boss Needle': 'Silk Skill: Pale Nails',
    'Spell: Silk Charge': 'Silk Skill: Sharpdart',
    'Spell: Silk Bomb': 'Silk Skill: Rune Rage',
    'Spell: Thread Sphere': 'Silk Skill: Thread Storm',
    'Flea: The Marrow (Tangle)': 'Flea: The Marrow',
    "Flea: Hunter's March (Yapper)": "Flea: Hunter's March",
    'Flea: Shellwood (Shelly)': 'Flea: Shellwood',
    "Flea: Pilgrim's Rest (Sleeby)": "Flea: Pilgrim's Rest",
    'Flea: Blasted Steps (Nini)': 'Flea: Blasted Steps',
    "Flea: Sinner's Road (Stelf)": "Flea: Sinner's Road",
    'Flea: Exhaust Organ (Rangle)': 'Flea: Exhaust Organ',
    'Flea: Bellhart (Bellphy)': 'Flea: Bellhart',
    'Flea: Wormways (Snacc)': 'Flea: Wormways',
    'Flea: Bilehaven (Spangle)': 'Flea: Bilehaven',
    'Flea: Sands of Karak (Crustly)': 'Flea: Sands of Karak',
    'Flea: Mount Fay (Ice Cube)': 'Flea: Mount Fay',
    'Flea: Songclave (Groggy)': 'Flea: Songclave',
    'Flea: Whispering Vaults (Birdy)': 'Flea: Whispering Vaults',
    'Flea: Underworks (Boomy)': 'Flea: Underworks',
    'Hunter Slot: Red 0 -2': 'Crest Slot: Hunter (Red 1)',
    'Hunter Slot: Blue -2 0': 'Crest Slot: Hunter (Blue 1)',
    'Hunter Slot: Yellow 2 0': 'Crest Slot: Hunter (Yellow 1)',
    'Reaper Slot: Red 0 -1': 'Crest Slot: Reaper (Red 1)',
    'Reaper Slot: Blue -1 1': 'Crest Slot: Reaper (Blue 1)',
    'Reaper Slot: Yellow 1 1': 'Crest Slot: Reaper (Yellow 1)',
    'Wanderer Slot: Blue -2 1': 'Crest Slot: Wanderer (Blue 1)',
    'Wanderer Slot: Blue 2 1': 'Crest Slot: Wanderer (Blue 2)',
    'Wanderer Slot: Yellow 0 -2': 'Crest Slot: Wanderer (Yellow 1)',
    'Beast Slot: Yellow -1 0': 'Crest Slot: Beast (Yellow 1)',
    'Beast Slot: Yellow 1 0': 'Crest Slot: Beast (Yellow 2)',
    'Witch Slot: Red 0 -2': 'Crest Slot: Witch (Red 1)',
    'Witch Slot: Blue -1 0': 'Crest Slot: Witch (Blue 1)',
    'Witch Slot: Blue 1 0': 'Crest Slot: Witch (Blue 2)',
    'Architect Slot: Blue -1 2': 'Crest Slot: Architect (Blue 1)',
    'Architect Slot: Yellow 1 2': 'Crest Slot: Architect (Yellow 1)',
    'Architect Slot: Yellow 2 0': 'Crest Slot: Architect (Yellow 2)',
    'Architect Slot: Blue -2 0': 'Crest Slot: Architect (Blue 2)',
    'Shaman Slot: Blue -1 0': 'Crest Slot: Shaman (Blue 1)',
    'Shaman Slot: Blue 1 0': 'Crest Slot: Shaman (Blue 2)',
    'Pin: Bench': 'Bench Pins',
    'Pin: Ventrica': 'Ventrica Pins',
    'Pin: Bellway': 'Bellway Pins',
    'Pin: Vendor': 'Vendor Pins',
    'Relic: Weaver Totem Witch':
        'Relic: Weaver Effigy (Keelal, Shellwood)',
    'Relic: Psalm Cylinder Library Roof':
        'Relic: Psalm Cylinder (East Whispering Vaults)',
    'Relic: Bone Record Wisp Top':
        'Relic: Bone Scroll (Wisp Thicket)',
    'Relic: Weaver Totem Bonetown_upper_room':
        'Relic: Weaver Effigy (Camora, Moss Grotto)',
    'Relic: Librarian Melody Cylinder': 'Relic: Sacred Cylinder',
    'Relic: Seal Chit City Merchant':
        'Relic: Choral Commandment (Jubilana)',
    'Relic: Psalm Cylinder Ward': 'Relic: Psalm Cylinder (Underworks)',
    'Relic: Weaver Record Conductor': 'Relic: Rune Harp (High Halls)',
    'Relic: Psalm Cylinder Librarian':
        'Relic: Psalm Cylinder (Vaultkeeper Cardinius)',
    'Relic: Psalm Cylinder Hang': 'Relic: Psalm Cylinder (High Halls)',
    'Relic: Seal Chit Ward Corpse':
        'Relic: Choral Commandment (Western Whiteward)',
    'Relic: Weaver Record Sprint_Challenge':
        'Relic: Rune Harp (Weavenest Cindril)',
    'Relic: Psalm Cylinder Grindle': 'Relic: Psalm Cylinder (Grindle)',
    'Relic: Weaver Record Weave_08': 'Relic: Rune Harp (Weavenest Atla)',
    'Relic: Bone Record Understore_Map_Room':
        'Relic: Bone Scroll (Underworks)',
    'Relic: Bone Record Bone_East_14':
        'Relic: Bone Scroll (Far Fields)',
    'Relic: Seal Chit Aspid_01':
        'Relic: Choral Commandment (Moss Grotto)',
    'Relic: Seal Chit Silk Siphon':
        'Relic: Choral Commandment (Eastern Whiteward)',
    'Relic: Bone Record Greymoor_flooded_corridor':
        'Relic: Bone Scroll (Greymoor)',
    'Relic: Weaver Totem Slab_Bottom':
        'Relic: Weaver Effigy (Atla, The Slab)',
    'Relic: Ancient Egg Abyss Middle': 'Relic: Arcane Egg',
}

NATIVE_ITEM_NAME_TO_CURRENT: Mapping[str, str] = {
    native_name: clean_item_display_name(table_name)
    for native_name, table_name in NATIVE_ITEM_NAME_TO_TABLE_NAME.items()
}
NATIVE_ITEM_NAME_TO_CURRENT = {
    **NATIVE_ITEM_NAME_TO_CURRENT,
    **{
        source_name: current_name
        for source_name, _category in CURRENT_ITEM_SOURCE_ROWS
        if (
            current_name := clean_item_display_name(source_name)
        ) != source_name
    },
    # These are the native ToolItem identities used by the two physical
    # Mosscreep sources. Current rooms award the one progressive item.
    'Tool: Mosscreep Tool 1': "Progressive Druid's Eyes",
    'Tool: Mosscreep Tool 2': "Progressive Druid's Eyes",
}

POOL_ONLY_USEFUL_ITEM_NAMES: tuple[str, ...] = (
    'Shell Satchel',
    'Growstone',
)
POOL_ONLY_FILLER_SOURCE_CATEGORIES: tuple[str, ...] = (
    'Quest',
    'Boss',
    RELIC_TURN_IN_LOCATION_CATEGORY,
)

PROGRESSION_ITEMS: FrozenSet[str] = frozenset(
    name
    for name, category in ITEM_TABLE_SOURCE
    if category in {
        "Skill",
        "Quill",
        "Flea",
        "Crest",
        "Key",
        "Map",
        "Melody",
        "MemoryLocket",
        "Craftmetal",
        "Mossberry",
        "PollipHeart",
        "MajorKey",
        "ToolPouch",
        ALPHABET_ITEM_CATEGORY,
        'InnateAbility',
        'Soul',
        'OldHeart',
        'Everbloom',
        'TwistedBud',
    }
) | (
    get_logic_item_references()
    - frozenset(INDIVIDUAL_RELIC_TURN_IN_ITEM_NAMES)
) | frozenset({
    'Relic: Sacred Cylinder',
    'Progressive Crafting Kit',
}) | frozenset(BOSS_CREDIT_BY_LOCATION['Boss: ' + name] for name in (
    'Bell Beast', 'Cogwork Dancers', 'Fourth Chorus', 'Great Conchflies', 'Groal the Great',
    'Skull Tyrant (The Marrow)', 'Widow', 'Lace (Cradle)', 'Summoned Saviour',
))

USEFUL_ITEMS: FrozenSet[str] = frozenset(
    name
    for name, category in ITEM_TABLE_SOURCE
    if name not in {
        'Relic: Sacred Cylinder',
        'Progressive Crafting Kit',
    } and category in {
        "Tool",
        "Compass",
        "Spell",
        "Eva",
        "CrestSlot",
        "MaskShard",
        "SpoolFragment",
        "SilkHeart",
        "Upgrade",
        "Pin",
        "Relic",
        "Silkeater",
        "BellShrine",
        "Boss",
    }
) | frozenset(POOL_ONLY_USEFUL_ITEM_NAMES)

item_table: Dict[str, int] = {
    name: ITEM_BASE_ID + index
    for index, (name, _category) in enumerate(ITEM_TABLE_SOURCE)
}

ITEM_TABLE_SOURCE = tuple(dict.fromkeys(ITEM_TABLE_SOURCE))

from .enemy_souls import CATALOGUE as ENEMY_SOUL_CATALOGUE, item_name as enemy_soul_name
from .boss_souls import CATALOGUE as BOSS_SOUL_CATALOGUE, SETH_SOUL
item_table.update({npc_soul_name(row["name"]): row["item_id"] for row in NPC_SOUL_CATALOGUE})
item_table.update({enemy_soul_name(row['name']): row['item_id'] for row in ENEMY_SOUL_CATALOGUE})
item_table.update({row["item"]: row["item_id"] for row in BOSS_SOUL_CATALOGUE})

item_table[SETH_SOUL] = 842038

VICTORY_ITEM_NAME = "Victory"
ITEM_CATEGORY_BY_NAME: Dict[str, str] = dict(ITEM_TABLE_SOURCE)
ITEM_CATEGORY_BY_NAME.update({enemy_soul_name(row["name"]): "EnemySoul" for row in ENEMY_SOUL_CATALOGUE})
ITEM_CATEGORY_BY_NAME.update({row["item"]: "BossSoul" for row in BOSS_SOUL_CATALOGUE})

ITEM_CATEGORY_BY_NAME[SETH_SOUL] = "BossSoul"

item_name_groups: Dict[str, set[str]] = {
    "Skills": {name for name, category in ITEM_TABLE_SOURCE if category == "Skill"},
    "Spells": {name for name, category in ITEM_TABLE_SOURCE if category == "Spell"},
    "Crests": {name for name, category in ITEM_TABLE_SOURCE if category == "Crest"},
    "Tools": {
        name
        for name, category in ITEM_TABLE_SOURCE
        if category in {"Tool", "Compass"}
    },
    "Fleas": {name for name, category in ITEM_TABLE_SOURCE if category == "Flea"},
    "MaskShard": {name for name, category in ITEM_TABLE_SOURCE if category == "MaskShard"},
    "SpoolFragment": {name for name, category in ITEM_TABLE_SOURCE if category == "SpoolFragment"},
    "SilkHeart": {
        name
        for name, category in ITEM_TABLE_SOURCE
        if category == "SilkHeart"
    },
    "Bells": {name for name, category in ITEM_TABLE_SOURCE if category == "BellShrine"},
    "Bellway": {name for name, category in ITEM_TABLE_SOURCE if category == "Bellway"},
    "Ventrica": {name for name, category in ITEM_TABLE_SOURCE if category == "Ventrica"},
    "Maps": {name for name, category in ITEM_TABLE_SOURCE if category == "Map"},
    "Melodies": {
        name for name, category in ITEM_TABLE_SOURCE if category == "Melody"
    },
    "Upgrades": {name for name, category in ITEM_TABLE_SOURCE if category == "Upgrade"},
    "Pins": {name for name, category in ITEM_TABLE_SOURCE if category == "Pin"},
    "Relics": {name for name, category in ITEM_TABLE_SOURCE if category == "Relic"},
    "Memory Lockets": {
        name for name, category in ITEM_TABLE_SOURCE
        if category == "MemoryLocket"
    },
    "Craftmetals": {
        name for name, category in ITEM_TABLE_SOURCE
        if category == "Craftmetal"
    },
    "Mossberries": {
        name for name, category in ITEM_TABLE_SOURCE
        if category == "Mossberry"
    },
    "Pollip Hearts": {
        name for name, category in ITEM_TABLE_SOURCE
        if category == "PollipHeart"
    },
    "Silkeaters": {
        name for name, category in ITEM_TABLE_SOURCE
        if category == "Silkeater"
    },
    "Tool Pouches": {
        name for name, category in ITEM_TABLE_SOURCE
        if category == "ToolPouch"
    },
    "Major Keys": {
        name for name, category in ITEM_TABLE_SOURCE
        if category == "MajorKey"
    },
    "Simple Keys": {
        name for name, category in ITEM_TABLE_SOURCE if category == "Key"
    },
    "Currency": {name for name, category in ITEM_TABLE_SOURCE if category == "Currency"},
    "Resources": {name for name, category in ITEM_TABLE_SOURCE if category == "Resource"},
    "Boss Credits": set(BOSS_CREDIT_BY_LOCATION.values()),
    "Journal Entries": set(JOURNAL_ITEMS.values()) - {JOURNAL},
    "Enemy Souls": {enemy_soul_name(row["name"]) for row in ENEMY_SOUL_CATALOGUE},
    "NPC Souls": {npc_soul_name(row["name"]) for row in NPC_SOUL_CATALOGUE if not row.get("legacy")},
    "Boss Souls": {row["item"] for row in BOSS_SOUL_CATALOGUE} | {SETH_SOUL},
    "Traps": {name for name, category in ITEM_TABLE_SOURCE if category == "Trap"},
    "Needle Upgrades": {'Progressive Needle Upgrade'},
    "Pale Oils": {'Pale Oil'},
    "Lore": {
        name
        for name, category in ITEM_TABLE_SOURCE
        if category == LORE_TABLET_CATEGORY
    },
    "Alphabet Letters": set(ALPHABET_ITEM_NAMES),
    "Innate Abilities": {
        name
        for name, category in ITEM_TABLE_SOURCE
        if category == "InnateAbility"
    },
}


def _classification_for(name: str) -> ItemClassification:
    if ITEM_CATEGORY_BY_NAME[name] == "Trap":
        return ItemClassification.trap
    if ITEM_CATEGORY_BY_NAME[name] in {"BossSoul", "NpcSoul", "EnemySoul"}:
        return ItemClassification.progression
    if name in DIRECTIONAL_ITEMS:
        return ItemClassification.progression
    if name == JOURNAL:
        return ItemClassification.progression
    if ITEM_CATEGORY_BY_NAME[name] == "Journal":
        return ItemClassification.filler
    if name in PROGRESSION_ITEMS:
        return ItemClassification.progression
    if name in USEFUL_ITEMS:
        return ItemClassification.useful
    return ItemClassification.filler


item_data_table: Dict[str, SilksongItemData] = {
    name: SilksongItemData(item_table[name], category, _classification_for(name))
    for name, category in ITEM_TABLE_SOURCE
}
item_data_table.update({enemy_soul_name(row["name"]): SilksongItemData(row["item_id"], "EnemySoul", ItemClassification.progression) for row in ENEMY_SOUL_CATALOGUE})
item_data_table.update({row["item"]: SilksongItemData(row["item_id"], "BossSoul", ItemClassification.progression) for row in BOSS_SOUL_CATALOGUE})

item_data_table[SETH_SOUL] = SilksongItemData(item_table[SETH_SOUL], "BossSoul", ItemClassification.progression)

# Archipelago permits several copies to share one item ID/name. The client
# applies these by received-item index, so progressive upgrades and currency
# remain repeatable without inventing numbered aliases.
ITEM_POOL_COUNTS: Dict[str, int] = {
    'Flea': 27,
    'Mask Shard': 20,
    'Spool Fragment': 18,
    EVOLVED_HUNTER: 2,
    'Progressive Crafting Kit': 4,
    "Progressive Druid's Eyes": 2,
    'Progressive Claw Mirror': 2,
    'Progressive Curveclaw': 2,
    'Progressive Silkheart': 3,
    # Baseline rewards are replaced with eligible boss credits after goal trimming.
    'Rosaries (60)': 20,
    'Shell Shards (80)': 19,
    'Memory Locket': 20,
    'Craftmetal': 8,
    'Mossberry': 7,
    'Pollip Heart': 6,
    'Silkeater': 9,
    'Progressive Tool Pouch': 4,
    'Shell Satchel': 1,
    'Growstone': 1,
}

PROGRESSIVE_SWIFT_STEP_ITEM = 'Progressive Swift Step'
PROGRESSIVE_SILK_HEART_ITEM = 'Progressive Silkheart'
REGULAR_SWIFT_STEP_ITEM = 'Swift Step'
PROGRESSIVE_NEEDLE_UPGRADE_ITEM = 'Progressive Needle Upgrade'
PALE_OIL_ITEM = 'Pale Oil'
LEDGE_GRAB_ITEM = 'Ledge Grab'
SWIM_ITEM = 'Swim'
INNATE_ABILITY_ITEM_NAMES = (LEDGE_GRAB_ITEM, SWIM_ITEM)
SILK_SOAR_ITEM = 'Silk Soar'
QUILL_ITEM = 'Item: Quill'
NEEDLE_UPGRADE_POOL_COUNTS: Mapping[str, int] = {
    PROGRESSIVE_NEEDLE_UPGRADE_ITEM: 4,
}
PALE_OIL_POOL_COUNTS: Mapping[str, int] = {
    PALE_OIL_ITEM: 3,
}

# Quest Sanity adds one ordinary currency filler per added quest check. These
# copies participate in trap_percentage whenever Quest Sanity is randomized.
QUEST_FILLER_COUNTS: Dict[str, int] = {
    'Rosaries (60)': 15,
    'Shell Shards (80)': 9,
}

# These items enter the pool only when their corresponding option is enabled.
CONDITIONAL_POOL_ITEM_NAMES: FrozenSet[str] = frozenset({
    PROGRESSIVE_SWIFT_STEP_ITEM,
    'Sprint',
    *DIRECTIONAL_ITEMS,
    *PALE_OIL_POOL_COUNTS,
    *NEEDLE_UPGRADE_POOL_COUNTS,
    *ALPHABET_ITEM_NAMES,
    *INNATE_ABILITY_ITEM_NAMES,
    'Diving Bell Key',
    *JOURNAL_ITEMS.values(),
})

TRAP_ITEM_NAME_BY_WEIGHT_OPTION: Dict[str, str] = {
    'stagger_trap_weight': 'Stagger Trap',
    'rosary_spill_trap_weight': 'Rosary Spill Trap',
    'darkness_trap_weight': 'Darkness Trap',
    'cursed_crest_trap_weight': 'Cursed Crest Trap',
    'muckmaggot_status_trap_weight': 'Muckmaggot Status Trap',
    'naked_trap_weight': 'Naked Trap',
    'literacy_trap_weight': 'Literacy Trap',
    'shader_trap_weight': 'Shader Trap',
}
TRAP_ITEM_NAMES: tuple[str, ...] = tuple(
    TRAP_ITEM_NAME_BY_WEIGHT_OPTION.values()
)

STARTING_CREST_ITEM_BY_KEY: Dict[str, str | None] = {
    'naked': None,
    'hunter': 'Crest: Hunter',
    'wanderer': 'Crest: Wanderer',
    'reaper': 'Crest: Reaper',
    'beast': 'Crest: Beast',
    'architect': 'Crest: Architect',
    'witch': 'Crest: Witch',
    'shaman': 'Crest: Shaman',
}
STARTING_CREST_KEYS: tuple[str, ...] = tuple(STARTING_CREST_ITEM_BY_KEY)
START_WITH_MAP_ITEMS: tuple[str, ...] = tuple(
    name
    for name, category in ITEM_TABLE_SOURCE
    if category == 'Map'
)
ACT_TWO_START_WITH_MAP_ITEMS: tuple[str, ...] = tuple(
    name
    for name in START_WITH_MAP_ITEMS
    if name not in {'Map: The Abyss', 'Map: Verdania'}
)
AUTOMATIC_COMPASS_ITEM = 'Compass'
OPTIONAL_START_REPLACEMENT_ITEM = 'Rosaries (60)'


@dataclass(frozen=True)
class ItemPoolEntry:
    name: str
    source_category: str
    placement_category: str | None = None


def _is_replaceable_filler(item_name: str) -> bool:
    data = item_data_table[item_name]
    return data.classification == ItemClassification.filler and data.category not in {'Memento', 'Journal'}


def add_pool_only_useful_items(
    entries: list[ItemPoolEntry], reserved_filler: int = 0, reserved_anywhere_filler: int = 0,
) -> None:
    present_names = {
        entry.name
        for entry in entries
        if entry.name in POOL_ONLY_USEFUL_ITEM_NAMES
    }
    for item_name in POOL_ONLY_USEFUL_ITEM_NAMES:
        if item_name in present_names:
            continue
        if reserved_filler and sum(_is_replaceable_filler(entry.name) for entry in entries) <= reserved_filler:
            break
        if reserved_anywhere_filler and sum(
            entry.placement_category is None and _is_replaceable_filler(entry.name) for entry in entries
        ) <= reserved_anywhere_filler:
            break
        replacement_index = None
        for classification in (
            ItemClassification.filler,
            ItemClassification.trap,
        ):
            replacement_index = next(
                (
                    index
                    for source_category in POOL_ONLY_FILLER_SOURCE_CATEGORIES
                    for index, entry in enumerate(entries)
                    if entry.source_category == source_category
                    and item_data_table[entry.name].classification
                    == classification
                ),
                None,
            )
            if replacement_index is not None:
                break
        if replacement_index is None:
            continue
        replaced_entry = entries[replacement_index]
        entries[replacement_index] = ItemPoolEntry(
            item_name,
            replaced_entry.source_category,
            replaced_entry.placement_category,
        )


def replace_filler_with_innate_ability_items(
    entries: list[ItemPoolEntry],
    item_names: tuple[str, ...],
    randomizer: Random | None = None,
) -> None:
    if not item_names:
        return
    eligible_indices = [
        index
        for index, entry in enumerate(entries)
        if _is_replaceable_filler(entry.name)
    ]
    if len(eligible_indices) < len(item_names):
        raise OptionError(
            "Optional item randomization needs "
            f"{len(item_names)} filler rewards in the configured random "
            f"pool but only {len(eligible_indices)} are available."
        )
    unrestricted_indices = [
        index
        for index in eligible_indices
        if entries[index].placement_category is None
    ]
    restricted_indices = [
        index
        for index in eligible_indices
        if entries[index].placement_category is not None
    ]
    if randomizer is not None:
        randomizer.shuffle(unrestricted_indices)
        randomizer.shuffle(restricted_indices)
    eligible_indices = unrestricted_indices + restricted_indices
    for entry_index, item_name in zip(eligible_indices, item_names):
        replaced_entry = entries[entry_index]
        entries[entry_index] = ItemPoolEntry(
            item_name,
            replaced_entry.source_category,
            replaced_entry.placement_category,
        )

OBSERVATION_FILLER_COUNTS_BY_CATEGORY: Dict[str, Dict[str, int]] = {
    # Observation checks use ordinary filler rather than boss rewards.
    'Boss': {
        'Rosaries (60)': 20,
        'Shell Shards (80)': 20,
    },
    'Quest': dict(QUEST_FILLER_COUNTS),
}

# Enabling the fifteen Scrounge and six Cardinius deposit checks adds the same
# number of unrestricted rewards. These ordinary filler copies are eligible
# for the configured trap percentage like every other filler source.
RELIC_TURN_IN_FILLER_COUNTS: Dict[str, int] = {
    'Rosaries (60)': 11,
    'Shell Shards (80)': 10,
}

PAIRED_ITEM_CATEGORIES: tuple[str, ...] = (
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

REPEATED_CATEGORY_ITEM_COUNTS: Mapping[str, Mapping[str, int]] = {
    'Flea': {'Flea': 27, 'Flea (Kratt)': 1, 'Flea (Vog)': 1, 'Flea (Huge Flea)': 1},
    'MaskShard': {'Mask Shard': 20},
    'SpoolFragment': {'Spool Fragment': 18},
    'SilkHeart': {'Progressive Silkheart': 3},
    'MemoryLocket': {'Memory Locket': 20},
    'Craftmetal': {'Craftmetal': 8},
    NEEDLE_UPGRADE_LOCATION_CATEGORY: NEEDLE_UPGRADE_POOL_COUNTS,
    PALE_OIL_LOCATION_CATEGORY: PALE_OIL_POOL_COUNTS,
    'Mossberry': {'Mossberry': 7},
    'PollipHeart': {'Pollip Heart': 6},
    'Silkeater': {'Silkeater': 9},
    'ToolPouch': {'Progressive Tool Pouch': 4},
}

OBSERVATION_ITEM_CATEGORIES: tuple[str, ...] = (
    'Boss',
    'Quest',
)

def get_category_item_names(category: str) -> tuple[str, ...]:
    """Return the exact reward multiset paired with a source category."""

    if category == 'Eva':
        return tuple(reward for reward, _, _ in EVA_REWARDS.values())
    if category == LORE_TABLET_CATEGORY:
        return tuple(
            item for location, item in LORE_TABLET_ITEM_BY_LOCATION.items()
            if location in location_data_table
        )
    if category in MINOR_FAMILY_CATEGORIES:
        family_key = category.split(":", 1)[1]
        return tuple(
            item_name
            for item_name, count in
            MINOR_FAMILY_REWARD_COUNTS[family_key].items()
            for _copy_index in range(count)
        )
    if category == 'Tool':
        return (
            *(
                name
                for name, item_category in ITEM_TABLE_SOURCE
                if (
                    item_category == 'Tool'
                    and name not in POOL_ONLY_USEFUL_ITEM_NAMES
                )
            ),
            "Progressive Druid's Eyes",
            "Progressive Druid's Eyes",
            # Each progressive identity already appears once in the Tool
            # table above. These second copies balance the added upgrade
            # sources while preserving strict base-before-upgrade receipt.
            'Progressive Claw Mirror',
            'Progressive Curveclaw',
        )
    if category == 'Upgrade':
        return ('Progressive Crafting Kit',) * 4
    if category == 'Resource':
        return tuple(
            MINOR_REWARD_BY_LOCATION[location_name]
            for location_name in MINOR_REWARD_BY_LOCATION
        )
    if category in REPEATED_CATEGORY_ITEM_COUNTS:
        return tuple(
            item_name
            for item_name, count
            in REPEATED_CATEGORY_ITEM_COUNTS[category].items()
            for _copy_index in range(count)
        )

    excluded_names = (
        set(TRAP_ITEM_NAMES)
        | set(CONDITIONAL_POOL_ITEM_NAMES)
        | set(POOL_ONLY_USEFUL_ITEM_NAMES)
    )
    return tuple(
        name
        for name, item_category in ITEM_TABLE_SOURCE
        if item_category == category and name not in excluded_names
    )


def get_vanilla_reward_name(
    location_name: str,
    category: str,
) -> str:
    """Get this check's vanilla reward."""

    location_name = canonicalize_location_name(location_name)
    shop_reward = {
        'Songclave Shop - Spider Strings': 'Spider Strings',
        'Bone Bottom Shop - Magnetite Brooch (Grindle in Act 3)': 'Magnetite Brooch',
        "Songclave Shop - Ascendant's Grip": "Ascendant's Grip",
        'Songclave Shop - Spool Extender': 'Spool Extender',
        'Songclave Shop - Choral Commandment': 'Relic: Choral Commandment (Jubilana)',
    }.get(location_name)
    if shop_reward is not None:
        return shop_reward
    if location_name in EVA_REWARDS:
        return EVA_REWARDS[location_name][0]
    source_location_name = get_item_first_location_name(location_name)

    if category == 'Key':
        try:
            return {
                'Bone Bottom Shop - Simple Key (Grindle in Act 3)':
                    'Simple Key (Wormways)',
                'Simple Key: Roachkeeper':
                    'Simple Key (Green Prince)',
                'Simple Key: Songclave Shop':
                    'Simple Key (Rosary Bank)',
                'Simple Key: Sands of Karak East Bench':
                    'Simple Key (Deep Docks)',
            }[source_location_name]
        except KeyError as exc:
            raise ValueError(
                f"No native Key reward mapping for {location_name!r}."
            ) from exc
    if category == 'Flea':
        return clean_item_display_name(source_location_name)
    if category in REPEATED_CATEGORY_ITEM_COUNTS:
        return next(iter(REPEATED_CATEGORY_ITEM_COUNTS[category]))
    if category == 'MajorKey':
        try:
            return {
                'Key of Indolent': 'Key of Indolent',
                'Key of Heretic': 'Key of Heretic',
                'Key of Apostate': 'Key of Apostate',
                'Songclave Shop - White Key': 'White Key',
                "Surgeon's Key": "Surgeon's Key",
                "Architect's Key": "Architect's Key",
                'Craw Summons': 'Craw Summons',
            }[location_name]
        except KeyError as exc:
            raise ValueError(
                f"No native MajorKey reward mapping for {location_name!r}."
            ) from exc
    if category == 'BellShrine':
        try:
            return {
                'The Marrow - Bellshrine': 'Bell: The Marrow',
                'Deep Docks - Bellshrine': 'Bell: Deep Docks',
                'Greymoor - Bellshrine': 'Bell: Greymoor',
                'Shellwood - Bellshrine': 'Bell: Shellwood',
                'Bellhart - Bellshrine': 'Bell: Bellhart',
            }[location_name]
        except KeyError as exc:
            raise ValueError(
                f"No native BellShrine reward mapping for "
                f"{location_name!r}."
            ) from exc
    if category == LORE_TABLET_CATEGORY:
        try:
            return LORE_TABLET_ITEM_BY_LOCATION[location_name]
        except KeyError as exc:
            raise ValueError(
                f"No native Lore Tablet reward mapping for "
                f"{location_name!r}."
            ) from exc
    if location_name in {
        "Druid's Eye",
        "Druid's Eyes",
    }:
        return "Progressive Druid's Eyes"
    if location_name in {'Claw Mirror', 'Dark Mirror'}:
        return 'Progressive Claw Mirror'
    if location_name in {'Curveclaw', 'Curvesickle'}:
        return 'Progressive Curveclaw'
    if category == 'Upgrade':
        return 'Progressive Crafting Kit'
    if get_base_randomization_category(category) == 'Resource':
        try:
            return MINOR_REWARD_BY_LOCATION[location_name]
        except KeyError as exc:
            raise ValueError(
                f"No native Resource reward mapping for {location_name!r}."
            ) from exc
    if source_location_name in ITEM_CATEGORY_BY_NAME:
        return source_location_name
    if source_location_name.startswith('Pin Purchase: '):
        native_name = source_location_name.replace(
            'Pin Purchase: ',
            '',
            1,
        )
    elif source_location_name.startswith('Map Purchase: '):
        native_name = source_location_name.replace(
            'Map Purchase: ',
            'Map: ',
            1,
        )
    elif source_location_name.startswith('Map Pickup: '):
        native_name = source_location_name.replace(
            'Map Pickup: ',
            'Map: ',
            1,
        )
    else:
        raise ValueError(
            f"No native {category} reward mapping for {location_name!r}."
        )
    return NATIVE_ITEM_NAME_TO_CURRENT.get(native_name, native_name)


def get_act_one_start_with_map_items(
    excluded_location_names: FrozenSet[str],
) -> tuple[str, ...]:
    retained_rewards = {
        get_vanilla_reward_name(location_name, "Map")
        for location_name in LOCATION_NAMES_BY_CATEGORY["Map"]
        if location_name not in excluded_location_names
    }
    return tuple(
        item_name
        for item_name in START_WITH_MAP_ITEMS
        if item_name in retained_rewards
    )


def _trim_act_one_pool_entries(
    entries: list[ItemPoolEntry],
    category_modes: Mapping[str, str],
    starting_crest_item: str | None,
    split_dash_and_sprint: bool,
    automatic_compass: bool,
    removed_option_items_by_category: Mapping[str, tuple[str, ...]],
    individual_relic_turn_ins: bool,
    donation_tool_pouch_requirements: Mapping[str, int] | None,
) -> list[ItemPoolEntry]:
    from .act1_scope import get_act_one_excluded_location_names

    major_key_mode = category_modes.get("MajorKey", "vanilla")
    boss_mode = category_modes.get("Boss", "anywhere")
    excluded_location_names = get_act_one_excluded_location_names(
        major_key_mode,
        boss_mode,
        donation_tool_pouch_requirements,
        starting_crest_item,
    ) & frozenset(location_data_table)
    for location_name in sorted(excluded_location_names):
        location_data = location_data_table[location_name]
        category = location_data.category

        if (
            category == RELIC_TURN_IN_LOCATION_CATEGORY
            and not individual_relic_turn_ins
        ):
            continue
        if location_name in WISH_REWARD_LOCATION_BY_COMPLETION:
            continue

        source_category = (
            get_minor_family_category_for_location(location_name)
            if category == "Resource"
            else category
        )
        if source_category == RELIC_TURN_IN_LOCATION_CATEGORY:
            active = individual_relic_turn_ins
        else:
            active = category_modes.get(source_category, "anywhere") != "vanilla"
        if not active:
            continue

        if source_category in {
            *OBSERVATION_LOCATION_CATEGORIES,
            RELIC_TURN_IN_LOCATION_CATEGORY,
        }:
            entry_index = next(
                (
                    index
                    for index, entry in enumerate(entries)
                    if (
                        entry.source_category == source_category
                        and _is_replaceable_filler(entry.name)
                    )
                ),
                None,
            )
        else:
            reward_name = get_vanilla_reward_name(
                location_name,
                category,
            )
            if reward_name == starting_crest_item and category == "Crest":
                reward_name = "Crest: Hunter"
            elif (
                reward_name == REGULAR_SWIFT_STEP_ITEM
                and split_dash_and_sprint
            ):
                reward_name = PROGRESSIVE_SWIFT_STEP_ITEM
            elif reward_name in removed_option_items_by_category.get(
                category,
                (),
            ):
                reward_name = OPTIONAL_START_REPLACEMENT_ITEM

            entry_index = next(
                (
                    index
                    for index, entry in enumerate(entries)
                    if (
                        entry.source_category == source_category
                        and entry.name == reward_name
                    )
                ),
                None,
            )

        if entry_index is None:
            raise ValueError(
                "Act 1 content trim could not remove an item for "
                f"{location_name!r} from the {source_category!r} pool lane."
            )
        entries.pop(entry_index)

    return entries


def _balance_act_two_skill_pool(
    entries: list[ItemPoolEntry],
    category_modes: Mapping[str, str],
    silk_soar_begone: bool = False,
) -> None:
    """Keep the pool balanced when Silk Soar's physical source is omitted."""

    mode = category_modes.get('Skill', 'anywhere')
    if mode == 'vanilla':
        return
    soar_indices = [
        index for index, entry in enumerate(entries)
        if entry.source_category == 'Skill' and entry.name == SILK_SOAR_ITEM
    ]
    if len(soar_indices) != 1:
        raise ValueError("Act 2 Skill pool must contain exactly one Silk Soar before balancing.")
    if mode == 'anywhere' and not silk_soar_begone:
        filler_index = next(
            (
                index for index, entry in enumerate(entries)
                if entry.placement_category is None
                and _is_replaceable_filler(entry.name)
            ),
            None,
        )
        if filler_index is not None:
            entries.pop(filler_index)
            return
    elif mode != 'anywhere':
        raise ValueError(f"Unknown Skill randomization mode: {mode!r}")
    entries.pop(soar_indices[0])


def get_dynamic_trap_capacity(
    category_modes: Mapping[str, str],
    split_dash_and_sprint: bool = False,
    starting_crest_item: str | None = 'Crest: Hunter',
    start_with_maps: bool = False,
    automatic_compass: bool = False,
    individual_relic_turn_ins: bool = False,
    act_two_only: bool = False,
    start_fully_mapped: bool = False,
    act_one_only: bool = False,
    retain_green_prince_key: bool = False,
    alphabet_mode: bool = False,
    act_one_donation_tool_pouch_requirements: Mapping[str, int] | None = None,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    randomize_diving_bell_key: bool = False,
    cursed_ending: bool = False,
    steel_soul: bool = False,
    minimum_memory_lockets: int = 0,
    required_goal_items: tuple[str, ...] = (),
    silk_soar_begone: bool = False,
    directional_abilities: tuple[str, ...] = (),
    soul_pool_entries: tuple[ItemPoolEntry, ...] = (),
) -> int:
    """Count filler entries that can be replaced by traps."""

    return len(_trap_eligible_indices(build_item_pool_entries(
            starting_crest_item,
            None,
            split_dash_and_sprint,
            category_modes,
            start_with_maps,
            automatic_compass,
            individual_relic_turn_ins=individual_relic_turn_ins,
            act_two_only=act_two_only,
            start_fully_mapped=start_fully_mapped,
            act_one_only=act_one_only,

            retain_green_prince_key=retain_green_prince_key,
            alphabet_mode=alphabet_mode,
            act_one_donation_tool_pouch_requirements=(
                act_one_donation_tool_pouch_requirements
            ),
            randomize_ledge_grab=randomize_ledge_grab,
            randomize_swim=randomize_swim,
            randomize_diving_bell_key=randomize_diving_bell_key,
            cursed_ending=cursed_ending,
            steel_soul=steel_soul,
            include_later_act_items=False,
            minimum_memory_lockets=minimum_memory_lockets,
            required_goal_items=required_goal_items,
            silk_soar_begone=silk_soar_begone,
            directional_abilities=directional_abilities,
            soul_pool_entries=soul_pool_entries,
        )))


def _trap_eligible_indices(entries):
    return [index for index, entry in enumerate(entries) if _is_replaceable_filler(entry.name)]


def _replace_verdania_only_key_pool_entry(
    entries: list[ItemPoolEntry],
    category_modes: Mapping[str, str],
) -> None:
    """Replace the Green Prince key outside the Act 3 content scope."""

    if category_modes.get("Key", "anywhere") == "vanilla":
        return

    entry_index = next(
        (
            index
            for index, entry in enumerate(entries)
            if (
                entry.source_category == "Key"
                and entry.name == SIMPLE_KEY_GREEN_PRINCE
            )
        ),
        None,
    )
    if entry_index is None:
        raise ValueError(
            "Lost Verdania content trim could not replace "
            f"{SIMPLE_KEY_GREEN_PRINCE!r} in the Key pool lane."
        )

    replaced_entry = entries[entry_index]
    entries[entry_index] = ItemPoolEntry(
        OPTIONAL_START_REPLACEMENT_ITEM,
        replaced_entry.source_category,
        replaced_entry.placement_category,
    )


def build_item_pool_entries(
    starting_crest_item: str | None,
    trap_counts: Mapping[str, int] | None,
    split_dash_and_sprint: bool,
    category_modes: Mapping[str, str],
    start_with_maps: bool = False,
    automatic_compass: bool = False,
    trap_randomizer: Random | None = None,
    individual_relic_turn_ins: bool = False,
    act_two_only: bool = False,
    start_fully_mapped: bool = False,
    act_one_only: bool = False,
    retain_green_prince_key: bool = False,
    alphabet_mode: bool = False,
    act_one_donation_tool_pouch_requirements: Mapping[str, int] | None = None,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    randomize_diving_bell_key: bool = False,
    cursed_ending: bool = False,
    steel_soul: bool = False,
    alphabet_nonadvancement_demand_by_placement_category: (
        Mapping[str | None, int] | None
    ) = None,
    alphabet_item_is_advancement: Callable[[str], bool] | None = None,
    include_later_act_items: bool = True,
    minimum_memory_lockets: int = 0,
    required_goal_items: tuple[str, ...] = (),
    silk_soar_begone: bool = False,
    directional_abilities: tuple[str, ...] = (),
    soul_pool_entries: tuple[ItemPoolEntry, ...] = (),
) -> tuple[ItemPoolEntry, ...]:
    """Build the unfilled-location pool for the selected category modes."""
    from .act1_scope import get_act_one_excluded_location_names

    for category, mode in category_modes.items():
        if mode == 'shuffle' and category != 'Key':
            raise ValueError(f"{category} does not support shuffle.")
    if act_one_only and act_two_only:
        raise ValueError("Act 1 and Act 2 content scopes cannot overlap.")

    if act_two_only and category_modes.get('Crest', 'anywhere') == 'anywhere':
        required_goal_items = tuple(dict.fromkeys((*required_goal_items, 'Crest: Shaman')))

    entries: list[ItemPoolEntry] = []
    act_one_excluded_location_names = (
        get_act_one_excluded_location_names(
            category_modes.get("MajorKey", "vanilla"),
            category_modes.get("Boss", "anywhere"),
            act_one_donation_tool_pouch_requirements,
            starting_crest_item,
        )
        if act_one_only
        else frozenset()
    )
    goal_excluded_location_names = (
        act_one_excluded_location_names
        if act_one_only
        else get_act_two_excluded_location_names(
            starting_crest_item, category_modes.get("Skill", "anywhere"), cursed_ending, silk_soar_begone,
            required_goal_items)
        if act_two_only
        else frozenset()
    )
    start_with_map_items = (
        get_act_one_start_with_map_items(
            act_one_excluded_location_names
        )
        if act_one_only
        else ACT_TWO_START_WITH_MAP_ITEMS
        if act_two_only
        else START_WITH_MAP_ITEMS
    )
    removed_option_items_by_category: Dict[str, tuple[str, ...]] = {
        'Map': start_with_map_items if start_with_maps else (),
        'Quill': (QUILL_ITEM,) if start_fully_mapped else (),
        'Compass': (
            (AUTOMATIC_COMPASS_ITEM,)
            if automatic_compass
            else ()
        ),
    }

    pool_categories = (
        *(
            category
            for category in PAIRED_ITEM_CATEGORIES
            if category != 'Resource'
        ),
        *MINOR_FAMILY_CATEGORIES,
    )
    for category in pool_categories:
        mode = category_modes.get(category, 'anywhere')
        if mode == 'vanilla':
            continue

        item_names = list(get_category_item_names(category))
        if category == 'Crest' and starting_crest_item is not None:
            try:
                item_names.remove(starting_crest_item)
            except ValueError as exc:
                raise ValueError(
                    f"Starting crest is not present in the Crest pool: "
                    f"{starting_crest_item!r}"
                ) from exc
        elif category == 'Skill' and split_dash_and_sprint:
            try:
                item_names.remove(REGULAR_SWIFT_STEP_ITEM)
            except ValueError as exc:
                raise ValueError(
                    'Split Swift Step requires the regular Swift Step item '
                    'in the Skill pool.'
                ) from exc
            item_names.extend((PROGRESSIVE_SWIFT_STEP_ITEM,) * 2)

        for removed_name in removed_option_items_by_category.get(
            category,
            (),
        ):
            try:
                item_names.remove(removed_name)
            except ValueError as exc:
                raise ValueError(
                    f"Option-removed item is not present in the "
                    f"{category} pool: {removed_name!r}"
                ) from exc
            item_names.append(OPTIONAL_START_REPLACEMENT_ITEM)

        placement_category = 'Key' if category == 'Key' and mode == 'shuffle' else None
        entries.extend(
            ItemPoolEntry(
                item_name,
                category,
                placement_category,
            )
            for item_name in item_names
        )

    for category in OBSERVATION_ITEM_CATEGORIES:
        mode = category_modes.get(category, 'anywhere')
        if mode == 'vanilla':
            continue
        for item_name, count in (
            OBSERVATION_FILLER_COUNTS_BY_CATEGORY[category].items()
        ):
            entries.extend(
                ItemPoolEntry(
                    item_name,
                    category,
                )
                for _copy_index in range(count)
            )

    if individual_relic_turn_ins:
        for item_name, count in RELIC_TURN_IN_FILLER_COUNTS.items():
            entries.extend(
                ItemPoolEntry(
                    item_name,
                    RELIC_TURN_IN_LOCATION_CATEGORY,
                )
                for _copy_index in range(count)
            )

    entries_before_goal_trim = tuple(entries)

    if act_one_only:
        entries = _trim_act_one_pool_entries(
            entries,
            category_modes,
            starting_crest_item,
            split_dash_and_sprint,
            automatic_compass,
            removed_option_items_by_category,
            individual_relic_turn_ins,
            act_one_donation_tool_pouch_requirements,
        )
    elif act_two_only:
        entries = list(
            trim_act_two_pool_entries(
                entries, starting_crest_item, category_modes.get("Skill", "anywhere"), cursed_ending, silk_soar_begone,
                required_goal_items)
        )

    from .game_modes import excluded_locations
    mode_exclusions = excluded_locations(steel_soul, act_one_only)
    for location in sorted(mode_exclusions - goal_excluded_location_names):
        if location in {"Shell Satchel", "Boss: Summoned Saviour"}:
            continue
        category = location_data_table[location].category
        if category_modes.get(category, "anywhere") == "vanilla":
            continue
        reward = None if category in OBSERVATION_ITEM_CATEGORIES else get_vanilla_reward_name(location, category)
        index = next((index for index, entry in enumerate(entries)
                      if entry.source_category == category
                      and (entry.name == reward if reward else _is_replaceable_filler(entry.name))), None)
        if index is None:
            raise ValueError(f"Missing {category} pool entry for mode-excluded location {location!r}.")
        entries.pop(index)
    if steel_soul:
        additions = [("Shell Satchel", "Tool")] if "Dead Bug's Purse" not in goal_excluded_location_names else []
        if not act_one_only:
            additions += [("Rosaries (60)", "Boss")]
        for item, category in additions:
            mode = category_modes.get(category, "anywhere")
            if mode != "vanilla":
                entries.append(ItemPoolEntry(item, category))
    goal_excluded_location_names |= mode_exclusions
    if steel_soul and category_modes.get("Quest", "anywhere") != "vanilla" and "Wish: A Vassal Lost" not in goal_excluded_location_names:
        index = next(index for index, entry in enumerate(entries)
                     if entry.source_category == "Quest" and _is_replaceable_filler(entry.name))
        entry = entries[index]
        entries[index] = ItemPoolEntry("Growstone", entry.source_category, entry.placement_category)

    if category_modes.get("Boss", "vanilla") != "vanilla":
        credits = [item for location, item in BOSS_CREDIT_BY_LOCATION.items()
                   if location not in goal_excluded_location_names]
        indices = [index for index, entry in enumerate(entries) if entry.source_category == "Boss"]
        if len(indices) < len(credits):
            raise ValueError("The boss pool has fewer slots than eligible credits.")
        for index, credit in zip(indices, credits):
            entry = entries[index]
            entries[index] = ItemPoolEntry(credit, entry.source_category, entry.placement_category)

    if category_modes.get("Journal", "vanilla") != "vanilla":
        from .boss_journal import excluded_locations
        journal_excluded = excluded_locations(goal_excluded_location_names, 1 if act_one_only else 2 if act_two_only else 3)
        entries.extend(ItemPoolEntry(item, "Journal")
                       for location, item in JOURNAL_ITEMS.items() if location not in journal_excluded)

    # Act 2 may keep the otherwise Verdania-only key as an optional bingo
    # collectible without restoring any Verdania locations or requirements.
    if (
        act_two_only
        and not act_one_only
        and not retain_green_prince_key
    ):
        _replace_verdania_only_key_pool_entry(entries, category_modes)

    if split_dash_and_sprint:
        unrestricted_filler_indices = tuple(
            index
            for index, entry in enumerate(entries)
            if (
                entry.placement_category is None
                and _is_replaceable_filler(entry.name)
            )
        )
        filler_index = unrestricted_filler_indices[0] if unrestricted_filler_indices else None
        if filler_index is None:
            raise OptionError(
                "split_dash_and_sprint needs one unrestricted filler item "
                "from an 'anywhere' category to balance its second "
                "Progressive Swift Step."
            )
        entries.pop(filler_index)

    if act_two_only:
        _balance_act_two_skill_pool(entries, category_modes, silk_soar_begone)
    elif silk_soar_begone and not act_one_only:
        entries = [entry for entry in entries if entry.name != SILK_SOAR_ITEM]

    missing_lockets = max(
        0, minimum_memory_lockets - sum(entry.name == 'Memory Locket' for entry in entries)
    )
    if (
        category_modes.get('Crest', 'anywhere') == 'anywhere'
        and starting_crest_item in goal_excluded_location_names
    ):
        required_goal_items = (*required_goal_items, 'Crest: Hunter')
    missing_goal_items = [name for name in required_goal_items
                          if name != starting_crest_item and not any(entry.name == name for entry in entries)]
    needed_items = ['Memory Locket'] * missing_lockets + missing_goal_items
    if needed_items:
        is_advancement = alphabet_item_is_advancement or (
            lambda name: bool(item_data_table[name].classification & ItemClassification.progression)
        )
        eligible_indices = [
            index for index, entry in enumerate(entries)
            if entry.placement_category is None
            and _is_replaceable_filler(entry.name)
            and not is_advancement(entry.name)
        ]
        nonadvancement_count = sum(
            not is_advancement(entry.name)
            for entry in entries if entry.placement_category is None
        )
        reserved = (alphabet_nonadvancement_demand_by_placement_category or {}).get(None, 0)
        capacity = min(len(eligible_indices), max(0, nonadvancement_count - reserved))
        if len(needed_items) > capacity:
            raise OptionError(
                f"The enabled checks need {len(needed_items)} more items "
                "in the pool, but there is not enough unrestricted filler. "
                "Set more categories to anywhere or disable some checks."
            )
        for index, name in zip(eligible_indices, needed_items):
            entry = entries[index]
            entries[index] = ItemPoolEntry(name, entry.source_category, None)

    innate_ability_items = (
        *((LEDGE_GRAB_ITEM,) if randomize_ledge_grab else ()),
        *((SWIM_ITEM,) if randomize_swim else ()),
        *(("Diving Bell Key",) if randomize_diving_bell_key else ()),
    )
    if not steel_soul:
        split_sources = {clean_item_display_name(entry.name) for entry in entries} | set(innate_ability_items)
        split_slots = sum(ability == 'Dash' or ability in split_sources for ability in directional_abilities)
        reserved_filler = len(innate_ability_items) + len(soul_pool_entries) + split_slots
        if alphabet_mode:
            reserved_filler += len(ALPHABET_ITEM_NAMES)
        reserved_anywhere_filler = len(innate_ability_items) + len(soul_pool_entries) if soul_pool_entries else 0
        add_pool_only_useful_items(entries, reserved_filler, reserved_anywhere_filler)

    replace_filler_with_innate_ability_items(entries, innate_ability_items, trap_randomizer)

    if soul_pool_entries:
        indices = [index for index, entry in enumerate(entries)
                   if entry.placement_category is None
                   and item_data_table[entry.name].classification == ItemClassification.filler
                   and entry.source_category not in {'Memento', 'MemoryLocket', 'Journal'}]
        if len(indices) < len(soul_pool_entries):
            raise OptionError(
                f"Boss and NPC Souls need {len(soul_pool_entries)} anywhere filler slots; "
                f"only {len(indices)} are available. Enable more anywhere cache or resource checks."
            )
        rng = trap_randomizer or Random(0)
        for soul, index in zip(soul_pool_entries, rng.sample(indices, len(soul_pool_entries))):
            entries[index] = soul

    if alphabet_mode:
        max_alphabet_replacements_by_category = None
        if (
            alphabet_nonadvancement_demand_by_placement_category
            is not None
        ):
            if alphabet_item_is_advancement is None:
                raise ValueError(
                    "Alphabet placement capacity needs an item "
                    "classification callback."
                )
            eligible_filler_count_by_category: Dict[
                str | None,
                int,
            ] = {}
            nonadvancement_count_by_category: Dict[
                str | None,
                int,
            ] = {}
            advancement_by_name = {
                entry.name: alphabet_item_is_advancement(entry.name)
                for entry in entries
            }
            for entry in entries:
                category = entry.placement_category
                if _is_replaceable_filler(entry.name):
                    eligible_filler_count_by_category[category] = (
                        eligible_filler_count_by_category.get(category, 0)
                        + 1
                    )
                if not advancement_by_name[entry.name]:
                    nonadvancement_count_by_category[category] = (
                        nonadvancement_count_by_category.get(category, 0)
                        + 1
                    )
            max_alphabet_replacements_by_category = {
                category: min(
                    eligible_count,
                    max(
                        0,
                        nonadvancement_count_by_category.get(category, 0)
                        - (
                            alphabet_nonadvancement_demand_by_placement_category
                            .get(category, 0)
                        ),
                    ),
                )
                for category, eligible_count
                in eligible_filler_count_by_category.items()
            }
        replace_filler_with_alphabet_items(
            entries,
            _is_replaceable_filler,
            trap_randomizer,
            max_alphabet_replacements_by_category,
            alphabet_item_is_advancement,
        )

    configured_traps = {
        trap_name: int((trap_counts or {}).get(trap_name, 0))
        for trap_name in TRAP_ITEM_NAMES
    }
    unknown_traps = set(trap_counts or {}) - set(TRAP_ITEM_NAMES)
    if unknown_traps:
        raise ValueError(
            f"Unknown trap item names: {sorted(unknown_traps)!r}"
        )
    if any(count < 0 for count in configured_traps.values()):
        raise ValueError("Trap counts cannot be negative.")

    trap_names = tuple(
        trap_name
        for trap_name in TRAP_ITEM_NAMES
        for _copy_index in range(configured_traps[trap_name])
    )
    eligible_indices = _trap_eligible_indices(entries)
    if trap_randomizer is not None:
        # Shuffle the complete filler pool so each entry has the configured
        # trap chance.
        trap_randomizer.shuffle(eligible_indices)
    trap_capacity = len(eligible_indices)
    if len(trap_names) > trap_capacity:
        raise ValueError(
            f"At most {trap_capacity} traps can replace filler items in the "
            f"configured random pool but received {len(trap_names)}."
        )

    for entry_index, trap_name in zip(eligible_indices, trap_names):
        replaced_entry = entries[entry_index]
        entries[entry_index] = ItemPoolEntry(
            trap_name,
            replaced_entry.source_category,
            replaced_entry.placement_category,
        )
    if include_later_act_items and (act_one_only or act_two_only):
        from collections import Counter
        remaining = Counter((entry.name, entry.source_category) for entry in entries)
        required_retained = set(missing_goal_items)
        retained = []
        for entry in entries_before_goal_trim:
            key = (entry.name, entry.source_category)
            if remaining[key]:
                remaining[key] -= 1
            elif entry.name in required_retained:
                required_retained.remove(entry.name)
            elif (
                category_modes.get(entry.source_category, 'anywhere') == 'anywhere'
                and not (silk_soar_begone and entry.name == SILK_SOAR_ITEM)
                and entry.source_category not in {'OldHeart', 'Everbloom', 'Memento'}
                and not (act_one_only and entry.source_category in {'Soul', 'TwistedBud'})
                and not (act_one_only and (
                    'Cylinder' in entry.name
                    or entry.name in {'Bellway: Grand Bellway', 'Ventrica: Grand Bellway'}
                ))
                and entry.source_category not in OBSERVATION_ITEM_CATEGORIES
                and entry.source_category != RELIC_TURN_IN_LOCATION_CATEGORY
                and not entry.source_category.startswith('Resource')
                and not entry.name.startswith(('Rosaries (', 'Shell Shards ('))
            ):
                retained.append(entry)
        filler_indices = [
            index for index, entry in enumerate(entries)
            if entry.placement_category is None
            and entry.name.startswith(('Rosaries (', 'Shell Shards ('))
        ]
        rng = trap_randomizer or Random(0)
        rng.shuffle(retained)
        is_advancement = alphabet_item_is_advancement or (
            lambda name: bool(item_data_table[name].classification & ItemClassification.progression)
        )
        nonadvancement_count = sum(
            not is_advancement(entry.name)
            for entry in entries if entry.placement_category is None
        )
        reserved = (alphabet_nonadvancement_demand_by_placement_category or {}).get(None, 0)
        advancement_capacity = max(0, nonadvancement_count - reserved)
        minimum_filler = (len(filler_indices) + 3) // 4
        later_act_capacity = len(filler_indices) - minimum_filler
        split_sources = {clean_item_display_name(entry.name) for entry in entries}
        split_capacity = sum(_is_replaceable_filler(entry.name) for entry in entries)
        selected = []
        for entry in retained:
            if len(selected) >= later_act_capacity:
                break
            sources = split_sources | {clean_item_display_name(entry.name)}
            split_slots = sum(ability == 'Dash' or ability in sources for ability in directional_abilities)
            if len(selected) + 1 + split_slots > split_capacity:
                continue
            if is_advancement(entry.name):
                if advancement_capacity == 0:
                    continue
                advancement_capacity -= 1
            selected.append(entry)
            split_sources = sources
        for index, entry in zip(filler_indices, selected):
            entries[index] = entry

    split_pool(entries, directional_abilities, ItemPoolEntry, replace_filler_with_innate_ability_items)
    return tuple(entries)


def get_configured_item_pool_size(
    starting_crest_item: str | None,
    trap_counts: Mapping[str, int] | None,
    split_dash_and_sprint: bool,
    category_modes: Mapping[str, str],
    start_with_maps: bool = False,
    automatic_compass: bool = False,
    individual_relic_turn_ins: bool = False,
    act_two_only: bool = False,
    start_fully_mapped: bool = False,
    act_one_only: bool = False,
    retain_green_prince_key: bool = False,
    alphabet_mode: bool = False,
    act_one_donation_tool_pouch_requirements: Mapping[str, int] | None = None,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    randomize_diving_bell_key: bool = False,
    cursed_ending: bool = False,
    steel_soul: bool = False,
) -> int:
    return len(
        build_item_pool_entries(
            starting_crest_item,
            trap_counts,
            split_dash_and_sprint,
            category_modes,
            start_with_maps,
            automatic_compass,
            individual_relic_turn_ins=individual_relic_turn_ins,
            act_two_only=act_two_only,
            start_fully_mapped=start_fully_mapped,
            act_one_only=act_one_only,

            retain_green_prince_key=retain_green_prince_key,
            alphabet_mode=alphabet_mode,
            act_one_donation_tool_pouch_requirements=(
                act_one_donation_tool_pouch_requirements
            ),
            randomize_ledge_grab=randomize_ledge_grab,
            randomize_swim=randomize_swim,
            randomize_diving_bell_key=randomize_diving_bell_key,
            cursed_ending=cursed_ending,
            steel_soul=steel_soul,
        )
    )


def _get_adjusted_pool_counts(
    trap_counts: Mapping[str, int] | None = None,
    split_dash_and_sprint: bool = False,
    wish_sanity: bool = True,
    randomize_needle_upgrades: bool = False,
    randomize_minor_pickups: bool = False,
    randomize_pale_oils: bool = False,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    randomize_diving_bell_key: bool = False,
) -> Dict[str, int]:
    configured_traps = {
        trap_name: int((trap_counts or {}).get(trap_name, 0))
        for trap_name in TRAP_ITEM_NAMES
    }
    unknown_traps = set(trap_counts or {}) - set(TRAP_ITEM_NAMES)
    if unknown_traps:
        raise ValueError(
            f"Unknown trap item names: {sorted(unknown_traps)!r}"
        )
    if any(count < 0 for count in configured_traps.values()):
        raise ValueError("Trap counts cannot be negative.")

    counts = {
        name: (
            (
                MINOR_REWARD_COUNTS.get(name, 0)
            )
            if category == 'Resource' and randomize_minor_pickups
            else (
                0
                if (
                    category in {'Resource', 'BossSoul', 'NpcSoul'}
                    or name in TRAP_ITEM_NAMES
                    or name in CONDITIONAL_POOL_ITEM_NAMES
                    or name in POOL_ONLY_USEFUL_ITEM_NAMES
                )
                else 1
            )
        )
        for name, category in ITEM_TABLE_SOURCE
    }
    counts.update(ITEM_POOL_COUNTS)
    counts['Rosaries (60)'] -= 20
    counts['Shell Shards (80)'] -= len(BOSS_CREDIT_BY_LOCATION) - 20
    counts['Shell Shards (80)'] -= len(POOL_ONLY_USEFUL_ITEM_NAMES)
    if wish_sanity:
        for item_name, count in QUEST_FILLER_COUNTS.items():
            counts[item_name] += count
    counts[REGULAR_SWIFT_STEP_ITEM] = int(
        not split_dash_and_sprint
    )
    counts[PROGRESSIVE_SWIFT_STEP_ITEM] = (
        2 if split_dash_and_sprint else 0
    )
    for item_name, count in NEEDLE_UPGRADE_POOL_COUNTS.items():
        counts[item_name] = count if randomize_needle_upgrades else 0
    for item_name, count in PALE_OIL_POOL_COUNTS.items():
        counts[item_name] = count if randomize_pale_oils else 0
    counts['Rosaries (60)'] -= int(split_dash_and_sprint)

    innate_ability_items = (
        *((LEDGE_GRAB_ITEM,) if randomize_ledge_grab else ()),
        *((SWIM_ITEM,) if randomize_swim else ()),
        *(("Diving Bell Key",) if randomize_diving_bell_key else ()),
    )
    for item_name in innate_ability_items:
        counts[item_name] = 1
    remaining_replacements = len(innate_ability_items)
    for item_name, _category in ITEM_TABLE_SOURCE:
        if (
            remaining_replacements == 0
            or not _is_replaceable_filler(item_name)
        ):
            continue
        replaced_count = min(counts[item_name], remaining_replacements)
        counts[item_name] -= replaced_count
        remaining_replacements -= replaced_count
    if remaining_replacements:
        raise OptionError(
            "Optional item randomization needs more filler rewards in the "
            "configured random pool."
        )

    total_traps = sum(configured_traps.values())
    trap_capacity = sum(
        count
        for item_name, count in counts.items()
        if _is_replaceable_filler(item_name)
    )
    if total_traps > trap_capacity:
        raise ValueError(
            f"At most {trap_capacity} traps can replace filler items in this "
            f"pool but received {total_traps}."
        )

    remaining_traps = total_traps
    for item_name, _category in ITEM_TABLE_SOURCE:
        if (
            remaining_traps == 0
            or not _is_replaceable_filler(item_name)
        ):
            continue
        replaced_count = min(counts[item_name], remaining_traps)
        counts[item_name] -= replaced_count
        remaining_traps -= replaced_count

    counts.update(configured_traps)
    return counts


def iter_item_pool_names(
    starting_crest_item: str | None = None,
    trap_counts: Mapping[str, int] | None = None,
    split_dash_and_sprint: bool = False,
    wish_sanity: bool = True,
    randomize_needle_upgrades: bool = False,
    randomize_pale_oils: bool = False,
    randomize_minor_pickups: bool = False,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    randomize_diving_bell_key: bool = False,
):
    pool_counts = _get_adjusted_pool_counts(
        trap_counts=trap_counts,
        split_dash_and_sprint=split_dash_and_sprint,
        wish_sanity=wish_sanity,
        randomize_needle_upgrades=randomize_needle_upgrades,
        randomize_minor_pickups=randomize_minor_pickups,
        randomize_pale_oils=randomize_pale_oils,
        randomize_ledge_grab=randomize_ledge_grab,
        randomize_swim=randomize_swim,
        randomize_diving_bell_key=randomize_diving_bell_key,
    )
    removed_starting_crest = False
    for name, _category in ITEM_TABLE_SOURCE:
        if _category == 'Resource':
            default_count = (
                (
                    MINOR_REWARD_COUNTS.get(name, 0)
                )
                if randomize_minor_pickups
                else 0
            )
        else:
            default_count = (
                0
                if (
                    name in TRAP_ITEM_NAMES
                    or name in CONDITIONAL_POOL_ITEM_NAMES
                    or name in POOL_ONLY_USEFUL_ITEM_NAMES
                )
                else 1
            )
        for _copy_index in range(pool_counts.get(name, default_count)):
            if name == starting_crest_item and not removed_starting_crest:
                removed_starting_crest = True
                continue
            yield name

    if starting_crest_item is not None:
        if not removed_starting_crest:
            raise ValueError(
                f"Starting crest is not present in the item pool: "
                f"{starting_crest_item!r}"
            )


def get_item_pool_size(
    trap_counts: Mapping[str, int] | None = None,
    split_dash_and_sprint: bool = False,
    wish_sanity: bool = True,
    randomize_needle_upgrades: bool = False,
    randomize_pale_oils: bool = False,
    randomize_minor_pickups: bool = False,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    randomize_diving_bell_key: bool = False,
) -> int:
    return sum(
        1
        for _name in iter_item_pool_names(
            starting_crest_item=None,
            trap_counts=trap_counts,
            split_dash_and_sprint=split_dash_and_sprint,
            wish_sanity=wish_sanity,
            randomize_needle_upgrades=randomize_needle_upgrades,
            randomize_minor_pickups=randomize_minor_pickups,
            randomize_pale_oils=randomize_pale_oils,
            randomize_ledge_grab=randomize_ledge_grab,
            randomize_swim=randomize_swim,
            randomize_diving_bell_key=randomize_diving_bell_key,
        )
    )


class SilksongItem(Item):
    game = "Hollow Knight: Silksong"

    def __init__(
        self,
        name: str,
        classification: ItemClassification,
        code: int,
        player: int,
        placement_category: str | None = None,
    ) -> None:
        super().__init__(name, classification, code, player)
        self.silksong_placement_category = placement_category
