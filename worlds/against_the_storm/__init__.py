import logging
import re
from random import sample
from typing import Any, ClassVar, Optional

from BaseClasses import CollectionState, MultiWorld, Region, Tutorial

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule, set_rule

from .Items import AgainstTheStormItem, ATSItemClassification, get_item_name_groups, item_dict
from .Locations import AgainstTheStormLocation, ATSLocationClassification, get_location_name_groups, location_dict
from .Options import AgainstTheStormOptions, RecipeShuffle
from .Recipes import Recipe, blueprint_recipes, nonitem_blueprint_recipes, satisfies_recipe

class AgainstTheStormWeb(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Against The Storm with MWGG.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ryguy9999"],
    )

    tutorials = [setup_en]

class AgainstTheStormWorld(World):
    """
    Against the Storm is a roguelite city builder about managing resource production chains and keeping villagers happy.
    """

    game = "Against the Storm"
    options_dataclass = AgainstTheStormOptions
    options: AgainstTheStormOptions # type: ignore
    topology_present = True
    web = AgainstTheStormWeb()
    base_id = 9999000000
    item_name_to_id: ClassVar = {item: id for id, item in enumerate(item_dict.keys(), base_id)}
    location_name_to_id: ClassVar = {location: id for id, location in enumerate(location_dict.keys(), base_id)}
    item_name_groups = get_item_name_groups(item_dict)
    location_name_groups = get_location_name_groups(location_dict)

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.included_location_indices: list[int] = []
        self.production_recipes: dict[str, list[Recipe]] = {}
        self.filler_items: list[str] = []

    def generate_early(self):
        base_locations = [name for (name, (classification, _logic, _loc_group)) in location_dict.items() if
                          classification == ATSLocationClassification.basic or
                          classification == ATSLocationClassification.dlc_keepers and self.options.enable_keepers_dlc or
                          classification == ATSLocationClassification.dlc_nightwatchers and
                            self.options.enable_nightwatchers_dlc]
        total_location_count = (len(base_locations) +
                                self.options.reputation_locations_per_biome.value * (6 +
                                 (2 if self.options.enable_keepers_dlc else 0) +
                                 (2 if self.options.enable_nightwatchers_dlc else 0)) +
                                self.options.extra_trade_locations.value +
                                (self.options.grove_expedition_locations if self.options.enable_keepers_dlc else 0)
                                - len(self.options.exclude_locations.value))
        total_item_count = len([name for (name, (_class, classification, _item_group)) in item_dict.items() if
                                classification == ATSItemClassification.good or
                                classification == ATSItemClassification.guardian_part and self.options.seal_items or
                                classification == ATSItemClassification.blueprint and self.options.blueprint_items or
                                classification == ATSItemClassification.keepers_dlc_blueprint and
                                    self.options.enable_keepers_dlc or
                                classification == ATSItemClassification.biome_key and self.options.enable_biome_keys or
                                classification == ATSItemClassification.keepers_dlc_biome_key and
                                    self.options.enable_keepers_dlc and self.options.enable_biome_keys or
                                classification == ATSItemClassification.nightwatchers_dlc_biome_key and
                                    self.options.enable_nightwatchers_dlc and self.options.enable_biome_keys])
        if total_location_count < total_item_count:
            while total_location_count < total_item_count:
                self.options.reputation_locations_per_biome.value += 1
                total_location_count += (6 + (2 if self.options.enable_keepers_dlc else 0) +
                                         (2 if self.options.enable_nightwatchers_dlc else 0))
            logging.warning(f"[Against the Storm] Fewer locations than items detected in player #{self.player} "
                            "options, increased reputation_locations_per_biome to "
                            f"{self.options.reputation_locations_per_biome.value} to fit all items")

        self.included_location_indices.append(1)
        # This evenly spreads the option's number of locations between 2 and 17
        # Generating, for example, [10], [4, 8, 11, 15], or [2-17 sans 9]
        for i in range(self.options.reputation_locations_per_biome):
            self.included_location_indices.append(
                round(1 + (i + 1) * (17 / (self.options.reputation_locations_per_biome + 1))))

        # Recipe shuffle
        all_production: dict[str, list[Recipe]] = {}
        all_production.update(blueprint_recipes)
        all_production.update(nonitem_blueprint_recipes)
        if hasattr(self.multiworld, "re_gen_passthrough"):
            prod_recipes = getattr(self.multiworld, "re_gen_passthrough")["Against the Storm"]['production_recipes']
            self.production_recipes = {building: [Recipe(recipe[0], recipe[1]) for recipe in recipes]
                                       for building, recipes in prod_recipes.items()}
            pass
        else:
            if self.options.recipe_shuffle != "vanilla":
                skip_cws = (self.options.recipe_shuffle.value == RecipeShuffle.option_exclude_crude_ws or
                    self.options.recipe_shuffle.value == RecipeShuffle.option_exclude_crude_ws_and_ms_post)
                skip_msp = (self.options.recipe_shuffle.value == RecipeShuffle.option_exclude_ms_post or
                    self.options.recipe_shuffle.value == RecipeShuffle.option_exclude_crude_ws_and_ms_post)

                # Store as a dict from product -> Recipe, to iterate one of each product for logical reachability
                all_recipes: dict[str, list[Recipe]] = {}
                for blueprint, recipes in all_production.items():
                    if blueprint == "Crude Workstation" and skip_cws or blueprint == "Makeshift Post" and skip_msp:
                        continue
                    for recipe in recipes:
                        if recipe.product not in all_recipes:
                            all_recipes[recipe.product] = []
                        all_recipes[recipe.product].append(recipe)

                valid_blueprints = list(blueprint_recipes.keys())
                if not skip_cws:
                    valid_blueprints.append("Crude Workstation")
                if not skip_msp:
                    valid_blueprints.append("Makeshift Post")
                # First, add one recipe for each resource to a non-glade event bp to ensure they are all logically reachable
                for _product, recipes in all_recipes.items():
                    blueprint = self.random.choice(valid_blueprints)
                    if blueprint not in self.production_recipes:
                        self.production_recipes[blueprint] = []
                    recipe_index = self.random.randint(0, len(recipes)-1)
                    self.production_recipes[blueprint].append(recipes[recipe_index])
                    recipes.pop(recipe_index)
                    if len(self.production_recipes[blueprint]) >= len(all_production[blueprint]):
                        valid_blueprints.remove(blueprint)

                valid_blueprints.extend([bp for bp in list(nonitem_blueprint_recipes.keys()) if
                                        bp != "Crude Workstation" and bp != "Makeshift Post"])
                # Now, we distribute the remaining recipes among all production buildings
                for _product, recipes in all_recipes.items():
                    for recipe in recipes:
                        filtered_blueprints = [bp for bp in valid_blueprints if bp not in self.production_recipes
                                        or not any(recipe.product == rec.product for rec in self.production_recipes[bp])]
                        blueprint = self.random.choice(filtered_blueprints if len(filtered_blueprints) > 0 else
                                                    valid_blueprints)
                        if blueprint not in self.production_recipes:
                            self.production_recipes[blueprint] = []
                        self.production_recipes[blueprint].append(recipe)
                        if len(self.production_recipes[blueprint]) >= len(all_production[blueprint]):
                            valid_blueprints.remove(blueprint)
            else:
                self.production_recipes = all_production

    def get_filler_item_name(self):
        choice = self.random.choices(self.filler_items)[0]
        # Reroll Survivor Bonding to halve its occurence
        return (self.random.choices(self.filler_items)[0] if
                choice == "Survivor Bonding" and self.random.random() < 0.5 else choice)

    def create_item(self, name: str) -> AgainstTheStormItem:
        return AgainstTheStormItem(name, item_dict[name][0], self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        itempool: list[str] = []
        biome_keys: list[str] = []
        for item_key, (_ap_classification, classification, _item_group) in item_dict.items():
            match classification:
                case ATSItemClassification.good:
                    itempool.append(item_key)
                case ATSItemClassification.blueprint:
                    if self.options.blueprint_items:
                        itempool.append(item_key)
                case ATSItemClassification.filler:
                    self.filler_items.append(item_key)
                case ATSItemClassification.guardian_part:
                    if self.options.seal_items:
                        itempool.append(item_key)
                case ATSItemClassification.keepers_dlc_blueprint:
                    if self.options.enable_keepers_dlc and self.options.blueprint_items:
                        itempool.append(item_key)
                case ATSItemClassification.biome_key:
                    if self.options.enable_biome_keys:
                        biome_keys.append(item_key)
                case ATSItemClassification.keepers_dlc_biome_key:
                    if self.options.enable_biome_keys and self.options.enable_keepers_dlc:
                        biome_keys.append(item_key)
                case ATSItemClassification.nightwatchers_dlc_biome_key:
                    if self.options.enable_biome_keys and self.options.enable_nightwatchers_dlc:
                        biome_keys.append(item_key)

        if self.options.enable_biome_keys:
            biome_precollected = any(key in [item.name for item in self.multiworld.precollected_items[self.player]]
                                     for key in biome_keys)
            # Pick a random biome to be the starting biome, IF the player hasn't for us
            if not biome_precollected:
                starting_biome = self.random.choice(biome_keys)
                biome_keys.remove(starting_biome)
                self.multiworld.push_precollected(self.create_item(starting_biome))
            itempool.extend(biome_keys)

        # Fill remaining itempool space with filler
        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            itempool += [self.create_filler().name]

        self.multiworld.itempool += map(self.create_item, itempool)

    def create_regions(self) -> None:
        location_pool: dict[str, int] = {}

        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        trade_locations: list[str] = []
        for name, (classification, _logic, _loc_group) in location_dict.items():
            match classification:
                case ATSLocationClassification.basic:
                    location_pool[name] = self.location_name_to_id[name]
                case ATSLocationClassification.biome_rep:
                    loc_index = int(re.search(r"^(\d\d?)\w\w Reputation - .*$", name).group(1)) # type: ignore
                    if loc_index in self.included_location_indices:
                        location_pool[name] = self.location_name_to_id[name]
                case ATSLocationClassification.extra_trade:
                    trade_locations.append(name)
                case ATSLocationClassification.dlc_keepers:
                    if self.options.enable_keepers_dlc:
                        location_pool[name] = self.location_name_to_id[name]
                case ATSLocationClassification.dlc_keepers_biome_rep:
                    if self.options.enable_keepers_dlc:
                        loc_index = int(re.search(r"^(\d\d?)\w\w Reputation - .*$", name).group(1)) # type: ignore
                        if loc_index in self.included_location_indices:
                            location_pool[name] = self.location_name_to_id[name]
                case ATSLocationClassification.dlc_nightwatchers:
                    if self.options.enable_nightwatchers_dlc:
                        location_pool[name] = self.location_name_to_id[name]
                case ATSLocationClassification.dlc_nightwatchers_biome_rep:
                    if self.options.enable_nightwatchers_dlc:
                        loc_index = int(re.search(r"^(\d\d?)\w\w Reputation - .*$", name).group(1)) # type: ignore
                        if loc_index in self.included_location_indices:
                            location_pool[name] = self.location_name_to_id[name]
                case ATSLocationClassification.dlc_grove_expedition:
                    if self.options.enable_keepers_dlc:
                        expedition_index = int(re.search(r"^Coastal Grove - (\d\d?)\w\w Expedition$", name).group(1)) # type: ignore
                        if expedition_index <= self.options.grove_expedition_locations:
                            location_pool[name] = self.location_name_to_id[name]

        # Samples a number of trade locations based on yaml setting (or doesn't for UT, so all locations exist for it)
        if not getattr(self.multiworld, "generation_is_fake", False):
            trade_locations = sample(trade_locations, self.options.extra_trade_locations.value)
            
        for location in trade_locations:
            location_pool[location] = self.location_name_to_id[location]

        main_region = Region("Main", self.player, self.multiworld)

        main_region.add_locations(location_pool, AgainstTheStormLocation)
        self.multiworld.regions.append(main_region)

        menu_region.connect(main_region)

    def can_goal(self, state: CollectionState) -> bool:
        if self.options.seal_items and not state.has_all(["Sealed Forest",
                "Guardian Heart", "Guardian Blood", "Guardian Feathers", "Guardian Essence"], self.player):
            return False

        if self.options.required_seal_tasks.value > 1:
            return satisfies_recipe(state, self.player,
                                    self.production_recipes if self.options.blueprint_items.value else None,
                ["Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Coal,Oil,Sea Marrow", "Amber",
                 "Ale,Training Gear,Incense,Scrolls,Wine,Tea", "Tools", "Purging Fire", "Planks", "Bricks", "Fabric",
                 # Above is the baseline that ensures normal winnable conditions, below ensures every Seal task
                 "Pack of Crops", "Pack of Provisions", "Pack of Building Materials", "Stone,Sea Marrow,Training Gear",
                 "Pipes", "Parts", "Ancient Tablet"])
        else:
            return satisfies_recipe(state, self.player,
                                    self.production_recipes if self.options.blueprint_items.value else None,
                ["Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Coal,Oil,Sea Marrow", "Amber",
                 "Ale,Training Gear,Incense,Scrolls,Wine,Tea","Tools", "Purging Fire", "Planks", "Bricks", "Fabric"])

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: self.can_goal(state)

        production_recipes = self.production_recipes if self.options.blueprint_items.value else None
        biome_keys = [key for key, (_classification, item_class, _group) in item_dict.items() if
                      item_class == ATSItemClassification.biome_key or
                      item_class == ATSItemClassification.keepers_dlc_biome_key or
                      item_class == ATSItemClassification.nightwatchers_dlc_biome_key]

        for location in self.multiworld.get_locations(self.player):
            (_classification, logic, group) = location_dict[location.name]
            set_rule(location,
                     lambda state, logic=logic: satisfies_recipe(state, self.player, production_recipes, logic))
            # Most locations that would need a biome key have the biome they're in as a group
            if group in biome_keys and self.options.enable_biome_keys:
                add_rule(location, lambda state, group=group: state.has(group, self.player))
            if group == "Coastal Grove Expeditions" and self.options.enable_biome_keys:
                add_rule(location, lambda state: state.has("Coastal Grove", self.player))

        if self.options.blueprint_items.value:
            add_rule(self.get_location("The Marshlands - Harvest from an Ancient Proto Wheat"),
                    lambda state: state.has("Forager's Camp", self.player))
            add_rule(self.get_location("The Marshlands - Harvest from a Dead Leviathan"),
                    lambda state: state.has("Trapper's Camp", self.player))
            add_rule(self.get_location("The Marshlands - Harvest from a Giant Proto Fungus"),
                    lambda state: state.has("Herbalist's Camp", self.player))
            
    def interpret_slot_data(self, slot_data: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
        if slot_data is not None:
            self.production_recipes = {building: [Recipe(recipe[0], recipe[1]) for recipe in recipes]
                                   for building, recipes in slot_data["production_recipes"].items()}
        return slot_data

    def fill_slot_data(self) -> dict[str, Any]:
        # Convert Recipes into list[Any]s for storing in slot data
        prod_recipes: dict[str, list[list[Any]]] = {building: [[recipe.product, recipe.stars] for recipe in recipes]
                                                    for building, recipes in self.production_recipes.items()}
        return {
            "recipe_shuffle": self.options.recipe_shuffle.value,
            "deathlink": self.options.deathlink.value,
            "blueprint_items": self.options.blueprint_items.value,
            "continue_blueprints_for_reputation": self.options.continue_blueprints_for_reputation.value,
            "seal_items": self.options.seal_items.value,
            "required_seal_tasks": self.options.required_seal_tasks.value,
            "enable_keepers_dlc": self.options.enable_keepers_dlc.value,
            "enable_nightwatchers_dlc": self.options.enable_nightwatchers_dlc.value,
            "enable_biome_keys": self.options.enable_biome_keys.value,
            "rep_location_indices": self.included_location_indices,
            "production_recipes": prod_recipes
        }
