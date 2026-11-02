from collections.abc import Mapping
from copy import deepcopy
import os
import time
from typing import Any, ClassVar, Optional
import zipfile

from Fill import fill_restrictive
from BaseClasses import CollectionState, Item, LocationProgressType, Region
from BaseClasses import ItemClassification as IC
from BaseClasses import Tutorial
from worlds.Files import APPatch
from .ClientUtils import VERSION
from .Items import (
    ITEM_TABLE,
    TPItem,
    item_factory,
    item_name_groups,
)
from Options import OptionError, Toggle
from .Locations import (
    LOCATION_TABLE,
    LOCATION_TO_REGION,
    TPFlag,
    TPLocation,
)
from .options import *
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import (
    Component,
    SuffixIdentifier,
    Type,
    components,
    launch_subprocess,
)

from .Randomizer.SeedId import gen_seed_id
from .Randomizer.SettingsEncoder import get_item_placements, get_setting_string
from .Randomizer.ItemPool import (
    DUNGEON_TO_BOSS_DEFEAT,
    DUNGEON_TO_BOSS_DEFEAT,
    VANILLA_GOLDEN_BUG_LOCATIONS,
    VANILLA_POE_LOCATIONS,
    VANILLA_SKY_CHARACTER_LOCATIONS,
    generate_itempool,
    get_boss_defeat_items,
    place_deterministic_items,
    VANILLA_SMALL_KEYS_LOCATIONS,
    VANILLA_BIG_KEY_LOCATIONS,
    VANILLA_MAP_AND_COMPASS_LOCATIONS,
)

from .Logic.Rules import set_location_access_rules
from .Logic.RegionConnection import connect_regions
from .Logic.RegionCreation import (
    create_regions,
)
from .Logic.RegionRules import set_region_access_rules


def run_client() -> None:
    """
    Launch the Twilight Princess client.
    """
    print("Running Twilight Princess Client")
    from .TPClient import main

    launch_subprocess(main, name="TwilightPrincessClient")


components.append(
    Component(
        "Twilight Princess Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".aptp"),
    )
)


class TPPlayerContainer(APPatch):
    """
    Defines the container file for Twilight Princess
    """

    game = "Twilight Princess"
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".aptp"

    def __init__(
        self,
        seed_string: str,
        patch_path: str,
        player_name: str,
        player: int,
        server: str = "",
    ):
        self.output_data = seed_string
        super().__init__(patch_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("settings.txt", self.output_data)
        super().write_contents(opened_zipfile)


class TPWeb(WebWorld):
    """
    This class handles the web interface for Twilight Princess.

    The web interface includes the setup guide and the options page for generating YAMLs.
    """

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the MultiworldGG Twilight Princess software on your computer.",
            "English",
            "setup_en.md",
            "setup/en",
            ["WritingHusky"],
        )
    ]
    display_name = "The Legend of Zelda: Twilight Princess"
    theme = "grass"
    option_groups = tp_option_groups
    rich_text_options_doc = True


class TPWorld(World):
    """
    Join Link and Midna on their adventure through Hyrule in Twilight Princess.
    """

    # Currently using can reach region to check for access rules. may update later
    explicit_indirect_conditions = False

    options_dataclass = TPOptions
    options: TPOptions

    game: ClassVar[str] = "Twilight Princess"
    topology_present: bool = True

    item_name_to_id: ClassVar[dict[str, int]] = {
        name: TPItem.get_apid(data.code)
        for name, data in ITEM_TABLE.items()
        if data.code is not None
    }
    location_name_to_id: ClassVar[dict[str, int]] = {
        name: TPLocation.get_apid(data.code)
        for name, data in LOCATION_TABLE.items()
        if data.code is not None
    }

    item_name_groups: ClassVar[dict[str, set[str]]] = item_name_groups

    web: ClassVar[TPWeb] = TPWeb()

    origin_region_name: str = "Menu"

    player: int

    progression_pool: list[str]
    seed_id = ""

    def __init__(self, *args, **kwargs):
        super(TPWorld, self).__init__(*args, **kwargs)

        self.nonprogress_locations: set[str] = set()
        self.progress_locations: set[str] = set()

        self.useful_pool: list[str] = []
        self.filler_pool: list[str] = []
        self.prefill_pool: list[str] = []

        self.progression_pool = []
        self.pre_pool: list[str] = []

        self.invalid_locations: list[str] = []

    def _determine_nonprogress_and_progress_locations(
        self,
    ) -> tuple[set[str], set[str]]:
        """
        Sort locations into non progesssion location and progression locations based on options set.
        """

        def add_flag(option: Toggle, flag: TPFlag) -> TPFlag:
            return flag if option else TPFlag.Always

        options = self.options

        enabled_flags = TPFlag.Always
        enabled_flags |= TPFlag.Boss
        enabled_flags |= add_flag(options.golden_bugs_shuffled, TPFlag.Golden_Bug)
        enabled_flags |= add_flag(options.shop_items_shuffled, TPFlag.Shop)
        enabled_flags |= add_flag(options.sky_characters_shuffled, TPFlag.Sky_Book)
        enabled_flags |= add_flag(options.poe_shuffled, TPFlag.Poe)
        enabled_flags |= add_flag(options.npc_items_shuffled, TPFlag.Npc)
        enabled_flags |= add_flag(options.hidden_skills_shuffled, TPFlag.Hidden_Skill)
        enabled_flags |= add_flag(options.heart_piece_shuffled, TPFlag.Heart_Container)
        enabled_flags |= add_flag(options.overworld_shuffled, TPFlag.Overworld)
        enabled_flags |= add_flag(options.dungeons_shuffled, TPFlag.Dungeon)
        enabled_flags |= add_flag(
            options.freestanding_rupee_shuffled, TPFlag.Rupee_Freestanding
        )
        enabled_flags |= add_flag(options.hidden_rupee_shuffled, TPFlag.Rupee_Hidden)

        # If not all the flags for a location are set, then force that location to have a non-progress item.
        nonprogress_locations: set[str] = set()
        progress_locations: set[str] = set()

        CHECK_TYPE_MASK = (
            TPFlag.Always
            | TPFlag.Dungeon
            | TPFlag.Overworld
            # | TPFlag.Rupee_Hidden
            # | TPFlag.Rupee_Freestanding
            | TPFlag.Npc
            | TPFlag.Golden_Bug
            # | TPFlag.Bug_Reward
            | TPFlag.Poe
            | TPFlag.Shop
            # | TPFlag.Quest
            | TPFlag.Boss
            # | TPFlag.Dungeon_Reward
            | TPFlag.Heart_Container
            | TPFlag.Hidden_Skill
            | TPFlag.Sky_Book
            | TPFlag.Rupee_Freestanding
            | TPFlag.Rupee_Hidden
        )

        for location, data in LOCATION_TABLE.items():
            # Mask both sides to only compare check-type flags
            location_check_flags = data.flags & CHECK_TYPE_MASK
            enabled_check_flags = enabled_flags & CHECK_TYPE_MASK

            if location_check_flags & enabled_check_flags == location_check_flags:
                progress_locations.add(location)
            else:
                nonprogress_locations.add(location)

                assert progress_locations.isdisjoint(nonprogress_locations)

        return nonprogress_locations, progress_locations

    # Start of generation Process -----------------------------------------------------------------------

    # stage_assert_generate() not used currently

    def generate_early(self) -> None:
        """
        Setup things ready for generation.
        """

        if len(self.player_name) > 16:
            raise OptionError(
                "[Twilight Princess] Player name must be 16 character or less"
            )
        try:
            str.encode(self.player_name, encoding="latin")
        except UnicodeEncodeError:
            raise OptionError(
                "[Twilight Princess] Player name cannot use special characters that do not fit in the Latin encoding."
            )

        # If overworld is not shuffled then override for vanilla placements if in overworld (locations already excluded but prefill needs note)
        if self.options.overworld_shuffled.value == OverWoldShuffled.option_false:
            print(
                "[Twilight Princess] functionality for disabling overworld shuffle is not yet implemented, Overworld Shuffle is being enabled"
            )
            self.options.overworld_shuffled.value = OverWoldShuffled.option_true
            # self.options.golden_bugs_shuffled.value = GoldenBugsShuffled.option_false
            # self.options.shop_items_shuffled.value = ShopItemsShuffled.option_false
            # self.options.heart_piece_shuffled.value = HeartPieceShuffled.option_false
            # self.options.hidden_skills_shuffled.value = (
            #     HiddenSkillsShuffled.option_false
            # )
            # self.options.sky_characters_shuffled.value = (
            #     SkyCharactersShuffled.option_false
            # )
            # self.options.poe_shuffled.value = PoeShuffled.option_false

            # # Add things needed to beat dungeons to early spheres
            # # self.multiworld.local_early_items[self.player][
            # #     "Progressive Master Sword"
            # # ] = 1
            # # self.multiworld.local_early_items[self.player]["Progressive Hero's Bow"] = 1
            # # self.multiworld.local_early_items[self.player]["Progressive Clawshot"] = 1
            # # self.multiworld.local_early_items[self.player]["Bomb bag"] = 1
            # self.multiworld.early_items[self.player]["Shadow Crystal"] = 1
            # self.multiworld.early_items[self.player]["Gate Keys"] = 1

        if (
            self.options.overworld_shuffled.value == OverWoldShuffled.option_false
            and self.options.dungeons_shuffled.value == DungeonsShuffled.option_false
        ):
            raise OptionError(
                "[Twilight Princess] One of Overworld and Dungeons must be shuffled, Please fix this"
            )

        if (
            self.options.castle_requirements_count.value < 0
        ):  # Should not occur but just incase
            raise OptionError(
                "[Twilight Princess] Castle Requirement Count cannot be a negative number"
            )

        if (
            self.options.castle_requirements.value
            not in [CastleRequirements.option_open, CastleRequirements.option_vanilla]
        ) and (self.options.castle_requirements_count.value == 0):
            raise OptionError(
                "[Twilight Princess] A non Zero value must be chosen for your Castle Requirement setting"
            )
        max_count = 0
        match (self.options.castle_requirements.value):
            case CastleRequirements.option_fused_shadows:
                max_count = min(self.options.castle_requirements_count.value, 3)
            case CastleRequirements.option_mirror_shards:
                max_count = min(self.options.castle_requirements_count.value, 4)
            case CastleRequirements.option_dungeons:
                max_count = min(self.options.castle_requirements_count.value, 8)
            case CastleRequirements.option_poe_souls:
                max_count = min(self.options.castle_requirements_count.value, 60)
            case CastleRequirements.option_hearts:
                max_count = min(
                    max(self.options.castle_requirements_count.value, 4), 20
                )
            case CastleRequirements.option_mirror_shards:
                max_count = min(self.options.castle_requirements_count.value, 4)
            case _:
                pass
        self.options.castle_requirements_count = (
            self.options.castle_requirements_count.from_any(max_count)
        )

        if (
            self.options.castle_bk_requirements_count.value < 0
        ):  # Should not occur but just incase
            raise OptionError(
                "[Twilight Princess] Castle Boss Key Requirement Count cannot be a negative number"
            )

        if (
            self.options.castle_bk_requirements.value
            != CastleBKRequirements.option_none
        ) and (self.options.castle_bk_requirements_count.value == 0):
            raise OptionError(
                "[Twilight Princess] A non Zero value must be chosen for your Castle Boss Key Requirement setting"
            )
        max_count = 0
        match (self.options.castle_bk_requirements.value):
            case CastleBKRequirements.option_fused_shadows:
                max_count = min(self.options.castle_bk_requirements_count.value, 3)
            case CastleBKRequirements.option_mirror_shards:
                max_count = min(self.options.castle_bk_requirements_count.value, 4)
            case CastleBKRequirements.option_dungeons:
                max_count = min(self.options.castle_bk_requirements_count.value, 8)
            case CastleBKRequirements.option_poe_souls:
                max_count = min(self.options.castle_bk_requirements_count.value, 60)
            case CastleBKRequirements.option_hearts:
                max_count = min(
                    max(self.options.castle_bk_requirements_count.value, 4), 20
                )
            case CastleBKRequirements.option_mirror_shards:
                max_count = min(self.options.castle_bk_requirements_count.value, 4)
            case _:
                pass

        self.options.castle_bk_requirements_count = (
            self.options.castle_bk_requirements_count.from_any(max_count)
        )

        self.boss_defeat_items = get_boss_defeat_items(self)

        # Early into generation, set the options for the keys and map/compass.
        if self.options.dungeons_shuffled.value == DungeonsShuffled.option_false:
            if (
                self.options.small_key_settings.value
                != SmallKeySettings.option_startwith
            ):
                self.options.small_key_settings.value = SmallKeySettings.option_vanilla

            if self.options.big_key_settings.value != BigKeySettings.option_startwith:
                self.options.big_key_settings.value = BigKeySettings.option_vanilla
            if (
                self.options.map_and_compass_settings.value
                != MapAndCompassSettings.option_startwith
            ):
                self.options.map_and_compass_settings.value = (
                    MapAndCompassSettings.option_vanilla
                )

        # If Shadow Crystal is a precollected item don't try to put it in Sphere 1
        if any(
            [
                item.name == "Shadow Crystal"
                for item in self.multiworld.precollected_items[self.player]
            ]
        ):
            self.options.early_shadow_crystal.value = EarlyShadowCrystal.option_false

        self.nonprogress_locations, self.progress_locations = (
            self._determine_nonprogress_and_progress_locations()
        )

        assert len(self.progress_locations) > 10

        if self.options.faron_woods_logic.value == FaronWoodsLogic.option_closed:
            self.multiworld.early_items[self.player]["Gale Boomerang"] = 1
            self.multiworld.early_items[self.player]["Lantern"] = 1
            self.multiworld.early_items[self.player]["North Faron Woods Gate Key"] = 1
            self.multiworld.early_items[self.player]["Faron Woods Coro Key"] = 1
            # self.multiworld.early_items[self.player]["Shadow Crystal"] = 1

        if self.options.early_shadow_crystal.value == EarlyShadowCrystal.option_true:
            self.multiworld.early_items[self.player]["Shadow Crystal"] = 1

    def create_regions(self) -> None:
        """
        Create and connect regions for the Twilight Princess world.

        This method first creates all the regions and adds the locations to them.
        Then it connects the regions to each other.
        """

        # This adds all the regions. (build vertices)
        create_regions(self.multiworld, self.player)

        # This connects all the regions to each other. (build edges)
        connect_regions(self.multiworld, self.player)

        menu = self.get_region(self.origin_region_name)
        menu.connect(self.get_region("Outside Links House"))

        # Ensure that all locations are added to lists
        if len(self.progress_locations) + len(self.nonprogress_locations) != len(
            LOCATION_TABLE
        ):
            locations_set = set(LOCATION_TABLE.keys())
            locations_set.difference_update(self.progress_locations)
            locations_set.difference_update(self.nonprogress_locations)
            assert (
                len(locations_set) == 0
            ), f"[Twilight Princess] location(s) dropped from the locations lists {locations_set=}"
            assert set(self.progress_locations).isdisjoint(
                self.nonprogress_locations
            ), f"[Twilight Princess] duplicate locations in list {set(self.progress_locations).intersection(self.nonprogress_locations)=}"
            assert (
                False
            ), f"[Twilight Princess] Something Terrible went wrong with the location categorizing {len(self.progress_locations)=} + {len(self.nonprogress_locations)} != {len(LOCATION_TABLE)=}"

        # Place locations in their locations
        for location_name, data in LOCATION_TABLE.items():
            assert (
                location_name in self.progress_locations
                or location_name in self.nonprogress_locations
            ), f"[Twilight Princess] {location_name=} is not in non/progress_locations"
            assert (
                location_name in LOCATION_TO_REGION
            ), f"[Twilight Princess] {location_name=} is not in location to region table"

            region_name = LOCATION_TO_REGION[location_name]

            assert (
                region_name in self.multiworld.regions.region_cache[self.player]
            ), f"[Twilight Princess] {region_name=} is not in multiworld regions"

            region = self.multiworld.get_region(region_name, self.player)
            location = TPLocation(
                self.player,
                location_name,
                region,
                data,
            )

            region.locations.append(location)
            if location_name in self.nonprogress_locations:
                self.get_location(location_name).progress_type = (
                    LocationProgressType.EXCLUDED
                )

        # If dungeon rewards are progression then take a second pass to update Progress Type
        if (
            self.options.dungeon_rewards_progression.value
            != DungeonRewardsProgression.option_anything
        ):
            for location, data in LOCATION_TABLE.items():
                if (TPFlag.Boss & data.flags) == TPFlag.Boss:
                    self.get_location(location).progress_type = (
                        LocationProgressType.PRIORITY
                    )  # This happens after location building so it will override dungeons shuffled option

    def create_items(self) -> None:
        """
        Create the items for the Twilight Princess world.
        """
        # First Items with deterministic locations are placed (mostly for logic in generation)
        place_deterministic_items(self)

        # This fills the itempool with items according to the location count (any precollected items are pushed to precollected_items)
        generate_itempool(self)

    # No more items, locations, or regions can be created past this point

    def set_rules(self) -> None:
        """
        Set the rules for the Twilight Princess world.
        """
        # Set access rules
        set_region_access_rules(self, self.player)
        set_location_access_rules(self)

        # Set item rules

        # Early shadow crystal item rules
        if self.options.early_shadow_crystal.value == EarlyShadowCrystal.option_true:

            # Add item rule for dungeon item locations
            options = [
                self.options.small_key_settings,
                self.options.big_key_settings,
                self.options.map_and_compass_settings,
            ]
            settings = [SmallKeySettings, BigKeySettings, MapAndCompassSettings]
            vanillas = [
                VANILLA_SMALL_KEYS_LOCATIONS,
                VANILLA_BIG_KEY_LOCATIONS,
                VANILLA_MAP_AND_COMPASS_LOCATIONS,
            ]
            for option, setting, vanilla in zip(options, settings, vanillas):
                if option.value == setting.option_vanilla:
                    for dungeon in vanilla:
                        for item in vanilla[dungeon]:
                            for location in vanilla[dungeon][item]:
                                old_rule = self.get_location(location).item_rule
                                self.get_location(location).item_rule = (
                                    lambda item, _oldrule=old_rule: (
                                        item.name != "Shadow Crystal" and _oldrule(item)
                                    )
                                )

            # Add item rules for bug and poe locations
            if (
                self.options.golden_bugs_shuffled.value
                == GoldenBugsShuffled.option_false
            ):
                for location in VANILLA_GOLDEN_BUG_LOCATIONS.values():
                    old_rule = self.get_location(location).item_rule
                    self.get_location(location).item_rule = (
                        lambda item, _oldrule=old_rule: (
                            item.name != "Shadow Crystal" and _oldrule(item)
                        )
                    )
            if self.options.poe_shuffled.value == PoeShuffled.option_false:
                for location in VANILLA_POE_LOCATIONS:
                    old_rule = self.get_location(location).item_rule
                    self.get_location(location).item_rule = (
                        lambda item, _oldrule=old_rule: (
                            item.name != "Shadow Crystal" and _oldrule(item)
                        )
                    )

        # Small Keys on bosses based on setting
        if self.options.small_keys_on_bosses.value == SmallKeysOnBosses.option_false:
            for location, data in LOCATION_TABLE.items():
                if (data.flags & TPFlag.Boss) == TPFlag.Boss:
                    old_rule = self.get_location(location).item_rule
                    self.get_location(location).item_rule = (
                        lambda item, _oldrule=old_rule: (
                            (item.name not in item_name_groups["Small Keys"])
                            and _oldrule(item)
                        )
                    )

        # Boss keys on own defeat locations
        for dungeon, data in VANILLA_BIG_KEY_LOCATIONS.items():
            for key, _ in data.items():
                for location in DUNGEON_TO_BOSS_DEFEAT[dungeon]:
                    if not location:
                        continue
                    old_rule = self.get_location(location).item_rule
                    self.get_location(location).item_rule = (
                        lambda item, _oldrule=old_rule, _key=key: (
                            (item.name != _key) and _oldrule(item)
                        )
                    )

        # Quick sanity check, Must happen here so it runs before plando-ed items
        allstate = self.multiworld.get_all_state(allow_partial_entrances=True)
        explorable_regions = [
            self.get_region(self.origin_region_name),
        ]
        total_region_count = len(self.get_regions())
        checked_regions: list[Region] = []
        just_checked_regions: list[Region] = []
        fresh_regions: list[Region] = []
        timer = time.time()

        # BFS through graph to see if all state reaches
        while True:
            if time.time() > timer + 3:
                print("[Twilight Princess] Timed out acessiblity pre checks")
                break
            for region in explorable_regions:
                if region in checked_regions and region in explorable_regions:
                    explorable_regions.remove(region)
                    continue
                if allstate.can_reach_region(region.name, self.player):
                    fresh_regions.append(region)
                    explorable_regions.remove(region)
                    checked_regions.append(region)
                    just_checked_regions.append(region)

            for region in fresh_regions:

                for exit in region.entrances:
                    if exit.connected_region not in checked_regions:
                        explorable_regions.append(exit.connected_region)
                    elif exit.parent_region not in checked_regions:
                        explorable_regions.append(exit.parent_region)
                for exit in region.exits:
                    if exit.connected_region not in checked_regions:
                        explorable_regions.append(exit.connected_region)
                    elif exit.parent_region not in checked_regions:
                        explorable_regions.append(exit.parent_region)
                fresh_regions.remove(region)

            if len(checked_regions) == total_region_count:
                break

            if len(explorable_regions) == 0:
                raise Exception(
                    f"[Twilight Princess] No more explorable regions and Ganon was not found {just_checked_regions=}"
                )
            else:
                just_checked_regions = []

        for location in [
            location_name
            for location_name in LOCATION_TABLE.keys()
            if LOCATION_TABLE[location_name].code != None
        ]:
            assert allstate.can_reach_location(
                location, self.player
            ), f"[Twilight Princess] Pre fill allstate check failed for {location=}"

    def pre_fill(self) -> None:
        """
        Apply special fill rules before the fill stage.
        """

        pre_fill_items = self.get_pre_fill_items()

        collection_state_base = CollectionState(self.multiworld)

        # Only do pre fill if it is needed
        if len(pre_fill_items) == 0:
            assert (
                not self.options.small_key_settings.in_dungeon
            ), "[Twilight Princess] No pre fill items but small keys in dungeon"
            assert (
                not self.options.big_key_settings.in_dungeon
            ), "[Twilight Princess] No pre fill items but big keys in dungeon"
            assert (
                not self.options.map_and_compass_settings.in_dungeon
            ), "[Twilight Princess] No pre fill items but maps and compasses in dungeon"
            assert (
                self.options.golden_bugs_shuffled.value
                == GoldenBugsShuffled.option_true
            ), "[Twilight Princess] No pre fill items but golden bugs not shuffled"
            assert (
                self.options.poe_shuffled.value == PoeShuffled.option_true
            ), "[Twilight Princess] No pre fill items but poes not shuffled"
            assert self.options.dungeon_rewards_progression.value in [
                DungeonRewardsProgression.option_anything,
                DungeonRewardsProgression.option_any_progressive,
            ], "[Twilight Princess] No pre fill items but Dungeon Rewards are vanilla"
            return

        if self.options.golden_bugs_shuffled.value == GoldenBugsShuffled.option_false:
            bug_list = [
                item for item in pre_fill_items if item.name in item_name_groups["Bugs"]
            ]
            assert (
                len(bug_list) == 24
            ), f"[Twilight Princess] There is only {len(bug_list)} / 24 bugs in the pre fill pool"

            bug_list_str = [item.name for item in bug_list]
            for bug in item_name_groups["Bugs"]:
                assert (
                    bug in bug_list_str
                ), f"[Twilight Princess] {bug=} is not in pre_fill_items, {pre_fill_items=}"
            del bug

            for bug in bug_list:
                assert (
                    bug.name in VANILLA_GOLDEN_BUG_LOCATIONS
                ), f"[Twilight Princess] {bug} not in vanilla locations"

                vanilla_location_name = VANILLA_GOLDEN_BUG_LOCATIONS[bug.name]
                self.get_location(vanilla_location_name).place_locked_item(bug)
                pre_fill_items.remove(bug)
                collection_state_base.collect(bug)
            del bug

        # Shuffle Poes into vanilla spots if not shuffled
        if self.options.poe_shuffled.value == PoeShuffled.option_false:
            poe_list = [item for item in pre_fill_items if item.name == "Poe Soul"]
            assert (
                len(poe_list) == 60
            ), f"[Twilight Princess] There is only {len(poe_list)} / 60 poe souls in the pre fill pool"
            assert (
                len(VANILLA_POE_LOCATIONS) == 60
            ), f"[Twilight Princess] There is only {len(VANILLA_POE_LOCATIONS)} / 60 poe souls locations"

            for i, poe_soul in enumerate(poe_list):
                location = VANILLA_POE_LOCATIONS[i]
                self.get_location(location).place_locked_item(poe_soul)
                pre_fill_items.remove(poe_soul)
                collection_state_base.collect(poe_soul)
            assert (
                location == "Snowpeak Poe Among Trees"
            ), f"[Twilight Princess] {location=}"
            del location, poe_list, poe_soul

        # Shuffle Sky characters into vanilla spots if not shuffled
        if (
            self.options.sky_characters_shuffled.value
            == SkyCharactersShuffled.option_false
        ):
            character_list = [
                item for item in pre_fill_items if item.name == "Progressive Sky Book"
            ]
            assert (
                len(character_list) == 7
            ), f"[Twilight Princess] There is only {len(character_list)} / 7 sky characters in the pre fill pool"
            assert (
                len(VANILLA_SKY_CHARACTER_LOCATIONS) == 6
            ), f"[Twilight Princess] There is only {len(VANILLA_SKY_CHARACTER_LOCATIONS)} / 7 sky character locations"

            for i, character in enumerate(character_list):
                # There are only 6 locations for the characters. Idk where the 7th is so just giving the first
                if i == 6:
                    self.push_precollected(character)
                    pre_fill_items.remove(character)
                    continue
                location = VANILLA_SKY_CHARACTER_LOCATIONS[i]
                self.get_location(location).place_locked_item(character)
                pre_fill_items.remove(character)
                collection_state_base.collect(character)
            assert (
                location == "Lake Hylia Bridge Owl Statue Sky Character"
            ), f"[Twilight Princess] {location=}"
            # Sky book chest will already be excluded
            del location, character_list, character

        # Place boss items
        if (
            self.options.dungeon_rewards_progression.value
            == DungeonRewardsProgression.option_vanilla
        ):
            boss_item_list = [
                item
                for item in pre_fill_items
                if item.name in item_name_groups["Boss items"]
            ]

            assert (
                len(boss_item_list) == 7
            ), f"[Twilight Princess] There is only {len(boss_item_list)} boss items in the pre fill pool"

            boss_item_list_str = [item.name for item in boss_item_list]

            for boss_item in item_name_groups["Boss items"]:
                assert (
                    boss_item in boss_item_list_str
                ), f"[Twilight Princess] {boss_item=} is not in pre_fill_items, {pre_fill_items=}"
            del boss_item
            boss_locations = [
                "Arbiters Grounds Dungeon Reward",
                "City in The Sky Dungeon Reward",
                "Forest Temple Dungeon Reward",
                "Goron Mines Dungeon Reward",
                "Lakebed Temple Dungeon Reward",
                "Snowpeak Ruins Dungeon Reward",
                "Temple of Time Dungeon Reward",
            ]
            self.multiworld.random.shuffle(boss_locations)
            self.multiworld.random.shuffle(boss_item_list)

            for item, location in zip(boss_item_list, boss_locations):
                self.get_location(location).place_locked_item(item)
                collection_state_base.collect(item)
                pre_fill_items.remove(item)

        # Add everything from the item pool to allow for full access
        for item in self.progression_pool:
            collection_state_base.collect(self.create_item(item))

        # If faron woods is closed open it so that dungeons can be accessed
        if self.options.faron_woods_logic == FaronWoodsLogic.option_closed:
            collection_state_base.collect(self.boss_defeat_items["Diababa"])

        collection_state_base.sweep_for_advancements()

        # region DugeonItem-Setup

        collection_state_small_key = collection_state_base.copy()
        collection_state_big_key = collection_state_base.copy()
        collection_state_map_and_compass = collection_state_base.copy()

        collection_states = [
            collection_state_small_key,
            collection_state_big_key,
            collection_state_map_and_compass,
        ]

        starting_pool_copy = self.multiworld.precollected_items[self.player].copy()

        # Fill collection states, b/c if small keys are in the prefill pool then they are not in the item_pool
        # and Big Keys need small keys to define access, similar for map and compass etc
        if self.options.small_key_settings.in_dungeon:
            for dungeon_name in VANILLA_SMALL_KEYS_LOCATIONS:
                for item_name in VANILLA_SMALL_KEYS_LOCATIONS[dungeon_name]:
                    assert (
                        item_name in self.prefill_pool
                    ), f"[Twilight Princess] {item_name=} not in prefill pool"
                    for _ in range(
                        len(VANILLA_SMALL_KEYS_LOCATIONS[dungeon_name][item_name])
                    ):
                        collection_state_big_key.collect(self.create_item(item_name))
                        collection_state_map_and_compass.collect(
                            self.create_item(item_name)
                        )

        if self.options.big_key_settings.in_dungeon:
            for dungeon_name in VANILLA_BIG_KEY_LOCATIONS:
                for item_name in VANILLA_BIG_KEY_LOCATIONS[dungeon_name]:
                    if (
                        item_name == "Hyrule Castle Big Key"
                        and self.options.castle_bk_requirements.value
                        != CastleBKRequirements.option_none
                    ):
                        continue  # Handle in place deterministic
                    assert (
                        item_name in self.prefill_pool
                    ), f"[Twilight Princess] {item_name=} not in prefill pool"
                    for _ in range(
                        len(VANILLA_BIG_KEY_LOCATIONS[dungeon_name][item_name])
                    ):
                        # This could deal with small keys on bosses but I think item rules would be better
                        # collection_state_small_key.collect(self.create_item(item_name))
                        collection_state_map_and_compass.collect(
                            self.create_item(item_name)
                        )

        if self.options.map_and_compass_settings.in_dungeon:
            for dungeon_name in VANILLA_MAP_AND_COMPASS_LOCATIONS:
                for item_name in VANILLA_MAP_AND_COMPASS_LOCATIONS[dungeon_name]:
                    assert (
                        item_name in self.prefill_pool
                    ), f"[Twilight Princess] {item_name=} not in prefill pool"
                    # Realisticlly this is not needed
                    for _ in range(
                        len(VANILLA_MAP_AND_COMPASS_LOCATIONS[dungeon_name][item_name])
                    ):
                        collection_state_small_key.collect(self.create_item(item_name))
                        collection_state_big_key.collect(self.create_item(item_name))

        collection_state_small_key.sweep_for_advancements()
        collection_state_big_key.sweep_for_advancements()
        collection_state_map_and_compass.sweep_for_advancements()

        # All the information about what is to be pre filled is stored here to condense code
        options = [
            self.options.small_key_settings,
            self.options.big_key_settings,
            self.options.map_and_compass_settings,
        ]
        settings = [SmallKeySettings, BigKeySettings, MapAndCompassSettings]
        vanillas = [
            VANILLA_SMALL_KEYS_LOCATIONS,
            VANILLA_BIG_KEY_LOCATIONS,
            VANILLA_MAP_AND_COMPASS_LOCATIONS,
        ]

        for dungeon_name in VANILLA_SMALL_KEYS_LOCATIONS:
            for item_name in VANILLA_SMALL_KEYS_LOCATIONS[dungeon_name]:
                assert collection_state_big_key.has(
                    item_name,
                    self.player,
                    len(VANILLA_SMALL_KEYS_LOCATIONS[dungeon_name][item_name]) - 1,
                ), f"[Twilight Princess] {item_name} not in big key state count={collection_state_big_key.count(item_name,self.player)}"
                assert collection_state_map_and_compass.has(
                    item_name,
                    self.player,
                    len(VANILLA_SMALL_KEYS_LOCATIONS[dungeon_name][item_name]) - 1,
                ), f"[Twilight Princess] {item_name} not in MnC state count={collection_state_map_and_compass.count(item_name,self.player)}"

        for dungeon_name in VANILLA_BIG_KEY_LOCATIONS:
            for item_name in VANILLA_BIG_KEY_LOCATIONS[dungeon_name]:
                assert collection_state_map_and_compass.has(
                    item_name,
                    self.player,
                    len(VANILLA_BIG_KEY_LOCATIONS[dungeon_name][item_name]) - 1,
                ), f"[Twilight Princess] {item_name} not in MnC state count={collection_state_map_and_compass.count(item_name,self.player)}"

        for dungeon_name in VANILLA_MAP_AND_COMPASS_LOCATIONS:
            for item_name in VANILLA_MAP_AND_COMPASS_LOCATIONS[dungeon_name]:
                assert collection_state_big_key.has(
                    item_name,
                    self.player,
                    len(VANILLA_MAP_AND_COMPASS_LOCATIONS[dungeon_name][item_name]) - 1,
                ), f"[Twilight Princess] {item_name} not in big key state count={collection_state_big_key.count(item_name,self.player)}"
                assert collection_state_small_key.has(
                    item_name,
                    self.player,
                    len(VANILLA_MAP_AND_COMPASS_LOCATIONS[dungeon_name][item_name]) - 1,
                ), f"[Twilight Princess] {item_name} not in small key state count={collection_state_small_key.count(item_name,self.player)}"

        # endregion

        # region DungeonItem-Prefill

        dungeon_name = None
        item_name = None

        def on_place(location):
            # logging.info(location.name)
            pass

        # Place Vanilla items first so that they are ensured to be placed correctly
        #   Note: This will will put items even if precollected
        for option, setting, vanilla, state in zip(
            options, settings, vanillas, collection_states
        ):
            if option.value == setting.option_vanilla:
                for dungeon_name in vanilla:
                    for item_name in vanilla[dungeon_name]:
                        if (
                            item_name == "Hyrule Castle Big Key"
                            and self.options.castle_bk_requirements.value
                            != CastleBKRequirements.option_none
                        ):
                            continue  # handled in place deterministic

                        assert (
                            item_name in ITEM_TABLE
                        ), f"[Twilight Princess] {item_name=}"
                        assert (
                            item_name in self.prefill_pool
                        ), f"[Twilight Princess] {item_name=}"

                        items = list(
                            filter(lambda item: item.name == item_name, pre_fill_items)
                        )

                        assert isinstance(
                            items, list
                        ), f"[Twilight Princess] (Vanilla) Items not list ({item_name}){items=}"
                        assert (
                            len(items) > 0
                        ), f"[Twilight Princess] (Vanilla) No items found in pre fill items {item_name=}"
                        assert len(items) == len(
                            vanilla[dungeon_name][item_name]
                        ), f"[Twilight Princess] (Vanilla) Items does not match number needed {items=}"

                        locations_base = [
                            self.get_location(location_name)
                            for location_name in vanilla[dungeon_name][item_name]
                        ]
                        locations = [
                            location
                            for location in locations_base
                            if location.item is None and location.address is not None
                        ]
                        assert (
                            len(locations) > 0
                        ), f"[Twilight Princess] (Vanilla) Locations not avaliable {locations_base=}, {item_name=} "
                        assert len(locations) == len(
                            vanilla[dungeon_name][item_name]
                        ), f"[Twilight Princess] (Vanilla) Some locations not avaliable {locations=}"

                        for item, location in zip(items, locations):
                            location.place_locked_item(item)
                            pre_fill_items.remove(item)
                            state.collect(item)

            # sanity check
            dungeon_name = None
            item_name = None

        for option, setting, vanilla, state in zip(
            options, settings, vanillas, collection_states
        ):
            if option.value == setting.option_own_dungeon:
                for dungeon_name in vanilla:

                    locations_base = [
                        self.get_location(location)
                        for location, data in LOCATION_TABLE.items()
                        if data.stage_id.value == dungeon_name
                    ]
                    locations = [
                        location
                        for location in locations_base
                        if location.item is None and location.address is not None
                    ]
                    assert (
                        len(locations) > 0
                    ), f"[Twilight Princess] (Own Dungeon) no locations for {dungeon_name=}"

                    # !!
                    items: list[Item] = []

                    for item_name in vanilla[dungeon_name]:
                        if (
                            item_name == "Hyrule Castle Big Key"
                            and self.options.castle_bk_requirements.value
                            != CastleBKRequirements.option_none
                        ):
                            continue  # handled in place deterministic

                        assert item_name in ITEM_TABLE
                        assert item_name in self.prefill_pool

                        # Don't place item if its precollected
                        skip_item = False

                        new_item = list(
                            filter(lambda item: item.name == item_name, pre_fill_items)
                        )

                        for item in starting_pool_copy:
                            if item.name == item_name:
                                skip_item = True
                                starting_pool_copy.remove(item)
                                break

                        if skip_item:
                            for nu_item in new_item:
                                pre_fill_items.remove(nu_item)
                            continue

                        items.extend(new_item)

                    # Sanity check
                    item_name = None

                    # Palace of Twilight needs arbiters grounds to be able to be commpleted
                    state_copy = None
                    if dungeon_name == "Palace of Twilight":
                        state_copy = state.copy()
                        if not state.has("Arbiters Grounds Big Key", self.player):
                            state.collect(self.create_item("Arbiters Grounds Big Key"))
                        if not state.has("Arbiters Grounds Small Key", self.player, 5):
                            for _ in range(5):
                                state.collect(
                                    self.create_item("Arbiters Grounds Small Key")
                                )

                        if (
                            self.options.palace_requirements
                            == PalaceRequirements.option_vanilla
                        ):
                            state.collect(self.boss_defeat_items["Argorok"])
                        state.sweep_for_advancements()

                    elif dungeon_name == "Hyrule Castle":
                        state_copy = state.copy()

                        if (
                            self.options.castle_requirements
                            == CastleRequirements.option_dungeons
                        ):
                            for name, item in self.boss_defeat_items.items():
                                state.collect(item)
                        elif (
                            self.options.castle_requirements
                            == CastleRequirements.option_vanilla
                        ):
                            state.collect(self.boss_defeat_items["Zant"])

                        state.sweep_for_advancements()

                    assert len(locations) >= len(
                        items
                    ), f"[Twilight Princess] (Own Dungeon) There are not enough locations for items with {setting.display_name=} in {dungeon_name=} acording to final counts {locations=}, {items=}"

                    items_copy = deepcopy(items)
                    self.multiworld.random.shuffle(items_copy)
                    self.multiworld.random.shuffle(locations)

                    fill_restrictive(
                        self.multiworld,
                        state,
                        locations,
                        items,
                        single_player_placement=True,
                        lock=True,
                        allow_excluded=True,
                        on_place=on_place,
                    )

                    # All items should be placed
                    assert (
                        len(items) == 0
                    ), f"[Twilight Princess] (Own dungeon) Not all items placed {items=}"

                    # Restore state if in palace of twilight
                    if state_copy:
                        state = state_copy

                    for item in items_copy:
                        pre_fill_items.remove(item)
                        state.collect(item)

            # sanity check
            dungeon_name = None
            item_name = None

        for option, setting, vanilla, state in zip(
            options, settings, vanillas, collection_states
        ):
            if option.value == setting.option_any_dungeon:
                items = []
                locations = []
                skip_hyrule_castle = False
                skip_palace_of_twilight = False
                skip_forest_temple = False
                for dungeon_name in vanilla:

                    if dungeon_name == "Hyrule Castle":
                        if self.options.castle_requirements.value in [
                            CastleRequirements.option_vanilla,
                            CastleRequirements.option_dungeons,
                        ]:
                            skip_hyrule_castle = True
                            continue
                    elif dungeon_name == "Palace of Twilight":
                        if (
                            self.options.palace_requirements.value
                            == PalaceRequirements.option_vanilla
                        ):
                            skip_palace_of_twilight = True
                            continue
                    elif dungeon_name == "Forest Temple":
                        if (
                            self.options.faron_woods_logic
                            == FaronWoodsLogic.option_closed
                        ):
                            skip_forest_temple = True
                            continue

                    locations_base = [
                        self.get_location(location)
                        for location, data in LOCATION_TABLE.items()
                        if data.stage_id.value == dungeon_name
                    ]
                    new_locations = [
                        location
                        for location in locations_base
                        if location.item is None
                        and location.address is not None
                        and location not in locations
                    ]
                    assert (
                        len(new_locations) > 0
                    ), f"[Twilight Princess] (Any Dungeon) no locations for {dungeon_name=}"

                    locations.extend(new_locations)

                    for item_name in vanilla[dungeon_name]:
                        if (
                            item_name == "Hyrule Castle Big Key"
                            and self.options.castle_bk_requirements.value
                            != CastleBKRequirements.option_none
                        ):
                            continue  # handled in place deterministic

                        assert item_name in ITEM_TABLE
                        assert item_name in self.prefill_pool

                        new_items = list(
                            filter(lambda item: item.name == item_name, pre_fill_items)
                        )

                        # Don't place item if its precollected
                        skip_item = False

                        for item in starting_pool_copy:
                            if item.name == item_name:
                                skip_item = True
                                starting_pool_copy.remove(item)
                                break
                        if skip_item:
                            for nu_item in new_items:
                                pre_fill_items.remove(nu_item)
                            continue

                        items.extend(new_items)

                    # Sanity check
                    item_name = None

                assert len(locations) >= len(
                    items
                ), f"[Twilight Princess] (Any Dungeon) There are not enough locations for items with {setting.display_name=} in {dungeon_name=} acording to final counts {locations=}, {items=}"

                items_copy = deepcopy(items)
                self.multiworld.random.shuffle(items)
                self.multiworld.random.shuffle(locations)

                fill_restrictive(
                    self.multiworld,
                    state,
                    locations,
                    items,
                    single_player_placement=True,
                    lock=True,
                    allow_excluded=True,
                    on_place=on_place,
                )

                # All items should be placed
                assert (
                    len(items) == 0
                ), f"[Twilight Princess] (Any dungeon) Not all items placed {items=}"

                for item in items_copy:
                    pre_fill_items.remove(item)
                    state.collect(item)

                # Now deal with POT and HC items
                # Which will be own_dungeon
                skipped_dungeons = []
                if skip_hyrule_castle:
                    skipped_dungeons.append("Hyrule Castle")
                if skip_palace_of_twilight:
                    skipped_dungeons.append("Palace of Twilight")
                if skip_forest_temple:
                    skipped_dungeons.append("Forest Temple")
                for dungeon_name in skipped_dungeons:

                    locations_base = [
                        self.get_location(location)
                        for location, data in LOCATION_TABLE.items()
                        if data.stage_id.value == dungeon_name
                    ]
                    locations = [
                        location
                        for location in locations_base
                        if location.item is None and location.address is not None
                    ]
                    assert (
                        len(locations) > 0
                    ), f"[Twilight Princess] (Any-Own Dungeon) no locations for {dungeon_name=}"

                    # !!
                    items: list[Item] = []

                    for item_name in vanilla[dungeon_name]:
                        if (
                            item_name == "Hyrule Castle Big Key"
                            and self.options.castle_bk_requirements.value
                            != CastleBKRequirements.option_none
                        ):
                            continue  # handled in place deterministic

                        assert item_name in ITEM_TABLE
                        assert item_name in self.prefill_pool

                        new_items = list(
                            filter(lambda item: item.name == item_name, pre_fill_items)
                        )

                        # Don't place item if its precollected
                        skip_item = False
                        for item in starting_pool_copy:
                            if item.name == item_name:
                                skip_item = True
                                starting_pool_copy.remove(item)
                                break
                        if skip_item:
                            for nu_item in new_item:
                                pre_fill_items.remove(nu_item)
                            continue

                        items.extend(new_items)

                    # Sanity check
                    item_name = None

                    # Palace of Twilight needs arbiters grounds to be able to be commpleted
                    state_copy = None
                    if dungeon_name == "Palace of Twilight":
                        state_copy = state.copy()
                        if not state.has("Arbiters Grounds Big Key", self.player):
                            state.collect(self.create_item("Arbiters Grounds Big Key"))
                        if not state.has("Arbiters Grounds Small Key", self.player, 5):
                            for _ in range(5):
                                state.collect(
                                    self.create_item("Arbiters Grounds Small Key")
                                )

                        if (
                            self.options.palace_requirements
                            == PalaceRequirements.option_vanilla
                        ):
                            state.collect(self.boss_defeat_items["Argorok"])
                        state.sweep_for_advancements()

                    elif dungeon_name == "Hyrule Castle":
                        state_copy = state.copy()

                        if (
                            self.options.castle_requirements
                            == CastleRequirements.option_dungeons
                        ):
                            for name, item in self.boss_defeat_items.items():
                                state.collect(item)
                        elif (
                            self.options.castle_requirements
                            == CastleRequirements.option_vanilla
                        ):
                            state.collect(self.boss_defeat_items["Zant"])

                    assert len(locations) >= len(
                        items
                    ), f"[Twilight Princess] (Any-Own Dungeon) There are not enough locations for items with {setting.display_name=} in {dungeon_name=} acording to final counts {locations=}, {items=}"

                    items_copy = deepcopy(items)
                    self.multiworld.random.shuffle(items_copy)
                    self.multiworld.random.shuffle(locations)

                    fill_restrictive(
                        self.multiworld,
                        state,
                        locations,
                        items,
                        single_player_placement=True,
                        lock=True,
                        allow_excluded=True,
                        on_place=on_place,
                    )

                    # All items should be placed
                    assert (
                        len(items) == 0
                    ), f"[Twilight Princess] (Any-Own dungeon) Not all items placed {items=}"

                    # Restore state if in palace of twilight
                    if state_copy:
                        state = state_copy

                    for item in items_copy:
                        pre_fill_items.remove(item)
                        state.collect(item)

            # sanity check
            dungeon_name = None
            item_name = None
        # endregion

        # All items in the pre fill pool need to be processed in the pre fill
        assert (
            len(pre_fill_items) == 0
        ), f"[Twilight Princess] Not all pre fill items placed {pre_fill_items=}"

        for location in self.multiworld.get_filled_locations(self.player):
            if location.address != None and location.item.advancement:
                if location.progress_type == LocationProgressType.EXCLUDED:
                    location.progress_type = LocationProgressType.DEFAULT

    def post_fill(self):
        self.seed_id = gen_seed_id(self)
        # Post fill location type checking removed due to changing location types based on prefilled items

        return super().post_fill()

    def generate_output(self, output_directory: str) -> None:
        """
        Create the output APTP file that is used to randomize the GCI.

        :param output_directory: The output directory for the APTP file.
        """
        multiworld = self.multiworld
        player = self.player

        item_str, debug_str = get_item_placements(self.multiworld, self.player)

        setting_string = get_setting_string(self.multiworld, self.player)

        # Output the settings and item_placement to file.
        file_path = os.path.join(
            output_directory,
            f"{multiworld.get_out_file_name_base(player)}",
        )
        seed_string = f"{setting_string},{item_str},{self.player_name},{self.seed_id}"
        # with open(f"{file_path}.txt", "w") as f:
        #     f.write(seed_string)

        aptp = TPPlayerContainer(
            seed_string, f"{file_path}.aptp", self.player_name, self.player
        )
        aptp.write()

        # puml_path = file_path = os.path.join(
        #     output_directory, f"{multiworld.get_out_file_name_base(player)}.puml"
        # )
        # visualize_regions(
        #     self.multiworld.get_region("Menu", self.player),
        #     puml_path,
        #     show_entrance_names=True,
        #     regions_to_highlight=self.multiworld.get_all_state(
        #         self.player
        #     ).reachable_regions[self.player],
        # )

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        """
        Fill in additional information text into locations, displayed when hinted.

        :param hint_data: A dictionary of mapping a player ID to a dictionary mapping location IDs to the extra hint
        information text. This dictionary should be modified as a side-effect of this method.
        """
        # Build out the hint data for this player. by telling them where each location is.
        # Regardless of ER settings, always hint the outermost entrance for every "interior" location
        hint_data[self.player] = {}
        for location in self.multiworld.get_locations(self.player):
            if location.address is not None and location.item is not None:
                assert isinstance(
                    location, TPLocation
                ), f"[Twilight Princess] {location=}"
                assert location.stage_id is not None, f"[Twilight Princess] {location=}"
                hint_data[self.player][location.address] = location.stage_id.name

    # Overides the base classification of an item if not None
    def determine_item_classification(self, name: str) -> IC | None:
        assert isinstance(name, str), f"[Twilight Princess] {name=}"
        assert name in ITEM_TABLE, f"[Twilight Princess] {name=}"

        adjusted_classification = None
        if False or (
            name == "Piece of Heart"
            and all(
                [
                    self.options.dungeons_shuffled.value
                    == DungeonsShuffled.option_false,
                    self.options.dungeon_rewards_progression.value
                    == DungeonRewardsProgression.option_anything,
                    self.options.heart_piece_shuffled.value
                    == HeartPieceShuffled.option_false,
                    self.options.hidden_skills_shuffled.value
                    == HiddenSkillsShuffled.option_false,
                    self.options.npc_items_shuffled.value
                    == NpcItemsShuffled.option_false,
                    self.options.poe_shuffled.value == PoeShuffled.option_true,
                    self.options.shop_items_shuffled.value
                    == ShopItemsShuffled.option_false,
                    self.options.sky_characters_shuffled.value
                    == SkyCharactersShuffled.option_false,
                ]
            )
        ):
            adjusted_classification = IC.filler

        return adjusted_classification

    def create_item(self, name: str) -> TPItem:
        """
        Create an item for this world type and player.

        :param name: The name of the item to create.
        :raises KeyError: If an invalid item name is provided.
        """
        assert isinstance(name, str), f"[Twilight Princess] {name=}"
        assert name in ITEM_TABLE, f"[Twilight Princess] {name}"

        return TPItem(
            name,
            self.player,
            ITEM_TABLE[name],
            self.determine_item_classification(name),
        )

    def get_filler_item_name(self) -> str:
        """
        This method is called when the item pool needs to be filled with additional items to match the location count.

        :return: The name of a filler item from this world.
        """

        # If there are still useful items to place, place those first.
        if len(self.useful_pool) > 0:
            return self.useful_pool.pop()

        # If there are still vanilla filler items to place, place those first.
        if len(self.filler_pool) > 0:
            return self.filler_pool.pop()

        assert len(self.useful_pool) == 0
        assert len(self.filler_pool) == 0

        # Use the same weights for filler items used in the base randomizer.
        filler_consumables = [
            # "Green Rupee",
            # "Blue Rupee",
            # "Yellow Rupee",
            # "Red Rupee",
            "Purple Rupee",
            "Orange Rupee",
            "Silver Rupee",
            # "Arrows (10)",
            # "Arrows (20)",
            "Arrows (30)",
            "Seeds (50)",
            # "Bombs (5)",
            # "Bombs (10)",
            # "Bombs (20)",
            "Bombs (30)",
            # "Bomblings (3)",
            # "Bomblings (5)",
            "Bomblings (10)",
            # "Water Bombs (3)",
            # "Water Bombs (5)",
            "Water Bombs (10)",
            "Ice Trap",
        ]
        filler_weights = [
            # 1,  # Green Rupee
            # 2,  # Blue Rupee
            # 3,  # Yellow Rupee
            # 1,  # Red Rupee
            2,  # Purple Rupee
            3,  # Orange Rupee
            2,  # Silver Rupee
            # 1,  # Arrows 10
            # 2,  # Arrows 20
            1,  # Arrows 30
            1,  # Seeds 50
            # 1,  # Bombs 5
            # 2,  # Bombs 10
            # 2,  # Bombs 20
            1,  # Bombs 30
            # 1,  # Bomblings 3
            # 2,  # Bomblings 5
            1,  # Bomblings 10
            # 1,  # Water Bombs 3
            # 2,  # Water Bombs 5
            1,  # Water Bombs 10
            self.options.trap_frequency.value,  # Ice Trap
        ]
        assert len(filler_consumables) == len(
            filler_weights
        ), f"[Twilight Princess] {len(filler_consumables)=}, {len(filler_weights)=}"
        return self.multiworld.random.choices(
            filler_consumables, weights=filler_weights, k=1
        )[0]

    def get_pre_fill_items(self) -> list[Item]:
        """
        Return items that need to be collected when creating a fresh `all_state` but don't exist in the multiworld's
        item pool.

        :return: A list of pre-fill items.
        """
        pre_fiill_items = item_factory(self.prefill_pool, self)
        if pre_fiill_items:
            assert isinstance(pre_fiill_items, list)
        return pre_fiill_items

    def fill_slot_data(self) -> Mapping[str, Any]:
        """
        Return the `slot_data` field that will be in the `Connected` network package.

        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response.

        :return: A dictionary to be sent to the client when it connects to the server.
        """
        slot_data = {
            "World Version": VERSION,
            "DeathLink": self.options.death_link.value,
            "Settings": self.get_settings_map(),
            "LocationClassification": {},
            "SeedID": self.seed_id,
            "StartInventory": [
                item.code for item in self.multiworld.precollected_items[self.player]
            ],
        }

        for location in self.get_locations():
            assert isinstance(location, TPLocation)
            if location.progress_type == LocationProgressType.PRIORITY:
                location_classification = "Priority"
            elif location.progress_type == LocationProgressType.EXCLUDED:
                location_classification = "Excluded"
            else:
                continue

            slot_data["LocationClassification"][
                f"{TPLocation.get_apid(location.code) if location.code != None else location.name}"
            ] = location_classification

        return slot_data

    def collect_item(
        self, state: "CollectionState", item: "Item", remove: bool = False
    ) -> Optional[str]:
        """
        Collect an item name into state. For speed reasons items that aren't logically useful get skipped.
        Collect None to skip item.
        :param state: CollectionState to collect into
        :param item: Item to decide on if it should be collected into state
        :param remove: indicate if this is meant to remove from state instead of adding.
        """
        if item.advancement:
            return item.name
        return None

    def get_settings_map(self):
        """A map of all the settings for slot data, settings marked 'Gen only' only affect placement of items not in game changes
        See ClientUtils.py L:6 for a full break down of the possible values"""
        return {
            # Time Savers
            "Skip Minor Cutscenes": self.options.skip_minor_cutscenes.get_option_name(
                self.options.skip_minor_cutscenes.value
            ),
            "Skip Major Cutscenes": self.options.skip_major_cutscenes.get_option_name(
                self.options.skip_major_cutscenes.value
            ),
            "Fast Iron Boots": self.options.fast_iron_boots.get_option_name(
                self.options.fast_iron_boots.value
            ),
            "Quick Transform": self.options.quick_transform.get_option_name(
                self.options.quick_transform.value
            ),
            "Instant Message Text": self.options.instant_message_text.get_option_name(
                self.options.instant_message_text.value
            ),
            "Open Map": self.options.open_map.get_option_name(
                self.options.open_map.value
            ),
            "Increase Spinner Speed": self.options.increase_spinner_speed.get_option_name(
                self.options.increase_spinner_speed.value
            ),
            "Open Door of Time": self.options.open_door_of_time.get_option_name(
                self.options.open_door_of_time.value
            ),
            "Early Shadow Crystal": self.options.early_shadow_crystal.get_option_name(  # Gen only
                self.options.early_shadow_crystal.value
            ),
            "Goron Mines Shortcut": self.options.goron_mines_sc.get_option_name(
                self.options.goron_mines_sc.value
            ),
            "Castle Shortcut": self.options.castle_sc.get_option_name(
                self.options.castle_sc.value
            ),
            "Skip Bridge Donation": self.options.skip_bridge_don.get_option_name(
                self.options.skip_bridge_don.value
            ),
            # Additional Settings
            "Transform Anywhere": self.options.transform_anywhere.get_option_name(
                self.options.transform_anywhere.value
            ),
            "Wallet Size": self.options.wallet_size.get_option_name(
                self.options.wallet_size.value
            ),
            "Auto Fill Wallet": self.options.auto_fill_wallet.get_option_name(
                self.options.auto_fill_wallet.value
            ),
            "Bonks do Damage": self.options.bonks_do_damage.get_option_name(
                self.options.bonks_do_damage.value
            ),
            "Trap Frequency": self.options.trap_frequency.get_option_name(
                self.options.trap_frequency.value
            ),
            "Damage Magnification": self.options.damage_magnification.get_option_name(
                self.options.damage_magnification.value
            ),
            "Starting ToD": self.options.starting_tod.get_option_name(
                self.options.starting_tod.value
            ),
            "Ilia Quest": self.options.ilia_quest.get_option_name(  # Gen only
                self.options.ilia_quest.value
            ),
            "Modify Shop Models": self.options.modify_shop_models.get_option_name(
                self.options.modify_shop_models.value
            ),
            # Dungeon Entrance Settings
            "Goron Mines Entrance Requirements": self.options.goron_mines_entrance.get_option_name(
                self.options.goron_mines_entrance.value
            ),
            "Lakebed Entrance Requirements": self.options.skip_lakebed_entrance.get_option_name(
                self.options.skip_lakebed_entrance.value
            ),
            "Arbiters Grounds Entrance Requirements": self.options.skip_arbiters_grounds_entrance.get_option_name(
                self.options.skip_arbiters_grounds_entrance.value
            ),
            "Snowpeak Entrance Requirements": self.options.skip_snowpeak_entrance.get_option_name(
                self.options.skip_snowpeak_entrance.value
            ),
            "Sacred Grove Entrance Requirements": self.options.grove_entrance.get_option_name(
                self.options.grove_entrance.value
            ),
            "City in the Sky Entrance Requirements": self.options.skip_city_in_the_sky_entrance.get_option_name(
                self.options.skip_city_in_the_sky_entrance.value
            ),
            # Logic Settings
            "Logic Settings": self.options.logic_rules.get_option_name(  # Gen only
                self.options.logic_rules.value
            ),
            "Castle Requirements": self.options.castle_requirements.get_option_name(
                self.options.castle_requirements.value
            ),
            "Castle Requirements Count": self.options.castle_requirements_count.get_option_name(
                self.options.castle_requirements_count.value
            ),
            "Castle Big Key Requirements": self.options.castle_bk_requirements.get_option_name(
                self.options.castle_bk_requirements.value
            ),
            "Castle Big Key Requirements Count": self.options.castle_bk_requirements_count.get_option_name(
                self.options.castle_bk_requirements_count.value
            ),
            "Palace of Twilight Requirements": self.options.palace_requirements.get_option_name(
                self.options.palace_requirements.value
            ),
            "Faron Woods Logic": self.options.faron_woods_logic.get_option_name(
                self.options.faron_woods_logic.value
            ),
            # Item Pool / Location settings
            "Golden Bugs Shuffled": self.options.golden_bugs_shuffled.get_option_name(  # Gen only
                self.options.golden_bugs_shuffled.value
            ),
            "Sky Chracters Shuffled": self.options.sky_characters_shuffled.get_option_name(  # Gen only
                self.options.sky_characters_shuffled.value
            ),
            "NPC Items Shuffled": self.options.npc_items_shuffled.get_option_name(  # Gen only
                self.options.npc_items_shuffled.value
            ),
            "Shop Items Shuffled": self.options.shop_items_shuffled.get_option_name(  # Gen only
                self.options.shop_items_shuffled.value
            ),
            "Hidden Skills Shuffled": self.options.hidden_skills_shuffled.get_option_name(  # Gen only
                self.options.hidden_skills_shuffled.value
            ),
            "Poes Shuffled": self.options.poe_shuffled.get_option_name(  # Gen only
                self.options.poe_shuffled.value
            ),
            "Heart Pieces Shuffled": self.options.heart_piece_shuffled.get_option_name(  # Gen only
                self.options.heart_piece_shuffled.value
            ),
            "Overworld Shuffled": self.options.overworld_shuffled.get_option_name(  # Gen only
                self.options.overworld_shuffled.value
            ),
            "Dungeons Shuffled": self.options.dungeons_shuffled.get_option_name(  # Gen only
                self.options.dungeons_shuffled.value
            ),
            # Dungeon Items
            "Dungeon Rewards Progression": self.options.dungeon_rewards_progression.get_option_name(  # Gen only
                self.options.dungeon_rewards_progression.value
            ),
            "Small Key Settings": self.options.small_key_settings.get_option_name(  # Gen only
                self.options.small_key_settings.value
            ),
            "Big Key Settings": self.options.big_key_settings.get_option_name(  # Gen only
                self.options.big_key_settings.value
            ),
            "Map and Compass Settings": self.options.map_and_compass_settings.get_option_name(  # Gen only
                self.options.map_and_compass_settings.value
            ),
            "Small Keys On Bosses": self.options.small_keys_on_bosses.get_option_name(  # Gen only
                self.options.small_keys_on_bosses.value
            ),
        }
