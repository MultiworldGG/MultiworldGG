from .Names import LocationName


class WLBlock:
    blockName: str
    locationID: int

    def __init__(self, blockName: str, locationID: int):
        self.blockName = blockName
        self.locationID = locationID


block_info_dict = {
    # Rice Beach, same blockIDs for 0x17 rb flooded
    0x07D30A: WLBlock(LocationName.ricebeach_1_block1, 0xA82000),
    0x07D30D: WLBlock(LocationName.ricebeach_1_block2, 0xA82001),
    0x07D511: WLBlock(LocationName.ricebeach_1_block3, 0xA82002),
    0x07D12D: WLBlock(LocationName.ricebeach_1_block4, 0xA82003),
    0x07D12F: WLBlock(LocationName.ricebeach_1_block5, 0xA82004),
    0x07D131: WLBlock(LocationName.ricebeach_1_block6, 0xA82005),
    0x07D133: WLBlock(LocationName.ricebeach_1_block7, 0xA82006),
    0x07D42F: WLBlock(LocationName.ricebeach_1_block8, 0xA82007),
    0x07D430: WLBlock(LocationName.ricebeach_1_block9, 0xA82008),
    0x07DB42: WLBlock(LocationName.ricebeach_1_block10, 0xA82009),
    0x07DB49: WLBlock(LocationName.ricebeach_1_block11, 0xA82010),
    0x07D555: WLBlock(LocationName.ricebeach_1_block12, 0xA82011),
    0x07D370: WLBlock(LocationName.ricebeach_1_block13, 0xA82012),
    0x07D375: WLBlock(LocationName.ricebeach_1_block14, 0xA82013),
    0x07D39E: WLBlock(LocationName.ricebeach_1_block15, 0xA82014),
    0x07D3A3: WLBlock(LocationName.ricebeach_1_block16, 0xA82015),
    0x07D3A8: WLBlock(LocationName.ricebeach_1_block17, 0xA82016),
    0x07DCA8: WLBlock(LocationName.ricebeach_1_block18, 0xA82017),
    0x0FD90D: WLBlock(LocationName.ricebeach_2_block1, 0xA82018),
    0x0FD83A: WLBlock(LocationName.ricebeach_2_block2, 0xA82019),
    0x0FDC40: WLBlock(LocationName.ricebeach_2_block3, 0xA82020),
    0x0FDC48: WLBlock(LocationName.ricebeach_2_block4, 0xA82021),
    0x0FDC50: WLBlock(LocationName.ricebeach_2_block5, 0xA82022),
    0x0FDC58: WLBlock(LocationName.ricebeach_2_block6, 0xA82023),
    0x0FD848: WLBlock(LocationName.ricebeach_2_block7, 0xA82024),
    0x0FD850: WLBlock(LocationName.ricebeach_2_block8, 0xA82025),
    0x0FDC84: WLBlock(LocationName.ricebeach_2_block9, 0xA82026),
    0x0FDC85: WLBlock(LocationName.ricebeach_2_block10, 0xA82027),
    0x0FDC86: WLBlock(LocationName.ricebeach_2_block11, 0xA82028),
    0x0FD996: WLBlock(LocationName.ricebeach_2_block12, 0xA82029),
    0x0FD9AF: WLBlock(LocationName.ricebeach_2_block13, 0xA82030),
    0x0FDAB4: WLBlock(LocationName.ricebeach_2_block14, 0xA82031),
    0x0FD0BB: WLBlock(LocationName.ricebeach_2_block15, 0xA82032),
    0x0FD0BC: WLBlock(LocationName.ricebeach_2_block16, 0xA82033),
    0x0FDBCC: WLBlock(LocationName.ricebeach_2_block17, 0xA82034),
    0x0FCBD5: WLBlock(LocationName.ricebeach_2_block18, 0xA82035),
    0x0FD3F3: WLBlock(LocationName.ricebeach_2_block19, 0xA82036),
    0x0FCB1C: WLBlock(LocationName.ricebeach_2_block20, 0xA82037),
    0x0ED119: WLBlock(LocationName.ricebeach_3_block1, 0xA82038),
    0x0ED11F: WLBlock(LocationName.ricebeach_3_block2, 0xA82039),
    0x0ED431: WLBlock(LocationName.ricebeach_3_block3, 0xA82040),
    0x0ED537: WLBlock(LocationName.ricebeach_3_block4, 0xA82041),
    0x0ED056: WLBlock(LocationName.ricebeach_3_block5, 0xA82042),
    0x0ED371: WLBlock(LocationName.ricebeach_3_block6, 0xA82043),
    0x0ED482: WLBlock(LocationName.ricebeach_3_block7, 0xA82044),
    0x0EDB9B: WLBlock(LocationName.ricebeach_3_block8, 0xA82045),
    0x0EDBA5: WLBlock(LocationName.ricebeach_3_block9, 0xA82046),
    0x0ED0B8: WLBlock(LocationName.ricebeach_3_block10, 0xA82047),
    0x0EDBD1: WLBlock(LocationName.ricebeach_3_block11, 0xA82048),
    0x0EDBD2: WLBlock(LocationName.ricebeach_3_block12, 0xA82049),
    0x0EDBD3: WLBlock(LocationName.ricebeach_3_block13, 0xA82050),
    0x0EDBD4: WLBlock(LocationName.ricebeach_3_block14, 0xA82051),
    0x0ECAD2: WLBlock(LocationName.ricebeach_3_block15, 0xA82052),
    0x0CD630: WLBlock(LocationName.ricebeach_4_block1, 0xA82053),
    0x0CD24B: WLBlock(LocationName.ricebeach_4_block2, 0xA82054),
    0x0CD267: WLBlock(LocationName.ricebeach_4_block3, 0xA82055),
    0x0CD183: WLBlock(LocationName.ricebeach_4_block4, 0xA82056),
    0x0CD69E: WLBlock(LocationName.ricebeach_4_block5, 0xA82057),
    0x0CD6A4: WLBlock(LocationName.ricebeach_4_block6, 0xA82058),
    0x19DB32: WLBlock(LocationName.ricebeach_5_block1, 0xA82059),
    0x19D998: WLBlock(LocationName.ricebeach_5_block2, 0xA82060),
    0x19DAAC: WLBlock(LocationName.ricebeach_5_block3, 0xA82061),
    0x19DAAD: WLBlock(LocationName.ricebeach_5_block4, 0xA82062),
    0x19DAAE: WLBlock(LocationName.ricebeach_5_block5, 0xA82063),
    0x19DBB1: WLBlock(LocationName.ricebeach_5_block6, 0xA82064),
    0x29DB13: WLBlock(LocationName.ricebeach_6_block1, 0xA82065),
    0x29DA2A: WLBlock(LocationName.ricebeach_6_block2, 0xA82066),
    0x29DA31: WLBlock(LocationName.ricebeach_6_block3, 0xA82067),
    0x29DA38: WLBlock(LocationName.ricebeach_6_block4, 0xA82068),
    0x29DA3F: WLBlock(LocationName.ricebeach_6_block5, 0xA82069),
    0x29DA46: WLBlock(LocationName.ricebeach_6_block6, 0xA82070),
    0x29DA4D: WLBlock(LocationName.ricebeach_6_block7, 0xA82071),
    0x29DA54: WLBlock(LocationName.ricebeach_6_block8, 0xA82072),
    0x06D908: WLBlock(LocationName.mtteapot_7_block1, 0xA82073),
    0x06D612: WLBlock(LocationName.mtteapot_7_block2, 0xA82074),
    0x06D613: WLBlock(LocationName.mtteapot_7_block3, 0xA82075),
    0x06D614: WLBlock(LocationName.mtteapot_7_block4, 0xA82076),
    0x06DA1B: WLBlock(LocationName.mtteapot_7_block5, 0xA82077),
    0x06D81E: WLBlock(LocationName.mtteapot_7_block6, 0xA82078),
    0x06D81F: WLBlock(LocationName.mtteapot_7_block7, 0xA82079),
    0x06D820: WLBlock(LocationName.mtteapot_7_block8, 0xA82080),
    0x06D821: WLBlock(LocationName.mtteapot_7_block9, 0xA82081),
    0x06D822: WLBlock(LocationName.mtteapot_7_block10, 0xA82082),
    0x06D823: WLBlock(LocationName.mtteapot_7_block11, 0xA82083),
    0x06D824: WLBlock(LocationName.mtteapot_7_block12, 0xA82084),
    0x06D825: WLBlock(LocationName.mtteapot_7_block13, 0xA82085),
    0x06D826: WLBlock(LocationName.mtteapot_7_block14, 0xA82086),
    0x06D827: WLBlock(LocationName.mtteapot_7_block15, 0xA82087),
    0x06D828: WLBlock(LocationName.mtteapot_7_block16, 0xA82088),
    0x06D829: WLBlock(LocationName.mtteapot_7_block17, 0xA82089),
    0x06D82A: WLBlock(LocationName.mtteapot_7_block18, 0xA82090),
    0x06D82B: WLBlock(LocationName.mtteapot_7_block19, 0xA82091),
    0x06D82C: WLBlock(LocationName.mtteapot_7_block20, 0xA82092),
    0x06D248: WLBlock(LocationName.mtteapot_7_block21, 0xA82093),
    0x06D24E: WLBlock(LocationName.mtteapot_7_block22, 0xA82094),
    0x06C749: WLBlock(LocationName.mtteapot_7_block23, 0xA82095),
    0x06C74D: WLBlock(LocationName.mtteapot_7_block24, 0xA82096),
    0x06D37E: WLBlock(LocationName.mtteapot_7_block25, 0xA82097),
    0x06D98F: WLBlock(LocationName.mtteapot_7_block26, 0xA82098),
    0x06D990: WLBlock(LocationName.mtteapot_7_block27, 0xA82099),
    0x10DC1A: WLBlock(LocationName.mtteapot_8_block1, 0xA82100),
    0x10DC1C: WLBlock(LocationName.mtteapot_8_block2, 0xA82101),
    0x10DB2F: WLBlock(LocationName.mtteapot_8_block3, 0xA82102),
    0x10DB30: WLBlock(LocationName.mtteapot_8_block4, 0xA82103),
    0x10DB31: WLBlock(LocationName.mtteapot_8_block5, 0xA82104),
    0x10DB32: WLBlock(LocationName.mtteapot_8_block6, 0xA82105),
    0x10D958: WLBlock(LocationName.mtteapot_8_block7, 0xA82106),
    0x10D86E: WLBlock(LocationName.mtteapot_8_block8, 0xA82107),
    0x10CF62: WLBlock(LocationName.mtteapot_8_block9, 0xA82108),
    0x10C46D: WLBlock(LocationName.mtteapot_8_block10, 0xA82109),
    0x10D980: WLBlock(LocationName.mtteapot_8_block11, 0xA82110),
    0x10D985: WLBlock(LocationName.mtteapot_8_block12, 0xA82111),
    0x10D989: WLBlock(LocationName.mtteapot_8_block13, 0xA82112),
    0x10D98E: WLBlock(LocationName.mtteapot_8_block14, 0xA82113),
    0x10DCAF: WLBlock(LocationName.mtteapot_8_block15, 0xA82114),
    0x10DAB2: WLBlock(LocationName.mtteapot_8_block16, 0xA82115),
    0x10DBB7: WLBlock(LocationName.mtteapot_8_block17, 0xA82116),
    0x10DCBA: WLBlock(LocationName.mtteapot_8_block18, 0xA82117),
    0x10DBBF: WLBlock(LocationName.mtteapot_8_block19, 0xA82118),
    0x10DAC2: WLBlock(LocationName.mtteapot_8_block20, 0xA82119),
    0x10DBC7: WLBlock(LocationName.mtteapot_8_block21, 0xA82120),
    0x10D1E2: WLBlock(LocationName.mtteapot_8_block22, 0xA82121),
    0x0DDA0F: WLBlock(LocationName.mtteapot_9_block1, 0xA82122),
    0x0DDB16: WLBlock(LocationName.mtteapot_9_block2, 0xA82123),
    0x0DDA20: WLBlock(LocationName.mtteapot_9_block3, 0xA82124),
    0x0DDB33: WLBlock(LocationName.mtteapot_9_block4, 0xA82125),
    0x0DDB3D: WLBlock(LocationName.mtteapot_9_block5, 0xA82126),
    0x0DD235: WLBlock(LocationName.mtteapot_9_block6, 0xA82127),
    0x0DCA27: WLBlock(LocationName.mtteapot_9_block7, 0xA82128),
    0x0DCB24: WLBlock(LocationName.mtteapot_9_block8, 0xA82129),
    0x0DCA22: WLBlock(LocationName.mtteapot_9_block9, 0xA82130),
    0x0DCA11: WLBlock(LocationName.mtteapot_9_block10, 0xA82131),
    0x0DCB0E: WLBlock(LocationName.mtteapot_9_block11, 0xA82132),
    0x0DCB0D: WLBlock(LocationName.mtteapot_9_block12, 0xA82133),
    0x0DCD0A: WLBlock(LocationName.mtteapot_9_block13, 0xA82134),
    0x0DDA68: WLBlock(LocationName.mtteapot_9_block14, 0xA82135),
    0x0DDB84: WLBlock(LocationName.mtteapot_9_block15, 0xA82136),
    0x05DC15: WLBlock(LocationName.mtteapot_10_block1, 0xA82137),
    0x05D916: WLBlock(LocationName.mtteapot_10_block2, 0xA82138),
    0x05D81E: WLBlock(LocationName.mtteapot_10_block3, 0xA82139),
    0x05DC21: WLBlock(LocationName.mtteapot_10_block4, 0xA82140),
    0x05D328: WLBlock(LocationName.mtteapot_10_block5, 0xA82141),
    0x05D92B: WLBlock(LocationName.mtteapot_10_block6, 0xA82142),
    0x05D93D: WLBlock(LocationName.mtteapot_10_block7, 0xA82143),
    0x05D944: WLBlock(LocationName.mtteapot_10_block8, 0xA82144),
    0x05DC4C: WLBlock(LocationName.mtteapot_10_block9, 0xA82145),
    0x05DC58: WLBlock(LocationName.mtteapot_10_block10, 0xA82146),
    0x05D155: WLBlock(LocationName.mtteapot_10_block11, 0xA82147),
    0x05DB66: WLBlock(LocationName.mtteapot_10_block12, 0xA82148),
    0x05DB67: WLBlock(LocationName.mtteapot_10_block13, 0xA82149),
    0x05DB68: WLBlock(LocationName.mtteapot_10_block14, 0xA82150),
    0x05C96F: WLBlock(LocationName.mtteapot_10_block15, 0xA82151),
    0x05C970: WLBlock(LocationName.mtteapot_10_block16, 0xA82152),
    0x05C971: WLBlock(LocationName.mtteapot_10_block17, 0xA82153),
    0x05D274: WLBlock(LocationName.mtteapot_10_block18, 0xA82154),
    0x05DBA4: WLBlock(LocationName.mtteapot_10_block19, 0xA82155),
    0x05DBA6: WLBlock(LocationName.mtteapot_10_block20, 0xA82156),
    0x05DBA8: WLBlock(LocationName.mtteapot_10_block21, 0xA82157),
    0x05DBAA: WLBlock(LocationName.mtteapot_10_block22, 0xA82158),
    0x11C616: WLBlock(LocationName.mtteapot_11_block1, 0xA82159),
    0x11C90C: WLBlock(LocationName.mtteapot_11_block2, 0xA82160),
    0x11CC1A: WLBlock(LocationName.mtteapot_11_block3, 0xA82161),
    0x11CF14: WLBlock(LocationName.mtteapot_11_block4, 0xA82162),
    0x11D217: WLBlock(LocationName.mtteapot_11_block5, 0xA82163),
    0x11D50E: WLBlock(LocationName.mtteapot_11_block6, 0xA82164),
    0x11D815: WLBlock(LocationName.mtteapot_11_block7, 0xA82165),
    0x11DB06: WLBlock(LocationName.mtteapot_11_block8, 0xA82166),
    0x11D604: WLBlock(LocationName.mtteapot_11_block9, 0xA82167),
    0x11D607: WLBlock(LocationName.mtteapot_11_block10, 0xA82168),
    0x11D004: WLBlock(LocationName.mtteapot_11_block11, 0xA82169),
    0x11D00D: WLBlock(LocationName.mtteapot_11_block12, 0xA82170),
    0x11D96C: WLBlock(LocationName.mtteapot_11_block13, 0xA82171),
    0x11D975: WLBlock(LocationName.mtteapot_11_block14, 0xA82172),
    0x11DB34: WLBlock(LocationName.mtteapot_11_block15, 0xA82173),
    0x11C32B: WLBlock(LocationName.mtteapot_11_block16, 0xA82174),
    0x11DB95: WLBlock(LocationName.mtteapot_11_block17, 0xA82175),
    0x11C885: WLBlock(LocationName.mtteapot_11_block18, 0xA82176),
    0x09DB22: WLBlock(LocationName.mtteapot_12_block1, 0xA82177),
    0x09DB28: WLBlock(LocationName.mtteapot_12_block2, 0xA82178),
    0x09DB2E: WLBlock(LocationName.mtteapot_12_block3, 0xA82179),
    0x09DB40: WLBlock(LocationName.mtteapot_12_block4, 0xA82180),
    0x09DB5E: WLBlock(LocationName.mtteapot_12_block5, 0xA82181),
    0x09D4A3: WLBlock(LocationName.mtteapot_12_block6, 0xA82182),
    0x09CCA3: WLBlock(LocationName.mtteapot_12_block7, 0xA82183),
    0x09C7AA: WLBlock(LocationName.mtteapot_12_block8, 0xA82184),
    0x0ADC15: WLBlock(LocationName.mtteapot_13_block1, 0xA82185),
    0x0AD916: WLBlock(LocationName.mtteapot_13_block2, 0xA82186),
    0x0AD81E: WLBlock(LocationName.mtteapot_13_block3, 0xA82187),
    0x0ADC21: WLBlock(LocationName.mtteapot_13_block4, 0xA82188),
    0x0AD328: WLBlock(LocationName.mtteapot_13_block5, 0xA82189),
    0x0AD92B: WLBlock(LocationName.mtteapot_13_block6, 0xA82190),
    0x0AD93D: WLBlock(LocationName.mtteapot_13_block7, 0xA82191),
    0x0AD944: WLBlock(LocationName.mtteapot_13_block8, 0xA82192),
    0x0ADC4C: WLBlock(LocationName.mtteapot_13_block9, 0xA82193),
    0x0ADC58: WLBlock(LocationName.mtteapot_13_block10, 0xA82194),
    0x0AD156: WLBlock(LocationName.mtteapot_13_block11, 0xA82195),
    0x0ACA5A: WLBlock(LocationName.mtteapot_13_block12, 0xA82196),
    0x0ACA6F: WLBlock(LocationName.mtteapot_13_block13, 0xA82197),
    0x0ACA70: WLBlock(LocationName.mtteapot_13_block14, 0xA82198),
    0x0ACA71: WLBlock(LocationName.mtteapot_13_block15, 0xA82199),
    0x0AD970: WLBlock(LocationName.mtteapot_13_block16, 0xA82200),
    0x0AD5AD: WLBlock(LocationName.mtteapot_13_block17, 0xA82201),
    0x0AD5B3: WLBlock(LocationName.mtteapot_13_block18, 0xA82202),
    0x0AD5B9: WLBlock(LocationName.mtteapot_13_block19, 0xA82203),
    0x0AD0AD: WLBlock(LocationName.mtteapot_13_block20, 0xA82204),
    0x0AD0B4: WLBlock(LocationName.mtteapot_13_block21, 0xA82205),
    0x21D90D: WLBlock(LocationName.sherbetland_14_block1, 0xA82206),
    0x21DA36: WLBlock(LocationName.sherbetland_14_block2, 0xA82207),
    0x21D965: WLBlock(LocationName.sherbetland_14_block3, 0xA82208),
    0x21D97E: WLBlock(LocationName.sherbetland_14_block4, 0xA82209),
    0x21DB96: WLBlock(LocationName.sherbetland_14_block5, 0xA82210),
    0x21DAE2: WLBlock(LocationName.sherbetland_14_block6, 0xA82211),
    0x21D9EC: WLBlock(LocationName.sherbetland_14_block7, 0xA82212),
    0x02C92B: WLBlock(LocationName.sherbetland_15_block1, 0xA82213),
    0x02C92C: WLBlock(LocationName.sherbetland_15_block2, 0xA82214),
    0x02CB48: WLBlock(LocationName.sherbetland_15_block3, 0xA82215),
    0x02CB49: WLBlock(LocationName.sherbetland_15_block4, 0xA82216),
    0x02D33A: WLBlock(LocationName.sherbetland_15_block5, 0xA82217),
    0x02DB4A: WLBlock(LocationName.sherbetland_15_block6, 0xA82218),
    0x02DA99: WLBlock(LocationName.sherbetland_15_block7, 0xA82219),
    0x02DB9A: WLBlock(LocationName.sherbetland_15_block8, 0xA82220),
    0x02DC9B: WLBlock(LocationName.sherbetland_15_block9, 0xA82221),
    0x02DCB9: WLBlock(LocationName.sherbetland_15_block10, 0xA82222),
    0x02DCC6: WLBlock(LocationName.sherbetland_15_block11, 0xA82223),
    0x02CA5E: WLBlock(LocationName.sherbetland_15_block12, 0xA82224),
    0x02CA73: WLBlock(LocationName.sherbetland_15_block13, 0xA82225),
    0x04DB05: WLBlock(LocationName.sherbetland_16_block1, 0xA82226),
    0x04D918: WLBlock(LocationName.sherbetland_16_block2, 0xA82227),
    0x04D922: WLBlock(LocationName.sherbetland_16_block3, 0xA82228),
    0x04DAD3: WLBlock(LocationName.sherbetland_16_block4, 0xA82229),
    0x04CB63: WLBlock(LocationName.sherbetland_16_block5, 0xA82230),
    0x04CB6C: WLBlock(LocationName.sherbetland_16_block6, 0xA82231),
    0x04CBA4: WLBlock(LocationName.sherbetland_16_block7, 0xA82232),
    0x04CB84: WLBlock(LocationName.sherbetland_16_block8, 0xA82233),
    0x08DA09: WLBlock(LocationName.sherbetland_17_block1, 0xA82234),
    0x08DA0A: WLBlock(LocationName.sherbetland_17_block2, 0xA82235),
    0x08DB2C: WLBlock(LocationName.sherbetland_17_block3, 0xA82236),
    0x08DA3C: WLBlock(LocationName.sherbetland_17_block4, 0xA82237),
    0x08DA3D: WLBlock(LocationName.sherbetland_17_block5, 0xA82238),
    0x08D5BD: WLBlock(LocationName.sherbetland_17_block6, 0xA82239),
    0x08D0B2: WLBlock(LocationName.sherbetland_17_block7, 0xA82240),
    0x08CBBC: WLBlock(LocationName.sherbetland_17_block8, 0xA82241),
    0x08C6B3: WLBlock(LocationName.sherbetland_17_block9, 0xA82242),
    0x08DCE7: WLBlock(LocationName.sherbetland_17_block10, 0xA82243),
    0x08DCE8: WLBlock(LocationName.sherbetland_17_block11, 0xA82244),
    0x08DCE9: WLBlock(LocationName.sherbetland_17_block12, 0xA82245),
    0x08D9E7: WLBlock(LocationName.sherbetland_17_block13, 0xA82246),
    0x08D9E8: WLBlock(LocationName.sherbetland_17_block14, 0xA82247),
    0x08D9E9: WLBlock(LocationName.sherbetland_17_block15, 0xA82248),
    0x08DB95: WLBlock(LocationName.sherbetland_17_block16, 0xA82249),
    0x08DB96: WLBlock(LocationName.sherbetland_17_block17, 0xA82250),
    0x08DB97: WLBlock(LocationName.sherbetland_17_block18, 0xA82251),
    0x20DA1B: WLBlock(LocationName.sherbetland_18_block1, 0xA82252),
    0x20D951: WLBlock(LocationName.sherbetland_18_block2, 0xA82253),
    0x20D952: WLBlock(LocationName.sherbetland_18_block3, 0xA82254),
    0x20DA91: WLBlock(LocationName.sherbetland_18_block4, 0xA82255),
    0x20DBCF: WLBlock(LocationName.sherbetland_18_block5, 0xA82256),
    0x20DBD0: WLBlock(LocationName.sherbetland_18_block6, 0xA82257),
    0x20DBD1: WLBlock(LocationName.sherbetland_18_block7, 0xA82258),
    0x20DBF6: WLBlock(LocationName.sherbetland_18_block8, 0xA82259),
    0x20DBF8: WLBlock(LocationName.sherbetland_18_block9, 0xA82260),
    0x18DA2D: WLBlock(LocationName.sherbetland_19_block1, 0xA82261),
    0x18DA30: WLBlock(LocationName.sherbetland_19_block2, 0xA82262),
    0x18DA3D: WLBlock(LocationName.sherbetland_19_block3, 0xA82263),
    0x18DA40: WLBlock(LocationName.sherbetland_19_block4, 0xA82264),
    0x18C566: WLBlock(LocationName.sherbetland_19_block5, 0xA82265),
    0x18CC63: WLBlock(LocationName.sherbetland_19_block6, 0xA82266),
    0x18CF69: WLBlock(LocationName.sherbetland_19_block7, 0xA82267),
    0x18D66D: WLBlock(LocationName.sherbetland_19_block8, 0xA82268),
    0x18D966: WLBlock(LocationName.sherbetland_19_block9, 0xA82269),
    0x18D979: WLBlock(LocationName.sherbetland_19_block10, 0xA82270),
    0x18D68C: WLBlock(LocationName.sherbetland_19_block11, 0xA82271),
    0x18D49E: WLBlock(LocationName.sherbetland_19_block12, 0xA82272),
    0x18CB93: WLBlock(LocationName.sherbetland_19_block13, 0xA82273),
    0x18DBB6: WLBlock(LocationName.sherbetland_19_block14, 0xA82274),
    0x03DA0B: WLBlock(LocationName.stovecanyon_20_block1, 0xA82275),
    0x03DB22: WLBlock(LocationName.stovecanyon_20_block2, 0xA82276),
    0x03DA27: WLBlock(LocationName.stovecanyon_20_block3, 0xA82277),
    0x03DB33: WLBlock(LocationName.stovecanyon_20_block4, 0xA82278),
    0x03DB41: WLBlock(LocationName.stovecanyon_20_block5, 0xA82279),
    0x03D84E: WLBlock(LocationName.stovecanyon_20_block6, 0xA82280),
    0x03D855: WLBlock(LocationName.stovecanyon_20_block7, 0xA82281),
    0x03DA5D: WLBlock(LocationName.stovecanyon_20_block8, 0xA82282),
    0x03DA61: WLBlock(LocationName.stovecanyon_20_block9, 0xA82283),
    0x03DC80: WLBlock(LocationName.stovecanyon_20_block10, 0xA82284),
    0x03CB9C: WLBlock(LocationName.stovecanyon_20_block11, 0xA82285),
    0x15D820: WLBlock(LocationName.stovecanyon_21_block1, 0xA82286),
    0x15DC46: WLBlock(LocationName.stovecanyon_21_block2, 0xA82287),
    0x15DD63: WLBlock(LocationName.stovecanyon_21_block3, 0xA82288),
    0x15DD64: WLBlock(LocationName.stovecanyon_21_block4, 0xA82289),
    0x15DA8A: WLBlock(LocationName.stovecanyon_21_block5, 0xA82290),
    0x15DA8E: WLBlock(LocationName.stovecanyon_21_block6, 0xA82291),
    0x15DA92: WLBlock(LocationName.stovecanyon_21_block7, 0xA82292),
    0x16DA26: WLBlock(LocationName.stovecanyon_22_block1, 0xA82293),
    0x16DC4A: WLBlock(LocationName.stovecanyon_22_block2, 0xA82294),
    0x16DB4E: WLBlock(LocationName.stovecanyon_22_block3, 0xA82295),
    0x16DA86: WLBlock(LocationName.stovecanyon_22_block4, 0xA82296),
    0x16DB90: WLBlock(LocationName.stovecanyon_22_block5, 0xA82297),
    0x16D99C: WLBlock(LocationName.stovecanyon_22_block6, 0xA82298),
    0x16CB26: WLBlock(LocationName.stovecanyon_22_block7, 0xA82299),
    0x27D90A: WLBlock(LocationName.stovecanyon_23_block1, 0xA82300),
    0x27D85B: WLBlock(LocationName.stovecanyon_23_block2, 0xA82301),
    0x27D37B: WLBlock(LocationName.stovecanyon_23_block3, 0xA82302),
    0x27DAA0: WLBlock(LocationName.stovecanyon_23_block4, 0xA82303),
    0x27DAA1: WLBlock(LocationName.stovecanyon_23_block5, 0xA82304),
    0x27DBE0: WLBlock(LocationName.stovecanyon_23_block6, 0xA82305),
    0x27DDF5: WLBlock(LocationName.stovecanyon_23_block7, 0xA82306),
    0x27D9FA: WLBlock(LocationName.stovecanyon_23_block8, 0xA82307),
    0x1BDB25: WLBlock(LocationName.stovecanyon_24_block1, 0xA82308),
    0x1BC99A: WLBlock(LocationName.stovecanyon_24_block2, 0xA82309),
    0x1BCA6D: WLBlock(LocationName.stovecanyon_24_block3, 0xA82310),
    0x1BD3BC: WLBlock(LocationName.stovecanyon_24_block4, 0xA82311),
    0x1BD890: WLBlock(LocationName.stovecanyon_24_block5, 0xA82312),
    0x1BCB74: WLBlock(LocationName.stovecanyon_24_block6, 0xA82313),
    0x1BD66D: WLBlock(LocationName.stovecanyon_24_block7, 0xA82314),
    0x1BD671: WLBlock(LocationName.stovecanyon_24_block8, 0xA82315),
    0x1CDA07: WLBlock(LocationName.stovecanyon_25_block1, 0xA82316),
    0x1CD821: WLBlock(LocationName.stovecanyon_25_block2, 0xA82317),
    0x1CDB38: WLBlock(LocationName.stovecanyon_25_block3, 0xA82318),
    0x1CDB41: WLBlock(LocationName.stovecanyon_25_block4, 0xA82319),
    0x1CDB4F: WLBlock(LocationName.stovecanyon_25_block5, 0xA82320),
    0x1CD977: WLBlock(LocationName.stovecanyon_25_block6, 0xA82321),
    0x1CD978: WLBlock(LocationName.stovecanyon_25_block7, 0xA82322),
    0x00DB39: WLBlock(LocationName.ssteacup_26_block1, 0xA82323),
    0x00DA49: WLBlock(LocationName.ssteacup_26_block2, 0xA82324),
    0x00DA4A: WLBlock(LocationName.ssteacup_26_block3, 0xA82325),
    0x00DA4B: WLBlock(LocationName.ssteacup_26_block4, 0xA82326),
    0x00D855: WLBlock(LocationName.ssteacup_26_block5, 0xA82327),
    0x00DC65: WLBlock(LocationName.ssteacup_26_block6, 0xA82328),
    0x00D995: WLBlock(LocationName.ssteacup_26_block7, 0xA82329),
    0x00CB66: WLBlock(LocationName.ssteacup_26_block8, 0xA82330),
    0x00CB95: WLBlock(LocationName.ssteacup_26_block9, 0xA82331),
    0x00CB9A: WLBlock(LocationName.ssteacup_26_block10, 0xA82332),
    0x00CB9B: WLBlock(LocationName.ssteacup_26_block11, 0xA82333),
    0x1EDB07: WLBlock(LocationName.ssteacup_27_block1, 0xA82334),
    0x1EDB08: WLBlock(LocationName.ssteacup_27_block2, 0xA82335),
    0x1ED412: WLBlock(LocationName.ssteacup_27_block3, 0xA82336),
    0x1EDA24: WLBlock(LocationName.ssteacup_27_block4, 0xA82337),
    0x1ED734: WLBlock(LocationName.ssteacup_27_block5, 0xA82338),
    0x1ED736: WLBlock(LocationName.ssteacup_27_block6, 0xA82339),
    0x1ED738: WLBlock(LocationName.ssteacup_27_block7, 0xA82340),
    0x1EDA34: WLBlock(LocationName.ssteacup_27_block8, 0xA82341),
    0x1EDA36: WLBlock(LocationName.ssteacup_27_block9, 0xA82342),
    0x1EDA38: WLBlock(LocationName.ssteacup_27_block10, 0xA82343),
    0x1ECB9B: WLBlock(LocationName.ssteacup_27_block11, 0xA82344),
    0x1EDBA6: WLBlock(LocationName.ssteacup_27_block12, 0xA82345),
    0x1EDCAC: WLBlock(LocationName.ssteacup_27_block13, 0xA82346),
    0x1EDBB5: WLBlock(LocationName.ssteacup_27_block14, 0xA82347),
    0x1ED9B9: WLBlock(LocationName.ssteacup_27_block15, 0xA82348),
    0x1EDBBE: WLBlock(LocationName.ssteacup_27_block16, 0xA82349),
    0x1EDCC6: WLBlock(LocationName.ssteacup_27_block17, 0xA82350),
    0x1EDCC7: WLBlock(LocationName.ssteacup_27_block18, 0xA82351),
    0x1EDCC8: WLBlock(LocationName.ssteacup_27_block19, 0xA82352),
    0x1EDBC9: WLBlock(LocationName.ssteacup_27_block20, 0xA82353),
    0x1EDBCA: WLBlock(LocationName.ssteacup_27_block21, 0xA82354),
    0x1EDBCB: WLBlock(LocationName.ssteacup_27_block22, 0xA82355),
    0x1ED9CD: WLBlock(LocationName.ssteacup_27_block23, 0xA82356),
    0x1EDCCE: WLBlock(LocationName.ssteacup_27_block24, 0xA82357),
    0x1EDAED: WLBlock(LocationName.ssteacup_27_block25, 0xA82358),
    0x1FDB0A: WLBlock(LocationName.ssteacup_28_block1, 0xA82359),
    0x1FDB0D: WLBlock(LocationName.ssteacup_28_block2, 0xA82360),
    0x1FD91D: WLBlock(LocationName.ssteacup_28_block3, 0xA82361),
    0x1FDA2B: WLBlock(LocationName.ssteacup_28_block4, 0xA82362),
    0x1FDA4B: WLBlock(LocationName.ssteacup_28_block5, 0xA82363),
    0x1FDA55: WLBlock(LocationName.ssteacup_28_block6, 0xA82364),
    0x1FDA90: WLBlock(LocationName.ssteacup_28_block7, 0xA82365),
    0x1FDA94: WLBlock(LocationName.ssteacup_28_block8, 0xA82366),
    0x1FDBE7: WLBlock(LocationName.ssteacup_28_block9, 0xA82367),
    0x1FDBE8: WLBlock(LocationName.ssteacup_28_block10, 0xA82368),
    0x0BDA06: WLBlock(LocationName.ssteacup_29_block1, 0xA82369),
    0x0BCACD: WLBlock(LocationName.ssteacup_29_block2, 0xA82370),
    0x0BD279: WLBlock(LocationName.ssteacup_29_block3, 0xA82371),
    0x0BCB5F: WLBlock(LocationName.ssteacup_29_block4, 0xA82372),
    0x0BCAE9: WLBlock(LocationName.ssteacup_29_block5, 0xA82373),
    0x0BCAEA: WLBlock(LocationName.ssteacup_29_block6, 0xA82374),
    0x0BCAEB: WLBlock(LocationName.ssteacup_29_block7, 0xA82375),
    0x0BDAF2: WLBlock(LocationName.ssteacup_29_block8, 0xA82376),
    0x0BDAF4: WLBlock(LocationName.ssteacup_29_block9, 0xA82377),
    0x0BDAE3: WLBlock(LocationName.ssteacup_29_block10, 0xA82378),
    0x0BDAE6: WLBlock(LocationName.ssteacup_29_block11, 0xA82379),
    0x14DB15: WLBlock(LocationName.ssteacup_30_block1, 0xA82380),
    0x14DB22: WLBlock(LocationName.ssteacup_30_block2, 0xA82381),
    0x14DB23: WLBlock(LocationName.ssteacup_30_block3, 0xA82382),
    0x14DB24: WLBlock(LocationName.ssteacup_30_block4, 0xA82383),
    0x14DB4C: WLBlock(LocationName.ssteacup_30_block5, 0xA82384),
    0x14CB29: WLBlock(LocationName.ssteacup_30_block6, 0xA82385),
    0x14D86D: WLBlock(LocationName.ssteacup_30_block7, 0xA82386),
    0x14D86E: WLBlock(LocationName.ssteacup_30_block8, 0xA82387),
    0x14CF69: WLBlock(LocationName.ssteacup_30_block9, 0xA82388),
    0x14CD72: WLBlock(LocationName.ssteacup_30_block10, 0xA82389),
    0x14C86B: WLBlock(LocationName.ssteacup_30_block11, 0xA82390),
    0x14C870: WLBlock(LocationName.ssteacup_30_block12, 0xA82391),
    0x14D695: WLBlock(LocationName.ssteacup_30_block13, 0xA82392),
    0x14D387: WLBlock(LocationName.ssteacup_30_block14, 0xA82393),
    0x14D389: WLBlock(LocationName.ssteacup_30_block15, 0xA82394),
    0x14D17B: WLBlock(LocationName.ssteacup_30_block16, 0xA82395),
    0x14CE7F: WLBlock(LocationName.ssteacup_30_block17, 0xA82396),
    0x14CC9E: WLBlock(LocationName.ssteacup_30_block18, 0xA82397),
    0x14CFA5: WLBlock(LocationName.ssteacup_30_block19, 0xA82398),
    0x14CDA9: WLBlock(LocationName.ssteacup_30_block20, 0xA82399),
    0x14C8A0: WLBlock(LocationName.ssteacup_30_block21, 0xA82400),
    0x14C8A5: WLBlock(LocationName.ssteacup_30_block22, 0xA82401),
    0x14D8B9: WLBlock(LocationName.ssteacup_30_block23, 0xA82402),
    # pw lake flooded
    0x26DC0E: WLBlock(LocationName.parsleywoods_31_block1, 0xA82403),
    0x26DA2C: WLBlock(LocationName.parsleywoods_31_block2, 0xA82404),
    0x26DA2D: WLBlock(LocationName.parsleywoods_31_block3, 0xA82405),
    0x26D932: WLBlock(LocationName.parsleywoods_31_block4, 0xA82406),
    0x26D933: WLBlock(LocationName.parsleywoods_31_block5, 0xA82407),
    0x26DC47: WLBlock(LocationName.parsleywoods_31_block6, 0xA82408),
    0x26DC6C: WLBlock(LocationName.parsleywoods_31_block7, 0xA82409),
    0x26DB7D: WLBlock(LocationName.parsleywoods_31_block8, 0xA82410),
    0x26D9AF: WLBlock(LocationName.parsleywoods_31_block9, 0xA82411),
    0x26D9B5: WLBlock(LocationName.parsleywoods_31_block10, 0xA82412),
    0x26D9B6: WLBlock(LocationName.parsleywoods_31_block11, 0xA82413),
    0x26D9BC: WLBlock(LocationName.parsleywoods_31_block12, 0xA82414),
    0x26D9BD: WLBlock(LocationName.parsleywoods_31_block13, 0xA82415),
    0x26DBC1: WLBlock(LocationName.parsleywoods_31_block14, 0xA82416),
    # pw lake drained
    0x2AD40E: WLBlock(LocationName.parsleywoods_31_drained_block1, 0xA82417),
    0x2ADC1D: WLBlock(LocationName.parsleywoods_31_drained_block2, 0xA82418),
    0x2ADC1E: WLBlock(LocationName.parsleywoods_31_drained_block3, 0xA82419),
    0x2AD22C: WLBlock(LocationName.parsleywoods_31_drained_block4, 0xA82420),
    0x2AD133: WLBlock(LocationName.parsleywoods_31_drained_block5, 0xA82421),
    0x2AD941: WLBlock(LocationName.parsleywoods_31_drained_block6, 0xA82422),
    0x2AD447: WLBlock(LocationName.parsleywoods_31_drained_block7, 0xA82423),
    0x2AD46C: WLBlock(LocationName.parsleywoods_31_drained_block8, 0xA82424),
    0x2ADB6E: WLBlock(LocationName.parsleywoods_31_drained_block9, 0xA82425),
    0x2ADB76: WLBlock(LocationName.parsleywoods_31_drained_block10, 0xA82426),
    0x2AD37D: WLBlock(LocationName.parsleywoods_31_drained_block11, 0xA82427),
    0x2ADBA1: WLBlock(LocationName.parsleywoods_31_drained_block12, 0xA82428),
    0x2AD1AF: WLBlock(LocationName.parsleywoods_31_drained_block13, 0xA82429),
    0x1DD90F: WLBlock(LocationName.parsleywoods_32_block1, 0xA82430),
    0x1DDA80: WLBlock(LocationName.parsleywoods_32_block2, 0xA82431),
    0x1DD88B: WLBlock(LocationName.parsleywoods_32_block3, 0xA82432),
    0x1DDADD: WLBlock(LocationName.parsleywoods_32_block4, 0xA82433),
    0x01CA0F: WLBlock(LocationName.parsleywoods_33_block1, 0xA82434),
    0x01CA0E: WLBlock(LocationName.parsleywoods_33_block2, 0xA82435),
    0x01DB4F: WLBlock(LocationName.parsleywoods_33_block3, 0xA82436),
    0x01CB53: WLBlock(LocationName.parsleywoods_33_block4, 0xA82437),
    0x01CB4E: WLBlock(LocationName.parsleywoods_33_block5, 0xA82438),
    0x01DCB1: WLBlock(LocationName.parsleywoods_33_block6, 0xA82439),
    0x01DCAE: WLBlock(LocationName.parsleywoods_33_block7, 0xA82440),
    0x01DBA4: WLBlock(LocationName.parsleywoods_33_block8, 0xA82441),
    0x01DBA3: WLBlock(LocationName.parsleywoods_33_block9, 0xA82442),
    0x01CA71: WLBlock(LocationName.parsleywoods_33_block10, 0xA82443),
    0x13DB05: WLBlock(LocationName.parsleywoods_34_block1, 0xA82444),
    0x13DB19: WLBlock(LocationName.parsleywoods_34_block2, 0xA82445),
    0x13CC0B: WLBlock(LocationName.parsleywoods_34_block3, 0xA82446),
    0x13C210: WLBlock(LocationName.parsleywoods_34_block4, 0xA82447),
    0x13C524: WLBlock(LocationName.parsleywoods_34_block5, 0xA82448),
    0x13C444: WLBlock(LocationName.parsleywoods_34_block6, 0xA82449),
    0x13C470: WLBlock(LocationName.parsleywoods_34_block7, 0xA82450),
    0x13C471: WLBlock(LocationName.parsleywoods_34_block8, 0xA82451),
    0x13C98F: WLBlock(LocationName.parsleywoods_34_block9, 0xA82452),
    0x13D397: WLBlock(LocationName.parsleywoods_34_block10, 0xA82453),
    0x13D398: WLBlock(LocationName.parsleywoods_34_block11, 0xA82454),
    0x13C8A3: WLBlock(LocationName.parsleywoods_34_block12, 0xA82455),
    0x12DB10: WLBlock(LocationName.parsleywoods_35_block1, 0xA82456),
    0x12CB44: WLBlock(LocationName.parsleywoods_35_block2, 0xA82457),
    0x12CC51: WLBlock(LocationName.parsleywoods_35_block3, 0xA82458),
    0x12DBA6: WLBlock(LocationName.parsleywoods_35_block4, 0xA82459),
    0x12DBE2: WLBlock(LocationName.parsleywoods_35_block5, 0xA82460),
    0x1AD90F: WLBlock(LocationName.parsleywoods_36_block1, 0xA82461),
    0x1AD923: WLBlock(LocationName.parsleywoods_36_block2, 0xA82462),
    0x1ADB4C: WLBlock(LocationName.parsleywoods_36_block3, 0xA82463),
    0x1ADB5F: WLBlock(LocationName.parsleywoods_36_block4, 0xA82464),
    0x1ADB6D: WLBlock(LocationName.parsleywoods_36_block5, 0xA82465),
    0x1ADB94: WLBlock(LocationName.parsleywoods_36_block6, 0xA82466),
    0x1ADB95: WLBlock(LocationName.parsleywoods_36_block7, 0xA82467),
    0x1ADB96: WLBlock(LocationName.parsleywoods_36_block8, 0xA82468),
    0x1ADAFD: WLBlock(LocationName.parsleywoods_36_block9, 0xA82469),
    0x25DA1E: WLBlock(LocationName.syrupcastle_37_block1, 0xA82470),
    0x25DA1F: WLBlock(LocationName.syrupcastle_37_block2, 0xA82471),
    0x25DA20: WLBlock(LocationName.syrupcastle_37_block3, 0xA82472),
    0x25DA6D: WLBlock(LocationName.syrupcastle_37_block4, 0xA82473),
    0x25DA6E: WLBlock(LocationName.syrupcastle_37_block5, 0xA82474),
    0x25DA6F: WLBlock(LocationName.syrupcastle_37_block6, 0xA82475),
    0x25D997: WLBlock(LocationName.syrupcastle_37_block7, 0xA82476),
    0x25D998: WLBlock(LocationName.syrupcastle_37_block8, 0xA82477),
    0x25DB9E: WLBlock(LocationName.syrupcastle_37_block9, 0xA82478),
    0x25DB9F: WLBlock(LocationName.syrupcastle_37_block10, 0xA82479),
    0x25DBA0: WLBlock(LocationName.syrupcastle_37_block11, 0xA82480),
    0x25DBA5: WLBlock(LocationName.syrupcastle_37_block12, 0xA82481),
    0x25DBA6: WLBlock(LocationName.syrupcastle_37_block13, 0xA82482),
    0x25DBA7: WLBlock(LocationName.syrupcastle_37_block14, 0xA82483),
    0x25DBAC: WLBlock(LocationName.syrupcastle_37_block15, 0xA82484),
    0x25DBAD: WLBlock(LocationName.syrupcastle_37_block16, 0xA82485),
    0x25DBAE: WLBlock(LocationName.syrupcastle_37_block17, 0xA82486),
    0x25DABF: WLBlock(LocationName.syrupcastle_37_block18, 0xA82487),
    0x25DAC1: WLBlock(LocationName.syrupcastle_37_block19, 0xA82488),
    0x25DBC6: WLBlock(LocationName.syrupcastle_37_block20, 0xA82489),
    0x25DCD4: WLBlock(LocationName.syrupcastle_37_block21, 0xA82490),
    0x22D315: WLBlock(LocationName.syrupcastle_38_block1, 0xA82491),
    0x22D310: WLBlock(LocationName.syrupcastle_38_block2, 0xA82492),
    0x22D30B: WLBlock(LocationName.syrupcastle_38_block3, 0xA82493),
    0x22DA17: WLBlock(LocationName.syrupcastle_38_block4, 0xA82494),
    0x22DA24: WLBlock(LocationName.syrupcastle_38_block5, 0xA82495),
    0x22CDE4: WLBlock(LocationName.syrupcastle_38_block6, 0xA82496),
    0x22DA4A: WLBlock(LocationName.syrupcastle_38_block7, 0xA82497),
    0x22DB8A: WLBlock(LocationName.syrupcastle_38_block8, 0xA82498),
    0x22DAA6: WLBlock(LocationName.syrupcastle_38_block9, 0xA82499),
    0x23DB0F: WLBlock(LocationName.syrupcastle_39_block1, 0xA82500),
    0x23DA15: WLBlock(LocationName.syrupcastle_39_block2, 0xA82501),
    0x23D828: WLBlock(LocationName.syrupcastle_39_block3, 0xA82502),
    0x23D82B: WLBlock(LocationName.syrupcastle_39_block4, 0xA82503),
    0x23D94C: WLBlock(LocationName.syrupcastle_39_block5, 0xA82504),
    0x23CB12: WLBlock(LocationName.syrupcastle_39_block6, 0xA82505),
    0x23CB1B: WLBlock(LocationName.syrupcastle_39_block7, 0xA82506),
    0x23DAA7: WLBlock(LocationName.syrupcastle_39_block8, 0xA82507),
    0x23CA8D: WLBlock(LocationName.syrupcastle_39_block9, 0xA82508),
    0x23DB74: WLBlock(LocationName.syrupcastle_39_block10, 0xA82509),
    0x23DB8C: WLBlock(LocationName.syrupcastle_39_block11, 0xA82510),
    0x28DA09: WLBlock(LocationName.syrupcastle_40_block1, 0xA82511),
    0x28DA0C: WLBlock(LocationName.syrupcastle_40_block2, 0xA82512),
    0x28D819: WLBlock(LocationName.syrupcastle_40_block3, 0xA82513),
    0x28D823: WLBlock(LocationName.syrupcastle_40_block4, 0xA82514),
    0x28D82A: WLBlock(LocationName.syrupcastle_40_block5, 0xA82515),
    0x28D832: WLBlock(LocationName.syrupcastle_40_block6, 0xA82516),
    0x28DC36: WLBlock(LocationName.syrupcastle_40_block7, 0xA82517),
    0x28DC42: WLBlock(LocationName.syrupcastle_40_block8, 0xA82518),
    0x28D843: WLBlock(LocationName.syrupcastle_40_block9, 0xA82519),
    0x28D845: WLBlock(LocationName.syrupcastle_40_block10, 0xA82520),
    0x28D970: WLBlock(LocationName.syrupcastle_40_block11, 0xA82521),
    0x28D883: WLBlock(LocationName.syrupcastle_40_block12, 0xA82522),
    0x28D888: WLBlock(LocationName.syrupcastle_40_block13, 0xA82523),
    0x28DACB: WLBlock(LocationName.syrupcastle_40_block14, 0xA82524),
    0x28CB15: WLBlock(LocationName.syrupcastle_40_block15, 0xA82525),
    0x28CB1D: WLBlock(LocationName.syrupcastle_40_block16, 0xA82526),
    0x28CB25: WLBlock(LocationName.syrupcastle_40_block17, 0xA82527),
    0x28CB4A: WLBlock(LocationName.syrupcastle_40_block18, 0xA82528),
}
