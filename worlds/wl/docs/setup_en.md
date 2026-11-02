# Wario Land Setup Guide

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases)
- A (World) ROM of Super Mario Land 3: Wario Land.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.9.x recommended

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- If you're using BizHawk 2.7 or 2.8, go to `Config > Customize`. On the Advanced tab, switch the Lua Core from
`NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. (If you're using BizHawk 2.9, you can skip this step.)
- Under `Config > Customize`, check the "Run in background" option to prevent disconnecting from the client while you're
tabbed out of EmuHawk.
- Open a `.gb` file in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click
`Controllers…`, load any `.gb` ROM first.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to
clear it.

## Optional Software

- [Wario Land AP Tracker](https://github.com/randomcodegen/wl_ap_tracker/releases/latest), for use with
[PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Generating and Patching a Game

1. On AP: Download [wl.apworld](https://github.com/randomcodegen/Archipelago_WL/releases/latest) and put it in C:\ProgramData\Archipelago\lib\custom_worlds
2. Generate the required .yaml file in the Launcher (Generate Template Options) and then put the Wario Land.yaml file into the .\players\ folder.
3. Follow the general Archipelago instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).
This will generate an output file for you. Your patch file will have the `.apwl` file extension.
1. Drag&Drop the *.apwl Patch-File onto MultiworldGGLauncher.exe
2. If this is your first time patching, you will be prompted to locate your vanilla ROM.
3. A patched `.gb` file (`.gbc` for DX) will be created in the same place as the patch file.
4. On your first time opening a patch with BizHawk Client, you will also be asked to locate `EmuHawk.exe` in your
BizHawk install.

## Optional DX colorization

To generate a color version, set `use_dx: true` in the `Wario Land` section of
your player YAML.  

If the DX IPS path is missing, generation opens a file picker.

Use korxo's [DX 1.2 patch](https://www.romhacking.net/hacks/6683/) and a clean World-version ROM.  
The default `use_dx: false` produces the original monochrome version.

## Connecting to a Server

By default, opening a patch file will do steps 1-5 below for you automatically. Even so, keep them in your memory just
in case you have to close and reopen a window mid-game for some reason.

1. Wario Land uses MultiworldGG's BizHawk Client. If the client isn't still open from when you patched your game,
you can re-open it from the launcher.
2. Ensure EmuHawk is running the patched ROM.
3. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing.
4. In the Lua Console window, go to `Script > Open Script…`.
5. Navigate to your MultiworldGG install folder and open `data/lua/connector_bizhawk_generic.lua`.
6. The emulator may freeze every few seconds until it manages to connect to the client. This is expected.\
The BizHawk Client window should indicate that it connected and recognized Wario Land.
7. To connect the client to the server, enter your room's address and port (e.g. `multiworld.gg:38281`) into the
top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect.

## Auto-Tracking

Wario Land has a fully functional map tracker that supports auto-tracking.

1. Download [Wario Land AP Tracker](https://github.com/randomcodegen/wl_ap_tracker/releases/latest) and
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Put the tracker pack into packs/ in your PopTracker install.
3. Open PopTracker, and load the Wario Land pack.
4. For autotracking, click on the "AP" symbol at the top.
5. Enter the MultiworldGG server address (the one you connected your client to), slot name, and password.