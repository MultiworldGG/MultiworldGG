# Setup Guide for Ocarina of Time MultiworldGG

## Required Software

- An Emulator of choice
  - [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) (v2.10+) (not on Linux)
  - [Project 64](https://www.pj64-emu.com/windows-downloads)
  - [simple64](https://simple64.github.io/)
  - [Rosalie's Mupen GUI](https://github.com/Rosalie241/RMG)
  - [Gopher64](https://github.com/gopher64/gopher64) (Windows/Linux)
  - [ares](https://ares-emu.net/) (Windows/Linux)
  - [RetroArch](https://www.retroarch.com/?page=platforms) (works on MacOS) 
- The built-in MultiworldGG Ocarina of Time client, which gets installed alongside [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases).
- If you want to use AP: The latest APWorld from [here](https://github.com/TreZc0/OoTR-APWorld/releases)
- An Ocarina of Time v1.0 NTSC-U or NTSC-J ROM.

## Install the APworld (only on AP)

Since OoT currently ships with AP in a non-standard way, the old apworld will collide with the new one. Before installing this apworld, make sure to delete the `oot` folder in `lib/worlds` in your MultiworldGG folder. Afterwards, to install the APworld, simply double click it or drag and drop it into the running MultiworldGG Launcher. Alternatively, you can choose the option `Install APWorld` in the Archipelago Launcher or drop the `.apworld` file into the `custom_world`-folder in your Archipelago install.

After installing, restart the Launcher.

### Important Note

Archipelago current hardcodes the OoT Client and OoT Adjuster independently of the apworld, so they will stick around either way. For this new apworld, you NEED to use the new clients, named `Ocarina of Time Client` and `Ocarina of Time Adjuster`, both featuring a description clearly outlining the new apworld version.

## Configuring the Emulator

- Good guides to set up your emulator for choice for OoT Randomizer can be found in the official [OoTR wiki](https://wiki.ootrandomizer.com/index.php?title=Setup#Emulators)
  - Please note that Dolphin is currently not supported.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the MultiworldGG setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Options page on the website allows you to configure your personal options and export a config file from
them. Player options page: [Ocarina of Time Player Options Page](/games/Ocarina%20of%20Time/player-options)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/mysterycheck)

## Joining a MultiWorld Game

### Obtain your OOT patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apz5` extension.

Double-click on your `.apz5` file to start your client and start the ROM patch process. Once the process is finished
(this can take a while), the client and the emulator will be started automatically.
Alternatively, you can run the `Ocarina of Time Adjuster` from the launcher, allowing you to customize you seed with a lot of visual and sfx options, like custom music, voices, models, and a lot of color and sound options.
After patching, the client is started automatically.

To choose a specific emulator for auto-launch, set `oot_options.emulator_path` in your `host.yaml` to your emulator
executable. If it is blank, the patching process will ask you to select an emulator executable before auto-launching.

### Connect to the Multiserver

Once both the client and the emulator are started, the Ocarina of Time Client will connect to the loaded ROM automatically. You do
not need to open the BizHawk Lua console or drag in a connector script. If the client is not connecting, make sure the
patched ROM is loaded in a supported emulator and use `/n64` in the client to check the emulator connection status.
For RetroArch, install an N64 capable core (Mupen64Plus-Next for example) and enable `Settings > Network > Network Commands` and leave the Network Command Port at `55355`.

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)

Now you are ready to start your adventure in Hyrule.
