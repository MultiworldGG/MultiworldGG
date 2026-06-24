from .region_base import JakAndDaxterRegion
from ..options import EnableOrbsanity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import JakAndDaxterWorld
from ..rules import can_fight, can_reach_orbs_level


def build_regions(level_name: str, world: "JakAndDaxterWorld") -> tuple[JakAndDaxterRegion, ...]:
    multiworld = world.multiworld
    options = world.options
    player = world.player


    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 25)

    # You can get this scout fly by running from the blue eco vent across the temple bridge,
    # falling onto the river, collecting the 3 blue clusters, using the jump pad, and running straight to the box.
    main_area.add_fly_locations([393223])

    lurker_machine = JakAndDaxterRegion("Lurker Machine", player, multiworld, level_name, 5)
    lurker_machine.add_cell_locations([3], access_rule=lambda state: world.can_fight_or_roll_jump(state, player))

    # This cell and this scout fly can both be gotten with the blue eco clusters near the jump pad.
    lurker_machine.add_cell_locations([9])
    lurker_machine.add_fly_locations([131079])

    river = JakAndDaxterRegion("River", player, multiworld, level_name, 42)

    # All of these can be gotten with blue eco, hitting the dark eco boxes, or by running.
    river.add_cell_locations([5, 8])
    river.add_fly_locations([7, 196615])
    river.add_special_locations([5])
    river.add_cache_locations([10369])

    # 12 orbs around temple exit, excluding those directly above (which are in temple_plant_boss_defeated).
    temple_exit = JakAndDaxterRegion("Temple Exit", player, multiworld, level_name, 12)

    if options.forbidden_jungle_attackless_spiral_stumps_scout_fly:
        # This fly can be reached using the blue eco vent inside the temple (easiest with Fall Damage Animation Cancel).
        temple_exit.add_fly_locations([262151])
    else:
        # This fly is too far from accessible blue eco sources.
        temple_exit.add_fly_locations([262151], access_rule=lambda state: world.can_free_scout_flies(state, player))

    temple_exterior = JakAndDaxterRegion("Temple Exterior", player, multiworld, level_name, 10)

    # All of these can be gotten with blue eco and running.
    temple_exterior.add_cell_locations([4])
    temple_exterior.add_fly_locations([327687, 65543])
    temple_exterior.add_special_locations([4])

    temple_int_pre_blue = JakAndDaxterRegion("Temple Interior (Pre Blue Eco)", player, multiworld, level_name, 17)
    temple_int_pre_blue.add_cell_locations([2])
    temple_int_pre_blue.add_special_locations([2])

    temple_int_post_blue = JakAndDaxterRegion("Temple Interior (Post Blue Eco)", player, multiworld, level_name, 29)

    # 5 orbs from Plant Boss + 5 orbs from leaving via jump pad. Only reachable when Jak can fight the plant boss.
    temple_plant_boss_defeated = JakAndDaxterRegion("Temple (Plant Boss defeated)", player, multiworld, level_name, 10)
    temple_plant_boss_defeated.add_cell_locations([6])

    main_area.connect(lurker_machine)               # Run and jump (tree stump platforms).
    main_area.connect(river)                        # Jump down.
    main_area.connect(temple_exit)                  # Run and jump (bridges).

    lurker_machine.connect(main_area)               # Jump down.
    lurker_machine.connect(river)                   # Jump down.
    lurker_machine.connect(temple_exterior)         # Jump down (ledge).

    river.connect(main_area)                        # Jump up (ledges near fisherman).
    river.connect(lurker_machine)                   # Jump pad (aim toward machine).
    river.connect(temple_exit)                      # Run and jump (trampolines).
    river.connect(temple_exterior)                  # Jump pad (aim toward temple door).

    temple_exit.connect(main_area)                  # Run and jump (bridges).
    temple_exit.connect(river)                      # Jump down.
    temple_exit.connect(temple_exterior)            # Run and jump (bridges, dodge spikes).

    if options.forbidden_jungle_elevator_skip:
        # With a deload, it's possible to skip the Elevator, but Jak has to hit the loading zone while falling down.
        # With Jump Kick, that's definitely possible.
        temple_exterior.connect(temple_int_pre_blue, rule=lambda state:
                                state.has("Jungle Elevator", player) or state.has("Jump Kick", player))
    else:
        # Requires Jungle Elevator.
        temple_exterior.connect(temple_int_pre_blue, rule=lambda state: state.has("Jungle Elevator", player))

    # It is possible to reach the boss by jumping through a collision hole above the door, using boosteds.
    # After defeating the boss, it's possible to go back with blue eco and grab everything (including jump pads).
    temple_int_pre_blue.connect(temple_int_post_blue, rule=lambda state:
                                world.can_do_boosted_extended(state, player)
                                or state.has("Blue Eco Switch", player))

    # Requires defeating the plant boss (combat).
    temple_int_post_blue.connect(temple_plant_boss_defeated, rule=lambda state: can_fight(state, player))
    temple_plant_boss_defeated.connect(temple_exit)

    world.level_to_regions[level_name].append(main_area)
    world.level_to_regions[level_name].append(lurker_machine)
    world.level_to_regions[level_name].append(river)
    world.level_to_regions[level_name].append(temple_exit)
    world.level_to_regions[level_name].append(temple_exterior)
    world.level_to_regions[level_name].append(temple_int_pre_blue)
    world.level_to_regions[level_name].append(temple_int_post_blue)
    world.level_to_regions[level_name].append(temple_plant_boss_defeated)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 150 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            amount = world.orb_bundle_size * (bundle_index + 1)
            orbs.add_orb_locations(3,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, orb_amount=amount:
                                   can_reach_orbs_level(state, player, world, level, orb_amount))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return main_area, temple_plant_boss_defeated
