# ULTRAKILL Multiworld Setup Guide

First, download and install the Archipelago mod with r2modman, or manually by extracting the contents of the zip file into the `plugins` folder. If you decide to install manually, you will also need to install [PluginConfigurator](https://github.com/eternalUnion/UKPluginConfigurator).

Optionally, you can also download [NoTutorial](https://thunderstore.io/c/ultrakill/p/TRPG/NoTutorial/) to avoid accidentally entering the tutorial when making new save files.

*Note that only one player in the multiworld will need to complete steps 1-5.*

1. Download and install [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases).

2. Unless you are using MWGG: Download `ultrakill.apworld` from the mod's [releases page](https://github.com/TRPG0/ArchipelagoULTRAKILL/releases) and add it to your `worlds` folder. (Default path: `C:\ProgramData\Archipelago\lib\worlds`)

3. Set up all `.yaml` files for each player in the multiworld, then add them to the `Players` folder. A template can be downloaded for ULTRAKILL from the mod's [releases page.](https://github.com/TRPG0/ArchipelagoULTRAKILL/releases) A guide for advanced settings can be found [here.](/tutorial/Archipelago/advanced_settings/en)

4. Run `MultiworldGGGenerate.exe` to generate a game, which will appear in the `output` folder.

5. Host a game, either manually, or by [uploading](https://multiworld.gg/uploads) it to the MultiworldGG website.

6. To connect to the server, first select a new save file. Then open the options menu, click the PLUGIN CONFIG button, click Configure next to Archipelago, and open the PLAYER SETTINGS menu. Enter your name, the server's address in the form of `address:port`, and a password if necessary, then click the Connect button.

There are also some commands that can be used by pressing `F8` to open the console:

- `connect [address:port] [player] [password]` - Connect to an MultiworldGG server.
- `disconnect`: Disconnect from an MultiworldGG server.
- `say [message]`: Send messages or commands to the server.