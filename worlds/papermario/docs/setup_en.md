# AP World Setup

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases) v0.7.100 or higher. Make sure to install the
  Generator. You will not be able to generate games with Paper Mario on the Archipelago site, only locally.
- If you want to use Archipelago: [The Paper Mario AP World](https://github.com/icebound777/PMR_APWorld/). To download it, go to the [latest release](https://github.com/icebound777/PMR_APWorld/releases) and download the papermario.apworld file.
- A legally obtained US 1.0 Paper Mario ROM.
- Emulator
  - [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 to 2.9.1; **2.10's release does not work**, 2.11 or newer.
  - or [Luna's Project64](https://github.com/Luna-Project64/Luna-Project64/releases)

## Emulator setup for Luna's Project64

If you want to try using the Luna's Project64 emulator instead of bizhawk, then in addition to the emulator itself you'll need to do the following:

1. Get the lua connector script from the sm64 hacks ap github, only the `connector_pj64_generic.js` file is needed: [SM64 Hacks AP Github](https://github.com/DNVIC/archipelago-sm64hacks/releases). After downloading it, place it in `%appdata%/Luna-Project64/Scripts/` (first create the `Scripts` directory if it does not exist already)
2. Setup your PM64 game such that you have a .z64 file with the patch applied
3. In the Luna's PJ64 settings, you need to change:
    - Options dropdown -> click Configuration -> go to Advanced on the left -> check "Always use interpreter core"
    - Options dropdown -> graphics settings -> Frame buffer tab -> check Emulate frame buffer
4. Load the pm64 rando rom and open the generic bizhawk client from the AP side
5. In Luna's PJ64 go to the Debugger drop down and enable the debugger, then go back to the Debugger drop down and open the scripts menu. Inside the scripts menu you'll want to double click the `connector_pj64_generic.js` script so that the `-` turns into a `>`, and that means the script is running

(Note for unix users: This _does_ work when run through Steam's Proton compatability layer)

## Add the Paper Mario AP World to your Archipelago install

As of Archipelago v0.5.0, you can double click .apworld files to add apworlds to your Archipelago installation.

## Creating a YAML file

### Option A: Generate a template YAML using MultiworldGG and edit it

Want the typical Archipelago experience? Run MultiworldGGLauncher.exe (found in the base MultiworldGG folder) and click  
Generate Template Settings to generate a template YAML file. It will open the folder of template files which you can  
then edit to your liking.

### Option B: Use the PM Sample.yaml file and edit it to your liking

Want a YAML that looks like what you'd get when exporting it from the site? Grab the [PM Sample.yaml file.](https://github.com/icebound777/PMR_APWorld/blob/main/docs/PM%20Sample.yaml)  
It has all the settings and shows options for each setting as well as what is/isn't implemented. If you want to see  
the descriptions that you would see on the site, you can check out [options.py,](https://github.com/icebound777/PMR_APWorld/blob/main/options.py)  
or check out option C...

### Option C: Use the PMR website to get a setting string

Want a GUI with buttons, sliders, descriptions, and cute styling? Grab the [PMR Settings String.yaml file.](https://github.com/icebound777/PMR_APWorld/blob/main/docs/PMR%20Settings%20String.yaml)
Visit [the Paper Mario Randomizer site](https://pm64randomizer.com/) and select your settings. When you're  
ready, go to the top of the page and click the Export button. This will update the Settings String field with the  
settings you've selected. Copy that string and put it in your YAML as the value for `pmr_settings_string`. It'll look  
similar to this:  
`pmr_settings_string: (iIvejnSpf0Kdl0rbg2u0a6Om)(gb1f1p1s0Rzm2)(pSaRn1x1(pGktpbwsl))(qh3SiPZgc2ELt7DQFVO)(dd1ca1.5m1kshzw4EFlvyp0b)(xq100r0t0xubpl128)(mc150h10f5b3s0j0a0irn4x16Q)(om2btwcrFPs65796o2dz0x?50!70Y)(cm7p20g20k20o20a20b20w20s20l20x2n2e2y2c5trhdu-1j)g)`

Note that since some settings are not yet implemented fully, not all of them will result in a successful generation.  
[PM Sample.YAML](https://github.com/icebound777/PMR_APWorld/blob/main/docs/PM%20Sample.yaml) can be referred to to see what options are and are not implemented, regardless of how you choose  
to create your YAML.

## Generating a Game

Follow [the general MultiworldGG instructions](/tutorial/Archipelago/setup/en#generating-a-game) for generating a game, specifically on your local installation. You cannot generate games using the Paper Mario AP World on the website.

## Hosting a Game

Follow [the general MultiworldGG instructions](/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) for hosting a MultiworldGG server. You _can_ host games that use the Paper Mario AP World on the website, or you can host it locally.

## Connecting to a MultiworldGG Server
1. Obtain your .appm64 file from whoever is hosting the game. These files will not upload to the MultiworldGG even if it is hosted there, so you will have to send/receive them elsewhere.
2. Once you have obtained your .appm64 patch file, open up MultiworldGGLauncher.exe from the base MultiworldGG folder and click "Open Patch". In the prompt that comes up, choose your .appm64 file. If this is your first time opening the patch file, you will be prompted to locate your vanilla ROM. You will also be prompted to locate your BizHawk client, which is named EmuHawk.exe in your BizHawk install. A patched .z64 file will be created in the same place as the patch file.
3. Once the patch file has been created, BizHawk should start up automatically with the patched ROM. The Generic BizHawk Client for MultiworldGG will also open, as well as a Lua Console window. At this point all you need to do to connect is enter your room's address and port (e.g. multiworld.gg:38281) into the top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is perfectly safe to make progress offline; everything will re-sync when you reconnect.

Note: After the first time you open an .appm64 file through the MultiworldGG Launcher, it should associate that file type with the launcher and all you should have to do is double click them.
