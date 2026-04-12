# Pokémon Mystery Dungeon: Explorers of Sky

## Where is the options page?

You can read through all the options and generate a YAML [here](../player-options).

## What does randomization do to this game?

The Explorers of Sky Randomizer randomizes all dungeon unlocks and end game goals, as well as quite a bit more. Here's a 
breakdown of what the checks and locations look like:  
Checks: Dungeon Completion, Mission/Outlaw completions per dungeon, spinda drinks and drink events, legendary recruits, 
a few shop items, ranks, and donating to the bank among other smaller things.  
[Full List of Locations](https://github.com/CrypticMonkey33/ArchipelagoExplorersOfSky/blob/main/worlds/pmd_eos/Locations.py)  
[SubX checks not included in location list](https://github.com/CrypticMonkey33/ArchipelagoExplorersOfSky/blob/main/worlds/pmd_eos/RomTypeDefinitions.py)

Items: Dungeon Unlocks, Relic Fragment Shards (Macguffins), Special Episode unlocks, Dojo unlocks, Legendaries added to 
Chimeco assembly, instruments (macguffins), with the addition of a lot of filler items that can be items normally retrieved
 from the main game.  
[Full List of Items](https://github.com/CrypticMonkey33/ArchipelagoExplorersOfSky/blob/main/worlds/pmd_eos/Items.py)

There are two main goals, either beating Dialga (default) or beating Darkrai. Based on which goal you choose, the checks 
and item lists are configured down to be manageable.

There is a lot of QoL added to the game configurable in the yaml, such as IQ and XP scaling, level scaling, and starter 
options 

## How would I dump this game from my console to play it with AP?

Here are a couple guides you can use to get a legal dump of your EU Pokemon Mystery Dungeon: Explorers of Sky  
[Getting your 3DS set up](https://3ds.hacks.guide/)  
[Dumping your EOS Catridge](https://wiki.hacks.guide/wiki/3DS:Dump_titles_and_game_cartridges)

## Why is this game the EU version only?

EU is the objectively superior version of the game. It features support for other languages 
(Spanish, French, German, and Italian), and some bugfixes not present in the NA version (such as fixing the 10 letter 
name evolution softlock).

## Will there be NA support in the future?

Maybe. One of our devs has [drafted out plans](https://discord.com/channels/731205301247803413/1175911373822242946/1343011021895241810)
 on how to port our modifications to an NA ROM with a Python script in our [c-of-time](https://github.com/Chesyon/eos-archipelago-patches) repo,
but it's a long process. 
For now, it's not at the top of our priority list given the difficulty of the task. 
If you feel up to the task, any help would be appreciated!

## I found a bug, where do I report it?

Create an issue on the [pmd_eos Github](https://github.com/CrypticMonkey33/ArchipelagoExplorersOfSky/issues).
We will review it and try to fix it for a future version
  
## Is there a tracker for this game?

Yes, two actually! There is a poptracker developed by ScarredSceptile which you can find at 
[EOS Poptracker](https://github.com/ScarredSceptile/pmd_eos-AP-poptracker/releases/tag/v0.2.0-rc1).  
There is also an in game tracker that you can find in your menus! You can also set your top screen to always display the 
tracker through Other→Options→Top Screen

## How do I unlock Hidden Land and get to Temporal Tower?

In order to access Temporal Tower, you have to have Hidden Land which can be access from Lapras on the beach once you have enough 
Relic Fragment Shards. You will also need the item "Temporal Tower." Once you have cleared Hidden Land for the first time, Lapras will 
take you straight to Temporal Tower if you want.  

## There are some instruments in the game that I don't recognize!

Yeah! We created some new instruments to create a good count for Macguffins to open Dark Crater in Darkrai Goal. All of them 
are the same as the other instruments, but for their specific typing. The only exceptions are Null Bagpipes, Stellar Symphony, 
and Glimmer Harp.  
* Glimmer Harp - Increase the chance to recruit mono-type pokemon
* Stellar Symphony - Increases the chance to recruit dual-type pokemon
* Null Bagpipes - Decreases the chance to spawn pokemon in the dungeon

## How do I skip cutscenes?

You can press Select during a cutscene to skip the cutscene

## Is there any way to generate quests for a specific area?

Yes! Go talk to Diglett in the Guild, he will let you generate quests for specific dungeons.

## I lost my save game! How do I make sure this doesn't happen again?

In some versions of Bizhawk, there is an option that tries to save the game, but fails. You can turn this options off by
going to Config→Customize, switching to the advanced tab and turning off AutoSaveRAM. Another way to ensure that Bizhawk 
saves properly is by saving the game like normal (at a bed) and then going to File->Save Ram->Flush Save Ram or pressing 
Control+S

## Oh no I got unowned! How do I get rid of it?

For any trap that effects your game for a long span of time, it will go away once you rest. Sentry Duty, however, will
 not go away until the guildmaster is satisfied with your progress.

## I'm getting a message saying "You feel as if you are being watched by a powerful being." What does that mean?

That message tells you that a legendary is waiting for you to recruit them, but they will only be able to be recruited after Dialga
 is defeated. Just a little flavor we added in.

## My first quiz question is a bunch of gibberish! Is my game broken??

Nope, we changed the first question to be silly if you know how to decode it! Don't worry about it, just choose whichever 
option sounds best to you!

## How do I unlock the Main Game if I have Special Episode sanity on?

There will be an item called Main Game Unlock that you will get from one of the special episode checks that will unlock the main game.

## What is the difference between Drink Checks and Drink Events?

Drink Checks are earned whenever you get Spinda to give you a drink.  
Drink Events are earned whenever something good, bad, or unexpected happens as part of getting the drink. This includes 
drink upgrades, having someone want to be part of your team, etc.

## I got a hint in game from a dimensional scream, but missed it. Can I play the hint again?

Yes! Go talk to Torkoal in Hot Springs. Any hint that you have already claimed he can replay for you.

## My hint looks a little funny

Yeah, EOS has poor automatic line-breaking so if your hint is excessively long, it might make the the formatting look a little 
weird. You should be able to see it just fine in the Archipelago Client and Server though!

## I see a dungeon that looks close to the correct dungeon name, but not quite. What is that?

That is one of our traps! There are lookalike dungeons (similar to lookalike items) that are silly gimmick dungeons that don't actually give you anything (and thus are traps)

## My partner got removed from the party and I can't add them back!

Talk to your partner in the overworld (press R), and select "Add To Team". This will force them back onto the team!
