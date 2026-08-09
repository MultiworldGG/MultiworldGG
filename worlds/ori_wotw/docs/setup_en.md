# Setup Guide for Ori and the Will of the Wisps for MultiworldGG

## Disclaimer


The implementation is in a beta state (although stable). Most features are there, but some bugs remain (see the known issues section below).
## Source code (you don't need this if you just want to play)

[AP World](https://github.com/Satisha10/Archipelago_wotw/tree/main/worlds/ori_wotw) (Also available as a submodule in this repo, pinned to the latest release) (installed with MultiworldGG)
[Client code](https://github.com/ori-community/wotw-rando-client/tree/main/projects/Randomizer/archipelago)

## Setup guide

### AP World (only needed with AP)

Download the AP world from [this repository](https://github.com/Satisha10/APwotw_release/releases/latest) and install it by double-clicking it (make sure to restart the Archipelago launcher before generating). There are some `.yaml` templates in the `Yaml template` folder for different logic difficulties (Moki being the easiest, Kii the hardest). You can also generate a template or use the option creator in the AP launcher.

### Client installation

- Download the [standalone WotW randomizer](https://wotw.orirando.com/).
- Make sure that you are on a version above 4.31.0. (and above 4.44.0 for the latest AP World)
- The randomizer can be detected as a malware by some antiviruses. If you use Windows Defender, you can add an exception in `Settings -> System`, otherwise you have to manually add an exception for the `Injector.exe` file, which is located in the randomizer directory (the launcher has a button to open it).

### Connecting to the MultiworldGG game

In the Ori randomizer launcher, click on the three dots next to settings, then `Play Archipelago`. Enter the connection information, and launch the game. If successful, a message will be displayed when opening a save file.
Remark: when connection to a game hosted on `multiworld.gg`, make sure to enable secure connection. Disable it if you connect to `localhost` or an IP address.

## Important remarks and troubleshoot

- If the game launches as vanilla (for example there is no text on the right when a save file is selected), it likely means that you antivirus blocked the injector. Refer to the `Client installation` section.
- There is a [wiki](https://wiki.orirando.com/) for the randomizer if you want more information about it or to learn some tricks/glitches.
- The slot is considered goaled when defeating Shriek (the final boss). The goal(s) that you mention on the `yaml` only prevent you from entering the fight before you finish them.
- The randomizer has a tracker that you can start from the launcher, as well as a logic filter for the map, that shows the all the locations and highlights the ones that are in logic. Alternatively, yaml-less UT is supported.
- There are some AP related actions accessible from the randomizer wheel. Hold **V** to open it.

## Feedback

You can report issues or give suggestions in the Archipelago Discord server (in the corresponding discussion of [`future-game-design`](https://discordapp.com/channels/731205301247803413/1272952565843103765) ). I will also see it if you send it in the Ori Runs or the Ori Rando Dev Server.

## Known issues

- Seed generation might fail with non-vanilla spawns if there are not many games to fill the early spheres (this is currently getting worked on). Generation is stable otherwise.
- Released locations count for the goals (except wisps).
