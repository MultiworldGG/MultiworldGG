from typing import Dict, Callable, NamedTuple, Optional, Tuple, TYPE_CHECKING
from BaseClasses import CollectionState, LocationProgressType
from .Options import ActUnlocks, PaintingChecksBalancing, RandomizeChallenges, Act2RandomizeBridge

if TYPE_CHECKING:
    from . import InscryptionWorld
else:
    InscryptionWorld = object

# Each Act 1 boss keeps its grizzly phase until this many Progressive Grizzlies are collected.
PROSPECTOR, ANGLER, TRAPPER = 1, 2, 3

# How far a boss's points threshold rises while it keeps its grizzly phase.
GRIZZLY_PENALTY = 10

# The four kinds of Act 1 fight. Which one a rule gates decides what its points may come from:
# a boss ignores the regular-only items and vice versa, and the woodlands ignores the later nodes.
class Act1Fight(NamedTuple):
    is_boss: bool
    is_beyond_area1: bool

WOODLANDS_BATTLE = Act1Fight(is_boss=False, is_beyond_area1=False)
WOODLANDS_BOSS = Act1Fight(is_boss=True, is_beyond_area1=False)
LATER_BATTLE = Act1Fight(is_boss=False, is_beyond_area1=True)
LATER_BOSS = Act1Fight(is_boss=True, is_beyond_area1=True)

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
            # Each file node carries ActiveIfStoryFlag(FileAccessGiven), and the only thing that
            # sets that flag is the Archivist's own file-browse sequence, so all four need it.
            "Act 3 - Luke's File Entry 1": self.has_forest_file_requirements,
            "Act 3 - Luke's File Entry 2": self.has_bridge_file_requirements,
            "Act 3 - Luke's File Entry 3": self.has_bridge_file_requirements,
            "Act 3 - Luke's File Entry 4": self.has_tower_file_requirements,
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

    @property
    def nodes_randomized(self) -> bool:
        return bool(self.world.options.randomize_nodes)

    @property
    def challenges_randomized(self) -> bool:
        return self.world.options.randomize_challenges != RandomizeChallenges.option_disable

    # Grizzlies are only in the pool on the full "randomize" setting, not on "no grizzlies".
    @property
    def grizzlies_randomized(self) -> bool:
        return self.world.options.randomize_challenges == RandomizeChallenges.option_randomize

    @property
    def act1_randomized(self) -> bool:
        return self.nodes_randomized or self.challenges_randomized

    @property
    def act2_bridge_randomized(self) -> bool:
        return self.world.options.act2_randomize_bridge == Act2RandomizeBridge.option_enable

    @property
    def act2_starts_on_left_side(self) -> bool:
        return self.world.options.act2_randomize_bridge == Act2RandomizeBridge.option_left_side_start

    @property
    def act3_overhauled(self) -> bool:
        return bool(self.world.options.act3_overhaul)

    @property
    def acts_unlocked_by_items(self) -> bool:
        return self.world.options.act_unlocks == ActUnlocks.option_items

    @property
    def acts_unlocked_sequentially(self) -> bool:
        return self.world.options.act_unlocks == ActUnlocks.option_sequential

    act1_item_values: Dict[str, int] = {
        "Angler Hook": 1,
        "Oil Painting's Clover Plant": 1,
        "Dagger": 1,
        "Woodcarver Node": 2,
        "Backpack Node": 2,
        "Sacrifice Stones Node": 3,
        "Campfire Node": 3,
        "Bee Figurine": 3,
        "Extra Candle": 3
    }

    act1_boss_item_values: Dict[str, int] = {
        "Greater Smoke": 1,
        "Boss Totems Challenge": 3,
    }

    # Only ever counted for a regular battle. All Totem Battles turns regular map nodes into
    # totem battles; Boss Totems, above, is the challenge that puts a totem on a boss.
    act1_regular_item_values: Dict[str, int] = {
        "All Totem Battles Challenge": 3
    }

    act1_progressive_values: Dict[str, list[int]] = {
        "More Difficult Challenge": [5, 4],
        "Progressive Candle": [3, 3],
        "Progressive Squirrel": [2, 3],
        "Tipped Scales Challenge": [5, 4, 3]
    }

    act1_beyond_area1_values: Dict[str, int] = {
        "Mycologists Node": 1,
        "Bone Altar Node": 1
    }

    # Pairs that pay only when both halves are held. The second table is worth nothing before the
    # wetlands, where the base game has not started spawning those nodes.
    act1_pair_values: Dict[Tuple[str, str], int] = {
        ("Squirrel Totem Head", "Woodcarver Node"): 3,
        ("Smaller Backpack Challenge", "Backpack Node"): 1
    }

    act1_beyond_area1_pair_values: Dict[Tuple[str, str], int] = {
        ("Sacrifice Stones Node", "Goobert Node"): 1
    }

    # What the player's items are worth to this fight. A boss ignores the regular-only items and
    # a regular battle ignores the boss-only ones; the woodlands ignores what does not spawn yet.
    def act1_battle_points(self, state: CollectionState, fight: Act1Fight) -> int:
        def counts(item: str, needed: int = 1) -> bool:
            return state.has(item, self.player, needed)

        points = 0

        for item, value in self.act1_item_values.items():
            if counts(item): points += value

        for item, values in self.act1_progressive_values.items():
            for copy, value in enumerate(values, start=1):
                if counts(item, copy): points += value

        for item, value in (self.act1_boss_item_values if fight.is_boss
                            else self.act1_regular_item_values).items():
            if counts(item): points += value

        for pair, value in self.act1_pair_values.items():
            if all(counts(item) for item in pair): points += value

        if fight.is_beyond_area1:
            # The base game only spawns these nodes from the wetlands on, so they can only have
            # helped a battle in the wetlands or later.
            for item, value in self.act1_beyond_area1_values.items():
                if counts(item): points += value

            for pair, value in self.act1_beyond_area1_pair_values.items():
                if all(counts(item) for item in pair): points += value

        return points

    # Thresholds are tuned per option combination. None means neither option is on, so Act 1
    # runs at vanilla difficulty and its battles are free.
    def act1_points_needed(self, both: int, challenges_only: int, nodes_only: int) -> Optional[int]:
        if self.nodes_randomized and self.challenges_randomized:
            return both
        if self.challenges_randomized:
            return challenges_only
        if self.nodes_randomized:
            return nodes_only
        return None

    # How much extra help a boss needs while it still has its grizzly phase.
    def act1_grizzly_penalty(self, state: CollectionState, boss: int) -> int:
        if self.grizzlies_randomized and not state.has("Progressive Grizzlies", self.player, boss):
            return GRIZZLY_PENALTY
        return 0

    # A concrete answer to a boss that still has its grizzly phase. Only bites when nodes are
    # randomized: with them off the backpack node is always there and its consumables suffice.
    def bypass_grizzly_requirements(self, state: CollectionState, boss: int) -> bool:
        if not self.grizzlies_randomized or not self.nodes_randomized:
            return True
        grizzlies_short = boss - state.count("Progressive Grizzlies", self.player)
        if grizzlies_short <= 0:
            return True
        # One short is close enough to the tuned fight that the dagger's death card plus the
        # hook can carry it. Any further short, only the backpack's consumables will do.
        if grizzlies_short == 1:
            return state.has("Backpack Node", self.player) or \
                state.has_all(["Dagger", "Angler Hook"], self.player)
        return state.has("Backpack Node", self.player)

    def has_later_woodlands_requirements(self, state: CollectionState) -> bool:
        if not (self.nodes_randomized and self.challenges_randomized):
            return True
        return self.act1_battle_points(state, WOODLANDS_BATTLE) >= 3

    def has_prospector_requirements(self, state: CollectionState) -> bool:
        base = self.act1_points_needed(both=6, challenges_only=4, nodes_only=4)
        if base is None:
            return True
        needed = base + self.act1_grizzly_penalty(state, PROSPECTOR)
        return self.act1_battle_points(state, WOODLANDS_BOSS) >= needed and \
            self.has_later_woodlands_requirements(state) and \
            self.bypass_grizzly_requirements(state, PROSPECTOR)

    def has_wetlands_requirements(self, state: CollectionState) -> bool:
        base = self.act1_points_needed(both=13, challenges_only=8, nodes_only=5)
        if base is None:
            return True
        return self.act1_battle_points(state, LATER_BATTLE) >= base and \
            self.has_prospector_requirements(state)

    def has_angler_requirements(self, state: CollectionState) -> bool:
        base = self.act1_points_needed(both=18, challenges_only=13, nodes_only=8)
        if base is None:
            return True
        needed = base + self.act1_grizzly_penalty(state, ANGLER)
        return self.act1_battle_points(state, LATER_BOSS) >= needed and \
            self.bypass_grizzly_requirements(state, ANGLER)

    def has_snow_line_requirements(self, state: CollectionState) -> bool:
        base = self.act1_points_needed(both=23, challenges_only=17, nodes_only=8)
        if base is None:
            return True
        return self.act1_battle_points(state, LATER_BATTLE) >= base and \
            self.has_angler_requirements(state)

    def has_trapper_requirements(self, state: CollectionState) -> bool:
        base = self.act1_points_needed(both=27, challenges_only=22, nodes_only=12)
        if base is None:
            return True
        needed = base + self.act1_grizzly_penalty(state, TRAPPER)
        return self.act1_battle_points(state, LATER_BOSS) >= needed and \
            self.bypass_grizzly_requirements(state, TRAPPER)

    def has_leshy_requirements(self, state: CollectionState) -> bool:
        base = self.act1_points_needed(both=33, challenges_only=27, nodes_only=12)
        if base is None:
            return True
        return self.act1_battle_points(state, LATER_BOSS) >= base and \
            self.has_trapper_requirements(state)

    # Consumable checks are the items a run picks up off the map, which only exist while the
    # backpack node does.
    def has_backpack_consumables(self, state: CollectionState) -> bool:
        return not self.nodes_randomized or state.has("Backpack Node", self.player)

    def has_woodlands_consumable_requirements(self, state: CollectionState) -> bool:
        return self.has_backpack_consumables(state) and self.has_later_woodlands_requirements(state)

    def has_wetlands_consumable_requirements(self, state: CollectionState) -> bool:
        return self.has_backpack_consumables(state) and self.has_wetlands_requirements(state)

    def has_snow_line_consumable_requirements(self, state: CollectionState) -> bool:
        return self.has_backpack_consumables(state) and self.has_snow_line_requirements(state)

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
        if self.nodes_randomized:
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
        if self.act2_starts_on_left_side:
            return state.has("Act 2 Bridge Repair", self.player)
        return True

    def has_act2_bridge_requirements(self, state: CollectionState) -> bool:
        if self.act2_bridge_randomized:
            return state.has("Act 2 Bridge Repair", self.player)
        if self.act2_starts_on_left_side:
            return True
        # Vanilla: the bridge opens once either the forest or the crypt route is finished.
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

    # Without the overhaul the battery is the one key to the whole map, so most Act 3 rules
    # collapse to owning it.
    def has_act3_missable_check_requirements(self, state: CollectionState) -> bool:
        if self.act3_overhauled:
            return True
        return self.has_inspectometer_battery(state)

    def has_act3_bridge_requirements(self, state: CollectionState) -> bool:
        if self.act3_overhauled:
            return state.has("Act 3 Bridge Repair", self.player)
        return self.has_inspectometer_battery(state)

    def has_filthy_corpse_world_requirements(self, state: CollectionState) -> bool:
        if self.act3_overhauled:
            return True
        return self.has_inspectometer_battery(state)

    def has_archivist_requirements(self, state: CollectionState) -> bool:
        return self.has_filthy_corpse_world_requirements(state) and state.has("Quill", self.player)

    # The file rooms themselves are ungated, but their node stays inactive until the Archivist has
    # asked to browse a file, so reaching the Archivist is a requirement on top of the area's own.
    # One per area rather than one factory: the three areas are three rules, and the tracker's
    # sync check reads these by name to confirm the pack splits the four entries the same way.
    def has_forest_file_requirements(self, state: CollectionState) -> bool:
        return self.has_inspectometer_battery(state) and self.has_archivist_requirements(state)

    def has_bridge_file_requirements(self, state: CollectionState) -> bool:
        return self.has_act3_bridge_requirements(state) and self.has_archivist_requirements(state)

    def has_tower_file_requirements(self, state: CollectionState) -> bool:
        return self.has_gaudy_gem_land_requirements(state) and self.has_archivist_requirements(state)

    def has_gaudy_gem_land_requirements(self, state: CollectionState) -> bool:
        if self.act3_overhauled:
            return self.has_act3_bridge_requirements(state) and state.has("Gems Module", self.player)
        return self.has_gems_and_battery(state)

    def has_resplendent_bastion_requirements(self, state: CollectionState) -> bool:
        if self.act3_overhauled:
            return self.has_act3_bridge_requirements(state) and state.has("Resplendent Bastion Gate", self.player)
        return self.has_gems_and_battery(state)

    def has_gems_and_battery(self, state: CollectionState) -> bool:
        return state.has("Gems Module", self.player) and self.has_act3_bridge_requirements(state)

    def has_pelts(self, count: int) -> Callable[[CollectionState], bool]:
        return lambda state: state.has("Holo Pelt", self.player, count) and \
            self.has_resplendent_bastion_requirements(state)

    # Some Act 3 checks are spread over the map or cost money to buy, so they are gated on how
    # much of Botopia is open rather than on one specific area.
    def count_act3_areas_open(self, state: CollectionState,
                              *areas: Callable[[CollectionState], bool]) -> int:
        return sum(area(state) for area in areas)

    def has_vessel_upgrade_requirements(self, count: int) -> Callable[[CollectionState], bool]:
        return lambda state: self.count_act3_areas_open(
            state,
            self.has_resplendent_bastion_requirements,
            self.has_inspectometer_battery,
            self.has_archivist_requirements,
            self.has_gaudy_gem_land_requirements
        ) >= count

    # Available as soon as the hut can be opened and eastern Botopia reached, not at the end of the
    # act. Mirrors the Bone Lord room, the other key-gated room on that side.
    def has_mycologists_boss_requirements(self, state: CollectionState) -> bool:
        return state.has("Mycologists Holo Key", self.player) and \
            self.has_filthy_corpse_world_requirements(state)

    def has_bone_lord_room_requirements(self, state: CollectionState) -> bool:
        return state.has("Bone Lord Holo Key", self.player) and self.has_filthy_corpse_world_requirements(state)

    def has_transcendence_requirements(self, state: CollectionState) -> bool:
        return self.has_resplendent_bastion_requirements(state) and self.has_inspectometer_battery(state) and \
            self.has_archivist_requirements(state) and self.has_gaudy_gem_land_requirements(state)

    def has_goobert_painting_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_1 and not self.has_trapper_requirements(state):
            return False
        return self.has_resplendent_bastion_requirements(state) and self.has_inspectometer_battery(state)

    def has_act3_shop_requirements(self, state: CollectionState) -> bool:
        return self.count_act3_areas_open(
            state,
            self.has_resplendent_bastion_requirements,
            self.has_inspectometer_battery,
            self.has_filthy_corpse_world_requirements,
            self.has_gaudy_gem_land_requirements
        ) >= 3


    def has_ourobot_requirements(self, state: CollectionState) -> bool:
        return self.has_gaudy_gem_land_requirements(state) and self.has_act3_shop_requirements(state)

    def has_act1_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_1 and self.acts_unlocked_by_items:
            return state.has("Act 1", self.player)
        return True

    def beat_act1_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_1:
            return self.has_act1_requirements(state) and state.has("Film Roll", self.player) and \
                self.has_leshy_requirements(state)
        return True

    def has_act2_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_2:
            if self.acts_unlocked_by_items:
                return state.has("Act 2", self.player)
            if self.acts_unlocked_sequentially:
                return self.beat_act1_requirements(state)
        return True
    
    # Beating the act means beating all four Scrybes, so it inherits each boss's own rule rather
    # than restating the items. That is what carries the bridge, whichever side the run starts on.
    def beat_act2_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_2:
            return self.has_act2_requirements(state) and self.has_forest_requirements(state) and \
                self.has_grimora_requirements(state) and self.has_tower_requirements(state) and \
                self.has_act2_bridge_requirements(state)
        return True

    def has_battery_and_quill_or_gems(self, state: CollectionState) -> bool:
        return (state.has("Quill", self.player) or state.has("Gems Module", self.player)) and \
            self.has_inspectometer_battery(state)

    def has_act3_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_3:
            if self.acts_unlocked_by_items:
                return state.has("Act 3", self.player)
            if self.acts_unlocked_sequentially:
                return self.beat_act2_requirements(state)
        return True

    def beat_act3_requirements(self, state: CollectionState) -> bool:
        if self.world.options.enable_act_3:
            return self.has_act3_requirements(state) and self.has_transcendence_requirements(state)
        return True

    def has_epilogue_requirements(self, state: CollectionState) -> bool:
        enabled_acts = [self.world.options.enable_act_1, self.world.options.enable_act_2,
                        self.world.options.enable_act_3]
        beat_rules = [self.beat_act1_requirements, self.beat_act2_requirements, self.beat_act3_requirements]
        acts_beaten = sum(bool(enabled) and beat_rule(state)
                          for enabled, beat_rule in zip(enabled_acts, beat_rules))
        # The goal is a zero-based count of acts to beat, capped at how many are enabled.
        required_acts = min(int(self.world.options.goal) + 1, sum(bool(act) for act in enabled_acts))
        return acts_beaten >= required_acts

    # The mod hands over an act's remaining checks the moment it is beaten, so every check is
    # reachable its normal way or once its act can be finished. Applied last, over the overrides.
    def apply_act_release_rules(self) -> None:
        beat_rules = {
            "Act 1": self.beat_act1_requirements,
            "Act 2": self.beat_act2_requirements,
            "Act 3": self.beat_act3_requirements
        }

        for loc in self.world.multiworld.get_locations(self.player):
            beat_rule = beat_rules.get(loc.name.split(" - ")[0])
            if beat_rule is None:
                continue

            normal_rule = loc.access_rule
            loc.access_rule = lambda state, n=normal_rule, b=beat_rule: n(state) or b(state)

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
            if self.act1_randomized:
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
            if self.act1_randomized:
                self.world.get_location("Act 3 - Goobert's Painting").progress_type = LocationProgressType.EXCLUDED

        if self.world.options.release_on_act_completion:
            self.apply_act_release_rules()
