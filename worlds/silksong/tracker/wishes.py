TURN_INS = {
    'Bone Bottom Wishwall': (
        ('Bonetown', 285.64999, 9.38, 315.0, 90.0),
        (
            'Building Materials',
            'Building Materials (Bridge)',
            'Building Materials (Statue)',
            'Rock Rollers',
            'Skull King',
            'Save the Fleas Pre',
            'Mossberry Collection Pre',
        ),
    ),
    'Bellhart Wishwall': (
        ('Belltown', 48.45767, 5.752009, 109.0, 75.0),
        (
            'Belltown House Start',
            'Belltown House Mid',
            'Shiny Bell Goomba',
            'Beastfly Hunt',
            'Ant Trapper',
            'Save Courier Short',
            'Save Courier Tall',
            'Garmond Black Threaded',
            'Shakra Final Quest',
            'Pinstress Battle Pre',
            'Flea Games Pre',
            'Crow Feathers Pre',
        ),
    ),
    'Songclave Wishwall': (
        ('Song_Enclave', 70.555757, 4.579541, 120.0, 33.0),
        (
            'Songclave Donation 1',
            'Songclave Donation 2',
            'Fine Pins',
            'Song Pilgrim Cloaks',
            'Broodmother Hunt',
            'Save City Merchant',
            'Save City Merchant Bridge',
            'Save Sherma',
            'Tormented Trobbio',
            'Song Knight',
        ),
    ),
    'Gourmand Servant': (('Song_09b', 109.64, 132.79, 165.0, 146.0),
        ('Great Gourmand',)),
    'Pinmaster Plinney': (('Belltown_Room_pinsmith', 25.809999, 8.36, 55.0, 26.0),
        ('A Pinsmiths Tools',)),
    'Seamstress': (('Bone_East_Umbrella', 27.63, 8.37, 55.0, 26.0),
        ('Brolly Get',)),
    'Herald Tablet': (('Aqueduct_05', 238.389999, 84.800003, 332.0, 100.0),
        ('Mr Mushroom',)),
    'Alchemist': (('Crawl_08', 52.860001, 10.161187, 105.0, 22.0),
        ('Extractor Blue', 'Extractor Blue Worms')),
    'Huntress': (('Room_Huntress', 24.24, 10.43, 35.0, 25.0),
        ('Huntress Quest',)),
    'Yarnaby': (('Wisp_03', 50.790268, 5.916079, 179.0, 47.0),
        ('Doctor Curse Cure',)),
    'Greyroot': (('Room_Witch', 16.780001, 8.36, 33.0, 19.0),
        ('Shell Flowers', 'Wood Witch Curse')),
    'Zi': (('Coral_37', 65.670025, 8.64, 80.0, 21.0),
        ('Steel Sentinel',)),
    'Bellhart Couriers': (
        ('Belltown', 44.736, 21.337, 109.0, 75.0),
        (
            'Courier Delivery Bonebottom',
            'Courier Delivery Pilgrims Rest',
            'Courier Delivery Songclave',
            'Courier Delivery Fleatopia',
            'Courier Delivery Fixer',
            'Courier Delivery Dustpens Slave',
            'Courier Delivery Mask Maker',
        ),
    ),
}

CHECKS = {
    'Wish: Bone Bottom Repairs': ('Building Materials', 'Bone Bottom Wishwall'),
    'Wish: A Lifesaving Bridge': ('Building Materials (Bridge)', 'Bone Bottom Wishwall'),
    'Wish: An Icon of Hope': ('Building Materials (Statue)', 'Bone Bottom Wishwall'),
    'Wish: Garb of the Pilgrims': (None, 'Bone Bottom Wishwall'),
    'Wish: Volatile Flintbeetles': ('Rock Rollers', 'Bone Bottom Wishwall'),
    'Volatile Flintbeetles - Memory Locket': ('Rock Rollers', 'Bone Bottom Wishwall'),
    'Wish: The Terrible Tyrant': ('Skull King', 'Bone Bottom Wishwall'),
    'Wish: Restoration of Bellhart': ('Belltown House Start', 'Bellhart Wishwall'),
    "Wish: Bellhart's Glory": ('Belltown House Mid', 'Bellhart Wishwall'),
    "Wish: Hero's Call": (None, 'Bellhart Wishwall'),
    'Wish: Silver Bells': ('Shiny Bell Goomba', 'Bellhart Wishwall'),
    'Savage Beastfly - Mask Shard': ('Beastfly Hunt', 'Bellhart Wishwall'),
    'The Hidden Hunter - Mask Shard': ('Ant Trapper', 'Bellhart Wishwall'),
    'Wish: Fine Pins': ('Fine Pins', 'Songclave Wishwall'),
    'Wish: Cloaks of the Choir': ('Song Pilgrim Cloaks', 'Songclave Wishwall'),
    'Wish: Building Up Songclave': ('Songclave Donation 1', 'Songclave Wishwall'),
    'Wish: Strengthening Songclave': ('Songclave Donation 2', 'Songclave Wishwall'),
}


def location_mapping(world):
    sources = {target: source for source, target in world._progression_assignments.wishes}
    hosts = {offer: host for host, (_, offers) in TURN_INS.items() for offer in offers}
    mapping = {}
    for name, (identity, vanilla) in CHECKS.items():
        source = sources.get(identity)
        host = hosts[source] if source is not None else vanilla
        mapping[f'{host}/Turn-in: {name}'] = world.location_name_to_id[name]
    return mapping
