from ...data.Locations import LOCATIONS_DATA

def write_spoiler(world, spoiler_handle):
    if world.seasons:
        from ...data.Constants import SEASON_NAMES
        spoiler_handle.write(f"\n\nDefault Seasons ({world.multiworld.player_name[world.player]}):\n")
        for region_name, season in world.default_seasons.items():
            spoiler_handle.write(f"\t- {region_name} --> {SEASON_NAMES[season]}\n")

    if world.options.shuffle_dungeons:
        spoiler_handle.write(f"\nDungeon Entrances ({world.multiworld.player_name[world.player]}):\n")
        for entrance, dungeon in world.dungeon_entrances.items():
            spoiler_handle.write(f"\t- {entrance} --> {dungeon.replace('enter ', '')}\n")

    if world.seasons and world.options.shuffle_portals != "vanilla":
        spoiler_handle.write(f"\nSubrosia Portals ({world.multiworld.player_name[world.player]}):\n")
        for portal_holo, portal_sub in world.portal_connections.items():
            spoiler_handle.write(f"\t- {portal_holo} --> {portal_sub}\n")

    spoiler_handle.write(f"\nShop Prices ({world.multiworld.player_name[world.player]}):\n")
    shop_codes = [code for shop in world.shop_order for code in shop]
    if world.seasons:
        from ...data.Constants import MARKET_LOCATIONS
        shop_codes.extend(MARKET_LOCATIONS)
    for shop_code in shop_codes:
        price = world.shop_prices[shop_code]
        for loc_name, loc_data in LOCATIONS_DATA.items():
            if loc_data.get("symbolic_name", None) is None or loc_data["symbolic_name"] != shop_code:
                continue
            if world.location_is_active(loc_name, loc_data):
                currency = "Ore Chunks" if world.seasons and shop_code.startswith("subrosia") else "Ore Chunks" if world.ages and shop_code.startswith("tokay") else "Rupees"
                spoiler_handle.write(f"\t- {loc_name}: {price} {currency}\n")
            break