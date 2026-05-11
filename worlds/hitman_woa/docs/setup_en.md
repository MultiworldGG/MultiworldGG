# Setup Guide for HITMAN World of Assassination

## Required Software

- Any game from the World of Assassination Trilogy from either Steam or Epic Games
  - Hitman (2016) [Steam](https://store.steampowered.com/app/236870/HITMAN/)/[Epic](https://www.epicgames.com/store/en-US/p/hitman)
  - Hitman 2 (2018) [Steam](https://store.steampowered.com/app/863550/HITMAN_2/)/[Epic](https://www.epicgames.com/store/en-US/p/hitman-2)
  - Hitman 3 / Hitman World of Assassination (2021) [Steam](https://store.steampowered.com/app/1659040/HITMAN_World_of_Assassination/)/[Epic](https://www.epicgames.com/store/en-US/p/hitman-3)
    - The Demo version of Hitman 3 is not supported
- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases)
- [Peacock](https://github.com/thepeacockproject/Peacock/releases/latest)
- The [Archipelago Plugin for Peacock](https://github.com/BenDipp/Archipelago/releases/latest) and (if you want to use stock AP) the [Hitman APworld](https://github.com/BenDipp/Archipelago/releases/latest)

### Optional software
- [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases?q=Tracker) for a map tracking (ships with MWGG)

## Installation

### Peacock

If you already have installed Peacock, it is still recommended to install a seperate instance for MultiworldGG, as the obtaining of items and unlocks will mess with your Peacock progression.

More information about the installation can be found on the [Peacock website](https://thepeacockproject.org/wiki/intel/installation/).

 1. Download the latest version of [Peacock](https://github.com/thepeacockproject/Peacock/releases/latest).
 2. Unzip the files into an easily accessible place.
    - Do not place them in the game folder or the "Program Files" folder of Windows.
 3. In that unzipped folder run both `Start Server.cmd` and `PeacockPatcher.exe`.
 4. Start Hitman to verify it worked. The Main Menu should feature a Panel stating "Powered by The Peacock Project".
 5. Close `Start Server.cmd` and place `archipelago.plugin.js` in the `plugins`-folder.
 6. Run `Start Server.cmd` again. The Server Console should feature a line with the text `[Info | Archipelago Plugin] Archipelago Plugin Loaded.`.

### APworld

This is not needed if you use MultiworldGG. To install the APworld, simply double click it or drag and drop it into the running Archipelago Launcher. Alternatively, you can choose the option `Install APWorld` in the Archipelago Launcher or drop the `.apworld` file into the `custom_world`-folder in your Archipelago install.

After installing, restart the Launcher and `HITMAN World of Assassination Client` should appear as an option in the `Client` list.

If your Peacock Server is not running locally on your machine or is using a different port than default, you must change the address and port that the Client uses to connect to Peacock in the `host.yaml` of your MultiworldGG installation.

## Joining a Multiworld 

 1. Run both `Start Server.cmd` and `PeacockPatcher.exe` from the folder where Peacock is installed.
 2. Run the `MultiworldGG Launcher` and choose `HITMAN World of Assassination Client` in the `Client` list.
 3. Enter room's address and port (e.g. `multiworld.gg:12345`) into the top text field of the client and click Connect.
 4. Enter your slot name.
 5. Start Hitman from the Launcher of your choice. Your unlocked Levels can be found under `Campaigns > Archipelago`.
    - If you received a level while in the main menu, the campaigns tab will not update unless you enter and leave a level, or click "Go Offline" and then "Go Online" in the main menu.  

## Uninstalling

To play Hitman unmodified, simply launch Hitman without having `PeacockPatcher.exe` open to connect to official IOI Servers.

To play Hitman with Peacock but without MultiworldGG, simply delete `archipelago.plugin.js` from the `plugins`-folder and Launch Hitman with `PeacockPatcher.exe` and `Start Server.cmd` open.