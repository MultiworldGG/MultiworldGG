from typing import TYPE_CHECKING

from BaseClasses import ItemClassification

from .character_ability import CharacterAbility
from .data.areas import PURCHASABLE_NON_POWER_BRICK_EXTRAS
from .data.characters import Character
from .data.extras import Extra
from .data.items import GenericCharacterData, GenericItemData
from .data.items.all_character_items import CHARACTER_TO_ITEM_DATA
from .data.items.extra_items import ExtraData
from .data.items.generic_items import (
    MINIKITS_BY_NAME,
    NonDataItemName,
    CHAPTER_UNLOCK_ITEM_TO_CHAPTER,
    EPISODE_UNLOCK_TO_EPISODE,
)
from .items import ITEM_DATA_BY_NAME
from .options import AllEpisodesCharacterPurchaseRequirements, EpisodeUnlockRequirement

if TYPE_CHECKING:
    from . import LegoStarWarsTCSWorld
else:
    LegoStarWarsTCSWorld = object


__all__ = [
    "evaluate_effective_item",
]


_USEFUL_NON_PROGRESSION_CHARACTERS: set[str] = {
    CHARACTER_TO_ITEM_DATA[c].name for c in
    (
        # Ghosts are invincible and untargetable.
        Character.BEN_KENOBI_GHOST,
        Character.ANAKIN_SKYWALKER_GHOST,
        Character.YODA_GHOST,
        # Yoda is fast when jumping, and is usable in many tricks in higher logic difficulties.
        Character.YODA,
        # The fastest character (1.8).
        Character.DROIDEKA,
        # The second-fastest characters (1.5), though a bit clunky to use since they cannot jump properly, and either
        # cannot attack at all, or have a very slow attack.
        Character.WATTO,
        Character.GEONOSIAN,
        # The third-fastest character when Super Gonk is active (1.44), also has good jump height with Super Gonk
        # active.
        Character.GONK_DROID,
        # Fastest vehicles.
        Character.ANAKINS_POD,
        Character.SEBULBAS_POD,
    )
}
"""Characters that should always have at least Useful Classification."""

_TOO_LOGICALLY_POWERFUL_CHARACTERS: set[str] = {
    CHARACTER_TO_ITEM_DATA[c].name for c in
    (
        # Can access Bounty Hunter, Astromech and Protocol panels, as well as the usual benefits of being a Bounty
        # Hunter, being able to jump, ride vehicles, shoot, melee and grapple.
        Character.FOUR_LOM,
        Character.IG_88,
    )
}
"""Characters that should always have Useful Classification. When they are logically relevant they will be
Progression + Useful + Skip Balancing."""


def _evaluate_effective_extra_data(world: LegoStarWarsTCSWorld,
                                   item_data: ExtraData,
                                   relevant_item_counts: dict[str, int] | None = None
                                   ) -> ItemClassification:
    if world.is_universal_tracker():
        # An Extra might only be relevant to logic in a higher logic difficulty. So for 'glitched' Universal Tracker
        # logic to work correctly, all Extra items are marked as progression.
        return ItemClassification.progression

    extra = item_data.extra
    if relevant_item_counts is not None:
        if relevant_item_counts.get(item_data.name, 0) > 0:
            return ItemClassification.progression
        elif extra not in PURCHASABLE_NON_POWER_BRICK_EXTRAS or extra is Extra.EXTRA_TOGGLE:
            return ItemClassification.useful
        else:
            return ItemClassification.filler
    else:
        if extra in PURCHASABLE_NON_POWER_BRICK_EXTRAS:
            # Only Extra Toggle is useful out of these Extras due to the high movement speed Mouse Droid and a
            # few logic uses.
            if extra is Extra.EXTRA_TOGGLE:
                if world.options.logic_difficulty.normal_plus:
                    return ItemClassification.progression
                else:
                    return ItemClassification.useful
            else:
                return ItemClassification.filler
        else:
            # Many Power Brick Extras provide cheat-like abilities to the player, so should be given at least
            # Useful classification.
            if world.options.logic_difficulty.normal_plus:
                return ItemClassification.progression
            else:
                return ItemClassification.useful


def _evaluate_effective_character_data(world: LegoStarWarsTCSWorld,
                                       item_data: GenericCharacterData,
                                       effective_character_abilities_lookup: dict[str, CharacterAbility] | None = None,
                                       relevant_item_counts: dict[str, int] | None = None,
                                       ) -> tuple[ItemClassification, CharacterAbility]:
    if world.is_universal_tracker():
        # A Character might only be relevant to logic in a higher logic difficulty. So for 'glitched' Universal Tracker
        # logic to work correctly, all Character items are marked as progression, and retain all abilities.
        return ItemClassification.progression, item_data.abilities

    classification = ItemClassification.filler
    name = item_data.name
    if effective_character_abilities_lookup is not None:
        abilities = effective_character_abilities_lookup[name]
    else:
        abilities = item_data.abilities & ~world.starting_character_abilities

    # Special handling for Gonk Droid -> Super Gonk Droid
    inherit_progression_from_super_gonk_droid = False
    if item_data.character is Character.GONK_DROID:
        # Check if Super Gonk should be progression classification.
        super_gonk_extra_classification = _evaluate_effective_extra_data(
            world,
            ExtraData.from_extra(Extra.SUPER_GONK),
            relevant_item_counts,
        )
        if ItemClassification.progression in super_gonk_extra_classification:
            # Check if Super Gonk Droid should be progression classification, and get its abilities.
            super_gonk_droid_classification, _super_gonk_droid_abilities = _evaluate_effective_character_data(
                world,
                CHARACTER_TO_ITEM_DATA[Character.EVENT_SUPER_GONK_DROID],
                effective_character_abilities_lookup,
                relevant_item_counts,
            )
            if ItemClassification.progression in super_gonk_droid_classification:
                # Super Gonk Droid is progression, so Gonk Droid should always be progression.
                inherit_progression_from_super_gonk_droid = True

    if world.character_chapter_access_counts[item_data.character] > 0:
        if world.character_chapter_access_counts[item_data.character] >= world.prog_useful_level_access_threshold_count:
            # Characters that block access to a large number of chapters get progression + useful
            # classification. This is functionally identical to progression classification, but some
            # games/clients may specially highlight progression + useful items.
            classification = ItemClassification.progression | ItemClassification.useful
        else:
            classification = ItemClassification.progression
    elif abilities.contains_rare_and_useful_abilities():
        # These abilities are typically much less common, so the characters should never be given skip_balancing
        # classification.
        classification = ItemClassification.progression
    elif abilities:
        # Characters, with only abilities where there are many other characters in the item pool providing those
        # abilities, are given deprioritized and skip_balancing classifications towards the end of create_items.
        classification = ItemClassification.progression
    elif inherit_progression_from_super_gonk_droid:
        # Special handling for Super Gonk Droid so that if Super Gonk Droid is relevant to logic, Gonk Droid is also
        # relevant to logic.
        classification = ItemClassification.progression
    elif name in _USEFUL_NON_PROGRESSION_CHARACTERS:
        # Force ghosts, glitchy characters and fast characters.
        classification = ItemClassification.useful

    if name == Character.ADMIRAL_ACKBAR.readable_name:
        # There is no trap functionality, this trap classification is a joke.
        # Maybe once/if the world switches to modding, receiving this item could play the iconic "It's a trap!"
        # line.
        classification |= ItemClassification.trap

    # If the character is not currently progression, but is used directly in some rules, then they need to be
    # considered as progression.
    if (relevant_item_counts is not None
            and classification & ItemClassification.progression == 0
            and relevant_item_counts.get(name, 0) > 0):
        # Remove useful classification, if set.
        classification &= ~ItemClassification.useful
        # And add progression classification.
        classification |= ItemClassification.progression

    # Some characters are really logically powerful so should be Prog+Useful, or at least Useful if they are not
    # Progression. It is desirable to mark them as Skip Balancing to disallow progression balancing from moving
    # them earlier.
    if name in _TOO_LOGICALLY_POWERFUL_CHARACTERS:
        classification |= ItemClassification.useful
        if ItemClassification.progression in classification:
            classification |= ItemClassification.skip_balancing
    return classification, abilities

def _evaluate_effective_other_data(world: LegoStarWarsTCSWorld,
                                   item_data: GenericItemData,
                                   relevant_item_counts: dict[str, int] | None = None) -> ItemClassification:
    name = item_data.name
    if name in MINIKITS_BY_NAME:
        # A goal macguffin.
        if world.goal_minikit_count > 0:
            # Options are special and raise an Exception when compared against a string that does not exist, so a
            # string literal is okay instead of the option value.
            if world.options.accessibility == "minimal" or world.minikit_bundle_count > 10:
                # Minikits are sorted first for minimal players in stage_fill_hook to reduce generation
                # failures, so should always be deprioritized for minimal players.
                return ItemClassification.progression_deprioritized_skip_balancing
            else:
                # If there are only very few bundles, e.g. the bundles are 10 minikits at a time and there are
                # not many in the pool, then don't use deprioritized classification.
                return ItemClassification.progression_skip_balancing
    elif name == NonDataItemName.PROGRESSIVE_SCORE_MULTIPLIER.value:
        # Generic item that grants Score multiplier Extras, which are used in logic for purchases from the shop.
        if relevant_item_counts is not None:
            if relevant_item_counts.get(name, 0) > 0:
                return ItemClassification.progression
            else:
                return ItemClassification.useful
        else:
            # todo: Vary between progression and progression_skip_balancing depending on what percentage of
            #  locations need them.
            return ItemClassification.progression
    elif name == NonDataItemName.EPISODE_COMPLETION_TOKEN.value:
        # Very few location checks and typically late into a seed.
        if (world.options.all_episodes_character_purchase_requirements
                == AllEpisodesCharacterPurchaseRequirements.option_episodes_tokens):
            return ItemClassification.progression_skip_balancing
    elif name == NonDataItemName.KYBER_BRICK.value:
        # Kyber Bricks are only logically relevant to the Kyber Bricks goal and do not unlock any locations, so
        # should skip progression balancing.
        if world.options.goal_requires_kyber_bricks:
            return ItemClassification.progression_skip_balancing
    elif name in EPISODE_UNLOCK_TO_EPISODE:
        # Episode Unlock item.
        if (EPISODE_UNLOCK_TO_EPISODE[name] in world.enabled_episodes
                and world.options.episode_unlock_requirement == EpisodeUnlockRequirement.option_episode_item):
            return ItemClassification.progression | ItemClassification.useful
    elif name in CHAPTER_UNLOCK_ITEM_TO_CHAPTER:
        # Chapter Unlock item.
        if CHAPTER_UNLOCK_ITEM_TO_CHAPTER[name] in world.enabled_chapters:
            return ItemClassification.progression
    # Everything else.
    return ItemClassification.filler

def evaluate_effective_item(world: LegoStarWarsTCSWorld,
                            name: str,
                            effective_character_abilities_lookup: dict[str, CharacterAbility] | None = None,
                            relevant_item_counts: dict[str, int] | None = None,
                            ) -> tuple[ItemClassification, CharacterAbility]:
    item_data = ITEM_DATA_BY_NAME[name]
    code = item_data.code
    if code is None or code < 1:
        raise RuntimeError(f"Error: Item '{name}' cannot be created")
    assert item_data.code != -1
    if isinstance(item_data, ExtraData):
        classification = _evaluate_effective_extra_data(world, item_data, relevant_item_counts)
        return classification, CharacterAbility.NONE
    elif isinstance(item_data, GenericCharacterData):
        return _evaluate_effective_character_data(
            world, item_data, effective_character_abilities_lookup, relevant_item_counts)
    else:
        classification = _evaluate_effective_other_data(world, item_data, relevant_item_counts)
        return classification, CharacterAbility.NONE
