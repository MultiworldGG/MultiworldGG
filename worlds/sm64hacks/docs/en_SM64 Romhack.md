# Super Mario 64 Hacks

Archipelago world for (most) Super Mario 64 Romhacks. Currently shuffles keys, stars, caps, and cannons throughout the worlds.
Any Decomp hack is not supported. Any binary hack with 8 stars per level is not currently supported, nor is Decades Later or Star Revenge 6.25.

## NOTE
Use and discussion of this apworld (unfortunately) is not allowed anymore in the main archipelago server. 
Please ask for support in our Discord, or join [this one](https://discord.gg/Nu4X9gmGDR) instead if you want help, or just want to share a json file.

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file. Please note that by default, the website only exposes a couple well known romhacks. If you want to use your custom hack, please generate locally.

## Anticipated Questions

Q: Why does this exist? Why not just use the regular randomizer?

A: I wanted to add sm64 romhacks to archipelago, since the "normal" world only supports vanilla sm64 (and even then, it's the PC port, while I prefer playing stuff via emulator)

Q: You said (most) romhacks, what hacks aren't supported?

A: Basically any decomp hack will probably not ever be supported since this uses MIPS assembly code to change certain parts of the game to read from File 2 (easiest way to implement it, sm64's code is a mess), and when you recompile a rom from source and edit basically anything, the compiler will shift all of these pointers the assembly code relies upon, which causes the assembly code to fail completely. 

Some more complicated binary hacks/hacks with a lot of stars, like Star Revenge 6.25 and Decades Later are not currently supported. Eventually, the goal is to get these hacks supported though.
In the far future, it might be possible to create little C library for decomp hacks, which if the hack is compiled with the library, the hack will be archipelago-compatible. Though that requires the hack to have its source code released, and it's a bit too much work for me for now.

Q: Why don't you support BizHawk even though this uses the "bizhawk client"?

A: BizHawk is a crappy emulator for SM64 hacks, it is not good at all for them, it will break in certain hacks. Whereas Luna's Project64 was literally made specifically for SM64 hacks. If you *really* want to use bizhawk, I have no way of stopping you. I will not provide support however, as I have no way of knowing whether or not it's a problem with my code, or just a problem with BizHawk

Q: Why aren't objects randomized?

A: The current "best" object randomizer for SM64 hacks is like 6 years old and super janky. If you want an object randomizer, put your rom through [this](https://github.com/aGlitch/Mario-64-Randomizer) after you apply the ASM patch. I'm planning on making a better one as part of this project, but it's a lot of effort.

Q: Can you randomize X?

A: Feel free to pitch ideas to me, but reminder that this world is meant to be generalized to most hacks. A lot of stuff either requires significant amounts of custom code (difficult to do without potentially infringing on already-existing custom code in current hacks), or is difficult to implement in a system that allows it to work for more than one hack.

## Future ideas (in approximate order of greatest to least priority)

* Better/more functional JSON editor
* Level tickets
* Move rando
* Better object and music shuffler
* Custom items for specific hacks (Badges in sr7/7.5/8, sm64oot, probably others im not thinking of)
* Ideas I have for dynamic locations that could be interesting
* Some sort of way to know what items you're sending to other people in-game
* Presets for major/important hacks (probably every megapack hack)

## Credits

* aglab2 - Making StarDisplay (referencing the StarDisplay code was really helpful in figuring out where pointers were)
* ShiN3 - Helping a lot with the ASM code (which doesn't exist anymore as it's now edited in RAM in the client)
* SheepSquared - Testing
* KingToad74EE - Testing
* Agyroth - Testing
* HeralayanSalty - Making a good bit of the bizhawk client connector script
* Everyone who submitted JSON files for the github repo
* A bunch of archipelago worlds I ended up referencing when making this.