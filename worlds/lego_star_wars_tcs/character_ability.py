from enum import auto, IntFlag


__all__ = [
    "CharacterAbility",
    "ASTROMECH_PANEL",
    "BLASTER",
    "GRAPPLE",
    "BOUNTY_HUNTER",
    "HOVER",
    "HIGH_JUMP",
    "IMPERIAL",
    "JEDI",
    "PROTOCOL_PANEL",
    "SHORTIE",
    "SITH",

    "JETPACK",

    "CAN_WEAR_HAT",
    "CAN_WEAR_HAT_AND_GRAPPLE",
    "CAN_WEAR_HAT_AND_DOUBLE_JUMP",
    "CAN_RIDE_VEHICLES",
    "CAN_PULL_LEVERS",
    "CAN_PUSH_OBJECTS",
    "CAN_BUILD_BRICKS",
    "CAN_BARELY_JUMP",
    "CAN_JUMP_HEIGHT_0_37",
    "CAN_JUMP_DISTANCE_0_69",
    "CAN_JUMP_DISTANCE_0_84",
    "CAN_JUMP_DISTANCE_0_92",
    "CAN_REGULAR_DIVE_ROLL",
    "RUN_SPEED_0_9_OR_HIGHER",
    "RUN_SPEED_1_18_OR_HIGHER",
    "CAN_JUMP_0_44",
    "CAN_FLOP_JUMP",
    "CAN_DOUBLE_JUMP",
    "CAN_HIGH_JUMP_SLAM",
    "CAN_TRIPLE_JUMP_GREAT_DISTANCE",
    "CAN_MELEE",
    "CAN_DEFLECT_BOLTS",
    "ASTROMECH_DROID",

    "WEAPON_EWOK",
    "WEAPON_ZAPPER",

    "CAN_SELF_DESTRUCT",
    "CAN_AGGRAVATE_ENEMIES",
    "IS_NON_GHOST_JEDI",
    "TRAINED_JEDI",
    "IS_PASSIVE",

    "IS_A_VEHICLE",
    "FITS_EASILY_THROUGH_VENATOR",
    "VEHICLE_TIE",
    "VEHICLE_TOW",
    "VEHICLE_BLASTER",

    "IMPLIED_ABILITIES",
    "IMPLIED_BY_ABILITIES",
    "ABILITY_REDUCTIONS",
    "COMBINATION_ABILITY_REDUCTIONS",
]


# todo: These are the abilities from the manual logic, not the real abilities.
class CharacterAbility(IntFlag):
    NONE = 0
    ASTROMECH_PANEL = auto()
    # todo: This will eventually need to be split into separate Grapple and Blaster.
    BLASTER = auto()
    GRAPPLE = auto()
    BOUNTY_HUNTER = auto()
    HOVER = auto()
    HIGH_JUMP = auto()
    IMPERIAL = auto()
    JEDI = auto()
    PROTOCOL_PANEL = auto()
    SHORTIE = auto()
    SITH = auto()

    JETPACK = auto()

    # Relevant for some Imperial access and 6-1 Bounty Hunter access.
    CAN_WEAR_HAT = auto()
    # CAN_WEAR_HAT + BLASTER (grapple) on a single character.
    CAN_WEAR_HAT_AND_GRAPPLE = auto()
    # CAN_WEAR_HAT + JEDI on a single character.
    CAN_WEAR_HAT_AND_DOUBLE_JUMP = auto()
    CAN_PULL_LEVERS = auto()
    # All characters that can push objects also can ride vehicles, and vice-versa, so these use the same flag for better
    # performance.
    CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS = auto()
    CAN_RIDE_VEHICLES = CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS
    CAN_PUSH_OBJECTS = CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS  # Blocks and Spinners
    CAN_BUILD_BRICKS = auto()

    CAN_BARELY_JUMP = auto()
    CAN_JUMP_HEIGHT_0_37 = auto()  # Has at least a basic jump height.
    # Note: Every character that can jump a distance less than this is covered by CAN_BARELY_JUMP, except
    # Every character that can jump, except Boba Fett (Boy) [jump_distance=0.56]
    CAN_JUMP_DISTANCE_0_69 = auto()
    # Chewbacca, Han Solo, Padme and a few others have 0.84.
    CAN_JUMP_DISTANCE_0_84 = auto()
    # Storm Troopers, Leia, Luke (non-Jedi) and a few others have 0.92.
    CAN_JUMP_DISTANCE_0_92 = auto()
    # The dive roll does not provide extra height, except Ackbar, who is logically considered to have a double jump
    # instead and is not given this ability. The dive roll is useful for getting extra jump distance, as well as using
    # it to increase air speed enough to slide up some collision that is too tall/sloped to jump up normally.
    CAN_REGULAR_DIVE_ROLL = auto()
    # If a character is too slow, they cannot get past the 2-3 conveyor crushers without jumping around them or using
    # the thin edge of collision along the front edge of the conveyor.
    # run_speed=0.9 is fast enough, run_speed=0.8285375 is too slow and there are no runs speeds inbetween.
    RUN_SPEED_0_9_OR_HIGHER = auto()
    RUN_SPEED_1_18_OR_HIGHER = auto()
    CAN_JUMP_0_44 = auto()
    CAN_FLOP_JUMP = auto()  # Stormtroopers can flop instead dive-rolling, which gets ever so slightly more height.
    CAN_DOUBLE_JUMP = auto()  # Jedi or High Jump

    CAN_HIGH_JUMP_SLAM = auto()  # General Grievous or Grievous' Bodyguard. Only used in Moderate+ Logic.
    CAN_TRIPLE_JUMP_GREAT_DISTANCE = auto()  # General Grievous and Jedi (except Yoda/Yoda(Ghost))

    CAN_MELEE = auto()
    # Not to be confused with being able to reflect bolts, which only Jedi can do.
    # Specifically, this covers characters that can deflect bolts, but cannot shoot bolts, so Droideka is not included.
    CAN_DEFLECT_BOLTS = auto()  # All Jedi, except ghosts, + Captain Tarpals + Grievous' Bodyguard + General Grievous.

    ASTROMECH_DROID = auto()  # This character is an Astromech Droid, relevant to Dagobah and sometimes P2's AI.
    CAN_SELF_DESTRUCT = auto()  # Most droids, but not 4-LOM and IG-88.
    # Can this character cause enemy AI to attack them? Passive characters, ghost characters, and neutral characters
    # without weapons cannot cause enemy AI to attack them. This is relevant for the Deflect Bolts extra.
    # Ugnaught and Jawa cannot aggravate enemies, unless they have Super Zapper, but this only works on Droids is only
    # relevant in 3-4 where there are both Droids and Clones
    CAN_AGGRAVATE_ENEMIES = auto()
    # Ghost Jedi on their cannot be used to reflect blaster bolts, such as at the start of 1-6 because enemies will not
    # shoot at them in the first place to allow reflecting blaster bolts.
    IS_NON_GHOST_JEDI = auto()
    TRAINED_JEDI = auto()  # Any JEDI/SITH, except Luke Skywalker (Dagobah)
    # IMMUNE_TO_GAS = auto()  # Droids and ghosts.
    # todo: Lots more abilities to add to split up and replace the basic existing ones...
    # GHOST = auto()
    # DROID = auto()
    # UNTARGETABLE = auto()  # Are there any characters other than Ghosts?
    IS_PASSIVE = auto()  # Causes enemies to de-aggro when both players are passive characters.

    WEAPON_EWOK = auto()
    WEAPON_ZAPPER = auto()

    IS_A_VEHICLE = auto()
    FITS_EASILY_THROUGH_VENATOR = auto()  # Max height 2.5.
    VEHICLE_TIE = auto()
    VEHICLE_TOW = auto()
    VEHICLE_BLASTER = auto()

    ALL_VEHICLE_ABILITIES = IS_A_VEHICLE | FITS_EASILY_THROUGH_VENATOR | VEHICLE_TIE | VEHICLE_TOW | VEHICLE_BLASTER

    # def __matmul__(self, other):
    #     """(A | B | C) @ D -> (A in D) or (B in D) or (C in D)"""
    #     if isinstance(other, CharacterAbility):
    #         return self & other != 0
    #     else:
    #         return NotImplemented

    def to_readable_list(self) -> str:
        return ", ".join(ability.name for ability in self)

    def simplify_and(self) -> "CharacterAbility":
        """
        JEDI and CAN_BUILD_BRICKS -> JEDI because JEDI implies CAN_BUILD_BRICKS.
        :return:
        """
        if self.bit_count() < 2:
            return self
        simplified = self
        for ability in self:
            if ability in IMPLIED_BY_ABILITIES and IMPLIED_BY_ABILITIES[ability] & simplified:
                simplified &= ~ability
        return simplified

    def simplify_or(self) -> "CharacterAbility":
        """
        JEDI or CAN_BUILD_BRICKS -> CAN_BUILD_BRICKS because JEDI implies CNA_BUILD_BRICKS
        :return:
        """
        if self.bit_count() < 2:
            return self
        simplified = self

        for ability in self:
            if ability in IMPLIED_ABILITIES and IMPLIED_ABILITIES[ability] & simplified:
                simplified &= ~ability

        if simplified.value.bit_count() < 2:
            return simplified

        for combination, reducable_to in ABILITY_REDUCTIONS.items():
            if combination in simplified:
                # Remove the combination bits.
                simplified &= ~combination
                # Add the reduced bit.
                simplified |= reducable_to
        return simplified

    def simplify_combination(self) -> "CharacterAbility":
        """
        Simplify a combination of abilities where a character with this exact combination of abilities is desired.
        e.g. `HasAbilityCombination(JEDI | CAN_WEAR_HAT)` can be reduced to `HasAbility(CAN_WEAR_HAT_AND_DOUBLE_JUMP)`
        because all characters that have both the `JEDI` ability and the `CAN_WEAR_HAT` ability, are all the same
        characters that have the `CAN_WEAR_HAT_AND_DOUBLE_JUMP` ability.

        So this reduces:
        (JEDI | CAN_WEAR_HAT) -> CAN_WEAR_HAT_AND_DOUBLE_JUMP
        :return:
        """
        if self.bit_count() < 2:
            return self

        simplified = self.simplify_and()
        if simplified.bit_count() < 2:
            return simplified

        if simplified in COMBINATION_ABILITY_REDUCTIONS:
            return COMBINATION_ABILITY_REDUCTIONS[simplified]
        return simplified

    def expand_to_implied(self) -> "CharacterAbility":
        """Fully expand this ability to include all implied bits."""
        expanded = self
        for ability in self:
            expanded |= IMPLIED_ABILITIES[ability]
        return expanded

    def expand_to_implied_by(self) -> "CharacterAbility":
        """Fully expand this ability to include all bits that imply its contained bits."""
        expanded = self
        for ability in self:
            expanded |= IMPLIED_BY_ABILITIES[ability]
        return expanded

    @staticmethod
    def optimize_and_has_any_abilities(and_any_abilities: "set[CharacterAbility]") -> "set[CharacterAbility]":
        """
        Optimize the abilities within an `And(*HasAnyAbilities(abilities) for abilities in and_any_abilities)` by
        removing redundant HasAllAbilities.

        :param and_any_abilities:
        :return:
        """
        # Expand abilities to include all abilities that imply the given abilities, to allow discarding unneeded
        # abilities.
        # For example, And(HasAnyAbilities(BOUNTY_HUNTER | ASTROMECH_PANEL), HasAnyAbilities(GRAPPLE | ASTROMECH_PANEL))
        # can be reduced to just HasAnyAbilities(BOUNTY_HUNTER | ASTROMECH_PANEL) because GRAPPLE is implied by
        # BOUNTY_HUNTER.
        expanded_and_any_abilities = {c.expand_to_implied_by() for c in and_any_abilities}

        # Discard all any_abilities that contain other any_abilities.
        by_smallest_bit_count = sorted(expanded_and_any_abilities, key=CharacterAbility.bit_count)
        contained_any_abilities_removed: list[CharacterAbility] = []
        while by_smallest_bit_count:
            # Pop from the end to get largest bits first.
            largest_any_abilities = by_smallest_bit_count.pop()
            # If `largest_any_abilities` contains another any_abilities, then `largest_any_abilities` is pointless
            # because that other any_abilities also needs to be satisfied for the rule to return True, and when that
            # other any_abilities is satisfied, `largest_any_abilities` is always also satisfied.
            # Only abilities with smaller bit counts can be contained within `largest_any_abilities`, so checking can
            # stop once an any_abilities with the same bit count is found.
            current_bit_count = largest_any_abilities.bit_count()
            for other_any_abilities in by_smallest_bit_count:
                if other_any_abilities.bit_count() == current_bit_count:
                    # The other any_abilities are sorted by bit count, so if the iteration has reached the same bit
                    # count as `largest_any_abilities`, then the iteration can stop because the
                    # `expanded_and_any_abilities` is a set, so any any_abilities with the same bits cannot be the same
                    # any_abilities.
                    contained_any_abilities_removed.append(largest_any_abilities)
                    break
                if other_any_abilities in largest_any_abilities:
                    # `largest_any_abilities` contains `other_any_abilities`, so satisfying `other_any_abilities` will
                    # always also satisfy `largest_any_abilities`, so `largest_any_abilities` can be discarded.
                    break
            else:
                # No break, so `largest_any_abilities` did not contain any other any_abilities.
                contained_any_abilities_removed.append(largest_any_abilities)
        # Return after optimizing for HasAnyAbilities
        return set(map(CharacterAbility.simplify_or, contained_any_abilities_removed))

    @staticmethod
    def convert_or_has_all_to_and_has_any(*or_all_abilities: "CharacterAbility") -> "set[CharacterAbility]":
        """
        Convert `Or(*HasAllAbilities(abilities) for abilities in or_all_abilities)` into
        `And(*HasAnyAbilities(?) for ? in ?)`.

        This is effectively converting DNF -> CNF, but with CharacterAbility-specific optimizations.
        :param or_all_abilities:
        :return:
        """
        # reverse=False to reduce the number of times abilities are combined.
        or_all_abilities = sorted(set(or_all_abilities), key=CharacterAbility.bit_count)
        and_any_abilities: set[CharacterAbility] = {CharacterAbility.NONE}
        for all_abilities in or_all_abilities:
            updated_and_any_abilities = set()
            for ability in all_abilities.simplify_and():
                for existing_ability in and_any_abilities:
                    updated_and_any_abilities.add((ability | existing_ability).simplify_or())
            and_any_abilities = updated_and_any_abilities
        # Return after optimizing for HasAnyAbilities
        return CharacterAbility.optimize_and_has_any_abilities(and_any_abilities)

    @staticmethod
    def optimize_or_has_all_abilities(or_all_abilities: "set[CharacterAbility]") -> "set[CharacterAbility]":
        """
        Optimize the abilities within an `Or(*HasAllAbilities(abilities) for abilities in or_all_abilities)` by removing
        redundant HasAllAbilities.

        :param or_all_abilities:
        :return:
        """
        # Expand abilities to include all implied abilities, to allow discarding unneeded abilities.
        # For example, Or(HasAllAbilities(BOUNTY_HUNTER | ASTROMECH_PANEL), HasAllAbilities(GRAPPLE | ASTROMECH_PANEL))
        # can be reduced to just HasAllAbilities(GRAPPLE | ASTROMECH_PANEL) because BOUNTY_HUNTER implies GRAPPLE.
        expanded_or_all_abilities = {c.expand_to_implied() for c in or_all_abilities}

        # Discard all all_abilities that contain other all_abilities.
        by_smallest_bit_count = sorted(expanded_or_all_abilities, key=CharacterAbility.bit_count)
        contained_all_abilities_removed: list[CharacterAbility] = []
        while by_smallest_bit_count:
            # Pop from the end to get largest bits first.
            largest_all_abilities = by_smallest_bit_count.pop()
            # If another all_abilities is contained within this ability, then this `largest_all_abilities` is pointless.
            # Only abilities with smaller bit counts can be contained within `largest_all_abilities`, so checking can
            # stop once an all_abilities with the same bit count is found.
            current_bit_count = largest_all_abilities.bit_count()
            for other_all_abilities in by_smallest_bit_count:
                if other_all_abilities.bit_count() == current_bit_count:
                    # The other all_abilities are sorted by bit count, so if the iteration has reached the same bit
                    # count as `largest_all_abilities`, then the iteration can stop because the
                    # `expanded_or_all_abilities` is a set, so any all_abilities with the same bits cannot be the same
                    # all_abilities.
                    contained_all_abilities_removed.append(largest_all_abilities)
                    break
                if other_all_abilities in largest_all_abilities:
                    # `other_all_abilities` is contained within `largest_all_abilities`, so `other_all_abilities` will
                    # always be satisfied before `largest_all_abilities`, so `largest_all_abilities` can be discarded.
                    break
            else:
                # No break, so no other all_abilities were contained within `largest_all_abilities`.
                contained_all_abilities_removed.append(largest_all_abilities)
        # Return after optimizing for HasAllAbilities
        return set(map(CharacterAbility.simplify_and, contained_all_abilities_removed))

    @staticmethod
    def convert_and_has_any_to_or_has_all(*and_any_abilities: "CharacterAbility") -> "set[CharacterAbility]":
        """
        Convert `And(*(HasAnyAbilities(abilities) for abilities in and_any_required))` into
        `Or(*HasAllAbilities(?) for ? in ?)`.

        This is useful for figuring out the abilities required to go from region A to region B by following entrances,
        or could be used to optimize an And() rule.

        This is effectively converting CNF -> DNF, but with CharacterAbility-specific optimizations
        :param and_any_abilities:
        :return:
        """
        # Sort so that individual bits, that are therefore always required, are combined first.
        and_any_abilities = sorted(set(and_any_abilities), key=CharacterAbility.bit_count)
        # Or(*HasAllAbilities(?) for ? in ?)
        or_all_abilities: set[CharacterAbility] = {CharacterAbility.NONE}
        for any_abilities in and_any_abilities:
            updated_or_all_abilities: set[CharacterAbility] = set()
            # Simplify first to potentially reduce the number of bits iterated.
            for ability in any_abilities.simplify_or():
                for all_abilities in or_all_abilities:
                    # Simplify to remove abilities implied by another ability within the same all_abilities.
                    # Because `updated_or_all_abilities` is a set, this can sometimes deduplicate elements.
                    updated_or_all_abilities.add((all_abilities | ability).simplify_and())
            or_all_abilities = updated_or_all_abilities
        return CharacterAbility.optimize_or_has_all_abilities(or_all_abilities)

    def contains_rare_and_useful_abilities(self):
        return self & _RARE_AND_USEFUL_ABILITIES != 0


# Humanoid Special Abilities. These are rather more obvious to players.
ASTROMECH_PANEL = CharacterAbility.ASTROMECH_PANEL
BLASTER = CharacterAbility.BLASTER
GRAPPLE = CharacterAbility.GRAPPLE
BOUNTY_HUNTER = CharacterAbility.BOUNTY_HUNTER
HOVER = CharacterAbility.HOVER
HIGH_JUMP = CharacterAbility.HIGH_JUMP
IMPERIAL = CharacterAbility.IMPERIAL
JEDI = CharacterAbility.JEDI
PROTOCOL_PANEL = CharacterAbility.PROTOCOL_PANEL
SHORTIE = CharacterAbility.SHORTIE
SITH = CharacterAbility.SITH
JETPACK = CharacterAbility.JETPACK

# Vehicle Special Abilities.
VEHICLE_TIE = CharacterAbility.VEHICLE_TIE
VEHICLE_TOW = CharacterAbility.VEHICLE_TOW
VEHICLE_BLASTER = CharacterAbility.VEHICLE_BLASTER

# Chapter-specific flags.
CAN_WEAR_HAT = CharacterAbility.CAN_WEAR_HAT
CAN_WEAR_HAT_AND_GRAPPLE = CharacterAbility.CAN_WEAR_HAT_AND_GRAPPLE
CAN_WEAR_HAT_AND_DOUBLE_JUMP = CharacterAbility.CAN_WEAR_HAT_AND_DOUBLE_JUMP
ASTROMECH_DROID = CharacterAbility.ASTROMECH_DROID
IS_A_VEHICLE = CharacterAbility.IS_A_VEHICLE
FITS_EASILY_THROUGH_VENATOR = CharacterAbility.FITS_EASILY_THROUGH_VENATOR

# Extremely common ability flags.
CAN_RIDE_VEHICLES = CharacterAbility.CAN_RIDE_VEHICLES
CAN_PULL_LEVERS = CharacterAbility.CAN_PULL_LEVERS
CAN_PUSH_OBJECTS = CharacterAbility.CAN_PUSH_OBJECTS
CAN_BUILD_BRICKS = CharacterAbility.CAN_BUILD_BRICKS
CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS = CharacterAbility.CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS

CAN_DOUBLE_JUMP = CharacterAbility.CAN_DOUBLE_JUMP
CAN_JUMP_0_44 = CharacterAbility.CAN_JUMP_0_44
CAN_FLOP_JUMP = CharacterAbility.CAN_FLOP_JUMP
CAN_JUMP_HEIGHT_0_37 = CharacterAbility.CAN_JUMP_HEIGHT_0_37
CAN_JUMP_DISTANCE_0_69 = CharacterAbility.CAN_JUMP_DISTANCE_0_69
CAN_JUMP_DISTANCE_0_84 = CharacterAbility.CAN_JUMP_DISTANCE_0_84
CAN_JUMP_DISTANCE_0_92 = CharacterAbility.CAN_JUMP_DISTANCE_0_92
CAN_REGULAR_DIVE_ROLL = CharacterAbility.CAN_REGULAR_DIVE_ROLL
RUN_SPEED_0_9_OR_HIGHER = CharacterAbility.RUN_SPEED_0_9_OR_HIGHER
RUN_SPEED_1_18_OR_HIGHER = CharacterAbility.RUN_SPEED_1_18_OR_HIGHER
CAN_BARELY_JUMP = CharacterAbility.CAN_BARELY_JUMP

CAN_HIGH_JUMP_SLAM = CharacterAbility.CAN_HIGH_JUMP_SLAM
CAN_TRIPLE_JUMP_GREAT_DISTANCE = CharacterAbility.CAN_TRIPLE_JUMP_GREAT_DISTANCE

CAN_MELEE = CharacterAbility.CAN_MELEE
CAN_DEFLECT_BOLTS = CharacterAbility.CAN_DEFLECT_BOLTS

# Weapon type flags.
WEAPON_EWOK = CharacterAbility.WEAPON_EWOK
WEAPON_ZAPPER = CharacterAbility.WEAPON_ZAPPER

# Other flags.
CAN_SELF_DESTRUCT = CharacterAbility.CAN_SELF_DESTRUCT
CAN_AGGRAVATE_ENEMIES = CharacterAbility.CAN_AGGRAVATE_ENEMIES
IS_NON_GHOST_JEDI = CharacterAbility.IS_NON_GHOST_JEDI
TRAINED_JEDI = CharacterAbility.TRAINED_JEDI
IS_PASSIVE = CharacterAbility.IS_PASSIVE


# Combination flags
#CHARACTER_CAN_JUMP_NORMALLY = CAN_JUMP_HEIGHT_0_37 | CAN_BARELY_JUMP
#CHARACTER_CAN_JUMP_SLIGHTLY_HIGHER = CAN_JUMP_0_44 | CHARACTER_CAN_JUMP_NORMALLY
#CHARACTER_SITH = SITH | JEDI

# CHARACTER_ASTROMECH_DROID = ASTROMECH_PANEL | CAN_BARELY_JUMP | WEAPON_ZAPPER | ASTROMECH_DROID | HOVER

# Rare and also useful abilties.
_RARE_AND_USEFUL_ABILITIES = (
    ASTROMECH_PANEL
    | BOUNTY_HUNTER
    | HIGH_JUMP
    | SHORTIE
    | SITH
    | PROTOCOL_PANEL
    | HOVER
    | VEHICLE_TIE
    | VEHICLE_TOW
)


# This dictionary is generated by test.test_abilities.TestAbilities.test_implied_abilities when the test fails.
# By listing out the dict contents, it provides a visual aid into understanding possible optimisations in rules, rather
# than there just being a dictionary with unknown contents.
# If A => B (A implies B), then A | B is B, and A & B is A.
# This dict maps A to all B that are implied.
# noinspection LongLine
IMPLIED_ABILITIES: dict[CharacterAbility, CharacterAbility] = {
    # All characters with this ability: Also have these abilities,
    # HasAllAbilities(left | right) -> HasAbility(left)
    # HasAnyAbilities(left | right) -> HasAbility(right)
    ASTROMECH_PANEL: CAN_BARELY_JUMP | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | RUN_SPEED_0_9_OR_HIGHER,
    BLASTER: RUN_SPEED_0_9_OR_HIGHER | CAN_AGGRAVATE_ENEMIES,
    GRAPPLE: BLASTER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | RUN_SPEED_0_9_OR_HIGHER | CAN_AGGRAVATE_ENEMIES,
    BOUNTY_HUNTER: BLASTER | GRAPPLE | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | RUN_SPEED_0_9_OR_HIGHER | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE | CAN_AGGRAVATE_ENEMIES,
    HOVER: CAN_BARELY_JUMP | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | RUN_SPEED_0_9_OR_HIGHER,
    HIGH_JUMP: CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | RUN_SPEED_0_9_OR_HIGHER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_FLOP_JUMP | CAN_DOUBLE_JUMP | CAN_AGGRAVATE_ENEMIES,
    IMPERIAL: CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | RUN_SPEED_0_9_OR_HIGHER | CAN_AGGRAVATE_ENEMIES,
    JEDI: CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | CAN_JUMP_0_44 | CAN_FLOP_JUMP | CAN_DOUBLE_JUMP | CAN_MELEE,
    PROTOCOL_PANEL: CharacterAbility.NONE,
    SHORTIE: CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37,
    SITH: JEDI | CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | RUN_SPEED_0_9_OR_HIGHER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_FLOP_JUMP | CAN_DOUBLE_JUMP | CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_MELEE | CAN_DEFLECT_BOLTS | CAN_AGGRAVATE_ENEMIES | IS_NON_GHOST_JEDI | TRAINED_JEDI,
    JETPACK: BLASTER | GRAPPLE | BOUNTY_HUNTER | HOVER | CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | RUN_SPEED_0_9_OR_HIGHER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES,
    CAN_WEAR_HAT: CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | RUN_SPEED_0_9_OR_HIGHER | RUN_SPEED_1_18_OR_HIGHER,
    CAN_WEAR_HAT_AND_GRAPPLE: BLASTER | GRAPPLE | CAN_WEAR_HAT | CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | RUN_SPEED_0_9_OR_HIGHER | RUN_SPEED_1_18_OR_HIGHER | CAN_AGGRAVATE_ENEMIES,
    CAN_WEAR_HAT_AND_DOUBLE_JUMP: JEDI | CAN_WEAR_HAT | CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | RUN_SPEED_0_9_OR_HIGHER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_FLOP_JUMP | CAN_DOUBLE_JUMP | CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_MELEE,
    CAN_PULL_LEVERS: CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37,
    CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS: CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37,
    CAN_BUILD_BRICKS: CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37,
    CAN_BARELY_JUMP: CharacterAbility.NONE,
    CAN_JUMP_HEIGHT_0_37: CAN_BARELY_JUMP,
    CAN_JUMP_DISTANCE_0_69: CAN_BARELY_JUMP,
    CAN_JUMP_DISTANCE_0_84: CAN_BARELY_JUMP | CAN_JUMP_DISTANCE_0_69,
    CAN_JUMP_DISTANCE_0_92: CAN_BARELY_JUMP | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84,
    CAN_REGULAR_DIVE_ROLL: BLASTER | GRAPPLE | CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | RUN_SPEED_0_9_OR_HIGHER | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE | CAN_AGGRAVATE_ENEMIES,
    RUN_SPEED_0_9_OR_HIGHER: CharacterAbility.NONE,
    RUN_SPEED_1_18_OR_HIGHER: RUN_SPEED_0_9_OR_HIGHER,
    CAN_JUMP_0_44: CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69,
    CAN_FLOP_JUMP: CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | CAN_JUMP_0_44,
    CAN_DOUBLE_JUMP: CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | CAN_JUMP_0_44 | CAN_FLOP_JUMP,
    CAN_HIGH_JUMP_SLAM: HIGH_JUMP | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | RUN_SPEED_0_9_OR_HIGHER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_FLOP_JUMP | CAN_DOUBLE_JUMP | CAN_MELEE | CAN_DEFLECT_BOLTS | CAN_AGGRAVATE_ENEMIES,
    CAN_TRIPLE_JUMP_GREAT_DISTANCE: CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | RUN_SPEED_0_9_OR_HIGHER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_FLOP_JUMP | CAN_DOUBLE_JUMP | CAN_MELEE,
    CAN_MELEE: CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69,
    CAN_DEFLECT_BOLTS: CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES,
    ASTROMECH_DROID: ASTROMECH_PANEL | HOVER | CAN_BARELY_JUMP | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | RUN_SPEED_0_9_OR_HIGHER | CAN_SELF_DESTRUCT | IS_PASSIVE | WEAPON_ZAPPER,
    CAN_SELF_DESTRUCT: CharacterAbility.NONE,
    CAN_AGGRAVATE_ENEMIES: CharacterAbility.NONE,
    IS_NON_GHOST_JEDI: JEDI | CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | CAN_JUMP_0_44 | CAN_FLOP_JUMP | CAN_DOUBLE_JUMP | CAN_MELEE | CAN_DEFLECT_BOLTS | CAN_AGGRAVATE_ENEMIES,
    TRAINED_JEDI: JEDI | CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | CAN_JUMP_DISTANCE_0_84 | CAN_JUMP_DISTANCE_0_92 | CAN_JUMP_0_44 | CAN_FLOP_JUMP | CAN_DOUBLE_JUMP | CAN_MELEE,
    IS_PASSIVE: CharacterAbility.NONE,
    WEAPON_EWOK: SHORTIE | CAN_PULL_LEVERS | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_BARELY_JUMP | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69 | RUN_SPEED_0_9_OR_HIGHER | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES,
    WEAPON_ZAPPER: CAN_BARELY_JUMP | RUN_SPEED_0_9_OR_HIGHER,
    IS_A_VEHICLE: CharacterAbility.NONE,
    FITS_EASILY_THROUGH_VENATOR: IS_A_VEHICLE,
    VEHICLE_TIE: IS_A_VEHICLE | FITS_EASILY_THROUGH_VENATOR | VEHICLE_BLASTER,
    VEHICLE_TOW: IS_A_VEHICLE | FITS_EASILY_THROUGH_VENATOR | VEHICLE_BLASTER,
    VEHICLE_BLASTER: IS_A_VEHICLE,
}


def _make_implied_by_abilities() -> dict[CharacterAbility, CharacterAbility]:
    implied_by_dict: dict[CharacterAbility, CharacterAbility] = {
        ability: CharacterAbility.NONE for ability in CharacterAbility
    }
    for ability, implies in IMPLIED_ABILITIES.items():
        for implied in implies:
            implied_by_dict[implied] |= ability
    return implied_by_dict


# If A => B (A implies B), then A | B is B, and A & B is A.
# This dict maps B to all A that imply it.
IMPLIED_BY_ABILITIES = _make_implied_by_abilities()


ABILITY_REDUCTIONS: dict[CharacterAbility, CharacterAbility] = {
    # 2) Are at least one of these: 1) All of these.
    # 1) All of these: 2) Are these.
    # HasAnyAbilities(A | B) can be reduced to HasAbility(C).
    # Combinations with more bits need to be first.
    CAN_WEAR_HAT_AND_DOUBLE_JUMP | IS_NON_GHOST_JEDI | TRAINED_JEDI: JEDI,
    CAN_WEAR_HAT_AND_DOUBLE_JUMP | TRAINED_JEDI: JEDI,
    IS_NON_GHOST_JEDI | TRAINED_JEDI: JEDI,
    # Thanks to Admiral Ackbar, these are not possible:
    # HIGH_JUMP | JEDI | CAN_TRIPLE_JUMP_GREAT_DISTANCE: CAN_DOUBLE_JUMP,
    # HIGH_JUMP | JEDI: CAN_DOUBLE_JUMP,
    ASTROMECH_PANEL | CAN_JUMP_HEIGHT_0_37: CAN_BARELY_JUMP,
    HOVER | CAN_JUMP_HEIGHT_0_37: CAN_BARELY_JUMP,
    CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_DISTANCE_0_69: CAN_BARELY_JUMP,
    CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_92: CAN_BARELY_JUMP,
    CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_84: CAN_BARELY_JUMP,
    CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69: CAN_BARELY_JUMP,
    CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_0_44: CAN_JUMP_HEIGHT_0_37,
    CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_DISTANCE_0_84: CAN_BARELY_JUMP,
    CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_DISTANCE_0_92: CAN_BARELY_JUMP,
    JETPACK | ASTROMECH_DROID: HOVER,
    CAN_JUMP_HEIGHT_0_37 | ASTROMECH_DROID: CAN_BARELY_JUMP,
    CAN_JUMP_HEIGHT_0_37 | WEAPON_ZAPPER: CAN_BARELY_JUMP,
    CAN_PULL_LEVERS | CAN_JUMP_DISTANCE_0_69: CAN_BARELY_JUMP,
    CAN_PULL_LEVERS | CAN_JUMP_DISTANCE_0_84: CAN_BARELY_JUMP,
    FITS_EASILY_THROUGH_VENATOR | VEHICLE_BLASTER: IS_A_VEHICLE
    # # Thanks to Imperial Guard, these are not possible:
    # SITH | GRAPPLE: IMPERIAL
    # JEDI | GRAPPLE: IMPERIAL
}


# This dictionary is generated by test.test_abilities.TestAbilities.test_combination_reductions when the test fails.
# By listing out the dict contents, it provides a visual aid into understanding possible optimisations in rules, rather
# than there just being a dictionary with unknown contents.
# noinspection LongLine
COMBINATION_ABILITY_REDUCTIONS: dict[CharacterAbility, CharacterAbility] = {
    # 1) All characters with this combination: 2) Have this ability.
    # 2) Have these abilities: 1) All characters with this ability.
    # HasAbilityCombination(A | B) can be reduced to HasAbility(C).
    BLASTER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_DISTANCE_0_69: GRAPPLE,
    BLASTER | CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69: GRAPPLE,
    BLASTER | CAN_JUMP_DISTANCE_0_69: GRAPPLE,
    CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_FLOP_JUMP | CAN_MELEE: JEDI,
    CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_DOUBLE_JUMP | CAN_MELEE: JEDI,
    CAN_PULL_LEVERS | CAN_FLOP_JUMP | CAN_MELEE: JEDI,
    CAN_PULL_LEVERS | CAN_DOUBLE_JUMP | CAN_MELEE: JEDI,
    BLASTER | HOVER: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_PULL_LEVERS | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_BUILD_BRICKS: JETPACK,
    BLASTER | HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    BLASTER | HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_BUILD_BRICKS | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_BUILD_BRICKS | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_JUMP_HEIGHT_0_37: JETPACK,
    BLASTER | HOVER | CAN_JUMP_HEIGHT_0_37 | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    BLASTER | HOVER | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    BLASTER | HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_JUMP_0_44: JETPACK,
    BLASTER | HOVER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    BLASTER | HOVER | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_0_44: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_JUMP_0_44: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_PULL_LEVERS | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_BUILD_BRICKS: JETPACK,
    GRAPPLE | HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    GRAPPLE | HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    GRAPPLE | HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_BUILD_BRICKS | CAN_JUMP_0_44: JETPACK,
    GRAPPLE | HOVER | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_BUILD_BRICKS | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    GRAPPLE | HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    GRAPPLE | HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_JUMP_0_44: JETPACK,
    GRAPPLE | HOVER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    GRAPPLE | HOVER | CAN_MELEE: JETPACK,
    BOUNTY_HUNTER | HOVER: JETPACK,
    BOUNTY_HUNTER | HOVER | CAN_PULL_LEVERS: JETPACK,
    BOUNTY_HUNTER | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS: JETPACK,
    BOUNTY_HUNTER | HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_0_44: JETPACK,
    BOUNTY_HUNTER | HOVER | CAN_PULL_LEVERS | CAN_JUMP_0_44: JETPACK,
    BOUNTY_HUNTER | HOVER | CAN_BUILD_BRICKS: JETPACK,
    BOUNTY_HUNTER | HOVER | CAN_BUILD_BRICKS | CAN_JUMP_0_44: JETPACK,
    BOUNTY_HUNTER | HOVER | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_PULL_LEVERS: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_MELEE: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | RUN_SPEED_1_18_OR_HIGHER | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_MELEE: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_PULL_LEVERS | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_MELEE: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | RUN_SPEED_1_18_OR_HIGHER | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_MELEE: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_RIDE_VEHICLES_AND_PUSH_OBJECTS | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_BUILD_BRICKS: JETPACK,
    HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_BUILD_BRICKS | RUN_SPEED_1_18_OR_HIGHER | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_BUILD_BRICKS | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_BUILD_BRICKS | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_BUILD_BRICKS | CAN_MELEE: JETPACK,
    HOVER | CAN_BUILD_BRICKS | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_BUILD_BRICKS | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_JUMP_HEIGHT_0_37: JETPACK,
    HOVER | CAN_JUMP_HEIGHT_0_37 | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    HOVER | CAN_JUMP_HEIGHT_0_37 | RUN_SPEED_1_18_OR_HIGHER | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_JUMP_HEIGHT_0_37 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | RUN_SPEED_1_18_OR_HIGHER: JETPACK,
    HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44: JETPACK,
    HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE: JETPACK,
    HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | RUN_SPEED_1_18_OR_HIGHER | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_JUMP_0_44: JETPACK,
    HOVER | CAN_JUMP_0_44 | CAN_MELEE: JETPACK,
    HOVER | CAN_JUMP_0_44 | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_MELEE: JETPACK,
    HOVER | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: JETPACK,
    HOVER | CAN_AGGRAVATE_ENEMIES: JETPACK,
    BLASTER | CAN_WEAR_HAT: CAN_WEAR_HAT_AND_GRAPPLE,
    GRAPPLE | CAN_WEAR_HAT: CAN_WEAR_HAT_AND_GRAPPLE,
    JEDI | CAN_WEAR_HAT: CAN_WEAR_HAT_AND_DOUBLE_JUMP,
    JEDI | CAN_WEAR_HAT | CAN_TRIPLE_JUMP_GREAT_DISTANCE: CAN_WEAR_HAT_AND_DOUBLE_JUMP,
    CAN_WEAR_HAT | CAN_FLOP_JUMP: CAN_WEAR_HAT_AND_DOUBLE_JUMP,
    CAN_WEAR_HAT | CAN_FLOP_JUMP | CAN_MELEE: CAN_WEAR_HAT_AND_DOUBLE_JUMP,
    CAN_WEAR_HAT | CAN_DOUBLE_JUMP: CAN_WEAR_HAT_AND_DOUBLE_JUMP,
    CAN_WEAR_HAT | CAN_DOUBLE_JUMP | CAN_MELEE: CAN_WEAR_HAT_AND_DOUBLE_JUMP,
    CAN_WEAR_HAT | CAN_TRIPLE_JUMP_GREAT_DISTANCE: CAN_WEAR_HAT_AND_DOUBLE_JUMP,
    ASTROMECH_PANEL | HOVER: ASTROMECH_DROID,
    ASTROMECH_PANEL | HOVER | CAN_SELF_DESTRUCT: ASTROMECH_DROID,
    ASTROMECH_PANEL | HOVER | CAN_SELF_DESTRUCT | IS_PASSIVE: ASTROMECH_DROID,
    ASTROMECH_PANEL | HOVER | CAN_SELF_DESTRUCT | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | HOVER | CAN_SELF_DESTRUCT | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | HOVER | IS_PASSIVE: ASTROMECH_DROID,
    ASTROMECH_PANEL | HOVER | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | HOVER | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_JUMP_DISTANCE_0_92 | CAN_SELF_DESTRUCT: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_JUMP_DISTANCE_0_92 | CAN_SELF_DESTRUCT | IS_PASSIVE: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_JUMP_DISTANCE_0_92 | CAN_SELF_DESTRUCT | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_JUMP_DISTANCE_0_92 | CAN_SELF_DESTRUCT | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_JUMP_DISTANCE_0_92 | IS_PASSIVE: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_JUMP_DISTANCE_0_92 | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_JUMP_DISTANCE_0_92 | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_SELF_DESTRUCT: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_SELF_DESTRUCT | IS_PASSIVE: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_SELF_DESTRUCT | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | CAN_SELF_DESTRUCT | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | IS_PASSIVE: ASTROMECH_DROID,
    ASTROMECH_PANEL | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    ASTROMECH_PANEL | WEAPON_ZAPPER: ASTROMECH_DROID,
    HOVER | CAN_SELF_DESTRUCT: ASTROMECH_DROID,
    HOVER | CAN_SELF_DESTRUCT | IS_PASSIVE: ASTROMECH_DROID,
    HOVER | CAN_SELF_DESTRUCT | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    HOVER | CAN_SELF_DESTRUCT | WEAPON_ZAPPER: ASTROMECH_DROID,
    HOVER | IS_PASSIVE: ASTROMECH_DROID,
    HOVER | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    HOVER | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_69 | CAN_SELF_DESTRUCT | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_69 | CAN_SELF_DESTRUCT | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_69 | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_84 | CAN_SELF_DESTRUCT | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_84 | CAN_SELF_DESTRUCT | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_84 | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_84 | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_92 | CAN_SELF_DESTRUCT | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_92 | CAN_SELF_DESTRUCT | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_92 | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_JUMP_DISTANCE_0_92 | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_SELF_DESTRUCT | IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    CAN_SELF_DESTRUCT | WEAPON_ZAPPER: ASTROMECH_DROID,
    IS_PASSIVE | WEAPON_ZAPPER: ASTROMECH_DROID,
    JEDI | CAN_DEFLECT_BOLTS: IS_NON_GHOST_JEDI,
    JEDI | CAN_AGGRAVATE_ENEMIES: IS_NON_GHOST_JEDI,
    CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_FLOP_JUMP | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: IS_NON_GHOST_JEDI,
    CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_FLOP_JUMP | CAN_DEFLECT_BOLTS: IS_NON_GHOST_JEDI,
    CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_DOUBLE_JUMP | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: IS_NON_GHOST_JEDI,
    CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_DOUBLE_JUMP | CAN_DEFLECT_BOLTS: IS_NON_GHOST_JEDI,
    CAN_PULL_LEVERS | CAN_FLOP_JUMP | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: IS_NON_GHOST_JEDI,
    CAN_PULL_LEVERS | CAN_FLOP_JUMP | CAN_DEFLECT_BOLTS: IS_NON_GHOST_JEDI,
    CAN_PULL_LEVERS | CAN_DOUBLE_JUMP | CAN_MELEE | CAN_AGGRAVATE_ENEMIES: IS_NON_GHOST_JEDI,
    CAN_PULL_LEVERS | CAN_DOUBLE_JUMP | CAN_DEFLECT_BOLTS: IS_NON_GHOST_JEDI,
    SHORTIE | RUN_SPEED_0_9_OR_HIGHER | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: WEAPON_EWOK,
    SHORTIE | CAN_JUMP_0_44 | CAN_AGGRAVATE_ENEMIES: WEAPON_EWOK,
}
