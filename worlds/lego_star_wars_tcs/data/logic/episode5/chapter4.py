from rule_builder.rules import And, Or, False_, True_

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_GRAPPLE,
    CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
    HAS_ANY_YODA,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    HAS_FLUTTER_CHARACTER,
    CAN_SITH_FORCE_AND_GRAPPLE,
    can_jump_distance_rule,
    CAN_YODA_CLIP,
    CAN_USE_SELF_DESTRUCT,
    HAS_0_53_JUMP_HEIGHT_CHARACTER,
)
from ..option_filters import logic_options, ot_high_jump_ternary, OT_HIGH_JUMP_ENABLED
from ..rules import (
    HasAbility,
    HasAnyAbilities,
    HasAllAbilities, HasAbilityExceptCharacters, HasAbilityCombination,
)
from ..types import minikit_data, ExitData, ChapterHelper, LocationData, MinikitData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *
from ...items.all_character_items import CHARACTER_TO_ITEM_DATA
from ...items.character_items import NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA

R_SPAWN = "Spawn"
R_SPAWN_SWAMP_ISLAND = "Spawn Swamp Island"
R_UP_STEPS_FROM_SPAWN = "Up Steps From Spawn"
R_RACETRACK = "Racetrack"
R_FIRST_SWAMP_MINIKIT_ISLAND_AND_CHALLENGE_KIT_ISLAND = "First Swamp Minikit Island and Challenge Kit Island"
R_ACROSS_FIRST_SWAMP = "Across First Swamp"
R_FIRST_SWAMP_LAST_AREA_WITH_BRIDGE_PANEL = "First Swamp Last Area With Bridge Panel"
R_SPAWN_ACROSS_SWAMP_FROM_YODAS_HUT = "Spawn Across Swamp From Yoda's Hut"
R_IN_FRONT_OF_YODAS_HUT = "In Front Of Yoda's Hut"
R_YODAS_HUT = "Yoda's Hut"
R_ACROSS_RAFT_TO_SILVER_BRICK_CAVE = "Across Raft To Silver Brick Cave"
R_TRAINING_AREA_START = "Training Area Start"
R_TRAINING_AREA_MIDDLE_ISLAND = "Training Area Middle Island"
R_TRAINING_AREA_END = "Training Area End"
R_POST_TRAINING_AREA = "Post-Training Area"
R_ROOTS_PLATFORMING_END = "Roots Platforming End"
R_CAVE_START = "Cave Start"
R_CAVE_ACROSS_SITH_FORCE_BRIDGE = "Cave: Across Sith Force Bridge"
R_CAVE_AFTER_FIRST_LOWERING_PLATFORMS = "Cave: After First Lowering Platforms"
R_CAVE_UPPER_AREA_AFTER_FIRST_LOWERING_PLATFORMS = "Cave: Upper Area After First Lowering Platforms"
R_CAVE_AFTER_SECOND_LOWERING_PLATFORMS = "Cave: After Second Lowering Platforms"
R_CAVE_UPPER_AREA_WITH_PANEL_AFTER_SECOND_LOWERING_PLATFORMS = \
    "Cave: Upper Area With Panel After Second Lowering Platforms"
R_CAVE_ACCESS_HATCH_EXIT_PLATFORM_AFTER_SECOND_LOWERING_PLATFORMS = \
    "Cave: Access Hatch Exit Platform After Second Lowering Platforms"
R_VADER_FIGHT_AREA = "Vader Fight Area"
R_CAVE_MANY_COLLAPSING_PLATFORMS_ROOM = "Cave: Many Collapsing Platforms Room"
R_FINAL_AREA_SPAWN = "Final Area Spawn"
R_FINAL_AREA_ACROSS_BRIDGE = "Final Area Across Bridge"


_HAS_KAMINOAN = Character.has_any(Character.LAMA_SU, Character.TAUN_WE)

_YODAS_HUT_SHORT_CHARACTERS = {
    Character.YODA,
    Character.YODA_GHOST,
    Character.BOBA_FETT_BOY,
    Character.GONK_DROID,
    Character.PK_DROID,
    Character.JAWA,
    Character.UGNAUGHT,
    Character.PIT_DROID,
}

# The entrance to Yoda's hut only allows short characters.
# The only Extra Toggle character in this chapter is Skeleton, who cannot fit through the hut's entrance.
_CAN_ENTER_YODAS_HUT = HasAnyAbilities(ASTROMECH_DROID | WEAPON_EWOK) | Character.has_any(
    *sorted(_YODAS_HUT_SHORT_CHARACTERS)
)


def _make_can_walk_across_swamp_right_of_yoda_hut():
    # Astromech Droids can go across by design, so are not considered too short to walk across.
    too_short_characters = _YODAS_HUT_SHORT_CHARACTERS | {
        # Ewoks are accounted for through WEAPON_EWOK, which is more performant to check.
        Character.EWOK,
        Character.WICKET,
        # Gamorrean Guard is barely too short to cross, and also too tall to enter Yoda's hut.
        Character.GAMORREAN_GUARD,
    }
    short_characters_abilities_union = CharacterAbility.NONE
    for character in too_short_characters:
        short_characters_abilities_union |= CHARACTER_TO_ITEM_DATA[character].abilities
    #
    non_short_character_abilities = ~CharacterAbility.ALL_VEHICLE_ABILITIES & ~short_characters_abilities_union
    other_non_short_characters = []
    for character, character_data in NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA.items():
        if character in too_short_characters:
            # This character is too short to cross this swamp.
            continue
        if character_data.abilities & non_short_character_abilities != 0:
            # This character has an ability covered by non_short_character_abilities, so does not need to be explicitly
            # checked for.
            continue
        other_non_short_characters.append(character)
    return Or(
        HasAnyAbilities(non_short_character_abilities.simplify_or()),
        Character.has_any(*other_non_short_characters),
        # Skeleton can walk across.
        Extra.EXTRA_TOGGLE.has(),
    )


_CAN_WALK_ACROSS_SWAMP_RIGHT_OF_YODA_HUT = _make_can_walk_across_swamp_right_of_yoda_hut()


# Non-double jump, non-jetpack characters that can cross.
# These characters satisfy HasAbilityCombination(CAN_JUMP_0_44 | CAN_JUMP_DISTANCE_0_84), and are tall enough to not
# drown.
# The penultimate jump requires reasonable jump distance.
# The final jump requires good height.
_JUMP_ACROSS_SWAMP_PLATFORMS_WITHOUT_RAISING_OTHER_CHARACTERS = Character.has_any(
    Character.ADMIRAL_ACKBAR,
    Character.BEACH_TROOPER,
    Character.BESPIN_GUARD,
    Character.BIB_FORTUNA,
    Character.BOSSK,
    Character.CAPTAIN_ANTILLES,
    Character.DEATH_STAR_TROOPER,
    Character.DENGAR,
    Character.GRAND_MOFF_TARKIN,
    Character.GREEDO,
    Character.IG_88,
    Character.IMPERIAL_GUARD,
    Character.IMPERIAL_OFFICER,
    Character.IMPERIAL_SHUTTLE_PILOT,
    Character.IMPERIAL_SPY,
    Character.LANDO_CALRISSIAN,
    Character.LANDO_PALACE_GUARD,
    Character.LOBOT,
    Character.LUKE_SKYWALKER_HOTH,
    Character.LUKE_SKYWALKER_PILOT,
    Character.LUKE_SKYWALKER_TATOOINE,
    Character.PALACE_GUARD,
    Character.PRINCESS_LEIA,
    Character.PRINCESS_LEIA_BESPIN,
    Character.PRINCESS_LEIA_BOUSHH,
    Character.PRINCESS_LEIA_ENDOR,
    Character.PRINCESS_LEIA_HOTH,
    Character.PRINCESS_LEIA_SLAVE,
    Character.REBEL_FRIEND,
    Character.REBEL_PILOT,
    Character.REBEL_TROOPER,
    Character.REBEL_TROOPER_HOTH,
    Character.SANDTROOPER,
    Character.SKIFF_GUARD,
    Character.SNOWTROOPER,
    Character.STORMTROOPER,
    Character.STRANGER_1,
    Character.STRANGER_2,
    Character.TIE_FIGHTER_PILOT,
    Character.TUSKEN_RAIDER,
)

_HARD_CAN_JUMP_ACROSS_SWAMP_PLATFORMS_WITHOUT_RAISING_THEM = (
    # This covers all double jump characters, except Yodas, who drown due to being too short.
    HasAnyAbilities(JETPACK | CAN_TRIPLE_JUMP_GREAT_DISTANCE | HIGH_JUMP),
    # All the other characters.
    _JUMP_ACROSS_SWAMP_PLATFORMS_WITHOUT_RAISING_OTHER_CHARACTERS,
)

helper = ChapterHelper(
    area=Area.DAGOBAH,
    start_region=R_SPAWN,
)

DAGOBAH = helper.make_chapter(
    intended_completion_path={
        "base": (
            R_UP_STEPS_FROM_SPAWN,
            R_ACROSS_FIRST_SWAMP,
            R_FIRST_SWAMP_LAST_AREA_WITH_BRIDGE_PANEL,
            R_SPAWN_ACROSS_SWAMP_FROM_YODAS_HUT,
            R_IN_FRONT_OF_YODAS_HUT,
            R_POST_TRAINING_AREA,
            R_ROOTS_PLATFORMING_END,
            R_CAVE_START,
            R_CAVE_AFTER_FIRST_LOWERING_PLATFORMS,
            R_CAVE_AFTER_SECOND_LOWERING_PLATFORMS,
            R_VADER_FIGHT_AREA,
            R_FINAL_AREA_SPAWN,
            R_FINAL_AREA_ACROSS_BRIDGE,
        ),
    },
    regions={
        R_SPAWN: (
            ExitData(
                R_UP_STEPS_FROM_SPAWN,
                logic_options(
                    # Base logic expects fighting the bats.
                    base=CAN_DAMAGE_AT_CLOSE_RANGE & HasAnyAbilities(CAN_BUILD_BRICKS | CAN_JUMP_HEIGHT_0_37),
                    normal=HasAnyAbilities(CAN_BUILD_BRICKS | CAN_JUMP_HEIGHT_0_37),
                    # Astromechs can get up without building the ramps.
                    moderate=HasAnyAbilities(CAN_BUILD_BRICKS | CAN_BARELY_JUMP),
                ),
            ),
            # # There's nothing here yet that is logically relevant.
            # ExitData(
            #     R_SPAWN_SWAMP_ISLAND,
            #     logic_options(
            #         base=HasAbility(ASTROMECH_DROID),
            #         # Kaminoans are clearly tall enough with their massive 0.62 height.
            #         normal=HasAnyAbilities(ASTROMECH_DROID | HOVER) | HAS_FLUTTER_CHARACTER | _HAS_KAMINOAN,
            #     ).or_rule(
            #         # Allow Super Battle Droid and General Grievous who are less obviously tall enough.
            #         apply_to="moderate+",
            #         rule=Character.has_any(
            #             Character.SUPER_BATTLE_DROID,  # 0.53 height
            #             Character.GENERAL_GRIEVOUS,  # 0.52 height
            #         )
            #     ).or_rule(
            #         # Allow Droideka which looks like it is going to drown. Droideka becomes too short when rolling, so
            #         # you must walk.
            #         # TODO: This is extremely annoying/difficult on keyboard. Either Hard+ logic should expect that the
            #         #  player has a controller available, or there should be separate logic for controlling whether
            #         #  controller-required tricks are allowed.
            #         apply_to="hard+",
            #         rule=Character.DROIDEKA.has(),  # 0.50 height (when walking)
            #     ),
            # ),
        ),
        R_UP_STEPS_FROM_SPAWN: (
            ExitData(
                R_RACETRACK,
                logic_options(
                    base=CAN_SITH_FORCE,
                    # Triple jump over the Sith Force bricks.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
            ExitData(
                R_ACROSS_FIRST_SWAMP,
                logic_options(
                    # All characters that can grapple can destroy the bush to reveal the grapple point.
                    base=CAN_GRAPPLE | HasAbility(ASTROMECH_DROID),
                    # Allow jetpack hover, flutter and kaminoan.
                    normal=CAN_GRAPPLE | HasAbility(HOVER) | HAS_FLUTTER_CHARACTER | _HAS_KAMINOAN,
                    # You can hop across the stones, even Boba Fett (Boy) can make these jumps.
                    # General Grievous/Super Battle Droid can also just walk across the swamp because of how tall they
                    # are.
                    # And double jump characters can jump between shallower parts of the swamp.
                    moderate=HasAbility(CAN_BARELY_JUMP) | Character.SUPER_BATTLE_DROID.has(),
                ).or_rule(
                    # TODO: This is extremely annoying/difficult on keyboard. Either Hard+ logic should expect that the
                    #  player has a controller available, or there should be separate logic for controlling whether
                    #  controller-required tricks are allowed.
                    apply_to="hard+",
                    rule=Character.DROIDEKA.has(),
                ),
            ),
            ExitData(
                R_FIRST_SWAMP_MINIKIT_ISLAND_AND_CHALLENGE_KIT_ISLAND,
                logic_options(
                    base=HasAbility(HOVER),
                    # Stand slightly in the swamp and just double jump to the island.
                    # Yoda cannot stand as deep in the swamp, but can double jump further to make up for this.
                    normal=HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP) | HAS_FLUTTER_CHARACTER,
                )
            ),
        ),
        R_RACETRACK: (
            ExitData(
                R_ACROSS_FIRST_SWAMP,
                # Just walk down.
            ),
        ),
        R_ACROSS_FIRST_SWAMP: (
            ExitData(
                R_RACETRACK,
                logic_options(
                    # "Racetrack -> Across First Swamp" is intended to be 1-way, so even if this is easy with OT High
                    # Jump enabled, Base logic will not consider it.
                    base=False_(),
                    # Allow high jump up.
                    normal=CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    # Allow triple jump up.
                    # Allow jetpack off a nearby destroyable bush.
                    moderate=Or(
                        HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM | JETPACK),
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                )
            ),
            ExitData(
                R_FIRST_SWAMP_MINIKIT_ISLAND_AND_CHALLENGE_KIT_ISLAND,
                logic_options(
                    base=HasAllAbilities(HOVER | CAN_JUMP_HEIGHT_0_37),
                    normal=HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP) | HAS_FLUTTER_CHARACTER,
                ).or_rule(
                    # Imperial Guard, jump distance of 0.92, can make it from the right side after going slightly into
                    # the swamp near the ramp.
                    # todo: There are probably more characters that can make this jump, especially those with dive
                    #  rolls.
                    apply_to="moderate+",
                    rule=can_jump_distance_rule(Character.IMPERIAL_GUARD)
                )
            ),
            ExitData(
                R_FIRST_SWAMP_LAST_AREA_WITH_BRIDGE_PANEL,
                logic_options(
                    base=ot_high_jump_ternary(
                        uncapped=Or(
                            HasAbility(HOVER),
                            HasAbilityExceptCharacters(HIGH_JUMP, Character.GRIEVOUS_BODYGUARD)
                        ),
                        capped=HasAbility(HOVER)
                    ),
                    # Allow any double jump, except bodyguard who cannot get enough distance.
                    # Allow flutter characters that just fly over the swamp.
                    normal=Or(
                        HasAbility(HOVER),
                        HasAbilityExceptCharacters(CAN_DOUBLE_JUMP, Character.GRIEVOUS_BODYGUARD),
                        HAS_FLUTTER_CHARACTER,
                    ),
                    # Allow any double jump because Bodyguard can triple jump.
                    moderate=Or(
                        HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP),
                        HAS_FLUTTER_CHARACTER,
                    )
                ).or_rule(
                    # Allow Kaminoan. The main difficulty is jumping up to this area from the swamp itself because the
                    # swamp is deep around this area. Hugging the left wall allows a Kaminoan to jump and sort of slide
                    # up out of the swamp.
                    apply_to="moderate+",
                    rule=_HAS_KAMINOAN,
                ),
            ),
        ),
        R_FIRST_SWAMP_MINIKIT_ISLAND_AND_CHALLENGE_KIT_ISLAND: (
            ExitData(
                R_FIRST_SWAMP_LAST_AREA_WITH_BRIDGE_PANEL,
                # All of these are considered from the Challenge Kit island.
                # Both islands are the same region because being able to reach the Minikit Island means you can also go
                # from the Minikit Island to the Challenge Kit Island. This region could be split into two later on.
                logic_options(
                    base=HasAbility(HOVER),
                    normal=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP),
                        capped=Or(
                            HasAbility(HOVER),
                            HasAbilityExceptCharacters(CAN_DOUBLE_JUMP, Character.GRIEVOUS_BODYGUARD),
                        ),
                    ) | HAS_FLUTTER_CHARACTER,
                    moderate=HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP) | HAS_FLUTTER_CHARACTER,
                )
            ),
        ),
        R_FIRST_SWAMP_LAST_AREA_WITH_BRIDGE_PANEL: (
            ExitData(
                R_SPAWN_ACROSS_SWAMP_FROM_YODAS_HUT,
                logic_options(
                    base=CAN_DAMAGE_AT_CLOSE_RANGE | HasAbility(CAN_DOUBLE_JUMP),
                    # You can jump sort of through/over the plants on the right hand side.
                    moderate=Or(
                        CAN_DAMAGE_AT_CLOSE_RANGE,
                        # Kaminoan's are too tall to enter the next area...
                        HasAbilityExceptCharacters(CAN_JUMP_HEIGHT_0_37,
                                                   Character.TAUN_WE,
                                                   Character.LAMA_SU)
                    ),
                ),
                new_level=Level.DAGOBAH_B,
            ),
        ),
        R_SPAWN_ACROSS_SWAMP_FROM_YODAS_HUT: (
            ExitData(
                R_IN_FRONT_OF_YODAS_HUT,
                logic_options(
                    base=HasAllAbilities(CAN_BUILD_BRICKS | CAN_DOUBLE_JUMP),
                    # Allow hovering across the platforms, or fluttering across the swamp.
                    normal=Or(
                        HasAllAbilities(CAN_BUILD_BRICKS | CAN_DOUBLE_JUMP),
                        HasAllAbilities(CAN_BUILD_BRICKS | HOVER),
                        HAS_FLUTTER_CHARACTER,
                    ),
                    # With good timing, any character that can jump reasonably well can cross the platforms as they
                    # rise by jumping to the un-raised closest platform, and jumping to the first platform as it rises.
                    # The rest of the platforms are then trivial. Note that failing the jump to the first platform that
                    # rises results in having to restart the level.
                    #
                    # Kaminoans can also just walk through the swamp because they're so tall, but are only considered
                    # for moderate logic because jumping out of the swamp with them is actually quite difficult. The
                    # easiest way is to jump onto the un-raised last platform, and then swap to a character that can
                    # jump better, but it is possible to jump out as a Kaminoan on their own, either from the last,
                    # un-raised platform, or along the left side of the swamp.
                    moderate=Or(
                        And(
                            HasAbility(CAN_BUILD_BRICKS),
                            # Gamorrean Guard is a bit more difficult than others because he has low movement speed, but
                            # exceptional jump height.
                            HasAbilityExceptCharacters(CAN_JUMP_DISTANCE_0_69, Character.GAMORREAN_GUARD),
                        ),
                        HasAllAbilities(CAN_BUILD_BRICKS | HOVER),
                        HAS_FLUTTER_CHARACTER,
                    ),
                    # Allow skipping activating the platforms by just knowing where the platforms are and jumping across
                    # the swamp.
                    hard=Or(
                        # todo: It seems Yoda can cross, by carefully picking which platforms to land on?
                        #  see https://www.twitch.tv/videos/2822300963?t=1h5m10s
                        # Yoda is too short to double jump across without activating the platforms (he drowns), so this
                        # CAN_DOUBLE_JUMP logic is kept.
                        HasAllAbilities(CAN_BUILD_BRICKS | CAN_DOUBLE_JUMP),
                        HasAllAbilities(CAN_BUILD_BRICKS | HOVER),
                        HAS_FLUTTER_CHARACTER,
                        # Jump across *without raising the platforms*.
                        *_HARD_CAN_JUMP_ACROSS_SWAMP_PLATFORMS_WITHOUT_RAISING_THEM,
                    ),
                )
            ),
        ),
        R_IN_FRONT_OF_YODAS_HUT: (
            ExitData(
                R_YODAS_HUT,
                _CAN_ENTER_YODAS_HUT,
                new_level=Level.DAGOBAH_E,
            ),
            ExitData(
                R_ACROSS_RAFT_TO_SILVER_BRICK_CAVE,
                logic_options(
                    base=CAN_SITH_FORCE,
                    normal=CAN_SITH_FORCE | HasAbility(HOVER) | HAS_FLUTTER_CHARACTER,
                    # Reaching here requires a character that can jump well enough to cross the raising platforms
                    # (potentially without raising them), or a character that can hover across the raising platforms.
                    moderate=Or(
                        CAN_SITH_FORCE,
                        HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                        # Flutter characters can also walk across, so don't need to be specified separately.
                        # Kaminoans are also included.
                        _CAN_WALK_ACROSS_SWAMP_RIGHT_OF_YODA_HUT,
                    )
                ),
                er_rule=logic_options(
                    base=CAN_SITH_FORCE,
                    # Allow using JETPACK, ASTROMECH_DROID, 'flutter' or Kaminoan to cross.
                    normal=Or(
                        CAN_SITH_FORCE,
                        HasAnyAbilities(JETPACK | ASTROMECH_DROID),
                        HAS_FLUTTER_CHARACTER,
                        _HAS_KAMINOAN
                    ),
                    # Allow triple jump for distance.
                    # Allow non-short characters that can just walk across this swamp without drowning. Note that
                    # jumping into the swamp tends to cause characters to reduce in height as they land, causing them to
                    # drown, so walking across is necessary. Some character that can cross cannot jump out of the swamp
                    # at the end, so a character that can at least barely jump is required.
                    moderate=Or(
                        CAN_SITH_FORCE,
                        HasAnyAbilities(JETPACK | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                        HAS_FLUTTER_CHARACTER,
                        _CAN_WALK_ACROSS_SWAMP_RIGHT_OF_YODA_HUT & HasAbility(CAN_BARELY_JUMP),
                    ),
                )
            ),
            ExitData(
                R_TRAINING_AREA_START,
                # The area is not blocked in Free Play, so the player can enter it immediately.
                new_level=Level.DAGOBAH_E,
            ),
            ExitData(
                R_POST_TRAINING_AREA,
                logic_options(
                    # Force Yoda's hut into a ramp and then jump up.
                    # Or travel across the swamp as an Astromech Droid
                    base=HasAnyAbilities(JEDI | ASTROMECH_DROID),
                    # Just jump along the side of the rock instead of trying to jump up the highest part where the ramp
                    # goes.
                    # Allow fluttering across the top of the swamp.
                    # Double jump characters can also just double jump up the highest part without forcing the ramp.
                    normal=HasAnyAbilities(ASTROMECH_DROID | CAN_JUMP_HEIGHT_0_37) | HAS_FLUTTER_CHARACTER
                ),
            )
        ),
        R_YODAS_HUT: (),
        R_ACROSS_RAFT_TO_SILVER_BRICK_CAVE: (),
        R_TRAINING_AREA_START: (
            # This entrance is never logically relevant because R_IN_FRONT_OF_YODAS_HUT is always reached first.
            # ExitData(
            #     R_IN_FRONT_OF_YODAS_HUT,
            #     CAN_DESTROY_CLOSE_SILVER_BRICKS,
            #     new_level=Level.DAGOBAH_B,
            # ),
            ExitData(
                R_TRAINING_AREA_MIDDLE_ISLAND,
                logic_options(
                    base=HasAnyAbilities(JEDI | ASTROMECH_DROID),
                    # Allow jetpack hover or flutter
                    normal=HasAnyAbilities(JEDI | HOVER) | HAS_FLUTTER_CHARACTER,
                    # Allow large distance triple jump to as close to the ramp on the middle island as possible.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HOVER | CAN_HIGH_JUMP_SLAM) | HAS_FLUTTER_CHARACTER,
                        # Grievous's bodyguard cannot make it without OT High Jump being enabled.
                        capped=HasAnyAbilities(JEDI | HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE) | HAS_FLUTTER_CHARACTER,
                    ),
                )
            ),
        ),
        R_TRAINING_AREA_MIDDLE_ISLAND: (
            ExitData(
                R_TRAINING_AREA_START,
                logic_options(
                    base=HasAbility(ASTROMECH_DROID),
                    # Allow flutter over the swamp.
                    normal=HasAbility(ASTROMECH_DROID) | HAS_FLUTTER_CHARACTER,
                    # Allow jumping across the un-raised platforms. Yoda just drowns, so he's no good.
                    hard=Or(
                        HasAbility(ASTROMECH_DROID),
                        HasAbilityExceptCharacters(CAN_DOUBLE_JUMP, Character.YODA, Character.YODA_GHOST),
                        HAS_FLUTTER_CHARACTER
                    ),
                ),
            ),
            ExitData(
                R_TRAINING_AREA_END,
                logic_options(
                    # The jump from the final platform to the end is a little tight on worse jumping characters, so
                    # expect 0.84 for base logic.
                    base=HasAnyAbilities(ASTROMECH_DROID | CAN_JUMP_DISTANCE_0_84),
                    # Allow flutter characters.
                    # Ewok (0.69) can jump across.
                    normal=HasAnyAbilities(ASTROMECH_DROID | CAN_JUMP_DISTANCE_0_69) | HAS_FLUTTER_CHARACTER,
                ),
            ),
        ),
        R_TRAINING_AREA_END: (
            # I don't think this entrance will ever be logically relevant, but I'm not fully sure, so it has been left
            # in for now.
            ExitData(
                R_POST_TRAINING_AREA,
                logic_options(
                    base=HasAllAbilities(JEDI | ASTROMECH_PANEL),
                    normal=HasAbility(ASTROMECH_PANEL) & HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                    hard=Or(
                        HasAbility(ASTROMECH_PANEL) & HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                        # Yoda can fit through the gap in the collision above the wood gate and hit the level transition
                        # trigger.
                        # Boba Fett (Boy) is too tall, though Astromech Droids fit.
                        HAS_ANY_YODA,
                        # Triple high jump from the panel and onto the top of the collision of the gate. The gate's
                        # collision does not extend all the way back to the invisible wall around the level, so you can
                        # walk far enough to fall off the collision, and then approach the gate from behind.
                        # The level transition trigger seems to be in a weird position. Bodyguard can just run to the
                        # right and hug the gate to hit it, but Grievous I find needs to triple high jump from the left
                        # side of the gate to hit it.
                        HasAbility(CAN_HIGH_JUMP_SLAM),
                    ),
                ),
                new_level=Level.DAGOBAH_B,
            ),
        ),
        R_POST_TRAINING_AREA: (
            ExitData(
                R_TRAINING_AREA_END,
                # No requirements, just walk in.
                new_level=Level.DAGOBAH_E,
            ),
            ExitData(
                R_ROOTS_PLATFORMING_END,
                logic_options(
                    # Fall into the swamp and go around.
                    base=HasAbility(ASTROMECH_DROID),
                    # Jetpack can jump up to the top platform, then hover across.
                    # Flutter across the swamp.
                    # Walk through the swamp as a kaminoan.
                    # Yoda/Ackbar's double jump distance is enough to cross the gap.
                    # High jumpers can just jump across (when OT high jump is enabled).
                    normal=Or(
                        ot_high_jump_ternary(
                            uncapped=HasAnyAbilities(ASTROMECH_DROID | JETPACK | CAN_DOUBLE_JUMP),
                            # Bodyguard and Grievous cannot jump across without their high jump.
                            capped=Or(
                                HasAnyAbilities(ASTROMECH_DROID | JETPACK),
                                HasAbilityExceptCharacters(CAN_DOUBLE_JUMP,
                                                           Character.GRIEVOUS_BODYGUARD,
                                                           Character.GENERAL_GRIEVOUS),
                            )
                        ),
                        HAS_FLUTTER_CHARACTER,
                        _HAS_KAMINOAN,
                    ),
                    # Allow triple jump for distance.
                    moderate=Or(
                        HasAnyAbilities(ASTROMECH_DROID | JETPACK | CAN_DOUBLE_JUMP),
                        HAS_FLUTTER_CHARACTER,
                        _HAS_KAMINOAN,
                    ),
                ),
            ),
        ),
        R_ROOTS_PLATFORMING_END: (
            ExitData(
                R_CAVE_START,
                CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                new_level=Level.DAGOBAH_D,
            ),
        ),
        R_CAVE_START: (
            ExitData(
                R_CAVE_ACROSS_SITH_FORCE_BRIDGE,
                logic_options(
                    base=CAN_SITH_FORCE,
                    # While Astromech HOVER can cross the gap from the first platform, if the platform is lowered by
                    # mistake, the chapter must be restarted to re-attempt.
                    normal=Or(
                        CAN_SITH_FORCE,
                        HasAllAbilities(CAN_DOUBLE_JUMP | JETPACK),
                    ),
                    # Allow basic HOVER by not messing up and lowering the first platform.
                    # Allow triple jump across. This is possible even after the platform has been lowered.
                    moderate=ot_high_jump_ternary(
                        uncapped=Or(
                            HasAllAbilities(CAN_DOUBLE_JUMP | HOVER),
                            HasAnyAbilities(JEDI | HIGH_JUMP),
                        ),
                        capped=Or(
                            HasAllAbilities(CAN_DOUBLE_JUMP | HOVER),
                            HasAbilityExceptCharacters(CAN_TRIPLE_JUMP_GREAT_DISTANCE, Character.GENERAL_GRIEVOUS),
                        ),
                    ),
                    # Yoda cannot cross alone, and would need to triple jump and then swap to a fast character, e.g.
                    # Droideka. There is curretly no logic for deliberately swapping to a fast moving character after
                    # using a high jumping character to jump high.
                    # hard=???
                ),
            ),
            ExitData(
                R_CAVE_AFTER_FIRST_LOWERING_PLATFORMS,
                logic_options(
                    base=HasAbility(CAN_DOUBLE_JUMP),
                    normal=Or(
                        HasAnyAbilities(CAN_DOUBLE_JUMP | CAN_JUMP_DISTANCE_0_84),
                    ),
                    moderate=Or(
                        HasAbility(CAN_DOUBLE_JUMP),
                        can_jump_distance_rule(Character.DEXTER_JETTSTER),
                    ),
                ),
            ),
        ),
        R_CAVE_ACROSS_SITH_FORCE_BRIDGE: (),
        R_CAVE_AFTER_FIRST_LOWERING_PLATFORMS: (
            ExitData(
                R_CAVE_AFTER_SECOND_LOWERING_PLATFORMS,
                logic_options(
                    base=HasAbility(CAN_DOUBLE_JUMP),
                    normal=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                    moderate=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER | CAN_JUMP_DISTANCE_0_92),
                ),
            ),
            # There is barely logical relevance for this until Blue/Purple Stud Sanity, or full True Jedi logic, is
            # developed (there are two blue studs behind the silver bricks up here, and JETPACK can cross to the exit of
            # the Access Hatch from here.
            ExitData(
                R_CAVE_UPPER_AREA_AFTER_FIRST_LOWERING_PLATFORMS,
                logic_options(
                    base=CAN_GRAPPLE,
                    # Allow high jump.
                    normal=Or(
                        CAN_GRAPPLE,
                        # Avoid destroying one of the plants and high jump from it.
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                    # Allow triple jump.
                    moderate=Or(
                        HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM | GRAPPLE),
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                ),
            ),
        ),
        R_CAVE_UPPER_AREA_AFTER_FIRST_LOWERING_PLATFORMS: (
            ExitData(
                R_CAVE_ACCESS_HATCH_EXIT_PLATFORM_AFTER_SECOND_LOWERING_PLATFORMS,
                logic_options(
                    base=False_(),
                    normal=HasAbility(JETPACK),
                    moderate=HasAnyAbilities(JETPACK | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                    # Jump off the roots to refresh jumps.
                    hard=HasAnyAbilities(JETPACK | CAN_DOUBLE_JUMP),
                )
            ),
        ),
        R_CAVE_AFTER_SECOND_LOWERING_PLATFORMS: (
            ExitData(
                R_CAVE_UPPER_AREA_WITH_PANEL_AFTER_SECOND_LOWERING_PLATFORMS,
                logic_options(
                    base=HasAbility(CAN_DOUBLE_JUMP),
                    # The jump and then jetpack hover can get enough height.
                    normal=HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                    moderate=Or(
                        HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                        # Just barely possible.
                        HAS_0_53_JUMP_HEIGHT_CHARACTER,
                    ),
                ),
            ),
            ExitData(
                R_CAVE_ACCESS_HATCH_EXIT_PLATFORM_AFTER_SECOND_LOWERING_PLATFORMS,
                logic_options(
                    base=HasAbility(SHORTIE),
                    # Triple high jump. Triple jump is just barely possible, but is far more precise than most triple
                    # jumps, so is not being considered for moderate logic.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(SHORTIE | CAN_HIGH_JUMP_SLAM),
                        capped=HasAbility(SHORTIE),
                    ),
                    # The roots just past the platform have glitchy collision, and you can jump up them. Character-swap
                    # upwarps also work beneath these roots.
                    hard=HasAnyAbilities(SHORTIE | CAN_JUMP_HEIGHT_0_37),
                ),
            ),
            ExitData(
                R_VADER_FIGHT_AREA,
                logic_options(
                    # The AI will only use double jump and astromech characters, so that will be considered developer
                    # intended. Jetpack hover is the better version of astromech hover, so that is also allowed, despite
                    # the AI not knowing to use it.
                    base=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                    normal=Or(
                        # The first jump requires distance, the second jump (from the platform used by astromechs)
                        # requires height.
                        HasAllAbilities(CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_0_44)
                    ),
                    moderate=Or(
                        And(
                            # The first jump requires distance, the second jump (from the platform used by astromechs)
                            # requires height.
                            # Dexter has 0.76 distance, which is just enough.
                            HasAbility(CAN_JUMP_DISTANCE_0_84) | Character.DEXTER_JETTSTER.has(),
                            Or(
                                HasAbility(CAN_JUMP_0_44),
                                # Characters with 0.37 jump height and 0.84 distance are able to cross the gap without
                                # needing the platform used by astromechs, but messing up can mean restarting the level,
                                # so only the characters that can recover from this mess-up are being included.
                                Character.has_any(
                                    # The dive roll from these characters is enough height to jump up after missing the
                                    # jump and falling onto the platform used by astromechs to avoid needing to restart
                                    # the level.
                                    Character.HAN_SOLO,
                                    Character.HAN_SOLO_STORMTROOPER,
                                    Character.HAN_SOLO_SKIFF,
                                    Character.HAN_SOLO_HOOD,
                                    Character.HAN_SOLO_HOTH,
                                    Character.HAN_SOLO_ENDOR,
                                    Character.INDIANA_JONES,
                                    # The extra large collision boxes of the Kaminoans allow them to slide up slopes
                                    # more easily when their jump is not quite enough, which allows them to jump up from
                                    # the platform used by astromechs if the jump over that platform is missed.
                                    Character.LAMA_SU,
                                    Character.TAUN_WE,
                                ),
                            ),
                        ),
                    ),
                    # So long as you don't miss the jump over the platform used by astromechs, then 0.84 jump distance
                    # is all that is needed to progress. Missing the jump and causing your respawn point to be set to
                    # the platform used by astromechs can mean needing to restart the level.
                    hard=HasAbility(CAN_JUMP_DISTANCE_0_84) | Character.DEXTER_JETTSTER.has(),
                ),
            ),
        ),
        R_CAVE_UPPER_AREA_WITH_PANEL_AFTER_SECOND_LOWERING_PLATFORMS: (),
        R_CAVE_ACCESS_HATCH_EXIT_PLATFORM_AFTER_SECOND_LOWERING_PLATFORMS: (),
        R_VADER_FIGHT_AREA: (
            ExitData(
                R_CAVE_MANY_COLLAPSING_PLATFORMS_ROOM,
                logic_options(
                    base=CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    hard=CAN_DESTROY_CLOSE_SILVER_BRICKS | CAN_YODA_CLIP
                )
            ),
            ExitData(
                R_FINAL_AREA_SPAWN,
                logic_options(
                    # Fight him and force the platforms to get around the fight area.
                    base=HasAbility(JEDI),
                    normal=And(
                        # Darth Vader tends to deflect all blaster bolts, so melee attacks or an explosion are needed.
                        HasAbility(CAN_MELEE) | CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        # Allow high jump to get to each part of the fight. Building one of the objects is required to
                        # get enough jump height to get up the right side.
                        HasAbility(JEDI) | (CAN_ORIGINAL_TRILOGY_HIGH_JUMP & HasAbility(CAN_BUILD_BRICKS)),
                    ),
                    # Allow triple jump.
                    moderate=And(
                        HasAbility(CAN_MELEE) | CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        Or(
                            HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                            CAN_ORIGINAL_TRILOGY_HIGH_JUMP & HasAbility(CAN_BUILD_BRICKS),
                        ),
                    ),
                ),
                new_level=Level.DAGOBAH_C,
            ),
        ),
        R_CAVE_MANY_COLLAPSING_PLATFORMS_ROOM: (),
        R_FINAL_AREA_SPAWN: (
            ExitData(
                R_FINAL_AREA_ACROSS_BRIDGE,
                logic_options(
                    base=Or(
                        # Build the bridge and cross.
                        HasAbility(JEDI),
                        # Go into the swamp as an Astromech Droid, then swamp to a different character to jump up the
                        # step on the other side.
                        # Flutter characters can also jump up this step.
                        HasAbility(ASTROMECH_DROID) & (HasAbility(CAN_JUMP_HEIGHT_0_37) | HAS_FLUTTER_CHARACTER)
                    ),
                    # Allow jetpack hover.
                    # Allow flutter characters flying over the swamp entirely.
                    # Allow Kaminoans walking through the swamp.
                    normal=Or(
                        HasAnyAbilities(JEDI | JETPACK),
                        HasAllAbilities(ASTROMECH_DROID | CAN_JUMP_HEIGHT_0_37),
                        HAS_FLUTTER_CHARACTER,
                        _HAS_KAMINOAN,
                    ),
                    # Allow all double jump characters.
                    moderate=Or(
                        # All double jump characters can jump from the start of the bridge and get enough distance to
                        # land on a shallow enough part of the swamp on the other side to not drown.
                        HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                        HasAllAbilities(ASTROMECH_DROID | CAN_JUMP_HEIGHT_0_37),
                        HAS_FLUTTER_CHARACTER,
                        _HAS_KAMINOAN,
                    )
                ),
            ),
        ),
        R_FINAL_AREA_ACROSS_BRIDGE: (
            ExitData(
                "Chapter Completion",
                HasAllAbilities(ASTROMECH_PANEL | TRAINED_JEDI),
            ),
        ),
    },
    minikits={
        "Spawn Tree Minikit": minikit_data(
            R_SPAWN,
            logic_options(
                base=HasAbility(JEDI),
                normal=HasAbility(CAN_DOUBLE_JUMP),
                moderate=HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
            ),
            pickup_name="m_pup2"
        ),
        "Snake Swamp Central Island Minikit": minikit_data(
            R_FIRST_SWAMP_MINIKIT_ISLAND_AND_CHALLENGE_KIT_ISLAND,
            # The top part of the island, where the box to destroy and spawn the minikit is, needs a jump to get onto.
            logic_options(
                base=CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE & HasAbility(CAN_JUMP_HEIGHT_0_37),
                normal=CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE & HasAbility(CAN_BARELY_JUMP),
            ),
            pickup_name="m_pup1",
        ),
        "Yoda's TV Minikit": minikit_data(
            R_YODAS_HUT,
            CAN_SITH_FORCE,
            pickup_name="m_pup2",
        ),
        "Swamp Silver Brick Cave Minikit": minikit_data(
            R_ACROSS_RAFT_TO_SILVER_BRICK_CAVE,
            CAN_DESTROY_CLOSE_SILVER_BRICKS,
            pickup_name="m_pup3",
        ),
        "Open Three Hatches Minikit": MinikitData(
            R_TRAINING_AREA_END,
            And(
                CAN_DAMAGE_AT_CLOSE_RANGE,
                helper.can_reach_region(R_TRAINING_AREA_START),
                helper.can_reach_region(R_TRAINING_AREA_MIDDLE_ISLAND),
            ),
            pickup_names=("m_pup1", "m_pup3", "m_pup4",)
        ),
        "Grapple Minikit After Hut": minikit_data(
            R_ROOTS_PLATFORMING_END,
            logic_options(
                base=CAN_GRAPPLE,
                # High jump off the astromech panel box. It seems like the developers intended to make you slide off
                # this box, but messed up, and you can stand, and jump from some parts of it.
                normal=CAN_GRAPPLE | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                # Allow triple jump for height.
                moderate=ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(GRAPPLE | JEDI | HIGH_JUMP),
                    capped=HasAnyAbilities(GRAPPLE | JEDI | CAN_HIGH_JUMP_SLAM),
                )
            ),
            pickup_name="m_pup2",
        ),
        "Sith Force Bridge Minikit": minikit_data(
            R_CAVE_ACROSS_SITH_FORCE_BRIDGE,
            # The minikit is visible from the start, but cannot be interacted with until grapple point is built.
            # The grapple point is hidden within the silver bricks.
            # The silver bricks cannot be destroyed until the bridge is built.
            logic_options(
                base=CAN_SITH_FORCE_AND_GRAPPLE & CAN_DESTROY_CLOSE_SILVER_BRICKS,
                # Allow triple jump. Grievous can also just barely jump up without needing to triple jump.
                moderate=CAN_SITH_FORCE & CAN_DESTROY_CLOSE_SILVER_BRICKS,
            ),
            pickup_name="m_pup1",
        ),
        "Caged Minikit": minikit_data(
            R_CAVE_AFTER_SECOND_LOWERING_PLATFORMS,
            # It is so easy to shoot this minikit down from ground-level, that I'm not going to consider using the
            # Access Hatch and then shooting it from the high vantage point to be the developer intended solution.
            logic_options(
                base=HasAbility(BLASTER),
                # Allow WEAPON_EWOK from this higher area, shooting backwards to hit the cage.
                normal=Or(
                    HasAbility(BLASTER),
                    And(
                        helper.can_reach_region(R_CAVE_UPPER_AREA_WITH_PANEL_AFTER_SECOND_LOWERING_PLATFORMS),
                        HasAbility(WEAPON_EWOK),
                    ),
                ),
                # Allow WEAPON_EWOK from the Access Hatch Exit platform.
                # Allow Astromech hover over to the cage from the Access Hatch Exit platform, and then Self-Destruct.
                # Allow jumping on top of the cage and then attacking it from there.
                moderate=Or(
                    # All WEAPON_EWOK can use the access hatch, so there's no need to specify reaching the region, or
                    # the SHORTIE ability requirement.
                    HasAnyAbilities(BLASTER | WEAPON_EWOK),
                    # Get to the cage from the area with the astromech panel.
                    And(
                        helper.can_reach_region(R_CAVE_UPPER_AREA_WITH_PANEL_AFTER_SECOND_LOWERING_PLATFORMS),
                        Or(
                            And(
                                # Triple jump or high jump to the cage.
                                # Or ignore the astromech panel, double jump around to the window, and then double jump
                                # to the cage. Note that all the terrain around the window is slippery, so touching it
                                # will eat your double jump.
                                HasAbility(CAN_DOUBLE_JUMP),
                                # Destroy the cage from on top of it.
                                Or(
                                    # Slam
                                    HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                                    # Explode
                                    CAN_USE_SELF_DESTRUCT,
                                    # Combo-type attacks auto-target nearby objects, including the cage while standing
                                    # on it. The other combo-type attackers can all slam, so it's just IMPERIAL_GUARD
                                    # that needs to be specified individually.
                                    Character.IMPERIAL_GUARD.has(),
                                ),
                            ),
                            # Hover over to the cage, then explode next to it.
                            HasAbility(ASTROMECH_DROID) & Extra.SELF_DESTRUCT.has(),
                        ),
                    ),
                    # Get to the cage from the Access Hatch exit.
                    And(
                        helper.can_reach_region(R_CAVE_ACCESS_HATCH_EXIT_PLATFORM_AFTER_SECOND_LOWERING_PLATFORMS),
                        # Hover over to the cage, then explode next to it.
                        HasAbility(ASTROMECH_DROID) & Extra.SELF_DESTRUCT.has(),
                    ),
                ),
            ),
            pickup_name="m_pup2",
        ),
        "Many Collapsing Platforms Minikit": minikit_data(
            R_CAVE_MANY_COLLAPSING_PLATFORMS_ROOM,
            # If you can reach here, you can get to the minikit. The platforms that don't collapse are fixed, and even
            # the worse jumpers can jump across.
            True_(),
            er_rule=HasAbility(CAN_BARELY_JUMP),
            pickup_name="m_pup4",
        ),
        "Final Area Lever Minikit": minikit_data(
            R_FINAL_AREA_ACROSS_BRIDGE,
            logic_options(
                # 1) Use the Access Hatch.
                # 2) Hover/double jump across to the lever.
                # 3) Pull the lever.
                # 4A) Build the grapple point, grapple up, and jump to the minikit.
                # 4B) High jump up
                base=And(
                    HasAllAbilities(SHORTIE | CAN_PULL_LEVERS),
                    HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                    Or(
                        HasAllAbilities(CAN_BUILD_BRICKS | CAN_DOUBLE_JUMP) & CAN_GRAPPLE,
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                ),
                # Allow high jump up to the lever, then pull the lever, and then high jump to the minikit.
                # Allow grappling and then jumping to the minikit with characters that have a good single jump height +
                # distance.
                normal=Or(
                    HasAllAbilities(CAN_PULL_LEVERS | HIGH_JUMP) & OT_HIGH_JUMP_ENABLED,
                    # Use the access hatch to get to the lever.
                    And(
                        HasAllAbilities(SHORTIE | CAN_PULL_LEVERS),
                        # Jump from the access hatch to the lever.
                        HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                        # Build the grapple point, grapple up, and jump to the minikit.
                        And(
                            HasAbility(CAN_BUILD_BRICKS),
                            CAN_GRAPPLE,
                            # Reasonable jump distance and height are required.
                            HasAbilityCombination(CAN_JUMP_0_44 | CAN_JUMP_DISTANCE_0_92),
                        ),
                    )
                ),
                # Allow triple jump and characters that can only reach the minikit with a dive roll.
                moderate=HasAbility(CAN_PULL_LEVERS) & Or(
                    # High jump to the lever and kit.
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    # Triple jump to the lever and kit.
                    HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    # Use the access hatch to reach the lever.
                    And(
                        HasAbility(SHORTIE),
                        # Jump from the access hatch to the lever.
                        HasAnyAbilities(CAN_JUMP_DISTANCE_0_92 | HOVER),
                        # Build the grapple point, grapple up, and jump to the minikit.
                        And(
                            # Jedi can triple jump up on their own, so there is no need to use CAN_GRAPPLE to check for
                            # Force Grapple Leap usage.
                            HasAllAbilities(CAN_BUILD_BRICKS | GRAPPLE),
                            Or(
                                # Reasonable jump distance and height are required.
                                HasAbilityCombination(CAN_JUMP_0_44 | CAN_JUMP_DISTANCE_0_92),
                                # Despite not having enough jump height/distance on their own, their dive roll does give
                                # enough height/distance.
                                Character.has_any(
                                    Character.HAN_SOLO,
                                    Character.HAN_SOLO_STORMTROOPER,
                                    Character.HAN_SOLO_SKIFF,
                                    Character.HAN_SOLO_HOOD,
                                    Character.HAN_SOLO_HOTH,
                                    Character.HAN_SOLO_ENDOR,
                                    Character.INDIANA_JONES,
                                    Character.LANDO_CALRISSIAN,
                                    Character.LANDO_PALACE_GUARD,
                                )
                            ),
                        ),
                    ),
                ),
            ),
            pickup_name="m_pup1",
        ),
    },
    power_brick=LocationData(
        R_RACETRACK,
        CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE & HasAllAbilities(CAN_RIDE_VEHICLES | CAN_BUILD_BRICKS)
    ),
    ridables={
        Character.TRACTOR: (
            LocationData(
                R_RACETRACK,
                # Destroy the object containing the bricks, and then build it.
                CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE & HasAbility(CAN_BUILD_BRICKS)
            ),
            LocationData(
                R_POST_TRAINING_AREA,
                # It must be forced out of the swamp, and then the trailer must be forced off.
                HasAbility(JEDI),
            ),
        ),
    }
)
