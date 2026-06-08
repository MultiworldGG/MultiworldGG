# Changelog

## 0.6.6

### Bugfixes/Corrections

* Fixed packaging mistake of the apworld file, leading to errors during seed generation.

### Other

* Updated the `Ressources and FAQ` docs
  * Swap links to point to the new Github repository
  * Update the tracker list
* Updated the setup docs
  * Mention bizhawk 2.11 or newer as possible emulator version
  * Add setup guide for Luna's Project64

## 0.6.5

### Bugfixes/Corrections (0.6.5)

* Fix logic bug that could assume possible access to chapter 8 even though the required spirits were not obtained yet during `Required Spirits: Specific` and `Required Spirits: Specific_And_Limit_Chapter_Logic`. This could lead to impossible seeds.

### Other (0.6.5)

* Implemented Archipelago procedure patching. From now on hosts generating a multiworld seed will no longer need to provide their own Paper Mario ROM.
* Added `archipelago.json` file for AP version 0.7.0 compatability.

## 0.6.4

### Bugfixes/Corrections (0.6.4)

* Fix for Kent C Koopa logic not working correctly, which often meant the logic expected you to access the Koopa region through the sewers rather than Pleasant Path.

## 0.6.3

### Bugfixes/Corrections (0.6.3)

* Fix for ISpyPanelHints being set incorrectly
* Fix for partner upgrade shuffle generating incorrectly / errors in certain setting combinations

## 0.6.2

### Changes to existing features (0.6.2)

* Chapter 8 locations are now removed when your goal is set to `open_star_way`
* There are a handful of other minor fixes related to the `open_star_way` setting such as star beam power stars being taken into account despite it not being attainable.

### Bugfixes/Corrections (0.6.2)

* Thanks Icebound for fixing the issue with Merlow shop item strings getting offset as you buy items
* Fix for situations where the item pool was almost too large for the number of available checks; if the item pool is still too large for the number of checks, there's now an error that gives some suggestions towards fixing it.

## 0.6.1

### New features (0.6.1)

* When receiving consumables, Mario will now act as though he just found the item in the field. If your inventory is full, you'll have the opportunity to toss the item or toss something already in your inventory. Other items will still not have an animation for now. Feedback is welcome on whether it would be desired or not to have this animation for every item received.
* Shop items now have their descriptions changed when it's a multiworld item. The player the item belongs to and the item's name will be displayed, with the item name's color matching the default colors for progression, useful, filler, and trap item classifications. Autohinting will still be on for now, though that may be revisited in the future.
* The item trap option is now implemented. You can choose `no_traps`, `sparse`, `moderate`, or `plenty`.

### Changes to existing features (0.6.1)

* The license for the apworld has been changed from GPL-3 to MIT to match PMR.

### Bugfixes/Corrections (0.6.1)

* Corrected the logic function on the TTT pipe to Jade Jungle (thanks dakennyman for reporting this and faristheancient for reminding me)

Thanks Icebound for all of the base mod changes that made these updates possible!

## 0.6.0

### New features (0.6.0)

* Paper Mario Randomizer, the base rando, received its [0.30.0 release](https://pm64randomizer.com/changelog). For a full list of changes coming from the base randomizer, see the above change log. The new features include options for I Spy Panel Hints to show what item or item type is under a panel, options for Kent C Koopa and the Bowser Door Quiz, and the ability to shuffle multi coin blocks to be anywhere (the item for them becomes a coin bag if not in a block.) The coin bag part in particular may alleviate many of the issues trackers have with multicoin blocks.

### Changes to existing features (0.6.0)

* LCL and Specific Star Spirits are now unified under one option, `spirit_requirements`, which can be set to `any`, `specific`, or `specific_and_limit_chapter_logic`

## 0.5.0

### New features (0.5.0)

* Paper Mario Randomizer, the base rando, received its [0.29.0 release](https://pm64randomizer.com/changelog). For a full list of changes coming from the base randomizer, see the above change log. The main update for the base randomizer was that they added plando. As AP already has a built in plando, this part of PMR is not being ported over.
* You can now choose to be given random starting stats while choosing what level you start at. For example, if you start at level 3, you might start the game with 5 HP, 15 FP, and 9 BP.

### Changes to existing features (0.5.0)

* Power stars in shops now will have their price vary with the amount of power stars in the game. More power stars means they'll be cheaper, fewer power stars means they'll be more expensive.

### Bugfixes/Corrections (0.5.0)

* The palm tree on the beach that drops two items, one of which is replenishable and one of which is not, has had its location names modified to clarify which is which.

**Note: A world generated on a previous version will not match up when using a client from this version and up.**

## 0.4.4

### Bugfixes/Corrections (0.4.4)

* Fixed random_puzzles failures related to LCL and not getting enough valid shop items for DDO Shop puzzles
* Allow require_specific_spirits and power_star_hunt
* Updated sample YAMLs to account for puzzles being allowed and death_link not being implemented

## 0.4.3

### New features (0.4.3)

* The random_puzzles option is now usable, meaning in game puzzles can now have random solutions. [thanks to Alchav!](https://github.com/JKBSunshine/PMR_APWorld/pull/5) For more information on what turning this option on entails, check the [PMR wiki here](https://github.com/icebound777/PMR-SeedGenerator/wiki/Random-Puzzles)

### Bugfixes/Corrections (0.4.3)

* Fixed a logic bug where Bowser's Castle water puzzle wasn't checking for ultra boots to raise the water level to the maximum, [thanks to Psither](https://github.com/JKBSunshine/PMR_APWorld/pull/7)
* Fixed a validation error against games smaller than 32MB, [thanks to Icebound777](https://github.com/JKBSunshine/PMR_APWorld/pull/6)

## 0.4.2

### New features (0.4.2)

* Features added to Paper Mario Randomizer in the [0.28.0 release](https://pm64randomizer.com/changelog) including additional options for Rowf, Dojo, and Partner locations. Boss Shuffle is not yet implemented.

### Changes to existing features (0.4.2)

* Updated APWorld to work correctly with Archipelago 0.5.1
* The PMR Settings String will now work again if you want to use the PMR site to choose your options. Old strings will no longer work.
* The same seed now properly generates the same randomized game

## 0.4.1

### Changes to existing features (0.4.1)

* The ratio of late game locations that get excluded has been updated for the new goal settings
The Gift of the Stars (the Star Beam) location is now included in the list of late game locations when Star Beam is shuffled
* You can now select random for the magical seeds when using the PMR site's setting string for your YAML
* You can now choose up to 16 starting items when using the PMR site's setting string for your YAML
* The generator will throw an error if you have more power stars required for Star Way or Star Beam than the total power stars in the seed

### Bugfixes/Corrections (0.4.1)

* Fixed md5 hash not being checked when selecting Paper Mario ROM file
* Fixed logic for having Star Way as the goal when not doing Star Hunt

## 0.4.0

### New features (0.4.0)

* Features added to Paper Mario Randomizer in the [0.27.0 release](https://pm64randomizer.com/changelog) including Star Beam Shuffle and the various changes to the goal options have been added to the Archipelago implementation! For a full list of those changes, check out the change log for their release above.
* For Star Beam Shuffle, upon reaching Bowser without Star Beam, he will tell you its location. If it is in your world, he will give you the region that it is in. If it is not in your world, he will tell you it is in Rogueport, meaning that it is in someone else's world. It is planned to be either baked into the rom or otherwise revealed without needing to spend hint points in the future, but for the moment you will have to use AP's hint system if you wish to know its exact location.
* There is a sign at Shooting Star Summit and in the Sanctuary of the Stars to tell you what the requirements are for Star Way and the Star Beam check respectively.
* Both Star Way and the Star Beam check can now be set to unlock with spirits, power stars, or any combination of the two. This means you can require both 5 spirits AND 50 power stars to enter Star Haven, rather than one or the other.
* The seed goal can now be set to Open Star Way, which will cause the game to end once you have opened Star Way instead of going to defeat Bowser. Before you could do this for Power Star Hunt, but now you can do it regardless of your goal settings.

### Changes to existing features (0.4.0)

* The dark cave rooms in Bowser's Castle now logically require you to have Watt to traverse them.
* The PMR Settings String will now work again if you want to use the PMR site to choose your options. Old strings will no longer work.

## 0.3.3

### Changes to existing features (0.3.3)

* More unshuffled locations are now removed from the multiworld's location pool so as to reduce the total check count, effectively reducing the amount of locations you need to check when unlocking hints when these options are turned off. Includes Koot Favors, shop items, and radio trade events.

### Bugfixes/Corrections (0.3.3)

* Badge pool limit is now 128 by default, with the vanilla badge count in the description being corrected from 79 to 80.
* Fixed Goomba Road to Goomba Village logic
* Fixed issue with no local consumables + LCL

## 0.3.2

### Changes to existing features (0.3.2)

* Logical Star Piece requirements for Merlow's Badge Shop Item locations (not the reward locations) have been reduced from 68 to 30. The locations are all excluded so this is purely to help with generation when doing a low number of star spirits + LCL
* Locations whose requirements are beyond the number of required star spirits are no longer added to the multiworld pool when using LCL, also aimed at helping LCL generation
* Various clarifications to setting descriptions

### Bugfixes/Corrections (0.3.2)

* Fixed Jelly Shroom item name in client/spoiler
* Fixed settings string incorrectly setting enemy damage value too high

## 0.3.1

### Changes to existing features (0.3.1)

* Gear (hammer/boots) is now received from the server at the start of the game. This means that even for solo games (you should probably just use the [normal randomizer](https://pm64randomizer.com/) instead of AP), you'll need to connect to the server (even if it's just a local server) to get your starting boots/hammer if you granted yourself any. This was done to fix an issue with trackers not knowing what gear (or partner) you started with.
* Some QoL settings that defaulted to off now default to on. Why would you not want Speedy Spin, anyways?
* Receiving consumables from other players while your inventory is full makes the received item disappear, with no way of getting it back. This is still the case, but you are now allowed to generate with the setting set to less than 100 at their own risk. It's very much recommended against because you could end up in fairly dire straits without consumables being more accessible. But, given the other goofy stuff AP and PMR can allow, if you want to make yourself suffer, go for it. Just know you've been warned.
* Reduced MultiWorld item prices from 35 to a random multiple of 5 between 10 and 30

### Bugfixes/Corrections (0.3.1)

* Fixed item rules (which prevent items from going into locations that the game can't handle) to allow non-local items, which will help generation
* Added a default value to the pmr_settings_string setting to prevent issues with the auto-generated yaml template
* The Out of Bounds/Loading Zone Storage setting now gets set properly in the rom
* Quake Bounce's name in the client now matches its in game name
* Fixed boss, NPC, enemy, and hammer color palettes not being set properly in the rom when choosing random options
* Changed keysanity: false's fill to allow excluded locations so that Bowser's Castle key placement doesn't get inhibited by excluded locations

## 0.3.0

### New features (0.3.0)

* `start_inventory` (the built-in AP option for setting what items you'd like to start the game with) now works with Paper Mario. You will receive your items upon connecting to the server similar to how you would if they were sent to you. More info on how to use the [start_items option here](https://archipelago.gg/tutorial/Archipelago/advanced_settings/en#universal-game-options).
* random_start_items is now functional, and condenses what was previously 3 settings that weren't implemented. You can set this setting from 0 to 16 to be granted that many randomly selected items upon connecting to the server and starting your game. These items can include up to 10 consumables.
* blooper_damage_requirements is a new setting with options None, Low, Medium, and High. Depending on the option, logic can be added to Blooper fights that make it so you aren't logically expected to fight them until you are well-equipped enough to do so.
* pmr_settings_string is a new setting that allows you to take the Settings string from the [PMR Site](https://pm64randomizer.com/), allowing you to use that for almost all of the YAML settings instead of editing a text file

### Changes to existing features (0.3.0)

* Some or all chapter 8 locations now get set to Excluded based on the requirements for reaching Star Haven. This will reduce the chance of progression items being placed in this chapter.
* `enemy_xp_multiplier` was previously changed to allow you to put in the multiplier you like without doing math, but it turns out that doing that made it so that non-integer multipliers wouldn't work. So we're back to needing to use a value of 4 for double XP, 2 for vanilla XP, 3 for 1.5XP, etc.

### Other (0.3.0)

* Docs got updated and moved around some. Everything aside from the ReadMe is now in the docs folder.

## 0.2.4

### New features (0.2.4)

* Shuffle_Chapter_Difficulty is now working for the enemy_difficulty setting. This means that instead of vanilla or progressively scaling hp and damage values, each chapter is assigned a difficulty from 1-7 which approximates the stats to match that chapter number's difficulty level.
* Formation_Shuffle is now working. Setting this to true will make it so that enemies will appear in random numbers and formations that may not exist in the original game. Enemies will still only exist in the chapter they are normally found.

### Changes to existing features (0.2.4)

* Added logic handling for quizmo and triple star piece items
* LCL now allows the use of merlow_items setting
* Locations requiring more star spirits than the star_spirits_required setting now get marked as excluded, meaning they will always contain junk items. This goes for Koot, Rowf, Dojo, and Trade locations.

### Bugfixes/Corrections (0.2.4)

* Star spirit requirements in the trade events setting description are now correct (was 0, 2, 5, corrected to 1, 3, 5)

### Other (0.2.4)

* Ultra Stone is now considered useful
* Attempting to generate a game with options that aren't implemented will result in an error and generation will fail

## 0.2.3

* Updated base patch with a fix for multiworld items in replenishable locations still spawning after being collected (courtesy of Icebound)
* Priority locations will no longer be filled with consumables (courtesy of Alchav)
* Items should no longer get placed in locations that cause crashing or glitchy behavior (coins on the Goomba Road sign, items with multiples in the Toad Town shop's store room)

0.4.6 of AP also came out today. While there have been no reported issues with compatibility, please report any issues in the Discord thread.

## 0.2.2

### Smaller Features

* Mystery_shuffle can now be set to random_pick and random_per_use
* Coin and Menu palette options are now implemented

### Bugfixes

* Fixed Super Jump Charge not being removed from the pool of items when progressive badges are turned on
* Fixed All or Nothing being set to filler instead of useful
* Fixed Magical Seed being the wrong ID when received while requiring less than 4 seeds

### Slot Data

* Added [slot data](https://github.com/JKBSunshine/PMR_APWorld/blob/main/__init__.py#L610). Tracker devs, feel free to let me know what if anything else might need added.

### Require Specific Spirits and Limit Chapter Logic

* require_specific_spirits (RSS) is now implemented
* limit_chapter_logic (LCL) is now implemented, which requires RSS being set to true as well

The two above options can be used together to reduce the length of a Paper Mario seed considerably.

RSS makes it so that instead of requiring any of the seven star spirits, you will require specifically the ones randomly selected at generation. Example: with star_spirits_required: 4 and require_specific_spirits: True, the generator could randomly choose for you to need the star spirits from chapters 1, 2, 5, and 7.

LCL makes it so that chapters whose star spirits will only have junk items and the key items specific to those chapters. So, in the above example, chapters 3, 4, and 6 would have no logically relevant items. Instead they will be filled with consumables, badges, coins, and key items that aren't used outside of those specific chapters. This means you can choose to completely ignore and avoid Forever Forest, Boo's Mansion, Gusty Gulch, Tubba's Castle, Shy Guy's Toybox, and Flower Fields.

**Quick recap/other notes on LCL**:

* Out of logic chapters have no off world items
* Useful items will stay in logic as much as possible
* Many options are incompatible with LCL, particularly those that involve going to multiple chapters to unlock those checks (e.g. Koot favors, the letter chain when not fully shuffled)
* Because these locations fill with only local items, the in logic locations will be more lacking in consumables than usual. Some players may prefer this, some may not; the behavior around what items get placed in the out of logic locations could be changed in the future. Make sure to give feedback on this if you have any.

Try out LCL with 3 or 4 star spirits and see how it goes! It could end up being short enough for syncs where Paper Mario might've been too long before.

## 0.2.1

* Generation now works on Linux
* Added Autograph item locations to Koot item locations group
* Fixed Volcano Vase turn-in logic rule (it was referencing the name without the space)
* Auto hinting now only gets applied to progression items

## 0.2.0a

Potential hotfix for an issue with receiving items that have multiple IDs. May or may not work, relatively untested; try only if you have an error pop up in your client while playing that mentions an index error. It's recommended you ask in the PM thread in the AP Discord before doing so. If you haven't had this issue, please stick to v0.2.0 for now, as this is an experimental fix.

## 0.2.0

You will need to adjust existing YAMLs from previous versions.

* The min/max starting partners have now been combined into one option. If you wish to have the number of partners be random, you can use the random syntax from Archipelago's [Advanced YAML Guide](https://archipelago.gg/tutorial/Archipelago/advanced_settings/en#random-numbers)
* The XP Multiplier now takes the actual multiplier you want, you no longer have to double it. If you want normal XP, set it to 1, if you want double, set it to 2, etc.
* Power Star Hunt is now a working option
* The game should now properly detect when your goal is reached (and release if set to auto-release)

## 0.1.7

Renaming overhaul. Doesn't actually change too terribly much, but better player-facing names has a lot of back end ramifications that could cause issues. Let me know in the PM thread in AP discord if you come across issues while playing with sending, or receiving items, or with generation and logic.

## 0.1.6a

Potentially fixes item receiving occasionally failing

## 0.1.6

Update PM Sample.yaml

## 0.1.5

Update setup_en.md

## 0.1.4

fixed DDD oasis superblock and item on bluffs check addresses

## 0.1.3

add super hammer to access rule for train station super block

## 0.1.2

fix local consumable random placement

## 0.1.1

change some option defaults to more expected values

## 0.1.0-alpha

change some option defaults to more expected values
