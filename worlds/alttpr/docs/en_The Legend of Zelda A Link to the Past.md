# The Legend of Zelda: A Link to the Past (Door Randomizer)

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Items which the player would normally acquire throughout the game have been moved around. Logic remains, so the game is
always able to be completed, but because of the item shuffle the player may need to access certain areas before they
would in the vanilla game.

## Features

* Goal options: Crystals, Ganon, All Dungeons, Pedestal, Triforce Hunt, Ganon Hunt, Trinity (complete any one of Ganon/Pedestal/Triforce Hunt goals), Completionist (collect every check and then kill Ganon),
* Standard and Inverted game modes,
* Set the number of crystals required for GT/Ganon, and number of Triforce pieces,
* All varieties of keysanity, including key drop shuffle,
* Shopsanity
* Potsanity
* Enemy and boss shuffle, including logical enemy shuffle where enemies which require specific items to kill can block progression
* Enemy Drop Shuffle
* Crossed entrance shuffle
* Option for Zelgawoods to add two Skull Woods dropdowns into the entrance shuffle pool. [Example](https://raw.githubusercontent.com/aurabot24/Archipelago-ALttPR/refs/heads/alttpr/worlds/alttpr/docs/Zelgawoods.png)
* Option to add Pendants and Crystals to the item pool
* Randomize flute spots and/or automatically activate the Flute upon pickup
* Options for Pseudoboots (dash from the start, but without any of the progression from Pegasus Boots) and Mirror Scroll (Y item that warps Link to the start of the current dungeon),
* FastROM to significantly reduce in-game lag,
* AP items are visually distinct: progressive items appear as green clocks, useful items as blue clocks, and filler/trap items as red clocks,
* Can be generated without a ROM file
 
## Known Bugs:

* Rare generation failures, especially with prize shuffle + crossed entrances (~7% failure rate)
* Some checks aren't sent until you leave their room,
* Triforce Pieces and Small Keys can't be in the starting inventory,
* The spoiler log shows a lot of events that should be hidden
