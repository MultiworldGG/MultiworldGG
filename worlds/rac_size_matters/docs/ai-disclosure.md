# AI Disclosure
This apworld is not done entirly by hand I used AI to help me decomp function calls as well as generate the basic boiler plate for this apworld. I use it to speed up time and to help with complicated functions/logic that are required for the game to run. 

## Ghidra and PCSX2
I use both Ghidra-MCP and Pine-MCP with AI. my process is to find the memory region myself or using addresses found by others and attempt to understand what function calls are interacting with the address, if i get stuck and cant figure out something i just Ghidra-MCP to help disassemble the function call, Pine-MCP is for checking live values on emulator to help with Ghidra-MCP decomp. I am not amazing as decompiling manually however i do find the memory regions myself and dont rely on AI for everything as it can be wrong.

Patches to the game with the Live Patch implementation I am using are written by hand I dont use AI for pcsx2 patches as that would take all the fun out of making an AP World. They are initially written as PCSX2 patches then transfered over to python for this implementation. Saying that i do use AI to assist in writing the python implementation of each patch, this is to help ensure i am converting them correctly.

## Documentation
Documentaion and other aspects are generated initially, this disclosre isnt as i tought it would be better to manually write however when a new option is added it gets added to the documentation automatically. As well as the initial documentation for the AP world.

## Programming
Core logic has AI code in it, when creating function calls and other logic i initially write a function and use AI to improve or attempt to improve the preformance out of the function to make it shorter and easier to maintain in long run. I review each function call and piece of logic by hand but that doesnt mean ive written this entirly by hand. I also use AI to quickly implement some new feature or new patch logic to see if it would work, this means i can make multiple PCSX2 patches for a feature, and quickly test them instead of writing that conversion by hand for every test. 

I also use AI for tedious tasks in the apworld. this includes the initial boilerplate of the AP world, i didnt know an APWorld generator existed at the time of implementing SM. Pine communication and implementation are originally done by hand with struct class layout done by hand. Converting of logic, what this means is over the course of this APworlds lifespan i restructured Size Matters APworld multiple times this is due to rushed implementation over quality and will continue to have some more restructuring to remove outdated function calls and logic. One such example would be the Locations, when changing over to a more rule builder appraoch instead of copying and pasting the location class a couple hundred times i used AI to speed up that process so i could get a release done in a week rather than in month. 

Not everything in this APworld is done by AI but not everything is done by hand aswel, its why i made this document earlier and why with the latest rules changes i wanted to make sure i include more information than what was stated in it was previously. 

## Why I use AI in my APWorld

I understand my apworlds will not be as amazing as hand crafted ones, i chose the games i did as no one has shown an interest into making AP worlds for them. I wouldn't take on an APworld if there was any interest by someone else before hand. If someone does want to make a hand crafted APWorld of the games i make id happly step back and let them, and even provide addresses, memory anything to help them. There is a vast difference between AI worlds and hand crafted APWorlds.

Hand crafted worlds deserve the praise they get as they do massive improvements and require a lot of knowledge and skill to make.

An AI disclosure has always existed in the AP world in the README however im not sure people actualy read those. I also want to stress i keep my AI code to my own repos i dont feel it is fair to make PR's to someone elses work without it already being tainted by AI. 
