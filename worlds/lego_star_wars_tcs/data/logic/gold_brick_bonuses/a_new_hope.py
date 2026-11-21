from rule_builder.rules import True_

from ..types import GoldBrickBonus, ExitData
from ..option_filters import logic_options
from ...areas import Area
from ...levels import Level
from ..macros import CAN_DAMAGE_AT_CLOSE_RANGE
from ..rules import HasAbility
from ....character_ability import *

A_NEW_HOPE = GoldBrickBonus(
    area=Area.ANEWHOPE,
    start_region="Spawn",
    regions={
        "Spawn": (
            ExitData(
                "Crossroads After First Corridor",
                logic_options(
                    base=CAN_DAMAGE_AT_CLOSE_RANGE,
                    # Ignore the enemies.
                    normal=True_(),
                ),
            ),
        ),
        "Crossroads After First Corridor": (
            ExitData(
                "Free C-3PO Room",
                new_level=Level.ANEWHOPE_B,
            ),
            ExitData(
                "Force LEGO Logo Room",
                new_level=Level.ANEWHOPE_B,
            ),
            ExitData(
                "T-Junction After Second Corridor",
                # You cannot Yoda Clip over this door, its collision extends too high and invisible walls surround
                # everything else.
                HasAbility(PROTOCOL_PANEL),
            ),
        ),
        "Free C-3PO Room": (),
        "Force LEGO Logo Room": (),
        "T-Junction After Second Corridor": (
            ExitData(
                "Fan Room",
                new_level=Level.ANEWHOPE_B,
            ),
            ExitData(
                GoldBrickBonus.COMPLETION_REGION_NAME,
                # Destroyable objects block access to the panel.
                # This door also has collision too high to Yoda Clip over.
                HasAbility(PROTOCOL_PANEL) & CAN_DAMAGE_AT_CLOSE_RANGE,
            ),
        ),
        "Fan Room": (),
    },
    gold_brick_requirement=20,
)
