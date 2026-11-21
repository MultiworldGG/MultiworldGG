from collections import defaultdict
from unittest import TestCase

from ..character_ability import *
from ..data.items.all_character_items import NORMAL_CHARACTER_TO_ITEM_DATA


class TestAbilities(TestCase):
    implied_abilities_dict: dict[CharacterAbility, CharacterAbility]
    implied_by_abilities_dict: dict[CharacterAbility, CharacterAbility]
    ability_to_used_by: dict[CharacterAbility, frozenset[CharacterAbility]]
    unused_abilities: CharacterAbility

    @classmethod
    def setUpClass(cls):
        implied_dict: dict[CharacterAbility, CharacterAbility] = {ability: ~ability for ability in CharacterAbility}

        ability_to_used_by: dict[CharacterAbility, set[CharacterAbility]] = defaultdict(set)
        used_abilities = CharacterAbility.NONE
        for character_data in NORMAL_CHARACTER_TO_ITEM_DATA.values():
            for ability in character_data.abilities:
                implied_dict[ability] &= character_data.abilities
                used_abilities |= character_data.abilities
                ability_to_used_by[ability].add(character_data.abilities)

        cls.ability_to_used_by = {k: frozenset(ability_to_used_by[k]) for k in CharacterAbility}
        cls.unused_abilities = ~used_abilities

        # The implied_dict relies on at least one character having the ability.
        for ability in cls.unused_abilities:
            implied_dict[ability] = CharacterAbility.NONE

        cls.implied_abilities_dict = implied_dict

        implied_by_dict: dict[CharacterAbility, CharacterAbility] = {
            ability: CharacterAbility.NONE for ability in CharacterAbility
        }
        for ability, implies in implied_dict.items():
            for implied in implies:
                implied_by_dict[implied] |= ability
        cls.implied_by_abilities_dict = implied_by_dict

    @classmethod
    def tearDownClass(cls):
        del cls.implied_abilities_dict

    def test_implied_abilities(self):
        failed = False
        for ability, implied in self.implied_abilities_dict.items():
            with self.subTest(ability.name):
                actual = IMPLIED_ABILITIES.get(ability, CharacterAbility.NONE)
                try:
                    self.assertEqual(implied, actual,
                                     f"Implied abilities for {ability!r} should be"
                                     f"\n\t{implied!r}\nbut were\n\t{actual!r}")
                except AssertionError:
                    failed = True
                    raise
        if failed:
            implied_abilities_lines = [
                "{",
                "    # All characters with this ability: Also have these abilities,",
                "    # HasAllAbilities(left | right) -> HasAbility(left)",
                "    # HasAnyAbilities(left | right) -> HasAbility(right)",
            ]
            for ability, implied in self.implied_abilities_dict.items():
                if implied is CharacterAbility.NONE:
                    implied_name = "CharacterAbility.NONE"
                else:
                    implied_name = implied.name
                    implied_name = implied_name.replace("|", " | ")
                implied_abilities_lines.append(f"    {ability.name}: {implied_name},")
            implied_abilities_lines.append("}")
            lines = "\n".join(implied_abilities_lines)
            self.fail(f"Implied abilities did not match. Expected implied abilities:\n{lines}")

    def test_circular_implications(self):
        for ability, implied in self.implied_abilities_dict.items():
            with self.subTest(ability.name):
                for implied_ability in implied:
                    self.assertNotIn(ability, self.implied_abilities_dict[implied_ability],
                                     f"Circular implication of {ability.name} and {implied_ability.name}")

    def test_no_unused_abilities(self):
        self.assertIs(self.unused_abilities, CharacterAbility.NONE)

    def abilities_tup_gen(self, to_gen_from: CharacterAbility, r_max: int):
        """
        itertools.combinations, but with pre-filtering for known bad cases.
        If A, B are pointless, then A, B, C won't be tried.
        """
        if r_max < 2:
            raise ValueError(f"r_max must be at least 2, but got {r_max}")
        tup_list = [(c, self.implied_abilities_dict[c]) for c in to_gen_from]

        def abilities_tup_gen_recur(
                start_offset: int,
                last_v: CharacterAbility,
                last_v_implies: CharacterAbility,
                recursion_depth_remaining: int):
            for i in range(start_offset, len(to_gen_from)):
                v, v_implies = tup_list[i]
                # Reduce the search space by skipping cases where one already seen abilities imply another ability.
                # e.g. JEDI is implied_by SITH, so skip combinations involving SITH and JEDI.
                if v in last_v_implies or (last_v & v_implies is not CharacterAbility.NONE):
                    continue
                # PyCharm being dumb. The outermost parenthesis are required.
                # noinspection PyRedundantParentheses
                yield (combined := (last_v | v))
                if recursion_depth_remaining > 0:
                    combined_implies = v_implies | last_v_implies
                    yield from abilities_tup_gen_recur(i + 1, combined, combined_implies,
                                                       recursion_depth_remaining - 1)
        yield from abilities_tup_gen_recur(0, CharacterAbility.NONE, CharacterAbility.NONE, r_max - 1)

    def test_pair_reductions(self):

        reductions: dict[CharacterAbility, CharacterAbility] = {}

        for ability_main, implied_by in self.implied_by_abilities_dict.items():
            relevant_abilities = implied_by

            # At least 2 abilities are needed for a reduction to be possible.
            if relevant_abilities.value.bit_count() < 2:
                continue

            # Do all characters with ability_main have either ability_a or ability_b?
            # Do all HAS_DOUBLE_JUMP characters have either JEDI or HIGH_JUMP? (yes)
            # Do all HAS_DOUBLE_JUMP characters have either JEDI or SITH? (no, there are HIGH_JUMP that are neither)
            # I honestly doubt anything above 3 (A | B | C -> D) will ever be used.
            r_max = min(relevant_abilities.value.bit_count() + 1, 5)
            # So many combinations can be reduced to the basic jump height abilities, and most of the combinations are
            # useless, so skip most combinations by reducing the max combination length.
            if ability_main in CharacterAbility.CAN_BARELY_JUMP | CharacterAbility.CAN_JUMP_HEIGHT_0_37:
                r_max = min(r_max, 2)
            for reduced_abilities in self.abilities_tup_gen(relevant_abilities, r_max):
                for user_of_ability_main in self.ability_to_used_by[ability_main]:
                    if not any(reduce_ability in user_of_ability_main for reduce_ability in reduced_abilities):
                        break
                else:
                    if relevant_abilities in reductions:
                        # If this happens, we'll need to figure something out.
                        raise AssertionError(f"Duplicate reduction for {reduced_abilities.name}."
                                             f" It reduces to both {reductions[reduced_abilities].name}"
                                             f" and {ability_main.name}")
                    reductions[reduced_abilities] = ability_main

        all_keys = set(reductions.keys()) | set(ABILITY_REDUCTIONS.keys())
        for key in sorted(all_keys):
            with self.subTest(key.name):
                calculated = reductions.get(key)
                defined = ABILITY_REDUCTIONS.get(key)
                self.assertEqual(calculated,
                                 defined,
                                 f"Failed to tell that {key.name} can be reduced to {calculated.name}"
                                 if calculated is not None
                                 else f"No reduction should be defined for {key.name}, but a reduction to"
                                      f" {defined.name} is defined.")

    def test_combination_reductions(self):
        combination_reductions: dict[CharacterAbility, CharacterAbility] = {}
        characters_with_combination_anded_bits: dict[CharacterAbility, CharacterAbility] = {}
        for ability, implies in self.implied_abilities_dict.items():
            for combination in self.abilities_tup_gen(implies, 7):
                if combination.bit_count() == 1:
                    continue

                if combination in characters_with_combination_anded_bits:
                    anded_abilities = characters_with_combination_anded_bits[combination]
                else:
                    anded_abilities = ~CharacterAbility.NONE
                    characters = set().union(*(self.ability_to_used_by[part] for part in combination))
                    for character in characters:
                        if combination in character:
                            anded_abilities &= character
                    if anded_abilities is ~CharacterAbility.NONE:
                        self.fail(f"Ability combination {combination!r} is not used by any characters. This should not"
                                  f" happen because the only checked combinations are those that are implied by another"
                                  f" ability.")
                    characters_with_combination_anded_bits[combination] = anded_abilities

                if ability in anded_abilities:
                    # All characters with `combination` have `ability`.
                    # (and all characters with `ability` have `combination` because `ability` implies `combination`)
                    if combination in combination_reductions:
                        self.fail(f"{combination!r} already reduces to {combination_reductions[combination]!r}, but"
                                  f" tried to mark it as reducing to {ability!r}")
                    combination_reductions[combination] = ability

        if combination_reductions != COMBINATION_ABILITY_REDUCTIONS:
            expected_str_lines = [
                "{",
                "    # 1) All characters with this combination: 2) Have this ability.",
                "    # 2) Have these abilities: 1) All characters with this ability.",
                "    # HasAbilityCombination(A | B) can be reduced to HasAbility(C).",
            ]
            for combination, reduced_to in combination_reductions.items():
                combination_name = combination.name
                combination_name = combination_name.replace("|", " | ")
                expected_str_lines.append(f"    {combination_name}: {reduced_to.name},")
            expected_str_lines.append("}")
            expected_str = "\n".join(expected_str_lines)
            self.fail(f"Combination ability reductions did not match. Was expecting:\n{expected_str}")

    def test_pair_reductions_bits(self):
        """The keys in ABILITY_REDUCTIONS need to be sorted by most bits first because they are iterated in order. If a
        reduction that is contained by another reduction were to be run first, additional .simplify_or() steps would be
        needed following the pair reductions, which could then additionally have more pair reductions, which could then
        have more .simplify_or() steps etc."""
        last_bits = 999_999_999
        for ability in ABILITY_REDUCTIONS.keys():
            self.assertLessEqual(ability.bit_count(), last_bits)
            last_bits = ability.bit_count()

    def test_optimize_and_has_any(self):
        cases: list[tuple[set[CharacterAbility], set[CharacterAbility], str]] = [
            ({BOUNTY_HUNTER, BOUNTY_HUNTER},
             {BOUNTY_HUNTER},
             "Duplicates are deduplicated"),

            ({BOUNTY_HUNTER | ASTROMECH_PANEL, BOUNTY_HUNTER | ASTROMECH_PANEL},
             {BOUNTY_HUNTER | ASTROMECH_PANEL},
             "Duplicates are deduplicated"),

            ({BOUNTY_HUNTER, GRAPPLE},
             {BOUNTY_HUNTER},
             "Whenever BOUNTY_HUNTER is satisfied, GRAPPLE will also be satisfied"),

            ({BOUNTY_HUNTER | GRAPPLE},
             {GRAPPLE},
             "Standalone HasAnyAbilities simplify_or optimization applies"),

            ({BOUNTY_HUNTER | ASTROMECH_PANEL, GRAPPLE | ASTROMECH_PANEL},
             {BOUNTY_HUNTER | ASTROMECH_PANEL},
             "Whenever BOUNTY_HUNTER | ASTROMECH_PANEL is satisfied, GRAPPLE | ASTROMECH_PANEL will also be satisfied"),

            ({BOUNTY_HUNTER | ASTROMECH_PANEL | JEDI, GRAPPLE | ASTROMECH_PANEL},
             {BOUNTY_HUNTER | ASTROMECH_PANEL | JEDI, GRAPPLE | ASTROMECH_PANEL},
             "No optimisation possible"),

            ({BOUNTY_HUNTER, JEDI, HIGH_JUMP},
             {BOUNTY_HUNTER, JEDI, HIGH_JUMP},
             "No optimisation possible"),

            ({BOUNTY_HUNTER | JEDI, GRAPPLE | CAN_DOUBLE_JUMP},
             {BOUNTY_HUNTER | JEDI},
             "GRAPPLE is implied by BOUNTY_HUNTER, and CAN_DOUBLE_JUMP is implied by JEDI"),

            ({BOUNTY_HUNTER | JEDI, GRAPPLE | CAN_DOUBLE_JUMP | CAN_MELEE},
             {BOUNTY_HUNTER | JEDI},
             "GRAPPLE is implied by BOUNTY_HUNTER, CAN_DOUBLE_JUMP is implied by JEDI, and CAN_MELEE is implied by"
             " both"),

            ({BOUNTY_HUNTER | JEDI | HIGH_JUMP, CAN_HIGH_JUMP_SLAM},
             {CAN_HIGH_JUMP_SLAM},
             "CAN_HIGH_JUMP_SLAM is implied by HIGH_JUMP, so for CAN_HIGH_JUMP_SLAM to be satisfied,"
             " BOUNTY_HUNTER | JEDI | HIGH_JUMP will also always be satisfied"),
        ]
        for and_has_any, expected, name in cases:
            with self.subTest(name, and_has_any=and_has_any):
                optimized = CharacterAbility.optimize_and_has_any_abilities(and_has_any)
                self.assertEqual(optimized, expected)

    def test_optimize_ar_has_all(self):
        cases: list[tuple[set[CharacterAbility], set[CharacterAbility], str]] = [
            ({BOUNTY_HUNTER, BOUNTY_HUNTER},
             {BOUNTY_HUNTER},
             "Duplicates are deduplicated"),

            ({BOUNTY_HUNTER | ASTROMECH_PANEL, BOUNTY_HUNTER | ASTROMECH_PANEL},
             {BOUNTY_HUNTER | ASTROMECH_PANEL},
             "Duplicates are deduplicated"),

            ({BOUNTY_HUNTER, GRAPPLE},
             {GRAPPLE},
             "Whenever BOUNTY_HUNTER is satisfied, GRAPPLE will also be satisfied"),

            ({BOUNTY_HUNTER | GRAPPLE},
             {BOUNTY_HUNTER},
             "Standalone HasAnyAbilities simplify_and optimization applies"),

            ({BOUNTY_HUNTER | ASTROMECH_PANEL, GRAPPLE | ASTROMECH_PANEL},
             {GRAPPLE | ASTROMECH_PANEL},
             "Whenever BOUNTY_HUNTER & ASTROMECH_PANEL is satisfied, GRAPPLE & ASTROMECH_PANEL will also be satisfied"),

            ({BOUNTY_HUNTER | ASTROMECH_PANEL | JEDI, GRAPPLE | ASTROMECH_PANEL},
             {GRAPPLE | ASTROMECH_PANEL},
             "Whenever BOUNTY_HUNTER & ASTROMECH_PANEL & JEDI is satisfied, GRAPPLE & ASTROMECH_PANEL will also be"
             " satisfied"),

            ({BOUNTY_HUNTER, JEDI, HIGH_JUMP},
             {BOUNTY_HUNTER, JEDI, HIGH_JUMP}, #should become CAN_DOUBLE_JUMP?
             "No optimisation possible"),

            ({BOUNTY_HUNTER | JEDI, GRAPPLE | CAN_DOUBLE_JUMP},
             {GRAPPLE | CAN_DOUBLE_JUMP},
             "GRAPPLE is implied by BOUNTY_HUNTER, and CAN_DOUBLE_JUMP is implied by JEDI"),

            ({BOUNTY_HUNTER | JEDI, GRAPPLE | CAN_DOUBLE_JUMP | CAN_MELEE},
             {GRAPPLE | CAN_DOUBLE_JUMP | CAN_MELEE},
             "GRAPPLE is implied by BOUNTY_HUNTER, CAN_DOUBLE_JUMP is implied by JEDI, and CAN_MELEE is implied by"
             " both"),

            ({BOUNTY_HUNTER | JEDI | HIGH_JUMP, CAN_HIGH_JUMP_SLAM},
             {BOUNTY_HUNTER | JEDI | HIGH_JUMP, CAN_HIGH_JUMP_SLAM},
             "No optimisation possible"),
        ]
        for or_has_all, expected, name in cases:
            with self.subTest(name, or_has_all=or_has_all):
                optimized = CharacterAbility.optimize_or_has_all_abilities(or_has_all)
                self.assertEqual(optimized, expected)

    def test_convert_or_has_all_to_and_has_any(self):
        cases: list[tuple[list[CharacterAbility], set[CharacterAbility], str]] = [
            ([BOUNTY_HUNTER | JEDI | HIGH_JUMP],
             {JEDI, BOUNTY_HUNTER, HIGH_JUMP},
             "1"),
            ([BOUNTY_HUNTER, JETPACK, ASTROMECH_DROID],
             {BOUNTY_HUNTER | ASTROMECH_DROID},
             "2"),
            ([BOUNTY_HUNTER | JEDI | HIGH_JUMP, CAN_HIGH_JUMP_SLAM],
             {JEDI | CAN_HIGH_JUMP_SLAM, BOUNTY_HUNTER | CAN_HIGH_JUMP_SLAM, HIGH_JUMP},
             "3"),
            ([BLASTER, WEAPON_EWOK | CAN_DOUBLE_JUMP],
             {BLASTER | CAN_DOUBLE_JUMP, BLASTER | WEAPON_EWOK},
             "4"),
            ([BLASTER | CAN_BUILD_BRICKS, WEAPON_EWOK | CAN_DOUBLE_JUMP],
             {CAN_BUILD_BRICKS, BLASTER | CAN_DOUBLE_JUMP, BLASTER | WEAPON_EWOK},
             "5"),
        ]
        for or_has_all, expected, name in cases:
            with self.subTest(name, or_has_all=or_has_all):
                and_has_any = CharacterAbility.convert_or_has_all_to_and_has_any(*or_has_all)
                self.assertEqual(and_has_any, expected)

    def test_convert_and_has_any_to_or_has_all(self):
        cases: list[tuple[list[CharacterAbility], set[CharacterAbility], str]] = [
            ([JEDI | JETPACK | ASTROMECH_DROID],
             {JEDI, HOVER},
             "1"),
            ([BOUNTY_HUNTER, JEDI, HIGH_JUMP],
             {BOUNTY_HUNTER | HIGH_JUMP | JEDI},
             "2"),
            ([BOUNTY_HUNTER | JEDI | HIGH_JUMP, CAN_HIGH_JUMP_SLAM],
             {CAN_HIGH_JUMP_SLAM},
             "3"),
            ([BLASTER, WEAPON_EWOK | CAN_DOUBLE_JUMP],
             {BLASTER | WEAPON_EWOK, BLASTER | CAN_DOUBLE_JUMP},
             "4"),
            ([BLASTER | CAN_BUILD_BRICKS, WEAPON_EWOK | CAN_DOUBLE_JUMP],
             {WEAPON_EWOK, CAN_BUILD_BRICKS | CAN_DOUBLE_JUMP, BLASTER | CAN_DOUBLE_JUMP},
             "5"),
        ]
        for and_has_any, expected, name in cases:
            with self.subTest(name, or_has_all=and_has_any):
                and_has_any = CharacterAbility.convert_and_has_any_to_or_has_all(*and_has_any)
                self.assertEqual(and_has_any, expected)