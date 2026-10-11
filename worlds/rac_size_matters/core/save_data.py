from __future__ import annotations

from dataclasses import asdict, dataclass, field

from ..data.weapons import WEAPON_MAX_LEVELS


@dataclass
class RAC5SaveData:
    """Playthrough state that must survive a client reconnect but isn't recoverable from
    AP's checked_locations/items_received: quick-select loadout, equipped armour slots,
    and per-weapon levels. One AP data-storage key (context.py's
    _save_data_key()) instead of three.

    Deliberately excludes armour/weapon ownership -- that always comes from
    items_received via Core.apply_inventory(), so an AP-granted item can never be
    mistaken for a location actually collected in-game (see Core._ap_inventory_ready)."""

    quick_select: dict[str, int] = field(default_factory=dict)
    armour_slots: dict[str, int] = field(default_factory=dict)
    weapon_state: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict | None) -> RAC5SaveData:
        if not isinstance(data, dict):
            return cls()
        # Accept the old [level, experience] format, discarding experience.
        levels = {}
        raw = data.get("weapon_state")
        if isinstance(raw, dict):
            for name, value in raw.items():
                if isinstance(value, (list, tuple)) and len(value) == 2:
                    value = value[0]
                if name in WEAPON_MAX_LEVELS and type(value) is int and 0 <= value < WEAPON_MAX_LEVELS[name]:
                    levels[name] = value
        return cls(
            quick_select=dict(data.get("quick_select") or {}),
            armour_slots=dict(data.get("armour_slots") or {}),
            weapon_state=levels,
        )


def highest_weapon_levels(*snapshots: dict[str, int]) -> dict[str, int]:
    """Per-weapon highest valid level across `snapshots`. Levels never go down in normal play,
    so a lower reading is a bad write (or a stale copy) and must never be saved or restored."""
    levels: dict[str, int] = {}
    for snapshot in snapshots:
        for name, value in snapshot.items():
            if name not in WEAPON_MAX_LEVELS or type(value) is not int:
                continue
            if 0 <= value < WEAPON_MAX_LEVELS[name] and value > levels.get(name, -1):
                levels[name] = value
    return levels
