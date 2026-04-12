import os
import typing

import settings
from BaseClasses import Item, MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld

from . import Items, Locations, Regions, Rom, Rules
from .Client import MarioKart64Client  # Import to register client with BizHawkClient
from .Locations import MK64Location
from .Options import MK64Options, GameMode, Opt, ShuffleDriftAbilities


class MK64Web(WebWorld):
    theme = "grass"

    setup = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the MultiworldGG Mario Kart 64 software on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Edsploration"]
    )
    tutorials = [setup]


class MK64Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the MK64 ROM"""
        description = "Mario Kart 64 ROM File"
        copy_to = "Mario Kart 64 (U) [!].z64"
        md5s = [Rom.MK64DeltaPatch.hash]
        # "e19398a0fd1cc12df64fca7fbcaa82cc"  # byte-swapped ROM hash

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MK64World(World):
    """
    Mario Kart 64 is the original 3D kart racing game. Collect and fire off items,
    maneuver around hazards, execute drifts and mini-turbos, risk shortcuts but
    stay on the track, and race to victory in each course and cup.
    """
    game = "Mario Kart 64"
    author: str = "Edsploration"
    web = MK64Web()
    topology_present = False

    options: MK64Options
    options_dataclass = MK64Options
    settings: typing.ClassVar[MK64Settings]

    item_name_to_id = Items.item_name_to_id
    location_name_to_id = Locations.location_name_to_id
    item_name_groups = Items.item_name_groups

    opt: Opt
    num_filler_items: int
    shuffle_clusters: list[bool]
    filler_spots: list[bool]
    victory_location: MK64Location
    course_order: list[int]
    starting_karts: list[str]

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = Rom.get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self) -> None:
        self.opt = opt = Opt(self)

        # Count items without a paired location and vice versa, based on player options
        # hardcoded for speed, and because duplicating the the world generation logic here would be excessive.
        # Tests may be needed to keep this from being fragile, or it may need to be refactored to later into generation.
        num_unpaired_items = ((not opt.feather and not opt.two_player and 21)  # 20 to 155
                              + (opt.feather and not opt.two_player and 22)
                              + (not opt.feather and opt.two_player and 34)
                              + (opt.feather and opt.two_player and 36)
                              + (3 if opt.mode == GameMode.option_cups else opt.locked_courses)
                              + (0 if opt.drift == ShuffleDriftAbilities.option_off else
                                 (opt.drift == ShuffleDriftAbilities.option_on and 16) or
                                 (opt.drift == ShuffleDriftAbilities.option_plentiful and 24) or 8)
                              + (opt.traction and 16)
                              + (opt.starting_items and 8)
                              + (opt.railings and 13)
                              + (opt.fences and 4)
                              + (opt.box_respawning and 1)
                              + opt.min_filler)
        num_unpaired_locations = ((67 if opt.mode == GameMode.option_cups else 47)  # 47 to 88
                                  + (opt.hazards and 11)
                                  + (opt.secrets and 10))

        num_needed_extra_locs = max(num_unpaired_items - num_unpaired_locations, 0)  # 0 to 108
        num_needed_extra_items = max(num_unpaired_locations - num_unpaired_items, 0)
        self.num_filler_items = opt.min_filler + num_needed_extra_items  # 0 to 65
        self.shuffle_clusters = ([True] * opt.clusters + [False] * (72 - opt.clusters))
        self.filler_spots = ([True] * num_needed_extra_locs + [False] * (338 - num_needed_extra_locs - opt.clusters))
        # Uncomment to print at generation time extra locations/items
        # if num_needed_extra_locs:
        #     print(f"{num_needed_extra_locs} extra Mario Kart 64 locations will be made"
        #           f" for {self.multiworld.get_player_name(self.player)} to match their number of items.")
        # elif num_needed_extra_items:
        #     print(f"{num_needed_extra_items} extra Mario Kart 64 filler items will be made"
        #           f" for {self.multiworld.get_player_name(self.player)} to match their number of locations.")

    def create_regions(self) -> None:
        Regions.create_regions_locations_connections(self)

    def create_item(self, name: str) -> Item:
        return Items.create_item(name, self.player)

    def create_items(self) -> None:
        Items.create_items(self)

    def set_rules(self) -> None:
        Rules.create_rules(self)

    def generate_output(self, output_directory: str) -> None:
        Rom.generate_rom_patch(self, output_directory)
        # Uncomment to export PUML location visualization
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "mk64.puml")

    def modify_multidata(self, multidata: dict) -> None:
        player_name = self.multiworld.player_name[self.player]
        slot_name = player_name + "_" + self.multiworld.seed_name[:20]
        multidata["connect_names"][slot_name] = multidata["connect_names"][player_name]
