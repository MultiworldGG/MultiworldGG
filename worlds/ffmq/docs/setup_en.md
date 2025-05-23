# Final Fantasy Mystic Quest Setup Guide

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases).

- Hardware or software capable of loading and playing SNES ROM files
    - An emulator capable of connecting to SNI such as:
        - snes9x-rr from: [snes9x rr](https://github.com/gocha/snes9x-rr/releases),
        - BizHawk from: [BizHawk Website](http://tasvideos.org/BizHawk.html)
        - RetroArch 1.10.1 or newer from: [RetroArch Website](https://retroarch.com?page=platforms). Or,
    - An SD2SNES, FXPak Pro ([FXPak Pro Store Page](https://krikzz.com/store/home/54-fxpak-pro.html)), or other
      compatible hardware

- Your legally obtained Final Fantasy Mystic Quest NA 1.0 or 1.1 ROM file, probably named `Final Fantasy - Mystic Quest (U) (V1.0).sfc` or `Final Fantasy - Mystic Quest (U) (V1.1).sfc`
The Archipelago community cannot supply you with this.

## Installation Procedures

### Linux Setup

1. Download and install [MultiworldGG](<https://github.com/MultiworldGG/MultiworldGG/releases/latest>). **The installer 
   file is located in the assets section at the bottom of the version information. You'll likely be looking for the `.AppImage`.**
2. It is recommended to use either RetroArch or BizHawk if you run on linux, as snes9x-rr isn't compatible.

### Windows Setup

1. Download and install [MultiworldGG](<https://github.com/MultiworldGG/MultiworldGG/releases/latest>). **The installer 
   file is located in the assets section at the bottom of the version information.**
2. If you are using an emulator, you should assign your Lua capable emulator as your default program for launching ROM
   files.
    1. Extract your emulator's folder to your Desktop, or somewhere you will remember.
    2. Right-click on a ROM file and select **Open with...**
    3. Check the box next to **Always use this app to open .sfc files**
    4. Scroll to the bottom of the list and click the grey text **Look for another App on this PC**
    5. Browse for your emulator's `.exe` file and click **Open**. This file should be located inside the folder you
       extracted in step one.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Options page on the website allows you to configure your personal options and export a config file from
them. Player options page: [Final Fantasy Mystic Quest Player Options Page](/games/Final%20Fantasy%20Mystic%20Quest/player-options)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/mysterycheck)

## Generating a Single-Player Game

1. Navigate to the Player Options page, configure your options, and click the "Generate Game" button.
    - Player Options page: [Final Fantasy Mystic Quest Player Options Page](/games/Final%20Fantasy%20Mystic%20Quest/player-options)
2. You will be presented with a "Seed Info" page.
3. Click the "Create New Room" link.
4. You will be presented with a server page, from which you can download your `.apmq` patch file.
5. Go to the [FFMQR website](https://ffmqrando.net/Archipelago) and select your Final Fantasy Mystic Quest ROM
and the .apmq file you received, choose optional preferences, and click `Generate` to get your patched ROM.
7. Since this is a single-player game, you will no longer need the client, so feel free to close it.

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your patch file, or with a zip file containing
everyone's patch files. Your patch file should have a `.apmq` extension.

Go to the [FFMQR website](https://ffmqrando.net/Archipelago) and select your Final Fantasy Mystic Quest ROM
and the .apmq file you received, choose optional preferences, and click `Generate` to get your patched ROM.

Manually launch the SNI Client, and run the patched ROM in your chosen software or hardware.

### Connect to the client

#### With an emulator

If this is the first time SNI launches, you may be prompted to allow it to communicate through the Windows Firewall.

##### snes9x-rr

1. Load your ROM file if it hasn't already been loaded.
2. Click on the File menu and hover on **Lua Scripting**
3. Click on **New Lua Script Window...**
4. In the new window, click **Browse...**
5. Select the connector lua file included with your client
    - Look in the MultiworldGG folder for `/SNI/lua/x64` or `/SNI/lua/x86` depending on if the
      emulator is 64-bit or 32-bit.
6. If you see an error while loading the script that states `socket.dll missing` or similar, navigate to the folder of 
the lua you are using in your file explorer and copy the `socket.dll` to the base folder of your snes9x install.

##### BizHawk

1. Ensure you have the BSNES core loaded. You may do this by clicking on the Tools menu in BizHawk and following these
   menu options:  
   `Config --> Cores --> SNES --> BSNES`  
   Once you have changed the loaded core, you must restart BizHawk.
2. Load your ROM file if it hasn't already been loaded.
3. Click on the Tools menu and click on **Lua Console**
4. Click the Open Folder icon that says `Open Script` via the tooltip on mouse hover, or click the Script Menu then `Open Script...`, or press `Ctrl-O`.
5. Select the `Connector.lua` file included with your client
    - Look in the MultiworldGG folder for `/SNI/lua/x64` or `/SNI/lua/x86` depending on if the
      emulator is 64-bit or 32-bit. Please note the most recent versions of BizHawk are 64-bit only.

##### RetroArch 1.10.1 or newer

You only have to do these steps once. Note, RetroArch 1.9.x will not work as it is older than 1.10.1.

1. Enter the RetroArch main menu screen.
2. Go to Settings --> User Interface. Set "Show Advanced Settings" to ON.
3. Go to Settings --> Network. Set "Network Commands" to ON. (It is found below Request Device 16.) Leave the default
   Network Command Port at 55355.

![Screenshot of Network Commands setting](/static/generated/docs/A%20Link%20to%20the%20Past/retroarch-network-commands-en.png)
4. Go to Main Menu --> Online Updater --> Core Downloader. Scroll down and select "Nintendo - SNES / SFC (bsnes-mercury
   Performance)".

When loading a ROM, be sure to select a **bsnes-mercury** core. These are the only cores that allow external tools to
read ROM data.

#### With hardware

This guide assumes you have downloaded the correct firmware for your device. If you have not done so already, please do
this now. SD2SNES and FXPak Pro users may download the appropriate firmware on the SD2SNES releases page. SD2SNES
releases page: [SD2SNES Releases Page](https://github.com/RedGuyyyy/sd2snes/releases)

Other hardware may find helpful information on the usb2snes platforms
page: [usb2snes Supported Platforms Page](http://usb2snes.com/#supported-platforms)

1. Close your emulator, which may have auto-launched.
2. Power on your device and load the ROM.

### Connect to the Archipelago Server

SNI serves as the interface between your emulator and the server. Since you launched it manually, you need to tell it what server to connect to. 
If the server is hosted on multiworld.gg, get the port the server hosts your game on at the top of the game room (last line before the worlds are listed).
In the SNI client, either type `/connect address` (where `address` is the address of the server, for example `/connect multiworld.gg:12345`), or type the address and port on the "Server" input field, then press `Connect`.
If the server is hosted locally, simply ask the host for the address of the server, and copy/paste it into the "Server" input field then press `Connect`.

The client will attempt to reconnect to the new server address, and should momentarily show "Server Status: Connected".

### Play the game

When the client shows both SNES Device and Server as connected, you're ready to begin playing. Congratulations on
successfully joining a multiworld game!

## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the Generate page above.
    - Generate page: [WebHost Seed Generation Page](/generate)
4. Wait a moment while the seed is generated.
5. When the seed is generated, you will be redirected to a "Seed Info" page.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players, so
   they may download their patch files from there.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all
   players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.
