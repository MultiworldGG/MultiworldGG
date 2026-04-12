# UFO 50 Setup Guide

## Required Software
- [UFO 50](https://store.steampowered.com/app/1147860/UFO_50/) for PC
- The [UFO 50 APWorld](https://github.com/UFO-50-Archipelago/Archipelago/releases) (bundled with MultiworldGG)

## Installation

### Automated Installation
1. Unless you use MultiworldGG: Place the UFO 50 APWorld in your `custom_worlds` folder.
2. Create a new folder for the modded UFO 50 installation (don't put it in your normal UFO 50 install folder). Do not manually copy anything into this folder.
3. Open the MultiworldGG Launcher and click on the UFO 50 Client.
4. When it asks you to select a folder for the mod installation, select the folder you created in step 2.
5. When it asks you to locate the UFO 50 executable, navigate to your UFO 50 .exe file and select it.
6. To launch the game, run the UFO 50 Client from the MultiworldGG Launcher.


### Manual Installation

Do not follow these steps if you are doing the Automated Installation above.

Extra required software:
- A way to apply `.bsdiff4` patches, such as [bspatch](https://www.romhacking.net/utilities/929/).

Steps:
1. Copy all of your UFO 50 files to a safe location.
2. Extract all files from `ufo_50_archipelago.zip` into the same directory as the files extracted in the previous step.
   * This should include, at least, `ufo_50_basepatch.bsdiff4` and `gm-apclientpp.dll`.
3. Delete `steam_api64.dll` and `Steamworks_x64.dll`.
4. If you don't have `original_data.win`, copy `data.win` and rename its copy to `original_data.win`.
   * By keeping an unmodified copy of `data.win`, you will have an easier time updating in the future.
5. Apply the `ufo_50_basepatch.bsdiff4` patch using your patching software.
6. To launch the game, run `ufo50.exe`.

### Downpatching UFO 50

As UFO 50 is a game that is still receiving updates, periods of time between new official patches and the mod being updated will exist.
Therefore, the user may end up having to either wait for the mod to be updated or use an older version of the game in order to play. You can check which version of UFO 50 the mod targets [in the patch releases page](https://github.com/UFO-50-Archipelago/Patch/releases).

0. You may wish to make a backup of your save files before proceeding.
1. Launch Steam in Online Mode.
2. Open the Steam Console by entering `steam://open/console` on any file or internet browser.
3. On the Steam Console, enter `download_depot 1147860 1147861 7193516691465454523`.
4. Steam will now download the right version of the game, wait for the download to finish. There is no progress bar.
5. Once the download is finished, a path to the contents will be displayed, note it down, as it may be required for installation.
6. Enter the depot folder and delete `steam_api64.dll` and `Steamworks_x64.dll`, then launch to game.
7. In the intro, look at the bottom left corner and verify that the version is the same version the mod targets.
8. You can now proceed with the installation, using the depot folder if prompted to locate UFO 50.

## Joining a MultiWorld Game

Launch the game and continue until you reach the profile select screen, which has been replaced with the connection screen.

From here, enter the different menus and type in the following details in their respective fields. In order:
- **server:port** (e.g. `multiworld.gg:38281`)
   * If hosting on the website, this detail will be shown in your created room.
- **slot name** (e.g. `Player`)
   * This is your player name, which you chose along with your player options.
- **password** (e.g. `123456`)
  * If the room does not have a password, it can be left empty.
