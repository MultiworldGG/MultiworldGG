from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, And

from ..constants import Rac5Gadgets, Rac5Infobots
from ._helpers import HasClankPack, HasProjectileWeapon

if TYPE_CHECKING:
    from ..world import RACSizeMatterWorld


def set_entrance_rules(world: "RACSizeMatterWorld") -> None:
    player = world.player
    mw = world.multiworld
    world.set_rule(mw.get_entrance("To Pokitaru", player), Has(Rac5Infobots.POKITARU))
    world.set_rule(mw.get_entrance("To Ryllus", player), Has(Rac5Infobots.RYLLUS))
    world.set_rule(mw.get_entrance("To Kalidon", player), Has(Rac5Infobots.KALIDON))
    world.set_rule(mw.get_entrance("To Metalis", player), Has(Rac5Infobots.METALIS))
    world.set_rule(
        mw.get_entrance("To Dreamtime", player),
        Has(Rac5Infobots.OUTPOST_OMEGA),
    )
    world.set_rule(mw.get_entrance("To Outpost Omega", player), Has(Rac5Infobots.OUTPOST_OMEGA))
    world.set_rule(mw.get_entrance("To Challax", player), HasAll(Rac5Infobots.CHALLAX))
    world.set_rule(mw.get_entrance("To Dayni Moon", player), Has(Rac5Infobots.DAYNI_MOON))
    world.set_rule(
        mw.get_entrance("To Inside Clank", player),
        And(HasAll(Rac5Infobots.DAYNI_MOON, Rac5Gadgets.SPROUT_O_MATIC),
            HasProjectileWeapon(),
            HasClankPack(world),
        )
    )
    world.set_rule(mw.get_entrance("To Quodrona", player), Has(Rac5Infobots.QUODRONA))
