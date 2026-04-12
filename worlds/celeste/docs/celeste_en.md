# Celeste Randomizer Setup Guide

## Required Software

- [Everest mod loader](https://everestapi.github.io) installed on your copy of Celeste.
- CelesteArchipelago Everest mod from the [GitHub releases page](https://github.com/doshyw/CelesteArchipelago/releases).
- Celeste APWorld from the [GitHub releases page](https://github.com/doshyw/CelesteArchipelago/releases) (not needed with the MWGG client)
- MultiworldGG from the [MultiworldGG Releases Page](https://github.com/MultiworldGG/MultiworldGG/releases).

## Configuring your YAML file

### Generating a Celeste game (online)

1. Follow the instructions in the [MultiworldGG Setup Guide](tutorial/Archipelago/setup/en#on-the-website) to generate a
`.yaml` file using the [Celeste Player Settings Page](/games/celeste/player-options).
1. If playing multiplayer, follow the instructions in the [MultiworldGG Setup Guide](tutorial/Archipelago/setup/en#generating-a-multiplayer-game) to complete the generation and hosting steps.

### Generating a Celeste game (offline)

1. Download and install [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases).
2. Open your MultiworldGG installation in a file explorer (defaults to `C:\Program Files\MultiworldGG` on Windows).
3. Follow the instructions in the [MultiworldGG Setup Guide](tutorial/Archipelago/setup/en#on-your-local-installation) to
generate and host your game.


## Setting up your Celeste client

### Installation

1. Follow the steps in the [Installing Everest guide](https://everestapi.github.io/#installing-everest) to download 
Olympus and use it to install the Everest mod loader for your Celeste client.
1. Download the `CelesteArchipelago.zip` Everest mod from the 
[GitHub releases page](https://github.com/doshyw/CelesteArchipelago/releases) and place it into the `Mods` directory 
under your Celeste installation.
1. Launch Olympus, click "Manage Installed Mods", and ensure that `CelesteArchipelago` is the only mod enabled.


### Connect to the MultiServer

1. Launch Celeste (either by normal means or by clicking "Everest" on the Olympus main menu).
1. Press the "Archipelago" button on the main menu.
1. Enter in your connection details
    - Name: enter your slot name (e.g., `Madeline`).
    - Server: enter the IP/HTTP address (e.g., `multiworld.gg`).
    - Port: enter the port you wish to connect on (e.g., `38281`).
    - Password: enter the password set for the room (leave this blank if no password has been set).
1. Press "Connect to Session" to connect to the MultiServer! Happy playing!


### Using MultiworldGG console commands

At this stage, the Everest mod does not support sending commands to the MultiworldGG server. If you wish to do so, you 
will need to open `MultiworldGGTextClient.exe` under your local 
[MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases) installation and separately connect to the 
MultiServer to execute commands.
