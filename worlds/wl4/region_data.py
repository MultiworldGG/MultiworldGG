from __future__ import annotations

from enum import Enum, auto
from typing import NamedTuple

from .data import Passage
from .options import Difficulty, Goal
from .rules import Requirement, has, has_all, has_any, has_treasures, option, difficulty, not_difficulty, advanced_logic
from .tricks import trick


normal = Difficulty.option_normal
hard = Difficulty.option_hard
s_hard = Difficulty.option_s_hard


class LocationType(Enum):
    MAIN = auto()
    DIAMOND = auto()
    KEYZER = auto()
    SWITCH = auto()


class LevelData(NamedTuple):
    regions: list[RegionData]
    use_entrance_region: bool = True


class RegionData(NamedTuple):
    name: str | None
    exits: list[ExitData]
    locations: list[LocationData] = []


class ExitData(NamedTuple):
    destination: str | None
    access_rule: Requirement | None = None  # Forward and reverse


class LocationData(NamedTuple):
    name: str
    type: LocationType = LocationType.MAIN
    access_rule: Requirement | None = None
    difficulties: list[int] = [normal, hard, s_hard]


class BossData(NamedTuple):
    name: str
    kill_rule: Requirement
    quick_kill_rule: Requirement | None = None


passage_levels = {
    Passage.ENTRY: ["Hall of Hieroglyphs"],
    Passage.EMERALD: ["Palm Tree Paradise", "Wildflower Fields", "Mystic Lake", "Monsoon Jungle"],
    Passage.RUBY: ["The Curious Factory", "The Toxic Landfill", "40 Below Fridge", "Pinball Zone"],
    Passage.TOPAZ: ["Toy Block Tower", "The Big Board", "Doodle Woods", "Domino Row"],
    Passage.SAPPHIRE: ["Crescent Moon Village", "Arabian Night", "Fiery Cavern", "Hotel Horror"],
    Passage.GOLDEN: ["Golden Passage"],
}


level_table = {
    "Hall of Hieroglyphs": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(
                        None,
                        has_all(["Dash Attack", "Grab", "Super Ground Pound"])
                    ),
                ]
            ),
            RegionData(
                None,
                [],
                [
                    LocationData("First Jewel Box"),
                    LocationData("Second Jewel Box"),
                    LocationData("Full Health Item Box"),
                    LocationData("Third Jewel Box"),
                    LocationData("Fourth Jewel Box"),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Stone Block Diamond", LocationType.DIAMOND),
                    LocationData("Grab Tutorial Diamond", LocationType.DIAMOND, difficulties=[s_hard]),
                    LocationData("Diamond Above Jewel Box", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Alcove Diamond", LocationType.DIAMOND, difficulties=[normal, hard]),
                    LocationData("Ground Pound Tutorial Diamond", LocationType.DIAMOND),
                ]
            ),
        ]
    ),

    "Palm Tree Paradise": LevelData(
        [
            RegionData(
                None,
                [],
                [
                    LocationData("First Box", difficulties=[normal]),
                    LocationData("Ledge Box", difficulties=[hard]),
                    LocationData("Dead End Box", difficulties=[s_hard]),
                    LocationData("Box Before Cave", difficulties=[normal]),
                    LocationData("Hidden Box", difficulties=[hard, s_hard]),
                    LocationData("Platform Cave Jewel Box"),
                    LocationData("Ladder Cave Box"),
                    LocationData("CD Box"),
                    LocationData("Full Health Item Box"),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
#                   LocationData("Unused Cave Diamond", LocationType.DIAMOND),
                    LocationData("Ledge Diamond", LocationType.DIAMOND, difficulties=[s_hard]),
                    LocationData("Hidden Tunnel Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Platform Cave Hidden Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Submerged Diamond", LocationType.DIAMOND, access_rule=has("Swim")),
                    LocationData(
                        "Switch Staircase Diamond",
                        LocationType.DIAMOND,
                        access_rule=has("Grab") | advanced_logic() & has("Stomp Jump")
                    ),
                    LocationData("Scienstein Throw Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                ]
            ),
        ],
        use_entrance_region=False
    ),
    "Wildflower Fields": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("8-Shaped Cave", has("Super Ground Pound")),
                    ExitData("Sunflower Roots", has("Super Ground Pound")),
                ],
                [
                    LocationData("CD Box"),
                ]
            ),
            RegionData(
                "8-Shaped Cave",
                [],
                [
                    LocationData(
                        "8-Shaped Cave Box",
                        access_rule=(difficulty(hard) & has("Grab")) | (difficulty(s_hard) & has("Heavy Grab")),
                        difficulties=[hard, s_hard]
                    ),
                    LocationData("8-Shaped Cave Diamond", LocationType.DIAMOND, has("Grab"), difficulties=[normal]),
                ]
            ),
            RegionData(
                "Sunflower Roots",
                [
                    ExitData("Giant Sunflower", has("Swim")),
                ],
                [
                    LocationData(
                        "Scienstein Stomp Diamond",
                        LocationType.DIAMOND,
                        access_rule=has("Grab") & has("Stomp Jump")
                    )
                ]
            ),
            RegionData(
                "Giant Sunflower",
                [],
                [
                    LocationData("Current Cave Box"),
                    LocationData("Sunflower Jewel Box", difficulties=[normal]),
                    LocationData("Sunflower Box", difficulties=[hard, s_hard]),
                    LocationData("Slope Room Box", difficulties=[normal]),
                    LocationData("Beezley Box"),
                    LocationData("Full Health Item Box", difficulties=[normal]),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Hidden Tunnel Diamond", LocationType.DIAMOND),
                    LocationData("Escape Detour Diamond", LocationType.DIAMOND),
                    LocationData("Escape Detour Corner Diamond", LocationType.DIAMOND),
                    LocationData("Current Cave Diamond", LocationType.DIAMOND),
                    LocationData("Sunflower Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Switch Puzzle Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                ]
            ),
        ]
    ),
    "Mystic Lake": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Rock Cave", has("Grab")),
                    ExitData("Shallows", has("Swim")),
                ],
                []
            ),
            RegionData(
                "Rock Cave",
                [],
                [
                    LocationData("Rock Cave Box", difficulties=[s_hard]),
                    LocationData("Full Health Item Box", difficulties=[normal, hard]),
                ]
            ),
            RegionData(
                "Shallows",
                [
                    ExitData("Large Cave", has("Head Smash")),
                    ExitData("Depths", has("Head Smash")),
                ],
                [
                    LocationData("Air Pocket Box", difficulties=[normal]),
                    LocationData("Air Pocket Diamond", LocationType.DIAMOND, difficulties=[hard, s_hard]),
                ]
            ),
            RegionData(
                "Large Cave",
                [],
                [
                    LocationData("Large Cave Box", difficulties=[hard, s_hard]),
                    LocationData("Large Cave Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData(
                        "Shallow Pool Puzzle Diamond",
                        LocationType.DIAMOND,
                        access_rule=has_all(["Super Ground Pound", "Grab"])
                    ),
                ]
            ),
            RegionData(
                "Depths",
                [
                    ExitData("Utsuboanko Hidden Cave", access_rule=has("Dash Attack")),
                ],
                [
                    LocationData("Hill Room Box", difficulties=[normal]),
                    LocationData("Cavern Box", difficulties=[normal]),
                    LocationData("Spring Cave Box", difficulties=[hard, s_hard]),
                    LocationData("Box Before Bridge", difficulties=[normal]),
                    LocationData("Lake Exit Bubble Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box", access_rule=has("Dash Attack")),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Eel Cave Underwater Diamond", LocationType.DIAMOND),
                    LocationData("Bubble Path Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Deep Pool Puzzle Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                ]
            ),
            RegionData(
                "Utsuboanko Hidden Cave",
                [],
                [
                    LocationData("Small Cave Box", difficulties=[hard]),
                    LocationData("Full Health Item Box", difficulties=[s_hard]),
                    LocationData("Small Cave Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
        ]
    ),
    "Monsoon Jungle": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Deeps", access_rule=has("Ground Pound")),
                ],
                [
                    LocationData("Fat Plummet Box"),
                    LocationData("CD Box", access_rule=has("Ground Pound") | trick("MJ CD box with grab")),
                    LocationData("Full Health Item Box", access_rule=has("Swim")),
                    LocationData("Fat Plummet Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Archer Pink Room Diamond", LocationType.DIAMOND),
                    LocationData("Rock Catching Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                ]
            ),
            RegionData(
                "Deeps",
                [
                    ExitData("Puffy Hallway", access_rule=has("Dash Attack")),
                    ExitData("Buried Cave", access_rule=has("Grab")),
                ],
                [
                    LocationData("Spiky Box", difficulties=[normal]),
                    LocationData("Escape Climb Box", difficulties=[hard]),
                    LocationData("Brown Pipe Cave Box", difficulties=[s_hard]),
                    LocationData("Descent Box", difficulties=[normal]),
                    LocationData("Buried Cave Box", difficulties=[normal]),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                ]
            ),
            RegionData(
                "Puffy Hallway",
                [],
                [
                    LocationData("Puffy Hallway Box", difficulties=[hard, s_hard]),
                    LocationData("Puffy Hallway Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
            RegionData(
                "Buried Cave",
                [],
                [
                    LocationData("Buried Cave Box", difficulties=[hard, s_hard]),
                    LocationData("Buried Cave Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
        ]
    ),

    "The Curious Factory": LevelData(
        [
            RegionData(
                None,
                [
                    ExitData("Gear Elevator", access_rule=has("Dash Attack")),
                ],
                [
                    LocationData("First Drop Box", difficulties=[normal]),
                    LocationData("Thin Gap Box", difficulties=[hard, s_hard]),
                    LocationData("Early Escape Box", difficulties=[normal]),
                    LocationData("Conveyor Room Box", difficulties=[hard, s_hard]),
                    LocationData("Late Escape Box", difficulties=[normal]),
                    LocationData("Underground Chamber Box", difficulties=[hard, s_hard]),
                    LocationData("Frog Switch Room Box", difficulties=[normal]),
                    LocationData("CD Box"),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("T-Tunnel Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Scienstein Puzzle Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                    LocationData("Rock Puzzle Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                    LocationData("Underground Chamber Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
            RegionData(
                "Gear Elevator",
                [],
                [
                    LocationData("Gear Elevator Box", difficulties=[hard, s_hard]),
                    LocationData("Gear Elevator Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
        ],
        use_entrance_region=False
    ),
    "The Toxic Landfill": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(None, has_all(["Dash Attack", "Super Ground Pound", "Head Smash"])),
                ]
            ),
            RegionData(
                None,
                [
                    ExitData("Current Circle Room", access_rule=has("Swim")),
                    ExitData("Transformation Puzzle", access_rule=has_any(["Heavy Grab", "Stomp Jump"])),
                ],
                [
                    LocationData("Portal Room Box", difficulties=[normal]),
                    LocationData("Box Above Portal", difficulties=[hard, s_hard]),
                    LocationData("Fat Room Box"),
                    LocationData("Spring Room Box", difficulties=[normal]),
                    LocationData("Ledge Box", difficulties=[normal]),
                    LocationData("CD Box"),
                    LocationData("Full Health Item Box", difficulties=[normal]),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Trash Plummet Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Spike Ceiling Diamond", LocationType.DIAMOND),
                    LocationData("Sewage Pool Diamond", LocationType.DIAMOND, access_rule=has("Swim")),
                    LocationData("Trash Sprint Diamond", LocationType.DIAMOND),
                    LocationData(
                        "Transformation Puzzle Lower Diamond",
                        LocationType.DIAMOND,
                        access_rule=has("Swim")
                            & (has("Heavy Grab") | trick("TTL transformation puzzle without heavy grab"))
                    ),
                    LocationData("Rock Throwing Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                ]
            ),
            RegionData(
                "Current Circle Room",
                [],
                [
                    LocationData("Current Circle Box", difficulties=[hard, s_hard]),
                    LocationData("Current Circle Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
            RegionData(
                "Transformation Puzzle",
                [],
                [
                    LocationData("Transformation Puzzle Box", difficulties=[hard, s_hard]),
                    LocationData("Transformation Puzzle Upper Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
        ]
    ),
    "40 Below Fridge": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(None, has("Super Ground Pound")),
                ],
                [
                    LocationData("Conveyor Room Diamond", LocationType.DIAMOND),
                ]
            ),
            RegionData(
                None,
                [],
                [
                    LocationData("Looping Room Box"),
                    LocationData("Maze Room Box"),
                    LocationData("Snowman Puzzle Lower Left Box", difficulties=[normal]),
                    LocationData("Snowman Puzzle Upper Left Box", difficulties=[hard, s_hard]),
                    LocationData("Snowman Puzzle Upper Right Box", difficulties=[normal]),
                    LocationData("Snowman Puzzle Lower Right Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box", access_rule=has("Head Smash") | trick("40BF CD box with heavy grab")),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Maze Cage Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Maze Pit Diamond", LocationType.DIAMOND),
                    LocationData("Looping Room Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Ice Block Diamond", LocationType.DIAMOND),
                    LocationData("Snowman Puzzle Left Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Snowman Puzzle Bottom Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Snowman Puzzle Diamond Under Door", LocationType.DIAMOND),
                    LocationData("Snowman Puzzle Right Diamond", LocationType.DIAMOND),
                    LocationData(
                        "Glass Ball Puzzle Diamond",
                        LocationType.DIAMOND,
                        access_rule=has("Grab") | trick("40BF glass ball stomp jump")
                    ),
                    LocationData("Yeti Puzzle Diamond", LocationType.DIAMOND, access_rule=has("Heavy Grab")),
                ]
            ),
        ]
    ),
    "Pinball Zone": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Early Rooms", has("Grab")),
                ]
            ),
            RegionData(
                "Early Rooms",
                [
                    ExitData("Jungle Room", has("Ground Pound") | trick("PZ fruit room without ground pound")),
                ],
                [
                    LocationData("Rolling Room Box", difficulties=[normal, hard]),
                    LocationData("Fruit Room Box"),
                    LocationData("Rolling Room Full Health Item Box", difficulties=[s_hard]),
                    LocationData("Fruit Room Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Flaming Wario Diamond", LocationType.DIAMOND),
                ]
            ),
            RegionData(
                "Jungle Room",
                [
                    ExitData("Late Rooms", has("Ground Pound") | trick("PZ jungle room with Fat Wario")),
                ],
                [
                    LocationData("Jungle Room Box"),
                ]
            ),
            RegionData(
                "Late Rooms",
                [
                    ExitData("Scienstein Puzzle Pink Room", has("Super Ground Pound")),
                    ExitData("Escape", has_all(["Ground Pound", "Head Smash"])),
                ],
                [
                    LocationData("Switch Room Box", difficulties=[s_hard]),
                    LocationData("Snow Room Box"),
                    LocationData("CD Box"),
                    LocationData("Switch Room Diamond", LocationType.DIAMOND, difficulties=[hard, s_hard]),
                    LocationData("Snow Room Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
            RegionData(
                "Scienstein Puzzle Pink Room",
                [],
                [
                    LocationData("Full Health Item Box", difficulties=[normal, hard]),
                    LocationData("Pink Room Full Health Item Box", difficulties=[s_hard]),
                ]
            ),
            RegionData(
                "Escape",
                [],
                [
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Robot Room Diamond", LocationType.DIAMOND, access_rule=has("Dash Attack")),
                ]
            ),
        ]
    ),

    "Toy Block Tower": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(None, has("Heavy Grab")),
                ]
            ),
            RegionData(
                None,
                [
                    ExitData("Block Catch Pink Room", access_rule=has("Dash Attack")),
                ],
                [
                    LocationData("Toy Car Overhang Box", difficulties=[normal, hard]),
                    LocationData("Tower Exterior Top Box", difficulties=[s_hard]),
                    LocationData("Hidden Tower Room Box", difficulties=[normal]),
                    LocationData("Digging Room Box", access_rule=has("Dash Attack"), difficulties=[hard, s_hard]),
                    LocationData("Fire Box", difficulties=[normal]),
                    LocationData("Hidden Falling Block Door Box", difficulties=[hard]),
                    LocationData("Bonfire Block Box", difficulties=[s_hard]),
                    LocationData("Red Pipe Box", difficulties=[normal]),
                    LocationData("Escape Ledge Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box"),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Tower Diamond", LocationType.DIAMOND, difficulties=[hard]),
                    LocationData("Digging Room Diamond", LocationType.DIAMOND, access_rule=has("Dash Attack")),
                    LocationData("Escape Ledge Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Cage Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData(
                        "Circle Block Diamond",
                        LocationType.DIAMOND,
                        access_rule=has_all(["Super Ground Pound", "Dash Attack"])
                    ),
                ]
            ),
            RegionData(
                "Block Catch Pink Room",
                [],
                [
                    LocationData("Full Health Item Box", difficulties=[normal, hard]),
                    LocationData("Dash Puzzle Diamond", LocationType.DIAMOND, difficulties=[s_hard]),
                ]
            ),
        ]
    ),
    "The Big Board": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(None, access_rule=has("Ground Pound")),
                ]
            ),
            RegionData(
                None,
                [],
                [
                    LocationData("First Box", difficulties=[normal]),
                    LocationData("Hard Fire Room Box", difficulties=[hard, s_hard]),
                    LocationData("Normal Fire Room Box", difficulties=[normal]),
                    LocationData("Hard Enemy Room Box", access_rule=has("Grab"), difficulties=[hard, s_hard]),
                    LocationData("Normal Enemy Room Box", difficulties=[normal]),
                    LocationData("Fat Room Box", difficulties=[hard, s_hard]),
                    LocationData("Toy Car Box", difficulties=[normal]),
                    LocationData("Flat Room Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box"),
                    LocationData(
                        "Full Health Item Box",
                        access_rule=has_all(["Grab", "Stomp Jump"]),
                        difficulties=[normal, hard]
                    ),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Fire Room Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData(
                        "Enemy Room Diamond",
                        LocationType.DIAMOND,
                        access_rule=has("Grab"),
                        difficulties=[normal]
                    ),
                    LocationData("Fat Room Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Bouncy Room Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Scienstein Puzzle Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                ]
            ),
        ]
    ),
    "Doodle Woods": LevelData(
        [
            RegionData(
                None,
                [
                    ExitData("Blue Circle Room", has("Stomp Jump")),
                    ExitData("Pink Circle Room", has("Ground Pound")),
                    ExitData("Gray Square Room", has("Ground Pound") | trick("DW gray square room with grab")),
                ],
                [
                    LocationData("Box Behind Wall", difficulties=[normal]),
                    LocationData("Orange Escape Box", difficulties=[normal]),
                    LocationData("Buried Door Box", difficulties=[normal]),
                    LocationData("Purple Square Box", difficulties=[hard, s_hard]),
                    LocationData("Blue Escape Box", difficulties=[normal]),
                    LocationData("CD Box", difficulties=[hard, s_hard]),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Platform Staircase Diamond", LocationType.DIAMOND, difficulties=[normal, hard]),
                    LocationData("Hidden Platform Puzzle Diamond", LocationType.DIAMOND),
                    LocationData("Rolling Room Diamond", LocationType.DIAMOND),
                ]
            ),
            RegionData(
                "Blue Circle Room",
                [],
                [
                    LocationData("Blue Circle Box", difficulties=[hard, s_hard]),
                    LocationData("Blue Circle Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
            RegionData(
                "Pink Circle Room",
                [],
                [
                    LocationData("Pink Circle Box", difficulties=[hard, s_hard]),
                    LocationData("Pink Circle Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
            RegionData(
                "Gray Square Room",
                [],
                [
                    LocationData("Gray Square Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box", difficulties=[normal]),
                ]
            ),
        ],
        use_entrance_region=False
    ),
    "Domino Row": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Lake Entrance", has("Ground Pound") | trick("DR escape with only swim")),
                ],
                [
                    LocationData("Racing Box"),
                ]
            ),
            RegionData(
                "Lake Entrance",
                [
                    ExitData("Lake Area", has("Swim")),
                ],
                [
                    LocationData(
                        "Toy Car Tower Diamond",
                        LocationType.DIAMOND,
                        access_rule=has_all(["Grab", "Stomp Jump"]) | trick("DR toy car tower diamond damage boost"),
                        difficulties=[normal, hard]
                    ),
                ]
            ),
            RegionData(
                "Lake Area",
                [],
                [
                    LocationData("Rolling Box"),
                    LocationData("Swimming Detour Box", access_rule=has("Head Smash"), difficulties=[normal, hard]),
                    LocationData("Swimming Room Escape Box", access_rule=has("Ground Pound"), difficulties=[s_hard]),
                    LocationData("Keyzer Room Box", access_rule=has("Ground Pound")),
                    LocationData("CD Box"),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData(
                        "Switch Ladder Diamond",
                        LocationType.DIAMOND,
                        difficulties=[normal, hard],
                        access_rule=has("Super Ground Pound") & (
                            has("Dash Attack") | trick("DR switch room block no dash attack"))
                    ),
                ]
            ),
        ]
    ),

    "Crescent Moon Village": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Upper", access_rule=has("Head Smash"))
                ],
                [
                    LocationData("First Village Diamond", LocationType.DIAMOND),
                ]
            ),
            RegionData(
                "Upper",
                [
                    ExitData("Agile Bat Rock Puzzle", access_rule=has_all(["Ground Pound", "Grab"])),
                    ExitData("Lower", access_rule=has("Dash Attack")),
                ],
                [
                    LocationData("Agile Bat Box", difficulties=[normal]),
                ]
            ),
            RegionData(
                "Agile Bat Rock Puzzle",
                [],
                [
                    LocationData("Agile Bat Hidden Box", difficulties=[hard, s_hard]),
                    LocationData("Agile Bat Hidden Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
            RegionData(
                "Lower",
                [
                    ExitData("Sewer", access_rule=has("Swim"))
                ],
                [
                    LocationData("Metal Platform Box", difficulties=[normal]),
                    LocationData("Metal Platform Rolling Box", difficulties=[hard, s_hard]),
                    LocationData("Rolling Box", difficulties=[normal]),
                    LocationData("!-Switch Rolling Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box"),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Dropdown Diamond", LocationType.DIAMOND),
                    LocationData("Candle Dodging Diamond", LocationType.DIAMOND),
                    LocationData("Glass Ball Puzzle Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                ]
            ),
            RegionData(
                "Sewer",
                [],
                [
                    LocationData("Sewer Box"),
                    LocationData("Sewer Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
        ]
    ),
    "Arabian Night": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(
                        "Onomi Room Bottom",
                        has_any(["Ground Pound", "Head Smash"]) | trick("AN Onomi room with grab")
                    ),
                    ExitData("Flying Carpet Dash Attack Puzzle", has("Dash Attack")),
                    ExitData("Kool-Aid Man", has("Dash Attack")),
                    ExitData("Sewer", has("Swim")),
                ],
                [
                    LocationData("Onomi Box", difficulties=[normal]),
                    LocationData("Flying Carpet Overhang Box", difficulties=[normal]),
                    LocationData("Zombie Plummet Box", difficulties=[normal]),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("City Ledge Diamond", LocationType.DIAMOND),
                    LocationData("Scienstein Puzzle Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                ]
            ),
            RegionData(
                "Onomi Room Bottom",
                [],
                [
                    LocationData("Onomi Box", difficulties=[hard, s_hard]),
                    LocationData("Onomi Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
            RegionData(
                "Flying Carpet Dash Attack Puzzle",
                [],
                [
                    LocationData("Flying Carpet Dash Attack Box", difficulties=[hard, s_hard]),
                    LocationData("Flying Carpet Dash Attack Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
            RegionData(
                "Kool-Aid Man",
                [],
                [
                    LocationData("Kool-Aid Box", difficulties=[hard, s_hard]),
                    LocationData("Kool-Aid Diamond", LocationType.DIAMOND, difficulties=[normal]),
                ]
            ),
            RegionData(
                "Sewer",
                [
                    ExitData("Sewer Underwater", access_rule=has("Super Ground Pound"))
                ],
                [
                    LocationData("Sewer Box", difficulties=[normal]),
                    LocationData("CD Box"),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Left Sewer Ceiling Diamond", LocationType.DIAMOND),
                    LocationData("Right Sewer Ceiling Diamond", LocationType.DIAMOND),
                ]
            ),
            RegionData(
                "Sewer Underwater",
                [],
                [
                    LocationData("Sewer Box", difficulties=[hard, s_hard]),
                    LocationData("Sewer Air Pocket Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Sewer Submerged Diamond", LocationType.DIAMOND),
                ]
            ),
        ]
    ),
    "Fiery Cavern": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Frozen", has_all(["Ground Pound", "Dash Attack", "Head Smash"])),
                ],
                [
                    LocationData("Lava Dodging Box", difficulties=[normal]),
                    LocationData("Long Lava Geyser Box"),
                    LocationData("Long Lava Geyser Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Scienstein Puzzle Diamond", LocationType.DIAMOND, access_rule=has("Grab")),
                    LocationData("Spring Puzzle Diamond", LocationType.DIAMOND, access_rule=has("Ground Pound")),
                ]
            ),
            RegionData(
                "Frozen",
                [],
                [
                    LocationData("Ice Beyond Door Box", difficulties=[hard, s_hard]),
                    LocationData("Ice Detour Box"),
                    LocationData("Snowman Box"),
                    LocationData("CD Box"),
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData(
                        "Ice Jump Diamond",
                        LocationType.DIAMOND,
                        access_rule=has("Stomp Jump"),
                        difficulties=[normal, hard]
                    ),
                    LocationData("Corner Diamond", LocationType.DIAMOND, difficulties=[normal, hard]),
                    LocationData("Hidden Ice Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Frozen Diamond", LocationType.DIAMOND),
                ]
            ),
        ]
    ),
    "Hotel Horror": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(
                        "Switch Room",
                        access_rule=has("Heavy Grab") | trick("HH escape minion jump") | difficulty(s_hard)
                    ),
                ],
                [
                    LocationData("1F Hallway Box", difficulties=[normal]),
                    LocationData("Room 102 Box", difficulties=[hard, s_hard]),
                    LocationData("2F Hallway Box", difficulties=[normal]),
                    LocationData("Room 303 Box", difficulties=[hard, s_hard]),
                    LocationData("3F Hallway Box", difficulties=[normal]),
                    LocationData("Room 402 Box", difficulties=[hard, s_hard]),
                    LocationData("4F Hallway Box", difficulties=[normal]),
                    LocationData("Exterior Box", difficulties=[hard, s_hard]),
                    LocationData("Keyzer", LocationType.KEYZER, difficulties=[normal, hard]),
                    LocationData("Room 102 Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Room 402 Diamond", LocationType.DIAMOND, difficulties=[normal]),
                    LocationData("Bonfire Block Diamond", LocationType.DIAMOND, difficulties=[s_hard]),
                    LocationData("Exterior Diamond", LocationType.DIAMOND),
                    LocationData("Transformation Puzzle Fat Diamond", LocationType.DIAMOND),
                    LocationData("Transformation Puzzle Spring Diamond", LocationType.DIAMOND),
                ]
            ),
            RegionData(
                "Switch Room",
                [],
                [
                    LocationData("CD Box"),
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Keyzer", LocationType.KEYZER, difficulties=[s_hard]),
                ]
            ),
        ]
    ),

    "Golden Passage": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Current Puzzle", has("Swim")),
                    ExitData("Passage", trick("GP current room skip")),
                ],
                [
                    LocationData("Frog Switch", LocationType.SWITCH),
                    LocationData("Long Hall Left Diamond", LocationType.DIAMOND),
                    LocationData("Long Hall Right Diamond", LocationType.DIAMOND),
                ]
            ),
            RegionData(
                "Current Puzzle",
                [
                    ExitData("Passage"),
                ],
                [
                    LocationData("Current Puzzle Box"),
                    LocationData("Current Puzzle Diamond", LocationType.DIAMOND),
                ]
            ),
            RegionData(
                "Passage",
                [
                    ExitData("Scienstein Area", has("Ground Pound") | trick("GP Keyzer puzzle without ground pound")),
                ],
                [
                    LocationData("River Box"),
                    LocationData("Bat Room Box"),
                    LocationData("Spring Shaft Diamond", LocationType.DIAMOND),
                    LocationData("Zombie Hall Left Diamond", LocationType.DIAMOND),
                    LocationData("Zombie Hall Right Diamond", LocationType.DIAMOND),
                    LocationData("Digging Diamond", LocationType.DIAMOND),
                    LocationData("Slope Diamond", LocationType.DIAMOND),
                    LocationData("Scienstein Escape Diamond", LocationType.DIAMOND, access_rule=has("Swim")),
                ]
            ),
            RegionData(
                "Scienstein Area",
                [
                    ExitData("Keyzer Area", has("Grab")),
                ],
                [
                    LocationData("Mad Scienstein Box"),
                ]
            ),
            RegionData(
                "Keyzer Area",
                [],
                [
                    LocationData("Keyzer", LocationType.KEYZER),
                    LocationData("Scienstein Roll Diamond", LocationType.DIAMOND),
                ]
            ),
        ]
    ),
}


passage_boss_table = {
    Passage.EMERALD: BossData(
        "Cractus",
        has("Ground Pound"),
        not_difficulty(s_hard) | has("Stomp Jump") | advanced_logic()
    ),
    Passage.RUBY: BossData("Cuckoo Condor", has("Grab")),
    Passage.TOPAZ: BossData("Aerodent", has("Grab")),
    Passage.SAPPHIRE: BossData(
        "Catbat",
        has("Ground Pound") & (has("Stomp Jump") | trick("Catbat without stomp jump")),
        has("Stomp Jump") | advanced_logic() & not_difficulty(s_hard)
    ),
}

golden_diva = BossData(
    "Golden Diva",
    has("Heavy Grab") & (option("goal", Goal.option_golden_diva) | has_treasures())
)
