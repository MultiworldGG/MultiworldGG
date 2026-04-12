from random import choice
from typing import Union, List, Dict, TYPE_CHECKING
from Options import Choice, Range, Toggle, PerGameCommonOptions, DeathLink, FreeText, OptionList, NamedRange, Visibility
from dataclasses import dataclass

if TYPE_CHECKING:
    from . import AM2RWorld
else:
    AM2RWorld = object


class MetroidsRequired(Range):
    """Chose how many Metroids need to be killed or obtained to go through to the Omega Nest"""
    display_name = "Metroids Required for Omega Nest"
    range_start = 0
    range_end = 100
    default = 46


class MetroidsInPool(Range):
    """Chose how many Metroids will be in the pool, if Metroids are randomized.
    This will value will be ignored if smaller than the required amount"""
    display_name = "Total Metroids in Pool"
    range_start = 0
    range_end = 100
    default = 46


class LocationSettings(Choice):
    """Chose what items you want in the pool
    not including checks via the no_A6 will force them to be excluded
    not adding Metroids will force them to be vanilla and will not randomize them into item locations
    adding metroids but excluding A6 will leave the A6 and omega nest metroids vanilla but will leave the full amount in the pool"""
    display_name = "Locations to Check"
    default = 2
    option_items_no_A6 = 0
    option_items_and_A6 = 1
    option_add_metroids_no_A6 = 2
    option_add_metroids_and_A6 = 3

class MissileWeight(Range):
    """Change the weight of missiles in the item pool. Higher values will make missiles more common, lower values will make them rarer. Setting this to 0 will remove missiles from the item pool."""
    display_name = "Missile Weight"
    range_start = 0
    range_end = 100
    default = 44

class SuperMissileWeight(Range):
    """Change the weight of super missiles in the item pool. Higher values will make super missiles more common, lower values will make them rarer. Setting this to 0 will remove super missiles from the item pool."""
    display_name = "Super Missile Weight"
    range_start = 0
    range_end = 100
    default = 10

class PowerBombWeight(Range):
    """Change the weight of power bombs in the item pool. Higher values will make power bombs more common, lower values will make them rarer. Setting this to 0 will remove power bombs from the item pool."""
    display_name = "Power Bomb Weight"
    range_start = 0
    range_end = 100
    default = 10

class EnergyTankWeight(Range):
    """Change the weight of energy tanks in the item pool. Higher values will make energy tanks more common, lower values will make them rarer. Setting this to 0 will remove energy tanks from the item pool."""
    display_name = "Energy Tank Weight"
    range_start = 0
    range_end = 100
    default = 10


class TrapFillPercentage(Range):
    """Adds in slightly inconvenient traps into the item pool"""
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class RemoveFloodTrap(Toggle):
    """Removes Flood Traps from trap fill"""
    display_name = "Remove Flood Trap"


class RemoveTossTrap(Toggle):
    """There is a pipebomb in your mailbox"""
    display_name = "Remove Toss Trap"


class RemoveShortBeam(Toggle):
    """Remove muscle memory trap"""
    display_name = "Remove Short Beam"


class RemoveEMPTrap(Toggle):
    """Yes we know that it looks weird during the idle animation, but it's a vanilla bug"""
    display_name = "Remove EMP Trap"


class RemoveTouhouTrap(Toggle):
    """Removes Touhou Traps from trap fill"""
    display_name = "Remove Touhou Trap"


class RemoveOHKOTrap(Toggle):
    """Removes OHKO Traps from trap fill"""
    display_name = "Remove OHKO Trap"

class RemoveWrongWarpTrap(Toggle):
    """Removes Wrong Warp Traps from trap fill"""
    display_name = "Remove Wrong Warp Trap"

class RemoveIceTrap(Toggle):
    """Removes Ice Traps from trap fill"""
    display_name = "Remove Ice Trap"

class WrongWarpTrapSeed(NamedRange):
    """Seed for Wrong Warp Traps pick an integer from 0 to 2^64-1, or choose random for a random seed.

    Best used with an item link for wrong warp traps to share the maximum amount of random teleports"""
    display_name = "Wrong Warp Trap Seed"
    range_start = 0
    range_end = 2**64-1
    default = "random"


class TrapSprites(Choice):
    """Change what sprites are used for traps.
    Retro: Sprites styled from Fusion, Zero Mission and Super Metroid
    Super: Sprites styled from Super Metroid
    Chiny: Uses the "chiny tozo" sprites
    Tricky: Uses Sprites that are "tricky" to distinguish from non traps
    Evil: Uses Sprites that are "evil" to distinguish from non traps
    Vanilla: Uses the vanilla sprites from AM2R
    """
    display_name = "Item Sprites"
    default = 0
    option_All = 0
    option_Retro = 1
    option_Chiny = 2
    option_Tricky = 3
    option_Evil = 4
    option_Vanilla = 5

class Tozos(Range):
    """Enable dynamic Tozo items"""
    display_name = "Tozo Items"
    range_start = 0
    range_end = 100
    default = 0


class CustomDeathLinkMessages(OptionList):
    """Custom DeathLink Messages
    You can use {player} to include the name of the player whose death triggered the message.
    You can use {enemy} to include the name of the enemy that killed them.
    You can use {rand_player} to include the name of a random player in the game."""
    display_name = "Custom DeathLink Messages"
    default = ["That was totally your fault"]

class DeathlinkMessagePacks(OptionList):
    """Predefined DeathLink Message Packs
    valid_keys = {"default", "enemy", "ror2", "copypastas", "randplayer", "custom"}"""
    display_name = "Predefined DeathLink Message Packs"
    valid_keys = {"default", "enemy", "ror2", "terraria", "copypastas", "randplayer", "custom"}
    default = ["default"]

class ForceAprilFoolsSurprise(Toggle):
    """Forces the April Fools surprise to be active."""
    display_name = "Force April Fools Surprise"
    visibility = Visibility.spoiler


@dataclass
class AM2ROptions(PerGameCommonOptions):
    MetroidsRequired: MetroidsRequired
    MetroidsInPool: MetroidsInPool
    LocationSettings: LocationSettings
    MissileWeight: MissileWeight
    SuperMissileWeight: SuperMissileWeight
    PowerBombWeight: PowerBombWeight
    EnergyTankWeight: EnergyTankWeight
    TrapFillPercentage: TrapFillPercentage
    RemoveFloodTrap: RemoveFloodTrap
    RemoveTossTrap: RemoveTossTrap
    RemoveShortBeam: RemoveShortBeam
    RemoveEMPTrap: RemoveEMPTrap
    RemoveTouhouTrap: RemoveTouhouTrap
    RemoveOHKOTrap: RemoveOHKOTrap
    RemoveWrongWarpTrap: RemoveWrongWarpTrap
    RemoveIceTrap: RemoveIceTrap
    WrongWarpTrapSeed: WrongWarpTrapSeed
    TrapSprites: TrapSprites
    Tozos: Tozos
    CustomDeathLinkMessages: CustomDeathLinkMessages
    DeathlinkMessagePacks: DeathlinkMessagePacks
    DeathLink: DeathLink
    ForceAprilFoolsSurprise: ForceAprilFoolsSurprise
