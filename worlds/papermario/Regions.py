from collections.abc import Generator
from typing import Any, List, Dict

from BaseClasses import Region, MultiWorld
from rule_builder.rules import Rule

from .Entrance import PMEntrance
from .Locations import PMLocation, location_factory
from .options import SeedGoal

from .data.regions.boos_mansion import boos_mansion_regions
from .data.regions.bowsers_castle import bowsers_castle_regions
from .data.regions.crystal_palace import crystal_palace_regions
from .data.regions.dry_dry_desert import dry_dry_desert_regions
from .data.regions.dry_dry_outpost import dry_dry_outpost_regions
from .data.regions.dry_dry_ruins import dry_dry_ruins_regions
from .data.regions.flower_fields import flower_fields_regions
from .data.regions.forever_forest import forever_forest_regions
from .data.regions.goomba_village import goomba_village_regions
from .data.regions.gusty_gulch import gusty_gulch_regions
from .data.regions.inside_the_whale import inside_the_whale_regions
from .data.regions.jade_jungle import jade_jungle_regions
from .data.regions.koopa_bros_fortress import koopa_bros_fortress_regions
from .data.regions.koopa_region import koopa_region_regions
from .data.regions.minigames import minigames_regions
from .data.regions.mt_lavalava import mt_lavalava_regions
from .data.regions.mt_rugged import mt_rugged_regions
from .data.regions.peachs_castle import peachs_castle_regions
from .data.regions.shooting_star_summit import shooting_star_summit_regions
from .data.regions.shiver_region import shiver_region_regions
from .data.regions.shy_guys_toybox import shy_guys_toybox_regions
from .data.regions.star_haven import star_haven_regions
from .data.regions.toad_town_tunnels import toad_town_tunnels_regions
from .data.regions.toad_town import toad_town_regions
from .data.regions.tubbas_castle import tubbas_castle_regions

class PMRegion(Region):
    game: str = "Paper Mario"

    def __init__(self, name: str, player: int, multiworld: MultiWorld):
        super(PMRegion, self).__init__(name, player, multiworld)
        self.map_name = None
        self.map_id = None
        self.area_id = None


def get_regions(
    world_player: Any,
    multiworld: Any,
    excluded_areas: List[str],
    ch_excluded_location_names: List[str],
    seed_goal: SeedGoal
) -> Generator[PMRegion, None, None]:
    optionfiltered_regions: list[Dict[str, str | Dict[str, Rule | None]]] = []
    for region_data in [
        boos_mansion_regions,
        crystal_palace_regions,
        dry_dry_desert_regions,
        dry_dry_outpost_regions,
        dry_dry_ruins_regions,
        flower_fields_regions,
        forever_forest_regions,
        goomba_village_regions,
        gusty_gulch_regions,
        inside_the_whale_regions,
        jade_jungle_regions,
        koopa_bros_fortress_regions,
        koopa_region_regions,
        minigames_regions,
        mt_lavalava_regions,
        mt_rugged_regions,
        shooting_star_summit_regions,
        shiver_region_regions,
        shy_guys_toybox_regions,
        toad_town_tunnels_regions,
        toad_town_regions,
        tubbas_castle_regions,
    ]:
        optionfiltered_regions.extend(region_data)

    if seed_goal != SeedGoal.option_Open_Star_Way:
        # Open Star Way makes chapter 8 unreachable
        optionfiltered_regions.extend(star_haven_regions)
        optionfiltered_regions.extend(bowsers_castle_regions)
        optionfiltered_regions.extend(peachs_castle_regions)

    for region_entry in optionfiltered_regions:
        new_region = PMRegion(
            region_entry["region_name"],
            world_player,
            multiworld,
        )

        region_prefix: str = region_entry["region_name"][:3]

        for entry_key in region_entry.keys():
            if "area_id" == entry_key:
                new_region.font_color = region_entry["area_id"]
            elif "map_id" == entry_key:
                new_region.map_id = region_entry["map_id"]
            elif "map_name" == entry_key:
                new_region.scene = region_entry["map_name"]

            elif "locations" == entry_key and region_prefix not in excluded_areas:
                for (location_name, rule) in [
                    (x, y)
                    for (x, y) in region_entry["locations"].items()
                    if x not in ch_excluded_location_names
                ]:
                    new_location = location_factory(location_name, world_player)
                    new_location.parent_region = new_region
                    if rule is not None:
                        new_location.access_rule = rule
                    #set_rule
                    #if new_location.never:
                    #    # We still need to fill the location even if ALR is off.
                    #    logger.debug('Unreachable location: %s', new_location.name)
                    new_location.player = world_player
                    new_region.locations.append(new_location)

            elif "events" == entry_key and region_prefix not in excluded_areas:
                for (event_name, rule) in region_entry["events"].items():
                    # Allow duplicate placement of events
                    lname = '%s from %s' % (event_name, new_region.name)
                    new_location = PMLocation(
                        world_player,
                        lname,
                        event = True,
                        event_name = event_name,
                        parent = new_region,
                    )
                    if rule is not None:
                        new_location.access_rule = rule
                    #if new_location.never:
                    #    logger.debug('Dropping unreachable event: %s', new_location.name)
                    #else:
                    #    new_location.player = self.player
                    #    new_region.locations.append(new_location)
                    #    self.make_event_item(event, new_location)
                    #    new_location.show_in_spoiler = False
                    new_location.player = world_player
                    new_location.show_in_spoiler = False
                    new_region.locations.append(new_location)
            elif "exits" == entry_key:
                for exit_name, rule in region_entry["exits"].items():
                    if (    seed_goal == SeedGoal.option_Open_Star_Way
                        and exit_name == "SSS Star Way"
                    ):
                        # Don't create Star Way connection if Star Way doesn't
                        # even exist in this seed
                        continue

                    new_exit = PMEntrance(
                        world_player,
                        multiworld,
                        f"{new_region.name} -> {exit_name}",
                        new_region,
                    )
                    new_exit.vanilla_connected_region = exit_name
                    if rule is not None:
                        new_exit.access_rule = rule
                    #self.parser.parse_spot_rule(new_exit)
                    #if new_exit.never:
                    #    logger.debug('Dropping unreachable exit: %s', new_exit.name)
                    #else:
                    #    new_region.exits.append(new_exit)
                    new_region.exits.append(new_exit)

        yield new_region
