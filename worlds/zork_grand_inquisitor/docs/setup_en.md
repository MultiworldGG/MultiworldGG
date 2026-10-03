# Zork Grand Inquisitor Randomizer Setup Guide

## Requirements

- Windows OS (Hard required. Client reads, writes and allocates memory in the ScummVM process and redirects some of its function pointers to code it injects there, through the Win32 API. No remote threads are created)
- A copy of Zork Grand Inquisitor. GOG version preferred. Steam version will need to be manually configured to work with ScummVM
- ScummVM 2026.3.0 64-bit ([Direct Download](https://downloads.scummvm.org/frs/scummvm/2026.3.0/scummvm-2026.3.0-win32-x86_64.zip))
- MultiworldGG 0.7.100+


## Game Setup Instructions

No game modding is required to play Zork Grand Inquisitor with MultiworldGG. The client included with the APWorld does all the work by attaching to the ScummVM process and reading and manipulating the game state in real-time. The instructions assume the game is already installed.

**GOG Instructions**
- Open the directory where you installed Zork Grand Inquisitor. You should see a `Launch Zork Grand Inquisitor` shortcut.
- Open the `scummvm` directory. Delete the entire contents of that directory.
- Still inside the `scummvm` directory, unzip the contents of the ScummVM zip file you downloaded earlier. `scummvm.exe` should end up directly inside the `scummvm` directory, not in a subdirectory.
- Go back to the directory where you installed Zork Grand Inquisitor.
- Verify that the game still launches when using the `Launch Zork Grand Inquisitor` shortcut.
- Your game is now ready to be played with MultiworldGG. From now on, you can use the `Launch Zork Grand Inquisitor` shortcut to launch the game.

**Steam Instructions**
- Unzip the contents of the ScummVM zip file you downloaded earlier to a directory of your choosing.
- Launch ScummVM.
- Click `Add Game` and select the directory where you installed Zork Grand Inquisitor.
- You might have to tweak a few ScummVM settings, as you won't have the curated configuration the GOG version does, but the game should be playable regardless.
- Verify that the game launches and plays normally.


## Joining a Multiworld Game

- Launch Zork Grand Inquisitor and start a new game. Skip or wait for the cinematic to finish.
- Open the MultiworldGG Launcher. Find and click `Zork Grand Inquisitor Client`.
- Using the `Zork Grand Inquisitor Client`:
  - Enter the room's hostname and port number (e.g. multiworld.gg:54321) in the top box and press `Connect`.
  - Input your player name at the bottom when prompted and press `Enter`.
  - You should now be connected to the MultiworldGG room.
  - Next, input `/zork` at the bottom and press `Enter`. This will attach the client to the game process and will output information about the seed.
  - If the command is successful, you are now ready to play Zork Grand Inquisitor with MultiworldGG. Make sure to check out the `Items` tab in the client, and the `Entrances` tab when playing with the entrance randomizer.


## Continuing a Multiworld Game

- Perform the same steps as above, but instead of starting a new game, load your latest save file.
- The client ensures that the loaded save file matches the data of the connected slot before continuing. Nothing undesirable will happen if you accidentally load the wrong save file and connect.


## Important Notes

- Restarting the client or ScummVM is fine. Stop playing until the client is attached again with `/zork`, then load your latest save if ScummVM was restarted.
- If you update the APWorld while ScummVM is running, restart ScummVM.
- Client commands:
  - `/zork`: Attach to an open Zork Grand Inquisitor process.
  - `/overlay`: Toggle the in-game overlay.
  - `/overlay_tracker`: Toggle the in-game list of locations in logic. Requires Universal Tracker.
  - `/deathlink`: Toggle death link. Only available when death link is enabled in your options.
