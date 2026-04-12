# StarCraft 2 Randomizer Setup Guide

This guide contains instructions on how to install and troubleshoot the StarCraft 2 MultiworldGG client, as well as 
where to obtain a config file for StarCraft 2.

## Required Software

- [StarCraft 2](https://starcraft2.com/en-us/)
   - While StarCraft 2 for AP/MWGG supports all four campaigns, they are not mandatory to play the randomizer. 
   If you do not own certain campaigns, you only need to exclude them in the configuration file of your world.
- [The most recent MultiworldGG release](https://github.com/MultiworldGG/MultiworldGG/releases)

## How do I install this randomizer?

1. Install StarCraft 2 and MultiworldGG using the links above. The StarCraft 2 MultiworldGG client is downloaded by the 
MultiworldGG installer.
   - Linux users should also follow the instructions found at the bottom of this page 
     (["Running in Linux"](#running-in-linux)).
2. Run Starcraft II Launcher from the MultiworldGG Launcher.
   - macOS users should instead follow the instructions found at ["Running in macOS"](#running-in-macos) for this step 
   only.
3. Type the command `/download_data`. 
This will automatically install the Maps and Data files needed to play StarCraft 2 AP/MWGG.

## Where do I get a config file (aka "YAML") for this game?

Yaml files are configuration files that tell MultiworldGG how you'd like your game to be randomized, even if you're only 
using default options.
When you're setting up a multiworld, every world needs its own yaml file.

There are three basic ways to get a yaml:
* You can go to the [Player Options](/games/Starcraft%202/player-options) page, set your options in the GUI, and export 
the yaml.
* You can generate a template, either by downloading it from the [Player Options](/games/Starcraft%202/player-options) 
page or by generating it from the Launcher (`MultiworldGGLauncher.exe`). 
The template includes descriptions of each option, you just have to edit it in your text editor of choice.
* You can ask someone else to share their yaml to use it for yourself or adjust it as you wish.

Remember the name you enter in the options page or in the yaml file, you'll need it to connect later!

Check out [Creating a YAML](/tutorial/Archipelago/setup/en#creating-a-yaml) for more game-agnostic information.

### Common yaml questions

#### How do I know I set my yaml up correctly?

The simplest way to check is to use the website [validator](/check). 

You can also test it by attempting to generate a multiworld with your yaml. Save your yaml to the `Players/` folder 
within your MultiworldGG installation and run `MultiworldGGGenerate.exe`. 
You should see a new `.zip` file within the `output/` folder of your MultiworldGG installation if things worked 
correctly. 
It's advisable to run `MultiworldGGGenerate.exe` through a terminal so that you can see the printout, which will include 
any errors and the precise output file name if it's successful. 
If you don't like terminals, you can also check the log file in the `logs/` folder.

#### What does Progression Balancing do?

For StarCraft 2, this option doesn't have much impact. 
It is an MultiworldGG option designed to balance world progression by swapping items in spheres. 
If the Progression Balancing of one world is greater than that of others, items in that world are more likely to be 
obtained early, and vice versa if its value is smaller. 
However, StarCraft 2 is more permissive regarding the items that can be used to progress, so this option has little 
influence on progression in a StarCraft 2 world. 
StarCraft 2. 
Since this option increases the time required to generate a MultiWorld, we recommend deactivating it (i.e., setting it 
to zero) for a StarCraft 2 world.

#### How do I specify items in a list, like in excluded items?

You can look up the syntax for yaml collections in the 
[YAML specification](https://yaml.org/spec/1.2.2/#21-collections). 
For lists, every item goes on its own line, started with a hyphen:

```yaml
excluded_items:
  - Battlecruiser
  - Drop-Pods (Kerrigan Tier 7)
```

An empty list is just a matching pair of square brackets: `[]`. 
That's the default value in the template, which should let you know to use this syntax.

#### How do I specify items for the starting inventory?

The starting inventory is a YAML mapping rather than a list, which associates an item with the amount you start with. 
The syntax looks like the item name, followed by a colon, then a whitespace character, and then the value:

```yaml
start_inventory:
  Micro-Filtering: 1
  Additional Starting Vespene: 5
```

An empty mapping is just a matching pair of curly braces: `{}`. 
That's the default value in the template, which should let you know to use this syntax.

#### How do I know the exact names of items and locations?

You can look up a complete list of the item names in the 
[APSC2 Item Docs](https://archipelago-sc2.github.io/content-docs/) page.
This page also contains supplementary information of each item.
However, the items shown in that page might differ from those shown in the datapackage page of MultiworldGG since the 
former is generated, most of the time, from beta versions of StarCraft 2 AP/MWGG undergoing development.

As for the locations, you can see all the locations associated to a mission in your world by placing your cursor over 
the mission in the 'StarCraft 2 Launcher' tab in the client.

## How do I join a MultiWorld game?

1. Run MultiworldGGLauncher.exe.
2. Search for the Starcraft 2 Client in the launcher to open the game-specific client
   - Alternatively, steps 1 and 2 can be combined by providing the `"Starcraft 2 Client"` launch argument to the launcher.
3. In the Archipelago tab, type `/connect [server IP]`.
   - If you're running through the website, the server IP should be displayed near the top of the room page.
   - The server IP may also be typed into the top bar, and then clicking "Connect"
4. Type your slot name from your YAML when prompted.
5. If the server has a password, enter that when prompted.
6. Once connected, switch to the 'StarCraft 2 Launcher' tab in the client. There, you can see all the missions in your 
world.

Unreachable missions will have greyed-out text. Completed missions (all locations collected) will have white text.
Accessible but incomplete missions will have blue text. Goal missions will have a gold border.
Mission buttons will have a color corresponding to the faction you play as in that mission.

Click on an available mission to start it.

## Troubleshooting

### I can't connect to my seed.

Rooms on the MultiworldGG website go to sleep after two hours of inactivity; reload or refresh the room page
to start them back up.
When restarting the room, the connection port may change (the numbers after "multiworld.gg:"),
make sure that is accurate.
Your slot name should be displayed on the room page as well; make sure that exactly matches the slot name you
type into your client, and note that it is case-sensitive.

If none of these things solve the problem, visit the [Discord](https://discord.com/invite/8Z65BR2) and check
the #software-announcements channel to see if there's a listed outage, or visit the #starcraft-2 channel for
tech support.

### The game isn't launching when I try to start a mission.

Usually, this is caused by the mod files not being downloaded.
Make sure you have run `/download_data` in the Archipelago tab before playing.
You should only have to run `/download_data` again to pick up bugfixes and updates.

Make sure that you are running an up-to-date version of the client.
Check the [MultiworldGG Releases Page](https://github.com/MultiworldGG/MultiworldGG/releases) to
look up what the latest version is.

If these things are in order, check the log file for issues (stored at `[MultiworldGG Directory]/logs/SC2Client_<date>.txt`).
If you can't figure out the log file, visit our [Discord's](https://discord.com/invite/8Z65BR2) tech-support channel 
for help. 
Please include a specific description of what's going wrong and attach your log file to your message.

### My keyboard shortcuts profile is not available when I play *StarCraft 2 Archipelago*.

For your keyboard shortcuts profile to work in MultiworldGG, you need to copy your shortcuts file from 
`Documents/StarCraft II/Accounts/######/Hotkeys` to `Documents/StarCraft II/Hotkeys`. 
If the folder doesn't exist, create it.

To enable StarCraft 2 AP/MWGG to use your profile, follow these steps:
1. Launch StarCraft 2 via the Battle.net application.
2. Change your hotkey profile to the standard mode and accept.
3. Select your custom profile and accept.

You will only need to do this once.

## Running in macOS

To run StarCraft 2 through MultiworldGG in macOS, you will need to run the client via source as seen here: 
[macOS Guide](/tutorial/Archipelago/mac/en). 
Note: to launch the client, you will need to run the command `python3 Starcraft2Client.py`.

## Running in Linux

To run StarCraft 2 through MultiworldGG in Linux, you will need to install the game using Wine, then run the Linux build
of the MultiworldGG client.

Make sure you have StarCraft 2 installed using Wine, and that you have followed the
[installation procedures](#how-do-i-install-this-randomizer?) to add the Archipelago maps to the correct location. 
You will not need to copy the `.dll` files. 
If you're having trouble installing or running StarCraft 2 on Linux, it is recommend to use the Lutris installer.

Copy the following into a .sh file, replacing the values of **WINE** and **SC2PATH** variables with the relevant
locations, as well as setting **PATH_TO_MultiworldGG** to the directory containing the AppImage if it is not in the same
folder as the script.

```sh
# Let the client know we're running SC2 in Wine
export SC2PF=WineLinux
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# FIXME Replace with path to the version of Wine used to run SC2
export WINE="/usr/bin/wine"

# FIXME Replace with path to StarCraft II install folder
export SC2PATH="/home/user/Games/starcraft-ii/drive_c/Program Files (x86)/StarCraft II/"

# FIXME Set to directory which contains MultiworldGG AppImage file
PATH_TO_MWGG=

# Gets the latest version of MWGG AppImage in PATH_TO_MWGG.
# If PATH_TO_MWGG is not set, this defaults to the directory containing
# this script file.
MWGG="$(ls ${PATH_TO_MWGG:-$(dirname $0)}/MultiworldGG_*.AppImage | sort -r | head -1)"

# Start the MWGG client
$MWGG Starcraft2Client
```

For Lutris installs, you can run `lutris -l` to get the numerical ID of your StarCraft II install, then run the command
below, replacing **${ID}** with the numerical ID.

    lutris lutris:rungameid/${ID} --output-script sc2.sh

This will get all of the relevant environment variables Lutris sets to run StarCraft 2 in a script, including the path
to the Wine binary that Lutris uses. 
You can then remove the line that runs the Battle.Net launcher and copy the code above into the existing script.
