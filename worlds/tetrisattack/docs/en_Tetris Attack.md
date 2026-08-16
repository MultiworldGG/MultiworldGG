# Tetris Attack Randomizer for MultiworldGG

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file. 

## Items
In the menu, the number of items you have received is shown at the bottom next to "CONNECTED!".

### Progression Items
Based on Stage Clear mode:
- **0 to 6** Stage Clear Round Gates, can't play any stages without them
- **0 to 30** Stage Clear (progressive) Stage unlocks, can't play the individual stages without them
- Stage Clear Last Stage, only exists if Round 6 is in the starter pack, required to clear the mode

If ! Panels are added to Stage Clear, a number of Stage Clear ! Panels items equal to the number of checks are added **(1 to 100 sets)**

Based on Puzzle mode:
- **0 to 6** Puzzle Level Gates, can't play any puzzles without them
- **0 to 60** Puzzle Stage (progressive) unlocks, can't play the individual puzzles without them
- **0 to 6** Puzzle Extra Level Gates
- **0 to 60** Puzzle Extra Stage (progressive) unlocks

Based on Vs. mode:
- **0 to 12** Vs. (progressive) Stage unlocks, can't fight certain characters without their stages
- Mt. Wickedness Gate, can't access stages 9 to 12 without it

### Filler Items
- **Any number of** Stage Clear points, values are based on Chains and Combos; the score counter never goes down except when you get a Game Over or quit a stage
- **0 or 8** Playable characters in Vs.; they're in your party forever
  - (Later on, there may be an option to have these 8 characters replace the Mt. Wickedness Gate, turning them into progression items)

### Traps
- **0 to 30** Stage Clear Special Stages, operates as a trap where you must win or lose against Bowser; effectively a deathlink threat or simply a time waster

## Locations
If you have multiple goals, you must clear all of them before your world is considered done.

The menu is changed to show in-game trackers. The number at the top right shows how many checks you have collected in any one mode.

Locations will be marked with the Archipelago symbol if they have not been collected. If another player auto-collects it, a fanfare sound will play in the menu and get rid of the symbol. The game will try to skip anything you've already cleared yourself to help with pacing. Checks that you are not allowed to make will have a lock symbol. The Vs. stage selector may show an additional lock if you don't have the Mt. Wickedness Gate.

### Stage Clear
- **0, 5, or 6** Round Clears, obtained after clearing the fifth stage of each round; note that all 5 Stage Clears are needed locally even if their checks have been collected
- **0 or 30** Stage Clears, obtained after getting under the clear line
- **0 to 30** Special Stage triggers, distributed evenly across Round or Stage Clears; in vanilla there's only 1, after Round 3 Clear
- Victory condition: deplete Bowser's HP in the Last Stage; Last Stage is typically accessible after the Round 6 Clear
- If ! Panels are added, a check is sent every X panels cleared **1 to 100 times**
  - Two more panels will appear to guarantee it being possible; if the panels per check is 1 or 2, it is possible to skip logic
  - To help with pacing, ! Panels will appear more aggressively if the player has a large backlog

### Puzzle
- **0 or 6** Round Clears, obtained after clearing all 10 puzzles of a level; note that all 10 clears are needed locally even if their checks have been collected
- **0 or 6** Extra Round Clears, obtained after clearing all 10 puzzles of an extra level
- **0 to 120** Puzzle Clears and Extra Puzzle clears, obtained after clearing the board completely of all panels
- Victory condition: Round 6 Clear and/or Extra Round 6 Clear, based on mode

### Vs.
- **10 to 12** Stage clears, obtained after defeating the opponent in a Vs. stage
  - A minimum difficulty may be set, stage 11 typically requires at least Normal and stage 12 typically requires Hard or V.Hard
- **8** Free characters, obtained after defeating the opponent in one of the first 8 Vs. stages
- All Friends Normal Again, obtained after clearing the first 8 Vs. stages which would normally allow access to Mt. Wickedness; note that all 8 stage clears are needed locally even if their checks have been collected or you have all 8 friends already
- Victory condition: beat the last stage, typically according to vanilla clear condition such as Stage 10 in Easy and Stage 12 in Hard

## Deathlink
Deathlink occurs if you hit the top of your board or you run out of moves in Puzzle mode. The game has a unique message for each situation.
