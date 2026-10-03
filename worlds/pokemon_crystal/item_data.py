POKEDEX_OFFSET = 10000
POKEDEX_COUNT_OFFSET = 20000
GRASS_OFFSET = 30000
FLAG_ITEM_OFFSET = 512
# Some items are effectively the same but with a different name in a different context; & this mask onto an item code
# to resolve its in-game ID
CANONICAL_ITEM_ID_MASK = 0x3ff

# AP_Start_Inventory is a 384 byte table of 3 byte entries; pocket sizes come from data.json
START_INVENTORY_ENTRIES = 128
