# DELTARUNE MultiworldGG Setup Guide

## Required Software

- DELTARUNE from the [Steam page](https://store.steampowered.com/app/1671210/)
  - If you want to use a Steam depot instead of a Steam install, use (`download_depot 1671210 1671212 2054633419585385858`)
- MultiworldGG from the [MultiworldGG Releases Page](https://github.com/MultiworldGG/MultiworldGG/releases)
  - Require minimum 0.7.200
- If you want to use AP: DELTARUNE APWorld from the [Releases Page](https://github.com/theemeraldsword85/DELTARUNEAP/releases)
- DELTARUNE Archipelago mod from [GameBanana Page](https://gamebanana.com/mods/699556) or [Releases Page](https://github.com/Tenebrosful/DeltaruneAP-mod/releases)
  
## HIGHLY Recommended Software

- Only needed with AP: Universal Tracker APWorld from the [UT Releases Page](https://github.com/FarisTheAncient/Archipelago/releases)

## Create your YAML

Your YAML file is the settings of your Archipelago world.

Using `Generate Template Options` you can find the default YAML and other presets in `<MultiworldGG folder Path>\Players\Templates` which you can edit to your liking. You can also use the `Option Creator` in the MultiworldGG Launcher but be warned that using `Options Generator` will make it harder to read some of the option descriptions. Otherwise, it works great.

After setting your options to your liking, you can generate a Multiworld by following 

## Installation

The game mod can either be installed through a Mod Loader or by using the Archipelago client.

You can also patch your game with DeltaPatcher if you would like, though we recommend the other options since they are easier.

### Patching the game with a Mod Loader

Download the mod from [GameBanana](https://gamebanana.com/mods/699556) with either G3M or DeltaMod (We recommend using the xdelta version as it patches in 6 seconds versus csx that patches in like 2 minutes.)

### OR Patching the game with the MultiworldGG DELTARUNE Client

Download the APWorld and place it into archipelago/custom_worlds (Double clicking the APWorld will also work!) (not needed with MWGG)

Download the bsdiff files from the mod [Releases Page](https://github.com/Tenebrosful/DeltaruneAP-mod/releases) (it's the .zip that says "bsdiff" at the end) and unzip the folder.

Rename the unzipped folder `DELTARUNE_PATCH`, and move it to at the root of MultiworldGG folder. If you don't know where that is, you can find your Archipelago folder by clicking `Browse Files` in your Archipelago launcher.

Run the MultiworldGG Launcher (Or restart the launcher if it's already running)

Start the DELTARUNE client from your MultiworldGG app.

If your game is installed on your `C:` drive through Steam, you can type `/auto_patch steaminstall` word for word or if it's a downloaded depot `/auto_patch steamdepot` (`/auto_patch linux` or `/auto_patch linuxdepot` for linux) at the bottom of the client. 

Usually, Steam automatically attempts to download games to you `C:` drive, so it will likely be there unless you know you told Steam to use a `D:` drive, for example. Though, if you're not sure, you can easily find the directory by opening the DELTARUNE directory through Steam by right-clicking DELTARUNE in your library and selecting `Manage > Browse local files`. Then, on Windows you can see the directory you need at the top of the window.

If your game isn't installed on your `C:` drive, or if it's not working for some reason, input the directory as explained in the previous instruction, like `/auto_patch "**[directory]**"`. Obviously don't put the square brackets `[]` inside the command.

Next, go to your MultiworldGG folder. If everything goes according to plan, you will see a folder called `DELTARUNE`. Inside this folder, run the DELTARUNE application. In the bottom left corner, you'll see the version number. If it matches the version in the title bar of your client plus a number at the end, then you patched the game successfully.

#### Linux users

The Linux installation is mostly similar, however, DELTARUNE will be installed on Steam as the Linux variant.

Since this randomizer only supports the Windows version, we must fix this, by right-click the game in Steam, going to `Properties -> Compatibility`, and checking `Force the use of a specific Steam Play compatibility tool`.

This downloads the Windows version of DELTARUNE to use instead of the Linux version. If the play button is greyed out in Steam, be sure to go to `Settings -> Compatibility` and toggle `Enable Steam Play for all other titles`.

### Connect to the Multiworld

Open your patched DELTARUNE version and choose `Change connection info` to input your host, port, slot and (if applicable) password.

You can also copy/paste `host:port` directly into the host slot.

If you want to change the preview items color, it's configurable by switching menu with left/right arrow key.

Not required, but you can also open the DELTARUNE Client in the MultiworldGG Launcher to use Text commands. You can also use Universal Tracker features if you have the tracker APWorld installed.

#### Linux users

Linux users require the usage of a proxy. Start the Archipelago Deltarune Client, then connect to the room and use the command `/linux_proxy`. You should now be able to connect with the window method with `localhost` for host and `1225` as port.

**On Steam (via Proton)**: This assumes the game is in a Steam Library folder.  Right-click DELTARUNE, go to `Manage -> Browse Local Files`. Go up the directories to the `steamapps` folder, open `compatdata/1671210` (1671210 is the "magic number" for
DELTARUNE in Steam). Save data from here is at `/pfx/drive_c/users/steamuser/AppData/Local/DELTARUNE`.

**Through WINE directly**: This depends on the prefix used. If it is default, then the save data is located at
`/home/USERNAME/.wine/drive_c/users/USERNAME/AppData/Local/DELTARUNE`.
