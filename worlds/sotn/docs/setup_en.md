

[Installation video guide here](https://youtu.be/F_yL3QM4qYw)

[0.81 changes](https://youtu.be/w-Y_4slbMtA)
[0.82 changes](https://www.youtube.com/watch?v=F_yL3QM4qYw&t=8s)

[GRAB THE LAST RELEASE HERE](https://github.com/fdelduque/Archipelago/releases) (ships with MultiworldGG)

## Symphony of the Night
Symphony of the Night is a metroidvania from playstation 1

### Requirements
* MultiworldGG Client
* Symphony of the Night ROM file
* Bizhawk 2.7 or 2.8 or 2.9.1

# Playing
## Generate
Place your options file along with all others players yaml in your players folder. You can get an default yaml for SOTN on MultiworldGGLauncher and choose Generate Template Options.  
Run MultiworldGGGenerate, your seed will be on output directory.  
Since this is an unsupported apworld is required to generate locally. You can open the zipped seed to get the patches for all unsuported games SOTN extension is .apsotn. You can send the file to MultiworldGG website to host.  
## Running
Select Open Patch from MultiworldGGLauncher. PAY ATTENTION TO FILE DIALOG. During the process will be asked for Castlevania - Symphony of the Night (USA) (Track 1).bin or ROM File and Castlevania - Symphony of the Night (USA) (Track 2).bin or Audio File. You could be asked for a bizhawk binary also. You might get No handler found during Sony and Playstation logos. Don't forget to enter your server address and click connect after getting Symphony of the Night handler.
If you prefer to open manually, run the game with AP_SEED_PLAYER.cue, chooose Bizhawk client from MultiworldGGLauncher, on Bizhawk choose Tools->Lua Console, on Lua console choose Script->Open script and select connector_bizhawk_generic.lua from data\lua directory. Don't forget to enter your server address and click connect after getting Symphony of the Night handler.  
In the same folder as your .apsotn you will get and AP_SEED_NAME.cue, AP_SEED_NAME.bin and Castlevania - Symphony of the Night (USA) (track 2).bin files.  
# Customize
You can tweak some option in your default yaml:  
## Tweaks
* rng_start_gear: Randomize starting inventory.
* open_no4: Change the state of Underground Caverns back door.
* open_are: Open Colosseum back door.
* item_pool: Choose which location will be added to the pool.
* randomize_items: Will randomize items not in the seed pool.
* enemysanity: Hiting a enemy become a check
* enemy_scroll: Faerie scroll is required for enemysanity checks
* difficult: Preset to tweak the game
## Quality of Life
* infinite_wing: Your bat wing smash spell will remain.
* powerful_items: Will try to add more powerful items to the pool.
* boss_locations: Add boss items to the pool.

![map_normal](https://github.com/user-attachments/assets/f586e1bc-9eaf-4998-83c7-5562ff30bf91)
![map_inverted](https://github.com/user-attachments/assets/bd1c6ba5-9b25-4d7a-ae1e-ee34f56e5ca3)

# The game
Your received items will appear on the lower left corner of the screen.  
Items on breakable walls could be an secret boots, that means is an offworld item and will be send as soon you break the wall. Items for your game would fall in the floor if you did not loot before it vanish you lost it.  
Items on the floor could be your item or a bag of gold. The color of the bag is red for useful items, yellow for filler ones and blue for progression.  

# Troubleshooting
If you choose the wrong file ROM or audio during patching you can delete both Castlevania - Symphony of the Night (USA) from your MultiworldGG main folder and the patched ones also, you be asked again during the patch process.  

