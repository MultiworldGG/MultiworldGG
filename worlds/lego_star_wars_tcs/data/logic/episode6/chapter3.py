from rule_builder.rules import And, Or

from ..macros import (
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_GRAPPLE,
    CAN_SITH_FORCE,
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_USE_SELF_DESTRUCT,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    CAN_USE_BOUNTY_HUNTER_ROCKETS,
    CAN_SUPER_EWOK_CATAPULT,
    MODERATE_PLUS,
    HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
)
from ..option_filters import logic_options, ot_high_jump_ternary, OT_HIGH_JUMP_ENABLED
from ..rules import HasAbility, HasAnyAbilities, HasAllAbilities, HasAbilityExceptCharacters
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character

from ....character_ability import *

# Exploding Blaster Bolts does not work.
# Thermal Detonators do not work.
CAN_DESTROY_GENERATORS_WITHOUT_AT_ST = Or(
    # One of the four sides of the generator is barely not reachable with a droid that cannot jump.
    CAN_USE_SELF_DESTRUCT & HasAbility(CAN_BARELY_JUMP),
    CAN_USE_BOUNTY_HUNTER_ROCKETS,
    CAN_SUPER_EWOK_CATAPULT,
)

# Slam attack, Self Destruct, Super Ewok Catapult and Bounty Hunter Rockets all work.
# Blasters bounce off, and all melee attacks are ineffective.
# Exploding Blaster Bolts does work, but needs the cage to be close to a wall, or for you to have an Ewok, or for the
# bolt to deflect into you, or for you to position P2 next to the cage and shoot them instead.
# AT-ST seems to be unable to target the caged minikit, so I could not test it.
# Unlike the cages in the Forest Loop, these cages cannot be destroyed by ramming them in a Speeder Bike.
# todo: Hard logic for deflecting bolts with "Exploding Blaster Bolts" active.
CAN_DESTROY_MINIKIT_CAGES = Or(
    HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
)


SPEEDER_SHOWDOWN = Chapter(
    area=Area.SPEEDERCHASE,
    start_region="Spawn",
    regions={
        "Spawn": (
            ExitData(
                "Past First Log",
                logic_options(
                    # Destroy the plants to reveal the platform, then force it together and stand on it to have P2 force
                    # it into the air.
                    base=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAbility(JEDI),
                    ),
                    # Allow triple jump.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
            ),
        ),
        "Past First Log": (
            ExitData(
                "First Open Area",
                # There is an invisible wall over the second log until you force the stairs into position.
                logic_options(
                    base=HasAbility(JEDI),
                    # Allow triple high jump over the invisible wall.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                        capped=HasAbility(JEDI),
                    ),
                ),
            ),
        ),
        "First Open Area": (
            ExitData(
                "Forest Loop",
                logic_options(
                    # Expect fighting the Scout Troopers before getting on the Speeder Bikes.
                    base=CAN_DAMAGE_AT_CLOSE_RANGE & HasAbility(CAN_RIDE_VEHICLES),
                    normal=HasAbility(CAN_RIDE_VEHICLES),
                ),
            ),
        ),
        "Forest Loop": (
            # Shoot the Speeder Bikes.
            ExitData("Second Open Area"),
            # Drop in P2, then you can Drop Out from the pause menu, and Drop Out while in a Speeder Bike, ejects you
            # from the Speeder Bike, so you can explore whichever area you want by dropping out in that area.
            # There is complexity, however, from the fact that certain things won't spawn in unless you progress
            # normally. This allows access to the Fourth Open Area without a Jedi to build the AT-ST in the third area
            # (and without some other means of destroying the generator in the third open area).
            # Access to the Second and Third open areas is always possible, since all you need is to shoot the Speeder
            # Bikes to get to the Second area, shoot the AT-ST that spawns with the Speeder Bike and use the AT-ST to
            # destroy the generator, then shoot the Speeder Bikes again and make it to the Third area.
            ExitData("Fourth Open Area", MODERATE_PLUS, name="2P Drop Out Sequence Break Into Fourth Open Area"),
            # Hard logic could skip the force field entirely when they have a Jedi:
            # The trick here, is that choosing to Drop Out from the menu, while riding a vehicle, ejects you from that
            # vehicle, and *you can do this in the middle of a loop*.
            # The Drop Out option in the menu only shows when both players are Dropped In, so drop in P2.
            # Perform a loop in the Speeder by the force field.
            # At the top of the loop, Drop Out, to eject from the vehicle.
            # From the ejection, triple jump over the invisible wall of the force field.
            # The loading zone for the area is close to the force field, so you may need to walk backwards to hit it.
            # However, simply having a Jedi on Hard logic allows you to access every other area the intended way, so
            # this sequence break is not relevant.
            # ExitData(
            #     "Landing Pad Ground Level",
            #     logic_options(
            #         base=False_(),
            #         hard=HasAbility(JEDI),
            #     ),
            #     name="Loop, Drop Out, and Triple Jump over the force field",
            # ),
        ),
        "Second Open Area": (
            # Get in the Speeder Bike, shoot the AT-ST, get in the AT-ST, shoot the generator.
            # The AT-ST only spawns if the Speeder Bikes have been defeated.
            ExitData("Third Open Area"),
        ),
        "Third Open Area": (
            # The AT-ST needs to be built this time. Destroy some plants to reveal some parts, then go to the left area
            # and pull the lever to spawn the rest of the parts. Force the parts together to make the AT-ST.
            # Note that this AT-ST is able to be built even if you sequence break to get to the Third area early.
            ExitData(
                "Fourth Open Area (No Sequence Break)",
                # Jedi is strictly required to build the AT-ST.
                logic_options(
                    # Destroy some plants to reveal some parts, then go to the left area and pull the lever to spawn
                    # the rest of the parts. Force the parts together to make the AT-ST.
                    base=And(
                        # All Jedi can pull levers.
                        HasAbility(JEDI),
                        CAN_GRAPPLE | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                    moderate=HasAbility(JEDI),
                ).or_rule(CAN_DESTROY_GENERATORS_WITHOUT_AT_ST),
            ),
        ),
        "Fourth Open Area (No Sequence Break)": (
            # Get in the Speeder Bike, shoot the AT-ST, get in the AT-ST, shoot the generator.
            # The AT-ST only spawns if the Speeder Bikes have been defeated.
            ExitData("First Open Area (Second Visit)"),
            # Can be accessed without being able to destroy the generator in "Third Open Area", through a sequence
            # break, so an extra region is required to represent this logic.
            ExitData("Fourth Open Area"),
        ),
        "Fourth Open Area": (),
        # The Plants and AT-ST on the other side of the bridge only spawn when the Speeder Bikes have all been defeated.
        "First Open Area (Second Visit)": (
            # Go across the small bridge, destroy the plants, build the spinner, push the spinner, get in the AT-ST,
            # shoot the objects containing bridge parts with the AT-ST, force to build the large bridge, then walk over
            # to the generator and destroy it with the AT-ST. Now that the last generator is destroyed, the force field
            # is lowered, and the Landing Pad can be accessed.
            ExitData(
                "Landing Pad Ground Level",
                # JEDI is strictly required to build the AT-ST, and can do each of the steps themselves.
                HasAbility(JEDI) | CAN_DESTROY_GENERATORS_WITHOUT_AT_ST,
            ),
        ),
        "Landing Pad Ground Level": (
            ExitData(
                "Landing Pad Top",
                logic_options(
                    # Activate the elevator on the right side.
                    # Moderate logic can get here without a character that can pull levers, by doing the start of the
                    # level with General Grievous/Grievous' Bodyguard, then riding the Speeder Bikes as Jar Jar Binks,
                    # and destroying all the generators using a droid character with Self Destruct.
                    base=HasAbility(CAN_PULL_LEVERS),
                    hard=Or(
                        HasAbility(CAN_PULL_LEVERS),
                        # Stand on a plant and triple high jump up to the Power Brick catwalk or the Grapple catwalk.
                        # Hover out of the end of the catwalk, and into the middle section catwalk. The walls of the
                        # middle section catwalk only block collision from the inside.
                        (HasAbility(HOVER) & Character.GENERAL_GRIEVOUS.has()) & OT_HIGH_JUMP_ENABLED,
                    ),
                ),
            ),
        ),
        "Landing Pad Top": (
            # There is no way to reach here without being able to ride vehicles.
            ExitData(
                "Chapter Completion",
                HasAbility(CAN_PULL_LEVERS),
            ),
        ),
    },
    minikits={
        "Activate Pad To Raise Ramp Minikit": minikit_data(
            "Forest Loop",
            pickup_name="MINI01",
        ),
        "Activate Three Pads Minikit": minikit_data(
            "Forest Loop",
            pickup_name="MINI03",
        ),
        "Activate Two Pads To Raise Ramp Minikit": minikit_data(
            "Forest Loop",
            pickup_name="MINI06",
        ),
        "Activate Four Pads Minikit": minikit_data(
            "Forest Loop",
            pickup_name="MINI05",
        ),
        "Activate Four Pads To Raise Two Ramps Minikit": minikit_data(
            "Forest Loop",
            pickup_name="MINI08",
        ),
        "Standalone Forest Loop Minikit": minikit_data(
            "Forest Loop",
            pickup_name="MINI02",
        ),
        "Second Open Area Minikit": minikit_data(
            "Second Open Area",
            logic_options(
                # Destroy the Sith plants, use the Access Hatch, then Hover across.
                # All CAN_SITH_FORCE can pull levers, so that does not need to be specified.
                base=CAN_SITH_FORCE & HasAllAbilities(SHORTIE | HOVER),
                normal=And(
                    CAN_SITH_FORCE & HasAbility(SHORTIE),
                    Or(
                        HasAbility(HOVER),
                        # Yoda/Ackbar can double jump across.
                        HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                        # High jump characters, except Grievous' Bodygaurd can jump across.
                        HasAbilityExceptCharacters(HIGH_JUMP, Character.GRIEVOUS_BODYGUARD) & OT_HIGH_JUMP_ENABLED,
                    )
                ),
                # Triple jump up, and triple jump across.
                moderate=HasAbility(JEDI) | HasAllAbilities(CAN_HIGH_JUMP_SLAM | CAN_PULL_LEVERS),
            ).and_rule(CAN_DESTROY_MINIKIT_CAGES),
            pickup_name="MINI09",
        ),
        "Third Open Area Minikit": minikit_data(
            "Third Open Area",
            logic_options(
                base=And(
                    HasAbility(JEDI),
                    Or(
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    )
                ),
                # Allow high jump off the silver bricks.
                # Technically, the platform that is not locked behind Silver bricks can also be double jumped from to
                # reach the platform with the lever, but it's a bit of an awkward jump, so I've opted not to include it
                # in Normal logic.
                normal=Or(
                    CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(JEDI),
                    HasAllAbilities(HIGH_JUMP | CAN_PULL_LEVERS) & OT_HIGH_JUMP_ENABLED,
                ),
                # Triple jump up.
                moderate=Or(
                    HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    HasAllAbilities(HIGH_JUMP | CAN_PULL_LEVERS) & OT_HIGH_JUMP_ENABLED
                )
            ).and_rule(CAN_DESTROY_MINIKIT_CAGES),
            pickup_name="MINI07",
        ),
        "Fourth Open Area Minikit": minikit_data(
            "Fourth Open Area",
            logic_options(
                # Build the bricks, jump up, force the platforms onto the tree, destroy the silver bricks, grapple up.
                base=And(
                    HasAbility(JEDI),
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    CAN_GRAPPLE,
                ),
                # Allow skipping building the first platform, just double jump up.
                # Allow skipping forcing the platforms onto the tree and destroying the silver bricks when High Jump is
                # enabled. Jump on a plant and then high jump to the lever.
                normal=Or(
                    And(
                        # All jedi can pull levers.
                        HasAbility(JEDI),
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        CAN_GRAPPLE,
                    ),
                    HasAllAbilities(HIGH_JUMP | CAN_PULL_LEVERS) & OT_HIGH_JUMP_ENABLED,
                ),
                # Allow triple jump.
                moderate=Or(
                    # All jedi can pull levers.
                    HasAbility(JEDI),
                    ot_high_jump_ternary(
                        uncapped=HasAllAbilities(HIGH_JUMP | CAN_PULL_LEVERS),
                        capped=HasAllAbilities(CAN_HIGH_JUMP_SLAM | CAN_PULL_LEVERS)
                    ),
                ),
            ).and_rule(CAN_DESTROY_MINIKIT_CAGES),
            pickup_name="MINI04",
        ),
        "Landing Pad Silver Brick Caged Minikit": minikit_data(
            "Landing Pad Ground Level",
            HasAbility(IMPERIAL) & CAN_DESTROY_CLOSE_SILVER_BRICKS,
            pickup_name="MINI10",
        ),
    },
    power_brick=LocationData(
        "Landing Pad Ground Level",
        logic_options(
            base=HasAbility(SHORTIE),
            # Allow triple jump off a plant with Grievous. Bodyguard does not appear to get enough height.
            moderate=ot_high_jump_ternary(
                uncapped=HasAbility(SHORTIE) | Character.GENERAL_GRIEVOUS.has(),
                capped=HasAbility(SHORTIE)
            )
        )
    ),
    ridables={
        Character.SPEEDERBIKE: LocationData("Forest Loop"),
        Character.ATST: LocationData("Second Open Area"),
        Character.ATAT: LocationData("Landing Pad Top")
    }
)

