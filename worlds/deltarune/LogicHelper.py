from typing import TYPE_CHECKING

from worlds.deltarune.Options import (
    ChosenRoute,
    IncludeMike,
    IncludeUnusedItems,
    RandomizeChapters,
    RandomizeMANTLE,
    RandomizeSecretBosses,
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


def include_recruit_swatchlings_weird_route(world: "DeltaruneWorld"):
    return include_recruits(world) and (
        world.options.include_swatchling_during_weird_route == 1 or not_weird_route_only(world)
    )


def include_lose_swatchlings_weird_route(world: "DeltaruneWorld"):
    return include_lose_recruits(world) and (
        world.options.include_swatchling_during_weird_route == 1 or not_weird_route_only(world)
    )


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


# region Direct Option Read


def weird_route(world: "DeltaruneWorld") -> bool:
    return world.options.chosen_route.value in [
        ChosenRoute.option_weird_route,
        ChosenRoute.option_both_all_recruits_and_weird_route,
    ]


def not_weird_route_only(world: "DeltaruneWorld") -> bool:
    return world.options.chosen_route.value != ChosenRoute.option_weird_route


def all_recruits_route(world: "DeltaruneWorld") -> bool:
    return world.options.chosen_route.value in [
        ChosenRoute.option_all_recruits,
        ChosenRoute.option_both_all_recruits_and_weird_route,
    ]


def both_routes(world: "DeltaruneWorld") -> bool:
    return world.options.chosen_route == ChosenRoute.option_both_all_recruits_and_weird_route


def normal_route(world: "DeltaruneWorld") -> bool:
    return world.options.chosen_route.value in [
        ChosenRoute.option_all_recruits,
        ChosenRoute.option_normal_route,
        ChosenRoute.option_both_all_recruits_and_weird_route,
    ]


def include_mike_battle(world: "DeltaruneWorld") -> bool:
    return world.options.include_mike.value in [
        IncludeMike.option_battle_only,
        IncludeMike.option_battle_and_games,
    ]


def include_mike_games(world: "DeltaruneWorld") -> bool:
    return world.options.include_mike.value == IncludeMike.option_battle_and_games


def include_mantle(world: "DeltaruneWorld") -> bool:
    return world.options.randomize_mantle.value != RandomizeMANTLE.option_mantleless


def randomized_mantle(world: "DeltaruneWorld") -> bool:
    return world.options.randomize_mantle.value in [RandomizeMANTLE.option_true, RandomizeMANTLE.option_mantleless]


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


def excluded_t_rank(world: "DeltaruneWorld") -> bool:
    return world.options.exclude_t_rank.value == 1


def excluded_z_rank(world: "DeltaruneWorld") -> bool:
    return world.options.exclude_z_rank.value == 1


# endregion

# region Fusion Access


def can_access_fusion(world: "DeltaruneWorld"):
    if world.options.chosen_route.value == ChosenRoute.option_weird_route:
        return any_included_chapter(world, [2, 4])
    else:
        return any_included_chapter(world, [2, 4, 5])


def can_access_fusion_post_chapter_5(world: "DeltaruneWorld"):
    if world.options.chosen_route.value == ChosenRoute.option_weird_route:
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
