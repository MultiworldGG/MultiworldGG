from rule_builder.rules import And, Or, True_

from ..macros import (
    CAN_GRAPPLE,
    CAN_USE_SELF_DESTRUCT,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE_AND_GRAPPLE,
    CAN_SITH_FORCE,
    CAN_ACTIVATE_CLOSE_TARGET,
    CAN_YODA_CLIP,
    HAS_ANY_YODA,
    CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
    HAS_WALL_CLIMB,
)
from ..option_filters import logic_options
from ..rules import HasAbility, HasAllAbilities, HasAnyAbilities, HasAbilityExceptCharacters, HasAnyCharacterExcept
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_ROOFTOPS_SPAWN = "Rooftops Spawn"
R_ROOFTOPS_CLIMB = "Rooftops Climb"
R_TOWER = "Tower"
R_ROOFTOPS_AFTER_SMALL_BLASTER_TARGET_GATE = "Rooftops After Small Blaster Target Gate"
R_FINAL_ROOFTOP = "Final Rooftop"

ESCAPE_FROM_NABOO = Chapter(
    area=Area.PALACERESCUE,
    start_region=R_ROOFTOPS_SPAWN,
    regions={
        R_ROOFTOPS_SPAWN: (
            ExitData(
                R_ROOFTOPS_CLIMB,
                logic_options(
                    base=CAN_GRAPPLE,
                    # Allow triple high jump, possible from standing on one of the flowerbeds, but easier by starting
                    # from one of the fences which are higher up.
                    moderate=CAN_GRAPPLE | HasAbility(CAN_HIGH_JUMP_SLAM),
                    # Allow Yoda's extra height triple jump, starting from the spike on one of the fences.
                    # You can also Yoda Clip into the arch one of the windows is in, and stand on top of the window,
                    # then jump up.
                    hard=CAN_GRAPPLE | HasAbility(CAN_HIGH_JUMP_SLAM) | And(
                        HAS_ANY_YODA,
                        HasAnyCharacterExcept(Character.YODA, Character.YODA_GHOST),
                    ),
                )
            ),
        ),
        R_ROOFTOPS_CLIMB: (
            ExitData(R_TOWER, new_level=Level.RESCUE_B),
        ),
        R_TOWER: (
            ExitData(
                R_ROOFTOPS_AFTER_SMALL_BLASTER_TARGET_GATE,
                logic_options(
                    base=True_(),
                    normal=CAN_ACTIVATE_CLOSE_TARGET,
                    # Allow Yoda Clip while standing beneath the arch. The arch's collision extends like a tunnel with
                    # double-sided walls, so you'll have to walk around to the end of the collision to then walk inside
                    # the tunnel and get to the level transition. Droideka always seems to get pushed out.
                    # Triple High Jump should also be possible here because there is a collision wall to the right that
                    # is just short enough to get onto, but I was having trouble with this.
                    hard=CAN_ACTIVATE_CLOSE_TARGET | (HAS_ANY_YODA & HasAnyCharacterExcept(
                        Character.YODA, Character.YODA_GHOST, Character.DROIDEKA)),
                ),
                er_rule=logic_options(
                    base=CAN_ACTIVATE_CLOSE_TARGET,
                    hard=CAN_ACTIVATE_CLOSE_TARGET | (HAS_ANY_YODA & HasAnyCharacterExcept(
                        Character.YODA, Character.YODA_GHOST, Character.DROIDEKA)),
                ),
                new_level=Level.RESCUE_C,
            ),
        ),
        R_ROOFTOPS_AFTER_SMALL_BLASTER_TARGET_GATE: (
            ExitData(
                R_FINAL_ROOFTOP,
                logic_options(
                    base=True_(),
                    moderate=Or(
                        HasAnyAbilities(BLASTER | WEAPON_EWOK),
                        CAN_USE_SELF_DESTRUCT & HasAbility(CAN_JUMP_HEIGHT_0_37),
                    ),
                ).or_rule(
                    apply_to="hard+",
                    rule=CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS | HAS_WALL_CLIMB,
                ),
                er_rule=logic_options(
                    base=HasAbility(BLASTER),
                    # Ewoks are awkward because they don't auto-target the targets.
                    normal=HasAnyAbilities(BLASTER | WEAPON_EWOK),
                    # The platforms that raise up to the targets start slightly raised above the ground, too high for
                    # Astromech Droids and Droids that cannot jump to get on, so if using Self Destruct to activate
                    # these targets, a Droid that can jump is required.
                    moderate=Or(
                        HasAnyAbilities(BLASTER | WEAPON_EWOK),
                        CAN_USE_SELF_DESTRUCT & HasAbility(CAN_JUMP_HEIGHT_0_37),
                    ),
                ).or_rule(
                    # The wall above the gate can be wall climbed, or you can Yoda Clip through the arched part of the
                    # collision. Either way, you can then drop down to the other side of the gate and hit the level
                    # transition.
                    apply_to="hard+",
                    rule=CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS | HAS_WALL_CLIMB,
                ),
                # rescue_d does not exist.
                new_level=Level.RESCUE_E,
            ),
        ),
        R_FINAL_ROOFTOP: (
            ExitData(
                "Chapter Completion",
                er_rule=logic_options(
                    # The button to press is in a raised area, and there is a destroyable cover over the chapter
                    # completion.
                    base=HasAbility(CAN_JUMP_HEIGHT_0_37) & CAN_DAMAGE_AT_CLOSE_RANGE,
                    # Consider Self Destruct for dealing damage.
                    normal=CAN_DAMAGE_AT_CLOSE_RANGE & HasAbility(CAN_JUMP_HEIGHT_0_37),
                    # Astromech droids can just barely get up to the raised area.
                    moderate=CAN_DAMAGE_AT_CLOSE_RANGE & HasAbility(CAN_BARELY_JUMP),
                ),
            ),
        ),
    },
    minikits={
        "Stack Boxes Minikit": minikit_data(
            R_ROOFTOPS_SPAWN,
            logic_options(
                strict=False,
                # Destroy the doors, force the columns into boxes, stack the boxes and then high jump up.
                base=HasAllAbilities(JEDI | HIGH_JUMP),
            ).or_rule(
                # Take the first grapple, jump onto the window sill, then jump and jetpack hover across.
                apply_to="normal+",
                rule=HasAbility(JETPACK),
            ).or_rule(
                # Triple High Jump can reach the minikit without stacking any boxes.
                apply_to="moderate+",
                rule=HasAbility(CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="mk_0",
        ),
        "Minikit Hidden In Climbing Plants": minikit_data(
            R_ROOFTOPS_CLIMB,
            logic_options(
                # Force the wall platforms, high jump up and then hover across.
                base=HasAllAbilities(JEDI | HOVER | HIGH_JUMP),
                # Double jump + slam (no triple jump needed) is enough to reach the kit from the silver objects beneath
                # it. Alternatively, a High Jump from the silver objects works too.
                normal=HasAnyAbilities(JEDI | HIGH_JUMP),
            ),
            pickup_name="mk_1",
        ),
        "Minikit Behind Camera At Roof Tower Spawn": minikit_data(
            R_TOWER,
            pickup_name="mk_1",
        ),
        "Roof Tower Lower Ledge Minikit": minikit_data(
            R_TOWER,
            er_rule=logic_options(
                # Destroy the windows to get into the outside area.
                # If the player jumps down without being able to grapple back up, they have to restart the level, so
                # expect grapple on the base logic difficulty.
                # All grapple users have blasters and can jump.
                base=HasAbility(GRAPPLE),
                # There is a small lip around the upper area, that needs a jump or Astromech hover to cross.
                # TODO: Check if Captain Tarpals can destroy these windows.
                normal=And(
                    CAN_DAMAGE_AT_CLOSE_RANGE,
                    HasAbility(CAN_BARELY_JUMP),
                ),
                # Droideka can also get over the lip by taking a running start from the furthest right flower bed.
                moderate=And(
                    CAN_DAMAGE_AT_CLOSE_RANGE,
                    HasAbility(CAN_BARELY_JUMP) | Character.DROIDEKA.has(),
                ),
            ),
            pickup_name="mk_0",
        ),
        "Sith Force Flowerbeds Minikit": minikit_data(
            R_TOWER,
            logic_options(
                base=HasAllAbilities(SITH | HOVER),
                normal=HasAbility(HOVER) & CAN_SITH_FORCE,
                moderate=CAN_SITH_FORCE
            ),
            er_rule=logic_options(
                # Grapple to get up/down the tower/roofing. Hover to cross the gap between roofs. Sith to force the
                # flowers.
                base=HasAbility(HOVER) & CAN_SITH_FORCE_AND_GRAPPLE,
                # Triple jump can cross the gap and replace using grapple to get to the minikit.
                # Note that to continue with the level, one of the flowerbeds in the first lower section cannot be
                # destroyed because it is needed to get enough height to triple jump back up to the higher section and
                # continue with the level.
                moderate=CAN_SITH_FORCE
            ),
            pickup_name="m_pup1",
        ),
        "Minikit After Access Hatch": minikit_data(
            R_ROOFTOPS_AFTER_SMALL_BLASTER_TARGET_GATE,
            logic_options(
                base=HasAllAbilities(SHORTIE | HIGH_JUMP),
                # Jedi can triple jump up instead of using high jump, so Force Grapple Leap is irrelevant.
                moderate=HasAbility(SHORTIE) & HasAnyAbilities(JEDI | GRAPPLE | HIGH_JUMP),
            ).or_rule(
                apply_to="hard+",
                rule=Or(
                    # Yoda Clip from the small arched alcove next to the Access Hatch. You can then either jump up to
                    # the higher area, or character swap to upwarp to the higher area.
                    # To get through the small target gate, you need another non-Yoda character to either activate the
                    # target and open the gate, or to Yoda Clip around the gate.
                    CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                    # The wall to the left of the small arched alcove can be wall-climbed with Grievous.
                    HAS_WALL_CLIMB,
                ),
            ),
            er_rule=logic_options(
                # Grapple or High Jump up and then use the hatch.
                base=HasAbility(SHORTIE) & (CAN_GRAPPLE | HasAbility(HIGH_JUMP)),
                moderate=HasAbility(SHORTIE) & HasAnyAbilities(JEDI | GRAPPLE | HIGH_JUMP),
            ).or_rule(
                apply_to="hard+",
                rule=CAN_YODA_CLIP,
            ),
            pickup_name="mk_0",
        ),
        "Force All Fences Minikit": minikit_data(
            R_ROOFTOPS_AFTER_SMALL_BLASTER_TARGET_GATE,
            HasAbility(JEDI),
            er_rule=logic_options(
                # Jedi alone cannot get here, so Grapple or High Jump are needed.
                base=HasAbility(JEDI) & HasAnyAbilities(GRAPPLE | HIGH_JUMP),
                # Also consider Force Grapple Leap.
                normal=And(
                    HasAbility(JEDI),
                    HasAnyAbilities(GRAPPLE | HIGH_JUMP) | Extra.FORCE_GRAPPLE_LEAP.has()
                ),
                # Triple jump to the fences area.
                moderate=HasAbility(JEDI),
            ),
            pickup_name="MINI_1",
        ),
        "Force Mural Minikit": minikit_data(
            R_ROOFTOPS_AFTER_SMALL_BLASTER_TARGET_GATE,
            logic_options(
                # All Bounty Hunters can grapple.
                base=HasAllAbilities(BOUNTY_HUNTER | JEDI),
                normal=HasAbility(JEDI) & CAN_DESTROY_CLOSE_SILVER_BRICKS,
            ),
            er_rule=logic_options(
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(JEDI) & CAN_GRAPPLE,
                # Allow using extras to destroy the silver brick windows, and allow Force Grapple Leap.
                normal=And(
                    HasAbility(JEDI),
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    HasAbility(HIGH_JUMP) | CAN_GRAPPLE,
                ),
                # Triple jump skips any need to grapple.
                moderate=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(JEDI),
            ),
            pickup_name="m_pup1",
        ),
        "Minikit Under Silver Cover": minikit_data(
            R_FINAL_ROOFTOP,
            CAN_DESTROY_CLOSE_SILVER_BRICKS,
            er_rule=logic_options(
                # (all bounty hunters can jump normal height)
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(CAN_JUMP_HEIGHT_0_37),
                # The button to press is in a raised area.
                normal=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(CAN_JUMP_HEIGHT_0_37),
                # The button to press is in a raised area. Astromech droids can just barely get up.
                moderate=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(CAN_BARELY_JUMP),
            ),
            pickup_name="mk_1",
        ),
        "Stack Plant Pots High Minikit": minikit_data(
            R_FINAL_ROOFTOP,
            logic_options(
                base=HasAbility(JEDI),
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            er_rule=logic_options(
                # Stack the plant pots and then double jump to the minikit.
                base=HasAbility(JEDI),
                # Triple high jump can reach the minikit without stacking any plant pots.
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="mk_0"
        ),
    },
    power_brick=LocationData(
        R_ROOFTOPS_CLIMB,
        logic_options(
            base=HasAllAbilities(SITH | BOUNTY_HUNTER),
            normal=And(
                Or(
                    HasAbility(SITH),
                    Extra.DARK_SIDE.has() & HasAbilityExceptCharacters(JEDI, Character.YODA, Character.YODA_GHOST)
                ),
                CAN_DESTROY_CLOSE_SILVER_BRICKS
            ),
            moderate=Or(
                HasAbility(SITH),
                Extra.DARK_SIDE.has() & HasAbilityExceptCharacters(JEDI, Character.YODA, Character.YODA_GHOST)
            )
        ),
        er_rule=logic_options(
            # There are Silver brick objects to destroy and Dark Side force flowers to force.
            # All Sith (and Jedi) can build bricks and push blocks.
            base=And(
                CAN_DESTROY_CLOSE_SILVER_BRICKS,
                CAN_SITH_FORCE,
                # When Dark Side is allowed instead of just Sith. Yoda (and Yoda (Ghost)) struggle a lot to use force on
                # one of the flowers, so they are excluded.
                HasAbilityExceptCharacters(JEDI, Character.YODA, Character.YODA_GHOST)
            ),
            # The Silver brick objects can actually be destroyed with a slam attack for some reason, so being able to
            # destroy Silver brick objects is not needed.
            moderate=Or(
                HasAbility(SITH),
                Extra.DARK_SIDE.has() & HasAbilityExceptCharacters(JEDI, Character.YODA, Character.YODA_GHOST)
            )
        )
    ),
)
