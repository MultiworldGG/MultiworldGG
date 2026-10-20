from .entrances import ENTRANCE_IDS

# Must match ASM/src/ap/entrances.asm. IDs are seed-version-local, with no migration.
ENTRANCE_TAG_BASE = 0x2000
ENTRANCE_CAPACITY = 512


def tag_entrance(rom, name, destination, variant=0):
    """Preserve the source identity until the ROM resolves the real destination."""
    entrance_id = ENTRANCE_IDS[name]
    if entrance_id >= ENTRANCE_CAPACITY:
        raise ValueError("Universal Tracker entrance table exceeds the ROM's capacity")
    address = rom.sym('AP_UT_ENTRANCE_DESTINATIONS') + entrance_id * 8
    if variant == 0:
        rom.write_int16s(address, [destination] * 4)
    else:
        rom.write_int16(address + variant * 2, destination)
    return ENTRANCE_TAG_BASE + entrance_id * 4 + variant
