# Archipelago MultiWorld integration for Tyrian
#
# This file is copyright (C) Kay "Kaito" Sinclaire,
# and is released under the terms of the zlib license.
# See "LICENSE" for more details.

from enum import IntEnum
from typing import NamedTuple

from BaseClasses import ItemClassification as IClass


class Episode(IntEnum):
    Escape = 1
    Treachery = 2
    MissionSuicide = 3
    AnEndToFate = 4
    HazudraFodder = 5


class LocalItem:
    local_id: int
    count: int
    tossable: bool
    item_class: IClass

    def __init__(self, local_id: int, count: int = 0, item_class: IClass = IClass.filler):
        self.local_id = local_id
        self.count = count
        self.item_class = item_class
        self.tossable = (IClass.progression not in item_class)


class LocalLevel(LocalItem):
    episode: Episode
    goal_level: bool

    def __init__(self, local_id: int, episode: Episode, goal_level: bool = False):
        self.local_id = local_id
        self.count = 1
        self.item_class = IClass.progression | IClass.useful
        self.episode = episode
        self.tossable = False
        self.goal_level = goal_level

        if goal_level:
            self.item_class |= IClass.skip_balancing


class LocalWeapon(LocalItem):
    def __init__(self, local_id: int, item_class: IClass = IClass.filler, tossable: bool = True, count: int = 1):
        self.local_id = local_id
        self.count = count
        self.item_class = item_class
        self.tossable = tossable


class UpgradeCost(NamedTuple):
    original: int
    balanced: int


# --------------------------------------------------------------------------------------------------------------------


class LocalItemData:
    levels: dict[str, LocalLevel] = {
        "TYRIAN (Episode 1)":    LocalLevel(  0, Episode.Escape),
        "BUBBLES (Episode 1)":   LocalLevel(  1, Episode.Escape),
        "HOLES (Episode 1)":     LocalLevel(  2, Episode.Escape),
        "SOH JIN (Episode 1)":   LocalLevel(  3, Episode.Escape),
        "ASTEROID1 (Episode 1)": LocalLevel(  4, Episode.Escape),
        "ASTEROID2 (Episode 1)": LocalLevel(  5, Episode.Escape),
        "ASTEROID? (Episode 1)": LocalLevel(  6, Episode.Escape),
        "MINEMAZE (Episode 1)":  LocalLevel(  7, Episode.Escape),
        "WINDY (Episode 1)":     LocalLevel(  8, Episode.Escape),
        "SAVARA (Episode 1)":    LocalLevel(  9, Episode.Escape),
        "SAVARA II (Episode 1)": LocalLevel( 10, Episode.Escape),  # Savara Hard
        "BONUS (Episode 1)":     LocalLevel( 11, Episode.Escape),
        "MINES (Episode 1)":     LocalLevel( 12, Episode.Escape),
        "DELIANI (Episode 1)":   LocalLevel( 13, Episode.Escape),
        "SAVARA V (Episode 1)":  LocalLevel( 14, Episode.Escape),
        "ASSASSIN (Episode 1)":  LocalLevel( 15, Episode.Escape, goal_level=True),

        "TORM (Episode 2)":      LocalLevel(100, Episode.Treachery),
        "GYGES (Episode 2)":     LocalLevel(101, Episode.Treachery),
        "BONUS 1 (Episode 2)":   LocalLevel(102, Episode.Treachery),
        "ASTCITY (Episode 2)":   LocalLevel(103, Episode.Treachery),
        "BONUS 2 (Episode 2)":   LocalLevel(104, Episode.Treachery),
        "GEM WAR (Episode 2)":   LocalLevel(105, Episode.Treachery),
        "MARKERS (Episode 2)":   LocalLevel(106, Episode.Treachery),
        "MISTAKES (Episode 2)":  LocalLevel(107, Episode.Treachery),
        "SOH JIN (Episode 2)":   LocalLevel(108, Episode.Treachery),
        "BOTANY A (Episode 2)":  LocalLevel(109, Episode.Treachery),
        "BOTANY B (Episode 2)":  LocalLevel(110, Episode.Treachery),
        "GRYPHON (Episode 2)":   LocalLevel(111, Episode.Treachery, goal_level=True),

        "GAUNTLET (Episode 3)":  LocalLevel(200, Episode.MissionSuicide),
        "IXMUCANE (Episode 3)":  LocalLevel(201, Episode.MissionSuicide),
        "BONUS (Episode 3)":     LocalLevel(202, Episode.MissionSuicide),
        "STARGATE (Episode 3)":  LocalLevel(203, Episode.MissionSuicide),
        "AST. CITY (Episode 3)": LocalLevel(204, Episode.MissionSuicide),
        "SAWBLADES (Episode 3)": LocalLevel(205, Episode.MissionSuicide),
        "CAMANIS (Episode 3)":   LocalLevel(206, Episode.MissionSuicide),
        "MACES (Episode 3)":     LocalLevel(207, Episode.MissionSuicide),
        "TYRIAN X (Episode 3)":  LocalLevel(208, Episode.MissionSuicide),
        "SAVARA Y (Episode 3)":  LocalLevel(209, Episode.MissionSuicide),
        "NEW DELI (Episode 3)":  LocalLevel(210, Episode.MissionSuicide),
        "FLEET (Episode 3)":     LocalLevel(211, Episode.MissionSuicide, goal_level=True),

        "SURFACE (Episode 4)":   LocalLevel(300, Episode.AnEndToFate),
        "WINDY (Episode 4)":     LocalLevel(301, Episode.AnEndToFate),
        "LAVA RUN (Episode 4)":  LocalLevel(302, Episode.AnEndToFate),
        "CORE (Episode 4)":      LocalLevel(303, Episode.AnEndToFate),
        "LAVA EXIT (Episode 4)": LocalLevel(304, Episode.AnEndToFate),
        "DESERTRUN (Episode 4)": LocalLevel(305, Episode.AnEndToFate),
        "SIDE EXIT (Episode 4)": LocalLevel(306, Episode.AnEndToFate),
        "?TUNNEL? (Episode 4)":  LocalLevel(307, Episode.AnEndToFate),
        "ICE EXIT (Episode 4)":  LocalLevel(308, Episode.AnEndToFate),
        "ICESECRET (Episode 4)": LocalLevel(309, Episode.AnEndToFate),
        "HARVEST (Episode 4)":   LocalLevel(310, Episode.AnEndToFate),
        "UNDERDELI (Episode 4)": LocalLevel(311, Episode.AnEndToFate),
        "APPROACH (Episode 4)":  LocalLevel(312, Episode.AnEndToFate),
        "SAVARA IV (Episode 4)": LocalLevel(313, Episode.AnEndToFate),
        "DREAD-NOT (Episode 4)": LocalLevel(314, Episode.AnEndToFate),
        "EYESPY (Episode 4)":    LocalLevel(315, Episode.AnEndToFate),
        "BRAINIAC (Episode 4)":  LocalLevel(316, Episode.AnEndToFate),
        "NOSE DRIP (Episode 4)": LocalLevel(317, Episode.AnEndToFate, goal_level=True),

        # ---------- TYRIAN 2000 LINE ----------
        "ASTEROIDS (Episode 5)": LocalLevel(400, Episode.HazudraFodder),
        "AST ROCK (Episode 5)":  LocalLevel(401, Episode.HazudraFodder),
        "MINERS (Episode 5)":    LocalLevel(402, Episode.HazudraFodder),
        "SAVARA (Episode 5)":    LocalLevel(403, Episode.HazudraFodder),
        "CORAL (Episode 5)":     LocalLevel(404, Episode.HazudraFodder),
        "STATION (Episode 5)":   LocalLevel(405, Episode.HazudraFodder),
        "FRUIT (Episode 5)":     LocalLevel(406, Episode.HazudraFodder, goal_level=True),
    }

    # ----------------------------------------------------------------------------------------------------------------

    # All Front and Rear port weapons are progression, some specific specials are too
    # All other specials and sidekicks are useful at most
    front_ports: dict[str, LocalWeapon] = {
        "Pulse-Cannon":                   LocalWeapon(500, item_class=IClass.progression, tossable=False),
        "Multi-Cannon (Front)":           LocalWeapon(501, item_class=IClass.progression),
        "Mega Cannon":                    LocalWeapon(502, item_class=IClass.progression),
        "Laser":                          LocalWeapon(503, item_class=IClass.progression, tossable=False),
        "Zica Laser":                     LocalWeapon(504, item_class=IClass.progression),
        "Protron Z":                      LocalWeapon(505, item_class=IClass.progression),
        "Vulcan Cannon (Front)":          LocalWeapon(506, item_class=IClass.progression),
        "Lightning Cannon":               LocalWeapon(507, item_class=IClass.progression, tossable=False),
        "Protron (Front)":                LocalWeapon(508, item_class=IClass.progression),
        "Missile Launcher":               LocalWeapon(509, item_class=IClass.progression),
        "Mega Pulse (Front)":             LocalWeapon(510, item_class=IClass.progression),
        "Heavy Missile Launcher (Front)": LocalWeapon(511, item_class=IClass.progression),
        "Banana Blast (Front)":           LocalWeapon(512, item_class=IClass.progression, tossable=False),
        "HotDog (Front)":                 LocalWeapon(513, item_class=IClass.progression),
        "Hyper Pulse":                    LocalWeapon(514, item_class=IClass.progression),
        "Guided Bombs":                   LocalWeapon(515, item_class=IClass.progression),
        "Shuriken Field":                 LocalWeapon(516, item_class=IClass.progression, tossable=False),
        "Poison Bomb":                    LocalWeapon(517, item_class=IClass.progression, tossable=False),
        "Protron Wave":                   LocalWeapon(518, item_class=IClass.progression),
        "The Orange Juicer":              LocalWeapon(519, item_class=IClass.progression),
        "NortShip Super Pulse":           LocalWeapon(520, item_class=IClass.progression),
        "Atomic RailGun":                 LocalWeapon(521, item_class=IClass.progression, tossable=False),
        "Widget Beam":                    LocalWeapon(522, item_class=IClass.progression),
        "Sonic Impulse":                  LocalWeapon(523, item_class=IClass.progression, tossable=False),
        "RetroBall":                      LocalWeapon(524, item_class=IClass.progression),
        # ---------- TYRIAN 2000 LINE ----------
        "Needle Laser":                   LocalWeapon(525, count=0, item_class=IClass.progression, tossable=False),
        "Pretzel Missile":                LocalWeapon(526, count=0, item_class=IClass.progression),
        "Dragon Frost":                   LocalWeapon(527, count=0, item_class=IClass.progression),
        "Dragon Flame":                   LocalWeapon(528, count=0, item_class=IClass.progression),
    }

    rear_ports: dict[str, LocalWeapon] = {
        "Starburst":                     LocalWeapon(600, item_class=IClass.progression, tossable=False),
        "Multi-Cannon (Rear)":           LocalWeapon(601, item_class=IClass.progression),
        "Sonic Wave":                    LocalWeapon(602, item_class=IClass.progression, tossable=False),
        "Protron (Rear)":                LocalWeapon(603, item_class=IClass.progression),
        "Wild Ball":                     LocalWeapon(604, item_class=IClass.progression),
        "Vulcan Cannon (Rear)":          LocalWeapon(605, item_class=IClass.progression),
        "Fireball":                      LocalWeapon(606, item_class=IClass.progression, tossable=False),
        "Heavy Missile Launcher (Rear)": LocalWeapon(607, item_class=IClass.progression),
        "Mega Pulse (Rear)":             LocalWeapon(608, item_class=IClass.progression, tossable=False),
        "Banana Blast (Rear)":           LocalWeapon(609, item_class=IClass.progression, tossable=False),
        "HotDog (Rear)":                 LocalWeapon(610, item_class=IClass.progression),
        "Guided Micro Bombs":            LocalWeapon(611, item_class=IClass.progression),
        "Heavy Guided Bombs":            LocalWeapon(612, item_class=IClass.progression),
        "Scatter Wave":                  LocalWeapon(613, item_class=IClass.progression),
        "NortShip Spreader":             LocalWeapon(614, item_class=IClass.progression, tossable=False),
        "NortShip Spreader B":           LocalWeapon(615, item_class=IClass.progression),
        # ---------- TYRIAN 2000 LINE ----------
        "People Pretzels":               LocalWeapon(616, count=0, item_class=IClass.progression),
    }

    special_weapons: dict[str, LocalWeapon] = {
        "Repulsor":          LocalWeapon(700, item_class=IClass.progression, tossable=False),
        "Pearl Wind":        LocalWeapon(701),
        "Soul of Zinglon":   LocalWeapon(702),
        "Attractor":         LocalWeapon(703),
        "Ice Beam":          LocalWeapon(704, item_class=IClass.useful),
        "Flare":             LocalWeapon(705),
        "Blade Field":       LocalWeapon(706),
        "SandStorm":         LocalWeapon(707),
        "MineField":         LocalWeapon(708),
        "Dual Vulcan":       LocalWeapon(709),
        "Banana Bomb":       LocalWeapon(710, item_class=IClass.useful),
        "Protron Dispersal": LocalWeapon(711),
        "Astral Zone":       LocalWeapon(712),
        "Xega Ball":         LocalWeapon(713),
        "MegaLaser Dual":    LocalWeapon(714),
        "Orange Shield":     LocalWeapon(715),
        "Pulse Blast":       LocalWeapon(716),
        "MegaLaser":         LocalWeapon(717),
        "Missile Pod":       LocalWeapon(718),
        "Invulnerability":   LocalWeapon(719, item_class=IClass.progression, tossable=False),
        "Lightning Zone":    LocalWeapon(720),
        "SDF Main Gun":      LocalWeapon(721, item_class=IClass.useful),
        "Protron Field":     LocalWeapon(722, count=0),  # Deprecated (doesn't function properly)
        # ---------- TYRIAN 2000 LINE ----------
        "Super Pretzel":     LocalWeapon(723, count=0),
        "Dragon Lightning":  LocalWeapon(724, count=0),
    }

    sidekicks: dict[str, LocalWeapon] = {
        "Single Shot Option":         LocalWeapon(800, count=2),
        "Dual Shot Option":           LocalWeapon(801, count=2),
        "Charge Cannon":              LocalWeapon(802, count=2),
        "Vulcan Shot Option":         LocalWeapon(803, count=2),
        "Wobbley":                    LocalWeapon(804, count=2),
        "MegaMissile":                LocalWeapon(805, count=2, item_class=IClass.useful),
        "Atom Bombs":                 LocalWeapon(806, count=2, item_class=IClass.useful),
        "Phoenix Device":             LocalWeapon(807, count=2, item_class=IClass.useful),
        "Plasma Storm":               LocalWeapon(808, count=2, item_class=IClass.useful),
        "Mini-Missile":               LocalWeapon(809, count=2),
        "Buster Rocket":              LocalWeapon(810, count=2),
        "Zica Supercharger":          LocalWeapon(811, count=2),
        "MicroBomb":                  LocalWeapon(812, count=2),
        "8-Way MicroBomb":            LocalWeapon(813, count=2),
        "Post-It Mine":               LocalWeapon(814, count=2),
        "Mint-O-Ship":                LocalWeapon(815, count=2),
        "Zica Flamethrower":          LocalWeapon(816, count=2),
        "Side Ship":                  LocalWeapon(817, count=2),
        "Companion Ship Warfly":      LocalWeapon(818, count=2),
        "MicroSol FrontBlaster":      LocalWeapon(819, count=1, item_class=IClass.useful),  # Right-only (limited to 1)
        "Companion Ship Gerund":      LocalWeapon(820, count=2),
        "BattleShip-Class Firebomb":  LocalWeapon(821, count=1, item_class=IClass.useful),  # Right-only (limited to 1)
        "Protron Cannon Indigo":      LocalWeapon(822, count=1, item_class=IClass.useful),  # Right-only (limited to 1)
        "Companion Ship Quicksilver": LocalWeapon(823, count=2),
        "Protron Cannon Tangerine":   LocalWeapon(824, count=1, item_class=IClass.useful),  # Right-only (limited to 1)
        "MicroSol FrontBlaster II":   LocalWeapon(825, count=1, item_class=IClass.useful),  # Right-only (limited to 1)
        "Beno Wallop Beam":           LocalWeapon(826, count=1, item_class=IClass.useful),  # Right-only (limited to 1)
        "Beno Protron System -B-":    LocalWeapon(827, count=1, item_class=IClass.useful),  # Right-only (limited to 1)
        "Tropical Cherry Companion":  LocalWeapon(828, count=2),
        "Satellite Marlo":            LocalWeapon(829, count=2),
        # ---------- TYRIAN 2000 LINE ----------
        "Bubble Gum-Gun":             LocalWeapon(830, count=0),
        "Flying Punch":               LocalWeapon(831, count=0, item_class=IClass.useful),
    }

    # ----------------------------------------------------------------------------------------------------------------

    nonprogressive_items: dict[str, LocalItem] = {
        "Advanced MR-12":        LocalItem(900, count=1, item_class=IClass.progression),
        "Gencore Custom MR-12":  LocalItem(901, count=1, item_class=IClass.progression),
        "Standard MicroFusion":  LocalItem(902, count=1, item_class=IClass.progression),
        "Advanced MicroFusion":  LocalItem(903, count=1, item_class=IClass.progression),
        "Gravitron Pulse-Wave":  LocalItem(904, count=1, item_class=IClass.progression),
    }

    progressive_items: dict[str, LocalItem] = {
        "Progressive Generator": LocalItem(905, count=5, item_class=IClass.progression),
    }

    bonus_games: dict[str, LocalItem] = {
        "Zinglon's Ale":         LocalItem(920, count=1),
        "Zinglon's Squadrons":   LocalItem(921, count=1),
        "Zinglon's Revenge":     LocalItem(922, count=1),
    }

    other_items: dict[str, LocalItem] = {
        "Maximum Power Up":      LocalItem(906, count=10, item_class=IClass.progression_skip_balancing),  # 1 -> 11
        "Armor Up":              LocalItem(907, count=9,  item_class=IClass.progression_skip_balancing),  # 5 -> 14
        "Shield Up":             LocalItem(908, count=9,  item_class=IClass.useful),  # 5 -> 14
        "Solar Shields":         LocalItem(909, count=1,  item_class=IClass.useful),

        "SuperBomb":             LocalItem(910, count=1),  # More can be added in junk fill

        # Goal collectible item for Data Cube Hunt mode
        "Data Cube":             LocalItem(911, item_class=IClass.progression_deprioritized_skip_balancing),

        # All Credits items have their count set dynamically.
        "50 Credits":            LocalItem(980),
        "75 Credits":            LocalItem(981),
        "100 Credits":           LocalItem(982),
        "150 Credits":           LocalItem(983),
        "200 Credits":           LocalItem(984),
        "300 Credits":           LocalItem(985),
        "375 Credits":           LocalItem(986),
        "500 Credits":           LocalItem(987),
        "750 Credits":           LocalItem(988),
        "800 Credits":           LocalItem(989),
        "1000 Credits":          LocalItem(990),
        "2000 Credits":          LocalItem(991),
        "5000 Credits":          LocalItem(992),
        "7500 Credits":          LocalItem(993),
        "10000 Credits":         LocalItem(994),
        "20000 Credits":         LocalItem(995),
        "40000 Credits":         LocalItem(996),
        "75000 Credits":         LocalItem(997),
        "100000 Credits":        LocalItem(998),
        "1000000 Credits":       LocalItem(999, item_class=IClass.useful),  # Should only be seen in case of emergency
    }

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def set_tyrian_2000_items(cls, enable: bool) -> None:
        # This feels like a kinda disgusting way to handle it, but it works...
        cls.front_ports["Needle Laser"].count = (1 if enable else 0)
        cls.front_ports["Pretzel Missile"].count = (1 if enable else 0)
        cls.front_ports["Dragon Frost"].count = (1 if enable else 0)
        cls.front_ports["Dragon Flame"].count = (1 if enable else 0)
        cls.rear_ports["People Pretzels"].count = (1 if enable else 0)
        cls.special_weapons["Super Pretzel"].count = (1 if enable else 0)
        cls.special_weapons["Dragon Lightning"].count = (1 if enable else 0)
        cls.sidekicks["Bubble Gum-Gun"].count = (2 if enable else 0)
        cls.sidekicks["Flying Punch"].count = (2 if enable else 0)

    @classmethod
    def get_item_name_to_id(cls, base_id: int) -> dict[str, int]:
        all_items = {}
        all_items.update({name: (base_id + item.local_id) for (name, item) in cls.levels.items()})
        all_items.update({name: (base_id + item.local_id) for (name, item) in cls.front_ports.items()})
        all_items.update({name: (base_id + item.local_id) for (name, item) in cls.rear_ports.items()})
        all_items.update({name: (base_id + item.local_id) for (name, item) in cls.special_weapons.items()})
        all_items.update({name: (base_id + item.local_id) for (name, item) in cls.sidekicks.items()})
        all_items.update({name: (base_id + item.local_id) for (name, item) in cls.nonprogressive_items.items()})
        all_items.update({name: (base_id + item.local_id) for (name, item) in cls.progressive_items.items()})
        all_items.update({name: (base_id + item.local_id) for (name, item) in cls.bonus_games.items()})
        all_items.update({name: (base_id + item.local_id) for (name, item) in cls.other_items.items()})
        return all_items

    @classmethod
    def get_item_groups(cls) -> dict[str, set[str]]:
        return {
            "Levels": {name for name in cls.levels.keys()},
            "Front Weapons": {name for name in cls.front_ports.keys()},
            "Rear Weapons": {name for name in cls.rear_ports.keys()},
            "Specials": {name for name in cls.special_weapons.keys()},
            "Sidekicks": {name for name in cls.sidekicks.keys()},
            "Generators": {"Progressive Generator", "Advanced MR-12", "Gencore Custom MR-12", "Standard MicroFusion",
                           "Advanced MicroFusion", "Gravitron Pulse-Wave"},
            "Credits": {name for name in cls.other_items.keys() if name.endswith(" Credits")}
        }

    @classmethod
    def get(cls, name: str) -> LocalItem:
        if name in cls.levels:               return cls.levels[name]
        if name in cls.front_ports:          return cls.front_ports[name]
        if name in cls.rear_ports:           return cls.rear_ports[name]
        if name in cls.special_weapons:      return cls.special_weapons[name]
        if name in cls.sidekicks:            return cls.sidekicks[name]
        if name in cls.nonprogressive_items: return cls.nonprogressive_items[name]
        if name in cls.progressive_items:    return cls.progressive_items[name]
        if name in cls.bonus_games:          return cls.bonus_games[name]
        if name in cls.other_items:          return cls.other_items[name]
        raise KeyError(f"Item {name} not found")

    # ================================================================================================================

    default_upgrade_costs: dict[str, UpgradeCost] = {
        # To upgrade a weapon to a specific level, multiply the cost by:
        # (0x, 1x, 4x, 10x, 20x, 35x, 56x, 84x, 120x, 165x, 220x)

        # Original is the values from the original game.
        # Balanced places the Pulse-Cannon at 800, and everything balanced around compared usefulness to that.

        # Front ports
        "Pulse-Cannon":                   UpgradeCost(original=500,  balanced=800),
        "Multi-Cannon (Front)":           UpgradeCost(original=750,  balanced=700),
        "Mega Cannon":                    UpgradeCost(original=1000, balanced=1000),
        "Laser":                          UpgradeCost(original=900,  balanced=1750),
        "Zica Laser":                     UpgradeCost(original=1100, balanced=1800),
        "Protron Z":                      UpgradeCost(original=900,  balanced=1250),
        "Vulcan Cannon (Front)":          UpgradeCost(original=600,  balanced=500),
        "Lightning Cannon":               UpgradeCost(original=1000, balanced=1250),
        "Protron (Front)":                UpgradeCost(original=600,  balanced=900),
        "Missile Launcher":               UpgradeCost(original=850,  balanced=600),
        "Mega Pulse (Front)":             UpgradeCost(original=900,  balanced=1000),
        "Heavy Missile Launcher (Front)": UpgradeCost(original=1000, balanced=1000),
        "Banana Blast (Front)":           UpgradeCost(original=950,  balanced=1000),
        "HotDog (Front)":                 UpgradeCost(original=1100, balanced=900),
        "Hyper Pulse":                    UpgradeCost(original=1050, balanced=850),
        "Guided Bombs":                   UpgradeCost(original=800,  balanced=800),
        "Shuriken Field":                 UpgradeCost(original=850,  balanced=950),
        "Poison Bomb":                    UpgradeCost(original=800,  balanced=1750),
        "Protron Wave":                   UpgradeCost(original=750,  balanced=500),
        "The Orange Juicer":              UpgradeCost(original=900,  balanced=900),
        "NortShip Super Pulse":           UpgradeCost(original=1100, balanced=1500),
        "Atomic RailGun":                 UpgradeCost(original=1101, balanced=1800),  # Yes, that's not a typo
        "Widget Beam":                    UpgradeCost(original=950,  balanced=500),
        "Sonic Impulse":                  UpgradeCost(original=1000, balanced=1000),
        "RetroBall":                      UpgradeCost(original=1000, balanced=600),

        # Rear ports
        "Starburst":                     UpgradeCost(original=900,  balanced=900),
        "Multi-Cannon (Rear)":           UpgradeCost(original=750,  balanced=700),
        "Sonic Wave":                    UpgradeCost(original=950,  balanced=1500),
        "Protron (Rear)":                UpgradeCost(original=650,  balanced=900),
        "Wild Ball":                     UpgradeCost(original=800,  balanced=800),
        "Vulcan Cannon (Rear)":          UpgradeCost(original=500,  balanced=500),
        "Fireball":                      UpgradeCost(original=1000, balanced=950),
        "Heavy Missile Launcher (Rear)": UpgradeCost(original=1000, balanced=1000),
        "Mega Pulse (Rear)":             UpgradeCost(original=900,  balanced=1250),
        "Banana Blast (Rear)":           UpgradeCost(original=1100, balanced=1500),
        "HotDog (Rear)":                 UpgradeCost(original=1100, balanced=700),
        "Guided Micro Bombs":            UpgradeCost(original=1100, balanced=800),
        "Heavy Guided Bombs":            UpgradeCost(original=1000, balanced=950),
        "Scatter Wave":                  UpgradeCost(original=900,  balanced=700),
        "NortShip Spreader":             UpgradeCost(original=1100, balanced=1250),
        "NortShip Spreader B":           UpgradeCost(original=1100, balanced=1250),

        # Tyrian 2000 stuff -- Original prices of 50 have been changed to 1000.
        # Front ports
        "Needle Laser":                  UpgradeCost(original=600,  balanced=750),
        "Pretzel Missile":               UpgradeCost(original=1000, balanced=900),
        "Dragon Frost":                  UpgradeCost(original=700,  balanced=900),
        "Dragon Flame":                  UpgradeCost(original=1000, balanced=1000),

        # Rear ports
        "People Pretzels":               UpgradeCost(original=1000, balanced=900),
    }
