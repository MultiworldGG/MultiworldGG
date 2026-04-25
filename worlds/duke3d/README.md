Duke Nukem 3D Randomizer for Archipelago
========================================

Installation
------------

* Get latest engine binary release from https://github.com/LLCoolDave/NBloodAP/releases or https://github.com/LLCoolDave/Duke3DAP/releases (rednukemAP.exe) (64bit Windows only for now)
* Get DUKE3DAP.zip, DUKE3DAP.grpinfo from https://github.com/LLCoolDave/Duke3DAP/releases and put them in the same directory as rednukemAP.exe
* Get the matching duke3d.apworld from https://github.com/LLCoolDave/Duke3DAP/releases as well.
  * Make sure the DUKE3DAP.zip you use matches the duke3d.apworld used to generate a seed or the client will not connect
* This randomizer requires a duke3d.grp and DUKE.RTS from the **1.5 Atomic Edition** release of Duke Nukem 3D
  * This is the most common distribution of the classic game and bundled with almost all digital release of the past two decades
  * The World Tour 20th Anniversary release is **not** supported
  * duke3d.grp should have SHA1 hash `4fdef8559e2d35b1727fe92f021df9c148cf696c` and MD5 hash `22b6938fe767e5cc57d1fe13080cd522`
  * Rednukem generally detects the files in most installation directories of common distributions of the game. If the auto detection
    does not detect your files, copy them into the same directory as rednukemAP.exe
* This APWorld requires Archipelago 0.4.4!

If all dependencies are detected correctly, a single game of `Duke Nukem 3D Randomizer for Archipelago` should be selectable
in the rednukemAP.exe launcher window

Simply enter your connection details and enjoy!

How the randomizer works
------------------------

All weapon and inventory pickups have been converted into AP locations. If enabled, secret sectors also get converted to locations.

Unlockable items are weapons, ammunition capacity, inventory items and one time buffs.
If enabled, the ability to jump, crouch, sprint, dive into water, open doors and use switches have to be unlocked. 
This is a fun new way to explore the familiar levels.
If diving is unlockable, Duke can only submerge into water while he has scuba gear capacity remaining.

Progression inventory items are restored on every level entry. The logic is designed so that locations can be checked from the start
of a level with the unlocked capacity thresholds, but not necessarily all locations can be checked in a single go. Simply restart a level to try again.

If enabled, saving and loading is enabled. This preserves the level, but **not** player state to be resumed later. For the purposes of inventory management,
loading a previously saved game functions as a new level entry, just at an intermediate state.

Special Thanks
--------------

* The Rednukem team for providing an open source, faithful source port of Duke Nukem 3D to use as a baseline
* Daivuk for creating [apdoom](https://github.com/Daivuk/apdoom/tree/heretic) and the animated Archipelago sprites I shamelessly reused.
* rand0 for supporting me in alpha testing and creating the logic rules for episode 4
* oasiz for being the resident build engine wizzard
