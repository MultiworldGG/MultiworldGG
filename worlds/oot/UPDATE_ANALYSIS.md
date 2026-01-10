# OoT Apworld Update Analysis: 7.1.0 to 9.0.0

## Executive Summary

The MultiworldGG Ocarina of Time apworld implementation is based on **version 7.1.0** of the upstream OoT-Randomizer, while the current upstream release is **version 9.0.0**. This represents a **2 major version gap** with substantial new features, logic changes, and architectural improvements.

**Complexity Assessment: HIGH**

Updating the apworld will require significant effort due to:
- Many new shuffle systems and settings
- Extensive logic changes across all world files
- New modules that need Archipelago integration
- Breaking changes in the settings/options system
- ASM/patch changes requiring new binaries

---

## Version Information

| Component | Apworld (Current) | Upstream (Latest) |
|-----------|-------------------|-------------------|
| Version   | 7.1.0             | 9.0.0 Release     |
| Python    | 3.8+              | 3.9+ (3.8 dropped)|

---

## File Size Comparison (Lines of Code)

| File Category | Upstream | Apworld | Difference |
|---------------|----------|---------|------------|
| Settings/Options | 5,758 | 1,448 | +298% |
| Logic Tricks | 3,321 | 1,547 | +115% |
| Location List | 2,658 | 2,103 | +26% |
| Hint List | 2,058 | 1,717 | +20% |
| Item List | 705 | 433 | +63% |
| Entrance Shuffle | 1,166 | 966 | +21% |
| Overworld.json | 3,298 | 2,899 | +14% |

---

## Major New Features (7.1 -> 9.0)

### Version 8.0 Features
1. **Silver Rupee Shuffle** - Entire new item category with pouches option
2. **Treasure Chest Game Keys Shuffle** - Keys can be anywhere in the world
3. **Wonderitem Shuffle** - New location type with visual indicators
4. **Thieves' Hideout Entrance Shuffle** - Interior entrance pool expansion
5. **Hyrule Loach Reward Shuffle** - New fishing mechanic
6. **Individual Ocarina Notes Shuffle** - Notes as items
7. **Key Rings give Boss Keys** - Combined key functionality
8. **Reworked Trade Sequences** - Multiple trade items per age, multiselect
9. **Important Checks Hint Type** - Major items per region hints
10. **Many new SFX and cosmetic options**
11. **New model for key rings**
12. **Goals system for hint generation**

### Version 8.1 Features
1. **Minor Items in Big Chests** - Granular multiselect
2. **Combined Trial Hints** option
3. **Clearer Rainbow Bridge hints**

### Version 8.2 Features
1. **Input Viewer cosmetic**
2. **Stone of Agony Unlocks Chest Textures**
3. **Include Empty Pots/Crates settings**
4. **Pre-completed Dungeons: Specific Rewards** mode
5. **ToT Reward from Rauru** rename and skip option
6. **Password Lock plando setting**
7. **Fairy pots in shuffle**
8. **Boss key icon display**

### Version 8.3 Features
1. **Custom Ice Trap counts**
2. **Shadow Temple boat speedup**
3. **Lens of Truth for TCG setting**
4. **Market Big Poes misc hint**
5. **Shuffle Ganon's Tower Entrance**
6. **GF child heart piece setting**
7. **MM Randomizer custom music support**

### Version 9.0 Features
1. **Advanced Logic** - Renamed from Glitched, now works with all settings including ER
2. **Many new advanced tricks**
3. **Door of Time new options** (Stones/Ocarina requirements)
4. **Additional Random Starting Items**
5. **Maps/Compasses give dungeon/boss entrance info**
6. **Scarecrow Behavior setting** (replaces Free Scarecrow)
7. **100 Skulltula Reward shuffle**
8. **Special deal price controls**
9. **Randomize Frogs 2 melody**

---

## New Upstream Modules (Not in Apworld)

| Module | Purpose | Integration Complexity |
|--------|---------|------------------------|
| `Goals.py` | Goal-based hint system | HIGH - Core hint logic |
| `State.py` | Search state management | MEDIUM - Logic system |
| `Search.py` | Item accessibility search | HIGH - Fill algorithm |
| `StartingItems.py` | Starting item management | LOW - Data structure |
| `OcarinaSongs.py` | Ocarina song randomization | MEDIUM - New feature |
| `RulesCommon.py` | Shared rule utilities | LOW - Helper functions |
| `Audiobank.py` | Audio bank management | MEDIUM - ROM patching |
| `MusicHelpers.py` | Music shuffle helpers | MEDIUM - Cosmetics |
| `Sequence.py` | Music sequence handling | MEDIUM - Cosmetics |
| `SettingsListTricks.py` | Separated tricks settings | MEDIUM - Options |

---

## Architecture Differences

### Settings System
- **Upstream**: Uses `SettingsList.py` with `SettingInfo` classes (5,758 lines)
- **Apworld**: Uses Archipelago's `Options` system with custom classes (1,448 lines)
- **Challenge**: Every new setting must be translated to AP's option format

### World/State Management
- **Upstream**: `World.py` class with internal state management
- **Apworld**: Inherits from AP's `World` class with mixin state
- **Challenge**: State tracking (child/adult reachability) must be adapted

### Fill Algorithm
- **Upstream**: Custom `Fill.py` with sophisticated placement logic
- **Apworld**: Uses AP's `fill_restrictive` with custom pre-fill
- **Challenge**: New item types (silver rupees, etc.) need special handling

### Hints System
- **Upstream**: Complex `Goals.py` with category-based hints
- **Apworld**: Simplified hint generation integrated with AP
- **Challenge**: Goals system would require significant rework

---

## Required Update Tasks

### Phase 1: Foundation (Estimated: Large effort)
1. Update Python version requirement to 3.9+
2. Port new settings to Archipelago Options format
3. Add new item definitions to Items.py
4. Add new location definitions to LocationList.py
5. Update world JSON files with new logic

### Phase 2: Core Features (Estimated: Very large effort)
1. Implement Silver Rupee shuffle system
2. Implement Wonderitem shuffle
3. Implement Treasure Chest Game keys
4. Implement Thieves' Hideout entrance shuffle
5. Implement Individual Ocarina Notes shuffle
6. Port Advanced Logic system

### Phase 3: Logic & Tricks (Estimated: Large effort)
1. Port ~1,800 new lines of logic tricks
2. Update all dungeon logic files
3. Update Overworld.json with ~400 new lines
4. Integrate new Goals system for hints

### Phase 4: Patching & ROM (Estimated: Large effort)
1. Update ASM patches and binaries
2. Port new cosmetic options
3. Update ROM patching for new features
4. Update save context for new items

### Phase 5: Testing & Integration (Estimated: Large effort)
1. Test all new settings combinations
2. Test multiworld compatibility
3. Test entrance randomizer with new entrances
4. Regression test existing functionality

---

## Risk Assessment

### High Risk Areas
1. **Advanced Logic + ER** - Complex interaction, upstream took years to implement
2. **Silver Rupee System** - New item category with puzzle tracking
3. **Goals System** - Deep integration with hint generation
4. **ASM Changes** - Binary patches may have breaking changes

### Medium Risk Areas
1. **Settings Migration** - Many renamed/restructured settings
2. **Trade Sequence Rework** - Logic changes throughout
3. **Entrance Shuffle Expansion** - New pool interactions

### Low Risk Areas
1. **Cosmetic Options** - Additive changes
2. **Hint Text Updates** - String changes
3. **Speedups** - Mostly ROM patches

---

## Recommendations

### Option A: Full Update (Recommended for feature parity)
- Port all changes from 7.1 to 9.0
- Estimated effort: 3-6 months of dedicated development
- Pros: Full feature parity, community benefit
- Cons: High effort, risk of breaking existing seeds

### Option B: Selective Update
- Port only critical bug fixes and high-demand features
- Skip complex features (Advanced Logic, Silver Rupees)
- Estimated effort: 1-2 months
- Pros: Lower risk, faster delivery
- Cons: Growing version divergence

### Option C: Incremental Updates
- Update in phases (8.0, 8.1, 8.2, 8.3, 9.0)
- Release each phase for testing
- Estimated effort: 6-12 months
- Pros: Manageable chunks, community testing
- Cons: Extended timeline, maintenance burden

---

## Dependencies & Prerequisites

1. **ROM Patching**: New ASM binaries from upstream
2. **Testing Infrastructure**: Seed generation tests
3. **Documentation**: Settings translation guide
4. **Community**: Coordination with upstream for clarifications

---

## ROM Patching & Symbols Analysis

### Generated Files Comparison

| File | Apworld | Upstream 9.0 | Notes |
|------|---------|--------------|-------|
| `rom_patch.txt` | 446 KB | 714 KB | +60% more ASM code |
| `symbols.json` | 10 KB (255 lines) | 31 KB (1,449 lines) | +5.7x more symbols |
| `patch_symbols.json` | N/A | 940 bytes | New file in upstream |
| `settings_list.json` | N/A | 1.5 MB | GUI settings (not needed) |

### symbols.json Format Difference

**Apworld format (simple):**
```json
{
    "SYMBOL_NAME": "03480839"
}
```

**Upstream format (complex):**
```json
{
    "SYMBOL_NAME": {
        "address": "034861B8",
        "length": 4
    }
}
```

The apworld's `Rom.py:34` parses as: `{name: int(addr, 16) for name, addr in symbols.items()}`

**Conversion required:** Extract addresses from upstream format, add AP-specific symbols.

### COOP_CONTEXT Memory Layout

Both use the same base address (`0x03480020`) for multiworld context:

```
COOP_CONTEXT:          ; Base: 0x03480020
├── COOP_VERSION       ; +0x00 (4 bytes)
├── PLAYER_ID          ; +0x04 (1 byte)
├── PLAYER_NAME_ID     ; +0x05 (1 byte)
├── INCOMING_PLAYER    ; +0x06 (2 bytes)
├── INCOMING_ITEM      ; +0x08 (2 bytes)
├── MW_SEND_OWN_ITEMS  ; +0x0A (1 byte)
├── [DEATH_LINK]       ; +0x0B (1 byte) - AP reuses this offset
├── ...
├── PLAYER_NAMES       ; +0x14 (8*256 bytes)
│   └── [AP_PLAYER_NAME] ; +0x819 offset within PLAYER_NAMES
└── ...
```

### AP-Specific Symbols (Must Preserve)

| Symbol | Address | Purpose |
|--------|---------|---------|
| `AP_PLAYER_NAME` | 0x03480839 | Archipelago player name |
| `DEATH_LINK` | 0x0348002B | Death link toggle |

These can be mapped to existing COOP_CONTEXT offsets in the upstream ASM.

### Patches.py Symbol Usage

| Metric | Upstream | Apworld |
|--------|----------|---------|
| Unique symbols used | 104 | 83 |
| New symbols needed | 45 | - |
| AP-only symbols | - | 2 |

### New Symbols Required for 8.0+ (45 total)

**Core Feature Symbols:**
```
SHUFFLE_SILVER_RUPEES         # Silver rupee shuffle
CFG_DUNGEON_INFO_SILVER_RUPEES
SHUFFLE_CHEST_GAME            # TCG keys shuffle
TCG_REQUIRES_LENS
HIDEOUT_SHUFFLED              # Thieves' Hideout ER
SHUFFLE_OCARINA_BUTTONS       # Ocarina notes shuffle
KEYRING_BOSSKEY_CONDITION     # Key rings give boss keys
CFG_ADULT_TRADE_SHUFFLE       # Trade sequence rework
CFG_CHILD_TRADE_SHUFFLE
DOT_CONDITION                 # Door of Time condition
```

**Cosmetic/Texture Symbols:**
```
CHEST_GILDED_TEXTURE          # Chest texture options
CHEST_GOLD_TEXTURE
CHEST_SILVER_TEXTURE
CHEST_SKULL_TEXTURE
CHEST_HEART_TEXTURE
POTCRATE_GILDED_TEXTURE       # Pot/crate textures
POTCRATE_GOLD_TEXTURE
POTCRATE_SILVER_TEXTURE
POTCRATE_SKULL_TEXTURE
POTCRATE_HEART_TEXTURE
SOA_UNLOCKS_CHEST_TEXTURE     # Stone of Agony unlocks
SOA_UNLOCKS_POTCRATE_TEXTURE
CUSTOM_KEY_MODELS             # Dungeon-specific keys
```

**Infrastructure Symbols:**
```
AUDIOBANK_TABLE_EXTENDED      # Music system
CFG_BIGOCTO_OVERRIDE_KEY
CFG_BOSSES
CFG_DUNGEON_BOSS_INFO
CFG_DUNGEON_ENTRANCES
CFG_DUNGEON_PRECOMPLETED
CFG_DUNGEON_REWARD_WORLDS
CFG_DUNGEON_INFO_REWARD_WORLDS_ENABLE
CFG_MASK_AUTOEQUIP
CFG_MASK_SHOP_HINT
EPONAS_SONG_NOTES
FREE_BOMBCHU_DROPS
PASSWORD
PLANDOMIZER_USED
REWARDS_AS_ITEMS
SHUFFLE_GRANNYS_POTION_SHOP
SPECIAL_DEAL_COUNTS
SPOILER_AVAILABLE
WEB_ID_STRING_TXT
xflag_room_blob               # Extended flags system
xflag_room_table
xflag_scene_table
```

### Symbols in Apworld Not in Upstream (Renamed/Refactored)

These symbols exist in apworld but are named differently or refactored in upstream:

| Apworld Symbol | Upstream Equivalent | Notes |
|----------------|---------------------|-------|
| `SILVER_CHEST_FRONT_TEXTURE` | `CHEST_SILVER_TEXTURE` | Renamed |
| `GILDED_CHEST_FRONT_TEXTURE` | `CHEST_GILDED_TEXTURE` | Renamed |
| `SKULL_CHEST_FRONT_TEXTURE` | `CHEST_SKULL_TEXTURE` | Renamed |
| `BOMBCHUS_IN_LOGIC` | `FREE_BOMBCHU_DROPS` | Refactored |
| `ENHANCE_MAP_COMPASS` | Multiple CFG_* symbols | Split |
| `collectible_override_flags` | `xflag_*` symbols | New system |

### Update Path for ROM Patching

1. **Get both files from 8.0 release:**
   - `data/generated/rom_patch.txt`
   - `data/generated/symbols.json`

2. **Convert symbols.json format:**
   ```python
   import json

   with open('upstream_symbols.json') as f:
       upstream = json.load(f)

   apworld = {name: data['address'] for name, data in upstream.items()}

   # Add AP-specific symbols (mapped to COOP_CONTEXT offsets)
   apworld['DEATH_LINK'] = '0348002B'
   apworld['AP_PLAYER_NAME'] = '03480839'

   with open('symbols.json', 'w') as f:
       json.dump(apworld, f, indent=4)
   ```

3. **Update Patches.py:**
   - Add new symbol references for 8.0 features
   - Update renamed symbols (chest textures, etc.)
   - Port xflag system for extended collectible tracking

4. **Get new item models:**
   - `data/items/*.zobj` (dungeon-specific keys, magic meter, etc.)

---

## Conclusion

Updating the OoT apworld from 7.1.0 to 9.0.0 is a significant undertaking that will require substantial development effort. The upstream has added major new shuffle systems, reworked the logic system to support Advanced (Glitched) mode with all settings, and expanded hints significantly.

The recommended approach is **Option C: Incremental Updates**, starting with the most impactful features (Silver Rupees, new entrance shuffles) and gradually incorporating the rest. This allows for community testing and feedback while maintaining stability.

Key priority features to consider first:
1. Silver Rupee Shuffle (highly requested)
2. Treasure Chest Game Keys
3. Thieves' Hideout Entrance Shuffle
4. Bug fixes from all versions

---

*Generated: 2024-12-31*
*Analysis by: Claude Code*
