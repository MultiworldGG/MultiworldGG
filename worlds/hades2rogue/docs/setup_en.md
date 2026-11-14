# Hades 2 Rogue Setup Guide

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases)

- [r2modman](https://thunderstore.io/c/riskofrain2/p/ebkr/r2modman/) (or a similar mod launcher for Thunderstore)

- On AP: The Hades2Rogue [APWorld](https://github.com/BrittisH39/Hades2Archipelago/releases/latest) (the file is `Hades2Rogue.apworld`, from the latest release)

Works on Windows. Linux and Steam Deck work through Proton. Steam Deck guide: https://sgg-modding.github.io/Hades2ModWiki/docs/installing-mods/steam-deck

The mod, the apworld, and the host's apworld must all be the version the seed was generated with. The client now shows an error box naming all three when they don't match.

- The Hades2Rogue [mod](https://thunderstore.io/c/hades-ii/p/BrittisH39/Hades2RogueArchipelago/) (installed via r2modman)


## Optional
- An installation of Hades 1 will allow you to utilize the Zagreus' Journey mod made by NikkelM to include some original Hades 1 content in your Hades 2 game. This includes the original route, some NPCs, and some keepsakes. Zagreus' Journey is no longer a dependency of the AP mod, so it won't be downloaded automatically. If you want that content, search for and download "Zagreus Journey" in r2modman, on the same profile as the AP mod.



## Installation

### Mod

- Install and launch [r2modman](https://thunderstore.io/c/riskofrain2/p/ebkr/r2modman/).
- Find and select Hades 2. Select which store you own Hades 2 on. (Epic Games Launcher untested at this time)
- Select or create a profile (name doesn't matter).
- Select Online on the left side, then search for and find "Hades2RogueArchipelago".

- Select download, then download with dependencies. This also downloads the other mods it needs (Hell2Modding, and zerp's NPCRoomRandomizer, Extended NPC Encounters, and DreamDiveTweaks).



### APWorld (only with AP)

- Launch [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).
- Drag and drop the [APWorld](https://github.com/BrittisH39/Hades2Archipelago/releases/latest) onto the Archipelago window.
- Close and relaunch Archipelago.

The other way is to place the file in the `custom_worlds` folder of your Archipelago installation. Install the apworld one way, not both. Two copies is a known cause of checks not sending. When updating, replace the old file. The host needs the same apworld.



## Configuring Your YAML

- Runs are designed to be possible regardless of your YAML settings, but it's recommended not to set maximum vows unless you are very confident in your Hades 2 skills. You will start the game with nothing, and the logic is set to believe you can at least make it to the boss of each region you have access to.
- The miniboss room shuffle is fixed per seed (e.g. Olympus always has the same two minibosses). That's by design.
- DO NOT enable Zagreus' Journey unless you have downloaded the Zagreus' Journey mod, and have Hades 1 installed in the same location you have Hades 2 installed in; alternatively you can use the Zagreus' Journey config in r2modman to point to your Hades 1 installation.



## Connecting to a Game

- Launch MultiworldGG, and launch the Hades 2 Rogue Client.
- Put in the server you're connecting to and the port at the top (example: multiworld.gg:45829). Hit connect.
- Enter your slot name when it asks for it.
- Once connected, hit "Launch Modded" in r2modman.
- Launch into a save, ensure the client says "Game connected to Bridge", and enjoy!



## For Troubleshooting/Issue Reports

- "Items arrive but checks don't send" is almost always a version mismatch. The client's error box names the mod, apworld and seed versions so you can see which one doesn't match.
- Mod log: r2modman profile folder → `ReturnOfModding\LogOutput.log`. It resets on every game start, earlier ones are in `ReturnOfModding\backup\<date>_LogOutput.log`. Client log: `<Archipelago folder>\logs\Hades2RogueClient_<date>.txt` (default `C:\ProgramData\Archipelago\logs`).
- Downpatching: the mod's Thunderstore page → Versions tab → install an older one. Older apworlds are on the [GitHub releases list](https://github.com/BrittisH39/Hades2Archipelago/releases).
- Visit the Hades 2 Rogue thread found [here](https://discord.com/channels/731205301247803413/1521929337954238624).
