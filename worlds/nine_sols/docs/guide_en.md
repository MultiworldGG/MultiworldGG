# Nine Sols Setup Guide

## Prerequisites

- Make sure you have Nine Sols installed
	- The "speedrun branch" is not supported. Current/latest patch only.
- Install [r2modman](https://r2modman.net/#Download_R2modman_Latest_Version)
- Install the core MultiworldGG tools (at least version 0.7, but preferably the latest version) from [MultiworldGG's Github Releases page](https://github.com/MultiworldGG/MultiworldGG/releases). On that page, scroll down to the "Assets" section for the release you want, click on the appropriate installer for your system to start downloading it (for most Windows users, that will be the file called `Setup.MultiworldGG.X.Y.Z.exe`), then run it.
- If you are not using MultiworldGG, go to [the Releases page](https://github.com/Ixrec/NineSolsArchipelagoRandomizer/releases) of this repository and look at the latest release. There should be three files: A .zip, an .apworld and a .yaml. Download the .apworld and the .yaml.

## MultiworldGG tools setup

- Go to your MultiworldGG installation folder. Typically that will be `C:\Program Files\MultiworldGG`.
- Put the `Nine.Sols.yaml` file in `MultiworldGG\Players`. You may leave the `.yaml` unchanged to play on default settings, or use your favorite text editor to read and change the settings in it.
- If you are not using MultiworldGG: Double click on the `nine_sols.apworld` file. AP should display a popup saying it installed the apworld. Optionally, you can double-check that there's now an `nine_sols.apworld` file in `Archipelago\custom_worlds\`.

### I've never used MultiworldGG before. How do I generate a multiworld?

Let's create a randomized "multiworld" with only a single Nine Sols world in it.

- Make sure `Nine.Sols.yaml` is the only file in `MultiworldGG\Players` (subfolders here are fine).
- Double-click on `MultiworldGG\MultiworldGGGenerate.exe`. You should see a console window appear and then disappear after a few seconds.
- In `MultiworldGG\output\` there should now be a file with a name like `AP_95887452552422108902.zip`.
- Open https://multiworld.gg/uploads in your favorite web browser, and upload the output .zip you just generated. Click "Create New Room".
- The room page should give you a hostname and port number to connect to, e.g. "multiworld.gg:12345".

For a more complex multiworld, you'd put one `.yaml` file in the `\Players` folder for each world you want to generate. You can have multiple worlds of the same game (each with different options), as well as several different games, as long as each `.yaml` file has a unique player/slot name. It also doesn't matter who plays which game; it's common for one human player to play more than one game in a multiworld.

## Modding and Running Nine Sols

- In r2modman, create a profile and select the Nine Sols game. Then go to the "Mods" > "Online" section and search for "Archipelago Randomizer". Click on it to expand the listing, and click the Download button that appears (if you were wondering about the .zip file we didn't download earlier, that's what r2modman is installing).
- Now click the "Start modded" button in the top left corner. Note that you must launch Nine Sols through r2modman in order for the mods to be applied; launching from Steam won't work.
- Once you're at the main menu of Nine Sols itself, click "Start Game", click on an empty save slot, and you will be asked for connection info such as the hostname and port number. Unless you edited `Nine.Sols.yaml` (or used multiple `.yaml`s), your slot/player name will be "Solarian1". And by default, multiworld.gg rooms have no password.

### What if I want to run a pre-release version for testing, or downgrade to an older version of this mod (so I can finish a longer async)?

<details>
<summary>Click here to show instructions</summary>

To use an older or pre-release version, you'll need to install a `Ixrec-ArchipelagoRandomizer-X.Y.Z.zip` manually. This repo's Releases page should have all the `.zip`s for different versions of the mod.

Once you have the `.zip` you want:
- In r2modman, go to "Other" > "Settings"
- Scroll down to "Import local mod" and click on it
- Click "Select file" and navigate to the mod `.zip`

</details>

## Client/Mod Settings

The client-side settings currently in the randomizer mod are:

- Boss Scaling
- Force True Eigong
- Death Link
- Flowerless Death Link
- Show AP Messages
- Filter By Player

More details can be found in the settings menu tooltips. Press F1 in-game to bring up the settings menu for all of your Nine Sols mods, including the randomizer. This F1 menu comes from the [BepinExConfigurationManager](https://thunderstore.io/c/nine-sols/p/ninesolsmodding/BepinExConfigurationManager/) mod.