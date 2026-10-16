from typing import List, Optional, NamedTuple, TYPE_CHECKING
from .Options import GateItems, SoulsanityLevel, SoulRandomizer

if TYPE_CHECKING:
    from . import DoSWorld


class LocationData(NamedTuple):
    region: str
    name: str
    is_event: Optional[bool] = False


def get_locations(world: "DoSWorld") -> List[LocationData]:

    location_table: List[LocationData] = [
        LocationData("Lost Village Upper", "Lost Village: Above Entrance"),
        LocationData("Lost Village Upper Doorway", "Lost Village: Upper Big Room Corner"),
        LocationData("Lost Village Upper", "Lost Village: Pre-Boss Room Upper"),
        LocationData("Lost Village Upper", "Lost Village: Pre-Boss Room Lower"),
        LocationData("Lost Village Upper", "Lost Village: Drawbridge Room"),
        LocationData("Lost Village Upper", "Lost Village: Above Drawbridge"),
        LocationData("Lost Village Upper", "Lost Village: In Moat"),
        LocationData("Lost Village Upper", "Flying Armor Soul"),
        LocationData("Lost Village Upper", "Lost Village: Boss Room", True),
        LocationData("Lost Village Courtyard", "Lost Village: Above Guest House Entrance"),

        LocationData("Lost Village Lower", "Lost Village: Flying Armor Indoor Room"),
        LocationData("Lost Village Lower", "Lost Village: West Plaza"),
        LocationData("Lost Village Lower", "Lost Village: West Building Upper"),
        LocationData("Lost Village Lower", "Lost Village: West Building Lower"),
        LocationData("Lost Village Lower", "Lost Village: Central Building"),
        LocationData("Lost Village Lower", "Lost Village: East Plaza"),
        LocationData("Lost Village Lower", "Lost Village: Hidden Floor Room 1"),
        LocationData("Lost Village Lower", "Lost Village: Hidden Floor Room 2"),
        LocationData("Lost Village Lower", "Lost Village: Mirror Room Left"),
        LocationData("Lost Village Lower", "Lost Village: Mirror Room Right"),
        LocationData("Lost Village Lower", "Lost Village: Moat Drain Switch", True),
        LocationData("Lost Village Underground Top", "Lost Village: Axe Armor Hallway"),
        LocationData("Lost Village Underground Top", "Lost Village: Underground Shaft"),

        LocationData("Wizardry Lab Main", "Wizardry Lab: Mirror Room"),
        LocationData("Wizardry Lab Main", "Wizardry Lab: Mirror World"),
        LocationData("Wizardry Lab Main", "Wizardry Lab: Main Entry Shaft"),
        LocationData("Wizardry Lab Main", "Wizardry Lab: Upper Big Room"),
        LocationData("Wizardry Lab Main", "Wizardry Lab: West Gate"),
        LocationData("Wizardry Lab West Gate", "Wizardry Lab: Behind West Gate"),
        LocationData("Wizardry Lab Main", "Wizardry Lab: Ceiling Secret Room"),
        LocationData("Wizardry Lab Main", "Balore Soul"),
        LocationData("Wizardry Lab Main", "Wizardry Lab: Boss Room", True),
        LocationData("Wizardry Lab East Gate", "Wizardry Lab: East Gate"),
        LocationData("Wizardry Lab Sunken", "Wizardry Lab: Money Gate"),
        LocationData("Wizardry Lab Sunken", "Wizardry Lab: Underwater Left"),
        LocationData("Wizardry Lab Sunken", "Wizardry Lab: Underwater Right"),
        LocationData("Wizardry Lab Sunken", "Wizardry Lab: Above Water"),

        LocationData("Garden of Madness Lower", "Garden of Madness: Lower Tree Hallway"),
        LocationData("Garden of Madness Lower", "Garden of Madness: West Big Room"),
        LocationData("Garden of Madness Lower", "Garden of Madness: West Big Room Alcove"),
        LocationData("Garden of Madness Upper", "Garden of Madness: West Upper Room"),
        LocationData("Garden of Madness Upper", "Garden of Madness: Hidden Room"),
        LocationData("Garden of Madness Lower", "Garden of Madness: Center Room"),
        LocationData("Garden of Madness Lower", "Garden of Madness: Money Gate"),
        LocationData("Garden of Madness Water Blocked", "Garden of Madness: Underground Room"),
        LocationData("Garden of Madness East Gate", "Garden of Madness: East Alcove"),
        LocationData("Garden of Madness Post-Boss", "Garden of Madness: Boss Room", True),

        LocationData("Demon Guest House Main", "Demon Guest House: Secret Room"),
        LocationData("Demon Guest House Main", "Demon Guest House: Antechamber"),
        LocationData("Demon Guest House Main", "Demon Guest House: Lower Main Chamber Bottom Room"),
        LocationData("Demon Guest House Puppet Wall Right", "Demon Guest House: Puppet Hole"),

        LocationData("Demon Guest House Number Puzzle West", "Demon Guest House: Number 1 Room"),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Number 5 Room"),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Number 8 Room"),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Number 9 Room"),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Number 12 Room"),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Mirror World"),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Mirror Room"),
        LocationData("Demon Guest House West Wing", "Demon Guest House: Doll Alcove"),

        LocationData("Demon Guest House West Wing", "Demon Guest House: West Wing Left"),
        LocationData("Demon Guest House West Wing", "Demon Guest House: West Wing Right"),
        LocationData("Demon Guest House West Wing", "Puppet Master Soul"),
        LocationData("Demon Guest House West Wing", "Demon Guest House: Boss Room", True),
        LocationData("Demon Guest House West Wing", "Demon Guest House: Ice Block Room Left"),
        LocationData("Demon Guest House West Wing", "Demon Guest House: Ice Block Room Right"),

        LocationData("Demon Guest House Main", "Demon Guest House: Central Main Chamber Bottom Room"),
        LocationData("Demon Guest House Main", "Demon Guest House: Central Main Chamber Middle Room"),
        LocationData("Demon Guest House Main", "Demon Guest House: Central Main Chamber Top Room"),

        LocationData("Demon Guest House Upper", "Paranoia Soul"),
        LocationData("Demon Guest House Upper", "Upper Guest House: Boss Room", True),
        LocationData("Demon Guest House Upper", "Demon Guest House: Beyond Paranoia"),
        LocationData("Demon Guest House Upper", "Demon Guest House: Paranoia Mirror"),

        LocationData("Dark Chapel", "Dark Chapel: Entrance Alcove"),
        LocationData("Dark Chapel", "Dark Chapel: Catacombs Top Left"),
        LocationData("Dark Chapel", "Dark Chapel: Catacombs Middle Room"),
        LocationData("Dark Chapel", "Dark Chapel: Catacombs Soul Barrier"),
        LocationData("Dark Chapel", "Dark Chapel: Catacombs Mirror Room"),
        LocationData("Dark Chapel", "Dark Chapel: Catacombs Mirror World"),
        LocationData("Dark Chapel", "Dark Chapel: Big Square Room Alcove"),
        LocationData("Dark Chapel", "Dark Chapel: Main Room"),
        LocationData("Dark Chapel", "Dark Chapel: Bell Room In Bell"),
        LocationData("Dark Chapel", "Dark Chapel: Bell Room Top Left"),
        LocationData("Dark Chapel", "Dark Chapel: Bell Room Right"),
        LocationData("Dark Chapel", "Dark Chapel: Post-Dmitrii Room"),
        LocationData("Dark Chapel", "Malphas Soul"),
        LocationData("Dark Chapel", "Dark Chapel: Inner Chapel Boss Room", True),
        LocationData("Dark Chapel", "Dark Chapel: Boss Room", True),

        LocationData("Dark Chapel Big Room", "Dark Chapel: Big Room Top Right"),
        LocationData("Dark Chapel Big Room", "Dark Chapel: Big Room Central"),
        LocationData("Dark Chapel Big Room", "Dark Chapel: Big Room Lower"),

        LocationData("Condemned Tower Bottom", "Condemned Tower: 1F West"),
        LocationData("Condemned Tower Bottom", "Condemned Tower: 1F East"),
        LocationData("Condemned Tower Bottom", "Condemned Tower: 2F East"),
        LocationData("Condemned Tower Main", "Condemned Tower: 5F West"),
        LocationData("Condemned Tower Main", "Condemned Tower: 7F West"),
        LocationData("Condemned Tower Top", "Condemned Tower: Top of the Tower"),
        LocationData("Condemned Tower Main", "Gergoth Soul"),
        LocationData("Condemned Tower Main", "Condemned Tower: Boss Room", True),

        LocationData("Cursed Clock Tower Entrance", "Cursed Clock Tower: Money Gate"),
        LocationData("Cursed Clock Tower Entrance", "Cursed Clock Tower: Lower Corner Room"),
        LocationData("Cursed Clock Tower Central", "Cursed Clock Tower: Mirror Room"),
        LocationData("Cursed Clock Tower Central", "Cursed Clock Tower: Mirror World"),
        LocationData("Cursed Clock Tower Central", "Cursed Clock Tower: Bugbear Hallway"),
        LocationData("Cursed Clock Tower Central", "Cursed Clock Tower: East Gear Room",),
        LocationData("Cursed Clock Tower Central", "Cursed Clock Tower: Spike Room Secret"),
        LocationData("Cursed Clock Tower Boss Area", "Zephyr Soul"),
        LocationData("Cursed Clock Tower Boss Area", "Cursed Clock Tower: Boss Room", True),

        LocationData("Subterranean Hell Top Entrance", "Rahab Soul"),
        LocationData("Subterranean Hell Top Entrance", "Subterranean Hell: Boss Room", True),
        LocationData("Subterranean Hell East", "Subterranean Hell: Giant Underwater Room Center Left"),
        LocationData("Subterranean Hell East", "Subterranean Hell: Giant Underwater Room Center Right"),
        LocationData("Subterranean Hell East", "Subterranean Hell: Giant Underwater Room Top Left"),
        LocationData("Subterranean Hell East", "Subterranean Hell: Giant Underwater Room Bottom Right"),
        LocationData("Subterranean Hell Central Exit", "Subterranean Hell: Near Save Room"),
        LocationData("Subterranean Hell Central Lower", "Subterranean Hell: Central Lower Room"),
        LocationData("Subterranean Hell Central Upper", "Subterranean Hell: Central Upper Room"),
        LocationData("Subterranean Hell Shaft Middle", "Subterranean Hell: Behind Waterfall"),
        LocationData("Subterranean Hell Shaft Bottom Stairs", "Subterranean Hell: Waterfall Room Lower"),
        LocationData("Subterranean Hell Shaft Middle", "Subterranean Hell: Waterfall Room Middle"),
        LocationData("Subterranean Hell Shaft Middle", "Subterranean Hell: Waterfall Room Upper"),

        LocationData("Silenced Ruins", "Silenced Ruins: Ice Block Room"),
        LocationData("Silenced Ruins", "Bat Company Soul"),
        LocationData("Silenced Ruins", "Silenced Ruins: Boss Room", True),
        LocationData("Silenced Ruins Back Exit", "Silenced Ruins: Mirror Room"),
        LocationData("Silenced Ruins Back Exit", "Silenced Ruins: Mirror World"),

        LocationData("The Pinnacle Left Exit", "The Pinnacle: Lower Hidden Room"),
        LocationData("The Pinnacle", "The Pinnacle: Under Big Staircase"),
        LocationData("The Pinnacle", "The Pinnacle: Central Indoor Room"),
        LocationData("The Pinnacle", "The Pinnacle: Central Outdoor Room"),

        LocationData("The Pinnacle Throne Room", "The Pinnacle: Before Throne Room Secret Left"),
        LocationData("The Pinnacle Throne Room", "The Pinnacle: Before Throne Room Secret Right"),
    ]

    if world.options.goal:  # Add the checks in the Throne Room and the Abyss
        location_table += [
            LocationData("The Pinnacle Throne Room", "The Pinnacle: Beyond Throne Room"),
            LocationData("The Pinnacle Throne Room", "Aguni Soul"),
            LocationData("The Pinnacle Throne Room", "The Pinnacle: Throne Room", True),
            LocationData("The Abyss Beyond Abaddon", "Abyss Center", True)
        ]
    else:
        location_table += [
            LocationData("The Pinnacle Throne Room", "Abyss Center", True),
        ]

    if world.garden_chamber_available:
        location_table += [
            LocationData("Garden of Madness Lower", "Garden of Madness: Central Chamber", True),
        ]

    if world.mine_status != "Disabled":  # Add the Mine/Abyss checks
        location_table += [
            LocationData("Mine of Judgment", "Death Soul"),
            LocationData("Mine of Judgment", "Mine of Judgment: Boss Room", True),
            LocationData("The Abyss", "The Abyss: Sand Area"),
            LocationData("The Abyss", "The Abyss: Ice Area"),
            LocationData("The Abyss Beyond Abaddon", "Abaddon Soul"),
            LocationData("The Abyss Beyond Abaddon", "The Abyss: Boss Room", True)]

    if world.options.gate_items == GateItems.option_buttonsanity:
        location_table += [
            LocationData("Wizardry Lab West Gate", "Wizardry Lab: West Gate Button"),
            LocationData("Wizardry Lab East Gate", "Wizardry Lab: East Gate Button"),
            LocationData("Garden of Madness East Gate", "Garden of Madness: Gate Button"),
            LocationData("Silenced Ruins Back Exit", "Subterranean Hell: Gate Button")]

    if world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        for soul in world.common_souls:
            location_table.append(
             LocationData(soul, soul))

        if world.options.soulsanity_level:
            for soul in world.uncommon_souls:
                location_table.append(
                 LocationData(soul, soul))
        else:
            location_table.append(LocationData("Imp Soul", "Imp Soul", True))

        if world.options.soulsanity_level == SoulsanityLevel.option_rare:
            for soul in world.rare_souls:
                location_table.append(
                 LocationData(soul, soul))
    else:
        for soul in sorted(world.important_souls):
            if soul not in world.excluded_static_souls:  # Boss souls that are always in the pool
                location_table.append(LocationData(soul, soul, True))

    return location_table
