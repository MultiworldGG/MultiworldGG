# MultiworldGG: Path of Exile

## What does randomization do?

The apworld does not modify Path of Exile directly. Instead it:

- Reads your character data through the GGG API (equipment, gems, passive points).
- Reads your PoE `Client.txt` log to detect zone changes and in-game chat.
- Writes an item filter to highlight items that correspond to unchecked AP locations.
- Validates that you are only using items and abilities you have actually unlocked.

## The core loop

1. **Enter a zone** — the client pulls your current character state from the GGG API, validates that you're in logic, and sends any new checks you've earned.
2. **Pick up items** — highlighted items in the filter are base types tied to unchecked locations.
3. **Change zones** — checks are sent for any items you've picked up or conditions you've met (levels, area visits) since the last zone change.

Checks are sent **on zone change**, not the moment you pick something up. If you pick up an item and nothing happens immediately, that is expected — just walk to the next area.

## What are locations (checks)?

- Picking up specific item base types that drop from monsters (e.g. a particular sword base, a specific boot base).
- Reaching certain character levels (if enabled).
- Visiting certain areas of the campaign (if enabled).
- Defeating boss encounters (for boss-rush goals).

## What are items (unlocks)?

Unlocks you can receive from the multiworld:

| Category | Examples |
|---|---|
| Character classes | Marauder, Ranger, Witch, Duelist, Templar, Shadow |
| Ascendancy classes | Berserker, Deadeye, Elementalist, etc. (up to 3 per class) |
| Gear rarity | Normal / Magic / Rare / Unique per slot |
| Flask slots | Up to 5 normal, magic, and unique flask slots |
| Linked gem sockets | Maximum supported gem links per slot |
| Passive skill points | Each unlock grants one spendable point |
| Skill gems | Active abilities (Fireball, Heavy Strike, etc.) |
| Support gems | Gem modifiers (Added Fire Damage, Brutality, etc.) |
| Utility gems | Auras, movement skills, curses, buffs |
| Alternate gems | "of Trarthus" variants — requires the "Alternate Gems" unlock and the base gem |

Items from other worlds are highlighted in your item filter. Receiving an unlock does **not** place an item in your inventory — it unlocks the ability to equip or use that category of item once you find one in-game.

## Out of logic

If you equip something you haven't unlocked — a rarity tier you don't have, a gem you haven't received, too many linked supports, etc. — you are **out of logic**. **Alternate gems** (e.g. "Heavy Strike of Trarthus") require both the "Alternate Gems" unlock item and the base gem ("Heavy Strike") to be received. While out of logic:

- Your item filter switches to `__invalid`, showing all items the same way to avoid giving you information.
- Checks are **not sent** until you return to a valid state.
- The client whispers you the specific reason on each zone change.

To recover: unequip or stash the offending item, then change zones.

## Starting a run

By default, you start with access to one character class and some starting gear (configurable). Everything else — other classes, gear rarities, gems, flask slots, passive points — must be unlocked through checks.

**Scion** is not available as a starting class. She is locked behind her in-game rescue quest in Act 3, and must be unlocked as an AP item.

## Options

### Goal
- Complete the campaign (reach Karui Shores after Act 10)
- Complete a specific act
- Defeat a set of bosses (configurable pool and count)

### Character
- **Starting character** — which base class you begin with (random by default)
- **Ascendancies available per class** — 0 to 3 ascendancy unlocks per base class
- **Allow unlock of other characters** — whether other base classes can appear as items
- **Usable starting gear** — how much of the Twilight Strand starting items you can use (weapon only, weapon + gems, weapon + gems + flasks, or nothing)

### Gear and progression
- **Progressive gear** — gear rarity upgrades arrive in order (Normal → Magic → Rare → Unique) for more balanced pacing
- **Gear unlock starting point** — optionally start with some rarities already unlocked
- **Flask slots** — whether flask slots are restricted and must be unlocked
- **Linked sockets** — whether the number of support gem links is restricted
- **Passive skill points** — whether you must unlock passive points before spending them
- **Level-ups as locations** — whether reaching each character level is a check
- **Area visits as locations** — whether entering each campaign zone for the first time is a check
- **Skill, support, and utility gems** — whether gem types must be unlocked

### Minimum available per act
Each restriction (gear upgrades, flask slots, links, gems) has a configurable minimum that guarantees a certain number of unlocks are reachable by each act, preventing complete progression blocks.

### Gucci Hobo Mode
An extreme challenge mode that restricts you to unique items only (or allows only one non-unique slot). Expect a very slow early game. Not recommended for first runs.

### Client options
- **Loot filter sounds** — jingle, TTS, random audio, or none for AP item drops
- **TTS** — text-to-speech for received item names
- **DeathLink** — share deaths with other players in the multiworld

---

## Tips

- **Vendor recipes still work.** Chromatics, fusings, and the crafting bench are all fair game. SSF crafting knowledge is especially useful here.
- **Starting gear matters.** Starting with no gems means Default Attack until you unlock something. No flasks means survival is harder through early acts. There is no shame in starting with your class weapon, gem, and flasks enabled.
- **Check often.** Walking through a zone entrance is what triggers check sends, so a quick map loop is more valuable than staying in one area.
- **Town portal to offload items.** If your inventory fills up with unchecked base items, portal to town and stash them — they'll register as checks on your next zone entry.
- **"Bad" skills are viable.** If your goal is Kitava, not endgame mapping, many otherwise-ignored skill gems become completely usable. Use what you have.
- **Alternate gems need two unlocks.** To use a "of Trarthus" gem (e.g. "Sunder of Trarthus"), you need the "Alternate Gems" item received from the multiworld AND the base gem (e.g. "Sunder") received.
- **The Equipment tab** in the ArchiPoElago client shows exactly what you can currently equip and how much rarity you've unlocked per slot.

---

## Bugs and support

- Discord: ask in the Path of Exile channel on the Archipelago Discord server.
- GitHub issues: [github.com/stubobis1/Archipelago/issues](https://github.com/stubobis1/Archipelago/issues)

---

*This product is not affiliated with or endorsed by Grinding Gear Games.*
