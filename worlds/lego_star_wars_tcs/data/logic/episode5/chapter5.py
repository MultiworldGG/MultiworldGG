from rule_builder.rules import And, Or, True_, False_

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
    HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
    CAN_USE_DEFLECT_BOLTS,
    CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
    HAS_0_53_JUMP_HEIGHT_CHARACTER,
)
from ..option_filters import logic_options, OT_HIGH_JUMP_ENABLED, ot_high_jump_ternary
from ..rules import (
    HasAbility,
    HasAnyAbilities,
    HasAllAbilities,
    HasAbilityExceptCharacters,
    HasAbilityCombination,
)
from ..types import minikit_data, ExitData, ChapterHelper, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN_LANDING_PAD = "Spawn Landing Pad"
R_SPAWN_LANDING_PAD_BRIDGE_CONTROL_PLATFORM = "Spawn Landing Pad Bridge Control Platform"
R_ACROSS_LANDING_PAD_BRIDGE = "Across Landing Pad Bridge"
R_SPAWN_LANDING_PAD_INTERIOR = "Spawn Landing Pad Interior"
R_SPAWN_LANDING_PAD_INTERIOR_CORRIDOR = "Spawn Landing Pad Interior Corridor"
R_SPAWN_LANDING_PAD_INTERIOR_CORRIDOR_BOUNTY_HUNTER_ROOM = "Spawn Landing Pad Interior Corridor Bounty Hunter Room"
R_CARBONITE_CHAMBER = "Carbonite Chamber"
R_CARBONITE_CHAMBER_VADER_DEFEATED = "Carbonite Chamber (Vader Defeated)"
R_CARBONITE_CHAMBER_ACROSS_BRIDGE_VADER_DEFEATED = "Carbonite Chamber Across Bridge (Vader Defeated)"
R_CARBONITE_CHAMBER_ACROSS_BRIDGE = "Carbonite Chamber Across Bridge"
R_FIRST_VADER_CHASE_SECTION = "First Vader Chase Section"
R_FIRST_VADER_CHASE_SECTION_FAN_UPPER_PATH = "First Vader Chase Section Fan Upper Path"
R_FIRST_VADER_CHASE_SECTION_MOVING_PLATFORM = "First Vader Chase Section Moving Platform"
R_FIRST_VADER_CHASE_SECTION_AFTER_MOVING_PLATFORM = "First Vader Chase Section After Moving Platform"
R_FIRST_VADER_CHASE_AFTER_SECOND_FAN = "First Vader Chase After Second Fan"
R_VADER_CHASE_FIRST_FIGHT_ROOM = "Vader Chase First Fight Room"
R_VADER_CHASE_ROUND_WINDOW_ROOM = "Vader Chase Round Window Room"
R_FINAL_VADER_CHASE = "Final Vader Chase"
R_FINAL_VADER_CHASE_PLATFORM_AFTER_FORCE_RAMP = "Final Vader Chase Platform After Force Ramp"
R_FINAL_VADER_FIGHT = "Final Vader Fight"


_HAS_ANY_HATLESS_DIVE_ROLL = Character.has_any(
    Character.LUKE_SKYWALKER_TATOOINE,
    Character.LUKE_SKYWALKER_STORMTROOPER,
    Character.HAN_SOLO,
    Character.HAN_SOLO_STORMTROOPER,
    Character.HAN_SOLO_HOTH,
    Character.HAN_SOLO_SKIFF,
    Character.HAN_SOLO_ENDOR,
    Character.HAN_SOLO_HOOD,
    Character.INDIANA_JONES,
    Character.LANDO_CALRISSIAN,
)


_CAN_DAMAGE_VADER = logic_options(
    # Vader tends to deflect all blaster bolts.
    base=HasAbility(CAN_MELEE),
    # Allow explosions for damaging Vader.
    normal=CAN_DESTROY_CLOSE_SILVER_BRICKS | HasAbility(CAN_MELEE),
    # Allow using blasters only to damage Vader. It seems easiest to shoot him by getting him to start a
    # 'perfect combo' attack.
    moderate=CAN_DAMAGE_AT_CLOSE_RANGE,
)

_helper = ChapterHelper(
    Area.CLOUDCITYTRAP,
    start_region=R_SPAWN_LANDING_PAD,
)


CLOUD_CITY_TRAP = _helper.make_chapter(
    intended_completion_path={
        "base": (
            # Visit and return
            R_SPAWN_LANDING_PAD_BRIDGE_CONTROL_PLATFORM,
            R_SPAWN_LANDING_PAD,
            R_ACROSS_LANDING_PAD_BRIDGE,
            R_SPAWN_LANDING_PAD_INTERIOR,
            R_SPAWN_LANDING_PAD_INTERIOR_CORRIDOR,
            R_CARBONITE_CHAMBER,
            R_CARBONITE_CHAMBER_VADER_DEFEATED,
            R_CARBONITE_CHAMBER_ACROSS_BRIDGE_VADER_DEFEATED,
            R_FIRST_VADER_CHASE_SECTION,
            R_FIRST_VADER_CHASE_SECTION_FAN_UPPER_PATH,
            R_FIRST_VADER_CHASE_SECTION_MOVING_PLATFORM,
            R_FIRST_VADER_CHASE_SECTION_AFTER_MOVING_PLATFORM,
            R_FIRST_VADER_CHASE_AFTER_SECOND_FAN,
            R_VADER_CHASE_FIRST_FIGHT_ROOM,
            R_VADER_CHASE_ROUND_WINDOW_ROOM,
            R_FINAL_VADER_CHASE,
            R_FINAL_VADER_CHASE_PLATFORM_AFTER_FORCE_RAMP,
            R_FINAL_VADER_FIGHT,
        ),
    },
    regions={
        R_SPAWN_LANDING_PAD: (
            ExitData(
                R_SPAWN_LANDING_PAD_BRIDGE_CONTROL_PLATFORM,
                logic_options(
                    base=HasAbility(HOVER),
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM),
                        capped=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                    ),
                ),
            ),
            ExitData(
                R_ACROSS_LANDING_PAD_BRIDGE,
                logic_options(
                    # Force one half of the bridge and activate the other half using the panel, then jump across.
                    base=And(
                        _helper.can_reach_region(R_SPAWN_LANDING_PAD_BRIDGE_CONTROL_PLATFORM),
                        HasAllAbilities(ASTROMECH_PANEL | JEDI),
                    ),
                    normal=Or(
                        # Just hover across the full gap.
                        HasAbility(JETPACK),
                        # Activate the Astromech Panel half of the bridge and then cross.
                        And(
                            _helper.can_reach_region(R_SPAWN_LANDING_PAD_BRIDGE_CONTROL_PLATFORM),
                            HasAbility(ASTROMECH_PANEL),
                            Or(
                                # Hover across or force the other half of the bridge and jump across.
                                HasAnyAbilities(HOVER | JEDI),
                                # Yoda can just force the other half of the bridge.
                                # # Yoda's extra double jump distance is enough to cross.
                                # HAS_ANY_YODA,
                                # High jump characters, except Bodyguard can cross
                                (
                                        HasAbilityExceptCharacters(HIGH_JUMP, Character.GRIEVOUS_BODYGUARD)
                                        & OT_HIGH_JUMP_ENABLED
                                ),
                            ),
                        ),
                        # Only move the Force half of the bridge.
                        HasAllAbilities(JEDI | HOVER),
                    ),
                    moderate=Or(
                        HasAbility(JETPACK),
                        # Activate the Astromech Panel half of the bridge and then cross.
                        And(
                            _helper.can_reach_region(R_SPAWN_LANDING_PAD_BRIDGE_CONTROL_PLATFORM),
                            HasAbility(ASTROMECH_PANEL),
                            # Hover or triple jump across.
                            HasAnyAbilities(HOVER | JEDI | CAN_HIGH_JUMP_SLAM),
                            # There is no need to check for also Forcing the bridge because all JEDI can cross.
                        ),
                        # Only move the Force half of the bridge.
                        And(
                            HasAbility(JEDI),
                            Or(
                                HasAbility(HOVER),
                                ot_high_jump_ternary(
                                    uncapped=Or(
                                        HasAbility(CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                                        Character.GRIEVOUS_BODYGUARD.has(),
                                    ),
                                    # Grievous and Bodyguard cannot make the distance.
                                    capped=HasAbilityExceptCharacters(JEDI, Character.YODA, Character.YODA_GHOST),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
        R_SPAWN_LANDING_PAD_BRIDGE_CONTROL_PLATFORM: (),
        R_ACROSS_LANDING_PAD_BRIDGE: (
            ExitData(
                R_SPAWN_LANDING_PAD_INTERIOR,
                logic_options(
                    base=HasAllAbilities(ASTROMECH_PANEL | CAN_BUILD_BRICKS),
                    # Allow Yoda Ceiling clip.
                    # This clip is a bit more difficult than most because it is easy to overshoot and hit the
                    # return-door instead. Alternatively, you can ceiling clip and then go to the side to start falling
                    # out-of-bounds and then spam jump while under the floor to jump up into the room, though this sort
                    # or out-of-bounds movement is usually reserved for Expert logic.
                    hard=Or(
                        HasAllAbilities(ASTROMECH_PANEL | CAN_BUILD_BRICKS),
                        # Yoda cannot reach here on his own.
                        CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                    ),
                ),
            ),
        ),
        R_SPAWN_LANDING_PAD_INTERIOR: (
            ExitData(
                R_SPAWN_LANDING_PAD_INTERIOR_CORRIDOR,
                logic_options(
                    # Reveal the turret bricks and build them.
                    # Open the door with the turret base and push it into place.
                    # Force the turret top onto the base to complete it.
                    base=HasAllAbilities(JEDI | ASTROMECH_PANEL),
                    # Allow exploding the blocked door.
                    normal=HasAllAbilities(JEDI | ASTROMECH_PANEL) | CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    # Allow Yoda Ceiling clip to bypass the blocked door.
                    # Allow deflecting stormtrooper bolts into the blocked door with Exploding Blaster Bolts active.
                    hard=Or(
                        HasAllAbilities(JEDI | ASTROMECH_PANEL),
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        # Deflect stormtrooper bolts into the blocked door.
                        Extra.EXPLODING_BLASTER_BOLTS.has() & CAN_USE_DEFLECT_BOLTS,
                        # Yoda cannot reach here on his own.
                        CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                    ),
                ),
            ),
        ),
        R_SPAWN_LANDING_PAD_INTERIOR_CORRIDOR: (
            ExitData(
                R_SPAWN_LANDING_PAD_INTERIOR_CORRIDOR_BOUNTY_HUNTER_ROOM,
                logic_options(
                    base=HasAbility(BOUNTY_HUNTER),
                    # Allow Yoda Ceiling clip over the door.
                    hard=HasAbility(BOUNTY_HUNTER) | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                )
            ),
            ExitData(
                R_CARBONITE_CHAMBER,
                logic_options(
                    base=HasAbility(ASTROMECH_PANEL),
                    # Clip over the door. Overshooting the intended door transition and hitting the return-door
                    # transition is pretty easy here.
                    hard=HasAbility(ASTROMECH_PANEL) | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                ),
            ),
        ),
        R_SPAWN_LANDING_PAD_INTERIOR_CORRIDOR_BOUNTY_HUNTER_ROOM: (),
        R_CARBONITE_CHAMBER: (
            ExitData(
                R_CARBONITE_CHAMBER_VADER_DEFEATED,
                HasAbility(ASTROMECH_PANEL) & _CAN_DAMAGE_VADER,
            ),
            ExitData(
                R_CARBONITE_CHAMBER_ACROSS_BRIDGE,
                logic_options(
                    # Expect defeating Vader.
                    base=False_(),
                    # Allow Jetpack, Yoda, Ackbar or High Jump (except Bodyguard).
                    normal=Or(
                        HasAbility(JETPACK),
                        HasAbilityExceptCharacters(HIGH_JUMP, Character.GRIEVOUS_BODYGUARD) & OT_HIGH_JUMP_ENABLED,
                        HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                    ),
                    # Allow triple jumps.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JETPACK | JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(JETPACK | JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                )
            ),
        ),
        R_CARBONITE_CHAMBER_VADER_DEFEATED: (
            ExitData(
                # This is explicitly only using the bridge/crane to cross the gap, so that the logic for carrying the
                # Stormtrooper Helmet is simpler.
                R_CARBONITE_CHAMBER_ACROSS_BRIDGE_VADER_DEFEATED,
                logic_options(
                    # Expect an Astromech Droid so that the P2 AI will activate the bridge, then have P1 double jump
                    # across.
                    base=HasAllAbilities(CAN_BUILD_BRICKS | CAN_RIDE_VEHICLES | ASTROMECH_DROID | CAN_DOUBLE_JUMP),
                    # Use the crane and have P2's AI activate the bridge. Then jump across the bridge. All astromech
                    # droids can hover across to the bridge and then walk up the sloped part of the bridge to make it
                    # all the way across.
                    normal=HasAllAbilities(CAN_BUILD_BRICKS | CAN_RIDE_VEHICLES | ASTROMECH_DROID),
                    # Allow any Astromech Panel user, and use 1P2C (controlling one character at a time, or
                    # simultaneously for Hard+ logic). Cross the gap using the crane instead of the bridge.
                    moderate=Or(
                        HasAllAbilities(CAN_BUILD_BRICKS | CAN_RIDE_VEHICLES | ASTROMECH_PANEL),
                    ),
                ),
            ),
        ),
        R_CARBONITE_CHAMBER_ACROSS_BRIDGE_VADER_DEFEATED: (
            ExitData(
                R_CARBONITE_CHAMBER_ACROSS_BRIDGE,
            ),
            ExitData(
                R_FIRST_VADER_CHASE_SECTION,
                logic_options(
                    # Without an IMPERIAL character, double jump across the gap to the bridge while carrying the helmet.
                    base=HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT_AND_DOUBLE_JUMP),
                    # Allow Lando/Han/Luke to cross the gap to the bridge while wearing a helmet, by using their dive to
                    # get the required distance.
                    normal=Or(
                        HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT_AND_DOUBLE_JUMP),
                        _HAS_ANY_HATLESS_DIVE_ROLL,
                    ),
                    # Without an IMPERIAL character, use 1P2C to move one character wearing the helmet across the gap.
                    # But you can trick one of the Stormtroopers that spawns into activating the Imperial Panel by
                    # swapping to passive characters, or moving far enough away.
                    # moderate=HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT),
                    moderate=True_(),
                ),
                new_level=Level.CLOUDCITYTRAP_C,
            ),
        ),
        R_CARBONITE_CHAMBER_ACROSS_BRIDGE: (
            ExitData(
                R_FIRST_VADER_CHASE_SECTION,
                logic_options(
                    base=HasAbility(IMPERIAL),
                    # Allow extending the bridge without defeating Vader, then carrying a Helmet across.
                    normal=Or(
                        HasAbility(IMPERIAL),
                        HasAllAbilities(ASTROMECH_PANEL | CAN_WEAR_HAT_AND_DOUBLE_JUMP),
                        HasAbility(ASTROMECH_PANEL) & _HAS_ANY_HATLESS_DIVE_ROLL,
                    ),
                    # I could not manage to do a Yoda Ceiling Clip and bypass this door.
                ),
                new_level=Level.CLOUDCITYTRAP_C,
            ),
        ),
        R_FIRST_VADER_CHASE_SECTION: (
            ExitData(
                R_FIRST_VADER_CHASE_SECTION_FAN_UPPER_PATH,
                logic_options(
                    base=HasAbility(JEDI),
                    # Triple jump up.
                    # With OT High Jump enabled, Grievous and Bodyguard can also get up here without a slam, by jumping
                    # onto the moving platform, but that's not logically relevant unless it gets allowed for normal
                    # logic.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                )
            ),
            ExitData(
                R_FIRST_VADER_CHASE_SECTION_AFTER_MOVING_PLATFORM,
                logic_options(
                    # Expect using the upper path.
                    base=False_(),
                    # Allow Jetpack or Yoda/Ackbar's extra distance double jump
                    normal=Or(
                        HasAbility(JETPACK),
                        (HasAbilityExceptCharacters(HIGH_JUMP, Character.GRIEVOUS_BODYGUARD) & OT_HIGH_JUMP_ENABLED),
                        HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                    ),
                    # Allow triple jumps.
                    # Allow all high jumpers even without OT high jump enabled because Tarpals and Jar Jar can actually
                    # just barely make the jump across.
                    moderate=HasAnyAbilities(JETPACK | JEDI | HIGH_JUMP),
                )
            )
        ),
        R_FIRST_VADER_CHASE_SECTION_FAN_UPPER_PATH: (
            ExitData(
                R_FIRST_VADER_CHASE_SECTION_MOVING_PLATFORM,
                # The panel is actually below, but is always reachable from here.
                HasAbility(ASTROMECH_PANEL),
            ),
        ),
        R_FIRST_VADER_CHASE_SECTION_MOVING_PLATFORM: (
            ExitData(
                # Just drop down.
                R_FIRST_VADER_CHASE_SECTION_AFTER_MOVING_PLATFORM,
            ),
            ExitData(
                R_FIRST_VADER_CHASE_AFTER_SECOND_FAN,
                logic_options(
                    # Definitely not the intended route.
                    base=False_(),
                    # Jump from the moving platform.
                    normal=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JETPACK | CAN_DOUBLE_JUMP),
                        capped=Or(
                            HasAbility(JETPACK),
                            HasAbilityExceptCharacters(CAN_DOUBLE_JUMP, Character.GRIEVOUS_BODYGUARD)
                        ),
                    ),
                ),
            )
        ),
        R_FIRST_VADER_CHASE_SECTION_AFTER_MOVING_PLATFORM: (
            ExitData(
                R_FIRST_VADER_CHASE_AFTER_SECOND_FAN,
                logic_options(
                    # Force the fan and float up.
                    base=HasAbility(JEDI),
                    # Allow high jump when enabled; only Grievous and Bodyguard get enough height.
                    normal=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                        capped=HasAbility(JEDI),
                    ),
                    # Allow triple jump.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                )
            ),
        ),
        R_FIRST_VADER_CHASE_AFTER_SECOND_FAN: (
            ExitData(
                R_VADER_CHASE_FIRST_FIGHT_ROOM,
                logic_options(
                    # Activate the elevator using the astromech panel.
                    base=HasAbility(ASTROMECH_PANEL),
                    # Allow high jump when enabled.
                    normal=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(ASTROMECH_PANEL | HIGH_JUMP),
                        capped=HasAbility(ASTROMECH_PANEL),
                    ),
                    # Allow triple jump
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(ASTROMECH_PANEL | HIGH_JUMP | JEDI),
                        capped=HasAnyAbilities(ASTROMECH_PANEL | CAN_HIGH_JUMP_SLAM | JEDI),
                    ),
                    # Allow double jump off the collision of the Astromech Panel. This is barely possible with Jar Jar
                    # and Tarpals and fairly easy with Ackbar, who are the only characters this is relevant for. I did
                    # not check if it was possible for other double-jump characters because they can all triple jump.
                    hard=HasAnyAbilities(ASTROMECH_PANEL | CAN_DOUBLE_JUMP),
                ),
            ),
        ),
        R_VADER_CHASE_FIRST_FIGHT_ROOM: (
            ExitData(
                R_VADER_CHASE_ROUND_WINDOW_ROOM,
                logic_options(
                    base=HasAllAbilities(JEDI | ASTROMECH_DROID),
                    # Allow any Double Jump character instead of just Jedi.
                    # Allow any ASTROMECH_PANEL user instead of relying on P2's AI to activate the right panel. Build
                    # the spinner and platform and move the elevator half-way up so that two double jumps can be
                    # performed to reach the panel.
                    # Allow high jump up to Vader, skipping the ASTROMECH_PANEL requirement.
                    normal=And(
                        _CAN_DAMAGE_VADER,
                        Or(
                            HasAllAbilities(CAN_DOUBLE_JUMP | ASTROMECH_PANEL | CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS),
                            CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                        ),
                    ),
                    # Allow triple jumps up to Vader.
                    # Allow Gamorrean Guard/Super Gonk, who can jump up the 'steps' despite not having a double jump.
                    moderate=And(
                        _CAN_DAMAGE_VADER,
                        Or(
                            HasAllAbilities(CAN_DOUBLE_JUMP | ASTROMECH_PANEL | CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS),
                            ot_high_jump_ternary(
                                uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                                capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                            ),
                            HAS_0_53_JUMP_HEIGHT_CHARACTER & HasAbility(ASTROMECH_PANEL),
                        ),
                    ),
                ),
                new_level=Level.CLOUDCITYTRAP_B,
            ),
        ),
        R_VADER_CHASE_ROUND_WINDOW_ROOM: (
            ExitData(
                # Note: For logic purposes, the area with the two respawning Stormtroopers is considered to be part of
                # the Final Vader Chase region.
                R_FINAL_VADER_CHASE,
                logic_options(
                    base=HasAnyAbilities(JEDI | HOVER),
                    normal=ot_high_jump_ternary(
                        uncapped=Or(
                            # CAN_TRIPLE_JUMP_GREAT_DISTANCE includes Grievous, but not Bodyguard.
                            HasAnyAbilities(JEDI | HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                            Character.has_any(Character.JAR_JAR_BINKS, Character.CAPTAIN_TARPALS),
                        ),
                        capped=HasAnyAbilities(JEDI | HOVER),
                    ),
                    # Allow triple jump (this lets Bodyguard and Grievous cross the gap even when OT high jump is not
                    # enabled.
                    # Allow Jar Jar/Tarpals even without OT high jump because their increased movement speed is enough.
                    moderate=HasAnyAbilities(JEDI | HOVER | HIGH_JUMP),
                # Vader will not jump through the window unless you are a character he feels threatened by. With only a
                # Ghost Jedi and an Astromech droid, you cannot proceed any further in the level.
                # The 'door' to the next part of the level appears to not spawn until Vader jumps through the window, so
                # ceiling clipping to get past the window with Yoda (Ghost) is not useful.
                ).and_rule(HasAbility(CAN_AGGRAVATE_ENEMIES)),
            ),
        ),
        R_FINAL_VADER_CHASE: (
            ExitData(
                R_FINAL_VADER_CHASE_PLATFORM_AFTER_FORCE_RAMP,
                logic_options(
                    base=HasAbility(JEDI),
                    # Allow JETPACK.
                    normal=HasAnyAbilities(JEDI | JETPACK),
                    # Allow triple jump.
                    # Allow Tarpals and Jar Jar who can just make the jump due to their higher base movement speed.
                    moderate=HasAnyAbilities(JEDI | JETPACK | HIGH_JUMP),
                ),
            ),
        ),
        R_FINAL_VADER_CHASE_PLATFORM_AFTER_FORCE_RAMP: (
            ExitData(
                R_FINAL_VADER_FIGHT,
                logic_options(
                    # Prevent getting stuck and having to restart.
                    base=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(ASTROMECH_PANEL | HIGH_JUMP),
                        capped=HasAbility(ASTROMECH_PANEL),
                    ),
                    # Allow hovering across because it is easy to not get stuck when hovering across.
                    normal=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(ASTROMECH_PANEL | HIGH_JUMP | HOVER),
                        capped=HasAnyAbilities(ASTROMECH_PANEL | HOVER),
                    ),
                    # Allow triple jump.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(ASTROMECH_PANEL | HOVER | JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(ASTROMECH_PANEL | HOVER | JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
            ),
        ),
        R_FINAL_VADER_FIGHT: (
            # You must be able to fight Vader to reach here, so no requirements are needed.
            ExitData("Chapter Completion"),
        ),
    },
    minikits={
        "Minikit Around Corner After Bridge": minikit_data(
            R_ACROSS_LANDING_PAD_BRIDGE,
            logic_options(
                base=HasAbility(HOVER),
                # Allow high jump with double jump.
                # Allow Yodas/Ackbar with their better double jump distance.
                normal=ot_high_jump_ternary(
                    uncapped=HasAbility(HOVER) | HasAbilityExceptCharacters(HIGH_JUMP, Character.GRIEVOUS_BODYGUARD),
                    capped=HasAbility(HOVER),
                ) | HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                # Allow triple jumps.
                moderate=ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(HOVER | HIGH_JUMP | JEDI),
                    capped=HasAnyAbilities(HOVER | CAN_HIGH_JUMP_SLAM | JEDI),
                ),
            ),
            pickup_name="m_pup1",
        ),
        "Bounty Hunter Panel Room Minikit": minikit_data(
            R_SPAWN_LANDING_PAD_INTERIOR_CORRIDOR_BOUNTY_HUNTER_ROOM,
            pickup_name="pup1",
        ),
        "Carbonite Chamber Minikit": minikit_data(
            R_CARBONITE_CHAMBER_VADER_DEFEATED,
            CAN_SITH_FORCE,
            pickup_name="pup2",
        ),
        "Vader Chase High Minikit 1": minikit_data(
            R_FIRST_VADER_CHASE_SECTION_FAN_UPPER_PATH,
            logic_options(
                # You need to jump to actually get the character to target the platform.
                base=Or(
                    HasAbility(CAN_DOUBLE_JUMP) & HasAbilityCombination(BLASTER | CAN_JUMP_HEIGHT_0_37),
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                ),
                normal=Or(
                    HasAbility(CAN_DOUBLE_JUMP) & HasAbilityCombination(BLASTER | CAN_JUMP_HEIGHT_0_37),
                    # Explosions work instead of blasters.
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    ot_high_jump_ternary(
                        uncapped=HasAbility(HIGH_JUMP),
                        capped=Character.GENERAL_GRIEVOUS.has(),
                    ),
                    # Double jump + slam under the minikit to collect it.
                    # Alternatively, super jedi slam hits the platform.
                    # todo?: The Stud Magnet logic and the specific logic for General Grievous maybe should not be in
                    #  Normal logic?
                    And(
                        HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                        Extra.has_any(Extra.STUD_MAGNET, Extra.SUPER_JEDI_SLAM),
                    ),
                ),
                moderate=Or(
                    HasAbility(CAN_DOUBLE_JUMP) & HasAbilityCombination(BLASTER | CAN_JUMP_HEIGHT_0_37),
                    # Explosions work instead of blasters.
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
            ),
            pickup_name="pup3",
        ),
        "Vader Chase High Minikit 2": minikit_data(
            R_FIRST_VADER_CHASE_AFTER_SECOND_FAN,
            logic_options(
                # Expect activating the elevator and then hovering across to the minikit.
                base=HasAllAbilities(ASTROMECH_PANEL | HOVER),
                # Allow double jump from below; it's just barely reachable. Slam attacks and/or Stud Magnet make this
                # easier.
                normal=Or(
                    HasAbility(CAN_DOUBLE_JUMP),
                    HasAllAbilities(ASTROMECH_PANEL | HOVER),
                ),
            ),
            pickup_name="pup1",
        ),
        "Access Hatch Caged Minikit": minikit_data(
            R_VADER_CHASE_FIRST_FIGHT_ROOM,
            HasAbility(SHORTIE),
            pickup_name="pup2",
        ),
        "Below Floor Minikit Across From Round Window": minikit_data(
            R_VADER_CHASE_ROUND_WINDOW_ROOM,
            # Shoot P2 if necessary.
            CAN_DESTROY_CLOSE_SILVER_BRICKS,
            pickup_name="m_pup1",
        ),
        "Final Vader Chase Spawn Minikit": minikit_data(
            R_FINAL_VADER_CHASE,
            pickup_name="m_pup2",
        ),
        "Final Vader Chase Platform Towards Camera Minikit": minikit_data(
            R_FINAL_VADER_CHASE_PLATFORM_AFTER_FORCE_RAMP,
            logic_options(
                # Expect good jump distance.
                base=HasAbility(CAN_JUMP_DISTANCE_0_92),
                # Allow decent jump distance.
                normal=HasAbility(CAN_JUMP_DISTANCE_0_84),
                # Allow Dexter Jettster (0.7666 jump distance).
                moderate=CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS,
            ),
            pickup_name="mk_0",
        ),
        "Final Vader Chase Imperial Room Minikit": minikit_data(
            R_FINAL_VADER_FIGHT,
            # todo: It's possible to use JETPACK to go around from the right of the panel and grab the minikit as the
            #  jetpack runs out. I did this by accident first try, thinking it could be in Hard logic, but could not
            #  perform the trick since, so maybe this could be Hard logic if someone figures it out, or maybe it should
            #  only be in Expert logic if it is too difficult.
            logic_options(
                base=HasAbility(IMPERIAL),
                # Carry a stormtrooper helmet all the way through the level. Use P2 for any required triple jumps and
                # any other character swaps. Technically any hat-wearing character can do this, but the time and
                # patience to carry the stormtrooper helmet all the way without losing it would suck, so only the Force
                # Ghosts that can wear hats are expected.
                # Vader cannot be tricked into opening the door because his AI doesn't like to go that far towards the
                # door, and even if you push him that far, he only puts his lightsaber away once he returns to his idle
                # position.
                hard=Or(
                    HasAbility(IMPERIAL),
                    Character.has_any(Character.BEN_KENOBI_GHOST, Character.ANAKIN_SKYWALKER_GHOST)
                ),
            ),
            pickup_name="mk_1",
        ),
    },
    power_brick=LocationData(
        R_SPAWN_LANDING_PAD_BRIDGE_CONTROL_PLATFORM,
        logic_options(
            base=CAN_DESTROY_CLOSE_SILVER_BRICKS,
            # Just jump over the silver bricks.
            normal=CAN_DESTROY_CLOSE_SILVER_BRICKS | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
            moderate=Or(
                CAN_DESTROY_CLOSE_SILVER_BRICKS,
                ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                    capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
        )
    ),
    ridables={
        Character.TROOPERCANNON: LocationData(
            R_SPAWN_LANDING_PAD_INTERIOR,
            # Reveal the turret bricks and build them.
            # Open the door with the turret base and push it into place.
            # Force the turret top onto the base to complete it.
            HasAllAbilities(JEDI | ASTROMECH_PANEL),
        ),
        Character.GRABBERCONTROL: LocationData(
            R_CARBONITE_CHAMBER_VADER_DEFEATED,
            # Vader must be defeated to spawn the bricks, and then the crane control must be fully built.
            HasAbility(CAN_BUILD_BRICKS),
        ),
    }
)
