# Outer Wilds Setup Guide

## Prerequisites

- Make sure you have Outer Wilds installed
- Install the [Outer Wilds Mod Manager](https://outerwildsmods.com/mod-manager/)
- Install the core MultiworldGG tools (at least version 0.7.0, but preferably the latest version) from [MultiworldGG's Github Releases page](https://github.com/MultiworldGG/MultiworldGG/releases). On that page, scroll down to the "Assets" section for the release you want, click on the appropriate installer for your system to start downloading it (for most Windows users, that will be the file called `Setup.MultiworldGG.X.Y.Z.exe`), then run it.

## MultiworldGG tools setup

- Go to your MultiworldGG installation folder. Typically that will be `C:\Program Files\MultiworldGG`.
- Put the `Outer.Wilds.yaml` file in `MultiworldGG\Players`. You may leave the `.yaml` unchanged to play on default settings, or use your favorite text editor to read and change the settings in it.
- Not necessary if you use MultiworldGG: Double click on the `outer_wilds.apworld` file. Archipelago should display a popup saying it installed the apworld. Optionally, you can double-check that there's now an `outer_wilds.apworld` file in `Archipelago\custom_worlds\`.

### I've never used MultiworldGG before. How do I generate a multiworld?

Let's create a randomized "multiworld" with only a single Outer Wilds world in it.

- Make sure `Outer.Wilds.yaml` is the only file in `MultiworldGG\Players` (subfolders here are fine).
- Double-click on `MultiworldGG\MultiworldGGGenerate.exe`. You should see a console window appear and then disappear after a few seconds.
- In `MultiworldGG\output\` there should now be a file with a name like `AP_95887452552422108902.zip`.
- Open https://multiworld.gg/uploads in your favorite web browser, and upload the output .zip you just generated. Click "Create New Room".
- The room page should give you a hostname and port number to connect to, e.g. "multiworld.gg:12345".

For a more complex multiworld, you'd put one `.yaml` file in the `\Players` folder for each world you want to generate. You can have multiple worlds of the same game (each with different options), as well as several different games, as long as each `.yaml` file has a unique player/slot name. It also doesn't matter who plays which game; it's common for one human player to play more than one game in a multiworld.

## Modding and Running Outer Wilds

- In the Outer Wilds Mod Manager, click on "Get Mods", search for "Archipelago Randomizer", and once you see this mod listed, click the install button to the right of it (if you were wondering about the .zip file we didn't download earlier, that's what the Mod Manager is installing).
- (**Optional: Other Mods**) Some other mods that I personally like to play with, and that this randomizer is compatible with, include: "Clock" (exactly what it sounds like), "Cheat and Debug Menu" (for its fast-forward button), and "Suit Log" (access the ship log from your suit).
- Now click the big green Run Game button. Note that you must launch Outer Wilds through the Mod Manager in order for the mods to be applied; launching from Steam won't work.
- Once you're at the main menu of Outer Wilds itself, make sure your current profile / save file is one you're fine with overwriting. If you aren't sure: click Switch Profile to see a menu with all of your existing profiles, as well as the option to create a brand new profile. Return to the main menu when you're sure you're on the profile you want.
- Now click "New Random Expedition", and you will be asked for connection info such as the hostname and port number. Unless you edited `Outer.Wilds.yaml` (or used multiple `.yaml`s), your slot/player name will be "Hearthian1". And by default, multiworld.gg rooms have no password.

### What if I want to run a pre-release version for testing, or downgrade to an older version of this mod (so I can finish a longer async)?

<details>
<summary>Click here to show instructions</summary>

To use a pre-release version:

- In the Mod Manager, go to the "Get Mods" section (**not** "Installed Mods")
- Search for "Archipelago Randomizer", click the 3 dots icon next to this mod, and select the "Use Prerelease ..." option

To downgrade to an older version, you'll need to install a `Ixrec.ArchipelagoRandomizer.zip` manually. This repo's Releases page has all the mod `.zip`s for past releases (and the current release `.zip`, which is what the Mod Manager normally downloads for you).

- In the Mod Manager, click the 3 dots icon at the top of the window, and select the "Install From" option
- In this popup, make sure the "Install From" mode on top is set to "URL"
- Go to [this repo's Releases page](https://github.com/Ixrec/OuterWildsArchipelagoRandomizer/releases) and copy the link address to one of the `Ixrec.ArchipelagoRandomizer.zip` files from a previous release. For example, the 0.1.1 .zip link would be "https://github.com/Ixrec/OuterWildsArchipelagoRandomizer/releases/download/v0.1.1/Ixrec.ArchipelagoRandomizer.zip".
- Back in the Mod Manager popup, paste this link into the "URL" entry below, and click Install.

Either way, the Mod Manager should immediately display the version number of the mod version you installed. Be careful not to click the Fix Issues button until you want to go back to the latest stable mod version.
</details>
