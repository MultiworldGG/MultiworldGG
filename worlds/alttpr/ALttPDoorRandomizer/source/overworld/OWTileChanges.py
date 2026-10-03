# Static overworld map16 overlays written by the generator.
#
# In-game loader (Overworld_LoadNewTiles) applies this table first from bank $A3,
# then the dynamic OverworldMapChangePointers table. Seed-known overlays belong
# here; true runtime event checks / custom commands stay dynamic.
#
# Layout at SNES $A3B000 (PC $11B000):
#   - word pointers for screens $00..$81 (0x82 entries); $0000 = no changes
#   - packed overlay payloads (same encoding as the dynamic overlays)
#
# Each screen is assembled independently: every matching change(...) unit for that
# screen is concatenated in declaration order, then overlay() terminates once.
# Mixed reasons on one screen are just multiple change() entries with different
# when/param pairs (flip, glitch, disabled edge, etc.).

from enum import IntEnum
from typing import NamedTuple, Optional

from ...BaseClasses import OWEdge
from ...Utils import int16_as_bytes, snes_to_pc

# ---------------------------------------------------------------------------------------------------
# Addresses / layout

STATIC_MAP_SNES = 0xA3B000
NUM_SCREENS = 0x82
POINTER_TABLE_BYTES = NUM_SCREENS * 2  # 0x104
DATA_START_OFFSET = POINTER_TABLE_BYTES  # payloads pack immediately after the pointer table

# ---------------------------------------------------------------------------------------------------
# Inclusion rules

class ChangeWhen(IntEnum):
    """
    Condition family for a change unit. Optional string `param` refines the rule.

    FLIPPED param:
      None        — screen is flipped
      'noglitch'  — flipped and not OW-glitch logic (WarningFlags $20 skip)
      'glitched'  — flipped and OW-glitch logic

    OWLAYOUT param:
      None        — OW layout/crossed/mixed modes that set OWTileMapAlt bit $02
      'lw'        — same, and screen is light-world-like (OWTileWorldAssoc without $40)

    ATGT param:
      'swapped'   — Agahnim Tower / Ganon Tower swapped
      'vanilla'   — not swapped

    DISABLED_EDGE param:
      OWEdge name from create_owedges (e.g. 'Lost Woods EN'). Applies when
      that edge has no dest — the same condition Rom.py writes as destination $FF.
    """
    ALWAYS = 0
    FLIPPED = 1
    UNFLIPPED = 2
    ATGT = 3
    GLITCHED = 4
    OWLAYOUT = 5
    DISABLED_EDGE = 6


class Change(NamedTuple):
    when: ChangeWhen
    words: list
    param: Optional[str] = None


def is_disabled_edge(world, player, screen, edge_id):
    """True when this OWEdge is unconnected (ROM destination byte $FF)."""
    edge = world.check_for_owedge(edge_id, player)
    if edge is None:
        return False
    return not (edge.dest is not None and isinstance(edge.dest, OWEdge))


def change_applies(change, world, player, screen):
    when = change.when
    param = change.param
    flipped = world.is_tile_swapped(screen, player)
    glitched = world.logic[player] in ['owglitches', 'hybridglitches', 'nologic']

    if when == ChangeWhen.ALWAYS:
        return True

    if when == ChangeWhen.FLIPPED:
        if not flipped:
            return False
        if param is None:
            return True
        if param == 'noglitch':
            return not glitched
        if param == 'glitched':
            return glitched
        raise ValueError(f"Unknown FLIPPED param {param!r} on screen {screen:#x}")

    if when == ChangeWhen.UNFLIPPED:
        return not flipped

    if when == ChangeWhen.GLITCHED:
        return glitched

    if when == ChangeWhen.OWLAYOUT:
        if not (world.owLayout[player] != 'vanilla'
                or world.owCrossed[player] not in ['none', 'polar']
                or world.owMixed[player]):
            return False
        if param is None:
            return True
        if param == 'lw':
            return world.is_tile_lw_like(screen, player)
        raise ValueError(f"Unknown OWLAYOUT param {param!r} on screen {screen:#x}")

    if when == ChangeWhen.ATGT:
        swapped = world.is_atgt_swapped(player)
        if param == 'swapped':
            return swapped
        if param == 'vanilla':
            return not swapped
        raise ValueError(f"ATGT requires param 'swapped' or 'vanilla' on screen {screen:#x}")

    if when == ChangeWhen.DISABLED_EDGE:
        if not param:
            raise ValueError(f"DISABLED_EDGE requires param on screen {screen:#x}")
        return is_disabled_edge(world, player, screen, param)

    return False

# ---------------------------------------------------------------------------------------------------
# Overlay command encoding (mirrors invertedmaps.asm)

OWW_END = 0xFFFF
OWW_STOP = 0x8000
OWW_SKIP = 0xFFFF
OWW_VERTICAL = 0x0080
OWW_HORIZONTAL = 0x0000

OWW_STRIPE = 0x8000
OWW_STRIPE_RLE = 0x8001
OWW_STRIPE_RLE_INC = 0x8002
OWW_ARB_TILE_COPY = 0x8003


def oww_rle_size(size):
    return (size & 0x7F) << 8


def tile(tile_id, pos):
    """Single map16 write: dw <tile>, <pos>."""
    return [tile_id & 0xFFFF, pos & 0xFFFF]


def end():
    return [OWW_END]


def stripe(start, tiles, vertical=False):
    """
    Stripe of unique tiles; final tile is OR'd with OWW_STOP.

    Entries equal to OWW_SKIP leave a gap (bit 15 set, ASM continues without
    writing). SKIP is never OR'd with STOP.
    """
    if not tiles:
        raise ValueError('stripe requires at least one tile')
    direction = OWW_VERTICAL if vertical else OWW_HORIZONTAL
    words = [OWW_STRIPE | direction, start & 0xFFFF]
    last = len(tiles) - 1
    for i, t in enumerate(tiles):
        value = t & 0xFFFF
        if value == OWW_SKIP:
            words.append(OWW_SKIP)
        elif i == last:
            words.append(value | OWW_STOP)
        else:
            words.append(value)
    return words


def stripe_rle(tile_id, start, size, vertical=False):
    direction = OWW_VERTICAL if vertical else OWW_HORIZONTAL
    return [
        OWW_STRIPE_RLE | direction | oww_rle_size(size),
        tile_id & 0xFFFF,
        start & 0xFFFF,
    ]


def stripe_rle_inc(tile_id, start, size, vertical=False):
    direction = OWW_VERTICAL if vertical else OWW_HORIZONTAL
    return [
        OWW_STRIPE_RLE_INC | direction | oww_rle_size(size),
        tile_id & 0xFFFF,
        start & 0xFFFF,
    ]


def arb_tile_copy(tile_id, positions):
    """Write the same tile to each position; final pos is OR'd with OWW_STOP."""
    if not positions:
        raise ValueError('arb_tile_copy requires at least one position')
    words = [OWW_ARB_TILE_COPY, tile_id & 0xFFFF]
    for i, pos in enumerate(positions):
        value = pos & 0xFFFF
        if i == len(positions) - 1:
            value |= OWW_STOP
        words.append(value)
    return words


def overlay(*parts):
    """
    Flatten overlay fragments into a single screen payload, terminating with END.

    Applied at the screen-assembly layer after selecting which change units apply,
    so multiple sources/reasons can contribute fragments to the same screen.
    """
    words = []
    for part in parts:
        words.extend(part)
    if not words or words[-1] != OWW_END:
        words.append(OWW_END)
    return words

# ---------------------------------------------------------------------------------------------------
# Change units

def change(when, *parts, param=None):
    """
    Bundle tile-change fragments under a condition.

    when   — ChangeWhen family
    param  — optional string refining the condition (see ChangeWhen)
    parts  — fragment word lists from tile()/stripe()/...

    Does not append END; overlay() is applied when the screen is assembled.
    """
    words = []
    for part in parts:
        words.extend(part)
    return Change(when, words, param)


def build_screen_overlay(screen, world, player):
    """
    Build the static overlay word list for a single screen, or None if empty.

    Walks that screen's change units in order, keeps those whose when/param
    apply for this seed, then wraps with overlay().
    """
    units = SCREEN_CHANGES.get(screen)
    if not units:
        return None

    parts = []
    for unit in units:
        if unit.words and change_applies(unit, world, player, screen):
            parts.append(unit.words)
    if not parts:
        return None
    return overlay(*parts)

# ---------------------------------------------------------------------------------------------------
# Table build / ROM write

def _words_to_bytes(words):
    data = []
    for word in words:
        data.extend(int16_as_bytes(word & 0xFFFF))
    return data


def build_static_map_table(world, player):
    """
    Build the full static overlay blob: pointer table + payloads.

    Screens are assembled independently via build_screen_overlay, then packed
    in screen-id order immediately after the pointer table.

    Returns (blob_bytes, screen_pointer_snes_addrs) where the second value maps
    screen id -> SNES address of that screen's payload (or 0 if none).
    """
    screen_payloads = {}
    for screen in range(NUM_SCREENS):
        words = build_screen_overlay(screen, world, player)
        if words:
            screen_payloads[screen] = _words_to_bytes(words)

    pointers = [0] * NUM_SCREENS
    data = bytearray()
    cursor = DATA_START_OFFSET
    for screen in sorted(screen_payloads):
        payload = screen_payloads[screen]
        snes_addr = (STATIC_MAP_SNES + cursor) & 0xFFFF
        pointers[screen] = snes_addr
        data.extend(payload)
        cursor += len(payload)

    blob = bytearray()
    for ptr in pointers:
        blob.extend(int16_as_bytes(ptr))
    blob.extend(data)
    return bytes(blob), pointers


def write_static_map_changes(rom, world, player):
    """Write OverworldStaticMapPointers (+ payloads) to the fixed ROM location."""
    blob, _ = build_static_map_table(world, player)
    rom.write_bytes(snes_to_pc(STATIC_MAP_SNES), blob)
    return len(blob)

# ---------------------------------------------------------------------------------------------------
# Per-screen change units
#
# A screen is an ordered list of change(when, *fragments, param=...). Mixed
# types on one screen are separate units; only matching units are emitted, in
# list order, then overlay() terminates the payload.
#
# Runtime-only leftovers stay in invertedmaps.asm (event flags, custom commands).

SCREEN_CHANGES = {
    0x00: [
        change(ChangeWhen.DISABLED_EDGE,  # Lost Woods NW
            stripe(0x2512, [0x04C, 0x004, 0x030, 0x034], vertical=True),
            stripe(0x2514, [0x004, 0x004, 0x030, 0x034], vertical=True),
            stripe(0x2516, [0x004, 0x04C, 0x030, 0x034], vertical=True),
            param='Lost Woods NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lost Woods EN
            stripe(0x23FC, [0x0BA, 0x096, 0x08C, 0x096], vertical=True),
            stripe(0x23FE, [0x0BB, 0x021, 0x01A, 0x021, 0x045], vertical=True),
            param='Lost Woods EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lost Woods SW
            stripe(0x3E0E, [0x03F, 0x040]),
            stripe(0x3E8A, [0x0B1, 0x0AF, 0x045, 0x0B2, 0x023, 0x045, 0x046, 0x043]),
            stripe(0x3F0A, [0x016, 0x014, 0x015, 0x016, 0x014, 0x015, 0x054, 0x004]),
            stripe(0x3F8A, [0x01E, 0x01C, 0x01D, 0x01E, 0x01C, 0x01D, 0x02E, 0x004]),
            param='Lost Woods SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lost Woods SC
            stripe(0x3EAE, [0x0B1, 0x0AF, 0x045, 0x046, 0x06B]),
            stripe(0x3F2E, [0x016, 0x014, 0x015, 0x054, 0x004]),
            stripe(0x3FAE, [0x01E, 0x01C, 0x01D, 0x01F, 0x004]),
            param='Lost Woods SC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lost Woods SE
            stripe(0x3D6E, [0x337, 0x333]),
            stripe(0x3FF0, [0x01F, 0x02D]),
            param='Lost Woods SE',
        ),
    ],
    0x02: [
        change(ChangeWhen.DISABLED_EDGE,  # Lumberjack WN
            stripe(0x2380, [0x0BA, 0x096, 0x08C, 0x096], vertical=True),
            stripe(0x2382, [0x0BB, 0x097, 0x08D, 0x097], vertical=True),
            param='Lumberjack WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lumberjack SW
            stripe_rle_inc(0x333, 0x2F0C, 2),
            tile(0x336, 0x2F8E),
            stripe_rle(0x10B, 0x2F90, 13),
            param='Lumberjack SW',
        ),
    ],
    0x03: [
        change(ChangeWhen.FLIPPED,  # portal
            tile(0x034, 0x2BE0),
        ),
        change(ChangeWhen.FLIPPED,  # spectacle rock
            stripe(0x29B6, [0x21A, 0x1F3, 0x0A0, 0x104]),
            arb_tile_copy(0x0C6, [0x2A34, 0x2A38, 0x2A3A]),
            param='noglitch',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # West Death Mountain EN
            stripe(0x237E, [0x118, 0x127, 0x127, 0x6A7], vertical=True),
            param='West Death Mountain EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # West Death Mountain ES
            tile(0xD1E, 0x397E),
            stripe_rle(0x10A, 0x39FE, 4, vertical=True),
            tile(0x333, 0x3BFE),
            param='West Death Mountain ES',
        ),
    ],
    0x05: [
        change(ChangeWhen.ALWAYS,
            tile(0x101, 0x2E18),  # OWG sign
        ),
        change(ChangeWhen.FLIPPED,
            tile(0x034, 0x3D4A),  # portal
        ),
        change(ChangeWhen.FLIPPED,
            # spiral/mimic ledge hops
            tile(0x139, 0x2C6C),
            tile(0x14B, 0x2C6E),
            tile(0x16B, 0x29F0),
            tile(0x16B, 0x2CEC),
            tile(0x182, 0x29F2),
            tile(0x182, 0x2CEE),

            # floating island
            tile(0x034, 0x21F2),
            tile(0x116, 0x216E),
            tile(0x126, 0x21F4),
            stripe(0x206E, [0x111, 0x113, 0x113, 0x112]),
            stripe_rle_inc(0x111, 0x20EC, 2),
            stripe_rle_inc(0x116, 0x20F0, 3),
            stripe(0x216C, [0x112, 0x116, 0x11C, 0x11D, 0x11E]),
            stripe_rle_inc(0x11C, 0x2170, 3),
            stripe_rle_inc(0x123, 0x21EC, 2),
            stripe_rle_inc(0x144, 0x2364, 4),
            stripe_rle_inc(0x1B3, 0x236C, 2),
            stripe(0x2970, [0x139, 0x14B]),
            arb_tile_copy(0x130, [0x21E2, 0x21F0, 0x22E2, 0x22F0]),
            arb_tile_copy(0x135, [0x2262, 0x2270, 0x2362, 0x2370]),
            arb_tile_copy(0x136, [0x2264, 0x2266, 0x226C, 0x226E]),
            arb_tile_copy(0x137, [0x2268, 0x226A]),
            stripe(0x22E4, [0x13C, 0x13C, 0x13D, 0x13D, 0x13C, 0x13C]),
            param='noglitch',
        ),
        change(ChangeWhen.FLIPPED,  # spiral/mimic bridge connection
            stripe_rle(0x0E3, 0x2BDC, 8),
            stripe_rle(0x14E, 0x2C5C, 2),
            stripe_rle(0x14E, 0x2C64, 4),
            stripe(0x2C60, [0x139, 0x14B]),
            stripe_rle(0x152, 0x2CDC, 2),
            stripe_rle(0x152, 0x2CE4, 4),
            stripe(0x2CE0, [0x16B, 0x182]),
            stripe_rle(0x22E, 0x2D5C, 8),
            stripe_rle(0x230, 0x2DDC, 3),
            stripe_rle(0x230, 0x2DE6, 3),
            stripe_rle(0x2A6, 0x2DE2, 2),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # East Death Mountain WN
            stripe(0x2300, [0x116, 0x124, 0x124, 0x6A7], vertical=True),
            param='East Death Mountain WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # East Death Mountain WS
            tile(0xD1E, 0x3900),
            stripe_rle(0x10A, 0x3980, 4, vertical=True),
            tile(0x333, 0x3B80),
            param='East Death Mountain WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # East Death Mountain EN
            stripe(0x237E, [0x118, 0x127, 0x127, 0x127, 0x6A7], vertical=True),
            param='East Death Mountain EN',
        ),
    ],
    0x07: [
        change(ChangeWhen.FLIPPED,  # TR peg ledge barrier
            stripe(0x251C, [0x163, 0x0152, 0x0152, 0x0152, 0x0152, 0x01F2]),
            stripe(0x259A, [0x163, 0x11C, 0x11D, 0x11D, 0x11D, 0x11D, 0x11E, 0x01F2]),
            stripe(0x2618, [0x163, 0x124, 0x124, 0x124, 0x124, 0x124, 0x140], vertical=True),
            stripe(0x262A, [0x1F2, 0x127, 0x127, 0x127, 0x127, 0x127, 0x150], vertical=True),
            stripe(0x299A, [0x161, 0x141, 0x14E, 0x14E, 0x14E, 0x14E, 0x14F, 0x150]),
            arb_tile_copy(0x125, [0x261C, 0x269A]),
            arb_tile_copy(0x126, [0x2626, 0x26A8]),
            arb_tile_copy(0x139, [0x289A, 0x291C]),
            arb_tile_copy(0x14B, [0x28A8, 0x2926]),
            arb_tile_copy(0x152, [0x2A1E, 0x2A24]),
            tile(0x11C, 0x261A),
            tile(0x11E, 0x2628),
            tile(0x0CE, 0x2896),
            tile(0x16A, 0x28AC),
            tile(0x141, 0x291A),
            tile(0x14F, 0x2928),
            tile(0x161, 0x2A1C),
            tile(0x150, 0x2A26),
            tile(0x21B, 0x2620),  # moved peg
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Death Mountain TR Pegs WN
            stripe(0x2300, [0x116, 0x124, 0x124, 0x124, 0x6A7], vertical=True),
            param='Death Mountain TR Pegs WN',
        ),
    ],
    0x0A: [
        change(ChangeWhen.DISABLED_EDGE,  # Mountain Pass NW
            stripe_rle(0x337, 0x200C, 7),
            tile(0x333, 0x201A),
            stripe_rle(0x10B, 0x201C, 7),
            param='Mountain Pass NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Mountain Pass SE
            stripe(0x2E8E, [0x337, 0x333]),
            stripe(0x2E92, [0x334, 0x336], vertical=True),
            stripe(0x2F14, [0x334, 0x336], vertical=True),
            stripe_rle(0x337, 0x2F96, 9),
            tile(0x333, 0x2FA6),
            stripe_rle(0x10B, 0x2FA8, 8),
            param='Mountain Pass SE',
        ),
    ],
    0x0F: [
        change(ChangeWhen.DISABLED_EDGE,  # Zora Waterfall NE
            tile(0x2FA, 0x2026),
            stripe_rle_inc(0x2F8, 0x2028, 3),
            stripe(0x20A6, [0x2FA, 0x2D1]),
            param='Zora Waterfall NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Zora Waterfall SE
            stripe(0x2EAE, [0x319, OWW_SKIP, 0x316]),
            stripe(0x2F2A, [0x171, 0x166, 0x72E, 0x54C, 0x72F, 0x106, 0x179]),
            stripe(0x2FAA, [0x0C6, 0x171, 0x165, 0x165, 0x165, 0x107, 0x179]),
            param='Zora Waterfall SE',
        ),
    ],
    0x10: [
        change(ChangeWhen.FLIPPED,  # portal
            tile(0x034, 0x2B2E),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lost Woods Pass NW
            stripe(0x208A, [0x082, 0x086, 0x09E], vertical=True),
            stripe(0x208C, [0x083, 0x087, 0x17C], vertical=True),
            param='Lost Woods Pass NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lost Woods Pass NE
            stripe(0x20AE, [0x082, 0x086, 0x09E], vertical=True),
            stripe(0x20B0, [0x083, 0x087, 0x17C], vertical=True),
            param='Lost Woods Pass NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lost Woods Pass SW
            stripe(0x2F8E, [0x0B1, 0x0AF, 0x07E, 0x0B1]),
            param='Lost Woods Pass SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lost Woods Pass SE
            stripe(0x2FA6, [0x0B1, 0x0AF, 0x07E, 0x0B1]),
            param='Lost Woods Pass SE',
        ),
    ],
    0x11: [
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Fortune NE
            stripe(0x2030, [0x000, 0x082, 0x086, 0x09E], vertical=True),
            stripe(0x2032, [0x001, 0x083, 0x087, 0x17C], vertical=True),
            param='Kakariko Fortune NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Fortune EN
            stripe(0x22BE, [0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe(0x233C, [0x034, 0x17C, 0x0AC], vertical=True),
            param='Kakariko Fortune EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Fortune ES
            stripe(0x2B3E, [0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe(0x2C3C, [0x17C, 0x0AC], vertical=True),
            param='Kakariko Fortune ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Fortune SC
            tile(0x3A4, 0x2E9C),
            stripe(0x2F1C, [0x3A5, 0x3A4, OWW_SKIP, 0x034, 0x034]),
            tile(0x3A5, 0x2F9E),
            stripe_rle(0x337, 0x2FA0, 4),
            tile(0x333, 0x2FA8),
            param='Kakariko Fortune SC',
        ),
    ],
    0x12: [
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Pond NE
            tile(0x61B, 0x2012),
            stripe_rle(0x10B, 0x2014, 18),
            stripe(0x2090, [0x333, 0x669]),
            param='Kakariko Pond NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Pond WN
            stripe(0x2280, [0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe_rle(0x034, 0x2382, 2, vertical=True),
            stripe(0x2384, [0x09E, 0x0AD], vertical=True),
            param='Kakariko Pond WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Pond WS
            stripe(0x2B00, [0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe_rle(0x034, 0x2C02, 2, vertical=True),
            stripe(0x2C04, [0x09E, 0x0AD], vertical=True),
            param='Kakariko Pond WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Pond EN
            tile(0xD1E, 0x24BE),
            stripe_rle(0x29C, 0x253E, 6, vertical=True),
            tile(0x333, 0x283E),
            param='Kakariko Pond EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Pond ES
            stripe(0x29BE, [0x0CC, 0xD1E], vertical=True),
            stripe_rle(0x29C, 0x2ABE, 6, vertical=True),
            stripe(0x2BBC, [0x0A1, 0x179, 0x0AC], vertical=True),
            tile(0x333, 0x2DBE),
            param='Kakariko Pond ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Pond SW
            stripe(0x2E96, [0x332, 0x337, 0x333]),
            stripe(0x2F14, [0x332, 0x335]),
            stripe(0x2F90, [0x333, 0x10B, 0x335]),
            param='Kakariko Pond SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Pond SE
            stripe_rle_inc(0x333, 0x2EA2, 2),
            stripe(0x2F24, [0x336, 0x334]),
            tile(0x336, 0x2FA6),
            param='Kakariko Pond SE',
        ),
    ],
    0x13: [
        change(ChangeWhen.DISABLED_EDGE,  # Sanctuary WN
            tile(0xD1E, 0x2480),
            stripe_rle(0x29C, 0x2500, 6, vertical=True),
            tile(0x333, 0x2800),
            param='Sanctuary WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Sanctuary WS
            tile(0xD1E, 0x2A00),
            stripe_rle(0x29C, 0x2A80, 6, vertical=True),
            stripe(0x2C02, [0x0A9, 0x0AD], vertical=True),
            tile(0x333, 0x2D80),
            param='Sanctuary WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Sanctuary EC
            tile(0x333, 0x23BE),
            stripe_rle(0x0F2, 0x243E, 19, vertical=True),
            stripe(0x2C3C, [0x17C, 0x0AC], vertical=True),
            tile(0x333, 0x2DBE),
            param='Sanctuary EC',
        ),
    ],
    0x14: [
        change(ChangeWhen.FLIPPED,  # graveyard ladder
            stripe(0x2422, [0x2F1, 0x184, 0x184], vertical=True),
            stripe(0x2424, [0x2F2, 0x185, 0x185], vertical=True),
            param='noglitch',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Graveyard WC
            tile(0xD1E, 0x2380),
            stripe_rle(0x29C, 0x2400, 19, vertical=True),
            stripe(0x2C02, [0x0A9, 0x0AD], vertical=True),
            tile(0x333, 0x2D80),
            param='Graveyard WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Graveyard EC
            tile(0x333, 0x23BE),
            stripe_rle(0x0F2, 0x243E, 19, vertical=True),
            stripe(0x273C, [0x382, 0x381], vertical=True),
            stripe(0x2B3C, [0x381, OWW_SKIP, 0x17C, 0x0AC], vertical=True),
            param='Graveyard EC',
        ),
    ],
    0x15: [
        change(ChangeWhen.DISABLED_EDGE,  # River Bend WC
            tile(0x333, 0x2380),
            stripe_rle(0x0F2, 0x2400, 19, vertical=True),
            stripe(0x2882, [0x071, 0x034, 0x0E2, 0x034], vertical=True),
            stripe(0x2B82, [0x0A9, 0x0A9, 0x0AD], vertical=True),
            tile(0x0AC, 0x2C84),
            param='River Bend WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # River Bend EN
            tile(0x69E, 0x24BE),
            param='River Bend EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # River Bend EC
            tile(0x333, 0x263E),
            stripe_rle(0x0F2, 0x26BE, 4, vertical=True),
            tile(0x333, 0x28BE),
            param='River Bend EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # River Bend ES
            stripe(0x2B3E, [0x0D5, 0x0CE, 0x0CE, 0x105, 0x105], vertical=True),
            tile(0x100, 0x2C3C),
            stripe(0x2CBA, [0x100, 0x104], vertical=True),
            stripe_rle_inc(0x104, 0x2CBC, 2, vertical=True),
            param='River Bend ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # River Bend SW
            stripe(0x2F0E, [0x0AD, 0x0AC]),
            tile(0x333, 0x2F88),
            stripe_rle(0x10B, 0x2F8A, 5),
            stripe_rle(0x337, 0x2F94, 5),
            tile(0x333, 0x2F9E),
            param='River Bend SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # River Bend SC
            stripe(0x2EA2, [0x1F2, 0x2F6, 0x396, 0x324]),
            stripe(0x2F22, [0x161, 0x1F2, 0x397, 0x3A2, 0x163]),
            stripe(0x2FA2, [0x0C8, 0x161, 0x28F, 0x28F, 0x150]),
            param='River Bend SC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # River Bend SE
            stripe(0x2F2C, [0x99D, 0x141]),
            stripe_rle(0x14E, 0x2F30, 3),
            stripe(0x2FAC, [0x0C8, 0x161, 0x152, 0x152, 0x152, 0x0D5]),
            param='River Bend SE',
        ),
    ],
    0x16: [
        change(ChangeWhen.DISABLED_EDGE,  # Potion Shop WN
            tile(0x69E, 0x2480),
            param='Potion Shop WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Potion Shop WC
            tile(0xD1E, 0x2600),
            stripe_rle(0x29C, 0x2680, 4, vertical=True),
            tile(0x333, 0x2880),
            param='Potion Shop WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Potion Shop WS
            stripe(0x2B00, [0x220, 0x16A, 0x16A, 0x158, 0x158], vertical=True),
            stripe(0x2C02, [0x218, 0x21A, 0x225], vertical=True),
            param='Potion Shop WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Potion Shop EN
            tile(0x69E, 0x233E),
            param='Potion Shop EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Potion Shop EC
            stripe(0x243A, [0x522, 0x126, 0x100, 0x104, 0x105], vertical=True),
            stripe(0x243C, [0x105, 0x0D5, 0x0CE, 0x105, 0x232, 0x235], vertical=True),
            stripe(0x243E, [0x232, 0x237, 0x237, 0x237, 0x235, 0x034], vertical=True),
            param='Potion Shop EC',
        ),
    ],
    0x17: [
        change(ChangeWhen.DISABLED_EDGE,  # Zora Approach NE
            stripe(0x202A, [0x17E, 0x0D1, 0x0D1, 0x0D1, 0x0D2, 0x0D2, 0x179]),
            stripe_rle(0x0C9, 0x20AC, 3),
            stripe(0x20B2, [0x0D0, 0x0D2, 0x179]),
            stripe_rle(0x386, 0x212C, 3),
            stripe(0x2132, [0x0C8, 0x0D0, 0x179]),
            stripe(0x21B2, [0x2ED, 0x23A]),
            param='Zora Approach NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Zora Approach WN
            tile(0x69E, 0x2300),
            param='Zora Approach WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Zora Approach WC
            stripe(0x2400, [0x234, 0x1ED, 0x1ED, 0x1ED, 0x236, 0x034], vertical=True),
            stripe(0x2402, [0x158, 0x220, 0x16A, 0x158, 0x234, 0x236], vertical=True),
            stripe(0x2404, [0x398, 0x125, 0x218, 0x21A, 0x225], vertical=True),
            param='Zora Approach WC',
        ),
    ],
    0x18: [
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko NW
            stripe(0x200E, [0x016, 0x01E, 0x0D6, 0x09D], vertical=True),
            stripe(0x2010, [0x014, 0x01C, 0x04E, 0x09B, 0x09E], vertical=True),
            stripe(0x2012, [0x015, 0x01D, 0x04F, 0x09C, 0x17C], vertical=True),
            stripe(0x2014, [0x016, 0x01E, 0x0D6, 0x09D], vertical=True),
            param='Kakariko NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko NC
            tile(0x016, 0x2026),
            stripe_rle_inc(0x014, 0x2028, 3),
            tile(0x01E, 0x20A6),
            stripe_rle_inc(0x01C, 0x20A8, 3),
            stripe(0x2126, [0x0D6, 0x04E, 0x04F, 0x0D6]),
            tile(0x09D, 0x21A6),
            stripe_rle_inc(0x09B, 0x21A8, 3),
            param='Kakariko NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko NE
            tile(0x332, 0x205E),
            stripe_rle(0x337, 0x2060, 4),
            tile(0x333, 0x2068),
            stripe(0x20DE, [0x335, 0x034, 0x09E, 0x17C]),
            param='Kakariko NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko ES
            stripe(0x38FE, [0xD1E, 0x29C, 0x29C, 0x29C, 0x61B, 0x669], vertical=True),
            stripe(0x39FC, [0x425, 0x5D7, OWW_SKIP, 0x333], vertical=True),
            param='Kakariko ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko SE
            stripe(0x3EEA, [0x337, 0x337, 0x333, 0x10B, 0x10B]),
            stripe(0x3F6E, [0x09E, 0x17C]),
            param='Kakariko SE',
        ),
    ],
    0x1A: [
        change(ChangeWhen.OWLAYOUT,  # rocks for hardlock protection
            stripe_rle_inc(0x2F8, 0x2FBC, 2),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Forgotten Forest NW
            stripe(0x2010, [0x333, 0x10B, 0x10B, 0x337, 0x337, 0x333]),
            param='Forgotten Forest NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Forgotten Forest NE
            stripe(0x2022, [0x337, 0x333, 0x10B]),
            param='Forgotten Forest NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Forgotten Forest ES
            stripe(0x293E, [0xD1E, 0x29C, 0x333], vertical=True),
            param='Forgotten Forest ES',
        ),
    ],
    0x1B: [
        change(ChangeWhen.OWLAYOUT,  # rocks for hardlock protection
            stripe(0x2FFE, [0x39A, 0x39B], vertical=True),
            stripe(0x2F80, [0x2FA, 0x30A, 0x30D], vertical=True),
        ),
        change(ChangeWhen.FLIPPED,
            tile(0x101, 0x2252),  # goal sign
            arb_tile_copy(0x46D, [0x243E, 0x24BC, 0x24BE, 0x253E, 0x2440, 0x24C0, 0x24C2, 0x2540]),  # eye removed

            # new trees
            stripe(0x2DAA, [0x034, 0x4BA, 0x4BB, 0x034], vertical=True),
            stripe(0x2DB0, [0x034, 0x4BA, 0x4BB, 0x034], vertical=True),

            # new HC door
            stripe_rle(0x44F, 0x201C, 2),
            stripe_rle(0x455, 0x209C, 2),
            stripe_rle_inc(0x45A, 0x211A, 4),
            stripe_rle_inc(0x463, 0x219A, 4),
        ),
        change(ChangeWhen.ATGT,
            tile(0x101, 0x222C),  # tower entry sign
            param='swapped',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hyrule Castle WN
            stripe(0x2900, [0xD1E, 0x29C, 0x333], vertical=True),
            param='Hyrule Castle WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hyrule Castle ES
            stripe(0x347E, [0xD1E, 0x29C, 0x29C, 0x333], vertical=True),
            param='Hyrule Castle ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hyrule Castle SW
            stripe_rle_inc(0x333, 0x3E8E, 2),
            stripe(0x3F10, [0x336, 0x334]),
            stripe(0x3F92, [0x336, 0x10B]),
            param='Hyrule Castle SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hyrule Castle SE
            stripe_rle(0x0A5, 0x3F68, 2),
            tile(0x333, 0x3FD4),
            stripe_rle(0x10B, 0x3FD6, 8),
            stripe_rle(0x337, 0x3FE6, 8),
            tile(0x333, 0x3FF6),
            param='Hyrule Castle SE',
        ),
    ],
    0x1D: [
        change(ChangeWhen.DISABLED_EDGE,  # Wooden Bridge NW
            tile(0x46A, 0x2008),
            stripe_rle(0x337, 0x200A, 10),
            tile(0x333, 0x201E),
            stripe(0x208E, [0x09E, 0x17C]),
            param='Wooden Bridge NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Wooden Bridge NC
            stripe(0x2022, [0x1EE, 0x153, 0x156, 0x0C8, 0x0C8]),
            stripe(0x20A2, [0x1EE, 0x2CF, 0x2DB, 0x2D4, 0x0D3]),
            param='Wooden Bridge NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Wooden Bridge NE
            tile(0x163, 0x202C),
            stripe_rle(0x28F, 0x202E, 4),
            tile(0x0D5, 0x2036),
            stripe_rle(0x11D, 0x20AE, 4),
            tile(0x0D5, 0x20B6),
            param='Wooden Bridge NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Wooden Bridge SW
            stripe(0x2F10, [0x034, 0x034, 0x071, 0x034, 0x034, 0x071, 0x034]),
            tile(0x333, 0x2F88),
            stripe_rle(0x10B, 0x2F8A, 6),
            stripe_rle(0x337, 0x2F96, 6),
            tile(0x333, 0x2FA2),
            param='Wooden Bridge SW',
        ),
    ],
    0x1E: [
        change(ChangeWhen.DISABLED_EDGE,  # Eastern Palace SW
            tile(0x218, 0x3E8E),
            stripe(0x3F08, [0x236, 0x234, 0x158, 0x21A, 0x1C2, 0x1C2]),
            stripe(0x3F88, [0x071, 0x236, 0x234, 0x225, 0x1D5, 0x1D5, 0x2B0, 0x106, 0x107]),
            param='Eastern Palace SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Eastern Palace SE
            stripe_rle(0x1C2, 0x3EEE, 2),
            stripe(0x3F68, [0x171, 0x166, 0x225, 0x1D5, 0x1D5, 0x2B0, 0x106, 0x107]),
            stripe(0x3FE8, [0x0C6, 0x171, 0x165, 0x165, 0x165, 0x165, 0x107, 0x0C6]),
            param='Eastern Palace SE',
        ),
    ],
    0x22: [
        change(ChangeWhen.OWLAYOUT,  # rocks for hardlock protection
            tile(0x2B9, 0x203C),
            tile(0x309, 0x203E),
            tile(0x30E, 0x20BE),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Blacksmith WS
            stripe(0x2880, [0xD1E, 0x29C, 0x29C, 0x29C, 0x10A, 0x034], vertical=True),
            stripe(0x2982, [0x3C2, 0x42E, 0x334, 0x336], vertical=True),
            param='Blacksmith WS',
        ),
    ],
    0x25: [
        change(ChangeWhen.DISABLED_EDGE,  # Sand Dunes NW
            tile(0x333, 0x2008),
            stripe_rle(0x10B, 0x200A, 6),
            stripe_rle(0x337, 0x2016, 6),
            tile(0x333, 0x2022),
            tile(0x09E, 0x208E),
            stripe_rle(0x09F, 0x2090, 9),
            param='Sand Dunes NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Sand Dunes WN
            tile(0x163, 0x2380),
            stripe_rle(0x124, 0x2400, 4, vertical=True),
            stripe(0x2600, [0x161, 0x0C8, 0x2D4, 0x2D3], vertical=True),
            param='Sand Dunes WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Sand Dunes SC
            tile(0x0AD, 0x2F10),
            stripe_rle(0x0A5, 0x2F12, 18),
            tile(0x333, 0x2F88),
            stripe_rle(0x10B, 0x2F8A, 11),
            stripe_rle(0x337, 0x2FA0, 10),
            tile(0x333, 0x2FB4),
            param='Sand Dunes SC',
        ),
    ],
    0x28: [
        change(ChangeWhen.DISABLED_EDGE,  # Maze Race ES
            stripe(0x2D3E, [0x0C8, 0x0D3, 0x0CE], vertical=True),
            stripe(0x2E3C, [0x100, 0x104, 0x2B0], vertical=True),
            stripe_rle_inc(0x105, 0x2EBE, 3, vertical=True),
            param='Maze Race ES',
        ),
    ],
    0x29: [
        change(ChangeWhen.FLIPPED,  # bush relocated
            tile(0x034, 0x248A),
            tile(0x036, 0x2386),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Suburb NE
            stripe(0x202A, [0x337, 0x337, 0x333, 0x10B, 0x10B]),
            stripe(0x20AE, [0x09F, 0x17C]),
            param='Kakariko Suburb NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Suburb WS
            stripe(0x2D00, [0x153, 0x1EE, 0x16A, 0x158, 0x166, 0x171], vertical=True),
            stripe(0x2E02, [0x218, 0x21A, 0x225], vertical=True),
            param='Kakariko Suburb WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Kakariko Suburb ES
            tile(0x0B0, 0x29BC),
            stripe(0x2ABE, [0x0D7, 0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe(0x2C3C, [0x17C, 0x0AC], vertical=True),
            param='Kakariko Suburb ES',
        ),
    ],
    0x2A: [
        change(ChangeWhen.DISABLED_EDGE,  # Flute Boy WS
            stripe(0x2B00, [0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe_rle(0x034, 0x2C02, 2, vertical=True),
            param='Flute Boy WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Flute Boy SW
            stripe(0x2E84, [0x333, 0x10B, 0x334]),
            stripe(0x2F08, [0x336, 0x334]),
            stripe(0x2F88, [0x034, 0x336, 0x10B]),
            param='Flute Boy SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Flute Boy SC
            stripe(0x2F1A, [0x0B1, 0x0AF, 0x07E, 0x0B1]),
            tile(0x016, 0x2F9A),
            stripe_rle_inc(0x014, 0x2F9C, 3),
            param='Flute Boy SC',
        ),
    ],
    0x2B: [
        change(ChangeWhen.DISABLED_EDGE,  # Central Bonk Rocks NW
            stripe(0x200E, [0x333, 0x10B, 0x337, 0x333]),
            param='Central Bonk Rocks NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Central Bonk Rocks EN
            stripe(0x25BE, [0x0D5, 0x0CE, 0x0CE, 0x105], vertical=True),
            stripe(0x26BC, [0x15C, 0x174], vertical=True),
            param='Central Bonk Rocks EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Central Bonk Rocks EC
            stripe(0x27BC, [0x522, 0x126], vertical=True),
            tile(0x1F2, 0x27BE),
            stripe_rle(0x127, 0x283E, 5, vertical=True),
            stripe(0x2A3C, [0x14B, 0x182], vertical=True),
            tile(0x150, 0x2ABE),
            param='Central Bonk Rocks EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Central Bonk Rocks ES
            stripe(0x2B3C, [0x0C8, 0x0C8, 0x0DB, 0x034, 0x15C, 0x174], vertical=True),
            stripe(0x2B3E, [0x0C8, 0x0C8, 0x23A, 0x0CE, 0x0CE, 0x106, 0x107], vertical=True),
            stripe(0x2C3A, [0x034, 0x17C, 0x0AC], vertical=True),
            param='Central Bonk Rocks ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Central Bonk Rocks SW
            stripe(0x2F12, [0x0AD, 0x0AC]),
            stripe(0x2F92, [0x337, 0x333, 0x10B]),
            param='Central Bonk Rocks SW',
        ),
    ],
    0x2C: [
        change(ChangeWhen.DISABLED_EDGE,  # Links House NE
            tile(0x333, 0x2014),
            stripe_rle(0x10B, 0x2016, 8),
            stripe_rle(0x337, 0x2026, 8),
            tile(0x333, 0x2036),
            stripe(0x20A8, [0x09E, 0x17C]),
            param='Links House NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Links House WN
            stripe(0x2580, [0x220, 0x16A, 0x16A, 0x158], vertical=True),
            stripe(0x2682, [0x160, 0x172], vertical=True),
            param='Links House WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Links House WC
            tile(0x163, 0x2780),
            stripe(0x2782, [0x398, 0x125], vertical=True),
            stripe_rle(0x124, 0x2800, 5, vertical=True),
            stripe(0x2A02, [0x139, 0x16B], vertical=True),
            tile(0x161, 0x2A80),
            param='Links House WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Links House WS
            stripe(0x2B00, [0x153, 0x153, 0x1EE, 0x16A, 0x16A, 0x166, 0x171], vertical=True),
            stripe(0x2B02, [0x153, 0x153, 0x186, 0x034, 0x160, 0x172], vertical=True),
            stripe(0x2C04, [0x09E, 0x0AD], vertical=True),
            param='Links House WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Links House ES
            stripe(0x2BBE, [0xD1E, 0x29C, 0x29C, 0x333], vertical=True),
            stripe(0x2C3C, [0x17C, 0x0AC], vertical=True),
            param='Links House ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Links House SC
            stripe(0x2E98, [0x167, 0x160, OWW_SKIP, 0x9CF]),
            stripe(0x2F16, [0x171, 0x166, 0x172, 0x15E, 0x174, 0x105, 0x106, 0x107]),
            stripe(0x2F96, [0x0C6, 0x171, 0x165, 0x165, 0x165, 0x0D5, 0x0C5, 0x0C6]),
            param='Links House SC',
        ),
    ],
    0x2D: [
        change(ChangeWhen.DISABLED_EDGE,  # Stone Bridge NC
            tile(0x333, 0x2008),
            stripe_rle(0x10B, 0x200A, 11),
            stripe_rle(0x337, 0x2020, 10),
            tile(0x333, 0x2034),
            tile(0x09E, 0x2090),
            stripe_rle(0x09F, 0x2092, 17),
            tile(0x17C, 0x20B4),
            param='Stone Bridge NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Stone Bridge EN
            stripe(0x23BC, [0x17C, 0x0AC], vertical=True),
            tile(0xD1E, 0x23BE),
            stripe_rle(0x29C, 0x243E, 4, vertical=True),
            tile(0x333, 0x263E),
            param='Stone Bridge EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Stone Bridge EC
            stripe(0x283E, [0x51C, 0x39B, 0x2F8, 0x39A, 0x39B, 0x2F8, 0x39A, 0x39B, 0x69E], vertical=True),
            param='Stone Bridge EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Stone Bridge WC
            stripe(0x28AC, [0xC86, 0x39B, 0x2F8], vertical=True),
            param='Stone Bridge WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Stone Bridge WS
            stripe(0x2B80, [0xD1E, 0x29C, 0x29C, 0x333], vertical=True),
            stripe(0x2C02, [0x09E, 0x0AD], vertical=True),
            param='Stone Bridge WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Stone Bridge SC
            stripe(0x2F18, [0x0AD, 0x0AC]),
            tile(0x333, 0x2F90),
            stripe_rle(0x10B, 0x2F92, 6),
            stripe_rle(0x337, 0x2F9E, 5),
            tile(0x333, 0x2FA8),
            param='Stone Bridge SC',
        ),
    ],
    0x2E: [
        change(ChangeWhen.DISABLED_EDGE,  # Tree Line NW
            stripe(0x2008, [0x1E7, 0x1EB, 0x153, 0x0DC, 0x0DC, 0x0DC, 0x0C8, 0x0D0, 0x0D2]),
            stripe(0x208A, [0x153, 0x178, 0x51D, 0x51D, 0x51D, 0x0CA, 0x0C8]),
            stripe(0x210C, [0x153, 0x0E3, 0x0E3, 0x0E3, 0x0C8]),
            param='Tree Line NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Tree Line WN
            tile(0xD1E, 0x2380),
            stripe(0x2382, [0x09E, 0x0AD], vertical=True),
            stripe_rle(0x29C, 0x2400, 4, vertical=True),
            tile(0x333, 0x2600),
            param='Tree Line WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Tree Line WC
            stripe(0x2800, [0x51C, 0x39B, 0x2F8, 0x39A, 0x39B, 0x2F8, 0x39A, 0x39B, 0x69E], vertical=True),
            param='Tree Line WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Tree Line SC
            stripe(0x2EA2, [0x171, 0x166, 0x2F6, 0x396, 0x39D, 0x303, 0x163]),
            stripe(0x2F22, [0x384, 0x171, 0x166, 0x397, 0x3A2, 0x106, 0x183]),
            stripe(0x2FA2, [0x0C6, 0x0AB, 0x171, 0x165, 0x165, 0x150, 0x153]),
            param='Tree Line SC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Tree Line SE
            stripe_rle(0x14E, 0x2F32, 2),
            stripe(0x2FB0, [0x161, 0x152, 0x152, 0x0D5]),
            param='Tree Line SE',
        ),
    ],
    # 0x2F: [
    #     change(ChangeWhen.FLIPPED,  # portal
    #         tile(0x034, 0x2BB2),
    #     ),
    # ],
    0x2F: [
        change(ChangeWhen.DISABLED_EDGE,  # Eastern Nook NE
            stripe(0x2028, [0x17E, 0x183, 0x153, 0x0DC, 0x0C8, 0x0D0, 0x0D2, 0x0C6]),
            stripe(0x20AA, [0x153, 0x153, 0x0C9, 0x0C8, 0x0C8, 0x0D0, 0x0D2]),
            stripe(0x212C, [0x153, 0x386, 0x0C8, 0x0C8, 0x0D3, 0x0D2]),
            stripe(0x21AE, [0x2E5, 0x2ED, 0x0D3]),
            stripe(0x2230, [0x2E5, 0x53C]),
            param='Eastern Nook NE',
        ),
    ],
    0x30: [
        change(ChangeWhen.FLIPPED,  # portal
            tile(0x034, 0x3D94),
        ),
        change(ChangeWhen.FLIPPED,  # checkerboard cave mods
            stripe_rle(0x0D1, 0x2052, 6),
            stripe_rle(0x0C9, 0x20D2, 6),
            stripe_rle(0x0DC, 0x2152, 6),
            stripe_rle(0x0D1, 0x2266, 6),
            stripe_rle(0x721, 0x22E6, 6),
            stripe_rle(0x0CC, 0x2366, 6),
            stripe_rle(0x384, 0x25E6, 4),
            stripe_rle(0x6B4, 0x2662, 8),
            stripe_rle(0x165, 0x26E0, 9),
            stripe(0x2460, [0x0A3, 0x0D5, 0x0C5, 0x63D, 0x384, 0x0AB, 0x384]),
            stripe(0x2552, [0x6E5, 0x63D, 0x6AB, 0x109, 0x6AA, 0x6AA, 0x6AA, 0x10C, 0x106, 0x107, 0x6AB, 0x384]),
            stripe(0x25D2, [0x6E5, 0x6AB, 0x109, 0x10C, 0x6A7, 0x6A7, 0x6A7, 0x106, 0x107, 0x6AB]),
            stripe(0x2652, [0x6E5, 0x6AB, 0x10C, 0x105, 0x106, 0x165, 0x166, 0x766]),
            stripe(0x24E0, [0x109, 0x0D5, 0x0C5]),
            stripe(0x224C, [0x0DC, 0x0C9, 0x386, 0x759], vertical=True),
            stripe(0x21CE, [0x153, 0x153, 0x153, 0x256, 0x757, 0x759], vertical=True),
            stripe(0x2150, [0x153, 0x178, 0x153, 0x256, 0x6AB, 0x6AB, 0x757, 0x759], vertical=True),
            stripe(0x26D2, [0x6E5, 0x6E5, 0x6E5, 0x759], vertical=True),
            stripe(0x26D6, [0x0D5, 0x0D5, 0x0D5, 0x0D5, 0x1E9], vertical=True),
            stripe(0x26D8, [0x0C4, 0x0CF, 0x302, 0x0C5], vertical=True),
            stripe(0x20DE, [0x0D0, 0x0C8, 0x0CA, 0x0C8, 0x0DB], vertical=True),
            stripe(0x2160, [0x0D0, 0x0C8, 0x0CA, 0x0C8, 0x0DB, 0x09E], vertical=True),
            stripe(0x21E2, [0x0D0, 0x0C8, 0x0CA, 0x0D3, 0x0CE], vertical=True),
            stripe(0x2264, [0x0D0, 0x0C8, 0x302, 0x0C5], vertical=True),
            arb_tile_copy(0x6AB, [0x23D2, 0x23E6, 0x2452, 0x2454, 0x24D4, 0x24E6, 0x26D4, 0x2754, 0x27D4]),
            arb_tile_copy(0x0D2, [0x205E, 0x20E0, 0x2162, 0x21E4, 0x275C]),
            arb_tile_copy(0x17E, [0x2050, 0x20CE]),
            arb_tile_copy(0x183, [0x20D0, 0x214E]),
            arb_tile_copy(0x384, [0x24D8, 0x24EA]),
            arb_tile_copy(0x757, [0x24D2, 0x2854]),
            tile(0x0AB, 0x2352),
            tile(0x171, 0x26DE),
            tile(0x759, 0x28D4),
            param='noglitch',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Desert EC
            stripe(0x357C, [0x1F2, 0x1F9, 0x767], vertical=True),
            stripe(0x357E, [0x158, 0x1F2], vertical=True),
            stripe_rle(0x201, 0x367E, 7, vertical=True),
            stripe(0x397C, [0x1E5, 0x96E], vertical=True),
            tile(0x150, 0x39FE),
            param='Desert EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Desert ES
            stripe(0x3A7A, [0x161, 0x0C8, 0x0C8, 0x0C8, 0x6E7], vertical=True),
            stripe(0x3A7C, [0x96A, 0x161, 0x0C8, 0x0C8, 0x0C8, 0x6E7, 0x593, 0x599, 0x2B0], vertical=True),
            stripe(0x3A7E, [0x1F2, 0x96A, 0x161, 0x0C8, 0x0C8, 0x0D3, 0x2FD], vertical=True),
            stripe_rle_inc(0x105, 0x3DFE, 3, vertical=True),
            param='Desert ES',
        ),
    ],
    0x32: [
        change(ChangeWhen.FLIPPED,  # cave 45 mods
            tile(0x1D5, 0x2486),
            tile(0x165, 0x2506),
            tile(0x166, 0x2508),
            tile(0x220, 0x278C),
            tile(0x75E, 0x299A),
            tile(0x0AB, 0x299C),
            tile(0xBDB, 0x2C0A),
            stripe(0x2586, [0x0C6, 0x171, 0x166]),
            stripe(0x2A1A, [0x75F, 0x0C6, 0x1E5, 0x77E]),
            stripe(0x2A9A, [0x775, 0x1E5, 0x77E, 0x106, 0x165]),
            stripe(0x2B1A, [0x75F, 0x77E, 0x106, 0x107, 0x0C6]),
            stripe(0x2B9C, [0x0D5, 0x0C5, 0x0C6]),
            stripe_rle(0x09F, 0x2812, 4),
            stripe_rle(0x6E1, 0x2890, 4),
            stripe_rle(0x034, 0x29A2, 4),
            stripe_rle(0x0C6, 0x2608, 4, vertical=True),
            stripe_rle(0x21C, 0x260A, 4, vertical=True),
            arb_tile_copy(0x167, [0x2488, 0x250A, 0x258C, 0x2A28, 0x2AAA, 0x2B2C, 0x2BAE]),
            arb_tile_copy(0x160, [0x248A, 0x250C, 0x2A2A, 0x2AAC, 0x2B2E]),
            arb_tile_copy(0x17C, [0x270E, 0x2790, 0x281A, 0x289C, 0x291E, 0x29A0]),
            arb_tile_copy(0x1FF, [0x278E, 0x2810, 0x289A, 0x291C, 0x299E]),
            arb_tile_copy(0x757, [0x280E, 0x2898, 0x291A]),
            arb_tile_copy(0x034, [0x281C, 0x289E, 0x2920]),
            arb_tile_copy(0x759, [0x288E, 0x2918, 0x2B9A]),
            arb_tile_copy(0x2EC, [0x2A8A, 0x2A8E, 0x2A92, 0x2A94, 0x2A96, 0x2C0C]),
            arb_tile_copy(0x789, [0x2B0A, 0x2B0E, 0x2B14, 0x2B94]),
            arb_tile_copy(0x2EB, [0x2B12, 0x2B16, 0x2C8C, 0x2C94]),
            arb_tile_copy(0xBDC, [0x2B8A, 0x2B8E, 0x2C0E, 0x2C14]),
            param='noglitch',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Flute Boy Approach NW
            stripe_rle(0x034, 0x2008, 2),
            stripe(0x2086, [0x333, 0x10B, 0x337, 0x333]),
            stripe(0x2108, [0x09E, 0x17C]),
            param='Flute Boy Approach NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Flute Boy Approach NC
            tile(0x01E, 0x201A),
            stripe_rle_inc(0x01C, 0x201C, 3),
            stripe(0x209A, [0x0D6, 0x04E, 0x04F, 0x0D6]),
            tile(0x09D, 0x211A),
            stripe_rle_inc(0x09B, 0x211C, 3),
            param='Flute Boy Approach NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Flute Boy Approach EC
            tile(0x0D5, 0x22BE),
            stripe_rle(0x0CE, 0x233E, 22, vertical=True),
            stripe(0x26BC, [0x17C, 0x0AC], vertical=True),
            stripe(0x2D3C, [0x034, 0x100, 0x104, 0x2B0], vertical=True),
            stripe_rle_inc(0x105, 0x2E3E, 3, vertical=True),
            param='Flute Boy Approach EC',
        ),
    ],
    # 0x33: [
    #     change(ChangeWhen.FLIPPED,  # portal
    #         tile(0x034, 0x22A8),
    #     ),
    # ],
    0x33: [
        change(ChangeWhen.DISABLED_EDGE,  # C Whirlpool NW
            stripe(0x2012, [0x337, 0x333, 0x10B]),
            stripe(0x2092, [0x09E, 0x17C]),
            param='C Whirlpool NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # C Whirlpool WC
            tile(0x220, 0x2280),
            stripe_rle(0x16A, 0x2300, 22, vertical=True),
            stripe(0x2682, [0x09E, 0x0A9], vertical=True),
            stripe(0x2D82, [0x218, 0x21A, 0x225], vertical=True),
            stripe(0x2E00, [0x158, 0x166, 0x171], vertical=True),
            param='C Whirlpool WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # C Whirlpool EN
            tile(0xD1E, 0x243E),
            stripe(0x24BC, [0x381, 0x0E2, 0x2EA, 0x2D2, 0x2D2, 0x2E8], vertical=True),
            stripe_rle(0x29C, 0x24BE, 5, vertical=True),
            tile(0x333, 0x273E),
            param='C Whirlpool EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # C Whirlpool EC
            stripe_rle(0x2F8, 0x27BE, 6, vertical=True),
            param='C Whirlpool EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # C Whirlpool ES
            stripe(0x2ABC, [0x2C7, 0x2D2, 0x2C8, 0x677, 0x682, 0x682], vertical=True),
            tile(0xD1E, 0x2ABE),
            stripe_rle(0x29C, 0x2B3E, 6, vertical=True),
            tile(0x333, 0x2E3E),
            param='C Whirlpool ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # C Whirlpool SC
            tile(0x333, 0x2F94),
            stripe_rle(0x10B, 0x2F96, 8),
            stripe_rle(0x337, 0x2FA6, 8),
            tile(0x333, 0x2FB6),
            param='C Whirlpool SC',
        ),
    ],
    0x34: [
        change(ChangeWhen.DISABLED_EDGE,  # Statues NC
            stripe(0x2016, [0x0C6, 0x384, 0x0C6, 0x0C6, 0x0C6, 0x0D5, 0x0C5, 0x0C6]),
            stripe(0x2096, [0x384, 0x17E, 0x0D1, 0x0D1, 0xC06, 0x0D5, 0x0C5, 0x384]),
            stripe(0x2116, [0x17E, 0x183, 0x51D, 0x51D, 0x1EC, 0x1E9, 0x0D0, 0x0D2]),
            stripe(0x2198, [0x153, 0x0E3, 0x0E3, 0x0C8, 0x0CA, 0x0C8]),
            stripe(0x221E, [0x0DB, 0x0C8]),
            param='Statues NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Statues WN
            tile(0xD1E, 0x2400),
            stripe_rle(0x29C, 0x2480, 5, vertical=True),
            stripe(0x2582, [0xAFD, 0xAFF, 0xAFF, 0xAFE], vertical=True),
            tile(0x333, 0x2700),
            param='Statues WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Statues WC
            stripe_rle(0x2F8, 0x2780, 6, vertical=True),
            param='Statues WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Statues WS
            tile(0xD1E, 0x2A80),
            tile(0xB01, 0x2A82),
            stripe_rle(0x29C, 0x2B00, 6, vertical=True),
            stripe_rle_inc(0xAFF, 0x2B02, 2, vertical=True),
            tile(0x333, 0x2E00),
            param='Statues WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Statues SC
            tile(0x333, 0x2F86),
            stripe_rle(0x10B, 0x2F88, 12),
            stripe_rle(0x337, 0x2FA0, 11),
            tile(0x333, 0x2FB6),
            param='Statues SC',
        ),
    ],
    0x35: [
        change(ChangeWhen.FLIPPED,
            tile(0x034, 0x2F56),  # portal
        ),
        change(ChangeWhen.FLIPPED,  # lake hylia island ladder
            stripe(0x2BB0, [0x2F1, 0x184, 0x392, 0x394], vertical=True),
            stripe(0x2BB2, [0x2F2, 0x185, 0x393, 0x395], vertical=True),
            param='noglitch',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lake Hylia NW
            tile(0x333, 0x2010),
            stripe_rle(0x10B, 0x2012, 6),
            stripe_rle(0x337, 0x201E, 5),
            tile(0x333, 0x2028),
            stripe(0x2098, [0x09E, 0x17C]),
            param='Lake Hylia NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lake Hylia NC
            stripe(0x2064, [0x1EE, 0x153, 0x0C9, 0x0C9, 0x0CA, 0x0CA]),
            stripe(0x20E4, [0x1EE, 0x153, 0x156, 0x156, 0x0C8, 0x0CA]),
            stripe(0x2164, [0x1EE, 0x2CF, 0x2DB, 0x2DB, 0x2D4, 0x0D3]),
            param='Lake Hylia NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lake Hylia NE
            stripe(0x2070, [0x163, 0x9AF, 0x9AF, 0x0D5]),
            stripe(0x20F2, [0x11D, 0x11D, 0x0D5]),
            param='Lake Hylia NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lake Hylia WS
            stripe(0x3A80, [0x2EB, 0x667], vertical=True),
            stripe(0x3A82, [0x667, 0x38A, 0x1EE, 0x328, 0x328, 0x328, 0x328, 0x158, 0x166, 0x171], vertical=True),
            stripe_rle(0x532, 0x3B80, 5, vertical=True),
            stripe(0x3D84, [0x319, 0x666, 0x225], vertical=True),
            stripe(0x3E00, [0x6A7, 0x165, 0x0C6], vertical=True),
            param='Lake Hylia WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lake Hylia EC
            stripe(0x36FE, [0x0D2, 0x0D0, 0x0CA, 0x0CA, 0x0D3, 0x12D, 0x12D, 0x12D, 0x105, 0x105], vertical=True),
            stripe_rle(0x2CD, 0x397C, 3, vertical=True),
            stripe(0x3AFC, [0x303, 0x2B0], vertical=True),
            param='Lake Hylia EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Lake Hylia ES
            stripe(0x3BFC, [0x2E1, 0x2E6], vertical=True),
            tile(0x1F2, 0x3BFE),
            stripe_rle(0x786, 0x3C7E, 4, vertical=True),
            stripe(0x3E7E, [0x201, 0x6A7], vertical=True),
            tile(0x74E, 0x3EFC),
            param='Lake Hylia ES',
        ),
    ],
    0x37: [
        change(ChangeWhen.DISABLED_EDGE,  # Ice Cave SW
            stripe_rle(0x502, 0x2F8E, 3),
            param='Ice Cave SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Ice Cave SE
            stripe(0x2E9C, [0x315, OWW_SKIP, 0x2E6, 0x2E7, 0x2E0, OWW_SKIP, 0x2E0, 0x2E7, 0x306]),
            stripe(0x2F1A, [0x161, 0x31D]),
            stripe_rle(0x321, 0x2F1E, 14),
            stripe(0x2F9A, [0x0C8, 0x161]),
            stripe_rle(0x152, 0x2F9E, 14),
            tile(0x0D5, 0x2FBA),
            param='Ice Cave SE',
        ),
    ],
    0x3A: [
        change(ChangeWhen.FLIPPED,  # bombos tablet ladder
            tile(0x964, 0x2984),
            tile(0x17E, 0x2986),
            stripe_rle(0x184, 0x2A04, 4, vertical=True),
            stripe_rle(0x185, 0x2A06, 4, vertical=True),
            param='noglitch',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Desert Pass WC
            tile(0x163, 0x2580),
            stripe(0x2582, [0x16E, 0x966], vertical=True),
            stripe_rle(0x71C, 0x2600, 7, vertical=True),
            stripe_rle_inc(0x969, 0x2902, 2, vertical=True),
            tile(0x161, 0x2980),
            param='Desert Pass WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Desert Pass WS
            stripe(0x2A00, [0x163, 0x150, 0x153, 0x153, 0x1EE, 0x328, 0x328, 0x158, 0x166, 0x171,], vertical=True),
            stripe(0x2A02, [0x150, 0x153, 0x153, 0x153, 0x53F, 0x2E5, OWW_SKIP, 0x666, 0x225,], vertical=True),
            param='Desert Pass WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Desert Pass EC
            stripe(0x26BA, [0x0D2, 0x0D0, 0x0D3, 0x0C4, 0x0C4, 0x0C4, 0x106, 0x107, 0x0AB], vertical=True),
            stripe(0x26BC, [0x6AB, 0x0D2], vertical=True),
            stripe_rle(0x6AB, 0x26BE, 8, vertical=True),
            stripe_rle(0x0C5, 0x27BC, 4, vertical=True),
            stripe(0x2838, [0x0D3, 0x0CE, 0x0CE, 0x105], vertical=True),
            tile(0x034, 0x28B4),
            stripe(0x29BC, [0x107, 0x6AB], vertical=True),
            param='Desert Pass EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Desert Pass ES
            stripe(0x2C3A, [0x0D2, 0x0D0, 0x0CA, 0x0CA, 0x0D3, 0x0CE, 0x2B0], vertical=True),
            stripe(0x2C3C, [0x6AB, 0x0D2, 0x0D0, 0x0D3, 0x0C4, 0x0C4, 0x106, 0x107], vertical=True),
            stripe(0x2C3E, [0x6AB, 0x6AB, 0x0D2, 0x0C5, 0x0C5, 0x0C5, 0x107, 0x6AB], vertical=True),
            param='Desert Pass ES',
        ),
    ],
    0x3B: [
        change(ChangeWhen.DISABLED_EDGE,  # Dam NC
            tile(0x333, 0x2014),
            stripe_rle(0x10B, 0x2016, 8),
            stripe_rle(0x337, 0x2026, 8),
            tile(0x333, 0x2036),
            param='Dam NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dam WC
            stripe(0x2680, [0x0C6, 0x17E], vertical=True),
            stripe(0x2682, [0x17E, 0x183, 0x1EE, 0x15B, 0x15B, 0x15B, 0x166, 0x171], vertical=True),
            stripe_rle(0x21C, 0x2780, 4, vertical=True),
            stripe(0x2804, [0x1EE, 0x16A, 0x16A, 0x158], vertical=True),
            stripe(0x2980, [0x171, 0x0C6], vertical=True),
            param='Dam WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dam WS
            stripe(0x2C00, [0x0C6, 0x17E], vertical=True),
            stripe(0x2C02, [0x17E, 0x183, 0x1EE, 0x15B, 0x15B, 0x166, 0x171, 0x384], vertical=True),
            stripe_rle(0x21C, 0x2D00, 3, vertical=True),
            stripe(0x2D84, [0x1EE, 0x16A, 0x158, 0x166, 0x171], vertical=True),
            stripe(0x2E06, [0x218, 0x21A, 0x225], vertical=True),
            stripe(0x2E80, [0x171, 0x0C6, 0x0C6], vertical=True),
            param='Dam WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dam EC
            tile(0x333, 0x21BE),
            stripe_rle(0x0F2, 0x223E, 24, vertical=True),
            tile(0x333, 0x2E3E),
            param='Dam EC',
        ),
    ],
    0x3C: [
        change(ChangeWhen.DISABLED_EDGE,  # South Pass NC
            tile(0x333, 0x2006),
            stripe_rle(0x10B, 0x2008, 12),
            stripe_rle(0x337, 0x2020, 11),
            tile(0x333, 0x2036),
            param='South Pass NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # South Pass WC
            tile(0xD1E, 0x2180),
            stripe_rle(0x29C, 0x2200, 24, vertical=True),
            tile(0x333, 0x2E00),
            param='South Pass WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # South Pass ES
            stripe(0x2A3A, [0x2EC, 0x2F4, 0x2F0, 0x0C8, 0x2ED], vertical=True),
            tile(0x0CF, 0x2AB6),
            stripe(0x2ABC, [0x2EB, 0x2F4, 0x2F0, 0x0D3, 0x2FD, 0x2FD, 0x2FD], vertical=True),
            stripe(0x2ABE, [0x2E5, 0x2EB, 0x2F4, 0x2E4, 0x2E4, 0x2E4, 0x2E4, 0x6A7, 0x165, 0x0C6], vertical=True),
            stripe(0x2DBA, [0x593, 0x599, 0x2B0], vertical=True),
            stripe_rle_inc(0x105, 0x2E3C, 3, vertical=True),
            param='South Pass ES',
        ),
    ],
    0x3F: [
        change(ChangeWhen.OWLAYOUT,  # C terrain
            stripe_rle_inc(0x75C, 0x2A9A, 2, vertical=True),
            stripe(0x2A22, [0x752, 0x753, 0x2E5]),
            stripe(0x2A9E, [0x774, 0x6E1, 0x757, 0x6E3, 0x2E5]),
            stripe(0x2B1E, [0x76E, 0x2E5, 0x759, 0x779]),
            stripe(0x2B9E, [0x76C, 0x2EC, 0x6F5, 0x705]),
            stripe(0x2C1E, [0x704, 0x6F6, 0x6F7, 0x6E3]),
            stripe(0x2CA2, [0x762, 0x773]),
            arb_tile_copy(0x2EC, [0x29A4, 0x2C16]),
            tile(0x75E, 0x2B9A),
            tile(0x76F, 0x2C1A),
            param='lw',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Octoballoon NW
            stripe_rle(0x502, 0x200E, 3),
            param='Octoballoon NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Octoballoon NE
            stripe(0x201A, [0x105, 0x163]),
            stripe_rle(0x28F, 0x201E, 14),
            tile(0x0D5, 0x203A),
            stripe(0x209A, [0x163, 0x301]),
            stripe_rle(0x2E7, 0x209E, 14),
            tile(0x0D5, 0x20BA),
            param='Octoballoon NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Octoballoon WC
            tile(0x306, 0x211C),
            stripe(0x2680, [0x17E, 0x183, 0x153, 0x153, 0x1EE, 0x131, 0x131, 0x131, 0x158, 0x158], vertical=True),
            stripe_rle(0x2C4, 0x2902, 3, vertical=True),
            stripe(0x2A82, [0x2F6, 0x225], vertical=True),
            param='Octoballoon WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Octoballoon WS
            tile(0x163, 0x2B80),
            stripe(0x2B82, [0x304, 0x306], vertical=True),
            stripe_rle(0x2FC, 0x2C00, 5, vertical=True),
            tile(0x6A7, 0x2E80),
            param='Octoballoon WS',
        ),
    ],
    0x40: [
        change(ChangeWhen.DISABLED_EDGE,  # Skull Woods EN
            tile(0x7BB, 0x23FC),
            tile(0x848, 0x23FE),
            stripe_rle(0x7F5, 0x247C, 3, vertical=True),
            stripe_rle(0x849, 0x247E, 3, vertical=True),
            param='Skull Woods EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Skull Woods SW
            stripe_rle_inc(0x7CC, 0x3E0E, 2),
            stripe(0x3E8A, [0x841, 0x83E, 0x7D1, 0x842, 0x7B1, 0x800, 0x7D2, 0x7CF]),
            stripe(0x3F0A, [0x7A7, 0x7A5, 0x7A6, 0x7A7, 0x7A5, 0x7A6, 0x7DF, 0x794]),
            stripe(0x3F8A, [0x7AE, 0x7AC, 0x7AD, 0x7AE, 0x7AC, 0x7AD, 0x7AF, 0x7AA]),
            param='Skull Woods SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Skull Woods SC
            stripe(0x3EAE, [0x841, 0x83E, 0x821, 0x7D2, 0x84B]),
            stripe(0x3F2E, [0x7A7, 0x7A5, 0x7A6, 0x83A, 0x84B]),
            stripe(0x3FAE, [0x7AE, 0x7AC, 0x7AD, 0x7AF, 0x84B]),
            param='Skull Woods SC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Skull Woods SE
            stripe(0x3D6E, [0x337, 0x333]),
            stripe(0x3FF0, [0x7AF, 0x7BE]),
            param='Skull Woods SE',
        ),
    ],
    0x42: [
        change(ChangeWhen.DISABLED_EDGE,  # Dark Lumberjack WN
            stripe(0x2300, [0x00A, 0x014, 0x01C, 0x009, 0x013, 0x00A], vertical=True),
            stripe(0x2302, [0x00B, 0x015, 0x01D, 0x0D8, 0x094], vertical=True),
            stripe(0x2304, [0x00D, 0x017, 0x076, 0x0D9, 0x095], vertical=True),
            param='Dark Lumberjack WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Lumberjack SW
            stripe_rle_inc(0x333, 0x2F0C, 2),
            tile(0x336, 0x2F8E),
            stripe_rle(0x10B, 0x2F90, 13),
            param='Dark Lumberjack SW',
        ),
    ],
    0x43: [
        change(ChangeWhen.ATGT,
            tile(0x101, 0x2550),  # gt entry sign
            param='vanilla',
        ),
        change(ChangeWhen.ATGT,  # gt entrance auto-opened
            stripe(0x235E, [0x8D5, 0x8E3, 0xE90, 0xE96, 0xE96, 0xE94], vertical=True),
            stripe(0x2360, [0x8D6, 0x8E4, 0xE91, 0xE97, 0xE97, 0xE95], vertical=True),
            param='swapped',
        ),
        change(ChangeWhen.FLIPPED,  # portal
            tile(0x212, 0x2BE0),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # West Dark Death Mountain EN
            stripe(0x237E, [0x118, 0x127, 0x127, 0x6A7], vertical=True),
            param='West Dark Death Mountain EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # West Dark Death Mountain ES
            tile(0xD1E, 0x397E),
            stripe_rle(0x10A, 0x39FE, 4, vertical=True),
            tile(0x333, 0x3BFE),
            param='West Dark Death Mountain ES',
        ),
    ],
    0x45: [
        change(ChangeWhen.FLIPPED,  # portal
            tile(0x239, 0x3D4A),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # East Dark Death Mountain WN
            stripe(0x2300, [0x116, 0x124, 0x124, 0x6A7], vertical=True),
            param='East Dark Death Mountain WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # East Dark Death Mountain WS
            tile(0xD1E, 0x3900),
            stripe_rle(0x10A, 0x3980, 4, vertical=True),
            tile(0x333, 0x3B80),
            param='East Dark Death Mountain WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # East Dark Death Mountain EN
            stripe(0x237E, [0x118, 0x127, 0x127, 0x127, 0x6A7], vertical=True),
            param='East Dark Death Mountain EN',
        ),
    ],
    0x47: [
        change(ChangeWhen.FLIPPED,  # portals
            tile(0x239, 0x269E),
            tile(0x239, 0x26A4),
        ),
        change(ChangeWhen.FLIPPED,  # turtle tail hop
            tile(0x398, 0x25A0),
            tile(0x522, 0x25A2),
            tile(0x125, 0x2620),
            tile(0x126, 0x2622),
            param='noglitch',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Turtle Rock WN
            stripe(0x2300, [0x116, 0x124, 0x124, 0x124, 0x6A7], vertical=True),
            param='Turtle Rock WN',
        ),
    ],
    0x4A: [
        change(ChangeWhen.DISABLED_EDGE,  # Bumper Cave NW
            stripe_rle(0x337, 0x200C, 7),
            tile(0x333, 0x201A),
            stripe_rle(0x10B, 0x201C, 7),
            param='Bumper Cave NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Bumper Cave SE
            stripe(0x2E8E, [0x337, 0x333]),
            stripe(0x2E92, [0x334, 0x336], vertical=True),
            stripe(0x2F14, [0x334, 0x336], vertical=True),
            stripe_rle(0x337, 0x2F96, 9),
            tile(0x333, 0x2FA6),
            stripe_rle(0x10B, 0x2FA8, 8),
            param='Bumper Cave SE',
        ),
    ],
    0x4F: [
        change(ChangeWhen.DISABLED_EDGE,  # Catfish SE
            stripe(0x2EAE, [0x319, OWW_SKIP, 0x316]),
            stripe(0x2F2A, [0x171, 0x166, 0x72E, 0x54C, 0x72F, 0x106, 0x179]),
            stripe(0x2FAA, [0x0C6, 0x171, 0x165, 0x165, 0x165, 0x107, 0x179]),
            param='Catfish SE',
        ),
    ],
    0x50: [
        change(ChangeWhen.FLIPPED,  # portal
            tile(0x20F, 0x2B2E),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Skull Woods Pass NW
            stripe(0x208A, [0x082, 0x086, 0x09E], vertical=True),
            stripe(0x208C, [0x083, 0x087, 0x17C], vertical=True),
            param='Skull Woods Pass NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Skull Woods Pass NE
            stripe(0x20AE, [0x082, 0x086, 0x09E], vertical=True),
            stripe(0x20B0, [0x083, 0x087, 0x17C], vertical=True),
            param='Skull Woods Pass NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Skull Woods Pass SW
            stripe(0x2F8E, [0x0B1, 0x0AF, 0x07E, 0x0B1]),
            param='Skull Woods Pass SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Skull Woods Pass SE
            stripe(0x2FA6, [0x0B1, 0x0AF, 0x07E, 0x0B1]),
            param='Skull Woods Pass SE',
        ),
    ],
    0x51: [
        change(ChangeWhen.DISABLED_EDGE,  # Dark Fortune NE
            stripe(0x2030, [0x000, 0x082, 0x086, 0x09E], vertical=True),
            stripe(0x2032, [0x001, 0x083, 0x087, 0x17C], vertical=True),
            param='Dark Fortune NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Fortune EN
            stripe(0x22BE, [0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe(0x233C, [0x034, 0x17C, 0x0AC], vertical=True),
            param='Dark Fortune EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Fortune ES
            stripe(0x2B3E, [0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe(0x2C3C, [0x17C, 0x0AC], vertical=True),
            param='Dark Fortune ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Fortune SC
            tile(0x3A4, 0x2E9C),
            stripe(0x2F1C, [0x3A5, 0x3A4, OWW_SKIP, 0x034, 0x034]),
            tile(0x3A5, 0x2F9E),
            stripe_rle(0x337, 0x2FA0, 4),
            tile(0x333, 0x2FA8),
            param='Dark Fortune SC',
        ),
    ],
    0x52: [
        change(ChangeWhen.DISABLED_EDGE,  # Outcast Pond NE
            tile(0x61B, 0x2012),
            stripe_rle(0x10B, 0x2014, 18),
            stripe(0x2090, [0x333, 0x669]),
            param='Outcast Pond NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Outcast Pond WN
            stripe(0x2280, [0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe_rle(0x034, 0x2382, 2, vertical=True),
            stripe(0x2384, [0x09E, 0x0AD], vertical=True),
            param='Outcast Pond WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Outcast Pond WS
            stripe(0x2B00, [0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe_rle(0x034, 0x2C02, 2, vertical=True),
            stripe(0x2C04, [0x09E, 0x0AD], vertical=True),
            param='Outcast Pond WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Outcast Pond EN
            tile(0xD1E, 0x24BE),
            stripe_rle(0x29C, 0x253E, 6, vertical=True),
            tile(0x333, 0x283E),
            param='Outcast Pond EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Outcast Pond ES
            stripe(0x29BE, [0x0CC, 0xD1E], vertical=True),
            stripe_rle(0x29C, 0x2ABE, 6, vertical=True),
            stripe(0x2BBC, [0x0A1, 0x179, 0x0AC], vertical=True),
            tile(0x333, 0x2DBE),
            param='Outcast Pond ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Outcast Pond SW
            stripe(0x2E96, [0x332, 0x337, 0x333]),
            stripe(0x2F14, [0x332, 0x335]),
            stripe(0x2F90, [0x333, 0x10B, 0x335]),
            param='Outcast Pond SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Outcast Pond SE
            stripe_rle_inc(0x333, 0x2EA2, 2),
            stripe(0x2F24, [0x336, 0x334]),
            tile(0x336, 0x2FA6),
            param='Outcast Pond SE',
        ),
    ],
    0x53: [
        change(ChangeWhen.DISABLED_EDGE,  # Dark Chapel WN
            tile(0xD1E, 0x2480),
            stripe_rle(0x29C, 0x2500, 6, vertical=True),
            tile(0x333, 0x2800),
            param='Dark Chapel WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Chapel WS
            tile(0xD1E, 0x2A00),
            stripe_rle(0x29C, 0x2A80, 6, vertical=True),
            stripe(0x2C02, [0x0A9, 0x0AD], vertical=True),
            tile(0x333, 0x2D80),
            param='Dark Chapel WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Chapel EC
            tile(0x333, 0x23BE),
            stripe_rle(0x0F2, 0x243E, 19, vertical=True),
            stripe(0x2C3C, [0x17C, 0x0AC], vertical=True),
            tile(0x333, 0x2DBE),
            param='Dark Chapel EC',
        ),
    ],
    0x54: [
        change(ChangeWhen.DISABLED_EDGE,  # Dark Graveyard WC
            tile(0xD1E, 0x2380),
            stripe_rle(0x29C, 0x2400, 19, vertical=True),
            stripe(0x2C02, [0x0A9, 0x0AD], vertical=True),
            tile(0x333, 0x2D80),
            param='Dark Graveyard WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Graveyard EC
            tile(0x333, 0x23BE),
            stripe_rle(0x0F2, 0x243E, 19, vertical=True),
            stripe(0x273C, [0x382, 0x381], vertical=True),
            stripe(0x2B3C, [0x381, OWW_SKIP, 0x17C, 0x0AC], vertical=True),
            param='Dark Graveyard EC',
        ),
    ],
    0x55: [
        change(ChangeWhen.DISABLED_EDGE,  # Qirn Jump WC
            tile(0x333, 0x2380),
            stripe_rle(0x0F2, 0x2400, 19, vertical=True),
            stripe(0x2882, [0x071, 0x034, 0x0E2, 0x034], vertical=True),
            stripe(0x2B82, [0x0A9, 0x0A9, 0x0AD], vertical=True),
            tile(0x0AC, 0x2C84),
            param='Qirn Jump WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Qirn Jump EN
            tile(0x69E, 0x24BE),
            param='Qirn Jump EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Qirn Jump EC
            tile(0x333, 0x263E),
            stripe_rle(0x0F2, 0x26BE, 4, vertical=True),
            tile(0x333, 0x28BE),
            param='Qirn Jump EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Qirn Jump ES
            stripe(0x2B3E, [0x0D5, 0x0CE, 0x0CE, 0x105, 0x105], vertical=True),
            tile(0x100, 0x2C3C),
            stripe(0x2CBA, [0x100, 0x104], vertical=True),
            stripe_rle_inc(0x104, 0x2CBC, 2, vertical=True),
            param='Qirn Jump ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Qirn Jump SW
            stripe(0x2F0E, [0x0AD, 0x0AC]),
            tile(0x333, 0x2F88),
            stripe_rle(0x10B, 0x2F8A, 5),
            stripe_rle(0x337, 0x2F94, 5),
            tile(0x333, 0x2F9E),
            param='Qirn Jump SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Qirn Jump SC
            stripe(0x2EA2, [0x1F2, 0x2F6, 0x396, 0x324]),
            stripe(0x2F22, [0x161, 0x1F2, 0x397, 0x3A2, 0x163]),
            stripe(0x2FA2, [0x0C8, 0x161, 0x28F, 0x28F, 0x150]),
            param='Qirn Jump SC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Qirn Jump SE
            stripe(0x2F2C, [0x99D, 0x141]),
            stripe_rle(0x14E, 0x2F30, 3),
            stripe(0x2FAC, [0x0C8, 0x161, 0x152, 0x152, 0x152, 0x0D5]),
            param='Qirn Jump SE',
        ),
    ],
    0x56: [
        change(ChangeWhen.DISABLED_EDGE,  # Dark Witch WN
            tile(0x69E, 0x2480),
            param='Dark Witch WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Witch WC
            tile(0xD1E, 0x2600),
            stripe_rle(0x29C, 0x2680, 4, vertical=True),
            tile(0x333, 0x2880),
            param='Dark Witch WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Witch WS
            stripe(0x2B00, [0x220, 0x16A, 0x16A, 0x158, 0x158], vertical=True),
            stripe(0x2C02, [0x218, 0x21A, 0x225], vertical=True),
            param='Dark Witch WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Witch EN
            tile(0x69E, 0x233E),
            param='Dark Witch EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Witch EC
            stripe(0x243A, [0x522, 0x126, 0x100, 0x104, 0x105], vertical=True),
            stripe(0x243C, [0x105, 0x0D5, 0x0CE, 0x105, 0x232, 0x235], vertical=True),
            stripe(0x243E, [0x232, 0x237, 0x237, 0x237, 0x235, 0x034], vertical=True),
            param='Dark Witch EC',
        ),
    ],
    0x57: [
        change(ChangeWhen.DISABLED_EDGE,  # Catfish Approach NE
            stripe(0x202A, [0x17E, 0x0D1, 0x0D1, 0x0D1, 0x0D2, 0x0D2, 0x179]),
            stripe_rle(0x0C9, 0x20AC, 3),
            stripe(0x20B2, [0x0D0, 0x0D2, 0x179]),
            stripe_rle(0x386, 0x212C, 3),
            stripe(0x2132, [0x0C8, 0x0D0, 0x179]),
            stripe(0x21B2, [0x2ED, 0x23A]),
            param='Catfish Approach NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Catfish Approach WN
            tile(0x69E, 0x2300),
            param='Catfish Approach WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Catfish Approach WC
            stripe(0x2400, [0x234, 0x1ED, 0x1ED, 0x1ED, 0x236, 0x034], vertical=True),
            stripe(0x2402, [0x158, 0x220, 0x16A, 0x158, 0x234, 0x236], vertical=True),
            stripe(0x2404, [0x398, 0x125, 0x218, 0x21A, 0x225], vertical=True),
            param='Catfish Approach WC',
        ),
    ],
    0x58: [
        change(ChangeWhen.DISABLED_EDGE,  # Village of Outcasts NW
            stripe(0x200E, [0x016, 0x01E, 0x0D6, 0x09D], vertical=True),
            stripe(0x2010, [0x014, 0x01C, 0x04E, 0x09B, 0x09E], vertical=True),
            stripe(0x2012, [0x015, 0x01D, 0x04F, 0x09C, 0x17C], vertical=True),
            stripe(0x2014, [0x016, 0x01E, 0x0D6, 0x09D], vertical=True),
            param='Village of Outcasts NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Village of Outcasts NC
            tile(0x016, 0x2026),
            stripe_rle_inc(0x014, 0x2028, 3),
            tile(0x01E, 0x20A6),
            stripe_rle_inc(0x01C, 0x20A8, 3),
            stripe(0x2126, [0x0D6, 0x04E, 0x04F, 0x0D6]),
            tile(0x09D, 0x21A6),
            stripe_rle_inc(0x09B, 0x21A8, 3),
            param='Village of Outcasts NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Village of Outcasts NE
            tile(0x332, 0x205E),
            stripe_rle(0x337, 0x2060, 4),
            tile(0x333, 0x2068),
            stripe(0x20DE, [0x335, 0x034, 0x09E, 0x17C]),
            param='Village of Outcasts NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Village of Outcasts ES
            stripe(0x38FE, [0xD1E, 0x29C, 0x29C, 0x29C, 0x61B, 0x669], vertical=True),
            stripe(0x39FC, [0x425, 0x5D7, OWW_SKIP, 0x333], vertical=True),
            param='Village of Outcasts ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Village of Outcasts SE
            stripe(0x3EEA, [0x337, 0x337, 0x333, 0x10B, 0x10B]),
            stripe(0x3F6E, [0x09E, 0x17C]),
            param='Village of Outcasts SE',
        ),
    ],
    0x5A: [
        change(ChangeWhen.OWLAYOUT,  # rocks for hardlock protection
            stripe_rle_inc(0x2F8, 0x2FBC, 2),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Shield Shop NW
            stripe(0x2010, [0x333, 0x10B, 0x10B, 0x337, 0x337, 0x333]),
            param='Shield Shop NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Shield Shop NE
            stripe(0x2022, [0x337, 0x333, 0x10B]),
            param='Shield Shop NE',
        ),
    ],
    0x5B: [
        change(ChangeWhen.OWLAYOUT,  # rocks for hardlock protection
            stripe(0x2F80, [0x2FA, 0x30A, 0x30D], vertical=True),
            stripe_rle_inc(0x39A, 0x2FFE, 2, vertical=True),
        ),
        change(ChangeWhen.UNFLIPPED,  # sign/peg
            tile(0x101, 0x27B6),
            tile(0x5C2, 0x27B4),
        ),
        change(ChangeWhen.FLIPPED,
            stripe(0x2E1C, [0xA06, 0xA0E]),  # seal pyramid entrance

            # south pyramid terrain
            tile(0x323, 0x39B6),
            stripe_rle(0x324, 0x39B8, 4),
            tile(0x2FE, 0x3A34),
            tile(0x2FF, 0x3A36),
            tile(0x235, 0x3BB4),
            stripe_rle(0x326, 0x3A38, 4),
            stripe(0x3AB2, [0x39D, 0x303, 0x232, 0x233, 0x233, 0x233, 0x233]),
            stripe(0x3B32, [0x3A2, 0x232, 0x235, 0x46A, 0x333, 0x333, 0x333]),
            arb_tile_copy(0x034, [0x3BB6, 0x3BBA, 0x3BBC, 0x3C3A, 0x3C3C, 0x3C3E]),
            tile(0x0F2, 0x3BB8),
            tile(0x108, 0x3C38),
            stripe(0x39C0, [0x324, 0x324, 0x324, 0x325, 0x2D5, OWW_SKIP, 0x2CC]),
            tile(0x2CC, 0x39D4),
            stripe(0x3A40, [0x326, 0x326, 0x326, 0x327, 0x2F7, OWW_SKIP, 0x2E3, 0x2E3]),
            stripe(0x3AC0, [0x233, 0x233, 0x233, 0x234, 0x2F6, 0x396]),
            stripe(0x3B40, [0x333, 0x333, 0x3AA, 0x3A3, 0x234, 0x397]),
            stripe(0x3BC0, [0x034, 0x034, 0x29C, 0x034, 0x3A3]),
            stripe(0x3C40, [0x034, 0x034, 0x10A]),
            stripe_rle(0x10B, 0x3C46, 17),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Pyramid ES
            stripe(0x347E, [0xD1E, 0x29C, 0x29C, 0x333], vertical=True),
            param='Pyramid ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Pyramid SW
            stripe_rle_inc(0x333, 0x3E8E, 2),
            stripe(0x3F10, [0x336, 0x334]),
            stripe(0x3F92, [0x336, 0x10B]),
            param='Pyramid SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Pyramid SE
            stripe_rle(0x0A5, 0x3F68, 2),
            tile(0x333, 0x3FD4),
            stripe_rle(0x10B, 0x3FD6, 8),
            stripe_rle(0x337, 0x3FE6, 8),
            tile(0x333, 0x3FF6),
            param='Pyramid SE',
        ),
    ],
    0x5D: [
        change(ChangeWhen.DISABLED_EDGE,  # Broken Bridge NW
            tile(0x46A, 0x2008),
            stripe_rle(0x337, 0x200A, 10),
            tile(0x333, 0x201E),
            stripe(0x208E, [0x09E, 0x17C]),
            param='Broken Bridge NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Broken Bridge NC
            stripe(0x2022, [0x1EE, 0x153, 0x156, 0x0C8, 0x0C8]),
            stripe(0x20A2, [0x1EE, 0x2CF, 0x2DB, 0x2D4, 0x0D3]),
            param='Broken Bridge NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Broken Bridge NE
            tile(0x163, 0x202C),
            stripe_rle(0x28F, 0x202E, 4),
            tile(0x0D5, 0x2036),
            stripe_rle(0x11D, 0x20AE, 4),
            tile(0x0D5, 0x20B6),
            param='Broken Bridge NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Broken Bridge SW
            stripe(0x2F10, [0x034, 0x034, 0x071, 0x034, 0x034, 0x071, 0x034]),
            tile(0x333, 0x2F88),
            stripe_rle(0x10B, 0x2F8A, 6),
            stripe_rle(0x337, 0x2F96, 6),
            tile(0x333, 0x2FA2),
            param='Broken Bridge SW',
        ),
    ],
    0x5E: [
        change(ChangeWhen.DISABLED_EDGE,  # Palace of Darkness SW
            tile(0x218, 0x3E8E),
            stripe(0x3F08, [0x236, 0x234, 0x158, 0x21A, 0x1C2, 0x1C2]),
            stripe(0x3F88, [0x071, 0x236, 0x234, 0x225, 0x1D5, 0x1D5, 0x2B0, 0x106, 0x107]),
            param='Palace of Darkness SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Palace of Darkness SE
            stripe_rle(0x1C2, 0x3EEE, 2),
            stripe(0x3F68, [0x171, 0x166, 0x225, 0x1D5, 0x1D5, 0x2B0, 0x106, 0x107]),
            stripe(0x3FE8, [0x0C6, 0x171, 0x165, 0x165, 0x165, 0x165, 0x107, 0x0C6]),
            param='Palace of Darkness SE',
        ),
    ],
    0x62: [
        change(ChangeWhen.OWLAYOUT,  # rocks for hardlock protection
            tile(0x2B9, 0x203C),
            tile(0x309, 0x203E),
            tile(0x30E, 0x20BE),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hammer Pegs WS
            stripe(0x2880, [0xD1E, 0x29C, 0x29C, 0x29C, 0x10A, 0x034], vertical=True),
            stripe(0x2982, [0x3C2, 0x42E, 0x334, 0x336], vertical=True),
            param='Hammer Pegs WS',
        ),
    ],
    0x65: [
        change(ChangeWhen.DISABLED_EDGE,  # Dark Dunes NW
            tile(0x333, 0x2008),
            stripe_rle(0x10B, 0x200A, 6),
            stripe_rle(0x337, 0x2016, 6),
            tile(0x333, 0x2022),
            tile(0x09E, 0x208E),
            stripe_rle(0x09F, 0x2090, 9),
            param='Dark Dunes NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Dunes WN
            tile(0x163, 0x2380),
            stripe_rle(0x124, 0x2400, 4, vertical=True),
            stripe(0x2600, [0x161, 0x0C8, 0x2D4, 0x2D3], vertical=True),
            param='Dark Dunes WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Dunes SC
            tile(0x0AD, 0x2F10),
            stripe_rle(0x0A5, 0x2F12, 18),
            tile(0x333, 0x2F88),
            stripe_rle(0x10B, 0x2F8A, 11),
            stripe_rle(0x337, 0x2FA0, 10),
            tile(0x333, 0x2FB4),
            param='Dark Dunes SC',
        ),
    ],
    0x68: [
        change(ChangeWhen.DISABLED_EDGE,  # Dig Game EC
            tile(0x0F2, 0x2BBE),
            param='Dig Game EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dig Game ES
            stripe(0x2D3E, [0x0C8, 0x0D3, 0x0CE], vertical=True),
            stripe(0x2E3C, [0x100, 0x104, 0x2B0], vertical=True),
            stripe_rle_inc(0x105, 0x2EBE, 3, vertical=True),
            param='Dig Game ES',
        ),
    ],
    0x69: [
        change(ChangeWhen.DISABLED_EDGE,  # Frog NE
            stripe(0x202A, [0x337, 0x337, 0x333, 0x10B, 0x10B]),
            stripe(0x20AE, [0x09F, 0x17C]),
            param='Frog NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Frog WC
            tile(0x29C, 0x2B80),
            param='Frog WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Frog WS
            stripe(0x2D00, [0x153, 0x1EE, 0x16A, 0x158, 0x166, 0x171], vertical=True),
            stripe(0x2E02, [0x218, 0x21A, 0x225], vertical=True),
            param='Frog WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Frog ES
            tile(0x0B0, 0x29BC),
            stripe(0x2ABE, [0x0D7, 0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe(0x2C3C, [0x17C, 0x0AC], vertical=True),
            param='Frog ES',
        ),
    ],
    0x6A: [
        change(ChangeWhen.DISABLED_EDGE,  # Stumpy WS
            stripe(0x2B00, [0xD1E, 0x29C, 0x29C, 0x29C, 0x333], vertical=True),
            stripe_rle(0x034, 0x2C02, 2, vertical=True),
            param='Stumpy WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Stumpy SW
            stripe(0x2E84, [0x333, 0x10B, 0x334]),
            stripe(0x2F08, [0x336, 0x334]),
            stripe(0x2F88, [0x034, 0x336, 0x10B]),
            param='Stumpy SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Stumpy SC
            stripe(0x2F1A, [0x0B1, 0x0AF, 0x07E, 0x0B1]),
            tile(0x016, 0x2F9A),
            stripe_rle_inc(0x014, 0x2F9C, 3),
            param='Stumpy SC',
        ),
    ],
    0x6B: [
        change(ChangeWhen.DISABLED_EDGE,  # Dark Bonk Rocks NW
            stripe(0x200E, [0x333, 0x10B, 0x337, 0x333]),
            param='Dark Bonk Rocks NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Bonk Rocks EN
            stripe(0x25BE, [0x0D5, 0x0CE, 0x0CE, 0x105], vertical=True),
            stripe(0x26BC, [0x15C, 0x174], vertical=True),
            param='Dark Bonk Rocks EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Bonk Rocks EC
            stripe(0x27BC, [0x522, 0x126], vertical=True),
            tile(0x1F2, 0x27BE),
            stripe_rle(0x127, 0x283E, 5, vertical=True),
            stripe(0x2A3C, [0x14B, 0x182], vertical=True),
            tile(0x150, 0x2ABE),
            param='Dark Bonk Rocks EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Bonk Rocks ES
            stripe(0x2B3C, [0x0C8, 0x0C8, 0x0DB, 0x034, 0x15C, 0x174], vertical=True),
            stripe(0x2B3E, [0x0C8, 0x0C8, 0x23A, 0x0CE, 0x0CE, 0x106, 0x107], vertical=True),
            stripe(0x2C3A, [0x034, 0x17C, 0x0AC], vertical=True),
            param='Dark Bonk Rocks ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Bonk Rocks SW
            stripe(0x2F12, [0x0AD, 0x0AC]),
            stripe(0x2F92, [0x337, 0x333, 0x10B]),
            param='Dark Bonk Rocks SW',
        ),
    ],
    0x6C: [
        change(ChangeWhen.DISABLED_EDGE,  # Big Bomb Shop NE
            tile(0x333, 0x2014),
            stripe_rle(0x10B, 0x2016, 8),
            stripe_rle(0x337, 0x2026, 8),
            tile(0x333, 0x2036),
            stripe(0x20A8, [0x09E, 0x17C]),
            param='Big Bomb Shop NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Big Bomb Shop WN
            stripe(0x2580, [0x220, 0x16A, 0x16A, 0x158], vertical=True),
            stripe(0x2682, [0x160, 0x172], vertical=True),
            param='Big Bomb Shop WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Big Bomb Shop WC
            tile(0x163, 0x2780),
            stripe(0x2782, [0x398, 0x125], vertical=True),
            stripe_rle(0x124, 0x2800, 5, vertical=True),
            stripe(0x2A02, [0x139, 0x16B], vertical=True),
            tile(0x161, 0x2A80),
            param='Big Bomb Shop WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Big Bomb Shop WS
            stripe(0x2B00, [0x153, 0x153, 0x1EE, 0x16A, 0x16A, 0x166, 0x171], vertical=True),
            stripe(0x2B02, [0x153, 0x153, 0x186, 0x034, 0x160, 0x172], vertical=True),
            stripe(0x2C04, [0x09E, 0x0AD], vertical=True),
            param='Big Bomb Shop WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Big Bomb Shop ES
            stripe(0x2BBE, [0xD1E, 0x29C, 0x29C, 0x333], vertical=True),
            stripe(0x2C3C, [0x17C, 0x0AC], vertical=True),
            param='Big Bomb Shop ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Big Bomb Shop SC
            stripe(0x2E98, [0x167, 0x160, OWW_SKIP, 0x9CF]),
            stripe(0x2F16, [0x171, 0x166, 0x172, 0x15E, 0x174, 0x105, 0x106, 0x107]),
            stripe(0x2F96, [0x0C6, 0x171, 0x165, 0x165, 0x165, 0x0D5, 0x0C5, 0x0C6]),
            param='Big Bomb Shop SC',
        ),
    ],
    0x6D: [
        change(ChangeWhen.DISABLED_EDGE,  # Hammer Bridge NC
            tile(0x333, 0x2008),
            stripe_rle(0x10B, 0x200A, 11),
            stripe_rle(0x337, 0x2020, 10),
            tile(0x333, 0x2034),
            tile(0x09E, 0x2090),
            stripe_rle(0x09F, 0x2092, 17),
            tile(0x17C, 0x20B4),
            param='Hammer Bridge NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hammer Bridge EN
            stripe(0x23BC, [0x17C, 0x0AC], vertical=True),
            tile(0xD1E, 0x23BE),
            stripe_rle(0x29C, 0x243E, 4, vertical=True),
            tile(0x333, 0x263E),
            param='Hammer Bridge EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hammer Bridge EC
            stripe(0x283E, [0x51C, 0x39B, 0x2F8, 0x39A, 0x39B, 0x2F8, 0x39A, 0x39B, 0x69E], vertical=True),
            param='Hammer Bridge EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hammer Bridge WS
            stripe(0x2B80, [0xD1E, 0x29C, 0x29C, 0x333], vertical=True),
            stripe(0x2C02, [0x09E, 0x0AD], vertical=True),
            param='Hammer Bridge WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hammer Bridge SC
            stripe(0x2F18, [0x0AD, 0x0AC]),
            tile(0x333, 0x2F90),
            stripe_rle(0x10B, 0x2F92, 6),
            stripe_rle(0x337, 0x2F9E, 5),
            tile(0x333, 0x2FA8),
            param='Hammer Bridge SC',
        ),
    ],
    0x6E: [
        change(ChangeWhen.DISABLED_EDGE,  # Dark Tree Line NW
            stripe(0x2008, [0x1E7, 0x1EB, 0x153, 0x0DC, 0x0DC, 0x0DC, 0x0C8, 0x0D0, 0x0D2]),
            stripe(0x208A, [0x153, 0x178, 0x51D, 0x51D, 0x51D, 0x0CA, 0x0C8]),
            stripe(0x210C, [0x153, 0x0E3, 0x0E3, 0x0E3, 0x0C8]),
            param='Dark Tree Line NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Tree Line WN
            tile(0xD1E, 0x2380),
            stripe(0x2382, [0x09E, 0x0AD], vertical=True),
            stripe_rle(0x29C, 0x2400, 4, vertical=True),
            tile(0x333, 0x2600),
            param='Dark Tree Line WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Tree Line WC
            stripe(0x2800, [0x51C, 0x39B, 0x2F8, 0x39A, 0x39B, 0x2F8, 0x39A, 0x39B, 0x69E], vertical=True),
            param='Dark Tree Line WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Tree Line SC
            stripe(0x2EA2, [0x171, 0x166, 0x2F6, 0x396, 0x39D, 0x303, 0x163]),
            stripe(0x2F22, [0x384, 0x171, 0x166, 0x397, 0x3A2, 0x106, 0x183]),
            stripe(0x2FA2, [0x0C6, 0x0AB, 0x171, 0x165, 0x165, 0x150, 0x153]),
            param='Dark Tree Line SC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark Tree Line SE
            stripe_rle(0x14E, 0x2F32, 2),
            stripe(0x2FB0, [0x161, 0x152, 0x152, 0x0D5]),
            param='Dark Tree Line SE',
        ),
    ],
    0x6F: [
        change(ChangeWhen.FLIPPED,  # portal
            tile(0x20F, 0x2BB2),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Palace of Darkness Nook NE
            stripe(0x2028, [0x17E, 0x183, 0x153, 0x0DC, 0x0C8, 0x0D0, 0x0D2, 0x0C6]),
            stripe(0x20AA, [0x153, 0x153, 0x0C9, 0x0C8, 0x0C8, 0x0D0, 0x0D2]),
            stripe(0x212C, [0x153, 0x386, 0x0C8, 0x0C8, 0x0D3, 0x0D2]),
            stripe(0x21AE, [0x2E5, 0x2ED, 0x0D3]),
            stripe(0x2230, [0x2E5, 0x53C]),
            param='Palace of Darkness Nook NE',
        ),
    ],
    0x70: [
        change(ChangeWhen.FLIPPED,  # portal
            tile(0x239, 0x3D94),
        ),
    ],
    0x72: [
        change(ChangeWhen.DISABLED_EDGE,  # Stumpy Approach NW
            stripe_rle(0x034, 0x2008, 2),
            stripe(0x2086, [0x333, 0x10B, 0x337, 0x333]),
            stripe(0x2108, [0x09E, 0x17C]),
            param='Stumpy Approach NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Stumpy Approach NC
            tile(0x01E, 0x201A),
            stripe_rle_inc(0x01C, 0x201C, 3),
            stripe(0x209A, [0x0D6, 0x04E, 0x04F, 0x0D6]),
            tile(0x09D, 0x211A),
            stripe_rle_inc(0x09B, 0x211C, 3),
            param='Stumpy Approach NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Stumpy Approach EC
            tile(0x0D5, 0x22BE),
            stripe_rle(0x0CE, 0x233E, 22, vertical=True),
            stripe(0x26BC, [0x17C, 0x0AC], vertical=True),
            stripe(0x2D3C, [0x034, 0x100, 0x104, 0x2B0], vertical=True),
            stripe_rle_inc(0x105, 0x2E3E, 3, vertical=True),
            param='Stumpy Approach EC',
        ),
    ],
    0x73: [
        change(ChangeWhen.FLIPPED,  # portal
            tile(0x20F, 0x22A8),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark C Whirlpool NW
            stripe(0x2012, [0x337, 0x333, 0x10B]),
            stripe(0x2092, [0x09E, 0x17C]),
            param='Dark C Whirlpool NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark C Whirlpool WC
            tile(0x220, 0x2280),
            stripe_rle(0x16A, 0x2300, 22, vertical=True),
            stripe(0x2682, [0x09E, 0x0A9], vertical=True),
            stripe(0x2D82, [0x218, 0x21A, 0x225], vertical=True),
            stripe(0x2E00, [0x158, 0x166, 0x171], vertical=True),
            param='Dark C Whirlpool WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark C Whirlpool EN
            tile(0xD1E, 0x243E),
            stripe(0x24BC, [0x381, 0x0E2, 0x2EA, 0x2D2, 0x2D2, 0x2E8], vertical=True),
            stripe_rle(0x29C, 0x24BE, 5, vertical=True),
            tile(0x333, 0x273E),
            param='Dark C Whirlpool EN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark C Whirlpool EC
            stripe_rle(0x2F8, 0x27BE, 6, vertical=True),
            param='Dark C Whirlpool EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark C Whirlpool ES
            stripe(0x2ABC, [0x2C7, 0x2D2, 0x2C8, 0x677, 0x682, 0x682], vertical=True),
            tile(0xD1E, 0x2ABE),
            stripe_rle(0x29C, 0x2B3E, 6, vertical=True),
            tile(0x333, 0x2E3E),
            param='Dark C Whirlpool ES',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark C Whirlpool SC
            tile(0x333, 0x2F94),
            stripe_rle(0x10B, 0x2F96, 8),
            stripe_rle(0x337, 0x2FA6, 8),
            tile(0x333, 0x2FB6),
            param='Dark C Whirlpool SC',
        ),
    ],
    0x74: [
        change(ChangeWhen.DISABLED_EDGE,  # Hype Cave NC
            stripe(0x2016, [0x0C6, 0x384, 0x0C6, 0x0C6, 0x0C6, 0x0D5, 0x0C5, 0x0C6]),
            stripe(0x2096, [0x384, 0x17E, 0x0D1, 0x0D1, 0xC06, 0x0D5, 0x0C5, 0x384]),
            stripe(0x2116, [0x17E, 0x183, 0x51D, 0x51D, 0x1EC, 0x1E9, 0x0D0, 0x0D2]),
            stripe(0x2198, [0x153, 0x0E3, 0x0E3, 0x0C8, 0x0CA, 0x0C8]),
            stripe(0x221E, [0x0DB, 0x0C8]),
            param='Hype Cave NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hype Cave WN
            tile(0xD1E, 0x2400),
            stripe_rle(0x29C, 0x2480, 5, vertical=True),
            stripe(0x2582, [0xAFD, 0xAFF, 0xAFF, 0xAFE], vertical=True),
            tile(0x333, 0x2700),
            param='Hype Cave WN',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hype Cave WC
            stripe_rle(0x2F8, 0x2780, 6, vertical=True),
            param='Hype Cave WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hype Cave WS
            tile(0xD1E, 0x2A80),
            tile(0xB01, 0x2A82),
            stripe_rle(0x29C, 0x2B00, 6, vertical=True),
            stripe_rle_inc(0xAFF, 0x2B02, 2, vertical=True),
            tile(0x333, 0x2E00),
            param='Hype Cave WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Hype Cave SC
            tile(0x333, 0x2F86),
            stripe_rle(0x10B, 0x2F88, 12),
            stripe_rle(0x337, 0x2FA0, 11),
            tile(0x333, 0x2FB6),
            param='Hype Cave SC',
        ),
    ],
    0x75: [
        change(ChangeWhen.FLIPPED,  # portal
            tile(0x239, 0x3352),
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Ice Lake NW
            tile(0x333, 0x2010),
            stripe_rle(0x10B, 0x2012, 6),
            stripe_rle(0x337, 0x201E, 5),
            tile(0x333, 0x2028),
            stripe(0x2098, [0x09E, 0x17C]),
            param='Ice Lake NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Ice Lake NC
            stripe(0x2064, [0x1EE, 0x153, 0x0C9, 0x0C9, 0x0CA, 0x0CA]),
            stripe(0x20E4, [0x1EE, 0x153, 0x156, 0x156, 0x0C8, 0x0CA]),
            stripe(0x2164, [0x1EE, 0x2CF, 0x2DB, 0x2DB, 0x2D4, 0x0D3]),
            param='Ice Lake NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Ice Lake NE
            stripe(0x2070, [0x163, 0x9AF, 0x9AF, 0x0D5]),
            stripe(0x20F2, [0x11D, 0x11D, 0x0D5]),
            param='Ice Lake NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Ice Lake WS
            stripe(0x3A80, [0x2EB, 0x667], vertical=True),
            stripe(0x3A82, [0x667, 0x38A, 0x1EE, 0x328, 0x328, 0x328, 0x328, 0x158, 0x166, 0x171], vertical=True),
            stripe_rle(0x532, 0x3B80, 5, vertical=True),
            stripe(0x3D84, [0x319, 0x666, 0x225], vertical=True),
            stripe(0x3E00, [0x6A7, 0x165, 0x0C6], vertical=True),
            param='Ice Lake WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Ice Lake EC
            stripe(0x36FE, [0x0D2, 0x0D0, 0x0CA, 0x0CA, 0x0D3, 0x12D, 0x12D, 0x12D, 0x105, 0x105], vertical=True),
            stripe_rle(0x2CD, 0x397C, 3, vertical=True),
            stripe(0x3AFC, [0x303, 0x2B0], vertical=True),
            param='Ice Lake EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Ice Lake ES
            stripe(0x3BFC, [0x2E1, 0x2E6], vertical=True),
            tile(0x1F2, 0x3BFE),
            stripe_rle(0x786, 0x3C7E, 4, vertical=True),
            stripe(0x3E7E, [0x201, 0x6A7], vertical=True),
            tile(0x74E, 0x3EFC),
            param='Ice Lake ES',
        ),
    ],
    0x77: [
        change(ChangeWhen.DISABLED_EDGE,  # Shopping Mall SW
            stripe_rle(0x502, 0x2F8E, 3),
            param='Shopping Mall SW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Shopping Mall SE
            stripe(0x2E9C, [0x315, OWW_SKIP, 0x2E6, 0x2E7, 0x2E0, OWW_SKIP, 0x2E0, 0x2E7, 0x306]),
            stripe(0x2F1A, [0x161, 0x31D]),
            stripe_rle(0x321, 0x2F1E, 14),
            stripe(0x2F9A, [0x0C8, 0x161]),
            stripe_rle(0x152, 0x2F9E, 14),
            tile(0x0D5, 0x2FBA),
            param='Shopping Mall SE',
        ),
    ],
    0x7A: [
        change(ChangeWhen.DISABLED_EDGE,  # Swamp Nook EC
            stripe(0x26BA, [0x0D2, 0x0D0, 0x0D3, 0x0C4, 0x0C4, 0x0C4, 0x106, 0x107, 0x0AB], vertical=True),
            stripe(0x26BC, [0x6AB, 0x0D2], vertical=True),
            stripe_rle(0x6AB, 0x26BE, 8, vertical=True),
            stripe_rle(0x0C5, 0x27BC, 4, vertical=True),
            stripe(0x2838, [0x0D3, 0x0CE, 0x0CE, 0x105], vertical=True),
            tile(0x034, 0x28B4),
            stripe(0x29BC, [0x107, 0x6AB], vertical=True),
            param='Swamp Nook EC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Swamp Nook ES
            stripe(0x2C3A, [0x0D2, 0x0D0, 0x0CA, 0x0CA, 0x0D3, 0x0CE, 0x2B0], vertical=True),
            stripe(0x2C3C, [0x6AB, 0x0D2, 0x0D0, 0x0D3, 0x0C4, 0x0C4, 0x106, 0x107], vertical=True),
            stripe(0x2C3E, [0x6AB, 0x6AB, 0x0D2, 0x0C5, 0x0C5, 0x0C5, 0x107, 0x6AB], vertical=True),
            param='Swamp Nook ES',
        ),
    ],
    0x7B: [
        change(ChangeWhen.DISABLED_EDGE,  # Swamp NC
            tile(0x333, 0x2014),
            stripe_rle(0x10B, 0x2016, 8),
            stripe_rle(0x337, 0x2026, 8),
            tile(0x333, 0x2036),
            param='Swamp NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Swamp WC
            stripe(0x2680, [0x0C6, 0x17E], vertical=True),
            stripe(0x2682, [0x17E, 0x183, 0x1EE, 0x15B, 0x15B, 0x15B, 0x166, 0x171], vertical=True),
            stripe_rle(0x21C, 0x2780, 4, vertical=True),
            stripe(0x2804, [0x1EE, 0x16A, 0x16A, 0x158], vertical=True),
            stripe(0x2980, [0x171, 0x0C6], vertical=True),
            param='Swamp WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Swamp WS
            stripe(0x2C00, [0x0C6, 0x17E], vertical=True),
            stripe(0x2C02, [0x17E, 0x183, 0x1EE, 0x15B, 0x15B, 0x166, 0x171, 0x384], vertical=True),
            stripe_rle(0x21C, 0x2D00, 3, vertical=True),
            stripe(0x2D84, [0x1EE, 0x16A, 0x158, 0x166, 0x171], vertical=True),
            stripe(0x2E06, [0x218, 0x21A, 0x225], vertical=True),
            stripe(0x2E80, [0x171, 0x0C6, 0x0C6], vertical=True),
            param='Swamp WS',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Swamp EC
            tile(0x333, 0x21BE),
            stripe_rle(0x0F2, 0x223E, 24, vertical=True),
            tile(0x333, 0x2E3E),
            param='Swamp EC',
        ),
    ],
    0x7C: [
        change(ChangeWhen.DISABLED_EDGE,  # Dark South Pass NC
            tile(0x333, 0x2006),
            stripe_rle(0x10B, 0x2008, 12),
            stripe_rle(0x337, 0x2020, 11),
            tile(0x333, 0x2036),
            param='Dark South Pass NC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark South Pass WC
            tile(0xD1E, 0x2180),
            stripe_rle(0x29C, 0x2200, 24, vertical=True),
            tile(0x333, 0x2E00),
            param='Dark South Pass WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Dark South Pass ES
            stripe(0x2A3A, [0x2EC, 0x2F4, 0x2F0, 0x0C8, 0x2ED], vertical=True),
            tile(0x0CF, 0x2AB6),
            stripe(0x2ABC, [0x2EB, 0x2F4, 0x2F0, 0x0D3, 0x2FD, 0x2FD, 0x2FD], vertical=True),
            stripe(0x2ABE, [0x2E5, 0x2EB, 0x2F4, 0x2E4, 0x2E4, 0x2E4, 0x2E4, 0x6A7, 0x165, 0x0C6], vertical=True),
            stripe(0x2DBA, [0x593, 0x599, 0x2B0], vertical=True),
            stripe_rle_inc(0x105, 0x2E3C, 3, vertical=True),
            param='Dark South Pass ES',
        ),
    ],
    0x7F: [
        change(ChangeWhen.OWLAYOUT,  # C terrain
            stripe_rle_inc(0x75C, 0x2A9A, 2, vertical=True),
            stripe(0x2A22, [0x752, 0x753, 0x2E5]),
            stripe(0x2A9E, [0x774, 0x6E1, 0x757, 0x6E3, 0x2E5]),
            stripe(0x2B1E, [0x76E, 0x2E5, 0x759, 0x779]),
            stripe(0x2B9E, [0x76C, 0x2EC, 0x6F5, 0x705]),
            stripe(0x2C1E, [0x704, 0x6F6, 0x6F7, 0x6E3]),
            stripe(0x2CA2, [0x762, 0x773]),
            arb_tile_copy(0x2EC, [0x29A4, 0x2C16]),
            tile(0x75E, 0x2B9A),
            tile(0x76F, 0x2C1A),
            param='lw',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Bomber Corner NW
            stripe_rle(0x502, 0x200E, 3),
            param='Bomber Corner NW',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Bomber Corner NE
            stripe(0x201A, [0x105, 0x163]),
            stripe_rle(0x28F, 0x201E, 14),
            tile(0x0D5, 0x203A),
            stripe(0x209A, [0x163, 0x301]),
            stripe_rle(0x2E7, 0x209E, 14),
            tile(0x0D5, 0x20BA),
            param='Bomber Corner NE',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Bomber Corner WC
            tile(0x306, 0x211C),
            stripe(0x2680, [0x17E, 0x183, 0x153, 0x153, 0x1EE, 0x131, 0x131, 0x131, 0x158, 0x158], vertical=True),
            stripe_rle(0x2C4, 0x2902, 3, vertical=True),
            stripe(0x2A82, [0x2F6, 0x225], vertical=True),
            param='Bomber Corner WC',
        ),
        change(ChangeWhen.DISABLED_EDGE,  # Bomber Corner WS
            tile(0x163, 0x2B80),
            stripe(0x2B82, [0x304, 0x306], vertical=True),
            stripe_rle(0x2FC, 0x2C00, 5, vertical=True),
            tile(0x6A7, 0x2E80),
            param='Bomber Corner WS',
        ),
    ],
}
