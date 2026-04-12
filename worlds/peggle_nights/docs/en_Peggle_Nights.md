# Peggle Nights

[Read on the Archipelago Wiki](https://archipelago.miraheze.org/wiki/Peggle_Nights)

## Where is the options page?

The player options page for this game is located [here](../player-options). It contains all the options
you need to configure and export a config file.


## Randomizer Features

- All 70 Quick Play levels + 11 Peggle Masters supported
- Ability to select individual levels to include / exclude from generation
- Ability to select individual masters to include / exclude from generation
- Ability to customize how many levels to play (5-70)
- Ability to customize how many masters are available for play (1-11)
- Ability to set / randomize difficulty of target scores (by level or globally)
- Ability to convert filler items into useful items during generation to provide additional help
- Starting Ball Count / Fever Meter logic
- Scales well for all types of multiworlds: Short / Long Syncs, Asyncs; ~50-950 checks
- Custom client UI that displays important information and updates in real-time (see screenshot)
- No modding! Only light memory manipulation that works directly from the client
- Universal Tracker (UT) fully supported (and recommended for guidance). YAML-free!


## How It Works and What to Expect

- A custom campaign of N levels is generated based on your settings
- You are granted a starting level and master where you are able to complete your first location checks
- You start with only 5 balls, but can receive more
- Your fever meter is capped at each multiplier, but you can receive upgrades
- You progress through the campaign by receiving level unlocks and progressive items
- You will also gather some shadow pegs along the way. These are needed for both goal types. Either:
  - Collect N shadow pegs to unlock a final level and clear it to win
  - Collect N shadow pegs to win
- Each master's power is usable right away
- Your playthrough will have you jumping between levels as you unlock more stuff, not just beating levels and moving on
- The game is on the shorter side, with high check density. It is on the easier side, save for high tier scores and full clears
- Since the game hasn't been deeply modified, you won't be prevented from playing anything. That said, location checks will only be registered when meeting the proper requirements


## Locations

- Fever Meter Multipliers (2X, 3X, 5X, 10X)
- Level Clears
- Target Scores (Low / Mid / High)
- Style Shots
- Orange Peg Combos (3X, 5X)
- Peg Combos (7X, 15X)
- Full Clears (optional)


## Items

- Level Unlocks
- Master Unlocks
- Progressive Fever Meter Thresholds (Locks Fever Meter Multiplier, Level Clear and Target Score locations)
- Progressive Starting Ball Increases (Locks Target Score and Full Clear locations)
- Shadow Pegs (Macguffins)
- Level-specific useful items to progressively make things (even) easier:
  - Fever Meter Permanent Bonuses
  - Full Clear Discounts
  - Score Multipliers
  - Target Score Discounts