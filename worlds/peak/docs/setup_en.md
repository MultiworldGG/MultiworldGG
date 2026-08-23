# Guide for PEAK in MultiworldGG

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
