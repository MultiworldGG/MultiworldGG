# Super Mario Odyssey Setup Guide
## Note
This mod only works on version 1.0.0 of Super Mario Odyssey! Please downgrade your game before installing the mod!

## Installation
* Install the latest version from the releases page. `smo.apworld` and either `SMO_Archipelago_Vx.x_Switch.zip` for console or `SMO_Archipelago_Vx.x_Emu.zip` for emulator.
* If you want to use AP: Place `smo.apworld` in the `custom_worlds` folder of your Archipelago install which the default directory is `C:\ProgramData\Archipelago\custom_worlds`

<details>
<summary>Switch</summary> 
  
- Extract `SMO_Archipelago_Vx.x_Switch.zip` and Place the `atmosphere` folder onto the root of your sd card.

</details>

<details>
<summary>Emulator</summary>

### Ryujinx (Not well tested, may be unstable)
- Extract `SMO_Archipelago_Vx.x_Emu.zip` and Place `SMOAP` folder in the mods directory for Super Mario Odyssey.
- Create a new User Profile (`Options` > `User Profiles` > `+`)
- Enable LAN Mode (`Options` > `Settings` > `Network`)

### Eden
- Right Click on Super Mario Odyssey in the game menu and select `Open Mod Data Location`.
- Extract `SMO_Archipelago_Vx.x_Emu.zip` and Place `SMOAP` folder in the mods directory that opened.
- Go to `Emulation` > `Configure` > `System` > `Network` and uncheck `Enable Airplane Mode`
</details>

## Usage
- Launch the Archipelago Client, search for `Super Mario Odyssey` and click the `Open` button
- After the client opens, launch your modded SMO installation
- When prompted, the `IP Address` you are connecting to is your computer's local IP address
    - On Switch: this is found by entering the `ipconfig` command into command prompt on Windows
    - On Emulator: leave the IP at its default value: `127.0.0.1`
- When prompted, the `Port` is `1027` by default which does not need to be changed.
- To change your IP later, hold ZL while closing the pause menu
- After connecting, both the client and game should display a confirmation message
- Enter the IP and Port for your lobby into the SMO Client. For example: `archipelago.gg:38281`. You will then be prompted for a Username and Password
- At this point, everything should be working and you should be able to send and receive checks

### Usage Tips
- `/smo` can be used to check the status of your connection
- `/warp <kingdom> [scenario]` can be used to warp to any kingdom in any scenario at any time
    - `/warp metro 3` will take you to Festival Metro to avoid [#3](https://github.com/AdalynBlack/SuperMarioOdysseyArchipelago/issues/3)
    - `/warp wooded 3` will take you to post-peace Wooded Kingdom to avoid [#4](https://github.com/AdalynBlack/SuperMarioOdysseyArchipelago/issues/4)
- Depending on when the mod connects to the client, checks may stop sending in some cases. Enter and exit a loading zone to fix this issue
