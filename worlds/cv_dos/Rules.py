from typing import TYPE_CHECKING
from rule_builder.rules import HasAll, HasAny, Has, OptionFilter
if TYPE_CHECKING:
    from . import DoSWorld

big_uppies = HasAny("Hippogryph Soul", "Bat Company Soul")
small_uppies = HasAny("Hippogryph Soul", "Bat Company Soul", "Malphas Soul")


def set_location_rules(world: "DoSWorld") -> None:
    from .Options import BoostSpeed, Goal

    set_rule = world.set_rule
    paranoia_souls = {wall for i, wall in enumerate(world.red_soul_walls) if i != 2}
    world.set_completion_rule(Has("Menace Defeated"))
    # Lost Village
    set_rule(world.get_location("Lost Village: Above Entrance"), big_uppies | HasAll("Malphas Soul", "Puppet Master Soul"))
    set_rule(world.get_location("Lost Village: Above Drawbridge"), small_uppies)
    set_rule(world.get_location("Lost Village: In Moat"), big_uppies & Has("Moat Drained"))
    set_rule(world.get_location("Flying Armor Soul"), Has(world.magic_seal_table["Lost Village"]))
    set_rule(world.get_location("Lost Village: Boss Room"), Has(world.magic_seal_table["Lost Village"]))
    set_rule(world.get_location("Lost Village: Mirror Room Right"), Has("Paranoia Soul"))
    set_rule(world.get_location("Lost Village: Above Guest House Entrance"), big_uppies)
    if not world.options.boost_speed:
        set_rule(world.get_location("Lost Village: Moat Drain Switch"),(small_uppies | HasAny("Puppet Master Soul", "Black Panther Soul", "Flying Armor Soul")))

    # Wizardry Lab
    set_rule(world.get_location("Wizardry Lab: Mirror Room"), Has("Balore Soul"))
    set_rule(world.get_location("Wizardry Lab: Mirror World"), HasAll("Balore Soul", "Paranoia Soul"))
    set_rule(world.get_location("Wizardry Lab: Ceiling Secret Room"), HasAny("Balore Soul", "Bat Company Soul") | (HasAny("Malphas Soul", "Hippogryph Soul") & Has("Puppet Master Soul")))
    set_rule(world.get_location("Balore Soul"), Has(world.magic_seal_table["Wizardry Lab"]))
    set_rule(world.get_location("Wizardry Lab: Boss Room"), Has(world.magic_seal_table["Wizardry Lab"]))

    set_rule(world.get_location("Wizardry Lab: Money Gate"), Has("Rahab Soul"))  # Sunken checks
    set_rule(world.get_location("Wizardry Lab: Above Water"), Has("Rahab Soul"))
    set_rule(world.get_location("Wizardry Lab: Underwater Left"), Has("Rahab Soul"))
    set_rule(world.get_location("Wizardry Lab: Underwater Right"), Has("Rahab Soul"))

    set_rule(world.get_location("Garden of Madness: Hidden Room"), small_uppies)
    set_rule(world.get_location("Garden of Madness: Underground Room"), small_uppies | HasAny("Puppet Master Soul", "Black Panther Soul"))
    set_rule(world.get_location("Garden of Madness: Boss Room"), Has(world.magic_seal_table["Garden of Madness"]))

    set_rule(world.get_location("Demon Guest House: Secret Room"), big_uppies)

    set_rule(world.get_location("Demon Guest House: Number 8 Room"), small_uppies | Has("Puppet Master Soul"))
    set_rule(world.get_location("Demon Guest House: Number 9 Room"), small_uppies | Has("Puppet Master Soul"))
    set_rule(world.get_location("Demon Guest House: Number 12 Room"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("Demon Guest House: Mirror Room"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("Demon Guest House: Mirror World"), (small_uppies | Has("Puppet Master")) & Has("Paranoia Soul"))

    set_rule(world.get_location("Puppet Master Soul"), small_uppies & Has(world.magic_seal_table["Demon Guest House"]))
    set_rule(world.get_location("Demon Guest House: Boss Room"), small_uppies & Has(world.magic_seal_table["Demon Guest House"]))
    set_rule(world.get_location("Demon Guest House: Ice Block Room Left"), small_uppies & Has("Balore Soul"))
    set_rule(world.get_location("Demon Guest House: Ice Block Room Right"), small_uppies & Has("Balore Soul"))
    set_rule(world.get_location("Demon Guest House: West Wing Left"),
             (small_uppies | HasAny("Puppet Master Soul", "Black Panther Soul")) | OptionFilter(BoostSpeed, True))
    set_rule(world.get_location("Demon Guest House: West Wing Right"),
             (small_uppies | HasAny("Puppet Master Soul", "Black Panther Soul")) | OptionFilter(BoostSpeed, True))

    set_rule(world.get_location("The Pinnacle: Under Big Staircase"), big_uppies)

    set_rule(world.get_location("Dark Chapel: Entrance Alcove"), small_uppies | Has("Puppet Master Soul"))
    set_rule(world.get_location("Dark Chapel: Catacombs Mirror World"), Has("Paranoia Soul"))
    set_rule(world.get_location("Dark Chapel: Big Square Room Alcove"), small_uppies | Has("Puppet Master Soul"))
    set_rule(world.get_location("Dark Chapel: Bell Room In Bell"), Has("Hippogryph Soul"))
    # If soulsanity, the Soul Barrier needs Skeleton

    set_rule(world.get_location("Dark Chapel: Bell Room Right"), small_uppies | HasAny("Puppet Master Soul", "Black Panther Soul"))

    set_rule(world.get_location("Dark Chapel: Big Room Top Right"),     big_uppies | HasAll("Puppet Master Soul", "Malphas Soul"))
    set_rule(world.get_location("Dark Chapel: Big Room Lower"), big_uppies)
    set_rule(world.get_location("Malphas Soul"), HasAll(world.magic_seal_table["Dark Chapel Inner"], world.magic_seal_table["Dark Chapel"]))
    set_rule(world.get_location("Dark Chapel: Inner Chapel Boss Room"), HasAll(world.magic_seal_table["Dark Chapel Inner"], world.magic_seal_table["Dark Chapel"]))
    set_rule(world.get_location("Dark Chapel: Boss Room"), Has(world.magic_seal_table["Dark Chapel Inner"]))
    set_rule(world.get_location("Dark Chapel: Post-Dmitrii Room"), Has(world.magic_seal_table["Dark Chapel Inner"]) & small_uppies)

    set_rule(world.get_location("Condemned Tower: 1F West"), big_uppies)
    set_rule(world.get_location("Condemned Tower: 2F East"), small_uppies | Has("Puppet Master Soul"))
    set_rule(world.get_location("Gergoth Soul"), Has(world.magic_seal_table["Condemned Tower"]))
    set_rule(world.get_location("Condemned Tower: Boss Room"), Has(world.magic_seal_table["Condemned Tower"]))

    set_rule(world.get_location("Cursed Clock Tower: Mirror World"), Has("Paranoia Soul"))
    set_rule(world.get_location("Cursed Clock Tower: Spike Room Secret"), Has("Bat Company Soul"))

    set_rule(world.get_location("Zephyr Soul"), Has(world.magic_seal_table["Cursed Clock Tower"]))
    set_rule(world.get_location("Cursed Clock Tower: Boss Room"), Has(world.magic_seal_table["Cursed Clock Tower"]))

    set_rule(world.get_location("Rahab Soul"), Has(world.magic_seal_table["Subterranean Hell"]))
    set_rule(world.get_location("Subterranean Hell: Boss Room"), Has(world.magic_seal_table["Subterranean Hell"]))
    set_rule(world.get_location("Subterranean Hell: Near Save Room"), small_uppies | HasAny("Puppet Master Soul", "Flying Armor Soul", "Black Panther Soul"))

    set_rule(world.get_location("Subterranean Hell: Giant Underwater Room Center Left"), Has("Rahab Soul"))
    set_rule(world.get_location("Subterranean Hell: Giant Underwater Room Center Right"), Has("Rahab Soul"))
    set_rule(world.get_location("Subterranean Hell: Giant Underwater Room Top Left"), Has("Rahab Soul"))
    set_rule(world.get_location("Subterranean Hell: Giant Underwater Room Bottom Right"), Has("Rahab Soul"))

    set_rule(world.get_location("Subterranean Hell: Behind Waterfall"), small_uppies | HasAny("Flying Armor Soul", "Black Panther Soul"))

    set_rule(world.get_location("Subterranean Hell: Waterfall Room Upper"), small_uppies | Has("Puppet Master Soul"))

    set_rule(world.get_location("Silenced Ruins: Ice Block Room"), Has("Balore Soul"))
    set_rule(world.get_location("Silenced Ruins: Mirror World"), Has("Paranoia Soul"))
    set_rule(world.get_location("Bat Company Soul"), Has(world.magic_seal_table["Silenced Ruins"]))
    set_rule(world.get_location("Silenced Ruins: Boss Room"), Has(world.magic_seal_table["Silenced Ruins"]))
    abyss_rule = big_uppies
    if world.options.menace_condition:
        abyss_rule &= HasAll(*world.menace_triggers)
    if not world.options.goal:
        abyss_rule &= Has(world.magic_seal_table["The Pinnacle"])

    set_rule(world.get_location("Abyss Center"), abyss_rule)
    
    if world.options.goal:
        set_rule(world.get_location("The Pinnacle: Beyond Throne Room"), HasAll(world.magic_seal_table["The Pinnacle"], "Paranoia Soul"))
        set_rule(world.get_location("Aguni Soul"), HasAll(world.magic_seal_table["The Pinnacle"], "Paranoia Soul"))
        set_rule(world.get_location("The Pinnacle: Throne Room"), HasAll(world.magic_seal_table["The Pinnacle"], "Paranoia Soul"))

    if world.mine_status != "Disabled":
        set_rule(world.get_location("Death Soul"), Has(world.magic_seal_table["Mine of Judgment"]) & (small_uppies | Has("Puppet Master Soul")))
        set_rule(world.get_location("Mine of Judgment: Boss Room"), Has(world.magic_seal_table["Mine of Judgment"]) & (small_uppies | Has("Puppet Master Soul")))

    if world.options.soul_randomizer == 2:
        if world.options.soulsanity_level == 2:
            for location in world.rare_souls:
                set_rule(world.get_location(location), Has("Soul Eater Ring"))
            set_rule(world.get_location("Iron Golem Soul"), Has("Imp Soul"))

    set_rule(world.get_location("Paranoia Soul"), Has(world.magic_seal_table["Demon Guest House Upper"]) & HasAll(*paranoia_souls))
    set_rule(world.get_location("Upper Guest House: Boss Room"), Has(world.magic_seal_table["Demon Guest House Upper"]) & HasAll(*paranoia_souls))
    set_rule(world.get_location("Demon Guest House: Paranoia Mirror"), HasAll(world.magic_seal_table["Demon Guest House Upper"], "Paranoia Soul") & HasAll(*paranoia_souls))
    set_rule(world.get_location("Demon Guest House: Beyond Paranoia"), Has(world.magic_seal_table["Demon Guest House Upper"]) & HasAll(*paranoia_souls))
    set_rule(world.get_location("Dark Chapel: Catacombs Soul Barrier"), Has(world.red_soul_walls[2]))

    if world.garden_chamber_available:
        garden_rule = HasAll("Mina's Talisman", world.magic_seal_table["Castle Center"])
        if world.options.garden_condition:
            garden_rule &= HasAll(*world.garden_triggers)
        set_rule(world.get_location("Garden of Madness: Central Chamber"), garden_rule)

        #  021A3278 for walls
