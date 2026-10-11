from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from CommonClient import logger

from ..core import vendor_presentation
from ..core.skins import Skin

try:
    from worlds.tracker.TrackerClient import TrackerCommandProcessor as ClientCommandProcessor
except ImportError:
    from CommonClient import ClientCommandProcessor

if TYPE_CHECKING:
    from .context import RACContext


class RACCommandProcessor(ClientCommandProcessor):
    ctx: RACContext

    def _cmd_reconnect(self) -> bool:
        """Reconnect to PCSX2 and re-apply received Archipelago items."""
        asyncio.create_task(self.ctx.reconnect_pine())
        return True

    def _cmd_force_sync(self) -> bool:
        """Force the player's in-game state to match what was received from AP."""
        asyncio.create_task(self.ctx.force_sync())
        return True

    def _cmd_states(self) -> bool:
        """Print every active state."""
        w = self.ctx._wiring
        for state in (
            w.armour, w.bolts, w.player_bolts, w.planet_unlock, w.quick_select,
            w.clank, w.skyboard, w.shrink_ray, w.skill_points, w.missions, w.skin,
            w.planet, w.planet.weapons, w.planet.player, w.planet.menu,
            w.weapon_vendor, w.mod_vendor, w.vendor,
        ):
            logger.info(repr(state))
        return True

    def _cmd_rac5_info(self) -> bool:
        """Print the current slot options, then every active state's repr."""
        ctx = self.ctx
        options = "\n".join(f"{key}: {value}" for key, value in ctx.slot_data.items())
        logger.info(f"[RAC] Options:\n{options}")

        w = ctx._wiring
        states = (
            w.armour, w.bolts, w.player_bolts, w.planet_unlock, w.quick_select,
            w.clank, w.skyboard, w.shrink_ray, w.skill_points, w.missions, w.skin,
            w.planet, w.planet.weapons, w.planet.player, w.planet.menu,
            w.weapon_vendor, w.mod_vendor, w.vendor,
        )
        logger.info("[RAC] States: " + " ".join(repr(state) for state in states))
        return True

    def _cmd_vendor_refresh(self) -> bool:
        """Debug: force-rewrite the vendor item list immediately, without waiting for the next tick."""
        w = self.ctx._wiring
        w.vendor.force_refresh()
        logger.info(f"[RAC] {w.vendor!r}")
        return True

    def _cmd_skin(self, skin: str = "") -> bool:
        """Set a skin directly: /skin trash, /skin tuxedo, or an id 0-19."""
        names = {s.name.lower(): s for s in Skin}
        names.update({s.name.lower().removesuffix("_ratchet"): s for s in Skin})
        names.update({str(s.equip_id): s for s in Skin})
        selected = names.get(skin.lower().replace("-", "_").replace(" ", "_"))
        if selected is None:
            logger.info("[RAC] /skin default|pirate|trash|tuxedo|qwark|ninja (or 0-19). "
                        "Multiplayer skins use their red variant.")
            return False
        if not self.ctx.pine_connected or self.ctx._wiring is None:
            logger.info("[RAC] Connect to PCSX2 before changing skins.")
            return False
        if selected.unlock_mask is None and not self.ctx._wiring.native.patch_options.multiplayer_skins:
            logger.info("[RAC] Multiplayer skins need Experimental Skins enabled in your YAML.")
            return False
        asyncio.create_task(self.ctx._guarded_wiring_call(
            lambda: self.ctx._wiring.skin.set(selected)))
        logger.info("[RAC] Skin queued: %s. Applies when gameplay is ready.", selected.name)
        return True

    def _cmd_apicon(self, style: str = "") -> bool:
        """Choose which Archipelago icon shows on vendor items: /apicon original (default), purple, blue, grey.
        No argument prints the current style. Applies next time a vendor item's icon is assigned."""
        style = style.lower().strip()
        if not style:
            logger.info(f"[RAC] AP icon style: {vendor_presentation.get_icon_style()}. "
                        f"Choices: {', '.join(vendor_presentation.ICON_STYLES)}")
            return True
        try:
            vendor_presentation.set_icon_style(style)
        except ValueError as e:
            logger.info(f"[RAC] {e}")
            return False
        self.ctx._ap_icon_chosen_by_command = True
        logger.info(f"[RAC] AP icon style set to {vendor_presentation.get_icon_style()}.")
        return True

    def _cmd_spawn_ghost(self) -> bool:
        """Spawn a static ghost clone of Ratchet at his current position
        (only on planets with confirmed Ghost Ratchet addresses)."""
        w = self.ctx._wiring
        if w.spawn_ghost_ratchet():
            logger.info("[RAC] Ghost Ratchet spawned.")
        else:
            logger.info("[RAC] Ghost Ratchet isn't available on this planet yet.")
        return True

    def _cmd_debug(self) -> bool:
        """Toggle printing of state changes as they occur."""
        self.ctx._debug_messages = not self.ctx._debug_messages
        state = "enabled" if self.ctx._debug_messages else "disabled"
        logger.info(f"[RAC] Debug messages {state}.")
        return True

    def _cmd_toggle_deathlink(self) -> bool:
        """Toggle DeathLink on or off for this session."""
        asyncio.create_task(self.ctx._set_death_link_enabled(not self.ctx._death_link_enabled))
        return True

    def _cmd_toggle_ammolink(self) -> bool:
        """Toggle AmmoLink on or off for this session."""
        asyncio.create_task(self.ctx._set_ammo_link_enabled(not self.ctx._ammo_link_enabled))
        return True

    def _cmd_toggle_boltlink(self) -> bool:
        """Toggle BoltLink on or off for this session."""
        asyncio.create_task(self.ctx._set_bolt_link_enabled(not self.ctx._bolt_link_enabled))
        return True
