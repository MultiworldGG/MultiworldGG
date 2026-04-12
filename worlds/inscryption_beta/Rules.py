from typing import Dict, Callable, TYPE_CHECKING
from BaseClasses import CollectionState, LocationProgressType
from .Options import ActUnlocks, Goal, PaintingChecksBalancing, RandomizeChallenges, Act2RandomizeBridge

if TYPE_CHECKING:
    from . import InscryptionWorld
else:
    InscryptionWorld = object


# Based on The Messenger's implementation
class InscryptionRules:
    player: int
    world: InscryptionWorld
    location_rules: Dict[str, Callable[[CollectionState], bool]]
    region_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: InscryptionWorld) -> None:
        self.player = world.player
        self.world = world
        self.location_rules = {
            "Act 1 - Wardrobe Drawer 1": self.has_wardrobe_key,
            "Act 1 - Wardrobe Drawer 2": self.has_wardrobe_key,
            "Act 1 - Wardrobe Drawer 3": self.has_wardrobe_key,
            "Act 1 - Wardrobe Drawer 4": self.has_wardrobe_key,
            "Act 1 - Dagger": self.has_caged_wolf,
            "Act 1 - Magnificus Eye": self.has_dagger,
            "Act 1 - Clock Main Compartment": self.has_magnificus_eye,
            "Act 1 - Clock Upper Compartment": self.has_trapper_requirements,
            "Act 1 - Woodlands Battle 2": self.has_later_woodlands_requirements,
            "Act 1 - Woodlands Battle 3": self.has_later_woodlands_requirements,
            "Act 1 - Boss Prospector": self.has_prospector_requirements,
            "Act 1 - Wetlands Battle 1": self.has_wetlands_requirements,
            "Act 1 - Wetlands Battle 2": self.has_wetlands_requirements,
            "Act 1 - Wetlands Battle 3": self.has_wetlands_requirements,
            "Act 1 - Boss Angler": self.has_angler_requirements,
            "Act 1 - Snow Line Battle 1": self.has_snow_line_requirements,
            "Act 1 - Snow Line Battle 2": self.has_snow_line_requirements,
            "Act 1 - Snow Line Battle 3": self.has_snow_line_requirements,
            "Act 1 - Boss Trapper": self.has_trapper_requirements,
            "Act 1 - Boss Leshy": self.has_leshy_requirements,
            "Act 1 - New Game Button": self.beat_act1_requirements,
            "Act 1 - Trader Rabbit Pelt": self.has_later_woodlands_requirements,
            "Act 1 - Trader Wolf Pelt": self.has_wolf_pelt_requirements,
            "Act 1 - Trader Golden Pelt": self.has_golden_pelt_requirements,
            "Act 1 - Woodlands Consumable Check 1": self.has_woodlands_consumable_requirements,
            "Act 1 - Woodlands Consumable Check 2": self.has_woodlands_consumable_requirements,
            "Act 1 - Wetlands Consumable Check 1": self.has_wetlands_consumable_requirements,
            "Act 1 - Wetlands Consumable Check 2": self.has_wetlands_consumable_requirements,
            "Act 1 - Snow Line Consumable Check 1": self.has_snow_line_consumable_requirements,
            "Act 1 - Snow Line Consumable Check 2": self.has_snow_line_consumable_requirements,
            "Act 2 - Battle Sawyer": self.has_act2_right_side_requirements,
            "Act 2 - Battle Royal": self.has_act2_right_side_requirements,
            "Act 2 - Battle Kaycee": self.has_act2_right_side_requirements,
            "Act 2 - Dock Chest": self.has_act2_right_side_requirements,
            "Act 2 - Forest Cabin Chest": self.has_act2_right_side_requirements,
            "Act 2 - Cabin Wardrobe Drawer": self.has_act2_right_side_requirements,
            "Act 2 - Cabin Safe": self.has_act2_right_side_requirements,
            "Act 2 - Crypt Casket 1": self.has_act2_right_side_requirements,
            "Act 2 - Crypt Casket 2": self.has_act2_right_side_requirements,
            "Act 2 - Crypt Well": self.has_act2_right_side_requirements,
            "Act 2 - Camera Replica": self.has_act2_right_side_requirements,
            "Act 2 - Clover": self.has_act2_right_side_requirements,
            "Act 2 - Epitaph Piece 1": self.has_act2_right_side_requirements,
            "Act 2 - Epitaph Piece 2": self.has_act2_right_side_requirements,
            "Act 2 - Epitaph Piece 3": self.has_act2_right_side_requirements,
            "Act 2 - Epitaph Piece 4": self.has_act2_right_side_requirements,
            "Act 2 - Epitaph Piece 5": self.has_act2_right_side_requirements,
            "Act 2 - Epitaph Piece 6": self.has_act2_right_side_requirements,
            "Act 2 - Epitaph Piece 7": self.has_act2_right_side_requirements,
            "Act 2 - Epitaph Piece 8": self.has_act2_right_side_requirements,
            "Act 2 - Epitaph Piece 9": self.has_act2_right_side_requirements,
            "Act 2 - Battle Prospector": self.has_forest_requirements,
            "Act 2 - Battle Angler": self.has_forest_requirements,
            "Act 2 - Battle Trapper": self.has_forest_requirements,
            "Act 2 - Battle Pike Mage": self.has_tower_requirements,
            "Act 2 - Battle Goobert": self.has_tower_requirements,
            "Act 2 - Battle Lonely Wizard": self.has_tower_requirements,
            "Act 2 - Battle Inspector": self.has_act2_bridge_requirements,
            "Act 2 - Battle Melter": self.has_act2_bridge_requirements,
            "Act 2 - Battle Dredger": self.has_act2_bridge_requirements,
            "Act 2 - Forest Meadow Chest": self.has_forest_requirements,
            "Act 2 - Tower Chest 1": self.has_act2_bridge_requirements,
            "Act 2 - Tower Chest 2": self.has_tower_requirements,
            "Act 2 - Tower Chest 3": self.has_tower_requirements,
            "Act 2 - Tentacle": self.has_tower_and_right_requirements,
            "Act 2 - Factory Trash Can": self.has_act2_bridge_requirements,
            "Act 2 - Factory Drawer 1": self.has_act2_bridge_requirements,
            "Act 2 - Factory Drawer 2": self.has_act2_bridge_requirements,
            "Act 2 - Factory Chest 1": self.has_act2_bridge_requirements,
            "Act 2 - Factory Chest 2": self.has_act2_bridge_requirements,
            "Act 2 - Factory Chest 3": self.has_act2_bridge_requirements,
            "Act 2 - Factory Chest 4": self.has_act2_bridge_requirements,
            "Act 2 - Monocle": self.has_act2_bridge_requirements,
            "Act 2 - Boss Grimora": self.has_grimora_requirements,
            "Act 2 - Boss Leshy": self.has_forest_requirements,
            "Act 2 - Boss Magnificus": self.has_tower_requirements,
            "Act 2 - Boss P03": self.has_act2_bridge_requirements,
            "Act 2 - Bone Lord Femur": self.has_bone_lord_stairs_requirements,
            "Act 2 - Bone Lord Horn": self.has_bone_lord_stairs_requirements,
            "Act 2 - Bone Lord Holo Key": self.has_bone_lord_stairs_requirements,
            "Act 2 - Mycologists Holo Key": self.has_tower_and_right_requirements,  # Could need money
            "Act 2 - Ancient Obol": self.has_tower_and_right_requirements,  # Need money for the pieces? Use the tower mannequin.
            "Act 3 - Boss Photographer": self.has_inspectometer_battery,
            "Act 3 - Boss Archivist": self.has_archivist_requirements,
            "Act 3 - Boss Unfinished": self.has_gaudy_gem_land_requirements,
            "Act 3 - Boss G0lly": self.has_resplendent_bastion_requirements,
            "Act 3 - Extra Battery": self.has_act3_missable_check_requirements,  # Hard to miss but soft lock still possible.
            "Act 3 - Nano Armor Generator": self.has_act3_shop_requirements,  # Costs money, so can need multiple battles.
            "Act 3 - Shop Holo Pelt": self.has_act3_shop_requirements,  # Costs money, so can need multiple battles.
            "Act 3 - Middle Holo Pelt": self.has_act3_missable_check_requirements,  # Can be reached without but possible soft lock
            "Act 3 - Forest Holo Pelt": self.has_inspectometer_battery,
            "Act 3 - Crypt Holo Pelt": self.has_filthy_corpse_world_requirements,
            "Act 3 - Tower Holo Pelt": self.has_gems_and_battery,
            "Act 3 - Trader 1": self.has_pelts(1),
            "Act 3 - Trader 2": self.has_pelts(2),
            "Act 3 - Trader 3": self.has_pelts(3),
            "Act 3 - Trader 4": self.has_pelts(4),
            "Act 3 - Trader 5": self.has_pelts(5),
            "Act 3 - Goobert's Painting": self.has_goobert_painting_requirements,
            "Act 3 - The Great Transcendence": self.has_transcendence_requirements,
            "Act 3 - Boss Mycologists": self.has_mycologists_boss_requirements,
            "Act 3 - Bone Lord Room": self.has_bone_lord_room_requirements,
            "Act 3 - Luke's File Entry 1": self.has_battery_and_quill,
            "Act 3 - Luke's File Entry 2": self.has_bridge_and_quill,
            "Act 3 - Luke's File Entry 3": self.has_bridge_and_quill,
            "Act 3 - Luke's File Entry 4": self.has_gem_land_access_and_quill,
            "Act 3 - Well": self.has_filthy_corpse_world_requirements,
            "Act 3 - Gems Drone": self.has_act3_bridge_requirements,
            "Act 3 - Clock": self.has_ourobot_requirements,  # Can be brute-forced, but the solution needs those items.
            "Act 3 - Foul Backwater Shortcut": self.has_inspectometer_battery,
            "Act 3 - Filthy Corpse World Shortcut": self.has_filthy_corpse_world_requirements,
            "Act 3 - Gaudy Gem Land Shortcut": self.has_gaudy_gem_land_requirements, 
            "Act 3 - Vessel Upgrade 1": self.has_vessel_upgrade_requirements(1),
            "Act 3 - Vessel Upgrade 2": self.has_vessel_upgrade_requirements(2),
            "Act 3 - Vessel Upgrade 3": self.has_vessel_upgrade_requirements(3),
            "Act 3 - Conduit Upgrade": self.has_resplendent_bastion_requirements,
            "Act 3 - Wizard Tower Satellite Dish": self.has_gaudy_gem_land_requirements
        }
        self.region_rules = {
            "Act 1": self.has_act1_requirements,
            "Act 2": self.has_act2_requirements,
            "Act 3": self.has_act3_requirements,
            "Epilogue": self.has_epilogue_requirements
        }

    act1_item_values: Dict[str, int] = {
        "Angler Hook": 1,
        "Oil Painting's Clover Plant": 1,
        "Dagger": 1,
        "Woodcarver Node": 2,
        "Backpack Node": 2,
        "Sacrifice Stones Node": 3,
        "Campfire Node": 3,
        "All Totem Battles Challenge": 3,
        "Bee Figurine": 3,
        "Extra Candle": 3
    }

    act1_boss_item_values: Dict[str, int] = {
        "Greater Smoke": 1,
        "Boss Totems Challenge": 3,
    }

    act1_progressive_values: Dict[str, list[int]] = {
        "More Difficult Challenge": [5, 4],
        "Progressive Candle": [3, 3],
        "Progressive Squirrel": [2, 3],
        "Tipped Scales Challenge": [5, 4, 3]
    }

    act1_area2_values: Dict[str, int] = {
        "Mycologists Node": 1,
        "Bone Altar Node": 1
    }

    def act1_battle_requirements(self, state: CollectionState, amount: int, isBoss: bool, area2: bool) -> bool:
        enough = 0
        for item, value in self.act1_item_values.items():
            if state.has(item, self.player): enough += value
        for item, values in self.act1_progressive_values.items():
            count = 1
            for value in values:
                if state.has(item, self.player, count): enough += value
                count += 1
        if isBoss:
            for item, value in self.act1_boss_item_values.items():
                if state.has(item, self.player): enough += value
        if area2:
            if state.has_all(["Sacrifice Stones", "Goobert Node"], self.player): enough += 1
            for item, value in self.act1_area2_values.items():
                if state.has(item, self.player): enough += value
        if state.has_all(["Squirrel Totem Head", "Woodcarver Node"], self.player): enough += 3
        if state.has_all(["Smaller Backpack Challenge", "Backpack Node"], self.player): enough += 1
        return enough >= amount
    
    def bypass_grizzly_requirements(self, state: CollectionState, boss_number: int) -> bool:
        if self.world.options.randomize_challenges == RandomizeChallenges.option_randomize and \
            not state.has("Progressive Grizzlies", self.player, boss_number):
            required_count = boss_number - state.count("Progressive Grizzlies", self.player)
            if required_count == 1:
                return state.has_any(["Dagger", "Angler Hook"], self.player)
            elif not self.world.options.randomize_nodes:
                return state.has("Dagger", self.player)
            elif required_count == 2:
                return state.has("Dagger", self.player) and state.has_any(["Angler Hook", "Backpack Node"], self.player)
            elif required_count == 3:
                return state.has_all(["Dagger", "Backpack Node"], self.player)
        return True

    def has_later_woodlands_requirements(self, state: CollectionState) -> bool:
        extra_points = 0
        extra_points += state.count("Progressive Candle", self.player)*3
        extra_points += state.count("Backpack Node", self.player)*2
        if self.world.options.randomize_nodes and \
            self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 3 + extra_points, True, False)
        return True

    def has_prospector_requirements(self, state: CollectionState) -> bool:
        extra_points = 0
        if state.has("All Totem Battles Challenge", self.player): extra_points += 3
        if self.world.options.randomize_challenges == RandomizeChallenges.option_randomize and \
            not state.has("Progressive Grizzlies", self.player):
                extra_points = 10
        if self.world.options.randomize_nodes and \
            self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 6 + extra_points, True, False) and \
                self.has_later_woodlands_requirements(state) and self.bypass_grizzly_requirements(state, 1)
        elif self.world.options.randomize_nodes or \
            self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 4 + extra_points, True, False) and \
                self.has_later_woodlands_requirements(state) and self.bypass_grizzly_requirements(state, 1)
        return True

    def has_wetlands_requirements(self, state: CollectionState) -> bool:
        if self.world.options.randomize_nodes and \
            self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 13, True, True) and self.has_prospector_requirements(state)
        elif self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 8, True, True) and self.has_prospector_requirements(state)
        elif self.world.options.randomize_nodes:
            return self.act1_battle_requirements(state, 5, True, False) and self.has_prospector_requirements(state)
        return True
    
    def has_angler_requirements(self, state: CollectionState) -> bool:
        extra_points = 0
        if state.has("All Totem Battles Challenge", self.player): extra_points += 3
        if self.world.options.randomize_challenges == RandomizeChallenges.option_randomize and \
            not state.has("Progressive Grizzlies", self.player, 2):
                extra_points = 10
        if self.world.options.randomize_nodes and \
            self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 18 + extra_points, True, True) and \
                self.bypass_grizzly_requirements(state, 2)
        elif self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 13 + extra_points, True, True) and \
                self.bypass_grizzly_requirements(state, 2)
        elif self.world.options.randomize_nodes:
            return self.act1_battle_requirements(state, 8, True, True)
        return True

    def has_snow_line_requirements(self, state: CollectionState) -> bool:
        if self.world.options.randomize_nodes and \
            self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 23, True, True) and self.has_angler_requirements(state)
        elif self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 17, True, True) and self.has_angler_requirements(state)
        elif self.world.options.randomize_nodes:
            return self.act1_battle_requirements(state, 8, True, True) and self.has_angler_requirements(state)
        return True

    def has_trapper_requirements(self, state: CollectionState) -> bool:
        extra_points = 0
        if state.has("All Totem Battles Challenge", self.player): extra_points += 3
        if self.world.options.randomize_challenges == RandomizeChallenges.option_randomize and \
            not state.has("Progressive Grizzlies", self.player, 3):
                extra_points += 10
        if self.world.options.randomize_nodes and \
            self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 27 + extra_points, True, True) and \
                self.bypass_grizzly_requirements(state, 3)
        elif self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 22 + extra_points, True, True) and \
                self.bypass_grizzly_requirements(state, 3)
        elif self.world.options.randomize_nodes:
            return self.act1_battle_requirements(state, 12, True, True)
        return True

    def has_leshy_requirements(self, state: CollectionState) -> bool:
        nope = 0
        if state.has("All Totem Battles Challenge", self.player): nope += 3
        if self.world.options.randomize_nodes and \
            self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 33 + nope, True, True) and self.has_trapper_requirements(state)
        elif self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
            return self.act1_battle_requirements(state, 27 + nope, True, True) and self.has_trapper_requirements(state)
        elif self.world.options.randomize_nodes:
            return self.act1_battle_requirements(state, 12 + nope, True, True) and self.has_trapper_requirements(state)
        return True

    def has_woodlands_consumable_requirements(self, state: CollectionState) -> bool:
        return (not self.world.options.randomize_nodes or state.has("Backpack Node", self.player)) and \
            self.has_later_woodlands_requirements(state)

    def has_wetlands_consumable_requirements(self, state: CollectionState) -> bool:
        return (not self.world.options.randomize_nodes or state.has("Backpack Node", self.player)) and \
            self.has_wetlands_requirements(state)

    def has_snow_line_consumable_requirements(self, state: CollectionState) -> bool:
        return (not self.world.options.randomize_nodes or state.has("Backpack Node", self.player)) and \
            self.has_snow_line_requirements(state)

    def has_wolf_pelt_requirements(self, state: CollectionState) -> bool:
        return self.has_snow_line_requirements(state) or \
            (self.has_wetlands_requirements(state) and state.has("Pricey Pelts Challenge", self.player))

    def has_golden_pelt_requirements(self, state: CollectionState) -> bool:
        return self.has_trapper_requirements(state) and state.has("Pricey Pelts Challenge", self.player)

    def has_wardrobe_key(self, state: CollectionState) -> bool:
        return state.has("Wardrobe Key", self.player)

    def has_caged_wolf(self, state: CollectionState) -> bool:
        return state.has("Caged Wolf Card", self.player)

    def has_dagger(self, state: CollectionState) -> bool:
        return state.has("Dagger", self.player)

    def has_magnificus_eye(self, state: CollectionState) -> bool:
        return state.has("Magnificus Eye", self.player)

    def has_useful_act1_items(self, state: CollectionState) -> bool:
        if self.world.options.randomize_nodes:
            return state.has_all(("Oil Painting's Clover Plant", "Squirrel Totem Head", "Woodcarver Node"), self.player)
        return state.has_all(("Oil Painting's Clover Plant", "Squirrel Totem Head"), self.player)
    
    def has_painting_2_requirements(self, state: CollectionState) -> bool:
        return state.has("Oil Painting's Clover Plant", self.player) and self.has_angler_requirements(state)
    
    def has_painting_3_requirements(self, state: CollectionState) -> bool:
        return state.has("Oil Painting's Clover Plant", self.player) and self.has_trapper_requirements(state)

    def has_all_epitaph_pieces(self, state: CollectionState) -> bool:
        return state.has(self.world.required_epitaph_pieces_name, self.player, self.world.required_epitaph_pieces_count)

    def has_camera_and_meat(self, state: CollectionState) -> bool:
        return state.has_all(("Camera Replica", "Pile Of Meat"), self.player)

    def has_monocle(self, state: CollectionState) -> bool:
        return state.has("Monocle", self.player)

    def has_obol(self, state: CollectionState) -> bool:
        return state.has("Ancient Obol", self.player)

    def has_epitaphs_and_forest_items(self, state: CollectionState) -> bool:
        return self.has_camera_and_meat(state) and self.has_all_epitaph_pieces(state)

    def has_act2_right_side_requirements(self, state: CollectionState) -> bool:
        if (self.world.options.act2_randomize_bridge == Act2RandomizeBridge.option_left_side_start):
            return state.has("Act 2 Bridge Repair", self.player)
        return True

    def has_act2_bridge_requirements(self, state: CollectionState) -> bool:
        if (self.world.options.act2_randomize_bridge == Act2RandomizeBridge.option_enable):
            return state.has("Act 2 Bridge Repair", self.player)
        elif (self.world.options.act2_randomize_bridge == Act2RandomizeBridge.option_left_side_start):
            return True
        return self.has_camera_and_meat(state) or self.has_all_epitaph_pieces(state)

    def has_forest_requirements(self, state: CollectionState) -> bool:
        return self.has_camera_and_meat(state) and self.has_act2_right_side_requirements(state)

    def has_grimora_requirements(self, state: CollectionState) -> bool:
        return self.has_all_epitaph_pieces(state) and self.has_act2_right_side_requirements(state)

    def has_bone_lord_stairs_requirements(self, state: CollectionState) -> bool:
        return self.has_obol(state) and self.has_act2_right_side_requirements(state)
    
    def has_tower_and_right_requirements(self, state: CollectionState) -> bool:
        return self.has_tower_requirements(state) and self.has_act2_right_side_requirements(state)

    def has_tower_requirements(self, state: CollectionState) -> bool:
        return self.has_monocle(state) and self.has_act2_bridge_requirements(state)

    def has_inspectometer_battery(self, state: CollectionState) -> bool:
        return state.has("Inspectometer Battery", self.player)

    def has_act3_missable_check_requirements(self, state: CollectionState) -> bool:
        if self.world.options.act3_overhaul:
            return True
        return state.has("Inspectometer Battery", self.player)

    def has_act3_bridge_requirements(self, state: CollectionState) -> bool:
        if self.world.options.act3_overhaul:
            return state.has("Act 3 Bridge Repair", self.player)
        return state.has("Inspectometer Battery", self.player)

    def has_filthy_corpse_world_requirements(self, state: CollectionState) -> bool:
        if self.world.options.act3_overhaul:
            return True
        return state.has("Inspectometer Battery", self.player)

    def has_archivist_requirements(self, state: CollectionState) -> bool:
        return self.has_filthy_corpse_world_requirements(state) and state.has("Quill", self.player)

    def has_gaudy_gem_land_requirements(self, state: CollectionState) -> bool:
        if self.world.options.act3_overhaul:
            return self.has_act3_bridge_requirements(state) and state.has("Gems Module", self.player)
        return self.has_gems_and_battery(state)

    def has_resplendent_bastion_requirements(self, state: CollectionState) -> bool:
        if self.world.options.act3_overhaul:
            return self.has_act3_bridge_requirements(state) and state.has("Respledent Bastion Gate", self.player)
        return self.has_gems_and_battery(state)

    def has_gem_land_access_and_quill(self, state: CollectionState) -> bool:
        return state.has("Quill", self.player) and self.has_gaudy_gem_land_requirements(state)

    def has_gems_and_battery(self, state: CollectionState) -> bool:
        return state.has("Gems Module", self.player) and self.has_act3_bridge_requirements(state)

    def has_bridge_and_quill(self, state: CollectionState) -> bool:
        return state.has("Quill", self.player) and self.has_act3_bridge_requirements(state)

    def has_pelts(self, count: int) -> Callable[[CollectionState], bool]:
        return lambda state: state.has("Holo Pelt", self.player, count) and \
            self.has_resplendent_bastion_requirements(state)

    def has_vessel_upgrade_requirements(self, count: int) -> Callable[[CollectionState], bool]:
        return lambda state: (int(self.has_resplendent_bastion_requirements(state)) + \
            int(self.has_inspectometer_battery(state)) + int(self.has_archivist_requirements(state)) + \
            int(self.has_gaudy_gem_land_requirements(state))) >= count

    def has_mycologists_boss_requirements(self, state: CollectionState) -> bool:
        return state.has("Mycologists Holo Key", self.player) and self.has_transcendence_requirements(state)

    def has_bone_lord_room_requirements(self, state: CollectionState) -> bool:
        return state.has("Bone Lord Holo Key", self.player) and self.has_filthy_corpse_world_requirements(state)

    def has_battery_and_quill(self, state: CollectionState) -> bool:
        return state.has("Quill", self.player) and self.has_inspectometer_battery(state)

    def has_transcendence_requirements(self, state: CollectionState) -> bool:
        return self.has_resplendent_bastion_requirements(state) and self.has_inspectometer_battery(state) and \
            self.has_archivist_requirements(state) and self.has_gaudy_gem_land_requirements(state)

    def has_goobert_painting_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_1:
            return self.has_trapper_requirements(state) and self.has_resplendent_bastion_requirements(state) and \
                self.has_inspectometer_battery(state)
        return self.has_resplendent_bastion_requirements(state) and self.has_inspectometer_battery(state)

    def has_act3_shop_requirements(self, state: CollectionState) -> bool:
        return int(self.has_resplendent_bastion_requirements(state)) + \
            int(self.has_inspectometer_battery(state)) + int(self.has_filthy_corpse_world_requirements(state)) + \
            int(self.has_gaudy_gem_land_requirements(state)) >= 3
  
    def has_ourobot_requirements(self, state: CollectionState) -> bool:
        return self.has_gaudy_gem_land_requirements(state) and self.has_act3_shop_requirements(state)

    def has_act1_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_1 and self.world.options.act_unlocks == ActUnlocks.option_items:
            return state.has("Act 1", self.player)
        return True

    def beat_act1_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_1:
            return self.has_act1_requirements(state) and state.has("Film Roll", self.player) and \
                self.has_leshy_requirements(state)
        return True

    def has_act2_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_2:
            if self.world.options.act_unlocks == ActUnlocks.option_items:
                return state.has("Act 2", self.player)
            elif self.world.options.act_unlocks == ActUnlocks.option_sequential:
                return self.beat_act1_requirements(state)
        return True
    
    def beat_act2_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_2:
            return self.has_act2_requirements(state) and self.has_all_epitaph_pieces(state) and \
                self.has_camera_and_meat(state) and self.has_monocle(state)
        return True

    def has_battery_and_quill_or_gems(self, state: CollectionState) -> bool:
        return (state.has("Quill", self.player) or state.has("Gems Module", self.player)) and \
            self.has_inspectometer_battery(state)

    def has_act3_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_3:
            if self.world.options.act_unlocks == ActUnlocks.option_items:
                return state.has("Act 3", self.player)
            elif self.world.options.act_unlocks == ActUnlocks.option_sequential:
                return self.beat_act2_requirements(state)
        return True

    def beat_act3_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_3:
            return self.has_act3_requirements(state) and self.has_transcendence_requirements(state)
        return True

    def has_epilogue_requirements(self, state: CollectionState) -> bool:
        total_acts = self.world.options.enable_act_1.__int__() + self.world.options.enable_act_2.__int__() \
                    + self.world.options.enable_act_3.__int__()
        act1 = self.world.options.enable_act_1.__bool__() and self.beat_act1_requirements(state)
        act2 = self.world.options.enable_act_2.__bool__() and self.beat_act2_requirements(state)
        act3 = self.world.options.enable_act_3.__bool__() and self.beat_act3_requirements(state)
        required_acts = self.world.options.goal.__int__() + 1
        if required_acts > total_acts: required_acts = total_acts # required acts always =< total acts

        if required_acts == 1:
            return act1 or act2 or act3
        if required_acts == 2:
            return (act1 and act2) or (act1 and act3) or (act2 and act3)
        if required_acts == 3:
            return act1 and act2 and act3
        return True

    def set_all_rules(self) -> None:
        multiworld = self.world.multiworld
        multiworld.completion_condition[self.player] = self.has_epilogue_requirements
        for region in multiworld.get_regions(self.player):
            if self.world.options.act_unlocks != ActUnlocks.option_open:
                if region.name in self.region_rules:
                    for entrance in region.entrances:
                        entrance.access_rule = self.region_rules[region.name]
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = self.location_rules[loc.name]
        if self.world.options.enable_act_1:
            if self.world.options.randomize_nodes or \
                self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
                self.world.get_location("Act 1 - Painting 1").access_rule = self.has_prospector_requirements
                self.world.get_location("Act 1 - Painting 2").access_rule = self.has_painting_2_requirements
                self.world.get_location("Act 1 - Painting 3").access_rule = self.has_painting_3_requirements
            elif self.world.options.painting_checks_balancing == PaintingChecksBalancing.option_balanced:
                self.world.get_location("Act 1 - Painting 2").access_rule = self.has_useful_act1_items
                self.world.get_location("Act 1 - Painting 3").access_rule = self.has_useful_act1_items
            if self.world.options.painting_checks_balancing == PaintingChecksBalancing.option_force_filler:
                self.world.get_location("Act 1 - Painting 2").progress_type = LocationProgressType.EXCLUDED
                self.world.get_location("Act 1 - Painting 3").progress_type = LocationProgressType.EXCLUDED
        elif self.world.options.enable_act_3:
            if self.world.options.randomize_nodes or \
                self.world.options.randomize_challenges != RandomizeChallenges.option_disable:
                self.world.get_location("Act 3 - Goobert's Painting").progress_type = LocationProgressType.EXCLUDED
