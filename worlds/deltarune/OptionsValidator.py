import logging
from typing import TYPE_CHECKING

from Options import OptionError
from worlds.deltarune.LogicHelper import (
    all_recruits_route,
    include_lose_recruits,
    include_recruits,
    randomized_chapters,
)
from worlds.deltarune.Options import ChosenRoute, StartingChapter

if TYPE_CHECKING:
    from . import DeltaruneWorld


def validate_options(world: "DeltaruneWorld"):
    validate_chapter5_weird_route_only_random_prevention(world)
    validate_playable_chapters(world)
    validate_starting_chapter(world)
    validate_all_recruits(world)


def validate_chapter5_weird_route_only_random_prevention(world: "DeltaruneWorld"):
    if world.included_chapters == [5] and world.options.chosen_route.value == ChosenRoute.option_weird_route:
        if world.options.random_safety_chapter_inclusion.value == 1:
            chapter = 5
            while chapter == 5:
                chapter = world.random.randint(1, world.max_deltarune_chapter)

                if chapter == 5:
                    logging.info(
                        f"[DELTARUNE] {world.player_name} triggered 'Chapter 5 Weird Route Only Inclusion Safety'. Chapter {chapter} has been randomly chosen. (So we will reroll)"
                    )
                else:
                    setattr(world.options, f"include_chapter_{chapter}.value", 1)
                    logging.info(
                        f"[DELTARUNE] {world.player_name} triggered 'Chapter 5 Weird Route Only Inclusion Safety'. Chapter {chapter} has been randomly enabled."
                    )


def validate_playable_chapters(world: "DeltaruneWorld"):
    if len(world.included_chapters) == 0:
        if world.options.random_safety_chapter_inclusion.value == 1:
            chapter = world.random.randint(1, world.max_deltarune_chapter)
            setattr(world.options, f"include_chapter_{chapter}.value", 1)
            logging.info(
                f"[DELTARUNE] {world.player_name} triggered 'Random Chapter Inclusion Safety'. Chapter {chapter} has been randomly enabled."
            )
        else:
            raise OptionError(
                "You need at least one chapter included. Using all random? Enable 'RANDOM SAFETY : Chapter inclusion' option in your YAML."
            )


def validate_starting_chapter(world: "DeltaruneWorld"):
    if randomized_chapters(world) and world.options.starting_chapter.value != StartingChapter.option_random_chapter:
        if getattr(world.options, f"include_chapter_{world.options.starting_chapter.value}").value == False:
            raise OptionError(
                f"Your random starting chapter is set to {world.options.starting_chapter.value} but it isn't included."
            )


def validate_all_recruits(world: "DeltaruneWorld"):
    if all_recruits_route(world):
        if not include_recruits(world):
            world.options.recruits_sanity.value = 1
            logging.info(
                f"[DELTARUNE] Recruits Sanity was enabled for {world.player_name} as chosen route is All Recruits or Both."
            )
