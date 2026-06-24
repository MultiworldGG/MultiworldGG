# DELTARUNE MultiworldGG Setup Guide

## Required Software

- DELTARUNE from the [Steam page](https://store.steampowered.com/app/1671210/)
- MultiworldGG from the [MultiworldGG Releases Page](https://github.com/MultiworldGG/MultiworldGG/releases)
- If you want to use AP: DELTARUNE APWorld from the [Releases Page](https://github.com/theemeraldsword85/DELTARUNEAP/releases)
  
## Recommended Software

- If you are using AP: Universal Tracker APWorld from the [UT Releases Page](https://github.com/FarisTheAncient/Archipelago/releases)

## Installation

### Patching the game

**Requires DELTARUNE 1.04 vanilla *(last public branch on Steam)***

On AP, Download the APWorld and place it into archipelago/custom_worlds (Double clicking the APWorld will also work!)

Run the Archipelago Launcher (Or restart the launcher if it's already running)

Start the DELTARUNE client from your MultiworldGG app and input `/auto_patch <Your DELTARUNE Install Directory>` at the bottom.

If you game is a installed on your `C:` drive through Steam, you can use `/auto_patch steaminstall` or if it's a downloaded depot `/auto_patch steamdepot`

If you're not sure, you can easily find the directory by opening the DELTARUNE directory through Steam by right-clicking DELTARUNE in your library and selecting `Manage > Browse local files`. Then, on Windows you can see the directory you need at the top of the window.

Next, go to your MultiworldGG folder either by finding it yourself or by clicking `Browse Files` in your MultiworldGG laucher. If everything went according to plan, you will see a folder called `DELTARUNE`. Inside this folder, run the DELTARUNE application. In the bottom left corner, you'll see the version number. If it matches the version in the titlebar of your Client, then you patched the game successfully.

#### Linux users

**Linux is currently not supported as it will disconnect you from the server few seconds after connection**

The Linux installation is mostly similar, however, DELTARUNE will be installed on Steam as the Linux 
variant.

Since this randomizer only supports the Windows version, we must fix this, by right-click the game in Steam, going to `Properties -> Compatibility`, and checking `Force the use of a specific Steam Play compatibility tool`.

This downloads the Windows version of DELTARUNE to use instead of the Linux version. If the play button is greyed out in Steam, be sure to go to `Settings -> Compatibility` and toggle `Enable Steam Play for all other titles`.

### Create your YAML

Your YAML file is the settings of your MultiworldGG world.

Using `Generate Template Options` you can find the default YAML and other presets in `<MultiworldGG folder Path>\Players\Templates` which you can edit to your liking. You can also use the `Option Creator` in the MultiworldGG Launcher, but be warned that using `Options Generator` will make it harder to read some of the option descriptions. Otherwise it works great.

### Connect to the Multiworld

Open your patched DELTARUNE version and choose `Change connection info` to input your host, port, slot and (if applicable) password.

You can also copy/paste `host:port` directly into the host slot.

If you want to change the preview items color, it's configurable by switching menu with left/right arrow key.

Not required, but you can also open the DELTARUNE Text Client in the MultiworldGG Launcher to use Text commands as well as Universal Tracker features if you have the tracker APWorld installed.

#### Linux users

**On Steam (via Proton)**: This assumes the game is in a Steam Library folder.  Right-click DELTARUNE, go to `Manage -> 
Browse Local Files`. Go up the directories to the `steamapps` folder, open `compatdata/1671210` (1671210 is the "magic number" for
DELTARUNE in Steam).  Save data from here is at `/pfx/drive_c/users/steamuser/AppData/Local/DELTARUNE`.

**Through WINE directly**: This depends on the prefix used.  If it is default, then the save data is located at
`/home/USERNAME/.wine/drive_c/users/USERNAME/AppData/Local/DELTARUNE`.
