from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import Has

from worlds.deltarune.Locations import locations, LocationIDs
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.Rules import have_susie, have_kris_susie_or_ralsei, have_kris

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def set_rules(world: "DeltaruneWorld"):
    return
    # Region lockers

    # Macguffin


def handle_locked_items(world: "DeltaruneWorld"):
    if not world.is_secret_bosses_randomized():
        return

    # Hidden Items
    if not world.is_hidden_items_randomized():
        return
