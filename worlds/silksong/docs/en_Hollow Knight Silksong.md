# Hollow Knight: Silksong

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a config file.


## What is randomized?
The world can randomize Silksong checks and progression items, including movement abilities, tools, crests, maps, mask shards, silk skills, fleas, and other useful or filler items. Traps may also be enabled depending on the generation settings.

The exact checks and options available can change as the randomizer develops. Use the generated YAML template and the release notes for the current version.


## Frequently Asked Questions (FAQ)

### I Got to Act 3 and Missed Some Checks in Act 2?
Some items become unavailable once you enter Act 3. Go to your Bellhome in Bellhart. 
Once you reach act 3 once, sit on the bed, press dash + needolin to get a pop-up asking to revert the world back to Act 2 and vice versa.

### What Are the Map Markers Showing?
When enabled in the yaml "location_map_markers", the map can show randomized locations at their physical locations.

Key for these markers are as follows:
- **Fully opaque (with AP style rosary icon)**: Reachable / in logic.
- **Half transparent (with AP style rosary icon)**: Not reachable / not in logic.
- **? / inverted icons**: Missing logic so far / guaranteed junk.

### I’m Stuck Somewhere, What Do I Do?
**Press F4.**

Seriously. It allows warping to homepoints like Bone Bottom, Bellhart, and Songclave as you reach them, skips the widow cutscene to stop softlocks and can save you from the slab. 
Also you can press F3 and it'll allow changing of warp locations as of v0.4.3.

### Do You Have a Feature like Benchwarp?
Short answer, no. Please refer to I’m stuck somewhere, what do I do?

Long answer, it can cause softlocks and other issues, it can be used but at your own risk of issues and potential woodchipper related incidents.


## Feedback and Bug Reports

Please report bugs and logic issues through the repository's [issues](https://github.com/Batatvideogames/silksong-archipelago-randomizer/issues) page. Include enough information to reproduce the problem, but do not upload save files containing personal information.

A second place to give this feedback can be this [Google Form](https://forms.gle/bAsQ2o453eccpL2i7).

A [Trello board](https://trello.com/b/as8YLuLA/skonging) is also available to post known bugs, what's been fixed, and what's upcoming.


## Credits

A huge thanks goes out to all that support the channel and thread, the logic mapping team, playtesters, mod developers, and others who have helped contribute to this project:

### Logic Mapping

Some of these regions are still incomplete and still being mapped out. They've been placed in UNMAPPED.

| Contributor | Regions |
| :--- | :--- |
| **Herchey** | [Bilewater](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/bilewater), [Sinner's Road](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/sinner-s-road) |
| **Heric** | [Memorium](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/memorium) |
| **Hero** | [Bone Bottom](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/bone-bottom), [Deep Docks](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/deep-docks), [Far Fields](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/far-fields), [Hunter's March](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/hunter-s-march), [Moss Grotto](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/moss-grotto), [The Marrow](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-marrow), [Weavenest Atla](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/weavenest-atla), [Wormways](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/wormways) |
| **Isssma** | [Greymoor](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/greymoor) |
| **Pyxl** | [Bellhart](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/bellhart), [Grand Gate](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/grand-gate), [Mount Fay](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/mount-fay), [Putrified Ducts](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/putrified-ducts), [Sands of Karak](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/sands-of-karak), [Shellwood](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/shellwood), [The Abyss](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-abyss), [The Cradle](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-cradle) |
| **Rebel** | [Cogwork Core](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/cogwork-core), [Underworks (East)](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/underworks), [Whispering Vaults](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/whispering-vaults) |
| **Sergio** | [Choral Chambers](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/choral-chambers), [Grand Gate](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/grand-gate), [High Halls](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/high-halls), [The Slab](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-slab), [Underworks (West)](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/underworks), [Wisp Thicket](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/whisp-thicket) |
| **Skai** | [Blasted Steps](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/blasted-steps), [Grand Gate](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/grand-gate), [Whiteward](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/whiteward)|
| **SuperEpicGuy** | [Moss Grotto](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/moss-grotto) |
| **UNMAPPED** | [The Mist](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/the-mist), [Red Memory](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/red-memory), [Verdania](https://github.com/zerounit-dev/silksong-rando-ap-logic/tree/main/verdania) |

### Contributors
A huge thanks to all the people who have contributed to this project including ones that aren't displayed on the contributors list.

<a href="https://github.com/Batatvideogames/silksong-archipelago-randomizer/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Batatvideogames/silksong-archipelago-randomizer" />
</a>

- [HeroUnit](https://github.com/zerounit-dev) for his great work on standardizing logic for this project and largely handling all logical coordination.
- [TheMathGeek314](https://github.com/TheMathGeek314) for the original [HK Alphabet Rando](https://github.com/TheMathGeek314/AlphabetRando) and for giving permission to extend their idea to Silksong.
- [Nix](https://github.com/Nix-main) for [SilksongArchiDisplay](https://github.com/Nix-main/SilksongArchiDisplay) and all the additional help with [Cogfly](https://github.com/Nix-main/Cogfly) support.
- [FarisTheAncient](https://github.com/FarisTheAncient) for a ton of help with archipelago compliance and consistent help with making things work with [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases?q=Tracker).
- RainingChain and IdoManti for their incredible work on documenting Silksong's map and providing us the image files to be used for UT and our logic tool. The map can be found on [Scripter's War](https://scripterswar.com/silksong/map).