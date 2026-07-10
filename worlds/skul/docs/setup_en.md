# Skul: The Hero Slayer Randomizer Setup Guide

## Required Software

- [Skul: The Hero Slayer on Steam](https://store.steampowered.com/app/1147560/Skul_The_Hero_Slayer/)
- For easy setup (recommended):
  - [r2modman](https://thunderstore.io/package/ebkr/r2modman/) OR [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager)
- For manual setup:
  - [BepInEx Skul](https://thunderstore.io/c/skul-the-hero-slayer/p/BepInEx/BepInExPack_Skul/)
  - [SkulAPMod](https://github.com/Jeffdev-Archipelago-Implementations/SkulAPMod/releases)

## Installation
Before starting the installation process, here's what you should know:
- It is strongly recommended to use a mod manager if you want a quicker and easier installation process, but if you don't like installing extra software and are comfortable moving files around, you can refer to the manual setup guide instead.

## Generating a game
Generating a multiworld game works like any other Multiworld. If you are on AP, you will download the apworld file and put it in your custom_worlds folder.
Then use the Options Creator to make a yaml and put it into your Players folder. Then click "Generate" on the launcher, and you will have a generated game!
**NOTE: YOU MUST HAVE MultiworldGG v0.7.200 or AP v0.6.7 TO GENERATE AND USE THE SKUL APWORLD!**

### Easy setup (mod manager)
1. Download [r2modman](https://thunderstore.io/package/ebkr/r2modman/) using the "Manual Download" button, then install it using the executable in the downloaded zip package (You can also use [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager) which works the same, but it requires [Overwolf](https://www.overwolf.com/))
2. Open the mod manager and select Skul: The Hero Slayer in the game selection screen.
3. Select the default profile or create a new one.
4. Open the `Online` tab on the left, then search for `SkulAPMod` and `BepInEx Skul`.
5. Expand `SkulAPMod` and click the `Download` button to install the latest version, and also do the same for `BepInEx Skul`.
6. Click `Start Modded` to open the game with the mods.

### Manual setup
1. Download the following mods using the `Manual Download` button:
    - [BepInEx Skul](https://thunderstore.io/c/skul-the-hero-slayer/p/BepInEx/BepInExPack_Skul/)
    - [SkulAPMod](https://github.com/Jeffdev-Archipelago-Implementations/SkulAPMod/releases)
2. Open your Skul: The Hero Slayer installation directory. On Steam, you can find it easily by right-clicking the game and clicking `Manage` > `Browse local files`.
3. Open the BepInEx pack zip file, then open the `BepInExPack` folder.
4. Drag all folders and files located inside the `BepInExPack` folder and drop them in your Skul: The Hero Slayer directory.
5. Open the `BepInEx` folder in your Skul: The Hero Slayer directory.
6. Open the `SkulAPMod` zip file.
7. Drag and drop the `plugins` folder in the `BepInEx` folder to fuse with the existing `plugins` folder.
8. Open the game normally to play with mods (if BepInEx was installed correctly, a console should appear).

## Joining a new MultiWorld Game
1. After opening the game and selecting any button to open the game, you should see a window show up to type in your connection info and slot name and such.
2. Enter the address (typically multiworld.gg) and port, and then your slot name, and password (if you have one) then press the `Connect` button.
3. The game will inform you to restart the game. Do so, and click connect after going through the process again. (You will only need to do this once per connection)
4. After connecting again, you should enter the game and be ready to go!
 
## Troubleshooting
### The game opens normally, and no connection window appears
 - If there is a console, this means the mods loaded but the SkulAP mod wasn't found or had errors while loading.
   - Look in the console and make sure you can find a message about the SkulAP mod being loaded.
   - If you see any red text, there was an error. Report the issue in the [Archipelago Discord Server](https://discord.gg/8Z65BR2), by going to [the Skul: The Hero Slayer thread](https://discord.com/channels/731205301247803413/1346144590536904734) and pinging Jeffdev.

### I'm getting a different issue.
You can ask for help in the [Archipelago Discord Server](https://discord.gg/8Z65BR2), by going to [the Skul: The Hero Slayer thread](https://discord.com/channels/731205301247803413/1346144590536904734).
