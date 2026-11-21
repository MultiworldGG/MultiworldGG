from rule_builder.rules import And

from ..macros import CAN_SITH_FORCE, CAN_DESTROY_CLOSE_SILVER_BRICKS, CAN_DAMAGE_AT_CLOSE_RANGE
from ..rules import HasAllAbilities, HasAbility
from ..types import GoldBrickBonus, ExitData, LocationData
from ...areas import Area
from ...characters import Character
from ....character_ability import *

NEW_TOWN = GoldBrickBonus(
    area=Area.BONUS,
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
                        | CAN_PUSH_OBJECTS
                        | CAN_RIDE_VEHICLES
                    ),
                    CAN_SITH_FORCE,
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                ),
            ),
        )
    },
    ridables={
        Character.SPEEDER_LAND: LocationData("Spawn"),
        Character.DEWBACK: LocationData("Spawn"),
        # The car is hidden within Silver Bricks and then must be built.
        Character.MOONCAR: LocationData(
            "Spawn",
            CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(CAN_BUILD_BRICKS)
        ),
        # Fix the lifeboat, then push it into the water.
        Character.LIFEBOAT: LocationData(
            "Spawn",
            HasAllAbilities(CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS)
        ),
        Character.FIRETRUCK: LocationData("Spawn"),
        Character.BASKETCANNON: LocationData("Spawn"),
        Character.CLONEWALKER: LocationData("Spawn"),
        Character.CLOUDCAR: LocationData("Spawn"),
        # There is a Tauntaun just barely close enough to the fence that there is no need for a character that can jump
        # or destroy the fences, though all characters that can ride vehicles can also jump.
        Character.TAUNTAUN: LocationData("Spawn"),
        # The house and bins need destroying, and then the car needs to be built.
        Character.TOWNCAR: LocationData(
            "Spawn",
            CAN_DAMAGE_AT_CLOSE_RANGE & HasAbility(CAN_BUILD_BRICKS)
        ),
        # A small building needs to be destroyed, and then the tractor needs to be built.
        Character.TRACTOR: LocationData(
            "Spawn",
            CAN_DAMAGE_AT_CLOSE_RANGE & HasAbility(CharacterAbility.CAN_BUILD_BRICKS)
        ),
        Character.BANTHA: LocationData("Spawn"),
    },
    gold_brick_requirement=50,
)
