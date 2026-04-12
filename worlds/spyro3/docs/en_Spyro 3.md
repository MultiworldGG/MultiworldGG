# Spyro: Year of the Dragon (Spyro 3)

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## Which version of the game is supported?

This is a MultiworldGG implementation of the PlayStation 1 version of Spyro: Year of the Dragon (2000), **not**
the Reignited Trilogy version (2018).  This randomizer requires use of either
NTSC-U (North America, as opposed to the PAL/European) version, due to differences in the internal workings of the game.

## What does randomization do to this game?

When the player completes a task (such as collecting an egg), an item is sent. Collecting an egg may not increment the player's egg counter,
while a check received from another game may do so.

This does not randomize the location of eggs or gems, shuffle entrances, or make large-scale cosmetic changes to the game.
While previous versions of this MultiworldGG implementation were compatible with the standalone Spyro 3 randomizer,
support has been removed based on community feedback and developer time constraints.

When open world mode is disabled, the underlying game logic is unchanged.  For instance, accessing the balloon to Buzz in Sunrise Spring requires
helping all 5 NPCs in this world, whether or not they give an egg for the assistance.  The HUD's egg count
shows how many egg items you have received, while the in game Atlas shows which checks you have completed.

Open World mode gives access to all 4 homeworlds immediately, removing some eggs from the game.

It is possible to change the access restrictions for normal levels, as well.

## What items and locations get shuffled?
Eggs are always shuffled.  Based on the player's options, skill points, life bottles, individual gems,
and milestones for reaching certain numbers of gems per level or overall may also release checks.

The item pool will contain 150 eggs, unless the goal is Egg Hunt.
Depending on the player's options, companion unlocks or all Moneybags unlocks may
be shuffled into the pool, rather than having the player pay Moneybags.  Leftover items will be "filler", based on the player's
options.  Examples include giving extra lives, temporary invincibility, changing Spyro's color, or making the player Sparxless.

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world.

## What does another world's item look like in Spyro 3?

The visuals of the game are unchanged by the MultiworldGG randomization. The Spyro 3 MultiworldGG Client
will display the obtained item and to whom it belongs.

## When the player receives an item, what happens?

The player's game and HUD will update accordingly, provided that they are in their save file.  Some effects,
such as healing Sparx, may operate with a delay to avoid unintended interactions in game.

Receiving a Moneybags unlock while not in the same zone as him will complete the unlock automatically.
Doing so while in the same zone as him will require you to speak with him (or leave the zone) to finalize
the unlock.  Unlocks completed in this way cost 0 gems.

If for any reason the player is not in their save file when items come in, there may be a temporary desync.
Egg count will update the next time the player completes a check or receives an item.  Missed Moneybags
unlocks require the `clearSpyroGameState` command to be entered into the client.

## Unique Local Commands

The following command (without a slash or exclamation point) is available when using the S3AP client to play with MultiworldGG.

- `clearSpyroGameState` Resync your save file's received items with the server.  This may result in duplicate filler items.
If playing on a new save file, you will still need to get to the end of each level and defeat the bosses to progress in the game.
- `useQuietHints` Suppresses hints for found locations to make the client easier to read. On by default.
- `useVerboseHints` Include found locations in hint lists. Due to MWGG/AP Server limitations, only applies to hints requested after this change.
- `showGoal` Show what your completion goal is.

## Are There Any Bugs?

The following are known issues that can impact your gameplay.

- Leaving the client and game open for extended periods of time may result in errors.
- Receiving invincibility in a time attack stops the timer and doesn't automatically complete until invincibility runs out, you give up (which counts as victory), or crash (counts as victory)
