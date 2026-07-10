import random
import logging
from collections import defaultdict
from typing import Dict, Union, ClassVar, Any, Mapping
from BaseClasses import MultiWorld, Item, ItemClassification, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld
from worlds.sly1.Items import item_table, create_itempool, create_item, event_item_pairs, sly_episodes, sly_items, bottles, junk_items, ep_to_lvl
from worlds.sly1.Locations import (get_location_names, get_total_locations,
                                   did_avoid_early_bk, generate_bottle_locations,
                                   generate_minigame_locations, generate_key_caches,
                                   loc_to_ep, all_minigames, lvl_lookup)
from worlds.sly1.Options import Sly1Options
from worlds.sly1.Regions import create_regions
from worlds.sly1.Types import Sly1Item, EpisodeType, episode_type_to_unlock
from worlds.sly1.Rules import set_rules
from worlds.LauncherComponents import (
    Component,
    Type,
    components,
    launch_subprocess,
    icon_paths,
)
from Options import OptionError
import settings

def run_client():
    from worlds.sly1.Sly1Client import launch_client
    launch_subprocess(launch_client, name="Sly1Client")

#icon_paths["sly1_ico"] = f"ap:{__name__}/icon.png"
components.append(
    Component("Sly 1 Client", func=run_client, component_type=Type.CLIENT)
)

def setup_item_groups(items) -> dict[str, set]:
    item_groups = defaultdict(set)
    for item in items:
        if "Progressive" in item:
            item_groups["Moves (Progressive)"].add(item)
            item_groups["Moves (All)"].add(item)
        if item in ["Coin Magnet", "Mine", "Fast", "Decoy", "Hacking"]:  # couldn't think of a good way to rename these for dynamic logic
            item_groups["Moves (Non-Progressive)"].add(item)
            item_groups["Moves (All)"].add(item)
        if item in junk_items and "Trap" not in item:
            item_groups["All Filler"].add(item)
        if item in junk_items and "Trap" in item:
            item_groups["All Traps"].add(item)

        if item.find(":") == -1:  # all remaining items we care about will have a : in them
            continue
        ep_or_lvl, item_type = item.split(":")  # unknown at this stage if this is an episode or level item

        if ep_or_lvl in ep_to_lvl.keys():  # if true, this is an episode-based item
            for group_type in ["Blueprint", "Key", "Episode Unlock"]:
                if group_type in item_type:
                    item_groups[f"{ep_or_lvl} (All)"].add(item)
                    item_groups[f"All {group_type}s"].add(item)
                    break  # small optimization to stop once found
        else:  # if else, this is a bottle item (all level-based items are bottle items) and we must find which episode it belongs to
            for episode in ep_to_lvl:  # could make this a direct lookup if another dict was made for level -> ep, but I didn't find that justified
                if ep_or_lvl in ep_to_lvl[episode]:  # found the level in an episode's list
                    item_groups[f"{episode} Bottles"].add(item)
                    item_groups[f"{episode} (All)"].add(item)
                    item_groups[f"All Bottles"].add(item)
                    break  # small optimization to stop once found
    return item_groups

def setup_location_groups(locations) -> dict[str, set]:
    location_groups = defaultdict(set)
    location_groups["All Bosses"] = {"Eye of the Storm", "Last Call", "Deadly Dance", "Flame Fu!"}  # rest of loop is simpler if this is hardcoded here

    # this is SO much better and more efficient now, at the cost of reformatting almost all location names. Worth it 100% imo
    for loc in locations:
        if loc.find(":") == -1:  # paris files and boss-related locations intentionally do not have a : and aren't in any groups
            continue

        # all locations (minus the ones skipped above) have format of "Level: Location Type" e.g. Stealthy Approach: Key or Treasure in the Depths: Minigame Cache #3
        level, loc_type = loc.split(":")
        episode = loc_to_ep[level]

        location_groups[f"{episode} (All)"].add(loc)  # everything in an episode

        # generalizing per-level, per-episode, and full-game groups for bottles, keys, minigame caches, vaults, and hourglasses
        # doing this cuts out a ton of redundancy in lines of code because most groups are similar
        def helper(single, plural):  # singular and plural form of the group names. All because hourglasses pluralizes weirdly
            if single in loc_type:  # every location gets checked for if it's a bottle, key, etc. so only continue if there's a match
                if single in ["Bottle", "Minigame Cache"] or (single == "Key" and level not in all_minigames):  # only do per-level key groups for non-minigames
                    location_groups[f"{level} {plural}"].add(loc)
                location_groups[f"{episode} {plural}"].add(loc)
                location_groups[f"All {plural}"].add(loc)

        for single in ["Bottle", "Key", "Minigame Cache", "Vault", "Hourglass"]:
            plural = "Hourglasses" if single == "Hourglass" else single + "s"  # hourglass is the only one that can't be pluralized with just adding an s. I hate English
            helper(single, plural)

        for lvl_string, lvl_list in lvl_lookup.items():
            if level in lvl_list:
                location_groups[f"All {lvl_string} Levels"].add(loc)

        if level not in all_minigames:  # minigame levels don't have enough diversity in locations to justify {level} (All) groups
            location_groups["All Platforming Levels"].add(loc)
            location_groups[f"{level} (All)"].add(loc)
    return location_groups

class Sly1Web(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Sly Cooper and the Thievius Raccoonus for MultiworldGG. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Nep"]
    )]

class Sly1Settings(settings.Group):
    class AutoFillLocations(settings.Bool):
        """Adds "Key Cache" locations if items outnumber locations, preventing errors.
        It is strongly recommended you keep this enabled unless you know what you're doing!"""
        description = "Sly 1 Auto Fill Locations"

    auto_fill_locations: Union[AutoFillLocations, bool] = True

class Sly1World(World):
    """
    Sly Cooper and the Thievius Raccoonus is a action-stealth game set in a cartoony cel-shaded world.
    Avenge your father and take back the pages of the Thievius Raccoonus from the Fiendish Five!
    """

    game = "Sly Cooper and the Thievius Raccoonus"
    author: str = "Nep & Philiard"
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = Sly1Options
    options = Sly1Options
    web = Sly1Web()
    settings: ClassVar[Sly1Settings]

    # set up item and location groups
    item_name_groups = setup_item_groups(item_name_to_id)
    location_name_groups = setup_location_groups(location_name_to_id)

    # this is how we tell the Universal Tracker we want to use re_gen_passthrough
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data

    # and this is how we tell Universal Tracker we don't need the yaml
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.generated_key_caches = 0

    def generate_early(self) -> None:
        # implement .yaml-less Universal Tracker support
        if getattr(self.multiworld, "generation_is_fake", False):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough")

                if "Sly Cooper and the Thievius Raccoonus" in re_gen_passthrough:
                    slot_data = re_gen_passthrough["Sly Cooper and the Thievius Raccoonus"]
                    self.options.UnlockClockwerk.value = slot_data["UnlockClockwerk"]
                    self.options.FastClockwerk.value = slot_data["FastClockwerk"]
                    self.options.RequiredBosses.value = slot_data["RequiredBosses"]
                    self.options.MaxPages.value = slot_data["MaxPages"]
                    self.options.RequiredPages.value = slot_data["RequiredPages"]
                    self.options.StartingEpisode.value = slot_data["StartingEpisode"]
                    self.options.IncludeHourglasses.value = slot_data["IncludeHourglasses"]
                    self.options.HourglassesRequireRoll.value = slot_data["HourglassesRequireRoll"]
                    self.options.EnableTricks.value = slot_data["EnableTricks"]
                    self.options.AvoidEarlyBK.value = slot_data["AvoidEarlyBK"]
                    self.options.ExcludeMinigames.value = slot_data["ExcludeMinigames"]
                    self.options.MinigameCaches.value = slot_data["MinigameCaches"]
                    self.options.LocationCluesanityBundleSize.value = slot_data["LocationCluesanityBundleSize"]
                    self.options.ItemCluesanityBundleSize.value = slot_data["ItemCluesanityBundleSize"]
                    self.options.CutsceneSkip.value = slot_data["CutsceneSkip"]
                    self.options.TrapChance.value = slot_data["TrapChance"]
                    self.options.IcePhysicsTrapWeight.value = slot_data["IcePhysicsTrapWeight"]
                    self.options.SpeedChangeTrapWeight.value = slot_data["SpeedChangeTrapWeight"]
                    self.options.InvisibilityTrapWeight.value = slot_data["InvisibilityTrapWeight"]
                    self.options.BallTrapWeight.value = slot_data["BallTrapWeight"]

                    starting_episode = EpisodeType(self.options.StartingEpisode)
                    starting_episode_unlock = episode_type_to_unlock[starting_episode]
                    starting_episode_name = starting_episode_unlock.replace(": Episode Unlock", "")

                    if did_avoid_early_bk(self):
                        if starting_episode_name == "All":
                            starting_episode_name = episode_type_to_unlock[EpisodeType(random.randint(1, 4))].replace(
                                ": Episode Unlock", "")
                            self.random_episode = starting_episode_name
            return

        starting_episode = EpisodeType(self.options.StartingEpisode)
        starting_episode_unlock = episode_type_to_unlock[starting_episode]
        starting_episode_name = starting_episode_unlock.replace(": Episode Unlock", "")

        # Starting Episode - please clean this up oml
        if starting_episode_name == "All":
            for episode in sly_episodes.keys():
                self.multiworld.push_precollected(self.create_item(episode))
        else:
            self.multiworld.push_precollected(self.create_item(starting_episode_unlock))

        # Avoid Early BK
        if did_avoid_early_bk(self):
            if starting_episode_name == "All":
                starting_episode_name = episode_type_to_unlock[EpisodeType(random.randint(1, 4))].replace(": Episode Unlock", "")
                self.random_episode = starting_episode_name
            self.multiworld.push_precollected(self.create_item(f'{starting_episode_name}: Key'))

    def create_regions(self):
        create_regions(self)

        if self.options.LocationCluesanityBundleSize.value > 0:
            generate_bottle_locations(self, self.options.LocationCluesanityBundleSize.value)

        if self.options.LocationCluesanityBundleSize.value == 0 and self.options.ItemCluesanityBundleSize.value > 0:
            logging.warning(
                f"{self.player}: Cannot have item bundles without location bundles. Setting location bundle size to item bundle size.")
            self.options.LocationCluesanityBundleSize.value = self.options.ItemCluesanityBundleSize.value
            generate_bottle_locations(self, self.options.LocationCluesanityBundleSize.value)
        
        generate_minigame_locations(self, self.options.MinigameCaches.value)

    def create_items(self):
        itempool = create_itempool(self)
        self.multiworld.itempool.extend(itempool)

        for event, item in event_item_pairs.items():
            event_item = Sly1Item(item, ItemClassification.progression_skip_balancing, None, self.player)
            self.multiworld.get_location(event, self.player).place_locked_item(event_item)

        if Sly1World.settings.auto_fill_locations:
            total_locations = get_total_locations(self)
            total_items = sum(1 for item in self.multiworld.itempool if item.player == self.player) + len(
                event_item_pairs) + 1
            deficit = total_items - total_locations
            generate_key_caches(self, deficit)
            self.generated_key_caches = max(0, deficit)
        else:
            location_count = len(self.multiworld.get_unfilled_locations(self.player))
            item_count = len(itempool)
            if location_count - item_count < 0:
                self.handle_not_enough_locations(item_count - location_count)

    def handle_not_enough_locations(self, count):
        """Check the available location and items counts, raise OptionErrors to warn the player of too few locations"""
        option_list: list[str] = []
        if self.options.LocationCluesanityBundleSize == 0:
            option_list.append("Location Cluesanity Bundle Size")
        if self.options.MinigameCaches == 0:
            option_list.append("Minigame Caches")
        if not option_list:
            option_list: str = "dunno"  # ¯\_(''/)_/¯
        message = f"Not enough location options enabled! {count} items have nowhere to be placed."
        message += f"Consider adjusting some of the following options: {option_list}"
        raise OptionError(message)
    set_rules = set_rules

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def get_options_as_dict(self) -> Dict[str, Any]:
        return self.options.as_dict(
            "UnlockClockwerk",
            "RequiredBosses",
            "MaxPages",
            "RequiredPages",
            "FastClockwerk",
            "StartingEpisode",
            "IncludeHourglasses",
            "HourglassesRequireRoll",
            "AvoidEarlyBK",
            "EnableTricks",
            "LocationCluesanityBundleSize",
            "ItemCluesanityBundleSize",
            "CutsceneSkip",
            "ExcludeMinigames",
            "MinigameCaches",
            "TrapChance",
            "IcePhysicsTrapWeight",
            "SpeedChangeTrapWeight",
            "InvisibilityTrapWeight",
            "BallTrapWeight",
        )

    def fill_slot_data(self) ->Mapping[str, object]:
        return {
            "UnlockClockwerk": self.options.UnlockClockwerk.value,
            "RequiredBosses": self.options.RequiredBosses.value,
            "MaxPages": self.options.MaxPages.value,
            "RequiredPages": self.options.RequiredPages.value,
            "FastClockwerk": self.options.FastClockwerk.value,
            "StartingEpisode": self.options.StartingEpisode.value,
            "IncludeHourglasses": self.options.IncludeHourglasses.value,
            "HourglassesRequireRoll": self.options.HourglassesRequireRoll.value,
            "AvoidEarlyBK": self.options.AvoidEarlyBK.value,
            "EnableTricks": self.options.EnableTricks.value,
            "LocationCluesanityBundleSize": self.options.LocationCluesanityBundleSize.value,
            "ItemCluesanityBundleSize": self.options.ItemCluesanityBundleSize.value,
            "CutsceneSkip": self.options.CutsceneSkip.value,
            "ExcludeMinigames": self.options.ExcludeMinigames.value,
            "MinigameCaches": self.options.MinigameCaches.value,
            "TrapChance": self.options.TrapChance.value,
            "IcePhysicsTrapWeight": self.options.IcePhysicsTrapWeight.value,
            "SpeedChangeTrapWeight": self.options.SpeedChangeTrapWeight.value,
            "InvisibilityTrapWeight": self.options.InvisibilityTrapWeight.value,
            "BallTrapWeight": self.options.BallTrapWeight.value,
            "Seed": self.multiworld.seed_name,
        }

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)