# Toontown Randomizer for MWGG - Setup Guide

## Video Tutorial

A Video tutorial is available on [YouTube](https://www.youtube.com/watch?v=TJTC7A5OFTE) outlining the steps for setting up the game and the randomizer.

## Required Software

* [Toontown AP](https://github.com/toontown-archipelago/toontown-archipelago/releases/latest)

## Getting Started

At this time, Windows is the only supported platform. For other platforms, please see [Running From Source.](#running-from-source)

### Windows

To play Toontown: Archipelago, you will need to run a server.
If someone else is running a server, skip steps 3 and 4.

1. Download `TTAP.zip` from [here.](https://github.com/toontown-archipelago/toontown-archipelago/releases/latest)
2. Extract the ZIP to a folder of your choice.
3. Open the folder and run `start_servers.bat`. This will make some windows appear, do not close these during gameplay!
4. If you're looking to play with friends, see [here.](#i-set-up-the-server-and-everything-is-running-fine-i-can-connect-to-my-own-server-but-my-friends-cant-why)
5. To start the game, run `start_client.bat`. This will open a window that will help you set up your client.
6. Where it says "Username", enter a name unique to you. You should enter this same name everytime you play. Then press enter.
7. Where it says "Server IP", enter the IP address of the server. Then press enter. If you're running the server locally, just press enter without typing anything.
8. Enjoy Toontown: Archipelago!
9. For Archipelago randomizer specific setup check the [FAQ section.](#common-issuesfaq),

If you need more assistance, try following the video tutorial [here.](https://youtu.be/TJTC7A5OFTE)

### Docker (Linux Server)

Before starting, please ensure you have Docker and Docker Compose installed.
You can find out how to install them [here.](https://docs.docker.com/engine/install/)

1. Download the `Source Code (ZIP)` from [here.](https://github.com/toontown-archipelago/toontown-archipelago/releases/latest)
2. Extract the ZIP to a folder of your choice.
3. Using `cd`, navigate to the `launch/docker` directory.
4. Start the server using `docker compose up`. This may take a while.
5. Press `Control+C` to stop the server.

## Running from source

### Panda3D

This source code requires a specific version of Panda3D to run.

### Windows

Please download the latest engine build from [here.](https://github.com/toontown-archipelago/panda3d/releases/latest)

### Other

At this time Toontown: Archipelago only supports Windows.
To run on other platforms you will need to build the engine. 
This is an advanced use-case and is unsupported.
To get started, please see the build instructions [here.](https://github.com/toontown-archipelago/panda3d)

## Starting the game

Once Panda3D is installed, please find your operating systems' launch directory.
- Windows: `launch/windows`
- Mac: `launch/darwin`
- Linux: `launch/linux`

Then run the following scripts in order:
- `start_astron_server`
- `start_uberdog_server`
- `start_ai_server`
- `start_game`

## Joining a MultiWorld Game

* Extract the TTAP Zip file to a folder of your choice
* Open the folder and run `start_servers.bat`. This will make some windows appear, do not close these during gameplay!
* To start the game, run `start_client.bat`. This will open a window that will help you set up your client.
* Where it says "Username", enter a name unique to you. You should enter this same name everytime you play. Then press enter.
* Where it says "Server IP", enter the IP address of the server. Then press enter. If you're running the server locally, just press enter without typing anything.
* When in game, you first need to type (in Toontown's chat) !slot <SLOT NAME> where you replace <SLOT NAME> with whatever your slot is in the Multiworld room. 
* Type !connect <MWGG SERVER IP> to play!