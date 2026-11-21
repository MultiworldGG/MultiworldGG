# from enum import IntFlag, auto
import math
from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder import rules

from worlds.ufo50.options import GolfariaStartWithBrakes, GolfariaDifficulty

if TYPE_CHECKING:
    from ... import UFO50World


# This would be a good way to rewrite and clean up this file
# basically turn it into a big list of rules to loop through instead of writing it out manually
#
# class Pow(IntFlag):
#     NONE = 0
#     BRAKES = auto()
#     BLOCK = auto()
#     SAND = auto()
#     WATER = auto()
#
#
# class DifficultyRules:
#     def __init__(self, strokes: int, powerups: int):
#         self.strokes: int = strokes
#         self.powerups: int = powerups
#
#
# class PowerupRules:
#
#     @staticmethod
#     # take items from the secondary list and add them to the primary if its powerup requirement differs
#     def merge_lists(primary: list[DifficultyRules], secondary: list[DifficultyRules]) -> list[DifficultyRules]:
#         items_to_add: list[DifficultyRules] = []
#         for rule_set2 in secondary:
#             for rule_set in primary:
#                 if rule_set2.powerups == rule_set.powerups:
#                     break
#             else:
#                 items_to_add.append(rule_set2)
#         return primary + items_to_add
#
#     easy: list[DifficultyRules]
#     medium: list[DifficultyRules]
#     hard: list[DifficultyRules]
#
#     def __init__(self, easy: DifficultyRules | list[DifficultyRules],
#                  medium: DifficultyRules | list[DifficultyRules],
#                  hard: DifficultyRules | list[DifficultyRules],
#                  hardcore=None):
#
#         self.easy = list(easy)
#
#         if medium:
#             self.medium = self.merge_lists(list(medium), self.easy)
#         else:
#             self.medium = self.easy
#
#         if hard:
#             self.hard = self.merge_lists(list(hard), self.medium)
#         else:
#             self.hard = self.medium
#
#         self.hardcore = hardcore
#
#
# rules_dict: dict[str, dict[str, PowerupRules]] = {
#     "Calm Cave": {
#         "Driver Depths Club": PowerupRules(
#             easy=[
#                 DifficultyRules(32, Pow.BRAKES),
#                 DifficultyRules(18, Pow.BLOCK)
#             ],
#             medium=DifficultyRules(22, Pow.BRAKES),
#             hard=DifficultyRules(17, Pow.BRAKES)
#         )
#     },
#
#     "Gur Grotto": {
#         "Mt Driver Parabot": PowerupRules(
#             easy=DifficultyRules(32, Pow.BRAKES),
#             medium=DifficultyRules(24, Pow.BRAKES),
#             hard=DifficultyRules(17, Pow.BRAKES)
#         ),
#         "Tee Temple Holy Tee": PowerupRules(
#             easy=DifficultyRules(8, Pow.BRAKES | Pow.WATER),
#             medium=[],
#             hard=[]
#         )
#     },
# }


def create_rules(world: "UFO50World", regions: dict[str, Region]) -> None:
    water = "Golfaria - Water Roll"
    sand = "Golfaria - Sand Roll"
    block = "Golfaria - Block Buster"
    club = "Golfaria - Club"
    brakes = "Golfaria - Brakes"

    brakestemp1 = [rules.OptionFilter(GolfariaStartWithBrakes, GolfariaStartWithBrakes.option_true)]
    brakestemp2 = rules.Has(brakes)
    hasbrakes = brakestemp1 | brakestemp2
    haswater = rules.Has(water)
    hassand = rules.Has(sand)
    hasblock = rules.Has(block)
    hastee = rules.Has("Golfaria - Tee 1") & rules.Has("Golfaria - Tee 2") & rules.Has("Golfaria - Tee 3") & rules.Has("Golfaria - Tee 4")
    hasnpc = rules.Has("Golfaria - Temple North NPC") & rules.Has("Golfaria - Temple East NPC") & rules.Has("Golfaria - Desert Cave NPC") & rules.Has("Golfaria - Water Save Cave NPC") & rules.Has("Golfaria - Water Cave NPC") & rules.Has("Golfaria - Lake Center NPC") & rules.Has("Golfaria - Im Lost NPC") & rules.Has("Golfaria - Sandman NPC")
    hasparbot = rules.Has(club, count=10)
    wise = rules.Has("Golfaria - Wise Ball's Cave Checkpoint") & rules.CanReachLocation("Golfaria - Wise Ball's Cave Checkpoint Location")
    calm = rules.Has("Golfaria - Calm Cave Checkpoint") & rules.CanReachLocation("Golfaria - Calm Cave Checkpoint Location")
    gur = rules.Has("Golfaria - Gur Grotto Checkpoint") & rules.CanReachLocation("Golfaria - Gur Grotto Checkpoint Location")
    rooted = rules.Has("Golfaria - Rooted Route Checkpoint") & rules.CanReachLocation("Golfaria - Rooted Route Checkpoint Location")
    tee = rules.Has("Golfaria - Tee Temple Checkpoint") & rules.CanReachLocation("Golfaria - Tee Temple Checkpoint Location")
    cave = rules.Has("Golfaria - Cave Town Checkpoint") & rules.CanReachLocation("Golfaria - Cave Town Checkpoint Location")
    downswing = rules.Has("Golfaria - Downswing Dip Checkpoint") & rules.CanReachLocation("Golfaria - Downswing Dip Checkpoint Location")
    winding = rules.Has("Golfaria - Winding Wetway Checkpoint") & rules.CanReachLocation("Golfaria - Winding Wetway Checkpoint Location")
    bunker = rules.Has("Golfaria - Bunker Below Checkpoint") & rules.CanReachLocation("Golfaria - Bunker Below Checkpoint Location")
    menu = regions["Menu"]
    start = regions["Start"]
    forest = regions["Forest"]
    temple = regions["Temple"]
    mountain = regions["Mountain"]
    desert = regions["Desert"]
    islands = regions["Islands"]
    water = regions["Water"]
    boss = regions["Boss"]

    handicap = float((100 + 10 * world.options.golfaria_handicap) / 100)
    difficulty = world.options.golfaria_difficulty

    menu.connect(start)
    start.connect(forest)
    forest.connect(temple)
    temple.connect(mountain)
    start.connect(desert)
    start.connect(islands)
    start.connect(water)

    # def clubs_needed(amount: int, handi: bool = False) -> rules.Has:
    #     if handi:
    #         return rules.Has(club, count=math.ceil(((amount * handicap) - 20) / 3))
    #     return rules.Has(club, count=amount)
    #
    # this would be part of the rewrite if it happens
    # def get_powerup_rule_from_flags(powerups: int):
    #     flag_rules: list[rules.Rule] = []
    #     if Pow.BRAKES in powerups:
    #         flag_rules.append(hasbrakes)
    #     if Pow.BLOCK in powerups:
    #         flag_rules.append(hasblock)
    #     if Pow.SAND in powerups:
    #         flag_rules.append(hassand)
    #     if Pow.WATER in powerups:
    #         flag_rules.append(haswater)
    #     return flag_rules
    #
    # for origin, destinations in rules_dict.items():
    #     for destination, dest_rules in destinations.items():
    #         if difficulty == GolfariaDifficulty.easy:
    #             rule_list = [
    #                 (clubs_needed(rule.strokes) & get_powerup_rule_from_flags(rule.powerups))
    #                 for rule in dest_rules.easy
    #             ]
    #             world.add_rule(world.get_location(f"Golfaria - {destination}"), any(rule_list))

    clubsneeded = rules.Has(club, count=math.ceil(((53 * handicap) - 20) / 3))
    temprule = hasbrakes & hasblock & hassand & haswater & hastee & clubsneeded
    world.create_entrance(temple, boss, temprule)
    clubsneeded = rules.Has(club, count=20)
    temprule = hasbrakes & hasblock & hassand & haswater & hastee & hasparbot & hasnpc & clubsneeded
    if "Golfaria" in world.options.cherry_allowed_games:
        world.set_rule(world.get_location("Golfaria - Cherry"), temprule)
    if difficulty == 1:
        world.set_rule(world.get_location("Golfaria - Calm Cave Checkpoint Location"), hasbrakes)
        world.set_rule(world.get_location("Golfaria - Gur Grotto Checkpoint Location"), hasbrakes)
        world.set_rule(world.get_location("Golfaria - Rooted Route Checkpoint Location"), hasbrakes)
        temprule = hasbrakes & hasblock
        world.set_rule(world.get_location("Golfaria - Tee Temple Checkpoint Location"), temprule)
        clubsneeded = rules.Has(club, count=math.ceil(((32 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((30 * handicap) - 20) / 3))
        caverule1 = hasbrakes & clubsneeded
        caverule2 = hasblock
        caverule3 = calm & hasbrakes & clubsneeded3
        caverule4 = caverule1 | caverule2 | caverule3
        world.set_rule(world.get_location("Golfaria - Cave Town Checkpoint Location"), caverule4)
        world.set_rule(world.get_location("Golfaria - Downswing Dip Checkpoint Location"), hasbrakes)
        temprule = hasbrakes & hasblock
        temprule2 = temprule | haswater
        world.set_rule(world.get_location("Golfaria - Winding Wetway Checkpoint Location"), temprule2)
        clubsneeded = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & hassand & clubsneeded
        world.set_rule(world.get_location("Golfaria - Bunker Below Checkpoint Location"), temprule)
        clubsneeded = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        temprule = clubsneeded
        temprule2 = haswater & clubsneeded2
        temprule3 = wise & clubsneeded3
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Brakes Location"), temprule4)
        clubsneeded = rules.Has(club, count=math.ceil(((23 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((22 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((19 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = calm & hasbrakes & clubsneeded2
        temprule3 = gur & hasbrakes & clubsneeded3
        temprule4 = rooted & hasbrakes & clubsneeded4
        temprule5 = tee & hasbrakes & hasblock & clubsneeded5
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Block Buster Location"), temprule6)
        world.set_rule(world.get_location("Golfaria - Garden"), temprule6)
        clubsneeded = rules.Has(club, count=math.ceil(((32 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((26 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        clubsneeded6 = rules.Has(club, count=math.ceil(((23 * handicap) - 20) / 3))
        clubsneeded7 = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = hasbrakes & haswater & clubsneeded2
        temprule3 = wise & hasbrakes & hassand & haswater & clubsneeded3
        temprule4 = downswing & hasbrakes & hasblock & clubsneeded4
        temprule5 = downswing & hasbrakes & haswater & clubsneeded5
        temprule6 = winding & hasbrakes & clubsneeded6
        temprule7 = bunker & hasbrakes & hassand & clubsneeded7
        temprule8 = temprule | temprule2 | temprule3 | temprule4 | temprule5 | temprule6 | temprule7
        world.set_rule(world.get_location("Golfaria - Sand Roll Location"), temprule8)
        clubsneeded = rules.Has(club, count=math.ceil(((40 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((26 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & hassand & clubsneeded
        temprule2 = hasbrakes & hassand & haswater
        temprule3 = bunker & hasbrakes & hassand & clubsneeded3
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Water Roll Location"), temprule4)
        clubsneeded = rules.Has(club, count=math.ceil(((22 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = cave & hasbrakes & hasblock & clubsneeded2
        temprule3 = temprule | temprule2
        world.set_rule(world.get_location("Golfaria - Crumbling Cut Tee"), temprule3)
        clubsneeded = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = haswater & clubsneeded
        temprule2 = hassand & haswater & clubsneeded2
        temprule3 = wise & haswater
        temprule4 = downswing & haswater
        temprule5 = winding & haswater
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Water-Wedge Way Tee"), temprule6)
        world.set_rule(world.get_location("Golfaria - Sandy Subterra Tee"), hasbrakes)
        clubsneeded = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & haswater & clubsneeded
        temprule2 = calm & hasbrakes & haswater
        temprule3 = gur & hasbrakes & haswater
        temprule4 = tee & hasbrakes & haswater
        temprule5 = temprule | temprule2 | temprule3 | temprule4
        world.set_rule(world.get_location("Golfaria - Tee Temple Tee"), temprule5)
        world.set_rule(world.get_location("Golfaria - Underputt Club 2"), haswater)
        clubsneeded = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = wise & clubsneeded2
        temprule3 = downswing
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Downswing Dip Club"), temprule4)
        clubsneeded = rules.Has(club, count=math.ceil(((19 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = hasbrakes & hasblock & hassand & clubsneeded2
        temprule3 = wise & hasbrakes & hasblock
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Up N Over Cove Club"), temprule4)
        world.set_rule(world.get_location("Golfaria - Gritty Grip Grotto Club"), hassand)
        world.set_rule(world.get_location("Golfaria - Moebius Hole Club"), hasblock)
        world.set_rule(world.get_location("Golfaria - Rooted Route Blocked Club"), hasblock)
        world.set_rule(world.get_location("Golfaria - Rooted Route Sand Roll Club"), hassand)
        world.set_rule(world.get_location("Golfaria - Rooted Route Water Roll Club"), haswater)
        world.set_rule(world.get_location("Golfaria - Tee Temple Club 1"), hasbrakes)
        clubsneeded = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = calm & hasbrakes & clubsneeded2
        temprule3 = gur & hasbrakes
        temprule4 = rooted & hasbrakes & clubsneeded4
        temprule5 = tee & hasbrakes & hasblock
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Tee Temple Club 2"), temprule6)
        world.set_rule(world.get_location("Golfaria - Gur Grotto Club 1"), hasbrakes)
        clubsneeded = rules.Has(club, count=math.ceil(((31 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((29 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((24 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = calm & hasbrakes & hasblock & clubsneeded2
        temprule3 = gur & hasbrakes & hasblock & clubsneeded3
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Mulligan Caverns Club"), temprule4)
        temprule = hasbrakes | hasblock | haswater
        world.set_rule(world.get_location("Golfaria - Calm Cave Club"), temprule)
        clubsneeded = rules.Has(club, count=math.ceil(((34 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((32 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((23 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = hasblock & clubsneeded2
        temprule3 = calm & hasbrakes & clubsneeded3
        temprule4 = calm & hasblock & clubsneeded4
        temprule5 = gur & hasbrakes & clubsneeded5
        temprule6 = cave & hasbrakes
        temprule7 = temprule | temprule2 | temprule3 | temprule4 | temprule5 | temprule6
        world.set_rule(world.get_location("Golfaria - Driver Depths Club"), temprule7)
        clubsneeded = rules.Has(club, count=math.ceil(((34 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & hassand & clubsneeded
        world.set_rule(world.get_location("Golfaria - Wormburn Way Club"), temprule)
        clubsneeded2 = rules.Has(club, count=math.ceil(((40 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((34 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((30 * handicap) - 20) / 3))
        temprule = hasbrakes & haswater
        temprule2 = hasbrakes & hasblock & clubsneeded2
        temprule3 = downswing & hasbrakes & hasblock & clubsneeded3
        temprule4 = winding & hasbrakes & clubsneeded4
        temprule5 = temprule | temprule2 | temprule3 | temprule4
        world.set_rule(world.get_location("Golfaria - Winding Wetway Club"), temprule5)
        world.set_rule(world.get_location("Golfaria - South Green Parbot"), hasbrakes)
        world.set_rule(world.get_location("Golfaria - North Green Parbot"), hasbrakes)
        clubsneeded = rules.Has(club, count=math.ceil(((34 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((32 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((27 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = hasbrakes & hasblock
        temprule3 = calm & hasbrakes & clubsneeded3
        temprule4 = gur & hasbrakes & clubsneeded4
        temprule5 = cave & hasbrakes
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Mt Driver Parbot"), temprule6)
        clubsneeded = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & hassand & clubsneeded
        temprule2 = bunker & hasbrakes & hassand
        temprule3 = temprule | temprule2
        world.set_rule(world.get_location("Golfaria - Bunker Dunes Parbot 2"), temprule3)
        clubsneeded = rules.Has(club, count=math.ceil(((14 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = hasbrakes & haswater
        temprule3 = downswing & hasbrakes & hasblock
        temprule4 = winding & hasbrakes
        temprule5 = temprule | temprule2 | temprule3 | temprule4
        world.set_rule(world.get_location("Golfaria - Up And Down Isle Parbot"), temprule5)
        world.set_rule(world.get_location("Golfaria - Arc Archipelago Parbot"), haswater)
        world.set_rule(world.get_location("Golfaria - Underputt Parbot"), haswater)
        clubsneeded = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        temprule = hasblock & haswater & clubsneeded
        temprule2 = wise & hasblock & haswater
        temprule3 = temprule | temprule2
        world.set_rule(world.get_location("Golfaria - Up N Over Cove NPC"), temprule3)
        temprule = hasbrakes & haswater
        world.set_rule(world.get_location("Golfaria - Winding Wetway NPC"), temprule)
        clubsneeded = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = hasbrakes & hasblock
        temprule3 = calm & hasbrakes & clubsneeded3
        temprule4 = gur & hasbrakes
        temprule5 = temprule | temprule2 | temprule3 | temprule4
        world.set_rule(world.get_location("Golfaria - East Temple NPC"), temprule5)
        world.set_rule(world.get_location("Golfaria - Sandy Subterra NPC"), hasbrakes)
        temprule = hasbrakes & hassand
        world.set_rule(world.get_location("Golfaria - Sandy Sinkhole B NPC"), temprule)
        world.set_rule(world.get_location("Golfaria - Ocean Pit NPC"), haswater)

    if difficulty == GolfariaDifficulty.option_medium:
        world.set_rule(world.get_location("Golfaria - Calm Cave Checkpoint Location"), hasbrakes)
        world.set_rule(world.get_location("Golfaria - Rooted Route Checkpoint Location"), hasbrakes)
        temprule = hasbrakes & hasblock
        world.set_rule(world.get_location("Golfaria - Tee Temple Checkpoint Location"), temprule)
        clubsneeded = rules.Has(club, count=math.ceil(((22 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        caverule1 = hasbrakes & clubsneeded
        caverule2 = hasblock
        caverule3 = calm & hasbrakes & clubsneeded3
        caverule4 = caverule1 | caverule2 | caverule3
        world.set_rule(world.get_location("Golfaria - Cave Town Checkpoint Location"), caverule4)
        temprule = hasbrakes & hasblock
        temprule2 = haswater
        temprule3 = hasbrakes & hassand
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Winding Wetway Checkpoint Location"), temprule4)
        clubsneeded = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & hassand & clubsneeded
        world.set_rule(world.get_location("Golfaria - Bunker Below Checkpoint Location"), temprule)
        clubsneeded = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        temprule = clubsneeded
        temprule2 = haswater & clubsneeded2
        temprule3 = wise & clubsneeded3
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Brakes Location"), temprule4)
        clubsneeded = rules.Has(club, count=math.ceil(((23 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((22 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((19 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = calm & hasbrakes & clubsneeded2
        temprule3 = gur & hasbrakes & clubsneeded3
        temprule4 = rooted & hasbrakes & clubsneeded4
        temprule5 = tee & hasbrakes & hasblock & clubsneeded5
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Block Buster Location"), temprule6)
        world.set_rule(world.get_location("Golfaria - Garden"), temprule6)
        clubsneeded = rules.Has(club, count=math.ceil(((32 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((26 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        clubsneeded6 = rules.Has(club, count=math.ceil(((23 * handicap) - 20) / 3))
        clubsneeded7 = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        clubsneeded8 = rules.Has(club, count=math.ceil(((28 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = hasbrakes & haswater & clubsneeded2
        temprule3 = wise & hasbrakes & hassand & haswater & clubsneeded3
        temprule4 = downswing & hasbrakes & hasblock & clubsneeded4
        temprule5 = downswing & hasbrakes & haswater & clubsneeded5
        temprule6 = winding & hasbrakes & clubsneeded6
        temprule7 = bunker & hasbrakes & hassand & clubsneeded7
        temprule8 = hasbrakes & hassand & clubsneeded8
        temprule9 = temprule | temprule2 | temprule3 | temprule4 | temprule5 | temprule6 | temprule7 | temprule8
        world.set_rule(world.get_location("Golfaria - Sand Roll Location"), temprule9)
        clubsneeded = rules.Has(club, count=math.ceil(((40 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((26 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & hassand & clubsneeded
        temprule2 = hasbrakes & hassand & haswater
        temprule3 = bunker & hasbrakes & hassand & clubsneeded3
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Water Roll Location"), temprule4)
        clubsneeded = rules.Has(club, count=math.ceil(((22 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = cave & hasbrakes & hasblock & clubsneeded2
        temprule3 = temprule | temprule2
        world.set_rule(world.get_location("Golfaria - Crumbling Cut Tee"), temprule3)
        temprule = haswater
        world.set_rule(world.get_location("Golfaria - Water-Wedge Way Tee"), temprule)
        world.set_rule(world.get_location("Golfaria - Sandy Subterra Tee"), hasbrakes)
        clubsneeded = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & haswater & clubsneeded
        temprule2 = calm & hasbrakes & haswater
        temprule3 = gur & hasbrakes & haswater
        temprule4 = tee & hasbrakes & haswater
        temprule5 = temprule | temprule2 | temprule3 | temprule4
        world.set_rule(world.get_location("Golfaria - Tee Temple Tee"), temprule5)
        world.set_rule(world.get_location("Golfaria - Underputt Club 2"), haswater)
        clubsneeded = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        world.set_rule(world.get_location("Golfaria - Downswing Dip Club"), clubsneeded)
        clubsneeded = rules.Has(club, count=math.ceil(((19 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = hasbrakes & hassand & clubsneeded2
        temprule3 = wise & hasbrakes
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Up N Over Cove Club"), temprule4)
        world.set_rule(world.get_location("Golfaria - Gritty Grip Grotto Club"), hassand)
        world.set_rule(world.get_location("Golfaria - Moebius Hole Club"), hasblock)
        world.set_rule(world.get_location("Golfaria - Rooted Route Blocked Club"), hasblock)
        world.set_rule(world.get_location("Golfaria - Rooted Route Sand Roll Club"), hassand)
        world.set_rule(world.get_location("Golfaria - Rooted Route Water Roll Club"), haswater)
        world.set_rule(world.get_location("Golfaria - Tee Temple Club 1"), hasbrakes)
        clubsneeded = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = calm & hasbrakes & clubsneeded2
        temprule3 = gur & hasbrakes
        temprule4 = rooted & hasbrakes & clubsneeded4
        temprule5 = tee & hasbrakes & hasblock
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Tee Temple Club 2"), temprule6)
        clubsneeded = rules.Has(club, count=math.ceil(((29 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((27 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = calm & hasbrakes & hasblock & clubsneeded2
        temprule3 = gur & hasbrakes & hasblock & clubsneeded3
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Mulligan Caverns Club"), temprule4)
        temprule = hasbrakes | hasblock | haswater
        world.set_rule(world.get_location("Golfaria - Calm Cave Club"), temprule)
        clubsneeded = rules.Has(club, count=math.ceil(((24 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((22 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = hasblock & clubsneeded2
        temprule3 = calm & hasbrakes & clubsneeded3
        temprule4 = calm & hasblock & clubsneeded4
        temprule5 = gur & hasbrakes & clubsneeded5
        temprule6 = cave & hasbrakes
        temprule7 = temprule | temprule2 | temprule3 | temprule4 | temprule5 | temprule6
        world.set_rule(world.get_location("Golfaria - Driver Depths Club"), temprule7)
        clubsneeded2 = rules.Has(club, count=math.ceil(((40 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((34 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((30 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((42 * handicap) - 20) / 3))
        temprule = hasbrakes & haswater
        temprule2 = hasbrakes & hasblock & clubsneeded2
        temprule3 = downswing & hasbrakes & hasblock & clubsneeded3
        temprule4 = winding & hasbrakes & clubsneeded4
        temprule5 = hasbrakes & hassand & clubsneeded5
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Winding Wetway Club"), temprule6)
        world.set_rule(world.get_location("Golfaria - South Green Parbot"), hasbrakes)
        world.set_rule(world.get_location("Golfaria - North Green Parbot"), hasbrakes)
        clubsneeded = rules.Has(club, count=math.ceil(((26 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((24 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((22 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = hasbrakes & hasblock
        temprule3 = calm & hasbrakes & clubsneeded3
        temprule4 = gur & hasbrakes & clubsneeded4
        temprule5 = cave & hasbrakes
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Mt Driver Parbot"), temprule6)
        clubsneeded = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & hassand & clubsneeded
        temprule2 = bunker & hasbrakes & hassand
        temprule3 = temprule | temprule2
        world.set_rule(world.get_location("Golfaria - Bunker Dunes Parbot 2"), temprule3)
        clubsneeded = rules.Has(club, count=math.ceil(((14 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = hasbrakes & haswater
        temprule3 = downswing & hasbrakes & hasblock
        temprule4 = winding & hasbrakes
        temprule5 = hasbrakes & hassand & clubsneeded5
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Up And Down Isle Parbot"), temprule6)
        world.set_rule(world.get_location("Golfaria - Arc Archipelago Parbot"), haswater)
        world.set_rule(world.get_location("Golfaria - Underputt Parbot"), haswater)
        clubsneeded = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        temprule = hasblock & haswater & clubsneeded
        temprule2 = wise & hasblock & haswater
        temprule3 = temprule | temprule2
        world.set_rule(world.get_location("Golfaria - Up N Over Cove NPC"), temprule3)
        temprule = hasbrakes & haswater
        world.set_rule(world.get_location("Golfaria - Winding Wetway NPC"), temprule)
        clubsneeded3 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        temprule = hasbrakes
        temprule2 = hasbrakes & hasblock
        temprule3 = calm & hasbrakes & clubsneeded3
        temprule4 = gur & hasbrakes
        temprule5 = temprule | temprule2 | temprule3 | temprule4
        world.set_rule(world.get_location("Golfaria - East Temple NPC"), temprule5)
        world.set_rule(world.get_location("Golfaria - Sandy Subterra NPC"), hasbrakes)
        temprule = hasbrakes & hassand
        world.set_rule(world.get_location("Golfaria - Sandy Sinkhole B NPC"), temprule)
        world.set_rule(world.get_location("Golfaria - Ocean Pit NPC"), haswater)

    if difficulty == GolfariaDifficulty.option_hard:
        temprule = hasbrakes & hasblock
        world.set_rule(world.get_location("Golfaria - Tee Temple Checkpoint Location"), temprule)
        clubsneeded = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        caverule1 = hasbrakes & clubsneeded
        caverule2 = hasblock
        caverule3 = calm & hasbrakes & clubsneeded3
        caverule4 = caverule1 | caverule2 | caverule3
        world.set_rule(world.get_location("Golfaria - Cave Town Checkpoint Location"), caverule4)
        clubsneeded4 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock
        temprule2 = haswater
        temprule3 = hasbrakes & hassand
        temprule4 = hasbrakes & clubsneeded4
        temprule5 = temprule | temprule2 | temprule3 | temprule4
        world.set_rule(world.get_location("Golfaria - Winding Wetway Checkpoint Location"), temprule5)
        clubsneeded = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((28 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & hassand & clubsneeded
        temprule2 = hasbrakes & clubsneeded2
        temprule3 = hasbrakes & hassand & clubsneeded3
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Bunker Below Checkpoint Location"), temprule4)
        clubsneeded = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        temprule = clubsneeded
        temprule2 = haswater & clubsneeded2
        temprule3 = wise & clubsneeded3
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Brakes Location"), temprule4)
        clubsneeded = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((19 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((12 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = calm & hasbrakes & clubsneeded2
        temprule3 = gur & hasbrakes & clubsneeded3
        temprule4 = rooted & hasbrakes & clubsneeded4
        temprule5 = tee & hasbrakes & hasblock & clubsneeded5
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Block Buster Location"), temprule6)
        world.set_rule(world.get_location("Golfaria - Garden"), temprule6)
        clubsneeded = rules.Has(club, count=math.ceil(((32 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((26 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        clubsneeded6 = rules.Has(club, count=math.ceil(((23 * handicap) - 20) / 3))
        clubsneeded7 = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        clubsneeded8 = rules.Has(club, count=math.ceil(((28 * handicap) - 20) / 3))
        clubsneeded9 = rules.Has(club, count=math.ceil(((26 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = hasbrakes & haswater & clubsneeded2
        temprule3 = wise & hasbrakes & hassand & haswater & clubsneeded3
        temprule4 = downswing & hasbrakes & hasblock & clubsneeded4
        temprule5 = downswing & hasbrakes & haswater & clubsneeded5
        temprule6 = winding & hasbrakes & clubsneeded6
        temprule7 = bunker & hasbrakes & hassand & clubsneeded7
        temprule8 = hasbrakes & hassand & clubsneeded8
        temprule9 = wise & hasbrakes & hassand & clubsneeded9
        temprule10 = temprule | temprule2 | temprule3 | temprule4 | temprule5 | temprule6 | temprule7 | temprule8 | temprule9
        world.set_rule(world.get_location("Golfaria - Sand Roll Location"), temprule10)
        clubsneeded = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((26 * handicap) - 20) / 3))
        temprule = hasbrakes & hassand & clubsneeded
        temprule2 = hasbrakes & hassand & haswater
        temprule3 = bunker & hasbrakes & hassand & clubsneeded3
        temprule4 = cave & hasbrakes & hassand
        temprule5 = temprule | temprule2 | temprule3 | temprule4
        world.set_rule(world.get_location("Golfaria - Water Roll Location"), temprule5)
        clubsneeded = rules.Has(club, count=math.ceil(((22 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = cave & hasbrakes & hasblock & clubsneeded2
        temprule3 = temprule | temprule2
        world.set_rule(world.get_location("Golfaria - Crumbling Cut Tee"), temprule3)
        temprule = haswater
        world.set_rule(world.get_location("Golfaria - Water-Wedge Way Tee"), temprule)
        world.set_rule(world.get_location("Golfaria - Sandy Subterra Tee"), hasbrakes)
        clubsneeded = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & haswater & clubsneeded
        temprule2 = calm & hasbrakes & haswater
        temprule3 = gur & hasbrakes & haswater
        temprule4 = tee & hasbrakes & haswater
        temprule5 = temprule | temprule2 | temprule3 | temprule4
        world.set_rule(world.get_location("Golfaria - Tee Temple Tee"), temprule5)
        world.set_rule(world.get_location("Golfaria - Underputt Club 2"), haswater)
        clubsneeded = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        world.set_rule(world.get_location("Golfaria - Downswing Dip Club"), clubsneeded)
        clubsneeded = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        temprule = clubsneeded
        temprule2 = hassand & clubsneeded2
        temprule3 = wise
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Up N Over Cove Club"), temprule4)
        world.set_rule(world.get_location("Golfaria - Gritty Grip Grotto Club"), hassand)
        world.set_rule(world.get_location("Golfaria - Moebius Hole Club"), hasblock)
        world.set_rule(world.get_location("Golfaria - Rooted Route Blocked Club"), hasblock)
        world.set_rule(world.get_location("Golfaria - Rooted Route Water Roll Club"), haswater)
        world.set_rule(world.get_location("Golfaria - Tee Temple Club 1"), hasbrakes)
        clubsneeded = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = calm & hasbrakes & clubsneeded2
        temprule3 = gur & hasbrakes
        temprule4 = rooted & hasbrakes & clubsneeded4
        temprule5 = tee & hasbrakes & hasblock
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Tee Temple Club 2"), temprule6)
        clubsneeded = rules.Has(club, count=math.ceil(((24 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((22 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((19 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = calm & hasbrakes & hasblock & clubsneeded2
        temprule3 = gur & hasbrakes & hasblock & clubsneeded3
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Mulligan Caverns Club"), temprule4)
        clubsneeded = rules.Has(club, count=math.ceil(((19 * handicap) - 20) / 3))
        clubsneeded2 = rules.Has(club, count=math.ceil(((15 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((18 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((14 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = hasblock & clubsneeded2
        temprule3 = calm & hasbrakes & clubsneeded3
        temprule4 = calm & hasblock & clubsneeded4
        temprule5 = gur & hasbrakes & clubsneeded5
        temprule6 = cave & hasbrakes
        temprule7 = temprule | temprule2 | temprule3 | temprule4 | temprule5 | temprule6
        world.set_rule(world.get_location("Golfaria - Driver Depths Club"), temprule7)
        clubsneeded2 = rules.Has(club, count=math.ceil(((30 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((24 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((37 * handicap) - 20) / 3))
        clubsneeded6 = rules.Has(club, count=math.ceil(((25 * handicap) - 20) / 3))
        temprule = hasbrakes & haswater
        temprule2 = hasbrakes & hasblock & clubsneeded2
        temprule3 = downswing & hasbrakes & hasblock & clubsneeded3
        temprule4 = winding & hasbrakes & clubsneeded4
        temprule5 = hasbrakes & clubsneeded5
        temprule6 = wise & hasbrakes & hassand & clubsneeded6
        temprule7 = temprule | temprule2 | temprule3 | temprule4 | temprule5 | temprule6
        world.set_rule(world.get_location("Golfaria - Winding Wetway Club"), temprule7)
        clubsneeded = rules.Has(club, count=math.ceil(((19 * handicap) - 20) / 3))
        clubsneeded3 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        clubsneeded4 = rules.Has(club, count=math.ceil(((17 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = hasbrakes & hasblock
        temprule3 = calm & hasbrakes & clubsneeded3
        temprule4 = gur & hasbrakes & clubsneeded4
        temprule5 = cave & hasbrakes
        temprule6 = temprule | temprule2 | temprule3 | temprule4 | temprule5
        world.set_rule(world.get_location("Golfaria - Mt Driver Parbot"), temprule6)
        clubsneeded = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        temprule = hasbrakes & clubsneeded
        temprule2 = bunker & hasbrakes & hassand
        temprule3 = hasbrakes & hassand
        temprule4 = temprule | temprule2 | temprule3
        world.set_rule(world.get_location("Golfaria - Bunker Dunes Parbot 2"), temprule4)
        clubsneeded = rules.Has(club, count=math.ceil(((14 * handicap) - 20) / 3))
        clubsneeded5 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        clubsneeded6 = rules.Has(club, count=math.ceil(((21 * handicap) - 20) / 3))
        temprule = hasbrakes & hasblock & clubsneeded
        temprule2 = hasbrakes & haswater
        temprule3 = downswing & hasbrakes & hasblock
        temprule4 = winding & hasbrakes
        temprule5 = hasbrakes & hassand & clubsneeded5
        temprule6 = hasbrakes & clubsneeded6
        temprule7 = wise & hasbrakes & hassand
        temprule8 = temprule | temprule2 | temprule3 | temprule4 | temprule5 | temprule6 | temprule7
        world.set_rule(world.get_location("Golfaria - Up And Down Isle Parbot"), temprule8)
        world.set_rule(world.get_location("Golfaria - Arc Archipelago Parbot"), haswater)
        world.set_rule(world.get_location("Golfaria - Underputt Parbot"), haswater)
        clubsneeded = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        temprule = hasblock & haswater & clubsneeded
        temprule2 = wise & hasblock & haswater
        temprule3 = temprule | temprule2
        world.set_rule(world.get_location("Golfaria - Up N Over Cove NPC"), temprule3)
        temprule = hasbrakes & haswater
        world.set_rule(world.get_location("Golfaria - Winding Wetway NPC"), temprule)
        clubsneeded3 = rules.Has(club, count=math.ceil(((16 * handicap) - 20) / 3))
        temprule = hasbrakes
        temprule2 = hasbrakes & hasblock
        temprule3 = calm & hasbrakes & clubsneeded3
        temprule4 = gur & hasbrakes
        temprule5 = temprule | temprule2 | temprule3 | temprule4
        world.set_rule(world.get_location("Golfaria - East Temple NPC"), temprule5)
        world.set_rule(world.get_location("Golfaria - Sandy Subterra NPC"), hasbrakes)
        clubsneeded2 = rules.Has(club, count=math.ceil(((20 * handicap) - 20) / 3))
        temprule = hasbrakes & hassand
        temprule2 = clubsneeded2
        temprule3 = temprule | temprule2
        world.set_rule(world.get_location("Golfaria - Sandy Sinkhole B NPC"), temprule3)
        world.set_rule(world.get_location("Golfaria - Ocean Pit NPC"), haswater)

    if difficulty == GolfariaDifficulty.option_hardcore:
        strokes = world.options.golfaria_hardcore_strokes
        temprule = hasbrakes & hasblock
        world.set_rule(world.get_location("Golfaria - Tee Temple Checkpoint Location"), temprule)
        temprule = hasbrakes & rules.Has(club, count=15 - strokes)
        temprule2 = temprule | hasblock
        world.set_rule(world.get_location("Golfaria - Cave Town Checkpoint Location"), temprule2)
        temprule = hasbrakes & rules.Has(club, count=15 - strokes)
        world.set_rule(world.get_location("Golfaria - Winding Wetway Checkpoint Location"), temprule)
        temprule = hasbrakes & hassand & rules.Has(club, count=19 - strokes)
        world.set_rule(world.get_location("Golfaria - Bunker Below Checkpoint Location"), temprule)
        world.set_rule(world.get_location("Golfaria - Brakes Location"), rules.Has(club, count=6))
        temprule = hasbrakes & rules.Has(club, count=16 - strokes)
        world.set_rule(world.get_location("Golfaria - Block Buster Location"), temprule)
        world.set_rule(world.get_location("Golfaria - Garden"), temprule)
        temprule = hasbrakes & haswater & rules.Has(club, count=17 - strokes)
        world.set_rule(world.get_location("Golfaria - Sand Roll Location"), temprule)
        temprule = hasbrakes & hassand & rules.Has(club, count=15 - strokes)
        world.set_rule(world.get_location("Golfaria - Water Roll Location"), temprule)
        temprule = hasbrakes & hasblock & rules.Has(club, count=18 - strokes)
        world.set_rule(world.get_location("Golfaria - Crumbling Cut Tee"), temprule)
        temprule = haswater & rules.Has(club, count=13 - strokes)
        world.set_rule(world.get_location("Golfaria - Water-Wedge Way Tee"), temprule)
        world.set_rule(world.get_location("Golfaria - Sandy Subterra Tee"), hasbrakes)
        temprule = hasbrakes & haswater & rules.Has(club, count=14 - strokes)
        world.set_rule(world.get_location("Golfaria - Tee Temple Tee"), temprule)
        world.set_rule(world.get_location("Golfaria - Underputt Club 2"), haswater)
        world.set_rule(world.get_location("Golfaria - Downswing Dip Club"), rules.Has(club, count=11 - strokes))
        world.set_rule(world.get_location("Golfaria - Up N Over Cove Club"), rules.Has(club, count=18 - strokes))
        world.set_rule(world.get_location("Golfaria - Gritty Grip Grotto Club"), hassand)
        world.set_rule(world.get_location("Golfaria - Moebius Hole Club"), hasblock)
        world.set_rule(world.get_location("Golfaria - Rooted Route Blocked Club"), hasblock)
        world.set_rule(world.get_location("Golfaria - Rooted Route Water Roll Club"), haswater)
        world.set_rule(world.get_location("Golfaria - Tee Temple Club 1"), hasbrakes)
        temprule = hasbrakes & rules.Has(club, count=13 - strokes)
        world.set_rule(world.get_location("Golfaria - Tee Temple Club 2"), temprule)
        temprule = hasbrakes & hasblock & rules.Has(club, count=18 - strokes)
        world.set_rule(world.get_location("Golfaria - Mulligan Caverns Club"), temprule)
        temprule = hasbrakes & rules.Has(club, count=15 - strokes)
        temprule2 = temprule | hasblock
        world.set_rule(world.get_location("Golfaria - Driver Depths Club"), temprule2)
        temprule = hasbrakes & haswater & rules.Has(club, count=11 - strokes)
        world.set_rule(world.get_location("Golfaria - Winding Wetway Club"), temprule)
        world.set_rule(world.get_location("Golfaria - West Green Parbot"), rules.Has(club, count=11 - strokes))
        temprule = hasbrakes & rules.Has(club, count=14 - strokes)
        world.set_rule(world.get_location("Golfaria - Mt Driver Parbot"), temprule)
        temprule = hasbrakes & rules.Has(club, count=17 - strokes)
        world.set_rule(world.get_location("Golfaria - Bunker Dunes Parbot 2"), temprule)
        temprule = hasbrakes & rules.Has(club, count=18 - strokes)
        world.set_rule(world.get_location("Golfaria - Up And Down Isle Parbot"), temprule)
        temprule = haswater & rules.Has(club, count=11 - strokes)
        world.set_rule(world.get_location("Golfaria - Arc Archipelago Parbot"), temprule)
        world.set_rule(world.get_location("Golfaria - Underputt Parbot"), haswater)
        temprule = hasblock & haswater & rules.Has(club, count=15 - strokes)
        world.set_rule(world.get_location("Golfaria - Up N Over Cove NPC"), temprule)
        temprule = hasbrakes & haswater & rules.Has(club, count=11 - strokes)
        world.set_rule(world.get_location("Golfaria - Winding Wetway NPC"), temprule)
        world.set_rule(world.get_location("Golfaria - East Temple NPC"), hasbrakes)
        world.set_rule(world.get_location("Golfaria - Sandy Subterra NPC"), hasbrakes)
        world.set_rule(world.get_location("Golfaria - Sandy Sinkhole B NPC"), rules.Has(club, count=19 - strokes))
        temprule = haswater & rules.Has(club, count=11 - strokes)
        world.set_rule(world.get_location("Golfaria - Ocean Pit NPC"), temprule)
