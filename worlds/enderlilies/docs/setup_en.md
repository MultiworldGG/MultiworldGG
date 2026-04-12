# Ender lilies Randomizer Setup Guide

This guide contains instructions on how to install and troubleshoot the Ender Lilies client, as well as where to obtain a config file for Ender Lilies.


## Required Software

- [The most recent MultiworldGG release](https://github.com/MultiworldGG/MultiworldGG/releases)
- [LiveSplit](https://livesplit.org/downloads/)
- [Ender lilies Randomizer](https://github.com/Trexounay/EnderLilies.Randomizer/releases)


## How do I install this randomizer?

1. Install MultiworldGG and LiveSplit using the first two links above. 
2. Extract EnderLilies.Randomizer.zip **in** the "Components" folder of your LiveSplit installation. 
3. To make the randomizer available in LiveSplit: right click on LiveSplit -> "Edit Layout" -> "( + )" -> "Control" -> "Randomizer Ender Lilies" -> "Ok"
4. To keep the randomizer available in LiveSplit, right click on LiveSplit -> "Save Layout"


## Where do I get a config file (aka "YAML") for this game?

The [Player Settings](/games/Ender%20Lilies/player-options) page on this website allows you to choose your personal settings for the randomizer and download them into a config file. 
Remember the name you type in the `Player Name` box; that's the "slot name" the client will ask you for when you attempt to connect!


### And why do I need a config file?

Config files tell MultiworldGG how you'd like your game to be randomized, even if you're only using default settings.
When you're setting up a multiworld, every world needs its own config file.
Check out [Creating a YAML](/tutorial/Archipelago/setup/en#creating-a-yaml) for more information.


## How do I join a MultiWorld game?

1. Launch LiveSplit.
2. Either load the layout where you included Ender Lilies randomizer or repeat line 3 of Installation.
3. "Edit Layout" -> Double click on "Randomizer Ender Lilies"
    - Ignore all other sub-tabs of "Ender Lilies Randomizer". 
    They are only relevant for the standalone randomizer and ignored when playing via MultiworldGG.  
4. In the "Archipelago" sub-tab, fill the Server/Port, Password (if any) and Slot name.
5. Click Connect. 
   A green message will indicate if it worked.  
6. Press "Launch Ender Lilies" to start!


## My controller is not working

If your controller is not detected by Ender Lilies, try launching the game via Steam (i.e., not with LiveSplit button).
However, do not forget that you need to be connected to LiveSplit before you load a save file. 


## Running in Linux

Note that neither Ender Lilies nor its randomizer are officially supported for Linux.
The following is a solution provided by a kind soul, use at your own risk.

- Download LiveSplit as requested.  
- Put it in the same folder as ENDER LILIES.
- Install the randomizer as outlined in Installation.
    - Using the "EnderLilies.Randomizer_splitted_dlls.zip" versions seems more stable on Linux.
- In the same folder as the ENDER LILIES executable is located, make a new document which will be a .bat script with the following lines:
    ```
    start EnderLilies.exe  
    start LiveSplit/LiveSplit.exe  
    exit
    ```
- Save it as a .bat file. (e.g., "EL_Rando_launcher.bat")
- In Steam, add a new program. Pick the bat file as the program.
- Under compatibility, force a Compatibility tool.
    - Tested with Proton Experimental.
- In theory, launching that game will launch both Ender Lilies and LiveSplit at the same time.


### Known issues
- LiveSplit freeze and then crash when the bat file is launched.
    - Try disconnecting the internet before launching the bat file. If LiveSplit does not freeze, you can reconnect the internet. 
- I get "The component could not be loaded" when adding Ender Lilies to the layout of LiveSplit.
    - Use the component with each dll separated.
- I get "Microsoft Visual C++ Runtime missing" when launching the bat file.
    - Currently, there is no clean/safe way to deal with this.
    - One user was able to make it work by doing the following:
        - **Note that doing this might corrupt the Compatibility tool used. Attempt at your own risk.**
        - Download the X86 and X64 versions of "Microsoft Visual C++ Redistributable latest supported downloads"
        - Create a steam "game" for each of them.
        - Force the same Compatibility tool as the bat file to the two "games". 
        - Launch both "games" via Steam. You will see an installation window for the libraries.
        - In the launch option of the batch file, add  `STEAM_COMPAT_DATA_PATH="PATH_OF_THE_FAKE_GAME1" STEAM_COMPAT_DATA_PATH="PATH_OF_THE_FAKE_GAME2  %command%"` in the launch option.
        - It should work from there.


## Tracker

A tracker is available via [Poptracker](https://github.com/black-sliver/PopTracker/releases). 
The data required for Ender lilies are available [here](https://github.com/lurch9229/ender-lilies-poptracker/releases).

