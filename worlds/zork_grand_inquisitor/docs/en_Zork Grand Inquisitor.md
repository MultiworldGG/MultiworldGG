# Zork Grand Inquisitor

## Randomizer Summary

A majority of inventory items you can normally pick up are completely removed from the game (e.g. the lantern won't be in the crate, the mead won't be at the fish market, etc.). Instead, these items will be distributed in the multiworld. This means that you can expect to access areas and be in a position to solve certain puzzles in a completely different order than you normally would.

Subway, teleporter and totemizer destinations are initially locked and need to be unlocked by receiving the corresponding item in the multiworld. This alone enables creative routing in a game that would otherwise be rather linear.

Important hotspots can also optionally be randomized. This means that you will be unable to interact with certain objects until you receive the corresponding item in the multiworld. This can be a bit confusing at first, but it adds depth to the randomization and makes the game more interesting to play once you master it.

Location checks are granted for the following actions:

- Solving puzzles
- Accessing certain areas for the first time
- Triggering certain unique interactions, even if they aren't puzzles per se
- Looking at certain documents
- Picking up items where they normally lie
- Visiting landmarks (Optional; Landmarksanity option)
- Dying in unique ways (Optional; Deathsanity option)


## Randomizer Features
- A choice of 5 goals: _Three Artifacts, Artifact of Magic Hunt, Spell Heist, Zork Tour_ and _Grim Journey_
- 10 possible starting locations
- Random starter kits. 46 possible sphere 1 starts
- Random initial totemizer destination
- Randomizable hotspots: Individually or grouped by region
- VOXAM repurposed to always teleport you back to your starting location
- VOXAM can optionally have a very small chance to go wild and take you somewhere else, enabling out-of-logic gameplay
- Thematic filler items. Still do nothing. Much funnier than nothing.
- Shuffle Time Tunnels: Randomize where the three time tunnels lead
- Entrance Randomizer: Coupled / Uncoupled entrances. Optionally include subway destinations
- Traps: _Infinite Corridor Trap, Reverse Controls Trap, Teleport Trap_ and _ZVision Trap_
- Death Link :)
- Energy Link. Hit the mushroom with the hammer. See what happens. You wouldn't THROCK it
- Missable location checks can optionally be granted once they become unobtainable while in logic
- Death return: After dying, you're sent back to just before the fatal screen, no need to juggle saves
- In-game overlay: Goal progress, item notifications and locations in logic
- Mod-free setup, allowing for easy updates and juggling multiple versions
- A healthy number of locations for a point-and-click game
- The opportunity to impress family and friends by knowing and playing a randomizer for such an obscure game


## Tracking

### In-Client Trackers
The client that ships with the APWorld includes 2 trackers. All tracker state is persisted server-side and will be fully available for whoever connects to the slot. Having and launching the game is not mandatory to look at the in-client trackers.

The `Items` tab lists the items you've received, including destinations and hotspots.

For those braving the entrance randomizer, the `Entrances` tab is a fully automated entrance tracker. As you go through any entrance in the game, its destination will be permanently annotated in the tracker!


### Universal Tracker
The APWorld is also fully compatible with Universal Tracker, and its tabs are built right into the client. It is a YAML-free implementation (i.e. you don't need to have the YAML used to generate in your Players directory). It also includes a map view for a more visual tracking experience.

If you ever need to know how to check a location, click the ? button next to its name on the Tracker Page to get a full explanation.
