# Mega Man Zero 3

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Every stage is unlocked by its own access item, and the mission select screen lets you pick any stage you have the
access item for. Secret disks, weapons, armor chips, EX skills and sub tanks are all shuffled into the multiworld.
Clearing a stage always brings you back to the Resistance Base, and you can leave any stage at any time.

The mission select screen shows the boss portraits in pages of four, like in vanilla. Use left and right on the d-pad
(or the shoulder buttons) to switch pages. Hovering a stage shows its name, how many of its secret disks you have found,
whether it is LOCKED, OPEN or CLEARED, and your best rank on it. Picking a stage you have already cleared gives you two
choices: EXPLORE is the vanilla revisit for picking up disks you missed, and RETRY MISSION plays the stage as a real
mission again, with the boss included, for another try at the A+ rank check.

## What is the goal?

Clear the Abandoned Research Laboratory and defeat Omega. The stage only opens once you have cleared every other stage and are holding enough
secret disks, (120 by default).

## What items and locations get shuffled?

Locations:
- All 180 secret disks
- Each stage clear
- An A+ rank clear in each of the 15 stages (the rank needed is set with `ex_skill_rank`)
- The nine armor chips
- Both sub tanks
- Cerveau's Recoil Rod and Shield Boomerang
- Eleven miniboss fights
- Optionally, the ten 1-UPs placed in stages (`extra_life_sanity`, on by default)
- Optionally, the 82 life capsules and E-Crystals placed in stages (`itemsanity`)
- Optionally, the slots in Cerveau's shop (`shop_slots`)

Items:
- 180 secret disks
- The four weapons, as progressive items
- Nine armor chips
- Twelve EX skills
- Two sub tanks
- Fifteen stage access items
- Two Story Progress items
- E-Crystals as filler, and traps if `trap_percentage` is enabled.

## Which items can be in another player's world?

Any of the items above can be placed in another player's world.

## What does another world's item look like in Mega Man Zero 3?

Secret disk pickups are drawn as the Archipelago logo. With `extra_life_sanity` or `itemsanity` on, the pickups that
are checks have a small Archipelago logo over them until you collect them. Cerveau's shop shows the name of each item
and which player it is for.

## When the player receives an item, what happens?

The item is applied right away, and a small icon for it pops up over Zero's head. When the item is a secret disk, a
message box at the bottom of the screen also says which disk it is (turn this off with `disk_name_popup`). Received disks
need to be opened from the secret disk analysis screen like in the vanilla game.

## Progressive weapons

Each weapon is a progressive item. The first copy you receive gives you the weapon itself, the next ones unlock its abilities,
and the last three raise its attack power ( which are damage boosts from the e-Reader cards). 

This works a lot like the weapon level system from Zero 1 and 2, with your progress being shown as stars in the pause menu.

| Weapon | Upgrades, in order |
| --- | --- |
| Buster | weapon, semi charge, full charge, damage +1, +2, +3 |
| Z-Saber | weapon, 2nd slash, 3rd slash, charged slash, damage +1, +2, +3 |
| Recoil Rod | weapon, charged rod, damage +1, +2, +3 |
| Shield Boomerang | weapon, charged throw, damage +1, +2, +3 |

## What other changes are made to the game?

- Later NPC conversations, and the checks attached to them, are locked behind the two Story Progress items.
- Cerveau has a shop. Open it with L or R on his secret disk analysis screen, and buy items with E-Crystals.
- Pressing SELECT on the secret disk analysis screen opens every disk you own.
- The pause menu shows how many secret disks you need for the final stage.
- All skippable cutscenes can be skipped.
- Enemies that can drop disks are marked with the AP logo.
- Pressing SELECT during gameplay does one thing of your choice. By default it swaps sub weapons.
- EX skills are awarded based on your score on the stage you just cleared. Your overall rank is the average of your best clear on each stage.
- Some lore secret disks also unlock a random e-Reader graphics change. The full list is
  [here](https://tcrf.net/Mega_Man_Zero_3/e-Reader_Functions).

## What are the item and location name groups?

These work with `!hint`, for example `!hint Stage Access` or `!missing Sub Arcadia`.

| Locations | |
| --- | --- |
| Per stage | `Resistance Base` (all three mission sets), `Aegis Volcano Base`, `Sunken Library`, and so on |
| By type | `Secret Disks`, `Stage Clears`, `Chips`, `A+ Rank Clears`, `Subtanks`, `Weapons`, `1-UPs`, `Minibosses`, `Itemsanity`, `Shop` |

| Items | |
| --- | --- |
| By type | `Secret Disks`, `Stage Access`, `Chips`, `Body Chips`, `Foot Chips`, `Head Chips`, `EX Skills`, `Subtanks`, `Weapons`, `Traps` |

## Is there a tracker?

Yes, there is a PopTracker pack made by ambibii. [Get it here.](https://github.com/ambibii/mmz3-poptracker/releases/latest)

## Bugs
Report bugs on [GitHub](https://github.com/brodieberger/MMZero3Archipelago/issues) or in the MultiworldGG Discord.

Click [here](https://github.com/brodieberger/MMZero3Archipelago) for a slightly more in depth Readme.