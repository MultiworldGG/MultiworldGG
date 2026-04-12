## Required Software
* Phoenotopia: Awakening: [Available on Steam](https://store.steampowered.com/app/1436590/Phoenotopia_Awakening/)
* BepInEx: Follow the installation guide [here](https://docs.bepinex.dev/articles/user_guide/installation/index.html)
    * **ALWAYS** install the 32bit (x86) version even if you run a 64bit system. Phoenotopia only runs a 86x executable
* PhoA Archipelago Mod: [Github](https://github.com/Amphyros/Phoenotopia-Awakening-AP-client)

## Installing the Archipelago Mod

1. Download [BepInEx](https://docs.bepinex.dev/articles/user_guide/installation/index.html) and follow the installation guide. Be sure to download the **32bit (86x)** version, **even if you're running a 64bit operating system**.
In the guide they refer to the game root. For you this should be `[Your Steam installation folder]\SteamLibrary\steamapps\common\Phoenotopia Awakening`.
After following the steps, your game folder should have a `BepInEx` folder containing (among others) a `plugins` and `config` folder.
2. Download the latest release of the [Phoa Archipelago Mod](https://github.com/Amphyros/Phoenotopia-Awakening-AP-client/releases). The release has a zipfile containing a bunch of .dll files. Extract these files to the `BepInEx\plugins` folder in your game folder.
3. Launch the game, let it run till the Cape Cosmic logo shows and then close it. If you've done everything correctly, the `BepInEx\config` folder now contains a file called: `PhoA_AP_client.cfg`.
4. The mod is now successfully installed! You can open PhoA_AP_client.cfg with a text editor like notepad to change the connection data. More about entering a multiworld game can be found below.
5. OPTIONAL: It might be a good idea to enable the console window, as most of the connection info is logged in there. In the config folder you'll find a file named `BepInEx.cfg`. Open this with a text editor and scroll down to "Logging.Console". Set the value of "Enabled" to "true".
- NOTE: Please do **not** attempt to play the vanilla game with the mod installed, as some features are critically changed. If you want to disable the mod temporarily, drag the dll files from the plugins folder to a place outside the game folder.

## Generating a Multiworld Game

1. Visit the [Player Options](/games/Phoenotopia:%20Awakening/player-options) and configure which types of checks you want to include.
2. Export your YAML file and use it to generate a new randomized game. If you're playing solo, you can also generate a single player game. The site will start hosting a multiworld server which you can join

* For more information about generating a Multiworld game, please refer to the [Web guide](/tutorial/Archipelago/setup_en)

## Joining a Multiworld Game

1. Before starting the game, navigate to the `BepEnIx` folder in your game folder and open the config folder. Then open PhoA_AP_client.cfg with a text editor
2. Adjust the values to match the connection info of the multiworld server you want to join. Save after editing
3. Start the game. If successfully connect, the game should play a confirming sound effect and tell you're successfully connected in the console if you enabled that.

* If you disconnect during your session, your game will try and reconnect every few seconds. The console will give you more information about your connection status.

## Reporting a problem

If you encounter a problem that could possibly be a bug, please report it trough one of the following channels:
1. File an issue at the repository on [Github](https://github.com/Amphyros/Phoenotopia-Awakening-AP-client/issues)
2. Describe your issue in the game thread on the official AP discord.
3. Post it in the mwgg-support channel in the [Unofficial AP Discord](https://discord.multiworld.gg)

Please include as many as possible of the following when reporting a problem:
1. A description of the problem you've encountered.
2. **Probably the most important one**: A step-by-step on how to recreate the problem.
3. Game state information like, which area are you in and which game object were you interacting with.
4. If not ran locally, a link to your AP server.
5. A screenshot or recording of the game state.
6. A copy/screenshot of the console.

* The more information I have, the easier it is for me to find the problem. That being said, I **really** appreciate you helping me test the mod. So don't hesitate to report anything.