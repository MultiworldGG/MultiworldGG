from rule_builder.rules import And, Or, False_, True_

from ..macros import CAN_USE_SELF_DESTRUCT
from ..option_filters import logic_options
from ..rules import HasAbility, HasAllAbilities, HasAnyAbilities, HasAnyCharacterExcept
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_FOREST_SPAWN = "Forest Spawn"
R_AFTER_FIRST_FALLEN_TREE = "After First Fallen Tree"
R_AFTER_CRASHED_MTT = "After Crashed MTT"
R_CLIFF_FACE_RUINS_ENTRANCE = "Cliff Face Ruins Entrance"
R_CLIFF_FACE_RUINS_COLLAPSING_DEBRIS_SECTION = "Cliff Face Ruins Collapsing Debris Section"
R_CLIFF_FACE_RUINS_PAST_COLLAPSING_DEBRIS = "Cliff Face Ruins Past Collapsing Debris"
R_CLIFF_FACE_RUINS_RAISED_SQUARE = "Cliff Face Ruins Raised Square"
R_CLIFF_FACE_RUINS_END_PLATFORM = "Cliff Face Ruins End Platform"
R_SWAMP_RUINS_ENTRANCE = "Swamp Ruins Entrance"
R_SWAMP_RUINS = "Swamp Ruins"
R_SWAMP_BEFORE_WATER = "Swamp Before Water"

INVASION_OF_NABOO = Chapter(
    area=Area.GUNGAN,
    start_region=R_FOREST_SPAWN,
    intended_completion_path={
        "base": (
            R_AFTER_FIRST_FALLEN_TREE,
            R_AFTER_CRASHED_MTT,
            R_CLIFF_FACE_RUINS_ENTRANCE,
            R_CLIFF_FACE_RUINS_COLLAPSING_DEBRIS_SECTION,
            R_CLIFF_FACE_RUINS_PAST_COLLAPSING_DEBRIS,
            R_CLIFF_FACE_RUINS_END_PLATFORM,
            R_SWAMP_RUINS_ENTRANCE,
            R_SWAMP_RUINS,
            R_SWAMP_BEFORE_WATER,
        ),
    },
    regions={
        R_FOREST_SPAWN: (
            # Expert logic could get past the tree without a jedi.
            ExitData(
                R_AFTER_FIRST_FALLEN_TREE,
                logic_options(
                    base=HasAbility(JEDI),
                    # Allow triple-high-jump. All jedi can actually triple jump high enough to go over the top of the
                    # tree, though it's a bit close with non-Yoda jedi.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
        ),
        R_AFTER_FIRST_FALLEN_TREE: (
            ExitData(
                R_AFTER_CRASHED_MTT,
                er_rule=logic_options(
                    base=HasAbility(JEDI),
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP)
                ),
            ),
        ),
        R_AFTER_CRASHED_MTT: (
            ExitData(R_CLIFF_FACE_RUINS_ENTRANCE, new_level=Level.GUNGAN_B),
        ),
        R_CLIFF_FACE_RUINS_ENTRANCE: (
            # Hover across the gap or force down the mosaic.
            ExitData(
                R_CLIFF_FACE_RUINS_COLLAPSING_DEBRIS_SECTION,
                logic_options(
                    base=True_(),
                    moderate=HasAnyAbilities(JEDI | HOVER) | Character.GENERAL_GRIEVOUS.has(),
                    # JEDI | CAN_HIGH_JUMP_SLAM is required towards the start.
                    hard=True_(),
                ),
                er_rule=logic_options(
                    base=HasAbility(JEDI),
                    # Allow HOVER (P2 AI only follows if the mosaic is forced)
                    normal=HasAnyAbilities(JEDI | HOVER),
                    # Allow Grievous's triple jump, but not Bodyguard.
                    moderate=HasAnyAbilities(JEDI | HOVER) | Character.GENERAL_GRIEVOUS.has(),
                    # Allow Bodyguard's triple jump by jumping to the top of the waterfall, and then across.
                    hard=HasAnyAbilities(JEDI | HOVER | CAN_HIGH_JUMP_SLAM),
                ),
            ),
        ),
        R_CLIFF_FACE_RUINS_COLLAPSING_DEBRIS_SECTION: (
            ExitData(
                R_CLIFF_FACE_RUINS_PAST_COLLAPSING_DEBRIS,
                logic_options(
                    base=HasAbility(HIGH_JUMP),
                    moderate=True_(),
                ),
                er_rule=logic_options(
                    base=HasAllAbilities(JEDI | HIGH_JUMP),
                    # Jedi triple jump gets more height than a high jump.
                    # There is, however a collapsing debris that sits in a dip, so requires a high triple jump to get on
                    # top without.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    # From the first collapsing platform, a high double jump is just enough to collapse the second
                    # platform without needing a jedi.
                    # A jetpack can also get across here by jumping from each collapsing platform and then hovering to
                    # the next, but needs a High Jump/Jedi to get up at the start.
                    # Restarting the level is required to re-attempt, so this is in Hard logic.
                    hard=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM) | HasAllAbilities(HIGH_JUMP | JETPACK),
                ),
            ),
            ExitData(
                R_CLIFF_FACE_RUINS_RAISED_SQUARE,
                logic_options(
                    base=False_(),
                    hard=HasAbility(JETPACK),
                ),
                er_rule=logic_options(
                    # Not expected, use the exit from R_CLIFF_FACE_RUINS_PAST_COLLAPSING_DEBRIS instead.
                    base=False_(),
                    # Triple or high jump up to the first collapsing platform, then jumping from each collapsing
                    # platform and then hovering to the next, it is possible to get to the top of the raised square.
                    # Restarting the level is required to re-attempt, so this is in Hard logic.
                    hard=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM) & HasAbility(JETPACK),
                ),
            ),
        ),
        # This is the lower area around the Raised Square platform.
        R_CLIFF_FACE_RUINS_PAST_COLLAPSING_DEBRIS: (
            ExitData(
                R_CLIFF_FACE_RUINS_END_PLATFORM,
                er_rule=logic_options(
                    # Force down the blocks from on top of the square to make a platform, then jump up.
                    base=HasAbility(JEDI),
                    # Triple jump up, ignoring the force blocks.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
            ExitData(
                R_CLIFF_FACE_RUINS_RAISED_SQUARE,
                er_rule=logic_options(
                    # Force down the blocks on the top of the square and then high jump up.
                    base=HasAllAbilities(JEDI | HIGH_JUMP),
                    # Triple jump up (don't even need to force down the blocks).
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
        ),
        R_CLIFF_FACE_RUINS_RAISED_SQUARE: (
            ExitData(
                R_CLIFF_FACE_RUINS_END_PLATFORM,
                logic_options(
                    base=False_(),
                    normal=HasAbility(JETPACK),
                    moderate=True_(),
                ),
                er_rule=logic_options(
                    # Not expected, use the exit from R_CLIFF_FACE_RUINS_PAST_COLLAPSING_DEBRIS instead.
                    base=False_(),
                    # Jump and jetpack hover across.
                    normal=HasAbility(JETPACK),
                    # There is a cliff face alcove that gives extra starting height, so astromech hover is enough to
                    # cross.
                    # Triple jump can just jump straight over.
                    moderate=HasAnyAbilities(HOVER | JEDI | CAN_HIGH_JUMP_SLAM),
                    # A regular high jump can also just barely cross the gap from the cliff face alcove.
                    hard=HasAnyAbilities(HOVER | JEDI | CAN_HIGH_JUMP_SLAM | HIGH_JUMP),
                ),
            ),
            # This exit might not be needed, but including it won't really hurt.
            ExitData(
                # Just drop down.
                R_CLIFF_FACE_RUINS_PAST_COLLAPSING_DEBRIS,
            ),
        ),
        R_CLIFF_FACE_RUINS_END_PLATFORM: (
            ExitData(
                R_CLIFF_FACE_RUINS_RAISED_SQUARE,
                logic_options(
                    base=False_(),
                    normal=HasAbility(HOVER),
                    moderate=True_(),
                ),
                er_rule=logic_options(
                    # Not intended.
                    base=False_(),
                    normal=HasAbility(HOVER),
                    moderate=HasAnyAbilities(HOVER | JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
            ExitData(
                R_SWAMP_RUINS_ENTRANCE,
                new_level=Level.GUNGAN_C
            ),
        ),
        R_SWAMP_RUINS_ENTRANCE: (
            ExitData(
                R_SWAMP_RUINS,
                logic_options(
                    base=True_(),
                    moderate=HasAbility(JEDI),
                    hard=True_(),
                ),
                er_rule=logic_options(
                    # Move the blocks out of the way to collapse the log.
                    base=HasAbility(JEDI),
                    # A triple jump can bypass the log entirely, but the jump is quite tight, so is only in Hard logic.
                    # Jar Jar + Tarpals can also make the jump as far as I know.
                    hard=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM | HIGH_JUMP),
                ),
            ),
        ),
        R_SWAMP_RUINS: (
            # ExitData(
            #     "Swamp Behind MTT",
            #     # The collision for the MTT is enormous, though there's probably ways to get out-of-bounds to get
            #     # behind it.
            #     # One of the trees close by can be stood on to help with getting out-of-bounds.
            #     can_destroy_close_silver_bricks,
            # ),
            ExitData(
                R_SWAMP_BEFORE_WATER,
                er_rule=logic_options(
                    # High jump up to get on top of the collapsing debris.
                    base=HasAbility(HIGH_JUMP),
                    # Alternatively, jump + jetpack hover across from the higher swamp area.
                    normal=HasAnyAbilities(HIGH_JUMP | JETPACK),
                    # Triple jump up with a jedi instead.
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP | JETPACK),
                    # The collision on the boards is busted, and can be used to clip inside the wall, or jump on top of
                    # the wall.
                    hard=HasAnyAbilities(JEDI | HIGH_JUMP | JETPACK | CAN_JUMP_HEIGHT_0_37),
                ),
                new_level=Level.GUNGAN_E,
            ),
        ),
        # There is nothing of logical relevance here yet, so this region is disabled for now.
        # "Swamp Behind MTT": (),
        R_SWAMP_BEFORE_WATER: (
            ExitData(
                # Just walk.
                "Chapter Completion",
            ),
        ),
    },
    minikits={
        "Shoot Target Minikit": minikit_data(
            R_FOREST_SPAWN,
            logic_options(
                # Shoot the target, then force the boulders and jump up to the minikit.
                base=HasAllAbilities(JEDI | BLASTER),
                # Stacking the boulders allows an ewok to hit the target.
                # High jump can be expected instead of a jedi, but requires a blaster character.
                normal=Or(
                    HasAbility(JEDI) & HasAnyAbilities(BLASTER | WEAPON_EWOK),
                    HasAllAbilities(HIGH_JUMP | BLASTER)
                ),
                moderate=Or(
                    And(
                        HasAnyAbilities(JEDI | HIGH_JUMP),
                        Or(
                            HasAbility(BLASTER),
                            # The explosion allows Ewok to hit the target without needing a Jedi to move the boulders
                            # for extra height.
                            And(
                                HasAbility(WEAPON_EWOK),
                                Extra.has_any(Extra.SUPER_EWOK_CATAPULT, Extra.EXPLODING_BLASTER_BOLTS)
                            ),
                            # Self-destruct can also hit the target.
                            CAN_USE_SELF_DESTRUCT,
                        )
                    ),
                    # With only an ewok, a Jedi is still required to move the boulders so the ewok can hit the target.
                    HasAllAbilities(JEDI | WEAPON_EWOK),
                )
            ),
            pickup_name="m_pup2",
        ),
        "Destroy Fallen Tree Minikit": minikit_data(
            R_AFTER_FIRST_FALLEN_TREE,
            er_rule=HasAbility(JEDI),
            pickup_name="m_pup1",
        ),
        "Minikit Above Crashed MTT": minikit_data(
            R_AFTER_FIRST_FALLEN_TREE,
            er_rule=logic_options(
                # Destroy the MTT using the force.
                base=HasAbility(JEDI),
                # A high jump from the MTT's side-cannon is just enough to get on top of the MTT's hitbox.
                moderate=HasAnyAbilities(JEDI | HIGH_JUMP),
            ),
            pickup_name="m_pOOP1",
        ),
        "Minikit Under Crashed MTT": minikit_data(
            R_AFTER_FIRST_FALLEN_TREE,
            logic_options(
                base=True_(),
                moderate=HasAbility(JEDI),
            ),
            er_rule=HasAbility(JEDI),
            pickup_name="m_pOOP3",
        ),
        "High Minikit Above Steps": minikit_data(
            R_AFTER_CRASHED_MTT,
            logic_options(
                base=HasAbility(HIGH_JUMP),
                moderate=True_(),
            ),
            er_rule=logic_options(
                base=HasAllAbilities(JEDI | HIGH_JUMP),
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="m_pOOP2",
        ),
        "Minikit On Top Of Raised Square": minikit_data(
            R_CLIFF_FACE_RUINS_RAISED_SQUARE,
            pickup_name="m_pup1",
        ),
        "Minikit In Ruins Alcove": minikit_data(
            R_SWAMP_RUINS_ENTRANCE,
            logic_options(
                base=True_(),
                # Moderate can get here with just Grievous.
                # Hard can get here with just Grievous/Bodyguard.
                moderate=HasAbility(JEDI),
            ),
            er_rule=logic_options(
                base=HasAbility(JEDI),
                # Just fall down next to it.
                # todo: I thought you simply couldn't get this without forcing the bricks down?
                normal=True_()
            ),
            pickup_name="mk_2",
        ),
        "Minikit After Access Hatch": minikit_data(
            R_SWAMP_RUINS,
            HasAbility(SHORTIE),
            pickup_name="mk_1",
        ),
        "Minikit In Boarded Up Room": minikit_data(
            R_SWAMP_RUINS,
            logic_options(
                base=True_(),
                # Hard logic can get here with just General Grievous and Droideka.
                hard=HasAnyCharacterExcept(Character.GENERAL_GRIEVOUS),
            ),
            er_rule=logic_options(
                # Force the boards out of the way.
                base=HasAbility(JEDI),
                # The collision on the boards is broken, you can walk through them if you know what you're doing.
                # Droideka/Grievous are too big.
                moderate=HasAnyCharacterExcept(Character.DROIDEKA, Character.GENERAL_GRIEVOUS),
            ),
            pickup_name="mk_0",
        ),
        "Statue Puzzle Minikit": minikit_data(
            R_SWAMP_BEFORE_WATER,
            logic_options(
                base=True_(),
                # Hard can get here with just Grievous/Bodyguard.
                hard=HasAbility(JEDI),
            ),
            er_rule=HasAbility(JEDI),
            pickup_name="m_pup1",
        ),
    },
    power_brick=LocationData(R_CLIFF_FACE_RUINS_PAST_COLLAPSING_DEBRIS, HasAbility(BOUNTY_HUNTER)),
)
