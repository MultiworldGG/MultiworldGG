from rule_builder.rules import And, Or, True_, False_

from ..macros import (
    CAN_SITH_FORCE,
    CAN_USE_DEFLECT_BOLTS,
    CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
    CAN_USE_SELF_DESTRUCT,
    CAN_YODA_CLIP,
    CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
    CAN_GRAPPLE,
    HAS_ANY_YODA,
    HAS_P2_AI_DOUBLE_JUMP,
)
from ..option_filters import logic_options
from ..rules import HasAbility, HasAllAbilities, HasAnyAbilities, HasAnyCharacterExcept, HasAbilityExceptCharacters
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_LANDING_PAD = "Landing Pad"
R_SPAWN_FLOATING_MINIKIT_PLATFORM = "Spawn Floating Minikit Platform"
R_CLONE_VIEWING_AREA = "Clone Viewing Area"
R_BOUNTY_HUNTER_AREA = "Bounty Hunter Area"
R_LIVING_QUARTERS = "Living Quarters"
R_LIVING_QUARTERS_BEHIND_FORCE_FIELD = "Living Quarters Behind Force Field"
R_OUTSIDE_JANGO_CHASE = "Outside Jango Chase"
R_START_OF_OUTSIDE_JANGO_CHASE_MINIKIT_PLATFORM = "Start Of Outside Jango Chase Minikit Platform"
R_END_OF_OUTSIDE_JANGO_CHASE = "End Of Outside Jango Chase"
R_END_OF_OUTSIDE_JANGO_CHASE_UPPER_SECTION = "End Of Outside Jango Chase Upper Section"
R_INTERIOR_BEFORE_JANGO_FIGHT = "Interior Before Jango Fight"
R_SITH_FORCE_DROID_ROOM = "Sith Force Droid Room"
R_JANGO_FIGHT = "Jango Fight"

_CAN_YODA_GRAB_BLASTER_TARGETS_REWARD_MINIKIT = And(
    HAS_ANY_YODA,
    Or(
        HasAbilityExceptCharacters(
            JEDI,
            Character.YODA,
            Character.YODA_GHOST,
            # Luke cannot Yoda Grab.
            Character.LUKE_SKYWALKER_DAGOBAH,
            Character.LUKE_SKYWALKER_BESPIN,
            Character.LUKE_SKYWALKER_JEDI,
            Character.LUKE_SKYWALKER_ENDOR,
        ),
        Character.has_any(
            Character.GENERAL_GRIEVOUS,
            Character.CAPTAIN_TARPALS,
            Character.IMPERIAL_GUARD,
            # Dive roll into the window, and near the very start of the dive roll, swap to Yoda.
            Character.ADMIRAL_ACKBAR,
        ),
    ),
)

# By swapping to a character with higher air speed after triple jumping, it is possible to triple jump across some gaps
# as Yoda/Yoda (Ghost).
# Geonosian and Watto only have high movement speed while fluttering, their default movement  speed (which corresponds
# to their air speed after swapping to them in this case), is very slow.
# The next slowest characters are as fast as C-3PO.
# Since this accepts basically any character, I am allowing this in Moderate logic, whereas usually Hard logic is
# required when a specific Free Play Roster arrangement is required.
_HAS_CHARACTER_THAT_ALLOWS_YODA_TO_TRIPLE_JUMP_GREAT_DISTANCE = logic_options(
    base=False_(),
    moderate=HasAbilityExceptCharacters(
        RUN_SPEED_0_9_OR_HIGHER,
        Character.YODA,
        Character.YODA_GHOST,
        Character.GEONOSIAN,
        Character.WATTO,
    ),
    hard=HasAnyCharacterExcept(
        Character.YODA,
        Character.YODA_GHOST,
        Character.GEONOSIAN,
        Character.WATTO,
    ),
)

DISCOVERY_ON_KAMINO = Chapter(
    area=Area.KAMINO,
    start_region=R_LANDING_PAD,
    intended_completion_path={
        "base": (
            R_CLONE_VIEWING_AREA,
            R_LIVING_QUARTERS,
            R_LIVING_QUARTERS_BEHIND_FORCE_FIELD,
            R_OUTSIDE_JANGO_CHASE,
            R_END_OF_OUTSIDE_JANGO_CHASE,
            R_INTERIOR_BEFORE_JANGO_FIGHT,
            R_JANGO_FIGHT,
        ),
    },
    regions={
        R_LANDING_PAD: (
            ExitData(
                R_SPAWN_FLOATING_MINIKIT_PLATFORM,
                logic_options(
                    base=HasAbility(HOVER),
                    # Triple jump across the gap.
                    moderate=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                    # Allow Bodyguard.
                    hard=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM),
                ).or_rule(
                    apply_to="moderate+",
                    rule=And(
                        HasAbility(JEDI),
                        _HAS_CHARACTER_THAT_ALLOWS_YODA_TO_TRIPLE_JUMP_GREAT_DISTANCE,
                    ),
                ),
            ),
            ExitData(
                R_CLONE_VIEWING_AREA,
                # Force to fix the pylon thing and extend the bridge.
                HasAbility(JEDI),
                # Yes, the levels are out-of-order, and kamino_b does not exist.
                new_level=Level.KAMINO_D,
            ),
        ),
        R_SPAWN_FLOATING_MINIKIT_PLATFORM: (
            ExitData(
                R_CLONE_VIEWING_AREA,
                logic_options(
                    base=False_(),
                    # Hover to near the minikit, then hover to the building entrance.
                    # There is a 'fall plane' on the left of the building entrance, which also extends slightly
                    # outwards, so the final part of the hover needs to approach the entrance platform from the front.
                    # Also allow General Grievous' triple high jump distance from the same starting point near the
                    # minikit.
                    hard=HasAbility(JETPACK) | Character.GENERAL_GRIEVOUS.has(),
                    # Expert I believe can even cross with Astromech Hover (see the any% speedrun guide for 2-2).
                ),
                new_level=Level.KAMINO_D,
            ),
        ),
        R_CLONE_VIEWING_AREA: (
            ExitData(
                R_BOUNTY_HUNTER_AREA,
                logic_options(
                    base=HasAllAbilities(JEDI | BOUNTY_HUNTER),
                    # Ceiling clip to get on the other side of the door.
                    hard=HasAllAbilities(JEDI | BOUNTY_HUNTER) | CAN_YODA_CLIP,
                ),
            ),
            ExitData(
                R_LIVING_QUARTERS,
                # Notably, clipping past the door does not allow you to enter kamino_c, the trigger does not load until
                # the astromech panel has been used.
                HasAllAbilities(JEDI | ASTROMECH_PANEL),
                new_level=Level.KAMINO_C,
            ),
        ),
        R_BOUNTY_HUNTER_AREA: (),
        # I can't seem to get Drop Xin Warp to work.
        R_LIVING_QUARTERS: (
            ExitData(
                R_LIVING_QUARTERS_BEHIND_FORCE_FIELD,
                logic_options(
                    # Meet Jango, then destroy the robots to leave the room and the two ceiling turrets to lower the
                    # force field.
                    base=HasAnyAbilities(IS_NON_GHOST_JEDI | BLASTER),
                    # Standing close to the robots and turrets can cause deflected bolts to destroy them.
                    # Super Zapper can destroy the robots, but cannot destroy the turrets.
                    moderate=Or(
                        HasAnyAbilities(IS_NON_GHOST_JEDI | BLASTER),
                        CAN_USE_DEFLECT_BOLTS,
                    ),
                ).or_rule(
                    # Yoda Clip from the first room to the second. This is only relevant for Yoda (Ghost).
                    # An ASTROMECH_PANEL character is strictly required to reach here, so there is no need to check for
                    # having any non-Yoda character unlocked.
                    # Since Hard logic never expects running around beneath the level, if you don't have a character to
                    # swap to that can actually make the jump to the second room, if you build the mosaic, it gains
                    # floor collision on top, just outside the room's wall, so you can Yoda Clip onto the top of the
                    # mosaic, and then double jump across to the second room with Yoda.
                    apply_to="hard+",
                    # rule=CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                    rule=Character.YODA_GHOST.has(),
                ),
            ),
        ),
        R_LIVING_QUARTERS_BEHIND_FORCE_FIELD: (
            # The levels are out-of-order again.
            ExitData(R_OUTSIDE_JANGO_CHASE, new_level=Level.KAMINO_F),
        ),
        R_OUTSIDE_JANGO_CHASE: (
            ExitData(
                R_START_OF_OUTSIDE_JANGO_CHASE_MINIKIT_PLATFORM,
                logic_options(
                    base=HasAbility(HOVER),
                    # JEDI is required to reach here.
                    moderate=Or(
                        HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM),
                        # You can make the jump even with a swap to C-3PO. Because there are so many possible characters
                        # this is allowed on Moderate logic.
                        _HAS_CHARACTER_THAT_ALLOWS_YODA_TO_TRIPLE_JUMP_GREAT_DISTANCE
                    ),
                ),
                er_rule=logic_options(
                    # Hover across to the platform.
                    base=HasAbility(HOVER),
                    # Or triple jump across to the platform.
                    # Yodas can only triple jump across so long as you have a character with decent movement speed to
                    # swap to.
                    moderate=Or(
                        HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM),
                        And(
                            HasAbility(JEDI),
                            _HAS_CHARACTER_THAT_ALLOWS_YODA_TO_TRIPLE_JUMP_GREAT_DISTANCE,
                        ),
                    )
                ),
            ),
            ExitData(
                R_END_OF_OUTSIDE_JANGO_CHASE,
                # JEDI is required to reach here.
                # HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
            ),
        ),
        R_START_OF_OUTSIDE_JANGO_CHASE_MINIKIT_PLATFORM: (),
        R_END_OF_OUTSIDE_JANGO_CHASE: (
            ExitData(
                R_END_OF_OUTSIDE_JANGO_CHASE_UPPER_SECTION,
                logic_options(
                    base=HasAbility(GRAPPLE),
                    # JEDI is required to reach here, so optimize out the JEDI from CAN_GRAPPLE.
                    normal=HasAbility(GRAPPLE) | Extra.FORCE_GRAPPLE_LEAP.has(),
                    # JEDI triple jump is enough to get up here by jumping from the fence, and JEDI is required to reach
                    # here.
                    moderate=True_(),
                ),
                er_rule=logic_options(
                    base=CAN_GRAPPLE,
                    moderate=CAN_GRAPPLE | HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
            ExitData(
                R_INTERIOR_BEFORE_JANGO_FIGHT,
                # JEDI and ASTROMECH_PANEL are required to reach here.
                logic_options(
                    base=HasAbility(HOVER),
                    moderate=Or(
                        HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                        _HAS_CHARACTER_THAT_ALLOWS_YODA_TO_TRIPLE_JUMP_GREAT_DISTANCE,
                    ),
                ),
                er_rule=logic_options(
                    base=HasAllAbilities(JEDI | HOVER | ASTROMECH_PANEL),
                    moderate=And(
                        # Cross the gap.
                        Or(
                            HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                            And(
                                HAS_ANY_YODA,
                                _HAS_CHARACTER_THAT_ALLOWS_YODA_TO_TRIPLE_JUMP_GREAT_DISTANCE,
                            ),
                        ),
                        # Use the panel to open the elevator door.
                        HasAllAbilities(JEDI | ASTROMECH_PANEL),
                    ),
                    hard=And(
                        # Cross the gap.
                        Or(
                            HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                            And(
                                HAS_ANY_YODA,
                                _HAS_CHARACTER_THAT_ALLOWS_YODA_TO_TRIPLE_JUMP_GREAT_DISTANCE,
                            ),
                        ),
                        # Use the panel, or ceiling clip with Yoda from where the studs are above the elevator door.
                        Or(
                            HasAllAbilities(JEDI | ASTROMECH_PANEL),
                            CAN_YODA_CLIP,
                        ),
                        # todo?: Drop in warp: https://youtu.be/W66qxVkOaPA?t=1768, I couldn't get it to work in Free
                        #  Play, but maybe I'm doing it wrong.
                    ),
                ),
                new_level=Level.KAMINO_E,
            ),
        ),
        R_END_OF_OUTSIDE_JANGO_CHASE_UPPER_SECTION: (),
        R_INTERIOR_BEFORE_JANGO_FIGHT: (
            # Force the bricks out of the way, use the panel and then defeat Jango Fett.
            ExitData(
                R_JANGO_FIGHT,
                # JEDI and ASTROMECH_PANEL are required to reach here.
                True_(),
                er_rule=logic_options(
                    base=HasAllAbilities(JEDI | ASTROMECH_PANEL),
                    # Allow yoda ceiling clip to bypass the door.
                    hard=Or(
                        HasAllAbilities(JEDI | ASTROMECH_PANEL),
                        CAN_YODA_CLIP,
                    )
                ),
            ),
            ExitData(
                R_SITH_FORCE_DROID_ROOM,
                # JEDI and ASTROMECH_PANEL are required to reach here.
                logic_options(
                    base=HasAbility(SITH),
                    normal=HasAbility(SITH) | Extra.DARK_SIDE.has(),
                    hard=Or(
                        HasAbility(SITH),
                        Extra.DARK_SIDE.has(),
                        # ASTROMECH_PANEL means the player must have at least another character.
                        CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                    ),
                ),
                er_rule=logic_options(
                    base=CAN_SITH_FORCE,
                    # Allow using a Yoda ceiling clip to get into the room.
                    hard=CAN_SITH_FORCE | CAN_YODA_CLIP,
                )
            ),
        ),
        R_JANGO_FIGHT: (
            ExitData(
                "Chapter Completion",
                logic_options(
                    base=HasAbility(IS_NON_GHOST_JEDI),
                    # HasAnyAbilities(IS_NON_GHOST_JEDI | BLASTER) is required to get past the ceiling turrets force
                    # field.
                    normal=True_(),
                    # The ceiling turrets could have been destroyed by characters that can deflect bolts, or the Deflect
                    # Bolts Extra and a character that the turrets will shoot at.
                    moderate=Or(
                        HasAnyAbilities(IS_NON_GHOST_JEDI | BLASTER),
                        # JEDI is also required to reach here, and all IS_NON_GHOST_JEDI are JEDI anyway.
                        Extra.SUPER_JEDI_SLAM.has(),
                        CAN_USE_SELF_DESTRUCT,
                    ),
                ),
                er_rule=logic_options(
                    # During the first hovering phase, Jango will not fire Rockets, so a Ghost jedi cannot hit him.
                    # Expect the intended strategy of a Jedi.
                    base=HasAbility(IS_NON_GHOST_JEDI),
                    # Allow Blaster characters.
                    normal=HasAnyAbilities(IS_NON_GHOST_JEDI | BLASTER),
                    moderate=Or(
                        HasAnyAbilities(IS_NON_GHOST_JEDI | BLASTER),
                        # todo?: Also allow Grievous/Bodyguard/Tarpals/Imperial Guard on their own, to deflect bolts
                        #  into Jango during the first hovering phase?
                        # Ghost Jedi can hit Jango in the first hovering phase with Super Jedi Slam.
                        HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM) & Extra.SUPER_JEDI_SLAM.has(),
                        # Self-destruct will also hit Jango if the only character you have is a passive droid.
                        CAN_USE_SELF_DESTRUCT,
                    ),
                ),
            ),
        ),
        R_SITH_FORCE_DROID_ROOM: (),
    },
    minikits={
        "Minikit Above Landing Pad Platform": minikit_data(
            R_LANDING_PAD,
            logic_options(
                # Force the gears, then high jump to reach the minikit.
                base=HasAllAbilities(JEDI | HIGH_JUMP),
                # Force the gears, then stand on the gears, and double jump + slam to reach the minikit.
                # Double jump + slam from beneath the minikit also works when Stud Magnet is enabled.
                normal=HasAbility(JEDI),
            ),
            pickup_name="MINI01",
        ),
        "Floating Platform Minikit": minikit_data(
            R_SPAWN_FLOATING_MINIKIT_PLATFORM,
            pickup_name="MINI02",
        ),
        "Six Walkway Lights Minikit": minikit_data(
            R_CLONE_VIEWING_AREA,
            logic_options(
                # Jedi is required to reach here.
                base=True_(),
                # Hard logic can reach here with a Jetpack character instead.
                hard=HasAbility(JEDI),
            ),
            er_rule=HasAbility(JEDI),
            pickup_name="MINI3",
        ),
        "Four Updrafts Platform Minikit": minikit_data(
            R_BOUNTY_HUNTER_AREA,
            # Jedi is required to reach here.
            True_(),
            er_rule=logic_options(
                # Double jump across the platforms and then force the small platform out, to use to reach the minikit.
                # HOVER/CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS/CAN_DOUBLE_JUMP can jump across the circular platforms, but
                # HOVER/'can jump slighter further'(CAN_JUMP_DISTANCE_0_84 + CAN_JUMP_0_44)/CAN_DOUBLE_JUMP
                # is needed to jump to the platform where the minikit is. CAN_JUMP_DISTANCE_0_84 just barely makes the
                # jump, so can_jump_distance_rule(0.9) is more appropriate.
                # Note that the AI P2 will only use JEDI/HIGH_JUMP/Astromech Droid to cross the circular platforms, but
                # we don't have a good way to logically check for just Astromech Hover and not Jetpack Hover currently.
                base=HasAbility(JEDI),
                # High triple jump can reach the minikit without needing to force the small platform out.
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="MINI05",
        ),
        "Five Access Hatches Minikit": minikit_data(
            R_BOUNTY_HUNTER_AREA,
            # Jedi is required to reach here.
            logic_options(
                # Bounty Hunter is required to reach here.
                base=HasAbility(SHORTIE),
                # Bounty Hunter is no longer required, if you can ceiling clip.
                hard=And(
                    # Reach the Access Hatches area.
                    HasAbility(BLASTER) | Character.GENERAL_GRIEVOUS.has(),
                    # Actually get the minikit.
                    HasAbility(SHORTIE) | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                )
            ),
            er_rule=logic_options(
                # AI P2 will only use Jedi/High-Jump and Astromech Hover, so Jetpack Hover is not allowed here because
                # then 1P2C would be required.
                base=(HAS_P2_AI_DOUBLE_JUMP | HasAbility(ASTROMECH_DROID)) & HasAllAbilities(BLASTER | SHORTIE),
                # Allow jumping across the platforms with normal jump distance (may require 1P2C).
                # Jetpack Hover would work too (potentially requiring 1P2C), but both Jango and Boba have normal jump
                # distance.
                # General Grievous's triple jump can skip needing a BLASTER character to extend the bridge.
                # todo: It seems to be possible to grab this minikit with Droideka + Yoda + maybe Stud Magnet, but it
                #  seems inconsistent.
                # The distance from the start area to the first platform is about 0.9376
                # Ewok (0.69) and Clone (0.7) cannot jump across the platforms.
                # Dexter can make it with a good jump.
                moderate=And(
                    HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER) | CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
                    HasAbility(BLASTER) | Character.GENERAL_GRIEVOUS.has(),
                    HasAbility(SHORTIE),
                ),
                # Instead of using a vent, Yoda ceiling clip over the top of the machine and access the minikit from
                # behind.
                hard=And(
                    HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER | CAN_JUMP_DISTANCE_0_69),
                    HasAbility(BLASTER) | Character.GENERAL_GRIEVOUS.has(),
                    HasAbility(SHORTIE) | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                ),
            ),
            pickup_name="MINI04",
        ),
        "Mosaic Vending Machine Minikit": minikit_data(
            R_LIVING_QUARTERS,
            # Jedi is required to reach here.
            True_(),
            er_rule=logic_options(
                base=HasAbility(JEDI),
                # Swap to Droideka while as close to the Minikit as possible. Stud Magnet isn't even needed.
                moderate=Or(
                    HasAbility(JEDI),
                    HasAbility(CAN_JUMP_HEIGHT_0_37) & Character.DROIDEKA.has(),
                ),
                # Yoda Grabs can get this, but Yoda can just get the minikit the intended way.
            ),
            pickup_name="mkvend",
        ),
        "Two Player Triple Buttons Minikit": minikit_data(
            R_LIVING_QUARTERS_BEHIND_FORCE_FIELD,
            # Jedi is required to reach here.
            True_(),
            er_rule=logic_options(
                # A higher than normal jump is required to get into the alcove that the minikit is in.
                base=HasAbility(CAN_DOUBLE_JUMP),
                # Allow characters with a slightly higher jump.
                normal=HasAbility(CAN_JUMP_0_44),
                # Allow stormtrooper flop for a tiny bit of extra height.
                # Allow Taun We and Lama Su, who only have a basic jump height, but can make this jump anyway, sort of
                # sliding up the wall when holding forwards on the controller.
                moderate=Or(
                    HasAnyAbilities(CAN_JUMP_0_44 | CAN_FLOP_JUMP),
                    Character.has_any(Character.TAUN_WE, Character.LAMA_SU),
                ),
            ),
            pickup_name="mk3way",
        ),
        "Jango Chase Hover Platform Minikit": minikit_data(
            R_START_OF_OUTSIDE_JANGO_CHASE_MINIKIT_PLATFORM,
            pickup_name="mk_1",
        ),
        "Blaster Targets Reward Minikit": minikit_data(
            R_END_OF_OUTSIDE_JANGO_CHASE_UPPER_SECTION,
            # Jedi is required to reach here.
            logic_options(
                # Grapple is expected to reach here, so logic only needs to check for PROTOCOL_PANEL.
                base=HasAbility(PROTOCOL_PANEL),
                normal=HasAllAbilities(PROTOCOL_PANEL | BLASTER),
                moderate=Or(
                    # Self Destruct does not work because the moving platform is not safe ground, so, after
                    # exploding, you respawn back on the ground.
                    # Hitting the targets with an ewok is a bit annoying, but doable.
                    HasAbility(PROTOCOL_PANEL) & HasAnyAbilities(BLASTER | WEAPON_EWOK),
                    # Jump up to the slightly raised part of the machine the minikit is in, and then swap to
                    # Droideka to grab the minikit through the door of the machine. Stud Magnet is not required.
                    Character.DROIDEKA.has(),
                ),
                # Allow Yoda Grab.
                hard=Or(
                    HasAbility(PROTOCOL_PANEL) & HasAnyAbilities(BLASTER | WEAPON_EWOK),
                    Character.DROIDEKA.has(),
                    _CAN_YODA_GRAB_BLASTER_TARGETS_REWARD_MINIKIT,
                ),
            ),
            er_rule=logic_options(
                base=CAN_GRAPPLE & HasAbility(PROTOCOL_PANEL),
                moderate=And(
                    # Get to the upper area.
                    HasAnyAbilities(GRAPPLE | CAN_HIGH_JUMP_SLAM),
                    # Access the Minikit.
                    Or(
                        # Self Destruct does not work because the moving platform is not safe ground, so, after
                        # exploding, you respawn back on the ground.
                        # Hitting the targets with an ewok is a bit annoying, but doable.
                        HasAbility(PROTOCOL_PANEL) & HasAnyAbilities(BLASTER | WEAPON_EWOK),
                        # Jump up to the slightly raised part of the machine the minikit is in, and then swap to
                        # Droideka to grab the minikit through the door of the machine. Stud Magnet is not required.
                        Character.DROIDEKA.has(),
                    )
                ),
            ),
            pickup_name="mk_0",
        ),
        "Dark Side Droid Room Minikit": minikit_data(
            R_SITH_FORCE_DROID_ROOM,
            # JEDI is required to reach here.
            # ASTROMECH_PANEL is required to reach here.
            logic_options(
                base=HasAbility(SITH),
                normal=HasAbility(SITH) | Extra.DARK_SIDE.has(),
                # Droideka can also grab this through the force field, though this isn't logically relevant currently.
                hard=Or(
                    HasAbility(SITH) | Extra.DARK_SIDE.has(),
                    HAS_ANY_YODA,
                ),
            ),
            er_rule=logic_options(
                base=CAN_SITH_FORCE,
                # Yoda's weird collision can grab it through the force field, no character swapping required.
                hard=CAN_SITH_FORCE | HAS_ANY_YODA,
            ),
            pickup_name="m_pup1",
        )
    },
    # Expert can level transition skip to get beneath the floor.
    power_brick=LocationData(
        R_LIVING_QUARTERS,
        logic_options(
            base=HasAbility(IMPERIAL),
            # An ASTROMECH_PANEL user is strictly required to reach here.
            hard=HasAbility(IMPERIAL) | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
        )
    ),
)
