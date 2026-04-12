import itertools
import logging
from pathlib import Path
from typing import Any, ClassVar, cast

import settings
from BaseClasses import CollectionState, Item, Location, MultiWorld, Tutorial
from Fill import fill_restrictive
from Options import Option, OptionError
from worlds.AutoWorld import WebWorld, World

from .client import WL4Client as WL4Client  # Suppress unused import warning
from .data import Passage, data_path
from .items import (
    KeyzerItemData,
    WL4EventItem,
    WL4Item,
    ability_table,
    cd_table,
    get_jewel_pieces_by_passage,
    golden_treasure_table,
    item_name_to_id,
    jewel_piece_table,
    keyzer_table,
)
from .locations import WL4Location, get_level_locations, location_name_to_id
from .options import Goal, OpenDoors, WL4Options, wl4_option_groups
from .region_data import passage_levels
from .regions import WL4Level, connect_regions, create_regions
from .rom import MD5_JP, MD5_US_EU, WL4ProcedurePatch, write_tokens


class WL4Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Wario Land 4 ROM"""
        description = "Wario Land 4 ROM File"
        copy_to = "Wario Land 4.gba"
        md5s = [MD5_US_EU, MD5_JP]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class WL4Web(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Wario Land 4 randomizer connected to a MultiworldGG Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["lil David", "Fairweather-Furry"]
    )

    theme = "jungle"
    tutorials = [setup_en]
    option_groups = wl4_option_groups


class WL4World(World):
    """
    A golden pyramid has been discovered deep in the jungle, and Wario has set
    out to rob it. But when he enters, he finds the Golden Diva's curse has
    taken away his moves! To escape with his life and more importantly, the
    treasure, Wario must find his abilities to defeat the passage bosses and
    the Golden Diva.
    """

    game: str = "Wario Land 4"
    options_dataclass = WL4Options
    options: WL4Options
    settings: ClassVar[WL4Settings]

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    required_client_version = (0, 6, 0)
    origin_region_name = "Pyramid"

    item_name_groups = {
        "Entry Jewel Pieces": set(get_jewel_pieces_by_passage(Passage.ENTRY)),
        "Emerald Pieces": set(get_jewel_pieces_by_passage(Passage.EMERALD)),
        "Ruby Pieces": set(get_jewel_pieces_by_passage(Passage.RUBY)),
        "Topaz Pieces": set(get_jewel_pieces_by_passage(Passage.TOPAZ)),
        "Sapphire Pieces": set(get_jewel_pieces_by_passage(Passage.SAPPHIRE)),
        "Golden Jewel Pieces": set(get_jewel_pieces_by_passage(Passage.GOLDEN)),
        "CDs": set(cd_table.keys()),
        "Keyzers": set(keyzer_table.keys()),
        "Abilities": set(ability_table.keys()),
        "Golden Treasure": set(golden_treasure_table.keys()),
        "Traps": {"Wario Form Trap", "Lightning Trap"},
        "Junk": {"Heart", "Minigame Medal"},
        "Prizes": {"Full Health Item", "Diamond"},

        # Aliases
        "Ground Pound": {"Progressive Ground Pound"},
        "Grab": {"Progressive Grab"},
        "Smash Attack": {"Progressive Ground Pound"},
        "Progressive Smash Attack": {"Progressive Ground Pound"},
        "Enemy Jump": {"Stomp Jump"},
        "Minigame Coin": {"Minigame Medal"},
    }

    location_name_groups = {
        "Hall of Hieroglyphs": set(get_level_locations(Passage.ENTRY, 0)),
        "Palm Tree Paradise": set(get_level_locations(Passage.EMERALD, 0)),
        "Wildflower Fields": set(get_level_locations(Passage.EMERALD, 1)),
        "Mystic Lake": set(get_level_locations(Passage.EMERALD, 2)),
        "Monsoon Jungle": set(get_level_locations(Passage.EMERALD, 3)),
        "Cractus Treasures": set(get_level_locations(Passage.EMERALD, 4)),
        "The Curious Factory": set(get_level_locations(Passage.RUBY, 0)),
        "The Toxic Landfill": set(get_level_locations(Passage.RUBY, 1)),
        "40 Below Fridge": set(get_level_locations(Passage.RUBY, 2)),
        "Pinball Zone": set(get_level_locations(Passage.RUBY, 3)),
        "Cuckoo Condor Treasures": set(get_level_locations(Passage.RUBY, 4)),
        "Toy Block Tower": set(get_level_locations(Passage.TOPAZ, 0)),
        "The Big Board": set(get_level_locations(Passage.TOPAZ, 1)),
        "Doodle Woods": set(get_level_locations(Passage.TOPAZ, 2)),
        "Domino Row": set(get_level_locations(Passage.TOPAZ, 3)),
        "Aerodent Treasures": set(get_level_locations(Passage.TOPAZ, 4)),
        "Crescent Moon Village": set(get_level_locations(Passage.SAPPHIRE, 0)),
        "Arabian Night": set(get_level_locations(Passage.SAPPHIRE, 1)),
        "Fiery Cavern": set(get_level_locations(Passage.SAPPHIRE, 2)),
        "Hotel Horror": set(get_level_locations(Passage.SAPPHIRE, 3)),
        "Catbat Treasures": set(get_level_locations(Passage.SAPPHIRE, 4)),
        "Golden Passage": set(get_level_locations(Passage.GOLDEN, 0)),
    }

    web = WL4Web()

    PRIZES = ("Full Health Item", "Diamond")
    JUNK = ("Heart", "Minigame Medal")
    TRAPS = ("Wario Form Trap", "Lightning Trap")

    filler_item_weights: tuple[int, int, int] | None

    def __init__(self, *args, **kwargs):
        super(WL4World, self).__init__(*args, **kwargs)
        self.filler_item_weights = None

    levels: dict[str, WL4Level]

    def generate_early(self):
        if self.is_universal_tracker():
            self.set_options_from_slot_data()

        if self.options.goal in (Goal.option_local_golden_treasure_hunt, Goal.option_local_golden_diva_treasure_hunt):
            self.options.local_items.value.update(self.item_name_groups["Golden Treasure"])
        if self.options.required_jewels > self.options.pool_jewels:
            logging.warning(f"{self.player_name} has Required Jewels set to "
                            f"{self.options.required_jewels.value} but Pool Jewels set to "
                            f"{self.options.pool_jewels.value}. Setting Pool Jewels to "
                            f"{self.options.required_jewels.value}")
            self.options.pool_jewels.value = self.options.required_jewels.value
        if self.options.required_jewels >= 1 and self.options.golden_jewels == 0:
            logging.warning(f"{self.player_name} has Required Jewels set to at least 1 but "
                            f"Golden Jewels set to {self.options.golden_jewels}. Setting Golden "
                            "Jewels to 1.")
            self.options.golden_jewels.value = 1

        # TODO: Make this more tolerant when start inventory from pool is involved?
        abilities = 8
        full_health_items = (9, 7, 6)[self.options.difficulty.value]
        rando_jewel_pieces = 4 * (min(self.options.pool_jewels.value, 1) +  # Entry
                                  4 * self.options.pool_jewels.value +  # Emerald, Ruby, Topaz, Sapphire
                                  self.options.golden_jewels.value)  # Golden Pyramid
        vanilla_jewel_pieces = 4 * 18
        if (rando_jewel_pieces + abilities - vanilla_jewel_pieces > full_health_items and
            not self.options.diamond_shuffle.value):
            raise OptionError(f"Not enough locations to place abilities for {self.player_name}. "
                              'Set the "Pool Jewels" or "Golden Jewels" option to a lower value and try again.')

        self.filler_item_weights = self.options.prize_weight.value, self.options.junk_weight.value, self.options.trap_weight.value

        self.levels = {}

    def create_regions(self):
        import logging
        logging.info(self.options)
        create_regions(self)
        connect_regions(self)

    def create_items(self):
        difficulty = self.options.difficulty.value
        treasure_hunt = self.options.goal.needs_treasure_hunt()
        diamond_shuffle = self.options.diamond_shuffle.value

        vanilla_jewel_pieces = 18 * 4
        cds = 16
        full_health_items = (9, 7, 6)[difficulty]
        treasures = 12 * treasure_hunt
        diamonds = diamond_shuffle * (109, 71, 68)[difficulty]
        total_required_locations = vanilla_jewel_pieces + cds + full_health_items + treasures + diamonds

        itempool = []

        required_jewels = self.options.required_jewels.value
        pool_jewels = self.options.pool_jewels.value
        for name, item in jewel_piece_table.items():
            force_non_progression = required_jewels == 0
            if item.passage == Passage.ENTRY:
                copies = min(pool_jewels, 1)
            elif item.passage == Passage.GOLDEN:
                copies = self.options.golden_jewels.value
                if self.options.goal.is_treasure_hunt():
                    force_non_progression = True
            else:
                copies = pool_jewels

            itempool += [self.create_item(name, force_non_progression) for _ in range(copies)]

        itempool += [self.create_item(name) for name in cd_table]

        for name in ability_table:
            itempool.append(self.create_item(name))
            if name.startswith("Progressive"):
                itempool.append(self.create_item(name))

        # Remove diamonds or full health items to make space for abilities
        abilities = 8
        total_rando_jewel_pieces = 4 * (min(self.options.pool_jewels.value, 1) +  # Entry
                                        4 * self.options.pool_jewels.value +  # Emerald, Ruby, Topaz, Sapphire
                                        self.options.golden_jewels.value)  # Golden Pyramid
        extra_items = total_rando_jewel_pieces + abilities - vanilla_jewel_pieces
        if extra_items > 0:
            if diamond_shuffle:
                diamonds -= extra_items
            else:
                full_health_items -= extra_items
        assert diamonds >= 0 and full_health_items >= 0

        itempool += [self.create_item("Full Health Item") for _ in range(full_health_items)]

        if treasure_hunt:
            itempool += [self.create_item(name) for name in golden_treasure_table]

        if diamond_shuffle:
            itempool += [self.create_item("Diamond") for _ in range(diamonds)]

        keyzers_in_levels: dict[str, KeyzerItemData]
        starting_keyzers: list[str]
        match self.options.open_doors.value:
            case OpenDoors.option_off:
                keyzers_in_levels = dict(keyzer_table)
                starting_keyzers = []
            case OpenDoors.option_closed_diva:
                gp_keyzer = "Keyzer (Golden Pyramid Boss)"
                keyzers_in_levels = {gp_keyzer: keyzer_table[gp_keyzer]}
                starting_keyzers = [keyzer for keyzer in keyzer_table.keys() if keyzer != gp_keyzer]
            case OpenDoors.option_open:
                keyzers_in_levels = {}
                starting_keyzers = list(keyzer_table.keys())
        assert keyzers_in_levels or starting_keyzers  # This assertion was written in blood
        for name, data in keyzers_in_levels.items():
            self.levels[passage_levels[data.passage][data.level]].items.append(cast(WL4Item, self.create_item(name)))
        for name in starting_keyzers:
            self.multiworld.push_precollected(self.create_item(name))
        if self.options.keyzer_shuffle.value:
            total_required_locations += len(starting_keyzers)

        junk_count = total_required_locations - len(itempool)
        itempool += [self.create_item(self.get_filler_item_name()) for _ in range(junk_count)]

        self.multiworld.itempool += itempool

    def get_pre_fill_items(self):
        return list(itertools.chain.from_iterable(level.items for level in self.levels.values()))

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld):
        keyzers = set()
        items: list[WL4Item] = []
        locations: list[WL4Location] = []

        for world in multiworld.get_game_worlds(cls.game):
            player = world.player
            if player in multiworld.groups:
                continue
            assert type(world) is WL4World

            if world.options.keyzer_shuffle.value:
                for level in world.levels.values():
                    keyzers.update((player, item.name) for item in level.items if type(item.data) is KeyzerItemData)
                    items.extend(item for item in level.items if type(item.data) is KeyzerItemData)
                    locations.extend(location for location in level.locations if not location.item)

        if items:
            def add_level_item_rule(location: WL4Location):
                old_rule = location.item_rule
                location.item_rule = lambda item: (
                    old_rule(item)
                    and (
                        (item.player, item.name) not in keyzers
                        or (
                            type(item) is WL4Item
                            and type(item.data) is KeyzerItemData
                            and (item.data.passage, item.data.level) == (location.passage, location.level)
                        )
                    )
                )

            for location in locations:
                add_level_item_rule(location)

            multiworld.random.shuffle(locations)

            shuffled_player_ids = {item.player for item in items}
            all_state = CollectionState(multiworld)
            for item in multiworld.itempool:
                multiworld.worlds[item.player].collect(all_state, item)
            prefill_items: list[Item] = []
            for player in shuffled_player_ids:
                prefill_items.extend(multiworld.worlds[player].get_pre_fill_items())
            for item in items:
                prefill_items.remove(item)
            for item in prefill_items:
                multiworld.worlds[item.player].collect(all_state, item)
            all_state.sweep_for_advancements()

            for player in shuffled_player_ids:
                if all_state.has("Escape the Pyramid", player):
                    all_state.remove(WL4EventItem("Escape the Pyramid", player))

            for player in shuffled_player_ids:
                local_items = [cast(Item, item) for item in items if item.player == player]
                local_locations = [cast(Location, loc) for loc in locations if loc.player == player]
                multiworld.random.shuffle(local_locations)
                fill_restrictive(
                    multiworld,
                    all_state,
                    local_locations,
                    local_items,
                    lock=True,
                    single_player_placement=True,
                    allow_excluded=True,
                    allow_partial=False,
                    name="WL4 Keyzers",
                )

    def generate_output(self, output_directory: str):
        output_path = Path(output_directory)

        patch = WL4ProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("basepatch.bsdiff", data_path("basepatch.bsdiff"))
        write_tokens(self, patch)
        patch.procedure.append((
            "shuffle_music_and_wario_voice",
            [self.options.music_shuffle.value, self.options.wario_voice_shuffle.value]
        ))

        output_filename = self.multiworld.get_out_file_name_base(self.player)
        patch.write(str((output_path / output_filename).with_suffix(patch.patch_file_ending)))

    def fill_slot_data(self) -> dict[str, Any]:
        return self.options.as_dict(
            "goal",
            "golden_treasure_count",
            "difficulty",
            "logic",
            "required_jewels",
            "open_doors",
            "keyzer_shuffle",
            "portal",
            "diamond_shuffle",
            "death_link",
        )

    def get_filler_item_name(self) -> str:
        if self.filler_item_weights is None:
            self.filler_item_weights = self.options.prize_weight.value, self.options.junk_weight.value, self.options.trap_weight.value
        pool = self.random.choices((self.PRIZES, self.JUNK, self.TRAPS), self.filler_item_weights)[0]
        return self.random.choice(pool)

    def create_item(self, name: str, force_non_progression=False):
        if name == self.glitches_item_name:
            return WL4EventItem(name, self.player)
        return WL4Item(name, self.player, force_non_progression)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = (
            lambda state: state.has("Escape the Pyramid", self.player))

    # UT integration

    ut_can_gen_without_yaml = True
    glitches_item_name = "SEQUENCE BREAKS"

    def is_universal_tracker(self):
        return hasattr(self.multiworld, "generation_is_fake")

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]):
        # Trigger a re-gen
        return slot_data

    def set_options_from_slot_data(self):
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if not re_gen_passthrough or self.game not in re_gen_passthrough:
            return
        slot_data: dict[str, Any] = re_gen_passthrough[self.game]

        def set_option(option_name: str):
            option: Option | None = getattr(self.options, option_name, None)
            value = slot_data.get(option_name)
            if option is not None and value is not None:
                setattr(self.options, option_name, option.from_any(value))

        set_option("goal")
        set_option("golden_treasure_count")
        set_option("difficulty")
        set_option("logic")
        set_option("required_jewels")
        set_option("open_doors")
        set_option("keyzer_shuffle")
        set_option("portal")
        set_option("diamond_shuffle")
