from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances
from random import Random
from time import strftime
from typing import Dict, Any, Iterable, TextIO, List, Tuple, ClassVar
import logging
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, CollectionState, MultiWorld
from Fill import fill_restrictive
from Utils import visualize_regions
from worlds.AutoWorld import World, WebWorld
from . import Options
from .OptionGroups import lunacid_option_groups
from .Tracker import disconnect_entrances, reconnect_found_entrance
from .data.enemy_positions import (base_enemy_placement, EnemyPlacement, construct_flag_data_for_mod,
                                   construct_enemy_dictionary)
from .data.location_data import grass_location_names, breakable_location_names
from .strings.custom_features import all_classes, DefaultColors
from .strings.enemies import Enemy
from .strings.spells import Spell, MobSpell
from .strings.weapons import Weapon
from .data.item_data import (all_item_data_by_name, all_filler_items, starting_weapon, drop_starting_weapons,
                             shop_starting_weapons, LunacidItemData, all_basic_materials)
from .data.weapon_info import weapons_by_element
from .strings.items import Creation, Coins, UniqueItem, Progressives, Switch, Door, Trap, Alchemy
from .strings.options import Endings, Victory, Settings
from .strings.regions_entrances import LunacidRegion
from .strings.locations import (BaseLocation, ShopLocation, unique_drop_locations, other_drop_locations,
                                AlchemyLocation, all_drops, Quench, all_drops_by_enemy)
from .Items import (item_table, complete_items_by_name, create_items, determine_starting_weapon,
                    determine_weapon_elements, all_filler)
from .Options import LunacidOptions
from .Locations import create_locations, location_table
from .Regions import create_regions, randomized_entrance_names
from .Rules import LunacidRules
from worlds.generic.Rules import set_rule
from .data.plant_data import all_alchemy_plant_data
from . import Tracker

logger = logging.getLogger()


class LunacidItem(Item):
    game: str = "Lunacid"


#class LunacidSettings(Group):

    #class UTPoptrackerPath(FilePath):
    #    """Path to the user's Lunacid's Poptracker Pack."""
    #    description = "Lunacid's Poptracker Pack zip file"
    #    required = False

    #ut_poptracker_path: UTPoptrackerPath | str = UTPoptrackerPath()


class LunacidWeb(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Lunacid randomizer connected to a MultiworldGG Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Albrekka", "Tesseract (Advice/Direction)", "Scipio (UT Help)", "Miracee/Scipio (Tracker)"]
    )]


class LunacidWorld(World):
    """
    Lunacid is a first person dungeon crawler inspired by old FROMSOFT games like Shadow Tower and King’s Field.

    Long ago a great beast arose from the sea and covered the earth in a poison fog. Now those deemed undesirable
    are thrown into a great well, which has become a pit of chaos and disease. You awaken in a moonlit subterranean world,
    having been thrown into the Great Well for crimes unknown. The only way out is to go further down and confront the
    sleeping old one below. On the way there will be many creatures and secrets to discover.
    """

    game = "Lunacid"
    author: str = "Albrekka"
    topology_present = False
    item_name_to_id = {item.name: item.code for item in item_table}
    location_name_to_id = {location.name: location.location_id for location in location_table}

    item_name_groups = {
        "Vampiric Symbols": [Progressives.vampiric_symbol],
        "Switch Keys": Switch.switches,
        "Door Keys": Door.all_door_keys,
        "VHS Tapes": [UniqueItem.vhs_tape, UniqueItem.white_tape],
        "Talismans": [UniqueItem.earth_talisman, UniqueItem.water_talisman],
        "Traps": Trap.all_traps,
        "Materials": all_basic_materials,
        "Junk": all_filler_items
    }

    location_name_groups = {
        "Daedalus Spells": [BaseLocation.archives_daedalus_one, BaseLocation.archives_daedalus_two,
                            BaseLocation.archives_daedalus_third],
        "Tower of Abyss": BaseLocation.abyss_locations,
        "Coins": BaseLocation.coin_locations,
        "Shops": ShopLocation.shop_locations,
        "Grass": grass_location_names,
        "Breakables": breakable_location_names,
        "Unique Drops": unique_drop_locations,
        "Non-unique Drops": other_drop_locations,
        "Quench": Quench.all_quenches,
        "Alchemy": AlchemyLocation.all_alchemy_locations
    }

    required_client_version = (0, 6, 1)

    options_dataclass = LunacidOptions
    option_groups = lunacid_option_groups
    options: LunacidOptions
    rolled_month = int(strftime('%m'))
    starting_weapon: LunacidItem
    level = 0
    local_alchemy: List[Item] = []
    local_filler: List[Item] = []
    locations_for_filler: List[Location] = []
    #settings: ClassVar[LunacidSettings]
    weapon_elements: Dict[str, str] = {}
    world_entrances = dict[str, Entrance]
    randomized_entrances: Dict[str, str] = {}
    enemy_random_data: Dict[str, List[str]]
    enemy_regions: Dict[str, List[str]]
    custom_class_name: str
    custom_class_description: str
    custom_class_stats: Dict[str, int]
    web = LunacidWeb()
    logger = logging.getLogger()
    explicit_indirect_conditions = True
    glitches_item_name = "Glitched Item"

    passthrough: Dict[str, Any]
    using_ut: bool = False
    tracker_world: ClassVar = Tracker.TRACKER_WORLD
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml
    disconnected_entrances: dict[Entrance, Region]
    found_entrances_datastorage_key = "Slot:{player}:TraversedEntrances"

    def __init__(self, multiworld, player):
        super(LunacidWorld, self).__init__(multiworld, player)
        slot_data = getattr(multiworld, "re_gen_passthrough", {}).get("Lunacid")
        if slot_data:
            self.seed = slot_data.get("ut_seed")
            self.using_ut = True
        else:
            self.seed = self.random.getrandbits(64)
        self.random = Random(self.seed)
        self.custom_class_name = ""
        self.custom_class_description = ""
        self.custom_class_stats = {}

    def generate_early(self) -> None:
        Tracker.setup_options_from_slot_data(self)
        self.package_custom_class()
        self.level = self.determine_starting_level()
        self.enemy_random_data, enemy_regions = self.randomize_enemies()
        slot_data = getattr(self.multiworld, "re_gen_passthrough", {}).get("Lunacid")
        if slot_data:
            self.enemy_regions = slot_data.get("enemy_regions")
        else:
            self.enemy_regions = enemy_regions
        if self.options.challenges == self.options.challenges.option_exp:
            self.options.levelsanity.value = self.options.levelsanity.option_false

    def create_item(self, name: str, override_classification: ItemClassification = None) -> "LunacidItem":
        if name == self.glitches_item_name:
            return LunacidItem(name, ItemClassification.progression_skip_balancing, None, self.player)
        item_id: int = self.item_name_to_id[name]

        if override_classification is None:
            override_classification = complete_items_by_name[name].classification

        return LunacidItem(name, override_classification, item_id, player=self.player)

    def create_event(self, event: str):
        return Item(event, ItemClassification.progression_skip_balancing, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(all_filler_items)

    def set_rules(self):
        if self.options.challenges == self.options.challenges.option_logic:
            logger.info(f"WARNING: Player {self.player} has chosen NO LOGIC for Lunacid.  If not intended reroll and smack them.")
            return
        LunacidRules(self).set_lunacid_rules(self.weapon_elements, self.enemy_regions)

    def create_items(self):
        locations_count = len([location
                               for location in self.get_locations() if location.item is None]) - 1
        if self.options.etnas_pupil and self.options.dropsanity == self.options.dropsanity.option_randomized:
            locations_count -= 80
        if self.options.starting_area == self.options.starting_area.option_tomb:
            locations_count -= 1
        excluded_items = self.multiworld.precollected_items[self.player]
        slot_data = getattr(self.multiworld, "re_gen_passthrough", {}).get("Lunacid")
        if slot_data:
            ut_starting_weapon = slot_data["starting_weapon"]
        else:
            ut_starting_weapon = ""
        if not self.weapon_elements:
            self.weapon_elements = determine_weapon_elements(self.options, self.random)
        (potential_pool, self.local_filler, starting_weapon_choice) = create_items(self.create_item, locations_count, excluded_items,
                                                                                   self.weapon_elements, self.rolled_month, self.level, ut_starting_weapon, self.options,
                                                                                   self.random)
        self.starting_weapon = starting_weapon_choice
        if potential_pool.count(self.starting_weapon) > 1:
            potential_pool.remove(self.starting_weapon)

        # There's a weird edge case where very rarely there's one more item in the pool than there should be.
        all_items = potential_pool + self.local_filler + self.local_alchemy + [self.starting_weapon]
        if len(set(self.get_locations())) < len(all_items):
            random_filler = [item for item in potential_pool if item.classification == 0]
            potential_pool.remove(random_filler)

        self.multiworld.itempool += potential_pool

        starting_location = self.get_location(BaseLocation.wings_rest_crystal_shard)
        starting_location.place_locked_item(self.starting_weapon)
        if self.options.starting_area == self.options.starting_area.option_tomb:
            lamp = self.create_item(UniqueItem.oil_lantern, ItemClassification.progression | ItemClassification.useful)
            bony_friend = self.get_location(BaseLocation.wings_rest_clives_gift)
            bony_friend.place_locked_item(lamp)

        if self.options.etnas_pupil and self.options.dropsanity == self.options.dropsanity.option_randomized:
            alchemy_items = []
            for _ in range(5):  # make sure there's enough of them to go around
                for alchemy_item in Alchemy.necessary_alchemy_items:
                    alchemy_items.append(Item(alchemy_item, ItemClassification.progression | ItemClassification.useful,
                                              self.item_name_to_id[alchemy_item], self.player))
            self.local_alchemy = alchemy_items

        if self.multiworld.players == 1:
            self.multiworld.itempool += self.local_filler

    def create_regions(self):
        multiworld = self.multiworld
        player = self.player
        starting_area = self.options.starting_area.current_key

        def create_region(region_name: str, exits: Iterable[str]) -> Region:
            lunacid_region = Region(region_name, player, multiworld)
            lunacid_region.exits = [Entrance(player, exit_name, lunacid_region) for exit_name in exits]
            return lunacid_region

        world_regions, world_entrances = create_regions(starting_area, create_region, multiworld)
        self.world_entrances = world_entrances
        locations = create_locations(self.options, self.rolled_month, self.level)
        for location in locations:
            name = location.name
            location_id = location.location_id
            region: Region = world_regions[location.region]
            region.add_locations({name: location_id})

        self.multiworld.regions.extend(world_regions.values())

        if self.options.ending == self.options.ending.option_ending_b:
            ending_region = self.get_region(LunacidRegion.labyrinth_of_ash)
        elif self.options.ending != self.options.ending.option_any_ending:
            ending_region = self.get_region(LunacidRegion.grave_of_the_sleeper)
        else:
            ending_region = self.get_region(LunacidRegion.grave_of_the_sleeper)
        grotto_region = self.get_region(LunacidRegion.boiling_grotto)

        hicket = Location(player, "Free Sir Hicket", None, grotto_region)
        hicket.place_locked_item(self.create_event("Sir Hicket's Freedom from Armor"))
        if self.options.ending == self.options.ending.option_ending_cd:
            victory = Location(player, Endings.look_into_abyss, None, ending_region)
        elif self.options.ending == self.options.ending.option_ending_b:
            victory = Location(player, Endings.open_door, None, ending_region)
        elif (self.options.ending == self.options.ending.option_ending_a
              or self.options.ending == self.options.ending.option_ending_e):
            victory = Location(player, Endings.wake_dreamer, None, ending_region)
        else:
            victory = Location(player, "The Dreamer or the Door", None, ending_region)
        victory.place_locked_item(self.create_event(Victory.victory))
        ending_region.locations.append(victory)

        if self.options.ending == self.options.ending.option_ending_b:
            set_rule(victory, lambda state: LunacidRules(self).has_coins_for_door(self.options, state))
        elif self.options.ending == self.options.ending.option_ending_e:
            set_rule(victory, lambda state: LunacidRules(self).has_every_spell(state, self.options, self.starting_weapon.name)
                                            and state.has(UniqueItem.white_tape, self.player))
        elif self.options.ending == self.options.ending.option_any_ending:
            set_rule(victory, lambda state: state.can_reach_region(LunacidRegion.grave_of_the_sleeper, self.player)
                                            or (LunacidRules(self).has_coins_for_door(self.options, state)
                                                and state.can_reach_region(LunacidRegion.labyrinth_of_ash, self.player)))

        multiworld.completion_condition[self.player] = lambda state: state.has(Victory.victory, player)

    def connect_entrances(self) -> None:
        world_entrances = self.world_entrances
        entrances_randod = self.options.entrance_randomization
        if entrances_randod:
            randomized_entrances = [world_entrances[entrance] for entrance in world_entrances if world_entrances[entrance].name in randomized_entrance_names]
            for entrance in randomized_entrances:
                disconnect_entrance_for_randomization(entrance, None, entrance.connected_region.name)
            result = randomize_entrances(self, True, {0: [0]})
            self.randomized_entrances = dict(result.pairings)
            slot_data = getattr(self.multiworld, "re_gen_passthrough", {}).get("Lunacid")
            if slot_data:
                e_dict = {entrance.name: entrance for region in self.multiworld.get_regions(self.player) for entrance in region.entrances}
                entrances = slot_data["entrances"]
                for connection in slot_data["entrances"]:
                    assert connection in e_dict, f"entrance {connection} in slot data not in world"
                    assert entrances[connection] in e_dict, f"entrance {entrances[connection]} in slot data not in world"

                    e_dict[connection].connected_region = e_dict[entrances[connection]].parent_region
                self.randomized_entrances = slot_data["entrances"]
            if self.using_ut and self.multiworld.enforce_deferred_connections in ("on", "default"):
                disconnect_entrances(self)
        # self.visualize_regions()
        # hi = True

    def reconnect_found_entrances(self, found_key: str, data_storage_value: Any) -> None:
        if not data_storage_value:
            return
        reconnect_found_entrance(self, data_storage_value)

    def visualize_regions(self):
        multiworld = self.multiworld
        player = self.player
        visualize_regions(multiworld.get_region("Menu", player), f"{multiworld.get_out_file_name_base(player)}.puml", show_locations=False)

    def package_custom_class(self) -> None:
        def package_custom_class_stat(stat: str, minimum: int, maximum: int) -> None:
            stat_data = min(maximum, self.options.custom_class.get(stat, -1))
            if stat_data == -1:
                self.custom_class_stats[stat] = self.random.randrange(minimum, maximum)
            else:
                self.custom_class_stats[stat] = max(minimum, stat_data)

        name = self.options.custom_class.get("Name", "RANDOM")
        description = self.options.custom_class.get("Description", "RANDOM")
        if name == "RANDOM" and description == "RANDOM":
            chosen_class = self.random.choice(list(all_classes.keys()))
            self.custom_class_name = chosen_class
            self.custom_class_description = all_classes[chosen_class]
        elif name == "RANDOM":
            chosen_class = self.random.choice(list(all_classes.keys()))
            self.custom_class_name = chosen_class
            self.custom_class_description = description
        elif description == "RANDOM":
            chosen_class = self.random.choice(list(all_classes.keys()))
            self.custom_class_name = name
            self.custom_class_description = all_classes[chosen_class]
        else:
            self.custom_class_name = name
            self.custom_class_description = description
        package_custom_class_stat("Level", 1, 10)
        package_custom_class_stat("Strength", 1, 20)
        package_custom_class_stat("Speed", 1, 20)
        package_custom_class_stat("Intelligence", 1, 20)
        package_custom_class_stat("Defense", 1, 20)
        package_custom_class_stat("Dexterity", 1, 20)
        package_custom_class_stat("Resistance", 1, 20)
        package_custom_class_stat("Normal Res", 0, 20)
        package_custom_class_stat("Fire Res", 0, 300)
        package_custom_class_stat("Ice Res", 0, 300)
        package_custom_class_stat("Poison Res", 0, 300)
        package_custom_class_stat("Light Res", 0, 300)
        package_custom_class_stat("Dark Res", 0, 300)

    def determine_starting_level(self) -> int:
        options = self.options
        if not options.levelsanity:
            return -1
        if options.starting_class == 0:
            return 5
        elif options.starting_class == 1:
            return 10
        elif options.starting_class == 2:
            return 7
        elif options.starting_class == 3:
            return 9
        elif options.starting_class == 4:
            return 8
        elif options.starting_class == 5:
            return 6
        elif options.starting_class == 6:
            return 8
        elif options.starting_class == 7:
            return 9
        elif options.starting_class == 8:
            return 1
        elif options.starting_class == 9:
            return self.custom_class_stats["Level"]
        return -1

    @staticmethod
    def total_points_given_starting_level(starting_level: int):
        if starting_level <= 5:
            return 310 - 6 * starting_level
        elif starting_level <= 50:
            return 300 - 4 * starting_level
        else:
            return 200 - 2 * starting_level

    def randomize_enemies(self) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        chosen_enemies = []
        enemy_counts = {enemy: 0 for enemy in Enemy.randomizable_enemies}
        randomized_enemy_placement = []
        enemy_to_enemy_placement = {}
        if self.options.enemy_randomization:
            for enemy_data in base_enemy_placement:
                picked_enemy = self.random.choice(Enemy.randomizable_enemies)
                new_data = EnemyPlacement(enemy_data.scene, enemy_data.group_name, enemy_data.child_id, picked_enemy,
                                          enemy_data.region)
                if picked_enemy not in chosen_enemies:
                    chosen_enemies.append(picked_enemy)
                enemy_counts[picked_enemy] += 1
                if picked_enemy in enemy_to_enemy_placement:
                    enemy_to_enemy_placement[picked_enemy].append(new_data)
                else:
                    enemy_to_enemy_placement[picked_enemy] = [new_data]
                randomized_enemy_placement.append(new_data)
            unused_enemies = [enemy for enemy in enemy_counts if enemy_counts[enemy] == 0]
            while len(unused_enemies) > 0:
                acceptable_enemies = [enemy for enemy in enemy_counts if enemy_counts[enemy] > 2]
                for checked_enemy in Enemy.randomizable_enemies:
                    if checked_enemy not in chosen_enemies:
                        random_enemy = self.random.choice(acceptable_enemies)
                        random_data = self.random.choice(enemy_to_enemy_placement[random_enemy])
                        enemy_to_enemy_placement[random_enemy].remove(random_data)
                        randomized_enemy_placement.remove(random_data)
                        enemy_counts[random_enemy] -= 1
                        new_data = EnemyPlacement(random_data.scene, random_data.group_name, random_data.child_id,
                                                  checked_enemy, random_data.region)
                        enemy_to_enemy_placement[checked_enemy] = [new_data]
                        enemy_counts[checked_enemy] = 1
                        randomized_enemy_placement.append(new_data)
                        chosen_enemies.append(checked_enemy)
                unused_enemies = [enemy for enemy in enemy_counts if enemy_counts[enemy] == 0]
        else:
            randomized_enemy_placement = base_enemy_placement

        mod_data = construct_flag_data_for_mod(randomized_enemy_placement)
        enemy_dictionary = construct_enemy_dictionary(randomized_enemy_placement)
        return mod_data, enemy_dictionary

    def pre_fill(self) -> None:
        if self.options.etnas_pupil and self.options.dropsanity == self.options.dropsanity.option_randomized:
            state = self.multiworld.get_all_state(False)
            logger.info(f"Randomized Drops and Etna's Pupil found in generation for Player {self.player}.  "
                        f"Adding progressives to dropsanity locations regardless of settings.")

            repeat_locations = [location for location in self.get_locations() if location.name in all_drops]
            self.random.shuffle(repeat_locations)
            repeat_locations = repeat_locations[0:80]

            fill_restrictive(self.multiworld, state, repeat_locations, self.local_alchemy,
                             single_player_placement=True, lock=True, allow_excluded=True)
        if len(self.local_filler) > 0:
            sphere_one_locations = [location for location in self.multiworld.get_reachable_locations(CollectionState(self.multiworld), self.player) if
                                    location.item is None]
            necessary_locations = set(self.random.sample(sphere_one_locations, 3))
            good_locations_to_fill = [location for location in self.multiworld.get_unfilled_locations(self.player)
                                      if location not in necessary_locations and location.name not in self.options.priority_locations]
            self.locations_for_filler = good_locations_to_fill

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld) -> None:
        lunacid_fill_worlds: List[LunacidWorld] = [world for world in multiworld.get_game_worlds("Lunacid")
                                                   if world.options.filler_local_percent.value > 0]
        if not lunacid_fill_worlds:
            return
        if multiworld.players > 1:
            for world in lunacid_fill_worlds:
                if world.options.filler_local_percent > 0:
                    world.random.shuffle(world.locations_for_filler)
                    for item in world.local_filler:
                        world.locations_for_filler.pop().place_locked_item(item)

    def get_pre_fill_items(self) -> List["Item"]:
        pre_fill_items = []
        pre_fill_items.extend(self.local_alchemy)
        pre_fill_items.extend(self.local_filler)
        return pre_fill_items

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        """Write to the spoiler header. If individual it's right at the end of that player's options,
        if as stage it's right under the common header before per-player options."""
        if self.options.entrance_randomization:
            self.add_entrances_to_spoiler_log()

    def add_entrances_to_spoiler_log(self) -> None:
        for original_entrance, replaced_entrance in self.randomized_entrances.items():
            self.multiworld.spoiler.set_entrance(original_entrance, replaced_entrance, "entrance", self.player)

    def important_item_locations(self):
        item_spots: Dict[str, List[List[str]]] = {}
        if self.options.progressive_symbols:
            location_info = [[self.multiworld.player_name[data.player] + "'s " + data.name, data.player, data.address]
                            for data in self.multiworld.find_item_locations(Progressives.vampiric_symbol, self.player)]
            item_spots[Progressives.vampiric_symbol] = location_info
        else:
            location_info = [[self.multiworld.player_name[data.player] + "'s " + data.name, data.player, data.address] for data in self.multiworld.find_item_locations(
                UniqueItem.vampiric_symbol_w, self.player)]
            item_spots[UniqueItem.vampiric_symbol_w] = location_info
            location_info = [[self.multiworld.player_name[data.player] + "'s " + data.name, data.player, data.address] for data in self.multiworld.find_item_locations(
                UniqueItem.vampiric_symbol_a, self.player)]
            item_spots[UniqueItem.vampiric_symbol_a] = location_info
            location_info = [[self.multiworld.player_name[data.player] + "'s " + data.name, data.player, data.address] for data in self.multiworld.find_item_locations(
                UniqueItem.vampiric_symbol_e, self.player)]
            item_spots[UniqueItem.vampiric_symbol_e] = location_info

        location_info = [[self.multiworld.player_name[data.player] + "'s " + data.name, data.player, data.address]
                         for data in self.multiworld.find_item_locations(Weapon.lucid_blade, self.player)]
        item_spots[Weapon.lucid_blade] = location_info
        for item in UniqueItem.completion_important:
            location_info = [[self.multiworld.player_name[data.player] + "'s " + data.name, data.player, data.address]
                             for data in self.multiworld.find_item_locations(item, self.player)]
            item_spots[item] = location_info
        if self.options.door_locks == self.options.door_locks.option_true:
            for key in Door.all_door_keys:
                location_info = [[self.multiworld.player_name[data.player] + "'s " + data.name, data.player, data.address]
                                 for data in self.multiworld.find_item_locations(key, self.player)]
                item_spots[key] = location_info
        if self.options.switch_locks == self.options.switch_locks.option_true:
            for key in Switch.switches:
                location_info = [[self.multiworld.player_name[data.player] + "'s " + data.name, data.player, data.address]
                                 for data in self.multiworld.find_item_locations(key, self.player)]
                item_spots[key] = location_info
        if self.options.ending == self.options.ending.option_ending_e:
            for spell in Spell.base_spells:
                location_info = [[self.multiworld.player_name[data.player] + "'s " + data.name, data.player, data.address]
                                 for data in self.multiworld.find_item_locations(spell, self.player)]
                item_spots[spell] = location_info
            if self.options.dropsanity != self.options.dropsanity.option_off:
                for spell in MobSpell.drop_spells:
                    location_info = [[self.multiworld.player_name[data.player] + "'s " + data.name, data.player, data.address]
                                     for data in self.multiworld.find_item_locations(spell, self.player)]
                    item_spots[spell] = location_info
        return item_spots

    def fill_slot_data(self) -> Dict[str, Any]:
        item_spots = self.important_item_locations()
        slot_data = {
            "ut_seed": self.seed,
            "seed": self.random.randrange(1000000000),  # Seed should be max 9 digits
            "client_version": "1.0.9",
            "rolled_month": self.rolled_month,
            "starting_weapon": self.starting_weapon.name,
            "elements": self.weapon_elements,
            "created_class_name": self.custom_class_name,
            "created_class_description": self.custom_class_description,
            "created_class_stats": self.custom_class_stats,
            "enemy_placement": self.enemy_random_data,
            "item_spots": item_spots,
            "enemy_regions": self.enemy_regions,
            "force_no_exp": self.options.challenges == self.options.challenges.option_exp,
            **self.options.as_dict("ending", "entrance_randomization",
                                   "required_strange_coin", "enemy_randomization", "shopsanity", "dropsanity",
                                   "quenchsanity", "etnas_pupil", "switch_locks", "door_locks", "random_elements",
                                   "secret_door_lock", "death_link", "starting_class",
                                   "starting_area", "levelsanity", "bookworm",
                                   "grasssanity", "breakables", "total_strange_coin", "random_equip_stats", "silver_link",
                                   "challenges", "tricks_and_glitches"),
            "entrances": self.randomized_entrances
        }

        return slot_data

    def interpret_slot_data(self, slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data
