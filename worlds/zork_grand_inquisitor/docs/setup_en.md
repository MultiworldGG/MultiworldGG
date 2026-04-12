# Zork Grand Inquisitor Randomizer Setup Guide

## Requirements

- Windows OS (Hard required. Client is using memory reading / writing through Win32 API)
  - A Linux environment can also be used if configured properly. See the Linux instructions below.
- A copy of Zork Grand Inquisitor. GOG version preferred. Steam version will need to be manually configured to work with ScummVM
- ScummVM 2.7.1 64-bit (Important: Will not work with any other version. Direct Download)
- Archipelago 0.6.3+


## Game Setup Instructions

No game modding is required to play Zork Grand Inquisitor with Archipelago. The client included with the APWorld does all the work by attaching to the game process and reading and manipulating the game state in real-time. The instructions assume the game is already installed.

**GOG Instructions**
- Open the directory where you installed Zork Grand Inquisitor. You should see a `Launch Zork Grand Inquisitor` shortcut.
- Open the `scummvm` directory. Delete the entire contents of that directory.
- Still inside the `scummvm` directory, unzip the contents of the ScummVM 2.7.1 zip file you downloaded earlier.
- Go back to the directory where you installed Zork Grand Inquisitor.
- Verify that the game still launches when using the `Launch Zork Grand Inquisitor` shortcut.
- Your game is now ready to be played with Archipelago. From now on, you can use the `Launch Zork Grand Inquisitor` shortcut to launch the game.

**Steam Instructions**
- Unzip the contents of the ScummVM 2.7.1 zip file you downloaded earlier to a directory of your choosing.
- Launch ScummVM.
- Click `Add Game` and select the directory where you installed Zork Grand Inquisitor
- You might have to tweak a few ScummVM settings, as you won't have the curated configuration the GOG version does, but the game should be playable regardless.

**Linux Instructions**
- Before continuing, your goal should be to have the vanilla game running in ScummVM 2.7.1 through Wine. Unzipping the ScummVM 2.7.1 zip file to a directory of your choosing, running ScummVM and adding Zork Grand Inquisitor manually is the recommended method, even if you own the GOG version.
- Download the latest _Windows_ release of Archipelago (.exe file).
- Install it to a Wine prefix of your choosing.
- Inside your ScummVM directory, create a batch file (.bat) with the following content:
```batch
start C:\ProgramData\Archipelago\ArchipelagoLauncher.exe "Zork Grand Inquisitor Client"
.\scummvm.exe
```
- Run your newly created batch file. Both ScummVM and the Zork Grand Inquisitor Archipelago Client should open.
- This is how you will launch everything to play the Archipelago version of Zork Grand Inquisitor on Linux from this point forward.


## Joining a Multiworld Game

- Launch Zork Grand Inquisitor and start a new game. Skip or wait for the cinematic to finish.
- Open the Archipelago Launcher. Find and click `Zork Grand Inquisitor Client`.
  - If you are on Linux, running the batch file you created in your ScummVM directory should take care of the 2 previous steps. You will have to launch Zork Grand Inquisitor through the ScummVM interface manually.
- Using the `Zork Grand Inquisitor Client`:
  - Enter the room's hostname and port number (e.g. archipelago.gg:54321) in the top box and press `Connect`.
  - Input your player name at the bottom when prompted and press `Enter`.
  - You should now be connected to the Archipelago room.
  - Next, input `/zork` at the bottom and press `Enter`. This will attach the client to the game process and will output information about the seed.
  - If the command is successful, you are now ready to play Zork Grand Inquisitor with Archipelago.


## Continuing a Multiworld Game

- Perform the same steps as above, but instead of starting a new game, load your latest save file.
- The client ensures that the loaded save file matches the data of the connected slot before continuing. Nothing undesirable will happen if you accidentally load the wrong save file and connect.
