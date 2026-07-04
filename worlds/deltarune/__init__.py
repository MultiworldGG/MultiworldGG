from typing import Any, ClassVar, Optional

from BaseClasses import ItemClassification, Tutorial
from Options import Option, OptionError
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, Type, icon_paths
from multiprocessing import Process

from worlds.deltarune.Locations import get_location_groups, locations
from worlds.deltarune.Items import (
    DeltaruneItem,
    ItemData,
    ItemIDs,
    ItemGroups,
    convert_filler_and_trap_to_weights,
    get_item_groups,
    items,
    glitched_item_name,
)
from worlds.deltarune.Goals import set_completion_goal
from worlds.deltarune.Options import (
    DeltaruneOptions,
    deltarune_option_groups,
    options_presets,
    RandomizeChapterOptions,
    ChosenRouteOptions,
    RandomizeSecretBossesOptions,
    RandomizeMANTLEOptions,
    IncludeMikeOptions,
    UnlockCharactersOptions,
    IncludeUnusedItemsOptions,
)
from worlds.deltarune.Regions import Regions
from worlds.deltarune.cross_chapter.Items import (
    get_filler_and_trap_items as get_cross_chapter_filler_and_trap_items,
    create_items as create_cross_chapter_items,
)
from worlds.deltarune.cross_chapter.Rules import (
    set_rules as set_cross_chapter_rules,
    handle_locked_items as handle_cross_chapter_locked_items,
)
from worlds.deltarune.chapter_1.Rules import (
    handle_locked_items as handle_chapter_1_locked_items,
    set_rules as set_chapter_1_rules,
)
from worlds.deltarune.chapter_2.Rules import (
    handle_locked_items as handle_chapter_2_locked_items,
    set_rules as set_chapter_2_rules,
)
from worlds.deltarune.chapter_3.Rules import (
    handle_locked_items as handle_chapter_3_locked_items,
    set_rules as set_chapter_3_rules,
)
from worlds.deltarune.chapter_4.Rules import (
    handle_locked_items as handle_chapter_4_locked_items,
    set_rules as set_chapter_4_rules,
)
from worlds.deltarune.cross_chapter.Regions import create_regions as create_cross_chapter_regions
from worlds.deltarune.chapter_1.Regions import create_regions as create_chapter_1_regions
from worlds.deltarune.chapter_2.Regions import create_regions as create_chapter_2_regions
from worlds.deltarune.chapter_3.Regions import create_regions as create_chapter_3_regions
from worlds.deltarune.chapter_4.Regions import create_regions as create_chapter_4_regions
from worlds.deltarune.cross_chapter.Items import (
    cross_chapter_items,
    create_items as create_cross_chapter_items,
    get_filler_and_trap_items as get_cross_chapter_filler_and_trap_items,
)
from worlds.deltarune.chapter_1.Items import (
    chapter1_items,
    create_items as create_chapter_1_items,
    get_filler_and_trap_items as get_chapter_1_filler_and_trap_items,
)
from worlds.deltarune.chapter_2.Items import (
    chapter2_items,
    create_items as create_chapter_2_items,
    get_filler_and_trap_items as get_chapter_2_filler_and_trap_items,
)
from worlds.deltarune.chapter_3.Items import (
    chapter3_items,
    create_items as create_chapter_3_items,
    get_filler_and_trap_items as get_chapter_3_filler_and_trap_items,
)
from worlds.deltarune.chapter_4.Items import (
    chapter4_items,
    create_items as create_chapter_4_items,
    get_filler_and_trap_items as get_chapter_4_filler_and_trap_items,
)
from worlds.deltarune.chapter_1.Locations import chapter1_locations
from worlds.deltarune.chapter_2.Locations import chapter2_locations
from worlds.deltarune.chapter_3.Locations import chapter3_locations
from worlds.deltarune.chapter_4.Locations import chapter4_locations
from worlds.deltarune.cross_chapter.Locations import cross_chapter_locations
from worlds.deltarune.tracker import handle_auto_tracking, handle_player_icon_position

all_item_data: list[ItemData] = chapter1_items + chapter2_items + chapter3_items + chapter4_items + cross_chapter_items

all_locations = []

for region, location in cross_chapter_locations.items():
    all_locations += location
for region, location in chapter1_locations.items():
    all_locations += location
for region, location in chapter2_locations.items():
    all_locations += location
for region, location in chapter3_locations.items():
    all_locations += location
for region, location in chapter4_locations.items():
    all_locations += location


def run_client():
    print("running deltarune client")
    from .DeltaruneClient import main  # lazy import

    p = Process(target=main)
    p.start()


components.append(
    Component(
        "DELTARUNE Client",
        func=run_client,
        component_type=Type.CLIENT,
        icon="deltarune",
        game_name="DELTARUNE",
        supports_uri=True,
    )
)

# I apologize for the name of the icon - Emerald
icon_paths["deltarune"] = f"ap:{__name__}/icons/gay_deltarune.png"

max_deltarune_chapter = 4
fusion_access_chapter = [2, 4]

def data_path(file_name: str):
    import pkgutil

    return pkgutil.get_data(__name__, "data/" + file_name)


class DeltaruneWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the MultiworldGG DELTARUNE software on your computer. This guide covers "
            "single-player, multiworld, and related software.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Mewlif"],
        )
    ]

    option_groups = deltarune_option_groups
    options_presets = options_presets
    rich_text_options_doc = True


class DeltaruneWorld(World):
    """
    DELTARUNE is an RPG.
    """

    game = "DELTARUNE"
    options_dataclass = DeltaruneOptions
    options: DeltaruneOptions
    web = DeltaruneWeb()

    item_name_to_id = {name: id.value for id, name in items.items()}
    item_name_groups = get_item_groups(all_item_data)

    location_name_to_id = {name: id.value for id, name in locations.items()}
    location_name_groups = get_location_groups(all_locations)

    glitches_item_name = glitched_item_name
    ut_can_gen_without_yaml = True

    origin_region_name = Regions.chapter_select

    cached_filler_and_trap_weights: dict[int, float] = {}

    tracker_world: ClassVar = {
        "map_page_folder": "tracker",
        "map_page_maps": "maps/maps.json",
        "map_page_locations": [
            "locations/chapter1.json",
            "locations/chapter2.json",
            "locations/chapter3.json",
            "locations/chapter4.json",
            "locations/overview.json",
        ],
        "map_page_index": handle_auto_tracking,
        "map_page_setting_key": "{player}_{team}_current_location",
        "location_icon_coords": handle_player_icon_position,
        "location_setting_key": "{player}_{team}_current_location",
    }

    def _get_deltarune_data(self):
        return {
            "options": self.options.as_dict(
                "randomize_secret_bosses",
                "macguffin_chapter_1",
                "macguffin_chapter_2",
                "macguffin_chapter_3",
                "macguffin_chapter_4",
                "macguffin_extra",
                "remove_starting_equipment",
                "include_chapter_1",
                "include_chapter_2",
                "include_chapter_3",
                "include_chapter_4",
                "exclude_t_rank",
                "exclude_z_rank",
                "chosen_route",
                "include_lose_swatchling",
                "exclude_post_chapter_2_locations",
                "randomize_chapters",
                "include_hidden_items",
                "include_secret_bosses_items_requirement",
                "death_link",
                "item_balancing",
                "include_shadow_mantle",
                "randomize_mantle",
                "include_unused_items",
                "include_mike",
                "exclude_mike_platinum",
                "unlock_characters",
                "better_odds",
                "unlock_fun_gang_actions",
                "chapter_1_recruit",
                toggles_as_bools=True,
            ),
            "world_seed": self.random.getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "client_version": self.required_client_version,
            "race": self.multiworld.is_race,
        }

    def create_item(self, name: str) -> DeltaruneItem:
        if name == glitched_item_name:
            return DeltaruneItem(name, ItemClassification.progression, -1, self.player)

        item_data = next((item_data for item_data in all_item_data if items[item_data.code] == name), None)

        if item_data is None:
            raise ValueError(f"Item name '{name}' not found in item data.")

        return DeltaruneItem(name, item_data.classification, item_data.code.value, self.player)

    def get_filler_item_name(self):
        if len(self.cached_filler_and_trap_weights) == 0:
            self.fill_weighted_fillers_and_traps()

        return items[
            self.random.choices(
                list(self.cached_filler_and_trap_weights.keys()),
                weights=list(self.cached_filler_and_trap_weights.values()),
            )[0]
        ]

    def fill_weighted_fillers_and_traps(self):
        filler_pool = get_cross_chapter_filler_and_trap_items(self)

        if self.options.include_chapter_1:
            filler_pool += get_chapter_1_filler_and_trap_items(self)
        if self.options.include_chapter_2:
            filler_pool += get_chapter_2_filler_and_trap_items(self)
        if self.options.include_chapter_3:
            filler_pool += get_chapter_3_filler_and_trap_items(self)
        if self.options.include_chapter_4:
            filler_pool += get_chapter_4_filler_and_trap_items(self)

        self.cached_filler_and_trap_weights = convert_filler_and_trap_to_weights(filler_pool, self.options)

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data

    def fill_slot_data(self):
        return self._get_deltarune_data()

    def generate_early(self) -> None:
        if (
            self.options.randomize_chapters == RandomizeChapterOptions.randomized
            and self.options.starting_chapter.value != 0
        ):
            if getattr(self.options, f"include_chapter_{self.options.starting_chapter.value}").value == 0:
                raise OptionError(
                    f"Your random starting chapter is set to {self.options.starting_chapter.value} but it isn't included"
                )

        if len(self.get_playable_chapters()) == 0:
            raise OptionError("WHAT INTERESTING BEHAVIOR. (You forgot to include at least one chapter to play.)")

        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            slot_options: dict[str, Any] = slot_data.get("options", {})
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_options.items():
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))

    def include_chapter(self, chapter: int) -> bool:
        return getattr(self.options, f"include_chapter_{chapter}").value == 1

    def is_chapters_in_order(self):
        return self.options.randomize_chapters == RandomizeChapterOptions.in_order

    def is_all_chapters_unlocked(self):
        return self.options.randomize_chapters == RandomizeChapterOptions.all_unlocked

    def is_chapters_randomized(self):
        return self.options.randomize_chapters == RandomizeChapterOptions.randomized

    def is_not_weird_route_only(self):
        return self.options.chosen_route != ChosenRouteOptions.weird_route or self.is_all_routes()

    def is_neutral_route(self):
        return self.options.chosen_route == ChosenRouteOptions.neutral_route or self.is_all_routes()

    def is_all_recruits(self):
        return self.options.chosen_route == ChosenRouteOptions.all_recruits or self.is_all_routes()

    def is_weird_route(self):
        return self.options.chosen_route == ChosenRouteOptions.weird_route or self.is_all_routes()

    def is_all_routes(self):
        return self.options.chosen_route == ChosenRouteOptions.all_routes

    def is_starting_equipment_removed(self):
        return self.options.remove_starting_equipment.value == 1

    def is_secret_bosses_randomized(self):
        return (
            self.options.randomize_secret_bosses == RandomizeSecretBossesOptions.true
            or self.is_secret_bosses_mandatory()
        )

    def is_secret_bosses_mandatory(self):
        return self.options.randomize_secret_bosses == RandomizeSecretBossesOptions.mandatory

    def is_mantle_randomized(self):
        return self.options.randomize_mantle == RandomizeMANTLEOptions.true

    def is_mantleless(self):
        return self.options.randomize_mantle == RandomizeMANTLEOptions.mantleless

    def is_shadow_mantle_included(self):
        return self.options.include_shadow_mantle.value == 1

    def is_hidden_items_randomized(self):
        return self.options.include_hidden_items.value == 1

    def is_secret_bosses_items_requirement_randomized(self):
        return self.options.include_secret_bosses_items_requirement.value == 1

    def is_chapter_1_recruit_system_enabled(self):
        return self.options.chapter_1_recruit.value == 1

    def is_mike_battle_included(self):
        return self.options.include_mike == IncludeMikeOptions.battle_only or self.is_mike_games_included()

    def is_mike_games_included(self):
        return self.options.include_mike == IncludeMikeOptions.battle_and_games

    def is_kris_weapons_progressive(self):
        return self.options.progressive_kris_weapons.value == 1

    def is_susie_weapons_progressive(self):
        return self.options.progressive_susie_weapons.value == 1

    def is_ralsei_weapons_progressive(self):
        return self.options.progressive_ralsei_weapons.value == 1

    def is_noelle_weapons_progressive(self):
        return self.options.progressive_noelle_weapons.value == 1 and self.include_chapter(2)

    def is_characters_unlockables(self):
        return (
            self.options.unlock_characters == UnlockCharactersOptions.true
            or self.options.unlock_characters == UnlockCharactersOptions.except_kris
        )

    def is_kris_unlockable(self):
        return self.options.unlock_characters == UnlockCharactersOptions.true

    def is_fun_gang_actions_unlockable(self):
        return self.options.unlock_fun_gang_actions.value == 1

    def is_unused_items_included(self):
        return (
            self.options.include_unused_items == IncludeUnusedItemsOptions.true_without_everybodyweapon
            or self.is_everybodyweapon_included()
        )

    def is_everybodyweapon_included(self):
        return self.options.include_unused_items == IncludeUnusedItemsOptions.true

    # Check if you have at least one chapter that give you access to fusions
    def can_access_fusion(self) -> bool:
        result = self.has_at_least_one_chapter_included(fusion_access_chapter)
        return result

    def count_chapter_included(self, chapters=list(range(1, max_deltarune_chapter + 1))):
        count = 0
        for chapterToCheck in chapters:
            if getattr(self.options, f"include_chapter_{chapterToCheck}").value == 1:
                count += 1
        return count

    # Check if at least one of specified chapters is included
    def has_at_least_one_chapter_included(self, chapters: list[int]) -> bool:
        return any(getattr(self.options, f"include_chapter_{chapter}").value == 1 for chapter in chapters)

    def have_all_chapters_included(self, chapters: list[int]) -> bool:
        return all(getattr(self.options, f"include_chapter_{chapter}").value == 1 for chapter in chapters)

    def get_first_chapter(self) -> int:
        for chapterToCheck in range(1, max_deltarune_chapter + 1, 1):
            if self.include_chapter(chapterToCheck):
                return chapterToCheck
        return -1

    def get_playable_chapters(self) -> list[int]:
        playable_chapters = []
        for chapterToCheck in range(1, max_deltarune_chapter + 1, 1):
            if getattr(self.options, f"include_chapter_{chapterToCheck}"):
                playable_chapters.append(chapterToCheck)
        return playable_chapters

    def get_previous_in_order_chapter(self, chapter: int):
        if chapter <= 1:
            return -1

        for chapterToCheck in range(chapter - 1, 0, -1):
            if getattr(self.options, f"include_chapter_{chapterToCheck}"):
                return chapterToCheck

        return -1

    def is_t_rank_excluded(self):
        return self.options.exclude_t_rank == 1

    def is_z_rank_excluded(self):
        return self.options.exclude_z_rank == 1

    def get_next_in_order_chapter(self, chapter: int):
        if chapter > max_deltarune_chapter:
            return -1

        for chapterToCheck in range(chapter + 1, max_deltarune_chapter + 1, 1):
            if getattr(self.options, f"include_chapter_{chapterToCheck}"):
                return chapterToCheck

        return -1

    def create_regions(self):
        # every_connections = CCLocationsAndRegions.get_cross_chapter_mandatory_connection(self)

        create_cross_chapter_regions(self)
        if self.include_chapter(1):
            create_chapter_1_regions(self)
        if self.include_chapter(2):
            create_chapter_2_regions(self)
        if self.include_chapter(3):
            create_chapter_3_regions(self)
        if self.include_chapter(4):
            create_chapter_4_regions(self)
        # if self.include_chapter(5): Ch5LocationAndRegions.create_regions(self)
        # if self.include_chapter(6): Ch6LocationAndRegions.create_regions(self)
        # if self.include_chapter(7): Ch7LocationAndRegions.create_regions(self)

    def create_items(self):
        if self.get_playable_chapters() == []:
            self.multiworld.push_precollected(self.create_item(items[ItemIDs.what_interesting_behavior]))
            return

        item_pool: list[ItemData] = []

        item_pool += create_cross_chapter_items(self)
        handle_cross_chapter_locked_items(self)
        if self.include_chapter(1):
            item_pool += create_chapter_1_items(self)
            handle_chapter_1_locked_items(self)
        if self.include_chapter(2):
            item_pool += create_chapter_2_items(self)
            handle_chapter_2_locked_items(self)
        if self.include_chapter(3):
            item_pool += create_chapter_3_items(self)
            handle_chapter_3_locked_items(self)
        if self.include_chapter(4):
            item_pool += create_chapter_4_items(self)
            handle_chapter_4_locked_items(self)
        # if self.include_chapter(5): Ch5Items.create_items(self)
        # if self.include_chapter(6): Ch6Items.create_items(self)
        # if self.include_chapter(7): Ch7Items.create_items(self)

        if self.is_kris_weapons_progressive():
            self.handle_progressive_weapon(item_pool, ItemGroups.kris_weapons)
        if self.is_susie_weapons_progressive():
            self.handle_progressive_weapon(item_pool, ItemGroups.susie_weapons)
        if self.is_ralsei_weapons_progressive():
            self.handle_progressive_weapon(item_pool, ItemGroups.ralsei_weapons)
        if self.is_noelle_weapons_progressive():
            self.handle_progressive_weapon(item_pool, ItemGroups.noelle_weapons)

        self.handle_chapter_keys(item_pool)
        self.handle_macguffins_items(item_pool)

        item_pool_names_and_amounts = []

        for item_data in item_pool:
            item_pool_names_and_amounts += [items[item_data.code]] * item_data.amount

        item_pool_converted = [self.create_item(item) for item in item_pool_names_and_amounts]
        self.handle_item_unfill_and_overflows(item_pool_converted)

        self.multiworld.itempool += item_pool_converted

    def handle_macguffins_items(self, item_pool: list[ItemData]):
        if self.include_chapter(1):
            item_data = next(
                (item_data for item_data in item_pool if item_data.code == ItemIDs.king_shape_key_piece), None
            )
            index = item_pool.index(item_data)
            item_pool[index] = item_data._replace(
                amount=self.options.macguffin_chapter_1.value + self.options.macguffin_extra.value
            )
        if self.include_chapter(2):
            item_data = next((item_data for item_data in item_pool if item_data.code == ItemIDs.keygen_2_segment), None)
            index = item_pool.index(item_data)
            item_pool[index] = item_data._replace(
                amount=self.options.macguffin_chapter_2.value + self.options.macguffin_extra.value
            )
        if self.include_chapter(3):
            item_data = next((item_data for item_data in item_pool if item_data.code == ItemIDs.remote_battery), None)
            index = item_pool.index(item_data)
            item_pool[index] = item_data._replace(
                amount=self.options.macguffin_chapter_3.value + self.options.macguffin_extra.value
            )
        if self.include_chapter(4):
            item_data = next(
                (item_data for item_data in item_pool if item_data.code == ItemIDs.combination_lock_digit), None
            )
            index = item_pool.index(item_data)
            item_pool[index] = item_data._replace(
                amount=self.options.macguffin_chapter_4.value + self.options.macguffin_extra.value
            )

    def handle_chapter_keys(self, item_pool: list[ItemData]):
        if self.is_all_chapters_unlocked():
            return

        starting_chapter = -1

        if self.is_chapters_in_order():
            starting_chapter = self.get_first_chapter()
        elif self.is_chapters_randomized():
            if self.options.starting_chapter.value == 0:
                starting_chapter = self.random.choice(self.get_playable_chapters())
            else:
                starting_chapter = self.options.starting_chapter.value

        if starting_chapter == -1:
            return

        item_name = f"Chapter {starting_chapter} Unlock"

        if self.is_chapters_randomized():
            item_id = self.item_name_to_id[item_name]
            item_pool.remove(next((item_data for item_data in item_pool if item_data.code == item_id), None))

        self.multiworld.push_precollected(self.create_item(item_name))

    def handle_item_unfill_and_overflows(self, item_pool: list[DeltaruneItem]):
        # Remove random junk items if the item pool overflows
        if len(item_pool) > len(self.multiworld.get_unfilled_locations(self.player)):
            print(f"Item pool overflow: {len(item_pool) - len(self.multiworld.get_unfilled_locations(self.player))}")
            while len(item_pool) > len(self.multiworld.get_unfilled_locations(self.player)):
                item_pool.remove(
                    self.random.choice(
                        [
                            item
                            for item in item_pool
                            if item.classification == ItemClassification.filler
                            or item.classification == ItemClassification.trap
                        ]
                    )
                )

        # Fill remaining items with randomly generated junk
        while len(item_pool) < len(self.multiworld.get_unfilled_locations(self.player)):
            item_pool.append(self.create_filler())

    def set_rules(self):
        set_cross_chapter_rules(self)
        if self.include_chapter(1):
            set_chapter_1_rules(self)
        if self.include_chapter(2):
            set_chapter_2_rules(self)
        if self.include_chapter(3):
            set_chapter_3_rules(self)
        if self.include_chapter(4):
            set_chapter_4_rules(self)
        # if self.include_chapter(5): set_chapter_5_rules(self)
        # if self.include_chapter(6): set_chapter_6_rules(self)
        # if self.include_chapter(7): set_chapter_7_rules(self)

        set_completion_goal(self)

        # from Utils import visualize_regions

        # state = self.multiworld.get_all_state(False)
        # state.update_reachable_regions(self.player)
        # visualize_regions(self.get_region(self.origin_region_name), f"deltarune_regions{self.player}.puml")

    def handle_progressive_weapon(
        self,
        itempool: list[ItemData],
        character: ItemGroups,
    ):
        weapons_character_in_pool = [
            item for item in itempool if character in item.groups and item.classification != ItemClassification.filler
        ]

        # Remove them from the item pool
        for weapon in weapons_character_in_pool:
            itempool.remove(weapon)

        match character:
            case ItemGroups.kris_weapons:
                itempool += [
                    ItemData(
                        ItemIDs.progressive_kris_weapons,
                        ItemClassification.useful,
                        groups=[ItemGroups.weapons, ItemGroups.kris_weapons],
                        amount=len(weapons_character_in_pool),
                    )
                ]
            case ItemGroups.susie_weapons:
                itempool += [
                    ItemData(
                        ItemIDs.progressive_susie_weapons,
                        ItemClassification.useful,
                        groups=[ItemGroups.weapons, ItemGroups.susie_weapons],
                        amount=len(weapons_character_in_pool),
                    )
                ]
            case ItemGroups.ralsei_weapons:
                itempool += [
                    ItemData(
                        ItemIDs.progressive_ralsei_weapons,
                        ItemClassification.useful,
                        groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons],
                        amount=len(weapons_character_in_pool),
                    )
                ]
            case ItemGroups.noelle_weapons:
                itempool += [
                    ItemData(
                        ItemIDs.progressive_noelle_weapons,
                        ItemClassification.useful | ItemClassification.progression,
                        groups=[ItemGroups.weapons, ItemGroups.noelle_weapons],
                        amount=len(weapons_character_in_pool),
                    )
                ]
            case _:
                raise ValueError("Invalid character for progressive weapon")
