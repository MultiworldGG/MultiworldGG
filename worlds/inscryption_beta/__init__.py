from .Options import InscryptionOptions, ActUnlocks, EpitaphPiecesRandomization, PaintingChecksBalancing, \
    RandomizeHammer, Act2RandomizeBridge, RandomizeShortcuts, RandomizeVesselUpgrades, StartingAct, \
    RandomizeChallenges, inscryption_option_groups
from .Items import act1_items, act2_items, act3_items, act2_3_items, act_items, filler_items, \
    trap_items, item_groups, base_id, InscryptionItem
from .Locations import act1_locations, act2_locations, act3_locations, regions_to_locations
from .Regions import inscryption_regions_all
from typing import Dict, Any
from . import Rules
from BaseClasses import Region, Item, Tutorial, ItemClassification
from Options import OptionError
from worlds.AutoWorld import World, WebWorld
import random


class InscrypWeb(WebWorld):
    theme = "dirt"

    guide_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Inscryption Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["DrBibop"]
    )

    guide_fr = Tutorial(
        "Multiworld Setup Guide",
        "Un guide pour configurer Inscryption Archipelago Multiworld",
        "Français",
        "setup_fr.md",
        "setup/fr",
        ["Glowbuzz"]
    )

    tutorials = [guide_en, guide_fr]

    bug_report_page = "https://github.com/DrBibop/Archipelago_Inscryption/issues"

    option_groups = inscryption_option_groups


class InscryptionWorld(World):
    """
    Inscryption is an inky black card-based odyssey that blends the deckbuilding roguelike,
    escape-room style puzzles, and psychological horror into a blood-laced smoothie.
    Darker still are the secrets inscrybed upon the cards...
    """
    game = "Inscryption Beta"
    web = InscrypWeb()
    options_dataclass = InscryptionOptions
    options: InscryptionOptions
    all_items = act1_items + act2_items + act3_items + act2_3_items + act_items + filler_items + trap_items
    item_name_to_id = {item["name"]: i + base_id for i, item in enumerate(all_items)}
    all_locations = act1_locations + act2_locations + act3_locations
    location_name_to_id = {location: i + base_id for i, location in enumerate(all_locations)}
    item_name_groups = item_groups
    required_epitaph_pieces_count = 9
    required_epitaph_pieces_name = "Epitaph Piece"

    def generate_early(self) -> None:
        if not self.options.enable_act_1 and not self.options.enable_act_2 and not self.options.enable_act_3:
            raise OptionError(f'{self.player_name} must enable at least one act.')
        if self.options.act_unlocks == ActUnlocks.option_items:
            if  (not self.options.enable_act_1 and self.options.starting_act == StartingAct.option_act_1) or \
                (not self.options.enable_act_2 and self.options.starting_act == StartingAct.option_act_2) or \
                (not self.options.enable_act_3 and self.options.starting_act == StartingAct.option_act_3):
                    possible_starts = []
                    if self.options.enable_act_1: possible_starts.append(StartingAct.option_act_1)
                    if self.options.enable_act_2: possible_starts.append(StartingAct.option_act_2)
                    if self.options.enable_act_3: possible_starts.append(StartingAct.option_act_3)
                    self.options.starting_act = StartingAct(self.random.choice(possible_starts))
        if not self.options.enable_act_1 and not self.options.enable_act_3:
            self.options.trap_type_weights.value["Bleach Trap"] = 0
        if not self.options.enable_act_2:
            self.options.trap_type_weights.value["Deck Size Trap"] = 0

        self.all_items = [item.copy() for item in self.all_items]

        if self.options.epitaph_pieces_randomization == EpitaphPiecesRandomization.option_all_pieces:
            self.required_epitaph_pieces_name = "Epitaph Piece"
            self.required_epitaph_pieces_count = 9
        elif self.options.epitaph_pieces_randomization == EpitaphPiecesRandomization.option_in_groups:
            self.required_epitaph_pieces_name = "Epitaph Pieces"
            self.required_epitaph_pieces_count = 3
        else:
            self.required_epitaph_pieces_name = "Epitaph Pieces"
            self.required_epitaph_pieces_count = 1
        if self.options.randomize_nodes or self.options.randomize_challenges != RandomizeChallenges.option_disable:
            self.all_items[6]["classification"] = ItemClassification.progression
            self.all_items[11]["classification"] = ItemClassification.progression
            self.all_items[12]["classification"] = ItemClassification.progression
            self.all_items[13]["classification"] = ItemClassification.progression
            self.all_items[14]["classification"] = ItemClassification.progression
            self.all_items[15]["classification"] = ItemClassification.progression
        elif self.options.painting_checks_balancing == PaintingChecksBalancing.option_balanced:
            self.all_items[6]["classification"] = ItemClassification.progression
            self.all_items[11]["classification"] = ItemClassification.progression

        if self.options.painting_checks_balancing == PaintingChecksBalancing.option_force_filler \
                and not self.options.enable_act_2\
                and not self.options.enable_act_3:
            self.all_items[3]["classification"] = ItemClassification.filler

        if self.options.epitaph_pieces_randomization != EpitaphPiecesRandomization.option_all_pieces:
            self.all_items[len(act1_items) + 3]["count"] = self.required_epitaph_pieces_count

        if self.options.randomize_vessel_upgrades != RandomizeVesselUpgrades.option_randomize:
            self.all_items[len(act1_items) + len(act2_items) + 15]["count"] = 2

        if self.options.act_unlocks == ActUnlocks.option_items:
            if self.options.starting_act == StartingAct.option_act_1: 
                self.multiworld.push_precollected(self.create_item("Act 1"))
            elif self.options.starting_act == StartingAct.option_act_2: 
                self.multiworld.push_precollected(self.create_item("Act 2"))
            elif self.options.starting_act == StartingAct.option_act_3: 
                self.multiworld.push_precollected(self.create_item("Act 3"))

    def get_filler_item_name(self) -> str:
        if self.options.trap_chance == 100 and any(v > 0 for v in self.options.trap_type_weights.values()):
            return self.random.choice(trap_items)["name"]
        return self.random.choice(filler_items)["name"]

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        item_data = self.all_items[item_id - base_id]
        return InscryptionItem(name, item_data["classification"], item_id, self.player)

    def create_items(self) -> None:
        nb_items_added = 0
        useful_items = self.all_items.copy()
        included_locations = len(self.all_locations)
        filler_trap_items = filler_items + trap_items

        useful_items = [item for item in useful_items
                        if not any(filler_trap_item["name"] == item["name"] for filler_trap_item in filler_trap_items)]
        if self.options.act_unlocks == ActUnlocks.option_items:
            if not self.options.enable_act_3 or self.options.starting_act == StartingAct.option_act_3: 
                useful_items.pop(len(act1_items) + len(act2_items) + len(act3_items) + 3)
            if not self.options.enable_act_2 or self.options.starting_act == StartingAct.option_act_2: 
                useful_items.pop(len(act1_items) + len(act2_items) + len(act3_items) + 2)
            if not self.options.enable_act_1 or self.options.starting_act == StartingAct.option_act_1: 
                useful_items.pop(len(act1_items) + len(act2_items) + len(act3_items) + 1)
        else:
            useful_items.pop(len(act1_items) + len(act2_items) + len(act3_items) + 3)
            useful_items.pop(len(act1_items) + len(act2_items) + len(act3_items) + 2)
            useful_items.pop(len(act1_items) + len(act2_items) + len(act3_items) + 1)
        if self.options.randomize_hammer != RandomizeHammer.option_randomize \
        or not (self.options.enable_act_2 or self.options.enable_act_3):
            useful_items.pop(len(act1_items) + len(act2_items) + len(act3_items))
        if self.options.enable_act_3:
            if not self.options.act3_overhaul:
                useful_items.pop(len(act1_items) + len(act2_items) + 18)
                useful_items.pop(len(act1_items) + len(act2_items) + 17)
            if self.options.randomize_vessel_upgrades == RandomizeVesselUpgrades.option_vanilla:
                useful_items.pop(len(act1_items) + len(act2_items) + 16)
                useful_items.pop(len(act1_items) + len(act2_items) + 15)
                included_locations -= 4
            if self.options.randomize_shortcuts != RandomizeShortcuts.option_randomize:
                useful_items.pop(len(act1_items) + len(act2_items) + 14)
                useful_items.pop(len(act1_items) + len(act2_items) + 13)
                useful_items.pop(len(act1_items) + len(act2_items) + 12)
                if self.options.randomize_shortcuts == RandomizeShortcuts.option_vanilla:
                    included_locations -= 3
        if self.options.enable_act_2:
            if self.options.act2_randomize_bridge == Act2RandomizeBridge.option_disable:
                useful_items.pop(len(act1_items) + 13)
            if self.options.epitaph_pieces_randomization == EpitaphPiecesRandomization.option_all_pieces:
                useful_items.pop(len(act1_items) + 3)
            else:
                useful_items.pop(len(act1_items) + 2)
        if self.options.enable_act_1:
            if self.options.randomize_challenges == RandomizeChallenges.option_disable:
                useful_items.pop(31) # progressive grizzlies
                useful_items.pop(30) # progressive squirrel
                useful_items.pop(29) # progressive candle
                useful_items.pop(28) # more difficult challenge
                useful_items.pop(27) # all totem battles challenge
                useful_items.pop(26) # tipped scales challenge
                useful_items.pop(25) # boss totems challenge
                useful_items.pop(24) # pricey pelts challenge
                useful_items.pop(23) # smaller backpack challenge
            elif self.options.randomize_challenges == RandomizeChallenges.option_no_grizzlies:
                useful_items.pop(31) # progressive grizzlies
            if not self.options.randomize_nodes:
                useful_items.pop(22) # goobert node
                useful_items.pop(21) # campfire node
                useful_items.pop(20) # backpack node
                useful_items.pop(19) # sacrifice stones node
                useful_items.pop(18) # bone altar node
                useful_items.pop(17) # mycologists node
                useful_items.pop(16) # woodcarver node
            if self.options.randomize_challenges != RandomizeChallenges.option_disable:
                useful_items.pop(13) # bee figurine (it's progressive now)
                useful_items.pop(12) # extra candle (it's progressive now)
        if not self.options.enable_act_1:
            useful_items = [item for item in useful_items
                            if not any(act1_item["name"] == item["name"] for act1_item in act1_items)]
            included_locations -= len(act1_locations)
        if not self.options.enable_act_2:
            useful_items = [item for item in useful_items
                            if not any(act2_item["name"] == item["name"] for act2_item in act2_items)]
            included_locations -= len(act2_locations)
        if not self.options.enable_act_3:
            useful_items = [item for item in useful_items
                            if not any(act3_item["name"] == item["name"] for act3_item in act3_items)]
            included_locations -= len(act3_locations)

        for item in useful_items:
            for _ in range(item["count"]):
                new_item = self.create_item(item["name"])
                self.multiworld.itempool.append(new_item)
                nb_items_added += 1

        filler_count = included_locations
        filler_count -= nb_items_added

        trap_chance = (self.options.trap_chance / 100)
        trap_weights = self.options.trap_type_weights
        apply_trap_items = self.options.trap_chance > 0 and any(v > 0 for v in self.options.trap_type_weights.values())

        if apply_trap_items:
            trap_count = int(filler_count * trap_chance)
            filler_count = filler_count - trap_count
            trap_list = random.choices (
                population = list(trap_weights.keys()),
                weights = list(trap_weights.values()),
                k = trap_count
            )
            for i in trap_list:
                new_item = self.create_item(i)
                self.multiworld.itempool.append(new_item)

        for i in range(filler_count):
            index = i % len(filler_items)
            filler_item = filler_items[index]
            new_item = self.create_item(filler_item["name"])
            self.multiworld.itempool.append(new_item)

    def create_regions(self) -> None:
        used_regions = inscryption_regions_all

        if not self.options.enable_act_1:
            del used_regions["Act 1"]
            used_regions["Menu"].remove("Act 1")
        if not self.options.enable_act_2:
            del used_regions["Act 2"]
            used_regions["Menu"].remove("Act 2")
        if not self.options.enable_act_3:
            del used_regions["Act 3"]
            used_regions["Menu"].remove("Act 3")
        if self.options.enable_act_3:
            if not self.options.act3_overhaul:
                regions_to_locations["Act 3"].pop(38)
            if self.options.randomize_vessel_upgrades == RandomizeVesselUpgrades.option_vanilla:
                regions_to_locations["Act 3"].pop(37)
                regions_to_locations["Act 3"].pop(36)
                regions_to_locations["Act 3"].pop(35)
                regions_to_locations["Act 3"].pop(34)
            if self.options.randomize_shortcuts == RandomizeShortcuts.option_vanilla:
                regions_to_locations["Act 3"].pop(33)
                regions_to_locations["Act 3"].pop(32)
                regions_to_locations["Act 3"].pop(31)
        if self.options.enable_act_1:
            if self.options.randomize_challenges == RandomizeChallenges.option_disable:
                    regions_to_locations["Act 1"].pop(38) #consumable checks
                    regions_to_locations["Act 1"].pop(37)
                    regions_to_locations["Act 1"].pop(36)
                    regions_to_locations["Act 1"].pop(35)
                    regions_to_locations["Act 1"].pop(34)
                    regions_to_locations["Act 1"].pop(33)
                    regions_to_locations["Act 1"].pop(32) # pelts
                    regions_to_locations["Act 1"].pop(31)
                    regions_to_locations["Act 1"].pop(30)
                    regions_to_locations["Act 1"].pop(29) # new game button
                    regions_to_locations["Act 1"].pop(28) # free checks
                    regions_to_locations["Act 1"].pop(27)
                    regions_to_locations["Act 1"].pop(26)
            if not self.options.randomize_nodes and \
                self.options.randomize_challenges == RandomizeChallenges.option_disable:
                    regions_to_locations["Act 1"].pop(25)
                    regions_to_locations["Act 1"].pop(24)
                    regions_to_locations["Act 1"].pop(23)
                    regions_to_locations["Act 1"].pop(22)
                    regions_to_locations["Act 1"].pop(21)
                    regions_to_locations["Act 1"].pop(20)
                    regions_to_locations["Act 1"].pop(19)
                    regions_to_locations["Act 1"].pop(18)
                    regions_to_locations["Act 1"].pop(17)
            elif not self.options.randomize_nodes and \
                self.options.randomize_challenges != RandomizeChallenges.option_disable:
                    regions_to_locations["Act 1"].pop(38)
                    regions_to_locations["Act 1"].pop(37)
                    regions_to_locations["Act 1"].pop(36)
                    regions_to_locations["Act 1"].pop(35)
                    regions_to_locations["Act 1"].pop(34)
                    regions_to_locations["Act 1"].pop(33)
        for region_name in used_regions.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        for region_name, region_connections in used_regions.items():
            region = self.get_region(region_name)
            region.add_exits(region_connections)
            region.add_locations({
                location: self.location_name_to_id[location] for location in regions_to_locations[region_name]
            })

    def set_rules(self) -> None:
        Rules.InscryptionRules(self).set_all_rules()

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict(
            "death_link",
            "act1_death_link_behaviour",
            "enable_act_1",
            "enable_act_2",
            "enable_act_3",
            "act_unlocks",
            "goal",
            "randomize_codes",
            "randomize_deck",
            "randomize_sigils",
            "extra_sigils",
            "randomize_nodes",
            "randomize_challenges",
            "randomize_hammer",
            "act2_randomize_bridge",
            "act3_overhaul",
            "randomize_shortcuts",
            "randomize_vessel_upgrades",
            "optional_death_card",
            "skip_tutorial",
            "skip_epilogue",
            "epitaph_pieces_randomization"
        )
