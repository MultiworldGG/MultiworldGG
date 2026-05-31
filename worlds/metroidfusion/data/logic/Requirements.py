from typing import TYPE_CHECKING

from .Requirement import Requirement, PONRRequirement

if TYPE_CHECKING:
    from ... import MetroidFusionOptions

level_1_e_tanks = 3
level_2_e_tanks = 5
level_3_e_tanks = 7
level_4_e_tanks = 10


#region Individual Item Requirements
#Morph Ball Items
class HasMorph(Requirement):
    """
    The player has Morph Ball.

    :param name: Defaults to "Has Morph Ball"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Morph Ball"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Morph Ball",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Morph Ball"})
        items_needed.add("Morph Ball")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasBombData(Requirement):
    """
    The player has Bomb Data.

    :param name: Defaults to "Has Bomb Data"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Bomb Data"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Bomb Data",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Bomb Data"})
        items_needed.add("Bomb Data")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasPowerBombData(Requirement):
    """
    The player has Power Bomb Data.

    :param name: Defaults to "Has Power Bomb Data"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Power Bomb Data"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Power Bomb Data",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Power Bomb Data"})
        items_needed.add("Power Bomb Data")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


#Suit Items
class HasVaria(Requirement):
    """
    The player has Varia Suit.

    :param name: Defaults to "Has Varia Suit"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Varia Suit"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Varia Suit",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Varia Suit"})
        items_needed.add("Varia Suit")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasGravity(Requirement):
    """
    The player has Gravity Suit.

    :param name: Defaults to "Has Gravity Suit"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Gravity Suit"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Gravity Suit",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Gravity Suit"})
        items_needed.add("Gravity Suit")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


#Mobility Items
# Reserved for when Wall Jump Boots enter the fray
class HasWallJump(Requirement):
    """
    The player has Wall Jump Boots.

    :param name: Defaults to "Has Wall Jump"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Wall Jump Boots"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Wall Jump",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Wall Jump Boots"})
        items_needed.add("Wall Jump Boots")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasHiJump(Requirement):
    """
    The player has Hi-Jump.

    :param name: Defaults to "Has Hi-Jump"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Hi-Jump"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Hi-Jump",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Hi-Jump"})
        items_needed.add("Hi-Jump")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasSpaceJump(Requirement):
    """
    The player has Space Jump.

    :param name: Defaults to "Has Space Jump"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Space Jump"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Space Jump",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Space Jump"})
        items_needed.add("Space Jump")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasSpeedBooster(Requirement):
    """
    The player has Speed Booster.

    :param name: Defaults to "Has Speed Booster"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Speed Booster"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Speed Booster",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Speed Booster"})
        items_needed.add("Speed Booster")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasScrewAttack(Requirement):
    """
    The player has Screw Attack.

    :param name: Defaults to "Has Screw Attack"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Screw Attack"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Screw Attack",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Screw Attack"})
        items_needed.add("Screw Attack")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


#Missile Items
class HasMissile(Requirement):
    """
    The player has Missile Data.

    :param name: Defaults to "Has Missile Data"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Missile Data"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Missile Data",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Missile Data"})
        items_needed.add("Missile Data")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasSuperMissile(Requirement):
    """
    The player has Super Missile.

    :param name: Defaults to "Has Super Missile"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Super Missile"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Super Missile",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Super Missile"})
        items_needed.add("Super Missile")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasIceMissile(Requirement):
    """
    The player has Ice Missile.

    :param name: Defaults to "Has Ice Missile"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Ice Missile"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Ice Missile",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Ice Missile"})
        items_needed.add("Ice Missile")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasDiffusionMissile(Requirement):
    """
    The player has Diffusion Missile.

    :param name: Defaults to "Has Diffusion Missile"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Diffusion Missile"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Diffusion Missile",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Diffusion Missile"})
        items_needed.add("Diffusion Missile")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


#Beam Items
class HasChargeBeam(Requirement):
    """
    The player has Charge Beam.

    :param name: Defaults to "Has Charge Beam"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Charge Beam"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Charge Beam",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Charge Beam"})
        items_needed.add("Charge Beam")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasWideBeam(Requirement):
    """
    The player has Wide Beam.

    :param name: Defaults to "Has Wide Beam"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Wide Beam"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Wide Beam",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Wide Beam"})
        items_needed.add("Wide Beam")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasPlasmaBeam(Requirement):
    """
    The player has Plasma Beam.

    :param name: Defaults to "Has Plasma Beam"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Plasma Beam"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Plasma Beam",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Plasma Beam"})
        items_needed.add("Plasma Beam")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasWaveBeam(Requirement):
    """
    The player has Wave Beam.

    :param name: Defaults to "Has Wave Beam"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Wave Beam"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Wave Beam",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Wave Beam"})
        items_needed.add("Wave Beam")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasIceBeam(Requirement):
    """
    The player has Ice Beam.

    :param name: Defaults to "Has Ice Beam"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Ice Beam"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Ice Beam",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Ice Beam"})
        items_needed.add("Ice Beam")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


#Keycard Items
class HasKeycard1(Requirement):
    """
    The player has Level 1 Keycard.

    :param name: Defaults to "Has Level 1 Keycard"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Level 1 Keycard"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Level 1 Keycard",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Level 1 Keycard"})
        items_needed.add("Level 1 Keycard")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasKeycard2(Requirement):
    """
    The player has Level 2 Keycard.

    :param name: Defaults to "Has Level 2 Keycard"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Level 2 Keycard"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Level 2 Keycard",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Level 2 Keycard"})
        items_needed.add("Level 2 Keycard")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasKeycard3(Requirement):
    """
    The player has Level 3 Keycard.

    :param name: Defaults to "Has Level 3 Keycard"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Level 3 Keycard"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Level 3 Keycard",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Level 3 Keycard"})
        items_needed.add("Level 3 Keycard")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


class HasKeycard4(Requirement):
    """
    The player has Level 4 Keycard.

    :param name: Defaults to "Has Level 4 Keycard"
    :param requirements:
    :key items_needed: A set of items that must be in the inventory.
        Defaults to ``{"Level 4 Keycard"}`` or adds that element to the passed set.
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Has Level 4 Keycard",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Level 4 Keycard"})
        items_needed.add("Level 4 Keycard")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)


#endregion

#region Combined Item Requirements
class CanBomb(HasMorph, HasBombData):
    """
    The player can lay bombs in Morph Ball.

    :param name: Defaults to "Can Bomb"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Bomb",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanPowerBomb(HasMorph, HasPowerBombData):
    """
    The player can lay at least one Power Bomb in Morph Ball.

    :param name: Defaults to "Can Power Bomb"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed: Defaults to 1
    """
    def __init__(self,
                 name="Can Power Bomb",
                 *requirements, **kwargs):
        kwargs['power_bomb_ammo_needed'] = kwargs.pop('power_bomb_ammo_needed', 1)
        super().__init__(name, *requirements, **kwargs)


class CanBallJump(HasMorph):
    """
    The player has Morph Ball and can either lay bombs or use Jumpball.

    :param name: Defaults to "Can Ball Jump"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Ball Jump",
                 *requirements, **kwargs):
        requirements += ([HasBombData(), HasHiJump()],)
        super().__init__(name, *requirements, **kwargs)


class CanJumpHigh(Requirement):
    """
    The player can jump higher than normal with Hi-Jump or Space Jump.

    :param name: Defaults to "Can Jump High"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Jump High",
                 *requirements, **kwargs):
        requirements += ([HasHiJump(), HasSpaceJump()],)
        super().__init__(name, *requirements, **kwargs)


class CanLavaDive(HasVaria, HasGravity):
    """
    The player can enter lava without taking damage.

    :param name: Defaults to "Can Lava Dive"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Lava Dive",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanJumpHighUnderwater(HasGravity):
    """
    The player can jump higher than normal and is unaffected by water physics.

    :param name: Defaults to "Can Jump High Underwater"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Jump High Underwater",
                 *requirements, **kwargs):
        requirements += ([CanJumpHigh()],)
        super().__init__(name, *requirements, **kwargs)


class CanSpeedBoosterUnderwater(HasGravity, HasSpeedBooster):
    """
    The player has Speed Booster and is unaffected by water physics.

    :param name: Defaults to "Can Speed Booster Underwater"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Speed Booster Underwater",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanScrewAttackUnderwater(HasGravity, HasScrewAttack):
    """
    The player has Screw Attack and is unaffected by water physics.

    :param name: Defaults to "Can Screw Attack Underwater"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Screw Attack Underwater",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanUseSuperMissile(HasMissile, HasSuperMissile):
    """
    The player has Super Missile and can fire them.

    :param name: Defaults to "Can Use Super Missile"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Use Super Missile",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanUseIceMissile(HasMissile, HasIceMissile):
    """
    The player has Ice Missile and can fire them.

    :param name: Defaults to "Can Use Ice Missile"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Use Ice Missile",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanUseDiffusionMissile(HasMissile, HasDiffusionMissile):
    """
    The player has Diffusion Missile and can fire them.

    :param name: Defaults to "Can Use Diffusion Missile"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Use Diffusion Missile",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanUseAllMissileUpgrades(HasMissile, HasSuperMissile, HasIceMissile, HasDiffusionMissile):
    """
    The player has all missile upgrades in the game and can fire them.

    :param name: Defaults to "Can Use All Missiles"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Use All Missiles",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanFreezeEnemies(Requirement):
    """
    The player is able to freeze enemies.

    :param name: Defaults to "Can Freeze Enemies"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Defines the minimum missiles needed to freeze all target enemies.
        Defaults to 1 and passes along to ``CanUseIceMissile`` and ``CanUseDiffusionMissile``.
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Freeze Enemies",
                 *requirements, **kwargs):
        missiles = kwargs.pop('missile_ammo_needed', 1)
        requirements += ([
                             HasIceBeam(),
                             CanUseIceMissile(missile_ammo_needed=missiles),
                             CanUseDiffusionMissile(missile_ammo_needed=missiles),
                         ],)
        super().__init__(name, *requirements, **kwargs)


class CanActivatePillar(Requirement):
    """
    The player can initiate a pillar extension via a bomb, Power Bomb, or Wave Beam shot.

    :param name: Defaults to "Can Activate Pillar"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed: Defaults to 1 and passes along to ``CanPowerBomb``
    """
    def __init__(self,
                 name="Can Activate Pillar",
                 *requirements, **kwargs):
        power_bombs = kwargs.pop('power_bomb_ammo_needed', 1)
        requirements += ([
            CanBomb(),
            CanPowerBomb(power_bomb_ammo_needed=power_bombs),
            HasWaveBeam()
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanDestroyBombBlocks(Requirement):
    """
    The player can destroy bomb blocks that aren't a chain.

    :param name: Defaults to "Can Destroy Bomb Blocks"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed: Defaults to 1 and passes along to ``CanPowerBomb``
    """
    def __init__(self,
                 name="Can Destroy Bomb Blocks",
                 *requirements, **kwargs):
        power_bombs = kwargs.pop('power_bomb_ammo_needed', 1)
        requirements += ([
            CanBomb(),
            CanPowerBomb(power_bomb_ammo_needed=power_bombs),
            HasScrewAttack()
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanDestroyBombBlocksUnderwater(HasGravity, CanDestroyBombBlocks):
    """
    The player can destroy bomb blocks that aren't a chain and is unaffected by water physics.

    :param name: Defaults to "Can Destroy Bomb Blocks Underwater"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Destroy Bomb Blocks Underwater",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanChargedWaveShot(HasChargeBeam, HasWaveBeam):
    """
    The player has Wave Beam and can fire a charged beam.

    :param name: Defaults to "Can Shoot Charged Wave Beam"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Shoot Charged Wave Beam",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanUseOneBeamUpgrade(Requirement):
    """
    The player has any one beam upgrade.

    :param name: Defaults to "Can Use One Beam Upgrade"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Use One Beam Upgrade",
                 *requirements, **kwargs):
        requirements += ([
                             HasChargeBeam(),
                             HasWideBeam(),
                             HasPlasmaBeam(),
                             HasWaveBeam(),
                             HasIceBeam()
                         ],)
        super().__init__(name, *requirements, **kwargs)


class CanUseTwoBeamUpgrades(Requirement):
    """
    The player has any two beam upgrades.

    :param name: Defaults to "Can Use Two Beam Upgrades"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Use Two Beam Upgrades",
                 *requirements, **kwargs):
        requirements += ([
                             Requirement("Charge Wide", items_needed={"Charge Beam", "Wide Beam"}),
                             Requirement("Charge Plasma", items_needed={"Charge Beam", "Plasma Beam"}),
                             Requirement("Charge Wave", items_needed={"Charge Beam", "Wave Beam"}),
                             Requirement("Charge Ice", items_needed={"Charge Beam", "Ice Beam"}),
                             Requirement("Wide Plasma", items_needed={"Wide Beam", "Plasma Beam"}),
                             Requirement("Wide Wave", items_needed={"Wide Beam", "Wave Beam"}),
                             Requirement("Wide Ice", items_needed={"Wide Beam", "Ice Beam"}),
                             Requirement("Plasma Wave", items_needed={"Plasma Beam", "Wave Beam"}),
                             Requirement("Plasma Ice", items_needed={"Plasma Beam", "Ice Beam"}),
                             Requirement("Wave Ice", items_needed={"Wave Beam", "Ice Beam"})
                         ],)
        super().__init__(name, *requirements, **kwargs)


class CanUseThreeBeamUpgrades(Requirement):
    """
    The player has any three beam upgrades.

    :param name: Defaults to "Can Use Three Beam Upgrades"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Use Three Beam Upgrades",
                 *requirements, **kwargs):
        requirements += ([
                             Requirement("Charge Wide Plasma",
                                         items_needed={"Charge Beam", "Wide Beam", "Plasma Beam"}),
                             Requirement("Charge Wide Wave",
                                         items_needed={"Charge Beam", "Wide Beam", "Wave Beam"}),
                             Requirement("Charge Wide Ice",
                                         items_needed={"Charge Beam", "Wide Beam", "Ice Beam"}),
                             Requirement("Charge Plasma Wave",
                                         items_needed={"Charge Beam", "Plasma Beam", "Wave Beam"}),
                             Requirement("Charge Plasma Ice",
                                         items_needed={"Charge Beam", "Plasma Beam", "Ice Beam"}),
                             Requirement("Charge Wave Ice",
                                         items_needed={"Charge Beam", "Wave Beam", "Ice Beam"}),
                             Requirement("Wide Plasma Wave",
                                         items_needed={"Wide Beam", "Plasma Beam", "Wave Beam"}),
                             Requirement("Wide Plasma Ice",
                                         items_needed={"Wide Beam", "Plasma Beam", "Ice Beam"}),
                             Requirement("Wide Wave Ice",
                                         items_needed={"Wide Beam", "Wave Beam", "Ice Beam"}),
                             Requirement("Plasma Wave Ice",
                                         items_needed={"Plasma Beam", "Wave Beam", "Ice Beam"})
                         ],)
        super().__init__(name, *requirements, **kwargs)


class CanUseFourBeamUpgrades(Requirement):
    """
    The player has any four beam upgrades.

    :param name: Defaults to "Can Use Four Beam Upgrades"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Use Four Beam Upgrades",
                 *requirements, **kwargs):
        requirements += ([
                             Requirement("Charge Wide Plasma Wave",
                                         items_needed={"Charge Beam", "Wide Beam", "Plasma Beam", "Wave Beam"}),
                             Requirement("Charge Wide Plasma Ice",
                                         items_needed={"Charge Beam", "Wide Beam", "Plasma Beam", "Ice Beam"}),
                             Requirement("Charge Wide Wave Ice",
                                         items_needed={"Charge Beam", "Wide Beam", "Wave Beam", "Ice Beam"}),
                             Requirement("Charge Plasma Wave Ice",
                                         items_needed={"Charge Beam", "Plasma Beam", "Wave Beam", "Ice Beam"}),
                             Requirement("Wide Plasma Wave Ice",
                                         items_needed={"Wide Beam", "Plasma Beam", "Wave Beam", "Ice Beam"}),
                         ],)
        super().__init__(name, *requirements, **kwargs)


class CanUseAllBeamUpgrades(HasChargeBeam, HasWideBeam, HasPlasmaBeam, HasWaveBeam, HasIceBeam):
    """
    The player has all beam upgrades.

    :param name: Defaults to "Can Use All Beam Upgrades"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Use All Beam Upgrades",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


#endregion

#region Combination Missile Upgrades for Damage Tracking

class CanDo45MissileDamage(HasMissile, HasSuperMissile, HasIceMissile, HasDiffusionMissile):
    """
    The player can deal 45 damage with each missile fired.

    :param name: Defaults to "Can Do 45 Missile Damage"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Defaults to 1
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do 45 Missile Damage",
                 *requirements, **kwargs):
        kwargs['missile_ammo_needed'] = kwargs.pop('missile_ammo_needed', 1)
        super().__init__(name, *requirements, **kwargs)


class CanDo40MissileDamage(HasMissile, HasSuperMissile, HasIceMissile):
    """
    The player can deal 40 damage with each missile fired.

    :param name: Defaults to "Can Do 40 Missile Damage"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Defaults to 1
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do 40 Missile Damage",
                 *requirements, **kwargs):
        kwargs['missile_ammo_needed'] = kwargs.pop('missile_ammo_needed', 1)
        super().__init__(name, *requirements, **kwargs)


class CanDo35MissileDamage(HasMissile, HasSuperMissile, HasDiffusionMissile):
    """
    The player can deal 35 damage with each missile fired.

    :param name: Defaults to "Can Do 35 Missile Damage"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Defaults to 1
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do 35 Missile Damage",
                 *requirements, **kwargs):
        kwargs['missile_ammo_needed'] = kwargs.pop('missile_ammo_needed', 1)
        super().__init__(name, *requirements, **kwargs)


class CanDo30MissileDamage(HasMissile, HasSuperMissile):
    """
    The player can deal 30 damage with each missile fired.

    :param name: Defaults to "Can Do 30 Missile Damage"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Defaults to 1
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do 30 Missile Damage",
                 *requirements, **kwargs):
        kwargs['missile_ammo_needed'] = kwargs.pop('missile_ammo_needed', 1)
        super().__init__(name, *requirements, **kwargs)


class CanDo25MissileDamage(HasMissile, HasIceMissile, HasDiffusionMissile):
    """
    The player can deal 25 damage with each missile fired.

    :param name: Defaults to "Can Do 25 Missile Damage"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Defaults to 1
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do 25 Missile Damage",
                 *requirements, **kwargs):
        kwargs['missile_ammo_needed'] = kwargs.pop('missile_ammo_needed', 1)
        super().__init__(name, *requirements, **kwargs)


class CanDo20MissileDamage(HasMissile, HasIceMissile):
    """
    The player can deal 20 damage with each missile fired.

    :param name: Defaults to "Can Do 20 Missile Damage"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Defaults to 1
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do 20 Missile Damage",
                 *requirements, **kwargs):
        kwargs['missile_ammo_needed'] = kwargs.pop('missile_ammo_needed', 1)
        super().__init__(name, *requirements, **kwargs)


class CanDo15MissileDamage(HasMissile, HasDiffusionMissile):
    """
    The player can deal 15 damage with each missile fired.

    :param name: Defaults to "Can Do 15 Missile Damage"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Defaults to 1
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do 15 Missile Damage",
                 *requirements, **kwargs):
        kwargs['missile_ammo_needed'] = kwargs.pop('missile_ammo_needed', 1)
        super().__init__(name, *requirements, **kwargs)


class CanDo10MissileDamage(HasMissile):
    """
    The player can deal 10 damage with each missile fired.

    :param name: Defaults to "Can Do 10 Missile Damage"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Defaults to 1
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do 10 Missile Damage",
                 *requirements, **kwargs):
        kwargs['missile_ammo_needed'] = kwargs.pop('missile_ammo_needed', 1)
        super().__init__(name, *requirements, **kwargs)

class AnyMissileRequirement(HasMissile):
    """
    The player can defeat enemies with total health ``enemy_hp`` using any combination of missile upgrades.

    :param name: Defaults to "Can Clear With Missiles"
    :param enemy_hp: Defaults to 1
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Automatically calculated based on ``enemy_hp``
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Clear With Missiles",
                 enemy_hp: int = 1,
                 *requirements, **kwargs):
        requirements += ([
            CanDo10MissileDamage(missile_ammo_needed=-int(-(enemy_hp / 10) // 1)),
            CanDo15MissileDamage(missile_ammo_needed=-int(-(enemy_hp / 15) // 1)),
            CanDo20MissileDamage(missile_ammo_needed=-int(-(enemy_hp / 20) // 1)),
            CanDo25MissileDamage(missile_ammo_needed=-int(-(enemy_hp / 25) // 1)),
            CanDo30MissileDamage(missile_ammo_needed=-int(-(enemy_hp / 30) // 1)),
            CanDo35MissileDamage(missile_ammo_needed=-int(-(enemy_hp / 35) // 1)),
            CanDo40MissileDamage(missile_ammo_needed=-int(-(enemy_hp / 40) // 1)),
            CanDo45MissileDamage(missile_ammo_needed=-int(-(enemy_hp / 45) // 1))
        ],)
        super().__init__(name, *requirements, **kwargs)

#endregion

#region Enemy Requirements
class CanDamageSmallGeron(AnyMissileRequirement):
    """
    The player can kill a Small Geron weak to any Missiles.

    :param name: Defaults to "Can Damage Small Geron"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Automatically calculated based on missile upgrades.
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Damage Small Geron",
                 *requirements, **kwargs):
        super().__init__(name, 30, *requirements, **kwargs)


class CanDamageMediumGeron(CanUseSuperMissile):
    """
    The player can kill a Medium Geron weak to Super Missiles.

    :param name: Defaults to "Can Damage Medium Geron"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Automatically calculated based on missile upgrades.
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Damage Medium Geron",
                 *requirements, **kwargs):
        requirements += ([
            CanDo45MissileDamage(missile_ammo_needed=2),
            CanDo40MissileDamage(missile_ammo_needed=3),
            CanDo35MissileDamage(missile_ammo_needed=3),
            CanDo30MissileDamage(missile_ammo_needed=3),
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanDamageLargeGeron(CanPowerBomb):
    """
    The player can kill a Large Geron weak to Power Bombs.

    :param name: Defaults to "Can Damage Large Geron"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed: Defaults to 1
    """
    def __init__(self,
                 name="Can Damage Large Geron",
                 *requirements, **kwargs):
        kwargs['power_bomb_ammo_needed'] = kwargs.pop('power_bomb_ammo_needed', 1)
        super().__init__(name, *requirements, **kwargs)


class CanDamageStabilizer(Requirement):
    """
    The player can kill the X Parasites clogging Atmospheric Stabilizers found in Sector 1.

    :param name: Defaults to "Can Damage Stabilizer"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Automatically calculated based on missile upgrades.
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Damage Stabilizer",
                 *requirements, **kwargs):
        requirements += ([
            AnyMissileRequirement(None, 21),
            HasChargeBeam()
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanDamageAnyGeron(Requirement):
    """
    The player can kill any Geron with Power Bomb or Screw Attack
    and does not have NerfGeronWeaknesses YAML option enabled.

    :param name: Defaults to "Can Damage Any Geron"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Damage Any Geron",
                 *requirements, **kwargs):
        requirements += ([CanPowerBomb(), HasScrewAttack()],)
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions"):
        return not options.NerfGeronWeaknesses


class CanDamageToughEnemy(Requirement):
    """
    The player can defeat beam-resistant enemies with total health ``enemy_hp``.
    Damage methods are Charge Beam, Missiles, Bombs (not yet implemented), Power Bombs, or Screw Attack.

    :param name: Defaults to "Can Damage Tough Enemy".
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Auto-calculates minimum missiles based on ``enemy_hp`` and missile upgrades.
        Disables missile requirement if ``immunities`` contains "Missile".
    :key power_bomb_ammo_needed: Auto-calculates minimum power bombs needed based on ``enemy_hp``.
        Disables power bomb requirement if ``immunities`` contains "Power Bomb".
    :key behind_wall: A boolean toggling requirement behavior to treat the enemy behind a wall. Defaults to False.
    :key immunities: A set of items this enemy is immune to damage from.
        Valid items are "Charge Beam", "Missile", "Bomb", "Power Bomb", and "Screw Attack".
        Defaults to an empty set.
    :key enemy_hp: An integer representing the health of the enemy or enemies to defeat. Defaults to 1.
    """
    def __init__(self,
                 name="Can Damage Tough Enemy",
                 *requirements, **kwargs):
        enemy_hp: int = kwargs.pop('enemy_hp', 1)
        max_pb_ammo_value = -int(-(enemy_hp / 50) // 1)
        immunities: set[str] = kwargs.pop('immunities', set())
        immunities.discard("Beam")
        for immunity in immunities:
            assert immunity in {"Charge Beam", "Missile", "Bomb", "Power Bomb", "Screw Attack"}
        if {"Charge Beam", "Missile", "Bomb", "Power Bomb", "Screw Attack"}.issubset(immunities):
            raise ValueError("Cannot make a Requirement for a beam-resistant enemy immune to all attack forms!")
        end_list: list[Requirement] = []
        if kwargs.pop('behind_wall', False):
            if "Power Bomb" not in immunities:
                end_list.append(CanPowerBomb(power_bomb_ammo_needed=max_pb_ammo_value))
            if "Charge Beam" not in immunities:
                end_list.append(CanChargedWaveShot())
        else:
            # if {"Power Bomb", "Missile"}.isdisjoint(immunities):
            #     end_list.extend([
            #         CanPowerBomb(None, [
            #             AnyMissileRequirement(None, enemy_hp - (pb_ammo * 50))
            #         ], power_bomb_ammo_needed=pb_ammo)
            #         for pb_ammo in range(1, max_pb_ammo_value)
            #     ])
            if "Power Bomb" not in immunities:
                end_list.append(CanPowerBomb(power_bomb_ammo_needed=max_pb_ammo_value))
            if "Missile" not in immunities:
                end_list.append(AnyMissileRequirement(None, enemy_hp))
            if "Charge Beam" not in immunities:
                end_list.append(HasChargeBeam())
            if "Screw Attack" not in immunities:
                end_list.append(HasScrewAttack())
            # Bomb not implemented here due to masochistic and tedious nature. Awaiting masochist difficulty settings.
            # if not {"Bomb"}.issubset(immunities):
            #     end_list.append(CanDoMasochistCombat())
        requirements += (end_list,)
        super().__init__(name, *requirements, **kwargs)


class CanDefeatGerubus(CanDamageToughEnemy):
    """
    The player can kill a number of Gerubus enemies equal to ``count``.

    :param name: Defaults to "Can Defeat Gerubus"
    :param count: Defaults to 1
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Automatically calculated based on missile upgrades and ``count``
    :key power_bomb_ammo_needed: Disabled
    """
    def __init__(self,
                 name = "Can Defeat Gerubus",
                 count: int = 1,
                 *requirements, **kwargs):
        kwargs.update({
            'enemy_hp': 45 * count,
            'immunities': {"Beam", "Charge Beam", "Bomb", "Power Bomb"}
        })
        super().__init__(name, *requirements, **kwargs)


#endregion

#region Boss Requirements
class CanDamageCoreX(HasMissile):
    """
    The player can damage a boss in the Core X state. Players can refill missile ammo by attempting to damage the
    Core X shell with anything but missiles and collecting the spawning X parasites.

    :param name: Defaults to "Can Damage Core X"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Damage Core X",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanFightBoss(CanDamageCoreX):
    """
    The player can fight a boss and win.

    :param name: Defaults to "Can Fight Boss"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    :key boss_hp: Defines how much health must be depleted on the boss to push it into the Core X state. Defaults to 1.
    :key immunities: A set of damage methods the boss is immune to.
        Valid categories are "Beam", "Charge Beam", "Missile", "Bomb", "Power Bomb", and "Screw Attack".
        Defaults to an empty set.
    """
    def __init__(self,
                 name="Can Fight Boss",
                 *requirements, **kwargs):
        immunities: set[str] = kwargs.pop('immunities', set())
        for immunity in immunities:
            assert immunity in {"Beam", "Charge Beam", "Missile", "Bomb", "Power Bomb", "Screw Attack"}
        requirements_list: list[Requirement] = []
        if "Beam" not in immunities:
            requirements_list.append(Requirement("Push Boss into Core X state - Beam Only"))
        requirements_list.append(
            CanDamageToughEnemy("Push Boss into Core X state",
                                enemy_hp=kwargs.pop('boss_hp', 1),
                                immunities=immunities)
        )
        requirements += (requirements_list,)
        super().__init__(name, *requirements, **kwargs)


class CanFightEarlyGameBoss(CanFightBoss):
    """
    The player can fight an early game boss and win.

    :param name: Defaults to "Can Fight Early Game Boss"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed: Defaults to minimum value ``level_1_e_tanks``, or 3
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    :key boss_hp: Defines how much health must be depleted on the boss to push it into the Core X state. Defaults to 1.
    :key immunities: A set of damage methods the boss is immune to.
        Valid categories are "Beam", "Charge Beam", "Missile", "Bomb", "Power Bomb", and "Screw Attack".
        Defaults to an empty set.
    """
    def __init__(self,
                 name="Can Fight Early Game Boss",
                 *requirements, **kwargs):
        kwargs['energy_tanks_needed'] = max(kwargs.pop('energy_tanks_needed', 0), level_1_e_tanks)
        super().__init__(name, *requirements, **kwargs)


class CanFightMidGameBoss(CanFightBoss, CanUseSuperMissile, HasChargeBeam):
    """
    The player can fight a mid-game boss and win.

    :param name: Defaults to "Can Fight Mid Game Boss"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed: Defaults to minimum value ``level_2_e_tanks``, or 5
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    :key boss_hp: Defines how much health must be depleted on the boss to push it into the Core X state. Defaults to 1.
    :key immunities: A set of damage methods the boss is immune to.
        Valid categories are "Beam", "Charge Beam", "Missile", "Bomb", "Power Bomb", and "Screw Attack".
        Defaults to an empty set.
    """
    def __init__(self,
                 name="Can Fight Mid Game Boss",
                 *requirements, **kwargs):
        kwargs['energy_tanks_needed'] = max(kwargs.pop('energy_tanks_needed', 0), level_2_e_tanks)
        super().__init__(name, *requirements, **kwargs)


class CanFightLateGameBoss(CanFightMidGameBoss, HasPlasmaBeam, HasSpaceJump):
    """
    The player can fight a late game boss and win.

    :param name: Defaults to "Can Fight Late Game Boss"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed: Defaults to minimum value ``level_3_e_tanks``, or 7
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    :key boss_hp: Defines how much health must be depleted on the boss to push it into the Core X state. Defaults to 1.
    :key immunities: A set of damage methods the boss is immune to.
        Valid categories are "Beam", "Charge Beam", "Missile", "Bomb", "Power Bomb", and "Screw Attack".
        Defaults to an empty set.
    """
    def __init__(self,
                 name="Can Fight Late Game Boss",
                 *requirements, **kwargs):
        kwargs['energy_tanks_needed'] = max(kwargs.pop('energy_tanks_needed', 0), level_3_e_tanks)
        super().__init__(name, *requirements, **kwargs)


#endregion

#region Trick Options Requirements

class CanDoBeginnerShinespark(HasSpeedBooster):
    """
    The player can perform a shinespark with YAML option ``ShinesparkTrickDifficulty: beginner``.

    :param name: Defaults to "Can Do Beginner Shinespark"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do Beginner Shinespark",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Shinespark Trick - Beginner"})
        items_needed.add("Shinespark Trick - Beginner")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.ShinesparkTrickDifficulty >= 1  #options.ShinesparkTrickDifficulty.option_beginner


class CanDoAdvancedShinespark(HasSpeedBooster):
    """
    The player can perform a shinespark with YAML option ``ShinesparkTrickDifficulty: advanced``.

    :param name: Defaults to "Can Do Advanced Shinespark"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do Advanced Shinespark",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Shinespark Trick - Advanced"})
        items_needed.add("Shinespark Trick - Advanced")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.ShinesparkTrickDifficulty >= 2  #options.ShinesparkTrickDifficulty.option_advanced

# Prepared in advance of trick setting. Currently unreachable due to lack of setting.
class CanDoExpertShinespark(HasSpeedBooster):
    """
    The player can perform a shinespark with YAML option ``ShinesparkTrickDifficulty: expert``.

    :param name: Defaults to "Can Do Expert Shinespark"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do Expert Shinespark",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Shinespark Trick - Expert"})
        items_needed.add("Shinespark Trick - Expert")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.ShinesparkTrickDifficulty >= 3  #options.ShinesparkTrickDifficulty.option_expert


class CanDoSimpleWallJump(HasWallJump):
    """
    The player can perform a wall jump with YAML option ``WallJumpTrickDifficulty: beginner``.

    :param name: Defaults to "Can Do Simple Wall Jump"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do Simple Wall Jump",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Wall Jump Trick - Beginner"})
        items_needed.add("Wall Jump Trick - Beginner")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= 1  #options.WallJumpTrickDifficulty.option_beginner


class CanDoAdvancedWallJump(HasWallJump):
    """
    The player can perform a wall jump with YAML option ``WallJumpTrickDifficulty: advanced``.

    :param name: Defaults to "Can Do Advanced Wall Jump"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do Advanced Wall Jump",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Wall Jump Trick - Advanced"})
        items_needed.add("Wall Jump Trick - Advanced")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= 2  #options.WallJumpTrickDifficulty.option_advanced


class CanDoExpertWallJump(HasWallJump):
    """
    The player can perform a wall jump with YAML option ``WallJumpTrickDifficulty: expert``.

    :param name: Defaults to "Can Do Expert Wall Jump"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do Expert Wall Jump",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Wall Jump Trick - Expert"})
        items_needed.add("Wall Jump Trick - Expert")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= 3  #options.WallJumpTrickDifficulty.option_expert


class CanDoAdvancedCombat(Requirement):
    """
    The player can perform advanced combat maneuvers with YAML option ``CombatDifficulty: advanced``.

    :param name: Defaults to "Can Do Advanced Combat"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do Advanced Combat",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Combat - Advanced"})
        items_needed.add("Combat - Advanced")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.CombatDifficulty >= 1  #options.CombatDifficulty.option_advanced


class CanDoExpertCombat(Requirement):
    """
    The player can perform expert combat maneuvers with YAML option ``CombatDifficulty: expert``.

    :param name: Defaults to "Can Do Expert Combat"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do Expert Combat",
                 *requirements, **kwargs):
        items_needed: set[str] = kwargs.pop('items_needed', {"Combat - Expert"})
        items_needed.add("Combat - Expert")
        kwargs['items_needed'] = items_needed
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.CombatDifficulty >= 2  #options.CombatDifficulty.option_expert


class CanFightMidGameBossOnAdvanced(CanDoAdvancedCombat, CanFightBoss):
    """
    The player can fight a mid-game boss and win with YAML option ``CombatDifficulty: advanced``.

    :param name: Defaults to "Can Fight Mid Game Boss On Advanced"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed: Defaults to minimum value ``level_1_e_tanks``, or 3
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    :key boss_hp: Defines how much health must be depleted on the boss to push it into the Core X state. Defaults to 1.
    :key immunities: A set of damage methods the boss is immune to.
        Valid categories are "Beam", "Charge Beam", "Missile", "Bomb", "Power Bomb", and "Screw Attack".
        Defaults to an empty set.
    """
    def __init__(self,
                 name="Can Fight Mid Game Boss On Advanced",
                 *requirements, **kwargs):
        kwargs['energy_tanks_needed'] = max(kwargs.pop('energy_tanks_needed', 0), level_1_e_tanks)
        super().__init__(name, *requirements, **kwargs)


class CanFightLateGameBossOnAdvanced(CanDoAdvancedCombat, CanFightMidGameBoss):
    """
    The player can fight a late game boss and win with YAML option ``CombatDifficulty: advanced``.

    :param name: Defaults to "Can Fight Late Game Boss On Advanced"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed: Defaults to minimum value ``level_2_e_tanks``, or 5
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    :key boss_hp: Defines how much health must be depleted on the boss to push it into the Core X state. Defaults to 1.
    :key immunities: A set of damage methods the boss is immune to.
        Valid categories are "Beam", "Charge Beam", "Missile", "Bomb", "Power Bomb", and "Screw Attack".
        Defaults to an empty set.
    """
    def __init__(self,
                 name="Can Fight Late Game Boss on Advanced",
                 *requirements, **kwargs):
        kwargs['energy_tanks_needed'] = max(kwargs.pop('energy_tanks_needed', 0), level_2_e_tanks)
        super().__init__(name, *requirements, **kwargs)


class CanFightBossOnExpert(CanDoExpertCombat, CanFightBoss):
    """
    The player can fight any boss and win with YAML option ``CombatDifficulty: expert``.

    :param name: Defaults to "Can Fight Boss On Expert"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    :key boss_hp: Defines how much health must be depleted on the boss to push it into the Core X state. Defaults to 1.
    :key immunities: A set of damage methods the boss is immune to.
        Valid categories are "Beam", "Charge Beam", "Missile", "Bomb", "Power Bomb", and "Screw Attack".
        Defaults to an empty set.
    """
    def __init__(self,
                 name="Can Fight Boss on Expert",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class SectorHubLevel1KeycardRequirement(HasKeycard1):
    """
    The player can access Sector Hub Elevators normally locked behind Level 1 Security Doors.

    Requires YAML options:

    * ``GameMode: custom`` AND ``OpenSectorElevators: false``
    * ``GameMode: vanilla``

    :param name: Defaults to "Sector Hub Level 1 Keycard Requirement"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Sector Hub Level 1 Keycard Requirement",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions"):
        if options.GameMode == options.GameMode.option_custom:
            return not options.OpenSectorElevators
        else:
            return options.GameMode == 0  #options.GameMode.option_vanilla


class SectorHubLevel1And2KeycardRequirement(SectorHubLevel1KeycardRequirement, HasKeycard2):
    """
    The player can access Sector Hub Elevators normally locked behind Level 1 Security Doors and Level 2 Security Doors.

    Requires YAML options:

    * ``GameMode: custom`` AND ``OpenSectorElevators: false``
    * ``GameMode: vanilla``

    :param name: Defaults to "Sector Hub Level 1 and 2 Keycard Requirement"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Sector Hub Level 1 and 2 Keycard Requirement",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


# endregion

#region Prefab Requirements

class CanCollectCrumbleCity(Requirement):
    """
    The player can access item locations in Sector 2 - Crumble City.

    :param name: Defaults to "Can Collect Crumble City"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Collect Crumble City",
                 *requirements, **kwargs):
        requirements += ([
            Requirement("Can Collect Crumble City Item", [
                HasScrewAttack("Break into Crumble City and Collect Item", [
                    HasSpaceJump("Fly"),
                    # Awaiting trick option evaluation. This is masochistic to perform.
                    # [CanDoExpertCrumbleJank()]
                    ]
                    # MARS changes the door type to a Level 0 Security Door.
                    #    This is the original door requirement.
                    # , [HasKeycard4()]
                )
            ])
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanObtainRipperTower(Requirement):
    """
    The player can access item locations in Sector 2 - Ripper Tower.

    :param name: Defaults to "Can Obtain Ripper Tower"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Obtain Ripper Tower",
                 *requirements, **kwargs):
        requirements += ([
            Requirement("Can Obtain Ripper Tower Item",
                        [CanFreezeEnemies(missile_ammo_needed=2)],
                        items_needed={"Morph Ball"})
        ],)
        super().__init__(name, *requirements, **kwargs)


class PONREnterBobsTunnelFromAbove(PONRRequirement, HasMorph, HasKeycard2):
    """
    The player can access the tunnel from above in Sector 3 - Bob's Abode.

    :param name: Defaults to "Can Enter Bob's Tunnel From Above"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Enter Bob's Tunnel From Above",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanFightBOX(CanDamageToughEnemy):
    """
    The player can fight BOX 1 and win. BOX has 300 HP.

    :param name: Defaults to "Can Fight BOX"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed: Defaults to minimum value ``level_2_e_tanks``, or 5
    :key missile_ammo_needed: Defaults to enable auto-calculation of missile requirements in
        ``CanDamageToughEnemy``
    :key power_bomb_ammo_needed: Disabled. BOX is immune to Power Bombs
    """
    def __init__(self,
                 name="Can Fight BOX",
                 *requirements, **kwargs):
        requirements += ([CanJumpHigh(), CanDoSimpleWallJump()],)
        kwargs.update({
            'energy_tanks_needed': max(kwargs.pop('energy_tanks_needed', 0), level_2_e_tanks),
            'immunities': {"Beam", "Bomb", "Power Bomb", "Screw Attack"},
            'enemy_hp': 300,
        })
        super().__init__(name, *requirements, **kwargs)


class CanClimbSector3AlcoveRight(Requirement):
    """
    The player can access the door from the bottom of Sector 3 - Alcove.

    :param name: Defaults to "Can Climb Sector 3 Alcove Right"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Climb Sector 3 Alcove Right",
                 *requirements, **kwargs):
        requirements += ([
            # From below the items
            CanBomb(),
            CanPowerBomb()
        ], [
            # From bottom right section
            HasSpaceJump(),
            CanFreezeEnemies("Use Sidehopper as platform", [
                CanDoSimpleWallJump(),
                HasHiJump()
            ]),
            CanDoAdvancedWallJump("Wall Jumping without Sidehopper", [
                HasHiJump(),
                CanBallJump("Jump out of tunnel, then Wall Jump")
            ])
        ], [
            # Dealing with Sidehoppers
            CanDamageToughEnemy("Kill Sidehoppers", enemy_hp=(24 * 3)),
            CanFreezeEnemies("Freeze Sidehoppers", missile_ammo_needed=3),
            CanDoAdvancedCombat("Dodge Sidehoppers")
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanClimbSector3AlcoveLeft(Requirement):
    """
    The player can access the upper middle pocket from the bottom of Sector 3 - Alcove.

    :param name: Defaults to "Can Climb Sector 3 Alcove Left"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Climb Sector 3 Alcove Left",
                 *requirements, **kwargs):
        requirements += ([
            # Get height to destroy bomb blocks
            HasScrewAttack("Use Screw Attack", [
                HasSpaceJump("Fly"),
                CanDoAdvancedWallJump("Wall Jump Good", [
                    HasHiJump()
                ]),
                CanActivatePillar("Start from on Pillar")
            ]),
            CanPowerBomb("Lay Waste and Use Pillar", power_bomb_ammo_needed=2),
            CanBomb("Use Bombs with Pillar")
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanDoBoiler(CanDamageCoreX):
    """
    The player can traverse Sector 3 and enter the Boiler Control Terminal Room.

    :param name: Defaults to "Can Do Boiler"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed: Defaults to minimum value ``level_2_e_tanks``, or 5
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do Boiler",
                 *requirements, **kwargs):
        requirements += ([
            # Required to get to the Boiler Control Room
            # Main blocker is Pyrochamber Access
            HasSpaceJump("Fly"),
            CanFreezeEnemies("Freeze Funes", [
                CanDoSimpleWallJump(),
                HasHiJump()
            ], missile_ammo_needed=2),
        ], [
            CanDamageGadora()
        ])
        kwargs['energy_tanks_needed'] = max(kwargs.pop('energy_tanks_needed', 0), level_2_e_tanks)
        super().__init__(name, *requirements, **kwargs)


class CanGetSovaProcessingItem(HasMorph):
    """
    The player can access item locations in Sector 3 - Sova Processing.

    :param name: Defaults to "Can Get Sova Processing Item"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Get Sova Processing Item",
                 *requirements, **kwargs):
        requirements += ([
            HasSpaceJump(),
            CanFreezeEnemies(missile_ammo_needed=4),
            CanDoAdvancedShinespark("Diagonal-Right Shinespark", [
                CanLavaDive()
            ])
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanActivatePumpControl(Requirement):
    """
    The player can access and activate the Pump Control Terminal in Sector 4.

    :param name: Defaults to "Can Activate Pump Control"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Activate Pump Control",
                 *requirements, **kwargs):
        requirements += ([
            HasKeycard1("Enter Pump Control", [
                # Getting to the Terminal
                HasSpeedBooster("Break through Speed Booster Blocks"),
                HasGravity("Use Drain Pipe below Pump Control Terminal", [
                    # Get in and out of Item Nook
                    CanBallJump()
                ], [
                    # Climb Up Drain Pipe
                    HasSpaceJump(),
                    CanDoSimpleWallJump(items_needed={"Hi-Jump"})
                ], energy_tanks_needed=level_2_e_tanks)
            ], [
                # Leaving
                CanBallJump("Use Tunnel"),
                # Shinespark will risk softlocking
                CanDoAdvancedShinespark("Charge Shinespark and Use Terminal")
            ], energy_tanks_needed=level_1_e_tanks),
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanDoScizerSanctuary(Requirement):
    """
    The player can unlock the door in Sector 4 - Scizer Sanctuary to Sanctuary Cache.

    :param name: Defaults to "Can Do Scizer Sanctuary"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Do Scizer Sanctuary",
                 *requirements, **kwargs):
        requirements += ([
            CanDamageToughEnemy("Kill the Golden Crabs and Unlock Door", [
                # Kill the caged crabs
                HasWaveBeam(),
                CanPowerBomb(),
                CanDoAdvancedCombat("Use Flare from Charge Beam",
                                    items_needed={"Charge Beam"})
            ], [
                # Kill the gold crabs
                CanChargedWaveShot(),
                HasMissile("Open Tunnel", [
                    CanDoAdvancedCombat("Thread the Needle"),
                    HasMorph("Enter Tunnel into Golden Crab Enclosure")
                ], missile_ammo_needed=2)
            ], enemy_hp=(16 * 2))
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanEnterReservoirVault(Requirement):
    """
    The player can access the item locations in Sector 4 - Reservoir Vault.

    :param name: Defaults to "Can Enter Reservoir Vault"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Enter Reservoir Vault",
                 *requirements, **kwargs):
        requirements += ([
            HasMorph("Break Bomb Block Chain and Enter Tunnel", [
                # Break Bomb Block Chains
                CanBomb(),
                CanPowerBomb()
            ], [
                # Enter Tunnel
                CanBallJump(),
                #future CanDoAdvancedMidairMorph()
            ])
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanCrossSector4DrainPipeTunnel(Requirement):
    """
    The player can traverse the tunnel in Sector 4 - Drain Pipe.

    :param name: Defaults to "Can Cross Sector 4 Drain Pipe Tunnel"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Cross Sector 4 Drain Pipe Tunnel",
                 *requirements, **kwargs):
        requirements += ([
            HasMorph(None, [
                # Freeze the Powamp
                CanUseDiffusionMissile(),
                HasIceBeam(items_needed={"Wave Beam"})
            ], [
                CanActivatePumpControl(),
                Requirement("Damage Run through Electrified Water",
                            energy_tanks_needed=level_2_e_tanks)
            ])
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanGetToTrainingAerie(Requirement):
    """
    The player can climb Training Grounds in Sector 5 to access Training Aerie.

    :param name: Defaults to "Can Get to Training Aerie"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Get to Training Aerie",
                 *requirements, **kwargs):
        requirements += ([
            HasSpaceJump(),
            CanFreezeEnemies(missile_ammo_needed=2),
            # Video proof: https://youtu.be/Qe9eMPmoUcU?si=1sAjemYzoZWeI1Jg
            CanDoBeginnerShinespark(None, [
                HasKeycard3()
            ], [
                CanDoExpertWallJump()
            ], [
                HasHiJump()
            ])
        ],)
        super().__init__(name, *requirements, **kwargs)


class CanFightNightmare(CanDamageCoreX):
    """
    The player can fight Nightmare and win. Nightmare has 1200 HP.

    :param name: Defaults to "Can Fight Nightmare"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Fight Nightmare",
                 *requirements, **kwargs):
        requirements += ([
            # Nightmare Fight Requirements
            CanFightLateGameBoss("Fight Nightmare", boss_hp=1200),
            CanFightLateGameBossOnAdvanced("Fight Nightmare - Advanced Combat", boss_hp=1200),
            CanFightBossOnExpert("Fight Nightmare - Expert Combat", boss_hp=1200),
        ], [
            # Can leave Nightmare Arena?
            CanSpeedBoosterUnderwater(),
            HasGravity("PONR - Enter Nightmare Arena with Gravity Suit",
                       [PONRRequirement()]),
            HasSpeedBooster("PONR - Enter Nightmare Arena with Speed Booster",
                            [PONRRequirement()]),
            PONRRequirement("PONR - Enter Nightmare Arena")
        ])
        super().__init__(name, *requirements, **kwargs)


class CanFightVariaCoreX(CanDamageCoreX, HasChargeBeam):
    """
    The player can fight the Varia Core X and win. Varia Core X requires Charge Beam to push it into the Core X stage.

    :param name: Defaults to "Can Fight Varia Core X"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed: Defaults to minimum value ``level_2_e_tanks``, or 5
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Fight Varia Core X",
                 *requirements, **kwargs):
        kwargs['energy_tanks_needed'] = max(kwargs.pop('energy_tanks_needed', 0), level_2_e_tanks)
        super().__init__(name, *requirements, **kwargs)


class CanEnterSpaceboostAlley(CanPowerBomb, HasScrewAttack, HasKeycard4, HasSpeedBooster):
    """
    The player can enter Sector 6 - Spaceboost Alley.

    :param name: Defaults to "Can Enter Spaceboost Alley"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed:
    :key power_bomb_ammo_needed:
    """
    def __init__(self,
                 name="Can Enter Spaceboost Alley",
                 *requirements, **kwargs):
        super().__init__(name, *requirements, **kwargs)


class CanDamageGadora(CanDamageToughEnemy):
    """
    The player can defeat a Gadora (Eyedoor) enemy. Gadora have 24 HP. Damage methods are Charge Beam or Missiles.

    :param name: Defaults to "Can Damage Gadora".
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed:
    :key missile_ammo_needed: Auto-calculates minimum missiles based on ``enemy_hp`` and missile upgrades.
        Enabled due to missiles being a Gadora's main weakness.
    :key power_bomb_ammo_needed: Disabled as Gadora are immune to Power Bombs.
    """
    def __init__(self,
                 name="Can Damage Gadora",
                 *requirements, **kwargs):
        kwargs.update({
            'immunities': {"Beam", "Bomb", "Power Bomb", "Screw Attack"},
            'enemy_hp': 24
        })
        super().__init__(name, *requirements, **kwargs)


class CanFightXBOX(CanDamageToughEnemy, CanDamageCoreX):
    """
    The player can fight BOX 2 and win. X-B.O.X. has 500 HP.

    :param name: Defaults to "Can Fight X-B.O.X."
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed: Defaults to minimum value ``level_3_e_tanks``, or 7
    :key missile_ammo_needed: Defaults to enable auto-calculation of missile requirements in
        ``CanDamageToughEnemy``
    :key power_bomb_ammo_needed: Disabled. X-B.O.X. is immune to Power Bombs
    """
    def __init__(self,
                 name = "Can Fight X-B.O.X.",
                 *requirements, **kwargs):
        requirements += ([CanJumpHigh()],[CanPowerBomb()],)
        kwargs.update({
            'energy_tanks_needed': max(kwargs.pop('energy_tanks_needed', 0), level_3_e_tanks),
            'immunities': {"Beam", "Bomb", "Power Bomb", "Screw Attack"},
            'enemy_hp': 500
        })
        super().__init__(name, *requirements, **kwargs)


class CanFightZazabi(CanDamageCoreX):
    """
    The player can fight Zazabi and win. Zazabi has an arbitrary health value equivalent to 2 projectile strikes per
    each of 3 body segments and 4 projectile strikes for the head, totaling to 10 projectile strikes.

    :param name: Defaults to "Can Fight Zazabi"
    :param requirements:
    :key items_needed:
    :key hard_items_needed:
    :key energy_tanks_needed: Defaults to minimum value ``level_1_e_tanks``, or 3
    :key missile_ammo_needed: Defaults to 10
    :key power_bomb_ammo_needed: Disabled. Zazabi is immune to Power Bombs
    """
    def __init__(self,
                 name="Can Fight Zazabi",
                 *requirements, **kwargs):
        requirements += ([
            HasChargeBeam(),
            CanDo10MissileDamage(missile_ammo_needed=10)
        ], [
            CanBomb("Escape the succ"),
            CanDoAdvancedCombat("Don't be succ'd")
        ], [
            PONRRequirement("PONR - Fight Zazabi"),
            CanJumpHigh()
        ],)
        kwargs['energy_tanks_needed'] = max(kwargs.pop('energy_tanks_needed', 0), level_1_e_tanks)
        super().__init__(name, *requirements, **kwargs)