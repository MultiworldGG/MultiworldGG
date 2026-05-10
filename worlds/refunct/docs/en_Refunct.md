# Refunct

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What are items and locations?

- You will have to unlock every cluster of platforms (that normally rise by pressing a button).
- You also have to find your abilities to swim, ledge grab, wall kick and jump on jumppads!
- Location checks are making platforms grassy by jumping on 'em (200+ locations).
- Your goal is to collect enough grass and go to the final platform (adjustable via yaml, shown in-game).
- There are now minigames that give extra checks!

## Other stuff

- Softlocked? Press New Game, your progress is saved.
- Buttons and platforms underneath buttons are not checks in the main game. (Red) buttons don't do anything.
- Universal Tracker can help you to figure out which platforms are accessible. The mini-map should help!
- You should be able to quit a game and continue it later, just follow the steps again. Minigames do save checks but do not save progress.
- The final cluster in the game won't appear and will stay underwater in the main game (the final button is weird).

## Troubleshooting

* **thread 'main' panicked at 'Failed to decode config: Error**:
  Your config file is invalid and couldn't be parsed correctly.
  Please make sure to correctly configure it.
* **thread 'main' panicked at 'called `Result::unwrap()` on an `Err` value [...] "Connection Refused"**:
  The tool couldn't connect to the game.
  Please make sure that Refunct is started before running the tool.
  On Linux also make sure that you configured `LD_PRELOAD` correctly.
  *If you're still having problems, try updating your graphics drivers (yes this really solves some problems).*
* **thread 'main' panicked at 'Cannot get pid of Refunct: Error { kind: NotFound, message: "program not found" }'**:
  WMIC (Windows Management Instrumentation Command-Line) either doesn't exist or its directory isn't in PATH.
  To put it in path, run `control sysdm.cpl,,3` in Run (WIN+R) -> Environment Variables -> [Under "User variables for (user)] -> Double click "Path". Add this entry to it: `%SystemRoot%\System32\Wbem`. Start the tool, and it should work.
* **Refunct crashes with (or without) FATAL ERROR**:
  On Windows this can happen from time to time when you start the tool.
  Try restarting Refunct and the tool.
  If the game continues to FATAL ERROR after multiple tries (2-3 should be enough),
  try to change your ingame FPS to a fixed value (e.g. 60 FPS) and try again 2-3 times.
  If it continues to crash, it could be due to multiple causes:
    1. You are not using the latest version of Refunct.
        Please verify your game files with Steam: Library → Right Click on Refunct →
        Properties → Local Files → Verify Integrity of Game Files...
    1. It could mean that I was too lazy to update all pointers to the latest version
        of Refunct.
        Currently refunct-tas is updated for Refunct BuildID 1964685.
        You can find your BuildID in Steam: Library → Right Click on Refunct →
        Properties → Local Files → bottom left
* **Refunct / the TAS tool crashes and the file `refunct-tas.exe` disappears:**
  Refunct-tas uses library injection, which some antivirus programs see as malicious
  action.
  Therefore your antivirus might have stopped execution and moves the executable
  into quarantine.
  Redownload the zip file and either whitelist `refunct-tas.exe` or disable it
  while you are using the TAS tool.
* **I got EAC banned**:
  No, you didn't. Refunct does not come with EAC. Period.
