from typing import Dict, NamedTuple, Optional, Tuple

from rule_builder.rules import Rule, Has

from ..enums import PeggleDeluxeAPItems, PeggleDeluxeAPTags, PeggleDeluxeLevels


class PeggleDeluxeLocationData(NamedTuple):
    archipelago_id: Optional[int]
    region: PeggleDeluxeLevels
    tags: Optional[Tuple[PeggleDeluxeAPTags, ...]] = None
    requirements: Optional[Rule] = None


location_offset: int = 1000000

location_data: Dict[str, PeggleDeluxeLocationData] = dict()

i: int
level: PeggleDeluxeLevels
for i, level in enumerate(PeggleDeluxeLevels):
    level_offset: int = 1000 * i
    location_prefix: str = f"{level.value} -"

    location_data[f"{location_prefix} Fever Meter X2"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 1,
        region=level,
        tags=(
            PeggleDeluxeAPTags.FEVER_METER_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} Fever Meter X3"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 2,
        region=level,
        tags=(
            PeggleDeluxeAPTags.FEVER_METER_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleDeluxeAPItems.PROGRESSIVE_FEVER_METER.value, 1)
        ),
    )

    location_data[f"{location_prefix} Fever Meter X5"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 3,
        region=level,
        tags=(
            PeggleDeluxeAPTags.FEVER_METER_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleDeluxeAPItems.PROGRESSIVE_FEVER_METER.value, 2)
        ),
    )

    location_data[f"{location_prefix} Fever Meter X10"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 4,
        region=level,
        tags=(
            PeggleDeluxeAPTags.FEVER_METER_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleDeluxeAPItems.PROGRESSIVE_FEVER_METER.value, 3)
        ),
    )

    location_data[f"{location_prefix} Level Clear"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 5,
        region=level,
        tags=(
            PeggleDeluxeAPTags.LEVEL_CLEAR_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleDeluxeAPItems.PROGRESSIVE_FEVER_METER.value, 4)
        ),
    )

    location_data[f"{location_prefix} Target Score (Low)"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 6,
        region=level,
        tags=(
            PeggleDeluxeAPTags.SCORE_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} Target Score (Mid)"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 7,
        region=level,
        tags=(
            PeggleDeluxeAPTags.SCORE_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleDeluxeAPItems.PROGRESSIVE_FEVER_METER.value, 2)
        ),  # Rest of rule dynamically created in World
    )

    location_data[f"{location_prefix} Target Score (High)"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 8,
        region=level,
        tags=(
            PeggleDeluxeAPTags.SCORE_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=(
            Has(PeggleDeluxeAPItems.PROGRESSIVE_FEVER_METER.value, 4)
        ),  # Rest of rule dynamically created in World
    )

    location_data[f"{location_prefix} Style Shot (25,000+)"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 9,
        region=level,
        tags=(
            PeggleDeluxeAPTags.STYLE_SHOT_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} 3 Orange Peg Combo"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 10,
        region=level,
        tags=(
            PeggleDeluxeAPTags.ORANGE_PEG_COMBO_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} 5 Orange Peg Combo"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 11,
        region=level,
        tags=(
            PeggleDeluxeAPTags.ORANGE_PEG_COMBO_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} 7 Peg Combo"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 12,
        region=level,
        tags=(
            PeggleDeluxeAPTags.PEG_COMBO_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} 15 Peg Combo"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 13,
        region=level,
        tags=(
            PeggleDeluxeAPTags.PEG_COMBO_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
    )

    location_data[f"{location_prefix} Full Clear"] = PeggleDeluxeLocationData(
        archipelago_id=location_offset + level_offset + 14,
        region=level,
        tags=(
            PeggleDeluxeAPTags.FULL_CLEAR_LOCATION,
            getattr(PeggleDeluxeAPTags, f"{level.name}_LOCATION"),
        ),
        requirements=None  # Rest of rule dynamically created in World
    )
