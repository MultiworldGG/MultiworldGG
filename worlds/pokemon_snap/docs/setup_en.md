# Pokemon Snap Randomizer Setup Guide

## Required Software

- [Project64 (PJ64) 3.0.X](https://www.pj64-emu.com/public-releases)
  - 3.0.1 the last tested version the devs have personally checked
  - Dev / 4.0 versions currently do NOT work with Pokemon Snap, as the emulator fails to load this game properly.
  - It has been confirmed to work with Linux systems using Wine
- for AP: [Pokemon Snap APWorld](https://github.com/nielrenned/PokemonSnap_Archipelago/releases/latest)
- An American/US version of Pokemon Snap

# General Concept

## Installation Procedures

1. Download and install the most recent MultiworldGG Multiworld Suite from the link above, making sure to install the most recent version.

2. If you want to use AP: Acquire the most recent APWorld from the [Releases page](https://github.com/nielrenned/PokemonSnap_Archipelago/releases/latest) and place the pokemon_snap.apworld in the custom_worlds folder of your Archipelago install

3. Download and install the PJ64 Emulator from the link above. Run the emulator at least once to make sure it is working.

4. Note: It is recommended for the first time you setup this world, you let the APWorld run before PJ64.
Why? Because this world will update some settings within PJ64 itself and it cannot save the file while the program is open.
This includes creating the connection between AP and PJ64. If you have a client that fails to communicate with AP, this might be your error.

## Create a Player file (.yaml)

### What is a player file and why do I need one?

Your player yaml file contains a set of configuration options which provide the generator with information about how it
should generate your game. Each player of a multiworld will provide their own file. This setup allows each player
to enjoy an experience customized for their taste, and different players in the same multiworld can all have different
options.

### Where do I get a player file? (Easy)

Run the MultiworldGGLauncher.exe from your MultiworldGG install and click `Options Creator`.
In the new window that opens scroll down on the left until you find `Pokemon Snap`.
Enter your Player Name in the `Player Name` box.
Pokemon Snap has a custom option to prevent useful items from showing up behind Photos that require RNG.
The photographs to be avoided can be adjusted by clicking on `Edit` under `Excluded RNG Required Photos`.
Once you have chosen your desired options click `Export Options` in the top right to export your player file.

### Where do I get a player file? (Hard)

Run the MultiworldGGLauncher.exe from your MultiworldGG install and click `Generate Template Options`.
This will produce a `/Players/Templates` folder in your MultiworldGG install, which contains default config files for 
every game in your `custom_worlds` and `lib/worlds` folder. You can manually edit the config file using a text editor of your choice.

## Generating a Single-Player Game

1. After modifying your yaml, place it into your MultiworldGG/player folder
2. Open the MultiworldGG Launcher and click "Generate". This will create a zip file in MultiworldGG/output
   - You will need to open this .zip to get your `.apsnap` patch file if you are not using the MultiworldGG website
3. Navigate to the MultiworldGG website and go to the Host Game page (top right menu)
4. Click upload file and pass it the .zip created in your output folder
5. Click the "Create New Room" link. You are now able to download your patch file from here (as of AP 0.6.2).
6. Run the MultiworldGGLauncher.exe and click `Open Patch`. Select your `.apsnap` patch file.
You will be prompted to locate your vanilla/original USA Pokemon Snap ROM the first time you do this.
   - This action will automatically run the Pokemon Snap Client (and connect to the webhost if the patch was downloaded from there).
   - The patch will be placed in the same folder as your patch file by default.
   - You will ***not*** need to patch the game every time you resume the _same session_, and can simply run the `Pokemon Snap Client` from the list on the right of the MultiworldGG Launcher
to continue later.
7. Open Project64 (if it has not opened already), open your newly patched Pokemon Snap Rom. Load all the way into a brand new save file.
   - You ***must*** use a brand new save file.
8. In the server page, there will be a port number. Copy this port number into the top of your Pokemon Snap Client if it did not populate on its own. 
   - The field should read `multiworld.gg:<port number>` for example
9. Once you have loaded into the game, click the `Connect` button at the top of the Pokemon Snap Client. You are now connected and ready to play!
   - Unfortunately, due to the nature of some checks, you must be connected to a server while playing. Please keep a link to the webpage on hand
10. To rejoin the room later, you need to open the webpage, open the Pokemon Snap Client through the MultiworldGG Launcher, and open the patched ISO with PJ64.
Then you can click connect on the Pokemon Snap Client so long as the port matches what is shown on the webpage.

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your patch file, or with an APSNAP patch file that they have extracted from the zip. 

Put your patch file on your desktop or somewhere convenient. Open the MultiworldGGLauncher.exe and click `Open Patch`. 
This should automatically launch the client, and will also create your ISO in the same place as your patch file. On first time patching, you will be prompted 
to locate your Pokemon Snap USA ROM and Project 64 installation.

### Connect to the client

When the ISO patched, the Pokemon Snap Client should have also automatically launched in
the background. If it did not, please check the log in your Archipelaog/logs folder. If this is its first time launching, you may be prompted to allow it to communicate through the Windows Firewall. You must reopen the client each time you connect to a different randomized ISO.

1. Open PJ64 and from PJ64, open your newly patched Pokemon Snap USA Rom
2. In the server page, there will be a port number. Copy this port number into the top of your Pokemon Snap Client. 
   - The field should read `multiworld.gg:<port number>`
3. Once you have loaded into the game, the client should log that PJ64 has been connected. Click the `Connect` button
at the top of the Pokemon Snap Client. If the port number is correct, you are now connected and ready to play!
   - Unfortunately, due to the nature of some checks, you must be connected to a server while playing
4. Start the connection script in Project 64: Click `Debugger -> Scripts...`, highlight the `ap_snap_pj64_adapter_30.js` script, and click `Run`
   - If you see "Unable to connect to Project 64. Attempting again in 5 seconds...", do this step.
