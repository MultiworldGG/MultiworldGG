import io
import json
import pkgutil
import struct

import bsdiff4
import random

from typing import TYPE_CHECKING, Dict, Tuple, Iterable
from BaseClasses import Location, ItemClassification
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension, AutoPatchExtensionRegister
from .Items import items_by_id, ItemData
from .Locations import locationName_to_data, location_table, location_id_to_name
from .Data import Rels, shop_items, item_prices, rel_filepaths, location_to_unit, shop_names
from .TTYDPatcher import TTYDPatcher

if TYPE_CHECKING:
    from . import TTYDWorld


class TTYDPatchExtension(APPatchExtension):
    game = "Paper Mario: The Thousand-Year Door"

    @staticmethod
    def patch_mod(caller: "TTYDProcedurePatch") -> None:
        manifest_data = pkgutil.get_data(__name__, "archipelago.json")
        if manifest_data is None:
            raise Exception("TTYD APWorld is missing manifest file (archipelago.json)")
        manifest = json.loads(manifest_data.decode("utf-8"))
        current_version = manifest.get("world_version")
        if current_version is None:
            raise Exception("TTYD APWorld manifest is missing world_version")

        seed_options = json.loads(caller.get_file("options.json").decode("utf-8"))
        patch_version = seed_options.get("world_version")
        if patch_version is None:
            raise Exception("Patch file is missing world_version - regenerate with a newer APWorld")
        if patch_version != current_version:
            raise Exception(f"Patch version ({patch_version}) does not match APWorld version ({current_version}). "
                            f"Please regenerate your patch file or use the matching APWorld version.")

        name_length = min(len(seed_options["player_name"]), 0x10)
        random.seed(seed_options["seed"] + seed_options["player"])
        caller.patcher.dol.data.seek(0x1FF)
        caller.patcher.dol.data.write(name_length.to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x200)
        caller.patcher.dol.data.write(seed_options["player_name"].encode("utf-8")[0:name_length])
        caller.patcher.dol.data.seek(0x210)
        caller.patcher.dol.data.write(seed_options["seed_name"].encode("utf-8")[0:16])
        caller.patcher.dol.data.seek(0x220)
        caller.patcher.dol.data.write(seed_options["palace_stars"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x221)
        caller.patcher.dol.data.write(seed_options["starting_partner"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x222)
        caller.patcher.dol.data.write(seed_options["yoshi_color"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x223)
        caller.patcher.dol.data.write((1).to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x224)
        caller.patcher.dol.data.write((0x80003260).to_bytes(4, "big"))
        caller.patcher.dol.data.seek(0x229)
        caller.patcher.dol.data.write(seed_options["palace_skip"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x22A)
        caller.patcher.dol.data.write(seed_options["westside"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x22B)
        caller.patcher.dol.data.write(seed_options["peekaboo"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x22C)
        caller.patcher.dol.data.write(seed_options["intermissions"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x22D)
        caller.patcher.dol.data.write(seed_options["starting_hp"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x22E)
        caller.patcher.dol.data.write(seed_options["starting_fp"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x22F)
        caller.patcher.dol.data.write(seed_options["starting_bp"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x230)
        caller.patcher.dol.data.write(seed_options["full_run_bar"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x231)
        for star in seed_options["required_chapters"]:
            caller.patcher.dol.data.write(star.to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x238)
        caller.patcher.dol.data.write(seed_options["tattlesanity"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x239)
        caller.patcher.dol.data.write(seed_options["fast_travel"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x23A)
        caller.patcher.dol.data.write(seed_options["succeed_conditions"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x23C)
        caller.patcher.dol.data.write(seed_options["cutscene_skip"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x23D)
        caller.patcher.dol.data.write(seed_options["experience_multiplier"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x23E)
        caller.patcher.dol.data.write(seed_options["starting_level"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x241)
        caller.patcher.dol.data.write(seed_options["music"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x242)
        caller.patcher.dol.data.write(seed_options["block_visibility"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x243)
        caller.patcher.dol.data.write(seed_options["first_attack"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x244)
        caller.patcher.dol.data.write(random.randbytes(4))
        caller.patcher.dol.data.seek(0x248)
        caller.patcher.dol.data.write(seed_options["goal_stars"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x249)
        caller.patcher.dol.data.write(seed_options["goal"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x24A)
        caller.patcher.dol.data.write(seed_options["star_shuffle"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x24B)
        caller.patcher.dol.data.write(seed_options["dazzle_rewards"].to_bytes(1, "big"))
        # caller.patcher.dol.data.seek(0x24C)
        # caller.patcher.dol.data.write() RESERVED
        caller.patcher.dol.data.seek(0x24D)
        caller.patcher.dol.data.write(seed_options["shop_purchase_limit"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x24E)
        caller.patcher.dol.data.write(seed_options["grubba_bribe_direction"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x24F)
        caller.patcher.dol.data.write(seed_options["grubba_bribe_cost"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x250)
        caller.patcher.dol.data.write(seed_options["blue_pipe_toggle"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x251)
        caller.patcher.dol.data.write(seed_options["enemy_randomizer"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x252)
        caller.patcher.dol.data.write(seed_options["enemy_stat_scaling"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x253)
        caller.patcher.dol.data.write(seed_options["shuffle_chapter_stats"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x258)
        caller.patcher.dol.data.write(seed_options["badge_bp"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x259)
        caller.patcher.dol.data.write(seed_options["badge_fp"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x25A)
        caller.patcher.dol.data.write(seed_options["partner_fp"].to_bytes(1, "big"))
        caller.patcher.dol.data.seek(0x260)
        caller.patcher.dol.data.write(seed_options["yoshi_name"].encode("utf-8")[0:8] + b"\x00")
        caller.patcher.dol.data.seek(0xEB6B6)
        caller.patcher.dol.data.write(int.to_bytes(seed_options["starting_coins"], 2, "big"))
        caller.patcher.dol.data.seek(0x1888)
        caller.patcher.dol.data.write(pkgutil.get_data(__name__, "data/US.bin"))
        caller.patcher.dol.data.seek(0x6CE38)
        caller.patcher.dol.data.write(int.to_bytes(0x4BF94A50, 4, "big"))
        caller.patcher.dol.data.seek(0x3C25FC)
        caller.patcher.dol.data.write(int.to_bytes(0x2198, 4, "big"))
        caller.patcher.iso.add_new_directory("files/mod")
        caller.patcher.iso.add_new_directory("files/mod/subrels")
        for file in [file for file in rel_filepaths if file != "mod"]:
            caller.patcher.iso.add_new_file(f"files/mod/subrels/{file}.rel", io.BytesIO(pkgutil.get_data(__name__, f"data/{file}.rel")))
        caller.patcher.iso.add_new_file("files/mod/mod.rel", io.BytesIO(pkgutil.get_data(__name__, f"data/mod.rel")))
        caller.patcher.iso.add_new_file("files/mod/custom.rel", io.BytesIO(pkgutil.get_data(__name__, f"data/custom.rel")))
        caller.patcher.iso.add_new_file("files/mod/enemies.bin", io.BytesIO(caller.get_file("enemies.bin")))
        caller.patcher.iso.add_new_file("files/msg/US/mod.txt", io.BytesIO(pkgutil.get_data(__name__, f"data/mod.txt")))
        caller.patcher.iso.add_new_file("files/msg/US/desc.txt", io.BytesIO(caller.get_file("desc.txt")))



    @staticmethod
    def close_iso(caller: "TTYDProcedurePatch") -> None:
        for rel in caller.patcher.rels.keys():
            caller.patcher.iso.changed_files[get_rel_path(rel)] = caller.patcher.rels[rel]
        caller.patcher.iso.changed_files["sys/main.dol"] = caller.patcher.dol.data
        for _,_ in caller.patcher.iso.export_disc_to_iso_with_changed_files(caller.file_path):
            continue

    @staticmethod
    def patch_icon(caller: "TTYDProcedurePatch") -> None:
        icon_patch = pkgutil.get_data(__name__, f"data/icon.bsdiff4")
        bin_patch = pkgutil.get_data(__name__, f"data/icon_bin.bsdiff4")
        icon_file = caller.patcher.iso.read_file_data("files/icon.tpl")
        bin_file = caller.patcher.iso.read_file_data("files/icon.bin")
        icon_file.seek(0)
        original_icon_data = icon_file.read()
        bin_file.seek(0)
        original_bin_data = bin_file.read()
        patched_icon_data = bsdiff4.patch(original_icon_data, icon_patch)
        patched_bin_data = bsdiff4.patch(original_bin_data, bin_patch)
        new_icon_file = io.BytesIO(patched_icon_data)
        new_bin_file = io.BytesIO(patched_bin_data)
        caller.patcher.iso.changed_files["files/icon.tpl"] = new_icon_file
        caller.patcher.iso.changed_files["files/icon.bin"] = new_bin_file


    @staticmethod
    def patch_items(caller: "TTYDProcedurePatch") -> None:
        from CommonClient import logger
        locations: Dict[str, Tuple] = json.loads(caller.get_file(f"locations.json").decode("utf-8"))
        for location_name, (item_id, player, shop_price) in locations.items():
            data = locationName_to_data.get(location_name, None)
            if data is None:
                continue
            if data.offset or "Tattle" in location_name:
                if player != caller.player:
                    item_data = ItemData(id=0, item_name="", progression="filler", rom_id=0x71)
                else:
                    item_data = items_by_id.get(item_id, ItemData(id=0, item_name="", progression="filler", rom_id=0x0))
                if item_data.rom_id == 0:
                    logger.error(f"Item {item_data.item_name} not found in item_type_dict")
                if data.rel == Rels.dol:
                    if "Tattle" in location_name:
                        for unit_id in location_to_unit[location_table[location_name]]:
                            logger.info(f"Writing Tattle item {item_data.item_name} to unit {unit_id}")
                            caller.patcher.dol.data.seek(0xB00 + ((unit_id - 1) * 2))
                            caller.patcher.dol.data.write(item_data.rom_id.to_bytes(2, "big"))
                        continue
                    if "Dazzle" in location_name:
                        caller.patcher.dol.data.seek(data.offset[0])
                        caller.patcher.dol.data.write(item_data.rom_id.to_bytes(2, "big"))
                else:
                    for i, offset in enumerate(data.offset):
                        if "30 Coins" in data.name and i == 1:
                            caller.patcher.rels[Rels.pik].seek(offset)
                            caller.patcher.rels[Rels.pik].write(item_data.rom_id.to_bytes(4, "big"))
                            continue
                        caller.patcher.rels[data.rel].seek(offset)
                        caller.patcher.rels[data.rel].write(item_data.rom_id.to_bytes(4, "big"))
                        if data.id in shop_items:
                            caller.patcher.rels[data.rel].seek(offset + 4)
                            if item_data.rom_id == 0x71:
                                caller.patcher.rels[data.rel].write(int.to_bytes(20, 4, "big"))
                            else:
                                caller.patcher.rels[data.rel].write(int.to_bytes(shop_price, 4, "big"))

def get_rel_path(rel: Rels):
    return f'files/rel/{rel.value}.rel'


class TTYDProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Paper Mario: The Thousand-Year Door"
    hash = "4b1a5897d89d9e74ec7f630eefdfd435"
    patch_file_ending = ".apttyd"
    result_file_ending = ".iso"
    file_path: str = ""
    patcher: "TTYDPatcher"

    procedure = [
        ("patch_mod", []),
        ("patch_icon", []),
        ("patch_items", []),
        ("close_iso", [])
    ]

    def patch(self, target) -> None:
        self.patcher = TTYDPatcher()
        self.file_path = target
        self.read()
        patch_extender = AutoPatchExtensionRegister.get_handler(self.game)
        assert not isinstance(self.procedure, str), f"{type(self)} must define procedures"
        for step, args in self.procedure:
            if isinstance(patch_extender, list):
                extension = next((item for item in [getattr(extender, step, None) for extender in patch_extender]
                                  if item is not None), None)
            else:
                extension = getattr(patch_extender, step, None)
            if extension is not None:
                extension(self, *args)

def write_files(world: "TTYDWorld", patch: TTYDProcedurePatch) -> None:
    manifest_data = pkgutil.get_data(__name__, "archipelago.json")
    if manifest_data is None:
        raise Exception("TTYD APWorld is missing manifest file (archipelago.json)")
    manifest = json.loads(manifest_data.decode("utf-8"))
    world_version = manifest.get("world_version")
    if world_version is None:
        raise Exception("TTYD APWorld manifest is missing world_version")

    options_dict = {
        "world_version": world_version,
        "seed": world.multiworld.seed,
        "seed_name": world.multiworld.seed_name,
        "player": world.player,
        "player_name": world.multiworld.player_name[world.player],
        "yoshi_name": world.options.yoshi_name.value,
        "yoshi_color": world.options.yoshi_color.value,
        "starting_partner": world.options.starting_partner.value,
        "palace_stars": world.options.palace_stars.value,
        "goal_stars": world.options.goal_stars.value,
        "starting_coins": world.options.starting_coins.value,
        "palace_skip": world.options.palace_skip.value,
        "westside": world.options.open_westside.value,
        "peekaboo": world.options.permanent_peekaboo.value,
        "intermissions": world.options.disable_intermissions.value,
        "starting_hp": world.options.starting_hp.value,
        "starting_fp": world.options.starting_fp.value,
        "starting_bp": world.options.starting_bp.value,
        "full_run_bar": world.options.full_run_bar.value,
        "required_chapters": world.required_chapters,
        "tattlesanity": world.options.tattlesanity.value,
        "fast_travel": world.options.fast_travel.value,
        "succeed_conditions": world.options.succeed_conditions.value,
        "cutscene_skip": world.options.cutscene_skip.value,
        "experience_multiplier": world.options.experience_multiplier.value,
        "starting_level": world.options.starting_level.value,
        "first_attack": world.options.first_attack.value,
        "music": world.options.music_settings.value,
        "block_visibility": world.options.block_visibility.value,
        "goal": world.options.goal.value,
        "star_shuffle": world.options.star_shuffle.value,
        "dazzle_rewards": world.options.dazzle_rewards.value,
        "shop_purchase_limit": world.options.shop_purchase_limit.value,
        "grubba_bribe_direction": world.options.grubba_bribe_direction.value,
        "grubba_bribe_cost": world.options.grubba_bribe_cost.value,
        "blue_pipe_toggle": world.options.blue_pipe_toggle.value,
        "enemy_randomizer": world.options.enemy_randomizer.value,
        "enemy_stat_scaling": world.options.enemy_stat_scaling.value,
        "shuffle_chapter_stats": world.options.shuffle_chapter_stats.value,
        "badge_bp": world.options.badge_bp.value,
        "badge_fp": world.options.badge_fp.value,
        "partner_fp": world.options.partner_fp.value
    }

    buffer = io.BytesIO()
    for i in range(len(shop_items)):
        location = world.get_location(location_id_to_name[shop_items[i]])
        player_name = sanitize_string(world.multiworld.player_name[location.item.player]) if location.item is not None else "Unknown Player"
        item_name = sanitize_string(location.item.name)
        buffer.write(f"ap_{shop_names[i // 6]}_{i % 6}".encode('utf-8'))
        buffer.write(b'\x00')
        buffer.write(f"{player_name}'s\n<col {classification_to_color(location.item.classification)}ff>{item_name}</col>".encode('utf-8'))
        buffer.write(b'\x00')
    buffer.write(b'\x00')  # null terminator for the end of the table

    enemy_buffer = io.BytesIO()
    encounters = world.encounters
    enemy_buffer.write(struct.pack(">H", len(encounters)))
    for entry in encounters:
        ids = entry.enemy_ids
        enemy_buffer.write(struct.pack("B", len(ids)))
        for eid in ids:
            enemy_buffer.write(struct.pack("B", eid))

    patch.write_file("desc.txt", buffer.getvalue())
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))
    patch.write_file(f"locations.json", json.dumps(locations_to_dict(world.multiworld.get_locations(world.player))).encode("UTF-8"))
    patch.write_file("enemies.bin", enemy_buffer.getvalue())

def classification_to_color(classification: ItemClassification = ItemClassification.filler) -> str:
    if classification & ItemClassification.progression:
        return "6838c6"
    elif classification & ItemClassification.trap:
        return "b1130f"
    elif classification & ItemClassification.useful:
        return "3d4f84"
    else:
        return "005858"


def locations_to_dict(locations: Iterable[Location]) -> Dict[str, Tuple]:
    result = {}
    for location in locations:
        if location.item is not None:
            item_code = location.item.code
            item_player = location.item.player
            # Add shop price if this location is a shop item
            is_shop = locationName_to_data[location.name].id in shop_items
            shop_price = item_prices.get(item_code, 10) if is_shop else 10
            result[location.name] = (item_code, item_player, shop_price)
        else:
            result[location.name] = (0, 0, 0)
    return result

def sanitize_string(input_string) -> str:
    input_string = input_string.replace('\\', '\\\\') # Use the built in heart symbol and make sure escape sequences don't happen
    allowed_chars = ' !"#$%&\'()=~|-^\\[]P{};:+*/?_,.@`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789‘’‚“”„Œœ¡¤ª«²³º»¼½¾¿ÀÁÂÄÇÈÉÊËÌÍÎÏÐÑÒÓÔÖ×ØÙÚÛÜÞßàáâäçèéêëìíîïñòóôöùúûü'
    filtered_chars = [char for char in input_string if char in allowed_chars]
    return "".join(filtered_chars)
    