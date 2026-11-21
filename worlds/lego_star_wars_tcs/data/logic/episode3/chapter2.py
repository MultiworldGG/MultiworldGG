from rule_builder.rules import True_, Or

from ..macros import (
    CAN_GRAPPLE,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    HAS_ANY_YODA,
)
from ..option_filters import logic_options
from ..rules import HasAbility, HasAnyAbilities, HasAllAbilities
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...levels import Level

from ....character_ability import *

R_HANGAR = "Hangar"
R_GENERATOR_ROOM = "Generator Room"
R_DROID_DOORS_AND_DROID_ENEMIES_ROOM = "Droid Doors And Droid Enemies Room"
R_TOWER_CLIMB = "Tower Climb"
R_DOOKU_FIGHT = "Dooku Fight"
R_HORIZONTAL_ELEVATOR_SHAFT = "Horizontal Elevator Shaft"
R_ROTATED_PATH_TO_THE_BRIDGE = "Rotated Path To The Bridge"
R_SHIPS_BRIDGE = "Ship's Bridge"


CHANCELLOR_IN_PERIL = Chapter(
    area=Area.CRUISER,
    start_region=R_HANGAR,
    regions={
        R_HANGAR: (
            ExitData(
                R_GENERATOR_ROOM,
                HasAbility(JEDI),
                new_level=Level.CRUISER_G,
            ),
        ),
        R_GENERATOR_ROOM: (
            # ExitData(
            #     "Generator Room (Upper)",
            #     # Getting here implies Jedi.
            #     logic_options(
            #         # Astromech panel to activate the elevator, or force the platforms as a Jedi.
            #         base=HasAnyAbilities(ASTROMECH_PANEL | JEDI),
            #         # Triple high jump up from the Astromech Panel.
            #         moderate=HasAnyAbilities(ASTROMECH_PANEL | JEDI | CAN_HIGH_JUMP_SLAM),
            #     ),
            # ),
            ExitData(
                R_DROID_DOORS_AND_DROID_ENEMIES_ROOM,
                # Force the platformsForce off the grates to the next area.
                # HasAbility(JEDI),
                new_level=Level.CRUISER_B,
            ),
        ),
        R_DROID_DOORS_AND_DROID_ENEMIES_ROOM: (
            ExitData(
                R_TOWER_CLIMB,
                # Optimise out the JEDI required to reach here.
                logic_options(
                    base=HasAbility(ASTROMECH_PANEL),
                    hard=HasAbility(ASTROMECH_PANEL) | HAS_ANY_YODA,
                ),
                er_rule=logic_options(
                    # Use the panel to open the door, force the explosive into position, and then force the explosive
                    # again to explode it and open the way forward.
                    base=HasAllAbilities(ASTROMECH_PANEL | JEDI),
                    # Yoda can triple jump under the trigger to the next area, swap to another character,
                    # and then hit the trigger to load into the next area, skipping the Astromech Panel requirement.
                    # This is not a Yoda Clip, because it works even when swapping between Yoda and Yoda (Ghost), it
                    # might be because of Yodas' janky collision box, but maybe it's more to do with Yoda's small height
                    # and being able to fit behind the explodable ramp.
                    # The player is guaranteed to have at least 2 unique characters, even if one of them is just the
                    # Womp Rat from only having Yoda/Yoda (Ghost) unlocked, so there is no need to check for having
                    # any other character that can be swapped to (required to triple jump).
                    # todo: Try other small characters with a different Jedi to see if the character height is the
                    #  important part, of if it is the Yodas' janky collision.
                    hard=Or(
                        HasAllAbilities(ASTROMECH_PANEL | JEDI),
                        HAS_ANY_YODA,
                    ),
                ),
            ),
        ),
        R_TOWER_CLIMB: (
            ExitData(
                R_DOOKU_FIGHT,
                # logic_options(
                #     # Jump up, force to activate the updraft, defeat the Droideka and use the panel to open the door.
                #     base=HasAllAbilities(JEDI | ASTROMECH_PANEL),
                #     # Triple high jump can skip the updraft.
                #     moderate=HasAbility(ASTROMECH_PANEL) & HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM)
                # ),
                # Simplified without ER:
                logic_options(
                    base=True_(),
                    hard=HasAbility(ASTROMECH_PANEL),
                ),
                new_level=Level.CRUISER_C,
            ),
        ),
        R_DOOKU_FIGHT: (
            ExitData(
                R_HORIZONTAL_ELEVATOR_SHAFT,
                # Fully covered without ER.
                # Being able to reach here provides everything necessary to defeat Dooku.
                # logic_options(
                #     base=HasAbility(JEDI),
                #     # Would need to double check, but I was able to defeat him entirely as a Droideka.
                #     normal=can_damage_at_close_range,
                # ),
                new_level=Level.CRUISER_D,
            ),
        ),
        R_HORIZONTAL_ELEVATOR_SHAFT: (
            ExitData(
                R_ROTATED_PATH_TO_THE_BRIDGE,
                # Fully covered without ER.
                # All astromech panel characters can move fast enough to outrun the falling lift/elevator.
                # logic_options(
                #     # Ewok (0.9) is too slow, and R2-D2 (1.0) only just outruns the elevator.
                #     base=HasAbility(RUN_SPEED_1_0_OR_HIGHER),
                #     # Yoda has too slow movement speed, but fast ground attacks and jumps.
                #     normal=HasAbility(RUN_SPEED_1_0_OR_HIGHER) | HasAny("Yoda", "Yoda (Ghost)"),
                # ),
                new_level=Level.CRUISER_E,
            ),
        ),
        R_ROTATED_PATH_TO_THE_BRIDGE: (
            ExitData(
                R_SHIPS_BRIDGE,
                # Fully covered without ER.
                # All Astromech Panel users can walk through the gas, then all that is needed is a jump to get up a
                # later part.
                # logic_options(
                #     base=HasAllAbilities(ASTROMECH_PANEL | CAN_JUMP_HEIGHT_0_37),
                #     # Astromech Droids can just barely hover around the jump obstacle. The other Astromech Panel users
                #     # are IG-88 and 4-LOM, who can jump.
                #     moderate=HasAbility(ASTROMECH_PANEL),
                # ),
                new_level=Level.CRUISER_F,
            ),
        ),
        R_SHIPS_BRIDGE: (
            ExitData(
                "Chapter Completion",
                # Fully covered without ER.
                # logic_options(
                #     base=HasAbility(JEDI),
                # ),
            ),
        )
    },
    minikits={
        "Hangar Minikit": minikit_data(
            R_HANGAR,
            logic_options(
                base=CAN_GRAPPLE,
                # Triple jump from the red starfighter
                moderate=HasAnyAbilities(JEDI | GRAPPLE | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="m_pup1",
        ),
        "Generator Room Grapple Minikit": minikit_data(
            R_GENERATOR_ROOM,
            logic_options(
                base=CAN_GRAPPLE,
                normal=CAN_GRAPPLE | HasAbility(HIGH_JUMP),
                moderate=HasAnyAbilities(GRAPPLE | JEDI | HIGH_JUMP),
            ),
            pickup_name="m_pup1",
        ),
        "Minikit Behind Astromech Droid Door": minikit_data(
            R_DROID_DOORS_AND_DROID_ENEMIES_ROOM,
            HasAbility(ASTROMECH_PANEL),
            pickup_name="mk_0",
        ),
        "Minikit Behind Protocol Droid Door": minikit_data(
            R_DROID_DOORS_AND_DROID_ENEMIES_ROOM,
            HasAbility(ASTROMECH_PANEL),
            pickup_name="mk_1",
        ),
        "Tower Far Left Minikit": minikit_data(
            R_TOWER_CLIMB,
            # Fully covered without ER.
            # HasAbility(CAN_JUMP_HEIGHT_0_37),
            pickup_name="mk_3",
        ),
        "Tower Access Hatch Minikit": minikit_data(
            R_TOWER_CLIMB,
            # logic_options(
            #     base=HasAbility(SHORTIE),
            #     # High jump to the minikit.
            #     normal=HasAnyAbilities(SHORTIE | HIGH_JUMP),
            #     # Triple jump to the minikit.
            #     moderate=HasAnyAbilities(SHORTIE | HIGH_JUMP | JEDI),
            # ),
            # Simplified without ER:
            logic_options(
                base=HasAbility(SHORTIE),
                normal=HasAnyAbilities(SHORTIE | HIGH_JUMP),
                moderate=True_(),
            ),
            pickup_name="mk_2",
        ),
        "Minikit Behind Door After Dooku Fight": minikit_data(
            R_DOOKU_FIGHT,
            # Fully covered without ER.
            # logic_options(
            #     base=HasAbility(JEDI),
            #     # Would need to double check, but I was able to defeat him entirely as a Droideka.
            #     normal=can_damage_at_close_range,
            # ),
            pickup_name="m_pup1",
        ),
        "Minikit Behind Orange Piping": minikit_data(
            R_ROTATED_PATH_TO_THE_BRIDGE,
            # Already covered without ER.
            # logic_options(
            #     base=HasAllAbilities(ASTROMECH_PANEL | JEDI),
            #     # Include force ghosts.
            #     normal=HasAnyAbilities(ASTROMECH_PANEL | GAS_IMMUNE) & HasAbility(JEDI),
            #     # Jump around the gas...
            #     moderate=HasAbility(JEDI),
            # ),
            pickup_name="m_pup1",
        ),
        "Bridge Left Minikit": minikit_data(
            R_SHIPS_BRIDGE,
            # With ER, base logic would need to consider defeating the Bodyguards, a melee attack or explosion are
            # required, as they seem to always deflect blasters.
            # er_rule=HasAbility(CAN_JUMP_HEIGHT_0_37) & (HasAbility(CAN_MELEE) | CAN_DESTROY_CLOSE_SILVER_BRICKS),
            pickup_name="mk_0",
        ),
        "Bridge Right Minikit": minikit_data(
            R_SHIPS_BRIDGE,
            # Same logic as the left minikit
            pickup_name="mk_1",
        ),
    },
    power_brick=LocationData(
        R_HORIZONTAL_ELEVATOR_SHAFT,
        CAN_DESTROY_CLOSE_SILVER_BRICKS,
        # With ER, base logic would expect reversing the elevator to get the Power Brick.
        er_rule=logic_options(
            base=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(ASTROMECH_PANEL),
            normal=CAN_DESTROY_CLOSE_SILVER_BRICKS,
        ),
    ),
)
