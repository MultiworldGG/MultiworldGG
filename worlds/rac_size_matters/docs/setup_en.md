# Ratchet & Clank: Size Matters MultiworldGG Setup Guide

## Requirements

The following are required in order to play Ratchet & Clank: Size Matters in MultiworldGG

- Installed the latest version of [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases)
- The latest version of the Ratchet & Clank: Size Matters apworld (ships with MultiworldGG)
- [PCSX2 emulator](https://pcsx2.net/downloads/) (2.x or later recommended for the required PINE support)
- A copy of **Ratchet & Clank: Size Matters** — US (`SCUS-97615`), EU (`SCES-55019`), or JP (`SCPS-15120`).
---

## Enabling PINE in PCSX2

PINE is the memory interface the client uses to communicate with the emulator.

1. Open PCSX2.
2. Go to **Settings → General Settings** (or **Tools → Settings** depending on your version).
3. Find the **PINE** section and enable it. Leave the slot/port at the default value unless you have a specific reason to change it.
4. Restart PCSX2 if prompted.

---
## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?


You can use the "Options Creator" (a GUI tool in the MultiworldGG Launcher) to customize your options and export your YAML file. You can also use the "Generate Template Options" feature if you prefer editing your YAML in a text editor. Both tools are available in the MultiworldGG Launcher.

---
## Setting up your Multiworld
### Hosting your MultiWorld

This section is for players who want to host a solo or multiplayer game.

1. Collect YAML files from all participating players.
    - In the MultiworldGG Launcher, select "Browse Files" and open the `Players` folder.
    - Place each player's YAML file into the `Players` folder.

2. In the MultiworldGG Launcher, select "Generate" to create your multiworld.
    - The generated zip file will appear in the `output` folder.

3. To host online, upload the zip file from the `output` folder to the [MultiworldGG Website](https://multiworld.gg/uploads).
    - To host locally, select "Host" in the MultiworldGG Launcher and choose the zip file from the `output` folder.

### Starting a Game

1. Launch the **R&C: Size Matters Client** from the MultiworldGG launcher.
2. Connect to your MultiworldGG server with your slot name.
3. In PCSX2, load the game and wait at the **main menu** for the client to connect. The same client automatically selects the address map from the disc serial.
4. With Random Starting Planet enabled, wait for the client's **Ready to start a new game** message before selecting **New Game**. The frontend patch starts the new save directly on the selected planet, without first loading Pokitaru.
5. With Random Starting Planet off (or Pokitaru selected), start a **New Game** normally on Pokitaru.


> **Important:** Always start from a New Game at the beginning of a seed. Loading a save from a previous run will cause inventory and location state to be out of sync. To continue an ongoing session, simply reconnect to the same MultiworldGG connection address and load the save file you used for that session.

---

## Client Commands

The weapon/gadget array's memory location is resolved directly from the loaded planet, not scanned — no manual step needed there. The following commands are available in the client console:

| Command | Description |
|---------|-------------|
| `/reconnect` | Disconnect and reconnect to PCSX2, then re-apply all received items. Use this if the client loses sync with the emulator. |
| `/force_sync` | Force the player's in-game state to match what was received from MultiworldGG. |
| `/states` | Print every active internal state — useful when reporting a bug. |
| `/rac5_info` | Print the current slot options plus every active state's repr. |
| `/vendor_refresh` | Force-rewrite the vendor's item list immediately, instead of waiting for the next menu open/close. |
| `/skin <name>` | Set Ratchet's skin directly, e.g. `/skin trash`, `/skin tuxedo`, or an id 0-19. Multiplayer skins need Experimental Skins enabled in your YAML. |
| `/apicon [style]` | Choose the Archipelago icon shown on vendor items: `original`, `purple`, `grey`, or `blue`. No argument prints the current style. |
| `/debug` | Toggle verbose per-tick state-change logging in the client console. |
| `/spawn_ghost` | Spawn a static ghost clone of yourself at your current position - debug tool. |
| `/toggle_deathlink` | Toggle DeathLink on or off for this session. |
| `/toggle_ammolink` | Toggle Ammo Link on or off for this session. |
| `/toggle_boltlink` | Toggle Bolt Link on or off for this session. |

Toggling a Link on/off client-side is only half the picture — the matching YAML option (Ammo Link, Bolt Link, Ghost Link) must also be enabled at generation time. See the game info page's "What options are available?" section for details.

## Poptracker
SomeLazyGamer did a fantastic job on the poptracker and if you use poptracker make sure to check it out [link](https://github.com/SomeLazyGamer/RaC-5-SM-AP-Poptracker)

---
## Optional Balance Patch

Set `balance_patch: true` in your player YAML to enable, this is taken from UsernameCiphers Balance patch none of it was done by me i just used his changes into the patch for EU, US and JP aswel. Check out his original patch here he did a great job on it and deserves all the credit. [link](https://github.com/usernamecipher/size-matters-update)


## Troubleshooting

**Client says "Wrong game in PCSX2"**
Make sure you are running a recognized serial: `SCUS-97615` (US), `SCES-55019` (EU), or `SCPS-15120` (JP). Restart the client after updating so it loads the regional detection code.

**Weapons are not appearing after receiving items**
Use `/reconnect` in the client console to re-apply everything received so far.

**Experimental Skins causing large texture or is missing textures.** The experimental skins are as they say experimental, there are patches located in the `standalone_skins` folder for all 3 versions of the game (EU, US and JP). If you are using Experiemental skins without the patch it will work but you must connected the client to the game before loading a planet. the patch is applied during load transitions so as long as you dont enter a level transition while disconnected to the client it should work as intended. this is a toggleable option and is optional you are not forced into this patch.

**Vendor purchases are not registering**
Make sure you are standing at a vendor on a planet that has vendor locations. Purchases are detected when you buy from the vendor menu - the client needs to be connected before you open the menu.

**Ratchet's model is invisible after a planet load (Starting Skin set to anything other than Default)**
Open the in-game Skins menu and close it again — the chosen skin doesn't fully apply on its own after a planet load, and skipping this step can leave the model invisible instead.

**If you need further help**, join the [Archipelago Discord](https://discord.gg/archipelago) and visit the `[PSP/PS2] Ratchet & Clank Size Matters` thread in the `future-game-design` forum channel.
