import struct
import time
from typing import TYPE_CHECKING

from .address_maps import GHOST_RATCHET_ADDRESSES

if TYPE_CHECKING:
    from ..pypine import Pine


class GhostRatchetInt32Field:
    """Pine-backed accessor for a raw int32 ghost-struct field — a pre-encoded
    float bit pattern or plain flag, written verbatim, not float-encoded."""

    def __init__(self, field_name: str) -> None:
        self.field_name = field_name

    def _address(self, instance: "GhostRatchetAddresses") -> int:
        return instance.base + instance._OFFSETS[self.field_name]

    def __get__(self, instance: "GhostRatchetAddresses | None", owner) -> int | None:
        if instance is None:
            return None
        return instance.pine.read_int32(self._address(instance))

    def __set__(self, instance: "GhostRatchetAddresses", value: int) -> None:
        instance.pine.write_int32(self._address(instance), value)


class GhostRatchetFloatField:
    """Pine-backed accessor for a genuine float ghost-struct field (X/Y/Z,
    timer). Pine has no read_float, so reads go through read_bytes + struct.unpack."""

    def __init__(self, field_name: str) -> None:
        self.field_name = field_name

    def _address(self, instance: "GhostRatchetAddresses") -> int:
        return instance.base + instance._OFFSETS[self.field_name]

    def __get__(self, instance: "GhostRatchetAddresses | None", owner) -> float | None:
        if instance is None:
            return None
        return struct.unpack_from("<f", instance.pine.read_bytes(self._address(instance), 4))[0]

    def __set__(self, instance: "GhostRatchetAddresses", value: float) -> None:
        instance.pine.write_float(self._address(instance), value)


class GhostRatchetAddresses:
    """Pine-backed live accessor for one Ghost Ratchet entity struct instance.
    The rotation/scale/base/visibility fields are fixed int32 bit patterns, the
    same for every spawn regardless of position; x/y/z/timer are genuine floats."""

    _OFFSETS: dict[str, int] = {
        "rotation_scale_1": -0x14,
        "rotation_1":       -0xC,
        "base_field":        0x0,
        "rotation_2":        0xC,
        "rotation_scale_2":  0x14,
        "x":                 0x1C,
        "y":                 0x20,
        "z":                 0x24,
        "visibility":        0x50,
        "timer":             0x5C,
    }

    rotation_scale_1 = GhostRatchetInt32Field("rotation_scale_1")
    rotation_1       = GhostRatchetInt32Field("rotation_1")
    base_field       = GhostRatchetInt32Field("base_field")
    rotation_2       = GhostRatchetInt32Field("rotation_2")
    rotation_scale_2 = GhostRatchetInt32Field("rotation_scale_2")
    visibility       = GhostRatchetInt32Field("visibility")
    x                = GhostRatchetFloatField("x")
    y                = GhostRatchetFloatField("y")
    z                = GhostRatchetFloatField("z")
    timer            = GhostRatchetFloatField("timer")

    def __init__(self, base: int, pine: "Pine") -> None:
        self.base = base
        self.pine = pine

    def __repr__(self) -> str:
        return f"GhostRatchetAddresses(base=0x{self.base:08X}, visibility={self.visibility})"


# Fixed values for the non-position fields, confirmed in-game.
_ROTATION_SCALE_1 = 0x3F76EAAC
_ROTATION_1       = 0x3E872D1A
_BASE_FIELD       = 0x3F7FFFFE
_ROTATION_2       = 0xBE872D19
_ROTATION_SCALE_2 = 0x3F76EAAB
_VISIBLE          = 1
_HIDDEN           = 0
_TIMER_VALUE: float = 1000.0

_DESPAWN_AFTER_SECONDS: float = 1.0


class GhostRatchetInventory:
    """Pine-backed accessor for the Ghost Ratchet feature: spawns a static clone of
    Ratchet at his own current position. Position must be written LAST, after the
    trigger and other fixed fields — writing it first reproducibly froze the game."""

    def __init__(self, pine: "Pine") -> None:
        self.pine = pine
        self.active = False
        self._spawned_at: float | None = None
        self._planet_id: int | None = None
        self._addr: GhostRatchetAddresses | None = None
        self._trigger_address: int | None = None

        self._follow_active = False
        self._follow_planet_id: int | None = None
        self._follow_addr: GhostRatchetAddresses | None = None
        self._follow_trigger: int | None = None

    def _prepare_ghost(self, planet_addrs) -> bool:
        """Initialize an unused native ghost before enabling its callbacks.

        Level loading allocates the 0x18C-byte payload without initializing it.
        Its update/destructor dereference the owner at offset zero. Validate
        reciprocal object links and the native payload size before writing.
        """
        p = self.pine
        obj = planet_addrs.trigger - 0x40
        matrix = planet_addrs.ghost_base - 0x14
        player = planet_addrs.player_position - 0x30
        if (p.read_int32(obj + 0x24) != 0x0805C334
                or p.read_int32(obj + 0xC) != matrix
                or p.read_int32(matrix + 0x40) != obj):
            return False
        player_obj = p.read_int32(player + 0x40)
        definition = p.read_int32(obj + 0x10)
        payload = p.read_int32(matrix + 0x58)
        if not all(0x100000 <= value < 0x1E00000 - 0x18C
                   for value in (player_obj, definition, payload)):
            return False
        if (p.read_int32(player_obj + 0x24) != 0x36919224
                or p.read_int32(player_obj + 0xC) != player
                or p.read_int32(definition + 0x1C) != 0x18C):
            return False
        if p.read_int32(matrix + 0x64) == 0x8000:
            p.write_bytes(payload, struct.pack('<I', player) + bytes(0x188))
        return p.read_int32(payload) == player

    def spawn(self, planet_id: int) -> bool:
        """Spawn a ghost at Ratchet's current position on `planet_id`.
        Returns False (no-op) if that planet isn't in
        GHOST_RATCHET_ADDRESSES yet."""
        planet_addrs = GHOST_RATCHET_ADDRESSES.get(planet_id)
        if planet_addrs is None:
            return False

        if not self._prepare_ghost(planet_addrs):
            return False

        x, y, z = struct.unpack_from("<3f", self.pine.read_bytes(planet_addrs.player_position, 12))

        self._planet_id = planet_id
        self._addr = GhostRatchetAddresses(planet_addrs.ghost_base, self.pine)
        self._trigger_address = planet_addrs.trigger
        self.active = True
        self._spawned_at = time.monotonic()
        self.keep_alive(planet_id)

        self._addr.x = x
        self._addr.y = y
        self._addr.z = z
        return True

    def keep_alive(self, planet_id: int) -> None:
        """Re-arm the trigger/rotation/scale/visibility/timer fields every tick while
        `active`. If `planet_id` no longer matches, the struct address is stale — deactivate
        without writing further rather than risk corrupting unrelated memory."""
        if not self.active or self._addr is None or self._trigger_address is None:
            return
        if planet_id != self._planet_id:
            self.active = False
            self._spawned_at = None
            return
        if self._spawned_at is not None and time.monotonic() - self._spawned_at >= _DESPAWN_AFTER_SECONDS:
            self._despawn()
            return

        self.pine.write_int32(self._trigger_address, 1)
        addr = self._addr
        addr.rotation_scale_1 = _ROTATION_SCALE_1
        addr.rotation_1       = _ROTATION_1
        addr.base_field       = _BASE_FIELD
        addr.rotation_2       = _ROTATION_2
        addr.rotation_scale_2 = _ROTATION_SCALE_2
        addr.visibility       = _VISIBLE
        addr.timer            = _TIMER_VALUE

    def _despawn(self) -> None:
        if self._addr is not None:
            self._addr.visibility = _HIDDEN
        self.active = False
        self._spawned_at = None

    def read_own_position(self, planet_id: int) -> tuple[float, float, float] | None:
        """Read this client's own live X/Y/Z on `planet_id`, for GhostLink to broadcast
        to other linked players. None if `planet_id` isn't in GHOST_RATCHET_ADDRESSES."""
        planet_addrs = GHOST_RATCHET_ADDRESSES.get(planet_id)
        if planet_addrs is None:
            return None
        return struct.unpack_from("<3f", self.pine.read_bytes(planet_addrs.player_position, 12))

    def follow(self, planet_id: int, x: float, y: float, z: float) -> bool:
        """Render another GhostLink player at (x, y, z) on `planet_id`, rewriting X/Y/Z
        every call so the ghost tracks movement. No despawn timer — caller must call
        stop_following() once that peer's data goes stale or they leave the planet."""
        planet_addrs = GHOST_RATCHET_ADDRESSES.get(planet_id)
        if planet_addrs is None:
            return False
        if not self._prepare_ghost(planet_addrs):
            return False
        if self._follow_planet_id != planet_id:
            self._follow_addr = GhostRatchetAddresses(planet_addrs.ghost_base, self.pine)
            self._follow_trigger = planet_addrs.trigger
            self._follow_planet_id = planet_id
        self._follow_active = True

        self.pine.write_int32(self._follow_trigger, 1)
        addr = self._follow_addr
        addr.rotation_scale_1 = _ROTATION_SCALE_1
        addr.rotation_1       = _ROTATION_1
        addr.base_field       = _BASE_FIELD
        addr.rotation_2       = _ROTATION_2
        addr.rotation_scale_2 = _ROTATION_SCALE_2
        addr.visibility       = _VISIBLE
        addr.timer            = _TIMER_VALUE
        addr.x = x
        addr.y = y
        addr.z = z
        return True

    def stop_following(self) -> None:
        """Hide whichever peer's ghost follow() last rendered, if any."""
        if self._follow_active and self._follow_addr is not None:
            self._follow_addr.visibility = _HIDDEN
        self._follow_active = False
        self._follow_planet_id = None

    def __repr__(self) -> str:
        return f"GhostRatchetInventory(active={self.active}, planet_id={self._planet_id!r}, addr={self._addr!r})"
