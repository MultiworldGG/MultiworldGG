# Slime Rancher Setup Guide

## Requirements

1. Install [.NET 6.0](https://dotnet.microsoft.com/en-us/download/dotnet/6.0).
2. Download and install [Melon Loader](https://melonwiki.xyz/#/?id=automated-installation). Use Melon Loader version 7.1, not 7.2.

The default Steam installation directory is `C:\\Program Files (x86)\\Steam\\steamapps\\common\\Slime Rancher`.

## Install Slimipelago

1. Launch Slime Rancher once, then close it to finish the Melon Loader installation. If this does not complete correctly, antivirus or anti-malware software may be interfering.
2. Download and extract `Slimipelago.zip` from the [latest Slimipelago release](https://github.com/SWCreeperKing/Slimipelago/releases).
3. Copy the extracted `Mods` and `UserLibs` folders into the Slime Rancher game directory.
4. Confirm that the mod DLL is at `Slime Rancher/Mods/Slimipelago.dll`.
5. Launch the game again. The usual New Game and Load Game options should no longer appear; instead, an Archipelago connection menu is available in the options.

If Melon Loader works but the mod does not load, check that the mod folder is not named `~SW_CreeperKing.Slimipelago`. Remove the leading `~` if it is present. This mod will most likely not work with SRModLoader.

## Connect and play

Use the Archipelago connection menu in the game's options. You cannot create or load a save before connecting, and only saves created with the same seed are shown.

## Uninstall

Remove the `Mods/SW_CreeperKing.Slimipelago` folder.
