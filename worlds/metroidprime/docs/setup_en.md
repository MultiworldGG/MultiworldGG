# Setup Guide for Metroid Prime MultiworldGG

This guide is meant to help you get up and running with Metroid Prime APWorld with MultiworldGG.
This has only been tested on Windows, but feel free to let us know if you get the chance to try it on other OS platforms!

## Requirements

The following are required in order to play _Metroid Prime_ in MultiworldGG:

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases)
- Latest Release of [Dolphin Emulator](https://dolphin-emu.org/download/) or [PrimeHack](https://github.com/shiiion/dolphin/releases)
- A _Metroid Prime_ (GameCube version) ISO file
  - Any official release copy of the GameCube version will work. (All region versions are compatible, including all three versions of NTSC-USA)
  - The Wii and Switch version of the game are _not_ supported.
  - This must be dumped from your own disc.

## APWorld Installation
* These steps are not required if you are using MultiworldGG.

1. Download the latest version of the [Metroid Prime AP](https://github.com/UltiNaruto/MetroidAPrime/releases/latest)
2. Unzip the downloaded Metroid Prime APWorld zip file and extract its files.
3. In the AP Launcher, select `Install APWorld`, and then select `metroidprime.apworld` file from the previous step.

## Setting Up Player Options YAML File

All players participating must provide the room host with a YAML file containing the player options for their world.

After installing Metroid Prime AP, in the MultiworldGG Launcher, select `Generate Template Options`.
When it is finished, `Metroid Prime.yaml` will appear inthe Templates folder.
Edit the options in this file to your liking and then send a copy of it to the room host.

## Generating a Multiworld
As usual, randomized MultiworldGG games with custom worlds must be generated locally - see [MultiworldGG Setup Guide: Generating a game - On your local installation](/tutorial/Archipelago/setup/en#on-your-local-installation)

## Hosting a Room

If you're generating the multiworld, follow the instructions in the previous section.
Once you have the zip file corresponding to your multiworld, follow [MultiworldGG Setup Guide: Hosting a MultiworldGG Server](/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) to host a room.

## Starting the Game and Connecting to a Room

You should have the `.apmp1` patch file provided to you by the multiworld generator. You should also have the room's server
name and port number from the room's host.

Once you do, follow these steps to connect to the room:

1. In the MultiworldGG Launcher, click `Open Patch File`. Then select the `.apmp1` patch file.
   If you have not done so before, it will ask you what program you want to open it with.
2. If this is your first time, it will prompt you for an input iso. Select your _Metroid Prime_ GameCube ISO file.
3. The patch will take some time to complete in the background. (Be patient! The game is 1.46 GB!)
4. Once the output iso file appears in the same directory as your `.apmp1` file (it should be named `AP_XXXX.iso`), open it with Dolphin.
5. After the game is running, connect the Metroid Prime Client to the room by entering the server name and port number at the top and pressing `Connect`.
   For rooms hosted on the website, this will be `multiworld.gg:<port>`, where `<port>` is the port number.
   If a game is hosted from the `MultiworldGGServer.exe` (without `.exe` on Linux), this will default to `38281` but may be changed in the `host.yaml`.

>[!TIP]
>  **Optional**
>  If you want double-clicking `.apmp1` patch file to automatically open your game for you,
>    - Navigate to your `MultiworldGG` installation and edit the `host.yaml` file.
>    - Scroll down to `metroidprime_options` and either set `rom_start` to `true` if ISO files are already associated with Dolphin or set it to the path to your `Dolphin.exe`.
>    - If `metroidprime_options` isn't in the `host.yaml` yet, click your `.apmp1` patch file and then reopen the `host.yaml` and it should now be there.
>
>    Now when double-clicking the `.apmp1` patch file, it should open the client, patch, and launch Dolphin all at once!

## Troubleshooting

### General Troubleshooting Tips
- Use the latest [Metroid Prime AP release](https://github.com/UltiNaruto/MetroidAPrime/releases)
- Use the latest Release of [Dolphin Emulator](https://dolphin-emu.org/download/) or [PrimeHack](https://github.com/shiiion/dolphin/releases)

### Generating and Patching Troubleshooting

- If you receive this error in a dialog box after opening the AP_XXXXX_PX.apmp1 file:
  > Count Mount File
  > The disc image is corrupted.

  This is not an error related to the patcher - this is Windows File Explorer attempting to mount the GameCube ISO as a removable drive. It's likely that the patcher did sucessfully patch the game.
  See if the patched ISO exists (often named AP_XXXXX_PX.iso). If it does, you can load it manually in Dolphin.

- If you are unable to patch your game:
  - Make sure the game format is ISO.<br>
    .nkit.iso, .rvz, or other formats are *not* supported.<br>
    If unsure, redump your game from your own disc.

### Connection Troubleshooting
I have the randomized game open in Dolphin, but the Metroid Prime client says it can't connect to it!
- Make Sure the ISO is Randomized:
  - On the Main Menu, "Archipelago Metroid Prime" text should appear. ([image example](https://i.imgur.com/W6172zf.png))

- Ensure Only One Instance of Dolphin is Running:
  - Check Task Manager to see if there's multiple emulator instances running or restart your computer.

- Disable Emulated Memory Size Override:
  - In Dolphin, navigate to Options -> Configuration -> Advanced tab, and **Uncheck** Enable Emulated Memory Size Override

- Try Starting the Metroid Prime Client and Dolphin in this order:
    1. Start the Metroid Prime client
    2. Start Dolphin and start the game (if it launches automatically, that's fine)
    3. Select or create a save file and enter the game
    4. Enter the AP server address into the Metroid Prime Client

- For Linux, use Dolphin FlatPak:
  - Install Dolphin Emulator from the [official Flatpak repository](https://dolphin-emu.org/download/#flatpak) or from [Flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu)
  - Dolphin Memory Engine, as part of the Prime AP Client, can not access regular Dolphin's process but can access Flatpak's containerized Dolphin's process

## Feedback

In the offical [Archipelago Discord](https://discord.com/invite/8Z65BR2) there is the [#metroid-prime channel](https://discord.com/channels/731205301247803413/1425600401733980301).
Feel free to ping `@UltiNaruto` with any issues or feedback.
