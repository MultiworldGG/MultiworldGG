from __future__ import annotations

import random
from collections import Counter

from ..core import (
    ALL_TRAPS,
    INFOBOT_ITEM_TO_PLANET,
    WEAPON_MAX_LEVELS,
    activate_trap,
)
from ..core import address_maps
from ..core.menu import MenuStateValue
from ..core.address_maps import PLAYER_BOLT_COUNT
from ..core.notifications import receipt_text, sent_text
from ..core.player_bolts import MAX_PLAYER_BOLTS
from ..items import (
    ARMOUR_DISPLAY_TO_INTERNAL,
    ARMOUR_PIECE_BITMASKS,
    ARMOUR_SET_DISPLAY_TO_INTERNAL,
    ARMOUR_SETS,
    CLANK_PACK_NAME,
    GADGET_DISPLAY_TO_INTERNAL,
    PROGRESSIVE_ARMOUR_NAME,
    PROGRESSIVE_ARMOUR_UNIFIED_NAME,
    PROGRESSIVE_CHALLENGE_MODE_NAME,
    PROGRESSIVE_MOD_NAME,
    PROGRESSIVE_WEAPON_NAME,
    WEAPON_DISPLAY_TO_INTERNAL,
    WEAPON_MOD_NAME_TO_SLOT,
)
from ..locations import GADGET_INTERNAL_TO_LOCATION, WEAPON_INTERNAL_TO_LOCATION

PROGRESSIVE_WEAPON_NAME_REVERSE = {v: k for k, v in PROGRESSIVE_WEAPON_NAME.items()}
PROGRESSIVE_ARMOUR_NAME_REVERSE = {v: k for k, v in PROGRESSIVE_ARMOUR_NAME.items()}
PROGRESSIVE_MOD_NAME_REVERSE = {v: k for k, v in PROGRESSIVE_MOD_NAME.items()}

_SLOT_ATTR: dict[int, str] = {1: "mod_slot_one", 2: "mod_slot_two", 3: "mod_slot_three"}


class VendorHandlerMixin:
    async def _send_vendor_hints(self) -> None:
        """Send AP location hints for all currently purchasable vendor items, skipping locations
        already hinted or checked. Whichever vendor menu is active decides which list to hint."""
        if self.slot is None or not self.pine_connected:
            return
        vendor = self._wiring.vendor
        if self._wiring.planet.menu.get() == MenuStateValue.PDA:
            return
        if self._wiring.weapon_vendor.active:
            loc_names = vendor.purchasable_locations()
        elif self._wiring.mod_vendor.active:
            loc_names = vendor.mod_locations()
        else:
            return
        checked   = self.checked_locations | self._locally_checked_locations
        server_locations = getattr(self, "server_locations", None)
        new_ids: list[int] = []
        for name in loc_names:
            loc_id = self._location_name_to_id.get(name)
            if loc_id is None or loc_id in self._already_hinted or loc_id in checked:
                continue
            if server_locations is not None and loc_id not in server_locations:
                continue
            new_ids.append(loc_id)
        if not new_ids:
            return
        await self.send_msgs([
            {"cmd": "LocationScouts", "locations": new_ids, "create_as_hint": 2}
        ])
        self._already_hinted.update(new_ids)



class InventoryMixin:
    def _parse_inventory(self) -> dict:
        """Rebuild the full AP inventory snapshot from items_received."""
        weapon_prog_counts:     dict[str, int] = {}
        weapon_mod_prog_counts: dict[str, int] = {}
        armour_prog_counts:     dict[str, int] = {}
        unified_armour_count = 0
        challenge_mode_count = 0
        clank_pack = False
        weapon_unlocked:  dict[str, bool]     = {}
        gadget_unlocked:  dict[str, bool]     = {}
        weapon_mod_slots: dict[str, set[str]] = {}
        armour_unlocked:  dict[str, int]      = {}
        infobot_planets:  set[str]            = set()

        for network_item in self.items_received:
            item_name = self.item_names[self.game].get(network_item.item, "")
            if item_name == CLANK_PACK_NAME:
                clank_pack = True
                continue
            if item_name == "Infobot: Pokitaru and Ryllus":
                infobot_planets.update(("POKITARU", "RYLLUS"))
                continue

            if item_name in PROGRESSIVE_WEAPON_NAME_REVERSE:
                display = PROGRESSIVE_WEAPON_NAME_REVERSE[item_name]
                weapon_prog_counts[display] = weapon_prog_counts.get(display, 0) + 1
                continue
            if item_name in PROGRESSIVE_MOD_NAME_REVERSE:
                display = PROGRESSIVE_MOD_NAME_REVERSE[item_name]
                weapon_mod_prog_counts[display] = weapon_mod_prog_counts.get(display, 0) + 1
                continue
            if item_name in WEAPON_MOD_NAME_TO_SLOT:
                mod_display, slot = WEAPON_MOD_NAME_TO_SLOT[item_name]
                mod_internal = WEAPON_DISPLAY_TO_INTERNAL.get(mod_display)
                if mod_internal:
                    weapon_mod_slots.setdefault(mod_internal, set()).add(_SLOT_ATTR[slot])
                continue
            if item_name == PROGRESSIVE_ARMOUR_UNIFIED_NAME:
                unified_armour_count += 1
                continue
            if item_name == PROGRESSIVE_CHALLENGE_MODE_NAME:
                challenge_mode_count += 1
                continue
            if item_name in PROGRESSIVE_ARMOUR_NAME_REVERSE:
                display = PROGRESSIVE_ARMOUR_NAME_REVERSE[item_name]
                armour_prog_counts[display] = armour_prog_counts.get(display, 0) + 1
                continue

            if item_name in INFOBOT_ITEM_TO_PLANET:
                infobot_planets.update(planet.upper() for planet in INFOBOT_ITEM_TO_PLANET[item_name])
            elif item_name in WEAPON_DISPLAY_TO_INTERNAL:
                weapon_unlocked[WEAPON_DISPLAY_TO_INTERNAL[item_name]] = True
            elif item_name in GADGET_DISPLAY_TO_INTERNAL:
                gadget_unlocked[GADGET_DISPLAY_TO_INTERNAL[item_name]] = True
            elif item_name in ARMOUR_DISPLAY_TO_INTERNAL:
                set_key, piece = ARMOUR_DISPLAY_TO_INTERNAL[item_name]
                armour_unlocked[set_key] = armour_unlocked.get(set_key, 0) | int(piece)

        for display, count in armour_prog_counts.items():
            internal = ARMOUR_SET_DISPLAY_TO_INTERNAL.get(display)
            if not internal:
                continue
            bitmask = 0
            for i, bit in enumerate(ARMOUR_PIECE_BITMASKS):
                if i < count:
                    bitmask |= bit
            armour_unlocked[internal] = armour_unlocked.get(internal, 0) | bitmask

        remaining = unified_armour_count
        for _display, internal in ARMOUR_SETS:
            if remaining <= 0:
                break
            pieces = min(remaining, len(ARMOUR_PIECE_BITMASKS))
            bitmask = 0
            for i, bit in enumerate(ARMOUR_PIECE_BITMASKS):
                if i < pieces:
                    bitmask |= bit
            armour_unlocked[internal] = armour_unlocked.get(internal, 0) | bitmask
            remaining -= pieces

        weapon_levels: dict[str, int] = {}
        for display, count in weapon_prog_counts.items():
            internal = WEAPON_DISPLAY_TO_INTERNAL.get(display)
            if not internal:
                continue
            if count >= 1:
                weapon_unlocked[internal] = True
            weapon_levels[internal] = min(max(0, count - 1), WEAPON_MAX_LEVELS.get(internal, 1) - 1)

        for display, count in weapon_mod_prog_counts.items():
            internal = WEAPON_DISPLAY_TO_INTERNAL.get(display)
            if not internal:
                continue
            slots = {_SLOT_ATTR[i] for i in range(1, count + 1) if i in _SLOT_ATTR}
            weapon_mod_slots.setdefault(internal, set()).update(slots)

        return {
            "weapons":         weapon_unlocked,
            "gadgets":         gadget_unlocked,
            "weapon_levels":   weapon_levels,
            "weapon_mods":     weapon_mod_slots,
            "armour_unlocked": armour_unlocked,
            "infobot_planets": infobot_planets,
            "challenge_mode":  challenge_mode_count,
            "clank_pack":      clank_pack,
        }

    def _sync_vendor_rule_items(self) -> None:
        vendor = self._wiring.vendor
        items = Counter(self.item_names[self.game].get(item.item, "") for item in self.items_received)
        if items != vendor.rule_items:
            vendor.rule_items = items
            if vendor.location_rules is not None:
                vendor.force_refresh()

    async def force_sync(self) -> None:
        """Force the player's in-game state to match AP, wiping the current planet's weapon/gadget/mod
        array first. Skipped if the planet isn't ready or a vendor is open, which already zero/restore.
        Also skipped entirely while no save is loaded (see Core.at_main_menu) — apply_inventory()/
        restore_world_states() already no-op in that case, but weapons.wipe() below doesn't
        go through either of them and would otherwise write to a stale/invalid planet base."""
        if not self.pine_connected or not self._items_received_ready or not self._save_data_received:
            return
        inventory = self._parse_inventory()
        checked   = self._checked_location_names()
        async with self._pine_lock:
            wiring = self._wiring
            if wiring.at_main_menu:
                return
            if wiring.planet.weapons_available and not wiring.vendor_active:
                wiring.planet.weapons.wipe()
            wiring.apply_inventory(**inventory)
            self._sync_vendor_rule_items()
            wiring.restore_world_states(checked)
            wiring.restore_armour_from_locations(checked)
            self._try_restore_weapon_state(force=True)
            if wiring.planet.is_ready and not wiring.vendor_active:
                self._connection_sync_pending = False
        self._pending_item_apply = False

    async def _apply_received_items(self) -> None:
        if not self._items_received_ready or not self._save_data_received:
            self._pending_item_apply = True
            return
        if self._wiring.native.waiting:
            self._pending_item_apply = True
            return
        if not self.pine_connected:
            self._pending_item_apply = True
            return
        if self._wiring.at_main_menu:
            self._pending_item_apply = True
            return
        inventory = self._parse_inventory()
        async with self._pine_lock:
            self._wiring.apply_inventory(**inventory)
            self._sync_vendor_rule_items()
            if self.items_received and self._filler_checkpoint_synced:
                self._grant_new_bolt_items()
                self._grant_new_trap_items()
                await self._persist_filler_checkpoint()
        self._show_new_item_notifications()
        self._pending_item_apply = False

    async def _persist_filler_checkpoint(self) -> None:
        """Persist how far into items_received bolts/traps have been granted, so a restart can resume.
        Uses "max" rather than "replace" to guard against racing a stale read of the checkpoint."""
        checkpoint = max(self._processed_item_count, self._processed_trap_count)
        await self.send_msgs([{
            "cmd": "Set",
            "key": self._filler_applied_key(),
            "default": 0,
            "want_reply": False,
            "operations": [{"operation": "max", "value": checkpoint}],
        }])

    async def _restore_world_states(self) -> None:
        """Seed and apply bolt/skill-point/armour state from already-checked
        locations. Called only on connection events (crash recovery)."""
        if not self.pine_connected:
            return
        checked = self._checked_location_names()
        async with self._pine_lock:
            self._wiring.restore_world_states(checked)
            self._wiring.restore_armour_from_locations(checked)


    def _grant_random_bonus_item(self, trigger_name: str) -> None:
        """Called when lacerator/acid_bomb_glove/concussion_gun's unlocked bit transitions 0->1, from
        either a real pickup or our own re-apply. Guards on the *location* since a precollected
        weapon's resync write flips the bit before the real pickup happens."""
        if not self.pine_connected or not self._wiring.planet.is_ready:
            return
        wi = self._wiring.planet.weapons
        loc = WEAPON_INTERNAL_TO_LOCATION.get(trigger_name)
        already_checked = loc is not None and loc in self._checked_location_names()
        if already_checked:
            return
        if loc:
            self._log(f"[RAC] Intro weapon picked: {trigger_name!r} -> loc={loc!r}")
            self._append_location_by_name(loc)
        candidates = [name for name in wi.weapons if wi.weapons[name] and name != trigger_name]
        candidates += [name for name in wi.gadgets if wi.gadgets[name]]
        if not candidates:
            return
        wi.set(random.choice(candidates), True)

    def _handle_scripted_gadget_pickup(self, trigger_name: str) -> None:
        """Called when hypershot's unlocked bit transitions 0->1 during Pokitaru's scripted tutorial.
        Same already-checked-location guard as _grant_random_bonus_item, for the same reason."""
        if not self.pine_connected or not self._wiring.planet.is_ready:
            return
        loc = GADGET_INTERNAL_TO_LOCATION.get(trigger_name)
        if loc is not None and loc in self._checked_location_names():
            return
        if loc:
            self._log(f"[RAC] Intro gadget picked: {trigger_name!r} -> loc={loc!r}")
            self._append_location_by_name(loc)

    def _write_notification_text(self, msg: bytes) -> None:
        if not self.pine_connected:
            return
        self._wiring.notify(msg)

    def _show_new_item_notifications(self) -> None:
        new_items = self.items_received[self._notification_item_index:]
        self._notification_item_index = len(self.items_received)
        if not new_items or not self.pine_connected:
            return
        for net_item in new_items:
            item_name = self.item_names[self.game].get(net_item.item, "???")
            player_name = self.player_names.get(net_item.player, f"Player {net_item.player}")
            self._write_notification_text(receipt_text(item_name, player_name, bool(net_item.flags & 4)))

    def _show_item_send_notification(self, net_item, receiving: int) -> None:
        """Called from on_print_json for a live ItemSend where this slot is the sender --
        mirrors _show_new_item_notifications' receipt toast, but for the outgoing side."""
        if not self.pine_connected or receiving == self.slot:
            return
        receiver_game = self.slot_info[receiving].game if receiving in self.slot_info else self.game
        item_name = self.item_names[receiver_game].get(net_item.item, "???")
        player_name = self.player_names.get(receiving, f"Player {receiving}")
        self._write_notification_text(sent_text(item_name, player_name))

    def _grant_new_bolt_items(self) -> None:
        starting_bolts = int(self.slot_data.get("starting_bolts", 0))
        skipped_precollected = self._processed_item_count != 0
        new_items = self.items_received[self._processed_item_count:]
        self._processed_item_count = len(self.items_received)

        bolt_items_to_grant = 0
        for network_item in new_items:
            item_name = self.item_names[self.game].get(network_item.item, "")
            if item_name != "Bolts":
                continue
            if starting_bolts and not skipped_precollected:
                skipped_precollected = True
                continue
            bolt_items_to_grant += 1

        if bolt_items_to_grant <= 0 or not self.pine_connected:
            return
        try:
            current = self.pine.read_int32(address_maps.PLAYER_BOLT_COUNT)
            for _ in range(bolt_items_to_grant):
                grant = min(200000, max(35000, int(current * 0.2)))
                current = min(current + grant, MAX_PLAYER_BOLTS)
            self.pine.write_int32(address_maps.PLAYER_BOLT_COUNT, current)
            self._wiring.player_bolts.rebaseline(current)
        except Exception as exc:
            self._log(f"[RAC] Could not grant bolts: {exc}", "warning")

    def _grant_new_trap_items(self) -> None:
        new_items = self.items_received[self._processed_trap_count:]
        self._processed_trap_count = len(self.items_received)

        if not self.pine_connected:
            return
        for network_item in new_items:
            item_name = self.item_names[self.game].get(network_item.item, "")
            if item_name not in ALL_TRAPS:
                continue
            try:
                activate_trap(self.pine, item_name)
            except Exception as exc:
                self._log(f"[RAC] Could not activate trap {item_name!r}: {exc}", "warning")
