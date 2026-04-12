# Pinball FX3

## Where is the options page?

The player options page for this game is located [here](../player-options). It contains all the options
you need to configure and export a config file.


## Randomizer Features

- Entire collection of 100 tables (2 Free + 98 DLC) is supported
- Ability to select individual tables to include / exclude from generation
- Ability to customize how many tables to play (10-100)
- Target scores are accurately scaled per table
- Ability to set / randomize difficulty of target scores and stars (by table or globally)
- Ability to convert filler items into useful items during generation to help tackle the difficulty
- Scales well for all types of multiworlds: Short / Long Syncs, Asyncs; ~110-4800 checks
- Custom client UI that displays important information and updates in real-time (see screenshot)
- No modding! Only light memory reading that works directly from the client
- Universal Tracker (UT) fully supported (and recommended for guidance). YAML-free!


## How It Works and What to Expect

- A custom campaign of N pinball tables is generated based on your settings
- You are granted a starting table where you are able to complete all target scores and challenge stars
- You progress through the campaign by receiving table unlocks and challenge access items
- You will also gather some shiny quarters along the way. These are needed for both goal types. Either:
  - Collect N shiny quarters to unlock a final table and beat the high tier target score to win
  - Collect N shiny quarters to win
- Target scores have to be achieved in single-player mode
- Since the game hasn't been modified, you won't be prevented from playing anything. That said, location checks will only be registered when meeting the proper requirements
- Your playthrough will have you jumping between tables more than grinding a single table. Variety!
- You are free to use wizard powers and passive upgrades in any mode


## Locations

- Single-Player Score Targets: Low / Mid / High
- Challenge Star Targets: Low / Mid / High (for each of the 3 challenge types)
- Starsanity (optional — each star under each target is also a location)


## Items

- Table Unlocks
- 1 Ball Challenge Access: Low / Mid / High
- 5 Minute Challenge Access: Low / Mid / High
- Survival Challenge Access: Low / Mid / High
- Shiny Quarters (Macguffins)
- Table-specific useful items to progressively reduce the difficulty:
  - Score Multipliers
  - Star Requirement Discounts
  - Target Score Discounts


## Rapid-Fire Playing Instructions

- Prerequisite: Install the Pinball FX3 APWorld as you would any other custom APWorld
- Prerequisite: Have a multiworld generated and a room hosted
- Open Pinball FX3
- Reopen the Archipelago Launcher and open the Pinball FX3 Archipelago Client
- Connect to the multiworld room
- Send the `/pinball` command
- You are ready to play! Make sure to check out the Pinball FX3 tab in the client


## Disclaimers

- This implementation will **only** work on the current Steam version of Pinball FX3 (as of January 25, 2026). Any other version will not work. Future versions (if any) will require an APWorld update
- You do **not** need all DLC to play, but at least 10 tables are required to generate. This roughly equates to needing 2–3 DLC packs. They frequently go on sale, and you should be able to meet the minimum table requirement fairly cheaply
- While the implementation is meant to work with the Windows executable of the game, Linux should work with both a Windows MultiworldGG install and the game running under the same Wine prefix. This has not been tested and no support will be provided for it
- While this implementation has been relatively well-tested, issues could still arise, especially with individual tables (not all 100 tables were fully played during testing). Generation should be flawless, and multiple seeds have been completed without issues. The custom client tab is more experimental, but issues with it (if any) should not prevent you from checking locations or reaching the goal
- While Pinball FX3 is no longer Zen Studios' main product, it is still technically an online game. To err on the side of caution, this implementation does not modify any game files or write to RAM in any way. This limits what can be achieved randomizer-wise but keeps it safer for your account and EULA-friendly. You can add `-offline` to the game's launch parameters to fully disable online features (recommended)
- This game is **hard**. Especially the upper half of 1 Ball Challenge stars. Make sure you are comfortable with your table selection before committing to a multiworld with other players. You could be expected to get 11 stars on any table, and you likely will not be able to rely on useful items for your starting table