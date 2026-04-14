from typing import TYPE_CHECKING

from worlds.generic.Rules import add_rule
from BaseClasses import Entrance, Region

from .sms_regions.sms_region_helper import (
    SmsLocation,
    SmsRegionName,
    SmsRegion,
    get_correct_requirements,
)
from .sms_regions.delfino_plaza import DELFINO_PLAZA, BOATHOUSE_TRADERS
from .sms_regions.delfino_airstrip import DELFINO_AIRSTRIP
from .sms_regions.corona_mountain import CORONA_MOUNTAIN
from .sms_regions.bianco_hills import (
    BIANCO_HILLS_ENTRANCE,
    BIANCO_HILLS_ONE,
    BIANCO_HILLS_TWO,
    BIANCO_HILLS_THREE,
    BIANCO_HILLS_FOUR,
    BIANCO_HILLS_FIVE,
    BIANCO_HILLS_SIX,
    BIANCO_HILLS_SEVEN,
    BIANCO_HILLS_EIGHT,
)
from .sms_regions.ricco_harbor import (
    RICCO_HARBOR_ENTRANCE,
    RICCO_HARBOR_ONE,
    RICCO_HARBOR_TWO,
    RICCO_HARBOR_THREE,
    RICCO_HARBOR_FOUR,
    RICCO_HARBOR_FIVE,
    RICCO_HARBOR_SIX,
    RICCO_HARBOR_SEVEN,
    RICCO_HARBOR_EIGHT,
)
from .sms_regions.gelato_beach import (
    GELATO_BEACH_ENTRANCE,
    GELATO_BEACH_ONE,
    GELATO_BEACH_TWO,
    GELATO_BEACH_THREE,
    GELATO_BEACH_FOUR,
    GELATO_BEACH_FIVE,
    GELATO_BEACH_SIX,
    GELATO_BEACH_SEVEN,
    GELATO_BEACH_EIGHT,
)
from .sms_regions.pinna_park import (
    PINNA_PARK_ENTRANCE,
    PINNA_PARK_ONE,
    PINNA_PARK_TWO,
    PINNA_PARK_THREE,
    PINNA_PARK_FOUR,
    PINNA_PARK_FIVE,
    PINNA_PARK_SIX,
    PINNA_PARK_SEVEN,
    PINNA_PARK_EIGHT,
)
from .sms_regions.noki_bay import (
    NOKI_BAY_ENTRANCE,
    NOKI_BAY_ONE,
    NOKI_BAY_TWO,
    NOKI_BAY_THREE,
    NOKI_BAY_FOUR,
    NOKI_BAY_FIVE,
    NOKI_BAY_SIX,
    NOKI_BAY_SEVEN,
    NOKI_BAY_EIGHT,
)
from .sms_regions.sirena_beach import (
    SIRENA_BEACH_ENTRANCE,
    SIRENA_BEACH_ONE,
    SIRENA_BEACH_TWO,
    SIRENA_BEACH_THREE,
    SIRENA_BEACH_FOUR,
    SIRENA_BEACH_FIVE,
    SIRENA_BEACH_SIX,
    SIRENA_BEACH_SEVEN,
    SIRENA_BEACH_EIGHT,
)
from .sms_regions.pianta_village import (
    PIANTA_VILLAGE_ENTRANCE,
    PIANTA_VILLAGE_ONE,
    PIANTA_VILLAGE_TWO,
    PIANTA_VILLAGE_THREE,
    PIANTA_VILLAGE_FOUR,
    PIANTA_VILLAGE_FIVE,
    PIANTA_VILLAGE_SIX,
    PIANTA_VILLAGE_SEVEN,
    PIANTA_VILLAGE_EIGHT,
)

if TYPE_CHECKING:
    from . import SmsWorld


def get_location_name_to_id():
    dict_locs: dict[str, int] = {}
    for sms_reg in ALL_REGIONS.values():
        for shine_loc in sms_reg.shines:
            dict_locs.update({f"{sms_reg.name} - {shine_loc.name}": len(dict_locs) + 1})
        for blue_loc in sms_reg.blue_coins:
            dict_locs.update({f"{sms_reg.name} - {blue_loc.name}": len(dict_locs) + 1})
        for nozz_loc in sms_reg.nozzle_boxes:
            dict_locs.update({f"{sms_reg.name} - {nozz_loc.name}": len(dict_locs) + 1})
    return dict_locs


ALL_REGIONS: dict[str, SmsRegion] = {
    "Menu": SmsRegion("Menu"),
    SmsRegionName.AIRSTRIP: DELFINO_AIRSTRIP,
    SmsRegionName.PLAZA: DELFINO_PLAZA,
    SmsRegionName.BOATHOUSE: BOATHOUSE_TRADERS,
    SmsRegionName.BIANCO_ENTRANCE: BIANCO_HILLS_ENTRANCE,
    SmsRegionName.BIANCO_ONE: BIANCO_HILLS_ONE,
    SmsRegionName.BIANCO_TWO: BIANCO_HILLS_TWO,
    SmsRegionName.BIANCO_THREE: BIANCO_HILLS_THREE,
    SmsRegionName.BIANCO_FOUR: BIANCO_HILLS_FOUR,
    SmsRegionName.BIANCO_FIVE: BIANCO_HILLS_FIVE,
    SmsRegionName.BIANCO_SIX: BIANCO_HILLS_SIX,
    SmsRegionName.BIANCO_SEVEN: BIANCO_HILLS_SEVEN,
    SmsRegionName.BIANCO_EIGHT: BIANCO_HILLS_EIGHT,
    SmsRegionName.RICCO_ENTRANCE: RICCO_HARBOR_ENTRANCE,
    SmsRegionName.RICCO_ONE: RICCO_HARBOR_ONE,
    SmsRegionName.RICCO_TWO: RICCO_HARBOR_TWO,
    SmsRegionName.RICCO_THREE: RICCO_HARBOR_THREE,
    SmsRegionName.RICCO_FOUR: RICCO_HARBOR_FOUR,
    SmsRegionName.RICCO_FIVE: RICCO_HARBOR_FIVE,
    SmsRegionName.RICCO_SIX: RICCO_HARBOR_SIX,
    SmsRegionName.RICCO_SEVEN: RICCO_HARBOR_SEVEN,
    SmsRegionName.RICCO_EIGHT: RICCO_HARBOR_EIGHT,
    SmsRegionName.GELATO_ENTRANCE: GELATO_BEACH_ENTRANCE,
    SmsRegionName.GELATO_ONE: GELATO_BEACH_ONE,
    SmsRegionName.GELATO_TWO: GELATO_BEACH_TWO,
    SmsRegionName.GELATO_THREE: GELATO_BEACH_THREE,
    SmsRegionName.GELATO_FOUR: GELATO_BEACH_FOUR,
    SmsRegionName.GELATO_FIVE: GELATO_BEACH_FIVE,
    SmsRegionName.GELATO_SIX: GELATO_BEACH_SIX,
    SmsRegionName.GELATO_SEVEN: GELATO_BEACH_SEVEN,
    SmsRegionName.GELATO_EIGHT: GELATO_BEACH_EIGHT,
    SmsRegionName.PINNA_ENTRANCE: PINNA_PARK_ENTRANCE,
    SmsRegionName.PINNA_ONE: PINNA_PARK_ONE,
    SmsRegionName.PINNA_TWO: PINNA_PARK_TWO,
    SmsRegionName.PINNA_THREE: PINNA_PARK_THREE,
    SmsRegionName.PINNA_FOUR: PINNA_PARK_FOUR,
    SmsRegionName.PINNA_FIVE: PINNA_PARK_FIVE,
    SmsRegionName.PINNA_SIX: PINNA_PARK_SIX,
    SmsRegionName.PINNA_SEVEN: PINNA_PARK_SEVEN,
    SmsRegionName.PINNA_EIGHT: PINNA_PARK_EIGHT,
    SmsRegionName.NOKI_ENTRANCE: NOKI_BAY_ENTRANCE,
    SmsRegionName.NOKI_ONE: NOKI_BAY_ONE,
    SmsRegionName.NOKI_TWO: NOKI_BAY_TWO,
    SmsRegionName.NOKI_THREE: NOKI_BAY_THREE,
    SmsRegionName.NOKI_FOUR: NOKI_BAY_FOUR,
    SmsRegionName.NOKI_FIVE: NOKI_BAY_FIVE,
    SmsRegionName.NOKI_SIX: NOKI_BAY_SIX,
    SmsRegionName.NOKI_SEVEN: NOKI_BAY_SEVEN,
    SmsRegionName.NOKI_EIGHT: NOKI_BAY_EIGHT,
    SmsRegionName.SIRENA_ENTRANCE: SIRENA_BEACH_ENTRANCE,
    SmsRegionName.SIRENA_ONE: SIRENA_BEACH_ONE,
    SmsRegionName.SIRENA_TWO: SIRENA_BEACH_TWO,
    SmsRegionName.SIRENA_THREE: SIRENA_BEACH_THREE,
    SmsRegionName.SIRENA_FOUR: SIRENA_BEACH_FOUR,
    SmsRegionName.SIRENA_FIVE: SIRENA_BEACH_FIVE,
    SmsRegionName.SIRENA_SIX: SIRENA_BEACH_SIX,
    SmsRegionName.SIRENA_SEVEN: SIRENA_BEACH_SEVEN,
    SmsRegionName.SIRENA_EIGHT: SIRENA_BEACH_EIGHT,
    SmsRegionName.PIANTA_ENTRANCE: PIANTA_VILLAGE_ENTRANCE,
    SmsRegionName.PIANTA_ONE: PIANTA_VILLAGE_ONE,
    SmsRegionName.PIANTA_TWO: PIANTA_VILLAGE_TWO,
    SmsRegionName.PIANTA_THREE: PIANTA_VILLAGE_THREE,
    SmsRegionName.PIANTA_FOUR: PIANTA_VILLAGE_FOUR,
    SmsRegionName.PIANTA_FIVE: PIANTA_VILLAGE_FIVE,
    SmsRegionName.PIANTA_SIX: PIANTA_VILLAGE_SIX,
    SmsRegionName.PIANTA_SEVEN: PIANTA_VILLAGE_SEVEN,
    SmsRegionName.PIANTA_EIGHT: PIANTA_VILLAGE_EIGHT,
    SmsRegionName.CORONA: CORONA_MOUNTAIN,
}


def create_region(region: SmsRegion, world: "SmsWorld"):
    curr_region = Region(region.name, world.player, world.multiworld)
    world.multiworld.regions.append(curr_region)

    if region.name == "Menu":
        return curr_region

    # Add Entrance to the parent region and set the requirements to be used later on
    new_entrance: Entrance = world.get_region(region.parent_region).connect(curr_region)
    new_entrance.requirements = get_correct_requirements(region, world.options.difficulty)

    # If the user is fludd-less or access is in ticket mode, change the PLAZA entrance requirements to nothing.
    if region.name == SmsRegionName.PLAZA and (
        world.options.starting_nozzle.value == 2
        or world.options.level_access.value == 1
    ):
        new_entrance.requirements = []

    # Require that the player has the ticket required for the region when ticket mode is enabled
    if world.options.level_access.value == 1 and region.ticketed:
        new_entrance.requirements = []
        curr_region.ticket_str = region.ticketed
        add_rule(
            new_entrance,
            (
                lambda state, ticket_str=region.ticketed: state.has(
                    ticket_str, world.player
                )
            ),
        )

    if (
        world.options.trade_shine_maximum.value == 0
        or world.options.blue_coin_sanity.value == 0
    ) and region.trade:
        return curr_region

    for shine in region.shines:
        # Ignore any 100 Coin shines if not enabled.
        if shine.hundred and not world.options.enable_coin_shines.value == 1:
            continue
        elif region.name == SmsRegionName.AIRSTRIP:
            # If User chose to be fludd-less, don't create the Dilemma shine.
            if (
                world.options.starting_nozzle.value == 2
                and shine.name == "Delfino Airstrip Dilemma"
            ):
                continue
        elif (
            region.trade
            and world.options.blue_coin_sanity.value > 0
            and len([reg_loc for reg_loc in curr_region.get_locations()])
            >= world.options.trade_shine_maximum.value
        ):
            continue

        shine_loc: SmsLocation = SmsLocation(
            world,
            f"{curr_region.name} - {shine.name}",
            region,
            get_correct_requirements(shine, world.options.difficulty),
        )
        if region.trade:
            shine_loc.trades_req = True
        curr_region.locations.append(shine_loc)

    if world.options.blue_coin_sanity.value > 0:
        for blue_coin in region.blue_coins:
            blue_loc: SmsLocation = SmsLocation(
                world,
                f"{curr_region.name} - {blue_coin.name}",
                region,
                get_correct_requirements(blue_coin, world.options.difficulty),
            )
            if world.options.blue_coin_sanity.value != 1:
                curr_region.add_event(
                    blue_loc.name,
                    "Blue Coin",
                    (lambda state, temp_loc=blue_loc: temp_loc.access_rule(state)),
                )
            else:
                blue_loc.blue = True
                curr_region.locations.append(blue_loc)

    if world.options.nozzle_boxes.value:
        for nozzle_box in region.nozzle_boxes:
            nozzle_loc: SmsLocation = SmsLocation(
                world,
                f"{curr_region.name} - {nozzle_box.name}",
                region,
                get_correct_requirements(nozzle_box, world.options.difficulty),
            )
            curr_region.locations.append(nozzle_loc)

    return curr_region


def create_regions(world: "SmsWorld"):
    for region_name, region_data in ALL_REGIONS.items():
        create_region(region_data, world)

    corona_region: Region = world.get_region(SmsRegionName.CORONA)
    corona_region.add_event(
        f"{SmsRegionName.CORONA} - Father and Son Shine!", "Victory"
    )
