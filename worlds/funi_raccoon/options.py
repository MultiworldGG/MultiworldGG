from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle, DefaultOnToggle, OptionSet, DeathLink, Range

class Goal(OptionSet):
    """
    Select one or more goals you will have to complete to win the run.
    orb: Act 4 access, the Orb, 3 Progressive Cooling Rods. Throw the orb in the pot.
    museum: Act 4 access, 100 dumpster items, the Belgium Waffle, 4 Progressive Mystical Dumbbells, 3 Progressive Cooling Rods. Throw the Belgium Waffle in the pot.
    fellowship: Act 4 access, the GREENISH ABOMINATION, the Priestess, 3 Progressive Cooling Rods. Throw the GREENISH ABOMINATION in the pot.
    lugh: Act 4 access, all 4 Mystical Gems. Jump into Lugh's hands at the Gully.
    """
    display_name = "Goal"
    valid_keys = ["orb", "museum", "fellowship", "lugh"]
    default = {"orb"}

class Eurosanity(Toggle):
    """
    Include the scattered Euro collectibles as randomizer locations.
    """
    display_name = "Eurosanity"


class Gemsanity(DefaultOnToggle):
    """
    Include the Mystical Gem locations as randomizer checks.
    Automatically enabled if is the Lugh goal is selected.
    """
    display_name = "Gemsanity"


class Hatsanity(DefaultOnToggle):
    """
    Include the hat locations as randomizer checks.
    """
    display_name = "Hatsanity"


class LughQuestLocking(Toggle):
    """
    When enabled, Lugh will not accept items you bring to him unless you have been sent that specific item.
    """
    display_name = "Lugh Quest Locking"
    
    
class DumpsterWeightBlocking(DefaultOnToggle):
    """
    When enabled (default), the dumpster enforces weight limits strictly: truck weight skips are
    removed from logic entirely and all dumbbell requirements always apply. You will not
    be able to use the truck to store heavier objects.
    When disabled, logic expects you to use the Kei Truck to bypass weight
    requirements in areas where the truck is accessible.
    """
    display_name = "Dumpster Weight Blocking"


class TrapToggle(DefaultOnToggle):
    """
    When enabled, trap items (Police Trap, Phone Ratio Trap) may appear in the item pool
    as filler, replacing some Euro drops.
    """
    display_name = "Trap Toggle"

class MuseumThreshold(Range):
    """
    Number of dumpster items required to unlock the Museum.
    NOTE: Changing these can sometimes lead to weird generation problems, but usually does not. If you run into problems, try generating with slightly different values.
    If you DO run into generation problems, let Jeff know.
    """
    display_name = "Museum Threshold"
    range_start = 5
    range_end = 25
    default = 15


class Act2Threshold(Range):
    """
    Number of dumpster items required to unlock Act 2 (Beenie HQ cluster).'
    NOTE: Changing these can sometimes lead to weird generation problems, but usually does not. If you run into problems, try generating with slightly different values.
    If you DO run into generation problems, let Jeff know.
    """
    display_name = "Act 2 Threshold"
    range_start = 10
    range_end = 50
    default = 25


class Act3Threshold(Range):
    """
    Number of dumpster items required to unlock Act 3 (Driving Test/Blimbo City, contains the Kei Truck).
    NOTE: Changing these can sometimes lead to weird generation problems, but usually does not. If you run into problems, try generating with slightly different values.
    If you DO run into generation problems, let Jeff know.
    """
    display_name = "Act 3 Threshold"
    range_start = 15
    range_end = 75
    default = 35


class Act4Threshold(Range):
    """
    Number of dumpster items required to unlock Act 4 (post-apocalypse areas, also requires the Kei Truck).
    NOTE: Changing these can sometimes lead to weird generation problems, but usually does not. If you run into problems, try generating with slightly different values.
    If you DO run into generation problems, let Jeff know.
    """
    display_name = "Act 4 Threshold"
    range_start = 20
    range_end = 100
    default = 50
    
class RaccoonColorRando(Toggle):
    """
    When enabled, the color of Raccoon will be randomized every time you enter a new area.
    """
    display_name = "Raccoon Color Randomization"


@dataclass
class FuniRaccoonOptions(PerGameCommonOptions):
    eurosanity: Eurosanity
    gemsanity: Gemsanity
    hatsanity: Hatsanity
    goal: Goal
    dumpster_weight_blocking: DumpsterWeightBlocking
    lugh_quest_locking: LughQuestLocking
    trap_toggle: TrapToggle
    museum_threshold: MuseumThreshold
    act2_threshold: Act2Threshold
    act3_threshold: Act3Threshold
    act4_threshold: Act4Threshold
    color_rando: RaccoonColorRando
