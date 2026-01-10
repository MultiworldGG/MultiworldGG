# OoT Apworld Update Plan: 7.1.0 to 8.0.0

## Overview

This document provides a detailed, actionable plan for updating the OoT apworld from version 7.1.0 to 8.0.0. The update is broken into phases with specific tasks, file changes, and dependencies.

---

## Quick Start Checklist

Before beginning, ensure you have:

- [ ] Clone of upstream OoT-Randomizer at v8.0 tag: `git clone --branch v8.0 https://github.com/OoTRandomizer/OoT-Randomizer.git`
- [ ] Python 3.9+ installed
- [ ] Diff tool (VS Code, Beyond Compare, or similar)
- [ ] Test ROM for verification

**First 5 Steps:**
1. Download `rom_patch.txt` and `symbols.json` from 8.0 release
2. Convert `symbols.json` format and add AP symbols
3. Copy new item model files (`data/items/*.zobj`)
4. Update `Items.py` with new item definitions
5. Update `LocationList.py` with new locations

---

## Prerequisites & External Resources

### Files to Download from v8.0 Release

**From GitHub:** `https://github.com/OoTRandomizer/OoT-Randomizer/tree/v8.0`

| File | Destination | Notes |
|------|-------------|-------|
| `data/generated/rom_patch.txt` | `worlds/oot/data/generated/` | Replace existing |
| `data/generated/symbols.json` | Convert first, then replace | See conversion script |
| `data/items/*.zobj` | `worlds/oot/data/items/` | New directory |
| `data/World/*.json` | Compare & merge | Logic updates |

### Upstream Reference Files

Keep these open for reference during development:

| Upstream File | Purpose |
|---------------|---------|
| `ItemList.py` | New item definitions, GetItemId values |
| `LocationList.py` | New location definitions |
| `SettingsList.py` | New settings (translate to Options.py) |
| `Patches.py` | ROM patching code to port |
| `World.py` | Silver rupee puzzle logic |
| `EntranceShuffle.py` | New entrance definitions |

---

## Phase 0: Preparation (Do This First)

### 0.1 Set Up Development Environment

```bash
# Clone upstream at v8.0
cd G:\source
git clone --branch v8.0 https://github.com/OoTRandomizer/OoT-Randomizer.git OoT-Randomizer-8.0

# Create a working branch in MultiworldGG
cd G:\source\MultiworldGG
git checkout -b oot-update-8.0
```

### 0.2 Generate File Diffs

```bash
# Compare key files to understand changes
diff -u worlds/oot/Items.py ../OoT-Randomizer-8.0/ItemList.py > diffs/items.diff
diff -u worlds/oot/LocationList.py ../OoT-Randomizer-8.0/LocationList.py > diffs/locations.diff
diff -u worlds/oot/Options.py ../OoT-Randomizer-8.0/SettingsList.py > diffs/settings.diff
```

### 0.3 Update ROM Patching Files

**Step 1: Copy rom_patch.txt**
```bash
cp ../OoT-Randomizer-8.0/data/generated/rom_patch.txt worlds/oot/data/generated/
```

**Step 2: Convert and update symbols.json**
```python
# Run this script: scripts/convert_symbols.py
import json

with open('../OoT-Randomizer-8.0/data/generated/symbols.json') as f:
    upstream = json.load(f)

# Convert format
apworld = {name: data['address'] for name, data in upstream.items()}

# Add AP-specific symbols
apworld['DEATH_LINK'] = '0348002B'
apworld['AP_PLAYER_NAME'] = '03480839'

with open('worlds/oot/data/generated/symbols.json', 'w') as f:
    json.dump(apworld, f, indent=4, sort_keys=True)
```

**Step 3: Copy new item models**
```bash
mkdir -p worlds/oot/data/items
cp ../OoT-Randomizer-8.0/data/items/*.zobj worlds/oot/data/items/
```

---

## Phase 1: Foundation & Infrastructure

### 1.1 Python Version Update
**Priority: HIGH | Complexity: LOW**

- [ ] Update minimum Python version to 3.9+ (8.0 drops 3.6/3.7, 9.0 drops 3.8)
- [ ] Update type hints to use native generics instead of `typing` module where applicable
- [ ] Add `from __future__ import annotations` where needed

**Files to modify:**
- `__init__.py`
- All `.py` files with type hints

---

### 1.2 Item ID Infrastructure
**Priority: HIGH | Complexity: MEDIUM**

New item types require new IDs. The apworld uses a mapping system.

**Tasks:**
- [ ] Review `Items.py` and update `item_table` with new items
- [ ] Add new `GetItemId` enum values (reference upstream `ItemList.py`)
- [ ] Update `oot_data_to_ap_id()` function for new item types

**New Item Categories to Add:**

| Category | Count | Example Items |
|----------|-------|---------------|
| Silver Rupees | 22 | `Silver Rupee (Dodongos Cavern Staircase)` |
| Silver Rupee Pouches | 22 | `Silver Rupee Pouch (Shadow Temple Huge Pit)` |
| Ocarina Notes | 5 | `Ocarina A Button`, `Ocarina C Down` |
| TCG Keys | 6 | `Small Key (Treasure Chest Game)` |
| Bombchu Bag | 1 | `Bombchu Bag` |
| Loach Reward | 1 | `Hyrule Loach` |
| **Total** | **~57** | |

**Step-by-Step: Adding Silver Rupees to Items.py**

1. **Find the item_table in Items.py** (~line 50)

2. **Add new item type classification:**
```python
# In item_table, add silver rupee entries:
'Silver Rupee (Dodongos Cavern Staircase)': ItemData(
    classification=ItemClassification.progression_skip_balancing,
    type='SilverRupee',
    index=0x00D4,  # Get from upstream ItemList.py GI_ values
),
# ... repeat for all 22 puzzles
```

3. **Add silver rupee pouches:**
```python
'Silver Rupee Pouch (Dodongos Cavern Staircase)': ItemData(
    classification=ItemClassification.progression,
    type='SilverRupee',
    index=0x00F0,  # Pouch GI values
),
```

4. **Reference upstream `ItemList.py` lines 496-540** for exact GI values:
```python
# Upstream format:
'Silver Rupee (Dodongos Cavern Staircase)': ('SilverRupee', True, GetItemId.GI_SILVER_RUPEE_DODONGOS_CAVERN_STAIRCASE, {'progressive': 5}),
```

**Step-by-Step: Adding Ocarina Notes to Items.py**

```python
# Add to item_table:
'Ocarina A Button': ItemData(
    classification=ItemClassification.progression,
    type='OcarinaNote',
    index=0x00XX,  # Get from upstream
),
'Ocarina C Up': ItemData(...),
'Ocarina C Down': ItemData(...),
'Ocarina C Left': ItemData(...),
'Ocarina C Right': ItemData(...),
```

**Files to modify:**
- `Items.py` (major changes - add ~60 new items)
- `data/generated/symbols.json` (already updated in Phase 0)

---

### 1.3 Location Infrastructure
**Priority: HIGH | Complexity: MEDIUM**

**Tasks:**
- [ ] Add Silver Rupee locations (~100+ locations)
- [ ] Add Thieves' Hideout interior locations
- [ ] Add TCG locations
- [ ] Add Loach reward location
- [ ] Update location ID mappings

**New Location Counts by Type:**

| Location Type | Vanilla | MQ | Total | Notes |
|---------------|---------|-----|-------|-------|
| Silver Rupees | ~60 | ~40 | ~100 | 5 per puzzle, 22 puzzles |
| TCG Chests | 6 | - | 6 | Keys for chest game |
| Loach Reward | 1 | - | 1 | Fishing pond |
| Hideout Interior | - | - | 0 | Just entrances, no new checks |

**Step-by-Step: Adding Silver Rupee Locations**

1. **Open upstream `LocationList.py`** and search for `SilverRupee`

2. **Find the location format** (upstream lines ~1170-2300):
```python
# Upstream format:
("Dodongos Cavern MQ Staircase Silver Rupee Beamos",
    ("SilverRupee", 0x1, (2,0,11), None,
     'Silver Rupee (Dodongos Cavern Staircase)',
     ("Dodongo's Cavern MQ", "Master Quest", "Silver Rupees",))),
```

3. **Translate to apworld format** in `LocationList.py`:
```python
# Apworld format - add to location_table:
("Dodongos Cavern MQ Staircase Silver Rupee Beamos", {
    'type': 'SilverRupee',
    'scene': 0x01,
    'default': 'Silver Rupee (Dodongos Cavern Staircase)',
    'filter_tags': ("Dodongo's Cavern MQ", "Master Quest", "Silver Rupees"),
}),
```

4. **Add location type to `Location.py`**:
```python
# In the location_type_to_classification function or similar:
'SilverRupee': LocationClassification.always,  # Or appropriate classification
```

**Silver Rupee Puzzle List (22 puzzles):**
```
Dodongos Cavern Staircase (MQ only, 5 rupees)
Ice Cavern Spinning Scythe (5)
Ice Cavern Push Block (5)
Bottom of the Well Basement (5)
Shadow Temple Scythe Shortcut (5)
Shadow Temple Invisible Blades (10)
Shadow Temple Huge Pit (5)
Shadow Temple Invisible Spikes (10)
Gerudo Training Ground Slopes (5)
Gerudo Training Ground Lava (6)
Gerudo Training Ground Water (5)
Spirit Temple Child Early Torches (5)
Spirit Temple Adult Boulders (5)
Spirit Temple Lobby and Lower Adult (5)
Spirit Temple Sun Block (5)
Spirit Temple Adult Climb (5)
Ganons Castle Spirit Trial (5)
Ganons Castle Light Trial (5)
Ganons Castle Fire Trial (5)
Ganons Castle Shadow Trial (5)
Ganons Castle Water Trial (5)
Ganons Castle Forest Trial (5)
```

**Step-by-Step: Adding TCG Locations**

```python
# Add to LocationList.py:
("Treasure Chest Game Room 1 Chest", {
    'type': 'TCGSmallKey',
    'scene': 0x10,  # Market area
    'default': 'Small Key (Treasure Chest Game)',
}),
# Repeat for rooms 1-6
```

**Files to modify:**
- `LocationList.py` (add ~150 new locations)
- `Location.py` (add new location types: `SilverRupee`, `TCGSmallKey`)

---

## Phase 2: New Settings/Options

### 2.1 Silver Rupee Settings
**Priority: HIGH | Complexity: HIGH**

This is the largest new feature in 8.0.

**New Options to implement:**
```python
class ShuffleSilverRupees(Choice):
    """Controls silver rupee shuffle behavior"""
    option_vanilla = 0      # Silver rupees stay in place
    option_dungeon = 1      # Silver rupees shuffle within dungeon
    option_overworld = 2    # Silver rupees shuffle to overworld
    option_any_dungeon = 3  # Silver rupees shuffle to any dungeon
    option_regional = 4     # Silver rupees shuffle regionally
    option_keysanity = 5    # Silver rupees can be anywhere
    option_remove = 6       # Silver rupees removed, puzzles pre-solved

class SilverRupeePouches(Choice):
    """Controls silver rupee pouch behavior"""
    option_off = 0
    option_random = 1
    option_all = 2
    option_specific = 3

class SilverRupeePouchesMode(Choice):
    """How to select which puzzles get pouches"""
    option_count = 0
    option_random_puzzles = 1
```

**Files to modify:**
- `Options.py` (add 3-4 new option classes)
- `__init__.py` (handle silver rupee logic, item pool, pre-fill)

---

### 2.2 Treasure Chest Game Keys
**Priority: MEDIUM | Complexity: MEDIUM**

**New Options:**
```python
class TreasureChestGameKeys(Choice):
    """Shuffle TCG keys outside the minigame"""
    option_vanilla = 0
    option_shuffle = 1
    option_remove = 2
```

**Files to modify:**
- `Options.py`
- `LocationList.py` (add TCG chest locations)
- `ItemPool.py` (add TCG keys to pool)

---

### 2.3 Trade Sequence Rework
**Priority: MEDIUM | Complexity: HIGH**

Major rework allowing multiple trade items per age.

**New Options:**
```python
class ShuffleChildTrade(OptionSet):
    """Which child trade items to shuffle"""
    valid_keys = {"Weird Egg", "Chicken", "Zeldas Letter", "Keaton Mask",
                  "Skull Mask", "Spooky Mask", "Bunny Hood", "Mask of Truth",
                  "Goron Mask", "Zora Mask", "Gerudo Mask"}

class AdultTradeStart(OptionSet):
    """Which adult trade items to start with"""
    valid_keys = {"Pocket Egg", "Pocket Cucco", "Cojiro", "Odd Mushroom",
                  "Odd Potion", "Poachers Saw", "Broken Sword", "Prescription",
                  "Eyeball Frog", "Eyedrops", "Claim Check"}

class ShuffleAllAdultTrade(Toggle):
    """Shuffle all adult trade items"""
```

**Files to modify:**
- `Options.py` (rework trade options)
- `ItemPool.py` (handle multiple trade items)
- `__init__.py` (trade logic changes)
- `data/World/Overworld.json` (trade location logic)

---

### 2.4 Other New Settings
**Priority: LOW-MEDIUM | Complexity: LOW-MEDIUM**

| Setting | Complexity | Notes |
|---------|------------|-------|
| `key_rings_give_bosskeys` | LOW | Simple item pool change |
| `shuffle_gerudo_valley_river_exit` | MEDIUM | New entrance type |
| `bombchu_bag_and_drops` | MEDIUM | Item pool + logic changes |
| `shuffle_loach_reward` | LOW | Single new location |
| `shuffle_individual_ocarina_notes` | HIGH | New items + logic changes |
| `shuffle_hideout_entrances` | HIGH | New entrance pool |
| `ruto_already_at_f1` | LOW | ROM patch only |
| `key_appearance_matches_dungeon` | LOW | Cosmetic only |
| `maintain_mask_equips` | LOW | ROM patch only |

**Files to modify:**
- `Options.py` (add all settings)
- `ItemPool.py` (bombchu bag, ocarina notes)
- `EntranceShuffle.py` (river exit, hideout)

---

## Phase 3: Logic Updates

### 3.1 World JSON Updates
**Priority: HIGH | Complexity: MEDIUM**

The world JSON files contain all the logic rules.

**Tasks:**
- [ ] Diff upstream `data/World/*.json` with apworld versions
- [ ] Add new regions for hideout rooms
- [ ] Add silver rupee puzzle locations
- [ ] Update logic for new settings
- [ ] Add logic for Farore's Wind dungeon warping

**Files to modify (all need updates):**
```
data/World/Overworld.json              (+400 lines)
data/World/Bottom of the Well.json
data/World/Bottom of the Well MQ.json
data/World/Shadow Temple.json
data/World/Shadow Temple MQ.json
data/World/Spirit Temple.json
data/World/Spirit Temple MQ.json
data/World/Gerudo Training Ground.json
data/World/Gerudo Training Ground MQ.json
data/World/Ganons Castle.json
data/World/Ganons Castle MQ.json
data/World/Ice Cavern.json
data/World/Ice Cavern MQ.json
data/World/Dodongos Cavern MQ.json     (silver rupees only in MQ)
```

---

### 3.2 Logic Helpers Update
**Priority: MEDIUM | Complexity: LOW**

- [ ] Update `data/LogicHelpers.json` with new helper functions
- [ ] Add silver rupee counting helpers
- [ ] Add ocarina note checking helpers

---

### 3.3 Rule Parser Updates
**Priority: MEDIUM | Complexity: MEDIUM**

- [ ] Update `RuleParser.py` for new rule syntax
- [ ] Add silver rupee counting functions
- [ ] Add ocarina note check functions

---

## Phase 4: Entrance Shuffle Expansion

### 4.1 Gerudo Valley River Exit
**Priority: MEDIUM | Complexity: MEDIUM**

**Tasks:**
- [ ] Add new entrance type to `EntranceShuffle.py`
- [ ] Add entrance data to `entrance_shuffle_table`
- [ ] Update `Options.py` with setting

**New entrance:**
```python
('OwlDrop',  ('GV Lower Stream -> Lake Hylia', { 'index': 0x0219 })),
```

---

### 4.2 Thieves' Hideout Entrances
**Priority: MEDIUM | Complexity: HIGH**

This adds 6 new shufflable interior entrances.

**New entrances to add:**
```python
('Hideout', ('GF Entrances Behind Crates -> Hideout 1 Torch Jail', ...)),
('Hideout', ('GF Entrances Behind Crates -> Hideout Kitchen Hallway', ...)),
('Hideout', ('GF Roof Entrance Cluster -> Hideout 4 Torches Jail', ...)),
('Hideout', ('GF Roof Entrance Cluster -> Hideout 2 Torches Jail', ...)),
('Hideout', ('GF Roof Entrance Cluster -> Hideout Kitchen Front', ...)),
('Hideout', ('GF Break Room Entrance -> Hideout Break Room', ...)),
```

**Files to modify:**
- `EntranceShuffle.py` (add entrance definitions)
- `data/World/Overworld.json` (add hideout regions)
- `Options.py` (add `shuffle_hideout_entrances`)

---

## Phase 5: Hints System Updates

### 5.1 New Hint Types
**Priority: MEDIUM | Complexity: MEDIUM**

**New hint features:**
- [ ] Important Checks hint type (major items per region)
- [ ] Frogs Ocarina Game misc hint
- [ ] Merchant hints (Bean Salesman, Medigorin, etc.)
- [ ] King Zora dual hint
- [ ] Owls in warp songs misc hint
- [ ] `remove_stones` and `priority_stones` distribution options

**Files to modify:**
- `Hints.py` (add new hint types)
- `HintList.py` (add new hint texts)
- `data/Hints/*.json` (update distributions)

---

### 5.2 Hint Distribution Updates
**Priority: LOW | Complexity: LOW**

- [ ] Add `MW Season 3 (WotH)` distribution
- [ ] Add `Chaos!!! (no goal hints)` distribution
- [ ] Update existing distributions

---

## Phase 6: ROM Patching Updates

### 6.1 ASM Binary Updates
**Priority: HIGH | Complexity: HIGH (External Dependency)**

**Critical:** New features require updated ASM patches.

**Options:**
1. Grab ASM binaries from upstream release (https://github.com/OoTRandomizer/OoT-Randomizer/tree/v8.0/data/generated / https://github.com/OoTRandomizer/OoT-Randomizer/tree/v8.0/ASM/build)
2. Extract pre-built binaries from upstream release
3. Port only non-ASM features initially

**Files needed from 8.0 release:**
- `data/generated/rom_patch.txt` (714 KB vs current 446 KB)
- `data/generated/symbols.json` (31 KB vs current 10 KB)
- `data/items/*.zobj` (new item models for dungeon-specific keys, etc.)

**symbols.json Conversion Script:**
```python
import json

# Load upstream 8.0 symbols.json (complex format)
with open('upstream_symbols.json') as f:
    upstream = json.load(f)

# Convert to apworld format (simple)
apworld = {name: data['address'] for name, data in upstream.items()}

# Add AP-specific symbols (mapped to COOP_CONTEXT offsets)
apworld['DEATH_LINK'] = '0348002B'      # Reuses MW_PROGRESSIVE_ITEMS_ENABLE offset
apworld['AP_PLAYER_NAME'] = '03480839'  # Within PLAYER_NAMES area

with open('symbols.json', 'w') as f:
    json.dump(apworld, f, indent=4, sort_keys=True)
```

**New Symbols Required (27 for 8.0 core features):**
```
# Silver Rupee System
SHUFFLE_SILVER_RUPEES
CFG_DUNGEON_INFO_SILVER_RUPEES

# TCG Keys
SHUFFLE_CHEST_GAME
TCG_REQUIRES_LENS

# Hideout Entrances
HIDEOUT_SHUFFLED

# Ocarina Notes
SHUFFLE_OCARINA_BUTTONS
EPONAS_SONG_NOTES

# Key Rings + Boss Keys
KEYRING_BOSSKEY_CONDITION

# Trade Sequence
CFG_ADULT_TRADE_SHUFFLE
CFG_CHILD_TRADE_SHUFFLE

# Chest/Pot Textures (13 symbols)
CHEST_GILDED_TEXTURE, CHEST_GOLD_TEXTURE, CHEST_SILVER_TEXTURE
CHEST_SKULL_TEXTURE, CHEST_HEART_TEXTURE
POTCRATE_GILDED_TEXTURE, POTCRATE_GOLD_TEXTURE, POTCRATE_SILVER_TEXTURE
POTCRATE_SKULL_TEXTURE, POTCRATE_HEART_TEXTURE
SOA_UNLOCKS_CHEST_TEXTURE, SOA_UNLOCKS_POTCRATE_TEXTURE
CUSTOM_KEY_MODELS

# Infrastructure
AUDIOBANK_TABLE_EXTENDED
FREE_BOMBCHU_DROPS
REWARDS_AS_ITEMS
```

**Renamed Symbols (update Patches.py references):**
| Old (Apworld) | New (Upstream 8.0) |
|---------------|-------------------|
| `SILVER_CHEST_FRONT_TEXTURE` | Use `CHEST_SILVER_TEXTURE` |
| `GILDED_CHEST_FRONT_TEXTURE` | Use `CHEST_GILDED_TEXTURE` |
| `SKULL_CHEST_FRONT_TEXTURE` | Use `CHEST_SKULL_TEXTURE` |
| `BOMBCHUS_IN_LOGIC` | Use `FREE_BOMBCHU_DROPS` |

---

### 6.2 SaveContext Updates
**Priority: HIGH | Complexity: MEDIUM**

- [ ] Add silver rupee tracking to save context
- [ ] Add ocarina notes tracking
- [ ] Add new flags for settings

**Files to modify:**
- `SaveContext.py`

---

### 6.3 Patches.py Updates
**Priority: HIGH | Complexity: HIGH**

- [ ] Add silver rupee patching
- [ ] Add ocarina notes patching
- [ ] Add TCG key patching
- [ ] Add hideout entrance patching
- [ ] Update message patching for key counts
- [ ] Update renamed symbol references

**Step-by-Step: Updating Patches.py**

1. **Update symbol references for renamed symbols:**

| Find | Replace With |
|------|--------------|
| `rom.sym('SILVER_CHEST_FRONT_TEXTURE')` | `rom.sym('CHEST_SILVER_TEXTURE')` |
| `rom.sym('GILDED_CHEST_FRONT_TEXTURE')` | `rom.sym('CHEST_GILDED_TEXTURE')` |
| `rom.sym('SKULL_CHEST_FRONT_TEXTURE')` | `rom.sym('CHEST_SKULL_TEXTURE')` |
| `rom.sym('BOMBCHUS_IN_LOGIC')` | `rom.sym('FREE_BOMBCHU_DROPS')` |

2. **Add new patching for silver rupees** (reference upstream Patches.py ~line 1024):
```python
# Add after existing shuffle settings:
if world.shuffle_silver_rupees:
    rom.write_byte(rom.sym('SHUFFLE_SILVER_RUPEES'), 1)
    if world.settings.shuffle_silver_rupees != 'remove':
        rom.write_byte(rom.sym('CFG_DUNGEON_INFO_SILVER_RUPEES'), 1)
```

3. **Add TCG key patching** (reference upstream ~line 1631):
```python
if world.settings.shuffle_tcgkeys != 'vanilla':
    if world.settings.shuffle_tcgkeys == 'remove':
        rom.write_byte(rom.sym('SHUFFLE_CHEST_GAME'), 0x02)
    else:
        rom.write_byte(rom.sym('SHUFFLE_CHEST_GAME'), 0x01)

if world.settings.tcg_requires_lens:
    rom.write_byte(rom.sym('TCG_REQUIRES_LENS'), 0x01)
```

4. **Add hideout entrance patching** (reference upstream ~line 797):
```python
if world.settings.shuffle_hideout_entrances:
    rom.write_byte(rom.sym('HIDEOUT_SHUFFLED'), 1)
```

5. **Add ocarina notes patching** (reference upstream ~line 1921):
```python
if world.settings.shuffle_individual_ocarina_notes:
    rom.write_byte(rom.sym('SHUFFLE_OCARINA_BUTTONS'), 1)
```

6. **Add trade sequence patching** (reference upstream ~line 770):
```python
if world.settings.adult_trade_shuffle:
    rom.write_byte(rom.sym('CFG_ADULT_TRADE_SHUFFLE'), 0x01)
if world.settings.shuffle_child_trade:
    rom.write_byte(rom.sym('CFG_CHILD_TRADE_SHUFFLE'), 0x01)
```

7. **Add key ring boss key patching** (reference upstream ~line 960):
```python
symbol = rom.sym('KEYRING_BOSSKEY_CONDITION')
# Port the keyring boss key condition logic
```

8. **Update item model loading** (reference upstream ~line 70-95):
```python
# Add new zobj imports for dungeon-specific keys, etc.
zobj_imports = (
    ('object_gi_triforce',    data_path('items/Triforce.zobj'),     0x193),
    ('object_gi_keyring',     data_path('items/KeyRing.zobj'),      0x195),
    ('object_gi_warpsong',    data_path('items/Note.zobj'),         0x196),
    ('object_gi_chubag',      data_path('items/ChuBag.zobj'),       0x197),
    # ... add all dungeon-specific keys from upstream
)
```

**New Symbols to Add References For:**
```python
# These symbols are NEW - add rom.write_* calls:
SHUFFLE_SILVER_RUPEES
CFG_DUNGEON_INFO_SILVER_RUPEES
SHUFFLE_CHEST_GAME
TCG_REQUIRES_LENS
HIDEOUT_SHUFFLED
SHUFFLE_OCARINA_BUTTONS
KEYRING_BOSSKEY_CONDITION
CFG_ADULT_TRADE_SHUFFLE
CFG_CHILD_TRADE_SHUFFLE
CUSTOM_KEY_MODELS
AUDIOBANK_TABLE_EXTENDED
REWARDS_AS_ITEMS
FREE_BOMBCHU_DROPS
```

**Files to modify:**
- `Patches.py` (major changes - ~200 lines added/modified)
- `Messages.py` (if separate)

---

## Phase 7: Cosmetics & Minor Features

### 7.1 New Cosmetic Options
**Priority: LOW | Complexity: LOW**

- [ ] Rainbow tunic options
- [ ] Speed Up Music for Last Triforce Piece
- [ ] Slow Down Music When Low HP
- [ ] Uninvert Y-Axis in First Person
- [ ] D-Pad HUD left side option
- [ ] Key Appearance Matches Dungeon

**Files to modify:**
- `ColorSFXOptions.py`
- `Cosmetics.py`

---

### 7.2 New SFX Options
**Priority: LOW | Complexity: LOW**

- [ ] Port new SFX shuffle options from upstream

**Files to modify:**
- `Sounds.py`
- `ColorSFXOptions.py`

---

## Phase 8: Bug Fixes & Behavior Changes

### 8.1 Critical Bug Fixes
**Priority: HIGH | Complexity: VARIES**

- [ ] Fix path of hearts goal not enabled in certain cases
- [ ] Fix CSMC chests with ice traps not moved correctly
- [ ] Fix Lost Woods bridge ocarina check giving wrong item
- [ ] Fix Magic Beans starting count (9 -> 10)

---

### 8.2 Behavior Changes
**Priority: MEDIUM | Complexity: LOW**

- [ ] Closed Forest no longer changed to Closed Deku with Boss ER
- [ ] Heart Containers/Pieces no longer directly hinted by WotH
- [ ] Junk items float up when sent to another world
- [ ] Farore's Wind dungeon warping in logic

---

## Phase 9: Testing

### 9.1 Unit Tests
- [ ] Test new settings parse correctly
- [ ] Test item/location ID mappings
- [ ] Test silver rupee pool generation

**Quick Smoke Test:**
```python
# Run from MultiworldGG root:
python -m worlds.oot.test_generation
# Or if no test file exists, try generating a seed:
python -m worlds.oot --seed 12345 --settings '{"shuffle_silver_rupees": "dungeon"}'
```

### 9.2 Integration Tests
- [ ] Generate seeds with all new settings
- [ ] Test silver rupee + keysanity combinations
- [ ] Test hideout ER + interior ER
- [ ] Test TCG keys shuffle

**Test Matrix - Generate seeds with each combination:**

| Setting | Values to Test |
|---------|----------------|
| `shuffle_silver_rupees` | `vanilla`, `dungeon`, `overworld`, `anywhere`, `remove` |
| `shuffle_tcgkeys` | `vanilla`, `shuffle`, `remove` |
| `shuffle_hideout_entrances` | `off`, `on` |
| `shuffle_individual_ocarina_notes` | `off`, `on` |
| `key_rings_give_bosskeys` | `off`, `on` |
| `adult_trade_shuffle` | Various combinations |

### 9.3 Multiworld Tests
- [ ] Test silver rupee items between players
- [ ] Test new entrance hints in multiworld
- [ ] Test trade items in multiworld

**Multiworld Test Checklist:**
```
1. Generate 2-player multiworld with silver rupees on for both
2. Verify silver rupees can be placed in other player's world
3. Verify collecting other player's silver rupee sends correctly
4. Verify silver rupee counts update properly
5. Test with one player vanilla, one player keysanity
```

### 9.4 ROM Verification

**Manual ROM Tests:**
- [ ] Load generated ROM in emulator
- [ ] Verify file select hash displays correctly
- [ ] Verify new item models appear (key rings, notes, etc.)
- [ ] Collect a silver rupee and verify counter
- [ ] Test death link toggle (if enabled)
- [ ] Verify no crashes on new entrances

**Regression Tests:**
- [ ] Generate seed with 7.1 settings (no new features)
- [ ] Verify all existing functionality still works
- [ ] Test keysanity + boss shuffle + ER combination
- [ ] Test Triforce Hunt mode

---

## Verification Checklist

Use this checklist before considering the update complete:

### Symbol Verification
- [ ] All 27 new symbols exist in `symbols.json`
- [ ] AP-specific symbols (`DEATH_LINK`, `AP_PLAYER_NAME`) present
- [ ] No `KeyError` when generating seeds

### Item Verification
- [ ] All 57 new items have valid IDs
- [ ] Silver rupees show correct names in spoiler
- [ ] Pouches correctly count as 5 rupees
- [ ] Ocarina notes work with song logic

### Location Verification
- [ ] All ~150 new locations accessible
- [ ] Silver rupee locations have correct parent regions
- [ ] TCG locations only appear when shuffled
- [ ] Logic correctly gates silver rupee locations

### Generation Verification
- [ ] No generation failures with default settings
- [ ] No generation failures with all new settings ON
- [ ] Generation time reasonable (<30 seconds typical seed)
- [ ] Spoiler log contains new locations/items

### Multiworld Verification
- [ ] Items send/receive correctly between players
- [ ] Death link works (if implemented)
- [ ] No desync issues with silver rupees
- [ ] Hints work for new location types

---

## Dependency Graph

```
Phase 1 (Foundation)
    │
    ├──► Phase 2 (Settings)
    │        │
    │        └──► Phase 3 (Logic)
    │                 │
    │                 └──► Phase 4 (Entrances)
    │
    └──► Phase 6 (ROM Patching) ◄── [External: ASM Binaries]
             │
             └──► Phase 5 (Hints)
                      │
                      └──► Phase 7 (Cosmetics)
                               │
                               └──► Phase 8 (Bug Fixes)
                                        │
                                        └──► Phase 9 (Testing)
```

---

## Effort Estimates

| Phase | Tasks | Estimated LOC Changes | Complexity |
|-------|-------|----------------------|------------|
| 1. Foundation | 3 | +200 | Medium |
| 2. Settings | 10+ | +400 | High |
| 3. Logic | 15 | +600 | Medium |
| 4. Entrances | 2 | +150 | High |
| 5. Hints | 6 | +200 | Medium |
| 6. ROM Patching | 4 | +500 | High |
| 7. Cosmetics | 7 | +100 | Low |
| 8. Bug Fixes | 8 | +50 | Low |
| 9. Testing | - | - | Medium |
| **Total** | **55+** | **~2200** | **High** |

---

## Risk Mitigation

### High-Risk Items

1. **Silver Rupee System**
   - Mitigation: Implement as optional feature, default OFF
   - Fallback: Skip if too complex, prioritize for 8.1+

2. **ASM Binary Updates**
   - Mitigation: Test with upstream binaries first
   - Fallback: Disable features requiring new ASM

3. **Ocarina Notes Shuffle**
   - Mitigation: Implement last, verify all song logic
   - Fallback: Skip for initial release

4. **Hideout Entrance Shuffle**
   - Mitigation: Extensive ER testing
   - Fallback: Disable if causing generation failures

---

## Recommended Implementation Order

1. **Must Have (Core Functionality)**
   - Phase 1: Foundation
   - Phase 6.1: ASM binaries (or confirm compatibility)
   - Phase 8.1: Critical bug fixes

2. **Should Have (Popular Features)**
   - Phase 2.1: Silver Rupee settings
   - Phase 3.1: Logic updates
   - Phase 4.1: Gerudo Valley river exit

3. **Nice to Have (Quality of Life)**
   - Phase 2.2: TCG Keys
   - Phase 2.4: Minor settings
   - Phase 5: Hints updates
   - Phase 7: Cosmetics

4. **Defer if Needed**
   - Phase 2.3: Trade sequence rework
   - Phase 2.4: Ocarina notes shuffle
   - Phase 4.2: Hideout entrances

---

## File Change Summary

| File | Changes | Priority |
|------|---------|----------|
| `__init__.py` | Silver rupees, trade, settings | HIGH |
| `Options.py` | +15 new options | HIGH |
| `Items.py` | +100 new items | HIGH |
| `LocationList.py` | +150 new locations | HIGH |
| `ItemPool.py` | Pool generation for new items | HIGH |
| `EntranceShuffle.py` | +2 entrance types | MEDIUM |
| `data/World/*.json` | Logic updates | HIGH |
| `Patches.py` | ROM patching for new features | HIGH |
| `SaveContext.py` | New save flags | HIGH |
| `Hints.py` | New hint types | MEDIUM |
| `HintList.py` | New hint texts | MEDIUM |
| `Cosmetics.py` | New cosmetic options | LOW |
| `ColorSFXOptions.py` | New SFX options | LOW |

---

## Troubleshooting

### Common Issues

**KeyError: 'SYMBOL_NAME'**
```
Cause: Symbol missing from symbols.json
Fix: Ensure symbols.json was converted correctly and includes the symbol
Check: grep -c "SYMBOL_NAME" worlds/oot/data/generated/symbols.json
```

**Item not found in item_table**
```
Cause: New item not added to Items.py
Fix: Add item definition with correct name matching upstream
Check: Verify exact spelling matches upstream ItemList.py
```

**Location has no parent region**
```
Cause: Region not defined in World JSON files
Fix: Add region to appropriate data/World/*.json file
Check: Verify region name matches exactly in both location and JSON
```

**Generation fails with silver rupees**
```
Cause: Usually logic issue or missing locations
Fix:
1. Check all silver rupee locations are defined
2. Verify logic rules allow access
3. Check item pool has correct number of silver rupees
Debug: Generate with --debug flag, check logs
```

**ROM crashes on load**
```
Cause: Mismatched rom_patch.txt and symbols.json
Fix: Ensure both files are from the same 8.0 build
Check: Verify file sizes match expected (rom_patch.txt ~714KB)
```

**AP symbols not working (death link, etc.)**
```
Cause: AP symbol addresses incorrect for new ASM
Fix: Recalculate offsets based on new COOP_CONTEXT layout
Check: Verify COOP_CONTEXT base address matches (0x03480020)
```

### Debug Commands

```bash
# Test single seed generation
python Generate.py --seed 12345 --player 1 --game "Ocarina of Time"

# Test with specific settings
python Generate.py --seed 12345 --player 1 --game "Ocarina of Time" \
  --option "shuffle_silver_rupees=dungeon"

# Verify symbols.json format
python -c "import json; d=json.load(open('worlds/oot/data/generated/symbols.json')); print(len(d), 'symbols')"

# Check for missing items
python -c "from worlds.oot.Items import item_table; print(len(item_table), 'items')"
```

### Getting Help

- **Upstream OoTR Discord**: For understanding upstream implementation details
- **Archipelago Discord #oot**: For AP-specific integration questions
- **Upstream GitHub Issues**: Search for related bugs/features
- **Compare with upstream**: When in doubt, diff against upstream implementation

---

## Appendix: Full File List

### Files to Create
- `worlds/oot/data/items/` directory with all `.zobj` files

### Files to Modify (Priority Order)
1. `data/generated/symbols.json` - Convert from upstream
2. `data/generated/rom_patch.txt` - Copy from upstream
3. `Items.py` - Add ~60 new items
4. `LocationList.py` - Add ~150 new locations
5. `Options.py` - Add ~15 new options
6. `Patches.py` - Add ROM patching for new features
7. `Location.py` - Add new location types
8. `ItemPool.py` - Add pool generation logic
9. `EntranceShuffle.py` - Add new entrance types
10. `data/World/*.json` - Update logic files
11. `Hints.py` - Add new hint types
12. `HintList.py` - Add new hint texts
13. `SaveContext.py` - Add new save flags
14. `Cosmetics.py` - Add new cosmetic options

### Files to Reference (Upstream)
- `ItemList.py` → `Items.py`
- `LocationList.py` → `LocationList.py`
- `SettingsList.py` → `Options.py`
- `Patches.py` → `Patches.py`
- `World.py` → `__init__.py`
- `EntranceShuffle.py` → `EntranceShuffle.py`

---

*Document Version: 1.1*
*Created: 2024-12-31*
*Last Updated: 2024-12-31*
*Analysis by: Claude Code*
