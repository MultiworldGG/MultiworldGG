from rule_builder.rules import And, Or, True_

from ..macros import (
    CAN_USE_SELF_DESTRUCT,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_DAMAGE_SHIELDED_DROIDEKA,
    CAN_USE_DEFLECT_BOLTS,
    CAN_YODA_CLIP,
)
from ..option_filters import logic_options
from ..rules import HasAbility, HasAllAbilities, HasAnyAbilities
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN = "Spawn"
R_INSIDE_PALACE = "Inside Palace"
R_AFTER_COLLAPSED_FLOOR_IN_PALACE = "After Collapsed Floor In Palace"
R_COURTYARD = "Courtyard"
R_COURTYARD_AFTER_DESTROYED_BRIDGE = "Courtyard After Destroyed Bridge"
R_ROOFTOPS = "Rooftops"
R_DINING_HALL = "Dining Hall"
R_HANGAR = "Hangar"

RETAKE_THEED_PALACE = Chapter(
    area=Area.RETAKEPALACE,
    start_region=R_SPAWN,
    intended_completion_path={
        "base": (
            R_INSIDE_PALACE,
            R_AFTER_COLLAPSED_FLOOR_IN_PALACE,
            R_COURTYARD,
            R_COURTYARD_AFTER_DESTROYED_BRIDGE,
            R_ROOFTOPS,
            R_DINING_HALL,
            R_HANGAR,
        ),
    },
    regions={
        R_SPAWN: (
            ExitData(
                R_INSIDE_PALACE,
                logic_options(
                    base=And(
                        # Use the panel.
                        HasAbility(ASTROMECH_PANEL),
                        # Ascend to the higher area with the panel.
                        HasAnyAbilities(JEDI | GRAPPLE | HIGH_JUMP),
                        # Base logic expects being able to defeat the Droideka.
                        CAN_DAMAGE_SHIELDED_DROIDEKA,
                    ),
                    # Jump up the bricks to the side of the bricks that make the ramp.
                    # And just ignore Droideka if they cannot be defeated.
                    normal=HasAllAbilities(ASTROMECH_PANEL | CAN_JUMP_HEIGHT_0_37),
                    # Expert can push R2-D2 onto some objects to get him up to the panel, though I don't know if this is
                    # possible with other characters that cannot jump normally.
                    # expert=HasAbility(ASTROMECH_PANEL),
                ).or_rule(
                    # Clip through the door with a swap to a small character, or clip through the ceiling of the round
                    # window area with the minikit. In the latter case, you need to be careful to not go too short and
                    # fall down on the front of the door, or too far, and hit the backwards transition.
                    apply_to="hard+",
                    rule=CAN_YODA_CLIP,
                ),
                new_level=Level.RETAKE_B,
            ),
        ),
        R_INSIDE_PALACE: (
            ExitData(
                R_AFTER_COLLAPSED_FLOOR_IN_PALACE,
                logic_options(
                    # Force the platform and double jump across, or use the chute, or hover across.
                    base=HasAnyAbilities(JEDI | SHORTIE | HOVER),
                    # High jump characters can cross the gap by hugging the far wall, except Grievous' Bodyguard, but
                    # Grievous' Bodyguard can triple high jump to cross the gap.
                    moderate=HasAnyAbilities(JEDI | SHORTIE | HOVER | HIGH_JUMP),
                )
            ),
        ),
        R_AFTER_COLLAPSED_FLOOR_IN_PALACE: (
            ExitData(
                R_COURTYARD,
                logic_options(
                    base=HasAbility(CAN_BUILD_BRICKS),
                    normal=HasAbility(CAN_BUILD_BRICKS) & CAN_DAMAGE_AT_CLOSE_RANGE,
                    moderate=And(
                        HasAbility(CAN_BUILD_BRICKS),
                        CAN_DAMAGE_AT_CLOSE_RANGE | CAN_USE_DEFLECT_BOLTS,
                    ),
                    # Yoda Clip could have skipped the first Astromech Panel, so logic needs to check for it here.
                    hard=And(
                        HasAllAbilities(CAN_BUILD_BRICKS | ASTROMECH_PANEL),
                        CAN_DAMAGE_AT_CLOSE_RANGE | CAN_USE_DEFLECT_BOLTS,
                    ),
                ),
                er_rule=logic_options(
                    # All characters that can build bricks can jump, and being able to damage shielded droideka implies
                    # being able to destroy the statue to spawn the astromech panel bricks.
                    base=HasAllAbilities(CAN_BUILD_BRICKS | ASTROMECH_PANEL) & CAN_DAMAGE_SHIELDED_DROIDEKA,
                    # There's no expectation to be able to kill droideka so dealing damage at close range is enough,
                    # though Astromech can remove shields anyway.
                    normal=HasAllAbilities(CAN_BUILD_BRICKS | ASTROMECH_PANEL) & CAN_DAMAGE_AT_CLOSE_RANGE,
                    # Alternatively expect Deflect Bolts to deflect enemy blaster bolts into the statue.
                    moderate=And(
                        HasAllAbilities(CAN_BUILD_BRICKS | ASTROMECH_PANEL),
                        CAN_DAMAGE_AT_CLOSE_RANGE | CAN_USE_DEFLECT_BOLTS,
                    ),
                ),
                # retake_c does not exist.
                new_level=Level.RETAKE_D,
            ),
        ),
        R_COURTYARD: (
            ExitData(
                R_COURTYARD_AFTER_DESTROYED_BRIDGE,
                logic_options(
                    # Hover from the rising platform, or jump up the stairs and force the bridge.
                    base=HasAnyAbilities(JEDI | HOVER),
                    # High jump from the rising platform works, but it is easier to high jump up parts of the buildings
                    # on the left.
                    # For Ackbar, double jump from the rising platform or just jump across the broken bridge. There is
                    # also a tight double jump up part of one of the buildings that is used in speedruns:
                    # https://youtu.be/W66qxVkOaPA?t=945.
                    normal=HasAnyAbilities(JEDI | HOVER | HIGH_JUMP | CAN_DOUBLE_JUMP),
                )
            ),
        ),
        R_COURTYARD_AFTER_DESTROYED_BRIDGE: (
            ExitData(
                R_ROOFTOPS,
                logic_options(
                    base=HasAbility(SHORTIE),
                    normal=HasAnyAbilities(HIGH_JUMP | SHORTIE),
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP | SHORTIE),
                ),
                er_rule=logic_options(
                    # Destroy the flowerbed and use the chute and use the force to destroy the obstacles blocking the
                    # way.
                    # Or hover past the obstacles.
                    # Then use the chute up to the button.
                    base=HasAbility(SHORTIE) & HasAnyAbilities(JEDI | HOVER),
                    # High jump can jump on the first obstacle and then jump to the button.
                    # This is not in the base logic because the obstacles do not respawn if destroyed.
                    normal=Or(
                        HasAbility(HIGH_JUMP),
                        HasAbility(SHORTIE) & HasAnyAbilities(JEDI | HOVER),
                    ),
                    # Triple jump can replace high jump.
                    moderate=Or(
                        HasAnyAbilities(JEDI | HIGH_JUMP),
                        HasAllAbilities(SHORTIE | HOVER),
                    )
                ),
                new_level=Level.RETAKE_E,
            ),
        ),
        R_ROOFTOPS: (
            ExitData(
                R_DINING_HALL,
                logic_options(
                    base=True_(),
                    # Triple high jump can stand on one of the taller bushes and triple high jump up.
                    moderate=HasAnyAbilities(JEDI | GRAPPLE | SHORTIE | CAN_HIGH_JUMP_SLAM),
                ),
                er_rule=logic_options(
                    # Jedi can force platforms.
                    # Grapple can destroy the flowerbed hiding the grapple point.
                    # Shortie can use the chute.
                    base=HasAnyAbilities(JEDI | GRAPPLE | SHORTIE),
                    # Triple high jump can stand on one of the taller bushes and triple high jump up.
                    moderate=HasAnyAbilities(JEDI | GRAPPLE | SHORTIE | CAN_HIGH_JUMP_SLAM),
                ),
                new_level=Level.RETAKE_F,
            ),
        ),
        R_DINING_HALL: (
            ExitData(
                R_HANGAR,
                # Base:
                #  HasAnyAbilities(JEDI | GRAPPLE | HIGH_JUMP) implies CAN_BARELY_JUMP
                #  can_damage_shielded_droideka.base is
                #  Or(HasAnyAbilities(JEDI | BOUNTY_HUNTER | CAN_HIGH_JUMP_SLAM), Character.DROIDEKA.has())
                # Normal:
                #  HasAnyAbilities(HIGH_JUMP | SHORTIE) implies HasAbility(CAN_BARELY_JUMP).
                #  can_damage_at_close_range is already needed at "After Collapsed Floor In Palace -> Courtyard".
                # Moderate:
                #  can_damage_at_close_range | can_deflect_bolts is already needed at
                #  "After Collapsed Floor In Palace -> Courtyard".
                #  CAN_BUILD_BRICKS implies CAN_BARELY_JUMP.
                er_rule=logic_options(
                    # Fight the Droideka, destroy the statue, and stand on the button.
                    # A character that can jump, even astromech droids, is needed to get up a small lip before the
                    # button.
                    base=Or(
                        HasAnyAbilities(JEDI | BOUNTY_HUNTER | CAN_HIGH_JUMP_SLAM),
                        Character.DROIDEKA.has() & HasAbility(CAN_BARELY_JUMP),
                    ),
                    # The droideka can be ignored.
                    normal=HasAbility(CAN_BARELY_JUMP) & CAN_DAMAGE_AT_CLOSE_RANGE,
                    # Allow Deflect Bolts to destroy the statue.
                    # Droideka can also get up the small lip to get to the button, by repeatedly switching between
                    # Droideka and another character while rolling against the lip.
                    # ER Note: It is not currently possible to get here with just Droideka, but with ER, it could be
                    # possible, and then logic would need to ensure that the player has another character besides
                    # Droideka.
                    moderate=Or(
                        And(
                            CAN_DAMAGE_AT_CLOSE_RANGE | CAN_USE_DEFLECT_BOLTS,
                            HasAbility(CAN_BARELY_JUMP),
                        ),
                        Character.DROIDEKA.has(),
                    ),
                ),
                new_level=Level.RETAKE_G,
            ),
        ),
        R_HANGAR: (
            ExitData(
                "Chapter Completion",
                logic_options(
                    # All: ASTROMECH_PANEL is needed near the start.
                    base=HasAllAbilities(JEDI | GRAPPLE),
                    normal=HasAnyAbilities(JEDI | BLASTER),
                    #  can_damage_at_close_range | can_deflect_bolts is already needed at
                    #  "After Collapsed Floor In Palace -> Courtyard".
                    moderate=Or(
                        HasAnyAbilities(JEDI | BLASTER),
                        HasAbility(HIGH_JUMP),
                    ),
                ),
                # Logic breakdown for freeing each set of captive pilots:
                #  High up droid in the middle, with two captive pilots:
                #   Base: Reach the droid by using the force on the boxes with P2 (Jedi)
                #   Normal: Alternatively, shoot the droid from afar, or High Jump up off the starfighter, and then
                #    destroy the Battle Droid with a close range attack (high_jump AND can_damage_at_close_range).
                #  Droids on the ground with two captive pilots:
                #   Base: can_damage_at_close_range
                #  Far left droid at the front:
                #   Base: Destroy the objects in the front far left corner to spawn the grapple point, then grapple up
                #    (grapple [implies blaster])
                #   Normal: Alternatively, shoot the droid from afar (blaster) or stack the nearby boxes as a Jedi and
                #    jump across to the closed hangar exit and jump across to the platform the grapple point would take
                #    the player to (jedi). Force Grapple Leap is therefore not logically relevant here.
                #   Moderate: Alternatively, High Jump off terrain (high_jump AND can_damage_at_close_range) or triple
                #    jump up (jedi)
                #  Far left droid at the back (by the silver bricks):
                #   Base: Stack the boxes and jump up (jedi)
                #   Normal: Alternatively, shoot the droid from afar (blaster) or High Jump up from the large box
                #    (high_jump AND can_damage_at_close_range)
                #  Actually completing the chapter also requires astromech_panel.
                er_rule=logic_options(
                    base=HasAllAbilities(JEDI | GRAPPLE | ASTROMECH_PANEL),
                    normal=HasAnyAbilities(JEDI | BLASTER | ASTROMECH_PANEL),
                    moderate=And(
                        Or(
                            HasAnyAbilities(JEDI | BLASTER),
                            HasAbility(HIGH_JUMP) & (CAN_DAMAGE_AT_CLOSE_RANGE | CAN_USE_DEFLECT_BOLTS),
                        ),
                        HasAbility(ASTROMECH_PANEL),
                    )
                ),
            ),
        ),
    },
    minikits={
        "Circular Window Minikit": minikit_data(
            R_SPAWN,
            logic_options(
                base=HasAbility(JEDI),
                # Grapple characters can shoot the window, but the basic jump height (jump_speed=2.1) is not enough to
                # jump into the window. A character with the slightly better jump height (jump_speed=2.3), however, can
                # jump into the window.
                normal=Or(
                    HasAbility(JEDI),
                    HasAllAbilities(GRAPPLE | CAN_JUMP_0_44),
                ),
                # Triple High Jump can also reach the upper area that the window is in.
                # But General Grievous is too big to be able to hit the window without Super Jedi Slam or some means of
                # shooting, or exploding, the window.
                # Ewoks cannot hit the upper half of the window on their own, needing their projectile upgraded to cause
                # explosions.
                moderate=Or(
                    HasAbility(JEDI),
                    HasAllAbilities(GRAPPLE | CAN_JUMP_0_44),
                    Character.GRIEVOUS_BODYGUARD.has(),
                    And(
                        Character.GENERAL_GRIEVOUS.has(),
                        Or(
                            HasAbility(BLASTER),
                            Extra.SUPER_JEDI_SLAM.has(),
                            CAN_USE_SELF_DESTRUCT,
                            HasAbility(WEAPON_EWOK) & Extra.has_any(
                                Extra.SUPER_EWOK_CATAPULT, Extra.EXPLODING_BLASTER_BOLTS
                            )
                        )
                    )
                )
            ),
            pickup_name="mk_0",
        ),
        "Window Behind Grapple Point Minikit": minikit_data(
            R_SPAWN,
            HasAnyAbilities(JEDI | GRAPPLE),
            pickup_name="mk_1",
        ),
        "Minikit In Hidden Panel Behind Statue": minikit_data(
            R_AFTER_COLLAPSED_FLOOR_IN_PALACE,
            logic_options(
                # can_damage_shielded_droideka.base implies can_damage_at_close_range.base
                base=True_(),
                # Includes self-destruct.
                normal=CAN_DAMAGE_AT_CLOSE_RANGE,
                # Include Deflect Bolts.
                moderate=CAN_DAMAGE_AT_CLOSE_RANGE | CAN_USE_DEFLECT_BOLTS,
            ),
            er_rule=logic_options(
                base=CAN_DAMAGE_AT_CLOSE_RANGE,
                # Includes self-destruct.
                normal=CAN_DAMAGE_AT_CLOSE_RANGE,
                # Include Deflect Bolts.
                moderate=CAN_DAMAGE_AT_CLOSE_RANGE | CAN_USE_DEFLECT_BOLTS,
            ),
            pickup_name="mk_0",
        ),
        "Minikit Behind Dark Side Barrier": minikit_data(
            R_AFTER_COLLAPSED_FLOOR_IN_PALACE,
            CAN_SITH_FORCE,
            pickup_name="mk_1",
        ),
        "Minikit On Courtyard Far Ledge": minikit_data(
            R_COURTYARD,
            # Base/Normal:
            #  HasAnyAbilities(JEDI | SHORTIE | HOVER) is already needed at
            #  "Inside Palace -> After Collapsed Floor In Palace"
            # Moderate:
            #  HasAnyAbilities(JEDI | SHORTIE | HOVER | HIGH_JUMP) is already needed at
            #  "Inside Palace -> After Collapsed Floor In Palace"
            True_(),
            # Hover/jump from the platform that lifts into the air, or take the chute behind it.
            er_rule=HasAnyAbilities(JEDI | SHORTIE | HOVER | HIGH_JUMP),
            pickup_name="m_pup2",
        ),
        "Courtyard High Minikit": minikit_data(
            R_COURTYARD_AFTER_DESTROYED_BRIDGE,
            logic_options(
                base=HasAbility(JEDI),
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="m_pup1",
        ),
        "Build And Destroy Silver Bricks In Boxes Minikit": minikit_data(
            R_ROOFTOPS,
            # All: CAN_BUILD_BRICKS is needed at "After Collapsed Floor In Palace -> Courtyard".
            CAN_DESTROY_CLOSE_SILVER_BRICKS,
            er_rule=HasAbility(CAN_BUILD_BRICKS) & CAN_DESTROY_CLOSE_SILVER_BRICKS,
            pickup_name="m_pup1",
        ),
        "Minikit On Dining Hall Ledge": minikit_data(
            R_DINING_HALL,
            logic_options(
                # High jump up.
                # Or force the tables, double jump up and then grapple the last part.
                base=Or(
                    HasAbility(HIGH_JUMP),
                    HasAllAbilities(JEDI | GRAPPLE),
                ),
                # Jetpack hover is enough to jump from scenery and hover up the slanted lip to the grapple point.
                # Force Grapple Leap is allowed.
                normal=Or(
                    HasAnyAbilities(HIGH_JUMP | JETPACK),
                    And(
                        HasAbility(JEDI),
                        HasAbility(GRAPPLE) | Extra.FORCE_GRAPPLE_LEAP.has(),
                    ),
                ),
                # Astromech hover from the rail along the steps can get to the alcove next the alcove with the grapple
                # point, from which another astromech hover can get to the alcove with the grapple point.
                # Jedi can triple jump to get more height than high jump.
                moderate=Or(
                    HasAnyAbilities(HIGH_JUMP | JEDI | JETPACK),
                    HasAllAbilities(HOVER | GRAPPLE),
                ),
            ),
            pickup_name="m_pup1",
        ),
        "Hangar Far Right Minikit": minikit_data(
            R_HANGAR,
            logic_options(
                # Jump up the far left side, then hover across.
                # Or use the jedi blocks to get up to the high up Battle Droid in the middle with two captives, then
                # High Jump up to the upper area.
                # Then walk all the way to the right side to the Minikit.
                base=Or(
                    HasAllAbilities(HOVER | JEDI),
                    HasAllAbilities(HIGH_JUMP | JEDI),
                ),
                # High jump up to the high up battle droid by first jumping from the top of the nearby starfighter.
                normal=Or(
                    HasAllAbilities(HOVER | JEDI),
                    HasAbility(HIGH_JUMP),
                ),
                # Triple jump is higher than high jump.
                moderate=HasAnyAbilities(JEDI | HIGH_JUMP),
            ),
            pickup_name="m_pup2",
        ),
        "Hangar Far Left Minikit": minikit_data(
            R_HANGAR,
            logic_options(
                base=HasAllAbilities(SITH | BOUNTY_HUNTER),
                normal=Or(
                    HasAbility(HIGH_JUMP),
                    CAN_SITH_FORCE & CAN_DESTROY_CLOSE_SILVER_BRICKS,
                ),
                moderate=HasAnyAbilities(JEDI | HIGH_JUMP),
            ),
            er_rule=logic_options(
                # Jedi to move blocks to get to the silver bricks.
                # Bounty hunter to destroy the silver bricks.
                # Build Bricks to build the platform (all Jedi/Sith can build bricks).
                # Sith force to move the platform into position.
                base=CAN_SITH_FORCE & CAN_DESTROY_CLOSE_SILVER_BRICKS,
                # High jump can just jump up to the minikit from the right side, no Jedi needed.
                normal=Or(
                    HasAbility(HIGH_JUMP),
                    CAN_SITH_FORCE & CAN_DESTROY_CLOSE_SILVER_BRICKS,
                ),
                # Triple jump is higher than high jump.
                moderate=HasAnyAbilities(JEDI | HIGH_JUMP),
            ),
            pickup_name="m_pup1",
        )
    },
    power_brick=LocationData(
        R_DINING_HALL,
        HasAbility(JEDI),
    ),
    ridables={
        Character.FLASHSPEEDER: LocationData(R_SPAWN, HasAbility(JEDI)),
        Character.SERVICE_CAR: LocationData(R_HANGAR),
    }
)
