# Lego Star Wars: The Complete Saga

This MultiworldGG randomizer implementation is playable, but is a work in progress. This notice will be removed once the
logic has been rewritten from scratch, into a format that is more suitable for MultiworldGG.

## What does randomization do to this game?

Story mode is skipped for Chapters within an Episode, which should always be played in Free Play.

To unlock a Chapter, typically, Story Mode characters for that Chapter must be acquired, but this can be changed in the
options to other characters or 'Chapter Unlock' items instead. Optionally, an Episode Unlock item must also be acquired.

The player always starts with the items required to enter and complete their starting Chapter.

## What items and locations get randomized?

### Items
Characters, Extras and Minikits are in the item pool.

Score Multiplier Extras are replaced with Progressive Score Multiplier items that unlock more Score Multiplier Extras
the more Progressive Score Multipliers are acquired.

Stud and Power Up items are added to the item pool to fill out the rest of the item pool.

### Locations

Making purchases from the Characters or Extras shop are locations to check.

Completing an Episode Chapter in Free Play is a location to check. Additional checks can be sent for each Story mode
character that would have been unlocked if the Chapter had been completed in Story mode.

Completing the True Jedi for a Chapter can be a location to check.

Every 1-10 number of Minikits collected in a Chapter can be a check.

Completing Bonus levels and watching the Indiana Jones trailer can be locations to check. Additional checks can be sent
for each Story mode character that would have been unlocked if the Bonus had been completed in vanilla.

Riding unique creatures/turrets/vehicles can be locations to check.

## What other changes are made to the game?

Purchases in the Characters shop and Extras shop will not award their vanilla Characters/Extras and will display the
name and classification of the item that is at that shop slot.

Slots in the Characters shop that would normally unlock upon completing Story mode in every Chapter have been changed to
either unlock once all enabled Episodes are unlocked, or once 6 'Episode Completion Token' items have been received.
The unlock condition is controlled by an option in the game yaml.

## What does another world's item look like in Lego Star Wars: The Complete Saga?

All items display as they would in vanilla. The names of items in the Characters shop and Extras shop show the
Archipelago item that will be sent when making the purchase.

## When the player receives an item, what happens?

The item is immediately added to your unlocked Extras/Characters/Stud count. A text display in-game may show what the
received item was.

Studs are added to your in-level studs if you are a Chapter in Free Play, otherwise the studs are added directly to your
save file's total accumulated Studs. The received studs are multiplied by your maximum possible score multiplier and
multiplied by a further 2x for characters with a Power Up active (double score zones do not affect received studs
currently).

Power Ups automatically activate while in a level where Power Ups are relevant. Additional Power Ups will queue up and
activate automatically just before your current Power Up runs out, but all queued Power Ups will be lost once the
current game session ends.

## Can I play offline?

No, a connection to the MultiworldGG server is required to receive items, even in a single-player multiworld.

If the connection to the MultiworldGG server is lost temporarily, it is possible to continue playing. Most checked
locations while disconnected will be sent once the connection is reestablished. Some location types that are sent by
performing actions that do not get recorded into save data require a connection to the MultiworldGG server while
performing that action.

## Known Issues

### Logic

The logic is quite basic and may be overly restrictive (you can get a lot of checks out-of-logic). Work is ongoing to
rewrite the logic to fix issues and enable more randomization options, such as individual Minikit logic.

### Cantina Episode door lights

If you are in the main room of the Cantina when you unlock your first Chapter in an Episode, the red lights above the
Episode door won't change to green, but the door can still be entered normally. The lights will become green the next
time you enter the main room of the Cantina.

### Player 2 picking locked characters

When entering a Vehicle Chapter in Free Play with only one Vehicle Character unlocked, Player 2 can pick a locked
Character.

Locked characters should not be used until they are actually unlocked.

### In-game messages

Dying while a received item/checked location message is displayed will cause you to lose studs, but no studs will spawn
to be picked back up.

Collecting studs while an in-game message is displayed will play the sound for collecting Blue/Purple studs, but the
received value of the collected studs will be normal.

In some cases, the Double Score Zone background audio can start playing when in-game messages are displayed.

### 'All Episodes' Character unlocks

Because the AP randomizer changes the unlock condition for the slots in the Characters shop, that would normally unlock
upon completing Story mode in every Chapter, there may be a small delay before the purchase will be allowed, and other
slots in the shop may appear to be unlocked while making the purchase.

### Purchasing already unlocked Characters/Extras

When attempting to purchase a Character/Extra that has already been unlocked, by receiving that Character/Extra from
MultiworldGG, there may be a small delay before the purchase will be allowed because the client has to temporarily
disable that character to allow the purchase to go through.

### Studs

When in the Cantina, receiving a Stud item adds the studs directly to your save data, the stud counter shared by both
players that is only visible while in the Cantina.

Receiving a Stud while in a level will add it to your in-level stud count, contributing to True Jedi progress.

Receiving a Stud while under the effect of a Power Up will double the received studs.
However, receiving a Stud while in a Double Score Zone will not currently double the received studs.

## Credits

- maybejess: manual apworld reference
- Roushmore: manual apworld reference
- [Flit](https://flitpix.net): Linux setup guide