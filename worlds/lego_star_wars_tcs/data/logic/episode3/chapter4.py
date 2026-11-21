from rule_builder.rules import True_, And, Or

from ..macros import (
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_GRAPPLE,
    CAN_SITH_FORCE,
    CAN_DAMAGE_AT_CLOSE_RANGE,
    HAS_ANY_YODA,
)
from ..option_filters import logic_options
from ..rules import HasAbility, HasAnyAbilities, HasAllAbilities, HasAbilityCombination
from ..types import minikit_data, ExitData, Chapter, LocationData, MinikitData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN_PLATFORM = "Spawn Platform"
R_ORDER_66_PLATFORMS = "Order 66 Platforms"
R_RESCUE_WOOKIES_AREA = "Rescue Wookies Area"
R_BEACH_INVASION = "Beach Invasion"
R_SWAMP = "Swamp"
R_FOREST = "Forest"

CAN_BUILD_BEACH_CLONE_WALKER = logic_options(
    # Expect shooting the mines to reveal the brick.
    base=HasAllAbilities(BLASTER | CAN_BUILD_BRICKS),
    normal=HasAbility(CAN_BUILD_BRICKS),
)
_CAN_BUILD_BEACHFRONT_CLONE_WALKER_ER = CAN_BUILD_BEACH_CLONE_WALKER.and_rule(HasAbility(JEDI))

DEFENSE_OF_KASHYYYK = Chapter(
    area=Area.KASHYYYK,
    start_region=R_SPAWN_PLATFORM,
    regions={
        R_SPAWN_PLATFORM: (
            ExitData(
                R_ORDER_66_PLATFORMS,
                HasAbility(JEDI),
            ),
        ),
        R_ORDER_66_PLATFORMS: (
            ExitData(
                R_RESCUE_WOOKIES_AREA,
                True_(),
                er_rule=HasAbility(JEDI),
            ),
        ),
        R_RESCUE_WOOKIES_AREA: (
            ExitData(
                R_BEACH_INVASION,
                # Optimised out the HasAbility(JEDI) that is needed to reach here.
                logic_options(
                    base=CAN_GRAPPLE,
                    normal=HasAbility(GRAPPLE) | Extra.FORCE_GRAPPLE_LEAP.has(),
                    moderate=True_(),
                ),
                # In hard/moderate logic using Invincibility to make clones walk onto the buttons could also work.
                er_rule=logic_options(
                    # First Wookie.
                    base=CAN_GRAPPLE,
                    # Triple jump is just enough to make it up to the first platforms.
                    # You can also triple jump from the hat machine, but the jump doesn't seem any easier.
                    moderate=HasAnyAbilities(GRAPPLE | JEDI | CAN_HIGH_JUMP_SLAM),
                ).and_rule(
                    # Second Wookie.
                    # To spawn the grapple point, the boxes need to be destroyed and then the other object can be
                    # forced to spawn the grapple point.
                    logic_options(
                        base=HasAllAbilities(GRAPPLE | JEDI),
                        # Allow Force Grapple Leap.
                        normal=HasAbility(JEDI) & (HasAbility(GRAPPLE) | Extra.FORCE_GRAPPLE_LEAP.has()),
                        # Allow triple high jump.
                        # Allow triple jump. A near max height triple jump from one of the boxes or the forceable
                        # object is required, and Yoda is pretty difficult because he tends to slide off after just
                        # barely making the jump, due to his low walking speed and the edge of the platform being
                        # sloped. If Yoda makes it up to the platform, activate your lightsaber after landing to
                        # increase his walking speed and prevent him from sliding off.
                        moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM)
                    ),
                ).and_rule(
                    # Third Wookie.
                    CAN_DAMAGE_AT_CLOSE_RANGE,
                ),
                new_level=Level.KASHYYYK_B,
            ),
        ),
        R_BEACH_INVASION: (
            ExitData(
                R_SWAMP,
                logic_options(
                    base=True_(),
                    normal=Or(
                        HasAbility(BLASTER),
                        And(
                            HasAbility(WEAPON_EWOK),
                            Extra.has_any(Extra.SUPER_EWOK_CATAPULT, Extra.EXPLODING_BLASTER_BOLTS),
                        ),
                    ),
                    moderate=True_(),
                ),
                er_rule=logic_options(
                    # Note: The targets cannot be activated and are not auto-targeted until both the grapple point is
                    # revealed and the bridge is forced into place, so JEDI is required.
                    # the plant, and the bridge has been forced into place.
                    base=HasAbility(JEDI) & CAN_GRAPPLE,
                    normal=And(
                        HasAbility(JEDI),
                        Or(
                            And(
                                # Get up to the bridge
                                Or(
                                    _CAN_BUILD_BEACHFRONT_CLONE_WALKER_ER,
                                    CAN_GRAPPLE,
                                ),
                                # Activate the targets from the bridge (once the bridge and plant have been forced).
                                Or(
                                    # Shoot the targets like normal.
                                    HasAbility(BLASTER),
                                    # Shoot the targets with an ewok. The regular attacks are too low to hit the
                                    # targets, so an explosive Extra is needed.
                                    And(
                                        HasAbility(WEAPON_EWOK),
                                        Extra.has_any(Extra.SUPER_EWOK_CATAPULT, Extra.EXPLODING_BLASTER_BOLTS),
                                    ),
                                )
                            ),
                            # Shoot the targets from ground level.
                            HasAbility(BLASTER),
                        ),
                    ),
                    # While there are all sorts of logically interesting ways to activate the targets, you can just
                    # triple-jump over the gate.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
                new_level=Level.KASHYYYK_C,
            ),
        ),
        R_SWAMP: (
            ExitData(
                R_FOREST,
                True_(),
                er_rule=logic_options(
                    # Expect fighting the spawned droids to get through, but not killing the commander battle droids.
                    base=CAN_DAMAGE_AT_CLOSE_RANGE,
                    normal=True_(),
                ),
                new_level=Level.KASHYYYK_D,
            ),
        ),
        R_FOREST: (
            ExitData(
                "Chapter Completion",
                # All that's needed is a JEDI, which was needed at the very start of the chapter.
                True_(),
                er_rule=logic_options(
                    base=HasAbility(JEDI),
                    # Normal has to expect JEDI because there are two buttons to press simultaneously, but P2's AI won't
                    # follow you up unless you force the plants to reveal the platforms.
                    normal=HasAbility(JEDI),
                    moderate=And(
                        # To get up the cliff with rolling boulders.
                        HasAnyAbilities(JEDI | HIGH_JUMP | CAN_RIDE_VEHICLES),
                        # To activate the escape pod.
                        HasAbility(JEDI),
                    )
                ),
            ),
        ),
    },
    minikits={
        "Tall Tree High Platforms Minikit": minikit_data(
            R_RESCUE_WOOKIES_AREA,
            # Optimised out the HasAbility(JEDI) that is needed to reach here.
            logic_options(
                base=HasAllAbilities(GRAPPLE | JETPACK | HIGH_JUMP),
                normal=And(
                    HasAbility(GRAPPLE) | Extra.FORCE_GRAPPLE_LEAP.has(),
                    HasAllAbilities(HOVER | HIGH_JUMP),
                ),
                moderate=True_(),
            ),
            # The edge of the wookie platform is really annoying and tends to eat jumps.
            # Character swapping while on the edge of the platform can help to restore jumps.
            er_rule=logic_options(
                # Expect Jetpack because of the annoying edge of the wookie platform.
                base=CAN_GRAPPLE & HasAllAbilities(JETPACK | HIGH_JUMP),
                normal=CAN_GRAPPLE & HasAllAbilities(HOVER | HIGH_JUMP),
                # Pretty difficult with Yoda due to his reduced air movement speed during triple jumps.
                # Yoda can actually just double jump from the wookie platform to the next platform.
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="m_pup2"
        ),
        "Tall Tree Grapple Platform Minikit": minikit_data(
            R_RESCUE_WOOKIES_AREA,
            # Optimised out the HasAbility(JEDI) that is needed to reach here.
            logic_options(
                base=HasAbility(JEDI),
                normal=True_(),
            ),
            er_rule=logic_options(
                # Clearly the developer intended solution.
                base=HasAbility(GRAPPLE),
                # Avoid destroying one of the boxes, and a Jedi can stand on a box to jump up these platforms.
                # High jump can jump straight up to the lower of the two platforms.
                normal=HasAnyAbilities(JEDI | HIGH_JUMP | GRAPPLE),
            ),
            pickup_name="m_pup1",
        ),
        "Beach Rock Minikit": minikit_data(
            R_BEACH_INVASION,
            logic_options(
                base=HasAbility(HIGH_JUMP),
                # All Jedi can build and ride the Clone Walker.
                normal=HasAnyAbilities(HIGH_JUMP | JEDI),
            ),
            er_rule=logic_options(
                base=HasAbility(HIGH_JUMP),
                normal=Or(
                    HasAbility(HIGH_JUMP),
                    # Build the walker and use that to get extra height.
                    _CAN_BUILD_BEACHFRONT_CLONE_WALKER_ER & HasAbility(JEDI),
                ),
                # Triple jump.
                moderate=HasAnyAbilities(HIGH_JUMP | JEDI),
            ),
            pickup_name="mk_0"
        ),
        "Beach High Platform Minikit": minikit_data(
            R_BEACH_INVASION,
            # Optimised out the HasAbility(JEDI) (+GRAPPLE on base logic) that is needed to reach here.
            logic_options(
                base=HasAllAbilities(HIGH_JUMP | HOVER),
                # All Jedi can build the Clone Walker, ride it, and then triple jump out of it to the minikit.
                moderate=True_(),
            ),
            er_rule=logic_options(
                base=HasAllAbilities(HIGH_JUMP | HOVER),
                moderate=Or(
                    # Jedi, except yodas, can take the intended HIGH_JUMP+HOVER route.
                    # Triple high jump can take the same route, but can also triple high jump from the boulders to the
                    # right.
                    HasAnyAbilities(CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM),
                    # Build the walker, then triple jump or high jump out of it (high jump is irrelevant because a Jedi
                    # is needed for build the walker).
                    _CAN_BUILD_BEACHFRONT_CLONE_WALKER_ER & HasAbilityCombination(JEDI | CAN_RIDE_VEHICLES)
                )
            ),
            pickup_name="m_pup2",
        ),
        "Beach Force Three Carrots Miniki": MinikitData(
            R_BEACH_INVASION,
            # Base/Normal requires JEDI + can_grapple to get here.
            # Moderate+ requires JEDI to get here, and all Jedi can build the Clone Walker, ride it, and then double
            # jump to the minikit.
            True_(),
            er_rule=logic_options(
                base=HasAbility(JEDI) & CAN_GRAPPLE,
                normal=And(
                    HasAbility(JEDI),
                    Or(
                        _CAN_BUILD_BEACHFRONT_CLONE_WALKER_ER,
                        CAN_GRAPPLE,
                    ),
                ),
            ),
            pickup_names=(
                "m_pup1",
                "m_pup3",
                "m_pup4",
            ),
        ),
        "Minikit Above Crashed Clone Arcfighter": minikit_data(
            R_SWAMP,
            logic_options(
                base=HasAbility(HIGH_JUMP),
                normal=True_(),
            ),
            er_rule=logic_options(
                # Expect defeating the commanders to more easily force the Arcfighter.
                base=HasAllAbilities(JEDI | HIGH_JUMP),
                # To easily lift the Arcfighter, use the Power Up; it enables Deflect Bolts and Fast Force. Then double
                # jump to the minikit.
                normal=HasAbility(JEDI),
            ),
            pickup_name="m_pup1",
        ),
        "Minikit By Right Commander Battle Droid": minikit_data(
            R_SWAMP,
            logic_options(
                base=HasAbility(HIGH_JUMP),
                normal=True_(),
            ),
            er_rule=logic_options(
                # Expect high jump because it is not obvious that a double jump can get up here.
                # Expect defeating the commander too.
                base=HasAbility(HIGH_JUMP) & CAN_DAMAGE_AT_CLOSE_RANGE,
                # The terrain below the commander slopes up in the direction away from the spawn into the swamp, which
                # gives enough height to double jump up to the commander and the minikit.
                normal=HasAbility(CAN_DOUBLE_JUMP),
            ),
            pickup_name="m_pup2",
        ),
        "Minikit Above Sith Force Bush": minikit_data(
            R_FOREST,
            logic_options(
                # JEDI and can_grapple are required to reach here.
                base=HasAllAbilities(SITH | HOVER),
                # JEDI and can_grapple are required to reach here.
                normal=Or(
                    And(
                        HasAbility(SITH) | Extra.DARK_SIDE.has(),
                        HasAbility(HOVER),
                    ),
                    HasAbilityCombination(HIGH_JUMP | CAN_RIDE_VEHICLES),
                ),
                # JEDI is required to reach here.
                moderate=True_(),
            ),
            er_rule=logic_options(
                base=CAN_SITH_FORCE & CAN_GRAPPLE & HasAbility(HOVER),
                normal=Or(
                    CAN_SITH_FORCE & CAN_GRAPPLE & HasAbility(HOVER),
                    # Fight the Clone Walker, then ride it as a High Jump character, and then high jump out of the
                    # walker and up to the minikit platform.
                    CAN_DAMAGE_AT_CLOSE_RANGE & HasAbilityCombination(HIGH_JUMP | CAN_RIDE_VEHICLES),
                ),
                moderate=Or(
                    # Triple jump can cross the gap between the grapple platform and minikit platform.
                    CAN_SITH_FORCE & CAN_GRAPPLE,
                    CAN_DAMAGE_AT_CLOSE_RANGE & HasAbilityCombination(HIGH_JUMP | CAN_RIDE_VEHICLES),
                    # Fight the Clone Walker, like in the High Jump case, but a Jedi can triple jump out of the walker
                    # and up to the platform.
                    HasAbilityCombination(JEDI | CAN_RIDE_VEHICLES),
                    # Triple high jump up to the platform.
                    HasAbility(CAN_HIGH_JUMP_SLAM),
                    # For some reason, Yoda can repeatedly jump up the tree to the left by the Dark Side Bush, through
                    # this is irrelevant because all Jedi can ride vehicles and then triple jump up to the platform.
                    HAS_ANY_YODA,
                ),
            ),
            pickup_name="m_pup2",
        ),
        "Minikit Above Rolling Boulders": minikit_data(
            R_FOREST,
            logic_options(
                # Base and normal need JEDI and can_grapple to get here.
                base=True_(),
                moderate=CAN_GRAPPLE,
                # It's possible to get here without grapple, and with Yoda, who cannot make the triple jump from the
                # button.
                hard=CAN_GRAPPLE | HasAnyAbilities(CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM)
            ),
            er_rule=logic_options(
                base=HasAbility(JEDI) & CAN_GRAPPLE,
                normal=And(
                    # Grapple needed to reach the minikit.
                    CAN_GRAPPLE,
                    # Force the plants to spawn platforms.
                    # High jump up, ignoring the plants.
                    # Ride the Clone Walker and use it to jump onto the section with rolling boulders.
                    HasAnyAbilities(JEDI | HIGH_JUMP | CAN_RIDE_VEHICLES),
                ),
                hard=Or(
                    # From the left button, triple jump can reach the other side of the block of stone that the minikit
                    # is on, and then jump over the stone on top to get to the minikit.
                    # This requires Hard logic because there is a close stone that would be easier to jump to, but there
                    # is an invisible wall that prevents jumping on that stone, so it is not obvious at all, that the
                    # other side of the stone the minikit is on is *not* blocked by an invisible wall.
                    HasAnyAbilities(CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM),
                    And(
                        # Grapple needed to reach the minikit.
                        CAN_GRAPPLE,
                        # High jump up, ignoring the plants.
                        # Ride the Clone Walker and use it to jump onto the section with rolling boulders.
                        HasAnyAbilities(HIGH_JUMP | CAN_RIDE_VEHICLES),
                    )
                )
            ),
            pickup_name="m_pup1",
        ),
        "Minikit Above Escape Pod": minikit_data(
            R_FOREST,
            logic_options(
                base=HasAbility(HIGH_JUMP),
                # Ride the Clone Walker and double jump out, or force the escape pod most of the way up and then jump to
                # the minikit using the escape pod as a platform.
                normal=True_()
            ),
            pickup_name="m_pup3",
        )
    },
    power_brick=LocationData(
        R_ORDER_66_PLATFORMS,
        # JEDI is needed to reach here, so the normal+ rules can be slightly optimised.
        logic_options(
            base=HasAllAbilities(SITH | BOUNTY_HUNTER),
            normal=HasAbility(SITH) | Extra.DARK_SIDE.has() & CAN_DESTROY_CLOSE_SILVER_BRICKS,
        ),
        er_rule=CAN_SITH_FORCE & CAN_DESTROY_CLOSE_SILVER_BRICKS,
    ),
    ridables={
        Character.CLONEWALKER: LocationData(
            R_BEACH_INVASION,
            # If you could somehow get to the forest without being able to build the one on the beach, there is also a
            # walker being piloted by an enemy in the forest, requiring only the ability to damage/force it to be able
            # to ride it yourself.
            CAN_BUILD_BEACH_CLONE_WALKER,
            er_rule=_CAN_BUILD_BEACHFRONT_CLONE_WALKER_ER,
        ),
    },
)