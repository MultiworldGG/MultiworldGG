from typing import Dict, NamedTuple, Optional, Tuple

from BaseClasses import ItemClassification

from ..enums import (
    PeggleDeluxeAPItems,
    PeggleDeluxeAPTags,
    PeggleDeluxeAPUsefulItems,
    PeggleDeluxeLevels,
)


class PeggleDeluxeItemData(NamedTuple):
    archipelago_id: Optional[int]
    classification: ItemClassification
    tags: Tuple[PeggleDeluxeAPTags, ...]


item_offset: int = 1000000

item_data: Dict[str, PeggleDeluxeItemData] = {
    # Goal Items
    PeggleDeluxeAPItems.GOLD_PEG.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 2,
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        tags=(PeggleDeluxeAPTags.GOAL_ITEM,),
    ),
    # Progressive Items
    PeggleDeluxeAPItems.PROGRESSIVE_FEVER_METER.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 10 + 1,
        classification=ItemClassification.progression,
        tags=(PeggleDeluxeAPTags.PROGRESSIVE_ITEM,),
    ),
    PeggleDeluxeAPItems.PROGRESSIVE_STARTING_BALL_INCREASE.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 10 + 2,
        classification=ItemClassification.progression,
        tags=(PeggleDeluxeAPTags.PROGRESSIVE_ITEM,),
    ),
    # Character Unlock Items
    PeggleDeluxeAPItems.CHARACTER_UNLOCK_BJORN.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 100 + 1,
        classification=ItemClassification.useful,
        tags=(PeggleDeluxeAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleDeluxeAPItems.CHARACTER_UNLOCK_JIMMY_LIGHTNING.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 100 + 2,
        classification=ItemClassification.useful,
        tags=(PeggleDeluxeAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleDeluxeAPItems.CHARACTER_UNLOCK_KAT_TUT.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 100 + 3,
        classification=ItemClassification.useful,
        tags=(PeggleDeluxeAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleDeluxeAPItems.CHARACTER_UNLOCK_SPLORK.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 100 + 4,
        classification=ItemClassification.useful,
        tags=(PeggleDeluxeAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleDeluxeAPItems.CHARACTER_UNLOCK_CLAUDE.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 100 + 5,
        classification=ItemClassification.useful,
        tags=(PeggleDeluxeAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleDeluxeAPItems.CHARACTER_UNLOCK_RENFIELD.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 100 + 6,
        classification=ItemClassification.useful,
        tags=(PeggleDeluxeAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleDeluxeAPItems.CHARACTER_UNLOCK_TULA.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 100 + 7,
        classification=ItemClassification.useful,
        tags=(PeggleDeluxeAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleDeluxeAPItems.CHARACTER_UNLOCK_WARREN.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 100 + 8,
        classification=ItemClassification.useful,
        tags=(PeggleDeluxeAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleDeluxeAPItems.CHARACTER_UNLOCK_LORD_CINDERBOTTOM.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 100 + 9,
        classification=ItemClassification.useful,
        tags=(PeggleDeluxeAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    PeggleDeluxeAPItems.CHARACTER_UNLOCK_MASTER_HU.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 100 + 10,
        classification=ItemClassification.useful,
        tags=(PeggleDeluxeAPTags.CHARACTER_UNLOCK_ITEM,),
    ),
    # Filler Items
    PeggleDeluxeAPItems.BRITTLE_PEG.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 1000 + 1,
        classification=ItemClassification.filler,
        tags=(PeggleDeluxeAPTags.FILLER_ITEM,),
    ),
    PeggleDeluxeAPItems.CHIPPED_PEG.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 1000 + 2,
        classification=ItemClassification.filler,
        tags=(PeggleDeluxeAPTags.FILLER_ITEM,),
    ),
    PeggleDeluxeAPItems.DENTED_PEG.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 1000 + 3,
        classification=ItemClassification.filler,
        tags=(PeggleDeluxeAPTags.FILLER_ITEM,),
    ),
    PeggleDeluxeAPItems.HOLLOW_PEG.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 1000 + 4,
        classification=ItemClassification.filler,
        tags=(PeggleDeluxeAPTags.FILLER_ITEM,),
    ),
    PeggleDeluxeAPItems.RUSTY_PEG.value: PeggleDeluxeItemData(
        archipelago_id=item_offset + 1000 + 5,
        classification=ItemClassification.filler,
        tags=(PeggleDeluxeAPTags.FILLER_ITEM,),
    ),
}

# Level Items
item_offset = 10000

i: int
level: PeggleDeluxeLevels
for i, level in enumerate(PeggleDeluxeLevels):
    level_offset: int = 100 * i

    # Level Unlock Item
    item_data[f"Level Unlock: {level.value}"] = PeggleDeluxeItemData(
        archipelago_id=item_offset + level_offset + 1,
        classification=ItemClassification.progression,
        tags=(
            PeggleDeluxeAPTags.LEVEL_UNLOCK_ITEM,
            eval(f"PeggleDeluxeAPTags.{level.name}_ITEM"),
        ),
    )

    # Useful Items
    item_data[f"{PeggleDeluxeAPUsefulItems.FEVER_METER_BONUS.value}: {level.value}"] = PeggleDeluxeItemData(
        archipelago_id=item_offset + level_offset + 2,
        classification=ItemClassification.useful,
        tags=(
            PeggleDeluxeAPTags.USEFUL_ITEM,
            eval(f"PeggleDeluxeAPTags.{level.name}_ITEM"),
        ),
    )

    item_data[f"{PeggleDeluxeAPUsefulItems.FULL_CLEAR_DISCOUNT.value}: {level.value}"] = PeggleDeluxeItemData(
        archipelago_id=item_offset + level_offset + 3,
        classification=ItemClassification.useful,
        tags=(
            PeggleDeluxeAPTags.USEFUL_ITEM,
            eval(f"PeggleDeluxeAPTags.{level.name}_ITEM"),
        ),
    )

    item_data[f"{PeggleDeluxeAPUsefulItems.SCORE_MULTIPLIER.value}: {level.value}"] = PeggleDeluxeItemData(
        archipelago_id=item_offset + level_offset + 4,
        classification=ItemClassification.useful,
        tags=(
            PeggleDeluxeAPTags.USEFUL_ITEM,
            eval(f"PeggleDeluxeAPTags.{level.name}_ITEM"),
        ),
    )

    item_data[f"{PeggleDeluxeAPUsefulItems.TARGET_SCORE_DISCOUNT.value}: {level.value}"] = PeggleDeluxeItemData(
        archipelago_id=item_offset + level_offset + 5,
        classification=ItemClassification.useful,
        tags=(
            PeggleDeluxeAPTags.USEFUL_ITEM,
            eval(f"PeggleDeluxeAPTags.{level.name}_ITEM"),
        ),
    )
