# ArchipelagoOoA
This is an apworld for The Legend of Zelda: Oracle of Ages that takes an Oracle of Ages (US Version) ROM, and uses Archipelago to generate a new seed for you to play using your preferences according to the options in the Options.py file and settings in the Settings.py file.

## NOTE:
The common folder is not fully implemented yet. If there are things pointing to the common folder and their files don't exist, that's because they all came from this [repository](https://github.com/josephanimate2021/Tloz_oo_common) that is supported
for both ages and seasons that is currently being worked on and pending PR'd to Ishigh1's [repository](https://github.com/Ishigh1/Tloz_oo-common). Thank you for your patience.

Also, thank you for pointing that out SenPierre.

## Options I am thinking about addding.
* Shuffle Business Scrubs - Just like in Seasons, there are business scrubs that sell items to you for a certain price. Just like in Seasons Archipelago Randomizer, we can carry that over.
* Placed Essences - In Seasons Archipelago Randomizer, you can set how many essences are placed in the world. Well with Ages, I figured why not apply ths same logic as well. This will make some dungeons barren while the Required Essences option is set which makes more sense so that the user isn't just going into a dungeon with junk items and getting an essense at the end. This will cause them to get more essenses than what they need.
* Shuffle Essences - In Seasons Archipelago Randomizer, when that option is set, Essences will be placed anywhere in the world instead of dungeons.
* Exclude Dungeons Without Essence - This option will make dungeons without the essences barren by filling it with junk items (and locking the user out of the dungeon anyway with unreacable keys) just like in the Seasons Archipelago Randomizer.
* Show Dungeons With Essence - When the Exclude Dungeons Without Essence is enabled, you will see what dungeons have an essence on the minimap, making it easier for you to find out which dungeons are barren just like in the Seasons Archipelago Randomizer.
* Randomize Fairies Woods - in Ages, you are required to get a flute for your chosen animal conpanion in order to get to Symmetry City in the present. But to do that though, you will need to go to Fairies Woods for a second time where the bunnies will randomize the path again. From there, you will need to find your animal conpanion. Once you found it, you are given a flute for that animal for your effort. I am thinking of putting that check in sequence so that users have another fun way of playing the randomizer. It won't be too hard, it will just be interesting.
* Enforce Potion in Shop - In both Ages and Seasons, when you run out of Hearts, if you bought/got a potion, it will automaticly kick on and refresh your life. This option is already a thing in the Seasons Archipelago Randomizer, but this apworld does not have that option, so I am putting that in the works for this exact reason.
* Randomize AI - In Seasons, in the month of April, there would be an option where users can randomize how an enemy behaves around link. For example, a moblin could be shooting out balls whereas a knight could act as a moblin, and other possibilites like that. I think this will make things go crazy but I think that it will be really funny to introduce the same thing in Ages as well.
* Include Cross Items - In Seasons Archipelago Randomizer, you would need the Ages Rom in order to include items such as a switch hook, bombchus, seed shooter, and etc. This can make progression easier depending on the type of item a user got. I am considering adding the same thing to Ages except a Seasons Rom would be needed to include things such as Roc's Cape (useful), Rod of Seasons (useless but can kill/knockback some enemies), and Seed Slingshot (not as percise as the seed shooter). There are items such as a magnetic glove included at one point in the OG Ages Randomizer, however, it is no use so that won't be included.

## Current New Options that are functional that are not in the original apworld repo.
* duplicate seed trees - In Ages, there are 10 seed trees (8 of which are selectable) and 5 seed types. This causes duplicate trees to occur just like in Seasons. In order to give users a freedom to customize what trees are duplicates, this option was added. This was created by [Glan9](https://github.com/Glan9) on github, not myself. So please don't give me credit for this option.
* heros cave - In Ages, people say that you can complete hero's cave after D7, but I am starting to dobut that. To be fair I don't recall playing this part of the game, only the unlinked parts so I won't remember as much as some people think. With that, this option allows you to open up an entrance to hero's cave on the right side of the maku tree entrance and adding logical checks in the process.
* lynna gardner - In Flamestripe's Fork of the OoA Apworld (Not Tested), you could enable this feature to cut down on having to use a weapon or something like that to cut the grass each time to get to lynna city. This impacts the logic for lynna city and can make a difference in gameplay.
* rolling ridge old men as locations - This option allows you to convert the old man locations in rolling ridge into checks that you can get. Sure, there's only 2 of them, but it's still worth an add.

## Building
In order to build this code for usage with Archipelago, you need to follow these steps:
1. Download the source code by clicking on Code -> Download ZIP
2. Extract the zip file where you will see a folder called ArchipelagoOoA-<BRANCH_NAME> for which BRANCH_NAME will be ooa as that's the current branch this source code is on.
3. You may need to download Python 3.13 if you don't have it, because Archipelago does not support the latest version of Python yet. The link is [here](https://www.python.org/downloads/release/python-31312/).
4. Open your Terminal inside the extracted Archipelago Folder and type in this command: python Launcher.py
5. If this your first time launching Archipelago, you may be prompted with a few things to install. Once that's done, Archipelago will launch just fine, and that will allow you to manually test this apworld out for yourself.

## Want to colloborate?
Here are two ways to get in!
1. (Something most developers prefer and I'm fine with it): Fork this repository, create any changes you want, test your changes, and then send a PR to this repository explaining how your it will improve the apworld along with videos and screenshots of testing being done (If you don't have any of that, that's fine. I don't mind testing things myself, but my recomendation of you doing that saves me time).
2. DM me on discord (josephalt7000) and provide me with your GitHub Name. I will add it to my collobrators list with your prefered settings. Your options are read (default role if you choose option 1), triage (improvement from read this time you can manage issues and PR's), write, maintain (not as powerful as write but hey you now get to manage repo settings along with things mentioned in the traige and read options), and admin (you are basically the god of the repo at that point). Once i've added you, you will get an email invitation to this repo that is only valid for one week. If after one week you can't get it, please remind me on my discord DM that your invitation has expired and I'll add you again. Please don't be doing this repetively and just accept the invite. You chose to get invited to the repo and your invite expiring and you not saying anything tells me that you changed your mind unless you tell me otherwiese.

## Thought I was done there? Well there are some requirements that you need to meet in order to colloborate:
* You need to know Python. This apworld was built for Archipelago using that language.
* You need to understand the innerworkings of an Archipelago APWorld. You may start learning [here](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/apworld%20specification.md).
* I highly recommend that you download this [symbol](./docs/ages.sym) file of the game. It will help you read memory addresses more easily which will help you blend in to the requirements of having knowledge of debugging gameboy games with the [bgb](https://bgb.bircd.org/) emulator. You can also just read the symbol file as if it were a text file. You can do which ever you prefer as long as you meet this requirement.
* You need your own legally dumped Oracle of Ages ROM either for playtesting or a full randomizer walkthrough. I cannot legally provide you with a ROM if you don't have one, sorry.
* You need Archipelago v0.5.1 or newer installed in order to test this apworld (I recommend cloning this repo into the lib/worlds folder inside Archipelago that way you don't have to repackage the world every time during testing. And you can just commit your changes while not having to worry about repeating the same steps repetively).
* You need to have a full understanding of how the oracles randomizer works.

## Want to test the latest build of Archipelago with this world?
Visit [here](https://github.com/josephanimate2021/ArchipelagoOoA-withApSourceCodeBuiltIn) and follow these steps:
1. Go to Code -> Copy icon next to the URL and click on it.
2. Open your terminal and run git clone and then the url you just copied. Be sure to add the --recurse-submodules arguement to the command otherwise you may be recieving just a build with archipelago without my world in it. If you don't have Git installed on your computer, download it [here](https://git-scm.com)
3. Once that's cloned, head over to the Archipelago Folder and look for a file called Launcher. double click on it (assuming your default launcher is Python) and wait for it to do it's thing. You may need to follow some additional steps so just be warned of that.
4. Once Archipelago is launched, use it like how you would with any other archipelago installation to test my world. if you did things correctly, once you click on the Gneerate Template Options button, my world should be in there. The file name is The Legend of Zelda: Oracle of Ages.yaml

## Requested Features that are being worked on:
* Ambi's Palace As a Dungeon - Normally, i would not consider Ambi's Palace to be a dungeon, but a commenter from [mashy's video](https://youtube.com/watch?v=MgDrlOFINCc&lc=Ugwu35obzAjzsDfILW54AaABAg.ATVsNVmdbgUATY7u6h5N8x&si=l9zuUlHtL72z8dTJ) requested for this feature to be added. side entrances will stay in tact
