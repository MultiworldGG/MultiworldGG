def gen_flag_byte(location_data):
    """
    Calculates a flag byte based off of a room that a user is in.

    Parameters:
        object: data of all given locations.

    Returns:
        object: locations with their filled flag bytes.
    """
    for location in location_data.values():
        if "flag_byte" not in location:
            room = location["room"]
            if room >= 0x200:
                if room >= 0x300:
                    if room >= 0x600:
                        room -= 0x200
                    room -= 0x100
                room -= 0x100
            location["flag_byte"] = 0xc700 + room
    return location_data