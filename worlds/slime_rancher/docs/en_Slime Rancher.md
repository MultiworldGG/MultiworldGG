# Slime Rancher

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file. 

## What is randomized?

The randomizer includes the following:

- Personal Upgrades
- 7Zee Rewards (an optional YAML setting, disabled by default). The three upgrade locations are checked when their reward is purchased.
- Map Fragments. Interacting with them still unveils map regions.
- Treasure Pods. Their normal rewards are still given. Secret Style DLC Treasure Pods are included only when you own the DLC and enable the YAML setting.
- Hobson's Notes

## What changes while playing?

- You must connect before creating or loading a save. Only saves made with the same seed are shown.
- Tutorials and vanilla popups are disabled.
- Most locations have custom map markers: darkened markers are out of logic, non-darkened markers are in logic, and yellow markers are hinted. `|>|>` marks fast travel; these markers appear after opening their respective slime gate, except for Reef.
- Entering an area you are not meant to enter returns you to the Ranch.
- Demolishing buildings should refund all of their costs.
- Drones do not need water, extractors remain for infinite cycles, AirNets take no damage, and DeathLink is supported.

## How do upgrade requirements work?

| Upgrade | Previous upgrade required | In-game hours passed |
| --- | --- | ---: |
| Run Efficiency | None | 48 |
| Air Burst | None | 72 |
| Jetpack Efficiency | Jetpack | 120 |
| Health lv. 2 | Health lv. 1 | 48 |
| Health lv. 3 | Health lv. 2 | 72 |
| Energy lv. 2 | Energy lv. 1 | 48 |
| Energy lv. 3 | Energy lv. 2 | 72 |
| Ammo lv. 2 | Ammo lv. 1 | 48 |
| Ammo lv. 3 | Ammo lv. 2 | 72 |

Treasure Cracker upgrades require `Region Unlock: The Lab` and fabricated gadgets: one for level 1, 20 for level 2, and 50 for level 3.

## Is there a tracker?

The in-game tracker shows where items are and displays hinted items in green. It does not show shops or 7Zee rewards.

## What should I know about the Ancient Ruins?

Ancient Ruins and Ancient Ruins Transition are separate locations. The Ruins are beyond the slime door, while the transition contains the slime statues that open it. You need both items to enter the Ancient Ruins.

## What are the known issues?

Over time, some audio may stop playing or become shortened. Quit to the main menu and then return to the game to resolve it.

## Additional features

Traps and TrapLink are available; see [Traps.md](https://github.com/SWCreeperKing/Slimipelago/blob/master/Traps.md) for details.

Music randomization folders appear after the first launch with the mod. Restart the game to refresh music options. Organize music first by area, then by time of day: `day`, `night`, or `both`. Music in the `Any` region can play in any region. Tarr music is separate: it does not use `Any`, and other regions do not use the Tarr folder.

To customize text-trap messages, add, change, or remove text files in `Slime Rancher\\Mods\\SW_CreeperKing.Slimipelago\\TextTrap`. You may remove them all, but a built-in default message remains.
