from .region_base import JakAndDaxterRegion
from ..options import EnableOrbsanity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import JakAndDaxterWorld
from ..rules import can_reach_orbs_level


def build_regions(level_name: str, world: "JakAndDaxterWorld") -> tuple[JakAndDaxterRegion, ...]:
    multiworld = world.multiworld
    options = world.options
    player = world.player


    # This includes most of the area surrounding LPC as well, for orb_count purposes. You can swim and single jump.
    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 23)
    main_area.add_cell_locations([31], access_rule=lambda state: world.can_trade(state, world.total_trade_orbs, None))
    main_area.add_cell_locations([32], access_rule=lambda state: world.can_trade(state, world.total_trade_orbs, None))
    main_area.add_cell_locations([33], access_rule=lambda state: world.can_trade(state, world.total_trade_orbs, None))
    main_area.add_cell_locations([34], access_rule=lambda state: world.can_trade(state, world.total_trade_orbs, None))
    main_area.add_cell_locations([35], access_rule=lambda state: world.can_trade(state, world.total_trade_orbs, 34))

    # These 2 scout fly boxes can be broken by running with nearby blue eco.
    main_area.add_fly_locations([196684, 262220])
    main_area.add_fly_locations([76, 131148, 65612, 327756], access_rule=lambda state:
                                world.can_free_scout_flies(state, player))

    # Warrior Pontoon check. You just talk to him and get his introduction.
    main_area.add_special_locations([33])

    orb_cache = JakAndDaxterRegion("Orb Cache", player, multiworld, level_name, 20)

    if options.rock_village_single_jump_orb_cache:
        # It is possible to just reach the orb cache with blue eco without roll jump.
        orb_cache.add_cache_locations([10945])
    else:
        # You need roll jump to be able to reach this before the blue eco runs out.
        orb_cache.add_cache_locations([10945], access_rule=lambda state: state.has_all(("Roll", "Roll Jump"), player))

    # Fly here can be gotten with Yellow Eco from Boggy, goggles, and no extra movement options (see fly ID 43).
    pontoon_bridge = JakAndDaxterRegion("Pontoon Bridge", player, multiworld, level_name, 2)
    pontoon_bridge.add_fly_locations([393292])

    # Orbs that are not directly over the pontoons if Warrior's Pontoons is not unlocked.
    pontoon_bridge_high_orbs = JakAndDaxterRegion("Pontoon Bridge High Orbs", player, multiworld, level_name, 5)

    klaww_cliff = JakAndDaxterRegion("Klaww's Cliff", player, multiworld, level_name, 0)

    if options.rock_village_single_jump_orb_cache:
        # It is possible to just reach the orb cache with blue eco without roll jump.
        main_area.connect(orb_cache)
    else:
        main_area.connect(orb_cache, rule=lambda state: state.has_all(("Roll", "Roll Jump"), player))

    if options.rock_village_pontoon_skip:
        # Reachable with Jump/Swim
        main_area.connect(pontoon_bridge)
    else:
        main_area.connect(pontoon_bridge, rule=lambda state: state.has("Warrior's Pontoons", player))

    orb_cache.connect(main_area)

    if options.rock_village_pontoon_skip:
        pontoon_bridge.connect(main_area)
    else:
        pontoon_bridge.connect(main_area, rule=lambda state: state.has("Warrior's Pontoons", player))

    # Some orbs can only be reached by using the Pontoon Bridge or having Double Jump.
    pontoon_bridge.connect(pontoon_bridge_high_orbs, rule=lambda state:
                           state.has("Warrior's Pontoons", player) or state.has("Double Jump", player))

    if options.klaww_cliff_climb:
        # It is possible to reach the boulder by going out of bounds. After the Klaww region was loaded, it is possible
        # to go out of bounds again, and void out below the Klaww region, respawning in front of the boss fight.
        pontoon_bridge.connect(klaww_cliff)
    else:
        pontoon_bridge.connect(klaww_cliff, rule=lambda state:
                               state.has("Double Jump", player)
                               or state.has_all(("Crouch", "Crouch Jump"), player)
                               or state.has_all(("Crouch", "Crouch Uppercut", "Jump Kick"), player))

    pontoon_bridge_high_orbs.connect(pontoon_bridge) # Just jump/fall back down.
    klaww_cliff.connect(pontoon_bridge)  # Just jump back down.

    world.level_to_regions[level_name].append(main_area)
    world.level_to_regions[level_name].append(orb_cache)
    world.level_to_regions[level_name].append(pontoon_bridge)
    world.level_to_regions[level_name].append(pontoon_bridge_high_orbs)
    world.level_to_regions[level_name].append(klaww_cliff)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 50 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            amount = world.orb_bundle_size * (bundle_index + 1)
            orbs.add_orb_locations(6,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, orb_amount=amount:
                                   can_reach_orbs_level(state, player, world, level, orb_amount))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    # Return klaww_cliff required for inter-level connections.
    return main_area, pontoon_bridge, klaww_cliff
