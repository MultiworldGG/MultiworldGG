import io
import json
import os
import zipfile
from typing import Dict, Optional
from .Locations import locations_by_name

import Utils
from worlds.Files import APPlayerContainer


class LunacidContainer(APPlayerContainer):
    game: str = 'Lunacid'
    patch_file_ending = ".zip"

    def __init__(self, patch_data: Dict[str, str] | io.BytesIO, base_path: str = "", output_directory: str = "",
                 player: Optional[int] = None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + ".zip")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, text in self.patch_data.items():
            opened_zipfile.writestr(filename, text)
        super().write_contents(opened_zipfile)


def generate_json(world, output_directory):
    mod_name = f"AP-LUNACID-{world.multiworld.seed_name}-P{world.player}-{world.multiworld.get_file_safe_player_name(world.player)}"
    mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__)

    item_location_map = get_item_location_map(world)
    important_hints = world.important_item_locations()
    settings, entrances, elements = get_settings(world)
    enemy_placement = world.enemy_random_data
    custom_class = get_custom_class(world)

    files = {
        "item_location_map.json": json.dumps(item_location_map),
        "important_item_hints.json": json.dumps(important_hints),
        "enemy_placement.json": json.dumps(enemy_placement),
        "slot_data.json": json.dumps(settings),
        "elements.json": json.dumps(elements),
        "custom_class.json": json.dumps(custom_class),
        "entrances.json": json.dumps(entrances),
    }

    mod = LunacidContainer(files, mod_dir, output_directory, world.player,
                           world.multiworld.get_file_safe_player_name(world.player))
    mod.write()


def get_item_location_map(world):
    location_item_map = {}

    for location in world.multiworld.get_filled_locations(world.player):
        if location.address is None:
            continue
        location_data = locations_by_name[location.name]
        location_name = location_data.name
        item = world.get_location(location.name).item
        item_data = [item.code, item.name, item.player, world.multiworld.get_player_name(item.player), item.game, item.classification]
        location_item_map[location_name] = item_data
    return location_item_map


def get_settings(world):
    settings = world.fill_slot_data()
    entrances = settings.pop("entrances")
    elements = settings.pop("elements")

    return settings, entrances, elements

def get_custom_class(world):
    class_info = {"created_class_name": world.custom_class_name,
            "created_class_description": world.custom_class_description,
            "created_class_stats": world.custom_class_stats,}
    return class_info
