# Setup Guide for Ori and the Blind Forest Archipelago

## Required Software
* Ori and the Blind Forest: Definitive Edition
* [BepInEx x86](https://github.com/BepInEx/BepInEx/releases)
* [OriBFArchipelago Plugin](https://github.com/c-ostic/Archipelago/releases)

## Initial Setup

### Set up BepInEx
* Navigate to the Ori and the Blind Forest files
  - This can be done through steam using `Manage -> Browse local files` in the game settings for Ori
* Move the contents of the BepInEx_x86_x.x.x.x (depending on version) folder into the Ori DE folder
* Run Ori and the Blind Forest once for BepInEx to set up additional folders
   - Note: the game will be stuck on a black screen, this is expected and you will have to close the game manually
* Navigate into BepInEx\config and open BepInEx.cfg
* Change `Type = Application` to `Type = Camera`
   - This option is the second to last option in the cfg
* Optionally, set `Enabled = true` under [Logging.Console]
   - This option enables a terminal window to see additional log messages

### Set up OriBFArchipelago
* Navigate to BepInEx\plugins
* Move the entire OriBFArchipelago folder into the plugins folder
* If you are updating the mod it may ask you to replace files. If so, click yes

## Join a Multiworld Game
1. Start Ori and the Blind Forest

2. Upon startup, you should see a set of text boxes in the upper left corner

3. If you enabled the console, you should also get a message there

4. Highlight the save profile you want to use

5. Fill out the server name, port, slot name, and (optional) password in the upper left text boxes

6. If you are having problems with the game's UI moving as you type, press the "Edit" button. 
This prevents all other input into the game. Press "Done" when complete.

7. Start the profile and begin playing!