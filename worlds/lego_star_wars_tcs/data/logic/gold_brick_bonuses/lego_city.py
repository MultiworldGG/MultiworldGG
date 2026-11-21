from rule_builder.rules import And

from ..macros import CAN_DESTROY_CLOSE_SILVER_BRICKS, CAN_DAMAGE_AT_CLOSE_RANGE
from ..rules import HasAllAbilities, HasAbility
from ..types import GoldBrickBonus, ExitData, LocationData
from ...areas import Area
from ...characters import Character
from ....character_ability import *

LEGO_CITY = GoldBrickBonus(
    area=Area.BONUS2,
    start_region="Spawn",
    regions={
        "Spawn": (
            ExitData(
                GoldBrickBonus.COMPLETION_REGION_NAME,
                And(
                    HasAllAbilities(
                        JEDI
                        | BLASTER
                        | CAN_BUILD_BRICKS
                        | CAN_PULL_LEVERS
                        | CAN_MELEE
                        | CAN_RIDE_VEHICLES
                    ),
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                ),
            ),
        )
    },
    ridables={
        # There are Banthas and Dewbacks close enough to the fences that there is no requirement to destroy or jump over
        # the fences.
        Character.BANTHA: LocationData("Spawn"),
        Character.DEWBACK: LocationData("Spawn"),
        Character.CLOUDCAR: LocationData("Spawn"),
        Character.TAUNTAUN: LocationData("Spawn"),
        Character.TOWNCAR: LocationData("Spawn"),
        # Either The AT-ST or a Bounty Hunter can destroy the obstacles in the way of getting to the Landspeeder.
        Character.SPEEDER_LAND: LocationData(
            "Spawn",
            HasAbility(JEDI) | CAN_DESTROY_CLOSE_SILVER_BRICKS
        ),
        # To access the first part, levers need to be pulled, then force is needed to move a part into place, and build
        # bricks is needed to build the final part.
        Character.WOOKIEFLYER: LocationData(
            "Spawn",
            HasAllAbilities(JEDI | CAN_BUILD_BRICKS | CAN_PULL_LEVERS)
        ),
        # The car is hidden within Silver Bricks, and then needs to be built.
        Character.MOONCAR: LocationData(
            "Spawn",
            CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(CAN_BUILD_BRICKS)
        ),
        # A house needs to be destroyed to reveal the parts and then the Tractor needs to be built.
        Character.TRACTOR: LocationData(
            "Spawn",
            CAN_DAMAGE_AT_CLOSE_RANGE & HasAbility(CAN_BUILD_BRICKS)
        ),
        # A house needs to be destroyed to reveal the parts and then a Jedi is needed to assemble the AT-ST.
        Character.ATST: LocationData(
            "Spawn",
            HasAbility(JEDI) & CAN_DAMAGE_AT_CLOSE_RANGE
        ),
    },
    gold_brick_requirement=10,
)
