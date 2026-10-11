# Ratchet & Clank: Size Matters

A MultiworldGG implementation for Ratchet & Clank: Size Matters

## FAQ
- [Where is the settings page?](#where-is-the-settings-page)
- [What does randomization do to this game?](#what-does-randomization-do-to-this-game)
- [What options are available?](#what-options-are-available)
- [What is the goal?](#what-is-the-goal)
- [What items can be in another player's world?](#what-items-can-be-in-another-players-world)
- [When the player receives an item, what happens?](#when-the-player-receives-an-item-what-happens)
- [Setup guide](#setup-guide)

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options for configuring your randomizer experience.

## What does randomization do to this game?

All weapons, gadgets, armour pieces, and infobots are shuffled into the item pool and placed on the following location
types. Some of these are always in the pool; others are only included when their corresponding option is turned on
(noted below) — the exact total for your seed depends on your settings.

| Location type | Count | Notes |
|---|---|---|
| Titanium Bolts | 20 | Always included. |
| Armour Pickups | 21 total | Two pieces (Metalis Gloves, Challax Chestplate) require Giant Clank; the Hyperborean/Chameleon pieces additionally require Challenge Mode 1/2 (and NG+ Items). |
| Boss | 1 | Defeating Otto Destruct on Quodrona. |
| Gadget Pickups | 2 | Always included. |
| Weapon Vendors | 12 | Always included — one per weapon's kiosk. |
| Gadget Vendors | 5 | Always included. |
| Weapon Mod Vendors | 23 | Always included; 10 of these are Challenge Mode 1+ only. |
| Weapon Titan Vendor purchases | 12 | Requires Challenge Mode 1+. One per Titan-eligible weapon (every weapon except RYNO) — see [the weapon vendor FAQ entry](#how-does-the-weapon-vendors-leftright-view-work) for how this interacts with Progressive Weapons. |
| Story Missions | 18 (fewer without Giant Clank/Clank Challenges) | Requires All Missions. Two entries need Giant Clank; one needs Clank Challenges. |
| Cutscenes | 18 | Requires All Cutscenes. |
| Skill Points | up to 19 | Requires Skill Points: 8 on Easy, 19 on Hard (Easy's 8 plus 11 more). Clank Challenge (3) and Skyboard Challenge (2) skill points are controlled by their own separate toggles, on top of this. |
| Clank Challenge rewards | 6 | Requires Clank Challenges: Item Challenges (or higher). Filtered further by Clank Challenge Groups (Demolition Derby / Gadgetbot Toss / Gadgetbot) — excluding a group drops its locations from both this tier and the one below. |
| All Clank Challenge completions | 24 (on top of the rewards above) | Requires Clank Challenges: All. |
| Skyboard race completions | 4 | Requires Skyboard Challenges: All. |
| Extra Skyboard checks | 4 | Requires Skyboard Challenges: All. |
| Shrink Ray puzzle checks | 7 | Requires Shrink Ray Options: Locations. |
| Armour Set Checks | 13 | Requires Armour Set Checks (on by default). |
| Weapon Level 4 | 13 | Requires Weapon Level Checks: Level 4 (or Level 4 and 8 / All). |
| Weapon Level 8 | 12 | Requires Weapon Level Checks: Level 8 (or Level 4 and 8 / All) **and** Challenge Mode 1+. |
| Weapon Level 2-3 | 26 | Requires Weapon Level Checks: All. |
| Weapon Level 5-7 | 36 | Requires Weapon Level Checks: All **and** Challenge Mode 1+. |
| Nanotech (health) Level | up to 70 | Requires Nanotech Level Interval != Off. `all`: one check per level from 6 up to Nanotech Level Max. every_5/10/25: one check per level that's a multiple of the interval and no higher than Nanotech Level Max — e.g. every_5 with max 75 gives 14 checks (10, 15, ... 75). Levels 51-75 only exist with Challenge Mode 1+; without it the max is capped at 50. |

A bare-defaults YAML generates around 106 locations. With every optional location type enabled, the pool goes well past 300.

## What options are available?

The full option list with all details lives on the [player settings page](../player-settings), but here's a summary
of everything specific to this game:

| Option | Default | What it does |
|---|---|---|
| Starting Weapons | 2 | Number of random weapons precollected at the start. |
| Starting Gadgets | 1 | Number of random gadgets precollected at the start (1 grants the Hypershot). |
| Clank Pack | Off | Adds one Clank Pack unlock item. Ratchet starts without Clank's backpack abilities and regains them when it arrives. This is not a progressive item. |
| Random Starting Planet | Off | Off: start on Pokitaru; Ryllus requires its own infobot. Weighted: two of the seven eligible planets are chosen at random, weighted by how many locations they offer under your other settings (vendor locations only count if Starting Weapons/Gadgets is above 0). Unweighted: the same two-planet pick, but uniformly random. The replaced starting infobot goes back into the item pool. Dreamtime, Inside Clank, and Quodrona are never candidates. |
| Starting Bolts | 45,000 | Bolts precollected at the start. |
| Balance Patch | Off | Enables usernamecipher's Update 1.03 weapon and movement balance changes, including the Ryllus gadgetbot door bypass and Otto-specific damage changes. Supports US, EU and JP; applied by the client on level load. |
| Progressive Weapons | Off | Off: weapons are individual items, leveling works as in vanilla. Manual: a single Progressive Weapon item per weapon caps how far you can level by playing. Automatic: level is set directly from Progressive Weapon items received, no need to play to level up. With Challenge Mode 1+, a weapon at level 4 moves up to level 5 automatically: with Off as soon as the Challenge Mode tier is 1+, with Manual or Automatic once its 5th Progressive Weapon copy is received. Buying the Titan vendor location never changes a weapon's level itself. |
| Progressive Mods | Off | On: one Progressive Mod item per weapon grants mod slots in sequence, instead of each slot being its own item. |
| Progressive Armour | Off | Off: each armour piece is its own item. Per Set: each armour set has its own progressive item (Progressive Wildfire, Progressive Sludge Mk9, etc.) — 4 copies unlock that set's 4 pieces in order. Unified: a single Progressive Armour item grants pieces one set at a time in a fixed order: Wildfire, Sludge Mk9, Crystallix, Electroshock, Mega Bomb, Hyperborean, Chameleon. |
| Enabled Weapons | every weapon on | Selects which weapons are included in generation. Setting a weapon to 0 removes its item(s) (including Progressive Weapon/Mod items), its vendor location, its mod-vendor locations, and its Weapon Level checks. At least one long-range projectile weapon must remain available after NG+ Items is applied. |
| Trap Chance | 0% | Percent chance for each filler item to be replaced with a trap. |
| Trap Weight | equal | Relative weights of each trap type when a filler item rolls as a trap. |
| Trap Duration | 20s per trap (Reset Level is instant) | How many seconds each trap type stays active once triggered. |
| Weapon Experience Multiplier | 4x | Multiplies weapon experience gained, speeding up leveling (0/1 = no boost, up to 16x). Stops applying past level 4 (level 8 with Challenge Mode). |
| Bolt Multiplier | 4x | Multiplies bolts gained from crates/enemies (0/1 = no boost, up to 16x). Doesn't affect one-off AP grants like Starting Bolts. |
| Nanotech Experience Multiplier | 4x | Multiplies Nanotech (health) experience gained, speeding up Nanotech leveling (0/1 = no boost, up to 16x). |
| All Missions | On | Adds story mission completions as location checks. |
| All Cutscenes | Off | Adds cutscene/flag-event triggers as location checks. |
| Giant Clank | Off | On: the Giant Clank Metalis and Giant Clank Challax sequences become playable and their completion/armour/skill point checks are added. Off: entering either sequence immediately forces a load back out, as in vanilla before this option existed. |
| Clank Challenges | Item Challenges | Off: none. Item Challenges: only the armour/gadget reward per arena. All: every individual challenge completion is its own check. |
| Clank Challenge Groups | every group on | Selects which Clank Challenge groups (Demolition Derby / Gadgetbot Toss / Gadgetbot) get location checks at all, once Clank Challenges is on. Setting a group to 0 excludes all of its locations (both tiers) from generation — the challenge itself is still fully playable in-game, it just has no AP check. |
| Enable Clank Challenge Skill Points | Off | Adds skill points earned from Clank Challenge arenas as checks, regardless of the Clank Challenges option. |
| Skyboard Challenges | Off | All: every individual Skyboard race completion is a separate check. |
| Enable Skyboard Challenge Skill Points | Off | Adds skill points earned from Skyboard Challenges as checks, regardless of the Skyboard Challenges option. |
| Shrink Ray Options | Locations | Off: vanilla — puzzles must be solved normally, no checks. Locations: Shrink Ray puzzle completions become location checks. Skip: every tracked puzzle gate is force-solved automatically, bypassing whatever it would otherwise block (no checks). |
| Skill Points | Off | Off: none. Easy: a curated set of easier skill points. Hard: also includes a curated set of harder skill points. Clank Challenge and Skyboard Challenge skill points are controlled separately (see above), regardless of this setting. |
| Armour Set Checks | On | Treats equipping a complete armour set as a check. Adds 13 locations. |
| Weapon Level Checks | Off | Off: none. Level 4: one check per weapon for reaching level 4. Level 8: one check per weapon for reaching level 8 (Challenge Mode 1+ only). Level 4 and 8: both. All: one check per weapon per level, 2 through 8 (5-8 requires Challenge Mode 1+). |
| Nanotech Level Interval | Off | Off: no Nanotech (health) level checks. All: every level is its own check, up to Nanotech Level Max. every_5 / every_10 / every_25: one check for every level that's a multiple of the interval, up to Nanotech Level Max. Levels above 20 need access to a good EXP planet. |
| Nanotech Level Max | 75 | Highest Nanotech Level Nanotech Level Interval will create a check for — e.g. every_5 with this set to 25 checks only levels 10, 15, 20, 25. No effect while Nanotech Level Interval is Off. |
| NG+ Items | On | Off: removes RYNO and the Chameleon/Hyperborean armour sets from generation (along with their Weapon Level and Armour Set checks, and Stalker/Ice II, which need a Chameleon or Hyperborean piece), since these are New Game Plus exclusives that would be unobtainable on a fresh playthrough. |
| Max Challenge Mode | 0 | Enables the game's Challenge Mode (New Game Plus) tier and controls how far generation reaches into it. 0: vanilla, no Challenge Mode content. 1: adds the RYNO vendor purchase, 10 Challenge-Mode-only weapon mod purchases, and the 4 Hyperborean armour pieces. 2: everything from tier 1, plus the 4 Chameleon armour pieces. Without Progressive Challenge Mode, this is the tier the game starts in (written to memory on connect); with it, this is the highest tier the progressive items can raise you to. Everything this unlocks is still gated by NG+ Items — with that off, this option alone has no effect. |
| Progressive Challenge Mode | Off | On: adds one Progressive Challenge Mode item per tier (Max Challenge Mode 2 adds 2 copies). Tier 1 content requires 1 copy received, tier 2 content requires 2, and the in-game Challenge Mode tier rises as copies arrive instead of being fixed at connect. Off: Challenge Mode content is reachable as soon as its planet is. |
| Death Amnesty | 0 | Number of deaths allowed before items are removed from your inventory on death. Higher is more forgiving. |
| Experimental Skins | Off | Patches the thirteen red multiplayer skins into the single-player skin menu. Experimental. When off, the multiplayer skins aren't patched in and Starting Skin can't be set to one of them. |
| Starting Skin | Default | Cosmetic skin for Ratchet, applied automatically on each planet load. Includes the seven single-player skins and thirteen red multiplayer skins (the multiplayer skins need Experimental Skins on), with no blue variants. All skins are unlocked in-game regardless of this choice. Can also be changed while playing with `/skin`. |
| AP Icon | Original | Archipelago icon shown on vendor items: Original, Purple, Grey, or Blue. Can also be changed while playing with `/apicon`. |

### Clank Pack and No Clank trap

The optional `clank_pack: true` setting removes Clank from Ratchet's back until the
single **Clank Pack** item is received. It unlocks the backpack high and long jumps.
Normal movement and jumping still work, and playable Clank sections are unaffected.
Placement logic conservatively requires the pack for field checks; shops, armour
set checks, and Clank challenges retain their existing requirements.

**Trap: No Clank** remains available independently of this option. It temporarily
removes the pack for 20 seconds by default (configurable through Trap Duration).
Repeated traps add time. Receiving Clank Pack during a trap unlocks it once the
trap ends; a trap expiring before the item arrives does not grant the pack.
Removal waits until Ratchet is safely on the ground, and follows him across level
changes. The client must be connected to enforce these effects.

### Game Links

Cross-player options, each with a matching client-side toggle you also need to turn on (`/toggle_ammolink`, `/toggle_boltlink` — see the [setup guide](setup_en.md#client-commands)) before they actually do anything — enabling the YAML option alone auto-enables the toggle on connect, but you can flip any of them on/off per-session from the client too, same as Death Link.

**These only ever link you with other Ratchet & Clank: Size Matters players** — never with players of other games, even ones on your same team. Ghost Link picks its candidate peers by explicitly matching game, and Ammo/Bolt Link's underlying sync data is keyed under this game's own namespace, so another game's client never sees or touches it.

| Option | Default | What it does |
|---|---|---|
| Ammo Link | Off | Mirrors weapon ammo counts with every other connected, linked player: whenever your ammo for a weapon changes, everyone else linked for that weapon is updated to match, and vice versa. Players don't need matching weapon inventories. |
| Bolt Link | Off | Mirrors your bolt count with every other connected, linked player — spend or collect bolts on any linked player and everyone else's balance matches. |
| Ghost Link | Off | Renders another linked, connected player as a static ghost clone whenever you're both on the same planet. Only one ghost can ever be shown at once — if multiple linked players share your planet, the lowest slot number wins. Has an additional host.yaml-level kill switch (applied at generation time, not by the running server — see [dynamicpine's docs](../../dynamicpine/docs/adding_to_apworld.md) for the distinction if you host on a different machine than you generate on). |
| Ghost Link Update Interval | 5s | How often (in seconds) your position is broadcast to other Ghost Link players. 0 broadcasts as fast as possible (every poll tick, no throttling). |

Plus the standard MultiworldGG options (Death Link, Progression Balancing, Accessibility, Start Inventory From Pool,
etc.) shared across every game.

## What is the goal?

Defeat **Otto Destruct** on Quodrona. The client detects the end-boss cutscene completing and automatically sends goal completion to the MultiworldGG server.

## What items can be in another player's world?

Any weapon, gadget, armour piece, or infobot. When progressive modes are enabled, you receive `Progressive Weapon`, `Progressive Mod`, or `Progressive Armour` items that unlock each in a fixed order instead.

## When the player receives an item, what happens?

You will be able to visit the planets with whatever infobot you receive, receiving Infobot: Kalidon will unlock Kalidon
for travel within Ratchet's Ship. Upon receiving a weapon it unlocks in ratchet's inventory, which will let you equip it
and use to fire on enemy troops. Progressive upgrades will upgrade your weapons increasing their
firepower.

## How does the weapon vendor's left/right view work?

Any weapon's vendor menu has two views, swapped with D-Pad Left/Right:
- **Left (default) view** — the normal purchasable list: whatever's still available to buy at this vendor. If a weapon has already been fully purchased here, the vendor opens straight into the right view instead, since there's nothing left to show on the left.
- **Right view** — your full owned inventory instead, so you can buy ammo for a weapon you already own that isn't (or is no longer) listed on this vendor's purchasable side.

The PDA is ammo-only: it uses the game's normal PDA prices and ammo restrictions, with no Left/Right view switching or AP purchase locations.

With Challenge Mode 1+, a Titan-eligible weapon's kiosk also lists its Titan variant once the base weapon has reached level 4 — buying it is just a location check and never changes the weapon's level. The weapon moves up to level 5 on its own (with Progressive Weapons Off, as soon as Challenge Mode is 1+; with Manual or Automatic, once its 5th Progressive Weapon copy is received), and the check for the Titan purchase location fires the moment the level 4→5 transition happens, vendor visit or not.


## Setup guide

See [the Setup Guide](setup_en.md) for full instructions on connecting PCSX2 to MultiworldGG.
