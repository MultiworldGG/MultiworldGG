# Momodora Moonlit Farewell

## Where is the settings page?
The [player options page for this game](../player-options) contains all the options you need to configure and export a config file.

## Optional Settings in the YAML

### Deathlink
With this setting enabled, if you die, every other player in the session (that has Deathlink enabled) also dies. The same applies the other way around.

### Open Springleaf Path
When this is enabled, the Demon Strands and Wind Barriers on Springleaf Path are removed, so you can explore other areas earlier without needing to have Awakened Sacred Leaf/Sacred Anemone. Worth noting that this only removes these barries for access within Springleaf Path or into Lun Tree Roots. Items in Springleaf Path that have Demon Strands, if these only gate the item, will remain there.
All other areas and items that have Demon Strands will still require Awakened Sacred Leaf to access (these are some of the important ones):
- The Combat Challenges in Moonlight Repose
- Magic Blade Sigil in Demon Frontier
- Access to the Accursed Demon Autarch boss fight
- Worth noting that, with this setting on, you can access any area without defeating the Gariser Demon. However, **after** you defeat the Gariser Demon and get sent to Koho Village, **the game resets the map as if you're exploring it from scratch**, so be wary of that. This mostly affects the Fast Travel Locations if you unlocked any before the Gariser Demon fight.

### Bell Hover Generation
With this enabled, the world generation will consider being able to Bell Hover (increase height when jumping and using the Healing Bell at almost the peak of the jump) to randomize items in some locations. This can be used to access certain areas without the skill you require in a vanilla game to access them (i.e. Demon Frontier without Wall Jump).

You might need to get creative to access certain areas.

With this disabled, areas that can be accessed with Bell Hover will not have the skill needed to access them.

### Lunar Crystal Branch Shuffle
With this etting enabled, the Lunar Crystal Branches (the things that hang in the ceiling and give you money when destroyed) will be item location checks. They will still give you money when destroyed.

### Randomize Key Items
With this enabled, three key items are added as location checks and to the randomized item pool. These items are: 
- Gold Moonlit Dust
- Silver Moonlit Dust 
- Windmill Key

Both Moonlit Dust items are required for getting the Lunar Attunement check, and the Windmill Key is an important item to be able to access past Meikan Village. If you have the Windmill Key, you don't need to deliver the Wooden Box to be able to activate the Windmill.

### Oracle Sigil
With this setting enabled, the Oracle Sigil is added as a location check and to the randomized item pool. This Sigil is arguibly the hardest to get in the game, but also the best you could have, since it increases crit rate and damage by a great amount. However, in order to get it, you need to free all 30 Lumen Fairies that are all over the map. If you enable this setting, it's very likely one of the last checks you'll have, but it's also possible that you get this Sigil earlier.

### Berrysanity
With this setting enabled, all four type of berries are added as item location checks, and their respective stat gains (HP/Stamina/Magic/Black Berry stuff...) are added to the randomized item pool as progressive stat gains, with their respective names.

### Lilysanity
With this setting enabled, all Heavenly Lilies are added as item location checks, and Progressive Damage Upgrades are added to the randomized item pool.

### Fairysanity
With this setting enabled, all Lumen Fairies are arred as item location checks, and Progressive Lumen Fairies are added to the randomized item pool. You need all 30 Lumen Fairies for the Oracle Sigil item/location check.

### Companionsanity
With this setting enabled, all Companions (except Dora and Lineth) are added as item location checks, and each companion (except Dora and Lineth) is added to the randomized item pool.

### Selin Door Keysanity
With this setting on, it adds 4 Keys required to open the door to the Selin boss fight. This is usually done by defeating the 4 Selin's Shades before this door, but with the setting enabled these bosses will only have their regular location checks but won't help to open the door.

If you have this setting on as well as the Oracle Sigil setting, there's a possibility that one of the keys is in the Oracle Sigil check, making completing the game a very long task.

### Victory Condition
You can choose which boss you must defeat to consider the game as complete.
- **Moon God Selin**: Defeat Selin in Fount of Rebirth to complete the game
- **Dora**: Defeat Dora in Koho Village after the credits roll to complete the game

## Items and Locations
### Locations Checks
- All skills (all 5 main skills and fast travel)
- All Sigils
- All Grimoires
- All Bosses but the chosen final boss (most bosses send the check once their cutscene is over)

### Optional Checks (based on YAML settings)
- Lunar Crystal Branches
- Gold Moonlit Dust
- Silver Moonlit Dust
- Windmill Key
- Oracle Sigil
-  Heavenly Lilies
- Dotted Berries
- Stamina Berries
- Lun Berries
- Black Berries
- Lumen Fairies
- Companions (All but Dora and Lineth)

#### Note on Skills
Due to how the game manages the skills, if you have a skill before checking the room where you'd get it, the location will be disabled. 
To combat this, the game will automatically send the skill's location check if you enter the area where you'd get it in vanilla **only if** you have the skill by that point.
- For the Sacred Anemone, enter the room where you fight the Harpy Archdemon, and your skill will be temporarily disabled until you get the Sacred Anemone checks (after the Harpy Archedemon boss fight)
- For Lunar Attunement, you need all three requirements (Gold/Silver Moonlit Dust and defeating the Tainted Serpent)

### Items You Can Receive
- All skills (all 5 main skills and fast travel)
- All Sigils (Save for The Fool, Living Blood and all Sigils you can buy from Cereza. Checking these locations will send a location check as well as giving you their respective Sigil)
- All Grimoires
- 10 Lunar Crystals

### Optional Items You Can Receive (based on YAML settings)
- Gold Moonlit Dust 
- Silver Moonlit Dust
- Windmill Key
- Oracle Sigil
- Progressive Damage Upgrade
- Progressive Health Upgrade
- Progressive Stamina Upgrade
- Progressive Magic Upgrade
- Progressive Black Berry
- Progressive Lumen Fairy
- All companions (except for Dora and Lineth)
- 4 Selin Door Boos Keys


## Victory Condition
The game is considered finished when you defeat the chosen final boss and see their respective cutscene (if applicable).
- Selin: finish the text after the black screen to finish the game
- Dora: defeat Dora to finish the game

## Possible Issues
### Stuck in Harpy Room
- For some reason, with the OpenSpringleafPath setting on, the windzones in the fight with the Harpy, and only in this room, are **not** removed (I still don't get it). If you find yourself in this situation and can't leave the room, go back to the Title Screen and reload your save file. The red barrier that appears to the right of the room will be gone.
  - If you have **wall jump** or **double jump** you can just use those to leave the room. **If you don't**, the only other way I can think of is using [Bell Hover](https://www.youtube.com/watch?v=wEe-bJFBG_Q) for that particular place. This is a handy guide showcasing Bell Hover, and you can use the healing bell it up to 3 times to gain enough height to leave the room.

If any issues are found during playing or playtesting, please do us know in thew MultiworldGG Discord.
