"""Direct-emulator-memory client for the Banjo-Tooie Archipelago apworld.

Modules:
    emu_loader  -- attach to an emulator, expose endian-aware u8/u16/u32 I/O
    addresses   -- per-location flag descriptors parsed from the connector data
    state       -- read-only pollers (location flags, map, death/tag counters)
    game        -- write-side helpers (slot settings, items, traps, dialogs)
"""
