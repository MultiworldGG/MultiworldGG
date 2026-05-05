; MultiworldGG-specific symbol definitions
; These addresses are within the payload region and get auto-exported to symbols.json.
; Addresses correspond to locations in config.asm and the C bundle that MultiworldGG
; reads/writes at patch time but are not labeled in the upstream OoT randomizer build.

;==================================================================================================
; Config flags written by Patches.py
;==================================================================================================
.definelabel DUNGEON_IS_MQ_ADDRESS,        0x80400010
.definelabel DUNGEON_REWARDS_ADDRESS,      0x80400014
.definelabel ENHANCE_MAP_COMPASS,          0x80400018
.definelabel SHOW_DUNGEON_REWARDS,         0x80400019
.definelabel SMALL_KEY_SHUFFLE,            0x8040001A
.definelabel SHUFFLE_SCRUBS,               0x8040001B
.definelabel OPEN_FOREST,                  0x8040001C
.definelabel OPEN_FOUNTAIN,                0x8040001D
.definelabel BIG_POE_COUNT,                0x8040001E
.definelabel DEATH_LINK,                   0x8040002B

;==================================================================================================
; AP multiworld data
;==================================================================================================
.definelabel AP_PLAYER_NAME,               0x80400839

; Note: satisfied_pending_frames is already auto-exported from the C bundle (bundle.o).
; Its correct VRAM address is resolved at link time; no .definelabel needed.
