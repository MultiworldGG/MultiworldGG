from ..Items import oot_is_item_of_type


def shop_locations(world):
    return {
        location.name: location for location in world.get_locations()
        if location.type == 'Shop' and location.name not in world.shop_prices
    }


def serialize_shop_items(world):
    locations = shop_locations(world)
    if any(not oot_is_item_of_type(location.item, 'Shop') for location in locations.values()):
        raise ValueError("Universal Tracker shop snapshot requires completed shop placement")
    return {name: location.item.name for name, location in locations.items()}


def restore_shop_items(world, snapshot):
    """Restore ordinary stock before pool division; UT never runs pre_fill."""
    locations = shop_locations(world)
    if locations.keys() != snapshot.keys():
        raise ValueError("Universal Tracker shop snapshot does not match this world's shop slots")

    # Validate before mutating. Vanilla shops are already filled by ItemPool;
    # shuffled ordinary stock must come from the seed's saved placements.
    items = {}
    for name, location in locations.items():
        item = location.item if location.item is not None else world.create_item(snapshot[name])
        if not oot_is_item_of_type(item, 'Shop') or item.name != snapshot[name]:
            raise ValueError(f"Invalid Universal Tracker shop item at {name}: {snapshot[name]}")
        items[name] = item

    # Regeneration may have sampled different stock, including different junk
    # counts. Discard the whole provisional shop pool, not matching copies.
    world.itempool = [item for item in world.itempool if not oot_is_item_of_type(item, 'Shop')]
    for name, location in locations.items():
        if location.item is None:
            location.place_locked_item(items[name])
        location.locked = True
        location.address = None
        location.show_in_spoiler = False
