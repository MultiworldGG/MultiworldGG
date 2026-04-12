from typing import Dict, NamedTuple, Optional, Tuple

from BaseClasses import ItemClassification

from ..enums import (
    PinballFX3APItems,
    PinballFX3APTags,
    PinballFX3APUsefulItems,
    PinballFX3Tables,
)


class PinballFX3ItemData(NamedTuple):
    archipelago_id: Optional[int]
    classification: ItemClassification
    tags: Tuple[PinballFX3APTags, ...]


item_offset: int = 1000000

item_data: Dict[str, PinballFX3ItemData] = {
    # Victory and Goal Items
    PinballFX3APItems.VICTORY.value: PinballFX3ItemData(
        archipelago_id=item_offset + 1,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.VICTORY_ITEM,),
    ),
    PinballFX3APItems.SHINY_QUARTER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 2,
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        tags=(PinballFX3APTags.GOAL_ITEM,),
    ),
    # Challenge Access Items
    PinballFX3APItems.CHALLENGES_1_BALL_LOW_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 1,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.CHALLENGES_1_BALL_MID_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 2,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.CHALLENGES_1_BALL_HIGH_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 3,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.CHALLENGES_5_MINUTE_LOW_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 4,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.CHALLENGES_5_MINUTE_MID_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 5,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.CHALLENGES_5_MINUTE_HIGH_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 6,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.CHALLENGES_SURVIVAL_LOW_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 7,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.CHALLENGES_SURVIVAL_MID_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 8,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.CHALLENGES_SURVIVAL_HIGH_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 9,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 10,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.PROGRESSIVE_CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 11,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.PROGRESSIVE_CHALLENGE_ACCESS_ITEM,),
    ),
    PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 10 + 12,
        classification=ItemClassification.progression,
        tags=(PinballFX3APTags.PROGRESSIVE_CHALLENGE_ACCESS_ITEM,),
    ),
    # Filler Items
    PinballFX3APItems.CRACKED_QUARTER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 100 + 1,
        classification=ItemClassification.filler,
        tags=(PinballFX3APTags.FILLER_ITEM,),
    ),
    PinballFX3APItems.DIRTY_QUARTER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 100 + 2,
        classification=ItemClassification.filler,
        tags=(PinballFX3APTags.FILLER_ITEM,),
    ),
    PinballFX3APItems.DULL_QUARTER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 100 + 3,
        classification=ItemClassification.filler,
        tags=(PinballFX3APTags.FILLER_ITEM,),
    ),
    PinballFX3APItems.FADED_QUARTER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 100 + 4,
        classification=ItemClassification.filler,
        tags=(PinballFX3APTags.FILLER_ITEM,),
    ),
    PinballFX3APItems.WORN_QUARTER.value: PinballFX3ItemData(
        archipelago_id=item_offset + 100 + 5,
        classification=ItemClassification.filler,
        tags=(PinballFX3APTags.FILLER_ITEM,),
    ),
}

# Table Items
item_offset = 100000

i: int
table: PinballFX3Tables
for i, table in enumerate(PinballFX3Tables):
    table_offset: int = 100 * i

    # Table Unlock Item
    item_data[f"Table Unlock: {table.value}"] = PinballFX3ItemData(
        archipelago_id=item_offset + table_offset + 1,
        classification=ItemClassification.progression,
        tags=(
            PinballFX3APTags.TABLE_UNLOCK_ITEM,
            getattr(PinballFX3APTags, f"{table.name}_ITEM"),
        ),
    )

    # Useful Items
    item_data[f"{PinballFX3APUsefulItems.SCORE_MULTIPLIER.value}: {table.value}"] = PinballFX3ItemData(
        archipelago_id=item_offset + table_offset + 2,
        classification=ItemClassification.useful,
        tags=(
            PinballFX3APTags.USEFUL_ITEM,
            getattr(PinballFX3APTags, f"{table.name}_ITEM"),
        ),
    )

    item_data[f"{PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT.value}: {table.value}"] = PinballFX3ItemData(
        archipelago_id=item_offset + table_offset + 3,
        classification=ItemClassification.useful,
        tags=(
            PinballFX3APTags.USEFUL_ITEM,
            getattr(PinballFX3APTags, f"{table.name}_ITEM"),
        ),
    )

    item_data[f"{PinballFX3APUsefulItems.TARGET_SCORE_DISCOUNT.value}: {table.value}"] = PinballFX3ItemData(
        archipelago_id=item_offset + table_offset + 4,
        classification=ItemClassification.useful,
        tags=(
            PinballFX3APTags.USEFUL_ITEM,
            getattr(PinballFX3APTags, f"{table.name}_ITEM"),
        ),
    )
