import logging
import math
from typing import List, Union
from dataclasses import dataclass
from Options import Range, Toggle, PerGameCommonOptions, OptionSet, OptionError, Choice, Accessibility
from .Locations import land_vehicles, water_vehicles, air_vehicles, places, bonus_jobs, midgar, tomb_raider, \
    raw_location_dict, wallace_and_gromit, shrek, alice, warhammer_40k, back_to_the_future, spongebob
from settings import Group, Bool
from random import Random


class StartWithVan(Toggle):
    """
    Start with Van as the random starting level
    """
    display_name = "Start With Van"


class LandVehicleLocations(OptionSet):
    """
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Van", "Vintage Car", "Grandpa Miller's Car", "Fire Truck", "Dirt Bike", "Golf Cart", "Motorbike and Sidecar", "SUV", "Penny Farthing", "Recreation Vehicle", "Drill", "Monster Truck"]
    "All" - adds all locations above
    """
    display_name = "Land Vehicle Locations"
    valid_keys = frozenset(land_vehicles + ["All"])
    default = "All"


class WaterVehicleLocations(OptionSet):
    """
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Frolic Boat", "Fishing Boat"]
    "All" - adds all locations above
    """
    display_name = "Water Vehicle Locations"
    valid_keys = frozenset(water_vehicles + ["All"])
    default = "All"


class AirVehicleLocations(OptionSet):
    """
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Fire Helicopter", "Private Jet", "Stunt Plane", "Recreational Vehicle (Again)"]
    "All" - adds all locations above
    """
    display_name = "Air Vehicle Locations"
    valid_keys = frozenset(air_vehicles + ["All"])
    default = "All"


class PlaceLocations(OptionSet):
    """
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Back Garden", "Bungalow", "Playground", "Detached House", "Shoe House", "Fire Station", "Skatepark", "Forest Cottage", "Mayor's Mansion", "Carousel", "Tree House", "Temple", "Washroom", "Helter Skelter", "Ferris Wheel", "Subway Platform", "Fortune Teller's Wagon", "Ancient Statue", "Ancient Monument", "Lost City Palace"]
    "All" - adds all locations above
    """
    display_name = "Place Locations"
    valid_keys = frozenset(places + ["All"])
    default = "All"


class BonusJobLocations(OptionSet):
    """
    Locations:
    ["Mars Rover", "Gnome Fountain", "Mini Golf Course", "Steam Locomotive", "Food Truck", "Satellite Dish", "Solar Station", "Paintball Arena", "Spanish Villa", "Excavator", "Aquarium", "Submarine", "Modern Mansion", "Fire Plane", "Dessert Parlor", "Subway Train", "Sculpture Park"]
    "All" - adds all locations above
    """
    display_name = "Bonus Job Locations"
    valid_keys = frozenset(bonus_jobs + ["All"])


class MidgarLocations(OptionSet):
    """
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Scorpion Sentinel", "Hardy-Daytona & Shinra Hauler", "Seventh Heaven", "Mako Energy Exhibit", "Airbuster"]
    "All" - adds all locations above
    """
    display_name = "Midgar Locations"
    valid_keys = frozenset(midgar + ["All"])


class TombRaiderLocations(OptionSet):
    """
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Croft Manor", "Lara Croft's Obstacle Course and Quad Bike", "Lara Croft's Jeep and Motorboat", "Croft Manor's Maze", "Croft Manor's Treasure Room"]
    "All" - adds all locations above
    """
    display_name = "Tomb Raider Locations"
    valid_keys = frozenset(tomb_raider + ["All"])


class WallaceAndGromitLocations(OptionSet):
    """
    DISCLAIMER: YOU NEED TO HAVE BOUGHT THIS DLC TO PLAY IT
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Wallace & Gromit's Dining Room & Kitchen", "Wallace & Gromit's House", "The Knit-O-Matic", "Wallace & Gromit's Vehicles", "The Moon Rocket"]
    "All" - adds all locations above
    """
    display_name = "Wallace and Gromit Locations"
    valid_keys = frozenset(wallace_and_gromit + ["All"])


class ShrekLocations(OptionSet):
    """
    DISCLAIMER: YOU NEED TO HAVE BOUGHT THIS DLC TO PLAY IT
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Shrek's Swamp", "Duloc", "Fairy Godmother's Potion Factory", "Dragon's Lair", "Hansel's Honeymoon Hideaway"]
    "All" - adds all locations above
    """
    display_name = "Shrek Locations"
    valid_keys = frozenset(shrek + ["All"])


class AliceInWonderlandLocations(OptionSet):
    """
    DISCLAIMER: YOU NEED TO HAVE BOUGHT THIS DLC TO PLAY IT
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Wonderland Entrance Hall", "White Rabbit's House", "Caterpillar's Mushroom", "Mad Tea Party", "Queen of Hearts' Court"]
    "All" - adds all locations above
    """
    display_name = "Alice in Wonderland Locations"
    valid_keys = frozenset(alice + ["All"])


class Warhammer40kLocations(OptionSet):
    """
    DISCLAIMER: YOU NEED TO HAVE BOUGHT THIS DLC TO PLAY IT
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Land Raider", "Redemptor Dreadnought", "Imperial Knight Paladin", "Rogal Dorn Battle Tank", "Thunderhawk"]
    "All" - adds all locations above
    """
    display_name = "Warhammer 40k Locations"
    valid_keys = frozenset(warhammer_40k + ["All"])


class BackToTheFutureLocations(OptionSet):
    """
    DISCLAIMER: YOU NEED TO HAVE BOUGHT THIS DLC TO PLAY IT
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Doc Brown's Van", "The Time Machine", "Hill Valley Clocktower", "The Holomax Theater", "Doc's Time Train"]
    "All" - adds all locations above
    """
    display_name = "Back to the Future Locations"
    valid_keys = frozenset(back_to_the_future + ["All"])


class SpongebobLocations(OptionSet):
    """
    DISCLAIMER: YOU NEED TO HAVE BOUGHT THIS DLC TO PLAY IT
    REMEMBER: BEAT THE LEVELS IN VANILLA FIRST FOR THEM TO APPEAR IN FREE PLAY
    Locations:
    ["Conch Street", "Bikini Bottom Buss", "Krusty Krab", "Patty Wagon", "The Invisible Boatmobile", "The Mermalair"]
    "All" - adds all locations above
    """
    display_name = "Spongebob Locations"
    valid_keys = frozenset(spongebob + ["All"])


class Sanities(OptionSet):
    """
    Which sanities should be enabled?

    Percentsanity: every % total cleaned of a level is a check
    Objectsanity: each part of a cleanable object is a check

    Objectsanity can only be enabled if the host has `allow_objectsanity` enabled in their host.yaml
    """
    display_name = "Sanities"
    valid_keys = frozenset(["Percentsanity", "Objectsanity"])
    default = "Percentsanity"


class Percentsanity(Range):
    """
    What intervals of cleaned % to have checks at

    default 20: checks at 20%, 40%, 60%, 80%, and 100%
    host yaml setting `allow_percentsanity_below_7` (off by default) will allow % below 7%
    """
    default = 20
    range_end = 20
    range_start = 1


class LocalFill(Range):
    """
    Minimums:
        - Percentsanity or Objectsanity: 55%
        - Percentsanity and Objectsanity: 97%

    the host yaml setting `allow_below_localfill_minimums` will allow for local fill to go below the minimums
    """
    default = 55
    range_start = 0
    range_end = 100


class GoalType(Choice):
    """
    What is required to goal?
    0 = mcguffin hunt (find a certain amount of `A Job Well Done`s to goal)
    1 = level hunt (complete levels to goal)
    """
    display_name = "Goal Type"
    default = 0
    option_mcguffin = 0
    option_level = 1


class LevelsToGoal(OptionSet):
    """
    Which levels to beat to goal (accepts any level)
    """
    display_name = "Levels to Goal"
    default = "Random"
    valid_keys = frozenset(raw_location_dict + ["Random", "All"])


class AmountOfLevelsToGoal(Range):
    """
    How many levels needed to goal
    
    Setting to -1 will pick a random amount of levels to goal, 50% of enabled levels <= N <= total amount of enabled levels 
    The amount of levels to goal must be > 50% of enabled levels
    The host setting: `allow_potentially_excessive_releases` will disable this
    """
    display_name = "Amount of Levels to Goal"
    range_start = -1
    range_end = len(raw_location_dict) + 99
    default = -1


@dataclass
class PowerwashSimulatorOptions(PerGameCommonOptions):
    start_with_van: StartWithVan
    land_vehicles: LandVehicleLocations
    water_vehicles: WaterVehicleLocations
    air_vehicles: AirVehicleLocations
    places: PlaceLocations
    bonus_jobs: BonusJobLocations
    midgar: MidgarLocations
    tomb_raider: TombRaiderLocations
    wallace_and_gromit_dlc: WallaceAndGromitLocations
    shrek_dlc: ShrekLocations
    alice_in_wonderland_dlc: AliceInWonderlandLocations
    warhammer_40k_dlc: Warhammer40kLocations
    back_to_the_future_dlc: BackToTheFutureLocations
    spongebob_dlc: SpongebobLocations
    sanities: Sanities
    percentsanity: Percentsanity
    local_fill: LocalFill
    goal_type: GoalType
    levels_to_goal: LevelsToGoal
    amount_of_levels_to_goal: AmountOfLevelsToGoal

    def get_locations(self) -> List[str]:
        locations = (self.flatten_locations(land_vehicles, self.land_vehicles)
                     + self.flatten_locations(water_vehicles, self.water_vehicles)
                     + self.flatten_locations(air_vehicles, self.air_vehicles)
                     + self.flatten_locations(places, self.places)
                     + self.flatten_locations(bonus_jobs, self.bonus_jobs)
                     + self.flatten_locations(midgar, self.midgar)
                     + self.flatten_locations(tomb_raider, self.tomb_raider)
                     + self.flatten_locations(wallace_and_gromit, self.wallace_and_gromit_dlc)
                     + self.flatten_locations(shrek, self.shrek_dlc)
                     + self.flatten_locations(alice, self.alice_in_wonderland_dlc)
                     + self.flatten_locations(warhammer_40k, self.warhammer_40k_dlc)
                     + self.flatten_locations(back_to_the_future, self.back_to_the_future_dlc)
                     + self.flatten_locations(spongebob, self.spongebob_dlc))

        if self.start_with_van and "Van" not in locations:
            locations.append("Van")

        return locations

    def get_goal_levels(self, locs: List[str]) -> List[str]:
        return [loc for loc in self.flatten_locations(locs, self.levels_to_goal) if loc in locs]

    def has_percentsanity(self) -> bool:
        return "Percentsanity" in self.sanities

    def has_objectsanity(self) -> bool:
        return "Objectsanity" in self.sanities

    def flatten_locations(self, list, self_list) -> List[str]:
        return list if "All" in self_list else [loc for loc in self_list if loc != "Random"]


class PowerwashSimulatorSettings(Group):
    class AllowPercentsanityBelow7(Bool):
        """Allow players to have the Percentsanity setting to be below 7%"""

    class AllowObjectsanity(Bool):
        """Allow players to enable Objectsanity"""

    class AllowBelowLocalfillMinimums(Bool):
        """Allow players to have local fill below the defined minimums"""

    class AllowPotentiallyExcessiveReleases(Bool):
        """Allow players to have less than 50% levels be required for level hunt, this can cause very large releases"""

    allow_percentsanity_below_7: Union[AllowPercentsanityBelow7, bool] = False
    allow_objectsanity: Union[AllowObjectsanity, bool] = False
    allow_below_localfill_minimums: Union[AllowBelowLocalfillMinimums, bool] = False
    allow_potentially_excessive_releases: Union[AllowPotentiallyExcessiveReleases, bool] = False


def check_options(world, locations: List[str]):
    options: PowerwashSimulatorOptions = world.options
    settings: PowerwashSimulatorSettings = world.settings
    random: Random = world.random

    if options.accessibility == Accessibility.option_minimal:
        print("Powerwash simulator doesn't support accessibility minimal, defaulting accessibility to full")
        options.accessibility = Accessibility(Accessibility.option_full)

    if len(locations) < 0:
        raise_yaml_error(world.player_name, "Does not have locations listed in their yaml")

    if options.goal_type == 1:
        raw_goal_levels = options.get_goal_levels(locations)

        if len(raw_goal_levels) == 0 and "Random" not in options.levels_to_goal:
            raise_yaml_error(world.player_name,
                             "Can't pick goal levels from 0 possible levels, make sure goal levels are included in their respective locations")

        amount_to_goal: int = options.amount_of_levels_to_goal.value
        max_random = len(locations)

        if "Random" in options.levels_to_goal or amount_to_goal > len(raw_goal_levels) or amount_to_goal < 0:
            levels_to_goal = random.sample(locations, random.randint(math.ceil(max_random / 2), max_random))
        elif "All" in options.levels_to_goal:
            levels_to_goal = locations
        else:
            levels_to_goal = raw_goal_levels

        if amount_to_goal == 0 or amount_to_goal > len(levels_to_goal):
            amount_to_goal = len(levels_to_goal)

        if amount_to_goal < 0:
            max_levels_to_goal = len(levels_to_goal)
            amount_to_goal = random.randint(int(max_levels_to_goal / 2), max_levels_to_goal)
            print(f"rand: [{amount_to_goal},{int(max_levels_to_goal / 2)},{max_levels_to_goal},{levels_to_goal}]")

        allow_below_50 = settings.allow_potentially_excessive_releases
        if amount_to_goal > len(locations):
            raise_yaml_error(world.player_name,
                             f"You cannot have more levels required to goal than goal-able levels ({len(locations)})")

        if (amount_to_goal < max_random / 2) and not allow_below_50:
            raise_yaml_error(world.player_name,
                             f"Goal level amount ({amount_to_goal}) required to goal can not be less than 50% ({int(max_random / 2)}) of your total enabled levels ({max_random})")

        options.levels_to_goal = LevelsToGoal(levels_to_goal)
        options.amount_of_levels_to_goal = AmountOfLevelsToGoal(amount_to_goal)

    if not settings.allow_below_localfill_minimums:
        if options.has_percentsanity() and options.has_objectsanity() and options.local_fill < 97:
            set_local_fill(world.player_name, options, 97)
        elif options.local_fill < 55:
            set_local_fill(world.player_name, options, 55)

    if options.percentsanity < 7 and not settings.allow_percentsanity_below_7:
        logging.info(
            f"Powerwash Simulator: {world.player_name} has {options.percentsanity} < 7 for percentsanity. since the host.yaml has allow_percentsanity_below_7 {settings.allow_percentsanity_below_7} percentsanity will be set to 7")
        options.percentsanity = Percentsanity(7)

    if options.has_objectsanity() and not settings.allow_objectsanity:
        raise_yaml_error(world.player_name,
                         "Objectsanity can not be enabled unless the host,yaml setting 'allow_objectsanity' is also enabled")

    if not options.has_objectsanity() and not options.has_percentsanity():
        raise_yaml_error(world.player_name,
                         "No sanities are listed, you must have one either: `Percentsanity` or `Objectsanity`")

    if not options.start_with_van or "Van" not in locations or (
            options.goal_type == 1 and "Van" in options.levels_to_goal and options.amount_of_levels_to_goal == 1):
        possible_locations = locations if options.goal_type != 1 else [loc for loc in locations if
                                                                       loc not in options.levels_to_goal]

        if len(possible_locations) == 0:
            if options.goal_type == 1 and options.amount_of_levels_to_goal == 1:
                logging.info(f"Powerwash Simulator: {world.player_name} will goal in sphere 1")

            possible_locations = locations

        world.starting_location = world.random.choice(possible_locations)


def set_local_fill(player_name, options, amount):
    logging.info(
        f"Powerwash Simulator: {player_name} has a local fill below the allowed minimum, it will be set to the minimum, if you want to allow below minimums then change the host.yaml setting `allow_below_localfill_minimums`")
    options.local_fill = LocalFill(amount)


def raise_yaml_error(player_name, error):
    raise OptionError(
        f"\n\n=== Powerwash Simulator YAML ERROR ===\nPowerwash Simulator: {player_name} {error}, PLEASE FIX YOUR YAML\n\n")
