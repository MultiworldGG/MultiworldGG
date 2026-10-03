from rule_builder.rules import And, CanReachRegion, Has, Or, True_

from ... import OracleOfSeasonsWorld
from ...options import (
    OracleOfSeasonsIncludeSecretLocations,
    OracleOfSeasonsLogicDifficulty,
    OracleOfSeasonsOptions,
    OracleOfSeasonsRemoveD0AltEntrance,
    OracleOfSeasonsRemoveD2AltEntrance,
    OracleOfSeasonsTarmGateRequirement,
)
from ..Constants import SEASON_AUTUMN, SEASON_SPRING, SEASON_SUMMER, SEASON_WINTER
from . import LogicLine
from .logic_predicates import (
    oos_can_beat_required_golden_beasts,
    oos_can_break_bush,
    oos_can_break_flowers,
    oos_can_break_mushroom,
    oos_can_complete_lost_woods_main_sequence,
    oos_can_dimitri_clip,
    oos_can_farm_rupees,
    oos_can_harvest_gasha,
    oos_can_harvest_tree,
    oos_can_jump_1_wide_liquid,
    oos_can_jump_1_wide_pit,
    oos_can_jump_2_wide_liquid,
    oos_can_jump_2_wide_pit,
    oos_can_jump_3_wide_liquid,
    oos_can_jump_3_wide_pit,
    oos_can_jump_4_wide_liquid,
    oos_can_jump_4_wide_pit,
    oos_can_jump_5_wide_liquid,
    oos_can_jump_5_wide_pit,
    oos_can_jump_6_wide_pit,
    oos_can_kill_armored_enemy,
    oos_can_kill_facade,
    oos_can_kill_moldorm,
    oos_can_meet_maple,
    oos_can_reach_lost_woods_pedestal,
    oos_can_reach_rooster_adventure,
    oos_can_remove_rockslide,
    oos_can_remove_season,
    oos_can_remove_snow,
    oos_can_summon_dimitri,
    oos_can_summon_moosh,
    oos_can_summon_ricky,
    oos_can_swim,
    oos_can_trigger_lever,
    oos_can_use_ember_seeds,
    oos_can_use_mystery_seeds,
    oos_can_use_pegasus_seeds,
    oos_can_use_seeds,
    oos_has_autumn,
    oos_has_biggoron_sword,
    oos_has_bombchus,
    oos_has_bombchus_for_bombjump,
    oos_has_bombchus_for_tiles,
    oos_has_bombs,
    oos_has_bombs_for_bombjump,
    oos_has_bombs_for_tiles,
    oos_has_bracelet,
    oos_has_cane,
    oos_has_cape,
    oos_has_ember_seeds,
    oos_has_essences,
    oos_has_essences_for_maku_seed,
    oos_has_essences_for_treehouse,
    oos_has_feather,
    oos_has_flippers,
    oos_has_flute,
    oos_has_fools_ore,
    oos_has_gale_seeds,
    oos_has_hearts_by_difficulty,
    oos_has_magic_boomerang,
    oos_has_magnet_gloves,
    oos_has_mystery_seeds,
    oos_has_noble_sword,
    oos_has_pegasus_seeds,
    oos_has_prog,
    oos_has_required_jewels,
    oos_has_rod,
    oos_has_rupees_for_shop,
    oos_has_satchel,
    oos_has_scent_seeds,
    oos_has_season,
    oos_has_seed_thrower,
    oos_has_shield,
    oos_has_shovel,
    oos_has_spring,
    oos_has_summer,
    oos_has_switch_hook,
    oos_has_sword,
    oos_has_tight_switch_hook,
    oos_has_winter,
    oos_is_companion_moosh,
    oos_is_companion_ricky,
    oos_is_default_season,
    oos_not_season_in_eastern_suburbs,
    oos_option_hard_logic,
    oos_option_hell_logic,
    oos_option_medium_logic,
    oos_roosters,
    oos_season_in_central_woods_of_winter,
    oos_season_in_eastern_suburbs,
    oos_season_in_eyeglass_lake,
    oos_season_in_holodrum_plain,
    oos_season_in_horon_village,
    oos_season_in_lost_woods,
    oos_season_in_mt_cucco,
    oos_season_in_spool_swamp,
    oos_season_in_sunken_city,
    oos_season_in_tarm_ruins,
    oos_season_in_temple_remains,
    oos_season_in_western_coast,
    oos_season_in_woods_of_winter,
    oos_self_locking_item,
)
from .rulebuilder import from_option


def make_holodrum_logic(world: OracleOfSeasonsWorld, options: OracleOfSeasonsOptions) -> list[LogicLine]:
    return [
        (
            world.origin_region_name,
            "gasha tree 1",
            False,
            oos_can_harvest_gasha(1),
            options.deterministic_gasha_locations >= 1,
        ),
        ("gasha tree 1", "gasha tree 2", False, oos_can_harvest_gasha(2), options.deterministic_gasha_locations >= 2),
        ("gasha tree 2", "gasha tree 3", False, oos_can_harvest_gasha(3), options.deterministic_gasha_locations >= 3),
        ("gasha tree 3", "gasha tree 4", False, oos_can_harvest_gasha(4), options.deterministic_gasha_locations >= 4),
        ("gasha tree 4", "gasha tree 5", False, oos_can_harvest_gasha(5), options.deterministic_gasha_locations >= 5),
        ("gasha tree 5", "gasha tree 6", False, oos_can_harvest_gasha(6), options.deterministic_gasha_locations >= 6),
        ("gasha tree 6", "gasha tree 7", False, oos_can_harvest_gasha(7), options.deterministic_gasha_locations >= 7),
        ("gasha tree 7", "gasha tree 8", False, oos_can_harvest_gasha(8), options.deterministic_gasha_locations >= 8),
        ("gasha tree 8", "gasha tree 9", False, oos_can_harvest_gasha(9), options.deterministic_gasha_locations >= 9),
        (
            "gasha tree 9",
            "gasha tree 10",
            False,
            oos_can_harvest_gasha(10),
            options.deterministic_gasha_locations >= 10,
        ),
        (
            "gasha tree 10",
            "gasha tree 11",
            False,
            oos_can_harvest_gasha(11),
            options.deterministic_gasha_locations >= 11,
        ),
        (
            "gasha tree 11",
            "gasha tree 12",
            False,
            oos_can_harvest_gasha(12),
            options.deterministic_gasha_locations >= 12,
        ),
        (
            "gasha tree 12",
            "gasha tree 13",
            False,
            oos_can_harvest_gasha(13),
            options.deterministic_gasha_locations >= 13,
        ),
        (
            "gasha tree 13",
            "gasha tree 14",
            False,
            oos_can_harvest_gasha(14),
            options.deterministic_gasha_locations >= 14,
        ),
        (
            "gasha tree 14",
            "gasha tree 15",
            False,
            oos_can_harvest_gasha(15),
            options.deterministic_gasha_locations >= 15,
        ),
        (
            "gasha tree 15",
            "gasha tree 16",
            False,
            oos_can_harvest_gasha(16),
            options.deterministic_gasha_locations >= 16,
        ),
        (
            "maple encounter",
            "maple trade",
            False,
            Or(Has("Lon Lon Egg"), oos_self_locking_item("Maple Trade", "Lon Lon Egg")),
        ),
        ("maple encounter", "maple rare item 1", False, oos_has_prog(15)),
        ("maple rare item 1", "maple rare item 2", False, oos_has_prog(30)),
        ("maple rare item 2", "maple rare item 3", False, oos_has_prog(45)),
        ("maple rare item 3", "maple rare item 4", False, oos_has_prog(60)),
        ("horon village", "mayor's gift", False, True_()),
        ("horon village", "vasu's gift", False, True_()),
        ("horon village", "mayor's house secret room", False, oos_can_remove_rockslide(False)),
        ("horon village", "horon heart piece", False, Or(oos_can_use_ember_seeds(False), oos_can_dimitri_clip())),
        ("horon village", "dr. left reward", False, oos_can_use_ember_seeds(True)),
        ("horon village", "old man in horon", False, oos_can_use_ember_seeds(False)),
        (
            "horon village",
            "old man trade",
            False,
            Or(Has("Fish"), oos_self_locking_item("North Horon: Yelling Old Man Trade", "Fish")),
        ),
        (
            "horon village",
            "tick tock trade",
            False,
            Or(Has("Wooden Bird"), oos_self_locking_item("Horon Village: Tick Tock Trade", "Wooden Bird")),
        ),
        ("horon village", "maku tree", False, oos_has_sword(False)),
        (
            "horon village",
            "horon village SE chest",
            False,
            And(
                oos_can_remove_rockslide(False),
                Or(
                    oos_can_swim(False),
                    oos_season_in_horon_village(SEASON_WINTER),
                    oos_can_jump_2_wide_liquid(allow_bombchus=True),
                ),
            ),
        ),
        (
            "horon village",
            "horon village SW chest",
            False,
            Or(And(oos_season_in_horon_village(SEASON_AUTUMN), oos_can_break_mushroom(True)), oos_can_dimitri_clip()),
        ),
        ("horon village", "horon village portal", False, Or(oos_has_magic_boomerang(), oos_can_jump_6_wide_pit())),
        ("horon village portal", "horon village", False, Or(oos_can_trigger_lever(), oos_can_jump_6_wide_pit())),
        ("horon village", "horon village tree", False, oos_can_harvest_tree(True)),
        ("horon village", "horon shop", False, oos_has_rupees_for_shop("horonShop")),
        ("horon village", "advance shop", False, oos_has_rupees_for_shop("advanceShop"), bool(options.advance_shop)),
        ("horon village", "member's shop", False, And(Has("Member's Card"), oos_has_rupees_for_shop("memberShop"))),
        (
            "horon village",
            "clock shop secret",
            False,
            And(
                oos_has_shovel(),
                Or(
                    oos_has_noble_sword(),
                    oos_has_biggoron_sword(),
                    oos_has_fools_ore(),
                    And(oos_option_medium_logic(), Or(oos_has_sword(), oos_has_bombchus(3))),
                ),
            ),
            bool(options.secret_locations),
        ),
        # WESTERN COAST ##############################################################################################
        ("horon village", "western coast", True, True_()),
        ("western coast", "maple encounter", False, oos_can_meet_maple()),
        (
            "western coast",
            "black beast's chest",
            False,
            And(
                And(
                    oos_has_seed_thrower(),
                    oos_can_use_ember_seeds(True),
                ),
                oos_can_use_mystery_seeds(),
                oos_can_kill_moldorm(),
            ),
        ),
        ("western coast", "d0 entrance", True, True_()),
        (
            "western coast",
            "d0 rupee chest",
            False,
            And(
                from_option(OracleOfSeasonsRemoveD0AltEntrance, OracleOfSeasonsRemoveD0AltEntrance.option_false),
                oos_can_break_bush(True),
            ),
        ),
        ("western coast after ship", "western coast", False, And(Has("_met_pirates"), Has("Pirate's Bell"))),
        (
            "western coast after ship",
            "coast stump",
            False,
            And(oos_can_remove_rockslide(False), Or(oos_has_feather(), oos_option_hard_logic())),
        ),
        ("western coast after ship", "old man near western coast house", False, oos_can_use_ember_seeds(False)),
        (
            "western coast after ship",
            "d7 entrance",
            False,
            And(
                Or(oos_can_jump_3_wide_pit(), oos_season_in_western_coast(SEASON_SUMMER)),
                Or(
                    oos_has_shovel(),
                    oos_is_default_season("WESTERN_COAST", SEASON_WINTER, False),
                    And(CanReachRegion("coast stump"), oos_can_remove_season(SEASON_WINTER)),
                ),
            ),
        ),
        (
            "western coast after ship",
            "graveyard heart piece",
            False,
            And(oos_season_in_western_coast(SEASON_AUTUMN), oos_can_jump_3_wide_pit(), oos_can_break_mushroom(False)),
        ),
        (
            "d7 entrance",
            "graveyard heart piece",
            False,
            And(oos_is_default_season("WESTERN_COAST", SEASON_AUTUMN), oos_can_break_mushroom(False)),
        ),
        ("d7 entrance", "graveyard secret", False, oos_has_shovel(), bool(options.secret_locations)),
        (
            "d7 entrance",
            "western coast after ship",
            False,
            Or(
                oos_is_default_season("WESTERN_COAST", SEASON_WINTER, False),
                oos_has_shovel(),
            ),
        ),
        # EASTERN SUBURBS #############################################################################################
        ("horon village", "suburbs", True, oos_can_use_ember_seeds(False)),
        ("suburbs", "maple encounter", False, oos_can_meet_maple()),
        (
            "suburbs",
            "windmill heart piece",
            False,
            Or(oos_season_in_eastern_suburbs(SEASON_WINTER), oos_can_dimitri_clip()),
        ),
        (
            "suburbs",
            "guru-guru trade",
            False,
            Or(Has("Engine Grease"), oos_self_locking_item("Eastern Suburbs: Guru-Guru Trade", "Engine Grease")),
        ),
        (
            "suburbs",
            "eastern suburbs spring cave",
            False,
            And(
                oos_has_bracelet(),
                oos_season_in_eastern_suburbs(SEASON_SPRING),
                Or(oos_has_magnet_gloves(), oos_can_jump_3_wide_pit()),
            ),
        ),
        ("eastern suburbs portal", "suburbs", False, oos_can_break_bush(False)),
        ("suburbs", "eastern suburbs portal", False, oos_can_break_bush(True)),
        (
            "suburbs",
            "suburbs fairy fountain",
            True,
            And(
                Or(oos_can_swim(True), oos_can_jump_1_wide_liquid(True), oos_has_switch_hook()),
                oos_not_season_in_eastern_suburbs(SEASON_WINTER),
            ),
        ),
        ("suburbs fairy fountain", "maple encounter", False, oos_can_meet_maple()),
        ("suburbs fairy fountain", "suburbs fairy fountain (winter)", False, oos_has_winter()),
        # Should be a useless transition, but it might be useful someday
        ("suburbs", "suburbs fairy fountain (winter)", True, oos_season_in_eastern_suburbs(SEASON_WINTER)),
        ("suburbs fairy fountain (winter)", "maple encounter", False, oos_can_meet_maple()),
        ("suburbs fairy fountain (winter)", "suburbs fairy fountain", False, oos_can_remove_season(SEASON_WINTER)),
        ("suburbs fairy fountain", "sunken city entrance", False, oos_season_in_eastern_suburbs(SEASON_SPRING)),
        ("sunken city entrance", "suburbs fairy fountain", False, oos_not_season_in_eastern_suburbs(SEASON_WINTER)),
        (
            "sunken city entrance",
            "suburbs fairy fountain (winter)",
            False,
            oos_season_in_eastern_suburbs(SEASON_WINTER),
        ),
        # WOODS OF WINTER / 2D SECTOR ################################################################################
        ("suburbs fairy fountain (winter)", "moblin road", False, True_()),
        ("moblin road", "suburbs fairy fountain (winter)", False, oos_season_in_eastern_suburbs(SEASON_WINTER)),
        ("moblin road", "maple encounter", False, oos_can_meet_maple()),
        (
            "sunken city entrance",
            "moblin road",
            False,
            And(
                oos_has_flippers(),
                Or(oos_is_default_season("SUNKEN_CITY", SEASON_WINTER, False), oos_can_remove_season(SEASON_WINTER)),
            ),
        ),
        (
            "moblin road",
            "woods of winter, 1st cave",
            False,
            And(
                oos_can_remove_rockslide(True),
                oos_can_break_bush(False, True),
                Or(
                    oos_is_default_season("WOODS_OF_WINTER", SEASON_WINTER, False), oos_can_remove_season(SEASON_WINTER)
                ),
            ),
        ),
        (
            "moblin road",
            "woods of winter, 2nd cave",
            False,
            Or(oos_can_swim(False), oos_can_jump_3_wide_liquid(allow_bombchus=True)),
        ),
        ("moblin road", "holly's house", False, oos_season_in_woods_of_winter(SEASON_WINTER)),
        ("moblin road", "old man near holly's house", False, oos_can_use_ember_seeds(False)),
        (
            "moblin road",
            "woods of winter heart piece",
            False,
            Or(oos_can_swim(True), oos_has_bracelet(), oos_can_jump_1_wide_liquid(True)),
        ),
        ("suburbs fairy fountain", "central woods of winter", False, True_()),
        (
            "suburbs fairy fountain (winter)",
            "central woods of winter",
            False,
            Or(
                And(oos_can_jump_1_wide_pit(True), oos_has_bracelet()),
                And(oos_option_medium_logic(), oos_has_switch_hook(), oos_has_bracelet()),
                oos_can_remove_snow(True),
            ),
        ),
        (
            "central woods of winter",
            "suburbs fairy fountain",
            False,
            oos_is_default_season("EASTERN_SUBURBS", SEASON_WINTER, False),
        ),
        (
            "central woods of winter",
            "suburbs fairy fountain (winter)",
            False,
            And(
                oos_is_default_season("EASTERN_SUBURBS", SEASON_WINTER),
                Or(
                    And(oos_can_jump_1_wide_pit(True), oos_has_bracelet()),
                    And(oos_option_medium_logic(), oos_has_switch_hook(), oos_has_bracelet()),
                    oos_can_remove_snow(True),
                ),
            ),
        ),
        ("central woods of winter", "woods of winter tree", False, oos_can_harvest_tree(True)),
        ("central woods of winter", "d2 entrance", True, oos_can_break_bush(True, True)),
        (
            "central woods of winter",
            "cave outside D2",
            False,
            And(
                Or(
                    And(
                        oos_season_in_central_woods_of_winter(SEASON_AUTUMN),
                        oos_can_break_mushroom(True),
                    ),
                    oos_can_dimitri_clip(),
                ),
                Or(oos_can_jump_4_wide_pit(), oos_has_magnet_gloves()),
            ),
        ),
        ("central woods of winter", "d2 stump", True, True_()),
        ("d2 stump", "d2 roof", True, oos_has_bracelet()),
        (
            "d2 roof",
            "d2 alt entrances",
            # Do not allow for turning back if the dungeon is excluded
            not options.exclude_dungeons_without_essence.value or "Gift of Time" in world.essences_in_game,
            from_option(OracleOfSeasonsRemoveD2AltEntrance, OracleOfSeasonsRemoveD2AltEntrance.option_false),
        ),
        ("central woods of winter", "mystery owl", False, oos_can_use_mystery_seeds()),
        # EYEGLASS LAKE SECTOR #########################################################################################
        ("impa's house", "horon village", True, True_()),
        ("impa's house", "maple encounter", False, oos_can_meet_maple()),
        (
            "impa's house",
            "eyeglass lake, across bridge",
            False,
            Or(
                oos_can_jump_4_wide_pit(),
                And(
                    oos_has_feather(),
                    Or(
                        oos_is_default_season("EYEGLASS_LAKE", SEASON_AUTUMN),
                        And(oos_has_autumn(), oos_can_break_bush(True)),
                    ),
                ),
            ),
        ),
        ("impa's house", "d1 stump", True, oos_can_break_bush(True, True)),
        ("d1 stump", "north horon", True, oos_has_bracelet()),
        (
            "d1 stump",
            "malon trade",
            False,
            Or(Has("Cuccodex"), oos_self_locking_item("North Horon: Malon Trade", "Cuccodex")),
        ),
        ("d1 stump", "d1 island", True, oos_can_break_bush(True, True)),
        ("d1 stump", "old man near d1", False, oos_can_use_ember_seeds(False)),
        ("d1 island", "d1 entrance", True, Has("Gnarled Key")),
        (
            "d1 island",
            "golden beasts old man",
            False,
            And(
                Or(
                    oos_is_default_season("EYEGLASS_LAKE", SEASON_SUMMER),
                    And(oos_has_summer(), oos_can_break_bush(True)),
                ),
                oos_can_beat_required_golden_beasts(),
            ),
        ),
        (
            "d1 stump",
            "eyeglass lake (default)",
            True,
            And(
                Or(
                    oos_season_in_eyeglass_lake(SEASON_SPRING),
                    oos_season_in_eyeglass_lake(SEASON_AUTUMN),
                ),
                oos_can_jump_1_wide_pit(True),
                Or(
                    oos_can_swim(False),
                    And(
                        # To be able to use Dimitri, we need the bracelet to throw him above the pit
                        oos_option_medium_logic(),
                        oos_can_summon_dimitri(),
                        oos_has_bracelet(),
                    ),
                ),
            ),
        ),
        (
            "d1 stump",
            "eyeglass lake (dry)",
            True,
            And(oos_season_in_eyeglass_lake(SEASON_SUMMER), oos_can_jump_1_wide_pit(True)),
        ),
        (
            "d1 stump",
            "eyeglass lake (frozen)",
            True,
            And(oos_season_in_eyeglass_lake(SEASON_WINTER), oos_can_jump_1_wide_pit(True)),
        ),
        ("d5 stump", "maple encounter", False, oos_can_meet_maple()),
        (
            "d5 stump",
            "eyeglass lake (default)",
            True,
            And(
                Or(
                    oos_season_in_eyeglass_lake(SEASON_SPRING),
                    oos_season_in_eyeglass_lake(SEASON_AUTUMN),
                ),
                oos_can_swim(True),
            ),
        ),
        (
            "d5 stump",
            "eyeglass lake (dry)",
            False,
            And(oos_season_in_eyeglass_lake(SEASON_SUMMER), oos_can_swim(False)),
        ),
        ("d5 stump", "eyeglass lake (frozen)", True, oos_season_in_eyeglass_lake(SEASON_WINTER)),
        (
            "eyeglass lake portal",
            "eyeglass lake (default)",
            False,
            And(
                Or(
                    oos_is_default_season("EYEGLASS_LAKE", SEASON_AUTUMN),
                    oos_is_default_season("EYEGLASS_LAKE", SEASON_SPRING),
                ),
                oos_can_swim(False),
            ),
        ),
        ("eyeglass lake (default)", "eyeglass lake portal", False, True_()),
        (
            "eyeglass lake portal",
            "eyeglass lake (frozen)",
            False,
            And(
                oos_is_default_season("EYEGLASS_LAKE", SEASON_WINTER),
                Or(oos_can_swim(False), oos_can_jump_5_wide_liquid()),
            ),
        ),
        ("eyeglass lake (frozen)", "eyeglass lake portal", False, Or(oos_can_swim(True), oos_can_jump_5_wide_liquid())),
        # This transition has been removed since the anti-softlock has been removed
        # ["eyeglass lake portal", "eyeglass lake (dry)", False,  \
        #     oos_is_default_season( "EYEGLASS_LAKE", SEASON_SUMMER)),
        # Instead, jump straight from the portal to lost woods in summer
        (
            "eyeglass lake portal",
            "lost woods",
            False,
            And(oos_option_hard_logic(), oos_is_default_season("EYEGLASS_LAKE", SEASON_SUMMER)),
        ),
        (
            "eyeglass lake (dry)",
            "dry eyeglass lake, west cave",
            False,
            And(
                oos_can_remove_rockslide(True),
                oos_can_swim(False),  # chest is surrounded by water
            ),
        ),
        (
            "d5 stump",
            "d5 entrance",
            False,
            And(
                # If we don't have autumn, we need to ensure we were able to reach that node with autumn as default
                # season without changing to another season which we wouldn't be able to revert back.
                # For this reason, "default season is autumn" case is handled through direct routes from the lake portal
                # and from D1 stump.
                oos_has_autumn(),
                oos_can_break_mushroom(True),
            ),
        ),
        # Direct route #1 to reach D5 entrance taking advantage of autumn as default season
        (
            "d1 stump",
            "d5 entrance",
            False,
            And(
                oos_is_default_season("EYEGLASS_LAKE", SEASON_AUTUMN),
                oos_can_jump_1_wide_pit(True),
                oos_can_break_mushroom(True),
                Or(
                    oos_can_swim(False),
                    And(
                        # To be able to use Dimitri, we need the bracelet to throw him above the pit
                        oos_option_medium_logic(),
                        oos_can_summon_dimitri(),
                        oos_has_bracelet(),
                    ),
                    And(
                        # Alternatively, we can use winter to summon Dimitri then reset the season with the portal
                        oos_can_summon_dimitri(),
                        oos_has_winter(),
                    ),
                ),
            ),
        ),
        # Direct route #2 to reach D5 entrance taking advantage of autumn as default season
        (
            "eyeglass lake portal",
            "d5 entrance",
            False,
            And(
                oos_is_default_season("EYEGLASS_LAKE", SEASON_AUTUMN), oos_can_swim(False), oos_can_break_mushroom(True)
            ),
        ),
        (
            "d5 entrance",
            "d5 stump",
            False,
            Or(
                oos_can_jump_1_wide_pit(True),
                And(
                    oos_is_default_season("EYEGLASS_LAKE", SEASON_AUTUMN),
                    oos_can_break_mushroom(False),
                    # TODO: Maybe change that by removing the anti-softlock
                    #  mechanism that also adds an anti-ricky protection
                    # Alternatively, move the rock up to prevent ricky from jumping while preserving the anti-softlock
                ),
            ),
        ),
        (
            "d5 stump",
            "dry eyeglass lake, east cave",
            False,
            And(
                oos_has_summer(),
                oos_has_bracelet(),
            ),
        ),
        (
            "d5 entrance",
            "dry eyeglass lake, east cave",
            False,
            And(
                oos_can_jump_1_wide_pit(True),
                oos_is_default_season("EYEGLASS_LAKE", SEASON_SUMMER),
                oos_has_bracelet(),
            ),
        ),
        # NORTH HORON / HOLODRUM PLAIN ###############################################################################
        ("north horon", "maple encounter", False, oos_can_meet_maple()),
        ("north horon", "north horon tree", False, oos_can_harvest_tree(True)),
        ("north horon", "blaino prize", False, oos_can_farm_rupees()),
        (
            "north horon",
            "cave north of D1",
            False,
            And(
                Or(
                    And(
                        oos_season_in_holodrum_plain(SEASON_AUTUMN),
                        oos_can_break_mushroom(True),
                    ),
                    oos_can_dimitri_clip(),
                ),
                oos_has_flippers(),
            ),
        ),
        (
            "north horon",
            "old man near blaino",
            False,
            And(
                oos_can_use_ember_seeds(False),
                Or(
                    oos_is_default_season("HOLODRUM_PLAIN", SEASON_SUMMER),
                    oos_can_summon_ricky(),
                    And(
                        # can get from the stump to old man in summer
                        oos_has_summer(),
                        Or(oos_can_jump_1_wide_pit(True), And(oos_can_break_bush(True), oos_can_swim(True))),
                    ),
                ),
            ),
        ),
        ("north horon", "underwater item below natzu bridge", False, oos_can_swim(False)),
        ("north horon", "temple remains lower stump", False, oos_can_jump_3_wide_pit()),
        (
            "north horon",
            "spool swamp north",
            False,
            Has("Ricky's Gloves")
        ),
        ("temple remains lower stump", "north horon", False, Or(oos_can_jump_3_wide_pit(), oos_has_switch_hook())),
        ("ghastly stump", "maple encounter", False, oos_can_meet_maple()),
        (
            "ghastly stump",
            "mrs. ruul trade",
            False,
            Or(Has("Ghastly Doll"), oos_self_locking_item("Holodrum Plain: Mrs. Ruul Trade", "Ghastly Doll")),
        ),
        ("ghastly stump", "old man near mrs. ruul", False, oos_can_use_ember_seeds(False)),
        (
            "north horon",
            "ghastly stump",
            True,
            Or(oos_can_jump_1_wide_pit(True), oos_season_in_holodrum_plain(SEASON_WINTER)),
        ),
        ("spool swamp north", "ghastly stump", False, True_()),
        (
            "ghastly stump",
            "spool swamp north",
            False,
            Or(
                oos_season_in_holodrum_plain(SEASON_SUMMER),
                oos_can_jump_4_wide_pit(),
                oos_can_summon_ricky(),
                oos_can_summon_moosh(),
            ),
        ),
        (
            "ghastly stump",
            "spool swamp south",
            True,
            And(
                oos_can_swim(True),
                oos_can_break_bush(True),
            ),
        ),
        # Goron Mountain <-> North Horon <-> D1 island <-> Spool swamp waterway
        ("d1 island", "spool swamp south", False, oos_can_swim(True)),
        (
            "spool swamp south (spring)",
            "d1 island",
            False,
            Or(oos_can_summon_dimitri(), And(Has("Swimmer's Ring"), oos_can_swim(False), oos_option_medium_logic())),
        ),
        ("spool swamp south (summer)", "d1 island", False, oos_can_swim(True)),
        ("spool swamp south (autumn)", "d1 island", False, oos_can_swim(True)),
        ("spool swamp south (winter)", "d1 island", False, oos_can_swim(True)),
        ("d1 island", "north horon", True, oos_can_swim(True)),
        ("north horon", "goron mountain entrance", True, oos_can_swim(True)),
        ("goron mountain entrance", "natzu region, across water", True, oos_can_swim(True)),
        (
            "ghastly stump",
            "d1 island",
            True,
            And(
                # Technically, Ricky and Moosh don't work to go from the ghastly stump bank to the stump,
                # but both can go through north horon and jump the holes
                oos_can_break_bush(True),
                oos_can_swim(True),
            ),
        ),
        ("d1 island", "old man in treehouse", False, And(oos_can_swim(True), oos_has_essences_for_treehouse())),
        ("d1 island", "cave south of mrs. ruul", False, oos_can_swim(False)),
        # SPOOL SWAMP #############################################################################################
        ("spool swamp north", "maple encounter", False, oos_can_meet_maple()),
        ("spool swamp north", "spool swamp tree", False, oos_can_harvest_tree(True)),
        (
            "spool swamp north",
            "floodgate keeper's house",
            False,
            Or(oos_can_trigger_lever(), And(oos_option_hard_logic(), oos_has_bracelet())),
        ),
        (
            "spool swamp north",
            "spool swamp digging spot",
            False,
            And(oos_season_in_spool_swamp(SEASON_SUMMER), oos_has_shovel()),
        ),
        ("floodgate keeper's house", "floodgate owl", False, oos_can_use_mystery_seeds()),
        (
            "floodgate keeper's house",
            "floodgate keyhole",
            False,
            And(
                Or(
                    oos_can_use_pegasus_seeds(),
                    oos_has_cape(),
                    oos_has_flippers(),
                    And(
                        # The cane doesn't hold the button
                        oos_option_medium_logic(),
                        oos_has_cane(),
                    ),
                    And(
                        oos_option_medium_logic(),
                        oos_has_feather(),
                    ),
                ),
                oos_has_bracelet(),
            ),
        ),
        (
            "floodgate keyhole",
            "spool swamp scrub",
            False,
            oos_has_rupees_for_shop("spoolSwampScrub"),
            bool(options.shuffle_business_scrubs),
        ),
        ("floodgate keyhole", "spool stump", False, Has("Floodgate Key")),
        ("spool stump", "d3 entrance", False, oos_season_in_spool_swamp(SEASON_SUMMER)),
        (
            "d3 entrance",
            "spool swamp north",
            False,
            # Coming from alt d0/d2
            oos_can_swim(False),
        ),
        (
            "spool stump",
            "spool swamp middle",
            False,
            Or(
                oos_is_default_season("SPOOL_SWAMP", SEASON_SPRING, False),
                oos_can_remove_season(SEASON_SPRING),
                oos_can_swim(True),
            ),
        ),
        ("spool swamp middle", "spool swamp south near gasha spot", False, oos_can_summon_ricky()),
        (
            "spool swamp south near gasha spot",
            "spool swamp middle",
            False,
            Or(
                oos_can_summon_ricky(),
                And(
                    oos_has_feather(),
                    Or(
                        oos_has_magic_boomerang(),
                        And(
                            oos_option_medium_logic(),
                            Or(
                                oos_has_sword(),
                                And(
                                    oos_has_seed_thrower(),
                                    oos_can_use_ember_seeds(False),
                                ),
                                And(oos_has_bombs_for_tiles(), oos_option_hard_logic()),
                            ),
                        ),
                    ),
                ),
            ),
        ),
        ("spool swamp south near gasha spot", "maple encounter", False, oos_can_meet_maple()),
        ("spool swamp south near gasha spot", "spool swamp portal", True, oos_has_bracelet()),
        (
            "spool swamp middle",
            "spool swamp south",
            True,
            Or(oos_can_jump_2_wide_pit(), oos_can_summon_moosh(), oos_can_swim(True)),
        ),
        ("spool swamp south", "maple encounter", False, oos_can_meet_maple()),
        # make sure you can go directly from the stump to south, or default season
        # just because you can reach the stump doesn't mean you can also get there
        # ex. only access to gasha section is through subrosia
        ("spool swamp south", "spool swamp south (spring)", False, oos_is_default_season("SPOOL_SWAMP", SEASON_SPRING)),
        (
            "spool stump",
            "spool swamp south (spring)",
            False,
            And(
                oos_has_spring(),
                oos_can_swim(True),
                Or(oos_can_summon_ricky(), oos_can_summon_moosh(), oos_can_jump_2_wide_pit()),
            ),
        ),
        ("spool swamp south", "spool swamp south (summer)", False, oos_is_default_season("SPOOL_SWAMP", SEASON_SUMMER)),
        (
            "spool stump",
            "spool swamp south (summer)",
            False,
            And(
                oos_has_summer(),
                Or(oos_can_swim(True), oos_can_summon_ricky(), oos_can_summon_moosh(), oos_can_jump_2_wide_pit()),
            ),
        ),
        ("spool swamp south", "spool swamp south (autumn)", False, oos_is_default_season("SPOOL_SWAMP", SEASON_AUTUMN)),
        (
            "spool stump",
            "spool swamp south (autumn)",
            False,
            And(
                oos_has_autumn(),
                Or(oos_can_swim(True), oos_can_summon_ricky(), oos_can_summon_moosh(), oos_can_jump_2_wide_pit()),
            ),
        ),
        ("spool swamp south", "spool swamp south (winter)", False, oos_is_default_season("SPOOL_SWAMP", SEASON_WINTER)),
        (
            "spool stump",
            "spool swamp south (winter)",
            False,
            And(
                oos_has_winter(),
                Or(oos_can_swim(True), oos_can_summon_ricky(), oos_can_summon_moosh(), oos_can_jump_2_wide_pit()),
            ),
        ),
        ("spool swamp south (winter)", "spool swamp south", False, True_()),
        ("spool swamp south (spring)", "spool swamp south", False, True_()),
        ("spool swamp south (summer)", "spool swamp south", False, True_()),
        ("spool swamp south (autumn)", "spool swamp south", False, True_()),
        ("spool swamp south (spring)", "spool swamp south near gasha spot", False, oos_can_break_flowers(True)),
        ("spool swamp south (winter)", "spool swamp south near gasha spot", False, oos_can_remove_snow(True)),
        ("spool swamp south (summer)", "spool swamp south near gasha spot", False, True_()),
        ("spool swamp south (autumn)", "spool swamp south near gasha spot", False, True_()),
        # default season only because of the portal
        (
            "spool swamp south near gasha spot",
            "spool swamp south (spring)",
            False,
            And(oos_is_default_season("SPOOL_SWAMP", SEASON_SPRING), oos_can_break_flowers(True)),
        ),
        (
            "spool swamp south near gasha spot",
            "spool swamp south (summer)",
            False,
            oos_is_default_season("SPOOL_SWAMP", SEASON_SUMMER),
        ),
        (
            "spool swamp south near gasha spot",
            "spool swamp south (autumn)",
            False,
            oos_is_default_season("SPOOL_SWAMP", SEASON_AUTUMN),
        ),
        (
            "spool swamp south near gasha spot",
            "spool swamp south (winter)",
            False,
            And(oos_is_default_season("SPOOL_SWAMP", SEASON_WINTER), oos_can_remove_snow(True)),
        ),
        (
            "spool swamp south (winter)",
            "spool swamp cave",
            False,
            And(oos_can_remove_snow(True), oos_can_remove_rockslide(True)),
        ),
        ("spool swamp south (spring)", "spool swamp heart piece", False, oos_can_swim(True)),
        # NATZU REGION #############################################################################################
        ("north horon", "natzu west", True, True_()),
        ("moblin keep bridge", "moblin keep", True, Or(oos_has_flippers(), oos_can_jump_4_wide_liquid(True))),
        ("moblin keep", "moblin keep chest", False, oos_has_bracelet()),
        ("moblin keep", "sunken city entrance", False, True_()),
        ("natzu river bank", "goron mountain entrance", True, oos_can_swim(True)),
        # Access to natzu deku is companion specific
        (
            "natzu deku",
            "deku secret",
            False,
            And(
                oos_can_use_seeds(),
                oos_has_ember_seeds(),
                oos_has_scent_seeds(),
                oos_has_pegasus_seeds(),
                oos_has_gale_seeds(),
                oos_has_mystery_seeds(),
            ),
            bool(options.secret_locations),
        ),
        # SUNKEN CITY ############################################################################################
        (
            "sunken city entrance",
            "sunken city",
            True,
            Or(
                oos_has_feather(),
                oos_has_flippers(),
                oos_can_summon_dimitri(),
                oos_is_default_season("SUNKEN_CITY", SEASON_WINTER),
            ),
        ),
        (
            "sunken city",
            "sunken city tree",
            False,
            And(
                oos_can_harvest_tree(True),
            ),
        ),
        (
            "sunken city",
            "sunken city dimitri",
            False,
            Or(
                oos_can_summon_dimitri(),
                oos_has_bombs(),
            ),
        ),
        (
            # Go back to the entrance, useful when starting/coming from Sunken
            "sunken city dimitri",
            "sunken city entrance",
            False,
            True_(),
        ),
        (
            "sunken city",
            "ingo trade",
            False,
            Or(Has("Goron Vase"), oos_self_locking_item("Sunken City: Ingo Trade", "Goron Vase")),
        ),
        ("sunken city", "syrup trade", False, And(oos_season_in_sunken_city(SEASON_WINTER), Has("Mushroom"))),
        ("syrup trade", "syrup shop", False, oos_has_rupees_for_shop("syrupShop")),
        # Use Dimitri to get the tree seeds, using dimitri to get seeds being medium difficulty
        ("sunken city dimitri", "sunken city tree", False, And(oos_option_medium_logic(), oos_can_use_seeds())),
        (
            "sunken city dimitri",
            "master diver's challenge",
            False,
            And(oos_has_sword(False), Or(oos_has_feather(), oos_has_flippers())),
        ),
        (
            "sunken city dimitri",
            "master diver's reward",
            False,
            Or(Has("Master's Plaque"), oos_self_locking_item("Sunken City: Master's Plaque Trade", "Master's Plaque")),
        ),
        ("sunken city dimitri", "chest in master diver's cave", False, True_()),
        (
            "sunken city",
            "sunken city, summer cave",
            False,
            And(oos_season_in_sunken_city(SEASON_SUMMER), oos_has_flippers(), oos_can_break_bush(False, True)),
        ),
        (
            "sunken city",
            "diver secret",
            False,
            And(
                oos_has_flippers(),
                Or(
                    And(
                        Has("Swimmer's Ring"),
                        oos_option_medium_logic(),
                    ),
                    oos_option_hard_logic(),
                    oos_has_sword(),
                    oos_has_fools_ore(),
                ),
            ),
            bool(options.secret_locations),
        ),
        ("mount cucco", "sunken city", False, oos_has_flippers()),
        ("sunken city", "mount cucco", False, And(oos_has_flippers(), oos_season_in_sunken_city(SEASON_SUMMER))),
        # MT. CUCCO / GORON MOUNTAINS ##############################################################################
        ("mount cucco", "mt. cucco portal", True, True_()),
        (
            "mount cucco",
            "rightmost rooster ledge",
            False,
            And(
                Or(  # to reach the rooster
                    And(
                        oos_season_in_mt_cucco(SEASON_SPRING),
                        Or(
                            oos_can_break_flowers(),
                            Has("Spring Banana"),
                        ),
                    ),
                    oos_option_hard_logic(),
                ),
                oos_has_bracelet(),  # to grab the rooster
            ),
        ),
        ("rightmost rooster ledge", "mt. cucco, platform cave", False, True_()),
        (
            "rightmost rooster ledge",
            "spring banana tree",
            False,
            And(
                oos_has_feather(),
                oos_season_in_mt_cucco(SEASON_SPRING),
                Or(  # can harvest tree
                    oos_has_sword(), oos_has_fools_ore()
                ),
            ),
        ),
        ("mount cucco", "mt. cucco, talon's cave entrance", False, oos_season_in_mt_cucco(SEASON_SPRING)),
        ("mt. cucco, talon's cave entrance", "mount cucco", False, True_()),
        (
            "mt. cucco, talon's cave entrance",
            "talon trade",
            False,
            And(
                Has("Megaphone"),
                Or(oos_is_default_season("SUNKEN_CITY", SEASON_WINTER, False), oos_can_remove_season(SEASON_WINTER)),
            ),
        ),
        ("mt. cucco, talon's cave entrance", "mt. cucco heart piece", False, True_()),
        (
            "mt. cucco, talon's cave entrance",
            "diving spot outside D4",
            False,
            And(
                oos_has_flippers(),
                Or(oos_is_default_season("SUNKEN_CITY", SEASON_WINTER, False), oos_can_remove_season(SEASON_WINTER)),
            ),
        ),
        (
            "mt. cucco, talon's cave entrance",
            "dragon keyhole",
            False,
            And(
                oos_has_winter(),  # to reach cave
                oos_has_feather(),  # to jump in cave
                oos_has_bracelet(),  # to grab the rooster
            ),
        ),
        ("dragon keyhole", "d4 entrance", False, And(Has("Dragon Key"), oos_has_summer())),
        ("d4 entrance", "mt. cucco, talon's cave entrance", False, True_()),
        (
            "mount cucco",
            "goron mountain, across pits",
            False,
            Or(
                Has("Spring Banana"),
                And(
                    oos_option_hard_logic(),
                    oos_can_jump_4_wide_pit(),
                ),
                oos_can_jump_5_wide_pit(),
            ),
        ),
        ("mount cucco", "goron blocked cave entrance", False, Or(oos_can_remove_snow(False), Has("Spring Banana"))),
        ("goron blocked cave entrance", "mount cucco", False, oos_can_remove_snow(False)),
        ("goron blocked cave entrance", "maple encounter", False, oos_can_meet_maple()),
        ("goron blocked cave entrance", "goron mountain", True, oos_has_bracelet()),
        ("goron mountain", "maple encounter", False, oos_can_meet_maple()),
        ("goron blocked cave entrance", "goron's gift", False, oos_can_remove_rockslide(False)),
        (
            "goron mountain",
            "biggoron trade",
            False,
            And(
                oos_can_jump_1_wide_liquid(False),
                Or(
                    Has("Lava Soup"),
                    And(
                        oos_self_locking_item("Goron Mountain: Biggoron Trade", "Lava Soup"),
                        from_option(
                            OracleOfSeasonsIncludeSecretLocations, OracleOfSeasonsIncludeSecretLocations.option_false
                        ),
                    ),
                ),
            ),
        ),
        (
            "goron mountain",
            "chest in goron mountain",
            False,
            And(
                oos_can_jump_3_wide_liquid(),
                Or(
                    oos_has_bombs_for_tiles(),
                    And(  # Bombchu can only destroy the second block, so we need to use cape to jump around the first
                        oos_option_hard_logic(), oos_has_bombchus_for_tiles(), oos_can_use_pegasus_seeds()
                    ),
                    And(oos_option_hell_logic(), oos_has_bombchus_for_tiles(), oos_has_bombchus_for_bombjump()),
                ),
            ),
        ),
        ("goron mountain", "old man in goron mountain", False, oos_can_use_ember_seeds(False)),
        (
            "goron mountain entrance",
            "goron mountain",
            False,
            Or(oos_has_flippers(), oos_can_jump_4_wide_liquid(allow_bombchus=True), oos_has_tight_switch_hook()),
        ),
        (
            "goron mountain",
            "goron mountain entrance",
            False,
            Or(
                oos_has_flippers(),
                oos_can_jump_4_wide_liquid(allow_bombchus=True),
                And(
                    # You can't see the other side from this point
                    oos_option_medium_logic(),
                    oos_has_switch_hook(),
                ),
            ),
        ),
        (
            "goron mountain entrance",
            "temple remains lower stump",
            False,
            Or(
                oos_can_jump_3_wide_pit(),
                And(
                    oos_can_dimitri_clip(),
                    oos_can_jump_2_wide_pit(),
                    Or(
                        # The bombs are actually to clip out of the rock
                        oos_has_bombs_for_bombjump(),
                        oos_has_bombchus_for_bombjump(),
                    ),
                ),
            ),
        ),
        ("temple remains lower stump", "goron mountain entrance", False, oos_can_jump_3_wide_pit()),
        # TARM RUINS ###############################################################################################
        ("spool swamp north", "tarm ruins", False, oos_has_required_jewels()),
        ("tarm ruins", "spool swamp north", False, True_()),
        (
            "tarm ruins",
            "lost woods top statue",
            False,
            And(
                Or(
                    oos_season_in_lost_woods(SEASON_SUMMER),
                    And(
                        oos_season_in_lost_woods(SEASON_AUTUMN),
                        oos_option_medium_logic(),
                        oos_has_magic_boomerang(),
                        Or(oos_can_jump_1_wide_pit(False), oos_option_hard_logic()),
                    ),
                ),
                oos_season_in_lost_woods(SEASON_WINTER),
                oos_can_remove_season(SEASON_WINTER),
            ),
        ),
        (
            "lost woods top statue",
            "lost woods stump",
            False,
            And(
                # Winter has to be in inventory to be here, it allows crossing the water
                oos_has_autumn(),
                oos_can_break_mushroom(False),
            ),
        ),
        (
            "lost woods top statue",
            "lost woods deku",
            False,
            And(
                oos_has_autumn(),
                Or(oos_can_jump_2_wide_liquid(True), oos_can_swim(False)),
                oos_can_break_mushroom(False),
                oos_has_shield(),
            ),
        ),
        ("lost woods stump", "maple encounter", False, oos_can_meet_maple()),
        (
            "lost woods stump",
            "tarm ruins",
            False,
            And(
                oos_season_in_lost_woods(SEASON_AUTUMN),
                oos_can_break_mushroom(False),
                oos_has_winter(),
                from_option(OracleOfSeasonsTarmGateRequirement, 0),
            ),
        ),
        (
            "lost woods stump",
            "lost woods top statue",
            False,
            And(
                oos_season_in_lost_woods(SEASON_AUTUMN),
                oos_has_season(SEASON_WINTER),
                Or(
                    oos_has_season(SEASON_SUMMER),
                    And(
                        oos_has_season(SEASON_AUTUMN),
                        oos_option_medium_logic(),
                        oos_has_magic_boomerang(),
                        Or(oos_can_jump_1_wide_pit(False), oos_option_hard_logic()),
                    ),
                ),
            ),
        ),
        (
            "lost woods stump",
            "lost woods phonograph",
            False,
            And(
                Or(
                    oos_can_remove_snow(False),
                    oos_can_remove_season(SEASON_WINTER),
                ),
                oos_can_use_ember_seeds(False),
                Has("Phonograph"),
            ),
        ),
        ("lost woods stump", "lost woods", False, oos_can_reach_lost_woods_pedestal(False)),
        # When coming back from the eyeglass lake
        ("lost woods", "lost woods stump", False, True_()),
        # To allow reaching the deku if base season is autumn
        (
            "lost woods",
            "lost woods deku",
            False,
            And(
                oos_season_in_tarm_ruins(SEASON_AUTUMN),
                CanReachRegion("lost woods top statue"),
                Or(
                    # A bit tight and diagonal, above water
                    oos_can_jump_3_wide_pit(),
                    oos_can_swim(False),
                ),
                oos_can_break_mushroom(False),
                oos_has_shield(),
            ),
        ),
        # special case for getting to d6 using default season
        (
            "lost woods",
            "d6 sector",
            False,
            And(oos_can_complete_lost_woods_main_sequence(True), oos_option_medium_logic()),
        ),
        ("lost woods stump", "d6 sector", False, oos_can_complete_lost_woods_main_sequence()),
        ("d6 sector", "lost woods stump", False, True_()),
        # special case for getting to pedestal using default season
        ("d6 sector", "lost woods", False, And(oos_can_reach_lost_woods_pedestal(True), oos_option_medium_logic())),
        ("d6 sector", "maple encounter", False, oos_can_meet_maple()),
        ("d6 sector", "tarm ruins tree", False, oos_can_harvest_tree(False)),
        (
            "d6 sector",
            "tarm ruins, under tree",
            False,
            And(oos_season_in_tarm_ruins(SEASON_AUTUMN), oos_can_break_mushroom(False), oos_can_use_ember_seeds(False)),
        ),
        (
            "d6 sector",
            "d6 entrance",
            False,
            And(
                oos_season_in_tarm_ruins(SEASON_WINTER),
                Or(
                    oos_has_shovel(),
                    oos_can_use_ember_seeds(False),
                    And(oos_can_reach_rooster_adventure(), oos_roosters("d6", 1, 0, 0)),
                ),
                oos_season_in_tarm_ruins(SEASON_SPRING),
                oos_can_break_flowers(),
            ),
        ),
        (
            "d6 sector",
            "old man near d6",
            False,
            And(
                oos_season_in_tarm_ruins(SEASON_WINTER),
                oos_can_use_ember_seeds(False),
                Or(
                    And(oos_season_in_tarm_ruins(SEASON_SPRING), oos_can_break_flowers()),
                    And(oos_can_reach_rooster_adventure(), oos_roosters("d6", 1, 1, 0)),
                ),
            ),
        ),
        # When coming from D6 entrance, the pillar needs to be broken during spring to be able to go backwards
        (
            "d6 entrance",
            "d6 sector",
            False,
            And(oos_is_default_season("TARM_RUINS", SEASON_SPRING), oos_can_break_flowers()),
        ),
        # SAMASA DESERT ######################################################################################
        ("suburbs", "samasa desert", False, Has("_met_pirates")),
        ("samasa desert", "samasa desert pit", False, oos_has_bracelet()),
        ("samasa desert", "samasa desert chest", False, oos_has_flippers()),
        (
            "samasa desert",
            "samasa desert scrub",
            False,
            oos_has_rupees_for_shop("samasaCaveScrub"),
            bool(options.shuffle_business_scrubs),
        ),
        ("samasa desert", "subrosia pirates sector", False, True_()),
        # d11 in samasa rules
        (
            "samasa desert",
            "d11 entrance",
            True,
            True_(),
            options.linked_heros_cave.is_samasa,
        ),
        (
            "samasa desert",
            "d11 alt entrance",
            False,
            oos_can_break_bush(),
            options.linked_heros_cave.is_alt_entrance,
        ),
        # TEMPLE REMAINS ####################################################################################
        ("temple remains lower stump", "maple encounter", False, oos_can_meet_maple()),
        (
            "temple remains lower stump",
            "temple remains upper stump",
            False,
            And(
                oos_has_feather(),  # Require feather in case volcano has erupted
                oos_can_break_bush(False, False),
                Or(
                    Has("_triggered_volcano"),  # Volcano rule
                    And(  # Winter rule
                        oos_season_in_temple_remains(SEASON_WINTER),
                        oos_can_remove_snow(False),
                        oos_can_jump_6_wide_pit(),
                    ),
                    And(  # Summer rule
                        oos_season_in_temple_remains(SEASON_SUMMER), oos_can_jump_6_wide_pit()
                    ),
                    And(  # Spring rule
                        oos_season_in_temple_remains(SEASON_SPRING), oos_can_break_flowers(), oos_can_jump_6_wide_pit()
                    ),
                    oos_season_in_temple_remains(SEASON_AUTUMN),  # Autumn rule
                ),
            ),
        ),
        (
            "temple remains upper stump",
            "temple remains lower stump",
            False,
            And(
                oos_has_feather(),  # Require feather in case volcano has erupted
                Or(
                    Has("_triggered_volcano"),  # Volcano rule
                    oos_season_in_temple_remains(SEASON_WINTER),  # Winter rule
                    And(  # Summer rule
                        oos_season_in_temple_remains(SEASON_SUMMER),
                        oos_can_break_bush(False, False),
                        oos_can_jump_6_wide_pit(),
                    ),
                    And(  # Spring rule
                        oos_season_in_temple_remains(SEASON_SPRING),
                        oos_can_break_flowers(),
                        oos_can_break_bush(False, False),
                        oos_can_jump_6_wide_pit(),
                    ),
                    And(  # Autumn rule
                        oos_season_in_temple_remains(SEASON_AUTUMN), oos_can_break_bush()
                    ),
                ),
            ),
        ),
        (
            "temple remains lower stump",
            "temple remains lower portal access",
            False,
            And(Has("_triggered_volcano"), oos_has_feather()),
        ),
        (
            "temple remains upper stump",
            "temple remains lower portal access",
            False,
            And(
                oos_has_feather(),
                Or(
                    oos_has_winter(),
                    Has("_triggered_volcano"),
                    And(
                        # You can only reach the portal from here with the default Winter,
                        # if you made the zipper jump first
                        # Otherwise you would have turned it Autumn first
                        oos_season_in_temple_remains(SEASON_WINTER),
                        oos_can_remove_snow(False),
                        oos_can_break_bush(False),
                        oos_can_jump_6_wide_pit(),
                    ),
                ),
            ),
        ),
        ("temple remains lower portal access", "temple remains lower portal", True, True_()),
        # There is an added ledge in rando that enables jumping from the portal down to the stump,
        # whatever the season is
        ("temple remains lower portal", "temple remains lower stump", False, True_()),
        (
            "temple remains lower stump",
            "temple remains heart piece",
            False,
            And(
                Has("_triggered_volcano"),
                oos_can_jump_2_wide_liquid(),
                oos_can_remove_rockslide(False),
            ),
        ),
        (
            "temple remains lower stump",
            "temple remains upper portal",
            False,
            And(
                Has("_triggered_volcano"),
                oos_season_in_temple_remains(SEASON_SUMMER),
                oos_can_jump_2_wide_liquid(),
                Or(oos_has_magnet_gloves(), oos_can_jump_6_wide_pit()),
            ),
        ),
        (
            "temple remains upper portal",
            "temple remains lower stump",
            False,
            And(Has("_triggered_volcano"), oos_can_jump_1_wide_liquid(False)),
        ),
        ("temple remains upper portal", "temple remains upper stump", False, oos_can_jump_1_wide_pit(False)),
        (
            "temple remains upper portal",
            "temple remains lower portal access",
            False,
            And(
                oos_has_feather(),  # Require feather in case volcano has erupted
                Or(Has("_triggered_volcano"), oos_is_default_season("TEMPLE_REMAINS", SEASON_WINTER)),
            ),
        ),
        # ONOX CASTLE #############################################################################################
        ("maku tree", "maku seed", False, oos_has_essences_for_maku_seed()),
        ("maku tree", "maku tree, 3 essences", False, oos_has_essences(3)),
        ("maku tree", "maku tree, 5 essences", False, oos_has_essences(5)),
        ("maku tree", "maku tree, 7 essences", False, oos_has_essences(7)),
        ("north horon", "d9 entrance", False, CanReachRegion("maku seed")),
        (
            "d9 entrance",
            "onox beaten",
            False,
            And(
                oos_can_kill_armored_enemy(True, True),
                oos_can_kill_facade(),
                oos_has_sword(False),
                oos_has_feather(),
                Or(oos_option_hard_logic(), oos_has_rod()),
                oos_has_hearts_by_difficulty(8, 6, 4),
            ),
        ),
        (
            "onox beaten",
            "ganon beaten",
            False,
            Or(
                And(
                    # casual rules
                    oos_has_noble_sword(),
                    oos_has_seed_thrower(),
                    oos_can_use_ember_seeds(False),
                    oos_can_use_mystery_seeds(),
                ),
                And(
                    oos_option_medium_logic(),
                    oos_has_sword(False),
                    Or(
                        # all seeds damage Twinrova phase 2
                        oos_has_seed_thrower(),
                        And(
                            oos_option_hard_logic(),
                            oos_can_use_seeds(),
                            # satchel can't use pegasus to damage, but all others work
                            Or(
                                oos_has_ember_seeds(),
                                oos_has_mystery_seeds(),
                                oos_has_scent_seeds(),
                                oos_has_gale_seeds(),
                            ),
                        ),
                    ),
                ),
            ),
        ),
        # GOLDEN BEASTS #############################################################################################
        (
            "d0 entrance",
            "golden darknut",
            False,
            And(
                Or(
                    oos_is_default_season("WESTERN_COAST", SEASON_SPRING),
                    And(
                        oos_season_in_western_coast(SEASON_SPRING),
                        Has("Pirate's Bell"),
                        Has("_met_pirates"),
                    ),
                ),
                Or(
                    oos_has_sword(),
                    oos_has_fools_ore(),
                    oos_can_summon_dimitri(),
                    And(oos_option_hard_logic(), oos_has_cane()),
                ),
            ),
        ),
        (
            "lost woods top statue",
            "golden lynel",
            False,
            Or(oos_has_sword(), oos_has_fools_ore(), And(oos_option_hard_logic(), oos_has_cane())),
        ),
        (
            "lost woods stump",
            "golden lynel",
            False,
            And(
                # We can assume coming from d6 or pedestal otherwise rule above applies
                oos_season_in_lost_woods(SEASON_AUTUMN),
                oos_can_break_mushroom(False),
                oos_has_winter(),
                Or(oos_has_sword(), oos_has_fools_ore(), And(oos_option_hard_logic(), oos_has_cane())),
            ),
        ),
        (
            "d2 entrance",
            "golden moblin",
            False,
            And(
                oos_season_in_central_woods_of_winter(SEASON_AUTUMN),
                Or(
                    oos_has_sword(),
                    oos_has_fools_ore(),
                    # Moblin has the interesting property of being one-shottable using an ember seed
                    And(oos_option_medium_logic(), oos_can_use_ember_seeds(True)),
                    oos_can_summon_dimitri(),
                    And(oos_option_hard_logic(), oos_has_cane()),
                ),
            ),
        ),
        (
            "spool swamp south (summer)",
            "golden octorok",
            False,
            Or(
                oos_has_sword(),
                oos_has_fools_ore(),
                oos_can_summon_dimitri(),
                And(oos_option_hard_logic(), oos_has_cane()),
            ),
        ),
        # GASHA TREES #############################################################################################
        ("horon village", "horon gasha spot", False, True_(), options.deterministic_gasha_locations >= 1),
        (
            "impa's house",
            "impa gasha spot",
            False,
            oos_can_break_bush(True, True),
            options.deterministic_gasha_locations >= 1,
        ),
        (
            "suburbs",
            "suburbs gasha spot",
            False,
            oos_can_break_bush(True, True),
            options.deterministic_gasha_locations >= 1,
        ),
        (
            "ghastly stump",
            "holodrum plain gasha spot",
            False,
            And(
                oos_can_break_bush(True, False),  # Zoras make the bombchus not viable
                oos_has_shovel(),
            ),
            options.deterministic_gasha_locations >= 1,
        ),
        (
            "d1 island",
            "holodrum plain island gasha spot",
            False,
            And(
                oos_can_swim(True),
                Or(
                    oos_can_break_bush(False, False),
                    oos_can_summon_dimitri(),  # Only Dimitri can be brought here
                ),
            ),
            options.deterministic_gasha_locations >= 1,
        ),
        (
            "floodgate keyhole",
            "spool swamp north gasha spot",
            False,
            oos_has_bracelet(),
            options.deterministic_gasha_locations >= 1,
        ),
        (
            "spool swamp south near gasha spot",
            "spool swamp south gasha spot",
            False,
            oos_has_bracelet(),
            options.deterministic_gasha_locations >= 1,
        ),
        (
            "sunken city",
            "sunken city gasha spot",
            False,
            And(
                oos_season_in_sunken_city(SEASON_SUMMER),
                oos_can_swim(False),
                oos_can_break_bush(False, False),  # Technically doable by positioning link with a sword
            ),
            options.deterministic_gasha_locations >= 1,
        ),
        ("sunken city dimitri", "sunken city gasha spot", False, True_(), options.deterministic_gasha_locations >= 1),
        (
            "goron mountain entrance",
            "goron mountain left gasha spot",
            False,
            oos_has_shovel(),
            options.deterministic_gasha_locations >= 1,
        ),
        (
            "goron mountain entrance",
            "goron mountain right gasha spot",
            False,
            oos_has_bracelet(),
            options.deterministic_gasha_locations >= 1,
        ),
        (
            "d5 stump",
            "eyeglass lake gasha spot",
            False,
            And(
                oos_has_shovel(),
                oos_can_break_bush(True, True),
            ),
            options.deterministic_gasha_locations >= 1,
        ),
        (
            "mount cucco",
            "mt cucco gasha spot",
            False,
            And(
                oos_season_in_mt_cucco(SEASON_AUTUMN),
                oos_can_break_mushroom(False),
            ),
            options.deterministic_gasha_locations >= 1,
        ),
        ("d6 sector", "tarm ruins gasha spot", False, oos_has_shovel(), options.deterministic_gasha_locations >= 1),
        ("samasa desert", "samasa desert gasha spot", False, True_(), options.deterministic_gasha_locations >= 1),
        (
            "western coast after ship",
            "western coast gasha spot",
            False,
            True_(),
            options.deterministic_gasha_locations >= 1,
        ),
        ("north horon", "onox gasha spot", False, oos_has_shovel(), options.deterministic_gasha_locations >= 1),
        ("natzu west", "natzu west (ricky)", True, True_(), options.animal_companion == "ricky"),
        ("natzu west (ricky)", "natzu east (ricky)", True, oos_can_summon_ricky(), options.animal_companion == "ricky"),
        ("natzu east (ricky)", "sunken city entrance", True, True_(), options.animal_companion == "ricky"),
        ("natzu east (ricky)", "moblin keep bridge", False, True_(), options.animal_companion == "ricky"),
        ("natzu east (ricky)", "natzu river bank", True, oos_can_summon_ricky(), options.animal_companion == "ricky"),
        (
            "natzu east (ricky)",
            "natzu deku",
            False,
            oos_can_break_bush(True),
            bool(options.animal_companion == "ricky" and options.secret_locations),
        ),
        ("natzu west", "natzu west (dimitri)", True, True_(), options.animal_companion == "dimitri"),
        (
            "natzu west (dimitri)",
            "natzu east (dimitri)",
            True,
            oos_can_swim(True),
            options.animal_companion == "dimitri",
        ),
        (
            "natzu east (dimitri)",
            "sunken city entrance",
            True,
            oos_can_jump_1_wide_pit(False),
            options.animal_companion == "dimitri",
        ),
        (
            "natzu east (dimitri)",
            "natzu region, across water",
            False,
            oos_can_jump_5_wide_liquid(),
            options.animal_companion == "dimitri",
        ),
        (
            "natzu east (dimitri)",
            "moblin keep bridge",
            False,
            Or(oos_can_summon_dimitri(), And(oos_option_medium_logic(), oos_has_flippers(), Has("Swimmer's Ring"))),
            options.animal_companion == "dimitri",
        ),
        ("natzu east (dimitri)", "natzu river bank", True, True_(), options.animal_companion == "dimitri"),
        (
            "natzu west (dimitri)",
            "natzu deku",
            False,
            oos_can_summon_dimitri(),
            bool(options.animal_companion == "dimitri" and options.secret_locations),
        ),
        ("sunken city entrance", "moblin keep", False, oos_can_dimitri_clip(), options.animal_companion == "dimitri"),
        (
            "moblin keep bridge",
            "natzu east (dimitri)",
            False,
            oos_can_swim(True),
            options.animal_companion == "dimitri",
        ),
        ("natzu west", "natzu west (moosh)", True, True_(), options.animal_companion == "moosh"),
        (
            "natzu west (moosh)",
            "natzu east (moosh)",
            True,
            Or(
                oos_can_summon_moosh(),
                And(oos_option_medium_logic(), oos_can_break_bush(True), oos_can_jump_3_wide_pit()),
            ),
            options.animal_companion == "moosh",
        ),
        (
            "natzu east (moosh)",
            "sunken city entrance",
            True,
            Or(
                oos_can_summon_moosh(),
                oos_can_jump_3_wide_liquid(),  # Not a liquid, but it's a diagonal jump so that's the same
            ),
            options.animal_companion == "moosh",
        ),
        (
            "natzu east (moosh)",
            "moblin keep bridge",
            False,
            Or(oos_can_summon_moosh(), And(oos_can_break_bush(), oos_can_jump_3_wide_pit())),
            options.animal_companion == "moosh",
        ),
        ("natzu east (moosh)", "natzu river bank", True, True_(), options.animal_companion == "moosh"),
        (
            "natzu west (moosh)",
            "natzu deku",
            False,
            Or(
                oos_can_summon_moosh(),
                oos_can_jump_4_wide_liquid(),
                And(oos_can_jump_4_wide_pit(), oos_can_break_bush()),
            ),
            bool(options.animal_companion == "moosh" and options.secret_locations),
        ),
        (
            "d4 entrance",
            "dragon keyhole",
            False,
            And(
                # Rule specifically to get to the dragon keyhole from a side entrance,
                # only useful for rooster's adventure
                oos_is_default_season("SUNKEN_CITY", SEASON_WINTER),  # to reach cave
                oos_has_feather(),  # to jump in cave
                oos_has_bracelet(),  # to grab the rooster
            ),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        # Item assumptions for the rest of that logic :
        # Bracelet
        # Feather
        (
            "dragon keyhole",
            "rooster adventure",
            False,
            And(oos_has_gale_seeds(), oos_has_satchel(), Or(oos_has_shovel(), Has("Spring Banana"))),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "goron mountain entrance",
            False,
            oos_roosters("cucco mountain", 0, 0, 0),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "moblin keep",
            False,
            Or(
                And(oos_roosters("sunken", 1, 1, 0), oos_is_companion_ricky()),
                And(
                    oos_roosters("horon", 1, 1, 0),
                    Or(oos_has_flute(), And(oos_is_companion_moosh(), oos_can_jump_3_wide_pit())),
                ),
            ),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "sunken city entrance",
            False,
            oos_roosters("sunken", 0, 0, 0),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "sunken city gasha spot",
            False,
            And(oos_roosters("sunken", 1, 0, 1), oos_season_in_sunken_city(SEASON_WINTER)),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell
            and options.deterministic_gasha_locations >= 1,
        ),
        (
            "rooster adventure",
            "syrup trade",
            False,
            And(oos_roosters("sunken", 1, 0, 1), Has("Mushroom")),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "suburbs",
            False,
            oos_roosters("suburbs", 0, 0, 0),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "eastern suburbs spring cave",
            False,
            And(
                oos_roosters("suburbs", 1, 0, 1),
                oos_season_in_eastern_suburbs(SEASON_SPRING),
                Or(oos_has_magnet_gloves(), oos_can_jump_3_wide_pit()),
            ),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "windmill heart piece",
            False,
            oos_roosters("suburbs", 1, 1, 0),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "samasa desert chest",
            False,
            And(
                oos_roosters("suburbs", 1, 1, 0),
                Has("_met_pirates"),
            ),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "moblin road",
            False,
            oos_roosters("moblin road", 0, 0, 0),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "holly's house",
            False,
            oos_roosters("moblin road", 1, 1, 0),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "horon heart piece",
            False,
            oos_roosters("horon", 1, 1, 0),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "graveyard heart piece",
            False,
            And(
                oos_roosters("horon", 1, 1, 0),
                Has("_met_pirates"),
                Has("Pirate's Bell"),
                oos_is_default_season("WESTERN_COAST", SEASON_SUMMER),
            ),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "spool swamp north",
            False,
            oos_roosters("swamp", 0, 0, 0),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "lost woods deku",
            False,
            And(
                oos_roosters("swamp", 1, 1, 0),
                oos_has_required_jewels(),
                Or(oos_season_in_lost_woods(SEASON_SUMMER), CanReachRegion("lost woods top statue")),
            ),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "spool swamp cave",
            False,
            Or(
                And(
                    oos_can_swim(True),
                    oos_roosters("horon", 0, 0, 0),
                ),
                And(
                    # We can assume jump 3 holes here, coming from the north
                    Has("Floodgate Key"),
                    Or(
                        oos_is_default_season("SPOOL_SWAMP", SEASON_SPRING, False), oos_can_remove_season(SEASON_SPRING)
                    ),
                    oos_roosters("swamp", 0, 0, 0),
                ),
            ),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "temple remains upper stump",
            False,
            And(
                oos_can_jump_3_wide_pit(),
                oos_roosters("cucco mountain", 0, 0, 0),
                Or(
                    # autumn doesn't matter since regular logic already covers that case
                    oos_season_in_temple_remains(SEASON_SUMMER),
                    And(oos_season_in_temple_remains(SEASON_WINTER), oos_has_shovel()),
                    And(oos_season_in_temple_remains(SEASON_SPRING), oos_can_break_flowers()),
                ),
            ),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
        (
            "rooster adventure",
            "temple remains upper portal",
            False,
            And(
                Has("_triggered_volcano"),
                oos_can_jump_3_wide_pit(),
                oos_roosters("cucco mountain", 1, 1, 0),
                Or(oos_has_magnet_gloves(), oos_can_jump_6_wide_pit()),
            ),
            options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell,
        ),
    ]
