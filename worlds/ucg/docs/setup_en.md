# Uncanny Cat Golf Setup Guide

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases).
- [Uncanny Cat Golf](https://slappyhappy2000.itch.io/uncanny-cat-golf) (The game is free!!!!)
- [Uncanny Cat Archipelago Mod](https://github.com/Jeffdev-Archipelago-Implementations/UncannyCatArchipelago)
- [Uncanny Cat Archipelago APWorld](https://github.com/Jeffdev-Archipelago-Implementations/Archipelago-UCG) (not needed with MWGG)
- [Cooler Mods v2.1.1 or higher](https://github.com/JustSomeJello/Cooler-Mods/releases/latest) (Technically optional, but required to make a config menu appear)

## Installation Procedures

1. Download the game and run it at least once, to create all the related folders.
2. Download the Uncanny Cat Archipelago Mod and Cooler Mods.
3. Place both of the ZIP FILES into the folder UNEXTRACTED located at %APPDATA%\Uncanny Cat Golf\mods for windows (unsure what it would be for mac or linux.) [NOTE: YOU MAY NEED TO MAKE THIS FOLDER YOURSELF]
4. Open the game, navigate to the settings menu, then mods on the bottom right, and enable mods.
5. Restart your game, then you should be able to fill out your MultiworldGG information from the title screen!

If you ever need to change any configurations (such as enabling/disabling deathlink, or stuff with the in game text client display) you can select the "gear" icon next to the mod in the mod menu to change configs. These changes will persist throughout. **THIS CONFIG MENU ONLY APPEARS IF YOU HAVE COOLER MODS INSTALLED.**

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the MultiworldGG setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

## Joining a MultiWorld Game

Once the mod is installed and enabled, you simply just have to open the game, click on the title screen, and fill out your connection info. After that, the game will setup your save for you, and you can play as normal!

## Hosting a MultiWorld game

The recommended way to host a game is to use the MultiworldGG hosting service. The process is relatively simple:

1. Collect yaml files from your players, created from the Options Creator on MultiworldGG or from selecting `Generate Template Options` and editing the yaml file.
2. Place these files into the Players folder in the MultiworldGG root folder. If you use AP, place the Uncanny Cat Archipelago APWorld into the custom_worlds folder.
3. Generate with the `Generate` button on the MultiworldGG Launcher.
4. Wait a moment while the seed is generated.
5. When the seed is generated, go to the `output` folder on the MultiworldGG folder.
6. Upload this zip to the [MultiworldGG host upload page](/uploads)
7. Create a new room.
8. Connect with the connection details on the top of the page on the mod. There is no attached client to open in the MultiworldGG launcher, you can connect in game.
