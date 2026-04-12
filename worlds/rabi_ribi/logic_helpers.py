"""
This module defines helper methods used for evaluating rule lambdas.
Its probably a little haphazardly sorted.. but the method names are descriptive
enough for it not to be confusing.
"""
from BaseClasses import CollectionState
from typing import Callable, List, Set, Tuple

from .existing_randomizer.utility import OpBacktrack, OpLit, OpNot, OpOr, OpAnd
from .items import recruit_table, recruit_table_irisu
from .names import ItemName, LocationName
from .options import RabiRibiOptions, TrickDifficulty, Knowledge
from .utility import convert_existing_rando_name_to_ap_name

def has_3_magic_types(state: CollectionState, player: int, options):
    """Player has at least 3 types of magic"""
    # If playing with more than 5 Easter Eggs, Rainbow Shot could be used as a magic type
    rainbow_shot = 1 if rainbow_shot_in_logic(state, player, options) else 0
    return state.count_group_unique("Magic", player) + rainbow_shot + 1 >= 3

def has_item_menu(state: CollectionState, player: int, options):
    """Player has access to the item menu"""
    return state.has("Chapter 1", player) or \
        (
            is_at_least_advanced_knowledge(state, player, options) and
            has_3_magic_types(state, player, options)
        )

def can_use_boost(state: CollectionState, player: int, options):
    """Player can use the boost skill at least once"""
    return state.has("Boost Unlock", player) or \
        (
            (state.has("Shop Access", player) or state.has(ItemName.rumi_donut, player)) and \
            has_item_menu(state, player, options)
        )

def can_use_boost_many(state: CollectionState, player: int, options):
    """Player can use the boost skill multiple times"""
    return state.has("Shop Access", player) and has_item_menu(state, player, options)

def can_use_boost_boring(state: CollectionState, player: int, options):
    """Player can use the boost skill or farm boost meter"""
    return (state.has("Boost Unlock", player) and options.boring_tricks_required.value) or \
        (
            (state.has("Shop Access", player) or state.has(ItemName.rumi_donut, player)) and \
            has_item_menu(state, player, options)
        )

def carrot_shooter_in_logic(state: CollectionState, player: int, options):
    """Player has Carrot Shooter and it's not out of logic by options"""
    return (options.carrot_shooter_in_logic.value or state.has(ItemName.glitched_logic, player)) and \
        state.has(ItemName.carrot_shooter, player)

def rainbow_shot_in_logic(state: CollectionState, player: int, options):
    """Player has Rainbow Shot and it's not out of logic by options"""
    return (options.rainbow_shot_in_logic.value or state.has(ItemName.glitched_logic, player)) and \
        state.has(ItemName.easter_egg, player, count = 5)

def can_navigate_darkness_without_light_orb(state: CollectionState, player: int, options):
    """
    Player has darkness without light orb turned on.
    """
    return options.darkness_without_light_orb.value or \
        state.has(ItemName.glitched_logic, player)

def can_navigate_darkness(state: CollectionState, player: int, options):
    """
    Player has light orb or has option for darkness without light orb turned on
    """
    return state.has(ItemName.light_orb, player) or \
        can_navigate_darkness_without_light_orb(state, player, options)

def can_navigate_underwater_without_water_orb(state: CollectionState, player: int, options):
    """Player has option for water without water orb turned on"""
    return state.has(ItemName.water_orb, player) or \
        options.underwater_without_water_orb.value or \
        state.has(ItemName.glitched_logic, player)

def can_navigate_underwater(state: CollectionState, player: int, options):
    """Player has water orb or has option for water without water orb turned on"""
    return state.has(ItemName.water_orb, player) or \
        can_navigate_underwater_without_water_orb(state, player, options)

def can_bunny_strike(state: CollectionState, player: int):
    """Player can use the bunny strike skill"""
    return state.has(ItemName.sliding_powder, player) and \
        state.has(ItemName.bunny_strike, player) and \
        state.has(ItemName.piko_hammer, player)

def can_bunny_whirl(state: CollectionState, player: int):
    """Player can use the bunny whirl skill"""
    return state.has(ItemName.bunny_whirl, player) and \
        state.has(ItemName.piko_hammer, player)

def can_air_dash(state: CollectionState, player: int):
    """Player can use air dash skill"""
    return state.has(ItemName.air_dash, player) and \
        state.has(ItemName.piko_hammer, player)

def can_air_dash_3(state: CollectionState, player: int):
    """Player can use the upgraded air dash skill"""
    return can_air_dash(state, player) and \
        state.has("Shop Access", player)

def wall_jump_2(state: CollectionState, player: int):
    """Player can use the upgraded wall jump skill"""
    return state.has(ItemName.wall_jump, player) and \
        state.has("Shop Access", player)

def can_hammer_roll(state: CollectionState, player: int):
    """Player can use the hammer roll skill"""
    return state.has(ItemName.hammer_roll, player) and \
        state.has(ItemName.bunny_whirl, player) and \
        state.has(ItemName.piko_hammer, player)

def can_hammer_roll_3(state: CollectionState, player: int):
    """Player can use the upgraded hammer roll skill"""
    return can_hammer_roll(state, player) and \
        state.has("Shop Access", player) and \
        state.has("Chapter 3", player)

def can_get_speed_boost_3(state: CollectionState, player: int):
    """Player can use the upgraded speed boost skill"""
    return state.has(ItemName.speed_boost, player) and \
        state.has("Shop Access", player)

def can_charge_carrot_shooter_entry(state: CollectionState, player: int, options):
    """Player can open entrances with a fully charged carrot shooter shot"""
    return carrot_shooter_in_logic(state, player, options) and \
        state.has(ItemName.charge_ring, player)

def can_bunny_amulet(state: CollectionState, player: int):
    """Player can use the bunny amulet skill"""
    return state.has(ItemName.bunny_amulet, player) or state.has("Chapter 2", player)

def can_bunny_amulet_2(state: CollectionState, player: int):
    """Player can use 2 bunny amulet skills"""
    return state.has("Chapter 3", player) or \
        (
            can_bunny_amulet(state, player) and \
            state.has("Shop Access", player)
        )

def can_bunny_amulet_3(state: CollectionState, player: int):
    """Player can use 3 bunny amulet skills"""
    return state.has("Chapter 4", player) or \
        (
            can_bunny_amulet(state, player) and \
            state.has("Shop Access", player)
        )

def can_bunny_amulet_4(state: CollectionState, player: int, options):
    """Player can use 4 bunny amulet skills"""
    return options.include_post_game.value and \
        can_bunny_amulet(state, player) and \
        state.has(ItemName.rumi_recruit, player)

def can_recruit_cocoa(state: CollectionState, player: int):
    """Player can recruit Cocoa"""
    return state.has(ItemName.cocoa_1, player) and \
        state.has(ItemName.kotri_1, player) and \
        state.can_reach_region(LocationName.cave_cocoa, player)

def can_recruit_ashuri(state: CollectionState, player: int):
    """Player can recruit Ashuri"""
    return state.has("Chapter 1", player) and \
        state.has(ItemName.ashuri_2, player)

def can_recruit_saya(state: CollectionState, player: int):
    """Player can recruit Saya"""
    return state.can_reach_region(LocationName.evernight_saya, player)

def can_recruit_nieve_and_nixie(state: CollectionState, player: int):
    """Player can recruit Nieve and Nixie"""
    return state.can_reach_region(LocationName.palace_level_5, player) and \
        state.can_reach_region(LocationName.icy_summit_nixie, player)

def can_recruit_seana(state: CollectionState, player: int):
    """Player can recruit Seana"""
    return state.has(ItemName.seana_1, player) and \
        state.has(ItemName.vanilla_recruit, player) and \
        state.has(ItemName.chocolate_recruit, player) and \
        state.has(ItemName.cicini_recruit, player) and \
        state.has(ItemName.syaro_recruit, player) and \
        state.has(ItemName.nieve_recruit, player) and \
        state.has(ItemName.nixie_recruit, player)

def can_recruit_lilith(state: CollectionState, player: int):
    """Player can recruit Lilith"""
    return state.has(ItemName.cicini_recruit, player)

def can_recruit_chocolate(state: CollectionState, player: int):
    """Player can recruit Chocolate"""
    return state.has("Chapter 1", player)

def can_recruit_kotri(state: CollectionState, player: int):
    """Player can recruit Kotri"""
    return state.has(ItemName.kotri_2, player)

def can_recruit_keke_bunny(state: CollectionState, player: int):
    """Player can recruit Keke Bunny"""
    return state.can_reach_region(LocationName.town_main, player)

def can_recruit_irisu(state: CollectionState, player: int):
    """Player can recruit Irisu"""
    return state.can_reach_region(LocationName.warp_destination_hospital, player) and \
        state.has("Chapter 5", player) and \
        state.has_from_list_unique(recruit_table_irisu, player, 15) and \
        state.has(ItemName.miriam_recruit, player) and \
        state.has(ItemName.rumi_recruit, player)

def can_recruit_n_town_members(state: CollectionState, num_town_members: int, player: int):
    """
    Player can recruit a set number of town members
    
    :int num_town_members: the number of town members to satisfy the condition
    """
    return state.has_from_list_unique(recruit_table, player, num_town_members)

def can_be_speedy(state: CollectionState, player: int, options):
    """Player can buy the speedy buff"""
    return is_at_least_intermediate_knowledge(state, player, options) and \
        state.has(ItemName.cicini_recruit, player) and \
        state.has("Chapter 1", player) and \
        can_recruit_n_town_members(state, 3, player)

def can_use_speed_1(state: CollectionState, player: int, options):
    """Player can get level 1 speed"""
    return can_be_speedy(state, player, options) or \
        state.has(ItemName.speed_boost, player)

def can_use_speed_2(state: CollectionState, player: int, options):
    """Player can get level 2 speed"""
    return can_get_speed_boost_3(state, player) or \
        can_be_speedy(state, player, options)

def can_use_speed_3(state: CollectionState, player: int, options):
    """Player can get level 3 speed"""
    return can_get_speed_boost_3(state, player) or \
        (
            state.has(ItemName.speed_boost, player) and \
            can_be_speedy(state, player, options)
        )

def can_use_speed_5(state: CollectionState, player: int, options):
    """
    Player can get level 5 speed.
    Level 4 is skipped, as you can always buy both speed boost upgrades
    and speedy gives the equivalent of 2 levels of movement speed.
    """
    return can_be_speedy(state, player, options) and \
        can_get_speed_boost_3(state, player)

def can_reach_chapter_2(state: CollectionState, player: int):
    """Player can reach chapter 2"""
    return state.has("Chapter 1", player) and \
        can_recruit_n_town_members(state, 2, player)

def can_reach_chapter_3(state: CollectionState, player: int):
    """Player can reach chapter 3"""
    return state.has("Chapter 2", player) and \
        can_recruit_n_town_members(state, 4, player)

def can_reach_chapter_4(state: CollectionState, player: int):
    """Player can reach chapter 4"""
    return state.has("Chapter 3", player) and \
        can_recruit_n_town_members(state, 7, player)

def can_reach_chapter_5(state: CollectionState, player: int):
    """Player can reach chapter 5"""
    return state.has("Chapter 4", player) and \
        can_recruit_n_town_members(state, 10, player)

def can_reach_chapter_6(state: CollectionState, player: int):
    """Player can reach chapter 6"""
    return state.has("Chapter 5", player)

def can_reach_chapter_7(state: CollectionState, player: int):
    """Player can reach chapter 7"""
    return state.has("Chapter 6", player) and \
        state.has(ItemName.rumi_recruit, player)

def can_move_out_of_prologue_areas(state: CollectionState, player: int, options):
    """Player can reach areas not locked to prologue"""
    return state.has("Chapter 1", player) or (options.open_mode.value)

def can_reach_ribbon(state: CollectionState, player: int):
    """Player can reach Ribbon"""
    return state.can_reach_region(LocationName.spectral_warp, player)

def can_reach_keke_bunny(state: CollectionState, player: int):
    """Player can reach Keke Bunny"""
    return state.can_reach_region(LocationName.plurkwood_main, player)

def can_use_consumables(state: CollectionState, player: int, options):
    """Player can use consumable items"""
    return has_item_menu(state, player, options) and \
        (
            state.has_group_unique("Consumables", player) or
            can_purchase_food(state, player) or
            can_purchase_cocoa_bomb(state, player)
        )

def can_purchase_food(state: CollectionState, player: int):
    """Player can purchase food"""
    return state.has("Shop Access", player)

def can_purchase_cocoa_bomb(state: CollectionState, player: int):
    """Player can purchase food"""
    return state.has("Chapter 1", player) and \
        state.has(ItemName.cocoa_recruit, player) and \
        can_recruit_n_town_members(state, 3, player)

def is_at_least_hard_difficulty(state: CollectionState, player: int, options):
    """Trick difficulty is at least hard"""
    return (options.trick_difficulty >= TrickDifficulty.option_hard) or state.has(ItemName.glitched_logic, player)

def is_at_least_v_hard_difficulty(state: CollectionState, player: int, options):
    """Trick difficulty is at least very hard"""
    return (options.trick_difficulty >= TrickDifficulty.option_v_hard) or state.has(ItemName.glitched_logic, player)

def is_at_least_extreme_difficulty(state: CollectionState, player: int, options):
    """Trick difficulty is at least extreme"""
    return (options.trick_difficulty >= TrickDifficulty.option_extreme) or state.has(ItemName.glitched_logic, player)

def is_at_least_stupid_difficulty(state: CollectionState, player: int, options):
    """Trick difficulty is at least stupid"""
    return (options.trick_difficulty >= TrickDifficulty.option_stupid) or state.has(ItemName.glitched_logic, player)

def is_at_least_intermediate_knowledge(state: CollectionState, player: int, options):
    """Knowledge is at least intermediate"""
    return (options.knowledge >= Knowledge.option_intermediate) or state.has(ItemName.glitched_logic, player)

def is_at_least_advanced_knowledge(state: CollectionState, player: int, options):
    """Knowledge is at least advanced"""
    return (options.knowledge >= Knowledge.option_advanced) or state.has(ItemName.glitched_logic, player)

def is_at_least_obscure_knowledge(state: CollectionState, player: int, options):
    """Knowledge is at least obscure"""
    return (options.knowledge >= Knowledge.option_obscure) or state.has(ItemName.glitched_logic, player)

def can_block_clip(state: CollectionState, player: int, options):
    """Player can perform block clips."""
    return (options.block_clips_required.value) or state.has(ItemName.glitched_logic, player)

def can_semi_solid_clip(state: CollectionState, player: int, options):
    """Player can perform semisolid clips."""
    return (options.semi_solid_clips_required.value) or state.has(ItemName.glitched_logic, player)

def can_zip(state: CollectionState, player: int, options):
    """Player can perform zips."""
    return (options.zips_required.value) or state.has(ItemName.glitched_logic, player)

def can_bunstrike_zip(state: CollectionState, player: int, options):
    """Player can perform bunstrike zips."""
    return (options.bunstrike_zips_required.value) or state.has(ItemName.glitched_logic, player)

def can_do_boring_tricks(state: CollectionState, player: int, options):
    """Player can perform boring tricks."""
    return (options.boring_tricks_required.value) or state.has(ItemName.glitched_logic, player)

def can_use_event_warps(state: CollectionState, player: int, options):
    """Player can use event warps."""
    return (options.event_warps_in_logic.value) or state.has(ItemName.glitched_logic, player)

def can_enter_plurkwood(state: CollectionState, player: int, options):
    """Player can enter plurkwood."""
    return (options.include_plurkwood.value) or state.has(ItemName.glitched_logic, player)

def count_normal_consumable_items(state: CollectionState, player: int):
    """Counts which normal consumable items the player can reach, either from locations or purchases."""
    consumables = 0
    if state.has(ItemName.rumi_cake, player) or can_purchase_food(state, player):
        consumables += 1
    if state.has(ItemName.cocoa_bomb, player) or can_purchase_cocoa_bomb(state, player):
        consumables += 1
    if state.has(ItemName.gold_carrot, player):
        consumables += 1
    return consumables

def has_enough_amulet_food(state: CollectionState, player: int, options, num_amulet_food: int):
    """Player can utilize enough items to perform a trick"""
    amulet = 0
    food = 0

    if can_bunny_amulet_4(state, player, options):
        amulet = 4
    elif can_bunny_amulet_3(state, player):
        amulet = 3
    elif can_bunny_amulet_2(state, player):
        amulet = 2
    elif can_bunny_amulet(state, player):
        amulet = 1
    
    if has_item_menu(state, player, options):
        if state.has(ItemName.rumi_donut, player) or can_purchase_food(state, player):
            food = 1
            # Eating a Rumi Donut gives an amulet charge
            if can_bunny_amulet(state, player):
                amulet += 1
            food += count_normal_consumable_items(state, player)
            if amulet >= 4 and state.has(ItemName.kotri_recruit, player) and \
                can_recruit_n_town_members(state, 3, player):
                amulet += 1
    return (amulet + food) >= num_amulet_food

def has_many_amulet_food(state: CollectionState, player: int, options):
    """Player has access to many consumables due to being able to reach the town shop"""
    return has_item_menu(state, player, options) and \
        state.has("Shop Access", player) and \
        can_bunny_amulet(state, player)

####################################################
#           Utility used by other modules
####################################################

def convert_existing_rando_rule_to_ap_rule(existing_rule: object, player: int, regions: Set[str], options: RabiRibiOptions) -> Tuple[Callable[[CollectionState], bool], List[str]]:
    """
    This method converts a rule from the existing randomizer to a lambda which can be passed to AP.
    The existing randomizer evaluates a defined logic expression, which it seperates into 5 classes:
        - OpLit
        - OpAnd
        - OpOr
        - OpNot
        - OpBacktrack

    OpBacktrack exists in the standalone randomizer for two-way entrances that can only be opened
    from one side. Since AP logic assumes the player can warp to the starting location,
    these entrances add nothing to the graph and can be safely ignored.

    OpLit is used to evaluate a single literal statement. This can be having an item, or
    can be more complex (e.g. conjunction of literals), which is combined into a single literal
    in the existing randomizer. For the more complicated literals, Ive defined methods above to
    translate them, and placed them in the below "literal_eval_map". If its not in the below map,
    assume the literal is an item which we can check the state for.

    The other Ops are self explanatory, and are translated accordingly.

    :obj existing_rule: The existing rule as an OpX object.
    :player int: the relevant player

    :returns: An evaluatable labmda with one argument (for state)

    :raises ValueError: the passed in existing_rule is not a valid OpX object.
    """
    if isinstance(existing_rule, OpLit):
        literal = convert_existing_rando_name_to_ap_name(existing_rule.name)
        literal_eval_map = {
            "True": lambda _: True,
            "None": lambda _: True,
            "False": lambda _: False,
            "Impossible": lambda _: False,
            "Carrot Shooter": lambda state: carrot_shooter_in_logic(state, player, options),
            "Explosives With Carrot Shooter": lambda state: carrot_shooter_in_logic(state, player, options),
            "Bunny Strike": lambda state: can_bunny_strike(state, player),
            "Bunny Whirl": lambda state: can_bunny_whirl(state, player),
            "Wall Jump Lv2": lambda state: wall_jump_2(state, player),
            "Hammer Roll Lv3": lambda state: can_hammer_roll_3(state, player),
            "Hammer Roll": lambda state: can_hammer_roll(state, player),
            "Air Dash Lv3": lambda state: can_air_dash_3(state, player),
            "Air Dash": lambda state: can_air_dash(state, player),
            "Speed Boost Lv3": lambda state: can_get_speed_boost_3(state, player),
            "Bunny Amulet": lambda state: can_bunny_amulet(state, player),
            "Bunny Amulet Lv2": lambda state: can_bunny_amulet_2(state, player),
            "Bunny Amulet Lv3": lambda state: can_bunny_amulet_3(state, player),
            "Piko Hammer Leveled": lambda state: state.has(ItemName.piko_hammer, player),
            "Carrot Bomb Entry": lambda state: state.has(ItemName.carrot_bomb, player),
            "Carrot Shooter Entry": lambda state: carrot_shooter_in_logic(state, player, options),
            "Charge Carrot Shooter Entry": lambda state: can_charge_carrot_shooter_entry(state, player, options),
            "Tm Cocoa": lambda state: state.has(ItemName.cocoa_recruit, player),
            "Tm Ashuri": lambda state: state.has(ItemName.ashuri_recruit, player),
            "Tm Rita": lambda state: state.has(ItemName.rita_recruit, player),
            "Tm Cicini": lambda state: state.has(ItemName.cicini_recruit, player),
            "Tm Saya": lambda state: state.has(ItemName.saya_recruit, player),
            "Tm Syaro": lambda state: state.has(ItemName.syaro_recruit, player),
            "Tm Pandora": lambda state: state.has(ItemName.pandora_recruit, player),
            "Tm Nieve": lambda state: state.has(ItemName.nieve_recruit, player),
            "Tm Nixie": lambda state: state.has(ItemName.nixie_recruit, player),
            "Tm Aruraune": lambda state: state.has(ItemName.aruraune_recruit, player),
            "Tm Seana": lambda state: state.has(ItemName.seana_recruit, player),
            "Tm Lilith": lambda state: state.has(ItemName.lilith_recruit, player),
            "Tm Vanilla": lambda state: state.has(ItemName.vanilla_recruit, player),
            "Tm Chocolate": lambda state: state.has(ItemName.chocolate_recruit, player),
            "Tm Kotri": lambda state: state.has(ItemName.kotri_recruit, player),
            "Tm Keke Bunny": lambda state: state.has(ItemName.keke_bunny_recruit, player),
            "Tm Miriam": lambda state: state.has(ItemName.miriam_recruit, player),
            "Tm Rumi": lambda state: state.has(ItemName.rumi_recruit, player),
            "Tm Irisu": lambda state: state.has(ItemName.irisu_recruit, player),
            "Speedy": lambda state: can_be_speedy(state, player, options),
            "Speed1": lambda state: can_use_speed_1(state, player, options),
            "Speed2": lambda state: can_use_speed_2(state, player, options),
            "Speed3": lambda state: can_use_speed_3(state, player, options),
            "Speed5": lambda state: can_use_speed_5(state, player, options),
            "3 Magic Types": lambda state: has_3_magic_types(state, player, options),
            "Item Menu": lambda state: has_item_menu(state, player, options),
            "Chapter 1": lambda state: state.has("Chapter 1", player),
            "Chapter 2": lambda state: state.has("Chapter 2", player),
            "Chapter 3": lambda state: state.has("Chapter 3", player),
            "Chapter 4": lambda state: state.has("Chapter 4", player),
            "Chapter 5": lambda state: state.has("Chapter 5", player),
            "Chapter 6": lambda state: state.has("Chapter 6", player),
            "Chapter 7": lambda state: state.has("Chapter 7", player),
            "Boost": lambda state: can_use_boost(state, player, options),
            "Boost Many": lambda state: can_use_boost_many(state, player, options),
            "Boost Boring": lambda state: can_use_boost_boring(state, player, options),
            "Darkness": lambda state: can_navigate_darkness(state, player, options),
            "Darkness Without Light Orb": lambda state: can_navigate_darkness_without_light_orb(state, player, options),
            "Underwater": lambda state: can_navigate_underwater(state, player, options),
            "Underwater Without Water Orb": lambda state: can_navigate_underwater_without_water_orb(state, player, options),
            "Prologue Trigger": lambda state: can_move_out_of_prologue_areas(state, player, options),
            "Cocoa 1": lambda state: state.has(ItemName.cocoa_1, player),
            "Kotri 1": lambda state: state.has(ItemName.kotri_1, player),
            "Ashuri 2": lambda state: state.has(ItemName.ashuri_2, player),
            "Boss Ribbon": lambda state: can_reach_ribbon(state, player),
            "Difficulty Hard": lambda state: is_at_least_hard_difficulty(state, player, options),
            "Difficulty V Hard": lambda state: is_at_least_v_hard_difficulty(state, player, options),
            "Difficulty Extreme": lambda state: is_at_least_extreme_difficulty(state, player, options),
            "Difficulty Stupid": lambda state: is_at_least_stupid_difficulty(state, player, options),
            "Knowledge Intermediate": lambda state: is_at_least_intermediate_knowledge(state, player, options),
            "Knowledge Advanced": lambda state: is_at_least_advanced_knowledge(state, player, options),
            "Knowledge Obscure": lambda state: is_at_least_obscure_knowledge(state, player, options),
            "Boring Tricks Required": lambda state: can_do_boring_tricks(state, player, options),
            "Bunstrike Zip Required": lambda state: can_bunstrike_zip(state, player, options),
            "Consumable Use": lambda state: can_use_consumables(state, player, options),
            "Amulet Food": lambda state: has_enough_amulet_food(state, player, options, 1),
            "2 Amulet Food": lambda state: has_enough_amulet_food(state, player, options, 2),
            "3 Amulet Food": lambda state: has_enough_amulet_food(state, player, options, 3),
            "4 Amulet Food": lambda state: has_enough_amulet_food(state, player, options, 4),
            "6 Amulet Food": lambda state: has_enough_amulet_food(state, player, options, 6),
            "Many Amulet Food": lambda state: has_many_amulet_food(state, player, options),
            "Open Mode": lambda _: True,
            "Block Clips Required": lambda state: can_block_clip(state, player, options),
            "Semisolid Clips Required": lambda state: can_semi_solid_clip(state, player, options),
            "Zip Required": lambda state: can_zip(state, player, options),
            "Plurkwood Reachable": lambda state: can_enter_plurkwood(state, player, options),
            "Warp Destination Reachable": lambda _: options.include_warp_destination.value,
            "Post Game Allowed": lambda _: options.include_post_game.value,
            "Post Irisu Allowed": lambda _: options.include_post_irisu.value,
            "Halloween Reachable": lambda _: options.include_halloween.value,
            "Boss Keke Bunny" : lambda state: can_reach_keke_bunny(state, player),
            "Event Warps Required" : lambda state: can_use_event_warps(state, player, options),
        }
        if literal in literal_eval_map:
            return literal_eval_map[literal], []
        elif literal.endswith("tm"):
            num_town_members = int(literal[:-2:])
            return lambda state: can_recruit_n_town_members(state, num_town_members, player), []
        elif literal in regions:
            return lambda state: state.can_reach_region(literal, player), [literal]
        return lambda state: state.has(literal, player), []
    elif isinstance(existing_rule, OpNot):
        expr, added_regions = convert_existing_rando_rule_to_ap_rule(existing_rule.expr, player, regions, options)
        return lambda state: not expr(state), added_regions
    elif isinstance(existing_rule, OpOr):
        expr_l, added_regions_l = convert_existing_rando_rule_to_ap_rule(existing_rule.exprL, player, regions, options)
        expr_r, added_regions_r = convert_existing_rando_rule_to_ap_rule(existing_rule.exprR, player, regions, options)
        added_regions = added_regions_l + added_regions_r
        return lambda state: expr_l(state) or expr_r(state), added_regions
    elif isinstance(existing_rule, OpAnd):
        expr_l, added_regions_l = convert_existing_rando_rule_to_ap_rule(existing_rule.exprL, player, regions, options)
        expr_r, added_regions_r = convert_existing_rando_rule_to_ap_rule(existing_rule.exprR, player, regions, options)
        added_regions = added_regions_l + added_regions_r
        return lambda state: expr_l(state) and expr_r(state), added_regions
    elif isinstance(existing_rule, OpBacktrack):
        return lambda _: False, []
    raise ValueError("Invalid Expression recieved.")
