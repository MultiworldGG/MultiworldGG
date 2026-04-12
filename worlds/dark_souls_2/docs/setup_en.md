# Dark Souls II Randomizer Setup Guide

## Required Software

- The PC version of [Dark Souls II](https://store.steampowered.com/app/236430/DARK_SOULS_II/) or [Dark Souls II: Scholar of the First Sin](https://store.steampowered.com/app/335300/DARK_SOULS_II_Scholar_of_the_First_Sin/)
- [Dark Souls II Archipelago Mod](https://github.com/WildBunnie/DarkSoulsII-Archipelago/releases)

## Optional Software

- [Map Tracker](https://github.com/AkagiCritMagnet/Dark-Souls-2-poptracker-for-Archipelago)

## Setting Up

On the mod’s release page, you will find three files:
- One `.apworld` file (not needed with MultiworldGG)
- Two `.zip` files (one for each game version)

### Installing the Mod

1. Download the correct ZIP file for your game version:
   - `SOTFS` (Scholar of the First Sin)
   - `VANILLA` (Original version)
2. Extract (unzip) the ZIP file.
3. Copy all extracted files.
4. Navigate to your game installation directory.
5. Open the `GAME` folder (where the game's `.exe` file is located).
6. Paste the copied files into the `GAME` folder.
7. (Optional) Open `ds2modengine.ini` to adjust configuration settings.
   - We do **not** recommend using your main save file (`sl2`) or playing online while using the mod.

<!-- TODO linux instructions -->

### Running and Connecting to the Game

1. Launch the game. An overlay should appear automatically.
2. Before creating a save file, connect to the MultiworldGG server:
   - Enter the server URI (e.g. `multiworld.gg:123456`)
   - Enter your slot name (the one defined in your YAML file, e.g. `JohnDarkSoulsII`)
   - (Optional) Enter the server password, if one is set
   - Click **Connect** and wait until the overlay displays `Connected`
3. Once connected, create a new save file and start playing.
4. Always connect from the main menu **before** loading a save file.

## Frequently Asked Questions

### Enemy Randomizer

Enemy and boss randomization is not currently supported by the Archipelago mod.

You may use external enemy randomizers, such as [this one](https://www.nexusmods.com/darksouls2/mods/1317), but installation is not trivial, as both mods modify the same game files. For updated instructions, please visit the Dark Souls II channel on the [official Archipelago Discord](https://discord.com/invite/8Z65BR2).

### Installing Other Mods

The included `ds2-modengine` (the `dinput8.dll` file) can load additional DLL mods.

By default, it loads mods from the `archipelago` folder (configured in `ds2modengine.ini`).

To add another DLL mod:
1. Rename the DLL to something other than `dinput8.dll`.
2. Place it in the `archipelago` folder.

## Troubleshooting

### Game Crashes

This can happen for many different reasons, but below are some common causes:

- Make sure you are on the latest Steam version of the game, no other versions are supported