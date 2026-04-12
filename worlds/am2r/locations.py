from typing import List, Optional, Callable, NamedTuple, TYPE_CHECKING
from BaseClasses import CollectionState
from .rules import AM2RLogic

if TYPE_CHECKING:
    from . import AM2RWorld
else:
    AM2RWorld = object


EventId: Optional[int] = None


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    game_id: int = 0
    rule: Callable[[CollectionState], bool] = lambda state: True

def get_location_datas(world: Optional[AM2RWorld], player: Optional[int]):
    location_table = [LocationData, ...]
    logic = AM2RLogic(world, player)

    location_table: List[LocationData] = [
        LocationData("Main Caves", "Main Caves: Spider Ball Challenge Upper",  108680000, 53, lambda state: logic.AM2R_can_fly(state) and logic.AM2R_can_bomb(state)),  # spider + bomb
        LocationData("Main Caves", "Main Caves: Spider Ball Challenge Lower",  108680001, 52, lambda state: state.has("Power Bomb", player, 3) or state.has("Bombs", player)),  # bomb
        LocationData("Main Caves", "Main Caves: Hi-Jump Challenge",  108680002, 57, lambda state: state.has_any({'Hi Jump', 'Space Jump'}, player) and logic.AM2R_can_bomb(state)),  # jump. just jump. ibj and dbj can come later in advanced logic frogtroll
        LocationData("Main Caves", "Main Caves: Spiky Maze",  108680003, 210),
        LocationData("Main Caves", "Main Caves: Shinespark Before The Pit",  108680004, 54, lambda state: state.has("Speed Booster", player)),  # speed
        LocationData("Main Caves", "Main Caves: Shinespark After The Pit",  108680005, 55, lambda state: state.has("Speed Booster", player)),  # speed

        LocationData("Golden Temple", "Golden Temple: Bombs",  108680006, 0),
        LocationData("Golden Temple", "Golden Temple: Below Bombs",  108680007, 100, logic.AM2R_can_bomb),  # bomb
        LocationData("Golden Temple", "Golden Temple: Hidden Energy Tank",  108680008, 103, logic.AM2R_can_bomb),  # bomb
        LocationData("Golden Temple", "Golden Temple: Charge Beam",  108680009, 10),
        LocationData("Golden Temple", "Golden Temple: Armory Left",  108680010, 104),
        LocationData("Golden Temple", "Golden Temple: Armory Upper",  108680011, 106),
        LocationData("Golden Temple", "Golden Temple: Armory Lower",  108680012, 105),
        LocationData("Golden Temple", "Golden Temple: Armory False Wall",  108680013, 107, logic.AM2R_can_bomb),  # bomb
        LocationData("Golden Temple", "Golden Temple: 3-Orb Hallway Left",  108680014, 101),
        LocationData("Golden Temple", "Golden Temple: 3-Orb Hallway Middle",  108680015, 108),
        LocationData("Golden Temple", "Golden Temple: 3-Orb Hallway Right",  108680016, 102),
        LocationData("Golden Temple", "Golden Temple: Spider Ball",  108680017, 2),
        LocationData("Golden Temple", "Golden Temple: Exterior Ceiling",  108680018, 109, lambda state: state.has("Speed Booster", player) or logic.AM2R_can_spider(state)),  # canspider
        LocationData("Golden Temple", "Golden Temple: EMP Room",  108680019, 110, lambda state: state.has("Super Missile", player) and logic.AM2R_has_ballspark(state) and logic.AM2R_can_bomb(state) and state.has("Screw Attack", player) and state.can_reach("EMP", "Region", player)),  # super + ballspark

        LocationData("Guardian", "Guardian: Up Above",  108680020, 111, lambda state: logic.AM2R_can_bomb(state) and ((logic.AM2R_can_schmove(state) and state.has("Bombs", player)) or logic.AM2R_can_fly(state))),  # bomb + schmove
        LocationData("Guardian", "Guardian: Behind The Door",  108680021, 112, lambda state: state.has("Power Bomb", player, 2) and ((logic.AM2R_can_spider(state)) or logic.AM2R_can_fly(state))),  # PB + schmove

        LocationData("Hydro Station", "Hydro Station: Cliff",  108680022, 163, lambda state: state.has("Speed Booster", player) or logic.AM2R_can_spider(state)),
        LocationData("Hydro Station", "Hydro Station: Side Morph Tunnel",  108680023, 152),
        LocationData("Hydro Station", "Hydro Station: Turbine Room",  108680024, 150, logic.AM2R_can_bomb),  # bomb
        LocationData("Hydro Station", "Hydro Station: Not so Secret Tunnel",  108680025, 151, logic.AM2R_can_schmove),  # schmove
        LocationData("Hydro Station", "Hydro Station: Water Pressure Pre-Varia",  108680026, 159, logic.AM2R_can_bomb),  # bomb
        LocationData("Hydro Station", "Hydro Station: Varia Suit",  108680027, 5, logic.AM2R_can_bomb),  # bomb
        LocationData("Hydro Station", "Hydro Station: EMP Room",  108680028, 162, lambda state: state.has("Super Missile", player) and state.has("Speed Booster", player) and state.can_reach("EMP", "Region", player)),  # super + speed

        LocationData("Arachnus", "Arachnus: Boss", 108680029, 3),

        LocationData("Inner Hydro Station", "Hydro Station: Wave Beam",  108680030, 12, logic.AM2R_can_bomb),
        LocationData("Inner Hydro Station", "Hydro Station: Below Tower Pipe Upper",  108680031, 153, lambda state: logic.AM2R_can_schmove(state) and logic.AM2R_can_bomb(state)),  # schmove
        LocationData("Inner Hydro Station", "Hydro Station: Below Tower Pipe Lower",  108680032, 154, logic.AM2R_can_bomb),
        LocationData("Inner Hydro Station", "Hydro Station: Dead End",  108680033, 155, logic.AM2R_can_bomb),
        LocationData("Inner Hydro Station", "Hydro Station: Hi-Jump Boots",  108680034, 4),
        LocationData("Inner Hydro Station", "Hydro Station: Behind Hi-Jump Boots Upper",  108680035, 156, lambda state: logic.AM2R_can_schmove(state) and logic.AM2R_can_bomb(state)),
        LocationData("Inner Hydro Station", "Hydro Station: Behind Hi-Jump Boots Lower",  108680036, 157, logic.AM2R_can_bomb),

        LocationData("Hydro Nest", "Hydro Nest: Below the Walkway",  108680037, 158, logic.AM2R_can_bomb),  # Bomb
        LocationData("Hydro Nest", "Hydro Nest: Speed Ceiling",  108680038, 161, lambda state: state.has("Speed Booster", player)),  # speed
        LocationData("Hydro Nest", "Hydro Nest: Behind The Wall",  108680039, 160, lambda state: state.has("Power Bomb", player) and state.has("Screw Attack", player) and state.has("Speed Booster", player)),  # PB + screw/speed

        LocationData("Industrial Complex Nest", "Industrial Complex: Above Save",  108680040, 214),
        LocationData("Industrial Complex Nest", "Industrial Complex: EMP Room",  108680041, 213, lambda state: state.has("Power Bomb", player) and state.has("Super Missile", player) and state.can_reach("EMP", "Region", player)),  # PB + super
        LocationData("Industrial Complex Nest", "Industrial Complex Nest: Nest Shinespark",  108680042, 209, lambda state: state.has("Super Missile", player) and state.has("Speed Booster", player) and logic.AM2R_can_schmove(state) and logic.AM2R_can_bomb(state)),  # super + schmove

        LocationData("Pre Industrial Complex", "Industrial Complex: In the Sand",  108680043, 211),
        LocationData("Pre Industrial Complex", "Industrial Complex: Complex Side After Tunnel",  108680044, 202, lambda state: (state.has("Speed Booster", player) or logic.AM2R_can_spider(state)) and logic.AM2R_can_bomb(state)),
        LocationData("Pre Industrial Complex", "Industrial Complex: Complex Side Tunnel",  108680045, 200, lambda state: state.has("Speed Booster", player) or logic.AM2R_can_spider(state)),
        LocationData("Pre Industrial Complex", "Industrial Complex: Behind the Green Door", 108680146, 212, lambda state: state.has("Speed Booster", player) and state.has("Power Bomb", player) and state.has("Super Missile", player) and logic.AM2R_can_spider(state)),
        LocationData("Pre Industrial Complex", "Industrial Complex: Save Room",  108680046, 203, lambda state: state.has("Speed Booster", player) or logic.AM2R_can_spider(state)),
        LocationData("Pre Industrial Complex", "Industrial Complex: Spazer Beam",  108680047, 13, lambda state: state.has("Speed Booster", player) or logic.AM2R_can_spider(state)),
        LocationData("Pre Industrial Complex", "Industrial Complex: Sisyphus Spark",  108680048, 204, lambda state: state.has("Speed Booster", player)),
        LocationData("Pre Industrial Complex", "Industrial Complex: Speed Booster",  108680049, 7, lambda state: (state.has("Speed Booster", player) or logic.AM2R_can_bomb(state)) and logic.AM2R_can_spider(state)),  # bomb

        LocationData("Torizo Ascended", "Torizo Ascended: Boss", 108680050, 6, logic.AM2R_can_schmove),

        LocationData("Industrial Complex", "Industrial Complex: Conveyor Belt Room",  108680051, 205, lambda state: state.has("Speed Booster", player)),
        LocationData("Industrial Complex", "Industrial Complex: Doom Treadmill",  108680052, 201, lambda state: state.has("Speed Booster", player) and logic.AM2R_can_bomb(state)),
        LocationData("Industrial Complex", "Industrial Complex: Complex Hub Shinespark",  108680053, 208, lambda state: state.has("Speed Booster", player) and logic.AM2R_can_bomb(state)),
        LocationData("Industrial Complex", "Industrial Complex: Complex Hub in the Floor", 108680054, 207, lambda state: state.has("Super Missile", player) and state.has("Speed Booster", player) and logic.AM2R_can_bomb(state)),
        LocationData("Industrial Complex", "Industrial Complex: Skippy Reward",  108680055, 206, lambda state: state.has("Super Missile", player) and state.has("Speed Booster", player) and logic.AM2R_can_bomb(state)),

        LocationData("GFS Thoth", "GFS Thoth: Research Camp",  108680056, 215),
        LocationData("GFS Thoth", "GFS Thoth: Hornoad Room",  108680057, 58, lambda state: state.has("Power Bomb", player)),
        LocationData("GFS Thoth", "GFS Thoth: Outside the Front of the Ship",  108680058, 59, lambda state: state.has("Power Bomb", player)),
        LocationData("Genesis", "Genesis: Boss",  108680059, 50, lambda state: state.has("Power Bomb", player, 2)),

        LocationData("The Tower", "The Tower: Beside Hydro Pipe",  108680060, 259, lambda state: state.has("Screw Attack", player)),
        LocationData("The Tower", "The Tower: Right Side of Tower",  108680061, 250),
        LocationData("The Tower", "The Tower: In the Ceiling",  108680062, 257, lambda state: logic.AM2R_can_bomb(state) and (state.has("Space Jump", player) or state.has("Spider Ball", player))),  # spider + bomb
        LocationData("The Tower", "The Tower: Dark Maze",  108680063, 252, lambda state: state.has("Power Bomb", player, 4) or state.has("Bombs", player) and state.has("Spider Ball", player)),  # bomb
        LocationData("The Tower", "The Tower: After Dark Maze",  108680064, 251, lambda state: state.has("Power Bomb", player, 4) or state.has("Bombs", player) and state.has("Spider Ball", player)),
        LocationData("The Tower", "The Tower: Plasma Beam",  108680065, 14, lambda state: logic.AM2R_can_bomb(state) and state.can_reach("Tester", "Region", player)),
        LocationData("The Tower", "The Tower: After Tester",  108680066, 256, lambda state: state.has("Power Bomb", player)),  # pb
        LocationData("The Tower", "The Tower: Outside Reactor",  108680067, 258, lambda state: state.has("Power Bomb", player)),  # pb

        LocationData("Geothermal", "The Tower: Geothermal Reactor",  108680068, 253, lambda state: state.has("Power Bomb", player) and state.has("Speed Booster", player) and logic.AM2R_can_schmove(state)),  # pb + speed + spider
        LocationData("Geothermal", "The Tower: Post Reactor Chozo",  108680069, 254, lambda state: state.has("Power Bomb", player, 3) and state.has("Speed Booster", player) and logic.AM2R_can_schmove(state)),  # pb
        LocationData("Geothermal", "The Tower: Post Reactor Shinespark",  108680070, 255, lambda state: state.has("Power Bomb", player, 3) and state.has("Speed Booster", player) and logic.AM2R_can_schmove(state) and state.has("Super Missile", player)),  # Pb + spped + super

        LocationData("Underwater Distribution Center", "Distribution Center: Main Room Shinespark",  108680071, 309, lambda state: state.has("Gravity Suit", player) and state.has("Speed Booster", player)),  # grav + screw
        LocationData("Underwater Distribution Center", "Distribution Center: Underwater Speed Hallway",  108680072, 307, lambda state: state.has("Speed Booster", player) and state.has("Gravity Suit", player)),  # speed + grav

        LocationData("EMP", "Distribution Center: After EMP Activation",  108680073, 300, lambda state: state.has("Screw Attack", player) and state.has("Speed Booster", player)),  # screw

        LocationData("Underwater Distro Connection", "Distribution Center: Spider Ball Crumble Spiky \"Maze\"",  108680074, 303, lambda state: state.has("Spider Ball", player) and state.has("Gravity Suit", player) and logic.AM2R_can_bomb(state)),  # spiderball underwater
        LocationData("Underwater Distro Connection", "Distribution Center: Before Spiky Trial",  108680075, 304),
        LocationData("Underwater Distro Connection", "Distribution Center: Spiky Trial Shinespark",  108680076, 305, lambda state: state.has("Gravity Suit", player) and state.has("Speed Booster", player)),  # grav + speed
        LocationData("Underwater Distro Connection", "Distribution Center: After Spiky Trial",  108680078, 306, lambda state: state.has("Power Bomb", player) and state.has("Speed Booster", player) and state.has("Gravity Suit", player) and state.has("Space Jump", player)),  # speed + grav + space + pb

        LocationData("Screw Attack", "Distribution Center: Screw Attack", 108680080, 8),
        LocationData("Pipe Hell Outside", "Distribution Center: Exterior Post-Gravity", 108680081, 302, lambda state: state.has("Power Bomb", player) and state.has("Space Jump", player) and state.has("Gravity Suit", player)),  # pb + space + grav
        LocationData("Pipe Hell R", "Distribution Center: Spectator Jail", 108680082, 301, lambda state: state.has("Power Bomb", player) and state.has("Speed Booster", player)),  # pb + speed

        LocationData("Gravity", "Distribution Center: Before Gravity", 108680083, 308, lambda state: (state.has("Bombs", player) and (state.has("Charge Beam", player) or state.has("Gravity Suit", player))) or state.has("Power Bomb", player)),  # bomb + charge/gravity / PB
        LocationData("Gravity", "Distribution Center: Gravity Suit", 108680084, 9, logic.AM2R_can_bomb),  # can bomb

        LocationData("Ice Beam", "Serris: Ice Beam", 108680085, 11, lambda state: state.has("Ice Beam", player) and (state.has("Super Missile", player) or state.has("Speed Booster", player))),  # speed / Supers

        LocationData("Deep Caves", "Deep Caves: Drivel Ballspark",  108680086, 56, lambda state: state.has("Gravity Suit", player) and logic.AM2R_has_ballspark(state)),
        LocationData("Deep Caves", "Deep Caves: Ramulken Lava Pool",  108680087, 60, lambda state: state.has("Gravity Suit", player) and logic.AM2R_can_bomb),

        LocationData("Deep Caves", "Deep Caves: After Omega",  108680088, 51),

        LocationData("Research Station", "The Last Metroid is in Captivity", EventId),

        LocationData("First Alpha", "The Forgotten Alpha", 108680100, 310),

        LocationData("Golden Temple", "Golden Temple: Friendly Spider", 108680101, 311,  lambda state: state.has("Speed Booster", player) or logic.AM2R_can_spider(state)),
        LocationData("Golden Temple Nest", "Golden Temple Nest: Moe", 108680102, 312, logic.AM2R_can_bomb),  # Loj
        LocationData("Golden Temple Nest", "Golden Temple Nest: Larry", 108680103, 313, logic.AM2R_can_bomb),    # Loj
        LocationData("Golden Temple Nest", "Golden Temple Nest: Curly", 108680104, 314, logic.AM2R_can_bomb),    # Loj

        LocationData("Main Caves", "Main Caves: Freddy Fazbear", 108680105, 315),  # Epsilon
        LocationData("Hydro Station", "Hydro Station: Turbine Terror", 108680106, 316),  # Xander
        LocationData("Hydro Station", "Hydro Station: The Lookout", 108680107, 318, lambda state: state.has("Speed Booster", player) or logic.AM2R_can_schmove(state)),  # Xander
        LocationData("Hydro Station", "Hydro Station: Recent Guardian", 108680108, 317),  # ANX

        LocationData("Hydro Nest", "Hydro Nest: EnderMahan", 108680109, 319),
        LocationData("Hydro Nest", "Hydro Nest: Carnage Awful", 108680110, 320),
        LocationData("Hydro Nest", "Hydro Nest: Venom Awesome", 108680111, 321),
        LocationData("Hydro Nest", "Hydro Nest: Something More, Something Awesome", 108680112, 322),

        LocationData("Industrial Complex Nest", "Industrial Nest: Mimolette", 108680113, 326, lambda state: state.has("Speed Booster", player) or state.has("Super Missile", player)),
        LocationData("Industrial Complex Nest", "Industrial Nest: The Big Cheese", 108680114, 327, lambda state: state.has("Speed Booster", player) or state.has("Super Missile", player)),
        LocationData("Industrial Complex Nest", "Industrial Nest: Mohwir", 108680115, 328, lambda state: logic.AM2R_can_bomb(state) and (state.has("Speed Booster", player) or state.has("Super Missile", player))),
        LocationData("Industrial Complex Nest", "Industrial Nest: Chirn", 108680116, 329, lambda state: logic.AM2R_can_bomb(state) and (state.has("Speed Booster", player) or state.has("Super Missile", player))),
        LocationData("Industrial Complex Nest", "Industrial Nest: BHHarbinger", 108680117, 330, lambda state: logic.AM2R_can_bomb(state) and logic.AM2R_can_schmove(state) and (state.has("Speed Booster", player) or state.has("Super Missile", player))),
        LocationData("Industrial Complex Nest", "Industrial Nest: AbyssalCreature", 108680118, 331, lambda state: logic.AM2R_can_bomb(state) and logic.AM2R_can_schmove(state) and (state.has("Speed Booster", player) or state.has("Super Missile", player))),

        LocationData("Pre Industrial Complex", "Industrial Complex: Sisyphus", 108680119, 323, logic.AM2R_can_spider),  # Mimo
        LocationData("Pre Industrial Complex", "Industrial Complex: And then there\'s this Asshole", 108680120, 332, logic.AM2R_can_spider),  # ANX

        LocationData("Industrial Complex", "Inside Industrial: Guardian of Doom Treadmill", 108680121, 324, lambda state: state.has("Speed Booster", player) and logic.AM2R_can_bomb(state)),
        LocationData("Industrial Complex", "Inside Industrial: Rawsome1234 by the Lava Lake", 108680122, 325, lambda state: state.has("Speed Booster", player) and logic.AM2R_can_bomb(state) and (state.has("Gravity Suit", player) or state.has("Space Jump", player))),

        LocationData("GFS Thoth", "Research Camp Dual Alphas: Marco", 108680123, 333),  # Epsilon
        LocationData("GFS Thoth", "Research Camp Dual Alphas: Polo", 108680124, 334),  # Epsilon

        LocationData("Mines", "Mines: Unga", 108680125, 335, lambda state: state.has("Super Missile", player) and logic.AM2R_can_bomb(state) and (state.has("Space Jump", player) or state.has("Spider Ball", player))),
        LocationData("Mines", "Mines: Gunga", 108680126, 336, lambda state: state.has("Super Missile", player) and logic.AM2R_can_bomb(state) and (state.has("Space Jump", player) or state.has("Spider Ball", player))),

        LocationData("The Tower", "The Tower: Patricia", 108680127, 337, logic.AM2R_can_fly),  # Mahan
        LocationData("The Tower", "The Tower: Variable \"GUH\"", 108680128, 338, logic.AM2R_can_spider),  # ANX
        LocationData("The Tower", "The Tower: Slagathor, the Ruler", 108680129, 340, lambda state: state.has("Power Bomb", player, 3) or state.has("Bombs", player)),  # Rawsome
        LocationData("The Tower", "The Tower: Mr.Sandman", 108680130, 339, lambda state: state.has("Space Jump", player) or state.has("Hi Jump", player) and state.has("Speed Booster", player)),  # Xander
        LocationData("The Tower", "The Tower: Anakin", 108680131, 341, lambda state: state.has("Space Jump", player)),  # Xander
        LocationData("The Tower", "The Tower: Xander", 108680132, 342, lambda state: state.has("Space Jump", player)),

        LocationData("Pipe Hell BL", "EMP: Sir Zeta Commander of the Alpha Squadron", 108680133, 343, logic.AM2R_can_bomb),  # Lucina

        LocationData("Pipe Hell R", "Distribution Center Alpha Squadron: Timmy", 108680134, 346),  # Lucina
        LocationData("Pipe Hell R", "Distribution Center Alpha Squadron: Tommy", 108680135, 345),  # Lucina
        LocationData("Pipe Hell R", "Distribution Center Alpha Squadron: Terry", 108680136, 348),  # Lucina
        LocationData("Pipe Hell R", "Distribution Center Alpha Squadron: Telly", 108680137, 347),  # Lucina
        LocationData("Pipe Hell R", "Distribution Center Alpha Squadron: Martin", 108680138, 344),

        LocationData("Underwater Distro Connection", "Distribution Center: Gamma Bros Mario", 108680139, 349),  # Lucina
        LocationData("Underwater Distro Connection", "Distribution Center: Gamma Bros Luigi", 108680140, 350),  # Lucina

        LocationData("Deep Caves", "Deep Caves: Lil\' Bro", 108680141, 351),
        LocationData("Deep Caves", "Deep Caves: Big Sis", 108680142, 352),
        LocationData("Omega Nest", "Omega Nest: SA-X Queen Lucina", 108680143, 355),
        LocationData("Omega Nest", "Omega Nest: Epsilon", 108680144, 354),
        LocationData("Omega Nest", "Omega Nest: Druid", 108680145, 353),
    ]

    return tuple(location_table)
