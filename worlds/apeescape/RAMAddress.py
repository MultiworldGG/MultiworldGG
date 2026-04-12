from .Strings import AEDoor


class RAM:
# ===================== Locations/Checks =====================
    monkeyListGlobal = {
        # FF
        1: 0x0DF828,
        2: 0x0DF829,
        3: 0x0DF82A,
        4: 0x0DF82B,
        # PO
        5: 0x0DF830,
        6: 0x0DF831,
        8: 0x0DF832,
        7: 0x0DF833,
        10: 0x0DF834,
        9: 0x0DF835,
        # ML
        11: 0x0DF838,
        12: 0x0DF839,
        13: 0x0DF83A,
        17: 0x0DF83B,
        15: 0x0DF840,
        14: 0x0DF841,
        16: 0x0DF848,
        # TJ
        18: 0x0DF850,
        19: 0x0DF851,
        20: 0x0DF852,
        29: 0x0DF858,
        31: 0x0DF859,
        30: 0x0DF85A,
        21: 0x0DF860,
        22: 0x0DF861,
        23: 0x0DF862,
        25: 0x0DF868,
        24: 0x0DF869,
        26: 0x0DF86A,
        28: 0x0DF870,
        27: 0x0DF871,
        # DR
        33: 0x0DF878,
        37: 0x0DF879,
        42: 0x0DF87A,
        34: 0x0DF87B,
        32: 0x0DF87C,
        35: 0x0DF880,
        36: 0x0DF881,
        41: 0x0DF888,
        43: 0x0DF889,
        38: 0x0DF88A,
        39: 0x0DF890,
        40: 0x0DF891,
        44: 0x0DF892,
        # CR
        51: 0x0DF898,
        49: 0x0DF899,
        45: 0x0DF8A0,
        47: 0x0DF8A8,
        46: 0x0DF8A9,
        50: 0x0DF8AA,
        48: 0x0DF8B0,
        52: 0x0DF8B1,
        # CB
        53: 0x0DF8C0,
        54: 0x0DF8C1,
        55: 0x0DF8C2,
        56: 0x0DF8C3,
        57: 0x0DF8C8,
        60: 0x0DF8C9,
        58: 0x0DF8CA,
        59: 0x0DF8CB,
        # CC
        61: 0x0DF8D0,
        62: 0x0DF8D1,
        63: 0x0DF8D2,
        64: 0x0DF8D3,
        65: 0x0DF8D8,
        67: 0x0DF8D9,
        66: 0x0DF8DA,
        68: 0x0DF8DB,
        # DI
        70: 0x0DF8E0,
        69: 0x0DF8E1,
        77: 0x0DF8E8,
        71: 0x0DF8E9,
        78: 0x0DF8EA,
        72: 0x0DF8F0,
        73: 0x0DF8F1,
        74: 0x0DF8F2,
        75: 0x0DF8F3,
        76: 0x0DF8F4,
        79: 0x0DF8F8,
        # SM
        80: 0x0DF908,
        81: 0x0DF909,
        84: 0x0DF90A,
        82: 0x0DF90B,
        83: 0x0DF90C,
        85: 0x0DF90D,
        # FR
        86: 0x0DF910,
        87: 0x0DF911,
        91: 0x0DF918,
        93: 0x0DF919,
        92: 0x0DF91A,
        94: 0x0DF91B,
        88: 0x0DF920,
        89: 0x0DF921,
        90: 0x0DF922,
        # HS
        95: 0x0DF928,
        96: 0x0DF929,
        99: 0x0DF92A,
        100: 0x0DF92B,
        101: 0x0DF930,
        102: 0x0DF931,
        103: 0x0DF932,
        97: 0x0DF938,
        98: 0x0DF939,
        # ST
        104: 0x0DF948,
        105: 0x0DF949,
        106: 0x0DF94A,
        107: 0x0DF94B,
        109: 0x0DF950,
        110: 0x0DF951,
        108: 0x0DF952,
        114: 0x0DF953,
        115: 0x0DF954,
        113: 0x0DF958,
        111: 0x0DF959,
        112: 0x0DF95A,
        # WSW
        116: 0x0DF960,
        117: 0x0DF961,
        118: 0x0DF968,
        119: 0x0DF969,
        120: 0x0DF96A,
        123: 0x0DF970,
        121: 0x0DF978,
        122: 0x0DF979,
        124: 0x0DF980,
        125: 0x0DF981,
        # CrC
        127: 0x0DF988,
        136: 0x0DF989,
        126: 0x0DF98A,
        128: 0x0DF98B,
        137: 0x0DF98C,
        129: 0x0DF990,
        132: 0x0DF993,
        130: 0x0DF991,
        131: 0x0DF992,
        133: 0x0DF998,
        134: 0x0DF999,
        135: 0x0DF99A,
        138: 0x0DF9A8,
        139: 0x0DF9A9,
        140: 0x0DF9B0,
        141: 0x0DF9B1,
        142: 0x0DF9B2,
        143: 0x0DF9B8,
        144: 0x0DF9B9,
        145: 0x0DF9BA,
        # CP
        146: 0x0DF9C8,
        147: 0x0DF9C9,
        148: 0x0DF9CA,
        149: 0x0DF9CB,
        150: 0x0DF9D0,
        151: 0x0DF9D1,
        152: 0x0DF9D2,
        153: 0x0DF9D8,
        154: 0x0DF9D9,
        155: 0x0DF9DA,
        156: 0x0DF9DB,
        157: 0x0DF9DC,
        158: 0x0DF9DD,
        # SF
        159: 0x0DF9E0,
        160: 0x0DF9E1,
        161: 0x0DF9E8,
        162: 0x0DF9F0,
        163: 0x0DF9F8,
        164: 0x0DF9F9,
        165: 0x0DF9FA,
        166: 0x0DFA08,
        167: 0x0DFA09,
        168: 0x0DFA10,
        # TVT
        169: 0x0DFA18,
        170: 0x0DFA20,
        171: 0x0DFA21,
        172: 0x0DFA28,
        173: 0x0DFA29,
        174: 0x0DFA30,
        175: 0x0DFA31,
        176: 0x0DFA32,
        177: 0x0DFA38,
        178: 0x0DFA39,
        179: 0x0DFA3A,
        180: 0x0DFA3B,
        # MM
        181: 0x0DFA60,
        182: 0x0DFA78,
        183: 0x0DFA80,
        184: 0x0DFA81,
        185: 0x0DFA82,
        186: 0x0DFA88,
        187: 0x0DFA89,
        188: 0x0DFA8A,
        189: 0x0DFA8B,
        190: 0x0DFA90,
        191: 0x0DFA98,
        192: 0x0DFA99,
        193: 0x0DFAA0,
        194: 0x0DFAA1,
        196: 0x0DFAA3,
        195: 0x0DFAA2,
        197: 0x0DFAA8,
        198: 0x0DFAA9,
        199: 0x0DFAB0,
        200: 0x0DFAB1,
        201: 0x0DFAC0,
        202: 0x0DFAC1,
        203: 0x0DFAC2,
        204: 0x0DFAC8,
    }

    monkeyListLocal = {
        1: {  # 1-1
            1: 0x0E557A,
            3: 0x0E5A1A,
            2: 0x0E57CA,
            4: 0x0E5C6A
        },
        2: {  # 1-2
            5: 0x0E557A,
            6: 0x0E57CA,
            7: 0x0E5C6A,
            10: 0x0E5EBA,
            9: 0x0E610A,
            8: 0x0E5A1A
        },
        3: {  # 1-3
            11: 0x0E557A,
            12: 0x0E57CA,
            17: 0x0E5C6A,
            13: 0x0E5A1A
        },
        4: {  # volcano
            14: 0x0E57CA,
            15: 0x0E557A
        },
        5: {  # triceratops
            16: 0x0E557A
        },
        6: {  # 2-1
            18: 0x0E557A,
            19: 0x0E57CA,
            20: 0x0E5A1A
        },
        7: {  # mushroom area
            29: 0x0E557A,
            30: 0x0E5A1A,
            31: 0x0E57CA
        },
        8: {  # fish room
            23: 0x0E5A1A,
            21: 0x0E557A,
            22: 0x0E57CA
        },
        9: {  # tent/vine room
            24: 0x0E57CA,
            25: 0x0E557A,
            26: 0x0E5A1A
        },
        10: {  # boulder room
            27: 0x0E57CA,
            28: 0x0E557A
        },
        11: {  # 2-2
            32: 0x0E5EBA,
            33: 0x0E557A,
            34: 0x0E5C6A,
            37: 0x0E57CA,
            42: 0x0E5A1A
        },
        12: {  # fan basement
            35: 0x0E557A,
            36: 0x0E57CA
        },
        13: {  # obelisk inside
            38: 0x0E5A1A,
            41: 0x0E557A,
            43: 0x0E57CA
        },
        14: {  # water basement
            39: 0x0E557A,
            40: 0x0E57CA,
            44: 0x0E5A1A
        },
        15: {  # 2-3
            49: 0x0E57CA,
            51: 0x0E557A
        },
        16: {  # side room
            45: 0x0E557A
        },
        17: {  # main ruins
            47: 0x0E557A,
            50: 0x0E5A1A,
            46: 0x0E57CA
        },
        18: {  # pillar room
            48: 0x0E557A,
            52: 0x0E57CA
        },
        19: {  # 3-1

        },
        20: {  # 4-1
            53: 0x0E557A,
            54: 0x0E57CA,
            55: 0x0E5A1A,
            56: 0x0E5C6A
        },
        21: {  # second room
            57: 0x0E557A,
            58: 0x0E5A1A,
            59: 0x0E5C6A,
            60: 0x0E57CA
        },
        22: {  # 4-2
            61: 0x0E557A,
            62: 0x0E57CA,
            63: 0x0E5A1A,
            64: 0x0E5C6A
        },
        23: {  # second room
            65: 0x0E557A,
            67: 0x0E57CA,
            68: 0x0E5C6A,
            66: 0x0E5A1A
        },
        24: {  # 4-3
            69: 0x0E57CA,
            70: 0x0E557A
        },
        25: {  # stomach
            71: 0x0E57CA,
            77: 0x0E557A,
            78: 0x0E5A1A
        },
        26: {  # gallery/boulder
            72: 0x0E557A,
            73: 0x0E57CA,
            74: 0x0E5A1A,
            75: 0x0E5C6A,
            76: 0x0E5EBA
        },
        27: {  # tentacle room
            79: 0x0E557A
        },
        28: {  # slide room

        },
        29: {  # 5-1
            80: 0x0E557A,
            81: 0x0E57CA,
            84: 0x0E5A1A,
            83: 0x0E5C6A,
            85: 0x0E610A,
            82: 0x0E5EBA
        },
        30: {  # 5-2
            86: 0x0E557A,
            87: 0x0E57CA
        },
        31: {  # water room
            91: 0x0E557A,
            92: 0x0E5A1A,
            93: 0x0E57CA,
            94: 0x0E5C6A
        },
        32: {  # caverns
            88: 0x0E557A,
            90: 0x0E5A1A,
            89: 0x0E57CA
        },
        33: {  # 5-3
            95: 0x0E557A,
            96: 0x0E57CA,
            99: 0x0E5A1A,
            100: 0x0E5C6A
        },
        34: {  # hot spring
            101: 0x0E557A,
            102: 0x0E57CA,
            103: 0x0E5A1A
        },
        35: {  # polar bear cave
            98: 0x0E57CA,
            97: 0x0E557A
        },
        36: {  # 6-1

        },
        37: {  # 7-1
            104: 0x0E557A,
            105: 0x0E57CA,
            106: 0x0E5A1A,
            107: 0x0E5C6A
        },
        38: {  # temple
            108: 0x0E5A1A,
            110: 0x0E57CA,
            109: 0x0E557A,
            114: 0x0E5C6A,
            115: 0x0E5EBA
        },
        39: {  # well
            111: 0x0E57CA,
            112: 0x0E5A1A,
            113: 0x0E557A
        },
        40: {  # 7-2
            116: 0x0E557A,
            117: 0x0E57CA
        },
        41: {  # gong room
            118: 0x0E557A,
            119: 0x0E57CA,
            120: 0x0E5A1A
        },
        42: {  # middle room
            123: 0x0E557A
        },
        43: {  # obstacle course
            122: 0x0E57CA,
            121: 0x0E557A,
        },
        44: {  # barrel room
            124: 0x0E557A,
            125: 0x0E57CA
        },
        45: {  # 7-3
            126: 0x0E5A1A,
            127: 0x0E557A,
            128: 0x0E5C6A,
            137: 0x0E5EBA,
            136: 0x0E57CA
        },
        46: {  # castle main
            129: 0x0E557A,
            131: 0x0E5A1A,
            130: 0x0E57CA,
            132: 0x0E5C6A
        },
        47: {  # flooded basement
            133: 0x0E557A,
            134: 0x0E57CA,
            135: 0x0E5A1A
        },
        49: {  # button room
            139: 0x0E57CA,
            138: 0x0E557A
        },
        50: {  # elevator room
            140: 0x0E557A,
            141: 0x0E57CA,
            142: 0x0E5A1A
        },
        51: {  # bell tower
            145: 0x0E5A1A,
            144: 0x0E57CA,
            143: 0x0E557A
        },
        52: {

        },
        53: {  # 8-1
            146: 0x0E557A,
            149: 0x0E5C6A,
            147: 0x0E57CA,
            148: 0x0E5A1A
        },
        54: {  # sewers front
            151: 0x0E57CA,
            152: 0x0E5A1A,
            150: 0x0E557A
        },
        55: {  # barrel room
            155: 0x0E5A1A,
            153: 0x0E557A,
            156: 0x0E5C6A,
            157: 0x0E5EBA,
            154: 0x0E57CA,
            158: 0x0E610A
        },
        56: {  # 8-2
            159: 0x0E557A,
            160: 0x0E57CA
        },
        57: {  # main factory
            161: 0x0E557A
        },
        58: {  # rc car room
            162: 0x0E557A
        },
        59: {  # lava room
            163: 0x0E557A,
            164: 0x0E57CA,
            165: 0x0E5A1A
        },
        60: {

        },
        61: {  # conveyor room
            166: 0x0E557A,
            167: 0x0E57CA
        },
        62: {  # mech room
            168: 0x0E557A
        },
        63: {  # 8-3
            169: 0x0E557A
        },
        64: {  # water basement
            171: 0x0E57CA,
            170: 0x0E557A
        },
        65: {  # lobby
            172: 0x0E557A,
            173: 0x0E57CA
        },
        66: {  # tank room
            174: 0x0E557A,
            175: 0x0E57CA,
            176: 0x0E5A1A
        },
        67: {  # fan room
            177: 0x0E557A,
            179: 0x0E5A1A,
            180: 0x0E5C6A,
            178: 0x0E57CA
        },
        68: {

        },
        69: {  # MM Lobby

        },
        71: {

        },
        72: {  # coaster entry
            181: 0x0E557A
        },
        73: {  # coaster 1

        },
        74: {  # coaster 2

        },
        75: {  # haunted house
            182: 0x0E557A
        },
        76: {  # coffin room
            183: 0x0E557A,
            184: 0x0E57CA,
            185: 0x0E5A1A
        },
        77: {  # western land
            187: 0x0E57CA,
            186: 0x0E557A,
            188: 0x0E5A1A,
            189: 0x0E5C6A
        },
        78: {  # crater
            190: 0x0E557A
        },
        79: {  # outside castle
            192: 0x0E557A,
            191: 0X0E57CA
        },
        80: {  # castle main
            194: 0x0E57CA,
            195: 0x0E5A1A,
            196: 0x0E5C6A,
            193: 0x0E557A
        },
        81: {  # inside climb
            197: 0x0E557A,
            198: 0x0E57CA
        },
        82: {  # outside climb
            199: 0x0E557A,
            200: 0x0E57CA
        },
        84: {  # Monkey head
            201: 0x0E557A,
            202: 0x0E57CA,
            203: 0x0E5A1A
        },
        85: {  # side entry
            204: 0x0E557A
        }

    }

# List of temporary table that monkeys caught status get saved while traversing level.
# Get's written when going into a transition
# When exiting the level,it save them into global values
    monkeyListTempLocal = {
        1: {  # 1-1
            1: 0x0DFE00,
            3: 0x0DFE01,
            2: 0x0DFE02,
            4: 0x0DFE03
        },
        2: {  # 1-2
            5: 0x0DFE00,
            6: 0x0DFE01,
            7: 0x0DFE03,
            10: 0x0DFE04,
            9: 0x0DFE05,
            8: 0x0DFE02
        },
        3: {  # 1-3
            11: 0x0DFE00,
            12: 0x0DFE01,
            17: 0x0DFE03,
            13: 0x0DFE02
        },
        4: {  # volcano
            14: 0x0DFE19,
            15: 0x0DFE18
        },
        5: {  # triceratops
            16: 0x0DFE30
        },
        6: {  # 2-1
            18: 0x0DFE00,
            19: 0x0DFE01,
            20: 0x0DFE02
        },
        7: {  # mushroom area
            29: 0x0DFE18,
            30: 0x0DFE1A,
            31: 0x0DFE19
        },
        8: {  # fish room
            23: 0x0DFE32,
            21: 0x0DFE30,
            22: 0x0DFE31
        },
        9: {  # tent/vine room
            24: 0x0DFE49,
            25: 0x0DFE48,
            26: 0x0DFE4A
        },
        10: {  # boulder room
            27: 0x0DFE61,
            28: 0x0DFE60
        },
        11: {  # 2-2
            32: 0x0DFE04,
            33: 0x0DFE00,
            34: 0x0DFE03,
            37: 0x0DFE01,
            42: 0x0DFE02
        },
        12: {  # fan basement
            35: 0x0DFE18,
            36: 0x0DFE19
        },
        13: {  # obelisk inside
            38: 0x0DFE32,
            41: 0x0DFE30,
            43: 0x0DFE31
        },
        14: {  # water basement
            39: 0x0DFE48,
            40: 0x0DFE49,
            44: 0x0DFE4A
        },
        15: {  # 2-3
            49: 0x0DFE01,
            51: 0x0DFE00
        },
        16: {  # side room
            45: 0x0DFE18
        },
        17: {  # main ruins
            47: 0x0DFE30,
            50: 0x0DFE32,
            46: 0x0DFE31
        },
        18: {  # pillar room
            48: 0x0DFE48,
            52: 0x0DFE49
        },
        19: {  # 3-1

        },
        20: {  # 4-1
            53: 0x0DFE00,
            54: 0x0DFE01,
            55: 0x0DFE02,
            56: 0x0DFE03
        },
        21: {  # second room
            57: 0x0DFE18,
            58: 0x0DFE1A,
            59: 0x0DFE1B,
            60: 0x0DFE19
        },
        22: {  # 4-2
            61: 0x0DFE00,
            62: 0x0DFE01,
            63: 0x0DFE02,
            64: 0x0DFE03
        },
        23: {  # second room
            65: 0x0DFE18,
            67: 0x0DFE19,
            68: 0x0DFE1B,
            66: 0x0DFE1A
        },
        24: {  # 4-3
            69: 0x0DFE01,
            70: 0x0DFE00
        },
        25: {  # stomach
            71: 0x0DFE19,
            77: 0x0DFE18,
            78: 0x0DFE1A
        },
        26: {  # gallery/boulder
            72: 0x0DFE30,
            73: 0x0DFE31,
            74: 0x0DFE32,
            75: 0x0DFE33,
            76: 0x0DFE34
        },
        27: {  # tentacle room
            79: 0x0DFE48
        },
        28: {  # slide room

        },
        29: {  # 5-1
            80: 0x0DFE00,
            81: 0x0DFE01,
            84: 0x0DFE02,
            83: 0x0DFE04,
            85: 0x0DFE05,
            82: 0x0DFE03
        },
        30: {  # 5-2
            86: 0x0DFE00,
            87: 0x0DFE01
        },
        31: {  # water room
            91: 0x0DFE18,
            92: 0x0DFE1A,
            93: 0x0DFE19,
            94: 0x0DFE1B
        },
        32: {  # caverns
            88: 0x0DFE30,
            90: 0x0DFE32,
            89: 0x0DFE31
        },
        33: {  # 5-3
            95: 0x0DFE00,
            96: 0x0DFE01,
            99: 0x0DFE02,
            100: 0x0DFE03
        },
        34: {  # hot spring
            101: 0x0DFE18,
            102: 0x0DFE19,
            103: 0x0DFE1A
        },
        35: {  # polar bear cave
            98: 0x0DFE31,
            97: 0x0DFE30
        },
        36: {  # 6-1

        },
        37: {  # 7-1
            104: 0x0DFE00,
            105: 0x0DFE01,
            106: 0x0DFE02,
            107: 0x0DFE03
        },
        38: {  # temple
            108: 0x0DFE1A,
            110: 0x0DFE19,
            109: 0x0DFE18,
            114: 0x0DFE1B,
            115: 0x0DFE1C
        },
        39: {  # well
            111: 0x0DFE31,
            112: 0x0DFE32,
            113: 0x0DFE30
        },
        40: {  # 7-2
            116: 0x0DFE00,
            117: 0x0DFE01
        },
        41: {  # gong room
            118: 0x0DFE18,
            119: 0x0DFE19,
            120: 0x0DFE1A
        },
        42: {  # middle room
            123: 0x0DFE30
        },
        43: {  # obstacle course
            122: 0x0DFE49,
            121: 0x0DFE48,
        },
        44: {  # barrel room
            124: 0x0DFE60,
            125: 0x0DFE61
        },
        45: {  # 7-3
            126: 0x0DFE02,
            127: 0x0DFE00,
            128: 0x0DFE03,
            137: 0x0DFE04,
            136: 0x0DFE01
        },
        46: {  # castle main
            129: 0x0DFE18,
            131: 0x0DFE1A,
            130: 0x0DFE19,
            132: 0x0DFE1B
        },
        47: {  # flooded basement
            133: 0x0DFE30,
            134: 0x0DFE31,
            135: 0x0DFE32
        },
        49: {  # button room
            139: 0x0DFE61,
            138: 0x0DFE60
        },
        50: {  # elevator room
            140: 0x0DFE78,
            141: 0x0DFE79,
            142: 0x0DFE7A
        },
        51: {  # bell tower
            145: 0x0DFE92,
            144: 0x0DFE91,
            143: 0x0DFE90
        },
        52: {

        },
        53: {  # 8-1
            146: 0x0DFE00,
            149: 0x0DFE03,
            147: 0x0DFE01,
            148: 0x0DFE02
        },
        54: {  # sewers front
            151: 0x0DFE19,
            152: 0x0E5A1A,
            150: 0x0DFE18
        },
        55: {  # barrel room
            155: 0x0DFE32,
            153: 0x0DFE30,
            156: 0x0DFE33,
            157: 0x0DFE34,
            154: 0x0DFE31,
            158: 0x0DFE35
        },
        56: {  # 8-2
            159: 0x0DFE00,
            160: 0x0DFE01
        },
        57: {  # main factory
            161: 0x0DFE18
        },
        58: {  # rc car room
            162: 0x0DFE30
        },
        59: {  # lava room
            163: 0x0DFE48,
            164: 0x0DFE49,
            165: 0x0DFE4A
        },
        60: {

        },
        61: {  # conveyor room
            166: 0x0DFE78,
            167: 0x0DFE79
        },
        62: {  # mech room
            168: 0x0DFE90
        },
        63: {  # 8-3
            169: 0x0DFE00
        },
        64: {  # water basement
            171: 0x0DFE19,
            170: 0x0DFE18
        },
        65: {  # lobby
            172: 0x0DFE30,
            173: 0x0DFE31
        },
        66: {  # tank room
            174: 0x0DFE48,
            175: 0x0DFE49,
            176: 0x0DFE4A
        },
        67: {  # fan room
            177: 0x0DFE60,
            179: 0x0DFE62,
            180: 0x0DFE63,
            178: 0x0DFE61
        },
        68: {

        },
        69: {  # MM Lobby

        },
        71: {

        },
        72: {  # coaster entry
            181: 0x0DFE00
        },
        73: {  # coaster 1

        },
        74: {  # coaster 2

        },
        75: {  # haunted house
            182: 0x0DFE48
        },
        76: {  # coffin room
            183: 0x0DFE60,
            184: 0x0DFE61,
            185: 0x0DFE62
        },
        77: {  # western land
            187: 0x0DFE01,
            186: 0x0DFE00,
            188: 0x0DFE02,
            189: 0x0DFE03
        },
        78: {  # crater
            190: 0x0DFE00
        },
        79: {  # outside castle
            192: 0x0DFE19,
            191: 0x0DFE18
        },
        80: {  # castle main
            194: 0x0DFE31,
            195: 0x0DFE32,
            196: 0x0DFE33,
            193: 0x0DFE30
        },
        81: {  # inside climb
            197: 0x0DFE48,
            198: 0x0DFE49
        },
        82: {  # outside climb
            199: 0x0DFE60,
            200: 0x0DFE61
        },
        84: {  # Monkey head
            201: 0x0DFE90,
            202: 0x0DFE91,
            203: 0x0DFE92
        },
        85: {  # side entry
            204: 0x0DFEA8
        }

    }

    localMonkeyHitbox = {
        #Array order -> LocalMonkeyAddress : HitboxAddress
        0x0E557A : 0x0E5525,
        0x0E57CA : 0x0E5775,
        0x0E5A1A : 0x0E59C5,
        0x0E5C6A : 0x0E5C15,
        0x0E5EBA : 0x0E5E65,
        0x0E610A : 0x0E60B5

    }

    localmonkeyCatchHitbox = {
        # FF
        1: 0x0DF828,
        2: 0x0DF829,
        3: 0x0DF82A,
        4: 0x0DF82B,
        # PO
        5: 0x0DF830,
        6: 0x0DF831,
        8: 0x0DF832,
        7: 0x0DF833,
        10: 0x0DF834,
        9: 0x0DF835,
        # ML
        11: 0x0DF838,
        12: 0x0DF839,
        13: 0x0DF83A,
        17: 0x0DF83B,
        15: 0x0DF840,
        14: 0x0DF841,
        16: 0x0DF848,
        # TJ
        18: 0x0DF850,
        19: 0x0DF851,
        20: 0x0DF852,
        29: 0x0DF858,
        31: 0x0DF859,
        30: 0x0DF85A,
        21: 0x0DF860,
        22: 0x0DF861,
        23: 0x0DF862,
        25: 0x0DF868,
        24: 0x0DF869,
        26: 0x0DF86A,
        28: 0x0DF870,
        27: 0x0DF871,
        # DR
        33: 0x0DF878,
        37: 0x0DF879,
        42: 0x0DF87A,
        34: 0x0DF87B,
        32: 0x0DF87C,
        35: 0x0DF880,
        36: 0x0DF881,
        41: 0x0DF888,
        43: 0x0DF889,
        38: 0x0DF88A,
        39: 0x0DF890,
        40: 0x0DF891,
        44: 0x0DF892,
        # CR
        51: 0x0DF898,
        49: 0x0DF899,
        45: 0x0DF8A0,
        47: 0x0DF8A8,
        46: 0x0DF8A9,
        50: 0x0DF8AA,
        48: 0x0DF8B0,
        52: 0x0DF8B1,
        # CB
        53: 0x0DF8C0,
        54: 0x0DF8C1,
        55: 0x0DF8C2,
        56: 0x0DF8C3,
        57: 0x0DF8C8,
        60: 0x0DF8C9,
        58: 0x0DF8CA,
        59: 0x0DF8CB,
        # CC
        61: 0x0DF8D0,
        62: 0x0DF8D1,
        63: 0x0DF8D2,
        64: 0x0DF8D3,
        65: 0x0DF8D8,
        67: 0x0DF8D9,
        66: 0x0DF8DA,
        68: 0x0DF8DB,
        # DI
        70: 0x0DF8E0,
        69: 0x0DF8E1,
        77: 0x0DF8E8,
        71: 0x0DF8E9,
        78: 0x0DF8EA,
        72: 0x0DF8F0,
        73: 0x0DF8F1,
        74: 0x0DF8F2,
        75: 0x0DF8F3,
        76: 0x0DF8F4,
        79: 0x0DF8F8,
        # SM
        80: 0x0DF908,
        81: 0x0DF909,
        84: 0x0DF90A,
        82: 0x0DF90B,
        83: 0x0DF90C,
        85: 0x0DF90D,
        # FR
        86: 0x0DF910,
        87: 0x0DF911,
        91: 0x0DF918,
        93: 0x0DF919,
        92: 0x0DF91A,
        94: 0x0DF91B,
        88: 0x0DF920,
        89: 0x0DF921,
        90: 0x0DF922,
        # HS
        95: 0x0DF928,
        96: 0x0DF929,
        99: 0x0DF92A,
        100: 0x0DF92B,
        101: 0x0DF930,
        102: 0x0DF931,
        103: 0x0DF932,
        97: 0x0DF938,
        98: 0x0DF939,
        # ST
        104: 0x0DF948,
        105: 0x0DF949,
        106: 0x0DF94A,
        107: 0x0DF94B,
        109: 0x0DF950,
        110: 0x0DF951,
        108: 0x0DF952,
        114: 0x0DF953,
        115: 0x0DF954,
        113: 0x0DF958,
        111: 0x0DF959,
        112: 0x0DF95A,
        # WSW
        116: 0x0DF960,
        117: 0x0DF961,
        118: 0x0DF968,
        119: 0x0DF969,
        120: 0x0DF96A,
        123: 0x0DF970,
        121: 0x0DF978,
        122: 0x0DF979,
        124: 0x0DF980,
        125: 0x0DF981,
        # CrC
        127: 0x0DF988,
        136: 0x0DF989,
        126: 0x0DF98A,
        128: 0x0DF98B,
        137: 0x0DF98C,
        129: 0x0DF990,
        132: 0x0DF993,
        130: 0x0DF991,
        131: 0x0DF992,
        133: 0x0DF998,
        134: 0x0DF999,
        135: 0x0DF99A,
        138: 0x0DF9A8,
        139: 0x0DF9A9,
        140: 0x0DF9B0,
        141: 0x0DF9B1,
        142: 0x0DF9B2,
        143: 0x0DF9B8,
        144: 0x0DF9B9,
        145: 0x0DF9BA,
        # CP
        146: 0x0DF9C8,
        147: 0x0DF9C9,
        148: 0x0DF9CA,
        149: 0x0DF9CB,
        150: 0x0DF9D0,
        151: 0x0DF9D1,
        152: 0x0DF9D2,
        153: 0x0DF9D8,
        154: 0x0DF9D9,
        155: 0x0DF9DA,
        156: 0x0DF9DB,
        157: 0x0DF9DC,
        158: 0x0DF9DD,
        # SF
        159: 0x0DF9E0,
        160: 0x0DF9E1,
        161: 0x0DF9E8,
        162: 0x0DF9F0,
        163: 0x0DF9F8,
        164: 0x0DF9F9,
        165: 0x0DF9FA,
        166: 0x0DFA08,
        167: 0x0DFA09,
        168: 0x0DFA10,
        # TVT
        169: 0x0DFA18,
        170: 0x0DFA20,
        171: 0x0DFA21,
        172: 0x0DFA28,
        173: 0x0DFA29,
        174: 0x0DFA30,
        175: 0x0DFA31,
        176: 0x0DFA32,
        177: 0x0DFA38,
        178: 0x0DFA39,
        179: 0x0DFA3A,
        180: 0x0DFA3B,
        # MM
        181: 0x0DFA60,
        182: 0x0DFA78,
        183: 0x0DFA80,
        184: 0x0DFA81,
        185: 0x0DFA82,
        186: 0x0DFA88,
        187: 0x0DFA89,
        188: 0x0DFA8A,
        189: 0x0DFA8B,
        190: 0x0DFA90,
        191: 0x0DFA98,
        192: 0x0DFA99,
        193: 0x0DFAA0,
        194: 0x0DFAA1,
        196: 0x0DFAA3,
        195: 0x0DFAA2,
        197: 0x0DFAA8,
        198: 0x0DFAA9,
        199: 0x0DFAB0,
        200: 0x0DFAB1,
        201: 0x0DFAC0,
        202: 0x0DFAC1,
        203: 0x0DFAC2,
        204: 0x0DFAC8,
    }
    coinsListLocal = {
        #Array Order:
        # CoinNumber : [CoinVisualSprite,CoinHitBoxPosition]
        # CoinVisualSprite : 4 = Coin Sprite(Not collected),0 = Collected
        1 : [0x0BF03A,0x0BF03E], # This is the ONLY coin that has an audio bug for w/e reason
        2 : [0x0BF1D2,0x0BF1D6],
        3 : [0x0BF15A,0x0BF15E],
        6 : [0x0BF0CA,0x0BF0CE],
        7 : [0x0BF1BA,0x0BF1BE],
        8 : [0x0BF1A2,0x0BF1A6],
        9 : [0x0BF1EA,0x0BF1EE],
        11 : [0x0BF172,0x0BF176],
        12 : [0x0BF09A,0X0BF09E],
        13 : [0x0BF142,0x0BF146],
        14 : [0x0BF1A2,0x0BF1A6],
        17 : [0x0BF142,0x0BF146],
        21 : [0x0BF15A,0x0BF15E],
        23 : [0x0BF1A2,0x0BF1A6],
        24 : [0x0BF052,0x0BF056],
        25 : [0x0BF142,0x0BF146],
        28 : [0x0BF0B2,0x0BF0B6],
        29 : [0x0BF142,0x0BF146],
        30 : [0x0BF142,0x0BF146],
        31 : [0x0BF172,0x0BF176],
        32 : [0x0BF18A,0x0BF18E],
        34 : [0x0BF112,0x0BF116],
        35 : [0x0BF232,0x0BF236],
        37 : [0x0BF0B2,0x0BF0B6],
        38 : [0x0BF0E2,0x0BF0E6],
        39 : [0x0BF1EA,0x0BF1EE],
        40 : [0x0BF15A,0x0BF15E],
        41 : [0x0BF00A,0x0BF00E],
        44 : [0x0BF1A2,0x0BF1A6],
        45 : [0x0BF172,0x0BF176],
        46 : [0x0BF1BA,0x0BF1BE],
        49 : [0x0BF142,0x0BF146],
        50 : [0x0BF1EA,0x0BF1EE],
        53 : [0x0BF18A,0x0BF18E],
        54 : [0x0BF1A2,0x0BF1A6],
        55 : [0x0BF24A,0x0BF24E],
        58 : [0x0BF082,0x0BF086],
        59 : [0x0BF18A,0x0BF18E],
        64 : [0x0BF1EA,0x0BF1EE],
        66 : [0x0BEFAA,0x0BEFAE],
        73 : [0x0BF18A,0x0BF18E],
        74 : [0x0BF09A,0x0BF09E],
        75 : [0x0BF0E2,0x0BF0E6],
        77 : [0x0BF12A,0x0BF12E],
        78 : [0x0BF18A,0x0BF18E],
        79 : [0x0BF21A,0x0BF21E],
        80 : [0X0BF142,0X0BF146],
        82 : [0X0BF1BA,0X0BF1BE],
        84 : [0x0BF21A,0x0BF21E],
        85 : [0x0BF0FA,0x0BF0FE],
    }


    CoinHitBoxPositionOff = 0xFFB0
    localMonkeyHitbox1 = 0x0BBDF4
    localMonkeyCatchHitBox1 = 0x0BBDF0 # ? Seems to be indicative of Monkeys Hitboxes FOR THE NET

    caughtStatus = {
        "Unloaded": 0x00,
        "OutOfRender": 0x01,
        "Uncaught": 0x04,
        "Caught": 0x03,
        "PrevCaught": 0x02
    }


    # Indexes all monkeys per levelID
    monkeysperlevel = {
        1: {
            1, 3, 2, 4
        },
        2: {
            5, 6, 7, 10, 9, 8
        },
        3: {
            11, 12, 17, 13, 14, 15, 16
        },
        4: {
            18, 19, 20, 29, 30, 31, 23, 21, 22, 24, 25, 26, 27, 28
        },
        5: {
            32, 33, 34, 37, 42, 35, 36, 38, 41, 43, 39, 40, 44
        },
        6: {
            49, 51, 45, 47, 50, 46,48, 52
        },
        7: {

        },
        8: {
            53, 54, 55, 56, 57, 58, 59, 60
        },
        9: {
            61, 62, 63, 64, 65, 67, 68, 66
        },
        10: {
            69, 70, 71, 77, 78, 72, 73, 74, 75, 76, 79
        },
        11: {
            80, 81, 84, 83, 85, 82
        },
        12: {
            86, 87, 91, 92, 93, 94, 88, 90, 89
        },
        13: {
            95, 96, 99, 100, 101, 102, 103, 98, 97
        },
        14: {

        },
        15: {
            104, 105, 106, 107, 108, 110, 109, 114, 115, 111, 112, 113
        },
        16: {
            116, 117, 118, 119, 120, 123, 122, 121, 124, 125
        },
        17: {
            126, 127, 128, 137, 136, 129, 131, 130, 132, 133, 134, 135, 139, 138, 140, 141, 142, 145, 144, 143
        },
        20: {
            146, 149, 147, 148, 151, 152, 150, 155, 153, 156, 157, 154, 158
        },
        21: {
            159, 160, 161, 162, 163, 164, 165, 166, 167, 168
        },
        22: {
            169, 171, 170, 172, 173, 174, 175, 176, 177, 179, 180, 178
        },
        24: {
            181, 182, 183, 184, 185, 187, 186, 188, 189, 190, 192, 191,
            194, 195, 196, 193, 197, 198, 199, 200, 201, 202, 203, 204
        }
    }

    timeStationMailboxStart = 0x0C1798
    gotMailAddress = 0x0BBD99
    # Seems to be shared with other variables,
    # Detect when gotMailAddress = 2 then check what mailbox it is
    mailboxIDAddress = 0x0A6CD2

    # Associate by room just to be sure, since some of them have the same ID (Ex.: Thick Jungle have 2 IDs = 71)
    mailboxListLocal = {
        1: {  # 1-1: Entry
            401: 65,
            402: 66,
            403: 19
        },
        2: {  # 1-2: Entry
            404: 68,
            405: 69,
            406: 70,
            407: 67
        },
        3: {  # 1-3: Entry
            408: 103,
            409: 21
        },
        4: {  # 1-3: volcano
            410: 100
        },
        5: {  # 1-3: triceratops
            411: {101, 116},
            412: 41
        },
        6: {  # 2-1: Entry
            413: 72,
            414: 71
        },
        7: {  # 2-1: mushroom area
            415: {38, 99},
            416: 24
        },
        8: {  # 2-1: fish room
            417: 73,
            418: 71,
            419: 104
        },
        9: {  # 2-1: tent/vine room
            420: 48
        },
        10: {  # 2-1: boulder room
            421: 23
        },
        11: {  # 2-2: Entry
            422: 105,
            423: {49, 103},
            424: 22,
            425: 81,
        },
        12: {  # 2-2: fan basement
            426: 80,
            427: {70, 97}
        },
        13: {  # 2-2: obelisk inside
            428: {52, 97}
        },
        15: {  # 2-3: Entry
            429: 50,
            430: 112
        },
        17: {  # 2-3: main ruins
            431: 33,
            432: 37
        },
        18: {  # 2-3: pillar room
            433: 67
        },
        20: {  # 4-1: Entry
            434: 25,
            435: {22, 82}
        },
        21: {  # 4-1: second room
            436: 72
        },
        23: {  # 4-2: second room
            437: 53,
            438: 54
        },
        24: {  # 4-3: Entry
            439: 39,
            440: 55
        },
        26: {  # 4-3: gallery/boulder
            442: {32, 72}
        },
        28: {  # 4-3: slide room
            441: 40
        },
        29: {  # 5-1: Entry
            443: 86,
            444: 18,
            445: 87
        },
        32: {  # 5-2: caverns
            446: 35
        },
        33: {  # 5-3: Entry
            447: 20
        },
        34: {  # 5-3: hot spring
            448: 51
        },
        35: {  # 5-3: polar bear cave
            449: 85
        },
        38: {  # 7-1: temple
            450: 57,
            451: 65
        },
        39: {  # 7-1: well
            452: 68
        },
        41: {  # 7-2: gong room
            453: {25, 56}
        },
        42: {  # 7-2: middle room
            454: 34,
            455: 36
        },
        43: {  # 7-2: obstacle course
            456: 64
        },

        45: {  # 7-3: Entry
            457: 69
        },
        56: {  # 8-2: Entry
            458: 83
        },
        72: {  # MM - coaster entry
            459: 84
        },
        88: {  # Time station - Hub
            460: 113,
            461: 114
        },
        91: {  # Time station - Mini-game Corner
            462: 116
        },
        90: {  # Time station - Training Space
            463: 115
        }

    }

    # To check if red mailboxes are already checked in the current room
    redMailboxes = {
        1: {  # 1-1: Entry
            401: 0x16076E,
            402: 0x160786,
        },
        2: {  # 1-2: Entry
            404: 0x175BD6,
            405: 0x175BA6,
            406: 0x175BBE,
            407: 0x175B8E
        },
        3: {  # 1-3: Entry
            408: 0x181592
        },
        4: {  # 1-3: volcano
            410: 0x167D3A
        },
        5: {  # 1-3: triceratops
            411: 0x165C5A
        },
        6: {  # 2-1: Entry
            413: 0x17A65A,
            414: 0x17A672
        },
        8: {  # 2-1: fish room
            417: 0x18031E,
            419: 0x180336
        },
        11: {  # 2-2: Entry
            422: 0x184612,
            425: 0x1845FA
        },
        12: {  # 2-2: fan basement
            426: 0x16A386,
        },
        15: {  # 2-3: Entry
            430: 0x176092
        },
        20: {  # 4-1: Entry
            435: 0x1798EA
        },
        29: {  # 5-1: Entry
            443: 0x17566A,
            445: 0x175682
        },
        35: {  # 5-3: polar bear cave
            449: 0x176E22
        },
        56: {  # 8-2: Entry
            458: 0x178E02
        },
        72: {  # MM - coaster entry
            459: 0x17389A
        },
        88: {  # Time station - Hub
            460: 0x1608BE,
            461: 0x1608A6
        },
        91: {  # Time station - Mini-game Corner
            462: 0x15FE3A
        },
        90: {  # Time station - Training Space
            463: 0x16721A
        }
    }

    bossListLocal = {
        48: {  # CrC boss room
            500: 0x0E69E1
        },
        68: {  # TVT boss room
            501: 0x143E1F
        },
        70: {  # MM_Jake
            503: 0x1422E6
        },
        71: {  # Circus (Professor)
            502: 0x0E6BA9
        },
        # Victory conditions calculated separately, no values there
        83: {  # Specter 1 Phase 1

        },
        86: {  # Specter 1 Phase 2

        },
        87: {  # Specter 2

        }
    }

    jakeVictoryAddress = 0x0F447A
    unlockedLevelAddress = 0x0DFC70
    requiredApesAddress = 0x0F44D8
    currentApesAddress = 0x0F44B6
    hundoApesAddress = 0x0F44D6
    hundoCoinsAddress = 0x0F44DA
    localApeStartAddress = 0x0DFE00
    startingCoinAddress = 0x0DFB70
    endingCoinAddress = 0x0DFBD2  # Not used,could be used for a loop if current coin system is buggy

    totalCoinsAddress = 0x0F44BA

    SA_CompletedAddress = 0x0DFDD0  # Completed = 0x19, not completed = 00
    GA_CompletedAddress = 0x0DFDD1  # Completed = 0x19, not completed = 00

    # Custom write/read addresses
    # Current game values: 0DFBEC - On load, gets replaced by SAVED address

    tempLastReceivedArchipelagoID = 0x0DFBD8  # 4 bytes
    tempKeyCountFromServer = 0x0DFBDC

    # Unused 0DFBDD to 0DFBDF
    tempGadgetStateFromServer = 0x0DFBE0  # 2 bytes - 0DFBE1

    tempWaterNetAddress = 0x0DFBE2
    tempWaterCatchAddress = 0x0DFBE3

    tempCB_LampAddress = 0x0DFBE4
    tempDI_LampAddress = 0x0DFBE5
    tempCrC_LampAddress = 0x0DFBE6
    tempCP_LampAddress = 0x0DFBE7
    tempSF_LampAddress = 0x0DFBE8
    tempTVT_Lobby_LampAddress = 0x0DFBE9
    tempTVT_Tank_LampAddress = 0x0DFBEA
    tempMM_LampAddress = 0x0DFBEB

    tempTokenCountFromServer = 0x0DFBEC

    temp_startingCoinAddress = 0x0DFBF0  # Copy all 64 bytes of coin here while entering Level Select
    levelselect_coinlock_Address = 0x0DFC60 # To tell the client if we are changing the coin table
    blank_coinTable = 0x00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF
    blank_coinTable2 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    temp_SA_CompletedAddress = 0x0DFC56
    temp_GA_CompletedAddress = 0x0DFC57
    temp_MMLobbyDoorAddress = 0x0DFC58

    temp_MM_Jake_DefeatedAddress = 0x0DFC5A
    temp_MM_Professor_RescuedAddress = 0x0DFC5C
    temp_MM_Natalie_RescuedAddress = 0x0DFC5E

    # hex 510 <-> dec 1296 difference
    # SAVED values: 0E00FC - Data that gets included when saving

    lastReceivedArchipelagoID = 0x0E00E8  # 4 bytes - to 0E00EB
    keyCountFromServer = 0x0E00EC
    # Unused 0E00ED to 0E00EF
    gadgetStateFromServer = 0x0E00F0  # 2 bytes - 0E00F1

    WaterNetAddress = 0x0E00F2
    WaterCatchAddress = 0x0E00F3
    CB_LampAddress = 0x0E00F4
    DI_LampAddress = 0x0E00F5
    CrC_LampAddress = 0x0E00F6
    CP_LampAddress = 0x0E00F7
    SF_LampAddress = 0x0E00F8
    TVT_Lobby_LampAddress = 0x0E00F9
    TVT_Tank_LampAddress = 0x0E00FA
    MM_LampAddress = 0x0E00FB

    tokenCountFromServer = 0x0E00FC

# ===================== Items =====================
    items = {
        "Club": 0x1,
        "Net": 0x2,
        "Radar": 0x4,
        "Sling": 0x8,
        "Hoop": 0x10,
        "Punch": 0x20,
        "Flyer": 0x40,
        "Car": 0x80,
        "Key": 0x100,
        "Victory": 0x200,
        "WaterNet": 0x400,
        "ProgWaterNet": 0x401,
        "WaterCatch": 0x402,
        "CB_Lamp": 0x150,
        "DI_Lamp": 0x151,
        "CrC_Lamp": 0x152,
        "CP_Lamp": 0x153,
        "SF_Lamp": 0x154,
        "TVT_Lobby_Lamp": 0x155,
        "TVT_Tank_Lamp": 0x156,
        "MM_Lamp": 0x157,
        "MM_DoubleDoorKey": 0x403,
        "Token": 0x300,
        "Nothing": 0x0,
        "Shirt": 0x210,
        "Triangle": 0x211,
        "BigTriangle": 0x212,
        "Cookie": 0x213,
        "Flash": 0x214,
        "Rocket": 0x215,
        "BiggerTriangle": 0x216,
        "FiveCookies": 0x217,
        "ThreeFlash": 0x218,
        "ThreeRocket": 0x219,
        "BananaPeelTrap": 0x250,
        "GadgetShuffleTrap": 0x251,
        "MonkeyMashTrap": 0x252,
        "IcyHotPantsTrap": 0x253,
        "StunTrap": 0x254,
        "CameraRotateTrap": 0x255,
        "RainbowCookie": 0x270,
        "FAKE_OOL_ITEM": 0x999,

    }

    # Junk addresses
    energyChipsAddress = 0x0F44B8
    cookieAddress = 0x0EC2C8
    instakillAddress = 0x0EC2C9
    tankLife = 0x0BF826
    livesAddress = 0x0F448C
    flashAddress = 0x0F51C1
    rocketAddress = 0x0F51C2

# ===================== Levels, Level Unlocks and ER =====================
    levelStatus = {
        "Locked": 0x00,
        "Complete": 0x01,
        "Hundo": 0x02,
        "Open": 0x03
    }

    levels = {
        "Fossil": 0x01,
        "Primordial": 0x02,
        "Molten": 0x03,
        "Thick": 0x04,
        "Dark": 0x05,
        "Cryptic": 0x06,
        "Stadium": 0x07,
        "Crabby": 0x08,
        "Coral": 0x09,
        "Dexter": 0x0A,
        "Snowy": 0x0B,
        "Frosty": 0x0C,
        "Hot": 0x0D,
        "Gladiator": 0x0E,
        "Sushi": 0x0F,
        "Wabi": 0x10,
        "Crumbling": 0x11,
        "City": 0x14,
        "Factory": 0x15,
        "TV": 0x16,
        "Specter": 0x18,
        "S_Jake": 0x19,
        "S_Circus": 0x1A,
        "S_Coaster": 0x1B,
        "S_Western Land": 0x1C,
        "S_Castle": 0x1D,
        "Peak": 0x1E,
        "Time": 0x1F,
        "Training": 0x20
    }

    MM_SubLevels_Rooms_Spawns = {
        #Should spawn you in these rooms,depending on RSR
        #Take the possible room and warps you to the base Sub-Level Room
        # "Specter": 0x18,
        69 : 69,
        # "S_Jake": 0x19,
        70 : 70,
        # "S_Circus": 0x1A,
        71 : 71,
        # "S_Coaster": 0x1B,
        72: 72,
        73: 72,
        74: 72,
        75: 72,
        76 : 72,
        # "S_Western Land": 0x1C,
        77 : 77,
        # "S_Castle": 0x1D,
        78 : 78,
        79 : 78,
        80 : 78,
        81 : 78,
        82 : 78,
        84 : 78,
        85 : 78,
    }

    levelAddresses = {
        11: 0xdfc71,
        12: 0xdfc72,
        13: 0xdfc73,
        21: 0xdfc74,
        22: 0xdfc75,
        23: 0xdfc76,
        31: 0xdfc77,
        41: 0xdfc78,
        42: 0xdfc79,
        43: 0xdfc7A,
        51: 0xdfc7B,
        52: 0xdfc7C,
        53: 0xdfc7D,
        61: 0xdfc7E,
        71: 0xdfc7F,
        72: 0xdfc80,
        73: 0xdfc81,
        81: 0xdfc84,
        82: 0xdfc85,
        83: 0xdfc86,
        91: 0xdfc88,
        92: 0xdfc8e
    }

    levelMonkeyCount = {
        11: 0xdfc99,
        12: 0xdfc9a,
        13: 0xdfc9b,
        21: 0xdfc9c,
        22: 0xdfc9d,
        23: 0xdfc9e,
        31: 0xdfc9f, # Stadium Attack - unused
        41: 0xdfca0,
        42: 0xdfca1,
        43: 0xdfca2,
        51: 0xdfca3,
        52: 0xdfca4,
        53: 0xdfca5,
        61: 0xdfca6, # Gladiator Attack - unused
        71: 0xdfca7,
        72: 0xdfca8,
        73: 0xdfca9,
        81: 0xdfcac,
        82: 0xdfcad,
        83: 0xdfcae,
        91: 0xdfcb0
    }

    baselevelids = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11,
                    0x14, 0x15, 0x16, 0x18, 0x1E]

    firstroomids = [0x01, 0x02, 0x03, 0x06, 0x0B, 0x0F, 0x13, 0x14, 0x16, 0x18, 0x1D, 0x1E, 0x21, 0x24, 0x25, 0x28, 0x2D,
                    0x35, 0x38, 0x3F, 0x45, 0x57]

    roomsperlevel = {
        1: {
            1
        },
        2: {
            2
        },
        3: {
            3, 4, 5
        },
        4: {
            6, 7, 8, 9, 10
        },
        5: {
            11, 12, 13, 14
        },
        6: {
            15, 16, 17, 18
        },
        7: {
            19
        },
        8: {
            20, 21
        },
        9: {
            22, 23
        },
        10: {
            24, 25, 26, 27, 28
        },
        11: {
            29
        },
        12: {
            30, 31, 32
        },
        13: {
            33, 34, 35
        },
        14: {
            36
        },
        15: {
            37, 38, 39
        },
        16: {
            40, 41, 42, 43, 44
        },
        17: {
            45, 46, 47, 49, 50, 51  # Removed boss room
        },
        20: {
            53, 54, 55
        },
        21: {
            56, 57, 58, 59, 60, 61, 62
        },
        22: {
            63, 64, 65, 66, 67  # Removed boss room
        },
        24: {
            69, 72, 75, 76, 77, 78, 79, 80, 81, 82, 84, 85  # Removed boss rooms and coaster spawns
        },
        30: {
            87
        }
    }
    MM_roomspersublevel = {
        24: {

        },
        25: {

        },
        26: {

        },
        27: {
            72, 75, 76
        },
        28: {
            77
        },
        29: {
            78, 79, 80, 81, 82, 84, 85
        },
    }
    roomstostring = {
        1: AEDoor.FF_ENTRY.value,
        2: AEDoor.PO_ENTRY.value,
        3: AEDoor.ML_ENTRY.value,
        4: AEDoor.ML_VOLCANO_ENTRY.value,
        5: AEDoor.ML_TRICERATOPS_ENTRY.value,
        6: AEDoor.TJ_ENTRY.value,
        7: AEDoor.TJ_MUSHROOM_ENTRY.value,
        8: AEDoor.TJ_FISH_ENTRY.value,
        9: AEDoor.TJ_TENT_FISH.value,
        10: AEDoor.TJ_BOULDER_ENTRY.value,
        11: AEDoor.DR_ENTRY.value,
        12: AEDoor.DR_FAN_OUTSIDE_HOLE.value,
        13: AEDoor.DR_OBELISK_BOTTOM.value,
        14: AEDoor.DR_WATER_SIDE.value,
        15: AEDoor.CR_ENTRY.value,
        16: AEDoor.CR_SIDE_ROOM_ENTRY.value,
        17: AEDoor.CR_MAIN_RUINS_ENTRY.value,
        18: AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value,
        19: AEDoor.SA_ENTRY.value,
        20: AEDoor.CB_ENTRY.value,
        21: AEDoor.CB_SECOND_ROOM_ENTRY.value,
        22: AEDoor.CCAVE_ENTRY.value,
        23: AEDoor.CCAVE_SECOND_ROOM_ENTRY.value,
        24: AEDoor.DI_ENTRY.value,
        25: AEDoor.DI_STOMACH_ENTRY.value,
        26: AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value,
        27: AEDoor.DI_TENTACLE.value,  # Invalid starting room when lamps and doors are not shuffled
        28: AEDoor.DI_SLIDE_ROOM_STOMACH.value,
        29: AEDoor.SM_ENTRY.value,
        30: AEDoor.FR_ENTRY.value,
        31: AEDoor.FR_WATER_CAVERNS.value,
        32: AEDoor.FR_CAVERNS_ENTRY.value,
        33: AEDoor.HS_ENTRY.value,
        34: AEDoor.HS_HOT_SPRING.value,
        35: AEDoor.HS_POLAR_BEAR_CAVE.value,
        36: AEDoor.GA_ENTRY.value,
        37: AEDoor.ST_ENTRY.value,
        38: AEDoor.ST_TEMPLE.value,
        39: AEDoor.ST_WELL.value,
        40: AEDoor.WSW_ENTRY.value,
        41: AEDoor.WSW_GONG_ENTRY.value,
        42: AEDoor.WSW_MIDDLE_GONG.value,
        43: AEDoor.WSW_OBSTACLE_MIDDLE.value,
        44: AEDoor.WSW_BARREL_OBSTACLE.value,
        45: AEDoor.CC_ENTRY.value,
        46: AEDoor.CC_CASTLEMAIN_ENTRY.value,
        47: AEDoor.CC_BASEMENT_ENTRY.value,
        49: AEDoor.CC_BUTTON_BASEMENT_WATER.value,
        50: AEDoor.CC_ELEVATOR_CASTLEMAIN.value,
        51: AEDoor.CC_BELL_CASTLE.value,
        53: AEDoor.CP_ENTRY.value,
        54: AEDoor.CP_SEWERSFRONT_OUTSIDE.value,
        55: AEDoor.CP_BARREL_SEWERS_FRONT.value,
        56: AEDoor.SF_ENTRY.value,
        57: AEDoor.SF_FACTORY_OUTSIDE.value,
        58: AEDoor.SF_RC_CAR_FACTORY.value,
        59: AEDoor.SF_LAVA_MECH.value,
        60: AEDoor.SF_WHEEL_FACTORY_BOTTOM.value,
        61: AEDoor.SF_CONVEYOR_LAVA.value,
        62: AEDoor.SF_MECH_FACTORY.value,
        63: AEDoor.TVT_ENTRY.value,
        64: AEDoor.TVT_WATER_LOBBY.value,
        65: AEDoor.TVT_LOBBY_OUTSIDE.value,
        66: AEDoor.TVT_TANK_LOBBY.value,
        67: AEDoor.TVT_FAN_TANK.value,
        69: AEDoor.MM_SL_HUB.value,
        72: AEDoor.MM_COASTER_ENTRY_SL_HUB.value,
        73: AEDoor.MM_COASTER1_ENTRY.value,
        74: AEDoor.MM_COASTER2_ENTRY.value,
        75: AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value,
        76: AEDoor.MM_COFFIN_HAUNTED_HOUSE.value,
        77: AEDoor.MM_WESTERN_SL_HUB.value,
        78: AEDoor.MM_CRATER_SL_HUB.value,
        79: AEDoor.MM_OUTSIDE_CASTLE_CRATER.value,
        80: AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value,
        81: AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value,
        82: AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value,
        84: AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value,
        85: AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value,
        87: AEDoor.PPM_ENTRY.value
    }
    PPMShowCoins = 0x139966 # 0 = no coin icon, 2 = Have coin
    Event_Load_Block = 0x0967E8 # Stops loading some base level's data (Monkey/coins count,events,etc.) if Start room != Vanilla start room
    Event_Load_Block_On = 0x1697015C
    Event_Load_Block_Off = 0x00000000
    # 0x1697015C = Will branch off and ignore loading some base level's data if Start room != Vanilla start room
    # 0x00000000 = Ignore the branch off and load all of the level's meta data (Monkey/coins count,events,etc.) even if Start room != Vanilla start room

# ========================= Lamps / Doors =========================

    lockCamera = 0x162057  # Lock Camera (WsW Gong Room) Locked = 0x80, Free = 0x60
    WSW_RoomState = 0x161F9E # Set to 1 to allow for the last caught monkey event to trigger the Stairs/Doors

    # Array order: bytesToWrite, OpenValue, ClosedValue
    doors_addresses = {
        41: {  # WSW_GongRoom
            0x0BFCCB: [1, 0xF7, 0xFB],  # WSW_Gong_BackDoorVisual1
            0x0BFCCE: [1, 0x00, 0xFF],  # WSW_Gong_CoinDoorVisual1
            0x0BFCCF: [1, 0x00, 0xFF],  # WSW_Gong_CoinDoorVisual2
            0x0BFCEB: [1, 0xF7, 0xFB],  # WSW_Gong_CoinDoorVisual3
            0x0BFBCE: [1, 0xFF, 0x00],  # WSW_Gong_StairVisual1
            0x0BFBCF: [1, 0xFF, 0x00],  # WSW_Gong_StairVisual2
            0x0BFBEE: [1, 0xFF, 0x00],  # WSW_Gong_StairVisual3
            0x0BFBEF: [1, 0xFF, 0x00],  # WSW_Gong_StairVisual4
            0x15F7DB: [1, 0xF7, 0xFB],  # WSW_Gong_BackDoorHitBox
            0x15FAEB: [1, 0xF7, 0xFB],  # WSW_Gong_CoinDoorHitBox
            0x15FC7B: [1, 0x02, 0x00],  # WSW_Gong_Stair1HitBox
            0x15FCB3: [1, 0x01, 0x00],  # WSW_Gong_Stair2HitBox

        },
        44: {  # WSW_BarrelRoom
            0x0C040A: [2, 0xE5E9, 0xE200],  # WSW_Barrel_DoorVisual
            0x170FCA: [2, 0xE5E9, 0xE200],  # WSW_Barrel_DoorHitbox
        },
        67: {  # TVT_FanRoom
            0x0C028A: [2, 0xF3F2, 0xF000],  # TVT_FanDoorVisual
            0x1648C6: [2, 0xF3F2, 0xF000],  # TVT_FanDoorHitBox
            # 0x0BFFAE: [2, 0xFFFF, 0x0000],  # TVT_GlassDoorVisual1
            # 0x0BFFCE: [2, 0xFFFF, 0x0000],  # TVT_GlassDoorVisual2

        },
        69: {  # MM_DoubleDoor
            0x0E7901: [1, 0x00, 0x10],  # MM_DoubleDoorVisualL1
            0x0E7905: [1, 0x10, 0x00],  # MM_DoubleDoorVisualL2
            0x0E790D: [1, 0xF0, 0x00],  # MM_DoubleDoorVisualL3
            0x0E7911: [1, 0x00, 0x10],  # MM_DoubleDoorVisualL4
            0x0E7921: [1, 0x00, 0x10],  # MM_DoubleDoorVisualR1
            0x0E7925: [1, 0xF0, 0x00],  # MM_DoubleDoorVisualR2
            0x0E792D: [1, 0x10, 0x00],  # MM_DoubleDoorVisualR3
            0x0E7931: [1, 0x00, 0x10],  # MM_DoubleDoorVisualR4
            0x170B34: [2, 0xFC50, 0xFE00],  # MM_DoubleDoorHitboxL1
            0x170B38: [2, 0x1680, 0x18D0],  # MM_DoubleDoorHitboxL2
            0x170B3A: [2, 0x0050, 0x0200],  # MM_DoubleDoorHitboxL3
            0x170B3E: [2, 0x0200, 0x0050],  # MM_DoubleDoorHitboxL4
            0x170B6C: [2, 0x03B0, 0x0200],  # MM_DoubleDoorHitboxR1
            0x170B70: [2, 0x1680, 0x18D0],  # MM_DoubleDoorHitboxR2
            0x170B72: [2, 0x0050, 0x0200],  # MM_DoubleDoorHitboxR3
            0x170B76: [2, 0x0200, 0x0050],  # MM_DoubleDoorHitboxR4
        },
        75: {  # Haunted Mansion
            # Nothing to activate there
        },
        76: {
            # Nothing, event is triggering even after the monkeys are manually set
        }
    }

    #Old values, not used but let them here just in case
    #localLamp_localUpdate = 0x097474 # Default: 9062007A. Set this to 0 to disable
    #globalLamp_localUpdate = 0x097574 # Default: 9082007A. Set this to 0 to disable
    #globalLamp_globalUpdate = 0x097568  # 0x097568 Default: 1444000F. Set this to 0 to disable

    # More precise addresses for local monkeys/events

    localLamp_MonkeyDetect = 0x097464
    globalLamp_MonkeyDetect1 = 0x097564
    globalLamp_MonkeyDetect2 = 0x097560

    lampDoors_update = {
        'localLamp_MonkeyDetect_ON':0x3C02800E,
        'localLamp_MonkeyDetect_OFF': 0x00000000,

        'globalLamp_MonkeyDetect1_ON': 0x02712021,
        'globalLamp_MonkeyDetect1_OFF': 0x00000000,
        'globalLamp_MonkeyDetect2_ON': 0x96420126,
        'globalLamp_MonkeyDetect2_OFF': 0x00000000,
    }
    lampDoors_toggles = {
        # CBLamp
        # Array order: bytesToWrite, OpenValue, ClosedValue
        20: {  # CB_LampDoor
            0x0C01AB: [1,0xF4,0xF8],  #CB_LampDoor_Visual1 Open = F4
            0x0C01AF: [1,0x00,0x80],  #CB_LampDoor_Visual2 Open = 00
            0x177B77: [1,0xF4,0xF8],  #CB_LampDoor_Hitbox Open = F4
        },
        53: {  # CP_Lamp
            0x0E7901:[1,0x00,0x10],  # CP_LampDoor_Visual1 Open = 00
            0x0E7903:[1,0x10,0x00],  # CP_LampDoor_Visual2 Open = 10
            0x0E7907:[1,0xF0,0x00],  # CP_LampDoor_Visual3 Open = F0
            0x0E7909:[1,0x00,0x10],  # CP_LampDoor_Visual4 Open = 00
            0x17ABA0:[2,0xE0C0,0xE200],  # CP_LampDoor_Hitbox1 Open = E0C0
            0x17ABA6:[2,0x0040,0x0180],  # CP_LampDoor_Hitbox2 Open = 0040
            0x17ABA9:[2,0x8003,0x8000],  # CP_LampDoor_Hitbox3 Open = 8003
        },
        79: {  # MM_Lamp
            0x0E79D1:[1,0x00,0x10],  # MM_LampDoorL_Visual1 Open = 00
            0x0E79C1:[1,0x00,0x10],  # MM_LampDoorL_Visual2 Open = 00
            0x0E79C5:[1,0xF0,0x00],  # MM_LampDoorL_Visual3 Open = F0
            0x0E79CD:[1,0x10,0x00],  # MM_LampDoorL_Visual4 Open = 10
            0x0E79E1:[1,0x00,0x10],  # MM_LampDoorR_Visual1 Open = 00
            0x0E79E5:[1,0x10,0x00],  # MM_LampDoorR_Visual2 Open = 10
            0x0E79ED:[1,0xF0,0x00],  # MM_LampDoorR_Visual3 Open = F0
            0x0E79F1:[1,0x00,0x10],  # MM_LampDoorR_Visual4 Open = 00
            0x173C08:[2,0xFD40,0xFE80],  # MM_LampDoorL_Hitbox1 Open = FD40
            0x173C0C:[4,0x00400B80,0x018009C0],  # MM_LampDoorL_Hitbox2 Open = 00400B80
            0x173C12:[2,0x0180,0x0040],  # MM_LampDoorL_Hitbox3 Open = 0180
            0x173CB0:[2,0x02C0,0x0180],  # MM_LampDoorR_Hitbox1 Open = 02C0
            0x173CB4:[4,0x00400B80,0x018009C0],  # MM_LampDoorR_Hitbox2 Open = 00400B80
            0x173CBA:[2,0x0180,0x0040]  # MM_LampDoorR_Hitbox3 Open = 0180
        },
        26: {  # DI_Lamp
            0x0BFDAB:[1,0xF2,0xF6],  # DI_LampDoor_Visual1 Open = F2 | Closed = F6
            0x0BFDAF:[1,0x00,0x80],  # DI_LampDoor_Visual2 Open = 00 | Closed = 80
            0x169653:[1,0xF2,0xF6],  # DI_LampDoor_Hitbox Open = F2 | Closed = F6
        },
        46: {  # CrC_Lamp
            0x0E7981:[1,0x00,0x10],  # CrC_LampDoorL_Visual1 Open = 00
            0x0E7985:[1,0xF0,0x00],  # CrC_LampDoorL_Visual2 Open = F0
            0x0E798D:[1,0x10,0x00],  # CrC_LampDoorL_Visual3 Open = 10
            0x0E7991:[1,0x00,0x10],  # CrC_LampDoorL_Visual4 Open = 00
            0x0E79A1:[1,0x00,0x10],  # CrC_LampDoorR_Visual1 Open = 00
            0x0E79A5:[1,0x10,0x00],  # CrC_LampDoorR_Visual2 Open = 10
            0x0E79AD:[1,0xF0,0x00],  # CrC_LampDoorR_Visual3 Open = F0
            0x0E79B1:[1,0x00,0x10],  # CrC_LampDoorR_Visual4 Open = 00
            0x1710C0:[2,0x0040,0x0100],  # CrC_LampDoorL_Hitbox1 Open = 0040
            0x1710C4:[4,0x00400400,0x010002C0],  # CrC_LampDoorL_Hitbox2 Open = 00400400
            0x1710CA:[2,0x0100,0x0040],  # CrC_LampDoorL_Hitbox3 Open = 0100
            0x1710F8:[2,0x03C0,0x0300],  # CrC_LampDoorR_Hitbox1 Open = 03C0
            0x1710FC:[4,0x00400400,0x010002C0],  # CrC_LampDoorR_Hitbox2 Open = 00400400
            0x171102:[2,0x0100,0x0040],  # CrC_LampDoorR_Hitbox3 Open = 0100
        },
        57: {  # SF_Lamp
            0x0C04AD:[1,0x0B,0x0D],  # SF_LampDoor_Visual1 Open = 0B
            0x0C04AF:[1,0x00,0x80],  # SF_LampDoor_Visual2 Open = 00
            0x0C056D:[1,0x11,0x0F],  # SF_LampDoor_Visual3 Open = 11
            0x0C056F:[1,0x00,0x80],  # SF_LampDoor_Visual4 Open = 00
            0x16A499:[1,0x0B,0x0D],  # SF_LampDoor_Hitbox1 Open = 0B
            0x16A461:[1,0x11,0x0F],  # SF_LampDoor_Hitbox2 Open = 11
        },
        65: {  # TVT_LobbyLamp
            0x0C042D:[1,0xFF,0xFD],  # TvtL_LampDoorL_Visual1 Open = FF
            0x0C042F:[1,0x00,0x80],  # TvtL_LampDoorL_Visual2 Open = 00
            0x0C046D:[1,0xF9,0xFB],  # TvtL_LampDoorR_Visual1 Open = F9
            0x0C046F:[1,0x00,0x80],  # TvtL_LampDoorR_Visual2 Open = 00
            0x170C51:[1,0xFF,0xFD],  # TvtL_LampDoorL_Hitbox1 Open = FF
            0x170C65:[1,0x80,0x00],  # TvtL_LampDoorL_Hitbox2 Open = 80
            0x170C89:[1,0xF9,0xFB],  # TvtL_LampDoorR_Hitbox1 Open = F9
            0x170C9D:[1,0x80,0x00],  # TvtL_LampDoorR_Hitbox2 Open = 80
        },
        66: {  # TVT_TankLamp
            0x0C05AC:[4,0x00000DC0,0x80000F40],  # TvtTR_LampDoorL_Visual Open = 00000DC0
            0x0C056C:[4,0x00001240,0x800010C0],  # TvtTR_LampDoorR_Visual Open = 00001240
            0x16C294:[2,0x0DC0,0x0F40],  # TvtTR_LampDoorL_Hitbox1 Open = 0DC0
            0x16C2A9:[1,0x80,0x00],  # TvtTR_LampDoorL_Hitbox2 Open = 80
            0x16C2CC:[2,0x1240,0x10C0],  # TvtTR_LampDoorR_Hitbox1 Open = 1240
            0x16C2E1:[1,0x80,0x00],  # TvtTR_LampDoorR_Hitbox2 Open = 80
        },
    }

    DR_Block_Pushed = 0x18459A  # Address is more of "Entry is open", but same result at the end

    DI_Button_Pressed = 0x1693A6  # Activated = 0x01
    CrC_Basement_ButtonPressed = 0x184D46  # Pressed = 0x01
    CrC_Water_ButtonPressed = 0x173242  # 1 byte: While in room 49 -> Pressed = 0x01, Unpressed = 0x00 -> Send event object
    MM_Painting_Button = 0x17EACE  # Active 0x01 ROOM = 82
    MM_MonkeyHead_Button = 0x174ECE  # Active 0x01 ROOM = 84
    TVT_Lobby_Button = 0x1710E6  # Active 0x01 ROOM = 65

    buttonDoors_toggles = {
        # Array order: bytesToWrite, OpenValue, ClosedValue
        "DI_Button": {
            0x1693A6: [1, 0x01, 0x00],  # DI_Button_Pressed
            0x0BFC8F: [1, 0x00, 0x80],  # DI_Button_DoorVisual
            0x1676F7: [1, 0xDC, 0xE0],  # DI_Button_DoorHitBox
            0x0BFCB8: [4, 0x80162250, 0x80161C34],  # DI_Button_Visual1
            0x0BFCBC: [4, 0x80162268, 0x80161C4C],  # DI_Button_Visual2
            0x0BFCC0: [4, 0x80162390, 0x80161D74],  # DI_Button_Visual3
            0x0BFCC4: [4, 0x80162288, 0x80161C6C],  # DI_Button_Visual4
        },
        "CrCBasementButton": {
            0x184D46: [1, 0x01, 0x00],  # CrC_Basement_ButtonPressed
            0x1810A8: [4, 0xF200F808, 0xF200F900],  # CrC_Basement_DoorHitBox1
            0x1810AC: [4, 0x0008FB00, 0x0100FC08],  # CrC_Basement_DoorHitBox2
            0x1810B0: [4, 0x01000400, 0x00080400],  # CrC_Basement_DoorHitBox3
            0x0E7AC1: [1, 0x00, 0x10],  # CrC_Basement_DoorVisual1
            0x0E7ACD: [1, 0xF0, 0x00],  # CrC_Basement_DoorVisual2
            0x0C1518: [4, 0x80178ADC, 0x80178534],  # CrC_Basement_ButtonVisual1
            0x0C151C: [4, 0x80178AF4, 0x8017854C],  # CrC_Basement_ButtonVisual2
            0x0C1520: [4, 0x80178C14, 0x80178670],  # CrC_Basement_ButtonVisual3
            0x0C1524: [4, 0x80178B0C, 0x80178568],  # CrC_Basement_ButtonVisual4
        },
        "CrCWaterButton": {
            0x0C05AB: [1, 0xDC, 0xE0],  # CrC_Water_DoorVisual
            0x1542BC: [1, 0x00, 0x03],  # TR4_TransitionEnabled
        },
        "TVT_Lobby_Button": {
            0x170EFF: [1, 0x00, 0x01],  # TVT_Lobby_Water_HitBox
            0x170E5D: [1, 0x80, 0x00],  # TVT_Lobby_Water_DoorHitbox1
            0x170E25: [1, 0x80, 0x00],  # TVT_Lobby_Water_DoorHitbox2
            0x0C04CF: [1, 0x00, 0x80],  # TVT_Lobby_Water_DoorVisualP1
            0x0C04EF: [1, 0x00, 0x80],  # TVT_Lobby_Water_DoorVisualP2
            0x0C0698: [2, 0xAC78, 0x8DAC],  # TVT_Lobby_Water_BackColor1
            0x0C069C: [2, 0xAC90, 0x8DC4],  # TVT_Lobby_Water_BackColor2
            0x0C06A0: [2, 0xAE14, 0x8F50],  # TVT_Lobby_Water_BackColor3
            0x0C06A4: [2, 0xAC9C, 0x8DD8],  # TVT_Lobby_Water_BackColor4
            0x0C06B8: [2, 0xB1B8, 0x92F4],  # TVT_Lobby_Water_BackColor5
            0x0C06BC: [2, 0xB1D0, 0x930C],  # TVT_Lobby_Water_ColorS1P1
            0x0C06C0: [2, 0xB2EC, 0x942C],  # TVT_Lobby_Water_ColorS1P2
            0x0C06C4: [2, 0xB1E4, 0x9324],  # TVT_Lobby_Water_TunnelColorS1P1
            0x0C07B8: [2, 0xB9A0, 0xA41C],  # TVT_Lobby_Water_TunnelColorS1P2
            0x0C07BC: [2, 0xB9B8, 0xA434],  # TVT_Lobby_Water_TunnelColorS2P1
            0x0C07C0: [2, 0xBB44, 0xA5C4],  # TVT_Lobby_Water_TunnelColorS2P2
            0x0C07C4: [2, 0xB9C4, 0xA444],  # TVT_Lobby_Water_TunnelColorS2P3
            0x0C07EA: [2, 0xF70C, 0xF100],  # TVT_Lobby_WaterVisual1
            0x0C07EF: [1, 0x00, 0x80],  # TVT_Lobby_WaterVisual2
            0x0C080A: [2, 0xF70C, 0xF100],  # TVT_Lobby_WaterVisual3
            0x0C080F: [1, 0x00, 0x80]  # TVT_Lobby_WaterVisual4
        },
        "MM_MonkeyHead_Button": {
            0x0AFA22: [1, 0x01, 0x00],  # MM_MonkeyHead_Door
        },
        "MM_Painting_Button": {
            0x0C1569: [1, 0x06, 0x02],  # MM_Painting_Visual
            0x18CF31: [1, 0x06, 0x02],  # MM_Painting_HitBox
            0x0C0EAE: [1, 0x03, 0x00],  # MM_Painting_VisualStair1
            0x0C0ECE: [1, 0x03, 0x00],  # MM_Painting_VisualStair2
            0x0C0EEE: [1, 0x03, 0x00],  # MM_Painting_VisualStair3
            0x18CEA1: [1, 0x00, 0x80],  # MM_Painting_HitBoxStair1
            0x18CED9: [1, 0x00, 0x80],  # MM_Painting_HitBoxStair2
            0x18CF11: [1, 0x00, 0x80],  # MM_Painting_HitBoxStair3
            0x0C0F4E: [1, 0x00, 0x01],  # MM_Painting_VisualFence
            0x18CF81: [1, 0x80, 0x00],  # MM_Painting_HitBoxFence
        },
    }

    MM_Professor_RescuedAddress = 0x0DFDDC  # Not Rescued = 0, Rescued = 5
    MM_Clown_State = 0x174072
    MM_Natalie_RescuedAddress = 0x0DFDDD  # Not Rescued = 0, Rescued = 5
    MM_Natalie_CutsceneState = 0x0DFDDE  # play cutscene = 0x00, cutscene played = 0x0D
    MM_Natalie_Rescued_Local = 0x16F34E  # When in Room 76: Natalie rescued = 0x01
    MM_Jake_DefeatedAddress = 0x0DFDE0  # Not defeated = 0, Defeated = 5

    MM_Lobby_DoubleDoor_OpenAddress = 0x174F5E  # Set to 3 for electric fence. If JakeDefeated = 5 it will open the door
    MM_Lobby_JakeDoor_HitboxAddress = 0x1711DD  # Set to 128 to remove the hitbox
    MM_Lobby_JakeDoorFenceAddress = 0x174FA6  # Maybe not used
    MM_Lobby_DoorDetection = 0x0963C8  # 4b: Default to 8C820000. 8C800000 Prevent the door detection code from kicking in

    MM_NatalieDoor_Visual1 = 0x0BFCEF  # Open 0x00
    MM_NatalieDoor_Visual2 = 0x0BFE0F  # Open 0x00
    MM_NatalieDoor_Hitbox = 0x167965  # Open 0x80

    MM_AlertRoom_ButtonPressed = 0x172832 # Not pressed = 0x00, Pressed = 0x01
    MM_AlertRoom_CutsceneTrigger1 = 0x1728C2 # 0x00 Cutscene pending, 0x02 Cutscene Triggered
    MM_AlertRoom_BGCanPushButton = 0x1728DA # 0x03 BG cannot push the button, 0x00 BG can push it
# ===================== Input Related =====================
    BUTTON_BYTE_ADDR_HIGH = 0x0B87A3  # Triggers and Face Buttons (contains bits 8-15 of the 16-bit word)
    BUTTON_BYTE_ADDR_LOW = 0x0B87A2  # D-Pad, Start/Select, L3/R3 (contains bits 0-7 of the 16-bit word)

    # Joystick Analog Axes (8-bit values, 0x80 is center)
    # These 4 addresses are consecutive and will be written as a single 4-byte block starting at ANALOG_START_ADDR
    ANALOG_START_ADDR = 0x0B87A4  # Start of analog joystick data (RY, RX, LY, LX)

    # --- Button Mappings to Bit Positions within a conceptual 16-bit controller word ---
    # This dictionary maps the button name (e.g., "P1 X") to its bit position (0-15)
    # within the combined 16-bit digital input word.
    BUTTON_BIT_MAP = {
        #"P1 Select": 0,  # Bit 0 (low byte)
        "P1 L3": 1,  # Bit 1 (low byte)
        "P1 R3": 2,  # Bit 2 (low byte)
        #"P1 Start": 3,  # Bit 3 (low byte)
        #"P1 Up": 4,  # Bit 4 (low byte)
        #"P1 Right": 5,  # Bit 5 (low byte)
        #"P1 Down": 6,  # Bit 6 (low byte)
        #"P1 Left": 7,  # Bit 7 (low byte)
        "P1 L2": 8,  # Bit 0 (high byte)
        "P1 R2": 9,  # Bit 1 (high byte)
        "P1 L1": 10,  # Bit 2 (high byte)
        "P1 R1": 11,  # Bit 3 (high byte)
        "P1 Triangle": 12,  # Bit 4 (high byte)
        "P1 Circle": 13,  # Bit 5 (high byte)
        "P1 X": 14,  # Bit 6 (high byte)
        "P1 Square": 15,  # Bit 7 (high byte)
    }
    #ANALOG_STICK_ORDER = ["P1 R_Y", "P1 R_X", "P1 L_Y", "P1 L_X"]

    InputListener = 0x0A9A38
    # When in Nathalie's Intro, will be at 2 when the player pressed something
    # Not sure yet, but this value seems to react to inputs depending of actions.

    ANALOG_STICK_ORDER = ["P1 R_Y", "P1 R_X"]
    ANALOG_CENTER_VALUE = 0x80  # Default center value for 8-bit analog sticks (128 decimal)
    RIGHT_JOYSTICK_PSEUDO_INPUT = "Right Joystick"

    ControlsUpdate_DPAD_STARTSELECT_L3R3 = 0x02CA00 # Enabled : A0720000 Disabled : 00000000
    Controls_DPAD_STARTSELECT_L3R3 = 0x0B87A2
    Controls_TriggersShapes = 0x0B87A3


#===================== Gadget Related =====================
    # A bit is 1 if the gadget is unlocked. First bit is club, second is net, etc.
    unlockedGadgetsAddress = 0x0F51C4
    # the gadgets on triangle, square, circle, X on successive bytes
    # club = 0, net = 1, radar = 2, sling = 3, hoop = 4, punch = 5, flyer = 6, car = 7, empty = 255
    triangleGadgetAddress = 0x0F51A8
    squareGadgetAddress = 0x0F51A9
    circleGadgetAddress = 0x0F51AA
    crossGadgetAddress = 0x0F51AB
    # which gadget is currently selected for use
    heldGadgetAddress = 0x0EC2D2

    GadgetValues = 0x0F5124 #32 bytes
    GadgetValues2 = 0x0F5154 #32 bytes

    # Notes:
    # Club  : GadgetValues can be anything,it's fine
    # Net   : GadgetValues can be the last value,it's fine
    # Radar :
    #

    gadgetValue1 = 0x0F5124
    # Radar: ALWAYS equal to Spike_X_Orientation
    # Hoop :
    #   Off = 0x0000, On = 0x0001
    # Punch :
    #   Punch extension 1: (Default) 0x0400
    gadgetValue2 = 0x0F5126
    # Radar: 0x0000 (Not used)
    # Hoop :
    #   hoop_activated : standby = 0x0001, moving = 0x0000
    # Punch :
    #   Punch extension 2: (Default) 0x0400
    gadgetValue3 = 0x0F5128
    # Radar: ALWAYS equal to Spike_Z_Orientation
    # Hoop:
    #   Continuous spin timer (If the joystick spin is fast enough,this value goes up)
    # Punch:
    #   PunchState : (Default) 0x0000

    RadarValues = {
        #0x0F5124 : 0x0000,  #Radar_Orientation1 **Goes with Spike_X_Orientation
        0x0F5126 : 0x0000,  #Radar_Orientation2 **Not used,maybe Spike_Y_Orientation
        #0x0F5128 : 0x0000,  #Radar_Orientation3 **Goes with Spike_Z_Orientation
        0x0F512A : 0x0001,  #Radar_Orientation4

        0x0F5134 : 0xFFFF,  #Radar_SoundChannel1
        0x0F5136 : 0xFFFF,  #Radar_SoundChannel2
        0x0F5138 : 0xE5A3,  #Radar_SoundVariant
        0x0F513A : 0x0000,  #Radar_Scanned?
        0x0F513C : 0x0000,  #Radar_R2Flashing

        }

    # When sling is selected, string position is stored in these:
    SlingValues = {
        0x0F5124 : 0xFF9B,  #SlingRope1_1
        0x0F5126 : 0xFF55,  #SlingRope1_2
        0x0F5128 : 0xE5B9,  #SlingRope1_3

        0x0F512C : 0xFF5C,  #SlingRope2_1
        0x0F512E : 0xFF6B,  #SlingRope2_2
        0x0F5130 : 0xE595,  #SlingRope2_3

        0x0F5134 : 0xFF7B,  #SlingRope3_1
        0x0F5136 : 0xFF7F,  #SlingRope3_2
        0x0F5138 : 0xE5A3,  #SlingRope3_3

    }

    HoopValues = {
        0x0F5124: 0x0000,      # Hoop_Activated
        0x0F5126: 0x0000,      # Hoop_Standby
        0x0F5128: 0x0000,      # Hoop_SpinProgress

        0x0F512A: 0x0000,      # Hoop_AnimationReset
        0x0F512C: 0x00000000,  # Hoop_AnimationState1
        0x0F5130: 0x00000000,  # Hoop_AnimationState2
        0x0F5134: 0x00000000,  # Hoop_AnimationState3

        0x0F5138: 0x00000000,  # Hoop_Orientation_X (Relative)
        0x0F513C: 0x00000000,  # Hoop_Orientation_Z (Relative)

        0x0F5140: 0xFFFFFFFF,  # Hoop_SoundChannel (Might need to reset it to last value)

    }


    PunchValues = {
        0x0F5124: 0x04000400,  # Punch_GlovePosition? (Relative)
        0x0F5128: 0x0000,  # Punch_ExtensionState

        0x0F5134: 0x0000000,  # Punch_Extend2
        0x0F5138: 0x00000000,  # Hoop_AnimationReset
    }

    gadgetUseStateAddress = 0x0B20CC
    CatchingState = 0x0F44A0 # 0x00 Not catching , 0x08 Catching a Monkey
    # 1 = "Net down"
    # 8 = "Net down + can catch"

    trainingRoomProgressAddress = 0x0DFDCC
    GadgetTrainingsUnlockAddress = 0x0978E8  # 4 Bytes -> Prevent the checkup for activating Training Rooms Gadget Trainings (Default: 8C63FDCC, Disable: 0x00000000)

    punchVisualAddress = 0x0E78C0
#===================== WaterNet related =====================
    isUnderwater = 0x0F4DCA
    canDiveAddress = 0x061970 #08018664 - default value (4 bytes)
    canWaterCatchAddress = 0x063C35 # 04 - default value
    swim_oxygenLevelAddress = 0x0F4DC8 # 0x258 = 20 seconds, 0x64 = 3 seconds
    swim_oxygenReplenishSoundAddress = 0x06140C # Default: 0C021DFE, disable: 00000000 4 bytes
    swim_ReplenishOxygenUWAddress = 0x06141C # Default: A4500018, Disable: 00000000 4 bytes
    swim_replenishOxygenOnEntryAddress = 0x0665E8  # Default: A4434DC8, Disable: 00000000 4 bytes
    swim_surfaceDetectionAddress = 0x061420 # Default: 0801853A, disable: 0
    swim_oxygenLowLevelSoundAddress = 0x061458  # Default: 3C02800F, disable: 3C028004 4 bytes
    swim_oxygenMidLevelSoundAddress = 0x061490  # Default: 3C02800F, disable: 3C028004 4 bytes

# ==================== Transition Related ====================
    Nearby_RoomIDAddress = 0x0E38B4
    Nearby_DoorIDAddress   = 0x0E38A4

    Warp_State = 0x0F4480 #0x01 Spawning, 0x02 = Warping back to Hub, 0x03 ??, 0x04 Exiting Transition
    Transition_Screen_Progress = 0x0F4482 #0x18 = Full black screen, 0x00 is normal
    TransitionFlag = 0x0E3893 # Different stage of processing the transitions
    Screen_Fading = 0x0E0930
    LoadingState = 0x0E38B0

    # To translate Transition ID from doorTransitions Table to which address we need to change for the room
    transitionAddresses = {
        # --Array content--
        # TR_ID: {TargetRoomAddress,TargetDoorAddress}
        1: [0x154264, 0x154268],
        2: [0x15428C, 0x154290],
        3: [0x1542B4, 0x1542B8],
        4: [0x1542DC, 0x1542E0],
        5: [0x154304, 0x154308],
        6: [0x15432C, 0x154330],
        7: [0x154354, 0x154358],
        8: [0x15437C, 0x154380],
    }

    TR4_TransitionEnabled = 0x1542BC # For CrC_Boss_Door -> Blocked value: 0x03, Opened Value: 0x00

    transitionPhaseAddress = 0x0F447C # TheDragon Note: If you set Nearby_RoomIDAddress and Nearby_DoorIDAddress
    transitionPhase ={
        "Spawning" : 0x01,      # 0x01 = ?? Maybe spawning
        "DeathScreen": 0x02,    # 0x02 = Black screen fading out
        "Playing" : 0x03,       # 0x03 = in level, not near a transition
        "Nearby" : 0x04,        # 0x04 or 0x05 = near a transition
        "Loaded" : 0x05,
        "InTransition" : 0x06,  # 0x06 = Starting transition
        "NotSpawned" : 0x07, # 0x07 = When in LevelSelect or not spawned?
        "InitialSpawn" : 0x19   # 0x19 = Spawning in air

    }
    Transition1_X = 0x154248 #4 bytes
    Transition1_Y = 0x15424C #4 bytes
    Transition1_Z = 0x154250 #4 bytes

# ==================== Game States + Menu/Level Select ====================
    gameStateAddress = 0x0F4470
    gameState = {
        "Sony": 0x0,
        "Menu": 0x3,
        "Cutscene": 0x8,
        "LevelSelect": 0x9,
        "LevelIntro": 0xA,
        "InLevel": 0xB,
        "Cleared": 0xC,
        "TimeStation": 0xD,
        "Save/Load": 0xE,
        "GameOver": 0xF,
        "NewGadget": 0x11,
        "LevelIntroTT": 0x12,
        "InLevelTT": 0x13,
        "ClearedTT": 0x14,
        "Memory": 0x15,
        "JakeIntro": 0x17,
        "Jake": 0x18,
        "JakeCleared": 0x19,
        "Cutscene2": 0x1A,
        "Book": 0x1C,
        "Credits1": 0x1D,
        "Credits2": 0x1E,
        "PostCredits": 0x23,
        "Demo": 0x24
    }

    currentRoomIdAddress = 0x0F4476
    currentLevelAddress = 0x0F4474

    gameRunningAddress = 0x0B01C0
    newGameAddress = 0x137734
    loadGameAddress = 0x137734

    currentLoadedSave = 0x0E0034  # Not used for now, but could be used somehow
    menuStateAddress = 0x0A9A1B
    menuState2Address = 0x0A9A23

    # LevelSelection addresses (Number -1)
    selectedWorldAddress = 0x139BC4
    selectedLevelAddress = 0x139BCC
    selectedSaveLoadMenuEntry = 0x13AF52

    preventRoomOverride = 0x1380DC #False = 0xA6420126, True = 0
    worldIsScrollingRight = 0x139BD9 # 2 bytes: 0xFFFF = you are changing to the next world
    worldScrollToRightDPAD = 0x1381D4 # 2 bytes: Enabled = 0009, Disabled = 0000
    worldScrollToRightR1 = 0x138270  # 2 bytes: Enabled = 0009, Disabled = 0000

    enteredWorldAddress = 0x0F461C
    enteredLevelAddress = 0x0F461D
    startOfLevelNames = 0x1399E8
    startOfEraNames = 0x139B20

    levelselectFonts = 0x139CF6 # 0x36 = Classic One 0x26 = Current One
    time_attack_Times = 0x0DFD44

    coinsperlevel = {
        1: {
            1
        },
        2: {
            2
        },
        3: {
            3
        },
        4: {
            6, 7, 8, 9
        },
        5: {
            11, 12, 13, 14
        },
        6: {
            17
        },
        7: { #Stadium Attack
            95,96,97,98,99
        },
        8: {
            21
        },
        9: {
            23
        },
        10: {
            24,25,28
        },
        11: {
            29
        },
        12: {
            30, 31, 32
        },
        13: {
            34, 35
        },
        14: { # Gladiator Attack
            90,91,92,93,94
        },
        15: {
            37, 38, 39
        },
        16: {
            40, 41, 44
        },
        17: {
            45, 46, 49, 50
        },
        20: {
            53, 54, 55
        },
        21: {
            58, 59
        },
        22: {
            64, 66
        },
        24: {
            73, 74, 75, 77, 78, 79, 80, 82, 84, 85
        },
        30: { #PPM

        }
    }
# ==================== Kickout Prevention ====================
    localLevelState = 0x0F447E # Same as level state, but can be changed to impact some behaviors (Like Kickout Prevention)

    kickoutofLevelAddress = 0x097B98  # 4 bytes: Default 84830188, Disable kickout = 00000000 (050E67EC)
    kickoutofLevelAddress2 = 0x097B70  # BETTER 4 bytes: Default 24020001, Disable kickout = 00000000

    CrC_BossPhaseAddress = 0x17475E
    CrC_BossLife = 0x0E69E1
    # 0 :not started
    # 1 and 2: In cinematic
    # 3: In fight
    # 4: Opening door
    # 5: Victory

    TVT_BossPhase = 0x17C5A2
    TVT_BossLife = 0x143E1F
    # 1 In cinematic for boss
    # 2 Boss in waiting
    # 3 Boss in progress

    CrC_DoorVisual = 0x0C062B
    CrC_DoorHitBox = 0x164FFB

    CrC_kickoutofLevelAddress = 0x097B20  # 4 bytes: Default 86020166, Disable kickout = 00000000
    CrC_kickoutofLevelAddress2 = 0x097B24 # 4 bytes: Default 84830188, Disable kickout = 00000000
    TVT_kickoutofLevelAddress = 0x097B00  # 4 bytes: Default 84830188, Disable kickout = 00000000

# ==================== Spike Addresses ====================
    spikeStateAddress = 0x0EC250
    spikeState2Address = 0x0EC23E
    spikeIdleTimer = 0x0EC328 # Put this to 0x0000 to wake up
    spikeGroundStateAddress = 0x0EC23D
    spikeHittableAddress = 0x0EC227
    spikeSuperFlyerUseState = 0x0EC2E0 # 0x00 = SuperFlyer activated
    # This value is also shared with the Spawn/Return to hub animations, but we don't have a use for that in the rando

    spikeSkinPalette = 0x0EC1E5
    spikeColor = 0x0EC2D4
    #spikeColor2 = 0x0EC1E6
    spike_RedColorUpdate = 0x063AEC
    spike_GreenColorUpdate = 0x063B00
    spike_BlueColorUpdate = 0x063B04
    spike_LavaOrIceTimer = 0x0EC2D0 # 0100 means Spike is being launched in the air

    Spike_X_PosAddress = 0x0EC204 #4 bytes
    Spike_Y_PosAddress = 0x0EC208 #4 bytes
    Spike_Z_PosAddress = 0x0EC20C #4 bytes

    Spike_X_Orientation = 0x0EC240 #4 bytes
    Spike_Z_Orientation = 0x0EC244 #4 bytes

    Spike_Y_Velocity_Value = 0x0EC214     # 1 byte  : Max Speed -> Up : 0x01, Down : 0x80
    Spike_Y_Velocity_BitFlag = 0x0EC215   # 3 bytes : 0xFFFFFF = Up | 0x000000 = Down

    # Velocity Update addresses
    # These addresses are responsible for updating velocity
    # Setting them to 0 prevents velocity from changing.
    # *It will still stay at the value it was BEFORE setting these addresses to 0*
    Spike_VelocityUpdates = {
        0x063424: [4, 0xAE0A0030, 0x00000000],  # SpikeX_VelocityUpdate
        0x06343C: [4, 0xAE090034, 0x00000000],  # SpikeY_VelocityUpdate
        0x063480: [4, 0xAE040038, 0x00000000],  # SpikeZ_VelocityUpdate
    }

    #Postion Update addresses
    #These addresses lock the ability for the game to update the XYZ values of Spike
    # When set to 0 Spike cannot move
    Spike_PosUpdates = {
        0x0728A8 : [4,0xAE030000,0x00000000],  # SpikeX_PosLock1
        0x0734D4 : [4,0xAE620000,0x00000000],  # SpikeX_PosLock2
        0x0738B0 : [4,0xAE620000,0x00000000],  # SpikeX_PosLock3

        0x072E80 : [4,0xAE020004,0x00000000],  # SpikeY_PosLock1
        0x072E8C : [4,0xAE020004,0x00000000],  # SpikeY_PosLock2

        0x0728E4 : [4,0xAE030008,0x00000000],  # SpikeZ_PosLock1
        0x0734CC : [4,0xAE630008,0x00000000],  # SpikeZ_PosLock2
        0x0738C8 : [4,0xAE620008,0x00000000],  # SpikeZ_PosLock3
    }
    Spike_CanMove = 0x0F4450 # 0x00 means can move, 0x01 means cannot move (And every odd bit like 0x03)

    SpecialRoom_CameraMode = 0x0C0798 #0x00 = Fixed, 0x01 = Overhead, 0x02 = StrictFollowCam
    SpecialRoom_CameraRotateLeft = 0x0C07C4 #0x00 = Not tilted, 0xFF = Tilted
    SpecialRoom_CameraRotateRight = 0x0C07C5 #0x00 = Not tilted, 0xFF = Tilted
    Inside_CameraMode = 0x0C0F98 #0x00 = Fixed, 0x01 = Overhead, 0x02 = StrictFollowCam
    Inside_CameraRotateLeft = 0x0C0FC4 #0x00 = Not tilted, 0xFF = Tilted
    Inside_CameraRotateRight = 0x0C0FC5 #0x00 = Not tilted, 0xFF = Tilted
    Boss_CameraMode = 0x0C1798 #0x00 = Fixed, 0x01 = Overhead, 0x02 = StrictFollowCam
    Boss_CameraRotateLeft = 0x0C17C4 #0x00 = Not tilted, 0xFF = Tilted
    Boss_CameraRotateRight = 0x0C17C5 #0x00 = Not tilted, 0xFF = Tilted
    Outside_CameraMode = 0x0C1F98 #0x00 = Fixed, 0x01 = Overhead, 0x02 = StrictFollowCam
    Outside_CameraRotateLeft = 0x0C1FC4 #0x00 = Not tilted, 0xFF = Tilted
    Outside_CameraRotateRight = 0x0C1FC5 #0x00 = Not tilted, 0xFF = Tilted



    SPIKE_INVINCIBILITY_ADDR = 0x05E748 # Address for Spike's invincibility flag/state
    SPIKE_GOLDEN_FORM_ADDR = 0x0EC2E2    # Address for Spike's golden visual state flag/model ID

    # Values to write to these addresses to enable/disable effects.
    INVINCIBLE_ON_VALUE = 0xA46200E0  # Value to write to SPIKE_INVINCIBILITY_ADDR to make Spike invincible
    INVINCIBLE_OFF_VALUE = 0xA46200E8  # Value to write to SPIKE_INVINCIBILITY_ADDR to make Spike vulnerable

    GOLDEN_ON_VALUE = 0x01  # Value to write to SPIKE_GOLDEN_FORM_ADDR to activate golden form
    GOLDEN_OFF_VALUE = 0x00  # Value to write to SPIKE_GOLDEN_FORM_ADDR to revert form

    colortable = {
        "vanilla": 0, #This value is not important as the value is overwritten in the client
        "dark": 0x000000,
        "white": 0xFFFFFF,
        "red": 0x0000FF,
        "green": 0x00FF00,
        "blue": 0xFF0000,
        "yellow": 0x00FFFF,
        "cyan": 0xFFFF00,
        "magenta": 0xFF00FF
    }

    skinpallettable = {
        "vanilla": 0x1030,
        #"white": 0x7617,
        "white": 0x101F, # Pallet seems consistent in all levels, used as base for spikecolor
        "grey": 0x5E03,
        "purple": 0x1000,
        "orange": 0x2F2F,
        "green": 0x35F6,
        "red": 0x2F00,
        "yellow": 0x1065,
        "darkblue": 0x2600, #6F65
        "voidwhite": 0x2E05,
        "voidpurple": 0x4DFA,
        "voidorange": 0x0007,
        #"voidred": 0x372E, #More like voidbrown sometimes
        "neonpink": 0x3BFF,
        "neongreen": 0x2EF6,
        "greenskin": 0x0131,
        "blueskin": 0x75D8,
        "purpleskin": 0x75D7,
        "alien": 0x3300,
        "alien2": 0x350C,
        "metal": 0x3674,
        "rave": 0x1D2F
    }

# ==================== Specter Related ====================
    # Specter bosses values
    S1_P1_Life = 0x1408FB
    S1_P2_State = 0x144A04
    S1_P2_Life = 0x144A06
    S1_P1_FightTrigger = 0x16A5B2 # 1 byte. Put to 0x0D to prevent the fight, 0x00 to allow the fight
    S1_Cutscene_Redirection = 0x137C28  # 4 bytes. When GameState is 0A, change the last 2 bytes to redirect another gamestate after the cutscene (Redirect to time station = 2403000D)
    S2_isCaptured = 0x142328
    S2_Cutscene_Redirection = 0x05C5F0  # 4 bytes. Change the last 2 bytes to redirect another gamestate after the cutscene (Redirect to time station = 2403000D)
    S2_CutsceneState = 0x163272
    S2_GlobalCutsceneState = 0x0DFDE4 # 0x05 means you beat Specter previously
    # S1_LArm_Life = 0x14474E
    # S1_RArm_Life = 0x1446B6
    tempSpecter2CompleteAddress = 0x0DFBEE
    tempSpecter1CompleteAddress = 0x0DFBEF
    Specter2CompleteAddress = 0x0E00FE
    Specter1CompleteAddress = 0x0E00FF
