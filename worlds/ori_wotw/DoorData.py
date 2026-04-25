"""
Generated file, do not edit manually.

See https://github.com/Satisha10/APworld_wotw_extractors for the code.
Generated with `extract_rules.py`.
"""


doors_vanilla: list[tuple[str, str]] = [  # Vanilla door connections
    ('GladesTown.TwillenHome (Door)', 'GladesTown.KeyMokiHutInside (Door)'),
    ('GladesTown.KeyMokiHutInside (Door)', 'GladesTown.TwillenHome (Door)'),
    ('GladesTown.MotayHutDoor (Door)', 'GladesTown.MotayHutInside (Door)'),
    ('GladesTown.MotayHutInside (Door)', 'GladesTown.MotayHutDoor (Door)'),
    ('GladesTown.UpperWest (Door)', 'GladesTown.InsideThirdHut (Door)'),
    ('GladesTown.InsideThirdHut (Door)', 'GladesTown.UpperWest (Door)'),
    ('GladesTown.AcornMoki (Door)', 'GladesTown.AcornCave (Door)'),
    ('GladesTown.AcornCave (Door)', 'GladesTown.AcornMoki (Door)'),
    ('GladesTown.AboveOpher (Door)', 'GladesTown.StorageHut (Door)'),
    ('GladesTown.StorageHut (Door)', 'GladesTown.AboveOpher (Door)'),
    ('GladesTown.LupoHouse (Door)', 'GladesTown.InsideLupoHouse (Door)'),
    ('GladesTown.InsideLupoHouse (Door)', 'GladesTown.LupoHouse (Door)'),
    ('GladesTown.HoleHutEntrance (Door)', 'GladesTown.InsideHoleHut (Door)'),
    ('GladesTown.InsideHoleHut (Door)', 'GladesTown.HoleHutEntrance (Door)'),
    ('OuterWellspring.EntranceDoor (Door)', 'InnerWellspring.EntranceDoor (Door)'),
    ('OuterWellspring.WestDoor (Door)', 'InnerWellspring.WestDoor (Door)'),
    ('OuterWellspring.EastDoor (Door)', 'InnerWellspring.EastDoor (Door)'),
    ('OuterWellspring.TopDoor (Door)', 'InnerWellspring.Teleporter (Door)'),
    ('InnerWellspring.EntranceDoor (Door)', 'OuterWellspring.EntranceDoor (Door)'),
    ('InnerWellspring.WestDoor (Door)', 'OuterWellspring.WestDoor (Door)'),
    ('InnerWellspring.EastDoor (Door)', 'OuterWellspring.EastDoor (Door)'),
    ('InnerWellspring.Teleporter (Door)', 'OuterWellspring.TopDoor (Door)'),
    ('WoodsEntry.FamilyHut (Door)', 'WoodsEntry.FamilyHutInside (Door)'),
    ('WoodsEntry.FamilyHutInside (Door)', 'WoodsEntry.FamilyHut (Door)'),
    ('UpperReach.TreeRoom (Door)', 'UpperReach.SeedHut (Door)'),
    ('UpperReach.SeedHut (Door)', 'UpperReach.TreeRoom (Door)'),
    ('UpperWastes.OutsideRuins (Door)', 'WindtornRuins.UpperRuinsDoor (Door)'),
    ('WindtornRuins.UpperRuinsDoor (Door)', 'UpperWastes.OutsideRuins (Door)'),
    ('WeepingRidge.WillowEntranceLedge (Door)', 'WillowsEnd.Entry (Door)'),
    ('WillowsEnd.Entry (Door)', 'WeepingRidge.WillowEntranceLedge (Door)'),
    ('WillowsEnd.Upper (Door)', 'WillowsEnd.ShriekArena (Door)'),
    ('WillowsEnd.ShriekArena (Door)', 'WillowsEnd.Upper (Door)')
    ]


doors_map: dict[str, int] = {  # Mapping to door ID
    "GladesTown.TwillenHome (Door)": 9,
    "GladesTown.KeyMokiHutInside (Door)": 10,
    "GladesTown.MotayHutDoor (Door)": 5,
    "GladesTown.MotayHutInside (Door)": 6,
    "GladesTown.UpperWest (Door)": 3,
    "GladesTown.InsideThirdHut (Door)": 4,
    "GladesTown.AcornMoki (Door)": 13,
    "GladesTown.AcornCave (Door)": 14,
    "GladesTown.AboveOpher (Door)": 11,
    "GladesTown.StorageHut (Door)": 12,
    "GladesTown.LupoHouse (Door)": 1,
    "GladesTown.InsideLupoHouse (Door)": 2,
    "GladesTown.HoleHutEntrance (Door)": 7,
    "GladesTown.InsideHoleHut (Door)": 8,
    "OuterWellspring.EntranceDoor (Door)": 15,
    "OuterWellspring.WestDoor (Door)": 17,
    "OuterWellspring.EastDoor (Door)": 19,
    "OuterWellspring.TopDoor (Door)": 21,
    "InnerWellspring.EntranceDoor (Door)": 16,
    "InnerWellspring.WestDoor (Door)": 18,
    "InnerWellspring.EastDoor (Door)": 20,
    "InnerWellspring.Teleporter (Door)": 22,
    "WoodsEntry.FamilyHut (Door)": 25,
    "WoodsEntry.FamilyHutInside (Door)": 26,
    "UpperReach.TreeRoom (Door)": 23,
    "UpperReach.SeedHut (Door)": 24,
    "UpperWastes.OutsideRuins (Door)": 27,
    "WindtornRuins.UpperRuinsDoor (Door)": 28,
    "WeepingRidge.WillowEntranceLedge (Door)": 29,
    "WillowsEnd.Entry (Door)": 30,
    "WillowsEnd.Upper (Door)": 31,
    "WillowsEnd.ShriekArena (Door)": 32
    }
