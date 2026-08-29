# Setup Guide for Paper Mario: The Thousand-Year Door Archipelago

## Required Software

- Dolphin Emulator: [Dolphin Emulator Releases](https://dolphin-emu.org/download/?ref=btn)
- MultiworldGG: [Latest releases](https://github.com/MultiworldGG/MultiworldGG/releases)
- Not needed with MWGG: TTYD APWorld: [Latest releases](https://github.com/jamesbrq/ArchipelagoTTYD/releases)
- A US copy of Paper Mario: The Thousand-Year Door in .iso format. (EU and JP versions are not supported at this time)
	- This can not be a .ciso or .nkit.iso (or nkit.rvz) file as the data will not be structured properly

## Installing the APWorld

Place the TTYD apworld in the `custom_worlds` folder of your Archipelago installation. You will only need one copy of this file, specifically in `custom_worlds`.

## Dolphin Configuration

## Settings

- In Game Config > General, make sure Enable Dual Core is unchecked
- In Game Config > Graphics, set your Backend to either OpenGL or Vulkan (Direct3D can often cause errors that may lead to crashes)
- In Game Config > Advanced, make sure that Enable Emulated CPU Clock Override is unchecked

# Note

The MultiworldGG client will automatically configure Dolphin for you, you do not need to set these manually. But if you want to do it manually, here are the settings you need to change.

- In Game Config > Advanced, check 'Enable Emulated Memory Size Override' and set 'MEM1' to 64 MB. This is required for the mod's expanded memory usage. The MultiworldGG client enables this for you automatically every time it launches.
- In Game Config > Advanced, make sure Enable MMU is checked. This is required, the game will not boot correctly without it. The MultiworldGG client enables this for you automatically every time it launches.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

Once you've installed the apworld, you can generate a yaml using the `Generate Template Options` button in the MultiworldGGLauncher. 
It can be found in `Players/Templates` after you have done so. The name of the file will be `Paper Mario: The Thousand-Year Door.yaml`

If the `.yaml` file is missing in your `Players/Templates` folder, then please go through the apworld installation steps again,
and double check that everything was done correctly.

## Joining a MultiWorld Game

## Obtain your GC patch file

### Generating a game
If you are playing by yourself, then all you need to do is place your `.yaml` file that you customized into the `Players` folder in MultiworldGG. 
Note: It does not go in the `Templates` folder.

If you are playing with multiple people, then all of the players `.yaml` files will go in the same folder.

Once you have done so, run the `MultiworldGGGenerate.exe` application, and your game will be placed in the `output` folder if it was successful.
In the `output` folder, you will find a `.zip` file that contains your patch. 
In the launcher, you will find an `Open Patch` button you can use to run the patch and get your `.iso` file.
An alternative method is to double click the patch, and select `MultiworldGGLauncher.exe` as the application to run it with.

When you patch the game for the first time, it will ask you for an `.iso` file to use when patching, as well as your `Dolphin.exe` emulator executable file.
The client will open and the game will launch automatically if everything was done correctly.

### Hosting a game
Any `.zip` file you generate can be uploaded [here](/uploads) to create a room, which you can join in your client.



### Connect to the Multiserver

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)

_Note for Mac users: Due to additional security hardening that Apple added to MacOS, the steps from [here](https://github.com/aldelaro5/dolphin-memory-engine?tab=readme-ov-file#macos-code-signing) relating to Code Signing must be performed. Not doing so will prevent your MultiworldGG Client from connecting to the game appropriately._