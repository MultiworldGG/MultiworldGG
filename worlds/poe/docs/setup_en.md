# Path of Exile — MultiworldGG Setup Guide

## Requirements

- **Path of Exile** installed and playable — [pathofexile.com](https://www.pathofexile.com)
- **Python 3.12** — [python.org/downloads/release/python-31210](https://www.python.org/downloads/release/python-31210/) (3.13 not supported)
- **MultiworldGG** (latest release) — [github.com/MultiworldGG/MultiworldGG/releases](https://github.com/MultiworldGG/MultiworldGG/releases)
- **PoE .apworld file** — [github.com/stubobis1/Archipelago/releases](https://github.com/stubobis1/Archipelago/releases) (only needed for Archipelago)
- **ArchiPoElago client** — [github.com/stubobis1/Archipelago/releases](https://github.com/stubobis1/Archipelago/releases)

---

## 1) Install MultiworldGG/AP and the .apworld

1. Install Python 3.12 if you haven't already.
2. Download and install the latest MultiworldGG/AP release.
3. If you are using AP: Download the `poe.apworld` file from the PoE AP releases page.
4. If you are using AP: Place `poe.apworld` into the `Archipelago/custom_worlds/` folder.

---

## 2) Create Your YAML

You need a `.yaml` file describing your settings before generating a multiworld.

**Option A — Built-in YAML generator:** Open the ArchiPoElago client and click **YAML Generator** in the sidebar. It walks you through every option with descriptions.

**Option B — Web generator:**
- [ap.stripesoo7.org/games/Path%20of%20Exile/player-options](https://ap.stripesoo7.org/games/Path%20of%20Exile/player-options)
- [multiworld.gg/games/Path%20of%20Exile/player-options](https://multiworld.gg/games/Path%20of%20Exile/player-options)

**Option C — Edit the template manually:** Run `MultiworldGGLauncher.exe` → **Generate Template Options**, then edit `Players/Templates/Path of Exile.yaml`.

Key settings to review:
- `name` — your slot name; change it to something recognizable when playing with others
- `goal` — what you need to do to finish (campaign, act N, defeat bosses)
- `starting_character` — which class you start with (`random` by default; **Scion cannot be a starting class** — she must be unlocked in Act 3)
- `usable_starting_gear` — how much of the Twilight Strand gear you can use from the start
- `add_passive_skill_points_to_item_pool` — whether passive points are locked behind unlocks
- `add_leveling_up_to_location_pool` — whether level-ups count as checks

---

## 3) Generate and Host a Multiworld

**Playing solo or hosting for others:**
1. Place your `.yaml` (and any other players' `.yaml` files) into `MultiworldGG/Players/`.
2. Run `MultiworldGGLauncher.exe` → **Generate Game**.
3. Go to [multiworld.gg/uploads](/uploads), upload the generated archive from `MultiworldGG/output/`, and click **Create New Room**.
4. Note the server address and port (e.g. `multiworld.gg:38281`).

**Joining someone else's multiworld:**
1. Send your `.yaml` to the host (they must also have the same `poe.apworld`).
2. Wait for the host to share the server address, port, and your slot name.

---

## 4) Install and Launch ArchiPoElago

1. Download the **ArchiPoElago** client from the [PoE AP releases page](https://github.com/stubobis1/Archipelago/releases).
2. Extract and run it. You do **not** need to launch it through `MultiworldGGLauncher.exe`.
3. The first time you open it, a setup wizard walks you through five steps:

### Step 1 — Paths

Set two required paths (the client tries to detect them automatically):

- **Client.txt** — PoE's log file, usually at:
  - Windows: `C:\Games\Path of Exile\logs\Client.txt`
  - Steam: `C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\Client.txt`
- **PoE Documents folder** — where your item filters live, usually:
  - `C:\Users\<you>\Documents\My Games\Path of Exile\`

Optionally set a **base item filter** — an existing filter (e.g. Neversink) that the AP filter will chain-import. This keeps your normal item highlighting while the AP filter adds its own rules on top.

### Step 2 — GGG OAuth

Click **Login with GGG**. A browser window opens the GGG login page. Approve the read-only access request (character data only — no trading or account changes), and the browser redirects back automatically.

### Step 3 — Connect to MultiworldGG

Enter the server address (e.g. `multiworld.gg:38281`), your slot name, and the server password if one was set. Click **Connect**.

### Step 4 — Choose Your Character

Select the PoE character you will be playing as. The client uses the GGG API to read that character's equipment, gems, and passives to validate your state on each zone change.

If your character doesn't appear in the list, make sure OAuth is authenticated and you have logged into PoE at least once with that character.

### Step 5 — Ready

The status screen shows your connection states. Click **Open Dashboard** to start. The client is now watching your game and will manage your item filter automatically.

---

## 5) Start Playing

1. Launch Path of Exile normally (Steam or standalone launcher).
2. Log in with the character you selected in Step 4.
3. In the ArchiPoElago client, click **Start Monitoring** on the Dashboard.
4. Enter a zone in PoE to trigger the initial validation and filter load.

The client will:
- Automatically write and activate `__ap.filter` in your PoE documents folder whenever you enter a zone.
- Show a whisper in chat when you receive items (toggle off in Settings → Game Input → Item whispers).
- Tell you if you're "out of logic" (using gear you haven't unlocked yet) via an in-game whisper.

---

## 6) In-Game Chat Commands

Whisper **yourself** to query status without leaving the game. Example:

```
@YourCharacterName !gear
```

| Command | Description |
|---|---|
| `!help` | List all commands |
| `!gear` | Show all usable gear |
| `!weapons` | Show usable weapons |
| `!armor` | Show usable armour |
| `!links` | Show max link allowance |
| `!flasks` | Show flask unlocks |
| `!gems` | Show all received gems |
| `!main gems` | Show skill gems |
| `!support gems` | Show support gems |
| `!utility gems` | Show utility gems |
| `!usable gems` | Show gems usable at your current level |
| `!passives` or `!p` | Show available passive points |
| `!ascendancy` | Show unlocked ascendancies |
| `!goal` | Show current goal status |
| `!boss` | Show boss progress (boss-rush goals) |
| `!deathlink` | Toggle DeathLink on/off |
| `!whisper updates` | Toggle item received whispers on/off |

---

## 7) PopTracker (Optional but Recommended)

PopTracker provides a visual overview of your unlocked items and progress.

1. Download PopTracker: [github.com/black-sliver/PopTracker/releases](https://github.com/black-sliver/PopTracker/releases)
2. Extract it to a folder of your choice.
3. Download the PoE AP pack: [github.com/stubobis1/PathOfExilePoptracker/releases](https://github.com/stubobis1/PathOfExilePoptracker/releases)
4. Place the downloaded `.zip` into `poptracker/packs/` (do not extract it).
5. Launch PopTracker, click the **AP** button at the top, and enter your server address and slot name.
6. A green AP button means you are connected and synced.

---

## 8) Troubleshooting

**Filter not loading / showing the wrong items**
- Make sure the PoE Documents path is correct and writable.
- If OneDrive is managing your Documents folder, try disabling OneDrive for that folder — it can interfere with filter writes.
- Click **Regenerate filter** in Settings → Item Filter.

**Checks not sending**
- Checks are sent when you **enter a new zone**, not immediately when you pick something up. Change zones to trigger a send.
- Make sure monitoring is active (green on Dashboard) and the client is connected to the AP server.

**Out of logic / all items showing as orange blocks**
- You are using something you haven't unlocked yet. Check the **Equipment** tab in the client to see what's allowed.
- The client will whisper you the specific reason on each zone change.
- Unequip the offending item, then change zones to re-validate.

**Whispers or filter commands going to the wrong chat channel**
- Make sure Path of Exile is the active window when commands fire.
- If commands fire while PoE isn't focused, they will queue and retry until PoE is foregrounded.
- If commands are landing in global chat, go to Settings → Game Input and increase **Enter delay** or **Zone transition delay** by 50–100 ms.

**Goal button grayed out after reaching the goal zone**
- The client sends a verification whisper to confirm your in-game identity. If it doesn't receive an echo within 30 seconds, the button enables automatically.
- If you want instant activation, go to Settings → Goal and disable **Chat verification**.

**Character not found / OAuth errors**
- Re-authenticate via Settings → GGG Account → Login with GGG.
- Make sure you have logged into PoE at least once with that character so it appears in the API.

---

*This product is not affiliated with or endorsed by Grinding Gear Games.*
