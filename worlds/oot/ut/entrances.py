from ..EntranceShuffle import entrance_shuffle_table, invalidate_age_reachability, set_all_entrances_data

ENTRANCE_NAMES = {
    entrance[0]
    for row in entrance_shuffle_table
    for entrance in row[1:]
}
ENTRANCE_IDS = {name: index for index, name in enumerate(sorted(ENTRANCE_NAMES))}
FOUND_ENTRANCES_KEY = "oot_entrances_{team}_{player}"

def tracked_entrances(world):
    return {entrance.name: entrance for entrance in world.get_entrances() if entrance.name in ENTRANCE_NAMES}


def serialize_entrances(world):
    return {
        name: {
            "region": entrance.connected_region.name,
            "replaces": entrance.replaces.name if entrance.replaces else None,
            "shuffled": entrance.shuffled,
        }
        for name, entrance in tracked_entrances(world).items()
    }


def restore_entrances(world, snapshot):
    entrances = tracked_entrances(world)
    if entrances.keys() != snapshot.keys():
        raise ValueError("Universal Tracker entrance snapshot does not match this world's entrances")

    # Resolve the whole snapshot before changing any connections.
    connections = []
    for name, entrance in entrances.items():
        record = snapshot[name]
        region = world.get_region(record["region"])
        replacement = entrances[record["replaces"]] if record["replaces"] is not None else None
        connections.append((entrance, region, replacement, record["shuffled"]))

    if world.entrance_shuffle:
        set_all_entrances_data(world.multiworld, world.player)
    for entrance, region, replacement, shuffled in connections:
        entrance.disconnect()
        entrance.connect(region)
        entrance.replaces = replacement
        entrance.shuffled = shuffled

    invalidate_age_reachability(world.multiworld.state, world.player)
    world.multiworld.state.stale[world.player] = True


def defer_entrances(world):
    """Run after generation cleanup, while the full graph's events still exist."""
    world.ut_deferred_entrances = {}
    if world.ut_replay_slot_data is None or getattr(world.multiworld, "enforce_deferred_connections", "off") == "off":
        return
    for name, entrance in tracked_entrances(world).items():
        # Blue warps are rerouted by boss/dungeon ER without being marked shuffled.
        if not entrance.shuffled and not (entrance.type == "BlueWarp" and entrance.replaces):
            continue
        world.ut_deferred_entrances[name] = entrance.connected_region
        entrance.disconnect()
    # Generation may have cached reachability through the complete layout.
    invalidate_age_reachability(world.multiworld.state, world.player)
    world.multiworld.state.reachable_regions[world.player].clear()
    world.multiworld.state.blocked_connections[world.player].clear()
    world.multiworld.state.stale[world.player] = True


def reconnect_found_entrances(world, storage_key, discoveries):
    if not world.ut_deferred_entrances or not discoveries:
        return
    for name in discoveries:
        if name not in world.ut_deferred_entrances:
            continue
        entrance = world.get_entrance(name)
        to_connect = [entrance]
        if not world.decouple_entrances and entrance.reverse and entrance.replaces:
            # The return is at the destination, not the source's vanilla reverse.
            to_connect.append(entrance.replaces.reverse)
        for connection in to_connect:
            if connection and connection.name in world.ut_deferred_entrances and connection.connected_region is None:
                connection.connect(world.ut_deferred_entrances[connection.name])
    invalidate_age_reachability(world.multiworld.state, world.player)
    world.multiworld.state.stale[world.player] = True
