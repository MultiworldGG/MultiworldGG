# Pokemon Snap Randomizer FAQ

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