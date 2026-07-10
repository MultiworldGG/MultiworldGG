# Hatsune Miku Project DIVA Mega Mix+ Setup Guide

## Requirements
- [Hatsune Miku Project DIVA Mega Mix+](https://store.steampowered.com/app/1761390/Hatsune_Miku_Project_DIVA_Mega_Mix/) (Steam)
  - [Extra Song Pack](https://store.steampowered.com/app/1887030/Hatsune_Miku_Project_DIVA_Mega_Mix_Extra_Song_Pack/) (optional, recommended, cheaper bundled)
  - The game can be played in MultiworldGG without the Extra Song Pack DLC.
- Without MWGG: [The APWorld](https://github.com/Cynichill/DivaAPworld/releases/latest)
- [[GB]](https://gamebanana.com/mods/514140) [[DMA]](https://divamodarchive.com/post/279) Archipelago Mod

## First Time Setup
This is a minimal mod setup. **Mod managers are used at your discretion.**

1. [Install DivaModLoader.](https://github.com/blueskythlikesclouds/DivaModLoader?tab=readme-ov-file#installation)
2. Download and extract the Archipelago Mod listed under [Requirements.](#requirements)
3. Place the extracted `ArchipelagoMod` folder into the `mods` folder. 

If your **mod loader config** (see below) has a `priority` line, add `"ArchipelagoMod",` to it.

#### Resulting mod file structure
```
Hatsune Miku Project DIVA Mega Mix Plus\
├ DivaMegaMix.exe   <─ game, select if prompted by JSON generator
├ dinput8.dll       <─ mod loader
├ config.toml       <─ mod loader config
└ mods\
  └ ArchipelagoMod\ <─ AP mod folder
    ├ ArchipelagoMod.dll
    └ ...
```

## Optional Quality of Life Mods 
Please read descriptions before installing. These may not be relevant to you or may require additional files.

| Mod             | Sources                                                                                                                                              |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| ExPatch         | [[GB]](https://gamebanana.com/mods/388083) [[DMA]](https://divamodarchive.com/post/371) [[GH]](https://github.com/nastys/ExPatch/releases/latest)    |
| High Frame Rate | [[GB]](https://gamebanana.com/mods/380955)                                                                                                           |
| IntroPatch      | [[GB]](https://gamebanana.com/mods/449088) [[DMA]](https://divamodarchive.com/post/193) [[GH]](https://github.com/nastys/IntroPatch/releases/latest) |
| Window Thing    | [[GH]](https://github.com/vixen256/window_thing/releases/latest)                                                                                     |

## Mod Songs
**Note: Currently, using mod songs requires the seed to be [generated locally](/tutorial/Archipelago/setup_en#generating-a-multiplayer-game), not on the website. Hosting on the website afterwards is fine.**

1. Open the **Mega Mix JSON Generator** from the MultiworldGG Launcher.
2. If prompted to select `DivaMegaMix.exe`:
   - **If not prompted, skip this step**
   - Right-click the game entry in Steam, **Manage > Browse local files**
   - `DivaMegaMix.exe` (extension may be hidden) is what you will need to navigate to and select
3. Check song packs you want in your song selection pool.
4. When done checking packs click **Generate Mod String**.
5. In your YAML on the line for `megamix_mod_data` paste and format it as such:
   - `megamix_mod_data: '{"MyFirstSongPack":[["MyFirstSong",144,224]]}'`
   - If the line ends with `: 50` or similar, remove it.

Linux users that experience clipboard issues *may* need to run the MultiworldGG Launcher and JSON Generator through a command line to get the output there.

## Troubleshooting

### Determining song names for the YAML

To find the names to use for YAML options such as `include_songs`:

1. Create a valid YAML [including mod data if you have it](#mod-songs)
2. Place the YAML in MultiworldGG's `Players` folder
3. If running, completely restart MultiworldGG
4. Open **Export Datapackage** from the MultiworldGG Launcher
   - If asked, open with a text editor like Notepad 
5. Locate the game's section then the desired songs

For example, *Love is War* would be `Love is War [1]`.

### There are songs outside my specified difficulty settings
Starting (`start_inventory`), Included (`include_songs`), and the Goal Song (`goal_song`) will *always* ignore difficulty settings.

To increase the success of seed generation the difficulty settings are conservatively expanded until a minimally viable song pool is found. If you do not like the results of the difficulty expansion consider less restrictive settings.

### My settings are too long or difficult
**Note: You can play any available difficulty for the same checks.**

1. Enable **Developer Mode** from the Advanced tab
2. Switch to the Tracker tab
3. Right-click the song name

### Newly received songs are not appearing in game
While on the song list press ***F7***/your defined reload key or use `Client > Reload`.

- Switch to the **All** filter in the song list.
- Check each difficulty. Not every song is available on every difficulty.
  - Install [ExPatch](#optional-quality-of-life-mods). Without ExPatch a song's Extreme won't appear until its Hard is cleared.
  - Mod songs are commonly Extreme only and lack a Hard to clear, **requiring** ExPatch.
- If using New Classics, check the **All** filter for each gameplay style.
