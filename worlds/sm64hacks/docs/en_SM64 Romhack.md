# Super Mario 64 Hacks

This world supports most Super Mario 64 ROM hacks. It shuffles keys, stars, caps, cannons, and troll stars across the worlds. Star Revenge 3.5, 6.25, 7, 7.5, and 8 receive special support.

## Compatibility

Decompilation hacks are unlikely to be supported. The world uses MIPS assembly to make the game read from File 2; recompiling a ROM from source can shift the pointers that code relies on and cause it to fail.

Some complex binary hacks or hacks with many stars, including Decades Later and SM64OoT, are not currently supported. A future C library might make decompilation hacks compatible when their source is available and the hack is compiled with it.

## Getting a JSON file

MultiworldGG ships with several romhacks. For all others, check the [SM64 Hack Archipelago JSONs repository](https://github.com/DNVIC/sm64hack-archipelago-jsons) first. It likely includes a JSON file for major or popular hacks. When you generate a game with one of those files, its logic is downloaded automatically; only the JSON filename is needed.

For a hack without a JSON file, you can create one with the [JSON creator](https://dnvic.com/ArchipelagoGenerator/).

## Why is this separate from the regular randomizer?

The regular world supports vanilla Super Mario 64, including its PC port. This world adds Archipelago support for SM64 ROM hacks through an emulator.

## Why is BizHawk unsupported?

The connector is named the generic BizHawk client, but the supported emulator is Luna's Project64. BizHawk may work, but it has not been tested and support is not provided for it.

## Why are objects not randomized?

The available object randomizer is old and unreliable. If you want object randomization, run your ROM through the [Mario 64 Randomizer](https://github.com/aGlitch/Mario-64-Randomizer) after applying the ASM patch.

## Can additional features be randomized?

Suggestions are welcome, but this world is designed to work with most hacks. Features that need significant custom code or cannot be generalized across hacks can be difficult to add.

## Community and support

Use and discussion of this world are not allowed on the main Archipelago server. For help or to share a JSON file, join the [SM64 Hacks Discord](https://discord.gg/Nu4X9gmGDR).

## Planned work

- A better, more functional JSON editor
- Level tickets and move randomization
- Improved object and music shuffling
- Hack-specific custom items, including for SM64OoT
- A way to see in-game which items you send to other players

## Credits

- aglab2 — StarDisplay
- ShiN3 — ASM assistance
- SheepSquared, KingToad74EE, and Agyroth — testing
- HeralayanSalty — much of the connector script
- Awesome7285 — early bug finding
- Everyone who submitted JSON files to the repository
- The Archipelago worlds referenced during development
