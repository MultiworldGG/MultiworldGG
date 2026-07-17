from typing import TYPE_CHECKING
from BaseClasses import Item
import math
from .Items import item_table_pacts, item_table_keepsake, items_table_fates_completion, TOTAL_MIRROR_ITEMS
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule, add_rule, add_item_rule
from .Locations import location_weapons_subfixes
from .Data import mirror_upgrades, mirror_ri_requirements

if TYPE_CHECKING:
    from . import HadesWorld

class HadesLogic(LogicMixin):
    def _total_heat_level(self, player: int, amount: int, options) -> bool:
        if not options.heat_system == "reverse_heat":
            return True
        count = 0
        for key in item_table_pacts.keys():
            count = count + self.count(key, player)
        return count >= amount

    def _has_enough_of_item(self, player: int, amount: int, item: str) -> bool:
        return self.count(item, player) >= amount

    def _has_enough_routine_inspection(self, player: int, amount: int, options) -> bool:
        if not options.heat_system == "reverse_heat":
            return True
        return self._has_enough_of_item(player, amount, "Routine Inspection Pact Level")
    
    def _has_all_approval_process(self, player: int, options) -> bool:
        if not options.heat_system == "reverse_heat":
            return True
        total_approval_process = int(options.approval_process_pact_amount.value)
        return self._has_enough_of_item(player, total_approval_process, "Approval Process Pact Level")
    
    def _has_enough_urns(self, player: int, amount: int) -> bool:
        return self.count("Urns Of Wealth1 Item", player) + self.count("Urns Of Wealth2 Item", player) \
            + self.count("Urns Of Wealth3 Item", player) >= amount
    
    def _has_enough_throve(self, player: int, amount: int) -> bool:
        return self.count("Infernal Trove1 Item", player) + self.count("Infernal Trove2 Item", player) \
            + self.count("Infernal Trove3 Item", player) >= amount
    
    def _has_enough_weapons(self, player: int, options, amount: int) -> bool:
        if not options.weaponsanity:
            return True
        count = 0
        if self._has_weapon("Sword Weapon", player, options):
            count += 1
        if self._has_weapon("Bow Weapon", player, options):
            count += 1
        if self._has_weapon("Spear Weapon", player, options):
            count += 1
        if self._has_weapon("Shield Weapon", player, options):
            count += 1
        if self._has_weapon("Fist Weapon", player, options):
            count += 1
        if self._has_weapon("Gun Weapon", player, options):
            count += 1
        return count >= amount
    
    def _has_enough_keepsakes(self, player: int, amount: int, options) -> bool:
        amount_keepsakes = 0
        for keepsake_name in item_table_keepsake:
            amount_keepsakes += self.count(keepsake_name, player)
        return amount_keepsakes >= amount

    def _has_enough_fates_done(self, player: int, amount: int, options) -> bool:
        amount_fates = 0 
        for fates_names in items_table_fates_completion:
            amount_fates += self.count(fates_names, player)
        return amount_fates >= amount
    
    def _has_weapon(self, weaponSubfix : str, player: int, option) -> bool:
        if not option.weaponsanity:
            return True
        if weaponSubfix == "Sword Weapon":
            return ((option.initial_weapon == 0) or (self.has("Sword Weapon Unlock Item", player)))
        if weaponSubfix == "Bow Weapon":
            return ((option.initial_weapon == 1) or (self.has("Bow Weapon Unlock Item", player)))
        if weaponSubfix == "Spear Weapon":
            return ((option.initial_weapon == 2) or (self.has("Spear Weapon Unlock Item", player)))
        if weaponSubfix == "Shield Weapon":
            return ((option.initial_weapon == 3) or (self.has("Shield Weapon Unlock Item", player)))
        if weaponSubfix == "Fist Weapon":
            return ((option.initial_weapon == 4) or (self.has("Fist Weapon Unlock Item", player)))
        if weaponSubfix == "Gun Weapon":
            return ((option.initial_weapon == 5) or (self.has("Gun Weapon Unlock Item", player)))

    def _has_fishing_rod(self, player: int, option) -> bool:
        if not option.storesanity:
            return self._has_defeated_boss("Bros Victory", player, option)
        return self.has("Fishing Rod Item", player)

    def _has_ability(self, ability: str, player: int, option) -> bool:
        if option.abilitysanity.value == 2:
            return True
        if ability == "Dash" or ability == "Cast" or ability == "Call":
            return self.has(ability, player)
        #For any attack or any special, checks if there is a pair of weapon unlocked and its attack/special
        if ability.startswith("Any "):
                move = ability[4:] #Cut off the "Any " part
                if option.abilitysanity.value == 1:
                        return self.has(move,player)
                if option.weaponsanity:
                        return any(
                        self._has_weapon(f"{weapon} Weapon", player, option)
                        and self.has(f"{weapon} {move}", player)
                        for weapon in ("Sword", "Spear", "Shield", "Bow", "Fist", "Gun")
                        )
                else:
                        return any(
                        self.has(f"{weapon} {move}", player)
                        for weapon in ("Sword", "Spear", "Shield", "Bow", "Fist", "Gun")
                        )
        #For a specific attack or special, see if the player can access it
        
        if ability.endswith(" Attack"):
                if option.abilitysanity.value == 1:
                        return self.has("Attack", player)
                return self.has(ability, player)
        if ability.endswith(" Special"):
                if option.abilitysanity.value == 1:
                        return self.has("Special", player)
                return self.has(ability, player)
        return False
    def _ability_progression_count(self, player: int, options) -> int:
        count = 0
        if self._has_ability("Dash", player, options):
                count += 1
        if self._has_ability("Cast", player, options):
                count += 1
        if self._has_ability("Call", player, options):
                count += 1
        if options.abilitysanity.value == 1:
                if self.has("Attack", player) and self.has("Special", player):
                        count += 1
        else:
                if any(
                self._has_ability(f"{weapon} Attack", player, options)
                and self._has_ability(f"{weapon} Special", player, options)
                for weapon in ("Sword", "Spear", "Shield", "Bow", "Fist", "Gun")
                ):
                        count += 1
        return count
    def _has_required_ability_progression(self, player: int, options, amount: int):
        return self._ability_progression_count(player, options) >= amount
    def _has_attack_special_pairs(self, player: int, options, amount: int):
        count = 0
        for weapon in ("Sword", "Spear", "Shield", "Bow", "Fist", "Gun"):
                if(self._has_ability(f"{weapon} Attack", player, options)
                and self._has_ability(f"{weapon} Special", player, options)):
                        count += 1
        return count >= amount
    def _has_all_basic_moves(self, player: int, option) -> bool:
        return (self._has_ability("Dash", player, option) and self._has_ability("Cast", player, option) and \
                self._has_ability("Any Attack", player, option) and self._has_ability("Any Special", player, option))

    def _can_access_all_boons(self, player: int, option) -> bool:
        return (self._has_all_basic_moves(player, option) and self._has_ability("Call", player, option))

    #Only a few mirror upgrades have one level. The rest will not be locked behind one location, but we need to check these and enforce them.
    def _has_all_mirror_talents(self, player: int, option) -> bool:
        if not option.mirrorsanity:
            return True
        return self.has("Greater Reflex Level", player) and self.has("Ruthless Reflex Level", player) and self.has("Stubborn Defiance Level", player) 

    def _can_reach_mirror_rank(self, current_rank, max_rank, player: int, options) -> bool:
        quarter = math.floor(max_rank * 0.25)
        half = math.floor(max_rank * 0.50)
        three_quarters = math.floor(max_rank * 0.75)

        if max_rank <= 3: 
                return True
        if current_rank <= quarter:
                return True 
        if current_rank <= half:
                return self._has_defeated_boss("Meg Victory", player, options)
        if current_rank <= three_quarters:
                return self._has_defeated_boss("Lernie Victory", player, options)
        if current_rank < max_rank:
                return self._has_defeated_boss("Bros Victory", player, options)
        return self._has_defeated_boss("Hades Victory", player, options)

        
    def _has_unlocked_troves(self, player: int, option) -> bool:
        if not option.storesanity:
                return True
        return self.has("Infernal Trove1 Item", player)


    def _can_get_victory(self, player: int, options) -> bool:
        can_win = self._has_defeated_boss("Hades Victory", player, options)
        if options.weaponsanity:
            weapons = options.weapons_clears_needed.value
            can_win = (can_win) and (self._enough_weapons_victories(player, options, weapons))
        if options.keepsakesanity:
            keepsakes = options.keepsakes_needed.value
            can_win = (can_win) and (self._has_enough_keepsakes(player, keepsakes, options))
        fates = options.fates_needed.value
        can_win = (can_win) and (self._has_enough_fates_done(player, fates, options))
        return can_win
    
    def _has_defeated_boss(self, bossVictory : str, player: int, options) -> bool:
        #If checking for hades victory, check we logically bossVictory item.
        if (bossVictory == "Hades Victory"):
            if options.location_system == "room_weapon_based":
                counter = 0
                counter += self.count(bossVictory + " Sword Weapon", player)
                counter += self.count(bossVictory + " Spear Weapon", player)
                counter += self.count(bossVictory + " Bow Weapon", player)
                counter += self.count(bossVictory + " Shield Weapon", player)
                counter += self.count(bossVictory + " Fist Weapon", player)
                counter += self.count(bossVictory + " Gun Weapon", player)
                return counter > 0
            else:
                return self.has(bossVictory, player)
            
        #For every other boss, check we can reach the region after them
        if (bossVictory == "Meg Victory"):
             region = "Asphodel"
        if (bossVictory == "Lernie Victory"):
             region = "Elysium"
        if (bossVictory == "Bros Victory"):
             region = "Styx"

        if options.location_system == "room_weapon_based":
             return any(self.can_reach(f"{region} {weapon}", "Region", player) 
                        for weapon in location_weapons_subfixes)
        
        return self.can_reach(f"{region}", "Region", player)

    def _enough_weapons_victories(self, player: int, options, amount: int) -> bool:
        if options.location_system == "room_weapon_based":
            counter = 0
            counter += self.count("Hades Victory" + " Sword Weapon", player)
            counter += self.count("Hades Victory" + " Spear Weapon", player)
            counter += self.count("Hades Victory" + " Bow Weapon", player)
            counter += self.count("Hades Victory" + " Shield Weapon", player)
            counter += self.count("Hades Victory" + " Fist Weapon", player)
            counter += self.count("Hades Victory" + " Gun Weapon", player)
            return counter >= amount
        else:
            return self.has("Hades Victory", player) and self._has_enough_weapons(player, options, amount)

    def _has_enough_mirror_levels(self, amount: int, player: int, options) -> None:
        if not options.mirrorsanity:
            return True
        
        counter = 0
        for upgrade in mirror_upgrades:
            counter += self.count(f"{upgrade.name} Level", player)

        return counter >= amount

# -----------


def set_rules(world: "HadesWorld", player: int, number_items: int, location_table: dict, options) -> None:
    # Set up some logic in areas to avoid having all heats "stack up" as batch in other games.
    total_routine_inspection = int(options.routine_inspection_pact_amount.value)

    if options.location_system == "room_weapon_based":
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Sword Weapon", total_routine_inspection)
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Spear Weapon", total_routine_inspection)
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Bow Weapon", total_routine_inspection)
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Shield Weapon", total_routine_inspection)
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Fist Weapon", total_routine_inspection)
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Gun Weapon", total_routine_inspection)
    else:
        add_rule(world.get_entrance("Exit Tartarus", player), 
                 lambda state: state.has("Meg Victory", player) and  \
                    state._total_heat_level(player, min(math.floor(number_items / 4), 10), options) and  \
                    state._has_enough_routine_inspection(player, total_routine_inspection-2, options) and  \
                    state._has_enough_weapons(player, options, 2) and \
                    state.has("Dash", player) and \
                    state._has_attack_special_pairs(player, options, 1) and \
                    state._has_enough_mirror_levels(math.floor(TOTAL_MIRROR_ITEMS/4), player, options))
        add_rule(world.get_entrance("Exit Asphodel", player), lambda state: state.has("Lernie Victory", player) and  \
                    state._total_heat_level(player, min(math.floor(number_items / 2), 20), options) and \
                    state._has_enough_routine_inspection(player, total_routine_inspection - 1, options) and  \
                    state._has_enough_weapons(player, options, 3) and \
                    state._has_required_ability_progression(player, options, 2) and \
                    state._has_attack_special_pairs(player, options, 2) and \
                    state._has_enough_mirror_levels(math.floor(TOTAL_MIRROR_ITEMS/2), player, options))
        add_rule(world.get_entrance("Exit Elysium", player), lambda state: state.has("Bros Victory", player) and  \
                    state._total_heat_level(player, min(math.floor(number_items * 3 / 4), 30), options) and  \
                    state._has_enough_routine_inspection(player, total_routine_inspection, options) and  \
                    state._has_enough_weapons(player, options, 5) and \
                    state._has_required_ability_progression(player, options, 3) and \
                    state._has_attack_special_pairs(player, options, 3) and \
                    state._has_enough_mirror_levels(math.floor(3*TOTAL_MIRROR_ITEMS/4), player, options))
        add_rule(world.get_location("Beat Hades", player), lambda state: \
                    state._total_heat_level(player, min(number_items, 35), options) and \
                    state._has_enough_weapons(player, options, 6) and \
                    state._has_required_ability_progression(player, options, 4) and \
                    state._has_attack_special_pairs(player, options, 4) and \
                    state._has_enough_mirror_levels(TOTAL_MIRROR_ITEMS, player, options))
    

    forbid_important_items_on_late_styx(world, player, options)
    world.completion_condition[player] = lambda state: state._can_get_victory(player, options)
    
    if options.keepsakesanity:
        add_rule(world.get_entrance("NPCS", player), lambda state: True)
        add_rule(world.get_location("Eurydice Keepsake", player), lambda state: \
                 state._has_defeated_boss("Lernie Victory", player, options))
        add_rule(world.get_location("Thanatos Keepsake", player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))
        add_rule(world.get_location("Patroclus Keepsake", player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))
        set_keepsake_balance(world, player, location_table, options)
    if options.weaponsanity:
        add_rule(world.get_entrance("Weapon Cache", player), lambda state: True)
    if options.storesanity:
        set_store_rules(world, player, location_table, options)
    if options.fatesanity:
        set_fates_rules(world, player, location_table, options, "")
    set_fates_rules(world, player, location_table, options, " Event")
    if options.fishsanity:
        set_fishing_rules(world, player, options)
    if options.mirrorsanity:
        set_mirror_rules(world, player, options)

    if options.keepsakesanity and options.storesanity:
        add_rule(world.get_location("Orpheus Keepsake", player), lambda state: \
                state.has("Court Musician Sentence Item",player))
        

def set_keepsake_balance(world: "HadesWorld", player: int, location_table : dict, options) -> None:
    add_rule(world.get_location("Zeus Keepsake", player), lambda state:   \
            state.has("Zeus Keepsake", player))
    add_rule(world.get_location("Poseidon Keepsake", player), lambda state:   \
            state.has("Poseidon Keepsake", player))
    add_rule(world.get_location("Athena Keepsake", player), lambda state:   \
            state.has("Athena Keepsake", player))
    add_rule(world.get_location("Aphrodite Keepsake", player), lambda state:   \
            state.has("Aphrodite Keepsake", player))
    add_rule(world.get_location("Ares Keepsake", player), lambda state:   \
            state.has("Ares Keepsake", player))
    add_rule(world.get_location("Artemis Keepsake", player), lambda state:   \
            state.has("Artemis Keepsake", player))
    add_rule(world.get_location("Dionysus Keepsake", player), lambda state:   \
            state.has("Dionysus Keepsake", player))
    add_rule(world.get_location("Demeter Keepsake", player), lambda state:   \
            state.has("Demeter Keepsake", player))
    add_rule(world.get_location("Hermes Keepsake", player), lambda state:   \
            state._has_defeated_boss("Meg Victory", player, options))
    add_rule(world.get_location("Megaera Keepsake", player), lambda state:   \
            state._has_defeated_boss("Meg Victory", player, options))


def set_store_rules(world: "HadesWorld", player: int, location_table : dict, options) -> None:
    #Fountains
    add_rule(world.get_location("Fountain Upgrade1 Location", player), lambda state:  \
            state.has("Fountain Tartarus Item", player))
    add_rule(world.get_location("Fountain Upgrade2 Location", player), lambda state:  \
            state.has("Fountain Upgrade1 Item", player) and state.has("Fountain Tartarus Item", player))
    add_rule(world.get_location("Fountain Asphodel Location", player), lambda state:  \
            state.has("Fountain Tartarus Item", player) and state.has("Keepsake Collection Item", player) and  \
            state._has_defeated_boss("Meg Victory", player, options))
    add_rule(world.get_location("Fountain Elysium Location", player), lambda state: \
            state.has("Fountain Tartarus Item", player) and state.has("Keepsake Collection Item", player) and  \
            state._has_defeated_boss("Lernie Victory", player, options))
    
    #Urns
    add_rule(world.get_location("Urns Of Wealth1 Location", player), lambda state:  \
             state.has("Fountain Tartarus Item", player))
    add_rule(world.get_location("Urns Of Wealth2 Location", player), lambda state: state._has_enough_urns(player,1))
    add_rule(world.get_location("Urns Of Wealth3 Location", player), lambda state: state._has_enough_urns(player,2))
    
    #Infernal Trove
    add_rule(world.get_location("Infernal Trove2 Location", player), lambda state: state._has_enough_throve(player,1) \
        and state.has("Fountain Tartarus Item",player) and state.has("Fountain Asphodel Item",player) \
        and state.has("Fountain Elysium Item",player) and state.has("Keepsake Collection Item", player))

    add_rule(world.get_location("Infernal Trove3 Location", player), lambda state: state._has_enough_throve(player,2) \
        and state.has("Fountain Tartarus Item",player) and state.has("Fountain Asphodel Item",player) \
        and state.has("Fountain Elysium Item",player) and state.has("Keepsake Collection Item", player) \
        and state.has("Deluxe Contractor Desk Item", player))
    
    #Keepsake storage
    add_rule(world.get_location("Keepsake Collection Location", player), lambda state:  \
            state._has_defeated_boss("Meg Victory", player, options) and state.has("Fountain Tartarus Item", player))
    
    #Deluxe contractor desk
    add_rule(world.get_location("Deluxe Contractor Desk Location", player), lambda state:  \
            state.has("Fountain Elysium Item", player) and state.has("Court Musician Sentence Item", player) and \
            state.has("Urns Of Wealth1 Item", player) and state.has("Keepsake Collection Item", player) and \
            state.has("Infernal Trove1 Item", player))
    
    #Other random stuff
    add_rule(world.get_location("Vanquishers Keep Location", player), lambda state:\
            state.has("Deluxe Contractor Desk Item", player))
    add_rule(world.get_location("Fishing Rod Location", player), lambda state:  \
            state._has_defeated_boss("Bros Victory", player, options) and state.has("Fountain Tartarus Item", player))
    add_rule(world.get_location("Court Musician Stand Location", player), lambda state:  \
            state.has("Court Musician Sentence Item", player))
    
    #Orpheus might have other rules depending on settings
    add_rule(world.get_location("Court Musician Sentence Location", player), lambda state:  \
            state._has_defeated_boss("Meg Victory", player, options) and state.has("Fountain Tartarus Item", player))
    
    #Upgrades of runs with gems locations
    add_rule(world.get_location("Pitch Black Darkness Location", player), lambda state:  \
            state.has("Deluxe Contractor Desk Item", player))
    add_rule(world.get_location("Fated Keys Location", player), lambda state:  \
            state.has("Deluxe Contractor Desk Item", player))
    add_rule(world.get_location("Brilliant Gemstones Location", player), lambda state:  \
            state.has("Deluxe Contractor Desk Item", player))
    add_rule(world.get_location("Vintage Nectar Location", player), lambda state:  \
            state.has("Deluxe Contractor Desk Item", player))
    add_rule(world.get_location("Darker Thirst Location", player), lambda state: \
            state.has("Deluxe Contractor Desk Item", player))
    

def set_fates_rules(world: "HadesWorld", player: int, location_table : dict, options, subfix: str) -> None:
    #Rules that dont depend on other settings
    add_rule(world.get_location("Is There No Escape?" + subfix, player), lambda state: \
            state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("Harsh Conditions" + subfix, player), lambda state:  \
            state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("Slashed Benefits" + subfix, player), lambda state:  \
            state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("The Useless Trinket" + subfix, player), lambda state:  \
            state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("Wanton Ransacking" + subfix, player), lambda state:  \
            state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("Dark Reflections" + subfix, player), lambda state:  \
            state._has_defeated_boss("Hades Victory", player, options))

    #Rules that depend on storesanity
    if options.storesanity:
        add_rule(world.get_location("The Reluctant Musician" + subfix, player), lambda state:  \
                state.has("Court Musician Sentence Item", player))
        add_rule(world.get_location("Musician and Muse" + subfix, player), lambda state:  \
                state.has("Court Musician Sentence Item", player) \
                and state._has_defeated_boss("Hades Victory", player, options))
        add_rule(world.get_location("The Gift of Song" + subfix, player), lambda state: \
                state.has("Court Musician Sentence Item", player))
        add_rule(world.get_location("Denizens Of The Deep" + subfix, player), lambda state:  \
                state._has_defeated_boss("Hades Victory", player, options) and state.has("Fishing Rod Item",player))
        add_rule(world.get_location("A Place of Revelry" + subfix, player), lambda state: \
                state.has("Deluxe Contractor Desk Item", player))
        add_rule(world.get_location("Customer Loyalty" + subfix, player), lambda state: \
                state.has("Fishing Rod Item", player) and state.has("Infernal Trove1 Item", player))
        add_rule(world.get_location("Divided by Death" + subfix, player), lambda state: \
                state.has("Court Musician Sentence Item", player))   
    else:
        add_rule(world.get_location("The Reluctant Musician" + subfix, player), lambda state:  \
                state._has_defeated_boss("Meg Victory", player, options))
        add_rule(world.get_location("Musician and Muse" + subfix, player), lambda state:  \
                state._has_defeated_boss("Hades Victory", player, options))
        add_rule(world.get_location("Denizens Of The Deep" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    #This part depends on weaponsanity, but the false option is handled on has_enough_weapons
    add_rule(world.get_location("Infernal Arms" + subfix, player), lambda state:  \
            state._has_enough_weapons(player, options, 6))
    add_rule(world.get_location("A Violent Past" + subfix, player), lambda state:  \
            state._has_enough_weapons(player, options, 6))
    add_rule(world.get_location("Master Of Arms" + subfix, player), lambda state:  \
            state._has_enough_weapons(player, options, 6) and  \
            state._has_defeated_boss("Hades Victory", player, options))
   
    #rules that depend on weaponsanity:
    if options.weaponsanity:
        add_rule(world.get_location("The Stygian Blade" + subfix, player), lambda state: \
                state.has("Sword Weapon Unlock Item", player) or options.initial_weapon == 0)
        add_rule(world.get_location("The Heart Seeking Bow" + subfix, player), lambda state: \
                state.has("Bow Weapon Unlock Item", player) or options.initial_weapon == 1)
        add_rule(world.get_location("The Eternal Spear" + subfix, player), lambda state: \
                state.has("Spear Weapon Unlock Item", player) or options.initial_weapon == 2)
        add_rule(world.get_location("The Shield Of Chaos" + subfix, player), lambda state: \
                state.has("Shield Weapon Unlock Item", player) or options.initial_weapon == 3)
        add_rule(world.get_location("The Twin Fists" + subfix, player), lambda state: \
                state.has("Fist Weapon Unlock Item", player) or options.initial_weapon == 4)
        add_rule(world.get_location("The Adamant Rail" + subfix, player), lambda state: \
                state.has("Gun Weapon Unlock Item", player) or options.initial_weapon == 5)
        
        add_rule(world.get_location("Eternal Rest" + subfix, player), lambda state: \
                state.has("Sword Weapon Unlock Item", player) or options.initial_weapon == 0)
        
        #balancing for aspects related fates
        add_rule(world.get_location("The Holy Liege" + subfix, player), lambda state: \
                        state.has("Sword Weapon Unlock Item", player) or options.initial_weapon == 0)
        add_rule(world.get_location("The Preserver's Avatar" + subfix, player), lambda state: \
                        state.has("Bow Weapon Unlock Item", player) or options.initial_weapon == 1)
        add_rule(world.get_location("The Fated Saint of War" + subfix, player), lambda state: \
                        state.has("Spear Weapon Unlock Item", player) or options.initial_weapon == 2)
        add_rule(world.get_location("The Dragon's Rival" + subfix, player), lambda state: \
                        state.has("Shield Weapon Unlock Item", player) or options.initial_weapon == 3)
        add_rule(world.get_location("The God-like King" + subfix, player), lambda state: \
                        state.has("Fist Weapon Unlock Item", player) or options.initial_weapon == 4)
        add_rule(world.get_location("The Dawn Bringer" + subfix, player), lambda state: \
                        state.has("Gun Weapon Unlock Item", player) or options.initial_weapon == 5)
        
    #rules that depend on abilitysanity:
    if options.abilitysanity.value != 2:
        add_rule(world.get_location("Goddess Of Wisdom" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("God Of The Heavens" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("God Of The Sea" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("Goddess Of Love" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("God Of War" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("Goddess Of The Hunt" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("God Of Wine" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("God Of Swiftness" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("Goddess Of Seasons" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("Power Without Equal" + subfix, player), lambda state: \
                state._can_access_all_boons(player, options))
        add_rule(world.get_location("Primordial Boons" + subfix, player), lambda state: \
                state._has_all_basic_moves(player, options))
        add_rule(world.get_location("Primordial Banes" + subfix, player), lambda state: \
                state._has_all_basic_moves(player, options))
        add_rule(world.get_location("The Stygian Blade" + subfix, player), lambda state: \
                state._has_ability("Sword Attack", player, options) and state._has_ability("Sword Special", player, options))
        add_rule(world.get_location("The Heart Seeking Bow" + subfix, player), lambda state: \
                state._has_ability("Bow Attack", player, options) and state._has_ability("Bow Special", player, options))
        add_rule(world.get_location("The Eternal Spear" + subfix, player), lambda state: \
                state._has_ability("Spear Attack", player, options) and state._has_ability("Spear Special", player, options))
        add_rule(world.get_location("The Shield Of Chaos" + subfix, player), lambda state: \
                state._has_ability("Shield Attack", player, options) and state._has_ability("Shield Special", player, options))
        add_rule(world.get_location("The Twin Fists" + subfix, player), lambda state: \
                state._has_ability("Fist Attack", player, options) and state._has_ability("Fist Special", player, options))
        add_rule(world.get_location("The Adamant Rail" + subfix, player), lambda state: \
                state._has_ability("Gun Attack", player, options) and state._has_ability("Gun Special", player, options))

    #rule that depends on mirrorsanity
    if options.mirrorsanity:
        add_rule(world.get_location("Dark Reflections" + subfix, player), lambda state:  \
            state._has_all_mirror_talents(player, options))
        
    #rules that depend on trovesanity
    if options.trovesanity:
        add_rule(world.get_location("Infernal Trove in 15 seconds", player), lambda state: \
                state._has_unlocked_troves(player, options))
        add_rule(world.get_location("Infernal Trove in 30 seconds", player), lambda state: \
                state._has_unlocked_troves(player, options))
        add_rule(world.get_location("Infernal Trove in 45 seconds", player), lambda state: \
                state._has_unlocked_troves(player, options))
        add_rule(world.get_location("Infernal Trove in 60 seconds", player), lambda state: \
                state._has_unlocked_troves(player, options))
        add_rule(world.get_location("First Infernal Trove: Tartarus", player), lambda state: \
                state._has_unlocked_troves(player, options))
        add_rule(world.get_location("First Infernal Trove: Asphodel", player), lambda state: \
                state._has_unlocked_troves(player, options) and state._has_defeated_boss("Meg Victory", player, options))
        add_rule(world.get_location("First Infernal Trove: Elysium", player), lambda state: \
                state._has_unlocked_troves(player, options) and state._has_defeated_boss("Lernie Victory", player, options))
        add_rule(world.get_location("First Infernal Trove: Styx", player), lambda state: \
                state._has_unlocked_troves(player, options) and state._has_defeated_boss("Bros Victory", player, options))
        add_rule(world.get_location("5 Infernal Troves", player), lambda state: \
                state._has_unlocked_troves(player, options))
        add_rule(world.get_location("10 Infernal Troves", player), lambda state: \
                state._has_unlocked_troves(player, options))

    if options.keepsakesanity:
        add_rule(world.get_location("Close At Heart" + subfix, player), lambda state: \
                state._has_enough_keepsakes(player, 23, options))
        #This is balancing rules, so grinding gods is less painful
        add_rule(world.get_location("Goddess Of Wisdom" + subfix, player), lambda state: \
                state.has("Athena Keepsake", player))
        add_rule(world.get_location("God Of The Heavens" + subfix, player), lambda state: \
                state.has("Zeus Keepsake", player))
        add_rule(world.get_location("God Of The Sea" + subfix, player), lambda state: \
                state.has("Poseidon Keepsake", player))
        add_rule(world.get_location("Goddess Of Love" + subfix, player), lambda state: \
                state.has("Aphrodite Keepsake", player))
        add_rule(world.get_location("God Of War" + subfix, player), lambda state: \
                state.has("Ares Keepsake", player))
        add_rule(world.get_location("Goddess Of The Hunt" + subfix, player), lambda state: \
                state.has("Artemis Keepsake", player))
        add_rule(world.get_location("God Of Wine" + subfix, player), lambda state: \
                state.has("Dionysus Keepsake", player))
        add_rule(world.get_location("Goddess Of Seasons" + subfix, player), lambda state: \
                state.has("Demeter Keepsake", player))
        
        #Balancing rules
        add_rule(world.get_location("Primordial Boons" + subfix, player), lambda state: \
                state.has("Chaos Keepsake", player))
        add_rule(world.get_location("Primordial Banes" + subfix, player), lambda state: \
                state.has("Chaos Keepsake", player))
        add_rule(world.get_location("Amusing Chaos" + subfix, player), lambda state: \
                state.has("Chaos Keepsake", player))
        add_rule(world.get_location("Sea-God's Spite" + subfix, player), lambda state: \
                state.has("Poseidon Keepsake", player))
        add_rule(world.get_location("War-God's Bloodlust" + subfix, player), lambda state: \
                state.has("Ares Keepsake", player))
        
        #Balacing rules for DivinePairings
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Athena Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Zeus Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Poseidon Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Aphrodite Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Ares Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Artemis Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Dionysus Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Demeter Keepsake", player))
        
    if options.hidden_aspectsanity:
        #balancing for aspects related fates
        add_rule(world.get_location("The Holy Liege" + subfix, player), lambda state: \
                        state.has("Sword Hidden Aspect", player) or options.initial_weapon == 0)
        add_rule(world.get_location("The Preserver's Avatar" + subfix, player), lambda state: \
                        state.has("Bow Hidden Aspect", player) or options.initial_weapon == 1)
        add_rule(world.get_location("The Fated Saint of War" + subfix, player), lambda state: \
                        state.has("Spear Hidden Aspect", player) or options.initial_weapon == 2)
        add_rule(world.get_location("The Dragon's Rival" + subfix, player), lambda state: \
                        state.has("Shield Hidden Aspect", player) or options.initial_weapon == 3)
        add_rule(world.get_location("The God-like King" + subfix, player), lambda state: \
                        state.has("Fist Hidden Aspect", player) or options.initial_weapon == 4)
        add_rule(world.get_location("The Dawn Bringer" + subfix, player), lambda state: \
                        state.has("Gun Hidden Aspect", player) or options.initial_weapon == 5)

    # This is extra balancing rules to avoid fates being a pain in the butt
    add_rule(world.get_location("Primordial Boons" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("Primordial Banes" + subfix, player), lambda state: \
                state._has_defeated_boss("Lernie Victory", player, options))
    add_rule(world.get_location("Primordial Boons" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("Primordial Banes" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    
    add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    
    add_rule(world.get_location("Power Without Equal" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    
    add_rule(world.get_location("Chthonic Colleagues" + subfix, player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))
    add_rule(world.get_location("Customer Loyalty" + subfix, player), lambda state: \
                state._has_defeated_boss("Lernie Victory", player, options))
    
    add_rule(world.get_location("Goddess Of Wisdom" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("God Of The Heavens" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("God Of The Sea" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("Goddess Of Love" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("God Of War" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("Goddess Of The Hunt" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("God Of Wine" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("God Of Swiftness" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("Goddess Of Seasons" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    
    add_rule(world.get_location("The Stygian Blade" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("The Heart Seeking Bow" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("The Eternal Spear" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("The Shield Of Chaos" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("The Twin Fists" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    add_rule(world.get_location("The Adamant Rail" + subfix, player), lambda state: \
                state._has_all_approval_process(player, options))
    
    add_rule(world.get_location("End to Torment" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("Divided by Death" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("Eternal Rest" + subfix, player), lambda state: \
                state._has_defeated_boss("Lernie Victory", player, options))
    add_rule(world.get_location("A Place of Revelry" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("Amusing Chaos" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("Sea-God's Spite" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("War-God's Bloodlust" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("A Friendly Wager" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    add_rule(world.get_location("The Gift of Song" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    
    #balancing for aspects related fates
    add_rule(world.get_location("The Holy Liege" + subfix, player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))
    add_rule(world.get_location("The Fated Saint of War" + subfix, player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))
    add_rule(world.get_location("The Preserver's Avatar" + subfix, player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))
    add_rule(world.get_location("The Dragon's Rival" + subfix, player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))
    add_rule(world.get_location("The God-like King" + subfix, player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))
    add_rule(world.get_location("The Dawn Bringer" + subfix, player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))

def set_weapon_region_rules(world: "HadesWorld", player: int, number_items: int, 
                            location_table : list, options, weaponSubfix: str, 
                            total_routine_inspection: int) -> None:
    add_rule(world.get_entrance("Zags room " + weaponSubfix, player), lambda state: \
            state._has_weapon(weaponSubfix, player, options))
    add_rule(world.get_entrance("Exit Tartarus " + weaponSubfix, player), lambda state: \
            state.has("Meg Victory " + weaponSubfix, player) and \
            state._total_heat_level(player, min(math.floor(number_items / 4), 10), options) and \
            state._has_enough_routine_inspection(player, total_routine_inspection - 2, options) and \
            state._has_enough_weapons(player, options, 2) and \
            state.has("Dash", player) and \
            state._has_attack_special_pairs(player, options, 1) and \
            state._has_enough_mirror_levels(math.floor(TOTAL_MIRROR_ITEMS/4), player, options))
    add_rule(world.get_entrance("Exit Asphodel " + weaponSubfix, player), lambda state: \
            state.has("Lernie Victory " + weaponSubfix, player) and \
            state._total_heat_level(player, min(math.floor(number_items / 2), 20), options) and \
            state._has_enough_routine_inspection(player, total_routine_inspection - 1, options) and \
            state._has_enough_weapons(player, options, 3) and \
            state._has_required_ability_progression(player, options, 2) and \
            state._has_attack_special_pairs(player, options, 2) and \
            state._has_enough_mirror_levels(math.floor(TOTAL_MIRROR_ITEMS/2), player, options))
    add_rule(world.get_entrance("Exit Elysium " + weaponSubfix, player), lambda state: \
            state.has("Bros Victory " + weaponSubfix, player)  and \
            state._total_heat_level(player, min(math.floor(number_items * 3 / 4), 30), options) and \
            state._has_enough_routine_inspection(player, total_routine_inspection, options) and \
            state._has_enough_weapons(player, options, 5) and \
            state._has_required_ability_progression(player, options, 3) and \
            state._has_attack_special_pairs(player, options, 3) and \
            state._has_enough_mirror_levels(math.floor(3*TOTAL_MIRROR_ITEMS/4), player, options))
    add_rule(world.get_location("Beat Hades " + weaponSubfix, player), lambda state: \
            state._total_heat_level(player, min(number_items, 35), options) and \
            state._has_enough_weapons(player, options, 6) and \
            state._has_required_ability_progression(player, options, 4) and \
            state._has_attack_special_pairs(player, options, 4) and \
            state._has_enough_mirror_levels(TOTAL_MIRROR_ITEMS, player, options))

def set_mirror_rules(world: "HadesWorld", player: int, options) -> None:
    for upgrade in mirror_upgrades:
        required_ri = 5 - mirror_ri_requirements.get(upgrade.name, 0)
        total_ri = int(options.routine_inspection_pact_amount.value)
        required_ri = min(required_ri, total_ri)

        for level in range(1, upgrade.max_level + 1):
                location_name = f"Mirror {upgrade.name} - Level {level}"

                # in the minimal heat/routine inspection case, we removed some locations and want to make sure they're no longer counted
                try:
                        location = world.get_location(location_name, player)
                except KeyError:
                        continue


                add_rule(world.get_location(location_name, player), lambda state, lvl=level, max_lvl=upgrade.max_level: \
                        state._can_reach_mirror_rank(lvl, max_lvl, player, options))
                if required_ri > 0:
                        add_rule(world.get_location(location_name, player), lambda state, ri=required_ri: \
                                state._has_enough_routine_inspection(player, ri, options))
                        


def set_fishing_rules(world: "HadesWorld", player: int, options) -> None:

    # Rod required for everything
    fish_locations = [
        "Catch Hellfish",
        "Catch Knucklehead",
        "Catch Scyllascion",
        "Catch Slavug",
        "Catch Chrustacean",
        "Catch Flameater",
        "Catch Chlam",
        "Catch Charp",
        "Catch Seamare",
        "Catch Gupp",
        "Catch Scuffer",
        "Catch Stonewhal",
        "Catch Mati",
        "Catch Projelly",
        "Catch Voidskate",
    ]
    if options.fishsanity.value == 2:
        fish_locations.extend([
        "Catch Trout",
        "Catch Bass",
        "Catch Sturgeon",
    ])

    for location in fish_locations:
        add_rule(world.get_location(location, player), lambda state: state._has_fishing_rod(player, options))

    add_rule(world.get_location("Catch Slavug", player), lambda state: \
            state._has_defeated_boss("Meg Victory", player, options))
    add_rule(world.get_location("Catch Chrustacean", player), lambda state: \
            state._has_defeated_boss("Meg Victory", player, options))
    add_rule(world.get_location("Catch Flameater", player), lambda state: \
            state._has_defeated_boss("Meg Victory", player, options))
    add_rule(world.get_location("Catch Chlam", player), lambda state: \
            state._has_defeated_boss("Lernie Victory", player, options))
    add_rule(world.get_location("Catch Charp", player), lambda state: \
            state._has_defeated_boss("Lernie Victory", player, options))
    add_rule(world.get_location("Catch Seamare", player), lambda state: \
            state._has_defeated_boss("Lernie Victory", player, options))
    add_rule(world.get_location("Catch Gupp", player), lambda state: \
            state._has_defeated_boss("Bros Victory", player, options))
    add_rule(world.get_location("Catch Scuffer", player), lambda state: \
            state._has_defeated_boss("Bros Victory", player, options))
    add_rule(world.get_location("Catch Stonewhal", player), lambda state: \
            state._has_defeated_boss("Bros Victory", player, options))
    if options.fishsanity.value == 2:
        add_rule(world.get_location("Catch Trout", player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
        add_rule(world.get_location("Catch Bass", player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
        add_rule(world.get_location("Catch Sturgeon", player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))


def forbid_important_items_on_late_styx(world: "HadesWorld", player: int, options) -> None:
    if options.location_system == "room_weapon_based":
        for weaponString in location_weapons_subfixes:
                late_styx_region = world.get_region("Styx Late " + weaponString, player)
                for location in late_styx_region.locations:
                        add_item_rule(location,
                                lambda item: not item.advancement or item_is_plando(world, item, player, options))
    else:
        late_styx_region = world.get_region("Styx Late", player)
        for location in late_styx_region.locations:
                add_item_rule(location,
                        lambda item: not item.advancement or item_is_plando(world, item, player, options))
                

def item_is_plando(world: "HadesWorld", item: Item, player: int, options) -> bool:
    return item in [plando_item for block in options.plando_items for plando_item in block.items]