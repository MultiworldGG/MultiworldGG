from worlds.generic.Rules import set_rule, add_rule
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import DoSWorld

big_uppies = {"Hippogryph Soul", "Bat Company Soul"}
small_uppies = {"Hippogryph Soul", "Bat Company Soul", "Malphas Soul"}


def set_location_rules(world: "DoSWorld") -> None:
    player = world.player
    paranoia_souls = {wall for i, wall in enumerate(world.red_soul_walls) if i != 2}

    ### Lost Village
    set_rule(world.multiworld.get_location("Lost Village: Above Entrance", player), lambda state: state.has_any(big_uppies, player) or state.has_all({"Malphas Soul", "Pupper Master Soul"}, player))
    set_rule(world.multiworld.get_location("Lost Village: Above Drawbridge", player), lambda state: state.has_any(small_uppies, player))
    set_rule(world.multiworld.get_location("Lost Village: In Moat", player), lambda state: (state.has_any(big_uppies, player) and state.has("Moat Drained", player))) #state.has("Rahab Soul", player) this is permanently missable
    set_rule(world.multiworld.get_location("Flying Armor Soul", player), lambda state: state.has(world.magic_seal_table["Lost Village"], player))
    set_rule(world.multiworld.get_location("Lost Village: Boss Room", player), lambda state: state.has(world.magic_seal_table["Lost Village"], player))
    set_rule(world.multiworld.get_location("Lost Village: Mirror Room Right", player), lambda state: state.has("Paranoia Soul", player))
    set_rule(world.multiworld.get_location("Lost Village: Above Guest House Entrance", player), lambda state: state.has_any(big_uppies, player))

    ###Wizardry Lab
    set_rule(world.multiworld.get_location("Wizardry Lab: Mirror Room", player), lambda state: state.has("Balore Soul", player))
    set_rule(world.multiworld.get_location("Wizardry Lab: Mirror World", player), lambda state: state.has_all({"Balore Soul", "Paranoia Soul"}, player))
    set_rule(world.multiworld.get_location("Wizardry Lab: Ceiling Secret Room", player), lambda state: (state.has("Balore Soul", player)) or (state.has("Bat Company Soul", player)) or (state.has("Puppet Master Soul", player) and state.has_any({"Malphas Soul", "Hippogryph Soul"}, player)))

    set_rule(world.multiworld.get_location("Balore Soul", player), lambda state: state.has(world.magic_seal_table["Wizardry Lab"], player))
    set_rule(world.multiworld.get_location("Wizardry Lab: Boss Room", player), lambda state: state.has(world.magic_seal_table["Wizardry Lab"], player))

    set_rule(world.multiworld.get_location("Wizardry Lab: Money Gate", player), lambda state: state.has("Rahab Soul", player)) #Sunken checks
    set_rule(world.multiworld.get_location("Wizardry Lab: Above Water", player), lambda state: state.has("Rahab Soul", player))
    set_rule(world.multiworld.get_location("Wizardry Lab: Underwater Left", player), lambda state: state.has("Rahab Soul", player))
    set_rule(world.multiworld.get_location("Wizardry Lab: Underwater Right", player), lambda state: state.has("Rahab Soul", player))

    set_rule(world.multiworld.get_location("Garden of Madness: Hidden Room", player), lambda state: state.has_any(big_uppies, player))
    set_rule(world.multiworld.get_location("Garden of Madness: Underground Room", player), lambda state: state.has_any(small_uppies, player) or state.has_any({"Puppet Master Soul", "Black Panther Soul"}, player))
    set_rule(world.multiworld.get_location("Garden of Madness: Boss Room", player), lambda state: state.has(world.magic_seal_table["Garden of Madness"], player))

    set_rule(world.multiworld.get_location("Demon Guest House: Secret Room", player), lambda state: state.has_any(big_uppies, player))

    set_rule(world.multiworld.get_location("Demon Guest House: Number 8 Room", player), lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player))
    set_rule(world.multiworld.get_location("Demon Guest House: Number 9 Room", player), lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player))
    set_rule(world.multiworld.get_location("Demon Guest House: Number 12 Room", player), lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player))
    set_rule(world.multiworld.get_location("Demon Guest House: Mirror Room", player), lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player))
    set_rule(world.multiworld.get_location("Demon Guest House: Mirror World", player), lambda state: (state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)) and state.has("Paranoia Soul", player))

    set_rule(world.multiworld.get_location("Puppet Master Soul", player), lambda state: state.has_any(small_uppies, player) and state.has(world.magic_seal_table["Demon Guest House"], player))
    set_rule(world.multiworld.get_location("Demon Guest House: Boss Room", player), lambda state: state.has_any(small_uppies, player) and state.has(world.magic_seal_table["Demon Guest House"], player))
    set_rule(world.multiworld.get_location("Demon Guest House: Ice Block Room Left", player), lambda state: state.has_any(small_uppies, player) and state.has("Balore Soul", player))
    set_rule(world.multiworld.get_location("Demon Guest House: Ice Block Room Right", player), lambda state: state.has_any(small_uppies, player) and state.has("Balore Soul", player))

    set_rule(world.multiworld.get_location("The Pinnacle: Under Big Staircase", player), lambda state: state.has_any(big_uppies, player))

    set_rule(world.multiworld.get_location("Dark Chapel: Entrance Alcove", player), lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player))
    set_rule(world.multiworld.get_location("Dark Chapel: Catacombs Mirror World", player), lambda state: state.has("Paranoia Soul", player))
    set_rule(world.multiworld.get_location("Dark Chapel: Big Square Room Alcove", player), lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player))
    set_rule(world.multiworld.get_location("Dark Chapel: Bell Room In Bell", player), lambda state: state.has("Hippogryph Soul", player))
    # If soulsanity, the Soul Barrier needs Skeleton

    set_rule(world.multiworld.get_location("Dark Chapel: Bell Room Right", player), lambda state: state.has_any(small_uppies, player) or state.has_any({"Puppet Master Soul", "Black Panther Soul"}, player))

    set_rule(world.multiworld.get_location("Dark Chapel: Big Room Top Right", player), lambda state: state.has_any(big_uppies, player) or (state.has("Puppet Master Soul", player) and state.has("Malphas Soul", player)))
    set_rule(world.multiworld.get_location("Dark Chapel: Big Room Lower", player), lambda state: state.has_any(big_uppies, player))
    set_rule(world.multiworld.get_location("Malphas Soul", player), lambda state: state.has(world.magic_seal_table["Dark Chapel Inner"], player) and state.has(world.magic_seal_table["Dark Chapel"], player))
    set_rule(world.multiworld.get_location("Dark Chapel: Inner Chapel Boss Room", player), lambda state: state.has(world.magic_seal_table["Dark Chapel Inner"], player) and state.has(world.magic_seal_table["Dark Chapel"], player))
    set_rule(world.multiworld.get_location("Dark Chapel: Boss Room", player), lambda state: state.has(world.magic_seal_table["Dark Chapel Inner"], player))
    set_rule(world.multiworld.get_location("Dark Chapel: Post-Dimitrii Room", player), lambda state: state.has(world.magic_seal_table["Dark Chapel"], player) and state.has_any(small_uppies, player))

    set_rule(world.multiworld.get_location("Condemned Tower: 1F West", player), lambda state: state.has_any(big_uppies, player))
    set_rule(world.multiworld.get_location("Condemned Tower: 2F East", player), lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player))
    set_rule(world.multiworld.get_location("Gergoth Soul", player), lambda state: state.has(world.magic_seal_table["Condemned Tower"], player))
    set_rule(world.multiworld.get_location("Condemned Tower: Boss Room", player), lambda state: state.has(world.magic_seal_table["Condemned Tower"], player))

    set_rule(world.multiworld.get_location("Cursed Clock Tower: Mirror World", player), lambda state: state.has("Paranoia Soul", player))
    set_rule(world.multiworld.get_location("Cursed Clock Tower: Spike Room Secret", player), lambda state: state.has("Bat Company Soul", player))

    set_rule(world.multiworld.get_location("Zephyr Soul", player), lambda state: state.has(world.magic_seal_table["Cursed Clock Tower"], player))
    set_rule(world.multiworld.get_location("Cursed Clock Tower: Boss Room", player), lambda state: state.has(world.magic_seal_table["Cursed Clock Tower"], player))

    set_rule(world.multiworld.get_location("Rahab Soul", player), lambda state: state.has(world.magic_seal_table["Subterranean Hell"], player))
    set_rule(world.multiworld.get_location("Subterranean Hell: Boss Room", player), lambda state: state.has(world.magic_seal_table["Subterranean Hell"], player))
    set_rule(world.multiworld.get_location("Subterranean Hell: Near Save Room", player), lambda state: state.has_any(small_uppies, player) or state.has_any({"Puppet Master Soul", "Flying Armor Soul", "Black Panther Soul"}, player))

    set_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Center Left", player), lambda state: state.has("Rahab Soul", player))
    set_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Center Right", player), lambda state: state.has("Rahab Soul", player))
    set_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Top Left", player), lambda state: state.has("Rahab Soul", player))
    set_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Bottom Right", player), lambda state: state.has("Rahab Soul", player))

    set_rule(world.multiworld.get_location("Subterranean Hell: Behind Waterfall", player), lambda state: state.has_any(small_uppies, player) or state.has_any({"Flying Armor Soul", "Black Panther Soul"}, player))

    set_rule(world.multiworld.get_location("Silenced Ruins: Ice Block Room", player), lambda state: state.has("Balore Soul", player))
    set_rule(world.multiworld.get_location("Silenced Ruins: Mirror World", player), lambda state: state.has("Paranoia Soul", player))
    set_rule(world.multiworld.get_location("Bat Company Soul", player), lambda state: state.has(world.magic_seal_table["Silenced Ruins"], player))
    set_rule(world.multiworld.get_location("Silenced Ruins: Boss Room", player), lambda state: state.has(world.magic_seal_table["Silenced Ruins"], player))

    set_rule(world.multiworld.get_location("Abyss Center", player), lambda state: state.has_any(big_uppies, player))
    
    if world.options.goal:
        set_rule(world.multiworld.get_location("The Pinnacle: Beyond Throne Room", player), lambda state: state.has_all({world.magic_seal_table["The Pinnacle"], "Paranoia Soul"}, player))
        set_rule(world.multiworld.get_location("Aguni Soul", player), lambda state: state.has_all({world.magic_seal_table["The Pinnacle"], "Paranoia Soul"}, player))
        set_rule(world.multiworld.get_location("The Pinnacle: Throne Room", player), lambda state: state.has_all({world.magic_seal_table["The Pinnacle"], "Paranoia Soul"}, player))
    else:
        add_rule(world.multiworld.get_location("Abyss Center", player), lambda state: state.has(world.magic_seal_table["The Pinnacle"], player))

    if world.mine_status != "Disabled":
        set_rule(world.multiworld.get_location("Death Soul", player), lambda state: state.has(world.magic_seal_table["Mine of Judgment"], player) and (state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)))
        set_rule(world.multiworld.get_location("Mine of Judgment: Boss Room", player), lambda state: state.has(world.magic_seal_table["Mine of Judgment"], player) and (state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)))


    if not world.options.boost_speed:
        # These jumps are trivial with the speedboost option on
        set_rule(world.multiworld.get_location("Lost Village: Moat Drain Switch", player), lambda state: state.has_any(small_uppies, player) or state.has_any({"Flying Armor Soul", "Puppet Master Soul", "Black Panther Soul"}, player))
        set_rule(world.multiworld.get_location("Demon Guest House: West Wing Left", player), lambda state: state.has_any(small_uppies, player) or state.has_any({"Puppet Master Soul", "Black Panther Soul"}, player))
        set_rule(world.multiworld.get_location("Demon Guest House: West Wing Right", player), lambda state: state.has_any(small_uppies, player) or state.has_any({"Puppet Master Soul", "Black Panther Soul"}, player))

    if world.options.soul_randomizer == 2:
        if world.options.soulsanity_level == 2:
            for location in world.rare_souls:
                set_rule(world.multiworld.get_location(location, player), lambda state: state.has("Soul Eater Ring", player))
            set_rule(world.multiworld.get_location("Iron Golem Soul", player), lambda state: state.has("Imp Soul", player))

    set_rule(world.multiworld.get_location("Paranoia Soul", player), lambda state: state.has(world.magic_seal_table["Demon Guest House Upper"], player) and state.has_all(paranoia_souls, player))
    set_rule(world.multiworld.get_location("Upper Guest House: Boss Room", player), lambda state: state.has(world.magic_seal_table["Demon Guest House Upper"], player) and state.has_all(paranoia_souls, player))
    set_rule(world.multiworld.get_location("Demon Guest House: Paranoia Mirror", player), lambda state: state.has_all({world.magic_seal_table["Demon Guest House Upper"], "Paranoia Soul"}, player) and state.has_all(paranoia_souls, player))
    set_rule(world.multiworld.get_location("Demon Guest House: Beyond Paranoia", player), lambda state: state.has(world.magic_seal_table["Demon Guest House Upper"], player) and state.has_all(paranoia_souls, player))
    set_rule(world.multiworld.get_location("Dark Chapel: Catacombs Soul Barrier", player), lambda state: state.has(world.red_soul_walls[2], player))

    if not world.options.replace_menace_with_soma:
        set_rule(world.multiworld.get_location("Abyss Center", player), lambda state: state.has_any(big_uppies, player))

    if world.options.menace_condition:
        add_rule(world.multiworld.get_location("Abyss Center", player), lambda state: state.has_all(world.menace_triggers, player))

    if world.garden_chamber_available:
        set_rule(world.multiworld.get_location("Garden of Madness: Central Chamber", player), lambda state: state.has_all({"Mina's Talisman", world.magic_seal_table["Castle Center"]}, player))
        if world.options.garden_condition:
            add_rule(world.multiworld.get_location("Garden of Madness: Central Chamber", player), lambda state: state.has_all(world.garden_triggers, player))

    #if world.options.hidden_wall_status == RevealBreakableWalls.option_eye_spy:
     #   add_rule(world.multiworld.get_location("Lost Village: Hidden Floor Room 1", player), lambda state: state.has("Peeping Eye Soul", player))
      #  add_rule(world.multiworld.get_location("Lost Village: Hidden Floor Room 2", player), lambda state: state.has("Peeping Eye Soul", player))
       # add_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Bottom Right", player), lambda state: state.has("Peeping Eye Soul", player))
        #add_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Bottom Right", player), lambda state: state.has("Peeping Eye Soul", player))
        #add_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Bottom Right", player), lambda state: state.has("Peeping Eye Soul", player))
        #add_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Bottom Right", player), lambda state: state.has("Peeping Eye Soul", player))
        #add_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Bottom Right", player), lambda state: state.has("Peeping Eye Soul", player))
        #add_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Bottom Right", player), lambda state: state.has("Peeping Eye Soul", player))
        #add_rule(world.multiworld.get_location("Subterranean Hell: Giant Underwater Room Bottom Right", player), lambda state: state.has("Peeping Eye Soul", player))
        # 021A3278 for this