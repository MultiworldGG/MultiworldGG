# from https://github.com/Pronyo-Chan/paper-mario-randomizer-web-app/blob/master/app/src/app/services/setting-string-mapping/setting-string-mapping.service.ts
import numbers

from .items import item_id_prefix, ap_id_to_pm_data
from .data.starting_maps import starting_maps
from .options import *


class SettingModel:
    compressed_string = "A"
    key = "key"
    type = "formGroup"
    map = None

    def __init__(self, compressed_string, key, type, map=None):
        self.compressed_string = compressed_string
        self.key = key
        self.type = type
        self.map = map


cosmeticsMap = [
    SettingModel("x", "boss_palette", "number"),
    SettingModel("b", "bow_palette", "sprite"),
    SettingModel("c", "coin_palette", "number"),
    SettingModel("g", "goombario_palette", "sprite"),
    SettingModel("k", "kooper_palette", "sprite"),
    SettingModel("o", "bombette_palette", "sprite"),
    SettingModel("m", "status_menu_palette", "number"),
    SettingModel("p", "mario_palette", "sprite"),
    SettingModel("n", "npc_palette", "number"),
    SettingModel("e", "enemy_palette", "number"),
    SettingModel("y", "hammer_palette", "number"),
    SettingModel("t", "random_text", "bool"),
    SettingModel("w", "watt_palette", "sprite"),
    SettingModel("s", "sushie_palette", "sprite"),
    SettingModel("l", "lakilester_palette", "sprite"),
    SettingModel("a", "parakarry_palette", "sprite"),
    SettingModel("r", "roman_numerals", "bool"),
    SettingModel("h", "random_pitch", "bool"),
    SettingModel("d", "mute_danger_beeps", "bool"),
    SettingModel("u", "shuffle_music", "number"),
    SettingModel("j", "shuffle_jingles", "bool")
]

difficultyMap = [
    SettingModel("c", "cap_enemy_xp", "bool"),
    SettingModel("m", "enemy_damage", "number"),
    SettingModel("d", "enemy_difficulty", "number"),
    SettingModel("h", "no_heart_blocks", "bool"),
    SettingModel("s", "no_save_blocks", "bool"),
    SettingModel("a", "enemy_xp_multiplier", "number"),
    SettingModel("k", "one_hit_ko", "bool"),
    SettingModel("l", "no_healing_items", "bool"),
    SettingModel("y", "allowItemHints", "bool"),
    SettingModel("p", "merlow_rewards_pricing", "number"),
    SettingModel("b", "badge_synergy", "bool"),
    SettingModel("v", "drop_star_points", "bool"),
    SettingModel("o", "chet_rippo", "bool"),
    SettingModel("!", "bowser_door_quiz", "number"),
    SettingModel("@", "kent_c_koopa", "number"),
]

goalsMap = [
    SettingModel("w", "star_way_spirits", "number"),
    SettingModel("r", "spirit_requirements", "number"),
    SettingModel("@", "star_beam_spirits", "number"),
    SettingModel("#", "star_beam_power_stars", "number"),
    SettingModel("s", "shuffle_star_beam", "bool"),
    SettingModel("y", "seed_goal", "number"),
    SettingModel("?", "star_way_power_stars", "number"),
    SettingModel("!", "total_power_stars", "number"),
    SettingModel("p", "power_star_hunt", "bool"),
]

itemPoolMap = [
    SettingModel("t", "item_traps", "number"),
    SettingModel("q", "consumable_item_quality", "number"),
    SettingModel("r", "consumable_item_pool", "number"),
    SettingModel("x", "item_pouches", "bool"),
    SettingModel("u", "unused_badge_dupes", "bool"),
    SettingModel("b", "beta_items", "bool"),
    SettingModel("p", "progressive_badges", "bool"),
    SettingModel("l", "badge_pool_limit", "number"),
]

gameplayMap = [
    SettingModel("r", "formation_shuffle", "bool"),
    SettingModel("b", "badge_bp_shuffle", "number"),
    SettingModel("f", "badge_fp_shuffle", "number"),
    SettingModel("p", "partner_fp_shuffle", "number"),
    SettingModel("s", "sp_shuffle", "number"),
    SettingModel("m", "mystery_shuffle", "number"),
    SettingModel("z", "random_puzzles", "bool"),
    SettingModel("o", "boss_shuffle", "bool")
]

itemsMap = [
    SettingModel("v", "overworld_coins", "bool"),
    SettingModel("e", "coin_blocks", "bool"),
    SettingModel("j", "koot_coins", "bool"),
    SettingModel("n", "foliage_coins", "bool"),
    SettingModel("d", "dojo", "number"),
    SettingModel("f", "koot_favors", "number"),
    SettingModel("p", "shuffle_hidden_panels", "bool"),
    SettingModel("s", "include_shops", "bool"),
    SettingModel("k", "keysanity", "bool"),
    SettingModel("i", "shuffleItems", "bool"),
    SettingModel("l", "letter_rewards", "number"),
    SettingModel("r", "trading_events", "bool"),
    SettingModel("!", "super_multi_blocks", "number"),
    SettingModel("g", "gear_shuffle_mode", "number"),
    SettingModel("u", "partner_upgrades", "number"),
    SettingModel("a", "cheato_items", "number"),
    SettingModel("o", "rowf_items", "number"),
    SettingModel("m", "merlow_items", "bool")
]

marioStatsMap = [
    SettingModel("c", "starting_coins", "number"),
    SettingModel("b", "starting_bp", "number"),
    SettingModel("i", "StartingItems", "items"),
    SettingModel("f", "starting_fp", "number"),
    SettingModel("h", "starting_hp", "number"),
    SettingModel("w", "random_start_stats", "bool"),
    SettingModel("l", "random_start_stats_level", "number"),
    SettingModel("s", "starting_sp", "number"),
    SettingModel("j", "starting_boots", "number"),
    SettingModel("a", "starting_hammer", "number"),
    SettingModel("r", "startWithRandomItems", "bool"),
    SettingModel("n", "start_items_min", "number"),
    SettingModel("x", "start_items_max", "number"),
]

openLocationsMap = [
    SettingModel("b", "open_blue_house", "bool"),
    SettingModel("s", "starting_map", "number"),
    SettingModel("t", "open_toybox", "bool"),
    SettingModel("w", "open_whale", "bool"),
    SettingModel("c", "ch7_bridge_visible", "bool"),
    SettingModel("r", "open_mt_rugged", "bool"),
    SettingModel("f", "open_forest", "bool"),
    SettingModel("p", "open_prologue", "bool"),
    SettingModel("m", "magical_seeds", "number"),
    SettingModel("o", "bowser_castle_mode", "number"),
    SettingModel("d", "shuffle_dungeon_entrances", "number"),
    SettingModel("z", "mirror_mode", "number"),
]

startWithPartnersMap = [
    SettingModel("g", "start_with_goombario", "bool"),
    SettingModel("k", "start_with_kooper", "bool"),
    SettingModel("t", "start_with_bombette", "bool"),
    SettingModel("p", "start_with_parakarry", "bool"),
    SettingModel("b", "start_with_bow", "bool"),
    SettingModel("w", "start_with_watt", "bool"),
    SettingModel("s", "start_with_sushie", "bool"),
    SettingModel("l", "start_with_lakilester", "bool"),
]

partnersMap = [
    SettingModel("a", "partners_always_usable", "bool"),
    SettingModel("x", "start_partners_min", "number"),
    SettingModel("n", "start_partners_max", "number"),
    SettingModel("s", "partners", "number"),
    SettingModel("(p", "startWithPartners", "formGroup", startWithPartnersMap),
    SettingModel("r", "start_random_partners", "bool"),
]

qualityOfLifeMap = [
    SettingModel("i", "always_ispy", "bool"),
    SettingModel("p", "always_peekaboo", "bool"),
    SettingModel("s", "always_speedy_spin", "bool"),
    SettingModel("h", "hidden_block_mode", "number"),
    SettingModel("g", "prevent_ooblzs", "bool"),
    SettingModel("q", "quizmo_always_appears", "bool"),
    SettingModel("c", "cutscene_mode", "number"),
    SettingModel("e", "skip_epilogue", "bool"),
    SettingModel("z", "skip_quiz", "bool"),
    SettingModel("l", "writeSpoilerLog", "bool"),
    SettingModel("f", "foliage_item_hints", "bool"),
    SettingModel("t", "revealLogInHours", "number"),
    SettingModel("d", "delaySpoilerLog", "bool"),
    SettingModel("v", "visible_hidden_panels", "bool"),
    SettingModel("o", "cook_without_frying_pan", "bool"),
]

settings_map = [
    SettingModel("(c", "cosmetics", "formGroup", cosmeticsMap),
    SettingModel("(d", "difficulty", "formGroup", difficultyMap),
    SettingModel("(l", "goals", "formGroup", goalsMap),
    SettingModel("(x", "itemPool", "formGroup", itemPoolMap),
    SettingModel("(g", "gameplay", "formGroup", gameplayMap),
    SettingModel("(i", "items", "formGroup", itemsMap),
    SettingModel("(m", "marioStats", "formGroup", marioStatsMap),
    SettingModel("(o", "openLocations", "formGroup", openLocationsMap),
    SettingModel("(p", "partners", "formGroup", partnersMap),
    SettingModel("(q", "qualityOfLife", "formGroup", qualityOfLifeMap),
    SettingModel("g", "glitches", "glitches"),
]


def load_settings_from_site_string(world) -> None:
    settings_string = world.options.pmr_settings_string.value

    decompress_form_group(settings_string, settings_map, world)


def decompress_form_group(settings_string: str, cur_map: list, world):
    start_partners_min = -1

    start_items_min = -1
    start_items_max = -1
    start_random_items = "r"

    i = 0
    while i < len(settings_string):
        is_nesting_key = False

        # Check if we're entering or exiting a nested group
        if settings_string[i] == "(":
            is_nesting_key = True
            i += 1
        elif settings_string[i] == ")":
            i += 1
            return

        if is_nesting_key:
            current_substring = "(" + settings_string[i]
        else:
            current_substring = settings_string[i]

        cur_model = next(
            (
                x
                for x in cur_map
                if x.compressed_string.lower() == current_substring.lower()
            ),
            None
        )

        if cur_model is None:
            i += 1
        else:
            match cur_model.type:
                case "formGroup":
                    i += 1
                    nesting_levels = len([x for x in cur_model.map if x.type == "formGroup"]) + 1
                    form_group_end_index = index_of_nth_occurence(
                        settings_string[i:], ")",
                        nesting_levels
                    ) + i
                    nested_group_substring = settings_string[i:form_group_end_index + 1]

                    i += len(nested_group_substring)
                    decompress_form_group(nested_group_substring, cur_model.map, world)

                # boolean settings are uppercase for true, lowercase for false
                case "bool":
                    if cur_model.key in world.options.__dict__:
                        world.options.__dict__[cur_model.key].value = (
                            current_substring.upper() == current_substring
                        )
                    # store start with random items value
                    elif (   cur_model.key == "startWithRandomItems"
                          or cur_model.key == "startWithRandomItems"
                    ):
                        start_random_items = current_substring

                    i += 1
                    continue

                # sprites and numbers are the same for AP
                case "number":
                    i += 1
                    value = ""
                    while (   settings_string[i].isnumeric()
                           or settings_string[i] == "-"
                           or settings_string[i] == "."
                    ):
                        value += settings_string[i]
                        i += 1

                    if cur_model.key in world.options.__dict__:
                        match cur_model.key:
                            # double xp multiplier, settings string may have 1.5
                            # and we can only use integers
                            case "enemy_xp_multiplier":
                                world.options.__dict__[cur_model.key].value = int(float(value) * 2)
                            case "starting_map":
                                for option, data in starting_maps.items():
                                    if data[0] == int(value):
                                        world.options.__dict__[cur_model.key].value = option
                            # -1 is used as a random value for some settings,
                            # 5 was also used at one point
                            case "coin_palette" | "magical_seeds":
                                option = int(value)
                                if option == 5 or option == -1:
                                    option = world.random.randint(0, 4)
                                world.options.__dict__[cur_model.key].value = option
                            case "star_beam_spirits" | "star_way_spirits":
                                option = int(value)
                                if option == -1:
                                    option = world.random.randint(0, 7)
                                world.options.__dict__[cur_model.key].value = option
                            case _:
                                try:
                                    world.options.__dict__[cur_model.key].value = int(value)
                                except ValueError:
                                    raise ValueError(
                                        'Invalid Paper Mario Settings String: invalid value for '
                                        f'{cur_model.key}.'
                                    )
                    elif cur_model.key.startswith("start_partners_"):
                        if start_partners_min == -1:
                            start_partners_min = int(value)
                        else:
                            start_partners_max = int(value)
                            start_partners_max, start_partners_min = (
                                max(start_partners_max, start_partners_min),
                                min(start_partners_max, start_partners_min)
                            )
                            world.options.start_partners.value = world.random.randint(
                                start_partners_min,
                                start_partners_max
                            )

                    elif cur_model.key.startswith("start_items_"):
                        if start_items_min == -1:
                            start_items_min = int(value)
                        else:
                            start_items_max = int(value)
                            start_items_max, start_items_min = (
                                max(start_items_max, start_items_min),
                                min(start_items_max, start_items_min)
                            )

                case "sprite":
                    i += 1
                    setting = settings_string[i]
                    i += 1
                    palette = settings_string[i]
                    i += 1

                    if cur_model.key in world.options.__dict__:
                        world.options.__dict__[cur_model.key].value = decode_sprite(setting, palette)

                case "items":
                    i += 1
                    # starting items
                    while settings_string[i].isnumeric():
                        # item id in the string is formatted with a leading 0
                        item_id = int(settings_string[i:i+4])

                        # 604-697 are multiworld items, which don't exist on the site
                        if item_id > 603:
                            item_id += 94

                        item_data = ap_id_to_pm_data(item_id + item_id_prefix)
                        world.web_start_inventory.append(item_data[0])
                        i += 4

                # skip glitches for now
                case "glitches":
                    i += 1

            # Not only do we need to check for the min/max, but that the field
            # is actually set in the first place
            if start_random_items == "R" and start_items_min > 0 and start_items_max > 0:
                world.options.random_start_items.value = world.random.randint(start_items_min, start_items_max)
                start_random_items = "r"  # reset this so that we don't roll for item count repeatedly


def index_of_nth_occurence(string: str, substring: str, n: int):
    splits = string.split(substring, n)
    splits.pop()
    return len(substring.join(splits))


def decode_sprite(setting, palette) -> int:
    if setting == "0":
        return 0
    elif setting == "1":
        return int(palette)
    else:
        return int(setting) + 8
