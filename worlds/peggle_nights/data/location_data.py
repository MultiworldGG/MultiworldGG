from typing import Dict, NamedTuple, Optional, Tuple

from rule_builder.rules import Rule, Has

from ..enums import PeggleNightsAPItems, PeggleNightsAPTags, PeggleNightsLevels


class PeggleNightsLocationData(NamedTuple):
    archipelago_id: Optional[int]
    region: PeggleNightsLevels
    tags: Optional[Tuple[PeggleNightsAPTags, ...]] = None
    requirements: Optional[Rule] = None


location_offset: int = 1000000

location_data: Dict[str, PeggleNightsLocationData] = dict()

i: int
level: PeggleNightsLevels
for i, level in enumerate(PeggleNightsLevels):
    level_offset: int = 1000 * i
    location_prefix: str = f"{level.value} -"

    location_data[f"{location_prefix} Fever Meter X2"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 1,
        region=level,
        tags=(
            PeggleNightsAPTags.FEVER_METER_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} Fever Meter X3"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 2,
        region=level,
        tags=(
            PeggleNightsAPTags.FEVER_METER_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value, 1)
        ),
    )

    location_data[f"{location_prefix} Fever Meter X5"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 3,
        region=level,
        tags=(
            PeggleNightsAPTags.FEVER_METER_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value, 2)
        ),
    )

    location_data[f"{location_prefix} Fever Meter X10"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 4,
        region=level,
        tags=(
            PeggleNightsAPTags.FEVER_METER_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value, 3)
        ),
    )

    location_data[f"{location_prefix} Level Clear"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 5,
        region=level,
        tags=(
            PeggleNightsAPTags.LEVEL_CLEAR_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value, 4)
        ),
    )

    location_data[f"{location_prefix} Target Score (Low)"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 6,
        region=level,
        tags=(
            PeggleNightsAPTags.SCORE_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} Target Score (Mid)"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 7,
        region=level,
        tags=(
            PeggleNightsAPTags.SCORE_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value, 2)
        ),  # Rest of rule dynamically created in World
    )

    location_data[f"{location_prefix} Target Score (High)"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 8,
        region=level,
        tags=(
            PeggleNightsAPTags.SCORE_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value, 4)
        ),  # Rest of rule dynamically created in World
    )

    location_data[f"{location_prefix} Style Shot (25,000+)"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 9,
        region=level,
        tags=(
            PeggleNightsAPTags.STYLE_SHOT_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} 3 Orange Peg Combo"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 10,
        region=level,
        tags=(
            PeggleNightsAPTags.ORANGE_PEG_COMBO_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} 5 Orange Peg Combo"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 11,
        region=level,
        tags=(
            PeggleNightsAPTags.ORANGE_PEG_COMBO_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} 7 Peg Combo"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 12,
        region=level,
        tags=(
            PeggleNightsAPTags.PEG_COMBO_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} 15 Peg Combo"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 13,
        region=level,
        tags=(
            PeggleNightsAPTags.PEG_COMBO_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} Full Clear"] = PeggleNightsLocationData(
        archipelago_id=location_offset + level_offset + 14,
        region=level,
        tags=(
            PeggleNightsAPTags.FULL_CLEAR_LOCATION,
            getattr(PeggleNightsAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=None  # Rest of rule dynamically created in World
    )
