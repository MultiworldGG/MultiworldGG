# Vampire Survivors Setup Guide

## Requirements

You will need:
- [MultiworldGG Client](https://github.com/MultiworldGG/MultiworldGG/releases)


## How to install
- Make sure to have [.Net6.0](https://dotnet.microsoft.com/en-us/download/dotnet/6.0) installed
- Download and Install [Melon Loader](https://melonwiki.xyz/#/?id=automated-installation).
    - The default Vampire Survivors install directory (for steam): C:\Program Files (x86)\Steam\steamapps\common\Vampire Survivors
    - Recommended melon version: 7.1
- Launch the game and close it. This will finalize the Melon installation.
- Download and extract the `SW_CreeperKing.ArchipelagoSurvivors.zip` from
  the [latest release page](https://github.com/SWCreeperKing/ArchipelagoSurvivors/releases/latest).
    - Copy the `SW_CreeperKing.ArchipelagoSurvivors` folder from the release zip into `Mods` under your game's install directory.
- Launch the game again and you should see the connection input on the top left of the title screen!
- To uninstall the mod, either remove/delete the `SW_CreeperKing.ArchipelagoSurvivors` folder

## Downpatching
It is required to downpatch Vampire Survivors to make it work with the Apworld.
1. Type steam://nav/console in your browser console.
2. Enter the following download_depot command for the base game: ``download_depot 1794680 1794681 5861904299865288168``
3. Once downloaded, head to the directory given by the console.
4. Copy the contents.
5. Paste it in your original Folder.
6. Repeat steps 2 through 5 for each DLC you own.
  - Legacy of the Moonspell: download_depot 2230760 2230761 1888202607405303318
  - Tides of the Foscari: download_depot 2313550 2313551 638877543388105171
  - Emergency Meeting: download_depot 2690330 2690331 948012419207925656
  - Operation Guns: download_depot 2887680 2887681 4895670754162177291
  - Ode to Castlevania: download_depot 3210350 3210351 7384108667486945195
  - Emerald Diorama: download_depot 3451100 3451101 6733844109130581063
7. Enjoy and don't forget to not update your game until the plugin is fixed!


## Debug Steps
- When downpatching and messing with melon install/reinstall/uninstall
- Double/triple/quadruple check the mod folder, melon might rename it to `~SW_CreeperKing.ArchipelagoSurvivors` which will prevent the mod from loading correctly
