from typing import TYPE_CHECKING
import logging

from BaseClasses import CollectionState
from .data.logic.Requirement import Requirement
from .Items import valid_item_names, placeholder_names

if TYPE_CHECKING:
    from worlds.metroidfusion import MetroidFusionOptions

class LogicObject:
    requirements: list[set[str]] = []
    energy_tanks: list[int] = []
    missile_ammo: list[int] = []
    power_bomb_ammo: list[int] = []
    yaml_enabled: list[bool] = []
    calculated_energy_tanks: int = 0
    player: int
    options: "MetroidFusionOptions"

    def __init__(self, player: int, options: "MetroidFusionOptions"):
        self.player = player
        self.options = options

    def logic_rule(self, state: CollectionState) -> bool:
        if not self.requirements:
            return True
        if self.yaml_enabled and not any(self.yaml_enabled):
            return False
        expression = None
        for (requirement_list,
             energy_tanks_value,
             missile_ammo_value,
             power_bomb_ammo_value,
             yaml_enabled_flag) in zip(self.requirements,
                                       self.energy_tanks,
                                       self.missile_ammo,
                                       self.power_bomb_ammo,
                                       self.yaml_enabled):
            # Remove placeholder values in item list and re-validate
            requirement_list -= placeholder_names
            assert all([item in valid_item_names for item in requirement_list]), \
                f"Invalid item name in: {requirement_list}"
            if energy_tanks_value > 0:
                if self.options.ElevatorShuffle.value > self.options.ElevatorShuffle.option_none:
                    energy_tanks_value = energy_tanks_value // 2
                if self.options.CombatDifficulty >= self.options.CombatDifficulty.option_expert:
                    energy_tanks_value = energy_tanks_value // 2
            if missile_ammo_value > 0:
                match self.options.CombatDifficulty.value:
                    case self.options.CombatDifficulty.option_beginner:
                        missile_ammo_value = -int(-(missile_ammo_value * 1.25) // 1)
                    case self.options.CombatDifficulty.option_advanced:
                        missile_ammo_value = -int(-(missile_ammo_value * 1.1) // 1)
                missile_ammo_value -= self.options.MissileDataAmmo.value
                if self.options.MissileTankAmmo.value > 0:
                    missile_ammo_value = -int(-(missile_ammo_value / self.options.MissileTankAmmo.value) // 1)
            if power_bomb_ammo_value > 0:
                power_bomb_ammo_value -= self.options.PowerBombDataAmmo.value
                if self.options.PowerBombTankAmmo.value > 0:
                    power_bomb_ammo_value = -int(-(power_bomb_ammo_value / self.options.PowerBombTankAmmo.value) // 1)
            if expression is None:
                expression = (state.has_all(requirement_list, self.player)
                              and state.has("Energy Tank", self.player, energy_tanks_value)
                              and state.has("Missile Tank", self.player, missile_ammo_value)
                              and state.has("Power Bomb Tank", self.player, power_bomb_ammo_value)
                              and yaml_enabled_flag)
            else:
                expression = (expression
                              or state.has_all(requirement_list, self.player)
                              and state.has("Energy Tank", self.player, energy_tanks_value)
                              and state.has("Missile Tank", self.player, missile_ammo_value)
                              and state.has("Power Bomb Tank", self.player, power_bomb_ammo_value)
                              and yaml_enabled_flag)
        return expression



def create_logic_rule_for_list(
        requirements: list[Requirement],
        options: "MetroidFusionOptions",
        debug: bool = False) -> tuple[list[set[str]], list[int], list[int], list[int], list[bool]]:
    if debug:
        print("Create logic rule for list...")
        logging.info("Create logic rule for list...")
    r_e_m_p_y: tuple[list[set[str]], list[int], list[int], list[int], list[bool]] = ([], [], [], [], [])
    for requirement in requirements:
        for (new_rule,
             energy_tanks_in_rule,
             missile_ammo_in_rule,
             power_bomb_ammo_in_rule,
             yaml_enabled) in create_logic_rule(requirement, options, debug):
            r_e_m_p_y[0].append(new_rule)
            r_e_m_p_y[1].append(energy_tanks_in_rule)
            r_e_m_p_y[2].append(missile_ammo_in_rule)
            r_e_m_p_y[3].append(power_bomb_ammo_in_rule)
            r_e_m_p_y[4].append(yaml_enabled)
    if debug:
        for (requirement,
             energy_tanks,
             missiles,
             power_bombs,
             yaml_enabled) in zip(*r_e_m_p_y):
            debug_string = ("Logic rule:"
                            f"\nRequirements: {requirement}"
                            f"\nEnergy Tanks: {energy_tanks}"
                            f"\nMissiles: {missiles}"
                            f"\nPower Bombs: {power_bombs}"
                            f"\nEnabled: {yaml_enabled}"
                            "\n===\n")
            print(debug_string)
            logging.info(debug_string)
    return r_e_m_p_y

def create_logic_rule(
        requirement: Requirement,
        options: "MetroidFusionOptions",
        debug: bool = False) -> list[tuple[set[str], int, int, int, bool]]:
    possibilities: list[tuple[set[str], int, int, int, bool]] = requirement.unpack(options, debug=debug)
    # Validate all item names in possibilities before proceeding
    assert all([item_needed in valid_item_names
                for possibility in possibilities
                for item_needed in possibility[0]]), requirement
    if debug:
        sub_requirements_debug_string = [
            (f"\t({requirements_list},\n"
             f"\t\tEnergy Tanks: {energy_tanks},\n"
             f"\t\tMissiles: {missiles},\n"
             f"\t\tPower Bombs: {power_bombs},\n"
             f"\t\tEnabled: {yaml_enabled})")
            for requirements_list, energy_tanks, missiles, power_bombs, yaml_enabled in possibilities
        ]
        debug_string = ("Create logic rule...\n"
                        f"Requirement: {requirement.name}\n"
                        f"Item Possibilities: [\n{",\n".join(sub_requirements_debug_string)}\n]\n"
                        f"Enabled: {requirement.check_option_enabled(options)}")
        print(debug_string)
        logging.info(debug_string)
    return possibilities