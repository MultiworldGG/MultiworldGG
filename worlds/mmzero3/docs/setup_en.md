# Mega Man Zero 3 Setup Guide

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases) 0.7.100 or later
- If you want to use AP: The [Mega Man Zero 3 apworld](https://github.com/brodieberger/MMZero3Archipelago/releases/latest)
- An English (US) Mega Man Zero 3 ROM
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later

## Optional Software

- [Mega Man Zero 3 PopTracker pack](https://github.com/ambibii/mmz3-poptracker/releases/latest), for use with
  [PopTracker](https://github.com/black-sliver/PopTracker/releases)

## With AP: Installing the apworld

Download `mmzero3.apworld` from the latest release and double-click it. Archipelago will install it into your
`custom_worlds` folder. You can also copy it there yourself

## Generating and Patching a Game

1. Create your options file (YAML). You can make one on the
[Mega Man Zero 3 options page](../../../games/Mega%20Man%20Zero%203/player-options), or start from the example YAML
in the latest release.
2. Follow the general MultiworldGG instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).
This will generate an output file for you. Your patch file will have the `.apmmzero3` file extension.
3. Open `MultiworldGGLauncher.exe`.
4. Select "Open Patch" on the left side and select your patch file.
5. If this is your first time patching, you will be prompted to locate your Mega Man Zero 3 ROM.
6. A patched `.gba` file will be created in the same place as the patch file.
7. On your first time opening a patch with BizHawk Client, you will also be asked to locate `EmuHawk.exe` in your
BizHawk install.

Alternatively, you can double click on the .apmmzero3 file and open with the MultiworldGGLauncher.exe by default. This will go through the same process, but skip steps 3 and 4.

## Connecting to a Server

1. Double click your .apmmz3 or use the "Open Patch" option in the MultiworldGGLauncher
2. The emulator and client will eventually connect to each other. The BizHawk Client window should say that it
connected and recognized Mega Man Zero 3.
3. To connect the client to the server, enter your room's address and port (e.g. `multiworld.gg:38281`) into the
top text field of the client and click Connect, then enter your player name you set in the YAML.