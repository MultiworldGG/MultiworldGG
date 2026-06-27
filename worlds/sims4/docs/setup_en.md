# The Sims 4 Randomizer Setup Guide

## Required Software
- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases/latest)
- The Sims 4 from [Steam](https://store.steampowered.com/app/1222670/The_Sims_4/) or [EA](https://www.ea.com/games/the-sims/the-sims-4/buy)
- On AP: [APWorld](https://github.com/Simsipelago/Archipelago/releases/latest)
- [The Sims 4 Archipelago Mod](https://github.com/Simsipelago/Sims4ArchipelagoMod/releases)
- [Sims 4 Community Library (required dependency mod)](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest)
- [Lot51 Core Library (required dependency mod)](https://lot51.cc/mods/core-library)

## Installation
- Install MultiworldGG using the guide [from the website](/tutorial/Archipelago/setup/en). <!-- use this for webhost (../worlds/generic/docs/setup_en.md) -->
- On AP: Add the APWorld (the file should be named `sims4.apworld`) to the custom_worlds folder. This can be done in two ways: 
  - Open the client, and click `Browse Files` which will place you in your Archipelago directory. The `custom_worlds` folder should be visible. Drag and drop the APWorld file into the custom_worlds folder, and then you're done. 
    - NOTE: on platforms other than Windows, specifically for the AppImage version of Archipelago on Linux, and for people using Archipelago on MacOS, the folder you want to place the APWorld in is called `worlds`.
  - Alternatively, if you are on Windows, you can double-click the APWorld to install it automatically. 
  - Additionally, you may not see the .apworld extension on the `sims4.apworld` file on certain operating systems. Windows is usually the primary culprit for this, so the double click method is more friendly to people who are a bit less tech-savvy. However, there are guides online that show you how to enable file extensions on Windows, that you can find through a cursory Google search. 
- Follow the tutorial on [how to generate a game](/tutorial/Archipelago/setup/en) from MultiworldGG's website.
- Make sure you download both the `.ts4script` and `.package` files from the [Sims 4 Community Library](https://github.com/DeviantGameMods/Sims4CommunityLibrary/releases/latest) and the [Sims 4 Archipelago Mod](https://github.com/Simsipelago/Sims4ArchipelagoMod/releases/latest).
- You will also need to download the [Lot 51 Core Library](https://lot51.cc/mods/core-library). 
- Install all the downloaded mods to your Mods folder, which is usually located in `Documents/Electronic Arts/The Sims 4/Mods`.

## Setting up
- By default, this mod only uses skills from the base game as checks and locations. You can optionally enable your packs in the YAML file if you would like to have them included in the randomization. Packs are unlikely to cause problems with the mod, however you can disable them optionally **NOT USING THE IN GAME PACK SELECTOR**.
  * If you don't know how disable packs without using the in game pack selector, you can use this [tutorial](https://jamesturner.yt/disablepacks) by James Turner.
- Open the MultiworldGG Launcher and run the client. It should be called `The Sims 4 Client`. Upon the first time opening the client, it will prompt you to select your Mods folder. <strong>ONLY SELECT THE MODS FOLDER LOCATED AT</strong> <code>(your sims folder, typically called The Sims 4)/Mods</code>.
  * If you have to manually set the path make sure you don't include quotes in the path.
  * Example (Windows): <code>/set_path C:/Users/User/Documents/Electronic Arts/The Sims 4/Mods</code>
- Once you have selected the Mods folder if you've been prompted for it, follow the next steps before connecting.
- Launch your copy of The Sims 4, and ensure you have Script Mods enabled. The mod will not work correctly if Script Mods are not enabled.
  * You can enable Script Mods by going to `Game Options -> Other -> Script Mods Allowed`.
  * An existing save can be used, however since the mod will prompt you to reset your Sims' skills, it is recommended to use a new save file for every run of the randomizer you do. 
    * Some issues may occur if you use the same save file for multiple runs with different households for each run. We have not figured out how to fix this issue yet.
- Once you've launched your game once, and have had the mod load in and prompt you on a new file, return to the client window and connect to the server. Doing things in this order (especially for first time setup) is important for avoiding any issues or hiccups with setup. 
- After connecting, have fun! If you have any issues with setup, please feel free to ask for help, and we should be able to assist you with setting up the randomizer.
