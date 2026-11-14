# Hades 2 Rogue ↔ Archipelago bridge protocol

A local **TCP socket** carries newline-delimited UTF-8 messages between the
in-game Lua mod and the Python Archipelago client (Client.py). The message set itself
isn't versioned (optional messages are negotiated in `HELLO`), but three versions are
compared on connect (Client.py `check_versions`): the mod's (`HELLO`'s `version=`, read
from its `manifest.json`), the apworld's (`MOD_VERSION`) and the seed's (slot_data
`version_check`, the generating apworld's `mod_version`). A different major.minor, or a
mod that reports no version (older than 0.11.0), gets an error box in the client and,
for a mod that handles it, an `ALERT` banner in game. A patch-only difference is a log
line. Nothing is blocked.

- **Transport:** TCP on `127.0.0.1:43055`. Hardcoded on both ends (Client.py
  `BRIDGE_HOST`/`BRIDGE_PORT`, Bridge.lua `BRIDGE_HOST`/`BRIDGE_PORT`) --
  deliberately NOT in config.lua, since r2modman's config editor lets players
  edit it and a mismatch breaks the connection with no error on either side.
- **Roles:** the Python client is the **server** (listens); the Lua mod is the
  **client** (connects out from the render loop, retries every ~2s). Only one game
  connection is kept; a new one replaces the old.
- **Framing:** one message per line, terminated by `\n`.
- **Format:** `COMMAND:payload`. The mod splits on the FIRST `:`, so the payload
  may contain more colons. Payload may be empty.
- **Free text:** anything that comes from other players (slot names, other games'
  item names) goes through Client.py `_wire_text` first, which replaces newlines
  and the `|` / `~` delimiters. Our own item and location names never contain them.
  `JOURNAL` fields get the same treatment in `Journal._wire`.

## Mod → Client

| Message | Meaning |
|---|---|
| `HELLO` or `HELLO:<capabilities>` | Sent on every (re)connect, and again after a late-loaded save was wiped by the seed check. Client replies with `SEED`, `SETTINGS`, `CHECKEDSCORE`, then `ITEMS`. The payload is a comma-separated list: the optional client messages this mod build handles (`journal`: the client then also sends `JOURNAL`; `alert`: it may send `ALERT`), plus `version=<x>`, the mod's `manifest.json` `version_number` (`unknown` if the mod couldn't read it). Since 0.11.0 the mod sends `HELLO:journal,alert,version=<x>`. A 0.10.x mod sends `HELLO:journal`, an older one a bare `HELLO`; either is reported as "older than 0.11.0" and is never sent an `ALERT` or (bare `HELLO`) a `JOURNAL`. |
| `CHECK:<location name>` | A location was earned. Queued in the save (`APState.pending_checks`) and only flushed once the loaded save is verified against this connection's `SEED`, so a check earned while disconnected is never lost. The client buffers checks that arrive before it has the server's location list. A name the seed doesn't have is logged each time, and the first one per client session also gets an error box and an `ALERT` (worded by whether this apworld knows the name at all): it almost always means the mod, apworld and seed are from different releases. |
| `VICTORY:<chronosClears>-<weapons>-<typhonClears>-<weapons>-<zagreusClears>-<hadesClears>-<weapons>-<dreamClears>` | Goal state after a win (`LocationManager.victory_payload`). `<weapons>` is the same number in all three slots: distinct weapons used across every route's clears, Dream included (Dream reuses it; it has no slot of its own). Queued in the save (`victory_pending`) until a verified connection exists. Older clients read only the first 7 fields. |
| `DEATH` | Melinoë died and the `deathlink_amnesty` threshold was reached. The client broadcasts a DeathLink if DeathLink is on. Not queued: a death while disconnected isn't sent. |

## Client → Mod

| Message | Meaning |
|---|---|
| `SEED:<seed_name>` | AP's own per-generation identifier (`ctx.seed_name`, from `RoomInfo`). Sent first on every sync. The mod keeps it for the connection (`Bridge.seed_id`) and compares it with the save's `last_seed_id` (`Bridge.verify_save`): a save last used with a different multiworld is wiped (same wipe as `RESET`); a save with no seed on record is adopted. Nothing save-bound (queued checks, `VICTORY`) is sent until this matches. |
| `SETTINGS:k=v;k=v;...` | Slot settings (Client.py `encode_settings`): the option values the mod needs, the resolved `*_offset` / `*_start` / `*_active` route flags, `location_multiplier`, the room counts, the Dream counter sizes, `enemysanity_shuffle_map` / `miniboss_room_map` (`Name:Name,...`), `goal_requires_<route>` 0/1 flags, and the seed-shape flags `godsanity_chaos` / `dream_met_checks` (0 on a seed generated before those existed, which keeps the mod from gating on an item or sending a check that seed never had). Values never contain `;` or `=`. Cached to disk by the mod for the next boot. |
| `ITEMS:<item>~<sender>\|<item>~<sender>\|...` | The **full ordered list** of received items (stacks repeat). The mod applies only entries past its saved processed index (`APState.processed`), so resending is safe. Applied on the next frame where no menu, conversation or cutscene owns input. Trap items ride this list too: the mod queues each event trap in the save (`trap_queue`) and fires it once, later, in a run; counter traps (Onion Trap, Rarity Decrease, the Starting ... Loss items) raise a number in `trap_counts` instead. A mod that doesn't know a trap name ignores it. |
| `CHECKEDSCORE:underworld=<csv>;surface=<csv>;nightmare=<csv>;dream=<csv>;combined=<csv>` | **point_based only.** Score-check numbers the server already has (a released/collected slot, an admin `!send_location`). The mod advances past them for free instead of spending points to re-earn them. Per number, so gaps are handled. Replaces the previous set. Sent on every sync and on every `RoomUpdate`. `combined` is combine_pools' shared `Score N` pool. Empty lists are allowed. |
| `CHECKED:<location name>\|<player> - <item>` | Echo for a `CHECK` the server didn't already have, with the scouted contents so the corner log can show who got what. The detail after the first `\|` is empty if scouts haven't arrived yet. |
| `DEATH:<source>` | Incoming DeathLink from slot `<source>` (`Archipelago` if the bounce had no source). The mod holds one pending DeathLink and applies it when the player has control: in a run, `deathlink_percent`% of max health (Death Defiance can still save you), or a kill if that setting is 0; in the Crossroads, a death-and-respawn sequence. Further DeathLinks while one is pending are dropped. A DeathLink that arrives while the game isn't connected is held by the client and sent on the next `HELLO`. |
| `JOURNAL:<chapter title>\|<key>~<title>~<portrait>~<body>\|...` | **Only to a mod that sent `HELLO:journal`.** The in-game tracker: every page of the "Archipelago" chapter the mod adds to the Codex, already laid out (`Journal.py` builds them from the same `Tracker.build_model` as the client's "Hades 2" tab, plus the seed's enemy placement and this slot's hints). One record per page, in page order: `key` is a stable id (`goal`, `route_underworld`, `enemies_surface_2`, ...), `title` the page's name in the entry list, `portrait` a Codex portrait animation name (may be empty), `body` the page text in the game's own text markup, with ` 
 ` (backslash + n, not a newline) as the line break. Always the full set. Sent after `ITEMS` on every sync, then again whenever the pages change (the client compares a fingerprint of their inputs once a second). The mod rebuilds the chapter when the book is closed; with the book open it redraws in place if the page keys are unchanged, otherwise holds the update until the book closes. |
| `ALERT:<text>` | **Only to a mod that sent `alert` in `HELLO`.** A problem the player has to fix outside the game: a version mismatch (at most once per problem per connection) or the first check the seed doesn't know (once per client session). The mod shows `<text>` on the big orange banner (`Notifications.push("warning", ...)`) and logs it to LogOutput.log, **once per game session per text**: repeats (every reconnect and save load resends it) are dropped. The mod's Lua state doesn't survive a save load, so the shown texts are kept in `ReturnOfModding/config/Hades2RogueArchipelago.apalerts`, tagged with the game process's start time (`os.time() - os.clock()`); a restarted game shows them again. The client writes the text (Client.py `ALERT_TEXT`). |
| `GOAL` | The goal was sent to the server. Log only. |
| `RESET` | Debug: clear all applied-item state (processed index, counters, unlocks) so the next `ITEMS` re-applies from scratch. Traps already queued once are not queued again (`trap_high_water`). |
| `TRAP:<trap item name>` | Debug: fire that trap as a test, with no item behind it (`Traps.debug_fire`; the Cheats tab's "Fire trap" row, `/trap`, `tools/fake_client.py`). It skips the ledger and goes to the front of the queue (a counter trap just counts up); from there it is treated like a received one, so a combat trap still waits for combat. The corner log says what it is waiting for. |

## Scouting
- On `Connected`, the client sends a `LocationScouts` (with `create_as_hint=0`) for all of
  this slot's locations and caches each one's contents as `<player> - <item>` from the
  resulting `LocationInfo`. That cache feeds the `CHECKED` echo above.

## Sync model
- The **server** (AP) is authoritative on received items and checked locations.
- The **game save** stores how many received items the mod has already applied
  (the processed index), so reconnecting and re-receiving the full `ITEMS` list
  never double-grants.
- Location checks are idempotent on the AP side, so the mod may resend safely.
