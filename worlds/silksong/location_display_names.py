from __future__ import annotations

MAPPER_LOCATION_NAMES: dict[str, str] = {
    'Shellwood - Rosary Cache': 'Rosary cache: Shellwood Top Room',
    'Shellwood - Shell Shard Cache #3': 'Shell Shard Cache: Greyroots Diddy Basement 3',
    'Shellwood - Shell Shard Cache #6': 'Shell shard Cache: Outside Longpin 3',
    'Pollip Heart: Shellwood #2': 'Pollip Heart Flower Room',
    'Shellwood - Shell Shard Cache #1': 'Shell Shard Cache: Greyroots Diddy Basement 1',
    'Shellwood - Shell Shard Cache #5': 'Shell shard Cache: Outside Longpin 2',
    'Shellwood - Shell Shard Cache #2': 'Shell Shard Cache: Greyroots Diddy Basement 2',
    'Pollip Heart: Shellwood #6': 'Pollip Heart Right Side Big Room',
    'Shellwood - Shell Shard Cache #4': 'Shell shard Cache: Outside Longpin 1',
    'Pollip Heart: Shellwood #5': 'Pollip Heart Hidden Room',
    'Pollip Heart: Shellwood #3': 'Pollip Heart Cling Grip Room',
    'Pollip Heart: Shellwood #1': 'Pollip Heart Left Big Room',
    'Mask Shard: Shellwood': 'Mask Shard: Shellwood',
}


def location_first_name(source_name: str) -> str:
    """Convert an item-first native source name to its display form."""
    if source_name in MAPPER_LOCATION_NAMES:
        return MAPPER_LOCATION_NAMES[source_name]
    if source_name in MAPPER_LOCATION_NAMES.values():
        return source_name
    item_name, separator, location_name = source_name.partition(": ")
    if not separator:
        return source_name
    area_name, number_separator, number = location_name.rpartition(" #")
    if number_separator and number.isdigit():
        return f"{area_name} - {item_name} #{number}"
    return f"{location_name} - {item_name}"
