# Setup Guide for Lego Star Wars: The Complete Saga in MultiworldGG

## Required Software
- PC Release of Lego Star Wars: The Complete Saga
  - Both the Steam version and GOG version are supported.
  - The retail PC release is not expected to work currently, unless it is identical to the GOG version.
- MultiworldGG
- Lego Star Wars: The Complete Saga apworld

## Optional Software
- [Lego Star Wars: The Complete Saga Archipelago Tracker](https://github.com/Mysteryem/TCS_AP_PopTracker/releases/latest), 
for use with [PopTracker](https://github.com/black-sliver/PopTracker/releases)
- (ships with MultiworldGG) [Universal Tracker](https://discord.com/channels/731205301247803413/1367270230635839539) for Archipelago (links to the
Universal Tracker channel in the Archipelago discord server). Lego Star Wars: The Complete Saga Archipelago supports
yamlless Universal Tracker tracking. The Lego Star Wars: The Complete Saga Client will embed Universal Tracker within
the client when Universal Tracker is installed.
- [DxWnd](https://sourceforge.net/projects/dxwnd/) for alternate or more control over playing in a window instead of using `/toggle_windowed` in the client
  - DxWnd works better with the GOG version of the game because the Steam version has SteamStub DRM applied
  - Only download DxWnd from the linked *sourceforge.net* site, dxwnd.org is an **impersonation** and could serve **malware**
  - In DxWnd, use `File`>`Import`, and then open the `Lego Star Wars - The Complete Saga` file in the `DxWnd\exports`
folder. After importing, right click and `Modify`, then adjust the `Path` to your `LEGOStarWarsSaga.exe` and adjust the
window size to your liking (`W` and `H` in `Main`>`Position`>`Window initial position & size`)
  - In-game, change the game's resolution to match the window size (optional, but recommended) 
  - Additional steps for Steam version:
    - The Steam version can sometimes crash when starting when run through Dxwnd, but it is stable once it has managed
to start. You should at least sometimes get to the TTGames logo screen before crashing if everything is set up
correctly. Crashes can occur as late as the title screen.
    - If Lego Star Wars: The Complete Saga is installed on a separate drive to Steam, and you get
`Application load error 5:0000065434` when starting the game through DxWnd, copy your `Steam.exe` file into the same
directory as your `LEGOStarWarsSaga.exe`.

## Apworld Installation Instructions (not needed with MultiworldGG)

Install the Lego Star Wars: The Complete Saga apworld by either
- double-clicking on the .apworld,
- or directly putting it into your `custom_worlds` folder,
- or by dragging and dropping the apworld onto the Archipelago Launcher.

The Archipelago Launcher will need to be restarted if it was already open when the apworld was installed.

## Connecting to the MultiworldGG server
When connecting to a multiworld for the first time, a new game should be started. Save slots are bound to the first
multiworld seed and slot name they were connected to. To resume playing a multiworld at a later time, the same save slot
that initially connected to that multiworld should be loaded.

To connect to the multiworld server, run the **Lego Star Wars: The Complete Saga Client** from the **MultiworldGG Launcher**
and connect it to the MultiworldGG server. Lego Star Wars: The Complete Saga must be running before a connection can be
made.

The first time a save file connects to a MultiworldGG server, the slot name needs to be entered. After that, the slot
name will be set into the save data and read automatically from the save file by the client when connecting.

An in-game message will be displayed when the client is fully connected and running.

## Additional Setup for Linux
The client uses the `pymem` library, to read from/write to the game's memory, which only directly supports Windows,
therefore, additional setup is required to get the AP randomizer to work on Linux.

Follow the steps in [Flit's Linux Guide for Lego Star Wars TCS AP](https://gist.github.com/FlitPix/458ac9fb33610acc8bb3278ce071abca).
Ping `@flit` in the [Archipelago discord server's Linux & Steamdeck Setup thread](https://discord.com/channels/731205301247803413/957390083193966612)
for additional assistance with the Linux setup.