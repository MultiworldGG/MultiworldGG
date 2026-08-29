# Super Mario 64 Hacks Setup Guide

## Prepare your game configuration

1. Take a hack from the list in MultiworldGG or look for the hack you want to play in the [SM64 Hack Archipelago JSONs repository](https://github.com/DNVIC/sm64hack-archipelago-jsons). For a listed hack, the logic is downloaded automatically during generation; note the JSON filename.
2. If the hack is not listed, create a JSON file using the [JSON creator](https://dnvic.com/ArchipelagoGenerator/).
3. Get `template.yaml` from the releases, set `json_file` to the filename of the JSON to use, and put the YAML file in the `Players` folder. A JSON file in a subdirectory can be referenced by filename.
4. Adjust any desired settings in the YAML. Each setting includes a description. Level tickets and move randomization may not work when the selected hack does not support them.

## Connect to a generated game

1. Open the ROM hack and delete or move File B before playing.
2. Open the ROM in [Luna's Project64](https://github.com/Luna-Project64). BizHawk is not supported.
3. Open the generic BizHawk client. In Luna's Project64, enable the debugger if necessary and choose **Debugger → Scripts**.
4. Download the `.js` file from the releases page and put it in the scripts folder. Use the **…** button in the lower-left of the Scripts window to open that folder. If it does not open, open the main window's **Help → AppData** location and create a `Scripts` folder there.
5. Run `connector_pj64_generic.js`.

The game should now be ready to play.

## Support

Use and discussion of this world are not allowed on the main Archipelago server. For help or to share a JSON file, join the [SM64 Hacks Discord](https://discord.gg/Nu4X9gmGDR).
