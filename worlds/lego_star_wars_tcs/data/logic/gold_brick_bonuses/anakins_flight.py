from rule_builder.rules import True_

from ..types import GoldBrickBonus, ExitData
from ..option_filters import logic_options
from ..rules import HasAbility
from ...areas import Area
from ...extras import Extra
from ...levels import Level
from ....character_ability import *

ANAKINS_FLIGHT = GoldBrickBonus(
    area=Area.ANAKINSFLIGHT,
    start_region="Control Ship Exterior",
    extra_entrance_rules=logic_options(
        base=HasAbility(VEHICLE_BLASTER),
        normal=HasAbility(IS_A_VEHICLE),
    ),
    regions={
        "Control Ship Exterior": (
            ExitData("Control Ship First Hangar", new_level=Level.ANAKINSFLIGHT_B),
        ),
        "Control Ship First Hangar": (
            ExitData(
                "Control Ship Second Hangar",
                logic_options(
                    base=True_(),
                    normal=HasAbility(VEHICLE_BLASTER),
                    # The red targets can be shot with torpedoes, though it is finicky.
                    moderate=HasAbility(VEHICLE_BLASTER) | Extra.INFINITE_TORPEDOS.has(),
                    # I could not get bolts deflected with Deflect Bolts to destroy the red targets, even with Exploding
                    # Blaster Bolts active.
                    # You can bring 3 Torpedoes from the ship exterior with you. Only 2 are needed to open the door to
                    # the second hangar. The red target is difficult to hit with torpedoes, so this is not expected on
                    # Hard logic.
                    # expert=True_(),
                ),
            ),
        ),
        "Control Ship Second Hangar": (
            # You can actually destroy tanks with Deflect Bolts to get torpedoes, enough to make it to the core, though
            # maybe this is too annoying even for Expert logic.
            ExitData("Control Ship Core", new_level=Level.ANAKINSFLIGHT_C),
        ),
        "Control Ship Core": (
            ExitData(GoldBrickBonus.COMPLETION_REGION_NAME),
        ),
    },
    gold_brick_requirement=30
)
