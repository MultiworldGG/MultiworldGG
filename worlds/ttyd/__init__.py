import logging
import os

from Fill import fill_restrictive, fast_fill
from typing import List, Dict, ClassVar, Any, Set
from settings import UserFilePath, Group
from BaseClasses import Tutorial, ItemClassification, CollectionState, Item, Location
from worlds.AutoWorld import WebWorld, World
from .Data import starting_partners, stars, limit_pit, \
    pit_exclusive_tattle_stars_required, dazzle_counts, dazzle_location_names, chapter_keysanity_tags, \
    chapter_keys, limited_tags, limited_tag_items
from .Enemy import Encounter, parse_json_encounters, randomize_encounters
from .Locations import all_locations, location_table, location_id_to_name, TTYDLocation, locationName_to_data, \
    get_locations_by_tags, get_vanilla_item_names, get_location_names, LocationData
from .Options import Piecesanity, TTYDOptions, YoshiColor, StartingPartner, PitItems, LimitChapterEight, Goal, \
    DazzleRewards, StarShuffle, EnemyRandomizer
from .Items import TTYDItem, itemList, item_table, ItemData, items_by_id
from .Regions import create_regions, connect_regions, get_regions_dict, register_indirect_connections
from .Rom import TTYDProcedurePatch, write_files
from .Rules import set_rules, get_tattle_rules_dict, set_tattle_rules, get_random_enemy_tattle_rules_dict
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess


def launch_client(*args):
    from .TTYDClient import launch
    launch_subprocess(launch, name="TTYD Client", args=args)


components.append(
    Component(
        "TTYD Client",
        func=launch_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apttyd"),
        description="Open the Paper Mario: The Thousand-Year Door client.",
    ),
)


class TTYDWebWorld(WebWorld):
    theme = 'partyTime'
    bug_report_page = "https://github.com/jamesbrq/ArchipelagoTTYD/issues"
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to setting up Paper Mario: The Thousand-Year Door for MultiworldGG.',
            language='English',
            file_name='setup_en.md',
            link='setup/en',
            authors=['jamesbrq']
        )
    ]


class TTYDSettings(Group):
    class DolphinPath(UserFilePath):
        """
        The location of the Dolphin you want to auto launch patched ROMs with
        """
        is_exe = True
        description = "Dolphin Executable"

    class RomFile(UserFilePath):
        """File name of the TTYD US iso"""
        copy_to = "Paper Mario - The Thousand-Year Door (USA).iso"
        description = "US TTYD .iso File"

    dolphin_path: DolphinPath = DolphinPath(None)
    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class TTYDWorld(World):
    """
    Paper Mario: The Thousand-Year Door is a quirky, turn-based RPG with a paper-craft twist.
    Mario teams up with oddball allies to stop an ancient evil sealed behind a magical door.
    Set in Rogueport, the game mixes platforming, puzzles, and witty, self-aware dialogue.
    Battles play out on a stage with timed button presses and a live audience cheering you on.
    """
    game = "Paper Mario: The Thousand-Year Door"
    web = TTYDWebWorld()

    options_dataclass = TTYDOptions
    options: TTYDOptions
    settings: ClassVar[TTYDSettings]
    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    required_client_version = (0, 6, 2)
    disabled_locations: set
    excluded_regions: set
    required_chapters: List[int]
    limited_chapters: List[int]
    limited_chapter_locations: Dict[int, Dict[str, Set[Location]]]
    limited_misc_locations: Set[Location]
    limited_misc_items: List[Item]
    limited_items: Dict[int, Dict[str, List[Item]]]
    limited_state: CollectionState = None
    locked_item_frequencies: Dict[str, int]
    in_pre_fill: bool
    encounters: list[Encounter] = None
    ut_can_gen_without_yaml = True


    def generate_early(self) -> None:
        self.disabled_locations = set()
        self.excluded_regions = set()
        self.required_chapters = []
        self.limited_chapters = []
        self.in_pre_fill = False
        self.limited_chapter_locations = {chapter: {tag: set() for tag in limited_tags[chapter]} for chapter in
                                          range(1, 9)}
        self.limited_items = {chapter: {tag: list() for tag in limited_tags[chapter]} for chapter in range(1, 9)}
        self.limited_misc_locations = set()
        self.locked_item_frequencies = {}
        self.encounters = parse_json_encounters()
        # implementing yaml-less UT support
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                slot_data = self.multiworld.re_gen_passthrough[self.game]
                self.options.goal.value = slot_data["goal"]
                self.options.goal_stars.value = slot_data["goal_stars"]
                self.options.palace_stars.value = slot_data["palace_stars"]
                self.options.pit_items.value = slot_data["pit_items"]
                self.options.limit_chapter_logic.value = slot_data["limit_chapter_logic"]
                self.options.limit_chapter_eight.value = slot_data["limit_chapter_eight"]
                self.options.palace_skip.value = slot_data["palace_skip"]
                self.options.open_westside.value = slot_data["westside"]
                self.options.tattlesanity.value = slot_data["tattlesanity"]
                self.options.dazzle_rewards.value = slot_data["dazzle_rewards"]
                self.options.star_shuffle.value = slot_data["star_shuffle"]
                self.options.disable_intermissions.value = slot_data["disable_intermissions"]
                self.options.piecesanity.value = slot_data["piecesanity"]
                self.options.shinesanity.value = slot_data["shinesanity"]
                self.options.blue_pipe_toggle.value = slot_data["blue_pipe_toggle"]
                self.options.enemy_randomizer.value = slot_data["enemy_randomizer"]
                return
        if self.options.limit_chapter_eight and self.options.palace_skip:
            logging.warning(f"{self.player_name}'s has enabled both Palace Skip and Limit Chapter 8. "
                            f"Disabling the Limit Chapter 8 option due to incompatibility.")
            self.options.limit_chapter_eight.value = LimitChapterEight.option_false
        if self.options.goal == Goal.option_bonetail and self.options.goal_stars < 5:
            logging.warning(f"{self.player_name}'s has Bonetail as the goal with less than 5 stars required. "
                            f"Increasing number of goal stars to 5 for accessibility.")
            self.options.goal_stars.value = 5
        if self.options.palace_stars > self.options.goal_stars:
            logging.warning(f"{self.player_name}'s has more palace stars required than goal stars. "
                            f"Reducing number of stars required to enter the palace of shadow for accessibility.")
            self.options.palace_stars.value = self.options.goal_stars.value
        chapters = [i for i in range(1, 8)]
        if not self.options.required_stars_toggle:
            for i in range(self.options.goal_stars.value):
                self.required_chapters.append(chapters.pop(self.multiworld.random.randint(0, len(chapters) - 1)))
        else:
            star_names = self.options.required_stars.value
            self.required_chapters = [chapter for name in star_names for chapter, star in stars.items() if star == name][:self.options.goal_stars.value]
            if len(self.required_chapters) < self.options.goal_stars.value:
                remaining_chapters = [i for i in range(1, 8) if i not in self.required_chapters]
                for _ in range(self.options.goal_stars.value - len(self.required_chapters)):
                    self.required_chapters.append(
                        remaining_chapters.pop(self.multiworld.random.randint(0, len(remaining_chapters) - 1)))
        if self.options.limit_chapter_logic:
            self.limited_chapters += [chapter for chapter in chapters if chapter not in self.required_chapters]
        if self.options.limit_chapter_eight:
            self.limited_chapters += [8]
        if self.options.palace_skip:
            self.excluded_regions.update(["Palace of Shadow", "Palace of Shadow (Post-Riddle Tower)"])
        if not self.options.tattlesanity:
            self.excluded_regions.update(["Tattlesanity"])
        if self.options.goal != Goal.option_shadow_queen:
            self.excluded_regions.update(["Shadow Queen"])
            if self.options.tattlesanity:
                self.disabled_locations.update(["Tattle: Shadow Queen"])
        if self.options.tattlesanity and self.options.disable_intermissions:
            self.disabled_locations.update(["Tattle: Lord Crump"])
        if self.options.enemy_randomizer != EnemyRandomizer.option_vanilla:
            randomize_encounters(self)
        if self.options.tattlesanity:
            extra_disabled = [location.name for name, locations in get_regions_dict().items()
                              if name in self.excluded_regions for location in locations]
            for location_name, locations in get_tattle_rules_dict().items():
                if len(locations) == 0:
                    if "Palace of Shadow (Post-Riddle Tower)" in self.excluded_regions:
                        self.disabled_locations.update([location_name])
                else:
                    if all([location_id_to_name[location] in self.disabled_locations or location_id_to_name[
                        location] in extra_disabled for location in locations]):
                        self.disabled_locations.update([location_name])

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)
        register_indirect_connections(self)
        self.lock_item_remove_from_pool("Rogueport Center: Goombella",
                                        starting_partners[self.options.starting_partner.value - 1])
        if self.options.star_shuffle == StarShuffle.option_vanilla:
            self.lock_vanilla_items_remove_from_pool(get_locations_by_tags("star"))
        elif self.options.star_shuffle == StarShuffle.option_stars_only:
            locations = get_locations_by_tags("star")
            items = [location.vanilla_item for location in locations]
            self.multiworld.random.shuffle(items)
            for i, location in enumerate(locations):
                self.lock_item_remove_from_pool(location.name, items_by_id[items[i]].item_name)
        if self.options.goal == Goal.option_shadow_queen:
            self.lock_item("Shadow Queen", "Victory")
        if self.options.limit_chapter_eight:
            for location in [location for location in get_locations_by_tags("chapter_8")]:
                if "Palace Key (Tower)" in location.name:
                    self.lock_item_remove_from_pool(location.name, "Palace Key (Tower)")
                elif "Palace Key" in location.name:
                    self.lock_item_remove_from_pool(location.name, "Palace Key")
            self.lock_item_remove_from_pool("Palace of Shadow Gloomtail Room: Star Key", "Star Key")
        if self.options.palace_skip:
            self.locked_item_frequencies["Palace Key"] = 3
            self.locked_item_frequencies["Palace Key (Tower)"] = 8
            self.locked_item_frequencies["Star Key"] = 1
        if self.options.pit_items == PitItems.option_vanilla:
            self.lock_vanilla_items_remove_from_pool(get_locations_by_tags("pit_floor"))
        if self.options.piecesanity == Piecesanity.option_vanilla:
            self.lock_vanilla_items_remove_from_pool(get_locations_by_tags(["star_piece", "panel"]))
        if self.options.piecesanity == Piecesanity.option_nonpanel_only:
            self.lock_vanilla_items_remove_from_pool(get_locations_by_tags("panel"))
        if not self.options.shinesanity:
            self.lock_vanilla_items_remove_from_pool(get_locations_by_tags("shine"))
        if not self.options.shopsanity:
            self.lock_vanilla_items_remove_from_pool(get_locations_by_tags("shop"))
        if self.options.pit_items == PitItems.option_filler:
            self.lock_filler_items_remove_from_pool(get_locations_by_tags("pit_floor"))
        if self.options.dazzle_rewards == DazzleRewards.option_vanilla:
            self.lock_vanilla_items_remove_from_pool(get_locations_by_tags("dazzle"))
        elif self.options.dazzle_rewards == DazzleRewards.option_filler:
            self.lock_filler_items_remove_from_pool(get_locations_by_tags("dazzle"))
        else:
            for i, location in enumerate(dazzle_location_names):
                if dazzle_counts[i] > 100 - self.locked_item_frequencies.get("Star Piece", 0):
                    self.lock_item(location, self.get_filler_item_name())
        for chapter in self.limited_chapters:
            self.lock_vanilla_items_remove_from_pool(
                [location for location in get_locations_by_tags(f"chapter_{chapter}")
                 if items_by_id[location.vanilla_item].item_name == "Star Piece" and self.get_location(
                    location.name).item is None])
        for chapter in self.limited_chapters:
            for tag in limited_tags[chapter]:
                locations = [self.get_location(location.name) for location in get_locations_by_tags(tag)
                             if location.name not in self.disabled_locations]
                locations = [location for location in locations if location.item is None]
                self.limited_chapter_locations[chapter][tag].update(locations)
        if 3 in self.limited_chapters and self.options.limit_chapter_logic:
            if self.get_location("Rogueport Blimp Room: Star Piece 1").item is None:
                self.lock_item_remove_from_pool("Rogueport Blimp Room: Star Piece 1", self.get_filler_item_name())
        if 5 in self.limited_chapters and self.options.limit_chapter_logic:
            self.lock_item_remove_from_pool("Rogueport Westside: Train Ticket", self.get_filler_item_name())
        if not self.options.keysanity:
            for i in range(1, 9):
                if i == 8 and self.options.limit_chapter_eight:
                    continue
                tags = [chapter_keysanity_tags[i]] + (["riddle_tower"] if i == 8 else [])
                locations = [self.get_location(location.name) for location in get_locations_by_tags(tags) if
                             location.name not in self.disabled_locations]
                locations = [location for location in locations if location.item is None]
                self.limited_chapter_locations[i][chapter_keysanity_tags[i]].update(locations)
        if self.options.tattlesanity:
            self.limit_tattle_locations()

    def limit_tattle_locations(self) -> None:
        # Existing pit-exclusive logic unchanged
        for stars_required, locations in pit_exclusive_tattle_stars_required.items():
            if stars_required > len(self.required_chapters):
                self.limited_misc_locations.update(
                    self.get_location(loc)
                    for loc in locations
                    if loc not in self.disabled_locations
                )

        # Flatten limited chapter location-ids
        all_limited_locations: set[int] = {
            loc.address
            for chapter_locs in self.limited_chapter_locations.values()
            for locs in chapter_locs.values()
            for loc in locs
        }

        base_rules = get_tattle_rules_dict()

        # Use randomized rules if enabled; otherwise base.
        # IMPORTANT: your get_random_enemy_tattle_rules_dict() should already do the
        # "if no matches -> use base rule" fallback.
        rules_dict = (
            get_random_enemy_tattle_rules_dict(self)
            if self.options.enemy_randomizer != EnemyRandomizer.option_vanilla
            else base_rules
        )

        for location_name, locations in rules_dict.items():
            if location_name in self.disabled_locations:
                continue

            # Chapter 8 clamp: if a tattle location has no gating locations, force-limit it.
            if self.options.limit_chapter_eight and not locations:
                self.limited_misc_locations.add(self.get_location(location_name))
                continue

            enabled_locations = [
                loc_id
                for loc_id in locations
                if location_id_to_name[loc_id] not in self.disabled_locations
            ]
            if not enabled_locations:
                continue

            if self.options.pit_items != PitItems.option_all:
                if all(loc_id in limit_pit for loc_id in enabled_locations):
                    self.limited_misc_locations.add(self.get_location(location_name))

            if self.options.limit_chapter_logic:
                # Keep your special-case, but apply it to the *effective* rules being used.
                if len(enabled_locations) == 1 and enabled_locations[0] == 78780511:
                    if 5 in self.limited_chapters:
                        self.limited_misc_locations.add(self.get_location(location_name))

                if all(loc_id in all_limited_locations for loc_id in enabled_locations):
                    self.limited_misc_locations.add(self.get_location(location_name))

    def create_items(self) -> None:
        required_items = []
        useful_items = []
        filler_items = []
        self.limited_state = CollectionState(self.multiworld)

        precollected_item_names = [item.name for item in self.multiworld.precollected_items[self.player]]

        item_names = [item.item_name for item in itemList for _ in
                      range(max(item.frequency - self.locked_item_frequencies.get(item.item_name, 0), 0))]

        for item_name in item_names:
            item = self.create_item(item_name)
            if item_name in precollected_item_names:
                precollected_item_names.remove(item_name)
                continue
            self.limited_state.collect(item, prevent_sweep=True)
            if ItemClassification.progression in item.classification:
                required_items.append(item)
            elif ItemClassification.useful in item.classification:
                useful_items.append(item)
            else:
                filler_items.append(item)

        if not self.options.keysanity:
            for chapter in range(1, 9):
                if chapter == 8 and self.options.limit_chapter_eight:
                    continue
                keys = [item for item in required_items if item.name in chapter_keys[chapter]]
                required_items = [item for item in required_items if item.name not in chapter_keys[chapter]]
                self.limited_items[chapter][chapter_keysanity_tags[chapter]].extend(keys)

        for chapter in self.limited_chapters:
            for tag in limited_tags[chapter]:
                items = []
                progressive_item_names = [item_name for item_name in limited_tag_items[tag]]
                items += [item for item in required_items if item.name in progressive_item_names]
                required_items = [item for item in required_items if item.name not in progressive_item_names]
                location_len = len(self.limited_chapter_locations[chapter][tag])
                item_len = len(self.limited_items[chapter][tag])
                self.limited_items[chapter][tag] += items + [self.create_item(self.get_filler_item_name()) for _ in
                                                             range(location_len - item_len - len(items))]

        self.limited_misc_items = [self.create_item(self.get_filler_item_name()) for _ in
                                   range(len(self.limited_misc_locations))]

        unfilled = len(self.multiworld.get_unfilled_locations(self.player))
        unfilled -= len(self.limited_misc_items)
        unfilled -= sum(
            len(self.limited_items[chapter][tag]) for chapter in range(1, 9) for tag in limited_tags[chapter])

        self.random.shuffle(filler_items)
        self.random.shuffle(useful_items)
        self.random.shuffle(required_items)

        for item in required_items:
            self.multiworld.itempool.append(item)
            unfilled -= 1

        useful_count = min(int(unfilled * 0.7), len(useful_items))
        self.multiworld.itempool.extend(useful_items[:useful_count])
        unfilled -= useful_count

        for _ in range(unfilled):
            if len(filler_items) > 0:
                self.multiworld.itempool.append(filler_items.pop())
            else:
                self.multiworld.itempool.append(self.create_item(self.get_filler_item_name()))

    def pre_fill(self) -> None:
        _ = {self.limited_state.collect(location.item, prevent_sweep=True) for location in
             self.multiworld.get_filled_locations(self.player)
             if location.item is not None and location.item.name not in stars.values() and location.item.name != "Victory"}
        for chapter, locations in self.limited_chapter_locations.items().__reversed__():
            self.in_pre_fill = chapter != 8
            for tag, locs in locations.items():
                state = self.limited_state.copy()
                if chapter == 8:
                    state.prog_items[self.player]["stars"] = len(self.required_chapters)
                    state.prog_items[self.player]["required_stars"] = len(self.required_chapters)
                _ = {state.remove(item) for item in self.limited_items[chapter][tag]}
                _ = {state.remove(item) for chapters, locations in self.limited_chapter_locations.items() for tag in
                     locations.keys() if chapters != chapter for item in self.limited_items[chapters][tag]}
                if len(self.limited_items[chapter][tag]) == 0:
                    continue
                fill_restrictive(
                    self.multiworld,
                    state,
                    list(locs),
                    self.limited_items[chapter][tag],
                    single_player_placement=True,
                    lock=True
                )
        self.in_pre_fill = False
        fast_fill(self.multiworld, self.limited_misc_items, list(self.limited_misc_locations))

    def set_rules(self) -> None:
        set_rules(self)
        set_tattle_rules(self)
        if self.options.goal == Goal.option_shadow_queen:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        elif self.options.goal == Goal.option_crystal_stars:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("required_stars", self.player,
                                                                                        self.options.goal_stars.value)
        else:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach(
                "Pit of 100 Trials Floor 100: Return Postage", "Location", self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "goal": self.options.goal.value,
            "goal_stars": self.options.goal_stars.value,
            "palace_stars": self.options.palace_stars.value,
            "pit_items": self.options.pit_items.value,
            "limit_chapter_logic": self.options.limit_chapter_logic.value,
            "limit_chapter_eight": self.options.limit_chapter_eight.value,
            "palace_skip": self.options.palace_skip.value,
            "yoshi_color": self.options.yoshi_color.value,
            "westside": self.options.open_westside.value,
            "tattlesanity": self.options.tattlesanity.value,
            "dazzle_rewards": self.options.dazzle_rewards.value,
            "star_shuffle": self.options.star_shuffle.value,
            "disable_intermissions": self.options.disable_intermissions.value,
            "cutscene_skip": self.options.cutscene_skip.value,
            "death_link": self.options.death_link.value,
            "piecesanity": self.options.piecesanity.value,
            "shinesanity": self.options.shinesanity.value,
            "blue_pipe_toggle": self.options.blue_pipe_toggle.value,
            "enemy_randomizer": self.options.enemy_randomizer.value,
            "tattle_rules": get_random_enemy_tattle_rules_dict(self)
            if self.options.enemy_randomizer != EnemyRandomizer.option_vanilla
            else get_tattle_rules_dict(),
        }

    def create_item(self, name: str) -> TTYDItem:
        item = item_table.get(name, ItemData(None, name, "progression"))
        progression = (ItemClassification.useful if (item.item_name == "Goombella" and not self.options.tattlesanity) else item.progression)
        return TTYDItem(item.item_name, progression, item.id, self.player)

    def lock_item(self, location: str, item_name: str):
        item = self.create_item(item_name)
        item.location = self.get_location(location)
        if location not in self.disabled_locations:
            self.get_location(location).place_locked_item(item)

    def lock_vanilla_items(self, locations: LocationData | List[LocationData]) -> None:
        if isinstance(locations, LocationData):
            locations = [locations]
        for location in locations:
            if location.name not in self.disabled_locations:
                item = self.create_item(items_by_id[location.vanilla_item].item_name)
                item.location = self.get_location(location.name)
                self.get_location(location.name).place_locked_item(item)

    def lock_vanilla_items_remove_from_pool(self, locations: LocationData | List[LocationData]) -> None:
        if isinstance(locations, LocationData):
            locations = [locations]
        for location in locations:
            self.locked_item_frequencies[
                items_by_id[location.vanilla_item].item_name] = self.locked_item_frequencies.get(
                items_by_id[location.vanilla_item].item_name, 0) + 1
            if location.name not in self.disabled_locations:
                item = self.create_item(items_by_id[location.vanilla_item].item_name)
                item.location = self.get_location(location.name)
                self.get_location(location.name).place_locked_item(item)

    def lock_filler_items_remove_from_pool(self, locations: LocationData | List[LocationData]) -> None:
        if isinstance(locations, LocationData):
            locations = [locations]
        for location in locations:
            filler_item_name = self.get_filler_item_name()
            self.locked_item_frequencies[filler_item_name] = self.locked_item_frequencies.get(filler_item_name, 0) + 1
            if location.name not in self.disabled_locations:
                item = self.create_item(filler_item_name)
                item.location = self.get_location(location.name)
                self.get_location(location.name).place_locked_item(item)

    def lock_item_remove_from_pool(self, location: str, item_name: str):
        self.locked_item_frequencies[item_name] = self.locked_item_frequencies.get(item_name, 0) + 1
        item = self.create_item(item_name)
        item.location = self.get_location(location)
        if location not in self.disabled_locations:
            self.get_location(location).place_locked_item(item)

    def get_filler_item_name(self) -> str:
        return self.random.choice(
            list(filter(lambda item: item.progression == ItemClassification.filler, itemList))).item_name

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        change = super().collect(state, item)
        # Skip counting stars during pre_fill to prevent sweep from making the game
        # appear beatable (which causes fill_restrictive to skip placement logic)
        if change and not self.in_pre_fill:
            if item.name in stars.values():
                state.prog_items[item.player]["stars"] += 1
            for star in self.required_chapters:
                if item.location is not None:
                    if item.name == stars[star]:
                        state.prog_items[item.player]["required_stars"] += 1
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        change = super().remove(state, item)
        if change:
            if item.name in stars.values():
                state.prog_items[item.player]["stars"] -= 1
            for star in self.required_chapters:
                if item.location is not None:
                    if item.name == stars[star]:
                        state.prog_items[item.player]["required_stars"] -= 1
        return change

    def generate_output(self, output_directory: str) -> None:
        patch = TTYDProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        write_files(self, patch)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)
