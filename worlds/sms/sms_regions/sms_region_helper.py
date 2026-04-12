from enum import StrEnum
from typing import Optional, NamedTuple, TYPE_CHECKING

from BaseClasses import Location
from worlds.sms.options import Difficulty

if TYPE_CHECKING:
    from worlds.sms import SmsWorld


class SmsLocation(Location):
    name: str
    address: Optional[int]
    sms_region: "SmsRegion"
    loc_reqs: list["Requirements"]
    corona: bool

    def __init__(
        self,
        world: "SmsWorld",
        name: str,
        parent_region: "SmsRegion",
        reqs: list["Requirements"],
    ):
        self.address = world.location_name_to_id[name]
        self.loc_reqs = reqs
        self.sms_region = parent_region
        self.corona = False if not reqs else any(loc_req.corona for loc_req in reqs)
        if parent_region.requirements:
            self.corona = self.corona or any(
                reg_loc.corona for reg_loc in parent_region.requirements
            )
        super(SmsLocation, self).__init__(
            world.player,
            name,
            address=self.address,
            parent=world.get_region(parent_region.name),
        )


class SmsRegionName(StrEnum):
    AIRSTRIP = "Delfino Airstrip"
    PLAZA = "Delfino Plaza"
    BOATHOUSE = "Boathouse Traders"
    BIANCO_ENTRANCE = "Bianco Hills"
    BIANCO_ONE = "Bianco Hills 1"
    BIANCO_TWO = "Bianco Hills 2"
    BIANCO_THREE = "Bianco Hills 3"
    BIANCO_FOUR = "Bianco Hills 4"
    BIANCO_FIVE = "Bianco Hills 5"
    BIANCO_SIX = "Bianco Hills 6"
    BIANCO_SEVEN = "Bianco Hills 7"
    BIANCO_EIGHT = "Bianco Hills 8"
    RICCO_ENTRANCE = "Ricco Harbor"
    RICCO_ONE = "Ricco Harbor 1"
    RICCO_TWO = "Ricco Harbor 2"
    RICCO_THREE = "Ricco Harbor 3"
    RICCO_FOUR = "Ricco Harbor 4"
    RICCO_FIVE = "Ricco Harbor 5"
    RICCO_SIX = "Ricco Harbor 6"
    RICCO_SEVEN = "Ricco Harbor 7"
    RICCO_EIGHT = "Ricco Harbor 8"
    GELATO_ENTRANCE = "Gelato Beach"
    GELATO_ONE = "Gelato Beach 1"
    GELATO_TWO = "Gelato Beach 2"
    GELATO_THREE = "Gelato Beach 3"
    GELATO_FOUR = "Gelato Beach 4"
    GELATO_FIVE = "Gelato Beach 5"
    GELATO_SIX = "Gelato Beach 6"
    GELATO_SEVEN = "Gelato Beach 7"
    GELATO_EIGHT = "Gelato Beach 8"
    PINNA_ENTRANCE = "Pinna Park"
    PINNA_ONE = "Pinna Park 1"
    PINNA_TWO = "Pinna Park 2"
    PINNA_THREE = "Pinna Park 3"
    PINNA_FOUR = "Pinna Park 4"
    PINNA_FIVE = "Pinna Park 5"
    PINNA_SIX = "Pinna Park 6"
    PINNA_SEVEN = "Pinna Park 7"
    PINNA_EIGHT = "Pinna Park 8"
    SIRENA = "Sirena Beach"
    NOKI_ENTRANCE = "Noki Bay"
    NOKI_ONE = "Noki Bay 1"
    NOKI_TWO = "Noki Bay 2"
    NOKI_THREE = "Noki Bay 3"
    NOKI_FOUR = "Noki Bay 4"
    NOKI_FIVE = "Noki Bay 5"
    NOKI_SIX = "Noki Bay 6"
    NOKI_SEVEN = "Noki Bay 7"
    NOKI_EIGHT = "Noki Bay 8"
    SIRENA_ENTRANCE = "Sirena Beach"
    SIRENA_ONE = "Sirena Beach 1"
    SIRENA_TWO = "Sirena Beach 2"
    SIRENA_THREE = "Sirena Beach 3"
    SIRENA_FOUR = "Sirena Beach 4"
    SIRENA_FIVE = "Sirena Beach 5"
    SIRENA_SIX = "Sirena Beach 6"
    SIRENA_SEVEN = "Sirena Beach 7"
    SIRENA_EIGHT = "Sirena Beach 8"
    PIANTA_ENTRANCE = "Pianta Village"
    PIANTA_ONE = "Pianta Village 1"
    PIANTA_TWO = "Pianta Village 2"
    PIANTA_THREE = "Pianta Village 3"
    PIANTA_FOUR = "Pianta Village 4"
    PIANTA_FIVE = "Pianta Village 5"
    PIANTA_SIX = "Pianta Village 6"
    PIANTA_SEVEN = "Pianta Village 7"
    PIANTA_EIGHT = "Pianta Village 8"
    CORONA = "Corona Mountain"


class NozzleType(StrEnum):
    spray = "Spray Nozzle"
    hover = "Hover Nozzle"
    rocket = "Rocket Nozzle"
    turbo = "Turbo Nozzle"
    yoshi = "Yoshi"


class Requirements(NamedTuple):
    nozzles: Optional[list[list[str]]] = None  # conjunctive normal form
    shines: Optional[int] = None  # number of shine sprites needed
    blue_coins: Optional[int] = None
    location: Optional[str] = None
    corona: bool = False  # is corona access needed (configurable)
    skip_forward: bool = None  # Only in logic if tickets / fluddless are true
    manual_none: bool = (
        False  # Only matters for higher difficulties. Prevents fallback requirements.
    )

    def is_empty(self):
        return (
            True
            if (
                not self.nozzles
                and not self.shines
                and not self.blue_coins
                and not self.location
                and not self.corona
                and not self.skip_forward
                and not self.manual_none
            )
            else False
        )


class Shine(NamedTuple):
    name: str
    requirements: Optional[list[Requirements]] | None = None
    hard: Optional[list[Requirements]] | None = None
    advanced: Optional[list[Requirements]] | None = None
    tears: Optional[list[Requirements]] | None = None
    hundred: bool = False  # 100 coin Shines
    in_game_bit: int = None


class BlueCoin(NamedTuple):
    name: str
    requirements: Optional[list[Requirements]] | None = None
    hard: Optional[list[Requirements]] | None = None
    advanced: Optional[list[Requirements]] | None = None
    tears: Optional[list[Requirements]] | None = None
    in_game_bit: int = None


class OneUp(NamedTuple):
    name: str
    requirements: Requirements = Requirements()


# Yes, I'm going to include Shadow Mario Plaza chases as NozzleBox Locations
class NozzleBox(NamedTuple):
    name: str
    requirements: Optional[list[Requirements]] | None = None
    hard: Optional[list[Requirements]] | None = None
    advanced: Optional[list[Requirements]] | None = None
    tears: Optional[list[Requirements]] | None = None
    in_game_bit: int = None


class SmsRegion(NamedTuple):
    name: str
    requirements: Optional[list[Requirements]] | None = None
    shines: Optional[list[Shine]] | None = []
    blue_coins: Optional[list[BlueCoin]] | None = []
    nozzle_boxes: Optional[list[NozzleBox]] | None = []
    ticketed: str = ""
    trade: bool = False
    parent_region: str = None


def get_correct_requirements(
    item: Shine | BlueCoin | NozzleBox, difficulty: Difficulty
):
    match difficulty.value:
        case 0:
            return item.requirements
        case 1:
            return (
                item.hard
                if (item.hard != None and item.hard.count != 0)
                else item.requirements
            )
        case 2:
            return (
                item.advanced
                if (item.advanced != None and item.advanced.count != 0)
                else (
                    item.hard
                    if (item.hard != None and item.hard.count != 0)
                    else item.requirements
                )
            )
        case 3:
            return (
                item.tears
                if (item.tears != None and item.tears.count != 0)
                else (
                    item.advanced
                    if (item.advanced != None and item.advanced.count != 0)
                    else (
                        item.hard
                        if (item.hard != None and item.hard.count != 0)
                        else item.requirements
                    )
                )
            )
        case _:
            return item.requirements


# Common combinations of Nozzle Types
ANY_SPLASHER: list[list[str]] = [
    [NozzleType.spray],
    [NozzleType.hover],
    [NozzleType.yoshi],
]
SPROVER_OR_YOSHI: list[list[str]] = [
    [NozzleType.spray, NozzleType.hover],
    [NozzleType.yoshi],
]
SPROVER_OR_SPROCKET_OR_YOSHI: list[list[str]] = [
    [NozzleType.spray, NozzleType.hover],
    [NozzleType.spray, NozzleType.rocket],
    [NozzleType.yoshi],
]
SPROCKET_OR_HOVER: list[list[str]] = [
    [NozzleType.spray, NozzleType.rocket],
    [NozzleType.hover],
]
SPROCKET_OR_HOVER_OR_TURBO: list[list[str]] = [
    [NozzleType.spray, NozzleType.rocket],
    [NozzleType.hover],
    [NozzleType.turbo],
]
HOVER_OR_YOSHI: list[list[str]] = [[NozzleType.hover], [NozzleType.yoshi]]
ROCKET_OR_HOVER_OR_YOSHI: list[list[str]] = [
    [NozzleType.hover],
    [NozzleType.rocket],
    [NozzleType.yoshi],
]
ROCKET_AND_SPLASHER: list[list[str]] = [
    [NozzleType.rocket, NozzleType.spray],
    [NozzleType.rocket, NozzleType.hover],
    [NozzleType.rocket, NozzleType.yoshi],
]
ALL_SPLASHER: list[list[str]] = [[NozzleType.spray, NozzleType.hover, NozzleType.yoshi]]
ROCKET_AND_SPRAY_AND_HOVER: list[list[str]] = [
    [NozzleType.rocket, NozzleType.spray, NozzleType.hover]
]
SPROCKET_OR_SPROVER: list[list[str]] = [
    [NozzleType.rocket, NozzleType.spray],
    [NozzleType.hover, NozzleType.spray],
]
SPROVER_OR_ROCKET: list[list[str]] = [
    [NozzleType.rocket],
    [NozzleType.hover, NozzleType.spray],
]
ROCKET_AND_SPRAY_OR_ROCKET_AND_HOVER: list[list[str]] = [
    [NozzleType.rocket, NozzleType.spray],
    [NozzleType.rocket, NozzleType.hover],
]
ROCKET_AND_SPRAY_OR_ROCKET_AND_HOVER_OR_YOSHI: list[list[str]] = [
    [NozzleType.rocket, NozzleType.spray],
    [NozzleType.rocket, NozzleType.hover],
    [NozzleType.yoshi],
]
ROCKET_AND_SPRAY_OR_ROCKET_AND_HOVER_OR_YOSHI_OR_TURBO: list[list[str]] = [
    [NozzleType.rocket, NozzleType.spray],
    [NozzleType.rocket, NozzleType.hover],
    [NozzleType.yoshi],
    [NozzleType.turbo],
]
SPRAY_AND_TURBO_OR_HOVER_AND_TURBO: list[list[str]] = [
    [NozzleType.spray, NozzleType.turbo],
    [NozzleType.hover, NozzleType.turbo],
]
ROCKET_AND_YOSHI: list[list[str]] = [[NozzleType.rocket, NozzleType.yoshi]]
ROCKET_OR_HOVER: list[list[str]] = [[NozzleType.hover], [NozzleType.rocket]]
ROCKET_OR_TURBO: list[list[str]] = [[NozzleType.turbo], [NozzleType.rocket]]
ROCKET_AND_SPRAY: list[list[str]] = [[NozzleType.spray, NozzleType.rocket]]
SPRAY_OR_YOSHI: list[list[str]] = [[NozzleType.spray], [NozzleType.yoshi]]
TURSPRAY: list[list[str]] = [[NozzleType.spray, NozzleType.turbo]]
YOSHI_AND_HOVER: list[list[str]] = [[NozzleType.yoshi, NozzleType.hover]]
SPRAY_AND_HOVER: list[list[str]] = [[NozzleType.spray, NozzleType.hover]]
SPRAY_OR_HOVER: list[list[str]] = [[NozzleType.spray], [NozzleType.hover]]
SPROCKET_OR_HOVER_OR_YOSHI: list[list[str]] = [
    [NozzleType.spray, NozzleType.rocket],
    [NozzleType.hover],
    [NozzleType.yoshi],
]
SPROCKET_OR_HOVER_OR_TURBO_OR_YOSHI: list[list[str]] = [
    [NozzleType.spray, NozzleType.rocket],
    [NozzleType.hover],
    [NozzleType.turbo],
    [NozzleType.yoshi],
]
TURBO_OR_HOVER: list[list[str]] = [[NozzleType.hover], [NozzleType.turbo]]
TURBO_OR_SPLASHER: list[list[str]] = [
    [NozzleType.spray, NozzleType.hover, NozzleType.yoshi],
    [NozzleType.turbo],
]
ROCKET_OR_SPLASHER: list[list[str]] = [
    [NozzleType.spray, NozzleType.hover, NozzleType.yoshi],
    [NozzleType.rocket],
]
YOSHI_AND_SPRAY_OR_YOSHI_AND_HOVER: list[list[str]] = [
    [NozzleType.yoshi, NozzleType.spray],
    [NozzleType.yoshi, NozzleType.hover],
]
SPRAY_OR_HOVER_OR_TURBO: list[list[str]] = [
    [NozzleType.spray],
    [NozzleType.hover],
    [NozzleType.turbo],
]
SPRAY_OR_HOVER_OR_ROCKET: list[list[str]] = [
    [NozzleType.spray],
    [NozzleType.hover],
    [NozzleType.rocket],
]
ANY_FLUDD: list[list[str]] = [
    [NozzleType.spray],
    [NozzleType.hover],
    [NozzleType.rocket],
    [NozzleType.turbo],
]
ROCKET_OR_HOVER_OR_TURBO: list[list[str]] = [
    [NozzleType.rocket],
    [NozzleType.hover],
    [NozzleType.turbo],
]
YOSHI_OR_ROCKET: list[list[str]] = [[NozzleType.rocket], [NozzleType.yoshi]]
ALL_SPLASHERS: list[list[str]] = [
    [NozzleType.spray, NozzleType.hover, NozzleType.yoshi]
]
HOVER_AND_YOSHI: list[list[str]] = [[NozzleType.hover, NozzleType.yoshi]]
SPRAY_AND_YOSHI: list[list[str]] = [[NozzleType.spray, NozzleType.yoshi]]
SPROVER_OR_SPROCKET: list[list[str]] = [
    [NozzleType.spray, NozzleType.hover],
    [NozzleType.spray, NozzleType.rocket],
]
SPRAY_AND_ANY_FLUDD: list[list[str]] = [
    [NozzleType.spray, NozzleType.hover],
    [NozzleType.spray, NozzleType.rocket],
    [NozzleType.spray, NozzleType.turbo],
]
SPRAY_AND_ANY_NOZZLE: list[list[str]] = [
    [NozzleType.spray, NozzleType.hover],
    [NozzleType.spray, NozzleType.rocket],
    [NozzleType.spray, NozzleType.turbo],
    [NozzleType.spray, NozzleType.yoshi],
]
ROCKET_AND_ANY_NOZZLE: list[list[str]] = [
    [NozzleType.rocket, NozzleType.hover],
    [NozzleType.rocket, NozzleType.spray],
    [NozzleType.rocket, NozzleType.turbo],
    [NozzleType.rocket, NozzleType.yoshi],
]
ROCKET_AND_ANY_FLUDD: list[list[str]] = [
    [NozzleType.rocket, NozzleType.hover],
    [NozzleType.rocket, NozzleType.spray],
    [NozzleType.rocket, NozzleType.turbo],
]
ROCKET_AND_SPRAY_OR_ROCKET_AND_HOVER_OR_ROCKET_AND_YOSHI: list[list[str]] = [
    [NozzleType.rocket, NozzleType.hover],
    [NozzleType.rocket, NozzleType.spray],
    [NozzleType.rocket, NozzleType.yoshi],
]
TURBO_AND_SPRAY_OR_TURBO_AND_HOVER: list[list[str]] = [
    [NozzleType.turbo, NozzleType.spray],
    [NozzleType.turbo, NozzleType.hover],
]
ANY_SPLASHER_OR_TURBO: list[list[str]] = [
    [NozzleType.spray],
    [NozzleType.hover],
    [NozzleType.turbo],
    [NozzleType.yoshi],
]
SPRAY_OR_HOVER_OR_ROCKET_OR_YOSHI: list[list[str]] = [
    [NozzleType.spray],
    [NozzleType.hover],
    [NozzleType.rocket],
    [NozzleType.yoshi],
]
ROCKET_OR_HOVER_OR_TURBO_OR_YOSHI: list[list[str]] = [
    [NozzleType.rocket],
    [NozzleType.hover],
    [NozzleType.turbo],
    [NozzleType.yoshi],
]
ANY_NOZZLE: list[list[str]] = [
    [NozzleType.spray],
    [NozzleType.hover],
    [NozzleType.rocket],
    [NozzleType.turbo],
    [NozzleType.yoshi],
]
SPRAY_AND_OTHER_FLUDD: list[list[str]] = [
    [NozzleType.spray, NozzleType.hover],
    [NozzleType.spray, NozzleType.rocket],
    [NozzleType.spray, NozzleType.turbo],
]
SPRAY_AND_TURBO: list[list[str]] = [
    [NozzleType.spray, NozzleType.turbo],
]
