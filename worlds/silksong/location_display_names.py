from __future__ import annotations

def location_first_name(source_name: str) -> str:
    """Convert an item-first native source name to its display form."""
    item_name, separator, location_name = source_name.partition(": ")
    if not separator:
        return source_name
    area_name, number_separator, number = location_name.rpartition(" #")
    if number_separator and number.isdigit():
        return f"{area_name} - {item_name} #{number}"
    return f"{location_name} - {item_name}"
