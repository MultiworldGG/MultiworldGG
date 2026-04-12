# MultiworldGG Randomizer for Path of Exile (PC)


## What does randomization do to this game?

This `.apworld` does not modify Path of Exile directly, it:
- Reads your character data through an API.
- Reads your PoE client logs.
- Writes to an item filter (and can place audio files) to highlight AP items.
- Checks that you are using the items / gems that you have received. And sends checks when you find new items or level up.

## What items and locations get shuffled?

### Locations (checks)
- Finding certain base item types that drop from monsters (e.g., a specific sword base).
- Leveling up.

### Items (unlocks)
- Available characters
- Ascendancies
- Passive skill points
- Ability to equip certain gear rarities
- Ability to equip flasks
- Maximum allowed number of linked sockets
- Utility gems (auras, movement skills, curses, etc.)
- Skill gems (active attack/spell abilities)
- Support gems (that empower skill gems)


## How It Works (Read-Only Integration)

### Core loop
1. **Enter a zone** → the client validates your current gear and progression.
2. **Pick up items** → The filter should make clear what items will unlock things.
3. **Enter a new zone** → “checks” are sent for newly found items/conditions.

## What does another world's item look like in Path of Exile?
- Items from other players will be highlighted in your item filter.
- If enabled there will be audio cues for what an item will unlock when you pick it up and change zones.

## Options

### Configurable goals
- Finish acts / complete the campaign
- Kill endgame bosses

### Configurable Items

**Characters & Classes:**
- Starting character class (Marauder, Ranger, Witch, Duelist, Templar, Shadow, Scion)
- Additional character unlocks (optional)
- Ascendancy classes (0-3 per character class)

**Equipment & Gear:**
- Gear rarity restrictions (Normal, Magic, Rare, Unique)
- Starting gear allowances (weapon, flask slots, gems)
- Flask slot upgrades (up to 5 total)
- Support gem socket limits (linked sockets for gem combinations)

**Skills & Progression:**
- Passive skill points (can be restricted and unlocked through items)
- Skill gems (active attack/spell abilities)
- Support gems (enhance and modify skill gems)  
- Utility gems (auras, movement skills, curses, buffs)




**Quality of Life:**
- Text-to-Speech announcements for found items
- Configurable TTS speed (50-500 WPM)
- DeathLink integration (share deaths with other players)

**Item Distribution:**
- Minimum items per act (ensures progression isn't completely blocked)
- Gear upgrades, flask slots, and support gem slots distributed per act
- Skill gem availability scaling with acts

**Misc:**
- Gucci Hobo Mode (extreme equipment restrictions - unique items only) -- Would not recommend.

---
Example options:
I want to use my own end-game character, and go from nothing to mapping to a boss.
- Disable levels as checks.
- Enable passive skill points as unlocks.
- Respec my character, removing all passive points, and start with no gear.
- enable boss as a goal
- add my class in the "starting inventory" section.
  ```
    start_inventory:
    # Start with these items.
    {
      "Ascendant": 1,
    }
--- 
## What do I do if I encounter a bug with the game?
- Please reach out to the discord channel for Path of Exile archipelago
#### OR
- Create an issue here: [github.com/stubobis1/Archipelago/issues](https://github.com/stubobis1/Archipelago/issues)

# Setup

---

## 1) Prerequisites

- Path of Exile installed and playable.
- Python 3.13 installed (unless you use the downloadable release of MWGG)
- MultiworldGG (latest release).
- Except with MWGG: The Path of Exile `.apworld` file from the Path of Exile APWorld release page. 
  - [github.com/stubobis1/Archipelago/releases](https://github.com/stubobis1/Archipelago/releases)

---

## 2) Download & Install MultiworldGG

1. Download the latest MultiworldGG release:
   - [github.com/MultiworldGG/MultiworldGG/releases](https://github.com/MultiworldGG/MultiworldGG/releases)
2. Install Python if needed (unless you use the downloadable release of MWGG):
   - [python.org/downloads/release/python-31311/](https://www.python.org/downloads/release/python-31311/)
3. Extract the MultiworldGG release to a folder of your choice (e.g., `C:\Games\MultiworldGG` or `~/MultiworldGG`).

---

## 3) Add the Path of Exile .apworld (not needed with MultiworldGG)

1. Download the `.apworld`:
   - [github.com/stubobis1/Archipelago/releases](https://github.com/stubobis1/Archipelago/releases)
2. Place the `.apworld` file into the `MultiworldGG/custom_worlds/` folder.

---

## 4) Generate / Join a Multiworld

1. Launch `MultiworldGGLauncher.exe` from your MultiworldGG folder.
2. Generate Template Options
3. Modify `MultiworldGG/Players/Templates/Path of Exile.yaml` to change options to your liking.
4. Setup a Multiworld session:
  - If self-hosting / playing single player:
    - place the `Path of Exile.yaml` in your Players directory
    - run `MultiworldGGLauncher.exe`
    - Select **Generate Game**.
    - Select **Host**, and select the generated file from `/output`
    - By default the server will run on port `38281`
  - If playing with others:
    - Send your `yaml` to whomever is generating and hosting
    - Get your slot name from the host, and the server address (IP or domain) and port.


---

## 5) Setup Poptracker (Optional but Highly Recommended)

1. Download Poptracker from: [github.com/black-sliver/PopTracker/releases](https://github.com/black-sliver/PopTracker/releases)
2. Extract / Setup Poptracker to a folder of your choice.
3. Download the PoE Archipelago Poptracker pack from: [github.com/stubobis1/PathOfExilePoptracker/releases](https://github.com/stubobis1/PathOfExilePoptracker/releases)
4. Place the zip file into the `poptracker/packs` directory.
5. Launch `PopTracker.exe`.
6. Click on the `AP` button at the top.
7. Enter your slot name and server address from step 4. (Example: `127.0.0.1:38281`, slot `Player1`, no password)
8. If the `AP` button is green you are connected.


---

## 6) Start the Client

1. In `MultiworldGGLauncher.exe` run `Path of Exile` from the client list.
2. Enter the slot name and server address in the top bar 
   - something like `Player1:@127.0.0.1:38281` 
     - (note the `:` after the slot name is where you would put the password, if one was set by the host).
3. Click **Connect**.
4. (optional) Run `/received` to see which class you have received. (not needed if you setup poptracker)
5. Run `/poe_auth` in the client console to authenticate your PoE account.
6. Set the character you will be playing with `/char YourCharacterName`.
7. Set your `client.txt` path by running `/client "C:\PathOfExile\logs\Client.txt"` (adjust path as needed). Note the Quotation marks.
8. Set your item filter path by running `/filter <filterName>.filter` 
    - this should be a local filter, and exist at something like `C:\Users\<USERNAME>\Documents\My Games\Path of Exile`
9. (Optional) Enable or Disable DeathLink with `/deathlink` if you want to share deaths with other players.
10. If you haven't already, Launch Path of Exile and **LOGIN**. 
11. Run `/start` in the client.
12. Start playing Path of Exile!
    - Enter a zone to trigger an initial check.
    - Pick up items to unlock things.
    - Change zones to send checks for newly found items/conditions.


---


## 7) In‑Game Chat Commands (Whisper Yourself)

Send whispers **to your own character** using `@YourCharacterName` followed by a command. Example:
```
@YourCharacterName !gems
```

Commands:
```
!ap char                  - Set your character
!deathlink                - Toggle DeathLink
!goal                     - View your current goal
!passive or !p            - List usable passive points
!usable skill gems        - List usable skill gems (by level)
!usable support gems      - List usable support gems
!usable utility gems      - List usable utility gems
!usable gems              - List all usable gems
!main gems                - Show main skill gems received
!support gems             - Show support gems received
!utility gems             - Show utility gems received
!all gems or !gems        - Show all gems received
!gear                     - Show usable gear
!weapons                  - Show usable weapons
!armor                    - Show usable armor
!links                    - Show maximum link allowance
!flasks                   - Show flask unlocks
!ascendancy               - Show unlocked ascendancies
!help                     - Show help message
```

Note: Commands must be whispered to **yourself** (not global chat) using `@YourCharacterName`.

---

## 8) Tips & Troubleshooting

- If you get problems when you are trying to write the filter, it could be Windows OneDrive interfering. Try disabling OneDrive.
- Keep the MultiworldGG client running while you play PoE.
- If you pick up an item and no check is sent, **enter a new zone** to trigger a check.
- Make sure your PoE logs are being read (client should detect zone changes and chat whispers).
- If your normal item filter isn't working, load it with `/filter` in the client console.
- OAuth/API: Ensure your PoE account is properly authenticated if the client needs character data from the API.
- DeathLink: When enabled, your deaths (and others’) can be shared as events across players.
- F11 will restart the client if you run into issues.
- F12 will force the client to do a check. 
  - The API still only updates when changing zones, but this is helpful if something gets messed up. (AP can't read the client.txt file)

---

## 9) Quick Start Summary

1. Install Python (3.12) and MultiworldGG.
2. Without MWGG: Drop the PoE `.apworld` into `Archipelago/custom_worlds/`.
3. Use the Launcher to generate or connect to a multiworld.
4. Start playing PoE with the client open.
5. Whisper yourself for status/info commands and change zones to send checks.

---

Happy mapping, and good luck with your drops!



#### This product isn’t affiliated with or endorsed by Grinding Gear Games in any way.
