from __future__ import annotations

import asyncio
import time

from CommonClient import logger

_AMMO_LINK_PUSH_INTERVAL: float = 0.5


class AmmoLinkMixin:
    """Mirrors weapon ammo counts across every linked player as a straight overwrite (not a shared pool).
    Only weapons a player currently owns are read/written, keyed by weapon name."""

    def _ammo_link_key(self) -> str:
        return f"rsm_ammo_link_{self.team}"

    async def _set_ammo_link_enabled(self, enabled: bool) -> None:
        self._ammo_link_enabled = enabled
        await self._update_link_tag("AmmoLink", enabled)
        if enabled and self.slot is not None:
            self.set_notify(self._ammo_link_key())
            await self.send_msgs([{"cmd": "Get", "keys": [self._ammo_link_key()]}])
        logger.info(f"[RAC] AmmoLink {'enabled' if enabled else 'disabled'}.")

    def _maybe_sync_ammo_link(self) -> None:
        if not self._ammo_link_enabled or self.slot is None or not self.pine_connected:
            return
        if not self._wiring.planet.is_ready:
            return
        if self._wiring.vendor.ammo_link_paused:
            return
        now = time.monotonic()
        if now - self._last_ammo_link_push < _AMMO_LINK_PUSH_INTERVAL:
            return
        weapons = self._wiring.planet.weapons
        current = {name: weapons.get_ammo(name) for name, owned in weapons.weapons.items() if owned}
        if current == self._pushed_ammo_link:
            return
        self._last_ammo_link_push = now
        self._pushed_ammo_link = current
        asyncio.create_task(self._push_ammo_link(current))

    async def _push_ammo_link(self, data: dict[str, int]) -> None:
        if self.slot is None:
            return
        await self.send_msgs([{
            "cmd": "Set",
            "key": self._ammo_link_key(),
            "default": {},
            "want_reply": False,
            "operations": [{"operation": "update", "value": data}],
        }])

    def _apply_ammo_link_update(self) -> None:
        """Runs under _pine_lock (see context.py's Retrieved/SetReply
        handler) — writes memory directly, so never call this loose."""
        if not self._ammo_link_enabled or not self._wiring.planet.is_ready:
            return
        if self._wiring.vendor.ammo_link_paused:
            return
        data = self.stored_data.get(self._ammo_link_key())
        if not isinstance(data, dict) or data == self._applied_ammo_link:
            return
        self._applied_ammo_link = dict(data)
        weapons = self._wiring.planet.weapons
        for name, value in data.items():
            if not isinstance(value, int) or not weapons.weapons.get(name):
                continue
            if weapons.get_ammo(name) != value:
                weapons.set_ammo(name, value)
        self._pushed_ammo_link = {
            name: weapons.get_ammo(name) for name, owned in weapons.weapons.items() if owned
        }
