import datetime
import json

from Options import PerGameCommonOptions

from ..Hints import (buildAltarHints, buildGanonText, buildMiscDualHints, buildMiscItemHints,
                     buildMiscLocationHints, get_item_hint_text, getSimpleHintNoPrefix, writeGossipStoneHints)
from ..Messages import update_map_compass_messages, update_warp_song_text
from ..OcarinaSongs import patch_songs
from ..Options import OoTOptions
from ..Patches import (AP_MAX_PLAYER_ID, AP_PLAYER_TABLE_SIZE, check_location_dupes, configure_dungeon_info,
                       get_bigocto_location, get_override_entry, get_override_table,
                       get_override_table_bytes, override_key_struct, require_symbol_length,
                       write_ap_item_name_table)
from ..SceneFlags import (build_xflag_tables, build_xflags_from_world, get_alt_list_bytes,
                          get_collectible_flag_addresses)
from ..Utils import data_path
from Utils import __version__ as ap_version

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "AP"


class SymbolWrites:
    """Collect ROM writes using addresses from symbols.json."""

    def __init__(self):
        with open(data_path("generated/symbols.json")) as stream:
            self.symbols = json.load(stream)
        self.writes = []

    def sym(self, name):
        entry = self.symbols[name]
        return int(entry["address"] if isinstance(entry, dict) else entry, 16)

    def sym_length(self, name):
        if name not in self.symbols:
            return 0
        entry = self.symbols[name]
        return entry.get("length", 1) if isinstance(entry, dict) else 1

    def write_bytes(self, address, value):
        self.writes.append([address, bytes(value).hex()])

    def write_byte(self, address, value):
        self.write_bytes(address, bytes([value]))

    def write_int32(self, address, value):
        self.write_bytes(address, value.to_bytes(4, "big"))


class MessageUpdates:
    """Collect message edits to apply after reading the ROM's message table."""

    def __init__(self):
        self.updates = []

    def record(self, message_id, text, opts):
        self.updates.append([message_id, text, opts])


def json_value(value):
    if isinstance(value, dict):
        return {key: json_value(inner) for key, inner in value.items()}
    if isinstance(value, (set, frozenset)):
        return [json_value(inner) for inner in sorted(value)]
    if isinstance(value, (list, tuple)):
        return [json_value(inner) for inner in value]
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    raise TypeError(f"Unsupported OoT patch data: {type(value).__name__}")


def serialize_item(item, world):
    if item is None:
        return None
    return {
        "name": item.name, "game": item.game, "player": item.player,
        "type": getattr(item, "type", None), "index": getattr(item, "index", None),
        "special": {key: value for key, value in getattr(item, "special", {}).items()
                    if key in {"item_id", "song_id", "text_id", "object", "gi_id", "shop_object"}},
        "trap": item.trap, "advancement": item.advancement,
        "dungeonitem": getattr(item, "dungeonitem", False),
        "hint_text": get_item_hint_text(item, world),
        "simple_hint": getSimpleHintNoPrefix(item),
        "looks_like_item": serialize_item(getattr(item, "looks_like_item", None), world),
    }


def build_collectible_data(world):
    writer = SymbolWrites()
    tables, alternatives = build_xflags_from_world(world)
    scenes, rooms, blob, max_bit = build_xflag_tables(tables)
    for symbol, data in (("xflag_scene_table", scenes), ("xflag_room_table", rooms),
                         ("xflag_room_blob", blob), ("alt_overrides", get_alt_list_bytes(alternatives))):
        require_symbol_length(writer, symbol, len(data))
        writer.write_bytes(writer.sym(symbol), data)
    flag_bytes = int(max_bit / 8) + 1
    flag_bytes += flag_bytes % 8
    writer.write_bytes(writer.sym("num_override_flags"), flag_bytes.to_bytes(2, "big"))
    world.collectible_override_flags = writer.sym("collectible_override_flags") - writer.sym("RANDO_CONTEXT")
    world.collectible_flag_offsets = get_collectible_flag_addresses(world, tables)
    world.shop_location_flags = world.calculate_shop_location_flags()
    return writer.writes


def build_patch_data(world):
    if world.multiworld.players > AP_MAX_PLAYER_ID:
        raise RuntimeError(f"Ocarina of Time supports up to {AP_MAX_PLAYER_ID} AP players.")
    check_location_dupes(world)
    symbols = SymbolWrites()
    for symbol, length in (("PLAYER_ID", 2), ("PLAYER_NAMES", AP_PLAYER_TABLE_SIZE * 8),
                           ("MW_PROGRESSIVE_ITEMS_STATE", AP_PLAYER_TABLE_SIZE * 4),
                           ("CFG_DUNGEON_REWARD_WORLDS", 9 * 2)):
        require_symbol_length(symbols, symbol, length)
    writes = {"collectibles": build_collectible_data(world)}
    writer = SymbolWrites()
    configure_dungeon_info(writer, world)
    writes["dungeon_info"] = writer.writes

    world.ap_item_name_ids = {}
    world.ap_item_names = []
    bigocto = get_bigocto_location(world)
    writer = SymbolWrites()
    if bigocto is not None and bigocto.item is not None:
        entry = get_override_entry(world, bigocto)
        if entry is not None:
            writer.write_bytes(writer.sym("CFG_BIGOCTO_OVERRIDE_KEY"), override_key_struct.pack(*entry[:3]))
    writes["bigocto"] = writer.writes
    writer = SymbolWrites()
    overrides = get_override_table_bytes(get_override_table(world))
    if len(overrides) >= writer.sym_length("cfg_item_overrides"):
        raise RuntimeError("Exceeded item override table size")
    writer.write_bytes(writer.sym("cfg_item_overrides"), overrides)
    write_ap_item_name_table(world, writer)
    writes["overrides"] = writer.writes
    writer = SymbolWrites()
    patch_songs(world, writer)
    writes["songs"] = writer.writes

    messages = {}
    updates = MessageUpdates()
    if world.hints != "none":
        writeGossipStoneHints(world, updates)
    messages["gossip"] = updates.updates
    updates = MessageUpdates()
    if "ganondorf" in world.misc_hints:
        buildGanonText(world, updates)
    buildMiscItemHints(world, updates)
    buildMiscLocationHints(world, updates)
    buildMiscDualHints(world, updates)
    messages["misc"] = updates.updates
    updates = MessageUpdates()
    update_map_compass_messages(updates, world)
    messages["map_compass"] = updates.updates
    updates = MessageUpdates()
    buildAltarHints(world, updates,
                    include_rewards="altar" in world.misc_hints and "compass_reward" not in world.enhance_map_compass,
                    include_wincons="altar" in world.misc_hints)
    messages["altar"] = updates.updates
    updates = MessageUpdates()
    update_warp_song_text(updates, world)
    messages["warp"] = updates.updates

    locations = []
    for location in world.get_locations():
        record = {name: json_value(getattr(location, name, None)) for name in (
            "name", "address", "address1", "address2", "default", "type", "scene", "price",
            "vanilla_item", "locked", "show_in_spoiler")}
        record.update(region=location.parent_region.name, disabled=location.disabled.value,
                      item=serialize_item(location.item, world))
        locations.append(record)

    entrances = []
    for entrance in world.get_shufflable_entrances():
        replacement = entrance.replaces
        entrances.append({
            "name": entrance.name, "type": entrance.type, "primary": entrance.primary,
            "shuffled": entrance.shuffled, "data": json_value(entrance.data),
            "replacement": ({"name": replacement.name, "data": json_value(replacement.data)}
                            if replacement else None),
        })

    setting_names = (OoTOptions.type_hints.keys() - EXCLUDED_PATCH_OPTIONS) | set(PATCH_STATE_FIELDS)
    settings = {name: json_value(getattr(world, name)) for name in sorted(setting_names)}
    settings["adult_trade_starting_inventory"] = getattr(world, "adult_trade_starting_inventory", "")
    return {
        "settings": settings, "player": world.player, "player_count": world.multiworld.players,
        "show_shop_recipient": len(world.multiworld.worlds) > 1,
        "player_names": {player: world.multiworld.get_player_name(player)
                         for player in world.multiworld.get_all_ids()},
        "generation_time": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "generator_version": f"{apname} {ap_version}",
        "hylian_shield_discount": world.random.choice(list(range(5, 45, 5))),
        "rng_seed": world.random.getrandbits(32),
        "text_rng_seed": world.random.getrandbits(64),
        "cosmetic_rng_seed": world.random.getrandbits(64),
        "locations": locations, "entrances": entrances,
        "shuffled_grotto_entrances": [entrance.name for entrance in world.get_shuffled_entrances(type="Grotto")],
        "bigocto_location": bigocto.name if bigocto is not None else None,
        "king_dodongo_shortcut": world.region_has_shortcuts("King Dodongo Boss Room"),
        "boss_key_rings": [name for name in world.dungeon_mq if world.keyring_gives_boss_key(name)],
        "removed_silver_rupee_puzzles": world.silver_rupee_puzzles(),
        "song_notes": {name: str(song) for name, song in world.song_notes.items()},
        "trap_appearances": {address: serialize_item(item, world) for address, item in world.trap_appearances.items()},
        "shop_location_flags": world.shop_location_flags,
        "writes": writes, "messages": messages,
    }


EXCLUDED_PATCH_OPTIONS = {
    *PerGameCommonOptions.type_hints,
    "plando_connections", "plandomized_locations",
    "allowed_tricks", "advanced_allowed_tricks",
}

# Values computed during generation rather than declared in OoTOptions.
PATCH_STATE_FIELDS = (
    'available_tokens',
    'disable_trade_revert',
    'dungeon_mq',
    'file_hash',
    'keysanity',
    'lacs_condition',
    'lacs_hearts',
    'lacs_medallions',
    'lacs_rewards',
    'lacs_stones',
    'lacs_tokens',
    'randomized_starting_items',
    'scrub_prices',
    'selected_adult_trade_item',
    'shop_prices',
    'skip_child_zelda',
    'skipped_trials',
    'songs_as_items',
    'starting_items',
)
