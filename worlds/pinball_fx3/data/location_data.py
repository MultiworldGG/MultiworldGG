from typing import Dict, NamedTuple, Optional, Tuple

from rule_builder.rules import Rule, Has, Or

from ..data.mapping_data import table_to_table_groups
from ..enums import PinballFX3APItems, PinballFX3Tables, PinballFX3APTags


class PinballFX3LocationData(NamedTuple):
    archipelago_id: Optional[int]
    region: PinballFX3Tables
    tags: Optional[Tuple[PinballFX3APTags, ...]] = None
    requirements: Optional[Rule] = None


location_offset: int = 1000000

location_data: Dict[str, PinballFX3LocationData] = dict()

i: int
table: PinballFX3Tables
for i, table in enumerate(PinballFX3Tables):
    table_offset: int = 1000 * i
    location_prefix: str = f"{table.value} [{table_to_table_groups[table].value}] -"

    location_data[f"{location_prefix} Target Score (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 1,
        region=table,
        tags=(
            PinballFX3APTags.TARGET_SCORE_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.SINGLE_PLAYER_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} Target Score (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 2,
        region=table,
        tags=(
            PinballFX3APTags.TARGET_SCORE_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.SINGLE_PLAYER_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} Target Score (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 3,
        region=table,
        tags=(
            PinballFX3APTags.TARGET_SCORE_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.SINGLE_PLAYER_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Target Star (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 4,
        region=table,
        tags=(
            PinballFX3APTags.CHALLENGE_STAR_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Target Star (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 5,
        region=table,
        tags=(
            PinballFX3APTags.CHALLENGE_STAR_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Target Star (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 6,
        region=table,
        tags=(
            PinballFX3APTags.CHALLENGE_STAR_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Target Star (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 7,
        region=table,
        tags=(
            PinballFX3APTags.CHALLENGE_STAR_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Target Star (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 8,
        region=table,
        tags=(
            PinballFX3APTags.CHALLENGE_STAR_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Target Star (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 9,
        region=table,
        tags=(
            PinballFX3APTags.CHALLENGE_STAR_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Target Star (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 10,
        region=table,
        tags=(
            PinballFX3APTags.CHALLENGE_STAR_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Target Star (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 11,
        region=table,
        tags=(
            PinballFX3APTags.CHALLENGE_STAR_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Target Star (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 12,
        region=table,
        tags=(
            PinballFX3APTags.CHALLENGE_STAR_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 1 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 13,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_1_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 2 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 14,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_2_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 3 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 15,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_3_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 4 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 16,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_4_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 1 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 17,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_1_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 2 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 18,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_2_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 3 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 19,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_3_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 4 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 20,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_4_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 1 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 21,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_1_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 2 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 22,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_2_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 3 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 23,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_3_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} 1 Ball Challenge - Starsanity 4 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 24,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_4_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_1_BALL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_1_BALL_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 1 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 25,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_1_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 2 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 26,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_2_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 3 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 27,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_3_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 4 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 28,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_4_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 1 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 29,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_1_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 2 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 30,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_2_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 3 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 31,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_3_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 4 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 32,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_4_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 1 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 33,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_1_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 2 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 34,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_2_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 3 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 35,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_3_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} 5 Minute Challenge - Starsanity 4 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 36,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_4_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_5_MINUTE_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_5_MINUTE_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 1 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 37,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_1_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 2 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 38,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_2_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 3 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 39,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_3_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 4 (Low)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 40,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_4_LOCATION,
            PinballFX3APTags.LOW_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_LOW_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 1),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 1 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 41,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_1_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 2 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 42,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_2_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 3 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 43,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_3_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 4 (Mid)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 44,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_4_LOCATION,
            PinballFX3APTags.MID_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_MID_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 2),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 1 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 45,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_1_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 2 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 46,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_2_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 3 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 47,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_3_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 3),
            )
        )
    )

    location_data[f"{location_prefix} Survival Challenge - Starsanity 4 (High)"] = PinballFX3LocationData(
        archipelago_id=location_offset + table_offset + 48,
        region=table,
        tags=(
            PinballFX3APTags.STARSANITY_LOCATION,
            PinballFX3APTags.STARSANITY_4_LOCATION,
            PinballFX3APTags.HIGH_TIER_LOCATION,
            PinballFX3APTags.CHALLENGE_LOCATION,
            PinballFX3APTags.CHALLENGE_SURVIVAL_LOCATION,
            getattr(PinballFX3APTags, f"{table.name}_LOCATION"),
        ),
        requirements=(
            Or(
                Has(PinballFX3APItems.CHALLENGES_SURVIVAL_HIGH_TIER.value, 1),
                Has(PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value, 3),
            )
        )
    )
