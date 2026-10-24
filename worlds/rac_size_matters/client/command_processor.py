from typing import TYPE_CHECKING

from CommonClient import logger

from ..core.skins import Skin

try:
    from worlds.tracker.TrackerClient import TrackerCommandProcessor as ClientCommandProcessor
except ImportError:
    from CommonClient import ClientCommandProcessor

if TYPE_CHECKING:
    from .context import RACContext


class RACCommandProcessor(ClientCommandProcessor):
    """Parses commands here; anything touching the game runs as a cmd_* method in the PCSX2 worker."""

    ctx: "RACContext"

    def _cmd_reconnect(self) -> bool:
        """Reconnect to PCSX2 and re-apply received Archipelago items."""
        self.ctx.call_worker("cmd_reconnect")
        return True

    def _cmd_force_sync(self) -> bool:
        """Force the player's in-game state to match what was received from AP."""
        self.ctx.call_worker("cmd_force_sync")
        return True

    def _cmd_states(self) -> bool:
        """Print every active state."""
        self.ctx.call_worker("cmd_states")
        return True

    def _cmd_rac5_info(self) -> bool:
        """Print the current slot options, then every active state's repr."""
        self.ctx.call_worker("cmd_rac5_info")
        return True

    def _cmd_vendor_refresh(self) -> bool:
        """Debug: force-rewrite the vendor item list immediately, without waiting for the next tick."""
        self.ctx.call_worker("cmd_vendor_refresh")
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
        self.ctx.call_worker("cmd_skin", selected)
        return True

    def _cmd_skin_patch(self, state: str = "") -> bool:
        """Enable or disable the skin patch, including multiplayer skins: /skin_patch on|off.
        Reloads the current planet. Disabling equips Ratchet's default skin; item toasts and
        the connection warning share the skin hook, so they stop too while it is off."""
        choices = {"on": True, "enable": True, "off": False, "disable": False}
        state = state.lower().strip()
        if state and state not in choices:
            logger.info("[RAC] Use /skin_patch on|off.")
            return False
        self.ctx.call_worker("cmd_skin_patch", choices.get(state))
        return True

    def _cmd_apicon(self, style: str = "") -> bool:
        """Choose which Archipelago icon shows on vendor items: /apicon original (default), purple, blue, grey.
        No argument prints the current style. Applies next time a vendor item's icon is assigned."""
        self.ctx.call_worker("cmd_apicon", style.lower().strip())
        return True

    def _cmd_spawn_ghost(self) -> bool:
        """Spawn a static ghost clone of Ratchet at his current position
        (only on planets with confirmed Ghost Ratchet addresses)."""
        self.ctx.call_worker("cmd_spawn_ghost")
        return True

    def _cmd_debug(self) -> bool:
        """Toggle printing of state changes as they occur."""
        self.ctx.call_worker("cmd_debug")
        return True

    def _cmd_toggle_deathlink(self) -> bool:
        """Toggle DeathLink on or off for this session."""
        self.ctx.call_worker("cmd_toggle_deathlink")
        return True

    def _cmd_toggle_ammolink(self) -> bool:
        """Toggle AmmoLink on or off for this session."""
        self.ctx.call_worker("cmd_toggle_ammolink")
        return True

    def _cmd_toggle_boltlink(self) -> bool:
        """Toggle BoltLink on or off for this session."""
        self.ctx.call_worker("cmd_toggle_boltlink")
        return True
