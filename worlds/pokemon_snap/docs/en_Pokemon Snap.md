# Pokemon Snap

## Where is the options page?

You can read through all the options and generate a YAML [here](../player-options).

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

## Troubleshooting

### My AP won't connect

**Error:**
`Unable to connect to Project 64. Attempting again in 5 seconds...`

**Solution: Enable the AP script in Project64**

1. Open Project64
1. Ensure Debug mode is turned on (Options > uncheck "Hide Advanced Settings" > Apply)
1. Open the Scripts... Window (Debugger > Scripts...)
1. Select Script `ap_psnap_pj64_adapter_30.js` and press "Run"

---

### Oak won't Rate my Photos / There is a red dot when taking photos / Pikachu is detected as a Pokemon Sign

**Solution: Troubleshoot your base ROM**

This likely isn't related to the AP and is an issue with your emulator vs base Pokemon Snap ROM in general. 
Confirm by attempting to submit photos in your base ROM. The following steps have all been known to help:

 - Ensure you are using Project64 `3.0` NOT `4.0`
 - Swap to a different RDP plugin. Both the [angrylion-plus](https://github.com/ata4/angrylion-rdp-plus/releases) and [Parallel RDP Plugin](https://github.com/ariahiro64/pj64-parallelrdp/releases/tag/1.4) have been reported to work with Parallel having better performance.

---

### "Pokemon Snap Client Client Issue" / Permission Denied Error

**Error:**
```
An unknown error occurred while runing Pokemon Snap's Client.
Additional details:
[Win Error 5] Access is denied: `C:\\Program Files [x86]\\Project64 3.0\\Scripts'
```
**Solution: Run the Archipelago Launcher as Admin**

1. Close the Archipelago Launcher
2. Reopen the Archipelago Launcher as administrator (`Right Click` > `Run as administrator`)

---

### Select ROM path popup only shows .zip files as an option

This can happen if you accidentally selected the wrong file when initially selecting the ROM.

**Solution: Manually Target the ROM**

1. Navigate to the folder where the ROM lives
2. Type in the full file name manually, including the suffix

## General Questions

### How Do I Snap (whatever) with just the Dash Engine?
Dash and Snap at the same time! This wasn't required in the base game but is needed for some of the Randomizer logic.

---

### How Do I Snap Multiple Electabuzz without Zapdos to help out?

<details>
  <summary>Hint</summary>
  
  Be patient.
  
</details>

<details>
  <summary>Spoilers</summary>
  
  Multiple Electabuzz can be snapped without Zapdos by following these sick steps:
  1. Navigate to the room with the Pinsir Sign
  2. Ingore the first Electabuzz to your right as you enter the room
  3. Apple or Pester Ball the Second Electabuzz so it walks forward and shocks the machine
  4. After you go past it - line up your shot facing backwards, you should easily be able to capture the second Electabuzz in the background.
  
</details>

---

### How do I Snap Multiple/Good Technique Geodudes with no items?

<details>
  <summary>Hint</summary>
  
  Turn around
  
</details>

<details>
  <summary>Spoilers</summary>
  
  Multiple/Good Technique Geodudes can be Snapped with no items by following these sick steps:
  1. Watch the 2 Geodudes jump back onto the wall near where Sandslash jumps into the ground
  2. Look backwards at the close Geodude and snap the pic while the farther away one is in the background
  
</details>

---

### How come I was able to Snap (whatever) out of logic? / What does the "hard logic" option change?

The locations below default to using "soft logic" in a normal playthrough, but can actually be photographed
with fewer items. Some of them are quite difficult, and have had the soft logic applied to keep the randomizer fun.

The soft and hard logic requirements are listed below.

#### Beach
- Lapras: Good Technique / Multiple
  - Soft Logic: 5 Film
  - Hard Logic: 2 Film

#### Tunnel
- Pikachu on a Ball
  - Soft Logic: 5 Film
  - Hard Logic: 3 Film
- Kakuna: Multiple
  - Soft Logic: Pester Balls, Pokemon Food, or the Dash Engine
  - Hard Logic: Nothing
- Dugtrio: Normal / Good Technique
  - Soft Logic: 5 Film
  - Hard Logic: 4 Film
- Dugtrio: Multiple
  - Soft Logic: 7 Film
  - Hard Logic: 5 Film

#### Volcano
- Vulpix: Multiple
  - Soft Logic: Pokemon Food
  - Hard Logic: Dash Engine
- Charmander: Multiple
  - Soft Logic: Pokemon Food
  - Hard Logic: Nothing

#### River
- Poliwag
  - Soft Logic: Pokemon Food or Pester Ball
  - Hard Logic: Nothing
- Shellder: Good Technique / Multiple
  - Soft Logic: Dash Engine
  - Hard Logic: Nothing
- Metapod: Good Technique / Multiple
  - Soft Logic: Pester Ball
  - Hard Logic: Nothing
- Speed Pikachu
  - Soft Logic: 5 Film, Pokemon Food, or Pester Ball
  - Hard Logic: 2 Film

#### Cave
- Grimer: Good Technique
  - Soft Logic: 4 Film
  - Hard Logic: 2 Film
- Muk: Normal / Good Technique
  - Soft Logic: Pester Ball and 4 Film
  - Hard Logic: Pester Ball and 2 Film
- Pikachu: Normal / Good Technique
  - Soft Logic: Pokemon Food or Pester Ball
  - Hard Logic: Nothing

#### Valley
- Squirtle: Good Technique
  - Soft Logic: Pester Ball
  - Hard Logic: Nothing
- Squirtle: Multiple
  - Soft Logic: Pester Ball
  - Hard Logic: Dash Engine
- Graveler: Good Technique
  - Soft Logic: Pester Ball or PokeFlute
  - Hard Logic: Nothing
- Graveler: Multiple
  - Soft Logic: PokeFlute
  - Hard Logic: Nothing
- Starmie
  - Soft Logic: 5 Film
  - Hard Logic: 2 Film
- Starmie: Good Technique
  - Soft Logic: 7 Film
  - Hard Logic: 2 Film
- Starmie: Multiple
  - Soft Logic: 9 Film
  - Hard Logic: 3 Film