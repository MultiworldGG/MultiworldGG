import settings
import typing
import os
import logging
from typing import Dict, Any, TextIO
from BaseClasses import (Tutorial, CollectionState, MultiWorld, ItemClassification as ic, LocationProgressType)
from .modules.random_battles import get_boss_battles
from .SettingsString import load_settings_from_site_string
from worlds.AutoWorld import World, WebWorld
from . import Locations, options
from .data.chapter_logic import areas_by_chapter, get_chapter_excluded_location_names
from .modules.modify_entrances import get_bowser_rush_pairs, get_bowser_shortened_pairs
from .modules.random_audio import get_randomized_audio
from .modules.random_map_mirroring import get_mirrored_map_list
from .modules.random_movecosts import get_randomized_moves
from .modules.random_palettes import get_randomized_palettes
from .Regions import PMRegion
from .RuleParser import Rule_AST_Transformer
from .Entrance import PMEntrance
from .Utils import load_json_data
from .Locations import PMLocation, location_factory, location_name_to_id
from .ItemPool import generate_itempool
from .items import PMItem, pm_is_item_of_type, pm_data_to_ap_id, ap_id_to_pm_data, item_id_prefix
from .data.ItemList import item_table, item_groups, progression_miscitems, item_multiples_ids
from .data.itemlocation_special import limited_by_item_areas
from .data.itemlocation_replenish import replenishing_itemlocations
from .data.LocationsList import location_table, location_groups, ch8_locations
from .modules.random_actor_stats import get_shuffled_chapter_difficulty
from .Rules import set_rules
from .modules.random_partners import get_rnd_starting_partners
from .options import (SeedGoal, PaperMarioOptions, ShuffleKootFavors, PartnerUpgradeShuffle, HiddenBlockMode,
                      ShuffleSuperMultiBlocks, GearShuffleMode, StartingMap, BowserCastleMode, ShuffleLetters,
                      ItemTraps, MirrorMode, ShufflePartners, ShuffleKeys, ShuffleDungeonEntrances, BossShuffle,
                      SpiritRequirements, ConsumableItemPool, StartingBoots)
from .data.node import Node
from .data.starting_maps import starting_maps
from .Rom import generate_output, PaperMarioProcedurePatch
from Fill import fill_restrictive, remaining_fill
import pkg_resources
from .client import PaperMarioClient  # unused but required for generic client to hook onto
logger = logging.getLogger("Paper Mario")


class PaperMarioSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Paper Mario USA ROM"""
        description = "Paper Mario ROM File"
        copy_to = "Paper Mario (USA).z64"
        md5s = [PaperMarioProcedurePatch.hash]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
                    true  for operating system default program
        Alternatively, a path to a program to open the .z64 file with
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = True


# information for the supported games setup guide; set up to make it easier to add more guides
class PaperMarioWeb(WebWorld):
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A Guide to setting up the Paper Mario 64 randomizer connected to a MultiworldGG world",
        "English",
        "setup_en.md",
        "setup/en",
        ["JKB"]
    )

    # set tutorials to the list of each setup
    tutorials = [setup]


class PaperMarioWorld(World):
    """
    Paper Mario is a turn-based adventure RPG. Bowser has kidnapped Princess Peach along with her castle using the
    power of the Star Rod, which grants the wishes of the holder. You must rescue the Star Spirits so that they can
    help you take back the Star Rod from Bowser and save Peach. You will have to defeat powerful foes
    and venture through dangerous lands with the help of partners you meet along the way.
    """
    game = "Paper Mario"
    author: str = "JKB & icebound777"
    web = PaperMarioWeb()
    topology_present = True

    options_dataclass = PaperMarioOptions
    options: PaperMarioOptions

    settings_key = "paper_mario_settings"
    settings: typing.ClassVar[PaperMarioSettings]

    item_name_to_id = {item_name: pm_data_to_ap_id(data, False) for item_name, data in item_table.items()}
    location_name_to_id = location_name_to_id

    item_name_groups = item_groups
    location_name_groups = location_groups

    data_version = 1
    required_client_version = (0, 4, 4)
    auth: bytes

    def __init__(self, multiworld, player):
        super(PaperMarioWorld, self).__init__(multiworld, player)

        # For generation
        self.placed_items = []
        self.entrance_list = []

        self.required_spirits = []
        self.excluded_spirits = []
        self.excluded_areas = []
        self.ch_excluded_locations = []
        self.ch_excluded_location_names = []

        self.itempool = []
        self.pre_fill_items = []
        self.dungeon_restricted_items = {}
        self.dro_shop_puzzle_items = []
        self.remove_from_start_inventory = []
        self.web_start_inventory = []
        self.trappable_item_names = []

        self._regions_cache = {}
        self.parser = Rule_AST_Transformer(self, self.player)

        self.regions = []
        self.battle_list = []

        self.spoilerlog_puzzles = {}

    # Do some housekeeping before generating, namely fixing some options that might be incompatible with each other
    def generate_early(self) -> None:
        # load settings from pmr string before anything else, since almost all settings can be loaded this way
        if self.options.pmr_settings_string.value != "None":
            load_settings_from_site_string(self)

        # fail generation if attempting to use options that are not fully implemented yet
        nyi_warnings = ""
        if self.options.shuffle_dungeon_entrances.value != ShuffleDungeonEntrances.option_Off:  # NYI
            nyi_warnings += "\n'shuffle_dungeon_entrances' must be set to Off"
        if self.options.boss_shuffle.value:  # NYI
            nyi_warnings += "\n'boss_shuffle' must be set to False"
        if self.options.mirror_mode.value == MirrorMode.option_Static_Random:  # NYI
            nyi_warnings += "\n'mirror_mode' cannot be set to Static_Random"

        if nyi_warnings:
            nyi_warnings = ((f"Paper Mario: {self.player} ({self.multiworld.player_name[self.player]}) has settings "
                             "are not yet implemented in the .apworld being used for generation. "
                             "Please check for a newer release and/or adjust the settings below : ") + nyi_warnings)
            raise ValueError(nyi_warnings)

        # LCL is not compatible with several options
        # Rather than generate with drastically different settings, compile list of incompatible settings
        if self.options.spirit_requirements.value == SpiritRequirements.option_Specific_And_Limit_Chapter_Logic:
            lcl_warnings = ""
            if self.options.koot_favors.value != ShuffleKootFavors.option_Vanilla:
                lcl_warnings += "\n'koot_favors' must be set to vanilla"
            if self.options.letter_rewards.value == ShuffleLetters.option_Final_Letter_Chain_Reward:
                lcl_warnings += "\n'letter_rewards' cannot be set to Final_Letter_Chain_Reward"
            if self.options.gear_shuffle_mode.value != GearShuffleMode.option_Full_Shuffle:
                lcl_warnings += "\n'gear_shuffle_mode' must be set to full_shuffle"
            if not self.options.keysanity.value:
                lcl_warnings += "\n'keysanity' must be set to True"
            if self.options.partners.value != ShufflePartners.option_Full_Shuffle:
                lcl_warnings += "\n'partners' must be set to full_shuffle"

            if lcl_warnings:
                lcl_warnings = (f"Paper Mario: {self.player} ({self.multiworld.player_name[self.player]}) has limit "
                                "chapter logic set to true, but the following settings are incompatible with limiting "
                                "chapter logic: ") + lcl_warnings
                raise ValueError(lcl_warnings)

        # Make sure it doesn't try to shuffle Koot coins if rewards aren't shuffled
        if self.options.koot_favors.value == ShuffleKootFavors.option_Vanilla:
            self.options.koot_coins.value = False

        # turn off individual partner toggles if starting with random partners was selected
        if self.options.start_random_partners.value:
            self.options.start_with_goombario.value = False
            self.options.start_with_kooper.value = False
            self.options.start_with_bombette.value = False
            self.options.start_with_parakarry.value = False
            self.options.start_with_bow.value = False
            self.options.start_with_watt.value = False
            self.options.start_with_sushie.value = False
            self.options.start_with_lakilester.value = False

        # turn on random partner if no partners were selected; debatable whether to use min/max here or set both to 1.
        elif not (self.options.start_with_goombario.value or self.options.start_with_kooper.value
                  or self.options.start_with_bombette.value or self.options.start_with_parakarry.value
                  or self.options.start_with_bow.value or self.options.start_with_watt.value
                  or self.options.start_with_sushie.value or self.options.start_with_lakilester.value):
            logging.warning(f"Paper Mario: {self.player} ({self.multiworld.player_name[self.player]}) did not select a "
                            f"starting partner and will be given one at random.")
            self.options.start_random_partners.value = True

        if self.options.start_random_partners.value:
            starting_partners = get_rnd_starting_partners(self.options.start_partners.value, self.random)

            for partner in starting_partners:
                if partner == "Goombario":
                    self.options.start_with_goombario.value = True
                elif partner == "Kooper":
                    self.options.start_with_kooper.value = True
                elif partner == "Bombette":
                    self.options.start_with_bombette.value = True
                elif partner == "Parakarry":
                    self.options.start_with_parakarry.value = True
                elif partner == "Bow":
                    self.options.start_with_bow.value = True
                elif partner == "Watt":
                    self.options.start_with_watt.value = True
                elif partner == "Sushie":
                    self.options.start_with_sushie.value = True
                elif partner == "Lakilester":
                    self.options.start_with_lakilester.value = True

        # limit chapter logic only applies when using the specific star spirits setting
        if self.options.spirit_requirements.value == SpiritRequirements.option_Any:
            self.require_specific_spirits = False
            self.required_spirits = []
            self.excluded_spirits = []
        else:
            self.require_specific_spirits = True

            # determine which star spirits are needed
            remaining_spirits = [i for i in range(1, 8)]
            chosen_spirits = []

            for _ in range(self.options.star_way_spirits.value):
                rnd_spirit = self.random.randint(0, len(remaining_spirits) - 1)
                chosen_spirits.append(remaining_spirits.pop(rnd_spirit))

            self.required_spirits = chosen_spirits

            if self.options.spirit_requirements.value == SpiritRequirements.option_Specific_And_Limit_Chapter_Logic:
                self.excluded_spirits = remaining_spirits

                for chapter in remaining_spirits:
                    self.excluded_areas.extend(areas_by_chapter[chapter])

                self.ch_excluded_location_names = get_chapter_excluded_location_names(self.excluded_spirits,
                                                                self.options.letter_rewards.value)

        if self.options.seed_goal.value == SeedGoal.option_Open_Star_Way:
            self.ch_excluded_location_names.extend(ch8_locations)

        # set power star counts to 0 if option is not being used
        if not self.options.power_star_hunt.value:
            self.options.star_way_power_stars.value = 0
            self.options.star_beam_power_stars.value = 0
            self.options.total_power_stars.value = 0
        else:
            # ensure there are at least as many power stars as there are required for star way and star beam
            # if total power stars is less than either, then put it 15% higher than the bigger requirement, max 120
            required_power_stars = self.options.star_way_power_stars.value
            if self.options.seed_goal.value == SeedGoal.option_Open_Star_Way:
                required_power_stars = max(required_power_stars, self.options.star_beam_power_stars.value)

            if self.options.total_power_stars.value < required_power_stars:
                self.options.total_power_stars.value = min(120, int(1.15 * required_power_stars))
                logger.info(f"Paper Mario: {self.player} ({self.multiworld.player_name[self.player]}) had less total "
                            f"power stars than the required amount. New total set to 15% more than the larger "
                            f"requirement, restricted to 120 or fewer.")

        # shuffle bosses - NYI
        self.battles, self.boss_chapter_map = get_boss_battles(self.options.boss_shuffle.value, self.random)

    def create_regions(self) -> None:
        # Create base regions
        menu = PMRegion("Menu", self.player, self.multiworld)
        start = PMEntrance(self.player, self.multiworld, 'New Game', menu)
        menu.exits.append(start)
        self.multiworld.regions.append(menu)

        # Load region json files
        for file in pkg_resources.resource_listdir(__name__, "data/regions"):
            if not pkg_resources.resource_isdir(__name__, "data/regions/" + file):
                readfile = True
                match file:
                    case "bowser's_castle.json":
                        readfile = (self.options.bowser_castle_mode.value == BowserCastleMode.option_Vanilla and
                                    self.options.seed_goal.value != SeedGoal.option_Open_Star_Way)
                    case "bowser's_castle_shortened.json":
                        readfile = (self.options.bowser_castle_mode.value == BowserCastleMode.option_Shortened and
                                    self.options.seed_goal.value != SeedGoal.option_Open_Star_Way)
                    case "bowser's_castle_boss_rush.json":
                        readfile = (self.options.bowser_castle_mode.value == BowserCastleMode.option_Boss_Rush and
                                    self.options.seed_goal.value != SeedGoal.option_Open_Star_Way)
                    case "shooting_star_summit_no_star_way.json":
                        readfile = self.options.seed_goal.value == SeedGoal.option_Open_Star_Way
                    case "shooting_star_summit.json":
                        readfile = self.options.seed_goal.value != SeedGoal.option_Open_Star_Way
                    case "peachs_castle.json":
                        readfile = self.options.seed_goal.value != SeedGoal.option_Open_Star_Way

                if readfile:
                    self.load_regions_from_json("regions/" + file)

        # Connect start to chosen starting map
        start.connect(self.get_region(starting_maps[self.options.starting_map.value][1]))

        self.parser.create_delayed_rules()

        # Connect exits
        for region in self.regions:
            for exit in region.exits:
                exit.connect(self.get_region(exit.vanilla_connected_region))

        # handle any changed entrances
        if self.options.bowser_castle_mode.value == BowserCastleMode.option_Boss_Rush:
            self.entrance_list = get_bowser_rush_pairs()
        elif self.options.bowser_castle_mode.value == BowserCastleMode.option_Shortened:
            self.entrance_list = get_bowser_shortened_pairs()

    def create_items(self) -> None:
        # This checks what locations are being included, gets those items, places non-shuffled items,
        # adds any desired beta items and badges, ensures we have the correct number of items by removing coins or
        # adding Tayce T items, and randomizes the consumables pool according to the player's settings.
        generate_itempool(self)

        # Starting inventory
        # Gear
        for boots in range(1, self.options.starting_boots.value + 2):
            self.multiworld.push_precollected(self.create_item("Progressive Boots"))
            self.remove_from_start_inventory.append("Progressive Boots")

        for hammer in range(1, self.options.starting_hammer.value + 2):
            self.multiworld.push_precollected(self.create_item("Progressive Hammer"))
            self.remove_from_start_inventory.append("Progressive Hammer")

        # Partners
        if self.options.start_with_goombario.value:
            self.multiworld.push_precollected(self.create_item("Goombario"))
            self.remove_from_start_inventory.append("Goombario")
        if self.options.start_with_kooper.value:
            self.multiworld.push_precollected(self.create_item("Kooper"))
            self.remove_from_start_inventory.append("Kooper")
        if self.options.start_with_bombette.value:
            self.multiworld.push_precollected(self.create_item("Bombette"))
            self.remove_from_start_inventory.append("Bombette")
        if self.options.start_with_parakarry.value:
            self.multiworld.push_precollected(self.create_item("Parakarry"))
            self.remove_from_start_inventory.append("Parakarry")
        if self.options.start_with_bow.value:
            self.multiworld.push_precollected(self.create_item("Bow"))
            self.remove_from_start_inventory.append("Bow")
        if self.options.start_with_watt.value:
            self.multiworld.push_precollected(self.create_item("Watt"))
            self.remove_from_start_inventory.append("Watt")
        if self.options.start_with_sushie.value:
            self.multiworld.push_precollected(self.create_item("Sushie"))
            self.remove_from_start_inventory.append("Sushie")
        if self.options.start_with_lakilester.value:
            self.multiworld.push_precollected(self.create_item("Lakilester"))
            self.remove_from_start_inventory.append("Lakilester")

        starting_items = []

        # Items from setting string and/or random starting items
        if self.web_start_inventory:
            for item_name in self.web_start_inventory:
                item_to_add = self.create_item(item_name)
                starting_items.append(item_to_add)

        # Start with up to 16 random items on top of anything else already included
        if self.options.random_start_items.value:
            self.random.shuffle(self.itempool)

            # Mario can only hold 10 consumables, so disallow more than 10 from being sent to his inventory
            popped_consumables = []
            consumable_count = 0

            while len(starting_items) < self.options.random_start_items.value:
                item_to_add = self.itempool.pop()
                if item_to_add.type == "ITEM" and consumable_count == 10:
                    popped_consumables.append(item_to_add)
                else:
                    starting_items.append(item_to_add)
                    if item_to_add.type == "ITEM":
                        consumable_count += 1

            # add items back to itempool regardless of if they were in starting_items or not
            # removed items are handled in next block
            self.itempool.extend(starting_items)
            self.itempool.extend(popped_consumables)

        for item in starting_items:
            self.multiworld.push_precollected(item)

        # handle start inventory, be it from the AP option or from
        removed_items = []
        for item in self.multiworld.precollected_items[self.player]:
            if item.name in self.remove_from_start_inventory:
                self.remove_from_start_inventory.remove(item.name)
                removed_items.append(item.name)
            elif item in self.itempool:
                self.itempool.remove(item)
                self.itempool.append(self.create_item(self.get_filler_item_name()))

        # remove prefill items from item pool to be randomized
        (self.itempool, self.pre_fill_items,
         self.dungeon_restricted_items, self.dro_shop_puzzle_items) = self.divide_itempools()

        self.multiworld.itempool.extend(self.itempool)
        self.remove_from_start_inventory.extend(removed_items)

        # get valid trap items from remaining pool if needed
        if self.options.item_traps.value > ItemTraps.option_No_Traps:
            trappable_items = list(filter(lambda item: item.type not in ["ITEM", "COIN"], self.itempool))
            self.trappable_item_names = [item.name for item in trappable_items]
            # Bias towards placing Ultra Stone or upgrade traps, done in base PMR as well as requested by clover
            if self.options.partner_upgrades.value == PartnerUpgradeShuffle.option_Vanilla:
                self.trappable_item_names.extend(["Ultra Stone"] * 9)
            else:
                self.trappable_item_names.extend(item_groups["PartnerUpgrade"])


    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self):
        self.auth = bytearray(self.multiworld.random.getrandbits(8) for _ in range(16))

        # remove internal event locations that are not going to exist in this seed
        all_state = self.get_state_with_complete_itempool()
        all_locations = self.get_locations()
        all_state.sweep_for_advancements(locations=all_locations)
        reachable = self.multiworld.get_reachable_locations(all_state, self.player)
        unreachable = [loc for loc in all_locations if
                       loc.internal and loc.event and loc.locked and loc not in reachable]
        for loc in unreachable:
            loc.parent_region.locations.remove(loc)

        if self.options.open_forest.value:
            loc = self.multiworld.get_location("TT Southern District Fice T. Forest Pass", self.player)
            loc.parent_region.locations.remove(loc)

    def load_regions_from_json(self, file_path):
        region_json = load_json_data(file_path)
        region: Dict[str, Any]
        for region in region_json:
            region_prefix = region['region_name'][:3]
            new_region = PMRegion(region['region_name'], self.player, self.multiworld)
            if 'map_id' in region:
                new_region.map_id = region['map_id']
            if 'area_id' in region:
                new_region.font_color = region['area_id']
            if 'map_name' in region:
                new_region.scene = region['map_name']
            if 'locations' in region and region_prefix not in self.excluded_areas:
                for location, rule in region['locations'].items():
                    if location not in self.ch_excluded_location_names:
                        new_location = location_factory(location, self.player)
                        new_location.parent_region = new_region
                        new_location.rule_string = rule
                        self.parser.parse_spot_rule(new_location)
                        if new_location.never:
                            # We still need to fill the location even if ALR is off.
                            logger.debug('Unreachable location: %s', new_location.name)
                        new_location.player = self.player
                        new_region.locations.append(new_location)
            if 'events' in region and region_prefix not in self.excluded_areas:
                for event, rule in region['events'].items():
                    # Allow duplicate placement of events
                    lname = '%s from %s' % (event, new_region.name)
                    new_location = PMLocation(self.player, lname, event=True, parent=new_region)
                    new_location.rule_string = rule
                    self.parser.parse_spot_rule(new_location)
                    if new_location.never:
                        logger.debug('Dropping unreachable event: %s', new_location.name)
                    else:
                        new_location.player = self.player
                        new_region.locations.append(new_location)
                        self.make_event_item(event, new_location)
                        new_location.show_in_spoiler = False
            if 'exits' in region:
                for exit, rule in region['exits'].items():
                    new_exit = PMEntrance(self.player, self.multiworld, f"{new_region.name} -> {exit}", new_region)
                    new_exit.vanilla_connected_region = exit
                    new_exit.rule_string = rule
                    self.parser.parse_spot_rule(new_exit)
                    if new_exit.never:
                        logger.debug('Dropping unreachable exit: %s', new_exit.name)
                    else:
                        new_region.exits.append(new_exit)

            self.multiworld.regions.append(new_region)
            self.regions.append(new_region)
            self._regions_cache[new_region.name] = new_region

    # Note on allow_arbitrary_name:
    # PM defines many helper items and event names that are treated indistinguishably from regular items,
    # but are only defined in the logic files. This means we need to create items for any name.
    # Allowing any item name to be created is dangerous in case of plando, so this is a middle ground.
    def create_item(self, name: str, allow_arbitrary_name: bool = False):
        if name in item_table:
            return PMItem(name, self.player, item_table[name], False)
        if allow_arbitrary_name:
            return PMItem(name, self.player, ('Event', ic.progression, None, None, False, False, False), True)
        raise Exception(f"Invalid item name: {name}")

    def make_event_item(self, name, location, item=None):
        if item is None:
            item = self.create_item(name, allow_arbitrary_name=True)
        self.multiworld.push_item(location, item, collect=False)
        location.locked = True
        location.event = True
        if name not in item_table:
            location.internal = True
        return item

    def divide_itempools(self):
        main_items = []
        prefill_item_names = []
        dungeon_restricted_items = {}
        dro_shop_puzzle_item_names = []

        # progression items that need to be in replenishable locations
        for item in progression_miscitems:
            prefill_item_names.append(item)

        # key items shuffled within their own dungeons
        if not self.options.keysanity.value:
            for dungeon in limited_by_item_areas:
                for itemlist in limited_by_item_areas[dungeon].values():
                    for item in itemlist:
                        dungeon_restricted_items[item] = dungeon
                        prefill_item_names.append(item)

        # gear items shuffled among gear locations
        if self.options.gear_shuffle_mode.value == GearShuffleMode.option_Gear_Location_Shuffle:
            for item in self.itempool:
                if item.name in item_groups["Gear"]:
                    prefill_item_names.append(item.name)

        # partners if shuffled among partner locations
        if self.options.partners.value == ShufflePartners.option_Partner_Locations:
            for item in self.itempool:
                if item.name in item_groups["Partner"]:
                    prefill_item_names.append(item.name)

        # partner upgrades shuffled among super block locations, which may be shuffled
        if self.options.partner_upgrades.value == PartnerUpgradeShuffle.option_Super_Block_Locations:
            for item in self.itempool:
                if item.name in item_groups["PartnerUpgrade"]:
                    prefill_item_names.append(item.name)

        if self.options.super_multi_blocks.value == ShuffleSuperMultiBlocks.option_Shuffle:
            for item in self.itempool:
                if item.name == "Coin Bag":
                    prefill_item_names.append(item.name)

        # ensure DDO shop has 3 cheap consumables for puzzle purposes if needed
        if self.options.random_puzzles.value and self.options.include_shops.value and not (
                self.options.spirit_requirements.value == SpiritRequirements.option_Specific_And_Limit_Chapter_Logic and
                2 in self.excluded_spirits):
            for item in self.itempool:
                if (item_table[item.name][0] == "ITEM"
                        and item_table[item.name][3] <= 10 and item_table[item.name][2] <= 0xFF
                        and len(dro_shop_puzzle_item_names) < 3 and item.name not in dro_shop_puzzle_item_names
                        and item.classification == ic.filler):
                    dro_shop_puzzle_item_names.append(item.name)

            # sometimes the item pool is restricted, such as when the item pool is set to be mystery only
            # account for that by putting in consumables that need to be in replenishable locations anyways
            if len(dro_shop_puzzle_item_names) < 3:
                while len(dro_shop_puzzle_item_names) < 3:
                    consumable = self.random.choice(progression_miscitems)
                    if consumable not in dro_shop_puzzle_item_names:
                        dro_shop_puzzle_item_names.append(consumable)
                        prefill_item_names.remove(consumable)

        prefill_items = []
        dro_shop_puzzle_items = []
        local_consumable_chance = self.options.local_consumables.value
        for item in self.itempool:

            if item.name in prefill_item_names:
                prefill_items.append(item)
                prefill_item_names.remove(item.name)
            elif item.name in dro_shop_puzzle_item_names and item not in dro_shop_puzzle_items:
                dro_shop_puzzle_items.append(item)
            else:
                # check if this item gets kept local or not
                # sets extra copies of consumable progression items to be filler so that they aren't considered in logic
                keep_local = False
                if item.type == "ITEM" and item.classification != ic.trap:
                    item.classification = ic.filler
                    keep_local = self.random.randint(0, 100) <= local_consumable_chance
                elif item.type == "PARTNERUPGRADE":
                    keep_local = (self.options.partner_upgrades.value !=
                                  PartnerUpgradeShuffle.option_Full_Shuffle)
                elif item.name in prefill_item_names and item.type == "KEYITEM":
                    keep_local = (self.options.keysanity.value == ShuffleKeys.option_false)
                elif item.name in prefill_item_names and item.type == "GEAR":
                    keep_local = (self.options.gear_shuffle_mode.value <= GearShuffleMode.option_Full_Shuffle)
                elif item.name in prefill_item_names and item.type == "PARTNER":
                    keep_local = (self.options.partners.value <= ShufflePartners.option_Full_Shuffle)

                if keep_local:
                    prefill_items.append(item)
                else:
                    main_items.append(item)

        return main_items, prefill_items, dungeon_restricted_items, dro_shop_puzzle_items

    # handle player-specific stuff like cosmetics, audio, enemy stats, etc.

    # only returns proper result after create_items and divide_itempools are run
    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self):

        def prefill_state(base_state):
            state = base_state.copy()
            for item in self.get_pre_fill_items():
                self.collect(state, item)
            state.sweep_for_advancements(locations=self.get_locations())
            return state

        # Prefill required replenishable items, local key items depending on settings
        locations = list(self.multiworld.get_unfilled_locations(self.player))
        self.multiworld.random.shuffle(locations)

        # Set up initial state
        state = CollectionState(self.multiworld)
        for item in self.itempool:
            self.collect(state, item)
        state.sweep_for_advancements(locations=self.get_locations())

        if self.options.random_puzzles.value and self.options.include_shops.value and not (
                self.options.spirit_requirements.value == SpiritRequirements.option_Specific_And_Limit_Chapter_Logic and
                2 in self.excluded_spirits):
            dro_shop_locations = [self.multiworld.get_location(location, self.player)
                                  for location in self.random.sample([location for location in location_table.keys()
                                                                      if "DDO Outpost 1 Shop Item" in location], 3)]

            remaining_fill(self.multiworld, dro_shop_locations, self.dro_shop_puzzle_items)

        # place progression items that are also consumables in locations that are replenishable
        replenish_locations = [name for name, data in location_table.items() if data[0] in replenishing_itemlocations]
        replenish_items = list(filter(lambda item: item.name in progression_miscitems and
                                      item.classification == ic.progression, self.pre_fill_items))

        for item in replenish_items:
            self.pre_fill_items.remove(item)

        locations = list(filter(lambda location: location.name in replenish_locations
                                and location.progress_type != LocationProgressType.PRIORITY,
                                self.multiworld.get_unfilled_locations(player=self.player)))

        self.multiworld.random.shuffle(locations)
        fill_restrictive(self.multiworld, prefill_state(state), locations, replenish_items,
                         single_player_placement=True, lock=True, allow_excluded=False)

        # Place gear items in gear locations
        if self.options.gear_shuffle_mode.value == GearShuffleMode.option_Gear_Location_Shuffle:
            gear_items = list(filter(lambda item: pm_is_item_of_type(item, "GEAR"), self.pre_fill_items))
            # if starting jumpless, the first set of boots has to go elsewhere as there isn't a gear location for it
            # not to mention, no gear locations are reachable jumpless
            if self.options.starting_boots.value == StartingBoots.option_Jumpless:
                for item in gear_items:
                    if item.name == "Progressive Boots":
                        gear_items.remove(item)
                        break

            gear_locations = location_groups["Gear"]
            locations = list(filter(lambda location: location.name in gear_locations,
                                    self.multiworld.get_unfilled_locations(player=self.player)))
            if isinstance(locations, list):
                for item in gear_items:
                    self.pre_fill_items.remove(item)
                self.multiworld.random.shuffle(locations)
                fill_restrictive(self.multiworld, prefill_state(state), locations, gear_items,
                                 single_player_placement=True, lock=True, allow_excluded=False)

        # Place partner upgrade items in potential super block locations
        if self.options.partner_upgrades.value == PartnerUpgradeShuffle.option_Super_Block_Locations:
            upgrade_items = list(filter(lambda item: pm_is_item_of_type(item, "PARTNERUPGRADE"), self.pre_fill_items))
            super_block_locations = location_groups["SuperBlock"]

            # multi coin block locations are also candidates if they're shuffled
            if self.options.super_multi_blocks.value >= ShuffleSuperMultiBlocks.option_Shuffle:
                super_block_locations.extend(location_groups["MultiCoinBlock"])

            locations = list(filter(lambda location: location.name in super_block_locations,
                                    self.multiworld.get_unfilled_locations(player=self.player)))
            if isinstance(locations, list):
                for item in upgrade_items:
                    self.pre_fill_items.remove(item)
                self.multiworld.random.shuffle(locations)
                fill_restrictive(self.multiworld, prefill_state(state), locations, upgrade_items,
                                 single_player_placement=True, lock=True, allow_excluded=False)

        # Place coin bags in super or multi coin block locations
        if self.options.super_multi_blocks.value == ShuffleSuperMultiBlocks.option_Shuffle:
            coin_bag_items = list(filter(lambda item: item.name == "Coin Bag", self.pre_fill_items))
            multicoin_locations = location_groups["RandomBlock"]
            locations = list(filter(lambda location: location.name in multicoin_locations,
                                    self.multiworld.get_unfilled_locations(player=self.player)))
            if isinstance(locations, list):
                for item in coin_bag_items:
                    self.pre_fill_items.remove(item)
                fill_restrictive(self.multiworld, prefill_state(state), locations, coin_bag_items,
                                 single_player_placement=True, lock=True, allow_excluded=False)

        if self.options.partners.value == ShufflePartners.option_Partner_Locations:
            partner_items = list(filter(lambda item: pm_is_item_of_type(item, "PARTNER"), self.pre_fill_items))
            partner_locations = location_groups["Partner"]
            locations = list(filter(lambda location: location.name in partner_locations,
                                    self.multiworld.get_unfilled_locations(player=self.player)))
            if isinstance(locations, list):
                for item in partner_items:
                    self.pre_fill_items.remove(item)
                self.multiworld.random.shuffle(locations)
                fill_restrictive(self.multiworld, prefill_state(state), locations, partner_items,
                                 single_player_placement=True, lock=True, allow_excluded=False)

        # Place dungeon key items in their own dungeon
        if not self.options.keysanity.value:
            for dungeon in limited_by_item_areas:
                # get key items for this dungeon
                key_names = list(filter(lambda item: self.dungeon_restricted_items[item] == dungeon,
                                        self.dungeon_restricted_items.keys()))
                key_items = list(filter(lambda item: item.name in key_names,
                                        self.pre_fill_items))

                # get locations for this dungeon
                dungeon_locations = [name for name, data in location_table.items() if data[0][:3] == dungeon]

                # remove edge case location since it isn't actually in the dungeon
                if "KBF Fortress Exterior Chest On Ledge" in dungeon_locations:
                    dungeon_locations.remove("KBF Fortress Exterior Chest On Ledge")

                locations = list(filter(lambda location: location.name in dungeon_locations,
                                        self.multiworld.get_unfilled_locations(player=self.player)))
                if isinstance(locations, list):
                    for item in key_items:
                        self.pre_fill_items.remove(item)
                    self.multiworld.random.shuffle(locations)
                    fill_restrictive(self.multiworld, prefill_state(state), locations, key_items,
                                     single_player_placement=True, lock=True, allow_excluded=True)

        # Anything remaining in pre fill items is a consumable that got selected randomly to be kept local
        # LCL can really skew the item pool, so fill up the excluded locations to prevent generation errors
        if self.options.spirit_requirements.value == SpiritRequirements.option_Specific_And_Limit_Chapter_Logic:
            locations = list(filter(lambda location: location.progress_type == LocationProgressType.EXCLUDED,
                                    self.multiworld.get_unfilled_locations(player=self.player)))
            if len(locations) <= len(self.pre_fill_items):
                self.random.shuffle(self.pre_fill_items)
                items_for_excluded = []

                for _ in locations:
                    items_for_excluded.append(self.pre_fill_items.pop())

                fill_restrictive(self.multiworld, prefill_state(state), locations, items_for_excluded,
                                 single_player_placement=True, lock=True, allow_excluded=True)
                for loc in locations:
                    if loc.item:
                        loc.locked = True

        # Now throw the rest wherever
        locations = list(filter(lambda location: location.progress_type != LocationProgressType.PRIORITY,
                                self.multiworld.get_unfilled_locations(player=self.player)))
        self.multiworld.random.shuffle(locations)
        fill_restrictive(self.multiworld, prefill_state(state), locations, self.pre_fill_items,
                         single_player_placement=True, lock=True, allow_excluded=True)

        # Locations with unrandomized junk should be changed to events
        for loc in self.get_locations():
            if loc.address is not None and not loc.show_in_spoiler:
                loc.address = None

    def generate_output(self, output_directory: str) -> None:
        generate_output(self, output_directory)


    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.spoilerlog_puzzles:
            spoiler_handle.write(f"\n\nPuzzles ({self.multiworld.player_name[self.player]}):\n")
            for puzzle, solution in self.spoilerlog_puzzles.items():
                spoiler_handle.write(f"\n{puzzle}: {solution}")

    # handle star pieces from quizmo, triple star piece items
    def collect(self, state: CollectionState, item: PMItem) -> bool:
        if item.name == "3x Star Pieces":
            state.prog_items[self.player]["Star Piece"] += 3
        # Quizmo star pieces are events that can exist in multiple places, format "StarPiece_MAC_1"
        elif item.name.startswith("StarPiece_") and state.prog_items[self.player][item.name] == 1:
            state.prog_items[self.player]["Star Piece"] += 1
        return super().collect(state, item)

    def get_locations(self):
        return self.multiworld.get_locations(self.player)

    def get_location(self, location):
        return self.multiworld.get_location(location, self.player)

    def get_region(self, region_name):
        try:
            return self._regions_cache[region_name]
        except KeyError:
            ret = self.multiworld.get_region(region_name, self.player)
            self._regions_cache[region_name] = ret
            return ret

    # Specifically ensures that only real items are gotten, not any events.
    def get_state_with_complete_itempool(self):
        all_state = CollectionState(self.multiworld)
        for item in self.itempool + self.pre_fill_items:
            self.multiworld.worlds[item.player].collect(all_state, item)
        all_state.stale[self.player] = True

        return all_state

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "keysanity": self.options.keysanity.value,
            "shuffle_hidden_panels": self.options.shuffle_hidden_panels.value,
            "gear_shuffle_mode": self.options.gear_shuffle_mode.value,
            "trading_events": self.options.trading_events.value,
            "koot_favors": self.options.koot_favors.value,
            "koot_coins": self.options.koot_coins.value,
            "overworld_coins": self.options.overworld_coins.value,
            "foliage_coins": self.options.foliage_coins.value,
            "coin_blocks": self.options.coin_blocks.value,
            "include_shops": self.options.include_shops.value,
            "dojo": self.options.dojo.value,
            "partner_upgrades": self.options.partner_upgrades.value,
            "letter_rewards": self.options.letter_rewards.value,
            "super_multi_blocks": self.options.super_multi_blocks.value,
            "rowf_items": self.options.rowf_items.value,
            "merlow_items": self.options.merlow_items.value,
            "cheato_items": self.options.cheato_items.value,
            "partners": self.options.partners.value,
            "partners_always_usable": self.options.partners_always_usable.value,
            "start_with_goombario": self.options.start_with_goombario.value,
            "start_with_kooper": self.options.start_with_kooper.value,
            "start_with_bombette": self.options.start_with_bombette.value,
            "start_with_parakarry": self.options.start_with_parakarry.value,
            "start_with_bow": self.options.start_with_bow.value,
            "start_with_watt": self.options.start_with_watt.value,
            "start_with_sushie": self.options.start_with_sushie.value,
            "start_with_lakilester": self.options.start_with_lakilester.value,
            "enemy_difficulty": self.options.enemy_difficulty.value,
            "spirit_requirements": self.options.spirit_requirements.value,
            "starting_boots": self.options.starting_boots.value,
            "starting_hammer": self.options.starting_hammer.value,
            "starting_map": self.options.starting_map.value,
            "open_prologue": self.options.open_prologue.value,
            "open_mt_rugged": self.options.open_mt_rugged.value,
            "open_forest": self.options.open_forest.value,
            "open_toybox": self.options.open_toybox.value,
            "magical_seeds": self.options.magical_seeds.value,
            "open_whale": self.options.open_whale.value,
            "open_blue_house": self.options.open_blue_house.value,
            "ch7_bridge_visible": self.options.ch7_bridge_visible.value,
            "bowser_castle_mode": self.options.bowser_castle_mode.value,
            "shuffle_dungeon_entrances": self.options.shuffle_dungeon_entrances.value,
            "seed_goal": self.options.seed_goal.value,
            "shuffle_star_beam": self.options.shuffle_star_beam.value,
            "star_way_spirits": self.options.star_way_spirits.value,
            "star_beam_spirits": self.options.star_beam_spirits.value,
            "power_star_hunt": self.options.power_star_hunt.value,
            "star_way_power_stars": self.options.star_way_power_stars.value,
            "star_beam_power_stars": self.options.star_beam_power_stars.value,
            "total_power_stars": self.options.total_power_stars.value,
            "hidden_block_mode": self.options.hidden_block_mode.value,
            "cook_without_frying_pan": self.options.cook_without_frying_pan.value,
            "merlow_rewards_pricing": self.options.merlow_rewards_pricing.value,
            "required_spirits": self.required_spirits
        }

    def modify_multidata(self, multidata: dict):
        import base64
        # Replace connect name
        multidata['connect_names'][base64.b64encode(self.auth).decode("ascii")] = multidata['connect_names'][
            self.multiworld.player_name[self.player]]

    def get_filler_item_name(self) -> str:
        if self.options.consumable_item_pool.value == ConsumableItemPool.option_Mystery_Only:
            return "Mystery"
        else:
            return "Super Shroom"
