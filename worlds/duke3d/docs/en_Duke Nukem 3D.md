# Duke Nukem 3D Randomizer

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a config file.

## How the randomizer works

All weapon and inventory pickups have been converted into AP locations. If enabled, secret sectors also get converted to locations.

Unlockable items are weapons, ammunition capacity, inventory items and one time buffs.
If enabled, the ability to jump, crouch, sprint, dive into water, open doors and use switches have to be unlocked. 
This is a fun new way to explore the familiar levels.
If diving is unlockable, Duke can only submerge into water while he has scuba gear capacity remaining.

Progression inventory items are restored on every level entry. The logic is designed so that locations can be checked from the start
of a level with the unlocked capacity thresholds, but not necessarily all locations can be checked in a single go. Simply restart a level to try again.

If enabled, saving and loading is enabled. This preserves the level, but **not** player state to be resumed later. For the purposes of inventory management,
loading a previously saved game functions as a new level entry, just at an intermediate state.

## Special Thanks

* The Rednukem team for providing an open source, faithful source port of Duke Nukem 3D to use as a baseline
* Daivuk for creating [apdoom](https://github.com/Daivuk/apdoom/tree/heretic) and the animated Archipelago sprites I shamelessly reused.
* rand0 for supporting me in alpha testing and creating the logic rules for episode 4
* oasiz for being the resident build engine wizzard
