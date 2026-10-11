"""Temporarily detach Ratchet's backpack without changing saved inventory.

The native crouch-jump handlers test PLAYER+0x5AC (Helipack): a null
pointer selects the ordinary jump instead of high/long jump. Both backpack
objects are hidden with the native moby visibility bit while detached.
"""

from dataclasses import dataclass

from . import address_maps
from .patches.loader_gate import LoaderGate


HIDDEN = 0x20
BACKPACK_SLOTS = (0x5A0, 0x5AC)


def _pointer(value):
    return 0x100000 <= value < 0x1E00000 and value % 4 == 0


@dataclass
class Backpack:
    slot: int
    object: int
    object_class: int
    hidden: int


class NoClank:
    def __init__(self, pine):
        self.pine = pine
        self.context = None
        self.backpacks = []

    def _context(self):
        p = self.pine
        game = p.get_game_id()
        if game != address_maps.GAME_ID or game not in address_maps.SUPPORTED_GAMES:
            return None
        gate = LoaderGate(p, game_id=game)
        if p.read_int32(gate.STATE) != 6:
            return None
        planet = p.read_int32(address_maps.CURRENT_PLANET_ADDRESS)
        # Exclude races and other special modes even if a player address is known.
        if planet not in (*range(1, 11), 0x17):
            return None
        config = address_maps.PLANET_ADDRESSES.get(planet)
        if config is None:
            return None
        base = config.player_state - 0x100
        ratchet = p.read_int32(base + 0x5B0)
        if not _pointer(ratchet):
            return None
        return game, planet, base, ratchet

    def _restore(self, *, visible):
        p = self.pine
        for backpack in self.backpacks:
            # A respawn or savestate may have rebuilt these objects. Never put
            # a stale pointer into a slot the game has already repopulated.
            if p.read_int32(backpack.slot) != 0:
                continue
            if p.read_int32(backpack.object + 0x40) != backpack.object_class:
                continue
            if visible:
                flags = p.read_int32(backpack.object + 0x64)
                p.write_int32(backpack.object + 0x64, (flags & ~HIDDEN) | backpack.hidden)
            p.write_int32(backpack.slot, backpack.object)
        self.backpacks = []

    def update(self, active):
        p = self.pine
        context = self._context()
        if context != self.context:
            # A loaded level owns its own objects; travel resets the pointers.
            self.backpacks = []
            self.context = context
        if context is None:
            return
        _, planet, base, ratchet = context
        is_ratchet = p.read_int32(base + 0x59C) == ratchet
        if not active or not is_ratchet:
            self._restore(visible=is_ratchet)
            return

        if self.backpacks:
            if all(p.read_int32(pack.slot) == 0 for pack in self.backpacks):
                for pack in self.backpacks:
                    if p.read_int32(pack.object + 0x40) == pack.object_class:
                        flags = p.read_int32(pack.object + 0x64)
                        if not flags & HIDDEN:
                            p.write_int32(pack.object + 0x64, flags | HIDDEN)
                return
            self._restore(visible=True)

        config = address_maps.PLANET_ADDRESSES[planet]
        # Let an airborne move finish. Do not detach during a pickup, death,
        # cutscene, menu, or a pending level transition.
        if p.read_int16(base + 0x100) not in (0, 1, 2):
            return
        if config.menu is None or p.read_int32(config.menu) != 0 or p.read_int32(config.menu + 4) != 0:
            return
        if p.read_int32(address_maps.NEW_PLANET_START_LOAD_ADDR) != 0xFFFFFFFF:
            return
        backpacks = []
        for offset in BACKPACK_SLOTS:
            slot = base + offset
            obj = p.read_int32(slot)
            if obj == 0:
                continue  # Naturally missing Clank stays missing after expiry.
            if not _pointer(obj):
                return
            object_class = p.read_int32(obj + 0x40)
            if not _pointer(object_class):
                return
            backpacks.append(Backpack(slot, obj, object_class, p.read_int32(obj + 0x64) & HIDDEN))
        # Record before writes so a dropped connection can recover on reconnect.
        self.backpacks = backpacks
        for backpack in backpacks:
            flags = p.read_int32(backpack.object + 0x64)
            p.write_int32(backpack.slot, 0)
            p.write_int32(backpack.object + 0x64, flags | HIDDEN)
