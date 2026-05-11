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
- Universal Tracker can help you to figure out which platforms are accessible. The mini-map should help!
- You should be able to quit a game and continue it later, just follow the steps again. Minigames do save checks but do not save progress.

## Troubleshooting
All of these troubleshooting steps are for when the mod crashes on launch.
### The basics
- Is Refunct open when you open the mod? We only support the latest version of Refunct via Steam (build id 5753767).
- Please try it 2 or 3 times, sometimes it just crashes.
### Advanced
- There are two ways to learn more about the error.
  - Run `debug.bat` (after opening Refunct) and it'll print an error.
  - Find the log file at `Users\user\AppData\Local\Temp\refunct-tas.log` (note that the log file may not exist).
- **On Steam Deck: `debug.bat` says `CantConnectToRtil`.**
  - In compatibility, try if legacy mode works.
- **On linux, `debug.bat` says `thread 'main' panicked at 'called Result::unwrap()'...`**
  - Make sure that you configured `LD_PRELOAD` correctly.
- **`debug.bat` says `"failed to fill whole buffer"`**
  - Do you have Spybot system tray? That program might interfere with Refunct.
- **Log file ends with `Got code`**
  - You might have older graphics drivers.
  - Right-click the game on steam and add this as launch option: `cmd /C "set WGPU_BACKEND=gles&& %command%"`
  - Or you could try to update your graphics driver (this helped many times).
- **`debug.bat` says `An established connection was aborted` and the log file says `TcpError`.**
  - You might have older graphics drivers, please update them.
- **`debug.bat` says `ParseIntError { kind: InvalidDigit }`**
  - Refunct probably has multiple processes open (some kind of overlay)?
  - Please run Refunct, then open a cmd, and run `powershell -NoProfile -Command "Get-Process -Name 'Refunct-Win32-Shipping'"`. If it shows two or more lines, then this does seem to be the case.
  - Try to kill one of the processes (try the one with the lowest handles/cpu first) using `taskkill /Pid 8132` where `8132` is the ID. If Refunct doesn't crash, you got the correct one
  - Now try to run the mod again.


## Refunct TaS Tool

This tool is derived from https://github.com/oberien/refunct-tas.
There is a readme there too.
