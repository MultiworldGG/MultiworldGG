# Hades 2 ↔ Archipelago bridge protocol (v0.1)

A local **TCP socket** carries newline-delimited UTF-8 messages between the
in-game Lua mod and the Python Archipelago client.

- **Transport:** TCP on `127.0.0.1:43055`. Hardcoded on both ends (Client.py
  `BRIDGE_HOST`/`BRIDGE_PORT`, Bridge.lua `BRIDGE_HOST`/`BRIDGE_PORT`) --
  deliberately NOT in config.lua, since r2modman's config editor lets players
  edit it and a mismatch breaks the connection with no error on either side.
- **Roles:** the Python client is the **server** (listens); the Lua mod is the
  **client** (connects out on load, retries on failure).
- **Framing:** one message per line, terminated by `\n`.
- **Format:** `COMMAND:payload` (payload may be empty). Lists use `|` as the
  delimiter (no item/location name contains `|`).

## Mod → Client

| Message | Meaning |
|---|---|
| `HELLO` | Sent on (re)connect. Client replies with `SETTINGS` then a full `ITEMS` resync. |
| `CHECK:<location name>` | A location check was completed in-game. |
| `VICTORY:<chronosClears>-<chronosWeapons>-<typhonClears>-<typhonWeapons>` | Run-completion stats for goal evaluation (per-route clears + distinct weapons that have cleared). |
| `DEATH` | Melinoë died (broadcasts a DeathLink, if enabled and the send threshold is met). |

## Client → Mod

| Message | Meaning |
|---|---|
| `SETTINGS:k=v;k=v;...` | Slot settings from the generated seed. Includes `location_system` (0 point / 1 room / 2 per-weapon-room), `score_rewards_amount`, `underworld_room_count`/`surface_room_count` (fixed room-check counts per route, used for the cap and the final-boss cascade), `included_routes`, `underworld_active`/`surface_active` (whether each route was generated), the sanity modes, goal counts, deathlink params, etc. |
| `ITEMS:<name>\|<name>\|...` | The **full ordered list** of received items (stacks repeat). The mod applies only those past its saved processed-index, so this is safe to resend any time. |
| `SCORESYNC:underworld_room=R;surface_room=S;combined_room=C` | Highest already-earned **room** check per route (`combined_room` = the combine_pools shared room pool). The mod advances `room_high` past these so a fresh save doesn't re-notify already-earned room checks. No longer carries point-based keys — point_based skipping moved to `CHECKEDSCORE`. Per-weapon room checks aren't synced (their high-water is per weapon); they re-notify harmlessly. Sent on each sync. |
| `CHECKEDSCORE:underworld=<csv>;surface=<csv>` | **point_based only.** The comma-separated check numbers of `<route> Score N` locations the server **already** has (a finished player's auto-released/collected checks, an admin `!send_location`, fresh-save recovery). The mod skips those checks for **free** — advancing `next_check` past them without spending score or re-sending the `CHECK` — instead of charging score to re-earn them. Per-number (not a high-water mark) so out-of-order gaps like "0017 checked, 0015 not" are handled. **Replaces** the set on each receive. Sent on each sync (so a reconnecting mod gets the current set) and again on every `RoomUpdate` (so a player finishing mid-session is reflected immediately). Empty lists are allowed (`underworld=;surface=`). |
| `CHECKED:<location name>\|<player> - <item>` | Echoed back immediately after the client forwards a `CHECK`. Carries the scouted contents of that location so the mod's subtle corner log can show who got what (e.g. `Sent Score Check 15 - Mario64 - Power Star`). The detail after `\|` is empty if scout data hasn't arrived yet. |
| `DEATH:<source>` | Incoming DeathLink — the mod damages Melinoë by `deathlink_percent`% of max health (or kills outright if 0), and shows a "`<source>` Killed You" banner. `source` is the sending player's slot name (falls back to `Archipelago` if the bounce didn't carry one). |
| `GOAL` | Acknowledgement that the goal was registered as met (optional/cosmetic). |
| `RESET` | Debug: clear all applied-item state (processed index, counts, unlocks) so the next `ITEMS` re-applies from scratch. |

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
