# Setup Guide for Twilight Princess MultiworldGG

Welcome to Twilight Princess MultiworldGG! This guide will help you set up the randomizer and play your first multiworld.
Whether playing, generating, or hosting an Archipelago room with Twilight Princess, you must follow a few simple steps to
get started.

Unfortunately, Mac OS is not officially supported at this time.

## Requirements

You'll need the following components to be able to play/generate with Twilight Princess:

- Install [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases) v0.7 or higher.\
   **Make sure to install the Generator if you intend to generate multiworlds.**
- If you want to use AP: The latest version of the [Twilight Princess APWorld](https://github.com/WritingHusky/twilight_princess/releases/latest).

If you're playing Twilight Princess, you'll also need:

- Install [Dolphin Emulator](https://dolphin-emu.org/download/).\
   **We recommend using the latest release.**
- A legaly obtained Twilight Princess ISO.

If you intend to play under Linux, you will need to consider the following information.

- Grab the `tar.gz` version of MultiworldGG, not the `AppImage`. The file name should be similar to the following on the
  release page: `Archipelago_X.X.X_linux-x86_64.tar.gz`.
- For Dolphin, you can use the flatpak package
  [available on Flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu).

## Installation (Archipelago only)

All users should follow these steps:

1. Unzip the downloaded Twilight Princess APWorld zip file.
2. Double-click the `twilight_princess.apworld` file. It should automatically install the APWorld after a little while. You will get a
   little dialog window telling you it has been installed successfully. \* Alternatively, copy the `twilight_princess.apworld` to your Archipelago installation's `custom_worlds` folder (Windows default
   to: `%programdata%/Archipelago`).

### Note: If you have a previous version of the apworld you will need to remove it.

If you're playing Twilight Princess, you must also download the REL loader from https://tprandomizer.com/downloads/ and place it in the save data of dolphin (See [Placing the files](https://github.com/WritingHusky/Twilight_Princess_apworld/blob/main/docs/setup_en.md#Placing-the-files)).

## Setting Up a YAML

All players playing Twilight Princess must provide the room host with a YAML file containing the settings for their world.
The TP APWorld download includes a sample YAML file for Twilight Princess. The comments in that file explain each
setting's function.

Once you're happy with your settings, provide the room host with your YAML file and proceed to the next step.

## Generating a Multiworld

If you're generating a multiworld game that includes Twilight Princess, you'll need to do so locally as the online
generator does not yet support Twilight Princess. Follow these steps to generate a multiworld:

1. Gather all player's YAMLs. Place these YAMLs into the `Players` folder of your MultiworldGG installation. If the
   folder does not exist, then it must be created manually. The files here should not be compressed.
2. Modify any local host settings for generation, as desired.
3. Run `MultiworldGGGenerate.exe` (without `.exe` on Linux) or click `Generate` in the launcher. The generation output
   is placed in the `output` folder (usually named something like `AP_XXXXX.zip`). \* Please note that if any player in the game you want to generate plays a game that needs a ROM file to generate,
   you will need the corresponding ROM files. A ROM file is not required for Twilight Princess at this stage.
4. Unzip the `AP_XXXXX.zip` file. It should include a `.aptp` file for each player in the room playing Twilight Princess.
   Each file will be named `AP_XXXXX_P#_<name>.aptp`, where `#` corresponds to that player's slot number and `<name>` is
   their slot (player) name. The `.aptp` is used to create a seed file. This will be explained shortly.
5. In the next section, use the archive file `AP_XXXXX.zip` to host a room or provide it to the room host.

## Hosting a Room

If you're generating the multiworld, follow the instructions in the previous section. Once you have the zip file
corresponding to your multiworld, follow
[these steps](/tutorial/Archipelago/setup/en#hosting-a-multiworldgg-server) to host a room. Follow
the instructions for hosting on the website from a locally generated game or on a local machine.

## Generating a Seed File

In order to connect to a room you will need the seed file for the world.
You will need the `.aptp` file created during generation. If your multiworld is hosted on a MultiworldGG webserver you can download the patch from there or ask the host for your file.

1. Visit https://ap.tprandomizer.com/
2. Choose to randomize cosmetics / audio as you wish.
3. Upload `.aptp` file to the "AP File Upload" Section.
4. Press "Get Download Link" and download the file.
5. If you dont yet have the REL loader downloaded, download it at the bottom of the page (Note that it is region specific i.e. NA, PAL, and JP).

If you would like to patch your game instead of using a seed, before downloading, upload your ISO and select Patch ISO. Then you can place the patched ISO wherever your vanilla ISO is.

## Placing the files

You should now have a seed and REL Loader file.

1. Ensure that GCI Folder is the selected method. You can check this by going to 'Options > Configuration > Gamecube > Device Settings' Slot A should be selected as GCI Folder.
    - Note: If you see a folder path under the Slot A drop down that is the folder you should put the file in.
2. Now you will want to find where your dolphin is installed. By deafualt this is in `C:\Users\[your username]\AppData\Roaming\Dolphin Emulator`
3. Travse to `Dolphin Emulator\GC\USA\Card A` and place your files there.
4. If you see a file named `01-GZ2E-gczelda2.gci` that is your vanilla save data. You will need to remove / delete it.

## Connecting to a Room

Before connecting make sure you have created and placed your seed file.

Once you do, follow these steps to connect to the room:

1. Open Dolphin and use it to open Twilight Princess. (Ensure `Enable Emulated Memory Size Override` is disabled. See troubleshooting for more details)
2. Start the REL loader save file and select APTest as the seed you want to use.
   The game will restart if you press 'R + Z' a console will pop up and it should say "Archipelego Randomizer - v1.3" at the top
3. Start a new save file and leave links name as default, it will change when you begin.
4. Start `MultiworldGGLauncher.exe` (without `.exe` on Linux) and choose `Twilight Princess Client`, which will open the
   text client. It should automatically connect to Dolphin.
5. You will see a message saying "Randomizer loaded .... Using Seed ID [Seed name] that is the name of the current seed.
6. Connect to the room by entering the server name and port number at the top and pressing `Connect`. For rooms hosted
   on the website, this will be `multiworld.gg:<port>`, where `<port>` is the port number. If a game is hosted from the
   `MultiworldGGServer.exe` (without `.exe` on Linux), this will default to `38281` but may be changed in the `host.yaml`.
7. If the incorrect seed was loaded a message will appear with the name of the seed you are supossed to load.

## Troubleshooting

- Ensure that you are running version v0.7 or higher of MultiworldGG, and the latest version of the world.
- If you do not see the client in the launcher, ensure the `Twilight Princess.apworld` file is in the correct folder (the
  `custom_worlds` folder of your Archipelago installation).
- If the client says that seed version and client version do not match, it is recomended regenerate the seed with the current version.
  Differences in version can cause bugs which may make it unplayable.
- If the client throws an error along the lines of "could not read memory at < some-number >", dolphin has been disconnected.
  It should automaticly reconnect, so ensure that dolphin is open and running
- Ensure that you do not have any Dolphin cheats or codes enabled. Some cheats or codes can unexpectedly interfere with
  emulation and make troubleshooting errors difficult.
- If Dolphin is not connecting, ensure that `Enable Emulated Memory Size Override` in Dolphin (under `Options` >
  `Configuration` > `Advanced`) is **disabled**.
- If you run with a custom GC boot menu, you'll need to skip it by going to `Options` > `Configuration` > `GameCube`
  and checking `Skip Main Menu`.
- If Dolphin does load the RELoader save file and has a popup saying something like "Save file cannot be loaded",
  There may be a normal save file in your dolphin save folder, this will need to be removed in order for the randomizer to load.
- If you have killed Ganon but the world has not been realesed. Ensure that the host settings allows player releases.
  Check that the Archipelego Randomizer is loaded by bringing up the console window.
