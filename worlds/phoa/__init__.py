import time

from BaseClasses import Tutorial, Item
from BaseClasses import ItemClassification as IC
from worlds.AutoWorld import WebWorld, World
from .Options import PhoaOptions, phoa_option_groups
from .Locations import PhoaLocation, get_location_data
from .Items import PhoaItem, item_table, PhoaItemData, get_item_pool
from .Regions import create_regions_and_locations


class PhoaWebWorld(WebWorld):
    tutorials = [Tutorial(
        tutorial_name="Start Guide",
        description="A guide to start playing Phoenotopia: Awakening in MultiworldGG",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["Lenamphy"]
    )]
    option_groups = phoa_option_groups


class PhoaWorld(World):
    """
    Phoenotopia: Awakening is a 2020 action-adventure game, remaking the original flash game, a 2D side-scrolling action adventure in a post-apcalyptic fictional world.
    """
    game = "Phoenotopia: Awakening"
    web = PhoaWebWorld()
    options: PhoaOptions
    options_dataclass = PhoaOptions
    location_name_to_id = {name: data.address for name, data in get_location_data(-1, None).items()}
    item_name_to_id = {name: data.code for name, data in item_table.items()}

    progressive_item_classifications_overrides: list[str] = []

    def generate_early(self) -> None:
        self._determine_item_classifications_overrides()

    def create_item(self, name: str) -> PhoaItem:
        item_classification = IC.progression \
            if name in self.progressive_item_classifications_overrides \
            else item_table[name].type
        return PhoaItem(name, item_classification, item_table[name].code, self.player)

    def create_items(self):
        self.create_and_assign_event_items()

        item_pool_strings, precollected_items = get_item_pool(self, get_location_data(self.player, self.options))

        for item in precollected_items:
            self.multiworld.push_precollected(self.create_item(item))

        item_pool: list[PhoaItem] = []

        for item_name in item_pool_strings:
            item_pool.append(self.create_item(item_name))

        self.multiworld.itempool += item_pool
        # for itemyea in self.multiworld.itempool:
        #     print(itemyea.name, itemyea.classification)
        # time.sleep(1200)

    def create_regions(self):
        create_regions_and_locations(self.multiworld, self.player, self.options)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            "Strange Urn", self.player
        )

    def get_filler_item_name(self) -> str:
        return '20 Rin'

    def create_and_assign_event_items(self):
        for location in self.multiworld.get_locations(self.player):
            if location.address is None:
                location.place_locked_item(
                    Item(location.name, IC.progression, None, self.player))

    def fill_slot_data(self):
        return self.options.get_slot_data_dict()

    def _determine_item_classifications_overrides(self) -> None:
        options = self.options

        if not options.start_with_wooden_bat:
            self.progressive_item_classifications_overrides.append("Progressive Bat")
        if options.enable_fishing_spots:
            self.progressive_item_classifications_overrides.append("Fishing Rod")
            self.progressive_item_classifications_overrides.append("Serpent Rod")
            self.progressive_item_classifications_overrides.append("Progressive Fishing Rod")
