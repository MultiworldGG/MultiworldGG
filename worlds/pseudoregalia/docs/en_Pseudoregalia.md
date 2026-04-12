# Pseudoregalia


## Links

* [Setup Guide](/tutorial/Pseudoregalia/setup/en)
* [Options Page](../player-options)
* [Advanced Options Page](../weighted-options)
* [Pseudoregalia PopTracker Pack](https://github.com/highrow623/pseudoregalia_brooty/releases/latest)
* [Pseudoregalia Archipelago Github Repo](https://github.com/pseudoregalia-modding/pseudoregalia-archipelago)


## Items

All items that can be found "out in the open" in the base game are added to the item pool.
These include:

* Abilities like Dream Breaker and Slide
* Aspects, the pickups that look like green orbs
* Health pieces
* Major keys
* Small keys

The follow options will swap some of these items out with replacements:

* Progressive Dream Breaker:
  swaps Dream Breaker, Strikebreak and Soul Cutter with three Progressive Dream Breaker items.
  This normalizes the order you get access to the swapped out items.
* Progressive Slide: swaps Slide and Solar Wind with two Progressive Slide items.
  This normalizes the order you get access to the swapped out items.
* Split Sun Greaves: swaps Sun Greaves and Heliacal Power with four Air Kick items.
  Each Air Kick acts like Heliacal Power, adding 1 kick.
* Split Cling Gem: swaps Cling Gem with three Cling Shard items.
  Each Cling Shard increases your cling limit by 2.
  (In the base game, you can only cling 6 times with Cling Gem before you touch the ground.)

The Randomize Time Trials option will also add the outfits to the item pool if turned on.
If turned off, the outfits are given to you at the start of the game instead.

Turning on certain options, such as Randomize Goats, will add filler items to balance the item pool.
These are the filler items used in balancing:

* Healing: restores one pip of health
* Magic Power: gives one level of magic

By default, none of your items are restricted to your world,
meaning any item can appear in anyone's world in the multiworld.


## Locations

Any location where a default item listed above is found in the base game can hold a multiworld item.

The Split Sun Greaves and Split Cling Gem options each replace one item with three.
Turning these options on adds two additional locations where you would normally find Sun Greaves/Cling Gem.

If Randomize Time Trials is turned on, each time trial also guards an item.
You have to beat the bronze time to make the item spawn.
It is recommended to have some familiarity with all the time trials before playing with this option.

The following options add additional locations:

* Randomize Goats: talk to the goatling to get the item.
  Some goatlings are in easy-to-miss spots, so these videos can help you find them:
  * [Castle Sansa - Trapped Goatling](https://youtu.be/1xmK5C8Jf_Q)
  * [Empty Bailey - Alley Goatling](https://youtu.be/680X5O4OSCs)
  * [Twilight Theatre - Murderous Goatling](https://youtu.be/rB24sE1l-Ak)
* Randomize Chairs: sit down to get the item
* Randomize Books: read the book to get the item
* Randomize Notes: read the note to get the item


## Goal

Just like in the base game, the goal is to collect all 5 major keys to open the Great Door and defeat the Princess.

If you are playing in a multiworld with other people,
you may want to set your major keys to be local so you aren't waiting for someone else to get your MacGuffins.
To make your major keys local, add the following to Local Items when configuring your options:

* Major Key - Empty Bailey
* Major Key - The Underbelly
* Major Key - Tower Remains
* Major Key - Sansa Keep
* Major Key - Twilight Theatre

If the Major Key Hints option is turned on,
reading the tombstones next to the Great Door will tell you where your major keys are located.
This will automatically create hints.


## Spawn Points

The Spawn Point option allows you to choose (directly or randomly) where you will start the game.
The following spawn points have special behaviors:

* Dungeon Mirror: the vanilla starting point in Dilapidated Dungeon

    If this option is selected, Start With Breaker will be forced on
    and you will most likely be expected to leave through the dark rooms to The Underbelly.
    See [this video](https://youtu.be/Z_a9l2wzd8c) for a guide on how to do that.

* Library: the save point at the start of Listless Library

    If this option is selected, either Start With Breaker or Randomize Books must also be turned on.
    If both options are off at the start of generation, Start With Breaker will be forced on.
    
    If just Randomize Books is turned on, your sphere one will have a lot of checks but will be very short,
    so keep that in mind if you are playing in a multiworld with other people.

* Theatre Main: the save point in the auditorium in Twilight Theatre

    If this option is selected, your starting inventory will include Cling Gem/one Cling Shard on normal,
    or Heliacal Power/one Air Kick on hard+.
    You will be able to leave Twilight Theatre through the big pillar room to the south.

The following spawn points don't have any special behaviors:

* Castle Main: the save point near Memento in Castle Sansa
* Castle Gazebo: the save point in the gazebo in the Castle Sansa courtyard
* Underbelly South: the save point near the building at the south of The Underbelly
* Underbelly Big Room: the save point in the big room in the middle of The Underbelly
* Bailey Main: the save point in Empty Bailey
* Keep Main: the save point in the main hallway in Sansa Keep
* Keep North: the north save point in Sansa Keep


## Item Appearance

Vanilla Pseudoregalia items out in the open appear as they do in the base game.
This applies to your own items as well as items of other Pseudoregalia players in the multiworld.

Items from other games out in the open appear as the Archipelago logo with an aura around it.
The color of the aura indicates the classification of the item:

* A progression item has a gold aura
* A useful or trap item has a green aura
* A filler item has a red aura

The Healing and Magic Power items appear as generic filler items.

All items in interactable locations (goats, chairs, books, notes)
appear as an aura around the interactable object.
The color of the aura follows the same pattern as generic items described above.
The aura goes away once the item has been collected.

The appearance of items can be customized in client settings.
For example, you can make all items look the same if you would prefer that.
See the Setup Guide for more info.


## Extra Features

### Solar Wind Toggle

You can toggle Solar Wind once you've obtained it by pressing the top face button on controller
or left ctrl on keyboard.

### In-Game Console

Once you are in game, you can press enter to bring up the in-game console.
In addition to all the usual MultiworldGG commands like `!hint`,
here are some useful Pseudoregalia-specific commands:

* `/spawn`: saves the game and warps you to spawn. Useful to prevent softlocks.
* `/breaker`: recalls Dream Breaker if you've received it but don't have it for some reason.
* `/popups hide`: toggles whether item popups appear at all.
* `/popups mute`: toggles whether item popups make a sound when they appear.


## FAQ

* Log file can be found at `Pseudoregalia_AP/pseudoregalia/Binaries/Win64/ue4ss/UE4SS.log`.
  This isn't super helpful for crashes, but if you have other issues like an item not showing up,
  you might be able to get some information here.
  Note that the file is reset every time you boot up the game.
* You can reach the Castle Sansa - Alcove Near Mirror location itemless
  by jumping down after entering Dilapidated Dungeon from Castle Sansa.
  See [this video](https://youtu.be/Z_a9l2wzd8c?t=256) for an example of how to do that.
* You can enter The Underbelly "backwards" by taking a trek through these areas:
  Sansa Keep -> Twilight Theatre -> Dilapidated Dungeon (dark rooms) -> The Underbelly.
  On normal and hard, you won't be expected to go through the dark rooms until you have Ascendant Light.
* On hard+, you are expected to not cut down the hanging platform in the room behind the locked door in Sansa Keep.
  You can use it to access the locked room without a key and the Sunsetter location by doing a coyote jump,
  but cutting it down makes that impossible.
