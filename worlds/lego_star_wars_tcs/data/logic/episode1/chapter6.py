from rule_builder.rules import Or, True_, False_, And

from ..macros import (
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    can_jump_distance_rule,
    CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
    CAN_YODA_CLIP,
    HAS_WALL_CLIMB,
    HAS_ANY_YODA,
)
from ..option_filters import logic_options
from ..rules import HasAbility, HasAllAbilities, HasAnyAbilities, HasAbilityExceptCharacters
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN = "Spawn"
R_HANGAR = "Hangar"
R_IMPERIAL_ROOM = "Imperial Room"
R_TOWER_ROOM = "Tower Room"
R_TOWER_ROOM_TOP = "Tower Room Top"
R_ENERGY_COLUMNS_ROOM = "Energy Columns Room"
R_MAUL_BOSS_ROOM = "Maul Boss Room"

_CAN_YODA_GRAB_TOWER_MINIKIT_BEHIND_SILVER_BRICKS = And(
    HAS_ANY_YODA,
    Or(
        # Grab through both the grate and force field.
        HasAbilityExceptCharacters(
            JEDI,
            Character.YODA,
            Character.YODA_GHOST,
            # Luke cannot Yoda Grab.
            Character.LUKE_SKYWALKER_DAGOBAH,
            Character.LUKE_SKYWALKER_BESPIN,
            Character.LUKE_SKYWALKER_JEDI,
            Character.LUKE_SKYWALKER_ENDOR,
            # Custom characters also cannot Yoda Grab, but they don't have the JEDI ability on their own, so don't need
            # to be considered for logic here.
        ),
        # Grievous does not need to be considered because triple-high-jump can get the minikit on their own.
        # Character.GENERAL_GRIEVOUS.has(),
        Character.IMPERIAL_GUARD.has(),
        # Tarpals cannot get enough grab distance and I don't think this works with Ackbar, whose Yoda Grab requires his
        # dive roll, meaning he ends up too high to grab the minikit, even if the grab distance was enough.
    )
)

DARTH_MAUL = Chapter(
    area=Area.MAUL,
    start_region=R_SPAWN,
    intended_completion_path={
        "base": (
            R_HANGAR,
            R_TOWER_ROOM,
            R_ENERGY_COLUMNS_ROOM,
            R_MAUL_BOSS_ROOM,
        ),
        "moderate": (
            R_HANGAR,
            R_TOWER_ROOM,
            # R_TOWER_ROOM -> R_ENERGY_COLUMNS_ROOM is disabled due to being logically irrelevant.
            R_TOWER_ROOM_TOP,
            R_ENERGY_COLUMNS_ROOM,
            R_MAUL_BOSS_ROOM,
        ),
    },
    regions={
        R_SPAWN: (
            ExitData(
                R_HANGAR,
                logic_options(
                    # Fight Maul from across the gap, then force the bridge.
                    base=HasAbility(IS_NON_GHOST_JEDI),
                    # High jump can actually just jump onto the floating bridge, and walk across. Maul runs away when
                    # the player gets close to him.
                    # The high jump is a bit too difficult/inconsistent with Jar Jar/Captain Tarpals, but is pretty easy
                    # with General Grievous and Bodyguard.
                    normal=HasAnyAbilities(IS_NON_GHOST_JEDI | CAN_HIGH_JUMP_SLAM),
                    # Allow Jar Jar/Captain Tarpals and triple jump.
                    # Allow Ackbar by hovering across to the light, part way across the gap, and then double jumping
                    # across the rest of the gap.
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP) | HasAllAbilities(CAN_DOUBLE_JUMP | HOVER),
                )
            ),
        ),
        R_HANGAR: (
            ExitData(
                R_IMPERIAL_ROOM,
                logic_options(
                    # IS_NON_GHOST_JEDI implies JEDI.
                    base=HasAbility(IMPERIAL),
                    normal=HasAllAbilities(JEDI | IMPERIAL),
                    moderate=HasAbility(IMPERIAL) & HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM)
                ).or_rule(
                    apply_to="hard+",
                    rule=CAN_YODA_CLIP | HAS_WALL_CLIMB,
                ),
                er_rule=logic_options(
                    # Force the platforms with P2, then use the Imperial panel.
                    base=HasAllAbilities(JEDI | IMPERIAL),
                    # Alternatively, triple high jump all the way up.
                    moderate=HasAbility(IMPERIAL) & HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM)
                ).or_rule(
                    # Alternatively, you can Yoda Clip through the ceiling in front of the panel and fall down on the
                    # other side of the panel, then walk into the transition.
                    # Alternatively, you can Wall Climb up the outside and go all the way over the top of the wall
                    # collision. To make things easier for you, note that the walls, either side of the alcove
                    # containing the Imperial panel, have floor collision on top, so you can Wall Climb all the way up,
                    # and then drop down onto the top of one of these walls to more easily walk far enough to get over
                    # the Imperial panel 'door', without going too far that you hit the backwards transition instead of
                    # the forwards transition.
                    apply_to="hard+",
                    rule=CAN_YODA_CLIP | HAS_WALL_CLIMB,
                ),
                new_level=Level.MAUL_B,
            ),
            ExitData(
                R_TOWER_ROOM,
                new_level=Level.MAUL_B,
            ),
        ),
        R_IMPERIAL_ROOM: (),
        R_TOWER_ROOM: (
            ExitData(
                R_TOWER_ROOM_TOP,
                logic_options(
                    # IS_NON_GHOST_JEDI implies JEDI.
                    base=HasAbility(GRAPPLE),
                    # Allow Force Grapple Leap.
                    normal=Or(
                        HasAnyAbilities(JEDI | HIGH_JUMP) & HasAbility(GRAPPLE),
                        HasAbility(JEDI) & Extra.FORCE_GRAPPLE_LEAP.has(),
                    ),
                    # HasAnyAbilities(JEDI | HIGH_JUMP) was used at "Spawn -> Hangar"
                    moderate=True_(),
                ),
                er_rule=logic_options(
                    # Jump up to and use the grapple point.
                    base=HasAnyAbilities(JEDI | HIGH_JUMP) & HasAbility(GRAPPLE),
                    # Allow Force Grapple Leap.
                    normal=Or(
                        HasAnyAbilities(JEDI | HIGH_JUMP) & HasAbility(GRAPPLE),
                        HasAbility(JEDI) & Extra.FORCE_GRAPPLE_LEAP.has(),
                    ),
                    # The wall collision near the grapple point can be stood on to jump up to the end of the grapple
                    # point.
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP),
                ),
            ),
            ExitData(
                R_ENERGY_COLUMNS_ROOM,
                logic_options(
                    base=True_(),
                    normal=HasAbility(JEDI),
                    # This entrance is now useless to include in logic because the R_TOWER_ROOM_TOP path can be taken.
                    moderate=False_(),
                ),
                er_rule=HasAbility(JEDI),
                # maul_c does not exist.
                new_level=Level.MAUL_D,
            ),
        ),
        R_TOWER_ROOM_TOP: (
            # Just drop down.
            # maul_c does not exist.
            ExitData(R_ENERGY_COLUMNS_ROOM, new_level=Level.MAUL_D),
        ),
        R_ENERGY_COLUMNS_ROOM: (
            # Logically, fighting the Droideka and going through the force doors corridor (maul_e), is skipped and the
            # logic goes straight to the boss fight (maul_f).
            # Note: In higher logic, Blasters can skip fighting the Droidekas by shooting Maul into the pit.
            # Note: In expert logic, you can get out-of-bounds in the energy shield corridor room with Grievous by wall
            #  climbing at the start of the level, and then walk under the level, bypassing everything and then jumping
            #  back in-bounds at the level transition to the boss fight. This would allow for reaching the boss fight
            #  without JEDI, which is currently assumed to be present by the minikits within the Boss Fight. I don't
            #  currently know about other out-of-bounds strategies in this level.
            ExitData(
                R_MAUL_BOSS_ROOM,
                logic_options(
                    # IS_NON_GHOST_JEDI implies JEDI.
                    base=True_(),
                    normal=HasAbility(JEDI),
                ),
                er_rule=HasAbility(JEDI),
                new_level=Level.MAUL_F,
            ),
        ),
        R_MAUL_BOSS_ROOM: (
            ExitData(
                "Chapter Completion",
                # ER Note: Would be more complicated, but for now, assume JEDI was needed to reach here.
                # HasAbility(JEDI),
            ),
        ),
    },
    minikits={
        "Left Starfighter Minikit": minikit_data(
            R_HANGAR,
            er_rule=HasAnyAbilities(JEDI | HIGH_JUMP),
            pickup_name="m_pup2",
        ),
        "Right Starfighter Minikit": minikit_data(
            R_HANGAR,
            er_rule=HasAnyAbilities(JEDI | HIGH_JUMP),
            pickup_name="m_pup1",
        ),
        "Imperial Room Minikit": minikit_data(
            R_IMPERIAL_ROOM,
            logic_options(
                # Base: IS_NON_GHOST_JEDI implies JEDI.
                # Normal: HasAllAbilities(JEDI | IMPERIAL) is required.
                base=True_(),
                moderate=HasAbility(JEDI),
            ),
            er_rule=HasAbility(JEDI),
            pickup_name="m_pup3",
        ),
        "Top Of Tower Minikit": minikit_data(
            R_TOWER_ROOM_TOP,
            logic_options(
                # IS_NON_GHOST_JEDI implies JEDI.
                base=True_(),
                # Normal can get here with General Grievous and GRAPPLE.
                # Moderate can get here with just HIGH_JUMP.
                normal=HasAbility(JEDI),
            ),
            er_rule=logic_options(
                base=HasAbility(JEDI),
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="m_pup2",
        ),
        "Behind Silver Bricks Minikit": minikit_data(
            R_TOWER_ROOM,
            # IS_NON_GHOST_JEDI implies CAN_JUMP_DISTANCE_0_69.
            # Normal: HasAbility(IS_NON_GHOST_JEDI) | Character.GENERAL_GRIEVOUS.has() implies CAN_JUMP_DISTANCE_0_69.
            # Moderate: HasAnyAbilities(JEDI | HIGH_JUMP) implies CAN_JUMP_DISTANCE_0_69.
            logic_options(
                strict=False,
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS,
            ).or_rule(
                apply_to="hard+",
                rule=Or(
                    HasAbility(CAN_HIGH_JUMP_SLAM),
                    _CAN_YODA_GRAB_TOWER_MINIKIT_BEHIND_SILVER_BRICKS,
                ),
            ),
            er_rule=logic_options(
                # The first gap, at its shortest point is 0.8296566898853424.
                # The second gap, at its shortest point is 0.8234030011015903.
                # Han Solo (jump_distance=0.84) can comfortably jump across.
                # Dexter Jettstar (jump_distance=0.77) can make it with a decent jump.
                # Ewok (jump_distance=0.69) can barely make it.
                base=can_jump_distance_rule(0.83),
                normal=CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
                # Include Ewok and other slow characters that can only barely get enough jump distance.
                moderate=HasAbility(CAN_JUMP_DISTANCE_0_69),
            ).and_rule(
                CAN_DESTROY_CLOSE_SILVER_BRICKS
            ).or_rule(
                apply_to="hard+",
                rule=Or(
                    # Triple-high-jump over both the forwards and backwards transitions. Walk all the way down the
                    # corridor and then move back in the air after falling off the end of the corridor to land on the
                    # floor of the corridor below and walk all the way back to the minikit. The Silver Bricks have no
                    # collision on the back, so you can just walk out.
                    HasAbility(CAN_HIGH_JUMP_SLAM),
                    # Yoda Grab the minikit from outside the Silver Bricks.
                    _CAN_YODA_GRAB_TOWER_MINIKIT_BEHIND_SILVER_BRICKS,
                ),
            ),
            pickup_name="m_pup1",
        ),
        "Imperial Platform Minikit": minikit_data(
            R_ENERGY_COLUMNS_ROOM,
            logic_options(
                base=HasAbility(IMPERIAL),
                normal=HasAnyAbilities(IMPERIAL | JETPACK),
            ),
            pickup_name="m_pup1",
        ),
        "Energy Column Minikit": minikit_data(
            R_ENERGY_COLUMNS_ROOM,
            # Base: IS_NON_GHOST_JEDI implies CAN_JUMP_DISTANCE_0_69.
            # Normal: HasAbility(IS_NON_GHOST_JEDI) | Character.GENERAL_GRIEVOUS.has() implies CAN_JUMP_DISTANCE_0_69.
            # Moderate: HasAnyAbilities(JEDI | HIGH_JUMP) implies CAN_JUMP_DISTANCE_0_69.
            True_(),
            # The first gap is about 0.8650856462150265, though Ewok can cross it without too much trouble.
            # Boba Fett (Boy) cannot cross it.
            # The second gap is about 0.9404286708182122 and is just too big for Ewok/Clone to cross it.
            # Dexter Jettster (jump_distance=0.77) can make it across with a decent jump.
            # Han Solo (jump_distance=0.84) cannot make it without coyote/sliding-off time, but it is otherwise an easy
            # jump.
            # The final jump to the energy column platform is about 0.765745545551385 (maybe a little lower at the
            # closest point).
            er_rule=logic_options(
                base=HasAbility(CAN_JUMP_DISTANCE_0_84),
                normal=CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
            ),
            pickup_name="mk_1",  # "mk_1" + "\x00" + "2"
        ),
        "Maul Fight Minikit 2": minikit_data(
            R_MAUL_BOSS_ROOM,
            logic_options(
                # ER Note: Currently assuming JEDI is required to reach this room.
                # High jump up on the platform and then jump to the minikit.
                base=HasAbility(HIGH_JUMP),
                # The platform can be forced down enough to double jump onto, then wait for the platform to rise again,
                # and then the minikit can be double jumped to.
                # Note: Forcing the platform too low destroys it, requiring a level restart.
                normal=True_(),
                # Moderate: Triple jump instead of high jump.
            ),
            pickup_name="m_pup1",
        ),
        "Maul Fight Minikit 1": minikit_data(
            R_MAUL_BOSS_ROOM,
            logic_options(
                # ER Note: Currently assuming JEDI is required to reach this room.
                # High jump up on the platform and then jump to the minikit.
                base=HasAbility(HIGH_JUMP),
                # The platform can be forced down enough to double jump onto, then wait for the platform to rise again,
                # and then the minikit can be double jumped to, with a slam used to get the extra height needed.
                # Note: Forcing the platform too low destroys it.
                normal=True_(),
                # Moderate: Triple jump instead of high jump.
            ),
            pickup_name="m_pup2",
        ),
        "Maul Fight Minikit 3": minikit_data(
            R_MAUL_BOSS_ROOM,
            logic_options(
                # ER Note: Currently assuming JEDI is required to reach this room.
                # High jump up on the platform and then jump to the minikit.
                base=HasAbility(HIGH_JUMP),
                # The platform can be forced down enough to double jump onto, then wait for the platform to rise again,
                # and then the minikit can be double jumped to.
                # Note: Forcing the platform too low destroys it.
                normal=True_(),
                # Moderate: Triple jump instead of high jump.
            ),
            pickup_name="m_pup3",
        ),
    },
    power_brick=LocationData(R_IMPERIAL_ROOM),
    ridables={
        Character.SERVICE_CAR: LocationData(R_HANGAR),
    },
)
