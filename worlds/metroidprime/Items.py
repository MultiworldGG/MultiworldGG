from typing import Dict, List, TYPE_CHECKING, Optional, Union
from BaseClasses import Item, ItemClassification

from .Enum import ProgressiveUpgrade, SuitUpgrade

if TYPE_CHECKING:
    from . import MetroidPrimeWorld

AP_METROID_PRIME_ITEM_ID_BASE = 5031000


class ItemData:
    name: str
    code: int
    classification: ItemClassification
    max_capacity: int
    id: int

    def __init__(
        self, name: str, id_: int, progression: ItemClassification, max_capacity: int = 1
    ) -> None:
        self.name = name
        self.id = id_
        self.code = id_ + AP_METROID_PRIME_ITEM_ID_BASE
        self.classification = progression
        self.max_capacity = max_capacity


class MetroidPrimeItem(Item):
    game: str = "Metroid Prime"


PROGRESSIVE_ITEM_MAPPING: Dict[ProgressiveUpgrade, List[SuitUpgrade]] = {
    ProgressiveUpgrade.Progressive_Power_Beam: [
        SuitUpgrade.Power_Beam,
        SuitUpgrade.Power_Charge_Beam,
        SuitUpgrade.Super_Missile,
    ],
    ProgressiveUpgrade.Progressive_Ice_Beam: [
        SuitUpgrade.Ice_Beam,
        SuitUpgrade.Ice_Charge_Beam,
        SuitUpgrade.Ice_Spreader,
    ],
    ProgressiveUpgrade.Progressive_Wave_Beam: [
        SuitUpgrade.Wave_Beam,
        SuitUpgrade.Wave_Charge_Beam,
        SuitUpgrade.Wavebuster,
    ],
    ProgressiveUpgrade.Progressive_Plasma_Beam: [
        SuitUpgrade.Plasma_Beam,
        SuitUpgrade.Plasma_Charge_Beam,
        SuitUpgrade.Flamethrower,
    ],
    ProgressiveUpgrade.Progressive_Bomb: [
        SuitUpgrade.Spring_Ball,
        SuitUpgrade.Morph_Ball_Bomb,
    ]
}

PROGRESSIVE_BEAM_ITEM_EXCLUSION_LIST: List[SuitUpgrade] = [
    SuitUpgrade.Power_Beam,
    SuitUpgrade.Ice_Beam,
    SuitUpgrade.Wave_Beam,
    SuitUpgrade.Plasma_Beam,
    SuitUpgrade.Super_Missile,
    SuitUpgrade.Ice_Spreader,
    SuitUpgrade.Wavebuster,
    SuitUpgrade.Flamethrower,
    SuitUpgrade.Charge_Beam,
]

PROGRESSIVE_BOMB_ITEM_EXCLUSION_LIST: List[SuitUpgrade] = [
    SuitUpgrade.Spring_Ball,
    SuitUpgrade.Morph_Ball_Bomb,
]


def get_vanilla_item_for_progressive_upgrade(
    upgrade: ProgressiveUpgrade, count: int
) -> Optional[SuitUpgrade]:
    max_count = 3
    if count > max_count:
        count = max_count

    index = count - 1  # 0-indexed
    if upgrade in PROGRESSIVE_ITEM_MAPPING:
        return PROGRESSIVE_ITEM_MAPPING[upgrade][index]
    return None


def get_progressive_upgrade_for_item(item: SuitUpgrade) -> Optional[ProgressiveUpgrade]:
    if item == SuitUpgrade.Charge_Beam:
        return (
            ProgressiveUpgrade.Progressive_Power_Beam
        )  # Using this just so consumers know there is a progressive upgrade associated with this
    for upgrade, items in PROGRESSIVE_ITEM_MAPPING.items():
        if item in items:
            return upgrade
    return None


def __get_missile_item(world: "MetroidPrimeWorld") -> SuitUpgrade:
    if world.options.missile_launcher:
        return SuitUpgrade.Missile_Launcher
    return SuitUpgrade.Missile_Expansion


def __get_power_bomb_item(world: "MetroidPrimeWorld") -> SuitUpgrade:
    if world.options.main_power_bomb:
        return SuitUpgrade.Main_Power_Bomb
    return SuitUpgrade.Power_Bomb_Expansion


def get_item_for_options(
    world: "MetroidPrimeWorld", item: SuitUpgrade
) -> Union[SuitUpgrade, ProgressiveUpgrade]:
    if item == SuitUpgrade.Missile_Launcher:
        return __get_missile_item(world)
    if item == SuitUpgrade.Main_Power_Bomb:
        return __get_power_bomb_item(world)
    if world.options.progressive_beam_upgrades or world.options.spring_ball.current_option_name.lower() == "its own progressive item":
        progressive_upgrade = get_progressive_upgrade_for_item(item)
        if progressive_upgrade is not None:
            return progressive_upgrade
    return item


suit_upgrade_table: Dict[str, ItemData] = {
    SuitUpgrade.Power_Beam.value: ItemData(
        SuitUpgrade.Power_Beam.value, 0, ItemClassification.progression
    ),
    SuitUpgrade.Ice_Beam.value: ItemData(
        SuitUpgrade.Ice_Beam.value, 1, ItemClassification.progression
    ),
    SuitUpgrade.Wave_Beam.value: ItemData(
        SuitUpgrade.Wave_Beam.value, 2, ItemClassification.progression
    ),
    SuitUpgrade.Plasma_Beam.value: ItemData(
        SuitUpgrade.Plasma_Beam.value, 3, ItemClassification.progression
    ),
    SuitUpgrade.Missile_Expansion.value: ItemData(
        SuitUpgrade.Missile_Expansion.value, 4, ItemClassification.filler, 999
    ),
    SuitUpgrade.Scan_Visor.value: ItemData(
        SuitUpgrade.Scan_Visor.value, 5, ItemClassification.progression
    ),
    SuitUpgrade.Morph_Ball_Bomb.value: ItemData(
        SuitUpgrade.Morph_Ball_Bomb.value, 6, ItemClassification.progression
    ),
    SuitUpgrade.Power_Bomb_Expansion.value: ItemData(
        SuitUpgrade.Power_Bomb_Expansion.value, 7, ItemClassification.useful, 99
    ),
    SuitUpgrade.Flamethrower.value: ItemData(
        SuitUpgrade.Flamethrower.value, 8, ItemClassification.useful
    ),
    SuitUpgrade.Thermal_Visor.value: ItemData(
        SuitUpgrade.Thermal_Visor.value, 9, ItemClassification.progression
    ),
    SuitUpgrade.Charge_Beam.value: ItemData(
        SuitUpgrade.Charge_Beam.value, 10, ItemClassification.progression
    ),
    SuitUpgrade.Super_Missile.value: ItemData(
        SuitUpgrade.Super_Missile.value, 11, ItemClassification.progression
    ),
    SuitUpgrade.Grapple_Beam.value: ItemData(
        SuitUpgrade.Grapple_Beam.value, 12, ItemClassification.progression
    ),
    SuitUpgrade.X_Ray_Visor.value: ItemData(
        SuitUpgrade.X_Ray_Visor.value, 13, ItemClassification.progression
    ),
    SuitUpgrade.Ice_Spreader.value: ItemData(
        SuitUpgrade.Ice_Spreader.value, 14, ItemClassification.useful
    ),
    SuitUpgrade.Space_Jump_Boots.value: ItemData(
        SuitUpgrade.Space_Jump_Boots.value, 15, ItemClassification.progression
    ),
    SuitUpgrade.Morph_Ball.value: ItemData(
        SuitUpgrade.Morph_Ball.value, 16, ItemClassification.progression
    ),
    SuitUpgrade.Combat_Visor.value: ItemData(
        SuitUpgrade.Combat_Visor.value, 17, ItemClassification.progression
    ),
    SuitUpgrade.Boost_Ball.value: ItemData(
        SuitUpgrade.Boost_Ball.value, 18, ItemClassification.progression
    ),
    SuitUpgrade.Spider_Ball.value: ItemData(
        SuitUpgrade.Spider_Ball.value, 19, ItemClassification.progression
    ),
    SuitUpgrade.Power_Suit.value: ItemData(
        SuitUpgrade.Power_Suit.value, 20, ItemClassification.progression
    ),
    SuitUpgrade.Gravity_Suit.value: ItemData(
        SuitUpgrade.Gravity_Suit.value, 21, ItemClassification.progression
    ),
    SuitUpgrade.Varia_Suit.value: ItemData(
        SuitUpgrade.Varia_Suit.value, 22, ItemClassification.progression
    ),
    SuitUpgrade.Phazon_Suit.value: ItemData(
        SuitUpgrade.Phazon_Suit.value, 23, ItemClassification.progression
    ),
    SuitUpgrade.Energy_Tank.value: ItemData(
        SuitUpgrade.Energy_Tank.value, 24, ItemClassification.useful, 14
    ),
    SuitUpgrade.Wavebuster.value: ItemData(
        SuitUpgrade.Wavebuster.value, 28, ItemClassification.useful
    ),
    SuitUpgrade.Unlimited_Missiles.value: ItemData(
        SuitUpgrade.Unlimited_Missiles.value, 41, ItemClassification.useful
    ),
    SuitUpgrade.Unlimited_Power_Bombs.value: ItemData(
        SuitUpgrade.Unlimited_Power_Bombs.value, 42, ItemClassification.useful
    ),
    SuitUpgrade.Missile_Launcher.value: ItemData(
        SuitUpgrade.Missile_Launcher.value, 43, ItemClassification.progression
    ),
    SuitUpgrade.Main_Power_Bomb.value: ItemData(
        SuitUpgrade.Main_Power_Bomb.value, 44, ItemClassification.progression
    ),
    SuitUpgrade.Spring_Ball.value: ItemData(
        SuitUpgrade.Spring_Ball.value, 45, ItemClassification.progression
    ),
    SuitUpgrade.Nothing.value: ItemData(
        SuitUpgrade.Nothing.value, 46, ItemClassification.filler
    ),
    #SuitUpgrade.Floaty_Jump.value: ItemData(
    #    SuitUpgrade.Floaty_Jump.value, 47, ItemClassification.useful
    #),
    #SuitUpgrade.Ice_Trap.value: ItemData(
    #    SuitUpgrade.Ice_Trap.value, 48, ItemClassification.trap
    #),
}

misc_item_table: Dict[str, ItemData] = {
    "UnknownItem1": ItemData("UnknownItem1", 25, ItemClassification.useful),
    "HealthRefill": ItemData(
        "HealthRefill", 26, ItemClassification.trap
    ),  # health refill address
    "UnknownItem2": ItemData("UnknownItem2", 27, ItemClassification.trap),
}

# These item ids are invalid in the player state, we'll need to exclude it from logic relying on that
custom_suit_upgrade_table: Dict[str, ItemData] = {
    ProgressiveUpgrade.Progressive_Power_Beam.value: ItemData(
        ProgressiveUpgrade.Progressive_Power_Beam.value,
        49,
        ItemClassification.progression,
        3,
    ),
    ProgressiveUpgrade.Progressive_Ice_Beam.value: ItemData(
        ProgressiveUpgrade.Progressive_Ice_Beam.value,
        51,
        ItemClassification.progression,
        3,
    ),
    ProgressiveUpgrade.Progressive_Wave_Beam.value: ItemData(
        ProgressiveUpgrade.Progressive_Wave_Beam.value,
        52,
        ItemClassification.progression,
        3,
    ),
    ProgressiveUpgrade.Progressive_Plasma_Beam.value: ItemData(
        ProgressiveUpgrade.Progressive_Plasma_Beam.value,
        53,
        ItemClassification.progression,
        3,
    ),
    ProgressiveUpgrade.Progressive_Bomb.value: ItemData(
        ProgressiveUpgrade.Progressive_Bomb.value,
        54,
        ItemClassification.progression,
        2,
    ),

    # These aren't used in item generation but are referenced in the client
    SuitUpgrade.Power_Charge_Beam.value: ItemData(
        SuitUpgrade.Power_Charge_Beam.value, 55, ItemClassification.progression, 1
    ),
    SuitUpgrade.Wave_Charge_Beam.value: ItemData(
        SuitUpgrade.Wave_Charge_Beam.value, 56, ItemClassification.progression, 1
    ),
    SuitUpgrade.Ice_Charge_Beam.value: ItemData(
        SuitUpgrade.Ice_Charge_Beam.value, 57, ItemClassification.progression, 1
    ),
    SuitUpgrade.Plasma_Charge_Beam.value: ItemData(
        SuitUpgrade.Plasma_Charge_Beam.value, 58, ItemClassification.progression, 1
    ),
}

artifact_table: Dict[str, ItemData] = {
    "Artifact of Truth": ItemData(
        "Artifact of Truth", 29, ItemClassification.progression_skip_balancing
    ),
    "Artifact of Strength": ItemData(
        "Artifact of Strength", 30, ItemClassification.progression_skip_balancing
    ),
    "Artifact of Elder": ItemData(
        "Artifact of Elder", 31, ItemClassification.progression_skip_balancing
    ),
    "Artifact of Wild": ItemData(
        "Artifact of Wild", 32, ItemClassification.progression_skip_balancing
    ),
    "Artifact of Lifegiver": ItemData(
        "Artifact of Lifegiver", 33, ItemClassification.progression_skip_balancing
    ),
    "Artifact of Warrior": ItemData(
        "Artifact of Warrior", 34, ItemClassification.progression_skip_balancing
    ),
    "Artifact of Chozo": ItemData(
        "Artifact of Chozo", 35, ItemClassification.progression_skip_balancing
    ),
    "Artifact of Nature": ItemData(
        "Artifact of Nature", 36, ItemClassification.progression_skip_balancing
    ),
    "Artifact of Sun": ItemData(
        "Artifact of Sun", 37, ItemClassification.progression_skip_balancing
    ),
    "Artifact of World": ItemData(
        "Artifact of World", 38, ItemClassification.progression_skip_balancing
    ),
    "Artifact of Spirit": ItemData(
        "Artifact of Spirit", 39, ItemClassification.progression_skip_balancing
    ),
    "Artifact of Newborn": ItemData(
        "Artifact of Newborn", 40, ItemClassification.progression_skip_balancing
    ),
}

item_table: Dict[str, ItemData] = {
    **suit_upgrade_table,
    **artifact_table,
    **custom_suit_upgrade_table,
    **misc_item_table,
}


def progressive_beam_to_beam(
    charge_beam: SuitUpgrade
) -> Optional[SuitUpgrade]:
    if charge_beam == SuitUpgrade.Power_Charge_Beam:
        return SuitUpgrade.Power_Beam
    if charge_beam == SuitUpgrade.Wave_Charge_Beam:
        return SuitUpgrade.Wave_Beam
    if charge_beam == SuitUpgrade.Ice_Charge_Beam:
        return SuitUpgrade.Ice_Beam
    if charge_beam == SuitUpgrade.Plasma_Charge_Beam:
        return SuitUpgrade.Plasma_Beam
    return None


def get_artifact_layer_from_item_index(item_id: int):
    # Artifact of truth is handled differently since it is the first thing you interact with in the room
    if item_id <= 28 or item_id > 40:
        raise Exception(f'Item {item_id} is not an artifact. So we cannot get its layer.')
    return item_id - 28 if item_id > 29 else 23