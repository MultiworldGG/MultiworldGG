import logging

from typing import Any, ClassVar, Dict, List, Optional, Set, TextIO, Tuple, Union

from BaseClasses import Entrance, EntranceType, Item, ItemClassification, Location, Region, Tutorial
from Options import OptionError

from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances
from rule_builder.rules import Rule, And, Has

from worlds.AutoWorld import WebWorld, World

from .data.entrance_data import Entrance, EntranceRuleData, entrance_rule_data

from .data.entrance_randomizer_data import (
    entrances_to_game_location_teleports,
    entrances_to_game_locations,
    randomizable_entrances,
    randomizable_entrances_subway,
)

from .data.item_data import ZorkGrandInquisitorItemData, item_data
from .data.location_data import ZorkGrandInquisitorLocationData

from .data.mapping_data import (
    early_items_for_starting_location,
    endgame_connecting_regions_for_goal,
    entrance_names,
    entrance_names_reverse,
    starter_kit_for_entrance_randomizer,
    starter_kits_for_starting_location,
    starting_location_to_region,
)

from .data_funcs import (
    item_names_to_id,
    item_names_to_item,
    location_names_to_id,
    id_to_craftable_spell_behaviors,
    id_to_deathsanity,
    id_to_entrance_randomizer,
    id_to_goals,
    id_to_hotspots,
    id_to_landmarksanity,
    id_to_starting_locations,
    item_groups,
    items_with_tag,
    location_groups,
    locations_by_region_for_world,
    locations_with_tag,
    prepare_item_data,
    prepare_location_data,
    entrances_by_region_for_world,
)

from .enums import (
    ZorkGrandInquisitorCraftableSpellBehaviors,
    ZorkGrandInquisitorDeathsanity,
    ZorkGrandInquisitorEntranceRandomizer,
    ZorkGrandInquisitorEvents,
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorHotspots,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLandmarksanity,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorRegions,
    ZorkGrandInquisitorStartingLocations,
    ZorkGrandInquisitorTags,
)

from .options import ZorkGrandInquisitorOptions, option_groups


class ZorkGrandInquisitorItem(Item):
    game = "Zork Grand Inquisitor"


class ZorkGrandInquisitorLocation(Location):
    game = "Zork Grand Inquisitor"


class ZorkGrandInquisitorWebWorld(WebWorld):
    theme: str = "stone"

    tutorials: List[Tutorial] = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Zork Grand Inquisitor randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["Serpent.AI"],
        )
    ]

    option_groups = option_groups


class ZorkGrandInquisitorWorld(World):
    """
    Zork: Grand Inquisitor is a 1997 point-and-click adventure game for PC.
    Magic has been banned from the great Underground Empire of Zork. By edict of the Grand Inquisitor Mir Yannick, the
    Empire has been sealed off and the practice of mystic arts declared punishable by "Totemization" (a very bad thing).
    The only way to restore magic to the kingdom is to find three hidden artifacts: The Coconut of Quendor, The Cube of
    Foundation, and The Skull of Yoruk.
    """

    options_dataclass = ZorkGrandInquisitorOptions
    options: ZorkGrandInquisitorOptions

    game = "Zork Grand Inquisitor"

    item_name_to_id = item_names_to_id()
    location_name_to_id = location_names_to_id()

    item_name_groups = item_groups()
    location_name_groups = location_groups()

    required_client_version: Tuple[int, int, int] = (0, 6, 7)

    web = ZorkGrandInquisitorWebWorld()

    artifacts_of_magic_required: int
    artifacts_of_magic_total: int
    craftable_spells: ZorkGrandInquisitorCraftableSpellBehaviors
    deaths_required: int
    deathsanity: ZorkGrandInquisitorDeathsanity
    early_items: Tuple[ZorkGrandInquisitorItems, ...]
    entrance_randomizer: ZorkGrandInquisitorEntranceRandomizer
    entrance_randomizer_include_subway_destinations: bool

    entrance_randomizer_pairings: Dict[
        Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions],
        Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions],
    ]

    entrance_randomizer_pairings_by_name: Dict[str, str]
    entrance_rule_data: EntranceRuleData
    filler_item_names: List[str] = item_groups()["Filler"]
    goal: ZorkGrandInquisitorGoals
    grant_missable_location_checks: bool
    hotspots: ZorkGrandInquisitorHotspots
    initial_totemizer_destination: ZorkGrandInquisitorItems
    item_data: Dict[ZorkGrandInquisitorItems, ZorkGrandInquisitorItemData]
    item_name_to_item: Dict[str, ZorkGrandInquisitorItems] = item_names_to_item()
    landmarks_required: int
    landmarksanity: ZorkGrandInquisitorLandmarksanity
    location_data: Dict[Union[ZorkGrandInquisitorLocations, ZorkGrandInquisitorEvents], ZorkGrandInquisitorLocationData]
    locked_items: Dict[ZorkGrandInquisitorLocations, ZorkGrandInquisitorItems]
    starter_kit: Tuple[ZorkGrandInquisitorItems, ...]
    starting_location: ZorkGrandInquisitorStartingLocations
    trap_percentage: int
    trap_weights: Tuple[int, ...]

    ut_can_gen_without_yaml: bool = True

    tracker_world: ClassVar = {
        "map_page_folder": "ut",
        "map_page_maps": "maps/maps.json",
        "map_page_locations": "locations/locations.json",
    }

    # Needed for item link
    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

        self.item_data = dict()

    @property
    def is_universal_tracker(self) -> bool:
        return hasattr(self.multiworld, "re_gen_passthrough")

    def generate_early(self) -> None:
        self.goal = id_to_goals()[self.options.goal.value]

        self.artifacts_of_magic_required = self.options.artifacts_of_magic_required.value
        self.artifacts_of_magic_total = self.options.artifacts_of_magic_total.value

        if self.artifacts_of_magic_required > self.artifacts_of_magic_total:
            self.artifacts_of_magic_total = self.artifacts_of_magic_required

            if self.goal == ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT:
                logging.warning(
                    f"Zork Grand Inquisitor: {self.player_name} has more required artifacts than " 
                    "total artifacts. Using required artifacts as total artifacts..."
                )

        self.landmarks_required = self.options.landmarks_required.value
        self.deaths_required = self.options.deaths_required.value

        self.starting_location = id_to_starting_locations()[self.options.starting_location.value]

        self.entrance_randomizer = id_to_entrance_randomizer()[self.options.entrance_randomizer.value]

        if self.entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
            self.topology_present = True

        self.entrance_randomizer_include_subway_destinations = bool(
            self.options.entrance_randomizer_include_subway_destinations
        )

        self.starter_kit = tuple()

        if starter_kits_for_starting_location[self.starting_location] is not None:
            self.starter_kit = self.random.choice(
                starter_kits_for_starting_location[self.starting_location]
            )

            if self.entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
                starter_kit_extended: List[ZorkGrandInquisitorItems] = list(self.starter_kit)

                item: ZorkGrandInquisitorItems
                for item in starter_kit_for_entrance_randomizer:
                    if item not in starter_kit_extended:
                        starter_kit_extended.append(item)

                self.starter_kit = tuple(starter_kit_extended)

        self.early_items = tuple()

        if early_items_for_starting_location[self.starting_location] is not None:
            self.early_items = self.random.choice(
                early_items_for_starting_location[self.starting_location]
            )

        self.craftable_spells = id_to_craftable_spell_behaviors()[self.options.craftable_spells.value]
        self.hotspots = id_to_hotspots()[self.options.hotspots]

        self.deathsanity = id_to_deathsanity()[self.options.deathsanity]

        if self.goal == ZorkGrandInquisitorGoals.GRIM_JOURNEY and (
            self.deathsanity == ZorkGrandInquisitorDeathsanity.OFF
        ):
            self.deathsanity = ZorkGrandInquisitorDeathsanity.ON

        self.landmarksanity = id_to_landmarksanity()[self.options.landmarksanity]

        if self.goal == ZorkGrandInquisitorGoals.ZORK_TOUR and (
            self.landmarksanity == ZorkGrandInquisitorLandmarksanity.OFF
        ):
            self.landmarksanity = ZorkGrandInquisitorLandmarksanity.ON

        self.grant_missable_location_checks = bool(self.options.grant_missable_location_checks)

        if self.grant_missable_location_checks:
            if self.entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
                self.grant_missable_location_checks = False

                logging.warning(
                    f"Zork Grand Inquisitor: {self.player_name} wants to grant missable location checks but "
                    "has the entrance randomizer enabled. Disabling the granting of missable location checks..."
                )

        self.entrance_randomizer_pairings = dict()
        self.entrance_randomizer_pairings_by_name = dict()

        self.entrance_rule_data = entrance_rule_data

        self.item_data = prepare_item_data(
            self.starting_location,
            self.goal,
            self.deathsanity,
            self.landmarksanity,
            self.entrance_randomizer,
        )

        self.location_data = prepare_location_data(
            self.starting_location,
            self.goal,
            self.deathsanity,
            self.landmarksanity,
        )

        self.locked_items = self._prepare_locked_items()

        self.initial_totemizer_destination = self._select_initial_totemizer_destination()

        self.trap_percentage = self.options.trap_percentage.value / 100

        self.trap_weights = (
            self.options.infinite_corridor_trap_weight.value,
            self.options.reverse_controls_trap_weight.value,
            self.options.teleport_trap_weight.value,
            self.options.zvision_trap_weight.value,
        )

        if self.trap_percentage and not any(self.trap_weights):
            raise OptionError(
                f"Zork Grand Inquisitor: {self.player_name} has traps enabled but all traps are weighted at 0."
            )

        # Universal Tracker Support
        if self.is_universal_tracker:
            self._apply_universal_tracker_passthrough()

    def create_regions(self) -> None:
        entrances_by_region: Dict[ZorkGrandInquisitorRegions, List[Entrance]] = entrances_by_region_for_world(
            self.entrance_rule_data
        )

        region_mapping: Dict[ZorkGrandInquisitorRegions, Region] = dict()

        region_enum_item: ZorkGrandInquisitorRegions
        for region_enum_item in entrances_by_region.keys():
            region_mapping[region_enum_item] = Region(region_enum_item.value, self.player, self.multiworld)

        region_locations_mapping: Dict[ZorkGrandInquisitorRegions, List[ZorkGrandInquisitorLocations]]
        region_locations_mapping = locations_by_region_for_world(self.location_data)

        region_connecting_endgame: ZorkGrandInquisitorRegions = endgame_connecting_regions_for_goal[self.goal]

        region_enum_item: ZorkGrandInquisitorRegions
        region: Region
        for region_enum_item, region in region_mapping.items():
            regions_locations: List[ZorkGrandInquisitorLocations] = region_locations_mapping[region_enum_item]

            # Locations
            location_enum_item: ZorkGrandInquisitorLocations
            for location_enum_item in regions_locations:
                data: ZorkGrandInquisitorLocationData = self.location_data[location_enum_item]

                location: ZorkGrandInquisitorLocation = ZorkGrandInquisitorLocation(
                    self.player,
                    location_enum_item.value,
                    data.archipelago_id,
                    region_mapping[data.region],
                )

                # Locked Items
                if location_enum_item in self.locked_items:
                    location.place_locked_item(self.create_item(self.locked_items[location_enum_item].value))
                elif isinstance(location_enum_item, ZorkGrandInquisitorEvents):
                    location.place_locked_item(
                        ZorkGrandInquisitorItem(
                            data.event_item_name,
                            ItemClassification.progression,
                            None,
                            self.player,
                        )
                    )

                # Access Rules
                location_rule: Optional[Rule] = self.location_data[location_enum_item].requirements

                if location_rule is not None:
                    self.set_rule(location, location_rule)

                region.locations.append(location)

            # Connections
            region_exit: ZorkGrandInquisitorRegions
            for _, region_exit in entrances_by_region[region_enum_item]:
                connection_tuple: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions] = (
                    region_enum_item,
                    region_exit,
                )

                entrance: Entrance
                entrance_rule: Optional[Rule] = self.entrance_rule_data.get(connection_tuple, None)

                if entrance_rule is None:
                    entrance = region.connect(region_mapping[region_exit])
                else:
                    entrance = region.connect(region_mapping[region_exit], rule=entrance_rule)

                entrance.name = entrance_names.get(connection_tuple, entrance.name)

            if region_enum_item == region_connecting_endgame:
                goal_access_rule: Optional[Rule] = None

                if self.goal == ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT:
                    goal_access_rule = (
                        Has(ZorkGrandInquisitorItems.ARTIFACT_OF_MAGIC.value, self.artifacts_of_magic_required)
                    )
                elif self.goal == ZorkGrandInquisitorGoals.SPELL_HEIST:
                    goal_access_rule = (
                        And(
                            Has(ZorkGrandInquisitorItems.SPELL_BEBURTT.value),
                            Has(ZorkGrandInquisitorItems.SPELL_GLORF.value),
                            Has(ZorkGrandInquisitorItems.SPELL_GOLGATEM.value),
                            Has(ZorkGrandInquisitorItems.SPELL_IGRAM.value),
                            Has(ZorkGrandInquisitorItems.SPELL_KENDALL.value),
                            Has(ZorkGrandInquisitorItems.SPELL_OBIDIL.value),
                            Has(ZorkGrandInquisitorItems.SPELL_NARWILE.value),
                            Has(ZorkGrandInquisitorItems.SPELL_REZROV.value),
                            Has(ZorkGrandInquisitorItems.SPELL_SNAVIG.value),
                            Has(ZorkGrandInquisitorItems.SPELL_THROCK.value),
                            Has(ZorkGrandInquisitorItems.SPELL_YASTARD.value),
                        )
                    )
                elif self.goal == ZorkGrandInquisitorGoals.ZORK_TOUR:
                    goal_access_rule = (
                        Has(ZorkGrandInquisitorItems.LANDMARK.value, self.landmarks_required)
                    )
                elif self.goal == ZorkGrandInquisitorGoals.GRIM_JOURNEY:
                    goal_access_rule = (
                        Has(ZorkGrandInquisitorItems.DEATH.value, self.deaths_required)
                    )

                region.connect(region_mapping[ZorkGrandInquisitorRegions.ENDGAME], rule=goal_access_rule)

            self.multiworld.regions.append(region)

        # Connect "Menu" region to starting location and to endgame when applicable
        region_menu: Region = Region("Menu", self.player, self.multiworld)
        region_starting_location: ZorkGrandInquisitorRegions = starting_location_to_region[self.starting_location]

        region_menu.connect(region_mapping[ZorkGrandInquisitorRegions.ANYWHERE])
        region_menu.connect(region_mapping[region_starting_location])

        if region_connecting_endgame == ZorkGrandInquisitorRegions.MENU:
            if self.goal == ZorkGrandInquisitorGoals.THREE_ARTIFACTS:
                goal_access_rule = (
                    And(
                        Has(ZorkGrandInquisitorItems.COCONUT_OF_QUENDOR.value),
                        Has(ZorkGrandInquisitorItems.CUBE_OF_FOUNDATION.value),
                        Has(ZorkGrandInquisitorItems.SKULL_OF_YORUK.value),
                    )
                )

                region_menu.connect(region_mapping[ZorkGrandInquisitorRegions.ENDGAME], rule=goal_access_rule)

        self.multiworld.regions.append(region_menu)

    def create_items(self) -> None:
        # Populate Items to Ignore and Precollect
        items_to_ignore: Set[ZorkGrandInquisitorItems] = (
            items_with_tag(ZorkGrandInquisitorTags.FILLER)
            | items_with_tag(ZorkGrandInquisitorTags.TRAP)
            | items_with_tag(ZorkGrandInquisitorTags.GOAL_THREE_ARTIFACTS)
            | items_with_tag(ZorkGrandInquisitorTags.GOAL_ZORK_TOUR)
            | items_with_tag(ZorkGrandInquisitorTags.GOAL_GRIM_JOURNEY)
            | set(self.locked_items.values())
        )

        if self.goal != ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT:
            items_to_ignore |= items_with_tag(ZorkGrandInquisitorTags.GOAL_ARTIFACT_OF_MAGIC_HUNT)

        items_to_precollect: Set[ZorkGrandInquisitorItems] = (
            set(self.starter_kit)
            | {self.initial_totemizer_destination}
        )

        hotspot_items: Set[ZorkGrandInquisitorItems] = items_with_tag(ZorkGrandInquisitorTags.HOTSPOT)

        hotspot_regional_items: Set[ZorkGrandInquisitorItems] = items_with_tag(
            ZorkGrandInquisitorTags.HOTSPOT_REGIONAL
        )

        if self.hotspots == ZorkGrandInquisitorHotspots.ENABLED:
            items_to_ignore |= hotspot_items
            items_to_precollect |= hotspot_regional_items
        elif self.hotspots == ZorkGrandInquisitorHotspots.REQUIRE_ITEM_PER_REGION:
            items_to_ignore |= hotspot_items
        elif self.hotspots == ZorkGrandInquisitorHotspots.REQUIRE_ITEM_PER_HOTSPOT:
            items_to_ignore |= hotspot_regional_items

        if self.starting_location != ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR:
            items_to_precollect.add(ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_HOUSE_EXIT)

        if self.starting_location != ZorkGrandInquisitorStartingLocations.SPELL_LAB:
            items_to_precollect.add(ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_BRIDGE_EXIT)

        items_to_ignore |= items_to_precollect

        # Create Item Pool
        item_pool: List[ZorkGrandInquisitorItem] = list()

        data: ZorkGrandInquisitorItemData
        for item, data in self.item_data.items():
            if item in items_to_ignore:
                continue

            if item == ZorkGrandInquisitorItems.ARTIFACT_OF_MAGIC:
                for _ in range(self.artifacts_of_magic_total):
                    item_pool.append(self.create_item(item.value))
            else:
                item_pool.append(self.create_item(item.value))

        total_location_count: int = len(self.multiworld.get_unfilled_locations(self.player))
        to_fill_location_count: int = total_location_count - len(item_pool)

        trap_count: int = int(round(to_fill_location_count * self.trap_percentage))

        if trap_count:
            item_pool += [
                self.create_item(trap.value) for trap in self._sample_trap_items(trap_count)
            ]

        item_pool += [
            self.create_filler() for _ in range(to_fill_location_count - trap_count)
        ]

        self.multiworld.itempool += item_pool

        # Precollect Items
        for item_name in sorted([i.value for i in items_to_precollect]):
            self.multiworld.push_precollected(self.create_item(item_name))

        # Define Early Items
        items_to_place_early: Set[ZorkGrandInquisitorItems] = (
            set(self.early_items) - items_to_ignore
        )

        if len(items_to_place_early):
            for item in items_to_place_early:
                self.multiworld.early_items[self.player][item.value] = 1

    def create_item(self, name: str) -> ZorkGrandInquisitorItem:
        data: ZorkGrandInquisitorItemData = (self.item_data or item_data)[self.item_name_to_item[name]]

        return ZorkGrandInquisitorItem(
            name,
            data.classification,
            data.archipelago_id,
            self.player,
        )

    def connect_entrances(self) -> None:
        if self.entrance_randomizer == ZorkGrandInquisitorEntranceRandomizer.DISABLED:
            return

        randomization_pool: List[Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]] = list(
            randomizable_entrances
        )

        if self.entrance_randomizer_include_subway_destinations:
            randomization_pool.extend(randomizable_entrances_subway)

        entrance: Entrance
        for entrance in self.get_entrances():
            entrance_region_tuple: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions] = (
                ZorkGrandInquisitorRegions(entrance.parent_region.name),
                ZorkGrandInquisitorRegions(entrance.connected_region.name),
            )

            if entrance_region_tuple in randomization_pool:
                entrance.randomization_type = EntranceType.TWO_WAY
                disconnect_entrance_for_randomization(entrance)

        if self.is_universal_tracker:
            self._reconnect_entrances_for_universal_tracker()
            return

        entrance_randomizer_pairings: List[Tuple[str, str]] = randomize_entrances(
            self,
            self.entrance_randomizer == ZorkGrandInquisitorEntranceRandomizer.COUPLED,
            {0: [0]},
        ).pairings

        self.entrance_randomizer_pairings = self._process_entrance_randomizer_pairings(entrance_randomizer_pairings)

    def generate_basic(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = self.options.as_dict(
            "goal",
            "artifacts_of_magic_required",
            "artifacts_of_magic_total",
            "landmarks_required",
            "deaths_required",
            "starting_location",
            "hotspots",
            "craftable_spells",
            "wild_voxam",
            "wild_voxam_chance",
            "deathsanity",
            "landmarksanity",
            "entrance_randomizer",
            "entrance_randomizer_include_subway_destinations",
            "trap_percentage",
            "grant_missable_location_checks",
            "client_seed_information",
            "death_link",
        )

        slot_data["starter_kit"] = sorted([item.value for item in self.starter_kit])
        slot_data["initial_totemizer_destination"] = self.initial_totemizer_destination.value

        slot_data["trap_weights"] = self.trap_weights

        slot_data["save_ids"] = (
            self.random.randint(1, 65365),
            self.random.randint(1, 65365),
            self.random.randint(1, 65365),
        )

        # Relay generate_early Overrides
        if slot_data["artifacts_of_magic_total"] != self.artifacts_of_magic_total:
            slot_data["artifacts_of_magic_total"] = self.artifacts_of_magic_total

        if slot_data["deathsanity"] != self.deathsanity.value:
            slot_data["deathsanity"] = self.deathsanity.value

        if slot_data["landmarksanity"] != self.landmarksanity.value:
            slot_data["landmarksanity"] = self.landmarksanity.value

        if slot_data["grant_missable_location_checks"] != self.grant_missable_location_checks:
            slot_data["grant_missable_location_checks"] = self.grant_missable_location_checks

        slot_data["entrance_randomizer_data"] = dict()
        slot_data["entrance_randomizer_data_by_name"] = dict()

        if self.entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
            slot_data["entrance_randomizer_data"] = self._prepare_entrance_randomizer_slot_data()
            slot_data["entrance_randomizer_data_by_name"] = self._prepare_entrance_randomizer_slot_data_by_name()

        return slot_data

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]) -> None:
        if self.entrance_randomizer == ZorkGrandInquisitorEntranceRandomizer.DISABLED:
            return

        entrance_name_cache: Dict[ZorkGrandInquisitorRegions, List[str]] = dict()

        entrance_from: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]
        entrance_to: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]
        for entrance_from, entrance_to in self.entrance_randomizer_pairings.items():
            if entrance_to[1] not in entrance_name_cache:
                entrance_name_cache[entrance_to[1]] = list()

            entrance_name_cache[entrance_to[1]].append(
                f"{entrance_from[0].value}: {entrance_names[entrance_from]}"
            )

        data: Dict[int, str] = dict()

        location_enum_item: Union[ZorkGrandInquisitorLocations, ZorkGrandInquisitorEvents]
        location_data: ZorkGrandInquisitorLocationData
        for location_enum_item, location_data in self.location_data.items():
            if isinstance(location_enum_item, ZorkGrandInquisitorEvents):
                continue
            elif location_data.region not in entrance_name_cache:
                continue

            data[location_data.archipelago_id] = "  OR  ".join(entrance_name_cache[location_data.region])

        hint_data[self.player] = data

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.entrance_randomizer == ZorkGrandInquisitorEntranceRandomizer.DISABLED:
            return

        spoiler_handle.write("\nRandomized Entrances:")

        spoiler_lines: List[str] = list()

        entrance_from: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]
        entrance_to: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]
        for entrance_from, entrance_to in self.entrance_randomizer_pairings.items():
            spoiler_lines.append(
                f"\n    {entrance_from[0].value}: {entrance_names[entrance_from]} -> "
                f"{entrance_to[1].value} (Emerging out of: {entrance_names[entrance_to]})"
            )

        spoiler_line: str
        for spoiler_line in sorted(spoiler_lines):
            spoiler_handle.write(spoiler_line)

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.filler_item_names)

    # Universal Tracker Support
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        slot_data["goal"] = id_to_goals()[slot_data["goal"]]
        slot_data["starting_location"] = id_to_starting_locations()[slot_data["starting_location"]]
        slot_data["hotspots"] = id_to_hotspots()[slot_data["hotspots"]]
        slot_data["craftable_spells"] = id_to_craftable_spell_behaviors()[slot_data["craftable_spells"]]
        slot_data["deathsanity"] = id_to_deathsanity()[slot_data["deathsanity"]]
        slot_data["landmarksanity"] = id_to_landmarksanity()[slot_data["landmarksanity"]]
        slot_data["entrance_randomizer"] = id_to_entrance_randomizer()[slot_data["entrance_randomizer"]]
        slot_data["entrance_randomizer_include_subway_destinations"] = bool(slot_data["entrance_randomizer_include_subway_destinations"])

        slot_data["starter_kit"] = tuple([ZorkGrandInquisitorItems(item) for item in slot_data["starter_kit"]])

        slot_data["initial_totemizer_destination"] = ZorkGrandInquisitorItems(
            slot_data["initial_totemizer_destination"]
        )

        return slot_data

    def _apply_universal_tracker_passthrough(self) -> None:
        if "Zork Grand Inquisitor" in self.multiworld.re_gen_passthrough:
            passthrough: Dict[str, Any] = self.multiworld.re_gen_passthrough["Zork Grand Inquisitor"]

            self.goal = passthrough["goal"]
            self.artifacts_of_magic_required = passthrough["artifacts_of_magic_required"]
            self.artifacts_of_magic_total = passthrough["artifacts_of_magic_total"]
            self.landmarks_required = passthrough["landmarks_required"]
            self.deaths_required = passthrough["deaths_required"]
            self.starting_location = passthrough["starting_location"]
            self.starter_kit = passthrough["starter_kit"]
            self.craftable_spells = passthrough["craftable_spells"]
            self.hotspots = passthrough["hotspots"]
            self.deathsanity = passthrough["deathsanity"]
            self.landmarksanity = passthrough["landmarksanity"]
            self.entrance_randomizer = passthrough["entrance_randomizer"]

            self.entrance_randomizer_include_subway_destinations = passthrough[
                "entrance_randomizer_include_subway_destinations"
            ]

            self.entrance_randomizer_pairings_by_name = passthrough["entrance_randomizer_data_by_name"]

            self.item_data = prepare_item_data(
                self.starting_location,
                self.goal,
                self.deathsanity,
                self.landmarksanity,
                self.entrance_randomizer,
            )

            self.location_data = prepare_location_data(
                self.starting_location,
                self.goal,
                self.deathsanity,
                self.landmarksanity,
            )

            self.locked_items = self._prepare_locked_items()
            self.initial_totemizer_destination = passthrough["initial_totemizer_destination"]
            self.trap_percentage = passthrough["trap_percentage"] / 100
            self.trap_weights = passthrough["trap_weights"]

    def _prepare_entrance_randomizer_slot_data(self) -> Dict[str, str]:
        entrance_randomizer_slot_data: Dict[str, str] = dict()

        entrance_from: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]
        entrance_to: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]
        for entrance_from, entrance_to in self.entrance_randomizer_pairings.items():
            game_locations_pair: Tuple[str, str]
            for game_locations_pair in entrances_to_game_locations[entrance_from]:
                entrance_randomizer_slot_data["-".join(game_locations_pair)] = (
                    " ".join(entrances_to_game_location_teleports[entrance_to])
                )

        return entrance_randomizer_slot_data

    def _prepare_entrance_randomizer_slot_data_by_name(self) -> Dict[str, str]:
        entrance_randomizer_slot_data_by_name: Dict[str, str] = dict()

        entrance_from: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]
        entrance_to: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]
        for entrance_from, entrance_to in self.entrance_randomizer_pairings.items():
            entrance_randomizer_slot_data_by_name[entrance_names[entrance_from]] = entrance_names[entrance_to]

        return entrance_randomizer_slot_data_by_name

    def _prepare_locked_items(
        self,
    ) -> Dict[ZorkGrandInquisitorLocations, ZorkGrandInquisitorItems]:
        locked_items: Dict[ZorkGrandInquisitorLocations, ZorkGrandInquisitorItems] = dict()

        # Goal Items
        if self.goal == ZorkGrandInquisitorGoals.THREE_ARTIFACTS:
            locked_items[
                ZorkGrandInquisitorLocations.COME_TO_PAPA_YOU_NUT
            ] = ZorkGrandInquisitorItems.COCONUT_OF_QUENDOR

            locked_items[
                ZorkGrandInquisitorLocations.GOOD_PUZZLE_SMART_BROG
            ] = ZorkGrandInquisitorItems.SKULL_OF_YORUK

            locked_items[
                ZorkGrandInquisitorLocations.YOU_LOSE_MUFFET_ANTE_UP
            ] = ZorkGrandInquisitorItems.CUBE_OF_FOUNDATION
        elif self.goal == ZorkGrandInquisitorGoals.ZORK_TOUR:
            landmarksanity_locations: Set[ZorkGrandInquisitorLocations] = locations_with_tag(
                ZorkGrandInquisitorTags.LANDMARKSANITY
            )

            location: ZorkGrandInquisitorLocations
            for location in landmarksanity_locations:
                locked_items[location] = ZorkGrandInquisitorItems.LANDMARK
        elif self.goal == ZorkGrandInquisitorGoals.GRIM_JOURNEY:
            deathsanity_locations: Set[ZorkGrandInquisitorLocations] = locations_with_tag(
                ZorkGrandInquisitorTags.DEATHSANITY
            )

            location: ZorkGrandInquisitorLocations
            for location in deathsanity_locations:
                locked_items[location] = ZorkGrandInquisitorItems.DEATH

        # Craftable Spells
        if self.craftable_spells == ZorkGrandInquisitorCraftableSpellBehaviors.VANILLA:
            if ZorkGrandInquisitorItems.SPELL_BEBURTT not in self.starter_kit:
                locked_items[
                    ZorkGrandInquisitorLocations.IMBUE_BEBURTT
                ] = ZorkGrandInquisitorItems.SPELL_BEBURTT

            if ZorkGrandInquisitorItems.SPELL_OBIDIL not in self.starter_kit:
                locked_items[
                    ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP
                ] = ZorkGrandInquisitorItems.SPELL_OBIDIL

            if ZorkGrandInquisitorItems.SPELL_SNAVIG not in self.starter_kit:
                locked_items[
                    ZorkGrandInquisitorLocations.SNAVIG_REPAIRED
                ] = ZorkGrandInquisitorItems.SPELL_SNAVIG

            if ZorkGrandInquisitorItems.SPELL_YASTARD not in self.starter_kit:
                locked_items[
                    ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU
                ] = ZorkGrandInquisitorItems.SPELL_YASTARD
        elif self.craftable_spells == ZorkGrandInquisitorCraftableSpellBehaviors.ANY_SPELL:
            allowable_spells: Set[ZorkGrandInquisitorItems] = {
                ZorkGrandInquisitorItems.SPELL_BEBURTT,
                ZorkGrandInquisitorItems.SPELL_GLORF,
                ZorkGrandInquisitorItems.SPELL_GOLGATEM,
                ZorkGrandInquisitorItems.SPELL_IGRAM,
                ZorkGrandInquisitorItems.SPELL_KENDALL,
                ZorkGrandInquisitorItems.SPELL_OBIDIL,
                ZorkGrandInquisitorItems.SPELL_NARWILE,
                ZorkGrandInquisitorItems.SPELL_REZROV,
                ZorkGrandInquisitorItems.SPELL_SNAVIG,
                ZorkGrandInquisitorItems.SPELL_THROCK,
                ZorkGrandInquisitorItems.SPELL_YASTARD,
            }

            allowable_spells -= set(self.starter_kit)

            allowable_spells_yastard: List[str] = sorted([item.value for item in allowable_spells])

            spell_yastard: ZorkGrandInquisitorItems = self.item_name_to_item[
                self.random.choice(allowable_spells_yastard)
            ]

            locked_items[ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU] = spell_yastard

            allowable_spells -= {spell_yastard}

            if self.starting_location != ZorkGrandInquisitorStartingLocations.SPELL_LAB:
                allowable_spells -= {
                    ZorkGrandInquisitorItems.SPELL_GOLGATEM,
                    ZorkGrandInquisitorItems.SPELL_REZROV,
                }

            allowable_spells_spell_lab: List[str] = sorted(
                [item.value for item in allowable_spells]
            )

            spells_to_lock: List[ZorkGrandInquisitorItems] = [
                self.item_name_to_item[item]
                for item in self.random.sample(allowable_spells_spell_lab, 3)
            ]

            locked_items[ZorkGrandInquisitorLocations.IMBUE_BEBURTT] = spells_to_lock[0]
            locked_items[ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP] = spells_to_lock[1]
            locked_items[ZorkGrandInquisitorLocations.SNAVIG_REPAIRED] = spells_to_lock[2]

        return locked_items

    @staticmethod
    def _process_entrance_randomizer_pairings(pairings: List[Tuple[str, str]]) -> Dict[
        Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions],
        Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions],
    ]:
        entrance_randomizer_pairings: Dict[
            Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions],
            Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions],
        ] = dict()

        entrance_from: str
        entrance_to: str
        for entrance_from, entrance_to in pairings:
            entrance_randomizer_pairings[entrance_names_reverse[entrance_from]] = tuple(
                reversed(entrance_names_reverse[entrance_to])
            )

        return entrance_randomizer_pairings

    def _reconnect_entrances_for_universal_tracker(self) -> None:
        entrance_from: Entrance
        for entrance_from in self.get_entrances():
            if entrance_from.name in self.entrance_randomizer_pairings_by_name:
                entrance_to_name: str = self.entrance_randomizer_pairings_by_name[entrance_from.name]

                entrance_to_region_pair: Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions] = (
                    entrance_names_reverse[entrance_to_name]
                )

                entrance_from.connect(self.get_region(entrance_to_region_pair[1].value))

            # We also need to reconnect vanilla subway entrances when ER is on, but destinations are not randomized
            if not self.entrance_randomizer_include_subway_destinations:
                if entrance_from.name.startswith("Subway Ride"):
                    region_to: ZorkGrandInquisitorRegions = entrance_names_reverse[entrance_from.name][1]
                    entrance_from.connect(self.get_region(region_to.value))

    def _select_initial_totemizer_destination(self) -> ZorkGrandInquisitorItems:
        return self.random.choice((
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_SURFACE_OF_MERZ,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_NEWARK_NEW_JERSEY,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_INFINITY,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL,
        ))

    def _sample_trap_items(self, count: int) -> List[ZorkGrandInquisitorItems]:
        return self.random.choices(
            (
                ZorkGrandInquisitorItems.TRAP_INFINITE_CORRIDOR,
                ZorkGrandInquisitorItems.TRAP_REVERSE_CONTROLS,
                ZorkGrandInquisitorItems.TRAP_TELEPORT,
                ZorkGrandInquisitorItems.TRAP_ZVISION,
            ),
            weights=self.trap_weights,
            k=count,
        )
