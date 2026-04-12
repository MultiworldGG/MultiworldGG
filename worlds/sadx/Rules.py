import math
from dataclasses import dataclass

from BaseClasses import Region
from Utils import visualize_regions
from worlds.generic.Rules import add_rule
from . import level_areas
from .CharacterUtils import get_playable_characters, is_level_playable, is_character_playable
from .Enums import LevelMission, Character, AreaConnection, Area, non_existent_areas, bosses_areas, \
    non_existent_connections
from .Locations import get_location_by_name, level_location_table, upgrade_location_table, sub_level_location_table, \
    LocationInfo, capsule_location_table, boss_location_table, mission_location_table, field_emblem_location_table
from .Logic import LevelLocation, UpgradeLocation, SubLevelLocation, EmblemLocation, CharacterUpgrade, \
    CapsuleLocation, BossFightLocation, MissionLocation, chao_egg_location_table, ChaoEggLocation, \
    chao_race_location_table, enemy_location_table, EnemyLocation, fish_location_table, FishLocation, area_connections
from .Names import ItemName
from .Regions import get_region_name, get_entrance_name


class LocationDistribution:
    def __init__(self, levels_for_perfect_chaos=0, missions_for_perfect_chaos=0, bosses_for_perfect_chaos=0,
                 entrance_emblem_value_map=None):
        self.levels_for_perfect_chaos = levels_for_perfect_chaos
        self.missions_for_perfect_chaos = missions_for_perfect_chaos
        self.bosses_for_perfect_chaos = bosses_for_perfect_chaos
        self.entrance_emblem_value_map = entrance_emblem_value_map


def add_level_rules(self, location_name: str, level: LevelLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in level.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))
    if self.options.lazy_fishing.value == 3 and level.character == Character.Big and (
            level.levelMission == LevelMission.B or level.levelMission == LevelMission.A or level.levelMission == LevelMission.S):
        add_rule(location, lambda state: state.has(ItemName.Big.PowerRod, self.player))


def add_upgrade_rules(self, location_name: str, upgrade: UpgradeLocation):
    location = self.multiworld.get_location(location_name, self.player)
    logic_items = upgrade.get_logic_items(self.options)
    if all(isinstance(item, str) for item in logic_items):
        for need in logic_items:
            add_rule(location, lambda state, item=need: state.has(item, self.player))
    else:
        add_rule(location, lambda state, egg_requirements=logic_items: any(
            all(state.has(item, self.player) for item in requirement_group) for requirement_group in egg_requirements))


def add_sub_level_rules(self, location_name: str, sub_level: SubLevelLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location, lambda state: any(
        state.can_reach_region(
            get_region_name(character, sub_level.area, self.options.egg_carrier_starts_transformed, self.options),
            self.player) for character in
        sub_level.get_logic_characters(self.options) if character in get_playable_characters(self.options)))


def add_field_emblem_rules(self, location_name: str, field_emblem: EmblemLocation):
    location = self.multiworld.get_location(location_name, self.player)
    # We check if the player has any of the character / character+upgraded needed
    add_rule(location, lambda state: any(
        (state.can_reach_region(
            get_region_name(character.character if isinstance(character, CharacterUpgrade) else character,
                            field_emblem.area, self.options.egg_carrier_starts_transformed, self.options),
            self.player) and
         (state.has(character.upgrade, self.player) if isinstance(character, CharacterUpgrade) else True))
        for character in field_emblem.get_logic_characters_upgrades(self.options) if
        character in get_playable_characters(self.options) or
        (isinstance(character, CharacterUpgrade) and character.character in get_playable_characters(self.options))))


def add_capsule_rules(self, location_name: str, life_capsule: CapsuleLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in life_capsule.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_boss_fight_rules(self, location_name: str, boss_fight: BossFightLocation):
    location = self.multiworld.get_location(location_name, self.player)
    if not boss_fight.unified:
        return
    add_rule(location, lambda state: any(
        state.can_reach_region(
            get_region_name(character, boss_fight.area, self.options.egg_carrier_starts_transformed, self.options),
            self.player) for character in
        boss_fight.characters if character in get_playable_characters(self.options)))


def add_mission_rules(self, location_name: str, mission: MissionLocation):
    location = self.multiworld.get_location(location_name, self.player)
    if mission.cardArea == Area.ECOutside:
        card_area_name = get_region_name(mission.character, mission.cardArea, False, self.options)
    else:
        card_area_name = get_region_name(mission.character, mission.cardArea,
                                         self.options.egg_carrier_starts_transformed, self.options)
    if not self.options.auto_start_missions:
        add_rule(location, lambda state, card_area=card_area_name: state.can_reach_region(card_area, self.player))

    logic_items = mission.get_logic_items(self.options)
    if all(isinstance(item, str) for item in logic_items):
        for need in logic_items:
            add_rule(location, lambda state, item=need: state.has(item, self.player))
    else:
        add_rule(location, lambda state, requirements=logic_items: any(
            all(state.has(item, self.player) for item in requirement_group) for requirement_group in requirements))
    # If lazy fishing is enabled, we need the Big Power Rod for certain missions
    if self.options.lazy_fishing.value == 3 and mission.missionNumber in [14, 29, 35, 44]:
        add_rule(location, lambda state: state.has(ItemName.Big.PowerRod, self.player))


def add_egg_rules(self, location_name: str, egg: ChaoEggLocation):
    location = self.multiworld.get_location(location_name, self.player)
    add_rule(location, lambda state: any(
        state.can_reach_region(
            get_region_name(character, egg.area, self.options.egg_carrier_starts_transformed, self.options),
            self.player) for character in
        egg.characters if character in get_playable_characters(self.options)))
    if egg.requirements:
        add_rule(location, lambda state, egg_requirements=egg.requirements: any(
            all(state.has(item, self.player) for item in requirement_group) for requirement_group in egg_requirements))


def add_race_rules(self, location_name: str):
    location = self.multiworld.get_location(location_name, self.player)

    level_location_list = []
    for level in level_location_table:
        if is_level_playable(level, self.options) and level.levelMission == LevelMission.C:
            level_location_list.append(self.multiworld.get_location(level.get_level_name(), self.player))

    self.random.shuffle(level_location_list)
    num_locations = max(1, math.ceil(
        len(level_location_list) * self.options.chao_races_levels_to_access_percentage.value / 100))
    for level_location in level_location_list[:num_locations]:
        add_rule(location, lambda state, loc=level_location: loc.can_reach(state))


def add_enemy_rules(self, location_name: str, enemy: EnemyLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in enemy.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))


def add_fish_rules(self, location_name: str, fish: FishLocation):
    location = self.multiworld.get_location(location_name, self.player)
    for need in fish.get_logic_items(self.options):
        add_rule(location, lambda state, item=need: state.has(item, self.player))
    if self.options.lazy_fishing.value >= 2:
        add_rule(location, lambda state: state.has(ItemName.Big.PowerRod, self.player))


def calculate_rules(self, location: LocationInfo):
    if location is None:
        return
    for level in level_location_table:
        if location["id"] == level.locationId:
            add_level_rules(self, location["name"], level)
    for upgrade in upgrade_location_table:
        if location["id"] == upgrade.locationId:
            add_upgrade_rules(self, location["name"], upgrade)
    for sub_level in sub_level_location_table:
        if location["id"] == sub_level.locationId:
            add_sub_level_rules(self, location["name"], sub_level)
    for life_capsule in capsule_location_table:
        if location["id"] == life_capsule.locationId:
            add_capsule_rules(self, location["name"], life_capsule)
    for field_emblem in field_emblem_location_table:
        if location["id"] == field_emblem.locationId:
            add_field_emblem_rules(self, location["name"], field_emblem)
    for boss_fight in boss_location_table:
        if location["id"] == boss_fight.locationId:
            add_boss_fight_rules(self, location["name"], boss_fight)
    for mission in mission_location_table:
        if location["id"] == mission.locationId:
            add_mission_rules(self, location["name"], mission)
    for egg in chao_egg_location_table:
        if location["id"] == egg.locationId:
            add_egg_rules(self, location["name"], egg)
    for race in chao_race_location_table:
        if location["id"] == race.locationId:
            add_race_rules(self, location["name"])
    for enemy in enemy_location_table:
        if location["id"] == enemy.locationId:
            add_enemy_rules(self, location["name"], enemy)
    for fish in fish_location_table:
        if location["id"] == fish.locationId:
            add_fish_rules(self, location["name"], fish)


def create_sadx_rules(self, needed_emblems: int, area_map) -> LocationDistribution:
    area_map = connect_regions(self, needed_emblems, area_map)

    levels_for_perfect_chaos = 0
    missions_for_perfect_chaos = 0
    bosses_for_perfect_chaos = 0
    for ap_location in self.multiworld.get_locations(self.player):
        calculate_rules(self, get_location_by_name(ap_location.name))

    perfect_chaos_fight = self.multiworld.get_location("Perfect Chaos Fight", self.player)
    perfect_chaos_fight.place_locked_item(self.create_item(ItemName.Progression.ChaosPeace))

    if self.options.goal_requires_emblems.value:
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.Emblem, self.player, needed_emblems))

    if self.options.goal_requires_levels.value:
        level_location_list = []
        for level in level_location_table:
            if is_level_playable(level, self.options) and level.levelMission == LevelMission.C:
                level_location_list.append(self.multiworld.get_location(level.get_level_name(), self.player))

        self.random.shuffle(level_location_list)
        num_locations = max(1, math.ceil(len(level_location_list) * self.options.levels_percentage.value / 100))
        for location in level_location_list[:num_locations]:
            add_rule(perfect_chaos_fight, lambda state, loc=location: loc.can_reach(state))
            levels_for_perfect_chaos += 1

    if self.options.goal_requires_missions.value:
        mission_location_list = []
        for mission in mission_location_table:
            if str(mission.missionNumber) in self.options.mission_blacklist.value:
                continue
            if str(mission.character.name) in self.options.mission_blacklist.value:
                continue
            if is_character_playable(mission.character, self.options) and self.options.mission_mode_checks:
                mission_location_list.append(self.multiworld.get_location(mission.get_mission_name(), self.player))

        self.random.shuffle(mission_location_list)
        num_locations = max(1, math.ceil(len(mission_location_list) * self.options.mission_percentage.value / 100))
        for location in mission_location_list[:num_locations]:
            add_rule(perfect_chaos_fight, lambda state, loc=location: loc.can_reach(state))
            missions_for_perfect_chaos += 1

    if self.options.goal_requires_bosses.value:
        bosses_location_list = []
        for ap_location in self.multiworld.get_locations(self.player):
            location = get_location_by_name(ap_location.name)
            for boss_fight in boss_location_table:
                if location["id"] == boss_fight.locationId:
                    bosses_location_list.append(self.multiworld.get_location(boss_fight.get_boss_name(), self.player))

        self.random.shuffle(bosses_location_list)
        num_locations = max(1, math.ceil(len(bosses_location_list) * self.options.boss_percentage.value / 100))
        for location in bosses_location_list[:num_locations]:
            add_rule(perfect_chaos_fight, lambda state, loc=location: loc.can_reach(state))
            bosses_for_perfect_chaos += 1

    if self.options.goal_requires_chao_races.value:
        for chao_race in chao_race_location_table:
            chao_race_location = self.multiworld.get_location(chao_race.name, self.player)
            add_rule(perfect_chaos_fight, lambda state, loc=chao_race_location: loc.can_reach(state))

    if self.options.goal_requires_chaos_emeralds.value:
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.WhiteEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.RedEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.CyanEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.PurpleEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.GreenEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.YellowEmerald, self.player))
        add_rule(perfect_chaos_fight, lambda state: state.has(ItemName.Progression.BlueEmerald, self.player))

    self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Progression.ChaosPeace,
                                                                                self.player)
    indexed_area_map = {
        key.get_index(): value
        for key, value in area_map.items()
    }
    return LocationDistribution(
        levels_for_perfect_chaos=levels_for_perfect_chaos,
        missions_for_perfect_chaos=missions_for_perfect_chaos,
        bosses_for_perfect_chaos=bosses_for_perfect_chaos,
        entrance_emblem_value_map=indexed_area_map
    )


def assign_area_weights(self, starter_setup) -> dict[Area, float]:
    starter_area = starter_setup.area
    if starter_area == Area.ECOutside:
        starter_area = Area.ECDeck

    area_tiers = [[starter_area], [], [], [], [], []]

    remaining_areas = set([area for area in Area]) - {starter_area}

    # Process connections iteratively
    for i in range(5):
        for area in area_tiers[i]:
            connected_areas = {
                area_to for (character, area_from, area_to, is_alternative), _
                in area_connections.items() if area_from == area and area_to in remaining_areas
            }
            for area_to in connected_areas:
                # High chance to move areas to the next tier if the tier has too many areas
                if len(area_tiers[i + 1]) > 4 and self.random.random() < 0.75:
                    area_tiers[min(i + 2, 5)].append(area_to)
                elif len(area_tiers[i + 1]) > 6 and self.random.random() < 0.75:
                    area_tiers[min(i + 3, 5)].append(area_to)
                # Chance to move some areas to later tiers
                elif i > 3 and self.random.random() < 0.25:
                    area_tiers[min(i + 2, 5)].append(area_to)
                else:
                    area_tiers[i + 1].append(area_to)
            remaining_areas -= connected_areas

    # Add remaining areas to list_5
    area_tiers[5].extend(remaining_areas)

    # Assign weights based on list index
    area_weights: dict[Area, float] = {}
    for weight, area_list in enumerate(area_tiers):
        for area in area_list:
            area_weights[area] = max(0, weight - 1) / 5  # Normalize weight to be between 0 and 1

    return area_weights


def get_connection_requirement(connection_key, area_map, is_alternative):
    # Check direct and reverse connection values
    value = area_map.get(connection_key, -1)
    if value != -1:
        return value
    value = area_map.get(AreaConnection.from_areas(connection_key.area2, connection_key.area1, is_alternative), -1)
    if value != -1:
        return value

    return -1


@dataclass
class FullConnectionData:
    t_area_from: Area
    t_area_to: Area
    t_actual_area_to: Area
    t_region_from: Region
    t_region_to: Region
    t_entrance_name: str
    nt_area_from: Area
    nt_area_to: Area
    nt_actual_area_to: Area
    nt_region_from: Region
    nt_region_to: Region
    nt_entrance_name: str


def connect_pair(full_connection: FullConnectionData, rule=None):
    if rule:
        full_connection.t_region_from.connect(full_connection.t_region_to, full_connection.t_entrance_name, rule)
        if (full_connection.nt_area_from, full_connection.nt_area_to) not in non_existent_connections:
            full_connection.nt_region_from.connect(full_connection.nt_region_to, full_connection.nt_entrance_name, rule)
    else:
        full_connection.t_region_from.connect(full_connection.t_region_to, name=full_connection.t_entrance_name)
        if (full_connection.nt_area_from, full_connection.nt_area_to) not in non_existent_connections:
            full_connection.nt_region_from.connect(full_connection.nt_region_to, name=full_connection.nt_entrance_name)


def connect_regions(self, needed_emblems: int, area_map=None):
    # Initialize the key-value map
    area_map = calculate_connection_requirements(area_map, needed_emblems, self)

    for (character, area_from, area_to, is_alternative), (normal_logic_items, hard_logic_items, expert_dc_logic_items,
                                                          expert_dx_logic_items,
                                                          expert_plus_dx_logic_items) in area_connections.items():
        if self.options.entrance_randomizer.value > 0:
            connection = AreaConnection.from_areas(area_from, area_to, is_alternative)
            actual_connection = self.starter_setup.level_mapping.get(connection, connection)
            actual_area_to = actual_connection.area2
        else:
            actual_area_to = area_to

        if not is_character_playable(character, self.options):
            continue
        if (character, area_from) in non_existent_areas:
            continue
        if (character, actual_area_to) in non_existent_areas:
            continue

        t_region_from = self.created_regions.get((character, area_from, True))
        t_region_to = self.created_regions.get((character, actual_area_to, True))

        nt_area_from = area_from
        if area_from == Area.ECBridge or area_from == Area.ECDeck:
            nt_area_from = Area.ECOutside
        nt_area_to = area_to
        nt_actual_area_to = actual_area_to
        if nt_area_to == Area.ECBridge or nt_area_to == Area.ECDeck:
            nt_area_to = Area.ECOutside
        if nt_actual_area_to == Area.ECBridge or nt_actual_area_to == Area.ECDeck:
            nt_actual_area_to = Area.ECOutside

        nt_region_from = self.created_regions.get((character, nt_area_from, False))
        if nt_actual_area_to in level_areas or nt_actual_area_to in bosses_areas:
            nt_region_to = self.created_regions.get((character, nt_actual_area_to, True))
        else:
            nt_region_to = self.created_regions.get((character, nt_actual_area_to, False))

        if self.options.logic_level.value == 4:
            key_items = expert_plus_dx_logic_items.copy()
        elif self.options.logic_level.value == 3:
            key_items = expert_dx_logic_items.copy()
        elif self.options.logic_level.value == 2:
            key_items = expert_dc_logic_items.copy()
        elif self.options.logic_level.value == 1:
            key_items = hard_logic_items.copy()
        else:
            key_items = normal_logic_items.copy()

        t_entrance_name = get_entrance_name(character, t_region_from, t_region_to,
                                            is_alternative)
        nt_entrance_name = get_entrance_name(character, nt_region_from,
                                             nt_region_to, is_alternative)
        if actual_area_to != area_to:
            t_entrance_name += " [Original (Transformed): " + area_to.name + "]"
            nt_entrance_name += " [Original (Not Transformed): " + area_to.name + "]"

        full_connection_data = FullConnectionData(area_from, area_to, actual_area_to,
                                                  t_region_from, t_region_to, t_entrance_name,
                                                  nt_area_from, nt_area_to, nt_actual_area_to,
                                                  nt_region_from, nt_region_to, nt_entrance_name)

        self.multiworld.explicit_indirect_conditions = False
        if t_region_from and t_region_to:
            # Key item gating
            if self.options.gating_mode.value == 1:
                if "EMBLEM_BLOCKED" in key_items:
                    key_items.remove("EMBLEM_BLOCKED")
                    if not key_items:
                        connect_pair(full_connection_data)
                        continue
                if "ONLY_RANDO" in key_items:
                    if self.options.entrance_randomizer.value == 0:
                        continue
                    else:
                        key_items.remove("ONLY_RANDO")

                if all(isinstance(item, str) for item in key_items):
                    connect_pair(full_connection_data, lambda state, items=key_items: all(
                        state.has(item, self.player) for item in items))
                else:
                    connect_pair(full_connection_data, lambda state, items=key_items:
                    any(all(state.has(item, self.player) for item in requirement_group)
                        for requirement_group in items))
            # Emblem gating
            elif self.options.gating_mode.value == 0:
                if "ONLY_RANDO" in key_items:
                    if self.options.entrance_randomizer.value == 0:
                        continue
                    else:
                        key_items.remove("ONLY_RANDO")

                if not key_items:
                    connect_pair(full_connection_data)
                    continue

                # Replace any key items with EMBLEM_BLOCKED
                if any(item in vars(ItemName.KeyItem).values() for item in key_items):
                    key_items = ["EMBLEM_BLOCKED" if item in vars(ItemName.KeyItem).values() else item for item in
                                 key_items]

                if "EMBLEM_BLOCKED" in key_items:
                    key_items.remove("EMBLEM_BLOCKED")
                    emblem_requirement = area_map.get(
                        AreaConnection.from_areas(area_from, actual_area_to, is_alternative), 0)
                    if not key_items:
                        connect_pair(full_connection_data,
                                     lambda state, emblems=emblem_requirement:
                                     state.has("Emblem", self.player, emblems))
                    else:
                        connect_pair(full_connection_data,
                                     lambda state, items=key_items, emblems=emblem_requirement:
                                     all(state.has(item, self.player) for item in items) and
                                     state.has("Emblem", self.player, emblems))
                else:
                    connect_pair(full_connection_data,
                                 lambda state, items=key_items: all(
                                     state.has(sub_item, self.player) for item in items for sub_item
                                     in
                                     (item if isinstance(item, list) else [item])))

    for character in get_playable_characters(self.options):
        captain_region_transformed = self.created_regions.get((character, Area.CaptainRoom, True))
        captain_region_not_transformed = self.created_regions.get((character, Area.CaptainRoom, False))
        entrance_name_1 = get_entrance_name(character, captain_region_transformed, captain_region_not_transformed,
                                            False)
        entrance_name_2 = get_entrance_name(character, captain_region_not_transformed, captain_region_transformed,
                                            False)
        captain_region_transformed.connect(captain_region_not_transformed, name=entrance_name_1)
        captain_region_not_transformed.connect(captain_region_transformed, name=entrance_name_2)

    visualize_regions(self.get_region("Menu"), "sadx.puml")
    return area_map


def calculate_connection_requirements(area_map, needed_emblems, self):
    if area_map is None:
        area_map = {}
    max_required_emblems = needed_emblems * 0.8
    if self.options.gating_mode == 0:

        if area_map == {}:
            area_weights = assign_area_weights(self, self.starter_setup)
            for (character, area_from, area_to, is_alternative), _ in area_connections.items():
                connection_key = AreaConnection.from_areas(area_from, area_to, is_alternative)
                connection_requirement = get_connection_requirement(connection_key, area_map, is_alternative)
                if connection_requirement != -1:
                    area_map[connection_key] = connection_requirement
                else:
                    if self.starter_setup.area == area_to or self.starter_setup.area == area_from:
                        area_map[connection_key] = 0
                    elif area_to in level_areas or area_from in level_areas:
                        area_map[connection_key] = 0
                    elif area_to in bosses_areas or area_from in bosses_areas:
                        area_map[connection_key] = 0

                    else:
                        # We assign a random factor based on area weights
                        factor = self.random.uniform(max(0.0, area_weights.get(area_from, 0)),
                                                     min(1.0, area_weights.get(area_to, 0)))
                        # For lower to lower connections, make it slightly lower
                        if area_weights.get(area_from, 0) <= 0.6 and area_weights.get(area_to, 0) <= 0.6:
                            factor = self.random.uniform(max(0.0, area_weights.get(area_from, 0) - 0.2),
                                                         min(1.0, area_weights.get(area_to, 0)))
                        # For higher to higher connections, make it slightly higher
                        if area_weights.get(area_from, 0) >= 0.6 and area_weights.get(area_to, 0) >= 0.6:
                            factor = self.random.uniform(max(0.0, area_weights.get(area_from, 0)),
                                                         min(1.0, area_weights.get(area_to, 0) + 0.2))
                        factor = factor ** 2
                        area_map[connection_key] = int(max_required_emblems * factor)
    return area_map
