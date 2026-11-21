from typing import TYPE_CHECKING

from worlds.deltarune.Options import (
    ChosenRoute,
    IncludeMike,
    IncludeUnusedItems,
    RandomizeChapters,
    RandomizeSecretBosses,
    RockVideoSanity,
    UnlockCharacters,
)

if TYPE_CHECKING:
    from . import DeltaruneWorld

def include_hidden_items_chapter2_weird_route_exclusion(world: "DeltaruneWorld") -> bool:
    return include_hidden_items(world) and not_weird_route_only(world)


def include_secret_bosses_items_requirement_chapter2_weird_route_exclusion(world: "DeltaruneWorld") -> bool:
    return include_secret_bosses_items_requirement(world) and not_weird_route_only(world)


def include_secret_bosses_items_reward(world: "DeltaruneWorld") -> bool:
    return (
        world.options.randomize_secret_bosses.value == RandomizeSecretBosses.option_true
        or are_secret_bosses_mandatory(world)
    )


def include_secret_bosses_items_reward_chapter2_weird_route_exclusion(world: "DeltaruneWorld") -> bool:
    return include_secret_bosses_items_reward(world) and not_weird_route_only(world)


def include_recruits_chapter1(world: "DeltaruneWorld") -> bool:
    return include_recruits(world) and world.options.chapter_1_recruit.value == 1


def include_lose_recruits_chapter1(world: "DeltaruneWorld") -> bool:
    return include_lose_recruits(world) and world.options.chapter_1_recruit.value == 1


def include_freeze_recruits_chapter2(world: "DeltaruneWorld") -> bool:
    return include_lose_recruits(world) or weird_route(world)


def not_include_lose_recruits(world: "DeltaruneWorld") -> bool:
    return not include_lose_recruits(world)


def include_recruits(world: "DeltaruneWorld") -> bool:
    return world.options.recruits_sanity.value == 1


def include_lose_recruits(world: "DeltaruneWorld"):
    return world.options.lose_recruits_sanity.value == 1


def include_recruits_chapter2_weird_route_exclusion(world: "DeltaruneWorld"):
    return include_recruits(world) and not_weird_route_only(world)


def include_singapour_wrong_warp_locations(world: "DeltaruneWorld"):
    return not_weird_route_only(world) or is_speedrun_logic(world)


def include_singapour_wrong_warp_locations_recruit(world: "DeltaruneWorld"):
    return include_singapour_wrong_warp_locations(world) and include_recruits(world)


def include_singapour_wrong_warp_locations_lose_recruits(world: "DeltaruneWorld"):
    return include_singapour_wrong_warp_locations(world) and include_lose_recruits(world)


def include_twin_ribbon_fusion(world: "DeltaruneWorld"):
    return (
        can_access_fusion(world)
        and any_included_chapter(world, [2, 3])
        and (
            (starting_equipment_removed(world) and any_included_chapter(world, [1, 3]))
            or (not starting_equipment_removed(world) and any_included_chapter(world, [1, 2, 3]))
        )
    )


def include_spike_band_fusion(world: "DeltaruneWorld"):
    return (
        can_access_fusion(world)
        and included_chapter(world, 1)
        and (
            included_chapter(world, 2)
            or (
                not starting_equipment_removed(world)
                and (included_chapter(world, 4) or all_included_chapter(world, [3, 4]))
            )
        )
    )


def include_tensionbow_fusion(world: "DeltaruneWorld"):
    return can_access_fusion(world) and included_chapter(world, 2) and (normal_route(world))


def include_twistedsword_fusion(world: "DeltaruneWorld"):
    return (
        can_access_fusion(world) and included_chapter(world, 2) and include_unused_items(world) and weird_route(world)
    )


def include_truetie_fusion(world: "DeltaruneWorld"):
    return (
        can_access_fusion_post_chapter_5(world)
        # frayed bowtie
        and included_chapter(world, 2)
        and not_weird_route_only(world)
        # tennatie
        and included_chapter(world, 3)
    )


def include_lost_rabbick(world: "DeltaruneWorld"):
    return include_lose_recruits(world) and (
        included_chapter(world, 3) or (included_chapter(world, 1) and include_lose_recruits_chapter1(world))
    )


def include_monarchrbn_fusion(world: "DeltaruneWorld"):
    return can_access_fusion_post_chapter_5(world) and included_chapter(world, 4)


def include_tvdinner_fusion(world: "DeltaruneWorld"):
    return can_access_fusion_post_chapter_5(world) and included_chapter(world, 3)


def include_deluxedinner_fusion(world: "DeltaruneWorld"):
    return can_access_fusion_post_chapter_5(world) and included_chapter(world, 3)


def include_punchbowl_fusion(world: "DeltaruneWorld"):
    return can_access_fusion_post_chapter_5(world) and included_chapter(world, 4)


def include_tensionmax_fusion(world: "DeltaruneWorld"):
    return can_access_fusion_post_chapter_5(world) and included_chapter(world, 4)


def include_dogwidow_fusion(world: "DeltaruneWorld"):
    return can_access_fusion_post_chapter_5(world) and included_chapter(world, 4)


def include_lancer_cookie(world: "DeltaruneWorld"):
    return any_included_chapter(world, [1, 2, 4])


def physical_challenge_sanity_enabled(world: "DeltaruneWorld") -> bool:
    return world.options.physical_challenge_rank_sanity.value == 1


def rock_video_sanity_enabled(world: "DeltaruneWorld") -> bool:
    return have_access_to_rock_video(world) and world.options.rock_video_sanity.value in [
        RockVideoSanity.option_normal_only,
        RockVideoSanity.option_true,
    ]


def rock_video_sanity_hard_enabled(world: "DeltaruneWorld") -> bool:
    return have_access_to_rock_video(world) and world.options.rock_video_sanity.value == RockVideoSanity.option_true


def rock_video_sanity_enabled_ch5(world: "DeltaruneWorld") -> bool:
    return rock_video_sanity_enabled(world) and have_access_to_rock_video_ch5(world)


def rock_video_sanity_hard_enabled_ch5(world: "DeltaruneWorld") -> bool:
    return rock_video_sanity_hard_enabled(world) and have_access_to_rock_video_ch5(world)


def have_access_to_rock_video_ch5(world: "DeltaruneWorld") -> bool:
    return included_chapter(world, 5) and not_weird_route_only(world)


def have_access_to_rock_video(world: "DeltaruneWorld") -> bool:
    return included_chapter(world, 4) or have_access_to_rock_video_ch5(world)


# region Direct Option Read


def weird_route(world: "DeltaruneWorld") -> bool:
    return world.options.chosen_route.value in [
        ChosenRoute.option_side_b,
        ChosenRoute.option_both_all_recruits_and_side_b,
    ]


def not_weird_route_only(world: "DeltaruneWorld") -> bool:
    return world.options.chosen_route.value != ChosenRoute.option_side_b


def all_recruits_route(world: "DeltaruneWorld") -> bool:
    return world.options.chosen_route.value in [
        ChosenRoute.option_all_recruits,
        ChosenRoute.option_both_all_recruits_and_side_b,
    ]


def both_routes(world: "DeltaruneWorld") -> bool:
    return world.options.chosen_route == ChosenRoute.option_both_all_recruits_and_side_b


def normal_route(world: "DeltaruneWorld") -> bool:
    return world.options.chosen_route.value in [
        ChosenRoute.option_all_recruits,
        ChosenRoute.option_normal_route,
        ChosenRoute.option_both_all_recruits_and_side_b,
    ]


def include_mike_battle(world: "DeltaruneWorld") -> bool:
    return world.options.include_mike.value in [
        IncludeMike.option_battle_only,
        IncludeMike.option_battle_and_games,
    ]


def include_mike_games(world: "DeltaruneWorld") -> bool:
    return world.options.include_mike.value == IncludeMike.option_battle_and_games


def randomized_sword_route(world: "DeltaruneWorld") -> bool:
    return world.options.randomize_sword_route.value == 1


def shadow_mantle_holder_as_secret_boss(world: "DeltaruneWorld") -> bool:
    return world.options.shadow_mantle_holder_as_secret_boss.value == 1


def include_shadow_mantle(world: "DeltaruneWorld") -> bool:
    return world.options.include_shadow_mantle.value == 1


def mysterykey_from_pink_coins(world: "DeltaruneWorld") -> bool:
    return world.options.mysterykey_from_pink_coins.value == 1


def doorkey_from_broken_keys(world: "DeltaruneWorld") -> bool:
    return world.options.door_key_from_broken_keys.value == 1


def include_mysterykey(world: "DeltaruneWorld") -> bool:
    return include_secret_bosses_items_requirement(world) and not mysterykey_from_pink_coins(world)


def include_doorkey(world: "DeltaruneWorld") -> bool:
    return include_secret_bosses_items_requirement(world) and not doorkey_from_broken_keys(world)


def include_hidden_items(world: "DeltaruneWorld") -> bool:
    return world.options.include_hidden_items.value == 1


def include_secret_bosses_items_requirement(world: "DeltaruneWorld") -> bool:
    return world.options.include_secret_bosses_items_requirement.value == 1


def are_secret_bosses_mandatory(world: "DeltaruneWorld"):
    return world.options.randomize_secret_bosses.value == RandomizeSecretBosses.option_mandatory

def include_everybodyweapon(world: "DeltaruneWorld") -> bool:
    return world.options.include_unused_items.value == IncludeUnusedItems.option_true


def randomized_chapters(world: "DeltaruneWorld") -> bool:
    return world.options.randomize_chapters.value == RandomizeChapters.option_randomized


def chapters_in_order(world: "DeltaruneWorld") -> bool:
    return world.options.randomize_chapters.value == RandomizeChapters.option_in_order


def all_chapter_unlocked(world: "DeltaruneWorld") -> bool:
    return world.options.randomize_chapters.value == RandomizeChapters.option_all_unlocked

def starting_equipment_removed(world: "DeltaruneWorld"):
    return world.options.remove_starting_equipment.value == 1


def progressive_weapons_kris(world: "DeltaruneWorld"):
    return world.options.progressive_kris_weapons.value == 1


def progressive_weapons_susie(world: "DeltaruneWorld"):
    return world.options.progressive_susie_weapons.value == 1


def progressive_weapons_ralsei(world: "DeltaruneWorld"):
    return world.options.progressive_ralsei_weapons.value == 1


def progressive_weapons_noelle(world: "DeltaruneWorld"):
    return world.options.progressive_noelle_weapons.value == 1 and included_chapter(world, 2)

def progressive_area_unlocks(world: "DeltaruneWorld"):
    return world.options.progressive_area_unlocks.value == 1

def not_progressive_area_unlocks(world: "DeltaruneWorld"):
    return world.options.progressive_area_unlocks.value == 0

def normal_route_and_not_progressive_area_unlocks(world: "DeltaruneWorld"):
    return world.options.progressive_area_unlocks.value == 0 and normal_route(world)

def include_characters(world: "DeltaruneWorld"):
    return world.options.unlock_characters.value in [
        UnlockCharacters.option_true,
        UnlockCharacters.option_except_kris,
    ]


def include_kris(world: "DeltaruneWorld"):
    return world.options.unlock_characters.value == UnlockCharacters.option_true


def include_noelle(world: "DeltaruneWorld"):
    return include_characters(world) and included_chapter(world, 2)


def include_actions(world: "DeltaruneWorld"):
    return world.options.unlock_fun_gang_actions.value == 1 and any_included_chapter(world, [2, 3, 4, 5])


def include_unused_items(world: "DeltaruneWorld") -> bool:
    return world.options.include_unused_items.value in [
        IncludeUnusedItems.option_true,
        IncludeUnusedItems.option_true_without_everybodyweapon,
    ]


def excluded_t_rank_board(world: "DeltaruneWorld") -> bool:
    return world.options.exclude_t_rank_board.value == 1


def excluded_z_rank_board(world: "DeltaruneWorld") -> bool:
    return world.options.exclude_z_rank_board.value == 1


def excluded_t_rank_physical_challenge(world: "DeltaruneWorld") -> bool:
    return world.options.exclude_t_rank_physical_challenge.value == 1


def excluded_z_rank_physical_challenge(world: "DeltaruneWorld") -> bool:
    return world.options.exclude_z_rank_physical_challenge.value == 1


# endregion

# region Fusion Access


def can_access_fusion(world: "DeltaruneWorld"):
    if world.options.chosen_route.value == ChosenRoute.option_side_b:
        return any_included_chapter(world, [2, 4])
    else:
        return any_included_chapter(world, [2, 4, 5])


def can_access_fusion_post_chapter_5(world: "DeltaruneWorld"):
    if world.options.chosen_route.value == ChosenRoute.option_side_b:
        return False
    else:
        return any_included_chapter(world, [5])


# endregion


# region Chapter Inclusion


def included_chapter(world: "DeltaruneWorld", chapter: int) -> bool:
    return chapter in world.included_chapters


def any_included_chapter(world: "DeltaruneWorld", chapters: list[int]):
    return any(chapter in world.included_chapters for chapter in chapters)


def all_included_chapter(world: "DeltaruneWorld", chapters: list[int]):
    return all(chapter in world.included_chapters for chapter in chapters)


# endregion


# region Logic Difficulty


def is_speedrun_logic(world: "DeltaruneWorld") -> bool:
    return world.options.speedrun_gliches_as_logic == 1

def nohit_easy_as_logic(world: "DeltaruneWorld") -> bool:
    return world.options.nohit_as_logic.value >= IncludeUnusedItems.option_easy

def nohit_hard_as_logic(world: "DeltaruneWorld") -> bool:
    return world.options.nohit_as_logic.value >= IncludeUnusedItems.option_hard

def nohit_extreme_as_logic(world: "DeltaruneWorld") -> bool:
    return world.options.nohit_as_logic.value >= IncludeUnusedItems.option_extreme

def is_annoying_logic(world: "DeltaruneWorld") -> bool:
    return world.options.annoying_farming_as_logic == 1


# endregion
