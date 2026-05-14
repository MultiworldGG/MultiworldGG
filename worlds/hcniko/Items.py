from itertools import groupby
from typing import NamedTuple, Dict, Callable, Optional, Set

from BaseClasses import Item, ItemClassification


class HereComesNikoItem(Item):
    game = "Here Comes Niko!"


class HereComesNikoItemData(NamedTuple):
    id: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    num_exist: int = 1
    can_create: Callable = lambda options: True
    item_group: Optional[str] = ""


base_id = 598_145_444_000

item_data_table: Dict[str, HereComesNikoItemData] = {
    "Coin": HereComesNikoItemData(base_id, type=ItemClassification.progression_deprioritized_skip_balancing, num_exist=79),
    "Cassette": HereComesNikoItemData(base_id + 1, type=ItemClassification.progression_deprioritized_skip_balancing, can_create=lambda options: options.cassette_logic.value != 0, num_exist=71, item_group="Cassettes"),
    "Key": HereComesNikoItemData(base_id + 2, type=ItemClassification.progression, num_exist=9, can_create=lambda options: not options.level_based_keys.value, item_group="Keys"),
    #"Letter": HereComesNikoItemData(base_id + 7, type=ItemClassification.filler, num_exist=13),
    "Apples": HereComesNikoItemData(base_id + 3, type=ItemClassification.filler),
    "Contact List 1": HereComesNikoItemData(base_id + 4, type=ItemClassification.progression, num_exist=1, can_create=lambda options: not options.progressive_contact_list.value, item_group="Contact List"),
    "Contact List 2": HereComesNikoItemData(base_id + 5, type=ItemClassification.progression, num_exist=1, can_create=lambda options: not options.progressive_contact_list.value, item_group="Contact List"),
    "Progressive Contact List": HereComesNikoItemData(base_id + 15, type=ItemClassification.progression, num_exist=2, can_create=lambda options: options.progressive_contact_list.value, item_group="Contact List"),
    "Super Jump": HereComesNikoItemData(base_id + 6, type=ItemClassification.useful, num_exist=1),
    "Bugs": HereComesNikoItemData(base_id + 14, type=ItemClassification.filler),
    "Snail Money": HereComesNikoItemData(base_id + 16, type=ItemClassification.filler),
    "Speed Boost": HereComesNikoItemData(base_id + 18, type=ItemClassification.useful, num_exist=8),

    # Traps
    "Freeze Trap": HereComesNikoItemData(base_id + 70, type=ItemClassification.trap),
    "Iron Boots Trap": HereComesNikoItemData(base_id + 71, type=ItemClassification.trap),
    "Whoops! Trap": HereComesNikoItemData(base_id + 72, type=ItemClassification.trap),
    "My Turn! Trap": HereComesNikoItemData(base_id + 73, type=ItemClassification.trap),
    "Gravity Trap": HereComesNikoItemData(base_id + 74, type=ItemClassification.trap),
    "Home Trap": HereComesNikoItemData(base_id + 75, type=ItemClassification.trap),
    "W I D E Trap": HereComesNikoItemData(base_id + 76, type=ItemClassification.trap),
    "Phone Trap": HereComesNikoItemData(base_id + 77, type=ItemClassification.trap),
    "Tiny Trap": HereComesNikoItemData(base_id + 78, type=ItemClassification.trap),
    "Jumping Jacks Trap": HereComesNikoItemData(base_id + 79, type=ItemClassification.trap),
    "Camera Stuck Trap": HereComesNikoItemData(base_id + 81, type=ItemClassification.trap),
    "Inverted Camera Trap": HereComesNikoItemData(base_id + 82, type=ItemClassification.trap),
    "There Goes Niko Trap": HereComesNikoItemData(base_id + 83, type=ItemClassification.trap),

    # Fishsanity
    "Hairball City Fish": HereComesNikoItemData(base_id + 20, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.fishsanity.value == 2, item_group="Fish"),
    "Turbine Town Fish": HereComesNikoItemData(base_id + 21, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.fishsanity.value == 2, item_group="Fish"),
    "Salmon Creek Forest Fish": HereComesNikoItemData(base_id + 22, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.fishsanity.value == 2, item_group="Fish"),
    "Public Pool Fish": HereComesNikoItemData(base_id + 23, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.fishsanity.value == 2, item_group="Fish"),
    "Bathhouse Fish": HereComesNikoItemData(base_id + 24, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.fishsanity.value == 2, item_group="Fish"),
    "Tadpole HQ Fish": HereComesNikoItemData(base_id + 25, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.fishsanity.value == 2, item_group="Fish"),

    # Keys
    "Hairball City Key": HereComesNikoItemData(base_id + 30, type=ItemClassification.progression, can_create=lambda options: options.level_based_keys.value, item_group="Keys"),
    "Turbine Town Key": HereComesNikoItemData(base_id + 31, type=ItemClassification.progression, can_create=lambda options: options.level_based_keys.value, item_group="Keys"),
    "Salmon Creek Forest Key": HereComesNikoItemData(base_id + 32, type=ItemClassification.progression, can_create=lambda options: options.level_based_keys.value, item_group="Keys"),
    "Public Pool Key": HereComesNikoItemData(base_id + 33, type=ItemClassification.progression, can_create=lambda options: options.level_based_keys.value, item_group="Keys"),
    "Bathhouse Key": HereComesNikoItemData(base_id + 34, type=ItemClassification.progression, num_exist=2, can_create=lambda options: options.level_based_keys.value, item_group="Keys"),
    "Tadpole HQ Key": HereComesNikoItemData(base_id + 35, type=ItemClassification.progression, can_create=lambda options: options.level_based_keys.value, item_group="Keys"),

    # Seeds
    "Hairball City Seed": HereComesNikoItemData(base_id + 36, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.seedsanity.value == 2, item_group="Seeds"),
    "Salmon Creek Forest Seed": HereComesNikoItemData(base_id + 37, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.seedsanity.value == 2, item_group="Seeds"),
    "Bathhouse Seed": HereComesNikoItemData(base_id + 38, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.seedsanity.value== 2, item_group="Seeds"),

    # Flowers
    "Hairball City Flower": HereComesNikoItemData(base_id + 40, type=ItemClassification.progression, num_exist=3, can_create=lambda options: options.flowersanity.value == 2, item_group="Flowers"),
    "Turbine Town Flower": HereComesNikoItemData(base_id + 41, type=ItemClassification.progression, num_exist=3, can_create=lambda options: options.flowersanity.value == 2, item_group="Flowers"),
    "Salmon Creek Forest Flower": HereComesNikoItemData(base_id + 42, type=ItemClassification.progression, num_exist=6, can_create=lambda options: options.flowersanity.value == 2, item_group="Flowers"),
    "Public Pool Flower": HereComesNikoItemData(base_id + 43, type=ItemClassification.progression, num_exist=3, can_create=lambda options: options.flowersanity.value == 2, item_group="Flowers"),
    "Bathhouse Flower": HereComesNikoItemData(base_id + 44, type=ItemClassification.progression, num_exist=3, can_create=lambda options: options.flowersanity.value == 2, item_group="Flowers"),
    "Tadpole HQ Flower": HereComesNikoItemData(base_id + 45, type=ItemClassification.progression, num_exist=4, can_create=lambda options: options.flowersanity.value == 2, item_group="Flowers"),

    # NPCs
    # "Hairball City NPCs": HereComesNikoItemData(base_id + 46, type=ItemClassification.progression, can_create=lambda options: options.npcsanity.value, item_group="NPCs"),
    # "Turbine Town NPCs": HereComesNikoItemData(base_id + 47, type=ItemClassification.progression, can_create=lambda options: options.npcsanity.value, item_group="NPCs"),
    # "Salmon Creek Forest NPCs": HereComesNikoItemData(base_id + 48, type=ItemClassification.progression, can_create=lambda options: options.npcsanity.value, item_group="NPCs"),
    # "Public Pool NPCs": HereComesNikoItemData(base_id + 49, type=ItemClassification.progression, can_create=lambda options: options.npcsanity.value, item_group="NPCs"),
    # "Bathhouse NPCs": HereComesNikoItemData(base_id + 50, type=ItemClassification.progression, can_create=lambda options: options.npcsanity.value, item_group="NPCs"),
    # "Tadpole HQ NPCs": HereComesNikoItemData(base_id + 51, type=ItemClassification.progression, can_create=lambda options: options.npcsanity.value, item_group="NPCs"),

    # Level Based Cassettes
    "Hairball City Cassette": HereComesNikoItemData(base_id + 52, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.cassette_logic.value == 0, item_group="Cassettes"),
    "Turbine Town Cassette": HereComesNikoItemData(base_id + 53, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.cassette_logic.value == 0, item_group="Cassettes"),
    "Salmon Creek Forest Cassette": HereComesNikoItemData(base_id + 54, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.cassette_logic.value == 0, item_group="Cassettes"),
    "Public Pool Cassette": HereComesNikoItemData(base_id + 55, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.cassette_logic.value == 0, item_group="Cassettes"),
    "Bathhouse Cassette": HereComesNikoItemData(base_id + 56, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.cassette_logic.value == 0, item_group="Cassettes"),
    "Tadpole HQ Cassette": HereComesNikoItemData(base_id + 57, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.cassette_logic.value == 0, item_group="Cassettes"),
    "Gary's Garden Cassette": HereComesNikoItemData(base_id + 58, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.cassette_logic.value == 0 and options.shuffle_garys_garden.value, item_group="Cassettes"),

    # Permits
    "Safety Helmet": HereComesNikoItemData(base_id + 101, type=ItemClassification.progression, can_create=lambda options: options.bonk_permit.value != 0, item_group="Bonk"),
    "Bug Net": HereComesNikoItemData(base_id + 102, type=ItemClassification.progression, can_create=lambda options: options.bug_catching.value != 0, item_group="Net"),
    "Soda Repair": HereComesNikoItemData(base_id + 103, type=ItemClassification.progression, can_create=lambda options: options.soda_cans.value != 0, item_group="Soda Cans"),
    "Parasol Repair": HereComesNikoItemData(base_id + 104, type=ItemClassification.progression, can_create=lambda options: options.parasols.value != 0, item_group="Parasols"),
    "Swim Course": HereComesNikoItemData(base_id + 105, type=ItemClassification.progression, can_create=lambda options: options.swimming.value != 0, item_group="Swimming"),
    "AC Repair": HereComesNikoItemData(base_id + 107, type=ItemClassification.progression, can_create=lambda options: options.ac_repair.value != 0, item_group="AC"),
    "Apple Basket": HereComesNikoItemData(base_id + 108, type=ItemClassification.progression, can_create=lambda options: options.applebasket.value != 0, item_group="Basket"),

    # Textbox
    "Textbox": HereComesNikoItemData(base_id + 106, type=ItemClassification.progression, can_create=lambda options: options.textbox.value == 1),
    "Home Textbox": HereComesNikoItemData(base_id + 140, type=ItemClassification.progression, can_create=lambda options: options.textbox.value == 2, item_group="Textboxes"),
    "Hairball City Textbox": HereComesNikoItemData(base_id + 141, type=ItemClassification.progression, can_create=lambda options: options.textbox.value == 2, item_group="Textboxes"),
    "Turbine Town Textbox": HereComesNikoItemData(base_id + 142, type=ItemClassification.progression, can_create=lambda options: options.textbox.value == 2, item_group="Textboxes"),
    "Salmon Creek Forest Textbox": HereComesNikoItemData(base_id + 143, type=ItemClassification.progression, can_create=lambda options: options.textbox.value == 2, item_group="Textboxes"),
    "Public Pool Textbox": HereComesNikoItemData(base_id + 144, type=ItemClassification.progression, can_create=lambda options: options.textbox.value == 2, item_group="Textboxes"),
    "Bathhouse Textbox": HereComesNikoItemData(base_id + 145, type=ItemClassification.progression, can_create=lambda options: options.textbox.value == 2, item_group="Textboxes"),
    "Tadpole HQ Textbox": HereComesNikoItemData(base_id + 146, type=ItemClassification.progression, can_create=lambda options: options.textbox.value == 2, item_group="Textboxes"),
    "Gary's Garden Textbox": HereComesNikoItemData(base_id + 147, type=ItemClassification.progression, can_create=lambda options: options.textbox.value == 2 and options.shuffle_garys_garden.value, item_group="Textboxes"),

    # Bonesanity
    "Hairball City Bone": HereComesNikoItemData(base_id + 111, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.bonesanity.value == 2, item_group="Bone"),
    "Turbine Town Bone": HereComesNikoItemData(base_id + 112, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.bonesanity.value == 2, item_group="Bone"),
    "Salmon Creek Forest Bone": HereComesNikoItemData(base_id + 113, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.bonesanity.value == 2, item_group="Bone"),
    "Public Pool Bone": HereComesNikoItemData(base_id + 114, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.bonesanity.value == 2, item_group="Bone"),
    "Bathhouse Bone": HereComesNikoItemData(base_id + 115, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.bonesanity.value == 2, item_group="Bone"),
    "Tadpole HQ Bone": HereComesNikoItemData(base_id + 116, type=ItemClassification.progression, num_exist=5, can_create=lambda options: options.bonesanity.value == 2, item_group="Bone"),

    # Levels
    #"Home": HereComesNikoItemData(base_id + 7, type=ItemClassification.progression),
    "Hairball City Ticket": HereComesNikoItemData(base_id + 8, type=ItemClassification.progression, can_create=lambda options: options.shuffle_kiosk_reward.value, item_group="Tickets"),
    "Turbine Town Ticket": HereComesNikoItemData(base_id + 9, type=ItemClassification.progression, can_create=lambda options: options.shuffle_kiosk_reward.value, item_group="Tickets"),
    "Salmon Creek Forest Ticket": HereComesNikoItemData(base_id + 10, type=ItemClassification.progression, can_create=lambda options: options.shuffle_kiosk_reward.value, item_group="Tickets"),
    "Public Pool Ticket": HereComesNikoItemData(base_id + 11, type=ItemClassification.progression, can_create=lambda options: options.shuffle_kiosk_reward.value, item_group="Tickets"),
    "Bathhouse Ticket": HereComesNikoItemData(base_id + 12, type=ItemClassification.progression, can_create=lambda options: options.shuffle_kiosk_reward.value, item_group="Tickets"),
    "Tadpole HQ Ticket": HereComesNikoItemData(base_id + 13, type=ItemClassification.progression, can_create=lambda options: options.shuffle_kiosk_reward.value, item_group="Tickets"),
    "Gary's Garden Ticket": HereComesNikoItemData(base_id + 17, type=ItemClassification.progression, can_create=lambda options: options.shuffle_kiosk_reward.value and options.access_garys_garden.value != 0 and options.shuffle_garys_garden.value, item_group="Tickets"),
    "Party Invitation": HereComesNikoItemData(base_id + 80, type=ItemClassification.progression, can_create=lambda options: options.chatsanity.value != 0, item_group="Tickets"),

    # Garden Goal
    "Gary's Garden Seed": HereComesNikoItemData(base_id + 250, type=ItemClassification.progression, num_exist=10, can_create=lambda options: options.goal_completion.value == 3, item_group="Seeds"),

    "Victory": HereComesNikoItemData(type=ItemClassification.progression, can_create=lambda options: False)
}

def get_item_group(item_name: str) -> str:
    return item_data_table[item_name].item_group

item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in groupby(sorted(item_data_table, key=get_item_group), get_item_group) if group != ""
}

item_table = {name: data.id for name, data in item_data_table.items() if data.id is not None}
id_to_item_table = {data.id: name for name, data in item_data_table.items() if data.id is not None}
