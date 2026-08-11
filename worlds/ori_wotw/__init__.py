"""Definition of the World class and world structure for Ori and the Will of the Wisps."""


# TODO list spawn items:
# Make the new spawn points
# Put new spawn locs outside of data files (or add them auto)
# New spawn options: vanilla, TP, random TP (with weights ?), random anchor
# UT support for random name + add spawn info to slot data
# Change KS logic for spawn ? Also add early KS data

from __future__ import annotations

import logging
from typing import Any, Callable
from collections import Counter

from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule, set_rule
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, LocationProgressType, CollectionState

from .generated_data.Events import event_table
from .generated_data.Regions import region_table
from .generated_data.Entrances import entrance_table
from .generated_data.Refills import refill_events
from .generated_data.Locations import loc_table
from .generated_data.Quests import quest_table
from .generated_data.DoorData import doors_map, doors_vanilla
from .generated_data.Items import item_table
from .generated_data.Rules import (
    set_moki_rules,
    set_gorlek_rules,
    set_gorlek_glitched_rules,
    set_kii_rules,
    set_kii_glitched_rules,
    set_unsafe_rules,
    set_unsafe_glitched_rules
)

from .data.SpawnData import spawn_data
from .data.ItemsIcons import get_item_iconpath
from .data.LocationGroups import loc_sets, location_regions
from .data.ItemGroups import item_groups

from .Options import WotWOptions, option_groups, LogicDifficulty, Quests, StartingLocation, RandomizeDoors
from .Presets import options_presets
from .AdditionalRules import combat_rules, unreachable_rules, ut_combat_rules
from .ERGenerator import generate_er_connections


class WotWWeb(WebWorld):
    theme = "ocean"  # TODO documentation
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Ori and the Will of the Wisps randomizer connected to a MultiworldGG Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Satisha"]
    )]
    options_presets = options_presets
    option_groups = option_groups
    bug_report_page = "https://discord.com/channels/731205301247803413/1272952565843103765"


class WotWWorld(World):
    """Ori and the Will of the Wisps is a 2D Metroidvania;
    The sequel to Ori and the blind forest, a platform game emphasizing exploration, collecting items and upgrades, and
    backtracking to previously inaccessible areas.
    The player controls the titular Ori, a white guardian spirit.
    """
    game = "Ori and the Will of the Wisps"
    web = WotWWeb()

    item_name_to_id = {name: data[2] for name, data in item_table.items()}
    location_name_to_id = loc_table

    item_name_groups = item_groups
    location_name_groups = location_regions  # TODO Convert list to set (not directly in LocationGroups though)

    options_dataclass = WotWOptions
    options: WotWOptions

    glitches_item_name = "UTGlitch"

    required_client_version = (0, 6, 3)

    # Universal tracker support
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld, player) -> None:
        super(WotWWorld, self).__init__(multiworld, player)
        self.relic_placements: list[tuple[int, int]] = []  # Store the area ID and location ID of the relics
        self.empty_locations: list[str] = []  # Excluded locations
        self.filled_locations: list[str] = [] # Locations holding an item
        self.er_door_ids: list[int] = []  # Contain the data of door IDs if ER is enabled
        # The list index corresponds to the exit door ID minus one, and the int in the list is the target door ID
        self.spawn_region_name: str = "MarshSpawn.Main"
        self.spawn_area: str = "MarshSpawn"
        self.possible_combat_weapons: list[str] = []  # Energy weapons that can be used in combat

    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        # Ask to update the max resources and the refills on the next call to `RulesFunctions.has_enough_resources`
        # or `RulesFunctions.has_enough_max_health`
        if change and item.name in ("Health Fragment",
                                    "Energy Fragment",
                                    "EastHollow.ForestsVoice",
                                    "LowerReach.ForestsMemory",
                                    "UpperDepths.ForestsEyes",
                                    "WestPools.ForestsStrength",
                                    "WindtornRuins.Seir",):
            state.wotw_resource_stale[self.player] = True
        # Ask to update the combat data on the next call to `RulesFunctions.compute_combat`
        elif change and item.name in ("Hammer",
                                      "Sword",
                                      "Grenade",
                                      "Bow",
                                      "Shuriken",
                                      "Sentry",
                                      "Spear",
                                      "Blaze",
                                      "Flash",
                                      "Combat.Ranged",
                                      "Combat.Aerial",
                                      "Combat.Dangerous",
                                      "Combat.Shielded",
                                      "Combat.Bat",
                                      "Combat.Sand",
                                      ):
            state.wotw_enemies_stale_collect[self.player] = True
        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        # Ask to update the max resources and the refills on the next call to `RulesFunctions.has_enough_resources`
        # or `RulesFunctions.has_enough_max_health`
        if change and item.name in ("Health Fragment",
                                    "Energy Fragment",
                                    "EastHollow.ForestsVoice",
                                    "LowerReach.ForestsMemory",
                                    "UpperDepths.ForestsEyes",
                                    "WestPools.ForestsStrength",
                                    "WindtornRuins.Seir",):
            state.wotw_resource_stale[self.player] = True
        # Ask to update the combat data on the next call to `RulesFunctions.compute_combat`
        elif change and item.name in ("Hammer",
                                      "Sword",
                                      "Grenade",
                                      "Bow",
                                      "Shuriken",
                                      "Sentry",
                                      "Spear",
                                      "Blaze",
                                      "Flash",
                                      "Combat.Ranged",
                                      "Combat.Aerial",
                                      "Combat.Dangerous",
                                      "Combat.Shielded",
                                      "Combat.Bat",
                                      "Combat.Sand",
                                      ):
            state.wotw_enemies_stale_remove[self.player] = True
        return change

    def generate_early(self) -> None:
        # TODO Launch on seir + fragments
        options = self.options
        # Options checking
        if options.open_mode:
            options.no_rain.value = True

        # Prevent combinations that don't generate well on random spawn
        if not options.better_spawn and options.spawn == StartingLocation.option_outerruins:
            raise OptionError("Outer Ruins spawn (UpperWastes.NorthTP) behaves poorly without Better random spawn.")
        if not options.tp:
            if (options.spawn.value in (
                    StartingLocation.option_willow,
                    StartingLocation.option_shriek,
                    StartingLocation.option_random_loc,
                    StartingLocation.option_random_tp,
                    StartingLocation.option_depths,
                )
            or (options.difficulty.value == LogicDifficulty.option_moki and options.spawn.value in (
                    StartingLocation.option_westwoods,
                    StartingLocation.option_eastwoods,
                    StartingLocation.option_westwastes,
                    StartingLocation.option_eastwastes,
                    StartingLocation.option_outerruins,
                    StartingLocation.option_innerruins,
                )
                    )):
                raise OptionError("Removing Teleporters from the pool can cause impossible seeds"
                                  "when spawning in Willow, Depths or at a random location, "
                                  "or on the east side in Moki.")
            if not options.better_spawn and options.spawn.value in (
                StartingLocation.option_burrows,
                StartingLocation.option_howlsden,
                StartingLocation.option_eastpools,
                StartingLocation.option_westpools,  # outerruins already prevented just without better spawn
                StartingLocation.option_innerruins,  # random loc/tp and willow are already impossible just without tp
            ):
                raise OptionError("Removing Teleporters and not having Better random spawn can cause impossible seeds"
                                  "in most places (apart from glades, wellspring, woods, reach, early wastes).")

        if options.fragments_count.value < options.fragments_required.value:
            options.fragments_count.value = options.fragments_required.value
        # Spawning on willow usually gives Launch on spawn, which defeats the purpose of the options that affect Launch
        if (options.spawn.value == StartingLocation.option_willow
                and (options.launch_on_seir or options.launch_fragments)):
            options.spawn.value = StartingLocation.option_vanilla

        if options.difficulty == LogicDifficulty.option_moki:
            self.possible_combat_weapons = []  # Only use Sword or Hammer in Moki
        elif options.difficulty  == LogicDifficulty.option_unsafe:
            self.possible_combat_weapons = ["Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze", "Flash"]
        else:
            self.possible_combat_weapons = ["Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze"]

        # Selection of a random spawn location
        spawn_dict: dict[str, tuple[int, int]] = {  # Map from TP region name to associated spawn option and weight
            "MarshSpawn.Main": (StartingLocation.option_vanilla, 3),  # TODO change data structure ?
            "MidnightBurrows.Teleporter": (StartingLocation.option_burrows, 10),
            "HowlsDen.Teleporter": (StartingLocation.option_howlsden, 10),
            "EastHollow.Teleporter": (StartingLocation.option_hollow, 10),
            "GladesTown.Teleporter": (StartingLocation.option_glades, 10),
            "InnerWellspring.Teleporter": (StartingLocation.option_wellspring, 10),
            "WoodsEntry.Teleporter": (StartingLocation.option_westwoods, 7),
            "WoodsMain.Teleporter": (StartingLocation.option_eastwoods, 7),
            "LowerReach.Teleporter": (StartingLocation.option_reach, 10),
            "UpperDepths.Teleporter": (StartingLocation.option_depths, 10),
            "EastPools.Teleporter": (StartingLocation.option_eastpools, 7),
            "WestPools.Teleporter": (StartingLocation.option_westpools, 7),
            "LowerWastes.WestTP": (StartingLocation.option_westwastes, 5),
            "LowerWastes.EastTP": (StartingLocation.option_eastwastes, 5),
            "UpperWastes.NorthTP": (StartingLocation.option_outerruins, 5),
            "WindtornRuins.RuinsTP": (StartingLocation.option_innerruins, 3),
            "WillowsEnd.InnerTP": (StartingLocation.option_willow, 3),
            "WillowsEnd.ShriekArena": (StartingLocation.option_shriek, 3),
        }
        spawn_dict_reverse: dict[int, str] = {option[0]: region for region, option in spawn_dict.items()}

        if options.spawn.value == StartingLocation.option_random_loc:
            spawn_regions_candidates: list[str] = []
            for region_name, region_data in region_table.items():
                if region_data[0]:
                    spawn_regions_candidates.append(region_name)
            self.spawn_region_name = self.random.choice(spawn_regions_candidates)
        else:  # options.spawn.value != StartingLocation.option_random_loc
            if options.spawn.value == StartingLocation.option_random_tp:
                weights = [data[1] for data in spawn_dict.values()]
                total_weight = sum(weights)
                # TODO weights depending on difficulty ?
                for i, weight in enumerate(weights):  # TODO data structure here: option value, weight (don't rely on same order)
                    if self.random.random() < weight / total_weight:
                        options.spawn.value = i
                        break
                    else:
                        total_weight -= weight
                assert options.spawn.value != StartingLocation.option_random_tp  # TODO debug, remove
            self.spawn_region_name = spawn_dict_reverse[options.spawn.value]
        self.spawn_area = str.split(self.spawn_region_name, ".")[0]
        # TODO Debug, remove when generation stable ?
        logging.info(f"Ori WotW: Spawn {self.spawn_region_name} for player {self.player}")

        # Selection of a random goal
        if "one_random" in options.goal:
            possible_goals = sorted(list(options.goal.value))
            possible_goals.remove("one_random")
            selected_goal: list = []
            if not possible_goals:  # Only random selected, choose among all goals
                possible_goals = ["trees", "wisps", "quests", "relics"]
            # Select a goal at random among the selected ones
            selected_goal.append(self.random.choice(possible_goals))
            options.goal.value = set(selected_goal)


        # Construct the excluded and used locations lists
        if options.glades_done:
            self.empty_locations += loc_sets["Rebuild"].copy()
        else:
            self.filled_locations += loc_sets["Rebuild"].copy()
        if options.no_trials:
            self.empty_locations += loc_sets["Trials"].copy()
        else:
            self.filled_locations += loc_sets["Trials"].copy()
        if options.qol or options.quests == Quests.option_none:
            self.empty_locations += loc_sets["QOL"].copy()
        else:
            self.filled_locations += loc_sets["QOL"].copy()
        if options.quests != Quests.option_all:
            self.empty_locations += loc_sets["HandToHand"].copy()
        else:
            self.filled_locations += loc_sets["HandToHand"].copy()
        if options.quests == Quests.option_none:
            self.empty_locations += loc_sets["Quests"].copy()
        else:
            self.filled_locations += loc_sets["Quests"].copy()
        if options.zone_hints:
            self.empty_locations += loc_sets["Maps"].copy()
        else:
            self.filled_locations += loc_sets["Maps"].copy()
        self.filled_locations += loc_sets["Base"].copy()
        self.filled_locations += loc_sets["ExtraQuests"].copy()

        # Universal Tracker support
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            difficulty_dict: dict[str, int] = {
                "Moki": LogicDifficulty.option_moki,
                "Gorlek": LogicDifficulty.option_gorlek,
                "Kii": LogicDifficulty.option_kii,
                "Unsafe": LogicDifficulty.option_unsafe,
            }
            goals: set[str] = set()
            combat: set[str] = set()

            self.options.difficulty.value = difficulty_dict[slot_data["difficulty"]]
            self.options.glitches.value = slot_data["glitches"]
            self.options.unpopular.value = slot_data["unpopular"]
            # Overrides the random spawn selection done previously in generate_early
            self.spawn_region_name = slot_data["spawn_anchor"]
            if slot_data["goal_trees"]:
                goals.add("trees")
            if slot_data["goal_quests"]:
                goals.add("quests")
            if slot_data["goal_wisps"]:
                goals.add("wisps")
            if slot_data["goal_relics"]:
                goals.add("relics")
                self.options.relic_count.value = len(slot_data["relic_locs"])
            self.options.goal.value = goals
            self.options.hard_mode.value = slot_data["hard"]
            self.options.qol.value = slot_data["qol"]
            self.options.zone_hints.value = slot_data["zone_hints"]
            self.options.better_spawn.value = slot_data["better_spawn"]
            self.options.better_wellspring.value = slot_data["better_wellspring"]
            self.options.no_rain.value = slot_data["no_rain"]
            if slot_data["skip_boss"]:
                combat.add("bosses")
            if slot_data["skip_demi_boss"]:
                combat.add("demi bosses")
            if slot_data["skip_shrine"]:
                combat.add("shrines")
            if slot_data["skip_arena"]:
                combat.add("arenas")
            self.options.no_combat.value = combat
            self.options.no_trials.value = slot_data["no_trials"]
            self.options.no_hearts.value = slot_data["no_hearts"]
            if slot_data["no_hand_quest"]:
                if slot_data["no_quests"]:
                    self.options.quests.value = Quests.option_none
                else:
                    self.options.quests.value = Quests.option_no_hand
            else:
                self.options.quests.value = Quests.option_all
            self.options.no_ks.value = slot_data["no_ks"]
            self.options.open_mode.value = slot_data["open_mode"]
            self.options.glades_done.value = slot_data["glades_done"]
            if slot_data["launch_frag"] != 0:
                self.options.launch_fragments.value = True
                self.options.fragments_count.value = slot_data["total_frag"]
            if slot_data["door_rando"]:  # The `door_rando` key is associated with a bool
                # Coupled and decoupled behave the same for UT since the pairings are directly used
                self.options.door_rando.value = RandomizeDoors.option_coupled
            else:
                self.options.door_rando.value = RandomizeDoors.option_disabled
            self.options.free_teleporters.value = slot_data["free_tp"]
            self.options.free_regenerate.value = slot_data["regen"]
            self.options.ut_config.value = slot_data["ut_config"]

    def create_regions(self) -> None:
        mworld = self.multiworld
        player = self.player
        options = self.options

        for region_name in region_table.keys():
            region = Region(region_name, player, mworld)
            mworld.regions.append(region)

        for region_name in doors_map.keys():
            region = Region(region_name, player, mworld)
            mworld.regions.append(region)

        menu_region = Region("Menu", player, mworld)
        mworld.regions.append(menu_region)

        spawn_region = self.get_region(self.spawn_region_name)  # Links menu with spawn point
        menu_region.connect(spawn_region, rule=lambda state: True)

        # ExternalStates is used in the generated file as a base point to handle the logic for a few options.
        menu_region.connect(self.get_region("ExternalStates"), rule=lambda state: True)

        # Create regions on locations, and create a location on top of it if needed
        for loc_name in self.filled_locations:
            region = Region(loc_name, player, mworld)
            mworld.regions.append(region)
            region.locations.append(WotWLocation(player, loc_name, self.location_name_to_id[loc_name], region))
        # For empty locations, only create the base region
        for loc_name in self.empty_locations:
            region = Region(loc_name, player, mworld)
            mworld.regions.append(region)
        for quest_name in quest_table:  # Quests are locations that have to be tracked like events
            event_name = quest_name + ".quest"
            event_region = Region(event_name, player, mworld)  # Region that holds the event item
            mworld.regions.append(event_region)
            event_loc = WotWLocation(player, event_name, None, event_region)
            event_loc.show_in_spoiler = False
            event_loc.place_locked_item(self.create_event_item(quest_name))
            event_region.locations.append(event_loc)
            base_region = self.get_region(quest_name)  # Region that holds the location
            base_region.connect(event_region, rule=lambda state: True)  # Connect the event region to the base region

        for event in event_table:  # Various events
            self.create_event(event)
        for event in refill_events:  # Tracks the refills that are accessible
            self.create_event(event)

        for entrance_name in entrance_table:  # Create and connect the entrances
            (parent, connected) = entrance_name.split(" -> ")
            parent_region = self.get_region(parent)
            connected_region = self.get_region(connected)
            entrance = parent_region.create_exit(entrance_name)
            entrance.access_rule = lambda state: False  # The rules are mostly set with add_rule, so start with False.
            entrance.connect(connected_region)

        self.create_event("Victory", show_spoiler=True)

        mworld.completion_condition[player] = lambda state: state.has("Victory", player)

        # Universal Tracker support: link all the spawn items for free regardless of the spawn.
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            for i in range(1, 11):
                name = f"Spawn item {i}"
                spawn_loc = WotWLocation(player, name, self.location_name_to_id[name], menu_region)
                menu_region.locations.append(spawn_loc)

        if options.spawn != StartingLocation.option_vanilla:
            # Spawn items are local, and exclude Launch from them (except in late game areas)
            if self.spawn_area in ("WillowsEnd", "WeepingRidge"):
                item_rule = lambda item: item.player == self.player and item.name != "Launch Fragment"
            else:
                item_rule = (lambda item: item.player == self.player
                             and item.name not in ("Launch Fragment", "Launch"))

            # Create all spawn item locations
            extra_items = 3 if len(mworld.player_name) <= 1 else 1  # The range starts at 1
            for i in range(1, spawn_data[self.spawn_area].items_amount + extra_items):
                name = f"Spawn item {i}"
                spawn_loc = WotWLocation(player, name, self.location_name_to_id[name], menu_region)
                menu_region.locations.append(spawn_loc)
                # spawn_loc.progress_type = LocationProgressType.PRIORITY
                spawn_loc.item_rule = item_rule

    def create_event(self, event: str, show_spoiler=False) -> None:
        """Create an event, place the item and attach it to an event region (all with the same name)."""
        event_region = Region(event, self.player, self.multiworld)
        event_location = WotWLocation(self.player, event, None, event_region)
        event_location.show_in_spoiler = show_spoiler
        event_location.place_locked_item(self.create_event_item(event))
        self.multiworld.regions.append(event_region)
        event_region.locations.append(event_location)

    def create_item(self, name: str) -> WotWItem:
        if name == "UTGlitch":
            return WotWItem(name, ItemClassification.progression, None, player=self.player)
        return WotWItem(name, item_table[name][1], item_table[name][2], player=self.player)

    def create_items(self) -> None:
        mworld = self.multiworld
        options = self.options

        skipped_items: list[str] = []  # Remove one instance of the item
        removed_items: list[str] = []  # Remove all instances of the item
        pool: list[WotWItem] = []

        # Handle the random spawn items and early items
        items_data = spawn_data[self.spawn_area]
        # Put keystones in sphere 1
        if not options.no_ks and items_data.early_ks > 0:
            self.multiworld.early_items[self.player]["Keystone"] = items_data.early_ks
        # Give health and regenerate to fulfill the region requirements
        if options.difficulty == LogicDifficulty.option_moki:
            spawn_hf = items_data.moki_hf
            regen_spawn = bool(items_data.require_regen and not options.free_regenerate)
        elif options.difficulty == LogicDifficulty.option_gorlek:
            spawn_hf = items_data.gorlek_hf
            regen_spawn = bool(items_data.require_regen and not options.free_regenerate)
        elif options.difficulty == LogicDifficulty.option_kii:
            spawn_hf = items_data.kii_hf
            regen_spawn = False
        else:  # options.difficulty == LogicDifficulty.option_unsafe
            spawn_hf = 0
            regen_spawn = False
        for _ in range(spawn_hf):  # Give Health Fragments from the pool
            mworld.push_precollected(self.create_item("Health Fragment"))
            skipped_items.append("Health Fragment")
        if regen_spawn:  # Give Regenerate if needed
            mworld.push_precollected(self.create_item("Regenerate"))
            skipped_items.append("Regenerate")

        # The generator can have difficulties to find the exit to these areas, so guide it towards the key item
        if self.spawn_area in ("UpperWastes", "LowerWastes"):
            self.multiworld.early_items[self.player]["Burrow"] = 1
        elif self.spawn_area in ("UpperDepths", "LowerDepths"):
            self.multiworld.early_items[self.player]["Glide"] = 1
        elif self.spawn_area in ("EastPools", "WestPools", "UpperPools", "PoolsApproach"):
            self.multiworld.early_items[self.player]["Clean Water"] = 1

        for item, count in options.start_inventory.value.items():
            for _ in range(count):
                skipped_items.append(item)

        if options.sword:
            mworld.push_precollected(self.create_item("Sword"))
            removed_items.append("Sword")

        if options.regenerate:
            mworld.push_precollected(self.create_item("Regenerate"))
            removed_items.append("Regenerate")

        if not options.tp:
            for item in item_groups["Teleporters"]:
                removed_items.append(item)

        if not options.extratp:
            for item in item_groups["Extra Teleporters"]:
                removed_items.append(item)

        if not options.bonus:
            for item in item_groups["Bonus"]:
                removed_items.append(item)

        if not options.extra_bonus:
            for item in item_groups["Bonus+"]:
                removed_items.append(item)

        if not options.skill_upgrade:
            for item in item_groups["Skill Upgrades"]:
                removed_items.append(item)

        if options.glades_done:
            removed_items.append("Gorlek Ore")

        if options.no_ks:
            removed_items.append("Keystone")

        if options.vanilla_shop_upgrades:
            shop_items = {"OpherShop.ExplodingSpike": "Exploding Spear",
                          "OpherShop.ShockSmash": "Hammer Shockwave",
                          "OpherShop.StaticStar": "Static Shuriken",
                          "OpherShop.ChargeBlaze": "Charge Blaze",
                          "OpherShop.RapidSentry": "Rapid Sentry",
                          "OpherShop.WaterBreath": "Water Breath",
                          "TwillenShop.Overcharge": "Overcharge",
                          "TwillenShop.TripleJump": "Triple Jump",
                          "TwillenShop.Wingclip": "Wingclip",
                          "TwillenShop.Swap": "Swap",
                          "TwillenShop.LightHarvest": "Light Harvest",
                          "TwillenShop.Vitality": "Vitality",
                          "TwillenShop.Energy": "Energy (Shard)",
                          "TwillenShop.Finesse": "Finesse"}
            for location, item in shop_items.items():
                loc = self.get_location(location)
                loc.place_locked_item(self.create_item(item))
                removed_items.append(item)
            if (options.difficulty == LogicDifficulty.option_moki
                and options.door_rando != RandomizeDoors.option_disabled
                and not options.tp):
                # Add another water breath in the pool to prevent an impossible seed if the door rando connects
                # UpperWastes.OutsideRuins (Door) to InnerWellspring.Teleporter (Door).
                # In that case Wellspring escape is locked behind the Pools Wisp,
                # which logically requires Water Breath, which requires the escape on vanilla shop upgrades.
                removed_items.remove("Water Breath")


        if options.launch_on_seir:
            self.get_location("WindtornRuins.Seir").place_locked_item(self.create_item("Launch"))
            removed_items.append("Launch")

        if options.launch_fragments:
            removed_items.append("Launch")
            pool += [self.create_item("Launch Fragment") for _ in range(options.fragments_count.value)]

            menu_region = self.get_region("Menu")
            event_loc = WotWLocation(self.player, "LaunchFromFragments", None, menu_region)
            menu_region.locations.append(event_loc)
            event_loc.place_locked_item(self.create_item("Launch"))
            # Give logical launch when all fragments are collected
            set_rule(event_loc, lambda state: state.has("Launch Fragment", self.player, options.fragments_count.value))


        counter = Counter(skipped_items)


        for item, data in item_table.items():
            if item in removed_items:
                count = -counter[item]
            else:
                count = data[0] - counter[item]
            if count <= 0:  # This can happen with starting inventory
                count = 0

            for _ in range(count):
                pool.append(self.create_item(item))

        if options.difficulty == LogicDifficulty.option_moki:
            # Exclude a location that is inaccessible in the lowest difficulty.
            skipped_loc = self.get_location("WestPools.BurrowOre")
            skipped_loc.progress_type = LocationProgressType.EXCLUDED

        if "relics" in options.goal:  # Put the relics at random places in the areas
            area_data: dict[str, int] = {  # Map of each area to the area ID used in the client
                "Marsh": 0,
                "Hollow": 1,
                "Glades": 2,
                "Wellspring": 3,
                "Pools": 4,
                "Burrows": 5,
                "Reach": 6,
                "Woods": 7,
                "Depths": 8,
                "Wastes": 9,
                "Willow": 11,
                }
            remaining_areas: list[str] = list(area_data.keys())
            for _ in range(options.relic_count.value):
                area: str = self.random.choice(remaining_areas)
                remaining_areas.remove(area)

                relic_location: str = self.random.choice(location_regions[area])
                # TODO check if location excluded, put a threshold and skip the area if it fails (careful, this changes logic requirements for goal)
                while relic_location in self.empty_locations:  # Reroll if the location is excluded
                    relic_location = self.random.choice(location_regions[area])
                self.get_location(relic_location).place_locked_item(self.create_item("Relic"))
                self.relic_placements.append((area_data[area], self.location_name_to_id[relic_location]))

        # Add filler items to have the same number of items and locations
        extras = len(mworld.get_unfilled_locations(player=self.player)) - len(pool)
        pool += [self.create_item(self.get_filler_item_name()) for _ in range(extras)]

        mworld.itempool += pool

    def create_event_item(self, event: str) -> WotWItem:
        return WotWItem(event, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(["50 Spirit Light", "100 Spirit Light"])

    def connect_to_menu(self, region: str, rule: Callable[[CollectionState], bool] | None = None) -> None:
        """Connect the region to menu. If the connection already exists, add the access rule instead."""
        if not self.multiworld.regions.entrance_cache[self.player].get(f"Menu -> {region}"):
            self.get_region("Menu").connect(self.get_region(region), rule=rule)
        else:
            entrance = self.get_entrance(f"Menu -> {region}")
            if rule is None:
                entrance.access_rule = lambda s: True
            else:
                add_rule(entrance, rule, combine="or")

    def precollect_event(self, event: str) -> None:
        self.push_precollected(self.create_event_item(event))

    def set_rules(self) -> None:
        player = self.player
        options = self.options
        difficulty = options.difficulty

        # Add the basic rules.
        set_moki_rules(self)
        combat_rules(self)
        unreachable_rules(self)

        # Add rules depending on the logic difficulty.
        if difficulty == LogicDifficulty.option_moki:
            # Extra rule for a location that is inaccessible in the lowest difficulty.
            add_rule(self.get_entrance("WestPools.Teleporter -> WestPools.BurrowOre"),
                     lambda state: state.has_all(("Burrow", "Clean Water", "Water Dash"), player), "or")
        if difficulty >= LogicDifficulty.option_gorlek:
            set_gorlek_rules(self)
            if options.glitches:
                set_gorlek_glitched_rules(self)
        if difficulty >= LogicDifficulty.option_kii:
            set_kii_rules(self)
            if options.glitches:
                set_kii_glitched_rules(self)
        if difficulty == LogicDifficulty.option_unsafe:
            set_unsafe_rules(self)
            if options.glitches:
                set_unsafe_glitched_rules(self)

        # Add victory condition
        victory_conn = self.get_region("WillowsEnd.ShriekArena").connect(self.get_region("Victory"))
        set_rule(victory_conn, lambda s: s.has_any(("Sword", "Hammer"), player)
                         and s.has_all(("Double Jump", "Dash", "Bash", "Grapple", "Glide", "Burrow", "Launch"), player))
        if "trees" in options.goal:
            for tree in ["MarshSpawn.RegenTree",
                         "MarshSpawn.DamageTree",
                         "HowlsDen.SwordTree",
                         "HowlsDen.DoubleJumpTree",
                         "MarshPastOpher.BowTree",
                         "WestHollow.DashTree",
                         "EastHollow.BashTree",
                         "GladesTown.DamageTree",
                         "InnerWellspring.GrappleTree",
                         "UpperPools.SwimDashTree",
                         "UpperReach.LightBurstTree",
                         "LowerDepths.FlashTree",
                         "LowerWastes.BurrowTree",
                         "WeepingRidge.LaunchTree",
                         ]:
                add_rule(victory_conn, lambda s, tree_name=tree: s.can_reach_region(tree_name, player))  # TODO check
                # The entrance checks for regions, so we need to add an indirect condition
                self.multiworld.register_indirect_condition(self.get_region(tree), victory_conn)

        if "wisps" in options.goal:
            add_rule(victory_conn, lambda s: s.has_all(("EastHollow.ForestsVoice", "LowerReach.ForestsMemory",
                                                        "UpperDepths.ForestsEyes", "WestPools.ForestsStrength",
                                                        "WindtornRuins.Seir"), player)
                     )

        if "quests" in options.goal:
            quest_list: list[str] = loc_sets["ExtraQuests"].copy()
            if options.quests == Quests.option_no_hand:
                quest_list += loc_sets["Quests"].copy()
            elif options.quests == Quests.option_all:
                quest_list += loc_sets["Quests"].copy() + loc_sets["HandToHand"].copy()
            if not options.glades_done:
                quest_list += loc_sets["Rebuild"].copy()
            if not options.qol and options.quests != Quests.option_none:
                quest_list += loc_sets["QOL"].copy()
            add_rule(victory_conn, lambda s: s.has_all((quests for quests in quest_list), player))

        if "relics" in options.goal:
            add_rule(victory_conn, lambda s: s.count("Relic", player) >= options.relic_count.value)

        # Rules for specific options
        if options.qol:
            self.precollect_event("GladesTown.TuleySpawned")
            self.get_region("WoodsEntry.LastTreeBranch").connect(self.get_region("WoodsEntry.TreeSeed"))
        if options.better_spawn:
            self.precollect_event("MarshSpawn.HowlBurnt")
            self.precollect_event("HowlsDen.BoneBarrier")
            self.precollect_event("EastPools.EntryLever")
            self.precollect_event("UpperWastes.LeverDoor")

        if "Everything" in options.no_combat or "Bosses" in options.no_combat:
            for entrance in ("ExternalStates -> SkipKwolok",
                             "ExternalStates -> SkipMora1",
                             "ExternalStates -> SkipMora2"):
                set_rule(self.get_entrance(entrance), lambda s: True)
        else:  # Connect these events when the seed is completed, to make them reachable.
            set_rule(self.get_entrance("ExternalStates -> SkipKwolok"),
                     lambda s: s.has("Victory", player))
            set_rule(self.get_entrance("ExternalStates -> SkipMora1"),
                     lambda s: s.has("Victory", player))
            set_rule(self.get_entrance("ExternalStates -> SkipMora2"),
                     lambda s: s.has("Victory", player))
        if "Everything" in options.no_combat or "Shrines" in options.no_combat:
            for entrance in (
                        "DenShrine -> HowlsDen.CombatShrineCompleted",
                        "MarshShrine -> MarshPastOpher.CombatShrineCompleted",
                        "GladesShrine -> WestGlades.CombatShrineCompleted",
                        "WoodsShrine -> WoodsMain.CombatShrineCompleted",
                        "DepthsShrine -> LowerDepths.CombatShrineCompleted"):
                set_rule(self.get_entrance(entrance), lambda s: True)

        if options.better_wellspring:
            self.precollect_event("InnerWellspring.TopDoorOpen")
        if options.no_ks:
            for event in ("MarshSpawn.KeystoneDoor",
                          "HowlsDen.KeystoneDoor",
                          "MarshPastOpher.EyestoneDoor",
                          "MidnightBurrows.KeystoneDoor",
                          "WoodsEntry.KeystoneDoor",
                          "WoodsMain.KeystoneDoor",
                          "LowerReach.KeystoneDoor",
                          "UpperReach.KeystoneDoor",
                          "UpperDepths.EntryKeystoneDoor",
                          "UpperDepths.CentralKeystoneDoor",
                          "UpperPools.KeystoneDoor",
                          "UpperWastes.KeystoneDoor"):
                self.precollect_event(event)
        if options.open_mode:
            for event in ("HowlsDen.BoneBarrier",
                          "MarshSpawn.ToOpherBarrier",
                          "MarshSpawn.TokkBarrier",
                          "MarshSpawn.LogBroken",
                          "MarshSpawn.BurrowsOpen",
                          "MidnightBurrows.HowlsDenShortcut",
                          "MarshPastOpher.EyestoneDoor",
                          "WestHollow.PurpleDoorOpen",
                          "EastHollow.DepthsLever",
                          "GladesTown.GromsWall",
                          "OuterWellspring.EntranceDoorOpen",
                          "InnerWellspring.MiddleDoorsOpen",
                          "InnerWellspring.TopDoorOpen",
                          "EastHollow.DepthsOpen",
                          "LowerReach.Lever",
                          "LowerReach.TPLantern",
                          "LowerReach.RolledSnowball",
                          "LowerReach.EastDoorLantern",
                          "LowerReach.ArenaBeaten",
                          "UpperWastes.LeverDoor",
                          "WindtornRuins.RuinsLever",
                          "WeepingRidge.ElevatorFightCompleted",
                          "EastPools.EntryLever",
                          "EastPools.CentralRoomPurpleWall",
                          "UpperPools.UpperWaterDrained",
                          "UpperPools.ButtonDoorAboveTree",):
                self.precollect_event(event)
        if options.no_rain:
            for event in ("HowlsDen.UpperLoopExitBarrier",
                          "HowlsDen.UpperLoopEntranceBarrier",
                          "HowlsDen.RainLifted",):
                self.precollect_event(event)
            if not options.better_spawn:
                self.precollect_event("MarshSpawn.HowlBurnt")
        if options.glades_done:
            for event in ("TuleyShop.LastTreeBranchRejected",
                          "TuleyShop.SelaFlowers",
                          "TuleyShop.StickyGrass",
                          "TuleyShop.Lightcatchers",
                          "TuleyShop.BlueMoon",
                          "TuleyShop.SpringPlants",
                          "TuleyShop.LastTree"):
                self.precollect_event(event)
            # These locations and events are inaccessible without Ore
            for event in ("GladesTown.RebuildTheGlades",
                          "GladesTown.BuildHuts",
                          "GladesTown.RoofsOverHeads",
                          "GladesTown.OnwardsAndUpwards",
                          "GladesTown.ClearThorns",
                          "GladesTown.CaveEntrance"):
                self.connect_to_menu(event)

        if options.quests == Quests.option_none:  # Open locations locked behind NPCs
            # Connecting the other quests is not necessary, as their event don't appear in logic for non-quest locations
            for quest in ("WoodsEntry.LastTreeBranch",
                          "WoodsEntry.DollQI",
                          "GladesTown.FamilyReunionKey"):
                self.connect_to_menu(quest + ".quest")
        if options.unpopular:
            self.precollect_event("Unpopular")

        if options.free_teleporters:
            self.precollect_event("RemoveTPLocks")
        # The location is connected to menu on victory in any case (for accessibility check, as precollect_event just
        # grabs the event item and not the location)
        self.connect_to_menu("RemoveTPLocks", rule=lambda s: s.has("Victory", player))

        if options.free_regenerate:
            self.precollect_event("RemoveRegionRegen")
        # Same as above, the location must be reachable
        self.connect_to_menu("RemoveRegionRegen", rule=lambda s: s.has("Victory", player))

        # UT Glitched support
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            from .generated_data.RulesUTGlitch import (
                set_gorlek_rules_ut_glitch,
                set_gorlek_glitched_rules_ut_glitch,
                set_kii_rules_ut_glitch,
                set_kii_glitched_rules_ut_glitch,
                set_unsafe_rules_ut_glitch,
                set_unsafe_glitched_rules_ut_glitch
                )
            one_level = "one_level" in options.ut_config or "max_logic" in options.ut_config
            max_logic = "max_logic" in options.ut_config
            glitches = "glitches" in options.ut_config or "max_logic" in options.ut_config

            # Add the ut_glitched logic that is relevant, and not already included in the base logic.
            if options.difficulty == LogicDifficulty.option_moki and (one_level or max_logic):
                set_gorlek_rules_ut_glitch(self)

            if (
                    options.difficulty == LogicDifficulty.option_moki and (one_level and glitches)
                    or options.difficulty.value >= LogicDifficulty.option_gorlek and not options.glitches and glitches
            ):
                set_gorlek_glitched_rules_ut_glitch(self)

            if (
                    options.difficulty == LogicDifficulty.option_moki and max_logic
                    or options.difficulty == LogicDifficulty.option_gorlek and one_level
            ):
                set_kii_rules_ut_glitch(self)

            if (
                    options.difficulty == LogicDifficulty.option_moki and max_logic
                    or options.difficulty == LogicDifficulty.option_gorlek and (one_level and glitches)
                    or options.difficulty.value >= LogicDifficulty.option_kii and not options.glitches and glitches
            ):
                set_kii_glitched_rules_ut_glitch(self)

            if (
                    options.difficulty.value <= LogicDifficulty.option_gorlek and max_logic
                    or options.difficulty == LogicDifficulty.option_kii and one_level
            ):
                set_unsafe_rules_ut_glitch(self)

            if (
                    options.difficulty.value <= LogicDifficulty.option_gorlek and max_logic
                    or options.difficulty == LogicDifficulty.option_kii and (one_level and glitches)
                    or options.difficulty == LogicDifficulty.option_unsafe and not options.glitches and glitches
            ):
                set_unsafe_glitched_rules_ut_glitch(self)

            if max_logic:
                menu_region = self.get_region("Menu")
                unpop_loc = WotWLocation(self.player, "Unpopular", None, menu_region)
                menu_region.locations.append(unpop_loc)
                unpop_loc.place_locked_item(self.create_event_item("Unpopular"))
                unpop_loc.access_rule = lambda s: s.has("UTGlitch", player)

            if ("free_tp" in options.ut_config and not options.free_teleporters) or max_logic:
                self.connect_to_menu("RemoveTPLocks", lambda s: s.has("UTGlitch", player))

            if "free_region" in options.ut_config or max_logic:
                for event in (
                        "danger_MidnightBurrows",
                        "danger_WestHollow",
                        "danger_EastHollow",
                        "danger_WestGlades",
                        "danger_OuterWellspring",
                        "danger_InnerWellspring",
                        "danger_WoodsEntry",
                        "danger_WoodsMain",
                        "danger_LowerReach",
                        "danger_UpperReach",
                        "danger_UpperDepths",
                        "danger_LowerDepths",
                        "danger_PoolsApproach",
                        "danger_EastPools",
                        "danger_UpperPools",
                        "danger_WestPools",
                        "danger_LowerWastes",
                        "danger_UpperWastes",
                        "danger_WeepingRidge",
                        "danger_WillowsEnd",
                    ):
                    self.connect_to_menu(event, lambda s: s.has("UTGlitch", player))

            ut_combat_rules(self, one_level=one_level, max_logic=max_logic)

    def connect_entrances(self) -> None:
        if self.options.door_rando != RandomizeDoors.option_disabled:

            # Universal Tracker support
            re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
            if re_gen_passthrough and self.game in re_gen_passthrough:
                slot_data: dict[str, Any] = re_gen_passthrough[self.game]
                id_to_door_map = {door_id: door_name for door_name, door_id in doors_map.items()}
                for entry_index, target_index in enumerate(slot_data["door_connections"]):
                    entry, target = id_to_door_map[entry_index + 1], id_to_door_map[target_index]
                    # Remove ` (Door)` from the region name using the [:-7], to connect to the base region and not the
                    # door. This matters in decoupled mode, since you cannot always reenter the door you just exited.
                    self.get_region(entry).connect(self.get_region(target[:-7]))

            else:  # Non-UT: randomize entrances and fetch the output formatted for slot_data
                coupled = self.options.door_rando == RandomizeDoors.option_coupled
                self.er_door_ids = generate_er_connections(self, coupled=coupled)

        else:  # door_rando not used: vanilla connections
            for entry, target in doors_vanilla:
                self.get_region(entry).connect(self.get_region(target))


    def fill_slot_data(self) -> dict[str, Any]:
        options = self.options
        logic_difficulty: list[str] = ["Moki", "Gorlek", "Kii", "Unsafe"]
        icons_paths: dict[str, str] = {}
        shops: list[str] = ["TwillenShop.Overcharge",
                            "TwillenShop.TripleJump",
                            "TwillenShop.Wingclip",
                            "TwillenShop.Swap",
                            "TwillenShop.LightHarvest",
                            "TwillenShop.Vitality",
                            "TwillenShop.Energy",
                            "TwillenShop.Finesse",
                            "OpherShop.WaterBreath",
                            "OpherShop.Spike",
                            "OpherShop.SpiritSmash",
                            "OpherShop.Teleport",
                            "OpherShop.SpiritStar",
                            "OpherShop.Blaze",
                            "OpherShop.Sentry",
                            "OpherShop.ExplodingSpike",
                            "OpherShop.ShockSmash",
                            "OpherShop.StaticStar",
                            "OpherShop.ChargeBlaze",
                            "OpherShop.RapidSentry",
                            "LupoShop.ShardMapIcon"
                            ]
        if not options.zone_hints:
            shops += ["LupoShop.HCMapIcon", "LupoShop.ECMapIcon",]
        for loc in shops:
            item = self.get_location(loc).item
            icon_path = get_item_iconpath(self, item, bool(options.shop_keywords))
            icons_paths.update({loc: icon_path})

        location_flags = 0b000000
        if options.quests != Quests.option_none:
            location_flags += 0b000001
        if options.quests == Quests.option_all:
            location_flags += 0b000010
        if not options.glades_done:
            location_flags += 0b000100
        if not options.no_trials:
            location_flags += 0b001000
        if not options.qol and options.quests != Quests.option_none:
            location_flags += 0b010000
        if not options.zone_hints:
            location_flags += 0b100000

        spawn_items_amount = (int(spawn_data[self.spawn_area].items_amount)
                              if options.spawn != StartingLocation.option_vanilla
                              else 0)

        slot_data: dict[str, Any] = {
            "difficulty": logic_difficulty[options.difficulty.value],
            "glitches": bool(options.glitches.value),
            "unpopular": bool(options.unpopular),
            "spawn_x": region_table[self.spawn_region_name][1],
            "spawn_y": region_table[self.spawn_region_name][2],
            "spawn_anchor": self.spawn_region_name,
            "spawn_amount": spawn_items_amount,
            "goal_trees": bool("trees" in options.goal),
            "goal_quests": bool("quests" in options.goal),
            "goal_wisps": bool("wisps" in options.goal),
            "goal_relics": bool("relics" in options.goal),
            "hard": bool(options.hard_mode.value),
            "qol": bool(options.qol.value),
            "no_cs": bool(options.skip_cutscenes.value),
            "shrine_hints": bool(options.hints.value and "shrines" not in options.no_combat),
            "trial_hints": bool(options.hints.value and not options.no_trials),
            "zone_hints": bool(options.zone_hints.value),
            "knowledge_hints": bool(options.knowledge_hints.value),
            "better_spawn": bool(options.better_spawn.value),
            "better_wellspring": bool(options.better_wellspring.value),
            "no_rain": bool(options.no_rain.value),
            "skip_boss": bool("everything" in options.no_combat or "bosses" in options.no_combat),
            "skip_demi_boss": bool("everything" in options.no_combat or "demi bosses" in options.no_combat),
            "skip_shrine": bool("everything" in options.no_combat or "shrines" in options.no_combat),
            "skip_arena": bool("everything" in options.no_combat or "arenas" in options.no_combat),
            "no_trials": bool(options.no_trials.value),
            "no_hearts": bool(options.no_hearts.value),
            "no_hand_quest": bool(options.quests == Quests.option_no_hand or options.quests == Quests.option_none),
            "no_quests": bool(options.quests == Quests.option_none),
            "no_ks": bool(options.no_ks.value),
            "open_mode": bool(options.open_mode),
            "glades_done": bool(options.glades_done),
            "shop_icons": icons_paths,
            "bonus": bool(options.extra_bonus or options.skill_upgrade),
            "door_rando": bool(options.door_rando != RandomizeDoors.option_disabled),
            "door_connections": self.er_door_ids,
            "decoupled": bool(options.door_rando == RandomizeDoors.option_decoupled),
            "relic_locs": self.relic_placements,
            "launch_frag": options.fragments_required.value if options.launch_fragments else 0,
            "total_frag": options.fragments_count.value,  # Only used by UT
            "free_tp": bool(options.free_teleporters.value),
            "regen": bool(options.free_regenerate.value),
            "death_link": int(options.death_link.value),
            "ap_version": 3,
            "location_flags": location_flags,
            "ut_config": options.ut_config.value,  # Only used by UT
        }

        return slot_data


class WotWItem(Item):
    game: str = "Ori and the Will of the Wisps"


class WotWLocation(Location):
    game: str = "Ori and the Will of the Wisps"
