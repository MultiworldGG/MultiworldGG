# RimWorld for Archipelago Setup and Usage Guide

## Required Software
* Latest release of [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases).
* If you do not want to use MWGG: The `rimworld.apworld` from the latest [Archipelago RimWorld](https://github.com/PhantomOfAres/ArchipelagoRimworld/releases) release.
* The `Harmony` mod, which can be downloaded from the workshop [here](https://steamcommunity.com/workshop/filedetails/?id=2009463077)
* The `RimworldArchipelagoClient<version>.zip` mod file from the [Rimworld Archipelago Client](https://github.com/PhantomOfAres/RimworldArchipelagoClient)
    * Workshop support coming soon!
* A legal copy of RimWorld, on version 1.6 or later.
    * Only tested on Steam version.
    * All expansions up to Odyssey are currently supported.
    * Additional mods are not guaranteed to work, but if you're interested, see `Advanced Setup` at the end of this guide.

## Installing the Archipelago Mod to RimWorld
1. Navigate to the install folder for Rimworld (right-click RimWorld in Steam, click Properties -> Installed Files -> Browse)
2. Open the Mods folder
3. Extract the contents of `ArchipelagoRimworldClient.zip` into the Mods folder - there should now be a RimworldArchipelago folder alongside the "Place mods here.text" file in the Mods folder.
4. Open RimWorld
5. Click the "Mods" button from the main menu
6. Enable the Harmony mod, and the Archipelago mod. The Harmony mod must be at the top of the list, and the Archipelago mod should be below all of the base game files (Core, Royalty, Ideology, etc.) You can use the Auto-Sort button to resolve this order.

## Generating and Hosting a Seed
* If you are unfamiliar with MultiworldGG, I recommend reading through the [MultiworldGG Setup Guide](/tutorial/Archipelago/setup/en) to gain an understanding of how MultiworldGG works and to better understand the steps below.
1. Unless you want to use MWGG, download the `rimworld.apworld` and `yaml` files from the latest [Archipelago RimWorld](https://github.com/PhantomOfAres/ArchipelagoRimworld/releases) release. Note: There are multiple sample yaml files, depending on whether you own DLCs. Both can be edited as desired.
2. (Without MWGG:) Put the `rimworld.apworld` file in the `Archipelago/custom_worlds` directory.
3. Edit `Rimworld.yaml`
    1. Take a look at all of the options in the yaml file, and adjust them as desired. Take special note of the `expansion_enabled` settings if you don't own or would like to exclude certain expansions.
    2. The Rimworld randomizer allows for a lot of freedom of which types and how many of each location you will use. When editing this yaml and testing it, you will want to ensure that the number of locations matches the number of items in the game, which may change as you adjust various settings. If you have more locations than items, the generator will create filler for you, but if the inverse is true, you'll run into problems.
4. Place the edited `Rimworld.yaml` file into the `MultiworldGG/Players` folder.
5. Run the Generator (Run the `MultiworldGGLauncher.exe` file in `MultiworldGG`, and click "Generate")
6. Upload the `AP_#######.zip` file from `/MultiworldGG/output` to [the MultiworldGG website](https://multiworld.gg/uploads) to host the game.

## Joining an MultiworldGG Game in RimWorld
1. Open RimWorld after setting up the mod (see the `Installing the Archipelago Mod to RimWorld` section.)
2. You may notice the main menu removes the new game and load game buttons - this is normal! Click the "Connect to Archipelago" button
3. Fill in the host name (likely `multiworld.gg:#####`), slot name, and password (if you didn't set a password, leave this empty.)
4. Click Connect. The game may hang after doing this, this is normal, and the game should run normally once the hang is done. Please be patient.
5. Start a new game! If it's your first time connecting to this server, the main menu will prevent you from loading a game - this is mostly just a reminder that you should start a new game with every new server. Once you connect again during a later session, you can load normally from the main menu.

## Advanced Setup
**HERE BE DRAGONS** - This is untested and may not work even after putting effort into it. I'm happy to help folks on the Archipelago After Dark Discord if you run into trouble, but the answer may be that it's too hard to make work for a while.

This mod has been designed to attempt to support future expansions as well as mods. If mods don't mess with research, they should be simple enough to add alongside this mod. If you want to set up a multiworld that includes modded content, follow these steps:
1. Set up a client with all the mods that will be used **by all RimWorld players** in the multiworld you're targeting. (If player A is using Vanilla Genetics Expanded and player B is using Dub's Bad Hygiene, the person doing setup needs both to perform this setup.)
2. Open RimWorld, and DO NOT connect to a MultiworldGG server
3. Open Options -> Mod options -> Archipelago
4. Click the `Extract Ap Data` button. This wil export all of the game's data into a format that both the generator/server and the client can read. It will be saved in the user's Documents folder (note that modernly, there are two Documents folders, one connected to OneDrive, and one local - it's in the local one.)
5. Send the ArchipelagoItemDefs.xml file to all Rimworld players in this multiworld.
6. All players must put this ArchipelagoItemDefs.xml file in their mod folder (`Rimworld/Mods/RimworldArchipelago/Defs`) - it will overwrite the existing xml file.
7. Open the apworld file (it's a zip file - it can be opened with anything that can open a zip file.)
8. Replace the `ArchipelagoItemDefs.xml` in the apworld with the new xml file.
9. If multiple people in the same multiworld are using different sets of mods, each player must exclude the items from the other mods from their yamls. (Soon, there will be a way to do this directly. As a workaround, you should be able to exclude the locations and items from other mods - you'll have to go digging through `ArchipelagoItemDefs.xml` to find them - it should include the source mod for all items.)
10. Cross your fingers and generate as normal! If it all works and we ever meet in person, you now owe me a drink. Enjoy whatever madness you have cooked up. Also, and I hope nobody has to hear this, but just in case... research and item names will be visible to other players.
