<!--
Copyright 2025-2026 JKLeckr
SPDX-License-Identifier: MPL-2.0
-->
# Cuphead
[Main](/games/Cuphead/info/en) | **Setup** | [Settings](/games/Cuphead/player-options) | [Github](https://github.com/JKLeckr/CupheadArchipelagoMod)

## Required Software
- **Cuphead** ([Steam](https://store.steampowered.com/app/268910/Cuphead/), [GOG](https://www.gog.com/en/game/cuphead))
  - PC: Tested
  - Mac: Not Tested - Use at your own risk
  - Linux via Proton: Tested - Might require extra setup
- **CupheadArchipelagoMod** ([Github](https://github.com/JKLeckr/CupheadArchipelagoMod))

## Optional Software
- **Cuphead - DLC** ([Steam](https://store.steampowered.com/app/1117850/Cuphead__The_Delicious_Last_Course/), [GOG](https://www.gog.com/en/game/cuphead_the_delicious_last_course))

## Setting up

*Note: The install process is WIP, so it is not the most user-friendly.*

Refer to [Github](https://github.com/JKLeckr/CupheadArchipelagoMod) for more details.

### Prerequisites
- A legal copy of Cuphead
- [BepInEx](https://github.com/BepInEx/BepInEx/releases) 5.x
- [CupheadArchipelago](https://github.com/JKLeckr/CupheadArchipelagoMod/releases)

### Instructions
1. Download the CupheadArchipelago mod from the [releases page](https://github.com/JKLeckr/CupheadArchipelagoMod/releases).

2. Place the extracted contents of BepInEx 5.x x64 for your OS into the Cuphead installation folder (the folder with `cuphead.exe` in it).

3. Place the contents of the extracted CupheadArchipelago folder into the `BepInEx/plugins` folder.

4. Launch game.

### Extra Notes
- Make sure you are installing the binary build of the mod and not the source code. Don't be one of those fellas!
- After doing step 2, there should be a `winhttp.dll` and a `doorstop_config` along with a `BepInEx` folder and some other files in the same directory as `cuphead.exe`. If this isn't the case, make sure you are placing all of the contents of the extracted BepInEx zip in the Cuphead installation folder.
- If `BepInEx/plugins` does not exist, you can launch the game with BepInEx once, or create the folder yourself.
- If you are on the Steam version, and the mod does not load, launch the game directly from Steam.
- If you are on Linux using Wine/Proton, use the Windows build of BepInEx.
- If you are using Steam on Linux or SteamOS, make sure to put `WINEDLLOVERRIDES="winhttp=n,b" %command%` in the launch arguments.
- There are no binary builds of CupheadArchipelago for macOS. You can build from source, but you are on your own. 

## Setting up MultiworldGG / AP

1. Launch Cuphead with CupheadArchipelago installed. It will create the config files.
2. Select an empty save slot. (Note the save slot must be empty to enable or disable Archipelago on it.)
3. Press the button combination shown in game to show the Archiepalago setup menu (if you are using a keyboard, it's C+Z by default).
4. Set it to enabled, and set all the required settings for connecting to Archipelago.
5. Once you are done, close the Archipelago setup menu and start the save slot. (Note it says "AP" in the corner of the save slot if Archipelago is enabled.)
6. Have fun, and watch out for bugs!

## Logs
If you want to see what is going on behind the scenes (useful for diagnosing problems), you should check the logs.
The logs are located in the `BepInEx` folder in the game directory. Logging can be configured in the config (See [Configuring](#configuring)).

## Configuring
The config files are in the game directory's `BepInEx/config` folder. The mod config file is called `com.JKLeckr.CupheadArchipelago.cfg`. It might be useful for debugging to add more verbose logging flags in the config. The game must be launched at least once for this to appear.

### Logging
Logging can be configured in the config.

The BepInEx console allows you to see what's going on in real time. By default, the BepInEx console is disabled.

These are notable config files and their settings for logging:

- `BepInEx.cfg`
    - Under `[Logging.Console]`, set `Enabled` to `true` to see the logging console window. Useful for seeing what's going on in real time. The log file might update regularly too, but it isn't as real time.
    - Under `[Logging]`, setting `UnityLogListening` to `true` helps with logging what Cuphead itself is logging.

- `com.JKLeckr.CupheadArchipelago.cfg`
    - Adding `Network` to `Logging` will show more verbose network action logging.
    - `Debug` is probably too verbose to be useful for most people currently. Logging is pretty verbose, even without `Debug` currently while the mod is in heavy development.
