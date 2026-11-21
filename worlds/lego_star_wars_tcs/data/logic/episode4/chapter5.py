from rule_builder.rules import And, Or

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_GRAPPLE,
    CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
    can_jump_distance_rule,
    HAS_IMPERIAL_OR_CAN_WEAR_HAT_AND_GRAPPLE,
    HAS_CAN_WEAR_HAT_AND_GRAPPLE,
)
from ..option_filters import logic_options
from ..rules import (
    HasAbility,
    HasAnyAbilities,
    HasAllAbilities,
    HasAnyCharacterExcept,
    HasAbilityCombination,
)
from ..types import minikit_data, ExitData, ChapterHelper, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_TRASH_COMPACTOR = "Trash Compactor"
R_FIRST_CORRIDOR_AND_PLATFORMING_ROOM = "First Corridor, And Platforming Room"
R_PLATFORMING_ROOM_UPPER_LEFT_AND_SERVICE_CAR = "Platforming Room: Upper Left And Service Car"
R_LARGE_TRASH_COMPACTOR = "Large Trash Compactor"
R_CORRIDOR_AND_TOWER_AFTER_FIRST_IMPERIAL_PANEL = "Corridor And Tower After First Imperial Panel"
R_TOWER_TOP = "Tower Top"
R_AFTER_TOWER_TOP_IMPERIAL_DOOR = "After Tower Top Imperial Door"
R_BIG_GAP_GRAPPLE_SWINGING_ROOM = "Big Gap Grapple Swinging Room"
R_STORMTROOPER_CORRIDOR_CHASE_THROUGH_TO_HANGAR = "Stormtrooper Corridor Chase, through to Hangar"

# C-3PO, run_speed=0.75 can just barely do this.
# One of the destroyable objects covers one of the tiles quite a bit, which makes it difficult for fluttering characters
# to activate, but Watto can still just barely activate the tile (Geonosian can just destroy the object in the way).
_ONE_P_TWO_C_PLATFORMING_ROOM_FLOOR_TILES = HasAnyCharacterExcept(Character.GONK_DROID)

helper = ChapterHelper(
    area=Area.DEATHSTARESCAPE,
    start_region=R_TRASH_COMPACTOR,
)

DEATH_STAR_ESCAPE = helper.make_chapter(
    regions={
        R_TRASH_COMPACTOR: (
            ExitData(
                R_FIRST_CORRIDOR_AND_PLATFORMING_ROOM,
                HasAllAbilities(CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP)
            ),
        ),
        R_FIRST_CORRIDOR_AND_PLATFORMING_ROOM: (
            ExitData(
                R_LARGE_TRASH_COMPACTOR,
                # The level transition appears to be unusable until the panel is used.
                HasAbility(PROTOCOL_PANEL),
                new_level=Level.DEATHSTARESCAPE_D,
            ),
            ExitData(
                R_PLATFORMING_ROOM_UPPER_LEFT_AND_SERVICE_CAR,
                # CAN_PULL_LEVERS is required to reach here, and implies CAN_PUSH_OBJECTS.
                # The worst jump height (0.37) GRAPPLE character can make it to the upper left area with the explosive
                # to push down.
                # Double jump can skip the grappling.
                logic_options(
                    base=HasAbility(GRAPPLE) | HasAbility(CAN_DOUBLE_JUMP),
                    moderate=Or(
                        CAN_GRAPPLE,
                        HasAbility(CAN_DOUBLE_JUMP),
                        HasAbilityCombination(RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44),
                    )
                ),
            ),
        ),
        R_PLATFORMING_ROOM_UPPER_LEFT_AND_SERVICE_CAR: (
            ExitData(
                R_CORRIDOR_AND_TOWER_AFTER_FIRST_IMPERIAL_PANEL,
                logic_options(
                    # Get access to the Service Car, destroy the objects on the floor tiles, then drive over the tiles.
                    base=CAN_DAMAGE_AT_CLOSE_RANGE,
                    # Mouse Droid can activate the tiles all on its own. Droideka can too, but only just. Droideka can
                    # just shoot the objects in the way anyway, so it's not logically relevant.
                    normal=CAN_DAMAGE_AT_CLOSE_RANGE | Extra.EXTRA_TOGGLE.has(),
                    # Walk over the tiles with two players simultaneously (hold up for one player, and hold down for the
                    # other player).
                    moderate=CAN_DAMAGE_AT_CLOSE_RANGE | _ONE_P_TWO_C_PLATFORMING_ROOM_FLOOR_TILES,
                ).and_rule(
                    # todo: You can actually get a Stormtrooper up to the panel by getting them to follow you as you
                    #  grapple across, then de-aggroing a Stormtrooper standing by the panel will get them to use it
                    #  (oil glitch). You will want to make good use of the Power Up's invincibility throughout this.
                    #  https://youtu.be/TCih1jwCBrw?t=509
                    #  Using this strategy requires that you have characters that can push blocks, pull levers, grapple,
                    #  and have a passive character that both players can swap to to de-aggro (technically both players
                    #  dying would achieve the same, but doing so is difficult without a pit to jump in.
                    # Use the Imperial Panel.
                    logic_options(
                        # For carrying a hat across, strictly require grappling with a hat to start with because
                        # CAN_WEAR_HAT_AND_DOUBLE_JUMP cannot get a second hat if they mess up.
                        base=HAS_IMPERIAL_OR_CAN_WEAR_HAT_AND_GRAPPLE,
                        # Allow CAN_WEAR_HAT_AND_DOUBLE_JUMP alone, and just don't mess up, or restart the level if you
                        # do.
                        moderate=HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT_AND_GRAPPLE | CAN_WEAR_HAT_AND_DOUBLE_JUMP),
                        # As with getting to the upper left area of the room, this is just enough jump height and run
                        # speed to make it up the extending platform at its lowest, and then have P2 push the spinner to
                        # extend the platform up, carrying the hat to the panel.
                        hard=Or(
                            HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT_AND_GRAPPLE | CAN_WEAR_HAT_AND_DOUBLE_JUMP),
                            # I think Lobot might be the only character this bit of logic applies to.
                            # Other characters either can grapple, double jump, cannot wear hats, or cannot jump high
                            # enough.
                            And(
                                # Ensure enemies can be killed to prevent losing the hat.
                                CAN_DAMAGE_AT_CLOSE_RANGE,
                                HasAbilityCombination(RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_WEAR_HAT)
                            ),
                        ),
                    ),
                ),
                new_level=Level.DEATHSTARESCAPE_B,
            ),
        ),
        R_LARGE_TRASH_COMPACTOR: (),
        # The corridor through to the bottom of the tower only requires pulling levers and pushing blocks which is
        # required to reach here (pulling levers implies pushing blocks).
        R_CORRIDOR_AND_TOWER_AFTER_FIRST_IMPERIAL_PANEL: (
            ExitData(
                R_TOWER_TOP,
                logic_options(
                    base=CAN_GRAPPLE,
                    moderate=Or(
                        CAN_GRAPPLE,
                        HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                        # Avoid destroying the objects at the bottom of the tower, then Tarpals and Jar Jar can high
                        # jump off them.
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                ),
            ),
        ),
        R_TOWER_TOP: (
            ExitData(
                R_AFTER_TOWER_TOP_IMPERIAL_DOOR,
                logic_options(
                    base=HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT),
                    # todo: Allow triple jump and swap to Mouse Droid to go all the way around the door on the right
                    #  side where the grapple swinging room would be if it was within the same level.
                    # Allow Yoda clipping over the door.
                    hard=HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT) | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                )
            ),
        ),
        R_AFTER_TOWER_TOP_IMPERIAL_DOOR: (
            ExitData(
                R_BIG_GAP_GRAPPLE_SWINGING_ROOM,
                new_level=Level.DEATHSTARESCAPE_C,
            ),
        ),
        R_BIG_GAP_GRAPPLE_SWINGING_ROOM: (
            ExitData(
                R_STORMTROOPER_CORRIDOR_CHASE_THROUGH_TO_HANGAR,
                logic_options(
                    base=HasAllAbilities(GRAPPLE | IMPERIAL) | HAS_CAN_WEAR_HAT_AND_GRAPPLE,
                    # Oil Glitch:
                    # One of the Stormtroopers across the gap is standing in range of the Imperial Panel. If he attempts
                    # to put his weapon away, he will instead activate the panel.
                    # To do this, aggro the enemies in this room, and then de-aggro by either swapping both characters
                    # to passive characters, or have both players die simultaneously.
                    # If this Stormtrooper is killed, reinforcements appear to continue arriving until the Grapple point
                    # is build, so avoid building it until you get this trick, if needed.
                    moderate=CAN_GRAPPLE,
                ),
            ),
        ),
        # Since GRAPPLE is required to reach here, these areas can be the same region.
        R_STORMTROOPER_CORRIDOR_CHASE_THROUGH_TO_HANGAR: (
            ExitData(
                "Chapter Completion",
                logic_options(
                    base=HasAllAbilities(PROTOCOL_PANEL | ASTROMECH_PANEL),
                    # All ASTROMECH_PANEL character can jump this distance, so checking for the panel abilities is
                    # pointless:
                    # - Astromech droids can HOVER, which is superior to all jump distance rules.
                    # - 4-LOM has 0.84 jump distance (same as Captain Panaka).
                    # - IG-88 has 0.92 jump distance.
                    hard=can_jump_distance_rule(Character.CAPTAIN_PANAKA),
                ),
                er_rule=logic_options(
                    # Even the worst jumping GRAPPLE characters can reach and push the object on the right.
                    base=HasAllAbilities(PROTOCOL_PANEL | ASTROMECH_PANEL),
                    # There is a fairly well known trick in this level called Falconless where loading the level
                    # containing the Falcon, then going back to the previous level and moving far enough away to
                    # unload the level containing the Falcon (pre-loading the level even earlier), and then going back
                    # and loading the level containing the Falcon again, the level completion trigger of the Falcon's
                    # door will be active even without needing to raise the Falcon and defeat the enemies.
                    hard=Or(
                        HasAllAbilities(PROTOCOL_PANEL | ASTROMECH_PANEL),
                        # Can make it:
                        # - Captain Tarpals (single-jump) (0.90)
                        # - Captain Panaka (0.84)
                        # Cannot make it:
                        # - Dexter Jettster (0.7666)
                        # - Clone (0.7)
                        # - Ewok (0.69)
                        can_jump_distance_rule(Character.CAPTAIN_PANAKA),
                    ),
                ),
            ),
        ),
    },
    minikits={
        "Destroy Silver Bricks Minikit": minikit_data(
            R_FIRST_CORRIDOR_AND_PLATFORMING_ROOM,
            # The Minikit does not spawn until the silver bricks are destroyed, so Yoda clipping is useless.
            CAN_DESTROY_CLOSE_SILVER_BRICKS,
            pickup_name="m_pup1",
        ),
        "Access Hatch Minikit Beneath Floor Grate": minikit_data(
            R_PLATFORMING_ROOM_UPPER_LEFT_AND_SERVICE_CAR,
            HasAbility(SHORTIE),
            pickup_name="mk_0",
        ),
        "Window Washers Minikit": minikit_data(
            R_CORRIDOR_AND_TOWER_AFTER_FIRST_IMPERIAL_PANEL,
            # CAN_PULL_LEVERS and CAN_BUILD_BRICKS are needed at the start of the chapter, and CAN_PULL_LEVERS implies
            # being able to ride vehicles.
            # HasAbility(CAN_RIDE_VEHICLES),
            pickup_name="pup1",
        ),
        "Sith Side Force Minikit": minikit_data(
            R_CORRIDOR_AND_TOWER_AFTER_FIRST_IMPERIAL_PANEL,
            logic_options(
                base=CAN_SITH_FORCE,
                # Allow Yoda clip. An IMPERIAL character or a character that can wear hats is required to reach here,
                # and Yodas are neither of those, so having a non-yoda character is guaranteed.
                # The sith force bricks have 1-sided collision, so continuing with the level after Yoda Clipping is
                # trivial.
                # You can also Yoda Grab this minikit.
                hard=CAN_SITH_FORCE | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
            ),
            pickup_name="pup2",
        ),
        "Tower High Minikit": minikit_data(
            R_TOWER_TOP,
            logic_options(
                base=HasAbility(JEDI),
                # Triple high jump works too.
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="pup3",
        ),
        "Stormtrooper Chase Start Minikit": minikit_data(
            R_STORMTROOPER_CORRIDOR_CHASE_THROUGH_TO_HANGAR,
            pickup_name="pup4",
        ),
        "Reveal Three Berries Minikit": minikit_data(
            R_STORMTROOPER_CORRIDOR_CHASE_THROUGH_TO_HANGAR,
            pickup_name="m_pup1",
        ),
        "Stormtrooper Ledge Minikit": minikit_data(
            R_STORMTROOPER_CORRIDOR_CHASE_THROUGH_TO_HANGAR,
            logic_options(
                base=HasAbility(JEDI),
                normal=HasAbility(CAN_DOUBLE_JUMP),
                moderate=HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
            ),
            pickup_name="pup3",
        ),
        "Hangar Vader Minikit": minikit_data(
            R_STORMTROOPER_CORRIDOR_CHASE_THROUGH_TO_HANGAR,
            logic_options(
                base=HasAbility(BOUNTY_HUNTER),
                hard=HasAbility(BOUNTY_HUNTER) | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
            ),
            pickup_name="pup2",
        ),
        "Hangar Slide Panel Minikit": minikit_data(
            R_STORMTROOPER_CORRIDOR_CHASE_THROUGH_TO_HANGAR,
            pickup_name="pup1",
        ),
    },
    power_brick=LocationData(
        R_LARGE_TRASH_COMPACTOR,
        HasAbility(JEDI),
    ),
    ridables={
        Character.SERVICE_CAR: LocationData(R_PLATFORMING_ROOM_UPPER_LEFT_AND_SERVICE_CAR),
        Character.GRABBERCONTROL: LocationData(R_CORRIDOR_AND_TOWER_AFTER_FIRST_IMPERIAL_PANEL),
    }
)
