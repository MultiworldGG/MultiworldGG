Quake 1 Randomizer for Archipelago
========================================

Installation
------------

* Get latest engine binary release from https://github.com/randomcodegen/ironwail_ap/releases (64bit Windows only)
* Acquire an official release of quake to get access to the "id1" folder and move it to the ironwail_ap.exe folder
* Exctract q1_files.zip from GitHub into the folder containing ironwail_ap.exe
* Afterwards the following files should exist: 
  * ap_config.json 
  * ap_connect_info.json
  * ./id1/pak2.pak


* Get the matching quake.apworld from https://github.com/randomcodegen/Archipelago/releases
* Put it in C:\ProgramData\Archipelago\custom_worlds
* Start the launcher and press "Generate Template Options" to create the yaml
* Move the Quake1.yaml to the C:\ProgramData\Archipelago\players directory and change the settings in the file
* In the Launcher press Generate and then Host to run the server

* Fill the connetion details in ap_connect_info.json and start ironwail_ap.exe

How the randomizer works
------------------------

All weapon and inventory pickups have been converted into AP locations. 
If enabled, secret sectors also get converted to locations if the selected goal does not include secrets.

Unlockable items are weapons, ammunition capacity and inventory items.
If enabled, the ability to jump, crouch, sprint, dive into water, open doors and use switches have to be unlocked. 

Progression inventory items are restored on every level entry. 
The logic is designed so that locations can be checked from the start of a level 
with the unlocked capacity thresholds, but not necessarily all locations can be checked in a single go. 
Simply restart a level to try again.

Ironwail_AP adds an inventory system to Quake.
The required keys need to be bound in Ironwail under Options->Key Setup.
The AP keybinds are at the bottom of the page.

AP Quad Damage: Activates Quad Damage
AP Invuln: Activate Invulnerability
AP Biosuit: Activate Biosuit
AP Backpack: Gives ammo equivalent to an ammo pickup of every weapon type
AP Medkit: Heals for 25 HP, HP over 100 gets reduced comparable to Megahealth.
AP Armor: Adds 25 armor. Armor type (green,yellow,red) is set based on armorvalue (50, 100, 200).
AP Automap: Shows a 3D view of the available items, secrets and exits if the automap for the level was received.

Vanilla excluded pickups
------------------------

The YAML option `ap_vanilla_items` controls vanilla rewards for pickups excluded from the seed:

```yaml
Quake 1:
  ap_vanilla_items:
    "item_health (Megahealth)": 1
    "item_health (Large Medkit)": 1
    weapon_rocketlauncher: 0
    item_artifact_super_damage: 0
```

Use the same item names as `custom_included_locations`. Each value must be `0` or `1`; omitted types default to `0`. Active AP locations still use AP pickups. Disabled excluded items with map links appear as white translucent AP tokens so their triggers work. Excluded pickups obey the map's difficulty and multiplayer spawn flags.

