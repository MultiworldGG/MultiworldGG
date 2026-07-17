from .game_data import data

def item_list():
    items = []

    for name in data['unlocks'].keys():
        items.append(f'{name} Unlock')

    for item in data['items']:
        items.append(item)

    return items

def item_group_list():
    item_name_groups = {}

    for name in data['unlocks'].keys():
        add_to_item_group(item_name_groups, "Unlocks", f'{name} Unlock')

    for item in data['items']:
        if item.endswith(" Item"):
            add_to_item_group(item_name_groups, "Items", item)
        if item.startswith("Random "):
            add_to_item_group(item_name_groups, "Junk", item)
        if item.endswith(" Trap"):
            add_to_item_group(item_name_groups, "Traps", item)
        if item.startswith("Permanent "):
            add_to_item_group(item_name_groups, "Stat Ups", item)

    return item_name_groups

def add_to_item_group(item_name_groups, group, item):
    if group not in item_name_groups:
        item_name_groups[group] = set()
    item_name_groups[group].add(item)