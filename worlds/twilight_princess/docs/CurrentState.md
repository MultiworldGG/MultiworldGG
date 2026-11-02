# Current state of the World

Here is a file that lays out the basics for the current state of the randomizer

## Settings

All settings are functional in generation.

Note:
Known generation errors when dungeon rewards are set to `vanilla`, a solution has not been found in attempts to diagonse the bug with no success.
If you are able to diagnose the bug please let me know.

## Client

Each generation requires a custom seed. Each seed has an associated name, the client checks the seed name when connecting to ensure that the correct seed is loaded.
The client has a validation check every 10s. Interval can be changed with `/validation_time {number of seconds between validation}` The validation checks that you have the correct amount of important items. In the off chance that you do get the item when it is sent out the validation will ensure that you get it.

## Locations

The location settings will label locations as excluded which will means that they will prevent progession and usefull items from being placed at that location.
\*In some cases this will place the items in their vanilla location

With there being 575 locations in the game there may be mistakes in the data. If you notice a location not triggering correctly please leave a comment on the [Issue thread for it](https://github.com/WritingHusky/Twilight_Princess_apworld/issues/2)

## Generation

When generating the world, all possible locations will be created and given an item. Logic is based off the world data from the base randomizer web generator.
To easy the burden that shuffling keys creates, Pre-fill actions are taken to shuffle them locally if chosen by the settings. Locations chosen to have their vanilla items are also handled within the Pre-fill.

Overworld locations currently must always be shuffled. Later, after more logic, the setting will be fixed to work.

## Dungeons

Dungeon Items: Small keys, Big keys, Maps and Compasses, can be shuffled into the world according to some settings. See the Yaml for info about the settings.
\*Some settings will alter the way these items are shuffled, more info in setting description.

Due to the nature of Archipelago, "Unrequired" dungeons being empty is not implemented because there is no clear what makes a dungeon required when dungeon rewards are not vanilla (which has its own problems).

# Message

Thank you all for spending the time to enjoy this. I would also like to thank every one who has been reporting things for me to fix.

If you could star this repo that would mean a lot to me, I like numbers to go up.

If you feel something is wrong with this file let me know so I can fix it. If it is wrong here then its is highly likely that I don't know about it.
