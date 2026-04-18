import itertools
import os
import typing
from typing import TextIO

import settings
from BaseClasses import Item, Tutorial, ItemClassification
from Options import Accessibility
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, SuffixIdentifier, icon_paths
from .Events import create_events
from .Items import item_table, BfBBItem
from .Locations import location_table, BfBBLocation, patrick_location_table
from .Options import BfBBOptions, RandomizeGateCost
from .Regions import create_regions
from .Rom import BfBBContainer
from .Rules import set_rules
from .Settings import BattleForBikiniBottomSettings
from .Tracker import tracker_world_overview, tracker_world_detailed
from .constants import ItemNames, ConnectionNames, game_name


def run_client(*args):
    from worlds.LauncherComponents import launch
    from worlds.bfbb.BfBBClient import launch as bfbb_launch  # lazy import
    launch(bfbb_launch, f"{game_name} Client", args=args)

icon_paths["bfbb_icon"] = f"ap:{__name__}/icon.png"
components.append(Component(f"{game_name} Client", func=run_client, component_type=Type.CLIENT,
                            file_identifier=SuffixIdentifier('.apbfbb'), game_name=game_name, supports_uri=True, icon="bfbb_icon"))


class BattleForBikiniBottomWeb(WebWorld):
    display_name: str = "Spongebob Squarepants: Battle for Bikini Bottom"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the SpongeBob SquarePants: Battle for Bikini Bottom integration for MultiworldGG multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Cyb3R"]
    )]
    rich_text_options_doc = True
    theme = "ocean"


default_gate_costs: typing.Dict[str, int] = {
    # ConnectionNames.pineapple_hub1: 1,
    ConnectionNames.hub1_bb01: 5,
    ConnectionNames.hub1_gl01: 10,
    ConnectionNames.hub1_b1: 15,
    ConnectionNames.hub2_rb01: 25,
    ConnectionNames.hub2_sm01: 30,
    ConnectionNames.hub2_b2: 40,
    ConnectionNames.hub3_kf01: 50,
    ConnectionNames.hub3_gy01: 60,
    ConnectionNames.cb_b3: 75,
}


class BattleForBikiniBottom(World):
    """
    SpongeBob SquarePants: Battle for Bikini Bottom is a 2003 platform game based on the Nickelodeon animated series SpongeBob SquarePants, involving 
    gathering collectibles in various areas around Bikini Bottom by crossing platforms and avoiding environmental hazards like spikes and flames.
    """
    game = game_name
    options_dataclass = BfBBOptions
    options: BfBBOptions
    settings: typing.ClassVar[BattleForBikiniBottomSettings]
    settings_key = "bfbb_options"
    topology_present = False

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = location_table

    web = BattleForBikiniBottomWeb()
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.gate_costs: typing.Dict[str, int] = default_gate_costs.copy()
        self.level_order: typing.List[str] = [ConnectionNames.hub1_bb01, ConnectionNames.hub1_gl01, ConnectionNames.hub1_b1,
                                              ConnectionNames.hub2_rb01, ConnectionNames.hub2_sm01, ConnectionNames.hub2_b2,
                                              ConnectionNames.hub3_kf01, ConnectionNames.hub3_gy01, ConnectionNames.cb_b3]
        self.spat_counter: int = 0
        self.sock_counter: int = 0
        self.required_socks: int = 80
        self.required_spats: int = 75
        tracker_variant = settings.get_settings().bfbb_options.tracker_variant or 'detailed'
        BattleForBikiniBottom.tracker_world = tracker_world_overview if tracker_variant == 'overview' else tracker_world_detailed

    def generate_early(self) -> None:
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                self.apply_options_from_slot_data(self.multiworld.re_gen_passthrough[self.game])
                return

        if self.options.required_spatulas.value > self.options.available_spatulas.value:
            self.options.required_spatulas.value = self.options.available_spatulas.value
        if self.options.randomize_gate_cost.value > RandomizeGateCost.option_off:
            self.roll_level_order()
            self.set_gate_costs()
        self.gate_costs[ConnectionNames.cb_b3] = self.options.required_spatulas.value
        self.required_socks = self.get_required_socks()
        self.required_spats = max(self.gate_costs.values())

    def get_required_socks(self) -> int:
        socks = 80
        for pat_loc in sorted(patrick_location_table, key=patrick_location_table.get, reverse=True):
            if pat_loc in self.options.exclude_locations:
                socks -= 10
            else:
                break
        return socks

    def roll_level_order(self):
        level_left = [ConnectionNames.hub1_bb01, ConnectionNames.hub1_gl01, ConnectionNames.hub2_rb01,
                      ConnectionNames.hub2_sm01, ConnectionNames.hub3_kf01, ConnectionNames.hub3_gy01]
        counts = [4, 4, 2, 2, 1, 1]
        cnt = len(level_left)
        self.level_order = []
        for i in range(0, cnt):
            choices = [*range(0, len(level_left))]
            weighted_choices = list(itertools.chain.from_iterable([[choice] * count for choice, count in zip(choices, counts)]))
            idx = self.random.choice(weighted_choices)
            level = level_left[idx]
            if level in [ConnectionNames.hub2_rb01, ConnectionNames.hub2_sm01, ConnectionNames.hub3_kf01,
                         ConnectionNames.hub3_gy01] and ConnectionNames.hub1_b1 not in self.level_order:
                self.level_order.append(ConnectionNames.hub1_b1)
            if level in [ConnectionNames.hub3_kf01, ConnectionNames.hub3_gy01] and ConnectionNames.hub2_b2 not in self.level_order:
                self.level_order.append(ConnectionNames.hub2_b2)
            self.level_order.append(level)
            level_left.remove(level)
            counts.remove(counts[idx])

    def set_gate_costs(self):
        last_level = None
        min_incs = [0, 3, 5]
        last_cost = 1
        level_inc_min = min_incs[self.options.randomize_gate_cost.value - 1]
        level_inc_max = 8
        if self.options.include_socks.value:
            level_inc_max += 6
        if self.options.include_level_items.value:
            level_inc_max += 3
        if self.options.include_purple_so.value:
            level_inc_max += 1
        if self.options.randomize_gate_cost.value == 3:
            level_inc_max = round(level_inc_max * 1.35)
        elif self.options.randomize_gate_cost.value == 1:
            level_inc_max = round(level_inc_max * 0.75)
        for v in self.level_order:
            # set max increment after boss to 1/2
            if last_level is not None and last_level in [ConnectionNames.hub1_b1, ConnectionNames.hub2_b2]:
                level_inc_max = 2 if self.options.include_skills else 1
            level_inc_min = min(level_inc_min, level_inc_max)
            cost = min(self.random.randint(level_inc_min, level_inc_max) + last_cost, self.options.required_spatulas.value - 1)
            assert cost > 0, f"{v} gate cost too low"
            self.gate_costs[v] = cost
            last_level = v
            last_cost = cost

    def get_filler_item_name(self) -> str:
        return ItemNames.so_100

    def get_items(self):
        filler_items = [ItemNames.so_100, ItemNames.so_250]
        filler_weights = [1, 2]
        if self.options.include_purple_so.value == 0:
            filler_items += [ItemNames.so_500, ItemNames.so_750, ItemNames.so_1000]
            filler_weights += [5, 3, 2]
        # Generate item pool
        itempool = [ItemNames.spat] * self.options.available_spatulas.value
        if 100 - self.options.available_spatulas.value > 0:
            itempool += self.random.choices(filler_items, weights=filler_weights, k=100 - self.options.available_spatulas.value)
        if self.options.include_socks.value:
            itempool += [ItemNames.sock] * 80
        if self.options.include_skills.value:
            itempool += [ItemNames.bubble_bowl, ItemNames.cruise_bubble]
        if self.options.include_golden_underwear.value:
            itempool += [ItemNames.golden_underwear] * 3
        if self.options.include_level_items.value:
            itempool += [ItemNames.lvl_itm_jf]
            itempool += [ItemNames.lvl_itm_bb] * 11
            itempool += [ItemNames.lvl_itm_gl] * 5
            itempool += [ItemNames.lvl_itm_rb] * 6
            itempool += [ItemNames.lvl_itm_bc] * 4
            itempool += [ItemNames.lvl_itm_sm] * 8
            itempool += [ItemNames.lvl_itm_kf1] * 6
            itempool += [ItemNames.lvl_itm_kf2] * 6
            itempool += [ItemNames.lvl_itm_gy] * 4
        if self.options.include_purple_so.value:
            so_items = [ItemNames.so_100, ItemNames.so_250, ItemNames.so_500, ItemNames.so_750, ItemNames.so_1000]
            so_weights = [1, 2, 5, 3, 2]
            itempool += self.random.choices(so_items, weights=so_weights, k=38)

        # Convert itempool into real items
        itempool = list(map(lambda name: self.create_item(name), itempool))
        return itempool

    def create_items(self):
        self.multiworld.itempool += self.get_items()

    def set_rules(self):
        create_events(self.multiworld, self.player)
        set_rules(self.multiworld, self.options, self.player, self.gate_costs)

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

    def fill_slot_data(self):
        return {
            "version": self.world_version.as_simple_string(), #TODO: add version check/warning to patch/client
            "death_link": self.options.death_link.value,
            "ring_link": self.options.ring_link.value,
            "shiny_object_to_ring_ratio": self.options.shiny_object_to_ring_ratio.value,
            "include_socks": self.options.include_socks.value,
            "include_skills": self.options.include_skills.value,
            "include_golden_underwear": self.options.include_golden_underwear.value,
            "include_level_items": self.options.include_level_items.value,
            "include_purple_so": self.options.include_purple_so.value,
            "gate_costs": self.gate_costs
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict):
        return slot_data

    def apply_options_from_slot_data(self, slot_data: dict):
        for k, v in slot_data.items():
            if k == "gate_costs":
                self.gate_costs = v
                continue
            if hasattr(self.options, k):
                option = getattr(self.options, k)
                if option.value != v:
                    option.value = v

    def create_item(self, name: str, ) -> Item:
        item_data = item_table[name]
        classification = item_data.classification
        if name == ItemNames.spat:
            self.spat_counter += 1
            if self.spat_counter > self.required_spats:
                classification |= ItemClassification.skip_balancing
        if name == ItemNames.sock:
            self.sock_counter += 1
            if self.sock_counter > 40:
                classification |= ItemClassification.skip_balancing
            if self.options.accessibility.value == Accessibility.option_minimal and self.sock_counter > self.required_socks:
                classification = ItemClassification.useful
        if name in [ItemNames.so_500, ItemNames.so_750, ItemNames.so_1000] and self.options.include_purple_so == 0:
            classification = ItemClassification.useful
        item = BfBBItem(name, classification, item_data.id, self.player)

        return item

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.options.randomize_gate_cost.value > 0:
            spoiler_handle.write(f"\n\nGate Costs ({self.multiworld.get_player_name(self.player)}):\n\n")
            for k, v in self.gate_costs.items():
                spoiler_handle.write(f"{k}: {v}\n")

    def generate_output(self, output_directory: str) -> None:
        apbfbb = BfBBContainer(
            path=os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}{BfBBContainer.patch_file_ending}"),
            player=self.player,
            player_name=self.multiworld.get_player_name(self.player),
            data={
                "include_socks": bool(self.options.include_socks.value),
                "include_skills": bool(self.options.include_skills.value),
                "include_golden_underwear": bool(self.options.include_golden_underwear.value),
                "include_level_items": bool(self.options.include_level_items.value),
                "include_purple_so": bool(self.options.include_purple_so.value),
                "seed": self.multiworld.seed_name.encode('utf-8'),
                "randomize_gate_cost": self.options.randomize_gate_cost.value,
                "gate_costs": self.gate_costs,
            }
        )
        apbfbb.write()