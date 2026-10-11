from .address_maps import save_address
from .traps import set_clank_pack_ownership
from dataclasses import dataclass

from ..constants import Rac5Locations
from .armour import ARMOUR_FLAG_TO_LOCATION, ArmourPiece
from .planets import AUTO_UNLOCK_ADDRESSES, INFOBOT_UNLOCK_VALUE

_SCRIPTED_GADGET_LOCATIONS = {"sprout_o_matic": Rac5Locations.RYLLUS_SPROUT, "shrink_ray": Rac5Locations.KALIDON_SHRINK}


@dataclass
class InventorySync:
    core: object

    def apply_inventory(
        self,
        *,
        weapons: dict[str, bool],
        gadgets: dict[str, bool],
        weapon_levels: dict[str, int],
        weapon_mods: dict[str, set[str]],
        armour_unlocked: dict[str, int],
        infobot_planets: set[str],
        challenge_mode: int = 0,
        clank_pack: bool = False,
    ) -> None:
        """Write a fully-rebuilt AP inventory snapshot into game memory every tick."""
        core = self.core
        if core._refresh_main_menu_state():
            return
        core._ap_inventory_ready = True
        set_clank_pack_ownership(
            core.pine, enabled=core.options.clank_pack_enabled, owned=clank_pack
        )
        core.planet_unlock.set_unlocked_planets(infobot_planets)
        if core.progressive_challenge_mode_enabled:
            core.planet.weapons.challenge_mode = challenge_mode
            core.vendor.challenge_mode = challenge_mode
            core.challenge_mode.set_by_option(challenge_mode)
        core.armour.set_ap_armour(armour_unlocked)
        if (
            core.planet.is_ready
            and (not core.vendor_active)
            and (not core.planet.player.is_dead)
            and (not core.planet.player.is_picking_up)
            and (not core.planet.giant_clank_active)
        ):
            core._report_new_armour_pickups()
            core.armour.apply_full()
        core._ap_owned_weapons = dict(weapons)
        core._ap_owned_gadgets = dict(gadgets)
        core.planet.weapons.level_caps = dict(weapon_levels)
        if not core.planet.weapons_available or core.vendor_active:
            return
        wi = core.planet.weapons
        with wi.memory():
            for name, owned in weapons.items():
                if owned:
                    wi.set(name, True)
            for name, owned in gadgets.items():
                if owned:
                    wi.set(name, True)
            for name, slots in weapon_mods.items():
                for slot in slots:
                    wi.set_mod(name, slot, True)
            wi.sync_slots()
            core._sync_weapon_gadget_ownership()

    def _sync_weapon_gadget_ownership(self) -> None:
        """Forces every weapon/gadget's unlocked bit back to true AP ownership."""
        core = self.core
        wi = core.planet.weapons
        for name in wi._weapon_addrs:
            owned = core._ap_owned_weapons.get(name, False)
            if wi.weapons.get(name, False) != owned:
                wi.set(name, owned)
                wi.weapons[name] = owned
                wi._raw_weapons[name] = owned
        for name in wi._gadget_addrs:
            owned = core._ap_owned_gadgets.get(name, False)
            if wi.gadgets.get(name, False) != owned:
                if not owned and core._planet_settled():
                    loc = _SCRIPTED_GADGET_LOCATIONS.get(name)
                    if loc and (not (core.native.pickup is not None and loc == Rac5Locations.RYLLUS_SPROUT)):
                        core.send_location(loc)
                wi.set(name, owned)
                wi.gadgets[name] = owned
                wi._raw_gadgets[name] = owned

    def restore_world_states(self, checked_locations: set[str]) -> None:
        core = self.core
        core.bolts.sync_from_ap(checked_locations)
        core.skill_points.sync_from_ap(checked_locations)
        if core._refresh_main_menu_state():
            return
        core.bolts.sync()
        core.skill_points.sync()
        for address in AUTO_UNLOCK_ADDRESSES:
            core.pine.write_int8(save_address(address), INFOBOT_UNLOCK_VALUE)

    def restore_armour_from_locations(self, checked_locations: set[str]) -> None:
        """Seed armour.game_armour from already-checked AP locations so a reconnect
        doesn't re-detect a pickup. Deliberately does not write game memory."""
        core = self.core
        loc_to_flag = {v: k for k, v in ARMOUR_FLAG_TO_LOCATION.items()}
        pieces: dict[str, ArmourPiece] = {}
        for loc_name in checked_locations:
            flag = loc_to_flag.get(loc_name)
            if flag:
                set_key, piece = flag
                pieces[set_key] = pieces.get(set_key, ArmourPiece.NONE) | piece
        if pieces:
            core.armour.record_pickup(pieces)

    def sync_from_ap(self, checked_locations: set[str]) -> None:
        """Fold already-checked AP locations into every completion-tracking Inventory
        so a reconnect doesn't re-report anything the server already knows."""
        core = self.core
        core.native.checked.update(checked_locations)
        core.clank.sync_from_ap(checked_locations)
        core.skyboard.sync_from_ap(checked_locations)
        core.shrink_ray.sync_from_ap(checked_locations)
        core.planet.weapons.sync_from_ap(checked_locations)
        core.skill_points.sync_from_ap(checked_locations)
        core.missions.sync_from_ap(checked_locations)
        core.restore_armour_from_locations(checked_locations)
