from collections.abc import Callable
from typing import Literal

from BaseClasses import Region

from .constants import (
    CHARACTER_REGION_TEMPLATE,
    CRATE_DROP_GROUP_REGION_TEMPLATE,
    CRATE_DROP_LOCATION_TEMPLATE,
    LEGENDARY_CRATE_DROP_GROUP_REGION_TEMPLATE,
    LEGENDARY_CRATE_DROP_LOCATION_TEMPLATE,
    NUM_WAVES,
    RUN_COMPLETE_LOCATION_TEMPLATE,
    WAVE_COMPLETE_LOCATION_TEMPLATE,
)
from .locations import BrotatoCommonCrateLocation, BrotatoLegendaryCrateLocation, BrotatoLocation, location_table
from .loot_crates import BrotatoLootCrateGroup
from .rules import create_can_reach_wave_rule, create_has_character_rule, create_has_run_wins_rule

RegionFactory = Callable[[str], Region]


def create_regions(
    region_factory: RegionFactory,
    characters: list[str],
    waves_with_checks: list[int],
    wave_access: dict[int, int],
    common_loot_crate_groups: list[BrotatoLootCrateGroup],
    legendary_loot_crate_groups: list[BrotatoLootCrateGroup],
) -> list[Region]:
    menu_region: Region = region_factory("Menu")

    regions: list[Region] = [menu_region]

    crate_type_and_groups: list[tuple[Literal["common", "legendary"], list[BrotatoLootCrateGroup]]] = [
        ("common", common_loot_crate_groups),
        ("legendary", legendary_loot_crate_groups),
    ]
    for loot_crate_type, loot_crate_groups in crate_type_and_groups:
        crate_count: int = 1
        for group in loot_crate_groups:
            loot_crate_group_region = create_loot_crate_group_region(
                region_factory, group, loot_crate_type, crate_count_start=crate_count
            )
            crate_count += group.num_crates
            has_wins_rule = create_has_run_wins_rule(loot_crate_group_region.player, group.wins_to_unlock)
            menu_region.connect(loot_crate_group_region, name=loot_crate_group_region.name, rule=has_wins_rule)
            regions.append(loot_crate_group_region)

    for char in characters:
        character_region = create_character_region(region_factory, char, waves_with_checks, wave_access)
        has_character_rule = create_has_character_rule(character_region.player, char)
        menu_region.connect(character_region, f"Start Game ({char})", rule=has_character_rule)
        regions.append(character_region)

    return regions


def create_character_region(
    create_region: RegionFactory,
    character: str,
    waves_with_checks: list[int],
    wave_access: dict[int, int],
) -> Region:
    character_region: Region = create_region(CHARACTER_REGION_TEMPLATE.format(char=character))
    run_complete_location_name = RUN_COMPLETE_LOCATION_TEMPLATE.format(char=character)
    run_complete_location_id = location_table[run_complete_location_name].id
    run_complete_location = BrotatoLocation(
        character_region.player,
        name=run_complete_location_name,
        address=run_complete_location_id,
        parent=character_region,
    )
    # All wave cap increases are needed to reach the final wave.
    run_complete_location.access_rule = create_can_reach_wave_rule(
        character_region.player, character, wave_access[NUM_WAVES]
    )
    character_region.locations.append(run_complete_location)

    for wave in waves_with_checks:
        if wave not in range(1, NUM_WAVES + 1):
            raise ValueError(f"Invalid wave number {wave}.")
        wave_complete_location_name = WAVE_COMPLETE_LOCATION_TEMPLATE.format(wave=wave, char=character)
        wave_complete_location_id = location_table[wave_complete_location_name].id

        wave_complete_location = BrotatoLocation(
            character_region.player,
            name=wave_complete_location_name,
            address=wave_complete_location_id,
            parent=character_region,
        )

        num_wave_cap_items_needed_for_wave = wave_access[wave]
        wave_complete_location.access_rule = create_can_reach_wave_rule(
            character_region.player, character, num_wave_cap_items_needed_for_wave
        )
        character_region.locations.append(wave_complete_location)

    return character_region


def create_loot_crate_group_region(
    create_region: RegionFactory,
    loot_crate_group: BrotatoLootCrateGroup,
    crate_type: Literal["common", "legendary"],
    crate_count_start: int = 1,
) -> Region:
    if crate_type == "common":
        location_name_template = CRATE_DROP_LOCATION_TEMPLATE
        region_name_template = CRATE_DROP_GROUP_REGION_TEMPLATE
        location_cls = BrotatoCommonCrateLocation
    else:
        location_name_template = LEGENDARY_CRATE_DROP_LOCATION_TEMPLATE
        region_name_template = LEGENDARY_CRATE_DROP_GROUP_REGION_TEMPLATE
        location_cls = BrotatoLegendaryCrateLocation

    group_region: Region = create_region(region_name_template.format(num=loot_crate_group.index))
    group_locations: dict[str, int | None] = {}
    for crate_index in range(crate_count_start, crate_count_start + loot_crate_group.num_crates):
        crate_location_name = location_name_template.format(num=crate_index)
        group_locations[crate_location_name] = location_table[crate_location_name].id

    if not group_locations:
        raise ValueError(
            f"No loot crate locations created for {loot_crate_group=}, {crate_type=}, {crate_count_start=}."
        )

    group_region.add_locations(group_locations, location_cls)

    return group_region
