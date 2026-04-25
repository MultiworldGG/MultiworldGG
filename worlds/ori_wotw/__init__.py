"""AP world for Ori and the Will of the Wisps."""

# TODO Black market ?
# TODO rename spawn locations and add aliases
# TODO Check that random is taken from world


from typing import Any, Callable
from collections import Counter

from entrance_rando import randomize_entrances
from .Rules import (set_moki_rules, set_gorlek_rules, set_gorlek_glitched_rules, set_kii_rules,
                    set_kii_glitched_rules, set_unsafe_rules, set_unsafe_glitched_rules)
from .AdditionalRules import combat_rules, unreachable_rules
from .Items import item_table
from .Items_Icons import get_item_iconpath
from .Locations import loc_table
from .Quests import quest_table
from .LocationGroups import loc_sets, location_regions
from .Events import event_table
from .Regions import region_table
from .Entrances import entrance_table
from .Refills import refill_events
from .Options import WotWOptions, option_groups, LogicDifficulty, Quests, StartingLocation
from .SpawnItems import spawn_items, spawn_names, early_items
from .Presets import options_presets
from .ItemGroups import item_groups
from .RulesFunctions import get_max, get_refill, get_enemy_cost, IMPOSSIBLE_COST
from .DoorData import doors_map, doors_vanilla

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule, set_rule
from BaseClasses import (Region, Location, Item, Tutorial, ItemClassification, LocationProgressType, CollectionState,
                         EntranceType, Entrance)


class WotWWeb(WebWorld):
    theme = "ocean"  # TODO documentation
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Ori and the Will of the Wisps randomizer connected to an Archipelago Multiworld",
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

    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        # Ask to update the max resources and the refills on the next call to `RulesFunctions.has_enough_resources`
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
        options = self.options  # TODO Use option error instead for some cases
        # Options checking
        if options.open_mode:
            options.no_rain.value = True
        # Escaping from Willow require to complete the elevator fight, so a tp is needed to escape.
        if options.spawn.value == StartingLocation.option_willow and not options.tp:
            options.spawn.value = StartingLocation.option_marsh  # No TP in pool: spawn somewhere else.
        # Without TP in the pool, some random spawn are dead-ends without better random spawn
        if not options.tp and not options.better_spawn:
            options.better_spawn.value = True
        if options.fragments_count.value < options.fragments_required.value:
            options.fragments_count.value = options.fragments_required.value
        # Spawning on willow usually gives Launch on spawn, which defeats the purpose of the options that affect Launch
        if (options.spawn.value == StartingLocation.option_willow
                and (options.launch_on_seir or options.launch_fragments)):
            options.spawn.value = StartingLocation.option_marsh

        # Selection of a random goal
        if "random" in options.goal:
            possible_goals = sorted(list(options.goal.value))
            possible_goals.remove("random")
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
            spawn_dict: dict[str, int] = {
                "MarshSpawn.Main": StartingLocation.option_marsh,
                "MidnightBurrows.Teleporter": StartingLocation.option_burrows,
                "HowlsDen.Teleporter": StartingLocation.option_howlsden,
                "EastHollow.Teleporter": StartingLocation.option_hollow,
                "GladesTown.Teleporter": StartingLocation.option_glades,
                "InnerWellspring.Teleporter": StartingLocation.option_wellspring,
                "WoodsEntry.Teleporter": StartingLocation.option_westwoods,
                "WoodsMain.Teleporter": StartingLocation.option_eastwoods,
                "LowerReach.Teleporter": StartingLocation.option_reach,
                "UpperDepths.Teleporter": StartingLocation.option_depths,
                "EastPools.Teleporter": StartingLocation.option_eastpools,
                "WestPools.Teleporter": StartingLocation.option_westpools,
                "LowerWastes.WestTP": StartingLocation.option_westwastes,
                "LowerWastes.EastTP": StartingLocation.option_eastwastes,
                "UpperWastes.NorthTP": StartingLocation.option_outerruins,
                "WindtornRuins.RuinsTP": StartingLocation.option_innerruins,
                "WillowsEnd.InnerTP": StartingLocation.option_willow,
            }
            goals: set[str] = set()
            combat: set[str] = set()

            self.options.difficulty.value = difficulty_dict[slot_data["difficulty"]]
            self.options.glitches.value = slot_data["glitches"]
            self.options.unpopular.value = slot_data["unpopular"]
            self.options.spawn.value = spawn_dict[slot_data["spawn_anchor"]]
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
            self.options.door_rando.value = slot_data["door_rando"]
            self.options.free_teleporters.value = slot_data["free_tp"]
            self.options.regenerate_requirements.value = slot_data["regen"]

    def create_regions(self) -> None:
        mworld = self.multiworld
        player = self.player
        options = self.options

        for region_name in region_table:
            region = Region(region_name, player, mworld)
            mworld.regions.append(region)

        for region_name in doors_map.keys():
            region = Region(region_name, player, mworld)
            mworld.regions.append(region)

        menu_region = Region("Menu", player, mworld)
        mworld.regions.append(menu_region)

        spawn_name = spawn_names[options.spawn]
        spawn_region = self.get_region(spawn_name)  # Links menu with spawn point
        menu_region.connect(spawn_region, rule=lambda state: True)

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

    def create_event(self, event: str, show_spoiler=False) -> None:
        """Create an event, place the item and attach it to an event region (all with the same name)."""
        event_region = Region(event, self.player, self.multiworld)
        event_location = WotWLocation(self.player, event, None, event_region)
        event_location.show_in_spoiler = show_spoiler
        event_location.place_locked_item(self.create_event_item(event))
        self.multiworld.regions.append(event_region)
        event_region.locations.append(event_location)

    def create_item(self, name: str) -> "WotWItem":
        return WotWItem(name, item_table[name][1], item_table[name][2], player=self.player)

    def create_items(self) -> None:
        mworld = self.multiworld
        options = self.options

        skipped_items: list[str] = []  # Remove one instance of the item
        removed_items: list[str] = []  # Remove all instances of the item
        pool: list[WotWItem] = []

        for item in spawn_items(self, options.spawn.value, options.difficulty.value):  # Staring items
            mworld.push_precollected(self.create_item(item))
            skipped_items.append(item)

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
                while relic_location in self.empty_locations:  # Reroll if the location is excluded
                    relic_location = self.random.choice(location_regions[area])
                self.get_location(relic_location).place_locked_item(self.create_item("Relic"))
                self.relic_placements.append((area_data[area], self.location_name_to_id[relic_location]))

        # Add some items to sphere 1
        items, ks_amount = early_items(self, options.spawn.value)
        for item in items:
            self.multiworld.early_items[self.player][item] = 1
        if not options.no_ks and ks_amount > 0:
            self.multiworld.early_items[self.player]["Keystone"] = ks_amount

        # Add filler items to have the same number of items and locations
        extras = len(mworld.get_unfilled_locations(player=self.player)) - len(pool)
        pool += [self.create_item(self.get_filler_item_name()) for _ in range(extras)]

        mworld.itempool += pool

    def create_event_item(self, event: str) -> "WotWItem":
        return WotWItem(event, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(["50 Spirit Light", "100 Spirit Light"])

    def connect_to_menu(self, region: str, rule: Callable[[CollectionState], bool] | None = None) -> None:
        """Connect the region to menu (if the connection does not already exist)."""
        if not self.multiworld.regions.entrance_cache[self.player].get(f"Menu -> {region}"):
            self.get_region("Menu").connect(self.get_region(region), rule=rule)

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
                add_rule(victory_conn, lambda s, tree=tree: s.can_reach_region(tree, player))
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
            self.connect_to_menu("GladesTown.TuleySpawned")
            self.get_region("WoodsEntry.LastTreeBranch").connect(self.get_region("WoodsEntry.TreeSeed"))
        if options.better_spawn:
            self.connect_to_menu("MarshSpawn.HowlBurnt")
            self.connect_to_menu("HowlsDen.BoneBarrier")
            self.connect_to_menu("EastPools.EntryLever")
            self.connect_to_menu("UpperWastes.LeverDoor")

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
            self.connect_to_menu("InnerWellspring.TopDoorOpen")
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
                self.connect_to_menu(event)
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
                self.connect_to_menu(event)
        if options.no_rain:
            for event in ("HowlsDen.UpperLoopExitBarrier",
                          "HowlsDen.UpperLoopEntranceBarrier",
                          "HowlsDen.RainLifted",):
                self.connect_to_menu(event)
            if not options.better_spawn:
                self.connect_to_menu("MarshSpawn.HowlBurnt")
        if options.glades_done:
            for event in ("TuleyShop.LastTreeBranchRejected",
                          "TuleyShop.SelaFlowers",
                          "TuleyShop.StickyGrass",
                          "TuleyShop.Lightcatchers",
                          "TuleyShop.BlueMoon",
                          "TuleyShop.SpringPlants",
                          "TuleyShop.LastTree"):
                self.connect_to_menu(event)
            # This location is unaccessible without Ore, so it is manually collected in this case
            self.connect_to_menu("GladesTown.RebuildTheGlades")
            for event in ("GladesTown.BuildHuts",
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
            self.create_event("Unpopular")
            self.connect_to_menu("Unpopular")

        if options.free_teleporters:
            self.connect_to_menu("RemoveTPLocks")
        else:
            self.connect_to_menu("RemoveTPLocks", rule=lambda s: s.has("Victory", player))

        if options.regenerate_requirements <= options.difficulty:
            self.connect_to_menu("RemoveRegionRegen")
        else:
            self.connect_to_menu("RemoveRegionRegen", rule=lambda s: s.has("Victory", player))


    def connect_entrances(self) -> None:
        if self.options.door_rando:

            # Universal Tracker support
            re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
            if re_gen_passthrough and self.game in re_gen_passthrough:
                slot_data: dict[str, Any] = re_gen_passthrough[self.game]
                id_to_door_map = {door_id: door_name for door_name, door_id in doors_map.items()}
                for entry_index, target_index in enumerate(slot_data["door_connections"]):
                    entry, target = id_to_door_map[entry_index + 1], id_to_door_map[target_index]
                    self.get_region(entry).connect(self.get_region(target))

            else:
                er_targets: list[Entrance] = []
                exits: list[Entrance] = []
                for door in doors_map:
                    door_region: Region = self.get_region(door)
                    er_target = door_region.create_er_target(door)
                    er_target.randomization_type = EntranceType.TWO_WAY
                    er_targets.append(er_target)

                    exit_entrance = door_region.create_exit(door)
                    exit_entrance.randomization_type = EntranceType.TWO_WAY
                    exits.append(exit_entrance)

                er_results = randomize_entrances(self,
                                                 coupled=True,
                                                 target_group_lookup={0: [0]},
                                                 er_targets=er_targets,
                                                 exits=exits)

                self.er_door_ids = [0] * 32  # This contains the ER results for slot_data
                for (source_exit, target_entrance) in er_results.pairings:
                    self.er_door_ids[doors_map[source_exit] - 1] = doors_map[target_entrance]
        else:
            for entry, target in doors_vanilla:
                self.get_region(entry).connect(self.get_region(target))


    def fill_slot_data(self) -> dict[str, Any]:
        options = self.options
        logic_difficulty: list[str] = ["Moki", "Gorlek", "Kii", "Unsafe"]
        coord: list[list[int | str]] = [
            [-799, -4310, "MarshSpawn.Main"],
            [-945, -4582, "MidnightBurrows.Teleporter"],
            [-328, -4536, "HowlsDen.Teleporter"],
            [-150, -4238, "EastHollow.Teleporter"],
            [-307, -4153, "GladesTown.Teleporter"],
            [-1308, -3675, "InnerWellspring.Teleporter"],
            [611, -4162, "WoodsEntry.Teleporter"],
            [1083, -4052, "WoodsMain.Teleporter"],
            [-259, -3962, "LowerReach.Teleporter"],
            [513, -4361, "UpperDepths.Teleporter"],
            [-1316, -4153, "EastPools.Teleporter"],
            [-1656, -4171, "WestPools.Teleporter"],
            [1456, -3997, "LowerWastes.WestTP"],
            [1992, -3902, "LowerWastes.EastTP"],
            [2044, -3679, "UpperWastes.NorthTP"],
            [2130, -3984, "WindtornRuins.RuinsTP"],
            [422, -3864, "WillowsEnd.InnerTP"]
        ]
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
        if not options.qol:
            location_flags += 0b010000
        if not options.zone_hints:
            location_flags += 0b100000

        slot_data: dict[str, Any] = {
            "difficulty": logic_difficulty[options.difficulty.value],
            "glitches": bool(options.glitches.value),
            "unpopular": bool(options.unpopular),
            "spawn_x": coord[options.spawn.value][0],
            "spawn_y": coord[options.spawn.value][1],
            "spawn_anchor": coord[options.spawn.value][2],
            "goal_trees": bool("trees" in options.goal),
            "goal_quests": bool("quests" in options.goal),
            "goal_wisps": bool("wisps" in options.goal),
            "goal_relics": bool("relics" in options.goal),
            "hard": bool(options.hard_mode.value),
            "qol": bool(options.qol.value),
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
            "door_rando": bool(options.door_rando),
            "door_connections": self.er_door_ids,
            "relic_locs": self.relic_placements,
            "launch_frag": options.fragments_required.value if options.launch_fragments else 0,
            "total_frag": options.fragments_count.value,  # Only used by UT
            "free_tp": options.free_teleporters.value,
            "regen": options.regenerate_requirements.value,
            "death_link": int(options.death_link.value),
            "ap_version": 2,
            "location_flags": location_flags,
        }

        return slot_data


class WotWItem(Item):
    game: str = "Ori and the Will of the Wisps"


class WotWLocation(Location):
    game: str = "Ori and the Will of the Wisps"
