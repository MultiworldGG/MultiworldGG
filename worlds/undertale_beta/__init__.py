from .Items import UndertaleItem, item_table, required_armor, required_weapons, non_key_items, key_items, \
    junk_weights_all, junk_weights_neutral, junk_weights_pacifist, junk_weights_genocide, \
    junk_weights_cut_items, spells_attack, spells_heal, spells_gimmicks, spells_pacifist, spells_violent
from .Locations import advancement_table, exclusion_table
from .er_rules import set_er_location_rules
from .er_scripts import create_er_regions_vanilla, UndertaleERLocation
from .er_data import door_name_list, genocide_missing_rooms
from worlds.generic.Rules import exclusion_rules
from BaseClasses import Tutorial, Item, MultiWorld
from .Options import UndertaleOptions
from .Spells import _undertale_procedural_spell, spell_effects, targeting_spell_effects, numerical_spell_effects, soul_spell_effects
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components
from multiprocessing import Process
from typing import Dict, List, Any
import math
import typing



def run_client():
    print('running undertale beta client')
    from .UndertaleClient import main  # lazy import
    p = Process(target=main)
    p.start()


# components.append(Component("Undertale Client", "UndertaleClient"))
components.append(Component("Undertale Beta Client", func=run_client))


def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, "data/" + file_name)


class UndertaleWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the MultiworldGG Undertale software on your computer. This guide covers "
        "single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Mewlif"]
    )]





class UndertaleWorld(World):
    """
    Undertale is an RPG where every choice you make matters. You could choose to hurt all the enemies, eventually
    causing genocide of the monster species. Or you can spare all the enemies, befriending them and freeing them
    from their underground prison.
    """
    game = "Undertale Beta"
    options_dataclass = UndertaleOptions
    options: UndertaleOptions
    web = UndertaleWeb()
    topology_present = True
    glitches_item_name = "Out of Logic Access"

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 7
    er_portal_hints: Dict[int, str]
    
    all_door_locks: List[str] = []

    procedural_spells_list: List[_undertale_procedural_spell] = []

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        if "Locked Doors" in slot_data:
            self.all_door_locks = slot_data["Locked Doors"]
            return slot_data

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    def _get_undertale_data(self):
        return {
            "world_seed": self.random.getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "client_version": self.required_client_version,
            "race": self.multiworld.is_race,
            "route_required": self.options.route_required.current_key,
            "starting_area": self.options.starting_area.current_key,
            "temy_include": bool(self.options.temy_include.value),
            "only_flakes": bool(self.options.only_flakes.value),
            "no_equips": bool(self.options.no_equips.value),
            "key_hunt": bool(self.options.key_hunt.value),
            "key_pieces": self.options.key_pieces.value,
            "extra_key_pieces": self.options.extra_key_pieces.value,
            "rando_love": bool(self.options.rando_love.value),
            "rando_stats": bool(self.options.rando_stats.value),
            "prog_armor": bool(self.options.prog_armor.value),
            "prog_weapons": bool(self.options.prog_weapons.value),
            "rando_item_button": bool(self.options.rando_item_button.value),
            "kill_sanity": self.options.kill_sanity.current_key,
            "rando_jump": bool(self.options.rando_jump.value),
            "cut_items": bool(self.options.cut_items.value),
            "kill_sanity_pack_size": self.options.kill_sanity_pack_size.value,
            "ice_traps": self.options.ice_traps.value,
            "spare_sanity": self.options.spare_sanity.current_key,
            "gifting": False,
            # "gifting": bool(self.options.gifting.value),
            "entrance_rando": False,
            # "entrance_rando": bool(self.options.entrance_rando.value),
            "spare_sanity_max": self.options.spare_sanity_max.value,
            "spare_sanity_pack_size": self.options.spare_sanity_pack_size.value,
            "bonus_locations": bool(self.options.bonus_locations.value),
            "guaranteed_filler": self.options.guaranteed_filler.value,
            "hub_shop_cost": self.options.hub_shop_cost.value,
            "enabled_spells": set(self.options.enabled_spells.value),
            "door_locks": self.options.door_locks.value,
            "mandatory_door_locks": set(self.options.mandatory_door_locks.value),
            "excluded_door_locks": set(self.options.excluded_door_locks.value),
            "love_reduction_traps": self.options.love_reduction_traps.value,
            "max_hp_reduction_traps": self.options.max_hp_reduction_traps.value,
            "atk_reduction_traps": self.options.atk_reduction_traps.value,
            "def_reduction_traps": self.options.def_reduction_traps.value,
            "sans_req_hp": self.options.sans_req_hp.value,
            "sans_req_inv_tier": self.options.sans_req_inv_tier.value,
            "undying_req_hp": self.options.undying_req_hp.value,
            "undying_req_atk": self.options.undying_req_atk.value,
            "undying_req_def": self.options.undying_req_def.value,
            "asgore_req_atk": self.options.asgore_req_atk.value,
            "asgore_req_def": self.options.asgore_req_def.value,
            "start_inventory_from_pool": self.options.start_inventory_from_pool.value,
            "advanced_logic": bool(self.options.advanced_logic.value),
            "procedural_spell_amount": self.options.procedural_spell_amount.value
        }

    def get_filler_item_name(self):
        if self.options.route_required == "all_routes":
            junk_pool = junk_weights_all.copy()
        elif self.options.route_required == "genocide":
            junk_pool = junk_weights_genocide.copy()
        elif self.options.route_required == "neutral":
            junk_pool = junk_weights_neutral.copy()
        elif self.options.route_required == "pacifist":
            junk_pool = junk_weights_pacifist.copy()
        else:
            junk_pool = junk_weights_all.copy()
        if self.options.cut_items:
            junk_pool = junk_pool | junk_weights_cut_items.copy()
        if not self.options.only_flakes:
            return self.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()))[0]
        else:
            return "Temmie Flakes"

        # if self.options.entrance_rando:
            # self.undertale_portal_pairs = assemble_er(self)
        # else:

    def generate_early(self):
        if self.options.route_required.current_key != "genocide" and \
                self.options.route_required.current_key != "all_routes":
            self.options.kill_sanity.value = 0
            self.options.rando_love.value = 0
            self.options.rando_stats.value = 0
        if self.options.route_required.current_key == "genocide":
            self.options.spare_sanity.value = 0
        if self.options.kill_sanity.value != 2:
            self.options.kill_sanity_pack_size.value = 40
        if self.options.spare_sanity.value == 1:
            self.options.spare_sanity_pack_size.value = self.options.spare_sanity_max.value

        self.procedural_spells_list = []
        if self.options.procedural_spell_amount.value > 0:
            for x in range(self.options.procedural_spell_amount.value):
                failed_to_create = True
                while failed_to_create:
                    tp_cost_from_stats = 0
                    temp_proc_spell = _undertale_procedural_spell()
                    temp_proc_spell.effect_one = self.random.choice(list(spell_effects.keys()))
                    temp_proc_spell.effect_two = self.random.choice(list(spell_effects.keys())+(["none"]*10))
                    if temp_proc_spell.effect_two != "none":
                        temp_proc_spell.tp_cost = (spell_effects[temp_proc_spell.effect_one] + (spell_effects[temp_proc_spell.effect_two]/2.0)) * 5
                    else:
                        temp_proc_spell.tp_cost = (spell_effects[temp_proc_spell.effect_one]) * 5
                    if ((temp_proc_spell.effect_one in numerical_spell_effects) or (temp_proc_spell.effect_two in numerical_spell_effects)) and ((temp_proc_spell.effect_one in targeting_spell_effects) or (temp_proc_spell.effect_two in targeting_spell_effects)):
                        temp_returned = self.gen_random_spell_stats([-5, 5],[-5, 5],[-1, 3],[-3, 3])
                        temp_proc_spell.target_def_mult = temp_returned[0]
                        temp_proc_spell.target_def_add = temp_returned[1]
                        temp_proc_spell.target_def_sub = temp_returned[2]
                        temp_proc_spell.target_def_div = temp_returned[3]
                        temp_proc_spell.tp_cost -= (temp_proc_spell.target_def_add-temp_proc_spell.target_def_sub+3)*(temp_proc_spell.target_def_mult/temp_proc_spell.target_def_div)*2
                    if ((temp_proc_spell.effect_one in numerical_spell_effects) or (temp_proc_spell.effect_two in numerical_spell_effects)):
                        temp_forced_stat = self.random.choice(["atk", "def", "lv", "hp"])
                        temp_returned = self.gen_random_spell_stats([-20, 20],[-20, 20],[-5, 5],[-5, 5])
                        temp_proc_spell.atk_mult = temp_returned[0]
                        if temp_forced_stat == "atk" and temp_proc_spell.atk_mult <= 0:
                            temp_proc_spell.atk_mult = 1
                        if temp_proc_spell.atk_mult > 0:
                            temp_proc_spell.atk_add = temp_returned[1]
                            temp_proc_spell.atk_sub = temp_returned[2]
                            temp_proc_spell.atk_div = temp_returned[3]
                        tp_cost_from_stats += (temp_proc_spell.atk_add-temp_proc_spell.atk_sub+20)*(temp_proc_spell.atk_mult/temp_proc_spell.atk_div)*2
                        temp_proc_spell.tp_cost += (temp_proc_spell.atk_add-temp_proc_spell.atk_sub+20)*(temp_proc_spell.atk_mult/temp_proc_spell.atk_div)*2
                        temp_returned = self.gen_random_spell_stats([-10, 10],[-10, 10],[-5, 5],[-5, 5])
                        temp_proc_spell.def_mult = temp_returned[0]
                        if temp_forced_stat == "def" and temp_proc_spell.def_mult <= 0:
                            temp_proc_spell.def_mult = 1
                        if temp_proc_spell.def_mult > 0:
                            temp_proc_spell.def_add = temp_returned[1]
                            temp_proc_spell.def_sub = temp_returned[2]
                            temp_proc_spell.def_div = temp_returned[3]
                        tp_cost_from_stats += (temp_proc_spell.def_add-temp_proc_spell.def_sub+12)*(temp_proc_spell.def_mult/temp_proc_spell.def_div)*2
                        temp_proc_spell.tp_cost += (temp_proc_spell.def_add-temp_proc_spell.def_sub+12)*(temp_proc_spell.def_mult/temp_proc_spell.def_div)*2
                        temp_returned = self.gen_random_spell_stats([-20, 20],[-20, 20],[-2, 2],[-2, 2])
                        temp_proc_spell.hp_mult = temp_returned[0]
                        if temp_forced_stat == "hp" and temp_proc_spell.hp_mult <= 0:
                            temp_proc_spell.hp_mult = 1
                        if temp_proc_spell.hp_mult > 0:
                            temp_proc_spell.hp_add = temp_returned[1]
                            temp_proc_spell.hp_sub = temp_returned[2]
                            temp_proc_spell.hp_div = temp_returned[3]
                        tp_cost_from_stats += (temp_proc_spell.hp_add-temp_proc_spell.hp_sub+40)*(temp_proc_spell.hp_mult/temp_proc_spell.hp_div)*2
                        temp_proc_spell.tp_cost += (temp_proc_spell.hp_add-temp_proc_spell.hp_sub+40)*(temp_proc_spell.hp_mult/temp_proc_spell.hp_div)*2
                        temp_returned = self.gen_random_spell_stats([-5, 5],[-5, 5],[-2, 2],[-2, 2])
                        temp_proc_spell.lv_mult = temp_returned[0]
                        if temp_forced_stat == "lv" and temp_proc_spell.lv_mult <= 0:
                            temp_proc_spell.lv_mult = 1
                        if temp_proc_spell.lv_mult > 0:
                            temp_proc_spell.lv_add = temp_returned[1]
                            temp_proc_spell.lv_sub = temp_returned[2]
                            temp_proc_spell.lv_div = temp_returned[3]
                        tp_cost_from_stats += (temp_proc_spell.lv_add-temp_proc_spell.lv_sub+6)*(temp_proc_spell.lv_mult/temp_proc_spell.lv_div)*2
                        temp_proc_spell.tp_cost += (temp_proc_spell.lv_add-temp_proc_spell.lv_sub+6)*(temp_proc_spell.lv_mult/temp_proc_spell.lv_div)*2
                        temp_returned = self.gen_random_spell_stats([-10, 10],[-10, 10],[1, 1],[-2, 2])
                        temp_proc_spell.total_mult = max(1, self.random.randint(-1, 2))
                        temp_proc_spell.total_add = temp_returned[1]
                        temp_proc_spell.total_sub = temp_returned[2]
                        temp_proc_spell.total_div = temp_returned[3]
                        tp_cost_from_stats = (temp_proc_spell.total_add-temp_proc_spell.total_sub+(tp_cost_from_stats/2))*(temp_proc_spell.total_mult/temp_proc_spell.total_div)*2
                        temp_proc_spell.tp_cost = (temp_proc_spell.total_add-temp_proc_spell.total_sub+(temp_proc_spell.tp_cost/2))*(temp_proc_spell.total_mult/temp_proc_spell.total_div)*2
                    if ((temp_proc_spell.effect_one in numerical_spell_effects) and (temp_proc_spell.effect_two in numerical_spell_effects)):
                        temp_proc_spell.tp_cost += tp_cost_from_stats
                    if temp_proc_spell.effect_one in soul_spell_effects:
                        temp_proc_spell.soul_mode_length = max(2, self.random.randint(-4, 8))
                    if temp_proc_spell.effect_two in soul_spell_effects:
                        temp_proc_spell.soul_mode_length = round(max(2, self.random.randint(-4, 8))/2)
                    temp_proc_spell.tp_cost += (temp_proc_spell.soul_mode_length * 30)
                    if temp_proc_spell.effect_one == "self_defense_reduction":
                        if temp_proc_spell.effect_two == "none":
                            temp_proc_spell.tp_cost = -temp_proc_spell.tp_cost
                        elif temp_proc_spell.effect_two == "self_defense_reduction":
                            temp_proc_spell.tp_cost = -(temp_proc_spell.tp_cost * 2)
                        else:
                            temp_proc_spell.tp_cost = (temp_proc_spell.tp_cost - (tp_cost_from_stats/2))-(spell_effects["self_defense_reduction"]*5)
                    elif temp_proc_spell.effect_two == "self_defense_reduction":
                        temp_proc_spell.tp_cost = (temp_proc_spell.tp_cost - (tp_cost_from_stats/4))-(spell_effects["self_defense_reduction"]*5*0.5)
                    if temp_proc_spell.tp_cost <= 250 and temp_proc_spell.tp_cost >= -250:
                        self.procedural_spells_list.append(temp_proc_spell)
                        failed_to_create = False
            for x in self.procedural_spells_list:
                print(x)
            
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            self.all_door_locks = []
            if "Locked Doors" in slot_data:
                self.all_door_locks = slot_data["Locked Doors"]
        else:
            self.all_door_locks = []
            if self.options.door_locks.value > 0:
                rand_door_list = door_name_list.copy()
                if self.options.route_required.current_key == "genocide":
                    rand_door_list = [item for item in rand_door_list if (item.split(" <-> ")[0] not in genocide_missing_rooms and item.split(" <-> ")[1] not in genocide_missing_rooms)]
                rand_door_list = [item for item in rand_door_list if (item not in self.options.excluded_door_locks.value and item not in self.options.mandatory_door_locks.value and item.split(" <-> ")[1]+" <->"+item.split(" <-> ")[0] not in self.options.mandatory_door_locks.value and item.split(" <-> ")[1]+" <->"+item.split(" <-> ")[0] not in self.options.excluded_door_locks.value)]
                amount_to_add = min(len(rand_door_list), self.options.door_locks.value)
                # print("actually added = "+str(amount_to_add))
                self.random.shuffle(rand_door_list)
                for i in range(amount_to_add):
                    self.all_door_locks.append(rand_door_list.pop())
            if len(self.options.mandatory_door_locks.value) > 0:
                rand_door_list = door_name_list.copy()
                self.all_door_locks.extend([do for do in rand_door_list if do in self.options.mandatory_door_locks.value or do.split(" <-> ")[1]+" <->"+do.split(" <-> ")[0] in self.options.mandatory_door_locks.value])

    def create_items(self):
        exclusion_pool = set()
        # Generate item pool
        itempool = []
        # Add all required progression items
        for name, num in key_items.items():
            itempool += [name] * num
        for name, num in required_armor.items():
            itempool += [name] * num
        for name, num in required_weapons.items():
            itempool += [name] * num
        for name, num in non_key_items.items():
            itempool += [name] * num
            
        for door in self.all_door_locks:
            itempool += ["Door Unlock - "+door]

        if "attack" in self.options.enabled_spells:
            for name, num in spells_attack.items():
                itempool += [name] * num
        if "heal" in self.options.enabled_spells:
            for name, num in spells_heal.items():
                itempool += [name] * num
        if "pacifist" in self.options.enabled_spells:
            for name, num in spells_pacifist.items():
                itempool += [name] * num
        if "violent" in self.options.enabled_spells:
            for name, num in spells_violent.items():
                itempool += [name] * num
        if "gimmick" in self.options.enabled_spells:
            for name, num in spells_gimmicks.items():
                itempool += [name] * num
        if self.options.rando_item_button:
            itempool += ["ITEM"]
        else:
            self.multiworld.push_precollected(self.create_item("ITEM"))
        if not self.options.rando_jump:
            itempool.remove("Jump")
            self.multiworld.push_precollected(self.create_item("Jump"))
        if self.options.route_required == "genocide":
            itempool = [item for item in itempool if item != "Stained Apron"
                        and item != "Hot Dog...?" and item != "Punch Card"]
        elif self.options.route_required == "neutral":
            itempool = [item for item in itempool if item != "Hot Dog...?"]
        if self.options.route_required == "pacifist" or self.options.route_required == "all_routes":
            itempool += ["Undyne Letter"]
        else:
            itempool.remove("Complete Skeleton")
            itempool.remove("Fish")
            itempool.remove("DT Extractor")
        if self.options.key_hunt:
            itempool += ["Key Piece"] * (self.options.key_pieces.value + self.options.extra_key_pieces.value)
        else:
            itempool += ["Left Home Key"]
            itempool += ["Right Home Key"]
        if not self.options.rando_love or \
                (self.options.route_required != "genocide" and
                 self.options.route_required != "all_routes"):
            itempool = [item for item in itempool if not item == "LOVE"]
        if self.options.rando_love or \
                (self.options.route_required == "genocide" or
                 self.options.route_required == "all_routes"):
            itempool += ["LOVE Reduction Trap"] * self.options.love_reduction_traps.value
        if self.options.rando_stats or \
                (self.options.route_required == "genocide" or
                 self.options.route_required == "all_routes"):
            itempool += ["Max HP Reduction Trap"] * self.options.max_hp_reduction_traps.value
            itempool += ["ATK Reduction Trap"] * self.options.atk_reduction_traps.value
            itempool += ["DEF Reduction Trap"] * self.options.def_reduction_traps.value
        if self.options.spare_sanity == 2 and self.options.route_required != "genocide":
            itempool += ["Ruins Spare"] * math.ceil(self.options.spare_sanity_max.value /
                                                    self.options.spare_sanity_pack_size.value)
            itempool += ["Snowdin Spare"] * math.ceil(self.options.spare_sanity_max.value /
                                                      self.options.spare_sanity_pack_size.value)
            itempool += ["Waterfall Spare"] * math.ceil(self.options.spare_sanity_max.value /
                                                        self.options.spare_sanity_pack_size.value)
            itempool += ["Hotland Spare"] * math.ceil(self.options.spare_sanity_max.value /
                                                      self.options.spare_sanity_pack_size.value)
        elif self.options.spare_sanity == 1:
            self.multiworld.push_precollected(self.create_item("Ruins Spare"))
            self.multiworld.push_precollected(self.create_item("Snowdin Spare"))
            self.multiworld.push_precollected(self.create_item("Waterfall Spare"))
            self.multiworld.push_precollected(self.create_item("Hotland Spare"))
        if self.options.kill_sanity != 2 or \
                (self.options.route_required != "genocide" and
                 self.options.route_required != "all_routes"):
            self.multiworld.push_precollected(self.create_item("Ruins Population Pack"))
            self.multiworld.push_precollected(self.create_item("Snowdin Population Pack"))
            self.multiworld.push_precollected(self.create_item("Waterfall Population Pack"))
            self.multiworld.push_precollected(self.create_item("Hotland Population Pack"))
            exclusion_pool.update(exclusion_table["NoKills"])
        else:
            itempool += ["Ruins Population Pack"] * math.ceil(20/self.options.kill_sanity_pack_size.value)
            itempool += ["Snowdin Population Pack"] * math.ceil(16/self.options.kill_sanity_pack_size.value)
            itempool += ["Waterfall Population Pack"] * math.ceil(18/self.options.kill_sanity_pack_size.value)
            itempool += ["Hotland Population Pack"] * math.ceil(40/self.options.kill_sanity_pack_size.value)
        if self.options.ice_traps.value > 0:
            itempool += ["Ice Trap"] * self.options.ice_traps.value
        if self.options.procedural_spell_amount.value > 0:
            for x in range(self.options.procedural_spell_amount.value):
                itempool += ["Procedural Spell "+str(x+1)]
        if not self.options.rando_stats or \
                (self.options.route_required != "genocide" and
                 self.options.route_required != "all_routes"):
            itempool = [item for item in itempool if not (item == "ATK Up" or item == "DEF Up" or item == "HP Up")]
        if self.options.temy_include:
            itempool += ["temy armor"]
        if self.options.no_equips:
            itempool = [item for item in itempool if item not in required_armor and item not in required_weapons]
        else:
            if self.options.prog_armor:
                itempool = [item if (item not in required_armor and not item == "temy armor") else
                            "Progressive Armor" for item in itempool]
            if self.options.prog_weapons:
                itempool = [item if item not in required_weapons else "Progressive Weapons" for item in itempool]
        if self.options.route_required == "genocide" or \
                self.options.route_required == "all_routes":
            if not self.options.only_flakes:
                itempool += ["Snowman Piece"] * 2
            if not self.options.no_equips:
                itempool = ["Real Knife" if item == "Worn Dagger" else "The Locket"
                            if item == "Heart Locket" else item for item in itempool]
        if self.options.only_flakes:
            itempool = [item for item in itempool if item not in non_key_items]

        if self.options.starting_area.current_key.title() == "None":
            pass
        elif self.options.starting_area.current_key.title() == "All":
            all_keys = ["Ruins Key", "Snowdin Key", "Waterfall Key", "Hotland Key"]
            for item in all_keys:
                itempool.remove(item)
                self.multiworld.push_precollected(self.create_item(item))
        else:
            starting_key = self.options.starting_area.current_key.title() + " Key"
            itempool.remove(starting_key)
            self.multiworld.push_precollected(self.create_item(starting_key))
        # Choose locations to automatically exclude based on settings
        exclusion_pool.update(exclusion_table[self.options.route_required.current_key])
        if not self.options.rando_love or \
                (self.options.route_required != "genocide" and
                 self.options.route_required != "all_routes"):
            exclusion_pool.update(exclusion_table["NoLove"])
        if not self.options.rando_stats or \
                (self.options.route_required != "genocide" and
                 self.options.route_required != "all_routes"):
            exclusion_pool.update(exclusion_table["NoStats"])

        # Choose locations to automatically exclude based on settings
        exclusion_checks = set()
        exclusion_checks.update([])
        exclusion_rules(self.multiworld, self.player, exclusion_checks)

        # Convert itempool into real items
        completed_itempool = [item for item in map(lambda itm_name: self.create_item(itm_name), itempool)]
        # Fill remaining items with randomly generated junk or Temmie Flakes
        counter = 1
        while len(completed_itempool)+self.options.guaranteed_filler.value > len(self.multiworld.get_unfilled_locations(self.player)):
            region = self.get_region("room_area1")
            location = UndertaleERLocation(self.player, "Hub Shop "+str(counter), counter, region)
            region.locations.append(location)
            counter += 1
        while len(completed_itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            completed_itempool.append(self.create_filler())

        self.multiworld.itempool += completed_itempool
    
    def set_rules(self) -> None:
        set_er_location_rules(self)

    def create_regions(self):
        create_er_regions_vanilla(self)

    def fill_slot_data(self):
        slot_data = self._get_undertale_data()
        temp_list: List = []
        for spl in self.procedural_spells_list:
            temp_list.append([spl.effect_one, spl.effect_two, spl.soul_mode_length, spl.tp_cost, spl.lv_add, spl.lv_sub, spl.lv_mult, spl.lv_div, 
                                              spl.hp_add, spl.hp_sub, spl.hp_mult, spl.hp_div, spl.atk_add, spl.atk_sub, spl.atk_mult, spl.atk_div, 
                                              spl.def_add, spl.def_sub, spl.def_mult, spl.def_div, spl.target_def_add, spl.target_def_sub, spl.target_def_mult, spl.target_def_div, 
                                              spl.total_add, spl.total_sub, spl.total_mult, spl.total_div])
        slot_data["Procedural_Spells"] = temp_list
        print(temp_list)
        slot_data["Locked Doors"] = self.all_door_locks
        return slot_data

    def create_item(self, name: str) -> Item:
        from .Items import item_table
        item_data = item_table[name]
        item = UndertaleItem(name, item_data.classification, item_data.code, self.player)
        return item

    def format_spoiler_spell_math(self, math_add: float, math_sub: float, math_div: float, math_mult: float, math_name: str, math_base_name: str) -> str:
                list_as_string = ""
                if (math_mult != 1 or math_div != 1) and (math_add != 0 or math_sub != 0):
                    list_as_string += f"    {math_name}: ({math_base_name}"
                else:
                    list_as_string += f"    {math_name}: {math_base_name}"
                if math_add > 0:
                    list_as_string += f" + {math_add}"
                if math_sub > 0:
                    list_as_string += f" - {math_sub}"
                if math_mult != 1 or math_div != 1:
                    if math_add != 0 or math_sub != 0:
                        list_as_string += f")"
                    if math_mult != 1:
                        list_as_string += f" * "
                        if math_div != 1:
                            list_as_string += f"({math_mult} / {max(1, math_div)})"
                        else:
                            list_as_string += f"{math_mult}"
                    else:
                        list_as_string += f" / {max(1, math_div)}"
                list_as_string += f"\n"
                return list_as_string

    def gen_random_spell_stats(self, add_range: List[int], sub_range: List[int], mult_range: List[int], div_range: List[int]) -> List[int]:
                            _mult = max(0, self.random.randint(mult_range[0], mult_range[1]))
                            _add = 0
                            _sub = 0
                            _div = 1
                            _add = max(0, self.random.randint(add_range[0], add_range[1]))
                            _sub = max(0, self.random.randint(sub_range[0], sub_range[1]))
                            if _sub > _add:
                                _sub -= _add
                                _add = 0
                            elif _sub < _add:
                                _add -= _sub
                                _sub = 0
                            elif _sub == _add:
                                _sub = 0
                                _add = 0
                            _div = max(1, self.random.randint(div_range[0], div_range[1]))
                            if _mult == _div:
                                _div = 1
                                _mult = 1
                            return [_mult, _add, _sub, _div]

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        player_name = self.multiworld.get_player_name(self.player)
        spoiler_handle.write(f"\n\nLocked Doors ({player_name}): ")
        list_as_string = ""
        for item in self.all_door_locks:
            list_as_string += f"{item}, "
        list_as_string = list_as_string.removesuffix(", ")
        spoiler_handle.write(list_as_string)
        spoiler_handle.write(f"\n\nProcedural Spells ({player_name}): \n")
        list_as_string = " All spell totals are rounded down, and cannot be lower than zero.\n"
        i = 1
        for item in self.procedural_spells_list:
            list_as_string += f"  Spell {str(i)}:\n"
            list_as_string += f"    TP Cost: {(item.tp_cost/250.0*100.0)}\n"
            list_as_string += f"    Effect One: {item.effect_one}\n"
            if item.effect_two != "none":
                list_as_string += f"    Effect Two (Half Power): {item.effect_two}\n"
            if item.soul_mode_length > 0:
                list_as_string += f"    Soul Effect Turn Length: {item.soul_mode_length}\n"
            if item.lv_mult > 0:
                list_as_string += self.format_spoiler_spell_math(item.lv_add, item.lv_sub, item.lv_div, item.lv_mult, "LV Bonus", "LV")
            if item.hp_mult > 0:
                list_as_string += self.format_spoiler_spell_math(item.hp_add, item.hp_sub, item.hp_div, item.hp_mult, "HP Bonus", "HP")
            if item.atk_mult > 0:
                list_as_string += self.format_spoiler_spell_math(item.atk_add, item.atk_sub, item.atk_div, item.atk_mult, "ATK Bonus", "ATK")
            if item.def_mult > 0:
                list_as_string += self.format_spoiler_spell_math(item.def_add, item.def_sub, item.def_div, item.def_mult, "DEF Bonus", "DEF")
            if item.target_def_mult > 0:
                list_as_string += self.format_spoiler_spell_math(item.target_def_add, item.target_def_sub, item.target_def_div, item.target_def_mult, "Enemy DEF Modifier", "Enemy_DEF")
            if item.total_mult > 0 and (item.total_div != 1 or item.total_sub != 0 or item.total_add != 0 or item.total_mult != 1):
                list_as_string += self.format_spoiler_spell_math(item.total_add, item.total_sub, item.total_div, item.total_mult, "Total Modifier", "Total")
            i += 1
        spoiler_handle.write(list_as_string)
        