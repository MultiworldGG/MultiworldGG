import itertools
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import cast

from BaseClasses import EntranceType, Item, ItemClassification, Location, Region

from ..core.rule_builder.rule_import import Rule
from ..core.rule_builder.rules import Has, True_
from ..data.constants import OracleOfSeasonsConnectionType
from ..data.items import ItemName
from ..data.locations import LOCATIONS_DATA
from ..data.logic import LogicLine
from ..data.logic.dungeons_logic import (
    make_d0_logic,
    make_d1_logic,
    make_d2_logic,
    make_d3_logic,
    make_d4_logic,
    make_d5_logic,
    make_d6_logic,
    make_d7_logic,
    make_d8_logic,
    make_d11_logic,
)
from ..data.logic.overworld_logic import make_gasha_logic, make_holodrum_logic
from ..data.logic.subrosia_logic import make_subrosia_logic
from ..data.regions import GASHA_SPOT_REGIONS, RegionName
from ..options import (
    OracleOfSeasonsGoal,
    OracleOfSeasonsLogicDifficulty,
    OracleOfSeasonsOldMenShuffle,
    OracleOfSeasonsStartingPosition,
)
from ..world import OracleOfSeasonsWorld
from .locations import location_is_active


@dataclass
class LocationData:
    location_name: str
    item_name: str | None

    def __lt__(self, other: "LocationData"):
        return self.location_name < other.location_name

    def __gt__(self, other: "LocationData"):
        return self.location_name > other.location_name


class ConnectionCreator:
    def __init__(self, world: OracleOfSeasonsWorld):
        self.world = world
        self.randomized_entrances: list[tuple[RegionName, str, int]] = []
        self.region_replacement: dict[RegionName, RegionName] = world.region_replacement
        self.reverse_replacement: dict[RegionName, set[RegionName]] = defaultdict(set)
        self.connection_data: dict[tuple[RegionName, RegionName], Rule.Resolved] = {}
        self.known_connections: dict[RegionName, set[tuple[RegionName, RegionName]]] = defaultdict(set)
        self.regions: set[RegionName] = set()
        self.important_regions: set[RegionName] = set()
        self.locations_data: dict[RegionName, list[LocationData]] = defaultdict(lambda: [])

    def prepare_event(self, region: RegionName, item_name: str):
        self.locations_data[region].append(LocationData(f"{region}.{item_name}", item_name))
        self.important_regions.add(region)

    def prepare_events(self) -> None:
        # Events for "wild" seeds that can be found inside respawnable bushes in dungeons
        self.prepare_event("d2 wild bombs", "_wild_bombs")
        self.prepare_event("d4 miniboss room wild embers", "_wild_ember_seeds")
        self.prepare_event("d5 armos chest", "_wild_ember_seeds")
        self.prepare_event("d5 armos chest", "_wild_bombs")
        self.prepare_event("d7 entrance wild embers", "_wild_ember_seeds")
        self.prepare_event("frypolar room wild mystery", "_wild_mystery_seeds")
        # Various events to help with logic
        self.prepare_event("bomb temple remains", "_triggered_volcano")
        if self.world.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_medium:
            self.prepare_event("d2 rupee room", "_reached_d2_rupee_room")
            self.prepare_event("d6 rupee room", "_reached_d6_rupee_room")
        self.prepare_event("maku seed", "Maku Seed")

        if self.world.options.goal == OracleOfSeasonsGoal.option_beat_onox:
            self.prepare_event("onox beaten", "_beaten_game")
        elif self.world.options.goal == OracleOfSeasonsGoal.option_beat_ganon:
            self.prepare_event("ganon beaten", "_beaten_game")

        # Create events for reaching Gasha spots, used when Gasha-sanity is on
        if self.world.options.deterministic_gasha_locations > 0:
            for region_name in GASHA_SPOT_REGIONS:
                self.prepare_event(region_name, f"_reached_{region_name}")

        # Create event items to represent rupees obtained from Old Men, unless they are turned into locations
        if self.world.options.shuffle_old_men != OracleOfSeasonsOldMenShuffle.option_turn_into_locations:
            for region_name in self.world.old_man_rupee_values:
                self.prepare_event(region_name, "rupees from " + region_name)

        # Events for the trade sequence, only in casual and shuffled code
        if not self.world.options.trade_sequence and (
            self.world.options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_casual
            or self.world.options.randomize_lost_woods_item_sequence
        ):
            self.prepare_event(RegionName.dr_left_reward, ItemName.cuccodex)
            self.prepare_event(RegionName.malon_trade, ItemName.lon_lon_egg)
            self.prepare_event(RegionName.maple_trade, ItemName.ghastly_doll)
            self.prepare_event(RegionName.mrs_ruul_trade, ItemName.iron_pot)
            self.prepare_event(RegionName.subrosian_chef_trade, ItemName.lava_soup)
            self.prepare_event(RegionName.biggoron_trade, ItemName.goron_vase)
            self.prepare_event(RegionName.ingo_trade, ItemName.fish)
            self.prepare_event(RegionName.old_man_trade, ItemName.megaphone)
            self.prepare_event(RegionName.talon_trade, ItemName.mushroom)
            self.prepare_event(RegionName.syrup_trade, ItemName.wooden_bird)
            self.prepare_event(RegionName.tick_tock_trade, ItemName.engine_grease)
            self.prepare_event(RegionName.guru_guru_trade, ItemName.phonograph)

    def prepare_locations(self) -> None:
        # Prepare locations
        for location_name, location_data in LOCATIONS_DATA.items():
            if not location_is_active(self.world, location_name, location_data):
                continue

            # is_local = "local" in location_data and location_data["local"] is True
            # Local is no longer implemented
            is_owl = "owl_id" in location_data

            region_name = location_data["region_id"]
            self.locations_data[region_name].append(LocationData(location_name, "Hint" if is_owl else None))
            self.important_regions.add(region_name)

        self.prepare_events()

        start_position = self.world.options.start_position
        if start_position == OracleOfSeasonsStartingPosition.option_horon_village:
            self.world.origin_region_name = RegionName.impas_house
            inventory_locations = False
        elif start_position == OracleOfSeasonsStartingPosition.option_sunken_city:
            self.world.origin_region_name = RegionName.sunken_city
            inventory_locations = True
        elif start_position == OracleOfSeasonsStartingPosition.option_samasa_desert:
            self.world.origin_region_name = RegionName.samasa_desert
            inventory_locations = True
        elif start_position == OracleOfSeasonsStartingPosition.option_temple_of_seasons:
            self.world.origin_region_name = RegionName.subrosia_temple_sector
            inventory_locations = False
        elif start_position == OracleOfSeasonsStartingPosition.option_tarm_entrance:
            self.world.origin_region_name = RegionName.spool_swamp_north
            inventory_locations = True
        else:
            raise NotImplementedError

        self.important_regions.add(self.world.origin_region_name)
        if inventory_locations:
            self.world.inventory_locations = []
            self.locations_data[self.world.origin_region_name].append(LocationData("Server", None))
            self.locations_data[self.world.origin_region_name].append(LocationData("Cheat Console", None))

    def try_prune_node(self, region_name: RegionName) -> None:
        connections = self.known_connections.get(region_name, None)
        if connections is None:
            return
        connections = sorted(connections)

        # Leaf handling
        if len(connections) <= 2:
            if len(connections) == 1:
                connection = connections[0]
                if connection[1] != region_name:
                    return
                connection_rule = self.connection_data[connection]
            elif connections[0][0] != connections[1][1] or connections[0][1] != connections[1][0]:
                # Not a two-way leaf
                connection = None
            elif connections[0][1] == region_name:
                connection = connections[0]
                connection_rule = self.connection_data[connection]
            else:
                connection = connections[1]
                connection_rule = self.connection_data[connection]
            if connection is not None and (connection_rule.always_true or region_name not in self.important_regions):
                origin = connection[0]
                self.prune_region(region_name, origin, "leaf dead end")
                self.try_prune_node(origin)
                return
        else:
            if region_name not in self.important_regions:
                for connection in connections:
                    if connection[0] == region_name:
                        break
                else:
                    self.prune_region(region_name, None, "mutli-leaf deadend")
                    return

        # Corridor handling
        if region_name not in self.important_regions and 2 <= len(connections) <= 4:
            origin_region: RegionName | None = None
            target_region: RegionName | None = None
            two_way_progress = 0
            forward_rule = True_()
            backward_rule = True_()
            for connection in connections:
                if connection[0] == region_name:
                    other_region = connection[1]
                    if target_region is None or target_region == other_region:
                        target_region = other_region
                        forward_rule &= self.connection_data[connection]
                    elif origin_region is None or origin_region == other_region:
                        origin_region = other_region
                        backward_rule &= self.connection_data[connection]
                        two_way_progress += 1
                    else:
                        return
                else:
                    other_region = connection[0]
                    if origin_region is None or origin_region == other_region:
                        origin_region = other_region
                        forward_rule &= self.connection_data[connection]
                    elif target_region is None or target_region == other_region:
                        target_region = other_region
                        backward_rule &= self.connection_data[connection]
                        two_way_progress += 1
                    else:
                        return
            if origin_region is None or target_region is None:
                return
            self.prune_region(region_name, None, "empty corridor")
            self.register_connection((origin_region, target_region), forward_rule.resolve(self.world))
            if two_way_progress == 2:
                self.register_connection((target_region, origin_region), backward_rule.resolve(self.world))
            self.try_prune_node(origin_region)
            self.try_prune_node(target_region)

    def try_prune_nodes(self) -> None:
        for region_name in sorted(self.known_connections.keys()):
            self.try_prune_node(region_name)

    def create_connections(self) -> None:
        self.prepare_locations()

        self.parse_logic_lines()
        self.try_prune_nodes()

        # Move locations
        for original_region, new_region in self.region_replacement.items():
            if original_region in self.locations_data:
                self.locations_data[new_region].extend(self.locations_data.pop(original_region))

        for region_name in sorted(self.regions):
            region = Region(region_name, self.world.player, self.world.multiworld)
            self.world.multiworld.regions.append(region)
            for region_name in itertools.chain((region_name,), sorted(self.reverse_replacement[region_name])):
                if region_name in self.locations_data:
                    for location_data in sorted(self.locations_data[region_name]):
                        location_name = location_data.location_name
                        location_id = OracleOfSeasonsWorld.location_name_to_id.get(location_name, None)
                        if location_id:
                            inventory_location = False
                        else:
                            if location_name == "Server":
                                location_id = -2
                                inventory_location = True
                            elif location_name == "Cheat Console":
                                location_id = -1
                                inventory_location = True
                            else:
                                inventory_location = False
                        location = Location(self.world.player, location_name, location_id, region)
                        region.locations.append(location)
                        if inventory_location:
                            cast(list[Location], self.world.inventory_locations).append(location)
                        item_name = location_data.item_name
                        if item_name:
                            if item_name == "Hint":
                                classification = ItemClassification.filler
                            else:
                                classification = ItemClassification.progression
                            item = Item(item_name, classification, None, self.world.player)
                            location.place_locked_item(item)

        for regions, rule in self.connection_data.items():
            region_1, region_2 = regions
            if region_1 == region_2:
                continue
            region_1 = self.world.get_region(region_1)
            region_2 = self.world.get_region(region_2)
            self.world.create_entrance(region_1, region_2, rule=rule)

        for region_name, entrance_name, randomization_group in self.randomized_entrances:
            region_name = self.world.get_region(region_name)

            entrance = region_name.create_exit(entrance_name)
            entrance.randomization_group = randomization_group
            entrance.randomization_type = EntranceType.TWO_WAY
            self.world.set_rule(entrance, True_())

            entrance = region_name.create_er_target(entrance_name)
            entrance.randomization_group = randomization_group
            entrance.randomization_type = EntranceType.TWO_WAY
            self.world.set_rule(entrance, True_())

        if self.world.origin_region_name in self.world.region_replacement:
            self.world.origin_region_name = self.world.region_replacement[self.world.origin_region_name]

    def parse_logic_lines(self) -> None:
        options = self.world.options
        all_logic: list[list[LogicLine]] = [
            make_holodrum_logic(self.world, options),
            make_subrosia_logic(),
            make_d0_logic(),
            make_d1_logic(),
            make_d2_logic(self.world, options),
            make_d3_logic(),
            make_d4_logic(options),
            make_d5_logic(),
            make_d6_logic(),
            make_d7_logic(),
            make_d8_logic(),
            make_d11_logic(options),
            make_gasha_logic(self.world),
        ]

        for logic_array in all_logic:
            for entrance_desc in logic_array:
                region_1 = entrance_desc[0]
                region_2 = entrance_desc[1]
                transition_type = entrance_desc[2]
                rule = entrance_desc[3]

                resolved_rule: Rule.Resolved = rule.resolve(self.world)
                if resolved_rule.always_false:
                    continue
                self.important_regions.update(resolved_rule.region_dependencies().keys())
                if transition_type.is_dungeon_entrance():
                    if options.shuffle_dungeons:
                        self.important_regions.add(region_1)
                        self.important_regions.add(region_2)
                        self.randomized_entrances.append(
                            (region_1, region_1.value, OracleOfSeasonsConnectionType.CONNECT_DUNGEON_OVERWORLD)
                        )
                        self.randomized_entrances.append(
                            (region_2, region_2.value, OracleOfSeasonsConnectionType.CONNECT_DUNGEON_INSIDE)
                        )
                        continue

                elif transition_type.is_portal_entrance():
                    if options.shuffle_portals:
                        self.important_regions.add(region_1)
                        self.important_regions.add(region_2)
                        self.randomized_entrances.append(
                            (region_1, f"enter {region_1}", OracleOfSeasonsConnectionType.CONNECT_PORTAL_OVERWORLD)
                        )
                        self.randomized_entrances.append(
                            (region_2, f"enter {region_2}", OracleOfSeasonsConnectionType.CONNECT_PORTAL_SUBROSIA)
                        )
                        continue

                if region_1 in self.region_replacement:
                    region_1 = self.region_replacement[region_1]
                if region_2 in self.region_replacement:
                    region_2 = self.region_replacement[region_2]

                if region_1 == region_2:
                    continue

                is_two_way = transition_type.is_two_way()

                if is_two_way and resolved_rule.always_true:
                    # This connection is superfluous
                    self.regions.add(region_1)
                    self.prune_region(region_2, region_1, "always true connection")
                else:
                    self.regions.add(region_1)
                    self.regions.add(region_2)
                    self.register_connection((region_1, region_2), resolved_rule)
                    if is_two_way:
                        self.register_connection((region_2, region_1), resolved_rule)

    def prune_region(self, removed_region: RegionName, replacement_region: RegionName | None, reason: str):
        logging.debug(f"tloz_oos: Pruned {removed_region} ({reason})")
        self.regions.discard(removed_region)
        if replacement_region is not None:
            self.region_replacement[removed_region] = replacement_region
            self.reverse_replacement[replacement_region].add(removed_region)
        if removed_region in self.reverse_replacement:
            to_link_back = self.reverse_replacement.pop(removed_region)
            if replacement_region is not None:
                for region in sorted(to_link_back):
                    self.region_replacement[region] = replacement_region
                self.reverse_replacement[replacement_region].update(to_link_back)

        if removed_region in self.known_connections:
            for connection_pair in sorted(self.known_connections.pop(removed_region)):
                if connection_pair in self.connection_data:
                    # That connection may have been severed already
                    rule = self.connection_data.pop(connection_pair)
                    (region_a, region_b) = connection_pair
                    if region_a == removed_region:
                        new_pair = (replacement_region, region_b)
                        other_region = region_b
                    else:
                        new_pair = (region_a, replacement_region)
                        other_region = region_a

                    self.known_connections[other_region].remove(connection_pair)
                    if other_region != replacement_region and replacement_region is not None:
                        self.register_connection(cast(tuple[RegionName, RegionName], new_pair), rule)

        if removed_region in self.important_regions:
            if replacement_region is None:
                raise Exception
            self.important_regions.remove(removed_region)
            self.important_regions.add(replacement_region)

    def register_connection(
        self,
        connection_pair: tuple[RegionName, RegionName],
        rule: Rule.Resolved,
    ):
        if connection_pair in self.connection_data:
            self.connection_data[connection_pair] = (self.connection_data[connection_pair] | rule).resolve(self.world)
        else:
            self.connection_data[connection_pair] = rule
            self.known_connections[connection_pair[0]].add(connection_pair)
            self.known_connections[connection_pair[1]].add(connection_pair)


def create_connections(world: OracleOfSeasonsWorld):
    world.set_completion_rule(Has("_beaten_game"))
    ConnectionCreator(world).create_connections()
