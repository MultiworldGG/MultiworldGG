from typing import TYPE_CHECKING, List, Tuple

from BaseClasses import ItemClassification as IC
from ..Logic.Macros import *
from ...generic.Rules import set_rule
from ..options import (
    DungeonItem,
    DungeonRewardsProgression,
    GoldenBugsShuffled,
    PoeShuffled,
    SkyCharactersShuffled,
)
from ..Items import (
    ITEM_TABLE,
    PortalItems,
    TPItem,
    TPItemData,
    item_factory,
    item_name_groups,
)

if TYPE_CHECKING:
    from .. import TPWorld

VANILLA_SMALL_KEYS_LOCATIONS = {
    "Forest Temple": {
        "Forest Temple Small Key": [
            "Forest Temple Big Baba Key",
            "Forest Temple North Deku Like Chest",
            "Forest Temple Totem Pole Chest",
            "Forest Temple Windless Bridge Chest",
        ],
    },
    "Goron Mines": {
        "Goron Mines Small Key": [
            "Goron Mines Main Magnet Room Bottom Chest",
            "Goron Mines Crystal Switch Room Underwater Chest",
            "Goron Mines Outside Beamos Chest",
        ],
    },
    "Lakebed Temple": {
        "Lakebed Temple Small Key": [
            "Lakebed Temple Before Deku Toad Alcove Chest",
            "Lakebed Temple East Lower Waterwheel Stalactite Chest",
            "Lakebed Temple East Second Floor Southeast Chest",
        ],
    },
    "Arbiters Grounds": {
        "Arbiters Grounds Small Key": [
            "Arbiters Grounds Entrance Chest",
            "Arbiters Grounds East Lower Turnable Redead Chest",
            "Arbiters Grounds East Upper Turnable Redead Chest",
            "Arbiters Grounds Ghoul Rat Room Chest",
            "Arbiters Grounds North Turning Room Chest",
        ],
    },
    "Snowpeak Ruins": {
        "Snowpeak Ruins Small Key": [
            "Snowpeak Ruins East Courtyard Chest",
            "Snowpeak Ruins West Courtyard Buried Chest",
            "Snowpeak Ruins Wooden Beam Chandelier Chest",
            "Snowpeak Ruins Northeast Chandelier Chest",
        ],
        "Ordon Pumpkin": [
            "Snowpeak Ruins Ordon Pumpkin Chest",
        ],
        "Ordon Goat Cheese": ["Snowpeak Ruins Chest After Darkhammer"],
    },
    "Temple of Time": {
        "Temple of Time Small Key": [
            "Temple of Time Lobby Lantern Chest",
            "Temple of Time Armos Antechamber East Chest",
            "Temple of Time Guillotine Chest",
        ],
    },
    "City in The Sky": {
        "City in The Sky Small Key": [
            "City in The Sky West Wing First Chest",
        ],
    },
    "Palace of Twilight": {
        "Palace of Twilight Small Key": [
            "Palace of Twilight West Wing First Room Central Chest",
            "Palace of Twilight West Wing Second Room Central Chest",
            "Palace of Twilight East Wing First Room Zant Head Chest",
            "Palace of Twilight East Wing Second Room Southeast Chest",
            "Palace of Twilight Central Tower Chest",
            "Palace of Twilight Central Outdoor Chest",
            "Palace of Twilight Central First Room Chest",
        ],
    },
    "Hyrule Castle": {
        "Hyrule Castle Small Key": [
            "Hyrule Castle King Bulblin Key",
            "Hyrule Castle Graveyard Owl Statue Chest",
            "Hyrule Castle Southeast Balcony Tower Chest",
        ],
    },
}

VANILLA_BIG_KEY_LOCATIONS = {
    "Forest Temple": {
        "Forest Temple Big Key": [
            "Forest Temple Big Key Chest",
        ],
    },
    "Goron Mines": {
        "Goron Mines Key Shard": [
            "Goron Mines Gor Amato Key Shard",
            "Goron Mines Gor Ebizo Key Shard",
            "Goron Mines Gor Liggs Key Shard",
        ],
    },
    "Lakebed Temple": {
        "Lakebed Temple Big Key": [
            "Lakebed Temple Big Key Chest",
        ],
    },
    "Arbiters Grounds": {
        "Arbiters Grounds Big Key": [
            "Arbiters Grounds Big Key Chest",
        ],
    },
    "Snowpeak Ruins": {
        "Bedroom Key": [
            "Snowpeak Ruins Chapel Chest",
        ],
    },
    "Temple of Time": {
        "Temple of Time Big Key": [
            "Temple of Time Big Key Chest",
        ],
    },
    "City in The Sky": {
        "City in The Sky Big Key": [
            "City in The Sky Big Key Chest",
        ],
    },
    "Palace of Twilight": {
        "Palace of Twilight Big Key": [
            "Palace of Twilight Big Key Chest",
        ],
    },
    "Hyrule Castle": {
        "Hyrule Castle Big Key": [
            "Hyrule Castle Big Key Chest",
        ],
    },
}
DUNGEON_TO_BOSS_DEFEAT: dict[str, list[str | None]] = {
    "Forest Temple": [
        "Forest Temple Diababa Heart Container",
        "Forest Temple Dungeon Reward",
    ],
    "Goron Mines": [
        "Goron Mines Fyrus Heart Container",
        "Goron Mines Dungeon Reward",
    ],
    "Lakebed Temple": [
        "Lakebed Temple Morpheel Heart Container",
        "Lakebed Temple Dungeon Reward",
    ],
    "Arbiters Grounds": [
        "Arbiters Grounds Stallord Heart Container",
        "Arbiters Grounds Dungeon Reward",
    ],
    "Snowpeak Ruins": [
        "Snowpeak Ruins Blizzeta Heart Container",
        "Snowpeak Ruins Dungeon Reward",
    ],
    "Temple of Time": [
        "Temple of Time Armogohma Heart Container",
        "Temple of Time Dungeon Reward",
    ],
    "City in The Sky": [
        "City in The Sky Argorok Heart Container",
        "City in The Sky Dungeon Reward",
    ],
    "Palace of Twilight": [
        "Palace of Twilight Zant Heart Container",
        # "", # no dungeon reward
    ],
    # Hyrule castle boss defeat is game complete
    "Hyrule Castle": [
        #     "",
        #     "",
    ],
}
VANILLA_MAP_AND_COMPASS_LOCATIONS = {
    "Forest Temple": {
        "Forest Temple Map": [
            "Forest Temple Central North Chest",
        ],
        "Forest Temple Compass": [
            "Forest Temple Central Chest Hanging From Web",
        ],
    },
    "Goron Mines": {
        "Goron Mines Map": [
            "Goron Mines Gor Amato Chest",
        ],
        "Goron Mines Compass": [
            "Goron Mines Beamos Room Chest",
        ],
    },
    "Lakebed Temple": {
        "Lakebed Temple Map": [
            "Lakebed Temple Central Room Chest",
        ],
        "Lakebed Temple Compass": [
            "Lakebed Temple West Water Supply Chest",
        ],
    },
    "Arbiters Grounds": {
        "Arbiters Grounds Map": [
            "Arbiters Grounds Torch Room West Chest",
        ],
        "Arbiters Grounds Compass": [
            "Arbiters Grounds East Upper Turnable Chest",
        ],
    },
    "Snowpeak Ruins": {
        "Snowpeak Ruins Map": [
            "Snowpeak Ruins Mansion Map",
        ],
        "Snowpeak Ruins Compass": [
            "Snowpeak Ruins Wooden Beam Northwest Chest",
        ],
    },
    "Temple of Time": {
        "Temple of Time Map": [
            "Temple of Time First Staircase Armos Chest",
        ],
        "Temple of Time Compass": [
            "Temple of Time Moving Wall Beamos Room Chest",
        ],
    },
    "City in The Sky": {
        "City in The Sky Map": [
            "City in The Sky East First Wing Chest After Fans",
        ],
        "City in The Sky Compass": [
            "City in The Sky East Wing Lower Level Chest",
        ],
    },
    "Palace of Twilight": {
        "Palace of Twilight Map": [
            "Palace of Twilight East Wing Second Room Southwest Chest",
        ],
        "Palace of Twilight Compass": [
            "Palace of Twilight West Wing Second Room Lower South Chest",
        ],
    },
    "Hyrule Castle": {
        "Hyrule Castle Map": [
            "Hyrule Castle East Wing Boomerang Puzzle Chest",
        ],
        "Hyrule Castle Compass": [
            "Hyrule Castle Main Hall Northeast Chest",
        ],
    },
}

VANILLA_GOLDEN_BUG_LOCATIONS = {
    "Female Phasmid": "Bridge of Eldin Female Phasmid",
    "Male Phasmid": "Bridge of Eldin Male Phasmid",
    "Female Grasshopper": "Eldin Field Female Grasshopper",
    "Male Grasshopper": "Eldin Field Male Grasshopper",
    "Female Pill Bug": "Kakariko Gorge Female Pill Bug",
    "Male Pill Bug": "Kakariko Gorge Male Pill Bug",
    "Male Ant": "Kakariko Graveyard Male Ant",
    "Female Ant": "Kakariko Village Female Ant",
    "Female Beetle": "Faron Field Female Beetle",
    "Male Beetle": "Faron Field Male Beetle",
    "Female Snail": "Sacred Grove Female Snail",
    "Male Snail": "Sacred Grove Male Snail",
    "Female Dayfly": "Gerudo Desert Female Dayfly",
    "Male Dayfly": "Gerudo Desert Male Dayfly",
    "Female Mantis": "Lake Hylia Bridge Female Mantis",
    "Male Mantis": "Lake Hylia Bridge Male Mantis",
    "Female Stag Beetle": "Lanayru Field Female Stag Beetle",
    "Male Stag Beetle": "Lanayru Field Male Stag Beetle",
    "Female Ladybug": "Outside South Castle Town Female Ladybug",
    "Male Ladybug": "Outside South Castle Town Male Ladybug",
    "Female Dragonfly": "Upper Zoras River Female Dragonfly",
    "Female Butterfly": "West Hyrule Field Female Butterfly",
    "Male Butterfly": "West Hyrule Field Male Butterfly",
    "Male Dragonfly": "Zoras Domain Male Dragonfly",
}

VANILLA_POE_LOCATIONS = [
    "Arbiters Grounds East Turning Room Poe",
    "Arbiters Grounds Hidden Wall Poe",
    "Arbiters Grounds Torch Room Poe",
    "Arbiters Grounds West Poe",
    "City in The Sky Garden Island Poe",
    "City in The Sky Poe Above Central Fan",
    "Snowpeak Ruins Ice Room Poe",
    "Snowpeak Ruins Lobby Armor Poe",
    "Snowpeak Ruins Lobby Poe",
    "Temple of Time Poe Above Scales",
    "Temple of Time Poe Behind Gate",
    "Death Mountain Trail Poe",
    "Eldin Lantern Cave Poe",
    "Hidden Village Poe",
    "Kakariko Gorge Poe",
    "Kakariko Graveyard Grave Poe",
    "Kakariko Graveyard Open Poe",
    "Kakariko Village Bomb Shop Poe",
    "Kakariko Village Watchtower Poe",
    "Faron Field Poe",
    "Faron Mist Poe",
    "Lost Woods Boulder Poe",
    "Lost Woods Waterfall Poe",
    "Sacred Grove Master Sword Poe",
    "Sacred Grove Temple of Time Owl Statue Poe",
    "Bulblin Camp Poe",
    "Cave of Ordeals Floor 17 Poe",
    "Cave of Ordeals Floor 33 Poe",
    "Cave of Ordeals Floor 44 Poe",
    "Gerudo Desert East Poe",
    "Gerudo Desert North Peahat Poe",
    "Gerudo Desert Poe Above Cave of Ordeals",
    "Gerudo Desert Rock Grotto First Poe",
    "Gerudo Desert Rock Grotto Second Poe",
    "Outside Arbiters Grounds Poe",
    "Outside Bulblin Camp Poe",
    "East Castle Town Bridge Poe",
    "Flight By Fowl Ledge Poe",
    "Hyrule Field Amphitheater Poe",
    "Isle of Riches Poe",
    "Jovani House Poe",
    "Lake Hylia Alcove Poe",
    "Lake Hylia Bridge Cliff Poe",
    "Lake Hylia Dock Poe",
    "Lake Hylia Tower Poe",
    "Lake Lantern Cave Final Poe",
    "Lake Lantern Cave First Poe",
    "Lake Lantern Cave Second Poe",
    "Lanayru Field Bridge Poe",
    "Lanayru Field Poe Grotto Left Poe",
    "Lanayru Field Poe Grotto Right Poe",
    "Outside South Castle Town Poe",
    "Upper Zoras River Poe",
    "Zoras Domain Mother and Child Isle Poe",
    "Zoras Domain Waterfall Poe",
    "Snowpeak Above Freezard Grotto Poe",
    "Snowpeak Blizzard Poe",
    "Snowpeak Cave Ice Poe",
    "Snowpeak Icy Summit Poe",
    "Snowpeak Poe Among Trees",
]

VANILLA_SKY_CHARACTER_LOCATIONS = [
    "Kakariko Gorge Owl Statue Sky Character",
    "Bridge of Eldin Owl Statue Sky Character",
    "Faron Woods Owl Statue Sky Character",
    "Gerudo Desert Owl Statue Sky Character",
    "Hyrule Field Amphitheater Owl Statue Sky Character",
    "Lake Hylia Bridge Owl Statue Sky Character",
]


def generate_itempool(world: "TPWorld") -> None:
    multiworld = world.multiworld

    pool, precollected_items = get_pool_core(world)

    for item in precollected_items:
        multiworld.push_precollected(item_factory(item, world))

    items = item_factory(pool, world)
    multiworld.random.shuffle(items)

    multiworld.itempool.extend(items)


def get_pool_core(world: "TPWorld") -> Tuple[List[str], List[str]]:
    pool: List[str] = []
    precollected_items: List[str] = []
    # n_pending_junk: int = location_count

    # Split items into four different pools: prefill, progression, useful, and filler.
    prefill_pool: list[str] = []
    progression_pool: list[str] = []
    useful_pool: list[str] = []
    filler_pool: list[str] = []

    for item, data in ITEM_TABLE.items():
        # Catch items that need special handling
        if data.code != None and item not in ["Victory", "Ice Trap"]:
            if (
                item == "Hyrule Castle Big Key"
                and world.options.castle_bk_requirements.value
                != CastleBKRequirements.option_none
            ):
                continue  # already handled in place deterministic
            # Prefill check
            if (
                (
                    item in item_name_groups["Small Keys"]
                    and world.options.small_key_settings.in_dungeon
                )
                or (
                    item in item_name_groups["Big Keys"]
                    and (
                        world.options.big_key_settings.in_dungeon
                        or (
                            item == "Hyrule Castle Big Key"
                            and world.options.castle_bk_requirements.value
                            != CastleBKRequirements.option_none
                        )
                    )
                )
                or (
                    item in item_name_groups["Maps and Compasses"]
                    and world.options.map_and_compass_settings.in_dungeon
                )
                or (
                    item in item_name_groups["Bugs"]
                    and world.options.golden_bugs_shuffled.value
                    == GoldenBugsShuffled.option_false
                )
                or (
                    item == "Poe Soul"
                    and world.options.poe_shuffled.value == PoeShuffled.option_false
                )
                or (
                    item == "Progressive Sky Book"
                    and world.options.sky_characters_shuffled.value
                    == SkyCharactersShuffled.option_false
                )
                or (
                    item in item_name_groups["Boss items"]
                    and world.options.dungeon_rewards_progression.value
                    == DungeonRewardsProgression.option_vanilla
                )
            ):
                prefill_pool.extend([item] * data.quantity)
                continue

            # Start-with items
            if (
                (
                    item in item_name_groups["Small Keys"]
                    and world.options.small_key_settings.value
                    == DungeonItem.option_startwith
                )
                or (
                    item in ["Gate Keys", "Gerudo Desert Bulblin Camp Key"]
                    and world.options.small_key_settings.value
                    == DungeonItem.option_startwith
                )
                or (
                    item in item_name_groups["Big Keys"]
                    and world.options.big_key_settings.value
                    == DungeonItem.option_startwith
                )
                or (
                    item in item_name_groups["Maps and Compasses"]
                    and world.options.map_and_compass_settings.value
                    == DungeonItem.option_startwith
                )
            ):
                precollected_items.extend([item] * data.quantity)
                continue

            # Other items get shuffled normally so sort by classification into pools
            adjusted_classification = world.determine_item_classification(item)
            classification = (
                data.classification
                if adjusted_classification is None
                else adjusted_classification
            )

            if classification & IC.progression:
                progression_pool.extend([item] * data.quantity)
            elif classification & IC.useful:
                useful_pool.extend([item] * data.quantity)
            else:
                filler_pool.extend([item] * data.quantity)

        else:
            assert (item in ["Victory", "Ice Trap"]) or (
                item in PortalItems
            ), f"[Twilight Princess] {item}"

    progression_pool.extend(world.pre_pool)

    # Get the number of locations that have not been filled yet
    placeable_locations = [
        location
        for location in world.multiworld.get_locations(world.player)
        if location.address is not None and location.item is None
    ]

    num_items_left_to_place = len(placeable_locations) - len(prefill_pool)

    world.progression_pool.extend(progression_pool)
    pool.extend(progression_pool)
    num_items_left_to_place -= len(progression_pool)

    # For Sky characters vanilla, 1 item placed into precollected (in-prefill) so increase filler count
    if (
        world.options.sky_characters_shuffled.value
        == SkyCharactersShuffled.option_false
    ):
        num_items_left_to_place += 1

    world.multiworld.random.shuffle(useful_pool)
    world.multiworld.random.shuffle(filler_pool)
    world.useful_pool = useful_pool
    world.filler_pool = filler_pool
    world.prefill_pool = prefill_pool
    pre_fill_copy = prefill_pool.copy()
    # go through all pre fill dungeon items and add item if precollected
    for pre_item in [
        item
        for item in world.multiworld.precollected_items[world.player]
        if item.name in item_name_groups["Dungeon Items"]
    ]:
        for fill_item in pre_fill_copy:
            if pre_item.name == fill_item:
                # remove to counter repeats, also break
                num_items_left_to_place += 1
                pre_fill_copy.remove(fill_item)
                break

    assert len(world.useful_pool) > 0, f"[Twilight Princess] {len(world.useful_pool)=}"
    assert len(world.filler_pool) > 0, f"[Twilight Princess] {len(world.filler_pool)=}"

    # Place filler items ensure that the pool has the correct number of items.
    pool.extend([world.get_filler_item_name() for _ in range(num_items_left_to_place)])

    return pool, precollected_items


# Used to fill out boss defeat events and result used to fill out prefill Collection State
def get_boss_defeat_items(world: "TPWorld"):
    return {
        "Diababa": TPItem(
            "Diababa Defeated",
            world.player,
            TPItemData(
                code=None,
                type="Boss Defeated",
                quantity=1,
                classification=(IC.progression),
                item_id=1,
            ),
        ),
        "Fyrus": TPItem(
            "Fyrus Defeated",
            world.player,
            TPItemData(
                code=None,
                type="Boss Defeated",
                quantity=1,
                classification=(IC.progression),
                item_id=1,
            ),
        ),
        "Morpheel": TPItem(
            "Morpheel Defeated",
            world.player,
            TPItemData(
                code=None,
                type="Boss Defeated",
                quantity=1,
                classification=(IC.progression),
                item_id=1,
            ),
        ),
        "Stallord": TPItem(
            "Stallord Defeated",
            world.player,
            TPItemData(
                code=None,
                type="Boss Defeated",
                quantity=1,
                classification=(IC.progression),
                item_id=1,
            ),
        ),
        "Blizzeta": TPItem(
            "Blizzeta Defeated",
            world.player,
            TPItemData(
                code=None,
                type="Boss Defeated",
                quantity=1,
                classification=(IC.progression),
                item_id=1,
            ),
        ),
        "Armogohma": TPItem(
            "Armogohma Defeated",
            world.player,
            TPItemData(
                code=None,
                type="Boss Defeated",
                quantity=1,
                classification=(IC.progression),
                item_id=1,
            ),
        ),
        "Argorok": TPItem(
            "Argorok Defeated",
            world.player,
            TPItemData(
                code=None,
                type="Boss Defeated",
                quantity=1,
                classification=(IC.progression),
                item_id=1,
            ),
        ),
        "Zant": TPItem(
            "Zant Defeated",
            world.player,
            TPItemData(
                code=None,
                type="Boss Defeated",
                quantity=1,
                classification=(IC.progression),
                item_id=1,
            ),
        ),
    }


def place_deterministic_items(world: "TPWorld") -> None:
    """This function places items that are: not shuffled, only part of logic, or are used for the spoiler log."""

    # Place a "Victory" item on "Defeat Ganondorf" for the spoiler log.
    world.get_location("Hyrule Castle Ganondorf").place_locked_item(
        item_factory("Victory", world)
    )

    if world.options.castle_bk_requirements.value != CastleBKRequirements.option_none:
        world.get_location("Hyrule Castle Big Key Chest").place_locked_item(
            item_factory("Hyrule Castle Big Key", world)
        )

    # Place a Boss Defeated item on the boss rooms
    set_rule(
        world.get_location("Forest Temple Diababa"),
        lambda state: (can_defeat_Diababa(state, world.player)),
    )

    world.get_location("Forest Temple Diababa").place_locked_item(
        world.boss_defeat_items["Diababa"]
    )
    set_rule(
        world.get_location("Goron Mines Fyrus"),
        lambda state: (can_defeat_Fyrus(state, world.player)),
    )
    world.get_location("Goron Mines Fyrus").place_locked_item(
        world.boss_defeat_items["Fyrus"]
    )
    set_rule(
        world.get_location("Lakebed Temple Morpheel"),
        lambda state: (can_defeat_Morpheel(state, world.player)),
    )
    world.get_location("Lakebed Temple Morpheel").place_locked_item(
        world.boss_defeat_items["Morpheel"]
    )
    set_rule(
        world.get_location("Arbiters Grounds Stallord"),
        lambda state: (can_defeat_Stallord(state, world.player)),
    )
    world.get_location("Arbiters Grounds Stallord").place_locked_item(
        world.boss_defeat_items["Stallord"]
    )
    set_rule(
        world.get_location("Snowpeak Ruins Blizzeta"),
        lambda state: (can_defeat_Blizzeta(state, world.player)),
    )
    world.get_location("Snowpeak Ruins Blizzeta").place_locked_item(
        world.boss_defeat_items["Blizzeta"]
    )
    set_rule(
        world.get_location("Temple of Time Armogohma"),
        lambda state: (can_defeat_Armogohma(state, world.player)),
    )
    world.get_location("Temple of Time Armogohma").place_locked_item(
        world.boss_defeat_items["Armogohma"]
    )
    set_rule(
        world.get_location("City in The Sky Argorok"),
        lambda state: (can_defeat_Argorok(state, world.player)),
    )
    world.get_location("City in The Sky Argorok").place_locked_item(
        world.boss_defeat_items["Argorok"]
    )
    set_rule(
        world.get_location("Palace of Twilight Zant"),
        lambda state: (can_defeat_Zant(state, world.player)),
    )
    world.get_location("Palace of Twilight Zant").place_locked_item(
        world.boss_defeat_items["Zant"]
    )

    # Manually deal with quest locations. Place item or green ruppee
    # # Also precollect or shuffled the choosen item
    if world.options.ilia_quest.value == IliaQuest.option_vanilla:
        item = world.create_item("Renado's Letter")
    else:
        item = world.create_item("Green Rupee")
        if world.options.ilia_quest.value == IliaQuest.option_letter:
            world.pre_pool.append("Renado's Letter")
        else:
            world.push_precollected(world.create_item("Renado's Letter"))

    world.get_location("Renados Letter").place_locked_item(item)
    del item

    if world.options.ilia_quest.value in [
        IliaQuest.option_vanilla,
        IliaQuest.option_letter,
    ]:
        item = world.create_item("Invoice")
    else:
        item = world.create_item("Green Rupee")
        if world.options.ilia_quest.value == IliaQuest.option_invoice:
            world.pre_pool.append("Invoice")
        else:
            world.push_precollected(world.create_item("Invoice"))
    world.get_location("Telma Invoice").place_locked_item(item)
    del item

    if world.options.ilia_quest.value in [
        IliaQuest.option_vanilla,
        IliaQuest.option_letter,
        IliaQuest.option_invoice,
    ]:
        item = world.create_item("Wooden Statue")
    else:
        item = world.create_item("Green Rupee")
        if world.options.ilia_quest.value == IliaQuest.option_statue:
            world.pre_pool.append("Wooden Statue")
        else:
            world.push_precollected(world.create_item("Wooden Statue"))

    world.get_location("Wooden Statue").place_locked_item(item)
    del item

    if world.options.ilia_quest.value != IliaQuest.option_charm:
        item = world.create_item("Ilias Charm")
    else:
        item = world.create_item("Green Rupee")
        world.pre_pool.append("Ilias Charm")

    world.get_location("Ilia Charm").place_locked_item(item)
    del item
    #
    #
    #
    #
    #
    menu = world.get_region(world.origin_region_name)

    # Ordonn Portal
    world.get_location("Ordon Spring Portal").place_locked_item(
        world.create_item("Ordon Spring Portal")
    )
    set_rule(
        world.get_location("Ordon Spring Portal"),
        lambda state: state._tp_open_map(world.player)
        or (
            not state._tp_open_map(world.player)
            and any(
                [
                    state.can_reach_region(region, world.player)
                    for region in RoomFunctions.OrdonaMapRooms
                ]
            )
        ),
    )

    world.create_entrance(
        menu,
        world.get_region("Ordon Spring"),
        lambda state: (
            can_use(state, world.player, "Ordon Spring Portal")
            and can_use(state, world.player, "Shadow Crystal")
        ),
        "Menu -> Ordon Spring",
    )

    # South Faron Portal
    world.get_location("South Faron Portal").place_locked_item(
        world.create_item("South Faron Portal")
    )
    set_rule(
        world.get_location("South Faron Portal"),
        lambda state: state._tp_open_map(world.player)
        or (
            not state._tp_open_map(world.player)
            and any(
                [
                    state.can_reach_region(region, world.player)
                    for region in RoomFunctions.FaronMapRooms
                ]
            )
        ),
    )

    world.create_entrance(
        menu,
        world.get_region("South Faron Woods"),
        lambda state: (
            can_use(state, world.player, "South Faron Portal")
            and can_use(state, world.player, "Shadow Crystal")
        ),
        "Menu -> South Faron Woods",
    )

    # North Faron Woods Portal
    world.get_location("North Faron Portal").place_locked_item(
        world.create_item("North Faron Portal")
    )
    set_rule(
        world.get_location("North Faron Portal"),
        lambda state: state._tp_open_map(world.player)
        or (
            not state._tp_open_map(world.player)
            and any(
                [
                    state.can_reach_region(region, world.player)
                    for region in RoomFunctions.FaronMapRooms
                ]
            )
        ),
    )

    world.create_entrance(
        menu,
        world.get_region("North Faron Woods"),
        lambda state: (
            can_use(state, world.player, "North Faron Portal")
            and can_use(state, world.player, "Shadow Crystal")
        ),
        "Menu -> North Faron Woods",
    )

    world.get_location("Zoras Domain Portal").place_locked_item(
        world.create_item("Zoras Domain Portal")
    )
    set_rule(
        world.get_location("Zoras Domain Portal"),
        lambda state: state._tp_open_map(world.player)
        or (
            not state._tp_open_map(world.player)
            and any(
                [
                    state.can_reach_region(region, world.player)
                    for region in RoomFunctions.LanayruMapRooms
                ]
            )
        ),
    )

    world.create_entrance(
        menu,
        world.get_region("Zoras Domain Throne Room"),
        lambda state: (
            can_use(state, world.player, "Zoras Domain Portal")
            and can_use(state, world.player, "Shadow Crystal")
        ),
        "Menu -> Zoras Domain Throne Room",
    )

    world.get_location("Castle Town Portal").place_locked_item(
        world.create_item("Castle Town Portal")
    )
    set_rule(
        world.get_location("Castle Town Portal"),
        lambda state: state._tp_open_map(world.player)
        or (
            not state._tp_open_map(world.player)
            and any(
                [
                    state.can_reach_region(region, world.player)
                    for region in RoomFunctions.LanayruMapRooms
                ]
            )
        ),
    )

    world.create_entrance(
        menu,
        world.get_region("Outside Castle Town West"),
        lambda state: (
            can_use(state, world.player, "Castle Town Portal")
            and can_use(state, world.player, "Shadow Crystal")
        ),
        "Menu -> Outside Castle Town West",
    )

    world.get_location("Lake Hylia Portal").place_locked_item(
        world.create_item("Lake Hylia Portal")
    )
    set_rule(
        world.get_location("Lake Hylia Portal"),
        lambda state: state._tp_open_map(world.player)
        or (
            not state._tp_open_map(world.player)
            and any(
                [
                    state.can_reach_region(region, world.player)
                    for region in RoomFunctions.LanayruMapRooms
                ]
            )
        ),
    )

    world.create_entrance(
        menu,
        world.get_region("Lake Hylia"),
        lambda state: (
            can_use(state, world.player, "Lake Hylia Portal")
            and can_use(state, world.player, "Shadow Crystal")
        ),
        "Menu -> Lake Hylia",
    )

    world.get_location("Kakariko Gorge Portal").place_locked_item(
        world.create_item("Kakariko Gorge Portal")
    )
    set_rule(
        world.get_location("Kakariko Gorge Portal"),
        lambda state: state._tp_open_map(world.player)
        or (
            not state._tp_open_map(world.player)
            and any(
                [
                    state.can_reach_region(region, world.player)
                    for region in RoomFunctions.EldinMapRooms
                ]
            )
        ),
    )

    world.create_entrance(
        menu,
        world.get_region("Kakariko Gorge"),
        lambda state: (
            can_use(state, world.player, "Kakariko Gorge Portal")
            and can_use(state, world.player, "Shadow Crystal")
        ),
        "Menu -> Kakariko Gorge",
    )

    world.get_location("Kakariko Village Portal").place_locked_item(
        world.create_item("Kakariko Village Portal")
    )
    set_rule(
        world.get_location("Kakariko Village Portal"),
        lambda state: state._tp_open_map(world.player)
        or (
            not state._tp_open_map(world.player)
            and any(
                [
                    state.can_reach_region(region, world.player)
                    for region in RoomFunctions.EldinMapRooms
                ]
            )
        ),
    )

    world.create_entrance(
        menu,
        world.get_region("Lower Kakariko Village"),
        lambda state: (
            can_use(state, world.player, "Kakariko Village Portal")
            and can_use(state, world.player, "Shadow Crystal")
        ),
        "Menu -> Lower Kakariko Village",
    )

    world.get_location("Death Mountain Portal").place_locked_item(
        world.create_item("Death Mountain Portal")
    )
    set_rule(
        world.get_location("Death Mountain Portal"),
        lambda state: state._tp_open_map(world.player)
        or (
            not state._tp_open_map(world.player)
            and any(
                [
                    state.can_reach_region(region, world.player)
                    for region in RoomFunctions.EldinMapRooms
                ]
            )
        ),
    )

    world.create_entrance(
        menu,
        world.get_region("Death Mountain Volcano"),
        lambda state: (
            can_use(state, world.player, "Death Mountain Portal")
            and can_use(state, world.player, "Shadow Crystal")
        ),
        "Menu -> Death Mountain Volcano",
    )

    world.get_location("Snowpeak Portal").place_locked_item(
        world.create_item("Snowpeak Portal")
    )
    if world.options.skip_snowpeak_entrance.value:

        set_rule(
            world.get_location("Snowpeak Portal"),
            lambda state: state._tp_open_map(world.player)
            or (
                not state._tp_open_map(world.player)
                and any(
                    [
                        state.can_reach_region(region, world.player)
                        for region in RoomFunctions.SnowpeakMapRooms
                    ]
                )
            ),
        )

        world.create_entrance(
            menu,
            world.get_region("Snowpeak Summit Upper"),
            lambda state: (
                can_use(state, world.player, "Snowpeak Portal")
                and can_use(state, world.player, "Shadow Crystal")
            ),
            "Menu -> Snowpeak Summit Upper",
        )

    # Additional Portals
    # These portal locations are inplace unlocks, so accounting for the portal Travel is usless
    # Techincally they could be unlocked with pre collection but I will ignore that for now
    world.get_location("Upper Zoras River Portal").place_locked_item(
        world.create_item("Upper Zoras River Portal")
    )

    world.get_location("Bridge of Eldin Portal").place_locked_item(
        world.create_item("Bridge of Eldin Portal")
    )

    world.get_location("Sacred Grove Portal").place_locked_item(
        world.create_item("Sacred Grove Portal")
    )

    world.get_location("Mirror Chamber Portal").place_locked_item(
        world.create_item("Mirror Chamber Portal")
    )
    world.get_location("Gerudo Desert Portal").place_locked_item(
        world.create_item("Gerudo Desert Portal")
    )
