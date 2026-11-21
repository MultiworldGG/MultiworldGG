from rule_builder.rules import True_, And, Or, False_

from ..macros import (
    CAN_DESTROY_CLOSE_SILVER_BRICKS as BASE_CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_SITH_FORCE,
    CAN_DAMAGE_AT_CLOSE_RANGE as BASE_CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
    CAN_YODA_CLIP,
    HAS_0_53_JUMP_HEIGHT_CHARACTER,
)
from ..option_filters import logic_options
from ..rules import HasAbility, HasAnyAbilities, HasAllAbilities, HasAbilityCombination
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...extras import Extra
from ...levels import Level
from ...characters import Character

from ....character_ability import *

R_OUTSIDE_TEMPLE = "Outside Temple"
R_TEMPLE_EXTERIOR_RIGHT_COLLAPSED_COLUMN = "Temple Exterior Right Collapse Column"
R_TEMPLE_ENTRANCE_OVERHANG_LOWER_RIGHT = "Temple Entrance Overhand Lower Right"
R_TEMPLE_ENTRANCE_OVERHANG_TOP = "Temple Entrance Overhand Top"
R_ON_TOP_OF_TEMPLE_DOORS = "On Top Of Temple Doors"
R_INSIDE_TEMPLE_SPAWN = "Inside Temple Spawn"
R_OUTSIDE_CLONE_PIZZA_PARTY_ENTRANCE_THROUGH_TO_COUNCIL_CHAMBER = \
    "Outside Clone Pizza Party Entrance, through to Council Chamber"
R_CLONE_PIZZA_PARTY = "Clone Pizza Party"
R_ARCHIVES = "Archives"
R_HOLOGRAM_ROOM = "Hologram Room"


# Training Remote cannot be given the BLASTER ability because its BLASTER bolts deal no damage, so the automatic Extra
# Toggle rules won't cover this case of CAN_DESTROY_CLOSE_SILVER_BRICKS.
CAN_DESTROY_CLOSE_SILVER_BRICKS = BASE_CAN_DESTROY_CLOSE_SILVER_BRICKS.or_rule(
    # Use the Training Remote, to either Self Destruct, or shoot exploding bolts.
    Extra.has_all(Extra.EXTRA_TOGGLE, Extra.EXPLODING_BLASTER_BOLTS),
    apply_to="normal+",
)


RUIN_OF_THE_JEDI = Chapter(
    area=Area.TEMPLE,
    start_region=R_OUTSIDE_TEMPLE,
    intended_completion_path={
        "base": (
            R_OUTSIDE_TEMPLE,
            R_INSIDE_TEMPLE_SPAWN,
            R_OUTSIDE_CLONE_PIZZA_PARTY_ENTRANCE_THROUGH_TO_COUNCIL_CHAMBER,
            R_ARCHIVES,
            R_HOLOGRAM_ROOM,
        ),
    },
    # There are enemies at the start, so have the base logic expect fighting them.
    extra_entrance_rules=logic_options(
        base=BASE_CAN_DAMAGE_AT_CLOSE_RANGE,
        normal=True_(),
    ),
    regions={
        R_OUTSIDE_TEMPLE: (
            ExitData(
                R_INSIDE_TEMPLE_SPAWN,
                HasAbility(JEDI),
                new_level=Level.TEMPLE_B,
            ),
            ExitData(
                R_TEMPLE_EXTERIOR_RIGHT_COLLAPSED_COLUMN,
                logic_options(
                    base=HasAbility(GRAPPLE),
                    # Allow HIGH_JUMP.
                    # Fairly tight high jump with Jar Jar/Tarpals, but probably okay for Normal logic.
                    normal=HasAnyAbilities(GRAPPLE | HIGH_JUMP),
                    # Allow JEDI (triple jump).
                    moderate=HasAnyAbilities(GRAPPLE | HIGH_JUMP | JEDI),
                )
            ),
            ExitData(
                R_ON_TOP_OF_TEMPLE_DOORS,
                logic_options(
                    base=False_(),
                    # The JEDI option is logically irrelevant because a JEDI can just force the door out of the way.
                    moderate=HasAbility(CAN_HIGH_JUMP_SLAM),
                ),
                er_rule=logic_options(
                    base=False_(),
                    # Triple jump.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM)
                ),
            ),
        ),
        R_TEMPLE_EXTERIOR_RIGHT_COLLAPSED_COLUMN: (
            ExitData(
                R_TEMPLE_ENTRANCE_OVERHANG_LOWER_RIGHT,
                logic_options(
                    strict=False,
                    base=HasAbility(CAN_JUMP_0_44)
                ).or_rule(
                    apply_to="normal+",
                    # Her low gravity and/or high run speed allow her to make the jump without much difficulty.
                    rule=Character.ZAM_WESELL.has()
                ).or_rule(
                    apply_to="moderate+",
                    # Their extra tall collision allows them to make the jump by sliding up.
                    # Jar Jar and Tarpals can also make the jump with their first jump, but they can just high-jump up.
                    rule=Character.has_any(Character.LAMA_SU, Character.TAUN_WE)
                ).or_rule(
                    # Han Solo's dive roll is just barely enough to get up here.
                    apply_to="hard+",
                    rule=Character.has_any(
                        Character.HAN_SOLO,
                        Character.HAN_SOLO_STORMTROOPER,
                        Character.HAN_SOLO_SKIFF,
                        Character.HAN_SOLO_HOOD,
                        Character.HAN_SOLO_HOTH,
                        Character.HAN_SOLO_ENDOR,
                        Character.INDIANA_JONES,
                    ),
                ),
            ),
            ExitData(
                R_ON_TOP_OF_TEMPLE_DOORS,
                logic_options(
                    base=False_(),
                    # There is no reason for Normal logic to go here.
                    # normal=HasAbility(JETPACK),
                    moderate=HasAbility(JETPACK),
                ),
            ),
        ),
        R_TEMPLE_ENTRANCE_OVERHANG_LOWER_RIGHT: (
            ExitData(
                R_TEMPLE_ENTRANCE_OVERHANG_TOP,
                logic_options(
                    base=HasAbility(CAN_DOUBLE_JUMP),
                    # Jetpack hover can jump and then hover against the wall to slowly gain height and get on top.
                    normal=HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                    # See the description for the OR-ed hard logic below. Flop jumps actually get slightly more height
                    # than a dive roll (which doesn't give any height), allowing for Stormtroopers to barely make the
                    # jump on their own-ish, by character swapping before sliding off the edge. Using one flop jumping
                    # stormtrooper to push another flop jumping stormtrooper makes it much easier however, like with
                    # dive rolling characters.
                    hard=HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK | CAN_FLOP_JUMP),
                ).or_rule(
                    apply_to="moderate+",
                    rule=HAS_0_53_JUMP_HEIGHT_CHARACTER,
                ).or_rule(
                    # Luke Skywalker cannot jump up on his own with his 0.44 jump height and dive roll combined,
                    # however, if P2 jumps and dive rolls simultaneously, P2 can push P1 just enough to make it up.
                    # Unlike 1P2C dive rolls intended to greatly increase one player's jump height, like in high level
                    # 6-4 Any% speedruns, this trick is significantly easier. The one thing to watch out for is that
                    # right up against the side of the platform, there is a small bit of ceiling that sticks out, so you
                    # need to jump and dive from slightly away from the side of the platform, or you'll just bonk your
                    # head.
                    # Other 0.44 jump height + dive roll characters area just as easy.
                    apply_to="hard",
                    rule=HasAbilityCombination(CAN_JUMP_0_44, CAN_REGULAR_DIVE_ROLL),
                ),
                # Expert logic should be able to get up here with any two characters with 0.44 jump height or better.
                # The dive roll/flop used in Hard logic is not actually required, but just makes the trick much easier.
                # I did this trick with Lando Calrissian (no dive roll), and Dexter Jettster, which are both 0.44 jump
                # height.
            ),
            ExitData(
                R_ON_TOP_OF_TEMPLE_DOORS,
                # From here, you are close enough to astromech hover over to the top of the doors. Conveniently,
                # astromechs also fit behind the doors.
                logic_options(
                    base=False_(),
                    moderate=HasAbility(HOVER),
                ),
            ),
        ),
        R_TEMPLE_ENTRANCE_OVERHANG_TOP: (),
        R_ON_TOP_OF_TEMPLE_DOORS: (
            ExitData(
                R_INSIDE_TEMPLE_SPAWN,
                logic_options(
                    base=False_(),
                    # Characters with low height fit.
                    moderate=Or(
                        # Ewoks have 0.37 height.
                        # Astromech droids have 0.33 height.
                        HasAnyAbilities(ASTROMECH_DROID | WEAPON_EWOK),
                        # Gamorrean Guard has 0.4 height, and 0.1 radius, and does not fit.
                        Character.has_any(
                            # 0.37 height:
                            Character.BOBA_FETT_BOY,
                            Character.JAWA,
                            Character.UGNAUGHT,
                            # 0.32 height:
                            Character.PIT_DROID,
                            Character.PK_DROID,
                            # 0.3 height:
                            Character.GONK_DROID,
                            # Irrelevant due to being able to use the force to remove the doors.
                            # Character.YODA,
                            # Character.YODA_GHOST,
                        ),
                        # Character.TRAINING_REMOTE fits too.
                        Extra.EXTRA_TOGGLE.has(),
                    ),
                ),
                new_level=Level.TEMPLE_B,
            ),
        ),
        R_INSIDE_TEMPLE_SPAWN: (
            ExitData(
                R_OUTSIDE_CLONE_PIZZA_PARTY_ENTRANCE_THROUGH_TO_COUNCIL_CHAMBER,
                logic_options(
                    base=True_(),
                    # Gamorrean Guard/Super Gonk can get onto the pillar that makes the steps, but ASTROMECH_DROID
                    # barely cannot get enough height to hover across from there, and all JETPACK characters can cross
                    # on their own.
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP | JETPACK | CAN_DOUBLE_JUMP),
                ).or_rule(
                    apply_to="hard+",
                    # Around the back of the pillar on the left, the wall collision does not extend all the way down, so
                    # an Astromech droid can fit beneath the wall collision just as they're about to fall off the
                    # collision of the base of the pillar, and then character swap while under the floor to upwarp to
                    # the floor above.
                    # TRAINING_REMOTE, through EXTRA_TOGGLE can also fit beneath the wall collision, and will then
                    # 'upwarp' on its own.
                    rule=Or(
                        HasAbility(ASTROMECH_DROID),
                        Extra.EXTRA_TOGGLE.has(),
                        # Jawa (0.37 height) seems to be too tall.
                        Character.has_any(
                            Character.PK_DROID,
                            Character.PIT_DROID,
                            Character.EVENT_SUPER_GONK_DROID,
                        )
                    ),
                ),
                er_rule=logic_options(
                    base=HasAbility(JEDI),
                    normal=HasAnyAbilities(JEDI | HIGH_JUMP),
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP | JETPACK | CAN_DOUBLE_JUMP),
                ).or_rule(
                    apply_to="hard+",
                    rule=Or(
                        HasAbility(ASTROMECH_DROID),
                        Extra.EXTRA_TOGGLE.has(),
                        And(
                            HasAbility(CAN_BARELY_JUMP),
                            Character.has_any(
                                Character.PK_DROID,
                                Character.PIT_DROID,
                                Character.EVENT_SUPER_GONK_DROID,
                            ),
                        ),
                    )
                ),
            ),
        ),
        R_OUTSIDE_CLONE_PIZZA_PARTY_ENTRANCE_THROUGH_TO_COUNCIL_CHAMBER: (
            ExitData(
                R_CLONE_PIZZA_PARTY,
                logic_options(
                    base=HasAbility(IMPERIAL),
                    hard=Or(
                        # The platform/overhang above the door has collision. Triple jump onto it, then triple jump over
                        # the wall collision and hit the transition without needing to use the panel. The floor
                        # collision back here is a bit wonky, and you may get stuck sometimes if you miss the
                        # transition after initially getting over the wall.
                        # Instead of taking only two triple jumps, you can instead triple jump to the top of the pillar
                        # directly to the left of the door (its collision does not match its model) and then double jump
                        # over the door.
                        # For Jar Jar/Tarpals, on the far left of this area, stand on the stone fence, high jump onto
                        # the leftmost pillar, high jump onto the next-leftmost pillar, high jump (hover is easier)
                        # across to the pillar directly to the left of the door to R_CLONE_PIZZA_PARTY (its collision is
                        # the same as the previous pillar despite it appearing to be taller), then, finally, high jump
                        # over the wall above the door.
                        HasAnyAbilities(IMPERIAL | JEDI | CAN_HIGH_JUMP_SLAM | HIGH_JUMP),
                    ),
                ),
            ),
            ExitData(
                R_ARCHIVES,
                # I don't think there is any way to skip the JEDI requirement because the transition appears to be
                # inactive otherwise.
                logic_options(
                    base=True_(),
                    moderate=HasAbility(JEDI),
                ),
                er_rule=HasAbility(JEDI),
                new_level=Level.TEMPLE_C,
            ),
        ),
        R_CLONE_PIZZA_PARTY: (),
        R_ARCHIVES: (
            ExitData(
                R_HOLOGRAM_ROOM,
                True_(),
                # Activating all 3 switches on the right only needs a Jedi.
                # There is also a drop-in warp to get behind the arm blocking the door, that hard logic could do.
                # There is also a Grievous Wall Climb to get over the wall and behind the transition, to hit the
                # transition from behind.
                er_rule=HasAbility(JEDI),
            ),
        ),
        R_HOLOGRAM_ROOM: (
            ExitData(
                "Chapter Completion",
                True_(),
                # Force is needed to spin the wheel in the hologram projector.
                er_rule=HasAbility(JEDI),
            ),
        ),
    },
    minikits={
        "Outside Temple Minikit On Ground": minikit_data(
            R_OUTSIDE_TEMPLE,
            pickup_name="mk_0",
        ),
        "Outside Temple High Minikit": minikit_data(
            R_OUTSIDE_TEMPLE,
            logic_options(
                # Force the platforms, then high jump up.
                base=HasAllAbilities(JEDI | HIGH_JUMP),
                # Double Jump + Slam reaches the minikit from on top of the platforms.
                normal=HasAbility(JEDI),
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="mk_1",
        ),
        "Minikit Above Temple Entrance": minikit_data(
            R_TEMPLE_ENTRANCE_OVERHANG_TOP,
            logic_options(
                base=HasAllAbilities(BOUNTY_HUNTER | SITH),
                normal=CAN_DESTROY_CLOSE_SILVER_BRICKS & CAN_SITH_FORCE,
            ),
            # Sith force, then explode the silver bricks, then finally build the bricks to make the minikit.
            er_rule=CAN_DESTROY_CLOSE_SILVER_BRICKS & CAN_SITH_FORCE & HasAbility(CAN_BUILD_BRICKS),
            pickup_name="m_pup1",
        ),
        "Pizza Party Minikit": minikit_data(
            R_CLONE_PIZZA_PARTY,
            True_(),
            er_rule=HasAbility(CAN_BARELY_JUMP),
            pickup_name="mk_2",
        ),
        "Council Chamber Minikit": minikit_data(
            R_OUTSIDE_CLONE_PIZZA_PARTY_ENTRANCE_THROUGH_TO_COUNCIL_CHAMBER,
            # Stack the chairs and then double jump up to the minikit.
            logic_options(
                base=True_(),
                moderate=HasAbility(JEDI),
            ).or_rule(
                # Triple high jump from the arm of the front left chair.
                apply_to="hard+",
                rule=Character.GENERAL_GRIEVOUS.has() & Extra.STUD_MAGNET.has(),
            ),
            er_rule=HasAbility(JEDI),
            pickup_name="mk_1",
        ),
        "Minikit Floating Near Council Chamber": minikit_data(
            R_OUTSIDE_CLONE_PIZZA_PARTY_ENTRANCE_THROUGH_TO_COUNCIL_CHAMBER,
            logic_options(
                base=HasAbility(HOVER),
                # Normal: JEDI required to reach here.
                # Moderate: JEDI/HIGH_JUMP/JETPACK/CAN_DOUBLE_JUMP required to reach here.
                normal=True_(),
                hard=CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
            ),
            er_rule=logic_options(
                # Expect hovering to get the minikit and come back without dying.
                base=HasAbility(HOVER),
                # Jump to the minikit and then die.
                # Cannot get it:
                # - Clone (jump_distance=0.7)
                # I tried the 1P2C strategy of being shot to get extra distance + Stud Magnet, but still could not reach
                # it with Clone.
                # Can get it:
                # - Dexter Jettstar (jump_distance=0.77)
                # - Han Solo (jmup_distance=0.84)
                # - Captain Tarpals (single jump) (jump_distance=0.9051)
                normal=CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
            ),
            pickup_name="mk_0",
        ),
        "Archives Right Side Right Lever Minikit": minikit_data(
            R_ARCHIVES,
            logic_options(
                base=HasAbility(HIGH_JUMP),
                moderate=True_(),
            ),
            er_rule=logic_options(
                base=HasAllAbilities(JEDI | HIGH_JUMP),
                moderate=HasAbility(JEDI)
            ),
            pickup_name="mk_1",
        ),
        "Archives Right Side Left Lever Minikit": minikit_data(
            R_ARCHIVES,
            True_(),
            er_rule=HasAbility(JEDI),
            pickup_name="mk_0"
        ),
        "Archives Left Side Behind Force Field Minikit": minikit_data(
            R_ARCHIVES,
            logic_options(
                base=HasAllAbilities(HIGH_JUMP | PROTOCOL_PANEL),
                normal=HasAbility(HIGH_JUMP),
                moderate=True_(),
            ),
            er_rule=logic_options(
                # Force the 3 right levers as a jedi, high jump up onto the arm that now forms a platform.
                # Expect PROTOCOL_PANEL so that the level can be continued without restarting.
                base=HasAllAbilities(JEDI | HIGH_JUMP | PROTOCOL_PANEL),
                # Force out a platform and high jump from it to get over the force field.
                # Grievous' Bodyguard can just get enough horizontal distance to clear the force field, though normal
                # logic could be expected to just restart the level for this minikit.
                normal=HasAllAbilities(JEDI | HIGH_JUMP),
                # Triple jump can skip high jumps (and can also skip forcing the levers on the right side of the room by
                # triple jumping up to the lowest platform area).
                # Triple high jump can similarly jump straight up, or even straight over the forcefield.
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="mk_2"
        ),
        "Hologram Room Minikit": minikit_data(
            R_HOLOGRAM_ROOM,
            logic_options(
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS & CAN_SITH_FORCE,
                normal=And(
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    HasAbility(SITH) | Extra.DARK_SIDE.has(),
                ),
                hard=Or(
                    And(
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        HasAbility(SITH) | Extra.DARK_SIDE.has(),
                    ),
                    CAN_YODA_CLIP,
                ),
            ),
            er_rule=logic_options(
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS & CAN_SITH_FORCE,
                hard=Or(
                    CAN_DESTROY_CLOSE_SILVER_BRICKS & CAN_SITH_FORCE,
                    # Clip through the ceiling in front of the minikit, then go to the left to drop down to where the
                    # minikit is.
                    # It seems that if you swap from General Grievous to a Yoda while pressed against the force field,
                    # you can also grab the minikit that way, through the force field, though you can Yoda Clip with
                    # that combination anyway.
                    # Clipping back out and finishing the chapter can be a pain, I'm unsure if it's possible with every
                    # character.
                    # Yoda can get through the entire level on his own, so it is necessary to check that the player has
                    # some character other than having both Yoda and Yoda (Ghost).
                    CAN_YODA_CLIP,
                ),
            ),
            pickup_name="m_pup1",
        )
    },
    power_brick=LocationData(
        R_ARCHIVES,
        logic_options(
            base=HasAllAbilities(HIGH_JUMP | PROTOCOL_PANEL),
            normal=HasAbility(HIGH_JUMP),
            moderate=True_(),
        ),
        er_rule=logic_options(
            # While there is a Grapple point for the left side, middle lever, there are force platforms that can be high
            # jumped up to, and the button to remove the force field in front of the level requires high jump anyway.
            base=HasAllAbilities(JEDI | HIGH_JUMP | PROTOCOL_PANEL),
            normal=And(
                # High jump is expected to get to all 3 levers, and to reach the Power Brick.
                HasAllAbilities(JEDI | HIGH_JUMP),
                # Allow hovering out, or high jumping out instead.
                HasAnyAbilities(PROTOCOL_PANEL | HOVER | HIGH_JUMP),
            ),
            moderate=Or(
                # Just triple jump out, and triple jump up to the Power Brick.
                HasAbility(JEDI),
                # Triple high jump can skip the entire sequence and jump to the Power Brick directly.
                HasAbility(CAN_HIGH_JUMP_SLAM),
            )
        ),
    ),
)
