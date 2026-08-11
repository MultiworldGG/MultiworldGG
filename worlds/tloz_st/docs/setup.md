# The Legend of Zelda: Spirit Tracks AP Setup Guide

## Required Software

* [MultiworldGG 0.7.100+](/tutorial/Archipelago/setup/en)
* [Bizhawk 2.10+](https://github.com/TASEmulators/BizHawk)
* Legally acquired Spirit Tracks EU rom *(Not revision 1)*. Apparently it only works in English
* If you want to use vanilla AP: [Latest tloz_st.apworld](https://github.com/DayKat/spirit-tracks/releases)

## Recommended Software

* [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases) (Includes a full map tracker, with auto-tabbing and entrance rando support. by @catzador and @carrotinator)
* [Itemtracker](https://github.com/carrotinator/spirit-tracks-poptracker-ap) for [Poptracker](https://github.com/black-sliver/PopTracker) (still work in progress. the branch [carrot_map_tweaks](https://github.com/carrotinator/spirit-tracks-poptracker-ap/tree/carrot-map-tweaks) is most up to date. by @zobeeplays and @carrotinator)

## Setup

1. If you want to use vanilla AP: Find your Archipelago directory, and put tloz_st.apworld in the 'custom_worlds' folder
2. Create a yaml settings file, and put it in the MultiworldGG directories 'players' folder. You can generate a template yaml with the MultiworldGG launcher.
3. Generate your game
4. Host the game, either locally or via the MultiworldGG web hosting service
5. Open the 'generic bizhawk client' in the MultiworldGG Launcher, and connect to the server.
6. Launch the vanilla game in bizhawk, and open the lua console. Add the 'connector_bizhawk_generic.lua' script that can be found in 'MultiworldGG\data\lua'. 
7. You are now ready to play! Start a new savefile and go! If playing with random start, make sure to connect before launching a new game.

## FAQ/Useful Info

### How do i best use a touchscreen on the pc?
There are a number of options that work:
- Using a drawing tablet, make sure to turn of windows ink in the tablet settings.
- Using steamlink to a touch device.
- Using [moonlight 3ds](https://github.com/zoeyjodon/moonlight-N3DS) or [moonlight wiiu](https://github.com/GaryOderNichts/moonlight-wiiu) to mirror to a modded 3ds/wiiu.
- Using a controller patch. [This one](https://github.com/StraDaMa/Legend-of-Zelda-Spirit-Tracks-D-Pad-Patch) probably works.
- Using the touchpad on a steam controller.
- Playing with a mouse. It's possible to get used to it.

### Custom Commands
There are some custom commands for the bizhawk client:
- /train: change the train speed for each gear, or change train properties like instant acceleration or enter stations without stopping.
- /carrot_asked: found a bug? type this command and post what it says in the discord.
- /goal: display your goal requirements and progres towards them.
- /count_entrances: counts how many randomized entrances have be discovered out of how many are in your seed.
- /warp_to_start: manual warp to start command.

### Can I warp to start?
You can warp to start by opening the collection screen and pressing the button to swap the screens, then entering any entrance or saving and quitting. 
There will be messages in the client letting you know it's working.
You can also warp to any previously visited station if enabled in the yaml, by opening the rail map and tapping the station you want to go to.

### Is there a map tracker?
Yes! Get [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases) and it will create full map tracker!

### What is included in hard/glitched logic?
Check the [Tricks and Skips guide](https://github.com/DayKat/spirit-tracks/blob/main/worlds/tloz_st/docs/tricks_and_skips.md)

### What is different from vanilla or has unintuitive requirements in vanilla?
- If playing with randomized passengers, NPCs let you pick them up for quests once you have either rail holding their destination station, or after having visited their destination station, depending on yaml settings.
- Some minigames open with vanilla requirements. Hyrule sword game opens with Snow Source, Goron target range opens after removing the first lava in Goron village and each level of Take ‘em all on unlocks with forest-ocean-sand sources. Unlocking a higher level also unlocks the lower ones. 
- Beedle spawns with Snow Source
- When playing with combined track items, anything unlocked by a source is unlocked by packs containing that source track.
- The arena at the top of desert temple 1f has two states, each with 2 locations. In vanilla it switches state after getting the sand rod chest. In rando it switches after getting both checks in the first state and reloading the room.
- Ferrus has slightly different behavior in different passenger rando settings. You can pick him up south of Blizzard Temple if you’ve already picked up Alfonzo or have the Alfonzo item, and you can pick him up in Fire Realm if you have access to the Marine Temple. If vanilla passengers, he will give you his final item south of Wooded Temple after taking him to Marine Temple, while if vanilla abstract or randomized that location unlocks after getting the Ferrus item.
- Certain intro locations are missing. These include the vanilla locations of Engineer Certificate, Hero’s Outfit, Sword and Cannon.
- The Tower of Spirits summit counts as its own section for tower shuffle, and the stamp stand location there can’t be excluded or removed along with other sections. 
- The blue warp through ToS 5 will always be open if ToS 5 is excluded, meaning you still need to fight Staven to check what’s on the other side.
- Progressive tears of light with tower shuffle use the vanilla entrances to determine the order. So the order is entrance 1, e2 (forest source), e3 (snow source), e4 (ocean source), e5 (fire source), exit staven, enter altar in summit. Even if the summit is randomized to be your first section, the progressive tears for the section within will be last in the order.

### Who made this?
- The project is built upon @[Carrotinator](https://github.com/carrotinator)'s [Phantom Hourglass AP](https://github.com/carrotinator/Archipelago) implementation, which in turn is built upon @Dinopony and @Ishigh's [Oracle of Seasons AP](https://github.com/Dinopony/ArchipelagoOoS).
- The Forest and Snow Realms were helmed by @[DayKat](https://github.com/DayKat), with technical support from @[1313e](https://github.com/1313e).
- The Ocean Realm was made by @TriforceDrummer.
- The rest of the game was helmed by @Carrotinator.
- @[Catzador](https://github.com/catzador) added data for the map tracker, and was a huge help bugtesting entrance randomizer.
- Additional help provided by @Nepecute.
- Huge thanks to the [Spirit Tracks Decomp](https://github.com/zeldaret/st) including @[Yanis](https://github.com/Yanis002), @[Aetias](https://github.com/AetiasHax) and @[suggestion073002](https://github.com/SammygoodTunes) for documenting useful data in the spreadsheet and for answering our questions when needed.
