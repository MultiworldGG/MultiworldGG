# Dark Souls Remastered

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a config file.

## What do I need to do to randomize DSR?

See full instructions on [the setup page](/tutorial/Dark%20Souls%20Remastered/setup_en).

## What does randomization do to this game?

1. Every loose item on the ground, and potentially fog walls, are "locations" or "checks".
   Some guaranteed drops are also locations, in addition to the White Sign Soapstone location from the first Solaire encounter.
   All items in those locations will be shuffled into the randomized multiworld Item Pool.
   This means they can be found elsewhere, and that the items at those locations will themselves be replaced by other items in the Item Pool.

2. All keys and progression items (e.g. Lordvessel) will be forced into the Item Pool, unless they drop or are shoppable from non-randomized locations.

3. Undead Asylum is only partially randomized. This is intended behavior so as to not put the player into BK mode immediately.
   The keys and Estus flask are not randomized, but class equipment can be, depending on your settings.
   The only randomized ground item in the AP item pool is the one by the stairs to the exit.

4. By default, the starting equipment for each class is randomized. This can be
   disabled by setting "Randomize Starting Loadout" to false.

5. By setting the "Upgraded Weapons Percentage", you can randomize whether the
   weapons you find will be upgraded and/or infused.

6. You can exclude some locations from being randomized at all using specific options.

There are also options that can make playing the game more convenient or
bring a new experience, like removing start requiements for spells or weapons.
Check the options for more.

## How is the item pool constructed?
* Item Pool is currently constructed as follows:
    1. First all items in locations which were randomized are added to the pool.
    2. Then, key items and embers will replace any filler items. This includes any "Fog Wall Keys", if either `fogwall_sanity` option is on. This includes the three living Firekeepers' Souls.
    3. Then, Guaranteed items are added to the pool.
    4. If there are any Filler or Junk items left over, they are replaced with Souls of a Proud Knight (2000 souls each).
* If locations are excluded and excluded_locations_behavior is set to "do_not_randomize", then the items in those locations will not be added to the pool, and those locations will have their vanilla items. Even with `fogwall_sanity` on, fog walls excluded in this manner this will provide no item, as fog walls do not provide items in the base game.

## What's the goal?

That depends on your choice of `goal_condition`.
If you choose `gwyn`, it is to defeat Gwyn, which will require opening the path to his arena (by finding the lordvessel & 4 lord souls, which are randomized into the pool) and defeating him.
If you choose `all_bosses`, it is to defeat all 26 bosses.
If you choose `manus`, it is to defeat Manus, Father of the Abyss in the Artorias of the Abyss DLC (which is included in Remastered).
If you choose `ornstein_and_smough`, it is to defeat Ornstein and Smough in Anor Londo (recommended for short syncs). Note: You should exclude at least the `After O+S` location group if choosing this option. This will exclude all post-lordvessel checks, and the DLC.

## Isn't the game extremely open from the start? What is fogwall sanity?

In order to prevent ~60% of the game being open and available immediately, this mod introduces "Fogwall Sanity", which is on by default.    
With fogwall sanity, fogwalls in DSR will be locked, and will require an item from the Item Pool to unlock them.  
Passing through them will also count as a location or "check". 
* This includes the Fog Wall near the beginning of the Upper Undead Burg. If it's blocked - you'll have to go somewhere else! (e.g. check the skeleton courtyard, and part of Upper New Londo Ruins)
* This does not include the fogwall in the Northern Undead Asylum.
* This `fogwall_sanity` option can be disabled, but doing so is not recommended. Without this option, about 60% of the locations in your game would be consdiered in logic immediately - this is also considered a big "Sphere 1". With a big Sphere 1, you might need to get to the last check in the immediately available 60% of your game, in order to find an item that unlocks your friend who is stuck at 10% of their game. Because of how large Dark Souls is, it could take a long time to do that many checks - and make your friends have to wait on you, for quite a while.
* There is an additional `boss_fogwall_sanity` option that can be turned on, which makes most boss' arena fogs be similarly locked.
* The `Catacombs` and `Lower New Londo Ruins` fogwalls can be bypassed by basic platforming & elevator usage repsecitvely. As a result, they do not logically block access to their other sides.

## Do I have to check every item in every area?

By default, you will have to check every non-missable item.
This does not include failable quests or other missable items.

## What if I don't want to do the whole game?

If you want a shorter DSR randomizer experience, you can exclude certain locations
from containing progression items. By default, the items from those regions will
still be included in the randomization pool, but none of them will be mandatory.
However, you can set the `Excluded Location Behavior` option to `do_not_randomize`
in order to have their items not in the item pool and have them not impacted by AP randomization at all.

Besides excluding individual locations, you can exclude whole regions via the [Location Groups](#Location-Groups) listed below.

For example, the following configuration will not require you to do the DLC, The Great Hollow, or Ash Lake:

```yaml
  # Exclude DLC and out-of-the-way regions
  exclude_locations:
    ["All DLC regions", "Ash Lake", "The Great Hollow"]
```

## Artificial Logic Without Fogwall Locking
* If you disable the options for fogwall or boss fogwall locking, some artificial "logic" is introduced to limit the number of items that are "in logic" extremely early. This does not affect actual access, but affects what the randomizer considers "logically possible" to access at any point. Such rules are listed below:
* Access to the Great Hollow is behind Blighttown access + Lordvessel item.
* Access to New Londo Ruins Door to the Seal + Lower New Londo Ruins from Upper New Londo Ruins requires access to being able to defeat Ornstein and Smough (in addition to having the Key to the Seal - the default rule).

## How do I read the location names?

Locations are generally in this format:  
region code: item name - (optional) location

Region codes:  
UA - Undead Asylum  
UA2 - Undead Asylum 2nd visit  
FS - Firelink Shrine  
UB - Undead Burg  
UP - Undead Parish  
DE - Depths  
BT - Blighttown  
VotD - Valley of Drakes  
DB - Darkroot Basin  
DG - Darkroot Garden  
GH - The Great Hollow  
ASH - Ash Lake  
SF - Sen's Fortress  
AL - Anor Londo  
PW - The Painted World of Ariamis  
NL - New Londo  
TA - The Abyss  
DA - Duke's Archives  
CC - Crystal Cave  
DR - Demon Ruins  
LI - Lost Izalith  
TC - The Catacombs  
TotG - Tomb of the Giants  
FA - Firelink Altar  
KoFF - Kiln of First Flame  
SG - Sanctuary Garden  
OS - Oolacile Sanctuary  
RW - Royal Wood  
OT - Oolacile Township  
CotA - Chasm of the Abyss  


## Location Groups
By Category of check:
Fog Walls (17)
Boss Fog Walls (22)
Shop Basic Items (96)
Shop Extended Items (64)
Boss Souls (11)
Boss Humanity (20)
Boss Bones (10)
Boss Drops (10)
Lord Souls (4)
Mimic Drops (8)
Black Knight Titanites (7)
Black Knight Weapons (7)
Crystal Lizards (50)
Chest Items (75)
Corpse Filler Items (365)
Corpse Prog Items (7)
Corpse Useful Items (7)
Hostile Npc Drops (4)
Miniboss Drops (4)
Misc Drops (7)
Frozen Blacksmiths (5)
Corpse Ring Items (7)
Npc Prog Items (2)

By region:
2 Merchants - Bottomless Box (1)
3 Blacksmiths - Smithboxen (2)
4 Merchants - Repairbox (1)
Anor Londo (60)
Ash Lake (6)
Chasm of the Abyss (13)
Crystal Cave (12)
Darkroot Basin (26)
Darkroot Garden (36)
Demon Ruins (27)
Depths (27)
Firelink Shrine (93)
Kiln of the First Flame (6)
Lost Izalith (26)
Lower Blighttown (40)
Lower New Londo Ruins (11)
Lower Undead Burg (22)
Northern Undead Asylum (7)
Northern Undead Asylum Second Visit (11)
Oolacile Sanctuary (2)
Oolacile Township (17)
Painted World of Ariamis (49)
Royal Wood (41)
Sanctuary Garden (3)
Sen's Fortress (55)
The Abyss (3)
The Catacombs (35)
The Duke's Archives (54)
The Great Hollow (31)
Tomb of the Giants (35)
Undead Asylum Cell (1)
Undead Parish (37)
Upper Blighttown Depths Side (16)
Upper Blighttown VotD Side (9)
Upper New Londo Ruins (24)
Upper Undead Burg (53)
Valley of the Drakes (17)
Watchtower Basement (3)

## Item Groups
Ammunition (21)
Armor (235)
Boss Fog Wall Keys (22)
Boss Souls (12)
Bows (7)
Carvings (5)
Catalysts (11)
Consumables (71)
Covenant Items (4)
Embers (10)
Fire Keeper Souls (7)
Fog Wall Keys (17)
Junk (33)
Key items (32)
Lord Souls (4)
Medium Shields (23)
Melee Weapons (111)
Multiplayer Items (20)
Progression Items (27)
Ranged Weapons (11)
Rings (41)
Shields (46)
Souls (10)
Spell Tools (20)
Spells (72)
Talismans (7)
Traps (1)
Upgrade Materials (23)
Weapons (163)

