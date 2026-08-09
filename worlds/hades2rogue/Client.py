import asyncio
from typing import Optional

import Utils
from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, server_loop

from .Items import WEAPON_SHORT_NAMES, vow_names, aspect_titles, ASPECT_BASE_TITLE_BY_WEAPON, \
    ASPECT_TITLES_BY_WEAPON, ASPECT_MAX_RANK, INITIAL_WEAPON_BY_VALUE, \
    godsanity_gods, godsanity_shop_gods, helper_story_npcs, helper_story_npcs_nightmare, \
    combat_helper_npcs

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
MOD_VERSION = "0.9.3"

# Hades 2 tab colors. Routes: 0 (can't enter) -> red .. 4 (all zones open) -> blue.
ROUTE_LEVEL_COLORS = {
    0: (0.85, 0.2, 0.2, 1), 1: (1.0, 0.55, 0.15, 1), 2: (0.85, 0.8, 0.15, 1),
    3: (0.25, 0.8, 0.25, 1), 4: (0.25, 0.55, 1.0, 1),
}
# Weapons: 0 (not owned) -> grey, 1-5 match the game's own aspect-rank rarity colors.
WEAPON_LEVEL_COLORS = {
    0: (0.5, 0.5, 0.5, 1), 1: (0.9, 0.9, 0.9, 1), 2: (0.25, 0.8, 0.25, 1),
    3: (0.25, 0.55, 1.0, 1), 4: (0.65, 0.35, 0.9, 1), 5: (0.9, 0.25, 0.25, 1),
}
# God/helper icon+label tint: not-yet-unlocked -> grey, unlocked -> full color.
SANITY_LOCKED_COLOR = (0.45, 0.45, 0.45, 1)
SANITY_UNLOCKED_COLOR = (1, 1, 1, 1)


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
        # evaluate_goal), cached here purely so a subclass can re-check goal completion later
        # against the latest known numbers without re-parsing a payload itself. Unused by the
        # plain client's own UI/commands -- just bookkeeping.
        self.last_goal_clears: dict = {}
        self.last_goal_weapons: dict = {}
        self.last_goal_zagreus_clears: int = 0

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
                self.scouted[net_item.location] = f"{player_name} - {item_name}"

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
        # a generic message. ":" can't appear in a slot name (it's the mod protocol's own
        # command/payload separator), so no escaping needed beyond stripping stray newlines.
        source = source.replace("\n", " ").replace("\r", " ")
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
                    await self.handle_mod_message(message)
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
                await self.check_locations([loc_id])
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
            self.send_to_mod("SETTINGS:" + self.encode_settings())
            # Tell the mod the highest score check the server already has, so a fresh save
            # doesn't re-send / re-notify "Clear Score" checks it re-earns from depth 0.
            self.send_to_mod(self.compute_score_sync())
            # point_based: tell the mod which score checks the server already has so it can
            # skip them for free (see compute_checked_score). Sent here so a reconnecting mod
            # gets the current set; also resent on RoomUpdate when checked_locations changes.
            self.send_to_mod(self.compute_checked_score())
        await self.send_items_to_mod()

    def compute_score_sync(self) -> str:
        # Tell the mod the highest already-earned ROOM check per route, so a fresh save (lost
        # save, power outage) doesn't re-notify room checks the server already has. Covers
        # room_based ("<route> Room N") and the combine_pools shared room pool ("Room N").
        # Point-based "<route> Score N" checks are NO LONGER synced here: a max()-based jump
        # would wrongly skip 1..16 if 0017 is checked out of order. Point skipping is now
        # per-number via CHECKEDSCORE (see compute_checked_score). Per-weapon room checks
        # aren't synced (their high-water is per weapon); they re-notify harmlessly on a fresh
        # save - the checks themselves still dedupe server-side.
        id_to_name = {loc_id: name for name, loc_id in self.location_name_to_id.items()}
        uroom = sroom = hroom = croom = 0
        for loc_id in self.checked_locations:
            name = id_to_name.get(loc_id, "")
            # combine_pools shared room pool: "Room NNNN" (no route prefix, no weapon).
            if name.startswith("Room "):
                remainder = name[len("Room "):]
                if " " not in remainder:   # weapon suffix -> per-weapon combined, skip
                    try:
                        croom = max(croom, int(remainder))
                    except ValueError:
                        pass
                continue
            for prefix, route in (
                ("Underworld Room ", "u"), ("Surface Room ", "s"), ("Nightmare Room ", "h"),
            ):
                if not name.startswith(prefix):
                    continue
                remainder = name[len(prefix):]
                if " " in remainder:   # has a weapon suffix -> per-weapon, skip
                    break
                try:
                    num = int(remainder)
                except ValueError:
                    break
                if route == "u":
                    uroom = max(uroom, num)
                elif route == "s":
                    sroom = max(sroom, num)
                else:
                    hroom = max(hroom, num)
                break
        return (f"SCORESYNC:underworld_room={uroom};surface_room={sroom};"
                f"nightmare_room={hroom};combined_room={croom}")

    def compute_checked_score(self) -> str:
        # point_based only: tell the mod which score checks the server ALREADY has (a finished
        # player's auto-released/collected checks, an admin !send_location, fresh-save
        # recovery). The mod advances past these for FREE - no score spent, no CHECK re-sent.
        # This is per-number (not a high-water mark) so a gap like "0017 checked while 0015 is
        # not" is handled correctly. Parsing mirrors compute_score_sync (names with a trailing
        # space + weapon suffix are room checks and are skipped).
        # "combined" is separate_checks=combine_pools' shared, route-agnostic "Score N" pool;
        # the per-route buckets are split_pools' "<Route> Score N". A seed only ever uses one
        # kind, so the other simply comes through empty.
        id_to_name = {loc_id: name for name, loc_id in self.location_name_to_id.items()}
        underworld, surface, nightmare, combined = [], [], [], []
        for loc_id in self.checked_locations:
            name = id_to_name.get(loc_id, "")
            for prefix, bucket in (("Underworld Score ", underworld),
                                   ("Surface Score ", surface),
                                   ("Nightmare Score ", nightmare),
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
        for bucket in (underworld, surface, nightmare, combined):
            bucket.sort()
        return ("CHECKEDSCORE:underworld=" + ",".join(str(n) for n in underworld)
                + ";surface=" + ",".join(str(n) for n in surface)
                + ";nightmare=" + ",".join(str(n) for n in nightmare)
                + ";combined=" + ",".join(str(n) for n in combined))

    def compute_display_progress(self) -> list:
        """Hades 2 tab: a list of column dicts {"header": <route name, or None for the
        combine_pools shared pool>, "rows": [(label, checked, total), ...]}, shaped by
        location_system (point/room/per-weapon-room) and separate_checks (split per
        route vs. combine_pools' shared pool) -- one column per active route when
        split, a single header-less column when combined. Unlike compute_score_sync/
        compute_checked_score (wire-protocol high-water marks the mod consumes), this is
        display-only and always reflects the server's real checked_locations count."""
        if not self.slot_data:
            return []
        system = int(self.slot_data.get("location_system", 1))
        combined = bool(int(self.slot_data.get("separate_checks", 0)))
        multiplier = int(self.slot_data.get("location_multiplier", 1))
        score_total = int(self.slot_data.get("score_rewards_amount", 0))
        # combined room pool is always sized off Underworld's room_count (see
        # Locations._combined_room_count) -- every route uses the same room_count anyway.
        room_total_combined = int(self.slot_data.get("underworld_room_count", 0)) * multiplier

        id_to_name = {loc_id: name for name, loc_id in self.location_name_to_id.items()}
        checked_names = {id_to_name[loc_id] for loc_id in self.checked_locations if loc_id in id_to_name}

        def count_checked(prefix: str, weapon: Optional[str] = None) -> int:
            n = 0
            for name in checked_names:
                if not name.startswith(prefix):
                    continue
                tokens = name[len(prefix):].split()
                if not tokens:
                    continue
                last = tokens[-1]
                if weapon is None:
                    if last in WEAPON_SHORT_NAMES:
                        continue    # per-weapon check -- counted separately
                elif last != weapon:
                    continue
                n += 1
            return n

        # Weapons removed from the YAML (IncludedWeapons, Options.py) never had rooms/items for
        # them generated at all -- without this filter they'd still show a permanent 0/0 grey
        # row here, which reads as "not unlocked yet" instead of "not in this seed."
        included_weapons = [w for w in WEAPON_SHORT_NAMES
                             if w in self.slot_data.get("included_weapons", WEAPON_SHORT_NAMES)]

        routes = (
            ("Underworld", "underworld_active", "Underworld Room", "Underworld Score", "underworld_room_count"),
            ("Surface", "surface_active", "Surface Room", "Surface Score", "surface_room_count"),
            ("Nightmare", "nightmare_active", "Nightmare Room", "Nightmare Score", "nightmare_room_count"),
        )
        columns = []
        if system == 0:     # point_based
            if combined:
                columns.append({"header": None,
                                 "rows": [("Score Locations", count_checked("Score"), score_total)]})
            else:
                for label, active_key, _, score_prefix, _ in routes:
                    if int(self.slot_data.get(active_key, 0)):
                        columns.append({"header": label,
                                         "rows": [("Score Locations", count_checked(score_prefix), score_total)]})
        elif system == 2:   # per_weapon_room_based
            if combined:
                columns.append({"header": None, "rows": [
                    (weapon, count_checked("Room", weapon), room_total_combined) for weapon in included_weapons
                ]})
            else:
                for label, active_key, room_prefix, _, count_key in routes:
                    if not int(self.slot_data.get(active_key, 0)):
                        continue
                    total = int(self.slot_data.get(count_key, 0)) * multiplier
                    columns.append({"header": label, "rows": [
                        (weapon, count_checked(room_prefix, weapon), total) for weapon in included_weapons
                    ]})
        else:               # room_based
            if combined:
                columns.append({"header": None,
                                 "rows": [("Rooms Cleared", count_checked("Room"), room_total_combined)]})
            else:
                for label, active_key, room_prefix, _, count_key in routes:
                    if int(self.slot_data.get(active_key, 0)):
                        total = int(self.slot_data.get(count_key, 0)) * multiplier
                        columns.append({"header": label,
                                         "rows": [("Rooms Cleared", count_checked(room_prefix), total)]})
        return columns

    def compute_route_access_level(self, route: str) -> int:
        """0 (can't even enter) .. 4 (all 4 zones open), purely from Progressive-<route>/
        Access-item counts and the same thresholds Rules.set_rules uses for "Descend
        <route>"/"Exit <zone>" -- NOT a real logic sweep (deliberately ignores the
        weapon-count/boss-victory/arcana/grasp zone gates Rules.py also applies)."""
        if not self.slot_data:
            return 0
        lock_routes = bool(int(self.slot_data.get("lock_routes", 0)))
        prog_name = f"Progressive {route}"
        counts: dict = {}
        received_names = set()
        for net_item in self.items_received:
            name = self.item_names.lookup_in_game(net_item.item)
            counts[name] = counts.get(name, 0) + 1
            received_names.add(name)
        p = counts.get(prog_name, 0)

        if route == "Underworld":
            offset = int(self.slot_data.get("underworld_offset", 0))
            entered = p >= offset
        else:
            start = bool(int(self.slot_data.get(f"{route.lower()}_start", 0)))
            access_via_progressive = lock_routes and not start
            if access_via_progressive:
                entered = p >= 1
                # That first progressive is "spent" opening the door -- it doesn't also
                # count toward area 2 (Rules.py's own item-count math says it does, since
                # the door and the zone-1-exit share the same ">= 1" threshold, but the
                # zone-1-exit is also AND-gated on the zone's boss/weapons in real play,
                # so treating the door-opener as separate matches what's actually usable).
                offset = 1
            else:
                offset = 0
                entered = start or f"{route} Access" in received_names

        if not lock_routes:
            return 4 if entered else 0
        if not entered:
            return 0
        level = 1
        for i in range(3):
            if p >= i + 1 + offset:
                level = i + 2
        return level

    def compute_weapon_level(self, weapon: str) -> int:
        """0 (weapon not owned, grey) .. 5 (an aspect at max rank, matching the game's own
        rarity colors), purely from item counts for whichever aspectsanity mode this seed
        uses -- not a logic sweep."""
        if not self.slot_data:
            return 0
        asp = int(self.slot_data.get("aspectsanity", 0))
        combine_on = asp in (1, 2, 3)
        initial_weapon = INITIAL_WEAPON_BY_VALUE.get(int(self.slot_data.get("initial_weapon", 0)))
        starting_aspect_index = int(self.slot_data.get("starting_aspect_index", 0))

        counts: dict = {}
        for net_item in self.items_received:
            name = self.item_names.lookup_in_game(net_item.item)
            counts[name] = counts.get(name, 0) + 1

        unlock_item = f"{weapon} Weapon Unlock Item"
        owned = weapon == initial_weapon or counts.get(unlock_item, 0) > 0
        rank = 0

        if asp == 1:      # randomized: any of the weapon's 4 aspect items -> max rank
            names = [ASPECT_BASE_TITLE_BY_WEAPON[weapon]] + ASPECT_TITLES_BY_WEAPON.get(weapon, [])
            if any(counts.get(n, 0) > 0 for n in names):
                rank = ASPECT_MAX_RANK
                if combine_on:
                    owned = True
            elif weapon == initial_weapon:
                rank = 1   # starting weapon begins with its picked aspect at rank 1
        elif asp == 2:    # progressive: N copies of one shared line = rank N
            item_name = f"Progressive {weapon}" if combine_on else f"Progressive {weapon} Aspect"
            rank = min(ASPECT_MAX_RANK, counts.get(item_name, 0))
            if combine_on and rank > 0:
                owned = True
        elif asp == 3:    # per_aspect: 4 independent lines, take the highest
            names = [f"Progressive {weapon} Base Aspect"] + \
                [f"Progressive {title}" for title, w in aspect_titles if w == weapon]
            best = 0
            for i, name in enumerate(names):
                count = counts.get(name, 0)
                if weapon == initial_weapon and i == starting_aspect_index:
                    count += 1   # this one aspect's first copy is precollected
                best = max(best, min(ASPECT_MAX_RANK, count))
            rank = best
            if combine_on and rank > 0:
                owned = True
        # asp == 0 (unlocked): no aspect items exist; rank stays 0, ownership alone decides.

        if not owned:
            return 0
        return max(1, rank)

    def compute_vow_counts(self) -> dict:
        """vow name -> currently-applied count, purely from items_received: the static
        configured level (vow_<name> in slot_data) minus how many "<Vow> Vow Removal"
        items have been received. No mod state needed -- the mod computes this same
        "configured minus removed" value for its own in-game purposes (apply_all_vows),
        but the removal count is just an item count the client already has."""
        if not self.slot_data:
            return {}
        removals: dict = {}
        for net_item in self.items_received:
            name = self.item_names.lookup_in_game(net_item.item)
            if name.endswith(" Vow Removal"):
                vow = name[:-len(" Vow Removal")]
                removals[vow] = removals.get(vow, 0) + 1
        return {
            vow: max(0, int(self.slot_data.get(f"vow_{vow.lower()}", 0)) - removals.get(vow, 0))
            for vow in vow_names
        }

    def compute_god_status(self) -> list:
        """Hades 2 tab: [(god name, unlocked), ...] for GodSanity's 11 gods (the 9 boon-reward
        gods plus Hermes/Selene, see Items.godsanity_gods/godsanity_shop_gods) -- empty when
        godsanity is "unlocked" (slot_data value 0), since no "<God> Unlock" item exists in the
        pool at all in that mode. "unlocked" here checks either the plain unlock item or the
        fused "<God> Unlock + Keepsake" item (keepsakesanity=randomized + godsanity combo, see
        Items.item_table_god_keepsake_combined) -- whichever one this seed actually uses."""
        if not self.slot_data or not int(self.slot_data.get("godsanity", 0)):
            return []
        received_names = {self.item_names.lookup_in_game(net_item.item) for net_item in self.items_received}
        return [
            (god, f"{god} Unlock" in received_names or f"{god} Unlock + Keepsake" in received_names)
            for god in godsanity_gods + godsanity_shop_gods
        ]

    def compute_helper_status(self) -> list:
        """Hades 2 tab: [(npc name, unlocked), ...] for helper NPCs whose governing sanity
        option is one of the item-based modes (HelperRoomSanity/CombatHelperSanity option
        values 1="items"/3="items_random", both odd) -- e.g. combat helpers on but story-room
        helpers off surfaces Artemis but not Narcissus. Empty for a sanity whose option is
        "unlocked"/"unlocked_random" (0/2, even): no unlock item exists in the pool then."""
        if not self.slot_data:
            return []
        received_names = {self.item_names.lookup_in_game(net_item.item) for net_item in self.items_received}
        result = []
        if int(self.slot_data.get("helper_room_sanity", 0)) % 2 == 1:
            npcs = list(helper_story_npcs)
            if int(self.slot_data.get("nightmare_active", 0)):
                npcs += helper_story_npcs_nightmare
            result += [(npc, f"{npc} Room" in received_names) for npc in npcs]
        if int(self.slot_data.get("combat_helper_sanity", 0)) % 2 == 1:
            result += [(npc, f"{npc} Helper" in received_names) for npc in combat_helper_npcs]
        return result

    def compute_route_goal_complete(self, route: str) -> bool:
        """Whether `route`'s own goal boss (chronos/typhon/hades for Underworld/Surface/
        Nightmare respectively) has already met its configured clear-count and weapon-variety
        requirement, purely from the most recent VICTORY payload cached by evaluate_goal
        (last_goal_clears/last_goal_weapons) -- False until the mod has ever reported one,
        independent of whether this route's boss is actually one of goals_required."""
        boss = {"Underworld": "chronos", "Surface": "typhon", "Nightmare": "hades"}.get(route)
        if boss is None or not self.slot_data:
            return False
        weapons_needed = int(self.slot_data.get("weapons_clears_needed", 1))
        wins_needed = self._wins_needed(route.lower())
        return (self.last_goal_clears.get(boss, 0) >= wins_needed
                and self.last_goal_weapons.get(boss, 0) >= weapons_needed)

    # Pre-"Options simplification v0.7.3" slot_data keys. A seed generated before that
    # option rename still has ITS slot_data under these names, never "<route>_wins_needed"
    # -- so a plain .get(f"{route}_wins_needed", 1) silently reads back the "unset" default
    # of 1 for every route regardless of the real configured value (e.g. 10/4), making the
    # goal (and the mod's own goal-cascade checks) look satisfied after just one clear.
    LEGACY_WINS_NEEDED_KEY = {
        "underworld": "chronos_defeats_needed", "surface": "typhon_defeats_needed",
        "nightmare": "hades_defeats_needed",
    }
    # Same mapping, keyed by the NEW slot_data key name instead of the bare route -- what
    # encode_settings needs when substituting a legacy value in under its new name so the
    # mod (which only ever reads "<route>_wins_needed") gets a real number from an
    # old-generated seed's slot_data either way.
    LEGACY_WINS_NEEDED_KEY_BY_NEW_KEY = {
        "underworld_wins_needed": "chronos_defeats_needed",
        "surface_wins_needed": "typhon_defeats_needed",
        "nightmare_wins_needed": "hades_defeats_needed",
    }

    def _wins_needed(self, route_lower: str) -> int:
        v = self.slot_data.get(f"{route_lower}_wins_needed")
        if v is None:
            v = self.slot_data.get(self.LEGACY_WINS_NEEDED_KEY.get(route_lower, ""), 1)
        return int(v)

    def encode_settings(self) -> str:
        if not self.slot_data:
            return ""
        keys = [
            "initial_weapon", "location_system",
            "score_rewards_amount", "underworld_room_count", "surface_room_count",
            "nightmare_room_count", "location_multiplier",
            "enemy_locations", "npc_locations",
            "grasp_intervals", "arcanasanity",
            "aspectsanity", "starting_aspect_index",
            "keepsakesanity", "petsanity", "helper_room_sanity", "combat_helper_sanity", "godsanity",
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
            "underworld_offset", "surface_offset", "nightmare_offset",
            "surface_start", "nightmare_start",
            "underworld_active", "surface_active", "nightmare_active",
            "underworld_wins_needed", "surface_wins_needed", "nightmare_wins_needed",
            "zagreus_defeats_needed",
            "zagreus_weaken_tiers", "weapons_clears_needed",
            "nectar_pack_value",
            "starting_health_value", "starting_magick_value",
            "starting_gold_value", "starting_armor_value",
            "deathlink", "deathlink_percent", "deathlink_amnesty",
        ]
        def _value(k: str):
            if k in self.slot_data:
                return self.slot_data.get(k)
            legacy = self.LEGACY_WINS_NEEDED_KEY_BY_NEW_KEY.get(k)
            if legacy is not None and legacy in self.slot_data:
                return self.slot_data.get(legacy)
            return 0
        return ";".join(f"{k}={_value(k)}" for k in keys)

    async def send_items_to_mod(self) -> None:
        if self.bridge_writer is None:
            return
        names = [self.item_names.lookup_in_game(item.item) for item in self.items_received]
        self.send_to_mod("ITEMS:" + "|".join(names))

    # ---------------- Goal evaluation ----------------------------------------

    # Route bosses (chronos/typhon/hades) each need the configured weapon-clear variety;
    # zagreus (secret superboss, no route) doesn't. Mirrors Rules.GOAL_BOSSES; kept as an
    # inline duplicate since this module runs standalone and doesn't import the apworld
    # package.
    GOAL_BOSSES = ["chronos", "typhon", "hades", "zagreus"]
    # Route each boss's final-boss slot_data keys are prefixed with (goals_required entries
    # and <route>_wins_needed), mirrors Routes._BOSS_ROUTES. Zagreus has no route.
    BOSS_ROUTE = {"chronos": "underworld", "typhon": "surface", "hades": "nightmare"}

    def evaluate_goal(self, payload: str) -> None:
        # payload: "<chronos_clears>-<chronos_weapons>-<typhon_clears>-<typhon_weapons>-
        #           <zagreus_clears>-<hades_clears>-<hades_weapons>"
        if not self.slot_data:
            return
        parts = payload.split("-")
        try:
            (chronos_clears, chronos_weapons, typhon_clears, typhon_weapons,
             zagreus_clears, hades_clears, hades_weapons) = (int(p) for p in parts[:7])
        except (ValueError, IndexError):
            logger.warning(f"Malformed VICTORY payload: {payload!r}")
            return

        self.last_goal_clears = {"chronos": chronos_clears, "typhon": typhon_clears, "hades": hades_clears}
        self.last_goal_weapons = {"chronos": chronos_weapons, "typhon": typhon_weapons, "hades": hades_weapons}
        self.last_goal_zagreus_clears = zagreus_clears

        weapons_needed = int(self.slot_data.get("weapons_clears_needed", 1))
        clears = {"chronos": chronos_clears, "typhon": typhon_clears, "hades": hades_clears}
        weapons = {"chronos": chronos_weapons, "typhon": typhon_weapons, "hades": hades_weapons}
        achieved = {
            boss: clears[boss] >= self._wins_needed(self.BOSS_ROUTE[boss])
                  and weapons[boss] >= weapons_needed
            for boss in ("chronos", "typhon", "hades")
        }
        # No weapon-variety requirement for Zagreus.
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
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.label import Label
        from kivy.uix.scrollview import ScrollView

        class Hades2Manager(ui):
            base_title = "Archipelago Hades 2 Rogue Client"
            ctx: "Hades2Context"

            def build(self):
                container = super().build()
                self.add_client_tab("Hades 2", self.build_hades2_tab())
                return container

            # ---- Hades 2 tab: route/score/room progress + Vow Tracker ----

            def build_hades2_tab(self):
                root = BoxLayout(orientation="vertical")
                scroll = ScrollView()
                outer = BoxLayout(orientation="vertical", size_hint_y=None, spacing=8, padding=8)
                outer.bind(minimum_height=outer.setter("height"))
                # One column per active route (or a single header-less column when
                # combined) -- rebuilt whenever the column SHAPE changes, not just the
                # numbers inside it (see _refresh_hades2_tab).
                self._progress_columns = BoxLayout(orientation="horizontal", size_hint_y=None, height=200)
                self._god_grid = GridLayout(cols=3, size_hint_y=None, spacing=6)
                self._god_grid.bind(minimum_height=self._god_grid.setter("height"))
                self._helper_grid = GridLayout(cols=3, size_hint_y=None, spacing=6)
                self._helper_grid.bind(minimum_height=self._helper_grid.setter("height"))
                self._vow_grid = GridLayout(cols=3, size_hint_y=None, spacing=6)
                self._vow_grid.bind(minimum_height=self._vow_grid.setter("height"))
                outer.add_widget(self._progress_columns)
                outer.add_widget(self._god_grid)
                outer.add_widget(self._helper_grid)
                outer.add_widget(self._vow_grid)
                scroll.add_widget(outer)
                root.add_widget(scroll)
                self._progress_shape_key = None
                self._progress_labels = []     # [(Label widget, weapon-name-or-None), ...]
                self._progress_headers = []    # [(Label widget, route-name), ...]
                self._goal_banners = []        # [(Label widget, route-name), ...]
                self._god_refresh_key = None
                self._helper_refresh_key = None
                self._vow_refresh_key = None
                Clock.schedule_interval(self._refresh_hades2_tab, 1.0)
                return root

            def _refresh_hades2_tab(self, dt):
                ctx = self.ctx

                columns = ctx.compute_display_progress()
                shape_key = [(col["header"], [label for label, _, _ in col["rows"]]) for col in columns]
                if shape_key != self._progress_shape_key:
                    self._progress_shape_key = shape_key
                    self._progress_columns.clear_widgets()
                    self._progress_labels = []
                    self._progress_headers = []
                    self._goal_banners = []
                    for col in columns:
                        col_box = BoxLayout(orientation="vertical", size_hint_x=1)
                        if col["header"]:
                            # Reserved even when not yet complete (empty text) so a route's
                            # column doesn't jump/resize the moment its goal finishes.
                            banner_label = Label(text="", bold=True, color=(0.3, 0.85, 0.3, 1),
                                                  size_hint_y=None, height=20)
                            col_box.add_widget(banner_label)
                            self._goal_banners.append((banner_label, col["header"]))
                            header_label = Label(text=col["header"], bold=True,
                                                  size_hint_y=None, height=28)
                            col_box.add_widget(header_label)
                            self._progress_headers.append((header_label, col["header"]))
                        for label, checked, total in col["rows"]:
                            row_label = Label(text=f"{label}: {checked}/{total}",
                                               size_hint_y=None, height=24)
                            col_box.add_widget(row_label)
                            weapon = label if label in WEAPON_SHORT_NAMES else None
                            self._progress_labels.append((row_label, weapon))
                        self._progress_columns.add_widget(col_box)
                else:
                    i = 0
                    for col in columns:
                        for label, checked, total in col["rows"]:
                            self._progress_labels[i][0].text = f"{label}: {checked}/{total}"
                            i += 1

                # Colors are recomputed every tick regardless of the shape/text branch above --
                # they change purely from received items, independent of the text they're
                # attached to (see Hades2Context.compute_route_access_level/compute_weapon_level;
                # deliberately item-count-based, not a real logic sweep).
                for header_label, route in self._progress_headers:
                    header_label.color = ROUTE_LEVEL_COLORS[ctx.compute_route_access_level(route)]
                for row_label, weapon in self._progress_labels:
                    if weapon is not None:
                        row_label.color = WEAPON_LEVEL_COLORS[ctx.compute_weapon_level(weapon)]
                for banner_label, route in self._goal_banners:
                    banner_label.text = "Goal Complete!" if ctx.compute_route_goal_complete(route) else ""

                def refresh_status_grid(grid, refresh_key_attr, status):
                    key = tuple(status)
                    if key == getattr(self, refresh_key_attr):
                        return
                    setattr(self, refresh_key_attr, key)
                    grid.clear_widgets()
                    for name, unlocked in status:
                        row = BoxLayout(size_hint_y=None, height=36, spacing=6)
                        color = SANITY_UNLOCKED_COLOR if unlocked else SANITY_LOCKED_COLOR
                        name_label = Label(text=name, color=color, halign="left", valign="middle")
                        name_label.bind(size=lambda inst, value: setattr(inst, "text_size", value))
                        row.add_widget(name_label)
                        grid.add_widget(row)

                refresh_status_grid(self._god_grid, "_god_refresh_key", ctx.compute_god_status())
                refresh_status_grid(self._helper_grid, "_helper_refresh_key", ctx.compute_helper_status())

                slot_data = ctx.slot_data
                vow_counts = ctx.compute_vow_counts()
                vow_key = (tuple(sorted(vow_counts.items())), slot_data is not None)
                if vow_key != self._vow_refresh_key:
                    self._vow_refresh_key = vow_key
                    self._vow_grid.clear_widgets()
                    if slot_data and int(slot_data.get("reverse_vow", 0)):
                        for vow in vow_names:
                            n = int(slot_data.get(f"vow_{vow.lower()}", 0))
                            if n <= 0:
                                continue
                            x = vow_counts.get(vow, n)
                            row = BoxLayout(size_hint_y=None, height=36, spacing=6)
                            # halign has no effect unless text_size is bound to the widget's
                            # own size -- without it, Kivy centers the rendered text in
                            # whatever space the Label is given, which (since the Label fills
                            # the rest of the row) reads as "floating" away from the icon.
                            vow_label = Label(text=f"{vow} {x}/{n}", halign="left", valign="middle")
                            vow_label.bind(size=lambda inst, value: setattr(inst, "text_size", value))
                            row.add_widget(vow_label)
                            self._vow_grid.add_widget(row)

        return Hades2Manager


def launch():
    # Without this, a crash anywhere below is completely invisible: this client never
    # shows a console, and nothing else in this process writes to Archipelago's own
    # logs folder. This matches every other CommonClient-based client's launch().
    Utils.init_logging("Hades2RogueClient")

    async def main(args):
        ctx = Hades2Context(args.connect, args.password)
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
    parser = get_base_parser()
    args = parser.parse_args()
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
