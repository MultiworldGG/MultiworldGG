# Outer Wilds

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What This Mod Changes

Randomizers in the Archipelago/MWGG sense—which are sometimes called "Metroidvania-style" or "progression-based" randomizers—rely on the base game having several progression-blocking items you must find in order to complete the game. In Outer Wilds progression is usually blocked by player knowledge, so to make a good randomizer we take away some of your starting equipment (Translator, Scout, Signalscope, etc), and turn much of that player knowledge into items (using warp platforms now requires a "Nomai Warp Codes" item, using the special GD tornado now requires a "Tornado Aerodynamic Adjustments" item, etc). These "items" are then placed at randomly selected "locations" while ensuring the game can still be completed. Most of the locations in this randomizer are revealing facts in the Ship Log, finding notes/recorders/fuel tanks left by other Hearthians, and scanning each signal source.

[As shown below](#in-game-ship-log-tracker), complete lists and descriptions of all the items and locations in the randomizer can be found in-game in the ship log. Or in randomizer terms: we added an "in-game tracker" to the ship log. We strongly recommend using this tracker on your first randomizer playthrough to learn what you're supposed to be doing.

## Tracker Support

### In-Game Ship Log Tracker

If you've never played the Outer Wilds Archipelago Randomizer before, this is the tracker you want to focus on. It comes "for free" with the randomizer mod, uses the familiar ship log interface, contains detailed descriptions of every single item and location, and even displays the randomizer's "logic" for which items you need to access each location.

<img src="readme_images/APChecklist.png" height="300">
<img src="readme_images/TimberHearthChecklist.png" height="300">
<img src="readme_images/APInventory.png" height="300">


### Universal Tracker

Compared to the In-Game Tracker, the main advantage of Universal Tracker is that it runs outside of and separate from Outer Wilds. This lets you place UT on another monitor while playing, or leave UT running all day in the background so you can quickly check if you're still "in BK mode" without launching Outer Wilds itself.

### Items-only PopTracker Pack

Finally, [there's a PopTracker pack for Outer Wilds items](https://github.com/magicdotexe/Outer-Wilds-PopTracker-Pack). If you're not familiar with PopTracker itself, [you can find it here](https://github.com/black-sliver/PopTracker).

<img src="readme_images/ItemsOnlyPoptrackerPack.png" height="300">

Again, this pack is just items. No locations, maps, or logic. But since PopTracker is also a separate program from OW itself, and Universal Tracker shows *locations*, you may find this useful too.

## Mod Compatibility

Outer Wilds story mods whose content has been fully integrated into this randomizer:

- [Astral Codec](https://outerwildsmods.com/mods/astralcodec/)
- [Echo Hike](https://outerwildsmods.com/mods/echohike/)
- [Forgotten Castaways](https://outerwildsmods.com/mods/forgottencastaways/)
- [Fret's Quest](https://outerwildsmods.com/mods/fretsquest/)
- [Hearth's Neighbor](https://outerwildsmods.com/mods/hearthsneighbor/)
- [Hearth's Neighbor 2: Magistarium](https://outerwildsmods.com/mods/hearthsneighbor2magistarium/)
- [The Outsider](https://outerwildsmods.com/mods/theoutsider/)

Outer Wilds quality of life/tooling/etc mods that this randomizer goes out of its way to support:

- Suit Log: All of the ship log's "in-game tracker" content is available in the Suit Log too.

Outer Wilds quality of life/tooling/etc mods that are known to work without issue:

- Clock
- Cheat and Debug Menu
- Unity Explorer
- Light Bramble (thanks Rever for testing this), although it makes the "Silent Running Mode" item pointless
- Time Saver (thanks Jade for testing this)

Outer Wilds mods that have been tried, but are known to have issues (this information might not be kept up to date, as I don't/can't test these myself):

- NomaiVR (thanks Snout for testing this): Mostly works. Trying to grab the Translator or Signalscope *before donning the suit* will softlock, but this is fine once you're in the suit. The in-game console does not work reliably, so using the AP Text Client instead is recommended.
- Quantum Space Buddies: Awkward but can *probably* be made to work. I believe you would have to use one of the "... Random Expedition" main menu buttons to connect to your AP server, immediately quit back to the main menu, then use either of QSB's main menu buttons to load the game with multiplayer. Please tell us if you can test this properly.

## Credits

- Direct feature contributions include:
	- aXu-AP: Echo Hike mod / Threader integration
	- GameWyrm: this mod's in-game console, early versions of the in-game tracker, the banner art image, and the "Quality of Life" mod settings
	- hanophora: Suit Log integration
	- magic.exe: the items-only PopTracker pack
	- msyverw: Forgotten Castaways integration
	- MYoshua64: Ice Physics, HUD Corruption, Map Disable, Suit Puncture and Supernova Trap items
	- RS-Mind: Forgotten Castaways integration and Randomize Stranger Codes mod setting
	- t-rbernard: Death Link Roulette mod settings
	- thestrangepie: `shuffle_spacesuit: true` / "suitless" logic
- dgarroDC, hopop201, ScipioWright and Zannick for smaller direct contributions (bug fixes, typo fixes, spoiler-proofing, etc)
- clubby789, dgarroDC, GameWyrm, glitchewski, JohnCorby, nebula, Trifid, viovayo, xen and others from the "Outer Wilds Modding" Discord server for help learning how to mod Unity games in general and Outer Wilds in particular, and creating the other OW mods that this randomizer relies on or is often played with
- Amada, Axxroy, DCBomB, Groot, Hopop, Onemario, qwint, Rever, Scipio, Snow, and others in the "Archipelago" Discord server for feedback, discussion and encouragement
- Nicopopxd for creating the Outer Wilds "Manual" for Archipelago
- Flitter for talking me into trying out Archipelago randomizers in the first place
- All the Archipelago contributors who made that great multi-randomizer system
- Everyone at Mobius who made this great game

No relation to [the OW story mod called "Archipelago"](https://outerwildsmods.com/mods/archipelago/)
