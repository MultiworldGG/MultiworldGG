from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial
from .Regions import create_regions
from .Locations import create_locations, location_table
from BaseClasses import Item
from .Items import create_items, item_table, item_data_by_name
from .Options import ChainedEchoesOptions, SLOT_DATA_OPTION_NAMES

class ChainedEchoesWeb(WebWorld):
    rich_text_options_doc = True
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Chained Echoes on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["SergioAlonso"]
    )

    tutorials = [setup_en]

class ChainedEchoesWorld(World):
    """
    Chained Echoes world integration for MultiworldGG.
    Regions and locations are created in `create_regions` (including a call to `create_locations`).
    Items are created in `create_items`.
    """
    game = "Chained Echoes"
    author: str = "SergioAlonso"
    location_name_to_id = location_table
    item_name_to_id = item_table
    topology_present = True
    web = ChainedEchoesWeb()
    options_dataclass = ChainedEchoesOptions
    options: ChainedEchoesOptions

    def generate_early(self):
        """
        Resolve the server-provided randomizer seed during AP generation.
        A YAML value of -1 means AP should generate the seed once and send it in slot data.
        """
        self.generated_randomizer_seed = int(self.options.randomizer_seed.value)
        if self.generated_randomizer_seed == -1:
            self.generated_randomizer_seed = self.random.randint(0, 2147483647)

    def create_regions(self):
        """
        Creates regions and locations for the world.
        `create_regions` internally calls `create_locations`.
        """
        create_regions(self)
        create_locations(self)

    def create_item(self, name: str) -> Item:
        """
        Create a single item by name using the parsed item metadata.
        """
        item_data = item_data_by_name[name]
        return Item(name, item_data.classification, item_data.id, self.player)

    def create_items(self):
        """
        Populates the item pool with items for the world.
        """
        create_items(self)

    def fill_slot_data(self):
        """
        Sends AP-generated randomizer options and seed to the Chained Echoes client.
        """
        slot_data = {client_name: int(getattr(self.options, option_name).value)
                     for client_name, option_name in SLOT_DATA_OPTION_NAMES.items()}

        if not hasattr(self, "generated_randomizer_seed"):
            self.generate_early()
        slot_data["RandomizerSeed"] = self.generated_randomizer_seed

        return slot_data

