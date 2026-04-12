from typing import List, NamedTuple


class SubXBitfield(NamedTuple):
    bitfield_bit_number: int
    subX_area: int
    subX_byte: int
    subX_bit_number: int
    flag_definition: str  # name
    prerequisites: List[str]  # What item / state is needed for this check to be accessible
    default_item: str  # what item is normally there?
    classification: str = ""  # internal group name for referencing in the rules or initialization phases


subX_table = [
    SubXBitfield(0, 1, 0, 0, "Bag Upgrade 1", [], "Bag Upgrade", "ProgressiveBagUpgrade"),
    SubXBitfield(1, 1, 0, 1, "Bag Upgrade 2", ["Mt. Bristle"], "Bag Upgrade", "ProgressiveBagUpgrade"),
    SubXBitfield(2, 1, 0, 2, "Bag Upgrade 3", ["Apple Woods"], "Bag Upgrade", "ProgressiveBagUpgrade"),
    SubXBitfield(3, 1, 0, 3, "Bag Upgrade 4", ["Steam Cave"], "Bag Upgrade", "ProgressiveBagUpgrade"),
    SubXBitfield(
        4, 1, 0, 4, "Bag Upgrade 5", ["Defeat Dialga", "Mystifying Forest"], "Bag Upgrade", "ProgressiveBagUpgrade"
    ),
    SubXBitfield(5, 1, 0, 5, "Bidoof's Wish Location", [], "Bidoof's SE", "Free"),
    SubXBitfield(6, 1, 0, 6, "Igglybuff the Prodigy Location", [], "Igglybuff's SE", "Free"),
    SubXBitfield(7, 1, 0, 7, 'Today\'s "Oh My Gosh" Location', [], "Sunflora's SE", "Free"),
    SubXBitfield(8, 1, 1, 0, "Here Comes Team Charm! Location", [], "Team Charm SE", "Free"),
    SubXBitfield(
        9, 1, 1, 1, "In the Future of Darkness Location", ["Hidden Land"], "Grovyle + Dusknoir SE", "SEDungeonUnlock"
    ),
    SubXBitfield(10, 1, 1, 2, "Shop Item 1", ["ProgressiveBag3", "Main Game"], "Filler", "ShopItem"),  # 5k
    SubXBitfield(11, 1, 1, 3, "Shop Item 2", ["ProgressiveBag2", "Main Game"], "Filler", "ShopItem"),  # 1k
    SubXBitfield(12, 1, 1, 4, "Shop Item 3", ["ProgressiveBag2", "Main Game"], "Filler", "ShopItem"),  # 1k
    SubXBitfield(13, 1, 1, 5, "Shop Item 4", ["ProgressiveBag2", "Main Game"], "Filler", "ShopItem"),  # 1k
    SubXBitfield(14, 1, 1, 6, "Shop Item 5", ["ProgressiveBag2"], "Filler", "ShopItem"),  # 500
    SubXBitfield(15, 1, 1, 7, "Shop Item 6", ["ProgressiveBag2"], "Filler", "ShopItem"),  # 500
    SubXBitfield(16, 2, 0, 0, "Shop Item 7", ["ProgressiveBag2", "Main Game"], "Filler", "ShopItem"),  # 5k
    SubXBitfield(17, 2, 0, 1, "Shop Item 8", ["ProgressiveBag2", "Main Game"], "Filler", "ShopItem"),  # 1k
    SubXBitfield(18, 2, 0, 2, "Shop Item 9", ["ProgressiveBag3", "Main Game"], "Filler", "ShopItem"),  # 1k
    SubXBitfield(19, 2, 0, 3, "Shop Item 10", [], "Filler", "Free"),  # 100
    SubXBitfield(20, 2, 0, 4, "Blue Goomi #1", ["Defeat Dialga", "Surrounded Sea"], "Filler", "Manaphy"),
    SubXBitfield(21, 2, 0, 5, "Blue Goomi #2", ["Defeat Dialga", "Surrounded Sea"], "Filler", "Manaphy"),
    SubXBitfield(
        22, 2, 0, 6, "Manaphy Healed", ["Defeat Dialga", "Surrounded Sea", "Miracle Sea"], "Filler", "Manaphy"
    ),
    SubXBitfield(
        23, 2, 0, 7, "Manaphy's Gift", ["Defeat Dialga", "Surrounded Sea", "Miracle Sea"], "Manaphy", "Manaphy"
    ),
    SubXBitfield(24, 2, 1, 0, "Manaphy's Discovery", ["Defeat Dialga", "Manaphy"], "Marine Resort", "Manaphy"),
    SubXBitfield(25, 2, 1, 1, "Uxie's Gift", ["Defeat Dialga", "Steam Cave"], "Uxie", "Legendary"),
    SubXBitfield(26, 2, 1, 2, "Mesprit's Gift", ["Defeat Dialga", "Quicksand Cave"], "Mesprit", "Legendary"),
    SubXBitfield(27, 2, 1, 3, "Azelf's Gift", ["Defeat Dialga", "Crystal Crossing"], "Azelf", "Legendary"),
    SubXBitfield(
        28, 2, 1, 4, "Dialga's Gift", ["Defeat Dialga", "Temporal Tower", "Hidden Land"], "Dialga", "Legendary"
    ),
    SubXBitfield(
        29, 2, 1, 5, "Phione's Gift", ["Defeat Dialga", "Surrounded Sea", "Miracle Sea"], "Phione", "Legendary"
    ),
    SubXBitfield(30, 2, 1, 6, "Palkia's Gift", ["Defeat Dialga", "Spacial Rift"], "Dialga", "Legendary"),
    SubXBitfield(
        31,
        2,
        1,
        7,
        "Aqua-Monica Location",
        ["Defeat Dialga", "Secret Rank", "Bottomless Sea"],
        "Aqua-Monica",
        "Instrument",
    ),
    SubXBitfield(
        32, 3, 0, 0, "Kyogre's Gift", ["Defeat Dialga", "Secret Rank", "Bottomless Sea"], "Kyogre", "Legendary"
    ),
    SubXBitfield(
        33,
        3,
        0,
        1,
        "Terra Cymbal Location",
        ["Defeat Dialga", "Secret Rank", "Shimmer Desert"],
        "Terra Cymbal",
        "Instrument",
    ),
    SubXBitfield(
        34, 3, 0, 2, "Groudon's Gift", ["Defeat Dialga", "Secret Rank", "Shimmer Desert"], "Groudon", "Legendary"
    ),
    SubXBitfield(
        35, 3, 0, 3, "Icy Flute Location", ["Defeat Dialga", "Secret Rank", "Mt. Avalanche"], "Icy Flute", "Instrument"
    ),
    SubXBitfield(
        36, 3, 0, 4, "Articuno's Gift", ["Defeat Dialga", "Secret Rank", "Mt. Avalanche"], "Articuno", "Legendary"
    ),
    SubXBitfield(
        37,
        3,
        0,
        5,
        "Fiery Drum Location",
        ["Defeat Dialga", "Secret Rank", "Giant Volcano"],
        "Fiery Drum",
        "Instrument",
    ),
    SubXBitfield(
        38, 3, 0, 6, "Heatran's Gift", ["Defeat Dialga", "Secret Rank", "Giant Volcano"], "Heatran", "Legendary"
    ),
    SubXBitfield(
        39, 3, 0, 7, "Rock Horn Location", ["Defeat Dialga", "Secret Rank", "World Abyss"], "Rock Horn", "Instrument"
    ),
    SubXBitfield(
        40, 3, 1, 0, "Giratina's Gift", ["Defeat Dialga", "Secret Rank", "World Abyss"], "Giratina", "Legendary"
    ),
    SubXBitfield(
        41,
        3,
        1,
        1,
        "Sky Melodica Location",
        ["Defeat Dialga", "Secret Rank", "Sky Stairway"],
        "Sky Melodica",
        "Instrument",
    ),
    SubXBitfield(
        42, 3, 1, 2, "Rayquaza's Gift", ["Defeat Dialga", "Secret Rank", "Sky Stairway"], "Rayquaza", "Legendary"
    ),
    SubXBitfield(
        43,
        3,
        1,
        3,
        "Grass Cornet Location",
        ["Defeat Dialga", "Secret Rank", "Mystery Jungle"],
        "Grass Cornet",
        "Instrument",
    ),
    SubXBitfield(44, 3, 1, 4, "Mew's Gift", ["Defeat Dialga", "Secret Rank", "Mystery Jungle"], "Mew", "Legendary"),
    SubXBitfield(45, 3, 1, 5, "Cresselia's Gift", ["Defeat Dialga"], "Cresselia", "Legendary"),
    SubXBitfield(46, 3, 1, 6, "Shaymin's Gift", ["Defeat Dialga", "Sky Peak Summit Pass"], "Shaymin", "Legendary"),
    SubXBitfield(47, 3, 1, 7, "Scizor's Gift", ["Defeat Dialga", "Crevice Cave"], "Secret Rank", "SecretRank"),
    SubXBitfield(48, 4, 0, 0, "Aqua-Monica Mission", ["Secret Rank", "Bottomless Sea"], "Bottomless Sea", "LateSubX"),
    SubXBitfield(49, 4, 0, 1, "Terra Cymbal Mission", ["Secret Rank", "Shimmer Desert"], "Shimmer Desert", "LateSubX"),
    SubXBitfield(50, 4, 0, 2, "Icy Flute Mission", ["Secret Rank", "Mt. Avalanche"], "Mt. Avalanche", "LateSubX"),
    SubXBitfield(51, 4, 0, 3, "Fiery Drum Mission", ["Secret Rank", "Giant Volcano"], "Giant Volcano", "LateSubX"),
    SubXBitfield(52, 4, 0, 4, "Rock Horn Mission", ["Secret Rank", "World Abyss"], "World Abyss", "LateSubX"),
    SubXBitfield(53, 4, 0, 5, "Sky Melodica Mission", ["Secret Rank", "Sky Stairway"], "Sky Stairway", "LateSubX"),
    SubXBitfield(54, 4, 0, 6, "Grass Cornet Mission", ["Secret Rank", "Mystery Jungle"], "Mystery Jungle", "LateSubX"),
    SubXBitfield(55, 4, 0, 7, "Master ★ Rank", ["Secret Rank", "Defeat Dialga"], "Treacherous Waters", "Rank"),
    SubXBitfield(56, 4, 1, 0, "Master ★★ Rank", ["Secret Rank", "Defeat Dialga"], "Southeastern Islands", "Rank"),
    SubXBitfield(57, 4, 1, 1, "Master ★★★ Rank", ["Secret Rank", "Defeat Dialga"], "Inferno Cave", "Rank"),
    SubXBitfield(
        58, 4, 1, 2, "Guildmaster Rank", ["Secret Rank", "Defeat Dialga", "ProgressiveBag3"], "Inferno Cave", "Rank"
    ),
    SubXBitfield(59, 4, 1, 3, "Recycle Shop Treasure Found", ["Main Game"], "Filler", "ShopItem"),
    SubXBitfield(
        60, 4, 1, 4, "Recycle Shop Dungeon #1", ["ProgressiveBag3", "Main Game"], "Landslide Cave", "ShopItem"
    ),
    SubXBitfield(61, 4, 1, 5, "Recycle Shop Dungeon #2", ["ProgressiveBag3", "Main Game"], "Tiny Meadow", "ShopItem"),
    SubXBitfield(62, 4, 1, 6, "Recycle Shop Dungeon #3", ["ProgressiveBag3", "Main Game"], "Oran Forest", "ShopItem"),
    SubXBitfield(
        63,
        4,
        1,
        7,
        "Recycle Shop Dungeon #4",
        ["ProgressiveBag3", "Main Game", "Defeat Dialga", "Formation Control"],
        "Lake Afar",
        "ShopItem",
    ),
    SubXBitfield(
        64,
        5,
        0,
        0,
        "Recycle Shop Dungeon #5",
        ["ProgressiveBag3", "Defeat Dialga", "Formation Control", "Main Game"],
        "Zero Isle Center",
        "ShopItem",
    ),
    SubXBitfield(
        65,
        5,
        0,
        1,
        "Sneasel's Gratitude",
        ["Defeat Dialga", "7th Station Pass", "Sky Peak Summit Pass"],
        "Filler",
        "LateSubX",
    ),
    SubXBitfield(66, 5, 0, 2, "SE Marowak Dojo's Revival", ["Bidoof's Wish"], "Filler", "SpecialDungeonComplete"),
    SubXBitfield(67, 5, 0, 3, "Clear All Marowak Mazes", ["All Mazes"], "Filler", "OptionalSubX"),
    SubXBitfield(68, 5, 0, 4, "Grandpa's Treasure", ["Dojo Final Maze"], "Filler", "OptionalSubX"),
    SubXBitfield(69, 5, 0, 5, "Regice's Gift", ["Defeat Dialga", "Ice Seal", "Ice Aegis Cave"], "Regice", "Legendary"),
    SubXBitfield(
        70, 5, 0, 6, "Regirock's Gift", ["Defeat Dialga", "Rock Seal", "Ice Aegis Cave"], "Regirock", "Legendary"
    ),
    SubXBitfield(
        71, 5, 0, 7, "Registeel's Gift", ["Defeat Dialga", "Steel Seal", "Ice Aegis Cave"], "Registeel", "Legendary"
    ),
    SubXBitfield(
        72,
        5,
        1,
        0,
        "Regigigas's Gift",
        ["Defeat Dialga", "Ice Seal", "Rock Seal", "Steel Seal", "Ice Aegis Cave"],
        "Regigigas",
        "Legendary",
    ),
    SubXBitfield(73, 5, 1, 1, "Bronze Rank", ["3 Early"], "Filler", "Rank"),
    SubXBitfield(74, 5, 1, 2, "Silver Rank", ["3 Early"], "Filler", "Rank"),
    SubXBitfield(75, 5, 1, 3, "Gold Rank", ["3 Early"], "Filler", "Rank"),
    SubXBitfield(76, 5, 1, 4, "Diamond Rank", ["5 Early"], "Filler", "Rank"),
    SubXBitfield(77, 5, 1, 5, "Super Rank", ["5 Early"], "Filler", "Rank"),
    SubXBitfield(78, 5, 1, 6, "Ultra Rank", ["10 Early"], "Filler", "Rank"),
    SubXBitfield(79, 5, 1, 7, "Hyper Rank", ["10 Early"], "Filler", "Rank"),
    SubXBitfield(80, 6, 0, 0, "Master Rank", ["10 Early"], "Filler", "Rank"),
    SubXBitfield(81, 6, 0, 1, "Duskull 100G Reward", [], "Filler", "ShopItem"),
    SubXBitfield(82, 6, 0, 2, "Duskull 5,000G Reward", ["ProgressiveBag1"], "Filler", "ShopItem"),
    SubXBitfield(83, 6, 0, 3, "Duskull 10,000G Reward", ["ProgressiveBag2", "Main Game"], "Filler", "ShopItem"),
    SubXBitfield(84, 6, 0, 4, "Duskull 20,000G Reward", ["ProgressiveBag2", "Main Game"], "Filler", "ShopItem"),
    SubXBitfield(85, 6, 0, 5, "Duskull 50,000G Reward", ["ProgressiveBag3"], "Filler", "OptionalSubX"),
    SubXBitfield(86, 6, 0, 6, "Duskull 100,000G Reward", ["ProgressiveBag3"], "Filler", "OptionalSubX"),
    SubXBitfield(
        87, 6, 0, 7, "Duskull 9,999,999G Reward", ["ProgressiveBag3", "Defeat Dialga"], "Filler", "OptionalSubX"
    ),
    SubXBitfield(88, 6, 1, 0, "Ludicolo Dance", ["ProgressiveBag1"], "Filler", "OptionalSubX"),
    SubXBitfield(89, 6, 1, 1, "Unused", ["-"], "-"),
    SubXBitfield(90, 6, 1, 2, "Unused", ["-"], "-"),
    SubXBitfield(91, 6, 1, 3, "Unused", ["-"], "-"),
    SubXBitfield(92, 6, 1, 4, "Unused", ["-"], "-"),
    SubXBitfield(93, 6, 1, 5, "Unused", ["-"], "-"),
    SubXBitfield(94, 6, 1, 6, "Unused", ["-"], "-"),
    SubXBitfield(95, 6, 1, 7, "Unused", ["-"], "-"),
    SubXBitfield(96, 7, 0, 0, "Unused", ["-"], "-"),
    SubXBitfield(97, 7, 0, 1, "Unused", ["-"], "-"),
    SubXBitfield(98, 7, 0, 2, "Unused", ["-"], "-"),
    SubXBitfield(99, 7, 0, 3, "Unused", ["-"], "-"),
    SubXBitfield(100, 7, 0, 4, "Unused", ["-"], "-"),
    SubXBitfield(101, 7, 0, 5, "Unused", ["-"], "-"),
    SubXBitfield(102, 7, 0, 6, "Unused", ["-"], "-"),
    SubXBitfield(103, 7, 0, 7, "Unused", ["-"], "-"),
    SubXBitfield(104, 7, 1, 0, "Unused", ["-"], "-"),
    SubXBitfield(105, 7, 1, 1, "Unused", ["-"], "-"),
    SubXBitfield(106, 7, 1, 2, "Unused", ["-"], "-"),
    SubXBitfield(107, 7, 1, 3, "Unused", ["-"], "-"),
    SubXBitfield(108, 7, 1, 4, "Unused", ["-"], "-"),
    SubXBitfield(109, 7, 1, 5, "Unused", ["-"], "-"),
    SubXBitfield(110, 7, 1, 6, "Unused", ["-"], "-"),
    SubXBitfield(111, 7, 1, 7, "Unused", ["-"], "-"),
    SubXBitfield(112, 8, 0, 0, "Unused", ["-"], "-"),
    SubXBitfield(113, 8, 0, 1, "Unused", ["-"], "-"),
    SubXBitfield(114, 8, 0, 2, "Unused", ["-"], "-"),
    SubXBitfield(115, 8, 0, 3, "Unused", ["-"], "-"),
    SubXBitfield(116, 8, 0, 4, "Unused", ["-"], "-"),
    SubXBitfield(117, 8, 0, 5, "Unused", ["-"], "-"),
    SubXBitfield(118, 8, 0, 6, "Unused", ["-"], "-"),
    SubXBitfield(119, 8, 0, 7, "Unused", ["-"], "-"),
    SubXBitfield(120, 8, 1, 0, "Unused", ["-"], "-"),
    SubXBitfield(121, 8, 1, 1, "Unused", ["-"], "-"),
    SubXBitfield(122, 8, 1, 2, "Unused", ["-"], "-"),
    SubXBitfield(123, 8, 1, 3, "Unused", ["-"], "-"),
    SubXBitfield(124, 8, 1, 4, "Unused", ["-"], "-"),
    SubXBitfield(125, 8, 1, 5, "Unused", ["-"], "-"),
    SubXBitfield(126, 8, 1, 6, "Unused", ["-"], "-"),
    SubXBitfield(127, 8, 1, 7, "Team Name Location", ["Main Game"], "Team Name Trap", "Team Name"),
]
