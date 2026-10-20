# Pokémon Snap Archipelago World

Original forked from [ArsonAssassin's PSAP World](https://github.com/ArsonAssassin/PSAP).

Note: To use this repository, you must already have a legally acquired English ROM for Pokémon Snap (sha1: `edc7c49cc568c045fe48be0d18011c30f393cbaf`). It is **NOT** provided for you as part of this repository.

## Setup

See [Setup Instructions](docs/setup_en.md) for set up and [FAQ](docs/faq_en.md) for troubleshooting.

## AP World Details
### Checks
* Submitting a picture of every Pokémon (62)
* Submitting a wonderful picture of every Pokémon (62)
* Submitting pictures with multiple of the same Pokémon in them (34)
* Submitting pictures of Pokémon in special poses (11)
  * Beach: Surfing Pikachu, Pikachu on a Stump, Gust-Using Pidgey
  * Tunnel: Pikachu on a Ball
  * Volcano: Fighting Magmar
  * River: Speed Pikachu
  * Cave: Balloon Pikachu, Flying Pikachu, Jigglypuff on Stage, Jigglypuff Trio on Stage
  * Valley: Graveler's Group Dance
* Submitting pictures of the Pokémon Signs (6)
  * Kingler Rock, Pinsir's Shadow, Koffing Smoke, Cubone Tree, The Mewtwo Constellation, and Dugtrio Mountain
  * Requires the Pokémon Sign Detector item
* Taking the Secret Exits in Tunnel, River, and Valley
* Receive Oak's rewards for your PKMN Report
  * 3 Checks for Photo Count: 6, 22, and 40 photos
  * 3 Checks for Report Score: 24,000, 72,500, and 130,000

### Unlocks
* The six courses: Beach, Tunnel, Volcano, River, Cave, and Valley (start with a random one)
  * Each course unlock can be split into up to six "map fragments"
* Pokémon Food (a.k.a. Apples), Pester Balls, Pokéflute
  * Optionally can be unlocked per course, rather than globally
* Dash Engine (can be enabled from the start)
* Pokémon Sign Detector (custom AP item)
* Film Capacity Upgrades
  * Start, Upgrade Amount, and Max Film are all customizable
* "Good Technique" and "Multiple Pokemon" Scoring (optional)
* Press L to Stop (custom, optional unlock)

### Win Condition
* Unlock the Rainbow Cloud course by finding the required amount of Pokemon Sign Pictures or Pokemon Pictures (may be in others' worlds!)
* Submit a picture of Mew (requires the Pester Ball or Pokémon Food)
  * Optionally can require a "Good Technique" photo of Mew

## Guide

A decent guide to all the photos, poses, and signs can be [found here](https://strategywiki.org/wiki/Pok%C3%A9mon_Snap/Walkthrough).

Need a hint? Categories have been set up to help:
 - `!hint Pokemon Pictures` and `!hint Sign Pictures` will give you hints specific to your goal condition (Default goal is Sign Pictures)
 - `!hint Courses` or `!hint Fragments` will tell you about your current courses and the next progression course
 - `!hint Tools` will tell you about your current tools and your next progression tool
 - `!hint Scoring` will tell you where your score upgrades can be found

Stuck? Check out the [FAQ](docs/faq_en.md).

Still stuck? Ask in the [Discord channel](https://discord.com/channels/731205301247803413/1528972845479100617)!

## Tracker

A poptracker pack made by [@lighting8282](https://github.com/lighting8282) for this world can be [found here](https://github.com/lighting8282/Pokemon-Snap-AP-Pop-Tracker/releases).

## Credit

Thanks to [@ArsonAssassin](https://github.com/ArsonAssassin), [@GerbilJames](https://github.com/gerbiljames), and [@SomeJakeGuy](https://github.com/SomeJakeGuy) for initial repository setup and doing 90% of the work to get this functional.

Thanks to [@AliRobotnik](https://github.com/AliRobotnik) for the Pokémon Snap Manual, which already had all the logic implemented, along with custom items.

Thanks to [@cobyw](https://github.com/cobyw) for setting up better testing, logic tweaks, and gameplay improvements. (And maybe more to come?)

Thanks to [@OniHelix](https://github.com/OniHelix) for the launcher icon.

## Pokémon Snap Archipelago AI Usage Disclosure
- Pokémon Snap Archipelago is **not** vibe-coded.
- Pokémon Snap Archipelago does **not** contain AI art.
- Conversations with LLMs have been used to gain insights about the repository and brainstorm ideas for improvements. All ideas and insights pitched by LLMs are read by a human before being implemented. Generally, all new code by me, [@nielrenned](https://github.com/nielrenned), is handwritten and hand-tested.
- The [repository that this was forked from](https://github.com/gerbiljames/PSAP) **did** use LLMs to generate some code that is in the patch file. The amount of code that was LLM-generated vs. by a human is unknown. The generated code has been reviewed and tested by multiple humans. All that code is contained in the commit on `main` with short hash `771f72d`.
