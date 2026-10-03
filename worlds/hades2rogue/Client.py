import asyncio
from typing import Optional

import Utils
from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, handle_url_arg, server_loop

from . import Tracker
from .Items import ASPECT_MAX_RANK

# Universal Tracker integration: if the player has separately installed the real
# Universal Tracker (github.com/FarisTheAncient/Archipelago, distributed as
# tracker.apworld), inherit its context/command processor instead of the plain ones so
# its own Tracker tab (real reachability, using this apworld's own Rules.py via a solo
# regen) attaches to this client automatically -- same pattern real game clients with UT
# support use (e.g. Lego Star Wars: The Complete Saga's client). Falls back to the
# ordinary classes when it isn't installed.
try:
    from worlds.tracker.TrackerClient import (
        TrackerGameContext as CommonContext,
        TrackerCommandProcessor as ClientCommandProcessor,
    )
except ImportError:
    from CommonClient import CommonContext, ClientCommandProcessor
    UNIVERSAL_TRACKER_LOADED = False
else:
    UNIVERSAL_TRACKER_LOADED = True


# --- Local bridge to the in-game Lua mod -------------------------------------
BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 43055

# Compared against slot_data's version_check (set from Hades2World.mod_version) on connect.
# KEEP IN STEP with __init__.py's mod_version and the mod's manifest.json on every release.
MOD_VERSION = "0.10.0"


def _wire_text(text) -> str:
    """Free text from other players (slot names, other games' item names) made safe for the
    bridge's line protocol: every message ends at a newline, and ITEMS/CHECKED split on "|" and
    "~". Our own item and location names never contain these."""
    return str(text).replace("\r", " ").replace("\n", " ").replace("|", "/").replace("~", "-")


class Hades2CommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Resend settings and all received items to the game."""
        Utils.async_start(self.ctx.sync_mod())

    def _cmd_bridge(self):
        """Report whether the game (Lua mod) is connected to this client."""
        if self.ctx.bridge_server is None:
            logger.info(
                f"Game bridge: NOT LISTENING on {BRIDGE_HOST}:{BRIDGE_PORT} -- the port is "
                "likely held by another process (a stale client from a previous launch?). "
                "Check the log above for 'couldn't bind' retry messages.")
        elif self.ctx.bridge_writer is not None:
            logger.info(f"Game bridge: connected (listening on {BRIDGE_HOST}:{BRIDGE_PORT}).")
        else:
            logger.info(
                f"Game bridge: listening on {BRIDGE_HOST}:{BRIDGE_PORT}, but the game hasn't "
                "connected yet. Check the game's ReturnOfModding LogOutput.log for '[AP]' lines "
                "-- look for 'LuaSocket unavailable' or a missing 'render driver alive' heartbeat.")

    def _cmd_deathlink(self):
        """Toggle Death Link, overriding the YAML setting for this session."""
        self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
        Utils.async_start(self.ctx.update_death_link(self.ctx.deathlink_enabled))
        logger.info(f"Death Link: {'enabled' if self.ctx.deathlink_enabled else 'disabled'}")

    def _cmd_death(self):
        """Test-only: push a DeathLink to the game directly, without telling the AP server
        or any other player. Use this to verify the mod's death-handling in isolation."""
        logger.info("Sending a local test DeathLink to the game (not sent to the server or other players).")
        self.ctx._forward_death_to_mod("Test")


class Hades2Context(CommonContext):
    command_processor = Hades2CommandProcessor
    game = "Hades2Rogue"
    items_handling = 0b111  # full remote
    mod_version = MOD_VERSION

    def __init__(self, server_address: Optional[str] = None, password: Optional[str] = None):
        super().__init__(server_address, password)
        # Universal Tracker's TrackerGameContext (our base class when UT is installed --
        # see the import block up top) defaults tags to include "Tracker", and its
        # disconnect() clobbers self.game to "" whenever that tag is present at
        # disconnect time. We never want tracker-style passthrough behavior, so strip it
        # here immediately rather than only inside server_auth(): a disconnect() firing
        # before server_auth() ever runs once (e.g. reusing this client across multiple
        # generated seeds without restarting it) would otherwise still see "Tracker" in
        # tags and permanently stamp an empty self.game on this instance, which then
        # sends a blank game on every future Connect and gets the server's "Invalid Game"
        # refusal even though nothing about our own game name ever changed.
        self.tags = set()
        self.slot_data: Optional[dict] = None
        self.location_name_to_id: dict = {}
        # Checks the mod sent before we finished connecting to the server (location_name_to_id is
        # only populated on Connected). Without buffering, such a check is dropped as "unknown"
        # AND never retried -- the mod's send_first marks it sent, so a one-time check (e.g.
        # "Met <NPC>", met at the Crossroads the instant a run loads) is lost until a manual
        # release. Held here and flushed on Connected. See the CHECK handler / _flush_pending_checks.
        self.pending_checks: list = []
        # location_id -> "<PlayerName> - <ItemName>", from LocationScouts (see scout_locations).
        # Lets the mod's subtle corner log show who got what when a check is sent.
        self.scouted: dict = {}
        self.deathlink_enabled = False
        self.deathlink_pending = False
        # A DeathLink that arrived while the game wasn't connected to the bridge (very common
        # right after a reboot: the client reaches the AP server in ~1s but the game takes tens
        # of seconds to launch and connect the local bridge). Held here instead of being dropped
        # silently, and flushed to the mod the moment the game connects (on its HELLO handshake).
        # A bool, not a count: owing one death is enough -- we don't want to insta-kill the
        # player repeatedly on reconnect after a long disconnect.
        self.pending_mod_death = False
        # Sender's slot name for the held DeathLink above, so the mod can still show who killed
        # us once it's flushed on HELLO. "Archipelago" if the bounce never carried one.
        self.pending_death_source = "Archipelago"

        # Most recent REAL per-boss clears/weapon-variety from the mod's VICTORY payload (see
        # evaluate_goal). The Hades 2 tab's goal rows read these, and CheatClient re-checks goal
        # completion against them. The mod only sends VICTORY at the moment of a win, so they're
        # also saved to the server's data storage (goal_stats_key) and read back on connect --
        # otherwise every client restart would show the goal as unknown until the next win.
        self.last_goal_clears: dict = {}
        self.last_goal_weapons: dict = {}
        self.last_goal_zagreus_clears: int = 0
        self.goal_stats_known = False
        # (slot id, payload) of a VICTORY that arrived while the server link was down (CommonContext
        # clears self.slot on disconnect, so neither the goal StatusUpdate nor the stats save could
        # be sent). Evaluated on the next Connected -- only if that's the same slot again.
        self.pending_victory: Optional[tuple] = None
        self.connected_slot_id: Optional[tuple] = None

        # Hades 2 tab: this slot's locations (id -> name) and where the tab counts each one
        # (Tracker.classify_locations), built once per connection since the list never changes.
        self.tracker_locations: dict = {}
        self.tracker_keys: dict = {}

        # The single active connection from the Lua mod, if any.
        self.bridge_server: Optional[asyncio.AbstractServer] = None
        self.bridge_writer: Optional[asyncio.StreamWriter] = None

    # ---------------- AP server auth / lifecycle -----------------------------

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        self.tags = set()
        # Pass the class's real game name explicitly rather than relying on self.game:
        # TrackerGameContext.disconnect() (see __init__) can stamp an empty string onto
        # this instance under Universal Tracker, and self.game would silently stay wrong
        # for the rest of the process. Reading it off the class sidesteps that instance
        # shadowing no matter what set it.
        await self.send_connect(game=Hades2Context.game)

    async def shutdown(self):
        if self.bridge_server is not None:
            self.bridge_server.close()
        await super().shutdown()

    # ---------------- AP package handling ------------------------------------

    def on_package(self, cmd: str, args: dict) -> None:
        # Required for Universal Tracker integration (see the import block up top): its
        # TrackerGameContext.on_package does the actual regen/tracking setup on Connected.
        # A harmless no-op call into CommonContext.on_package (which does nothing) when UT
        # isn't installed.
        super().on_package(cmd, args)

        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            version = self.slot_data.get("version_check", "?")
            if version != self.mod_version:
                logger.warning(
                    f"Seed generated with mod version {version}, client expects {self.mod_version}. "
                    "These may be incompatible.")
            self.location_name_to_id = self.get_location_name_to_id()
            self.tracker_locations = {loc_id: name for name, loc_id in self.location_name_to_id.items()}
            self.tracker_keys = Tracker.classify_locations(self.slot_data, self.tracker_locations)
            # Goal stats belong to the slot just connected to (this may be a different one than
            # last time): start unknown, then evaluate a VICTORY held from an outage on this same
            # slot, or else read the stats saved on the server.
            self.connected_slot_id = self.goal_slot_id()
            held, self.pending_victory = self.pending_victory, None
            self.last_goal_clears, self.last_goal_weapons, self.last_goal_zagreus_clears = {}, {}, 0
            self.goal_stats_known = False
            if held is not None and held[0] == self.connected_slot_id:
                self.evaluate_goal(held[1])
            else:
                Utils.async_start(self.send_msgs([{"cmd": "Get", "keys": [self.goal_stats_key()]}]))
            # Flush any checks the mod sent during the pre-sync window (see pending_checks).
            if self.pending_checks:
                buffered, self.pending_checks = self.pending_checks, []
                Utils.async_start(self._flush_pending_checks(buffered))
            # Re-arm on every (re)connect: server_auth resets self.tags, so without this a
            # reconnect would silently drop the DeathLink tag even when it was enabled --
            # including a manual /deathlink enable on a seed whose slot_data has it off.
            if self.slot_data.get("deathlink") or self.deathlink_enabled:
                self.deathlink_enabled = True
                Utils.async_start(self.update_death_link(True))
            Utils.async_start(self.scout_locations())
            Utils.async_start(self.sync_mod())

        elif cmd == "ReceivedItems":
            Utils.async_start(self.send_items_to_mod())

        elif cmd == "RoomUpdate":
            # checked_locations may have changed by ANY means (another player finished and
            # released/collected their checks, an admin !send_location, etc.). Resend the
            # point_based "already checked" set so the mod can skip those checks for free.
            # (The Connected path is covered by sync_mod.) Guard like the other send paths.
            if self.bridge_writer is not None and self.slot_data is not None:
                self.send_to_mod(self.compute_checked_score())

        elif cmd == "LocationInfo":
            # Reply to our LocationScouts: cache each location's contents as
            # "<receiving player> - <item>" so sent-check banners can name who got what.
            for net_item in args.get("locations", []):
                player_name = self.player_names.get(net_item.player, f"Player {net_item.player}")
                item_name = self.item_names.lookup_in_slot(net_item.item, net_item.player)
                self.scouted[net_item.location] = _wire_text(f"{player_name} - {item_name}")

        elif cmd == "Retrieved":
            # Reply to the Connected-time Get for the saved goal stats (see goal_stats_key). A
            # live VICTORY this session is newer, so it wins. No saved value means no win has
            # ever been reported for this slot: every count really is 0, not unknown.
            if self.goal_stats_key() in args.get("keys", {}) and not self.goal_stats_known:
                saved = args["keys"][self.goal_stats_key()]
                stats = self.parse_victory(saved) if isinstance(saved, str) else None
                if stats is not None:
                    self.last_goal_clears, self.last_goal_weapons, self.last_goal_zagreus_clears = stats
                self.goal_stats_known = True

        # NOTE: no "Bounced" branch here on purpose. CommonContext.process_server_cmd already
        # dispatches DeathLink bounces to on_deathlink, guarded by an echo filter
        # (data["time"] != our own last_death_link, set by send_death). Handling Bounced here
        # too dispatched every link twice and bypassed that filter -- if the server echoed our
        # OWN death back after the 3s deathlink_pending window, we'd kill the player again.

    def get_location_name_to_id(self) -> dict:
        table = {}
        for location_id in self.server_locations:
            table[self.location_names.lookup_in_slot(location_id)] = location_id
        return table

    async def _flush_pending_checks(self, payloads: list) -> None:
        """Retry checks the mod sent before we were synced, now that location_name_to_id exists.
        A name still unknown here (wrong seed / genuinely-invalid location) is warned, not looped."""
        loc_ids = []
        for payload in payloads:
            loc_id = self.location_name_to_id.get(payload)
            if loc_id is None:
                logger.warning(f"Unknown location checked by game (buffered pre-connect): {payload!r}")
                continue
            loc_ids.append(loc_id)
            if loc_id not in self.checked_locations:
                detail = self.scouted.get(loc_id, "")
                self.send_to_mod(f"CHECKED:{payload}|{detail}")
        if loc_ids:
            await self.check_locations(loc_ids)
            logger.info(f"Flushed {len(loc_ids)} buffered check(s) after connecting.")

    async def scout_locations(self) -> None:
        # Ask the server what every location contains (no hints created) so we can tell
        # the mod "<player> - <item>" when it sends a check. Replies arrive as LocationInfo.
        if not self.server_locations:
            return
        await self.send_msgs([{
            "cmd": "LocationScouts",
            "locations": list(self.server_locations),
            "create_as_hint": 0,
        }])

    # ---------------- DeathLink ----------------------------------------------

    def on_deathlink(self, data: dict) -> None:
        if self.deathlink_pending:
            return
        self.deathlink_pending = True
        # "source" is the sending player's slot name per the standard DeathLink payload; fall
        # back to a generic label if a bounce ever arrives without one.
        source = str(data.get("source") or "Archipelago")
        self._forward_death_to_mod(source)
        super().on_deathlink(data)
        Utils.async_start(self._lower_deathlink_flag())

    def _forward_death_to_mod(self, source: str) -> None:
        # Push an incoming DeathLink to the game. If the game isn't connected to the bridge yet
        # (reboot gap: client connected to AP, game still launching), DON'T drop it -- hold it and
        # flush on the mod's next HELLO. Otherwise the client shows the DeathLink banner but the
        # player never dies, which reads as "DeathLink does nothing."
        # Payload carries the killer's name so the mod can show "<source> Killed You" instead of
        # a generic message. The mod splits a message on its FIRST ":", so a ":" inside the name
        # is harmless; newlines are not.
        source = _wire_text(source)
        if self.bridge_writer is not None:
            self.send_to_mod(f"DEATH:{source}")
        else:
            self.pending_mod_death = True
            self.pending_death_source = source
            logger.info("DeathLink received while the game wasn't connected -- holding it; "
                        "it will apply once the game connects to the bridge.")

    async def _lower_deathlink_flag(self) -> None:
        await asyncio.sleep(3)
        self.deathlink_pending = False

    # ---------------- Bridge: TCP server for the Lua mod ---------------------

    async def start_bridge_server(self) -> None:
        # Bind in a retry loop so a stuck port (a previous Hades 2 Rogue Client still holding
        # 43055, or a TIME_WAIT socket) NEVER prevents the client window from opening.
        # This runs as a background task; the client UI starts regardless.
        while not self.exit_event.is_set():
            try:
                self.bridge_server = await asyncio.start_server(
                    self.handle_bridge_connection, BRIDGE_HOST, BRIDGE_PORT)
                logger.info(f"Game bridge listening on {BRIDGE_HOST}:{BRIDGE_PORT}")
                return
            except OSError as exc:
                logger.warning(
                    f"Game bridge couldn't bind {BRIDGE_HOST}:{BRIDGE_PORT} ({exc}); "
                    "another Hades 2 Rogue Client may still be running. Retrying in 5s "
                    "(the client is usable now; the game will connect once the port frees).")
                await asyncio.sleep(5)

    async def watch_bridge_connection(self) -> None:
        # One-shot nudge: most people never type /bridge unprompted, so if the port itself
        # never bound after a generous grace period, tell them what to check instead of
        # leaving them staring at a client that looks idle.
        await asyncio.sleep(45)
        if not self.exit_event.is_set() and self.bridge_writer is None and self.bridge_server is None:
            logger.warning(
                f"Still couldn't bind {BRIDGE_HOST}:{BRIDGE_PORT} after 45s -- something "
                "else has that port. Close any other Hades 2 Rogue Client windows/processes "
                "and restart this client.")

    async def handle_bridge_connection(self, reader: asyncio.StreamReader,
                                       writer: asyncio.StreamWriter) -> None:
        # Only one game connection at a time; a new one supersedes the old.
        if self.bridge_writer is not None:
            try:
                self.bridge_writer.close()
            except Exception:
                pass
        self.bridge_writer = writer
        logger.info("Game connected to bridge.")
        try:
            while not reader.at_eof():
                line = await reader.readline()
                if not line:
                    break
                message = line.decode("utf-8", errors="replace").strip()
                if message:
                    try:
                        await self.handle_mod_message(message)
                    except Exception:
                        # One bad message must not end the read loop (and with it the game's
                        # connection) -- log it and keep reading.
                        logger.exception(f"Error handling game message {message[:200]!r}")
        except (ConnectionResetError, asyncio.IncompleteReadError):
            pass
        finally:
            if self.bridge_writer is writer:
                self.bridge_writer = None
            logger.info("Game disconnected from bridge.")

    def send_to_mod(self, message: str) -> None:
        if self.bridge_writer is None:
            return
        try:
            self.bridge_writer.write((message + "\n").encode("utf-8"))
        except Exception as exc:
            logger.warning(f"Failed to send to game: {exc}")

    async def handle_mod_message(self, message: str) -> None:
        command, _, payload = message.partition(":")

        if command == "HELLO":
            await self.sync_mod()
            # Flush a DeathLink that arrived while the game was disconnected (see
            # _forward_death_to_mod). The mod's own pending-death queue only applies it once the
            # player is in a killable, unpaused state, so this won't kill you at the Crossroads.
            if self.pending_mod_death:
                self.pending_mod_death = False
                self.send_to_mod(f"DEATH:{self.pending_death_source}")
                logger.info("Flushed a held DeathLink to the game now that it's connected.")

        elif command == "CHECK":
            if payload in self.location_name_to_id:
                loc_id = self.location_name_to_id[payload]
                # The mod re-sends checks the server already has (nothing tells it about them),
                # so only echo -- i.e. only show "Sent ..." in game -- for a new one.
                already = loc_id in self.checked_locations
                await self.check_locations([loc_id])
                if not already:
                    # Echo back the scouted contents so the mod's subtle log can show who got
                    # what. Detail is empty if scout data hasn't arrived yet (mod handles that).
                    detail = self.scouted.get(loc_id, "")
                    self.send_to_mod(f"CHECKED:{payload}|{detail}")
            elif not self.location_name_to_id:
                # Not connected/synced yet (location_name_to_id is only filled on Connected). Don't
                # drop it -- the mod won't resend a one-time check -- buffer and flush on Connected.
                self.pending_checks.append(payload)
                logger.info(f"Buffered a check until connected: {payload!r}")
            else:
                logger.warning(f"Unknown location checked by game: {payload!r}")

        elif command == "VICTORY":
            self.evaluate_goal(payload)

        elif command == "DEATH":
            await self.send_player_death()

    # ---------------- Bridge: pushing state to the mod -----------------------

    async def sync_mod(self) -> None:
        if self.slot_data is not None:
            # Sent FIRST, ahead of SETTINGS: identifies which multiworld generation this is
            # (AP's own self.seed_name, set from the RoomInfo packet -- unrelated to our seed's
            # options). Lets the mod tell "still the same seed I was tracking" apart from "this
            # save got reused for a different multiworld" and auto-wipe its stale AP state in the
            # latter case, BEFORE anything else in this sync (including SETTINGS's one-time
            # resync-lost-checks pass) has a chance to act on stale bookkeeping.
            self.send_to_mod(f"SEED:{self.seed_name}")
            self.send_to_mod("SETTINGS:" + self.encode_settings())
            # point_based: tell the mod which score checks the server already has so it can
            # skip them for free (see compute_checked_score). Sent here so a reconnecting mod
            # gets the current set; also resent on RoomUpdate when checked_locations changes.
            self.send_to_mod(self.compute_checked_score())
        await self.send_items_to_mod()

    def compute_checked_score(self) -> str:
        # point_based only: tell the mod which score checks the server ALREADY has (a finished
        # player's auto-released/collected checks, an admin !send_location, fresh-save
        # recovery). The mod advances past these for FREE - no score spent, no CHECK re-sent.
        # This is per-number (not a high-water mark) so a gap like "0017 checked while 0015 is
        # not" is handled correctly. Names with a trailing space + weapon suffix are room checks
        # and are skipped.
        # "combined" is separate_checks=combine_pools' shared, route-agnostic "Score N" pool;
        # the per-route buckets are split_pools' "<Route> Score N". A seed only ever uses one
        # kind, so the other simply comes through empty.
        id_to_name = {loc_id: name for name, loc_id in self.location_name_to_id.items()}
        underworld, surface, nightmare, dream, combined = [], [], [], [], []
        for loc_id in self.checked_locations:
            name = id_to_name.get(loc_id, "")
            # "Dream Score " must be listed before the bare "Score " (combine_pools) prefix --
            # the loop takes the first match. Dream was absent from this list entirely, so its
            # already-checked score numbers never got the free skip every other route gets.
            for prefix, bucket in (("Underworld Score ", underworld),
                                   ("Surface Score ", surface),
                                   ("Nightmare Score ", nightmare),
                                   ("Dream Score ", dream),
                                   ("Score ", combined)):
                if not name.startswith(prefix):
                    continue
                remainder = name[len(prefix):]
                if " " in remainder:   # weapon suffix -> per-weapon room check, skip
                    break
                try:
                    bucket.append(int(remainder))
                except ValueError:
                    pass
                break
        for bucket in (underworld, surface, nightmare, dream, combined):
            bucket.sort()
        return ("CHECKEDSCORE:underworld=" + ",".join(str(n) for n in underworld)
                + ";surface=" + ",".join(str(n) for n in surface)
                + ";nightmare=" + ",".join(str(n) for n in nightmare)
                + ";dream=" + ",".join(str(n) for n in dream)
                + ";combined=" + ",".join(str(n) for n in combined))

    # ---------------- Hades 2 tab ---------------------------------------------

    def tracker_in_logic(self) -> Optional[set]:
        """Location ids Universal Tracker currently has in logic, or None when UT isn't installed
        or has no working regen for this slot (the tab then hides every "in logic" count rather
        than showing a misleading 0)."""
        core = getattr(self, "tracker_core", None)
        if core is None:
            return None
        try:
            if core.get_current_world() is None:
                return None
            return set(core.locations_available)
        except Exception:
            return None

    def tracker_inputs_key(self) -> tuple:
        """Cheap fingerprint of everything build_tracker_model reads, so the once-a-second refresh
        only rebuilds the model when one of them changed. UT replaces locations_available with a
        new list on every update, so its identity is enough to notice a change."""
        core = getattr(self, "tracker_core", None)
        available = getattr(core, "locations_available", None)
        return (id(self.slot_data), len(self.tracker_keys), len(self.items_received),
                len(self.checked_locations), id(available), self.goal_stats_known,
                tuple(sorted(self.last_goal_clears.items())), tuple(sorted(self.last_goal_weapons.items())),
                self.last_goal_zagreus_clears, self.finished_game)

    def build_tracker_model(self) -> dict:
        received = [self.item_names.lookup_in_game(item.item) for item in self.items_received]
        stats = {"clears": self.last_goal_clears, "weapons": self.last_goal_weapons,
                 "zagreus": self.last_goal_zagreus_clears} if self.goal_stats_known else None
        return Tracker.build_model(self.slot_data, received, self.tracker_locations, self.tracker_keys,
                                   set(self.checked_locations), self.tracker_in_logic(), stats,
                                   bool(self.finished_game))

    def goal_stats_key(self) -> str:
        """Server data-storage key holding this slot's latest VICTORY payload (see evaluate_goal)."""
        return f"Hades2Rogue_goal_stats_{self.team}_{self.slot}"

    def goal_slot_id(self) -> tuple:
        return (self.seed_name, self.team, self.slot)

    def _wins_needed(self, route_lower: str) -> int:
        return int(self.slot_data.get(f"{route_lower}_wins_needed", 1))

    def encode_settings(self) -> str:
        if not self.slot_data:
            return ""
        keys = [
            "initial_weapon", "location_system",
            "score_rewards_amount", "underworld_room_count", "surface_room_count",
            "nightmare_room_count", "combined_room_count", "location_multiplier",
            "npc_locations",
            "grasp_intervals", "arcanasanity",
            "aspectsanity", "starting_aspect_index",
            "keepsakesanity", "enemysanity", "include_minibosses", "enemysanity_shuffle_map",
            "miniboss_room_map",
            "petsanity", "helper_room_sanity", "combat_helper_sanity", "godsanity",
            "godsanity_chaos",
            "reverse_vow", "reverse_rivals",
            "vow_pain", "vow_grit", "vow_wards", "vow_frenzy", "vow_hordes",
            "vow_menace", "vow_return", "vow_fangs", "vow_scars", "vow_debt",
            "vow_shadow", "vow_forfeit", "vow_time", "vow_void", "vow_hubris",
            "vow_denial", "vow_rivals",
            "goal_requires_zagreus", "goal_mode",
            "zagreus_encounter_mode",
            "include_zagreus_journey",
            "separate_checks",
            "starting_route", "lock_routes",
            "underworld_offset", "surface_offset", "nightmare_offset", "dream_offset",
            "surface_start", "nightmare_start", "dream_start",
            "underworld_active", "surface_active", "nightmare_active", "dream_active",
            "underworld_wins_needed", "surface_wins_needed", "nightmare_wins_needed",
            "dream_region_count", "dream_wins_needed", "dream_enemy_locations",
            "dream_region_count_actual", "dream_enemy_count", "dream_miniboss_count",
            "dream_boss_count", "dream_met_checks",
            "zagreus_defeats_needed",
            "zagreus_weaken_tiers", "weapons_clears_needed",
            "nectar_pack_value",
            "starting_health_value", "starting_magick_value",
            "starting_gold_value", "starting_armor_value",
            "deathlink", "deathlink_percent", "deathlink_amnesty",
        ]
        encoded = [f"{k}={self.slot_data.get(k, 0)}" for k in keys]

        # Which routes the goal actually requires, one 0/1 flag per route.
        # goals_required is a SET of route names in slot_data, which the ";"/"=" wire format
        # can't carry as-is -- so it was simply never sent, and the mod's own
        # LocationManager.all_required_goals_met read three keys ("goal_requires_chronos" /
        # "_typhon" / "_hades") that have never existed in any payload. Every lookup came back
        # nil -> false -> "no route is required" -> that function returned true unconditionally.
        # It exists specifically to stop combine_pools' ONE shared Score/Room pool from being
        # cascaded away the moment a single required route finishes (leaving nothing to earn on
        # the others), so that protection has been inert. Flags are named per ROUTE (matching
        # every other route-keyed setting here) rather than per boss.
        goals_required = self.slot_data.get("goals_required") or []
        for route in ("Underworld", "Surface", "Nightmare", "Dream"):
            encoded.append(f"goal_requires_{route.lower()}={1 if route in goals_required else 0}")
        return ";".join(encoded)

    async def send_items_to_mod(self) -> None:
        if self.bridge_writer is None:
            return
        # "<item>~<sender>" per entry (~ never appears in either) so the mod can show who
        # sent each item, e.g. "Received from Player1 - Progressive Underworld".
        entries = []
        for item in self.items_received:
            name = self.item_names.lookup_in_game(item.item)
            sender = _wire_text(self.player_names.get(item.player, f"Player {item.player}"))
            entries.append(f"{name}~{sender}")
        self.send_to_mod("ITEMS:" + "|".join(entries))

    # ---------------- Goal evaluation ----------------------------------------

    # Route bosses (chronos/typhon/hades) each need the configured weapon-clear variety;
    # zagreus (secret superboss, no route) doesn't. Mirrors Rules.GOAL_BOSSES; kept as an
    # inline duplicate since this module runs standalone and doesn't import the apworld
    # package.
    GOAL_BOSSES = ["chronos", "typhon", "hades", "zagreus", "dream"]
    # Route each boss's final-boss slot_data keys are prefixed with (goals_required entries
    # and <route>_wins_needed), mirrors Routes._BOSS_ROUTES. Zagreus has no route. "dream"
    # maps to itself since Dream's own route name lowercased already matches its slot_data
    # prefix ("dream_wins_needed") -- no separate route name to translate through.
    BOSS_ROUTE = {"chronos": "underworld", "typhon": "surface", "hades": "nightmare", "dream": "dream"}

    @staticmethod
    def parse_victory(payload: str) -> Optional[tuple]:
        """VICTORY payload -> (clears by boss, weapons by boss, zagreus clears), or None if malformed.
        payload: "<chronos_clears>-<chronos_weapons>-<typhon_clears>-<typhon_weapons>-
                  <zagreus_clears>-<hades_clears>-<hades_weapons>-<dream_clears>"
        dream_clears appended as an 8th field (not inserted mid-sequence) so a mod build that
        hasn't been updated yet still parses the first 7 fields fine via parts[:7]. Dream has no
        weapons field of its own: the mod sends one combined count (Dream clears included) in
        every <weapons> slot, so Dream reuses it."""
        parts = payload.split("-")
        try:
            (chronos_clears, chronos_weapons, typhon_clears, typhon_weapons,
             zagreus_clears, hades_clears, hades_weapons) = (int(p) for p in parts[:7])
        except (ValueError, IndexError):
            return None
        try:
            dream_clears = int(parts[7])
        except (ValueError, IndexError):
            dream_clears = 0  # older mod build that doesn't send Dream clears yet
        return ({"chronos": chronos_clears, "typhon": typhon_clears, "hades": hades_clears,
                 "dream": dream_clears},
                {"chronos": chronos_weapons, "typhon": typhon_weapons, "hades": hades_weapons,
                 "dream": chronos_weapons},
                zagreus_clears)

    def evaluate_goal(self, payload: str) -> None:
        if self.slot is None:
            # Server link down. Hold the newest win for the slot we were connected to (on_package's
            # Connected branch evaluates it). Before the first connection there's no slot to tie it
            # to, so it's dropped, as it always was.
            if self.connected_slot_id is not None:
                self.pending_victory = (self.connected_slot_id, payload)
            return
        stats = self.parse_victory(payload)
        if stats is None:
            logger.warning(f"Malformed VICTORY payload: {payload!r}")
            return
        self.last_goal_clears, self.last_goal_weapons, self.last_goal_zagreus_clears = stats
        self.goal_stats_known = True
        # Saved per slot on the server so the Hades 2 tab's goal rows survive a client restart
        # (read back on Connected -- see the "Retrieved" branch in on_package).
        Utils.async_start(self.send_msgs([{
            "cmd": "Set", "key": self.goal_stats_key(), "default": "", "want_reply": False,
            "operations": [{"operation": "replace", "value": payload}],
        }]))
        clears, weapons, zagreus_clears = stats

        weapons_needed = int(self.slot_data.get("weapons_clears_needed", 1))
        achieved = {
            boss: clears[boss] >= self._wins_needed(self.BOSS_ROUTE[boss])
                  and weapons[boss] >= weapons_needed
            for boss in ("chronos", "typhon", "hades", "dream")
        }
        # No weapon-variety requirement for Zagreus (matches Rules._hades2_can_get_victory).
        achieved["zagreus"] = zagreus_clears >= int(self.slot_data.get("zagreus_defeats_needed", 1))

        goals_required = self.slot_data.get("goals_required") or []
        bosses = [b for b in self.GOAL_BOSSES
                  if (b == "zagreus" and int(self.slot_data.get("goal_requires_zagreus", 0)))
                  or (b in self.BOSS_ROUTE and self.BOSS_ROUTE[b].capitalize() in goals_required)]
        if not bosses:
            return    # misconfigured -- never completable
        all_selected = int(self.slot_data.get("goal_mode", 1)) == 0
        done = all(achieved[b] for b in bosses) if all_selected else any(achieved[b] for b in bosses)

        if done:
            self.send_to_mod("GOAL")
            Utils.async_start(self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
            self.finished_game = True

    async def send_player_death(self) -> None:
        if self.deathlink_pending or not self.deathlink_enabled:
            return
        self.deathlink_pending = True
        await self.send_death("Melinoë was slain.")
        await self._lower_deathlink_flag()

    # ---------------- GUI ----------------------------------------------------

    def make_gui(self):
        # super().make_gui() first, before any of our own "from kivy..." imports below:
        # it's what pulls in kvui, which imports the real "kivy" package internally.
        # kvui must be the first thing to import kivy (some kvui builds -- e.g. a
        # vendored copy shipped inside another installed world -- assert on this for
        # frozen-build compatibility and hard-crash if it's already been imported).
        # Doing our own kivy.* imports first, as this used to, silently satisfies that
        # ordering violation and only surfaces as a crash when some other installed
        # world's kvui happens to enforce it.
        #
        # super().make_gui() also resolves through TrackerGameContext (when Universal
        # Tracker is installed -- see the import block up top), which already wraps
        # the base GameManager with its own Tracker tab. Subclassing that (rather than
        # kvui's bare GameManager) is what lets our own "Hades 2" tab stack alongside UT's.
        ui = super().make_gui()

        from kivy.clock import Clock
        from kivy.graphics import Color, Line, Rectangle
        from kivy.metrics import dp
        from kivy.uix.behaviors import ButtonBehavior
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.label import Label
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.widget import Widget

        labels = Tracker.LABELS
        row_height = dp(24)
        header_height = dp(30)

        class Marks(Widget):
            """`total` small squares, the first `filled` solid and the rest outlined. One square is
            an on/off state (zone open, weapon owned, check sent); five are an Aspect rank. The
            state is carried by shape, never by hue, so it reads the same for colorblind players."""
            def __init__(self, filled: int, total: int, color, **kwargs):
                self._marks = (filled, total, tuple(color))
                side, gap = dp(10), dp(3)
                super().__init__(size_hint=(None, None), height=row_height,
                                 width=total * side + (total - 1) * gap, **kwargs)
                self.bind(pos=self._draw, size=self._draw)
                self._draw()

            def _draw(self, *_):
                filled, total, color = self._marks
                side, gap = dp(10), dp(3)
                y = self.y + (self.height - side) / 2
                self.canvas.clear()
                with self.canvas:
                    Color(*color)
                    for i in range(total):
                        x = self.x + i * (side + gap)
                        if i < filled:
                            Rectangle(pos=(x, y), size=(side, side))
                        else:
                            Line(rectangle=(x + 0.5, y + 0.5, side - 1, side - 1), width=1)

        class ClickableRow(ButtonBehavior, BoxLayout):
            pass

        def text_label(text: str, color, bold: bool = False, height: float = row_height) -> Label:
            """Fills the remaining width, left-aligned, cut with "..." rather than overlapping."""
            label = Label(text=text, color=color, bold=bold, halign="left", valign="middle",
                          size_hint=(1, None), height=height, shorten=True, shorten_from="right")
            label.bind(size=lambda inst, value: setattr(inst, "text_size", value))
            return label

        def fit_label(text: str, color, bold: bool = False, height: float = row_height) -> Label:
            """Exactly as wide as its text."""
            label = Label(text=text, color=color, bold=bold, size_hint=(None, None), height=height)
            label.bind(texture_size=lambda inst, value: setattr(inst, "width", value[0]))
            return label

        def progress_text(checked: int, total: int, in_logic: Optional[int]) -> str:
            text = f"{checked}/{total}"
            if in_logic:
                text += "   " + labels["in_logic"].format(n=in_logic)
            return text

        def row(*widgets, height: float = row_height) -> BoxLayout:
            box = BoxLayout(orientation="horizontal", size_hint_y=None, height=height, spacing=dp(6))
            for widget in widgets:
                box.add_widget(widget)
            return box

        def auto_height(layout):
            layout.bind(minimum_height=layout.setter("height"))
            return layout

        def status_grid() -> GridLayout:
            return auto_height(GridLayout(cols=3, size_hint_y=None, row_default_height=row_height,
                                          row_force_default=True, spacing=(dp(12), 0)))

        class Hades2Manager(ui):
            base_title = "Archipelago Hades 2 Rogue Client"
            ctx: "Hades2Context"

            def build(self):
                container = super().build()
                self.add_client_tab("Hades 2", self.build_hades2_tab())
                return container

            # ---- Hades 2 tab: goal, routes/zones, weapons, check lists, unlocks, vows ----
            # Everything shown comes from Tracker.build_model; this class only draws it. The
            # model is rebuilt when one of its inputs changes (ctx.tracker_inputs_key) and the
            # widgets only when the model itself changed, so the 1s tick is nearly free.

            def build_hades2_tab(self):
                root = BoxLayout(orientation="vertical")
                scroll = ScrollView(do_scroll_x=False)
                self._tab_body = auto_height(BoxLayout(orientation="vertical", size_hint_y=None,
                                                       spacing=dp(12), padding=dp(10)))
                scroll.add_widget(self._tab_body)
                root.add_widget(scroll)
                self._tab_inputs = None
                self._tab_model = None
                self._tab_expanded = set()     # category keys whose lists are open
                self._tab_error = None
                Clock.schedule_interval(self._refresh_hades2_tab, 1.0)
                return root

            def _refresh_hades2_tab(self, dt):
                try:
                    inputs = self.ctx.tracker_inputs_key()
                    if inputs == self._tab_inputs:
                        return
                    self._tab_inputs = inputs
                    model = self.ctx.build_tracker_model()
                    if model != self._tab_model:
                        self._tab_model = model
                        self._render_hades2_tab()
                except Exception as exc:
                    # An exception escaping a Clock callback takes the whole client down (it
                    # did once, over a missing icon file). Log each distinct failure once.
                    if repr(exc) != self._tab_error:
                        self._tab_error = repr(exc)
                        logger.exception("Hades 2 tab failed to refresh")

            def _toggle_category(self, key: str) -> None:
                self._tab_expanded ^= {key}
                self._render_hades2_tab()

            def _tab_colors(self) -> tuple:
                """Text colors from the client's own theme (so a light theme stays readable); the
                dim variant marks locked/finished things by brightness, never by hue."""
                theme = getattr(self, "theme_cls", None)
                text = tuple(getattr(theme, "onSurfaceColor", None) or (1, 1, 1, 1))
                return text, text[:3] + (0.45,)

            def _render_hades2_tab(self) -> None:
                body = self._tab_body
                body.clear_widgets()
                model = self._tab_model
                if not model:
                    return
                text, dim = self._tab_colors()

                def header(title: str, *extra) -> BoxLayout:
                    return row(fit_label(title, text, bold=True, height=header_height), *extra,
                               Widget(), height=header_height)

                def goal_banner() -> Label:
                    return fit_label(labels["goal_complete"], text, bold=True, height=header_height)

                def section(width: Optional[float] = None) -> BoxLayout:
                    """One section's rows, stacked tight; `body` spaces the sections apart. A
                    width keeps short name/count rows readable instead of window-wide."""
                    box = auto_height(BoxLayout(orientation="vertical", size_hint_y=None))
                    if width is not None:
                        box.size_hint_x, box.width = None, width
                    return box

                narrow = dp(460)

                # Goal
                goal = model["goal"]
                if goal:
                    sec = section(narrow)
                    sec.add_widget(header(labels["goal_title"], *([goal_banner()] if goal["complete"] else [])))
                    if sum(1 for r in goal["rows"] if r["kind"] == "boss") > 1:
                        sec.add_widget(row(text_label(
                            labels["goal_mode_all" if goal["mode_all"] else "goal_mode_any"], dim)))
                    for goal_row in goal["rows"]:
                        have = labels["unknown"] if goal_row["have"] is None else str(goal_row["have"])
                        count = f"{have}/{goal_row['need']}"
                        if goal_row["label"]:
                            count += " " + goal_row["label"]
                        sec.add_widget(row(Marks(1 if goal_row["done"] else 0, 1, text),
                                           text_label(goal_row["name"], text), fit_label(count, text)))
                    body.add_widget(sec)

                # combine_pools' shared pool
                if model["shared"]:
                    sec = section(narrow)
                    sec.add_widget(header(labels["shared_title"]))
                    for label, checked, total, in_logic in model["shared"]:
                        sec.add_widget(row(text_label(label, text),
                                           fit_label(progress_text(checked, total, in_logic), text)))
                    body.add_widget(sec)

                # Routes, side by side: which zones your items open, and room progress per zone
                routes = model["routes"]
                if routes:
                    grid = auto_height(GridLayout(cols=len(routes) if len(routes) <= 3 else 2,
                                                  size_hint_y=None, spacing=(dp(24), dp(12))))
                    columns = []
                    for route in routes:
                        column = section()
                        column.add_widget(header(route["route"], *([goal_banner()] if route["goal_done"] else [])))
                        if route["progressive"]:
                            name, have, need = route["progressive"]
                            column.add_widget(row(text_label(name, text), fit_label(f"{have}/{need}", text)))
                        for label, checked, total, in_logic in route["rows"]:
                            column.add_widget(row(text_label(label, text),
                                                  fit_label(progress_text(checked, total, in_logic), text)))
                        for zone in route["zones"]:
                            widgets = [Marks(1 if zone["open"] else 0, 1, text),
                                       text_label(zone["name"], text if zone["open"] else dim)]
                            if zone["total"] is not None:
                                widgets.append(fit_label(progress_text(
                                    zone["checked"], zone["total"], zone["in_logic"]), text))
                            column.add_widget(row(*widgets))
                        columns.append(column)
                    # GridLayout bottom-aligns a shorter cell, so pad every column in a grid row
                    # down to the tallest one to keep the route headers lined up.
                    per_row = grid.cols
                    for start in range(0, len(columns), per_row):
                        group = columns[start:start + per_row]
                        tallest = max(sum(child.height for child in c.children) for c in group)
                        for c in group:
                            gap = tallest - sum(child.height for child in c.children)
                            if gap > 0:
                                c.add_widget(Widget(size_hint_y=None, height=gap))
                    for c in columns:
                        grid.add_widget(c)
                    body.add_widget(grid)

                # Weapons: owned, Aspect rank, and (per-weapon/per-aspect systems) room progress
                weapons = model["weapons"]
                if weapons["rows"]:
                    sec = section()
                    sec.add_widget(header(labels["weapons_title"]))
                    columns = weapons["columns"]
                    name_width, rank_width, cell_width, gap = dp(170), dp(110), dp(170), dp(12)
                    grid = auto_height(GridLayout(cols=2 + len(columns), size_hint=(None, None),
                                                  row_default_height=row_height, row_force_default=True,
                                                  spacing=(gap, 0)))
                    grid.width = name_width + rank_width + len(columns) * cell_width + (1 + len(columns)) * gap

                    def cell(widget, width):
                        widget.size_hint_x, widget.width = None, width
                        return widget

                    if columns:
                        grid.add_widget(cell(Widget(), name_width))
                        grid.add_widget(cell(text_label(labels["rank"], dim), rank_width))
                        for column in columns:
                            grid.add_widget(cell(text_label(column or labels["shared_title"], dim), cell_width))
                    for weapon in weapons["rows"]:
                        name_cell = cell(row(), name_width)
                        if weapon["indent"]:
                            name_cell.add_widget(Widget(size_hint_x=None, width=dp(24)))
                            active = bool(weapon["rank"])
                        else:
                            name_cell.add_widget(Marks(1 if weapon["owned"] else 0, 1, text))
                            active = weapon["owned"]
                        name_cell.add_widget(text_label(weapon["name"], text if active else dim))
                        grid.add_widget(name_cell)
                        rank = weapon["rank"]
                        rank_cell = cell(row(), rank_width)
                        if rank is not None:
                            rank_cell.add_widget(Marks(rank, ASPECT_MAX_RANK, text))
                            rank_cell.add_widget(fit_label(f"{rank}/{ASPECT_MAX_RANK}", text))
                        grid.add_widget(rank_cell)
                        for progress in weapon["cells"]:
                            grid.add_widget(cell(text_label(
                                progress_text(*progress) if progress else "", text), cell_width))
                    sec.add_widget(grid)
                    body.add_widget(sec)

                # Check lists (keepsakes by NPC, NPCs met, enemies defeated): a count, and the
                # full list on click
                for category in model["categories"]:
                    key = category["key"]
                    expanded = key in self._tab_expanded
                    sec = section()
                    toggle = ClickableRow(orientation="horizontal", size_hint_y=None,
                                          height=header_height, spacing=dp(12))
                    toggle.add_widget(fit_label(category["title"], text, bold=True, height=header_height))
                    toggle.add_widget(fit_label(progress_text(category["checked"], category["total"],
                                                              category["in_logic"]), text, height=header_height))
                    toggle.add_widget(fit_label(labels["hide" if expanded else "show"], dim,
                                                height=header_height))
                    toggle.add_widget(Widget())
                    toggle.bind(on_release=lambda _, k=key: self._toggle_category(k))
                    sec.add_widget(toggle)
                    if expanded:
                        grid = status_grid()
                        for name, checked, in_logic in category["entries"]:
                            entry = row(Marks(1 if checked else 0, 1, text),
                                        text_label(name, dim if checked else text))
                            if in_logic:
                                entry.add_widget(fit_label(labels["entry_in_logic"], text))
                            grid.add_widget(entry)
                        sec.add_widget(grid)
                    body.add_widget(sec)

                # Unlocks and vows
                for title, statuses in (("gods_title", model["gods"]), ("helpers_title", model["helpers"])):
                    if not statuses:
                        continue
                    sec = section()
                    sec.add_widget(header(labels[title]))
                    grid = status_grid()
                    for name, unlocked in statuses:
                        grid.add_widget(row(Marks(1 if unlocked else 0, 1, text),
                                            text_label(name, text if unlocked else dim)))
                    sec.add_widget(grid)
                    body.add_widget(sec)
                if model["vows"]:
                    sec = section()
                    sec.add_widget(header(labels["vows_title"]))
                    grid = status_grid()
                    for vow, current, configured in model["vows"]:
                        grid.add_widget(row(text_label(vow, text if current else dim),
                                            fit_label(f"{current}/{configured}", text)))
                    sec.add_widget(grid)
                    body.add_widget(sec)

        return Hades2Manager


def launch(*launch_args):
    # Without this, a crash anywhere below is completely invisible: this client never
    # shows a console, and nothing else in this process writes to Archipelago's own
    # logs folder. This matches every other CommonClient-based client's launch().
    Utils.init_logging("Hades2RogueClient")

    async def main(args):
        ctx = Hades2Context(args.connect, args.password)
        # get_username() falls back to this before prompting, and keeps using it on reconnects.
        ctx.username = args.name
        ctx.server_task = Utils.async_start(server_loop(ctx), name="server loop")
        # Background task (retries on a stuck port) so the UI always opens.
        Utils.async_start(ctx.start_bridge_server(), name="bridge server")
        Utils.async_start(ctx.watch_bridge_connection(), name="bridge watchdog")
        if UNIVERSAL_TRACKER_LOADED:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None
        await ctx.shutdown()

    import colorama
    parser = get_base_parser(description="Hades 2 Rogue Archipelago client.")
    parser.add_argument("--name", default=None, help="Slot name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    # Parse the Launcher-forwarded args, not sys.argv (which is the Launcher's own).
    args = handle_url_arg(parser.parse_args(launch_args), parser=parser)
    colorama.init()
    try:
        asyncio.run(main(args))
    except Exception:
        # A crash here previously meant the client just silently failed to open, with
        # no window, no console, and no clue for the player to go on. Log it AND pop a
        # native error box (works even though the Kivy window may never have appeared)
        # so there's something concrete to report back to us.
        logger.exception("Hades 2 Rogue Client crashed on startup")
        Utils.messagebox(
            "Hades 2 Rogue Client Error",
            "The Hades 2 Rogue Client crashed on startup.\n\n"
            "Please check logs/Hades2RogueClient.txt in your Archipelago folder and "
            "share it so this can be fixed.",
            error=True,
        )
    finally:
        colorama.deinit()
