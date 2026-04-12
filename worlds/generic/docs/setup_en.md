# MultiworldGG Setup Guide

This guide is intended to provide an overview of how to:
- Install, set up, and run the MultiworldGG Multiworld software
- Generate and host multiworlds
- Connect to the multiworld after hosting has begun

This is a general overview. For more specific steps, reference the relevant game's [setup guide](/tutorial).

Some steps also assume use of Windows, so may vary with your OS.

## Installing the MultiworldGG software

The most recent public release of MultiworldGG from the [Client page](/downloads)

Run the exe file, and after accepting the license agreement you will be asked which components you would like to
install.

MultiworldGG installations are automatically bundled with some programs. These include a launcher, a generator, a
server and some clients.

- The launcher lets you quickly access MultiworldGG's different components and programs. It is found under the name 
  `MultiworldGGLauncher` and can be found in the main directory of your MultiworldGG installation.

- The generator allows you to generate multiworld games on your computer. Please refer to the 'Generating a game'
  section of this guide for more information about it.

- The server will allow you to host the multiworld on your machine. Hosting on your machine requires forwarding the port
you are hosting on. The default port for MultiworldGG is `38281`. If you are unsure how to do this there are plenty of
other guides on the internet that will be more suited to your hardware.

- The clients are what are used to connect your game to the multiworld. Some games use a client that is automatically
installed with a MultiworldGG installation. You can access those clients via the launcher or by navigating
to your MultiworldGG installation. 

## Generating a game

### What is a YAML?

YAML is the file format which MultiworldGG uses in order to configure a player's world. It allows you to dictate which
game you will be playing as well as the options you would like for that game.

YAML is a format very similar to JSON however it is made to be more human-readable. If you are ever unsure of the
validity of your YAML file you may check the file by uploading it to the check page on the MultiworldGG website:
[YAML Validation Page](/check)

### Creating a YAML

YAML files may be generated on the MultiworldGG website by visiting the [games page](/games) and clicking the
"Options Page" link under the relevant game. Clicking "Export Options" in a game's options page will download the
YAML to your system.

Alternatively, you can run `MultiworldGGLauncher.exe` and click on `Generate Template Options` to create a set of template 
YAMLs for each game in your MultiworldGG install (including for APWorlds). These will be placed in your `Players/Templates` folder.

In a multiworld there must be one YAML per world. Any number of players can play on each world using either the game's
native coop system or using MultiworldGG's coop support. Each world will hold one slot in the multiworld and will have a
slot name and, if the relevant game requires it, files to associate it with that multiworld.

If multiple people plan to play in one world cooperatively then they will only need one YAML for their coop world. If
each player is planning on playing their own game then they will each need a YAML.

### Generating a single player game

#### On the website

The easiest way to get started playing a MultiworldGG generated game, after following the base setup from the game's
setup guide, is to find the game on the [MultiworldGG Games List](/games), click on `Options Page`, set the options for
how you want to play, and click `Generate Game` at the bottom of the page. This will create a page for the seed, from
which you can create a room, and then [connect](#connecting-to-an-multiworldgg-server).

If you have downloaded the options, or have created an options file manually, this file can be uploaded on the
[Generation Page](/generate) where you can also set any specific hosting settings.

#### On your local installation

To generate a game on your local machine, make sure to install the MultiworldGG software. Navigate to your MultiworldGG
installation (usually C:\Program Files\MultiworldGG), and place the options file you have either created or downloaded
from the website in the `Players` folder.

Run `MultiworldGGGenerate.exe`, or click on `Generate` in the launcher, and it will inform you whether the generation
was successful or not. If successful, there will be an output zip in the `output` folder 
(usually named something like `AP_XXXXX.zip`). This will contain all relevant information to the session, including the
spoiler log, if one was generated.

Please note that some games require you to own their ROM files to generate with them as they are needed to generate the
relevant patch files. When you generate with a ROM game for the first time, you will be asked to locate its base ROM file.
This step only needs to be done once.

### Generating a multiplayer game

MultiworldGG is a multi-game multiworld architecture, so any number of players and any number of games may be used to
generate. Of note, the website currently has a maximum generated player count of 30. If you would like to generate a game
larger than that, it must be done on a local installation. Generally, it is better to generate locally to free server
resources, and host the resulting multiworld on the website.

#### Gather All Player YAMLs

All players that wish to play in the generated multiworld must have a YAML file which contains the options that they
wish to play with. One person should gather all files from all participants in the generated multiworld. It is possible
for a single player to have multiple games, or even multiple slots of a single game, but each YAML must have a unique
player name.

#### On the website

Gather all player YAML files into a single place, then navigate to the [Generate Page](/generate). Select the host settings
you would like, click on `Upload File(s)`, and select all player YAML files. The site also accepts `zip` archives containing YAML
files.

After some time, you will be redirected to a seed info page that will display the generated seed, the time it was
created, the number of players, the spoiler (if one was created) and all rooms created from this seed.


#### On your local installation

It is possible to generate the multiworld locally, using a local MultiworldGG installation. This is done by entering the
MultiworldGG installation folder (usually C:\Program Files\MultiworldGG) and placing each YAML file in the `Players` folder.
If the folder does not exist then it must be created manually. The files here should not be compressed.

After filling the `Players` folder, run`MultiworldGGGenerate.exe` or click `Generate` in the launcher. The output of 
the generation is placed in the `output` folder (usually named something like `AP_XXXXX.zip`).

Please note that if any player in the game you want to generate plays a game that needs a ROM file to generate, you will
need the corresponding ROM files.

##### Changing local host settings for generation

Sometimes there are various settings that you may want to change before rolling a seed such as enabling race mode,
auto-release, plando support, or setting a password.

All of these settings, plus more, can be changed by modifying the `host.yaml` file in the MultiworldGG
installation folder. You can quickly access this file by clicking on `Open host.yaml` in the launcher. The settings
chosen here are baked into the `.archipelago` file that gets output with the other files after generation, so if you 
are rolling locally, ensure this file is edited to your liking **before** rolling the seed. This file is overwritten 
when running the MultiworldGG installation software. If you have changed settings in this file, and would like to retain 
them, you may rename the file to `options.yaml`. 

### Playing with custom worlds

If you are generating locally, you can play with worlds that are not included in the MultiworldGG installation.
These worlds are packaged as `.apworld` files. To add a world to your installation, click the "Install APWorld" button
in the launcher and select the `.apworld` file you wish to install. Alternatively, you can drag the `.apworld` file
onto the launcher or double-click the file itself (if on Windows). Once the world is installed, it will function like
the worlds that are already packaged with MultiworldGG. Also note that while generation with custom worlds must be done
locally, these games can then be uploaded to the website for hosting and played as normal.

We strongly recommend that you ensure the source of the `.apworld` is safe and trustworthy before playing with a
custom world. Installed APWorlds are able to run custom code on your computer whenever you open MultiworldGG.

#### Alternate versions of included worlds

If you want to play with an alternate version of a game that is already included in MultiworldGG, you should also
remove the original APWorld after completing the above installation. To do so, go to your MultiworldGG installation
folder and navigate to the `lib/worlds` directory. Then move the `.apworld` or the folder corresponding to the game you
want to play an alternate version of to somewhere else as a backup. If you want to play this original again, then
restore the original version to `lib/worlds` and remove the alternate version, which is in the `custom_worlds` folder.

Note: Currently, this cannot be done on the Linux AppImage release.

## Hosting a MultiworldGG Server

When a multiworld seed is generated, the multidata will be output as a `.archipelago`. If the game was generated locally,
a compressed folder will be in `/output` and will contain the `.archipelago`, the spoiler log, and any relevant files
for the generated games.

### Hosting on the website

After a seed page has been created on the website, clicking on `Create Room` will create a new server instance, and a
page that can be linked to the other players, so they can all see the connection info, obtain their data files, and
connect to the multiworld. Simply click on the url in the title bar, copy the link, and send it to your friends. Room
servers will shut down after 4 hours of inactivity, saving the multiworld progress. By returning to the room page, the
room server can be started back up, and the multiworld can continue to be played. If the link to the room is lost, the
creator of the room can find it on their [User Content Page](/user-content). The person who created the room becomes the
"owner" of the room, and as such has access to the server console. Clearing cookies will remove access to this console,
and there is no way to regain it. If a server password was set when generating the multiworld game, server admin
privileges may be gained by entering `!admin <password>` from the `MultiworldGGTextClient.exe`.

#### The room page

![Screenshot of Room Page](example_room.png)
1. Server/Host Name
2. Port
3. Slot Name
4. Download link for data files
5. Link to tracker page for this player

#### From a website generated game

After generating a game on the website, you will be redirected to the seed page. To begin playing click on `Create Room`
to create a new room page and server for your game.

#### From a locally generated game

After generating a game, a compressed folder will be output to the `/output` folder. Go to the
[MultiworldGG Host Game Page](/uploads), click on `Upload File`, navigate to your MultiworldGG installation, and select
the generated folder. This will create a new seed page using the information from this folder.

### Hosting on a local machine

The `.archipelago` file may be extracted from the compressed file. Double-clicking the file will then open
`MultiworldGGServer.exe` in order to host the multiworld on the local machine. Alternatively, running
`MultiworldGGServer.exe` and pointing the resulting file selection prompt to the `.archipelago` file or the generated
compressed folder will begin hosting.

## Connecting to a MultiworldGG Server

The actual method of connection will vary depending on the game, so follow that game's setup guide, but all games will
use the same general connection info noted here.

### Connection Info

For connecting from the game to the server, the connection info is needed for any of the game clients. Games that use
data files will usually contain the connection info within these files, when hosted on the MultiworldGG website. If the
information needs to be entered manually, it is usually comprised of four different sections.

* `Server`, `Server Name` or `Host Name` are all used interchangeably as the domain or IP address of the server. If the
game is being hosted on the main MultiworldGG website this will be `multiworld.gg`. If the game is being hosted on your
own local machine `localhost` will work. If the game is being hosted on another person's computer then you enter that
person's public IP address.
* `Port` is which port on the domain or IP address the game is being hosted on. On the website room pages, this is
displayed as `multiworld.gg:<port>`. Most clients will accept that information being entered directly as is. If the
information needs to be entered separately, then the port is the sequence of numbers after the `:`, and the `:` does
not need to be entered. If a game is being hosted from the `MultiworldGGServer.exe`, this will default to `38281` but may
be changed in the `host.yaml`.
* `Slot Name` is the name of your player slot that you are connecting to. This is the same as the name that was set
when creating your [YAML file](#creating-a-yaml). If the game is hosted on the website, this is also displayed on the
room page. The name is case-sensitive.
* `Password` is the password set by the host in order to join the multiworld. By default, this will be empty and is almost
never required, but one can be set when generating the game. Generally, leave this field blank when it exists,
unless you know that a password was set, and what that password is.
