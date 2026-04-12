# Setup Guide
## Requirements
- [Rift of the Necrodancer](https://store.steampowered.com/app/2073250/Rift_of_the_NecroDancer/) from Steam
- [RiftArchipelago](https://github.com/studkid/RiftArchipelago/releases) mod from the github releases.

## Installation
1. Download and extract the RiftArchipelago.zip file into the Rift of the Necrodancer installation folder.  This folder can be found by right clicking on Rift of the Necrodancer on steam and navigating Manage -> Browse Local files.
2. **Linux Only**: Right click Rift of the Necrodancer on steam and open up properties.  In the Launch Options, add `WINEDLLOVERRIDES="winhttp.dll=n,b" %command%`.
3. On the title screen there should now be a connection window on the top corner to input your server info.

If for whatever reason the bundled version of BepInEx doesn't work you can try installing it manually from [BepInEx's releases page](https://github.com/BepInEx/BepInEx/releases/tag/v5.4.23.2).

## How to play with Custom Songs
1. Open the Custom Song menu with the mod loaded
2. Navigate to your Rift of the Necrodancer installation folder, there should be a new folder called `Output` with a `CustomSongs.json` file inside.
3. Copy and paste the contents of the json into the `rotn_mod_data` option in your yaml.

Notes:
- Currently this will include every custom song you have installed, so you'll want to manually exclude songs you don't want to roll.
- Include/Exclude is expecting the song's item name, for custom songs it'll be formated `<song_name> [<song_id>]`.  Generating and hosting a local game and running /items in a text client would be the easiest way to find the exact name
- Adding more than 500 non steam workshop songs may cause issues if running a game with other RotN players