# Simpsons Hit and Run Setup Guide

## Required Software

- Simpsons Hit And Run PC release
- [Lucas' Mod Launcher](https://modbakery.donutteam.com/releases/view/6)
- [MultiworldGG](https://multiworld.gg/) (Latest release [here](https://github.com/MultiworldGG/MultiworldGG/releases/latest).)
- The latest release of the [client/memory manager and the lmlm mod](https://github.com/nmize1/AP-SHARRandomizer/releases/latest)
- The latest release of the [apworld](https://github.com/nmize1/Archipelago/releases/latest) (ships with MultiworldGG).
- [.NET 10 (x86)](https://dotnet.microsoft.com/en-us/download/dotnet/10.0) (**NOT x64**)

## AP Setup 

- Run Setup.MultiworldGG.version number.exe but don't open the launcher yet
- Double click simpsonshitandrun.apworld, it should pop up something saying APWorld successfully installed (and telling you to restart the AP launcher if you have it open) (this is not needed if you run MultiworldGG)

## Game Generation 

- Open MultiworldGGLauncher.exe in the MultiworldGG folder created when you ran the AP setup
- Search for and click Generate Template Yamls which will open a folder full of yamls
- Find The Simpsons Hit and Run.yaml and edit it to your liking.
- Save your edited .yaml in MultiworldGG/Players which is 1 folder up from the template yaml folder that opened.
- Optionally add more yamls for other players or other games you want to play. The multiworld will have 1 slot per yaml included here.
- In the AP Launcher again, search for and click Generate

## Game Hosting

- Go to [MultiworldGG](https://multiworld.gg/) and click Get Started (top right) -> Host Game then click Upload File
- Go to the MultiworldGG/output folder and choose the .zip that was created when you clicked Generate (should be the newest one)
- Click Create Room and wait for it to spin up. This is the room. You're good to go once there's a line that says /connect multiworld.gg:{port}

Note: You can also self host a MultiworldGG game server, but that's outside the scope of this guide.
  
## Install Lucas' Mod Manager, the lmlm mod, and the client/memory monitor mod.

- Follow [these](https://docs.donutteam.com/docs/lucasmodlauncher/setup) instructions to setup Lucas' Mod Manager.
- Place SHARAP.lmlm in the mods folder.
- Enable Archipelago Randomizer by clicking the checkbox in the Mods List. Currently, no other major mods are supported.
- Check [here](https://docs.donutteam.com/docs/lucasmodlauncher/mods/installing-mods) for more help installing mods.
  
- Under the "Settings" tab of the mod launcher, there are several optional mods. Don't enable anything that changes gameplay, but graphical changes or setting changes are fine.
  Logic expects you to play between 60 and 150 fps.
- Install .NET 10 from the link above. Make sure to install the **x86** version. The site will default to x64 as that's more modern, but SHAR needs x86.

- Finally, extract SHARRandomizer.zip where ever you'd like.

## Connecting and Playing
- Download the .apshar patch file from your room.
- Open the SHAR Client in the MultiworldGG launcher
  - On first launch, 3 file select prompts will open asking for SHARRandomizerFrontend.exe, Lucas' Mod Launcher, and the patch file 
  - On subsequent launches, it will just ask for the patch file. If you need to change the paths to the executables, you can do so in your host.yaml in the root of your MultiworldGG install.
- Enter your connection info in SHARRandomizerFrontend.exe
- Enjoy!

## Optional Extra Steps
- Use Universal Tracker as a Text Client and a tracker to help identify in logic checks.
  - Use the Universal Tracker in the launcher and connect the same as in the text client.
  - You now have a text client tab and a tracker tab. Text client behaves exactly like the default text client, tracker gives you a list of available checks based on what items you've received and your game settings.

## I'm having issues!

This is in active development! Check the pinned FAQ and/or ask for help in the [Discord channel](https://discord.com/channels/731205301247803413/1158211913495359548). 

## I'm new to AP/MWGG, what does this do to the game?

I'll assume you're familiar with randomizers in general. MultiworldGG/AP randos are separated into items you receive and checks you do to send items. In SHAR, the items are (depending on your yaml settings): Each character's jump and double jump, each characters attack, a "Gagfinder" for each character that enables them to do gags, a "Level X" for each level that unlocks that level's missions, a "Checkered Flag" for each character that unlocks the level's races, all the cars, and then some filler items in the form of an inventory of wrenches and hit and run resets you can use on demand and some various traps.

The checks are: Missions, wasps, cards, gags, talking to the character that would sell you a mission needed car (Barney, Homer, Otto, Willie, etc), and Gil's shops.

Your goal is configurable in the yaml, generally its some combination of mission, wasp, and card completions. The "goal" is for every slot in the multiworld to reach its goal. By default, reaching your goal will send all of your undone checks and make all unsent items for your game be sent to you. This can be configured. 

