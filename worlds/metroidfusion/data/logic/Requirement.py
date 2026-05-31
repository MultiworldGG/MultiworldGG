from typing import TYPE_CHECKING, Self
from abc import ABC, abstractmethod

from itertools import product as itertools_product
import logging

if TYPE_CHECKING:
    from ... import MetroidFusionOptions


class RequirementBase(ABC):
    """
    Defines a set of requirements for a Connection or Location.

    The parameters are unpacked into a series of logical requirements where all housed in ``items_needed`` and
    one each of entries in each list housed in ``requirements`` must be met for this Requirement to be passed.

    Requirements logic is: (list1 AND list2 AND list3...)
    where (list_requirement1 OR list_requirement2 OR list_requirement3...)

    If there are any ``hard_items_needed``,
    the end possibilities that do not contain all of these items will be removed.

    :param name: A String to label this Requirement. Defaults to the class name.
    :param items_needed: A set of items as Strings. Defaults to an empty set.
    :param hard_items_needed: A set of items as Strings. Defaults to an empty set.
    :param energy_tanks_needed: An integer number of energy tanks required. Defaults to 0.
    :param missile_ammo_needed: An integer number of missiles required. Defaults to 0.
    :param power_bomb_ammo_needed: An integer number of power bombs required. Defaults to 0.
    :param requirements: A list of lists of Requirement objects. Defaults to an empty list.
    """
    name: str
    items_needed: set[str]
    hard_items_needed: set[str]
    energy_tanks_needed: int
    missile_ammo_needed: int
    power_bomb_ammo_needed: int
    requirements: list[list[Self]]

    @abstractmethod
    def __init__(self,
                 name: str = None,
                 items_needed: set[str] = None,
                 hard_items_needed: set[str] = None,
                 energy_tanks_needed: int = 0,
                 missile_ammo_needed: int = 0,
                 power_bomb_ammo_needed: int = 0,
                 *requirements: list[Self],
                 **kwargs):
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name
        if items_needed is None:
            items_needed = set()
        self.items_needed = items_needed
        if hard_items_needed is None:
            hard_items_needed = set()
        self.hard_items_needed = hard_items_needed
        self.requirements = [requirement for requirement in requirements]
        self.energy_tanks_needed = energy_tanks_needed
        self.missile_ammo_needed = missile_ammo_needed
        self.power_bomb_ammo_needed = power_bomb_ammo_needed

    def __repr__(self):
        return_string = f"Name: {self.name}\n"
        return_string += f"ItemsNeeded: [{', '.join(self.items_needed)}]\n"
        return_string += f"HardItemsNeeded: [{', '.join(self.hard_items_needed)}]\n"
        return_string += f"EnergyTanks: {self.energy_tanks_needed}\n"
        return_string += f"MissileAmmo: {self.missile_ammo_needed}\n"
        return_string += f"PowerBombAmmo: {self.power_bomb_ammo_needed}\n"
        return_string += "Requirements: ["
        if self.requirements:
            return_string += f"\n\t[{', '.join(req.name for req_list in self.requirements for req in req_list)}]"
            return_string += "\n]"
        else:
            return_string += "]"
        return return_string

    def __str__(self):
        return self.__repr__()

    def unpack(self,
               options: "MetroidFusionOptions",
               **kwargs) -> list[tuple[set[str], int, int, int, bool]]:
        """
        Unpacks this Requirement into a digestible list of possibilities able to be used by the logic interpreter.

        All ``kwargs`` are overrides for initial values. Do not set keywords if you don't know what you are doing.

        :param options: A dict of options defined in the AP YAML settings
        :key debug: A bool to enable/disable printing debug messages.
            Defaults to False.
        :key possibilities: A list of tuples each containing a set of items, energy tanks, missiles, power bombs, and
            if this is enabled by ``options``. This is the eventual return value. Defaults to an empty list.
        :key parent_items: A set of item names.
            Will default to this Requirement's ``items_needed``
        :key parent_hard_items: A set of item names.
            Will default to this Requirement's ``hard_items_needed``
        :key parent_energy_tanks: An int of energy tanks.
            Will default to this Requirement's ``energy_tanks_needed``
        :key parent_missile_ammo: An int of missile ammo.
            Will default to this Requirement's ``missile_ammo_needed``
        :key parent_power_bomb_ammo: An int of power bomb ammo.
            Will default to this Requirement's ``power_bomb_ammo_needed``
        :key yaml_enabled: A bool to override the YAML settings.
            Defaults to this Requirement's ``check_option_enabled()``
        :return: A list of tuples each containing a set of items, energy tanks, missiles, power bombs, and
            if this is enabled by ``options``
        """

        # Initialize variables
        possibilities: list[tuple[set[str], int, int, int, bool]] = kwargs.pop("possibilities", [])
        yaml_enabled: bool = kwargs.pop("yaml_enabled", self.check_option_enabled(options))
        debug: bool = kwargs.pop("debug", False)
        parent_items: set[str] = kwargs.pop("parent_items", self.items_needed)
        parent_hard_items: set[str] = kwargs.pop("parent_hard_items", self.hard_items_needed)
        parent_energy_tanks: int = kwargs.pop("parent_energy_tanks", self.energy_tanks_needed)
        parent_missile_ammo: int = kwargs.pop("parent_missile_ammo", self.missile_ammo_needed)
        parent_power_bomb_ammo: int = kwargs.pop("parent_power_bomb_ammo", self.power_bomb_ammo_needed)

        if debug:
            logging.info(f"Requirement {self.name}. "
                         f"Items needed {self.items_needed}. "
                         f"Sub-requirements {self.requirements}. "
                         f"Hard items needed {self.hard_items_needed}. "
                         f"Possibilities {possibilities}. "
                         f"Parent items {set() 
                         if parent_items is self.items_needed 
                         else parent_items}. "
                         f"Parent hard items {set() 
                         if parent_hard_items is self.hard_items_needed 
                         else parent_hard_items}. "
                         f"Parent Energy Tanks Needed {parent_energy_tanks}. "
                         f"Parent Missile Ammo {parent_missile_ammo}. "
                         f"Parent Power Bomb Ammo {parent_power_bomb_ammo}.")

        if self.requirements:
            # Create list of permutations of sub-requirements
            requirements_product: list[list[Requirement]] = list(itertools_product(*self.requirements))
            for requirements_permutation in requirements_product:
                if debug:
                    print(f"Evaluating permutation: ["
                          f"{self.name}, {", ".join(nested_requirement.name
                                       for nested_requirement in requirements_permutation)}]")
                    logging.info(f"Evaluating permutation: ["
                          f"{self.name}, {", ".join(nested_requirement.name
                                                    for nested_requirement in requirements_permutation)}]")

                # Check if all requirements in permutation have enabled options
                if not yaml_enabled or any([not nested_requirement.check_option_enabled(options)
                                            for nested_requirement in requirements_permutation]):
                    if debug:
                        print(f"Permutation disabled due to options: ["
                              f"{self.name}, {", ".join(nested_requirement.name
                                                        for nested_requirement in requirements_permutation)}]")
                        logging.info(f"Permutation disabled due to options: ["
                                     f"{self.name}, {", ".join(nested_requirement.name
                                                               for nested_requirement in requirements_permutation)}]")

                # Initialize for recursion
                new_possibilities: list[tuple[set[str], int, int, int, bool]] = []
                for nested_requirement in requirements_permutation:
                    # Recursive unpack
                    and_possibilities = nested_requirement.unpack(
                        options,
                        parent_items=parent_items | self.items_needed,
                        parent_hard_items=parent_hard_items | self.hard_items_needed,
                        parent_energy_tanks=max(parent_energy_tanks, self.energy_tanks_needed),
                        parent_missile_ammo=parent_missile_ammo + self.missile_ammo_needed,
                        parent_power_bomb_ammo=parent_power_bomb_ammo + self.power_bomb_ammo_needed,
                        debug=debug
                    )
                    if new_possibilities:
                        current_new_possibilities = new_possibilities.copy()
                        new_possibilities = [(p[0][0] | p[1][0],
                                              max(p[0][1], p[1][1]),
                                              p[0][2] + p[1][2],
                                              p[0][3] + p[1][3],
                                              p[0][4] and p[1][4])
                                             for p in itertools_product(current_new_possibilities, and_possibilities)]
                    elif not new_possibilities:
                        new_possibilities.extend(and_possibilities)

                # Post-recursion processing
                for (n_r_items, n_r_energy, n_r_missiles, n_r_pbs, n_r_yaml) in new_possibilities:
                    n_r_yaml = n_r_yaml and self.check_option_enabled(options)
                    combined_items = n_r_items | self.items_needed
                    calculated_energy = max(n_r_energy, self.energy_tanks_needed)
                    hard_test: bool = (parent_hard_items.issubset(combined_items)
                                       and self.hard_items_needed.issubset(combined_items))
                    exists_test: bool = \
                        (combined_items, calculated_energy, n_r_missiles, n_r_pbs, n_r_yaml) in possibilities
                    if hard_test and not exists_test:
                        possibilities.append((combined_items, calculated_energy, n_r_missiles, n_r_pbs, n_r_yaml))
                    elif debug:
                        print(f"Skipping Possibility: {combined_items}")
                        logging.info(f"Skipping Possibility: {combined_items}")
                        if not hard_test:
                            print(f"\tDoes not contain all of: {parent_hard_items | self.hard_items_needed}")
                            logging.info(f"\tDoes not contain all of: {parent_hard_items | self.hard_items_needed}")
                        elif exists_test:
                            print(f"\tPossibility already existed when attempting to add to list")
                            logging.info(f"\tPossibility already existed when attempting to add to list")
        else:
            if debug and not yaml_enabled:
                print(f"Requirement {self.name} disabled due to options.")
                logging.info(f"Requirement {self.name} disabled due to options.")
            possibilities.append((parent_items | self.items_needed,
                                  max(parent_energy_tanks, self.energy_tanks_needed),
                                  parent_missile_ammo + self.missile_ammo_needed,
                                  parent_power_bomb_ammo + self.power_bomb_ammo_needed,
                                  yaml_enabled and self.check_option_enabled(options)))
        return possibilities

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return True


class Requirement(RequirementBase):
    """
    Defines a single Requirement to be fulfilled that can contain sub-requirements.

    :param name: The name for this Requirement. Defaults to the class name if not already provided.
    :param requirements: Any number of lists of Requirement objects treated as sub-requirements.
        Each list is treated as an OR logic block.
        If there are more than one list, they are treated as list1 AND list2...

    :key items_needed: A set of items that must be in the inventory.
    :key hard_items_needed: A set of items that are absolutely required to fulfill this Requirement.
        Affects final calculation of possibilities to fulfill this Requirement.
    :key energy_tanks_needed: An integer representing the minimum amount of energy tanks to fulfill this Requirement.
    :key missile_ammo_needed: An integer representing the minimum amount of missile ammo to fulfill this Requirement.
        The final calculation will summate this with all sub-requirements.
    :key power_bomb_ammo_needed: An integer representing the minimum amount of power bomb ammo
        to fulfill this Requirement. The final calculation will summate this with all sub-requirements.
    """

    def __init__(self,
                 name = None,
                 *requirements: list[RequirementBase], **kwargs):
        super().__init__(name,
                         kwargs.pop('items_needed', None),
                         kwargs.pop('hard_items_needed', None),
                         kwargs.pop('energy_tanks_needed', 0),
                         kwargs.pop('missile_ammo_needed', 0),
                         kwargs.pop('power_bomb_ammo_needed', 0),
                         *requirements,
                         **kwargs)


class PONRRequirement(Requirement):
    """
    Defines a set of requirements to be used when Point of No Returns are disabled.
    These should always be more minimal than any surrounding requirements.

    :param name: The name for this Requirement. Defaults to "Point of No Return Requirement"
    :param requirements: Any number of lists of Requirement objects treated as sub-requirements.
        Each list is treated as an OR logic block.
        If there are more than one list, they are treated as list1 AND list2...

    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Point of No Return"}`` or adds that element to the passed set.
    :key hard_items_needed: A set of items that are absolutely required to fulfill this Requirement.
        Affects final calculation of possibilities to fulfill this Requirement.
    :key energy_tanks_needed: An integer representing the minimum amount of energy tanks to fulfill this Requirement.
    :key missile_ammo_needed: An integer representing the minimum amount of missile ammo to fulfill this Requirement.
        The final calculation will summate this with all sub-requirements.
    :key power_bomb_ammo_needed: An integer representing the minimum amount of power bomb ammo
        to fulfill this Requirement. The final calculation will summate this with all sub-requirements.
    """

    def __init__(self,
                 name = "Point of No Return Requirement",
                 *requirements: list[RequirementBase],
                 **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Point of No Return"})
        items_needed.add("Point of No Return")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.PointOfNoReturnsInLogic == True
