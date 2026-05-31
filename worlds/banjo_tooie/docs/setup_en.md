
# Setup Guide for Banjo-Tooie MultiworldGG

## Important

This guide is only applicable to Windows and Linux systems.
Our implementation also supports the Everdrive 3.0 and X7. (USB Support).

## Required Software and Hardware

- PC Emulation:
    - Tested emulators and recommended settings:
        -   BizHawk:  [BizHawk Releases](https://tasvideos.org/BizHawk/ReleaseHistory)
            -   Version **2.10** and later are supported
            -   Detailed installation instructions for BizHawk can be found at the above link
            -   Windows users must run the prereq installer first, which can also be found at the above link
        -   Project64 3.0: [Public Releases](https://www.pj64-emu.com/public-releases)
            -   Version **3.0.1** supported
            -   Default settings should work.
            -   enable Input Plugin N-Rage if you are having issues setting up your controller.
            -   Do not enable debugging in Options > configuration > Debugging
            -   to reduce lag:
                1. Open the ROM
                2. Options > Config: RANDO TOOIE > Counter Factor = 0 or 1
        -   Project64 4.0: [Development Builds](https://www.pj64-emu.com/nightly-builds)
            -   Version **4.0.6701** tested
            -   Interpreter Core needs to be enabled:
                - Options > configurations > Uncheck Hide Advanced Settings
                - Options > configurations > Advanced > Always Enable Interpreter Core
                - Do not enable debugging in Options > configuration > Debugging
            -   to reduce lag:
                1. Open the ROM
                2. Options > Config: RANDO TOOIE > Counter Factor = 0 or 1
        -   Luna64: [Latest Releases](https://github.com/Luna-Project64/Luna-Project64/releases)
            -   Version **3.6.5** tested
            -   Emulate Frame Buffer need to be enabled:
                - Options > Graphic Settings > Frame Buffer > Emulate Frame Buffer
                - Do not enable debugging in Options > configuration > Debugging
            -   to reduce lag:
                1. Open the ROM
                2. Options > Config: RANDO TOOIE > Counter Factor = 0 or 1
        -   RMG: [Latest Releases](https://github.com/Rosalie241/RMG/releases)
            -   Version **0.8.9** tested
            -   Default settings should work.
            -   to reduce lag:
                1. Open the ROM
                2. Settings > Game > Counter Factor = 0 or 1

    - Supported emulators but untested (use at your own discretion)
        -   simple64
        -   Parallel Launcher
        -   RetroArch (mupen64plus_next):
            - For MacOS users, enable Settings > Network > Network Commands and leave the Network Command Port at 55355.
        -   Gopher64
        -   Ares

- Everdrive:
    - The USB driver on the PC that will be connecting to the everdrive
        - Windows: https://ftdichip.com/wp-content/uploads/2021/08/CDM212364_Setup.zip
        - Linux: https://ftdichip.com/wp-content/uploads/2022/07/libftd2xx-x86_64-1.4.27.tgz
    - For Everdrive 3.0, the OS version needs to be 3.06 to be compatible
    - The Nintendo 64 Expansion Pak is required
    - Grab the latest release of the Everdrive connector from https://github.com/jjjj12212/AP_Banjo-Tooie/releases
-   A Banjo-Tooie ROM (USA ONLY)

## Playing on BizHawk

Once BizHawk has been installed, open EmuHawk and change the following settings:

- Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This will allow you to continue playing in the background, even if another window is selected
- Under Config > Hotkeys, many hotkeys are listed, with many bound to common keys on the keyboard. You will likely want to disable most of these, which you can do quickly using  `Esc`
- If playing with a controller, when you bind controls, disable "P1 A Up", "P1 A Down", "P1 A Left", and "P1 A Right" as these interfere with aiming if bound. Set directional input using the Analog tab instead
- Under N64 enable "Use Expansion Slot". (The N64 menu only appears after loading a ROM.)
- Under Config -> Speed/Skip, click "Audio Throttle" as this will fix the off pitch sounds while playing

It is strongly recommended to associate N64 rom extensions (*.n64, *.z64) to the EmuHawk we've just installed. To do so, we simply have to search any N64 rom we happened to own, right click and select "Open with…", unfold the list that appears and select the bottom option "Look for another application", then browse to the BizHawk folder and select EmuHawk.exe.

If you are experiencing performance issues with Banjo-Tooie, you can try the following:
- Under N64 -> Plugins, Set Active Video Plugin to Rice.
This will create some visual artifacts however, it should not affect gameplay.

To help recover from crashes in Bizhawk, play the game while the BT_companion.lua is loaded by dragging the lua script from data/lua/BT_companion.lua onto bizhawk.

### Setup - Emulator
- Run Launcher.exe and select Banjo-Tooie Client
- If this is your first time running this version, it will prompt for your Banjo-Tooie (US) ROM
- The patched rom is located in your MultiworldGG root folder by default
    - The exact path is also printed on the Banjo-Tooie Client
    - You can also click "Browse Files" in the Launcher which will take you to this folder
- **one time only** run `/autostart` in the Banjo-Tooie Client and select your preferred emulator. This will automatically open your emulator and the patched Banjo-Tooie ROM
- For certain emulators that don't automatically open, run `/program_args ` and try again
- Connect the MultiworldGG Client with the server.
    - To connect the client to the multiserver simply put  `<address>:<port>`  on the textfield on top and press `connect` (if the server uses password, then it will prompt after connection)
- If you rather not use **/autostart**:
    - Open your preferred emulator that is supported and open your patched Banjo-Tooie (US) game

- If you are using **Bizhawk**, Once you are in the game title menu or game select screen, drag and drop the BT_companion.lua script (which can be found in the data/lua folder of MultiworldGG) onto the Lua console window. This will recover any crashes if you experience any.

- If the Banjo-Tooie Client says its connected to your emulator, you have connected to your slot, but Banjo-Tooie shows "BTClient Disconnected",
try running the command `/writesettings` to force your slot data into the game.

## Playing on Everdrive
- Run MultiworldGGLauncher.exe and select Banjo-Tooie Client
- If this is your first time running this version, it will prompt for your Banjo-Tooie (US) ROM
- The patched rom is located in your MultiworldGG root folder
    - The exact path is also printed on the Banjo-Tooie Client
    - You can also click "Browse Files" in the Launcher which will take you to this folder
- Load the patched version of the ROM on your everdrive sd card
- The Everdrive will need to have a USB connection to the PC that will be running the Banjo-Tooie Client
- **one time only** run `/autostart` in the Banjo-Tooie Client and select banjo_tooie_everdrive_connector.exe. This will automatically open the connector for the everdrive
    - If you are on Linux, select Banjo_Tooie_everdrive_connector_linux instead
- If you rather not use `/autostart`:
    - Open banjo_tooie_everdrive_connector.exe if you are on Windows
    - If you are on Linux, select Banjo_Tooie_everdrive_connector_linux instead
- Run the patched Banjo-Tooie Rom on the everdrive
- Connect the MultiworldGG client with the server. (The banjo_tooie_connector window should say, "Connection Established")
- To connect the client to the multiserver, simply put  `<address>:<port>`  on the textfield on top and press `connect` (if the server uses password, then it will prompt after connection)
