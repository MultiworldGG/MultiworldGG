# Castlevania: Dawn of Sorrow MultiworldGG Randomizer Setup Guide

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases)
* [Bizhawk 2.10+](https://github.com/TASEmulators/BizHawk) 
- A legally obtained USA ROM of Castlevania Dawn of Sorrow

## Installation Procedures

### Windows Setup

1. Download and install MultiworldGG from the link above, making sure to install the most recent version.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the MultiworldGG setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get an options file?

The Player Options page on the website allows you to configure your personal options and export a config file from
them. You can also create one with your local MultiworldGG install.

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/mysterycheck)

## Joining a MultiWorld Game

### Generating and Patching a Game
1. Follow the general MultiworldGG instructions for generating a game. This will generate an output file for you. Your patch file will have the .apcvdos file extension.
   Open MultiworldGGLauncher.exe
2. Select "Open Patch" on the left side and select your patch file. Alternatively, you can open the MultiworldGGBizhawkClient with your patch file.
3. If this is your first time patching, you will be prompted to locate your vanilla ROM.
4. A patched .nds file will be created in the same place as the patch file.
5. On your first time opening a patch with BizHawk Client, you will also be asked to locate EmuHawk.exe in your BizHawk install.

If you are playing offline, you can simply run your ROM at this point. For Multiworld play, see the following section.

### Connecting to a Server
By default, opening a patch file will do steps 1-5 below for you automatically. Even so, keep them in your memory just in case you have to close and reopen a window mid-game for some reason.

1. This game uses MultiworldGG's BizHawk Client. If the client isn't still open from when you patched your game, you can re-open it from the launcher.
2. Ensure EmuHawk is running the patched ROM.
3. In EmuHawk, go to Tools > Lua Console. This window must stay open while playing.
4. In the Lua Console window, go to Script > Open Script….
5. Navigate to your MultiworldGG install folder and open data/lua/connector_bizhawk_generic.lua.
6. The emulator may freeze every few seconds until it manages to connect to the client. This is expected. The BizHawk Client window should indicate that it connected and recognized the game.
7. To connect the client to the server, enter your room's address and port (e.g. multiworld.gg:38281) into the top text field of the client and click Connect.
8. You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is perfectly safe to make progress offline; everything will re-sync when you reconnect.
