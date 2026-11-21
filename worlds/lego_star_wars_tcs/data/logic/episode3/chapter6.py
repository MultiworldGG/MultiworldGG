from rule_builder.rules import True_, And, Or, False_, Rule

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE_NO_SELF_DESTRUCT,
    CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
    HAS_ANY_YODA,
    HAS_P2_AI_DOUBLE_JUMP,
)
from ..option_filters import logic_options
from ..rules import (
    HasAbility,
    HasAnyAbilities,
    HasAbilityCombination,
    HasAbilityExceptCharacters,
    HasAnyCharacterExcept,
)
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

NAME = "Darth Vader"

R_COLLAPSING_LAVA_HALLWAY = "Collapsing Lava Hallway"
R_END_OF_COLLAPSING_LAVA_HALLWAY = "End Of Collapsing Lava Hallway"
R_TIMED_ROOM = "Timed Room"
R_POWER_BRICK_CONFERENCE_ROOM = "Power Brick Conference Room"
R_COLLAPSING_EXTERIOR_SPAWN = "Collapsing Exterior Spawn"
R_COLLAPSING_EXTERIOR_REVOLVING_PLATFORM = "Collapsing Exterior Revolving Platform"
R_COLLAPSING_EXTERIOR_AFTER_REVOLVING_PLATFORM = "Collapsing Exterior After Revolving Platform"
R_COLLAPSING_EXTERIOR_END = "Collapsing Exterior End"
R_LAVA_PLATFORMING_START = "Lava Platforming Start"
R_LAVA_PLATFORMING_SINKING_PLATFORMS_SECTION = "Lava Platforming Sinking Platforms Section"
R_LAVA_PLATFORMING_FINAL_PLATFORM_VERSUS_OTHER_PLAYER = "Lava Platforming Final Platform Versus Other Player"
R_LAVA_PLATFORMING_FAR_MINIKIT_PLATFORM = "Lava Platforming Far Minikit Platform"

ANY_DOUBLE_JUMP_EXCEPT_YODA_AND_ACKBAR = HasAnyAbilities(CAN_TRIPLE_JUMP_GREAT_DISTANCE | HIGH_JUMP)
# More expensive and makes fewer assumptions but should be identical.
ANY_DOUBLE_JUMP_EXCEPT_YODA_AND_ACKBAR_ER = HasAbilityExceptCharacters(
    CAN_DOUBLE_JUMP, Character.YODA, Character.YODA_GHOST, Character.ADMIRAL_ACKBAR)


DARTH_VADER = Chapter(
    area=Area.VADER,
    start_region=R_COLLAPSING_LAVA_HALLWAY,
    regions={
        R_COLLAPSING_LAVA_HALLWAY: (
            ExitData(
                R_END_OF_COLLAPSING_LAVA_HALLWAY,
                logic_options(
                    base=ANY_DOUBLE_JUMP_EXCEPT_YODA_AND_ACKBAR,
                    # Optimised out the RUN_SPEED_1_18_OR_HIGHER because all characters that have jump_distance>=0.84
                    # also have run_speed>=1.20.
                    hard=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER | CAN_JUMP_DISTANCE_0_84),
                ),
                er_rule=logic_options(
                    # Expect any character that can double jump.
                    # The AI will happily make it to the end with any double jump character, except "Yoda" and
                    # "Yoda (Ghost)" who the AI will walk with their lightsaber stowed and die over and over, and except
                    # "Admiral Ackbar" because the game only considers JEDI/HIGH_JUMP characters.
                    base=ANY_DOUBLE_JUMP_EXCEPT_YODA_AND_ACKBAR_ER,
                    # Normal and moderate continue expecting double jump characters, except Yodas, so that P2's AI
                    # doesn't die.
                    #
                    # This is a rather input intensive 1P2C section, so Hard logic expects being able to hold the 'down'
                    # movement key/stick the entire time, and jump across any gaps found.
                    # Boba Fett: run_speed=1.2 and jump_distance=0.92 was doable for me, without hovering.
                    # Han Solo: run_speed=1.2 and jump_distance=0.84 was doable for me, without with performing rolls.
                    # Lando: run_speed=1.18 and jump_distance=0.941 was doable for me, without performing rolls.
                    # Dexter Jettstar: run_speed=1.0 and jump_distance=0.7666 might be barely doable, but I gave up.
                    #  It might be possible for Dexter because his increase jump distance from having higher jump height
                    #  might be able to save him in the case that his lower run_speed has caused a platform below him to
                    #  start to collapse.
                    #  When controlling a single Dexter and allowing P2's AI to control a double jumper, I have managed
                    #  to clear this section with Dexter, but I needed to cross over to the left side towards the end
                    #  where the pathway collapses later on the left side.
                    #  Other run_speed=1.0 characters have much lower jump_distance, so might not be able to make it.
                    # Astromech Droids: run_speed=1.0, can just barely make it by hovering over gaps and hovering a lot
                    # towards the end.
                    hard=Or(
                        HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                        HasAbilityCombination(RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_DISTANCE_0_84),
                    ),
                    # expert=Or(
                    #     HasAnyAbilities(CAN_DOUBLE_JUMP | ASTROMECH_DROID),
                    #     # todo: I don't know if this is good enough.
                    #     HasAbilityCombination(RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_DISTANCE_0_84),
                    # )
                ),
            ),
        ),
        R_END_OF_COLLAPSING_LAVA_HALLWAY: (
            ExitData(R_TIMED_ROOM),
        ),
        R_TIMED_ROOM: (
            ExitData(
                R_POWER_BRICK_CONFERENCE_ROOM,
                HasAbility(ASTROMECH_PANEL),
            ),
            ExitData(
                R_COLLAPSING_EXTERIOR_SPAWN,
                HasAbility(JEDI),
                new_level=Level.VADER_B,
            ),
        ),
        R_POWER_BRICK_CONFERENCE_ROOM: (),
        R_COLLAPSING_EXTERIOR_SPAWN: (
            ExitData(
                R_COLLAPSING_EXTERIOR_REVOLVING_PLATFORM,
                # Jedi is needed to reach here.
                True_(),
                er_rule=logic_options(
                    base=And(
                        # Destroy the objects and step on the buttons.
                        CAN_DAMAGE_AT_CLOSE_RANGE_NO_SELF_DESTRUCT & HasAbility(CAN_BARELY_JUMP),
                    ),
                    # Respawning is disabled in this section, instead, dying restarts the section, so Self Destruct
                    # cannot be used in this section to destroy the objects.
                    moderate=Or(
                        CAN_DAMAGE_AT_CLOSE_RANGE_NO_SELF_DESTRUCT & HasAbility(CAN_BARELY_JUMP),
                        Character.DROIDEKA.has(),
                    ),
                ),
            ),
            ExitData(
                R_COLLAPSING_EXTERIOR_AFTER_REVOLVING_PLATFORM,
                # Logically irrelevant since a Jedi is required to reach here.
                False_(),
                er_rule=logic_options(
                    base=False_(),
                    # Hover around it. This is not in Normal logic  because the collision box of the revolving platform
                    # sticks out way further than you would think.
                    moderate=HasAbility(HOVER)
                ),
            ),
            ExitData(
                R_COLLAPSING_EXTERIOR_END,
                # Logically irrelevant since a Jedi is required to reach here.
                False_(),
                er_rule=logic_options(
                    # Moderate+ only.
                    base=False_(),
                    # Triple jump on top of the overhang above the normal area, then walk past all the obstacles and
                    # drop down at the end.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
        ),
        R_COLLAPSING_EXTERIOR_REVOLVING_PLATFORM: (
            ExitData(
                R_COLLAPSING_EXTERIOR_AFTER_REVOLVING_PLATFORM,
                # Jedi is needed to reach here.
                True_(),
                er_rule=logic_options(
                    # To progress after the revolving platform, P2's AI needs a character it can double jump with.
                    base=HAS_P2_AI_DOUBLE_JUMP,
                    # Move both characters individually if no double jump character is unlocked.
                    moderate=True_(),
                ),
            ),
        ),
        R_COLLAPSING_EXTERIOR_AFTER_REVOLVING_PLATFORM: (
            ExitData(
                R_COLLAPSING_EXTERIOR_END,
                # Jedi is needed to reach here.
                True_(),
                # todo: The DROID and GAS_IMMUNE abilities are not implemented currently because they are not currently
                #  needed.
                # er_rule=logic_options(
                #     # P2's AI will only pass the 'gas' as a droid, and not force ghosts.
                #     base=HasAnyAbilities(JEDI | DROID),
                #     # Pass the 'gas' by moving P2 yourself if necessary.
                #     # Hover around the 'gas'. It's collision box is larger than it might appear, so this is not in
                #     # Normal logic.
                #     moderate=HasAnyAbilities(JEDI | GAS_IMMUNE | HOVER),
                # )
            ),
        ),
        R_COLLAPSING_EXTERIOR_END: (
            ExitData(
                R_LAVA_PLATFORMING_START,
                True_(),
                # Strictly required, otherwise the trigger to load the next level does not happen.
                er_rule=HasAbility(JEDI),
                new_level=Level.VADER_C,
            ),
        ),
        R_LAVA_PLATFORMING_START: (
            ExitData(
                R_LAVA_PLATFORMING_SINKING_PLATFORMS_SECTION,
                True_(),
                er_rule=HasAbility(CAN_BARELY_JUMP),
            ),
        ),
        R_LAVA_PLATFORMING_SINKING_PLATFORMS_SECTION: (
            ExitData(
                R_LAVA_PLATFORMING_FINAL_PLATFORM_VERSUS_OTHER_PLAYER,
                True_(),
                # The jump from the last platform to the tower is quite high.
                # todo: Maybe Gamorrean guard can make this jump?
                er_rule=HasAbility(CAN_DOUBLE_JUMP),
            ),
            ExitData(
                R_LAVA_PLATFORMING_FAR_MINIKIT_PLATFORM,
                # Not logically relevant because getting to R_LAVA_PLATFORMING_FAR_MINIKIT_PLATFORM from the final
                # area is easier (can use HOVER instead of JETPACK), and the final area is always accessible because a
                # Jedi is needed to reach the start of the Lava Platforming.
                False_(),
                er_rule=logic_options(
                    # It's too far and requires an increase in height, so Astromech Hover is out.
                    base=False_(),
                    normal=HasAbility(JETPACK),
                    # Yoda cannot make the distance, but Grievous' Bodygaurd can.
                    moderate=HasAnyAbilities(JETPACK | CAN_HIGH_JUMP_SLAM | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                ),
            ),
        ),
        R_LAVA_PLATFORMING_FINAL_PLATFORM_VERSUS_OTHER_PLAYER: (
            ExitData(
                "Chapter Completion",
                # A Jedi is needed to reach this point and the AI exclusively swaps to Jedi, but Ghost Jedi are
                # invincible, so a non-ghost Jedi is needed.
                # Additionally, P2's AI seems to break here when P2 is a Ghost, refusing to attack for some reason.
                # Even if P2's AI did work, allowing AI P2 to kill you forces the fight to restart.
                logic_options(
                    strict=False,
                    base=HasAbility(IS_NON_GHOST_JEDI),
                ).or_rule(
                    apply_to="moderate+",
                    # Jedi is required to reach here, so if the only Jedi the player has are Force Ghosts, then they
                    # will need to drop in as P2 to a character that is not invincible (any non-Force Ghost).
                    rule=HasAnyCharacterExcept(Character.YODA_GHOST,
                                               Character.ANAKIN_SKYWALKER_GHOST,
                                               Character.BEN_KENOBI_GHOST),
                )
                # Having no Jedi unlocked at all would send the AI into an infinite character swapping loop, which might
                # prevent dealing damage to them. Either way, this sort of logic is not allowed in AP because going from
                # not having a Jedi unlocked, to having a Ghost Jedi unlocked, would cause this entrance to go from
                # in-logic to out-of-logic.
                # todo: The DROID ability is not currently implemented because it is not logically needed.
                # er_rule=logic_options(
                #     base=HasAbility(IS_NON_GHOST_JEDI)
                #     # Instead of instantly killing the character, when Super Zapper damages a player character, it
                #     # deals 1 heart of damage, so that can be used to deal damage too.
                #     # Self Destruct is not usable here because any respawn not directly caused by a player controlled
                #     # character results in restarting the fight.
                #     moderate=Or(
                #         HasAbility(IS_NON_GHOST_JEDI),
                #         # With no Jedi unlocked, or with only ghost Jedi unlocked, control both P1 and P2
                #         # independently to complete the chapter.
                #         HasAbility(CAN_DAMAGE_AT_CLOSE_RANGE) & ANY_CHARACTER_EXCEPT_FORCE_GHOST,
                #         # Gas-immune non-ghosts covers all droids.
                #         # todo: Check that Grievous' Bodyguard is damaged/killed by Super Zapper.
                #         Extra.SUPER_ZAPPER.has() & HasAbility(WEAPON_ZAPPER) & HAS_GAS_IMMUNE_EXCEPT_GHOSTS,
                #     ),
                # ),
            ),
            ExitData(
                R_LAVA_PLATFORMING_FAR_MINIKIT_PLATFORM,
                logic_options(
                    base=HasAbility(HOVER),
                    normal=Or(
                        HasAbility(HOVER),
                        HAS_ANY_YODA,
                        # Write out the HasAny to help confirm in logic tests that HasAbilityExceptCharacters is working
                        # as expected. Rule Builder will automatically combine the two HasAny within the Or.
                        Character.has_any(
                            Character.JAR_JAR_BINKS,
                            Character.CAPTAIN_TARPALS,
                            Character.GENERAL_GRIEVOUS,
                            Character.ADMIRAL_ACKBAR,
                        ),
                    ),
                    # A Jedi is required to reach here.
                    moderate=True_()
                ),
                er_rule=logic_options(
                    base=HasAbility(HOVER),
                    normal=Or(
                        HasAbility(HOVER),
                        # Yoda and Ackbar can make the jump due to their increased double jump distance.
                        # High jumpers, except Grievous' Bodyguard can also make the jump.
                        HAS_ANY_YODA,
                        Character.ADMIRAL_ACKBAR.has(),
                        HasAbilityExceptCharacters(HIGH_JUMP, Character.GRIEVOUS_BODYGUARD),
                    ),
                    # All double jump characters can jump the required distance, either with a regular double jump, or
                    # with a triple jump.
                    moderate=HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP),
                ),
            ),
        ),
        R_LAVA_PLATFORMING_FAR_MINIKIT_PLATFORM: (),
    },
    minikits={
        "Collapsing Hallway Minikit": minikit_data(
            R_END_OF_COLLAPSING_LAVA_HALLWAY,
            pickup_name="mk_0",
        ),
        "Timed Room Left Screen Minikit": minikit_data(
            R_TIMED_ROOM,
            HasAbility(JEDI),
            pickup_name="m_pup1",
        ),
        "Timed Room Far Minikit": minikit_data(
            R_TIMED_ROOM,
            pickup_name="mk_2",
        ),
        "Timed Room Sealed Minikit": minikit_data(
            R_TIMED_ROOM,
            # TODO: Check is Self Destruct is allowed here (I suspect not)
            # Non-combo type attacks work fine here.
            CAN_DAMAGE_AT_CLOSE_RANGE_NO_SELF_DESTRUCT,
            er_rule=CAN_DAMAGE_AT_CLOSE_RANGE_NO_SELF_DESTRUCT & HasAbility(CAN_BARELY_JUMP),
            pickup_name="mk_3",
        ),
        "Timed Room Grate Minikit": minikit_data(
            R_TIMED_ROOM,
            logic_options(
                base=HasAbility(JEDI),
                # A character that can jump, even if just barely, is required to reach here, so
                # HasAbility(CAN_BARELY_JUMP) can be optimised away.
                moderate=Or(
                    HasAbility(JEDI),
                    Extra.STUD_MAGNET.has(),
                )
            ),
            er_rule=logic_options(
                base=HasAbility(JEDI),
                # Moderate: Most (all?) characters can grab this through the grate if Stud Magnet is active.
                # Yoda can also grab this through the grate without Stud Magnet. I got it just by using a
                # single-jump-attack, but Jedi can just get the minikit normally, so this is logically pointless.
                moderate=Or(
                    HasAbility(JEDI),
                    Extra.STUD_MAGNET.has() & HasAbility(CAN_BARELY_JUMP),
                )
            ),
            pickup_name="mk_1",
        ),
        "Collapsing Exterior Spawn Minikit": minikit_data(
            R_COLLAPSING_EXTERIOR_SPAWN,
            pickup_name="mk_0",
        ),
        "Collapsing Exterior Revolving Platform Minikit": minikit_data(
            R_COLLAPSING_EXTERIOR_REVOLVING_PLATFORM,
            pickup_name="mk_1",
        ),
        "Lava Platforming Right Minikit": minikit_data(
            R_LAVA_PLATFORMING_SINKING_PLATFORMS_SECTION,
            True_(),
            er_rule=logic_options(
                base=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                # It's not too difficult with Han Solo (jump_distance=0.84)
                normal=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER | CAN_JUMP_DISTANCE_0_84),
                # Dexter Jettstar is a bit more difficult, and Ewok/Clone seems impossible, getting no further than the
                # first platform.
                moderate=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER) | CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
            ),
            pickup_name="mk_0",
        ),
        "Lava Platforming Left Minikit": minikit_data(
            R_LAVA_PLATFORMING_SINKING_PLATFORMS_SECTION,
            True_(),
            er_rule=logic_options(
                base=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                # It's not too difficult with Han Solo (jump_distance=0.84)
                normal=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER | CAN_JUMP_DISTANCE_0_84),
                # Dexter Jettstar is a bit more difficult, and Ewok/Clone seems impossible, getting no further than the
                # first platform.
                moderate=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER) | CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
            ),
            pickup_name="mk_2",
        ),
        "Lava Platforming Isolated Minikit": minikit_data(
            R_LAVA_PLATFORMING_FAR_MINIKIT_PLATFORM,
            pickup_name="mk_1",
        ),
    },
    power_brick=LocationData(
        R_POWER_BRICK_CONFERENCE_ROOM,
        True_(),
        er_rule=HasAbility(CAN_BARELY_JUMP),
    )
)
