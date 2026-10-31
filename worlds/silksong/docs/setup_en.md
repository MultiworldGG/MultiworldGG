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

**Cogfly Import Code:** `01a15150-4496-f47c-5102-41aae48899c7` (Same as R2Modman)

### Using R2Modman (3.2.18+) / Thunderstore Manager (1.123.1+)
1.) First start off by installing [R2Modman](https://r2modman.com/download-latest/) to the latest version for your preferred operating system.

2.) Select Hollow Knight: Silksong in the Game Selection Menu and select your Silksong storefront.

3.) In profile selection, select 'Import / Update', select 'From code', and enter the following profile code. 

The profile code contains the Archipelago Randomizer Mod, Custom Music Randomizer, Crest Wheel, Silksong Archip Display, Recent Items Display, Mod Menu, Mod List, and all other dependencies (CanvasUtil, DataManager, FsmUtil, I18N, BepInExPack_Silksong, Monodeteour_BepInEx_5, UnityHelper, MonoDetour, WavLib).

**NOTE: Please make sure to press "Update Mods" when installing or when new versions release and it'll automatically update you to the latest version of the mod.**

**R2Modman Import Code:** `01a15150-4496-f47c-5102-41aae48899c7` (Same as Cogfly)

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

4.) You can then generate a options configuration for yourself using one of the following two methods:

  - Press the "Options Creator" on the Launcher. Select Hollow Knight: Silksong on the left hand side of the screen that pops up and select all your preferred options. Finally, press export options and save it.

  - Press the "Generate Template Options" on the Launcher which will create .yaml's for all your installed .apworlds. Look for the 'Hollow Knight Silksong.yaml' file, this will be the file you edit for your options.

5.) Take the file that you generated in step 4 and place it in your MultiworldGG 'Players' folder alongside any other yaml that you will be using for your multiworld.

6.) Go back to the MultiworldGG Launcher and press generate. A script will run that will generate your multiworld seed and place a .zip file into your MultiworldGG 'output' folder.

7.) You can then upload the zip to host the game as you wish. MultiworldGG's upload hosting page can be found [here](/uploads).

## Frequently Asked Questions (FAQ)

### I Got to Act 3 and Missed Some Checks in Act 2?
Some items become unavailable once you enter Act 3. Go to your Bellhome in Bellhart. 
Once you reach act 3 once, sit on the bed, press dash + needolin to get a pop-up asking to revert the world back to Act 2 and vice versa.

### What Are the Map Markers Showing?
When enabled in the yaml "location_map_markers", the map can show randomized locations at their physical locations.

Key for these markers are as follows:
- **Fully opaque (with AP style rosary icon)**: Reachable / in logic.
- **Half transparent (with AP style rosary icon)**: Not reachable / not in logic.
- **? / inverted icons**: Missing logic so far / guaranteed junk.

### I’m Stuck Somewhere, What Do I Do?
**Press F4.**

Seriously. It allows warping to homepoints like Bone Bottom, Bellhart, and Songclave as you reach them, skips the widow cutscene to stop softlocks and can save you from the slab. 
Also you can press F3 and it'll allow changing of warp locations as of v0.4.3.

### Do You Have a Feature like Benchwarp?
Short answer, no. Please refer to I’m stuck somewhere, what do I do?

Long answer, it can cause softlocks and other issues, it can be used but at your own risk of issues and potential woodchipper related incidents.

### I Got An Error Saying My APWorld Version is Incompatible
This occurs when you've changed your APWorld to a new version for an update while having your world generated on an old one.

Use one of the installation methods to downgrade. Manual is preferred for downgrading but here are some old codes for the mod managers.

Given that Cogfly has some issues currently with import codes, you can downgrade manually by pressing the link attached to the version numbers below and then follow the steps. 

Alternatively, you can always replace Cogfly with a different mod manager that allows for downgrading. Downgrading on those mod managers can typically be done by uninstalling the mod and then reinstalling it and selecting the appropriate version to your generated run.

1.) Go to your BepInEx plugins folder, depending on your install this is located in one of two places. 
   - For a manual installation it should be in your game directory. 
   - For a mod manager, you want to go into the profile folder. For R2ModMan, this is in "Settings > Profile Folder". For Cogfly, go into the profile and press "Open Profile Folder".

2.) Go into BepInEx. Go into plugins. Go into the Silksong Randomizer folder this can also be named "BatAtVideoGames-SilksongArchipelagoRandomizer". A file named "SilksongRandomizer.dll" will be present in the folder, you want to replace this file using the version in one of the .rar files from below.

3.) Start up your game normally after replacing and you should be able to connect once again.

[**v0.5.2**](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/tag/v0.5.2) Import Code: `01a15150-4496-f47c-5102-41aae48899c7`

[**v0.5.1**](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/tag/v0.5.1) Import Code: `01a12cf3-f4cb-5402-d6a8-0f266b3e7aa8`

[**v0.5.0**](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/tag/v0.5.0) Import Code: `01a109ba-4c4f-b4f0-8695-8b4d42cb8159`

[**v0.4.7**](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/tag/v0.4.7) Import Code: `01a0dfd5-7d5b-682a-324c-6e2f385ad7df`

[**v0.4.6**](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/tag/v0.4.6) Import Code: `01a0b6c0-a24b-cc11-7b3e-ba412942686b`

[**v0.4.52**](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/tag/v0.4.5-Hotfix2) Import Code: `01a0926a-7b73-7a11-66bb-42117f64248f`

[**v0.4.51**](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/tag/v0.4.5-Hotfix) Import Code: `01a0926b-eab2-0a1b-bf2c-76345f9973d3`

[**v0.4.5**](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/tag/v0.4.5) Import Code: `01a0926c-50d2-f57d-ea27-e6261857cd3d`

[**v0.4.4**](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/tag/v0.4.4) Import Code: `01a07254-1646-8e29-7cee-2ba65c34300d`

[**v0.4.3**](https://github.com/Batatvideogames/silksong-archipelago-randomizer/releases/tag/v0.4.3) Import Code: `01a07252-fdcb-41ae-1ea2-84fb05e3f1e5`

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

## Feedback and Bug Reports

Please report bugs and logic issues through the repository's [issues](https://github.com/Batatvideogames/silksong-archipelago-randomizer/issues) page. Include enough information to reproduce the problem, but do not upload save files containing personal information.

A second place to give this feedback can be this [Google Form](https://forms.gle/bAsQ2o453eccpL2i7).

A [Trello board](https://trello.com/b/as8YLuLA/skonging) is also available to post known bugs, what's been fixed, and what's upcoming.

## Support and Additional Information

The best place to get any further support would be [Archipelago's Discord](https://discord.gg/archipelago) where you can access the [Hollow Knight: Silksong (Batsong Implementation)](https://discord.com/channels/731205301247803413/1540758118361727056) channel. 

This is a reminder that this is a passion project and people will try to help to the best of their ability but as always, please be respectful.

## Credits

A huge thanks goes out to all that support the channel and thread, the logic mapping team, playtesters, mod developers, and others who have helped contribute to this project:

### Logic Mapping

Some of these regions are still incomplete and still being mapped out. They've been placed in UNMAPPED.

| Contributor | Regions |
| :--- | :--- |
| **Gallos** | [Choral Chambers](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/choral-chambers) |
| **Herchey** | [Bilewater](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/bilewater), [Sinner's Road](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/sinner-s-road) |
| **Heric** | [Memorium](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/memorium) |
| **Hero** | [Bone Bottom](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/bone-bottom), [Deep Docks](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/deep-docks), [Far Fields](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/far-fields), [Hunter's March](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/hunter-s-march), [Moss Grotto](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/moss-grotto), [The Marrow](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-marrow), [Weavenest Atla](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/weavenest-atla), [Wormways](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/wormways) |
| **Isssma** | [Greymoor](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/greymoor) |
| **Maya** | [The Slab](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-slab)
| **Pyxl** | [Bellhart](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/bellhart), [Grand Gate](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/grand-gate), [Mount Fay](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/mount-fay), [Putrified Ducts](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/putrified-ducts), [Sands of Karak](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/sands-of-karak), [Shellwood](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/shellwood), [The Abyss](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-abyss), [The Cradle](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-cradle), [Verdania](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/verdania) |
| **Rebel** | [Cogwork Core](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/cogwork-core), [Underworks (East)](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/underworks), [Whispering Vaults](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/whispering-vaults) |
| **Sergio** | [Choral Chambers](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/choral-chambers), [Grand Gate](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/grand-gate), [High Halls](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/high-halls), [The Slab](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-slab), [Underworks (West)](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/underworks), [Wisp Thicket](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/whisp-thicket) |
| **Skai** | [Blasted Steps](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/blasted-steps), [Grand Gate](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/grand-gate), [Whiteward](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/whiteward)|
| **SuperEpicGuy** | [Moss Grotto](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/moss-grotto) |
| **UNMAPPED** | [The Mist](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-mist), [Red Memory](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/red-memory) |

### Contributors
A huge thanks to all the people who have contributed to this project including ones that aren't displayed on the contributors list.

<a href="https://github.com/Batatvideogames/silksong-archipelago-randomizer/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Batatvideogames/silksong-archipelago-randomizer" />
</a>

- [HeroUnit](https://github.com/zerounit-dev) for his great work on standardizing logic for this project and largely handling all logical coordination.
- [TheMathGeek314](https://github.com/TheMathGeek314) for the original [HK Alphabet Rando](https://github.com/TheMathGeek314/AlphabetRando) and for giving permission to extend their idea to Silksong.
- [Nix](https://github.com/Nix-main) for [SilksongArchiDisplay](https://github.com/Nix-main/SilksongArchiDisplay) and all the additional help with [Cogfly](https://github.com/Nix-main/Cogfly) support.
- [FarisTheAncient](https://github.com/FarisTheAncient) for a ton of help with archipelago compliance and consistent help with making things work with [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases?q=Tracker).
- RainingChain and IdoManti for their incredible work on documenting Silksong's map and providing us the image files to be used for UT and our logic tool. The map can be found on [Scripter's War](https://scripterswar.com/silksong/map).