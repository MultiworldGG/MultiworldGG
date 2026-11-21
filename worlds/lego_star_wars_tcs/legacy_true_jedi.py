"""Accurate True Jedi logic is not implemented yet, instead, True Jedi logic follows the legacy system of expecting
characters with the abilities of the story characters, plus reaching the chapter completion region. In a few cases, a
Score Multiplier is also expected."""
from rule_builder.options import OptionFilter
from rule_builder.rules import Has

from .character_ability import *
from .constants import CHAPTER_SPECIFIC_FLAGS
from .data.areas import Area
from .data.items.all_character_items import NORMAL_CHARACTER_TO_ITEM_DATA
from .data.items.generic_items import NonDataItemName
from .data.logic.rules import HasAllAbilities
from .options import EasierTrueJedi


__all__ = [
    "DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI",
    "get_legacy_true_jedi_rule",
]


# True Jedi that is difficult if not impossible in Free Play with just the Story characters for a level.
DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI: set[Area] = {
    # I don't think this is possible, I tried before, even with maximum usage of Power Ups. Higher logic could probably
    # get this because they can jump to the top of the cylindrical area with all the Battle Droids, which has a bunch of
    # Blue Studs.
    Area.MAUL,
    Area.DOOKU,  # I only managed 14180/22000
    Area.GRIEVOUS,  # Barely possible by re-entering and getting studs that replace minikits
    # I managed only 40700/45000, even with 3 double jump slams to get 3 Blue Studs that were just too high.
    Area.TEMPLE,
    # Dying is easy in multiple areas, where even without deaths, it is barely possible.
    Area.VADER,
    # It's pretty slow, but possible to overshoot by 20K studs while mostly wasting the two Power Ups. If it is possible
    # to get 9/10 TIE Fighters in the Turbolaser control area towards the very end, then return to the previous room via
    # the elevator, go back to the Turbolasers and destroy the last TIE Fighter before the Power Up runs out, then
    # doubling the studs that spawn (around 20K) would be a huge benefit.
    # Area.DEATHSTARRESCUE,
    # Possible to overshoot by 95K Studs, even without taking advantage of Power Ups, though it is slow, and a vehicle,
    # level, so dying a lot is expected. Vehicle chapters also just kind of suck for picking up studs. 4-6 could be
    # included in the difficult True Jedi if there are complaints.
    # Area.DEATHSTARBATTLE,
    # Apparently barely possible by re-entering and getting studs that replace minikits. I find this vehicle chapter
    # especially difficult to actually pick studs up off the ground, and dying is also easy in this chapter.
    Area.HOTHBATTLE,
    # I only managed 53K/80K without deaths, but while wasting Power Ups. Even with Power Ups, 5-2 is looking clearly
    # impossible.
    Area.HOTHESCAPE,
    # If no studs are lost from dying and Power Ups are used to their fullest, then 5-6 is just barely possible
    # without getting Minikit Blue Studs, but by only around 100-200 Studs.
    Area.CLOUDCITYESCAPE,
    # I am assuming that the extra room where the door needs to be blown up is required to get True Jedi in 6-5.
    Area.EMPERORFIGHT,
}

_CHAPTER_SPECIFIC_REQUIREMENTS: dict[Area, tuple[CharacterAbility, CharacterAbility | None]] = {
    # Mos Espa Pod Race does not require any Vehicle abilities, but does require having at least one vehicle character
    # unlocked, so extra logic is needed to ensure the player actually has a vehicle character.
    Area.PODSPRINT: (IS_A_VEHICLE, None),
    # There is a Hat Machine in Level D, which you can take all the way back to behind spawn to the Imperial Panel with
    # a Minikit behind.
    # All the characters that can wear hats can jump and can make it back to the panel.
    # todo: Maybe the most basic logic level should use (CAN_WEAR_HAT_AND_GRAPPLE or CAN_WEAR_HAT_AND_DOUBLE_JUMP)
    #  because CAN_WEAR_HAT on its own requires either a tight jump, or jumping off a small garbage bin than can be
    #  destroyed by accident.
    Area.MOSEISLEY: (CAN_WEAR_HAT, IMPERIAL),
    # There is a section where a Stormtrooper helmet needs to be taken across a gap that requires grappling if you want
    # to keep the hat.
    Area.DEATHSTARRESCUE: (CAN_WEAR_HAT_AND_GRAPPLE, IMPERIAL),
    # In 4-5, there is an Imperial Hat Machine with an Imperial panel that requires grappling across a gap to reach
    # (Level A), so, if the player has no Imperial character, they need a BLASTER character that can wear hats.
    # This additionally covers a later use of an Imperial Hat Machine where the panel is at the top of an elevator
    # (level B), and another later use of an Imperial Hat Machine where the panel is at the end of a Zipup, across a gap
    # (level C).
    Area.DEATHSTARESCAPE: (CAN_WEAR_HAT_AND_GRAPPLE, IMPERIAL),
    Area.DAGOBAH: (ASTROMECH_DROID, None),
    # In 5-5, there is an Imperial Hat Machine with an Imperial panel that requires double-jumping across a gap to
    # reach, so, if the player has no Imperial character, they need a Jedi/Sith that can wear hats.
    # This gets its own flag, instead of being JEDI | CAN_WEAR_HAT, for logic performance reasons. The complexity comes
    # from the fact that characters may have additional flags, but the logic system prefers to store only the combined
    # flag of all currently usable abilities.
    Area.CLOUDCITYTRAP: (CAN_WEAR_HAT_AND_DOUBLE_JUMP, IMPERIAL),
    # Level A has a Hat Machine where you need to walk to an elevator with the hat.
    Area.CLOUDCITYESCAPE: (CAN_WEAR_HAT, IMPERIAL),
    # The level is played in Story with a character than can wear hats instead of needing a bounty hunter.
    Area.JABBASPALACE: (CAN_WEAR_HAT, BOUNTY_HUNTER),
}
"""
Chapter completions that require logic that is specific to that chapter.

The first element of each value are the abilities that would normally be used in Story mode.

The second element of each value is an optional alternative ability that can be used instead, but often requires a rarer
ability. 
"""


def get_legacy_true_jedi_rule(area: Area):
    # The logic is not fully prepared for True Jedi logic currently, so the rule is set to require all the logical
    # abilities of the Story characters of the Chapter, which will be overly restrictive for many locations, but overly
    # restrictive logic cannot result in impossible seeds.
    # A few chapters have chapter-specific logical requirements that get stripped from the requirements
    # of other chapters.
    base_abilities: CharacterAbility = CharacterAbility.NONE
    for character in area.get_story_characters():
        base_abilities |= NORMAL_CHARACTER_TO_ITEM_DATA[character].abilities
    # Strip all chapter-specific flags. If there are any that are relevant to this chapter, they will be re-added in
    # the next step.
    base_abilities &= ~CHAPTER_SPECIFIC_FLAGS
    # Add any chapter-specific flags and set possible alternatives
    alt_ability_requirements: CharacterAbility | None = None
    if chapter_specific_requirement := _CHAPTER_SPECIFIC_REQUIREMENTS.get(area):
        story_logic, alternative_ability = chapter_specific_requirement
        main_ability_requirements = base_abilities | story_logic
        if alternative_ability is not None and alternative_ability not in base_abilities:
            # Define an alternative set of requirements.
            alt_ability_requirements = (base_abilities & ~story_logic) | alternative_ability
    else:
        main_ability_requirements = base_abilities
    if main_ability_requirements is CharacterAbility.NONE:
        raise AssertionError("Every chapter should have at least one CharacterAbility requirement.")
    if alt_ability_requirements is CharacterAbility.NONE:
        raise AssertionError("Every chapter's alternate requiremenents should have at least one CharacterAbility"
                             " requirement.")

    if alt_ability_requirements:
        abilities_rule = HasAllAbilities(main_ability_requirements) | HasAllAbilities(alt_ability_requirements)
    else:
        abilities_rule = HasAllAbilities(main_ability_requirements)

    if area in DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI:
        return abilities_rule & (Has(NonDataItemName.PROGRESSIVE_SCORE_MULTIPLIER.value)
                                 | OptionFilter(EasierTrueJedi, EasierTrueJedi.option_true))
    else:
        return abilities_rule
