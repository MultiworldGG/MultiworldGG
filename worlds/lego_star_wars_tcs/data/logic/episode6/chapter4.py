from rule_builder.rules import And, Or, True_, False_, Rule

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    CAN_GRAPPLE,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_USE_DEFLECT_BOLTS,
    HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
    CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
    HAS_FLUTTER_CHARACTER,
    CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
)
from ..option_filters import logic_options, OT_HIGH_JUMP_ENABLED, ot_high_jump_ternary
from ..rules import (
    HasAbility,
    HasAnyAbilities,
    HasAllAbilities,
    HasAbilityExceptCharacters,
)
from ..types import minikit_data, ExitData, ChapterHelper, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level
from ...items.character_items import NON_VEHICLE_CHARACTER_TO_ITEM_DATA


from ....character_ability import *

R_SPAWN = "Spawn"
R_AFTER_FIRST_BRIDGE = "After First Bridge"
R_SECOND_BRIDGE_LEVER_PLATFORM = "Second Bridge Lever Platform"
R_AFTER_SECOND_BRIDGE = "After Second Bridge"
R_MINIKIT_PLATFORM_ABOVE_SECOND_BRIDGE = "Minikit Platform Above Second Bridge"
R_ELEVATOR_ACTIVATION_PLATFORM = "Elevator Activation Platform"
R_GROUND_LEVEL_SPAWN = "Ground Level Spawn"
R_BOARDED_UP_MINIKIT_PLATFORM = "Boarded Up Minikit Platform"
R_RIVER_AREA = "River Area"
R_AFTER_SPLIT_PATHS = "After Split Paths"
R_EWOK_BATTLE = "Ewok Battle"
R_BUNKER_ENTRANCE_ROOF = "Bunker Entrance Roof"
R_INSIDE_BUNKER = "Inside Bunker"
R_BUNKER_LEFT_SIDE_STORMTROOPER_BEHIND_WINDOW_DEFEATED = "Bunker Left Side (Stormtrooper Behind Window Defeated)"
R_BUNKER_YELLOW_LEVER_AREA = "Bunker Yellow Lever Area"
R_BUNKER_PURPLE_LEVER_PLATFORM = "Bunker Purple Lever Platform"
R_BUNKER_POWER_BRICK_AREA = "Bunker Power Brick Area"


_CAN_HILL_ROLL_CHARACTERS: tuple[Character, ...] = (
    # Dive roll
    Character.HAN_SOLO,
    Character.HAN_SOLO_ENDOR,
    Character.HAN_SOLO_HOOD,
    Character.HAN_SOLO_HOTH,
    Character.HAN_SOLO_SKIFF,
    Character.HAN_SOLO_STORMTROOPER,
    Character.INDIANA_JONES,
    Character.LANDO_CALRISSIAN,
    Character.LUKE_SKYWALKER_PILOT,
    Character.LUKE_SKYWALKER_STORMTROOPER,
    Character.LUKE_SKYWALKER_TATOOINE,

    # Dive roll (cannot wear hats)
    Character.LUKE_SKYWALKER_HOTH,
    Character.LANDO_PALACE_GUARD,
    Character.BESPIN_GUARD,
    Character.GREEDO,
    Character.BOSSK,
    Character.DENGAR,

    # Flop
    Character.STORMTROOPER,
    Character.BEACH_TROOPER,
    Character.SNOWTROOPER,
    Character.DEATH_STAR_TROOPER,
    Character.TIE_FIGHTER_PILOT,
    Character.SANDTROOPER,

    # Air attack
    Character.IMPERIAL_GUARD,
    # Too difficult for Hard logic.
    # Character.GAMORREAN_GUARD,
)


# todo: Make a function that can take a list of characters and try to produce an optimised rule that checks for
#  abilities to skip needing to check long sublists of that list of characters. This function should consider both the
#  frequency of found abilities in the list of characters, as well as how many characters outside the list also have
#  those abilities.
def _make_has_hill_roll_character() -> Rule:
    common_abilities = ~CharacterAbility.NONE

    for character in _CAN_HILL_ROLL_CHARACTERS:
        data = NON_VEHICLE_CHARACTER_TO_ITEM_DATA[character]
        common_abilities &= data.abilities

    imperial_chars = [c for c in _CAN_HILL_ROLL_CHARACTERS
                      if IMPERIAL in NON_VEHICLE_CHARACTER_TO_ITEM_DATA[c].abilities]
    picked_chars = set(imperial_chars)

    hat_chars = [c for c in _CAN_HILL_ROLL_CHARACTERS
                 if c not in picked_chars
                 and CAN_WEAR_HAT_AND_GRAPPLE in NON_VEHICLE_CHARACTER_TO_ITEM_DATA[c].abilities]
    picked_chars.update(hat_chars)

    other_chars = [c for c in _CAN_HILL_ROLL_CHARACTERS if c not in picked_chars]

    return And(
        HasAllAbilities(common_abilities),
        Or(
            HasAbility(CAN_WEAR_HAT_AND_GRAPPLE) & Character.has_any(*hat_chars),
            # todo?: The automatic EXTRA_TOGGLE logic is going to pick up on this HasAbility(IMPERIAL), and auto-add the
            #  extra toggle rule to become `HasAbility(IMPERIAL) | Extra.EXTRA_TOGGLE.has()`, which is redundant here.
            #  Maybe there could be some attribute on an ability rule that disables auto-adding extra-toggle logic.
            HasAbility(IMPERIAL) & Character.has_any(*imperial_chars),
            Character.has_any(*other_chars),
        ),
    ) | Extra.EXTRA_TOGGLE.has()

_HAS_HILL_ROLL_CHARACTER = _make_has_hill_roll_character()
"""Dive-roll/flop characters can perform the "Hill Roll" speedrun strategy towards the start of Level.ENDORBATTLE_B."""


_helper = ChapterHelper(
    area=Area.ENDORBATTLE,
    start_region=R_SPAWN,
)

THE_BATTLE_OF_ENDOR = _helper.make_chapter(
    intended_completion_path={
        "base": (
            R_AFTER_FIRST_BRIDGE,
            R_SECOND_BRIDGE_LEVER_PLATFORM,
            R_AFTER_SECOND_BRIDGE,
            R_ELEVATOR_ACTIVATION_PLATFORM,
            R_GROUND_LEVEL_SPAWN,
            R_RIVER_AREA,
            R_AFTER_SPLIT_PATHS,
            R_EWOK_BATTLE,
            R_BUNKER_ENTRANCE_ROOF,
            R_INSIDE_BUNKER,
            # Visit and return.
            R_BUNKER_YELLOW_LEVER_AREA,
            R_INSIDE_BUNKER,
            # Visit and return
            R_BUNKER_PURPLE_LEVER_PLATFORM,
            R_INSIDE_BUNKER,
        ),
    },
    regions={
        R_SPAWN: (
            ExitData(
                R_AFTER_FIRST_BRIDGE,
                logic_options(
                    base=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(SHORTIE | HIGH_JUMP),
                        capped=HasAbility(SHORTIE),
                    ),
                    # Allow extra distance double jump.
                    # Allow Jetpack hover.
                    # Allow jumping onto the fence, and then hovering across.
                    normal=Or(
                        ot_high_jump_ternary(
                            uncapped=HasAnyAbilities(SHORTIE | HIGH_JUMP),
                            capped=HasAbility(SHORTIE),
                        ),
                        HasAllAbilities(CAN_JUMP_HEIGHT_0_37 | HOVER),
                        HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                    ),
                    # Allow triple jump.
                    # Allow using early objects that are lower, to hover onto, and then hover onto the fence.
                    # Allow Tarpals and Jar Jar without OT high jump that can barely cross the gap.
                    moderate=Or(
                        ot_high_jump_ternary(
                            uncapped=HasAnyAbilities(SHORTIE | HOVER | JEDI | HIGH_JUMP),
                            capped=Or(
                                HasAnyAbilities(SHORTIE | HOVER| JEDI | CAN_HIGH_JUMP_SLAM),
                                Character.has_any(Character.JAR_JAR_BINKS, Character.CAPTAIN_TARPALS),
                            ),
                        ),
                        HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                    ),
                ),
            ),
        ),
        R_AFTER_FIRST_BRIDGE: (
            ExitData(
                R_SECOND_BRIDGE_LEVER_PLATFORM,
                logic_options(
                    base=HasAllAbilities(PROTOCOL_PANEL | CAN_BUILD_BRICKS) & CAN_GRAPPLE,
                    normal=Or(
                        HasAbility(CAN_DOUBLE_JUMP),
                        HasAllAbilities(PROTOCOL_PANEL | CAN_BUILD_BRICKS) & CAN_GRAPPLE,
                    ),
                ),
            ),
        ),
        R_SECOND_BRIDGE_LEVER_PLATFORM: (
            ExitData(
                R_AFTER_SECOND_BRIDGE,
                logic_options(
                    base=HasAbility(CAN_PULL_LEVERS),
                    normal=HasAnyAbilities(CAN_PULL_LEVERS | CAN_DOUBLE_JUMP | HOVER),
                ),
            ),
            ExitData(
                R_MINIKIT_PLATFORM_ABOVE_SECOND_BRIDGE,
                HasAbility(JEDI),
            )
        ),
        R_AFTER_SECOND_BRIDGE: (
            ExitData(
                R_MINIKIT_PLATFORM_ABOVE_SECOND_BRIDGE,
                # JEDI is not considered by this entrance because all difficulties that can use JEDI to traverse this
                # entrance can preferably traverse
                # R_SECOND_BRIDGE_LEVER_PLATFORM -> R_MINIKIT_PLATFORM_ABOVE_SECOND_BRIDGE instead.
                logic_options(
                    # Expect R_SECOND_BRIDGE_LEVER_PLATFORM -> R_MINIKIT_PLATFORM_ABOVE_SECOND_BRIDGE.
                    base=False_(),
                    # Jar Jar and Tarpals cannot make it without standing on the torch.
                    normal=HasAbility(CAN_HIGH_JUMP_SLAM) & OT_HIGH_JUMP_ENABLED,
                    # Allow Jar Jar and Tarpals.
                    # Allow triple jumps.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAbility(HIGH_JUMP),
                        capped=HasAbility(CAN_HIGH_JUMP_SLAM),
                    ),
                )
            ),
            ExitData(
                R_ELEVATOR_ACTIVATION_PLATFORM,
                logic_options(
                    base=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(SHORTIE | HIGH_JUMP),
                        capped=HasAbility(SHORTIE)
                    ),
                    # Stand on the sliding object to get enough height to double jump up.
                    # Some of the destroyable objects can also be used to get enough height.
                    # If you fall down from the upper area after pulling the lever, you cannot jump back up the same
                    # way, and will have to restart. So, make sure to push the object into the slot, to activate the
                    # elevator, before falling off.
                    normal=HasAnyAbilities(SHORTIE | CAN_DOUBLE_JUMP),
                    # Allow jumping onto the right torch with Gamorrean Guard and then jumping to the platform.
                    moderate=HasAnyAbilities(SHORTIE | CAN_DOUBLE_JUMP) | Character.GAMORREAN_GUARD.has(),
                )
            ),
        ),
        R_MINIKIT_PLATFORM_ABOVE_SECOND_BRIDGE: (),
        R_ELEVATOR_ACTIVATION_PLATFORM: (
            ExitData(
                R_GROUND_LEVEL_SPAWN,
                # There is an object here that cannot be destroyed with basic melee attacks, but it doesn't actually
                # block pushing the object.
                # There is only actually one destroyable object that blocks the path of the pushing object.
                logic_options(
                    # Expect destroying all the objects for Base logic.
                    base=CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE & HasAllAbilities(CAN_PUSH_OBJECTS | CAN_PULL_LEVERS),
                    # Allow deflecting bolts from the Scout-Troopers/Stormtroopers, and only destroying the one object
                    # that actually blocks the path.
                    moderate=And(
                            CAN_DAMAGE_AT_CLOSE_RANGE | CAN_USE_DEFLECT_BOLTS,
                        HasAllAbilities(CAN_PUSH_OBJECTS | CAN_PULL_LEVERS),
                    ),
                ),
                new_level=Level.ENDORBATTLE_B,
            ),
        ),
        # From this point, being able to push objects and pull levers is required.
        R_GROUND_LEVEL_SPAWN: (
            ExitData(
                R_BOARDED_UP_MINIKIT_PLATFORM,
                logic_options(
                    base=CAN_GRAPPLE & HasAbility(CAN_BUILD_BRICKS),
                    # Allow high jumping up by jumping from on top of one of the destroyable plants.
                    normal=Or(
                        CAN_GRAPPLE & HasAbility(CAN_BUILD_BRICKS),
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                    moderate=Or(
                        CAN_GRAPPLE & HasAbility(CAN_BUILD_BRICKS),
                        ot_high_jump_ternary(
                            uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                            capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                        ),
                    ),
                ),
            ),
            ExitData(
                R_RIVER_AREA,
                # CAN_PUSH_OBJECTS and CAN_PULL_LEVERS are strictly required to reach here.
                logic_options(
                    base=Or(
                        HasAllAbilities(CAN_DOUBLE_JUMP),
                        # Destroy the plants to reveal the spinner bricks.
                        # Build the spinner.
                        # Push the spinner to raise the platform.
                        # Jump onto the platform and use the access hatch.
                        # Walk onto the button.
                        # Have P2's AI use the grapple point and pull the lever.
                        # Warning: The game incorrectly thinks General Grievous, and potentially some other characters,
                        #          can use this lever, which they cannot. This can sort of soft lock a player if the
                        #          character P2 uses to grapple cannot pull levers (IG-88/4-LOM) and then has to swap to
                        #          a different character.
                        And(
                            # The plants cannot be destroyed with basic melee attacks.
                            CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                            HasAllAbilities(CAN_BUILD_BRICKS | SHORTIE | GRAPPLE),
                        ),
                    ),
                    # Allow double jumping onto the lever, then double jumping over the log gate.
                    normal=Or(
                        HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                        # Destroy the plants to reveal the spinner bricks.
                        # Build the spinner.
                        # Push the spinner to raise the platform.
                        # Jump onto the platform and use the access hatch.
                        # Walk onto the button.
                        # Have P2's AI use the grapple point and pull the lever.
                        # Warning: The game incorrectly thinks General Grievous, and potentially some other characters,
                        #          can use this lever, which they cannot. This can sort of soft lock a player if the
                        #          character P2 uses to grapple cannot pull levers (IG-88/4-LOM) and then has to swap to
                        #          a different character.
                        And(
                            # The plants cannot be destroyed with basic melee attacks.
                            CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                            HasAllAbilities(CAN_BUILD_BRICKS | SHORTIE | GRAPPLE),
                        ),
                    ),
                ).or_rule(
                    apply_to="hard+",
                    # Flutter up the left hill side, behind the tree with the Stormtroopers and button platform.
                    # Fluttering up the right hull side might be possible, but it is much steeper in sections, which
                    # makes fluttering slower/harder.
                    rule=Or(
                        HAS_FLUTTER_CHARACTER,
                        # Perform the "Hill Roll" speedrun strategy. This is also possible with characters that 'flop'
                        # instead of dive-roll.
                        # https://www.youtube.com/watch?v=ahzhF_OQBTs&t=244s
                        _HAS_HILL_ROLL_CHARACTER,
                    ),
                ),
            ),
        ),
        R_BOARDED_UP_MINIKIT_PLATFORM: (),
        R_RIVER_AREA: (
            ExitData(
                R_AFTER_SPLIT_PATHS,
                logic_options(
                    strict=False,
                    # The cover of the Protocol Panel needs to be destroyed, which requires any close-range attack,
                    # which happens to be strictly required to reach here.
                    # CAN_PULL_LEVERS is also required here, but is strictly required to reach here.
                    base=HasAllAbilities(SHORTIE | PROTOCOL_PANEL),
                ).ror_rule(
                    # Moderate logic can now control both P1 and P2, just not simultaneously, alternatively, some cases
                    # allow for skipping the buttons entirely, from which a P2 drop-in is unnecessary.
                    apply_to="moderate+",
                    # Skip the log gates entirely, by triple jumping over them.
                    # Skip the first log gate entirely, by jumping from one of the destroyable plants, or from the cover
                    # of the Protocol Panel and JETPACK hover over the first gate. Skipping the first gate allows for
                    # the P2 drop-in to teleport them to P1 at the buttons.
                    # The first log gate can actually be skipped with any DOUBLE_JUMP character by jumping on top of the
                    # 'lamp' to the left of the Protocol Panel, then to the top of the first gate, and then to the
                    # buttons. If the jump from the top of the first gate to the second set of buttons is missed, all
                    # DOUBLE_JUMP characters can actually make it up to the second set of buttons by hugging the right
                    # wall.
                    rule=HasAnyAbilities(JETPACK | CAN_DOUBLE_JUMP),
                ).or_rule(
                    apply_to="hard+",
                    # Around the far right side of the right path, you can flutter over all the slippery terrain and
                    # around the extended collision box of the second gate on the right path.
                    rule=HAS_FLUTTER_CHARACTER,
                ).or_rule(
                    apply_to="normal",
                    # P2's AI will only follow as a SHORTIE, or as a GRAPPLE, after pulling the lever, and dropping in
                    # P2 won't be able to teleport them to P1 if the player has activated the Protocol Panel because P2
                    # will still be on-screen, so Normal logic also needs to require SHORTIE, OT High Jump alone is not
                    # sufficient.
                    rule=HasAllAbilities(SHORTIE | HIGH_JUMP) & OT_HIGH_JUMP_ENABLED,
                ),
                # Expert has a fancy 1P2C 'double jump' strategy using one player to boost up the other player,
                # which can be used to go past the right side with characters that cannot double jump/hover/flutter.
            ),
        ),
        R_AFTER_SPLIT_PATHS: (
            ExitData(
                R_EWOK_BATTLE,
                new_level=Level.ENDORBATTLE_C,
            ),
        ),
        # Being able to push blocks and damage up close are strictly required to reach here.
        # All characters that can push blocks can also ride vehicles. This means that all characters here can use the
        # Ewok catapult to destroy the first barricade, then fight the AT-ST and use it to destroy the second barricade.
        # This means the entire ground-level outside the bunker can be one big region.
        R_EWOK_BATTLE: (
            ExitData(
                R_BUNKER_ENTRANCE_ROOF,
                logic_options(
                    strict=False,
                    # Shoot the barricade around the platform with the button.
                    # Jump out of the AT-ST onto the platform and stand on the button.
                    # P2's AI will grapple up and pull the lever to spawn the bricks for the next grapple point.
                    # Build the next grapple point.
                    # Grapple up to the next platform, and then grapple across to the top of the bunker.
                    base=CAN_GRAPPLE & HasAbility(CAN_BUILD_BRICKS),
                    # Allow triple jump.
                    # Allow "Paul Skip". Stand against the right wall of the bunker entrance, up to near where the
                    # slippery terrain begins. P2's AI will start pathfinding to the top of the bunker, teleporting
                    # whenever a grapple point would be required. The AI will *not* use Force Grapple Leap. The AI will
                    # *not* swap to Extra Toggle characters if they are your only GRAPPLE characters, but you can swap
                    # P2 to an Extra Toggle GRAPPLE character in advance.
                    # JEDI covers the Yodas from HAS_EXTRA_DISTANCE_DOUBLE_JUMP, and GRAPPLE covers ADMIRAL_ACKBAR.
                    moderate=Or(
                        ot_high_jump_ternary(
                            uncapped=HasAnyAbilities(GRAPPLE | JEDI | HIGH_JUMP),
                            capped=HasAnyAbilities(GRAPPLE | JEDI | CAN_HIGH_JUMP_SLAM),
                        ),
                        # Since GRAPPLE alone is enough due to Paul Skip, expand out the JEDI side of CAN_GRAPPLE.
                        HasAllAbilities(JEDI | CAN_BUILD_BRICKS) & Extra.FORCE_GRAPPLE_LEAP.has(),

                    ),
                    # Push an AT-ST up to the raised area outside the bunker, then get in the AT-ST and jump out to get
                    # on top of the bunker.
                    hard=True_(),
                ).ror_rule(
                    apply_to="normal",
                    # Allow high jump off of plants around the bunker directly to the top of the bunker, or high jump to
                    # the platform with the lever, and then high jump across the platforms to the top of the bunker.
                    # Allow extra distance double jump to jump from the platform with the lever to the next platform.
                    rule=CAN_ORIGINAL_TRILOGY_HIGH_JUMP | HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                ),
            ),
        ),
        R_BUNKER_ENTRANCE_ROOF: (
            ExitData(
                R_INSIDE_BUNKER,
                # Destroy the objects on the roof (damaging at close range is strictly required to reach here), build
                # the sliding floor and push the object across and off the roof (pushing blocks is strictly required to
                # reach here). Then build and use the panel.
                HasAllAbilities(CAN_BUILD_BRICKS | ASTROMECH_PANEL),
                # For expert logic, there should be a super jump possible, like in the Story speedrun.
                new_level=Level.ENDORBATTLE_D,
            ),
        ),
        R_INSIDE_BUNKER: (
            ExitData(
                R_BUNKER_YELLOW_LEVER_AREA,
                # CAN_BUILD_BRICKS and ASTROMECH_PANEL are strictly required to reach here.
                logic_options(
                    base=Or(
                        HasAllAbilities(HOVER | SHORTIE),
                        HasAllAbilities(HIGH_JUMP | SHORTIE) & OT_HIGH_JUMP_ENABLED,
                    ),
                    # Allow triple jump to the astromech panel platform.
                    # If it were possible to reach here without ASTROMECH_PANEL, then there is a trick you can do where
                    # you pan up, or pan right, the camera so that where the Access Hatch gets built is off-screen, and
                    # then AI P2 will teleport to the exit of the Access Hatch without needing to activate the panel and
                    # build the access hatch.
                    moderate=HasAbility(SHORTIE) & ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(HIGH_JUMP | JEDI | HOVER),
                        capped=HasAnyAbilities(CAN_HIGH_JUMP_SLAM | JEDI | HOVER),
                    ),
                ).or_rule(
                    # Yoda clip through the ceiling (the ceiling collision is lower than you think, up to about the top
                    # of the silver brick tubes on the right wall).
                    # Getting back out can be difficult, so dropping out and walking away as P2, then dropping P1 back
                    # in (if needed), is recommended.
                    apply_to="hard+",
                    rule=CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                ),
            ),
            ExitData(
                R_BUNKER_PURPLE_LEVER_PLATFORM,
                # Basic melee attacks cannot reveal the 2 hidden buttons
                CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                # Moderate+ can triple jump up, but all triple jump characters have combo-melee attacks and slam
                # attacks, so this is logically irrelevant.
            ),
            ExitData(
                R_BUNKER_LEFT_SIDE_STORMTROOPER_BEHIND_WINDOW_DEFEATED,
                logic_options(
                    strict=False,
                    base=And(
                        # Use the panel to make the Stormtrooper move beneath the explosive.
                        HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT),
                        # Reach the protocol panel.
                        Or(
                            CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                            _helper.can_reach_region(R_BUNKER_PURPLE_LEVER_PLATFORM) & HasAbility(HOVER),
                        ),
                        # Activate the panel.
                        HasAbility(PROTOCOL_PANEL),
                    ),
                ).or_rule(
                    apply_to="moderate+",
                    rule=Or(
                        HasAbility(IMPERIAL) & Or(
                            # I could not get Exploding Blaster Bolts to work through the window.
                            Extra.SUPER_JEDI_SLAM.has() & HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                            Extra.SUPER_EWOK_CATAPULT.has() & HasAbility(WEAPON_EWOK),
                            Extra.SUPER_THERMAL_DETONATOR.has() & HasAbility(BOUNTY_HUNTER),
                            # Note: Basically guaranteed to die unless Invincibility/Power Up is active.
                            Extra.BOUNTY_HUNTER_ROCKETS.has() & HasAbility(JETPACK),
                            # Barely possible with Astromech droids and Protocol droids. I could not get this to work
                            # with Droideka, who I suspect is too large, so the explosion radius does not reach.
                            logic_options(
                                base=False_(),
                                hard=Extra.SELF_DESTRUCT.has() & HasAbilityExceptCharacters(
                                CAN_SELF_DESTRUCT,Character.DROIDEKA)
                            ),
                        ),
                    ),
                ),
                # todo: Many blaster characters can shoot through this window while angled towards the left, potentially
                #  killing the stormtrooper. This would probably want to be Hard+ logic. Presumably this comes from the
                #  characters holding the blaster in their left hand, where certain animations will move the weapon far
                #  enough to clip through the window. It will be important to check characters using *keyboard* controls
                #  due to keyboard having more limited movement precision.
            ),
            ExitData(
                R_BUNKER_POWER_BRICK_AREA,
                logic_options(
                    # Expect defeating the Stormtrooper and using the Access Hatch that spawns.
                    base=False_(),
                    # Destroy the lower panel that you would need to destroy to push the Sith Force bricks through into
                    # the Power Brick area, then hug the gap where the panel was destroyed. Pan the camera away from
                    # where the Access Hatch spawns and P2's AI will swap to a SHORTIE and then teleport across to the
                    # other side, ignoring the fact that the Access Hatch has not been spawned.
                    # Basic melee attacks cannot destroy this panel.
                    moderate=HasAbility(SHORTIE) & CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                ).ror_rule(
                    # This room has no ceiling. A maximum height triple jump from the Protocol Panel area just barely
                    # gets over the wall.
                    # Yoda's triple jump height can clear the wall much easier.
                    # Triple jumping and swapping to an Astromech droid (has lower gravity) can also make clearing the
                    # wall much easier.
                    # There are also some beams going down into the bottomless pit on the far right of the Protocol
                    # Panel platform. The top of these beams is lower than the ceiling, so triple jumping on top of
                    # their collision is easier, but the collision has no top face, so only the infinitely thin walls of
                    # their collision exists for standing on.
                    # Triple-high-jump is also much easier.
                    # Jumping back out of the Power Brick Area is easier than it may seem because the entire upper wall
                    # is one-way, so you can jump through it. There is a ceiling in the main part of the Power Brick
                    # area, but the ceiling is absent on the far left above the Access Hatch.
                    apply_to="hard+",
                    rule=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM)
                ),
            ),
            ExitData(
                "Chapter Completion",
                # CAN_PULL_LEVERS is strictly required to reach here.
                # CAN_BUILD_BRICKS is strictly required to reach here.
                # Some basic jump height is strictly required to reach here because either good jump height, or a
                # SHORTIE character is strictly required earlier in the level.
                And(
                    # Required to lower the force fields in front of the Green and Purple levers.
                    HasAbility(PROTOCOL_PANEL),
                    _helper.can_reach_region(R_BUNKER_YELLOW_LEVER_AREA),
                    # Only PROTOCOL_PANEL requirement for the Green lever because ASTROMECH_PANEL and basic attacking at
                    # close-range are strictly required to reach here.
                    # No additional requirements for the Blue Lever.
                    _helper.can_reach_region(R_BUNKER_PURPLE_LEVER_PLATFORM),
                    # After all four colored levers are pulled, there are two more levers to pull in the main room, and
                    # then explosives to build in the generator room
                )
                # Without going inside R_BUNKER_YELLOW_LEVER_AREA, if you could somehow aggro the Stormtroopers
                # inside R_BUNKER_YELLOW_LEVER_AREA, and then de-aggro them, they would pull the lever for you, but I
                # don't know how to achieve this.
            ),
        ),
        R_BUNKER_LEFT_SIDE_STORMTROOPER_BEHIND_WINDOW_DEFEATED: (
            ExitData(
                R_BUNKER_POWER_BRICK_AREA,
                HasAbility(SHORTIE),
            ),
        ),
        R_BUNKER_YELLOW_LEVER_AREA: (),
        R_BUNKER_PURPLE_LEVER_PLATFORM: (),
        R_BUNKER_POWER_BRICK_AREA: (),
    },
    minikits={
        "Minikit Left Of Spawn": minikit_data(
            R_SPAWN,
            logic_options(
                # Destroy the crates, build the spinner, push the spinner, then hover across.
                # High Jump directly to the platform if enabled.
                base=Or(
                    CAN_DAMAGE_AT_CLOSE_RANGE & HasAllAbilities(CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS | HOVER),
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                ),
                # Jump on the fence, then double-jump/jetpack-hover across.
                normal=Or(
                    HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                    CAN_DAMAGE_AT_CLOSE_RANGE & HasAllAbilities(CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS | HOVER)
                ),
            ),
            pickup_name="mk_0",
        ),
        "Minikit Behind Wooden Gate": minikit_data(
            R_AFTER_FIRST_BRIDGE,
            logic_options(
                base=Or(
                    HasAllAbilities(CAN_PULL_LEVERS | HOVER | JEDI),
                    HasAllAbilities(CAN_PULL_LEVERS | HIGH_JUMP) & OT_HIGH_JUMP_ENABLED,
                ),
                # Double jump up to the platform from the fence, skipping the HOVER.
                normal=Or(
                    HasAllAbilities(CAN_PULL_LEVERS | JEDI),
                    HasAllAbilities(CAN_PULL_LEVERS | HIGH_JUMP) & OT_HIGH_JUMP_ENABLED,
                ),
                # Allow triple jump with high-jump-slam characters.
                moderate=Or(
                    HasAllAbilities(CAN_PULL_LEVERS | JEDI),
                    ot_high_jump_ternary(
                        uncapped=HasAllAbilities(CAN_PULL_LEVERS | HIGH_JUMP),
                        capped=HasAllAbilities(CAN_PULL_LEVERS | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
            ),
            pickup_name="mk_1",
        ),
        "High Minikit Above Second Bridge": minikit_data(
            R_MINIKIT_PLATFORM_ABOVE_SECOND_BRIDGE,
            pickup_name="mk_2",
        ),
        "Boarded Up Minikit": minikit_data(
            R_BOARDED_UP_MINIKIT_PLATFORM,
            # Destroy the boards blocking access to the minikit.
            CAN_DAMAGE_AT_CLOSE_RANGE,
            pickup_name="mk_1",
        ),
        "Top Of River Minikit": minikit_data(
            R_RIVER_AREA,
            logic_options(
                strict=False,
                base=HasAllAbilities(CAN_BUILD_BRICKS | CAN_RIDE_VEHICLES) & CAN_DAMAGE_AT_CLOSE_RANGE,
            ).ror_rule(
                apply_to="normal+",
                rule=logic_options(
                    base=False_(),
                    # Allow JETPACK.
                    # While flutter characters can fly up the slope without sliding down, flutter characters take some
                    # time to gain height when moving up slopes, so flying too fast will cause them to collide with the
                    # slope and be forced into a sliding animation.
                    normal=HasAbility(JETPACK),
                    # Allow any hover.
                    # Allow good distance triple jump.
                    # Allow flutter, by flying *slowly* up the slope.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                        capped=Or(
                            HasAbility(HOVER),
                            # I am unsure if this jump is possible with Grievous without OT High Jump being enabled. If
                            # the jump is possible, it's probably too difficult for Moderate logic anyway.
                            HasAbilityExceptCharacters(CAN_TRIPLE_JUMP_GREAT_DISTANCE, Character.GENERAL_GRIEVOUS)
                        ),
                    ) | HAS_FLUTTER_CHARACTER,
                ),
            ),
            pickup_name="mk_0",
        ),
        "Platform After Split Paths Minikit": minikit_data(
            R_AFTER_SPLIT_PATHS,
            logic_options(
                # Use the Access Hatch, then Hover across to the platform.
                strict=False,
                base=HasAllAbilities(SHORTIE | HOVER),
            ).ror_rule(
                apply_to="normal+",
                rule=logic_options(
                    base=False_(),
                    # Walk up the cliff a little and double jump up.
                    # You can also hover across from the fence around the right platform, but if you can get up to the
                    # right platform, then you can jump to this minikit's platform directly.
                    normal=HasAbility(CAN_DOUBLE_JUMP),
                    # Also allow walking up the cliff a little and then Jetpack hovering up.
                    moderate=HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                ),
            ),
            pickup_name="mk_2",
        ),
        "Right Minikit Outside Bunker": minikit_data(
            R_EWOK_BATTLE,
            logic_options(
                strict=False,
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAllAbilities(SHORTIE | JEDI | CAN_BUILD_BRICKS),
            ).ror_rule(
                apply_to="normal",
                # High jump off the silver bricks, then high jump to the force platform, and finally to the minikit
                # platform.
                rule=CAN_ORIGINAL_TRILOGY_HIGH_JUMP
            ).ror_rule(
                apply_to="moderate+",
                rule=Or(
                    # Allow triple jump.
                    ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(HIGH_JUMP | JEDI),
                        capped=HasAnyAbilities(CAN_HIGH_JUMP_SLAM | JEDI),
                    ),
                    logic_options(
                        base=False_(),
                        # Allow jumping out of an AT-ST and then Jetpack hovering to the lowest platform, then jetpack
                        # hovering to the second-lowest platform, and finally double up the remaining platforms.
                        moderate=HasAllAbilities(JETPACK | CAN_DOUBLE_JUMP),
                        # Skip the JETPACK requirement by pushing an AT-ST up to the higher area directly outside the
                        # bunker, and then just jumping out of the AT-ST and onto the second-lowest platform.
                        # AT-STs can be pushed up to this higher area by jumping out of them next to the ledge and using
                        # the momentum from falling to push them up onto the higher area. I find this works easiest when
                        # having the AT-ST be side on to the ledge, so that the character jumps out and pushes against
                        # the side of the AT-ST.
                        hard=HasAbility(CAN_DOUBLE_JUMP),
                    )
                ),
            ),
            pickup_name="mk_0",
        ),
        "Left Minikit Outside Bunker": minikit_data(
            R_EWOK_BATTLE,
            # Pushing blocks (implies riding vehicles), damaging up close (also possible by riding AT-ST) are required
            # to reach here, so revealing and pushing the spinner are always possible.
            # All JEDI can build, so that does not need to be checked separately.
            logic_options(
                # Reveal the grapple point and spinner.
                # Build and push the spinner.
                # Grapple to the platform.
                # Force the boulder to raise the platform.
                # Double jump/hover across to the other platform.
                # Stand on the second raisable platform and force the second boulder.
                # Hover across to the next platform.
                # Hover across to the minikit platform.
                base=CAN_GRAPPLE & HasAllAbilities(JEDI | HOVER),
                # Skip the grapple by jumping out of an AT-ST.
                # High jump off the silver bricks without destroying them, and jump to the lower platform by the
                # minikit platform, and then to the minikit platform.
                normal=Or(
                    HasAllAbilities(JEDI | HOVER),
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                ),
                # Allow triple jump.
                # While not logically relevant, with OT High Jump enabled, Jar Jar and Tarpals can also jump directly to
                # the platform with the second force boulder, and then jump across instead of needing hover. Grievous
                # can also make this jump.
                moderate=ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                    capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
                # Use one AT-ST to push a second AT-ST up to the elevated area beneath the Minikit platform. Get into
                # that second AT-ST and then jump out to the Minikit platform.
                hard=True_(),
            ),
            pickup_name="mk_1",
        ),
        "Bunker Minikit After Hatch And Gap": minikit_data(
            R_BUNKER_YELLOW_LEVER_AREA,
            logic_options(
                base=HasAbility(HOVER),
                # Allow triple jumps.
                # Allow High Jump with Jar Jar/Tarpals, which is tight, needing a good amount of coyote time.
                # Standing on the console behind the lever makes it easier to cross with Yoda.
                moderate=ot_high_jump_ternary(
                    # Jar Jar and Tarpals can barely cross.
                    # Grievous and Bodyguard can only cross with a triple jump.
                    uncapped=HasAnyAbilities(JEDI | HOVER | HIGH_JUMP),
                    capped=HasAnyAbilities(JEDI | HOVER | CAN_HIGH_JUMP_SLAM),
                )
            ),
            pickup_name="m_pup1",
        ),
        "Bunker Buildable Minikit": minikit_data(
            R_INSIDE_BUNKER,
            # JEDI is required to force the panels to spawn the bricks.
            # JEDI can slam to damage to upper panels, required to reveal the force panels.
            # CAN_BUILD_BRICKS is strictly required to reach here, though all JEDI can build anyway.
            HasAbility(JEDI),
            pickup_name="MINI06",
        )
    },
    power_brick=LocationData(
        R_BUNKER_POWER_BRICK_AREA,
        logic_options(
            base=CAN_SITH_FORCE,
            # Stand on the right handrail close to the Power Brick, then triple jump to the left to get on top of the
            # wall collision of the left handrail, then double jump over the back wall to get behind the force field in
            # front of the Power Brick.
            # Higher triple jumps (Yoda/swap to astromech droid/triple-high-jump) can make this easier, or even triple
            # jump directly over the back wall from the right handrail in the case of triple-high-jump.
            # todo: Dooku can grab this Power Brick through the force field. Maybe other characters can too and this
            #  could be relevant for Moderate logic? I grabbed this through the forcefield as Ewok...
            hard=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
        ),
    ),
    ridables={
        Character.TRACTOR: LocationData(
            R_RIVER_AREA,
            HasAbility(CAN_BUILD_BRICKS) & CAN_DAMAGE_AT_CLOSE_RANGE,
        ),
        Character.CATAPULT: LocationData(R_EWOK_BATTLE),
        Character.ATST: LocationData(R_EWOK_BATTLE),
    },
)
