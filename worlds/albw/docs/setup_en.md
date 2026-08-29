# A Link Between Worlds Setup Guide

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases).
- A decrypted, **North American** A Link Between Worlds `.3ds` ROM until 0.1.3 and `.cci` ROM since 0.1.4. Instructions for dumping your ROM can be found [here](https://wiki.hacks.guide/wiki/3DS:Dump_titles_and_game_cartridges). **Make sure to select "decrypt" when dumping.** Note: if you need a `.cci` ROM, you can rename a `.3ds` ROM and vice versa. These files are identical, only the extension is different. If you have a `.cia` ROM then use [makerom.exe packaged into ctrtool (warning please install makerom not ctrtool)](https://github.com/3DSGuy/Project_CTR/releases) or this [script](https://github.com/davFaithid/CIA-to-3DS-Rom-Converter/releases)
- To play on emulator: [Azahar](https://azahar-emu.org/pages/download/)
- To play on 3ds: [Luma3DS](https://3ds.hacks.guide/) and LittleCube's [plugin.3gx](https://github.com/LittleCube-hax/albw-ap-plugin/releases/latest)

- **The game must be played with the language set to English.**

## Setup

1. Install the latest version of MultiworldGG.
2. If you are using AP: Download `albw.apworld` and put it in your `Archipelago/custom_worlds/` folder.

### Setup (Emulator)

3. In Azahar, select `File > Open Azahar Folder`. Create a `load` folder inside this folder, and inside the `load` folder create a `mods` folder.
4. Also in Azahar, select `Emulation > Configure`. Then, in the general section, on the top, select `Debug`. Finally, at the bottom, ensure that the `Enable RPC Server` option is enabled.
5. (Optional) If you want the patcher to automatically install the mod, run the MultiworldGG Launcher and select `Open host.yaml`. Under `albw_settings`, set `mod_path` to `"<path-to-your-azahar-folder>/load/mods"`. If you are on Windows, make sure to replace all `\` with `/` in the path.

### Setup (3DS)

3. Install Luma3DS, following the guide at https://3ds.hacks.guide/
4. On the Luma3DS configuration screen after power-up (if this screen does not show up, hold SELECT during power-up):
	1. _Make sure_ that `Enable loading external FIRMs and modules` does **NOT** have an x next to it. If so, disable it.
	2. Turn `Enable game patching` on and make sure it **DOES** have an x next to it.
	3. Press Start or choose `Save and exit`.
5. Press L+DPadDown+Select to open the Rosalina menu, and make sure that `Plugin loader` is set to `[Enabled]`.
6. Download [plugin.3gx](https://github.com/LittleCube-hax/albw-ap-plugin/releases/latest) and copy it to `/luma/plugins/00040000000EC300/` on your SD card.
7. (Optional) If you want the patcher to automatically install the mod, run the Archipelago Launcher and select `Open host.yaml`. Under `albw_settings`, set `mod_path` to `"<path-to-your-sd-card>/luma/titles"`. If you are on Windows, make sure to replace all `\` with `/` in the path.


## Generating a Game

1. Create your player options YAML file. A sample YAML is included.
2. Gather the YAMLs of all players into the `Archipelago/Players` folder.
3. Run the MultiworldGG Launcher and select Generate.
4. A zip file will be created in the `MultiworldGG/output` folder. Upload this to [the MultiworldGG website](/uploads) to host your game.
5. Inside the zip file is a `.apalbw` file. You **will need** this file to play the game.

## Playing a Game

### Playing a Game (Emulator)

1. The host will give you a `.apalbw` file. Drag and drop this file onto the MultiworldGG Launcher. Alternatively, run the Launcher, click Open Patch, and select your `.apalbw` file.
2. Enter the path to your A Link Between Worlds ROM when prompted (first time only, it is saved in `MultiworldGG/host.yaml`). Wait about 20 seconds for the client to create a patch for the game. If you set a `mod_path` during [Setup](#setup), skip steps 3 and 4.
3. This will do two things. First, it will open the A Link Between Worlds client. Second, it will create a zip file with the same name and directory as the patch file. Unzip this file; it contains a folder named `00040000000EC300`.
4. Place the `00040000000EC300` folder inside the `load/mods/` folder you created. (If there is already a folder with this name from a previous randomizer, delete it first.)
5. Run A Link Between Worlds in the emulator. The client should automatically connect to the emulator.
6. Enter the server URL into the client and press Connect.

### Playing a Game (3DS)

1. Insert your 3ds SD card into the computer.
2. The host will give you a `.apalbw` file. Drag and drop this file onto the MultiworldGG Launcher. Alternatively, run the Launcher, click Open Patch, and select your `.apalbw` file.
3. Enter the path to your A Link Between Worlds ROM when prompted (first time only, it is saved in `MultiworldGG/host.yaml`). Wait about 20 seconds for the client to create a patch for the game. If you set a `mod_path` during [Setup](#setup), skip steps 4 and 5.
4. This will do two things. First, it will open the A Link Between Worlds client. Second, it will create a zip file with the same name and directory as the patch file. Unzip this file; it contains a folder named `00040000000EC300`.
5. Copy the `00040000000EC300` folder to `/luma/titles/` on your SD card.
6. Re-insert your SD card into your 3DS and power it on.
7. Run A Link Between Worlds. At the end of the red 3DS loading screen, you should see a blue flash. This means the plugin has loaded successfully.
8. Run the command on-screen into your ALBW client.
9. Enter the server URL into the client and press Connect.

## Resuming a Game

1. Run the MultiworldGG Launcher and select the A Link Between Worlds client.
2. Perform steps 5-6 under Playing a Game (Emulator) or steps 7-9 under Playing a Game (3DS).
