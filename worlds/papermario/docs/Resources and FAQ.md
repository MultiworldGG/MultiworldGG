# Resources

## AP World

- [AP PMR Release Page](https://github.com/icebound777/PMR_APWorld/releases)
- [Sample YAML,](https://github.com/icebound777/PMR_APWorld/blob/main/docs/PM%20Sample.yaml) which has notes for what settings are and aren't implemented
- [Options Syntax and Explanations](https://github.com/icebound777/PMR_APWorld/blob/main/options.py)

## Paper Mario Randomizer

- [PMR Site](https://pm64randomizer.com/)
- [PMR Wiki](https://github.com/icebound777/PMR-SeedGenerator/wiki), with easily missable locations, tips, and a logic guide
- [Nintendo Power Official Strategy Guide](https://ia801606.us.archive.org/6/items/PaperMarioNintendoPowerOfficialStrategyGuide_20170328/PaperMarioNintendoPowerOfficialStrategyGuide.pdf)
 complete with maps, item locations, recipes, and more.

## Trackers

- [Pop Tracker Pack by ObsidianMaker, based on Phantom's](https://github.com/boiscljo/pmr-tracker/releases) Currently the most up to date tracker. Can autotrack via AP integration
- [Web Tracker by Yami](https://pm64r-tracker.mryami.xyz/), has AP integration: Use the :apcolor: button in the top left.
- [Web Tracker by Scatter](https://pmr-tracker.christianlegge.dev/) (no autotracking)
- [Emo/Pop Tracker Pack by Phantom](https://github.com/Phantom5800/pmr-emotracker/releases) **OUTDATED, CANNOT AUTOTRACK**. Emo Tracker packs can be opened and used in Pop Tracker.

You can view the key item tracker in your in-game inventory and view the map for checks remaining in an area

## First Time Players

### This is my first time playing PMR. What should I know before I dive in?

See the [Paper Mario Randomizer (PMR) Wiki](https://github.com/icebound777/PMR-SeedGenerator/wiki)
for a full list of useful features added by the base mod, a logic guide, a list of commonly missed locations, and more.
If you don't want to read through everything, here are a few highlights:

- Items found in blocks, trees/foliage, chests, lying on the ground, or given by NPCs are all shuffled.
- You start with the Homeward Shroom as a key item. Using it can bring you back to your spawn location at any time.
- The base mod has built-in trackers in the Maps and Key Item Tracker sections in the pause menu. External trackers can  
still be quite helpful, but these can be handy for checking what items you have and if any checks remain in an area.
- It's recommended to use `cutscene_mode: shortened` instead of `minimal` if you don't know puzzle solutions.
- You need coins to buy items from shops, and given how many shops are available at the start, you might be expected to
buy several things. It's not a bad idea to start yourself off with 200-300 coins just to be safe.
- If you decide to allow very many consumables to be off-world, you may want to be careful with your inventory,  
particularly in an async game. Make sure to sell or store items as your inventory fills up, and maybe head to a shop  
before you connect to a game where you might be receiving a bunch of consumables.

### I can't remember... how does that one thing work?

- Panels can be flipped using Super Boots or Ultra Hammer.
- Yellow blocks can be destroyed by hitting them with hammer or by using Bombette.
- Trees can also be shaken using Bombette.
- Floating blocks can be hit by using Kooper's ability.
- Rowf's shop gets more items with every Star Spirit found up to the fifth. You can talk to him to change his inventory.

- Koopa Koot has three new requests with every Star Spirit found up to the sixth. You have to do them in order.

- Parakarry needs any 3 letters to get his partner check.

- To open the gate to Gusty Gulch, you need to have the Boo Portrait item and speak to Lady Bow in Boo's Mansion.

- To enter Shy Guy's Toybox, you must hide using Bow's ability in the house just before you reach Toad Town's port.
- The jack in the boxes in Shy Guy's Toybox can be activated with hammer, no spin jump necessary.
- To solve the color blocks puzzle, give Russ T. (he lives near Toad Town's gate) his Dictionary and the Mystery Note.

- To get to Mt Lavalava, you must use the Jade Raven on the statue in Jade Jungle and talk to Raphael in the huge tree.
- The Bub-ulb in Jade Jungle's seed was taken by Kolorado; to get the item, give Kolorado the Volcano Vase.

## Frequently Asked Questions

### What do the prefixes in front of the location names mean?

| Prefix | Region                                                                         |
| ------ | ------------------------------------------------------------------------------ |
| GR     | Goomba Region                                                                  |
| TT     | Toad Town                                                                      |
| TTT    | Toad Town Tunnels                                                              |
| SSS    | Shooting Star Summit                                                           |
| KR     | Koopa Region                                                                   |
| KBF    | Koopa Bros Fortress                                                            |
| MR     | Mt Rugged                                                                      |
| DDO    | Dry Dry Outpost                                                                |
| DDD    | Dry Dry Desert                                                                 |
| DDR    | Dry Dry Ruins                                                                  |
| FOR    | Forever Forest (+ the exterior of Boo's Mansion)                               |
| BM     | Boo's Mansion                                                                  |
| GG     | Gusty Gulch                                                                    |
| TC     | Tubbas Castle                                                                  |
| SGT    | Shy Guys Toybox                                                                |
| JJ     | Jade Jungle (+)                                                                |
| MLL    | Mt Lavalava                                                                    |
| FLO    | Flower Fields                                                                  |
| SR     | Shiver Region (+ Starborn Valley and Shiver Mountain)                          |
| CP     | Crystal Palace                                                                 |
| BC     | Bowser's Castle                                                                |
| PCG    | Peach's Castle Grounds (+ the area between Toad Town and Shooting Star Summit) |
| PC     | Peach's Castle                                                                 |

### What do N1W3 and S2E1 mean in Dry Dry Desert?

The prefixes for the desert areas indicate what direction they are from the center  
(which is the screen with the stone cactus.) N means north, or up, while S means south, or downwards.  
E means east, or right, while w means west, or left. Be careful with east and west if you have mirror mode turned on.

### How am I supposed to know what I'm buying from the shop?

Items sold in shops or found in Merlow's item rewards will be automatically hinted if they are progression items. If  
they are unhinted, they are not progression items. Items are not able to have names and descriptions in the current  
version of the base mod, so this is the best workaround to make sure you don't waste any hard earned coins on filler  
items. Note that the items sold by Merlow are never going to be progression, as you require every star piece in the  
game to buy all of them.

### Why is the item I was sent not in my inventory yet?

Currently, items are granted while you are in the overworld on a one second loop by the game, and the items are written into the game on a one second loop by the Bizhawk Client for Archipelago. They will not continue to flow into your inventory while in battle, paused, transitioning between screens, in dialogue, and so on. This means when several items are queued to be received, it may still take some time for the item to show up. If it seems clear that no more items are showing up and you are still missing one or more items, please reach out to us in the Paper Mario thread in the Archipelago discord.  
