# Against the Storm for Archipelago Setup and Usage Guide

## Required Software
* Latest release of [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases). Currently tested/working on version 0.7.195.
* [Thunderstore Mod Manager](https://www.overwolf.com/app/thunderstore-thunderstore_mod_manager). (While a mod manager is not technically required, this guide will walk through using it to set up the mod)
* For any non-MWGG client: The `against_the_storm.apworld` from the latest [Against The Storm for Archipelago](https://github.com/RyanCirincione/ArchipelagoATS/releases) release.
* A legal copy of Against the Storm (tested as of v1.8.13, optionally including the Keepers of the Stone and Nightwatchers DLCs).
    * Only tested on Steam version.

## Installing the Archipelago Mod to Against the Storm using Thunderstore
1. Open the Thunderstore Mod Manager.
2. Search for the game Against the Storm and select it. (The first time I did while modding, the game didn't appear. Just closing and reopening Thunderstore worked for me)
3. Click Select Profile.
    - Optional: Create a new modding profile and name, if you don't want to use the Default
4. Click the Get Mods tab.
5. Find the Against The Storm for Archipelago mod, and download it.
* **Note:** ATS_API is a dependency of the mod. There have been some reports of the game getting stuck on the loading screen. If this happens, try manually downgrading the API to v3.5.0.

## **If you just want to play recipe shuffle without setting up MultiworldGG**
1. Just run the modded game through Thunderstore.
2. Before starting a settlement, open the dev console (\` by default), and use the `ap.randomizeRecipes` command.
3. The next settlement you start, check your Makeshift Post or Field Kitchen for shuffled recipes!

## Generating and Hosting a Seed
* If you are unfamiliar with MultiworldGG, I recommend reading through the [MultiworldGG Setup Guide](/tutorial/Archipelago/setup/en) to gain an understanding of how MultiworldGG works and to better understand the steps below. This is *not* the kind of randomizer you might be expecting!
1. For any non-MWGG client: Download the `against_the_storm.apworld` and `AgainstTheStorm.yaml` files from the latest [Against The Storm for Archipelago](https://github.com/RyanCirincione/ArchipelagoATS/releases) release.
2. For any non-MWGG client: Put the `against_the_storm.apworld` file in the `/MultiworldGG/lib/worlds` folder where you installed MultiworldGG.
3. Edit the `AgainstTheStorm.yaml`.
    1. Don't worry too much about the `name` if you're just trying this out on your own. The slot name would be more relevant if you are playing a MultiworldGG Multiworld.
    2. For the other options, read the comments and update them as you wish. The defaults should be fine if all these options are confusing.
    3. The one option you may want to pay attention to is `enable_dlc`, if you have Keepers of the Stone and want to include its locations, make sure to flip that to `true`!
4. Place the edited `AgainstTheStorm.yaml` in the `/MultiworldGG/Players` folder.
5. Run `MultiworldGGGenerate.exe` from the `/MultiworldGG` folder.
6. Upload the `AP_#######.zip` file from `/MultiworldGG/output` to [the MultiworldGG website](https://multiworld.gg/uploads) to host the game.

## Joining a MultiworldGG Game in Against The Storm
* Optional: backup your save files located in `%userprofile%\AppData\LocalLow\Eremite Games\Against the Storm`
1. Go to Thunderstore Mod Manager, open your Against the Storm profile with the Against the Storm for Archipelago mod, and click the blue Modded play button.
    * Optional: from the main menu, start a separate profile in the top right if you already have data in your default profile.
    * Optional: especially if you started a new profile from above, you will almost certainly want to run `meta.addAll` from the dev console, as the mod will assume you have all meta progression unlocked, and probably `goals.unlockAll` as well (these are the deeds, which have things like certain traders, decorations, and Big Shelter. **WARNING**: goals.unlockAll will grant you all the steam achievements unless you are on mod version v0.9.4 or later). The dev console is opened with \` (backtick, to the left of 1) by default, and at least for me only opens in the world map or settlements.
        * If you run `meta.addAll` on a fresh profile, the Training Expedition will still appear locked. This is an issue with the game's UI. Just enter and leave the Smoldering Citadel, and you should now see the Training Expedition available.
* Note: if you started a new profile, you will probably want to finish/skip the tutorial before proceeding.
2. From the world map, open the dev console (default \` (backtick, to the left of 1)) and type `ap.connect <url>:<port> "<slotName>" [password]`.
    * If you uploaded `AP_#######.zip` to MultiworldGG, then the room you generated should have the url: `multiworld.gg:#####`
    * slotName is the name from the `AgainstTheStorm.yaml`. The default was `ATSPlayer` if you didn't change it. The quotes are only necessary if the name you set has spaces.
    * password is only necessary if you added a password to your yaml.
3. In the game, start a settlement from the Training Expedition menu. (The mod should also work on any world settlements, you will just have more control over your game from the Training Expedition)
    * Note: several of the defaults in this menu have been adjusted by the mod for your convenience. You may want to override/further customize these settings and save them to a template in the top left.
        * *Column 1*
        * Don't forget to randomize your Seed each game! Or don't, I won't stop you.
        * Also don't forget to choose your Biome and Species, especially if you're looking to check certain locations in particular.
        * Feel free to choose any difficulty. The order locations only go up to slot #9, so you can still reach everything from Viceroy.
        * The mod overrides the default Reputation from 14 to 18, per half of Prestige 1.
        * The mod overrides the default Storm duration from 2 to 4 minutes, per Prestige 2.
        * The mod overrides the default Forest Mystery quantity to 1+/4- per Veteran+ difficulty.
        * The mod overrides the default blightrot footprint from 100% to 200%, per half of Prestige 11.
        * *Column 2*
        * The mod defaults the first 4 towns to be selected.
        * The mod defaults the embarkation goods to the following. This set is designed as a mix of the base embarkation package, and some extra basic resources:
            * 70 Wood
            * 28 Coal
            * 6 Wildfire Essence
            * 28 Parts
            * 14 Pipes
            * 42 Eggs
            * 28 Roots
            * 28 Vegetables
            * 28 Meat
            * 28 Mushrooms
            * 28 Insects
            * 28 Berries
            * 28 Fish
            * 7 Planks
            * 7 Fabric
            * 7 Bricks
        * *Column 3*
        * The mod shouldn't be harmed by any world/daily modifiers, so feel free to add them if you want to spice up your run.
        * Below the map modifiers is where you will find the Prestige modifiers, which should be in the order you get them from climbing Prestige. (Note the missing P2, P11, and half of P1 modifiers, which are represented by the variables explained above)
4. Click Embark.
