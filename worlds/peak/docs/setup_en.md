# Guide for PEAK in MultiworldGG

## Downpatching is currently required

After the Citadel update, the APWorld currently requires downpatching.
- Open your Steam console (Windows: Win+R and enter steam://open/console, Linux: open command line and enter steam steam://open/console) OR use a GUI such as mmvanheusden's SteamDepotDownloaderGUI
- Go to PEAK's SteamDB page, and note the following IDs: App ID (3527290), Depot ID (3527291) and Manifest ID (scroll down and click the Depots tab, then the first option under the Depots header (3527291). This will bring you to the Manifests page. Click on the Manifests tab and note the ID of the version you want (ex, last update from 26 July 2026: 970190337128155317)).
- In the Steam console, run the following command: 
  - ``download_depot 3527290 3527291 <manifestID>`` (replace <manifestID> accordingly). 
  - This will download into your Steam directory at ..\Steam\steamapps\content\app_3527290\depot_3527291\<manifestID>. If you use the GUI, fill out the ID fields as required, and optionally set what directory the depot will download into (it will download as ..\<customFolder>\<manifestID>).
- EXIT STEAM. 
- Go to ..\Steam\steamapps\common\PEAK and delete everything in the folder. Copy all the files from the depot you just downloaded (NOT the <manifestID> folder but the files WITHIN it) into the now empty PEAK folder.
- WITH STEAM STILL CLOSED go back up to ..\Steam\steamapps\ and look for a file called appmanifest_3527290.acf. Open this up in any text editor and locate the line that says "StateFlags" and set the number next to it to "4". Save and close.
- You may now reopen Steam. In r2modman (or the mod manager of your choice), be sure you have the mod PeakVersionBypass by kirigiri as that will allow you to play on the older version.
- If you want to return to the current version, simply go to the game properties in Steam and verify file integrity, which will automatically update you to the most recent version. You will need to follow the instructions above if you need to downpatch again. The badges/achievements from Citadel/Gloom should not be lost.
- Steam may still ask to update your PEAK install while it's downgraded. Simply go to Steam > Go Offline and play from there

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases)
- [BepInEx](https://github.com/BepInEx/BepInEx/releases)
- [Peakpelago Mod](https://github.com/Mickemoose/peak-archipelago/releases)
- [PEAK](https://store.steampowered.com/app/3527290/PEAK/)

## Setup the Mod

1. **Install BepInEx**:
   - Download BepInEx 5.x for your platform
   - Extract to your PEAK game directory
   - Run the game once to generate BepInEx folders

2. **Install the Plugin**:
   - Download the `peakpelago` folder from the releases
   - Drag the entire `peakpelago` folder into your `BepInEx/plugins/` directory 
   - The folder contains all necessary files

3. **Launch the Game**:
   - Start PEAK - the plugin will create a configuration file on first run
   - Connect using the in game UI


## How to Play

1. **Generate a Multiworld**:
   - Create a YAML configuration for your PEAK world
   - Generate the multiworld using Archipelago's generator
   - Host or join a multiworld session

2. **Start PEAK**:
   - Launch the game with the mod installed
   - The in-game UI will show connection status

3. **Connect to Archipelago**:
   - Use the in-game menu in the top left
   - Fill in the connection details and click Connect or hit Enter

4. **Play the Game**:
   - Ascents are initially locked - unlock them by receiving items
   - Collecting items and completing objectives sends checks to other players
   - Receive items from other players as they complete their objectives
   - Work together (or compete) to complete your goals!

## Note

- If you play in multiplayer mode, only the host should connect to the MultiworldGG server. Note that only the world connected by the host will send and receive items, so consider to only add one world to the seed if you want to play together.

## Troubleshooting

### Plugin Not Loading
- Verify BepInEx is installed correctly
- Check `BepInEx/LogOutput.log` for errors
- Ensure all dependencies are in the plugins folder

### Cannot Connect to Server
- Verify server address and port in config
- Check firewall settings
- Ensure the Archipelago server is running and accessible

### Items Not Received
- Check connection status in UI
- Verify slot name matches your generated world
- Review state file for corruption: `BepInEx/config/Peak.AP.state.*.txt`

### Locations Not Checking
- Ensure you're connected to the server
- Check that the location exists in the world definition
- Review debug logs for check submission errors
