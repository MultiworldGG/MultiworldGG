## Before Playing
This randomizer assumes the player is aware of hidden techniques that allow the game to be beaten without items, even at the lowest settings. It is HIGHLY recommended to play through the Basic section of the [Platforming Tricks Tutorial](https://steamcommunity.com/sharedfiles/filedetails/?id=1706422414) before starting your first seed!

Additionally, the logic assumes that the player knows of hidden paths throughout the game, revealed with Ribbon, Fire Orb, or Carrot Bombs. A patch is available to expose these paths, alongside other useful features! It can be enabled by setting "Apply Beginner Mod" to `true`.

## To Install
1. Download and install the latest archipelago release from the [Archipelago Releases page](https://github.com/ArchipelagoMW/Archipelago/releases).
2. Download `rabi_ribi.apworld` from the latest release on the [Archipelago Rabi-Ribi Releases page](https://github.com/tdkollins/Archipelago-Rabi-Ribi/releases)
3. Open `rabi_ribi.apworld` with Archipelago Launcher; it will be automatically installed to Archipelago's `custom_world` folder.

## To Generate a Game
1. Download `Rabi-Ribi.yaml` from the latest release on the [Archipelago Rabi-Ribi Releases page](https://github.com/tdkollins/Archipelago-Rabi-Ribi/releases)
2. Edit the file to have your desired settings.
3. Navigate to your Archipelago installation (by default, `C:\ProgramData\Archipelago`).
4. Navigate to the `Players` folder under your Archipelago base folder.
5. Move `Rabi-Ribi.yaml` into this folder (you can rename it if you wish).
6. Open Archipelago Launcher and click the **Generate** button.
7. Your generated game will be in the `Output` folder in the Archipelago base folder.

## To Host a Game
1. Navigate to the [Host Game](https://archipelago.gg/uploads) page.
2. Upload the `.zip` file outputted from the above "To Generate a Game"

## To Start Playing
1. Make sure you have an Archipelago room from the previous "To Host a Game".
2. Open the Archipelago Launcher and click "Rabi-Ribi Client".
3. Connect to the room via the room URL and port.
4. (First Time) When prompted, select the **Rabi-Ribi Installation Folder** on Steam. (This can be changed later via the `host.yaml` file in your Archipelago base folder)
5. (First Time, Optional) When prompted, select the **Rabi-Ribi Poptracker Pack** `.zip` file, available [here](https://github.com/rajanb/RabiRibiPoptracker). (This can be changed later via the `host.yaml` file in your Archipelago base folder)
6. Launch Rabi-Ribi through Steam.
7. On the Rabi-Ribi main menu, press F5 and select the scenario listed in the Rabi-Ribi Client.
8. Start and have fun!

## Using Universal Tracker
Universal Tracker is fully supported in the Rabi-Ribi APWorld! This includes support for providing an external poptracker pack to enable a Map Tracker tab. You can get the latest poptracker pack [here](https://github.com/rajanb/RabiRibiPoptracker). The Map Tracker also supports showing your current location, represented by an Erina Badge.

Note: If you have used a previous version of the Rabi-Ribi APWorld, you may need to edit your `host.yaml` to set the location of the pack, with `ut_pack_path` under `rabi_ribi_options`.

## Other Notes
At this time, the only goal this randomizer supports is "Easter Egg Hunt", which are all local! The goal is NOT to complete the base game (although there is intention to add this later).