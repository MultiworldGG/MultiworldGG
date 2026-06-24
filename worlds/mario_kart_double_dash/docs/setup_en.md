# Setup Guide for Mario Kart: Double Dash!! MultiworldGG

## Requirements

You'll need the following components to be able to play MKDD AP:
* [MultiworldGG](https://multiworld.gg/tutorial/Archipelago/setup/en) 0.7.100 or newer
    * If you are new to MultiworldGG it is recommended to read the guide above.
* [Mario Kart Double Dash APWorld](https://github.com/aXu-AP/archipelago-double-dash/releases)
    * Not needed if you use MWGG
    * The apworld should install simply by double clicking it if you have Archipelago installed.
    * Alternatively, drop the apworld inside `custom_worlds` folder in your Archipelago installation (presumably `C:/ProgramData/Archipelago/custom_worlds`)
* [Dolphin Emulator](https://dolphin-emu.org/download/). **We recommend using the latest release.**
    * For Linux users, you can use the flatpak package
    [available on Flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu).
* A rom of Mario Kart: Double Dash!! (NTSC-U / USA version)
    * Format (`.iso`, `.rvz`) doesn't matter.

Optionally, there's 2 options for tracking your progress:
* [PopTracker pack](https://github.com/Razerock/double-dash-ap-tracker/releases) by Raze
    * Requires [PopTracker](https://github.com/black-sliver/PopTracker/releases).
    * Shows available locations and obtained items with a nice interface.
    * Logic doesn't follow the difficulty modeling exactly, but is close enough.
* [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases) (ships with MultiworldGG)
    * Text-based, shows a list of accessible locations.
    * If you have Universal Tracker installed, the client will have a tracker page automatically.
    * Might be better on single screen / small screen setups.

## Setting Up a YAML

All players must provide the room host with a YAML file containing the settings for their world. Modify the template yaml from the [releases](https://github.com/aXu-AP/archipelago-double-dash/releases) page to your liking.
Once you're happy with your settings, provide the room host with your YAML file and proceed to the step "Connecting to a Room". If you want to play by yourself, you need to host the game yourself, see the next section.

## Self-hosting

* Place your YAML file in `Players` folder in your MultiworldGG installation (presumably `C:/Program Files/MultiworldGG/Players`).
* Open MultiworldGG Launcher and click Generate. A console window should pop up, do its stuff and close shortly.
* Click Host and locate your generated seed named `AP_#######.zip` at `output` folder in your MultiworldGG installation (presumably `C:/Program Files/MultiworldGG/output`).

## Connecting to a Room

Unlike most randomizers, MKDD AP doesn't need you to patch your rom beforehand. Everything is done at runtime.
Do note, that using the randomizer unlocks everything in your save of MKDD and you will probably make unrealistically good time trials times. So if you care for your vanilla save, you should do a backup of your save first!
* Open Mario Kart Double Dash Client from MultiworldGG Launcher.
  * You can also click your slot name in multiworld.gg room.
* Open Dolphin and launch the game.
  * You can use the "Launch Game" button in the client.
  * At this point, the client should say "Patch Applied".
  * **Important!** Do not select game mode before you are connected to the host!
* Write your host connection info in the box at the top of the client (if you are hosting yourself it's `localhost`) and press enter.
* Write your slot/player name (if you didn't modify the YAML then it's `Player1`) into the box at the bottom and press enter.

## Playing the Game

You should now get checks whenever you finish races. To see what is currently unlocked, type `/unlocked` in the client. To see what checks you can do, use Tracker page located at the top of the client (if you installed Universal Tracker).

## Troubleshooting

* For most random behavior / something doesn't work quite right try these first!
  * Restart the game.
  * Restart the client.
* The game crashes when I try to select a character.
  * You probably aren't connected to a server. Restart the game and ensure you have connection.
* The game crashes (other).
  * Use unmodified Mario Kart Double Dash USA rom. "Debug" build, MKDD Extender or other versions don't work.
  * Disable any Gecko codes like widescreen hack.
* Where's my patch?
  * There's no patch, use vanilla rom.
* Can I use ar/gecko cheat codes?
  * Gecko codes don't work, AR codes should mostly work.
  * If you find a cheat that doesn't work and you would like it to work, you can open an issue and we'll try to look into it.
* The client can't connect to Dolphin.
  * Make sure you are using USA version of MKDD.
  * Use MultiworldGG 0.7.100 or newer.
  * Try running the client with admin privileges.
  * As a last resort try resetting your settings (MAKE BACKUP FIRST - deleting `%appdata%/Dolphin Emulator` deletes your saves as well).
