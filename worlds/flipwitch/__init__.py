from random import Random
from typing import Dict, Any, List
import logging
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, CollectionState, MultiWorld
from Utils import visualize_regions
from worlds.AutoWorld import World, WebWorld
from . import options, tracker
from .data.locations import all_locations, FlipwitchLocation, stat_locations, shop_locations, quest_locations, sex_experience_locations, \
    gacha_locations, coin_locations, \
    chaos_piece_location_names, pot_locations, warp_locations, event_sex_locations, event_quest_locations
from .options import FlipwitchOptions
from .data.items import FlipwitchItemData
from .strings.locations import WitchyWoods, GhostCastle, ClubDemon, AngelicHallway, SlimeCitadel, UmiUmi, witchy_woods_locations, spirit_town_locations, \
    shady_sewer_locations, ghostly_castle_locations, jigoku_locations, tengoku_locations, fungal_forest_locations, slime_citadel_locations, umi_umi_locations, \
    chaos_castle_locations
from .strings.regions_entrances import ChaosCastleRegion, FungalForestRegion, CrystalRegion
from .strings.items import GoalItem, Power, Upgrade, Key
from .strings.locations import Gacha
from .strings.fake_hints import possible_fakes
from .items import item_table, complete_items_by_name, create_items
from .locations import location_table, create_locations
from .regions import create_regions, ConnectionData, randomized_entrance_names
from .rules import FlipwitchRules

logger = logging.getLogger()


class FlipwitchItem(Item):
    game: str = "Flipwitch"


class FlipwitchWeb(WebWorld):
    theme = "partyTime"
    rating: str = "nsfw"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Flipwitch randomizer connected to a MultiworldGG Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Albrekka", "Prin", "SomeLazyGamer"]
    )]


class FlipwitchWorld(World):
    """
    Use your newly-acquired genderbending abilities as a 'FlipWitch' to conquer evil monsters, giant bosses, and Monster Girls across the land!
    You'll have to use your wits in this quirky adventure to seduce everyone around you!
    """

    game = "Flipwitch Forbidden Sex Hex"
    author: str = "Albrekka"
    topology_present = False
    item_name_to_id = {item.name: item.code for item in item_table}
    location_name_to_id = {location.name: location.location_id for location in location_table}

    item_name_groups = {
    }

    location_name_groups = {
        "Witchy Woods": witchy_woods_locations,
        "Spirit City": spirit_town_locations,
        "Shady Sewers": shady_sewer_locations,
        "Ghostly Castle": ghostly_castle_locations,
        "Jigoku": jigoku_locations,
        "Tengoku": tengoku_locations,
        "Fungal Forest": fungal_forest_locations,
        "Slime Citadel": slime_citadel_locations,
        "Umi Umi": umi_umi_locations,
        "Chaos Castle": chaos_castle_locations,
    }

    required_client_version = (0, 5, 0)

    options_dataclass = FlipwitchOptions
    options: FlipwitchOptions
    web = FlipwitchWeb()
    logger = logging.getLogger()
    world_entrances = {}
    animal_order = []
    bunny_order = []
    monster_order = []
    angel_order = []
    item_lookup = {}
    hint_lookup = {}
    area_order = []
    necessary_to_do_order: Dict[int, str] = {}
    packaged_hints = {}

    passthrough: Dict[str, Any]
    using_ut: bool = False
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml

    def __init__(self, multiworld, player):
        super(FlipwitchWorld, self).__init__(multiworld, player)
        slot_data = getattr(multiworld, "re_gen_passthrough", {}).get("Flipwitch Forbidden Sex Hex")
        if slot_data:
            self.seed = slot_data.get("ut_seed")
            self.using_ut = True
        else:
            self.seed = self.random.getrandbits(64)
        self.random = Random(self.seed)

    def generate_early(self) -> None:
        tracker.setup_options_from_slot_data(self)

    def create_item(self, name: str, override_classification: ItemClassification = None) -> "FlipwitchItem":
        item_id: int = self.item_name_to_id[name]

        if override_classification is None:
            override_classification = complete_items_by_name[name].classification

        return FlipwitchItem(name, override_classification, item_id, player=self.player)

    def create_event(self, event: str):
        return Item(event, ItemClassification.progression_skip_balancing, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(["Nothing"])

    def set_rules(self):
        self.determine_gacha_order(self.multiworld, self.random)
        FlipwitchRules(self).set_flipwitch_rules(self.animal_order, self.bunny_order, self.monster_order, self.angel_order)

    def create_items(self):
        locations_count = len([location
                               for location in self.get_locations() if location.item is None])
        excluded_items = self.multiworld.precollected_items[self.player]
        potential_pool, self.hint_lookup = create_items(self.create_item, locations_count, excluded_items, self.options, self.random)
        self.multiworld.itempool += potential_pool

    def create_regions(self):
        world = self.multiworld
        player = self.player

        def create_region(region_name: str, exits: List[ConnectionData]) -> Region:
            flipwitch_region = Region(region_name, player, world)
            true_exits = [connector.name for connector in exits]
            flipwitch_region.exits = [Entrance(player, true_exit, flipwitch_region) for true_exit in true_exits]
            return flipwitch_region

        world_regions, world_entrances, = create_regions(create_region, world)
        self.world_entrances = world_entrances
        real_locations, event_locations = create_locations(self.random, self.options)

        for location in real_locations:
            name = location.name
            location_id = location.location_id
            region: Region = world_regions[location.region]
            region.add_locations({name: location_id})

        self.place_event_items_in_event_locations(event_locations, world_regions)

        self.multiworld.regions.extend(world_regions.values())

        ending_region = world.get_region(ChaosCastleRegion.cc_chaos_witch, player)
        ending_region.add_event("Defeat the Chaos Queen", "Victory", show_in_spoiler=True)

        world.completion_condition[self.player] = lambda state: state.has("Victory", player)

    def place_event_items_in_event_locations(self, event_locations_from_settings: Dict[str, List[FlipwitchLocation]], region_lookup: Dict[str, Region]):
        show_spoiler = self.options.quest_for_sex != self.options.quest_for_sex.option_off
        for region in event_locations_from_settings:
            for location in event_locations_from_settings[region]:
                region_lookup[region].add_event(location.name, location.forced_off_item)

        if self.options.quest_for_sex != self.options.quest_for_sex.option_all:
            for region in event_sex_locations:
                for location in event_sex_locations[region]:
                    region_lookup[region].add_event(location.name, location.forced_off_item)
        for region in event_quest_locations:
            for location in event_quest_locations[region]:
                region_lookup[region].add_event(location.name, location.forced_off_item)

    # def connect_entrances(self) -> None:
        # self.visualize_regions()

    def visualize_regions(self):
        multiworld = self.multiworld
        player = self.player
        regions_to_check = set([location.parent_region for location in self.multiworld.get_reachable_locations(CollectionState(self.multiworld), self.player) if
                                    location.item is None])
        visualize_regions(multiworld.get_region(CrystalRegion.menu, player), f"{multiworld.get_out_file_name_base(player)}.puml", show_locations=False, regions_to_highlight=regions_to_check)

    def get_groups_for_location(self, location: Location):
        player_game = self.multiworld.worlds[location.player]
        return [group for group in player_game.location_name_groups if location.name in player_game.location_name_groups[group] and group != "Everywhere"]

    def package_hints(self):
        packaged_hints: Dict[str, str] = {}
        for item in self.hint_lookup:
            is_junk = self.random.choice(range(101)) < self.options.junk_hint.value
            spot_location = self.hint_lookup[item].location
            if spot_location is None:
                self.write_hint(item, "in your starting inventory probably", is_junk, packaged_hints)
                continue
            player = self.multiworld.player_name[spot_location.player]
            possible_spots = self.get_groups_for_location(spot_location)
            if len(possible_spots) > 0:
                area = self.random.choice(possible_spots)
            else:
                area = self.hint_lookup[item].location.parent_region.name
                if area == "Menu":
                    area = "some area"
            if self.player == self.hint_lookup[item].location.player:
                self.write_hint(item, area + " in this world", is_junk, packaged_hints)
            else:
                area.replace("REGION_", "")  # I try I guess.
                while len(area) > 25:
                    if " " not in area:
                        break
                    area_array = area.split(" ")
                    area_array = area_array[:-1]
                    area = " ".join(area_array)
                if len(area) > 25:
                    area = area[:25]
                modified_player = player.replace("[", "(").replace("]", ")")
                self.write_hint(item, area + " in " + modified_player + "'s world", is_junk, packaged_hints)
        self.packaged_hints = packaged_hints

        for sphere in self.multiworld.get_spheres():
            for location in sphere:
                if location.address is None:  # Sometimes, an important location is made an event.  The player should know about it already.
                    continue
                if location.player != self.player or not location.item.advancement:
                    continue
                if location.name == "Defeat the Chaos Queen":
                    self.necessary_to_do_order[-100] = "I see the Chaos Queen's face.  It is time to face her and be victorious!"
                    break
                else:
                    possible_groups = self.get_groups_for_location(location)
                    if not possible_groups:
                        continue  # Curious about this scenario.
                    chosen_candidate = self.random.choice(possible_groups)
                    player_id = location.item.player
                    if self.player == player_id:
                        player = "yourself"
                    else:
                        player = "one named " + self.multiworld.player_name[player_id]
                    self.necessary_to_do_order[location.address] = "I sense something within [COLOR:YELLOW]" + chosen_candidate + "[COLOR:WHITE], an item for " + player + ".  What it is, I cannot make out, but it seems vital."

    def write_hint(self, item: str, message, is_junk: bool, hint_package: Dict[str, str]):
        if is_junk:
            hint_package[item] = self.random.choice(possible_fakes)
        else:
            hint_package[item] = message
        return hint_package

    def determine_gacha_order(self, multiworld: MultiWorld, random: Random):
        slot_data = getattr(multiworld, "re_gen_passthrough", {}).get("Flipwitch Forbidden Sex Hex")
        if not slot_data:
            bunny_order = Gacha.bunny_gacha.copy()
            random.shuffle(bunny_order)
            self.bunny_order = bunny_order
            animal_order = Gacha.animal_gacha.copy()
            random.shuffle(animal_order)
            self.animal_order = animal_order
            monster_order = Gacha.monster_gacha.copy()
            random.shuffle(monster_order)
            self.monster_order = monster_order
            angel_order = Gacha.angel_demon_gacha.copy()
            random.shuffle(angel_order)
            self.angel_order = angel_order


    def fill_slot_data(self) -> Dict[str, Any]:
        self.package_hints()
        slot_data = {
            "ut_seed": self.seed,
            "seed": self.random.randrange(1000000000),  # Seed should be max 9 digits
            "client_version": "1.0.5",
            "animal_order": self.animal_order,
            "bunny_order": self.bunny_order,
            "monster_order": self.monster_order,
            "angel_order": self.angel_order,
            "hints": self.packaged_hints,
            "path": self.necessary_to_do_order,
            **self.options.as_dict("starting_gender", "gachapon_shuffle", "shopsanity", "shop_prices", "stat_shuffle", "pottery_lottery",
                                   "shuffle_chaos_pieces", "gachapon_shuffle", "quest_for_sex", "crystal_teleports", "death_link", "starting_area",
                                   "shuffle_double_jump", "shuffle_dodge"),
        }
        return slot_data

    def print_hints(self):
        output = open("Output.txt", "w+")
        for item in self.packaged_hints:

            output.write(self.hint_lookup[item].location.name + ": " + self.packaged_hints[item] + "\n")

    def interpret_slot_data(self, slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data
