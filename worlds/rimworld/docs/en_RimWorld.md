# RimWorld

## What does randomization do to this game?
The primary element that's randomized is research. All research that AP/MWGG knows about will be turned into items that grant the player with that technology. In order to get that research, the player must research special technology or craft items (and soon, more!)

## What RimWorld items are randomized?
There are several types of item in RimWorld:
* Research
    * Each research item will automatically grant that technology to the player
    * Research is also the primary progression in the game - you need certain tech to complete your victory condition, and crafting items will also require their requisite research.
* Boons (Coming soon...)
    * All of the fun helpful stuff people can send you!
    * Colonists
    * Item drops
    * Merchants
    * And more!
* Traps (Coming soon...)
    * All the fun bad stuff people can send you! 
    * Raids
    * Scaria
    * Weather Events
    * Off-map problem causers
    * And more!

## What do Locations look like in RimWorld?
Locations in RimWorld are all tasks to be accomplished. They come in several formats, and their counts can be configured in yaml.

* Research
    * The "Archipelago" research tab contains all the research checks for the player
    * Yaml-configurable numbers of research, which can be spread among the research table, hi-tech research bench, and multi-analyzer
    * Currently, all research is automatically hinted (coming soon: Yaml configuration)
* Crafting
    * The Archipelago Grinder is a new building in the Production tab. It will request pairs of items that the player can craft. Send the two requested items to the grinder, and it will send the location.
* Combat (Coming soon...)
    * Defeat raiders to obtain items that can be consumed to complete a location
    * Trophies for all of the different types of enemy in the game
* Quests (Coming soon...)
    * Quest rewards that send location checks, as alternate choices to the vanilla quest rewards
* Trade (Coming soon...)
    * Traveling traders and merchants at other settlements will sell items that can send locations


## What is the goal of this game when randomized?
The goal is configurable to be any of the vanilla win conditions in the game.
(Coming soon...) For shorter multiworlds, a new McGuffin collection win condition to help allow RimWorld to better integrate into shorter games. Also, an option to enable the last stand for the new win condition, or to disable/reduce it for the vanilla ones.
