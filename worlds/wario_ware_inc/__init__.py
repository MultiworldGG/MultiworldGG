import os
import settings
import threading
import pkgutil
import math

from BaseClasses import MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
from rule_builder.rules import Rule
from Options import OptionError

from .options import WarioWareOptions, MicrogameUnlock
from .client import WarioWareClient
from .regions import create_regions
from .rom import patch_rom, WarioWareProcedurePatch, HASH_US
from .enums import Items
from .items import WarioWareItem, all_items, item_groups, game_items, microgame_items
from .locations import all_locations, count_locations_active, location_groups
from .constants import *
from .stage_data import microgame_data, game_groups

from typing import ClassVar, TextIO

class WarioWareSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        f"""File name of the {GAME_NAME} US rom"""
        copy_to = "WarioWare, Inc. - Mega Microgame$! (USA).gba"
        description = "WarioWare, Inc. - Mega Microgame$! (USA) ROM File"
        md5s = [HASH_US]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class WarioWareWeb(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        f"A guide to playing {GAME_NAME} with MultiworldGG",
        "English",
        "setup_en.md",
        "setup/en",
        ["lx5"]
    )
    tutorials = [setup_en]

class WarioWareWorld(World):
    """
    WarioWare, Inc.: Mega Microgames is the first ever WarioWare series title, released in 2003. It is about rapid completion of "microgames", short minigames given to the player consecutively and with increasing speed per each game complete.
    """
    game = GAME_NAME
    web = WarioWareWeb()

    settings: ClassVar[WarioWareSettings]
    
    options_dataclass = WarioWareOptions
    options: WarioWareOptions

    required_client_version = (0, 6, 7)

    item_name_to_id = {str(name): data.code for name, data in all_items.items()}
    location_name_to_id = all_locations
    item_name_groups = item_groups
    location_name_groups = location_groups
    #origin_region_name = Regions.intro_stage.value
    rule_macros: dict[str, Rule.Resolved]

    ut_can_gen_without_yaml: ClassVar = True
    glitches_item_name: str = Items.glitched
    is_ut: bool = False

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        self.rule_macros = {}
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        create_regions(self)

    def create_items(self) -> None:
        itempool: list[WarioWareItem] = []

        total_required_locations = count_locations_active(self)

        # Submit stages to item pool
        if self.is_ut:
            stages = sorted(list(game_items.keys()))
            for stage in stages:
                if stage in self.included_games:
                    itempool.append(self.create_item(stage))

        elif len(self.included_games) != 0:
            stages = sorted(list(game_items.keys()))

            if len(self.options.starting_stage.value) != 0:
                possible_starting_stages = sorted(list(set(self.included_games) & set(self.options.starting_stage.value)))
                starting_stage = self.random.choice(possible_starting_stages)
                stages.remove(starting_stage)
                self.push_precollected(self.create_item(starting_stage))

            for stage in stages:
                if stage in self.included_games:
                    itempool.append(self.create_item(stage))

        # Force initial microgames
        if not self.is_ut:
            starting_microgames_ids = self.random.choices(self.microgames, k=self.options.starting_microgames)
            for microgame in sorted(item_groups["Microgames"]):
                microgame_id = microgame_data[microgame.replace(" Microgame", "")]
                if microgame_id in starting_microgames_ids:
                    self.push_precollected(self.create_item(microgame))

        # Submit microgames to item pool
        if self.options.microgame_unlock == MicrogameUnlock.option_bundles:
            for microgame in sorted(item_groups["Microgame Bundle"]):
                itempool.append(self.create_item(microgame))
        else:
            for microgame in sorted(item_groups["Microgames"]):
                microgame_id = microgame_data[microgame.replace(" Microgame", "")]
                if microgame_id in self.microgames:
                    itempool.append(self.create_item(microgame))

        # Submit flowers to item pool
        if (total_required_locations - len(itempool)) < self.options.flowers.value:
            flower_count = total_required_locations - len(itempool)
        else:
            flower_count = self.options.flowers.value
        itempool += [self.create_item(Items.flower) for _ in range(flower_count)]
        if not self.is_ut:
            self.required_flowers = max(math.floor(flower_count * (self.options.flowers_required.value / 100.0)), 1)

        # Submit junk items
        junk_count = total_required_locations - len(itempool)

        junk_weights = []
        junk_weights += ([Items.beep] * 2)

        junk_pool = []
        for _ in range(junk_count):
            junk_item = self.random.choice(junk_weights)
            junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        # Finish
        self.multiworld.itempool += itempool


    def create_item(self, name: Items, force_classification=False) -> WarioWareItem:
        name = str(name)
        data = all_items[name]
        if force_classification:
            classification = force_classification
        else:
            classification = data.classsification
        created_item = WarioWareItem(name, classification, data.code, self.player)
        return created_item


    def set_rules(self):
        from .rules import WarioWareRules
        WarioWareRules(self).set_rules()


    def fill_slot_data(self) -> dict:
        slot_data = self.options.as_dict(
            "microgame_unlock",
            "stage_hi_scores",
            "flowers",
            "microgame_flowers",
        )
        slot_data["required_flowers"] = self.required_flowers
        slot_data["microgames"] = self.microgames
        slot_data["included_games"] = self.included_games
        return slot_data


    def generate_early(self):
        patch_version = f"{self.world_version.major:02}{self.world_version.minor:02}{self.world_version.build:02}"
        self.auth =  bytearray(f'WW-{patch_version}-{self.player}-{self.multiworld.seed:11}\0', 'utf8')[:21]
        self.auth.extend([0] * (21 - len(self.auth)))

        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data = self.multiworld.re_gen_passthrough[GAME_NAME]
            self.required_flowers = slot_data["required_flowers"]
            self.options.microgame_unlock.value = slot_data["microgame_unlock"]
            self.microgames = slot_data["microgames"]
            self.options.flowers.value = slot_data["flowers"]
            self.included_games = slot_data["included_games"]
            self.options.stage_hi_scores.value = slot_data["stage_hi_scores"]
            self.options.microgame_flowers.value = slot_data["microgame_flowers"]
            self.is_ut = True

        if not self.is_ut:
            if self.options.microgame_unlock == MicrogameUnlock.option_individual:
                if not(len(self.options.included_stages.value) != 0 or self.options.microgame_flowers):
                    raise OptionError(f"{self.player_name} requires including at least one stage or activate Flower locations in order to play with the Individual Microgame Unlock option.")

            # Select microgames
            game_groups_copy = {k.value: v.copy() for k,v in game_groups.items()}
            self.microgames = []
            total_count = self.options.microgame_count.value
            if total_count > 213 - len(self.options.excluded_microgames.value):
                raise OptionError(f"{self.player_name} has way too many excluded microgames, please adjust your YAML by lowering the amount of excluded microgames or lowering the amount of playable microgames.")
            
            count_per_group = total_count // len(game_groups_copy.keys())
            leftovers = total_count % len(game_groups_copy.keys())
            for group_name, microgame_list in game_groups_copy.items():
                microgame_list = [microgame for microgame in  microgame_list if microgame not in self.options.excluded_microgames.value]
                self.random.shuffle(microgame_list)
                for x in range(count_per_group):
                    if len(microgame_list) != 0:
                        microgame_name = microgame_list.pop(0)
                        microgame_id = microgame_data[microgame_name]
                        self.microgames.append(microgame_id)
                    else:
                        leftovers += 1

            # Fill microgame leftovers
            while leftovers != 0:
                for group_name, microgame_list in game_groups_copy.items():
                    microgame_list = [microgame for microgame in  microgame_list if microgame not in self.options.excluded_microgames.value]
                    if leftovers == 0:
                        break
                    if len(microgame_list) != 0:
                        microgame_name = microgame_list.pop(0)
                        microgame_id = microgame_data[microgame_name]
                        self.microgames.append(microgame_id)
                        leftovers -= 1

            self.included_games = []
            self.included_games.extend(self.options.included_stages.value)

            if len(self.options.starting_stage.value):
                self.options.starting_stage.value = self.included_games.copy()
            self.options.starting_stage.value = list(set(self.included_games) & set(self.options.starting_stage.value))


    @staticmethod
    def interpret_slot_data(slot_data):
        return slot_data


    def get_filler_item_name(self) -> str:
        return str(Items.beep)

    
    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nRequired Flowers: {self.required_flowers}")


    def generate_output(self, output_directory: str):
        try:
            patch = WarioWareProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected


    def modify_multidata(self, multidata: dict):
        import base64
        # Put the player's unique authentication in connect_names.
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.player_name]

