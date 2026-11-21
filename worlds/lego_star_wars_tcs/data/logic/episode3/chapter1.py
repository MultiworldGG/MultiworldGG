from ..rules import HasAbility, True_
from ..types import minikit_data, ExitData, Chapter, LocationData
from ..option_filters import logic_options

from ...areas import Area

from ....character_ability import IS_A_VEHICLE, VEHICLE_BLASTER, FITS_EASILY_THROUGH_VENATOR

NAME = "Battle Over Coruscant"

R_SPACE_BATTLE_SPAWN = "Space Battle Spawn"
R_AFTER_FIRST_DESTROYABLE_SHIP = "After First Destroyable Ship"
R_AFTER_SECOND_DESTROYABLE_SHIP = "After Second Destroyable Ship"

BATTLE_OVER_CORUSCANT = Chapter(
    area=Area.DOGFIGHT,
    start_region=R_SPACE_BATTLE_SPAWN,
    extra_entrance_rules=logic_options(
        # In base logic, expect a blaster vehicle to fight back at the start.
        base=HasAbility(VEHICLE_BLASTER),
        # The first 2 minikits can be collected by ramming into them.
        normal=HasAbility(IS_A_VEHICLE),
    ),
    regions={
        R_SPACE_BATTLE_SPAWN: (
            ExitData(R_AFTER_FIRST_DESTROYABLE_SHIP, HasAbility(VEHICLE_BLASTER)),
        ),
        R_AFTER_FIRST_DESTROYABLE_SHIP: (
            ExitData(
                R_AFTER_SECOND_DESTROYABLE_SHIP,
                logic_options(
                    # Slave 1 just barely fits through the ship later in the level. Imperial Shuttle is also a little
                    # easy to accidentally crash in the same place. To reduce confusion with newer players, and to
                    # potentially help with achieving True Jedi, any vehicle with max height no more than 2.5 is
                    # expected for the base logic.
                    # This excludes:
                    # - Slave 1 (3.2 height)
                    # - Imperial Shuttle (2.55 height)
                    # TIE Fighter (and variations) and Millennium Falcon are the next tallest, at 2.0.
                    base=HasAbility(FITS_EASILY_THROUGH_VENATOR),
                    normal=True_(),
                ),
            ),
        ),
        R_AFTER_SECOND_DESTROYABLE_SHIP: (
            ExitData("Chapter Completion"),
        ),
    },
    minikits={
        "Minikit 1": minikit_data(
            R_SPACE_BATTLE_SPAWN,
            pickup_name="m_pup1"
        ),
        "Minikit 2": minikit_data(
            R_SPACE_BATTLE_SPAWN,
            pickup_name="m_pup2"
        ),
        "Minikit 3": minikit_data(
            R_AFTER_FIRST_DESTROYABLE_SHIP,
            pickup_name="m_pup3"
        ),
        "Minikit 4": minikit_data(
            R_AFTER_FIRST_DESTROYABLE_SHIP,
            pickup_name="m_pup4"
        ),
        "Minikit 5": minikit_data(
            R_AFTER_FIRST_DESTROYABLE_SHIP,
            pickup_name="m_pup5"
        ),
        "Minikit 6": minikit_data(
            R_AFTER_FIRST_DESTROYABLE_SHIP,
            pickup_name="m_pup6"
        ),
        "Minikit 7": minikit_data(
            R_AFTER_FIRST_DESTROYABLE_SHIP,
            pickup_name="m_pup7"
        ),
        "Minikit 8": minikit_data(
            R_AFTER_SECOND_DESTROYABLE_SHIP,
            pickup_name="m_pup8"
        ),
        "Minikit 9": minikit_data(
            R_AFTER_SECOND_DESTROYABLE_SHIP,
            pickup_name="m_pup9"
        ),
        "Minikit 10": minikit_data(
            R_AFTER_SECOND_DESTROYABLE_SHIP,
            pickup_name="m_pup10"
        ),
    },
    power_brick=LocationData(R_AFTER_SECOND_DESTROYABLE_SHIP)
)
