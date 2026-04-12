# Pseudoregalia Archipelago Setup Guide


## Required Software

* [Pseudoregalia game on Steam](https://store.steampowered.com/app/2365810/Pseudoregalia/)
* [Pseudoregalia Archipelago mod](https://github.com/pseudoregalia-modding/pseudoregalia-archipelago/releases/latest)
  (the `pseudoregalia-archipelago.zip` file)


## Optional Software

* [Pseudoregalia PopTracker pack](https://github.com/highrow623/pseudoregalia_brooty/releases/latest) for
  [PopTracker](https://github.com/black-sliver/PopTracker/releases)
* Not needed with MWGG: [Pseudoregalia apworld](https://github.com/pseudoregalia-modding/pseudoregalia-archipelago/releases/latest)
  (the `pseudoregalia.apworld` file)
  for local generation with the [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest) software.
  Refer to the Archipelago setup guide for more information, in particular the "Playing with custom worlds" section.


## Mod Installation

Before installing:

* If you want to play on full gold instead of map patch,
  read the [Playing on Full Gold](#playing-on-full-gold) section below.
* If you already have any other mods installed,
  read the [Compatibility with Other Mods](#compatibility-with-other-mods) section below.
* If you are playing on Steam Deck or Linux, use the next section instead.

After installing, you can configure your client using the [client settings](#client-customization).

Installation steps:

1. Make a copy of the Pseudoregalia game folder:
    1. Right click the game in Steam, then go to Manage and click Browse local files.
    2. This will put you *into* the Pseudoregalia folder.
       Don't be confused by the lowercase "p" pseudoregalia folder!
       Go up one level in your file explorer in order to copy the capital "P" Pseudoregalia folder.
    3. Rename the copied folder to Pseudoregalia_AP or whatever else you like.
       This guide will refer to the copied folder as Pseudoregalia_AP from here on.
2. [Optional] Add the executable from Pseudoregalia_AP to Steam as a non-Steam game
   (this will allow you to still use Steam input for controller compatibility,
   which is required for some controllers):
    1. Click Add a Game in the bottom left of Steam, then Add a Non-Steam Game.
    2. Click Browse, then navigate to `pseudoregalia.exe` inside Pseudoregalia_AP and click Open.
    3. Click Add Selected Programs.
3. Extract `pseudoregalia-archipelago.zip` directly into Pseudoregalia_AP. Either:
    * Move the zip into Pseudoregalia_AP, right click the zip and choose Extract Here.
      The zip can be removed afterwards.
    * Right click the zip and choose Extract files, then navigate to and select Pseudoregalia_AP, then click OK.

The mod is now installed! To connect to a multiworld slot, create a new file in the modded main menu,
enter your connect information and click Start.


## Installing on Steam Deck/Linux

These steps are specifically for Steam Deck, though since it runs on Linux,
they should mostly work as-is if you are just on Linux.
Just ignore anything that is Steam Deck specific or that doesn't apply to you.

1. In Game Mode, ensure you have opened the base game at least once. Close it, then go to Desktop Mode.
2. In Steam/steamapps/common,
   make a copy of your Pseudoregalia folder and rename it Pseudoregalia_AP or whatever else you like.
   This guide will refer to the copied folder as Pseudoregalia_AP from here on.
3. Extract `pseudoregalia-archipelago.zip` directly into Pseudoregalia_AP.
   You should notice no change to the root folder, but the mod files will be added to the subfolders.
4. Open the Steam Client, Add a Non-Steam Game,
   then go to Pseudoregalia_AP folder and select `pseudoregalia.exe`.
5. Open Properties, then ensure that you check compatibility to Force Proton Experimental.
    * If Experimental doesn't work, try a different version (8.0-5 was verified to work)
6. Lastly, Pseudoregalia utilizes Visual C++ Runtime 2022.
   Download Protontricks if you have not already.
   This is located within Discovery.
   After launching Protontricks, select Non-Steam Shortcut: pseudoregalia.exe.
   Select the default wineprefix, install a Windows DLL or component, then scroll down and select vcrun2022.
   Wait and follow the prompts until it has installed twice.
   You can go through this process twice if you are unsure.
   When you scroll down to vcrun2022 again, it should already be checked. It has installed correctly.
7. Launch in Game Mode which should open Pseudoregalia. Select a new file.
8. Enter the connect info and select Start. You will need to edit your controls to include show keyboard.

Note: In order to use the in-game console once you've loaded into the game,
you'll also need to add `enter` to your controls.


## Playing on Full Gold

The full gold patch is a previous version of the game that is also supported by the randomizer.
The game was updated after release to add the map item and other significant changes,
but the randomizer supports the earlier version for people who prefer it.

To play on full gold, switch the Steam version of Pseudoregalia before following the installation steps:

1. Right click Pseudoregalia in Steam and select Properties.
2. Click Game Versions & Betas.
3. In the Private Versions box, enter `fullgoldjump` and click Check Code.
4. Click Opt into: fullgold.

You will then be able to switch back and forth between both versions in Steam.
If you want to be able to play both versions with the randomizer,
follow the installation steps for each version and make two separate folders,
e.g. Pseudoregalia_AP_MapPatch and Pseudoregalia_AP_FullGold.


## Compatibility with Other Mods

The Pseudoregalia Archipelago mod touches many parts of the game
in a way that may make it incompatible with other mods.
(This is part of the reason why the installation guide recommends installing into a new folder.)
Notably, it is **NOT** compatible with PseudoMenuMod because of the way they both modify the main menu.
However, it does seem to be compatible with the Attire UI Overhaul Mod (custom outfits).

If you want to use other mods with this one,
the safest thing to do is to install this mod first and add others one at a time, making sure they work as you go.
If you already have mods installed, you can get a "fresh install" by following these steps:

1. [Optional] Copy the Pseudoregalia folder to preserve the mods you already have installed.
2. Uninstall Pseudoregalia from Steam.
   This will remove all vanilla files from the Pseudoregalia folder and leave only modded files.
3. Delete the Pseudoregalia folder.
4. Reinstall Pseudoregalia.

This will result in the Pseudoregalia folder only having the vanilla game files.


## Client Customization

Client settings can be found here:
`Pseudoregalia_AP/pseudoregalia/Binaries/Win64/ue4ss/Mods/AP_Randomizer/settings.toml`.
The mod zip includes a file called `settings.tmpl.toml` in that location,
so you'll have to rename it by removing the `.tmpl` before any changes will take effect.
(The settings file is included as a template in releases
so that you don't overwrite your settings when installing updates.)

Client settings allow you to customize how certain things behave in the mod.
The death link option is also configured here.
The template file explains what each option does.

The settings file is only read when starting the executable,
so any changes you make require closing and reopening the game.
