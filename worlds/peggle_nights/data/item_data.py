from typing import Dict, NamedTuple, Optional, Tuple

from BaseClasses import ItemClassification

from ..enums import (
    PeggleNightsAPItems,
    PeggleNightsAPTags,
    PeggleNightsAPUsefulItems,
    PeggleNightsLevels,
)


class PeggleNightsItemData(NamedTuple):
    archipelago_id: Optional[int]
    classification: ItemClassification
    tags: Tuple[PeggleNightsAPTags, ...]


item_offset: int = 1000000

item_data: Dict[str, PeggleNightsItemData] = {
    # Goal Items
    PeggleNightsAPItems.SHADOW_PEG.value: PeggleNightsItemData(
        archipelago_id=item_offset + 2,
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        tags=(PeggleNightsAPTags.GOAL_ITEM,),
    ),
    # Progressive Items
    PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value: PeggleNightsItemData(
        archipelago_id=item_offset + 10 + 1,
        classification=ItemClassification.progression,
        tags=(PeggleNightsAPTags.PROGRESSIVE_ITEM,),
    ),
    PeggleNightsAPItems.PROGRESSIVE_STARTING_BALL_INCREASE.value: PeggleNightsItemData(
        archipelago_id=item_offset + 10 + 2,
        classification=ItemClassification.progression,
        tags=(PeggleNightsAPTags.PROGRESSIVE_ITEM,),
    ),
    # Character Unlock Items
    PeggleNightsAPItems.CHARACTER_UNLOCK_BJORN.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 1,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleNightsAPItems.CHARACTER_UNLOCK_JIMMY_LIGHTNING.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 2,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleNightsAPItems.CHARACTER_UNLOCK_KAT_TUT.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 3,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleNightsAPItems.CHARACTER_UNLOCK_SPLORK.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 4,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleNightsAPItems.CHARACTER_UNLOCK_CLAUDE.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 5,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleNightsAPItems.CHARACTER_UNLOCK_RENFIELD.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 6,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleNightsAPItems.CHARACTER_UNLOCK_TULA.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 7,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleNightsAPItems.CHARACTER_UNLOCK_WARREN.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 8,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleNightsAPItems.CHARACTER_UNLOCK_LORD_CINDERBOTTOM.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 9,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleNightsAPItems.CHARACTER_UNLOCK_MASTER_HU.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 10,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleNightsAPItems.CHARACTER_UNLOCK_MARINA.value: PeggleNightsItemData(
        archipelago_id=item_offset + 100 + 11,
        classification=ItemClassification.useful,
        tags=(PeggleNightsAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    # Filler Items
    PeggleNightsAPItems.BRITTLE_PEG.value: PeggleNightsItemData(
        archipelago_id=item_offset + 1000 + 1,
        classification=ItemClassification.filler,
        tags=(PeggleNightsAPTags.FILLER_ITEM,),
    ),
    PeggleNightsAPItems.CHIPPED_PEG.value: PeggleNightsItemData(
        archipelago_id=item_offset + 1000 + 2,
        classification=ItemClassification.filler,
        tags=(PeggleNightsAPTags.FILLER_ITEM,),
    ),
    PeggleNightsAPItems.DENTED_PEG.value: PeggleNightsItemData(
        archipelago_id=item_offset + 1000 + 3,
        classification=ItemClassification.filler,
        tags=(PeggleNightsAPTags.FILLER_ITEM,),
    ),
    PeggleNightsAPItems.HOLLOW_PEG.value: PeggleNightsItemData(
        archipelago_id=item_offset + 1000 + 4,
        classification=ItemClassification.filler,
        tags=(PeggleNightsAPTags.FILLER_ITEM,),
    ),
    PeggleNightsAPItems.RUSTY_PEG.value: PeggleNightsItemData(
        archipelago_id=item_offset + 1000 + 5,
        classification=ItemClassification.filler,
        tags=(PeggleNightsAPTags.FILLER_ITEM,),
    ),
}

# Level Items
item_offset = 10000

i: int
level: PeggleNightsLevels
for i, level in enumerate(PeggleNightsLevels):
    level_offset: int = 100 * i

    # Level Unlock Item
    item_data[f"Level Unlock: {level.value}"] = PeggleNightsItemData(
        archipelago_id=item_offset + level_offset + 1,
        classification=ItemClassification.progression,
        tags=(
            PeggleNightsAPTags.LEVEL_UNLOCK_ITEM,
            eval(f"PeggleNightsAPTags.{level.name}_ITEM"),
        ),
    )

    # Useful Items
    item_data[f"{PeggleNightsAPUsefulItems.FEVER_METER_BONUS.value}: {level.value}"] = PeggleNightsItemData(
        archipelago_id=item_offset + level_offset + 2,
        classification=ItemClassification.useful,
        tags=(
            PeggleNightsAPTags.USEFUL_ITEM,
            eval(f"PeggleNightsAPTags.{level.name}_ITEM"),
        ),
    )

    item_data[f"{PeggleNightsAPUsefulItems.FULL_CLEAR_DISCOUNT.value}: {level.value}"] = PeggleNightsItemData(
        archipelago_id=item_offset + level_offset + 3,
        classification=ItemClassification.useful,
        tags=(
            PeggleNightsAPTags.USEFUL_ITEM,
            eval(f"PeggleNightsAPTags.{level.name}_ITEM"),
        ),
    )

    item_data[f"{PeggleNightsAPUsefulItems.SCORE_MULTIPLIER.value}: {level.value}"] = PeggleNightsItemData(
        archipelago_id=item_offset + level_offset + 4,
        classification=ItemClassification.useful,
        tags=(
            PeggleNightsAPTags.USEFUL_ITEM,
            eval(f"PeggleNightsAPTags.{level.name}_ITEM"),
        ),
    )

    item_data[f"{PeggleNightsAPUsefulItems.TARGET_SCORE_DISCOUNT.value}: {level.value}"] = PeggleNightsItemData(
        archipelago_id=item_offset + level_offset + 5,
        classification=ItemClassification.useful,
        tags=(
            PeggleNightsAPTags.USEFUL_ITEM,
            eval(f"PeggleNightsAPTags.{level.name}_ITEM"),
        ),
    )
