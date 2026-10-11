from __future__ import annotations

import asyncio
import random
import time
from typing import Any

from CommonClient import logger
from ..core import address_maps

from ..core import (
    PlayerMovementState as PlayerState,
    TextColour,
    colored_text,
)

_DEATH_CAUSES: dict[PlayerState, list[str]] = {
    PlayerState.FishDeath: [
        "got eaten by a fish",
        "tried to swim with the fishes",
        "became an aquatic creature's lunch",
        "found out fish bite back",
    ],
    PlayerState.FadeDeath: [
        "was faded out of existence",
        "ceased to exist, briefly",
        "got erased from reality",
        "found the off switch for themselves",
    ],
    PlayerState.Electrocution: [
        "got electrocuted",
        "touched the wrong wire",
        "became a lightning rod",
        "found out electricity is not their friend",
    ],
    PlayerState.VoidDeath: [
        "fell out of the world",
        "discovered the world has edges",
        "took a step too far",
        "found a shortcut to the void",
    ],
    PlayerState.UnknownDeath: [
        "met an untimely end",
        "had a very bad day",
        "encountered something unfortunate",
        "lost a fight with the universe",
    ],
    PlayerState.SwimDeath: [
        "tried to swim in lava",
        "thought lava was just spicy water",
        "went for a relaxing lava bath",
        "underestimated the temperature of magma",
    ],
    PlayerState.MysteriousDeath: [
        "died under mysterious circumstances",
        "departed this world inexplicably",
        "achieved death through unknown means",
        "was claimed by forces beyond comprehension",
    ],
}


def _dead(player_state: int) -> bool:
    return PlayerState.is_dead(player_state)


def _death_cause(player_state: int) -> str:
    causes = _DEATH_CAUSES.get(player_state)
    return random.choice(causes) if causes else "died"


class DeathLinkMixin:
    async def _set_death_link_enabled(self, enabled: bool) -> None:
        """Toggle DeathLink at runtime, updating both the local gate flag and
        the server-side "DeathLink" connection tag."""
        self._death_link_enabled = enabled
        await self.update_death_link(enabled)
        logger.info(f"[RAC] DeathLink {'enabled' if enabled else 'disabled'}.")

    def _send_death_link_from_sync(self, player_state: int) -> None:
        if not self._death_link_enabled:
            return
        now = time.time()
        if now - self._last_death_link < 1:
            return
        self._last_death_link = now
        logger.info("[RAC] DeathLink sent.")
        source = self.auth or "Ratchet"
        planet_name = self.current_planet or "an unknown planet"
        cause_text = _death_cause(player_state)
        self._write_notification_text(colored_text(
            TextColour.RED, "Deathlink: ", source, TextColour.WHITE, " ", cause_text,
        ))
        asyncio.create_task(
            self.send_msgs([
                {
                    "cmd": "Bounce",
                    "tags": ["DeathLink"],
                    "data": {
                        "time": now,
                        "source": source,
                        "cause": f"{source} {cause_text} on {planet_name}.",
                    },
                }
            ])
        )

    async def _receive_death_link(self, data: dict[str, Any]) -> None:
        if not self.pine_connected:
            return
        timestamp = float(data.get("time", 0))
        if timestamp and timestamp <= self._last_death_link:
            return
        self._last_death_link = max(timestamp, time.time())
        source = data.get("source", "Unknown")
        cause  = data.get("cause") or f"{source} died"
        self._log(f"[RAC] DeathLink received: {cause}")
        self._write_notification_text(colored_text(
            TextColour.RED, "Deathlink: ", source, TextColour.WHITE, " ", cause,
        ))
        async with self._pine_lock:
            self._kill_player_sync()

    def _kill_player_sync(self) -> None:
        if self._wiring.at_main_menu:
            return
        planet_id = self._wiring.planet.planet_id
        state_addr, health_addr = address_maps.PLAYER_ADDRS.get(planet_id, (address_maps.PLAYER_STATE, address_maps.PLAYER_HEALTH))
        death_state = random.choice(list(_DEATH_CAUSES))
        self.pine.write_int16(state_addr, death_state)
        self.pine.write_int16(health_addr, 0)
