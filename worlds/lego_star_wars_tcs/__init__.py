import json
import logging
from collections import Counter
from typing import Mapping, Any, NoReturn, Callable, ClassVar, TextIO, Iterable

from BaseClasses import (
    Region,
    ItemClassification,
    CollectionState,
    Location,
    Entrance,
    Tutorial,
    Item,
    MultiWorld,
)
from Options import OptionError
from rule_builder.rules import Rule, Has
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import components, Component, launch, Type
from worlds.generic.Rules import CollectionRule

from . import constants, regions, item_pool
from .character_ability import CharacterAbility
from .constants import GOLD_BRICK_EVENT_NAME, GAME_NAME, SETTINGS_KEY
from .data.areas import Area
from .data.bosses import Boss
from .data.extras import Extra
from .data.items.generic_items import MINIKITS_BY_NAME
from .items import (
    ITEM_NAME_TO_ID,
    LegoStarWarsTCSItem,
    SUPER_GONK_ITEMS,
    SUPER_GONK_DROID_ABILITIES_VALUE,
)
from .item_classification import evaluate_effective_item
from .locations import LegoStarWarsTCSLocation, LegoStarWarsTCSShopLocation
from .host_yaml_settings import LegoStarWarsTCSSettings
from .options import LegoStarWarsTCSOptions, OPTION_GROUPS
from .option_resolution.common import resolve_options
from .option_resolution.universal_tracker import UTAttribute
from .slot_data import TCSSlotDataOptions
from .item_groups import ITEM_GROUPS, REVERSE_READABLE_ABILITY_TO_ABILITY

from .data.characters import Character
from .data.levels import SAVE_DATA_MINIKITS_ELEMENT_SIZE
from .data.locations import LOCATION_NAME_TO_ID, LOCATION_GROUPS
from .data_storage import (
    COMPLETED_FREE_PLAY_KEY,
    COMPLETED_TRUE_JEDI_KEY,
    COMPLETED_10_MINIKITS_KEY,
    COMPLETED_BONUSES_KEY,
    COLLECTED_POWER_BRICKS_KEY,
    MINIKIT_GOAL_SUBMITTED_KEY,
)

# 1 byte to write the length
SLOT_NAME_MAX_BYTES = SAVE_DATA_MINIKITS_ELEMENT_SIZE - 1
MULTIWORLD_SEED_NAME_MAX_BYTES = SAVE_DATA_MINIKITS_ELEMENT_SIZE - 1

__all__ = [
    "TCSUniversalTrackerAPWorldVersionMismatchError",
    "LegoStarWarsTCSWebWorld",
    "LegoStarWarsTCSWorld",
]


def launch_client(*args: str):
    # Lazy import. Generation does not need to even load client modules, it would just be a waste of memory.
    from .client import launch as run_client
    launch(run_client, name="LegoStarWarsTheCompleteSagaClient", args=args)


components.append(Component("Lego Star Wars: The Complete Saga Client",
                            func=launch_client,
                            supports_uri=True,
                            game_name=GAME_NAME,
                            component_type=Type.CLIENT,
                            description=f"APWorld Version {'.'.join(map(str, constants.AP_WORLD_VERSION))}"
))


class TCSUniversalTrackerAPWorldVersionMismatchError(Exception):
    """
    Raised when Universal Tracker attempts to connect to a multiworld generated with a different APWorld version to the
    client's APWorld version.
    """


class LegoStarWarsTCSWebWorld(WebWorld):
    theme = "partyTime"
    option_groups = OPTION_GROUPS
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up Lego Star Wars: The Complete Saga to be played in MultiworldGG.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Mysteryem"]
    )]


logger = logging.getLogger("Lego Star Wars TCS")


class LegoStarWarsTCSWorld(World):
    """
    Lego Star Wars: The Complete Saga is a 2007 compilation of the all Lego Star Wars series games.
    The game follows the events of the first six episodes of the Skywalker Saga from a third-person perspective 
    of the 3D game world modeled after the Lego Star Wars line of construction toys.
    """

    game = constants.GAME_NAME
    web = LegoStarWarsTCSWebWorld()
    options: LegoStarWarsTCSOptions
    options_dataclass = LegoStarWarsTCSOptions

    settings_key = SETTINGS_KEY
    settings: ClassVar[LegoStarWarsTCSSettings]

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS

    origin_region_name = "Cantina"

    # Universal Tracker 0.2.12 or newer is required because the game name contains a colon.
    # noinspection PyClassVar
    ut_can_gen_without_yaml: ClassVar[bool] = UTAttribute(True, class_var=True, ut_api=True)
    glitches_item_name: str = UTAttribute("UT_GLITCHED", ut_api=True)
    # Custom item name for use in UT with `/manually_collect` to adjust glitched logic to show all higher difficulties.
    glitches_all_item_name: str = UTAttribute("UT_GLITCHED_ALL")
    ut_disconnected_free_play_completion_events: dict[Area, tuple[Entrance, Region]] = UTAttribute()
    ut_disconnected_true_jedi_gold_brick_events: dict[Area, tuple[Entrance, Region]] = UTAttribute()
    ut_disconnected_10_minikits_gold_brick_events: dict[Area, tuple[Entrance, Region]] = UTAttribute()
    ut_disconnected_bonus_completion_events: dict[Area, tuple[Entrance, Region]] = UTAttribute()
    ut_disconnected_power_brick_events: dict[Area, tuple[Entrance, Region]] = UTAttribute()
    ut_disconnected_boss_events: dict[Area, tuple[Entrance, Region]] = UTAttribute()
    ut_datastorage_key_to_disconnected_dict: dict[str, Iterable[dict[Area, tuple[Entrance, Region]]]] = UTAttribute()
    ut_minikit_goal_submitted_key: str = UTAttribute()
    ut_minikit_goal_disconnected_entrance: tuple[Entrance, Region] | None  = UTAttribute(None)
    found_entrances_datastorage_key: tuple[str, ...] = UTAttribute(
        (
            COMPLETED_FREE_PLAY_KEY,
            COMPLETED_TRUE_JEDI_KEY,
            COMPLETED_10_MINIKITS_KEY,
            COMPLETED_BONUSES_KEY,
            COLLECTED_POWER_BRICKS_KEY,
            MINIKIT_GOAL_SUBMITTED_KEY,
        ),
        ut_api=True,
    )

    PROG_USEFUL_LEVEL_ACCESS_THRESHOLD_PERCENT: ClassVar[float] = 1/6
    prog_useful_level_access_threshold_count: int = 6
    character_chapter_access_counts: Counter[Character]

    starting_character_abilities: CharacterAbility = CharacterAbility.NONE

    # The effective abilities of each character, minus logically irrelevant abilities and abilities provided by
    # precollected characters. Used to determine the correct ItemClassification for character items.
    effective_character_abilities: dict[str, CharacterAbility] | None = None
    # The maximum logically relevant counts of each item, minus the counts of precollected items. Used to determine the
    # correct ItemClassification for items.
    logical_item_counts: Counter[str] | None = None

    enabled_chapters: set[Area]
    enabled_chapters_with_locations: set[Area]  # Includes the Goal Chapter when it has locations.
    enabled_non_goal_chapters: set[Area]
    enabled_episodes: set[int]
    enabled_bonuses: set[Area]
    enabled_bosses: set[Area]
    boss_area_to_boss: dict[Area, Boss]
    goal_chapter: Area | None
    chapters_requiring_alt_characters: set[Area]
    chapter_required_character_counts: dict[Area, int]
    chapter_extra_random_character_counts: dict[Area, int]
    chapter_random_character_requirements: dict[Area, list[Character]]
    spoiler_chapter_character_requirements: dict[str, tuple[int, list[str]]]

    starting_chapter: Area = Area.NEGOTIATIONS
    minikit_bundle_name: str = ""
    available_minikits: int = -1
    minikit_bundle_count: int = -1
    goal_minikit_count: int = -1
    goal_minikit_bundle_count: int = -1
    goal_boss_count: int = -1
    goal_area_completion_count: int = 0
    gold_brick_event_count: int = 0
    # Used in generation to check that created Gold Bricks match the number expected to be created from options.
    expected_gold_brick_event_count: int = -1
    character_unlock_location_count: int = 0
    goal_excluded_character_unlock_location_count: int = 0

    ridesanity_location_count: int = 0

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.enabled_chapters = set()
        self.enabled_chapters_with_locations = set()
        self.enabled_non_goal_chapters = set()
        self.enabled_episodes = set()
        self.enabled_bonuses = set()
        self.character_chapter_access_counts = Counter()
        self.boss_area_to_boss = {}
        self.chapters_requiring_alt_characters = set()
        self.chapter_required_character_counts = {}
        self.spoiler_chapter_character_requirements = {}
        self.chapter_extra_random_character_counts = {}
        self.chapter_random_character_requirements = {}
        # UT-specific attributes are deliberately only set when generating under Universal Tracker, so an AttributeError
        # will occur in normal generation if normal generation tries to access one of these attributes.
        if self.is_universal_tracker():
            self.ut_disconnected_free_play_completion_events = {}
            self.ut_disconnected_true_jedi_gold_brick_events = {}
            self.ut_disconnected_10_minikits_gold_brick_events = {}
            self.ut_disconnected_bonus_completion_events = {}
            self.ut_disconnected_power_brick_events = {}
            self.ut_disconnected_boss_events = {}
            self.ut_datastorage_key_to_disconnected_dict = {
                k.format(team=0, player=self.player): v for k, v in {
                    COMPLETED_FREE_PLAY_KEY: (
                        self.ut_disconnected_free_play_completion_events,
                        # Bosses are currently implemented by completing the chapter, so share the same datastorage key.
                        self.ut_disconnected_boss_events,
                    ),
                    COMPLETED_TRUE_JEDI_KEY: (
                        self.ut_disconnected_true_jedi_gold_brick_events,
                    ),
                    COMPLETED_10_MINIKITS_KEY: (
                        self.ut_disconnected_10_minikits_gold_brick_events,
                    ),
                    COMPLETED_BONUSES_KEY: (
                        # TODO: Bonus completion should use the same datastorage as free play completion.
                        self.ut_disconnected_bonus_completion_events,
                    ),
                    COLLECTED_POWER_BRICKS_KEY: (
                        self.ut_disconnected_power_brick_events,
                    ),
                }.items()
            }
            self.ut_minikit_goal_submitted_key = MINIKIT_GOAL_SUBMITTED_KEY.format(team=0, player=self.player)

    def log_info(self, message: str, *args) -> None:
        logger.info("Lego Star Wars TCS (%s): " + message, self.player_name, *args)

    def log_warning(self, message: str, *args) -> None:
        logger.warning("Lego Star Wars TCS (%s): " + message, self.player_name, *args)

    def log_error(self, message: str, *args) -> None:
        logger.error("Lego Star Wars TCS (%s): " + message, self.player_name, *args)

    def log_debug(self, message: str, *args) -> None:
        logger.debug("Lego Star Wars TCS (%s): " + message, self.player_name, *args)

    def raise_error(self, ex_type: Callable[[str], Exception], message: str, *args) -> NoReturn:
        raise ex_type(("Lego Star Wars TCS (%s): " + message) % (self.player_name, *args))

    def option_error(self, message: str, *args) -> NoReturn:
        self.raise_error(OptionError, message, *args)

    def is_universal_tracker(self) -> bool:
        """Return whether the current generation is being done with Universal Tracker rather than a real generation."""
        # The `generation_is_fake` attribute is added by Universal Tracker to allow detection of generation with
        # Universal Tracker rather than real generation.
        return hasattr(self.multiworld, "generation_is_fake")

    def is_universal_tracker_deferred_entrances(self) -> bool:
        """Return whether Universal Tracker deferred entrances are enabled."""
        return (self.is_universal_tracker()
                and getattr(self.multiworld, "enforce_deferred_connections", "default") != "off")

    @property
    def starting_episode(self) -> int:
        return self.starting_chapter.get_chapter_episode()

    def set_rule(self, spot: Location | Entrance, rule: CollectionRule | Rule[Any]) -> None:
        # Allow passing in resolved rules.
        if isinstance(rule, Rule.Resolved):
            self.register_rule_dependencies(rule)
            if isinstance(spot, Entrance):
                self._register_rule_indirects(rule, spot)
            spot.access_rule = rule
        else:
            super().set_rule(spot, rule)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        # Check that the multiworld seed name can fit in the unused section of the game's save-data that the seed name
        # has been designated to.
        seed_name_byte_count = len(multiworld.seed_name.encode('utf-8'))
        if seed_name_byte_count > MULTIWORLD_SEED_NAME_MAX_BYTES:
            # While Archipelago does not place a bound on the maximum length of a seed name, Archipelago generates a
            # seed name, from the multiworld seed. The generated seed name is usually up to 20 numeric characters,
            # though webhost generations prepend a "W".
            # This should never happen in a real generation unless the generator has been modified to accept custom seed
            # names or to otherwise use the multiworld seed as the seed name.
            # Technically, unit test generations could specify custom seed names that surpass this number of bytes, but
            # stage_assert_generate would not be run there anyway.
            raise OptionError(f"The multiworld seed name ('{multiworld.seed_name}') is too large for Lego Star Wars:"
                              f" The Complete Saga. Lego Star Wars: The Complete Saga requires that the multiworld seed"
                              f" name encodes to no more than {MULTIWORLD_SEED_NAME_MAX_BYTES} bytes, but"
                              f" '{multiworld.seed_name}' encodes to {seed_name_byte_count} bytes.")
        # I can't imagine this ever happening, but it would cause issues with the client if it did.
        if seed_name_byte_count == 0:
            raise OptionError(f"An empty multiworld seed name was set. This would break the Lego Star Wars: The"
                              f" Complete Saga client, so generation cannot continue.")


    def generate_early(self) -> None:
        # Check that the player's name can fit in the unused section of the game's save-data that the player's name has
        # been designated to.
        name_byte_count = len(self.player_name.encode("utf-8"))
        if name_byte_count > SLOT_NAME_MAX_BYTES:
            # This should never happen currently, because player names are limited to a maximum of 16 utf-8 characters,
            # which can be up to 4 bytes each, so up to 64 bytes.
            self.option_error("Player name is too large. Lego Star Wars TCS restricts player names to a maximum"
                              " of %i bytes, but '%s' encodes to %i bytes.",
                              SLOT_NAME_MAX_BYTES, self.player_name, name_byte_count)
        # I can't imagine this ever happening, but it would cause issues with the client if it did.
        if name_byte_count == 0:
            self.option_error("An empty player name was set. This would break the Lego Star Wars: The Complete Saga"
                              " client, so generation cannot continue.")
        resolve_options(self)

    def get_filler_item_name(self) -> str:
        junk_weights: dict[str, int] = self.options.junk_weights.value
        return self.random.choices(tuple(junk_weights), tuple(junk_weights.values()))[0]

    def create_item(self, name: str) -> LegoStarWarsTCSItem:
        if self.is_universal_tracker():
            if name == self.glitches_item_name or name == self.glitches_all_item_name:
                return LegoStarWarsTCSItem(name, ItemClassification.progression, None, self.player)
            if name not in self.item_name_to_id and name in REVERSE_READABLE_ABILITY_TO_ABILITY:
                return LegoStarWarsTCSItem(name, ItemClassification.progression, None, self.player,
                                           REVERSE_READABLE_ABILITY_TO_ABILITY[name])

        code = self.item_name_to_id[name]

        # `self.effective_character_abilities`, `self.logical_item_counts` are `None` until `create_items()`.
        classification, collect_abilities = evaluate_effective_item(
            self, name, self.effective_character_abilities, self.logical_item_counts)

        return LegoStarWarsTCSItem(name, classification, code, self.player, collect_abilities)

    def create_event(self, name: str) -> LegoStarWarsTCSItem:
        return LegoStarWarsTCSItem(name, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        self.multiworld.itempool.extend(item_pool.create_item_pool(self))

        if self.is_universal_tracker():
            # Universal Tracker deletes the items added to precollected_items by create_items, instead later creating
            # all items with create_item(), but starting characters need to be created before
            # self.starting_character_abilities is set to `starting_abilities` otherwise the starting characters will
            # lose all their abilities. To work around this, Universal Tracker is made to pretend that the starting
            # characters had no abilities, so no abilities will be stripped from any characters created later on with
            # create_item().
            self.starting_character_abilities = CharacterAbility.NONE

    def create_region(self, name: str) -> Region:
        r = Region(name, self.player, self.multiworld)
        self.multiworld.regions.append(r)
        return r

    def create_regions(self) -> None:
        regions.create_regions(self)
        # Check that the number of Gold Brick events created matched what was expected from the calculation in
        # generate_early.
        assert self.gold_brick_event_count == self.expected_gold_brick_event_count, \
            "Created Gold Bricks did not match expected Gold Bricks, something is wrong."
        self.set_completion_rule(Has("Victory"))

    def add_location(self, name: str, region: Region) -> LegoStarWarsTCSLocation:
        location = LegoStarWarsTCSLocation(self.player, name, self.location_name_to_id[name], region)
        region.locations.append(location)
        return location

    def add_shop_location(self, name: str, region: Region, purchase_cost: int) -> LegoStarWarsTCSLocation:
        location = LegoStarWarsTCSShopLocation(self.player, name, self.location_name_to_id[name], region, purchase_cost)
        region.locations.append(location)
        return location

    def add_event_pair(self, location_name: str, region: Region, item_name: str = "", hide_in_spoiler: bool = True
                       ) -> LegoStarWarsTCSLocation:
        if not item_name:
            item_name = location_name
        location = LegoStarWarsTCSLocation(self.player, location_name, None, region)
        # Showing in the spoiler is only useful if the event is randomized in some way.
        # This does no affect whether events are shown in a spoiler playthrough.
        location.show_in_spoiler = not hide_in_spoiler
        item = self.create_event(item_name)
        location.place_locked_item(item)
        region.locations.append(location)
        return location

    def add_gold_brick_event(self, location_name: str, region: Region) -> LegoStarWarsTCSLocation:
        self.gold_brick_event_count += 1
        return self.add_event_pair(location_name, region, GOLD_BRICK_EVENT_NAME)

    def get_score_multiplier_requirement(self, studs_cost: int):
        max_no_multiplier_cost = self.options.most_expensive_purchase_with_no_multiplier.value * 1000
        count: int
        if studs_cost <= max_no_multiplier_cost:
            count = 0
        elif studs_cost <= max_no_multiplier_cost * 2:
            count = 1  # x2
        elif studs_cost <= max_no_multiplier_cost * 8:
            count = 2  # x2 x4 = x8
        elif studs_cost <= max_no_multiplier_cost * 48:
            count = 3  # x2 x4 x6 = x48
        elif studs_cost <= max_no_multiplier_cost * 384:
            count = 4  # x2 x4 x6 x8 = x384
        elif studs_cost <= max_no_multiplier_cost * 3840:
            count = 5  # x2 x4 x6 x8 x10 = x3840
        else:
            # The minimum value of the option range guarantee that x3840 is enough to purchase everything.
            raise AssertionError(f"Studs cost {studs_cost} is too large. This is an error with the apworld.")

        return count

    def get_starting_inventory_abilities(self) -> CharacterAbility:
        """Get the abilities currently provided by the player's starting inventory."""
        starting_abilities = CharacterAbility.NONE
        for item in self.multiworld.precollected_items[self.player]:
            if not item.advancement:
                continue
            assert isinstance(item, LegoStarWarsTCSItem)
            if item.abilities:
                starting_abilities |= item.abilities
        return starting_abilities

    def set_rules(self) -> None:
        # Rules are set when the locations/entrances are created, during create_regions. This makes sense for
        # location/entrance rules, but the completion condition is also set during create_regions so that the rules can
        # be inspected to determine the classifications of items during create_items, which runs after create_regions,
        # but before set_rules.

        if not self.is_universal_tracker():
            from .rule_builder_optimise import optimise_rules
            optimise_rules(self)

    @classmethod
    def stage_fill_hook(cls,
                        multiworld: MultiWorld,
                        progitempool: list[Item],
                        usefulitempool: list[Item],
                        filleritempool: list[Item],
                        fill_locations: list[Location],
                        ) -> None:
        game_players = multiworld.get_game_players(cls.game)
        # Get all player IDs that have progression classification minikits.
        minikit_player_ids = {player for player in game_players if multiworld.worlds[player].goal_minikit_count > 0}
        # Get the player IDs of those that are using minimal accessibility.
        minikit_minimal_player_ids = {player for player in game_players
                                      if multiworld.worlds[player].options.accessibility == "minimal"}

        def sort_func(item: Item):
            if item.player in minikit_player_ids and item.name in MINIKITS_BY_NAME:
                if item.player in minikit_minimal_player_ids:
                    # For minimal players, place goal macguffins first. This helps prevent fill from dumping logically
                    # relevant items into unreachable locations and reducing the number of reachable locations to fewer
                    # than the number of items remaining to be placed.
                    #
                    # Placing only the non-required goal macguffins first or slightly more than the number of
                    # non-required goal macguffins first was also tried, but placing all goal macguffins first seems to
                    # give fill the best chance of succeeding.
                    #
                    # All sizes of minikit bundles, are given the *deprioritized* classification for minimal players,
                    # which avoids them being placed on priority locations, which would otherwise occur due to them
                    # being sorted to be placed first.
                    return 1
                else:
                    # For non-minimal players, place goal macguffins last. The helps prevent fill from filling most/all
                    # reachable locations with the goal macguffins that are only required for the goal.
                    return -1
            else:
                # Python sorting is stable, so this will leave everything else in its original order.
                return 0

        progitempool.sort(key=sort_func)

    def collect(self, state: CollectionState, item: LegoStarWarsTCSItem) -> bool:
        if super().collect(state, item):
            abilities_as_int = item.collect_abilities_int
            if abilities_as_int is not None:
                # The collected item has abilities, so collect them into the state too.
                player_prog = state.prog_items[self.player]
                player_prog["COMBINED_ABILITIES"] |= abilities_as_int
                # state.prog_items is typed as Counter[str], but `abilities_as_int` is an `int`, so this is technically
                # not allowed, but works for now.
                player_prog[abilities_as_int] += 1

                # Gonk Droid is a character, so has abilities and needs to be checked in this branch.
                # Most progression items are usually characters, and most characters are not in SUPER_GONK_ITEMS.
                # `.collect()` is performance critical, so checking "Gonk Droid" and "Super Gonk" is done separately for
                # better performance, at the cost of readability.
                if (item.name == "Gonk Droid"
                        and "Super Gonk" in player_prog
                        and "Super Gonk Droid" not in player_prog):
                    # The pair is newly complete, so grant the abilities.
                    player_prog["COMBINED_ABILITIES"] |= SUPER_GONK_DROID_ABILITIES_VALUE
                    player_prog[SUPER_GONK_DROID_ABILITIES_VALUE] += 1
                    player_prog["Super Gonk Droid"] = 1
            # Super Gonk is an Extra, so does not have abilities, so has to be checked in a separate branch.
            elif item.name == "Super Gonk":
                player_prog = state.prog_items[self.player]
                if "Gonk Droid" in player_prog and "Super Gonk Droid" not in player_prog:
                    # The pair is newly complete, so grant the abilities.
                    player_prog["COMBINED_ABILITIES"] |= SUPER_GONK_DROID_ABILITIES_VALUE
                    player_prog[SUPER_GONK_DROID_ABILITIES_VALUE] += 1
                    player_prog["Super Gonk Droid"] = 1
            return True
        return False

    # .remove() is barely used by Core AP, so readable code is preferred over extremely optimised code.
    def _remove_state_abilities(self, state: CollectionState, abilities_as_int: int):
        player_prog = state.prog_items[self.player]
        current_abilities_int_count = player_prog[abilities_as_int]
        if current_abilities_int_count == 1:
            del player_prog[abilities_as_int]
            new_combined_abilities = 0
            key: int | str
            # This is not fast, but `remove()` is barely ever called by Core AP.
            # If it is needed to make this faster, then TCS could stop abusing `state.prog_items`, and put its own
            # `state.tcs_abilities` on the state instead as a `Counter[int, int]`.
            for key in player_prog:
                if type(key) is int:
                    new_combined_abilities |= key
            player_prog["COMBINED_ABILITIES"] = new_combined_abilities
        else:
            # At least one other collected item is providing the same combination of abilities, so the combined
            # abilities won't have changed.
            player_prog[abilities_as_int] = current_abilities_int_count - 1

    def remove(self, state: CollectionState, item: LegoStarWarsTCSItem) -> bool:
        if super().remove(state, item):
            abilities_as_int = item.collect_abilities_int
            if abilities_as_int is not None:
                # The removed item has abilities, so remove them from the state too.
                self._remove_state_abilities(state, abilities_as_int)
            # Most items with abilities are not in SUPER_GONK_ITEMS, but the code is more readable to handle both items
            # in a single branch, and `.remove()` is not performance critical, so it's not a concern.
            if item.name in SUPER_GONK_ITEMS:
                player_prog = state.prog_items[self.player]
                if ("Super Gonk Droid" in player_prog
                        and ("Gonk Droid" not in player_prog or "Super Gonk" not in player_prog)):
                    # One of the pair is no longer provided, so remove the abilities.
                    self._remove_state_abilities(state, SUPER_GONK_DROID_ABILITIES_VALUE)
                    # Remove the marker that Super Gonk abilities have been provided.
                    del player_prog["Super Gonk Droid"]
            return True
        return False

    def fill_slot_data(self) -> Mapping[str, Any]:
        # The dict is presented here, rather than being returned directly by a function call, to help with debugging.
        slot_data_dict: dict[str, Any] = {}
        slot_data_options = TCSSlotDataOptions.from_world(self)
        slot_data_options.fill_slot_data(slot_data_dict)
        # Make sure the slot data deserializes correctly, so the client won't just be bricked when it tries to load it.
        from_slot_data = TCSSlotDataOptions.from_slot_data(json.loads(json.dumps(slot_data_dict)))
        if from_slot_data != slot_data_options:
            raise Exception(f"Slot data does not match following deserialization."
                            f"\n\t{slot_data_options}"
                            f"\nserialized as:"
                            f"\n\t{slot_data_dict}"
                            f"\ndeserialized as:"
                            f"\n\t{from_slot_data}")
        return slot_data_dict

    @classmethod
    def stage_write_spoiler_header(cls, multiworld: MultiWorld, spoiler_handle: TextIO):
        spoiler_handle.write(f"Generated with {cls.game} Apworld version {constants.AP_WORLD_VERSION}\n")

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        super().write_spoiler_header(spoiler_handle)

        spoiler_handle.write(f"Starting Chapter: {self.starting_chapter.get_long_name()}\n")

        enabled_episodes = sorted(self.enabled_episodes)
        spoiler_handle.write(f"Enabled Episodes: {enabled_episodes}\n")

        enabled_chapters = ", ".join(Area.to_human_readable_list(self.enabled_chapters))
        spoiler_handle.write(f"Enabled Chapters: {enabled_chapters}\n")

        enabled_bonuses = sorted(self.enabled_bonuses)
        spoiler_handle.write(f"Enabled Bonuses: {enabled_bonuses}\n")

        enabled_bosses = ", ".join(Area.to_human_readable_list(self.enabled_bosses))
        spoiler_handle.write(f"Enabled Bosses: {enabled_bosses}\n")

        if self.spoiler_chapter_character_requirements:
            spoiler_handle.write(f"Chapter Character requirements:\n")
            for chapter, required in sorted(self.spoiler_chapter_character_requirements.items(), key=lambda t: t[0]):
                required_count = required[0]
                sorted_characters = sorted(required[1])
                spoiler_handle.write(f"    {chapter}:"
                                     f" {required_count}/{len(sorted_characters)} of {', '.join(sorted_characters)}\n")

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any] | None:
        slot_data_version = tuple(slot_data["apworld_version"])
        # Allow connecting only if the APWorld major and minor version matches, and if there are no logic changes in the
        # case that the APWorld versions are not the same.
        if (slot_data_version[:2] != constants.AP_WORLD_VERSION[:2]
                or slot_data["logic_version"] != constants.UT_LOGIC_VERSION):
            raise TCSUniversalTrackerAPWorldVersionMismatchError(
                f"LSW TCS version error: The version of the apworld used to generate this world ({slot_data_version})"
                f" does not have matching logic with the version of your installed apworld ({constants.AP_WORLD_VERSION})."
            )
        return slot_data

    def _ut_connect_deferred_area_events(self, found_key: str, data_storage_value: Iterable[Any]) -> None:
        if data_storage_value is None:
            # Likely means that no value has been set on the server's datastorage yet.
            return
        if not isinstance(data_storage_value, Iterable):
            raise Exception(f"Expected an Iterable for datastorage key {found_key}, but got {data_storage_value} of "
                            f"type {type(data_storage_value)}")
        area_to_disconnected_entrance_dicts = self.ut_datastorage_key_to_disconnected_dict[found_key]
        for area_to_disconnected_entrance in area_to_disconnected_entrance_dicts:
            for area_id in data_storage_value:
                if area_id not in area_to_disconnected_entrance:
                    # The player could theoretically complete a disabled level (e.g. playing without the client being
                    # connected), and the client might write read that completed level from the save data and send the
                    # completion to datastorage.
                    continue
                entrance, region = area_to_disconnected_entrance[area_id]
                if entrance.connected_region is None:
                    entrance.connect(region)

    def _ut_connect_minikit_goal_submitted_event(self, data_storage_value: Any) -> None:
        if not data_storage_value:
            return
        if (disconnected_entrance_pair := self.ut_minikit_goal_disconnected_entrance) is not None:
            entrance, region = disconnected_entrance_pair
            if entrance.connected_region is None:
                entrance.connect(region)

    def reconnect_found_entrances(self, found_key: str, data_storage_value: Any):
        """UT-specific method for handling deferred entrances. The name of the method must not be changed."""
        self.log_info("Received data storage key %s with value %s", found_key, data_storage_value)
        if found_key in self.ut_datastorage_key_to_disconnected_dict:
            self._ut_connect_deferred_area_events(found_key, data_storage_value)
        elif found_key == self.ut_minikit_goal_submitted_key:
            self._ut_connect_minikit_goal_submitted_event(data_storage_value)
        else:
            # Probably should not happen, but who knows with Universal Tracker.
            pass
