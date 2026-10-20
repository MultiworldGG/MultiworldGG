import os
import pkgutil
from typing import ClassVar, Any

from BaseClasses import MultiWorld, Region, Entrance, Tutorial, ItemClassification
from NetUtils import MultiData
from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess, icon_paths
from math import ceil
from .constants import *
from .items import PokemonSnapItem, PokemonSnapItemCategory, key_item_names, useful_item_names, \
    _all_items, build_item_pool, build_required_item_pool, PokemonSnapItemData, item_dictionary, POKEMON_PIC_NAMES, SIGN_PIC_NAMES
from .locations import PokemonSnapLocation, PokemonSnapLocationCategory, location_tables, bonus, wonderful, \
    RNG_LOCATIONS, HARD_LOCATIONS
from .options import PokemonSnapOption, PhotoBonusChecks, FillerItemNamingScheme, PressLToStop, pokemon_snap_option_groups, GoalType
from .psnap_settings import PokemonSnapSettings
from .rom import PokemonSnapProcedurePatch
from .rules import set_rules


def run_client(*args):
    from .client import main  # lazy import
    launch_subprocess(main, name="PokemonSnapClient", args=args)

# Adds the launcher for our component and our client logo.
icon_paths['pokemon_snap_icon'] = f"ap:{__name__}/icon.png"
components.append(
    Component("Pokemon Snap Client", func=run_client, component_type=Type.CLIENT,
              file_identifier=SuffixIdentifier(".apsnap"), icon="pokemon_snap_icon"))


class PokemonSnapWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the MultiworldGG Pokemon Snap randomizer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin", "SomeJakeGuy", "gerbiljames", "nielrenned", "cobyw"]
    )

    tutorials = [setup_en]
    option_groups = pokemon_snap_option_groups


class PokemonSnapWorld(World):
    """
    Pokemon Snap is a game about taking photographs of monsters to score points.
    """

    game = "Pokemon Snap"
    web = PokemonSnapWeb()

    options_dataclass = PokemonSnapOption
    options: PokemonSnapOption
    topology_present: bool = True

    enabled_location_categories: set[PokemonSnapLocationCategory]
    required_client_version = (0, 6, 7)
    item_name_to_id = PokemonSnapItem.get_name_to_id()
    location_name_to_id = PokemonSnapLocation.get_name_to_id()
    item_name_groups = items.item_name_groups
    settings: ClassVar[PokemonSnapSettings]
    start_area: PokemonSnapItemData
    auth: bytes

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.enabled_location_categories = set()

    def generate_early(self):
        self.enabled_location_categories |= {
            PokemonSnapLocationCategory.NORMAL_PHOTO,
        }

        if self.options.photo_bonuses == PhotoBonusChecks.option_technique_and_multiple:
            self.enabled_location_categories.add(PokemonSnapLocationCategory.WONDERFUL_PHOTO)
            self.enabled_location_categories.add(PokemonSnapLocationCategory.MULTIPLE_PHOTO)
        elif self.options.photo_bonuses == PhotoBonusChecks.option_technique_only:
            self.enabled_location_categories.add(PokemonSnapLocationCategory.WONDERFUL_PHOTO)

        if self.options.special_poses:
            self.enabled_location_categories.add(PokemonSnapLocationCategory.SPECIAL_POSE)
        if self.options.pokemon_signs:
            self.enabled_location_categories.add(PokemonSnapLocationCategory.POKEMON_SIGN)
        if self.options.secret_exits:
            self.enabled_location_categories.add(PokemonSnapLocationCategory.SECRET_EXIT)
        if self.options.report_photo_count:
            self.enabled_location_categories.add(PokemonSnapLocationCategory.PHOTO_COUNT)
        if self.options.report_score_total:
            self.enabled_location_categories.add(PokemonSnapLocationCategory.REPORT_SCORE)


        # Per-seed connect token, baked into the ROM and registered server-side.
        self.auth = self.random.randbytes(16)

        # Starting course as precollected (build_item_pool excludes it). Exclude
        # Rainbow Cloud so the goal course can't be the start.
        areas = [item for item in _all_items
                 if item.category == PokemonSnapItemCategory.AREA
                 and item.name != LVL_CLOUD]
        self.start_area = self.random.choice(areas)
        self.multiworld.push_precollected(self.create_item(self.start_area.name))

        if self.options.start_with_dash_engine:
            self.multiworld.push_precollected(self.create_item(DASH_ENGINE))

        if self.options.enable_left_bumper_to_start_stop:
            self.options.left_bumper_to_start_stop.value = PressLToStop.option_start_with

        if not getattr(self.multiworld, "generation_is_fake", False):
            # Check that the options don't generate too much stuff
            base_fillable = sum(1 for table in location_tables.values() for loc in table if self.location_enabled(loc))
            max_fillable = 2 * base_fillable - 1 # double every location and then remove one for victory item
            if len(build_required_item_pool(self)) > max_fillable:
                raise OptionError(
                    f"YAML for Pokemon Snap - {self.player_name}: not enough locations for items. "
                    "Try reducing extra items or enabling more checks (`photo_bonuses` is a likely culprit)."
                )

    def create_regions(self):
        # Create Regions
        regions = {"Menu": self.create_region("Menu", [])}
        regions.update({region_name: self.create_region(region_name, region_entry)
                        for region_name, region_entry in location_tables.items()})

        # Create more locations, if necessary
        location_count = sum(1 for loc in self.multiworld.get_locations(self.player) if not loc.locked)
        required_count = len(build_item_pool(self))
        if getattr(self.multiworld, "generation_is_fake", False):
            # Fix Universal Tracker issue with bonus locations (since they are random)
            self.create_extra_locations(len(self.multiworld.get_locations(self.player)))
        elif location_count < required_count:
            self.create_extra_locations(required_count - location_count)

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        create_connection("Menu", START_GAME)

        create_connection(START_GAME, LVL_BEACH)
        create_connection(START_GAME, LVL_TUNNEL)
        create_connection(START_GAME, LVL_VOLCANO)
        create_connection(START_GAME, LVL_RIVER)
        create_connection(START_GAME, LVL_CAVE)
        create_connection(START_GAME, LVL_VALLEY)
        create_connection(START_GAME, LVL_CLOUD)

    def location_enabled(self, location) -> bool:
        return (
            location.category in self.enabled_location_categories and
            (location.name not in RNG_LOCATIONS  or self.options.rng_checks) and
            (location.name not in HARD_LOCATIONS or self.options.hard_checks)
        )

    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        for location in location_table:
            if not self.location_enabled(location): continue

            new_location = PokemonSnapLocation(
                self.player,
                location.name,
                location.category,
                self.location_name_to_id[location.name],
                new_region
            )

            # Place victory item
            if location.name == MEW and (not self.options.good_technique_mew_photo or self.options.photo_bonuses == PhotoBonusChecks.option_none):
                new_location.place_locked_item(self.create_item(VICTORY_ITEM_NAME))
            if location.name == wonderful(MEW) and self.options.good_technique_mew_photo:
                new_location.place_locked_item(self.create_item(VICTORY_ITEM_NAME))
            
            new_region.locations.append(new_location)
        
        self.multiworld.regions.append(new_region)
        return new_region

    def create_extra_locations(self, extra_count: int):
        all_locations = [(region, loc) for region in self.multiworld.get_regions(self.player) for loc in region.locations]
        self.random.shuffle(all_locations)
        for region, location in all_locations[:extra_count]:
            name = bonus(location.name)
            new_location = PokemonSnapLocation(
                self.player,
                name,
                location.category,
                self.location_name_to_id[name],
                region
            )
            region.locations.append(new_location)

    def create_items(self):
        item_pool = build_item_pool(self)
        self.multiworld.itempool.extend(
            self.create_item(item.name) for item in item_pool 
            if item.name not in ({FILM_UPGRADE} | POKEMON_PIC_NAMES | SIGN_PIC_NAMES)
        )

        # For Film Upgrades, Pokemon Pics, and Sign Pics, we need to upgrade some of the
        # items to "progression" instead of "useful" so that the world is completable.
        # But classifying every one of these items as "progression" can lead to fill
        # errors, so we'll only include the minimum amount necessary.

        # Add the pokemon pictures
        pokemon_pics = [item for item in item_pool if item.name in POKEMON_PIC_NAMES]
        self.random.shuffle(pokemon_pics)
        for i, item in enumerate(pokemon_pics):
            item_class = ItemClassification.useful
            # intentionally including an extra progressive pokemon picture here
            if self.options.goal_type == GoalType.option_pokemon_pictures and i < self.options.pokemon_required.value:
                item_class = ItemClassification.progression
            self.multiworld.itempool.append(self.create_classified_item(item.name, item_class))

        # Add the sign pictures
        sign_pics = [item for item in item_pool if item.name in SIGN_PIC_NAMES]
        self.random.shuffle(sign_pics)
        for i, item in enumerate(sign_pics):
            item_class = ItemClassification.useful
            # intentionally including an extra progressive sign here
            if self.options.goal_type == GoalType.option_signs and i < self.options.signs_required.value:
                item_class = ItemClassification.progression
            self.multiworld.itempool.append(self.create_classified_item(item.name, item_class))

        # Add the film upgrades
        film_upgrade_count = item_pool.count(item_dictionary[FILM_UPGRADE])
        min_film = min(10 if self.options.hard_logic else 15, self.options.maximum_film)
        required_progressive = max(0, ceil((min_film - self.options.starting_film) / self.options.film_upgrade_amount))
        self.multiworld.itempool.extend(
            self.create_classified_item(FILM_UPGRADE, ItemClassification.progression_skip_balancing)
            for _ in range(required_progressive))
        self.multiworld.itempool.extend(
            self.create_classified_item(FILM_UPGRADE, ItemClassification.useful)
            for _ in range(film_upgrade_count - required_progressive))

    def create_item(self, name: str) -> PokemonSnapItem:
        if name in key_item_names:
            return self.create_classified_item(name, ItemClassification.progression)
        elif name in useful_item_names:
            return self.create_classified_item(name, ItemClassification.useful)
        else:
            return self.create_classified_item(name, ItemClassification.filler)

    def create_classified_item(self, name: str, classification: ItemClassification) -> PokemonSnapItem:
        return PokemonSnapItem(name, classification, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        if self.options.filler_item_names == FillerItemNamingScheme.option_flavorful: 
            return self.random.choice(items.filler_item_names)
        else:
            return SIMPLE_TRASH_ITEM_NAME

    def set_rules(self) -> None:
        set_rules(self)

    def modify_multidata(self, multidata: MultiData) -> None:
        import base64
        # Let the client connect with base64(token); a wrong-seed ROM's token
        # isn't registered here, so the server rejects it.
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.player_name]

    def generate_output(self, output_directory: str) -> None:
        from . import addresses as addr
        from worlds.Files import APTokenTypes

        patch = PokemonSnapProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff4"))
        patch.write_token(APTokenTypes.WRITE, addr.AUTH_ROM, self.auth)
        patch.write_file("token_patch.bin", patch.get_token_binary())
        out_path = os.path.join(
            output_directory,
            f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}")
        patch.write(out_path)

    def fill_slot_data(self) -> dict[str, Any]:
        return self.options.as_dict(
            "goal_type", "good_technique_mew_photo", "signs_required", "pokemon_required", "photo_scoring",
            "photo_bonuses", "pokemon_signs", "secret_exits", "report_photo_count",
            "report_score_total", "rng_checks", "hard_checks", "hard_logic",
            "left_bumper_to_start_stop", "camera_inversion",
            "starting_film", "film_upgrade_amount", "maximum_film", 
            "map_fragments", "per_course_items")