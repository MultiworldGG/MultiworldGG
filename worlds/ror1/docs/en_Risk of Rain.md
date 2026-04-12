# Risk of Rain

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a config file.

## Can I play this randomzier with Risk of Rain Returns?
Yes!  Both Returns and the original 2013 versions of Risk of Rain are fully compatible.

## What does randomization do to this game?
All item pickups count as an item check.  When picking up an item, it will be removed and a location will be sent out.  With the `item_pickup_step` yaml option (and ingame setting), you can set an interval for how many items you want to pickup normally before one is sent to the multiworld.  Total number of checks can be set in the yaml settings.

Checks can also be grouped either based on map or universally.
### Universal grouping
All locations can be obtained anywhere in numbered order.

### Map Grouping
Locations are split between each individual map.  You must be on that specific map to send out it's given check.

In addition to this, all maps and stages will require the given item to be sent to you.  The rules for when you can access these stages are as follows
- You will need both the map and numbered stage (or the corresponding number of progressive stages if enabled) to enter.
   - You can disable the stage item requirement by disabling `require_stage` in the yaml
- With `strict_stage_prog` enabled, you can additionally set a requirement on if you need to have a prior stage and access to one of those maps to enter a later stage map.  
   - For example, to get to Ancient Valley, you need `Stage 2` and either `Sky Meadow` or `Damp Caverns` in addition to `Stage 3` and `Ancient Valley`.

In the settings, you can enable an option that will prioritize maps that have the most checks in them (currently defaulted to disabled until further testing is done with it).

## What is the goal of risk of rain 2 in archipelago?
Goal is set to release after defeating Providence at Risk of Rain.  The divine teleporter's spawn conditions can be tweaked in the yaml to make it so goaling isn't possible instantly.
- On map grouping mode, `Risk of Rain` is required to enter the final stage.
- If `stage_five_tp` is enabled, the divine teleporter is set to spawn exclusively on a stage 5 map (which would be Temple of the Elders without mods).
   - This is recommended for map mode, otherwise you will be able to goal the instant `Risk of Rain` is sent unless you have teleporter fragments enabled.
- You can enable "Teleporter Fragments" to be shuffled into the pool and set a certain percentage that needs to be found before the divine teleporter can spawn.

## Can I play this in multiplayer?
Not at the moment, multiplayer will be automatically disabled on both games with the mod installed.

## Is Archipelago compatible with other Risk of Rain mods?
Most mods should work with minimal issue.  Mods that add new survivors and items shouldn't have any compatibility issues.  On RoR1, mods that add stages work, though custom stages will be automatically skipped when on map grouping mode.  Stage mods for RoRR have currently been untested.