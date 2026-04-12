import typing
from enum import Enum

from BaseClasses import ItemClassification


class Rels(Enum):
    aaa = "aaa"
    aji = "aji"
    bom = "bom"
    dmo = "dmo"
    dol = "dol"
    dou = "dou"
    eki = "eki"
    end = "end"
    gon = "gon"
    gor = "gor"
    gra = "gra"
    hei = "hei"
    hom = "hom"
    jin = "jin"
    jon = "jon"
    kpa = "kpa"
    las = "las"
    moo = "moo"
    mri = "mri"
    muj = "muj"
    nok = "nok"
    pik = "pik"
    rsh = "rsh"
    sys = "sys"
    tik = "tik"
    tou = "tou"
    tou2 = "tou2"
    usu = "usu"
    win = "win"
    yuu = "yuu"

rel_filepaths = [
    "aaa",
    "aji",
    "bom",
    "dou",
    "eki",
    "end",
    "gon",
    "gor",
    "gra",
    "hei",
    "hom",
    "init",
    "jin",
    "jon",
    "kpa",
    "las",
    "mod",
    "moo",
    "mri",
    "muj",
    "nok",
    "pik",
    "rsh",
    "tik",
    "tou",
    "tou2",
    "usu",
    "win",
]

class GSWType(Enum):
    GSW = 0
    GSWF = 1

starting_partners = [
    "Goombella",
    "Koops",
    "Bobbery",
    "Yoshi",
    "Flurrie",
    "Vivian",
    "Ms. Mowz"
]

shop_items = [
    78780030, 78780023, 78780053, 78780003, 78780041, 78780019,
    78780096, 78780102, 78780073, 78780080, 78780072, 78780098,
    78780125, 78780112, 78780131, 78780118, 78780110, 78780111,
    78780173, 78780177, 78780172, 78780175, 78780174, 78780176,
    78780247, 78780248, 78780251, 78780249, 78780246, 78780250,
    78780268, 78780284, 78780273, 78780274, 78780271, 78780283,
    78780317, 78780313, 78780315, 78780312, 78780316, 78780310,
    78780465, 78780462, 78780466, 78780463, 78780464, 78780469,
    78780531, 78780526, 78780524, 78780530, 78780525, 78780529,
    78780569, 78780564, 78780567, 78780573, 78780566, 78780574
]

shop_names = [
    "gor_01",
    "gor_03",
    "tik_00",
    "nok_00",
    "mri_07",
    "tou_01",
    "usu_01",
    "muj_01",
    "rsh_03",
    "bom_02"
]

location_gsw_info = {
    78780000: (GSWType.GSWF, 1247, 1),
    78780001: (GSWType.GSWF, 5568, 1),
    78780002: (GSWType.GSW, 1700, 7),
    78780004: (GSWType.GSWF, 6099, 1),
    78780045: (GSWType.GSWF, 5569, 1),
    78780046: (GSWType.GSWF, 5573, 1),
    78780047: (GSWType.GSWF, 5570, 1),
    78780048: (GSWType.GSWF, 5571, 1),
    78780049: (GSWType.GSWF, 5572, 1),
    78780055: (GSWType.GSWF, 1195, 1),
    78780060: (GSWType.GSW, 1700, 17),
    78780061: (GSWType.GSWF, 1248, 1),
    78780062: (GSWType.GSWF, 5525, 1),
    78780064: (GSWType.GSWF, 5575, 1),
    78780065: (GSWType.GSWF, 5574, 1),
    78780066: (GSWType.GSWF, 5576, 1),
    78780067: (GSWType.GSWF, 5577, 1),
    78780068: (GSWType.GSWF, 5578, 1),
    78780069: (GSWType.GSW, 1709, 3),
    78780070: (GSWType.GSW, 1709, 10),
    78780082: (GSWType.GSWF, 6100, 1),
    78780089: (GSWType.GSWF, 5528, 1),
    78780090: (GSWType.GSWF, 5527, 1),
    78780091: (GSWType.GSWF, 5580, 1),
    78780092: (GSWType.GSWF, 5581, 1),
    78780093: (GSWType.GSWF, 5582, 1),
    78780094: (GSWType.GSWF, 5579, 1),
    78780103: (GSWType.GSWF, 5584, 1),
    78780104: (GSWType.GSWF, 5583, 1),
    78780124: (GSWType.GSWF, 5530, 1),
    78780126: (GSWType.GSWF, 1354, 1),
    78780127: (GSWType.GSWF, 5586, 1),
    78780128: (GSWType.GSWF, 5587, 1),
    78780129: (GSWType.GSWF, 5588, 1),
    78780130: (GSWType.GSWF, 5585, 1),
    78780132: (GSWType.GSWF, 5589, 1),
    78780133: (GSWType.GSWF, 5531, 1),
    78780134: (GSWType.GSWF, 1356, 1),
    78780135: (GSWType.GSWF, 5590, 1),
    78780136: (GSWType.GSWF, 1337, 1),
    78780137: (GSWType.GSWF, 1357, 1),
    78780138: (GSWType.GSWF, 1358, 1),
    78780139: (GSWType.GSWF, 5591, 1),
    78780140: (GSWType.GSWF, 5532, 1),
    78780141: (GSWType.GSWF, 5592, 1),
    78780142: (GSWType.GSWF, 5593, 1),
    78780143: (GSWType.GSWF, 1359, 1),
    78780144: (GSWType.GSWF, 5533, 1),
    78780145: (GSWType.GSWF, 5595, 1),
    78780146: (GSWType.GSWF, 5594, 1),
    78780147: (GSWType.GSWF, 1362, 1),
    78780148: (GSWType.GSWF, 1363, 1),
    78780149: (GSWType.GSWF, 5534, 1),
    78780150: (GSWType.GSWF, 1364, 1),
    78780151: (GSWType.GSWF, 1365, 1),
    78780152: (GSWType.GSWF, 1366, 1),
    78780153: (GSWType.GSWF, 6055, 1),
    78780154: (GSWType.GSWF, 5597, 1),
    78780155: (GSWType.GSWF, 1367, 1),
    78780156: (GSWType.GSWF, 5535, 1),
    78780157: (GSWType.GSWF, 5536, 1),
    78780158: (GSWType.GSWF, 5537, 1),
    78780159: (GSWType.GSWF, 1368, 1),
    78780160: (GSWType.GSWF, 1802, 1),
    78780161: (GSWType.GSWF, 1785, 1),
    78780162: (GSWType.GSWF, 1784, 1),
    78780163: (GSWType.GSWF, 1786, 1),
    78780164: (GSWType.GSWF, 5600, 1),
    78780165: (GSWType.GSWF, 1787, 1),
    78780166: (GSWType.GSWF, 1791, 1),
    78780167: (GSWType.GSWF, 1790, 1),
    78780169: (GSWType.GSWF, 1775, 1),
    78780170: (GSWType.GSWF, 1796, 1),
    78780171: (GSWType.GSWF, 1774, 1),
    78780178: (GSWType.GSWF, 5601, 1),
    78780179: (GSWType.GSWF, 1628, 1),
    78780180: (GSWType.GSWF, 5602, 1),
    78780181: (GSWType.GSWF, 6101, 1),
    78780182: (GSWType.GSWF, 1780, 1),
    78780183: (GSWType.GSWF, 1778, 1),
    78780184: (GSWType.GSWF, 5598, 1),
    78780185: (GSWType.GSWF, 6077, 1),
    78780186: (GSWType.GSWF, 1800, 1),
    78780187: (GSWType.GSWF, 5599, 1),
    78780188: (GSWType.GSWF, 1799, 1),
    78780189: (GSWType.GSWF, 1797, 1),
    78780190: (GSWType.GSWF, 1798, 1),
    78780191: (GSWType.GSWF, 6102, 1),
    78780192: (GSWType.GSWF, 1501, 1),
    78780193: (GSWType.GSWF, 1502, 1),
    78780194: (GSWType.GSWF, 6002, 1),
    78780195: (GSWType.GSWF, 5603, 1),
    78780196: (GSWType.GSWF, 6006, 1),
    78780197: (GSWType.GSWF, 5538, 1),
    78780198: (GSWType.GSWF, 5604, 1),
    78780199: (GSWType.GSWF, 5605, 1),
    78780200: (GSWType.GSWF, 6009, 1),
    78780201: (GSWType.GSWF, 1503, 1),
    78780202: (GSWType.GSWF, 5539, 1),
    78780203: (GSWType.GSWF, 5606, 1),
    78780204: (GSWType.GSWF, 6011, 1),
    78780205: (GSWType.GSWF, 1504, 1),
    78780206: (GSWType.GSWF, 1494, 1),
    78780207: (GSWType.GSWF, 1505, 1),
    78780208: (GSWType.GSWF, 5607, 1),
    78780209: (GSWType.GSW, 1711, 8),
    78780210: (GSWType.GSWF, 1507, 1),
    78780211: (GSWType.GSWF, 1509, 1),
    78780212: (GSWType.GSWF, 1508, 1),
    78780213: (GSWType.GSWF, 5540, 1),
    78780214: (GSWType.GSWF, 1510, 1),
    78780215: (GSWType.GSWF, 2675, 1),
    78780216: (GSWType.GSWF, 2676, 1),
    78780217: (GSWType.GSWF, 2685, 1),
    78780218: (GSWType.GSWF, 2686, 1),
    78780219: (GSWType.GSWF, 2687, 1),
    78780220: (GSWType.GSWF, 2683, 1),
    78780221: (GSWType.GSWF, 2677, 1),
    78780222: (GSWType.GSWF, 5541, 1),
    78780223: (GSWType.GSWF, 5608, 1),
    78780224: (GSWType.GSWF, 5609, 1),
    78780225: (GSWType.GSWF, 5610, 1),
    78780226: (GSWType.GSWF, 2679, 1),
    78780227: (GSWType.GSWF, 6078, 1),
    78780228: (GSWType.GSWF, 5611, 1),
    78780229: (GSWType.GSWF, 2684, 1),
    78780230: (GSWType.GSWF, 2825, 1),
    78780231: (GSWType.GSWF, 2828, 1),
    78780232: (GSWType.GSW, 1713, 11),
    78780233: (GSWType.GSWF, 6103, 1),
    78780234: (GSWType.GSW, 1713, 5),
    78780235: (GSWType.GSWF, 5612, 1),
    78780236: (GSWType.GSWF, 5613, 1),
    78780237: (GSWType.GSWF, 2838, 1),
    78780238: (GSWType.GSWF, 2840, 1),
    78780239: (GSWType.GSWF, 2839, 1),
    78780240: (GSWType.GSWF, 2837, 1),
    78780241: (GSWType.GSWF, 5542, 1),
    78780242: (GSWType.GSWF, 2844, 1),
    78780243: (GSWType.GSWF, 6104, 1),
    78780244: (GSWType.GSWF, 2845, 1),
    78780245: (GSWType.GSWF, 5614, 1),
    78780252: (GSWType.GSWF, 2852, 1),
    78780253: (GSWType.GSWF, 2853, 1),
    78780254: (GSWType.GSWF, 5543, 1),
    78780255: (GSWType.GSWF, 6025, 1),
    78780256: (GSWType.GSWF, 2860, 1),
    78780257: (GSWType.GSWF, 5615, 1),
    78780258: (GSWType.GSWF, 2862, 1),
    78780259: (GSWType.GSWF, 5616, 1),
    78780260: (GSWType.GSWF, 2869, 1),
    78780261: (GSWType.GSWF, 5544, 1),
    78780262: (GSWType.GSWF, 2885, 1),
    78780263: (GSWType.GSWF, 5617, 1),
    78780264: (GSWType.GSWF, 2873, 1),
    78780265: (GSWType.GSWF, 5545, 1),
    78780266: (GSWType.GSWF, 2875, 1),
    78780267: (GSWType.GSWF, 2507, 1),
    78780269: (GSWType.GSWF, 6105, 1),
    78780270: (GSWType.GSWF, 2533, 1),
    78780272: (GSWType.GSWF, 2519, 1),
    78780275: (GSWType.GSWF, 5546, 1),
    78780276: (GSWType.GSWF, 5618, 1),
    78780277: (GSWType.GSWF, 5619, 1),
    78780278: (GSWType.GSWF, 5620, 1),
    78780279: (GSWType.GSWF, 5622, 1),
    78780280: (GSWType.GSWF, 5621, 1),
    78780281: (GSWType.GSWF, 6027, 1),
    78780282: (GSWType.GSWF, 6026, 1),
    78780285: (GSWType.GSWF, 5623, 1),
    78780286: (GSWType.GSWF, 6028, 1),
    78780287: (GSWType.GSW, 1703, 20),
    78780288: (GSWType.GSWF, 2520, 1),
    78780289: (GSWType.GSWF, 5624, 1),
    78780290: (GSWType.GSWF, 5625, 1),
    78780291: (GSWType.GSWF, 2523, 1),
    78780292: (GSWType.GSWF, 2521, 1),
    78780293: (GSWType.GSWF, 5547, 1),
    78780294: (GSWType.GSWF, 5626, 1),
    78780295: (GSWType.GSW, 1703, 14),
    78780296: (GSWType.GSWF, 2524, 1),
    78780297: (GSWType.GSWF, 6036, 1),
    78780298: (GSWType.GSWF, 6079, 1),
    78780299: (GSWType.GSWF, 5627, 1),
    78780300: (GSWType.GSWF, 1933, 1),
    78780301: (GSWType.GSWF, 6106, 1),
    78780302: (GSWType.GSWF, 5628, 1),
    78780303: (GSWType.GSWF, 5629, 1),
    78780304: (GSWType.GSWF, 6040, 1),
    78780305: (GSWType.GSWF, 6080, 1),
    78780306: (GSWType.GSWF, 1936, 1),
    78780307: (GSWType.GSWF, 1934, 1),
    78780308: (GSWType.GSWF, 1939, 1),
    78780309: (GSWType.GSWF, 1937, 1),
    78780311: (GSWType.GSWF, 1935, 1),
    78780314: (GSWType.GSWF, 5630, 1),
    78780318: (GSWType.GSWF, 6043, 1),
    78780319: (GSWType.GSWF, 2089, 1),
    78780320: (GSWType.GSWF, 2091, 1),
    78780321: (GSWType.GSWF, 2088, 1),
    78780322: (GSWType.GSWF, 2082, 1),
    78780323: (GSWType.GSWF, 2087, 1),
    78780324: (GSWType.GSWF, 6041, 1),
    78780325: (GSWType.GSWF, 5631, 1),
    78780326: (GSWType.GSWF, 5632, 1),
    78780327: (GSWType.GSWF, 2083, 1),
    78780328: (GSWType.GSWF, 2084, 1),
    78780329: (GSWType.GSWF, 2086, 1),
    78780330: (GSWType.GSWF, 2085, 1),
    78780331: (GSWType.GSWF, 5548, 1),
    78780332: (GSWType.GSWF, 2090, 1),
    78780333: (GSWType.GSWF, 5633, 1),
    78780434: (GSWType.GSWF, 2242, 1),
    78780435: (GSWType.GSWF, 6046, 1),
    78780436: (GSWType.GSWF, 6107, 1),
    78780437: (GSWType.GSW, 1715, 8),
    78780438: (GSWType.GSWF, 2235, 1),
    78780439: (GSWType.GSWF, 2237, 1),
    78780440: (GSWType.GSWF, 5549, 1),
    78780441: (GSWType.GSWF, 5635, 1),
    78780442: (GSWType.GSWF, 2238, 1),
    78780443: (GSWType.GSWF, 5636, 1),
    78780444: (GSWType.GSW, 1716, 1),
    78780445: (GSWType.GSWF, 2240, 1),
    78780446: (GSWType.GSWF, 2239, 1),
    78780447: (GSWType.GSWF, 5637, 1),
    78780448: (GSWType.GSWF, 2230, 1),
    78780449: (GSWType.GSWF, 6049, 1),
    78780450: (GSWType.GSWF, 5550, 1),
    78780451: (GSWType.GSWF, 2241, 1),
    78780452: (GSWType.GSWF, 5551, 1),
    78780453: (GSWType.GSWF, 5638, 1),
    78780454: (GSWType.GSWF, 6082, 1),
    78780455: (GSWType.GSWF, 6083, 1),
    78780456: (GSWType.GSWF, 6084, 1),
    78780457: (GSWType.GSWF, 6085, 1),
    78780458: (GSWType.GSWF, 6086, 1),
    78780459: (GSWType.GSWF, 6087, 1),
    78780460: (GSWType.GSWF, 6088, 1),
    78780461: (GSWType.GSW, 1719, 4),
    78780467: (GSWType.GSWF, 5639, 1),
    78780468: (GSWType.GSWF, 5640, 1),
    78780470: (GSWType.GSWF, 3154, 1),
    78780471: (GSWType.GSWF, 3150, 1),
    78780472: (GSWType.GSWF, 3146, 1),
    78780473: (GSWType.GSWF, 3152, 1),
    78780474: (GSWType.GSWF, 5641, 1),
    78780475: (GSWType.GSWF, 3134, 1),
    78780476: (GSWType.GSWF, 3133, 1),
    78780477: (GSWType.GSWF, 3156, 1),
    78780478: (GSWType.GSWF, 3153, 1),
    78780479: (GSWType.GSWF, 3155, 1),
    78780480: (GSWType.GSWF, 5552, 1),
    78780481: (GSWType.GSWF, 5642, 1),
    78780482: (GSWType.GSWF, 3147, 1),
    78780483: (GSWType.GSWF, 6090, 1),
    78780484: (GSWType.GSWF, 6091, 1),
    78780485: (GSWType.GSWF, 3148, 1),
    78780486: (GSWType.GSWF, 3158, 1),
    78780487: (GSWType.GSWF, 5553, 1),
    78780488: (GSWType.GSWF, 6081, 1),
    78780489: (GSWType.GSWF, 6108, 1),
    78780490: (GSWType.GSWF, 3157, 1),
    78780491: (GSWType.GSWF, 5643, 1),
    78780492: (GSWType.GSWF, 3143, 1),
    78780493: (GSWType.GSWF, 2990, 1),
    78780494: (GSWType.GSWF, 2975, 1),
    78780495: (GSWType.GSWF, 5554, 1),
    78780496: (GSWType.GSWF, 5644, 1),
    78780497: (GSWType.GSWF, 5645, 1),
    78780498: (GSWType.GSWF, 2977, 1),
    78780499: (GSWType.GSWF, 5555, 1),
    78780500: (GSWType.GSWF, 5646, 1),
    78780501: (GSWType.GSWF, 2993, 1),
    78780502: (GSWType.GSWF, 2986, 1),
    78780503: (GSWType.GSWF, 5556, 1),
    78780504: (GSWType.GSWF, 5647, 1),
    78780505: (GSWType.GSWF, 2987, 1),
    78780506: (GSWType.GSWF, 6052, 1),
    78780507: (GSWType.GSWF, 2985, 1),
    78780508: (GSWType.GSWF, 2994, 1),
    78780509: (GSWType.GSWF, 5557, 1),
    78780510: (GSWType.GSWF, 5558, 1),
    78780511: (GSWType.GSW, 1717, 10),
    78780512: (GSWType.GSW, 1706, 13),
    78780513: (GSWType.GSWF, 5648, 1),
    78780514: (GSWType.GSW, 1706, 25),
    78780515: (GSWType.GSWF, 6092, 1),
    78780516: (GSWType.GSW, 1706, 20),
    78780517: (GSWType.GSW, 1706, 29),
    78780518: (GSWType.GSWF, 3462, 1),
    78780519: (GSWType.GSW, 1706, 7),
    78780520: (GSWType.GSW, 1706, 29),
    78780521: (GSWType.GSW, 1706, 29),
    78780522: (GSWType.GSWF, 5559, 1),
    78780523: (GSWType.GSWF, 5649, 1),
    78780527: (GSWType.GSWF, 5650, 1),
    78780528: (GSWType.GSWF, 5651, 1),
    78780532: (GSWType.GSW, 1706, 21),
    78780533: (GSWType.GSWF, 5560, 1),
    78780534: (GSWType.GSWF, 5652, 1),
    78780535: (GSWType.GSWF, 6116, 1),
    78780536: (GSWType.GSWF, 6118, 1),
    78780537: (GSWType.GSWF, 3745, 1),
    78780538: (GSWType.GSWF, 5653, 1),
    78780539: (GSWType.GSWF, 6059, 1),
    78780540: (GSWType.GSWF, 3746, 1),
    78780541: (GSWType.GSWF, 5561, 1),
    78780542: (GSWType.GSWF, 3754, 1),
    78780543: (GSWType.GSWF, 3744, 1),
    78780544: (GSWType.GSWF, 3747, 1),
    78780545: (GSWType.GSWF, 6065, 1),
    78780546: (GSWType.GSWF, 6064, 1),
    78780547: (GSWType.GSWF, 5562, 1),
    78780548: (GSWType.GSWF, 6115, 1),
    78780549: (GSWType.GSWF, 3276, 1),
    78780550: (GSWType.GSWF, 5654, 1),
    78780551: (GSWType.GSWF, 5656, 1),
    78780552: (GSWType.GSWF, 5655, 1),
    78780553: (GSWType.GSWF, 5563, 1),
    78780554: (GSWType.GSW, 1706, 42),
    78780555: (GSWType.GSWF, 3277, 1),
    78780556: (GSWType.GSWF, 5564, 1),
    78780557: (GSWType.GSWF, 6109, 1),
    78780558: (GSWType.GSWF, 3279, 1),
    78780559: (GSWType.GSWF, 6110, 1),
    78780560: (GSWType.GSWF, 5657, 1),
    78780561: (GSWType.GSWF, 3891, 1),
    78780562: (GSWType.GSWF, 5658, 1),
    78780563: (GSWType.GSWF, 5659, 1),
    78780565: (GSWType.GSWF, 3892, 1),
    78780568: (GSWType.GSWF, 5565, 1),
    78780570: (GSWType.GSWF, 6111, 1),
    78780571: (GSWType.GSWF, 5661, 1),
    78780572: (GSWType.GSWF, 5660, 1),
    78780575: (GSWType.GSWF, 5566, 1),
    78780576: (GSWType.GSWF, 5662, 1),
    78780577: (GSWType.GSWF, 3887, 1),
    78780578: (GSWType.GSWF, 5663, 1),
    78780579: (GSWType.GSWF, 4035, 1),
    78780580: (GSWType.GSWF, 4037, 1),
    78780581: (GSWType.GSWF, 5664, 1),
    78780582: (GSWType.GSWF, 4038, 1),
    78780583: (GSWType.GSWF, 4039, 1),
    78780584: (GSWType.GSWF, 4176, 1),
    78780585: (GSWType.GSWF, 4211, 1),
    78780586: (GSWType.GSWF, 6093, 1),
    78780587: (GSWType.GSWF, 6094, 1),
    78780588: (GSWType.GSWF, 6095, 1),
    78780589: (GSWType.GSWF, 6096, 1),
    78780590: (GSWType.GSWF, 6097, 1),
    78780591: (GSWType.GSWF, 6098, 1),
    78780592: (GSWType.GSWF, 4198, 1),
    78780593: (GSWType.GSWF, 4216, 1),
    78780594: (GSWType.GSWF, 5665, 1),
    78780595: (GSWType.GSWF, 6069, 1),
    78780596: (GSWType.GSWF, 4182, 1),
    78780597: (GSWType.GSWF, 4212, 1),
    78780598: (GSWType.GSWF, 4194, 1),
    78780599: (GSWType.GSWF, 5666, 1),
    78780600: (GSWType.GSWF, 4180, 1),
    78780601: (GSWType.GSWF, 4183, 1),
    78780602: (GSWType.GSWF, 4181, 1),
    78780603: (GSWType.GSWF, 4215, 1),
    78780604: (GSWType.GSW, 1707, 16),
    78780605: (GSWType.GSWF, 4383, 1),
    78780606: (GSWType.GSWF, 4371, 1),
    78780607: (GSWType.GSWF, 4375, 1),
    78780608: (GSWType.GSWF, 4384, 1),
    78780609: (GSWType.GSWF, 6071, 1),
    78780610: (GSWType.GSWF, 4372, 1),
    78780611: (GSWType.GSWF, 4373, 1),
    78780612: (GSWType.GSWF, 4374, 1),
    78780613: (GSWType.GSWF, 4376, 1),
    78780614: (GSWType.GSWF, 4362, 1),
    78780615: (GSWType.GSWF, 4363, 1),
    78780616: (GSWType.GSWF, 4364, 1),
    78780617: (GSWType.GSWF, 4365, 1),
    78780618: (GSWType.GSWF, 4366, 1),
    78780619: (GSWType.GSWF, 4367, 1),
    78780620: (GSWType.GSWF, 4368, 1),
    78780621: (GSWType.GSWF, 4369, 1),
    78780622: (GSWType.GSWF, 4387, 1),
    78780623: (GSWType.GSWF, 4389, 1),
    78780624: (GSWType.GSWF, 4388, 1),
    78780625: (GSWType.GSWF, 4378, 1),
    78780626: (GSWType.GSWF, 6073, 1),
    78780627: (GSWType.GSWF, 4377, 1),
    78780628: (GSWType.GSWF, 4390, 1),
    78780629: (GSWType.GSWF, 4370, 1),
    78780630: (GSWType.GSWF, 4391, 1),
    78780631: (GSWType.GSWF, 4379, 1),
    78780632: (GSWType.GSWF, 4392, 1),
    78780633: (GSWType.GSWF, 4386, 1),
    78780634: (GSWType.GSWF, 4361, 1),
    78780635: (GSWType.GSWF, 4385, 1),
    78780636: (GSWType.GSWF, 4394, 1),
    78780637: (GSWType.GSWF, 4393, 1),
    78780638: (GSWType.GSWF, 5075, 1),
    78780639: (GSWType.GSWF, 5076, 1),
    78780640: (GSWType.GSWF, 5077, 1),
    78780641: (GSWType.GSWF, 5078, 1),
    78780642: (GSWType.GSWF, 5079, 1),
    78780643: (GSWType.GSWF, 5080, 1),
    78780644: (GSWType.GSWF, 5081, 1),
    78780645: (GSWType.GSWF, 5082, 1),
    78780646: (GSWType.GSWF, 5083, 1),
    78780647: (GSWType.GSWF, 5084, 1),
    78780702: (GSWType.GSWF, 4214, 1),
    78780704: (GSWType.GSWF, 5596, 1),
    78780705: (GSWType.GSWF, 1355, 1),
    78780706: (GSWType.GSWF, 5567, 1),
    78780707: (GSWType.GSWF, 5526, 1),
    78780708: (GSWType.GSWF, 5529, 1),
    78780800: (GSWType.GSWF, 1801, 1),
    78780801: (GSWType.GSWF, 1794, 1),
    78780802: (GSWType.GSWF, 1795, 1),
    78780803: (GSWType.GSWF, 1806, 1),
    78780805: (GSWType.GSWF, 5634, 1),
    78780806: (GSWType.GSWF, 6089, 1),
    78780807: (GSWType.GSWF, 4036, 1),
    #Shops
    78780030: (GSWType.GSWF, 6200, 1),
    78780023: (GSWType.GSWF, 6201, 1),
    78780053: (GSWType.GSWF, 6202, 1),
    78780003: (GSWType.GSWF, 6203, 1),
    78780041: (GSWType.GSWF, 6204, 1),
    78780019: (GSWType.GSWF, 6205, 1),
    78780096: (GSWType.GSWF, 6206, 1),
    78780102: (GSWType.GSWF, 6207, 1),
    78780073: (GSWType.GSWF, 6208, 1),
    78780080: (GSWType.GSWF, 6209, 1),
    78780072: (GSWType.GSWF, 6210, 1),
    78780098: (GSWType.GSWF, 6211, 1),
    78780125: (GSWType.GSWF, 6212, 1),
    78780112: (GSWType.GSWF, 6213, 1),
    78780131: (GSWType.GSWF, 6214, 1),
    78780118: (GSWType.GSWF, 6215, 1),
    78780110: (GSWType.GSWF, 6216, 1),
    78780111: (GSWType.GSWF, 6217, 1),
    78780173: (GSWType.GSWF, 6218, 1),
    78780177: (GSWType.GSWF, 6219, 1),
    78780172: (GSWType.GSWF, 6220, 1),
    78780175: (GSWType.GSWF, 6221, 1),
    78780174: (GSWType.GSWF, 6222, 1),
    78780176: (GSWType.GSWF, 6223, 1),
    78780247: (GSWType.GSWF, 6224, 1),
    78780248: (GSWType.GSWF, 6225, 1),
    78780251: (GSWType.GSWF, 6226, 1),
    78780249: (GSWType.GSWF, 6227, 1),
    78780246: (GSWType.GSWF, 6228, 1),
    78780250: (GSWType.GSWF, 6229, 1),
    78780268: (GSWType.GSWF, 6230, 1),
    78780284: (GSWType.GSWF, 6231, 1),
    78780273: (GSWType.GSWF, 6232, 1),
    78780274: (GSWType.GSWF, 6233, 1),
    78780271: (GSWType.GSWF, 6234, 1),
    78780283: (GSWType.GSWF, 6235, 1),
    78780317: (GSWType.GSWF, 6236, 1),
    78780313: (GSWType.GSWF, 6237, 1),
    78780315: (GSWType.GSWF, 6238, 1),
    78780312: (GSWType.GSWF, 6239, 1),
    78780316: (GSWType.GSWF, 6240, 1),
    78780310: (GSWType.GSWF, 6241, 1),
    78780465: (GSWType.GSWF, 6242, 1),
    78780462: (GSWType.GSWF, 6243, 1),
    78780466: (GSWType.GSWF, 6244, 1),
    78780463: (GSWType.GSWF, 6245, 1),
    78780464: (GSWType.GSWF, 6246, 1),
    78780469: (GSWType.GSWF, 6247, 1),
    78780531: (GSWType.GSWF, 6248, 1),
    78780526: (GSWType.GSWF, 6249, 1),
    78780524: (GSWType.GSWF, 6250, 1),
    78780530: (GSWType.GSWF, 6251, 1),
    78780525: (GSWType.GSWF, 6252, 1),
    78780529: (GSWType.GSWF, 6253, 1),
    78780569: (GSWType.GSWF, 6254, 1),
    78780564: (GSWType.GSWF, 6255, 1),
    78780567: (GSWType.GSWF, 6256, 1),
    78780573: (GSWType.GSWF, 6257, 1),
    78780566: (GSWType.GSWF, 6258, 1),
    78780574: (GSWType.GSWF, 6259, 1),
    # Tattles
    78780850: (GSWType.GSWF, 4475, 1),   # Tattle: Goomba
    78780851: (GSWType.GSWF, 4476, 1),   # Tattle: Paragoomba
    78780852: (GSWType.GSWF, 4477, 1),   # Tattle: Spiky Goomba
    78780853: (GSWType.GSWF, 4478, 1),   # Tattle: Hyper Goomba
    78780854: (GSWType.GSWF, 4479, 1),   # Tattle: Hyper Paragoomba
    78780855: (GSWType.GSWF, 4480, 1),   # Tattle: Hyper Spiky Goomba
    78780856: (GSWType.GSWF, 4481, 1),   # Tattle: Gloomba
    78780857: (GSWType.GSWF, 4482, 1),   # Tattle: Paragloomba
    78780858: (GSWType.GSWF, 4483, 1),   # Tattle: Spiky Gloomba
    78780859: (GSWType.GSWF, 4484, 1),   # Tattle: Koopa Troopa
    78780860: (GSWType.GSWF, 4485, 1),   # Tattle: Paratroopa
    78780861: (GSWType.GSWF, 4486, 1),   # Tattle: KP Koopa
    78780862: (GSWType.GSWF, 4487, 1),   # Tattle: KP Paratroopa
    78780863: (GSWType.GSWF, 4488, 1),   # Tattle: Shady Koopa
    78780864: (GSWType.GSWF, 4489, 1),   # Tattle: Shady Paratroopa
    78780865: (GSWType.GSWF, 4490, 1),   # Tattle: Dark Koopa
    78780866: (GSWType.GSWF, 4491, 1),   # Tattle: Dark Paratroopa
    78780867: (GSWType.GSWF, 4492, 1),   # Tattle: Koopatrol
    78780868: (GSWType.GSWF, 4493, 1),   # Tattle: Dark Koopatrol
    78780869: (GSWType.GSWF, 4494, 1),   # Tattle: Dull Bones
    78780870: (GSWType.GSWF, 4495, 1),   # Tattle: Red Bones
    78780871: (GSWType.GSWF, 4496, 1),   # Tattle: Dry Bones
    78780872: (GSWType.GSWF, 4497, 1),   # Tattle: Dark Bones
    78780873: (GSWType.GSWF, 4498, 1),   # Tattle: Hammer Bro
    78780874: (GSWType.GSWF, 4499, 1),   # Tattle: Boomerang Bro
    78780875: (GSWType.GSWF, 4500, 1),   # Tattle: Fire Bro
    78780876: (GSWType.GSWF, 4501, 1),   # Tattle: Lakitu
    78780877: (GSWType.GSWF, 4502, 1),   # Tattle: Dark Lakitu
    78780878: (GSWType.GSWF, 4503, 1),   # Tattle: Spiny
    78780879: (GSWType.GSWF, 4504, 1),   # Tattle: Sky-Blue Spiny
    78780880: (GSWType.GSWF, 4505, 1),   # Tattle: Buzzy Beetle
    78780881: (GSWType.GSWF, 4506, 1),   # Tattle: Spike Top
    78780882: (GSWType.GSWF, 4507, 1),   # Tattle: Parabuzzy
    78780883: (GSWType.GSWF, 4508, 1),   # Tattle: Spiky Parabuzzy
    78780884: (GSWType.GSWF, 4509, 1),   # Tattle: Red Spike Top
    78780885: (GSWType.GSWF, 4510, 1),   # Tattle: Magikoopa
    78780886: (GSWType.GSWF, 4511, 1),   # Tattle: Red Magikoopa
    78780887: (GSWType.GSWF, 4512, 1),   # Tattle: White Magikoopa
    78780888: (GSWType.GSWF, 4513, 1),   # Tattle: Green Magikoopa
    78780889: (GSWType.GSWF, 4514, 1),   # Tattle: Kammy Koopa
    78780890: (GSWType.GSWF, 4515, 1),   # Tattle: Bowser (Glitz Pit)
    78780891: (GSWType.GSWF, 4516, 1),   # Tattle: Gus
    78780892: (GSWType.GSWF, 4517, 1),   # Tattle: Dark Craw
    78780893: (GSWType.GSWF, 4518, 1),   # Tattle: Bandit
    78780894: (GSWType.GSWF, 4519, 1),   # Tattle: Big Bandit
    78780895: (GSWType.GSWF, 4520, 1),   # Tattle: Badge Bandit
    78780896: (GSWType.GSWF, 4521, 1),   # Tattle: Spinia
    78780897: (GSWType.GSWF, 4522, 1),   # Tattle: Spania
    78780898: (GSWType.GSWF, 4523, 1),   # Tattle: Spunia
    78780899: (GSWType.GSWF, 4524, 1),   # Tattle: Fuzzy
    78780900: (GSWType.GSWF, 4525, 1),   # Tattle: Gold Fuzzy
    78780901: (GSWType.GSWF, 4526, 1),   # Tattle: Green Fuzzy
    78780902: (GSWType.GSWF, 4527, 1),   # Tattle: Flower Fuzzy
    78780903: (GSWType.GSWF, 4528, 1),   # Tattle: Pokey
    78780904: (GSWType.GSWF, 4529, 1),   # Tattle: Poison Pokey
    78780905: (GSWType.GSWF, 4530, 1),   # Tattle: Pale Piranha
    78780906: (GSWType.GSWF, 4531, 1),   # Tattle: Putrid Piranha
    78780907: (GSWType.GSWF, 4532, 1),   # Tattle: Frost Piranha
    78780908: (GSWType.GSWF, 4533, 1),   # Tattle: Piranha Plant
    78780909: (GSWType.GSWF, 4534, 1),   # Tattle: Crazee Dayzee
    78780910: (GSWType.GSWF, 4535, 1),   # Tattle: Amazy Dayzee
    78780911: (GSWType.GSWF, 4536, 1),   # Tattle: Pider
    78780912: (GSWType.GSWF, 4537, 1),   # Tattle: Arantula
    78780913: (GSWType.GSWF, 4538, 1),   # Tattle: Swooper
    78780914: (GSWType.GSWF, 4539, 1),   # Tattle: Swoopula
    78780915: (GSWType.GSWF, 4540, 1),   # Tattle: Swampire
    78780916: (GSWType.GSWF, 4541, 1),   # Tattle: Dark Puff
    78780917: (GSWType.GSWF, 4542, 1),   # Tattle: Ruff Puff
    78780918: (GSWType.GSWF, 4543, 1),   # Tattle: Ice Puff
    78780919: (GSWType.GSWF, 4544, 1),   # Tattle: Poison Puff
    78780920: (GSWType.GSWF, 4545, 1),   # Tattle: Boo
    78780921: (GSWType.GSWF, 4546, 1),   # Tattle: Atomic Boo
    78780922: (GSWType.GSWF, 4547, 1),   # Tattle: Dark Boo
    78780923: (GSWType.GSWF, 4548, 1),   # Tattle: Ember
    78780924: (GSWType.GSWF, 4549, 1),   # Tattle: Lava Bubble
    78780925: (GSWType.GSWF, 4550, 1),   # Tattle: Phantom Ember
    78780926: (GSWType.GSWF, 4551, 1),   # Tattle: Bald Cleft
    78780927: (GSWType.GSWF, 4552, 1),   # Tattle: Hyper Bald Cleft
    78780928: (GSWType.GSWF, 4553, 1),   # Tattle: Cleft
    78780929: (GSWType.GSWF, 4554, 1),   # Tattle: Iron Cleft
    78780931: (GSWType.GSWF, 4556, 1),   # Tattle: Hyper Cleft
    78780932: (GSWType.GSWF, 4557, 1),   # Tattle: Moon Cleft
    78780933: (GSWType.GSWF, 4558, 1),   # Tattle: Bristle
    78780934: (GSWType.GSWF, 4559, 1),   # Tattle: Dark Bristle
    78780935: (GSWType.GSWF, 4560, 1),   # Tattle: Bob-omb
    78780936: (GSWType.GSWF, 4561, 1),   # Tattle: Bulky Bob-omb
    78780937: (GSWType.GSWF, 4562, 1),   # Tattle: Bob-ulk
    78780938: (GSWType.GSWF, 4563, 1),   # Tattle: Chain-Chomp
    78780939: (GSWType.GSWF, 4564, 1),   # Tattle: Red Chomp
    78780940: (GSWType.GSWF, 4565, 1),   # Tattle: Bill Blaster
    78780941: (GSWType.GSWF, 4566, 1),   # Tattle: Bullet Bill
    78780942: (GSWType.GSWF, 4567, 1),   # Tattle: B. Bill Blaster
    78780943: (GSWType.GSWF, 4568, 1),   # Tattle: Bombshell Bill
    78780944: (GSWType.GSWF, 4569, 1),   # Tattle: Dark Wizzerd
    78780945: (GSWType.GSWF, 4570, 1),   # Tattle: Wizzerd
    78780946: (GSWType.GSWF, 4571, 1),   # Tattle: Elite Wizzerd
    78780947: (GSWType.GSWF, 4572, 1),   # Tattle: Blooper
    78780948: (GSWType.GSWF, 4573, 1),   # Tattle: Hooktail
    78780949: (GSWType.GSWF, 4574, 1),   # Tattle: Gloomtail
    78780950: (GSWType.GSWF, 4575, 1),   # Tattle: Bonetail
    78780951: (GSWType.GSWF, 4576, 1),   # Tattle: Rawk Hawk
    78780952: (GSWType.GSWF, 4577, 1),   # Tattle: Macho Grubba
    78780953: (GSWType.GSWF, 4578, 1),   # Tattle: Doopliss
    78780954: (GSWType.GSWF, 4579, 1),   # Tattle: Cortez
    78780955: (GSWType.GSWF, 4580, 1),   # Tattle: Smorg
    78780956: (GSWType.GSWF, 4581, 1),   # Tattle: X-Naut
    78780957: (GSWType.GSWF, 4582, 1),   # Tattle: X-Naut PhD
    78780958: (GSWType.GSWF, 4583, 1),   # Tattle: Elite X-Naut
    78780959: (GSWType.GSWF, 4584, 1),   # Tattle: Yux
    78780960: (GSWType.GSWF, 4585, 1),   # Tattle: Mini-Yux
    78780961: (GSWType.GSWF, 4586, 1),   # Tattle: Z-Yux
    78780962: (GSWType.GSWF, 4587, 1),   # Tattle: Mini-Z-Yux
    78780963: (GSWType.GSWF, 4588, 1),   # Tattle: X-Yux
    78780964: (GSWType.GSWF, 4589, 1),   # Tattle: Mini-X-Yux
    78780965: (GSWType.GSWF, 4590, 1),   # Tattle: Grodus X
    78780966: (GSWType.GSWF, 4591, 1),   # Tattle: Magnus von Grapple
    78780967: (GSWType.GSWF, 4592, 1),   # Tattle: Magnus von Grapple 2.0
    78780968: (GSWType.GSWF, 4593, 1),   # Tattle: Lord Crump
    78780969: (GSWType.GSWF, 4594, 1),   # Tattle: Sir Grodus
    78780970: (GSWType.GSWF, 4595, 1),   # Tattle: Beldam
    78780971: (GSWType.GSWF, 4596, 1),   # Tattle: Marilyn
    78780972: (GSWType.GSWF, 4597, 1),   # Tattle: Vivian
    78780973: (GSWType.GSWF, 4598, 1),   # Tattle: Shadow Queen
    78780974: (GSWType.GSW, 1726, 1),   # Dazzle Item 1
    78780975: (GSWType.GSW, 1726, 2),   # Dazzle Item 2
    78780976: (GSWType.GSW, 1726, 3),   # Dazzle Item 3
    78780977: (GSWType.GSW, 1726, 4),   # Dazzle Item 4
    78780978: (GSWType.GSW, 1726, 5),   # Dazzle Item 5
    78780979: (GSWType.GSW, 1726, 6),   # Dazzle Item 6
    78780980: (GSWType.GSW, 1726, 7),   # Dazzle Item 7
    78780981: (GSWType.GSW, 1726, 8),   # Dazzle Item 8
    78780982: (GSWType.GSW, 1726, 9),   # Dazzle Item 9
    78780983: (GSWType.GSW, 1726, 10),   # Dazzle Item 10
    78780984: (GSWType.GSW, 1726, 11),   # Dazzle Item 11
    78780985: (GSWType.GSW, 1726, 12),   # Dazzle Item 12
    78780986: (GSWType.GSW, 1726, 13),   # Dazzle Item 13
    78780987: (GSWType.GSW, 1726, 14),   # Dazzle Item 14
    78780988: (GSWType.GSW, 1726, 15),   # Dazzle Item 15
}

item_prices = {
    77772000: 10,  # 10 Coins
    77772002: 50,  # All or Nothing - 50 buy price
    77772220: 50,  # Attack FX B - 50 buy price
    77772003: 50,  # Attack FX G - 50 buy price
    77772004: 50,  # Attack FX P - 50 buy price
    77772005: 50,  # Attack FX R - 50 buy price
    77772006: 50,  # Attack FX Y - 50 buy price
    77772007: 30,  # Autograph
    77772008: 30,  # Black Key (Plane)
    77772009: 30,  # Black Key (Paper)
    77772010: 30,  # Black Key (Tube)
    77772011: 30,  # Black Key (Boat)
    77772012: 30,  # Blanket
    77772013: 30,  # Blimp Ticket
    77772014: 30,  # Blue Key
    77772015: 30,  # Boat Mode
    77772016: 30,  # Bobbery
    77772017: 20,  # Boo's Sheet
    77772018: 30,  # Briefcase
    77772019: 80,  # Bump Attack - 80 buy price
    77772020: 5,  # Cake Mix
    77772021: 30,  # Card Key 1
    77772022: 30,  # Card Key 2
    77772023: 30,  # Card Key 3
    77772024: 30,  # Card Key 4
    77772025: 30,  # Castle Key
    77772026: 30,  # Champ's Belt
    77772027: 30,  # Charge - 30 buy price
    77772028: 40,  # Charge P - 40 buy price
    77772029: 40,  # Chill Out - 40 buy price
    77772221: 30,  # Choco Cake
    77772030: 30,  # Chuckola Cola
    77772031: 50,  # Close Call - 50 buy price
    77772032: 50,  # Close Call P - 50 buy price
    77772033: 30,  # Coconut
    77772034: 30,  # Cog
    77772036: 30,  # Contact Lens
    77772037: 30,  # Cookbook
    77772223: 15,  # Couple's Cake
    77772038: 4,  # Courage Shell
    77772039: 30,  # Crystal Star
    77772040: 80,  # Damage Dodge - 80 buy price
    77772041: 80,  # Damage Dodge P - 80 buy price
    77772042: 80,  # Defend Plus - 80 buy price
    77772043: 80,  # Defend Plus P - 80 buy price
    77772044: 30,  # Diamond Star
    77772045: 8,  # Dizzy Dial
    77772046: 50,  # Double Dip - 50 buy price
    77772047: 50,  # Double Dip P - 50 buy price
    77772048: 20,  # Double Pain - 20 buy price
    77772224: 8,  # Dried Bouquet
    77772049: 1,  # Dried Shroom
    77772051: 10,  # Earth Quake
    77772052: 30,  # Elevator Key (Station)
    77772053: 30,  # Elevator Key 1
    77772054: 30,  # Elevator Key 2
    77772055: 30,  # Emerald Star
    77772056: 80,  # Feeling Fine - 80 buy price
    77772057: 80,  # Feeling Fine P - 80 buy price
    77772058: 50,  # Fire Drive - 50 buy price
    77772059: 5,  # Fire Flower
    77772060: 50,  # First Attack - 50 buy price
    77772061: 50,  # Flower Finder - 50 buy price
    77772062: 60,  # Flower Saver - 60 buy price
    77772063: 60,  # Flower Saver P - 60 buy price
    77772064: 30,  # Flurrie
    77772065: 50,  # FP Drain - 50 buy price
    77772066: 80,  # FP Plus - 80 buy price
    77772067: 30,  # Fresh Pasta
    77772068: 5,  # Fright Mask
    77772069: 30,  # Galley Pot
    77772070: 30,  # Garnet Star
    77772071: 30,  # Gate Handle
    77772072: 110,  # Gold Bar
    77772073: 310,  # Gold Bar x3
    77772074: 30,  # Gold Ring
    77772075: 30,  # Gold Star
    77772076: 30,  # Goldbob Guide
    77772077: 5,  # Golden Leaf
    77772078: 30,  # Goombella
    77772079: 10,  # Gradual Syrup
    77772080: 30,  # Grotto Key
    77772081: 40,  # Hammer Throw - 40 buy price
    77772082: 80,  # Hammerman - 80 buy price
    77772083: 80,  # Happy Flower - 80 buy price
    77772084: 80,  # Happy Heart - 80 buy price
    77772085: 80,  # Happy Heart P - 80 buy price
    77772086: 50,  # Head Rattle - 50 buy price
    77772087: 50,  # Heart Finder - 50 buy price
    77772225: 15,  # Honey Shroom
    77772088: 5,  # Honey Syrup
    77772089: 4,  # Horsetail
    77772090: 8,  # Hot Dog
    77772226: 8,  # Hot Sauce
    77772091: 10,  # HP Drain
    77772092: 50,  # HP Drain (Badge) - 50 buy price
    77772093: 50,  # HP Drain P - 50 buy price
    77772094: 80,  # HP Plus - 80 buy price
    77772095: 80,  # HP Plus P - 80 buy price
    77772096: 40,  # Ice Power - 40 buy price
    77772097: 40,  # Ice Smash - 40 buy price
    77772098: 10,  # Ice Storm
    77772099: 8,  # Inn Coupon
    77772100: 50,  # Item Hog - 50 buy price
    77772101: 50,  # Jammin' Jelly
    77772102: 80,  # Jumpman - 80 buy price
    77772103: 5,  # Keel Mango
    77772104: 30,  # Koops
    77772105: 80,  # L Emblem - 80 buy price
    77772106: 30,  # Last Stand - 30 buy price
    77772107: 30,  # Last Stand P - 30 buy price
    77772108: 50,  # Life Shroom
    77772110: 80,  # Lucky Day - 80 buy price
    77772111: 50,  # Lucky Start - 50 buy price
    77772112: 10,  # Maple Syrup
    77772113: 30,  # Mega Rush - 30 buy price
    77772114: 30,  # Mega Rush P - 30 buy price
    77772227: 40,  # Meteor Meal
    77772115: 10,  # Mini Mr. Mini
    77772116: 90,  # Money Money - 90 buy price
    77772117: 30,  # Moon Stone
    77772118: 8,  # Mr. Softener
    77772222: 20,  # Ms. Mowz
    77772119: 40,  # Multibounce - 40 buy price
    77772120: 5,  # Mushroom
    77772121: 3,  # Mystery
    77772122: 4,  # Mystic Egg
    77772123: 30,  # Necklace
    77772124: 30,  # Old Letter
    77772125: 12,  # Omelette Meal
    77772126: 80,  # P-Down, D-Up - 80 buy price
    77772127: 50,  # P-Down, D-Up P - 50 buy price
    77772128: 50,  # P-Up, D-Down - 50 buy price
    77772129: 60,  # P-Up, D-Down P - 60 buy price
    77772130: 30,  # Palace Key
    77772131: 30,  # Palace Key (Tower)
    77772132: 30,  # Paper Mode
    77772133: 5,  # Peachy Peach
    77772134: 50,  # Peekaboo - 50 buy price
    77772135: 40,  # Piercing Blow - 40 buy price
    77772136: 50,  # Pity Flower - 50 buy price
    77772137: 30,  # Plane Mode
    77772138: 5,  # Point Swap
    77772139: 5,  # POW Block
    77772140: 50,  # Power Bounce - 50 buy price
    77772141: 30,  # Power Jump - 30 buy price
    77772142: 100,  # Power Plus - 100 buy price
    77772143: 100,  # Power Plus P - 100 buy price
    77772144: 15,  # Power Punch
    77772145: 30,  # Power Rush - 30 buy price
    77772146: 30,  # Power Rush P - 30 buy price
    77772147: 30,  # Power Smash - 30 buy price
    77772148: 80,  # Pretty Lucky - 80 buy price
    77772149: 80,  # Pretty Lucky P - 80 buy price
    77772150: 30,  # Puni Orb
    77772151: 50,  # Quake Hammer - 50 buy price
    77772152: 80,  # Quick Change - 80 buy price
    77772153: 30,  # Ragged Diary
    77772154: 30,  # Red Key
    77772155: 30,  # Refund - 30 buy price
    77772156: 15,  # Repel Cape
    77772157: 170, # Return Postage - 170 buy price
    77772158: 30,  # Ruby Star
    77772159: 15,  # Ruin Powder
    77772160: 30,  # Sapphire Star
    77772161: 30,  # Shell Earrings
    77772162: 15,  # Shine Sprite
    77772164: 30,  # Shooting Star
    77772165: 30,  # Shop Key
    77772166: 40,  # Shrink Stomp - 40 buy price
    77772167: 30,  # Simplifier - 30 buy price
    77772168: 30,  # Skull Gem
    77772169: 8,   # Sleepy Sheep
    77772219: 50,  # Sleepy Stomp
    77772170: 10,  # Slow Go - 10 buy price
    77772171: 15,  # Slow Shroom
    77772228: 15,  # Snow Bunny
    77772172: 40,  # Soft Stomp - 40 buy price
    77772173: 12,  # Space Food
    77772174: 80,  # Spike Shield - 80 buy price
    77772175: 10,  # Spite Pouch
    77772176: 30,  # Star Key
    77772177: 15,  # Star Piece
    77772178: 30,  # Station Key 1
    77772179: 30,  # Station Key 2
    77772180: 30,  # Steeple Key
    77772182: 12,  # Stopwatch
    77772183: 30,  # Storage Key 1
    77772184: 30,  # Storage Key 2
    77772185: 20,  # Strange Sack
    77772186: 30,  # Sun Stone
    77772187: 30,  # Super Appeal - 30 buy price
    77772188: 30,  # Super Appeal P - 30 buy price
    77772190: 30,  # Progressive Hammer
    77772191: 15,  # Super Shroom
    77772192: 30,  # Superbombomb
    77772193: 3,  # Tasty Tonic
    77772194: 30,  # The Letter "p"
    77772195: 12,  # Thunder Bolt
    77772196: 20,  # Thunder Rage
    77772197: 50,  # Timing Tutor - 50 buy price
    77772198: 50,  # Tornado Jump - 50 buy price
    77772199: 30,  # Train Ticket
    77772200: 30,  # Tube Mode
    77772201: 2,  # Turtley Leaf
    77772202: 30,  # Progressive Boots
    77772204: 50,  # Ultra Shroom
    77772205: 30,  # Unsimplifier - 30 buy price
    77772206: 20,  # Up Arrow
    77772207: 30,  # Vital Paper
    77772208: 30,  # Vivian
    77772209: 10,  # Volt Shroom
    77772210: 80,  # W Emblem - 80 buy price
    77772211: 30,  # Wedding Ring
    77772212: 50,  # Whacka Bump
    77772213: 30,  # Yoshi
    77772214: 50,  # Zap Tap - 50 buy price
    77772229: 40,  # Zess Dynamite
    77772230: 50,  # Zess Special
}

location_to_unit = {
    78780850: [0x01, 0x24],  # Tattle: Goomba -> unit_kuriboo
    78780851: [0x02],  # Tattle: Paragoomba -> unit_patakuri
    78780852: [0x03],  # Tattle: Spiky Goomba -> unit_togekuri
    78780853: [0x42],  # Tattle: Hyper Goomba -> unit_hyper_kuriboo
    78780854: [0x43],  # Tattle: Hyper Paragoomba -> unit_hyper_patakuri
    78780855: [0x44],  # Tattle: Hyper Spiky Goomba -> unit_hyper_togekuri
    78780856: [0x99],  # Tattle: Gloomba -> unit_yami_kuriboo
    78780857: [0x9a],  # Tattle: Paragloomba -> unit_yami_patakuri
    78780858: [0x9b],  # Tattle: Spiky Gloomba -> unit_yami_togekuri
    78780859: [0x0e],  # Tattle: Koopa Troopa -> unit_nokonoko
    78780860: [0x0f],  # Tattle: Paratroopa -> unit_patapata
    78780861: [0x25],  # Tattle: KP Koopa -> unit_nokonoko_fighter
    78780862: [0x26],  # Tattle: KP Paratroopa -> unit_patapata_fighter
    78780863: [0x2f],  # Tattle: Shady Koopa -> unit_ura_noko
    78780864: [0x30],  # Tattle: Shady Paratroopa -> unit_ura_pata
    78780865: [0x9c],  # Tattle: Dark Koopa -> unit_yami_noko
    78780866: [0x9d],  # Tattle: Dark Paratroopa -> unit_yami_pata
    78780867: [0x0b],  # Tattle: Koopatrol -> unit_togenoko
    78780868: [0x3c],  # Tattle: Dark Koopatrol -> unit_togenoko_ace
    78780869: [0x11],  # Tattle: Dull Bones -> unit_honenoko
    78780870: [0x16],  # Tattle: Red Bones -> unit_red_honenoko
    78780871: [0x82],  # Tattle: Dry Bones -> unit_karon
    78780872: [0x83],  # Tattle: Dark Bones -> unit_black_karon
    78780873: [0x38],  # Tattle: Hammer Bro -> unit_hammer_bros
    78780874: [0x39],  # Tattle: Boomerang Bro -> unit_boomerang_bros
    78780875: [0x3a],  # Tattle: Fire Bro -> unit_fire_bros
    78780876: [0x28],  # Tattle: Lakitu -> unit_jyugem
    78780877: [0x9f],  # Tattle: Dark Lakitu -> unit_hyper_jyugem
    78780878: [0x29],  # Tattle: Spiny -> unit_togezo
    78780879: [0xa0],  # Tattle: Sky-Blue Spiny -> unit_hyper_togezo
    78780880: [0x48],  # Tattle: Buzzy Beetle -> unit_met
    78780881: [0x49],  # Tattle: Spike Top -> unit_togemet
    78780882: [0x59],  # Tattle: Parabuzzy -> unit_patamet
    78780883: [0x69],  # Tattle: Spiky Parabuzzy -> unit_patatogemet
    78780884: [0x2e],  # Tattle: Red Spike Top -> unit_crimson_togemet
    78780885: [0x0C, 0x0D],  # Tattle: Magikoopa -> unit_kamec
    78780886: [0x31, 0x32],  # Tattle: Red Magikoopa -> unit_kamec_red
    78780887: [0x33, 0x34],  # Tattle: White Magikoopa -> unit_kamec_white
    78780888: [0x35, 0x36],  # Tattle: Green Magikoopa -> unit_kamec_green
    78780889: [0x91],  # Tattle: Kammy Koopa -> unit_boss_kamec_obaba
    78780890: [0x90, 0x3F],  # Tattle: Bowser -> unit_boss_koopa
    78780891: [0x07],  # Tattle: Gus -> unit_monban
    78780892: [0x37],  # Tattle: Dark Craw -> unit_dark_keeper
    78780893: [0x2c],  # Tattle: Bandit -> unit_borodo
    78780894: [0x2d],  # Tattle: Big Bandit -> unit_borodo_king
    78780895: [0x9e],  # Tattle: Badge Bandit -> unit_badge_borodo
    78780896: [0x04],  # Tattle: Spinia -> unit_hinnya
    78780897: [0x05],  # Tattle: Spania -> unit_hannya
    78780898: [0xa3],  # Tattle: Spunia -> unit_hennya
    78780899: [0x10, 0x15],  # Tattle: Fuzzy -> unit_chorobon
    78780900: [0x14],  # Tattle: Gold Fuzzy -> unit_gold_chorobon
    78780901: [0x56],  # Tattle: Green Fuzzy -> unit_green_chorobon
    78780902: [0x57],  # Tattle: Flower Fuzzy -> unit_flower_chorobon
    78780903: [0x27],  # Tattle: Pokey -> unit_sambo
    78780904: [0x68],  # Tattle: Poison Pokey -> unit_sambo_mummy
    78780905: [0x19],  # Tattle: Pale Piranha -> unit_monochrome_pakkun
    78780906: [0x58],  # Tattle: Putrid Piranha -> unit_poison_pakkun
    78780907: [0x71],  # Tattle: Frost Piranha -> unit_ice_pakkun
    78780908: [0xa2],  # Tattle: Piranha Plant -> unit_pakkun_flower
    78780909: [0x45],  # Tattle: Crazee Dayzee -> unit_pansy
    78780910: [0x46],  # Tattle: Amazy Dayzee -> unit_twinkling_pansy
    78780911: [0x1b],  # Tattle: Pider -> unit_piders
    78780912: [0xa4],  # Tattle: Arantula -> unit_churantalar
    78780913: [0x4a],  # Tattle: Swooper -> unit_basabasa
    78780914: [0x7b],  # Tattle: Swoopula -> unit_basabasa_chururu
    78780915: [0xa7],  # Tattle: Swampire -> unit_basabasa_green
    78780916: [0x18],  # Tattle: Dark Puff -> unit_monochrome_kurokumorn
    78780917: [0x67],  # Tattle: Ruff Puff -> unit_kurokumorn
    78780918: [0x70],  # Tattle: Ice Puff -> unit_bllizard
    78780919: [0xa6],  # Tattle: Poison Puff -> unit_dokugassun
    78780920: [0x4b],  # Tattle: Boo -> unit_teresa
    78780921: [0x4c],  # Tattle: Atomic Boo -> unit_atmic_teresa
    78780922: [0x6a],  # Tattle: Dark Boo -> unit_purple_teresa
    78780923: [0x54],  # Tattle: Ember -> unit_hermos
    78780924: [0x55],  # Tattle: Lava Bubble -> unit_bubble
    78780925: [0x7c],  # Tattle: Phantom Ember -> unit_phantom
    78780926: [0x12],  # Tattle: Bald Cleft -> unit_sinnosuke
    78780927: [0x2a],  # Tattle: Hyper Bald Cleft -> unit_hyper_sinnosuke
    78780928: [0x1a],  # Tattle: Cleft -> unit_monochrome_sinemon
    78780929: [0x3D, 0x3E],  # Tattle: Iron Cleft (Red) -> unit_iron_sinemon
    78780931: [0x47],  # Tattle: Hyper Cleft -> unit_hyper_sinemon
    78780932: [0x72],  # Tattle: Moon Cleft -> unit_sinemon
    78780933: [0x13],  # Tattle: Bristle -> unit_togedaruma
    78780934: [0xa5],  # Tattle: Dark Bristle -> unit_yamitogedaruma
    78780935: [0x2b],  # Tattle: Bob-omb -> unit_bomhei
    78780936: [0x5c],  # Tattle: Bulky Bob-omb -> unit_heavy_bom
    78780937: [0xa8],  # Tattle: Bob-ulk -> unit_giant_bomb
    78780938: [0x7f],  # Tattle: Chain-Chomp -> unit_wanwan
    78780939: [0x3b],  # Tattle: Red Chomp -> unit_burst_wanwan
    78780940: [0x5a],  # Tattle: Bill Blaster -> unit_killer_cannon
    78780941: [0x5b],  # Tattle: Bullet Bill -> unit_killer
    78780942: [0x7d],  # Tattle: B. Bill Blaster -> unit_super_killer_cannon
    78780943: [0x7e],  # Tattle: Bombshell Bill -> unit_super_killer
    78780944: [0x80, 0x81],  # Tattle: Dark Wizzerd -> unit_super_mahorn
    78780945: [0xa1],  # Tattle: Wizzerd -> unit_mahorn
    78780946: [0xA9, 0xAA],  # Tattle: Elite Wizzerd -> unit_mahorn_custom
    78780947: [0x08, 0x09, 0x0A],  # Tattle: Blooper -> unit_boss_gesso
    78780948: [0x17],  # Tattle: Hooktail -> unit_boss_gonbaba
    78780949: [0x84],  # Tattle: Gloomtail -> unit_boss_bunbaba
    78780950: [0xab],  # Tattle: Bonetail -> unit_boss_zonbaba
    78780951: [0x40],  # Tattle: Rawk Hawk -> unit_boss_champion
    78780952: [0x41],  # Tattle: Macho Grubba -> unit_boss_macho_gance
    78780953: [0x4D, 0x4E, 0x4F],  # Tattle: Doopliss -> unit_boss_rampell
    78780954: [0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62],  # Tattle: Cortez -> unit_boss_cortez
    78780955: [0x6b, 0x6E, 0x6D, 0x6C, 0x6F],  # Tattle: Smorg -> unit_boss_moamoa
    78780956: [0x1c, 0x64, 0x65, 0x66],  # Tattle: X-Naut -> unit_gundan_zako
    78780957: [0x77],  # Tattle: X-Naut PhD -> unit_gundan_zako_magician
    78780958: [0x78],  # Tattle: Elite X-Naut -> unit_gundan_zako_elite
    78780959: [0x1d],  # Tattle: Yux -> unit_barriern
    78780960: [0x1e],  # Tattle: Mini-Yux -> unit_barriern_satellite
    78780961: [0x73],  # Tattle: Z-Yux -> unit_barriern_z
    78780962: [0x74],  # Tattle: Mini-Z-Yux -> unit_barriern_z_satellite
    78780963: [0x75],  # Tattle: X-Yux -> unit_barriern_custom
    78780964: [0x76],  # Tattle: Mini-X-Yux -> unit_barriern_custom_satellite
    78780965: [0x93],  # Tattle: Grodus X -> unit_boss_batten_satellite
    78780966: [0x22, 0x23],  # Tattle: Magnus von Grapple -> unit_boss_magnum_battender
    78780967: [0x79, 0x7A],  # Tattle: Magnus von Grapple 2.0 -> unit_boss_magnum_battender_mkII
    78780968: [0x06],  # Tattle: Lord Crump -> unit_boss_kanbu1
    78780969: [0x92],  # Tattle: Sir Grodus -> unit_boss_batten_leader
    78780970: [0x1f, 0xBD, 0xC0, 0x85],  # Tattle: Beldam -> unit_boss_majolyne
    78780971: [0x20, 0xBE, 0xC1, 0x86],  # Tattle: Marilyn -> unit_boss_marilyn
    78780972: [0x21, 0xBF],  # Tattle: Vivian -> unit_boss_vivian
    78780973: [0x94, 0x96, 0x97, 0x98, 0x95]  # Tattle: Shadow Queen -> unit_boss_black_peach
}

limit_pit = [
    78780638, 78780639, 78780640, 78780641, 78780642, 78780643,
    78780644, 78780645, 78780646, 78780647
]

limited_tags = {
    1: ["petal_left", "petal_right", "hooktails_castle"],
    2: ["boggly_woods", "great_tree"],
    3: ["glitzville"],
    4: ["twilight_town", "twilight_trail", "creepy_steeple"],
    5: ["keelhaul_key", "pirates_grotto"],
    6: ["excess_express", "riverside", "poshley_heights"],
    7: ["fahr_outpost", "xnaut_fortress"],
    8: ["palace", "riddle_tower"]
}

limited_tag_items = {
    "petal_left": [],
    "petal_right": ["Sun Stone", "Moon Stone"],
    "hooktails_castle": ["Castle Key", "Black Key (Paper)"],
    "boggly_woods": ["Necklace"],
    "great_tree": ["Red Key", "Blue Key", "Puni Orb"],
    "glitzville": ["Storage Key 1", "Storage Key 2"],
    "twilight_town": ["Shop Key", "Superbombomb"],
    "twilight_trail": [],
    "creepy_steeple": ["Black Key (Tube)", "Steeple Key",  "The Letter \"p\""],
    "keelhaul_key": ["Chuckola Cola", "Skull Gem", "Wedding Ring", "Coconut"],
    "pirates_grotto": ["Gate Handle", "Black Key (Boat)", "Grotto Key"],
    "excess_express": ["Autograph", "Shell Earrings", "Gold Ring", "Briefcase", "Galley Pot", "Vital Paper", "Blanket", "Ragged Diary"],
    "riverside": ["Elevator Key (Station)", "Station Key 1", "Station Key 2"],
    "poshley_heights": [],
    "fahr_outpost": ["Goldbob Guide"],
    "xnaut_fortress": ["Elevator Key 1", "Elevator Key 2", "Cog", "Card Key 1", "Card Key 2", "Card Key 3", "Card Key 4"],
    "palace": [],
    "riddle_tower": []
}

stars = {
    1: "Diamond Star",
    2: "Emerald Star",
    3: "Gold Star",
    4: "Ruby Star",
    5: "Sapphire Star",
    6: "Garnet Star",
    7: "Crystal Star"
}

star_locations = [
    "Hooktail's Castle Hooktail's Room: Diamond Star",
    "Great Tree Entrance: Emerald Star",
    "Glitzville Arena: Gold Star",
    "Creepy Steeple Upper Room: Ruby Star",
    "Pirate's Grotto Cortez' Hoard: Sapphire Star",
    "Poshley Heights Sanctum Altar: Garnet Star",
    "X-Naut Fortress Boss Room: Crystal Star"
]

dazzle_location_names = [
    "Rogueport Sewers Town: Dazzle Item 1",
    "Rogueport Sewers Town: Dazzle Item 2",
    "Rogueport Sewers Town: Dazzle Item 3",
    "Rogueport Sewers Town: Dazzle Item 4",
    "Rogueport Sewers Town: Dazzle Item 5",
    "Rogueport Sewers Town: Dazzle Item 6",
    "Rogueport Sewers Town: Dazzle Item 7",
    "Rogueport Sewers Town: Dazzle Item 8",
    "Rogueport Sewers Town: Dazzle Item 9",
    "Rogueport Sewers Town: Dazzle Item 10",
    "Rogueport Sewers Town: Dazzle Item 11",
    "Rogueport Sewers Town: Dazzle Item 12",
    "Rogueport Sewers Town: Dazzle Item 13",
    "Rogueport Sewers Town: Dazzle Item 14",
    "Rogueport Sewers Town: Dazzle Item 15"
]

dazzle_counts = [
    1, 3, 6, 10, 14, 18, 23, 29, 35, 42, 50, 60, 70, 85, 100
]

chapter_keys = {
    1: ["Black Key (Paper)", "Castle Key"],
    2: ["Blue Key", "Red Key"],
    3: ["Storage Key 2", "Storage Key 1"],
    4: ["Steeple Key", "Black Key (Tube)", "Shop Key"],
    5: ["Black Key (Boat)", "Grotto Key"],
    6: ["Elevator Key (Station)", "Station Key 2", "Station Key 1"],
    7: [ "Card Key 4", "Card Key 3", "Card Key 2", "Card Key 1", "Elevator Key 2", "Elevator Key 1"],
    8: ["Star Key", "Palace Key (Tower)", "Palace Key"],
}

chapter_keysanity_tags = {
    1: "hooktails_castle",
    2: "great_tree",
    3: "glitzville",
    4: "creepy_steeple",
    5: "pirates_grotto",
    6: "riverside",
    7: "xnaut_fortress",
    8: "palace"
}

pit_exclusive_tattle_stars_required = {
    1: [
        "Tattle: Gloomba",
        "Tattle: Paragloomba"
    ],
    2: [
        "Tattle: Spiky Gloomba",
        "Tattle: Dark Koopa"
    ],
    3: [
        "Tattle: Dark Paratroopa",
        "Tattle: Badge Bandit",
        "Tattle: Dark Boo"
    ],
    4: [
        "Tattle: Dark Lakitu",
        "Tattle: Sky-Blue Spiny",
        "Tattle: Wizzerd"
    ],
    5: [
        "Tattle: Piranha Plant",
        "Tattle: Dark Bristle",
        "Tattle: Arantula",
        "Tattle: Elite Wizzerd",
        "Tattle: Swampire",
        "Tattle: Poison Puff",
        "Tattle: Bob-ulk",
        "Tattle: Bonetail"
    ]
}

item_classifications: typing.Dict[str, ItemClassification] = {
    "filler": ItemClassification.filler,
    "useful": ItemClassification.useful,
    "progression": ItemClassification.progression,
    "trap": ItemClassification.trap
}
