from __future__ import annotations

import asyncio
import time

from CommonClient import logger

_BOLT_LINK_PUSH_INTERVAL: float = 0.5


class BoltLinkMixin:
    """Mirrors the player's bolt count across every linked player, same absolute-value model as AmmoLink/DeathLink."""

    def _bolt_link_key(self) -> str:
        return f"rsm_bolt_link_{self.team}"

    async def _set_bolt_link_enabled(self, enabled: bool) -> None:
        self._bolt_link_enabled = enabled
        await self._update_link_tag("BoltLink", enabled)
        if enabled and self.slot is not None:
            self.set_notify(self._bolt_link_key())
            await self.send_msgs([{"cmd": "Get", "keys": [self._bolt_link_key()]}])
        logger.info(f"[RAC] BoltLink {'enabled' if enabled else 'disabled'}.")

    def _maybe_sync_bolt_link(self) -> None:
        if not self._bolt_link_enabled or self.slot is None or not self.pine_connected:
            return
        if not self._wiring.planet.is_ready:
            return
        now = time.monotonic()
        if now - self._last_bolt_link_push < _BOLT_LINK_PUSH_INTERVAL:
            return
        current = self._wiring.player_bolts.get()
        if current == self._pushed_bolt_link:
            return
        self._last_bolt_link_push = now
        self._pushed_bolt_link = current
        asyncio.create_task(self._push_bolt_link(current))

    async def _push_bolt_link(self, value: int) -> None:
        if self.slot is None:
            return
        await self.send_msgs([{
            "cmd": "Set",
            "key": self._bolt_link_key(),
            "default": 0,
            "want_reply": False,
            "operations": [{"operation": "replace", "value": value}],
        }])

    def _apply_bolt_link_update(self) -> None:
        """Runs under _pine_lock (see context.py's Retrieved/SetReply
        handler) — writes memory directly, so never call this loose."""
        if not self._bolt_link_enabled or not self._wiring.planet.is_ready:
            return
        value = self.stored_data.get(self._bolt_link_key())
        if not isinstance(value, int) or value == self._pushed_bolt_link:
            return
        bolts = self._wiring.player_bolts
        if bolts.get() != value:
            bolts.set(value)
            bolts.rebaseline(value)
        self._pushed_bolt_link = value
