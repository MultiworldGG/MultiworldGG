# Hades 2 Rogue ↔ Archipelago bridge protocol

A local **TCP socket** carries newline-delimited UTF-8 messages between the
in-game Lua mod and the Python Archipelago client (Client.py). Nothing in this
protocol is versioned on the wire; the apworld's `mod_version` / Client's
`MOD_VERSION` handshake (slot_data `version_check`) is the only compatibility check.

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

## Mod → Client

| Message | Meaning |
|---|---|
| `HELLO` | Sent on every (re)connect, and again after a late-loaded save was wiped by the seed check. Client replies with `SEED`, `SETTINGS`, `CHECKEDSCORE`, then `ITEMS`. |
| `CHECK:<location name>` | A location was earned. Queued in the save (`APState.pending_checks`) and only flushed once the loaded save is verified against this connection's `SEED`, so a check earned while disconnected is never lost. The client buffers checks that arrive before it has the server's location list. |
| `VICTORY:<chronosClears>-<weapons>-<typhonClears>-<weapons>-<zagreusClears>-<hadesClears>-<weapons>-<dreamClears>` | Goal state after a win (`LocationManager.victory_payload`). `<weapons>` is the same number in all three slots: distinct weapons used across every route's clears, Dream included (Dream reuses it; it has no slot of its own). Queued in the save (`victory_pending`) until a verified connection exists. Older clients read only the first 7 fields. |
| `DEATH` | Melinoë died and the `deathlink_amnesty` threshold was reached. The client broadcasts a DeathLink if DeathLink is on. Not queued: a death while disconnected isn't sent. |

## Client → Mod

| Message | Meaning |
|---|---|
| `SEED:<seed_name>` | AP's own per-generation identifier (`ctx.seed_name`, from `RoomInfo`). Sent first on every sync. The mod keeps it for the connection (`Bridge.seed_id`) and compares it with the save's `last_seed_id` (`Bridge.verify_save`): a save last used with a different multiworld is wiped (same wipe as `RESET`); a save with no seed on record is adopted. Nothing save-bound (queued checks, `VICTORY`) is sent until this matches. |
| `SETTINGS:k=v;k=v;...` | Slot settings (Client.py `encode_settings`): the option values the mod needs, the resolved `*_offset` / `*_start` / `*_active` route flags, `location_multiplier`, the room counts, the Dream counter sizes, `enemysanity_shuffle_map` / `miniboss_room_map` (`Name:Name,...`), `goal_requires_<route>` 0/1 flags, and the seed-shape flags `godsanity_chaos` / `dream_met_checks` (0 on a seed generated before those existed, which keeps the mod from gating on an item or sending a check that seed never had). Values never contain `;` or `=`. Cached to disk by the mod for the next boot. |
| `ITEMS:<item>~<sender>\|<item>~<sender>\|...` | The **full ordered list** of received items (stacks repeat). The mod applies only entries past its saved processed index (`APState.processed`), so resending is safe. Applied on the next frame where no menu, conversation or cutscene owns input. |
| `CHECKEDSCORE:underworld=<csv>;surface=<csv>;nightmare=<csv>;dream=<csv>;combined=<csv>` | **point_based only.** Score-check numbers the server already has (a released/collected slot, an admin `!send_location`). The mod advances past them for free instead of spending points to re-earn them. Per number, so gaps are handled. Replaces the previous set. Sent on every sync and on every `RoomUpdate`. `combined` is combine_pools' shared `Score N` pool. Empty lists are allowed. |
| `CHECKED:<location name>\|<player> - <item>` | Echo for a `CHECK` the server didn't already have, with the scouted contents so the corner log can show who got what. The detail after the first `\|` is empty if scouts haven't arrived yet. |
| `DEATH:<source>` | Incoming DeathLink from slot `<source>` (`Archipelago` if the bounce had no source). The mod holds one pending DeathLink and applies it when the player has control: in a run, `deathlink_percent`% of max health (Death Defiance can still save you), or a kill if that setting is 0; in the Crossroads, a death-and-respawn sequence. Further DeathLinks while one is pending are dropped. A DeathLink that arrives while the game isn't connected is held by the client and sent on the next `HELLO`. |
| `GOAL` | The goal was sent to the server. Log only. |
| `RESET` | Debug: clear all applied-item state (processed index, counters, unlocks) so the next `ITEMS` re-applies from scratch. |

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
