"""Resolve Treehouse's allocated ghost using native object identities and links."""
import time

from . import address_maps
from .address_maps.us_addresses import GhostRatchetPlanetAddresses
from .patches.loader_gate import LoaderGate


def pointer(value):
    return 0x100000 <= value < 0x1E00000 - 0x18C and value % 4 == 0


class TreehouseGhost:
    def __init__(self, pine):
        self.pine = pine
        self.addresses = None
        self.context = None
        self.retry_at = 0.0
        self.cursor = 0x100000

    def resolve(self, valid):
        p = self.pine
        game = p.get_game_id()
        if (game != address_maps.GAME_ID or game not in address_maps.SUPPORTED_GAMES
                or p.read_int32(address_maps.CURRENT_PLANET_ADDRESS) != 24
                or p.read_int32(LoaderGate(p, game_id=game).STATE) != 6):
            self.addresses = self.context = None
            return None
        base = address_maps.PLANET_ADDRESSES[24].player_state - 0x100
        player = p.read_int32(base + 0x5B0)
        if not pointer(player) or p.read_int32(base + 0x59C) != player:
            return None
        obj = p.read_int32(player + 0x40)
        if (not pointer(obj) or p.read_int32(obj + 0x24) != 0x36919224
                or p.read_int32(obj + 0xC) != player):
            return None
        context = (game, player, obj)
        if context != self.context:
            self.context, self.addresses, self.retry_at = context, None, 0.0
            self.cursor = 0x100000
        if self.addresses is not None and valid(self.addresses):
            return self.addresses
        self.addresses = None
        if time.monotonic() < self.retry_at:
            return None
        self.retry_at = time.monotonic() + 5.0
        # Scan incrementally: one 64 KiB read per poll, not a synchronous
        # multi-megabyte scan that would stall the client. Runtime objects live
        # below the level overlay; scan the common EE object arena.
        start = self.cursor
        data = p.read_bytes(start, 0x10000)
        self.cursor += 0x10000
        if self.cursor >= 0xD00000:
            self.cursor = 0x100000
        else:
            self.retry_at = 0.0
        offset = data.find(b'\x34\xc3\x05\x08')
        while offset != -1:
            ghost_obj = start + offset - 0x24
            if pointer(ghost_obj):
                matrix = p.read_int32(ghost_obj + 0xC)
                if pointer(matrix):
                    candidate = GhostRatchetPlanetAddresses(player + 0x30, matrix + 0x14, ghost_obj + 0x40)
                    if valid(candidate):
                        self.addresses = candidate
                        return candidate
            offset = data.find(b'\x34\xc3\x05\x08', offset + 4)
        return None
