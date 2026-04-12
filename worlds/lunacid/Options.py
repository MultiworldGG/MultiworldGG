from dataclasses import dataclass
from typing import ClassVar, Protocol

from Options import Choice, Toggle, DeathLink, PerGameCommonOptions, Range, OptionSet, OptionDict
from worlds.lunacid.data.item_data import all_filler_items, default_filler_weights, default_trap_weights
from .strings.items import Trap, Coins


class LunacidOption(Protocol):
    internal_name: ClassVar[str]


class Ending(Choice):
    """Choose which ending is required to complete the game.
    Ending A: Reach Chamber of the Sleeper without all spells and awaken the Dreamer.
    Ending B: Obtain enough Strange Coins and enter the door located in the Labyrinth of Ash.
    Ending CD: Reach Chamber of the Sleeper and stare into the water pool.
    Ending E: Reach Chamber of the Sleeper with all spells after watching the White VHS Tape and awaken the Dreamer."""
    internal_name = "ending"
    display_name = "Ending"
    option_any_ending = 0
    option_ending_a = 1
    option_ending_b = 2
    option_ending_cd = 3
    option_ending_e = 4
    default = 1


class Class(Choice):
    """The class you play as.
    Note: The following classes are handled differently in the game:
    Vampire has free access to the cattle cells and the first area, so the first vampiric symbol is unnecessary.
    Custom is an advanced option.  If on a website its values will not be visible.  You know how it is smh."""
    internal_name = "starting_class"
    display_name = "Class"
    option_thief = 0
    option_knight = 1
    option_witch = 2
    option_vampire = 3
    option_undead = 4
    option_royal = 5
    option_cleric = 6
    option_shinobi = 7
    option_forsaken = 8
    option_custom = 9


class StartingArea(Choice):
    """Where the player starts.  You will always land in the starting spot in Hollow Basin but it will be blocked off.
    Demi will warp you to Wing's Rest, and the crystal will have the given starting area.
    If starting area is Accursed Tomb, Clive will give you an Oil Lantern."""
    internal_name = "starting_area"
    display_name = "Starting Area"
    option_basin = 0
    option_mire = 1
    option_forest = 2
    option_archives = 3
    option_tomb = 4
    option_castle = 5
    option_grotto = 6
    option_prison = 7
    option_arena = 8
    option_ash = 9
    default = 0


class EntranceRandomization(Toggle):
    """Shuffles the entrances around.  The only untouched entrances are crystal warps (including spell/item), entrance to Chamber of Fate, entrance to
    Grave of the Sleeper, and the doors of Tower of Abyss."""
    internal_name = "entrance_randomization"
    display_name = "Entrance Randomization"


class ProgressiveSymbols(Toggle):
    """Whether the Vampiric Symbols you acquire are split or progressive.  Setting to false is good on entrance randomization, otherwise
    can be annoying."""
    internal_name = "progressive_symbols"
    display_name = "Progressive Symbols"
    default = True


class RequiredStrangeCoins(Range):
    """Changes the required coins needed to open the door for Ending B."""
    internal_name = "required_strange_coin"
    display_name = "Required Strange Coins"
    range_start = 1
    range_end = 60
    default = 30


class TotalStrangeCoins(Range):
    """The total amount of strange coins placed in the multiworld.  Matches required if lower than it.
    Note: Filler will be replaced to compensate."""
    internal_name = "total_strange_coin"
    display_name = "Total Strange Coins"
    range_start = 1
    range_end = 60
    default = 30


class RandomElements(Toggle):
    """Randomizes the elements of almost all weapons and spells.  Guaranteed Poison ranged option.
    Wand of Power is not randomized (its randomly every element and tied to its function)."""
    internal_name = "random_elements"
    display_name = "Random Elements"

class RandomEquipStats(Choice):
    """Determines how the stats of weapons and spells are changed.
    Off: The setting is off, and all stats are vanilla.
    Shuffled: The weapon stats are shuffled amongst each other.
    Randomize: A random stat value given the existing stats is chosen."""
    internal_name = "random_equip_stats"
    display_name = "Random Equipment Stats"
    option_off = 0
    option_shuffle = 1
    option_randomize = 2
    default = 0

class EnemyRandomization(Toggle):
    """Shuffles the in-game enemies around. Each enemy in the game is replaced by some other enemy.
    THIS IS EXPERIMENTAL.  Report any weirdness or problems."""
    internal_name = "enemy_randomization"
    display_name = "Enemy Randomization"


class Shopsanity(Toggle):
    """Choose whether the unique items Sheryl the Crow sells are locations.
    Adds 9 locations."""
    internal_name = "shopsanity"
    display_name = "Shuffle Shop Items"


class Dropsanity(Choice):
    """Choose whether the items monsters drop are locations.
    Off: All drops are vanilla.
    Uniques: Only the unique first-drop items (weapons, spells, elixirs) are locations.  Adds 19 locations.
    Randomized: Each drop is a location.  WARNING SOME DROPS ARE HORRIBLE TO GET.  Adds 143 locations."""
    internal_name = "dropsanity"
    display_name = "Mob Drops"
    option_off = 0
    option_uniques = 1
    option_randomized = 2
    default = 0


class Quenchsanity(Toggle):
    """If a weapon can gain experience, if it is quenched, it returns a check.
    Quenching a weapon now no longer upgrades the weapons, and all quench weapons are added to the pool.
    Exceptions: Brittle Arming Sword repairs itself for the sake of the player, and Death Scythe is removed from the inventory as normal."""
    internal_name = "quenchsanity"
    display_name = "Quenchsanity"


class EtnasPupil(Toggle):
    """Become Etna's pupil!  As in, all alchemy creations are locations to check.  Cmon saying -sanity a lot is boring.
    If Dropsanity: Randomized is selected, each material is force placed on drops or alchemy spots to ensure repeatability."""
    internal_name = "etnas_pupil"
    display_name = "Etna's Pupil"


class Bookworm(Toggle):
    """Love reading?  Of course you do!  Every lore spot is a check.  Does not include basic signs.  All of this will be on the exam.
    Adds 67 locations."""
    internal_name = "bookworm"
    display_name = "Bookworm"


class Levelsanity(Toggle):
    """The experience you would gain instead gives you checks for every level.  Levels in the form of Deep Knowledge items are given to compensate which do give a level.
    Adds up to 100 locations (amount depends on starting class)."""
    internal_name = "levelsanity"
    display_name = "Levelsanity"


class Grasssanity(Toggle):
    """Every foliage object that normally drops something is a check.  The original drops do drop as normal for now.  Adds 502 locations."""
    internal_name = "grasssanity"
    display_name = "Grasssanity"


class Breakables(Toggle):
    """Every non-foliage breakable object that normally drops something is a check.  The original drops do drop as normal for now.  Adds 318 locations."""
    internal_name = "breakables"
    display_name = "Breakables"


class SwitchLocks(Toggle):
    """All physical switches (not mirages) are locked, and cannot be flipped without their relevant item.
    Note: Removes filler at random to compensate."""
    internal_name = "switch_lock"
    display_name = "Lock Switches"


class DoorLocks(Toggle):
    """All physical doors leading to new zones are locked, and cannot be opened without their relevant item.
    Note: Removes filler at random to compensate."""
    internal_name = "door_lock"
    display_name = "Lock Doors"


class SecretDoorLock(Toggle):
    """All secret doors are locked until receiving the Dusty Crystal Orb."""
    internal_name = "secret_door_lock"
    display_name = "Secret Door Lock"


class TricksAndGlitches(OptionSet):
    """Which tricks or glitches are considered in-logic.
    Lightless: All light source items are not necessary for dark areas.
    Rock Bridge Skip: Skipping the Vampiric Symbol doors in Castle Le Fanu with Rock Bridge is logical.
    Early Surface: Removes logic for reaching the surface entrances from Wing's Rest and Hollow Basin (requires about 20 DEX only).
    Barrier Skip: Skips requiring the Earth and Water Talismans.
    """
    internal_name = "tricks_and_glitches"
    display_name = "Tricks & Glitches"
    valid_keys = ["Lightless", "Rock Bridge Skip", "Early Surface", "Barrier Skip"]
    default = []


class Challenges(Choice):
    """These are optional challenges to make your run harder.  These may not be winnable.  If you turn these on in a public game, don't blame me, blame yourself.
    No EXP: You cannot level.  This trumps Levelsanity and turns it off.
    No Logic: There is no logic.  You will probably not win.  You've been warned.  But good to try and find skips.
    """
    internal_name = "challenges"
    display_name = "Challenges"
    option_off = 0
    option_exp = 1
    option_logic = 2
    default = 0

class Filler(OptionDict):
    """Lets you decide which filler are added to the game and their weights.  If the set is empty or all values are zero,
    Silver and Deep Knowledge will be forced included with weights of 1. Amount received in game is a random value between 1~5, favoring 1~2.
    Most filler is self-explanatory save the following:
    Deep Knowledge: You get 1 level.
    Weight of the Dream (Nothing): Is a nothing item.  Useful if you feel like other items make the game too easy.
    Demi's Gift for a Stranger: Attempts to give a random player a random gift.  If it fails or is a solo game, does nothing."""

    internal_name = "filler"
    display_name = "Filler"
    valid_keys = [item for item in default_filler_weights]
    default = default_filler_weights


class FillerLocalPercent(Range):
    """How much of filler is forced local?  Helpful when you don't want to fill the multiworld with your own junk but its fine if some of it bleeds out.
    Note that 0% just means none of it is *forced* to be local, not that it is all non-local."""
    internal_name = "filler_local_percent"
    display_name = "Filler Local Percent"
    range_start = 0
    range_end = 98
    default = 0


class Traps(OptionDict):
    """Lets you decide which traps are in your game and their weights.  If empty or all values are zero, same as having 0 Trap Percent.
    Certain joyous traps are allowed during Christmas, otherwise are ignored.
    Most traps are self-explanatory save:
    Rat Gang: Spawns 5 rats, and "We're the rats" plays.
    Health ViaI: It's the fake health vial item Patchouli sells you.  Drink it.  For her.
    Date With Death: Sent to DETHLAND map where Death will instantly kill you if you don't teleport out fast enough.
    This won't trigger unless you have Spirit Warp so you can actually have a chance to escape.
    Patchouli's Gift for a Stranger: Attempts to send a random player a random trap.  If it fails or is a solo game, does nothing.
    Acceptable Traps: "Bleed Trap", "Poison Trap", "Curse Trap", "Slowness Trap", "Blindness Trap", "Mana Drain Trap",
    "Health ViaI", "XP Drain Trap", "Rat Gang", "Date With Death Trap", Coal, Eggnog."""
    internal_name = "traps"
    display_name = "Traps"
    valid_keys = [trap for trap in default_trap_weights]
    default = default_trap_weights


class TrapPercent(Range):
    """Percent of filler items to be converted to traps."""
    internal_name = "trap_percent"
    display_name = "Trap Percent"
    range_start = 0
    range_end = 100
    default = 20


class CustomClass(OptionDict):
    """If 'Custom' is chosen for starting class, this is used as a stand-in for that information.
    If Name or Description is 'RANDOM', or any stat is -1, a random value will be supplied.
    Level ranges from 1 to 10.
    Stats (Strength to Resistance) range from 1 to 20.
    Resistances (Normal Res to Dark Res) range from 0 to 300."""
    internal_name = "custom_class"
    display_name = "Custom Class"
    valid_keys = ["Name", "Description", "Level", "Strength", "Speed", "Intelligence", "Defense", "Dexterity", "Resistance", "Normal Res",
                  "Fire Res", "Ice Res", "Poison Res", "Light Res", "Dark Res"]
    default = {
        "Name": "RANDOM",
        "Description": "RANDOM",
        "Level": -1,
        "Strength": -1,
        "Speed": -1,
        "Intelligence": -1,
        "Defense": -1,
        "Dexterity": -1,
        "Resistance": -1,
        "Normal Res": -1,
        "Fire Res": -1,
        "Ice Res": -1,
        "Poison Res": -1,
        "Light Res": -1,
        "Dark Res": -1,
    }


class SilverLink(Toggle):
    """Silver is linked into the RingLink system.  Watch as Luigi's Mansion gets too much money and mimics beat your ass."""
    internal_name = "silver_link"
    display_name = "Silver Link"


@dataclass
class LunacidOptions(PerGameCommonOptions):
    ending: Ending
    starting_class: Class
    starting_area: StartingArea
    entrance_randomization: EntranceRandomization
    progressive_symbols: ProgressiveSymbols
    random_elements: RandomElements
    random_equip_stats: RandomEquipStats
    enemy_randomization: EnemyRandomization
    required_strange_coin: RequiredStrangeCoins
    total_strange_coin: TotalStrangeCoins
    shopsanity: Shopsanity
    dropsanity: Dropsanity
    quenchsanity: Quenchsanity
    etnas_pupil: EtnasPupil
    bookworm: Bookworm
    levelsanity: Levelsanity
    grasssanity: Grasssanity
    breakables: Breakables
    secret_door_lock: SecretDoorLock
    switch_locks: SwitchLocks
    door_locks: DoorLocks
    tricks_and_glitches: TricksAndGlitches
    challenges: Challenges
    filler: Filler
    filler_local_percent: FillerLocalPercent
    traps: Traps
    trap_percent: TrapPercent
    custom_class: CustomClass
    silver_link: SilverLink
    death_link: DeathLink
