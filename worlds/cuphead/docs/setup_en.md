<!--
Copyright 2025-2026 JKLeckr
SPDX-License-Identifier: MPL-2.0
-->
# Cuphead
[Main](/games/Cuphead/info/en) | **Setup** | [Settings](/games/Cuphead/player-options) | [Github](https://github.com/JKLeckr/CupheadArchipelagoMod)

## Required Software
- **Cuphead** ([Steam](https://store.steampowered.com/app/268910/Cuphead/), [GOG](https://www.gog.com/en/game/cuphead))
  - PC: Tested
  - Mac: Tested
  - Linux via Proton: Tested
- **CupheadArchipelagoMod** ([Github](https://github.com/JKLeckr/CupheadArchipelagoMod))

## Optional Software
- **Cuphead - DLC** ([Steam](https://store.steampowered.com/app/1117850/Cuphead__The_Delicious_Last_Course/), [GOG](https://www.gog.com/en/game/cuphead_the_delicious_last_course))

## Setting up

These instructions are for using the Gale Mod Manager. If you are using the macOS version of Cuphead or are not using Gale, refer to the [Github README](https://github.com/JKLeckr/CupheadArchipelagoMod/blob/main/README.md) for other install options.

More details about the mod are on the [Github Page](https://github.com/JKLeckr/CupheadArchipelagoMod).

### Prerequisites
- A legal copy of Cuphead
- [Gale Mod Manager](https://github.com/Kesomannen/gale)

### Instructions
1. In the Gale Mod Manager, select Cuphead as the game to mod.

2. Install CupheadArchipelago in Gale. You can either use built in browse mods function to download and install, or you can go to the [Thunderstore Page](https://thunderstore.io/c/cuphead/p/JKLeckr/CupheadArchipelago/) and select Install with App.

3. Select "Launch Modded" in Gale.

4. Enjoy!

## Setting up Archipelago

1. Launch Cuphead with CupheadArchipelago installed. It will create the config files.
2. Select an empty save slot. (Note the save slot must be empty to enable or disable Archipelago on it.)
3. Press the button combination shown in game to show the Archiepalago setup menu (if you are using a keyboard, it's C+Z by default).
4. Set it to enabled, and set all the required settings for connecting to MultiworldGG.
5. Once you are done, close the Archipelago setup menu and start the save slot. (Note it says "AP" in the corner of the save slot if MultiworldGG is enabled.)
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
