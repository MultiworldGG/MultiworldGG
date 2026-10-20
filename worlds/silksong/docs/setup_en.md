# Silksong MultiworldGG Randomizer

An AP/MultiworldGG randomizer for *Hollow Knight: Silksong*.

It randomizes Silksong checks and items into a MultiworldGG multiworld, allowing several players to share item progression across supported games. The randomizer includes progression items, useful items, filler, and traps, with in-game map and item feedback to help track the run.

This project is currently being tested and improved. Expect occasional bugs or logic changes between releases.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [What is randomized?](#what-is-randomized)
- [Requirements and Installation](#requirements-and-installation)
  - [Installation with Cogfly](#using-cogfly-125)
  - [Installation with R2Modman / Thunderstore Manager](#using-r2modman-3218--thunderstore-manager-11231)
  - [Manual Installation](#manually)
- [MultiworldGG Setup](#multiworldgg-setup)
- [Frequently Asked Questions (FAQ)](#frequently-asked-questions-faq)
- [Support and Additional Information](#support-and-additional-information)
- [Credits](#credits)
  - [Logic Mapping](#logic-mapping)
  - [Contributors](#contributors)

## What is randomized?

The world can randomize Silksong checks and progression items, including movement abilities, tools, crests, maps, mask shards, silk skills, fleas, and other useful or filler items. Traps may also be enabled depending on the generation settings.

The exact checks and options available can change as the randomizer develops. Use the generated YAML template and the release notes for the current version.


## Requirements and Installation

- *Hollow Knight: Silksong* on PC
- BepInEx configured for Silksong
- MultiworldGG (v0.7.200+)

There are multiple installation methods due to different issues with each of them at times, follow one of the methods below to install the MultiworldGG randomizer.

### Using Cogfly (1.2.5+)
1.) First start off by installing [Cogfly](https://github.com/Nix-main/Cogfly/releases/latest) to the latest version for your preferred operating system.

2.) Launch Cogfly and go to settings and make sure your path to your Silksong installation are valid.

3.) Go to profiles, select import from code, and enter the following profile code. 

The profile code contains the Archipelago Randomizer Mod, Custom Music Randomizer, Crest Wheel, Silksong Archip Display, Recent Items Display, Mod Menu, Mod List, and all other dependencies (CanvasUtil, DataManager, FsmUtil, I18N, BepInExPack_Silksong, Monodeteour_BepInEx_5, UnityHelper, MonoDetour, WavLib).

> [!WARNING]
> If you get an error when importing a code into Cogfly, especially the error below, refer to [here](#cogfly---getting-a-server-returned-http-response-code-502-error):
> 
> **Server returned HTTP response code: 502 for URL**

**NOTE: Please make sure to press "Update Mods" when installing or when new versions release and it'll automatically update you to the latest version of the mod.**

**Cogfly Import Code:** `01a12cf3-f4cb-5402-d6a8-0f266b3e7aa8` (Same as R2Modman)

### Using R2Modman (3.2.18+) / Thunderstore Manager (1.123.1+)
1.) First start off by installing [R2Modman](https://r2modman.com/download-latest/) to the latest version for your preferred operating system.

2.) Select Hollow Knight: Silksong in the Game Selection Menu and select your Silksong storefront.

3.) In profile selection, select 'Import / Update', select 'From code', and enter the following profile code. 

The profile code contains the Archipelago Randomizer Mod, Custom Music Randomizer, Crest Wheel, Silksong Archip Display, Recent Items Display, Mod Menu, Mod List, and all other dependencies (CanvasUtil, DataManager, FsmUtil, I18N, BepInExPack_Silksong, Monodeteour_BepInEx_5, UnityHelper, MonoDetour, WavLib).

**NOTE: Please make sure to press "Update Mods" when installing or when new versions release and it'll automatically update you to the latest version of the mod.**

**R2Modman Import Code:** `01a12cf3-f4cb-5402-d6a8-0f266b3e7aa8` (Same as Cogfly)

### Manually
1.) Find your Hollow Knight: Silksong installation folder based on your Silksong storefront.

2.) Download the latest release of [BepInEx](https://github.com/BepInEx/BepInEx/releases) for your preferred operating system.

3.) Drag all the contents of the BepInEx zip file that you downloaded into your Silksong game folder where the game's .exe resides.

4.) Launch Silksong once for the BepInEx files to initialize and then close the game.

5.) Download the Silksong Randomizer's [latest release](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/latest) .rar file.

6.) There will be a folder named "PUT IN SILKSONG FOLDER" with a 'BepInEx' folder inside it. Drag the 'BepInEx' folder from the zip file into your Silksong installation folder. This will merge or prompt you to merge the folders which is what you want to do.

The resulting folder structure should look something like:

```
- 📂 BepInEx
  | - 📂 plugins
    | - 📂 Silksong Randomizer
  | - 📂 config
  | - 📂 core
  | - 📂 patchers
- 📂 D3D12
- 📂 Hollow Knight Silksong_Data
- 📂 MonoBleedingEdge
- 📜 Hollow Knight Silksong.exe
```

 **OPTIONAL**: If you want any of the other additional mods mentioned, you can find them on Thunderstore, download them, and place them into the 'plugins' folder found in the 'BepInEx' folder in your Silksong game installation folder.

## MultiworldGG Setup

1.) Download the [MultiworldGG Launcher](https://github.com/MultiworldGG/MultiworldGG/releases/latest) for your preferred operating system.

2.) If you want to use AP: Download the Silksong Randomizer's [latest release](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/latest) .apworld file.

2a.) Launch the Archipelago Launcher and drag the .apworld file into the client. Restart the Archipelago Launcher after installing the apworld.

3.) You can then generate a options configuration for yourself using one of the following two methods:

  - Press the "Options Creator" on the Launcher. Select Hollow Knight: Silksong on the left hand side of the screen that pops up and select all your preferred options. Finally, press export options and save it.

  - Press the "Generate Template Options" on the Launcher which will create .yaml's for all your installed .apworlds. Look for the 'Hollow Knight Silksong.yaml' file, this will be the file you edit for your options.

4.) Take the file that you generated in step 4 and place it in your MultiworldGG 'Players' folder alongside any other yaml that you will be using for your multiworld.

5.) Go back to the MultiworldGG Launcher and press generate. A script will run that will generate your multiworld seed and place a .zip file into your MultiworldGG 'output' folder.

6.) You can then upload the zip to host the game as you wish. MultiworldGG's upload hosting page can be found [here](/uploads).

## I Got An Error Saying My APWorld Version is Incompatible
This occurs when you've changed your APWorld to a new version for an update while having your world generated on an old one.

Use one of the installation methods to downgrade. Manual is preferred for downgrading but here are some old codes for the mod managers (these work for both):

**v0.5.1** Import Code: `01a12cf3-f4cb-5402-d6a8-0f266b3e7aa8`

**v0.5.0** Import Code: `01a109ba-4c4f-b4f0-8695-8b4d42cb8159`

**v0.4.7** Import Code: `01a0dfd5-7d5b-682a-324c-6e2f385ad7df`

**v0.4.6** Import Code: `01a0b6c0-a24b-cc11-7b3e-ba412942686b`

**v0.4.52** Import Code: `01a0926a-7b73-7a11-66bb-42117f64248f`

**v0.4.51** Import Code: `01a0926b-eab2-0a1b-bf2c-76345f9973d3`

**v0.4.5** Import Code: `01a0926c-50d2-f57d-ea27-e6261857cd3d`

**v0.4.4** Import Code: `01a07254-1646-8e29-7cee-2ba65c34300d`

**v0.4.3** Import Code: `01a07252-fdcb-41ae-1ea2-84fb05e3f1e5`

### My Mod Manager Boots The Game In Vanilla
For **Cogfly**, press 'Copy Launch Arguments' at the top. Go to Hollow Knight: Silksong on Steam, right-click and press "Properties...". In Launch Options, paste the the arguments Cogfly copied for you and start your game.

If this still doesn't work, make sure your Silksong folder doesn't have any BepInEx files (folder and doorstop files) from the manual installation. This *can* conflict with the mod managers and Cogfly will place these back for you.

Worst case scenario, delete your Silksong folder, reinstall it using Verify Integrity of Game Files, relaunch Cogfly, then import the a new profile with one of the codes.

### Cogfly - Getting a Server Returned HTTP Response Code 502 Error
This has been happening for a little bit where it seems that Cogfly is having a connection issue with Thunderstore. 
Try manually installing the mod list using the photo below, [swap to R2Modman](https://github.com/Batatvideogames/silksong-archipelago-randomizer#using-r2modman-3218--thunderstore-manager-11231) using the same code, or try a [manual install](https://github.com/Batatvideogames/silksong-archipelago-randomizer#manually).
<img width="1377" height="506" alt="image" src="https://github.com/user-attachments/assets/dcc2824c-d762-4300-8aac-1493a651054d" />

### Additional common issues or troubleshooting steps to take

- If Silksong does not connect, confirm that BepInEx is installed correctly and that the plugin is in the `BepInEx/plugins` folder.
- If the Silksong world does not appear in Archipelago, confirm that the `.apworld` is in `custom_worlds` and restart the Archipelago launcher.
- If items or checks appear out of sync, reconnect the client or use the client's resynchronization command if available.
- If reporting a bug, include the randomizer version, MultiworldGG version, relevant YAML settings, and the BepInEx log.
