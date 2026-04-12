# Setup Guide for Resident Evil 3 Remake in MultiworldGG

## Required Software
- Resident Evil 3 Remake - With the latest changes made to the client, you should no longer *need* the Steam version to play.
- Praydog's REFramework - Frontend for our Client.
- Resident Evil 3 Remake AP Client 

## Optional Visual Setup Guide
- [RE3R Visual Guide](https://therealsolidussnake.github.io/RE3R_AP_SetupGuide) - note that it only covers non-RTX at the moment but you can substitute
the steps with RTX versions.

## Instructions

1. Install [Praydog REFramework](https://github.com/praydog/REFramework/releases) - make sure to grab the proper one for your installed RE3R
(You don't need to install the VR .dll files if you do not plan on using VR features)

2. Install our client [Non-RTX](https://github.com/TheRealSolidusSnake/RE3R_Non-RTX_AP_Client/releases) or
[RTX](https://github.com/TheRealSolidusSnake/RE3R_RTX_AP_Client/releases), again making sure to grab the proper one for your installed RE3R

3. You should now be good to go. See below for more details on how to use the mod and connect to a MultiworldGG game.

## Connecting to the MultiworldGG server

To connect to the multiworld server, simply type in your connection info into the "Archipelago Client for REFramework" window that appears
when you launch Resident Evil 3 Remake.

## Console Commands

You can use the same "Archipelago Client for REFramework" window to send commands.
"!" commands such as "!hint" and "!release" will work from the client window, "/" commands will not and would need a separate text client.
This may change in the future.

## FAQ/Common Issues

### I don't want to replay the beginning over and over!
Do yourself a favor, and make a save at the Subway Station right after meeting up with Carlos's crew for the first time.
Be sure not to grab anything near the typewriter prior to making the save. All items near it are part of the randomizer and grabbing any of
them early prior to saving will delete them from any randomizers played afterwards.

### The client windows aren't showing up when I start my game!
Be sure to double check that you installed the proper clients for the version of the game you're running. Mismatching either Praydog's or ours
to the installed version of your game will result in this behavior.

### I died because I ran out of ammo, so I went back to an older save and now my items are missing, what can I do?
The way the randomizer works, you should be starting back from whichever latest save you've made, autosaves count in this manner too. 
Starting from an older save will desync the items, but in the worst case if you do need to start from an older save or from the beginning you
can push the "Receive Items Again" button within the "Archipelago Game Mod" window.
