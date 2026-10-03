from dataclasses import dataclass
from Options import DefaultOnToggle, Choice, PerGameCommonOptions, Toggle, ItemSet, Range
from .Items import item_names, default_shop_items


class ExpandedPool(DefaultOnToggle):
    """Puts room clear drops and take any caves into the pool of items and locations."""
    display_name = "Expanded Item Pool"


class TriforceLocations(Choice):
    """Where Triforce fragments can be located. Note that Triforce pieces
    obtained in a dungeon will heal and warp you out, while overworld Triforce pieces obtained will appear to have
    no immediate effect. This is normal."""
    display_name = "Triforce Locations"
    option_vanilla = 0
    option_dungeons = 1
    option_anywhere = 2


class StartingPosition(Choice):
    """How easy is the start of the game.
    Safe means a weapon is guaranteed in Starting Sword Cave.
    Unsafe means that a weapon is guaranteed between Starting Sword Cave, Letter Cave, and Armos Knight.
    Dangerous adds these level locations to the unsafe pool (if they exist):
#       Level 1 Compass, Level 2 Bomb Drop (Keese), Level 3 Key Drop (Zols Entrance), Level 3 Compass
    Very Dangerous is the same as dangerous except it doesn't guarantee a weapon. It will only mean progression
    will be there in single player seeds. In multi worlds, however, this means all bets are off and after checking
    the dangerous spots, you could be stuck until someone sends you a weapon"""
    display_name = "Starting Position"
    option_safe = 0
    option_unsafe = 1
    option_dangerous = 2
    option_very_dangerous = 3

class StartingWeapon(Choice):
    """For StartingPosition settings that guarantee a starting weapon, determines what that weapon will be.
    bluecandle makes the starting weapon a Blue Candle which is likely to be very difficult.
    sword makes the starting weapon a basic wooden Sword which is an average challenge.
    weapon makes the starting weapon any repeating weapon which on average will be very powerful."""
    display_name = "Starting Weapon"
    option_bluecandle = 0
    option_sword = 1
    option_weapon = 2
    default = 2

class BlueCandleFighting(Toggle):
    """This allows the Blue Candle to be used to fight enemies and farm resources.
    This can be very tedious and is only recommended for expert players."""
    display_name = "Blue Candle Fighting"

class BlueWizzrobeBombs(Toggle):
    """This allows defeating Blue Wizzrobes with bombs to be in logic.
    This requires skillful 10 counts and is only recommended for expert players."""
    display_name = "Blue Wizzrobe Bombs"

class CombatDifficulty(Choice):
    """This setting allows the player to decide how much equipment is needed to fight difficult enemies.
    Difficulty in this case is looking at how hard the player can hit (sword upgrades, Wand) and how
    defensive the player is (rings). Hearts are not considered as the player always respawns
    with 3 hearts and refilling health is often inconvenient. Expect the most help for fighting Blue
    Darknuts/Wizzrobes and hard bosses, some help for most enemies that take several hits, and
    minimal help for the weakest enemies.

    Very Easy: Expect both defense and offense upgrades for any multi-hit enemy.
    Easy: Expect the maximum stats for the hardest enemies and somewhat more help for other enemies than normal.
    Normal: The hardest fights guarantee you help to both defense and offense. Middling enemies get at least one piece of help.
    Hard: Only the hardest fights offer any help, and you can only be sure of one of defense or offense.
    Very Hard: You get minimal help for the hardest fights.
    Disabled: The logic does not care about combat difficulty and could make you do anything.
    Custom: Advanced options can be used to tune the difficulty in a player chosen way."""

    display_name = "Combat Difficulty"
    option_veryeasy = 0
    option_easy = 1
    option_normal = 2
    option_hard = 3
    option_veryhard = 4
    option_disabled = 5
    option_custom = 6
    default = 2

class HardEnemyCombatHelp(Range):
    """This is the amount of combat help guaranteed to the player to fight hard enemies.
    Each sword upgrade (beyond wooden) is worth one point, and each ring upgrade is worth one point.
    Wizzrobes and Ganon understand that the Wand is ineffective, but otherwise, the Wand is equivalent
    to the White Sword (one point, does not stack with sword upgrades).
    The hard enemy list is Blue Darknuts, Blue Wizzrobes, Blue Lanmolas, Manhandla, Gleeok, Patra, and Ganon."""
    display_name = "Hard Enemy Combat Help"
    range_start = 0
    range_end = 4
    default = 2

class MediumEnemyCombatHelp(Range):
    """This is the amount of combat help guaranteed to the player to fight medium enemies.
    Each sword upgrade (beyond wooden) is worth one point, and each ring upgrade is worth one point.
    Wizzrobes understand that the Wand is ineffective, but otherwise, the Wand is equivalent
    to the White Sword (one point, does not stack with sword upgrades).
    The medium enemy list is Red Darknuts, Red Wizzrobes, Red Lanmolas, Goriyas (all), Gibdos,
    Like Likes, Digdogger, and Super Ropes (2q only)."""
    display_name = "Medium Enemy Combat Help"
    range_start = 0
    range_end = 4
    default = 0

class EasyEnemyCombatHelp(Range):
    """This is the amount of combat help guaranteed to the player to fight easy enemies.
    Each sword upgrade (beyond wooden) is worth one point, and each ring upgrade is worth one point.
    The Wand is equivalent to the White Sword (one point, does not stack with sword upgrades).
    The easy enemy list is Keese, Vires, Gels, Zols, Stalfos, Wallmasters, Moldorms, Aquamentus,
    Dodongos, Gohma (all), and Ropes (1q only)."""
    display_name = "Easy Enemy Combat Help"
    range_start = 0
    range_end = 4
    default = 0

class PolsVoiceCombatHelp(Range):
    """This is the amount of combat help guaranteed to the player to fight Pols Voice without arrows.
    Each sword upgrade (beyond wooden) is worth one point, and each ring upgrade is worth one point.
    The Wand is equivalent to the White Sword (one point, does not stack with sword upgrades).
    Set this to 5 to make arrows always required to fight Pols Voice."""
    display_name = "Pols Voice Combat Help"
    range_start = 0
    range_end = 5
    default = 1

class LogicTrickq1d1KeyDoor(DefaultOnToggle):
    """This setting dictates whether entering and exiting First Quest Dungeon 1 to force open
    the key door in the first room can be required by logic."""
    display_name: "1st-1 Key Door Logic Trick"

class LogicTrickBlindDarkRooms(Toggle):
    """This setting dictates whether the player can be forced to navigate dark rooms without
    the ability to illuminate them."""
    display_name: "Blind Dark Rooms Logic Trick"

class EntranceShuffle(Choice):
    """Shuffle entrances around.
    Dungeons means only dungeon entrances will be shuffled with each other.
    Major means that dungeon entrances and major item locations (sword caves, take any caves, letter cave)
    will be shuffled with each other
    Open means that only dungeon entrances and open caves will be shuffled with each other.
    Major Open is a combination combines and shuffles both Major and Open locations.
    All means all entrances will be shuffled amongst each other. Starting Sword Cave will be in an open location
    and have a weapon.
    Warp Caves will be included as major locations if the Randomize Warp Caves setting is turned on
    """
    display_name = "Entrance Shuffle"
    option_off = 0
    option_dungeons = 1
    option_major = 2
    option_open = 3
    option_major_open = 4
    option_all = 5
    default = 0

class RandomizeWarpCaves(Toggle):
    """Include the Take Any Road caves in entrance randomization"""
    display_name = "Randomize Warp Caves"

class ShopItems(ItemSet):
    """Items that are guarnateed to be in a shop somewhere. If more items than the number of shop slots
    (fourteen) are picked, then a random remainder will be excluded. Small Keys are always included in an open shop.
    All items except Triforce Fragments are valid options."""
    valid_keys = item_names
    default = default_shop_items

class DialogSpeed(Choice):
    """The speed at which dialog advances.
    option_vanilla: 6 frames per letter
    option_fast: 2 frames per letter
    option_faster: 1 frame per letter
    """
    display_name = "Dialog Speed"
    option_vanilla = 0
    option_fast = 1
    option_faster = 2
    alias_normal = 0

@dataclass
class TlozOptions(PerGameCommonOptions):
    ExpandedPool: ExpandedPool
    TriforceLocations: TriforceLocations
    StartingPosition: StartingPosition
    StartingWeapon: StartingWeapon
    BlueCandleFighting: BlueCandleFighting
    BlueWizzrobeBombs: BlueWizzrobeBombs
    CombatDifficulty: CombatDifficulty
    HardEnemyCombatHelp: HardEnemyCombatHelp
    MediumEnemyCombatHelp: MediumEnemyCombatHelp
    EasyEnemyCombatHelp: EasyEnemyCombatHelp
    PolsVoiceCombatHelp: PolsVoiceCombatHelp
    LogicTrickq1d1KeyDoor: LogicTrickq1d1KeyDoor
    LogicTrickBlindDarkRooms: LogicTrickBlindDarkRooms
    EntranceShuffle: EntranceShuffle
    RandomizeWarpCaves: RandomizeWarpCaves
    ShopItems: ShopItems
    DialogSpeed: DialogSpeed
    
def is_open_cave_shuffled(option_value) -> bool:
    # A couple of things care if Starting Sword Cave is in the shuffle. This centralizes the check for that.
    # This also applies for the Blue Ring Shop.
    check_list = [EntranceShuffle.option_open, EntranceShuffle.option_major_open, EntranceShuffle.option_all]
    return option_value in check_list
