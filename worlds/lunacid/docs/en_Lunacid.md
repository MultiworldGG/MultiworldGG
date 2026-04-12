# Lunacid

## Where is the settings page?
The [player settings page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?
The game's randomization changes the base game by
- removing the initial barrier at the start of the game,
- shuffling starting class and weapon,
- allowing shuffling entrances,
- choosing whether to lock doors or switches unless an item is obtained, 
- selecting which ending is necessary for victory,
- determining how many Strange Coins are required to complete Ending B,
- giving yourself more experience gain rates,
- giving the Dusty Crystal Orb a purpose by potentially locking hidden walls,
- allows custom music to be injected into the game,

among other settings.  Some of these settings are in the YAML, others in the in-game options
when you are in-game (not at the menu).  If its an option that would not impact logic, 
chances are its an in-game option.

## What items and locations get shuffled?
The base settings shuffle:
- all normal item pickup locations scattered around the world,
- the strange coin locations,
- gifts given to the player by Demi and Clive,
- the spells given to you by Daedalus,

With additional settings:
- shuffle all drops enemies drop,
- removing either Tower of Abyss or Coin locations from your game,
- shuffle results from quenching
- shuffle results from alchemy
- shuffle enemy placement.

with more planned as time moves on. 

Items shuffled depend on your settings, but can include:
- weapons,
- spells,
- key items (Vampiric Symbols, Terminus Prison Key, etc),
- voucher items that reduce the cost of items to 0,
- crafted goods (Health Vials, Bombs, Throwing Knives),
- rare drops (Angelic Feather, Pink Shrimp),
- custom quality-of-life items (experience, additional drop chances).

Additional "for fun" items and traps are made, such as
- Weight of the Dream, a "nothing" item that can increase difficulty,
- [Character Name]'s Gift for a Stranger, a gifting option, documented below,
- Rat Gang, which summons 5 rats who sing a song and follow you,
- Date with Death Trap, which sends you to an unused map with a chance to meet death (and die!).


## When the player receives an item, what happens?
When the player receives an item, the game will wait until it seems acceptable to give
and item to the player.  Then, it will be displayed on the client.  The item's
name is colored to help determine its progression value.

## How does the Gifting system work in Lunacid?
This is a setting that currently works in more automated way, via dropsanity and items.  
For dropsanity, if the following conditions are met, you are allowed to continuously
farm Archipelago/MWGG items:
- The other game has opted into the gifting system (up to developer to add it).
- If the game is not Stardew Valley, the item must not be progression.
- If the game is Stardew Valley, it has to be a basic "Object" from that game (not
furniture, weapons, hats, and so on).
- The initial drop was already found.

When this occurs, the drop item name will be colored olive green, and it will say the
item is gifted.

Two items can also be added to the multiworld, which attempt to gift a random item
to a player (if there is no other player like this the item does nothing):
- Demi's Gift for a Stranger
- Patchouli's Gift for a Stranger

The second always gives a random *trap*, not just a random gift.

## How does Ringlink work in this game?
Silver is attached to the ringlink system.  Gaining or losing silver sends a packet,
similar to any other game's ringlink system.  This can be amusing to include if ringlink is
being used in the multiworld and you don't mind being jumpscared by mimics.


## Known quirks
- Sometimes when being sent key items to open doors, they might not work if you 
are still in the same area.  A reload should fix this.
- When connecting, the slot name is case-sensitive; the font used by the game 
obscures this as it is always in upper case.
- If the game does not get past a connection attempt, it's likely that the server has winded down,
or there is a version mismatch.  Check the LogOutput of BepInEx if you aren't sure.
- If the game's port changes, this can be changed in-game at the title screen's option menu.