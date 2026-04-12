from typing import List, Optional, NamedTuple, TYPE_CHECKING
from .static_location_data import location_ids
from .Options import GateItems, SoulsanityLevel, SoulRandomizer

if TYPE_CHECKING:
    from . import DoSWorld


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]


def get_locations(world: "DoSWorld") -> List[LocationData]:

    location_table: List[LocationData] = [
        LocationData("Lost Village Upper", "Lost Village: Above Entrance", 0x01),
        LocationData("Lost Village Upper Doorway", "Lost Village: Upper Big Room Corner", 0x02),
        LocationData("Lost Village Upper", "Lost Village: Pre-Boss Room Upper", 0x03),
        LocationData("Lost Village Upper", "Lost Village: Pre-Boss Room Lower", 0x04),
        LocationData("Lost Village Upper", "Lost Village: Drawbridge Room", 0x05),
        LocationData("Lost Village Upper", "Lost Village: Above Drawbridge", 0x06),
        LocationData("Lost Village Upper", "Lost Village: In Moat", 0x07),
        LocationData("Lost Village Upper", "Flying Armor Soul", 0x08),
        LocationData("Lost Village Upper", "Lost Village: Boss Room", None),
        LocationData("Lost Village Courtyard", "Lost Village: Above Guest House Entrance", 0x15),

        LocationData("Lost Village Lower", "Lost Village: Flying Armor Indoor Room", 0x09),
        LocationData("Lost Village Lower", "Lost Village: West Plaza", 0x0A),
        LocationData("Lost Village Lower", "Lost Village: West Building Upper", 0x0B),
        LocationData("Lost Village Lower", "Lost Village: West Building Lower", 0x0C),
        LocationData("Lost Village Lower", "Lost Village: Central Building", 0x0D),
        LocationData("Lost Village Lower", "Lost Village: East Plaza", 0x0E),
        LocationData("Lost Village Lower", "Lost Village: Hidden Floor Room 1", 0x0F),
        LocationData("Lost Village Lower", "Lost Village: Hidden Floor Room 2", 0x10),
        LocationData("Lost Village Lower", "Lost Village: Mirror Room Left", 0x11),
        LocationData("Lost Village Lower", "Lost Village: Mirror Room Right", 0x12),
        LocationData("Lost Village Lower", "Lost Village: Moat Drain Switch", None),
        LocationData("Lost Village Underground Top", "Lost Village: Axe Armor Hallway", 0x13),
        LocationData("Lost Village Underground Top", "Lost Village: Underground Shaft", 0x14),

        LocationData("Wizardry Lab Main", "Wizardry Lab: Mirror Room", 0x16),
        LocationData("Wizardry Lab Main", "Wizardry Lab: Mirror World", 0x17),
        LocationData("Wizardry Lab Main", "Wizardry Lab: Main Entry Shaft", 0x18),
        LocationData("Wizardry Lab Main", "Wizardry Lab: Upper Big Room", 0x19),
        LocationData("Wizardry Lab Main", "Wizardry Lab: West Gate", 0x1A),
        LocationData("Wizardry Lab West Gate", "Wizardry Lab: Behind West Gate", 0x1B),
        LocationData("Wizardry Lab Main", "Wizardry Lab: Ceiling Secret Room", 0x1C),
        LocationData("Wizardry Lab Main", "Balore Soul", 0x1D),
        LocationData("Wizardry Lab Main", "Wizardry Lab: Boss Room", None),
        LocationData("Wizardry Lab East Gate", "Wizardry Lab: East Gate", 0x1E),
        LocationData("Wizardry Lab Sunken", "Wizardry Lab: Money Gate", 0x1F),
        LocationData("Wizardry Lab Sunken", "Wizardry Lab: Underwater Left", 0x20),
        LocationData("Wizardry Lab Sunken", "Wizardry Lab: Underwater Right", 0x21),
        LocationData("Wizardry Lab Sunken", "Wizardry Lab: Above Water", 0x22),

        LocationData("Garden of Madness Lower", "Garden of Madness: Lower Tree Hallway", 0x23),
        LocationData("Garden of Madness Lower", "Garden of Madness: West Big Room", 0x24),
        LocationData("Garden of Madness Lower", "Garden of Madness: West Big Room Alcove", 0x25),
        LocationData("Garden of Madness Upper", "Garden of Madness: West Upper Room", 0x26),
        LocationData("Garden of Madness Upper", "Garden of Madness: Hidden Room", 0x27),
        LocationData("Garden of Madness Lower", "Garden of Madness: Center Room", 0x28),
        LocationData("Garden of Madness Lower", "Garden of Madness: Money Gate", 0x29),
        LocationData("Garden of Madness Water Blocked", "Garden of Madness: Underground Room", 0x2A),
        LocationData("Garden of Madness East Gate", "Garden of Madness: East Alcove", 0x2B),
        LocationData("Garden of Madness Post-Boss", "Garden of Madness: Boss Room", None),

        LocationData("Demon Guest House Main", "Demon Guest House: Secret Room", 0x2C),
        LocationData("Demon Guest House Main", "Demon Guest House: Antechamber", 0x2D),
        LocationData("Demon Guest House Main", "Demon Guest House: Lower Main Chamber Bottom Room", 0x2E),
        LocationData("Demon Guest House Puppet Wall Right", "Demon Guest House: Puppet Hole", 0x2F),

        LocationData("Demon Guest House Number Puzzle West", "Demon Guest House: Number 1 Room", 0x30),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Number 5 Room", 0x31),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Number 8 Room", 0x32),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Number 9 Room", 0x33),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Number 12 Room", 0x34),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Mirror World", 0x35),
        LocationData("Demon Guest House Number Puzzle", "Demon Guest House: Mirror Room", 0x36),
        LocationData("Demon Guest House West Wing", "Demon Guest House: Doll Alcove", 0x37),

        LocationData("Demon Guest House West Wing", "Demon Guest House: West Wing Left", 0x38),
        LocationData("Demon Guest House West Wing", "Demon Guest House: West Wing Right", 0x39),
        LocationData("Demon Guest House West Wing", "Puppet Master Soul", 0x3A),
        LocationData("Demon Guest House West Wing", "Demon Guest House: Boss Room", None),
        LocationData("Demon Guest House West Wing", "Demon Guest House: Ice Block Room Left", 0x3B),
        LocationData("Demon Guest House West Wing", "Demon Guest House: Ice Block Room Right", 0x3C),

        LocationData("Demon Guest House Main", "Demon Guest House: Central Main Chamber Bottom Room", 0x3D),
        LocationData("Demon Guest House Main", "Demon Guest House: Central Main Chamber Middle Room", 0x3E),
        LocationData("Demon Guest House Main", "Demon Guest House: Central Main Chamber Top Room", 0x3F),

        LocationData("Demon Guest House Upper", "Paranoia Soul", 0x40),
        LocationData("Demon Guest House Upper", "Upper Guest House: Boss Room", None),
        LocationData("Demon Guest House Upper", "Demon Guest House: Beyond Paranoia", 0x41),
        LocationData("Demon Guest House Upper", "Demon Guest House: Paranoia Mirror", 0x42),

        LocationData("Dark Chapel", "Dark Chapel: Entrance Alcove", 0x43),
        LocationData("Dark Chapel", "Dark Chapel: Catacombs Top Left", 0x44),
        LocationData("Dark Chapel", "Dark Chapel: Catacombs Middle Room", 0x45),
        LocationData("Dark Chapel", "Dark Chapel: Catacombs Soul Barrier", 0x46),
        LocationData("Dark Chapel", "Dark Chapel: Catacombs Mirror Room", 0x47),
        LocationData("Dark Chapel", "Dark Chapel: Catacombs Mirror World", 0x48),
        LocationData("Dark Chapel", "Dark Chapel: Big Square Room Alcove", 0x49),
        LocationData("Dark Chapel", "Dark Chapel: Main Room", 0x4A),
        LocationData("Dark Chapel", "Dark Chapel: Bell Room In Bell", 0x4B),
        LocationData("Dark Chapel", "Dark Chapel: Bell Room Top Left", 0x4C),
        LocationData("Dark Chapel", "Dark Chapel: Bell Room Right", 0x4D),
        LocationData("Dark Chapel", "Dark Chapel: Post-Dimitrii Room", 0x60),
        LocationData("Dark Chapel", "Malphas Soul", 0x61),
        LocationData("Dark Chapel", "Dark Chapel: Inner Chapel Boss Room", None),
        LocationData("Dark Chapel", "Dark Chapel: Boss Room", None),

        LocationData("Dark Chapel Big Room", "Dark Chapel: Big Room Top Right", 0x4E),
        LocationData("Dark Chapel Big Room", "Dark Chapel: Big Room Central", 0x4F),
        LocationData("Dark Chapel Big Room", "Dark Chapel: Big Room Lower", 0x50),

        LocationData("Condemned Tower Bottom", "Condemned Tower: 1F West", 0x51),
        LocationData("Condemned Tower Bottom", "Condemned Tower: 1F East", 0x52),
        LocationData("Condemned Tower Bottom", "Condemned Tower: 2F East", 0x53),
        LocationData("Condemned Tower Main", "Condemned Tower: 5F West", 0x54),
        LocationData("Condemned Tower Main", "Condemned Tower: 7F West", 0x55),
        LocationData("Condemned Tower Top", "Condemned Tower: Top of the Tower", 0x56),
        LocationData("Condemned Tower Main", "Gergoth Soul", 0x57),
        LocationData("Condemned Tower Main", "Condemned Tower: Boss Room", None),

        LocationData("Cursed Clock Tower Entrance", "Cursed Clock Tower: Money Gate", 0x58),
        LocationData("Cursed Clock Tower Entrance", "Cursed Clock Tower: Lower Corner Room", 0x59),
        LocationData("Cursed Clock Tower Central", "Cursed Clock Tower: Mirror Room", 0x5A),
        LocationData("Cursed Clock Tower Central", "Cursed Clock Tower: Mirror World", 0x5B),
        LocationData("Cursed Clock Tower Central", "Cursed Clock Tower: Bugbear Hallway", 0x5C),
        LocationData("Cursed Clock Tower Central", "Cursed Clock Tower: East Gear Room", 0x5D),
        LocationData("Cursed Clock Tower Central", "Cursed Clock Tower: Spike Room Secret", 0x5E),
        LocationData("Cursed Clock Tower Boss Area", "Zephyr Soul", 0x5F),
        LocationData("Cursed Clock Tower Boss Area", "Cursed Clock Tower: Boss Room", None),

        LocationData("Subterranean Hell Top Entrance", "Rahab Soul", 0x62),
        LocationData("Subterranean Hell Top Entrance", "Subterranean Hell: Boss Room", None),
        LocationData("Subterranean Hell East", "Subterranean Hell: Giant Underwater Room Center Left", 0x63),
        LocationData("Subterranean Hell East", "Subterranean Hell: Giant Underwater Room Center Right", 0x64),
        LocationData("Subterranean Hell East", "Subterranean Hell: Giant Underwater Room Top Left", 0x65),
        LocationData("Subterranean Hell East", "Subterranean Hell: Giant Underwater Room Bottom Right", 0x66),
        LocationData("Subterranean Hell Central Exit", "Subterranean Hell: Near Save Room", 0x67),
        LocationData("Subterranean Hell Central Lower", "Subterranean Hell: Central Lower Room", 0x68),
        LocationData("Subterranean Hell Central Upper", "Subterranean Hell: Central Upper Room", 0x69),
        LocationData("Subterranean Hell Shaft Middle", "Subterranean Hell: Behind Waterfall", 0x6A),
        LocationData("Subterranean Hell Shaft Bottom Stairs", "Subterranean Hell: Waterfall Room Lower", 0x6B),
        LocationData("Subterranean Hell Shaft Middle", "Subterranean Hell: Waterfall Room Middle", 0x6C),
        LocationData("Subterranean Hell Shaft Middle", "Subterranean Hell: Waterfall Room Upper", 0x6D),

        LocationData("Silenced Ruins", "Silenced Ruins: Ice Block Room", 0x6E),
        LocationData("Silenced Ruins", "Bat Company Soul", 0x6F),
        LocationData("Silenced Ruins", "Silenced Ruins: Boss Room", None),
        LocationData("Silenced Ruins Back Exit", "Silenced Ruins: Mirror Room", 0x70),
        LocationData("Silenced Ruins Back Exit", "Silenced Ruins: Mirror World", 0x71),

        LocationData("The Pinnacle Lower", "The Pinnacle: Lower Hidden Room", 0x72),
        LocationData("The Pinnacle", "The Pinnacle: Under Big Staircase", 0x73),
        LocationData("The Pinnacle", "The Pinnacle: Central Indoor Room", 0x74),
        LocationData("The Pinnacle", "The Pinnacle: Central Outdoor Room", 0x75),

        LocationData("The Pinnacle Throne Room", "The Pinnacle: Before Throne Room Secret Left", 0x76),
        LocationData("The Pinnacle Throne Room", "The Pinnacle: Before Throne Room Secret Right", 0x77),
    ]

    if world.options.goal:  # Add the checks in the Throne Room and the Abyss
        location_table += [
            LocationData("The Pinnacle Throne Room", "The Pinnacle: Beyond Throne Room", 0x78),
            LocationData("The Pinnacle Throne Room", "Aguni Soul", 0x79),
            LocationData("The Pinnacle Throne Room", "The Pinnacle: Throne Room", None),
            LocationData("The Abyss Beyond Abaddon", "Abyss Center", None)
        ]
    else:
        location_table += [
            LocationData("The Pinnacle Throne Room", "Abyss Center", None),
        ]

    if world.garden_chamber_available:
        location_table += [
            LocationData("Garden of Madness Lower", "Garden of Madness: Central Chamber", None),
        ]

    if world.mine_status != "Disabled":  # Add the Mine/Abyss checks
        location_table += [
            LocationData("Mine of Judgment", "Death Soul", 0x7A),
            LocationData("Mine of Judgment", "Mine of Judgment: Boss Room", None),
            LocationData("The Abyss", "The Abyss: Sand Area", 0x7B),
            LocationData("The Abyss", "The Abyss: Ice Area", 0x7C),
            LocationData("The Abyss Beyond Abaddon", "Abaddon Soul", 0x7D),
            LocationData("The Abyss Beyond Abaddon", "The Abyss: Boss Room", None)]

    if world.options.gate_items == GateItems.option_buttonsanity:
        location_table += [
        LocationData("Wizardry Lab West Gate", "Wizardry Lab: West Gate Button", 0xE3),
        LocationData("Wizardry Lab East Gate", "Wizardry Lab: East Gate Button", 0xE4),
        LocationData("Garden of Madness East Gate", "Garden of Madness: Gate Button", 0xE5),
        LocationData("Silenced Ruins Back Exit", "Subterranean Hell: Gate Button", 0xE6)]

    if world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        for soul in world.common_souls:
            location_table.append(
             LocationData(soul, soul, location_ids[soul]))

        if world.options.soulsanity_level:
            for soul in world.uncommon_souls:
                location_table.append(
                 LocationData(soul, soul, location_ids[soul]))
        else:
            location_table.append(LocationData("Imp Soul", "Imp Soul", None))

        if world.options.soulsanity_level == SoulsanityLevel.option_rare:
            for soul in world.rare_souls:
                location_table.append(
                 LocationData(soul, soul, location_ids[soul]))
    else:
        location_table.append(LocationData("Imp Soul", "Imp Soul", None))
        for soul in world.important_souls:
            if soul not in world.excluded_static_souls:  # Boss souls that are always in the pool
                location_table.append(LocationData(soul, soul, None))

    return location_table
