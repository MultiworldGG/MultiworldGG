# Portal 2 Setup Guide

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases/latest)
- [Portal 2 apworld](https://github.com/GlassToadstool/Archipelago/releases) (not needed with MultiworldGG)
- [Portal 2 Archipelago Mod](https://github.com/GlassToadstool/Portal2ArchipelagoMod)

## Installation

To use this mod you must first have a copy of Portal 2 downloaded in your Steam library.

1. Download and install [Steam](https://store.steampowered.com/about/), and download and install [Portal 2](https://store.steampowered.com/app/620/Portal_2/).
2. Download the [latest Zip archive release of the Portal 2 mod](https://github.com/GlassToadstool/Portal2ArchipelagoMod/releases)
3. Extract the top-level folder from the Zip file
4. Place the `Portal2Archipelago` folder in the `sourcemods` Steam folder.
    - On Windows, this may be found at:
        - `C:\Program Files (x86)\Steam\steamapps\sourcemods`
    - On Linux, this may be found at:
        - `~/.local/share/Steam/steamapps/sourcemods/`

The folder structure should look like this:

```
sourcemods
|   
└─── Portal2Archipelago
    |  GameInfo.txt
    |   ...
    └─── cfg
    └─── ...
```

5. Open Steam, and you should see a new game named "Portal 2 Archipelago Mod" in your game library.
> [!NOTE]
> If the game does not appear in your Steam game library, please exit (completely closing) Steam and re-launch Steam.
6. We need to change the properties of the game in order to connect to the MultiworldGG Portal 2 APWorld client. Right-click the "Portal 2 Archipelago Mod" game in your Library, and select the "Properties..." menu option.
7. In the dialog that appears, navigate to the "General" menu item, then in the right pane of the dialog navigate to "Launch Options". In the text input:
    - On Windows, put:
        - `-netconport 3000`
    - On Linux, put: 
        - `%command% -netconport 3000`
> [!TIP]
> If on Linux, and you cannot get the game to open as expected, you may need to run the game using Proton, following the Windows install steps.
8. Unless you use MWGG: Download and install the [`portal2.apworld`](https://github.com/GlassToadstool/Archipelago/releases/latest) file into the Archipelago launcher using the "Install APWorld" option

## Running
1. Open the "Portal 2 Client" from the MultiworldGG launcher
2. Input the multiworld server address into the "Server" field at the top of the new window and press connect
3. Input your slot name into the command field and press enter
4. When you join a game the client may ask you to select a file with a prompt
    - Simply locate the Portal2Archipelago mod location and find a file called `extras.txt` in the `scripts` folder and select that file. For Windows that may looks something like `C:/.../Steam/steamapps/sourcemods/Portal2Archipelago/scripts/extras.txt`
6. Launch the sourcemod (Portal 2 Archipelago Mod) from steam
7. From the game main menu select "Play Portal Archipelago"
