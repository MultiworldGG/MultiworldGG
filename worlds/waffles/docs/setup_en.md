# Spicy Mycena Waffles Setup Guide

## Detailed Guide and updates

[Refer to this guide.](https://thelx5.github.io/smw/#setup)

## Required Software

- MultiworldGG from the [MultiworldGG Releases Page](https://github.com/MultiworldGG/MultiworldGG/releases)
- Software or hardware capable of loading and playing SNES ROM files
  - Recommended: [snes9x-nwa](https://github.com/Skarsnik/snes9x-emunwa/releases)
  - snes9x-rr
  - BSNES-plus
  - FxPak
- Your Super Mario World (US) ROM file from the original cartridge. We cannot provide this file.
  - MD5: cdd3c8c37322978ca8669b34bc89c804

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch
files. Your patch file should have a `.apwaffle` extension.

Put your patch file on your desktop or somewhere convenient, and double click it. This should automatically launch the
client, and will also create your ROM in the same place as your patch file.

### Connect to the client

#### With an emulator

When the client launched automatically, SNI should have also automatically launched in the background. If this is its
first time launching, you may be prompted to allow it to communicate through the Windows Firewall.

##### snes9x-nwa

1. Click on the Network Menu and check **Enable Emu Network Control**
2. Load your ROM file if it hasn't already been loaded.

##### snes9x-rr

1. Load your ROM file if it hasn't already been loaded.
2. Click on the File menu and hover on **Lua Scripting**
3. Click on **New Lua Script Window...**
4. In the new window, click **Browse...**
5. Select the connector lua file included with your client
    - Look in the MultiworldGG folder for `/SNI/lua/Connector.lua`.
6. If you see an error while loading the script that states `socket.dll missing` or similar, navigate to the folder of 
the lua you are using in your file explorer and copy the `socket.dll` to the base folder of your snes9x install.

##### BSNES-Plus

1. Load your ROM file if it hasn't already been loaded.
2. The emulator should automatically connect while SNI is running.


## Final Notes

- snes9x-nwa will require enabling Enable Emu Network Control under the Netplay menu in the emulator.
- snes9x will not run the randomized ROM if the overclock hacks within the emulator are enabled. Please disable those.
- FxPak will take a good amount of time to process bought items in the inventory menu with EnergyLink (around 20-30 seconds) as fetching SRAM changes is a slow procedure.

