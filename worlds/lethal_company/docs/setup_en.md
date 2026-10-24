# Setup Guide
This docment explains how to set up a Lethal Company world and configure it to your liking. Please read through **all** 
relevant portions before using this implementation in a public or private multiworld.

## Setup
Download the following two files from the [Releases page in Github](https://github.com/T0r1nn/APLC/releases/latest):
- lethal_company.yaml
- lethal_company.apworld (only needed if you are not using MWGG)

You also need to install the latest version of the [MultiworldGG Multiworld Randomizer](https://github.com/MultiworldGG/MultiworldGG/releases/latest) client.
Install the [APLC](https://thunderstore.io/c/lethal-company/p/APLC/APLC/) mod from Thunderstore (you may also install 
the mod via r2ModManager, Gale, or other Thunderstore alternatives).

**Note**: If you have an ongoing multiworld, you should use whichever version of the mod you **started with** unless you
are severely impacted by a bug that a later version fixes.

Then, follow the steps below to setup the randomizer:

### YAML configuration
<details>

The first thing you need to do is configure the lethal_company.yaml file. For that, open and edit the YAML to customize 
your playthrough:

- **name**: The player's chosen slot name. If left blank, {player} or {PLAYER} are replaced with the slot number, 
while {number} or {NUMBER} will increment once for each duplicate YAML name.
- **game_mode**: Can be Collectathon, Trophy, or Credit Hunt. In Trophy mode, the player needs to collect one trophy 
apparatus from each moon. In Collectathon, the player needs to collect a specific amount of AP chest scrap and several 
randomly chosen scrap. In Credit Hunt, the player needs to receive a specific amount of company credit items from the 
multiworld.
- **collectathon_scrap_goal**: Can be any number from 3 to 99, default is 10. This is the number of AP chests the 
player must collect for the Collectathon goal, in addition to the random scrap.
- **collectathon_random_scrap**: Can be any number from 0 to 20, default is 5. The player will need to collect this 
many randomly chosen scrap for the Collectathon goal in addition to the required AP chest scrap.
- **credit_replacement**: Can be any number from 5 to 80. This is the percentage of filler items will be replaced 
replaced with company credits for the Credit Hunt goal. This setting does nothing in other modes.
- **required_credits**: Can be any number from 10 to 100. The player must collect this percentage of the total company
credit items in order to complete the Credit Hunt goal. This setting does nothing in other modes.
- **grade_locations_per_moon**: Can be any number from 1 to 10, default is 3. The multiworld will generate this many 
grade locations per moon. A grade location is completed by collecting enough scrap in one day to obtain the minimum 
required grade on a moon.
- **num_quotas**: Can be any number from 0 to 50, default is 15. The multiworld will generate this many quota 
locations. A quota location is completed whenever the player fulfills money_per_quota_location-worth of quota. Progress 
accumulates over quotas and crew wipes.
- **quota_checkpoint_every**: Can be between 1 and 20, default is 3. This option controls how many quota locations the
player must complete between each checkpoint unlock event. Checkpoint unlock events divide quota locations into 
different generation spheres so players are not instantly expected to complete a late quota location. With the default 
values (num_quotas=15 and quota_checkpoint_every=3), quota locations will be grouped into five generation spheres with 
three locations each. Set higher than num_quotas to disable checkpoints entirely and group all quota locations into a 
single sphere.
- **money_per_quota_location**: Can be any number between 50 and 2000, default is 400. This is the total cumulative 
quota a player must obtain to complete each quota location. Be aware that each quota only contributes the required scrap
towards this goal, not the sold scrap. If a player sell 500 scrap but the quota is only 130, they will only contribute 
130 towards the location.
- **scrapsanity**: A value of True enables scrapsanity, which adds locations for collecting each scrap for the first 
time. Warning: adds >50 locations to the randomizer.
- **randomize_company_building**: When True, the company building becomes locked behind an item in the multiworld, 
preventing the player from routing there to sell scrap until they receive the required item.
- **randomize_scanner**: When True, the scanner becomes locked behind an item in the multiworld, rendering the player 
unable to scan until they receive it.
- **randomize_terminal**: When True, the terminal becomes locked behind an item in the multiworld, preventing its use 
until the player receive the item (in other words, the player cannot buy items or route to any moon other than their 
starting moon).
- **starting_moon**: This is the only moon the player will have access to at the start of a multiworld. All other 
moons are locked until received. This can be set to any moon name, or 'randomize', which randomly selects a starting 
moon. 
- **starting_stamina_bars**: Can be any number from 0 to 4, default is 4. The player begins with this many stamina 
bars, and the rest have to be unlocked.
- **starting_inventory_slots**: Can be any number from 1 to 4, default is 4. The player begins with this many 
inventory slots, and the rest have to be unlocked.
- **all_moon_required_grade**: Can be any of the following: s, a, b, c, d, or f. The end-of-day grade required to 
complete a grade location on a moon. This option will be ignored if split_moon_grades is true.
- **split_moon_grades**: Can be 'true' or 'false'. When 'true', the moon_grade option is ignored and the next three 
options are used instead. When 'false', the next three options do nothing.
- **easy_moon_required_grade**: The end-of-day grade required to complete a grade location on an easy difficulty moon 
(usually Experimentation, Assurance, and Vow).
- **medium_moon_required_grade**: The end-of-day grade required to complete a grade location on a medium difficulty 
moon (usually Offense, March, and Adamance).
- **hard_moon_required_grade**: The end-of-day grade required to complete a grade location on a hard difficulty moon 
(usually Rend, Dine, Titan, Artifice, and Embrion).
- **min_scrap_chance**: Can be any number between 0 and 10, default is 3. Scrap will not contain important items or be
required for the Collectathon goal if their spawn chance on an in-logic moon is less than this percentage. A value of 
less than 3% can significantly slow down games, while values above 6% exclude most scrap. This setting does nothing when
 scrapsanity is disabled.
- **min_monster_chance**: Can be any number between 0 and 10, default is 5. A bestiary entry will not contain 
important items if the monster's spawn chance on an in-logic moon is greater than or equal to this percentage. A value 
of less than 3% can significantly slow down games.
- **min_money**: Can be any number between 0 and 1000, default is 100. This is the minimum amount of money that a 
money item can give the player.
- **max_money**: Can be any number between 0 and 1000, default is 300. This is the maximum amount of money that a 
money item can give the player. This can't be less than min_money.
- **modify_scrap_spawns**: Can be 'true' or 'false'. When true, scrap spawn rates are modified in the following ways: 
    - all scrap on a moon have the same spawn chance
    - each moon spawns the same number of unique scrap, and those scrap cannot spawn anywhere else
    - a few scrap 'common' scrap are able to spawn on all moons
    - scrap that have special spawn conditions (apparatus, hive, shotgun, kitchen knife, and sapsucker egg) still 
    spawn on their respective moons
    This makes it a lot easier to find every in-logic scrap, which reduces the chance of a player getting stuck for a 
    long time trying to find a rare item that is blocking progression. 
- **exclude_killing**: Can be 'true' or 'false'. When true, scrapsanity locations that require the player to kill an 
enemy (Shotgun and Kitchen knife) will not contain progression or useful items.
- **exclude_hive**: Can be 'true' or 'false'. When true, the Hive scrapsanity location will not contain a progression 
or useful item.
- **exclude_egg**: Can be 'true' or 'false'. When true, the Sapsucker Egg scrapsanity location will not contain a 
progression or useful item.
- The following are filler items, and they fill the empty spots in the item pool according to their weight values, 
where higher weighted items will appear more than lower weighted items. All have a minimum of 0 and a maximum of 100
    - **money**: Default is 80. When redeemed, this item grants the player between min_money and max_money credits, 
    though they don't count toward the quota.
    - **birthday**: Default is 20. When redeemed, this item sends a random store item down in the dropship.
    - **weight_reducers**: Default is 5. These items reduce the carry weight of all scrap. Each strength training item
    reduces the weight of held scrap by (1 - 0.9^x)%, where x is the number of strength training items the player 
    possesses. 
    - **scrap_clone**: Default is 20. When redeemed, this item duplicates a random piece of scrap in the ship.
    - **time_add**: Default is 20. When redeemed, this item adds one day to the current quota (up to 9).
    - **time_trap**: Default is 30. When consumed, this trap reduces the remaining time to complete the current quota 
    by one day. If quota already has one day left, it'll wait until the next quota to remove a day.
    - **bracken_trap**: Default is 8. When consumed, this trap spawns a bracken on the current moon. If the player is 
    in orbit or at the company moon, this trap will activate the next time the player lands on a valid moon.
    - **haunt_trap**: Default is 4. When consumed, this trap spawns a ghost girl on the current moon. If the player is
    in orbit or at the company moon, this trap will activate the next time the player lands on a valid moon.
- **death_link**: Can be 'true' or 'false', when true turns on death link. When a party wipe occurs, a death link is 
sent, and when a death link is received, a random player dies.
- **death_link_percent_scrap_lost**: The percentage of scrap lost when the last living player dies from death link. 0 
means no scrap is lost, 50 means half of the scrap in the ship is lost, 100 means all scrap is lost. This option does 
not preserve scrap if the last player dies naturally, and does nothing if death link is disabled.
</details>

### Multiworld generation
<details>

Follow these steps to generate a multiworld with the Lethal Company apworld:
1. Once your YAML is configured, navigate to your MultiworldGG installation folder (the location will vary depending on 
where you installed Archipielago, but Windows users can generally find it in C:\Program Files\MultiworldGG). 
2. In the 'Players' folder, paste your YAML file as well as the YAMLs of any other players participating in the 
multiworld (Note: Only create one YAML per lobby of Lethal Company. For example, if 2 players plan to play in the same 
LC lobby and another player plays a different MultiworldGG game (or a different LC lobby), you would only need 1 YAML for
Lethal Company and 1 YAML for the other game). 
3. If you want to use AP: In AP's custom_worlds folder, paste lethal_company.apworld. 
4. Open the MultiworldGG Launcher and click Generate. This will generate a .zip file in the 'output' folder found in 
your MultiworldGG installation, in the same path where the Players folder is. 
5. Once the generation finishes, navigate to the [MultiworldGG website](/), select Start Playing, 
click 'host a pre-generated game', then select "Upload File" and upload the generated zip file in the 'output' folder of
your Archipelago installation. The game will generate along with the Spoiler log. 
6. Finally, select 'Create New Room', and you're done! The MultiworldGG server is now running with your multiworld!

</details>

### Setting up the mod
Run the game through your chosen mod installer (as you would usually start a modded LC game), and boot up a save. Once 
you are ready, you can type /connect multiworld.gg:*port* in the chat (**not** the terminal), then follow the 
instructions as they appear. Everyone in the lobby should connect when the host performs a /connect, but if anyone joins
late and *doesn't* automatically connect, they can type /connect with no arguments in the chat to connect themselves to 
the multiworld.

## Locations and items
<details>

In a multiworld, locations are objectives that, when completed, items for players. 
Lethal Company has the following locations:

- Log Entries(Excluding first log).
- Bestiary Entries.
- Completing moons on a set grade or higher as specified in the yaml.
- Completing a set amount of quota.
- Gathering each type of scrap for the first time if scrapsanity is enabled.

The items are:

- Moons
- Shop items
- Ship upgrades
- Inventory slots
- Stamina bars
- the Scanner
- Strength training (reduces the carry weight of scrap)
- Filler
    - Clone scrap (duplicate a random scrap in the ship)
    - Money
    - More time (extra days to complete a quota)
    - Birthday gifts (random store items in a dropship)
- Traps
    - Bracken trap (spawns a bracken)
    - Haunt trap (spawns a ghost girl)
    - Less time (reduced time to complete a quota)
</details>

## Useful Terminal Commands
<details>

`aphelp` - Displays this list of AP/MWGG-related commands.

`aptracker` - Displays all logically reachable locations.

`approgress` - Displays the player's current progress towards the chosen goal.

`apscrap [moon name]` - Displays the names of all scrap found on the specified and whether they are logically accessible.

`apscrap [scrap name]` - Displays the names of all moons that the specified scrap can be found on.

`aphint` - Displays all hints in your world that haven't been completed, where the item is, and whether the item is 
logically accessible.

`apconfig` - Displays the current value of all config settings, as well as what you can set them to.

`apconfig [setting name] [value]` - Sets a config setting to the specified value.

`apfiller` - Displays how many of each filler item has been received, as well as how many are available to be used.

`apfiller [item name]` - Uses a filler item if an item of that type is currently available to use.

`apworld [world name]` - Used only for advanced custom content. Allows the player to set the custom apworld's name.

`aplogic {copy|print|export}` - Retrieves logic used in custom apworlds.
</details>

## Adding custom scrap, monsters, and moons to the randomizer
<details>

EXPERIMENTAL FEATURE - WILL CHANGE OVER TIME, MAY BE BUGGY AND BROKEN
As of 0.6.0, APLC supports adding custom scrap, monsters, moons, and store items to the randomizer.
To set up a world with custom content, follow these steps: 
1. Install all custom content that you want to include. Boot up the game and create a new save file.
2. Interact with the ship terminal and run the command 'aplogic copy' to copy the logic string to your clipboard. If 
the logic string did not copy correctly, replace the 'copy' argument with 'export', navigate to the folder displayed on 
the terminal, and copy the entire contents of 'LogicOutput.json'. If this file is not present or the logic string is 
malformed, follow these steps instead:
    1. Close the game and install the [UnityExplorer](https://thunderstore.io/c/lethal-company/p/LethalCompanyModding/Yukieji_UnityExplorer/) 
    mod before repeating step 1.
    2. Open the UnityExplorer overlay with F7 if you do not already see it, then open the **C# Console** from the button
    at the top of the screen. 
    3. From the dropdown in the Console window, click **REPL**, then replace all content in the file with the following 
    line: APLC.Plugin.Instance.GetGameLogicString(); Click **Compile**.
    4. Open the **Log** window from the button at the top of the screen, then click **Open Log File**. If that does not 
    work, open the log file either using your mod manager or by locating it manually. Highlight the entire the logic 
    string, from the first { to the last }, then copy it. 
3. Find your lethal company.apworld file in your Archipelago folder and rename the file to lethal_company.zip. If you do
not see the .apworld file extension, you must first enable file name extensions in File Explorer or its Linux/Mac 
equivalent. Then, copy the lethal_company sub-folder into the custom_worlds folder. 
4. Inside the lethal_company folder, replace the contents of imported.py with 'data = ', then paste your logic string. 
5. Right click the lethal_company folder and select 'Send to', then 'Compressed (zipped) folder'. When prompted to name 
the file, change the '.zip' extension to '.apworld'.

Now, you can generate a multiworld using this apworld with the custom content.

### Using custom content in multiworlds with other lethal company games
If other players in your multiworld are playing Lethal Company with different mod packs, you need to to complete a few 
more steps to prevent your custom world from interfering with theirs.
1. First, you must choose a name for your game. Two Lethal Company players with different mod packs cannot use the same
name, as it's what keeps the apworlds from colliding. 
2. In the custom_content.py file, choose a name for your custom game and place it within the empty "" on the line that 
says 'name'. The file's contents should now look like this:
    ```python
    custom_content = {
        "name": "*your chosen name*"
    }
    ```
3. In archipelago.json, change the value of the 'game' field to "Lethal Company - *your chosen name*". Do not modify 
any other part of this file.
4. Rename the lethal_company folder to lethal_company-*your chosen name*, zip it back up, change the file 
extension back to .apworld, and change the apworld's name to lethal_company-*your chosen name*.apworld. 
5. Generate a new yaml file for this custom apworld. It *is* possible to recycle an existing yaml file, but you will 
need to open it and change **every** mention of Lethal Company to "Lethal Company - *your chosen name*".

Once this is complete, you can launch the game. Before you connect to the game, you must first enter the command 
'apworld *world name*' in the ship's terminal. This will sync your save file to the new apworld name, which will allow 
you to successfully connect to the multiworld using it. If you ever delete the save file or make a new one, you **must** 
run this command BEFORE connecting to a multiworld.

### Custom Content Disclaimers:
Multiworlds might be unbeatable with custom content. If this happens, let me know so I can improve the logic string 
generation method.

Custom content might be bugged, as testing with every possible modded moon/scrap/monster combo is not feasible.
If you run into any bugs, however, don't hesitate to either create a github issue or message me in the archipelago 
Discord server so I can work on fixing that bug.
</details>

## Credits
Thanks to my friends for helping me test this and fix a few annoying crashes. 

Thanks to everyone in the Lethal Company thread in the Archipelago discord server, who helped me fix a ton of bugs and 
get a bunch of ideas, without which this archipelago mod probably wouldn't be possible.

Thanks to Faxium for rewriting the setup portion of this guide, making it easier to understand.

Thanks to StevieSP for troubleshooting issues and helping other users in the Discord channel (for YEARS).

Thanks to ThisGuyHere for his feedback on bugs in the custom content system.
* And thank you T0r1nn for trusting me enough to take over development when you were unable to. - TGH

Thanks to Cupid for testing custom worlds and bringing awareness to numerous issues.

This project uses the Archipelago.MultiClient.Net library by Hussein Farran, Zach Parks, licensed under MIT.